"""
Parte 3 (A1) — editabilidade como GANHO DE TAREFA (lost-in-the-middle).

Sonda de recuperacao posicional (induction copy):
  - sequencia de tokens aleatorios de comprimento n
  - planta um par [M][X] na posicao p (M = marcador fixo, X = alvo aleatorio)
  - termina a sequencia com [M]; o modelo deve prever X (cópia via induction head)
  - varia p ao longo do contexto -> curva acuracia(p)  (tipicamente em U: bom no
    inicio/fim, pior no meio = lost-in-the-middle)

Intervencao: CALIBRA O SINK (atenua a coluna 0 por beta e renormaliza). Como a
Parte 2 mostrou que o sink E a coluna 0, isto e uma edicao NOMEADA direta. Mede se
a acuracia no MEIO melhora -> editabilidade vira ganho de tarefa, nao so KL.

Injecao via implementacao de atencao "recon" (mascara causal pura, como phase7).
"""
import argparse, json, os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, AttentionInterface

RECON = {"beta": 1.0}


def _repeat_kv(x, nrep):
    if nrep == 1:
        return x
    b, h, s, d = x.shape
    return x[:, :, None, :, :].expand(b, h, nrep, s, d).reshape(b, h * nrep, s, d)


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
    beta = RECON["beta"]
    if beta != 1.0:                      # calibra o sink = coluna 0
        aw = aw.clone()
        aw[..., 0] = aw[..., 0] * beta
        aw = aw / aw.sum(-1, keepdim=True).clamp_min(1e-9)
    out = torch.matmul(aw, value).transpose(1, 2)
    return out, aw


TAG = [101, 202, 303, 404]   # tag fixa de varios tokens (match inequivoco p/ induction)


def filler_pool(tok, n_needed, seed):
    """Stream de tokens de TEXTO REAL (contexto coerente prima a induction)."""
    ids = []
    with open("wikitext2_train.txt", "r", encoding="utf-8") as f:
        for ln in f:
            if len(ln.strip()) < 80:
                continue
            ids.extend(tok(ln.strip())["input_ids"])
            if len(ids) > n_needed:
                break
    return np.array(ids)


def build_probe(pool, vocab, n, positions, n_per_pos, rng):
    """Retorna {p: (input_ids [N,n], target [N])}. Filler real + tag multi-token + alvo."""
    L = len(TAG)
    out = {}
    tagset = set(TAG)
    content = np.array([t for t in pool if t not in tagset and t < vocab])
    for p in positions:
        rows, Xs = [], []
        for _ in range(n_per_pos):
            st = int(rng.integers(0, len(pool) - n - 1))
            seq = pool[st:st + n].copy()
            X = int(rng.choice(content))
            seq[p:p + L] = TAG                 # planta a tag na posicao p
            seq[p + L] = X                     # alvo logo apos a tag
            seq[n - L:n] = TAG                 # termina com a tag -> preve X
            rows.append(seq); Xs.append(X)
        out[p] = (torch.tensor(np.array(rows), dtype=torch.long), torch.tensor(Xs, dtype=torch.long))
    return out


@torch.no_grad()
def accuracy_by_pos(model, probe, device, batch=16):
    acc = {}
    for p, (ids, X) in probe.items():
        correct = 0
        for s in range(0, ids.shape[0], batch):
            chunk = ids[s:s + batch].to(device)
            logits = model(chunk).logits[:, -1, :]      # preve o token apos o ultimo M
            pred = logits.argmax(-1).cpu()
            correct += int((pred == X[s:s + batch]).sum())
        acc[p] = correct / ids.shape[0]
    return acc


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

    res = {}
    for beta in args.betas:
        RECON["beta"] = beta
        res[str(beta)] = accuracy_by_pos(model, probe, device, args.batch)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return {"positions": positions, "acc": res}


def midmean(acc, positions):
    mids = [p for p in positions if 0.25 * positions[-1] < p < 0.75 * positions[-1]]
    return float(np.mean([acc[p] for p in mids]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2-medium", "EleutherAI/pythia-1.4b"])
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--n_per_pos", type=int, default=80)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--betas", nargs="*", type=float, default=[1.0, 0.5, 0.25, 0.0])
    ap.add_argument("--tag", default="", help="sufixo do arquivo de saida (versionado, nunca sobrescreve)")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    AttentionInterface.register("recon", recon_attention_forward)

    fname = f"phase8_lostmiddle{('_' + args.tag) if args.tag else ''}.json"
    results = {"_meta": {"n_per_pos": args.n_per_pos, "seed": args.seed,
                         "betas": args.betas, "seq_len": args.seq_len}}
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
        print("  pos:        " + " ".join(f"{p:>4}" for p in pos), flush=True)
        for beta in [str(b) for b in args.betas]:
            a = r["acc"][beta]
            print(f"  beta={beta:>4}: " + " ".join(f"{a[p]:.2f}" for p in pos) + f"   | meio={midmean(a, pos):.3f}", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, fname))}")


if __name__ == "__main__":
    main()
