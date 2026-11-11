"""Run optional, explicitly exploratory CPU audits as validations finish."""
import json,subprocess,time
from pathlib import Path

def main():
    models=json.loads(Path('out/phase50_fp32_protocol.json').read_text())['models']
    for m in models:
        s=m.replace('/','__')
        while not Path(f'out/phase50_fp32_validation_{s}.json').exists():time.sleep(5)
        if Path(f'out/phase50_fp32_failure_audit_{s}.json').exists():continue
        p=Path(f'out/phase50_fp32_failure_audit_{s}_execution.log')
        with p.open('x') as out:
            subprocess.run(['.venv/Scripts/python.exe','-B','phase50_fp32_failure_audit.py','--model',m],stdout=out,stderr=subprocess.STDOUT,check=True)
        print('CPU audit finished',m,flush=True)

if __name__=='__main__':main()
