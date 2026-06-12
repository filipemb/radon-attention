"""
A1 — benchmark KV-retrieval real (retrieval entre distratores).

Mais convincente que a sonda single-needle: planta N pares [chave][valor] espalhados
em texto real; consulta UMA chave no fim; o modelo deve copiar o valor certo,
ignorando N-1 pares distratores. Mede acuracia por posicao do par consultado
(curva lost-in-the-middle), com/sem calibracao do sink (coluna 0, beta).

Modelos capazes: Qwen2.5-3B (bf16) + gpt2-medium (fp32). n=256.
Reusa o harness de injecao do phase8 (RECON["beta"] atenua a coluna 0).
"""
import argparse, json, os
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AttentionInterface

import phase8_lostmiddle as P8
from phase8_lostmiddle import recon_attention_forward, filler_pool

KEYS = [101, 202, 303, 404, 505, 606, 707, 808]   # N chaves distintas fixas


def build_kv(pool, vocab, n, positions, n_per_pos, rng):
    """{p: (ids[N,n], target[N])}. Par consultado (KEYS[0]) na posicao p; demais distratores."""
    N = len(KEYS); out = {}
    content = np.array([t for t in pool if t not in set(KEYS) and t < vocab])
    for p in positions:
        rows, tgt = [], []
        # slots possiveis (cada par ocupa 2 tokens), espalhados, sem sobrepor p
        for _ in range(n_per_pos):
            seq = pool[int(rng.integers(0, len(pool) - n - 1)):][:n].copy()
            cand = [s for s in range(4, n - 6, max(2, (n - 10) // (N + 1))) if abs(s - p) >= 3]
            rng.shuffle(cand)
            dslots = cand[:N - 1]
            X = int(rng.choice(content))
            seq[p] = KEYS[0]; seq[p + 1] = X                 # par consultado
            for j, s in enumerate(dslots):
                seq[s] = KEYS[j + 1]; seq[s + 1] = int(rng.choice(content))
            seq[n - 1] = KEYS[0]                              # consulta no fim
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


def midmean(acc, pos):
    mids = [p for p in pos if 0.2 * pos[-1] < p < 0.8 * pos[-1]]
    return float(np.mean([acc[p] for p in mids]))


def run(name, dtype, args, device, rng):
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, attn_implementation="eager", dtype=dtype).to(device).eval()
    vocab = model.config.vocab_size
    positions = [16, 48, 96, 144, 192, 232]
    pool = filler_pool(tok, args.n_per_pos * args.seq_len * 4, args.seed)
    probe = build_kv(pool, vocab, args.seq_len, positions, args.n_per_pos, rng)
    model.config._attn_implementation = "recon"
    for sub in model.modules():
        if hasattr(sub, "config"):
            try: sub.config._attn_implementation = "recon"
            except Exception: pass
    res = {"positions": positions}
    for beta in [1.0, args.beta]:
        P8.RECON["beta"] = beta
        res[str(beta)] = acc_by_pos(model, probe, device, args.batch)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq_len", type=int, default=256)
    ap.add_argument("--n_per_pos", type=int, default=200)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--beta", type=float, default=0.25)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="", help="sufixo do arquivo de saida (versionado)")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    AttentionInterface.register("recon", recon_attention_forward)

    fname = f"phase11_kv{('_' + args.tag) if args.tag else ''}.json"
    jobs = [("gpt2-medium", torch.float32, 8), ("Qwen/Qwen2.5-3B", torch.bfloat16, 4)]
    results = {"_meta": {"n_per_pos": args.n_per_pos, "seed": args.seed,
                         "beta": args.beta, "seq_len": args.seq_len}}
    for name, dt, bs in jobs:
        args.batch = bs
        print(f"\n===== {name} =====", flush=True)
        try:
            r = run(name, dt, args, device, rng)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[name] = {"error": f"{type(e).__name__}: {e}"}
            json.dump(results, open(os.path.join(args.out, fname), "w"), indent=2)
            continue
        results[name] = r
        json.dump(results, open(os.path.join(args.out, fname), "w"), indent=2)
        pos = r["positions"]
        b = {p: r["1.0"][p] for p in pos}; c = {p: r[str(args.beta)][p] for p in pos}
        print("  pos:      " + " ".join(f"{p:>4}" for p in pos), flush=True)
        print("  baseline: " + " ".join(f"{b[p]:.2f}" for p in pos) + f"  | meio={midmean(b,pos):.3f}", flush=True)
        print(f"  sink b={args.beta}: " + " ".join(f"{c[p]:.2f}" for p in pos) + f"  | meio={midmean(c,pos):.3f}  (+{(midmean(c,pos)-midmean(b,pos))*100:.1f})", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, fname))}")


if __name__ == "__main__":
    main()
