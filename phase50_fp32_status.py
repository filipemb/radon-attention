"""Read-only stdlib progress; numerical failures are not completion claims."""
import json
from pathlib import Path
from datetime import datetime,timezone

def read(p):return json.loads(Path(p).read_text())

def main():
    protocol=read('out/phase50_fp32_protocol.json');models={}
    for m in protocol['models']:
        s=m.replace('/','__');r={}
        for label in ('validation','matrix','timing','forward'):
            p=Path(f'out/phase50_fp32_{label}_{s}.json')
            if not p.exists():r[label]=None;continue
            obj=read(p)
            keys={'validation':['passed','max_absolute_relative_error_difference','max_normalized_frobenius_difference','max_TV_difference','n_failed_fits'],
                'matrix':['n_matrices','elapsed_seconds'],'timing':['steady_batch_all_required_arms_seconds','estimate_256_seconds_with_20percent_margin'],
                'forward':['n_articles','arms_run','ALS_validation_passed']}[label]
            r[label]={k:obj[k] for k in keys}
        models[m]=r
    events=Path('out/pairs/phase50_fp32_run_events.jsonl').read_text().splitlines()
    result={'UTC':datetime.now(timezone.utc).isoformat(),'models':models,'last_event':json.loads(events[-1]),
        'sample':read('out/phase50_fp32_sample.json') if Path('out/phase50_fp32_sample.json').exists() else None,
        'report':Path('out/phase50_report.json').exists(),'finished':Path('out/phase50_fp32_finished.json').exists()}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
