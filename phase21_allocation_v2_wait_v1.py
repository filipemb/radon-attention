"""Record V1 appearance or the user-defined 3h timeout; no GPU lock held."""
from datetime import datetime,timezone
import json
from pathlib import Path
import time

root=Path("out")
config=json.loads((root/"phase21_allocation_v2_run.json").read_text(encoding="utf-8"))
deadline=datetime.fromisoformat(config["waiting_for_V1_deadline_UTC"])
source=root/"phase2_downstream_v2.json"
while True:
    now=datetime.now(timezone.utc)
    if source.exists() and source.stat().st_mtime<=deadline.timestamp():
        target=root/"phase21_allocation_v2_V1_ready.json"
        value={"status":"ready","observed_UTC":now.isoformat(),"source":source.as_posix(),
               "source_mtime_UTC":datetime.fromtimestamp(source.stat().st_mtime,timezone.utc).isoformat(),
               "deadline_UTC":deadline.isoformat(),"GPU_lock_held_by_watcher":False}
        if not target.exists():
            with target.open("x",encoding="utf-8") as out:json.dump(value,out,indent=2)
        print(json.dumps(value),flush=True)
        break
    remaining=(deadline-now).total_seconds()
    if remaining<=0:
        target=root/"phase21_allocation_v2_V1_timeout.json"
        value={"status":"FALTA","observed_UTC":now.isoformat(),"missing_source":source.as_posix(),
               "wait_started_UTC":config["waiting_for_V1_started_UTC"],"deadline_UTC":deadline.isoformat(),
               "wait_limit_hours":3,"model_injection_executed":False}
        if not target.exists():
            with target.open("x",encoding="utf-8") as out:json.dump(value,out,indent=2)
        print(json.dumps(value),flush=True)
        break
    print(f"V1 pending; remaining_wait_seconds={remaining:.0f}",flush=True)
    time.sleep(min(30.,remaining))
