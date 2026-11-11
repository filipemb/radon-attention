"""Complete the CPU audit and report after the queued GPU continuation finishes."""
from pathlib import Path
import subprocess
import sys
import time

result=Path('out/phase21_allocation_v2_forward.json')
while not result.exists():
    time.sleep(30)
for script,output in (
    ('phase21_allocation_v2_forward_audit.py','out/phase21_allocation_v2_forward_audit.json'),
    ('phase21_allocation_v2_forward_report.py','out/_rerun_logs/phase21_allocation_v2_forward_results.md'),
):
    if not Path(output).exists():
        subprocess.run([sys.executable,'-B',script],check=True)
print('E4 FORWARD FINAL AUDIT AND REPORT COMPLETE',flush=True)
