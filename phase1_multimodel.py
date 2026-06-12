"""
Fase 1 (extensao) — replicacao multi-modelo do resultado central.

Mata a fraqueza "um modelo so". Para cada modelo aberto (arquiteturas distintas:
posicao absoluta vs rotary vs GQA) mede:
  - concentracao de Radon: razao suporte_real / suporte_aleatorio
  - reconstrucao em k: linhas uniformes (OMP) vs bandas com perfil (OMP) vs rank-k SVD
  - distribuicao de primitiva dominante por cabeca

Se o padrao (linhas travam ~0.5, SVD desce, low-rank domina) se repetir em todos,
a conclusao generaliza. Roda na RTX 3060 (fp16, seq curta).
"""
import argparse, json, os
import numpy as np
import torch

from phase0_radon_attention import (
    load_sequences, extract_attention, radon_support_fraction, make_controls,
)
from phase05_line_decomposition import omp_line, svd_errors
from phase06_profiled_lines import omp_profiled, precompute_band_norms, classify_support

DEFAULT_MODELS = [
    "gpt2",                    # 124M, posicao absoluta aprendida
    "gpt2-medium",             # 355M, idem (escala)
    "EleutherAI/pythia-410m",  # rotary, parallel attn
    "EleutherAI/pythia-1.4b",  # rotary, maior
    "Qwen/Qwen2.5-0.5B",       # rotary + GQA, moderno
]


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("--models", nargs="*", default=DEFAULT_MODELS)
    p.add_argument("--n_seq", type=int, default=200)
    p.add_argument("--seq_len", type=int, default=128)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--n_sample_conc", type=int, default=10, help="seqs p/ concentracao")
    p.add_argument("--n_instances", type=int, default=60, help="instancias p/ recon")
    p.add_argument("--max_k", type=int, default=32)
    p.add_argument("--out", default="out")
    p.add_argument("--seed", type=int, default=0)
    return p.parse_args()


def run_model(name, args, theta, band_norms, checkpoints, rng):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    n = args.seq_len
    tok = AutoTokenizer.from_pretrained(name)
    # fp32: fp16 deixa a atencao do GPTNeoX/pythia com NaN. Os modelos aqui cabem em fp32 na 3060.
    model = AutoModelForCausalLM.from_pretrained(
        name, attn_implementation="eager", dtype=torch.float32).to(device).eval()
    ids = load_sequences(tok, args.n_seq, n, args.seed)
    attn = extract_attention(model, ids, args.batch, device)
    attn = [np.nan_to_num(a, nan=0.0, posinf=0.0, neginf=0.0) for a in attn]  # guard
    n_layers, n_heads = len(attn), attn[0].shape[1]

    # concentracao
    real = []
    for li in range(n_layers):
        for hi in range(n_heads):
            for si in range(args.n_sample_conc):
                real.append(radon_support_fraction(attn[li][si, hi], theta)[0])
    _, rand_batch = make_controls(n, 40, rng)
    rand = [radon_support_fraction(rand_batch[i], theta)[0] for i in range(rand_batch.shape[0])]
    real_med, rand_med = float(np.median(real)), float(np.median(rand))

    # reconstrucao
    inst = [(int(rng.integers(n_layers)), int(rng.integers(n_heads)), int(rng.integers(attn[0].shape[0])))
            for _ in range(args.n_instances)]
    uni = {k: [] for k in checkpoints}; prof = {k: [] for k in checkpoints}; svd = {k: [] for k in checkpoints}
    for (li, hi, si) in inst:
        A = attn[li][si, hi].astype(np.float64)
        eu, _ = omp_line(A, args.max_k, n, checkpoints)
        ep, _ = omp_profiled(A, args.max_k, n, checkpoints, band_norms)
        es = svd_errors(A, checkpoints)
        for k in checkpoints:
            uni[k].append(eu[k]); prof[k].append(ep[k]); svd[k].append(es[k])
    uni_med = {k: float(np.median(uni[k])) for k in checkpoints}
    prof_med = {k: float(np.median(prof[k])) for k in checkpoints}
    svd_med = {k: float(np.median(svd[k])) for k in checkpoints}

    # primitiva dominante
    dom = {}
    for li in range(n_layers):
        for hi in range(n_heads):
            Abar = attn[li][:, hi].mean(axis=0).astype(np.float64)
            _, support = omp_profiled(Abar, 6, n, {6}, band_norms)
            d = max(classify_support(support).items(), key=lambda x: x[1])[0]
            dom[d] = dom.get(d, 0) + 1

    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return {
        "n_layers": n_layers, "n_heads": n_heads,
        "conc_real": real_med, "conc_random": rand_med, "conc_ratio": real_med / (rand_med + 1e-12),
        "uniform_err": uni_med, "profiled_err": prof_med, "svd_err": svd_med,
        "head_types": dom,
    }


def main():
    args = get_args()
    os.makedirs(args.out, exist_ok=True)
    theta = np.arange(0.0, 180.0, 2.0)
    band_norms = precompute_band_norms(args.seq_len)
    checkpoints = [k for k in [1, 2, 4, 8, 16, 32] if k <= args.max_k]
    rng = np.random.default_rng(args.seed)

    results = {}
    for name in args.models:
        print(f"\n===== {name} =====", flush=True)
        try:
            r = run_model(name, args, theta, band_norms, checkpoints, rng)
        except Exception as e:
            print(f"  FALHOU: {type(e).__name__}: {e}", flush=True)
            results[name] = {"error": f"{type(e).__name__}: {e}"}
            json.dump(results, open(os.path.join(args.out, "phase1_multimodel.json"), "w"), indent=2)
            continue
        results[name] = r
        json.dump(results, open(os.path.join(args.out, "phase1_multimodel.json"), "w"), indent=2)  # salva incremental
        print(f"  conc ratio real/rand: {r['conc_ratio']:.3f}", flush=True)
        print(f"  k=8  uniforme={r['uniform_err'][8]:.3f}  perfil={r['profiled_err'][8]:.3f}  SVD={r['svd_err'][8]:.3f}", flush=True)
        print(f"  head types: {r['head_types']}", flush=True)

    with open(os.path.join(args.out, "phase1_multimodel.json"), "w") as f:
        json.dump(results, f, indent=2)

    # tabela resumo
    print("\n" + "=" * 78)
    print("RESUMO MULTI-MODELO (k=8)")
    print("=" * 78)
    print(f"{'modelo':>22} | {'conc.ratio':>10} | {'uniforme':>8} | {'perfil':>7} | {'SVD':>6} | razao L/SVD")
    print("-" * 78)
    for name, r in results.items():
        if "error" in r:
            print(f"{name[:22]:>22} | ERRO: {r['error'][:40]}")
            continue
        u, p, s = r["uniform_err"][8], r["profiled_err"][8], r["svd_err"][8]
        print(f"{name[:22]:>22} | {r['conc_ratio']:>10.3f} | {u:>8.3f} | {p:>7.3f} | {s:>6.3f} | {p/(s+1e-12):>5.2f}")
    print("=" * 78)
    ok = [r for r in results.values() if "error" not in r]
    if ok:
        all_line_lose = all(r["profiled_err"][8] > 1.3 * r["svd_err"][8] for r in ok)
        all_conc = all(r["conc_ratio"] < 0.3 for r in ok)
        print(f"replicacao: concentracao alta em todos = {all_conc}; SVD domina linhas em todos = {all_line_lose}")
        if all_conc and all_line_lose:
            print("=> padrao GENERALIZA: concentracao de Radon real mas enganosa; low-rank domina em todos os modelos.")
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase1_multimodel.json'))}")


if __name__ == "__main__":
    main()
