"""Execute frozen64 FP32 forward in16-article chunks, sharing the GPU with E6."""
import argparse,json,subprocess,time
from datetime import datetime,timezone
from pathlib import Path

PY='.venv/Scripts/python.exe'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def slug(m):return m.replace('/','__')

def stage(label,args,gpu=True):
    log=Path(f'out/phase50_declared_{label}_execution.log')
    if log.exists():
        i=2
        while log.with_name(log.stem+f'_attempt{i}.log').exists():i+=1
        log=log.with_name(log.stem+f'_attempt{i}.log')
    cmd=(['flock','/tmp/radon-gpu.lock'] if gpu else [])+[PY,'-B']+args+(['--under-gpu-lock'] if gpu else [])
    ev={'UTC':datetime.now(timezone.utc).isoformat(),'event':'start','stage':label,'command':cmd,'log':log.as_posix()}
    with open('out/pairs/phase50_declared_events.jsonl','a',encoding='utf-8') as out:out.write(json.dumps(ev)+'\n')
    print('START',label,flush=True);tick=time.perf_counter()
    with log.open('x',encoding='utf-8') as out:proc=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT)
    ev.update(UTC=datetime.now(timezone.utc).isoformat(),event='end',exit_code=proc.returncode,wall_seconds_including_lock_wait=time.perf_counter()-tick)
    with open('out/pairs/phase50_declared_events.jsonl','a',encoding='utf-8') as out:out.write(json.dumps(ev)+'\n')
    print('END',label,proc.returncode,ev['wall_seconds_including_lock_wait'],flush=True)
    if proc.returncode:raise RuntimeError('Failed stage, preserved log: '+str(log))

def main(skip_models=(),only_models=()):
    dec=read('out/phase50_declared_fp32_decision.json')
    unknown=(set(skip_models)|set(only_models))-set(dec['models'])
    if unknown:raise ValueError('Unknown model selection: '+str(sorted(unknown)))
    selected=[m for m in dec['models'] if m not in skip_models and (not only_models or m in only_models)]
    if not read('out/phase50_declared_empty_counter_control.json')['passed']:raise AssertionError('Empty-row counter control did not pass')
    for start in range(0,64,16):
        for model in selected:
            chunk=Path(f'out/phase50_declared_chunk_{slug(model)}_{start:03d}_{start+16:03d}.json')
            if chunk.exists():continue
            stage(f'{slug(model)}_{start:03d}_{start+16:03d}',
                ['phase50_declared_forward.py','chunk','--model',model,'--start',str(start),'--stop',str(start+16)])
    for model in selected:
        if not Path(f'out/phase50_declared_forward_{slug(model)}.json').exists():
            stage('finalize_'+slug(model),['phase50_declared_forward.py','finalize','--model',model],False)
    missing=[m for m in dec['models'] if not Path(f'out/phase50_declared_forward_{slug(m)}.json').exists()]
    if missing:
        print('PENDING models; complete report will not be published:',missing,flush=True);return
    if not Path('out/phase50_declared_finished.json').exists():stage('report',['phase50_declared_report.py'],False)
    print('Declared FP32 E9 complete: out/phase50_report.json',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--temporarily-skip-model',action='append',default=[])
    ap.add_argument('--only-model',action='append',default=[]);arg=ap.parse_args()
    main(arg.temporarily_skip_model,arg.only_model)
