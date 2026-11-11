"""Resumable E2b jobs, with exclusive per-case leases and no old writes."""
import phase19b_common
import argparse,time
from pathlib import Path
import numpy as np
import torch
from filelock import FileLock,Timeout
from richlines_core import LineDictionary,PROFILES,svd_errors
from phase19b_common import (SEED,ROOT,PROTOCOL,RANKS,read_json,write_json,progress,
    prepare,parent_record,load_dataset,cache_path,all_counts,old_counts,line_counts,budgets,digest)
from phase19b_fit import fit_parametric
from phase19b_stats import decoded_statistics
from phase19b_omp import extend
from phase19b_controls import run as controls_run,targets


def controls_complete():
    marker=Path("out/phase19b_controls_complete.json")
    if marker.exists():return True
    paths=[ROOT/"controls"/f"n{n}_i{i}.json" for n in (128,256) for i in range(64)]
    if not all(p.exists() for p in paths):return False
    lease=FileLock(str(marker)+".lock")
    try:lease.acquire(timeout=0)
    except Timeout:return False
    try:
        if not marker.exists():
            rows=[read_json(p) for p in paths]
            if len({(r["n"],r["index"]) for r in rows})!=128:raise AssertionError("Repeated control identity")
            write_json(marker,{"complete":True,"cases":128,"arms":["free","thin"],
                "thresholds":{"clean":.001,"noise_0.01":.02,"minimum_group_success_rate":.9},
                "successes":{a:sum(r["gate_success"][a] for r in rows) for a in ("free","thin")},
                "policy":"All failures retained; no threshold, seed or optimizer change"})
    finally:lease.release()
    return True


def identity(row):
    return {k:row[k] for k in ("archive_index","instance_id","document_index","doc_id","layer","head","offset","n","model","model_slug")}


class Worker:
    def __init__(self,device,slot):
        self.device=device;self.slot=slot;self.datasets={};self.dictionaries={}
        selection=prepare();self.selected={(r["model_slug"],r["n"]):r["instances"] for r in selection["datasets"]}
        parent=read_json("out/phase19_selection.json");self.original=[];self.extension=[]
        self.parent_parameter_flags={}
        for record in parent["datasets"]:
            from phase19b_common import read_jsonl
            fitted=read_jsonl(Path('out')/f"phase19_gpu_stable_{record['model_slug']}_n{record['n']}.jsonl")
            for row,old in zip(record["instances"],fitted):
                key=(record["model_slug"],record["n"],row["archive_index"]);self.original.append(key)
                self.parent_parameter_flags[key]=("parameters" in next(iter(old["methods"]["parametric"].values())),old["diagnostics"]["device"])
        for record in selection["datasets"]:
            for row in record["instances"]:self.extension.append((record["model_slug"],record["n"],row["archive_index"]))

    def data(self,key):
        model,n,index=key
        if (model,n) not in self.datasets:
            record,A,cpu,fitted=load_dataset(model,n)
            self.datasets[(model,n)]=(record,A,cpu,fitted,{r["archive_index"]:i for i,r in enumerate(record["instances"])})
        record,A,cpu,fitted,lookup=self.datasets[(model,n)];q=lookup[index]
        if n not in self.dictionaries:self.dictionaries[n]=(LineDictionary(n),LineDictionary(n,profiles=PROFILES))
        u,p=self.dictionaries[n]
        return A[q],cpu[q],fitted[q],u,p

    def process(self,kind,key):
        model,n,index=key;matrix,row,old,u,p=self.data(key);b=matrix[u.i,u.j]
        if kind=="init":
            ur,ud=extend(b,u,row["methods"]["uniform"],all_counts(n))
            pr,pd=extend(b,p,row["methods"]["profiled"],all_counts(n))
            sv=svd_errors(matrix,RANKS)
            delta=max(abs(sv[r]["relative"]-row["methods"]["svd"][str(r)]["relative"]) for r in RANKS)
            if delta>1e-10:raise AssertionError("SVD differs on the same archived instance")
            return {**identity(row),"uniform":ur,"profiled":pr,"svd":sv,
                "diagnostics":{"uniform":ud,"profiled":pd,"svd_parent_max_delta":delta}}
        if kind=="original":
            saved=all("parameters" in old["methods"]["parametric"][str(k)] for k in line_counts(n)[:3])
            if saved:
                fitted=old["methods"]["parametric"];diag=old["diagnostics"]
                provenance="original_phase19_export"
            else:
                ur={int(k):v for k,v in row["methods"]["uniform"].items()}
                pr={int(k):v for k,v in row["methods"]["profiled"].items()}
                fitted,diag=fit_parametric(b,n,old_counts(n),u,p,ur,pr,SEED+n+index,
                    device=self.device,iterations=450,refine_iterations=150,return_parameters=True,
                    sigma_max=n,legacy_bounds=True)
                fitted={str(k):v for k,v in fitted.items()};provenance="phase19_settings_replayed_parameters_not_original_snapshot"
            outputs={}
            for B,k in zip(budgets(n)[:3],line_counts(n)[:3]):
                fit=fitted[str(k)];stats=decoded_statistics(fit["parameters"],n,b)
                reference=old["methods"]["parametric"][str(k)]
                outputs[str(B)]={**stats,"components":k,"stored_numbers":5*k,
                    "parameter_provenance":provenance,"phase19_reference_relative":reference["relative"],
                    "phase19_reference_absolute":reference["absolute"],"optimization_relative":fit["relative"],
                    "optimization_error_delta_from_phase19":fit["relative"]-reference["relative"],
                    "decoded_error_delta_from_phase19":stats["relative"]-reference["relative"]}
            return {**identity(row),"budget":outputs,"parameter_provenance":provenance,
                "reference_phase19_backend":old["diagnostics"]["device"],"diagnostics":diag}
        if kind not in ("free","thin"):raise ValueError(kind)
        if not controls_complete():raise RuntimeError("Extension fits require complete planted controls")
        init=read_json(cache_path("init",*key));ur={int(k):v for k,v in init["uniform"].items()};pr={int(k):v for k,v in init["profiled"].items()}
        cap=n if kind=="free" else 2
        fitted,diag=fit_parametric(b,n,all_counts(n),u,p,ur,pr,SEED+n+index,
            device=self.device,iterations=450,refine_iterations=150,return_parameters=True,sigma_max=cap)
        outputs={}
        for B,k in zip(budgets(n),line_counts(n)):
            fit=fitted[k];params=np.asarray(fit["parameters"])
            if (params[:,2]<.2-1e-12).any() or (params[:,2]>cap+1e-12).any():raise AssertionError("Infeasible fitted width")
            stats=decoded_statistics(params,n,b)
            outputs[str(B)]={**fit,**stats,"optimization_relative":fit["relative"],"optimization_absolute":fit["absolute"],
                "components":k,"stored_numbers":5*k}
        return {**identity(row),"arm":kind,"budget":outputs,"diagnostics":diag,
                "svd":init["svd"],"parameter_provenance":"new_paired_extension_fit"}

    def candidates(self):
        # Availability determines backend; no fitted error is read to select it.
        if self.device=="cuda":
            for key in sorted(self.extension,key=lambda x:-x[1]):
                if cache_path("init",*key).exists() and controls_complete():yield "free",key
            for key in sorted(self.original,key=lambda x:-x[1]):
                saved,original_device=self.parent_parameter_flags[key]
                if not saved and original_device=="cuda":yield "original",key
            for key in self.extension:
                if cache_path("init",*key).exists() and controls_complete():yield "thin",key
        else:
            if controls_complete():
                for key in self.extension:
                    if cache_path("init",*key).exists():yield "thin",key
            for key in self.extension:yield "init",key
            for key in self.original:yield "original",key
            if controls_complete():
                for key in self.extension:
                    if cache_path("init",*key).exists():yield "free",key

    def run(self):
        while True:
            found=False
            for kind,key in self.candidates():
                path=cache_path(kind,*key)
                if path.exists():continue
                path.parent.mkdir(parents=True,exist_ok=True);lease=FileLock(str(path)+".lock")
                try:lease.acquire(timeout=0)
                except Timeout:continue
                try:
                    if path.exists():continue
                    begin=time.perf_counter();result=self.process(kind,key)
                    result["execution"]={"worker_slot":self.slot,"device":self.device,"seconds":time.perf_counter()-begin,
                        "source_protocol":"out/phase19b_protocol.json"}
                    write_json(path,result);found=True
                    progress(f"phase19b {self.device} slot={self.slot} {kind} {key}: {result['execution']['seconds']:.1f}s")
                finally:lease.release()
                if found:break
            if not found:
                if self.device=="cuda":
                    progress("phase19b CUDA: no ready unleased work; releasing shared GPU")
                    return
                complete=all(cache_path(kind,*key).exists() for key in self.extension for kind in ("init","free","thin"))
                complete&=all(cache_path("original",*key).exists() for key in self.original)
                if complete:
                    progress(f"phase19b CPU slot={self.slot}: all work complete")
                    return
                time.sleep(5)


def main():
    ap=argparse.ArgumentParser();ap.add_argument("mode",choices=["cpu","gpu"]);ap.add_argument("--slot",type=int,default=0)
    args=ap.parse_args();torch.set_num_threads(4);torch.set_num_interop_threads(4)
    protocol=read_json(PROTOCOL)
    if any(digest(p)!=v for p,v in protocol["numeric_source_sha256"].items()):raise ValueError("Numeric sources changed after freeze")
    if args.mode=="gpu":
        import os
        if os.environ.get("RICHLINE_GPU_LOCK")!="1":raise RuntimeError("Launch GPU worker under flock /tmp/radon-gpu.lock")
        from phase19b_cuda import check_cuda_renderer
        check_cuda_renderer();Worker("cuda",args.slot).run()
    else:
        controls_run(args.slot);controls_complete();Worker("cpu",args.slot).run()


if __name__=="__main__":main()
