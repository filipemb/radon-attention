"""
Phase 18 (NN revision) — cross-validated sink-calibration strength (beta).

Reviewers objected that beta=0.25 was selected on the same probe family it is
evaluated on. This cross-validates across probe families: it sweeps beta on
family A, picks the argmax, then reports the gain that fixed beta gives on
family B (held out), and vice versa. If the calibration transfers across
families, the gain is not an artifact of tuning on the evaluation set.

Family A = induction-copy probe (phase8). Family B = multi-distractor key-value
retrieval (phase16). Same sink-calibration harness (column 0 scaled by beta).
"""
import argparse, json, os
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AttentionInterface

import phase8_lostmiddle as P8
from phase8_lostmiddle import recon_attention_forward, filler_pool, build_probe, accuracy_by_pos
from phase16_longcontext import build_kv, make_keys, position_grid, acc_by_pos


def mid(acc, positions):
    L = positions[-1]
    m = [acc[p] for p in positions if 0.25 * L <= p <= 0.75 * L]
    return float(np.mean(m))


def run(name, dtype, args, device, rng):
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, attn_implementation="eager", dtype=dtype).to(device).eval()
    vocab = model.config.vocab_size
    # Families A and B must be genuinely independent for a real cross-validation.
    # filler_pool reads wikitext from the start and ignores its seed, so we take
    # DISJOINT slices for A and B, and drive their construction with INDEPENDENT rngs.
    needA = args.n_per_pos * args.nA * 4
    needB = args.n_per_pos * args.nB * 4
    fullpool = filler_pool(tok, needA + needB + 64, args.seed)
    poolA, poolB = fullpool[:needA], fullpool[needA:]
    rng_a = np.random.default_rng(args.seed)
    rng_b = np.random.default_rng(args.seed + 12345)
    # family A: induction-copy at nA
    posA = [p for p in [4, 16, 32, 48, 64, 80, 96, 110] if p < args.nA - 6]
    probeA = build_probe(poolA, vocab, args.nA, posA, args.n_per_pos, rng_a)
    # family B: KV retrieval at nB
    posB = position_grid(args.nB, 8)
    keys = make_keys(8)
    probeB = build_kv(poolB, vocab, args.nB, posB, args.n_per_pos, keys, rng_b)

    model.config._attn_implementation = "recon"
    for sub in model.modules():
        if hasattr(sub, "config"):
            try: sub.config._attn_implementation = "recon"
            except Exception: pass

    grid = args.betas
    midA, midB = {}, {}
    for beta in grid:
        P8.RECON["beta"] = beta
        midA[beta] = mid(accuracy_by_pos(model, probeA, device, args.batch), posA)
        midB[beta] = mid(acc_by_pos(model, probeB, device, args.batch), posB)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()

    betaA = max(grid, key=lambda b: midA[b])   # selected on A
    betaB = max(grid, key=lambda b: midB[b])   # selected on B
    base = 1.0 if 1.0 in grid else max(grid)
    return {
        "midA": midA, "midB": midB, "posA": posA, "posB": posB,
        "beta_selected_on_A": betaA, "beta_selected_on_B": betaB,
        # held-out gains (select on one family, evaluate on the other)
        "heldout_gain_on_B_using_betaA": midB[betaA] - midB[base],
        "heldout_gain_on_A_using_betaB": midA[betaB] - midA[base],
        "gain_on_A_at_0.25": (midA[0.25] - midA[base]) if 0.25 in grid else None,
        "gain_on_B_at_0.25": (midB[0.25] - midB[base]) if 0.25 in grid else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "gpt2-medium", "EleutherAI/pythia-410m", "Qwen/Qwen2.5-0.5B"])
    ap.add_argument("--nA", type=int, default=128)
    ap.add_argument("--nB", type=int, default=256)
    ap.add_argument("--n_per_pos", type=int, default=150)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--betas", nargs="*", type=float, default=[1.0, 0.75, 0.5, 0.35, 0.25, 0.15, 0.10, 0.05, 0.0])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    AttentionInterface.register("recon", recon_attention_forward)

    fname = f"phase18_betacv{('_' + args.tag) if args.tag else ''}.json"
    results = {"_meta": {"nA": args.nA, "nB": args.nB, "betas": args.betas,
                         "n_per_pos": args.n_per_pos, "seed": args.seed}}
    for m in args.models:
        dtype = torch.bfloat16 if "Qwen2.5-3B" in m else torch.float32
        print(f"\n===== {m} =====", flush=True)
        try:
            r = run(m, dtype, args, device, rng)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[m] = {"error": f"{type(e).__name__}: {e}"}
            json.dump(results, open(os.path.join(args.out, fname), "w"), indent=2)
            continue
        results[m] = r
        json.dump(results, open(os.path.join(args.out, fname), "w"), indent=2)
        print(f"  beta* on A(induction)={r['beta_selected_on_A']} -> held-out gain on B(KV) = {r['heldout_gain_on_B_using_betaA']*100:+.1f}pp", flush=True)
        print(f"  beta* on B(KV)={r['beta_selected_on_B']} -> held-out gain on A(induction) = {r['heldout_gain_on_A_using_betaB']*100:+.1f}pp", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, fname))}")


if __name__ == "__main__":
    main()
