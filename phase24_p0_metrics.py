"""P0 V2: CPU-only core metrics on every immutable sampled instance.

No GPU, re-extraction, replacement of nonfinite values, or conditional subsets.
Run after extract_attn.py --ready. All output paths are exclusive/versioned.
"""
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
from phase0_radon_attention import radon_support_fraction, make_controls
from phase06_profiled_lines import omp_profiled, precompute_band_norms
from phase5_msclean import build_dict, msclean

torch.set_num_threads(4)

def describe(values, document_indices, seed=0):
    a, docs = np.asarray(values, dtype=np.float64), np.asarray(document_indices)
    if not np.isfinite(a).all():
        raise ValueError("Nonfinite metric; cannot drop instances")
    unique = np.unique(docs)
    blocks = [a[docs == d] for d in unique]
    if len(set(map(len, blocks))) != 1:
        raise ValueError("Expected balanced document blocks")
    block = np.stack(blocks)
    rng = np.random.default_rng(seed)
    boots = [float(np.median(block[rng.integers(0, len(unique), len(unique))])) for _ in range(2000)]
    return {"median": float(np.median(a)), "p25": float(np.percentile(a, 25)),
            "p75": float(np.percentile(a, 75)), "mean": float(a.mean()), "std": float(a.std(ddof=1)),
            "n_instances": len(a), "n_documents": len(unique),
            "median_ci_document_bootstrap": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
            "bootstrap_seed": seed, "n_bootstrap": 2000}

def svd_relative_error(a, rank):
    s = np.linalg.svd(a, compute_uv=False)
    return float(np.sqrt(np.dot(s[rank:], s[rank:]) / np.sum(a * a)))

def core_paths(model, n):
    return (Path("out") / f"phase24_core_{slug(model)}_n{n}_v2.json",
            Path("out/pairs") / f"core_{slug(model)}_n{n}_v2.jsonl")

def run_core(model, n):
    started = time.perf_counter()
    target, pairpath = core_paths(model, n)
    attention, manifest = load_sample(model, n)
    if target.exists():
        result = json.loads(target.read_text(encoding="utf-8"))
        if result["manifest_sha256"] != sha256_file(sample_paths(model, n)[1]) or not pairpath.exists():
            raise RuntimeError(f"Stale/incomplete output {target}")
        return result
    if pairpath.exists():
        raise RuntimeError(f"Unfinished prior metrics: {pairpath}; preserve and inspect before rerun")
    theta = np.arange(0.0, 180.0, 2.0)
    norms = precompute_band_norms(n)
    _, randoms = make_controls(n, 40, np.random.default_rng(np.random.SeedSequence([0, n, 331])))
    random_support = [radon_support_fraction(a, theta)[0] for a in randoms]
    rows = []
    d, labels = build_dict(n)
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    with pairpath.open("x", encoding="utf-8") as out:
        for i, raw in enumerate(attention):
            a = raw.astype(np.float64)
            norm = np.linalg.norm(a)
            if not np.isfinite(a).all() or norm <= 0:
                raise ValueError(f"Invalid input instance {i}")
            prof, support = omp_profiled(a, 8, n, {8}, norms)
            err_svd = svd_relative_error(a, 8)
            row = {**manifest["instances"][i], "radon_support": radon_support_fraction(a, theta)[0],
                   "profiled_line_k8_relative_error": prof[8], "svd_k8_relative_error": err_svd,
                   "profiled_line_k8_absolute_error": prof[8] * norm,
                   "svd_k8_absolute_error": err_svd * norm,
                   "paired_relative_error_line_minus_svd": prof[8] - err_svd,
                   "attention_frobenius_norm": float(norm), "line_support": support}
            if model == "Qwen/Qwen2.5-3B":
                mu, r, c = a.mean(), a.mean(-1, keepdims=True), a.mean(-2, keepdims=True)
                additive = r + c - mu
                theta_s = np.linalg.svd(a - additive, compute_uv=False)
                cc = c.ravel() - mu
                clean, _ = msclean(a, d, labels, 5)
                row.update({"anova_addrank8_relative_error": float(np.linalg.norm(theta_s[8:]) / norm),
                            "sink_frac_of_column_effect_energy": float(cc[0] ** 2 / np.dot(cc, cc)),
                            "named_m5_norm_ratio": float(np.linalg.norm(clean) / norm)})
            out.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
            rows.append(row)
            if (i + 1) % 128 == 0:
                out.flush()
                print(f"CORE {model} n={n}: {i+1}/{len(attention)}, seconds={time.perf_counter()-started:.1f}", flush=True)
    docs = [r["document_index"] for r in rows]
    metrics = ["radon_support", "profiled_line_k8_relative_error", "svd_k8_relative_error",
               "profiled_line_k8_absolute_error", "svd_k8_absolute_error", "paired_relative_error_line_minus_svd"]
    if model == "Qwen/Qwen2.5-3B":
        metrics += ["anova_addrank8_relative_error", "sink_frac_of_column_effect_energy", "named_m5_norm_ratio"]
    result = {"schema_version": 2, "model": model, "n": n, "n_sequences_effective": manifest["n_sequences_processed"],
              "n_documents_effective": manifest["n_documents_effective"], "n_instances": len(rows),
              "matrices_per_layer": manifest["matrices_per_layer"], "seed": manifest["seed"],
              "manifest_sha256": sha256_file(sample_paths(model, n)[1]), "pairs_path": pairpath.as_posix(),
              "pairs_sha256": sha256_file(pairpath), "theta_degrees": theta.tolist(),
              "random_control_n": len(random_support), "random_support_median": float(np.median(random_support)),
              "metrics": {key: describe([r[key] for r in rows], docs) for key in metrics},
              "elapsed_seconds": time.perf_counter() - started}
    result["concentration_real_to_random_ratio"] = result["metrics"]["radon_support"]["median"] / result["random_support_median"]
    write_json_new(target, result)
    progress("V2 core metrics", f"{model}, n={n}, {len(rows)} raw pairs, {len(set(docs))} documents", result["elapsed_seconds"],
             "OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models " + model + " --lengths " + str(n))
    return result

def aggregate_core(results):
    by = {(r["model"], r["n"]): r for r in results}
    n128 = {m: by[m, 128] for m in MODELS if (m, 128) in by}
    if len(n128) == len(MODELS):
        path = Path("out/phase1_multimodel_v2.json")
        if not path.exists():
            write_json_new(path, {"_meta": {"source": "immutable V2 samples", "n": 128}, **n128})
    if len(by) == 12:
        path = Path("out/phase3_robustness_v2.json")
        if not path.exists():
            write_json_new(path, {"_meta": {"lengths": [128, 256]}, "datasets": list(by.values())})
        path = Path("out/phase9_bigmodel_v2.json")
        if not path.exists():
            write_json_new(path, {"model": "Qwen/Qwen2.5-3B", "by_length": {str(n): by["Qwen/Qwen2.5-3B", n] for n in (128, 256)}})

def run_legacy_mass(model, empty_diagnostic=False):
    """Exact old clamp/row-normalize formula on fixed original matrices.

    This quantifies the masking defect on unmodified attention, not a rerun of
    the old contaminated full-model trajectory. Every instance/rank is kept.
    """
    started = time.perf_counter()
    tag = "empty_rows" if empty_diagnostic else "legacy_mass"
    target = Path("out") / f"phase2_{tag}_{slug(model)}_v2.json"
    if target.exists():
        return json.loads(target.read_text(encoding="utf-8"))
    a, manifest = load_sample(model, 128)
    ranks = [1, 2, 4, 8, 16, 32]
    pairs = Path("out/pairs") / f"{tag}_{slug(model)}_v2.jsonl"
    rows = []
    with pairs.open("x", encoding="utf-8") as out:
        for i, raw in enumerate(a):
            w = raw.astype(np.float64)
            u, s, vh = np.linalg.svd(w, full_matrices=False)
            row = {**manifest["instances"][i], "by_rank": {}}
            for rank in ranks:
                rec = np.maximum((u[:, :rank] * s[:rank]) @ vh[:rank], 0)
                sums = rec.sum(-1, keepdims=True)
                old = rec / np.maximum(sums, 1e-9)
                mass = np.triu(old, 1).sum(-1)
                row["by_rank"][str(rank)] = {"mean_query_upper_mass": float(mass.mean()),
                                            "max_query_upper_mass": float(mass.max()),
                                            "last_query_upper_mass": float(mass[-1]),
                                            "old_zero_rows": int((sums <= 0).sum())}
                if empty_diagnostic:
                    empty = np.tril(rec).sum(-1) <= 0
                    row["by_rank"][str(rank)].update({"empty_after_causal_mask": int(empty.sum()),
                        "first_row_empty": bool(empty[0]), "last_row_empty": bool(empty[-1]),
                        "empty_query_indices": np.flatnonzero(empty).tolist()})
            rows.append(row)
            out.write(json.dumps(row, allow_nan=False) + "\n")
    docs = [r["document_index"] for r in rows]
    result = {"model": model, "n": 128, "n_instances": len(rows), "n_documents": 64,
              "definition": "Exact legacy SVD -> clamp -> normalize on original frozen V2 attention; not the entire contaminated legacy trajectory",
              "pairs_path": pairs.as_posix(), "by_rank": {str(k): describe([r["by_rank"][str(k)]["mean_query_upper_mass"] for r in rows], docs) for k in ranks},
              "old_zero_rows_by_rank": {str(k): sum(r["by_rank"][str(k)]["old_zero_rows"] for r in rows) for k in ranks},
              "elapsed_seconds": time.perf_counter() - started}
    if empty_diagnostic:
        result["empty_after_mask_by_rank"] = {str(k): {
            "n_empty_rows": sum(r["by_rank"][str(k)]["empty_after_causal_mask"] for r in rows),
            "n_total_rows": len(rows)*128,
            "n_matrices_affected": sum(r["by_rank"][str(k)]["empty_after_causal_mask"] > 0 for r in rows),
            "n_first_rows_empty": sum(r["by_rank"][str(k)]["first_row_empty"] for r in rows),
            "n_last_rows_empty": sum(r["by_rank"][str(k)]["last_row_empty"] for r in rows)} for k in ranks}
    write_json_new(target, result)
    progress("V1 legacy mass", f"{model}; all {len(rows)} frozen matrices x six ranks", result["elapsed_seconds"],
             ".venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass")
    return result

def main():
    started = time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--lengths", nargs="+", type=int, default=[128, 256])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--legacy-mass", action="store_true")
    ap.add_argument("--empty-row-diagnostic", action="store_true")
    args = ap.parse_args()
    if not (DATA_ROOT / "READY").exists():
        raise RuntimeError("Wait for data/attn/READY")
    mass_mode = args.legacy_mass or args.empty_row_diagnostic
    jobs = [(m, args.empty_row_diagnostic) for m in args.models] if mass_mode else [(m, n) for m in args.models for n in args.lengths]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_legacy_mass if mass_mode else run_core, *job) for job in jobs]
        results = [f.result() for f in futures]
    if mass_mode:
        filename = "out/phase2_empty_rows_v2.json" if args.empty_row_diagnostic else "out/phase2_legacy_mass_v2.json"
        write_json_new(filename, {r["model"]: r for r in results})
    else:
        aggregate_core(results)
    progress("V1 diagnostic command complete" if mass_mode else "V2 metrics command complete", f"{len(jobs)} datasets, workers={args.workers}, four CPU threads per worker",
             time.perf_counter() - started, ".venv/Scripts/python.exe -B " + " ".join(sys.argv))
    print("V1 diagnostic complete" if mass_mode else "V2 core metrics complete", flush=True)

if __name__ == "__main__":
    main()
