"""
Parte 2, Etapa B — MS-CLEAN estruturado (rádio-astronomia).

Greedy: subtrai do residuo o componente NOMEADO mais forte (sink, banda com
perfil, diagonal de inducao), acumula um "clean model" interpretavel; o que sobra
e modelado por SVD low-rank. Mede:
  - fidelidade de [m atomos nomeados + rank-k residuo] vs SVD-(m+k) (orcamento casado)
  - FRACAO NOMEADA/EDITAVEL da energia (quanto da matriz fica em componentes com nome)
  - ordem de selecao (o que vira nomeado primeiro)

Diferenca p/ Etapa A: ANOVA nomeia so efeito de linha/coluna (sink). Aqui o canal
nomeado e mais rico (banda, inducao), entao MAIS da matriz fica interpretavel a
mesma fidelidade. MP nao-ortogonal (gain 1), rapido, sem NNLS.
"""
import argparse, json, os
import numpy as np
import torch

from phase0_radon_attention import load_sequences, extract_attention
from phase06_profiled_lines import atom_vector
from phase_stats import summ, median_ci_bootstrap

TAUS = [1, 2, 4, 8, 16, 32, 64]
DIAGS = [1, 2, 4, 8, 16, 32, 64]
VERTS = [0, 1, 2]


def build_dict(n):
    cols, labels = [], []
    for c in VERTS:
        cols.append(atom_vector("vert", c, n)); labels.append(("sink" if c == 0 else "vert", c))
    for tau in TAUS:
        cols.append(atom_vector("band", tau, n)); labels.append(("band", tau))
    for d in DIAGS:
        cols.append(atom_vector("diag", d, n)); labels.append(("diag", d))
    return np.stack(cols, axis=1), labels   # D: [n*n, m_atoms]


def msclean(A, D, labels, max_m):
    """MP guloso nomeado. Retorna clean (n*n,), lista de (label, coef)."""
    b = A.ravel().copy()
    R = b.copy()
    clean = np.zeros_like(b)
    chosen = set(); picks = []
    for _ in range(max_m):
        corr = D.T @ R                     # atomos normalizados -> corr = <R, atom>
        for j in chosen:
            corr[j] = -np.inf
        j = int(np.argmax(corr))
        if corr[j] <= 0:
            break
        coef = float(corr[j])
        clean += coef * D[:, j]
        R = b - clean
        chosen.add(j); picks.append((labels[j], coef))
    return clean, picks


def svd_rankk_err(residual_mat, A, clean, ks):
    normA = np.linalg.norm(A) + 1e-12
    U, S, Vt = np.linalg.svd(residual_mat, full_matrices=False)
    out = {}
    for k in ks:
        Rk = (U[:, :k] * S[:k]) @ Vt[:k] if k > 0 else np.zeros_like(residual_mat)
        recon = clean + Rk
        out[k] = float(np.linalg.norm(A - recon) / normA)
    return out


def med(x):
    return float(np.median(x))


def run(model_name, args, device, rng):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, attn_implementation="eager", dtype=torch.float32).to(device).eval()
    n = args.seq_len
    D, labels = build_dict(n)
    ids = load_sequences(tok, args.n_seq, n, args.seed)
    attn = extract_attention(model, ids, args.batch, device)
    attn = [np.nan_to_num(a) for a in attn]
    n_layers, n_heads = len(attn), attn[0].shape[1]

    ms = [1, 3, 5]            # nº de atomos nomeados
    ks = [0, 4, 8, 16]       # rank do residuo
    err = {(m, k): [] for m in ms for k in ks}
    named_frac = {m: [] for m in ms}       # energia nomeada / energia de A
    svd_match = {(m, k): [] for m in ms for k in ks}  # SVD-(m+k) puro
    first_picks = []

    inst = [(int(rng.integers(n_layers)), int(rng.integers(n_heads)), int(rng.integers(attn[0].shape[0])))
            for _ in range(args.n_instances)]
    for (li, hi, si) in inst:
        A = attn[li][si, hi].astype(np.float64)
        normA = np.linalg.norm(A) + 1e-12
        clean_full, picks = msclean(A, D, labels, max(ms))
        first_picks.append([p[0] for p in picks[:3]])
        U, S, Vt = np.linalg.svd(A, full_matrices=False)   # p/ SVD puro casado
        for m in ms:
            # reconstroi clean com m atomos
            clean_m = np.zeros(n * n)
            cm, pk = msclean(A, D, labels, m)
            clean_m = cm
            named_frac[m].append(float(np.linalg.norm(clean_m) / normA))
            resid = (A.ravel() - clean_m).reshape(n, n)
            e = svd_rankk_err(resid, A, clean_m.reshape(n, n), ks)
            for k in ks:
                err[(m, k)].append(e[k])
                kk = m + k
                Sk = (U[:, :kk] * S[:kk]) @ Vt[:kk]
                svd_match[(m, k)].append(float(np.linalg.norm(A - Sk) / normA))

    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    # ordem de selecao agregada
    from collections import Counter
    pos1 = Counter(f"{p[0][0]}_{p[0][1]}" for p in first_picks if len(p) > 0)
    return {
        "ms": ms, "ks": ks,
        "err": {f"{m}+{k}": med(err[(m, k)]) for m in ms for k in ks},
        "svd_match": {f"{m}+{k}": med(svd_match[(m, k)]) for m in ms for k in ks},
        "named_frac": {m: med(named_frac[m]) for m in ms},
        "first_pick_counts": dict(pos1),
        # dispersion (NN revision)
        "named_frac_disp": {m: summ(named_frac[m]) for m in ms},
        "named_frac_ci": {m: median_ci_bootstrap(named_frac[m]) for m in ms},
        "err_disp": {f"{m}+{k}": summ(err[(m, k)]) for m in ms for k in ks},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "EleutherAI/pythia-410m"])
    ap.add_argument("--n_seq", type=int, default=100)
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--n_instances", type=int, default=120)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)

    results = {}
    for m in args.models:
        print(f"\n===== {m} =====", flush=True)
        try:
            r = run(m, args, device, rng)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[m] = {"error": f"{type(e).__name__}: {e}"}; continue
        results[m] = r
        json.dump(results, open(os.path.join(args.out, "phase5_msclean.json"), "w"), indent=2)
        print(f"  primeiro atomo escolhido: {r['first_pick_counts']}", flush=True)
        print(f"  fracao nomeada (m=1/3/5): {r['named_frac']['1']:.2f} / {r['named_frac']['3']:.2f} / {r['named_frac']['5']:.2f}"
              if all(str(x) in r['named_frac'] for x in [1,3,5]) else f"  named_frac: {r['named_frac']}", flush=True)
        print(f"  {'m+k':>6} | {'CLEAN+SVD':>10} | {'SVD-(m+k)':>10}", flush=True)
        for m_ in r["ms"]:
            for k_ in r["ks"]:
                key = f"{m_}+{k_}"
                print(f"  {key:>6} | {r['err'][key]:>10.3f} | {r['svd_match'][key]:>10.3f}", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, 'phase5_msclean.json'))}")


if __name__ == "__main__":
    main()
