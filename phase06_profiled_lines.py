"""
Fase 0.6 — teste decisivo do angulo de linha, com atomos COM PERFIL.

A Fase 0.5 falhou porque os atomos de linha eram uniformes (peso igual ao longo
da linha), e a atencao real e uma banda com decaimento. Aqui o dicionario ganha
perfil:
  - banda com decaimento exponencial, parametrizada por timescale tau:
        B_tau[i,j] = exp(-(i-j)/tau)   para j<=i   (captura atencao local com alcance tau)
  - vertical na coluna c (sink quando c=0)
  - diagonal nitida de offset d (induction head: copia a d tokens de distancia)

Mesmo OMP nao-negativo + comparacao com rank-k SVD da Fase 0.5.

Pergunta: poucas k primitivas COM PERFIL reconstroem a atencao perto do otimo
rank-k? Se sim, a estrutura e geometrica e a compressao volta ao jogo. Se nem
assim baterem o SVD, veredito definitivo: low-rank domina compressao.
"""

import argparse
import json
import os
import numpy as np
import torch
from scipy.optimize import nnls

from phase0_radon_attention import load_sequences, extract_attention


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="gpt2")
    p.add_argument("--n_seq", type=int, default=100)
    p.add_argument("--seq_len", type=int, default=128)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--n_instances", type=int, default=80)
    p.add_argument("--max_k", type=int, default=32)
    p.add_argument("--class_k", type=int, default=6)
    p.add_argument("--out", default="out")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--gate_k", type=int, default=8)
    p.add_argument("--gate_err", type=float, default=0.25)
    return p.parse_args()


TAUS = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]


def band_profile(tau, n):
    o = np.arange(n)
    return np.exp(-o / tau)              # peso por offset o = i-j


def atom_vector(kind, param, n):
    """Vetor normalizado (n*n,) de um atomo com perfil."""
    M = np.zeros((n, n), dtype=np.float64)
    if kind == "band":
        w = band_profile(param, n)
        for o in range(n):
            if w[o] < 1e-6:
                break
            ii = np.arange(o, n)
            M[ii, ii - o] = w[o]
    elif kind == "diag":                 # offset nitido
        d = int(param); ii = np.arange(d, n)
        M[ii, ii - d] = 1.0
    else:                                # "vert": coluna param
        c = int(param); ii = np.arange(c, n)
        M[ii, c] = 1.0
    nrm = np.linalg.norm(M)
    return (M / nrm).ravel() if nrm > 0 else M.ravel()


def precompute_band_norms(n):
    counts = (n - np.arange(n)).astype(np.float64)
    norms = {}
    for tau in TAUS:
        w = band_profile(tau, n)
        norms[tau] = float(np.sqrt(np.sum(counts * w * w)))
    return norms


def best_atom(R, n, band_norms, chosen_set):
    """Atomo de maior correlacao com o residuo R, fora dos ja escolhidos."""
    diag_sum = np.array([np.trace(R, offset=-d) for d in range(n)])  # soma por offset
    counts = n - np.arange(n)
    col_sum = R.sum(axis=0)

    diag_corr = diag_sum / np.sqrt(counts)
    vert_corr = col_sum / np.sqrt(counts)
    band_corr = {}
    for tau in TAUS:
        w = band_profile(tau, n)
        band_corr[tau] = float(np.sum(w * diag_sum) / (band_norms[tau] + 1e-12))

    best = (None, None, -np.inf)
    for tau in TAUS:
        if ("band", tau) not in chosen_set and band_corr[tau] > best[2]:
            best = ("band", tau, band_corr[tau])
    for d in range(n):
        if ("diag", d) not in chosen_set and diag_corr[d] > best[2]:
            best = ("diag", d, diag_corr[d])
    for c in range(n):
        if ("vert", c) not in chosen_set and vert_corr[c] > best[2]:
            best = ("vert", c, vert_corr[c])
    return best[0], best[1]


def omp_profiled(A, max_k, n, checkpoints, band_norms):
    b = A.ravel(); normb = np.linalg.norm(b) + 1e-12
    chosen, chosen_set, cols = [], set(), []
    recon = np.zeros_like(b); errs = {}; coefs = None
    for step in range(1, max_k + 1):
        R = (b - recon).reshape(n, n)
        kind, param = best_atom(R, n, band_norms, chosen_set)
        chosen.append((kind, param)); chosen_set.add((kind, param))
        cols.append(atom_vector(kind, param, n))
        M = np.stack(cols, axis=1)
        coefs, _ = nnls(M, b)
        recon = M @ coefs
        if step in checkpoints:
            errs[step] = float(np.linalg.norm(recon - b) / normb)
    support = [(chosen[j][0], chosen[j][1], float(coefs[j])) for j in range(len(chosen))]
    return errs, support


def svd_errors(A, checkpoints):
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    normA = np.linalg.norm(A) + 1e-12
    return {k: float(np.linalg.norm((U[:, :k] * S[:k]) @ Vt[:k] - A) / normA) for k in checkpoints}


def classify_support(support):
    energy = {"banda_local": 0.0, "sink": 0.0, "vertical_outra": 0.0, "diag_inducao": 0.0}
    tot = sum(c * c for (_, _, c) in support) + 1e-12
    for (kind, param, c) in support:
        e = c * c
        if kind == "band":
            energy["banda_local"] += e
        elif kind == "vert":
            energy["sink" if param == 0 else "vertical_outra"] += e
        else:
            energy["banda_local" if param <= 2 else "diag_inducao"] += e
    return {k: v / tot for k, v in energy.items()}


def main():
    args = get_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    n = args.seq_len
    rng = np.random.default_rng(args.seed)
    checkpoints = [k for k in [1, 2, 4, 8, 16, 32] if k <= args.max_k]
    band_norms = precompute_band_norms(n)

    print(f"[setup] device={device} model={args.model} n_seq={args.n_seq} seq_len={n} taus={TAUS}")
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, attn_implementation="eager").to(device).eval()

    print("[data] carregando sequencias ...")
    input_ids = load_sequences(tok, args.n_seq, n, args.seed)
    print("[extract] forward pass com atencao eager ...")
    attn = extract_attention(model, input_ids, args.batch, device)
    n_layers, n_heads = len(attn), attn[0].shape[1]
    print(f"[extract] {n_layers} camadas x {n_heads} cabecas")

    print(f"[recon] OMP de linhas COM PERFIL vs SVD em {args.n_instances} instancias ...")
    inst = [(int(rng.integers(n_layers)), int(rng.integers(n_heads)), int(rng.integers(attn[0].shape[0])))
            for _ in range(args.n_instances)]
    line_curve = {k: [] for k in checkpoints}; svd_curve = {k: [] for k in checkpoints}
    for (li, hi, si) in inst:
        A = attn[li][si, hi].astype(np.float64)
        errs, _ = omp_profiled(A, args.max_k, n, checkpoints, band_norms)
        se = svd_errors(A, checkpoints)
        for k in checkpoints:
            line_curve[k].append(errs[k]); svd_curve[k].append(se[k])
    line_med = {k: float(np.median(line_curve[k])) for k in checkpoints}
    svd_med = {k: float(np.median(svd_curve[k])) for k in checkpoints}

    print(f"[class] decompondo cada cabeca (k={args.class_k}) ...")
    dom_counter = {}
    for li in range(n_layers):
        for hi in range(n_heads):
            Abar = attn[li][:, hi].mean(axis=0).astype(np.float64)
            _, support = omp_profiled(Abar, args.class_k, n, {args.class_k}, band_norms)
            dom = max(classify_support(support).items(), key=lambda x: x[1])[0]
            dom_counter[dom] = dom_counter.get(dom, 0) + 1

    gate_err = line_med.get(args.gate_k, 1.0); svd_ref = svd_med.get(args.gate_k, 1.0)
    go = gate_err < args.gate_err
    near_svd = gate_err < 1.5 * svd_ref

    results = {
        "model": args.model, "seq_len": n, "taus": TAUS, "checkpoints": checkpoints,
        "line_profiled_median_err": line_med, "svd_median_err": svd_med,
        "head_type_distribution": dom_counter,
        "gate": {"k": args.gate_k, "line_err": gate_err, "svd_err": svd_ref,
                 "go": bool(go), "near_svd": bool(near_svd)},
    }
    with open(os.path.join(args.out, "phase06_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 64)
    print("RESULTADO FASE 0.6 — reconstrucao por bandas COM perfil")
    print("=" * 64)
    print(f"{'k':>4} | {'linhas perfil':>14} | {'rank-k SVD':>12} | razao")
    print("-" * 64)
    for k in checkpoints:
        print(f"{k:>4} | {line_med[k]:>14.3f} | {svd_med[k]:>12.3f} | {line_med[k]/(svd_med[k]+1e-12):>5.2f}")
    print("-" * 64)
    print("cabecas por primitiva dominante:")
    for cls, cnt in sorted(dom_counter.items(), key=lambda x: -x[1]):
        print(f"  {cls:>16}: {cnt:3d}  ({100*cnt/(n_layers*n_heads):.1f}%)")
    print("-" * 64)
    print(f"erro com k={args.gate_k}: {gate_err:.3f}  (SVD rank-{args.gate_k}: {svd_ref:.3f}, razao {gate_err/(svd_ref+1e-12):.2f})")
    if go and near_svd:
        print("VEREDITO: GO FORTE -> bandas com perfil reconstroem perto do otimo rank-k.")
        print("          A estrutura E geometrica. Compressao geometrica volta ao jogo.")
    elif go:
        print("VEREDITO: GO -> reconstroi com erro baixo, mas ainda atras do SVD.")
        print("          Geometria captura o grosso; resto e low-rank difuso.")
    else:
        print("VEREDITO: NO-GO DEFINITIVO -> nem com perfil as linhas batem o SVD.")
        print("          Low-rank domina compressao. Projeto foca em interpretabilidade/edicao.")
    print("=" * 64)

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        plt.figure(figsize=(7, 5))
        plt.plot(checkpoints, [line_med[k] for k in checkpoints], marker="o", label="bandas com perfil (OMP)")
        plt.plot(checkpoints, [svd_med[k] for k in checkpoints], marker="s", label="rank-k SVD (piso)")
        plt.xscale("log", base=2); plt.xlabel("k componentes"); plt.ylabel("erro relativo (mediana)")
        plt.title("Fase 0.6: bandas com perfil vs SVD"); plt.legend(); plt.grid(True, alpha=0.3)
        plt.tight_layout(); plt.savefig(os.path.join(args.out, "phase06_recon_curve.png"), dpi=120); plt.close()
        print(f"[plots] {os.path.abspath(args.out)}")
    except Exception as e:
        print(f"[plots] pulado ({e})")
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase06_results.json'))}")


if __name__ == "__main__":
    main()
