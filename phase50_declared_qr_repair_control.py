"""Check an arithmetic overflow repair without changing the declared method."""
import phase50_fp32_als as als
import phase50_fp32_graph as base
import phase50_declared_safe_qr as safe
import argparse
import numpy as np
import torch
from phase50_experiment import read
from sampling import sha256_file,write_json_new
import phase2_downstream as harness

@torch.inference_mode()
def run():
    trace=read('out/phase50_declared_first_failure_trace.json');st=trace['stages']
    evidence=(not st['update_U']['solution']['nonfinite'] and not st['update_V']['solution']['nonfinite']
        and st['QR_input']['nonfinite']==0 and st['QR_input_column_square_sums']['nonfinite']>0)
    if not evidence:raise AssertionError('The actual failure is not overflow of the naive finite-vector QR squared norm')
    rng=np.random.default_rng(5010);checks=[]
    for b in (1,2,24,28,32):
        for r in (7,8,15,16):
            a=torch.tensor(rng.normal(size=(b,128,r)).astype(np.float32),device='cuda')
            oldq,oldr=base.qr(a);newq,newr=safe.qr(a)
            checks.append({'batch':b,'rank':r,'ordinary_path_Q_bit_equal':torch.equal(oldq,newq),'ordinary_path_R_bit_equal':torch.equal(oldr,newr)})
    a=torch.tensor(rng.normal(size=(2,128,16)).astype(np.float32),device='cuda')*1e20
    q,r=safe.qr(a);rel=float((q.double()@r.double()-a.double()).norm()/a.double().norm())
    if not bool(torch.isfinite(q).all() and torch.isfinite(r).all()) or rel>2e-5:raise AssertionError('Scaled QR norm control failed')
    if not all(c['ordinary_path_Q_bit_equal'] and c['ordinary_path_R_bit_equal'] for c in checks):
        raise AssertionError('Implementation repair changed an ordinary finite QR path')
    safe.install()
    source=read('out/phase50_declared_failed_ALS_input_Qwen05_docs4_6.json')
    a=torch.tensor(source['input_A'],device='cuda',dtype=torch.float32);support=harness.causal_support(128,128,'cuda')
    product,infos=als.fit(a,16,support,backend='graph')
    if not bool(torch.isfinite(product).all()):raise AssertionError('Repaired actual input is not finite')
    repairs=sum(x['QR_overflow_safe_norm_recomputations'] for x in infos)
    if repairs==0:raise AssertionError('Repair did not activate on the original failing input')
    # The same planted test and exact same stored initialization recipe.
    rng=np.random.default_rng(5001);planted=[];prior=read('out/phase50_fp32_controls.json')
    for rank in (8,16):
        u=rng.lognormal(0,.7,(128,rank));v=rng.lognormal(0,.7,(128,rank));raw=np.tril(u@v.T);raw/=raw.sum(-1,keepdims=True)
        left,s,vh=np.linalg.svd(raw,full_matrices=False)
        initial=(torch.tensor((left[:,:rank]*np.sqrt(s[:rank]))[None],device='cuda'),
                 torch.tensor((vh[:rank].T*np.sqrt(s[:rank]))[None],device='cuda'))
        a=torch.tensor(raw[None],device='cuda');p,ii=als.fit(a,rank,support,initial,backend='graph')
        err=float(((p.double()-a)*support).norm()/a.norm());old=next(c['relative_recovery_error'] for c in prior['planted'] if c['rank']==rank)
        delta=abs(err-old);planted.append({'rank':rank,'error':err,'prior_error':old,'error_difference':delta,
            'safe_norm_recomputations':sum(x['QR_overflow_safe_norm_recomputations'] for x in ii)})
        if err>.01 or delta>1e-10:raise AssertionError('The repair changed the planted ordinary trajectory')
    result={'passed':True,'actual_failure_cause_verified':True,'first_failed_sweep':trace['first_failed_sweep'],
        'ordinary_finite_QR_checks':checks,'large_finite_vector_QR_relative_product_error':rel,
        'original_failed_input_all200_sweeps_now_finite':True,'original_failed_input_QR_norm_recomputations':repairs,
        'original_failed_input_per_matrix_ALS_diagnostics':infos,'planted':planted,
        'method_parameters_unchanged':{'dtype':'float32','ridge':1e-6,'sweeps':200,'initialization':'truncated SVD'},
        'repair_only':'finite-vector sum-of-squares overflow; recompute that norm with max scaling, still float32; no NaN/Inf target or product replaced',
        'finite_old_outputs_compatibility':'Old completed fits had finite products/losses/gauge errors throughout200 sweeps; a QR squared-norm overflow would have made them fail. The ordinary finite QR path is bit-identical, so archived successful matrix/forward results are unaffected.',
        'repair_source':'phase50_declared_safe_qr.py','repair_source_sha256':sha256_file('phase50_declared_safe_qr.py'),
        'base_estimator_sources':source['estimator_sources'],'diagnostic_only_no_behavioral_KL_NLL':True}
    write_json_new('out/phase50_declared_qr_overflow_repair_control.json',result)
    print('QR OVERFLOW REPAIR CONTROL PASSED; failed input finite; repairs',repairs,flush=True)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--under-gpu-lock',action='store_true');a=ap.parse_args()
    if not a.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
    run()
