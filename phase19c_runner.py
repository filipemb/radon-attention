"""Exclusive, resumable E2c case jobs; GPU used for parametric fitting only."""
import phase19c_common
import argparse,time
from pathlib import Path
import numpy as np
import torch
from filelock import FileLock,Timeout
from richlines_core import LineDictionary,PROFILES,omp
from phase19c_common import (ROOT,SEED,RANKS,read_json,read_jsonl,write_json,digest,progress,
    cache_path,tag,identity,old_counts,budgets,load_dataset)
from phase19c_als import fit as fit_masked,svd_models,errors
from phase19c_fit import fit_parametric
from phase19c_metrics import line_result,factor_precision,line_image
from phase19c_synthetic import make,freeze_decay_pool


def path_for(kind,key):
    if isinstance(key,tuple):return cache_path(kind,*key)
    return ROOT/kind/(key+".json")


class Worker:
    def __init__(self,device,slot):
        self.device=device;self.slot=slot;self.protocol=read_json("out/phase19c_protocol.json")
        self.records=read_json("out/phase19_selection.json")["datasets"]
        selected=read_json("out/phase19b_selection.json")["datasets"]
        self.extension={(d["model_slug"],d["n"],s["archive_index"]) for d in selected for s in d["instances"]}
        self.keys=[(d["model_slug"],d["n"],s["archive_index"]) for d in self.records for s in d["instances"]]
        self.datasets={};self.dictionaries={};self.pool=freeze_decay_pool()
        self.specs={s["id"]:s for rows in self.protocol["synthetic_specs"].values() for s in rows}

    def dictionaries_for(self,n):
        if n not in self.dictionaries:self.dictionaries[n]=(LineDictionary(n),LineDictionary(n,profiles=PROFILES))
        return self.dictionaries[n]

    def data(self,key):
        model,n,index=key
        if (model,n) not in self.datasets:
            record=next(d for d in self.records if d["model_slug"]==model and d["n"]==n)
            a=load_dataset(record);parent=read_jsonl(f"out/phase19_cpu_{model}_n{n}.jsonl")
            expected=[s["instance_id"] for s in record["instances"]]
            if [s["instance_id"] for s in parent]!=expected:raise AssertionError("Parent OMP identities differ")
            self.datasets[(model,n)]=(a,parent,{s["archive_index"]:i for i,s in enumerate(record["instances"])})
        a,parent,lookup=self.datasets[(model,n)];q=lookup[index]
        return a[q],parent[q]

    def baselines(self,a,ranks):
        svd,decomposition=svd_models(a,ranks)
        masked={r:fit_masked(a,r,svd=decomposition) for r in ranks}
        for r in ranks:
            factor_precision(svd[r],a);factor_precision(masked[r],a,masked=True)
        return svd,masked

    def fitted(self,a,counts,ur,pr,seed,cap):
        n=len(a);u,p=self.dictionaries_for(n);b=a[u.i,u.j]
        result,diag=fit_parametric(b,n,counts,u,p,ur,pr,seed,device=self.device,
            iterations=450,refine_iterations=150,return_parameters=True,sigma_max=cap)
        return result,diag

    def process(self,kind,key):
        if kind=="baseline":
            a,row=self.data(key);model,n,index=key;ranks=RANKS if key in self.extension else (1,2,4)
            svd,masked=self.baselines(a,ranks);old=read_json(f"out/phase19b_cache/original/{tag(*key)}.json")
            free={};historical={}
            for B in budgets(n,(1,2,4)):
                p=old["budget"][str(B)];free[str(B)]=line_result(p["parameters"],a)
                delta=abs(free[str(B)]["relative"]-p["relative"])
                if delta>1e-9:raise AssertionError("Independent phase19c render differs from parent state")
                historical[str(B)]={"relative":p["phase19_reference_relative"],"absolute":p["phase19_reference_absolute"]}
            extension={}
            if key in self.extension:
                for arm in ("free","thin"):
                    source=read_json(f"out/phase19b_cache/{arm}/{tag(*key)}.json")
                    extension[arm]={}
                    for B,p in source["budget"].items():
                        result=line_result(p["parameters"],a)
                        if abs(result["relative"]-p["relative"])>1e-9:raise AssertionError("Extension render differs")
                        extension[arm][B]={**result,"parent_converged":p["converged"],"parent_best_start":p["best_start"]}
            return {**identity(row),"svd":svd,"masked":masked,"free768":free,"free_historical":historical,
                "free768_parameter_provenance":old["parameter_provenance"],"extension192":extension}
        if kind=="thin768":
            a,row=self.data(key);n=len(a);u,p=self.dictionaries_for(n)
            ur={int(k):v for k,v in row["methods"]["uniform"].items()};pr={int(k):v for k,v in row["methods"]["profiled"].items()}
            results,diag=self.fitted(a,old_counts(n),ur,pr,SEED+n+key[2],2)
            source=read_json(f"out/phase19b_cache/original/{tag(*key)}.json")
            expected=source["diagnostics"].get("initialization_hashes_before_width_projection")
            if expected is not None and expected!=diag["initialization_hashes_before_width_projection"]:
                raise AssertionError("New thin768 starts differ from original-grid free replay")
            rows={}
            for B in budgets(n,(1,2,4)):
                fit=results[B//5];rows[str(B)]={**fit,**line_result(fit["parameters"],a),"optimization_relative":fit["relative"]}
            return {**identity(row),"budget":rows,"diagnostics":diag,"initial_hash_verified_against_replay":expected is not None}
        spec=self.specs[key];a,generation=make(spec,self.pool);n=len(a)
        if kind=="masked_positive":
            fit=fit_masked(a,spec["rank"]);factor_precision(fit,a,masked=True)
            exact=errors(a,np.tril(np.asarray(generation["latent_U"])@np.asarray(generation["latent_V"]).T))
            return {**spec,"generation":generation,"fit":fit,"oracle_exact_representation_error":exact,
                "recovered":fit["relative"]<=1e-6,"threshold":1e-6}
        if kind in ("negative_init","planted_init"):
            u,p=self.dictionaries_for(n);counts=old_counts(n) if kind=="negative_init" else [spec["k"]]
            b=a[u.i,u.j];ur,ud=omp(b,u,counts,save_support=True);pr,pd=omp(b,p,counts,save_support=True)
            output={**spec,"generation":generation,"matrix_sha256":__import__('hashlib').sha256(a.tobytes()).hexdigest(),
                "uniform":ur,"profiled":pr,"diagnostics":{"uniform":ud,"profiled":pd}}
            if kind=="negative_init":output["svd"],output["masked"]=self.baselines(a,(1,2,4))
            return output
        group,arm=kind.split("_",1)
        if group not in ("negative","planted") or arm not in ("free","thin"):raise ValueError(kind)
        init=read_json(path_for(group+"_init",key))
        if __import__('hashlib').sha256(a.tobytes()).hexdigest()!=init["matrix_sha256"]:raise AssertionError("Synthetic target changed")
        ur={int(k):v for k,v in init["uniform"].items()};pr={int(k):v for k,v in init["profiled"].items()}
        counts=old_counts(n) if group=="negative" else [spec["k"]]
        results,diag=self.fitted(a,counts,ur,pr,spec.get("fit_seed",spec["seed"]+700000),n if arm=="free" else 2)
        rows={}
        for B in budgets(n,(1,2,4)) if group=="negative" else [5*spec["k"]]:
            fit=results[B//5];rows[str(B)]={**fit,**line_result(fit["parameters"],a),"optimization_relative":fit["relative"]}
        threshold=.001 if spec.get("noise",0)==0 else .02
        return {**spec,"generation":generation,"arm":arm,"budget":rows,"diagnostics":diag,
            "recovered":rows[str(5*spec["k"])]["relative"]<=threshold if group=="planted" else None,
            "threshold":threshold if group=="planted" else None}

    def candidates(self):
        plan=self.protocol["synthetic_specs"]
        if self.device=="cuda":
            for group in ("negative","planted"):
                for spec in plan[group]:
                    if path_for(group+"_init",spec["id"]).exists():
                        for arm in ("free","thin"):yield group+"_"+arm,spec["id"]
            for key in self.keys:yield "thin768",key
        else:
            for spec in plan["masked_positive"]:yield "masked_positive",spec["id"]
            for group in ("negative","planted"):
                for spec in plan[group]:yield group+"_init",spec["id"]
            for key in self.keys:yield "baseline",key
            for key in self.keys:yield "thin768",key
            for group in ("negative","planted"):
                for spec in plan[group]:
                    if path_for(group+"_init",spec["id"]).exists():
                        for arm in ("free","thin"):yield group+"_"+arm,spec["id"]

    def run(self):
        while True:
            found=False
            for kind,key in self.candidates():
                path=path_for(kind,key)
                if path.exists():continue
                path.parent.mkdir(parents=True,exist_ok=True);lease=FileLock(str(path)+".lock")
                try:lease.acquire(timeout=0)
                except Timeout:continue
                try:
                    if path.exists():continue
                    begin=time.perf_counter();result=self.process(kind,key)
                    result["execution"]={"device":self.device,"slot":self.slot,"elapsed_seconds":time.perf_counter()-begin}
                    write_json(path,result);found=True
                    progress(f"phase19c {self.device} slot={self.slot} {kind} {key}: {result['execution']['elapsed_seconds']:.1f}s")
                finally:lease.release()
                if found:break
            if not found:
                if self.device=="cuda":progress("phase19c GPU no ready unleased c work; releasing GPU");return
                from phase19c_richlines import status
                if status()["complete"]:progress(f"phase19c CPU slot={self.slot} complete");return
                time.sleep(5)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("mode",choices=["cpu","gpu"]);ap.add_argument("--slot",type=int,default=0);args=ap.parse_args()
    torch.set_num_threads(4);torch.set_num_interop_threads(4)
    protocol=read_json("out/phase19c_protocol.json")
    for p,h in protocol["numeric_sources_sha256"].items():
        if digest(p)!=h:raise AssertionError(f"Frozen E2c source changed: {p}")
    if args.mode=="gpu":
        import os
        if os.environ.get("RICHLINE_GPU_LOCK")!="1":raise RuntimeError("GPU requires external flock")
        from phase19c_cuda import check_cuda_renderer
        check_cuda_renderer()
    Worker("cuda" if args.mode=="gpu" else "cpu",args.slot).run()

if __name__=="__main__":main()
