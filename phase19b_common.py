"""Immutable inputs, predeclared sampling, and output paths for E2 extensions."""
from __future__ import annotations
import os
for key in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS","NUMBA_NUM_THREADS"):
    os.environ[key]="4"
os.environ["OMP_WAIT_POLICY"]="PASSIVE"
os.environ["KMP_BLOCKTIME"]="0"
os.environ["NUMBA_CACHE_DIR"]=os.path.abspath("out/phase19b_numba_cache")
import collections,hashlib,json,time
from pathlib import Path
import numpy as np

SEED=19027
RANKS=(1,2,4,8,16)
ROOT=Path("out/phase19b_cache")
SELECTION=Path("out/phase19b_selection.json")
PROTOCOL=Path("out/phase19b_protocol.json")


def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
    return h.hexdigest()


def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8") as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write("\n")


def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))


def read_jsonl(path):
    path=Path(path)
    if not path.exists():return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def progress(message):
    p=Path("out/_rerun_logs/phase19b_progress.md");p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f:f.write(f"- {time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    print(message,flush=True)


def budgets(n):return [(2*n+1)*r for r in RANKS]
def line_counts(n):return [b//5 for b in budgets(n)]
def old_counts(n):return sorted(set((1,2,4,8,16,32))|{b//5 for b in budgets(n)[:3]})
def all_counts(n):return sorted(set(old_counts(n))|set(line_counts(n)))
def tag(model,n,index):return f"{model}_n{n}_i{index}"
def cache_path(kind,model,n,index):return ROOT/kind/(tag(model,n,index)+".json")


def prepare():
    if SELECTION.exists():return read_json(SELECTION)
    source=read_json("out/phase19_selection.json");records=[]
    for record in source["datasets"]:
        model=record["model_slug"];n=record["n"]
        manifest=read_json(Path("data/attn")/f"{model}_n{n}.manifest.json")
        rng=np.random.default_rng(SEED+int.from_bytes(model.encode(),"little")%(2**32-SEED))
        quotas=[4]*4;head=collections.Counter();layer=collections.Counter();selected=[]
        remaining=list(record["instances"]);ties={r["instance_id"]:float(rng.random()) for r in remaining}
        # Four equal depth strata, four distinct documents per stratum. Within
        # strata prefer unrepresented layers, then balance heads; no errors read.
        while len(selected)<16:
            candidates=[r for r in remaining if quotas[min(3,4*r["layer"]//manifest["n_layers"])]>0]
            if not candidates:raise ValueError("Manifest cannot supply the predeclared strata")
            pick=min(candidates,key=lambda r:(layer[r["layer"]],head[r["head"]],ties[r["instance_id"]]))
            selected.append(pick);remaining.remove(pick)
            quotas[min(3,4*pick["layer"]//manifest["n_layers"])]-=1
            layer[pick["layer"]]+=1;head[pick["head"]]+=1
        selected.sort(key=lambda r:r["archive_index"])
        if len({r["doc_id"] for r in selected})!=16:raise ValueError("Repeated selected document")
        records.append({"model_slug":model,"model":record["model"],"n":n,
            "instances":selected,"layer_counts":dict(layer),"head_counts":dict(head),
            "depth_stratum_counts":[sum(min(3,4*r["layer"]//manifest["n_layers"])==b for r in selected) for b in range(4)]})
    result={"seed":SEED,"fixed_before_any_extension_attention_fit":True,"n_instances":192,
        "instances_per_model_n":16,"parent_n_instances":768,
        "parent_selection_sha256":digest("out/phase19_selection.json"),
        "design":"four equal layer-depth strata, four documents each; balance layer/head coverage; seeded ties; same identities for free, thin, SVD and all five budgets",
        "cost_reason":"The measured phase19 CPU n256 fit is about 100s for sum(k)=780; the enlarged union has sum(k)=3241 and two arms. Even without initialization and replay costs, 768 cases exceed six hours with three CPU workers. Use all 768 for parameter diagnostics and a fixed 192 for extensions.",
        "datasets":records}
    write_json(SELECTION,result);progress("PHASE19B selection fixed: 16/model x n = 192 instances; all 768 retained for original-budget parameter diagnostics")
    return result


def parent_record(model,n):
    return next(r for r in read_json("out/phase19_selection.json")["datasets"] if r["model_slug"]==model and r["n"]==n)


def load_dataset(model,n):
    record=parent_record(model,n);p=Path("data/attn")/f"{model}_n{n}.npz"
    if digest(p)!=record["npz_sha256_expected"] or digest(p.with_suffix('.manifest.json'))!=record["manifest_sha256"]:
        raise ValueError("Input archive or manifest changed")
    with np.load(p,allow_pickle=False) as z:
        arrays=z["attention"]
        if not np.isfinite(arrays).all() or (arrays<0).any() or np.count_nonzero(np.triu(arrays,k=1)):
            raise ValueError("Invalid archived attention")
        selected=arrays[[r["archive_index"] for r in record["instances"]]].astype(float)
        for r in record["instances"]:
            for name in ("layer","head","document_index"):
                if int(z[name][r["archive_index"]])!=r[name]:raise ValueError("Manifest identity mismatch")
    cpu=read_jsonl(Path("out")/f"phase19_cpu_{model}_n{n}.jsonl")
    fitted=read_jsonl(Path("out")/f"phase19_gpu_stable_{model}_n{n}.jsonl")
    expected=[r["instance_id"] for r in record["instances"]]
    if [r["instance_id"] for r in cpu]!=expected or [r["instance_id"] for r in fitted]!=expected:
        raise ValueError("Parent cases do not match the 768-instance manifest")
    return record,selected,cpu,fitted


def frozen_inputs():
    # These are the complete phase19 artifacts indexed at the end of E2.
    index=read_json("out/phase19_artifacts.json");items=[]
    for key in ("sources","paired_results","other_json_reports","raw_case_caches","logs"):
        items.extend(index[key])
    items.append(index["main_result"])
    return {r["path"]:r["sha256"] for r in items}
