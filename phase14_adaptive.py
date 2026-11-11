"""
A1 — beta ADAPTATIVO derivado da decomposicao (fix #1 do revisor TNNLS).

A vantagem teorica da nossa derivacao sobre o ACT e que a decomposicao da a
magnitude do sink por cabeca (o efeito de coluna c_0). Regra sem hiperparametro:
equalizar o sink de cada cabeca a MEDIANA entre cabecas:

    beta_h = min(1, median_h(c0) / c0_h)

Cabecas com sink acima da mediana sao atenuadas proporcionalmente; as demais
ficam intactas. Compara na sonda de retrieval: identity, fixo beta=0.25,
adaptativo, ACT-like. Saida versionada: out/phase14_adaptive_<tag>.json
"""
from sampling import MODELS  # datasets before torch; native thread caps.
import argparse, json, os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, AttentionInterface

from phase8_lostmiddle import filler_pool, build_probe, accuracy_by_pos, midmean, finish_sink_edit

RECON = {"mode": "identity", "beta": 0.25}
torch.set_num_threads(4)


def _repeat_kv(x, nrep):
    if nrep == 1:
        return x
    b, h, s, d = x.shape
    return x[:, :, None, :, :].expand(b, h, nrep, s, d).reshape(b, h * nrep, s, d)


def reconstruct(aw):
    mode = RECON["mode"]
    if mode == "identity":
        return aw
    before = aw
    aw = aw.clone()
    if mode == "fixed":
        aw[..., 0] = aw[..., 0] * RECON["beta"]
    elif mode == "adaptive":
        c0 = aw[..., 0].mean(dim=-1)                      # [b, h]: sink medio por cabeca
        med = c0.median(dim=-1, keepdim=True).values      # mediana entre cabecas
        beta_h = torch.clamp(med / c0.clamp_min(1e-9), max=1.0)   # [b, h]
        aw[..., 0] = aw[..., 0] * beta_h.unsqueeze(-1)
    elif mode == "act":
        c = aw.mean(dim=-2)
        thr = c.mean(dim=-1, keepdim=True) + 3 * c.std(dim=-1, keepdim=True)
        mask = (c > thr).unsqueeze(-2).expand_as(aw)
        aw = torch.where(mask, aw * RECON["beta"], aw)
    aw = finish_sink_edit(before, aw, RECON.setdefault("stats", {}))
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
    res = {"positions": positions, "acc": {}}
    for mode in ["identity", "fixed", "adaptive", "act"]:
        RECON["mode"] = mode
        res["acc"][mode] = accuracy_by_pos(model, probe, device, args.batch)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "gpt2-medium", "EleutherAI/pythia-410m", "Qwen/Qwen2.5-0.5B"])
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--n_per_pos", type=int, default=400)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="s0")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    AttentionInterface.register("recon", recon_attention_forward)

    fname = f"phase14_adaptive_{args.tag}.json"
    results = {"_meta": {"n_per_pos": args.n_per_pos, "seed": args.seed, "rule": "beta_h=min(1, median(c0)/c0_h)"}}
    for m in args.models:
        print(f"\n===== {m} =====", flush=True)
        try:
            r = run(m, args, device, rng)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[m] = {"error": f"{type(e).__name__}: {e}"}
            json.dump(results, open(os.path.join(args.out, fname), "w"), indent=2)
            continue
        results[m] = r
        json.dump(results, open(os.path.join(args.out, fname), "w"), indent=2)
        pos = r["positions"]
        mids = {k: midmean(r["acc"][k], pos) for k in r["acc"]}
        b = mids["identity"]
        print(f"  meio: base={b:.3f}  fixo={mids['fixed']:.3f} ({(mids['fixed']-b)*100:+.1f})  "
              f"adapt={mids['adaptive']:.3f} ({(mids['adaptive']-b)*100:+.1f})  "
              f"act={mids['act']:.3f} ({(mids['act']-b)*100:+.1f})", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, fname))}")


if __name__ == "__main__":
    main()
