"""J1: ANOVA do sink + curvas de reconstrucao por linhas nas amostras V2 (CPU-only).

Reaproveita sem alterar: phase24_p0_metrics.describe / svd_relative_error,
phase06_profiled_lines.omp_profiled + precompute_band_norms,
phase05_line_decomposition.omp_line. Nao extrai atencao de novo; le os
npz/manifests imutaveis. float64. Sem subamostragem, sem trocar NaN por zero,
sem try/except que engole erro, mesmos k em todos os modelos.
"""
import os
for _k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_k] = "4"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import argparse
import hashlib
import json
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from sampling import MODELS, DATA_ROOT, load_sample, slug, sample_paths, sha256_file
from phase24_p0_metrics import describe, svd_relative_error
from phase06_profiled_lines import omp_profiled, precompute_band_norms
from phase05_line_decomposition import omp_line

MODEL7 = "Qwen/Qwen2.5-7B"
DATA7 = Path("data/attn_7b")
ALL_MODELS = list(MODELS) + [MODEL7]
LENGTHS = (128, 256)
ANOVA_KS = (4, 8, 16)
CURVE_KS = (1, 2, 4, 8, 16, 32)
SVD_ALL_KS = sorted(set(CURVE_KS) | {k + 2 for k in ANOVA_KS})
PAIRS_DIR = Path("out/pairs")
AGG_PATH = Path("out/phase30_anova_curves.json")
LOG_PATH = Path("out/_rerun_logs/j1_progress.md")
SANITY_TOL = 1e-12


def log(stage, message):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"\n- {stamp} | J1 {stage}: {message}\n")
    print(f"J1 {stage}: {message}", flush=True)


def sha256_bytes(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json_new_j1(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / ("j1_" + path.name + ".tmp")
    if tmp.exists():
        tmp.unlink()
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.link(tmp, path)
    tmp.unlink(missing_ok=True)


def load_dataset(model, n):
    if model == MODEL7:
        base = DATA7 / f"{slug(model)}_n{n}"
        manifest = json.loads(Path(str(base) + ".manifest.json").read_text(encoding="utf-8"))
        if manifest.get("status") != "verified":
            raise RuntimeError(f"Unverified 7B sample {base}")
        with np.load(str(base) + ".npz", allow_pickle=False) as z:
            attention = z["attention"]
        if attention.shape != (manifest["n_matrices"], n, n):
            raise RuntimeError(f"7B archive shape mismatch: {base} {attention.shape}")
        return attention, manifest
    attention, manifest = load_sample(model, n)
    if attention.shape != (manifest["n_matrices"], n, n):
        raise RuntimeError(f"Archive shape mismatch for {model} n={n}")
    return attention, manifest


def pairs_path(model, n):
    return PAIRS_DIR / f"phase30_{slug(model)}_n{n}.jsonl"


def compute_row(a, n, band_norms):
    norm = float(np.linalg.norm(a))
    if not np.isfinite(a).all() or not np.isfinite(norm) or norm <= 0:
        raise ValueError("Invalid nonfinite/zero-norm attention matrix")
    # ANOVA: mesmas formulas do run_core (phase24).
    mu, r, c = a.mean(), a.mean(-1, keepdims=True), a.mean(-2, keepdims=True)
    additive = r + c - mu
    resid_s = np.linalg.svd(a - additive, compute_uv=False)
    cc = c.ravel() - mu
    cc0_sq = float(cc[0] ** 2)
    cc_energy = float(np.dot(cc, cc))
    if not np.isfinite(cc_energy) or cc_energy <= 0:
        raise ValueError("Degenerate column effect energy")
    anova = {k: float(np.linalg.norm(resid_s[k:]) / norm) for k in ANOVA_KS}
    sink_frac = float(cc0_sq / cc_energy)
    # SVD rank-k de A via reaproveitado.
    svd = {k: svd_relative_error(a, k) for k in SVD_ALL_KS}
    # Curvas OMP (dicionario uniforme + com perfil), mesmas matrizes.
    uni, _ = omp_line(a, 32, n, set(CURVE_KS))
    prof, _ = omp_profiled(a, 32, n, set(CURVE_KS), band_norms)
    return {
        "anova": anova, "sink_frac": sink_frac, "cc0_sq": cc0_sq, "cc_energy": cc_energy,
        "uni": {k: uni[k] for k in CURVE_KS}, "prof": {k: prof[k] for k in CURVE_KS},
        "svd": svd, "norm": norm,
    }


def run_dataset(model, n):
    started = time.perf_counter()
    target_pairs = pairs_path(model, n)
    attention, manifest = load_dataset(model, n)
    nmat = manifest["n_matrices"]
    if len(manifest["instances"]) != nmat or attention.shape[0] != nmat:
        raise RuntimeError(f"Instance count mismatch {model} n={n}")
    band_norms = precompute_band_norms(n)
    # Resume: reaproveita linhas ja escritas se os ids conferem em ordem.
    done = 0
    if target_pairs.exists():
        with target_pairs.open(encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                exp = manifest["instances"][done]
                if row["instance_id"] != exp["instance_id"]:
                    raise RuntimeError(f"Pairs prefix mismatch at {done} for {model} n={n}")
                done += 1
        if done > nmat:
            raise RuntimeError(f"Pairs longer than manifest for {model} n={n}")
        log("resume", f"{model} n={n}: {done}/{nmat} linhas ja presentes")
    else:
        target_pairs.parent.mkdir(parents=True, exist_ok=True)
        target_pairs.touch(exist_ok=False)
    mode = "a" if done > 0 else "w"
    # Se o arquivo foi criado vazio via touch, reabre em w.
    with target_pairs.open(mode, encoding="utf-8") as out:
        for i in range(done, nmat):
            raw = attention[i]
            a = raw.astype(np.float64)
            vals = compute_row(a, n, band_norms)
            inst = manifest["instances"][i]
            row = {
                **inst,
                "attention_frobenius_norm": vals["norm"],
                "sink_frac_of_column_effect_energy": vals["sink_frac"],
                "sink_cc0_squared": vals["cc0_sq"],
                "column_effect_energy_sum": vals["cc_energy"],
            }
            for k in ANOVA_KS:
                row[f"anova_addrank{k}_relative_error"] = vals["anova"][k]
            for k in CURVE_KS:
                row[f"uniform_line_k{k}_relative_error"] = vals["uni"][k]
                row[f"profiled_line_k{k}_relative_error"] = vals["prof"][k]
            for k in SVD_ALL_KS:
                row[f"svd_k{k}_relative_error"] = vals["svd"][k]
            for k in CURVE_KS:
                row[f"paired_profiled_minus_svd_k{k}_relative_error"] = (
                    vals["prof"][k] - vals["svd"][k]
                )
            # Chave historica do core (k=8) para comparacao direta.
            row["paired_relative_error_line_minus_svd"] = (
                vals["prof"][8] - vals["svd"][8]
            )
            out.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
            if (i + 1) % 128 == 0 or i + 1 == nmat:
                out.flush()
                log("progress", f"{model} n={n}: {i + 1}/{nmat} ({time.perf_counter() - started:.1f}s)")
    rows = [json.loads(l) for l in target_pairs.read_text(encoding="utf-8").splitlines()]
    if len(rows) != nmat:
        raise RuntimeError(f"Incomplete pairs for {model} n={n}: {len(rows)} != {nmat}")
    docs = [r["document_index"] for r in rows]
    metric_keys = (
        [f"anova_addrank{k}_relative_error" for k in ANOVA_KS]
        + ["sink_frac_of_column_effect_energy"]
        + [f"uniform_line_k{k}_relative_error" for k in CURVE_KS]
        + [f"profiled_line_k{k}_relative_error" for k in CURVE_KS]
        + [f"svd_k{k}_relative_error" for k in SVD_ALL_KS]
        + [f"paired_profiled_minus_svd_k{k}_relative_error" for k in CURVE_KS]
        + ["paired_relative_error_line_minus_svd"]
    )
    metrics = {k: describe([r[k] for r in rows], docs) for k in metric_keys}
    cc0_sum = float(sum(r["sink_cc0_squared"] for r in rows))
    cc_sum = float(sum(r["column_effect_energy_sum"] for r in rows))
    if not np.isfinite(cc0_sum) or not np.isfinite(cc_sum) or cc_sum <= 0:
        raise ValueError(f"Degenerate aggregated column energy {model} n={n}")
    if model == MODEL7:
        manifest_sha = sha256_bytes(str(DATA7 / f"{slug(model)}_n{n}.npz"))
    else:
        manifest_sha = sha256_file(sample_paths(model, n)[1])
    entry = {
        "model": model, "slug": slug(model), "n": n, "n_instances": nmat,
        "n_documents": len(set(docs)), "manifest_sha256": manifest_sha,
        "pairs_path": target_pairs.as_posix(), "pairs_sha256": sha256_bytes(target_pairs),
        "anova_ks": list(ANOVA_KS), "curve_ks": list(CURVE_KS), "svd_ks": list(SVD_ALL_KS),
        "sink_frac_aggregated": float(cc0_sum / cc_sum),
        "sink_cc0_sum": cc0_sum, "column_effect_energy_total": cc_sum,
        "metrics": metrics, "elapsed_seconds": time.perf_counter() - started,
    }
    log("dataset-done", f"{model} n={n}: {nmat} matrizes em {entry['elapsed_seconds']:.1f}s")
    return entry


def sanity_check():
    """Compara contra os pares do core nas mesmas instancias; falha se > SANITY_TOL."""
    report = {}
    for model, fname in (
        ("Qwen/Qwen2.5-3B", "out/pairs/core_Qwen__Qwen2.5-3B_n128_v2.jsonl"),
        ("gpt2", "out/pairs/core_gpt2_n128_v2.jsonl"),
    ):
        attention, manifest = load_sample(model, 128)
        core = [json.loads(l) for l in Path(fname).read_text(encoding="utf-8").splitlines()]
        if len(core) != manifest["n_matrices"] or not all(
            c["instance_id"] == m["instance_id"] for c, m in zip(core, manifest["instances"])
        ):
            raise RuntimeError(f"Core/manifest instance mismatch for {model}")
        norms = precompute_band_norms(128)
        keys = ("prof", "svd", "anova", "sink") if model == "Qwen/Qwen2.5-3B" else ("prof", "svd")
        worst = {k: 0.0 for k in keys}
        n_exact = {k: 0 for k in keys}
        for i, raw in enumerate(attention):
            a = raw.astype(np.float64)
            norm = float(np.linalg.norm(a))
            if not np.isfinite(a).all() or norm <= 0:
                raise ValueError(f"Invalid input instance {i}")
            prof, _ = omp_profiled(a, 8, 128, {8}, norms)
            err_svd = svd_relative_error(a, 8)
            mu, r, c = a.mean(), a.mean(-1, keepdims=True), a.mean(-2, keepdims=True)
            additive = r + c - mu
            theta_s = np.linalg.svd(a - additive, compute_uv=False)
            anova8 = float(np.linalg.norm(theta_s[8:]) / norm)
            cc = c.ravel() - mu
            sink = float(cc[0] ** 2 / np.dot(cc, cc))
            cr = core[i]
            diffs = {
                "prof": abs(prof[8] - cr["profiled_line_k8_relative_error"]),
                "svd": abs(err_svd - cr["svd_k8_relative_error"]),
            }
            if model == "Qwen/Qwen2.5-3B":
                diffs["anova"] = abs(anova8 - cr["anova_addrank8_relative_error"])
                diffs["sink"] = abs(sink - cr["sink_frac_of_column_effect_energy"])
            for k, d in diffs.items():
                worst[k] = max(worst[k], d)
                if d == 0.0:
                    n_exact[k] += 1
                if not np.isfinite(d) or d > SANITY_TOL:
                    raise RuntimeError(
                        f"Sanity FAIL {model} idx={i} key={k} diff={d!r} > {SANITY_TOL}"
                    )
        report[model] = {
            "n": len(core), "tol": SANITY_TOL, "worst_abs_diff": worst, "n_exact": n_exact,
        }
        log("sanity", f"{model} n=128 OK: worst={worst} exact={n_exact}")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sanity-only", action="store_true")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    if args.workers > 3:
        raise ValueError("Maximo 3 processos")
    total_start = time.perf_counter()
    log("start", f"modelos={len(ALL_MODELS)} n={LENGTHS} workers={args.workers} OMP_NUM_THREADS=4 CPU-only")
    sanity = sanity_check()
    log("sanity-done", json.dumps(sanity, ensure_ascii=False))
    if args.sanity_only:
        print(json.dumps(sanity, indent=2))
        return
    jobs = [(m, n) for m in ALL_MODELS for n in LENGTHS]
    if args.workers == 1:
        entries = [run_dataset(m, n) for m, n in jobs]
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            entries = list(pool.map(_run_job, jobs))
    result = {
        "schema_version": 1, "cpu_only": True, "float": "float64",
        "models": ALL_MODELS, "lengths": list(LENGTHS),
        "anova_ks": list(ANOVA_KS), "curve_ks": list(CURVE_KS), "svd_ks": list(SVD_ALL_KS),
        "sanity": sanity, "sanity_tol": SANITY_TOL,
        "datasets": {f"{e['slug']}_n{e['n']}": e for e in entries},
        "elapsed_seconds": time.perf_counter() - total_start,
    }
    write_json_new_j1(AGG_PATH, result)
    log("done", f"{len(entries)} datasets em {result['elapsed_seconds']:.1f}s -> {AGG_PATH.as_posix()}")


def _run_job(job):
    return run_dataset(*job)


if __name__ == "__main__":
    main()
