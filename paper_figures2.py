"""Extension figures (multi-model, downstream, robustness), 300 dpi, EN labels, no metadata."""
import json, os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "paper/figs"
os.makedirs(OUT, exist_ok=True)
DPI = 300
plt.rcParams.update({"font.size": 9, "axes.titlesize": 9, "figure.dpi": DPI})


def strip_png(path):
    im = Image.open(path).convert("RGB")
    clean = Image.new(im.mode, im.size)
    clean.putdata(list(im.getdata()))
    clean.save(path, "PNG")


def short(name):
    return name.split("/")[-1]


p1 = json.load(open("out/phase1_multimodel.json"))
p2 = json.load(open("out/phase2_downstream.json"))
p3 = json.load(open("out/phase3_robustness.json"))

# ---- Fig 5: multimodel ----
models = [m for m in p1 if "error" not in p1[m]]
labels = [short(m) for m in models]
prof = [p1[m]["profiled_err"]["8"] for m in models]
svd = [p1[m]["svd_err"]["8"] for m in models]
conc = [p1[m]["conc_ratio"] for m in models]

fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0))
x = np.arange(len(models)); w = 0.38
ax[0].bar(x - w/2, prof, w, label="profiled lines", color="#b03a2e")
ax[0].bar(x + w/2, svd, w, label="rank-8 SVD", color="#2e86c1")
ax[0].set_xticks(x); ax[0].set_xticklabels(labels, rotation=20, ha="right")
ax[0].set_ylabel("relative error ($k=8$)"); ax[0].set_title("(a) reconstruction per model")
ax[0].legend(fontsize=7)
ax[1].bar(x, conc, color="#7d3c98")
ax[1].set_xticks(x); ax[1].set_xticklabels(labels, rotation=20, ha="right")
ax[1].set_ylabel("concentration ratio (real/random)"); ax[1].set_title("(b) Radon concentration")
fig.tight_layout(); fig.savefig(f"{OUT}/fig5_multimodel.png", dpi=DPI); plt.close(fig)

# ---- Fig 6: downstream ----
fig, ax = plt.subplots(figsize=(5.2, 3.6))
ks = [1, 2, 4, 8, 16, 32]
colors = {"gpt2": "#b03a2e", "EleutherAI/pythia-410m": "#2e86c1", "Qwen/Qwen2.5-0.5B": "#27ae60"}
for m in p2:
    if "svd" not in p2[m]:
        continue
    c = colors.get(m, "#555")
    y = [p2[m]["svd"][str(k)]["kl"] for k in ks]
    ax.plot(ks, y, marker="o", color=c, label=f"{short(m)} SVD")
    ax.axhline(p2[m]["geom"]["kl"], color=c, ls="--", lw=1, alpha=0.8)
ax.set_xscale("log", base=2); ax.set_xlabel("SVD rank $k$")
ax.set_ylabel("KL(true $\\Vert$ reconstructed)")
ax.set_title("downstream effect: SVD converges, geometry (- -) plateaus")
ax.grid(True, alpha=0.3); ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig(f"{OUT}/fig6_downstream.png", dpi=DPI); plt.close(fig)

# ---- Fig 7: robustness ----
lengths = [128, 256, 512]
fig, ax = plt.subplots(figsize=(5.2, 3.4))
for base, c in [("gpt2", "#b03a2e"), ("EleutherAI/pythia-410m", "#2e86c1")]:
    line = [p3[f"{base}@{n}"]["line_k8"][1] for n in lengths]
    sv = [p3[f"{base}@{n}"]["svd_k8"][1] for n in lengths]
    ax.plot(lengths, line, marker="^", color=c, label=f"{short(base)} lines")
    ax.plot(lengths, sv, marker="s", color=c, ls="--", label=f"{short(base)} SVD")
ax.set_xticks(lengths); ax.set_xlabel("sequence length")
ax.set_ylabel("relative error at $k=8$ (median)")
ax.set_title("robustness to length: SVD below lines at every length")
ax.grid(True, alpha=0.3); ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig(f"{OUT}/fig7_robustness.png", dpi=DPI); plt.close(fig)

for f in ["fig5_multimodel", "fig6_downstream", "fig7_robustness"]:
    strip_png(f"{OUT}/{f}.png")
    im = Image.open(f"{OUT}/{f}.png")
    print(f"{f}: {im.size[0]}x{im.size[1]} info={dict(im.info)}")
