"""E9 FP32 timing and last-token injection through the original V1 harness."""
import phase50_fp32_als as als
import argparse,gc,json,time
from functools import partial
from pathlib import Path
import numpy as np
import torch
from transformers import AutoModelForCausalLM,AttentionInterface
import phase2_downstream as harness
from phase21_allocation_v2_forward import SymmetricNamedFirst
from phase50_forward import MaskedAdapter,source_records,attention
from phase50_experiment import read,jsonl,Dictionary
from sampling import MODELS,slug,sha256_file,write_json_new

PROTOCOL='out/phase50_fp32_protocol.json'

def diagnostics(infos):
    if not infos:return None
    return {'n_fits':len(infos),'converged':sum(x['converged'] for x in infos),
        'sweeps_per_fit':200,'CPU_recomputations':0,'ridge_relative_to_trace':als.RIDGE,
        'maximum_absolute_factor':max(x['maximum_absolute_factor'] for x in infos),
        'maximum_dynamic_range':max(x['factor_dynamic_range'] for x in infos),
        'maximum_QR_observed_product_error':max(x['maximum_QR_observed_product_error'] for x in infos),
        'objective_increase_sweeps':sum(x['objective_increase_sweeps'] for x in infos),
        'median_initial_relative':float(np.median([x['initial_relative'] for x in infos])),
        'median_final_relative':float(np.median([x['final_relative'] for x in infos])),
        'median_history':[{'sweep':s,'relative':float(np.median([next(h['relative'] for h in x['history'] if h['sweep']==s) for x in infos]))} for s in als.CHECKPOINTS]}

class Adapter(MaskedAdapter):
    @torch.inference_mode()
    def reconstruct(self,weights,module):
        if self.arm=='svd_K_diag_exact':return super().reconstruct(weights,module)
        b,h,q,n=weights.shape
        if (q,n)!=(128,128):raise ValueError('Frozen square128 prefill required')
        self.calls+=1;layer=getattr(module,'layer_idx',None)
        if layer is None:layer=getattr(module,'layer_index',None)
        if layer is None:raise ValueError('Layer index unavailable')
        layer=int(layer)
        heads=[hh for hh in range(h) if not(self.arm=='masked_K_diag_exact' and (layer,hh) in self.diag_heads)]
        if not heads:
            harness.record_reconstruction_rows(weights,self.stats);harness.validate_attention(weights,self.stats);return weights
        original=weights[:,heads].reshape(b*len(heads),q,n);w=original.float()
        named=self.project_named(w) if self.arm=='named_plus_masked' else 0
        target=w-named;rank=self.k-1 if self.arm=='named_plus_masked' else self.k
        product,infos=als.fit(target,rank,harness.causal_support(q,n,w.device),backend='graph')
        if self.document_infos is None:self.document_infos=[[] for _ in range(b)]
        for bi in range(b):self.document_infos[bi].extend(infos[bi*len(heads):(bi+1)*len(heads)])
        rec=harness.normalize_reconstruction(product+named,original,self.stats,'uniform').reshape(b,len(heads),q,n)
        result=weights.clone();result[:,heads]=rec
        if len(heads)<h:
            excluded=[hh for hh in range(h) if hh not in heads]
            harness.record_reconstruction_rows(weights[:,excluded],self.stats)
        harness.validate_attention(result,self.stats);return result

def load(name):
    old=read('out/phase50_protocol.json');cfg=old['datasets'][name]
    if sha256_file('phase2_downstream.py')!=old['harness_sha256_at_freeze']:raise ValueError('Harness changed')
    ctrl=read('out/phase50_fp32_controls.json')
    if not ctrl['passed']:raise ValueError('FP32 components not qualified')
    for p,digest in ctrl['sources'].items():
        if sha256_file(p)!=digest:raise ValueError('FP32 source changed after qualification')
    a,d,source,corpus=source_records(name)
    dtype={'torch.float32':torch.float32,'torch.bfloat16':torch.bfloat16}[cfg['dtype']]
    tick=time.perf_counter()
    model=AutoModelForCausalLM.from_pretrained(name,revision=corpus['models'][name]['revision'],local_files_only=True,
        dtype=dtype,attn_implementation='eager').to('cuda').eval()
    torch.manual_seed(0);harness.RECON.update(empty_row_policy='uniform',svd_driver=None,parallel_svd=False)
    dictionary=Dictionary(128)
    expected=read(f'out/phase21_allocation_v2_core_{slug(name)}_n128.json')['dictionary']['sha256_float64_C_order']
    if dictionary.digest!=expected:raise ValueError('E4 named dictionary changed')
    adapter=Adapter(dictionary,cfg['diagonal_heads']);named=SymmetricNamedFirst(dictionary,harness,'uniform')
    AttentionInterface.register('p0_recon',harness.attention_forward)
    AttentionInterface.register('phase50_fp32',partial(attention,adapter))
    AttentionInterface.register('phase50_fp32_named_svd',partial(harness.attention_forward,reconstruct_fn=named))
    windows=torch.tensor([x['token_ids'] for x in corpus['models'][name]['documents']],dtype=torch.long)
    seq=windows[:2];targets=seq[:,128]
    model.set_attn_implementation('eager');reference=harness.last_logits(model,seq,128)
    harness.activate(model,('phase2','identity',None),deferred=True)
    ident=harness.last_logits(model,seq,128);harness.RECON['stats'].finalize('FP32 native identity')
    kl,_=harness.kl_nll(reference,ident,targets)
    if not torch.equal(reference,ident) or np.any(kl!=0):raise AssertionError('Identity KL/logits failed')
    checks=[]
    for k in (8,16):
        harness.activate(model,('phase2','svd',k),deferred=True)
        logits=harness.last_logits(model,seq,128);harness.RECON['stats'].finalize('FP32 source SVD equality')
        ak,an=harness.kl_nll(reference,logits,targets)
        named.rank_cap=k;named.reset();model.set_attn_implementation('phase50_fp32_named_svd')
        logits=harness.last_logits(model,seq,128);dk,dn=harness.kl_nll(reference,logits,targets)
        errors={'a_KL':max(abs(float(ak[i])-a[k,i]['kl']) for i in range(2)),
            'a_NLL':max(abs(float(an[i])-a[k,i]['nll']) for i in range(2)),
            'd_KL':max(abs(float(dk[i])-d[k,i]['named_KL']) for i in range(2)),
            'd_NLL':max(abs(float(dn[i])-d[k,i]['named_NLL']) for i in range(2))}
        if max(errors.values())>2e-5:raise AssertionError(f'a/d source disagreement {errors}')
        checks.append({'K':k,'max_absolute_differences':errors})
    proof={'model':name,'protocol_sha256':sha256_file(PROTOCOL),'identity_KL_exactly_zero':True,
        'source_V1_E4_all256_records_equal':True,'native_checks':checks,'harness_sha256':sha256_file('phase2_downstream.py')}
    proofpath=Path(f'out/phase50_fp32_forward_sanity_{slug(name)}.json')
    if proofpath.exists():
        if proof!=read(proofpath):raise ValueError('Native proof changed')
    else:write_json_new(proofpath,proof)
    return model,adapter,windows,corpus,cfg,a,time.perf_counter()-tick

def modes(cfg,qualified=True):
    if not qualified:return ['svd_K_diag_exact'] if cfg['diagonal_heads'] else []
    return ['masked_K','named_plus_masked']+(['svd_K_diag_exact','masked_K_diag_exact'] if cfg['diagonal_heads'] else [])

def check_calls(adapter,corpus,name,batch):
    layers=corpus['models'][name]['n_layers'];heads=corpus['models'][name]['n_heads']
    if adapter.calls!=layers or adapter.stats.get('reconstruction_rows_total')!=batch*heads*128*layers:
        raise AssertionError('Injection did not visit every declared head/layer/row')

def timing(name):
    path=Path(f'out/phase50_fp32_timing_{slug(name)}.json')
    if path.exists():return read(path)
    from phase50_fp32_matrix import run as matrix_run
    matrix_run(name)
    model,adapter,windows,corpus,cfg,a,overhead=load(name);sequence=windows[:2]
    times=[]
    # No KL is evaluated for these candidate arms; selection depends only on
    # runtime, using the exact same two articles twice from the same SVD start.
    for repeat in (0,1):
        for k in (8,16):
            for arm in modes(cfg,True):
                adapter.arm=arm;adapter.k=k;adapter.reset();model.set_attn_implementation('phase50_fp32')
                torch.cuda.synchronize();tick=time.perf_counter();logits=harness.last_logits(model,sequence,128)
                adapter.stats.finalize('FP32 timing');torch.cuda.synchronize();seconds=time.perf_counter()-tick
                if not bool(torch.isfinite(logits).all()):raise FloatingPointError('Nonfinite timing logits')
                check_calls(adapter,corpus,name,2)
                times.append({'repeat':repeat,'K':k,'arm':arm,'seconds':seconds,'n_articles':2,
                    'ALS':diagnostics([x for block in (adapter.document_infos or []) for x in block])})
                print(f'TIMING {name} repeat{repeat} K{k} {arm}: {seconds:.3f}s (2 articles; KL not evaluated)',flush=True)
    # Native reference/identity passes are included in per-batch service time.
    tick=time.perf_counter();model.set_attn_implementation('eager');harness.last_logits(model,sequence,128)
    harness.activate(model,('phase2','identity',None),deferred=True);harness.last_logits(model,sequence,128)
    harness.RECON['stats'].finalize('FP32 timed identity');torch.cuda.synchronize();native=time.perf_counter()-tick
    steady=sum(t['seconds'] for t in times if t['repeat']==1)+native
    result={'model':name,'protocol_sha256':sha256_file(PROTOCOL),'n_articles_per_batch':2,
        'all_b_c_e_f_both_K_measured_or_exact_alias':True,'aliases':{} if cfg['diagonal_heads'] else {'svd_K_diag_exact':'svd_K','masked_K_diag_exact':'masked_K'},
        'load_and_native_control_seconds':overhead,'native_reference_and_identity_seconds_per_batch':native,
        'steady_batch_all_required_arms_seconds':steady,'cold_batch_seconds':sum(t['seconds'] for t in times if t['repeat']==0),
        'estimate_256_seconds_with_20percent_margin':1.2*(steady*128+overhead),
        'estimate_64_seconds_with_20percent_margin':1.2*(steady*32+overhead),
        'candidate_behavioral_KL_not_evaluated':True,'timings':times,
        'ALS_validation_passed':read(f'out/phase50_fp32_validation_{slug(name)}.json')['passed']}
    write_json_new(path,result);del model;gc.collect();torch.cuda.empty_cache();return result

def freeze_sample():
    path=Path('out/phase50_fp32_sample.json')
    if path.exists():return read(path)
    timings=[read(f'out/phase50_fp32_timing_{slug(m)}.json') for m in MODELS]
    total=sum(t['estimate_256_seconds_with_20percent_margin'] for t in timings)
    n=256 if total<=28800 else 64
    from sampling import CORPUS_PATH
    corpus=read(CORPUS_PATH)
    result={'protocol_sha256':sha256_file(PROTOCOL),'n_articles_per_model_all_arms':n,
        'document_indices':list(range(n)),'doc_ids':[d['doc_id'] for d in corpus['documents'][:n]],
        'estimated_total_256_GPU_service_seconds_including_20percent_margin':total,
        'estimated_total_64_GPU_service_seconds_including_20percent_margin':sum(t['estimate_64_seconds_with_20percent_margin'] for t in timings),
        'limit_seconds':28800,'decision':'256' if n==256 else 'first64',
        'same_first64_documents_as_matrix_sample':True,'fixed_before_new_scientific_forward_scoring':True,
        'selection_uses_runtime_only_no_new_candidate_KL':True,
        'passed_models':[m for m in MODELS if read(f'out/phase50_fp32_validation_{slug(m)}.json')['passed']],
        'failed_masked_models_not_qualified_for_equivalence_to_CPU_reference':[m for m in MODELS if not read(f'out/phase50_fp32_validation_{slug(m)}.json')['passed']],
        'timing_sources':{f'out/phase50_fp32_timing_{slug(m)}.json':sha256_file(f'out/phase50_fp32_timing_{slug(m)}.json') for m in MODELS}}
    write_json_new(path,result);print('FROZEN SAMPLE',n,'estimate256hours',total/3600,flush=True);return result

def forward(name):
    path=Path(f'out/phase50_fp32_forward_{slug(name)}.json')
    if path.exists():return read(path)
    sample=read('out/phase50_fp32_sample.json');n=sample['n_articles_per_model_all_arms']
    passed=read(f'out/phase50_fp32_validation_{slug(name)}.json')['passed']
    cfg=read('out/phase50_protocol.json')['datasets'][name];arms=modes(cfg,passed)
    pairs=Path(f'out/pairs/phase50_fp32_forward_{slug(name)}.jsonl')
    rows=jsonl(pairs) if pairs.exists() else [];seen={(r['arm'],r['K'],r['document_index']) for r in rows}
    if len(rows)!=len(seen) or any(r['protocol_sha256']!=sha256_file(PROTOCOL) for r in rows):raise ValueError('Mixed resume')
    started=time.perf_counter();model=None
    if arms:
        model,adapter,windows,corpus,cfg,a,overhead=load(name)
        with pairs.open('a',encoding='utf-8') as out:
            for start in range(0,n,2):
                if all((arm,k,i) in seen for arm in arms for k in (8,16) for i in (start,start+1)):continue
                sequence=windows[start:start+2];targets=sequence[:,128]
                model.set_attn_implementation('eager');ref=harness.last_logits(model,sequence,128)
                _,refn=harness.kl_nll(ref,ref,targets)
                harness.activate(model,('phase2','identity',None),deferred=True)
                ident=harness.last_logits(model,sequence,128);harness.RECON['stats'].finalize('FP32 perbatch identity')
                ik,_=harness.kl_nll(ref,ident,targets)
                if not torch.equal(ref,ident) or np.any(ik!=0):raise AssertionError('Perbatch identity failed')
                for k in (8,16):
                    for arm in arms:
                        if all((arm,k,i) in seen for i in (start,start+1)):continue
                        adapter.arm=arm;adapter.k=k;adapter.reset();model.set_attn_implementation('phase50_fp32')
                        logits=harness.last_logits(model,sequence,128);adapter.stats.finalize('FP32 scientific forward')
                        check_calls(adapter,corpus,name,2);kl,nll=harness.kl_nll(ref,logits,targets)
                        for bi in (0,1):
                            di=start+bi
                            if abs(float(refn[bi])-a[k,di]['reference_nll'])>2e-5:raise ValueError('V1 reference drift')
                            if (arm,k,di) in seen:continue
                            row={'model':name,'arm':arm,'K':k,'document_index':di,'doc_id':corpus['documents'][di]['doc_id'],
                                'target_id':int(targets[bi]),'offset':corpus['models'][name]['documents'][di]['offset'],
                                'n':128,'dtype':cfg['dtype'],'batch_start':start,'batch_size':2,
                                'kl':float(kl[bi]),'nll':float(nll[bi]),'reference_nll':float(refn[bi]),'identity_KL':float(ik[bi]),
                                'protocol_sha256':sha256_file(PROTOCOL),'sample_sha256':sha256_file('out/phase50_fp32_sample.json'),
                                'corpus_manifest_sha256':corpus['sha256'] if 'sha256' in corpus else read('out/phase50_protocol.json')['corpus_manifest_sha256'],
                                'empty_row_policy':'uniform','ALS_qualified_against_CPU_reference':passed if arm!='svd_K_diag_exact' else None,
                                'attention_validation_batch':dict(adapter.stats),'diagonal_heads':cfg['diagonal_heads'],
                                'max_NNLS_KKT':adapter.kkt,'max_active_atoms':adapter.max_active,
                                'ALS':diagnostics(adapter.document_infos[bi]) if adapter.document_infos else None}
                            out.write(json.dumps(row,separators=(',',':'),allow_nan=False)+'\n');out.flush();rows.append(row);seen.add((arm,k,di))
                print(f'FORWARD FP32 {name} {start+2}/{n} articles; elapsed={time.perf_counter()-started:.1f}s',flush=True)
    else:
        if not pairs.exists():pairs.touch(exist_ok=False)
    if seen!={(arm,k,i) for arm in arms for k in (8,16) for i in range(n)}:raise ValueError('Incomplete model')
    result={'model':name,'n_articles':n,'arms_run':arms,'ALS_validation_passed':passed,
        'unavailable_arms':[] if passed else ['masked_K','named_plus_masked','masked_K_diag_exact'],
        'aliases':{} if cfg['diagonal_heads'] else {'svd_K_diag_exact':'svd_K',**({'masked_K_diag_exact':'masked_K'} if passed else {})},
        'pairs_path':pairs.as_posix(),'pairs_sha256':sha256_file(pairs),'protocol_sha256':sha256_file(PROTOCOL),
        'sample_sha256':sha256_file('out/phase50_fp32_sample.json'),'elapsed_seconds':time.perf_counter()-started}
    write_json_new(path,result)
    if model is not None:del model;gc.collect();torch.cuda.empty_cache()
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['timing','forward','sample']);p.add_argument('--model',choices=MODELS)
    p.add_argument('--under-gpu-lock',action='store_true');a=p.parse_args()
    if a.action=='sample':freeze_sample()
    else:
        if not a.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
        (timing if a.action=='timing' else forward)(a.model)
