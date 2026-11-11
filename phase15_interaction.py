"""P0 V4: sink constancy per actual sequence/layer/head, never on Abar."""
from sampling import MODELS, load_sample, slug, sample_paths, sha256_file, write_json_new, progress
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import sys
import time
import numpy as np

EPSILON = 1e-12
MIN_VALID_ROWS = 8

def constancy_metrics(A):
    a = np.asarray(A, dtype=np.float64)
    if not np.isfinite(a).all():
        raise ValueError("Nonfinite attention; never replace or omit it")
    n = len(a)
    values, energies, deviations, means = [], [], [], []
    for j in range(n-MIN_VALID_ROWS+1):
        column = a[j:, j]
        energy = float(np.dot(column, column))
        mean = float(column.mean())
        deviation = float(np.sum((column-mean)**2))
        values.append(deviation/(energy+EPSILON))
        energies.append(energy); deviations.append(deviation); means.append(mean)
    return {"sink_nonconstancy_fraction": values[0],
            "control_column_nonconstancy_median": float(np.median(values[1:])),
            "sink_mean_weight": means[0], "sink_column_energy": energies[0],
            "sink_deviation_energy": deviations[0],
            "n_control_columns": len(values)-1,
            "zero_energy_control_columns": int(np.count_nonzero(np.asarray(energies[1:]) == 0)),
            "control_energy_minimum": min(energies[1:])}

def leaks(A):
    result = constancy_metrics(A)
    return result["sink_nonconstancy_fraction"], result["control_column_nonconstancy_median"]

def run_one(model, n):
    from phase26_p0_named import summary
    started = time.perf_counter()
    path = Path("out")/f"phase15_{slug(model)}_n{n}_v2.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    attention, manifest = load_sample(model, n)
    pairpath = Path("out/pairs")/f"constancy_{slug(model)}_n{n}_v2.jsonl"
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with pairpath.open("x", encoding="utf-8") as out:
        for i, a in enumerate(attention):
            row = {**manifest["instances"][i], **constancy_metrics(a)}
            rows.append(row)
            out.write(json.dumps(row, allow_nan=False)+"\n")
    keys = ["sink_nonconstancy_fraction", "control_column_nonconstancy_median", "sink_mean_weight"]
    result = {"model": model, "n": n, "n_instances": len(rows),
              "n_documents_effective": manifest["n_documents_effective"],
              "n_layer_head_pairs": len({(r["layer"], r["head"]) for r in rows}),
              "matrix_averaging_before_measurement": False,
              "denominator_epsilon": EPSILON, "minimum_valid_rows_per_column": MIN_VALID_ROWS,
              "zero_energy_control_columns_total": sum(r["zero_energy_control_columns"] for r in rows),
              "manifest_sha256": sha256_file(sample_paths(model, n)[1]), "pairs_path": pairpath.as_posix(),
              "metrics": {key: summary([r[key] for r in rows]) for key in keys},
              "by_layer": {str(layer): {key: summary([r[key] for r in rows if r["layer"] == layer]) for key in keys}
                           for layer in range(manifest["n_layers"])},
              "elapsed_seconds": time.perf_counter()-started}
    write_json_new(path, result)
    progress("V4 constancy", f"{model}, n={n}; all {len(rows)} individual forward matrices", result["elapsed_seconds"],
             ".venv/Scripts/python.exe -B phase15_interaction.py --models "+model+" --lengths "+str(n))
    return result

def main():
    started = time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--lengths", nargs="+", type=int, default=[128, 256])
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, m, n) for m in args.models for n in args.lengths]
        results = [f.result() for f in futures]
    if args.models == MODELS and args.lengths == [128, 256]:
        write_json_new("out/phase15_interaction_v2.json", {"datasets": results})
    progress("V4 command complete", f"{len(results)} datasets", time.perf_counter()-started,
             ".venv/Scripts/python.exe -B "+" ".join(sys.argv))

if __name__ == "__main__":
    main()
