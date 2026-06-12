"""
Fase 3 (extensao) — robustez.

Mostra que o resultado central (linhas travam, SVD domina) e estavel a:
  - amostra maior (centenas de instancias)
  - variar o comprimento da sequencia (128 / 256 / 512)

Reporta mediana + IQR (percentis 25-75), nao so a mediana.

Memoria: pra n=512 nao da pra guardar todas as matrizes de atencao (estouraria a
RAM). Extracao em STREAMING: por batch, amostra escalares de concentracao na hora
e faz reservoir sampling de N_rec matrizes inteiras pra reconstrucao, descartando
o resto.
"""
import argparse, json, os
import numpy as np
import torch

from phase0_radon_attention import load_sequences, radon_support_fraction, make_controls
from phase05_line_decomposition import svd_errors
from phase06_profiled_lines import omp_profiled, precompute_band_norms


@torch.no_grad()
def stream(model, ids, batch, device, theta, n_conc, n_rec, rng):
    conc, reservoir, seen = [], [], 0
    for s in range(0, ids.shape[0], batch):
        chunk = ids[s:s + batch].to(device)
        atts = model(chunk, output_attentions=True).attentions
        b, L, H = chunk.shape[0], len(atts), atts[0].shape[1]
        for li in range(L):
            a = np.nan_to_num(atts[li].float().cpu().numpy())
            for bi in range(b):
                for hi in range(H):
                    if len(conc) < n_conc and rng.random() < 0.5:
                        conc.append(radon_support_fraction(a[bi, hi], theta)[0])
                    seen += 1
                    M = a[bi, hi].astype(np.float64)
                    if len(reservoir) < n_rec:
                        reservoir.append(M)
                    elif rng.random() < n_rec / seen:
                        reservoir[int(rng.integers(n_rec))] = M
        if len(conc) >= n_conc and seen > 6 * n_rec:
            break
    return conc, reservoir


def q(x):
    a = np.array(x)
    return [float(np.percentile(a, 25)), float(np.median(a)), float(np.percentile(a, 75))]


def run(model_name, n, args, device, rng):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, attn_implementation="eager", dtype=torch.float32).to(device).eval()
    theta = np.arange(0.0, 180.0, 2.0)
    band_norms = precompute_band_norms(n)
    ckpts = [1, 2, 4, 8]
    batch = 2 if n >= 512 else (4 if n >= 256 else 8)
    ids = load_sequences(tok, args.n_seq, n, args.seed)

    conc, reservoir = stream(model, ids, batch, device, theta, args.n_conc, args.n_rec, rng)

    # controle aleatorio
    _, rb = make_controls(n, 30, rng)
    rand = [radon_support_fraction(rb[i], theta)[0] for i in range(rb.shape[0])]

    # reconstrucao na reserva
    line8, svd8 = [], []
    for A in reservoir:
        ep, _ = omp_profiled(A, 8, n, {8}, band_norms)
        es = svd_errors(A, [8])
        line8.append(ep[8]); svd8.append(es[8])

    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return {
        "n_conc": len(conc), "n_rec": len(reservoir),
        "conc_real": q(conc), "conc_random_median": float(np.median(rand)),
        "line_k8": q(line8), "svd_k8": q(svd8),
        "ratio_median": float(np.median(line8)) / (float(np.median(svd8)) + 1e-12),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "EleutherAI/pythia-410m"])
    ap.add_argument("--lengths", nargs="*", type=int, default=[128, 256, 512])
    ap.add_argument("--n_seq", type=int, default=400)
    ap.add_argument("--n_conc", type=int, default=200)
    ap.add_argument("--n_rec", type=int, default=120)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)

    results = {}
    for m in args.models:
        for n in args.lengths:
            key = f"{m}@{n}"
            print(f"\n===== {key} =====", flush=True)
            try:
                r = run(m, n, args, device, rng)
            except Exception as e:
                import traceback; traceback.print_exc()
                print(f"  FALHOU: {type(e).__name__}: {e}", flush=True)
                results[key] = {"error": f"{type(e).__name__}: {e}"}
                json.dump(results, open(os.path.join(args.out, "phase3_robustness.json"), "w"), indent=2)
                continue
            results[key] = r
            json.dump(results, open(os.path.join(args.out, "phase3_robustness.json"), "w"), indent=2)
            print(f"  n_rec={r['n_rec']} conc_real(med)={r['conc_real'][1]:.4f} vs rand={r['conc_random_median']:.4f}", flush=True)
            print(f"  k=8 line={r['line_k8'][1]:.3f} [{r['line_k8'][0]:.3f},{r['line_k8'][2]:.3f}]  SVD={r['svd_k8'][1]:.3f} [{r['svd_k8'][0]:.3f},{r['svd_k8'][2]:.3f}]  ratio={r['ratio_median']:.2f}", flush=True)

    print("\n" + "=" * 86)
    print("RESUMO FASE 3 — robustez (mediana [IQR])")
    print("=" * 86)
    print(f"{'modelo@n':>26} | {'conc real':>10} | {'line k=8':>16} | {'SVD k=8':>16} | ratio")
    print("-" * 86)
    for key, r in results.items():
        if "error" in r:
            print(f"{key:>26} | ERRO {r['error'][:40]}"); continue
        l, s = r["line_k8"], r["svd_k8"]
        print(f"{key:>26} | {r['conc_real'][1]:>10.4f} | {l[1]:.3f}[{l[0]:.2f},{l[2]:.2f}] | {s[1]:.3f}[{s[0]:.2f},{s[2]:.2f}] | {r['ratio_median']:.2f}")
    print("=" * 86)
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase3_robustness.json'))}")


if __name__ == "__main__":
    main()
