"""Retrieval/KV items and paired seed-stratified statistics, outputs v3 only."""
from revision_v3_probes import (prepare,run_job,load_probe,PROBE_MODELS,KV_MODELS,SEEDS,
                                slug,sha256_file,write_json_new,progress)
from revision_v3_stats import describe,mcnemar,seed_stratified_permutation,bootstrap_item_gains,holm
import argparse
import json
from pathlib import Path
import time
import numpy as np

PRIMARY_FAMILY=[("phase8",m) for m in PROBE_MODELS]+[("phase11",m) for m in KV_MODELS]

def read_job(task,model,seed,variant):
    path=Path(f"out/{task}_items_{slug(model)}_s{seed}_{variant}_v3.json")
    meta=json.loads(path.read_text(encoding="utf-8"));pairs=Path(meta["pairs_path"])
    assert meta["pairs_sha256"]==sha256_file(pairs) and meta["native_identity_logits_bit_equal"]
    rows=[json.loads(s) for s in pairs.read_text(encoding="utf-8").splitlines()]
    arrays,manifest=load_probe(task,model,seed);n=manifest["n_items"]
    assert sha256_file(manifest["historical_source"])==manifest["historical_sha256"]
    assert len(rows)==2*n and len({(r["arm"],r["trial_id"]) for r in rows})==2*n
    old=json.loads(Path(manifest["historical_source"]).read_text(encoding="utf-8"))[model]
    old=old["acc"] if task=="phase8" else old
    differences=[]
    for arm in ["1.0","0.25"]:
        selected=sorted((r for r in rows if r["arm"]==arm),key=lambda r:r["trial_id"])
        assert [r["trial_id"] for r in selected]==list(range(n))
        assert np.array_equal([r["target_id"] for r in selected],arrays["targets"])
        for pos in manifest["positions"]:
            items=[r for r in selected if r["position"]==pos]
            assert len(items)==manifest["n_per_position"]
            expected=old[arm][str(pos)]*len(items)
            assert abs(expected-round(expected))<1e-8
            actual=sum(r["correct"] for r in items)
            if actual!=round(expected):differences.append({"arm":arm,"position":pos,"old_n_correct":round(expected),"new_n_correct":actual})
    if differences and variant=="historical":
        failure=Path(f"out/{task}_historical_mismatch_{slug(model)}_s{seed}_v3.json")
        if not failure.exists():write_json_new(failure,{"source_job":str(path),"differences":differences})
        raise RuntimeError(f"Historical positive-beta aggregate mismatch, not hidden or tolerated: {failure}")
    by={a:{r["trial_id"]:r for r in rows if r["arm"]==a} for a in ["1.0","0.25"]}
    paired=[]
    for i in range(n):
        b,e=by["1.0"][i],by["0.25"][i]
        assert (b["target_id"],b["position"],b["item"])==(e["target_id"],e["position"],e["item"])
        paired.append({"seed":seed,"position":b["position"],"item":b["item"],"trial_id":i,
            "target_id":b["target_id"],"baseline_correct":b["correct"],"edited_correct":e["correct"]})
    return paired,{"seed":seed,"variant":variant,"dtype":meta["dtype"],"job_path":str(path),
        "pairs_path":str(pairs),"n_items":n,"historical_counts_exact_match":not differences,
        "historical_differences":differences,"elapsed_seconds":meta["elapsed_seconds"]},manifest

def summarize(rows):
    result=bootstrap_item_gains(rows)
    result["baseline_n_correct"]=sum(r["baseline_correct"] for r in rows)
    result["edited_n_correct"]=sum(r["edited_correct"] for r in rows)
    result["baseline_accuracy"]=result["baseline_n_correct"]/len(rows)
    result["edited_accuracy"]=result["edited_n_correct"]/len(rows)
    d=[int(r["edited_correct"])-int(r["baseline_correct"]) for r in rows]
    result["item_difference_describe"]=describe(d,np.arange(len(rows)))
    result["by_seed"]=[]
    for seed in SEEDS:
        selected=[r for r in rows if r["seed"]==seed]
        test=mcnemar([r["baseline_correct"] for r in selected],[r["edited_correct"] for r in selected])
        result["by_seed"].append({"seed":seed,**test})
    result["combined_seed_stratified_permutation"]=seed_stratified_permutation(result["by_seed"])
    return result

def analyze(task,model,variant):
    paired=[];jobs=[]
    for seed in SEEDS:
        rows,job,manifest=read_job(task,model,seed,variant);paired+=rows;jobs.append(job)
    n=manifest["n"]
    middle=[r for r in paired if .25*n<=r["position"]<=.75*n]
    positions={str(p):summarize([r for r in paired if r["position"]==p]) for p in manifest["positions"]}
    return {"model":model,"variant":variant,"dtype":jobs[0]["dtype"],"n":n,"seeds":SEEDS,
        "jobs":jobs,"all_historical_counts_exact_match":all(j["historical_counts_exact_match"] for j in jobs),
        "middle_rule":"0.25*n <= position <= 0.75*n","middle_positions":sorted({r["position"] for r in middle}),
        "all_positions":summarize(paired),"middle":summarize(middle),"by_position":positions}

def aggregate():
    started=time.perf_counter()
    results={(task,model):analyze(task,model,"historical") for task,model in PRIMARY_FAMILY}
    primary=holm([results[k]["middle"]["combined_seed_stratified_permutation"]["pvalue"] for k in PRIMARY_FAMILY])
    seeded=[(k,i) for k in PRIMARY_FAMILY for i in range(3)]
    seed_adjusted=holm([results[k]["middle"]["by_seed"][i]["mcnemar_exact_pvalue"] for k,i in seeded])
    for i,k in enumerate(PRIMARY_FAMILY):results[k]["middle"]["combined_seed_stratified_permutation"]["p_holm_7_task_model_comparisons"]=primary[i]
    for i,(k,j) in enumerate(seeded):results[k]["middle"]["by_seed"][j]["p_holm_21_seed_comparisons"]=seed_adjusted[i]
    for task in ["phase8","phase11"]:
        keys=[k for k in PRIMARY_FAMILY if k[0]==task]
        adjusted=holm([results[k]["middle"]["combined_seed_stratified_permutation"]["pvalue"] for k in keys])
        for i,k in enumerate(keys):results[k]["middle"]["combined_seed_stratified_permutation"]["p_holm_within_benchmark_secondary"]=adjusted[i]
    supplement=analyze("phase8","Qwen/Qwen2.5-0.5B","standard_bf16")
    # Precision comparison is secondary. Keep the original Holm7 primary
    # family intact and adjust all eight contrasts together, so the bf16
    # supplement also has a corrected test without selecting a dtype by result.
    precision_protocol=json.loads(Path("out/revision_v3_precision_family.json").read_text(encoding="utf-8"))
    eight=[results[k]["middle"] for k in PRIMARY_FAMILY]+[supplement["middle"]]
    assert len(precision_protocol["secondary_family_8"])==len(eight)==8
    adjusted8=holm([s["combined_seed_stratified_permutation"]["pvalue"] for s in eight])
    adjusted24=holm([s["by_seed"][i]["mcnemar_exact_pvalue"] for s in eight for i in range(3)])
    for index,s in enumerate(eight):
        s["combined_seed_stratified_permutation"]["p_holm_8_including_bf16_supplement_secondary"]=adjusted8[index]
        for i in range(3):s["by_seed"][i]["p_holm_24_including_bf16_supplement_secondary"]=adjusted24[index*3+i]
    for task,models in [("phase8",PROBE_MODELS),("phase11",KV_MODELS)]:
        output={"_meta":{"schema_version":3,"primary_precision":"historical precision to test aggregate reproduction",
            "primary_holm_family":[list(k) for k in PRIMARY_FAMILY],"primary_scope":"middle window only",
            "secondary_precision_holm_family":precision_protocol["secondary_family_8"],
            "precision_protocol_path":"out/revision_v3_precision_family.json",
            "precision_protocol_sha256":sha256_file("out/revision_v3_precision_family.json"),
            "analysis_source_sha256":sha256_file(__file__),
            "combined_test":"exact paired permutation within seed, statistic median of seed accuracy gains",
            "per_seed_tests":"exact McNemar; secondary Holm over all 21 task-model-seed tests",
            "binary_statistics":"Raw item median and its describe CI reported; median seed gain with item bootstrap; pooled mean accuracy gain secondary",
            "bootstrap":"2000 draws, seed0, paired items within seed x position",
            "all_items_retained":True,"all_primary_historical_aggregates_exact":True,
            "statistics_source_sha256":sha256_file("revision_v3_stats.py"),
            "elapsed_seconds_joint_aggregate":time.perf_counter()-started},
            "models":{m:results[task,m] for m in models}}
        if task=="phase8":output["standard_bf16_supplement"]={"Qwen/Qwen2.5-0.5B":supplement,"inference_status":"supplementary, outside the primary confirmatory family"}
        write_json_new(f"out/{task}_items_v3.json",output)
    progress("V3 paired item statistics","probe five models + KV two models, three seeds; exact historical counts; paired permutations and prespecified Holm7",time.perf_counter()-started,
             ".venv/Scripts/python.exe -B phase38_paired_items.py --aggregate-only")

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--prepare-only",action="store_true")
    ap.add_argument("--aggregate-only",action="store_true");ap.add_argument("--task",choices=["phase8","phase11"])
    ap.add_argument("--model");ap.add_argument("--seed",type=int,choices=SEEDS)
    ap.add_argument("--variant",choices=["historical","standard_bf16"],default="historical")
    args=ap.parse_args()
    if args.prepare_only:prepare();return
    if args.aggregate_only:aggregate();return
    if args.task is None or args.model is None or args.seed is None:ap.error("GPU job needs task, model, seed")
    if args.model not in (PROBE_MODELS if args.task=="phase8" else KV_MODELS):ap.error("Model not in historical task")
    run_job(args.task,args.model,args.seed,args.variant)

if __name__=="__main__":main()
