"""Declared batch-size sanity: first original batch in every seed/position.

This is a numerical sanity subset, never used to estimate task performance.
The complete main cohorts remain 6000 and 1800 items per configuration.
"""
import os
for key in ["OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    os.environ[key] = "4"
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

PROTOCOL = Path("out/phase53_massmatched_retrieval_protocol_v3.json")
PY = ".venv/Scripts/python.exe"


def gpu_job(task, model):
    from revision_v3_probes import load_probe, dtype_for
    from revision_v3_stats import sha256_file, write_json_new, slug
    from phase53_massmatched_retrieval import historical, log
    import torch
    from transformers import AutoModelForCausalLM
    torch.set_num_threads(4)
    began = time.perf_counter()
    tag = f"{task}_massmatched_batch_identity_{slug(model)}_v3"
    output = Path("out")/(tag+".json")
    if output.exists():
        raise FileExistsError(output)
    source = sha256_file(__file__)
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    for p, expected in protocol["source_hashes"].items():
        assert sha256_file(p) == expected
    batch = 16 if task == "phase8" else (4 if model == "Qwen/Qwen2.5-3B" else 8)
    arrays, manifest = load_probe(task, model, 0)
    dtype = dtype_for(task, model, "historical")
    obj = AutoModelForCausalLM.from_pretrained(model, revision=manifest["revision"],
        dtype=dtype, attn_implementation="eager", local_files_only=True).to("cuda").eval()
    rows = []
    max_difference = 0.
    with torch.inference_mode():
        for seed in [0, 1, 2]:
            arrays, manifest = load_probe(task, model, seed)
            old, _ = historical(task, model, seed, arrays, manifest)
            for pos in manifest["positions"]:
                if not .25*manifest["n"] <= pos <= .75*manifest["n"]:
                    continue
                indices = [i for i, p in enumerate(arrays["positions"]) if p == pos][:batch]
                x = torch.tensor(arrays["input_ids"][indices], device="cuda")
                baseline = obj(x).logits[:, -1, :].clone()
                doubled = obj(x.repeat(2, 1)).logits[:, -1, :].clone()
                assert bool(torch.isfinite(baseline).all()) and bool(torch.isfinite(doubled).all())
                error = float((doubled.float()-baseline.repeat(2, 1).float()).abs().max())
                max_difference = max(max_difference, error)
                a = baseline.argmax(-1).cpu().tolist()
                b = doubled.argmax(-1).cpu().tolist()
                for j, i in enumerate(indices):
                    assert a[j] == old["1.0", i]["prediction_id"]
                    rows.append({"seed": seed, "position": int(pos), "trial_id": i,
                        "original_batch_prediction": a[j], "doubled_copy1_prediction": b[j],
                        "doubled_copy2_prediction": b[len(indices)+j],
                        "prediction_changed": a[j] != b[j] or a[j] != b[len(indices)+j]})
                del x, baseline, doubled
    mismatches = sum(r["prediction_changed"] for r in rows)
    result = {"task": task, "model": model, "dtype": str(dtype),
        "n_independent_sanity_items": len(rows), "sanity_subset_rule": "first original batch in each seed x middle-position cell; fixed before this diagnostic",
        "main_cohort_not_subsampled": True, "original_batch": batch, "doubled_batch": 2*batch,
        "n_argmax_mismatches": mismatches, "max_logit_absolute_difference": max_difference,
        "all_original_batch_predictions_exact_historical": True, "rows": rows,
        "source_sha256": source, "main_protocol_sha256": sha256_file(PROTOCOL),
        "elapsed_seconds": time.perf_counter()-began}
    write_json_new(output, result)
    log(f"Batch-size sanity {task} {model}: {len(rows)} items, {mismatches} argmax differences; max logits={max_difference}; {result['elapsed_seconds']:.3f}s")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}), flush=True)


def run_all():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    records = []
    for task, model in protocol["primary_family_7"]:
        tag = f"{task}_massmatched_batch_identity_{model.replace('/', '__')}_v3"
        path = Path("out")/(tag+".json")
        cmd = ["flock", "/tmp/radon-gpu.lock", PY, "-B", Path(__file__).name, "--task", task, "--model", model]
        if not path.exists():
            with (Path("out/_rerun_logs")/(tag+".log")).open("x", encoding="utf-8") as f:
                subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True)
        result = json.loads(path.read_text(encoding="utf-8"))
        record = {k: v for k, v in result.items() if k != "rows"}
        record["command"] = cmd
        records.append(record)
        print(json.dumps(record), flush=True)
    output = Path("out/phase56_massmatched_batch_identity_summary_v3.json")
    with output.open("x", encoding="utf-8") as f:
        json.dump({"configurations": records, "n_sanity_items": sum(r["n_independent_sanity_items"] for r in records),
            "n_argmax_mismatches": sum(r["n_argmax_mismatches"] for r in records)}, f, indent=2, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    if "--run-all" in sys.argv:
        run_all()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--task", required=True, choices=["phase8", "phase11"])
        parser.add_argument("--model", required=True)
        args = parser.parse_args()
        gpu_job(args.task, args.model)
