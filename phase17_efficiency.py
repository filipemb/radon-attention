"""P0 V5: measured CPU analysis cost of NNLS + SVD; no inference-speed claim.

Fixed rank 8, five alternating iterations, one predeclared instance per each of
64 documents, identical triples at n=128/256/512. Both dense NNLS and its exact
QR reduction are measured, with counterbalanced order and raw timing records.
"""
from sampling import load_sample, sample_paths, sha256_file, write_json_new, progress
import argparse
import json
from pathlib import Path
import platform
import sys
import time
import numpy as np
import scipy
import torch
from phase5_msclean import build_dict
from phase6_srpca import srpca, prepare_nnls
from phase26_p0_named import summary

torch.set_num_threads(4)

def select_instances(manifest):
    rng = np.random.default_rng(0)
    layers = rng.permutation(np.arange(64) % manifest["n_layers"])
    chosen = []
    for di in range(64):
        choices = [i for i, item in enumerate(manifest["instances"]) if item["document_index"] == di and item["layer"] == int(layers[di])]
        chosen.append(int(rng.choice(choices)))
    return chosen

def main():
    command_started = time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt2")
    args = ap.parse_args()
    target = Path("out/phase17_efficiency_v2.json")
    if target.exists():
        raise FileExistsError(target)
    rows, datasets, matched_triples = [], {}, None
    pairpath = Path("out/pairs/analysis_cost_v2.jsonl")
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    with pairpath.open("x", encoding="utf-8") as out:
        for n in [128, 256, 512]:
            stage_started = time.perf_counter()
            attention, manifest = load_sample(args.model, n)
            indices = select_instances(manifest)
            triples = [tuple(manifest["instances"][i][key] for key in ("doc_id", "layer", "head")) for i in indices]
            if matched_triples is not None and triples != matched_triples:
                raise RuntimeError("Timing samples differ between lengths")
            matched_triples = triples
            setup_started = time.perf_counter()
            d, _ = build_dict(n)
            dictionary_setup_seconds = time.perf_counter()-setup_started
            setup_started = time.perf_counter()
            qr = prepare_nnls(d)
            qr_setup_seconds = time.perf_counter()-setup_started
            # Declared warmup, never used as a timing sample.
            warm = attention[indices[0]].astype(np.float64)
            srpca(warm, d, 8, qr=qr, iters=1)
            for ordinal, i in enumerate(indices):
                a = attention[i].astype(np.float64)
                methods = ["dense_nnls", "qr_nnls"] if ordinal % 2 == 0 else ["qr_nnls", "dense_nnls"]
                fits = {}
                for method in methods:
                    timings = []
                    started = time.perf_counter()
                    cpu_started = time.process_time()
                    fit = srpca(a, d, 8, iters=5, qr=qr if method == "qr_nnls" else None,
                                return_components=True, timings=timings)
                    process_seconds = time.process_time()-cpu_started
                    seconds = time.perf_counter()-started
                    fits[method] = fit
                    row = {**manifest["instances"][i], "solver": method, "rank": 8, "iterations": 5,
                           "elapsed_seconds": seconds, "process_cpu_seconds": process_seconds,
                           "nnls_seconds": sum(t["nnls_seconds"] for t in timings),
                           "svd_seconds": sum(t["svd_seconds"] for t in timings),
                           "iteration_timings": timings, "relative_error": fit[0]}
                    rows.append(row); out.write(json.dumps(row, allow_nan=False)+"\n")
                discrepancy = np.linalg.norm(fits["dense_nnls"][4]-fits["qr_nnls"][4])/np.linalg.norm(a)
                if discrepancy > 1e-9 or abs(fits["dense_nnls"][0]-fits["qr_nnls"][0]) > 1e-9:
                    raise RuntimeError("Dense/QR fitting equivalence failed in cost run")
                out.flush()
            datasets[str(n)] = {"n_documents": 64, "n_benchmark_matrices": 64,
                "n_available_matrices": len(attention), "sample_indices": indices,
                "manifest_sha256": sha256_file(sample_paths(args.model, n)[1]),
                "dictionary_setup_seconds": dictionary_setup_seconds, "qr_setup_seconds": qr_setup_seconds,
                "solvers": {method: {key: summary([r[key] for r in rows if r["n"] == n and r["solver"] == method])
                            for key in ("elapsed_seconds", "nnls_seconds", "svd_seconds", "relative_error")}
                            for method in ("dense_nnls", "qr_nnls")}}
            progress("V5 analysis cost", f"n={n}; 64 paired documents, rank=8, T=5, dense and QR NNLS", time.perf_counter()-stage_started,
                     ".venv/Scripts/python.exe -B phase17_efficiency.py")
    result = {"purpose": "offline analysis fitting cost, not inference speed", "model": args.model,
              "device": "CPU", "cpu_threads": torch.get_num_threads(), "numpy": np.__version__, "scipy": scipy.__version__,
              "torch": torch.__version__, "platform": platform.platform(), "processor": platform.processor(),
              "sampling_seed": 0, "selection": "one matrix per each of 64 documents; layer counts differ by at most one; identical triples at all lengths",
              "warmup": "one QR NNLS+rank8 SVD iteration per length, excluded from timings",
              "solver_order": "counterbalanced by document parity", "rank": 8, "iterations": 5,
              "pairs_path": pairpath.as_posix(), "datasets": datasets,
              "elapsed_seconds": time.perf_counter()-command_started}
    write_json_new(target, result)
    progress("V5 command complete", "All three lengths completed; analysis cost only", result["elapsed_seconds"],
             ".venv/Scripts/python.exe -B "+" ".join(sys.argv))

if __name__ == "__main__":
    main()
