"""
Parte 2, Etapa A — gate functional-ANOVA + low-rank.

Testa a ideia de "dois canais": termos aditivos NOMEADOS (efeito de linha,
efeito de coluna onde c_0 = SINK) + interacao low-rank (resíduo difuso).

  A_ij ~= mu + (r_i - mu) + (c_j - mu) + Theta_ij
        = r_i + c_j - mu  (parte aditiva, rank <= 2, NOMEADA)  + Theta (interacao)

Reconstrucao = aditivo + rank-k(Theta).  Comparo com:
  - SVD rank-k puro  e  SVD rank-(k+2) (orcamento casado: aditivo custa <=2 ranks)

Pergunta do gate:
  (1) aditivo+rank-k ~= SVD rank-(k+2)?  -> os termos nomeados saem "de graca"
  (2) o sink e limpo no efeito de coluna? -> energia de c_0 / energia total dos c_j

Se sim, a decomposicao de dois canais da fidelidade do SVD COM componentes
nomeados/editaveis. Barato (so SVD + medias), sem NNLS.
"""
import argparse, json, os
import numpy as np
import torch

from phase0_radon_attention import load_sequences, extract_attention
from phase05_line_decomposition import svd_errors
from phase_stats import summ, median_ci_bootstrap


def anova_decomp(A):
    """Retorna (additive, Theta, sink_frac, add_rank2_err)."""
    mu = A.mean()
    r = A.mean(axis=1, keepdims=True)   # efeito de linha (n,1)
    c = A.mean(axis=0, keepdims=True)   # efeito de coluna (1,n); c[0,0] ~ sink
    additive = r + c - mu
    Theta = A - additive
    cc = (c.ravel() - mu)
    sink_frac = float(cc[0] ** 2 / (np.sum(cc ** 2) + 1e-12))
    add_err = float(np.linalg.norm(A - additive) / (np.linalg.norm(A) + 1e-12))
    return additive, Theta, sink_frac, add_err


def anova_lowrank_errors(A, ks):
    additive, Theta, sink_frac, add_err = anova_decomp(A)
    normA = np.linalg.norm(A) + 1e-12
    U, S, Vt = np.linalg.svd(Theta, full_matrices=False)
    out = {}
    for k in ks:
        Tk = (U[:, :k] * S[:k]) @ Vt[:k]
        out[k] = float(np.linalg.norm(A - (additive + Tk)) / normA)
    return out, sink_frac, add_err


def med(x):
    return float(np.median(x))


def run(model_name, args, device, rng):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, attn_implementation="eager", dtype=torch.float32).to(device).eval()
    n = args.seq_len
    ids = load_sequences(tok, args.n_seq, n, args.seed)
    attn = extract_attention(model, ids, args.batch, device)
    attn = [np.nan_to_num(a) for a in attn]
    n_layers, n_heads = len(attn), attn[0].shape[1]

    ks = [1, 2, 4, 8, 16]
    inst = [(int(rng.integers(n_layers)), int(rng.integers(n_heads)), int(rng.integers(attn[0].shape[0])))
            for _ in range(args.n_instances)]
    anova = {k: [] for k in ks}
    svdk = {k: [] for k in ks}
    svdk2 = {k: [] for k in ks}
    sinks, adderrs = [], []
    for (li, hi, si) in inst:
        A = attn[li][si, hi].astype(np.float64)
        a, sf, ae = anova_lowrank_errors(A, ks)
        s = svd_errors(A, ks + [k + 2 for k in ks])
        for k in ks:
            anova[k].append(a[k]); svdk[k].append(s[k]); svdk2[k].append(s[k + 2])
        sinks.append(sf); adderrs.append(ae)

    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return {
        "anova_addrankk": {k: med(anova[k]) for k in ks},
        "svd_k": {k: med(svdk[k]) for k in ks},
        "svd_kplus2": {k: med(svdk2[k]) for k in ks},
        "sink_frac_of_coleffect": med(sinks),
        "additive_only_err": med(adderrs),
        "ks": ks,
        # dispersion (NN revision)
        "anova_addrankk_disp": {k: summ(anova[k]) for k in ks},
        "svd_k_disp": {k: summ(svdk[k]) for k in ks},
        "sink_frac_of_coleffect_disp": summ(sinks),
        "additive_only_err_disp": summ(adderrs),
        "anova_addrankk_ci": {k: median_ci_bootstrap(anova[k]) for k in ks},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "EleutherAI/pythia-410m"])
    ap.add_argument("--n_seq", type=int, default=100)
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--n_instances", type=int, default=150)
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
        json.dump(results, open(os.path.join(args.out, "phase4_anova.json"), "w"), indent=2)
        print(f"  sink_frac do efeito-coluna (mediana) = {r['sink_frac_of_coleffect']:.3f}", flush=True)
        print(f"  aditivo-so erro = {r['additive_only_err']:.3f}", flush=True)
        print(f"  {'k':>3} | {'ANOVA add+rk':>12} | {'SVD k':>7} | {'SVD k+2':>8} | add~free?", flush=True)
        for k in r["ks"]:
            a, s2 = r["anova_addrankk"][k], r["svd_kplus2"][k]
            free = "SIM" if a <= 1.10 * s2 else "nao"
            print(f"  {k:>3} | {a:>12.3f} | {r['svd_k'][k]:>7.3f} | {s2:>8.3f} | {free}", flush=True)

    print("\n" + "=" * 70)
    print("GATE ETAPA A")
    print("=" * 70)
    ok = [r for r in results.values() if "error" not in r]
    if ok:
        # gate: aditivo+rank-k perto do SVD-(k+2) (termos nomeados ~gratis) E sink limpo
        free_all = all(r["anova_addrankk"][8] <= 1.10 * r["svd_kplus2"][8] for r in ok)
        sink_clean = all(r["sink_frac_of_coleffect"] > 0.3 for r in ok)
        print(f"termos nomeados ~gratis (add+rk8 <= 1.1*SVD-k10): {free_all}")
        print(f"sink limpo no efeito-coluna (>0.3): {sink_clean}")
        if free_all and sink_clean:
            print("=> GO: dois canais dao fidelidade do SVD COM termos nomeados/editaveis.")
        else:
            print("=> revisar: aditivo simples nao basta; ir direto p/ MS-CLEAN/RPCA estruturado.")
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase4_anova.json'))}")


if __name__ == "__main__":
    main()
