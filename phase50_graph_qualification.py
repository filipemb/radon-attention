"""Diagnose the extra planted convergence control without changing its result.

CPU diagnosis is run only after the matrix pool exits. A CUDA backend can be
qualified as an implementation only if the extra error matches independent
CPU at1e-5 and the original, frozen seed5001 controls meet the original1% bound.
The failed additional convergence control remains failed in all reports.
"""
import phase50_als as als
import argparse
from pathlib import Path
import numpy as np
import torch
from phase50_experiment import read,PROTOCOL
from sampling import write_json_new,sha256_file


def cpu():
    if not Path("out/phase50_matrix_summary.json").exists(): raise RuntimeError("Wait for CPU matrix pool to finish")
    path=Path("out/phase50_graph_extra_CPU_control.json")
    if path.exists(): return read(path)
    rng=np.random.default_rng(5003)
    for rank in (7,8,15,16): rng.normal(size=(2,128,rank))
    u,v=rng.lognormal(0,.7,(2,128,8)),rng.lognormal(0,.7,(2,128,8))
    a=np.tril(u@v.transpose(0,2,1)); a/=a.sum(-1,keepdims=True)
    graph=read("out/phase50_GPU_graph_component_control.json")
    checks=[]
    for i in range(2):
        product,info=als.fit_cpu(a[i],8)
        error=float(np.linalg.norm(np.tril(product)-a[i])/np.linalg.norm(a[i]))
        delta=abs(error-graph["planted_relative_errors"][i])
        checks.append({"matrix":i,"CPU_relative_error":error,"GPU_graph_relative_error":graph["planted_relative_errors"][i],
                       "absolute_error_difference":delta,"CPU_ALS":info,"agrees_at_1e_5":delta<=1e-5,
                       "CPU_meets_original_1pct_recovery_bound":error<=.01})
    result={"protocol_sha256":sha256_file(PROTOCOL),"seed":5003,"K":8,"sweeps":200,"checks":checks,
            "max_absolute_error_difference":max(x["absolute_error_difference"] for x in checks),
            "implementation_agrees_at_1e_5":all(x["agrees_at_1e_5"] for x in checks),
            "extra_GPU_convergence_control_passed":graph["passed"],
            "diagnostic_tolerance_fixed_before_CPU_run":1e-5}
    write_json_new(path,result); print(result["checks"],flush=True); return result


def gpu(backend="prefix_qr_graph"):
    als.GPU_SOLVER=backend
    fit=als.fit_gpu
    import phase2_downstream as harness
    label="graph" if backend=="prefix_qr_graph" else "certified"
    implementation="phase50_graph_als_cuda.py" if label=="graph" else "phase50_certified_qr_cuda.py"
    source_hash=sha256_file(implementation)
    suffix="" if label=="graph" else "_"+source_hash[:12]
    path=Path(f"out/phase50_{label}_primary_GPU_control{suffix}.json")
    if path.exists(): return read(path)
    rng=np.random.default_rng(5001); controls=read("out/phase50_CPU_controls.json"); checks=[]
    for k in (8,16):
        u,v=rng.lognormal(0,.7,(128,k)),rng.lognormal(0,.7,(128,k))
        a=np.tril(u@v.T);a/=a.sum(-1,keepdims=True)
        product,infos=fit(torch.from_numpy(a[None]).to("cuda"),k,harness.causal_support(128,128,"cuda"))
        error=float(np.linalg.norm(np.tril(product[0].cpu().numpy())-a)/np.linalg.norm(a))
        cpu_error=next(c["relative_error"] for c in controls["planted"] if c["K"]==k)
        checks.append({"K":k,"GPU_relative_error":error,"CPU_relative_error":cpu_error,"meets_frozen_1pct_bound":error<=.01,
                       "absolute_error_difference":abs(error-cpu_error),"GPU_ALS":infos[0]})
    result={"protocol_sha256":sha256_file(PROTOCOL),"seed":5001,"sweeps":200,"checks":checks,
            "GPU_solver":backend,
            "implementation_source":implementation,"implementation_sha256":source_hash,
            "all_frozen_primary_controls_passed":all(c["meets_frozen_1pct_bound"] for c in checks)}
    write_json_new(path,result); print([{key:c[key] for key in ("K","GPU_relative_error","CPU_relative_error","meets_frozen_1pct_bound","absolute_error_difference")} for c in checks],flush=True); return result


def decide():
    original=read("out/phase50_GPU_graph_component_control.json")
    cp=read("out/phase50_graph_extra_CPU_control.json"); gp=read("out/phase50_graph_primary_GPU_control.json")
    result={"protocol_sha256":sha256_file(PROTOCOL),
            "implementation_valid":all(x["passed"] for x in original["component_checks"])
                                   and original["two_repeated_200_sweep_fits_bit_equal"]
                                   and cp["implementation_agrees_at_1e_5"] and gp["all_frozen_primary_controls_passed"],
            "original_frozen_positive_control_passed":gp["all_frozen_primary_controls_passed"],
            "additional_planted_convergence_control_passed":original["passed"],
            "extra_CPU_GPU_max_difference":cp["max_absolute_error_difference"],
            "failed_control_preserved":"out/phase50_GPU_graph_component_control.json",
            "interpretation":"The extra planted result is a200-sweep convergence limitation only if independent CPU matches at the prespecified1e-5 tolerance; it is never relabeled as passed. Full32-matrix/model CPU-double validation remains mandatory before forward."}
    write_json_new("out/phase50_graph_qualification.json",result)
    if not result["implementation_valid"]: raise AssertionError("Graph implementation qualification failed; keep original backend")


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("action",choices=("cpu","gpu","decide"));ap.add_argument("--under-gpu-lock",action="store_true")
    ap.add_argument("--backend",choices=("prefix_qr_graph","certified_qr"),default="prefix_qr_graph")
    args=ap.parse_args()
    if args.action=="cpu":cpu()
    elif args.action=="decide":decide()
    else:
        if not args.under_gpu_lock:raise RuntimeError("GPU primary control requires outer flock")
        gpu(args.backend)
