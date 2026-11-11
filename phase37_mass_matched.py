"""Coupled mass-matched interventions, true attention and ANOVA, last token.

Six same-item branches run together so that each sink/control pair removes
exactly the same feasible q at every layer/head/query even after feedback has
made their attention matrices differ. Nominal beta is capped for both arms;
it is not the uncapped full-removal beta0 experiment of phase28.
"""
from revision_v3_stats import (MODELS,CORPUS_PATH,slug,sha256_file,write_json_new,progress,
                               describe,paired_wilcoxon,holm)
import argparse
import gc
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import torch
from transformers import AutoModelForCausalLM,AttentionInterface
import phase2_downstream as p2
import phase7_editability as p7
from phase8_lostmiddle import finish_sink_edit

torch.set_num_threads(4)
ROLES=["baseline","zerocol_mid","sink_beta0_matched","control_beta0_matched",
       "sink_beta0.25_matched","control_beta0.25_matched"]
CONTEXTS=["identity","anova"]
STATE={"context":"identity","doc_id":"","layer":0,"parallel":False,"disable_edits":False}

class Checks(p2.DeferredStats):
    violation_keys=p2.DeferredStats.violation_keys+("mass_mismatch_rows","mass_invalid_values",
        "mass_invalid_budget","mass_first_row_changes")

def hashes():
    return {p:sha256_file(p) for p in ["phase37_mass_matched.py","revision_v3_stats.py",
        "phase2_downstream.py","phase7_editability.py","phase8_lostmiddle.py","phase34_parallel_svd.py","sampling.py"]}

def random_order(doc_id,layer,heads,q,k,device):
    digest=hashlib.sha256(f"seed0|{doc_id}|layer{layer}".encode()).digest()
    seed=int.from_bytes(digest[:8],"little")%(2**63-1)
    gen=torch.Generator(device=device).manual_seed(seed)
    # Zero-mass (future) columns can appear anywhere in the ordering: removing
    # zero consumes no budget. The causal nonzero subsequence is still random.
    return torch.argsort(torch.rand((1,heads,q,k-1),device=device,dtype=torch.float64,generator=gen),dim=-1,stable=True)

def matched_edit(sink,control,beta,order,stats):
    """Pure tensor adapter also usable by an external S+L reconstructor."""
    s,c=sink.double(),control.double();q,k=s.shape[-2:]
    stats.add_scalar("mass_invalid_values",((~torch.isfinite(s))|(s<0)).sum()+((~torch.isfinite(c))|(c<0)).sum())
    requested=(1-beta)*s[...,0]
    if q==k:
        requested=requested.clone();requested[...,0]=0
    ns_s=s[...,1:].sum(-1);ns_c=c[...,1:].sum(-1)
    budget=torch.minimum(requested,torch.minimum(ns_s,ns_c))
    es=s.clone();es[...,0]-=budget
    values=c[...,1:].gather(-1,order)
    previous=values.cumsum(-1)-values
    removed=torch.minimum(values,(budget[...,None]-previous).clamp_min(0))
    remaining=torch.empty_like(values).scatter(-1,order,values-removed)
    ec=c.clone();ec[...,1:]=remaining
    actual_s=(s-es).sum(-1);actual_c=(c-ec).sum(-1)
    # Fixed float64 construction bound, scaled only by row length, before data.
    atol=32*k*torch.finfo(torch.float64).eps
    error=torch.maximum((actual_s-budget).abs(),(actual_c-budget).abs())
    stats.add_scalar("mass_mismatch_rows",(error>atol).sum())
    stats.max_scalar("max_mass_match_error",error.max());stats["mass_match_atol"]=atol
    stats.add_scalar("mass_invalid_values",((es<0)|~torch.isfinite(es)).sum()+((ec<0)|~torch.isfinite(ec)).sum())
    stats.add_scalar("mass_invalid_budget",((budget<0)|(budget>s[...,0])|(budget>ns_s)|(budget>ns_c)).sum())
    stats.add_scalar("mass_rows_total",budget.numel())
    stats.add_scalar("mass_requested",requested.sum());stats.add_scalar("mass_removed_each_arm",budget.sum())
    stats.add_scalar("mass_rows_capped",(budget<requested).sum())
    stats.add_scalar("mass_rows_zero_request",(requested==0).sum())
    stats.add_scalar("last_query_mass_requested",requested[...,-1].sum())
    stats.add_scalar("last_query_mass_removed_each_arm",budget[...,-1].sum())
    stats.add_scalar("last_query_rows_capped",(budget[...,-1]<requested[...,-1]).sum())
    stats.add_scalar("last_query_rows_total",budget[...,-1].numel())
    if q==k:
        stats.add_scalar("mass_first_row_changes",(es[...,0,:]!=s[...,0,:]).sum()+(ec[...,0,:]!=c[...,0,:]).sum())
    return es,ec,budget

def reconstruct(weights):
    if weights.shape[0]!=6:raise ValueError("Exactly six same-item branches are required")
    layer=STATE["layer"];STATE["layer"]+=1
    base_stats=STATE["base_stats"];edit_stats=STATE["edit_stats"]
    if STATE["context"]=="anova":
        x=weights.float();mu=x.mean(dim=(-1,-2),keepdim=True)
        additive=x.mean(dim=-1,keepdim=True)+x.mean(dim=-2,keepdim=True)-mu
        u,s,vh=p2.factor_svd(x-additive,None,STATE["parallel"])
        rank=min(8,*x.shape[-2:])
        raw=additive+(u[...,:rank]*s[...,None,:rank])@vh[...,:rank,:]
        base=p2.normalize_reconstruction(raw,weights,STATE["combined_stats"],"uniform",cast_to_original=False)
        empty=(raw*p2.causal_support(*raw.shape[-2:],raw.device)).clamp_min(0).sum(-1,keepdim=True)<=0
        for i in range(6):
            p2.record_reconstruction_rows(base[i:i+1],base_stats[i],empty[i:i+1])
            p2.validate_attention(base[i:i+1],base_stats[i],normalized_fp32=True)
    else:
        base=weights.float()
        for i in range(6):
            p2.record_reconstruction_rows(weights[i:i+1],base_stats[i])
            p2.validate_attention(weights[i:i+1],base_stats[i])
    if STATE["disable_edits"]:
        result=base.to(weights.dtype)
        for i in range(6):p2.validate_attention(result[i:i+1],edit_stats[i])
        return result
    results=[base[i:i+1].to(weights.dtype) for i in range(6)]
    middle=base[1:2].clone();middle[...,middle.shape[-1]//2]=0
    results[1]=finish_sink_edit(base[1:2],middle,edit_stats[1]).to(weights.dtype)
    order=random_order(STATE["doc_id"],layer,weights.shape[1],*weights.shape[-2:],weights.device)
    for beta,si,ci in [(0.,2,3),(.25,4,5)]:
        ss,cc,budget=matched_edit(base[si:si+1],base[ci:ci+1],beta,order,STATE["mass_stats"][str(beta)])
        for index,edited in [(si,ss),(ci,cc)]:
            rec=p2.normalize_reconstruction(edited,weights[index:index+1],edit_stats[index],"uniform")
            # No requested edit means exact preservation, including native bf16
            # rows whose sums differ from 1 only by their original cast rounding.
            results[index]=torch.where((budget==0)[...,None],base[index:index+1].to(weights.dtype),rec)
    result=torch.cat(results,dim=0)
    for i in range(6):p2.validate_attention(result[i:i+1],edit_stats[i])
    if weights.shape[-2]==weights.shape[-1]:
        STATE["combined_stats"].add_scalar("sink_edit_first_row_changes",(result[...,0,:]!=weights[...,0,:]).sum())
    return result

def attention_forward(module,query,key,value,attention_mask,scaling=None,dropout=0.,**kwargs):
    return p2.attention_forward(module,query,key,value,attention_mask,scaling,dropout,reconstruct_fn=reconstruct,**kwargs)

def reset(context,doc_id,parallel=False,disable=False):
    STATE.update(context=context,doc_id=doc_id,layer=0,parallel=parallel,disable_edits=disable,
        base_stats=[Checks() for _ in ROLES],edit_stats=[Checks() for _ in ROLES],
        combined_stats=Checks(),mass_stats={str(b):Checks() for b in [0.,.25]})

def finish(n_layers):
    assert STATE["layer"]==n_layers
    for category in ["base_stats","edit_stats"]:
        for stats in STATE[category]:stats.finalize(category)
    STATE["combined_stats"].finalize("combined")
    for stats in STATE["mass_stats"].values():stats.finalize("mass equality")
    return {"base":[dict(s) for s in STATE["base_stats"]],"edit":[dict(s) for s in STATE["edit_stats"]],
        "combined":dict(STATE["combined_stats"]),"mass":{k:dict(v) for k,v in STATE["mass_stats"].items()}}

@torch.inference_mode()
def forward(model,sequence,context,doc_id,parallel=False,disable=False):
    reset(context,doc_id,parallel,disable)
    model.set_attn_implementation("revision_v3_mass")
    x=sequence[:128].to(next(model.parameters()).device)[None].repeat(6,1)
    logits=model(x,use_cache=False,logits_to_keep=1).logits[:,-1].float()
    stats=finish(model.config.num_hidden_layers)
    if not bool(torch.isfinite(logits).all()):raise RuntimeError("Nonfinite logits")
    return logits,stats

def cpu_checks():
    started=time.perf_counter();tested=0;maxerror=0.
    for dtype in [torch.float32,torch.bfloat16]:
        for q,k in [(8,8),(1,9),(3,9)]:
            support=p2.causal_support(q,k,"cpu")
            gen=torch.Generator().manual_seed(0)
            a=torch.rand((1,2,q,k),generator=gen)*support
            a=(a/a.sum(-1,keepdim=True)).to(dtype)
            b=a.flip(1).contiguous();order=random_order("unit",0,2,q,k,"cpu")
            for beta in [0.,.25,1.]:
                stats=Checks();s,c,budget=matched_edit(a,b,beta,order,stats);stats.finalize("CPU matching")
                maxerror=max(maxerror,stats["max_mass_match_error"])
                if beta==1.:
                    assert torch.equal(s,a.double()) and torch.equal(c,b.double())
                else:
                    assert torch.equal(c[...,0],b[...,0].double())
                if q==k:assert torch.equal(s[...,0,:],a[...,0,:].double())
                tested+=1
    for kind in ["only_sink","only_diagonal"]:
        a=torch.zeros(1,2,8,8)
        if kind=="only_sink":a[...,0]=1
        else:a+=torch.eye(8)
        stats=Checks();s,c,q=matched_edit(a,a,0.,random_order(kind,0,2,8,8,"cpu"),stats);stats.finalize(kind)
        assert torch.equal(s,a.double()) and torch.equal(c,a.double()) and not bool(q.any())
        tested+=1
    result={"all_passed":True,"n_cases":tested,"max_mass_match_error":maxerror,
        "budget_rule":"min((1-beta)*sink_sinkarm, nonsink_sinkarm, nonsink_controlarm); first absolute row q=0",
        "elapsed_seconds":time.perf_counter()-started}
    write_json_new("out/phase37_mass_matched_checks_v3.json",result)
    progress("V3 matched CPU checks",f"{tested} cases; exact mass construction, q0 identity, nonnegative and cached offsets",result["elapsed_seconds"])
    print(result,flush=True)

@torch.inference_mode()
def pilot(model,model_name,corpus):
    path=Path(f"out/phase7_massmatched_pilot_{slug(model_name)}_v3.json")
    if path.exists():
        result=json.loads(path.read_text(encoding="utf-8"))
        assert result["source_hashes"]==hashes() and result["corpus_sha256"]==sha256_file(CORPUS_PATH)
        return result
    doc=corpus["documents"][0]["doc_id"]
    seq=torch.tensor(corpus["models"][model_name]["documents"][0]["token_ids"])
    x=seq[:128].to(next(model.parameters()).device)[None].repeat(6,1)
    model.set_attn_implementation("eager");native=model(x,use_cache=False,logits_to_keep=1).logits[:,-1].float()
    identity,_=forward(model,seq,"identity",doc,disable=True)
    assert torch.equal(native,identity),"Identity callback changed vanilla logits"
    AttentionInterface.register("revision_v3_old_anova",p7.recon_attention_forward)
    p7.RECON.update(mode="anova",k=8,stats=Checks(),empty_row_policy="uniform",svd_driver=None,parallel_svd=False)
    model.set_attn_implementation("revision_v3_old_anova")
    original=model(x,use_cache=False,logits_to_keep=1).logits[:,-1].float();p7.RECON["stats"].finalize("old ANOVA baseline")
    reproduced,_=forward(model,seq,"anova",doc,disable=True)
    assert torch.equal(original,reproduced),"New adapter changed the shared ANOVA baseline"
    torch.cuda.synchronize();start=time.perf_counter()
    sequential,stats_seq=forward(model,seq,"anova",doc,parallel=False)
    torch.cuda.synchronize();seq_seconds=time.perf_counter()-start
    start=time.perf_counter();candidate,stats_par=forward(model,seq,"anova",doc,parallel=True)
    torch.cuda.synchronize();par_seconds=time.perf_counter()-start
    same=torch.equal(sequential,candidate) and stats_seq==stats_par
    parallel=same and par_seconds<=.9*seq_seconds
    changed=seq.clone();changed[128:]=changed[128:].flip(0)
    suffix={}
    for context in CONTEXTS:
        a,_=forward(model,seq,context,doc,parallel)
        b,_=forward(model,changed,context,doc,parallel)
        assert torch.equal(a,b),"Suffix changed an evaluated prefix"
        suffix[context]={"n_roles":6,"max_logit_difference":0.,"passed":True}
    result={"model":model_name,"corpus_sha256":sha256_file(CORPUS_PATH),"source_hashes":hashes(),
        "source_code":{p:Path(p).read_text(encoding="utf-8") for p in hashes()},
        "native_identity_bit_equal":True,"old_anova_baseline_bit_equal":True,
        "parallel_selected":parallel,"parallel_all_logits_and_counters_exact":same,
        "sequential_seconds":seq_seconds,"parallel_seconds":par_seconds,"suffix_checks":suffix,
        "driver":None,"rank":8,"source_precision":"float32 full exact SVD"}
    write_json_new(path,result)
    progress("V3 matched pilot",f"{model_name}; native/ANOVA/suffix passed; parallel={parallel}, exact={same}")
    return result

@torch.inference_mode()
def run_chunk(model_name,start,stop):
    if not 0<=start<stop<=256:raise ValueError("Chunk must lie in the fixed 256-document corpus")
    began=time.perf_counter();corpus=json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    tag=f"phase7_massmatched_{slug(model_name)}_d{start:03d}_{stop:03d}_v3"
    output=Path("out")/(tag+".json");pairs=Path("out/pairs")/(tag+".jsonl")
    if output.exists():
        result=json.loads(output.read_text(encoding="utf-8"))
        assert result["source_hashes"]==hashes() and result["pairs_sha256"]==sha256_file(pairs)
        return result
    dtype=torch.bfloat16 if "Qwen" in model_name else torch.float32
    model=AutoModelForCausalLM.from_pretrained(model_name,revision=corpus["models"][model_name]["revision"],
        dtype=dtype,attn_implementation="eager",local_files_only=True).to("cuda").eval()
    AttentionInterface.register("revision_v3_mass",attention_forward)
    proof=pilot(model,model_name,corpus);parallel=proof["parallel_selected"]
    existing=[]
    if pairs.exists():existing=[json.loads(s) for s in pairs.read_text(encoding="utf-8").splitlines()]
    seen={r["document_index"] for r in existing}
    for d in seen:
        rows=[r for r in existing if r["document_index"]==d]
        assert len(rows)==12 and len({(r["context"],r["arm"]) for r in rows})==12
    pairs.parent.mkdir(parents=True,exist_ok=True)
    with pairs.open("a",encoding="utf-8") as f:
        for di in range(start,stop):
            if di in seen:continue
            seq=torch.tensor(corpus["models"][model_name]["documents"][di]["token_ids"])
            target=seq[128:129].repeat(6)
            doc=corpus["documents"][di]["doc_id"]
            model.set_attn_implementation("eager")
            x=seq[:128].to(next(model.parameters()).device)[None].repeat(6,1)
            ref=model(x,use_cache=False,logits_to_keep=1).logits[:,-1].float();del x
            rows=[]
            for context in CONTEXTS:
                logits,checks=forward(model,seq,context,doc,parallel)
                if context=="identity":assert torch.equal(logits[0],ref[0]),"Identity KL must be exactly zero"
                kl,nll=p2.kl_nll(ref,logits,target)
                context_ref=logits[0:1].expand_as(logits)
                contextual,_=p2.kl_nll(context_ref,logits,target)
                _,ref_nll=p2.kl_nll(ref,ref,target)
                for i,role in enumerate(ROLES):
                    beta=0. if "beta0_" in role else (.25 if "beta0.25_" in role else None)
                    mass=checks["mass"].get(str(beta)) if beta is not None else None
                    row={"model":model_name,"document_index":di,"doc_id":doc,"context":context,
                        "arm":role,"beta_nominal":beta,"target_id":int(seq[128]),"prefix_length":128,
                        "kl_true":float(kl[i]),"kl_context":float(contextual[i]),"nll":float(nll[i]),
                        "reference_nll":float(ref_nll[i]),"context_reference_nll":float(nll[0]),
                        "base_validation":checks["base"][i],"edit_validation":checks["edit"][i],
                        "combined_sanity_passed":True,"mass":mass,"parallel_svd":parallel}
                    rows.append(row)
            assert len(rows)==12
            f.write("".join(json.dumps(r,allow_nan=False)+"\n" for r in rows));f.flush();existing+=rows
            print(f"MATCHED {model_name}: doc {di+1}/256, elapsed={time.perf_counter()-began:.1f}s",flush=True)
    assert len(existing)==(stop-start)*12
    del model;gc.collect();torch.cuda.empty_cache()
    result={"model":model_name,"start":start,"stop":stop,"n_documents":stop-start,"n_raw_records":len(existing),
        "dtype":str(dtype),"source_hashes":hashes(),"corpus_sha256":sha256_file(CORPUS_PATH),
        "pairs_path":pairs.as_posix(),"pairs_sha256":sha256_file(pairs),"pilot_path":f"out/phase7_massmatched_pilot_{slug(model_name)}_v3.json",
        "six_copies_are_not_independent_items":True,"elapsed_seconds":time.perf_counter()-began}
    write_json_new(output,result)
    progress("V3 matched chunk",f"{model_name}; articles {start}:{stop}, all twelve arms retained",result["elapsed_seconds"],
        f"flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model {model_name} --start {start} --stop {stop}")
    return result

def aggregate():
    began=time.perf_counter();corpus=json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    docs=[d["doc_id"] for d in corpus["documents"]];results={};family=[];pvalues=[]
    for model in MODELS:
        chunks=[];rows=[]
        pilot_meta=json.loads(Path(f"out/phase7_massmatched_pilot_{slug(model)}_v3.json").read_text(encoding="utf-8"))
        execution_hashes=pilot_meta["source_hashes"]
        for start in range(0,256,16):
            path=Path(f"out/phase7_massmatched_{slug(model)}_d{start:03d}_{start+16:03d}_v3.json")
            meta=json.loads(path.read_text(encoding="utf-8"))
            assert meta["source_hashes"]==execution_hashes and meta["pairs_sha256"]==sha256_file(meta["pairs_path"])
            rows.extend(json.loads(s) for s in Path(meta["pairs_path"]).read_text(encoding="utf-8").splitlines());chunks.append(str(path))
        assert len(rows)==256*12 and len({(r["document_index"],r["context"],r["arm"]) for r in rows})==len(rows)
        contexts={}
        for context in CONTEXTS:
            arms={}
            for role in ROLES:
                selected=sorted((r for r in rows if r["context"]==context and r["arm"]==role),key=lambda r:r["document_index"])
                assert [r["doc_id"] for r in selected]==docs
                assert all(r["target_id"]==corpus["models"][model]["documents"][i]["token_ids"][128] for i,r in enumerate(selected))
                item={"n_documents":256,"kl_true":describe([r["kl_true"] for r in selected],np.arange(256)),
                    "kl_context":describe([r["kl_context"] for r in selected],np.arange(256)),
                    "mean_nll_secondary":float(np.mean([r["nll"] for r in selected]))}
                if selected[0]["mass"] is not None:
                    masses=[r["mass"] for r in selected]
                    defined=[i for i,m in enumerate(masses) if m["mass_requested"]>0]
                    item["matching"]={"per_article_fraction":describe([masses[i]["mass_removed_each_arm"]/masses[i]["mass_requested"] for i in defined],defined,document_universe=np.arange(256)),
                        "n_articles_with_no_requested_mass":256-len(defined),
                        "total_requested":sum(m["mass_requested"] for m in masses),
                        "total_removed_each_arm":sum(m["mass_removed_each_arm"] for m in masses),
                        "rows_total":sum(m["mass_rows_total"] for m in masses),
                        "rows_capped":sum(m["mass_rows_capped"] for m in masses),
                        "last_query_requested":sum(m["last_query_mass_requested"] for m in masses),
                        "last_query_removed_each_arm":sum(m["last_query_mass_removed_each_arm"] for m in masses),
                        "max_mass_match_error":max(m["max_mass_match_error"] for m in masses)}
                arms[role]=item
            tests={}
            for beta in [0.,.25]:
                label="beta0" if beta==0 else "beta0.25"
                sink={r["document_index"]:r for r in rows if r["context"]==context and r["arm"]=="sink_"+label+"_matched"}
                control={r["document_index"]:r for r in rows if r["context"]==context and r["arm"]=="control_"+label+"_matched"}
                assert set(sink)==set(control)==set(range(256))
                assert all(sink[i]["mass"]==control[i]["mass"] for i in range(256))
                delta=[sink[i]["kl_true"]-control[i]["kl_true"] for i in range(256)]
                test=paired_wilcoxon(delta,np.arange(256))
                test["context_reference_difference_descriptive"]=describe([sink[i]["kl_context"]-control[i]["kl_context"] for i in range(256)],np.arange(256))
                tests[str(beta)]=test;family.append((model,context,str(beta)));pvalues.append(test["pvalue"])
            contexts[context]={"arms":arms,"sink_vs_matched_control":tests}
        results[model]={"contexts":contexts,"chunk_results":chunks,"n_raw_records":len(rows),"inference_source_hashes":execution_hashes}
    adjusted=holm(pvalues)
    for i,(m,c,b) in enumerate(family):results[m]["contexts"][c]["sink_vs_matched_control"][b]["p_holm_24_comparisons"]=adjusted[i]
    result={"_meta":{"schema_version":3,"n_documents_per_model":256,"prefix_length":128,"rank_anova":8,
        "primary_holm_family":[list(k) for k in family],"primary_test":"paired article Wilcoxon; difference KL_true(sink)-KL_true(control)",
        "budget_rule":"q=min((1-beta)*sink_mass_sinkarm, nonsink_mass_sinkarm, nonsink_mass_controlarm); absolute first row q=0",
        "randomization":"one seed0 hash per article and layer, shared across contexts/betas; random nonsink column ordering",
        "interpretation":"Beta is nominal and capped for feasibility; this is not the uncapped full-removal beta0 test",
        "contexts":"true attention and normalized ANOVA+rank8; KL against native and unedited context distributions both reported",
        "all_arms_use_same_documents":True,"source_hashes":hashes(),"corpus_sha256":sha256_file(CORPUS_PATH),
        "elapsed_seconds":time.perf_counter()-began},"models":results}
    write_json_new("out/phase7_editability_v3.json",result)
    progress("V3 matched complete","six models x 256 articles x twelve arms; Holm24, exact feasible mass equality",result["_meta"]["elapsed_seconds"])

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--cpu-checks",action="store_true");ap.add_argument("--aggregate-only",action="store_true")
    ap.add_argument("--model",choices=MODELS);ap.add_argument("--start",type=int);ap.add_argument("--stop",type=int)
    args=ap.parse_args()
    if args.cpu_checks:cpu_checks();return
    if args.aggregate_only:aggregate();return
    if args.model is None or args.start is None or args.stop is None:ap.error("GPU chunk requires model/start/stop")
    run_chunk(args.model,args.start,args.stop)

if __name__=="__main__":main()
