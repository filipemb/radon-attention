"""Read-only reconciliation of revision-v3 datasets, interventions and items."""
from revision_v3_stats import MODELS,CORPUS_PATH,sha256_file,write_json_new,progress,slug
from pathlib import Path
import argparse
import json
import math
import time
import numpy as np
from phase2_downstream import DeferredStats

def read(path):return json.loads(Path(path).read_text(encoding="utf-8"))

def rows(meta):
    assert meta["pairs_sha256"]==sha256_file(meta["pairs_path"])
    return [json.loads(s) for s in Path(meta["pairs_path"]).read_text(encoding="utf-8").splitlines()]

def check_stats(stats,legacy=False):
    if not legacy:assert all(stats.get(k,0)==0 for k in DeferredStats.violation_keys)
    assert all(math.isfinite(v) for v in stats.values() if isinstance(v,float))

def mass_chunk(path):
    meta=read(path);raw=rows(meta);corpus=read(CORPUS_PATH)
    assert meta["corpus_sha256"]==sha256_file(CORPUS_PATH)
    assert len(raw)==meta["n_documents"]*12
    assert len({(r["document_index"],r["context"],r["arm"]) for r in raw})==len(raw)
    assert sorted({r["document_index"] for r in raw})==list(range(meta["start"],meta["stop"]))
    expected=corpus["models"][meta["model"]]["n_layers"]*corpus["models"][meta["model"]]["n_heads"]
    for r in raw:
        i=r["document_index"]
        assert r["doc_id"]==corpus["documents"][i]["doc_id"]
        assert r["target_id"]==corpus["models"][meta["model"]]["documents"][i]["token_ids"][128]
        assert r["prefix_length"]==128 and r["combined_sanity_passed"]
        assert all(math.isfinite(r[k]) for k in ["kl_true","kl_context","nll","reference_nll"])
        assert r["base_validation"]["reconstruction_rows_total"]==expected*128
        check_stats(r["base_validation"]);check_stats(r["edit_validation"])
        if r["arm"]=="baseline":
            assert r["kl_context"]==0
            if r["context"]=="identity":assert r["kl_true"]==0
        if r["mass"] is not None:
            m=r["mass"];assert m["mass_rows_total"]==expected*128 and m["last_query_rows_total"]==expected
            assert all(m.get(k,0)==0 for k in ["mass_mismatch_rows","mass_invalid_values","mass_invalid_budget","mass_first_row_changes"])
            assert m["max_mass_match_error"]<=m["mass_match_atol"]
            assert 0<=m["mass_removed_each_arm"]<=m["mass_requested"]
            other=r["arm"].replace("sink_","control_",1) if r["arm"].startswith("sink_") else r["arm"].replace("control_","sink_",1)
            matched=next(x for x in raw if (x["document_index"],x["context"],x["arm"])==(i,r["context"],other))
            assert matched["mass"]==m
    pilot=read(meta["pilot_path"])
    assert meta["source_hashes"]==pilot["source_hashes"]
    assert pilot["native_identity_bit_equal"] and pilot["old_anova_baseline_bit_equal"]
    assert all(v["passed"] for v in pilot["suffix_checks"].values())
    return {"path":str(path),"n_records":len(raw),"passed":True}

def cv_beta(path):
    from revision_v3_probes import load_probe
    meta=read(path);raw=rows(meta);arrays,manifest=load_probe("phase18",meta["model"],meta["seed"])
    assert sha256_file(manifest["historical_source"])==manifest["historical_sha256"]
    assert meta["native_identity_logits_bit_equal"]
    assert len(raw)==len(arrays["targets_A"])+len(arrays["targets_B"])
    old=read(manifest["historical_source"])[meta["model"]]
    for family in ["A","B"]:
        selected=sorted((r for r in raw if r["family"]==family),key=lambda r:r["trial_id"])
        assert np.array_equal([r["target_id"] for r in selected],arrays["targets_"+family])
        assert all(r["correct"]==(r["prediction_id"]==r["target_id"]) for r in selected)
        for r in selected:check_stats(r["attention_validation_batch"],r["legacy_invalid_diagnostic"])
        if meta["variant"]=="historical" and meta["arm"]!="0.0":
            positions=manifest["positions_"+family]
            middle=[p for p in positions if .25*positions[-1]<=p<=.75*positions[-1]]
            actual=sum(r["correct"] for r in selected if r["position"] in middle)
            oldarm="0.0" if meta["arm"]=="legacy_beta0" else meta["arm"]
            expected=old["mid"+family][oldarm]*len(middle)*manifest["n_per_position"]
            if actual!=round(expected):
                failure=Path(f"out/phase18_count_mismatch_{slug(meta['model'])}_s{meta['seed']}_b{meta['arm']}_v3.json")
                if not failure.exists():write_json_new(failure,{"family":family,"expected":expected,"actual":actual,"source":str(path)})
                raise RuntimeError(f"CV historical aggregate mismatch: {failure}")
    return {"path":str(path),"n_records":len(raw),"passed":True}

def items(path):
    from phase38_paired_items import read_job
    meta=read(path);paired,job,_=read_job(meta["task"],meta["model"],meta["seed"],meta["variant"])
    for r in rows(meta):
        assert r["correct"]==(r["prediction_id"]==r["target_id"])
        check_stats(r["attention_validation_batch"])
    return {"path":str(path),"n_pairs":len(paired),"passed":True,"historical_exact":job["historical_counts_exact_match"]}

def current_cv_beta(path):
    """Numerical validity and provenance are reported as separate outcomes.

    The old strict reproduction gate above remains intact as the diagnostic
    which exposed the unavailable historical family-B generator/items.
    """
    from revision_v3_probes import load_probe
    meta=read(path);raw=rows(meta);arrays,manifest=load_probe("phase18",meta["model"],meta["seed"])
    assert sha256_file(manifest["historical_source"])==manifest["historical_sha256"]
    assert meta["native_identity_logits_bit_equal"] and meta["reset_batch_at_each_position"]
    legacy=meta["arm"]=="legacy_beta0"
    assert meta["legacy_attention_intentionally_invalid"]==legacy
    assert meta["all_attention_and_equality_sanities_passed"]==(not legacy)
    assert len(raw)==2400 and len({(r["family"],r["trial_id"]) for r in raw})==2400
    old=read(manifest["historical_source"])[meta["model"]]
    config=read(CORPUS_PATH)["models"][meta["model"]]
    historical_differences=[]
    for family in ["A","B"]:
        selected=sorted((r for r in raw if r["family"]==family),key=lambda r:r["trial_id"])
        assert [r["trial_id"] for r in selected]==list(range(1200))
        for key,field in [("targets","target_id"),("positions","position"),("item_index","item")]:
            assert np.array_equal([r[field] for r in selected],arrays[key+"_"+family])
        for r in selected:
            assert r["correct"]==(r["prediction_id"]==r["target_id"])
            check_stats(r["attention_validation_batch"],legacy)
            start=r["batch_start"];stop=start+r["batch_size"];npp=manifest["n_per_position"]
            assert start//npp==(stop-1)//npp and r["batch_size"]<=8
            row_distributions=r["batch_size"]*config["n_layers"]*config["n_heads"]
            expected_rows=row_distributions*arrays["input_ids_"+family].shape[1]
            if r["beta"]>0:
                assert r["attention_validation_batch"]["positive_beta_rows_compared"]==expected_rows
                assert r["attention_validation_batch"]["positive_beta_legacy_weight_mismatches"]==0
            elif legacy:
                assert r["attention_validation_batch"]["rows_total"]==expected_rows
                assert r["attention_validation_batch"]["zero_rows"]>=row_distributions
            else:
                assert r["attention_validation_batch"]["sink_edit_rows_total"]==expected_rows
                assert r["attention_validation_batch"]["sink_edit_rows_preserved_no_alternative"]>=row_distributions
        if meta["variant"]=="historical" and meta["arm"]!="0.0":
            positions=manifest["positions_"+family]
            middle=[p for p in positions if .25*positions[-1]<=p<=.75*positions[-1]]
            actual=sum(r["correct"] for r in selected if r["position"] in middle)
            oldarm="0.0" if legacy else meta["arm"]
            expected=old["mid"+family][oldarm]*len(middle)*npp
            assert abs(expected-round(expected))<1e-8
            if actual!=round(expected):historical_differences.append({"family":family,
                "old_correct":round(expected),"current_correct":actual})
    return {"path":str(path),"n_records":len(raw),"passed":True,
        "passed_scope":"all corrected attention sanities; legacy beta0 deliberately invalid diagnostic",
        "historical_reproduction_exact":(not historical_differences) if meta["variant"]=="historical" else None,
        "historical_comparison_applicable":meta["variant"]=="historical",
        "historical_differences":historical_differences}

def full():
    began=time.perf_counter();required=["out/phase15_constancy_v3.json","out/phase26_named_v3_ci.json",
        "out/phase7_editability_v3.json","out/phase8_items_v3.json","out/phase11_items_v3.json","out/phase18_betacv_v3.json",
        "out/phase8_beta0_statistics_v3.json"]
    assert all(Path(p).exists() for p in required)
    constancy=read(required[0]);assert len(constancy["datasets"])==14
    for d in constancy["datasets"]:
        raw=rows(d);assert len(raw)==d["n_instances"]
        assert d["denominator_epsilon"]==0 and d["input_validation"]["invalid_matrices"]==0
        for stratum,s in d["strata"].items():
            selected=[r for r in raw if r["sink_mass_stratum"]==stratum]
            assert len(selected)==s["n_heads"]
            assert all((r["sink_mean_weight"]>.3)==(stratum=="gt_0.3") for r in selected)
            assert s["n_zero_energy_control_columns"]==sum(r["n_zero_energy_control_columns"] for r in selected)
            for key in ["sink_nonconstancy","control_column_nonconstancy_median"]:
                valid=[r[key] for r in selected if r[key] is not None]
                assert s[key]["n_instances"]==len(valid)
                if valid:assert s[key]["median"]==float(np.median(valid))
    named=read(required[1]);assert len(named["datasets"])==12
    for d in named["datasets"]:
        assert not d["decompositions_recomputed"] and len(d["configurations"])==15
        for cfg in d["configurations"].values():
            for stat in cfg.values():assert stat["n_instances"]==d["n_instances"] and stat["n_documents"]==64 and stat["n_bootstrap"]==2000
    checks=[]
    for model in MODELS:
        for start in range(0,256,16):checks.append(mass_chunk(f"out/phase7_massmatched_{slug(model)}_d{start:03d}_{start+16:03d}_v3.json"))
    for p in Path("out").glob("phase8_items_*_s*_*_v3.json"):checks.append(items(p))
    for p in Path("out").glob("phase11_items_*_s*_*_v3.json"):checks.append(items(p))
    for p in Path("out").glob("phase18_posbatch_items_*_s*_*_b*_v3.json"):checks.append(current_cv_beta(p))
    assert len(checks)==300, "Expected all 96 mass, 24 item and 180 CV jobs"
    assert read("out/revision_v3_statistics_checks.json")["all_passed"] and read("out/phase37_mass_matched_checks_v3.json")["all_passed"]
    for p in required[3:5]:assert read(p)["_meta"]["all_primary_historical_aggregates_exact"]
    assert read(required[5])["_meta"]["all_numerical_sanities_strict"]
    assert read(required[5])["_meta"]["invalid_legacy_beta0_is_diagnostic_only"]
    assert read("out/phase45_positive_equality_checks_v3.json")["all_passed"]
    beta0=read(required[6]);old_beta0=read("out/phase8_beta0_v2.json")
    assert beta0["_meta"]["source_sha256"]==sha256_file("out/phase8_beta0_v2.json")
    assert beta0["_meta"]["no_new_forward"] and len(beta0["models"])==5
    for model,d in beta0["models"].items():
        assert d["n_items"]==3200 and d["pairs_sha256"]==sha256_file(d["pairs_path"])
        assert d["baseline_n_correct"]==old_beta0[model]["arms"]["baseline_beta1"]["n_correct"]
        assert d["corrected_n_correct"]==old_beta0[model]["arms"]["corrected_beta0"]["n_correct"]
        assert d["all_positions"]["paired_mcnemar"]["p_holm_five_models"]==old_beta0[model]["paired_corrected_vs_baseline"]["holm_pvalue_five_models"]
    sources=[Path(p) for p in ["revision_v3_stats.py","revision_v3_probes.py","phase36_constancy_named_ci.py",
        "phase37_mass_matched.py","phase38_paired_items.py","phase39_betacv_items.py","phase40_v3_checks.py","phase41_v3_run.py",
        "phase43_cv_batch_diagnostic.py","phase45_currentcv_items.py","phase46_currentcv_run.py","beta0_statistics_v3.py","revision_v3_report.py"]]
    paths=set(sources+[Path(p) for p in required])
    for pattern in ["phase15_constancy*_v3.json","phase26_named*_ci_v3.json","phase7_massmatched*_v3.json",
        "phase8_items*_v3.json","phase11_items*_v3.json","phase18_items*_v3.json","phase18_posbatch_items*_v3.json",
        "phase18_*diagnostic_v3.json","phase18_*mismatch*_v3.json","revision_v3_statistics_checks.json"]:
        paths.update(Path("out").glob(pattern))
    for prefix in ["phase8_items_","phase11_items_","phase18_items_","phase18_posbatch_items_","phase7_massmatched_","constancy_"]:
        paths.update(Path("out/pairs").glob(prefix+"*_v3.jsonl"))
    for prefix in ["phase8_items_","phase11_items_","phase18_items_"]:
        paths.update(Path("data/attn").glob(prefix+"*_v3.npz"));paths.update(Path("data/attn").glob(prefix+"*_v3.manifest.json"))
    paths.update(Path(p) for p in ["out/revision_v3_protocol.json",
        "out/phase37_mass_matched_checks_v3.json","out/phase45_positive_equality_checks_v3.json",
        "out/revision_v3_cv_reproduction_protocol.json","out/revision_v3_precision_family.json","out/revision_v3_timings.json"])
    inventory=[{"path":str(p).replace("\\","/"),"bytes":p.stat().st_size,"sha256":sha256_file(p)} for p in sorted(paths)]
    result={"all_required_experiments_complete":True,"all_passed":True,"required_outputs":required,"job_checks":checks,
        "inventory":inventory,"progress_log":"out/_rerun_logs/v3_progress.md","independent_other_family_review":"not performed by this script",
        "elapsed_seconds":time.perf_counter()-began}
    write_json_new("out/revision_v3_delivery.json",result)
    progress("V3 delivery audit",f"all six required outputs and {len(checks)} jobs reconciled",result["elapsed_seconds"])
    print(f"V3 DELIVERY PASSED: {len(checks)} jobs",flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--mass-chunk");ap.add_argument("--items-job");ap.add_argument("--cv-beta-job");ap.add_argument("--cv-current-beta-job");args=ap.parse_args()
    if args.mass_chunk:r=mass_chunk(args.mass_chunk)
    elif args.items_job:r=items(args.items_job)
    elif args.cv_beta_job:r=cv_beta(args.cv_beta_job)
    elif args.cv_current_beta_job:r=current_cv_beta(args.cv_current_beta_job)
    else:full();return
    print(json.dumps(r),flush=True)

if __name__=="__main__":main()
