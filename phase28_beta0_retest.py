"""P0: repeat only the five-model beta=0 retrieval claim, on frozen probes.

Prepare on CPU, then run each --models job under the shared flock. The legacy
beta=0 arm is explicitly an invalid-attention diagnostic, never a repaired run.
All outputs are exclusive versioned files; completed raw batches are resumable.
"""
from sampling import (MODELS, CORPUS_PATH, DATA_ROOT, slug, sha256_file,
                      write_json_new, progress)
import argparse
import gc
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import binomtest
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM, AttentionInterface
import phase8_lostmiddle as p8
from phase2_downstream import DeferredStats

torch.set_num_threads(4)
PROBE_MODELS = MODELS[:5]
POSITIONS = [4, 16, 32, 48, 64, 80, 96, 110]
N, N_PER_POS, SEED = 128, 400, 0
ARMS = ("baseline_beta1", "corrected_beta0", "legacy_beta0_diagnostic")
LEGACY = {"beta": 0., "stats": {}}
HISTORICAL = Path("out/phase8_lostmiddle_s0.json")

def probe_paths(name):
    stem = DATA_ROOT / f"beta0_probe_{slug(name)}_s0_v2"
    return Path(str(stem)+".npz"), Path(str(stem)+".manifest.json")

def digest_arrays(ids, targets, positions):
    h = hashlib.sha256()
    for a in (ids, targets, positions):
        h.update(np.ascontiguousarray(a, dtype=np.int64).tobytes())
    return h.hexdigest()

def prepare_probes():
    started = time.perf_counter()
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    old = json.loads(HISTORICAL.read_text(encoding="utf-8"))
    assert list(k for k in old if k != "_meta") == PROBE_MODELS
    assert old["_meta"] == {"n_per_pos":400, "seed":0,
                              "betas":[1., .5, .25, 0.], "seq_len":128}
    rng = np.random.default_rng(SEED)  # shared across models, exactly as phase8
    for name in PROBE_MODELS:
        revision = corpus["models"][name]["revision"]
        tok = AutoTokenizer.from_pretrained(name, revision=revision, local_files_only=True)
        cfg = AutoConfig.from_pretrained(name, revision=revision, local_files_only=True)
        pool = p8.filler_pool(tok, N_PER_POS*N*4, SEED)
        built = p8.build_probe(pool, cfg.vocab_size, N, POSITIONS, N_PER_POS, rng)
        ids = np.concatenate([built[p][0].numpy() for p in POSITIONS]).astype(np.int64)
        targets = np.concatenate([built[p][1].numpy() for p in POSITIONS]).astype(np.int64)
        positions = np.repeat(POSITIONS, N_PER_POS).astype(np.int64)
        assert ids.shape == (3200,128) and targets.shape == positions.shape == (3200,)
        assert ids.min() >= 0 and ids.max() < cfg.vocab_size
        assert np.all(ids[:, -len(p8.TAG):] == np.array(p8.TAG))
        for i,p in enumerate(positions):
            assert ids[i,p+len(p8.TAG)] == targets[i]
        payload_hash = digest_arrays(ids, targets, positions)
        archive, manifest_path = probe_paths(name)
        if archive.exists() or manifest_path.exists():
            if not (archive.exists() and manifest_path.exists()):
                raise RuntimeError("Incomplete immutable probe artifact")
            meta = json.loads(manifest_path.read_text(encoding="utf-8"))
            assert meta["payload_sha256"] == payload_hash
            assert meta["npz_sha256"] == sha256_file(archive)
        else:
            with archive.open("xb") as f:
                np.savez_compressed(f, input_ids=ids, targets=targets, positions=positions)
            write_json_new(manifest_path, {
                "schema_version":2,"model":name,"revision":revision,"seed":SEED,
                "sequence_length":N,"positions":POSITIONS,"n_per_position":N_PER_POS,
                "n_trials_effective":3200,"n_evaluated_next_tokens_per_arm":3200,
                "n_source_documents":None,"sampling_unit":"synthetic probe trial; text windows may overlap",
                "generator":"unchanged phase8.build_probe; one shared default_rng(0) consumed in historical five-model order",
                "tag":p8.TAG,"target_tokens":1,"known_query_key_tokens":len(p8.TAG),
                "filler_pool_tokens":len(pool),"filler_text_sha256":sha256_file("wikitext2_train.txt"),
                "historical_output":HISTORICAL.as_posix(),"historical_output_sha256":sha256_file(HISTORICAL),
                "payload_sha256":payload_hash,"npz_sha256":sha256_file(archive),
                "middle_positions":[p for p in POSITIONS if .25*N <= p <= .75*N],
                "completion_rule":"preserve pre-edit row iff the edit leaves exactly zero alternative mass",
                "positive_tiny_mass":"normalize by its positive total; historical denominator floor is not used",
                "claim_assessment":"report absolute and relative accuracy losses; no outcome-fitted collapse threshold"})
        print(f"Frozen {name}: {len(ids)} trials, payload {payload_hash}", flush=True)
    progress("V1 beta0 probes", "Five immutable probes; 3200 trials each; historical shared RNG order, no sample cut",
             time.perf_counter()-started,".venv/Scripts/python.exe -B phase28_beta0_retest.py --prepare-only")

def legacy_attention_forward(module, query, key, value, attention_mask, scaling=None, dropout=0., **kwargs):
    """Exact old phase8 arithmetic, intentionally permitting zero rows."""
    nrep = getattr(module,"num_key_value_groups",1)
    key, value = p8._repeat_kv(key,nrep), p8._repeat_kv(value,nrep)
    aw = (query @ key.transpose(-1,-2)) * (query.size(-1)**-.5 if scaling is None else scaling)
    q,k = aw.shape[-2:]
    causal = torch.full((q,k),float("-inf"),device=aw.device,dtype=aw.dtype)
    aw = F.softmax(aw+torch.triu(causal,diagonal=1+k-q),dim=-1).type(value.dtype)
    beta = LEGACY["beta"]
    if beta != 1.:
        aw = aw.clone()
        aw[...,0] *= beta
        sums = aw.sum(-1,keepdim=True)
        stats = LEGACY["stats"]
        stats["rows_total"] = stats.get("rows_total",0)+aw.numel()//k
        deferred = getattr(stats,"defer_validation",False)
        counts={"zero_rows":(sums==0).sum(),"zero_rows_at_last_query":(sums[...,-1,:]==0).sum(),
                "positive_mass_below_clamp":((sums>0)&(sums<1e-9)).sum()}
        for label,count in counts.items():
            stats[label]=stats.get(label,0)+(count if deferred else int(count))
        aw = aw / sums.clamp_min(1e-9)
    return (aw @ value).transpose(1,2),aw

def merge_stats(dest,other):
    for key,value in other.items():
        dest[key] = max(dest.get(key,0),value) if key.startswith("max_") else dest.get(key,0)+value

def summary(records):
    correct = np.array([r["correct"] for r in records])
    positions = np.array([r["position"] for r in records])
    middle = (positions>=.25*N)&(positions<=.75*N)
    assert len(records)==3200 and int(middle.sum())==2000
    return {"n_trials":len(records),"n_correct":int(correct.sum()),"accuracy":float(correct.mean()),
            "middle_n_trials":int(middle.sum()),"middle_n_correct":int(correct[middle].sum()),
            "middle_accuracy":float(correct[middle].mean()),
            "accuracy_by_position":{str(p):float(correct[positions==p].mean()) for p in POSITIONS}}

def paired_difference(rows, left, right):
    by = {a:{r["trial_id"]:r for r in rows if r["arm"]==a} for a in (left,right)}
    assert set(by[left])==set(by[right]) and len(by[left])==3200
    better = sum(by[left][i]["correct"] and not by[right][i]["correct"] for i in by[left])
    worse = sum(by[right][i]["correct"] and not by[left][i]["correct"] for i in by[left])
    return {"left":left,"right":right,"n_pairs":3200,"left_only_correct":better,
            "right_only_correct":worse,"accuracy_difference_left_minus_right":(better-worse)/3200,
            "mcnemar_exact_pvalue":float(binomtest(better,better+worse,.5).pvalue) if better+worse else 1.,
            "inference_scope":"conditional on this seed's synthetic probes; overlapping filler is not independent documents"}

@torch.inference_mode()
def cpu_regression():
    """Check actual pretrained GPT-2 before waiting for the shared GPU."""
    started=time.perf_counter()
    archive,manifest_path=probe_paths("gpt2")
    meta=json.loads(manifest_path.read_text(encoding="utf-8"))
    assert sha256_file(archive)==meta["npz_sha256"]
    with np.load(archive,allow_pickle=False) as z:
        x=torch.tensor(z["input_ids"][:2],device="cpu")
    model=AutoModelForCausalLM.from_pretrained("gpt2",revision=meta["revision"],local_files_only=True,
                                             dtype=torch.float32,attn_implementation="eager").eval()
    assert next(model.parameters()).device.type=="cpu"
    AttentionInterface.register("p0_beta0_corrected",p8.recon_attention_forward)
    AttentionInterface.register("p0_beta0_legacy",legacy_attention_forward)
    native=model(x,use_cache=False,logits_to_keep=1).logits
    p8.RECON.update(beta=1.,stats={});model.set_attn_implementation("p0_beta0_corrected")
    identity=model(x,use_cache=False,logits_to_keep=1).logits
    assert torch.equal(native,identity)
    p8.RECON.update(beta=.25,stats={})
    corrected=model(x,use_cache=False,logits_to_keep=1).logits
    LEGACY.update(beta=.25,stats={});model.set_attn_implementation("p0_beta0_legacy")
    legacy=model(x,use_cache=False,logits_to_keep=1).logits
    assert torch.equal(corrected,legacy)
    result={"model":"gpt2","device":"cpu","dtype":"torch.float32","beta":.25,"n_sequences":2,
            "native_identity_logits_bit_equal":True,"positive_beta_logits_bit_equal":True,
            "max_absolute_logit_difference":float((corrected-legacy).abs().max()),
            "probe_payload_sha256":meta["payload_sha256"],"attention_checks":dict(p8.RECON["stats"]),
            "elapsed_seconds":time.perf_counter()-started}
    write_json_new("out/phase28_positive_beta_cpu_v2.json",result)
    progress("V1 positive beta pretrained regression","GPT-2, beta=.25, two frozen probes, CPU; native identity and old/new positive-beta logits bit equal",
             result["elapsed_seconds"],".venv/Scripts/python.exe -B phase28_beta0_retest.py --cpu-regression-only")
    print(json.dumps(result),flush=True)

@torch.inference_mode()
def run_model(name,batch):
    output = Path("out")/f"phase8_beta0_{slug(name)}_v2.json"
    if output.exists():
        return json.loads(output.read_text(encoding="utf-8"))
    started = time.perf_counter()
    archive, manifest_path = probe_paths(name)
    meta = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert sha256_file(archive)==meta["npz_sha256"]
    with np.load(archive,allow_pickle=False) as z:
        ids,targets,positions = [z[k].copy() for k in ("input_ids","targets","positions")]
    assert digest_arrays(ids,targets,positions)==meta["payload_sha256"]
    dtype = torch.bfloat16 if "Qwen" in name else torch.float32
    model = AutoModelForCausalLM.from_pretrained(name,revision=meta["revision"],local_files_only=True,
                                               attn_implementation="eager",dtype=dtype).to("cuda").eval()
    AttentionInterface.register("p0_beta0_corrected",p8.recon_attention_forward)
    AttentionInterface.register("p0_beta0_legacy",legacy_attention_forward)
    def logits(x):
        result = model(x,use_cache=False,logits_to_keep=1).logits[:,-1]
        if not bool(torch.isfinite(result).all()):
            raise RuntimeError("Nonfinite retrieval logits: no trial is silently replaced or dropped")
        return result
    # Beta=1 must implement the actual eager model, including bf16 Qwen/GQA.
    identity_x = torch.tensor(ids[:2],device="cuda")
    model.set_attn_implementation("eager")
    native_identity = logits(identity_x)
    model.set_attn_implementation("p0_beta0_corrected")
    p8.RECON.update(beta=1.,stats=DeferredStats())
    custom_identity = logits(identity_x)
    p8.RECON["stats"].finalize("beta1 native identity")
    assert torch.equal(native_identity,custom_identity),"Beta=1 callback changed vanilla eager logits"
    identity_regression = {"n_sequences":2,"logits_bit_equal":True,
                           "max_absolute_logit_difference":float((native_identity-custom_identity).abs().max())}
    regression = None
    if name=="gpt2":
        x = torch.tensor(ids[:2],device="cuda")
        LEGACY.update(beta=.25,stats={})
        model.set_attn_implementation("p0_beta0_legacy")
        old = logits(x)
        p8.RECON.update(beta=.25,stats=DeferredStats())
        model.set_attn_implementation("p0_beta0_corrected")
        new = logits(x)
        p8.RECON["stats"].finalize("beta .25 legacy/corrected equivalence")
        assert torch.equal(old,new),"Positive-beta regression changed logits"
        regression = {"model":name,"beta":.25,"n_sequences":2,"logits_bit_equal":True,
                      "max_absolute_logit_difference":float((old-new).abs().max()),
                      "new_attention_checks":dict(p8.RECON["stats"])}
    pairpath = Path("out/pairs")/f"beta0_{slug(name)}_v2.jsonl"
    pairpath.parent.mkdir(parents=True,exist_ok=True)
    rows = []
    if pairpath.exists():
        rows = [json.loads(s) for s in pairpath.read_text(encoding="utf-8").splitlines()]
        assert all(r["probe_payload_sha256"]==meta["payload_sha256"] for r in rows)
        assert all(r["dtype"]==str(dtype) for r in rows)
    seen = {(r["arm"],r["trial_id"]) for r in rows}
    assert len(seen)==len(rows)
    with pairpath.open("a",encoding="utf-8") as f:
        for arm in ARMS:
            for start in range(0,len(ids),batch):
                stop = min(start+batch,len(ids))
                if all((arm,i) in seen for i in range(start,stop)):
                    continue
                if arm=="legacy_beta0_diagnostic":
                    model.set_attn_implementation("p0_beta0_legacy")
                    LEGACY.update(beta=0.,stats=DeferredStats())
                    stats = LEGACY["stats"]
                else:
                    model.set_attn_implementation("p0_beta0_corrected")
                    p8.RECON.update(beta=1. if arm=="baseline_beta1" else 0.,stats=DeferredStats())
                    stats = p8.RECON["stats"]
                x = torch.tensor(ids[start:stop],device="cuda")
                scores = logits(x)
                stats.finalize(context=f"{name} {arm} probes {start}:{stop}")
                pred = scores.argmax(-1).cpu().numpy()
                for j,i in enumerate(range(start,stop)):
                    if (arm,i) in seen:
                        continue
                    row = {"model":name,"arm":arm,"trial_id":i,"position":int(positions[i]),
                           "target_id":int(targets[i]),"prediction_id":int(pred[j]),
                           "correct":bool(pred[j]==targets[i]),"dtype":str(dtype),
                           "probe_payload_sha256":meta["payload_sha256"],
                           "batch_start":start,"batch_size":stop-start,"attention_validation_batch":dict(stats)}
                    f.write(json.dumps(row,allow_nan=False)+"\n")
                    rows.append(row);seen.add((arm,i))
                f.flush()
                if stop%400==0 or stop==len(ids):
                    print(f"BETA0 {name} {arm}: {stop}/{len(ids)}, elapsed={time.perf_counter()-started:.1f}s",flush=True)
    validation = {a:{} for a in ARMS}
    batches = set()
    for row in rows:
        key = (row["arm"],row["batch_start"],row["batch_size"])
        if key not in batches:
            merge_stats(validation[row["arm"]],row["attention_validation_batch"])
            batches.add(key)
    arms = {a:summary([r for r in rows if r["arm"]==a]) for a in ARMS}
    expected_rows = len(ids)*N*model.config.num_hidden_layers*model.config.num_attention_heads
    assert validation["corrected_beta0"]["sink_edit_rows_total"]==expected_rows
    assert validation["legacy_beta0_diagnostic"]["rows_total"]==expected_rows
    old = json.loads(HISTORICAL.read_text(encoding="utf-8"))[name]["acc"]
    mids = [p for p in POSITIONS if .25*N<=p<=.75*N]
    result = {"schema_version":2,"model":name,"dtype":str(dtype),"revision":meta["revision"],
              "n_trials_effective_per_arm":3200,"seed":SEED,"sequence_length":N,"batch":batch,
              "positions":POSITIONS,"n_per_position":N_PER_POS,"middle_positions":mids,
              "probe_manifest":manifest_path.as_posix(),"pairs_path":pairpath.as_posix(),
              "completion_rule":meta["completion_rule"],"positive_tiny_mass":meta["positive_tiny_mass"],
              "validation_schedule":"All row checks on device; synchronize and validate every forward before writing paired trials",
              "arms":arms,"attention_validation":validation,"positive_beta_regression":regression,
              "native_identity_regression":identity_regression,
              "historical_s0":{b:{"accuracy":float(np.mean([old[b][str(p)] for p in POSITIONS])),
                                     "middle_accuracy":float(np.mean([old[b][str(p)] for p in mids]))} for b in ("1.0","0.0")},
              "paired_corrected_vs_baseline":paired_difference(rows,"corrected_beta0","baseline_beta1"),
              "paired_corrected_vs_legacy":paired_difference(rows,"corrected_beta0","legacy_beta0_diagnostic"),
              "elapsed_seconds":time.perf_counter()-started}
    write_json_new(output,result)
    del model
    gc.collect();torch.cuda.empty_cache()
    progress("V1 beta0 model",f"{name}; 3200 matched trials x 3 arms; no trial dropped; checks passed",
             time.perf_counter()-started,"flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B "+" ".join(sys.argv))
    return result

def aggregate():
    results = {m:json.loads((Path("out")/f"phase8_beta0_{slug(m)}_v2.json").read_text(encoding="utf-8")) for m in PROBE_MODELS}
    ps = [(m,results[m]["paired_corrected_vs_baseline"]["mcnemar_exact_pvalue"]) for m in PROBE_MODELS]
    running = 0.
    for rank,(m,p) in enumerate(sorted(ps,key=lambda x:x[1])):
        running = max(running,min(1.,(len(ps)-rank)*p))
        results[m]["paired_corrected_vs_baseline"]["holm_pvalue_five_models"] = running
    output = Path("out/phase8_beta0_v2.json")
    result = {"_meta":{"schema_version":2,"historical_reference":HISTORICAL.as_posix(),"seed":SEED,
                        "n_models":5,"n_trials_per_model_per_arm":3200,"n_trials_total_unique":16000,
                        "conditions":list(ARMS),"no_other_beta_grid_rerun":True,
                        "legacy_condition_is_invalid_attention_diagnostic":True,
                        "all_evaluations_at_last_token":True,"all_trials_retained":True,
                        "positive_beta_regression":results["gpt2"]["positive_beta_regression"]},**results}
    if output.exists():
        raise FileExistsError(output)
    write_json_new(output,result)
    progress("V1 beta0 complete","Five models, 16000 distinct probes, paired baseline/corrected/legacy; aggregate saved")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only",action="store_true")
    ap.add_argument("--aggregate-only",action="store_true")
    ap.add_argument("--cpu-regression-only",action="store_true")
    ap.add_argument("--models",nargs="+",choices=PROBE_MODELS,default=PROBE_MODELS)
    ap.add_argument("--batch",type=int,default=16)
    args = ap.parse_args()
    if args.cpu_regression_only:
        cpu_regression();return
    if args.prepare_only:
        prepare_probes();return
    if args.aggregate_only:
        aggregate();return
    for name in args.models:
        run_model(name,args.batch)
    if args.models==PROBE_MODELS:
        aggregate()

if __name__=="__main__":
    main()
