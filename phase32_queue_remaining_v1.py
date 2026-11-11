"""WSL queue-only parallelism; every numerical process owns the same flock.

The first GPT-2 job is already running. Queue the five remaining models now,
then publish the aggregates as soon as all six immutable shards are complete.
The original sequential coordinator may reach cached outputs later; the model
runner checks those before loading any model or using CUDA.
"""
import os
for key in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
from datetime import datetime,timezone
from pathlib import Path
import shlex
import subprocess
import time

MODELS=["gpt2-medium","EleutherAI/pythia-410m","EleutherAI/pythia-1.4b","Qwen/Qwen2.5-0.5B","Qwen/Qwen2.5-3B"]

def log(message):
    with Path("out/_rerun_logs/p0_progress.md").open("a",encoding="utf-8") as f:
        f.write(f"\n- {datetime.now(timezone.utc).isoformat(timespec='seconds')} | {message}\n")

def main():
    jobs=[]
    for model in MODELS:
        cmd=["flock","/tmp/radon-gpu.lock",".venv/Scripts/python.exe","-B",
             "phase2_downstream.py","--models",model,"--batch","2"]
        start=time.perf_counter();proc=subprocess.Popen(cmd)
        jobs.append((model,cmd,proc,start))
        log(f"V1 queued remaining model; flock_pid={proc.pid}: {shlex.join(cmd)}")
    pending={proc.pid:(model,cmd,proc,start) for model,cmd,proc,start in jobs}
    failures=[]
    while pending:
        for pid,(model,cmd,proc,start) in list(pending.items()):
            code=proc.poll()
            if code is not None:
                log(f"V1 queued model exit={code}; {model}; command wall including queue: elapsed_seconds={time.perf_counter()-start:.3f} | command: `{shlex.join(cmd)}`")
                if code!=0:failures.append((model,code))
                del pending[pid]
        if pending:time.sleep(10)
    if failures:
        raise RuntimeError(f"V1 queue failures (none suppressed): {failures}")
    cmd=[".venv/Scripts/python.exe","-B","phase2_downstream.py","--aggregate-only"]
    start=time.perf_counter();subprocess.run(cmd,check=True)
    log(f"V1 all-six aggregates published after the locked queue: elapsed_seconds={time.perf_counter()-start:.3f} | command: `{shlex.join(cmd)}`")

if __name__=="__main__":main()
