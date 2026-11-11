"""Compiled direct design-matrix least squares, without changing the solver."""
import phase19c_common
import numpy as np
from numba import njit

@njit(cache=True)
def solve_blocks(a,factor,indices,reverse):
    out=np.empty((len(indices),factor.shape[1]))
    for q in range(len(indices)):
        i=indices[q]
        if reverse:
            design=factor[i:,:].copy();target=a[i,i:].copy()
        else:
            design=factor[:i+1,:].copy();target=a[i,:i+1].copy()
        out[q]=np.linalg.lstsq(design,target,1e-12)[0]
    return out
