"""
A1 — energia de interacao na coluna do sink (fix #2 do revisor NN).

"Qualquer coluna e rank-1" — a alegacao nao-trivial e que o peso do sink e
quase CONSTANTE ao longo das queries, i.e. o termo de interacao Theta na coluna 0
e pequeno. Mede, por cabeca:

    leak_0 = ||Theta[:,0]||^2 / ||A[:,0] - mu||^2     (fracao da energia da coluna
             do sink NAO capturada pelo modelo aditivo r_i + c_0 - mu)

e o mesmo para uma coluna de controle (mediana das outras colunas). Se
leak_0 << leak_ctrl, o sink e genuinamente um efeito de coluna (constante em i),
nao um artefato da decomposicao. 5 modelos, n_seq=50. GPU leve.
"""
import argparse, json, os
import numpy as np
import torch

from phase0_radon_attention import load_sequences, extract_attention


def leaks(A):
    """Nao-constancia relativa por coluna, SOMENTE nas linhas validas (i >= j):
        e_j = ||A[i>=j, j] - mean||^2 / ||A[i>=j, j]||^2
    Se o sink e ~constante ao longo das queries (a alegacao rank-1 nao-trivial),
    e_0 << e_ctrl. Nota: em matriz row-estocastica o efeito de LINHA e constante
    (1/n), entao a metrica via Theta e vacua; esta e a correta."""
    n = A.shape[0]
    out = []
    for j in range(n):
        col = A[j:, j]                      # linhas validas do triangulo causal
        if col.size < 8:
            out.append(np.nan); continue
        tot = float(np.sum(col ** 2))
        dev = float(np.sum((col - col.mean()) ** 2))
        out.append(dev / (tot + 1e-12))
    ctrl = [x for x in out[1:] if not np.isnan(x)]
    return out[0], float(np.median(ctrl))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=[
        "gpt2", "gpt2-medium", "EleutherAI/pythia-410m", "EleutherAI/pythia-1.4b", "Qwen/Qwen2.5-0.5B"])
    ap.add_argument("--n_seq", type=int, default=50)
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs(args.out, exist_ok=True)

    from transformers import AutoModelForCausalLM, AutoTokenizer
    results = {}
    for name in args.models:
        print(f"===== {name} =====", flush=True)
        try:
            tok = AutoTokenizer.from_pretrained(name)
            model = AutoModelForCausalLM.from_pretrained(
                name, attn_implementation="eager", dtype=torch.float32).to(device).eval()
            ids = load_sequences(tok, args.n_seq, args.seq_len, args.seed)
            attn = extract_attention(model, ids, args.batch, device)
            attn = [np.nan_to_num(a) for a in attn]
            sink_leaks, ctrl_leaks = [], []
            for li in range(len(attn)):
                for hi in range(attn[0].shape[1]):
                    Abar = attn[li][:, hi].mean(axis=0).astype(np.float64)
                    s, c = leaks(Abar)
                    sink_leaks.append(s); ctrl_leaks.append(c)
            del model
            if device == "cuda":
                torch.cuda.empty_cache()
            results[name] = {
                "sink_col_interaction_frac_median": float(np.median(sink_leaks)),
                "ctrl_col_interaction_frac_median": float(np.median(ctrl_leaks)),
            }
            r = results[name]
            print(f"  interacao na coluna do sink: {r['sink_col_interaction_frac_median']:.3f}  "
                  f"| controle (mediana outras colunas): {r['ctrl_col_interaction_frac_median']:.3f}", flush=True)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[name] = {"error": f"{type(e).__name__}: {e}"}
        json.dump(results, open(os.path.join(args.out, "phase15_interaction.json"), "w"), indent=2)
    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase15_interaction.json'))}")


if __name__ == "__main__":
    main()
