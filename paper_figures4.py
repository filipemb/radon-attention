"""Task-gain figure (fig11), pooled over versioned seed files, EN labels, 300 dpi."""
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


def short(m): return m.split("/")[-1]


def mid_positions(positions, L=128):
    return [p for p in positions if 0.25 * L <= p <= 0.75 * L]


# pool seed files
files = sorted(glob.glob("out/phase8_lostmiddle_s*.json"))
assert files, "rode a campanha versionada primeiro"
pool = {}   # model -> beta -> pos -> [accs]
positions = None
for f in files:
    d = json.load(open(f))
    for m, r in d.items():
        if m.startswith("_") or "error" in r:
            continue
        positions = r["positions"]
        for beta, acc in r["acc"].items():
            for p in positions:
                pool.setdefault(m, {}).setdefault(beta, {}).setdefault(p, []).append(acc[str(p)])

models = sorted(pool)
mean = lambda m, b, p: float(np.mean(pool[m][b][p]))

fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0))

gm = "gpt2-medium" if "gpt2-medium" in pool else models[0]
base = [mean(gm, "1.0", p) for p in positions]
cal = [mean(gm, "0.25", p) for p in positions]
ax[0].plot(positions, base, marker="o", color="#7f8c8d", label="baseline ($\\beta=1$)")
ax[0].plot(positions, cal, marker="^", color="#b03a2e", label="sink calibrated ($\\beta=0.25$)")
ax[0].set_xlabel("target position in context"); ax[0].set_ylabel("retrieval accuracy")
ax[0].set_title(f"(a) {short(gm)}: calibration lifts the whole curve")
ax[0].legend(fontsize=7); ax[0].grid(True, alpha=0.3)

mids = mid_positions(positions)
gains = []
for m in models:
    g = np.mean([mean(m, "0.25", p) for p in mids]) - np.mean([mean(m, "1.0", p) for p in mids])
    gains.append(g)
order = np.argsort(gains)[::-1]
ax[1].bar(range(len(models)), [gains[i] for i in order], color="#2e86c1")
ax[1].axhline(0, color="k", lw=0.6)
ax[1].set_xticks(range(len(models)))
ax[1].set_xticklabels([short(models[i]) for i in order], rotation=20, ha="right")
ax[1].set_ylabel("middle-window accuracy gain")
ax[1].set_title("(b) gain from sink calibration ($\\beta=0.25$)")
for i, idx in enumerate(order):
    ax[1].text(i, gains[idx], f"{gains[idx]*100:+.0f}", ha="center", va="bottom", fontsize=7)

fig.tight_layout(); fig.savefig(f"{OUT}/fig11_taskgain.png", dpi=DPI); plt.close(fig)
strip_png(f"{OUT}/fig11_taskgain.png")
im = Image.open(f"{OUT}/fig11_taskgain.png")
print(f"fig11_taskgain: {im.size[0]}x{im.size[1]} info={dict(im.info)} (pooled de {len(files)} sementes)")
