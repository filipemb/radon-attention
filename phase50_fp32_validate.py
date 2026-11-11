"""Validate the frozen FP32 estimator on the original 32 matrices per model."""
import phase50_fp32_als as als
import argparse,time,json
from pathlib import Path
import numpy as np
import torch
from phase50_experiment import read,jsonl,metrics,normalize_cpu,Dictionary
from sampling import MODELS,slug,load_sample,sha256_file,write_json_new
import phase2_downstream as harness

def run(model):
    protocol=read('out/phase50_fp32_protocol.json');parent=read('out/phase50_protocol.json')
    ctrl=read('out/phase50_fp32_controls.json')
    if not ctrl['passed']:raise RuntimeError('Algebra/planted controls failed')
    for p,digest in ctrl['sources'].items():
        if sha256_file(p)!=digest:raise ValueError('Implementation changed after controls')
    path=Path(f'out/phase50_fp32_validation_{slug(model)}.json')
    if path.exists():return read(path)
    ref=read(f'out/phase50_GPU_CPU_reference_{slug(model)}.json')
    if sha256_file(ref['pairs_path'])!=ref['pairs_sha256']:raise ValueError('CPU reference modified')
    cached={(r['archive_index'],r['K'],r['arm']):r for r in jsonl(ref['pairs_path'])}
    array,manifest=load_sample(model,128);dictionary=Dictionary(128)
    indices=parent['datasets'][model]['GPU_validation_indices']
    support=harness.causal_support(128,128,'cuda');checks=[];timings=[];started=time.perf_counter()
    pairs=Path(f'out/pairs/phase50_fp32_validation_{slug(model)}.jsonl')
    with pairs.open('x',encoding='utf-8') as out:
        for k in (8,16):
            for arm in ('masked_K','named_plus_masked'):
                originals=[];nameds=[];targets=[];initials=[]
                for idx in indices:
                    a=array[idx].astype(np.float64);s=dictionary.project(a)[0]
                    target=a if arm=='masked_K' else a-s;row=cached[idx,k,arm]
                    initials.append((np.array(row['initial_U']),np.array(row['initial_V'])))
                    originals.append(a);nameds.append(s);targets.append(target)
                tensor=torch.from_numpy(np.stack(targets)).cuda()
                init=tuple(torch.from_numpy(np.stack([x[j] for x in initials])).cuda() for j in (0,1))
                rank=k if arm=='masked_K' else k-1
                torch.cuda.synchronize();tick=time.perf_counter()
                product,infos=als.fit(tensor,rank,support,init,backend='graph')
                torch.cuda.synchronize();seconds=time.perf_counter()-tick
                # Repeat only for performance, no extra optimizer sweeps: starts
                # at the same truncated SVD, then checks deterministic output.
                tick=time.perf_counter();again,_=als.fit(tensor,rank,support,init,backend='graph')
                torch.cuda.synchronize();steady=time.perf_counter()-tick
                if not torch.equal(product,again):raise AssertionError('FP32 repeated fit not deterministic')
                timings.append({'K':k,'arm':arm,'rank':rank,'n_matrices':32,'cold_seconds':seconds,'steady_seconds':steady})
                products=product.cpu().numpy().astype(np.float64)
                for j,idx in enumerate(indices):
                    cpu=cached[idx,k,arm];a=originals[j];reference=normalize_cpu(a,a)[0]
                    add=nameds[j] if arm=='named_plus_masked' else 0
                    gpu=metrics(products[j]+add,a,reference)
                    diff=abs(cpu['CPU']['raw_causal_frobenius']-gpu['raw_causal_frobenius'])
                    nr=abs(cpu['CPU']['frobenius']-gpu['frobenius']);tv=abs(cpu['CPU']['TV']-gpu['TV'])
                    row={'model':model,'archive_index':idx,'instance_id':manifest['instances'][idx]['instance_id'],
                        'document_index':manifest['instances'][idx]['document_index'],'layer':manifest['instances'][idx]['layer'],
                        'head':manifest['instances'][idx]['head'],'K':k,'arm':arm,'CPU':cpu['CPU'],'GPU':gpu,
                        'absolute_relative_error_difference':diff,'normalized_frobenius_difference':nr,'TV_difference':tv,
                        'CPU_ALS':cpu['CPU_ALS'],'GPU_ALS':infos[j],
                        'passed':diff<=.002,'protocol_sha256':sha256_file('out/phase50_fp32_protocol.json')}
                    out.write(json.dumps(row,separators=(',',':'),allow_nan=False)+'\n');out.flush();checks.append(row)
                print(f'FP32 VALIDATE {model} K{k} {arm} cold={seconds:.3f}s steady={steady:.3f}s maxdiff={max(x["absolute_relative_error_difference"] for x in checks):.8g}',flush=True)
    worst=max(checks,key=lambda x:x['absolute_relative_error_difference'])
    result={'model':model,'protocol_sha256':sha256_file('out/phase50_fp32_protocol.json'),
        'n_unique_matrices':32,'n_fits':128,'same_indices_as_original_GPU_validation':indices,
        'same_initial_factors_rounded_to_float32':True,'GPU_dtype':'float32','CPU_reference_dtype':'float64',
        'CPU_recomputations':0,'ridge_relative_to_trace':als.RIDGE,'sweeps':als.SWEEPS,
        'max_absolute_relative_error_difference':worst['absolute_relative_error_difference'],
        'max_normalized_frobenius_difference':max(x['normalized_frobenius_difference'] for x in checks),
        'max_TV_difference':max(x['TV_difference'] for x in checks),
        'threshold_fixed_before_results':.002,'passed':all(x['passed'] for x in checks),
        'n_failed_fits':sum(not x['passed'] for x in checks),
        'worst':worst,'timings':timings,'elapsed_seconds':time.perf_counter()-started,
        'pairs_path':pairs.as_posix(),'pairs_sha256':sha256_file(pairs),'sources':ctrl['sources'],
        'CPU_reference_metadata':f'out/phase50_GPU_CPU_reference_{slug(model)}.json',
        'failure_interpretation':None if all(x['passed'] for x in checks) else
            'Uniform trace-relative ridge changes the unregularized finite-200-sweep estimator; FP32 normal equations lose small singular directions (conditioning squared). Worst CPU diagnostics and all raw per-fit errors retained. No threshold relaxation or CPU fallback.'}
    write_json_new(path,result)
    print('FP32 MODEL',model,'PASSED',result['passed'],'maxError',result['max_absolute_relative_error_difference'],'maxTV',result['max_TV_difference'],flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',choices=MODELS,required=True);p.add_argument('--under-gpu-lock',action='store_true');a=p.parse_args()
    if not a.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
    run(a.model)
    bundle=Path('out/phase50_fp32_schedule_bundle.json')
    if bundle.exists() and a.model in read(bundle)['models']:
        # Same model, same outer flock. Only timing (no candidate KL) is
        # bundled, then the coordinator releases the lock for another model.
        from phase50_fp32_forward import timing
        timing(a.model)
