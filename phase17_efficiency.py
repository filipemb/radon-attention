"""
Phase 17 (NN revision) — efficiency / rate-distortion of the representations.

Reviewers asked for an efficiency comparison whenever low-rank/compression is
discussed. This quantifies, on real attention matrices, the storage cost (number
of parameters to represent an n x n matrix) against reconstruction fidelity for:
  - rank-k truncated SVD           params = k * (2n + 1)
  - profiled line dictionary (OMP) params = 2k  (atom id + coefficient)
  - two-channel S+L (sRPCA)        params = 2 * n_active + r * (2n + 1)
                                   (r=0 = named channel only, to isolate its standalone fidelity)

Integrity fixes (after adversarial audit): the line dictionary is given a FAIR,
large budget (k up to 128, i.e. up to 256 params) so "lines plateau" is tested
well past the low-rank budgets, not capped at 64; per-model reached fractions are
reported with bootstrap CIs (no cross-model cherry-picking); and the named channel
alone (r=0) is reported so its standalone contribution is visible rather than
hidden behind an embedded low-rank term. In-sample reconstruction measurement
(no learned model, no generalization claim).

Reports (a) a rate-distortion curve, (b) a matched-fidelity table (parameters each
method needs to reach a target error, with reached fraction + CI), and (c) the
apply-cost ratio of a rank-k attention (the A@V product) vs dense: O(2 n k d) vs
O(n^2 d), i.e. 2k/n. Runs on the RTX 3060 in minutes. No training.
"""
import argparse, json, os
import numpy as np
import torch

from phase0_radon_attention import load_sequences, extract_attention
from phase06_profiled_lines import omp_profiled, precompute_band_norms
from phase5_msclean import build_dict
from phase6_srpca import srpca
from phase_stats import summ


def svd_error_all_k(A, ks):
    s = np.linalg.svd(A, compute_uv=False)
    e2 = s ** 2
    tot = e2.sum() + 1e-12
    tail = np.concatenate([np.cumsum(e2[::-1])[::-1][1:], [0.0]])  # tail[k] = sum_{i>k} s_i^2
    return {k: float(np.sqrt(max(tail[k - 1], 0.0) / tot)) for k in ks if k <= len(s)}


def smallest_params_to_target(err_by_params, target):
    for p in sorted(err_by_params):
        if err_by_params[p] is not None and err_by_params[p] <= target:
            return p
    return None


def feas(lst, seed=0, n_boot=2000):
    """Reached fraction + bootstrap CI, and median params among reached."""
    arr = np.array([1.0 if p is not None else 0.0 for p in lst])
    ok = [p for p in lst if p is not None]
    ci = [None, None]
    if arr.size >= 2:
        rng = np.random.default_rng(seed)
        bs = arr[rng.integers(0, arr.size, size=(n_boot, arr.size))].mean(axis=1)
        ci = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    return {"reached_frac": float(arr.mean()), "reached_frac_ci": ci,
            "median_params": float(np.median(ok)) if ok else None, "n": int(arr.size)}


def run_model(name, args, band_norms, D, ks, line_ks, rs, targets, device, rng):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    n = args.seq_len
    P_lr = 2 * n + 1
    tok = AutoTokenizer.from_pretrained(name)
    dtype = torch.bfloat16 if "Qwen2.5-3B" in name else torch.float32
    model = AutoModelForCausalLM.from_pretrained(name, attn_implementation="eager", dtype=dtype).to(device).eval()
    ids = load_sequences(tok, args.n_seq, n, args.seed)
    attn = extract_attention(model, ids, args.batch, device)
    attn = [np.nan_to_num(a) for a in attn]
    n_layers, n_heads = len(attn), attn[0].shape[1]
    del model
    if device == "cuda":
        torch.cuda.empty_cache()

    inst = [(int(rng.integers(n_layers)), int(rng.integers(n_heads)), int(rng.integers(attn[0].shape[0])))
            for _ in range(args.n_instances)]

    svd_pts = {k: [] for k in ks}
    line_pts = {k: [] for k in line_ks}
    tc_err = {r: [] for r in rs}
    tc_params = {r: [] for r in rs}
    need = {meth: {t: [] for t in targets} for meth in ("svd", "line", "twochannel")}

    for (li, hi, si) in inst:
        A = attn[li][si, hi].astype(np.float64)
        se = svd_error_all_k(A, ks)
        le, _ = omp_profiled(A, max(line_ks), n, set(line_ks), band_norms)
        for k in ks:
            if k in se:
                svd_pts[k].append(se[k])
        for k in line_ks:
            line_pts[k].append(le[k])
        tc_by_params = {}
        for r in rs:
            err, nf, nact, _ = srpca(A, D, r, iters=args.iters)
            params = 2 * nact + r * P_lr
            tc_err[r].append(err); tc_params[r].append(params)
            tc_by_params[params] = err
        svd_by_params = {k * P_lr: se.get(k) for k in ks}
        line_by_params = {2 * k: le[k] for k in line_ks}
        for t in targets:
            need["svd"][t].append(smallest_params_to_target(svd_by_params, t))
            need["line"][t].append(smallest_params_to_target(line_by_params, t))
            need["twochannel"][t].append(smallest_params_to_target(tc_by_params, t))

    return {
        "n_layers": n_layers, "n_heads": n_heads, "n_instances": len(inst),
        "param_cost_model": {"svd_per_rank": P_lr, "line_per_atom": 2, "lowrank_per_rank": P_lr,
                             "line_max_atoms": max(line_ks), "line_max_params": 2 * max(line_ks)},
        "rate_distortion": {
            "svd": {k: {"params": k * P_lr, **summ(svd_pts[k])} for k in ks if svd_pts[k]},
            "line": {k: {"params": 2 * k, **summ(line_pts[k])} for k in line_ks},
            "twochannel": {r: {"label": ("named_only" if r == 0 else f"named+rank{r}"),
                               "err": summ(tc_err[r]), "params": summ(tc_params[r])} for r in rs},
        },
        "matched_fidelity": {meth: {str(t): feas(need[meth][t]) for t in targets} for meth in need},
        "apply_flops_ratio_vs_dense": {k: round(2 * k / n, 4) for k in ks},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gpt2", "gpt2-medium", "EleutherAI/pythia-410m", "Qwen/Qwen2.5-0.5B"])
    ap.add_argument("--seq_len", type=int, default=128)
    ap.add_argument("--n_seq", type=int, default=100)
    ap.add_argument("--n_instances", type=int, default=200)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--iters", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    n = args.seq_len
    band_norms = precompute_band_norms(n)
    D, _ = build_dict(n)
    ks = [1, 2, 4, 8, 16, 32]
    line_ks = [1, 2, 4, 8, 16, 32, 64, 128]   # fair, large budget for lines (up to 256 params)
    rs = [0, 4, 8, 16]                          # r=0 = named channel only
    targets = [0.40, 0.30, 0.25, 0.20, 0.15, 0.10]

    results = {"_meta": {"seq_len": n, "n_instances": args.n_instances, "targets": targets,
                         "ks": ks, "line_ks": line_ks, "rs": rs, "seed": args.seed}}
    for name in args.models:
        print(f"\n===== {name} =====", flush=True)
        try:
            r = run_model(name, args, band_norms, D, ks, line_ks, rs, targets, device, rng)
        except Exception as e:
            import traceback; traceback.print_exc()
            results[name] = {"error": f"{type(e).__name__}: {e}"}
            json.dump(results, open(os.path.join(args.out, "phase17_efficiency.json"), "w"), indent=2)
            continue
        results[name] = r
        json.dump(results, open(os.path.join(args.out, "phase17_efficiency.json"), "w"), indent=2)
        rd = r["rate_distortion"]
        print("  line plateau (median err at k=8/32/64/128):",
              {k: round(rd['line'][k]['median'], 3) for k in [8, 32, 64, 128]}, flush=True)
        print("  named-only (r=0) median err / params:",
              round(rd['twochannel'][0]['err']['median'], 3), int(rd['twochannel'][0]['params']['median']), flush=True)
        mf = r["matched_fidelity"]
        for t in ["0.2", "0.15"]:
            s, l, c = mf["svd"][t], mf["line"][t], mf["twochannel"][t]
            print(f"    err<={t}: SVD {s['median_params']}p {s['reached_frac']:.0%}{s['reached_frac_ci']} | "
                  f"line {l['median_params']}p {l['reached_frac']:.0%}{l['reached_frac_ci']} | "
                  f"2ch {c['median_params']}p {c['reached_frac']:.0%}", flush=True)
    print(f"\n[json] {os.path.abspath(os.path.join(args.out, 'phase17_efficiency.json'))}")


if __name__ == "__main__":
    main()
