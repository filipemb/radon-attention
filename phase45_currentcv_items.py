"""Current phase18 protocol, original position batches, explicit legacy counterfactual.

Saved CV family B does not reproduce from the available generator. All numerical
sanities stay strict; the failed historical reproduction is retained as a result,
not silently asserted away. Positive-beta weights are compared with the legacy
harness on every actual item/layer. No parameter/seed search for old aggregates.
"""
from revision_v3_probes import (run_job,load_probe,PROBE_MODELS,SEEDS,GRID,p18,
                                slug,sha256_file,write_json_new,progress)
from revision_v3_stats import bootstrap_item_gains,describe
import argparse
import json
from pathlib import Path
import time
import numpy as np
import gc
import revision_v3_probes as probes

class CVChecks(probes.DeferredStats):
    violation_keys=probes.DeferredStats.violation_keys+("positive_beta_legacy_weight_mismatches",)

def verified_attention_forward(module,query,key,value,attention_mask,scaling=None,dropout=0.,**kwargs):
    result=probes.p8.recon_attention_forward(module,query,key,value,attention_mask,scaling,dropout,**kwargs)
    beta=probes.p8.RECON["beta"]
    if beta>0:
        diagnostic=probes.DeferredStats()
        probes.old_diagnostic.LEGACY.update(beta=beta,stats=diagnostic)
        legacy=probes.old_diagnostic.legacy_attention_forward(module,query,key,value,attention_mask,scaling,dropout,**kwargs)
        stats=probes.p8.RECON["stats"]
        stats.add_scalar("positive_beta_legacy_weight_mismatches",(result[1]!=legacy[1]).sum())
        stats.add_scalar("positive_beta_rows_compared",result[1].numel()//result[1].shape[-1])
    return result

@probes.torch.inference_mode()
def run_beta_job(model_name,seed,variant,arm):
    """One beta, both complete families; release GPU between beta jobs."""
    began=time.perf_counter();legacy=arm=="legacy_beta0"
    if not legacy and arm not in [str(b) for b in GRID]:raise ValueError(arm)
    beta=0. if legacy else float(arm)
    tag=f"phase18_posbatch_items_{slug(model_name)}_s{seed}_{variant}_b{arm}_v3"
    output=Path("out")/(tag+".json");pairs=Path("out/pairs")/(tag+".jsonl")
    arrays,manifest=load_probe("phase18",model_name,seed)
    source=probes.source_hashes()
    source.update({p:sha256_file(p) for p in ["phase45_currentcv_items.py",
        "phase28_beta0_retest.py","revision_v3_stats.py"]})
    if output.exists():
        saved=json.loads(output.read_text(encoding="utf-8"))
        assert saved["payload_sha256"]==manifest["payload_sha256"] and saved["source_hashes"]==source
        return saved
    torch=probes.torch;dtype=probes.dtype_for("phase18",model_name,variant)
    model=probes.AutoModelForCausalLM.from_pretrained(model_name,revision=manifest["revision"],dtype=dtype,
        attn_implementation="eager",local_files_only=True).to("cuda").eval()
    probes.AttentionInterface.register("revision_v3_cv",verified_attention_forward)
    probes.AttentionInterface.register("revision_v3_cv_legacy",probes.old_diagnostic.legacy_attention_forward)
    # A prior beta in the historical loop has already visited the longer B
    # family. Reproduce any length-dependent buffers without retaining a KV cache.
    if arm!="1.0":
        model(torch.tensor(arrays["input_ids_B"][:1],device="cuda"))
    x=torch.tensor(arrays["input_ids_A"][:2],device="cuda")
    model.set_attn_implementation("eager");native=model(x).logits[:,-1,:].clone()
    model.set_attn_implementation("revision_v3_cv");probes.p8.RECON.update(beta=1.,stats=CVChecks())
    identity=model(x).logits[:,-1,:].clone();probes.p8.RECON["stats"].finalize("CV native identity")
    assert torch.equal(native,identity),"CV beta1 changed native logits"
    del x,native,identity
    records=[]
    if pairs.exists():
        records=[json.loads(s) for s in pairs.read_text(encoding="utf-8").splitlines()]
        assert all(r["payload_sha256"]==manifest["payload_sha256"] and r["arm"]==arm for r in records)
    seen={(r["family"],r["trial_id"]) for r in records};assert len(seen)==len(records)
    pairs.parent.mkdir(parents=True,exist_ok=True)
    with pairs.open("a",encoding="utf-8") as f:
        for family in ["A","B"]:
            ids,targets,positions,items=[arrays[k+"_"+family] for k in ["input_ids","targets","positions","item_index"]]
            # Original evaluators reset the last short batch at every position.
            npp=manifest["n_per_position"]
            batches=[(start,min(start+8,(block+1)*npp))
                for block in range(len(manifest["positions_"+family]))
                for start in range(block*npp,(block+1)*npp,8)]
            for start,stop in batches:
                if all((family,i) in seen for i in range(start,stop)):continue
                stats=CVChecks()
                if legacy:
                    model.set_attn_implementation("revision_v3_cv_legacy");probes.old_diagnostic.LEGACY.update(beta=0.,stats=stats)
                else:
                    model.set_attn_implementation("revision_v3_cv");probes.p8.RECON.update(beta=beta,stats=stats)
                x=torch.tensor(ids[start:stop],device="cuda");out=model(x);scores=out.logits[:,-1,:]
                if not bool(torch.isfinite(scores).all()):raise RuntimeError("Nonfinite CV logits; no omitted item")
                stats.finalize(f"CV {model_name} s{seed} {arm} {family} {start}:{stop}")
                pred=scores.argmax(-1).cpu().numpy();del x,out,scores
                for j,i in enumerate(range(start,stop)):
                    if (family,i) in seen:continue
                    row={"model":model_name,"seed":seed,"family":family,"arm":arm,"beta":beta,"variant":variant,
                        "dtype":str(dtype),"legacy_invalid_diagnostic":legacy,"position":int(positions[i]),"item":int(items[i]),
                        "trial_id":i,"target_id":int(targets[i]),"prediction_id":int(pred[j]),"correct":bool(pred[j]==targets[i]),
                        "payload_sha256":manifest["payload_sha256"],"batch_start":start,"batch_size":stop-start,"batch_requested":8,
                        "attention_validation_batch":dict(stats)}
                    f.write(json.dumps(row,allow_nan=False)+"\n");records.append(row);seen.add((family,i))
                f.flush()
            print(f"CV {model_name} s{seed} {variant} beta={arm} {family}: {len(ids)} items",flush=True)
    expected=len(arrays["targets_A"])+len(arrays["targets_B"]);assert len(records)==expected
    del model;gc.collect();torch.cuda.empty_cache()
    result={"model":model_name,"seed":seed,"variant":variant,"arm":arm,"dtype":str(dtype),
        "payload_sha256":manifest["payload_sha256"],"source_hashes":source,"pairs_path":str(pairs),"pairs_sha256":sha256_file(pairs),
        "n_raw_records":len(records),"native_identity_logits_bit_equal":True,"batch":8,
        "n_identity_preflight_sequences":4,"n_length_buffer_warmup_sequences":int(arm!="1.0"),
        "reset_batch_at_each_position":True,
        "positive_beta_legacy_weights_compared_every_item_and_layer":beta>0,
        "all_attention_and_equality_sanities_passed":not legacy,
        "legacy_attention_intentionally_invalid":legacy,
        "elapsed_seconds":time.perf_counter()-began}
    write_json_new(output,result)
    progress("V3 CV beta job",f"{model_name} s{seed} {variant} beta={arm}; both full families, lock released after job",result["elapsed_seconds"],
        f"flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model {model_name} --seed {seed} --variant {variant} --beta {arm}")
    return result

def read_seed(model,seed,variant):
    rows=[];jobs=[]
    for arm in [str(b) for b in GRID]+["legacy_beta0"]:
        jobpath=Path(f"out/phase18_posbatch_items_{slug(model)}_s{seed}_{variant}_b{arm}_v3.json")
        meta=json.loads(jobpath.read_text(encoding="utf-8"));pairs=Path(meta["pairs_path"])
        assert meta["pairs_sha256"]==sha256_file(pairs) and meta["native_identity_logits_bit_equal"]
        rows.extend(json.loads(s) for s in pairs.read_text(encoding="utf-8").splitlines());jobs.append(meta)
    assert all(j["source_hashes"]==jobs[0]["source_hashes"] for j in jobs)
    arrays,manifest=load_probe("phase18",model,seed)
    old=json.loads(Path(manifest["historical_source"]).read_text(encoding="utf-8"))[model]
    curves={};legacy_curves={};by={};count_mismatches=[];n_expected=0
    for family in ["A","B"]:
        n=len(arrays["targets_"+family]);n_expected+=n*10
        positions=manifest["positions_"+family]
        middle=[p for p in positions if .25*positions[-1]<=p<=.75*positions[-1]]
        curves[family]={};legacy_curves[family]={}
        for arm in [str(b) for b in GRID]+["legacy_beta0"]:
            selected=sorted((r for r in rows if r["family"]==family and r["arm"]==arm),key=lambda r:r["trial_id"])
            assert len(selected)==n and [r["trial_id"] for r in selected]==list(range(n))
            assert np.array_equal([r["target_id"] for r in selected],arrays["targets_"+family])
            acc={p:sum(r["correct"] for r in selected if r["position"]==p)/manifest["n_per_position"] for p in positions}
            rate=p18.mid(acc,positions)
            by[family,arm]={r["trial_id"]:r for r in selected}
            if arm!="legacy_beta0":curves[family][arm]=rate
            old_arm="0.0" if arm=="legacy_beta0" else arm
            if arm=="legacy_beta0" or arm!="0.0":
                legacy_curves[family][old_arm]=rate
                old_count=old["mid"+family][old_arm]*(manifest["n_per_position"]*len(middle))
                assert abs(old_count-round(old_count))<1e-8
                new_count=sum(r["correct"] for r in selected if r["position"] in middle)
                if new_count!=round(old_count):count_mismatches.append({"family":family,"arm":arm,"old_n_correct":round(old_count),"replayed_n_correct":new_count})
    assert len(rows)==n_expected and len({(r["family"],r["arm"],r["trial_id"]) for r in rows})==n_expected
    if count_mismatches and variant=="historical":
        failure=Path(f"out/phase18_historical_mismatch_{slug(model)}_s{seed}_v3.json")
        if not failure.exists():write_json_new(failure,{"source_jobs":[j["pairs_path"] for j in jobs],"differences":count_mismatches})
        # Preserve the failed provenance/reproduction check; it is not an
        # attention sanity and cannot identify missing historical generator code.
        progress("V3 CV provenance limitation",f"{model} s{seed}: {failure}; current-item counterfactual reported separately")
    # Preserve the original float mean and max() tie rule exactly. Replacing
    # binary accuracy with a median would change selection rather than repair it.
    selectedA=max(GRID,key=lambda b:curves["A"][str(b)])
    selectedB=max(GRID,key=lambda b:curves["B"][str(b)])
    legacyA=max(GRID,key=lambda b:legacy_curves["A"][str(b)])
    legacyB=max(GRID,key=lambda b:legacy_curves["B"][str(b)])
    paired={};legacy_paired={}
    for family,selected_beta in [("A",selectedB),("B",selectedA)]:
        positions=manifest["positions_"+family]
        middle=[p for p in positions if .25*positions[-1]<=p<=.75*positions[-1]]
        baseline=by[family,"1.0"];edited=by[family,str(selected_beta)]
        paired[family]=[]
        for i in sorted(baseline):
            b,e=baseline[i],edited[i]
            assert (b["target_id"],b["position"],b["item"])==(e["target_id"],e["position"],e["item"])
            if b["position"] in middle:
                paired[family].append({"seed":seed,"position":b["position"],"item":b["item"],
                    "baseline_correct":b["correct"],"edited_correct":e["correct"],"selected_beta":selected_beta})
    for family,selected_beta in [("A",legacyB),("B",legacyA)]:
        positions=manifest["positions_"+family]
        middle=[p for p in positions if .25*positions[-1]<=p<=.75*positions[-1]]
        baseline=by[family,"1.0"]
        legacy_arm="legacy_beta0" if selected_beta==0 else str(selected_beta)
        edited=by[family,legacy_arm];legacy_paired[family]=[]
        for i in sorted(baseline):
            b,e=baseline[i],edited[i]
            assert (b["target_id"],b["position"],b["item"])==(e["target_id"],e["position"],e["item"])
            if b["position"] in middle:
                legacy_paired[family].append({"seed":seed,"position":b["position"],"item":b["item"],
                    "baseline_correct":b["correct"],"edited_correct":e["correct"],"selected_beta":selected_beta})
    gainB=curves["B"][str(selectedA)]-curves["B"]["1.0"]
    gainA=curves["A"][str(selectedB)]-curves["A"]["1.0"]
    result={"seed":seed,"variant":variant,"dtype":meta["dtype"],"source_jobs":[j["pairs_path"] for j in jobs],
        "n_raw_records":len(rows),"midA":curves["A"],"midB":curves["B"],
        "beta_selected_on_A":selectedA,"beta_selected_on_B":selectedB,
        "heldout_gain_on_B_using_betaA":gainB,"heldout_gain_on_A_using_betaB":gainA,
        "old_beta_selected_on_A":old["beta_selected_on_A"],"old_beta_selected_on_B":old["beta_selected_on_B"],
        "old_heldout_gain_on_B_using_betaA":old["heldout_gain_on_B_using_betaA"],
        "old_heldout_gain_on_A_using_betaB":old["heldout_gain_on_A_using_betaB"],
        "legacy_replayed_beta_selected_on_A":legacyA,"legacy_replayed_beta_selected_on_B":legacyB,
        "legacy_current_items_heldout_gain_on_B_using_betaA":legacy_curves["B"][str(legacyA)]-legacy_curves["B"]["1.0"],
        "legacy_current_items_heldout_gain_on_A_using_betaB":legacy_curves["A"][str(legacyB)]-legacy_curves["A"]["1.0"],
        "correction_changes_current_items_selection_A":selectedA!=legacyA,
        "correction_changes_current_items_selection_B":selectedB!=legacyB,
        "all_legacy_middle_counts_exact":not count_mismatches,"legacy_count_differences":count_mismatches,
        "legacy_selection_matches_recorded":legacyA==old["beta_selected_on_A"] and legacyB==old["beta_selected_on_B"],
        "selection_change_A":selectedA!=old["beta_selected_on_A"],"selection_change_B":selectedB!=old["beta_selected_on_B"],
        "middle_rule":"historical mid(): .25*last_tested_position <= p <= .75*last_tested_position",
        "elapsed_seconds_gpu_jobs":sum(j["elapsed_seconds"] for j in jobs)}
    return result,paired,legacy_paired

def analyze(model,variant):
    seeds=[];paired={"A":[],"B":[]};legacy_paired={"A":[],"B":[]}
    for seed in SEEDS:
        result,items,legacy_items=read_seed(model,seed,variant);seeds.append(result)
        for family in paired:
            paired[family].extend(items[family]);legacy_paired[family].extend(legacy_items[family])
    summary={}
    for family,gain in [("A","heldout_gain_on_A_using_betaB"),("B","heldout_gain_on_B_using_betaA")]:
        summary[family]={"new_gain":bootstrap_item_gains(paired[family]),
            "legacy_on_same_current_items_gain":bootstrap_item_gains(legacy_paired[family]),
            "new_seed_gains":[s[gain] for s in seeds],"old_seed_gains":[s["old_"+gain] for s in seeds],
            "old_median_seed_gain":float(np.median([s["old_"+gain] for s in seeds])),
            "old_mean_seed_gain_secondary":float(np.mean([s["old_"+gain] for s in seeds])),
            "selection_uncertainty":"Item bootstrap is conditional on beta selected on the independent other family; no retuning on held-out items"}
        differences=[int(r["edited_correct"])-int(r["baseline_correct"]) for r in paired[family]]
        summary[family]["item_difference_describe"]=describe(differences,np.arange(len(differences)))
    return {"model":model,"variant":variant,"seeds":seeds,"heldout":summary,
        "all_historical_legacy_counts_exact":all(s["all_legacy_middle_counts_exact"] for s in seeds)}

def aggregate():
    started=time.perf_counter();models={m:analyze(m,"historical") for m in PROBE_MODELS}
    supplement=analyze("Qwen/Qwen2.5-0.5B","standard_bf16")
    result={"_meta":{"schema_version":3,"seeds":SEEDS,"grid":GRID,"models":PROBE_MODELS,
        "n_per_position":150,"nA":128,"nB":256,"primary_precision":"historical fp32, including Qwen0.5; separate bf16 supplement",
        "selection":"unchanged original mean middle accuracy, Python max in original grid order; binary accuracy is count/n",
        "aggregation":"median seed held-out gain; bootstrap paired independent items within seed x position; pooled means secondary",
        "independent_tuning_evaluation":"A/B disjoint filler slices and independent seed and seed+12345 RNGs; selectors fixed before opposite-family evaluation",
        "legacy_beta0_replayed_as_invalid_diagnostic":True,
        "all_primary_legacy_counts_exact":all(m["all_historical_legacy_counts_exact"] for m in models.values()),
        "all_numerical_sanities_strict":True,
        "invalid_legacy_beta0_is_diagnostic_only":True,
        "positive_beta_counterfactual":"Every attention weight checked bit-for-bit against legacy on the same current items at every layer",
        "historical_reproduction_limitation":"FALTA: original CV item IDs and generator source hashes. Family B saved counts fail to reproduce from available phase16; current same-item legacy/corrected counterfactual isolates row-zero repair. Saved old/new differences may include generator drift.",
        "elapsed_seconds":time.perf_counter()-started},"models":models,
        "standard_bf16_supplement":{"Qwen/Qwen2.5-0.5B":supplement}}
    write_json_new("out/phase18_betacv_v3.json",result)
    progress("V3 CV complete","all five models x three seeds x full nine-beta grid; strict attention sanity and full positive-beta legacy equality; failed historical counts explicit, same-item legacy/corrected CV compared",result["_meta"]["elapsed_seconds"],
             ".venv/Scripts/python.exe -B phase45_currentcv_items.py --aggregate-only")

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--aggregate-only",action="store_true")
    ap.add_argument("--model",choices=PROBE_MODELS);ap.add_argument("--seed",type=int,choices=SEEDS)
    ap.add_argument("--variant",choices=["historical","standard_bf16"],default="historical")
    ap.add_argument("--beta",choices=[str(b) for b in GRID]+["legacy_beta0"])
    args=ap.parse_args()
    if args.aggregate_only:aggregate();return
    if args.model is None or args.seed is None or args.beta is None:ap.error("GPU CV job needs model, seed and beta")
    run_beta_job(args.model,args.seed,args.variant,args.beta)

if __name__=="__main__":main()
