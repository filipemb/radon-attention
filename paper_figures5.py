"""KV-benchmark figure (fig12), pooled over versioned seed files, EN labels, 300 dpi."""
import json, os, glob
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


files = sorted(glob.glob("out/phase11_kv_s*.json")) or ["out/phase11_kv.json"]
pool = {}
positions = None
for f in files:
    d = json.load(open(f))
    for m, r in d.items():
        if m.startswith("_") or "error" in r:
            continue
        positions = r["positions"]
        for beta in ["1.0", "0.25"]:
            if beta not in r:
                continue
            for p in positions:
                pool.setdefault(m, {}).setdefault(beta, {}).setdefault(p, []).append(r[beta][str(p)])

mean = lambda m, b, p: float(np.mean(pool[m][b][p]))
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0))
for k, (name, title) in enumerate([("gpt2-medium", "GPT-2-medium"), ("Qwen/Qwen2.5-3B", "Qwen2.5-3B")]):
    if name not in pool:
        continue
    base = [mean(name, "1.0", p) for p in positions]
    cal = [mean(name, "0.25", p) for p in positions]
    ax[k].plot(positions, base, marker="o", color="#7f8c8d", label="baseline")
    ax[k].plot(positions, cal, marker="^", color="#b03a2e", label="sink calibrated ($\\beta=0.25$)")
    ax[k].set_xlabel("queried pair position"); ax[k].set_ylabel("retrieval accuracy")
    ax[k].set_title(f"({'ab'[k]}) {title}"); ax[k].legend(fontsize=7); ax[k].grid(True, alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/fig12_kv.png", dpi=DPI); plt.close(fig)
strip_png(f"{OUT}/fig12_kv.png")
im = Image.open(f"{OUT}/fig12_kv.png")
print(f"fig12_kv: {im.size[0]}x{im.size[1]} info={dict(im.info)} (pooled de {len(files)} arquivos)")
