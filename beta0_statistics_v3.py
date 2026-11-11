"""Item CIs for the completed beta0 retest; no new model forward or changed item."""
from revision_v3_stats import (write_json_new,sha256_file,progress,describe,
                               bootstrap_item_gains,mcnemar,holm)
from pathlib import Path
import json
import time
import numpy as np

def summarize(rows):
    d=[int(r["edited_correct"])-int(r["baseline_correct"]) for r in rows]
    result=bootstrap_item_gains(rows)
    result["item_difference_describe"]=describe(d,np.arange(len(rows)))
    result["paired_mcnemar"]=mcnemar([r["baseline_correct"] for r in rows],
                                     [r["edited_correct"] for r in rows])
    return result

def main():
    began=time.perf_counter();source=Path("out/phase8_beta0_v2.json")
    old=json.loads(source.read_text(encoding="utf-8"));models={}
    for model,meta in old.items():
        if model=="_meta":continue
        pairs=Path(meta["pairs_path"])
        raw=[json.loads(s) for s in pairs.read_text(encoding="utf-8").splitlines()]
        assert len(raw)==9600 and len({(r["arm"],r["trial_id"]) for r in raw})==9600
        by={arm:{r["trial_id"]:r for r in raw if r["arm"]==arm}
            for arm in ["baseline_beta1","corrected_beta0","legacy_beta0_diagnostic"]}
        assert all(set(d)==set(range(3200)) for d in by.values())
        for arm,d in by.items():
            assert all(r["correct"]==(r["prediction_id"]==r["target_id"]) for r in d.values())
            assert sum(r["correct"] for r in d.values())==meta["arms"][arm]["n_correct"]
        rows=[]
        for i in range(3200):
            b,e=by["baseline_beta1"][i],by["corrected_beta0"][i]
            assert (b["target_id"],b["position"],b["probe_payload_sha256"])==(e["target_id"],e["position"],e["probe_payload_sha256"])
            rows.append({"seed":meta["seed"],"position":b["position"],"item":i,
                "baseline_correct":b["correct"],"edited_correct":e["correct"]})
        item={"dtype":meta["dtype"],"seed":meta["seed"],"n_items":3200,
            "baseline_n_correct":meta["arms"]["baseline_beta1"]["n_correct"],
            "corrected_n_correct":meta["arms"]["corrected_beta0"]["n_correct"],
            "legacy_n_correct":meta["arms"]["legacy_beta0_diagnostic"]["n_correct"],
            "all_positions":summarize(rows),"middle":summarize([r for r in rows if r["position"] in meta["middle_positions"]]),
            "attention_validation":meta["attention_validation"],
            "pairs_path":meta["pairs_path"],"pairs_sha256":sha256_file(pairs)}
        assert item["all_positions"]["paired_mcnemar"]["mcnemar_exact_pvalue"]==meta["paired_corrected_vs_baseline"]["mcnemar_exact_pvalue"]
        models[model]=item
    adjusted=holm([v["all_positions"]["paired_mcnemar"]["mcnemar_exact_pvalue"] for v in models.values()])
    for value,p in zip(models.values(),adjusted):value["all_positions"]["paired_mcnemar"]["p_holm_five_models"]=p
    result={"_meta":{"source":str(source),"source_sha256":sha256_file(source),"no_new_forward":True,
        "source_and_items_unmodified":True,"n_models":5,"seed":0,"n_items_per_model":3200,
        "scope":"Conditional on the completed seed0 probe items; no claim about seed-population uncertainty",
        "aggregation":"Raw item median with item CI; accuracy is count/n, paired gain CI from item bootstrap within position",
        "n_bootstrap":2000,"bootstrap_seed":0,"statistics_source_sha256":sha256_file("revision_v3_stats.py"),
        "script_sha256":sha256_file(__file__),"elapsed_seconds":time.perf_counter()-began},"models":models}
    write_json_new("out/phase8_beta0_statistics_v3.json",result)
    progress("V3 beta0 item intervals","Five completed seed0 probes; counts and exact McNemar unchanged, paired item CIs added without inference",result["_meta"]["elapsed_seconds"],
        ".venv/Scripts/python.exe -B beta0_statistics_v3.py")
    print(f"beta0 CIs complete in {result['_meta']['elapsed_seconds']:.3f}s",flush=True)

if __name__=="__main__":main()
