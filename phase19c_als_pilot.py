"""Validate the ALS update against direct least squares before attention fitting."""
import phase19c_common
import numpy as np
from scipy import linalg
from phase19c_lowrank import fit,update
from phase19c_common import write_json,SEED

def main():
    rng=np.random.default_rng(SEED);checks=[]
    for n,r in ((12,1),(12,4),(31,8)):
        a=np.tril(rng.normal(size=(n,n)));f=rng.normal(size=(n,r))
        for reverse in (False,True):
            target=a.T if reverse else a;actual,_=update(target,f,reverse)
            expected=np.stack([linalg.lstsq(f[i:] if reverse else f[:i+1],target[i,i:] if reverse else target[i,:i+1],
                cond=1e-12,lapack_driver="gelsd")[0] for i in range(n)])
            delta=float(np.max(np.abs(actual-expected)))
            if delta>1e-7:raise AssertionError(f"ALS block mismatch {delta}")
            checks.append({"n":n,"r":r,"reverse":reverse,"max_absolute":delta})
    recovery=[]
    for n in (128,256):
        for r in (1,2,4,8,16):
            u=rng.lognormal(0,.7,(n,r));v=rng.lognormal(0,.7,(n,r));a=np.tril(u@v.T);a/=a.sum(axis=1,keepdims=True)
            result=fit(a,r)
            recovery.append({"n":n,"r":r,"relative":result["relative"],"diagnostics":result["diagnostics"]})
            print(n,r,result["relative"],result["diagnostics"]["seconds"],flush=True)
    write_json("out/phase19c_als_pilot.json",{"block_solves_passed":True,"block_checks":checks,"positive_controls":recovery,
        "fixed_before_attention_fits":True})

if __name__=="__main__":main()
