"""CPU reference/alternate renderer for the same five-parameter line family.

Float64 accumulation avoids norm-square underflow without an extra pixel pass.
Torch parameters and losses remain float32. No GPU or attention extractor is
used. Four Numba threads render independent starts / atom gradients.
"""
import os
from pathlib import Path
os.environ["NUMBA_NUM_THREADS"]="4"
os.environ["NUMBA_CACHE_DIR"]=str(Path("out/phase19_numba_cache").resolve())
import math
import numpy as np
import torch
from numba import njit,prange,set_num_threads
set_num_threads(4)
STOP_PATH=None


class RequestedGPUPreemption(RuntimeError):
    """An explicit GPU handoff request, rather than an optimization failure."""


def request_path(path):
    global STOP_PATH
    STOP_PATH=Path(path) if path else None


@njit(inline="always")
def setup(theta,rho,logwidth,n):
    c=math.cos(theta);s=math.sin(theta);w=math.exp(logwidth)
    dominant=abs(c)>=abs(s)
    half=int(math.ceil(6*w/max(abs(c),abs(s))))+1
    span=2*half+3
    dense=span>=n
    if dense:span=n
    return c,s,w,dominant,half,span,dense


@njit(inline="always")
def point(z,n,span,half,dense,dominant,c,s,rho,w):
    anchor=z//span;v=z%span;center=(n-1)/2
    if dense:
        ii=anchor;jj=v
    else:
        den=c if dominant else s;other=s if dominant else c
        near=int(math.floor((rho-other*(anchor-center))/den+center))+v-half-1
        ii=anchor if dominant else near;jj=near if dominant else anchor
    if jj<0 or ii<0 or ii>=n or jj>ii:return -1,0.0,0.0
    xx=jj-center;yy=ii-center
    q=(c*xx+s*yy-rho)/w
    if abs(q)>=6:return -1,0.0,0.0
    t=(-s*xx+c*yy)/n
    return ii*(ii+1)//2+jj,q,t


@njit(inline="always")
def raw(q,t,decay):
    taper=max(1-q*q/36,0.0)
    return math.exp(-0.5*q*q-decay*t)*taper*taper*taper


@njit(parallel=True,cache=True)
def forward(theta,rho,logwidth,decay,amplitude,n):
    starts,k=theta.shape;pixels=n*(n+1)//2
    norms=np.ones((starts,k),dtype=np.float64)
    result=np.zeros((starts,pixels),dtype=np.float64)
    for start in prange(starts):
        for a in range(k):
            c,s,w,dominant,half,span,dense=setup(theta[start,a],rho[start,a],logwidth[start,a],n)
            squared=0.0
            for z in range(n*span):
                pix,q,t=point(z,n,span,half,dense,dominant,c,s,rho[start,a],w)
                if pix>=0:
                    value=raw(q,t,decay[start,a]);squared+=value*value
            norm=math.sqrt(squared)
            if norm==0:
                # Empty footprint, an exactly zero primitive.
                continue
            norms[start,a]=norm
            for z in range(n*span):
                pix,q,t=point(z,n,span,half,dense,dominant,c,s,rho[start,a],w)
                if pix>=0:result[start,pix]+=amplitude[start,a]*raw(q,t,decay[start,a])/norm
    return result,norms


@njit(parallel=True,cache=True)
def backward(theta,rho,logwidth,decay,amplitude,norms,go,n):
    starts,k=theta.shape
    grads=np.zeros((5,starts,k),dtype=np.float64)
    for index in prange(starts*k):
        start=index//k;a=index%k
        c,s,w,dominant,half,span,dense=setup(theta[start,a],rho[start,a],logwidth[start,a],n)
        sums=np.zeros(9,dtype=np.float64)
        for z in range(n*span):
            pix,q,t=point(z,n,span,half,dense,dominant,c,s,rho[start,a],w)
            if pix>=0:
                u=raw(q,t,decay[start,a])/norms[start,a]
                eu=go[start,pix]*u;uu=u*u
                f=-q-6*q/max(36-q*q,1e-15)
                dt=f*t*n/w+decay[start,a]*(rho[start,a]+w*q)/n
                dr=-f/w;dw=-f*q;dd=-t
                sums[0]+=eu*dt;sums[1]+=eu*dr;sums[2]+=eu*dw;sums[3]+=eu*dd
                sums[4]+=uu*dt;sums[5]+=uu*dr;sums[6]+=uu*dw;sums[7]+=uu*dd;sums[8]+=eu
        for coord in range(4):grads[coord,start,a]=amplitude[start,a]*(sums[coord]-sums[8]*sums[4+coord])
        grads[4,start,a]=sums[8]
    return grads


class NumbaRenderLines(torch.autograd.Function):
    @staticmethod
    def forward(ctx,theta,rho,logwidth,decay,amplitude,x,y,n):
        if STOP_PATH is not None and STOP_PATH.exists():
            raise RequestedGPUPreemption(str(STOP_PATH))
        params=tuple(p.detach().numpy().astype(np.float64) for p in (theta,rho,logwidth,decay,amplitude))
        output,norms=forward(*params,n)
        if not np.isfinite(output).all():raise FloatingPointError("Nonfinite Numba forward")
        ctx.params=params;ctx.norms=norms;ctx.n=n
        return torch.from_numpy(output.astype(np.float32))

    @staticmethod
    def backward(ctx,grad_output):
        gradients=backward(*ctx.params,ctx.norms,grad_output.detach().numpy().astype(np.float64),ctx.n)
        if not np.isfinite(gradients).all():raise FloatingPointError("Nonfinite Numba backward")
        return *(torch.from_numpy(g.astype(np.float32)) for g in gradients),None,None,None


def validate():
    from richlines_parametric import DenseRenderLines,torch_grid
    torch.manual_seed(19027);torch.set_num_threads(4)
    n=31;x,y=torch_grid(n,"cpu")
    params=[torch.nn.Parameter(p.contiguous()) for p in [torch.rand(4,7)*np.pi,
        (torch.rand(4,7)-0.5)*n,torch.rand(4,7)*2-0.5,torch.rand(4,7)*8-4,torch.rand(4,7)]]
    dense=DenseRenderLines.apply(*params,x,y,n);weights=torch.randn_like(dense)
    (dense*weights).sum().backward();reference=[p.grad.clone() for p in params]
    for p in params:p.grad=None
    actual=NumbaRenderLines.apply(*params,x,y,n);(actual*weights).sum().backward()
    value=float((dense-actual).abs().max())
    errors=[float(((p.grad-r).abs()/(1+r.abs())).max()) for p,r in zip(params,reference)]
    if value>2e-5 or max(errors)>2e-4:raise AssertionError(f"CPU renderer differs: {value}, {errors}")
    return {"forward_max_absolute":value,"gradient_max_scaled_absolute":errors,"passed":True,
            "parameters":"float32","renderer_accumulation":"float64","numba_threads":4}
