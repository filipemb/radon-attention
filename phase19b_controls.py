"""Same planted trials and noise seeds; truth widths mapped into [0.6,2]."""
import phase19b_common
import numpy as np
import torch
from pathlib import Path
from filelock import FileLock,Timeout
from richlines_core import LineDictionary,PROFILES,omp
from richlines_parametric import render_numpy
from phase19b_fit import fit_parametric
from phase19b_common import read_json,write_json,progress,ROOT


def targets(n):
    source=read_json(f"out/phase19_controls_cpu_n{n}.json");cases=[]
    for index,old in enumerate(source["parametric_cases"]):
        truth=np.asarray(old["truth"],dtype=float)
        u=np.log(truth[:,2]/.6)/np.log(4/.6)
        truth[:,2]=.6*np.exp(u*np.log(2/.6))
        if (truth[:,2]>2+1e-12).any():raise AssertionError("Thin planted truth exceeds two pixels")
        cases.append({"index":index,"k":old["k"],"trial":old["trial"],"noise":old["noise"],
            "truth":truth.tolist(),"noise_seed":old["noise_seed"],"fit_seed":old["fit_seed"]})
    return cases


def run(slot):
    dictionaries={}
    for n in (128,256):
        dictionaries[n]=(LineDictionary(n),LineDictionary(n,profiles=PROFILES))
    for n in (128,256):
        u,p=dictionaries[n]
        for case in targets(n):
            path=ROOT/"controls"/f"n{n}_i{case['index']}.json";path.parent.mkdir(parents=True,exist_ok=True)
            if path.exists():continue
            lease=FileLock(str(path)+".lock")
            try:lease.acquire(timeout=0)
            except Timeout:continue
            try:
                if path.exists():continue
                clean=render_numpy(case["truth"],n)
                z=np.random.default_rng(case["noise_seed"]).normal(size=len(clean));z/=np.linalg.norm(z)
                b=clean+case["noise"]*np.linalg.norm(clean)*z;k=case["k"]
                ur,ud=omp(b,u,[k],save_support=True);pr,pd=omp(b,p,[k],save_support=True)
                arms={};diagnostics={}
                for arm,cap in (("free",n),("thin",2)):
                    result,diag=fit_parametric(b,n,[k],u,p,ur,pr,case["fit_seed"],device="cpu",
                        iterations=450,refine_iterations=150,return_parameters=True,sigma_max=cap)
                    if np.max(np.asarray(result[k]["parameters"])[:,2])>cap+1e-12:
                        raise AssertionError("Optimizer exported an infeasible width")
                    arms[arm]=result[k];diagnostics[arm]=diag
                if diagnostics["free"]["initialization_hashes_before_width_projection"]!=diagnostics["thin"]["initialization_hashes_before_width_projection"]:
                    raise AssertionError("Arms do not share their preprojection starts")
                write_json(path,{**case,"n":n,"arms":arms,"diagnostics":diagnostics,
                    "threshold":.001 if case["noise"]==0 else .02,
                    "gate_success":{a:arms[a]["relative"]<=(.001 if case["noise"]==0 else .02) for a in arms}})
                progress(f"phase19b controls slot={slot} n={n} {case['index']+1}/64; k={k}; thin error={arms['thin']['relative']:.6g}")
            finally:lease.release()
    progress(f"phase19b controls slot={slot}: available control work finished")


if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument("--slot",type=int,default=0);args=ap.parse_args()
    torch.set_num_threads(4);torch.set_num_interop_threads(4);run(args.slot)
