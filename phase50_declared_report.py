"""Complete E9 for the explicitly declared FP32 method; preserve CPU reference."""
import phase50_fp32_als
import copy,hashlib,json,os,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import phase2_downstream as harness
from phase50_experiment import read,jsonl,describe,paired,holm,ARMS
from phase50_forward import source_records,reuse
from phase50_declared_forward import DECISION,E_REPLAY,IMPLEMENTATION_FIX,methods,check_decision,check_implementation_fix
from sampling import slug,sha256_file,write_json_new,sample_paths

sys.stdout.reconfigure(encoding='utf-8')

def execution_log_prefix():
    """Commit a prefix: the coordinator appends its report end event later."""
    path=Path('out/pairs/phase50_declared_events.jsonl')
    version=Path('out/phase50_declared_report.json');audit=Path('out/phase50_declared_integrity_audit.json')
    if version.exists():value=read(version)['completed_chunk_execution_timing']['execution_log_committed_prefix']
    elif audit.exists():value=read(audit)['execution_log_committed_prefix']
    else:
        data=path.read_bytes()
        value={'path':path.as_posix(),'byte_length':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'scope':'Committed execution history through report start; coordinator can append the report end event after publication'}
    data=path.read_bytes()[:value['byte_length']]
    if len(data)!=value['byte_length'] or hashlib.sha256(data).hexdigest()!=value['sha256']:
        raise AssertionError('Committed execution log prefix changed')
    return value

def record_groups(model,dec):
    """Assemble six paired arms; reuse a/d/e observations literally."""
    source_records(model);rr=reuse(model)
    base=[r for r in jsonl(rr['pairs_path']) if r['document_index']<64]
    meta=read(f'out/phase50_declared_forward_{slug(model)}.json');rows=jsonl(meta['pairs_path'])
    if sha256_file(meta['pairs_path'])!=meta['pairs_sha256'] or meta['decision_sha256']!=sha256_file(DECISION):
        raise AssertionError('Declared forward provenance mismatch')
    if any(sha256_file(p)!=digest for p,digest in meta['chunk_sha256'].items()):raise AssertionError('A model checkpoint changed')
    cfg=read('out/phase50_protocol.json')['datasets'][model]
    keys={(r['arm'],r['K'],r['document_index']) for r in rows}
    expected={(arm,k,i) for arm in methods(cfg) for k in (8,16) for i in range(64)}
    if keys!=expected or len(rows)!=len(keys):raise AssertionError('Incomplete or duplicate model observations')
    if any(r['identity_KL']!=0 or r['decision_sha256']!=sha256_file(DECISION) or r['sample_sha256']!=dec['sample_sha256'] for r in rows):
        raise AssertionError('Identity/declaration/article mismatch')
    groups={(arm,k):[] for arm in ARMS for k in (8,16)}
    for r in base:groups[r['arm'],r['K']].append(r)
    for r in rows:
        if r['arm']!=E_REPLAY:groups[r['arm'],r['K']].append(r)
    oldmeta=read(f'out/phase50_fp32_forward_{slug(model)}.json')
    if sha256_file(oldmeta['pairs_path'])!=oldmeta['pairs_sha256']:raise AssertionError('Preserved e records changed')
    if cfg['diagonal_heads']:
        replay={(r['K'],r['document_index']):r for r in rows if r['arm']==E_REPLAY}
        for raw in jsonl(oldmeta['pairs_path']):
            if raw['arm']!='svd_K_diag_exact':raise AssertionError('Unexpected old FP32 behavioral arm')
            r=dict(raw);other=replay[r['K'],r['document_index']]
            if max(other['e_KL_absolute_replay_difference'],other['e_NLL_absolute_replay_difference'])>2e-5:
                raise AssertionError('e counter replay changed behavior')
            r['uniform_completion_batch']=other['uniform_completion_batch']
            r['uniform_completion_source']='declared forward e counter replay; original e behavioral KL/NLL retained'
            groups['svd_K_diag_exact',r['K']].append(r)
    else:
        for k in (8,16):
            groups['svd_K_diag_exact',k]=groups['svd_K',k]
            groups['masked_K_diag_exact',k]=groups['masked_K',k]
    for key,g in groups.items():
        g.sort(key=lambda r:r['document_index'])
        if [r['document_index'] for r in g]!=list(range(64)):raise AssertionError(f'All64 articles required for {model}/{key}')
        for r,baseline in zip(g,groups['svd_K',key[1]]):
            if any(r[f]!=baseline[f] for f in ('doc_id','offset','target_id','dtype','n','batch_start','batch_size')):
                raise AssertionError('An arm changed article, target, dtype or batch')
            if abs(r['reference_nll']-baseline['reference_nll'])>2e-5:
                raise AssertionError('An arm changed the native last-token reference')
    fix=check_implementation_fix()
    for r in rows:
        revision=r.get('implementation_fix_sha256')
        if revision is not None and (not fix or revision!=sha256_file(IMPLEMENTATION_FIX)):
            raise AssertionError('Uncontrolled numerical implementation revision')
    return groups,meta,rr,oldmeta,rows

def empty_summary(group,expected_rows,expected_last,exact_rows=0,exact_last=0):
    batches={}
    for row in group:
        key=(row['batch_start'],row['batch_size'])
        cc=row.get('uniform_completion_batch')
        if cc is None:cc=harness.completion_summary(row['attention_validation_batch'])
        if key in batches:
            if cc!=batches[key]:raise AssertionError('Duplicated article rows disagree on batch counters')
        else:batches[key]=cc
    if sorted(batches)!=[(i,2) for i in range(0,64,2)]:raise AssertionError('Wrong batch population for empty-row fraction')
    counters=['rows_total','rows_completed','last_query_rows_total','last_query_rows_completed']
    result={key:sum(s[key] for s in batches.values()) for key in counters}
    optional=['candidate_rows_completed_before_exact_overwrite','candidate_last_query_rows_completed_before_exact_overwrite',
        'discarded_exact_head_candidate_empty_rows','discarded_exact_head_candidate_empty_last_rows','exact_rows_total','exact_last_query_rows_total']
    for key in optional:
        present=[key in s for s in batches.values()]
        if any(present) and not all(present):raise AssertionError('Inconsistent optional completion counters')
        if all(present):result[key]=sum(s[key] for s in batches.values())
    if result.get('exact_rows_total',exact_rows)!=exact_rows or result.get('exact_last_query_rows_total',exact_last)!=exact_last:
        raise AssertionError('Observed exact-head row counts disagree with the fixed head list')
    result['exact_rows_total']=exact_rows;result['exact_last_query_rows_total']=exact_last
    if result['rows_total']!=expected_rows or result['last_query_rows_total']!=expected_last:
        raise AssertionError('Empty-row denominator does not cover every article/head/layer/query exactly once')
    if not 0<=result['rows_completed']<=expected_rows or not 0<=result['last_query_rows_completed']<=expected_last:
        raise AssertionError('Impossible actual uniform-completion counts')
    result.update(policy='uniform_causal',fraction_rows_completed=result['rows_completed']/expected_rows,
        fraction_last_query_rows_completed=result['last_query_rows_completed']/expected_last,n_articles=64,n_unique_batches=32,
        denominator_scope='all attention rows, including heads kept exact; exact heads contribute zero completions',
        aggregation='sum integer counts across unique batch_start/batch_size keys, not twice per article record')
    result['rows_reconstructed']=expected_rows-exact_rows
    result['fraction_reconstructed_rows_completed']=result['rows_completed']/(expected_rows-exact_rows) if expected_rows>exact_rows else 0.
    return result

def pool_empty(by_k):
    fields=['rows_total','rows_completed','last_query_rows_total','last_query_rows_completed']
    result={key:sum(v[key] for v in by_k) for key in fields}
    result.update(fraction_rows_completed=result['rows_completed']/result['rows_total'],
        fraction_last_query_rows_completed=result['last_query_rows_completed']/result['last_query_rows_total'],
        scope='K8 and K16 pooled by row counts, same64 articles in each experiment')
    return result

def als_summary(group):
    blocks=[r['ALS'] for r in group]
    if not blocks or blocks[0] is None:return None
    if any(x['sweeps_per_fit']!=200 or x['ridge_relative_to_trace']!=1e-6 or x['CPU_recomputations']!=0 for x in blocks):
        raise AssertionError('Declared ALS settings changed')
    return {'n_fits':sum(x['n_fits'] for x in blocks),'converged_under_original_gradient_criterion':sum(x['converged'] for x in blocks),
        'invalid_native_core_singular_values_recomputed':sum(x.get('invalid_native_core_singular_values_recomputed',0) for x in blocks),
        'fits_with_native_core_singular_value_recomputation':sum(x.get('fits_with_native_core_singular_value_recomputation',0) for x in blocks),
        'factor_magnitudes_scope':'final balanced factors, maximum across fits; not the maximum of every intermediate sweep',
        'history_aggregation':'median across articles of each article\'s median across fitted head/layer matrices',
        'convergence_criterion':'original unregularized normalized-target gradient<=1e-6 and (last20 relative objective change<=1e-7 or squared error<=1e-12); this is not a penalized-objective optimality certificate',
        'maximum_absolute_factor':max(x['maximum_absolute_factor'] for x in blocks),
        'maximum_factor_max_over_min_nonzero':max(x['maximum_dynamic_range'] for x in blocks),
        'maximum_QR_observed_product_error_relative_to_target':max(x['maximum_QR_observed_product_error'] for x in blocks),
        'objective_increase_sweeps':sum(x['objective_increase_sweeps'] for x in blocks),'CPU_recomputations':0,'sweeps':200,
        'median_history':[{'sweep':s,'relative':float(np.median([next(h['relative'] for h in x['median_history'] if h['sweep']==s) for x in blocks]))} for s in phase50_fp32_als.CHECKPOINTS]}

def stats(group,metric):
    s=describe([r[metric] for r in group],range(64));s['CI95_articles']=s['median_ci_document_bootstrap'];return s

def interval(s):
    lo,hi=s['CI95_articles'];return f'{s["median"]:.4g} [{lo:.4g}, {hi:.4g}]'

def render(result):
    lines=['E9 completo para o método FP32 declarado pelo usuário;64 artigos, K8/16, seis modelos. A equivalência com a referência float64 não foi atendida e não é um portão de execução.',
        'a=svd_K; b=masked_K; c=named_plus_masked; d=named_plus_svd; e=svd_K_diag_exact; f=masked_K_diag_exact.',
        'KL mediana [IC95 por artigos]','',
        '| Modelo | K | a | b | c | d | e | f |','|---|---:|---|---|---|---|---|---|']
    for r in result['forward_KL_table']:
        lines.append('| '+' | '.join([r['model'],str(r['K'])]+[interval(r['arms'][a]['KL']) for a in ARMS])+' |')
    lines+=['','Wilcoxon por64 artigos, Holm na família60; rank-biserial positivo favorece o braço da direita.',
        '| Modelo | K | b-d pH; rb | c-d pH; rb | c-b pH; rb | f-b pH; rb | e-a pH; rb |',
        '|---|---:|---|---|---|---|---|']
    lookup={(t['model'],t['K'],t['left'],t['right']):t for t in result['forward_paired_tests']}
    for r in result['forward_KL_table']:
        cells=[r['model'],str(r['K'])]
        for left,right in result['declared_method_decision']['statistics']['comparisons']:
            t=lookup[r['model'],r['K'],left,right];cells.append(f'{t["p_Holm"]:.3g}; {t["rank_biserial"]:+.4f}')
        lines.append('| '+' | '.join(cells)+' |')
    lines+=['','Fração de linhas efetivamente completadas com uniforme causal, em porcentagem. Denominador: todos os artigos, cabeças, camadas e posições; deduplicação por lote.','',
        '| Modelo | K | a | b | c | d | e | f |','|---|---:|---|---|---|---|---|---|']
    for model,rr in result['empty_row_fractions_by_model'].items():
        for k in ('8','16'):
            lines.append('| '+' | '.join([model,k]+[f'{100*rr["K"][k][a]["fraction_rows_completed"]:.6g}%' for a in ARMS])+' |')
    lines+=['','Matriz: Frobenius relativo / TV após normalização causal,384 matrizes/modelo,64 documentos. b/c são o método FP32 declarado; a/d reutilizados do estudo CPU. A tabela float64 permanece no JSON.','',
        '| Modelo | K | a | b | c | d |','|---|---:|---|---|---|---|']
    for r in result['matrix_table_FP32']:
        lines.append('| '+' | '.join([r['model'],str(r['K'])]+[f'{r["arms"][a]["frobenius"]["median"]:.4f}/{r["arms"][a]["TV"]["median"]:.4f}' for a in ARMS[:4]])+' |')
    return '\n'.join(lines+['']+result['honest_reading'])

def assemble():
    dec=check_decision();old=read(dec['predecessor_report_snapshot']);parent=read('out/phase50_protocol.json')
    fix=check_implementation_fix()
    if fix is None:raise AssertionError('The actual operational SVD failure and controlled correction must be recorded')
    if sha256_file(dec['predecessor_report_snapshot'])!=dec['predecessor_report_sha256']:raise AssertionError('Predecessor snapshot changed')
    result=copy.deepcopy(old);all_rows=[];tests=[];details={};empty={};audit=[]
    for model in dec['models']:
        groups,meta,base,old_e,raw=record_groups(model,dec)
        archive,manifest=sample_paths(model,128);cfg=parent['datasets'][model]
        if sha256_file(archive)!=cfg['archive_sha256'] or sha256_file(manifest)!=cfg['manifest_sha256']:raise AssertionError('Matrix archive/manifest changed')
        from sampling import CORPUS_PATH
        corpus=read(CORPUS_PATH);layer=corpus['models'][model]['n_layers'];head=corpus['models'][model]['n_heads']
        expected_rows=64*layer*head*128;expected_last=64*layer*head
        empty[model]={'K':{},'pooled_K':{}};details[model]={'metadata':meta,'baseline_metadata':base,'preserved_e_metadata':old_e,
            'native_sanity':read(f'out/phase50_fp32_forward_sanity_{slug(model)}.json'),'actual_article_count_per_arm_and_K':{a:{str(k):len(groups[a,k]) for k in (8,16)} for a in ARMS},'K':{}}
        for k in (8,16):
            row={'model':model,'K':k,'arms':{}};empty[model]['K'][str(k)]={}
            for arm in ARMS:
                n_exact=len(cfg['diagonal_heads']) if arm in ('svd_K_diag_exact','masked_K_diag_exact') else 0
                g=groups[arm,k];es=empty_summary(g,expected_rows,expected_last,64*n_exact*128,64*n_exact)
                empty[model]['K'][str(k)][arm]=es
                alias=('svd_K' if arm=='svd_K_diag_exact' else 'masked_K') if not cfg['diagonal_heads'] and arm in ('svd_K_diag_exact','masked_K_diag_exact') else None
                rr={'KL':stats(g,'kl'),'NLL':stats(g,'nll'),'executed':True,'reused':arm in ('svd_K','named_plus_svd','svd_K_diag_exact'),
                    'exact_alias_of':alias,'uniform_completion':es}
                if arm in ('masked_K','named_plus_masked','masked_K_diag_exact'):rr['ALS']=als_summary(g)
                row['arms'][arm]=rr
                if arm in ('svd_K','named_plus_svd','svd_K_diag_exact'):
                    oldcell=next(x for x in old['forward_KL_table'] if x['model']==model and x['K']==k)['arms'][arm]
                    if rr['KL']!=oldcell['KL'] or rr['NLL']!=oldcell['NLL']:raise AssertionError('A reused behavioral summary changed')
            all_rows.append(row);details[model]['K'][str(k)]=row['arms']
            for left,right in dec['statistics']['comparisons']:
                tt=paired([x['kl']-y['kl'] for x,y in zip(groups[left,k],groups[right,k])],range(64))
                tt.update(model=model,K=k,left=left,right=right,executed=True);tests.append(tt)
            active=max(r['max_active_atoms'] for r in groups['named_plus_masked',k])
            named_cost=2*active+2*128*(k-1)
            if named_cost>k*257:raise AssertionError('Named-plus-masked common storage cap exceeded')
            details[model]['K'][str(k)]['named_plus_masked']['storage_check']={
                'maximum_active_named_atoms':active,'maximum_parameters_per_reconstructed_head':named_cost,
                'cap':k*257,'max_NNLS_KKT':max(r['max_NNLS_KKT'] for r in groups['named_plus_masked',k]),
                'same_named_first_dictionary_and_NNLS_as_E4':True}
        for arm in ARMS:empty[model]['pooled_K'][arm]=pool_empty([empty[model]['K'][str(k)][arm] for k in (8,16)])
        replay=[r for r in raw if r['arm']==E_REPLAY]
        audit.append({'model':model,'all_six_arms_all64_articles_both_K':True,'new_pairs_sha256':meta['pairs_sha256'],
            'all_per_batch_identity_KL_zero':True,'all_empty_row_denominators_exact':True,'source_a_d_e_unchanged':True,
            'max_e_KL_replay_discrepancy':max((r['e_KL_absolute_replay_difference'] for r in replay),default=0.),
            'max_e_NLL_replay_discrepancy':max((r['e_NLL_absolute_replay_difference'] for r in replay),default=0.)})
    if len(tests)!=60:raise AssertionError('The planned family60 is incomplete')
    holm(tests)
    result.update(created_UTC=datetime.now(timezone.utc).isoformat(),revision='user-declared FP32 trace-ridge masked ALS',
        status='complete_declared_FP32_method_not_equivalent_to_CPU_float64',
        status_explanation='Todos os seis braços completos em64 artigos/K/modelo para o método FP32 explicitamente declarado. Equivalência com a referência CPU float64 não atendida, registrada e sem função de portão comportamental.',
        complete_scientific_E9_forward_comparison=True,complete_as_CPU_float64_replica=False,
        declared_method_decision=dec,declared_method_decision_sha256=sha256_file(DECISION),
        numerical_acceptance_is_behavioral_gate=False,CPU_float64_equivalence_passed=False,
        CPU_float64_equivalence_failed_models=old['failed_models'],
        CPU_float64_equivalence_test_role='Historical numerical-replication test, threshold unchanged; explicitly no longer a behavioral gate for the user-declared FP32 method',
        predecessor_report={'path':dec['predecessor_report_snapshot'],'sha256':dec['predecessor_report_sha256'],'status':old['status']},
        predecessor_decisions=old['decisions'],
        native_core_SVD_implementation_fix=fix,native_core_SVD_implementation_fix_sha256=sha256_file(IMPLEMENTATION_FIX),
        execution_schedule_adjustment={
            'reason':'Qwen0.5B stopped on the demonstrated native core SVD failure; other models continued while it was diagnosed',
            'adjustment':'Five-model round-robin coordinator plus a Qwen0.5B-only resume coordinator, both using the same flock for each16-article chunk',
            'article_order_batch_size_and_estimator_parameters_changed':False,
            'lock_released_after_every_chunk_and_between_models':True,
            'scientific_sample_or_hypotheses_changed':False},
        forward_KL_table=all_rows,forward_paired_tests=tests,forward_models=details,
        forward_Holm_missing_hypotheses_policy='No missing tests; all60 planned hypotheses evaluated',
        empty_row_fractions_by_model=empty,
        empty_row_fraction_definition='Actual uniform-causal completions / all attention rows, deduplicated by original batch2; exact heads contribute zero. e counters corrected from harness masks on behavior-checked replay.',
        empty_row_counter_control=read('out/phase50_declared_empty_counter_control.json'))
    result['storage_protocol']=parent['storage']
    result['sample_at_original_numerical_gate']=copy.deepcopy(old['sample'])
    result['sample']['CPU_float64_equivalence_passed_models_at_sampling']=result['sample'].pop('passed_models',[])
    result['sample']['all_models_executed_for_declared_FP32_method']=dec['models']
    result['sample']['CPU_reference_equivalence_is_current_execution_gate']=False
    result['completed_chunk_execution_timing']={
        'per_model_seconds':{m:d['metadata']['elapsed_chunk_seconds'] for m,d in details.items()},
        'total_seconds':sum(d['metadata']['elapsed_chunk_seconds'] for d in details.values()),
        'scope':'Elapsed worker execution inside the GPU lock for committed chunks, including loading/native checks/e counter replay; excludes lock waiting, diagnosis, and the failed first Qwen0.5B attempt that had written some valid partial records',
        'complete_event_history':'out/pairs/phase50_declared_events.jsonl',
        'execution_log_committed_prefix':execution_log_prefix(),
        'predeclared_full_run_estimates_and_selection_preserved':True}
    result.pop('failed_models',None)
    # Reading, integrity, publication and artifacts are defined below.
    return result,audit

def complete_reading(result):
    comparisons=result['declared_method_decision']['statistics']['comparisons'];summaries={}
    for left,right in comparisons:
        tests=[t for t in result['forward_paired_tests'] if (t['left'],t['right'])==(left,right)]
        summaries[left+'__minus__'+right]={
            'left_significantly_lower_KL':sum(t['p_Holm']<.05 and t['rank_biserial']<0 for t in tests),
            'right_significantly_lower_KL':sum(t['p_Holm']<.05 and t['rank_biserial']>0 for t in tests),
            'not_significant_after_Holm':sum(t['p_Holm']>=.05 for t in tests),
            'n_cells':12,'alpha':.05,'rank_biserial_range':[min(t['rank_biserial'] for t in tests),max(t['rank_biserial'] for t in tests)],
            'effect_direction':'positive difference/effect favors right'}
    result['forward_contrast_summary']=summaries
    blocks=[r['arms'][arm]['ALS'] for r in result['forward_KL_table'] for arm in ('masked_K','named_plus_masked','masked_K_diag_exact')
        if not r['arms'][arm]['exact_alias_of']]
    diag={'n_unique_computed_fits':sum(x['n_fits'] for x in blocks),
        'invalid_native_core_singular_values_recomputed':sum(x['invalid_native_core_singular_values_recomputed'] for x in blocks),
        'fits_with_native_core_singular_value_recomputation':sum(x['fits_with_native_core_singular_value_recomputation'] for x in blocks),
        'factor_magnitudes_scope':'final balanced factors across all fits, not every intermediate sweep',
        'converged_under_original_gradient_criterion':sum(x['converged_under_original_gradient_criterion'] for x in blocks),
        'maximum_absolute_factor':max(x['maximum_absolute_factor'] for x in blocks),
        'maximum_factor_max_over_min_nonzero':max(x['maximum_factor_max_over_min_nonzero'] for x in blocks),
        'maximum_QR_observed_product_error_relative_to_target':max(x['maximum_QR_observed_product_error_relative_to_target'] for x in blocks),
        'CPU_recomputations':0,'exact_aliases_not_counted_twice':True,'maximum_minimum_ratio_is_not_a_condition_number':True}
    result['forward_ALS_diagnostics']=diag
    lines=[
        'O método principal de b/c/f é o estimador FP32 declarado pelo usuário antes de qualquer KL desses braços: SVD truncada,200 varreduras, ridge1e-6*tr(G), Grams cumulativas, Cholesky em lote e QR+SVD do núcleo. Não se trata de uma réplica do ajustador float64.',
        'O teste histórico de equivalência com a CPU, limite0,002, continua reprovado nos seis modelos e nas24 combinações modelo×K×b/c. Seu resultado, os erros matriciais float64 e FP32 e a discordância foram preservados. O usuário mudou explicitamente a declaração do método e a função do teste, sem reclassificar a reprovação como aprovação.',
        'A amostra contém os mesmos primeiros64 artigos, n128, K8/16 e dtype por modelo. a/d/e foram preservados; e foi repetido apenas para obter contagens reais de linhas vazias nas cabeças não isentas, com KL/NLL conferidos contra os valores existentes. Todos os60 contrastes planejados foram executados.',
        'Os braços a/b/c/d respeitam o teto comum K(2n+1); c registra a contagem máxima de átomos e a verificação do custo. As ablações e/f mantêm cabeças inteiras exatas e, por isso, acrescentam armazenamento nessas cabeças. Elas testam o papel dessas cabeças, sem estabelecer uma compressão global ao mesmo custo.',
        'Uma execução do Qwen0.5B falhou antes de gravar KL inválido: na varredura71, a SVD nativa retornou um valor singular infinito para um núcleo finito de norma próxima de1 e vetores finitos, com status de sucesso. A correção controlada recalcula somente valores nativos inválidos como u_i^T C v_i em GPU float32. Ela conserva os valores nativos válidos e os parâmetros do estimador; a entrada real passou em200 varreduras e as trajetórias plantadas foram idênticas. A exceção e os diagnósticos permanecem nos arquivos.',
    ]
    labels={('masked_K','named_plus_svd'):'b vs d',('named_plus_masked','named_plus_svd'):'c vs d',
        ('named_plus_masked','masked_K'):'c vs b',('masked_K_diag_exact','masked_K'):'f vs b',('svd_K_diag_exact','svd_K'):'e vs a'}
    for left,right in comparisons:
        s=summaries[left+'__minus__'+right]
        lines.append(f'{labels[left,right]}: braço da esquerda com KL significativamente menor em{s["left_significantly_lower_KL"]}/12 células; direita em{s["right_significantly_lower_KL"]}/12; sem rejeição após Holm em{s["not_significant_after_Holm"]}/12. A família é60, não uma seleção de contrastes após os resultados. Nos Pythia, f=b e e=a são aliases estruturais exatos.')
    b_vs_d=summaries['masked_K__minus__named_plus_svd'];c_vs_b=summaries['named_plus_masked__minus__masked_K']
    if b_vs_d['right_significantly_lower_KL']:
        lines.append('Há evidência comportamental a favor de S+L com SVD em parte dos cenários, frente a este ajustador causal FP32 específico. Isso não demonstra superioridade sobre a classe inteira de matrizes de posto baixo sob máscara nem sobre seu ótimo global.')
    if b_vs_d['left_significantly_lower_KL']:
        lines.append('Também há cenários em que o posto baixo causal FP32 preserva melhor a distribuição final que S+L com SVD. Uma afirmação universal de vantagem de S+L não é sustentada pelos testes deste protocolo.')
    if c_vs_b['left_significantly_lower_KL']:
        lines.append('O contraste c-b isola a alocação named_first em relação ao postoK causal, dentro do armazenamento comum: nos cenários significativos a favor de c, manter o canal nomeado ajuda no comportamento mesmo com um resíduo ajustado sob a máscara. O estudo matricial, por outro lado, favorece b nas medianas; as duas métricas não são intercambiáveis.')
    lines.append(f'No forward foram calculados{diag["n_unique_computed_fits"]} ajustes únicos: {diag["converged_under_original_gradient_criterion"]} atingiram o critério original de gradiente/convergência; maior fator absoluto {diag["maximum_absolute_factor"]:.6g}; maior razão máximo/mínimo não nulo {diag["maximum_factor_max_over_min_nonzero"]:.6g}; maior alteração numérica observada em QR/SVD {diag["maximum_QR_observed_product_error_relative_to_target"]:.6g} em unidades da norma do alvo. Não houve recomputação CPU. Estes dados delimitam a interpretação de um procedimento finito de200 varreduras, sem garantia de ótimo global.')
    lines.append(f'Foram recomputados {diag["invalid_native_core_singular_values_recomputed"]} valores singulares nativos inválidos em {diag["fits_with_native_core_singular_value_recomputation"]} ajustes. As magnitudes dos fatores referem-se aos fatores balanceados finais, agregados entre ajustes. Os resultados anteriores que terminaram finitos usaram o caminho nativo válido, preservado pelos controles de igualdade; nenhuma medida matricial anterior foi substituída.')
    lines.append('As frações de linha vazia usam contagens inteiras agregadas por lote único. Cabeças exatas contribuem para o denominador e zero para o numerador. As contagens de candidatos SVD vazios descartados em e permanecem separadas, evitando apresentá-las como preenchimentos efetivamente injetados. Linhas da última posição são reportadas separadamente, pois só ela participa de KL/NLL.')
    result['honest_reading']=lines
    result['decisions']=[
        {'decision':'Adopt the existing controlled FP32 estimator as the declared masked method, before any b/c/f KL','certainty':'alta','executed':True,'authority':'explicit user decision recorded verbatim'},
        {'decision':'Preserve the failed float64-equivalence test and both matrix estimators as reference/discordance','certainty':'alta','executed':True},
        {'decision':'Run all64 fixed articles, bothK, six models, original harness, all planned paired contrasts','certainty':'alta','executed':True},
        {'decision':'Release the GPU lock every model/chunk while keeping batch2 and200 sweeps','certainty':'alta','executed':True},
        {'decision':'Use actual empty masks from the imported harness and exclude discarded exact-head candidates in e','certainty':'alta','executed':True},
        {'decision':'Correct the demonstrated invalid native core singular value with a controlled GPU FP32 recomputation from the same core/vectors, keeping valid native values and all estimator parameters','certainty':'alta','executed':True},
        {'decision':'Generalize to the global optimum or entire class of causal rankK models','certainty':'baixa','executed':False,'reason':'Finite200-sweep heuristic, ill-conditioned completion, no global convergence guarantee'},
    ]
    return result

def finite(obj):
    if isinstance(obj,dict):return all(finite(v) for v in obj.values())
    if isinstance(obj,(list,tuple)):return all(finite(v) for v in obj)
    if isinstance(obj,float):return bool(np.isfinite(obj))
    return True

def put_new_or_equal(path,value):
    """Resume publication without changing any previously published artifact."""
    path=Path(path)
    if path.exists():
        if read(path)!=value:raise AssertionError('Existing scientific artifact differs: '+str(path))
    else:write_json_new(path,value)

def main():
    finished=Path('out/phase50_declared_finished.json')
    if finished.exists():
        done=read(finished)
        if sha256_file('out/phase50_report.json')!=done['report_sha256']:raise AssertionError('Completed report changed')
        return read('out/phase50_report.json')
    result,audit_models=assemble();result=complete_reading(result)
    old_audit=result['integrity_audit_path'];result['predecessor_integrity_audit_path']=old_audit
    audit={'passed':True,'scope':'all six arms, bothK,64 articles/model for declared FP32 method',
        'complete_scientific_E9_forward_comparison_for_declared_FP32':True,'CPU_float64_equivalence_passed':False,
        'CPU_float64_equivalence_is_behavioral_gate':False,'decision_before_first_b_c_f_KL':True,
        'n_articles_per_arm_model_K':64,'n_paired_tests':60,'Holm_family_size':60,
        'no_missing_tests':all(t['executed'] for t in result['forward_paired_tests']),
        'harness_unchanged':sha256_file('phase2_downstream.py')==result['declared_method_decision']['harness_sha256'],
        'estimator_sources_unchanged':all(sha256_file(p)==d for p,d in result['declared_method_decision']['estimator_sources'].items()),
        'estimator_sources_unchanged_scope':'Imported base source files remain byte-identical; the explicit controlled numerical wrapper is separately recorded and hashed',
        'controlled_core_SVD_fix_passed':check_implementation_fix()['control']['original_failed_input200_sweeps_finite'],
        'all_report_numbers_finite':finite(result),'empty_row_counters_control_passed':result['empty_row_counter_control']['passed'],
        'per_model':audit_models,'internal_self_audit_not_independent':True,'decision_sha256':sha256_file(DECISION)}
    audit['execution_log_committed_prefix']=result['completed_chunk_execution_timing']['execution_log_committed_prefix']
    if not all(audit[k] for k in ('no_missing_tests','harness_unchanged','estimator_sources_unchanged','all_report_numbers_finite','empty_row_counters_control_passed','controlled_core_SVD_fix_passed')):
        raise AssertionError('Declared-method report audit failed')
    audit_path=Path('out/phase50_declared_integrity_audit.json');put_new_or_equal(audit_path,audit)
    result['integrity_audit_path']=audit_path.as_posix()
    result['rendered_tables_markdown']=render(result)
    version=Path('out/phase50_declared_report.json')
    if version.exists():result['created_UTC']=read(version)['created_UTC']
    put_new_or_equal(version,result)
    # The user expressly requested completion of this report. Keep its old
    # bytes, write a new version, and update only the requested destination.
    target=Path('out/phase50_report.json')
    if sha256_file(target) not in (result['declared_method_decision']['predecessor_report_sha256'],sha256_file(version)):
        raise AssertionError('Another writer changed the requested report; preserve both versions')
    pending=Path('out/phase50_declared_report_to_publish.json')
    if sha256_file(target)!=sha256_file(version):
        if pending.exists():
            if pending.read_bytes()!=version.read_bytes():raise AssertionError('Uncommitted report differs; preserve both versions')
        else:
            with pending.open('xb') as out:out.write(version.read_bytes())
        os.replace(pending,target)
    if sha256_file(target)!=sha256_file(version):raise AssertionError('Published report differs from audited version')
    artifacts={'report':'out/phase50_report.json','report_sha256':sha256_file(target),'versioned_report':version.as_posix(),
        'predecessor_report':result['predecessor_report'],'decision':DECISION,'decision_sha256':sha256_file(DECISION),
        'scripts':{p.as_posix():sha256_file(p) for p in Path('.').glob('phase50_declared_*.py')},
        'scientific_json_files':{p.as_posix():sha256_file(p) for p in Path('out').glob('phase50_declared_*.json')
            if p.name not in ('phase50_declared_artifacts.json','phase50_declared_finished.json','phase50_declared_report_to_publish.json')},
        'scientific_pairs':{p.as_posix():sha256_file(p) for p in Path('out/pairs').glob('phase50_declared_*.jsonl')
            if p.name!='phase50_declared_events.jsonl'},
        'execution_log_committed_prefix':result['completed_chunk_execution_timing']['execution_log_committed_prefix'],
        'append_only_execution_log_excluded_from_immutable_pair_hashes':True}
    put_new_or_equal('out/phase50_declared_artifacts.json',artifacts)
    put_new_or_equal(finished,{'status':result['status'],'report_path':target.as_posix(),'report_sha256':sha256_file(target),
        'declared_FP32_comparison_complete':True,'CPU_float64_equivalence_passed':False,'n_paired_tests':60,'decision_sha256':sha256_file(DECISION)})
    print(result['rendered_tables_markdown'],flush=True);return result

if __name__=='__main__':main()

