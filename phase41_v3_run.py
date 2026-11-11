"""WSL coordinator: one locked GPU job, release before CPU checks/bootstrap.

Mass jobs are 16 articles; CV jobs are one beta and both complete families.
Existing independently queued pilot jobs are joined by exact argv, not rerun.
"""
import os
for key in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
from datetime import datetime,timezone
from pathlib import Path
import json
import shlex
import subprocess
import time
import argparse

PY=".venv/Scripts/python.exe"
LOCK="/tmp/radon-gpu.lock"
MODELS=["gpt2","gpt2-medium","EleutherAI/pythia-410m","EleutherAI/pythia-1.4b","Qwen/Qwen2.5-0.5B","Qwen/Qwen2.5-3B"]
GRID=["1.0","0.75","0.5","0.35","0.25","0.15","0.1","0.05","0.0","legacy_beta0"]
LOG=Path("out/_rerun_logs/v3_progress.md")

def log(message):
    with LOG.open("a",encoding="utf-8") as f:f.write("\n- "+datetime.now(timezone.utc).isoformat(timespec="seconds")+" | "+message+"\n")

def exact_running(cmd):
    result=subprocess.run(["ps","-eo","pid=,args="],capture_output=True,text=True,check=True)
    matches=[];expected=" ".join(cmd)
    for line in result.stdout.splitlines():
        pieces=line.strip().split(None,1)
        if len(pieces)==2 and pieces[1]==expected:matches.append(int(pieces[0]))
    if len(matches)>1:raise RuntimeError(f"Duplicate queued job already exists: {cmd}")
    return matches[0] if matches else None

def job(kind,script,args,tag):
    return {"kind":kind,"command":["flock",LOCK,PY,"-B",script,*args],
            "output":Path("out")/(tag+".json"),"log":Path("out/_rerun_logs")/(tag+".log")}

def plan():
    mass=[];items=[];cv=[]
    for start in range(0,256,16):
        for m in MODELS:
            slug=m.replace("/","__");tag=f"phase7_massmatched_{slug}_d{start:03d}_{start+16:03d}_v3"
            mass.append(job("mass","phase37_mass_matched.py",["--model",m,"--start",str(start),"--stop",str(start+16)],tag))
    for seed in range(3):
        for task,models in [("phase8",MODELS[:5]),("phase11",["gpt2-medium",MODELS[-1]])]:
            for m in models:
                tag=f"{task}_items_{m.replace('/','__')}_s{seed}_historical_v3"
                items.append(job("items","phase38_paired_items.py",["--task",task,"--model",m,"--seed",str(seed),"--variant","historical"],tag))
    for seed in range(3):
        m=MODELS[4];tag=f"phase8_items_{m.replace('/','__')}_s{seed}_standard_bf16_v3"
        items.append(job("items","phase38_paired_items.py",["--task","phase8","--model",m,"--seed",str(seed),"--variant","standard_bf16"],tag))
    for variant,models in [("historical",MODELS[:5]),("standard_bf16",[MODELS[4]])]:
        for seed in range(3):
            for m in models:
                for beta in GRID:
                    tag=f"phase18_items_{m.replace('/','__')}_s{seed}_{variant}_b{beta}_v3"
                    entry=job("cv","phase39_betacv_items.py",["--model",m,"--seed",str(seed),"--variant",variant,"--beta",beta],tag)
                    if (m,seed,variant,beta)==("gpt2",0,"historical","1.0"):
                        entry["log"]=Path("out/_rerun_logs/phase18_items_gpt2_s0_b1.0_historical_v3.log")
                    cv.append(entry)
    ordered=[]
    for i in range(max(map(len,[mass,items,cv]))):
        for group in [mass,items,cv]:
            if i<len(group):ordered.append(group[i])
    assert len(mass)==96 and len(items)==24 and len(cv)==180 and len(ordered)==300
    return ordered

def cpu(cmd):
    begin=time.perf_counter();log("CPU start: "+shlex.join(cmd))
    with Path("out/_rerun_logs/v3_cpu_aggregation.log").open("a",encoding="utf-8") as f:
        subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
    log(f"CPU complete; wall_seconds={time.perf_counter()-begin:.3f}: {shlex.join(cmd)}")

def verify(entry):
    flag={"mass":"--mass-chunk","items":"--items-job","cv":"--cv-beta-job",
        "cv_current":"--cv-current-beta-job"}[entry["kind"]]
    cpu([PY,"-B","phase40_v3_checks.py",flag,entry["output"].as_posix()])

def run(entry):
    cmd=entry["command"];output=entry["output"];started=time.perf_counter()
    if output.exists():
        log("Cached completed output, CPU verification: "+str(output));verify(entry);return
    existing=exact_running(cmd)
    if existing is not None:
        log(f"Join already queued initial job PID={existing}: {shlex.join(cmd)}")
        while not output.exists():
            if not Path(f"/proc/{existing}").exists():
                # Final metadata is atomically published before process exit.
                time.sleep(2)
                if not output.exists():raise RuntimeError(f"Initial GPU job exited without result; see {entry['log']}")
            time.sleep(5)
    else:
        with entry["log"].open("a",encoding="utf-8") as f:
            proc=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
            log(f"GPU queue/start; flock_pid={proc.pid}: {shlex.join(cmd)}")
            while proc.poll() is None:time.sleep(5)
            if proc.returncode!=0:raise RuntimeError(f"GPU job failed exit={proc.returncode}: {shlex.join(cmd)}; see {entry['log']}")
        if not output.exists():raise RuntimeError(f"Missing completed output: {output}")
    # The flock process has exited or the initial job published its result and
    # is tearing down. No GPU lock is held by this coordinator for CPU checks.
    log(f"GPU result complete; observed_wait_and_run_seconds={time.perf_counter()-started:.3f}: {shlex.join(cmd)}")
    verify(entry)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--kinds",nargs="+",choices=["mass","items","cv"],default=["mass","items","cv"])
    args=ap.parse_args()
    started=time.perf_counter();jobs=[j for j in plan() if j["kind"] in args.kinds];counts={k:0 for k in ["mass","items","cv"]}
    protocol=Path("out/revision_v3_protocol.json")
    value={"models":MODELS,"seeds":[0,1,2],"mass_documents_per_model":256,"mass_chunk_size":16,
        "mass_contexts":["identity","anova"],"mass_nominal_betas":[0.,.25],"mass_roles_per_context":6,
        "mass_budget":"min((1-beta)*sink_sinkarm, nonsink_sinkarm, nonsink_controlarm), first absolute row q=0",
        "mass_computation":"coupled branches in one same-article forward; float64 budget construction; same row normalization",
        "mass_randomization":"seed0 article/layer hash, same nonsink ordering across contexts/betas",
        "primary_mass_family":"six models x two contexts x two betas =24 paired article Wilcoxon comparisons; Holm24",
        "probe_kv_primary_precision":"historical: Qwen0.5 fp32, Qwen3 KV bf16, other models fp32",
        "qwen05_bf16_supplement":"phase8 and full CV repeated separately at standard bf16, same frozen items",
        "item_tests":"McNemar per seed; exact within-item label permutation stratified by seed, statistic median of seed accuracy gains",
        "primary_item_family":"five probe task-models plus two KV task-models, middle window; Holm7; seed diagnostics Holm21",
        "aggregation":"median and document/item bootstrap CI95, seed0, 2000 draws; binary accuracy count/n; pooled mean gains secondary",
        "cv_grid":GRID,"cv_selection":"original mean middle accuracy and original float/Python-max tie rule",
        "cv_middle":"historical mid() uses last tested position; not silently replaced by phase13's sequence-length window",
        "cv_independence":"A/B disjoint filler slices and independent RNGs; held-out bootstrap conditional on selected beta",
        "cv_gpu_jobs":"one beta and both full families; release shared lock after each",
        "job_counts":{"mass":96,"items":24,"cv":180},"all_samples_retained":True,
        "no_existing_result_overwritten":True,"old_beta0_conclusion_source":"out/phase8_beta0_v2.json"}
    if protocol.exists():assert json.loads(protocol.read_text(encoding="utf-8"))==value
    else:
        # WSL stdlib, exclusive creation; this is not a readiness signal.
        with protocol.open("x",encoding="utf-8") as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write("\n")
    log(f"V3 coordinator started: {len(jobs)} short GPU jobs, kinds={args.kinds}; release lock before each CPU verification")
    for entry in jobs:
        run(entry);counts[entry["kind"]]+=1
        if counts["items"]==24 and not Path("out/phase8_items_v3.json").exists():
            cpu([PY,"-B","phase38_paired_items.py","--aggregate-only"])
        if counts["mass"]==96 and not Path("out/phase7_editability_v3.json").exists():
            cpu([PY,"-B","phase37_mass_matched.py","--aggregate-only"])
        if counts["cv"]==180 and not Path("out/phase18_betacv_v3.json").exists():
            cpu([PY,"-B","phase39_betacv_items.py","--aggregate-only"])
    if set(args.kinds)=={"mass","items","cv"}:
        cpu([PY,"-B","phase40_v3_checks.py"])
        log(f"V3 ALL REQUESTED WORK COMPLETE; elapsed_seconds={time.perf_counter()-started:.3f}; counts={counts}")
    else:
        log(f"V3 selected job kinds complete; elapsed_seconds={time.perf_counter()-started:.3f}; counts={counts}")

if __name__=="__main__":main()
