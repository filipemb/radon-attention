"""Synthetic-only timing and value/gradient validation of the CPU backend."""
import os
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
import argparse
import numpy as np
import torch
import richlines_parametric as parametric
from richlines_core import LineDictionary,PROFILES,SEED,counts,omp,write_json,progress
from richlines_numba import NumbaRenderLines,validate


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--n",type=int,default=256)
    ap.add_argument("--iterations",type=int,default=100);args=ap.parse_args()
    torch.set_num_threads(4);torch.set_num_interop_threads(4)
    check=validate();parametric.RenderLines=NumbaRenderLines
    u=LineDictionary(args.n);p=LineDictionary(args.n,profiles=PROFILES)
    b=np.random.default_rng(SEED+args.n).lognormal(0,1,u.p)
    ks=counts(args.n)["parametric"]
    ur,ud=omp(b,u,ks,save_support=True);pr,pd=omp(b,p,ks,save_support=True)
    progress(f"CPU backend synthetic preparation n={args.n} complete")
    result,diag=parametric.fit_parametric(b,args.n,ks,u,p,ur,pr,SEED,device="cpu",iterations=args.iterations)
    write_json(f"out/phase19_benchmark_numba_n{args.n}.json",{"validation":check,"fit":diag,"errors":result,
               "data":"synthetic lognormal, no attention results used to choose the backend"})
    progress(f"CPU backend n={args.n}: all budgets + four starts + refinement {diag['seconds']:.1f}s")


if __name__=="__main__":main()
