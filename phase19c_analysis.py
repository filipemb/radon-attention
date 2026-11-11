"""Document-paired effects are primary; marginal error medians are secondary."""
import phase19c_common
import csv,json
from pathlib import Path
import numpy as np
from scipy.stats import wilcoxon,rankdata
from phase19c_common import SEED,read_json,write_json,read_jsonl,digest,budgets,tag,progress

ROOT=Path("out/phase19c_v2_cache")
ARMS=("masked","svd","free","thin")
PAIRS=(("free","masked"),("thin","masked"),("svd","masked"),("free","svd"),("thin","svd"),("free","thin"))

def summary(values,documents):
    if len(values)!=len(documents) or not len(values):raise ValueError("Empty or unmatched summary")
    missing=sum(v is None for v in values)
    if missing:return {"n_instances":len(values),"n_documents":len(set(documents)),"undefined_count":missing,
        "median":None,"q25":None,"q75":None,"iqr":None,"ci95":None,"reason":"Undefined codecs retained; no conditional primary median"}
    a=np.asarray(values,dtype=float)
    if not np.isfinite(a).all():raise ValueError("Nonfinite measurement")
    labels=np.asarray(documents);docs=np.unique(labels)
    perdoc=np.array([np.median(a[labels==d]) for d in docs])
    rng=np.random.default_rng(SEED);indices=rng.integers(0,len(docs),(2000,len(docs)))
    boot=np.median(perdoc[indices],axis=1);q=np.quantile(perdoc,[.25,.5,.75])
    return {"n_instances":len(a),"n_documents":len(docs),"undefined_count":0,"median":float(q[1]),
        "q25":float(q[0]),"q75":float(q[2]),"iqr":float(q[2]-q[0]),"ci95":np.quantile(boot,[.025,.975]).tolist(),
        "bootstrap_replicates":2000,"seed":SEED,"definition":"median of document medians; percentile bootstrap over whole documents"}

def paired(a,b,documents,inference=True):
    n=len(a);missing=sum(x is None or y is None for x,y in zip(a,b))
    if missing:
        known=[x-y for x,y in zip(a,b) if x is not None and y is not None]
        wins=sum(v<0 for v in known)
        return {"n_instances":n,"n_documents":len(set(documents)),"undefined_pairs":missing,
            "paired_effect":summary([x-y if x is not None and y is not None else None for x,y in zip(a,b)],documents),"fraction_instances_a_wins":None,"fraction_instances_b_wins":None,
            "fraction_ties":None,"known_a_win_count":wins,"a_win_fraction_bounds":[wins/n,(wins+missing)/n],
            "wilcoxon_p":None,"wilcoxon_statistic":None,"rank_biserial":None,
            "reason":"At least one codec cannot decode; no conditional median, test or point win fraction"}
    delta=np.asarray(a,dtype=float)-np.asarray(b,dtype=float)
    if not np.isfinite(delta).all():raise ValueError("Nonfinite paired difference")
    labels=np.asarray(documents);docs=np.unique(labels);d=np.array([np.median(delta[labels==doc]) for doc in docs]);nz=d[d!=0]
    statistic=pvalue=rbc=None
    if inference:
        if len(nz):
            test=wilcoxon(d,zero_method="wilcox",method="auto",alternative="two-sided",correction=False)
            statistic=float(test.statistic);pvalue=float(test.pvalue);ranks=rankdata(np.abs(nz))
            rbc=float((ranks[nz>0].sum()-ranks[nz<0].sum())/ranks.sum())
        else:statistic=0.;pvalue=1.;rbc=0.
        if not np.isfinite([statistic,pvalue,rbc]).all():raise ValueError("Undefined signed-rank result")
    return {"n_instances":n,"n_documents":len(docs),"undefined_pairs":0,"paired_effect":summary(delta.tolist(),documents),
        "fraction_instances_a_wins":float(np.mean(delta<0)),"fraction_instances_b_wins":float(np.mean(delta>0)),
        "fraction_ties":float(np.mean(delta==0)),"document_median_differences":d.tolist(),
        "wilcoxon_p":pvalue,"wilcoxon_statistic":statistic,"rank_biserial":rbc,"inference":inference,
        "definition":"Delta=e_a-e_b within each instance, median within document then median across documents. Negative favors a. Instance win fractions use strict comparisons, exact ties retained.",
        "wilcoxon_definition":"two-sided scipy method=auto, zero_method=wilcox, on document median paired differences" if inference else "Deterministic control: no inferential p-value"}

def holm(tests,planned):
    valid=[t for t in tests if t["wilcoxon_p"] is not None]
    if len(tests)!=planned:raise AssertionError(f"Unexpected testing family size {len(tests)} != {planned}")
    previous=0.
    for rank,index in enumerate(np.argsort([t["wilcoxon_p"] for t in valid],kind="stable")):
        adjusted=min(1.,max(previous,valid[index]["wilcoxon_p"]*(planned-rank)));previous=adjusted
        valid[index]["wilcoxon_p_holm"]=float(adjusted)
    for t in tests:
        if t["wilcoxon_p"] is None:t["wilcoxon_p_holm"]=None
        t["holm_planned_family_size"]=planned

def method_summary(rows,documents,arm,precision):
    measurements=[r[arm] if precision=="reference" else r[arm]["fp16"] for r in rows]
    return {metric:summary([v[metric] for v in measurements],documents) for metric in ("relative","absolute")}

def point(rows,documents,inference=True,quantized_inference=True):
    result={"reference":{"methods":{},"paired":{}},"binary16":{"methods":{},"paired":{}},"precision_sensitivity":{}}
    result["costs"]={a:rows[0][a]["stored_numbers"] for a in ARMS}
    if any(r[a]["stored_numbers"]!=result["costs"][a] for r in rows for a in ARMS):raise AssertionError("Changing cost within a paired point")
    for precision in ("reference","binary16"):
        result[precision]["methods"]={a:method_summary(rows,documents,a,precision) for a in ARMS}
        for a,b in PAIRS:
            av=[r[a]["relative"] if precision=="reference" else r[a]["fp16"]["relative"] for r in rows]
            bv=[r[b]["relative"] if precision=="reference" else r[b]["fp16"]["relative"] for r in rows]
            result[precision]["paired"][a+"_minus_"+b]=paired(av,bv,documents,inference=inference and precision=="reference")
        if precision=="binary16" and inference and quantized_inference:
            # Precision comparisons have their own predeclared testing family.
            for a,b in PAIRS:
                result[precision]["paired"][a+"_minus_"+b]=paired(
                    [r[a]["fp16"]["relative"] for r in rows],[r[b]["fp16"]["relative"] for r in rows],documents)
    for arm in ARMS:
        base=[r[arm]["relative"] for r in rows];quant=[r[arm]["fp16"]["relative"] for r in rows]
        result["precision_sensitivity"][arm]={"quantized_minus_reference":paired(quant,base,documents,inference=False),
            "codec_failures":sum(v is None for v in quant),"failure_fraction":sum(v is None for v in quant)/len(quant),
            "stored_numbers":rows[0][arm]["stored_numbers"],"stored_bits":16*rows[0][arm]["stored_numbers"],
            "maximum_error_change":max(abs(x-y) for x,y in zip(quant,base)) if all(v is not None for v in quant) else None}
    return result

def pair_file(path,rows):
    path=Path(path)
    with path.open("x",encoding="utf-8") as f:
        for row in rows:f.write(json.dumps(row,allow_nan=False)+"\n")
    return {"pair_path":path.as_posix(),"pair_sha256":digest(path)}

def attention_cohort(selection_path,cohort):
    selection=read_json(selection_path);datasets=[];extension=cohort=="phase19b_192"
    ranks=(1,2,4,8,16) if extension else (1,2,4)
    for d in selection["datasets"]:
        model,n=d["model_slug"],d["n"];pairs=[]
        for inst in d["instances"]:
            name=tag(model,n,inst["archive_index"])+".json";base=read_json(ROOT/"baseline"/name)
            if base["instance_id"]!=inst["instance_id"]:raise AssertionError("Unpaired baseline")
            row={k:base[k] for k in ("archive_index","instance_id","document_index","doc_id","layer","head","offset","n","model","model_slug")}
            row["budget"]={};row["cohort"]=cohort
            if not extension:
                thin=read_json(ROOT/"thin768"/name)
                if thin["instance_id"]!=inst["instance_id"]:raise AssertionError("Unpaired new thin768 fit")
                row["thin_diagnostics"]=thin["diagnostics"];row["free_parameter_provenance"]=base["free768_parameter_provenance"]
                row["historical_phase19_free_errors"]=base["free_historical"]
            for r,B in zip(ranks,budgets(n,ranks)):
                free=base["extension192"]["free"][str(B)] if extension else base["free768"][str(B)]
                fine=base["extension192"]["thin"][str(B)] if extension else thin["budget"][str(B)]
                row["budget"][str(B)]={"svd":base["svd"][str(r)],"masked":base["masked"][str(r)],"free":free,"thin":fine}
            pairs.append(row)
        docs=[r["doc_id"] for r in pairs]
        dataset={"cohort":cohort,"model":d["model"],"model_slug":model,"n":n,"n_instances":len(pairs),
            "n_documents":len(set(docs)),"budget":{},**pair_file(f"out/pairs/phase19c_{cohort}_{model}_n{n}.jsonl",pairs)}
        for rank,B in zip(ranks,budgets(n,ranks)):
            rows=[p["budget"][str(B)] for p in pairs];entry=point(rows,docs);entry.update({"rank":rank,"budget":B})
            dataset["budget"][str(B)]=entry
        datasets.append(dataset);progress(f"phase19c aggregated {cohort} {model} n={n}")
    return datasets

def controls():
    from phase19c_synthetic_controls import make
    from phase19c_metrics import line_result,factor_precision
    protocol=read_json("out/phase19c_protocol_v2.json");plan=protocol["synthetic_specs"]
    negatives=[];planted=[];masked=[]
    for n in (128,256):
        nr=[];pr=[];mr=[]
        for spec in plan["negative"]:
            if spec["n"]!=n:continue
            key=spec["id"];init=read_json(ROOT/"negative_init"/(key+".json"));a=read_json(ROOT/"negative_free"/(key+".json"));b=read_json(ROOT/"negative_thin"/(key+".json"))
            if a["diagnostics"]["initialization_hashes_before_width_projection"]!=b["diagnostics"]["initialization_hashes_before_width_projection"]:raise AssertionError("Negative control starts differ")
            rows={str(B):{"svd":init["svd"][str(r)],"masked":init["masked"][str(r)],"free":a["budget"][str(B)],"thin":b["budget"][str(B)]}
                for r,B in zip((1,2,4),budgets(n,(1,2,4)))}
            nr.append({**spec,"doc_id":key,"generation":init["generation"],"budget":rows,"diagnostics":{"free":a["diagnostics"],"thin":b["diagnostics"]}})
        nf=pair_file(f"out/pairs/phase19c_negative_n{n}.jsonl",nr)
        for family in sorted({r["family"] for r in nr}):
            group=[r for r in nr if r["family"]==family];docs=[r["doc_id"] for r in group]
            item={"family":family,"n":n,"n_draws":len(group),"unit":"synthetic draw, not a corpus document",**nf,"budget":{}}
            for rank,B in zip((1,2,4),budgets(n,(1,2,4))):
                v=point([g["budget"][str(B)] for g in group],docs,inference=family!="uniform_causal",quantized_inference=False);v.update({"rank":rank,"budget":B});item["budget"][str(B)]=v
            negatives.append(item)
        for spec in plan["planted"]:
            if spec["n"]!=n:continue
            key=spec["id"];a=read_json(ROOT/"planted_free"/(key+".json"));b=read_json(ROOT/"planted_thin"/(key+".json"))
            if a["diagnostics"]["initialization_hashes_before_width_projection"]!=b["diagnostics"]["initialization_hashes_before_width_projection"]:raise AssertionError("Planted control starts differ")
            target,_=make(spec)
            oracle=line_result(a["generation"]["truth"],target)
            pr.append({**spec,"doc_id":key,"generation":a["generation"],"arms":{"free":a,"thin":b},
                "oracle_truth_code":oracle,"oracle_note":"Known planted parameters, not a fitted code; never substituted into primary results"})
        pf=pair_file(f"out/pairs/phase19c_planted_n{n}.jsonl",pr)
        for k in (51,102,205):
            for noise in (0.,.01):
                group=[p for p in pr if p["k"]==k and p["noise"]==noise];threshold=.001 if noise==0 else .02
                item={"n":n,"k":k,"stored_numbers":5*k,"noise":noise,"n_trials":len(group),"threshold":threshold,"arms":{},**pf}
                item["oracle_known_representation_relative"]=summary([
                    noise*g["generation"]["clean_norm_frobenius"]/g["arms"]["free"]["budget"][str(5*k)]["norm_frobenius"] for g in group],
                    [g["doc_id"] for g in group])
                item["oracle_truth_binary16_relative"]=summary([g["oracle_truth_code"]["fp16"]["relative"] for g in group],[g["doc_id"] for g in group])
                for arm in ("free","thin"):
                    values=[g["arms"][arm]["budget"][str(5*k)] for g in group];docs=[g["doc_id"] for g in group]
                    successes=sum(v["relative"]<=threshold for v in values)
                    item["arms"][arm]={"successes":successes,"success_rate":successes/len(group),"gate_pass":successes/len(group)>=.9,
                        "relative":summary([v["relative"] for v in values],docs),"absolute":summary([v["absolute"] for v in values],docs),
                        "max_relative":max(v["relative"] for v in values),"binary16_relative":summary([v["fp16"]["relative"] for v in values],docs),
                        "converged_fraction":float(np.mean([v["converged"] for v in values]))}
                planted.append(item)
        for spec in plan["masked_positive"]:
            if spec["n"]==n:
                row=read_json(ROOT/"masked_positive"/(spec["id"]+".json"));target,_=make(spec)
                oracle={"U":row["generation"]["latent_U"],"V":row["generation"]["latent_V"],"stored_numbers":2*n*spec["rank"]}
                row["oracle_truth_binary16_code"]=factor_precision(oracle,target,masked=True)
                row["oracle_note"]="Known latent factors, no fitted-code replacement; distinguishes representation precision from encoder failure"
                mr.append(row)
        mf=pair_file(f"out/pairs/phase19c_masked_positive_n{n}.jsonl",mr)
        for rank in (1,2,4,8,16):
            group=[r for r in mr if r["rank"]==rank];docs=[r["id"] for r in group];successes=sum(r["recovered"] for r in group)
            masked.append({"n":n,"rank":rank,"n_trials":len(group),"successes":successes,"success_rate":successes/len(group),
                "gate_pass":successes/len(group)>=.9,"threshold":1e-6,"relative":summary([r["fit"]["relative"] for r in group],docs),
                "max_relative":max(r["fit"]["relative"] for r in group),"max_oracle_error":max(r["oracle_exact_representation_error"]["relative"] for r in group),**mf})
            masked[-1]["fit_binary16_relative"]=summary([r["fit"]["fp16"]["relative"] for r in group],docs)
            masked[-1]["fit_binary16_failures"]=sum(r["fit"]["fp16"]["relative"] is None for r in group)
            masked[-1]["oracle_truth_binary16_relative"]=summary([r["oracle_truth_binary16_code"]["fp16"]["relative"] for r in group],docs)
    return negatives,planted,masked

def write_csv(path,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with Path(path).open("x",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)

def point_rows(datasets,category):
    for d in datasets:
        for B,p in d["budget"].items():
            yield {"category":category,"cohort":d.get("cohort",d.get("family")),"model":d.get("model","synthetic"),
                "n":d["n"],"rank":p["rank"],"budget":int(B)},p

def exports(result):
    effects=[];errors=[];precision=[]
    for datasets,category in ((result["attention_768"],"attention"),(result["attention_192"],"attention"),(result["negative_controls"],"negative_control")):
        for meta,p in point_rows(datasets,category):
            for stored in ("reference","binary16"):
                for name,t in p[stored]["paired"].items():
                    a,b=name.split("_minus_");s=t["paired_effect"];ci=s["ci95"] or [None,None]
                    effects.append({**meta,"precision":stored,"a":a,"b":b,"delta_definition":"e_a-e_b; negative favors a",
                        "n_instances":t["n_instances"],"n_documents_or_draws":t["n_documents"],"undefined_pairs":t["undefined_pairs"],
                        "paired_document_median_delta":s["median"],"paired_ci_low":ci[0],"paired_ci_high":ci[1],
                        "paired_q25":s["q25"],"paired_q75":s["q75"],"fraction_instances_a_wins":t["fraction_instances_a_wins"],
                        "fraction_instances_b_wins":t["fraction_instances_b_wins"],"fraction_ties":t["fraction_ties"],
                        "wilcoxon_p":t["wilcoxon_p"],"wilcoxon_p_holm":t.get("wilcoxon_p_holm"),
                        "holm_planned_family":t.get("holm_planned_family_size"),"a_numbers":p["costs"][a],"b_numbers":p["costs"][b]})
                for arm,v in p[stored]["methods"].items():
                    s=v["relative"];ci=s["ci95"] or [None,None]
                    errors.append({**meta,"precision":stored,"arm":arm,"n_instances":s["n_instances"],"undefined_count":s["undefined_count"],
                        "secondary_median_relative":s["median"],"secondary_ci_low":ci[0],"secondary_ci_high":ci[1],"q25":s["q25"],"q75":s["q75"],
                        "secondary_median_absolute":v["absolute"]["median"],"stored_numbers":p["costs"][arm]})
            for arm,v in p["precision_sensitivity"].items():
                s=v["quantized_minus_reference"]["paired_effect"];ci=s["ci95"] or [None,None]
                precision.append({**meta,"arm":arm,"numbers":v["stored_numbers"],"bits":v["stored_bits"],"codec_failures":v["codec_failures"],
                    "failure_fraction":v["failure_fraction"],"delta_binary16_minus_reference":s["median"],"ci_low":ci[0],"ci_high":ci[1],
                    "maximum_absolute_error_change":v["maximum_error_change"],"reference_median":p["reference"]["methods"][arm]["relative"]["median"],
                    "binary16_median":p["binary16"]["methods"][arm]["relative"]["median"]})
    write_csv("out/phase19c_effects.csv",effects)
    write_csv("out/phase19c_main_and_negative.csv",[r for r in effects if r["precision"]=="reference"])
    write_csv("out/phase19c_errors_secondary.csv",errors)
    write_csv("out/phase19c_precision.csv",precision)
    planted=[]
    for p in result["planted_controls"]:
        for arm,v in p["arms"].items():
            s=v["relative"];ci=s["ci95"]
            planted.append({"n":p["n"],"k":p["k"],"numbers":p["stored_numbers"],"noise":p["noise"],"arm":arm,
                "successes":v["successes"],"trials":p["n_trials"],"success_rate":v["success_rate"],"threshold":p["threshold"],"gate_pass":v["gate_pass"],
                "median_error":s["median"],"q25":s["q25"],"q75":s["q75"],"ci_low":ci[0],"ci_high":ci[1],"max_error":v["max_relative"],
                "binary16_median_error":v["binary16_relative"]["median"],"converged_fraction":v["converged_fraction"]})
            planted[-1]["oracle_known_representation_median_error"]=p["oracle_known_representation_relative"]["median"]
            planted[-1]["oracle_truth_binary16_median_error"]=p["oracle_truth_binary16_relative"]["median"]
    write_csv("out/phase19c_planted.csv",planted)
    write_csv("out/phase19c_masked_positive.csv",[{k:v for k,v in p.items() if k not in ("relative","pair_path","pair_sha256","fit_binary16_relative","oracle_truth_binary16_relative")}|
        {"median_error":p["relative"]["median"],"q25":p["relative"]["q25"],"q75":p["relative"]["q75"],
            "fit_binary16_median_error":p["fit_binary16_relative"]["median"],"oracle_truth_binary16_median_error":p["oracle_truth_binary16_relative"]["median"]} for p in result["masked_positive_controls"]])
    result["files"]={"paired_primary":"out/phase19c_main_and_negative.csv","all_effects_both_precisions":"out/phase19c_effects.csv",
        "secondary_errors":"out/phase19c_errors_secondary.csv","precision":"out/phase19c_precision.csv","planted":"out/phase19c_planted.csv",
        "masked_positive":"out/phase19c_masked_positive.csv"}

def aggregate():
    output=Path("out/phase19c_richlines.json")
    if output.exists():raise FileExistsError(output)
    from phase19c_experiment import status
    state=status()
    if not state["complete"] or state["errors"]:raise AssertionError(f"Incomplete or failed primary E2c jobs: {state}")
    protocol=read_json("out/phase19c_protocol_v2.json")
    result={"protocol":protocol,"statistics_primary":"paired document effects and instance win fractions; marginal medians explicitly secondary",
        "limitations":["Free768 uses241 original exported states and527 explicitly labelled replays; historical phase19 errors are retained separately, never substituted for the decoded state in precision analysis.",
            "The192 cohort is a fixed subset of768, not an independent replication; the larger budgets are reported separately.",
            "ALS and parametric fitting are finite nonconvex procedures. Failed exact-membership controls, numerical safeguards and nonconvergence do not establish lack of representational capacity.",
            "Random QK has no planted lines; causal normalization, accidental structure and geometric approximability are allowed. Uniform causal attention is an algebraic control, not an assertion that its image has no geometry.",
            "Binary16 directly quantizes the chosen parameterization/factor gauge, decodes in float64 and does not refit. It is not an optimal bit allocation or an impossibility result for other16-bit codecs.",
            "A=tril(UV^T) generally has full ordinary rank; masked rank denotes the latent factor rank. Both learned lines and masked low rank receive the causal mask without stored overhead.",
            "A suspended own CPU case may include the GPU handoff pause in execution elapsed time; iteration stopping never depends on elapsed time."],
        "numerical_validation":read_json("out/phase19c_numerical_validation.json"),
        "ALS_direct_design_validation":read_json("out/phase19c_qr_validation.json")}
    result["statistics_validation"]=read_json("out/phase19c_statistics_validation.json")
    result["attention_768"]=attention_cohort("out/phase19_selection.json","phase19_768")
    result["attention_192"]=attention_cohort("out/phase19b_selection.json","phase19b_192")
    result["negative_controls"],result["planted_controls"],result["masked_positive_controls"]=controls()
    reference=[];precision=[];negative=[]
    for _,p in point_rows(result["attention_768"]+result["attention_192"],"attention"):
        reference.extend(p["reference"]["paired"].values());precision.extend(p["binary16"]["paired"].values())
    holm(reference,576);holm(precision,576)
    for d in result["negative_controls"]:
        if d["family"]!="uniform_causal":
            for p in d["budget"].values():negative.extend(p["reference"]["paired"].values())
    holm(negative,72)
    result["all_masked_positive_gates_pass"]=all(p["gate_pass"] for p in result["masked_positive_controls"])
    result["all_planted_segment_gates_pass"]=all(v["gate_pass"] for p in result["planted_controls"] for v in p["arms"].values())
    result["paired_point_counts"]={}
    for name,cohort in (("768",result["attention_768"]),("192",result["attention_192"])):
        result["paired_point_counts"][name]={}
        for contrast in (a+"_minus_"+b for a,b in PAIRS):
            tests=[p["reference"]["paired"][contrast] for d in cohort for p in d["budget"].values()]
            result["paired_point_counts"][name][contrast]={"points":len(tests),
                "negative_paired_median":sum(t["paired_effect"]["median"]<0 for t in tests),
                "positive_paired_median":sum(t["paired_effect"]["median"]>0 for t in tests),
                "negative_and_Holm_significant":sum(t["paired_effect"]["median"]<0 and t["wilcoxon_p_holm"]<.05 for t in tests),
                "positive_and_Holm_significant":sum(t["paired_effect"]["median"]>0 and t["wilcoxon_p_holm"]<.05 for t in tests)}
    source_counts={};deltas=[];convergence={"masked":[],"thin768":[]};retries=[];rejected=[]
    for path in (ROOT/"baseline").glob("*.json"):
        row=read_json(path);src=row["free768_parameter_provenance"];source_counts[src]=source_counts.get(src,0)+1
        for B,v in row["free768"].items():deltas.append(v["relative"]-row["free_historical"][B]["relative"])
        for fit in row["masked"].values():
            diag=fit["diagnostics"];convergence["masked"].append(diag["converged"]);retries.append(diag["direct_sweep_retries"]);rejected.append(len(diag["numerically_rejected_sweeps"]))
    for path in (ROOT/"thin768").glob("*.json"):
        row=read_json(path);convergence["thin768"].extend(v["converged"] for v in row["budget"].values())
    result["free768_provenance_counts"]=source_counts
    result["current_minus_historical_free_relative_error"]={"median":float(np.median(deltas)),"median_absolute":float(np.median(np.abs(deltas))),"max_absolute":float(np.max(np.abs(deltas)))}
    result["convergence"]={a:{"fraction":float(np.mean(v)),"n_fits_or_budget_points":len(v)} for a,v in convergence.items()}
    result["ALS_numerical_safeguards"]={"fits_with_direct_retry":int(np.sum(np.asarray(retries)>0)),"fits_with_rejected_sweep":int(np.sum(np.asarray(rejected)>0)),
        "total_direct_retries":int(np.sum(retries)),"total_rejected_sweeps":int(np.sum(rejected)),"retained_per_fit_in_pairs":True}
    handoff=Path("out/phase19c_v2_gpu_resource_handoff_complete.json")
    result["resource_handoff"]={"gpu_used":handoff.exists(),"maximum_active_calculation_processes":3}
    if handoff.exists():result["resource_handoff"].update({"start":read_json("out/phase19c_v2_gpu_resource_handoff.json"),"finish":read_json(handoff)})
    exports(result)
    result["source_code_sha256"]={p.as_posix():digest(p) for p in sorted(Path('.').glob('phase19c_*.py'))}
    write_json(output,result);progress("PHASE19C primary paired report,30 pair files and6 CSV tables complete")
    return result

if __name__=="__main__":aggregate()
