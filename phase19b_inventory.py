"""Inventory the new E2b sources and final artifacts after worker completion."""
import phase19b_common
from pathlib import Path
from phase19b_common import ROOT,read_json,write_json,digest


def items(paths):
    return [{"path":p.as_posix(),"bytes":p.stat().st_size,"sha256":digest(p)} for p in sorted(paths)]


def main():
    output=Path("out/phase19b_artifacts.json")
    if output.exists():raise FileExistsError(output)
    report=read_json("out/phase19b_richlines.json");audit=read_json("out/phase19b_integrity_audit.json")
    if not audit["passed"] or digest("out/phase19b_richlines.json")!=audit["report_sha256"]:
        raise AssertionError("Final audited report is required")
    for p,h in report["source_code_sha256"].items():
        if digest(p)!=h:raise AssertionError(f"Post-aggregation source change: {p}")
    expected={"controls":128,"init":192,"original":768,"free":192,"thin":192}
    counts={k:len(list((ROOT/k).glob("*.json"))) for k in expected}
    if counts!=expected:raise AssertionError("Incomplete final cache")
    pairs=list(Path("out/pairs").glob("phase19b_*.jsonl"))
    if len(pairs)!=24:raise AssertionError("Expected24 paired instance files")
    result={"sources":items(Path('.').glob('phase19b_*.py')),
        "paired_results":items(pairs),"reports":items(Path('out').glob('phase19b_*.json')),
        "tables":items(Path('out').glob('phase19b_*.csv')),
        "figures":items([*Path('out').glob('phase19b_*.svg'),*Path('out').glob('phase19b_*.png')]),
        "raw_case_caches":items(ROOT.glob('*/*.json')),
        "logs":items(Path('out/_rerun_logs').glob('phase19b_*')),
        "raw_cache_counts":counts,"parent_artifacts_unchanged":audit["parent_artifacts_byte_identical"],
        "all_positive_control_gates_pass":report["all_positive_control_gates_pass"],
        "excluded_ephemeral_files":"Numba/CuPy compiled caches and FileLock lease files are not research outputs",
        "inventory_self_hash_omitted":True}
    write_json(output,result)
    print(f"Indexed {len(result['sources'])} sources,24 pair files and {sum(counts.values())} case caches",flush=True)


if __name__=="__main__":main()
