"""Queue current-generator CV beta jobs; never hold the GPU during CPU checks."""
from phase41_v3_run import job,run,cpu,log,PY
import json
from pathlib import Path
import time

MODELS=["gpt2","gpt2-medium","EleutherAI/pythia-410m","EleutherAI/pythia-1.4b","Qwen/Qwen2.5-0.5B"]
BETAS=["1.0","0.75","0.5","0.35","0.25","0.15","0.1","0.05","0.0","legacy_beta0"]

def main():
    began=time.perf_counter()
    protocol={"purpose":"Full phase18 from current available generator, same old seeds/grid and original per-position batches",
        "original_failure":"out/phase18_count_mismatch_gpt2_s0_b1.0_v3.json",
        "batch_diagnostic":"out/phase18_batch_diagnostic_v3.json",
        "no_generator_parameter_or_seed_search_to_match_old_counts":True,
        "historical_provenance":"FALTA: archived old family-B item IDs and generator source hashes; do not attribute old/new table changes solely to row-zero repair",
        "strict_sanities":"All corrected attention checks unchanged; every positive-beta weight checked bit-for-bit against legacy on every current item/layer",
        "counterfactual":"Legacy beta0 runs on the very same frozen items; legacy/current CV selections and held-out gains reported separately from saved old results",
        "primary_precision":"historical fp32 including Qwen0.5; separate standard bf16 Qwen0.5 full-grid supplement",
        "datasets":"Existing frozen phase18_items_*_v3 arrays, no resampling",
        "new_namespace":"phase18_posbatch_items_*_v3; failed first flat-batch job retained unchanged",
        "model_seeds":{"historical":{"models":MODELS,"seeds":[0,1,2]},
            "standard_bf16":{"models":[MODELS[-1]],"seeds":[0,1,2]}},
        "betas":BETAS,"n_gpu_jobs":180,"bootstrap":"Paired independent items within seed x position; 2000 draws, fixed seed0, conditional on selected beta",
        "selection":"Original mean middle accuracy and original grid-order/Python-float tie rule; no tuning on held-out family"}
    path=Path("out/revision_v3_cv_reproduction_protocol.json")
    if path.exists():assert json.loads(path.read_text(encoding="utf-8"))==protocol
    else:
        with path.open("x",encoding="utf-8") as f:json.dump(protocol,f,indent=2,ensure_ascii=False);f.write("\n")
    diagnostic=Path("out/phase18_batch_diagnostic_v3.json")
    if not diagnostic.exists():log("V3 CV waiting without GPU lock for the already queued original-batch diagnostic")
    while not diagnostic.exists():
        diagnostic_log=Path("out/_rerun_logs/phase18_batch_diagnostic_v3.log")
        if diagnostic_log.exists() and "Traceback" in diagnostic_log.read_text(encoding="utf-8",errors="replace"):
            raise RuntimeError("Batch diagnostic failed; preserve its log and investigate before full CV")
        time.sleep(5)
    diagnostic_result=json.loads(diagnostic.read_text(encoding="utf-8"))
    assert diagnostic_result["all_attention_sanities_passed"]
    if all(r["old_counts_reproduced"] for r in diagnostic_result["results"].values()):
        raise RuntimeError("Original batches resolved the entire mismatch; retain the strict historical reproduction gate instead")
    jobs=[]
    for beta in BETAS:
        for variant,models in [("historical",MODELS),("standard_bf16",[MODELS[-1]])]:
            for seed in range(3):
                for model in models:
                    tag=f"phase18_posbatch_items_{model.replace('/','__')}_s{seed}_{variant}_b{beta}_v3"
                    jobs.append(job("cv_current","phase45_currentcv_items.py",["--model",model,"--seed",str(seed),
                        "--variant",variant,"--beta",beta],tag))
    assert len(jobs)==180
    log("V3 current-generator CV coordinator: 180 short locked jobs; failed historical reproduction retained")
    for entry in jobs:run(entry)
    cpu([PY,"-B","phase45_currentcv_items.py","--aggregate-only"])
    log(f"V3 current-generator CV complete; wall_seconds={time.perf_counter()-began:.3f}; jobs=180")

if __name__=="__main__":main()
