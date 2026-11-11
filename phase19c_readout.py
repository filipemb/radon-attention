"""Wide review tables from the immutable audited primary report."""
import phase19c_common
from pathlib import Path
from phase19c_common import read_json,write_json,digest
from phase19c_analysis import write_csv

def effect_fields(point):
    out={}
    for arm in ("svd","free","thin"):
        t=point["reference"]["paired"][arm+"_minus_masked"];s=t["paired_effect"];ci=s["ci95"] or [None,None]
        out.update({arm+"_minus_masked_delta":s["median"],arm+"_ci_low":ci[0],arm+"_ci_high":ci[1],
            arm+"_win_fraction":t["fraction_instances_a_wins"],arm+"_wilcoxon_p":t["wilcoxon_p"],
            arm+"_p_holm":t.get("wilcoxon_p_holm")})
    return out

def main():
    report=read_json("out/phase19c_richlines.json");audit=read_json("out/phase19c_integrity_audit.json")
    if not audit["passed"] or digest("out/phase19c_richlines.json")!=audit["report_sha256"]:raise AssertionError("Audited report required")
    paths=[Path(f"out/phase19c_table1_3_paired_{n}.csv") for n in (768,192)]
    paths.extend(Path(f"out/phase19c_table5_precision_{n}.csv") for n in (768,192))
    paths.extend([Path("out/phase19c_table2_negative.csv"),Path("out/phase19c_table4_planted.csv"),Path("out/phase19c_readout.json")])
    if any(p.exists() for p in paths):raise FileExistsError("A wide readout table already exists")
    precision_summary=[]
    for cohort,key in ((768,"attention_768"),(192,"attention_192")):
        rows=[];precision=[];perarm={a:[] for a in ("svd","masked","free","thin")}
        for d in report[key]:
            for B,p in d["budget"].items():
                meta={"cohort":cohort,"model":d["model"],"n":d["n"],"rank":p["rank"],"budget":int(B),"n_documents":d["n_documents"]}
                rows.append({**meta,**effect_fields(p)})
                q=meta.copy()
                for arm in perarm:
                    v=p["precision_sensitivity"][arm];perarm[arm].append(v);s=v["quantized_minus_reference"]["paired_effect"];ci=s["ci95"] or [None,None]
                    q.update({arm+"_delta_binary16_minus_reference":s["median"],arm+"_ci_low":ci[0],arm+"_ci_high":ci[1],
                        arm+"_codec_failures":v["codec_failures"],arm+"_numbers":v["stored_numbers"],arm+"_bits":v["stored_bits"]})
                precision.append(q)
        write_csv(f"out/phase19c_table1_3_paired_{cohort}.csv",rows)
        write_csv(f"out/phase19c_table5_precision_{cohort}.csv",precision)
        for arm,values in perarm.items():
            med=[v["quantized_minus_reference"]["paired_effect"]["median"] for v in values]
            precision_summary.append({"cohort":cohort,"arm":arm,"codec_failures":sum(v["codec_failures"] for v in values),
                "n_codes":sum(v["quantized_minus_reference"]["n_instances"] for v in values),"undefined_budget_points":sum(v is None for v in med),
                "range_of_document_paired_median_deltas":[min(med),max(med)] if all(v is not None for v in med) else None,
                "range_definition":"Range across all model x n x budget cells, not a conditional or pooled median"})
    negatives=[]
    for d in report["negative_controls"]:
        for B,p in d["budget"].items():
            row={"family":d["family"],"n":d["n"],"rank":p["rank"],"budget":int(B),"n_draws":d["n_draws"],**effect_fields(p)}
            for arm in ("svd","masked","free","thin"):row[arm+"_secondary_median_error"]=p["reference"]["methods"][arm]["relative"]["median"]
            negatives.append(row)
    write_csv("out/phase19c_table2_negative.csv",negatives)
    plants=[]
    for p in report["planted_controls"]:
        row={"n":p["n"],"k":p["k"],"noise":p["noise"],"trials":p["n_trials"],"threshold":p["threshold"],
            "oracle_reference":p["oracle_known_representation_relative"]["median"],"oracle_binary16":p["oracle_truth_binary16_relative"]["median"]}
        for arm in ("free","thin"):
            v=p["arms"][arm];s=v["relative"];row.update({arm+"_successes":v["successes"],arm+"_median_error":s["median"],
                arm+"_q25":s["q25"],arm+"_q75":s["q75"],arm+"_ci_low":s["ci95"][0],arm+"_ci_high":s["ci95"][1],arm+"_max_error":v["max_relative"]})
        plants.append(row)
    write_csv("out/phase19c_table4_planted.csv",plants)
    write_json("out/phase19c_readout.json",{"report_sha256":digest("out/phase19c_richlines.json"),"source_sha256":digest(__file__),
        "tables":[p.as_posix() for p in paths if p.suffix==".csv"],"precision_summary":precision_summary,
        "all_controls_and_undefined_points_retained":True,"no_fit_or_inference_changes":True})
    print("Created six wide review CSVs and readout index",flush=True)

if __name__=="__main__":main()
