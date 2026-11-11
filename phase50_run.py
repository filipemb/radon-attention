"""WSL coordinator: wait for CPU matrices, release the GPU lock between models.

No third-party imports. Each child uses the repository's Windows Python.
Existing scientific outputs are immutable; unfinished JSONL files resume only
inside the relevant worker after provenance and duplicate checks.
"""
import json
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PYTHON = ".venv/Scripts/python.exe"
MODELS = ["gpt2", "gpt2-medium", "EleutherAI/pythia-410m", "EleutherAI/pythia-1.4b", "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-3B"]
EVENTS = ROOT / "out/pairs/phase50_run_events.jsonl"


def event(kind, **values):
    row={"UTC":datetime.now(timezone.utc).isoformat(),"event":kind,**values}
    with EVENTS.open("a",encoding="utf-8") as out: out.write(json.dumps(row,allow_nan=False)+"\n")
    print(json.dumps(row),flush=True)


def run(label,args,gpu=False):
    cmd=(["flock","/tmp/radon-gpu.lock"] if gpu else [])+[PYTHON,"-B",*args]
    event("stage_start",stage=label,command=cmd)
    log=ROOT/"out"/f"phase50_{label}_execution.log"
    attempt=1
    while log.exists():
        attempt+=1
        log=ROOT/"out"/f"phase50_{label}_execution_attempt{attempt:02d}.log"
    with log.open("x",encoding="utf-8") as out:
        result=subprocess.run(cmd,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
    event("stage_end",stage=label,returncode=result.returncode,log=str(log))
    if result.returncode:
        raise subprocess.CalledProcessError(result.returncode,cmd)


def main():
    EVENTS.parent.mkdir(parents=True,exist_ok=True)
    event("start",pid=__import__("os").getpid(),matrix_stage="already launched separately with3 workers")
    wait_started=time.monotonic()
    while not (ROOT/"out/phase50_matrix_summary.json").exists():
        time.sleep(30)
    event("CPU_matrix_complete",wait_seconds=time.monotonic()-wait_started)
    controls=json.loads((ROOT/"out/phase50_CPU_controls.json").read_text(encoding="utf-8"))
    if not controls["all_passed"]: raise RuntimeError("Fixed-sweep planted control failed")
    reference_log=ROOT/"out/phase50_CPU_references_execution.log"
    if not all((ROOT/"out"/f"phase50_GPU_CPU_reference_{m.replace('/','__')}.json").exists() for m in MODELS):
        attempt=1
        while reference_log.exists():
            attempt+=1; reference_log=ROOT/"out"/f"phase50_CPU_references_execution_attempt{attempt:02d}.log"
        refout=reference_log.open("x",encoding="utf-8")
        references=subprocess.Popen([PYTHON,"-B","phase50_cpu_references.py","--workers","2"],cwd=ROOT,stdout=refout,stderr=subprocess.STDOUT)
        event("CPU_reference_prepare_start",pid=references.pid,workers=2,log=str(reference_log))
    else: references=None
    while not (ROOT/"out/phase50_gpu_solver.json").exists():
        time.sleep(5)
    solver=json.loads((ROOT/"out/phase50_gpu_solver.json").read_text(encoding="utf-8"))
    chunk_documents=solver.get("chunk_documents",16)
    scheduling=ROOT/"out/phase50_execution_chunks_v2.json"
    if scheduling.exists():chunk_documents=json.loads(scheduling.read_text(encoding="utf-8"))["chunk_documents"]
    if chunk_documents%2 or 256%chunk_documents:raise ValueError("GPU scheduling chunks must preserve V1 batches and all256 articles")
    # Validate every model's GPU estimator before starting the long forwards.
    for model in MODELS:
        slug=model.replace("/","__")
        while not (ROOT/"out"/f"phase50_GPU_CPU_reference_{slug}.json").exists():
            if references is None or references.poll() is not None:
                raise RuntimeError("CPU reference preparation exited before this model completed; inspect log")
            time.sleep(5)
        validation=ROOT/"out"/f"phase50_estimator_validation_{slug}.json"
        if not validation.exists():
            run("estimator_validation_"+slug,["phase50_gpu_validation.py","--model",model,"--under-gpu-lock"],gpu=True)
        elif not json.loads(validation.read_text(encoding="utf-8"))["passed"]:
            raise RuntimeError("Preserved failed GPU validation; inspect before continuing")
    event("all_six_GPU_CPU_validations_complete")
    if references is not None:
        if references.wait()!=0: raise RuntimeError("CPU reference preparation failed")
        refout.close();references=None
    # These are the first actual two articles of the fixed256, retained in
    # the final records; this is execution scheduling, never a scored subset.
    for model in MODELS:
        slug=model.replace("/","__")
        probe=ROOT/"out"/f"phase50_forward_chunk_{slug}_000_002.json"
        target=ROOT/"out"/f"phase50_forward_{slug}.json"
        if not probe.exists() and not target.exists():
            run(f"forward_probe_{slug}",["phase50_forward.py","gpu-model","--model",model,"--under-gpu-lock",
                 "--start-document","0","--stop-document","2"],gpu=True)
    event("all_six_first_forward_batches_complete")
    for model in MODELS:
        slug=model.replace("/","__")
        target=ROOT/"out"/f"phase50_forward_{slug}.json"
        if not target.exists():
            # Each chunk consists of unchanged V1 batches. It releases the
            # shared GPU before the next chunk; all256 articles still run.
            for start in range(0,256,chunk_documents):
                end=start+chunk_documents
                chunk=ROOT/"out"/f"phase50_forward_chunk_{slug}_{start:03d}_{end:03d}.json"
                if chunk.exists():continue
                run(f"forward_{slug}_{start:03d}_{end:03d}",["phase50_forward.py","gpu-model","--model",model,"--under-gpu-lock",
                     "--start-document",str(start),"--stop-document",str(end)],gpu=True)
            if not target.exists():run("finalize_"+slug,["phase50_forward.py","finalize-model","--model",model])
        event("model_complete",model=model)
    if references is not None:
        if references.wait()!=0: raise RuntimeError("CPU reference preparation failed")
        refout.close()
    if not (ROOT/"out/phase50_forward_summary.json").exists(): run("aggregate",["phase50_forward.py","aggregate"])
    run("report",["phase50_report.py"])
    if not (ROOT/"out/phase50_integrity_audit.json").exists(): run("audit",["phase50_audit.py"])
    event("complete")


if __name__=="__main__": main()
