"""CPU revision: mass-stratified constancy and document CIs of saved V3 pairs."""
from revision_v3_stats import (MODELS,slug,sha256_file,write_json_new,progress,
                               describe,fraction_summary)
from sampling import load_sample,validate_matrices
import argparse
import json
from pathlib import Path
import time
import numpy as np

MODELS_CONSTANCY=MODELS+["Qwen/Qwen2.5-7B"]
MIN_ROWS=8
THRESHOLD=.3

def paths(model,n):
    root=Path("data/attn_7b" if model.endswith("-7B") else "data/attn")
    stem=root/f"{slug(model)}_n{n}"
    return Path(str(stem)+".npz"),Path(str(stem)+".manifest.json")

def load(model,n):
    archive,manifest_path=paths(model,n)
    meta=json.loads(manifest_path.read_text(encoding="utf-8"))
    assert meta["status"]=="verified" and meta["npz_sha256"]==sha256_file(archive)
    with np.load(archive,allow_pickle=False) as z:a=z["attention"]
    assert a.dtype==np.float16 and a.shape==(len(meta["instances"]),n,n)
    check=validate_matrices(a,meta["storage_row_sum_atol"])
    assert check["invalid_matrices"]==0
    return a,meta,check

def measure(a):
    x=np.asarray(a,dtype=np.float64);n=len(x)
    if not np.isfinite(x).all():raise ValueError("Nonfinite input cannot be replaced")
    values=[];energies=[]
    for j in range(n-MIN_ROWS+1):
        col=x[j:,j];energy=float(np.dot(col,col));energies.append(energy)
        values.append(float(np.dot(col-col.mean(),col-col.mean())/energy) if energy>0 else None)
    control=[v for v in values[1:] if v is not None]
    return {"sink_mean_weight":float(x[:,0].mean()),
        "sink_mass_stratum":"gt_0.3" if x[:,0].mean()>THRESHOLD else "le_0.3",
        "sink_nonconstancy":values[0],
        "control_column_nonconstancy_median":float(np.median(control)) if control else None,
        "middle_column_nonconstancy_secondary":values[n//2],
        "sink_column_energy":energies[0],"n_control_columns_total":len(values)-1,
        "n_zero_energy_control_columns":sum(v is None for v in values[1:]),
        "zero_energy_control_column_indices":[j for j,v in enumerate(values) if j and v is None],
        "n_defined_control_columns":len(control)}

def summarize_stratum(rows,all_rows,universe):
    docs=[r["document_index"] for r in all_rows]
    selected_ids={r["instance_id"] for r in rows}
    result={"n_heads":len(rows),"fraction_of_all_heads":fraction_summary(
        [r["instance_id"] in selected_ids for r in all_rows],docs,universe),
        "n_zero_energy_sink_columns":sum(r["sink_nonconstancy"] is None for r in rows),
        "n_zero_energy_control_columns":sum(r["n_zero_energy_control_columns"] for r in rows),
        "n_control_columns_total":sum(r["n_control_columns_total"] for r in rows),
        "n_heads_without_defined_control":sum(r["control_column_nonconstancy_median"] is None for r in rows)}
    for key in ["sink_nonconstancy","control_column_nonconstancy_median","middle_column_nonconstancy_secondary","sink_mean_weight"]:
        defined=[r for r in rows if r[key] is not None]
        result[key]=describe([r[key] for r in defined],[r["document_index"] for r in defined],document_universe=universe)
        result[key]["n_undefined_heads_excluded"]=len(rows)-len(defined)
    paired=[r for r in rows if r["sink_nonconstancy"] is not None and r["control_column_nonconstancy_median"] is not None]
    result["same_heads_comparison"]={"n_heads":len(paired),
        "sink":describe([r["sink_nonconstancy"] for r in paired],[r["document_index"] for r in paired],document_universe=universe),
        "control":describe([r["control_column_nonconstancy_median"] for r in paired],[r["document_index"] for r in paired],document_universe=universe),
        "sink_minus_control":describe([r["sink_nonconstancy"]-r["control_column_nonconstancy_median"] for r in paired],
                                      [r["document_index"] for r in paired],document_universe=universe)}
    return result

def constancy_one(model,n):
    target=Path(f"out/phase15_constancy_{slug(model)}_n{n}_v3.json")
    if target.exists():return json.loads(target.read_text(encoding="utf-8"))
    started=time.perf_counter();a,meta,validation=load(model,n)
    pairs=Path(f"out/pairs/constancy_{slug(model)}_n{n}_v3.jsonl");pairs.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    if pairs.exists():
        rows=[json.loads(s) for s in pairs.read_text(encoding="utf-8").splitlines()]
        assert [r["instance_id"] for r in rows]==[r["instance_id"] for r in meta["instances"][:len(rows)]]
    with pairs.open("a",encoding="utf-8") as f:
        for i in range(len(rows),len(a)):
            row={**meta["instances"][i],**measure(a[i])};rows.append(row)
            f.write(json.dumps(row,allow_nan=False)+"\n")
    universe=np.arange(meta["n_documents_effective"])
    result={"model":model,"n":n,"n_instances":len(rows),"n_documents":len(universe),
        "threshold":THRESHOLD,"minimum_valid_rows_per_column":MIN_ROWS,"denominator_epsilon":0,
        "control_definition":"Per head: median nonconstancy among non-sink columns with >=8 causal rows and positive energy",
        "zero_energy_policy":"Undefined; exclude and count. All-zero control heads stay explicitly undefined.",
        "bootstrap_rule":"Resample all original document blocks, including empty blocks after stratification; no balancing/subsampling",
        "manifest_path":paths(model,n)[1].as_posix(),"manifest_sha256":sha256_file(paths(model,n)[1]),
        "pairs_path":pairs.as_posix(),"pairs_sha256":sha256_file(pairs),"input_validation":validation,
        "strata":{s:summarize_stratum([r for r in rows if r["sink_mass_stratum"]==s],rows,universe)
                  for s in ["gt_0.3","le_0.3"]},"elapsed_seconds":time.perf_counter()-started}
    assert sum(s["n_heads"] for s in result["strata"].values())==len(a)
    write_json_new(target,result)
    progress("V3 constancy",f"{model} n={n}; {len(a)} heads, two mass strata, zero energy excluded/counted",result["elapsed_seconds"])
    print(f"CONSTANCY {model} n={n}: {len(rows)} heads, {result['elapsed_seconds']:.1f}s",flush=True)
    return result

def named_one(model,n):
    target=Path(f"out/phase26_named_{slug(model)}_n{n}_ci_v3.json")
    if target.exists():return json.loads(target.read_text(encoding="utf-8"))
    started=time.perf_counter()
    source=Path(f"out/phase26_named_{slug(model)}_n{n}_msclean_srpca_v2.json")
    old=json.loads(source.read_text(encoding="utf-8"));pairs=Path(old["pairs_path"])
    assert old["pairs_sha256"]==sha256_file(pairs)
    rows=[json.loads(s) for s in pairs.read_text(encoding="utf-8").splitlines()]
    assert len(rows)==old["n_instances"]
    meta=json.loads(paths(model,n)[1].read_text(encoding="utf-8"))
    assert [r["instance_id"] for r in rows]==[r["instance_id"] for r in meta["instances"]]
    docs=[r["document_index"] for r in rows];configurations={}
    for config,metrics in rows[0]["configurations"].items():
        configurations[config]={}
        for metric,value in metrics.items():
            if not isinstance(value,(float,int)):continue
            values=[r["configurations"][config][metric] for r in rows]
            item=describe(values,docs)
            assert item["median"]==old["configurations"][config][metric]["median"]
            configurations[config][metric]=item
    result={"model":model,"n":n,"n_instances":len(rows),"n_documents":len(set(docs)),
        "decompositions_recomputed":False,"all_configurations_use_same_instances":True,
        "source_result":source.as_posix(),"source_result_sha256":sha256_file(source),
        "pairs_path":pairs.as_posix(),"pairs_sha256":sha256_file(pairs),
        "definitions":old["definitions"],"configurations":configurations,
        "elapsed_seconds":time.perf_counter()-started}
    write_json_new(target,result)
    progress("V3 named intervals",f"{model} n={n}; {len(rows)} instances, 15 configurations; raw decompositions reused",result["elapsed_seconds"])
    print(f"NAMED CI {model} n={n}: {result['elapsed_seconds']:.1f}s",flush=True)
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--part",choices=["constancy","named"],required=True)
    args=ap.parse_args();started=time.perf_counter()
    models=MODELS_CONSTANCY if args.part=="constancy" else MODELS
    datasets=[(constancy_one if args.part=="constancy" else named_one)(m,n) for m in models for n in [128,256]]
    target="out/phase15_constancy_v3.json" if args.part=="constancy" else "out/phase26_named_v3_ci.json"
    result={"schema_version":3,"primary":"median over instances; CI95 whole-document bootstrap, seed0, 2000 draws",
            "datasets":datasets,"elapsed_seconds":time.perf_counter()-started,
            "statistics_source_sha256":sha256_file("revision_v3_stats.py"),"script_sha256":sha256_file(__file__)}
    write_json_new(target,result)
    progress("V3 CPU complete",f"{args.part}; {len(datasets)} datasets",result["elapsed_seconds"],
             f".venv/Scripts/python.exe -B phase36_constancy_named_ci.py --part {args.part}")

if __name__=="__main__":main()
