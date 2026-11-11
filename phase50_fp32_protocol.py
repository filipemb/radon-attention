"""Freeze the user-authorized FP32 revision before numerical/behavioral results."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone

PATH=Path('out/phase50_fp32_protocol.json')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def freeze():
    if PATH.exists():return json.loads(PATH.read_text())
    old=json.loads(Path('out/phase50_protocol.json').read_text())
    result={'created_UTC':datetime.now(timezone.utc).isoformat(),'experiment':'E9 FP32 revision requested by user',
        'parent_protocol_sha256':sha('out/phase50_protocol.json'),'old_outputs_preserved':True,
        'models':old['models'],'K':[8,16],'n':128,
        'ALS':{'dtype':'float32','sweeps':200,'early_stop':False,'initialization':'truncated SVD, singular-value square roots; same stored double initialization rounded to FP32 for CPU/GPU validation',
            'normal_equations':'prefix/suffix cumulative outer products; target@factor RHS; batched KxK Cholesky solves',
            'ridge_relative_to_trace':1e-6,'ridge_absolute_floor_on_normalized_target':1e-30,
            'ridge_rationale':'each causal prefix/suffix with fewer than K observations has singular Gram; FP32 normal equations also square conditioning',
            'ridge_uniform_across_all_models_and_b_c_f':True,'TF32':False,
            'balance':'QR of both factors; SVD of Ru Rv^T; split sqrt(singular values) after EACH sweep',
            'CPU_recomputation':False,'objective_increases':'record all; do not stop or reject regularized block updates',
            'GPU_graph_allowed':'same FP32 algebra only; component/product controls before estimator validation'},
        'validation':{'same_32_archive_indices_as_previous':True,'both_K_and_b_c':True,'n_fits_per_model':128,
            'reference':'independent archived CPU float64 estimator, 200 sweeps, unregularized same initial factors',
            'max_absolute_raw_relative_frobenius_error_difference_tolerance':0.002,
            'report_also_normalized_frobenius_and_TV':True,'no_CPU_correction':True,
            'on_failure':'preserve all diagnostics; continue validation in remaining models; no qualified behavioral claim for failed FP32 estimator; never relax threshold'},
        'timing_and_sample':{'GPU_limit_seconds_for_256_articles_all_models_b_c_e_f_both_K':28800,
            'timing_batch_size':2,'performance_probe_articles':[0,1],'no_KL_outcome_selected_sample':True,
            'estimate':'per-model actual first two-article batch (all required arms/both K); subtract one-time controls/load/graph compilation for steady estimate, include measured native/SVD controls and reload overhead per model; extrapolate128 batches and conservatively multiply by1.2',
            'if_estimate_le_28800':'all256 documents in corpus order',
            'otherwise':'first64 documents0..63 of original corpus, the same documents as frozen matrix sample, all arms and models',
            'release_GPU_lock':'between every model; also between timing/validation stages',
            'sample_freeze':'write out/phase50_fp32_sample.json after timing and before any scientific forward scoring',
            'if_validation_fails':'time estimator anyway; report the failure; forward only numerically qualified masked models; e independent of ALS remains eligible'},
        'unchanged':{'harness_sha256':old['harness_sha256_at_freeze'],'corpus_manifest_sha256':old['corpus_manifest_sha256'],
            'heads':{m:old['datasets'][m]['diagonal_heads'] for m in old['models']},'storage':old['storage'],
            'matrix_sample':'same384/model,64 documents,6 layer strata; prior CPU float64 matrix results remain explicitly a distinct estimator'},
        'statistics':{'describe':'import phase24.describe;2000 whole-article bootstrap samples,seed0',
            'paired_comparisons':[['masked_K','named_plus_svd'],['named_plus_masked','named_plus_svd'],['named_plus_masked','masked_K'],['svd_K_diag_exact','svd_K'],['masked_K_diag_exact','masked_K']],
            'tests':'two-sided Wilcoxon per article, wilcox zeros, asymptotic p; rank-biserial positive favors right',
            'Holm_family_size':60,'missing_comparisons':'unavailable, no fabricated p; missing hypotheses treated as p=1 for planned family60 correction'},
        'fixed_before_new_FP32_results':True}
    with PATH.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,allow_nan=False)
    print('FROZEN',PATH,sha(PATH));return result

if __name__=='__main__':freeze()
