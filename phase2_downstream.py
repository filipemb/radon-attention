"""
Fase 2 (extensao) — teste A JUSANTE.

A pergunta que importa: substituindo a atencao A pela reconstruida no forward,
quanto muda a SAIDA do modelo? Mede KL(orig || recon) da distribuicao do proximo
token e a perplexidade, com o modelo inteiro rodando na atencao reconstruida.

Compara:
  - SVD rank-k (low-rank) para k em {1,2,4,8,16,32}
  - geometrica (minimos quadrados num dicionario de linhas estruturais: sink,
    bandas com perfil, diagonais)
  - identidade (sanity: KL deve ser ~0)

Hipotese (alinhada ao resultado de matriz): SVD com k pequeno preserva o
comportamento (KL->0); geometria nao alcanca.

Injecao: registra uma implementacao de atencao "recon" que reconstroi o
attn_weights (saida do softmax) antes do produto com V. Mesma assinatura eager
em todos os modelos (transformers 5.x), entao generaliza.
"""
import argparse, json, os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AttentionInterface
from transformers.models.gpt2.modeling_gpt2 import eager_attention_forward as _eager_ref

from phase0_radon_attention import load_sequences

# ---- estado global lido pela atencao custom ----
RECON = {"mode": "identity", "k": 8, "D": None, "n": None}


def reconstruct(weights):
    """weights: [b, h, q, k] (saida do softmax, causal). Retorna reconstruida,
    re-normalizada por linha (atencao valida)."""
    mode = RECON["mode"]
    if mode == "identity":
        return weights
    b, h, q, k = weights.shape
    W = weights.reshape(b * h, q, k).float()
    if mode == "svd":
        U, S, Vh = torch.linalg.svd(W, full_matrices=False)
        kk = RECON["k"]
        rec = (U[..., :kk] * S[..., None, :kk]) @ Vh[..., :kk, :]
    elif mode == "geom":
        D = RECON["D"]                       # [q*k, m]
        bvec = W.reshape(b * h, q * k).T     # [q*k, B]
        sol = torch.linalg.lstsq(D, bvec).solution   # [m, B]
        rec = (D @ sol).T.reshape(b * h, q, k)
    else:
        return weights
    rec = rec.clamp(min=0)
    rec = rec / rec.sum(-1, keepdim=True).clamp_min(1e-9)
    return rec.reshape(b, h, q, k).type(weights.dtype)


def _repeat_kv(x, n_rep):
    if n_rep == 1:
        return x
    b, h, s, d = x.shape
    return x[:, :, None, :, :].expand(b, h, n_rep, s, d).reshape(b, h * n_rep, s, d)


def recon_attention_forward(module, query, key, value, attention_mask, scaling=None, dropout=0.0, **kwargs):
    if scaling is None:
        scaling = query.size(-1) ** -0.5
    # GQA: repete as KV heads p/ casar com as query heads (Qwen etc)
    n_rep = getattr(module, "num_key_value_groups", 1)
    if n_rep and n_rep > 1:
        key = _repeat_kv(key, n_rep)
        value = _repeat_kv(value, n_rep)
    attn_weights = torch.matmul(query, key.transpose(-1, -2)) * scaling
    # Mascara causal PURA, identica p/ todos os modelos. Nossos inputs nao tem
    # padding, entao isto reproduz exatamente a atencao verdadeira (verificado pelo
    # sanity check de identidade) e elimina a variabilidade da attention_mask passada.
    q_len, k_len = attn_weights.shape[-2], attn_weights.shape[-1]
    causal = torch.full((q_len, k_len), float("-inf"), device=attn_weights.device, dtype=attn_weights.dtype)
    causal = torch.triu(causal, diagonal=1 + (k_len - q_len))
    attn_weights = attn_weights + causal
    attn_weights = F.softmax(attn_weights, dim=-1).type(value.dtype)
    attn_weights = reconstruct(attn_weights)            # <-- injecao
    attn_output = torch.matmul(attn_weights, value)
    attn_output = attn_output.transpose(1, 2)
    return attn_output, attn_weights


def build_dictionary(n, device):
    """Dicionario de linhas estruturais causais (colunas normalizadas)."""
    cols = []
    # sink + algumas verticais
    for c in [0, 1, 2]:
        M = torch.zeros(n, n); idx = torch.arange(c, n); M[idx, c] = 1.0
        cols.append(M)
    # bandas com perfil exponencial
    for tau in [1, 2, 4, 8, 16, 32, 64]:
        o = torch.arange(n).float()
        w = torch.exp(-o / tau)
        M = torch.zeros(n, n)
        for off in range(n):
            if w[off] < 1e-6:
                break
            ii = torch.arange(off, n); M[ii, ii - off] = w[off]
        cols.append(M)
    # diagonais nitidas (inducao)
    for d in [4, 8, 16, 32, 64]:
        M = torch.zeros(n, n); ii = torch.arange(d, n); M[ii, ii - d] = 1.0
        cols.append(M)
    D = torch.stack([c.reshape(-1) for c in cols], dim=1).to(device)  # [n*n, m]
    D = D / D.norm(dim=0, keepdim=True).clamp_min(1e-9)
    return D


@torch.no_grad()
def collect_logits(model, ids, batch, device):
    out = []
    for s in range(0, ids.shape[0], batch):
        chunk = ids[s:s + batch].to(device)
        out.append(model(chunk).logits.float().cpu())
    return torch.cat(out, 0)


def kl_and_ppl(ref_logits, rec_logits, ids):
    """KL(ref || rec) media por posicao, e perplexidade sob rec nos tokens reais."""
    p = F.softmax(ref_logits, dim=-1)
    logp = F.log_softmax(ref_logits, dim=-1)
    logq = F.log_softmax(rec_logits, dim=-1)
    kl = (p * (logp - logq)).sum(-1).mean().item()
    # ppl: -log q(token verdadeiro) nas posicoes 0..n-2 prevendo 1..n-1
    tgt = ids[:, 1:]
    lq = logq[:, :-1, :]
    nll = -lq.gather(-1, tgt.unsqueeze(-1)).squeeze(-1).mean().item()
    return kl, float(np.exp(nll))


def run_model(name, args, device):
    tok = AutoTokenizer.from_pretrained(name)
    n = args.seq_len
    RECON["n"] = n
    RECON["D"] = build_dictionary(n, device)
    ids = load_sequences(tok, args.n_seq, n, args.seed)

    # referencia VERDADEIRA: modelo eager original, sem patch
    model = AutoModelForCausalLM.from_pretrained(
        name, attn_implementation="eager", dtype=torch.float32).to(device).eval()
    ref = collect_logits(model, ids, args.batch, device)
    _, ppl_ref = kl_and_ppl(ref, ref, ids)

    # troca p/ a atencao custom "recon"
    model.config._attn_implementation = "recon"
    for sub in model.modules():
        if hasattr(sub, "config"):
            try:
                sub.config._attn_implementation = "recon"
            except Exception:
                pass

    # SANITY: identidade tem que reproduzir o modelo verdadeiro (KL ~ 0).
    # Se nao for ~0, o harness esta errado e os numeros nao valem.
    RECON["mode"] = "identity"
    idy = collect_logits(model, ids, args.batch, device)
    kl_id, _ = kl_and_ppl(ref, idy, ids)

    res = {"ppl_ref": ppl_ref, "kl_identity_sanity": kl_id, "svd": {}, "geom": {}}
    for k in [1, 2, 4, 8, 16, 32]:
        RECON["mode"] = "svd"; RECON["k"] = k
        rl = collect_logits(model, ids, args.batch, device)
        kl, ppl = kl_and_ppl(ref, rl, ids)
        res["svd"][k] = {"kl": kl, "ppl": ppl}
    RECON["mode"] = "geom"
    rl = collect_logits(model, ids, args.batch, device)
    kl, ppl = kl_and_ppl(ref, rl, ids)
    res["geom"] = {"kl": kl, "ppl": ppl, "m_atoms": RECON["D"].shape[1]}

    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2"])
    ap.add_argument("--n_seq", type=int, default=50)
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    AttentionInterface.register("recon", recon_attention_forward)

    results = {}
    for name in args.models:
        print(f"\n===== {name} =====", flush=True)
        try:
            r = run_model(name, args, device)
        except Exception as e:
            import traceback; traceback.print_exc()
            print(f"  FALHOU: {type(e).__name__}: {e}", flush=True)
            results[name] = {"error": f"{type(e).__name__}: {e}"}
            continue
        results[name] = r
        json.dump(results, open(os.path.join(args.out, "phase2_downstream.json"), "w"), indent=2)
        sane = "OK" if r["kl_identity_sanity"] < 1e-3 else "FALHOU (harness invalido!)"
        print(f"  ppl_ref={r['ppl_ref']:.2f}  | sanity KL(identidade)={r['kl_identity_sanity']:.2e} -> {sane}", flush=True)
        print(f"  SVD: " + "  ".join(f"k{k}=KL{r['svd'][k]['kl']:.3f}/ppl{r['svd'][k]['ppl']:.1f}" for k in [1,2,4,8,16,32]), flush=True)
        print(f"  GEOM: KL={r['geom']['kl']:.3f} ppl={r['geom']['ppl']:.1f} ({r['geom']['m_atoms']} atomos)", flush=True)

    print("\n" + "=" * 76)
    print("RESUMO FASE 2 — efeito a jusante (KL orig||recon; menor=preserva melhor)")
    print("=" * 76)
    for name, r in results.items():
        if "error" in r:
            print(f"{name}: ERRO {r['error'][:50]}"); continue
        s8 = r["svd"][8]["kl"]; g = r["geom"]["kl"]
        print(f"{name:>22} | SVD k=8 KL={s8:.3f} | GEOM KL={g:.3f} | geom/svd={g/(s8+1e-12):.1f}x pior")
        # sanity
    print("=" * 76)
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase2_downstream.json'))}")


if __name__ == "__main__":
    main()
