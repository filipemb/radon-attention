"""E2 extensions: parameter audit, thin primitives, and ranks8/16 budgets.

Three CPU workers: python phase19b_runner.py cpu --slot {0,1,2}.
Optional CUDA worker: launch phase19b_gpu_launcher.py under the global flock,
with the native CPU slot2 PID and creation time, to retain three active workers.
This CLI provides status, final aggregation and integrity audit. Existing
phase19 inputs are read only. New outputs use the phase19b prefix exclusively.
"""
import phase19b_common
import argparse,json
from pathlib import Path
from phase19b_common import ROOT,prepare,read_json,progress,cache_path


def status():
    selection=prepare();parent=read_json('out/phase19_selection.json')
    counts={k:sum(1 for p in (ROOT/k).glob('*.json')) for k in ['controls','init','original','free','thin']}
    errors=[]
    for p in [*Path('out/_rerun_logs').glob('phase19b_cpu_slot*.log'),Path('out/_rerun_logs/phase19b_gpu.log')]:
        if p.exists() and any(t in p.read_text(errors='replace') for t in ['Traceback','AssertionError','FloatingPointError','ValueError']):errors.append(str(p))
    return {'counts':counts,'targets':{'controls':128,'init':192,'original':768,'free':192,'thin':192},
        'errors':errors,'complete':all(counts[k]==v for k,v in {'controls':128,'init':192,'original':768,'free':192,'thin':192}.items()),
        'result_exists':Path('out/phase19b_richlines.json').exists()}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','status','aggregate','audit'],nargs='?',default='status');args=ap.parse_args()
    if args.mode=='prepare':prepare()
    elif args.mode=='status':print(json.dumps(status(),indent=2))
    elif args.mode=='aggregate':
        from phase19b_analysis import aggregate
        aggregate()
    else:
        from phase19b_audit import audit
        print(json.dumps(audit(),indent=2))


if __name__=='__main__':main()
