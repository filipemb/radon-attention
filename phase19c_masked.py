"""Unregularized causal masked low rank; SVD start and exact ALS block solves."""
import phase19c_common
import time
import numpy as np
from scipy import linalg

SWEEPS=500
LS_RCOND=1e-12
GRAM_MIN_RATIO=1e-9

def balance(u,v):
    qu,ru=np.linalg.qr(u,mode="reduced");qv,rv=np.linalg.qr(v,mode="reduced")
    left,s,right=np.linalg.svd(ru@rv.T,full_matrices=False)
    root=np.sqrt(s)
    return (qu@left)*root,(qv@right.T)*root

def update(a,factor,reverse=False,previous=None):
    products=np.einsum("ni,nj->nij",factor,factor)
    gram=np.cumsum(products[::-1],axis=0)[::-1] if reverse else np.cumsum(products,axis=0)
    rhs=a@factor
    eigen,rotation=np.linalg.eigh(gram)
    good=(eigen[:,0]>GRAM_MIN_RATIO*eigen[:,-1])&(eigen[:,-1]>0)
    result=np.empty_like(factor)
    if good.any():
        q=rotation[good];h=rhs[good]
        result[good]=np.einsum("nij,nj->ni",q,np.einsum("nji,nj->ni",q,h)/eigen[good])
    bad=np.flatnonzero(~good)
    for i in bad:
        sl=slice(i,None) if reverse else slice(None,i+1)
        prior=np.zeros(factor.shape[1]) if previous is None else previous[i]
        result[i]=prior+linalg.lstsq(factor[sl],a[i,sl]-factor[sl]@prior,cond=LS_RCOND,
            lapack_driver="gelsd",check_finite=False)[0]
    if not np.isfinite(result).all():raise FloatingPointError("Nonfinite ALS block solve")
    return result,len(bad)

def errors(a,hat):
    norm=float(np.linalg.norm(a));absolute=float(np.linalg.norm(a-hat))
    if norm<=0 or not np.isfinite([norm,absolute]).all():raise ValueError("Invalid reconstruction norm")
    return {"relative":absolute/norm,"absolute":absolute,"norm_frobenius":norm}

def svd_models(a,ranks):
    u,s,vt=np.linalg.svd(a,full_matrices=False);result={}
    for r in ranks:
        left=u[:,:r];values=s[:r];right=vt[:r].T
        result[r]={**errors(a,(left*values)@right.T),"U":left.tolist(),"S":values.tolist(),"V":right.tolist(),
            "components":r,"stored_numbers":r*(2*len(a)+1)}
    return result,(u,s,vt)

def fit(a,r,svd=None,sweeps=SWEEPS):
    begin=time.perf_counter();a=np.asarray(a,dtype=float)
    if a.ndim!=2 or a.shape[0]!=a.shape[1] or np.any(np.triu(a,1)) or not np.isfinite(a).all():raise ValueError("Expected finite causal matrix")
    n=len(a);norm=float(np.linalg.norm(a));target=a/norm
    if svd is None:svd=np.linalg.svd(a,full_matrices=False)
    u0,s,v0=svd;u=u0[:,:r]*np.sqrt(s[:r]/norm);v=v0[:r].T*np.sqrt(s[:r]/norm)
    initial=float(np.linalg.norm(np.tril(u@v.T)-target));history=[{"sweep":0,"relative":initial}]
    losses=[initial*initial];qr_fallbacks=0;max_increase=0.
    for iteration in range(1,sweeps+1):
        u,count=update(target,v,previous=u);qr_fallbacks+=count
        v,count=update(target.T,u,reverse=True,previous=v);qr_fallbacks+=count
        u,v=balance(u,v)
        loss=float(np.linalg.norm(np.tril(u@v.T)-target)**2)
        increase=loss-losses[-1];max_increase=max(max_increase,increase)
        if increase>1e-9*max(1.,losses[-1]):raise FloatingPointError("ALS objective increased beyond numerical tolerance")
        losses.append(loss)
        if iteration%10==0 or iteration==sweeps:history.append({"sweep":iteration,"relative":float(np.sqrt(loss))})
    residual=np.tril(u@v.T)-target
    grad=float(np.sqrt(np.linalg.norm(2*residual@v)**2+np.linalg.norm(2*residual.T@u)**2))
    relative_change=abs(losses[-21]-losses[-1])/max(losses[-21],1e-24)
    u*=np.sqrt(norm);v*=np.sqrt(norm)
    return {**errors(a,np.tril(u@v.T)),"U":u.tolist(),"V":v.tolist(),"components":r,"stored_numbers":2*n*r,
        "diagnostics":{"sweeps":sweeps,"fixed_sweeps_no_early_stop":True,"initialization":"ordinary truncated SVD, balanced sqrt singular values",
            "objective":"||tril(A-U V^T)||_F^2; decoder tril(U V^T)","nonnegativity_constraint":False,
            "regularization":0.,"LS_rcond":LS_RCOND,"Gram_min_eigenvalue_ratio_for_fast_solve":GRAM_MIN_RATIO,
            "fallback":"direct design-matrix SVD least squares, minimum change from previous block when underidentified; no ridge",
            "gauge":"balanced QR and small SVD every sweep, preserving U V^T",
            "direct_LS_block_fallbacks":qr_fallbacks,"history_every10":history,"initial_relative":initial,
            "last20_relative_objective_change":relative_change,"gradient_L2_normalized_target":grad,
            "converged":bool(relative_change<=1e-7 and grad<=1e-6),
            "convergence_definition":"last20 relative objective change <=1e-7 AND gradient L2 <=1e-6; no early stop",
            "maximum_objective_increase":max_increase,"seconds":time.perf_counter()-begin}}
