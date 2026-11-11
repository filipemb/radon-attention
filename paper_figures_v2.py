"""Paper figures v2 from stored results only (CPU, read only JSON/JSONL).

Reads aggregate JSON plus per instance JSONL. No experiment is recomputed,
except the two small closed form reconstructions of one stored example
(SVD by numpy, profiled lines by NNLS over the stored support atoms).
PNG 300 dpi, English labels, no metadata. No em or en dash in any text:
plain hyphen only inside numeric ranges or required model names, else "to".
"""
import json
import os
import sys

import numpy as np
from PIL import Image
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.optimize import nnls
from skimage.transform import radon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase06_profiled_lines import atom_vector
from phase24_p0_metrics import describe

OUT = "paper/figs"
os.makedirs(OUT, exist_ok=True)
DPI = 300

plt.rcParams.update({
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 7,
    "figure.dpi": DPI,
})

C_SVD = "#0072B2"
C_SVD_LIGHT = "#56B4E9"
C_PROF = "#E69F00"
C_UNIF = "#F0E442"
C_UNIF_EDGE = "#333333"
C_SL = "#009E73"
C_GEOM = "#D55E00"
C_GRAY = "#999999"
C_GRAY_D = "#555555"
C_SINK = "#CC79A7"
C_CTRL = "#999999"
C_IDENT = "#000000"

# (short slug, display name, phase24 aggregate path); 7B comes from phase27.
P24 = [
    ("gpt2", "GPT-2", "out/phase24_core_gpt2_n128_v2.json"),
    ("gpt2-medium", "GPT-2-medium", "out/phase24_core_gpt2-medium_n128_v2.json"),
    ("EleutherAI__pythia-410m", "Pythia-410m",
     "out/phase24_core_EleutherAI__pythia-410m_n128_v2.json"),
    ("EleutherAI__pythia-1.4b", "Pythia-1.4b",
     "out/phase24_core_EleutherAI__pythia-1.4b_n128_v2.json"),
    ("Qwen__Qwen2.5-0.5B", "Qwen2.5-0.5B",
     "out/phase24_core_Qwen__Qwen2.5-0.5B_n128_v2.json"),
    ("Qwen__Qwen2.5-3B", "Qwen2.5-3B",
     "out/phase24_core_Qwen__Qwen2.5-3B_n128_v2.json"),
]
QWEN7B = "out/phase27_qwen7b.json"
P30 = "out/phase30_anova_curves.json"
P30_SLUG = ["gpt2", "gpt2-medium", "EleutherAI__pythia-410m",
            "EleutherAI__pythia-1.4b", "Qwen__Qwen2.5-0.5B",
            "Qwen__Qwen2.5-3B", "Qwen__Qwen2.5-7B"]
P30_NAME = ["GPT-2", "GPT-2-medium", "Pythia-410m", "Pythia-1.4b",
            "Qwen2.5-0.5B", "Qwen2.5-3B", "Qwen2.5-7B"]
ALLOC = "out/phase21_allocation_v2.json"
ALLOC_MODELS = ["gpt2", "gpt2-medium", "EleutherAI/pythia-410m",
                "EleutherAI/pythia-1.4b", "Qwen/Qwen2.5-0.5B",
                "Qwen/Qwen2.5-3B"]
ALLOC_NAMES = ["GPT-2", "GPT-2-medium", "Pythia-410m", "Pythia-1.4b",
               "Qwen2.5-0.5B", "Qwen2.5-3B"]
DOCSTATS = "out/phase2_document_statistics_v2.json"
DOC_MODELS = ALLOC_MODELS
DOC_NAMES = ALLOC_NAMES
CORE_GPT2 = "out/pairs/core_gpt2_n128_v2.jsonl"
P30_GPT2 = "out/pairs/phase30_gpt2_n128.jsonl"
NPZ_GPT2 = "data/attn/gpt2_n128.npz"
P7_V2 = "out/phase7_editability_v2.json"
P7_V3 = "out/phase7_editability_v3.json"
P8_ITEMS = "out/phase8_items_v3.json"
P8_MM = "out/phase8_massmatched_items_v3.json"
P11_ITEMS = "out/phase11_items_v3.json"
P11_MM = "out/phase11_massmatched_items_v3.json"
P7_PAIRS = {
    "gpt2": "out/pairs/downstream_gpt2_uniform_v2.jsonl",
    "gpt2-medium": "out/pairs/downstream_gpt2-medium_uniform_v2.jsonl",
    "EleutherAI/pythia-410m":
        "out/pairs/downstream_EleutherAI__pythia-410m_uniform_v2.jsonl",
    "EleutherAI/pythia-1.4b":
        "out/pairs/downstream_EleutherAI__pythia-1.4b_uniform_v2.jsonl",
    "Qwen/Qwen2.5-0.5B":
        "out/pairs/downstream_Qwen__Qwen2.5-0.5B_uniform_v2.jsonl",
}
FIG9_MODELS = ["gpt2", "gpt2-medium", "EleutherAI/pythia-410m",
               "EleutherAI/pythia-1.4b", "Qwen/Qwen2.5-0.5B"]
FIG9_NAMES = ["GPT-2", "GPT-2-medium", "Pythia-410m", "Pythia-1.4b",
              "Qwen2.5-0.5B"]
FIG9B_MODELS = FIG9_MODELS + ["Qwen/Qwen2.5-3B"]
FIG9B_NAMES = FIG9_NAMES + ["Qwen2.5-3B"]
P8_MODELS = FIG9_MODELS
P8_NAMES = FIG9_NAMES

SOURCES = {"figures": {}, "notes": []}


def note(text):
    SOURCES["notes"].append(text)


def record(fig, panel, series):
    SOURCES["figures"].setdefault(fig, {})[panel] = series


def fail(panel, msg):
    raise RuntimeError("STOP panel %s: %s" % (panel, msg))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def med_ci(m, panel, field):
    try:
        ci = m["median_ci_document_bootstrap"]
        return float(m["median"]), float(ci[0]), float(ci[1])
    except KeyError:
        fail(panel, "missing median_ci_document_bootstrap in %s" % field)


def savefig_clean(fig, name):
    path = os.path.join(OUT, name)
    if not fig.get_constrained_layout():
        fig.tight_layout(pad=0.9, w_pad=2.5, h_pad=1.2)
    fig.savefig(path, dpi=DPI, metadata={"Software": None})
    plt.close(fig)
    im = Image.open(path).convert("RGB")
    clean = Image.new(im.mode, im.size)
    clean.putdata(list(im.getdata()))
    clean.save(path, "PNG")
    check = Image.open(path)
    assert dict(check.info) == {}, "metadata leaked into %s: %s" \
        % (name, check.info)
    return path


def fig1():
    panel = "1a"
    names, meds, los, his, rands = [], [], [], [], []
    for slug, disp, path in P24:
        d = load_json(path)
        try:
            m = d["metrics"]["radon_support"]
            r = float(d["random_support_median"])
        except KeyError:
            fail(panel, "missing metrics.radon_support or random_support_median "
                 "in %s" % path)
        med, lo, hi = med_ci(m, panel, path + ".metrics.radon_support")
        names.append(disp)
        meds.append(med)
        los.append(lo)
        his.append(hi)
        rands.append(r)
    d7 = load_json(QWEN7B)
    try:
        m7 = d7["datasets"]["128"]["metrics"]["radon_support"]
        r7 = float(d7["datasets"]["128"]["random_support_median"])
    except KeyError:
        fail(panel, "missing datasets.128.metrics.radon_support in %s" % QWEN7B)
    med7, lo7, hi7 = med_ci(m7, panel, QWEN7B + ".datasets.128")
    names.append("Qwen2.5-7B")
    meds.append(med7)
    los.append(lo7)
    his.append(hi7)
    rands.append(r7)

    fig, ax = plt.subplots(1, 2, figsize=(6.8, 3.0))
    x = np.arange(len(names))
    yerr = [np.array(meds) - np.array(los), np.array(his) - np.array(meds)]
    ax[0].errorbar(x, meds, yerr=yerr, fmt="o", color=C_SVD, ecolor=C_SVD,
                   capsize=3, markersize=4, label="Real Radon support")
    ax[0].axhline(float(np.median(rands)), color=C_GRAY_D, lw=1.2,
                  label="Random control median")
    ax[0].set_yscale("log")
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(names, rotation=25, ha="right")
    ax[0].set_ylabel("Effective support (median)")
    ax[0].set_title("(a) Concentration by model (n=128)")
    ax[0].legend()
    ax[0].grid(True, alpha=0.3, which="both")

    panel = "1b"
    rows = read_jsonl(CORE_GPT2)
    if not rows or "radon_support" not in rows[0]:
        fail(panel, "missing radon_support in %s" % CORE_GPT2)
    layers = sorted({int(r["layer"]) for r in rows})
    heads = sorted({int(r["head"]) for r in rows})
    grid = np.full((len(layers), len(heads)), np.nan)
    for li, l in enumerate(layers):
        for hi, h in enumerate(heads):
            vals = [float(r["radon_support"]) for r in rows
                    if int(r["layer"]) == l and int(r["head"]) == h]
            if vals:
                grid[li, hi] = float(np.median(vals))
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("white")
    im = ax[1].imshow(grid, norm=LogNorm(vmin=np.nanmin(grid),
                                        vmax=np.nanmax(grid)),
                      cmap=cmap, aspect="auto", interpolation="nearest")
    ax[1].set_xticks(range(len(heads)))
    ax[1].set_xticklabels([str(h) for h in heads])
    ax[1].set_yticks(range(len(layers)))
    ax[1].set_yticklabels([str(l) for l in layers])
    ax[1].set_xlabel("Head")
    ax[1].set_ylabel("Layer")
    ax[1].set_title("(b) GPT-2 median support by layer and head")
    cb = fig.colorbar(im, ax=ax[1], shrink=0.95)
    cb.set_label("Median effective support")
    savefig_clean(fig, "v2_fig1_concentration.png")
    record("v2_fig1_concentration.png", "(a) real medians with CI",
           [{"series": "median radon_support", "file": p,
             "field": "metrics.radon_support.median"} for _, _, p in P24]
           + [{"series": "median radon_support",
               "file": QWEN7B, "field": "datasets.128.metrics.radon_support.median"}])
    ci_series = [{"series": "95 percent CI of median", "file": p,
                  "field": "metrics.radon_support.median_ci_document_bootstrap"}
                 for _, _, p in P24]
    ci_series.append({"series": "95 percent CI of median", "file": QWEN7B,
                      "field": "datasets.128.metrics.radon_support."
                               "median_ci_document_bootstrap"})
    ci_series.append({"series": "random control median line",
                      "file": "out/phase24_core_*_n128_v2.json and " + QWEN7B,
                      "field": "random_support_median"})
    record("v2_fig1_concentration.png", "(a) CI and random line", ci_series)
    record("v2_fig1_concentration.png", "(b) layer by head map",
           [{"series": "cell median of radon_support", "file": CORE_GPT2,
             "field": "radon_support (median over instances per layer, head)"}])


RECON_CHECK = {}


def curve_series(metrics, prefix, ks, panel, src):
    out = []
    for k in ks:
        key = "%s_k%d_relative_error" % (prefix, k)
        if key not in metrics:
            fail(panel, "missing %s in %s" % (key, src))
        med, lo, hi = med_ci(metrics[key], panel, src + "." + key)
        out.append((med, lo, hi))
    return out


def fig2():
    panel = "2a/2b"
    agg = load_json(P30)
    try:
        metrics = agg["datasets"]["gpt2_n128"]["metrics"]
    except KeyError:
        fail(panel, "missing datasets.gpt2_n128.metrics in %s" % P30)
    ks = [1, 2, 4, 8, 16, 32]
    uni = curve_series(metrics, "uniform_line", ks, panel, P30 + ".gpt2_n128")
    prof = curve_series(metrics, "profiled_line", ks, panel, P30 + ".gpt2_n128")
    svd = curve_series(metrics, "svd", ks, panel, P30 + ".gpt2_n128")

    # Absolute errors: no absolute field in phase30; per instance
    # relative error times attention_frobenius_norm, median only.
    rows = read_jsonl(P30_GPT2)
    if "attention_frobenius_norm" not in rows[0]:
        fail("2b", "missing attention_frobenius_norm in %s" % P30_GPT2)
    abs_med = {}
    for prefix, tag in [("uniform_line", "uniform"),
                        ("profiled_line", "profiled"), ("svd", "svd")]:
        for k in ks:
            key = "%s_k%d_relative_error" % (prefix, k)
            if key not in rows[0]:
                fail("2b", "missing %s in %s" % (key, P30_GPT2))
            vals = [float(r[key]) * float(r["attention_frobenius_norm"])
                    for r in rows]
            abs_med[(tag, k)] = float(np.median(vals))

    fig = plt.figure(figsize=(6.8, 5.6))
    gs = fig.add_gridspec(2, 14, height_ratios=[1.0, 1.05])
    ax_a = fig.add_subplot(gs[0, 0:6])
    ax_b = fig.add_subplot(gs[0, 7:14])
    for ax, data, ylabel, title in [
            (ax_a,
             [(uni, C_UNIF, C_UNIF_EDGE, "s", "Uniform lines"),
              (prof, C_PROF, C_PROF, "o", "Profiled lines"),
              (svd, C_SVD, C_SVD, "^", "Rank k SVD")],
             "Relative error (median)",
             "(a) GPT-2 relative error to k"),
            (ax_b, None, "Absolute error (median Frobenius)",
             "(b) GPT-2 absolute error to k")]:
        if data is None:
            continue
        for series, col, edge, mk, lab in data:
            med = [v[0] for v in series]
            lo = [v[1] for v in series]
            hi = [v[2] for v in series]
            ax.fill_between(ks, lo, hi, color=col, alpha=0.25,
                            edgecolor=edge, linewidth=0.5)
            ax.plot(ks, med, color=col, marker=mk, markersize=4,
                    markerfacecolor=col, markeredgecolor=edge,
                    markeredgewidth=0.8, linewidth=1.6, label=lab)
        ax.set_xscale("log", base=2)
        ax.set_xticks(ks)
        ax.set_xticklabels([str(k) for k in ks])
        ax.set_xlabel("Budget k (lines) or rank k (SVD)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3, which="both")
    for tag, col, edge, mk, lab in [
            ("uniform", C_UNIF, C_UNIF_EDGE, "s", "Uniform lines"),
            ("profiled", C_PROF, C_PROF, "o", "Profiled lines"),
            ("svd", C_SVD, C_SVD, "^", "Rank k SVD")]:
        ax_b.plot(ks, [abs_med[(tag, k)] for k in ks], color=col, marker=mk,
                  markersize=4, markerfacecolor=col, markeredgecolor=edge,
                  markeredgewidth=0.8, linewidth=1.6, label=lab)
    ax_b.set_xscale("log", base=2)
    ax_b.set_xticks(ks)
    ax_b.set_xticklabels([str(k) for k in ks])
    ax_b.set_xlabel("Budget k (lines) or rank k (SVD)")
    ax_b.set_ylabel("Absolute error (median Frobenius)")
    ax_b.yaxis.set_label_position("right")
    ax_b.yaxis.tick_right()
    ax_b.yaxis.set_ticks_position("right")
    ax_b.set_title("(b) GPT-2 absolute error to k")
    ax_b.legend()
    ax_b.grid(True, alpha=0.3, which="both")
    return fig, gs, ks


def fig2_example(fig, gs):
    panel = "2c"
    core = read_jsonl(CORE_GPT2)
    if "paired_relative_error_line_minus_svd" not in core[0]:
        fail(panel, "missing paired_relative_error_line_minus_svd in %s"
             % CORE_GPT2)
    diffs = np.array([float(r["paired_relative_error_line_minus_svd"])
                      for r in core])
    med = float(np.median(diffs))
    order = sorted(core,
                   key=lambda r: (abs(float(
                       r["paired_relative_error_line_minus_svd"]) - med),
                       str(r["instance_id"])))
    rec = order[0]
    n = int(rec["n"])
    if "line_support" not in rec or "attention_frobenius_norm" not in rec:
        fail(panel, "missing line_support or attention_frobenius_norm in %s"
             % CORE_GPT2)
    z = np.load(NPZ_GPT2)
    di, la, he = int(rec["document_index"]), int(rec["layer"]), int(rec["head"])
    hit = np.where((z["document_index"] == di) & (z["layer"] == la)
                   & (z["head"] == he))[0]
    if len(hit) != 1:
        fail(panel, "npz match count %d for %s" % (len(hit), rec["instance_id"]))
    A = z["attention"][int(hit[0])].astype(np.float64)
    cols = [atom_vector(str(kind), float(param) if isinstance(param, float)
                        else int(param), n)
            for kind, param, _ in rec["line_support"][:8]]
    M = np.stack(cols, axis=1)
    coefs, _ = nnls(M, A.ravel())
    A_prof = (M @ coefs).reshape(n, n)
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    A_svd = (U[:, :8] * S[:8]) @ Vt[:8, :]
    nA = float(np.linalg.norm(A)) + 1e-12
    rel_prof = float(np.linalg.norm(A_prof - A) / nA)
    rel_svd = float(np.linalg.norm(A_svd - A) / nA)
    d_prof = abs(rel_prof - float(rec["profiled_line_k8_relative_error"]))
    d_svd = abs(rel_svd - float(rec["svd_k8_relative_error"]))
    ok = bool(d_prof <= 1e-9 and d_svd <= 1e-9)
    RECON_CHECK.update({"instance_id": str(rec["instance_id"]),
                        "median_paired_gap": med,
                        "instance_paired_gap": float(
                            rec["paired_relative_error_line_minus_svd"]),
                        "recomputed_profiled_rel": rel_prof,
                        "stored_profiled_rel": float(
                            rec["profiled_line_k8_relative_error"]),
                        "abs_diff_profiled": d_prof,
                        "recomputed_svd_rel": rel_svd,
                        "stored_svd_rel": float(rec["svd_k8_relative_error"]),
                        "abs_diff_svd": d_svd,
                        "tol": 1e-9, "match": ok})
    mats = [("Original", A, None), ("SVD rank k=8", A_svd, rel_svd),
            ("Profiled lines k=8", A_prof, rel_prof)]
    pos = np.concatenate([m.reshape(-1) for _, m, _ in mats])
    pos = pos[pos > 0]
    norm = LogNorm(vmin=float(pos.min()), vmax=float(np.max(pos)))
    cmap = plt.get_cmap("viridis")
    axes = [fig.add_subplot(gs[1, 0:4]), fig.add_subplot(gs[1, 4:8]),
            fig.add_subplot(gs[1, 8:12])]
    last_im = None
    for axi, (title, mat, rel) in zip(axes, mats):
        masked = np.ma.masked_where(mat <= 0, mat)
        last_im = axi.imshow(masked, cmap=cmap, norm=norm,
                             interpolation="nearest", aspect="equal")
        axi.set_xticks([])
        axi.set_yticks([])
        axi.set_title(title)
        if rel is not None:
            axi.set_xlabel("rel err %.3f" % rel)
    axes[0].set_title("(c) Original")
    cax = fig.add_subplot(gs[1, 12:14])
    cb = fig.colorbar(last_im, cax=cax)
    cb.set_label("Attention weight", fontsize=8)
    cax.tick_params(labelsize=7)
    note("Fig2c example %s layer %d head %d, paired gap %.6f to median %.6f; "
         "recon check tol 1e-9 profiled diff %.3g svd diff %.3g match %s"
         % (rec["instance_id"], la, he,
            float(rec["paired_relative_error_line_minus_svd"]), med,
            d_prof, d_svd, ok))
    record("v2_fig2_reconstruction.png", "(c) example matrices",
           [{"series": "original attention", "file": NPZ_GPT2,
             "field": "attention matched by document_index, layer, head"},
            {"series": "SVD k=8 of stored matrix", "file": NPZ_GPT2,
             "field": "attention (numpy SVD, closed form)"},
            {"series": "profiled lines k=8", "file": CORE_GPT2,
             "field": "line_support atoms refit by NNLS via "
                      "phase06_profiled_lines.atom_vector"},
            {"series": "chosen instance", "file": CORE_GPT2,
             "field": "paired_relative_error_line_minus_svd "
                      "(closest to median)"}])
    record("v2_fig2_reconstruction.png", "(a) relative curves",
           [{"series": "uniform/profiled/SVD k=%d" % k, "file": P30,
             "field": "datasets.gpt2_n128.metrics."
                      "{uniform_line,profiled_line,svd}_k%d_relative_error"
                      ".median" % k} for k in [1, 2, 4, 8, 16, 32]]
           + [{"series": "CI bands", "file": P30,
               "field": "datasets.gpt2_n128.metrics.*."
                        "median_ci_document_bootstrap"}])
    record("v2_fig2_reconstruction.png", "(b) absolute medians",
           [{"series": "median of instance %s times "
                      "attention_frobenius_norm" % k, "file": P30_GPT2,
             "field": "per instance {uniform_line,profiled_line,svd}_k%d_"
                      "relative_error x attention_frobenius_norm; "
                      "median only, no CI" % k}
            for k in [1, 2, 4, 8, 16, 32]])


def phase24_block():
    """Return per model dicts for the 7 models at n=128."""
    out = []
    for slug, disp, path in P24:
        out.append((disp, load_json(path)))
    d7 = load_json(QWEN7B)
    out.append(("Qwen2.5-7B", {"metrics": d7["datasets"]["128"]["metrics"],
                               "concentration_real_to_random_ratio":
                               d7["datasets"]["128"]
                               ["concentration_real_to_random_ratio"]}))
    return out


def fig5():
    panel = "5a"
    blocks = phase24_block()
    names = [b[0] for b in blocks]
    line, slo, shi, svd, vlo, vhi, ratio = [], [], [], [], [], [], []
    files = [p for _, _, p in P24] + [QWEN7B + ".datasets.128"]
    for (disp, d), src in zip(blocks, files):
        try:
            ml = d["metrics"]["profiled_line_k8_relative_error"]
            ms = d["metrics"]["svd_k8_relative_error"]
            ra = float(d["concentration_real_to_random_ratio"])
        except KeyError:
            fail(panel, "missing k8 errors or ratio in %s" % src)
        a, alo, ahi = med_ci(ml, panel, src + ".profiled_line_k8")
        b, blo, bhi = med_ci(ms, panel, src + ".svd_k8")
        line.append(a)
        slo.append(alo)
        shi.append(ahi)
        svd.append(b)
        vlo.append(blo)
        vhi.append(bhi)
        ratio.append(ra)
    fig, ax = plt.subplots(1, 2, figsize=(6.8, 3.1))
    x = np.arange(len(names))
    w = 0.38
    ax[0].bar(x - w / 2, line, w, yerr=[np.array(line) - np.array(slo),
                                        np.array(shi) - np.array(line)],
              color=C_PROF, ecolor=C_GRAY_D, capsize=2, label="Lines k=8")
    ax[0].bar(x + w / 2, svd, w, yerr=[np.array(svd) - np.array(vlo),
                                       np.array(vhi) - np.array(svd)],
              color=C_SVD, ecolor=C_GRAY_D, capsize=2, label="SVD k=8")
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(names, rotation=25, ha="right")
    ax[0].set_ylabel("Relative error (median)")
    ax[0].set_title("(a) Line k=8 and SVD k=8 by model")
    ax[0].legend()
    ax[0].grid(True, alpha=0.3, axis="y")
    ax[1].bar(x, ratio, color=C_GRAY, edgecolor=C_GRAY_D)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(names, rotation=25, ha="right")
    ax[1].set_ylabel("Concentration ratio (real to random)")
    ax[1].set_title("(b) Real to random ratio by model")
    ax[1].grid(True, alpha=0.3, axis="y")
    savefig_clean(fig, "v2_fig5_multimodel.png")
    record("v2_fig5_multimodel.png", "(a) paired bars",
           [{"series": "median profiled line k=8", "file": f,
             "field": "metrics.profiled_line_k8_relative_error.median"}
            for f in files]
           + [{"series": "median SVD k=8", "file": f,
               "field": "metrics.svd_k8_relative_error.median"} for f in files]
           + [{"series": "95 percent CI of each median", "file": f,
               "field": "*.median_ci_document_bootstrap"} for f in files])
    record("v2_fig5_multimodel.png", "(b) ratio bars",
           [{"series": "concentration ratio", "file": f,
             "field": "concentration_real_to_random_ratio"} for f in files])


def fig6():
    panel = "6"
    doc = load_json(DOCSTATS)
    ranks = [1, 2, 4, 8, 16, 32]
    ref_x = [64, 128, 256]
    ref_arms = [("phase2:uniform", "s", "Uniform causal"),
                ("phase2:diagonal", "^", "Diagonal only"),
                ("phase2:sink", "D", "Sink only")]
    fig, axes = plt.subplots(2, 3, figsize=(6.8, 4.4), sharex=True)
    for axi, model, disp in zip(axes.flat, DOC_MODELS, DOC_NAMES):
        try:
            arms = doc[model]["arms"]
        except KeyError:
            fail(panel, "missing arms for %s in %s" % (model, DOCSTATS))
        med, lo, hi = [], [], []
        for k in ranks:
            key = "phase2:svd:%d" % k
            if key not in arms:
                fail(panel, "missing %s for %s" % (key, model))
            m = arms[key]
            try:
                ci = m["median_kl_ci95_document_bootstrap"]
            except KeyError:
                fail(panel, "missing median_kl_ci95_document_bootstrap in "
                     "%s %s" % (model, key))
            med.append(float(m["median_kl"]))
            lo.append(float(ci[0]))
            hi.append(float(ci[1]))
        yerr = [np.array(med) - np.array(lo), np.array(hi) - np.array(med)]
        axi.errorbar(ranks, med, yerr=yerr, fmt="o-", color=C_SVD,
                     ecolor=C_SVD, capsize=2, markersize=3, label="SVD")
        if "phase2:geom" not in arms:
            fail(panel, "missing phase2:geom for %s" % model)
        g = float(arms["phase2:geom"]["median_kl"])
        axi.axhline(g, color=C_GEOM, linestyle=(0, (4, 2)), lw=1.4,
                    label="Geometric 15 atoms")
        for rx, (arm, mk, lab) in zip(ref_x, ref_arms):
            if arm not in arms:
                fail(panel, "missing %s for %s" % (arm, model))
            m = arms[arm]
            ci = m["median_kl_ci95_document_bootstrap"]
            axi.errorbar([rx], [float(m["median_kl"])],
                         yerr=[[float(m["median_kl"]) - float(ci[0])],
                               [float(ci[1]) - float(m["median_kl"])]],
                         fmt=mk, color=C_GRAY_D, ecolor=C_GRAY_D, capsize=2,
                         markersize=4, label=lab)
        axi.set_xscale("log", base=2)
        axi.set_xticks(ranks + ref_x)
        axi.set_xticklabels(["1", "2", "4", "8", "16", "32", "U", "D", "S"])
        axi.set_title(disp)
        axi.grid(True, alpha=0.3, which="both")
    axes[1, 0].set_ylabel("KL to reference (median, last token)")
    axes[1, 1].set_xlabel("SVD rank k, then U D S refs")
    axes[0, 0].legend(loc="upper left")
    savefig_clean(fig, "v2_fig6_downstream.png")
    record("v2_fig6_downstream.png", "SVD curves (all panels)",
           [{"series": "median KL at SVD rank k, model %s" % m, "file": DOCSTATS,
             "field": "%s.arms.phase2:svd:k.median_kl" % m} for m in DOC_MODELS]
           + [{"series": "95 percent CI of median KL", "file": DOCSTATS,
               "field": "*.arms.*.median_kl_ci95_document_bootstrap"}])
    record("v2_fig6_downstream.png", "geom line and gray refs",
           [{"series": "geometric 15 atom median KL", "file": DOCSTATS,
             "field": "%s.arms.phase2:geom.median_kl" % m} for m in DOC_MODELS]
           + [{"series": "uniform/diagonal/sink median KL", "file": DOCSTATS,
               "field": "%s.arms.{phase2:uniform,phase2:diagonal,phase2:sink}."
                        "median_kl" % m} for m in DOC_MODELS])


def fig8():
    panel = "8a"
    agg = load_json(P30)
    try:
        gm = agg["datasets"]["gpt2_n128"]["metrics"]
    except KeyError:
        fail(panel, "missing datasets.gpt2_n128.metrics in %s" % P30)
    aks = [4, 8, 16]
    add, alo, ahi, s1, s1l, s1h, s2, s2l, s2h = ([] for _ in range(9))
    for k in aks:
        ka = "anova_addrank%d_relative_error" % k
        k1 = "svd_k%d_relative_error" % k
        k2 = "svd_k%d_relative_error" % (k + 2)
        for key, store in [(ka, (add, alo, ahi)), (k1, (s1, s1l, s1h)),
                           (k2, (s2, s2l, s2h))]:
            if key not in gm:
                fail(panel, "missing %s in %s" % (key, P30))
            med, lo, hi = med_ci(gm[key], panel, P30 + ".gpt2_n128." + key)
            store[0].append(med)
            store[1].append(lo)
            store[2].append(hi)
    fig, ax = plt.subplots(1, 2, figsize=(6.8, 3.1))
    x = np.arange(len(aks))
    w = 0.24
    triples = [(add, alo, ahi, C_SL, "Additive + rank k"),
               (s1, s1l, s1h, C_SVD, "SVD rank k"),
               (s2, s2l, s2h, C_SVD_LIGHT, "SVD rank k+2")]
    for i, (med, lo, hi, col, lab) in enumerate(triples):
        ax[0].bar(x + (i - 1) * w, med, w,
                  yerr=[np.array(med) - np.array(lo),
                        np.array(hi) - np.array(med)],
                  color=col, ecolor=C_GRAY_D, capsize=2, label=lab)
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(["k=%d" % k for k in aks])
    ax[0].set_ylabel("Relative error (median)")
    ax[0].set_title("(a) GPT-2 additive vs SVD")
    ax[0].legend()
    ax[0].grid(True, alpha=0.3, axis="y")

    panel = "8b"
    names, med, lo, hi = [], [], [], []
    for slug, disp in zip(P30_SLUG, P30_NAME):
        key = slug + "_n128"
        try:
            m = agg["datasets"][key]["metrics"][
                "sink_frac_of_column_effect_energy"]
        except KeyError:
            fail(panel, "missing sink frac in %s %s" % (P30, key))
        a, b, c = med_ci(m, panel, P30 + "." + key + ".sink_frac")
        names.append(disp)
        med.append(a)
        lo.append(b)
        hi.append(c)
    x = np.arange(len(names))
    ax[1].bar(x, med, color=C_GRAY, edgecolor=C_GRAY_D,
              yerr=[np.array(med) - np.array(lo),
                    np.array(hi) - np.array(med)],
              ecolor=C_GRAY_D, capsize=2)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(names, rotation=25, ha="right")
    ax[1].set_ylabel("Sink fraction of column energy (median)")
    ax[1].set_title("(b) Sink share by model (n=128)")
    ax[1].grid(True, alpha=0.3, axis="y")
    savefig_clean(fig, "v2_fig8_anova.png")
    record("v2_fig8_anova.png", "(a) additive vs SVD bars",
           [{"series": "additive + rank k=%d" % k, "file": P30,
             "field": "datasets.gpt2_n128.metrics."
                      "anova_addrank%d_relative_error.median" % k}
            for k in aks]
           + [{"series": "SVD rank k=%d and k=%d" % (k, k + 2), "file": P30,
               "field": "datasets.gpt2_n128.metrics.svd_k%d_relative_error."
                        "median and svd_k%d" % (k, k + 2)} for k in aks]
           + [{"series": "95 percent CI of each median", "file": P30,
               "field": "datasets.gpt2_n128.metrics.*."
                        "median_ci_document_bootstrap"}])
    record("v2_fig8_anova.png", "(b) sink fraction bars",
           [{"series": "median sink fraction, %s" % s, "file": P30,
             "field": "datasets.%s_n128.metrics."
                      "sink_frac_of_column_effect_energy.median" % s}
            for s in P30_SLUG]
           + [{"series": "95 percent CI of median", "file": P30,
               "field": "*.metrics.sink_frac_of_column_effect_energy."
                        "median_ci_document_bootstrap"}])


def fig10():
    panel = "10"
    d = load_json(ALLOC)
    try:
        sup = d["allocation_at_common_K8_q7_supplement"]
    except KeyError:
        fail(panel, "missing allocation_at_common_K8_q7_supplement in %s"
             % ALLOC)
    # v2 stores the iterative Algorithm 1 procedure under
    # algorithm_1_5_iterations; that is the v1 "alternating" convention.
    convs = [("named_first", "Named first", C_PROF),
             ("lowrank_first", "Low rank first", C_SVD),
             ("algorithm_1_5_iterations", "Alternating (Algo 1)", C_SL)]
    vals = {c: [] for c, _, _ in convs}
    los = {c: [] for c, _, _ in convs}
    his = {c: [] for c, _, _ in convs}
    for model in ALLOC_MODELS:
        try:
            c128 = sup[model]["128"]["conventions"]
        except KeyError:
            fail(panel, "missing supplement for %s 128" % model)
        for c, _, _ in convs:
            if c not in c128:
                fail(panel, "missing convention %s for %s" % (c, model))
            m = c128[c]["metrics"].get("named_energy_ratio")
            if m is None:
                fail(panel, "missing named_energy_ratio for %s %s"
                     % (model, c))
            a, b, cc = med_ci(m, panel, ALLOC + "." + model + "." + c)
            vals[c].append(a)
            los[c].append(b)
            his[c].append(cc)
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    x = np.arange(len(ALLOC_MODELS))
    w = 0.24
    for i, (c, lab, col) in enumerate(convs):
        ax.bar(x + (i - 1) * w, vals[c], w,
               yerr=[np.array(vals[c]) - np.array(los[c]),
                     np.array(his[c]) - np.array(vals[c])],
               color=col, ecolor=C_GRAY_D, capsize=2, label=lab)
    ax.set_xticks(x)
    ax.set_xticklabels(ALLOC_NAMES, rotation=25, ha="right")
    ax.set_ylabel("Named energy fraction (median)")
    ax.set_title("Named energy by convention (n=128)")
    ax.set_ylim(0, 1.02)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    savefig_clean(fig, "v2_fig10_named.png")
    record("v2_fig10_named.png", "grouped bars",
           [{"series": "median named energy, %s, %s" % (m, c), "file": ALLOC,
             "field": "allocation_at_common_K8_q7_supplement.%s.128."
                      "conventions.%s.metrics.named_energy_ratio.median"
                      % (m, c)} for m in ALLOC_MODELS for c, _, _ in convs]
           + [{"series": "95 percent CI of median", "file": ALLOC,
               "field": "*.named_energy_ratio.median_ci_document_bootstrap"}])
    note("Fig10 third convention: task names it alternating; %s stores it "
         "as algorithm_1_5_iterations (v1 alternating procedure, 5 fixed "
         "iterations of Algorithm 1 per _meta.ALT)" % ALLOC)


def pick_by_support(rows, layer, which):
    sub = [r for r in rows if int(r["layer"]) == layer]
    if not sub:
        fail("4", "no instances at layer %d in %s" % (layer, CORE_GPT2))
    vals = np.array([float(r["radon_support"]) for r in sub])
    if which == "min":
        order = sorted(sub, key=lambda r: (float(r["radon_support"]),
                                           str(r["instance_id"])))
        return order[0]
    if which == "max":
        order = sorted(sub, key=lambda r: (-float(r["radon_support"]),
                                           str(r["instance_id"])))
        return order[0]
    med = float(np.median(vals))
    order = sorted(sub, key=lambda r: (abs(float(r["radon_support"]) - med),
                                       str(r["instance_id"])))
    return order[0]


def fig4():
    panel = "4"
    rows = read_jsonl(CORE_GPT2)
    if "radon_support" not in rows[0]:
        fail(panel, "missing radon_support in %s" % CORE_GPT2)
    layers = sorted({int(r["layer"]) for r in rows})
    mid = layers[len(layers) // 2]
    last = layers[-1]
    chosen = [(0, "min", "(a) Layer 0, smallest support"),
              (mid, "median", "(b) Layer %d, median support" % mid),
              (last, "max", "(c) Layer %d, largest support" % last)]
    z = np.load(NPZ_GPT2)
    theta = np.arange(0, 179, 2)
    fig, axes = plt.subplots(3, 2, figsize=(3.3, 4.6))
    picks = []
    for (lay, which, title), axi in zip(chosen, axes):
        rec = pick_by_support(rows, lay, which)
        di, la, he = (int(rec["document_index"]), int(rec["layer"]),
                      int(rec["head"]))
        hit = np.where((z["document_index"] == di) & (z["layer"] == la)
                       & (z["head"] == he))[0]
        if len(hit) != 1:
            fail(panel, "npz match count %d for %s"
                 % (len(hit), rec["instance_id"]))
        A = z["attention"][int(hit[0])].astype(np.float64)
        sino = radon(A, theta=theta, circle=False)
        picks.append((rec, float(rec["radon_support"])))
        for mat, a in [(A, axi[0]), (sino, axi[1])]:
            masked = np.ma.masked_where(mat <= 0, mat)
            a.imshow(masked, cmap="viridis",
                     norm=LogNorm(vmin=float(masked.min()),
                                  vmax=float(masked.max())),
                     interpolation="nearest", aspect="auto")
            a.set_xticks([])
            a.set_yticks([])
        axi[0].set_title(title, fontsize=8)
        axi[0].set_ylabel("log scale", fontsize=8)
    axes[0, 0].text(-0.32, 0.5, "Attention", transform=axes[0, 0].transAxes,
                    rotation=90, va="center", ha="center")
    axes[0, 1].text(-0.32, 0.5, "Sinogram", transform=axes[0, 1].transAxes,
                    rotation=90, va="center", ha="center")
    savefig_clean(fig, "v2_fig4_examples.png")
    for (rec, _), (lay, which, _) in zip(picks, chosen):
        note("Fig4 %s pick: %s layer %d head %d radon_support %.6g"
             % (which, rec["instance_id"], lay, int(rec["head"]),
                float(rec["radon_support"])))
    record("v2_fig4_examples.png", "matrices and sinograms",
           [{"series": "original attention", "file": NPZ_GPT2,
             "field": "attention matched by document_index, layer, head"},
            {"series": "choice rule", "file": CORE_GPT2,
             "field": "radon_support (min at layer 0, median at layer %d, "
                      "max at layer %d)" % (mid, last)},
            {"series": "sinogram", "file": NPZ_GPT2,
             "field": "skimage.transform.radon of stored attention, "
                      "theta 0 to 178 step 2"}])


def pairs_median_ci_kl(pairs_path, arm, panel):
    """Median KL with 95 percent document bootstrap CI from stored pairs.

    Same procedure as phase24_p0_metrics.describe over per article rows.
    Read only; no experiment is recomputed.
    """
    vals, docs = [], []
    for r in read_jsonl(pairs_path):
        if r.get("arm") != arm:
            continue
        if "kl" not in r or "document_index" not in r:
            fail(panel, "missing kl or document_index in %s" % pairs_path)
        vals.append(float(r["kl"]))
        docs.append(int(r["document_index"]))
    if not vals:
        fail(panel, "no rows for arm %s in %s" % (arm, pairs_path))
    out = describe(vals, docs)
    return float(out["median"]), float(out["median_ci_document_bootstrap"][0]), \
        float(out["median_ci_document_bootstrap"][1])


def gain_pp(block, panel, src):
    """Median seed accuracy gain in percentage points with 95 percent CI."""
    try:
        g = float(block["median_seed_accuracy_gain"])
        ci = block["median_seed_gain_ci95_item_bootstrap"]
    except KeyError:
        fail(panel, "missing median_seed_accuracy_gain or "
             "median_seed_gain_ci95_item_bootstrap in %s" % src)
    return 100.0 * g, 100.0 * float(ci[0]), 100.0 * float(ci[1])


def fig9():
    panel = "9a"
    d7 = load_json(P7_V2)
    arms = ["phase7:anova:8", "phase7:nosink:8", "phase7:zerocol_mid:8"]
    arm_meta = [(arms[0], "ANOVA alone", C_SVD),
                (arms[1], "Sink removed", C_SINK),
                (arms[2], "Mid column removed", C_PROF)]
    meds = {a: [] for a, _, _ in arm_meta}
    los = {a: [] for a, _, _ in arm_meta}
    his = {a: [] for a, _, _ in arm_meta}
    for model in FIG9_MODELS:
        try:
            am = d7[model]["arms"]
        except KeyError:
            fail(panel, "missing arms for %s in %s" % (model, P7_V2))
        if model not in P7_PAIRS:
            fail(panel, "no pairs path for %s" % model)
        for a, _, _ in arm_meta:
            if a not in am or "median_kl" not in am[a]:
                fail(panel, "missing %s.median_kl for %s" % (a, model))
            med = float(am[a]["median_kl"])
            cmed, clo, chi = pairs_median_ci_kl(P7_PAIRS[model], a, panel)
            if abs(cmed - med) > 1e-9:
                fail(panel, "pairs median %g disagrees with stored %g "
                     "for %s %s" % (cmed, med, model, a))
            meds[a].append(med)
            los[a].append(clo)
            his[a].append(chi)
    fig, ax = plt.subplots(1, 2, figsize=(6.8, 3.1))
    x = np.arange(len(FIG9_MODELS))
    w = 0.24
    for i, (a, lab, col) in enumerate(arm_meta):
        ax[0].bar(x + (i - 1) * w, meds[a], w,
                  yerr=[np.array(meds[a]) - np.array(los[a]),
                        np.array(his[a]) - np.array(meds[a])],
                  color=col, ecolor=C_GRAY_D, capsize=2, label=lab)
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(FIG9_NAMES, rotation=25, ha="right")
    ax[0].set_ylabel("KL to reference (median, last token)")
    ax[0].set_title("(a) Decomposition edits by model")
    ax[0].legend()
    ax[0].grid(True, alpha=0.3, axis="y")
    record("v2_fig9_editability.png", "(a) grouped bars",
           [{"series": "median KL, %s, %s" % (m, a), "file": P7_V2,
             "field": "%s.arms.%s.median_kl" % (m, a)}
            for m in FIG9_MODELS for a in arms]
           + [{"series": "95 percent CI of median KL, %s, %s" % (m, a),
               "file": P7_PAIRS[m],
               "field": "kl grouped by document_index via "
                        "phase24_p0_metrics.describe"}
              for m in FIG9_MODELS for a in arms])

    panel = "9b"
    d3 = load_json(P7_V3)
    try:
        models3 = d3["models"]
    except KeyError:
        fail(panel, "missing models in %s" % P7_V3)
    beta_arms = [("sink_beta0_matched", "Sink beta 0", C_SINK, None),
                 ("control_beta0_matched", "Control beta 0", C_CTRL, None),
                 ("sink_beta0.25_matched", "Sink beta 0.25", C_SINK, "///"),
                 ("control_beta0.25_matched", "Control beta 0.25", C_CTRL,
                  "///")]
    bmed = {a: [] for a, _, _, _ in beta_arms}
    blo = {a: [] for a, _, _, _ in beta_arms}
    bhi = {a: [] for a, _, _, _ in beta_arms}
    for model in FIG9B_MODELS:
        try:
            ctx = models3[model]["contexts"]["identity"]["arms"]
        except KeyError:
            fail(panel, "missing contexts.identity.arms for %s" % model)
        for a, _, _, _ in beta_arms:
            if a not in ctx or "kl_true" not in ctx[a]:
                fail(panel, "missing %s.kl_true for %s" % (a, model))
            kt = ctx[a]["kl_true"]
            try:
                ci = kt["median_ci_document_bootstrap"]
                bmed[a].append(float(kt["median"]))
                blo[a].append(float(ci[0]))
                bhi[a].append(float(ci[1]))
            except KeyError:
                fail(panel, "missing kl_true.median or "
                     "median_ci_document_bootstrap for %s %s" % (model, a))
    x = np.arange(len(FIG9B_MODELS))
    w = 0.18
    for i, (a, lab, col, hatch) in enumerate(beta_arms):
        ax[1].bar(x + (i - 1.5) * w, bmed[a], w,
                  yerr=[np.array(bmed[a]) - np.array(blo[a]),
                        np.array(bhi[a]) - np.array(bmed[a])],
                  color=col, ecolor=C_GRAY_D, capsize=2, label=lab,
                  hatch=hatch, edgecolor="white" if hatch is None
                  else C_GRAY_D)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(FIG9B_NAMES, rotation=25, ha="right")
    ax[1].set_ylabel("KL to true attention (median)")
    ax[1].set_title("Equal mass removed (true attention)")
    ax[1].legend()
    ax[1].grid(True, alpha=0.3, axis="y")
    savefig_clean(fig, "v2_fig9_editability.png")
    record("v2_fig9_editability.png", "(b) grouped bars",
           [{"series": "median KL, %s, %s" % (m, a), "file": P7_V3,
             "field": "models.%s.contexts.identity.arms.%s.kl_true.median"
                      % (m, a)} for m in FIG9B_MODELS
            for a, _, _, _ in beta_arms]
           + [{"series": "95 percent CI of median KL, %s, %s" % (m, a),
               "file": P7_V3,
               "field": "models.%s.contexts.identity.arms.%s.kl_true."
                        "median_ci_document_bootstrap" % (m, a)}
              for m in FIG9B_MODELS for a, _, _, _ in beta_arms])
    note("Fig9b hatch marks beta 0.25; solid bars are beta 0; "
         "pink is sink, gray is mass matched control")


def fig11():
    panel = "11a"
    d8 = load_json(P8_ITEMS)
    try:
        gm = d8["models"]["gpt2-medium"]
        bypos = gm["by_position"]
    except KeyError:
        fail(panel, "missing models.gpt2-medium.by_position in %s" % P8_ITEMS)
    pos = sorted([int(p) for p in bypos.keys()])
    if not pos:
        fail(panel, "empty by_position in %s" % P8_ITEMS)
    ident, sink = [], []
    for p in pos:
        b = bypos[str(p)]
        if "baseline_accuracy" not in b or "edited_accuracy" not in b:
            fail(panel, "missing baseline_accuracy or edited_accuracy "
                 "at position %d" % p)
        ident.append(float(b["baseline_accuracy"]))
        sink.append(float(b["edited_accuracy"]))
    if "n" not in gm:
        fail(panel, "missing n in models.gpt2-medium")
    n = int(gm["n"])
    fig, ax = plt.subplots(1, 2, figsize=(6.8, 3.1))
    ax[0].axvspan(0.25 * n, 0.75 * n, color=C_GRAY, alpha=0.18)
    ax[0].plot(pos, ident, color=C_IDENT, marker="o", markersize=3,
               linewidth=1.6, label="Identity")
    ax[0].plot(pos, sink, color=C_SINK, marker="s", markersize=3,
               linewidth=1.6, label="Sink beta 0.25")
    ax[0].set_xlabel("Needle position")
    ax[0].set_ylabel("Accuracy")
    ax[0].set_title("(a) GPT-2-medium accuracy by position")
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)
    record("v2_fig11_taskgain.png", "(a) accuracy lines",
           [{"series": "identity accuracy at position %d" % p,
             "file": P8_ITEMS,
             "field": "models.gpt2-medium.by_position.%d."
                      "baseline_accuracy" % p} for p in pos]
           + [{"series": "sink beta 0.25 accuracy at position %d" % p,
               "file": P8_ITEMS,
               "field": "models.gpt2-medium.by_position.%d."
                        "edited_accuracy" % p} for p in pos]
           + [{"series": "middle window shade", "file": P8_ITEMS,
               "field": "models.gpt2-medium.middle_rule "
                        "(0.25n to 0.75n)"}])
    note("Fig11a has no error bars: %s stores no per position accuracy CI, "
         "only seed gain CIs" % P8_ITEMS)

    panel = "11b"
    try:
        mm = load_json(P8_MM)["models"]
    except KeyError:
        fail(panel, "missing models in %s" % P8_MM)
    unc, unlo, unhi, lim, lilo, lihi, ctl, ctlo, cthi = \
        ([] for _ in range(9))
    for model in P8_MODELS:
        try:
            mid = d8["models"][model]["middle"]
        except KeyError:
            fail(panel, "missing models.%s.middle in %s" % (model, P8_ITEMS))
        g, lo, hi = gain_pp(mid, panel, P8_ITEMS + ".models." + model)
        unc.append(g)
        unlo.append(lo)
        unhi.append(hi)
        try:
            smo = mm[model]
            sm = smo["sink_minus_identity"]
            cm = smo["control_minus_identity"]
        except KeyError:
            fail(panel, "missing sink_minus_identity or "
                 "control_minus_identity for %s" % model)
        g, lo, hi = gain_pp(sm, panel, P8_MM + ".models." + model)
        lim.append(g)
        lilo.append(lo)
        lihi.append(hi)
        g, lo, hi = gain_pp(cm, panel, P8_MM + ".models." + model)
        ctl.append(g)
        ctlo.append(lo)
        cthi.append(hi)
    x = np.arange(len(P8_MODELS))
    w = 0.24
    triples = [(unc, unlo, unhi, C_SINK, None, "Sink uncapped"),
               (lim, lilo, lihi, C_SINK, "///", "Sink mass limited"),
               (ctl, ctlo, cthi, C_CTRL, None, "Control mass matched")]
    for i, (med, lo, hi, col, hatch, lab) in enumerate(triples):
        ax[1].bar(x + (i - 1) * w, med, w,
                  yerr=[np.array(med) - np.array(lo),
                        np.array(hi) - np.array(med)],
                  color=col, ecolor=C_GRAY_D, capsize=2, label=lab,
                  hatch=hatch,
                  edgecolor="white" if hatch is None else C_GRAY_D)
    ax[1].axhline(0.0, color=C_IDENT, lw=1.0)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(P8_NAMES, rotation=25, ha="right")
    ax[1].set_ylabel("Middle window gain (pp)")
    ax[1].set_title("(b) Middle window gain by arm")
    ax[1].legend()
    ax[1].grid(True, alpha=0.3, axis="y")
    savefig_clean(fig, "v2_fig11_taskgain.png")
    record("v2_fig11_taskgain.png", "(b) grouped bars",
           [{"series": "uncapped sink gain, %s" % m, "file": P8_ITEMS,
             "field": "models.%s.middle.median_seed_accuracy_gain (x100)"
                      % m} for m in P8_MODELS]
           + [{"series": "uncapped sink gain CI, %s" % m, "file": P8_ITEMS,
               "field": "models.%s.middle.median_seed_gain_ci95_item_"
                        "bootstrap (x100)" % m} for m in P8_MODELS]
           + [{"series": "mass limited sink gain, %s" % m, "file": P8_MM,
               "field": "models.%s.sink_minus_identity."
                        "median_seed_accuracy_gain (x100)" % m}
              for m in P8_MODELS]
           + [{"series": "mass matched control gain, %s" % m, "file": P8_MM,
               "field": "models.%s.control_minus_identity."
                        "median_seed_accuracy_gain (x100)" % m}
              for m in P8_MODELS]
           + [{"series": "gain CI of limited arms, %s" % m, "file": P8_MM,
               "field": "models.%s.{sink,control}_minus_identity."
                        "median_seed_gain_ci95_item_bootstrap (x100)" % m}
              for m in P8_MODELS])
    note("Fig11b hatch marks the mass limited sink; solid pink is the "
         "uncapped sink, gray is the mass matched control")


def fig12():
    panel = "12"
    kv_models = ["gpt2-medium", "Qwen/Qwen2.5-3B"]
    kv_names = ["GPT-2-medium", "Qwen2.5-3B"]
    d11 = load_json(P11_ITEMS)
    try:
        mm = load_json(P11_MM)["models"]
    except KeyError:
        fail(panel, "missing models in %s" % P11_MM)
    unc, unlo, unhi, lim, lilo, lihi, ctl, ctlo, cthi = \
        ([] for _ in range(9))
    for model in kv_models:
        try:
            mid = d11["models"][model]["middle"]
        except KeyError:
            fail(panel, "missing models.%s.middle in %s" % (model, P11_ITEMS))
        g, lo, hi = gain_pp(mid, panel, P11_ITEMS + ".models." + model)
        unc.append(g)
        unlo.append(lo)
        unhi.append(hi)
        try:
            smo = mm[model]
            sm = smo["sink_minus_identity"]
            cm = smo["control_minus_identity"]
        except KeyError:
            fail(panel, "missing sink_minus_identity or "
                 "control_minus_identity for %s" % model)
        g, lo, hi = gain_pp(sm, panel, P11_MM + ".models." + model)
        lim.append(g)
        lilo.append(lo)
        lihi.append(hi)
        g, lo, hi = gain_pp(cm, panel, P11_MM + ".models." + model)
        ctl.append(g)
        ctlo.append(lo)
        cthi.append(hi)
    # Constrained layout reserves space for the legend below the axes;
    # savefig_clean skips tight_layout for constrained figures.
    fig, axi = plt.subplots(figsize=(3.3, 3.4), layout="constrained")
    x = np.arange(len(kv_models))
    w = 0.24
    triples = [(unc, unlo, unhi, C_SINK, None, "Sink uncapped"),
               (lim, lilo, lihi, C_SINK, "///", "Sink mass limited"),
               (ctl, ctlo, cthi, C_CTRL, None, "Control mass matched")]
    for i, (med, lo, hi, col, hatch, lab) in enumerate(triples):
        axi.bar(x + (i - 1) * w, med, w,
                yerr=[np.array(med) - np.array(lo),
                      np.array(hi) - np.array(med)],
                color=col, ecolor=C_GRAY_D, capsize=2, label=lab,
                hatch=hatch,
                edgecolor="white" if hatch is None else C_GRAY_D)
    axi.axhline(0.0, color=C_IDENT, lw=1.0)
    axi.set_xticks(x)
    axi.set_xticklabels(kv_names, rotation=25, ha="right")
    axi.set_ylabel("Middle window gain (pp)")
    axi.set_title("KV 256 gain by arm")
    handles, labels = axi.get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncol=2)
    axi.grid(True, alpha=0.3, axis="y")
    savefig_clean(fig, "v2_fig12_kv.png")
    record("v2_fig12_kv.png", "grouped bars",
           [{"series": "uncapped sink gain, %s" % m, "file": P11_ITEMS,
             "field": "models.%s.middle.median_seed_accuracy_gain (x100)"
                      % m} for m in kv_models]
           + [{"series": "uncapped sink gain CI, %s" % m, "file": P11_ITEMS,
               "field": "models.%s.middle.median_seed_gain_ci95_item_"
                        "bootstrap (x100)" % m} for m in kv_models]
           + [{"series": "mass limited sink gain, %s" % m, "file": P11_MM,
               "field": "models.%s.sink_minus_identity."
                        "median_seed_accuracy_gain (x100)" % m}
              for m in kv_models]
           + [{"series": "mass matched control gain, %s" % m, "file": P11_MM,
               "field": "models.%s.control_minus_identity."
                        "median_seed_accuracy_gain (x100)" % m}
              for m in kv_models]
           + [{"series": "gain CI of limited arms, %s" % m, "file": P11_MM,
               "field": "models.%s.{sink,control}_minus_identity."
                        "median_seed_gain_ci95_item_bootstrap (x100)" % m}
              for m in kv_models])


def main():
    made = []
    fig1()
    made.append("v2_fig1_concentration.png")
    f2, gs2, _ = fig2()
    fig2_example(f2, gs2)
    savefig_clean(f2, "v2_fig2_reconstruction.png")
    made.append("v2_fig2_reconstruction.png")
    fig5()
    made.append("v2_fig5_multimodel.png")
    fig6()
    made.append("v2_fig6_downstream.png")
    fig8()
    made.append("v2_fig8_anova.png")
    fig10()
    made.append("v2_fig10_named.png")
    fig4()
    made.append("v2_fig4_examples.png")
    fig9()
    made.append("v2_fig9_editability.png")
    fig11()
    made.append("v2_fig11_taskgain.png")
    fig12()
    made.append("v2_fig12_kv.png")
    SOURCES["figures"]["v2_fig2_reconstruction.png"]["(c) recon check"] = \
        [dict({"series": "recomputed vs stored relative error, tol 1e-9"},
              **RECON_CHECK)]
    with open(os.path.join(OUT, "v2_figures_sources.json"), "w",
              encoding="utf-8") as f:
        json.dump(SOURCES, f, indent=1)
    print("Wrote:")
    for m in made:
        print("  paper/figs/" + m)
    print("  paper/figs/v2_figures_sources.json")
    print("Recon check: match=%s instance=%s profiled_diff=%.3g svd_diff=%.3g"
          % (RECON_CHECK.get("match"), RECON_CHECK.get("instance_id"),
             RECON_CHECK.get("abs_diff_profiled", float("nan")),
             RECON_CHECK.get("abs_diff_svd", float("nan"))))


if __name__ == "__main__":
    main()

