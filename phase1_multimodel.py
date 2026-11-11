"""P0 V2 multimodel metrics on immutable document-stratified archives."""
from sampling import MODELS
import argparse
from phase24_p0_metrics import run_core, aggregate_core

DEFAULT_MODELS = MODELS

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--seq_len", type=int, default=128)
    args = ap.parse_args()
    aggregate_core([run_core(m, args.seq_len) for m in args.models])

if __name__ == "__main__":
    main()
