"""Read-only progress for the user-declared FP32 E9 continuation."""
import json,sys
from pathlib import Path
from datetime import datetime,timezone

def main():
    dec=json.loads(Path('out/phase50_declared_fp32_decision.json').read_text());res={}
    for model in dec['models']:
        path=Path(f'out/pairs/phase50_declared_forward_{model.replace("/","__")}.jsonl')
        counts={}
        if path.exists():
            lines=path.read_bytes().splitlines(keepends=True)
            if lines and not lines[-1].endswith(b'\n'):lines=lines[:-1]  # Monitoring only; scientific readers remain strict.
            for line in lines:
                row=json.loads(line);key=row['arm']+':'+str(row['K']);counts[key]=counts.get(key,0)+1
        res[model]=counts
    ev=Path('out/pairs/phase50_declared_events.jsonl')
    events=ev.read_text().splitlines() if ev.exists() else []
    last=json.loads(events[-1]) if events else None
    if '--compact' in sys.argv:
        for model,counts in res.items():
            expected=['masked_K','named_plus_masked']+(['masked_K_diag_exact','svd_K_diag_exact_empty_stats_replay'] if dec['heads_exact_zero_based'][model] else [])
            minimum=min((counts.get(a+':'+str(k),0) for a in expected for k in (8,16)),default=0)
            print(model,minimum,'/64 complete across required arms/K')
        print('stage',None if last is None else last['stage'],None if last is None else last['event'],'finished',Path('out/phase50_declared_finished.json').exists())
    else:
        print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'articles_by_arm_K':res,
            'last_event':last,'finished':Path('out/phase50_declared_finished.json').exists(),
            'failed_events':[json.loads(line) for line in events if json.loads(line).get('event')=='end' and json.loads(line).get('exit_code',0)!=0]},indent=2))

if __name__=='__main__':main()
