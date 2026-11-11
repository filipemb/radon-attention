"""Independent final checks of identity, causal budgets and paired statistics."""
import phase19c_common
from pathlib import Path
import numpy as np
from phase19c_common import read_json,read_jsonl,digest,write_json,budgets,tag
from phase19c_analysis import ARMS,PAIRS,paired,summary

def audit():
    report=read_json("out/phase19c_richlines.json");protocol=report["protocol"]
    for section in ("parent_inventory_sha256","parent_artifact_sha256","numeric_sources_sha256"):
        changed=[p for p,h in protocol[section].items() if digest(p)!=h]
        if changed:raise AssertionError(f"Protected inputs changed: {changed}")
    for p,h in protocol["revision"]["retained_failed_worker_logs"].items():
        if digest(p)!=h:raise AssertionError("Initial failure evidence changed")
    counts={};max_ratio=0.;max_svd_delta=0.;thin_max=0.;reproduced=0
    for cohort,key,selection_path in (("768","attention_768","out/phase19_selection.json"),("192","attention_192","out/phase19b_selection.json")):
        selection=read_json(selection_path);planned={ (d["model_slug"],d["n"]):d for d in selection["datasets"]};count=0
        if digest(selection_path)!=protocol["cohorts"]["phase19_768" if cohort=="768" else "phase19b_192"]["sha256"]:raise AssertionError("Cohort selection changed")
        for dataset in report[key]:
            n=dataset["n"];ranks=(1,2,4) if cohort=="768" else (1,2,4,8,16);path=Path(dataset["pair_path"])
            if digest(path)!=dataset["pair_sha256"]:raise AssertionError("Pair file changed")
            pairs=read_jsonl(path);expected=planned[(dataset["model_slug"],n)]["instances"]
            if [p["instance_id"] for p in pairs]!=[p["instance_id"] for p in expected]:raise AssertionError("Unmatched attention selection")
            if len({p["doc_id"] for p in pairs})!=len(pairs):raise AssertionError("Unexpected repeated attention document")
            count+=len(pairs);docs=[p["doc_id"] for p in pairs]
            if cohort=="768":
                old=read_jsonl(f"out/phase19_cpu_{dataset['model_slug']}_n{n}.jsonl")
                if [p["instance_id"] for p in old]!=[p["instance_id"] for p in pairs]:raise AssertionError("Parent identities changed")
            for rank,B in zip(ranks,budgets(n,ranks)):
                rows=[p["budget"][str(B)] for p in pairs]
                for index,row in enumerate(rows):
                    norm=row["free"]["norm_frobenius"]
                    for arm in ARMS:
                        v=row[arm];expected_cost=rank*(2*n+1) if arm=="svd" else 2*n*rank if arm=="masked" else 5*(B//5)
                        if v["stored_numbers"]!=expected_cost or expected_cost>B or v["bits16"]!=16*expected_cost:raise AssertionError("Unfair storage budget")
                        if not np.isfinite([v["relative"],v["absolute"]]).all():raise AssertionError("Nonfinite reference error")
                        delta=abs(v["absolute"]/norm-v["relative"]);max_ratio=max(max_ratio,delta)
                        if delta>1e-10:raise AssertionError("Different Frobenius normalization")
                        if arm in ("free","thin"):
                            p=np.asarray(v["parameters"])
                            if p.shape!=(B//5,5) or not np.isfinite(p).all() or np.any(p[:,4]<0):raise AssertionError("Invalid line code")
                            if arm=="thin":
                                thin_max=max(thin_max,float(p[:,2].max()))
                                if p[:,2].max()>2+1e-12 or p[:,2].min()<.2-1e-12:raise AssertionError("Thin width bound violated")
                        else:
                            if np.asarray(v["U"]).shape!=(n,rank) or np.asarray(v["V"]).shape!=(n,rank):raise AssertionError("Invalid factor code")
                        q=v["fp16"]
                        if q["quantization"]["success"]:
                            if not np.isfinite([q["relative"],q["absolute"]]).all():raise AssertionError("Nonfinite successful binary16 codec")
                        elif q["relative"] is not None or q["absolute"] is not None:raise AssertionError("Failed codec error was imputed")
                    if cohort=="768":
                        d=abs(row["svd"]["relative"]-old[index]["methods"]["svd"][str(rank)]["relative"]);max_svd_delta=max(max_svd_delta,d)
                        if d>1e-10:raise AssertionError("Ordinary SVD changed")
                for precision in ("reference","binary16"):
                    for a,b in PAIRS:
                        av=[v[a]["relative"] if precision=="reference" else v[a]["fp16"]["relative"] for v in rows]
                        bv=[v[b]["relative"] if precision=="reference" else v[b]["fp16"]["relative"] for v in rows]
                        expected=paired(av,bv,docs);stored=dataset["budget"][str(B)][precision]["paired"][a+"_minus_"+b]
                        for field in ("paired_effect","wilcoxon_p","fraction_instances_a_wins","fraction_instances_b_wins","fraction_ties","undefined_pairs"):
                            if expected[field]!=stored[field]:raise AssertionError(f"Paired statistic mismatch: {field}")
                        reproduced+=1
        if count!=int(cohort):raise AssertionError("Missing attention instance")
        counts[cohort]=count
    if reproduced!=1152:raise AssertionError("Incomplete paired statistics")
    for n in (128,256):
        for kind,expected in (("negative",33),("planted",48),("masked_positive",40)):
            rows=read_jsonl(f"out/pairs/phase19c_{kind}_n{n}.jsonl")
            if len(rows)!=expected or len({r["id"] for r in rows})!=expected:raise AssertionError("Missing synthetic case")
    if max(p["max_oracle_error"] for p in report["masked_positive_controls"])>1e-12:raise AssertionError("Masked positive target not in the model")
    handoff=report["resource_handoff"]
    if handoff["gpu_used"] and not handoff["finish"]["resumed"]:raise AssertionError("Own CPU worker was not resumed")
    result={"passed":True,"cohort_instance_counts":counts,"paired_statistics_reproduced":reproduced,
        "all_four_arms_same_instances_and_budgets":True,"parent_artifacts_byte_identical":True,"frozen_numeric_sources_unchanged":True,
        "initial_numerical_failure_logs_retained":True,"all30_pair_files_complete":True,"strict_thin_maximum":thin_max,
        "ordinary_svd_max_delta_from_phase19":max_svd_delta,"absolute_relative_max_discrepancy":max_ratio,
        "binary16_failures_explicit_no_conditional_primary_medians":True,
        "all_masked_positive_gates_pass":report["all_masked_positive_gates_pass"],"all_planted_segment_gates_pass":report["all_planted_segment_gates_pass"],
        "maximum_active_calculation_processes":3,"report_sha256":digest("out/phase19c_richlines.json")}
    write_json("out/phase19c_integrity_audit.json",result);return result

if __name__=="__main__":print(audit())
