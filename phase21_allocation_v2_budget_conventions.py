"""Supplement: all three allocation conventions at common cap K8 (q7).

Keep the audited residual-r8 allocation sweep and its 17/9984 diagnostic. This
separate panel removes ambiguity between residual rank r and storage-cap K.
All methods here use residual rank seven and the unchanged named dictionary.
"""
import phase21_allocation_v2 as e4
import json
from pathlib import Path
import time
import numpy as np
from sampling import MODELS,load_sample,slug,sha256_file


def metrics(A,S,L,coef,norm2):
    m=int(np.count_nonzero(coef>0))
    cost=2*m+7*(2*A.shape[0]+1)
    cap=8*(2*A.shape[0]+1)
    if cost>cap:raise ArithmeticError("Convention exceeds the common K8 cap")
    return {"named_norm_ratio":float(np.linalg.norm(S)/np.sqrt(norm2)),
            "named_energy_ratio":float(np.sum(S*S)/norm2),
            "cross_energy_ratio":float(2*np.sum(S*L)/norm2),
            "named_only_explained_energy":1-float(np.sum((A-S)**2)/norm2),
            "relative_error":float(np.linalg.norm(A-S-L)/np.sqrt(norm2)),
            "named_channel_only_error":float(np.linalg.norm(A-S)/np.sqrt(norm2)),
            "named_channel_parameters":2*m,"actual_parameters":cost,"unused_parameters":cap-cost,
            "n_active":m}


def run(model,n):
    target=Path("out")/f"phase21_allocation_v2_budget8_conventions_{slug(model)}_n{n}.json"
    pairs=Path("out/pairs")/f"phase21_allocation_budget8_conventions_{slug(model)}_n{n}_v2.jsonl"
    if target.exists():return json.loads(target.read_text(encoding="utf-8"))
    Aall,manifest=load_sample(model,n)
    corepath,corepairs=e4.core_paths(model,n)
    core=json.loads(corepath.read_text(encoding="utf-8"))
    D=e4.v1.Dictionary(n)
    if core["dictionary"]["sha256_float64_C_order"]!=D.digest:raise ValueError("Named dictionary changed")
    rows=[]
    if pairs.exists():
        with pairs.open(encoding="utf-8") as inp:rows=[json.loads(s) for s in inp]
    start=time.perf_counter()
    e4.log(f"BUDGET CONVENTIONS START {model} n={n}: K8 q7 all three conventions; T5 fixed")
    pairs.parent.mkdir(parents=True,exist_ok=True)
    with corepairs.open(encoding="utf-8") as inp,pairs.open("a",encoding="utf-8") as out:
        for i,line in enumerate(inp):
            if i<len(rows):continue
            old=json.loads(line);A=Aall[i].astype(np.float64);eA=float(np.sum(A*A))
            if old["instance_id"]!=manifest["instances"][i]["instance_id"]:raise ValueError("Ordering mismatch")
            c0=np.array(old["named_first_coefficients"]);S0=(D.D@c0).reshape(n,n)
            f0=e4.v1.factor(A-S0);L0=e4.v1.truncate(f0,7)
            fA=e4.v1.factor(A);La=e4.v1.truncate(fA,7)
            Sl,cl,solver=D.project(A-La)
            S,L,c=S0,L0,c0
            trace=[float(np.sum((A-S-L)**2)/eA)];first_met=None
            fR=f0
            for iteration in range(2,6):
                S,c,solver=D.project(A-L)
                fR=e4.v1.factor(A-S);L=e4.v1.truncate(fR,7)
                objective=float(np.sum((A-S-L)**2)/eA)
                if objective>trace[-1]+2e-9:raise ArithmeticError("Alg1 objective increased")
                if first_met is None and abs(objective-trace[-1])/max(trace[-1],np.finfo(float).tiny)<=1e-7:first_met=iteration
                trace.append(objective)
            row={key:old[key] for key in ("instance_id","doc_id","document_index","model","n","layer","head")}
            row.update({"common_cap":8*(2*n+1),"budget_rank_K":8,"residual_rank":7,"conventions":{}})
            for method,SS,LL,cc,cut_s in (("named_first",S0,L0,c0,f0[1]),("lowrank_first",Sl,La,cl,fA[1]),
                                          (e4.ALT,S,L,c,fR[1])):
                mm=metrics(A,SS,LL,cc,eA)
                mm["svd_error"]=old["capacity"]["8"]["svd_error"]
                mm["paired_error_method_minus_svd"]=mm["relative_error"]-mm["svd_error"]
                item={"label":e4.LABELS[method],"metrics":mm,"coefficients":cc.tolist(),"cutoff":e4.v1.cutoff(cut_s,7,n)}
                if method==e4.ALT:item["diagnostics"]={"iterations":5,"early_stopping":False,"criterion_met":first_met is not None,
                    "criterion_first_met_at":first_met,"relative_squared_error_by_iteration":trace}
                row["conventions"][method]=item
            if abs(row["conventions"]["named_first"]["metrics"]["relative_error"]-old["capacity"]["8"]["named_first_error"])>1e-10:
                raise ArithmeticError("Named-first symmetric result does not reproduce audited spectrum")
            out.write(json.dumps(row,allow_nan=False,ensure_ascii=False,separators=(",",":"))+"\n");rows.append(row)
            if (i+1)%128==0:
                out.flush();e4.log(f"BUDGET CONVENTIONS {model} n={n}: {i+1}/{len(Aall)}")
    if len(rows)!=manifest["n_matrices"]:raise ValueError("Incomplete common-cap convention study")
    docs=[r["document_index"] for r in rows];summaries={}
    for method in e4.CONVENTIONS:
        obs=[r["conventions"][method] for r in rows]
        summaries[method]={"label":e4.LABELS[method],
            "metrics":{key:e4.summarize([r["metrics"][key] for r in obs],docs) for key in obs[0]["metrics"]},
            "paired_error_method_minus_SVD":e4.paired([r["metrics"]["paired_error_method_minus_svd"] for r in obs],rows),
            "cutoff_ties":{key:sum(int(r["cutoff"][key]) for r in obs) for key in ("exact_tie","numerical_tie","positive_numerical_tie")}}
        if method==e4.ALT:summaries[method]["criterion_met_by_5"]=sum(int(r["diagnostics"]["criterion_met"]) for r in obs)
    result={"schema_version":2,"model":model,"n":n,"n_instances":len(rows),"n_documents":64,
            "budget_rank_K":8,"residual_rank":7,"common_cap":8*(2*n+1),"conventions":summaries,
            "legacy_r8_diagnostic_note":"17/9984 belongs to the separate audited allocation sweep at residual r8, not this q7 common-cap panel",
            "source_core_sha256":sha256_file(corepath),"pairs_path":pairs.as_posix(),"pairs_sha256":sha256_file(pairs),
            "elapsed_seconds":time.perf_counter()-start}
    e4.write_new(target,result);e4.log(f"BUDGET CONVENTIONS DONE {model} n={n}; seconds={result['elapsed_seconds']:.1f}")
    return result


if __name__=="__main__":
    for n in (128,256):
        for model in MODELS:run(model,n)
