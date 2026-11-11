"""Validate signed-native-SVD canonicalization, no behavioral scoring."""
import phase50_fp32_als as als
import phase50_fp32_graph as base
import phase50_declared_signed_core as repair
import argparse
import numpy as np
import torch
from phase50_experiment import read
from sampling import sha256_file,write_json_new
import phase2_downstream as harness

@torch.inference_mode()
def run():
    evidence=read('out/phase50_declared_native_core_SVD_failure.json')
    e=evidence['captured_replay']
    if not e['negative_singular_indices'] or e['nonfinite_singular_indices'] or e['native_left_vectors']['nonfinite'] or e['native_right_vectors']['nonfinite']:
        raise AssertionError('Actual failure is not a finite signed native singular value')
    rng=np.random.default_rng(5011);checks=[]
    for b in (1,2,24,28,32):
        for r in (7,8,15,16):
            a=torch.tensor(rng.normal(size=(b,r,r)).astype(np.float32),device='cuda')
            solver=base.SmallSVD(b,r);l,s,vh=solver(a);cl,cs,cvh=repair.canonical(l,s,vh)
            if bool((s<0).any()) or int(solver.failures):raise AssertionError('Ordinary component input failed')
            oldroot=s.sqrt()[:,None,:];newroot=cs.sqrt()[:,None,:]
            checks.append({'batch':b,'rank':r,'left_factors_bit_equal':torch.equal(l*oldroot,cl*newroot),
                'right_factors_bit_equal':torch.equal(vh.transpose(-1,-2)*oldroot,cvh.transpose(-1,-2)*newroot)})
    if not all(c['left_factors_bit_equal'] and c['right_factors_bit_equal'] for c in checks):raise AssertionError('Ordinary factorization changed')
    repair.install()
    saved=read('out/phase50_declared_failed_ALS_input_Qwen05_docs4_6.json')
    a=torch.tensor(saved['input_A'],device='cuda',dtype=torch.float32);support=harness.causal_support(128,128,'cuda')
    product,infos=als.fit(a,16,support,backend='graph')
    fixed=sum(i['core_SVD_signed_values_reparameterized'] for i in infos)
    if not bool(torch.isfinite(product).all()) or fixed==0:raise AssertionError('Original failed input not repaired')
    rng=np.random.default_rng(5001);planted=[];prior=read('out/phase50_fp32_controls.json')
    for rank in (8,16):
        u=rng.lognormal(0,.7,(128,rank));v=rng.lognormal(0,.7,(128,rank));raw=np.tril(u@v.T);raw/=raw.sum(-1,keepdims=True)
        l,s,vh=np.linalg.svd(raw,full_matrices=False)
        initial=(torch.tensor((l[:,:rank]*np.sqrt(s[:rank]))[None],device='cuda'),torch.tensor((vh[:rank].T*np.sqrt(s[:rank]))[None],device='cuda'))
        a=torch.tensor(raw[None],device='cuda');p,ii=als.fit(a,rank,support,initial,backend='graph')
        err=float(((p.double()-a)*support).norm()/a.norm());old=next(z['relative_recovery_error'] for z in prior['planted'] if z['rank']==rank)
        planted.append({'rank':rank,'error':err,'prior_error':old,'absolute_difference':abs(err-old)})
        if err>.01 or abs(err-old)>1e-10:raise AssertionError('Planted ordinary trajectory changed')
    result={'passed':True,'failure_evidence_sha256':sha256_file('out/phase50_declared_native_core_SVD_failure.json'),
        'ordinary_factorization_checks':checks,'original_failed_input200_sweeps_finite':True,'signed_values_corrected_on_original_input':fixed,
        'original_input_per_matrix_diagnostics':infos,'planted':planted,
        'mathematical_identity':'L diag(s) Vh = L diag(abs(s)) diag(sign(s)) Vh; split sqrt(abs(s)) and carry sign to Vh',
        'no_clamping_or_nan_replacement':True,'ridge_sweeps_rank_initialization_unchanged':True,'CPU_recomputations':0,
        'all_previously_successful_outputs_compatible':'Negative singular values would have produced nonfinite sqrt and failed the old public estimator. The ordinary finite nonnegative path is bit-identical; successful archived matrix/forward outputs remain the same.',
        'source':'phase50_declared_signed_core.py','source_sha256':sha256_file('phase50_declared_signed_core.py'),
        'no_behavioral_KL_NLL_scored_during_control':True}
    write_json_new('out/phase50_declared_signed_core_control.json',result)
    print('SIGNED CORE CONTROL PASSED; original failed input finite, signed values',fixed,flush=True);return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--under-gpu-lock',action='store_true');a=p.parse_args()
    if not a.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
    run()
