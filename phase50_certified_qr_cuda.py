"""Direct causal least squares with certified triangular/complete QR solves.

All singular values must be above the existing1e-12 cutoff before the fast
solve is used. The conservative bound1/(||R||F ||R^-1||F)>4e-12 certifies this.
Short prefixes/suffixes use QR of the transposed full-row-rank triangular
block for the minimum-norm solution. Every uncertified block uses the original
direct small SVD, including all nonstructural rank deficiencies. No Gram solve,
regularization, altered rank cutoff, or nonfinite replacement is introduced.
"""
import phase50_als as als
import numpy as np
import torch
from phase50_prefix_qr_cuda import nested

SOURCE=r'''
__device__ double warp_sum(double v) {
  for(int d=16;d;d>>=1)v+=__shfl_down_sync(0xffffffff,v,d);
  return __shfl_sync(0xffffffff,v,0);
}
extern "C" __global__ void certified_solve(const double* R,const double* H,
    double* OUT,int* BAD,int n,int r,int reverse,double cutoff) {
  int z=blockIdx.x,t=threadIdx.x,i=z%n;
  int observed=reverse?n-i:i+1,q=observed<r?observed:r;
  const double* rr=R+z*r*r;const double* h=H+z*r;
  __shared__ double Q[256],T[256],inverse[256],col[16],sol[16],coef;
  __shared__ int bad;
  for(int j=t;j<r*r;j+=32){Q[j]=0.0;T[j]=0.0;inverse[j]=0.0;}
  if(t==0)bad=0;
  __syncwarp();
  if(q<r) {
    // R_top^T=Q*T, with two-pass MGS. Its q singular values equal
    // the nonzero singular values of the original short design.
    for(int j=0;j<q;j++) {
      if(t<r)col[t]=rr[j*r+t];
      __syncwarp();
      for(int pass=0;pass<2;pass++)for(int k=0;k<j;k++) {
        double dot=warp_sum(t<r?Q[t*r+k]*col[t]:0.0);
        if(t==0)T[k*r+j]+=dot;
        if(t<r)col[t]-=dot*Q[t*r+k];
        __syncwarp();
      }
      double norm=sqrt(warp_sum(t<r?col[t]*col[t]:0.0));
      if(t==0){T[j*r+j]=norm;if(norm==0.0)bad=1;}
      if(t<r)Q[t*r+j]=norm==0.0?0.0:col[t]/norm;
      __syncwarp();
    }
    // Structural zero rows must actually be zero; otherwise use SVD.
    double tail=0.0;
    for(int j=t;j<r*r;j+=32)if(j/r>=q)tail+=rr[j]*rr[j];
    if(warp_sum(tail)!=0.0 && t==0)bad=1;
  } else {
    for(int j=t;j<r*r;j+=32)T[j]=rr[j];
  }
  __syncwarp();
  // Explicit inverse only supplies a conservative condition-number bound.
  // The solution itself below is obtained by triangular substitution.
  for(int row=q-1;row>=0;row--) {
    if(t<q) {
      double value=row==t?1.0:0.0;
      for(int j=row+1;j<q;j++)value-=T[row*r+j]*inverse[j*r+t];
      double diagonal=T[row*r+row];
      inverse[row*r+t]=diagonal==0.0?0.0:value/diagonal;
    }
    if(t==0 && T[row*r+row]==0.0)bad=1;
    __syncwarp();
  }
  double ns=0.0,ni=0.0;
  for(int j=t;j<r*r;j+=32){ns+=T[j]*T[j];ni+=inverse[j]*inverse[j];}
  double condition=sqrt(warp_sum(ns))*sqrt(warp_sum(ni));
  if(t==0 && (!(condition>0.0)||!isfinite(condition)||1.0/condition<=4.0*cutoff))bad=1;
  __syncwarp();
  if(bad){if(t==0)BAD[z]=1;return;}
  if(q==r) {
    for(int row=r-1;row>=0;row--) {
      if(t==0){double value=h[row];for(int j=row+1;j<r;j++)value-=rr[row*r+j]*sol[j];sol[row]=value/rr[row*r+row];}
      __syncwarp();
    }
    if(t<r)OUT[z*r+t]=sol[t];
  } else {
    for(int row=0;row<q;row++) {
      if(t==0){double value=h[row];for(int j=0;j<row;j++)value-=T[j*r+row]*sol[j];sol[row]=value/T[row*r+row];}
      __syncwarp();
    }
    if(t<r){double value=0.0;for(int j=0;j<q;j++)value+=Q[t*r+j]*sol[j];OUT[z*r+t]=value;}
  }
  if(t==0)BAD[z]=0;
}
'''

_kernel=None


def update(a,f,support,reverse=False,direct=False):
    global _kernel
    import cupy as cp
    if _kernel is None:_kernel=cp.RawKernel(SOURCE,"certified_solve",options=("--std=c++11",))
    rr,rhs=nested(a,f,reverse);b,n,r=f.shape
    if direct:
        left,s,vh=torch.linalg.svd(rr,full_matrices=False)
        active=s>als.LS_RCOND*s[...,:1]
        inv=torch.where(active,s.reciprocal(),0.)
        out=(vh.transpose(-1,-2)@(inv*(left.transpose(-1,-2)@rhs.unsqueeze(-1)).squeeze(-1)).unsqueeze(-1)).squeeze(-1)
        return out,b*n
    # Raw kernels write C-order storage. SVD initial factors can have a
    # transposed/column-major layout; empty_like would preserve that layout.
    out=torch.empty(f.shape,device=f.device,dtype=f.dtype)
    bad=torch.empty((b,n),device=f.device,dtype=torch.int32)
    with cp.cuda.ExternalStream(torch.cuda.current_stream().cuda_stream):
        _kernel((b*n,),(32,),tuple(np.uint64(x.data_ptr()) for x in (rr,rhs,out,bad))+
                (np.int32(n),np.int32(r),np.int32(reverse),np.float64(als.LS_RCOND)))
    idx=bad.nonzero()
    if len(idx):
        bi,i=idx.unbind(1)
        left,s,vh=torch.linalg.svd(rr[bi,i],full_matrices=False)
        active=s>als.LS_RCOND*s[...,:1]
        inv=torch.where(active,s.reciprocal(),0.)
        out[bi,i]=(vh.transpose(-1,-2)@(inv*(left.transpose(-1,-2)@rhs[bi,i].unsqueeze(-1)).squeeze(-1)).unsqueeze(-1)).squeeze(-1)
    return out,len(idx)
