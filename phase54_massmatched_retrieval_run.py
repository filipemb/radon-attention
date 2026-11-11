"""WSL coordinator: short exclusive GPU jobs, bootstrap after lock release."""
import os
for key in ["OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    os.environ[key] = "4"
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import time

PY = ".venv/Scripts/python.exe"
LOG = Path("out/_rerun_logs/massmatched_retrieval_v3_progress.md")
PROTOCOL = Path("out/phase53_massmatched_retrieval_protocol_v3.json")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(4*1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def log(message):
    with LOG.open("a", encoding="utf-8") as f:
        f.write("\n- " + datetime.now(timezone.utc).isoformat(timespec="seconds") + " | " + message + "\n")


def main():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    timings = []
    for job in protocol["jobs"]:
        task, model, seed = job["task"], job["model"], job["seed"]
        tag = f"{task}_massmatched_items_{model.replace('/', '__')}_s{seed}_v3"
        output = Path("out") / (tag+".json")
        cmd = ["flock", "/tmp/radon-gpu.lock", PY, "-B", "phase53_massmatched_retrieval.py",
               "--task", task, "--model", model, "--seed", str(seed)]
        began = time.perf_counter()
        if not output.exists():
            log("GPU queue/start: " + shlex.join(cmd))
            path = Path("out/_rerun_logs") / (tag+".log")
            with path.open("x", encoding="utf-8") as f:
                subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True)
        meta = json.loads(output.read_text(encoding="utf-8"))
        assert meta["source_hashes"] == protocol["source_hashes"]
        assert meta["protocol_sha256"] == digest(PROTOCOL)
        assert meta["pairs_sha256"] == digest(meta["pairs_path"])
        assert meta["n_independent_items"] == job["n_independent_items"]
        assert meta["all_historical_identity_predictions_exact"] and meta["native_identity_logits_bit_equal"]
        timing = {"command": cmd, "output": output.as_posix(), "worker_seconds": meta["elapsed_seconds"],
                  "observed_queue_and_wall_seconds": time.perf_counter()-began}
        timings.append(timing)
        log(f"GPU complete, lock released: {tag}; worker_seconds={meta['elapsed_seconds']:.3f}; observed={timing['observed_queue_and_wall_seconds']:.3f}s")
        print(json.dumps(timing), flush=True)
    cmd = [PY, "-B", "phase53_massmatched_retrieval.py", "--aggregate-only"]
    began = time.perf_counter()
    with Path("out/_rerun_logs/massmatched_retrieval_v3_aggregation.log").open("x", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True)
    output = Path("out/phase53_massmatched_retrieval_timings_v3.json")
    with output.open("x", encoding="utf-8") as f:
        json.dump({"jobs": timings, "n_gpu_jobs": len(timings), "aggregation_command": cmd,
                   "aggregation_wall_seconds": time.perf_counter()-began}, f, indent=2, allow_nan=False)
        f.write("\n")
    log("All 21 jobs and joint Holm7 aggregation completed")


if __name__ == "__main__":
    main()
