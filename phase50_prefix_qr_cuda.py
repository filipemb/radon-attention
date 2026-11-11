"""Streaming prefix/suffix QR for E9 least squares (double, no Gram matrices).

The estimator accumulates QR of each nested design once, applying the same
Givens rotations to all right-hand sides. Small triangular factors go to the
same direct SVD least-squares cutoff. Attention projection remains in V1.
CUDA launches are restricted to the worker's existing outer GPU lock.
"""
import phase50_als
import numpy as np
import torch

SOURCE=r'''
extern "C" __global__ void nested_qr(const double* A,const double* F,
    double* OUT_R,double* OUT_H,int n,int r,int reverse) {
  int b=blockIdx.x,t=threadIdx.x;
  extern __shared__ double work[];
  double* R=work;
  double* H=R+r*r;
  double* incoming=H+r*n;
  double* rhs=incoming+r;
  double* cs=rhs+n;
  for(int z=t;z<r*r+r*n;z+=blockDim.x)work[z]=0.0;
  __syncthreads();
  for(int step=0;step<n;step++) {
    int i=reverse?n-1-step:step;
    if(t<r)incoming[t]=F[(b*n+i)*r+t];
    if(t<n)rhs[t]=A[(b*n+t)*n+i];
    __syncthreads();
    for(int j=0;j<r;j++) {
      if(t==0) {
        double x=R[j*r+j],y=incoming[j],radius=hypot(x,y);
        cs[0]=radius==0.0?1.0:x/radius;
        cs[1]=radius==0.0?0.0:y/radius;
      }
      __syncthreads();
      double c=cs[0],s=cs[1];
      if(t>=j && t<r) {
        double old=R[j*r+t],next=incoming[t];
        R[j*r+t]=c*old+s*next;
        incoming[t]=-s*old+c*next;
      }
      if(t<n) {
        double old=H[j*n+t],next=rhs[t];
        H[j*n+t]=c*old+s*next;
        rhs[t]=-s*old+c*next;
      }
      __syncthreads();
    }
    for(int z=t;z<r*r;z+=blockDim.x)OUT_R[((b*n+i)*r*r)+z]=R[z];
    if(t<r)OUT_H[(b*n+i)*r+t]=H[t*n+i];
    __syncthreads();
  }
}
'''

_kernel=None


def nested(a,f,reverse):
    global _kernel
    import cupy as cp
    if _kernel is None:
        _kernel=cp.RawKernel(SOURCE,"nested_qr",options=("--std=c++11",))
    a=a.contiguous(); f=f.contiguous()
    b,n,r=f.shape
    if a.shape!=(b,n,n) or n!=128 or r>16 or f.dtype!=torch.float64 or a.dtype!=torch.float64:
        raise ValueError("Declared double square n128, rank<=16 required")
    triangular=torch.empty((b,n,r,r),dtype=f.dtype,device=f.device)
    rhs=torch.empty_like(f)
    ptr=lambda x:np.uint64(x.data_ptr())
    shared=8*(r*r+r*n+r+n+2)
    with cp.cuda.ExternalStream(torch.cuda.current_stream().cuda_stream):
        _kernel((b,),(128,),(ptr(a),ptr(f),ptr(triangular),ptr(rhs),np.int32(n),np.int32(r),np.int32(reverse)),shared_mem=shared)
    return triangular,rhs


def update(a,f,support,reverse=False,direct=False):
    triangular,rhs=nested(a,f,reverse)
    left,singular,vh=torch.linalg.svd(triangular,full_matrices=False)
    active=singular>phase50_als.LS_RCOND*singular[...,:1]
    inv=torch.where(active,singular.reciprocal(),0.)
    out=(vh.transpose(-1,-2)@(inv*(left.transpose(-1,-2)@rhs.unsqueeze(-1)).squeeze(-1)).unsqueeze(-1)).squeeze(-1)
    return out,len(a)*a.shape[1]
