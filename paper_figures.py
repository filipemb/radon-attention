"""
Core figures (figs 1-4) at 300 dpi, EN labels, no metadata.
Re-extracts GPT-2 attention (needs GPU).
"""
import json
import os
import numpy as np
import torch
from PIL import Image
from skimage.transform import radon

from phase0_radon_attention import (
    load_sequences, extract_attention, radon_support_fraction, make_controls,
)

OUT = "paper/figs"
os.makedirs(OUT, exist_ok=True)
DPI = 300
THETA = np.arange(0.0, 180.0, 2.0)


def strip_png(path):
    im = Image.open(path).convert("RGB")
    clean = Image.new(im.mode, im.size)
    clean.putdata(list(im.getdata()))
    clean.save(path, "PNG")


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    n, n_seq = 128, 100
    p0 = json.load(open("out/phase0_results.json"))
    p05 = json.load(open("out/phase05_results.json"))
    p06 = json.load(open("out/phase06_results.json"))

    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2", attn_implementation="eager").to(device).eval()
    ids = load_sequences(tok, n_seq, n, 0)
    attn = extract_attention(model, ids, 8, device)
    n_layers, n_heads = len(attn), attn[0].shape[1]

    n_sample = 20
    head_support = np.zeros((n_layers, n_heads))
    for li in range(n_layers):
        for hi in range(n_heads):
            head_support[li, hi] = np.mean([radon_support_fraction(attn[li][si, hi], THETA)[0]
                                            for si in range(n_sample)])

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    plt.rcParams.update({"font.size": 9, "axes.titlesize": 9, "figure.dpi": DPI})

    # ---- Fig 1 ----
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.8))
    vals = [p0["real_median_support_frac"], p0["uniform_support_frac"], p0["random_median_support_frac"]]
    ax[0].bar(["real", "uniform", "random"], vals, color=["#b03a2e", "#7f8c8d", "#2e86c1"])
    ax[0].set_yscale("log"); ax[0].set_ylabel("effective Radon support (frac.)")
    ax[0].set_title("(a) concentration vs.\\ controls")
    for i, v in enumerate(vals):
        ax[0].text(i, v, f"{v:.3f}", ha="center", va="bottom", fontsize=7)
    im = ax[1].imshow(head_support, aspect="auto", cmap="viridis")
    ax[1].set_xlabel("head"); ax[1].set_ylabel("layer")
    ax[1].set_title("(b) per-head support (lighter = less sparse)")
    fig.colorbar(im, ax=ax[1], fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig1_radon_concentration.png", dpi=DPI); plt.close(fig)

    # ---- Fig 2 ----
    ks = p05["checkpoints"]
    fig, ax = plt.subplots(figsize=(4.2, 3.2))
    ax.plot(ks, [p05["line_omp_median_err"][str(k)] for k in ks], marker="o", color="#7f8c8d",
            label="uniform lines (OMP)")
    ax.plot(ks, [p06["line_profiled_median_err"][str(k)] for k in ks], marker="^", color="#b03a2e",
            label="profiled bands (OMP)")
    ax.plot(ks, [p05["svd_median_err"][str(k)] for k in ks], marker="s", color="#2e86c1",
            label="rank-$k$ SVD (floor)")
    ax.set_xscale("log", base=2); ax.set_xlabel("$k$ components")
    ax.set_ylabel("relative reconstruction error (median)")
    ax.set_title("reconstruction: geometry vs.\\ low rank")
    ax.grid(True, alpha=0.3); ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig2_reconstruction.png", dpi=DPI); plt.close(fig)

    # ---- Fig 3 ----
    dist = p06["head_type_distribution"]
    labels = {"sink": "sink", "banda_local": "local band",
              "vertical_outra": "other vertical", "diag_inducao": "induction diag."}
    keys = sorted(dist, key=lambda x: -dist[x])
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    ax.bar([labels.get(k, k) for k in keys], [dist[k] for k in keys], color="#34495e")
    ax.set_ylabel("number of heads")
    ax.set_title("dominant primitive per head ($k=6$)")
    for i, k in enumerate(keys):
        ax.text(i, dist[k], str(dist[k]), ha="center", va="bottom", fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig3_head_types.png", dpi=DPI); plt.close(fig)

    # ---- Fig 4 ----
    examples = [(0, 0), (n_layers // 2, n_heads // 2), (n_layers - 1, n_heads - 1)]
    fig, axes = plt.subplots(len(examples), 2, figsize=(5.0, 6.2))
    for r, (li, hi) in enumerate(examples):
        A = attn[li][0, hi]
        sino = radon(A, theta=THETA, circle=False)
        axes[r, 0].imshow(A, cmap="magma", norm=LogNorm(vmin=1e-3, vmax=1.0))
        axes[r, 0].set_title(f"attention L{li}H{hi}", fontsize=8)
        axes[r, 0].set_xticks([]); axes[r, 0].set_yticks([])
        axes[r, 1].imshow(sino, aspect="auto", cmap="magma",
                          extent=[0, 180, 0, sino.shape[0]])
        axes[r, 1].set_title("Radon sinogram", fontsize=8)
        axes[r, 1].set_xlabel("angle (deg)", fontsize=8)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig4_examples.png", dpi=DPI); plt.close(fig)

    for f in ["fig1_radon_concentration", "fig2_reconstruction", "fig3_head_types", "fig4_examples"]:
        strip_png(f"{OUT}/{f}.png")
    print("figures saved (EN labels, no metadata) in", os.path.abspath(OUT))
    for f in os.listdir(OUT):
        im = Image.open(f"{OUT}/{f}")
        print(f"  {f}: {im.size[0]}x{im.size[1]}px, info={dict(im.info)}")


if __name__ == "__main__":
    main()
