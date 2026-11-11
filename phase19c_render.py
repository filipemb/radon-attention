"""Exact Gaussian recurrences for the same normalized, tapered line family.

For q(v)=q0+g*v and t(v)=t0+h*v, the untapered value e satisfies
e(v+1)=e(v)*ratio(v), ratio(v+1)=ratio(v)*exp(-g*g). Three exponentials per
grid row replace one exponential per pixel. No fast-math approximation, pixel
subsampling, altered cutoff or modified primitive parameter is used.
"""
import phase19c_common
import math
import numpy as np
import torch
from numba import njit,prange


@njit(inline="always")
def setup(theta,rho,logwidth,n):
    c=math.cos(theta);s=math.sin(theta);w=math.exp(logwidth)
    dominant=abs(c)>=abs(s);half=int(math.ceil(6*w/max(abs(c),abs(s))))+1
    span=2*half+3;dense=span>=n
    if dense:span=n
    return c,s,w,dominant,half,span,dense


@njit(inline="always")
def row_state(anchor,n,span,half,dense,dominant,c,s,rho,w,decay):
    center=(n-1)/2
    if dense:
        ii=anchor;jj=0;di=0;dj=1
    else:
        den=c if dominant else s;other=s if dominant else c
        near=int(math.floor((rho-other*(anchor-center))/den+center))-half-1
        ii=anchor if dominant else near;jj=near if dominant else anchor
        di=0 if dominant else 1;dj=1 if dominant else 0
    # Clip the enumeration to causal image pixels before any exponential.
    # This changes loop bounds only: the old renderer skipped these pixels.
    if dj:
        lo=max(0,-jj);hi=min(span,ii-jj+1)
    else:
        lo=max(0,jj-ii);hi=min(span,n-ii)
    if hi<=lo:return ii,jj,di,dj,0.,0.,0.,0.,0.,0.,0.,0
    ii+=di*lo;jj+=dj*lo;count=hi-lo
    xx=jj-center;yy=ii-center
    q=(c*xx+s*yy-rho)/w;t=(-s*xx+c*yy)/n
    g=(c*dj+s*di)/w;h=(-s*dj+c*di)/n
    end=q+g*(count-1)
    if min(q,end)>=6 or max(q,end)<=-6:return ii,jj,di,dj,q,t,g,h,0.,0.,0.,0
    if abs(g)>1e-15:
        edge1=(-6-q)/g;edge2=(6-q)/g
        first=max(0,int(math.floor(min(edge1,edge2)))-1)
        last=min(count,int(math.ceil(max(edge1,edge2)))+2)
        if last<=first:return ii,jj,di,dj,q,t,g,h,0.,0.,0.,0
        ii+=di*first;jj+=dj*first;count=last-first
        xx=jj-center;yy=ii-center
        q=(c*xx+s*yy-rho)/w;t=(-s*xx+c*yy)/n
    e=math.exp(-.5*q*q-decay*t)
    ratio=math.exp(-g*q-.5*g*g-decay*h)
    ratio_step=math.exp(-g*g)
    return ii,jj,di,dj,q,t,g,h,e,ratio,ratio_step,count


@njit(parallel=True,cache=True)
def forward(theta,rho,logwidth,decay,amplitude,n):
    starts,k=theta.shape;pixels=n*(n+1)//2
    norms=np.ones((starts,k),dtype=np.float64);result=np.zeros((starts,pixels),dtype=np.float64)
    for start in prange(starts):
        for a in range(k):
            c,s,w,dominant,half,span,dense=setup(theta[start,a],rho[start,a],logwidth[start,a],n)
            squared=0.0
            for anchor in range(n):
                ii,jj,di,dj,q,t,g,h,e,ratio,step,count=row_state(anchor,n,span,half,dense,dominant,c,s,rho[start,a],w,decay[start,a])
                for v in range(count):
                    if jj>=0 and ii>=0 and ii<n and jj<=ii and abs(q)<6:
                        taper=1-q*q/36;value=e*taper*taper*taper;squared+=value*value
                    ii+=di;jj+=dj;q+=g;t+=h;e*=ratio;ratio*=step
            norm=math.sqrt(squared)
            if norm==0:continue
            norms[start,a]=norm
            factor=amplitude[start,a]/norm
            for anchor in range(n):
                ii,jj,di,dj,q,t,g,h,e,ratio,step,count=row_state(anchor,n,span,half,dense,dominant,c,s,rho[start,a],w,decay[start,a])
                for v in range(count):
                    if jj>=0 and ii>=0 and ii<n and jj<=ii and abs(q)<6:
                        taper=1-q*q/36;result[start,ii*(ii+1)//2+jj]+=factor*e*taper*taper*taper
                    ii+=di;jj+=dj;q+=g;t+=h;e*=ratio;ratio*=step
    return result,norms


@njit(parallel=True,cache=True)
def backward(theta,rho,logwidth,decay,amplitude,norms,go,n):
    starts,k=theta.shape;grads=np.zeros((5,starts,k),dtype=np.float64)
    for index in prange(starts*k):
        start=index//k;a=index%k
        c,s,w,dominant,half,span,dense=setup(theta[start,a],rho[start,a],logwidth[start,a],n)
        sums=np.zeros(9,dtype=np.float64)
        for anchor in range(n):
            ii,jj,di,dj,q,t,g,h,e,ratio,step,count=row_state(anchor,n,span,half,dense,dominant,c,s,rho[start,a],w,decay[start,a])
            for v in range(count):
                if jj>=0 and ii>=0 and ii<n and jj<=ii and abs(q)<6:
                    taper=1-q*q/36;u=e*taper*taper*taper/norms[start,a]
                    eu=go[start,ii*(ii+1)//2+jj]*u;uu=u*u
                    f=-q-6*q/max(36-q*q,1e-15)
                    dt=f*t*n/w+decay[start,a]*(rho[start,a]+w*q)/n
                    dr=-f/w;dw=-f*q;dd=-t
                    sums[0]+=eu*dt;sums[1]+=eu*dr;sums[2]+=eu*dw;sums[3]+=eu*dd
                    sums[4]+=uu*dt;sums[5]+=uu*dr;sums[6]+=uu*dw;sums[7]+=uu*dd;sums[8]+=eu
                ii+=di;jj+=dj;q+=g;t+=h;e*=ratio;ratio*=step
        for coord in range(4):grads[coord,start,a]=amplitude[start,a]*(sums[coord]-sums[8]*sums[4+coord])
        grads[4,start,a]=sums[8]
    return grads


class RecurrenceRenderLines(torch.autograd.Function):
    @staticmethod
    def forward(ctx,theta,rho,logwidth,decay,amplitude,x,y,n):
        params=tuple(p.detach().numpy().astype(np.float64) for p in (theta,rho,logwidth,decay,amplitude))
        output,norms=forward(*params,n)
        if not np.isfinite(output).all() or not np.isfinite(norms).all():raise FloatingPointError("Nonfinite recurrence rendering")
        ctx.params=params;ctx.norms=norms;ctx.n=n;ctx.dtype=theta.dtype
        return torch.from_numpy(output).to(theta.dtype)

    @staticmethod
    def backward(ctx,grad_output):
        grad=backward(*ctx.params,ctx.norms,grad_output.detach().numpy().astype(np.float64),ctx.n)
        if not np.isfinite(grad).all():raise FloatingPointError("Nonfinite recurrence gradient")
        return *(torch.from_numpy(g).to(ctx.dtype) for g in grad),None,None,None

