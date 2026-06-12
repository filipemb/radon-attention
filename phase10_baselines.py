"""
A1 — baseline ACT vs nossa edicao principiada do sink.

Na sonda de retrieval (induction-copy), compara, com a mesma forca beta:
  - identity:  modelo verdadeiro (baseline)
  - oursink:   atenua SO a coluna 0 (sink = efeito-coluna, derivado da decomposicao)
  - act:       detecta colunas-sink ADAPTATIVAMENTE (outliers de atencao recebida,
               estilo ACT/massive-activations) e atenua todas elas

Se 'oursink' (1 coluna, principiado) iguala/bate 'act' (heuristico, varias colunas),
o argumento e que a decomposicao da o mesmo controle de forma mais simples e
interpretavel.
"""
import argparse, json, os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, AttentionInterface

from phase8_lostmiddle import filler_pool, build_probe, accuracy_by_pos, midmean

RECON = {"mode": "identity", "beta": 0.25}


def _repeat_kv(x, nrep):
    if nrep == 1:
        return x
    b, h, s, d = x.shape
    return x[:, :, None, :, :].expand(b, h, nrep, s, d).reshape(b, h * nrep, s, d)


def reconstruct(aw):
    mode, beta = RECON["mode"], RECON["beta"]
    if mode == "identity":
        return aw
    aw = aw.clone()
    if mode == "oursink":
        aw[..., 0] = aw[..., 0] * beta
    elif mode == "act":
        c = aw.mean(dim=-2)                                   # atencao recebida por coluna
        thr = c.mean(dim=-1, keepdim=True) + 3 * c.std(dim=-1, keepdim=True)
        mask = (c > thr).unsqueeze(-2).expand_as(aw)
        aw = torch.where(mask, aw * beta, aw)
    aw = aw / aw.sum(-1, keepdim=True).clamp_min(1e-9)
    return aw


def recon_attention_forward(module, query, key, value, attention_mask, scaling=None, dropout=0.0, **kwargs):
    if scaling is None:
        scaling = query.size(-1) ** -0.5
    nrep = getattr(module, "num_key_value_groups", 1)
    if nrep and nrep > 1:
        key = _repeat_kv(key, nrep); value = _repeat_kv(value, nrep)
    aw = torch.matmul(query, key.transpose(-1, -2)) * scaling
    q, k = aw.shape[-2], aw.shape[-1]
    causal = torch.full((q, k), float("-inf"), device=aw.device, dtype=aw.dtype)
    aw = aw + torch.triu(causal, diagonal=1 + (k - q))
    aw = F.softmax(aw, dim=-1).type(value.dtype)
    aw = reconstruct(aw)
    return torch.matmul(aw, value).transpose(1, 2), aw


def run(name, args, device, rng):
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, attn_implementation="eager", dtype=torch.float32).to(device).eval()
    vocab = model.config.vocab_size
    positions = [4, 16, 32, 48, 64, 80, 96, 110]
    pool = filler_pool(tok, args.n_per_pos * args.seq_len * 4, args.seed)
    probe = build_probe(pool, vocab, args.seq_len, positions, args.n_per_pos, rng)
    model.config._attn_implementation = "recon"
    for sub in model.modules():
        if hasattr(sub, "config"):
            try: sub.config._attn_implementation = "recon"
            except Exception: pass
    res = {"positions": positions, "mid": {}}
    for mode in ["identity", "oursink", "act"]:
        RECON["mode"] = mode
        acc = accuracy_by_pos(model, probe, device, args.batch)
        res["mid"][mode] = midmean(acc, positions)
        res[mode] = acc
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "gpt2-medium", "EleutherAI/pythia-410m", "Qwen/Qwen2.5-0.5B"])
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--n_per_pos", type=int, default=200)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--beta", type=float, default=0.25)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    RECON["beta"] = args.beta
    AttentionInterface.register("recon", recon_attention_forward)

    results = {}
    for m in args.models:
        print(f"\n===== {m} =====", flush=True)
        try:
            r = run(m, args, device, rng)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[m] = {"error": f"{type(e).__name__}: {e}"}; continue
        results[m] = r
        json.dump(results, open(os.path.join(args.out, "phase10_baselines.json"), "w"), indent=2)
        b, o, a = r["mid"]["identity"], r["mid"]["oursink"], r["mid"]["act"]
        print(f"  meio: baseline={b:.3f}  oursink(col0)={o:.3f} (+{(o-b)*100:.1f})  ACT(adaptativo)={a:.3f} (+{(a-b)*100:.1f})", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, 'phase10_baselines.json'))}")


if __name__ == "__main__":
    main()
