"""Record the user's FP32 method declaration before any b/c/f behavioral KL."""
import json,hashlib
from datetime import datetime,timezone
from pathlib import Path

PATH=Path('out/phase50_declared_fp32_decision.json')
SNAPSHOT=Path('out/phase50_report_before_declared_fp32_forward.json')

USER_DECISION='''Decisão minha, tomada antes de ver qualquer KL de b/c/f: o portão de equivalência com a referência float64 servia para provar que GPU e CPU eram o mesmo estimador. Não são (o ridge e a trajetória mudam a solução, e o próprio problema mascarado é mal posto: fatores enormes, sem convergência). Então o método do braço mascarado passa a ser declarado como o seu estimador float32: SVD truncada como início, 200 varreduras de ALS com ridge 1e-6*tr(G), Grams cumulativas, Cholesky em lote, rebalanceamento QR+SVD do núcleo. Ele passou na recuperação plantada e nos controles locais, e seu desempenho matricial já está medido (b: 0,046 a 0,082 em K=8), que é o número que o artigo vai citar para ele, ao lado do float64 como referência e da discordância entre os dois (registre ambos).'''

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def freeze():
    if PATH.exists():return read(PATH)
    old=read('out/phase50_report.json');protocol=read('out/phase50_fp32_protocol.json');sample=read('out/phase50_fp32_sample.json')
    if sample['document_indices']!=list(range(64)):raise AssertionError('The fixed64 articles changed')
    for m,meta in old['forward_models'].items():
        if any(meta['actual_article_count_per_arm_and_K'][arm][str(k)] for arm in ['masked_K','named_plus_masked','masked_K_diag_exact'] for k in [8,16]):
            raise AssertionError('Declared FP32 masked behavioral KL already present')
        path=Path(meta['metadata']['pairs_path'])
        if sha(path)!=meta['metadata']['pairs_sha256']:raise AssertionError('Existing e data changed')
        if any(json.loads(line)['arm'] in ['masked_K','named_plus_masked','masked_K_diag_exact'] for line in path.read_text().splitlines() if line.strip()):
            raise AssertionError('Masked behavioral rows already present')
    controls=read('out/phase50_fp32_controls.json')
    if not controls['passed']:raise AssertionError('Plant/algebra controls did not pass')
    for p,digest in controls['sources'].items():
        if sha(p)!=digest:raise AssertionError('The declared estimator implementation changed')
    original=Path('out/phase50_report.json').read_bytes()
    if SNAPSHOT.exists():
        if SNAPSHOT.read_bytes()!=original:raise AssertionError('Predecessor snapshot differs')
    else:
        with SNAPSHOT.open('xb') as f:f.write(original)
    parent=read('out/phase50_protocol.json')
    result={'UTC':datetime.now(timezone.utc).isoformat(),'authority':'explicit user decision in this conversation',
        'user_decision_verbatim':USER_DECISION,'decision_before_first_behavioral_KL_b_c_f_for_declared_FP32_method':True,
        'method':{'name':'masked FP32 cumulative-Gram trace-ridge ALS','dtype':'float32','initialization':'truncated SVD with singular-value square roots',
            'sweeps':200,'early_stop':False,'ridge_relative_to_trace':1e-6,'ridge_absolute_floor_on_normalized_target':1e-30,
            'updates':'prefix/suffix cumulative Grams and masked-target matrix multiplication RHS; batched Cholesky',
            'rebalance_every_sweep':'QR of both factors plus SVD of KxK core, splitting square-root singular values',
            'backend':'CUDA Graph, previously controlled implementation, TF32 disabled','CPU_recomputations':False,
            'objective_increase_policy':'record all, no monotonic rejection, same existing FP32 estimator'},
        'CPU_float64_reference_equivalence':{'passed':False,'threshold_kept_for_historical_test':.002,
            'is_behavioral_execution_gate':False,'reason':'Ridge and optimization trajectory define a different finite200-sweep estimator. Original masked completion is ill-conditioned, factors can be huge and convergence is not established. The user declares the tested FP32 estimator as the method, not a replica of CPU float64.',
            'reference_results_and_all_disagreements_preserved':True,'legacy_float64_forward_probes_excluded':True},
        'models':protocol['models'],'K':[8,16],'n':128,'document_indices':list(range(64)),
        'sample_sha256':sha('out/phase50_fp32_sample.json'),'FP32_protocol_sha256':sha('out/phase50_fp32_protocol.json'),
        'parent_protocol_sha256':sha('out/phase50_protocol.json'),'estimator_sources':controls['sources'],
        'harness_sha256':parent['harness_sha256_at_freeze'],'corpus_manifest_sha256':parent['corpus_manifest_sha256'],
        'heads_exact_zero_based':protocol['unchanged']['heads'],'arms_run':['masked_K','named_plus_masked','masked_K_diag_exact'],
        'exact_alias_when_no_exempt_heads':{'masked_K_diag_exact':'masked_K'},
        'a_d_e_behavioral_results_reused_unchanged':True,
        'empty_row_measurement':'Count the actual harness empty mask. All-head/all-layer row denominator; exact heads contribute zero completions. Replay e to remove completion counts for discarded SVD candidates on exact heads; verify KL/NLL against existing e records.',
        'e_replay_is_counter_instrumentation_not_new_arm_or_sample':True,
        'execution':{'chunk_articles':16,'round_robin_models_each_chunk':True,'release_GPU_lock_between_every_model_and_chunk':True,'CPU_threads':4},
        'statistics':{'comparisons':[['masked_K','named_plus_svd'],['named_plus_masked','named_plus_svd'],['named_plus_masked','masked_K'],['masked_K_diag_exact','masked_K'],['svd_K_diag_exact','svd_K']],
            'Wilcoxon':'two-sided by article, wilcox zeros, asymptotic p','rank_biserial_positive_favors':'right arm','Holm_family_size':60,
            'CI':'phase24.describe,2000 whole-article bootstrap resamples,seed0','report_by_model_K_arm_and_pooled_K_empty_fractions':True},
        'predecessor_report_snapshot':SNAPSHOT.as_posix(),'predecessor_report_sha256':sha(SNAPSHOT),
        'report_update':'User explicitly requests completion of out/phase50_report.json. Preserve predecessor bytes and atomically replace only that report after all64 observations/arm/model/K and60 tests are audited.',
        'no_other_existing_scientific_files_overwritten':True}
    with PATH.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False)
    print('FROZEN USER DECLARATION',PATH,sha(PATH));return result

if __name__=='__main__':freeze()
