"""
Parte 2, Etapa C — Robust PCA estruturado (MCA por minimizacao alternada).

A = S + L, com S = combinacao NAO-NEGATIVA de atomos NOMEADOS (sink, bandas com
perfil, diagonais de inducao) e L = residuo LOW-RANK (rank r). Otimizacao conjunta
por block-coordinate (estilo MCA), em vez do guloso da Etapa B:

  repete: S <- NNLS(D, A - L)           # canal estruturado nomeado
          L <- rank-r SVD(A - S)        # canal low-rank fiel

Mede: erro final ||A-S-L||, fracao nomeada ||S||/||A||, nº de atomos ativos, e
compara com SVD puro de rank casado (n_ativos + r). Pergunta: o refino conjunto
fecha o gap que o guloso (B) tinha, mantendo alta interpretabilidade?
"""
import argparse, json, os
import numpy as np
import torch
from scipy.optimize import nnls

from phase0_radon_attention import load_sequences, extract_attention
from phase5_msclean import build_dict
from phase_stats import summ, median_ci_bootstrap


def srpca(A, D, r, iters=5):
    n = A.shape[0]
    b = A.ravel()
    normA = np.linalg.norm(b) + 1e-12
    L = np.zeros((n, n))
    coef = np.zeros(D.shape[1])
    for _ in range(iters):
        coef, _ = nnls(D, b - L.ravel())          # S estruturado nomeado
        S = (D @ coef).reshape(n, n)
        resid = A - S
        U, s, Vt = np.linalg.svd(resid, full_matrices=False)
        L = (U[:, :r] * s[:r]) @ Vt[:r] if r > 0 else np.zeros((n, n))
    S = (D @ coef).reshape(n, n)
    err = float(np.linalg.norm(A - S - L) / normA)
    named_frac = float(np.linalg.norm(S) / (np.linalg.norm(A) + 1e-12))
    n_active = int((coef > 1e-4 * (coef.max() + 1e-12)).sum())
    return err, named_frac, n_active, coef


def svd_err(A, k):
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    Ak = (U[:, :k] * s[:k]) @ Vt[:k]
    return float(np.linalg.norm(A - Ak) / (np.linalg.norm(A) + 1e-12))


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

    rs = [4, 8, 16]
    err = {r: [] for r in rs}; nf = {r: [] for r in rs}; na = {r: [] for r in rs}
    svd_match = {r: [] for r in rs}
    inst = [(int(rng.integers(n_layers)), int(rng.integers(n_heads)), int(rng.integers(attn[0].shape[0])))
            for _ in range(args.n_instances)]
    for (li, hi, si) in inst:
        A = attn[li][si, hi].astype(np.float64)
        for r in rs:
            e, f, a, _ = srpca(A, D, r, iters=args.iters)
            err[r].append(e); nf[r].append(f); na[r].append(a)
            svd_match[r].append(svd_err(A, a + r))   # SVD de rank casado (n_ativos + r)

    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return {
        "rs": rs,
        "err": {r: med(err[r]) for r in rs},
        "named_frac": {r: med(nf[r]) for r in rs},
        "n_active": {r: med(na[r]) for r in rs},
        "svd_matched": {r: med(svd_match[r]) for r in rs},
        # dispersion (NN revision)
        "err_disp": {r: summ(err[r]) for r in rs},
        "named_frac_disp": {r: summ(nf[r]) for r in rs},
        "svd_matched_disp": {r: summ(svd_match[r]) for r in rs},
        "named_frac_ci": {r: median_ci_bootstrap(nf[r]) for r in rs},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "EleutherAI/pythia-410m"])
    ap.add_argument("--n_seq", type=int, default=100)
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--n_instances", type=int, default=120)
    ap.add_argument("--iters", type=int, default=5)
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
        json.dump(results, open(os.path.join(args.out, "phase6_srpca.json"), "w"), indent=2)
        print(f"  {'r':>3} | {'S+L err':>8} | {'SVD casado':>10} | {'named%':>7} | {'#ativos':>7}", flush=True)
        for rr in r["rs"]:
            print(f"  {rr:>3} | {r['err'][rr]:>8.3f} | {r['svd_matched'][rr]:>10.3f} | {r['named_frac'][rr]*100:>6.1f}% | {r['n_active'][rr]:>7.1f}", flush=True)

    print("\n" + "=" * 64)
    print("RESUMO ETAPA C — Robust PCA estruturado")
    print("=" * 64)
    ok = [r for r in results.values() if "error" not in r]
    if ok:
        close = all(r["err"][8] <= 1.10 * r["svd_matched"][8] for r in ok)
        named = all(r["named_frac"][8] > 0.7 for r in ok)
        print(f"S+L ~= SVD casado (r=8, <=1.1x): {close}")
        print(f"fracao nomeada alta (>70% em r=8): {named}")
        if close and named:
            print("=> S+L iguala a fidelidade do SVD com >70% da energia em componentes nomeados/editaveis.")
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase6_srpca.json'))}")


if __name__ == "__main__":
    main()
