"""WSL stdlib runner: finish beta=0 after V1, one shared-lock job per model."""
import os
for key in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
import argparse
from datetime import datetime,timezone
from pathlib import Path
import shlex
import subprocess
import time

MODELS=["gpt2","gpt2-medium","EleutherAI/pythia-410m","EleutherAI/pythia-1.4b","Qwen/Qwen2.5-0.5B"]

def log(message):
    with Path("out/_rerun_logs/p0_progress.md").open("a",encoding="utf-8") as f:
        f.write(f"\n- {datetime.now(timezone.utc).isoformat(timespec='seconds')} | {message}\n")

def run(cmd):
    start=time.perf_counter();log("Queue/start: "+shlex.join(cmd))
    subprocess.run(cmd,check=True)
    log(f"Command wall including queue: elapsed_seconds={time.perf_counter()-start:.3f} | command: `{shlex.join(cmd)}`")

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--wait-for-pid",type=int)
    args=ap.parse_args();started=time.perf_counter()
    required=[Path("out/phase2_downstream_v2.json"),Path("out/phase7_editability_v2.json")]
    while not all(p.exists() for p in required):
        if args.wait_for_pid is None or not Path(f"/proc/{args.wait_for_pid}").exists():
            raise RuntimeError("V1 must finish successfully before this beta=0 repetition")
        time.sleep(10)
    pending={}
    for model in MODELS:
        cmd=["flock","/tmp/radon-gpu.lock",".venv/Scripts/python.exe","-B",
             "phase28_beta0_retest.py","--models",model,"--batch","16"]
        start=time.perf_counter();proc=subprocess.Popen(cmd)
        pending[proc.pid]=(model,cmd,proc,start)
        log(f"Beta0 queued; flock_pid={proc.pid}: {shlex.join(cmd)}")
    failures=[]
    while pending:
        for pid,(model,cmd,proc,start) in list(pending.items()):
            code=proc.poll()
            if code is not None:
                log(f"Beta0 queued model exit={code}; {model}; command wall including queue: elapsed_seconds={time.perf_counter()-start:.3f} | command: `{shlex.join(cmd)}`")
                if code!=0:failures.append((model,code))
                del pending[pid]
        if pending:time.sleep(10)
    if failures:
        raise RuntimeError(f"Beta0 queue failures (none suppressed): {failures}")
    run([".venv/Scripts/python.exe","-B","phase28_beta0_retest.py","--aggregate-only"])
    run([".venv/Scripts/python.exe","-B","phase30_validity_audit.py"])
    run([".venv/Scripts/python.exe","-B","phase25_p0_checks.py","--delivery-audit","--out","out/p0_delivery_v2.json"])
    log(f"V1/beta0 delivery complete: elapsed_seconds={time.perf_counter()-started:.3f} including prerequisite wait and GPU queues")

if __name__=="__main__":main()
