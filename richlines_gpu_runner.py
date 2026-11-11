"""GPU jobs must be launched by flock; CPU attention extraction is never run."""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "4"

import argparse
import json
import time
from pathlib import Path
import numpy as np
import torch
from richlines_core import LineDictionary, PROFILES, SEED, counts, digest, omp, progress, write_json
from richlines_parametric import fit_parametric, gradient_check


def benchmark(args):
    from richlines_cuda import check_cuda_renderer
    check=check_cuda_renderer()
    n = args.n
    rng = np.random.default_rng(SEED+n)
    i,j = np.tril_indices(n)
    b = rng.lognormal(0, 1, len(i))
    u = LineDictionary(n)
    p = LineDictionary(n, profiles=PROFILES)
    ks = counts(n)["parametric"]
    ur, ud = omp(b, u, ks, save_support=True)
    pr, pd = omp(b, p, ks, save_support=True)
    progress(f"GPU synthetic benchmark n={n} preparation complete")
    result, diag = fit_parametric(b,n,ks,u,p,ur,pr,SEED,iterations=args.iterations)
    out = {"n": n, "data": "synthetic lognormal; no archived attention used",
           "gradcheck": gradient_check(), "gpu": torch.cuda.get_device_name(),
           "parametric": diag, "cuda_renderer_check":check,"omp_uniform": ud, "omp_profiled": pd,
           "errors": result}
    write_json(args.out, out)
    progress(f"GPU synthetic benchmark n={n}: all k and three starts {diag['seconds']:.2f}s")


def controls(args):
    from richlines_cuda import check_cuda_renderer
    from richlines_parametric import render_numpy
    from phase19_richlines import read_jsonl
    check=check_cuda_renderer()
    n=args.n
    source=json.loads(Path(f"out/phase19_controls_cpu_n{n}.json").read_text())
    u=LineDictionary(n);p=LineDictionary(n,profiles=PROFILES)
    path=Path(f"out/phase19_controls_gpu_stable_raw_n{n}.jsonl")
    existing=read_jsonl(path)
    with path.open("a" if path.exists() else "x",encoding="utf-8") as f:
        for index,case in enumerate(source["parametric_cases"]):
            if index<len(existing):continue
            truth=np.asarray(case["truth"])
            clean=render_numpy(truth,n)
            z=np.random.default_rng(case["noise_seed"]).normal(size=len(clean));z/=np.linalg.norm(z)
            b=clean+case["noise"]*np.linalg.norm(clean)*z
            k=case["k"]
            result,diag=fit_parametric(b,n,[k],u,p,{k:case["uniform"]},{k:case["profiled"]},
                     case["fit_seed"],iterations=args.iterations,return_parameters=True,oracle=truth)
            row={"k":k,"trial":case["trial"],"noise":case["noise"],**result[k],"diagnostics":diag}
            f.write(json.dumps(row,allow_nan=False)+"\n");f.flush()
            if index%4==0 or index==len(source["parametric_cases"])-1:
                progress(f"CONTROLS GPU n={n}: {index+1}/{len(source['parametric_cases'])}; error {row['relative']:.5g}")
    rows=read_jsonl(path)
    write_json(args.out or f"out/phase19_controls_gpu_stable_n{n}.json",
               {"n":n,"cases":rows,"cuda_renderer_check":check,"iterations":args.iterations,
                "oracle_diagnostic_excluded_from_success_rate":True})


def fit(args):
    from richlines_cuda import check_cuda_renderer
    from phase19_richlines import MODELS,read_jsonl,selection_record,load_archive
    check=check_cuda_renderer()
    from richlines_validation import validate
    numerical_validation=validate()
    frozen=json.loads(Path("out/phase19_optimizer_stable_frozen.json").read_text())
    for source,expected in frozen["source_sha256"].items():
        if digest(source)!=expected:
            raise ValueError(f"Optimizer source changed after freeze: {source}")
    if args.iterations!=frozen["adam_steps"]:
        raise ValueError("Adam step count differs from frozen protocol")
    n=args.n
    u=LineDictionary(n);p=LineDictionary(n,profiles=PROFILES)
    for model in args.models or MODELS:
        from filelock import FileLock
        lease=Path("out")/f"phase19_fit_{model}_n{n}.lock"
        stop=Path("out")/f"phase19_fit_{model}_n{n}.gpu_requested"
        if not stop.exists():
            with stop.open("x",encoding="utf-8") as f:f.write("GPU owns the global lock and requests this dataset\n")
        # A CPU fallback checks this request at each renderer evaluation. Its
        # last unfinished case is explicitly cancelled; only complete rows are
        # resumed. Both backends use this same native Windows dataset lock.
        with FileLock(str(lease),timeout=60):
            fit_dataset(args,model,n,u,p,check,numerical_validation)


def fit_dataset(args,model,n,u,p,check,numerical_validation):
        from phase19_richlines import read_jsonl,selection_record,load_archive
        source=read_jsonl(Path(f"out/phase19_cpu_{model}_n{n}.jsonl"))
        record=selection_record(model,n)
        if len(source)!=record["selected_matrices"]:
            raise ValueError("CPU stage is incomplete; no conditional GPU subset is allowed")
        A=load_archive(record)
        path=Path(f"out/phase19_gpu_stable_{model}_n{n}.jsonl")
        existing=read_jsonl(path)
        if [r["instance_id"] for r in existing]!=[r["instance_id"] for r in source[:len(existing)]]:
            raise ValueError("GPU resume identities do not match CPU selection")
        progress(f"GPU {model} n={n}: {len(existing)}/{len(source)} already complete")
        with path.open("a" if path.exists() else "x",encoding="utf-8") as f:
            for index in range(len(existing),len(source)):
                row=source[index]
                ur={int(k):v for k,v in row["methods"]["uniform"].items()}
                pr={int(k):v for k,v in row["methods"]["profiled"].items()}
                result,diag=fit_parametric(A[index][u.i,u.j],n,counts(n)["parametric"],u,p,ur,pr,
                    SEED+n+row["archive_index"],iterations=args.iterations)
                output={"instance_id":row["instance_id"],"methods":{"parametric":result},
                        "diagnostics":{**diag,"cuda_renderer_check":check,"numerical_validation":numerical_validation}}
                f.write(json.dumps(output,allow_nan=False)+"\n");f.flush()
                if index%4==0 or index==len(source)-1:
                    progress(f"GPU {model} n={n}: {index+1}/{len(source)}; last {diag['seconds']:.1f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["benchmark","controls","fit"])
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out")
    ap.add_argument("--models",nargs="+")
    ap.add_argument("--iterations", type=int, default=450)
    args = ap.parse_args()
    if os.environ.get("RICHLINE_GPU_LOCK") != "1":
        raise RuntimeError("Launch under flock /tmp/radon-gpu.lock with RICHLINE_GPU_LOCK=1")
    torch.set_num_threads(4)
    torch.set_num_interop_threads(4)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required for this worker")
    if args.mode=="benchmark":benchmark(args)
    elif args.mode=="controls":controls(args)
    else:fit(args)


if __name__ == "__main__":
    main()
