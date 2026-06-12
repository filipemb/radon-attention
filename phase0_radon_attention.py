"""
Fase 0 — testa a hipotese central da proposta Radon-over-Attention:
a matriz de atencao de um transformer e dominada por poucas estruturas
lineares (banda local, listra de sink, diagonais de inducao), logo ela
e ESPARSA no dominio de Radon (poucas linhas -> poucos picos no sinograma).

Metodo:
  1. extrai atencao de um modelo aberto (GPT-2 small) via atencao eager
  2. para cada matriz de atencao, calcula o sinograma de Radon
  3. mede "suporte efetivo de Radon" (numero efetivo de coeficientes que
     concentram a energia) via razao de participacao inversa
  4. compara contra dois controles: atencao uniforme e atencao aleatoria
     (ambos com a mesma mascara causal) -> a hipotese preve que a atencao
     real e MUITO mais concentrada que a aleatoria
  5. curva de erro de reconstrucao vs k (compressibilidade)
  6. classifica cabecas pelo angulo dominante de Radon (0/90 = listra/sink,
     ~45 = diagonal local/inducao)

Saida: prints com o veredito do gate, JSON com metricas, e PNGs em ./out.

NAO treina nada. Forward pass apenas. Roda numa RTX 3060 em poucos minutos.
"""

import argparse
import json
import os
import numpy as np
import torch
from skimage.transform import radon, iradon


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="gpt2", help="modelo HF (gpt2, gpt2-medium, EleutherAI/pythia-410m, ...)")
    p.add_argument("--n_seq", type=int, default=100, help="numero de sequencias amostradas")
    p.add_argument("--seq_len", type=int, default=128, help="tokens por sequencia")
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--theta_step", type=float, default=2.0, help="passo angular do Radon (graus)")
    p.add_argument("--out", default="out")
    p.add_argument("--seed", type=int, default=0)
    # gate: fracao de suporte efetivo abaixo da qual consideramos a cabeca "Radon-esparsa"
    p.add_argument("--sparse_thresh", type=float, default=0.10,
                   help="cabeca e 'esparsa' se suporte efetivo de Radon < esta fracao do total de celulas")
    return p.parse_args()


def load_sequences(tokenizer, n_seq, seq_len, seed, corpus="wikitext2_train.txt"):
    """Carrega ~n_seq janelas de seq_len tokens de texto real.
    Le de um .txt local (uma linha util por linha) gerado a partir do wikitext-2.
    Evita a lib `datasets`/pyarrow, que conflita com torch no import (Windows)."""
    with open(corpus, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if len(ln.strip()) >= 200]
    rng = np.random.default_rng(seed)
    idxs = rng.permutation(len(lines))
    seqs = []
    for i in idxs:
        ids = tokenizer(lines[int(i)], return_tensors="pt")["input_ids"][0]
        if ids.shape[0] < seq_len:
            continue
        seqs.append(ids[:seq_len])
        if len(seqs) >= n_seq:
            break
    return torch.stack(seqs)  # [n_seq, seq_len]


@torch.no_grad()
def extract_attention(model, input_ids, batch, device):
    """Retorna lista por camada de tensores [N, heads, seq, seq] (CPU, float32)."""
    n_layers = model.config.n_layer if hasattr(model.config, "n_layer") else model.config.num_hidden_layers
    per_layer = [[] for _ in range(n_layers)]
    for s in range(0, input_ids.shape[0], batch):
        chunk = input_ids[s:s + batch].to(device)
        out = model(chunk, output_attentions=True)
        for li, att in enumerate(out.attentions):  # att: [b, heads, seq, seq]
            per_layer[li].append(att.float().cpu())
    return [torch.cat(x, dim=0).numpy() for x in per_layer]


def causal_mask(seq_len):
    return np.tril(np.ones((seq_len, seq_len), dtype=np.float32))


def make_controls(seq_len, n, rng):
    """Atencao uniforme e aleatoria, ambas causais e normalizadas por linha."""
    m = causal_mask(seq_len)
    # uniforme: cada query atende igualmente a todas as posicoes <= ela
    uni = m / m.sum(axis=1, keepdims=True)
    # aleatoria: softmax de logits aleatorios sob mascara causal
    rand_batch = []
    for _ in range(n):
        logits = rng.standard_normal((seq_len, seq_len)).astype(np.float32)
        logits = np.where(m > 0, logits, -1e9)
        e = np.exp(logits - logits.max(axis=1, keepdims=True))
        e *= m
        rand_batch.append(e / e.sum(axis=1, keepdims=True))
    return uni, np.stack(rand_batch)


def radon_support_fraction(A, theta):
    """Suporte efetivo de Radon como fracao do total de celulas do sinograma.
    Razao de participacao inversa da energia: 1/sum(p_i^2), p_i = energia normalizada.
    Valor baixo = energia concentrada em poucas linhas = hipotese verdadeira."""
    sino = radon(A, theta=theta, circle=False)
    energy = sino.astype(np.float64) ** 2
    total = energy.sum()
    if total <= 0:
        return 1.0, sino
    p = energy.ravel() / total
    eff = 1.0 / np.sum(p ** 2)          # numero efetivo de celulas significativas
    return eff / p.size, sino           # fracao do total


def recon_error_curve(A, sino, theta, ks):
    """Mantem os top-k coeficientes do sinograma, reconstroi via iradon,
    mede erro relativo de Frobenius. Retorna lista de erros e o erro-piso (k=all)."""
    flat = sino.ravel()
    order = np.argsort(np.abs(flat))[::-1]
    errs = []
    normA = np.linalg.norm(A) + 1e-12
    for k in ks:
        keep = np.zeros_like(flat)
        sel = order[:k]
        keep[sel] = flat[sel]
        s_k = keep.reshape(sino.shape)
        rec = iradon(s_k, theta=theta, circle=False, filter_name="ramp",
                     output_size=A.shape[0])
        errs.append(float(np.linalg.norm(rec - A) / normA))
    rec_full = iradon(sino, theta=theta, circle=False, filter_name="ramp", output_size=A.shape[0])
    floor = float(np.linalg.norm(rec_full - A) / normA)
    return errs, floor


def dominant_angle(sino, theta):
    """Angulo (graus) que concentra mais energia no sinograma."""
    col_energy = (sino.astype(np.float64) ** 2).sum(axis=0)
    return float(theta[int(np.argmax(col_energy))])


def main():
    args = get_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    theta = np.arange(0.0, 180.0, args.theta_step)

    print(f"[setup] device={device} model={args.model} n_seq={args.n_seq} seq_len={args.seq_len}")
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.model)
    # eager e OBRIGATORIO: flash/sdpa nao materializam a matriz n x n
    model = AutoModelForCausalLM.from_pretrained(args.model, attn_implementation="eager").to(device).eval()

    print("[data] carregando sequencias de wikitext-2 ...")
    input_ids = load_sequences(tok, args.n_seq, args.seq_len, args.seed)
    print(f"[data] {input_ids.shape[0]} sequencias x {input_ids.shape[1]} tokens")

    print("[extract] forward pass com atencao eager ...")
    attn = extract_attention(model, input_ids, args.batch, device)
    n_layers = len(attn)
    n_heads = attn[0].shape[1]
    print(f"[extract] {n_layers} camadas x {n_heads} cabecas")

    # controles
    uni, rand_batch = make_controls(args.seq_len, min(args.n_seq, 50), rng)

    # --- metrica primaria: suporte efetivo de Radon ---
    print("[radon] medindo suporte efetivo (real vs controles) ...")
    real_supports = []          # por (camada, cabeca): media sobre sequencias
    head_angle = np.zeros((n_layers, n_heads))
    head_support = np.zeros((n_layers, n_heads))
    n_sample = min(args.n_seq, 30)  # amostra p/ a metrica de suporte (suficiente p/ media estavel)

    for li in range(n_layers):
        for hi in range(n_heads):
            supps, angs = [], []
            for si in range(n_sample):
                A = attn[li][si, hi]
                frac, sino = radon_support_fraction(A, theta)
                supps.append(frac)
                angs.append(dominant_angle(sino, theta))
            head_support[li, hi] = np.mean(supps)
            head_angle[li, hi] = np.median(angs)
            real_supports.extend(supps)

    uni_frac, _ = radon_support_fraction(uni, theta)
    rand_fracs = [radon_support_fraction(rand_batch[i], theta)[0] for i in range(rand_batch.shape[0])]

    real_med = float(np.median(real_supports))
    rand_med = float(np.median(rand_fracs))
    ratio = real_med / (rand_med + 1e-12)
    frac_sparse_heads = float(np.mean(head_support < args.sparse_thresh))

    # --- metrica secundaria: curva de reconstrucao vs k (numa amostra) ---
    print("[radon] curva de reconstrucao vs k ...")
    ks = [2, 4, 8, 16, 32, 64, 128, 256]
    # pega uma cabeca representativa por terco de profundidade
    sample_heads = [(0, 0), (n_layers // 2, n_heads // 2), (n_layers - 1, n_heads - 1)]
    recon = {}
    for (li, hi) in sample_heads:
        A = attn[li][0, hi]
        _, sino = radon_support_fraction(A, theta)
        errs, floor = recon_error_curve(A, sino, theta, ks)
        recon[f"L{li}H{hi}"] = {"ks": ks, "errs": errs, "floor": floor}

    # --- veredito do gate ---
    results = {
        "model": args.model,
        "n_seq": args.n_seq, "seq_len": args.seq_len, "theta_step": args.theta_step,
        "real_median_support_frac": real_med,
        "uniform_support_frac": float(uni_frac),
        "random_median_support_frac": rand_med,
        "real_vs_random_ratio": ratio,
        "frac_heads_radon_sparse": frac_sparse_heads,
        "sparse_thresh": args.sparse_thresh,
        "reconstruction": recon,
    }
    with open(os.path.join(args.out, "phase0_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print("RESULTADO FASE 0")
    print("=" * 60)
    print(f"suporte efetivo de Radon (fracao do sinograma; menor = mais concentrado):")
    print(f"  atencao real    (mediana): {real_med:.4f}")
    print(f"  controle uniforme        : {uni_frac:.4f}")
    print(f"  controle aleatorio (med) : {rand_med:.4f}")
    print(f"  razao real/aleatorio     : {ratio:.3f}  (quanto menor, mais forte a hipotese)")
    print(f"cabecas Radon-esparsas (<{args.sparse_thresh}): {frac_sparse_heads*100:.1f}%")
    print("-" * 60)
    # gate sugerido: real claramente mais concentrado que aleatorio E fracao relevante de cabecas esparsas
    go = (ratio < 0.6) and (frac_sparse_heads > 0.40)
    if go:
        print("VEREDITO: GO  -> a atencao e geometricamente esparsa no dominio de Radon.")
        print("          Hipotese sobrevive. Vale seguir p/ Fase 1 (mapear motivos por cabeca).")
    elif ratio < 0.8 or frac_sparse_heads > 0.25:
        print("VEREDITO: PARCIAL -> sinal presente mas fraco. Inspecionar por camada/cabeca")
        print("          antes de decidir (ver out/*.png).")
    else:
        print("VEREDITO: NO-GO -> atencao nao e mais Radon-esparsa que o controle aleatorio.")
        print("          Achado negativo (ainda assim publicavel sobre estrutura de atencao).")
    print("=" * 60)

    # --- visualizacoes ---
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # 1) heatmap do suporte por camada/cabeca
        plt.figure(figsize=(8, 5))
        plt.imshow(head_support, aspect="auto", cmap="viridis_r")
        plt.colorbar(label="suporte efetivo de Radon (frac)")
        plt.xlabel("cabeca"); plt.ylabel("camada"); plt.title("Concentracao de Radon por cabeca (escuro = mais esparso)")
        plt.tight_layout(); plt.savefig(os.path.join(args.out, "support_heatmap.png"), dpi=120); plt.close()

        # 2) curvas de reconstrucao
        plt.figure(figsize=(7, 5))
        for name, d in recon.items():
            plt.plot(d["ks"], d["errs"], marker="o", label=f"{name} (piso={d['floor']:.2f})")
        plt.xscale("log", base=2); plt.xlabel("k coeficientes de Radon retidos")
        plt.ylabel("erro relativo de reconstrucao"); plt.title("Compressibilidade da atencao no dominio de Radon")
        plt.legend(); plt.grid(True, alpha=0.3)
        plt.tight_layout(); plt.savefig(os.path.join(args.out, "recon_curves.png"), dpi=120); plt.close()

        # 3) exemplos: matriz de atencao + sinograma
        fig, axes = plt.subplots(len(sample_heads), 2, figsize=(8, 3 * len(sample_heads)))
        for r, (li, hi) in enumerate(sample_heads):
            A = attn[li][0, hi]
            sino = radon(A, theta=theta, circle=False)
            axes[r, 0].imshow(A, cmap="magma"); axes[r, 0].set_title(f"atencao L{li}H{hi}")
            axes[r, 1].imshow(sino, aspect="auto", cmap="magma", extent=[0, 180, 0, sino.shape[0]])
            axes[r, 1].set_title("sinograma de Radon"); axes[r, 1].set_xlabel("angulo (graus)")
        plt.tight_layout(); plt.savefig(os.path.join(args.out, "examples.png"), dpi=120); plt.close()

        print(f"[plots] salvos em {os.path.abspath(args.out)}")
    except Exception as e:
        print(f"[plots] pulado ({e})")

    print(f"[json] {os.path.abspath(os.path.join(args.out, 'phase0_results.json'))}")


if __name__ == "__main__":
    main()
