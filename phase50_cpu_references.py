"""Prepare independent CPU-double references without holding the GPU lock."""
import phase50_als as als
import argparse
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import json
import numpy as np
from phase50_experiment import read,jsonl,PROTOCOL,Dictionary,normalize_cpu,metrics
from sampling import MODELS,slug,sha256_file,load_sample,write_json_new


def prepare(model):
    target=Path(f"out/phase50_GPU_CPU_reference_{slug(model)}.json")
    pairpath=Path(f"out/pairs/phase50_GPU_CPU_reference_{slug(model)}.jsonl")
    ph=sha256_file(PROTOCOL); protocol=read(PROTOCOL); selected=protocol["datasets"][model]["GPU_validation_indices"]
    if target.exists():
        old=read(target)
        if old["protocol_sha256"]!=ph or old["pairs_sha256"]!=sha256_file(pairpath): raise ValueError("CPU reference cache changed")
        return str(target)
    attention,manifest=load_sample(model,128); dictionary=Dictionary(128)
    rows=jsonl(pairpath) if pairpath.exists() else []
    seen={(r["archive_index"],r["K"],r["arm"]) for r in rows}
    if len(seen)!=len(rows) or any(r["protocol_sha256"]!=ph for r in rows): raise ValueError("CPU reference resume mismatch")
    pairpath.parent.mkdir(parents=True,exist_ok=True)
    with pairpath.open("a",encoding="utf-8") as out:
        for idx in selected:
            original=attention[idx].astype(np.float64); named=dictionary.project(original)[0]
            ref=normalize_cpu(original,original)[0]
            for k in (8,16):
                for arm in ("masked_K","named_plus_masked"):
                    if (idx,k,arm) in seen: continue
                    rank=k if arm=="masked_K" else k-1
                    a=original if arm=="masked_K" else original-named
                    u,s,vh=np.linalg.svd(a,full_matrices=False)
                    initial=(u[:,:rank]*np.sqrt(s[:rank]),vh[:rank].T*np.sqrt(s[:rank]))
                    product,info=als.fit_cpu(a,rank,initial)
                    row={"model":model,"archive_index":idx,"instance_id":manifest["instances"][idx]["instance_id"],
                         "K":k,"arm":arm,"protocol_sha256":ph,"initial_U":initial[0].tolist(),"initial_V":initial[1].tolist(),
                         "CPU":metrics(product+(named if arm=="named_plus_masked" else 0),original,ref),"CPU_ALS":info}
                    out.write(json.dumps(row,allow_nan=False,separators=(",",":"))+"\n");out.flush()
                    rows.append(row);seen.add((idx,k,arm))
            print(f"CPU REFERENCE {model}: {len(seen)}/128 fits",flush=True)
    if len(rows)!=128: raise ValueError("Incomplete32-matrix CPU reference study")
    write_json_new(target,{"model":model,"protocol_sha256":ph,"n_matrices":32,"n_fits":128,"pairs_path":pairpath.as_posix(),
                           "pairs_sha256":sha256_file(pairpath),"initial_factors_stored_exact_float64_round_trip":True})
    return str(target)


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--workers",type=int,default=2);args=ap.parse_args()
    with ProcessPoolExecutor(max_workers=min(3,args.workers)) as pool: list(pool.map(prepare,MODELS))
