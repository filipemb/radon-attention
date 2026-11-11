"""Synthetic cost measurements, independent of attention outcomes."""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "4"
import argparse
import time
import numpy as np
from richlines_core import LineDictionary, PROFILES, omp, make_radon, radon_decode, progress, write_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rng = np.random.default_rng(19027 + args.n)
    n = args.n
    i, j = np.tril_indices(n)
    b = rng.lognormal(0, 1, len(i))
    out = {"n": n, "data": "synthetic lognormal; no archived attention used", "threads": 4}
    for label, profiles in (("uniform", (0.0,)), ("profiled", PROFILES)):
        start = time.perf_counter()
        d = LineDictionary(n, profiles=profiles)
        construction = time.perf_counter() - start
        result, diag = omp(b, d, [8, 32, 64, 128])
        out[label] = {"construction_seconds": construction, "dictionary": d.meta, "omp": diag,
                      "errors": result}
        progress(f"Synthetic benchmark n={n} {label}: 128 OMP steps {diag['seconds']:.2f}s")
        del d
    start = time.perf_counter()
    d, R = make_radon(n)
    # A conservative row-sum bound is adequate for a cost pilot.
    bound = float(np.max(R.T @ np.asarray(R.sum(axis=1)).ravel()))
    result, diag = radon_decode(b, R, [1, 2, 4, 8, 16, 32, (2*n+1)//2, 2*n+1, 2*(2*n+1)],
                                bound, maxiter=200)
    out["radon"] = {"total_seconds": time.perf_counter() - start, "decode": diag, "errors": result}
    progress(f"Synthetic benchmark n={n} Radon 200 iterations: {diag['seconds']:.2f}s")
    write_json(args.out, out)


if __name__ == "__main__":
    main()
