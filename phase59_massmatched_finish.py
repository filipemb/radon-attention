"""Adopt completed main jobs; add full same-batch Qwen identity before publication.

Only the owned CPU coordinator is replaced. Its already-running GPU child is
joined and allowed to exit normally. Frozen intervention code is unchanged.
"""
import os
for key in ["OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    os.environ[key] = "4"
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import sys
import time

PY = ".venv/Scripts/python.exe"
MODEL = "Qwen/Qwen2.5-3B"
PROTOCOL = Path("out/phase53_massmatched_retrieval_protocol_v3.json")
ADDENDUM = Path("out/phase59_massmatched_batch_reference_protocol_v3.json")
LOG = Path("out/_rerun_logs/massmatched_retrieval_v3_progress.md")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(4*1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def log(message):
    with LOG.open("a", encoding="utf-8") as f:
        f.write("\n- "+datetime.now(timezone.utc).isoformat(timespec="seconds")+" | "+message+"\n")


def run_new(cmd, output, log_path):
    if not output.exists():
        began = time.perf_counter()
        log("GPU queued for same-batch completion: "+" ".join(cmd))
        with log_path.open("x", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True)
        log(f"GPU exited and lock released; observed_seconds={time.perf_counter()-began:.3f}: "+" ".join(cmd))
    return json.loads(output.read_text(encoding="utf-8"))


def coordinator():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    handoff = json.loads(Path("out/phase59_massmatched_coordinator_handoff_v3.json").read_text())
    if not ADDENDUM.exists():
        with ADDENDUM.open("x", encoding="utf-8") as f:
            json.dump({"reason": "BF16 Qwen3B sanity detected batch-size argmax drift; use full zero-edit reference in the same batch as the two edited trajectories",
                "main_protocol_sha256": digest(PROTOCOL), "main_interventions_unchanged": True,
                "scope": "all 1800 Qwen3B KV items, same seeds and positions; both zero-edit copies retained",
                "historical_identity": "retained as secondary; all six other configurations retain historical identity, numerical sanity had zero prediction mismatches",
                "source_sha256": {p: digest(p) for p in [Path(__file__).name, "phase58_massmatched_qwen_identity.py"]},
                "created_utc": datetime.now(timezone.utc).isoformat()}, f, indent=2)
    # A stopped parent can leave an exited flock child as a zombie. Z means
    # the child has exited and its GPU lock/file descriptors are released.
    child = handoff["child_flock_pid"]
    while Path(f"/proc/{child}/stat").exists():
        stat = Path(f"/proc/{child}/stat").read_text().split()
        assert stat[21] == handoff["child_start_ticks"]
        if stat[2] == "Z":
            break
        time.sleep(2)
    parent = handoff["coordinator_pid"]
    if Path(f"/proc/{parent}/stat").exists():
        stat = Path(f"/proc/{parent}/stat").read_text().split()
        assert stat[21] == handoff["coordinator_start_ticks"] and stat[2] in ["T", "t"]
        assert Path(f"/proc/{parent}/cwd").resolve() == Path.cwd()
        os.kill(parent, signal.SIGTERM)
        os.kill(parent, signal.SIGCONT)
        log(f"Terminated only stopped, owned CPU coordinator PID {parent}, after GPU child PID {child} exited normally")
    # Preserve and verify all 21 main artifacts. Only unfinished Qwen seeds
    # are launched; no completed forward is repeated or overwritten.
    for seed in [0, 1, 2]:
        tag = f"phase11_massmatched_items_Qwen__Qwen2.5-3B_s{seed}_v3"
        output = Path("out")/(tag+".json")
        cmd = ["flock", "/tmp/radon-gpu.lock", PY, "-B", "phase53_massmatched_retrieval.py",
               "--task", "phase11", "--model", MODEL, "--seed", str(seed)]
        meta = run_new(cmd, output, Path("out/_rerun_logs")/(tag+".log"))
        assert meta["source_hashes"] == protocol["source_hashes"]
        assert meta["pairs_sha256"] == digest(meta["pairs_path"])
        tag = f"phase11_massmatched_fullbatch_identity_Qwen__Qwen2.5-3B_s{seed}_v3"
        output = Path("out")/(tag+".json")
        cmd = ["flock", "/tmp/radon-gpu.lock", PY, "-B", "phase58_massmatched_qwen_identity.py", "--seed", str(seed)]
        meta = run_new(cmd, output, Path("out/_rerun_logs")/(tag+".log"))
        assert meta["pairs_sha256"] == digest(meta["pairs_path"]) and meta["n_independent_items"] == 600
    cmd = [PY, "-B", Path(__file__).name, "--aggregate-only"]
    with Path("out/_rerun_logs/massmatched_retrieval_v3_corrected_aggregation.log").open("x", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True)
    log("Same-batch corrected aggregation completed; all requested roots published once")


def aggregate():
    from phase53_massmatched_retrieval import FAMILY, analyze, contrast, hashes, job_paths
    from phase58_massmatched_qwen_identity import reference_paths
    from revision_v3_stats import holm, write_json_new
    import numpy as np
    began = time.perf_counter()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["source_hashes"] == hashes()
    addendum = json.loads(ADDENDUM.read_text(encoding="utf-8"))
    assert all(digest(p) == h for p, h in addendum["source_sha256"].items())
    results = {k: analyze(*k) for k in FAMILY}
    qwen = results["phase11", MODEL]
    joined = []
    reference_jobs = []
    n_prediction_changes = n_correct_changes = n_copy_correct_changes = 0
    for seed in [0, 1, 2]:
        refpath, refpairs = reference_paths(seed)
        ref = json.loads(refpath.read_text(encoding="utf-8"))
        assert ref["pairs_sha256"] == digest(refpairs) and ref["source_sha256"] == digest("phase58_massmatched_qwen_identity.py")
        assert ref["native_same_batch_identity_exact"] and ref["n_independent_items"] == 600
        reference = {r["trial_id"]: r for r in [json.loads(s) for s in refpairs.read_text(encoding="utf-8").splitlines()]}
        path, pairpath = job_paths("phase11", MODEL, seed)
        raw = [json.loads(s) for s in pairpath.read_text(encoding="utf-8").splitlines()]
        assert len(reference) == len(raw) == 600
        for r in raw:
            identity = reference[r["trial_id"]]
            assert (r["target_id"], r["position"], r["item"], r["identity_prediction"]) == (
                identity["target_id"], identity["position"], identity["item"], identity["original_prediction"])
            r["identity_historical_correct"] = r["identity_correct"]
            r["identity_correct"] = identity["copy1_correct"]
            r["identity_control_copy_correct"] = identity["copy2_correct"]
            joined.append(r)
        n_prediction_changes += ref["n_argmax_changed_original_copy1"]
        n_correct_changes += ref["n_correctness_changed_original_copy1"]
        n_copy_correct_changes += ref["n_correctness_changed_between_copies"]
        reference_jobs.append({"path": refpath.as_posix(), "sha256": digest(refpath), "pairs_path": refpairs.as_posix(),
            "pairs_sha256": digest(refpairs), "elapsed_seconds": ref["elapsed_seconds"]})
    def arm_summary(name):
        seeds = [{"seed": s, "n_items": 600,
                  "n_correct": sum(r[name+"_correct"] for r in joined if r["seed"] == s)} for s in [0, 1, 2]]
        for s in seeds:
            s["accuracy"] = s["n_correct"]/s["n_items"]
        return {"n_items": len(joined), "n_correct": sum(r[name+"_correct"] for r in joined),
                "pooled_accuracy_secondary": float(np.mean([r[name+"_correct"] for r in joined])),
                "median_seed_accuracy": float(np.median([s["accuracy"] for s in seeds])), "by_seed": seeds}
    qwen["arms"]["identity_historical_batch_secondary"] = qwen["arms"]["identity"]
    qwen["arms"]["identity"] = arm_summary("identity")
    qwen["arms"]["identity_control_copy"] = arm_summary("identity_control_copy")
    qwen["sink_minus_historical_identity_secondary"] = qwen["sink_minus_identity"]
    qwen["control_minus_historical_identity_secondary"] = qwen["control_minus_identity"]
    qwen["sink_minus_identity"] = contrast(joined, "sink", "identity")
    qwen["control_minus_identity"] = contrast(joined, "control", "identity_control_copy")
    qwen["identity_reference"] = {"kind": "full native zero-edit two-copy batch, same shape as edited trajectories",
        "original_batch": 4, "matched_batch": 8, "n_items": len(joined), "full_reference_jobs": reference_jobs,
        "n_predictions_changed_from_historical": n_prediction_changes,
        "n_correctness_changed_from_historical": n_correct_changes,
        "n_correctness_changed_between_native_copies": n_copy_correct_changes,
        "sink_control_contrast_unchanged": True}
    corrected = holm([results[k]["sink_minus_control"]["combined_seed_stratified_permutation"]["pvalue"] for k in FAMILY])
    for k, p in zip(FAMILY, corrected):
        results[k]["sink_minus_control"]["combined_seed_stratified_permutation"]["p_holm_family_7"] = p
    for task in ["phase8", "phase11"]:
        output = {"_meta": {"schema_version": 3, "protocol_path": PROTOCOL.as_posix(), "protocol_sha256": digest(PROTOCOL),
            "source_hashes": hashes(), "analysis_sha256": digest(__file__), "reference_addendum_path": ADDENDUM.as_posix(),
            "reference_addendum_sha256": digest(ADDENDUM), "beta_nominal": .25, "all_items_retained": True,
            "primary_family_7": protocol["primary_family_7"], "primary_contrast": "sink minus mass-matched random non-sink control",
            "budget_rule": protocol["budget_rule"], "randomization": protocol["randomization"], "statistics": protocol["statistics"],
            "primary_test": protocol["primary_test"], "qwen3b_identity": "all 1800 items rerun as native zero-edit batch8; original batch4 identity retained as secondary; interventions unchanged",
            "uncapped_reference_note": "historical uncapped calibration and its historical identity are separate secondary references",
            "elapsed_seconds_joint_aggregation": time.perf_counter()-began},
            "models": {m: r for (t, m), r in results.items() if t == task}}
        write_json_new(f"out/{task}_massmatched_items_v3.json", output)
    log(f"Joint aggregation passed with full Qwen same-batch identity: {n_prediction_changes} predictions and {n_correct_changes} correctness changes out of 1800; copies correctness differences={n_copy_correct_changes}")
    print(json.dumps({"all_main_items_retained": True, "qwen_identity_reference": qwen["identity_reference"],
        "elapsed_seconds": time.perf_counter()-began}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()
    if args.aggregate_only:
        aggregate()
    else:
        coordinator()
