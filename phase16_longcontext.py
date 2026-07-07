"""
Phase 16 (NN revision) — long-context retrieval with a genuine U-shaped baseline.

Reviewers noted the n=256 KV probe has flat baselines, so the sink-calibration
gain reads as a generic accuracy bump rather than a middle-of-context fix. This
runs the multi-distractor key-value retrieval at longer context (n in {512,1024})
with more distractor pairs and a dense position grid, and reports HONESTLY whether
a lost-in-the-middle dip appears in the baseline, plus the calibration lift per
position. If a real U-shape emerges, the middle-of-context claim is earned; if
not, the result is reported as a flat-baseline global gain. No curve is forced.

Reuses the sink-calibration injection harness from phase8 (RECON["beta"] scales
attention column 0 and renormalizes).
"""
import argparse, json, os
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AttentionInterface

import phase8_lostmiddle as P8
from phase8_lostmiddle import recon_attention_forward, filler_pool


def make_keys(n_pairs, klen=3):
    # Multi-token keys (unambiguous match, like phase8's 4-token TAG) to lift the
    # operating point off the floor so a middle dip, if present, is detectable.
    return [[201 + 13 * i + j for j in range(klen)] for i in range(n_pairs)]


def position_grid(n, n_pos):
    fr = np.linspace(0.03, 0.92, n_pos)
    pos = sorted(set(int(f * n) for f in fr))
    return [p for p in pos if 4 <= p <= n - 6]


def build_kv(pool, vocab, n, positions, n_per_pos, keys, rng):
    N = len(keys); klen = len(keys[0]); span = klen + 1; out = {}
    keytoks = set(t for k in keys for t in k)
    content = np.array([t for t in pool if t not in keytoks and t < vocab])
    step = max(span, (n - 10) // (N + 1))
    for p in positions:
        rows, tgt = [], []
        for _ in range(n_per_pos):
            seq = pool[int(rng.integers(0, len(pool) - n - 1)):][:n].copy()
            cand = [s for s in range(4, n - span - 2, step) if abs(s - p) >= span + 1]
            rng.shuffle(cand)
            dslots = cand[:N - 1]
            X = int(rng.choice(content))
            seq[p:p + klen] = keys[0]; seq[p + klen] = X        # queried pair at p (multi-token key)
            for j, s in enumerate(dslots):
                seq[s:s + klen] = keys[j + 1]; seq[s + klen] = int(rng.choice(content))
            seq[n - klen:n] = keys[0]                            # query (full key) at the end
            rows.append(seq); tgt.append(X)
        out[p] = (torch.tensor(np.array(rows), dtype=torch.long), torch.tensor(tgt, dtype=torch.long))
    return out


@torch.no_grad()
def acc_by_pos(model, probe, device, batch):
    acc = {}
    for p, (ids, X) in probe.items():
        ok = 0
        for s in range(0, ids.shape[0], batch):
            pred = model(ids[s:s + batch].to(device)).logits[:, -1, :].argmax(-1).cpu()
            ok += int((pred == X[s:s + batch]).sum())
        acc[p] = ok / ids.shape[0]
    return acc


def ushape_diag(acc, positions):
    """Dip = mean(ends) - mean(middle). Positive dip => lost-in-the-middle present."""
    L = positions[-1]
    ends = [acc[p] for p in positions if p < 0.17 * L or p > 0.83 * L]
    mids = [acc[p] for p in positions if 0.33 * L <= p <= 0.67 * L]
    em, mm = float(np.mean(ends)) if ends else 0.0, float(np.mean(mids)) if mids else 0.0
    return {"ends_mean": em, "mid_mean": mm, "dip": em - mm}


def run(name, dtype, args, device, rng):
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, attn_implementation="eager", dtype=dtype).to(device).eval()
    vocab = model.config.vocab_size
    keys = make_keys(args.n_pairs)
    positions = position_grid(args.seq_len, args.n_pos)
    pool = filler_pool(tok, args.n_per_pos * args.seq_len * 4, args.seed)
    probe = build_kv(pool, vocab, args.seq_len, positions, args.n_per_pos, keys, rng)
    model.config._attn_implementation = "recon"
    for sub in model.modules():
        if hasattr(sub, "config"):
            try: sub.config._attn_implementation = "recon"
            except Exception: pass
    res = {"positions": positions, "n_pairs": args.n_pairs}
    for beta in [1.0, args.beta]:
        P8.RECON["beta"] = beta
        acc = acc_by_pos(model, probe, device, args.batch)
        res[str(beta)] = acc
        res[f"ushape_{beta}"] = ushape_diag(acc, positions)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq_len", type=int, default=512)
    ap.add_argument("--n_pairs", type=int, default=12)
    ap.add_argument("--n_pos", type=int, default=11)
    ap.add_argument("--n_per_pos", type=int, default=150)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--beta", type=float, default=0.25)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    AttentionInterface.register("recon", recon_attention_forward)

    fname = f"phase16_longcontext{('_' + args.tag) if args.tag else ''}.json"
    # (name, dtype, batch) — keep batch small at long n to fit the eager n x n attention on 12 GB
    jobs = [("gpt2-medium", torch.float32, args.batch),
            ("EleutherAI/pythia-1.4b", torch.float32, max(2, args.batch // 2)),
            ("Qwen/Qwen2.5-3B", torch.bfloat16, 2)]
    results = {"_meta": {"seq_len": args.seq_len, "n_pairs": args.n_pairs, "n_per_pos": args.n_per_pos,
                         "beta": args.beta, "seed": args.seed}}
    for name, dt, bs in jobs:
        args.batch = bs
        print(f"\n===== {name} (n={args.seq_len}) =====", flush=True)
        try:
            r = run(name, dt, args, device, rng)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[name] = {"error": f"{type(e).__name__}: {e}"}
            json.dump(results, open(os.path.join(args.out, fname), "w"), indent=2)
            continue
        results[name] = r
        json.dump(results, open(os.path.join(args.out, fname), "w"), indent=2)
        pos = r["positions"]; b = r["1.0"]; c = r[str(args.beta)]
        ub, uc = r["ushape_1.0"], r[f"ushape_{args.beta}"]
        print("  pos:      " + " ".join(f"{p:>4}" for p in pos), flush=True)
        print("  baseline: " + " ".join(f"{b[p]:.2f}" for p in pos) + f"  | dip={ub['dip']:+.3f} (mid={ub['mid_mean']:.2f} ends={ub['ends_mean']:.2f})", flush=True)
        print(f"  sink b={args.beta}: " + " ".join(f"{c[p]:.2f}" for p in pos) + f"  | dip={uc['dip']:+.3f} mid={uc['mid_mean']:.2f} (+{(uc['mid_mean']-ub['mid_mean'])*100:.1f}pp mid)", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, fname))}")


if __name__ == "__main__":
    main()
