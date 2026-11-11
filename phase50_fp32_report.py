"""Final E9 tables, preserving failed numerical qualification as a failure."""
import phase50_fp32_als
import json,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from phase50_experiment import read,jsonl,describe,paired,holm,ARMS
from phase50_forward import source_records
from phase50_fp32_matrix import aggregate as aggregate_matrix
from sampling import MODELS,slug,sha256_file,write_json_new,sample_paths

sys.stdout.reconfigure(encoding='utf-8')

PROTOCOL='out/phase50_fp32_protocol.json'
COMPARISONS=read(PROTOCOL)['statistics']['paired_comparisons']

def interval(stats):
    if stats is None:return '—'
    lo,hi=stats['CI95_articles'];return f'{stats["median"]:.4g} [{lo:.4g}, {hi:.4g}]'

def render(result):
    lines=[result['status_explanation'],
        f'{result["n_articles_per_model"]} artigos por braço disponível; a=svd_K, b=masked_K, c=named_plus_masked, d=named_plus_svd, e=svd_K_diag_exact, f=masked_K_diag_exact.',
        'KL mediana [IC95 por artigos]. — significa não executado porque o estimador FP32 falhou no critério de equivalência com CPU, sem substituir resultados antigos.',
        '| Modelo | K | a | b | c | d | e | f |','|---|---:|---|---|---|---|---|---|']
    for r in result['forward_KL_table']:
        lines.append('| '+' | '.join([r['model'],str(r['K'])]+[interval(r['arms'][a]['KL']) for a in ARMS])+' |')
    lines+=['','Wilcoxon por artigo; Holm na família planejada de60 hipóteses; efeito positivo favorece o braço da direita.',
        '| Modelo | K | b-d pH; rb | c-d pH; rb | c-b pH; rb | e-a pH; rb | f-b pH; rb |',
        '|---|---:|---|---|---|---|---|']
    tests={(r['model'],r['K'],r['left'],r['right']):r for r in result['forward_paired_tests']}
    for r in result['forward_KL_table']:
        cells=[r['model'],str(r['K'])]
        for left,right in COMPARISONS:
            t=tests[r['model'],r['K'],left,right]
            cells.append('—' if not t['executed'] else f'{t["p_Holm"]:.3g}; {t["rank_biserial"]:+.4f}')
        lines.append('| '+' | '.join(cells)+' |')
    lines+=['','Matriz com o estimador FP32 regularizado: Frobenius relativo / TV média após normalização causal;384 matrizes/modelo,64 documentos. Esta tabela não representa equivalência com o ajustador CPU sem ridge.',
        '| Modelo | K | a | b | c | d |','|---|---:|---|---|---|---|']
    for r in result['matrix_table_FP32']:
        lines.append('| '+' | '.join([r['model'],str(r['K'])]+[f'{r["arms"][a]["frobenius"]["median"]:.4f} / {r["arms"][a]["TV"]["median"]:.4f}' for a in ARMS[:4]])+' |')
    lines+=['','Validação,32 matrizes/modelo ×2K ×2alvos =128 ajustes. Aceite: máxima diferença de erro relativo ≤0,002.',
        '| Modelo | Δerro máximo | ΔFrob normalizado máximo | ΔTV máximo | Passou |',
        '|---|---:|---:|---:|---|']
    for m,r in result['numerical_validation'].items():
        lines.append(f'| {m} | {r["max_absolute_relative_error_difference"]:.6g} | {r["max_normalized_frobenius_difference"]:.6g} | {r["max_TV_difference"]:.6g} | {r["passed"]} |')
    lines+=['']+result['honest_reading'];return '\n'.join(lines)

def main():
    if Path('out/phase50_report.json').exists():raise FileExistsError('Preserve existing report')
    sample=read('out/phase50_fp32_sample.json');n=sample['n_articles_per_model_all_arms'];ids=list(range(n))
    predeclaration=read('out/phase50_fp32_sample_predeclaration.json')
    if predeclaration['document_indices']!=ids or predeclaration['n_articles_per_model_available_arms']!=n:
        raise AssertionError('Forward article set differs from the timing-based predeclaration')
    protocol=read(PROTOCOL);parent=read('out/phase50_protocol.json');ph=sha256_file(PROTOCOL)
    matrix=aggregate_matrix() if not Path('out/phase50_fp32_matrix_summary.json').exists() else read('out/phase50_fp32_matrix_summary.json')
    refmatrix=read('out/phase50_matrix_summary.json')
    validation={m:read(f'out/phase50_fp32_validation_{slug(m)}.json') for m in MODELS}
    timing={m:read(f'out/phase50_fp32_timing_{slug(m)}.json') for m in MODELS}
    forward_table=[];tests=[];model_details={};audit_checks=[];matrix_table=[];cpu_table=[]
    for model in MODELS:
        a,d,source,corpus=source_records(model)
        cfg=parent['datasets'][model]
        archive,manifestpath=sample_paths(model,128)
        if sha256_file(archive)!=cfg['archive_sha256'] or sha256_file(manifestpath)!=cfg['manifest_sha256']:
            raise AssertionError('Frozen archive/manifest changed')
        vm=validation[model];vv=jsonl(vm['pairs_path'])
        if sha256_file(vm['pairs_path'])!=vm['pairs_sha256'] or len(vv)!=128:
            raise AssertionError('Validation records incomplete or modified')
        expectedval={(i,k,arm) for i in cfg['GPU_validation_indices'] for k in (8,16) for arm in ('masked_K','named_plus_masked')}
        if {(v['archive_index'],v['K'],v['arm']) for v in vv}!=expectedval:
            raise AssertionError('Original32 validation selection changed')
        if vm['passed']!=all(v['absolute_relative_error_difference']<=.002 for v in vv):
            raise AssertionError('Numerical acceptance was changed')
        mm=matrix['models'][model];mr=jsonl(mm['pairs_path'])
        if sha256_file(mm['pairs_path'])!=mm['pairs_sha256'] or len(mr)!=768:
            raise AssertionError('Matrix records incomplete or changed')
        if {(r['archive_index'],r['K']) for r in mr}!={(i,k) for i in cfg['matrix_archive_indices'] for k in (8,16)}:
            raise AssertionError('Frozen384 matrix selection changed')
        for r in mr:
            if r['doc_id']!=corpus['documents'][r['document_index']]['doc_id'] or r['protocol_sha256']!=ph:
                raise AssertionError('Matrix article/protocol mismatch')
            if r['masked_parameters']>r['cap'] or r['named_masked_parameters']>r['cap']:
                raise AssertionError('Storage budget exceeded')
            for arm in ('masked_K','named_plus_masked'):
                info=r['arms'][arm]['ALS']
                if info['sweeps']!=200 or info['dtype']!='float32' or info['ridge_relative_to_trace']!=1e-6 or info['CPU_recomputations']!=0:
                    raise AssertionError('Estimator precision/sweeps/ridge changed')
        meta=read(f'out/phase50_fp32_forward_{slug(model)}.json');rows=jsonl(meta['pairs_path'])
        if sha256_file(meta['pairs_path'])!=meta['pairs_sha256'] or meta['n_articles']!=n or meta['protocol_sha256']!=ph:
            raise ValueError('Forward model provenance mismatch')
        expected={(arm,k,i) for arm in meta['arms_run'] for k in (8,16) for i in ids}
        keys={(r['arm'],r['K'],r['document_index']) for r in rows}
        if keys!=expected or len(keys)!=len(rows):raise AssertionError('Incomplete/duplicate scientific forward')
        if any(r['identity_KL']!=0 or r['protocol_sha256']!=ph or r['sample_sha256']!=sha256_file('out/phase50_fp32_sample.json') for r in rows):
            raise AssertionError('Identity/sample/protocol violation')
        proof=read(f'out/phase50_fp32_forward_sanity_{slug(model)}.json')
        if not proof['identity_KL_exactly_zero']:raise AssertionError('Native identity proof failed')
        groups={(arm,k):sorted([r for r in rows if r['arm']==arm and r['K']==k],key=lambda r:r['document_index']) for arm in ARMS for k in (8,16)}
        for k in (8,16):
            groups['svd_K',k]=[a[k,i] for i in ids]
            groups['named_plus_svd',k]=[{'kl':d[k,i]['named_KL'],'nll':d[k,i]['named_NLL'],'document_index':i} for i in ids]
        for alias,sourcearm in meta['aliases'].items():
            for k in (8,16):groups[alias,k]=groups[sourcearm,k]
        model_details[model]={'metadata':meta,'native_sanity':proof,
            'actual_article_count_per_arm_and_K':{arm:{str(k):len(groups[arm,k]) for k in (8,16)} for arm in ARMS},'K':{}}
        for k in (8,16):
            row={'model':model,'K':k,'arms':{}}
            for arm in ARMS:
                group=groups[arm,k]
                if not group:
                    row['arms'][arm]={'KL':None,'NLL':None,'executed':False,'reason':'FP32 estimator failed the fixed2e-3 CPU-reference acceptance criterion'}
                    continue
                if [r['document_index'] for r in group]!=ids:raise AssertionError('Paired article set mismatch')
                def stats(metric):
                    result=describe([r[metric] for r in group],ids)
                    result['CI95_articles']=result['median_ci_document_bootstrap'];return result
                result={'KL':stats('kl'),'NLL':stats('nll'),'executed':True,
                    'reused':arm in ('svd_K','named_plus_svd'),'exact_alias_of':meta['aliases'].get(arm)}
                if group[0].get('ALS'):
                    dd=[r['ALS'] for r in group]
                    result['ALS']={'n_fits':sum(x['n_fits'] for x in dd),'converged':sum(x['converged'] for x in dd),
                        'maximum_absolute_factor':max(x['maximum_absolute_factor'] for x in dd),
                        'maximum_dynamic_range':max(x['maximum_dynamic_range'] for x in dd),
                        'maximum_QR_observed_product_error':max(x['maximum_QR_observed_product_error'] for x in dd),'CPU_recomputations':0}
                row['arms'][arm]=result
            forward_table.append(row);model_details[model]['K'][str(k)]=row['arms']
            for left,right in COMPARISONS:
                ll,rr=groups[left,k],groups[right,k]
                test={'model':model,'K':k,'left':left,'right':right,'executed':bool(ll and rr)}
                if ll and rr:
                    test.update(paired([x['kl']-y['kl'] for x,y in zip(ll,rr)],ids))
                else:test.update(p_two_sided=None,p_Holm=None,rank_biserial=None,reason='Masked estimator did not qualify; no behavioral observations substituted')
                tests.append(test)
            matrix_table.append({'model':model,'K':k,'arms':matrix['models'][model]['K'][str(k)]['arms']})
            cpu_table.append({'model':model,'K':k,'result':refmatrix['models'][model]['K'][str(k)]})
        audit_checks.append({'model':model,'source_all256_a_d_equal_exact':True,'identity_KL_exactly_zero':True,
            'scientific_forward_pairs_sha256':meta['pairs_sha256'],'complete_expected_available_arm_observations':True,
            'matrix_384_same_frozen_indices':read(f'out/phase50_fp32_matrix_{slug(model)}.json')['n_matrices']==384,
            'max_relative_error_difference_rechecked_from_pairs':max(x['absolute_relative_error_difference'] for x in jsonl(validation[model]['pairs_path']))})
    if len(tests)!=60:raise AssertionError('Planned Holm60 family incomplete')
    # Missing hypotheses retain their place in the planned family with p=1;
    # published unavailable tests remain null rather than fabricated outcomes.
    adjusted=[t if t['executed'] else {'p_two_sided':1.} for t in tests];holm(adjusted)
    for t in tests:
        if not t['executed']:t['Holm_family_size']=60
    failed=[m for m in MODELS if not validation[m]['passed']]
    complete=not failed
    matrix_diagnostics=[cell['arms'][arm]['ALS'] for m in matrix['models'].values()
        for cell in m['K'].values() for arm in ('masked_K','named_plus_masked')]
    numerical_summary={'n_matrix_ALS_fits':sum(x['n_fits'] for x in matrix_diagnostics),
        'converged_under_original_unregularized_gradient_criterion':sum(x['converged'] for x in matrix_diagnostics),
        'maximum_absolute_factor':max(x['maximum_absolute_factor'] for x in matrix_diagnostics),
        'maximum_factor_max_over_min_nonzero':max(x['maximum_dynamic_range'] for x in matrix_diagnostics),
        'maximum_QR_observed_product_error_relative_to_target':max(x['maximum_QR_observed_product_error'] for x in matrix_diagnostics),
        'ratio_is_not_a_condition_number':True,'CPU_recomputations_in_estimator':0,
        'QR_algebraically_preserves_product_but_FP32_roundoff_measured':True,
        'FP32_regularized_update_has_no_monotonic_rejection_policy':True}
    matrix_highlights={}
    for comparison in ('masked_K__minus__named_plus_svd','named_plus_masked__minus__named_plus_svd','masked_K__minus__named_plus_masked'):
        matrix_highlights[comparison]={}
        for metric in ('frobenius','TV'):
            values=[cell['paired'][comparison][metric] for m in matrix['models'].values() for cell in m['K'].values()]
            matrix_highlights[comparison][metric]={'maximum_p_Holm':max(t['p_Holm'] for t in values),
                'rank_biserial_range':[min(t['rank_biserial'] for t in values),max(t['rank_biserial'] for t in values)],
                'n_model_rank_cells':12,'n_documents_per_cell':64,'Holm_family_size':144}
    audits={m:read(f'out/phase50_fp32_failure_audit_{slug(m)}.json') for m in MODELS if Path(f'out/phase50_fp32_failure_audit_{slug(m)}.json').exists()}
    svd_warnings=[]
    for log in sorted(Path('out').glob('phase50_fp32*execution*.log')):
        for number,line in enumerate(log.read_text(encoding='utf-8').splitlines(),1):
            if 'failed to converge' in line and 'SVD' in line:
                svd_warnings.append({'log_path':log.as_posix(),'line':number,'warning':line,
                    'recorded_message_not_total_library_fallback_invocations':True})
    reading=[
        'A engenharia removeu o custo dominante: ALS FP32 com Grams cumulativas, soluções Cholesky em lote,200 varreduras e rebalanceamento QR/SVD capturado em CUDA Graph; nenhuma recomputação CPU no estimador.',
        'Na comparação matricial da variante FP32 regularizada, b tem medianas menores que c e d nas12 combinações modelo×K, tanto em Frobenius normalizado como em TV. b-d e c-d têm rank-biserial−1 em todas as células; a maior p de Holm é5,07672e-10. Para b-c, a maior p de Holm em Frobenius é7,19354e-6. Esses são resultados matriciais do ajustador testado, sem garantia de ótimo global ou equivalência com a CPU.',
        'O limite de aceite0,002 foi mantido. Falharam: '+', '.join(failed)+'.' if failed else 'Todos os seis modelos passaram na equivalência numérica fixada.',
        'O ridge1e-6 vezes o traço foi declarado antes dos resultados e é igual em todos os modelos/braços. A referência CPU não usa esse ridge e também tem uma política de repetição/rejeição monotônica; são trajetórias de otimização diferentes. Prefixos de comprimento menor que K são singulares e as equações normais elevam ao quadrado o condicionamento.',
        'O teste compara diferenças absolutas, não só degradação: no pior caso do Qwen0.5B, o erro causal bruto da CPU é0,774436 e o da GPU com ridge é0,165118. A variante acelerada foi melhor nesse caso e ainda assim reprovou a equivalência. Não se deve descrever toda reprovação como menor precisão da GPU.',
        'As24 combinações modelo×K×braço mascarado falharam individualmente no limite0,002. O maior desvio de cada modelo ocorre fora das cabeças quase diagonais fixadas; a isenção dessas cabeças não elimina esses casos de desacordo nas matrizes arquivadas.',
        'A validação plantada e os controles locais de álgebra passaram. Isso não garante proximidade ao estimador CPU nas atenções reais, nem convergência ao ótimo global.',
        'Os braços mascarados reprovados não foram usados para uma comparação comportamental qualificada. Seus campos de KL/testes estão nulos; os antigos probes float64 não foram misturados. A tabela matricial FP32 mede explicitamente outra variante regularizada.',
        'As comparações e-a avaliam o efeito de preservar as cabeças quase diagonais sob SVD. Mesmo um ganho nessa ablação não resolve se S+L vence um ajustador causal de posto baixo que tenha passado na validação.',
        'A superioridade comportamental de S+L sobre o estimador causal CPU float64 continua sem resposta neste protocolo. A precisão matricial e o custo computacional, isoladamente, não justificam uma conclusão sobre KL.'
    ]
    reading.insert(4,f'Nos9216 ajustes matriciais FP32, {numerical_summary["converged_under_original_unregularized_gradient_criterion"]} atendem ao critério original de convergência; maior fator absoluto {numerical_summary["maximum_absolute_factor"]:.6g}, maior razão máximo/mínimo não nulo {numerical_summary["maximum_factor_max_over_min_nonzero"]:.6g} (não é número de condição). A maior variação observada do produto causal no rebalanceamento QR/SVD foi {numerical_summary["maximum_QR_observed_product_error_relative_to_target"]:.6g} em unidades da norma do alvo. O ridge relativo ao traço e o balanceamento não garantiram fatores limitados nem preservação numérica perfeita do produto observado.')
    if not failed:reading=[s for s in reading if 'reprovados' not in s and 'continua sem resposta' not in s]
    result={'created_UTC':datetime.now(timezone.utc).isoformat(),'experiment':'E9','revision':'FP32 cumulative-Gram',
        'status':'complete' if complete else 'numerical_acceptance_failed_masked_forward_not_qualified',
        'status_explanation':'Experimento completo com o ajustador FP32 qualificado.' if complete else 'Engenharia, validação, tabela matricial e ablação SVD com cabeças exatas concluídas; comparação comportamental mascarada impedida pela falha do critério numérico.',
        'complete_scientific_E9_forward_comparison':complete,'protocol_sha256':ph,'parent_protocol_sha256':sha256_file('out/phase50_protocol.json'),
        'n_articles_per_model':n,'sample':sample,'sample_predeclaration':predeclaration,'ALS_sweeps':200,'ridge_relative_to_trace':1e-6,
        'numerical_acceptance_fixed_threshold':.002,'failed_models':failed,
        'forward_KL_table':forward_table,'forward_paired_tests':tests,'forward_Holm_planned_family_size':60,
        'forward_Holm_missing_hypotheses_policy':'p=1 placeholders for planned-family correction; unavailable scientific tests remain null',
        'forward_models':model_details,'matrix_table_FP32':matrix_table,'matrix_FP32_summary_path':'out/phase50_fp32_matrix_summary.json',
        'matrix_precision_and_sources':{'a_d':'original CPU float64 reconstructions/normalization from the preserved384-matrix study, reused unchanged',
            'b_c':'GPU float32 trace-ridge200-sweep fits; same384 archived matrices, causal normalization imported from phase2'},
        'matrix_paired_highlights':matrix_highlights,
        'matrix_CPU_float64_reference_table':cpu_table,'matrix_CPU_reference_summary_path':'out/phase50_matrix_summary.json',
        'numerical_validation':validation,'numerical_controls':read('out/phase50_fp32_controls.json'),
        'numerical_validation_compact_readout':read('out/phase50_fp32_validation_readout.json'),
        'numerical_diagnostics_summary':numerical_summary,
        'direction_at_maximum_validation_disagreement':{m:{
            'CPU_raw_causal_error':v['worst']['CPU']['raw_causal_frobenius'],
            'GPU_raw_causal_error':v['worst']['GPU']['raw_causal_frobenius'],
            'signed_GPU_minus_CPU_error':v['worst']['GPU']['raw_causal_frobenius']-v['worst']['CPU']['raw_causal_frobenius'],
            'interpretation':'GPU lower error at this case' if v['worst']['GPU']['raw_causal_frobenius']<v['worst']['CPU']['raw_causal_frobenius'] else 'GPU higher error at this case'
            } for m,v in validation.items()},
        'numerical_failure_mechanism_exploratory_audits':audits,
        'timings':timing,'heads_nearly_diagonal_zero_based':protocol['unchanged']['heads'],
        'initial_SVD_recorded_library_fallback_warnings':svd_warnings,
        'initial_SVD_fallback_note':'PyTorch CUDA default SVD may retry a nonconverged Jacobi SVD with its more accurate CUDA SVD driver. Same truncated-SVD initialization, no CPU ALS recomputation. Warnings preserved in execution logs; no exception caught or nonfinite value replaced.',
        'honest_reading':reading,
        'decisions':[{'decision':'Stop96302 and only its owned descendants by PID; preserve all prior artifacts','certainty':'alta','executed':True},
            {'decision':'FP32 cumulative Grams,200 fixed sweeps,uniform ridge,QR and core SVD,CUDA Graph,no CPU fallback','certainty':'alta','executed':True},
            {'decision':'Keep CPU-reference acceptance threshold2e-3 and report all six validations','certainty':'alta','executed':True},
            {'decision':'Project all-model service time from real two-article batches with20percent margin','certainty':'media','executed':True},
            {'decision':f'Use{n} corpus articles from runtime-only frozen rule','certainty':'alta','executed':True},
            {'decision':'All requested qualified masked forwards','certainty':'alta','executed':complete,'reason':None if complete else 'Numerical acceptance failed; no substitute estimator presented as equivalent'},
            {'decision':'S+L superiority over validated masked low rank','certainty':'baixa','executed':False,'reason':'No affirmative conclusion without qualified forward'}],
        'old_outputs_preserved':True,'paper_or_git_modified_by_this_experiment':False,
        'GPU_lock_released_between_models':True,'all_heavy_CPU_workers_threads':4}
    result['baseline_reuse_equality_semantics']='Every V1 SVD measurement equals the SVD reused by E4 on all256 articles/bothK. Native reruns compare a and d separately with their own original observations; this does not assert a equals d.'
    result['rendered_tables_markdown']=render(result)
    # Internal audit, not an independent reviewer or a proof of equivalence.
    def finite(obj):
        if isinstance(obj,dict):return all(finite(v) for v in obj.values())
        if isinstance(obj,(list,tuple)):return all(finite(v) for v in obj)
        if isinstance(obj,float):return bool(np.isfinite(obj))
        return True
    if not finite(result):raise FloatingPointError('Nonfinite report field')
    if sha256_file('phase2_downstream.py')!=parent['harness_sha256_at_freeze']:raise AssertionError('Harness modified')
    audit={'passed_for_executed_scope':True,'complete_scientific_E9_forward_comparison':complete,
        'numerical_acceptance_passed_for_all_models':complete,'planned_Holm_family':60,'executed_paired_tests':sum(t['executed'] for t in tests),
        'all_report_numbers_finite_or_explicit_null':True,'harness_unchanged':True,'per_model':audit_checks,
        'internal_self_audit_not_independent':True,'protocol_sha256':ph}
    write_json_new('out/phase50_fp32_integrity_audit.json',audit)
    result['integrity_audit_path']='out/phase50_fp32_integrity_audit.json'
    write_json_new('out/phase50_report.json',result)
    sources=[p for p in Path('.').glob('phase50_fp32_*.py')]
    artifacts={'report':'out/phase50_report.json','report_sha256':sha256_file('out/phase50_report.json'),
        'status':result['status'],'complete_scientific_E9_forward_comparison':complete,
        'scripts':{str(p):sha256_file(p) for p in sources},
        'scientific_json_files':{str(p):sha256_file(p) for p in Path('out').glob('phase50_fp32_*.json')},
        'scientific_pairs':{str(p):sha256_file(p) for p in Path('out/pairs').glob('phase50_fp32_*.jsonl')}}
    write_json_new('out/phase50_fp32_artifacts.json',artifacts)
    write_json_new('out/phase50_fp32_finished.json',{'status':result['status'],'complete_scientific_E9_forward_comparison':complete,
        'report_path':'out/phase50_report.json','report_sha256':sha256_file('out/phase50_report.json')})
    print(result['rendered_tables_markdown'],flush=True)

if __name__=='__main__':main()
