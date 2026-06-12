"""
Fase 0.5 — corrige o furo da Fase 0.

A Fase 0 provou que a atencao e concentrada no dominio de Radon (energia em
~0.17% do sinograma), mas a reconstrucao via iradon (filtered back-projection)
falhou (erro ~0.5 com o sinograma inteiro). Conclusao: FBP e o inverso errado
pra uma matriz triangular esparsa feita de linhas-delta.

Aqui troco a inversa de Radon por DETECCAO DE LINHAS + reconstrucao parametrica,
que e o que a hipotese realmente afirma: A ~= soma de k primitivas de linha.

Dicionario de linhas consciente da atencao (= as linhas que um Hough detectaria,
mas restritas aos eixos que importam numa matriz causal):
  - diagonais de offset d:  atende d tokens atras  (d=0..2 = banda local; d>=3 = indução/offset)
  - verticais na coluna c:  todos atendem ao token c (c=0 = attention sink)

Algoritmo: Orthogonal Matching Pursuit com coeficientes nao-negativos (NNLS).
A cada passo escolhe a linha mais correlacionada com o residuo, refita por NNLS,
mede erro relativo. Curva de erro vs k.

Baselines de contexto:
  - rank-k SVD: melhor reconstrucao linear possivel com k componentes (piso teorico)
  - top-k entradas: esparsidade trivial

Saida adicional: classificacao de cada cabeca por primitiva dominante
(banda local / sink / diagonal de inducao), a leitura interpretavel da proposta.

NAO treina nada. Roda na RTX 3060 em poucos minutos.
"""

import argparse
import json
import os
import numpy as np
import torch
from scipy.optimize import nnls

# reusa os helpers de dados da Fase 0 (importar nao roda o main, esta guardado)
from phase0_radon_attention import load_sequences, extract_attention


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="gpt2")
    p.add_argument("--n_seq", type=int, default=100)
    p.add_argument("--seq_len", type=int, default=128)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--n_instances", type=int, default=80, help="amostra (seq,camada,cabeca) p/ a curva")
    p.add_argument("--max_k", type=int, default=32)
    p.add_argument("--class_k", type=int, default=6, help="k usado na classificacao por cabeca")
    p.add_argument("--out", default="out")
    p.add_argument("--seed", type=int, default=0)
    # gate: erro mediano de reconstrucao com k=8 linhas abaixo deste valor => compressao vive
    p.add_argument("--gate_k", type=int, default=8)
    p.add_argument("--gate_err", type=float, default=0.25)
    return p.parse_args()


# ---------- dicionario de linhas (atomos esparsos) ----------

def atom_vector(kind, idx, n):
    """Vetor normalizado (n*n,) de um atomo de linha causal."""
    M = np.zeros((n, n), dtype=np.float64)
    if kind == "diag":          # i - j = idx  (atende idx tokens atras)
        i = np.arange(idx, n)
        M[i, i - idx] = 1.0
    else:                       # "vert": coluna idx (todos i>=idx atendem ao token idx)
        i = np.arange(idx, n)
        M[i, idx] = 1.0
    nrm = np.linalg.norm(M)
    return (M / nrm).ravel() if nrm > 0 else M.ravel()


def correlations(R, n):
    """Correlacao de cada atomo com o residuo R (n x n). Vetorizado.
    Retorna dois arrays: diag[d] e vert[c], ja normalizados pela norma do atomo
    (atomo binario com m uns -> norma sqrt(m); <R,atomo>/sqrt(m) = soma/sqrt(m))."""
    counts_d = n - np.arange(n)                       # m de cada diagonal
    diag_sum = np.array([np.trace(R, offset=-d) for d in range(n)])
    diag = diag_sum / np.sqrt(counts_d)
    counts_c = n - np.arange(n)                       # m de cada vertical causal
    vert_sum = R.sum(axis=0)                          # triangulo superior ~0, entao = soma causal
    vert = vert_sum / np.sqrt(counts_c)
    return diag, vert


def omp_line(A, max_k, n, checkpoints):
    """OMP nao-negativo no dicionario de linhas. Retorna {k: erro_rel} e o suporte final
    como lista de (kind, idx, coef)."""
    b = A.ravel()
    normb = np.linalg.norm(b) + 1e-12
    chosen = []          # (kind, idx)
    chosen_set = set()
    cols = []            # vetores dos atomos escolhidos
    recon = np.zeros_like(b)
    errs = {}
    coefs = None
    for step in range(1, max_k + 1):
        R = (b - recon).reshape(n, n)
        diag, vert = correlations(R, n)
        # zera os ja escolhidos
        for (k_, i_) in chosen:
            if k_ == "diag":
                diag[i_] = -np.inf
            else:
                vert[i_] = -np.inf
        bd, bv = int(np.argmax(diag)), int(np.argmax(vert))
        if diag[bd] >= vert[bv]:
            pick = ("diag", bd)
        else:
            pick = ("vert", bv)
        chosen.append(pick); chosen_set.add(pick)
        cols.append(atom_vector(pick[0], pick[1], n))
        M = np.stack(cols, axis=1)               # (n*n, step)
        coefs, _ = nnls(M, b)
        recon = M @ coefs
        if step in checkpoints:
            errs[step] = float(np.linalg.norm(recon - b) / normb)
    support = [(chosen[j][0], chosen[j][1], float(coefs[j])) for j in range(len(chosen))]
    return errs, support


def svd_errors(A, checkpoints):
    """Erro relativo de reconstrucao rank-k (piso teorico para k componentes lineares)."""
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    normA = np.linalg.norm(A) + 1e-12
    out = {}
    for k in checkpoints:
        Ak = (U[:, :k] * S[:k]) @ Vt[:k]
        out[k] = float(np.linalg.norm(Ak - A) / normA)
    return out


def topk_entry_error(A, checkpoints_entries):
    """Erro mantendo as k maiores entradas (esparsidade trivial), k em fracao de n*n."""
    b = A.ravel(); normb = np.linalg.norm(b) + 1e-12
    order = np.argsort(np.abs(b))[::-1]
    out = {}
    for k in checkpoints_entries:
        keep = np.zeros_like(b); keep[order[:k]] = b[order[:k]]
        out[k] = float(np.linalg.norm(keep - b) / normb)
    return out


def classify_support(support, n):
    """Fracao de energia por classe de primitiva (coef^2, atomos normalizados)."""
    energy = {"banda_local": 0.0, "sink": 0.0, "vertical_outra": 0.0, "diag_inducao": 0.0}
    tot = sum(c * c for (_, _, c) in support) + 1e-12
    for (kind, idx, c) in support:
        e = c * c
        if kind == "vert":
            energy["sink" if idx == 0 else "vertical_outra"] += e
        else:
            energy["banda_local" if idx <= 2 else "diag_inducao"] += e
    return {k: v / tot for k, v in energy.items()}


def main():
    args = get_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    n = args.seq_len
    rng = np.random.default_rng(args.seed)
    checkpoints = [k for k in [1, 2, 4, 8, 16, 32] if k <= args.max_k]

    print(f"[setup] device={device} model={args.model} n_seq={args.n_seq} seq_len={n}")
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, attn_implementation="eager").to(device).eval()

    print("[data] carregando sequencias ...")
    input_ids = load_sequences(tok, args.n_seq, n, args.seed)
    print("[extract] forward pass com atencao eager ...")
    attn = extract_attention(model, input_ids, args.batch, device)
    n_layers, n_heads = len(attn), attn[0].shape[1]
    print(f"[extract] {n_layers} camadas x {n_heads} cabecas")

    # ---------- curva de reconstrucao vs k (amostra de instancias) ----------
    print(f"[recon] OMP de linhas vs SVD em {args.n_instances} instancias ...")
    inst = []
    for _ in range(args.n_instances):
        li = int(rng.integers(n_layers)); hi = int(rng.integers(n_heads)); si = int(rng.integers(attn[0].shape[0]))
        inst.append((li, hi, si))
    line_curve = {k: [] for k in checkpoints}
    svd_curve = {k: [] for k in checkpoints}
    for (li, hi, si) in inst:
        A = attn[li][si, hi].astype(np.float64)
        errs, _ = omp_line(A, args.max_k, n, checkpoints)
        se = svd_errors(A, checkpoints)
        for k in checkpoints:
            line_curve[k].append(errs[k]); svd_curve[k].append(se[k])
    line_med = {k: float(np.median(line_curve[k])) for k in checkpoints}
    svd_med = {k: float(np.median(svd_curve[k])) for k in checkpoints}

    # ---------- classificacao por cabeca (mapa medio) ----------
    print(f"[class] decompondo cada cabeca (k={args.class_k}) ...")
    head_class = {}
    dom_counter = {}
    for li in range(n_layers):
        for hi in range(n_heads):
            Abar = attn[li][:, hi].mean(axis=0).astype(np.float64)
            _, support = omp_line(Abar, args.class_k, n, {args.class_k})
            frac = classify_support(support, n)
            dom = max(frac, key=frac.get)
            head_class[f"L{li}H{hi}"] = {"frac": frac, "dom": dom}
            dom_counter[dom] = dom_counter.get(dom, 0) + 1

    # ---------- veredito ----------
    gate_err = line_med.get(args.gate_k, 1.0)
    svd_ref = svd_med.get(args.gate_k, 1.0)
    go = gate_err < args.gate_err
    near_svd = gate_err < 1.5 * svd_ref

    results = {
        "model": args.model, "n_seq": args.n_seq, "seq_len": n,
        "checkpoints": checkpoints,
        "line_omp_median_err": line_med,
        "svd_median_err": svd_med,
        "head_type_distribution": dom_counter,
        "gate": {"k": args.gate_k, "line_err": gate_err, "svd_err": svd_ref,
                 "threshold": args.gate_err, "go": bool(go), "near_svd": bool(near_svd)},
    }
    with open(os.path.join(args.out, "phase05_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 64)
    print("RESULTADO FASE 0.5 — reconstrucao por primitivas de linha")
    print("=" * 64)
    print(f"{'k':>4} | {'linhas (OMP)':>14} | {'rank-k SVD':>12} | razao linha/SVD")
    print("-" * 64)
    for k in checkpoints:
        ratio = line_med[k] / (svd_med[k] + 1e-12)
        print(f"{k:>4} | {line_med[k]:>14.3f} | {svd_med[k]:>12.3f} | {ratio:>6.2f}")
    print("-" * 64)
    print("distribuicao de cabecas por primitiva dominante:")
    for cls, cnt in sorted(dom_counter.items(), key=lambda x: -x[1]):
        print(f"  {cls:>16}: {cnt:3d}  ({100*cnt/(n_layers*n_heads):.1f}%)")
    print("-" * 64)
    print(f"erro com k={args.gate_k} linhas: {gate_err:.3f}  (SVD rank-{args.gate_k}: {svd_ref:.3f})")
    if go and near_svd:
        print("VEREDITO: GO FORTE -> poucas linhas reconstroem a atencao, e perto do otimo")
        print("          rank-k. O dicionario de linhas e uma base correta. Compressao vive,")
        print("          alegacao de edicao por primitiva fica plausivel. Seguir p/ Fase 1.")
    elif go:
        print("VEREDITO: GO -> poucas linhas reconstroem com erro baixo (mas longe do SVD;")
        print("          parte da estrutura nao e puramente linear). Compressao vive.")
    else:
        print("VEREDITO: PARCIAL/NO-GO -> k linhas nao reconstroem bem. A concentracao de")
        print("          Radon era real mas a estrutura nao e capturada por este dicionario.")
        print("          Inspecionar: aumentar k, ou ampliar o dicionario (blocos, anti-diagonais).")
    print("=" * 64)

    # ---------- plots ----------
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        plt.figure(figsize=(7, 5))
        plt.plot(checkpoints, [line_med[k] for k in checkpoints], marker="o", label="primitivas de linha (OMP)")
        plt.plot(checkpoints, [svd_med[k] for k in checkpoints], marker="s", label="rank-k SVD (piso)")
        plt.xscale("log", base=2); plt.xlabel("k componentes"); plt.ylabel("erro relativo (mediana)")
        plt.title("Reconstrucao da atencao: linhas vs SVD"); plt.legend(); plt.grid(True, alpha=0.3)
        plt.tight_layout(); plt.savefig(os.path.join(args.out, "phase05_recon_curve.png"), dpi=120); plt.close()

        plt.figure(figsize=(7, 4))
        cls = sorted(dom_counter, key=lambda x: -dom_counter[x])
        plt.bar(cls, [dom_counter[c] for c in cls], color="#4c72b0")
        plt.ylabel("numero de cabecas"); plt.title(f"Cabecas por primitiva dominante (k={args.class_k})")
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout(); plt.savefig(os.path.join(args.out, "phase05_head_types.png"), dpi=120); plt.close()
        print(f"[plots] {os.path.abspath(args.out)}")
    except Exception as e:
        print(f"[plots] pulado ({e})")
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase05_results.json'))}")


if __name__ == "__main__":
    main()
