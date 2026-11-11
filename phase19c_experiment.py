"""E2c: masked ALS, causal nulls, paired effects, planted segments and binary16.

Frozen final protocol: phase19c_freeze.py. CPU workers: phase19c_run.py cpu
--slot N for N=0,1,2. Optional GPU uses phase19c_gpu_v2.py
under the global flock, replacing the verified CPU slot2 process temporarily.
"""
import phase19c_common
import argparse,json
from pathlib import Path
ROOT=Path("out/phase19c_v2_cache")

EXPECTED={"masked_positive":80,"negative_init":66,"negative_free":66,"negative_thin":66,
    "planted_init":96,"planted_free":96,"planted_thin":96,"baseline":768,"thin768":768}

def status():
    counts={k:len(list((ROOT/k).glob('*.json'))) for k in EXPECTED}
    errors=[]
    for p in Path('out/_rerun_logs').glob('phase19c_v2_worker*.log'):
        if any(s in p.read_text(errors='replace') for s in ['Traceback','AssertionError','FloatingPointError','ValueError']):errors.append(str(p))
    return {"counts":counts,"targets":EXPECTED,"complete":counts==EXPECTED,"errors":errors,
        "result_exists":Path('out/phase19c_richlines.json').exists()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['status','aggregate','audit'],nargs='?',default='status');args=ap.parse_args()
    if args.mode=='status':print(json.dumps(status(),indent=2))
    elif args.mode=='aggregate':
        from phase19c_analysis import aggregate
        aggregate()
    else:
        from phase19c_audit import audit
        print(json.dumps(audit(),indent=2))

if __name__=='__main__':main()
