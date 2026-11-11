"""Record the controlled native-SVD implementation fix before resuming Qwen05."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    target=Path('out/phase50_declared_implementation_fix.json')
    if target.exists():return read(target)
    control='out/phase50_declared_core_recompute_control.json';c=read(control)
    if not c['passed'] or not c['same_method_parameters'] or not c['original_failed_input200_sweeps_finite']:
        raise AssertionError('The actual numerical failure has not been controlled')
    source=c['source']
    if sha(source)!=c['source_sha256']:raise AssertionError('Controlled correction source changed')
    evidence='out/phase50_declared_native_core_SVD_failure.json';e=read(evidence)['captured_replay']
    if e['first_failed_sweep']!=71 or e['nonfinite_singular_indices']!=[[27,0]]:
        raise AssertionError('Unexpected operational failure evidence')
    result={'UTC':datetime.now(timezone.utc).isoformat(),
        'role':'Numerical implementation correction of QR+SVD rebalance, not a new optimization estimator or tuning of its parameters',
        'authority':'Necessary reversible numerical bug fix within the user-authorized forward run',
        'original_failure':{'model':'Qwen/Qwen2.5-0.5B','arm':'masked_K_diag_exact','K':16,
            'documents':[4,5],'layer_zero_based':11,'head_zero_based':13,'batch_matrix_index':27,
            'first_failed_sweep':71,'native_SVD_info':0,
            'cause':'cuSOLVER SgesvdjBatched returned an infinite singular value for a finite core with Frobenius norm about 1; finite singular vectors reconstruct that core when the invalid value is recomputed',
            'exception_preserved':True,'invalid_KL_NLL_written':False,
            'failed_attempt_log':'out/phase50_declared_Qwen__Qwen2.5-0.5B_000_016_execution.log'},
        'correction':{'formula':'For invalid native s_i only: s_i = u_i^T C v_i, evaluated on the original finite core C and returned finite singular vectors, all in GPU float32',
            'finite_nonnegative_native_values':'retained unchanged','negative_recomputed_value':'canonicalize sign into the corresponding right singular vector',
            'no_NaN_or_Infinity_imputation_to_zero':True,'no_CPU_ALS_fallback':True,
            'no_additional_ALS_sweeps':True,'ridge_relative_to_trace':1e-6,'sweeps':200,
            'initialization':'unchanged truncated SVD','rank_and_storage':'unchanged',
            'invalid_native_values_and_fits_counted':True},
        'control':{'path':control,'sha256':sha(control),
            'actual_core_max_relative_reconstruction_error':c['actual_core_reconstruction_max_relative_error'],
            'original_failed_input200_sweeps_finite':True,
            'ordinary_path_bit_equal_component_controls':len(c['ordinary_path_bit_equal_controls']),
            'planted_trajectories_match_original_exactly':all(x['difference']==0 for x in c['planted']),
            'no_behavioral_KL_NLL_scored':c['no_behavioral_KL_NLL_scored']},
        'source':source,'source_sha256':sha(source),
        'evidence_sha256':{p:sha(p) for p in [evidence,'out/phase50_declared_first_failure_trace.json',
            'out/phase50_declared_failed_ALS_input_Qwen05_docs4_6.json',
            'out/phase50_declared_core_rayleigh_diagnostic.json']},
        'compatibility_with_already_successful_matrix_and_forward_results':c['prior_successful_results_compatibility'],
        'prior_finite_results_retained_unchanged':True,
        'CPU_float64_equivalence_status':'still failed; no acceptance criterion relaxed',
        'unselected_prototypes':['QR overflow scaling (QR had finite moderate entries)',
            'signed-negative-only SVD correction (actual native singular value was infinite)'],
        'recorded_before_patched_behavioral_forward':True}
    with target.open('x',encoding='utf-8') as out:json.dump(result,out,indent=2,ensure_ascii=False,allow_nan=False)
    print('RECORDED NATIVE SVD IMPLEMENTATION FIX',sha(target),flush=True)
    return result

if __name__=='__main__':main()
