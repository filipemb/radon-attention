"""Document-block summaries and paired document-level signed-rank tests."""
import phase19b_common
import csv,itertools
from pathlib import Path
import numpy as np
from scipy.stats import wilcoxon,rankdata
from phase19b_common import (SEED,ROOT,PROTOCOL,RANKS,SELECTION,read_json,write_json,progress,
    cache_path,budgets,line_counts,digest)
from phase19b_stats import parameter_distribution,FWHM_FACTOR


def block_summary(values,documents):
    if any(v is None for v in values):
        return {"n_instances":len(values),"n_documents":len(set(documents)),"undefined_count":sum(v is None for v in values),
                "median":None,"median_ci95_document_block":None,"reason":"Undefined energy/distribution retained; no conditional primary median"}
    a=np.asarray(values,dtype=float)
    if not np.isfinite(a).all():raise ValueError("Nonfinite value cannot enter aggregation")
    docs=np.unique(documents);groups=[np.flatnonzero(np.asarray(documents)==doc) for doc in docs]
    rng=np.random.default_rng(SEED);draws=rng.integers(0,len(groups),(2000,len(groups)))
    if len({len(g) for g in groups})==1:
        indices=np.asarray(groups)[draws].reshape(2000,-1);replicates=np.median(a[indices],axis=1)
    else:replicates=np.asarray([np.median(a[np.concatenate([groups[i] for i in row])]) for row in draws])
    q=np.quantile(a,[.25,.5,.75]);ci=np.quantile(replicates,[.025,.975])
    means=[float(a[g].mean()) for g in groups]
    return {"n_instances":len(a),"n_documents":len(groups),"median":float(q[1]),"q25":float(q[0]),"q75":float(q[2]),
        "iqr":float(q[2]-q[0]),"median_ci95_document_block":ci.tolist(),"bootstrap_replicates":2000,"seed":SEED,
        "secondary_mean_of_document_means":float(np.mean(means))}


def paired_test(a,b,documents):
    difference=np.asarray(a)-np.asarray(b);docs=np.unique(documents)
    bydoc=np.asarray([np.median(difference[np.asarray(documents)==doc]) for doc in docs])
    nonzero=bydoc[bydoc!=0]
    if len(nonzero):
        result=wilcoxon(bydoc,zero_method="wilcox",correction=False,alternative="two-sided",method="auto")
        statistic=float(result.statistic);p=float(result.pvalue)
        ranks=rankdata(np.abs(nonzero));rplus=float(ranks[nonzero>0].sum());rminus=float(ranks[nonzero<0].sum())
        rbc=(rplus-rminus)/(rplus+rminus)
    else:statistic=0.;p=1.;rbc=0.
    if not np.isfinite([statistic,p,rbc]).all():raise ValueError("Undefined Wilcoxon result")
    return {"difference_a_minus_b":block_summary(difference,documents),"wilcoxon_statistic":statistic,
        "wilcoxon_p_two_sided":p,"rank_biserial_a_minus_b":rbc,"n_documents":len(docs),
        "all_zero_document_differences":len(nonzero)==0,
        "n_nonzero_documents":len(nonzero),"document_median_differences":bydoc.tolist(),
        "method":"scipy.stats.wilcoxon(method=auto, zero_method=wilcox), document medians of paired instance differences",
        "fraction_instances_a_lower":float(np.mean(difference<0)),"fraction_instances_b_lower":float(np.mean(difference>0))}


def width_summary(records,n):
    docs=[r["doc_id"] for r in records];result={"n_instances":len(records),"by_budget":{}}
    for B in records[0]["budget"]:
        rows=[r["budget"][B] for r in records];pooled=[]
        for row in rows:
            p=np.asarray(row["parameters"]).copy();p[:,4]/=row["norm_frobenius"];pooled.append(p)
        distribution=parameter_distribution(np.concatenate(pooled),n,1.)
        entry={"pooled_atom_distribution":distribution,
            "pooled_active_weighting":"Each stored atom has equal weight; active flag uses amplitude/instance Frobenius norm >1e-8. Separate instance summaries preserve equal instance weight.",
            "per_instance":{},"wide_energy_share":{}}
        for subset in ("all_atoms","active_atoms"):
            entry["per_instance"][subset]={}
            for variable in ("width_pixels","transverse_fwhm_pixels","decay_signed_canonical","absolute_decay","normal_angle_degrees_mod_180"):
                for quantile in ("q25","median","q75"):
                    values=[row["parameter_distribution"][subset][variable][quantile] if row["parameter_distribution"][subset][variable] else None for row in rows]
                    entry["per_instance"][subset][variable+"_"+quantile]=block_summary(values,docs)
            entry["per_instance"][subset]["width_fraction_greater_than"]={
                threshold:block_summary([row["parameter_distribution"][subset]["width_fraction_greater_than"][threshold] for row in rows],docs)
                for threshold in ("2.0","8.0",str(n/8))}
        for threshold in ("2.0","8.0",str(n/8)):
            entry["wide_energy_share"][threshold]={name:block_summary([row["wide_energy"][threshold][name] for row in rows],docs)
                for name in ("additive_share","self_energy_share","deletion_share")}
        entry["active_atom_count"]=block_summary([row["parameter_distribution"]["n_active_atoms"] for row in rows],docs)
        entry["zero_reconstruction_count"]=sum(row["zero_reconstruction"] for row in rows)
        result["by_budget"][B]=entry
    return result


def controls_summary():
    result={};all_gates=[]
    for n in (128,256):
        rows=[read_json(ROOT/"controls"/f"n{n}_i{i}.json") for i in range(64)]
        result[str(n)]={}
        for arm in ("free","thin"):
            groups={}
            for k in (1,2,4,8):
                for noise in (0.,.01):
                    group=[r for r in rows if r["k"]==k and r["noise"]==noise];v=np.asarray([r["arms"][arm]["relative"] for r in group])
                    threshold=.001 if noise==0 else .02;success=float(np.mean(v<=threshold));all_gates.append(success>=.9)
                    groups[f"k{k}_noise{noise}"]={"n":len(v),"successes":int(np.sum(v<=threshold)),"success_rate":success,
                        "median_relative":float(np.median(v)),"max_relative":float(v.max()),"threshold":threshold,"gate_pass":success>=.9}
            result[str(n)][arm]=groups
    return result,all(all_gates)


def aggregate():
    output=Path("out/phase19b_richlines.json")
    if output.exists():raise FileExistsError(output)
    selection=read_json(SELECTION);parent=read_json("out/phase19_selection.json");protocol=read_json(PROTOCOL)
    # Preflight the full planned experiment before creating any pair files.
    for record in parent["datasets"]:
        for inst in record["instances"]:
            p=cache_path("original",record["model_slug"],record["n"],inst["archive_index"])
            if not p.exists():raise ValueError(f"Missing parameter diagnostic: {p}")
    for record in selection["datasets"]:
        for inst in record["instances"]:
            for kind in ("init","free","thin"):
                p=cache_path(kind,record["model_slug"],record["n"],inst["archive_index"])
                if not p.exists():raise ValueError(f"Missing extension case: {p}")
    result={"protocol":protocol,"selection":selection,"parameter_diagnostics_768":[],"comparisons_192":[],
            "controls":{},"limitations":[
                "Original parameter snapshots exist for 241/768 cases. The other527 are replays, never claimed to recover the identical original optimizer state; original and decoded error deltas are retained.",
                "The extensions use a fixed 192-case subset,16 documents per model x n; confidence intervals and signed-rank tests are document-block based.",
                "Finite nonconvex optimization is not a global optimum certificate; all failed controls, nonconvergence and nesting/monotonicity violations remain visible.",
                "Widths are sigma, with tapered-profile FWHM=2.1775229093*sigma and support radius6*sigma. Thin means sigma<=2, not total support width two pixels.",
                "All codec costs are stored-number counts, not quantized bitrates; reconstruction accuracy alone does not establish useful inference replacement or encoding throughput."]}
    result["limitations"].append("execution.seconds is elapsed wall time; the suspended CPU case includes the GPU handoff pause. No optimizer uses a wall-time stopping rule.")
    result["protocol"]["numerical_validation"]=read_json("out/phase19b_numerical_validation.json")
    result["protocol"]["omp_continuation_validation"]=read_json("out/phase19b_omp_validation.json")
    result["protocol"]["statistics_validation"]=read_json("out/phase19b_statistics_validation.json")
    result["decisions"]=read_json("out/phase19b_decisions.json")
    result["resource_addendum"]=read_json("out/phase19b_resource_addendum.json")
    resource_path=Path("out/phase19b_gpu_resource_handoff_complete.json")
    result["resource_handoff"]={"gpu_used":resource_path.exists(),"maximum_active_calculation_processes":3}
    if resource_path.exists():
        result["resource_handoff"].update({"start":read_json("out/phase19b_gpu_resource_handoff.json"),"finish":read_json(resource_path)})
    csv_rows=[];tests=[];source_counts={};replay_deltas=[];extension_by_n={128:[],256:[]}
    original_by_key={}
    for record in parent["datasets"]:
        model,n=record["model_slug"],record["n"]
        rows=[read_json(cache_path("original",model,n,r["archive_index"])) for r in record["instances"]]
        if [r["instance_id"] for r in rows]!=[r["instance_id"] for r in record["instances"]]:raise AssertionError("Original parameter identities differ")
        p=Path("out/pairs")/f"phase19b_parameters_{model}_n{n}.jsonl"
        with p.open("x",encoding="utf-8") as f:
            import json
            for row in rows:f.write(json.dumps(row,allow_nan=False)+"\n")
        for row in rows:
            original_by_key[row["instance_id"]]=row
            source_counts[row["parameter_provenance"]]=source_counts.get(row["parameter_provenance"],0)+1
            replay_deltas.extend(v["optimization_error_delta_from_phase19"] for v in row["budget"].values() if row["parameter_provenance"]!="original_phase19_export")
        summary=width_summary(rows,n)
        summary.update({"model":record["model"],"model_slug":model,"n":n,"pair_path":p.as_posix(),"pair_sha256":digest(p),
            "parameter_provenance_counts":{s:sum(r["parameter_provenance"]==s for r in rows) for s in set(r["parameter_provenance"] for r in rows)},
            "replay_error_delta":block_summary([np.median([v["optimization_error_delta_from_phase19"] for v in r["budget"].values()]) for r in rows],[r["doc_id"] for r in rows])})
        result["parameter_diagnostics_768"].append(summary)
        progress(f"phase19b aggregated original-budget parameters {model} n={n}")
    for record in selection["datasets"]:
        model,n=record["model_slug"],record["n"];pairs=[]
        for inst in record["instances"]:
            key=(model,n,inst["archive_index"]);free=read_json(cache_path("free",*key));thin=read_json(cache_path("thin",*key));init=read_json(cache_path("init",*key))
            if free["instance_id"]!=inst["instance_id"] or thin["instance_id"]!=inst["instance_id"]:raise AssertionError("Unpaired extension identity")
            if free["diagnostics"]["initialization_hashes_before_width_projection"]!=thin["diagnostics"]["initialization_hashes_before_width_projection"]:
                raise AssertionError("Different starts between arms")
            row={k:free[k] for k in ("archive_index","instance_id","document_index","doc_id","layer","head","offset","n","model","model_slug")}
            row["budget"]={};row["diagnostics"]={"free":free["diagnostics"],"thin":thin["diagnostics"],"initialization":init["diagnostics"]}
            for r,B in zip(RANKS,budgets(n)):
                sv={**init["svd"][str(r)],"components":r,"stored_numbers":r*(2*n+1)}
                row["budget"][str(B)]={"svd":sv,"free":free["budget"][str(B)],"thin":thin["budget"][str(B)]}
            pairs.append(row)
        extension_by_n[n].extend(pairs)
        p=Path("out/pairs")/f"phase19b_comparison_{model}_n{n}.jsonl"
        with p.open("x",encoding="utf-8") as f:
            for row in pairs:f.write(json.dumps(row,allow_nan=False)+"\n")
        docs=[r["doc_id"] for r in pairs];dataset={"model":record["model"],"model_slug":model,"n":n,"n_instances":len(pairs),
            "n_documents":len(set(docs)),"pair_path":p.as_posix(),"pair_sha256":digest(p),"budget":{}}
        for rank,B in zip(RANKS,budgets(n)):
            rows=[r["budget"][str(B)] for r in pairs];entry={"svd_rank":rank,"budget":B,"methods":{},"paired_tests":{}}
            for method in ("svd","free","thin"):
                entry["methods"][method]={metric:block_summary([r[method][metric] for r in rows],docs) for metric in ("relative","absolute")}
                if method!="svd":
                    entry["methods"][method]["converged_fraction"]=float(np.mean([r[method]["converged"] for r in rows]))
                    entry["methods"][method]["lbfgsb_success_fraction"]=float(np.mean([r[method]["refinement"]["success"] for r in rows]))
                    entry["methods"][method]["refinement_iteration_limit_fraction"]=float(np.mean([
                        r[method]["refinement"]["iterations"]>=r[method]["refinement"]["max_iterations"] for r in rows]))
                    entry["methods"][method]["start_error_standard_deviation"]=block_summary([r[method]["start_error_std"] for r in rows],docs)
                    entry["methods"][method]["start_error_spread"]=block_summary([
                        r[method]["start_error_range"][1]-r[method]["start_error_range"][0] for r in rows],docs)
                    entry["methods"][method]["backend_counts"]={device:sum(p["diagnostics"][method]["device"]==device for p in pairs)
                        for device in sorted({p["diagnostics"][method]["device"] for p in pairs})}
            for a,b in (("free","svd"),("thin","svd"),("free","thin")):
                test=paired_test([r[a]["relative"] for r in rows],[r[b]["relative"] for r in rows],docs)
                entry["paired_tests"][a+"_minus_"+b]=test;tests.append(test)
            entry["thin_better_than_free_fraction"]=float(np.mean([r["thin"]["relative"]<r["free"]["relative"]-1e-6 for r in rows]))
            entry["nesting_note"]="Free contains thin; observed thin improvements diagnose optimizer limits, not superior global expressiveness"
            no_broad=np.asarray([r["free"]["wide_energy"]["2.0"]["additive_share"]==0 for r in rows])
            free_lower=np.asarray([r["free"]["relative"]<r["thin"]["relative"]-1e-6 for r in rows])
            entry["thin_feasibility_of_free_solution"]={
                "descriptive_posthoc_diagnostic_no_new_test":True,
                "fraction_free_solutions_with_exactly_zero_broad_contribution":float(no_broad.mean()),
                "fraction_free_lower_than_thin_and_zero_broad_contribution":float(np.mean(no_broad&free_lower)),
                "same_cohort_upper_bound_on_error_after_removing_broad_atoms":block_summary([
                    r["free"]["relative"]+np.sqrt(r["free"]["wide_energy"]["2.0"]["wide_self_energy"])/r["free"]["norm_frobenius"] for r in rows],docs),
                "definition":"Set amplitudes of sigma>2 atoms to zero, then clamp those zero-amplitude widths to2. This is a thin-feasible code at the same5*k cost. Triangle inequality bounds its relative error by free_error+||wide||/||A||. Zero broad contribution gives an exact thin-feasible witness even if the independently optimized thin arm has higher error. No primary fit, median or test is replaced."}
            dataset["budget"][str(B)]=entry
            c={"model":record["model"],"n":n,"rank":rank,"budget":B}
            for method in ("svd","free","thin"):
                s=entry["methods"][method]["relative"];c[method+"_median"]=s["median"];c[method+"_ci_low"],c[method+"_ci_high"]=s["median_ci95_document_block"]
            csv_rows.append((c,entry))
        dataset["parameter_diagnostics"]={a:width_summary([{**r,"budget":{B:r["budget"][B][a] for B in r["budget"]}} for r in pairs],n) for a in ("free","thin")}
        result["comparisons_192"].append(dataset)
        progress(f"phase19b aggregated paired extension {model} n={n}")
    previous=0.
    for position,i in enumerate(np.argsort([t["wilcoxon_p_two_sided"] for t in tests],kind="stable")):
        adjusted=min(1.,max(previous,tests[i]["wilcoxon_p_two_sided"]*(len(tests)-position)));previous=adjusted
        tests[i]["wilcoxon_p_holm_all180"]=adjusted
    for c,entry in csv_rows:
        for name,test in entry["paired_tests"].items():
            c[name+"_p"]=test["wilcoxon_p_two_sided"];c[name+"_p_holm"]=test["wilcoxon_p_holm_all180"]
    with Path("out/phase19b_comparison.csv").open("x",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(csv_rows[0][0]));writer.writeheader();writer.writerows(c for c,_ in csv_rows)
    result["controls"],result["all_positive_control_gates_pass"]=controls_summary()
    result["parameter_provenance_counts"]=source_counts
    result["parameter_diagnostics_768_by_n"]={str(n):width_summary([r for r in original_by_key.values() if r["n"]==n],n) for n in (128,256)}
    result["extension_parameter_diagnostics_by_n"]={str(n):{a:width_summary([
        {**r,"budget":{B:r["budget"][B][a] for B in r["budget"]}} for r in extension_by_n[n]],n)
        for a in ("free","thin")} for n in (128,256)}
    replay_deltas=np.asarray(replay_deltas)
    result["replay_error_delta_summary"]={"median":float(np.median(replay_deltas)),"max_absolute":float(np.max(np.abs(replay_deltas))),
        "median_absolute":float(np.median(np.abs(replay_deltas))),"q95_absolute":float(np.quantile(np.abs(replay_deltas),.95)),
        "fraction_absolute_greater_than_0.001":float(np.mean(np.abs(replay_deltas)>.001)),
        "fraction_absolute_greater_than_0.01":float(np.mean(np.abs(replay_deltas)>.01)),
        "n_budget_points":len(replay_deltas),"definition":"Optimization relative error of replay minus phase19 reported relative error; no replay chosen by this delta"}
    parameter_csv=[]
    for scope,datasets in (("phase19_parameter_diagnostics",result["parameter_diagnostics_768"]),("paired_extension",result["comparisons_192"])):
        for dataset in datasets:
            summaries={"phase19_free":dataset} if scope=="phase19_parameter_diagnostics" else dataset["parameter_diagnostics"]
            for arm,summary in summaries.items():
                for B,v in summary["by_budget"].items():
                    pooled=v["pooled_atom_distribution"];row={"scope":scope,"model":dataset["model"],"n":dataset["n"],"arm":arm,"budget":B}
                    for subset in ("all_atoms","active_atoms"):
                        for var in ("width_pixels","absolute_decay","normal_angle_degrees_mod_180"):
                            for q in ("q25","median","q75"):
                                row[subset+"_"+var+"_"+q]=pooled[subset][var][q] if pooled[subset][var] else None
                        for threshold in ("2.0","8.0",str(dataset["n"]/8)):
                            row[subset+"_fraction_width_gt_"+threshold]=pooled[subset]["width_fraction_greater_than"][threshold]
                    e=v["wide_energy_share"]["2.0"]["additive_share"]
                    row["wide_energy_median"]=e["median"]
                    row["wide_energy_ci_low"],row["wide_energy_ci_high"]=e["median_ci95_document_block"] or [None,None]
                    parameter_csv.append(row)
    fields=list(dict.fromkeys(k for row in parameter_csv for k in row))
    with Path("out/phase19b_parameters.csv").open("x",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(parameter_csv)
    result["files"]={"comparison_csv":"out/phase19b_comparison.csv","parameter_csv":"out/phase19b_parameters.csv"}
    result["source_code_sha256"]={p.as_posix():digest(p) for p in sorted(Path('.').glob('phase19b_*.py'))}
    write_json(output,result);progress("PHASE19B final JSON,24 paired files and comparison CSV complete")
    return result


if __name__=="__main__":aggregate()
