"""
A1 — replicacao das metricas-nucleo num modelo MAIOR (>=3B), o ataque de escala.

Qwen2.5-3B em bf16 (nativo, estavel) cabe na RTX 3060. Extracao em streaming
(reservoir) p/ nao estourar RAM. Mede, no 3B:
  - concentracao de Radon (real vs aleatorio)
  - reconstrucao linha(perfil) vs SVD em k=8
  - ANOVA: fracao do sink no efeito de coluna + aditivo+rank-k vs SVD
  - fracao nomeada (MS-CLEAN, m=5)

Mostra se o achado (concentracao enganosa + decomposicao de dois canais) generaliza
pra escala maior, nao so <=1.4B.
"""
import argparse, json, os
import numpy as np
import torch

from phase0_radon_attention import load_sequences, radon_support_fraction, make_controls
from phase3_robustness import stream
from phase05_line_decomposition import svd_errors
from phase06_profiled_lines import omp_profiled, precompute_band_norms
from phase4_anova import anova_lowrank_errors
from phase5_msclean import build_dict, msclean
from phase_stats import summ, median_ci_bootstrap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-3B")
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--n_seq", type=int, default=250)
    ap.add_argument("--n_conc", type=int, default=150)
    ap.add_argument("--n_rec", type=int, default=100)
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    n = args.seq_len
    theta = np.arange(0.0, 180.0, 2.0)
    band_norms = precompute_band_norms(n)
    D, labels = build_dict(n)

    from transformers import AutoModelForCausalLM, AutoTokenizer
    print(f"[load] {args.model} (bf16) ...", flush=True)
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, attn_implementation="eager", dtype=torch.bfloat16).to(device).eval()
    print(f"[load] ok. camadas={model.config.num_hidden_layers} heads={model.config.num_attention_heads}", flush=True)

    ids = load_sequences(tok, args.n_seq, n, args.seed)
    print("[stream] extraindo atencao (reservoir) ...", flush=True)
    conc, reservoir = stream(model, ids, args.batch, device, theta, args.n_conc, args.n_rec, rng)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()

    _, rb = make_controls(n, 40, rng)
    rand = [radon_support_fraction(rb[i], theta)[0] for i in range(rb.shape[0])]
    conc_real, conc_rand = float(np.median(conc)), float(np.median(rand))

    ks = [1, 2, 4, 8, 16]
    line8, svd8, anova8, sinkfr, named5 = [], [], [], [], []
    for A in reservoir:
        A = A.astype(np.float64)
        ep, _ = omp_profiled(A, 8, n, {8}, band_norms)
        line8.append(ep[8]); svd8.append(svd_errors(A, [8])[8])
        a, sf, _ = anova_lowrank_errors(A, ks); anova8.append(a[8]); sinkfr.append(sf)
        cm, _ = msclean(A, D, labels, 5)
        named5.append(float(np.linalg.norm(cm) / (np.linalg.norm(A) + 1e-12)))

    res = {
        "model": args.model,
        "conc_real": conc_real, "conc_random": conc_rand, "conc_ratio": conc_real / (conc_rand + 1e-12),
        "line_k8": float(np.median(line8)), "svd_k8": float(np.median(svd8)),
        "anova_addrank8": float(np.median(anova8)), "sink_frac_coleffect": float(np.median(sinkfr)),
        "named_frac_m5": float(np.median(named5)), "n_rec": len(reservoir),
        # dispersion (NN revision)
        "conc_real_disp": summ(conc),
        "line_k8_disp": summ(line8), "line_k8_ci": median_ci_bootstrap(line8),
        "svd_k8_disp": summ(svd8), "svd_k8_ci": median_ci_bootstrap(svd8),
        "anova_addrank8_disp": summ(anova8), "sink_frac_coleffect_disp": summ(sinkfr),
        "named_frac_m5_disp": summ(named5),
    }
    json.dump(res, open(os.path.join(args.out, "phase9_bigmodel.json"), "w"), indent=2)
    print("\n" + "=" * 56)
    print(f"RESULTADO 3B — {args.model}")
    print("=" * 56)
    print(f"  concentracao real/aleatorio: {res['conc_ratio']:.3f}  ({1/res['conc_ratio']:.0f}x mais concentrado)")
    print(f"  k=8: linha(perfil)={res['line_k8']:.3f}  SVD={res['svd_k8']:.3f}  (SVD {res['line_k8']/res['svd_k8']:.2f}x melhor)")
    print(f"  ANOVA: sink={res['sink_frac_coleffect']*100:.1f}% do efeito-coluna; add+rank8={res['anova_addrank8']:.3f} vs SVD8={res['svd_k8']:.3f}")
    print(f"  fracao nomeada (m=5): {res['named_frac_m5']*100:.1f}%")
    print("=" * 56)
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase9_bigmodel.json'))}")


if __name__ == "__main__":
    main()
