"""Freeze a globally applied numerical correction; retain all v1 outputs."""
import phase19c_common
from pathlib import Path
from phase19c_common import read_json,write_json,digest
from phase19c_synthetic_controls import specs

def main():
    path=Path("out/phase19c_protocol_v2.json")
    if path.exists():raise FileExistsError(path)
    original=Path("out/phase19c_protocol.json");protocol=read_json(original)
    validation=read_json("out/phase19c_qr_validation.json")
    if not validation["passed"]:raise AssertionError("Stable ALS validation failed")
    protocol["revision"]={"superseded_protocol":original.as_posix(),"superseded_protocol_sha256":digest(original),
        "reason":"Three workers stopped when proposed ALS objectives increased beyond the original1e-9 tolerance on random causal nulls. All old files retained.",
        "new_case_root":"out/phase19c_v2_cache","no_changes_to_cohorts_seeds_budgets_thresholds_or_parametric_optimizer":True,
        "global_rule":"Every final baseline/control is recomputed with stable ALS; no per-case best-of or exclusion",
        "retained_failed_worker_logs":{p.as_posix():digest(p) for p in Path("out/_rerun_logs").glob("phase19c_worker_cpu_slot*.log")},
        "stable_validation_sha256":digest("out/phase19c_qr_validation.json")}
    protocol["ALS"].update({"implementation":"phase19c_als_qr.py","gauge":"column norm balancing, preserving product without cross-column rotations",
        "block_solver":"Streaming prefix/suffix Givens QR on the original design and right-hand sides; small triangular-factor SVD least squares, rcond1e-12, no normal equations",
        "numerical_safeguard":"Unchanged1e-9 increase tolerance triggers a full direct-LS retry; if it still increases loss, record a numerical rejection and retain previous finite state; continue2000 fixed sweeps",
        "numerical_rejections_reported":True,"regularization":0.})
    protocol["synthetic_specs"]=specs()
    protocol["negative_controls"].update({"random":"16 paired Q,K draws per n and per convention: QK/sqrt64 and QK without scaling; d_k64. All original scaled cases retained.",
        "temperature_reason":"Audit dimension/temperature was not specified; both common conventions declared before any new parametric control fitting, with identical underlying Q,K seeds",
        "matrix_count":66})
    protocol["statistics"]["negative_random_Holm_family"]=72
    protocol["numeric_sources_sha256"]={p.as_posix():digest(p) for p in sorted(Path('.').glob('phase19c_*.py'))
        if p.name not in ['phase19c_analysis.py','phase19c_audit.py','phase19c_figures.py','phase19c_inventory.py']}
    write_json(path,protocol)

if __name__=="__main__":main()
