"""Optional algebra-preserving FP32 QR norm overflow repair, not yet a policy.

The ordinary finite squared-norm path is unchanged. Only a squared sum that
overflows for a finite vector is recomputed with max scaling, still in FP32.
No ridge, SVD initialization, sweep, factor rank or convergence rule changes.
Installation requires a separately audited, explicit implementation-fix record.
"""
import numpy as np
import torch
import phase50_fp32_als as als
import phase50_fp32_graph as base

MAX_SOURCE=r'''
__device__ float block_maximum(float x,float* partial) {
  for(int d=16;d;d>>=1)x=fmaxf(x,__shfl_down_sync(0xffffffff,x,d));
  int lane=threadIdx.x&31,warp=threadIdx.x>>5;
  if(!lane)partial[warp]=x;
  __syncthreads();
  if(threadIdx.x==0)partial[0]=fmaxf(fmaxf(partial[0],partial[1]),fmaxf(partial[2],partial[3]));
  __syncthreads();return partial[0];
}
'''
SOURCE=base.SOURCE.replace('extern "C" __global__ void mgs_qr(',MAX_SOURCE+'\nextern "C" __global__ void mgs_qr(')
SOURCE=SOURCE.replace('float* R,int n,int r) {','float* R,int n,int r,int* repairs) {')
OLD='float norm=sqrtf(block_sum(x[t]*x[t],partial));'
NEW=r'''
    float square_sum=block_sum(x[t]*x[t],partial);
    float norm=sqrtf(square_sum);
    if(isinf(square_sum)) {
      float scale=block_maximum(fabsf(x[t]),partial);
      if(isfinite(scale) && scale>0.f) {
        float scaled=x[t]/scale;
        norm=scale*sqrtf(block_sum(scaled*scaled,partial));
        if(t==0)atomicAdd(repairs+b,1);
      }
    }
'''
if SOURCE.count(OLD)!=1:raise AssertionError('Original QR source layout changed')
SOURCE=SOURCE.replace(OLD,NEW)
_kernel=None
_counts=None
_installed=False
_last=None

def qr(a):
    global _kernel,_counts
    import cupy as cp
    if _kernel is None:_kernel=cp.RawKernel(SOURCE,'mgs_qr',options=('--std=c++11','--fmad=false'))
    if _counts is None:_counts=torch.zeros(256,device='cuda',dtype=torch.int32)
    a=a.contiguous();b,n,r=a.shape
    if b>len(_counts) or n!=128 or r>16 or a.dtype!=torch.float32:raise ValueError('Declared FP32 QR dimensions exceeded')
    q=torch.empty(a.shape,device=a.device,dtype=a.dtype);rr=torch.empty((b,r,r),device=a.device,dtype=a.dtype)
    with cp.cuda.ExternalStream(torch.cuda.current_stream().cuda_stream):
        _kernel((b,),(128,),tuple(np.uint64(x.data_ptr()) for x in (a,q,rr))+(np.int32(n),np.int32(r),np.uint64(_counts.data_ptr())))
    return q,rr

def install():
    global _installed,_counts
    if _installed:return
    if base._cache:raise RuntimeError('Install implementation repair before any graph is cached')
    if _counts is None:_counts=torch.zeros(256,device='cuda',dtype=torch.int32)
    old_execute=base.SweepGraph.execute;old_fit=als.fit
    def execute(self,target,u,v):
        global _last
        _counts.zero_();result=old_execute(self,target,u,v)
        _last=_counts[:2*self.b].cpu().tolist()
        return result
    def fit(a,rank,support,initial=None,backend='torch'):
        if backend!='graph':raise ValueError('The controlled implementation repair is for the declared graph backend')
        product,infos=old_fit(a,rank,support,initial,backend)
        b=len(infos)
        for j,info in enumerate(infos):
            info['QR_overflow_safe_norm_recomputations_U']=int(_last[j])
            info['QR_overflow_safe_norm_recomputations_V']=int(_last[b+j])
            info['QR_overflow_safe_norm_recomputations']=int(_last[j]+_last[b+j])
            info['implementation_numeric_repair']='max-scaled norm only when the ordinary FP32 sum of squares overflows; same QR algebra'
        return product,infos
    base.qr=qr;base.SweepGraph.execute=execute;als.fit=fit;_installed=True
