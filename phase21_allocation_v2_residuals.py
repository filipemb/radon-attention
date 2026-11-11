"""E4 v2 residuals for the principal symmetric K=8, q=7 comparison.

Full spectra, Shannon effective ranks, diagonal-distance and initial-column
energy use instance medians and imported document-block bootstrap. Named-first
S and the cone dictionary are exactly those in the audited experiment.
"""
import phase21_allocation_v2 as e4
import json
from pathlib import Path
import time
import numpy as np
from sampling import MODELS, load_sample, sample_paths, sha256_file, slug


def run(model,n):
    path=Path("out")/f"phase21_allocation_v2_residuals_{slug(model)}_n{n}.json"
    pairs=Path("out/pairs")/f"phase21_allocation_residuals_{slug(model)}_n{n}_v2.jsonl"
    if path.exists():
        existing=json.loads(path.read_text(encoding="utf-8"))
        if existing["pairs_sha256"]!=sha256_file(pairs):
            raise ValueError("Existing residual pairs changed")
        return existing
    started=time.perf_counter()
    attention,manifest=load_sample(model,n)
    corepath,corepairs=e4.core_paths(model,n)
    core=json.loads(corepath.read_text(encoding="utf-8"))
    dictionary=e4.v1.Dictionary(n)
    if core["dictionary"]["sha256_float64_C_order"]!=dictionary.digest:
        raise ValueError("Residual dictionary changed")
    rows=[]
    if pairs.exists():
        with pairs.open(encoding="utf-8") as inp:rows=[json.loads(s) for s in inp]
    e4.log(f"RESIDUAL START {model} n={n}: symmetric K8/q7; all spectra/spatial energy; primary imported describe")
    pairs.parent.mkdir(parents=True,exist_ok=True)
    with corepairs.open(encoding="utf-8") as inp,pairs.open("a",encoding="utf-8") as out:
        for i,line in enumerate(inp):
            if i<len(rows):continue
            source=json.loads(line)
            A=attention[i].astype(np.float64)
            c=np.asarray(source["named_first_coefficients"])
            S=(dictionary.D@c).reshape(n,n)
            R=A-S
            factors=e4.v1.factor(R)
            L=e4.v1.truncate(factors,7)
            E=R-L
            energy=float(np.sum(A*A))
            if abs(float(np.linalg.norm(E)/np.sqrt(energy))-source["capacity"]["8"]["named_first_error"])>1e-10:
                raise ArithmeticError("New symmetric residual does not reproduce the stored spectral error")
            row={k:source[k] for k in ("instance_id","doc_id","document_index","model","n","layer","head")}
            row.update({"budget_rank_K":8,"residual_rank":7,"attention_frobenius_norm":np.sqrt(energy),
                        "R":e4.v1.residual_profile(R,factors[1],energy,dictionary),
                        "E":e4.v1.residual_profile(E,factors[1],energy,dictionary,"R",7)})
            out.write(json.dumps(row,allow_nan=False,separators=(",",":"))+"\n")
            rows.append(row)
            if (i+1)%128==0:
                out.flush();e4.log(f"RESIDUAL {model} n={n}: {i+1}/{len(attention)}")
    if len(rows)!=manifest["n_matrices"]:raise ValueError("Incomplete residual population")
    docs=[r["document_index"] for r in rows]
    summary={}
    for name in ("R","E"):
        records=[r[name] for r in rows]
        scalar=[k for k,v in records[0].items() if isinstance(v,(int,float,bool)) and k!="spectrum_drop_first"]
        item={k:e4.summarize([r[k] for r in records],docs) for k in scalar}
        for key in ("distance_fraction_of_residual","distance_energy_over_A","columns_0_to_3_fraction_of_residual",
                    "top_1_4_8_16_spectral_energy_fraction"):
            item[key]=[e4.summarize([r[key][j] for r in records],docs) for j in range(len(records[0][key]))]
        summary[name]=item
    # E's singular values are exactly the tail of R followed by seven zeros;
    # sharing these pointwise summaries avoids repeating the same estimator.
    R_spectra=np.stack([r["R"]["singular_values"] for r in rows])
    norms=np.array([r["attention_frobenius_norm"] for r in rows])
    summary["R"]["singular_values"]=[e4.summarize(R_spectra[:,j],docs) for j in range(n)]
    summary["R"]["singular_values_over_A_norm"]=[e4.summarize(R_spectra[:,j]/norms,docs) for j in range(n)]
    zero=e4.summarize(np.zeros(len(rows)),docs)
    summary["E"]["singular_values"]=summary["R"]["singular_values"][7:]+[zero]*7
    summary["E"]["singular_values_over_A_norm"]=summary["R"]["singular_values_over_A_norm"][7:]+[zero]*7
    result={"schema_version":2,"model":model,"n":n,"n_instances":len(rows),"n_documents":64,
            "budget_rank_K":8,"residual_rank":7,"convention":"named_first",
            "statistics":"Imported phase24.describe, instance median and document-block CI; mean of document means secondary",
            "distance_bins":list(e4.v1.DISTANCE_LABELS),"metrics":summary,
            "input_manifest_sha256":sha256_file(sample_paths(model,n)[1]),
            "pairs_path":pairs.as_posix(),"pairs_sha256":sha256_file(pairs),
            "elapsed_seconds":time.perf_counter()-started}
    e4.write_new(path,result)
    e4.log(f"RESIDUAL DONE {model} n={n}; {result['elapsed_seconds']:.1f}s")
    return result


if __name__=="__main__":
    for n in (128,256):
        for model in MODELS:run(model,n)
