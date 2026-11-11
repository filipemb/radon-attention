"""Audit complete forward artifacts against raw pairs, source and row budgets."""
import phase21_allocation_v2 as e4
from phase24_p0_metrics import describe
from sampling import MODELS,CORPUS_PATH,sha256_file,write_json_new
from scipy.stats import rankdata,wilcoxon
from pathlib import Path
import json
import numpy as np


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    x=read('out/phase21_allocation_v2_forward.json');run=x['_meta']
    if x['status']!='complete' or set(x['models'])!=set(MODELS):raise ValueError('All six completed models required')
    if sha256_file('out/phase21_allocation_v2.json')!=run['protected_matrix_aggregate_sha256']:
        raise ValueError('Historical matrix aggregate changed')
    if sha256_file(CORPUS_PATH)!=run['corpus_manifest_sha256']:raise ValueError('Corpus changed')
    if sha256_file('out/phase2_downstream_v2.json')!=run['source_V1_sha256']:raise ValueError('V1 changed')
    if sha256_file('phase2_downstream.py')!=run['imported_harness_sha256']:raise ValueError('Harness changed')
    corpus=read(CORPUS_PATH);baseline=read('out/phase2_downstream_v2.json')
    checks=[];n_pairs=0;max_native_difference=0.
    for model in MODELS:
        d=x['models'][model]['128'];source=baseline[model]
        if sha256_file(source['pairs_path'])!=run['source_pairs_sha256'][model]:raise ValueError('V1 raw pairs changed')
        if sha256_file(d['pairs_path'])!=d['pairs_sha256']:raise ValueError('E4 raw pairs changed')
        if not d['identity_exact_in_every_batch'] or not all(v['passed_exact'] for v in d['suffix_invariance'].values()):
            raise ValueError('Native identity or suffix invariance failed')
        with Path(d['pairs_path']).open(encoding='utf-8') as inp:rows=[json.loads(line) for line in inp]
        if len(rows)!=512:raise ValueError('Wrong model sample size')
        for K in (8,16):
            part=sorted((r for r in rows if r['budget_rank_K']==K),key=lambda r:r['document_index'])
            if [r['document_index'] for r in part]!=list(range(256)):raise ValueError('Missing/duplicated article')
            n_pairs+=256;B=K*257
            for i,row in enumerate(part):
                window=corpus['models'][model]['documents'][i]
                if (row['doc_id']!=corpus['documents'][i]['doc_id'] or row['target_id']!=window['token_ids'][128]
                        or row['offset']!=window['offset'] or row['n']!=128 or row['residual_rank']!=K-1):
                    raise ValueError('Wrong article, prefix, target, offset or residual rank')
                if not row['identity_exact'] or row['empty_row_policy']!='uniform':raise ValueError('Invalid row provenance')
                cost=row['budget_accounting'];H=cost['head_layer_fits']
                if cost['residual_rank_counts']!={str(K-1):H}:raise ValueError('Residual rank differs within an article')
                active=cost['active_atom_counts']
                if sum(active.values())!=H:raise ValueError('Active-atom counts do not cover every head/layer')
                expected=2*sum(int(k)*v for k,v in active.items())+(K-1)*257*H
                if (cost['actual_parameters_total']!=expected or cost['common_cap_total']!=B*H
                        or expected>B*H or cost['unused_parameters_total']!=B*H-expected):
                    raise ArithmeticError('Symmetric storage cap/slack is wrong')
                max_native_difference=max(max_native_difference,row['reference_NLL_difference_from_V1'])
                if row['reference_NLL_difference_from_V1']>2e-5:raise ArithmeticError('Native NLL parity failed')
            b=d['budgets'][str(K)];a=np.array([r['named_KL'] for r in part]);s=np.array([r['svd_KL'] for r in part]);delta=a-s
            if not np.isfinite(np.r_[a,s,delta]).all():raise ValueError('Nonfinite KL')
            for values,key in ((a,'named_first_KL'),(s,'SVD_KL'),(delta,'paired_KL_named_minus_SVD')):
                expected=describe(values,np.arange(256),seed=0);actual=b[key]
                for field,value in expected.items():
                    if actual[field]!=value:raise ArithmeticError(f'Imported describe differs: {model}/{K}/{field}')
            observed=b['paired_KL_named_minus_SVD']['wilcoxon'];nz=delta[delta!=0]
            if len(nz):
                rr=rankdata(np.abs(nz),method='average');effect=float(np.sum(np.sign(nz)*rr)/rr.sum())
                test=wilcoxon(delta,alternative='two-sided',zero_method='wilcox',method='asymptotic')
                p=float(test.pvalue);W=float(test.statistic)
            else:effect=0.;p=1.;W=0.
            if (observed['n_articles']!=256 or observed['rank_biserial']!=effect
                    or observed['p_two_sided']!=p or observed['statistic']!=W):
                raise ArithmeticError('Article signed-rank inference differs from raw pairs')
            for mode in ('named','svd'):
                seen={}
                for row in part:
                    key=(row['batch_start'],row['batch_size']);v=row[mode+'_validation_batch']
                    counts=tuple(v[k] for k in ('reconstruction_rows_total','empty_rows_completed','last_query_rows_total','empty_rows_completed_at_last_query'))
                    if key in seen and seen[key]!=counts:raise ValueError('Duplicated batch counters differ')
                    seen[key]=counts
                totals=np.array(list(seen.values()),dtype=np.int64).sum(axis=0)
                c=b['uniform_causal_completion_by_mode'][mode]
                if tuple(totals)!=(c['rows_total'],c['rows_completed'],c['last_query_rows_total'],c['last_query_rows_completed']):
                    raise ArithmeticError('Row completion counters were duplicated/lost')
                if (c['fraction_rows_completed']!=c['rows_completed']/c['rows_total']
                        or c['fraction_last_query_rows_completed']!=c['last_query_rows_completed']/c['last_query_rows_total']
                        or c['rows_total']!=128*c['last_query_rows_total']):
                    raise ArithmeticError('Row completion fraction/denominator wrong')
            checks.append({'model':model,'K':K,'n_articles':256,'all_checks_passed':True})
    if n_pairs!=3072:raise ValueError('Global paired cohort incomplete')
    result={'passed':True,'n_model_K_combinations':12,'n_paired_articles':n_pairs,'checks':checks,
            'max_native_reference_NLL_difference_from_V1':max_native_difference,
            'matrix_aggregate_unchanged':True,'source_V1_and_pairs_unchanged':True,
            'describe_recomputed_on_every_arm_and_paired_difference':True,
            'row_counters_recomputed_from_unique_batches':True,'per_head_layer_storage_formula_checked_per_article':True,
            'forward_aggregate_sha256':sha256_file('out/phase21_allocation_v2_forward.json')}
    write_json_new('out/phase21_allocation_v2_forward_audit.json',result)
    print('FORWARD AUDIT PASSED',12,n_pairs,'native NLL max delta',max_native_difference,flush=True)


if __name__=='__main__':main()
