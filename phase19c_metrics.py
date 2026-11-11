"""Identical full-matrix errors before and after direct IEEE binary16 storage."""
import phase19c_common
import numpy as np
from phase19c_render import forward
from phase19c_lowrank import errors

def line_image(parameters,n):
    p=np.asarray(parameters,dtype=float)
    if p.ndim!=2 or p.shape[1]!=5 or not np.isfinite(p).all() or np.any(p[:,2]<=0) or np.any(p[:,4]<0):
        raise ValueError("Invalid parametric code")
    values=[np.ascontiguousarray(p[:,i][None]) for i in range(5)];values[2]=np.log(values[2])
    packed,_=forward(*values,n)
    a=np.zeros((n,n));a[np.tril_indices(n)]=packed[0]
    if not np.isfinite(a).all():raise FloatingPointError("Nonfinite line reconstruction")
    return a

def binary16(values):
    a=np.asarray(values,dtype=float)
    if not np.isfinite(a).all():raise ValueError("Nonfinite input to quantization")
    # An overflow is a reported codec failure. Values are never clipped or imputed.
    with np.errstate(over="ignore"):out=a.astype(np.float16).astype(np.float64)
    if not np.isfinite(out).all():
        return None,{"success":False,"reason":"IEEE binary16 range overflow","maximum_absolute":float(np.abs(a).max())}
    return out,{"success":True,"format":"IEEE754 binary16, round-to-nearest ties-to-even, decode in float64",
        "underflow_to_zero_count":int(np.sum((a!=0)&(out==0))),"numbers":int(a.size),
        "max_absolute_rounding_error":float(np.max(np.abs(a-out)))}

def line_result(parameters,a,metadata=None):
    p=np.asarray(parameters,dtype=float);n=len(a);full=errors(a,line_image(p,n));q,diag=binary16(p)
    quant={**errors(a,line_image(q,n)),"quantization":diag} if q is not None else {"relative":None,"absolute":None,"quantization":diag}
    return {**full,"parameters":p.tolist(),"stored_numbers":5*len(p),"bits16":80*len(p),"components":len(p),
        "fp16":quant,**({"optimization":metadata} if metadata is not None else {})}

def factor_precision(row,a,masked=False):
    uq,ud=binary16(row["U"]);vq,vd=binary16(row["V"]);diags={"U":ud,"V":vd}
    success=ud["success"] and vd["success"]
    if not masked:
        sq,sd=binary16(row["S"]);diags["S"]=sd;success&=sd["success"]
    if success:
        hat=uq@vq.T if masked else (uq*sq)@vq.T
        if masked:hat=np.tril(hat)
        quant=errors(a,hat)
    else:quant={"relative":None,"absolute":None}
    row["fp16"]={**quant,"quantization":{"success":bool(success),"factors":diags,
        "format":"direct IEEE754 binary16 storage of every factor, float64 decode; no post-quantization fitting"}}
    row["bits16"]=16*row["stored_numbers"]
    return row
