"""Phase 54: controle de concentracao casado por embaralhamento de linhas.

Para cada matriz de atencao A (causal, linhas somam 1), gera B embaralhando
os valores de cada linha i apenas dentro do suporte causal (j<=i), com
semente fixa por instancia: np.random.default_rng([indice_da_instancia, 17]).
Preserva exatamente os valores de cada linha (pico, entropia e esparsidade
por linha) e destroi as linhas geometricas.

Compara o suporte efetivo de Radon (phase0_radon_attention.
radon_support_fraction, theta = arange(0,180,2)) da matriz real (reaproveitado
de out/pairs/core_{slug}_n{n}_v2.jsonl para os 6 modelos; recalculado para o
7B) com o da matriz embaralhada, em TODAS as matrizes.

CPU-only. Maximo 3 workers, OMP_NUM_THREADS=4.
"""
import os
for _key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "4"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import argparse
import json
import time
from pathlib import Path

import numpy as np

from sampling import MODELS, DATA_ROOT, load_sample, slug, sha256_file, write_json_new
from phase0_radon_attention import radon_support_fraction
from phase24_p0_metrics import describe

MODEL7 = "Qwen/Qwen2.5-7B"
DATA7 = Path("data/attn_7b")
ALL_MODELS = list(MODELS) + [MODEL7]
THETA = np.arange(0.0, 180.0, 2.0)
VERIFY_N = 20
VERIFY_ATOL = 1e-12
SANITY_SUM_ATOL = 1e-12

try:
    import torch
    torch.set_num_threads(4)
except Exception:
    pass


def root_for(model):
    return DATA7 if model == MODEL7 else DATA_ROOT


def core_pairs_path(model, n):
    if model == MODEL7:
        return None
    return Path("out/pairs") / f"core_{slug(model)}_n{n}_v2.jsonl"


def pairs_out_path(model, n):
    return Path("out/pairs") / f"phase54_{slug(model)}_n{n}.jsonl"


def rowshuffle(A, instance_index):
    """Embaralha cada linha i dentro de j<=i. A: (n,n) float64. Retorna B."""
    n = A.shape[0]
    rng = np.random.default_rng([int(instance_index), 17])
    B = np.zeros_like(A)
    for i in range(n):
        B[i, : i + 1] = rng.permutation(A[i, : i + 1])
    return B


def sanity_row(A, B):
    """Retorna (max_sum_abs_diff, sorted_mismatch_rows)."""
    sum_diff = float(np.abs(A.sum(axis=-1) - B.sum(axis=-1)).max())
    n = A.shape[0]
    bad = 0
    for i in range(n):
        if not np.array_equal(np.sort(A[i, : i + 1]), np.sort(B[i, : i + 1])):
            bad += 1
    return sum_diff, bad


def process_one(model, n):
    t0 = time.perf_counter()
    root = root_for(model)
    attention, manifest = load_sample(model, n, root=root)
    n_mat = int(manifest["n_matrices"])
    assert attention.shape == (n_mat, n, n), f"shape {attention.shape} != {(n_mat, n, n)}"
    instances = manifest["instances"]
    assert len(instances) == n_mat
    docs = [int(x["document_index"]) for x in instances]

    # Suporte real: reaproveita core para os 6 modelos; calcula para o 7B.
    cpath = core_pairs_path(model, n)
    real_supports = [None] * n_mat
    verify = {"checked": 0, "max_abs_diff": 0.0, "passed": None, "indices": []}
    if cpath is not None:
        if not cpath.exists():
            raise RuntimeError(f"Missing core pairs file {cpath}")
        stored = []
        with cpath.open("r", encoding="utf-8") as f:
            for line in f:
                stored.append(json.loads(line))
        if len(stored) != n_mat:
            raise RuntimeError(f"Core row count {len(stored)} != {n_mat} for {model} n={n}")
        for k, (srow, inst) in enumerate(zip(stored, instances)):
            if srow["instance_id"] != inst["instance_id"]:
                raise RuntimeError(f"Order mismatch at {k}: {srow['instance_id']} != {inst['instance_id']}")
        real_supports = [float(r["radon_support"]) for r in stored]
        # Confere em VERIFY_N instancias (espacadas) que o valor bate.
        idxs = sorted(set(int(x) for x in np.linspace(0, n_mat - 1, VERIFY_N).tolist()))
        maxd = 0.0
        for k in idxs:
            a = attention[k].astype(np.float64)
            frac, _ = radon_support_fraction(a, THETA)
            d = abs(float(frac) - real_supports[k])
            maxd = max(maxd, d)
        verify = {"checked": len(idxs), "max_abs_diff": float(maxd),
                  "passed": bool(maxd <= VERIFY_ATOL), "indices": idxs,
                  "atol": VERIFY_ATOL}
        if not verify["passed"]:
            raise ValueError(f"Real-support verification failed for {model} n={n}: maxdiff={maxd}")
    else:
        verify = {"checked": 0, "max_abs_diff": 0.0, "passed": True, "indices": [],
                  "atol": VERIFY_ATOL, "note": "7B has no core file; real support computed inline"}

    out_path = pairs_out_path(model, n)
    if out_path.exists():
        raise RuntimeError(f"Refusing to overwrite {out_path}; remove it to rerun")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    shuffled_supports = [0.0] * n_mat
    ratios = [0.0] * n_mat
    if cpath is None:
        real_list = [0.0] * n_mat
    else:
        real_list = real_supports

    global_sum_diff = 0.0
    global_bad_rows = 0
    with out_path.open("x", encoding="utf-8") as out:
        for i in range(n_mat):
            a = attention[i].astype(np.float64)
            if cpath is None:
                real, _ = radon_support_fraction(a, THETA)
                real_list[i] = float(real)
                real_supports[i] = float(real)
            b = rowshuffle(a, i)
            sd, bad = sanity_row(a, b)
            global_sum_diff = max(global_sum_diff, sd)
            global_bad_rows += bad
            if sd > SANITY_SUM_ATOL or bad > 0:
                raise ValueError(f"Sanity failed at instance {i} ({model} n={n}): sumdiff={sd} badrows={bad}")
            shuf, _ = radon_support_fraction(b, THETA)
            shuf = float(shuf)
            shuffled_supports[i] = shuf
            r = float(real_supports[i] / (shuf + 1e-300))
            ratios[i] = r
            inst = instances[i]
            row = {"instance_id": inst["instance_id"], "document_index": inst["document_index"],
                   "doc_id": inst["doc_id"], "layer": inst["layer"], "head": inst["head"],
                   "offset": inst["offset"], "n": n,
                   "radon_support_real": float(real_supports[i]),
                   "radon_support_shuffled": shuf,
                   "paired_ratio_real_over_shuffled": r}
            out.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
            if (i + 1) % 256 == 0:
                out.flush()
                print(f"phase54 {model} n={n}: {i+1}/{n_mat} elapsed={time.perf_counter()-t0:.1f}s", flush=True)

    d_real = describe(real_list, docs)
    d_shuf = describe(shuffled_supports, docs)
    d_ratio = describe(ratios, docs)
    med_real = float(np.median(real_list))
    med_shuf = float(np.median(shuffled_supports))
    result = {"model": model, "slug": slug(model), "n": n, "n_instances": n_mat,
              "n_documents": len(set(docs)), "pairs_path": out_path.as_posix(),
              "pairs_sha256": sha256_file(out_path),
              "manifest_sha256": sha256_file(root / f"{slug(model)}_n{n}.manifest.json"),
              "theta_step": 2.0, "seed_spec": "[instance_index, 17]",
              "median_real": med_real, "median_shuffled": med_shuf,
              "ratio_of_medians": float(med_real / (med_shuf + 1e-300)),
              "describe_real": d_real, "describe_shuffled": d_shuf,
              "describe_paired_ratio": d_ratio,
              "sanity": {"max_row_sum_abs_diff": float(global_sum_diff),
                         "sorted_mismatch_rows": int(global_bad_rows),
                         "checked_matrices": n_mat, "passed": True},
              "real_reuse_verification": verify,
              "elapsed_seconds": time.perf_counter() - t0}
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=ALL_MODELS)
    ap.add_argument("--lengths", nargs="+", type=int, default=[128, 256])
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    if args.workers < 1 or args.workers > 3:
        raise ValueError("workers must be in [1,3]")
    for m in args.models:
        if m not in ALL_MODELS:
            raise ValueError(f"Unknown model {m}")
    t_all = time.perf_counter()
    jobs = [(m, n) for m in args.models for n in args.lengths]
    from concurrent.futures import ProcessPoolExecutor
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(process_one, m, n) for (m, n) in jobs]
        for f in futs:
            results.append(f.result())
    by_key = {f"{r['slug']}_n{r['n']}": r for r in results}
    final = {"schema_version": 1, "experiment": "phase54_rowshuffle_control",
             "description": "Row-shuffle control matched on per-row values: each row i permuted within j<=i, seed [instance_index, 17]; radon_support_fraction theta=arange(0,180,2)",
             "cpu_only": True, "workers": args.workers, "omp_num_threads": "4",
             "theta_degrees": THETA.tolist(), "datasets": by_key,
             "elapsed_seconds": time.perf_counter() - t_all,
             "command": "OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase54_rowshuffle_control.py"}
    target = Path("out/phase54_rowshuffle_control.json")
    write_json_new(target, final)
    print(f"PHASE54 COMPLETE -> {target} ({len(results)} datasets, {final['elapsed_seconds']:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
