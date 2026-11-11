"""Fixed CPU pilot of the unmodified imported profiled OMP; no sampling change."""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "4"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import datasets
import json
from pathlib import Path
import time
import numpy as np
import torch
from sampling import load_sample, sha256_file
from phase06_profiled_lines import omp_profiled, precompute_band_norms

torch.set_num_threads(4)

if __name__ == "__main__":
    records = []
    for n in (128, 256):
        a, _ = load_sample("gpt2", n)
        max_k = 2 * n + 7
        checkpoints = {n, 2*n+1, max_k}
        start = time.perf_counter()
        print(f"UNMODIFIED OMP START n={n} fixed instance=0 max_k={max_k}", flush=True)
        errors, support = omp_profiled(a[0].astype(np.float64), max_k, n, checkpoints, precompute_band_norms(n))
        record = {"model": "gpt2", "n": n, "instance_index": 0, "max_k": max_k,
                  "seconds": time.perf_counter()-start, "errors": errors,
                  "support": support, "imported_OMP_source_sha256": sha256_file("phase06_profiled_lines.py")}
        records.append(record)
        print(f"UNMODIFIED OMP DONE n={n}: {record['seconds']:.3f}s errors={errors}", flush=True)
    path = Path("out/phase21_allocation_v2_omp_benchmark.json")
    with path.open("x", encoding="utf-8") as out:
        json.dump({"unmodified_function": True, "records": records}, out, indent=2, allow_nan=False)
