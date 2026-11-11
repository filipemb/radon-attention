"""Frozen historical item generators and GPU-only inference jobs for revision v3."""
from revision_v3_stats import (MODELS,CORPUS_PATH,slug,sha256_file,write_json_new,progress)
import gc
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
import numpy as np
import torch
from transformers import AutoTokenizer,AutoConfig,AutoModelForCausalLM,AttentionInterface
import phase8_lostmiddle as p8
import phase11_kv as p11
import phase16_longcontext as p16
import phase18_betacv as p18
import phase28_beta0_retest as old_diagnostic
from phase2_downstream import DeferredStats

torch.set_num_threads(4)
PROBE_MODELS=MODELS[:5]
KV_MODELS=["gpt2-medium","Qwen/Qwen2.5-3B"]
SEEDS=[0,1,2]
GRID=[1.,.75,.5,.35,.25,.15,.10,.05,0.]
DATA=Path("data/attn")

def source_hashes():
    return {p:sha256_file(p) for p in ["phase8_lostmiddle.py","phase11_kv.py","phase16_longcontext.py",
        "phase18_betacv.py","phase2_downstream.py","revision_v3_probes.py"]}

def paths(task,model,seed):
    stem=DATA/f"{task}_items_{slug(model)}_s{seed}_v3"
    return Path(str(stem)+".npz"),Path(str(stem)+".manifest.json")

def payload_hash(arrays):
    h=hashlib.sha256()
    for key in sorted(arrays):
        a=np.ascontiguousarray(arrays[key],dtype=np.int64)
        h.update(key.encode());h.update(str(a.shape).encode());h.update(a.tobytes())
    return h.hexdigest()

def publish_arrays(path,arrays):
    if path.exists():
        with np.load(path,allow_pickle=False) as z:
            assert set(z.files)==set(arrays)
            assert all(np.array_equal(z[k],arrays[k]) for k in arrays)
        return
    fd,temp=tempfile.mkstemp(dir=path.parent,prefix="."+path.name+".",suffix=".tmp")
    temporary=Path(temp)
    try:
        with os.fdopen(fd,"wb") as f:
            np.savez_compressed(f,**arrays);f.flush();os.fsync(f.fileno())
        os.link(temporary,path)
    finally:temporary.unlink(missing_ok=True)

def flatten(probe,positions,npp,suffix=""):
    return {"input_ids"+suffix:np.concatenate([probe[p][0].numpy() for p in positions]).astype(np.int64),
        "targets"+suffix:np.concatenate([probe[p][1].numpy() for p in positions]).astype(np.int64),
        "positions"+suffix:np.repeat(positions,npp).astype(np.int64),
        "item_index"+suffix:np.tile(np.arange(npp),len(positions)).astype(np.int64)}

def save_probe(task,model,seed,arrays,extra):
    archive,manifest=paths(task,model,seed);revision=json.loads(CORPUS_PATH.read_text(encoding="utf-8"))["models"][model]["revision"]
    digest=payload_hash(arrays)
    if manifest.exists():
        meta=json.loads(manifest.read_text(encoding="utf-8"))
        assert meta["payload_sha256"]==digest and meta["npz_sha256"]==sha256_file(archive)
        return
    publish_arrays(archive,arrays)
    write_json_new(manifest,{"schema_version":3,"task":task,"model":model,"seed":seed,"revision":revision,
        "payload_sha256":digest,"npz_sha256":sha256_file(archive),"source_hashes":source_hashes(),
        "filler_text_sha256":sha256_file("wikitext2_train.txt"),"sampling_unit":"synthetic item; filler windows may overlap",
        "target_evaluation":"last query token only; target is the planted past value, not appended after the query",**extra})

def prepare():
    started=time.perf_counter();corpus=json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    tokenizers={m:AutoTokenizer.from_pretrained(m,revision=corpus["models"][m]["revision"],local_files_only=True) for m in MODELS}
    configs={m:AutoConfig.from_pretrained(m,revision=corpus["models"][m]["revision"],local_files_only=True) for m in MODELS}
    for task,models,n,npp in [("phase8",PROBE_MODELS,128,400),("phase11",KV_MODELS,256,200)]:
        for seed in SEEDS:
            rng=np.random.default_rng(seed)
            historical=Path(f"out/{'phase8_lostmiddle' if task=='phase8' else 'phase11_kv'}_s{seed}.json")
            old=json.loads(historical.read_text(encoding="utf-8"));assert [k for k in old if k!="_meta"]==models
            for model in models:
                positions=old[model]["positions"]
                pool=p8.filler_pool(tokenizers[model],npp*n*4,seed)
                built=(p8.build_probe(pool,configs[model].vocab_size,n,positions,npp,rng) if task=="phase8"
                       else p11.build_kv(pool,configs[model].vocab_size,n,positions,npp,rng))
                arrays=flatten(built,positions,npp)
                if task=="phase8" and seed==0:
                    legacy=Path(f"data/attn/beta0_probe_{slug(model)}_s0_v2.npz")
                    with np.load(legacy,allow_pickle=False) as z:
                        assert all(np.array_equal(arrays[k],z[k]) for k in ["input_ids","targets","positions"])
                save_probe(task,model,seed,arrays,{"n":n,"n_per_position":npp,"positions":positions,
                    "n_items":len(arrays["targets"]),"historical_source":historical.as_posix(),
                    "historical_sha256":sha256_file(historical),"rng_rule":"one shared default_rng(seed) consumed in historical model order",
                    "historical_model_order":models,"middle_rule":"0.25*n <= position <= 0.75*n"})
    for model in PROBE_MODELS:
        for seed in SEEDS:
            oldpath=Path(f"out/phase18_betacv_s{seed}.json");old=json.loads(oldpath.read_text(encoding="utf-8"));meta=old["_meta"]
            assert meta["betas"]==GRID and meta["n_per_pos"]==150
            nA,nB,npp=meta["nA"],meta["nB"],meta["n_per_pos"]
            needA,needB=npp*nA*4,npp*nB*4
            pool=p8.filler_pool(tokenizers[model],needA+needB+64,seed)
            posA=old[model]["posA"];posB=old[model]["posB"]
            a=p8.build_probe(pool[:needA],configs[model].vocab_size,nA,posA,npp,np.random.default_rng(seed))
            b=p16.build_kv(pool[needA:],configs[model].vocab_size,nB,posB,npp,p16.make_keys(8),np.random.default_rng(seed+12345))
            arrays={**flatten(a,posA,npp,"_A"),**flatten(b,posB,npp,"_B")}
            save_probe("phase18",model,seed,arrays,{"nA":nA,"nB":nB,"n_per_position":npp,"grid":GRID,
                "positions_A":posA,"positions_B":posB,"n_items_A":len(arrays["targets_A"]),"n_items_B":len(arrays["targets_B"]),
                "historical_source":oldpath.as_posix(),"historical_sha256":sha256_file(oldpath),
                "source_pool_split_token":needA,"poolA_tokens":needA,"poolB_tokens":len(pool)-needA,
                "rng_rule":"independent RNG seed for A, seed+12345 for B, reset per model; disjoint filler slices",
                "selection_rule":"historical mean accuracy in mid(): .25*positions[-1] <= p <= .75*positions[-1]; first grid entry wins ties"})
    progress("V3 frozen probes","21 phase8/KV datasets and 15 two-family CV datasets; all seeds/models, seed0 matches v2 arrays exactly",time.perf_counter()-started,
             ".venv/Scripts/python.exe -B phase38_paired_items.py --prepare-only")
    print(f"Frozen v3 probes in {time.perf_counter()-started:.3f}s",flush=True)

def load_probe(task,model,seed):
    archive,manifest=paths(task,model,seed);meta=json.loads(manifest.read_text(encoding="utf-8"))
    assert meta["npz_sha256"]==sha256_file(archive)
    with np.load(archive,allow_pickle=False) as z:arrays={k:z[k].copy() for k in z.files}
    assert payload_hash(arrays)==meta["payload_sha256"]
    return arrays,meta

def dtype_for(task,model,variant):
    if variant=="standard_bf16":
        if model!="Qwen/Qwen2.5-0.5B":raise ValueError("Only the historical fp32 Qwen0.5 needs this supplement")
        return torch.bfloat16
    if variant!="historical":raise ValueError(variant)
    return torch.bfloat16 if model=="Qwen/Qwen2.5-3B" else torch.float32

@torch.inference_mode()
def run_job(task,model,seed,variant="historical"):
    started=time.perf_counter();tag=f"{task}_items_{slug(model)}_s{seed}_{variant}_v3"
    output=Path("out")/(tag+".json");pairpath=Path("out/pairs")/(tag+".jsonl")
    arrays,meta=load_probe(task,model,seed);dtype=dtype_for(task,model,variant)
    hashes=source_hashes()
    if output.exists():
        r=json.loads(output.read_text(encoding="utf-8"));assert r["payload_sha256"]==meta["payload_sha256"] and r["source_hashes"]==hashes
        return r
    model_obj=AutoModelForCausalLM.from_pretrained(model,revision=meta["revision"],dtype=dtype,
        attn_implementation="eager",local_files_only=True).to("cuda").eval()
    AttentionInterface.register("revision_v3_sink",p8.recon_attention_forward)
    AttentionInterface.register("revision_v3_legacy",old_diagnostic.legacy_attention_forward)
    families=["A","B"] if task=="phase18" else [""]
    batch=16 if task=="phase8" else (4 if model=="Qwen/Qwen2.5-3B" else 8)
    sample=arrays["input_ids_A" if task=="phase18" else "input_ids"][:2]
    x=torch.tensor(sample,device="cuda")
    # Reproduce full historical LM-head shape, not logits_to_keep=1.
    native=model_obj(x).logits[:,-1,:].clone()
    model_obj.set_attn_implementation("revision_v3_sink");p8.RECON.update(beta=1.,stats=DeferredStats())
    identity=model_obj(x).logits[:,-1,:].clone();p8.RECON["stats"].finalize("v3 native identity")
    assert torch.equal(native,identity),"Historical callback beta1 must equal vanilla eager logits"
    del native,identity,x
    records=[]
    if pairpath.exists():
        records=[json.loads(s) for s in pairpath.read_text(encoding="utf-8").splitlines()]
        assert all(r["payload_sha256"]==meta["payload_sha256"] and r["variant"]==variant and r["batch_requested"]==batch for r in records)
    seen={(r["family"],r["arm"],r["trial_id"]) for r in records};assert len(seen)==len(records)
    if task=="phase18":arms=[(str(b),b,False) for b in GRID]+[("legacy_beta0",0.,True)]
    else:arms=[("1.0",1.,False),("0.25",.25,False)]
    pairpath.parent.mkdir(parents=True,exist_ok=True)
    with pairpath.open("a",encoding="utf-8") as f:
        for family in families:
            suffix="_"+family if family else ""
            ids,targets,positions,items=[arrays[k+suffix] for k in ["input_ids","targets","positions","item_index"]]
            for arm,beta,legacy in arms:
                for start in range(0,len(ids),batch):
                    stop=min(start+batch,len(ids))
                    if all((family,arm,i) in seen for i in range(start,stop)):continue
                    stats=DeferredStats()
                    if legacy:
                        model_obj.set_attn_implementation("revision_v3_legacy");old_diagnostic.LEGACY.update(beta=beta,stats=stats)
                    else:
                        model_obj.set_attn_implementation("revision_v3_sink");p8.RECON.update(beta=beta,stats=stats)
                    x=torch.tensor(ids[start:stop],device="cuda")
                    outputs=model_obj(x);scores=outputs.logits[:,-1,:]
                    if not bool(torch.isfinite(scores).all()):raise RuntimeError("Nonfinite logits; no dropped item or replacement")
                    stats.finalize(f"{task} {model} seed{seed} {family} {arm} {start}:{stop}")
                    pred=scores.argmax(-1).cpu().numpy();del outputs,scores,x
                    for j,i in enumerate(range(start,stop)):
                        if (family,arm,i) in seen:continue
                        row={"model":model,"seed":seed,"family":family,"arm":arm,"beta":beta,
                            "legacy_invalid_diagnostic":legacy,"variant":variant,"dtype":str(dtype),
                            "position":int(positions[i]),"item":int(items[i]),"trial_id":i,
                            "target_id":int(targets[i]),"prediction_id":int(pred[j]),"correct":bool(pred[j]==targets[i]),
                            "payload_sha256":meta["payload_sha256"],"batch_start":start,"batch_size":stop-start,
                            "batch_requested":batch,"attention_validation_batch":dict(stats)}
                        f.write(json.dumps(row,allow_nan=False)+"\n");records.append(row);seen.add((family,arm,i))
                    f.flush()
                print(f"ITEMS {task} {model} s{seed} {variant} family={family} arm={arm}: {len(ids)} items, {time.perf_counter()-started:.1f}s",flush=True)
    # CPU bootstraps run in a separate command after this locked GPU job exits.
    del model_obj;gc.collect();torch.cuda.empty_cache()
    expected=sum(meta.get("n_items_"+a,0) for a in ["A","B"]) if task=="phase18" else meta["n_items"]
    assert len(records)==expected*len(arms)
    result={"schema_version":3,"task":task,"model":model,"seed":seed,"variant":variant,"dtype":str(dtype),
        "batch":batch,"revision":meta["revision"],"source_hashes":hashes,"payload_sha256":meta["payload_sha256"],
        "manifest_path":paths(task,model,seed)[1].as_posix(),"pairs_path":pairpath.as_posix(),"pairs_sha256":sha256_file(pairpath),
        "n_raw_records":len(records),"native_identity_logits_bit_equal":True,
        "lm_head":"full historical output; evaluate last query token; no KV reuse between items",
        "elapsed_seconds":time.perf_counter()-started}
    write_json_new(output,result)
    progress("V3 items GPU",f"{task} {model} s{seed} {variant}; {len(records)} records, no item omitted",result["elapsed_seconds"])
    return result
