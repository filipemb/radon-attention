"""CPU metadata for structurally exact aliases; never acquires/uses the GPU.

When no head was selected, e is literally a. If masked ALS did not qualify,
there is no other new arm to run for that model. Avoid queuing a GPU no-op.
"""
import json,time,hashlib
from pathlib import Path

def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    while not Path('out/phase50_fp32_sample.json').exists():time.sleep(2)
    sample=read('out/phase50_fp32_sample.json');parent=read('out/phase50_protocol.json')
    for m in parent['models']:
        s=m.replace('/','__');cfg=parent['datasets'][m]
        if cfg['diagonal_heads'] or read(f'out/phase50_fp32_validation_{s}.json')['passed']:continue
        result=Path(f'out/phase50_fp32_forward_{s}.json');pairs=Path(f'out/pairs/phase50_fp32_forward_{s}.jsonl')
        if result.exists():continue
        if pairs.exists() and pairs.stat().st_size:raise ValueError('Unexpected partial real records in alias-only model')
        if not pairs.exists():pairs.touch(exist_ok=False)
        obj={'model':m,'n_articles':sample['n_articles_per_model_all_arms'],'arms_run':[],
            'ALS_validation_passed':False,'unavailable_arms':['masked_K','named_plus_masked','masked_K_diag_exact'],
            'aliases':{'svd_K_diag_exact':'svd_K'},'pairs_path':pairs.as_posix(),'pairs_sha256':sha(pairs),
            'protocol_sha256':sha('out/phase50_fp32_protocol.json'),'sample_sha256':sha('out/phase50_fp32_sample.json'),
            'elapsed_seconds':0.,'metadata_only_CPU_no_GPU_allocation':True}
        with result.open('x') as out:json.dump(obj,out,indent=2,allow_nan=False)
        print('Exact CPU alias metadata completed',m,flush=True)

if __name__=='__main__':main()
