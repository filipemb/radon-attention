"""Independent algebraic and population audit of the versioned E4 raw ledgers.

Use cone projection identities, nesting of the two literal dictionaries, and
the explicit storage formula as certificates; no re-fitting or missing-value
replacement. Preserve every earlier control/output.
"""
import json
import math
from pathlib import Path
import hashlib
from collections import Counter


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as inp:
        while chunk:=inp.read(1<<20):h.update(chunk)
    return h.hexdigest()


def finite(value):
    if isinstance(value,float) and not math.isfinite(value):raise ValueError('Nonfinite raw number')
    if isinstance(value,dict):
        if 'named_only_error_same_budget' in value:raise ValueError('Old misnamed alias remains')
        for v in value.values():finite(v)
    elif isinstance(value,list):
        for v in value:finite(v)


def audit():
    destination=Path('out/phase21_allocation_v2_integrity_checks.json')
    if destination.exists():raise FileExistsError(destination)
    records=[];legacy_met=legacy_n=0
    maximum={'projection_energy_identity':0.,'named_norm_squared_identity':0.,'full_lines_above_named_only_error':0.,'full_lines_KKT':0.}
    candidates=sorted(Path('out').glob('phase21_allocation_v2_endpoint_preview_*_n*.json'))
    if len(candidates)!=12:raise ValueError('Expected all twelve populations')
    for path in candidates:
        summary=json.loads(path.read_text(encoding='utf-8'))
        corepath=Path(summary['source_core_path'])
        if sha(corepath)!=summary['source_core_sha256']:raise ValueError('Core summary hash mismatch')
        core=json.loads(corepath.read_text(encoding='utf-8'))
        pairs=Path(summary['pairs_path'])
        if sha(pairs)!=summary['pairs_sha256']:raise ValueError('Candidate pairs changed')
        docs=Counter();identities=set();N=summary['n'];count=0
        if summary['dictionary']['n_atoms']!=17:raise ValueError('Named dictionary changed')
        with pairs.open(encoding='utf-8') as inp:
            for line in inp:
                row=json.loads(line);finite(row);count+=1
                if row['instance_id'] in identities:raise ValueError('Duplicate instance')
                identities.add(row['instance_id']);docs[row['document_index']]+=1
                if row['n']!=N or row['model']!=summary['model']:raise ValueError('Wrong population')
                if '0' in row['capacity']:raise ValueError('Degenerate SVD0 comparison')
                reference=row['allocation']['named_first']['0']['metrics']
                for convention,rank_values in row['allocation'].items():
                    if set(rank_values)!={'0','1','2','4','8','16'}:raise ValueError('Allocation rank missing')
                    for r,item in rank_values.items():
                        m=item['metrics']
                        discrepancy=abs(m['named_norm_ratio']**2-m['named_energy_ratio'])
                        maximum['named_norm_squared_identity']=max(maximum['named_norm_squared_identity'],discrepancy)
                        if discrepancy>1e-12:raise ArithmeticError('Squared norm is not the reported energy')
                        if abs(m['named_channel_only_error']**2-(1-m['named_only_explained_energy']))>1e-11:
                            raise ArithmeticError('Named-only error refers to a different S')
                        active=sum(c>0 for c in item['coefficients'])
                        if m['named_channel_parameters']!=2*active:raise ArithmeticError('Wrong named-only cost')
                        if convention=='named_first':
                            discrepancy=abs(m['named_energy_ratio']-m['named_only_explained_energy'])
                            maximum['projection_energy_identity']=max(maximum['projection_energy_identity'],discrepancy)
                            if discrepancy>1e-11:raise ArithmeticError('Cone projection energy identity failed')
                            if item['coefficients']!=row['named_first_coefficients']:raise ValueError('S changed across named-first ranks')
                        if convention=='algorithm_1_5_iterations':
                            d=item['algorithm_1_diagnostics'];trace=d['relative_squared_error_by_iteration']
                            if d['iterations_run']!=5 or d['stop_reason']!='fixed_T' or len(trace)!=5:
                                raise ValueError('Wrong Algorithm1 iteration convention')
                            if any(b>a+2e-9 for a,b in zip(trace,trace[1:])):raise ArithmeticError('Algorithm1 objective increased')
                            if N==128 and r=='8':legacy_met+=int(d['diagnostic_tolerance_met']);legacy_n+=1
                endpoint=row['lines']['complete_dictionary_endpoint']
                kkt=endpoint['nnls_kkt_relative_violation'];maximum['full_lines_KKT']=max(maximum['full_lines_KKT'],kkt)
                if kkt>1e-8:raise ArithmeticError('Line endpoint KKT failed')
                diff=endpoint['error']-reference['named_channel_only_error']
                maximum['full_lines_above_named_only_error']=max(maximum['full_lines_above_named_only_error'],diff)
                if diff>1e-10:raise ArithmeticError('Full line cone, which contains the named cone, has a larger projection error')
                for K,cap in row['capacity'].items():
                    K=int(K);B=K*(2*N+1);active=sum(c>0 for c in row['named_first_coefficients'])
                    if cap['residual_rank']!=K-1 or cap['common_cap']!=B:raise ValueError('Wrong common cap')
                    cost=2*active+(K-1)*(2*N+1)
                    if cap['named_first_parameters']!=cost or cost>B or cap['named_first_unused_parameters']!=B-cost:
                        raise ArithmeticError('Symmetric cap or slack wrong')
                    k=min(B//2,2*N+7)
                    if cap['line_selected_atoms']!=k or cap['line_parameters']!=2*k or cap['line_unused_parameters']!=B-2*k:
                        raise ArithmeticError('Line cap or slack wrong')
                    if cap['line_error']!=endpoint['error'] or k!=2*N+7:raise ArithmeticError('Invalid full endpoint substitution')
        if count!=summary['n_instances'] or len(docs)!=64 or len(set(docs.values()))!=1:
            raise ValueError('Missing/unbalanced population')
        for K,cap in summary['capacity'].items():
            for name,p in cap['comparisons'].items():
                if p['wilcoxon']['n_documents']!=64 or len(p['document_median_differences'])!=64:
                    raise ValueError('Paired test did not use 64 documents')
                s=p['paired_instance_difference']
                if s['n_instances']!=count or s['n_documents']!=64 or s['n_bootstrap']!=2000:
                    raise ValueError('Wrong paired bootstrap population')
        records.append({'model':summary['model'],'n':N,'n_instances':count,'n_documents':64,
                        'balanced_instances_per_document':next(iter(docs.values())),
                        'candidate_pairs_path':pairs.as_posix(),'candidate_pairs_sha256':summary['pairs_sha256'],
                        'core_positive_capacity_budgets':list(core['capacity_without_lines']),
                        'line_candidate_capacity_budgets':list(summary['capacity'])})
        print('AUDITED',summary['model'],N,count,flush=True)
    if sum(r['n_instances'] for r in records)!=19968 or (legacy_met,legacy_n)!=(17,9984):
        raise ValueError('Global coverage/legacy criterion changed')
    result={'passed':True,'scope':'Independent population, algebraic and budget certificates on every candidate raw record; line protocol choice remains pending',
            'n_instances':19968,'records':records,'maximum_discrepancies':maximum,
            'algorithm_1_n128_residual_r8_criterion_met':legacy_met,'algorithm_1_n128_residual_r8_n_instances':legacy_n,
            'source_primary_statistics_sha256':sha('phase24_p0_metrics.py'),
            'unmodified_OMP_sha256':sha('phase06_profiled_lines.py')}
    with destination.open('x',encoding='utf-8') as out:json.dump(result,out,ensure_ascii=False,allow_nan=False,indent=2)
    print('PASSED',destination,flush=True)


if __name__=='__main__':audit()
