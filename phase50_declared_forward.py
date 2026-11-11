"""Behavioral E9 for the user-declared FP32 estimator, same frozen64 articles.

Kernel/ALS code is imported unchanged. Empty-row instrumentation receives the
actual mask computed inside phase2; it does not implement normalization again.
"""
import phase50_fp32_als as als
import argparse,gc,json,time,hashlib
from contextlib import contextmanager
from functools import partial
from pathlib import Path
import numpy as np
import torch
from transformers import AttentionInterface
import phase2_downstream as harness
from phase50_fp32_forward import Adapter,load,check_calls,diagnostics as base_diagnostics
from phase50_forward import attention
from phase50_experiment import read,jsonl
from sampling import slug,sha256_file,write_json_new

DECISION='out/phase50_declared_fp32_decision.json'
E_REPLAY='svd_K_diag_exact_empty_stats_replay'
IMPLEMENTATION_FIX='out/phase50_declared_implementation_fix.json'

def check_implementation_fix():
    if not Path(IMPLEMENTATION_FIX).exists():return None
    policy=read(IMPLEMENTATION_FIX)
    if sha256_file(policy['source'])!=policy['source_sha256']:
        raise AssertionError('Controlled numerical correction source changed')
    control=policy['control']
    if sha256_file(control['path'])!=control['sha256'] or not read(control['path'])['passed']:
        raise AssertionError('Native-SVD correction control changed or failed')
    return policy

def diagnostics(infos):
    result=base_diagnostics(infos)
    if result is None:return None
    result['invalid_native_core_singular_values_recomputed']=sum(x.get('invalid_native_core_singular_values_recomputed',0) for x in infos)
    result['fits_with_native_core_singular_value_recomputation']=sum(x.get('invalid_native_core_singular_values_recomputed',0)>0 for x in infos)
    result['factor_magnitudes_scope']='final balanced factors, maximum across the fits; not the maximum of every intermediate sweep'
    return result

@contextmanager
def count_effective_empty(adapter,weights,layer):
    """Observe the harness's computed empty mask; exact heads use original A."""
    b,h,q,n=weights.shape
    eligible=torch.tensor([(layer,hh) not in adapter.diag_heads for hh in range(h)],device=weights.device,dtype=torch.bool)
    saved=harness.record_reconstruction_rows
    def record(rec,stats,empty=None):
        saved(rec,stats,empty)
        if stats is not adapter.stats:return
        if empty is None or tuple(empty.shape)!=(b*h,q,1):raise AssertionError('Unexpected e completion-mask layout')
        mask=empty.reshape(b,h,q,1);effective=mask & eligible[None,:,None,None]
        stats.add_scalar('effective_empty_rows_completed',effective.sum())
        stats.add_scalar('effective_empty_rows_completed_at_last_query',effective[:,:,-1,:].sum())
        stats.add_scalar('discarded_exact_head_candidate_empty_rows',mask.sum()-effective.sum())
        stats.add_scalar('discarded_exact_head_candidate_empty_last_rows',mask[:,:,-1,:].sum()-effective[:,:,-1,:].sum())
        exact=sum((layer,hh) in adapter.diag_heads for hh in range(h))
        stats['exact_rows_total']=stats.get('exact_rows_total',0)+b*exact*q
        stats['exact_last_query_rows_total']=stats.get('exact_last_query_rows_total',0)+b*exact
    harness.record_reconstruction_rows=record
    try:yield
    finally:harness.record_reconstruction_rows=saved

class InstrumentedAdapter(Adapter):
    @torch.inference_mode()
    def reconstruct(self,weights,module):
        if self.arm!='svd_K_diag_exact':return super().reconstruct(weights,module)
        layer=getattr(module,'layer_idx',None)
        if layer is None:layer=getattr(module,'layer_index',None)
        if layer is None:raise ValueError('Layer index missing')
        with count_effective_empty(self,weights,int(layer)):
            return super().reconstruct(weights,module)

def completion(stats,arm):
    result=harness.completion_summary(stats)
    if arm==E_REPLAY:
        result['candidate_rows_completed_before_exact_overwrite']=result['rows_completed']
        result['candidate_last_query_rows_completed_before_exact_overwrite']=result['last_query_rows_completed']
        result['rows_completed']=stats['effective_empty_rows_completed']
        result['last_query_rows_completed']=stats['effective_empty_rows_completed_at_last_query']
        result['fraction_rows_completed']=result['rows_completed']/result['rows_total']
        result['fraction_last_query_rows_completed']=result['last_query_rows_completed']/result['last_query_rows_total']
        result['discarded_exact_head_candidate_empty_rows']=stats['discarded_exact_head_candidate_empty_rows']
        result['discarded_exact_head_candidate_empty_last_rows']=stats['discarded_exact_head_candidate_empty_last_rows']
        result['exact_rows_total']=stats['exact_rows_total']
        result['exact_last_query_rows_total']=stats['exact_last_query_rows_total']
        result['scope']='actual injected e; empty candidates on exact heads were discarded and do not count'
    else:
        result['scope']='actual injected arm; exact heads, if any, contribute zero completions'
    if not 0<=result['rows_completed']<=result['rows_total'] or not 0<=result['last_query_rows_completed']<=result['last_query_rows_total']:
        raise AssertionError('Impossible completion counts')
    return result

def methods(cfg):
    return ['masked_K','named_plus_masked']+(['masked_K_diag_exact',E_REPLAY] if cfg['diagonal_heads'] else [])

def check_decision():
    dec=read(DECISION)
    if dec['CPU_float64_reference_equivalence']['is_behavioral_execution_gate']:raise AssertionError('User declaration is not active')
    if sha256_file('out/phase50_fp32_sample.json')!=dec['sample_sha256']:raise AssertionError('Fixed sample changed')
    if sha256_file('phase2_downstream.py')!=dec['harness_sha256']:raise AssertionError('Harness changed')
    for p,digest in dec['estimator_sources'].items():
        if sha256_file(p)!=digest:raise AssertionError('Declared estimator changed')
    if als.SWEEPS!=200 or als.RIDGE!=1e-6:raise AssertionError('Sweeps or ridge changed')
    if not read('out/phase50_fp32_controls.json')['passed']:raise AssertionError('Local/plant controls failed')
    return dec

def control():
    """Meaningful CPU check: exact-head counters exclude only discarded fills."""
    path=Path('out/phase50_declared_empty_counter_control.json')
    if path.exists():
        previous=read(path)
        if not previous['passed'] or previous['decision_sha256']!=sha256_file(DECISION):raise AssertionError('Prior counter control failed or changed declaration')
        return previous
    class Dummy:pass
    obj=Dummy();obj.diag_heads={(0,0)};obj.stats=harness.DeferredStats()
    original=torch.eye(128).expand(6,128,128).clone();rec=original.clone().reshape(2,3,128,128);rec[:,:2]=0;rec=rec.reshape(6,128,128)
    untouched=harness.record_reconstruction_rows
    expected=harness.normalize_reconstruction(rec,original,harness.DeferredStats(),'uniform')
    with count_effective_empty(obj,original.reshape(2,3,128,128),0):
        actual=harness.normalize_reconstruction(rec,original,obj.stats,'uniform')
    obj.stats.finalize('declared empty-counter control');s=completion(obj.stats,E_REPLAY)
    passed=(torch.equal(actual,expected) and harness.record_reconstruction_rows is untouched
        and s['rows_total']==768 and s['candidate_rows_completed_before_exact_overwrite']==512
        and s['rows_completed']==256 and s['last_query_rows_total']==6 and s['last_query_rows_completed']==2
        and s['discarded_exact_head_candidate_empty_rows']==256)
    result={'passed':passed,'normalization_output_bit_equal':torch.equal(actual,expected),
        'hook_restored':harness.record_reconstruction_rows is untouched,'completion':s,
        'mask_computed_by_imported_phase2_normalizer':True,'decision_sha256':sha256_file(DECISION)}
    write_json_new(path,result)
    if not passed:raise AssertionError('Effective empty-row counter control failed')
    print('Effective empty-row counter control passed',flush=True);return result

def finalize(name):
    dec=check_decision();fix=check_implementation_fix();ph=sha256_file(DECISION);cfg=read('out/phase50_protocol.json')['datasets'][name]
    target=Path(f'out/phase50_declared_forward_{slug(name)}.json');pairs=Path(f'out/pairs/phase50_declared_forward_{slug(name)}.jsonl')
    if target.exists():
        old=read(target)
        if old['pairs_sha256']!=sha256_file(pairs) or old['decision_sha256']!=ph:raise AssertionError('Completed model changed')
        return old
    rows=jsonl(pairs);arms=methods(cfg)
    expected={(arm,k,i) for arm in arms for k in (8,16) for i in range(64)}
    keys={(r['arm'],r['K'],r['document_index']) for r in rows}
    if keys!=expected or len(rows)!=len(keys):raise AssertionError('Incomplete declared-model forward')
    if any(r['decision_sha256']!=ph or r['sample_sha256']!=dec['sample_sha256'] for r in rows):raise AssertionError('Mixed declaration or sample')
    chunks=sorted(Path('out').glob(f'phase50_declared_chunk_{slug(name)}_*.json'))
    if [(read(p)['start_document'],read(p)['stop_document']) for p in chunks]!=[(i,i+16) for i in range(0,64,16)]:
        raise AssertionError('The four declared16-article checkpoints are required')
    with pairs.open('rb') as inp:
        for p in chunks:
            checkpoint=read(p);inp.seek(0);prefix=inp.read(checkpoint['pairs_byte_length'])
            if checkpoint['decision_sha256']!=ph or hashlib.sha256(prefix).hexdigest()!=checkpoint['pairs_prefix_sha256']:
                raise AssertionError('A committed chunk or its decision changed')
    obj={'model':name,'n_articles':64,'K':[8,16],'arms_evaluated':['masked_K','named_plus_masked']+(['masked_K_diag_exact'] if cfg['diagonal_heads'] else []),
        'aliases':{} if cfg['diagonal_heads'] else {'masked_K_diag_exact':'masked_K','svd_K_diag_exact':'svd_K'},
        'e_empty_counter_replay':bool(cfg['diagonal_heads']),'decision_sha256':ph,'sample_sha256':dec['sample_sha256'],
        'CPU_float64_equivalence_passed':False,'equivalence_is_behavioral_gate':False,
        'pairs_path':pairs.as_posix(),'pairs_sha256':sha256_file(pairs),'n_records':len(rows),
        'chunks':[p.as_posix() for p in chunks],'chunk_sha256':{p.as_posix():sha256_file(p) for p in chunks},
        'elapsed_chunk_seconds':sum(read(p)['elapsed_seconds'] for p in chunks),
        'GPU_lock_released_between_models_and_chunks':True,'estimator_sources':dec['estimator_sources'],
        'implementation_fix_path':IMPLEMENTATION_FIX if fix else None,
        'implementation_fix_sha256':sha256_file(IMPLEMENTATION_FIX) if fix else None,
        'n_records_with_controlled_implementation_fix':sum(r.get('implementation_fix_sha256') is not None for r in rows)}
    write_json_new(target,obj);return obj

def run(name,start,stop):
    dec=check_decision();control();ph=sha256_file(DECISION);parent=read('out/phase50_protocol.json');cfg=parent['datasets'][name]
    fix=check_implementation_fix()
    if fix:
        from phase50_declared_core_value_recompute import install
        install()
    fix_sha=sha256_file(IMPLEMENTATION_FIX) if fix else None
    if not(0<=start<stop<=64 and start%2==0 and stop%2==0):raise ValueError('Chunk must preserve original batch2 and corpus64')
    target=Path(f'out/phase50_declared_chunk_{slug(name)}_{start:03d}_{stop:03d}.json')
    pairs=Path(f'out/pairs/phase50_declared_forward_{slug(name)}.jsonl')
    if target.exists():
        old=read(target)
        if old['decision_sha256']!=ph:raise AssertionError('Chunk decision changed')
        with pairs.open('rb') as f:prefix=f.read(old['pairs_byte_length'])
        if hashlib.sha256(prefix).hexdigest()!=old['pairs_prefix_sha256']:raise AssertionError('Committed chunk changed')
        return old
    rows=jsonl(pairs) if pairs.exists() else [];seen={(r['arm'],r['K'],r['document_index']) for r in rows}
    if len(rows)!=len(seen) or any(r['decision_sha256']!=ph for r in rows):raise AssertionError('Invalid resume rows')
    started=time.perf_counter();model,base,windows,corpus,cfg,a,overhead=load(name)
    adapter=InstrumentedAdapter(base.dictionary,cfg['diagonal_heads']);del base
    AttentionInterface.register('phase50_declared',partial(attention,adapter))
    old_e={}
    if cfg['diagonal_heads']:
        oldmeta=read(f'out/phase50_fp32_forward_{slug(name)}.json')
        if sha256_file(oldmeta['pairs_path'])!=oldmeta['pairs_sha256']:raise AssertionError('Existing e records changed')
        old_e={(r['K'],r['document_index']):r for r in jsonl(oldmeta['pairs_path'])}
    arms=methods(cfg);pairs.parent.mkdir(parents=True,exist_ok=True)
    with pairs.open('a',encoding='utf-8') as out:
        for begin in range(start,stop,2):
            if all((arm,k,i) in seen for arm in arms for k in (8,16) for i in (begin,begin+1)):continue
            seq=windows[begin:begin+2];targets=seq[:,128]
            model.set_attn_implementation('eager');ref=harness.last_logits(model,seq,128);_,refn=harness.kl_nll(ref,ref,targets)
            harness.activate(model,('phase2','identity',None),deferred=True)
            ident=harness.last_logits(model,seq,128);harness.RECON['stats'].finalize('declared per-batch identity')
            ik,_=harness.kl_nll(ref,ident,targets)
            if not torch.equal(ref,ident) or np.any(ik!=0):raise AssertionError('Identity KL/logits failed')
            for k in (8,16):
                for arm in arms:
                    if all((arm,k,i) in seen for i in (begin,begin+1)):continue
                    adapter.arm='svd_K_diag_exact' if arm==E_REPLAY else arm;adapter.k=k;adapter.reset()
                    model.set_attn_implementation('phase50_declared');tick=time.perf_counter()
                    logits=harness.last_logits(model,seq,128);adapter.stats.finalize('declared '+name+' '+arm)
                    check_calls(adapter,corpus,name,2);kl,nll=harness.kl_nll(ref,logits,targets)
                    stats=dict(adapter.stats);counts=completion(stats,arm)
                    for bi in (0,1):
                        di=begin+bi
                        if abs(float(refn[bi])-a[k,di]['reference_nll'])>2e-5:raise AssertionError('Native V1 reference drift')
                        if (arm,k,di) in seen:continue
                        row={'model':name,'arm':arm,'K':k,'document_index':di,'doc_id':corpus['documents'][di]['doc_id'],
                            'offset':corpus['models'][name]['documents'][di]['offset'],'target_id':int(targets[bi]),'n':128,
                            'dtype':cfg['dtype'],'batch_start':begin,'batch_size':2,'kl':float(kl[bi]),'nll':float(nll[bi]),
                            'reference_nll':float(refn[bi]),'identity_KL':float(ik[bi]),'decision_sha256':ph,
                            'sample_sha256':dec['sample_sha256'],'FP32_protocol_sha256':dec['FP32_protocol_sha256'],
                            'corpus_manifest_sha256':dec['corpus_manifest_sha256'],'empty_row_policy':'uniform',
                            'attention_validation_batch':stats,'uniform_completion_batch':counts,'diagonal_heads':cfg['diagonal_heads'],
                            'CPU_float64_equivalence_passed':False,'equivalence_is_behavioral_gate':False,
                            'implementation_fix_sha256':fix_sha,
                            'max_NNLS_KKT':adapter.kkt,'max_active_atoms':adapter.max_active,
                            'ALS':diagnostics(adapter.document_infos[bi]) if adapter.document_infos else None}
                        if arm==E_REPLAY:
                            source=old_e[k,di];dk=abs(row['kl']-source['kl']);dn=abs(row['nll']-source['nll'])
                            if max(dk,dn)>2e-5:raise AssertionError(f'Instrumented e changed behavior: KLdiff={dk}, NLLdiff={dn}')
                            row.update(behavioral_role='counter replay only; original e KL/NLL retained',
                                original_e_kl=source['kl'],original_e_nll=source['nll'],e_KL_absolute_replay_difference=dk,e_NLL_absolute_replay_difference=dn)
                        out.write(json.dumps(row,separators=(',',':'),allow_nan=False)+'\n');out.flush();rows.append(row);seen.add((arm,k,di))
                    print(f'DECLARED {name} docs{begin}:{begin+2} K{k} {arm} seconds={time.perf_counter()-tick:.2f} total={time.perf_counter()-started:.1f}s',flush=True)
    if not all((arm,k,i) in seen for arm in arms for k in (8,16) for i in range(start,stop)):raise AssertionError('Incomplete chunk')
    obj={'model':name,'start_document':start,'stop_document':stop,'decision_sha256':ph,
        'pairs_byte_length':pairs.stat().st_size,'pairs_prefix_sha256':sha256_file(pairs),
        'elapsed_seconds':time.perf_counter()-started,'load_and_native_control_seconds':overhead,
        'n_records_completed_so_far':len(rows),'e_replay_KL_NLL_verified':bool(old_e)}
    write_json_new(target,obj)
    del model,adapter;gc.collect();torch.cuda.empty_cache()
    if seen=={(arm,k,i) for arm in arms for k in (8,16) for i in range(64)}:finalize(name)
    return obj

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['control','chunk','finalize'])
    p.add_argument('--model');p.add_argument('--start',type=int);p.add_argument('--stop',type=int);p.add_argument('--under-gpu-lock',action='store_true');arg=p.parse_args()
    if arg.action=='control':control()
    elif arg.action=='finalize':finalize(arg.model)
    else:
        if not arg.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
        run(arg.model,arg.start,arg.stop)
