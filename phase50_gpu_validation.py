"""E9 GPU-double ALS validation against the independent CPU-double estimator.

Run only under flock /tmp/radon-gpu.lock. The benchmark option performs no
model forward. Full validation uses the 32 frozen archive instances per model.
"""
import phase50_als as als
import argparse
from pathlib import Path
import time
import numpy as np
import torch
from phase50_experiment import read, jsonl, PROTOCOL, normalize_cpu, metrics, Dictionary
import phase2_downstream as harness
from sampling import MODELS, load_sample, slug, sha256_file, write_json_new


def prefix_block_control():
    certified=als.GPU_SOLVER=="certified_qr"
    implementation="phase50_certified_qr_cuda.py" if certified else "phase50_prefix_qr_cuda.py"
    implementation_hash=sha256_file(implementation)
    path=Path(f"out/phase50_GPU_{'certified' if certified else 'prefix'}_block_control_{implementation_hash[:12]}.json")
    if path.exists():
        if not read(path)["passed"]: raise AssertionError("Preserved failed prefix QR control")
        return
    if certified:
        from phase50_certified_qr_cuda import update
    else:
        from phase50_prefix_qr_cuda import update
    rng=np.random.default_rng(5002); checks=[]
    for rank in (7,8,15,16):
        a=np.tril(rng.normal(size=(128,128)))
        for condition in (1.,1e9):
            factor=rng.normal(size=(128,rank))*np.geomspace(1,1/condition,rank)
            for reverse in (False,True):
                target=a.T.copy() if reverse else a.copy()
                reference=np.stack([np.linalg.lstsq(factor[i:] if reverse else factor[:i+1],
                                                    target[i,i:] if reverse else target[i,:i+1],rcond=als.LS_RCOND)[0] for i in range(128)])
                for layout in ("contiguous","transposed_storage"):
                    ff=factor[None] if layout=="contiguous" else np.asfortranarray(factor[None])
                    aa=target[None] if layout=="contiguous" else np.asfortranarray(target[None])
                    actual,_=update(torch.from_numpy(aa).to("cuda"),torch.from_numpy(ff).to("cuda"),
                                    harness.causal_support(128,128,"cuda"),reverse)
                    actual=actual[0].cpu().numpy()
                    factor_diff=float(np.linalg.norm(actual-reference)/max(1.,np.linalg.norm(reference)))
                    prediction=actual@factor.T; expected=reference@factor.T
                    obs_diff=float(np.linalg.norm(np.triu(prediction-expected) if reverse else np.tril(prediction-expected))/np.linalg.norm(target))
                    passed=factor_diff<=1e-5 and obs_diff<=1e-7
                    checks.append({"rank":rank,"condition":condition,"reverse":reverse,"layout":layout,"relative_factor_difference":factor_diff,
                                   "relative_observed_prediction_difference":obs_diff,"passed":passed})
    result={"passed":all(x["passed"] for x in checks),"checks":checks,
            "implementation_source":implementation,"implementation_sha256":implementation_hash,
            "relative_factor_tolerance":1e-5,"observed_prediction_tolerance":1e-7,"declared_before_control":True}
    write_json_new(path,result)
    if not result["passed"]: raise AssertionError("Prefix QR CUDA block differs from direct CPU double LS")


def graph_component_control(diagnostic_only=False):
    path=Path("out/phase50_GPU_graph_component_control.json")
    if path.exists():
        result=read(path)
        if not result["passed"] and not diagnostic_only: raise AssertionError("Preserved failed CUDA graph control")
        return result
    from phase50_graph_als_cuda import qr,SmallSVD,SweepGraph
    rng=np.random.default_rng(5003); checks=[]
    for rank in (7,8,15,16):
        source=rng.normal(size=(2,128,rank))*np.geomspace(1,1e-8,rank)[None,None,:]
        tensor=torch.from_numpy(source).to("cuda"); q,r=qr(tensor)
        product_error=float((q@r-tensor).norm()/tensor.norm())
        orth_error=float((q.transpose(-1,-2)@q-torch.eye(rank,device="cuda")).norm())
        solver=SmallSVD(2,rank); u,s,vh=solver(r)
        rec_error=float(((u*s[:,None,:])@vh-r).norm()/r.norm())
        if int(solver.failures): raise AssertionError("cuSOLVER small SVD failed in component control")
        passed=product_error<=1e-10 and orth_error<=1e-8 and rec_error<=1e-10
        checks.append({"rank":rank,"QR_relative_product_error":product_error,"Q_orthogonality_error":orth_error,
                       "SVD_relative_product_error":rec_error,"passed":passed})
    # A repeated direct solve with the same inputs must have the same outcome;
    # this is the only circumstance in which retry work can be deduplicated.
    rank=8; u=rng.lognormal(0,.7,(2,128,rank)); v=rng.lognormal(0,.7,(2,128,rank))
    planted=np.tril(u@v.transpose(0,2,1)); planted/=planted.sum(-1,keepdims=True)
    a=torch.from_numpy(planted).to("cuda"); norms=a.norm(dim=(-2,-1)); target=a/norms[:,None,None]
    left,s,vh=torch.linalg.svd(a,full_matrices=False); root=(s[:,:rank]/norms[:,None]).sqrt()[:,None,:]
    initial_u,initial_v=left[:,:,:rank]*root,vh[:,:rank,:].transpose(-1,-2)*root
    graph=SweepGraph(target,initial_u,initial_v,harness.causal_support(128,128,"cuda"))
    ua,va,*_=graph.execute(target,initial_u,initial_v); first=(ua@va.transpose(-1,-2)).clone(); first_log=graph.log_loss.clone()
    ub,vb,*_=graph.execute(target,initial_u,initial_v); second=ub@vb.transpose(-1,-2)
    repeated_equal=bool(torch.equal(first,second) and torch.equal(first_log,graph.log_loss))
    recovery=((second-target)*harness.causal_support(128,128,"cuda")).norm(dim=(-2,-1)).cpu().tolist()
    result={"passed":all(c["passed"] for c in checks) and repeated_equal and max(recovery)<=.01,
            "component_checks":checks,"two_repeated_200_sweep_fits_bit_equal":repeated_equal,
            "planted_relative_errors":recovery,"planted_tolerance":.01,
            "direct_retry_deduplication":"same deterministic all-direct per-head LS/QR/SVD input reproduces the same candidate; no alternative solver or convergence criterion selected"}
    write_json_new(path,result)
    if not result["passed"]: raise AssertionError("CUDA graph component/recovery/determinism control failed")
    return result


def run(model, benchmark=False,diagnostic_only=False,steady=False,repeats=1):
    protocol = read(PROTOCOL); cfg = protocol["datasets"][model]
    if not benchmark:
        decision=read("out/phase50_gpu_solver.json")
        if (als.GPU_SOLVER!=decision["backend"] or als.SWEEPS!=protocol["ALS"]["sweeps"]
                or sha256_file("phase50_certified_qr_cuda.py")!=decision["implementation_sha256"]):
            raise ValueError("GPU implementation/fixed-sweep decision changed before validation")
    timing_tag=als.GPU_SOLVER+(f"_steady_x{repeats}" if steady else "")
    if als.GPU_SOLVER=="certified_qr":timing_tag+="_"+sha256_file("phase50_certified_qr_cuda.py")[:8]
    correction_policy=Path("out/phase50_numerical_fallback.json")
    path = (Path(f"out/phase50_estimator_validation_{slug(model)}.json") if not benchmark and correction_policy.exists()
            else Path(f"out/phase50_GPU_{'benchmark_'+timing_tag if benchmark else 'validation'}_{slug(model)}.json"))
    if path.exists():
        return read(path)
    if als.GPU_SOLVER in ("prefix_qr","prefix_qr_graph","certified_qr"):
        prefix_block_control()
    if als.GPU_SOLVER=="prefix_qr_graph":
        graph_component_control(diagnostic_only)
    cache_path=Path(f"out/phase50_GPU_CPU_reference_{slug(model)}.json")
    cached={}
    if not benchmark and cache_path.exists():
        cache=read(cache_path)
        if cache["protocol_sha256"]!=sha256_file(PROTOCOL) or cache["pairs_sha256"]!=sha256_file(cache["pairs_path"]):
            raise ValueError("CPU reference cache provenance mismatch")
        cached={(r["archive_index"],r["K"],r["arm"]):r for r in jsonl(cache["pairs_path"])}
        if len(cached)!=128: raise ValueError("Incomplete independent CPU references")
    a, manifest = load_sample(model,128); dictionary = Dictionary(128)
    selected = cfg["GPU_validation_indices"][:2]*repeats if benchmark else cfg["GPU_validation_indices"]
    support = harness.causal_support(128,128,"cuda")
    checks = []; started = time.perf_counter()
    for k in (8,16):
        for arm in ("masked_K","named_plus_masked"):
            rank = k if arm=="masked_K" else k-1
            targets = []; nameds = []; originals = []
            cpu_products = []; cpu_infos = []; initials = []
            for idx in selected:
                original = a[idx].astype(np.float64); named = dictionary.project(original)[0]
                target = original if arm=="masked_K" else original-named
                if cached:
                    cache_row=cached[idx,k,arm]
                    initial=(np.array(cache_row["initial_U"],dtype=np.float64),np.array(cache_row["initial_V"],dtype=np.float64))
                    cpu_products.append(None);cpu_infos.append(cache_row["CPU_ALS"])
                else:
                    left,s,vh = np.linalg.svd(target,full_matrices=False)
                    initial = (left[:,:rank]*np.sqrt(s[:rank]),vh[:rank].T*np.sqrt(s[:rank]))
                if not benchmark and not cached:
                    product,info = als.fit_cpu(target,rank,initial)
                    cpu_products.append(product); cpu_infos.append(info)
                initials.append(initial); targets.append(target); nameds.append(named); originals.append(original)
            tensor = torch.from_numpy(np.stack(targets)).to("cuda")
            init = tuple(torch.from_numpy(np.stack([x[j] for x in initials])).to("cuda") for j in (0,1))
            if benchmark:
                als.os.environ["PHASE50_ALS_PROGRESS"] = "1"
            torch.cuda.synchronize(); tick = time.perf_counter()
            if benchmark:
                gpu,infos=als.fit_gpu(tensor,rank,support,init)
            else:
                gpu,infos,uncorrected,uncorrected_infos=als.fit_gpu(tensor,rank,support,init,return_uncorrected=True)
            torch.cuda.synchronize(); elapsed = time.perf_counter()-tick
            cold=elapsed
            if steady:
                tick=time.perf_counter(); again,infos=als.fit_gpu(tensor,rank,support,init)
                torch.cuda.synchronize(); elapsed=time.perf_counter()-tick
                if not torch.equal(gpu,again): raise AssertionError("Steady graph replay changed the repeated fit")
                gpu=again
            products = gpu.cpu().numpy()
            uncorrected_products=None if benchmark else uncorrected.cpu().numpy()
            for ordinal,idx in enumerate(selected):
                original = originals[ordinal]; target = targets[ordinal]
                ref = normalize_cpu(original,original)[0]
                add = nameds[ordinal] if arm=="named_plus_masked" else 0
                gm = metrics(products[ordinal]+add,original,ref)
                if benchmark:
                    checks.append({"archive_index":idx,"K":k,"arm":arm,"GPU":gm,"GPU_ALS":infos[ordinal],
                                   "GPU_batch_seconds":elapsed,"GPU_cold_batch_seconds":cold,"performance_only_no_CPU_comparison":True})
                    continue
                cm = cached[idx,k,arm]["CPU"] if cached else metrics(cpu_products[ordinal]+add,original,ref)
                error_diff = abs(cm["raw_causal_frobenius"]-gm["raw_causal_frobenius"])
                uncorrected_metrics=metrics(uncorrected_products[ordinal]+add,original,ref)
                checks.append({"archive_index":idx,"instance_id":manifest["instances"][idx]["instance_id"],
                               "K":k,"arm":arm,"CPU":cm,"GPU":gm,
                               "absolute_error_difference":error_diff,
                               "normalized_frobenius_difference":abs(cm["frobenius"]-gm["frobenius"]),
                               "TV_difference":abs(cm["TV"]-gm["TV"]),
                               "causal_prediction_difference_relative_to_A":None if cached else float(np.linalg.norm(np.tril(cpu_products[ordinal]-products[ordinal]))/np.linalg.norm(original)),
                               "CPU_ALS":cpu_infos[ordinal],"GPU_ALS":infos[ordinal],
                               "final_estimator_uses_CPU_reference":bool(infos[ordinal].get("numerical_fallback",False)),
                               "uncorrected_GPU_metrics":uncorrected_metrics,"uncorrected_GPU_ALS":uncorrected_infos[ordinal],
                               "uncorrected_GPU_CPU_error_difference":abs(cm["raw_causal_frobenius"]-uncorrected_metrics["raw_causal_frobenius"])})
            suffix = "performance only" if benchmark else f"max error diff={max(c['absolute_error_difference'] for c in checks):.6g}"
            print(f"GPU {'BENCH' if benchmark else 'VALIDATE'} {model} K{k} {arm} {len(selected)} matrices: GPU={elapsed:.3f}s; {suffix}",flush=True)
    maximum = None if benchmark else max(c["absolute_error_difference"] for c in checks)
    raw_maximum=None if benchmark else max(c["uncorrected_GPU_CPU_error_difference"] for c in checks)
    result = {"model":model,"protocol_sha256":sha256_file(PROTOCOL),"n_matrices":len(selected),"n_unique_matrices":len(set(selected)),"n_fits":len(checks),
              "GPU_dtype":"float64","CPU_dtype":"float64","GPU_solver":als.GPU_SOLVER,"same_initial_factors":True,"checks":checks,
              "CPU_reference_cache_path":cache_path.as_posix() if cached else None,
              "estimator_implementation_sha256":sha256_file("phase50_als.py"),
              "max_raw_error_difference":maximum,
              "max_uncorrected_GPU_CPU_error_difference":raw_maximum,
              "uncorrected_GPU_passed":None if benchmark else raw_maximum<=protocol["sanities"]["CPU_GPU_error_tolerance"],
              "CPU_reference_recomputed_fits":0 if benchmark else sum(c["final_estimator_uses_CPU_reference"] for c in checks),
              "correction_policy_sha256":sha256_file(correction_policy) if correction_policy.exists() else None,
              "max_normalized_frobenius_difference":None if benchmark else max(c["normalized_frobenius_difference"] for c in checks),
              "max_TV_difference":None if benchmark else max(c["TV_difference"] for c in checks),
              "validation_performed":not benchmark,
              "diagnostic_only_not_qualified_for_forward":diagnostic_only,
              "passed":None if benchmark else maximum<=protocol["sanities"]["CPU_GPU_error_tolerance"],"elapsed_seconds":time.perf_counter()-started}
    write_json_new(path,result)
    if not benchmark and not result["passed"]:
        raise AssertionError(f"GPU/CPU error disagreement {maximum}; preserve results and audit estimator")
    return result


if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--model",choices=MODELS,required=True)
    ap.add_argument("--benchmark",action="store_true"); ap.add_argument("--under-gpu-lock",action="store_true")
    ap.add_argument("--backend",choices=("hybrid","prefix_qr","prefix_qr_graph","certified_qr"),default=als.GPU_SOLVER)
    ap.add_argument("--timing-only-after-control-failure",action="store_true")
    ap.add_argument("--steady-benchmark",action="store_true");ap.add_argument("--benchmark-repeats",type=int,default=1)
    args=ap.parse_args()
    if not args.under_gpu_lock:
        raise RuntimeError("Must be launched by flock /tmp/radon-gpu.lock --under-gpu-lock")
    als.GPU_SOLVER=args.backend
    if args.timing_only_after_control_failure and not args.benchmark: raise ValueError("Diagnostic control bypass is only available to performance benchmarks, never validation or forward")
    if (args.steady_benchmark or args.benchmark_repeats!=1) and not args.benchmark: raise ValueError("Timing repetitions cannot change the validation sample")
    run(args.model,args.benchmark,args.timing_only_after_control_failure,args.steady_benchmark,args.benchmark_repeats)
