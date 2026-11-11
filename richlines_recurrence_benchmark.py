"""Synthetic-only renderer comparison and fixed-grid fit timing."""
import os
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
import argparse,time
import numpy as np
import torch
import richlines_parametric as parametric
from richlines_core import LineDictionary,PROFILES,SEED,counts,omp,write_json,progress
from richlines_recurrence import RecurrenceRenderLines,validate


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--n",type=int,default=256)
    ap.add_argument("--iterations",type=int,default=100);args=ap.parse_args()
    torch.set_num_threads(4);torch.set_num_interop_threads(4)
    check=validate();parametric.RenderLines=RecurrenceRenderLines
    u=LineDictionary(args.n);p=LineDictionary(args.n,profiles=PROFILES)
    b=np.random.default_rng(SEED+args.n).lognormal(0,1,u.p);ks=counts(args.n)["parametric"]
    ur,ud=omp(b,u,ks,save_support=True);pr,pd=omp(b,p,ks,save_support=True)
    progress(f"Recurrence CPU synthetic preparation n={args.n} complete")
    result,diag=parametric.fit_parametric(b,args.n,ks,u,p,ur,pr,SEED,device="cpu",iterations=args.iterations)
    write_json(f"out/phase19_benchmark_recurrence_n{args.n}.json",{"validation":check,"fit":diag,"errors":result,
        "data":"same synthetic lognormal seed, all budgets, four starts, no archived attention used"})
    progress(f"Recurrence CPU n={args.n}: 100 Adam + 150 L-BFGS-B all-budget synthetic fit {diag['seconds']:.1f}s")


if __name__=="__main__":main()
