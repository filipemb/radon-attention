"""Fixed controls for v2 aggregation, symmetric estimator and shared fallback."""
import phase21_allocation_v2 as e4
from phase21_allocation_v2_forward import SymmetricNamedFirst
import phase2_downstream as harness
import json
from pathlib import Path
import numpy as np
import torch
from sampling import load_sample,sha256_file


def main(output="out/phase21_allocation_v2_adapter_checks.json"):
    checks=[]
    for n in (128,256):
        dictionary=e4.v1.Dictionary(n)
        attention,_=load_sample("gpt2",n)
        cases=np.stack([attention[0],attention[-1]]).astype(np.float32)
        for dtype in (torch.float32,torch.bfloat16):
            original=torch.tensor(cases)[:,None].to(dtype)
            for K in (8,16):
                estimator=SymmetricNamedFirst(dictionary,harness,"uniform")
                estimator.rank_cap=K
                actual=estimator(original)
                differences=[]
                if dtype==torch.float32:
                    for i,A in enumerate(cases.astype(np.float64)):
                        S,c,_=dictionary.project(A)
                        reference=S+e4.v1.truncate(e4.v1.factor(A-S),K-1)
                        stats={}
                        expected=harness.normalize_reconstruction(torch.tensor(reference[None],dtype=torch.float32),original[i],stats,"uniform")[0]
                        difference=float(torch.linalg.norm(actual[i,0]-expected)/torch.linalg.norm(expected))
                        if difference>5e-5:raise AssertionError("V2 batched estimator differs from independent scalar reference")
                        differences.append(difference)
                if actual.dtype!=dtype:raise AssertionError("Model dtype not preserved")
                checks.append({"n":n,"model_dtype":str(dtype),"budget_rank_K":K,"residual_rank":K-1,
                               "float32_vs_float64_relative_errors":differences if differences else None,
                               "budget_accounting":estimator.document_costs,"validation":estimator.stats})
        original=torch.eye(n).repeat(2,1,1)
        stats={}
        filled=harness.normalize_reconstruction(torch.zeros_like(original),original,stats,"uniform")
        if not torch.allclose(filled[:,-1],torch.full((2,n),1/n),atol=1e-7,rtol=0):
            raise AssertionError("Empty final row was not filled uniformly")
        if stats["empty_rows_completed"]!=2*n or stats["empty_rows_completed_at_last_query"]!=2:
            raise AssertionError("Shared fallback counters wrong")
        checks.append({"n":n,"explicit_all_empty_control":True,"completion":harness.completion_summary(stats),
                       "original_row_values_not_used":bool(not torch.equal(filled,original))})
    # Known signed-rank direction and the required within-document median.
    rows=[{"document_index":d,"layer":0,"head":h} for d in range(64) for h in (0,1)]
    delta=np.tile(np.array([100.,-1.]),64)
    paired=e4.paired(delta,rows)
    if any(r["median_difference"]!=49.5 for r in paired["document_median_differences"]):
        raise AssertionError("Paired test did not use document median differences")
    if paired["wilcoxon"]["rank_biserial"]!=1 or paired["right_arm_win_fraction_instances"]!=0.5:
        raise AssertionError("Signed-rank effect direction or head-instance fraction wrong")
    e4.write_new(output,{
        "passed":True,"LM_forward_executed":False,"behavioral_KL_computed":False,"device":"CPU",
        "tests":checks,"signed_rank_control":paired,"imported_harness_sha256":sha256_file("phase2_downstream.py"),
        "primary_statistics_function":"Imported phase24_p0_metrics.describe, not reimplemented",
        "primary_source_sha256":sha256_file("phase24_p0_metrics.py")})
    e4.log("V2 CONTROLS PASSED: q=K-1, n128/256 fp32/bf16, shared uniform completion and counters, document-median signed-rank direction; no LM forward/KL")


def statistics_control():
    # A document mean is positive, while its median is negative; signed-rank
    # on all instances would also give a different effect. This distinguishes
    # the requested two-stage test from both common incorrect aggregations.
    rows=[{"document_index":d,"layer":0,"head":h} for d in range(64) for h in (0,1,2)]
    delta=np.tile(np.array([100.,-1.,-1.]),64)
    result=e4.paired(delta,rows)
    if any(row["median_difference"]!=-1 for row in result["document_median_differences"]):
        raise AssertionError("Document median was replaced by document mean")
    if result["wilcoxon"]["rank_biserial"]!=-1 or result["wilcoxon"]["n_documents"]!=64:
        raise AssertionError("Signed-rank did not operate on 64 negative document medians")
    primary=result["paired_instance_difference"]
    if primary["median"]!=-1 or primary["secondary_document_means"]["mean"]<=0:
        raise AssertionError("Instance median and secondary mean-of-means were confused")
    if not np.isclose(result["right_arm_win_fraction_instances"],1/3):
        raise AssertionError("Win fraction does not cover all 192 instances")
    e4.write_new("out/phase21_allocation_v2_statistics_checks.json",{
        "passed":True,"control":"64 documents x 3 instances, paired differences [100,-1,-1] per document",
        "expected_document_median":-1,"expected_secondary_document_mean":98/3,
        "expected_signed_rank_rank_biserial":-1,"result":result})
    e4.log("STATISTICS CONTROL PASSED: document medians negative despite positive document means; signed-rank has n64/rb=-1; instance median and secondary mean remain distinct")


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--statistics-only",action="store_true")
    parser.add_argument("--output",default="out/phase21_allocation_v2_adapter_checks.json")
    args=parser.parse_args()
    if args.statistics_only:statistics_control()
    else:main(args.output)
