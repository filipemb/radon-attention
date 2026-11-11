"""Independent read-only audit of V1 and corrected beta=0 ledgers."""
from sampling import MODELS, CORPUS_PATH, slug, sha256_file, write_json_new, progress
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np

def audit(include_beta0=True):
    corpus=json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    corpus_sha=sha256_file(CORPUS_PATH)
    documents=[d["doc_id"] for d in corpus["documents"]]
    p2=json.loads(Path("out/phase2_downstream_v2.json").read_text(encoding="utf-8"))
    p7=json.loads(Path("out/phase7_editability_v2.json").read_text(encoding="utf-8"))
    report={"all_passed":False,"models":{},"beta0_models":{},"missing_data":[]}
    for name in MODELS:
        r2,r7=p2[name],p7[name]
        assert r2["pairs_path"]==r7["pairs_path"]
        rows=[json.loads(s) for s in Path(r2["pairs_path"]).read_text(encoding="utf-8").splitlines()]
        driver=r2.get("svd_implementation",{}).get("selected_driver")
        assert all(r.get("svd_driver")==driver for r in rows)
        parallel=r2.get("svd_implementation",{}).get("parallel_schedule",{})
        selected_parallel=parallel.get("selected",False)
        assert all(r.get("svd_parallel_schedule",False)==selected_parallel for r in rows)
        if selected_parallel:
            assert parallel["all_candidate_logits_bit_equal"] and parallel["n_arms"]==15
        if "svd_implementation" not in r2:
            assert name=="gpt2" and Path("out/phase2_execution_gpt2_v2.json").exists()
        assert len(rows)==15*256 and len({(r["arm"],r["doc_id"]) for r in rows})==len(rows)
        expected_last=256*corpus["models"][name]["n_layers"]*corpus["models"][name]["n_heads"]
        arms={}
        for root in (r2,r7):
            assert root["n_documents_effective"]==256 and root["target_excluded_from_model_input"]
            assert root["corpus_manifest_sha256"]==corpus_sha and root["empty_row_policy"]=="uniform"
            assert root["identity_kl_exactly_zero"]
            if "validation_schedule_equivalence" in root:
                assert root["validation_schedule_equivalence"]["all_passed"]
            assert all(x["passed_exact"] and x["max_logit_difference"]==0
                       for x in root["suffix_invariance"]["arms"].values())
            for arm,summary in root["arms"].items():
                selected=sorted((r for r in rows if r["arm"]==arm),key=lambda r:r["document_index"])
                assert [r["doc_id"] for r in selected]==documents
                assert all(r["target_id"]==corpus["models"][name]["documents"][i]["token_ids"][128]
                           for i,r in enumerate(selected))
                assert all(r["prefix_length"]==128 and r["empty_row_policy"]=="uniform" for r in selected)
                assert all(math.isfinite(r[k]) for r in selected for k in ("kl","nll","reference_nll"))
                assert np.isclose(np.mean([r["kl"] for r in selected]),summary["mean_kl"],rtol=0,atol=1e-12)
                assert np.isclose(np.median([r["kl"] for r in selected]),summary["median_kl"],rtol=0,atol=1e-12)
                assert np.isclose(np.mean([r["nll"] for r in selected]),summary["mean_nll"],rtol=0,atol=1e-12)
                counts={};seen=set()
                for row in selected:
                    key=(row["evaluation_batch_start"],row["evaluation_batch_size"])
                    if key in seen:continue
                    seen.add(key)
                    stats=row["attention_validation_batch"]
                    assert stats["negative_nan_inf_upper_nonzero"]==0
                    for key in ("row_sum_violations","reconstruction_nonfinite_values","reconstruction_invalid_denominators",
                                "sink_edit_invalid_values","sink_edit_invalid_totals","sink_edit_noncausal_values",
                                "sink_edit_row_sum_violations","sink_edit_first_row_changes"):
                        assert stats.get(key,0)==0
                    assert stats["max_row_error_after_cast"]<=root["cast_row_atol"]
                    if "max_row_error_before_cast" in stats:
                        assert stats["max_row_error_before_cast"]<=root["normalized_fp32_row_atol"]
                    for k in ("reconstruction_rows_total","last_query_rows_total","empty_rows_completed",
                              "empty_rows_completed_at_last_query","sink_edit_rows_preserved_no_alternative",
                              "sink_edit_last_query_rows_preserved"):
                        counts[k]=counts.get(k,0)+stats.get(k,0)
                c=summary["uniform_completion"]
                assert c["rows_total"]==counts["reconstruction_rows_total"]==128*expected_last
                assert c["last_query_rows_total"]==counts["last_query_rows_total"]==expected_last
                assert c["rows_completed"]==counts["empty_rows_completed"]
                assert c["last_query_rows_completed"]==counts["empty_rows_completed_at_last_query"]
                assert c["fraction_rows_completed"]==c["rows_completed"]/c["rows_total"]
                assert c["fraction_last_query_rows_completed"]==c["last_query_rows_completed"]/expected_last
                if ":identity" in arm:assert all(r["kl"]==0 for r in selected)
                if arm=="phase7:nosink:8":
                    assert counts["sink_edit_rows_preserved_no_alternative"]>=expected_last
                arms[arm]={"n_documents":256,"mean_kl":summary["mean_kl"],"median_kl":summary["median_kl"],
                           "mean_nll":summary["mean_nll"],"uniform_completion":c,
                           "preserved_edit_rows":counts["sink_edit_rows_preserved_no_alternative"],
                           "preserved_edit_last_query_rows":counts["sink_edit_last_query_rows_preserved"]}
        report["models"][name]={"n_raw_records":len(rows),"all_arms_same_documents":True,
                                "suffix_checks_passed":True,"svd_driver":driver,"arms":arms}
    report["v1_all_passed"]=True
    if not include_beta0:
        report["beta0_status"]="Not audited yet; all_passed remains false until the full audit"
        return report
    beta=json.loads(Path("out/phase8_beta0_v2.json").read_text(encoding="utf-8"))
    assert beta["_meta"]["positive_beta_regression"]["logits_bit_equal"]
    assert beta["_meta"]["positive_beta_regression"]["max_absolute_logit_difference"]==0
    for name in MODELS[:5]:
        result=beta[name]
        assert result["native_identity_regression"]["logits_bit_equal"]
        rows=[json.loads(s) for s in Path(result["pairs_path"]).read_text(encoding="utf-8").splitlines()]
        assert len(rows)==3*3200 and len({(r["arm"],r["trial_id"]) for r in rows})==len(rows)
        assert result["n_trials_effective_per_arm"]==3200
        arms={}
        for arm,summary in result["arms"].items():
            selected=sorted((r for r in rows if r["arm"]==arm),key=lambda r:r["trial_id"])
            assert [r["trial_id"] for r in selected]==list(range(3200))
            assert sum(r["correct"] for r in selected)==summary["n_correct"]
            assert sum(r["correct"] for r in selected)/3200==summary["accuracy"]
            middle=[r for r in selected if 32<=r["position"]<=96]
            assert len(middle)==2000 and sum(r["correct"] for r in middle)==summary["middle_n_correct"]
            arms[arm]=summary
        targets={}
        for row in rows:
            targets.setdefault(row["trial_id"],set()).add(row["target_id"])
        assert len(targets)==3200 and all(len(values)==1 for values in targets.values())
        r=arms["corrected_beta0"]["accuracy"];base=arms["baseline_beta1"]["accuracy"]
        report["beta0_models"][name]={"n_raw_records":len(rows),"n_trials_per_arm":3200,
            "arms":arms,"corrected_minus_baseline_accuracy":r-base,
            "relative_loss_vs_baseline":1-r/base if base else None,
            "attention_validation":result["attention_validation"]}
    assert json.loads(Path("out/phase29_sink_checks_v2.json").read_text(encoding="utf-8"))["all_passed"]
    assert json.loads(Path("out/phase33_validation_schedule_checks_v2.json").read_text(encoding="utf-8"))["all_passed"]
    assert json.loads(Path("out/phase33_legacy_counter_checks_v2.json").read_text(encoding="utf-8"))["all_passed"]
    retrieval=json.loads(Path("out/phase25_retrieval_completion_v2.json").read_text(encoding="utf-8"))
    assert not retrieval["target_leakage_found"] and retrieval["beta0_editing_repair"]["first_row_unchanged"]
    report["missing_data"].append("Original phase2/phase7 outputs did not record effective article counts; historical and revised KL use different corpus/evaluation protocols.")
    report["outside_requested_rerun_scope"]={"phase18_CV":"Old beta0 was selected on family B for Pythia-1.4b in all three saved seeds. The shared code is fixed, but saved CV results are not revalidated by this phase8-only beta0 rerun.",
                                            "evidence":"out/phase18_beta0_dependency_audit_v2.json"}
    report["all_passed"]=True
    return report

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out")
    ap.add_argument("--v1-only",action="store_true",help="Reconcile all V1 ledgers; never mark the full delivery complete")
    args=ap.parse_args();start=time.perf_counter()
    result=audit(include_beta0=not args.v1_only);result["elapsed_seconds"]=time.perf_counter()-start
    output=args.out or ("out/phase30_validity_v1_checks_v2.json" if args.v1_only else "out/phase30_validity_audit_v2.json")
    write_json_new(output,result)
    message=("All V1 raw records reconciled; beta0 and full-delivery audit remain pending" if args.v1_only else
             "All V1 arms and beta0 trials reconciled to raw ledgers; completion denominators, identity, masks, sums and paired populations passed")
    command=".venv/Scripts/python.exe -B phase30_validity_audit.py"+(" --v1-only" if args.v1_only else "")
    progress("V1 raw validity audit" if args.v1_only else "V1 final validity audit",message,result["elapsed_seconds"],command)
    print(f"{'V1' if args.v1_only else 'Full'} validity audit passed in {result['elapsed_seconds']:.3f}s",flush=True)

if __name__=="__main__":main()
