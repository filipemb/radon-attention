"""Stable unregularized ALS: column scaling, residual refinement, direct retries.

The first implementation and its failure logs are retained. Every final case
uses this version; no per-case choice between implementations is performed.
"""
import phase19c_common
import time
import numpy as np
from scipy import linalg
from phase19c_lowrank import errors,svd_models

SWEEPS=2000
LS_RCOND=1e-12
GRAM_MIN_RATIO=1e-6
MONOTONIC_TOLERANCE=1e-9

def balance(u,v):
    # Avoid mixing columns using the unobserved upper triangle. Such rotations
    # can introduce large cancellation on the observed lower triangle.
    nu=np.array([linalg.norm(u[:,j]) for j in range(u.shape[1])])
    nv=np.array([linalg.norm(v[:,j]) for j in range(v.shape[1])])
    scale=np.ones_like(nu);active=(nu>0)&(nv>0)
    scale[active]=np.sqrt(nv[active]/nu[active])
    return u*scale,v/scale

def direct_update(a,factor,reverse=False):
    rows=[]
    for i in range(len(a)):
        sl=slice(i,None) if reverse else slice(None,i+1)
        rows.append(linalg.lstsq(factor[sl],a[i,sl],cond=LS_RCOND,
            lapack_driver="gelsd",check_finite=False)[0])
    result=np.asarray(rows)
    if not np.isfinite(result).all():raise FloatingPointError("Nonfinite direct ALS solve")
    return result

def update(a,factor,reverse=False):
    products=np.einsum("ni,nj->nij",factor,factor)
    gram=np.cumsum(products[::-1],axis=0)[::-1] if reverse else np.cumsum(products,axis=0)
    if not np.isfinite(gram).all():return direct_update(a,factor,reverse),len(a)
    eigen,rotation=np.linalg.eigh(gram)
    good=(eigen[:,0]>GRAM_MIN_RATIO*eigen[:,-1])&(eigen[:,-1]>0)
    result=np.empty_like(factor);rhs=a@factor
    if good.any():
        q=rotation[good]
        def solve(h):return np.einsum("nij,nj->ni",q,np.einsum("nji,nj->ni",q,h)/eigen[good])
        result[good]=solve(rhs[good])
    bad=np.flatnonzero(~good)
    for i in bad:
        sl=slice(i,None) if reverse else slice(None,i+1)
        result[i]=linalg.lstsq(factor[sl],a[i,sl],cond=LS_RCOND,
            lapack_driver="gelsd",check_finite=False)[0]
    # Refinement uses the original observed design, not an inaccurately
    # rounded Gram residual. This does not change the least-squares objective.
    if good.any():
        prediction=result@factor.T
        residual=a-(np.triu(prediction) if reverse else np.tril(prediction))
        result[good]+=solve((residual@factor)[good])
    if not np.isfinite(result).all():raise FloatingPointError("Nonfinite refined ALS solve")
    return result,len(bad)

def fit(a,r,svd=None,sweeps=SWEEPS):
    begin=time.perf_counter();a=np.asarray(a,dtype=float);n=len(a)
    if a.shape!=(n,n) or not np.isfinite(a).all() or np.any(np.triu(a,1)):raise ValueError("Expected finite causal matrix")
    norm=float(np.linalg.norm(a));target=a/norm
    if svd is None:svd=np.linalg.svd(a,full_matrices=False)
    left,s,right=svd;u=left[:,:r]*np.sqrt(s[:r]/norm);v=right[:r].T*np.sqrt(s[:r]/norm)
    loss=float(np.linalg.norm(np.tril(u@v.T)-target)**2);initial=float(np.sqrt(loss));losses=[loss]
    history=[{"sweep":0,"relative":initial}];fallbacks=0;retries=0;rejections=[];max_increase=0.;max_trial_increase=0.
    for iteration in range(1,sweeps+1):
        previous_u=u;previous_v=v
        candidate_u,count=update(target,previous_v);fallbacks+=count
        candidate_v,count=update(target.T,candidate_u,True);fallbacks+=count
        candidate_u,candidate_v=balance(candidate_u,candidate_v)
        candidate_loss=float(np.linalg.norm(np.tril(candidate_u@candidate_v.T)-target)**2)
        if not np.isfinite(candidate_loss):raise FloatingPointError("Nonfinite ALS objective")
        max_trial_increase=max(max_trial_increase,candidate_loss-loss)
        if candidate_loss>loss+MONOTONIC_TOLERANCE*max(1.,loss):
            retries+=1
            candidate_u=direct_update(target,previous_v)
            candidate_v=direct_update(target.T,candidate_u,True)
            candidate_u,candidate_v=balance(candidate_u,candidate_v)
            candidate_loss=float(np.linalg.norm(np.tril(candidate_u@candidate_v.T)-target)**2)
            if not np.isfinite(candidate_loss):raise FloatingPointError("Nonfinite direct-retry objective")
            if candidate_loss>loss+MONOTONIC_TOLERANCE*max(1.,loss):
                rejections.append({"sweep":iteration,"previous_loss":loss,"rejected_loss":candidate_loss})
                candidate_u=previous_u;candidate_v=previous_v;candidate_loss=loss
        max_increase=max(max_increase,candidate_loss-loss)
        u,v,loss=candidate_u,candidate_v,candidate_loss;losses.append(loss)
        if iteration%10==0 or iteration==sweeps:history.append({"sweep":iteration,"relative":float(np.sqrt(loss))})
    residual=np.tril(u@v.T)-target
    grad=float(np.sqrt(np.linalg.norm(2*residual@v)**2+np.linalg.norm(2*residual.T@u)**2))
    change=abs(losses[-21]-losses[-1])/max(losses[-21],1e-24)
    u=u*np.sqrt(norm);v=v*np.sqrt(norm);product=u@v.T
    prediction=np.tril(product);nonzero=np.concatenate([np.abs(u[u!=0]),np.abs(v[v!=0])])
    unmasked_norm=float(np.linalg.norm(product)/norm)
    output={**errors(a,prediction),"U":u.tolist(),"V":v.tolist(),"components":r,"stored_numbers":2*n*r,
        "diagnostics":{"implementation":"phase19c_als_stable","sweeps":sweeps,"fixed_sweeps_no_early_stop":True,
            "initialization":"ordinary truncated SVD, sqrt singular values split across U,V","objective":"||tril(A-U V^T)||F^2",
            "decoder":"tril(U V^T)","regularization":0.,"nonnegativity_constraint":False,"LS_rcond":LS_RCOND,
            "gauge":"column norm balancing only, no cross-column rotations; represented product preserved",
            "Gram_min_eigenvalue_ratio_for_fast_solve":GRAM_MIN_RATIO,"observed_residual_refinement":True,
            "direct_LS_block_fallbacks":fallbacks,"direct_sweep_retries":retries,"numerically_rejected_sweeps":rejections,
            "rejection_policy":"If a direct retry still increases the objective beyond the unchanged1e-9 tolerance, retain the previous finite state; record every rejection and continue fixed sweeps",
            "maximum_accepted_objective_increase":max_increase,"maximum_proposed_objective_increase":max_trial_increase,
            "history_every10":history,"initial_relative":initial,"last20_relative_objective_change":change,
            "gradient_L2_normalized_target":grad,"converged":bool(grad<=1e-6 and (change<=1e-7 or np.sqrt(loss)<=1e-6) and (not rejections or np.sqrt(loss)<=1e-6)),
            "convergence_definition":"gradient<=1e-6 AND (last20 relative objective change<=1e-7 OR relative error<=1e-6); rejected numerical sweeps mark nonconvergence unless error<=1e-6",
            "maximum_absolute_factor":float(max(np.abs(u).max(),np.abs(v).max())),
            "minimum_nonzero_absolute_factor":float(nonzero.min()) if len(nonzero) else None,
            "unmasked_product_norm_to_target_norm":unmasked_norm if np.isfinite(unmasked_norm) else None,
            "unmasked_norm_undefined_reason":None if np.isfinite(unmasked_norm) else "Unobserved completion norm overflows; causal score remains finite",
            "seconds":time.perf_counter()-begin}}
    return output
