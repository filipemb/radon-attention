"""
Parte 2, Etapa D — validacao a jusante + EDITABILIDADE.

Injeta no forward (modelo inteiro) a reconstrucao de dois canais ANOVA:
  recon = (efeito_linha + efeito_coluna - mu) + rank-k(interacao)
e mede KL(verdadeiro || recon). Se pequeno, a decomposicao preserva o comportamento.

Depois EDITA o componente nomeado:
  - nosink:      zera a atencao ao token 0 (remove o sink) e renormaliza
  - zerocol_mid: zera uma coluna do meio (controle: coluna nao-sink)
Se KL(nosink) >> KL(zerocol_mid), o sink e uma alavanca real, isolavel e editavel
via o termo nomeado, exatamente a promessa do canal interpretavel.

Referencia = modelo eager verdadeiro. Sanity: modo identidade tem KL ~ 0.
"""
import argparse, json, os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, AttentionInterface

from phase0_radon_attention import load_sequences

RECON = {"mode": "identity", "k": 8}


def _repeat_kv(x, n):
    if n == 1:
        return x
    b, h, s, d = x.shape
    return x[:, :, None, :, :].expand(b, h, n, s, d).reshape(b, h * n, s, d)


def reconstruct(W):
    mode = RECON["mode"]
    if mode == "identity":
        return W
    k = RECON["k"]
    b, h, q, kk = W.shape
    X = W.float()
    mu = X.mean(dim=(-1, -2), keepdim=True)
    r = X.mean(dim=-1, keepdim=True)            # efeito de linha
    c = X.mean(dim=-2, keepdim=True)            # efeito de coluna (c[...,0] = sink)
    additive = r + c - mu
    Theta = X - additive
    U, S, Vh = torch.linalg.svd(Theta, full_matrices=False)
    Tk = (U[..., :k] * S[..., None, :k]) @ Vh[..., :k, :]
    recon = additive + Tk
    if mode == "nosink":
        recon[..., :, 0] = 0.0                  # remove atencao ao token 0
    elif mode == "zerocol_mid":
        recon[..., :, kk // 2] = 0.0            # controle: coluna do meio
    causal = torch.tril(torch.ones(q, kk, device=W.device, dtype=recon.dtype))
    recon = recon * causal
    recon = recon.clamp(min=0)
    recon = recon / recon.sum(-1, keepdim=True).clamp_min(1e-9)
    return recon.type(W.dtype)


def recon_attention_forward(module, query, key, value, attention_mask, scaling=None, dropout=0.0, **kwargs):
    if scaling is None:
        scaling = query.size(-1) ** -0.5
    nrep = getattr(module, "num_key_value_groups", 1)
    if nrep and nrep > 1:
        key = _repeat_kv(key, nrep); value = _repeat_kv(value, nrep)
    aw = torch.matmul(query, key.transpose(-1, -2)) * scaling
    q_len, k_len = aw.shape[-2], aw.shape[-1]
    causal = torch.full((q_len, k_len), float("-inf"), device=aw.device, dtype=aw.dtype)
    aw = aw + torch.triu(causal, diagonal=1 + (k_len - q_len))
    aw = F.softmax(aw, dim=-1).type(value.dtype)
    aw = reconstruct(aw)
    out = torch.matmul(aw, value).transpose(1, 2)
    return out, aw


@torch.no_grad()
def logits(model, ids, batch, device):
    out = []
    for s in range(0, ids.shape[0], batch):
        out.append(model(ids[s:s + batch].to(device)).logits.float().cpu())
    return torch.cat(out, 0)


def kl(ref, other):
    p = F.softmax(ref, -1); logp = F.log_softmax(ref, -1); logq = F.log_softmax(other, -1)
    return float((p * (logp - logq)).sum(-1).mean())


def run(name, args, device):
    tok = AutoTokenizer.from_pretrained(name)
    ids = load_sequences(tok, args.n_seq, args.seq_len, args.seed)
    model = AutoModelForCausalLM.from_pretrained(name, attn_implementation="eager", dtype=torch.float32).to(device).eval()
    ref = logits(model, ids, args.batch, device)
    model.config._attn_implementation = "recon"
    for sub in model.modules():
        if hasattr(sub, "config"):
            try: sub.config._attn_implementation = "recon"
            except Exception: pass
    res = {}
    for mode in ["identity", "anova", "nosink", "zerocol_mid"]:
        RECON["mode"] = mode
        res[mode] = kl(ref, logits(model, ids, args.batch, device))
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "EleutherAI/pythia-410m"])
    ap.add_argument("--n_seq", type=int, default=50)
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    RECON["k"] = args.k
    AttentionInterface.register("recon", recon_attention_forward)

    results = {}
    for m in args.models:
        print(f"\n===== {m} =====", flush=True)
        try:
            r = run(m, args, device)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[m] = {"error": f"{type(e).__name__}: {e}"}; continue
        results[m] = r
        json.dump(results, open(os.path.join(args.out, "phase7_editability.json"), "w"), indent=2)
        sane = "OK" if r["identity"] < 1e-3 else "FALHOU"
        print(f"  sanity KL(identidade)={r['identity']:.2e} [{sane}]", flush=True)
        print(f"  KL anova (decomp fiel?) = {r['anova']:.3f}", flush=True)
        print(f"  KL nosink (remove sink) = {r['nosink']:.3f}", flush=True)
        print(f"  KL zerocol_mid (controle) = {r['zerocol_mid']:.3f}", flush=True)
        if r["zerocol_mid"] > 1e-6:
            print(f"  => remover sink e {r['nosink']/r['zerocol_mid']:.1f}x mais impactante que coluna aleatoria", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, 'phase7_editability.json'))}")


if __name__ == "__main__":
    main()
