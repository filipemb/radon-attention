"""Locate the first nonfinite numerical operation on a preserved failed input.

Diagnostic only: no behavioral score, no optimizer setting changes, no data
replacement. All finite pre-failure states are retained for exact replay.
"""
import phase50_fp32_als as als
import phase50_fp32_graph as gg
import argparse,time
import numpy as np
import torch
import phase2_downstream as harness
from phase50_experiment import read
from sampling import sha256_file,write_json_new

def summary(x):
    f=torch.isfinite(x);values=x[f]
    return {'shape':list(x.shape),'nonfinite':int((~f).sum()),
        'maximum_absolute_finite_entry':float(values.abs().max()) if values.numel() else None,
        'finite_entry_norm_float64':float(values.double().norm()) if values.numel() else None}

def stage_update(target,f,reverse):
    pp=f.unsqueeze(-1)*f.unsqueeze(-2);gram=pp.flip(1).cumsum(1).flip(1) if reverse else pp.cumsum(1);rhs=target@f
    counter=torch.zeros((),device='cuda',dtype=torch.int32);result=gg.solve(gram,rhs,counter)
    nonfinite=(~torch.isfinite(result)).any(-1);indices=nonfinite.nonzero().cpu().tolist()
    stats={'factor_in':summary(f),'outer_products':summary(pp),'cumulative_gram':summary(gram),'rhs':summary(rhs),
        'solution':summary(result),'Cholesky_failure_count':int(counter),'failed_matrix_row_indices':indices}
    if indices:
        b,i=indices[0];g=gram[b,i];r=rhs[b,i]
        stats['first_bad_gram_bits']=g.contiguous().view(torch.int32).cpu().tolist()
        stats['first_bad_rhs_bits']=r.contiguous().view(torch.int32).cpu().tolist()
        if bool(torch.isfinite(g).all()):
            trace=torch.zeros((),device='cuda')
            for j in range(g.shape[-1]):trace=trace+g[j,j]
            lam=(1e-6*trace).clamp_min(1e-30);reg=g+torch.eye(g.shape[-1],device='cuda')*lam
            chol,info=torch.linalg.cholesky_ex(reg,check_errors=False)
            stats['regularized_gram_eigenvalues_double']=torch.linalg.eigvalsh(reg.double()).cpu().tolist()
            stats['ridge_lambda']=float(lam);stats['native_float32_Cholesky_info']=int(info)
            if int(info)==0:stats['native_float32_solution']=torch.cholesky_solve(r[:,None],chol)[:,0].cpu().tolist()
    return result,stats

@torch.inference_mode()
def run():
    source='out/phase50_declared_failed_ALS_input_Qwen05_docs4_6.json';saved=read(source);rank=saved['rank']
    a=torch.tensor(saved['input_A'],device='cuda',dtype=torch.float32);support=harness.causal_support(128,128,'cuda')
    norms=a.norm(dim=(-2,-1));safe=torch.where(norms==0,1.,norms);target=a/safe[:,None,None]
    left,s,vh=torch.linalg.svd(a,full_matrices=False);root=(s[:,:rank]/safe[:,None]).sqrt()[:,None,:]
    u,v=left[:,:,:rank]*root,vh[:,:rank,:].transpose(-1,-2)*root
    g=gg.SweepGraph(target,u,v,support);g.target.copy_(target);g.u.copy_(u);g.v.copy_(v)
    g.iteration.zero_();g.failures.zero_();g.nonfinite.zero_();g.svd.failures.zero_();history=[]
    for step in range(1,201):
        before_u=g.u.clone();before_v=g.v.clone();g.graph.replay()
        flags=torch.stack((g.failures.long(),g.nonfinite,g.svd.failures)).cpu().tolist()
        history.append({'sweep':step,'flags':flags,'U':summary(g.u),'V':summary(g.v)})
        if any(flags):
            print('FIRST FAILURE',step,flags,flush=True)
            cu,first=stage_update(target,before_v,False);detail={'update_U':first}
            if not first['solution']['nonfinite']:
                cv,second=stage_update(target.transpose(-1,-2),cu,True);detail['update_V']=second
                if not second['solution']['nonfinite']:
                    both=torch.cat((cu,cv),0);q,r=gg.qr(both);qu,qv=q.chunk(2);ru,rv=r.chunk(2);core=ru@rv.transpose(-1,-2)
                    detail['QR_input']=summary(both);detail['QR_input_column_square_sums']=summary(both.square().sum(-2))
                    detail['Q']=summary(q);detail['R']=summary(r);detail['core']=summary(core)
                    detail['QR_input_column_norms_double']=both.double().norm(dim=-2).cpu().tolist()
            result={'failed_input_sha256':sha256_file(source),'context':saved['context'],'first_failed_sweep':step,'flags':flags,
                'initial_U_normalized':u.cpu().tolist(),'initial_V_normalized':v.cpu().tolist(),
                'pre_failure_U':before_u.cpu().tolist(),'pre_failure_V':before_v.cpu().tolist(),
                'target_normalized':target.cpu().tolist(),'history':history,'stages':detail,
                'diagnostic_only_no_KL_NLL':True,'estimator_sources':saved['estimator_sources']}
            write_json_new('out/phase50_declared_first_failure_trace.json',result)
            print('TRACE SAVED',detail,flush=True)
            if (detail.get('QR_input',{}).get('nonfinite')==0 and detail.get('QR_input_column_square_sums',{}).get('nonfinite',0)>0):
                from phase50_declared_qr_repair_control import run as control_repair
                control_repair()
            return
    write_json_new('out/phase50_declared_trace_failure_not_reproduced.json',{'failed_input_sha256':sha256_file(source),'same200_sweeps_finite':True,'history':history})
    print('No failure on preserved input; original failure remains recorded',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--under-gpu-lock',action='store_true');a=ap.parse_args()
    if not a.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
    run()
