"""WSL stdlib orchestration: release the shared GPU lock after each model.

Run with python3 -B phase27_finish_v1.py. Numerical work uses the Windows venv.
All subprocess failures propagate; no model is skipped. Wall times include the
GPU queue, while each numerical result records its useful execution time.
"""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "4"
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shlex
import subprocess
import time

MODELS = ["gpt2", "gpt2-medium", "EleutherAI/pythia-410m", "EleutherAI/pythia-1.4b",
          "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-3B"]

def log(text):
    path = Path("out/_rerun_logs/p0_progress.md")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n- {datetime.now(timezone.utc).isoformat(timespec='seconds')} | {text}\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    args = ap.parse_args()
    started = time.perf_counter()
    for model in args.models:
        cmd = ["flock", "/tmp/radon-gpu.lock", ".venv/Scripts/python.exe", "-B",
               "phase2_downstream.py", "--models", model, "--batch", "2"]
        begin = time.perf_counter()
        log("V1 queue/start: " + shlex.join(cmd))
        subprocess.run(cmd, check=True)
        log(f"V1 command wall including queue: elapsed_seconds={time.perf_counter()-begin:.3f} | command: `{shlex.join(cmd)}`")
    if args.models == MODELS:
        cmd = [".venv/Scripts/python.exe", "-B", "phase2_downstream.py", "--aggregate-only"]
        subprocess.run(cmd, check=True)
    log(f"V1 orchestration complete: elapsed_seconds={time.perf_counter()-started:.3f}")

if __name__ == "__main__":
    main()
