"""Read-only, standard-library status of E9, including incomplete forwards."""
import json
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent


def read(path):return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    protocol=read(ROOT/"out/phase50_protocol.json");result={"UTC":datetime.now(timezone.utc).isoformat(),"models":{}}
    for model in protocol["models"]:
        slug=model.replace("/","__");row={}
        mp=ROOT/"out"/f"phase50_matrix_{slug}.json"
        row["matrix_complete"]=mp.exists()
        cp=ROOT/"out"/f"phase50_GPU_CPU_reference_{slug}.json"
        row["CPU_reference_ready"]=cp.exists()
        vp=ROOT/"out"/f"phase50_estimator_validation_{slug}.json"
        if vp.exists():
            validation=read(vp);row["estimator_validation_passed"]=validation["passed"]
            row["CPU_GPU_max_error_difference"]=validation["max_raw_error_difference"]
            row["uncorrected_GPU_max_error_difference"]=validation["max_uncorrected_GPU_CPU_error_difference"]
            row["CPU_reference_corrections"]=validation["CPU_reference_recomputed_fits"]
            row["uncorrected_GPU_validation_passed"]=validation["uncorrected_GPU_passed"]
        else:row["estimator_validation_passed"]=None
        fp=ROOT/"out"/f"phase50_forward_{slug}.json";row["forward_complete"]=fp.exists()
        pairpath=ROOT/"out/pairs"/f"phase50_forward_{slug}.jsonl"
        groups={}
        if pairpath.exists():
            with pairpath.open(encoding="utf-8") as inp:
                for line in inp:
                    if not line.endswith("\n"):continue  # Writer may be between write and flush; never used for science.
                    record=json.loads(line);label=record["arm"]+":"+str(record["K"])
                    groups.setdefault(label,set()).add(record["document_index"])
        row["forward_articles_by_arm_K"]={a:len(ids) for a,ids in groups.items()}
        result["models"][model]=row
    events=ROOT/"out/pairs/phase50_run_events.jsonl"
    if events.exists():
        lines=events.read_text(encoding="utf-8").splitlines()
        result["last_coordinator_event"]=json.loads(lines[-1]) if lines else None
    result["complete"]=(ROOT/"out/phase50_complete.json").exists()
    result["report_path"]="out/phase50_report.json" if (ROOT/"out/phase50_report.json").exists() else None
    print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))


if __name__=="__main__":main()
