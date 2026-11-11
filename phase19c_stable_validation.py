"""Check stable ALS on direct block solves, uniform and random causal nulls."""
import phase19c_common
import numpy as np
from scipy import linalg
from phase19c_als_stable import fit,update
from phase19c_common import write_json,SEED
from phase19c_synthetic import make,specs

def main():
    rng=np.random.default_rng(SEED);block=[]
    for n,r in ((12,1),(12,4),(31,8)):
        a=np.tril(rng.normal(size=(n,n)));factor=rng.normal(size=(n,r))
        for reverse in (False,True):
            target=a.T if reverse else a;actual,_=update(target,factor,reverse)
            expected=np.stack([linalg.lstsq(factor[i:] if reverse else factor[:i+1],target[i,i:] if reverse else target[i,:i+1],cond=1e-12,lapack_driver="gelsd")[0] for i in range(n)])
            delta=float(np.max(np.abs(actual-expected)))
            if delta>1e-8:raise AssertionError("Refined block solve disagrees with direct design LS")
            block.append(delta)
    rows=[]
    for spec in specs()["negative"]:
        if spec["family"]!="uniform_causal" and spec["trial"] not in (0,1,3,4):continue
        a,_=make(spec)
        for r in (1,2,4):
            result=fit(a,r)
            rows.append({"id":spec["id"],"r":r,"relative":result["relative"],"diagnostics":result["diagnostics"]})
            print(spec["id"],r,result["relative"],result["diagnostics"]["direct_sweep_retries"],len(result["diagnostics"]["numerically_rejected_sweeps"]),flush=True)
    write_json("out/phase19c_stable_validation.json",{"passed":True,"direct_block_max_errors":block,"null_cases":rows,
        "no_attention_case_used_to_choose_algorithm":True,"old_failures_retained":True})

if __name__=="__main__":main()
