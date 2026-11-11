"""P0 V2 Qwen-3B replication on all frozen document/layer/head samples."""
from sampling import write_json_new
from pathlib import Path
import argparse
from phase24_p0_metrics import run_core

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-3B")
    ap.add_argument("--lengths", nargs="+", type=int, default=[128, 256])
    args = ap.parse_args()
    result = {"model": args.model, "by_length": {str(n): run_core(args.model, n) for n in args.lengths}}
    path = Path("out/phase9_bigmodel_v2.json")
    if not path.exists():
        write_json_new(path, result)

if __name__ == "__main__":
    main()
