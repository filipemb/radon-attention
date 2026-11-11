"""Continue the long E9 forwards outside the interactive tool process group.

The current coordinator deliberately exits75 only after all model validations
and a complete two-article forward probe. This supervisor resumes the same raw
files in a detached coordinator; scientific failures are reported and stop it.
"""
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent


def read(path):return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path,value):
    with Path(path).open("x",encoding="utf-8") as out:json.dump(value,out,indent=2,allow_nan=False)


def main():
    request=read(ROOT/"out/phase50_handoff_request.json");parent=request["current_coordinator_pid"]
    write(ROOT/"out/phase50_detached_supervisor.json",{"PID":os.getpid(),"created_UTC":datetime.now(timezone.utc).isoformat(),
          "awaiting_intentional_handoff_from_PID":parent,"scientific_failures_stop_execution":True})
    ready=ROOT/"out/phase50_handoff_ready.json"
    while not ready.exists():
        for path in (ROOT/"out").glob("phase50_GPU_validation_*.json"):
            record=read(path)
            if record.get("validation_performed") and record.get("passed") is False:
                raise RuntimeError(f"Preserved failed GPU validation: {path}")
        proc=Path(f"/proc/{parent}/cmdline")
        if not proc.exists() or b"phase50_run.py" not in proc.read_bytes().split(bytes([0])):
            raise RuntimeError("Interactive coordinator exited before the declared handoff; inspect its log before resuming")
        time.sleep(5)
    info=read(ready)
    if not info["intentional_handoff"]:raise RuntimeError("Unrecognized handoff state")
    for _ in range(60):
        proc=Path(f"/proc/{parent}/cmdline")
        if not proc.exists() or b"phase50_run.py" not in proc.read_bytes().split(bytes([0])):break
        time.sleep(1)
    else:raise RuntimeError("Original coordinator did not release its process after handoff")
    log=ROOT/"out/phase50_coordinator_detached_execution.log"
    with log.open("x",encoding="utf-8") as out:
        process=subprocess.Popen(["python3","-B","phase50_run.py"],cwd=ROOT,stdin=subprocess.DEVNULL,
                                 stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
        write(ROOT/"out/phase50_detached_coordinator.json",{"PID":process.pid,"log":str(log),"handoff":info,
              "started_UTC":datetime.now(timezone.utc).isoformat(),"detached_from_interactive_process_group":True})
        code=process.wait()
    if code!=0:raise subprocess.CalledProcessError(code,["python3","-B","phase50_run.py"])
    if not (ROOT/"out/phase50_complete.json").exists():raise RuntimeError("Coordinator exited without a complete audited report")
    write(ROOT/"out/phase50_detached_done.json",{"status":"complete","completed_UTC":datetime.now(timezone.utc).isoformat(),
                                              "report":"out/phase50_report.json","audit":"out/phase50_integrity_audit.json"})


if __name__=="__main__":main()
