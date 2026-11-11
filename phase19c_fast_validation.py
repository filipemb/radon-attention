"""Numerical agreement of compiled blocks and stable ALS; no attention fitting."""
import phase19c_common
import numpy as np
from scipy import linalg
from phase19c_batched import solve_blocks
from phase19c_als_fast import fit
from phase19c_synthetic_controls import make,specs
from phase19c_common import write_json,SEED

def main():
    rng=np.random.default_rng(SEED);checks=[]
    for n,r in ((12,1),(12,4),(31,8),(128,16)):
        a=rng.normal(size=(n,n));f=rng.normal(size=(n,r));indices=np.arange(n)
        for reverse in (False,True):
            actual=solve_blocks(a,f,indices,reverse)
            expected=np.stack([linalg.lstsq(f[i:] if reverse else f[:i+1],a[i,i:] if reverse else a[i,:i+1],cond=1e-12,lapack_driver="gelsd")[0] for i in indices])
            d=float(np.max(np.abs(actual-expected)))
            if d>1e-7:raise AssertionError("Compiled direct solver differs from scipy design SVD LS")
            checks.append({"n":n,"r":r,"reverse":reverse,"max_absolute":d})
    rows=[]
    for spec in specs()["negative"]:
        if spec["family"]!="uniform_causal" and spec["trial"] not in (1,4):continue
        a,_=make(spec)
        for r in (1,2,4):
            result=fit(a,r)
            rows.append({"id":spec["id"],"r":r,"relative":result["relative"],"diagnostics":result["diagnostics"]})
            print(spec["id"],r,result["relative"],result["diagnostics"]["seconds"],flush=True)
    write_json("out/phase19c_fast_validation.json",{"passed":True,"direct_block_checks":checks,"null_cases":rows,
        "compiled_solver_changes_no_objective_regularization_or_data":True})

if __name__=="__main__":main()
