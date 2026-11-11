"""Fail immediately, with numerical context, on a nonfinite CUDA fit value."""
import os
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"):
    os.environ[key]="4"
import argparse
import json
import numpy as np
import torch
from pathlib import Path
from richlines_core import LineDictionary,PROFILES,SEED,counts
from richlines_cuda import CudaRenderLines
from richlines_parametric import fit_parametric
from phase19_richlines import selection_record,load_archive,read_jsonl


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--index",type=int,default=3);ap.add_argument("--n",type=int,default=128)
    ap.add_argument("--model",default="gpt2");args=ap.parse_args()
    torch.set_num_threads(4)
    original_forward=CudaRenderLines.forward;original_backward=CudaRenderLines.backward
    calls=[0]
    def forward(ctx,*values):
        calls[0]+=1
        for name,v in zip(["theta","rho","logwidth","decay","amplitude"],values[:5]):
            if not torch.isfinite(v).all():
                raise FloatingPointError(f"nonfinite input {name}; call {calls[0]}; shape {v.shape}")
        out=original_forward(ctx,*values)
        if not torch.isfinite(out).all():
            print('parameters',[(v.min().item(),v.max().item()) for v in values[:5]],flush=True)
            print('norm',ctx.saved_tensors if hasattr(ctx,'saved_tensors') else 'unavailable',flush=True)
            raise FloatingPointError(f"nonfinite forward; call {calls[0]}; shape {values[0].shape}")
        return out
    def backward(ctx,grad):
        out=original_backward(ctx,grad)
        for name,v in zip(["theta","rho","logwidth","decay","amplitude"],out[:5]):
            if not torch.isfinite(v).all():
                ids=torch.nonzero(~torch.isfinite(v))
                print('bad gradient',name,ids.cpu().tolist(),flush=True)
                print('bad parameters',[[p[tuple(idx)].item() for p in ctx.saved_tensors] for idx in ids],flush=True)
                raise FloatingPointError(f"nonfinite backward; call {calls[0]}; shape {v.shape}")
        return out
    CudaRenderLines.forward=staticmethod(forward);CudaRenderLines.backward=staticmethod(backward)
    record=selection_record(args.model,args.n);A=load_archive(record)
    rows=read_jsonl(Path(f"out/phase19_cpu_{args.model}_n{args.n}.jsonl"))
    row=rows[args.index];u=LineDictionary(args.n);p=LineDictionary(args.n,profiles=PROFILES)
    ur={int(k):v for k,v in row["methods"]["uniform"].items()};pr={int(k):v for k,v in row["methods"]["profiled"].items()}
    result,diag=fit_parametric(A[args.index][u.i,u.j],args.n,counts(args.n)["parametric"],u,p,ur,pr,
        SEED+args.n+row["archive_index"])
    def check(value,path="result"):
        if isinstance(value,dict):
            for k,v in value.items():check(v,path+"/"+str(k))
        elif isinstance(value,list):
            for k,v in enumerate(value):check(v,path+"/"+str(k))
        elif isinstance(value,float) and not np.isfinite(value):print('NONFINITE',path,value,flush=True)
    check(result);check(diag,"diagnostics")
    print('finished debug',diag,flush=True)


if __name__=="__main__":main()
