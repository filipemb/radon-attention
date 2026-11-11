"""Same frozen E2(c) fit on CPU while waiting for the shared GPU.

Four threads, identical seeds / starts / 450 Adam + 150 L-BFGS-B steps. Only
the renderer's accumulation precision differs. A per-dataset Windows FileLock
prevents duplicate writers. The GPU requests a handoff; an unfinished CPU fit
is explicitly cancelled before the GPU resumes the complete JSONL prefix.
"""
import os
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
import argparse
import json
from pathlib import Path
import numpy as np
import torch
from filelock import FileLock
import richlines_parametric as parametric
from richlines_numba import NumbaRenderLines,RequestedGPUPreemption,request_path,validate
from richlines_core import LineDictionary,PROFILES,SEED,counts,digest,progress,write_json
from phase19_richlines import read_jsonl,selection_record,load_archive


def paths(model,n):
    base=Path("out")/f"phase19_fit_{model}_n{n}"
    return Path(str(base)+".lock"),Path(str(base)+".gpu_requested")


def controls(n,check):
    source=json.loads(Path(f"out/phase19_controls_cpu_n{n}.json").read_text())
    u=LineDictionary(n);p=LineDictionary(n,profiles=PROFILES)
    path=Path(f"out/phase19_controls_parametric_numba_raw_n{n}.jsonl")
    existing=read_jsonl(path)
    with path.open("a" if path.exists() else "x",encoding="utf-8") as f:
        for index,case in enumerate(source["parametric_cases"]):
            if index<len(existing):continue
            truth=np.asarray(case["truth"]);clean=parametric.render_numpy(truth,n)
            z=np.random.default_rng(case["noise_seed"]).normal(size=len(clean));z/=np.linalg.norm(z)
            b=clean+case["noise"]*np.linalg.norm(clean)*z;k=case["k"]
            result,diag=parametric.fit_parametric(b,n,[k],u,p,{k:case["uniform"]},{k:case["profiled"]},
                case["fit_seed"],device="cpu",iterations=450,return_parameters=True,oracle=truth)
            row={"k":k,"trial":case["trial"],"noise":case["noise"],**result[k],"diagnostics":diag}
            f.write(json.dumps(row,allow_nan=False)+"\n");f.flush()
            if index%4==0 or index==len(source["parametric_cases"])-1:
                progress(f"CONTROLS CPU parametric n={n}: {index+1}/64; error {row['relative']:.5g}")
    write_json(f"out/phase19_controls_parametric_numba_n{n}.json",{
        "n":n,"cases":read_jsonl(path),"renderer_validation":check,"iterations":450,
        "backend":"Numba CPU; float64 rendering/accumulation, float32 parameters and loss",
        "oracle_diagnostic_excluded_from_success_rate":True,"thresholds_unchanged":True})


def fit(n,models,check):
    control=Path(f"out/phase19_controls_parametric_numba_n{n}.json")
    if not control.exists():raise RuntimeError("Complete the identical CPU-backend controls before real fits")
    frozen=json.loads(Path("out/phase19_optimizer_stable_frozen.json").read_text())
    if any(digest(p)!=h for p,h in frozen["source_sha256"].items()):
        raise ValueError("The frozen optimizer changed")
    u=LineDictionary(n);p=LineDictionary(n,profiles=PROFILES)
    for model in models:
        lease,stop=paths(model,n)
        with FileLock(str(lease),timeout=60):
            if stop.exists():
                progress(f"CPU parametric {model} n={n}: GPU already claimed dataset; no duplicate fit")
                continue
            request_path(stop)
            record=selection_record(model,n)
            source=read_jsonl(Path(f"out/phase19_cpu_{model}_n{n}.jsonl"))
            if len(source)!=record["selected_matrices"]:raise ValueError("Incomplete CPU source")
            A=load_archive(record)
            path=Path(f"out/phase19_gpu_stable_{model}_n{n}.jsonl")
            existing=read_jsonl(path)
            if [r["instance_id"] for r in existing]!=[r["instance_id"] for r in source[:len(existing)]]:
                raise ValueError("CPU parametric resume identities do not match")
            try:
                with path.open("a" if path.exists() else "x",encoding="utf-8") as f:
                    for index in range(len(existing),len(source)):
                        if stop.exists():raise RequestedGPUPreemption(str(stop))
                        row=source[index]
                        ur={int(k):v for k,v in row["methods"]["uniform"].items()}
                        pr={int(k):v for k,v in row["methods"]["profiled"].items()}
                        result,diag=parametric.fit_parametric(A[index][u.i,u.j],n,counts(n)["parametric"],u,p,ur,pr,
                            SEED+n+row["archive_index"],device="cpu",iterations=450)
                        output={"instance_id":row["instance_id"],"methods":{"parametric":result},
                            "diagnostics":{**diag,"backend":"Numba CPU","renderer_validation":check,
                                "backend_controls":str(control),"renderer_accumulation_dtype":"float64",
                                "backend_protocol":"out/phase19_cpu_backend_protocol_frozen.json"}}
                        f.write(json.dumps(output,allow_nan=False)+"\n");f.flush()
                        progress(f"CPU parametric {model} n={n}: {index+1}/64; last {diag['seconds']:.1f}s")
            except RequestedGPUPreemption:
                progress(f"CPU parametric {model} n={n}: explicit GPU handoff; unfinished case cancelled, complete prefix preserved")
            request_path(None)


def main():
    ap=argparse.ArgumentParser();ap.add_argument("mode",choices=["controls","fit"])
    ap.add_argument("--n",type=int,required=True);ap.add_argument("--models",nargs="+",default=[])
    args=ap.parse_args();torch.set_num_threads(4);torch.set_num_interop_threads(4)
    check=validate();parametric.RenderLines=NumbaRenderLines
    if args.mode=="controls":controls(args.n,check)
    else:fit(args.n,args.models,check)


if __name__=="__main__":main()
