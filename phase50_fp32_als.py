"""E9 GPU float32: cumulative normal equations and balanced masked ALS.

No CPU recomputation. Causal support/probability normalization belong to the
unchanged phase2 harness, never this estimator. The protocol is immutable.
"""
import os
for _name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='4'
os.environ['TOKENIZERS_PARALLELISM']='false'
import datasets  # Required before torch in this Windows installation.
import time
import numpy as np
import torch

SWEEPS=200
RIDGE=1e-6
CHECKPOINTS=(0,1,10,25,50,100,150,180,200)
torch.set_num_threads(4)
torch.backends.cuda.matmul.allow_tf32=False
torch.backends.cudnn.allow_tf32=False


def update(target,f,reverse=False):
    outer=f.unsqueeze(-1)*f.unsqueeze(-2)
    gram=outer.flip(1).cumsum(1).flip(1) if reverse else outer.cumsum(1)
    trace=gram.diagonal(dim1=-2,dim2=-1).sum(-1)
    # Prefixes shorter than rank are necessarily singular. This uniform,
    # predeclared ridge also protects normal equations against FP32 roundoff.
    lam=(RIDGE*trace).clamp_min(1e-30)
    gram=gram+lam[...,None,None]*torch.eye(f.shape[-1],device=f.device,dtype=f.dtype)
    rhs=target@f
    chol,info=torch.linalg.cholesky_ex(gram,check_errors=False)
    out=torch.cholesky_solve(rhs.unsqueeze(-1),chol).squeeze(-1)
    return out,info


def balance(u,v):
    q,r=torch.linalg.qr(torch.cat((u,v),0),mode='reduced')
    qu,qv=q.chunk(2);ru,rv=r.chunk(2)
    left,s,vh=torch.linalg.svd(ru@rv.transpose(-1,-2),full_matrices=False)
    root=s.sqrt()[:,None,:]
    return (qu@left)*root,(qv@vh.transpose(-1,-2))*root


@torch.inference_mode()
def fit(a,rank,support,initial=None,backend='torch'):
    if backend=='graph':
        from phase50_fp32_graph import fit_graph
        return fit_graph(a,rank,support,initial)
    started=time.perf_counter();a=a.float()
    if a.ndim!=3 or a.shape[-2:]!=(128,128) or not a.is_cuda or not 1<=rank<=16:
        raise ValueError('Expected CUDA Bx128x128, rank<=16')
    if not bool(torch.isfinite(a).all()) or bool((a*~support).any()):
        raise ValueError('Nonfinite or noncausal target')
    norms=a.norm(dim=(-2,-1));safe=torch.where(norms==0,1.,norms)
    target=a/safe[:,None,None]
    if initial is None:
        left,s,vh=torch.linalg.svd(a,full_matrices=False)
        root=(s[:,:rank]/safe[:,None]).sqrt()[:,None,:]
        u,v=left[:,:,:rank]*root,vh[:,:rank,:].transpose(-1,-2)*root
    else:
        u,v=(x.float()/safe.sqrt()[:,None,None] for x in initial)
    initial_loss=(((u@v.transpose(-1,-2)-target)*support)**2).sum((-2,-1))
    losses=[];gauges=[];statuses=[]
    for _ in range(SWEEPS):
        cu,si=update(target,v)
        cv,sj=update(target.transpose(-1,-2),cu,True)
        before=(cu@cv.transpose(-1,-2))*support
        u,v=balance(cu,cv)
        product=u@v.transpose(-1,-2)
        losses.append(((product-target)*support).square().sum((-2,-1)))
        gauges.append((product*support-before).norm(dim=(-2,-1)))
        statuses.append(torch.stack((si,sj)).ne(0).sum())
    if int(torch.stack(statuses).sum()):
        raise FloatingPointError('FP32 batched Gram Cholesky failed; no solver substitution')
    return finish(u,v,target,safe,support,initial_loss,torch.stack(losses),torch.stack(gauges),started,'torch')


def finish(u,v,target,safe,support,initial_loss,losses,gauges,started,backend):
    raw=u@v.transpose(-1,-2)
    if not bool(torch.isfinite(raw).all() and torch.isfinite(losses).all() and torch.isfinite(gauges).all()):
        raise FloatingPointError('Nonfinite FP32 ALS; no replacement')
    residual=(raw-target)*support
    gradient=((2*residual@v).square().sum((-2,-1))+(2*residual.transpose(-1,-2)@u).square().sum((-2,-1))).sqrt()
    change=(losses[-21]-losses[-1]).abs()/losses[-21].clamp_min(1e-24)
    factors=torch.cat((u.abs().flatten(1),v.abs().flatten(1)),1)*safe.sqrt()[:,None]
    minimum=torch.where(factors>0,factors,torch.full_like(factors,float('inf'))).amin(1)
    pack=torch.stack((factors.amax(1),minimum,gradient,change,raw.norm(dim=(-2,-1)),gauges.amax(0)),1).cpu().tolist()
    hist=torch.cat((initial_loss[None],losses)).cpu().numpy()
    elapsed=time.perf_counter()-started;infos=[]
    for j,(maximum,minimum,grad,delta,unmasked,gauge) in enumerate(pack):
        if maximum==0 and minimum==float('inf'):minimum=None
        if minimum is not None and not np.isfinite(minimum):raise FloatingPointError('Nonfinite factor diagnostic')
        infos.append({'sweeps':SWEEPS,'dtype':'float32','GPU_solver':'cumulative_gram_'+backend,
            'ridge_relative_to_trace':RIDGE,'ridge_absolute_floor':1e-30,'CPU_recomputations':0,
            'initial_relative':float(np.sqrt(hist[0,j])),'final_relative':float(np.sqrt(hist[-1,j])),
            'history':[{'sweep':s,'relative':float(np.sqrt(hist[s,j]))} for s in CHECKPOINTS],
            'last20_relative_objective_change':delta,'gradient_normalized_target':grad,
            'converged':bool(grad<=1e-6 and (delta<=1e-7 or hist[-1,j]<=1e-12)),
            'objective_increase_sweeps':int(np.sum(np.diff(hist[:,j])>1e-9)),
            'maximum_absolute_factor':maximum,'minimum_nonzero_absolute_factor':minimum,
            'factor_dynamic_range':maximum/minimum if minimum is not None else 0.,
            'unmasked_product_norm_over_target':unmasked,'maximum_QR_observed_product_error':gauge,
            'seconds':elapsed})
    return raw*safe[:,None,None],infos
