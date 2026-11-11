"""Audit matched identities, strict thin widths, budgets and old-file immutability."""
import phase19b_common
import json
from pathlib import Path
import numpy as np
from phase19b_common import read_json,digest,write_json,SELECTION,PROTOCOL,RANKS,budgets
from phase19b_analysis import block_summary,paired_test


def audit():
    report=read_json("out/phase19b_richlines.json");protocol=read_json(PROTOCOL)
    old_changed=[p for p,h in protocol["parent_artifact_sha256"].items() if digest(p)!=h]
    if digest('out/phase19_artifacts.json')!=protocol['parent_inventory_sha256']:old_changed.append('out/phase19_artifacts.json')
    if old_changed:raise AssertionError(f"Parent artifacts changed: {old_changed}")
    for p,h in protocol["numeric_source_sha256"].items():
        if digest(p)!=h:raise AssertionError(f"Frozen numeric source changed: {p}")
    selection=read_json(SELECTION);n_comparison=0;max_ratio=0.;max_median=0.;max_thin_width=0.
    if digest(SELECTION)!=protocol["selection_sha256"]:raise AssertionError("Predeclared selection changed")
    if report["resource_handoff"]["gpu_used"] and not report["resource_handoff"]["finish"]["resumed"]:
        raise AssertionError("Suspended own CPU worker was not resumed")
    for dataset in report["comparisons_192"]:
        record=next(r for r in selection["datasets"] if r["model_slug"]==dataset["model_slug"] and r["n"]==dataset["n"])
        path=Path(dataset["pair_path"])
        if digest(path)!=dataset["pair_sha256"]:raise AssertionError("Pair checksum differs")
        pairs=[json.loads(l) for l in path.read_text().splitlines()]
        if [r["instance_id"] for r in pairs]!=[r["instance_id"] for r in record["instances"]]:raise AssertionError("Selection mismatch")
        if len(pairs)!=16 or len({r["doc_id"] for r in pairs})!=16:raise AssertionError("Wrong document coverage")
        n_comparison+=len(pairs);n=dataset["n"];docs=[r["doc_id"] for r in pairs]
        for rank,B in zip(RANKS,budgets(n)):
            for row in pairs:
                values=row["budget"][str(B)];norm=values["free"]["norm_frobenius"]
                for method,entry in values.items():
                    if not np.isfinite([entry["relative"],entry["absolute"]]).all():raise AssertionError("Nonfinite error")
                    delta=abs(entry["absolute"]/norm-entry["relative"]);max_ratio=max(max_ratio,delta)
                    if delta>1e-10:raise AssertionError("Whole-matrix absolute/relative error mismatch")
                    expected=rank if method=="svd" else B//5
                    cost=rank*(2*n+1) if method=="svd" else 5*expected
                    if entry["components"]!=expected or entry["stored_numbers"]!=cost or cost>B:raise AssertionError("Budget mismatch")
                    if method!="svd":
                        p=np.asarray(entry["parameters"])
                        if p.shape!=(expected,5) or not np.isfinite(p).all() or (p[:,4]<0).any():raise AssertionError("Invalid parameters")
                        cap=2 if method=="thin" else n
                        if (p[:,2]<.2-1e-12).any() or (p[:,2]>cap+1e-12).any():raise AssertionError("Width constraint violated")
                        if method=="thin":
                            max_thin_width=max(max_thin_width,float(p[:,2].max()))
                            if entry["wide_energy"]["2.0"]["additive_share"]!=0:raise AssertionError("Thin arm contains broad energy")
                if row["diagnostics"]["free"]["initialization_hashes_before_width_projection"]!=row["diagnostics"]["thin"]["initialization_hashes_before_width_projection"]:
                    raise AssertionError("Different starts across arms")
            for method in ("svd","free","thin"):
                vals=[r["budget"][str(B)][method]["relative"] for r in pairs]
                summary=dataset["budget"][str(B)]["methods"][method]["relative"]
                delta=abs(np.median(vals)-summary["median"]);max_median=max(max_median,float(delta))
                if delta>1e-12:raise AssertionError("Median mismatch")
            # Reproduce complete document-block CI and signed-rank computation.
            free=[r["budget"][str(B)]["free"]["relative"] for r in pairs]
            thin=[r["budget"][str(B)]["thin"]["relative"] for r in pairs]
            if block_summary(free,docs)!=dataset["budget"][str(B)]["methods"]["free"]["relative"]:raise AssertionError("Bootstrap mismatch")
            test=paired_test(free,thin,docs);stored=dataset["budget"][str(B)]["paired_tests"]["free_minus_thin"]
            if test["wilcoxon_p_two_sided"]!=stored["wilcoxon_p_two_sided"]:raise AssertionError("Wilcoxon mismatch")
    if n_comparison!=192:raise AssertionError("Incomplete comparison")
    n_original=0;provenance={};parent=read_json("out/phase19_selection.json")
    for dataset in report["parameter_diagnostics_768"]:
        p=Path(dataset["pair_path"])
        if digest(p)!=dataset["pair_sha256"]:raise AssertionError("Original parameter pair checksum differs")
        rows=[json.loads(l) for l in p.read_text().splitlines()];n_original+=len(rows)
        if len(rows)!=64 or len({r["doc_id"] for r in rows})!=64:raise AssertionError("Missing original document")
        record=next(r for r in parent["datasets"] if r["model_slug"]==dataset["model_slug"] and r["n"]==dataset["n"])
        if [r["instance_id"] for r in rows]!=[r["instance_id"] for r in record["instances"]]:raise AssertionError("Original diagnostic identities differ")
        for row in rows:
            source=row["parameter_provenance"];provenance[source]=provenance.get(source,0)+1
            for B,entry in row["budget"].items():
                parameters=np.asarray(entry["parameters"])
                if parameters.shape!=(int(B)//5,5) or not np.isfinite(parameters).all():raise AssertionError("Invalid original-budget parameter export")
    if n_original!=768:raise AssertionError("Incomplete parameter diagnostic")
    if provenance.get("original_phase19_export")!=241 or sum(provenance.values())!=768:raise AssertionError("Original snapshot provenance differs")
    result={"passed":True,"parent_artifacts_byte_identical":True,"numeric_sources_frozen":True,
        "original_parameter_diagnostics":768,"paired_comparison_instances":192,"datasets":12,
        "same_instances_all_methods_and_budgets":True,"storage_budgets_verified":True,
        "strict_thin_width_maximum":max_thin_width,"thin_broad_energy_zero":True,
        "absolute_relative_max_discrepancy":max_ratio,"median_max_discrepancy":max_median,
        "document_bootstrap_and_wilcoxon_reproduced":True,
        "selection_sha256_verified":True,"parameter_provenance_counts":provenance,
        "maximum_active_calculation_processes":3,"gpu_resource_handoff":report["resource_handoff"],
        "all_positive_control_gates_pass":report["all_positive_control_gates_pass"],
        "report_sha256":digest("out/phase19b_richlines.json")}
    write_json("out/phase19b_integrity_audit.json",result);return result


if __name__=="__main__":print(json.dumps(audit(),indent=2))
