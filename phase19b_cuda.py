"""Fused exact sparse rendering of C2 tapered Gaussian lines, via CUDA NVRTC.

CuPy supplies compilation and launch only. All allocations, parameters,
optimization, streams, and the autograd interface remain in PyTorch. Called
only by a worker launched under flock /tmp/radon-gpu.lock.
"""
import os
from pathlib import Path
import numpy as np
import torch


SOURCE = r'''
__device__ float reduce_sum(float v) {
  __shared__ float partial[8];
  for (int d=16; d; d>>=1) v += __shfl_down_sync(0xffffffff, v, d);
  int lane=threadIdx.x&31, warp=threadIdx.x>>5;
  if (!lane) partial[warp]=v;
  __syncthreads();
  v=(threadIdx.x<8)?partial[lane]:0.0f;
  if (!warp) for (int d=16; d; d>>=1) v += __shfl_down_sync(0xffffffff, v, d);
  __syncthreads();
  return v;
}
__device__ float reduce_max(float v) {
  __shared__ float partial[8];
  for(int d=16;d;d>>=1)v=fmaxf(v,__shfl_down_sync(0xffffffff,v,d));
  int lane=threadIdx.x&31,warp=threadIdx.x>>5;
  if(!lane)partial[warp]=v;
  __syncthreads();
  v=(threadIdx.x<8)?partial[lane]:-1e30f;
  if(!warp)for(int d=16;d;d>>=1)v=fmaxf(v,__shfl_down_sync(0xffffffff,v,d));
  __syncthreads();return v;
}
__device__ bool geometry(int z,int n,int span,int half,bool dense,bool dom,
    float c,float s,float r,float w,int &pix,float &q,float &t) {
  int axis=z/span,v=z%span,ii,jj;
  float center=0.5f*(n-1);
  if(dense) {ii=axis;jj=v;}
  else {
    float den=dom?c:s,other=dom?s:c;
    int near=(int)floorf((r-other*(axis-center))/den+center)+v-half-1;
    ii=dom?axis:near; jj=dom?near:axis;
  }
  if(jj<0||ii<0||ii>=n||jj>ii) return false;
  float x=jj-center,y=ii-center;
  q=(c*x+s*y-r)/w;
  if(fabsf(q)>=6) return false;
  t=(-s*x+c*y)/n; pix=ii*(ii+1)/2+jj;
  return true;
}
__device__ float value(float q,float t,float decay) {
  float v=fmaxf(1-q*q/36,0.0f);
  return expf(-0.5f*q*q-decay*t)*v*v*v;
}
__device__ float logvalue(float q,float t,float decay) {
  return -0.5f*q*q-decay*t+3*logf(fmaxf(1-q*q/36,1e-30f));
}
extern "C" __global__ void norms(const float* th,const float* rho,const float* lw,
  const float* de,float* norms,float* shifts,int n) {
  int a=blockIdx.x;float c=cosf(th[a]),s=sinf(th[a]),w=expf(lw[a]),r=rho[a];
  bool dom=fabsf(c)>=fabsf(s);float den=dom?c:s;
  int half=(int)ceilf(6*w/fabsf(den))+1,span=2*half+3;
  bool dense=span>=n;if(dense) span=n;
  float maximum=-1e30f;
  for(int z=threadIdx.x;z<n*span;z+=blockDim.x) {
    int pix;float q,t;
    if(geometry(z,n,span,half,dense,dom,c,s,r,w,pix,q,t)) {
      maximum=fmaxf(maximum,logvalue(q,t,de[a]));
    }
  }
  maximum=reduce_max(maximum);
  __shared__ float shift;
  if(threadIdx.x==0)shift=maximum;
  __syncthreads();
  if(shift==-1e30f){if(threadIdx.x==0){norms[a]=1;shifts[a]=0;}return;}
  float sum=0;
  for(int z=threadIdx.x;z<n*span;z+=blockDim.x) {
    int pix;float q,t;
    if(geometry(z,n,span,half,dense,dom,c,s,r,w,pix,q,t)) {
      float v=expf(logvalue(q,t,de[a])-shift);sum+=v*v;
    }
  }
  sum=reduce_sum(sum);
  if(threadIdx.x==0){norms[a]=sqrtf(sum);shifts[a]=shift;}
}
extern "C" __global__ void render(const float* th,const float* rho,const float* lw,
  const float* de,const float* amp,const float* norms,const float* shifts,float* out,int n,int k) {
  int a=blockIdx.x;float c=cosf(th[a]),s=sinf(th[a]),w=expf(lw[a]),r=rho[a];
  bool dom=fabsf(c)>=fabsf(s);float den=dom?c:s;
  int half=(int)ceilf(6*w/fabsf(den))+1,span=2*half+3;
  bool dense=span>=n;if(dense)span=n;
  int base=(a/k)*(n*(n+1)/2);
  for(int z=threadIdx.x;z<n*span;z+=blockDim.x) {
    int pix;float q,t;
    if(geometry(z,n,span,half,dense,dom,c,s,r,w,pix,q,t))
      atomicAdd(out+base+pix,amp[a]*expf(logvalue(q,t,de[a])-shifts[a])/norms[a]);
  }
}
extern "C" __global__ void backward(const float* th,const float* rho,const float* lw,
  const float* de,const float* amp,const float* norms,const float* shifts,const float* go,
  float* gth,float* gr,float* glw,float* gd,float* ga,int n,int k) {
  int a=blockIdx.x;float c=cosf(th[a]),s=sinf(th[a]),w=expf(lw[a]),r=rho[a];
  bool dom=fabsf(c)>=fabsf(s);float den=dom?c:s;
  int half=(int)ceilf(6*w/fabsf(den))+1,span=2*half+3;
  bool dense=span>=n;if(dense)span=n;
  int base=(a/k)*(n*(n+1)/2);float v[9]={0,0,0,0,0,0,0,0,0};
  for(int z=threadIdx.x;z<n*span;z+=blockDim.x) {
    int pix;float q,t;
    if(geometry(z,n,span,half,dense,dom,c,s,r,w,pix,q,t)) {
      float u=expf(logvalue(q,t,de[a])-shifts[a])/norms[a],eu=go[base+pix]*u,uu=u*u;
      float f=-q-6*q/fmaxf(36-q*q,1e-8f);
      float deriv[4]={f*t*n/w+de[a]*(r+w*q)/n,-f/w,-f*q,-t};
      v[8]+=eu;
      for(int j=0;j<4;j++){v[j]+=eu*deriv[j];v[4+j]+=uu*deriv[j];}
    }
  }
  float total[9];for(int j=0;j<9;j++)total[j]=reduce_sum(v[j]);
  if(threadIdx.x==0) {
    float e=total[8];
    gth[a]=amp[a]*(total[0]-e*total[4]);gr[a]=amp[a]*(total[1]-e*total[5]);
    glw[a]=amp[a]*(total[2]-e*total[6]);gd[a]=amp[a]*(total[3]-e*total[7]);ga[a]=e;
  }
}
'''

_kernels = None


def kernels():
    global _kernels
    if _kernels is None:
        if os.environ.get("RICHLINE_GPU_LOCK")!="1":
            raise RuntimeError("CUDA renderer requires the outer GPU lock")
        os.environ["CUPY_CACHE_DIR"]=str(Path("out/phase19b_cuda_cache").resolve())
        import cupy as cp
        module=cp.RawModule(code=SOURCE,options=("--std=c++11",))
        _kernels=(cp,{name:module.get_function(name) for name in ["norms","render","backward"]})
    return _kernels


def ptr(tensor):
    if not tensor.is_contiguous():
        raise ValueError("Fused renderer requires contiguous tensors")
    return np.uint64(tensor.data_ptr())


class CudaRenderLines(torch.autograd.Function):
    @staticmethod
    def forward(ctx,theta,rho,logwidth,decay,amplitude,x,y,n):
        cp,functions=kernels()
        starts,k=theta.shape
        norm=torch.empty_like(theta);shift=torch.empty_like(theta)
        result=torch.zeros((starts,n*(n+1)//2),device=theta.device,dtype=torch.float32)
        with cp.cuda.ExternalStream(torch.cuda.current_stream().cuda_stream):
            functions["norms"]((theta.numel(),),(256,),
                tuple(map(ptr,(theta,rho,logwidth,decay,norm,shift)))+(np.int32(n),))
            functions["render"]((theta.numel(),),(256,),
                tuple(map(ptr,(theta,rho,logwidth,decay,amplitude,norm,shift,result)))+(np.int32(n),np.int32(k)))
        ctx.save_for_backward(theta,rho,logwidth,decay,amplitude,norm,shift)
        ctx.n=n
        return result

    @staticmethod
    def backward(ctx,grad_output):
        cp,functions=kernels()
        params=ctx.saved_tensors
        grads=[torch.empty_like(params[0]) for _ in range(5)]
        grad_output=grad_output.contiguous()
        with cp.cuda.ExternalStream(torch.cuda.current_stream().cuda_stream):
            functions["backward"]((params[0].numel(),),(256,),
                tuple(map(ptr,(*params,grad_output,*grads)))+(np.int32(ctx.n),np.int32(params[0].shape[1])))
        return *grads,None,None,None


def check_cuda_renderer():
    from richlines_parametric import DenseRenderLines,torch_grid
    torch.manual_seed(19027)
    n=31;x,y=torch_grid(n,"cuda")
    params=[torch.nn.Parameter(p.contiguous()) for p in [torch.rand(3,7,device="cuda")*np.pi,
            (torch.rand(3,7,device="cuda")-0.5)*n,torch.rand(3,7,device="cuda")*2-0.5,
            torch.rand(3,7,device="cuda")*8-4,torch.rand(3,7,device="cuda")]]
    dense=DenseRenderLines.apply(*params,x,y,n)
    weight=torch.randn_like(dense)
    (dense*weight).sum().backward()
    reference=[p.grad.clone() for p in params]
    for p in params:p.grad=None
    actual=CudaRenderLines.apply(*params,x,y,n)
    (actual*weight).sum().backward()
    forward=float((dense-actual).abs().max())
    grad=[float(((p.grad-r).abs()/(1+r.abs())).max()) for p,r in zip(params,reference)]
    if forward>2e-5 or max(grad)>2e-4:
        raise AssertionError(f"CUDA renderer mismatch: forward={forward}, gradients={grad}")
    # Regression for a near-empty footprint that formerly underflowed in fp32.
    edge=[torch.nn.Parameter(torch.tensor([[v]],device="cuda",dtype=torch.float32)) for v in
          [2.174210786819458,-18.420080184936523,-1.017950177192688,3.790337085723877,0.006468346808105707]]
    ex,ey=torch_grid(128,"cuda")
    footprint=CudaRenderLines.apply(*edge,ex,ey,128)
    ratio=float(footprint.norm()/edge[4][0,0])
    footprint.square().sum().backward()
    finite=all(bool(torch.isfinite(p.grad).all()) for p in edge)
    if abs(ratio-1)>1e-5 or not finite:
        raise AssertionError(f"Near-empty line regression failed: norm ratio {ratio}, finite {finite}")
    return {"forward_max_absolute":forward,"gradient_max_scaled_absolute":grad,
            "forward_tolerance":2e-5,"gradient_tolerance":2e-4,"n":n,"passed":True,
            "near_empty_footprint_norm_ratio":ratio,"near_empty_footprint_gradients_finite":finite}
