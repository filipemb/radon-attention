"""The same frozen384 matrices with the new FP32 estimator, before its forward."""
import phase50_fp32_als as als
import time,json
from pathlib import Path
import numpy as np
import torch
from phase50_experiment import read,jsonl,Dictionary,normalize_cpu,metrics,describe,paired,holm,MATRIX_COMPARISONS
from sampling import MODELS,slug,load_sample,sha256_file,write_json_new
import phase2_downstream as harness

def run(model):
    path=Path(f'out/phase50_fp32_matrix_{slug(model)}.json')
    if path.exists():return read(path)
    started=time.perf_counter();protocol=read('out/phase50_protocol.json');cfg=protocol['datasets'][model]
    base=read(f'out/phase50_matrix_{slug(model)}.json')
    if sha256_file(base['pairs_path'])!=base['pairs_sha256']:raise ValueError('Reference matrix results changed')
    cached={(r['archive_index'],r['K']):r for r in jsonl(base['pairs_path'])}
    array,manifest=load_sample(model,128);dictionary=Dictionary(128)
    indices=cfg['matrix_archive_indices'];support=harness.causal_support(128,128,'cuda');rows={}
    for k in (8,16):
        for idx in indices:
            old=cached[idx,k];rows[idx,k]={key:old[key] for key in ('instance_id','document_index','doc_id','layer','head','offset','n','model','archive_index','K','cap','masked_parameters','named_masked_parameters','active_atoms')}
            rows[idx,k].update(protocol_sha256=sha256_file('out/phase50_fp32_protocol.json'),arms={a:old['arms'][a] for a in ('svd_K','named_plus_svd')},
                a_d_reused_unchanged=True)
    for start in range(0,len(indices),32):
        ids=indices[start:start+32];originals=[array[i].astype(np.float64) for i in ids]
        nameds=[dictionary.project(a)[0] for a in originals]
        references=[normalize_cpu(a,a)[0] for a in originals]
        for k in (8,16):
            for arm in ('masked_K','named_plus_masked'):
                targets=originals if arm=='masked_K' else [a-s for a,s in zip(originals,nameds)]
                tensor=torch.from_numpy(np.stack(targets)).cuda()
                product,infos=als.fit(tensor,k if arm=='masked_K' else k-1,support,backend='graph')
                products=product.cpu().numpy().astype(np.float64)
                for j,idx in enumerate(ids):
                    add=nameds[j] if arm=='named_plus_masked' else 0
                    rows[idx,k]['arms'][arm]={**metrics(products[j]+add,originals[j],references[j]),'ALS':infos[j]}
        print(f'MATRIX FP32 {model} {start+len(ids)}/384 elapsed={time.perf_counter()-started:.1f}s',flush=True)
    pairs=Path(f'out/pairs/phase50_fp32_matrix_{slug(model)}.jsonl')
    ordered=[rows[idx,k] for k in (8,16) for idx in indices]
    with pairs.open('x',encoding='utf-8') as out:
        for row in ordered:out.write(json.dumps(row,separators=(',',':'),allow_nan=False)+'\n')
    result={'model':model,'n_matrices':384,'n_documents':64,'n':128,'protocol_sha256':sha256_file('out/phase50_fp32_protocol.json'),
        'estimator':'GPU FP32 cumulative-Gram ALS, trace-relative ridge1e-6,200 sweeps',
        'CPU_reference_equivalence_passed':read(f'out/phase50_fp32_validation_{slug(model)}.json')['passed'],
        'pairs_path':pairs.as_posix(),'pairs_sha256':sha256_file(pairs),'K':{},'elapsed_seconds':time.perf_counter()-started}
    for k in (8,16):
        group=[r for r in ordered if r['K']==k];docs=[r['document_index'] for r in group];rr={'arms':{},'paired':{}}
        for arm in ('svd_K','masked_K','named_plus_masked','named_plus_svd'):
            rr['arms'][arm]={metric:describe([r['arms'][arm][metric] for r in group],docs) for metric in ('frobenius','TV')}
            if arm in ('masked_K','named_plus_masked'):
                from phase50_fp32_forward import diagnostics
                rr['arms'][arm]['ALS']=diagnostics([r['arms'][arm]['ALS'] for r in group])
        for left,right in MATRIX_COMPARISONS:
            rr['paired'][left+'__minus__'+right]={metric:paired([r['arms'][left][metric]-r['arms'][right][metric] for r in group],docs) for metric in ('frobenius','TV')}
        result['K'][str(k)]=rr
    write_json_new(path,result);return result

def aggregate():
    results={m:read(f'out/phase50_fp32_matrix_{slug(m)}.json') for m in MODELS};tests=[]
    for res in results.values():
        for cell in res['K'].values():
            for comp in cell['paired'].values():tests.extend(comp.values())
    if len(tests)!=144:raise AssertionError('Matrix Holm family144 incomplete')
    holm(tests);result={'models':results,'Holm_family_size':144,'n_matrices_per_model':384,'n_documents_per_model':64,
        'protocol_sha256':sha256_file('out/phase50_fp32_protocol.json'),'estimator_is_regularized_FP32_not_CPU_reference':True}
    write_json_new('out/phase50_fp32_matrix_summary.json',result);return result
