"""CPU-only independent reconciliation and compact report for the matched probe."""
from revision_v3_stats import sha256_file, write_json_new
from phase53_massmatched_retrieval import FAMILY, PROTOCOL, hashes, job_paths, log
import json
from pathlib import Path
import time
import numpy as np


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    began = time.perf_counter()
    protocol = read(PROTOCOL)
    assert protocol["source_hashes"] == hashes()
    root = {t: read(f"out/{t}_massmatched_items_v3.json") for t in ["phase8", "phase11"]}
    old_root = {t: read(f"out/{t}_items_v3.json") for t in ["phase8", "phase11"]}
    summaries = []
    checked = 0
    for task, model in FAMILY:
        result = root[task]["models"][model]
        raw = []
        for seed in [0, 1, 2]:
            plan = next(j for j in protocol["jobs"] if (j["task"], j["model"], j["seed"]) == (task, model, seed))
            assert sha256_file(plan["manifest_path"]) == plan["manifest_sha256"]
            for k in ["job", "pairs"]:
                assert sha256_file(plan["historical"][k+"_path"]) == plan["historical"][k+"_sha256"]
            path, pairpath = job_paths(task, model, seed)
            meta = read(path)
            assert meta["pairs_sha256"] == sha256_file(pairpath)
            rows = [json.loads(line) for line in pairpath.read_text(encoding="utf-8").splitlines()]
            old = [json.loads(line) for line in Path(plan["historical"]["pairs_path"]).read_text(encoding="utf-8").splitlines()]
            old_by = {(r["arm"], r["trial_id"]): r for r in old}
            assert len(rows) == plan["n_independent_items"]
            assert len({r["trial_id"] for r in rows}) == len(rows)
            for r in rows:
                for new_arm, old_arm in [("identity", "1.0"), ("historical_uncapped_sink", "0.25")]:
                    prior = old_by[old_arm, r["trial_id"]]
                    assert (r[new_arm+"_prediction"], r["target_id"], r["position"], r["item"]) == (
                        prior["prediction_id"], prior["target_id"], prior["position"], prior["item"])
                for arm in ["identity", "sink", "control", "historical_uncapped_sink"]:
                    assert r[arm+"_correct"] == (r[arm+"_prediction"] == r["target_id"])
            if (task, model) == ("phase11", "Qwen/Qwen2.5-3B"):
                reference_job = result["identity_reference"]["full_reference_jobs"][seed]
                assert sha256_file(reference_job["path"]) == reference_job["sha256"]
                refmeta = read(reference_job["path"])
                assert refmeta["native_same_batch_identity_exact"] and refmeta["n_independent_items"] == 600
                assert refmeta["source_sha256"] == sha256_file("phase58_massmatched_qwen_identity.py")
                assert sha256_file(reference_job["pairs_path"]) == reference_job["pairs_sha256"]
                references = {r["trial_id"]: r for r in [json.loads(s) for s in Path(reference_job["pairs_path"]).read_text(encoding="utf-8").splitlines()]}
                assert len(references) == len(rows) == 600
                assert sum(b["validation"]["base"]["rows_checked"] for b in refmeta["batch_checks"]) == 2*sum(b["checks"]["mass"]["mass_rows_total"] for b in meta["batch_checks"])
                for r in rows:
                    native = references[r["trial_id"]]
                    assert (native["position"], native["item"], native["target_id"], native["original_prediction"]) == (r["position"], r["item"], r["target_id"], r["identity_prediction"])
                    for arm in ["copy1", "copy2", "original"]:
                        assert native[arm+"_correct"] == (native[arm+"_prediction"] == r["target_id"])
                    r["identity_historical_correct"] = r["identity_correct"]
                    r["identity_correct"] = native["copy1_correct"]
                    r["identity_control_copy_correct"] = native["copy2_correct"]
            n = read(plan["manifest_path"])["n"]
            totals = 0
            for batch in meta["batch_checks"]:
                checks = batch["checks"]
                count = checks["mass"]["mass_rows_total"]
                totals += count
                assert checks["base"]["rows_checked"] == 2*count
                assert checks["mass"]["mass_mismatch_rows"] == 0
                assert checks["mass"]["mass_invalid_budget"] == 0
                assert checks["mass"]["mass_invalid_values"] == 0
                assert checks["mass"]["mass_first_row_changes"] == 0
                assert checks["mass"]["max_mass_match_error"] <= 32*n*np.finfo(np.float64).eps
                for arm in ["sink", "control"]:
                    assert checks[arm]["rows_checked"] == 3*count
                    assert checks[arm]["reconstruction_rows_total"] == count
                    assert checks[arm]["empty_rows_completed"] == 0
                    assert checks[arm]["sink_edit_first_row_changes"] == 0
                    assert checks[arm]["sink_edit_rows_preserved_no_alternative"] >= count//n
                    assert checks[arm]["negative_nan_inf_upper_nonzero"] == 0
                    assert checks[arm]["row_sum_violations"] == 0
            assert totals > 0
            raw += rows
            checked += 1
        assert len(raw) == result["n_independent_items"] == (6000 if task == "phase8" else 1800)
        for arm in ["identity", "sink", "control", "historical_uncapped_sink"]:
            assert result["arms"][arm]["n_correct"] == sum(r[arm+"_correct"] for r in raw)
        for contrast, left, right in [("sink_minus_identity", "sink", "identity"),
                                      ("control_minus_identity", "control", "identity"),
                                      ("sink_minus_control", "sink", "control")]:
            if contrast == "control_minus_identity" and (task, model) == ("phase11", "Qwen/Qwen2.5-3B"):
                right = "identity_control_copy"
            effect = result[contrast]
            d = np.array([int(r[left+"_correct"])-int(r[right+"_correct"]) for r in raw])
            seed_d = [np.mean([int(r[left+"_correct"])-int(r[right+"_correct"]) for r in raw if r["seed"] == seed]) for seed in [0, 1, 2]]
            assert effect["n_independent_items"] == len(raw)
            assert effect["median_item_difference"] == np.median(d)
            assert effect["median_seed_accuracy_gain"] == np.median(seed_d)
            assert effect["pooled_accuracy_gain_secondary"] == d.mean()
            assert effect["combined_seed_stratified_permutation"]["statistic_median_seed_gain"] == np.median(seed_d)
            for seed, test in zip([0, 1, 2], effect["by_seed"]):
                selected = [r for r in raw if r["seed"] == seed]
                plus = sum(r[left+"_correct"] and not r[right+"_correct"] for r in selected)
                minus = sum(r[right+"_correct"] and not r[left+"_correct"] for r in selected)
                assert (test["edited_only_correct"], test["baseline_only_correct"], test["n_pairs"]) == (plus, minus, len(selected))
        previous = old_root[task]["models"][model]["middle"]
        historical_identity = result["arms"].get("identity_historical_batch_secondary", result["arms"]["identity"])
        assert historical_identity["n_correct"] == previous["baseline_n_correct"]
        assert result["arms"]["historical_uncapped_sink"]["n_correct"] == previous["edited_n_correct"]
        assert result["historical_uncapped_sink_minus_identity_secondary"]["median_seed_accuracy_gain"] == previous["median_seed_accuracy_gain"]
        summaries.append({"task": task, "model": model, "n": len(raw), "dtype": result["dtype"],
            "arms": result["arms"], "sink_minus_identity": result["sink_minus_identity"],
            "control_minus_identity": result["control_minus_identity"], "sink_minus_control": result["sink_minus_control"],
            "historical_uncapped_gain": result["historical_uncapped_sink_minus_identity_secondary"]["median_seed_accuracy_gain"],
            "mass_accounting": result["mass_accounting"]})
    ps = np.array([r["sink_minus_control"]["combined_seed_stratified_permutation"]["pvalue"] for r in summaries])
    order = np.argsort(ps, kind="stable")
    adjusted = np.empty(7)
    adjusted[order] = np.minimum(1., np.maximum.accumulate(ps[order]*np.arange(7, 0, -1)))
    for r, p in zip(summaries, adjusted):
        assert r["sink_minus_control"]["combined_seed_stratified_permutation"]["p_holm_family_7"] == p
    batch_path = Path("out/phase56_massmatched_batch_identity_summary_v3.json")
    batch_sanity = read(batch_path)
    assert {(r["task"], r["model"]) for r in batch_sanity["configurations"]} == set(FAMILY)
    assert all(r["source_sha256"] == sha256_file("phase56_massmatched_batch_identity.py") for r in batch_sanity["configurations"])
    assert all(r["main_protocol_sha256"] == sha256_file(PROTOCOL) for r in batch_sanity["configurations"])
    qwen_reference = root["phase11"]["models"]["Qwen/Qwen2.5-3B"]["identity_reference"]
    assert qwen_reference["n_items"] == 1800 and len(qwen_reference["full_reference_jobs"]) == 3
    audit = {"all_passed": True, "n_jobs": checked, "n_items_within_configurations": sum(r["n"] for r in summaries),
        "historical_identity_predictions_exact": True, "historical_uncapped_counts_exact": True,
        "all_attention_rows_checked": True, "no_empty_row_completion": True, "mass_match_all_passed": True,
        "paired_counts_and_estimands_reconciled": True, "holm_family_7_reconciled": True,
        "protocol_sha256": sha256_file(PROTOCOL), "auditor_sha256": sha256_file(__file__),
        "output_sha256": {f"out/{t}_massmatched_items_v3.json": sha256_file(f"out/{t}_massmatched_items_v3.json") for t in root},
        "batch_size_sanity_path": batch_path.as_posix(), "batch_size_sanity_sha256": sha256_file(batch_path),
        "batch_size_sanity_n_items": batch_sanity["n_sanity_items"],
        "batch_size_sanity_argmax_mismatches": batch_sanity["n_argmax_mismatches"],
        "original_batch_size_prediction_invariance_passed": batch_sanity["n_argmax_mismatches"] == 0,
        "batch_size_effect_addressed_by_full_qwen_reference": True,
        "full_qwen_identity_reference": qwen_reference,
        "batch_size_sanity_scope": "first original batch per seed x position, numerical sanity subset only; all main items retained",
        "summaries": summaries, "elapsed_seconds": time.perf_counter()-began}
    main_times = []
    for job in protocol["jobs"]:
        path, _ = job_paths(job["task"], job["model"], job["seed"])
        meta = read(path)
        main_times.append({"path": path.as_posix(), "worker_seconds": meta["elapsed_seconds"],
            "command": ["flock", "/tmp/radon-gpu.lock", ".venv/Scripts/python.exe", "-B", "phase53_massmatched_retrieval.py",
                        "--task", job["task"], "--model", job["model"], "--seed", str(job["seed"])]})
    native_times = [{"path": r["path"], "worker_seconds": r["elapsed_seconds"],
        "command": ["flock", "/tmp/radon-gpu.lock", ".venv/Scripts/python.exe", "-B", "phase58_massmatched_qwen_identity.py", "--seed", str(seed)]}
        for seed, r in enumerate(qwen_reference["full_reference_jobs"])]
    write_json_new("out/phase59_massmatched_timings_v3.json", {"main_jobs": main_times,
        "full_native_reference_jobs": native_times, "numerical_sanity_jobs": batch_sanity["configurations"],
        "sum_main_worker_seconds": sum(r["worker_seconds"] for r in main_times),
        "sum_native_reference_worker_seconds": sum(r["worker_seconds"] for r in native_times),
        "time_definition": "inside worker after imports and lock acquisition; includes model setup, validation and writing; excludes lock queue; no pure-CUDA cost claim",
        "first_cpu_coordinator_replaced_after_its_gpu_child_exited": True})
    write_json_new("out/phase53_massmatched_retrieval_audit_v3.json", audit)
    def ci(effect):
        a, b = effect["median_seed_gain_ci95_item_bootstrap"]
        return f"{100*effect['median_seed_accuracy_gain']:+.2f} [{100*a:+.2f}, {100*b:+.2f}]"
    lines = ["Mass-matched retrieval: medians of seed gains; paired item bootstrap within seed x position.",
        "Accuracy columns below are pooled correct-count/n (secondary); effects are paired medians of seed gains.",
        "Capped beta=.25 uses q=min(.75*sink_S, nonsink_S, nonsink_C), not the historical uncapped calibration.",
        "", "| task | model | n | identity % | sink % | control % | S-I pp IC95 | C-I pp IC95 | S-C pp IC95 | Holm7 p |",
        "|---|---|---:|---:|---:|---:|---|---|---|---:|"]
    for r in summaries:
        acc = [100*r["arms"][a]["pooled_accuracy_secondary"] for a in ["identity", "sink", "control"]]
        effects = [ci(r[k]) for k in ["sink_minus_identity", "control_minus_identity", "sink_minus_control"]]
        p = r["sink_minus_control"]["combined_seed_stratified_permutation"]["p_holm_family_7"]
        lines.append(f"| {r['task']} | {r['model']} | {r['n']} | {acc[0]:.2f} | {acc[1]:.2f} | {acc[2]:.2f} | {' | '.join(effects)} | {p:.4g} |")
    lines += ["", "| task | model | seed | sink-only correct | control-only correct | exact McNemar p |",
        "|---|---|---:|---:|---:|---:|"]
    for r in summaries:
        for test in r["sink_minus_control"]["by_seed"]:
            lines.append(f"| {r['task']} | {r['model']} | {test['seed']} | {test['edited_only_correct']} | {test['baseline_only_correct']} | {test['mcnemar_exact_pvalue']:.5g} |")
    with Path("out/phase53_massmatched_retrieval_report_v3.md").open("x", encoding="utf-8") as f:
        f.write("\n".join(lines)+"\n")
    log(f"Independent final reconciliation passed: {checked} jobs, {audit['n_items_within_configurations']} items; {audit['elapsed_seconds']:.3f}s")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
