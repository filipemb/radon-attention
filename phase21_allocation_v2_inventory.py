"""Immutable inventory of new E4 v2 sources, results, paired ledgers and logs."""
import hashlib
import json
from pathlib import Path
from datetime import datetime,timezone


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as inp:
        while chunk:=inp.read(1<<20):h.update(chunk)
    return h.hexdigest()


def main():
    destination=Path('out/phase21_allocation_v2_files.json')
    if destination.exists():raise FileExistsError(destination)
    paths={p for p in Path('.').glob('phase21_allocation_v2*') if p.is_file() and p.suffix in ('.py','.sh')}
    paths.update(p for p in Path('out').glob('phase21_allocation_v2*.json') if p.is_file())
    paths.update(p for p in Path('out/pairs').glob('phase21_allocation*_v2.jsonl') if p.is_file())
    paths.update(p for p in Path('out/_rerun_logs').glob('phase21_allocation_v2*') if p.is_file())
    paths.discard(destination)
    records=[{'path':p.as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(paths)]
    primary=Path('out/phase21_allocation_v2.json')
    result={'schema_version':2,'created_UTC':datetime.now(timezone.utc).isoformat(),'files':records,
            'n_files_excluding_this_inventory':len(records),'total_bytes_excluding_this_inventory':sum(v['bytes'] for v in records),
            'this_inventory':destination.as_posix(),'self_hash_excluded':True,
            'primary_result_path':primary.as_posix() if primary.exists() else None,
            'old_v1_files_included_or_overwritten':False}
    with destination.open('x',encoding='utf-8') as out:json.dump(result,out,ensure_ascii=False,allow_nan=False,indent=2)
    print(f'{destination.as_posix()}: {len(records)} files, {result["total_bytes_excluding_this_inventory"]} bytes',flush=True)


if __name__=='__main__':main()
