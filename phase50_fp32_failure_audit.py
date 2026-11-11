"""Exploratory mechanism check, never an estimator/acceptance replacement.

On each model's worst validation case, run the same trace-ridge block update
in CPU float64 from the same SVD start. This separates a changed update rule
from an implementation error; it does not modify the frozen acceptance test.
"""
import phase50_als as original
import time,json,argparse
from pathlib import Path
import numpy as np
from phase50_experiment import read,jsonl,Dictionary,metrics,normalize_cpu
from sampling import MODELS,slug,load_sample,sha256_file,write_json_new

def run(model):
    path=Path(f'out/phase50_fp32_failure_audit_{slug(model)}.json')
    if path.exists():return read(path)
    val=read(f'out/phase50_fp32_validation_{slug(model)}.json');w=val['worst'];idx,k,arm=w['archive_index'],w['K'],w['arm']
    refmeta=read(f'out/phase50_GPU_CPU_reference_{slug(model)}.json')
    rows=jsonl(refmeta['pairs_path']);row=next(r for r in rows if (r['archive_index'],r['K'],r['arm'])==(idx,k,arm))
    array,manifest=load_sample(model,128);a=array[idx].astype(np.float64);s=Dictionary(128).project(a)[0] if arm=='named_plus_masked' else 0
    target=a-s;norm=np.linalg.norm(target);target=target/norm
    u=np.array(row['initial_U'])/np.sqrt(norm);v=np.array(row['initial_V'])/np.sqrt(norm)
    rank=u.shape[-1];eye=np.eye(rank);history=[];started=time.perf_counter()
    def update(aa,f,reverse=False):
        pp=f[:,:,None]*f[:,None,:]
        gram=np.cumsum(pp[::-1],axis=0)[::-1] if reverse else np.cumsum(pp,axis=0)
        lam=np.maximum(1e-6*np.trace(gram,axis1=-2,axis2=-1),1e-30)
        rhs=aa@f
        return np.linalg.solve(gram+lam[:,None,None]*eye,rhs[...,None])[...,0]
    for sweep in range(1,201):
        u=update(target,v);v=update(target.T,u,True);u,v=original.balance_cpu(u,v)
        if sweep in original.CHECKPOINTS:history.append({'sweep':sweep,'relative':float(np.linalg.norm(np.tril(u@v.T)-target))})
    product=(u@v.T)*norm+s;mm=metrics(product,a,normalize_cpu(a,a)[0])
    original_diff=abs(mm['raw_causal_frobenius']-w['CPU']['raw_causal_frobenius'])
    fp32_diff=abs(mm['raw_causal_frobenius']-w['GPU']['raw_causal_frobenius'])
    result={'model':model,'archive_index':idx,'K':k,'arm':arm,'layer':w['layer'],'head':w['head'],
        'exploratory_after_validation_not_preregistered':True,'does_not_change_acceptance_or_forward_estimator':True,
        'CPU_double_original_unregularized':w['CPU'],'GPU_FP32_ridge':w['GPU'],
        'CPU_double_same_trace_ridge_update':mm,'CPU_double_ridge_history':history,
        'absolute_raw_error_difference_double_ridge_vs_original_double':original_diff,
        'absolute_raw_error_difference_float32_ridge_vs_double_ridge':fp32_diff,
        'CPU_original_maximum_factor':w['CPU_ALS']['maximum_absolute_factor'],
        'CPU_original_rejected_sweeps':len(w['CPU_ALS']['rejected_sweeps']),
        'CPU_ridge_maximum_factor':float(max(np.abs(u).max(),np.abs(v).max())*np.sqrt(norm)),
        'elapsed_seconds':time.perf_counter()-started,
        'interpretation':'Compares the prescribed uniform trace-ridge closed-form200-sweep update at two precisions. Original reference additionally has direct LS and a monotonic retry/rejection policy; these are not equivalent optimization trajectories. This diagnostic does not prove a unique cause or global convergence.'}
    write_json_new(path,result);print(model,'doubleRidge-original',original_diff,'fp32Ridge-doubleRidge',fp32_diff,flush=True);return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',choices=MODELS,required=True);a=p.parse_args();run(a.model)
