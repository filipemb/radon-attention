"""P0 V3: all named-channel measurements, with complete raw instance pairs."""
from sampling import (MODELS, DATA_ROOT, load_sample, slug, sample_paths, sha256_file,
                      write_json_new, progress)
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import sys
import time
import numpy as np
import torch
from phase5_msclean import build_dict, msclean, fraction_metrics
from phase6_srpca import srpca, prepare_nnls

torch.set_num_threads(4)

def summary(values):
    a = np.array(values, dtype=np.float64)
    if not np.isfinite(a).all() or not len(a):
        raise ValueError("Cannot silently omit nonfinite/missing measurements")
    return {"median": float(np.median(a)), "p25": float(np.percentile(a, 25)),
            "p75": float(np.percentile(a, 75)), "mean": float(a.mean()),
            "std": float(a.std(ddof=1)), "n_instances": len(a)}

def check_qr_equivalence(attention, d, qr):
    indices = np.linspace(0, len(attention)-1, 8, dtype=int)
    maximum = 0.0
    for index in indices:
        a = attention[index].astype(np.float64)
        dense = srpca(a, d, 8, return_components=True)
        reduced = srpca(a, d, 8, qr=qr, return_components=True)
        s_error = np.linalg.norm(dense[4]-reduced[4])/np.linalg.norm(a)
        objective_error = abs(dense[0]-reduced[0])
        maximum = max(maximum, float(s_error), objective_error)
        if max(s_error, objective_error) > 1e-9:
            raise RuntimeError(f"Dense/QR NNLS equivalence failed on instance {index}: {s_error}, {objective_error}")
    return {"n_checked": len(indices), "indices": indices.tolist(), "atol": 1e-9,
            "max_named_relative_or_objective_error": maximum}

def run_named(model, n, methods=("msclean", "srpca")):
    started = time.perf_counter()
    method_tag = "_".join(methods)
    target = Path("out") / f"phase26_named_{slug(model)}_n{n}_{method_tag}_v2.json"
    if target.exists():
        result = json.loads(target.read_text(encoding="utf-8"))
        if result["methods"] != list(methods):
            raise RuntimeError("Existing named output has different methods")
        return result
    attention, manifest = load_sample(model, n)
    d, labels = build_dict(n)
    qr = prepare_nnls(d) if "srpca" in methods else None
    equivalence = check_qr_equivalence(attention, d, qr) if qr is not None else None
    pairpath = Path("out/pairs") / f"named_{slug(model)}_n{n}_{method_tag}_v2.jsonl"
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if pairpath.exists():
        with pairpath.open(encoding="utf-8") as f:
            rows = [json.loads(line) for line in f]
        for i, row in enumerate(rows):
            if row["instance_id"] != manifest["instances"][i]["instance_id"] or row["methods"] != list(methods):
                raise RuntimeError("Partial named results do not match the frozen run")
    label_index = {label: i for i, label in enumerate(labels)}
    with pairpath.open("a", encoding="utf-8") as out:
        for i in range(len(rows), len(attention)):
            a = attention[i].astype(np.float64)
            row = {**manifest["instances"][i], "methods": list(methods), "configurations": {}}
            if "msclean" in methods:
                _, picks = msclean(a, d, labels, 5)
                for m in [1, 3, 5]:
                    clean = np.zeros(n*n)
                    for label, coef in picks[:m]:
                        clean += coef*d[:, label_index[label]]
                    s = clean.reshape(n, n)
                    u, singular, vh = np.linalg.svd(a-s, full_matrices=False)
                    for rank in [0, 4, 8, 16]:
                        l = (u[:, :rank]*singular[:rank])@vh[:rank] if rank else np.zeros_like(a)
                        row["configurations"][f"msclean_m{m}_r{rank}"] = {
                            **fraction_metrics(a, s, l), "n_selected_atoms": min(m, len(picks))}
                row["greedy_picks"] = picks
            if "srpca" in methods:
                for rank in [4, 8, 16]:
                    error, norm_ratio, legacy_active, coef, s, l, trace = srpca(a, d, rank, qr=qr, return_components=True)
                    metrics = fraction_metrics(a, s, l)
                    if abs(metrics["reconstruction_relative_error"]-error) > 1e-12:
                        raise RuntimeError("Reported and recomputed decomposition error disagree")
                    row["configurations"][f"srpca_r{rank}"] = {**metrics,
                        "n_nonzero_coefficients": int(np.count_nonzero(coef)),
                        "n_active_legacy_threshold": legacy_active, "iteration_relative_squared_error": trace}
            out.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
            rows.append(row)
            if (i+1) % 128 == 0:
                out.flush()
                print(f"NAMED {model} n={n}: {i+1}/{len(attention)}, seconds={time.perf_counter()-started:.1f}", flush=True)
    configurations = {}
    for key, metrics in rows[0]["configurations"].items():
        configurations[key] = {metric: summary([r["configurations"][key][metric] for r in rows])
                               for metric, value in metrics.items() if isinstance(value, (float, int))}
    result = {"schema_version": 2, "model": model, "n": n, "methods": list(methods),
              "n_documents_effective": manifest["n_documents_effective"], "n_instances": len(rows),
              "manifest_sha256": sha256_file(sample_paths(model, n)[1]), "pairs_path": pairpath.as_posix(),
              "pairs_sha256": sha256_file(pairpath), "all_configurations_use_same_instances": True,
              "iterations_srpca": 5, "qr_nnls_equivalence": equivalence,
              "definitions": {"named_norm_ratio": "||S||_F/||A||_F", "named_energy_ratio": "||S||_F^2/||A||_F^2",
                  "cross_term_SL_over_A_energy": "2<S,L>/||A||_F^2; may be negative",
                  "named_error_reduction_energy": "1-||A-S||_F^2/||A||_F^2",
                  "total_error_reduction_energy": "1-||A-S-L||_F^2/||A||_F^2"},
              "configurations": configurations, "elapsed_seconds": time.perf_counter()-started}
    write_json_new(target, result)
    progress("V3 named metrics", f"{model}, n={n}, all {len(rows)} instances and {len(configurations)} configurations",
             result["elapsed_seconds"], ".venv/Scripts/python.exe -B phase26_p0_named.py --models " + model + " --lengths " + str(n))
    return result

def main(default_methods=None):
    started = time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--lengths", nargs="+", type=int, default=[128, 256])
    ap.add_argument("--methods", nargs="+", choices=["msclean", "srpca"], default=default_methods or ["msclean", "srpca"])
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    if not (DATA_ROOT/"READY").exists():
        raise RuntimeError("V2 archives are not ready")
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_named, m, n, tuple(args.methods)) for m in args.models for n in args.lengths]
        results = [f.result() for f in futures]
    if args.models == MODELS and args.lengths == [128, 256]:
        for method, filename in [("msclean", "phase5_msclean_v2.json"), ("srpca", "phase6_srpca_v2.json")]:
            if method in args.methods:
                path = Path("out")/filename
                if not path.exists():
                    write_json_new(path, {"method": method, "datasets": results})
        path = Path("out/phase9_bigmodel_named_v2.json")
        if set(args.methods) == {"msclean", "srpca"} and not path.exists():
            write_json_new(path, {"datasets": [r for r in results if r["model"] == "Qwen/Qwen2.5-3B"]})
    progress("V3 command complete", f"{len(results)} datasets; methods={args.methods}", time.perf_counter()-started,
             ".venv/Scripts/python.exe -B " + " ".join(sys.argv))

if __name__ == "__main__":
    main()
