"""Linux coordinator for FP32 E9. Each stage owns/releases its own flock."""
import json,subprocess,time
from pathlib import Path
from datetime import datetime,timezone

PY='.venv/Scripts/python.exe'
MODELS=json.loads(Path('out/phase50_protocol.json').read_text())['models']
def slug(m):return m.replace('/','__')

def stage(label,args,gpu=True):
    log=Path('out/phase50_fp32_'+label+'_execution.log')
    if log.exists():
        i=2
        while log.with_name(log.stem+'_attempt'+str(i)+log.suffix).exists():i+=1
        log=log.with_name(log.stem+'_attempt'+str(i)+log.suffix)
    cmd=(["flock","/tmp/radon-gpu.lock"] if gpu else [])+[PY,'-B']+args+(['--under-gpu-lock'] if gpu else [])
    event={'UTC':datetime.now(timezone.utc).isoformat(),'event':'start','stage':label,'command':cmd,'log':str(log)}
    with open('out/pairs/phase50_fp32_run_events.jsonl','a') as out:out.write(json.dumps(event)+'\n')
    print('START',label,'lock released by prior stage',flush=True);tick=time.perf_counter()
    with log.open('x') as out:result=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT)
    event.update(event='end',exit_code=result.returncode,wall_seconds_including_lock_wait=time.perf_counter()-tick)
    with open('out/pairs/phase50_fp32_run_events.jsonl','a') as out:out.write(json.dumps(event)+'\n')
    print('END',label,result.returncode,'wall',event['wall_seconds_including_lock_wait'],flush=True)
    if result.returncode:raise RuntimeError('Stage failed; log preserved: '+str(log))

def main():
    controls=json.loads(Path('out/phase50_fp32_controls.json').read_text())
    if not controls['passed']:raise ValueError('FP32 controls failed')
    for model in MODELS:
        if not Path(f'out/phase50_fp32_validation_{slug(model)}.json').exists():
            stage('validation_'+slug(model),['phase50_fp32_validate.py','--model',model])
    for model in MODELS:
        if not Path(f'out/phase50_fp32_timing_{slug(model)}.json').exists():
            stage('timing_'+slug(model),['phase50_fp32_forward.py','timing','--model',model])
    if not Path('out/phase50_fp32_sample.json').exists():stage('sample',['phase50_fp32_forward.py','sample'],False)
    for model in MODELS:
        if not Path(f'out/phase50_fp32_forward_{slug(model)}.json').exists():
            stage('forward_'+slug(model),['phase50_fp32_forward.py','forward','--model',model])
    stage('report',['phase50_fp32_report.py'],False)
    print('FP32 E9 processing finished; see out/phase50_report.json for qualification/completeness',flush=True)

if __name__=='__main__':main()
