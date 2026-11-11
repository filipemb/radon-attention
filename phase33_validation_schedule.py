"""P0 CPU regression: defer only synchronization, never any validity check."""
from sampling import CORPUS_PATH, write_json_new, progress, sha256_file
import json
from pathlib import Path
import time
import torch
from transformers import AutoModelForCausalLM, AttentionInterface
import phase2_downstream as p2
import phase7_editability as p7
import phase8_lostmiddle as p8
import phase28_beta0_retest as beta_probe

torch.set_num_threads(4)

def same_stats(immediate,deferred):
    deferred.finalize("CPU regression")
    for key,value in immediate.items():
        assert deferred[key]==value,(key,value,deferred[key])

def must_fail(action):
    try:
        action()
    except RuntimeError:
        return
    raise AssertionError("A required validity check was skipped")

def synthetic():
    torch.manual_seed(0)
    cases=[]
    for dtype in (torch.float32,torch.bfloat16):
        for q,k in ((16,16),(4,16),(1,16)):
            mask=p2.causal_support(q,k,"cpu")
            w=torch.randn(2,3,q,k).masked_fill(~mask,float("-inf")).softmax(-1).to(dtype)
            for mode in ("identity","svd","uniform","diagonal","sink"):
                immediate={};p2.RECON.update(mode=mode,k=4,stats=immediate)
                old=p2.reconstruct(w)
                deferred=p2.DeferredStats();p2.RECON["stats"]=deferred
                new=p2.reconstruct(w)
                assert torch.equal(old,new) and old.stride()==new.stride()
                same_stats(immediate,deferred)
                cases.append(f"{dtype}:{mode}:q{q}:k{k}")
            for mode in ("anova","nosink","zerocol_mid"):
                immediate={};p7.RECON.update(mode=mode,k=4,stats=immediate)
                old=p7.reconstruct(w)
                deferred=p2.DeferredStats();p7.RECON["stats"]=deferred
                new=p7.reconstruct(w)
                assert torch.equal(old,new) and old.stride()==new.stride()
                same_stats(immediate,deferred)
                cases.append(f"{dtype}:{mode}:q{q}:k{k}")
    # Interleaved geometric layout, with and without empty rows. Preserve the
    # old reduction layout/conditional branch rather than changing rounding.
    for empty in (False,True):
        rec=torch.rand(16,16,6).permute(2,0,1)
        if empty:rec[:,7,:]=0
        assert not rec.is_contiguous()
        original=torch.full_like(rec,float("nan"))
        immediate={};old=p2.normalize_reconstruction(rec,original,immediate)
        deferred=p2.DeferredStats();new=p2.normalize_reconstruction(rec,original,deferred)
        assert torch.equal(old,new) and old.stride()==new.stride()
        same_stats(immediate,deferred)
        cases.append(f"interleaved_reconstruction:empty={empty}")
    for dtype in (torch.float32,torch.bfloat16):
        for beta in (0.,.05,.25,1.):
            before=torch.zeros(1,2,5,5,dtype=dtype)
            before[...,0,0]=1;before[...,1,0]=1
            before[...,2,0]=.5;before[...,2,2]=.5
            before[...,3,0]=1;before[...,4,0]=1;before[...,4,4]=1e-15
            edited=before.clone();edited[...,0]*=beta
            immediate={};old=p8.finish_sink_edit(before,edited,immediate)
            deferred=p2.DeferredStats();new=p8.finish_sink_edit(before,edited,deferred)
            assert torch.equal(old,new)
            same_stats(immediate,deferred)
            cases.append(f"sink:{dtype}:beta{beta}")
    failures=[]
    bad_examples={}
    for name in ("negative","above_diagonal","nan","inf","wrong_row_sum"):
        w=torch.eye(4)[None,None].clone()
        if name=="negative":w[...,2,0]=-.1
        elif name=="above_diagonal":w[...,0,2]=.1
        elif name=="nan":w[...,2,1]=float("nan")
        elif name=="inf":w[...,2,1]=float("inf")
        else:w[...,2,2]=1.01
        bad_examples[name]=w
    for name,w in bad_examples.items():
        must_fail(lambda:p2.validate_attention(w,{}))
        deferred=p2.DeferredStats();p2.validate_attention(w,deferred)
        must_fail(deferred.finalize)
        failures.append(name)
    for value in (float("nan"),float("inf"),-float("inf")):
        rec=torch.eye(4)[None].clone();rec[...,2,1]=value
        must_fail(lambda:p2.normalize_reconstruction(rec,rec,{}))
        deferred=p2.DeferredStats();p2.normalize_reconstruction(rec,rec,deferred)
        must_fail(deferred.finalize)
        failures.append(f"nonfinite_reconstruction:{value}")
    boundary=[]
    for delta,expected in ((1.9e-6,True),(2.1e-6,False)):
        w=torch.eye(4)[None,None];w[...,2,2]+=delta
        deferred=p2.DeferredStats()
        if expected:
            p2.validate_attention(w,{},normalized_fp32=True)
            p2.validate_attention(w,deferred,normalized_fp32=True);deferred.finalize()
        else:
            must_fail(lambda:p2.validate_attention(w,{},normalized_fp32=True))
            p2.validate_attention(w,deferred,normalized_fp32=True);must_fail(deferred.finalize)
        boundary.append({"delta":delta,"accepted_by_both":expected})
    return {"bit_equal_tensor_and_counter_cases":cases,"invalid_inputs_rejected_by_both":failures,
            "fixed_tolerance_boundary_cases":boundary,"row_atol_unchanged":2e-6}

@torch.inference_mode()
def pretrained():
    corpus=json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    model=AutoModelForCausalLM.from_pretrained("gpt2",revision=corpus["models"]["gpt2"]["revision"],
                 local_files_only=True,dtype=torch.float32,attn_implementation="eager").eval()
    assert next(model.parameters()).device.type=="cpu"
    windows=torch.tensor([d["token_ids"] for d in corpus["models"]["gpt2"]["documents"][:2]])
    p2.RECON["D"]=p2.build_dictionary(128,"cpu")
    q,r=torch.linalg.qr(p2.RECON["D"],mode="reduced")
    p2.RECON["D_pinv"]=torch.linalg.solve_triangular(r,q.T,upper=True)
    AttentionInterface.register("p0_recon",p2.attention_forward)
    AttentionInterface.register("p0_anova",p7.recon_attention_forward)
    AttentionInterface.register("p0_schedule_sink",p8.recon_attention_forward)
    arms=[]
    for spec in p2.mode_specs(("phase2","phase7")):
        immediate=p2.activate(model,spec)
        old=p2.last_logits(model,windows,128)
        deferred=p2.activate(model,spec,deferred=True)
        new=p2.last_logits(model,windows,128)
        assert torch.equal(old,new),p2.arm_label(spec)
        same_stats(immediate,deferred)
        arms.append({"arm":p2.arm_label(spec),"logits_bit_equal":True,"maximum_difference":0.})
        print("CPU pretrained schedule regression:",p2.arm_label(spec),flush=True)
    probe_archive,_=beta_probe.probe_paths("gpt2")
    import numpy as np
    with np.load(probe_archive,allow_pickle=False) as z:ids=torch.tensor(z["input_ids"][:2])
    sink=[]
    model.set_attn_implementation("p0_schedule_sink")
    for beta in (0.,.25,1.):
        immediate={};p8.RECON.update(beta=beta,stats=immediate)
        old=model(ids,use_cache=False,logits_to_keep=1).logits
        deferred=p2.DeferredStats();p8.RECON.update(beta=beta,stats=deferred)
        new=model(ids,use_cache=False,logits_to_keep=1).logits
        assert torch.equal(old,new)
        same_stats(immediate,deferred)
        sink.append({"beta":beta,"logits_bit_equal":True,"maximum_difference":0.})
    return {"model":"pretrained gpt2","device":"cpu","n_documents":2,"prefix_length":128,
            "arms":arms,"sink_betas":sink}

def main():
    started=time.perf_counter()
    result={"all_passed":False,"synthetic":synthetic(),"pretrained":pretrained()}
    result["all_passed"]=True;result["elapsed_seconds"]=time.perf_counter()-started
    result["source_sha256"]={name:sha256_file(name) for name in ("phase2_downstream.py","phase7_editability.py","phase8_lostmiddle.py")}
    write_json_new("out/phase33_validation_schedule_checks_v2.json",result)
    progress("V1 batched validation regression","All checks and counters retained; bit-identical reconstructed tensors and pretrained logits; invalid inputs and original tolerance boundaries rejected",
             result["elapsed_seconds"],".venv/Scripts/python.exe -B phase33_validation_schedule.py")
    print(f"All validation schedule checks passed in {result['elapsed_seconds']:.3f}s",flush=True)

if __name__=="__main__":main()
