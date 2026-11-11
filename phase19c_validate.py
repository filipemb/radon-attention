"""Independent dense decoding and direct binary16 rounding checks."""
import phase19c_common
import numpy as np
from richlines_parametric import render_numpy
from phase19c_metrics import line_image,binary16,factor_precision
from phase19c_common import SEED,write_json
from phase19c_als import svd_models

def main():
    rng=np.random.default_rng(SEED);checks=[]
    for n in (128,256):
        p=np.column_stack([rng.uniform(0,2*np.pi,6),rng.uniform(-n/3,n/3,6),np.array([.2,.5,1.,2.,8.,32.]),rng.uniform(-32,32,6),rng.uniform(.1,1,6)])
        for precision in (64,16):
            q=p if precision==64 else binary16(p)[0]
            a=line_image(q,n)[np.tril_indices(n)];expected=render_numpy(q,n)
            delta=float(np.max(np.abs(a-expected)))
            if delta>1e-9:raise AssertionError("New renderer differs from independent dense implementation")
            checks.append({"n":n,"parameter_bits":precision,"max_absolute":delta})
    x=np.array([.2,1.,np.pi,65510.,1e-10]);q,d=binary16(x)
    if not np.array_equal(q,x.astype(np.float16).astype(float)):raise AssertionError("Incorrect binary16 rounding")
    q,d=binary16([1e10])
    if q is not None or d["success"]:raise AssertionError("Quantization overflow must be an explicit failure")
    a=np.tril(rng.random((12,12)));rows,_=svd_models(a,[2]);row=factor_precision(rows[2],a)
    u=np.asarray(row["U"]).astype(np.float16).astype(float);s=np.asarray(row["S"]).astype(np.float16).astype(float);v=np.asarray(row["V"]).astype(np.float16).astype(float)
    direct=np.linalg.norm(a-(u*s)@v.T)/np.linalg.norm(a)
    if abs(row["fp16"]["relative"]-direct)>1e-14:raise AssertionError("SVD quantized score differs")
    write_json("out/phase19c_numerical_validation.json",{"passed":True,"dense_renderer_checks":checks,"IEEE_binary16_direct_rounding":True,
        "overflow_is_explicit_failure":True,"quantized_svd_matches_manual_decode":True})

if __name__=='__main__':main()
