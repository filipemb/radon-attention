"""
A1 — estatistica rigorosa da intervencao (pedido dos dois revisores).

Le os arquivos VERSIONADOS phase8_lostmiddle_s{0,1,2}.json e phase11_kv_s{0,1,2}.json,
agrega sementes, e calcula:

  - janela "meio" definida UMA vez: posicoes p com 0.25*L <= p <= 0.75*L
    (L = seq_len; probe L=128 -> {32,48,64,80,96}; KV L=256 -> {96,144,192})
  - ganho beta=0.25 vs baseline no meio, agregado sobre sementes
  - teste z de duas proporcoes (pooled) por modelo
  - correcao de Holm-Bonferroni entre os M modelos testados
  - ganhos por semente (replicabilidade)

Saida: out/phase13_stats.json + tabela impressa. Este script E o agregador
canonico citado no paper (define a janela e o n).
"""
import json
import os
import glob
import numpy as np
from scipy.stats import norm


def mid_positions(positions, L):
    return [p for p in positions if 0.25 * L <= p <= 0.75 * L]


def pooled_z(acc1, acc0, n1, n0):
    """z de duas proporcoes (pooled). acc = proporcao, n = tentativas."""
    x1, x0 = acc1 * n1, acc0 * n0
    p = (x1 + x0) / (n1 + n0)
    se = np.sqrt(p * (1 - p) * (1 / n1 + 1 / n0))
    if se == 0:
        return 0.0
    return float((acc1 - acc0) / se)


def holm(pvals):
    """Correcao de Holm. Retorna p ajustados na ordem original."""
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * pvals[idx]
        running = max(running, val)
        adj[idx] = min(1.0, running)
    return adj.tolist()


def analyze(pattern, L, label, beta_key="0.25"):
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"[{label}] nenhum arquivo: {pattern}")
        return None
    per_model = {}
    n_per_pos_per_seed = {}
    for f in files:
        d = json.load(open(f))
        meta = d.get("_meta", {})
        npp = meta.get("n_per_pos", 200)
        for m, r in d.items():
            if m.startswith("_") or "error" in r:
                continue
            pos = r["positions"]
            mids = mid_positions(pos, L)
            acc = r.get("acc", r)  # phase8 tem r["acc"], phase11 tem direto
            base = np.mean([acc["1.0"][str(p)] for p in mids])
            cal = np.mean([acc[beta_key][str(p)] for p in mids])
            per_model.setdefault(m, []).append((base, cal, npp * len(mids)))
            n_per_pos_per_seed[m] = npp
    out = {}
    models = sorted(per_model)
    zs, ps = [], []
    for m in models:
        rows = per_model[m]
        n_tot = sum(n for (_, _, n) in rows)
        base = sum(b * n for (b, _, n) in rows) / n_tot
        cal = sum(c * n for (_, c, n) in rows) / n_tot
        z = pooled_z(cal, base, n_tot, n_tot)
        p = 2 * (1 - norm.cdf(abs(z)))
        zs.append(z); ps.append(p)
        out[m] = {
            "baseline_mid": base, "calibrated_mid": cal,
            "gain_pp": (cal - base) * 100, "n_per_arm": n_tot,
            "z": z, "p_raw": p,
            "per_seed_gains_pp": [(c - b) * 100 for (b, c, _) in rows],
        }
    padj = holm(ps)
    for i, m in enumerate(models):
        out[m]["p_holm"] = padj[i]
        out[m]["significant_holm05"] = bool(padj[i] < 0.05)
    return {"label": label, "mid_window_rule": "0.25*L <= p <= 0.75*L",
            "L": L, "models": out, "n_files": len(files)}


def main():
    res = {}
    probe = analyze("out/phase8_lostmiddle_s*.json", 128, "probe")
    kv = analyze("out/phase11_kv_s*.json", 256, "kv")
    if probe:
        res["probe"] = probe
    if kv:
        res["kv"] = kv
    json.dump(res, open("out/phase13_stats.json", "w"), indent=2)

    for key in res:
        r = res[key]
        print(f"\n=== {r['label'].upper()} (meio: {r['mid_window_rule']}, L={r['L']}, {r['n_files']} sementes) ===")
        print(f"{'modelo':>24} | {'base':>6} | {'calib':>6} | {'ganho':>7} | {'n/arm':>6} | {'z':>5} | {'p(Holm)':>8} | sig | por semente")
        for m, d in r["models"].items():
            seeds = "/".join(f"{g:+.1f}" for g in d["per_seed_gains_pp"])
            print(f"{m[-24:]:>24} | {d['baseline_mid']:.3f} | {d['calibrated_mid']:.3f} | {d['gain_pp']:+6.1f}pp | {d['n_per_arm']:>6} | {d['z']:5.1f} | {d['p_holm']:8.2e} | {'SIM' if d['significant_holm05'] else 'nao'} | {seeds}")
    print("\n[json] out/phase13_stats.json")


if __name__ == "__main__":
    main()
