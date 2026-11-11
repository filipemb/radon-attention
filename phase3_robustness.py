"""P0 V2 length robustness; all declared documents and layers are processed.

The former early-stopping stream favored initial layers/documents. Extraction
is now centralized in extract_attn.py and completes its declared corpus.
"""
from sampling import MODELS
import argparse
from phase24_p0_metrics import run_core, aggregate_core

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--lengths", nargs="+", type=int, default=[128, 256])
    args = ap.parse_args()
    aggregate_core([run_core(m, n) for m in args.models for n in args.lengths])

if __name__ == "__main__":
    main()
