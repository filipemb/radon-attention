"""Validate paired E2 output identities, finite metrics, storage and aggregates."""
import json
from pathlib import Path
import numpy as np
from richlines_core import COMPONENTS,block_summary,digest,grids,write_json


def audit(write=True):
    path=Path("out/phase19_richlines.json")
    report=json.loads(path.read_text(encoding="utf-8"))
    selection=report["protocol"]["selection"]
    records={(r["model_slug"],r["n"]):r for r in selection["datasets"]}
    if len(records)!=12 or len(report["datasets"])!=12:
        raise AssertionError("Expected all six models and both n values")
    total=0;max_ratio_error=0.0;max_median_error=0.0
    methods={"uniform","profiled","radon","parametric","svd","fbp"}
    for dataset in report["datasets"]:
        n=dataset["n"];record=records[(dataset["model_slug"],n)]
        pairs_path=Path(dataset["pair_path"])
        if digest(pairs_path)!=dataset["pair_sha256"]:
            raise AssertionError(f"Pair checksum mismatch: {pairs_path}")
        pairs=[json.loads(line) for line in pairs_path.read_text(encoding="utf-8").splitlines()]
        if [r["instance_id"] for r in pairs]!=[r["instance_id"] for r in record["instances"]]:
            raise AssertionError("Paired identities do not equal the fixed selection")
        if len({r["doc_id"] for r in pairs})!=64:
            raise AssertionError("A selected document is missing")
        total+=len(pairs)
        for comparison,grid in [("budget",grids(n)),("same_components",COMPONENTS)]:
            for value in grid:
                for method in methods:
                    values=[]
                    for pair in pairs:
                        row=pair[comparison][str(value)]
                        if set(row)!=methods:raise AssertionError("Unmatched methods")
                        error=row[method]
                        a,r=error["absolute"],error["relative"]
                        if not np.isfinite([a,r]).all() or min(a,r)<0:
                            raise AssertionError("Nonfinite or negative reconstruction error")
                        discrepancy=abs(a/pair["norm_frobenius"]-r)
                        max_ratio_error=max(max_ratio_error,discrepancy)
                        if discrepancy>1e-7:raise AssertionError("Absolute and relative metrics disagree")
                        cost=2*n+1 if method=="svd" else {"uniform":2,"profiled":3,"radon":2,"parametric":5,"fbp":2}[method]
                        expected=value//cost if comparison=="budget" else value
                        if error["components"]!=expected or error["stored_numbers"]!=expected*cost:
                            raise AssertionError("Storage count mismatch")
                        if comparison=="budget" and error["stored_numbers"]>value:
                            raise AssertionError("Storage budget exceeded")
                        values.append(r)
                    summary=dataset[comparison][method][str(value)]["relative"]
                    delta=abs(float(np.median(values))-summary["median"])
                    max_median_error=max(max_median_error,delta)
                    if delta>1e-12 or summary["n_instances"]!=len(pairs) or summary["n_documents"]!=64:
                        raise AssertionError("Aggregate is not over all paired instances")
                    q1,q3=np.quantile(values,[0.25,0.75])
                    if abs((q3-q1)-summary["iqr"])>1e-12:
                        raise AssertionError("IQR mismatch")
        # Independent recomputation of an entire document-block bootstrap point.
        value=str(grids(n)[0]);values=[p["budget"][value]["parametric"]["relative"] for p in pairs]
        recomputed=block_summary(values,[p["doc_id"] for p in pairs])
        if recomputed!=dataset["budget"]["parametric"][value]["relative"]:
            raise AssertionError("Document-block bootstrap does not reproduce")
    frozen=report["protocol"]["optimizer_frozen"]
    if digest("out/phase19_selection.json")!=frozen["selection_sha256"]:
        raise AssertionError("Selection changed after the optimizer freeze")
    if not all(digest(p)==expected for p,expected in frozen["source_sha256"].items()):
        raise AssertionError("Numerical sources changed after freeze")
    backend=report["protocol"].get("cpu_backend_protocol")
    if backend and not all(digest(p)==expected for p,expected in backend["source_sha256"].items()):
        raise AssertionError("CPU backend or handoff sources changed after their freeze")
    recurrence=report["protocol"].get("cpu_recurrence_protocol")
    if recurrence and not all(digest(p)==expected for p,expected in recurrence["source_sha256"].items()):
        raise AssertionError("Exact-recurrence CPU sources changed after their freeze")
    result={"passed":True,"report_sha256":digest(path),"datasets":12,"instances":total,
        "all_methods_same_instances":True,"finite_nonnegative_errors":True,"storage_budgets_verified":True,
        "absolute_relative_max_discrepancy":max_ratio_error,"median_max_discrepancy":max_median_error,
        "document_block_bootstrap_reproduced":True,"numerical_sources_match_frozen_hashes":True,
        "selection_matches_frozen_hash":True,
        "parametric_backend_counts":report["protocol"].get("parametric_backend_counts"),
        "positive_control_gates_pass":report["all_positive_control_gates_pass"],
        "note":"Integrity checks and positive-control recovery gates are separate; failed controls remain in the report."}
    if write:
        destination=Path("out/phase19_integrity_audit.json")
        if destination.exists():
            if json.loads(destination.read_text())!=result:
                raise ValueError("Existing audit differs from current output")
        else:write_json(destination,result)
    return result


if __name__=="__main__":print(json.dumps(audit(),indent=2))
