"""New E2c outputs, immutable parent inputs and four-thread resource limits."""
from __future__ import annotations
import os
for key in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS","NUMBA_NUM_THREADS"):
    os.environ[key]="4"
os.environ["OMP_WAIT_POLICY"]="PASSIVE"
os.environ["KMP_BLOCKTIME"]="0"
os.environ["NUMBA_CACHE_DIR"]=os.path.abspath("out/phase19c_numba_cache")
import hashlib,json,time
from pathlib import Path
import numpy as np

SEED=19027
ROOT=Path("out/phase19c_cache")
RANKS=(1,2,4,8,16)

def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def read_jsonl(path):return [json.loads(s) for s in Path(path).read_text(encoding="utf-8").splitlines() if s.strip()]
def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8") as f:json.dump(value,f,indent=2,allow_nan=False);f.write("\n")
def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def progress(message):
    p=Path("out/_rerun_logs/phase19c_progress.md");p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f:f.write(time.strftime("- %Y-%m-%d %H:%M:%S ")+message+"\n")
    print(message,flush=True)
def budgets(n,ranks=RANKS):return [(2*n+1)*r for r in ranks]
def old_counts(n):return sorted(set((1,2,4,8,16,32))|{b//5 for b in budgets(n,(1,2,4))})
def tag(model,n,index):return f"{model}_n{n}_i{index}"
def cache_path(kind,model,n,index):return ROOT/kind/(tag(model,n,index)+".json")
def identity(row):return {k:row[k] for k in ("archive_index","instance_id","document_index","doc_id","layer","head","offset","n","model","model_slug")}
def load_dataset(record):
    p=Path("data/attn")/f"{record['model_slug']}_n{record['n']}.npz"
    if digest(p)!=record["npz_sha256_expected"] or digest(p.with_suffix('.manifest.json'))!=record["manifest_sha256"]:
        raise ValueError("Archived input or manifest changed")
    with np.load(p,allow_pickle=False) as z:
        a=z["attention"][[s["archive_index"] for s in record["instances"]]].astype(float)
        for s in record["instances"]:
            for name in ("layer","head","document_index"):
                if int(z[name][s["archive_index"]])!=s[name]:raise AssertionError("Manifest identity mismatch")
    if not np.isfinite(a).all() or np.any(a<0) or np.any(np.triu(a,1)):raise ValueError("Invalid archived attention")
    return a
