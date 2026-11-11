"""Float64 value/gradient equivalence and kernel timing across line widths."""
import os
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
import time
import numpy as np
import richlines_numba as old
import richlines_recurrence as new
from richlines_core import SEED,write_json,progress


def parameters(n,k,width=None):
    rng=np.random.default_rng(SEED+n+k)
    theta=rng.uniform(0,2*np.pi,(4,k));i,j=np.tril_indices(n)
    anchor=rng.integers(len(i),size=(4,k));x=j[anchor]-(n-1)/2;y=i[anchor]-(n-1)/2
    rho=np.cos(theta)*x+np.sin(theta)*y
    w=np.exp(rng.uniform(np.log(.2),np.log(n),(4,k))) if width is None else np.full((4,k),width)
    decay=rng.uniform(-32 if width is None else -4,32 if width is None else 4,(4,k))
    if width is None:rho[:,-8:]=rng.uniform(-np.sqrt(2)*n,np.sqrt(2)*n,(4,8))
    arrays=(theta,rho,np.log(w),decay,np.full((4,k),1/np.sqrt(k)))
    return tuple(np.ascontiguousarray(p.astype(np.float32).astype(np.float64)) for p in arrays)


def main():
    n=256;params=parameters(n,32)
    go=np.random.default_rng(SEED).normal(size=(4,n*(n+1)//2))
    a,an=old.forward(*params,n);b,bn=new.forward(*params,n)
    ag=old.backward(*params,an,go,n);bg=new.backward(*params,bn,go,n)
    if not np.isfinite([*a.ravel(),*b.ravel(),*ag.ravel(),*bg.ravel()]).all():
        raise FloatingPointError("Nonfinite full-domain renderer comparison")
    value=float(np.max(np.abs(a-b)));gradient=float(np.max(np.abs(ag-bg)/(1+np.abs(ag))))
    if value>2e-10 or gradient>2e-8:raise AssertionError(f"Recurrence mismatch {value}, {gradient}")
    timings={}
    for width in [.5,4,32,128]:
        params=parameters(n,128,width);times={}
        for label,module in [("direct_exponentials",old),("exact_recurrence",new)]:
            output,norms=module.forward(*params,n);module.backward(*params,norms,go,n)
            begin=time.perf_counter()
            for repeat in range(3):
                output,norms=module.forward(*params,n);module.backward(*params,norms,go,n)
            times[label]=(time.perf_counter()-begin)/3
        times["speed_ratio"]=times["direct_exponentials"]/times["exact_recurrence"]
        timings[str(width)]=times
    result={"passed":True,"n":n,"full_allowed_domain_random_parameters":True,
        "parameters_float32_accumulation_float64":True,"forward_max_absolute":value,
        "gradient_max_scaled_absolute":gradient,"value_tolerance":2e-10,"gradient_tolerance":2e-8,
        "kernel_timings_four_starts_k128":timings,"data":"synthetic, no archived attention"}
    write_json("out/phase19_recurrence_numerical_validation.json",result)
    progress(f"Recurrence full-domain validation passed; maximum value difference {value:.3g}, scaled gradient {gradient:.3g}; kernel speed ratios {[round(t['speed_ratio'],2) for t in timings.values()]}")


if __name__=="__main__":main()
