"""Resumable full E2 orchestration: three CPU workers and one locked GPU worker.

Run .venv/Scripts/python.exe -B phase19_richlines.py from WSL. Existing paired
stage prefixes are verified, never resampled. Final JSON and pair files are
exclusive creations. Individual stages remain available on the main CLI.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from phase19_richlines import (MODELS,OUT,SELECTION,aggregate,controls,geometry,
                               prepare,prepare_runtime,read_jsonl)
from richlines_core import progress


def child(command,log):
    with Path(log).open("a",encoding="utf-8") as f:
        subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,check=True)


def gpu_command(mode,n,models=None):
    command=["flock","/tmp/radon-gpu.lock","env","WSLENV=RICHLINE_GPU_LOCK","RICHLINE_GPU_LOCK=1",
             ".venv/Scripts/python.exe","-B","-u","richlines_gpu_runner.py",mode,"--n",str(n)]
    if models:command.extend(["--models",*models])
    if os.name=="nt":
        return ["wsl.exe","--cd","/mnt/c/Users/filip/radon-attention",*command]
    return command


def run():
    if (OUT/"phase19_richlines.json").exists():
        from richlines_audit import audit
        audit();progress("Existing E2 output passed the integrity audit; no files overwritten")
        return
    prepare();prepare_runtime()
    for n in (128,256):
        geometry(n)
        if not (OUT/f"phase19_controls_cpu_n{n}.json").exists():controls(n)
        if not (OUT/f"phase19_controls_gpu_stable_n{n}.json").exists():
            child(gpu_command("controls",n),OUT/"_rerun_logs"/f"e2_auto_controls_gpu{n}.log")
    selection=json.loads(SELECTION.read_text())["datasets"]
    groups=[(n,MODELS[start:start+2]) for n in (128,256) for start in (0,2,4)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        jobs=[pool.submit(child,[sys.executable,"-B","-u","phase19_richlines.py","cpu","--n",str(n),"--models",*models],
                          OUT/"_rerun_logs"/f"e2_auto_cpu{n}_{index}.log")
              for index,(n,models) in enumerate(groups)]
        pending=list(selection)
        last_progress=0
        while pending:
            for job in jobs:
                if job.done():job.result()
            ready=None
            for record in pending:
                model,n=record["model_slug"],record["n"]
                path=OUT/f"phase19_cpu_{model}_n{n}.jsonl"
                # A writer may be halfway through its final JSON line. Inspect
                # completed newlines first, then parse the complete dataset.
                complete=path.read_text().count("\n") if path.exists() else 0
                if complete==record["selected_matrices"]:
                    cpu=read_jsonl(path)
                    if len(cpu)!=record["selected_matrices"]:
                        raise ValueError(f"Invalid completed CPU stage: {path}")
                    ready=record;break
            if ready is None:
                if time.monotonic()-last_progress>45:
                    progress(f"PIPELINE waiting for CPU stage; {len(pending)} datasets remain for GPU")
                    last_progress=time.monotonic()
                time.sleep(10)
                continue
            model,n=ready["model_slug"],ready["n"]
            child(gpu_command("fit",n,[model]),OUT/"_rerun_logs"/f"e2_auto_gpu_{model}_n{n}.log")
            pending.remove(ready)
        for job in jobs:job.result()
    aggregate()
    from richlines_audit import audit
    audit()
