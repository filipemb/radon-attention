"""Decode every saved discrete representation and verify whole-matrix errors.

This checks the reported storage model as well as the fit: atom identities and
amplitudes alone must reproduce the saved errors, without a saved residual.
"""
import os
for name in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[name]="4"
import json
from pathlib import Path
import numpy as np
from scipy import linalg
from richlines_core import LineDictionary,PROFILES,write_json,progress
from phase19_richlines import load_archive,read_jsonl


def main():
    selection=json.loads(Path("out/phase19_selection.json").read_text())
    stats={"instances":0,"discrete_decodes":0,"svd_reconstructions":0,
           "max_absolute_error_discrepancy":0.0,"max_relative_error_discrepancy":0.0,
           "max_svd_absolute_discrepancy":0.0,"max_active_nnls_projected_kkt":0.0}
    inverses=[]
    for n in (128,256):
        dictionaries={"uniform":LineDictionary(n),"profiled":LineDictionary(n,profiles=PROFILES)}
        for record in selection["datasets"]:
            if record["n"]!=n:continue
            model=record["model_slug"]
            rows=read_jsonl(Path(f"out/phase19_cpu_{model}_n{n}.jsonl"))
            if len(rows)!=record["selected_matrices"]:
                raise AssertionError("CPU audit requires every selected instance")
            A=load_archive(record)
            for index,row in enumerate(rows):
                if row["instance_id"]!=record["instances"][index]["instance_id"]:
                    raise AssertionError("Manifest identity mismatch in CPU cache")
                matrix=A[index];d=dictionaries["uniform"]
                target=matrix[d.i,d.j];norm=float(np.linalg.norm(matrix))
                for method,dictionary in dictionaries.items():
                    for k,result in row["methods"][method].items():
                        support=result["support"]
                        indices=support["indices"];amplitudes=np.asarray(support["amplitudes"])
                        if len(indices)>int(k) or len(indices)!=len(amplitudes) or (amplitudes<0).any():
                            raise AssertionError("Invalid discrete encoding")
                        selected=dictionary.D[indices]
                        decoded=np.asarray(selected.T@amplitudes).ravel()
                        residual=decoded-target
                        absolute=float(np.linalg.norm(residual));relative=absolute/norm
                        da=abs(absolute-result["absolute"]);dr=abs(relative-result["relative"])
                        stats["max_absolute_error_discrepancy"]=max(stats["max_absolute_error_discrepancy"],da)
                        stats["max_relative_error_discrepancy"]=max(stats["max_relative_error_discrepancy"],dr)
                        if max(da,dr)>1e-9:
                            raise AssertionError("Decoded discrete errors do not match saved metrics")
                        grad=np.asarray(selected@(residual/norm)).ravel()
                        kkt=float(np.max(np.abs(np.minimum(grad,amplitudes/norm)))) if len(indices) else 0.0
                        stats["max_active_nnls_projected_kkt"]=max(stats["max_active_nnls_projected_kkt"],kkt)
                        if kkt>1e-9:
                            raise AssertionError(f"Active NNLS KKT failure: {model} n={n} index={index} method={method} k={k} kkt={kkt}")
                        stats["discrete_decodes"]+=1
                U,s,V=linalg.svd(matrix,full_matrices=False,check_finite=False)
                for k,result in row["methods"]["svd"].items():
                    rank=int(k)
                    decoded=(U[:,:rank]*s[:rank])@V[:rank]
                    error=float(np.linalg.norm(decoded-matrix))
                    delta=abs(error-result["absolute"])
                    stats["max_svd_absolute_discrepancy"]=max(stats["max_svd_absolute_discrepancy"],delta)
                    if delta>1e-9:raise AssertionError("Explicit SVD differs from reported tail error")
                    stats["svd_reconstructions"]+=1
                inverses.append({"relative":row["methods"]["radon"]["all"]["relative"],
                                 "converged":row["methods"]["radon"]["all"]["converged"]})
                stats["instances"]+=1
            progress(f"CPU DECODE AUDIT {model} n={n}: all {len(rows)} instances verified")
    stats.update({"passed":True,"full_inverse_max_relative":max(r["relative"] for r in inverses),
                  "full_inverse_median_relative":float(np.median([r["relative"] for r in inverses])),
                  "full_inverse_converged_fraction":float(np.mean([r["converged"] for r in inverses])),
                  "error_comparison_tolerance":1e-9,"nnls_kkt_audit_tolerance":1e-9})
    write_json("out/phase19_cpu_integrity_audit.json",stats)
    progress(f"CPU DECODE AUDIT complete: {stats}")


if __name__=="__main__":main()
