"""Freeze cohorts, null draws, planted controls and all numeric code before fits."""
import phase19c_common
from pathlib import Path
from phase19c_common import read_json,write_json,digest,ROOT,SEED
from phase19c_synthetic import specs,freeze_decay_pool

def indexed_items(value):
    if isinstance(value,dict):
        if "path" in value and "sha256" in value:yield value
        for v in value.values():yield from indexed_items(v)
    elif isinstance(value,list):
        for v in value:yield from indexed_items(v)

def freeze():
    out=Path("out/phase19c_protocol.json")
    if out.exists():return read_json(out)
    parent={};inventory={}
    for path in ("out/phase19_artifacts.json","out/phase19b_artifacts.json"):
        inventory[path]=digest(path)
        for item in indexed_items(read_json(path)):
            if digest(item["path"])!=item["sha256"]:raise AssertionError(f"Parent changed before E2c: {item['path']}")
            parent[item["path"]]=item["sha256"]
    pool=freeze_decay_pool();plan=specs()
    report={"seed":SEED,"cohorts":{
        "phase19_768":{"selection_path":"out/phase19_selection.json","sha256":digest("out/phase19_selection.json"),"instances":768,"ranks":[1,2,4],
            "free":"Saved/replayed phase19b original-budget parameters, re-rendered float64; historical phase19 scores also retained",
            "thin":"New fits on all768 using original9 checkpoint union, identical seeds and original OMP starts; no reuse of11-checkpoint fits"},
        "phase19b_192":{"selection_path":"out/phase19b_selection.json","sha256":digest("out/phase19b_selection.json"),"instances":192,"ranks":[1,2,4,8,16],
            "free_and_thin":"Reuse both frozen phase19b arms, re-render float64; no new fitting or best-of replacement"}},
        "ALS":{"sweeps":2000,"initialization":"ordinary truncated SVD","objective":"||tril(A-U V^T)||F^2",
            "cost":"2*n*r <= r*(2*n+1)","regularization":0,"nonnegativity":False,"gauge":"balanced factors, UV^T unchanged",
            "block_solver":"prefix/suffix Gram eigensolve when min/max eigenvalue ratio>1e-9; otherwise direct design-matrix least squares rcond1e-12",
            "pilot_history":"Initial minimum-norm500-sweep and minimum-change500-sweep pilots retained, including failures. Final uses standard minimum norm2000 sweeps globally; no attention outcome used."},
        "parametric":{"frozen_from":"phase19b_fit.py","starts":4,"adam_steps":450,"lbfgsb_max_iterations":150,"learning_rates_unchanged":True,
            "thin_sigma":[.2,2.],"free_sigma":[.2,"n"],"all_orientations_initial_dictionary":180,"profile_grid":[0,1,-1,4,-4]},
        "negative_controls":{"uniform":"one deterministic matrix per n; no false replication or inferential p-value",
            "random":"16 iid draws per n, Q,K iid standard normal with d_k64, scaled dot product and causal softmax; no planted lines",
            "ranks":[1,2,4],"parametric_checkpoints":"original9-checkpoint union, identical raw starts for both caps"},
        "planted_controls":{"k":[51,102,205],"n":[128,256],"trials_each":8,"noise":[0,.01],"sigma":"log-uniform[.2,1]",
            "angle_decay":"joint empirical active(angle,decay) distribution from all192 free fits first3 budgets, frozen pool",
            "threshold_clean":.001,"threshold_noisy":.02,"minimum_success_rate_per_group":.9,
            "recovery":"reconstruction error threshold, no parameter-identifiability claim","checkpoints":"single planted k, same four starts and frozen optimizer"},
        "masked_positive":{"n":[128,256],"ranks":[1,2,4,8,16],"trials_each":8,"generator":"positive lognormal U,V; A=tril(UV^T), normalized rows",
            "threshold":1e-6,"minimum_success_rate_per_group":.9,"all_failures_retained":True},
        "precision":{"format":"IEEE754 binary16 direct round-to-nearest ties-to-even of every physical line parameter or factor",
            "decode":"float64","quantization_aware_refit":False,"overflow":"explicit failure with null error, never clipping or imputation",
            "costs":{"svd":"r*(2*n+1)","masked":"2*n*r","free":"5*floor(B/5)","thin":"5*floor(B/5)"}},
        "statistics":{"primary":"median of within-document paired differences,95percent document-block bootstrap CI and paired win/tie fractions",
            "bootstrap_replicates":2000,"seed":SEED,"wilcoxon":"two-sided, document median differences, method auto, zero_method wilcox",
            "primary_Holm_family":576,"primary_pairs":["free-masked","thin-masked","svd-masked","free-svd","thin-svd","free-thin"],
            "negative_random_Holm_family":36,"precision_Holm_family":576,"uniform_inference":False,
            "undefined_values":"Retain null and reason; no conditional primary aggregation"},
        "resources":{"active_calculation_processes_max":3,"threads_each":4,"gpu":"only c fitting under flock /tmp/radon-gpu.lock; pause verified own CPU slot2 while GPU active"},
        "parent_inventory_sha256":inventory,"parent_artifact_sha256":parent,"synthetic_specs":plan,
        "empirical_pool_sha256":digest(ROOT/"empirical_decay_pool.json"),
        "numeric_sources_sha256":{p.as_posix():digest(p) for p in sorted(Path('.').glob('phase19c_*.py')) if p.name not in ['phase19c_analysis.py','phase19c_audit.py','phase19c_figures.py','phase19c_inventory.py']}}
    write_json(out,report);return report

if __name__=="__main__":freeze()
