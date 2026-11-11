"""Three-worker, one-case-per-lease CPU execution of the frozen E2(c) fit.

Exact Gaussian recurrence is a numerical implementation of the same primitive,
not a different model. Dataset rotation follows availability, never loss. GPU
preemption uses the existing per-dataset request and native FileLock protocol.
"""
import os
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
import argparse,json,time
from pathlib import Path
import numpy as np
import torch
from filelock import FileLock,Timeout
import richlines_parametric as parametric
from richlines_numba import RequestedGPUPreemption,request_path
from richlines_recurrence import RecurrenceRenderLines,validate
from richlines_core import LineDictionary,PROFILES,SEED,counts,digest,progress,write_json
from richlines_cpu_parametric import paths
from phase19_richlines import read_jsonl,selection_record,load_archive

MODELS=["gpt2-medium","EleutherAI__pythia-410m","Qwen__Qwen2.5-0.5B","Qwen__Qwen2.5-3B"]
PROTOCOL=Path("out/phase19_recurrence_protocol_frozen.json")


def controls(n,check):
    source=json.loads(Path(f"out/phase19_controls_cpu_n{n}.json").read_text())
    u=LineDictionary(n);p=LineDictionary(n,profiles=PROFILES)
    path=Path(f"out/phase19_controls_parametric_recurrence_raw_n{n}.jsonl");existing=read_jsonl(path)
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
                progress(f"CONTROLS recurrence CPU n={n}: {index+1}/64; error {row['relative']:.5g}")
    write_json(f"out/phase19_controls_parametric_recurrence_n{n}.json",{
        "n":n,"cases":read_jsonl(path),"renderer_validation":check,"iterations":450,
        "backend":"exact Gaussian recurrence; float64 renderer, float32 parameters/loss",
        "oracle_diagnostic_excluded_from_success_rate":True,"thresholds_unchanged":True})


def fit(n,slot,check):
    control=Path(f"out/phase19_controls_parametric_recurrence_n{n}.json")
    if not control.exists():raise RuntimeError("Complete identical recurrence controls before real fits")
    for frozen_path in (Path("out/phase19_optimizer_stable_frozen.json"),PROTOCOL):
        frozen=json.loads(frozen_path.read_text())
        if any(digest(p)!=h for p,h in frozen["source_sha256"].items()):raise ValueError(f"Frozen source changed: {frozen_path}")
    u=LineDictionary(n);p=LineDictionary(n,profiles=PROFILES);cache={};cursor=slot;last_wait=0
    while True:
        claimed=False;pending=False
        for turn in range(len(MODELS)):
            model=MODELS[(cursor+turn)%len(MODELS)];lease_path,stop=paths(model,n)
            if stop.exists():continue
            pending=True;lease=FileLock(str(lease_path))
            try:
                lease.acquire(timeout=0)
            except Timeout:
                # A different CPU worker owns this dataset. This is a declared
                # availability condition, not an ignored fitting exception.
                continue
            try:
                if stop.exists():continue
                if model not in cache:
                    record=selection_record(model,n)
                    source=read_jsonl(Path(f"out/phase19_cpu_{model}_n{n}.jsonl"))
                    if len(source)!=record["selected_matrices"]:raise ValueError("Incomplete CPU source")
                    cache[model]=(source,load_archive(record))
                source,A=cache[model];path=Path(f"out/phase19_gpu_stable_{model}_n{n}.jsonl")
                existing=read_jsonl(path)
                if [r["instance_id"] for r in existing]!=[r["instance_id"] for r in source[:len(existing)]]:
                    raise ValueError("Recurrence resume identity mismatch")
                if len(existing)==len(source):continue
                index=len(existing);row=source[index];request_path(stop)
                ur={int(k):v for k,v in row["methods"]["uniform"].items()}
                pr={int(k):v for k,v in row["methods"]["profiled"].items()}
                try:
                    result,diag=parametric.fit_parametric(A[index][u.i,u.j],n,counts(n)["parametric"],u,p,ur,pr,
                        SEED+n+row["archive_index"],device="cpu",iterations=450,return_parameters=True)
                except RequestedGPUPreemption:
                    progress(f"Recurrence CPU slot={slot} {model} n={n}: explicit GPU handoff; unfinished case not stored")
                    continue
                output={"instance_id":row["instance_id"],"methods":{"parametric":result},
                    "diagnostics":{**diag,"backend":"Numba CPU exact recurrence","renderer_validation":check,
                        "backend_controls":str(control),"renderer_accumulation_dtype":"float64",
                        "backend_protocol":str(PROTOCOL),"slot":slot}}
                with path.open("a" if path.exists() else "x",encoding="utf-8") as f:
                    f.write(json.dumps(output,allow_nan=False)+"\n");f.flush()
                progress(f"Recurrence CPU slot={slot} {model} n={n}: {index+1}/64; last {diag['seconds']:.1f}s")
                cursor=(MODELS.index(model)+1)%len(MODELS);claimed=True
                break
            finally:
                request_path(None);lease.release()
        if claimed:continue
        if not pending:
            progress(f"Recurrence CPU slot={slot}: all remaining datasets claimed by GPU")
            return
        complete=True
        for model in MODELS:
            path=Path(f"out/phase19_gpu_stable_{model}_n{n}.jsonl")
            if not path.exists() or path.read_text().count("\n")!=64:complete=False
        if complete:
            progress(f"Recurrence CPU slot={slot}: all four n256 datasets complete")
            return
        if time.monotonic()-last_wait>45:
            progress(f"Recurrence CPU slot={slot}: waiting for a dataset lease or GPU completion")
            last_wait=time.monotonic()
        time.sleep(5)


def main():
    ap=argparse.ArgumentParser();ap.add_argument("mode",choices=["controls","fit"])
    ap.add_argument("--n",type=int,default=256);ap.add_argument("--slot",type=int,choices=[0,1,2],default=0)
    args=ap.parse_args();torch.set_num_threads(4);torch.set_num_interop_threads(4)
    check=validate();parametric.RenderLines=RecurrenceRenderLines
    if args.mode=="controls":controls(args.n,check)
    else:fit(args.n,args.slot,check)


if __name__=="__main__":main()
