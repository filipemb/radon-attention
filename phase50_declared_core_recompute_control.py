"""Control the actual invalid native SVD value, no behavioral scoring."""
import phase50_fp32_als as als
import phase50_fp32_graph as base
import phase50_declared_core_value_recompute as correction
import argparse
import numpy as np
import torch
from phase50_experiment import read
from sampling import sha256_file,write_json_new
import phase2_downstream as harness

@torch.inference_mode()
def run():
    source='out/phase50_declared_native_core_SVD_failure.json';ev=read(source)['captured_replay']
    if not ev['nonfinite_singular_indices'] or ev['native_left_vectors']['nonfinite'] or ev['native_right_vectors']['nonfinite']:
        raise AssertionError('Actual failure does not match a bad singular value with finite vectors')
    def decode(bits):return torch.tensor(bits,device='cuda',dtype=torch.int32).view(torch.float32)
    core=decode(ev['core_bits']);left=decode(ev['left_vector_bits']);vh=decode(ev['right_vector_bits']);s=decode(ev['singular_values_bits'])
    ll,ss,rr,bad=correction.corrected_values(core,left,s,vh)
    reconstructed=(ll*ss[:,None,:])@rr
    rel=(reconstructed.double()-core.double()).norm(dim=(-2,-1))/core.double().norm(dim=(-2,-1))
    if not bool(torch.isfinite(reconstructed).all()) or float(rel.max())>2e-5:raise AssertionError('Actual finite core not reconstructed by recomputed singular value')
    rng=np.random.default_rng(5012);checks=[]
    for b in (1,2,24,28,32):
        for r in (7,8,15,16):
            a=torch.tensor(rng.normal(size=(b,r,r)).astype(np.float32),device='cuda')
            solver=base.SmallSVD(b,r);l,sv,v=solver(a);cl,cs,cv,badnormal=correction.corrected_values(a,l,sv,v)
            if bool(badnormal.any()) or int(solver.failures):raise AssertionError('Normal component control invalid')
            oldroot=sv.sqrt()[:,None,:];newroot=cs.sqrt()[:,None,:]
            checks.append({'batch':b,'rank':r,'left_factors_bit_equal':torch.equal(l*oldroot,cl*newroot),
                'right_factors_bit_equal':torch.equal(v.transpose(-1,-2)*oldroot,cv.transpose(-1,-2)*newroot)})
    if not all(c['left_factors_bit_equal'] and c['right_factors_bit_equal'] for c in checks):raise AssertionError('Ordinary finite path changed')
    correction.install();failed=read('out/phase50_declared_failed_ALS_input_Qwen05_docs4_6.json')
    a=torch.tensor(failed['input_A'],device='cuda',dtype=torch.float32);support=harness.causal_support(128,128,'cuda')
    product,infos=als.fit(a,16,support,backend='graph');n=sum(x['invalid_native_core_singular_values_recomputed'] for x in infos)
    if not bool(torch.isfinite(product).all()) or n==0:raise AssertionError('Failed input200-sweep procedure not corrected')
    rng=np.random.default_rng(5001);planted=[];prior=read('out/phase50_fp32_controls.json')
    for rank in (8,16):
        u=rng.lognormal(0,.7,(128,rank));v=rng.lognormal(0,.7,(128,rank));raw=np.tril(u@v.T);raw/=raw.sum(-1,keepdims=True)
        l,sval,vh0=np.linalg.svd(raw,full_matrices=False)
        init=(torch.tensor((l[:,:rank]*np.sqrt(sval[:rank]))[None],device='cuda'),
              torch.tensor((vh0[:rank].T*np.sqrt(sval[:rank]))[None],device='cuda'))
        a=torch.tensor(raw[None],device='cuda');p,ii=als.fit(a,rank,support,init,backend='graph')
        error=float(((p.double()-a)*support).norm()/a.norm());old=next(z['relative_recovery_error'] for z in prior['planted'] if z['rank']==rank)
        if error>.01 or abs(error-old)>1e-10:raise AssertionError('Planted trajectory changed')
        planted.append({'rank':rank,'error':error,'prior_error':old,'difference':abs(error-old)})
    result={'passed':True,'actual_failure_evidence_sha256':sha256_file(source),'ordinary_path_bit_equal_controls':checks,
        'actual_core_reconstruction_max_relative_error':float(rel.max()),'actual_core_recomputed_values':ss[bad].cpu().tolist(),
        'original_failed_input200_sweeps_finite':True,'original_input_invalid_singular_values_recomputed':n,
        'original_input_per_matrix_diagnostics':infos,'planted':planted,'same_method_parameters':True,
        'dtype':'float32','ridge':1e-6,'sweeps':200,'initialization':'truncated SVD','CPU_recomputations':0,
        'correction':'Invalid native s_i recomputed as u_i.T @ same finite core @ v_i; all ordinary native values retained. No clamping or zero imputation.',
        'prior_successful_results_compatibility':'An invalid native singular value made the original estimator nonfinite and fail. All successful old matrix/forward fits used the unchanged ordinary nonnegative finite path; component tests confirm bit equality.',
        'source':'phase50_declared_core_value_recompute.py','source_sha256':sha256_file('phase50_declared_core_value_recompute.py'),
        'no_behavioral_KL_NLL_scored':True}
    write_json_new('out/phase50_declared_core_recompute_control.json',result)
    print('CORE VALUE RECOMPUTATION CONTROL PASSED; corrected values',result['actual_core_recomputed_values'],'events',n,flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--under-gpu-lock',action='store_true');a=p.parse_args()
    if not a.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
    run()
