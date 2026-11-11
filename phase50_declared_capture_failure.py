"""Reproduce and preserve an actual failed ALS input; exception is re-raised."""
import phase50_fp32_als as als
import argparse
import torch
from pathlib import Path
from phase50_declared_forward import InstrumentedAdapter,DECISION,load,attention
from functools import partial
from transformers import AttentionInterface
import phase2_downstream as harness
import phase50_fp32_graph as graph_module
from sampling import write_json_new,sha256_file

_fit=als.fit;_reconstruct=InstrumentedAdapter.reconstruct;context={};failed_execute_inputs={}
_execute=graph_module.SweepGraph.execute

def execute(self,target,u,v):
    try:return _execute(self,target,u,v)
    except FloatingPointError:
        failed_execute_inputs.update(target=target.cpu().tolist(),u=u.cpu().tolist(),v=v.cpu().tolist())
        raise

def reconstruct(self,weights,module):
    layer=getattr(module,'layer_idx',None)
    if layer is None:layer=getattr(module,'layer_index',None)
    context.update(arm=self.arm,K=self.k,layer=int(layer))
    return _reconstruct(self,weights,module)

def fit(a,rank,support,initial=None,backend='torch'):
    try:return _fit(a,rank,support,initial,backend)
    except FloatingPointError as exc:
        path=Path('out/phase50_declared_failed_ALS_input_Qwen05_docs4_6.json')
        if not path.exists():
            left,s,vh=torch.linalg.svd(a.float(),full_matrices=False)
            root=s[:,:rank].sqrt()[:,None,:]
            write_json_new(path,{'context':dict(context),'rank':rank,'dtype':'float32','shape':list(a.shape),
                'input_A':a.float().cpu().tolist(),'initial_U_recomputed':(left[:,:,:rank]*root).cpu().tolist(),
                'initial_V_recomputed':(vh[:,:rank,:].transpose(-1,-2)*root).cpu().tolist(),
                'exact_execute_inputs_normalized':dict(failed_execute_inputs),
                'initial_recomputation_note':'same CUDA truncated SVD input, deterministic library recomputation for diagnosis; failure result not replaced',
                'error_type':type(exc).__name__,'error':str(exc),'decision_sha256':sha256_file(DECISION),
                'estimator_sources':{p:sha256_file(p) for p in ['phase50_fp32_als.py','phase50_fp32_graph.py']}})
        print('PRESERVED FAILED INPUT',str(path),'context',dict(context),flush=True)
        raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--under-gpu-lock',action='store_true');args=ap.parse_args()
    if not args.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
    InstrumentedAdapter.reconstruct=reconstruct;als.fit=fit;graph_module.SweepGraph.execute=execute
    model,base,windows,corpus,cfg,original,overhead=load('Qwen/Qwen2.5-0.5B')
    adapter=InstrumentedAdapter(base.dictionary,cfg['diagonal_heads']);adapter.arm='masked_K_diag_exact';adapter.k=16
    AttentionInterface.register('phase50_capture_only',partial(attention,adapter));model.set_attn_implementation('phase50_capture_only')
    # No KL/NLL is computed and no scientific pair/checkpoint is written.
    logits=harness.last_logits(model,windows[4:6],128)
    write_json_new('out/phase50_declared_failure_not_reproduced_fresh_cache.json',{'finite_logits':bool(torch.isfinite(logits).all()),
        'same_model_arm_K_documents':True,'fresh_graph_cache':True,'no_behavioral_KL_NLL_computed':True,
        'interpretation':'The original failure remains preserved; a fresh-cache diagnostic cannot replace the failed scientific evaluation.'})
    print('Failure not reproduced with fresh cache; no KL/NLL scored',flush=True)
