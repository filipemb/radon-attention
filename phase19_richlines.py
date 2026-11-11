"""E2: richer causal line representations, paired with truncated SVD.

Commands (Windows venv, from the repository):
  python phase19_richlines.py prepare
  python phase19_richlines.py geometry --n 128
  python phase19_richlines.py cpu --n 128 --models gpt2 gpt2-medium
  python phase19_richlines.py controls --n 128
  python phase19_richlines.py aggregate

E2(c) is run by richlines_gpu_runner.py under the documented Linux flock.
Nothing imports an attention extraction or model-forward function.
"""
from __future__ import annotations
import os
for _key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "4"

import argparse
import collections
import json
import time
from pathlib import Path
import numpy as np
from richlines_core import (SEED, COMPONENTS, PROFILES, LineDictionary, block_summary,
    counts, digest, fbp_reference, grids, make_radon, omp, progress, radon_decode,
    radon_spectrum, svd_errors, write_json)


OUT = Path("out")
SELECTION = OUT / "phase19_selection.json"
MODELS = ["gpt2", "gpt2-medium", "EleutherAI__pythia-410m", "EleutherAI__pythia-1.4b",
          "Qwen__Qwen2.5-0.5B", "Qwen__Qwen2.5-3B"]
METHOD_COSTS = {"uniform": 2, "profiled": 3, "radon": 2, "parametric": 5, "fbp": 2}


def prepare():
    if SELECTION.exists():
        saved=json.loads(SELECTION.read_text())
        if saved["seed"]!=SEED or not saved["common_to_all_methods"]:
            raise ValueError("Existing selection does not match this protocol")
        progress("Using the existing fixed selection; no resampling")
        return
    records = []
    for model in MODELS:
        for n in (128,256):
            path = Path("data/attn")/f"{model}_n{n}.manifest.json"
            m = json.loads(path.read_text(encoding="utf-8"))
            seed = SEED+int.from_bytes(model.encode(),"little") % (2**32-SEED)
            rng = np.random.default_rng(seed)
            documents = list(range(len(m["documents"])))
            rng.shuffle(documents)
            layers = rng.permutation(m["n_layers"]).tolist()
            quotas = collections.Counter((layers*((len(documents)+len(layers)-1)//len(layers)))[:len(documents)])
            head_counts = collections.Counter()
            selected = []
            for doc in documents:
                candidates = [(idx, inst) for idx,inst in enumerate(m["instances"])
                              if inst["document_index"]==doc and quotas[inst["layer"]]>0]
                # Layer quotas are exact; head balance is a secondary criterion.
                # Random tie-breaks depend only on manifest identities and seed.
                tie = rng.random(len(candidates))
                order = sorted(range(len(candidates)),key=lambda j:(head_counts[candidates[j][1]["head"]],tie[j]))
                idx,inst = candidates[order[0]]
                quotas[inst["layer"]]-=1
                head_counts[inst["head"]]+=1
                selected.append({"archive_index":idx,**inst})
            selected.sort(key=lambda inst:inst["archive_index"])
            records.append({"model_slug":model,"model":m["model"],"n":n,
                "source_matrices":m["n_matrices"],"selected_matrices":len(selected),
                "source_documents":len(m["documents"]),"selected_documents":len(documents),
                "manifest_sha256":digest(path),"npz_sha256_expected":m["npz_sha256"],
                "layer_counts":dict(collections.Counter(str(s["layer"]) for s in selected)),
                "head_counts":dict(collections.Counter(str(s["head"]) for s in selected)),
                "instances":selected})
    write_json(SELECTION,{"seed":SEED,"fixed_before_attention_evaluation":True,
        "design":"one archived head per document; exact balanced layer quotas; secondary head balancing; seeded tie-breaks",
        "reason":"Synthetic full-grid n=256 CUDA pilot: 17.8 seconds per 100 updates; at 450 updates full n=256 archive alone exceeds 220 GPU hours. Sparse CPU and renderer engineering measured before selection.",
        "common_to_all_methods":True,"n_selected":sum(x["selected_matrices"] for x in records),
        "datasets":records})
    progress("SELECTION FIXED before archived-attention evaluation: 64/documents x 12 datasets = 768 matrices; every method uses exactly these identities")


def prepare_runtime():
    import sys,importlib.metadata
    import scipy,skimage,torch
    env_path=OUT/"phase19_environment.json"
    if not env_path.exists():
        write_json(env_path,{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,
            "skimage":skimage.__version__,"torch":torch.__version__,
            "cupy":importlib.metadata.version("cupy-cuda12x"),"threads_per_process":4,
            "cpu_worker_limit":3,"gpu_worker_limit":1,"gpu_lock":"/tmp/radon-gpu.lock",
            "subset_fixed_before_attention":str(SELECTION),
            "note":"Exact C2 compact transverse rendering; log-domain normalization; small CUDA atomic-sum nondeterminism is possible."})
    decisions_path=OUT/"phase19_decisions.json"
    if not decisions_path.exists():
        write_json(decisions_path,{"decisions":[
            {"question":"Full archive versus subset?","suggestion":"64 instances/dataset, all 64 documents, balanced layers and heads; same subset for all methods","certainty":"high","executed":True},
            {"question":"Common storage budgets?","suggestion":"(2*n+1)*[1,2,4], independently of results; same-k curve separately","certainty":"medium","executed":True},
            {"question":"Failed positive controls?","suggestion":"Keep fixed thresholds and all cases; limit negative conclusions","certainty":"high","executed":True}]})
    path=OUT/"phase19_optimizer_stable_frozen.json"
    sources=["richlines_core.py","richlines_parametric.py","richlines_initialization.py","richlines_cuda.py"]
    hashes={p:digest(p) for p in sources}
    if path.exists():
        old=json.loads(path.read_text())
        if old["source_sha256"]!=hashes or old["selection_sha256"]!=digest(SELECTION):
            raise ValueError("Stable optimizer or selection changed after freeze")
        return
    write_json(path,{"freeze_before_any_reported_parametric_fit":True,"seed":SEED,
        "adam_steps":450,"lbfgsb_max_iterations":150,"lbfgsb_gtol":1e-7,"lbfgsb_ftol":1e-12,
        "initializations":["uniform_omp","profiled_omp","random_importance","multiscale_sinogram_proposal_nnls"],
        "multiscale_width_grid":[0.5,1,2,4,8,16,32],"multiscale_max_proposals":32,
        "selection_sha256":digest(SELECTION),"source_sha256":hashes,
        "normalization":"log-domain including transverse taper, avoiding norm-square underflow",
        "normalized_amplitude_bounds":[0,1],
        "amplitude_bound_reason":"For nonnegative unit-norm atoms and a unit-norm target, every coordinatewise nonnegative optimum has amplitude <=1",
        "control_policy":"Same fixed targets, seeds and acceptance thresholds; preserve and report all failed controls",
        "max_cpu_workers":3,"cpu_threads_each":4,"max_gpu_workers":1,"gpu_lock":"/tmp/radon-gpu.lock"})
    progress("STABLE OPTIMIZER FROZEN: log-domain normalization; fixed seeds, four starts, 450 Adam + 150 L-BFGS-B; every reported fit uses this implementation")


def selection_record(model,n):
    s = json.loads(SELECTION.read_text(encoding="utf-8"))
    return next(r for r in s["datasets"] if r["model_slug"]==model and r["n"]==n)


def geometry(n):
    destination=OUT/f"phase19_geometry_n{n}.json"
    if destination.exists():
        saved=json.loads(destination.read_text())
        if saved["n"]!=n or saved["radon"]["lambda_min_RtR_estimate"]<=0:
            raise ValueError("Existing geometry diagnostics are inconsistent")
        progress(f"GEOMETRY n={n}: using existing verified diagnostics {destination}")
        return
    start=time.perf_counter()
    d,R=make_radon(n)
    spectrum=radon_spectrum(R)
    u=LineDictionary(n)
    p=LineDictionary(n,profiles=PROFILES)
    bound=float(np.max(R.T@np.asarray(R.sum(axis=1)).ravel()))
    result={"n":n,"uniform":u.meta,"profiled":p.meta,"radon":{**d.meta,**spectrum},
            "lipschitz_safe_row_sum_bound":bound,"seconds":time.perf_counter()-start}
    if R.shape[0]<R.shape[1] or ("lambda_min_RtR_estimate" in spectrum and spectrum["lambda_min_RtR_estimate"]<=0):
        raise RuntimeError("Discrete Radon geometry lacks numerical full-column-rank evidence")
    write_json(destination,result)
    progress(f"GEOMETRY n={n}: R shape {R.shape}, estimated condition {spectrum['condition_2_estimate']:.2f}")


def load_archive(record):
    model,n=record["model_slug"],record["n"]
    path=Path("data/attn")/f"{model}_n{n}.npz"
    manifest_path=path.with_suffix(".manifest.json")
    if digest(manifest_path)!=record["manifest_sha256"]:
        raise ValueError(f"Manifest changed after selection: {manifest_path}")
    if digest(path)!=record["npz_sha256_expected"]:
        raise ValueError(f"Archive SHA mismatch: {path}")
    with np.load(path,allow_pickle=False) as z:
        # Inspect the whole source for integrity; select only after validation.
        all_attention=z["attention"]
        if not np.isfinite(all_attention).all() or (all_attention<0).any():
            raise ValueError(f"Invalid source values: {path}")
        if np.count_nonzero(np.triu(all_attention,k=1)):
            raise ValueError(f"Noncausal source: {path}")
        for inst in record["instances"]:
            q=inst["archive_index"]
            for name in ("document_index","layer","head"):
                if int(z[name][q])!=inst[name]:
                    raise ValueError(f"Manifest/archive identity mismatch: {path} {q} {name}")
        A=all_attention[[i["archive_index"] for i in record["instances"]]].astype(float)
    return A


def read_jsonl(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def cpu(n,models):
    geo=json.loads((OUT/f"phase19_geometry_n{n}.json").read_text())
    u=LineDictionary(n)
    p=LineDictionary(n,profiles=PROFILES)
    _,R=make_radon(n)
    ks=counts(n)
    uk=sorted(set(ks["uniform"])|set(ks["parametric"]))
    pk=sorted(set(ks["profiled"])|set(ks["parametric"]))
    for model in models:
        record=selection_record(model,n)
        A=load_archive(record)
        path=OUT/f"phase19_cpu_{model}_n{n}.jsonl"
        existing=read_jsonl(path)
        if [r["instance_id"] for r in existing] != [r["instance_id"] for r in record["instances"][:len(existing)]]:
            raise ValueError("CPU resume prefix does not match the fixed selection")
        progress(f"CPU {model} n={n}: {len(existing)}/{len(A)} already complete")
        with path.open("a" if path.exists() else "x",encoding="utf-8") as f:
            for idx in range(len(existing),len(A)):
                start=time.perf_counter()
                matrix=A[idx]
                b=matrix[u.i,u.j]
                ur,ud=omp(b,u,uk,save_support=True)
                pr,pd=omp(b,p,pk,save_support=True)
                rr,rd=radon_decode(b,R,ks["radon"],geo["lipschitz_safe_row_sum_bound"])
                sv=svd_errors(matrix,ks["svd"])
                fb=fbp_reference(matrix,ks["radon"])
                row={**record["instances"][idx],"model":record["model"],"model_slug":model,
                     "norm_frobenius":float(np.linalg.norm(matrix)),
                     "methods":{"uniform":ur,"profiled":pr,"radon":rr,"svd":sv,"fbp":fb},
                     "diagnostics":{"uniform":ud,"profiled":pd,"radon":rd},
                     "cpu_seconds":time.perf_counter()-start}
                f.write(json.dumps(row,allow_nan=False)+"\n")
                f.flush()
                if idx%4==0 or idx==len(A)-1:
                    progress(f"CPU {model} n={n}: {idx+1}/{len(A)}; last {row['cpu_seconds']:.1f}s")


def controls(n):
    from richlines_parametric import render_numpy,gradient_check
    trials=8
    k_grid=[1,2,4,8]
    noisy=[0.0,0.01]
    rng=np.random.default_rng(SEED+n)
    dictionaries={"uniform":LineDictionary(n),"profiled":LineDictionary(n,profiles=PROFILES)}
    out={"n":n,"trials_per_k_noise_method":trials,"k":k_grid,"noise_relative_norm":noisy,
         "gate_fixed_before_controls":{"noiseless_error_max":1e-3,"noisy_error_max":0.02,
                                       "minimum_success_rate_per_k":0.90},
         "gradient_check":gradient_check(),"digital":{},"parametric_cases":[]}
    for name,d in dictionaries.items():
        rows=[]
        for k in k_grid:
            for trial in range(trials):
                ids=rng.choice(d.D.shape[0],size=k,replace=False)
                amp=rng.uniform(0.5,1.5,k)
                clean=np.asarray(d.D[ids].T@amp).ravel()
                z=rng.normal(size=len(clean));z/=np.linalg.norm(z)
                for noise in noisy:
                    b=clean+noise*np.linalg.norm(clean)*z
                    result,diag=omp(b,d,[k],save_support=True)
                    r=result[k]
                    chosen=r["support"]["indices"]
                    recovered=len(set(ids)&set(chosen))/k
                    recovered_equivalent=sum(any(np.linalg.norm(d.atom(t)-d.atom(s))<1e-8 for s in chosen) for t in ids)/k
                    rows.append({"k":k,"trial":trial,"noise":noise,"relative":r["relative"],
                        "absolute":r["absolute"],"exact_support_recall":recovered,
                        "equivalent_atom_recall":recovered_equivalent,"true_indices":ids.tolist(),
                        "true_amplitudes":amp.tolist(),"support":r["support"],"diagnostics":diag})
        out["digital"][name]=rows
        progress(f"CONTROLS digital {name} n={n} complete")
    for k in k_grid:
        for trial in range(trials):
            theta=rng.uniform(0,np.pi,k)
            anchor=rng.integers(0,len(dictionaries["uniform"].i),k)
            ii=dictionaries["uniform"].i[anchor]-(n-1)/2
            jj=dictionaries["uniform"].j[anchor]-(n-1)/2
            rho=np.cos(theta)*jj+np.sin(theta)*ii
            width=np.exp(rng.uniform(np.log(0.6),np.log(4),k))
            decay=rng.uniform(-4,4,k)
            amp=rng.uniform(0.5,1.5,k)
            truth=np.stack([theta,rho,width,decay,amp],axis=1)
            clean=render_numpy(truth,n)
            noise_seed=int(rng.integers(0,2**31))
            z=np.random.default_rng(noise_seed).normal(size=len(clean));z/=np.linalg.norm(z)
            for noise in noisy:
                b=clean+noise*np.linalg.norm(clean)*z
                ur,ud=omp(b,dictionaries["uniform"],[k],save_support=True)
                pr,pd=omp(b,dictionaries["profiled"],[k],save_support=True)
                out["parametric_cases"].append({"k":k,"trial":trial,"noise":noise,
                     "noise_seed":noise_seed,"truth":truth.tolist(),"uniform":ur[k],"profiled":pr[k],
                     "fit_seed":SEED+n+k*100+trial})
    write_json(OUT/f"phase19_controls_cpu_n{n}.json",out)
    progress(f"CONTROLS CPU n={n} saved, including all parametric targets and fixed starts")


def _lookup(row,method,k):
    return row["methods"][method][str(k)]


def aggregate():
    selection=json.loads(SELECTION.read_text())
    if (OUT/"phase19_richlines.json").exists():
        raise FileExistsError(OUT/"phase19_richlines.json")
    for record in selection["datasets"]:
        expected=[r["instance_id"] for r in record["instances"]]
        for stage in ("cpu","gpu_stable"):
            path=OUT/f"phase19_{stage}_{record['model_slug']}_n{record['n']}.jsonl"
            rows=read_jsonl(path)
            if [r["instance_id"] for r in rows]!=expected:
                raise ValueError(f"Incomplete stage before any pair files are written: {path}")
    protocol={"experiment":"E2 richer causal line representations","seed":SEED,
        "metric":"Frobenius absolute and relative error over all n*n entries; no row renormalization",
        "storage_unit":"one stored number, not bits; shared geometry is not charged per matrix",
        "costs":{"svd":"r*(2*n+1)","uniform":"2*k (strip index, amplitude)",
                 "profiled":"3*k (strip index, profile index, amplitude)",
                 "radon":"2*k (coefficient index, value)","parametric":"5*k (angle, offset, width, decay, amplitude)",
                 "fbp":"2*k; skimage transform, separately identified reference"},
        "budget_grid":{str(n):grids(n) for n in (128,256)},"component_grid":list(COMPONENTS),
        "statistical_unit":"document; resample whole document blocks and recompute instance median",
        "bootstrap_seed":SEED,"bootstrap_replicates":2000,"selection":selection,
        "geometry":{str(n):json.loads((OUT/f"phase19_geometry_n{n}.json").read_text()) for n in (128,256)},
        "parametric_rendering":"unit-norm exp(-q^2/2-decay*t)*(max(1-q^2/36,0))^3; q=normal distance/width; C2 compact transverse support; exact sparse rendering; causal",
        "parametric_constraints":{"width_pixels":[0.2,"n"],"decay":[-32,32],"amplitude":"[0, ||A||]; this contains every coordinatewise nonnegative optimum for unit-norm nonnegative atoms",
                                   "offset_pixels":["-sqrt(2)*n","sqrt(2)*n"]},
        "parametric_initializations":["uniform OMP","profiled OMP","importance-weighted random","multiscale sinogram proposals + NNLS"],
        "optimizer_frozen":json.loads((OUT/"phase19_optimizer_stable_frozen.json").read_text()),
        "environment":json.loads((OUT/"phase19_environment.json").read_text()),
        "decisions":json.loads((OUT/"phase19_decisions.json").read_text())["decisions"],
        "positive_control_noise":"fixed independent Gaussian noise on causal pixels, scaled to Frobenius norm 0.01 times the clean target; no clipping of observations",
        "fbp_reference":"skimage radon/iradon, 90 angles step 2 degrees, circle=False, ramp filter, raw output as phase0"}
    result={"protocol":protocol,"controls":{},"datasets":[],"summary_table":[],"limitations":[]}
    resources=OUT/"phase19_execution_resources.json"
    if resources.exists():
        result["protocol"]["execution_resources_actual"]=json.loads(resources.read_text())
    for key,filename in (("cpu_decode_audit","phase19_cpu_integrity_audit.json"),
                         ("numerical_reference_validation","phase19_stable_numerical_validation.json"),
                         ("cpu_backend_initial_timing_assessment","phase19_cpu_backend_feasibility.json"),
                         ("cpu_backend_protocol","phase19_cpu_backend_protocol_frozen.json"),
                         ("cpu_recurrence_protocol","phase19_recurrence_protocol_frozen.json"),
                         ("cpu_recurrence_validation","phase19_recurrence_numerical_validation.json"),
                         ("cpu_recurrence_runtime","phase19_cpu_recurrence_runtime_frozen.json"),
                         ("cpu_handoff_validation","phase19_cpu_handoff_validation.json")):
        audit_path=OUT/filename
        if audit_path.exists():result["protocol"][key]=json.loads(audit_path.read_text())
    for n in (128,256):
        cc=json.loads((OUT/f"phase19_controls_cpu_n{n}.json").read_text())
        gc=json.loads((OUT/f"phase19_controls_gpu_stable_n{n}.json").read_text())
        result["controls"][str(n)]={"digital":{},"parametric":{},"gradient_check":cc["gradient_check"],
                                    "gate":cc["gate_fixed_before_controls"],
                                    "raw_cpu_path":f"out/phase19_controls_cpu_n{n}.json",
                                    "raw_parametric_path":f"out/phase19_controls_gpu_stable_n{n}.json",
                                    "oracle_diagnostic_used_for_fitting":False}
        families=list(cc["digital"].items())+[("parametric",gc["cases"])]
        cpu_controls=OUT/f"phase19_controls_parametric_numba_n{n}.json"
        if cpu_controls.exists():
            families.append(("parametric_cpu_backend",json.loads(cpu_controls.read_text())["cases"]))
            result["controls"][str(n)]["raw_cpu_parametric_path"]=str(cpu_controls)
        recurrence_controls=OUT/f"phase19_controls_parametric_recurrence_n{n}.json"
        if recurrence_controls.exists():
            families.append(("parametric_cpu_recurrence",json.loads(recurrence_controls.read_text())["cases"]))
            result["controls"][str(n)]["raw_cpu_recurrence_path"]=str(recurrence_controls)
        result["controls"][str(n)]["parametric_summary_backend"]="CUDA"
        for method,rows in families:
            summary={}
            for k in [1,2,4,8]:
                for noise in [0.0,0.01]:
                    group=[r for r in rows if r["k"]==k and r["noise"]==noise]
                    values=[r["relative"] for r in group]
                    gate=1e-3 if noise==0 else 0.02
                    entry={"n":len(values),"median_relative":float(np.median(values)),
                           "max_relative":float(np.max(values)),"success_rate":float(np.mean(np.array(values)<=gate)),
                           "threshold":gate,"gate_pass":bool(np.mean(np.array(values)<=gate)>=0.90)}
                    if not method.startswith("parametric"):
                        entry["mean_exact_support_recall"]=float(np.mean([r["exact_support_recall"] for r in group]))
                        entry["mean_equivalent_atom_recall"]=float(np.mean([r["equivalent_atom_recall"] for r in group]))
                        entry["exact_support_recovery_rate"]=float(np.mean([r["exact_support_recall"]==1 for r in group]))
                        entry["equivalent_support_recovery_rate"]=float(np.mean([r["equivalent_atom_recall"]==1 for r in group]))
                    summary[f"k{k}_noise{noise}"]=entry
            if method.startswith("parametric"):result["controls"][str(n)][method]=summary
            else:result["controls"][str(n)]["digital"][method]=summary
    for record in selection["datasets"]:
        model,n=record["model_slug"],record["n"]
        cr=read_jsonl(OUT/f"phase19_cpu_{model}_n{n}.jsonl")
        gr=read_jsonl(OUT/f"phase19_gpu_stable_{model}_n{n}.jsonl")
        expected=[r["instance_id"] for r in record["instances"]]
        if [r["instance_id"] for r in cr]!=expected or [r["instance_id"] for r in gr]!=expected:
            raise ValueError(f"Incomplete or unmatched paired data: {model} n={n}")
        pairs=[]
        for c,g in zip(cr,gr):
            row={key:c[key] for key in ("archive_index","instance_id","document_index","doc_id","layer","head","offset","n","model","model_slug","norm_frobenius")}
            row["budget"]={};row["same_components"]={}
            c["methods"]["parametric"]=g["methods"]["parametric"]
            for comparison,grid in (("budget",grids(n)),("same_components",COMPONENTS)):
                for value in grid:
                    entries={}
                    for method in ["uniform","profiled","radon","parametric","svd","fbp"]:
                        cost=2*n+1 if method=="svd" else METHOD_COSTS[method]
                        k=value//cost if comparison=="budget" else value
                        source=_lookup(c,method,k)
                        entry={key:v for key,v in source.items() if key!="support"}
                        entry.update({"components":k,"stored_numbers":k*cost})
                        entries[method]=entry
                    row[comparison][str(value)]=entries
            row["full_inverse"]=_lookup(c,"radon","all")
            row["full_fbp_reference"]=_lookup(c,"fbp","all")
            row["diagnostics"]={**c["diagnostics"],"parametric":g["diagnostics"]}
            pairs.append(row)
        pair_path=OUT/"pairs"/f"phase19_richlines_{model}_n{n}.jsonl"
        with pair_path.open("x",encoding="utf-8") as f:
            for row in pairs:f.write(json.dumps(row,allow_nan=False)+"\n")
        docs=[r["doc_id"] for r in pairs]
        agg={"model":record["model"],"model_slug":model,"n":n,"n_instances":len(pairs),
             "n_documents":len(set(docs)),"pair_path":str(pair_path),"pair_sha256":digest(pair_path),
             "budget":{},"same_components":{},"full_inverse":{},"timing":{},"convergence":{}}
        for comparison,grid in (("budget",grids(n)),("same_components",COMPONENTS)):
            for method in ["uniform","profiled","radon","parametric","svd","fbp"]:
                agg[comparison][method]={}
                for value in grid:
                    rows=[r[comparison][str(value)][method] for r in pairs]
                    summary={metric:block_summary([r[metric] for r in rows],docs) for metric in ["relative","absolute"]}
                    summary["components"]=rows[0]["components"]
                    summary["stored_numbers"]=rows[0]["stored_numbers"]
                    if "converged" in rows[0]:summary["converged_fraction"]=float(np.mean([r["converged"] for r in rows]))
                    if method=="parametric":
                        summary["between_initializations_std"]=block_summary([r["start_error_std"] for r in rows],docs)
                        summary["between_initializations_range"]=block_summary([r["start_error_range"][1]-r["start_error_range"][0] for r in rows],docs)
                        summary["start_errors"]={name:block_summary([r["start_relative_errors"][index] for r in rows],docs)
                            for index,name in enumerate(rows[0]["start_names"])}
                        summary["best_start_counts"]=dict(collections.Counter(r["best_start"] for r in rows))
                        summary["refinement_solver_success_fraction"]=float(np.mean([r["refinement"]["success"] for r in rows]))
                    agg[comparison][method][str(value)]=summary
        for metric in ["relative","absolute"]:
            agg["full_inverse"][metric]=block_summary([r["full_inverse"][metric] for r in pairs],docs)
        agg["full_inverse"]["converged_fraction"]=float(np.mean([r["full_inverse"]["converged"] for r in pairs]))
        agg["full_fbp_reference"]={metric:block_summary([r["full_fbp_reference"][metric] for r in pairs],docs)
                                   for metric in ("relative","absolute")}
        agg["timing"]={"cpu_total_seconds":float(sum(r["cpu_seconds"] for r in cr)),
                       "parametric_total_seconds":float(sum(r["diagnostics"]["seconds"] for r in gr)),
                       "gpu_fit_total_seconds":float(sum(r["diagnostics"]["seconds"] for r in gr if r["diagnostics"]["device"]=="cuda")),
                       "cpu_parametric_total_seconds":float(sum(r["diagnostics"]["seconds"] for r in gr if r["diagnostics"]["device"]=="cpu"))}
        agg["parametric_backend_counts"]=dict(collections.Counter(r["diagnostics"]["device"] for r in gr))
        agg["parametric_renderer_counts"]=dict(collections.Counter(r["diagnostics"].get("backend","CUDA") for r in gr))
        cpu_control_paths={r["diagnostics"]["backend_controls"] for r in gr if r["diagnostics"]["device"]=="cpu"}
        if any(not Path(path).exists() for path in cpu_control_paths):
            raise ValueError("CPU parametric results require their complete matching controls")
        table={"model":record["model"],"n":n,"budget":{},"k8":{}}
        for comparison,values in (("budget",grids(n)),("same_components",[8])):
            for value in values:
                med={method:agg[comparison][method][str(value)]["relative"]["median"] for method in ["uniform","profiled","radon","parametric"]}
                winner=min(med,key=med.get)
                item={"line_method":winner,"line_error":med[winner],"line_errors":med,
                      "svd_error":agg[comparison]["svd"][str(value)]["relative"]["median"],
                      "selection_rule":"minimum of method medians; same complete instances for every method"}
                paired_differences=[r[comparison][str(value)][winner]["relative"]-
                                    r[comparison][str(value)]["svd"]["relative"] for r in pairs]
                item["paired_difference_line_minus_svd"]=block_summary(paired_differences,docs)
                item["line_win_fraction"]=float(np.mean(np.asarray(paired_differences)<0))
                item["svd_win_fraction"]=float(np.mean(np.asarray(paired_differences)>0))
                item["paired_difference_caution"]="The line method was selected by its median on these same cases; descriptive, without selection correction"
                if comparison=="budget":table["budget"][str(value)]=item
                else:table["k8"]=item
        result["summary_table"].append(table)
        result["datasets"].append(agg)
        progress(f"AGGREGATED paired model={model} n={n}")
    gates=[g["gate_pass"] for c in result["controls"].values() for method in c["digital"].values() for g in method.values()]
    gates += [g["gate_pass"] for c in result["controls"].values() for g in c["parametric"].values()]
    gates += [g["gate_pass"] for c in result["controls"].values() for g in c.get("parametric_cpu_backend",{}).values()]
    gates += [g["gate_pass"] for c in result["controls"].values() for g in c.get("parametric_cpu_recurrence",{}).values()]
    result["all_positive_control_gates_pass"]=all(gates)
    source_counts={(r["model_slug"],r["n"]):r["source_matrices"] for r in selection["datasets"]}
    estimated_cpu=sum(d["timing"]["cpu_total_seconds"]*source_counts[(d["model_slug"],d["n"])]/d["n_instances"]
                      for d in result["datasets"])
    estimated_gpu=sum(d["timing"]["gpu_fit_total_seconds"]*source_counts[(d["model_slug"],d["n"])]/d["n_instances"]
                      for d in result["datasets"])
    estimated_cpu_parametric=sum(d["timing"]["cpu_parametric_total_seconds"]*source_counts[(d["model_slug"],d["n"])]/d["n_instances"]
                                for d in result["datasets"])
    result["protocol"]["parametric_backend_counts"]=dict(sum((collections.Counter(d["parametric_backend_counts"]) for d in result["datasets"]),collections.Counter()))
    result["protocol"]["parametric_renderer_counts"]=dict(sum((collections.Counter(d["parametric_renderer_counts"]) for d in result["datasets"]),collections.Counter()))
    result["protocol"]["parametric_normalization_by_backend"]={
        "cuda":"Log-domain unit normalization including transverse taper, float32 rendering",
        "cpu":"Same normalized atom, float64 norm/render accumulation avoiding square underflow over the declared parameter bounds; float32 parameters and loss"}
    result["subsample_engineering_evidence"]={
        "sparse_synthesis_correlations":True,"incremental_nnls_cholesky":True,
        "radon_nnls_working_set_with_full_kkt_check":True,"fused_sparse_cuda_rendering":True,
        "exact_cpu_gaussian_recurrence_validated":"cpu_recurrence_validation" in result["protocol"],
        "estimated_full_archive_cpu_worker_hours":estimated_cpu/3600,
        "estimated_full_archive_cpu_wall_hours_with_three_workers":estimated_cpu/10800,
        "estimated_full_archive_parametric_cpu_worker_hours_at_observed_backend_mix":estimated_cpu_parametric/3600,
        "estimated_full_archive_single_gpu_hours":estimated_gpu/3600,
        "estimation":"Extrapolate per-dataset measured fit time by source_matrices/selected_matrices and observed CPU/CUDA backend mix; core CPU estimate excludes parametric fits, separately reported; excludes setup, aborted handoff cases and GPU lock waits; not a benchmark of unselected matrices or a controlled backend speed comparison",
        "selection_fixed_before_attention_evaluation":True,"selection_file":str(SELECTION)}
    result["protocol"]["source_code_sha256"]={str(p):digest(p) for p in [Path("phase19_richlines.py"),*sorted(Path('.').glob('richlines_*.py'))]}
    result["protocol"]["decisions"].extend([
        {"question":"How to strengthen continuous fitting without changing the representation budget?",
         "suggestion":"Four fixed starts, including multiscale proposals, and L-BFGS-B after Adam; freeze before all reported fits",
         "certainty":"high","executed":True},
        {"question":"How to handle norm-square underflow?",
         "suggestion":"Log-domain unit normalization and the mathematically redundant amplitude upper bound; rerun all parametric cases",
         "certainty":"high","executed":True}])
    if result["protocol"]["parametric_backend_counts"].get("cpu",0):
        result["protocol"]["decisions"].append({"question":"How to progress while the shared GPU is occupied?",
            "suggestion":"Validate the same primitive family on CPU, run identical controls, preassign remaining cohorts by availability, and hand off explicitly when CUDA is available",
            "certainty":"medium","executed":True})
    if result["protocol"]["parametric_renderer_counts"].get("Numba CPU exact recurrence",0):
        result["protocol"]["decisions"].append({"question":"How to reduce CPU rendering cost without changing the line family?",
            "suggestion":"Use exact Gaussian recurrences after full-domain value/gradient validation and the same 64 positive controls; rotate complete cases across available dataset leases",
            "certainty":"high","executed":True})
    baseline=OUT/"phase19_controls_gpu_n128.json"
    if baseline.exists():
        result["control_development_history"]={"initial_optimizer":"450 Adam steps, three starts; failed synthetic mixtures",
            "preserved_baseline_path":str(baseline),
            "final_optimizer":"Four starts including multiscale proposals; 450 Adam steps followed by up to 150 L-BFGS-B iterations",
            "fixed_before_all_reported_parametric_fits":True,"seeds_and_acceptance_thresholds_unchanged":True}
    result["numerical_stability_revision"]={
        "issue":"Float32 norm squares underflowed for a line barely intersecting the causal region; first three real fits preserved in an unused baseline cache",
        "fix":"Compute unit-norm atoms with log-sum-exp scaling, including the compact transverse taper; no nonfinite value was replaced by zero",
        "amplitude_bound":"0 <= amplitude <= ||A||; coordinatewise NNLS optimum for nonnegative unit-norm atoms is always within this bound",
        "policy":"All selected instances and all parametric positive controls rerun using the stable renderer; same seeds and grids",
        "unused_real_baseline_cache":"out/phase19_gpu_gpt2_n128.jsonl"}
    result["numerical_stability_revision"]["cpu_backend"]="The optional CPU fallback evaluates the same normalized atom in float64; identical controls and a separate backend source freeze are reported"
    result["limitations"]=[
        "Fixed 64-instance stratified subset per dataset; 64 document blocks; layer/head estimates do not cover all archived heads.",
        "Planted positive controls cover k=1,2,4,8; parametric truth widths are 0.6..4 pixels and decay -4..4. They do not certify global optimization at larger k or over every allowed primitive parameter.",
        "Finite angle, offset and decay grids; finite nonconvex optimization and four initializations do not exclude other line representations or global optima.",
        "Best-line summary selects a method on these evaluation errors; it is an optimistic descriptive envelope, not a separately validated compressor.",
        "SVD is not causally remasked: whole-matrix rank approximation is scored exactly as phase05; this experiment makes no downstream or inference-causality claim.",
        "Same component count is not the same storage cost; the two comparisons are kept separate.",
        "Any failed positive control or nonconvergence remains in every paired aggregate and limits a negative scientific interpretation."]
    if result["protocol"]["parametric_backend_counts"].get("cpu",0):
        result["limitations"].append("Some n=256 parametric fits use float64 CPU rendering with float32 parameters/loss; CUDA uses float32 rendering. Value/gradient equivalence and identical positive controls are reported separately. Numerical nonconvex paths can differ; backend assignment and handoff depend only on resource availability, never on fitted error.")
        if "cpu_backend_initial_timing_assessment" in result["protocol"]:
            result["protocol"]["cpu_backend_initial_timing_assessment"]["historical_assessment_superseded_by"]="out/phase19_cpu_backend_protocol_frozen.json and out/phase19_recurrence_protocol_frozen.json; final usage is in parametric_renderer_counts"
    write_json(OUT/"phase19_richlines.json",result)
    progress(f"COMPLETE out/phase19_richlines.json; all positive-control gates pass={all(gates)}")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",nargs="?",default="run",choices=["run","prepare","freeze","geometry","cpu","controls","aggregate"])
    parser.add_argument("--n",type=int,choices=[128,256])
    parser.add_argument("--models",nargs="+",choices=MODELS,default=MODELS)
    args=parser.parse_args()
    if args.mode in ["geometry","cpu","controls"] and args.n is None:
        parser.error("--n is required")
    if args.mode=="run":
        from richlines_run import run
        run()
    elif args.mode=="prepare":
        prepare();prepare_runtime()
    elif args.mode=="freeze":prepare_runtime()
    elif args.mode=="geometry":geometry(args.n)
    elif args.mode=="cpu":cpu(args.n,args.models)
    elif args.mode=="controls":controls(args.n)
    elif args.mode=="aggregate":aggregate()


if __name__=="__main__":main()
