"""Streaming Givens QR for every nested causal least-squares problem.

Each new design row rotates the same augmented right-hand sides. The small
triangular factor has the design singular values, so direct SVD least squares
on it preserves the original rcond without squaring the condition number.
"""
import phase19c_common
import math
import numpy as np
from numba import njit

@njit(cache=True)
def nested_solve(a,factor,reverse):
    n,r=factor.shape;triangular=np.zeros((r,r));transformed=np.zeros((r,n));out=np.empty((n,r))
    for step in range(n):
        i=n-1-step if reverse else step
        incoming=factor[i].copy();rhs=a[:,i].copy()
        first=0 if reverse else i;stop=i+1 if reverse else n
        for pivot in range(r):
            radius=math.hypot(triangular[pivot,pivot],incoming[pivot])
            if radius==0:continue
            cosine=triangular[pivot,pivot]/radius;sine=incoming[pivot]/radius
            for col in range(pivot,r):
                old=triangular[pivot,col]
                triangular[pivot,col]=cosine*old+sine*incoming[col]
                incoming[col]=-sine*old+cosine*incoming[col]
            for target in range(first,stop):
                old=transformed[pivot,target]
                transformed[pivot,target]=cosine*old+sine*rhs[target]
                rhs[target]=-sine*old+cosine*rhs[target]
        out[i]=np.linalg.lstsq(triangular,transformed[:,i].copy(),1e-12)[0]
    return out
