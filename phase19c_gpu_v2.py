"""Replace one CPU worker by the GPU worker while holding the shared GPU lock.

Only the explicitly identified native Windows process is suspended. Its PID,
creation time, complete arguments and working directory are checked first.
The redirecting venv launcher is idle; the supplied PID must be its CPU child.
No numeric routine or sample selection changes during this resource handoff.
"""
import phase19c_common
import argparse
import os
from pathlib import Path
import sys
import time
import psutil
from phase19c_common import write_json,progress


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--cpu-pid",required=True,type=int)
    parser.add_argument("--cpu-created",required=True,type=float)
    args=parser.parse_args()
    if os.environ.get("RICHLINE_GPU_LOCK")!="1":
        raise RuntimeError("Run only inside flock /tmp/radon-gpu.lock")
    # A completed experiment needs no GPU and no CPU handoff.
    from phase19c_experiment import status
    if status()["complete"]:
        progress("phase19b queued GPU handoff: experiment already complete")
        return
    process=psutil.Process(args.cpu_pid)
    expected=["python.exe","-B","-u","phase19c_run.py","cpu","--slot","2"]
    if process.cmdline()!=expected or abs(process.create_time()-args.cpu_created)>1e-6:
        raise RuntimeError("CPU PID identity changed; refusing to suspend")
    if Path(process.cwd()).resolve()!=Path.cwd().resolve():
        raise RuntimeError("CPU working directory differs; refusing to suspend")
    if process.children():
        raise RuntimeError("Specify the native calculation process, not its venv launcher")
    begin=time.time();suspended=False
    try:
        process.suspend();suspended=True
        write_json("out/phase19c_v2_gpu_resource_handoff.json",{
            "cpu_pid":process.pid,"cpu_created":process.create_time(),"cpu_arguments":expected,
            "pause_time_unix":begin,"cpu_worker_slot":2,"gpu_worker_slot":3,
            "maximum_active_calculation_processes":3,"threads_each":4,
            "policy":"Two CPU workers plus GPU while lock is held; otherwise three CPU workers"})
        progress(f"phase19b GPU lock acquired: paused own CPU slot2 PID={process.pid}; two CPU workers plus GPU")
        from phase19c_run import main as worker_main
        sys.argv=["phase19c_run.py","gpu","--slot","3"]
        worker_main()
    finally:
        if suspended:
            process.resume()
            write_json("out/phase19c_v2_gpu_resource_handoff_complete.json",{
                "cpu_pid":process.pid,"resumed":True,"elapsed_seconds":time.time()-begin,
                "maximum_active_calculation_processes":3})
            progress(f"phase19b GPU released: resumed own CPU slot2 PID={process.pid}")


if __name__=="__main__":main()
