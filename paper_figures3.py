"""Part-2 (constructive) figures, 300 dpi, EN labels, no metadata."""
import json, os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "paper/figs"; DPI = 300
plt.rcParams.update({"font.size": 9, "axes.titlesize": 9, "figure.dpi": DPI})


def strip_png(p):
    im = Image.open(p).convert("RGB"); c = Image.new(im.mode, im.size)
    c.putdata(list(im.getdata())); c.save(p, "PNG")


def short(m): return m.split("/")[-1]


p4 = json.load(open("out/phase4_anova.json"))
p5 = json.load(open("out/phase5_msclean.json"))
p7 = json.load(open("out/phase7_editability.json"))

# ---- Fig 8: ANOVA named-for-free + sink fraction ----
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0))
g = p4["gpt2"]; ks = g["ks"]
ax[0].plot(ks, [g["anova_addrankk"][str(k)] for k in ks], marker="o", color="#b03a2e", label="ANOVA (additive + rank-$k$)")
ax[0].plot(ks, [g["svd_k"][str(k)] for k in ks], marker="s", color="#2e86c1", label="SVD rank-$k$")
ax[0].plot(ks, [g["svd_kplus2"][str(k)] for k in ks], marker="^", color="#27ae60", ls="--", label="SVD rank-$(k{+}2)$")
ax[0].set_xscale("log", base=2); ax[0].set_xlabel("$k$"); ax[0].set_ylabel("relative error")
ax[0].set_title("(a) named terms nearly free (GPT-2)"); ax[0].legend(fontsize=7); ax[0].grid(True, alpha=0.3)
models = [m for m in p4 if "error" not in p4[m]]
sf = [p4[m]["sink_frac_of_coleffect"] for m in models]
ax[1].bar(range(len(models)), sf, color="#7d3c98")
ax[1].set_xticks(range(len(models))); ax[1].set_xticklabels([short(m) for m in models], rotation=20, ha="right")
ax[1].set_ylim(0.9, 1.0); ax[1].set_ylabel("sink / column-effect energy")
ax[1].set_title("(b) the sink IS the column effect")
fig.tight_layout(); fig.savefig(f"{OUT}/fig8_anova_named.png", dpi=DPI); plt.close(fig)

# ---- Fig 9: editability ----
em = [m for m in p7 if "error" not in p7[m]]
x = np.arange(len(em)); w = 0.26
fig, ax = plt.subplots(figsize=(7.0, 3.2))
ax.bar(x - w, [p7[m]["anova"] for m in em], w, label="ANOVA (faithful)", color="#95a5a6")
ax.bar(x,     [p7[m]["nosink"] for m in em], w, label="sink removed", color="#b03a2e")
ax.bar(x + w, [p7[m]["zerocol_mid"] for m in em], w, label="random column removed (control)", color="#2e86c1")
ax.set_xticks(x); ax.set_xticklabels([short(m) for m in em], rotation=20, ha="right")
ax.set_ylabel("KL(true $\\Vert$ edited)")
ax.set_title("editing the named sink has effect $\\gg$ random column")
ax.legend(fontsize=7); fig.tight_layout()
fig.savefig(f"{OUT}/fig9_editability.png", dpi=DPI); plt.close(fig)

# ---- Fig 10: named fraction vs m ----
fig, ax = plt.subplots(figsize=(5.0, 3.2))
ms = [1, 3, 5]
colors = ["#b03a2e", "#2e86c1", "#27ae60", "#8e44ad", "#e67e22"]
for i, m in enumerate([k for k in p5 if "error" not in p5[k]]):
    if "named_frac" not in p5[m]:
        continue
    nf = [p5[m]["named_frac"][str(j)] for j in ms]
    ax.plot(ms, nf, marker="o", color=colors[i % len(colors)], label=short(m))
ax.set_xticks(ms); ax.set_xlabel("number of named atoms ($m$)")
ax.set_ylabel("fraction of energy in named components")
ax.set_ylim(0.7, 1.0); ax.set_title("most attention energy is nameable")
ax.legend(fontsize=7); ax.grid(True, alpha=0.3); fig.tight_layout()
fig.savefig(f"{OUT}/fig10_named_fraction.png", dpi=DPI); plt.close(fig)

for f in ["fig8_anova_named", "fig9_editability", "fig10_named_fraction"]:
    strip_png(f"{OUT}/{f}.png")
    im = Image.open(f"{OUT}/{f}.png"); print(f"{f}: {im.size[0]}x{im.size[1]} info={dict(im.info)}")
