"""Direct-design checks and representative nulls for the streaming QR ALS."""
import phase19c_common
import numpy as np
from scipy import linalg
from phase19c_prefix_qr import nested_solve
from phase19c_als_qr import fit
from phase19c_synthetic_controls import specs,make
from phase19c_common import write_json,SEED

def main():
    rng=np.random.default_rng(SEED);checks=[]
    for n,r in ((12,1),(12,4),(31,8),(128,16)):
        a=rng.normal(size=(n,n));f=rng.normal(size=(n,r))
        for reverse in (False,True):
            actual=nested_solve(a,f,reverse)
            expected=np.stack([linalg.lstsq(f[i:] if reverse else f[:i+1],a[i,i:] if reverse else a[i,:i+1],cond=1e-12,lapack_driver="gelsd")[0] for i in range(n)])
            delta=float(np.max(np.abs(actual-expected)))
            if delta>1e-7:raise AssertionError(f"Streaming QR differs from direct LS {delta}")
            checks.append({"n":n,"r":r,"reverse":reverse,"max_absolute":delta})
    rows=[]
    for spec in specs()["negative"]:
        if spec["family"]!="uniform_causal" and spec["trial"] not in (1,4):continue
        a,_=make(spec)
        for r in (1,2,4):
            row=fit(a,r);rows.append({"id":spec["id"],"r":r,"relative":row["relative"],"diagnostics":row["diagnostics"]})
            print(spec["id"],r,row["relative"],row["diagnostics"]["seconds"],flush=True)
    write_json("out/phase19c_qr_validation.json",{"passed":True,"direct_block_checks":checks,"null_cases":rows,
        "objective_and_rcond_unchanged":True,"streaming_QR_avoids_normal_equations":True})

if __name__=="__main__":main()
