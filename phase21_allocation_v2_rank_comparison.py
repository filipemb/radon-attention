"""Secondary rank comparisons, explicitly separate from the common-cap test.

Preserve the original positive-r allocation sweep: compare S+L_r against SVD_r
and SVD_(r+m), m=active named atoms. Also include named_first q7 from the K8
panel. These comparisons have different storage costs; never label them as the
primary symmetric-budget result. No SVD rank zero comparison.
"""
import phase21_allocation_v2 as e4
import json
from pathlib import Path
import time
import numpy as np
from sampling import MODELS,slug,sha256_file


def observation(row,rank,metrics,coefficients):
    active=int(np.count_nonzero(np.asarray(coefficients)>0))
    n=row['n'];s=np.asarray(row['attention_singular_values']);norm=row['attention_frobenius_norm']
    plus=min(n,rank+active)
    error=metrics['relative_error']
    e_same=float(np.linalg.norm(s[rank:])/norm)
    e_plus=float(np.linalg.norm(s[plus:])/norm)
    cost=2*active+rank*(2*n+1)
    return {'residual_rank':rank,'n_active':active,'method_error':error,'svd_same_r_error':e_same,
            'svd_r_plus_atoms_error':e_plus,'svd_r_plus_atoms_rank':plus,
            'method_parameters':cost,'svd_same_r_parameters':rank*(2*n+1),'svd_r_plus_atoms_parameters':plus*(2*n+1),
            'difference_method_minus_same_r_SVD':error-e_same,'difference_method_minus_r_plus_atoms_SVD':error-e_plus}


def run(model,n):
    target=Path('out')/f'phase21_allocation_v2_rank_comparison_{slug(model)}_n{n}.json'
    pairs=Path('out/pairs')/f'phase21_allocation_rank_comparison_{slug(model)}_n{n}_v2.jsonl'
    if target.exists():
        result=json.loads(target.read_text(encoding='utf-8'))
        if result['pairs_sha256']!=sha256_file(pairs):raise ValueError('Rank comparison pairs changed')
        return result
    corepath,corepairs=e4.core_paths(model,n)
    core=json.loads(corepath.read_text(encoding='utf-8'))
    if core['pairs_sha256']!=sha256_file(corepairs):raise ValueError('Core ledger changed')
    rows=[];start=time.perf_counter()
    e4.log(f'SECONDARY RANK COMPARISON START {model} n={n}; positive ranks only, storage differences explicit')
    with corepairs.open(encoding='utf-8') as inp,pairs.open('x',encoding='utf-8') as out:
        for line in inp:
            source=json.loads(line)
            row={key:source[key] for key in ('instance_id','model','n','document_index','doc_id','layer','head')}
            row['allocation_positive_ranks']={}
            for method,by_rank in source['allocation'].items():
                row['allocation_positive_ranks'][method]={str(rank):observation(source,rank,by_rank[str(rank)]['metrics'],by_rank[str(rank)]['coefficients'])
                                                         for rank in e4.RANKS if rank>0}
            cap=source['capacity']['8']
            row['named_first_common_K8_q7']=observation(source,7,{'relative_error':cap['named_first_error']},source['named_first_coefficients'])
            out.write(json.dumps(row,allow_nan=False,separators=(',',':'))+'\n');rows.append(row)
    if len(rows)!=core['n_instances']:raise ValueError('Incomplete secondary comparison population')
    docs=[r['document_index'] for r in rows]
    def summarize(obs):
        keys=('method_error','svd_same_r_error','svd_r_plus_atoms_error','svd_r_plus_atoms_rank',
              'method_parameters','svd_same_r_parameters','svd_r_plus_atoms_parameters','n_active')
        return {'metrics':{key:e4.summarize([v[key] for v in obs],docs) for key in keys},
                'paired_method_minus_same_r_SVD':e4.paired([v['difference_method_minus_same_r_SVD'] for v in obs],rows),
                'paired_method_minus_r_plus_atoms_SVD':e4.paired([v['difference_method_minus_r_plus_atoms_SVD'] for v in obs],rows)}
    result={'schema_version':2,'model':model,'n':n,'n_instances':len(rows),'n_documents':64,
            'secondary_only':True,'same_parameter_budget_claimed':False,
            'interpretation':'Rank comparisons requested separately: S+L_r versus SVD_r and SVD_(r+active_named_atoms). Storage of all arms reported; primary symmetric-cap result is elsewhere.',
            'no_rank_zero_comparison':True,
            'allocation_positive_ranks':{method:{str(rank):summarize([r['allocation_positive_ranks'][method][str(rank)] for r in rows])
                                                for rank in e4.RANKS if rank>0} for method in e4.CONVENTIONS},
            'named_first_common_K8_q7':summarize([r['named_first_common_K8_q7'] for r in rows]),
            'source_core_sha256':sha256_file(corepath),'pairs_path':pairs.as_posix(),'pairs_sha256':sha256_file(pairs),
            'elapsed_seconds':time.perf_counter()-start}
    e4.write_new(target,result)
    e4.log(f'SECONDARY RANK COMPARISON DONE {model} n={n}; {len(rows)} instances; seconds={result["elapsed_seconds"]:.1f}')
    return result


if __name__=='__main__':
    for n in (128,256):
        for model in MODELS:run(model,n)
