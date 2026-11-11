"""E9 integrity checks on complete, immutable outputs (no independent audit claim)."""
import phase50_als
import math
from pathlib import Path
from phase50_experiment import read,jsonl,PROTOCOL,ARMS
from sampling import MODELS,slug,sha256_file,write_json_new


def finite_tree(value,path="root"):
    if isinstance(value,float) and not math.isfinite(value): raise ValueError(f"Nonfinite output at {path}")
    if isinstance(value,dict):
        for key,item in value.items(): finite_tree(item,path+"."+str(key))
    if isinstance(value,list):
        for i,item in enumerate(value): finite_tree(item,path+f"[{i}]")


def main():
    protocol=read(PROTOCOL); ph=sha256_file(PROTOCOL)
    if sha256_file("phase2_downstream.py")!=protocol["harness_sha256_at_freeze"]: raise ValueError("Harness changed")
    for path,expected in protocol["source_files"].items():
        if sha256_file(path)!=expected: raise ValueError(f"Immutable input changed {path}")
    counts={}; max_delta=0.
    for model in MODELS:
        dataset=protocol["datasets"][model]
        if (sha256_file(f"data/attn/{slug(model)}_n128.npz")!=dataset["archive_sha256"]
                or sha256_file(f"data/attn/{slug(model)}_n128.manifest.json")!=dataset["manifest_sha256"]):
            raise ValueError("Archived matrices or sampling manifest changed after the frozen selection")
        matrix=jsonl(f"out/pairs/phase50_matrix_{slug(model)}.jsonl")
        if len(matrix)!=768: raise ValueError("Incomplete matrix study")
        chosen=set(protocol["datasets"][model]["matrix_archive_indices"])
        for k in (8,16):
            rows=[r for r in matrix if r["K"]==k]
            if {r["archive_index"] for r in rows}!=chosen: raise ValueError("Changed matrix subset")
            for row in rows:
                if row["protocol_sha256"]!=ph: raise ValueError("Mixed matrix protocols")
                if row["masked_parameters"]>row["cap"] or row["named_masked_parameters"]>row["cap"]: raise ValueError("Budget mismatch")
                for arm in ("masked_K","named_plus_masked"):
                    info=row["arms"][arm]["ALS"]
                    if info["sweeps"]!=200 or info["history"][-1]["sweep"]!=200: raise ValueError("Changed sweep count")
                max_delta=max(max_delta,max(row["E4_raw_reconstruction_differences"].values()))
        reused=read(f"out/phase50_reused_{slug(model)}.json")
        forward=read(f"out/phase50_forward_{slug(model)}.json")
        for meta in (reused,forward):
            if sha256_file(meta["pairs_path"])!=meta["pairs_sha256"]: raise ValueError("Raw output changed")
        records=jsonl(reused["pairs_path"])+jsonl(forward["pairs_path"])
        for row in records:
            finite_tree(row)
            if row["protocol_sha256"]!=ph or row["empty_row_policy"]!="uniform": raise ValueError("Forward protocol mismatch")
            if row.get("identity_KL",0)!=0: raise ValueError("Identity not exactlyzero")
            if not row.get("reused_exact",False) and row.get("fit_policy_sha256")!=sha256_file("out/phase50_numerical_fallback.json"):
                raise ValueError("Mixed forward numerical correction policies")
        for k in (8,16):
            for arm in ARMS:
                source=forward["aliases"].get(arm,arm)
                group=[r for r in records if r["K"]==k and r["arm"]==source]
                if sorted(r["document_index"] for r in group)!=list(range(256)): raise ValueError("Incomplete paired articles")
        counts[model]={"matrix_records":len(matrix),"forward_records_including_reused":len(records)}
    for path in ("out/phase50_matrix_summary.json","out/phase50_forward_summary.json","out/phase50_report.json"):
        finite_tree(read(path))
    result={"passed":True,"protocol_sha256":ph,"counts":counts,"max_E4_matrix_raw_difference":max_delta,
            "harness_unchanged":True,"immutable_inputs_unchanged":True,"all_fixed_matrix_subsets_complete":True,
            "all_six_arms_all256_articles_both_ranks":True,"all_written_numbers_finite":True,
            "independent_other_model_family_audit":False,"paper_or_git_actions_by_this_experiment":False}
    write_json_new("out/phase50_integrity_audit.json",result)
    print("E9 integrity checks passed; this is a self-audit, not an independent-family review",flush=True)


if __name__=="__main__": main()
