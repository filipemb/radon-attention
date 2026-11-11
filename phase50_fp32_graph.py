"""Captured FP32 cumulative-Gram sweeps; explicit device error checks.

The row solves are batched Cholesky, not an iterative or truncated substitute.
FP32 QR uses two-pass modified Gram-Schmidt; the small SVD is cuSOLVER Sgesvdj.
"""
import ctypes
from pathlib import Path
import numpy as np
import torch
import phase50_fp32_als as als

SOURCE=r'''
extern "C" __global__ void gram_solve(const float* G,const float* H,float* X,
                                     int r,int* failures) {
  int b=blockIdx.x,t=threadIdx.x;
  __shared__ float L[256],x[16],pivot,lambda;
  if(t==0) {
    float trace=0.f;for(int j=0;j<r;j++)trace+=G[b*r*r+j*r+j];
    lambda=fmaxf(1e-6f*trace,1e-30f);
  }
  for(int z=t;z<r*r;z+=32)L[z]=G[b*r*r+z];
  __syncwarp();
  if(t<r)L[t*r+t]+=lambda;
  __syncwarp();
  for(int j=0;j<r;j++) {
    if(t==j) {
      float d=L[j*r+j];for(int k=0;k<j;k++)d-=L[j*r+k]*L[j*r+k];
      if(!(d>0.f) || !isfinite(d)) {atomicAdd(failures,1);pivot=nanf("");}
      else pivot=sqrtf(d);
      L[j*r+j]=pivot;
    }
    __syncwarp();
    if(t>j && t<r) {
      float s=L[t*r+j];for(int k=0;k<j;k++)s-=L[t*r+k]*L[j*r+k];
      L[t*r+j]=s/pivot;
    }
    __syncwarp();
  }
  if(t<r)x[t]=H[b*r+t];
  __syncwarp();
  for(int j=0;j<r;j++) {
    if(t==j)x[j]/=L[j*r+j];
    __syncwarp();
    if(t>j && t<r)x[t]-=L[t*r+j]*x[j];
    __syncwarp();
  }
  for(int j=r-1;j>=0;j--) {
    if(t==j)x[j]/=L[j*r+j];
    __syncwarp();
    if(t<j)x[t]-=L[j*r+t]*x[j];
    __syncwarp();
  }
  if(t<r)X[b*r+t]=x[t];
}
__device__ float block_sum(float x,float* partial) {
  for(int d=16;d;d>>=1)x+=__shfl_down_sync(0xffffffff,x,d);
  int lane=threadIdx.x&31,warp=threadIdx.x>>5;
  if(!lane)partial[warp]=x;
  __syncthreads();
  if(threadIdx.x==0)partial[0]=partial[0]+partial[1]+partial[2]+partial[3];
  __syncthreads();return partial[0];
}
extern "C" __global__ void mgs_qr(const float* A,float* Q,float* R,int n,int r) {
  int b=blockIdx.x,t=threadIdx.x;
  __shared__ float x[128],partial[4];
  for(int z=t;z<r*r;z+=128)R[b*r*r+z]=0.f;
  __syncthreads();
  for(int j=0;j<r;j++) {
    x[t]=A[(b*n+t)*r+j];__syncthreads();
    for(int pass=0;pass<2;pass++)for(int k=0;k<j;k++) {
      float dot=block_sum(Q[(b*n+t)*r+k]*x[t],partial);
      if(t==0)R[b*r*r+k*r+j]+=dot;
      x[t]-=dot*Q[(b*n+t)*r+k];__syncthreads();
    }
    float norm=sqrtf(block_sum(x[t]*x[t],partial));
    if(t==0)R[b*r*r+j*r+j]=norm;
    Q[(b*n+t)*r+j]=norm==0.f?0.f:x[t]/norm;__syncthreads();
  }
}
'''
_solve=None
_qr=None

def solve(gram,rhs,failures):
    global _solve
    import cupy as cp
    if _solve is None:_solve=cp.RawKernel(SOURCE,'gram_solve',options=('--std=c++11','--fmad=false'))
    gram=gram.contiguous();rhs=rhs.contiguous();r=rhs.shape[-1]
    result=torch.empty(rhs.shape,device=rhs.device,dtype=torch.float32)
    with cp.cuda.ExternalStream(torch.cuda.current_stream().cuda_stream):
        _solve((rhs.numel()//r,),(32,),tuple(np.uint64(x.data_ptr()) for x in (gram,rhs,result))+(np.int32(r),np.uint64(failures.data_ptr())))
    return result

def qr(a):
    global _qr
    import cupy as cp
    if _qr is None:_qr=cp.RawKernel(SOURCE,'mgs_qr',options=('--std=c++11','--fmad=false'))
    a=a.contiguous();b,n,r=a.shape
    q=torch.empty(a.shape,device=a.device,dtype=a.dtype);rr=torch.empty((b,r,r),device=a.device,dtype=a.dtype)
    with cp.cuda.ExternalStream(torch.cuda.current_stream().cuda_stream):
        _qr((b,),(128,),tuple(np.uint64(x.data_ptr()) for x in (a,q,rr))+(np.int32(n),np.int32(r)))
    return q,rr

class SmallSVD:
    def __init__(self,batch,r):
        import cupy as cp
        from cupy_backends.cuda.libs import cusolver as cs
        self.cs=cs;self.handle=cp.cuda.device.get_cusolver_handle();self.batch=batch;self.r=r
        self.native=ctypes.WinDLL(str(Path(torch.__file__).parent/'lib/cusolver64_11.dll'))
        self.set_stream=self.native.cusolverDnSetStream
        self.set_stream.argtypes=[ctypes.c_void_p,ctypes.c_void_p];self.set_stream.restype=ctypes.c_int
        self.native_svd=self.native.cusolverDnSgesvdjBatched
        self.native_svd.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,
            ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,
            ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        self.native_svd.restype=ctypes.c_int
        self.params=cs.createGesvdjInfo();cs.xgesvdjSetTolerance(self.params,1e-7)
        cs.xgesvdjSetMaxSweeps(self.params,100);cs.xgesvdjSetSortEig(self.params,1)
        self.a=torch.empty((batch,r,r),device='cuda',dtype=torch.float32)
        self.u=torch.empty_like(self.a);self.v=torch.empty_like(self.a);self.s=torch.empty((batch,r),device='cuda')
        self.info=torch.empty((batch,),device='cuda',dtype=torch.int32)
        self.failures=torch.zeros((),device='cuda',dtype=torch.int64)
        cs.setStream(self.handle,torch.cuda.current_stream().cuda_stream)
        self.lwork=cs.sgesvdjBatched_bufferSize(self.handle,cs.CUSOLVER_EIG_MODE_VECTOR,r,r,self.a.data_ptr(),r,
            self.s.data_ptr(),self.u.data_ptr(),r,self.v.data_ptr(),r,self.params,batch)
        self.work=torch.empty((self.lwork,),device='cuda',dtype=torch.float32)
    def __call__(self,a):
        r=self.r;self.a.copy_(a)
        status=self.set_stream(self.handle,torch.cuda.current_stream().cuda_stream)
        if status:raise RuntimeError(f'cuSOLVER setStream status {status}')
        status=self.native_svd(self.handle,self.cs.CUSOLVER_EIG_MODE_VECTOR,r,r,self.a.data_ptr(),r,self.s.data_ptr(),
            self.u.data_ptr(),r,self.v.data_ptr(),r,self.work.data_ptr(),self.lwork,self.info.data_ptr(),self.params,self.batch)
        if status:raise RuntimeError(f'cuSOLVER FP32 SVD status {status}')
        self.failures.add_((self.info!=0).sum())
        return self.v.transpose(-1,-2),self.s,self.u

class SweepGraph:
    def __init__(self,target,u,v,support):
        self.b,self.n,self.r=u.shape;b,n,r=self.b,self.n,self.r
        self.target=target.clone();self.u=u.clone();self.v=v.clone();self.support=support
        self.losses=torch.empty((als.SWEEPS,b),device='cuda');self.gauges=torch.empty_like(self.losses)
        self.iteration=torch.zeros((1,),device='cuda',dtype=torch.int64)
        self.failures=torch.zeros((),device='cuda',dtype=torch.int32)
        self.nonfinite=torch.zeros((),device='cuda',dtype=torch.int64);self.svd=SmallSVD(b,r)
        self.graph=torch.cuda.CUDAGraph();side=torch.cuda.Stream();side.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(side):
            for _ in range(3):self.step()
        torch.cuda.current_stream().wait_stream(side);torch.cuda.synchronize()
        with torch.cuda.graph(self.graph,stream=side):self.step()
        torch.cuda.current_stream().wait_stream(side);torch.cuda.synchronize()
    def update(self,target,f,reverse=False):
        outer=f.unsqueeze(-1)*f.unsqueeze(-2)
        gram=outer.flip(1).cumsum(1).flip(1) if reverse else outer.cumsum(1)
        return solve(gram,target@f,self.failures)
    def step(self):
        cu=self.update(self.target,self.v);cv=self.update(self.target.transpose(-1,-2),cu,True)
        before=(cu@cv.transpose(-1,-2))*self.support
        q,r=qr(torch.cat((cu,cv),0));qu,qv=q.chunk(2);ru,rv=r.chunk(2)
        left,s,vh=self.svd(ru@rv.transpose(-1,-2));root=s.sqrt()[:,None,:]
        self.u.copy_((qu@left)*root);self.v.copy_((qv@vh.transpose(-1,-2))*root)
        product=self.u@self.v.transpose(-1,-2)
        loss=((product-self.target)*self.support).square().sum((-2,-1))
        gauge=(product*self.support-before).norm(dim=(-2,-1))
        self.nonfinite.add_((~torch.isfinite(product)).sum()+(~torch.isfinite(loss)).sum()+(~torch.isfinite(gauge)).sum())
        self.losses.index_copy_(0,self.iteration,loss[None]);self.gauges.index_copy_(0,self.iteration,gauge[None])
        self.iteration.add_(1)
    def execute(self,target,u,v):
        self.target.copy_(target);self.u.copy_(u);self.v.copy_(v);self.iteration.zero_()
        self.failures.zero_();self.nonfinite.zero_();self.svd.failures.zero_()
        for _ in range(als.SWEEPS):self.graph.replay()
        status=torch.stack((self.failures.long(),self.nonfinite,self.svd.failures)).cpu().tolist()
        if any(status):raise FloatingPointError(f'FP32 graph failed Cholesky/nonfinite/SVD {status}; no fallback')
        return self.u,self.v,self.losses,self.gauges

_cache={}

@torch.inference_mode()
def fit_graph(a,rank,support,initial=None):
    import time
    started=time.perf_counter();a=a.float()
    if a.shape[-2:]!=(128,128) or not a.is_cuda or not bool(torch.isfinite(a).all()) or bool((a*~support).any()):
        raise ValueError('FP32 estimator requires finite CUDA causal n128 matrices')
    norms=a.norm(dim=(-2,-1));safe=torch.where(norms==0,1.,norms);target=a/safe[:,None,None]
    if initial is None:
        left,s,vh=torch.linalg.svd(a,full_matrices=False);root=(s[:,:rank]/safe[:,None]).sqrt()[:,None,:]
        u,v=left[:,:,:rank]*root,vh[:,:rank,:].transpose(-1,-2)*root
    else:u,v=(x.float()/safe.sqrt()[:,None,None] for x in initial)
    initial_loss=((u@v.transpose(-1,-2)-target)*support).square().sum((-2,-1))
    key=(len(a),rank)
    if key not in _cache:_cache[key]=SweepGraph(target,u,v,support)
    u,v,losses,gauges=_cache[key].execute(target,u,v)
    return als.finish(u,v,target,safe,support,initial_loss,losses,gauges,started,'graph')
