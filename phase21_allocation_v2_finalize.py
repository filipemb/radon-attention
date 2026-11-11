"""Assemble immutable E4 v2 results/review and emit the requested tables.

--review uses explicitly marked full-dictionary endpoint candidates. Final mode
requires the recorded line-protocol choice and complete final paired ledgers.
"""
import phase21_allocation_v2 as e4
from datetime import datetime,timezone
import argparse
import json
import os
import platform
import scipy
import sys
from pathlib import Path
import numpy as np
from sampling import MODELS,sample_paths,sha256_file,slug
from phase21_allocation_v2_lines import paths,DECISIONS


def matrix_path(model,n,review):
    if review:return Path("out")/f"phase21_allocation_v2_endpoint_preview_{slug(model)}_n{n}.json"
    return paths(model,n)[0]


def cutoff_audit(model,n):
    counts={str(K):{mode:{key:0 for key in ("boundary_exists","exact_tie","numerical_tie","positive_numerical_tie")}
                   for mode in ("named_first_residual_q","SVD_K")} for K in e4.BUDGET_RANKS}
    nonzero_named=0;n_instances=0
    with e4.core_paths(model,n)[1].open(encoding="utf-8") as inp:
        for line in inp:
            row=json.loads(line)
            n_instances+=1
            m=int(np.count_nonzero(np.asarray(row["named_first_coefficients"])>0))
            nonzero_named+=int(m>0)
            for K in e4.BUDGET_RANKS:
                if 2*m+(K-1)*(2*n+1)>K*(2*n+1):raise ArithmeticError("Asymmetric cap violation")
                for mode,s,rank in (("named_first_residual_q",row["named_first_residual_singular_values"],K-1),
                                    ("SVD_K",row["attention_singular_values"],K)):
                    cut=e4.v1.cutoff(np.asarray(s),rank,n)
                    for key in counts[str(K)][mode]:counts[str(K)][mode][key]+=int(cut[key])
    if nonzero_named!=n_instances:raise ArithmeticError("Cannot claim fixed q is the largest feasible rank when S=0")
    return {"cutoff_counts":counts,"nonzero_named_projection_instances":nonzero_named,
            "fixed_q_equals_largest_feasible_rank_on_all_valid_attention_instances":True}


def forward_state(config,review):
    result=Path("out/phase21_allocation_v2_forward.json")
    source=Path("out/phase2_downstream_v2.json")
    deadline=datetime.fromisoformat(config["waiting_for_V1_deadline_UTC"])
    if result.exists():return json.loads(result.read_text(encoding="utf-8"))
    if source.exists() and source.stat().st_mtime<=deadline.timestamp():
        if review:
            return {"status":"required_V1_ready_injection_pending","required_path":source.as_posix(),
                    "observed_UTC":datetime.now(timezone.utc).isoformat(),"deadline_UTC":deadline.isoformat(),
                    "injection_executed":False,"KL_values":None}
        raise RuntimeError("Required V1 arrived in time: execute the authorized injection under flock before finalizing")
    if datetime.now(timezone.utc)<deadline:
        if review:
            return {"status":"waiting_for_required_V1","required_path":source.as_posix(),
                    "observed_UTC":datetime.now(timezone.utc).isoformat(),"deadline_UTC":deadline.isoformat(),
                    "injection_executed":False,"KL_values":None}
        raise RuntimeError("Continue waiting for V1 until the user-defined three-hour deadline; use --review only for provisional artifacts")
    return {"status":"FALTA","required_path":source.as_posix(),"deadline_UTC":deadline.isoformat(),
            "waiting_started_UTC":config["waiting_for_V1_started_UTC"],"wait_limit_hours":3,
            "reason":"Required completed V1 aggregate did not arrive within the user-defined window",
            "injection_executed":False,"KL_values":None,
            "empty_row_completion_counts_by_mode":None,
            "models_not_evaluated":list(MODELS),"prefix_lengths_not_evaluated":[128,256],
            "budget_ranks_not_evaluated":[8,16],
            "prepared_runner":"phase21_allocation_v2_forward.py","required_GPU_lock":"/tmp/radon-gpu.lock"}


def assemble(review=False,output=None):
    config=e4.freeze()
    if not review and not DECISIONS.exists():raise RuntimeError("Pending explicit line-protocol choice; complete review artifacts are available")
    missing=[str(matrix_path(m,n,review)) for m in MODELS for n in (128,256) if not matrix_path(m,n,review).exists()]
    residual_paths={(m,n):Path("out")/f"phase21_allocation_v2_residuals_{slug(m)}_n{n}.json" for m in MODELS for n in (128,256)}
    missing += [str(p) for p in residual_paths.values() if not p.exists()]
    if missing:raise RuntimeError("FALTA: "+", ".join(missing))
    ready=json.loads(Path("data/attn/READY").read_text(encoding="utf-8"))
    expected={(row["model"],row["n"]):row["n_matrices"] for row in ready["datasets"]}
    matrices={m:{} for m in MODELS};residuals={m:{} for m in MODELS}
    all_positive_budgets={m:{} for m in MODELS};common_K8_conventions={m:{} for m in MODELS}
    rank_secondary={m:{} for m in MODELS}
    audit={"n_populations":0,"n_matrices":0,"n_allocation_convention_rank_pairs":0,
           "all_comparisons_use_identical_complete_instances":True,"SVD_rank_0_compared":False,
           "algorithm_1_n128_residual_r8_criterion_met":0,"algorithm_1_n128_residual_r8_n_instances":0,
           "capacity_cutoff_audits":{}}
    for model in MODELS:
        audit["capacity_cutoff_audits"][model]={}
        for n in (128,256):
            data=json.loads(matrix_path(model,n,review).read_text(encoding="utf-8"))
            if data["n_instances"]!=expected[model,n] or data["n_documents"]!=64:raise ValueError("Population differs from READY")
            if data["source_manifest_sha256"]!=sha256_file(sample_paths(model,n)[1]):raise ValueError("Manifest changed")
            if data["dictionary"]["n_atoms"]!=17:raise ValueError("Named dictionary changed")
            for K,cap in data["capacity"].items():
                if int(K)<=0 or cap["residual_rank"]!=int(K)-1:raise ValueError("Rank convention mismatch")
                for metric in cap["metrics"].values():
                    if metric["n_instances"]!=expected[model,n] or metric["n_documents"]!=64:raise ValueError("Conditional subset summary")
                for pair in cap["comparisons"].values():
                    if pair["wilcoxon"]["n_documents"]!=64:raise ValueError("Wrong signed-rank unit")
            if n==128:
                diagnostic=data["allocation"][e4.ALT]["8"]["algorithm_1_diagnostics"]
                audit["algorithm_1_n128_residual_r8_criterion_met"]+=diagnostic["criterion_met_by_5"]
                audit["algorithm_1_n128_residual_r8_n_instances"]+=diagnostic["n_instances"]
            matrices[model][str(n)]=data
            residuals[model][str(n)]=json.loads(residual_paths[model,n].read_text(encoding="utf-8"))
            corepath,corepairs=e4.core_paths(model,n)
            core=json.loads(corepath.read_text(encoding="utf-8"))
            all_positive_budgets[model][str(n)]=core["capacity_without_lines"]
            common_path=Path("out")/f"phase21_allocation_v2_budget8_conventions_{slug(model)}_n{n}.json"
            if common_path.exists():
                panel=json.loads(common_path.read_text(encoding="utf-8"))
                if panel["n_instances"]!=expected[model,n] or panel["residual_rank"]!=7:
                    raise ValueError("Common-cap convention panel differs from the complete population")
                if panel["source_core_sha256"]!=sha256_file(corepath):raise ValueError("Common-cap panel core changed")
                common_K8_conventions[model][str(n)]=panel
            elif not review:
                raise RuntimeError(f"FALTA: common-cap convention supplement {common_path}")
            rank_path=Path("out")/f"phase21_allocation_v2_rank_comparison_{slug(model)}_n{n}.json"
            if rank_path.exists():
                secondary=json.loads(rank_path.read_text(encoding="utf-8"))
                if secondary["n_instances"]!=expected[model,n] or not secondary["secondary_only"]:
                    raise ValueError("Secondary rank comparison population/label mismatch")
                if secondary["source_core_sha256"]!=sha256_file(corepath):raise ValueError("Secondary core changed")
                rank_secondary[model][str(n)]=secondary
            elif not review:
                raise RuntimeError(f"FALTA: secondary rank comparison {rank_path}")
            audit["n_populations"]+=1;audit["n_matrices"]+=data["n_instances"]
            audit["n_allocation_convention_rank_pairs"]+=18*data["n_instances"]
            audit["capacity_cutoff_audits"][model][str(n)]=cutoff_audit(model,n)
    if audit["n_matrices"]!=19968 or (audit["algorithm_1_n128_residual_r8_criterion_met"],audit["algorithm_1_n128_residual_r8_n_instances"])!=(17,9984):
        raise ValueError("Coverage or recorded Alg1 diagnostic changed")
    forward=forward_state(config,review)
    low_budget_missing=any(str(K) not in next(iter(matrices.values()))["128"]["capacity"] for K in (1,2))
    status=("review_exact_full_dictionary_endpoint_candidates" if review else
            ("primary_matrix_panels_complete_partial_OMP_FALTA" if low_budget_missing else "matrix_complete")+
            ("_injection_FALTA_after_3h" if forward.get("status")=="FALTA" else "_forward_complete"))
    result={"schema_version":2,"status":status,
            "_meta":config,"created_UTC":datetime.now(timezone.utc).isoformat(),
            "capacity_budget_ranks_present":list(next(iter(matrices.values()))["128"]["capacity"]),
            "line_protocol_choice":json.loads(DECISIONS.read_text(encoding="utf-8")) if DECISIONS.exists() else {"status":"user clarification pending; candidate computations explicitly separated"},
            "matrices":matrices,"principal_symmetric_residuals_K8_q7":residuals,"forward":forward,"integrity_audit":audit,
            "named_first_vs_SVD_all_positive_budgets":all_positive_budgets,
            "allocation_at_common_K8_q7_supplement":common_K8_conventions,
            "secondary_rank_matched_comparisons":rank_secondary,
            "allocation_panel_index_explanation":"Main allocation sweep uses residual rank r=8 as requested and independently audited (17/9984 criterion diagnostic). Capacity K=8 uses residual rank q=7. The common-K8 supplement reports all three allocation conventions at q=7, separately.",
            "line_low_budget_status":{str(K):("present" if str(K) in next(iter(matrices.values()))["128"]["capacity"] else "FALTA: unmodified partial-dictionary OMP trajectory not computed at this budget; scope not waived") for K in (1,2)},
            "complete_original_OMP_endpoint_controls":json.loads(Path("out/phase21_allocation_v2_complete_OMP_endpoint_controls.json").read_text(encoding="utf-8")),
            "implementation_files_sha256":{p.as_posix():sha256_file(p) for p in sorted(Path('.').glob('phase21_allocation_v2*')) if p.is_file() and p.suffix in ('.py','.sh')},
            "runtime_environment":{"python":sys.version,"python_executable":sys.executable,
                                   "platform":platform.platform(),"numpy":np.__version__,"scipy":scipy.__version__,
                                   "torch":e4.torch.__version__,"torch_CPU_threads":e4.torch.get_num_threads(),
                                   "thread_environment":{key:os.environ.get(key) for key in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS")},
                                   "maximum_concurrent_computing_CPU_processes":3,
                                   "GPU_lock":"/tmp/radon-gpu.lock"},
            "checks":{name:json.loads((Path("out")/name).read_text(encoding="utf-8")) for name in (
                "phase21_allocation_v2_adapter_checks.json","phase21_allocation_v2_statistics_checks.json",
                "phase21_allocation_v2_shared_SVD_adapter_checks.json","phase21_allocation_v2_integrity_checks.json",
                "phase21_allocation_v2_line_endpoint_check_n128.json","phase21_allocation_v2_line_endpoint_check_n256.json")}}
    path=Path(output or ("out/phase21_allocation_v2_review.json" if review else "out/phase21_allocation_v2.json"))
    if path.parent.resolve()!=Path("out").resolve() or not path.name.startswith("phase21_allocation_v2") or path.suffix!=".json":
        raise ValueError("Only new phase21_allocation_v2*.json destinations under out/")
    if path.name=="phase21_allocation_v2.json" and forward.get("status") in ("waiting_for_required_V1","required_V1_ready_injection_pending"):
        raise RuntimeError("Primary v2 output requires the completed injection or the expired three-hour V1 waiting window")
    e4.write_new(path,result)
    e4.log(f"ASSEMBLED {path}; review={review}; 19968 matrices; Alg1 diagnostic17/9984; forward={forward.get('status','complete')}")
    return path


def report(path):
    d=json.loads(Path(path).read_text(encoding="utf-8"))
    print("ALLOCATION ENERGY: instance median [95% document-block CI]; secondary mean-of-document-means")
    for n in ("128","256"):
        for model in MODELS:
            cells=[]
            for method in e4.CONVENTIONS:
                s=d["matrices"][model][n]["allocation"][method]["8"]["metrics"]["named_energy_ratio"]
                lo,hi=s["median_ci_document_bootstrap"]
                cells.append(f"{s['median']:.4f} [{lo:.4f},{hi:.4f}]; meanDoc={s['secondary_document_means']['mean']:.4f}")
            print(n,model," | ".join(cells))
    print("CAPACITY K8/q7: errSL errSVD errLines; paired delta/CI, Wilcoxon, rb, SVD-win fractions instances/distinct-heads")
    for n in ("128","256"):
        for model in MODELS:
            cap=d["matrices"][model][n]["capacity"]["8"]
            errors=" ".join(f"{cap['metrics'][k]['median']:.5f}" for k in ("named_first_error","svd_error","line_error"))
            print(n,model,errors)
            for name in ("named_minus_SVD","lines_minus_SVD"):
                p=cap["comparisons"][name];s=p["paired_instance_difference"]
                print(name,f"delta={s['median']:.6f}",s["median_ci_document_bootstrap"],
                      f"p={p['wilcoxon']['p_two_sided']:.4g}",f"rb={p['wilcoxon']['rank_biserial']:.5f}",
                      f"f_inst={p['right_arm_win_fraction_instances']:.5f}",
                      f"f_head={p['distinct_head_secondary']['right_arm_win_fraction']:.5f}")
    print("FORWARD",d["forward"].get("status","complete"))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("assemble","report"))
    parser.add_argument("--review",action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--input",default="out/phase21_allocation_v2_review.json")
    args=parser.parse_args()
    if args.command=="assemble":assemble(args.review,args.output)
    else:report(args.input)
