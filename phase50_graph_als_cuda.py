"""Experimental scheduling of direct prefix-QR ALS with a reusable CUDA graph.

No rank/sweep/data selection changes. Float64 cuSOLVER Jacobi SVD status stays
on device until the fit finishes, then every failure raises before scoring.
Two-pass MGS QR is checked separately against direct CPU solves/products.
This backend is not selected for the experiment until numerical controls pass.
"""
import phase50_als as als
import ctypes
from pathlib import Path
import numpy as np
import torch
from phase50_prefix_qr_cuda import nested

QR_SOURCE=r'''
__device__ double block_sum(double x,double* partial) {
  for(int d=16;d;d>>=1)x+=__shfl_down_sync(0xffffffff,x,d);
  int lane=threadIdx.x&31,warp=threadIdx.x>>5;
  if(!lane)partial[warp]=x;
  __syncthreads();
  if(threadIdx.x==0)partial[0]=partial[0]+partial[1]+partial[2]+partial[3];
  __syncthreads();return partial[0];
}
extern "C" __global__ void mgs_qr(const double* A,double* Q,double* R,int n,int r) {
  int b=blockIdx.x,t=threadIdx.x;
  __shared__ double x[128],partial[4];
  for(int z=t;z<r*r;z+=128)R[b*r*r+z]=0.0;
  __syncthreads();
  for(int j=0;j<r;j++) {
    x[t]=A[(b*n+t)*r+j];
    __syncthreads();
    for(int pass=0;pass<2;pass++)for(int k=0;k<j;k++) {
      double dot=block_sum(Q[(b*n+t)*r+k]*x[t],partial);
      if(t==0)R[b*r*r+k*r+j]+=dot;
      x[t]-=dot*Q[(b*n+t)*r+k];
      __syncthreads();
    }
    double norm=sqrt(block_sum(x[t]*x[t],partial));
    if(t==0)R[b*r*r+j*r+j]=norm;
    Q[(b*n+t)*r+j]=norm==0.0?0.0:x[t]/norm;
    __syncthreads();
  }
}
'''

_qr_kernel=None


def qr(a):
    global _qr_kernel
    import cupy as cp
    if _qr_kernel is None: _qr_kernel=cp.RawKernel(QR_SOURCE,"mgs_qr",options=("--std=c++11",))
    b,n,r=a.shape; a=a.contiguous()
    q=torch.empty_like(a); rr=torch.empty((b,r,r),device=a.device,dtype=a.dtype)
    with cp.cuda.ExternalStream(torch.cuda.current_stream().cuda_stream):
        _qr_kernel((b,),(128,),tuple(np.uint64(x.data_ptr()) for x in (a,q,rr))+(np.int32(n),np.int32(r)))
    return q,rr


class SmallSVD:
    """Square <=16 SVD; explicit device status accumulation, no hidden sync."""
    def __init__(self,batch,rank):
        import cupy as cp
        from cupy_backends.cuda.libs import cusolver as cs
        self.cs=cs; self.handle=cp.cuda.device.get_cusolver_handle()
        # CuPy's Python binding rejects all cuSOLVER calls during capture,
        # even when the installed CUDA library supports that operation. Call
        # the same already-loaded native function with explicit device status.
        self.native=ctypes.WinDLL(str(Path(torch.__file__).parent/"lib/cusolver64_11.dll"))
        self.native_set_stream=self.native.cusolverDnSetStream
        self.native_set_stream.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        self.native_set_stream.restype=ctypes.c_int
        self.native_svd=self.native.cusolverDnDgesvdjBatched
        self.native_svd.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,
                                 ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,
                                 ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_int,
                                 ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        self.native_svd.restype=ctypes.c_int
        self.params=cs.createGesvdjInfo()
        cs.xgesvdjSetTolerance(self.params,np.finfo(float).eps)
        cs.xgesvdjSetMaxSweeps(self.params,100)
        cs.xgesvdjSetSortEig(self.params,1)
        self.batch=batch; self.r=rank
        self.a=torch.empty((batch,rank,rank),device="cuda",dtype=torch.float64)
        self.u=torch.empty_like(self.a); self.v=torch.empty_like(self.a)
        self.s=torch.empty((batch,rank),device="cuda",dtype=torch.float64)
        self.info=torch.empty((batch,),device="cuda",dtype=torch.int32)
        self.failures=torch.zeros((),device="cuda",dtype=torch.int64)
        cs.setStream(self.handle,torch.cuda.current_stream().cuda_stream)
        self.lwork=cs.dgesvdjBatched_bufferSize(self.handle,cs.CUSOLVER_EIG_MODE_VECTOR,rank,rank,
                    self.a.data_ptr(),rank,self.s.data_ptr(),self.u.data_ptr(),rank,self.v.data_ptr(),rank,self.params,batch)
        self.work=torch.empty((self.lwork,),device="cuda",dtype=torch.float64)

    def __call__(self,a):
        cs=self.cs; r=self.r
        self.a.copy_(a.reshape(self.a.shape))
        status=self.native_set_stream(self.handle,torch.cuda.current_stream().cuda_stream)
        if status!=0: raise RuntimeError(f"Native cuSOLVER setStream failed: {status}")
        status=self.native_svd(self.handle,cs.CUSOLVER_EIG_MODE_VECTOR,r,r,self.a.data_ptr(),r,
                               self.s.data_ptr(),self.u.data_ptr(),r,self.v.data_ptr(),r,self.work.data_ptr(),
                               self.lwork,self.info.data_ptr(),self.params,self.batch)
        if status!=0: raise RuntimeError(f"Native cuSOLVER batched SVD launch failed: {status}")
        self.failures.add_((self.info!=0).sum())
        # cuSOLVER reads the C array as A^T and returns column-major U,V.
        # The original A therefore has U=V_cs and Vh=U_cs^T.
        return self.v.transpose(-1,-2),self.s,self.u


class SweepGraph:
    def __init__(self,target,u,v,support):
        self.b,self.n,self.r=u.shape; b,n,r=self.b,self.n,self.r
        self.target=target.clone(); self.u=u.clone(); self.v=v.clone(); self.support=support
        self.loss=((u@v.transpose(-1,-2)-target)*support).square().sum((-2,-1))
        self.svd_u=SmallSVD(b*n,r); self.svd_v=SmallSVD(b*n,r); self.svd_g=SmallSVD(b,r)
        self.log_loss=torch.empty((als.SWEEPS,b),device="cuda",dtype=torch.float64)
        self.log_trial=torch.empty_like(self.log_loss)
        self.log_gauge=torch.empty_like(self.log_loss)
        self.log_reject=torch.empty((als.SWEEPS,b),device="cuda",dtype=torch.bool)
        self.iteration=torch.zeros((1,),device="cuda",dtype=torch.long)
        self.nonfinite=torch.zeros((),device="cuda",dtype=torch.int64)
        self.graph=torch.cuda.CUDAGraph()
        side=torch.cuda.Stream(); side.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(side):
            for _ in range(3): self.step()
        torch.cuda.current_stream().wait_stream(side)
        torch.cuda.synchronize()
        with torch.cuda.graph(self.graph,stream=side): self.step()
        torch.cuda.current_stream().wait_stream(side)
        torch.cuda.synchronize()

    def solve(self,target,f,reverse,svd):
        rr,rhs=nested(target,f,reverse)
        left,s,vh=svd(rr)
        rhs=rhs.reshape(self.b*self.n,self.r)
        active=s>als.LS_RCOND*s[...,:1]
        inv=torch.where(active,s.reciprocal(),0.)
        result=(vh.transpose(-1,-2)@(inv*(left.transpose(-1,-2)@rhs.unsqueeze(-1)).squeeze(-1)).unsqueeze(-1)).squeeze(-1)
        return result.reshape(self.b,self.n,self.r)

    def balanced(self,u,v):
        both=torch.cat((u,v),0); q,r=qr(both)
        qu,qv=q[:self.b],q[self.b:]; ru,rv=r[:self.b],r[self.b:]
        left,s,vh=self.svd_g(ru@rv.transpose(-1,-2)); root=s.sqrt()[:,None,:]
        return (qu@left)*root,(qv@vh.transpose(-1,-2))*root

    def step(self):
        cu=self.solve(self.target,self.v,False,self.svd_u)
        cv=self.solve(self.target.transpose(-1,-2),cu,True,self.svd_v)
        before=(cu@cv.transpose(-1,-2))*self.support
        cu,cv=self.balanced(cu,cv)
        product=cu@cv.transpose(-1,-2)
        trial=((product-self.target)*self.support).square().sum((-2,-1))
        finite=torch.isfinite(product).all((-2,-1))&torch.isfinite(trial)
        self.nonfinite.add_((~finite).sum())
        reject=(trial>self.loss+als.MONOTONIC_TOL*torch.maximum(torch.ones_like(self.loss),self.loss))|(~finite)
        self.u.copy_(torch.where(reject[:,None,None],self.u,cu))
        self.v.copy_(torch.where(reject[:,None,None],self.v,cv))
        self.loss.copy_(torch.where(reject,self.loss,trial))
        self.log_loss.index_copy_(0,self.iteration,self.loss[None,:])
        self.log_trial.index_copy_(0,self.iteration,trial[None,:])
        self.log_gauge.index_copy_(0,self.iteration,(product*self.support-before).norm(dim=(-2,-1))[None,:])
        self.log_reject.index_copy_(0,self.iteration,reject[None,:])
        self.iteration.add_(1)

    def execute(self,target,u,v):
        self.target.copy_(target); self.u.copy_(u); self.v.copy_(v)
        self.loss.copy_(((u@v.transpose(-1,-2)-target)*self.support).square().sum((-2,-1)))
        initial=self.loss.clone(); self.iteration.zero_(); self.nonfinite.zero_()
        for solver in (self.svd_u,self.svd_v,self.svd_g): solver.failures.zero_()
        for _ in range(als.SWEEPS): self.graph.replay()
        failures=torch.stack((self.nonfinite,self.svd_u.failures,self.svd_v.failures,self.svd_g.failures)).cpu().tolist()
        if any(failures): raise FloatingPointError(f"Graph ALS nonfinite/cuSOLVER failures {failures}")
        return self.u,self.v,initial,self.log_loss,self.log_gauge,self.log_reject


_cache={}


@torch.inference_mode()
def fit(a,rank,support,initial=None):
    import time
    started=time.perf_counter(); a=a.double(); norms=a.norm(dim=(-2,-1)); safe=torch.where(norms==0,1.,norms)
    target=a/safe[:,None,None]
    if initial is None:
        left,s,vh=torch.linalg.svd(a,full_matrices=False)
        root=(s[:,:rank]/safe[:,None]).sqrt()[:,None,:]
        u,v=left[:,:,:rank]*root,vh[:,:rank,:].transpose(-1,-2)*root
    else: u,v=(x.double()/safe.sqrt()[:,None,None] for x in initial)
    key=(len(a),rank)
    if key not in _cache: _cache[key]=SweepGraph(target,u,v,support)
    graph=_cache[key]
    u,v,initial_loss,losses,gauges,rejected=graph.execute(target,u,v)
    # Reuse the ordinary backend's public diagnostic schema, evaluated in
    # double; copies below happen once after all200 graph replays.
    raw=u@v.transpose(-1,-2); residual=(raw-target)*support
    grad=((2*residual@v).square().sum((-2,-1))+(2*residual.transpose(-1,-2)@u).square().sum((-2,-1))).sqrt()
    change=(losses[-21]-losses[-1]).abs()/losses[-21].clamp_min(1e-24)
    factors=torch.cat((u.abs().flatten(1),v.abs().flatten(1)),1)*safe.sqrt()[:,None]
    minimum=torch.where(factors>0,factors,torch.full_like(factors,float("inf"))).amin(1)
    packed=torch.stack((factors.amax(1),minimum,grad,change,raw.norm(dim=(-2,-1)),gauges.amax(0)),1).cpu().tolist()
    il=initial_loss.cpu().tolist(); lc=losses.cpu().tolist(); rc=rejected.cpu().tolist(); trials=graph.log_trial.cpu().tolist()
    infos=[]; elapsed=time.perf_counter()-started
    for j,(maximum,minimum,gradient,change,unmasked,gauge) in enumerate(packed):
        if minimum==float("inf") and maximum==0.: minimum=None
        elif not np.isfinite(minimum): raise FloatingPointError("Nonfinite graph factor minimum")
        rejects=[{"sweep":s+1,"previous_loss":il[j] if s==0 else lc[s-1][j],"proposed_loss":trials[s][j],"accepted_loss":lc[s][j],
                  "direct_retry":"identical deterministic direct solve; same per-head operations"} for s in range(als.SWEEPS) if rc[s][j]]
        history=[{"sweep":s,"relative":float(np.sqrt(il[j] if s==0 else lc[s-1][j]))} for s in als.CHECKPOINTS]
        infos.append({"sweeps":als.SWEEPS,"dtype":"float64","GPU_solver":"prefix_qr_graph",
                      "initial_relative":float(np.sqrt(il[j])),"final_relative":float(np.sqrt(lc[-1][j])),"history":history,
                      "last20_relative_objective_change":change,"gradient_normalized_target":gradient,
                      "converged":bool(gradient<=1e-6 and (change<=1e-7 or lc[-1][j]<=1e-12) and (not rejects or lc[-1][j]<=1e-12)),
                      "direct_LS_blocks":2*128*als.SWEEPS,"direct_sweep_retries":len(rejects),"rejected_sweeps":rejects,
                      "maximum_absolute_factor":maximum,"minimum_nonzero_absolute_factor":minimum,
                      "factor_dynamic_range":maximum/minimum if minimum is not None else 0.,
                      "unmasked_product_norm_over_target":unmasked,"maximum_QR_observed_product_error":gauge,"seconds":elapsed})
    return raw*safe[:,None,None],infos
