"""Final immutable inventory; initial numerical failures remain available."""
import phase19c_common
from pathlib import Path
from phase19c_common import read_json,write_json,digest

def items(paths):return [{"path":p.as_posix(),"bytes":p.stat().st_size,"sha256":digest(p)} for p in sorted(paths)]

def main():
    output=Path("out/phase19c_artifacts.json")
    if output.exists():raise FileExistsError(output)
    report=read_json("out/phase19c_richlines.json");audit=read_json("out/phase19c_integrity_audit.json")
    if not audit["passed"] or digest("out/phase19c_richlines.json")!=audit["report_sha256"]:raise AssertionError("Completed audit required")
    for p,h in report["source_code_sha256"].items():
        if digest(p)!=h:raise AssertionError(f"Source changed after aggregation: {p}")
    result={"primary_entrypoint":"phase19c_experiment.py","primary_worker":"phase19c_run.py","primary_masked_solver":"phase19c_als_qr.py",
        "primary_protocol":"out/phase19c_protocol_v2.json","primary_case_root":"out/phase19c_v2_cache",
        "sources":items(Path('.').glob('phase19c_*.py')),"paired_results":items(Path('out/pairs').glob('phase19c_*.jsonl')),
        "reports":items(Path('out').glob('phase19c_*.json')),"tables":items(Path('out').glob('phase19c_*.csv')),
        "primary_cases":items(Path('out/phase19c_v2_cache').glob('*/*.json')),
        "development_cases_retained":items(Path('out/phase19c_cache').glob('**/*.json')),
        "logs":items(Path('out/_rerun_logs').glob('phase19c_*')),
        "parent_artifacts_unchanged":True,"all_masked_positive_gates_pass":report["all_masked_positive_gates_pass"],
        "all_planted_segment_gates_pass":report["all_planted_segment_gates_pass"],"self_hash_omitted":True,
        "ephemeral_files_excluded":"Numba/CuPy compiled caches and FileLock lease files"}
    if len(result["paired_results"])!=30 or len(result["primary_cases"])!=2102:raise AssertionError("Incomplete E2c output inventory")
    write_json(output,result);print("Indexed2102 primary cases,30 pair files and all retained development artifacts",flush=True)

if __name__=="__main__":main()
