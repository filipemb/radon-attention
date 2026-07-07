"""
Dispersion helpers shared across phases (added for the Neural Networks revision).

The original phases reduced per-(sequence, layer, head) populations to a single
median before saving. Reviewers asked for dispersion. summ() returns the median
plus IQR (p25/p75), mean/std and the population size n; median_ci_bootstrap()
returns a deterministic bootstrap confidence interval of the median. Both are
distribution free and reproducible (fixed seed), so re-running a phase yields the
same intervals.
"""
import numpy as np


def summ(values):
    """Summary of a 1D population: median, IQR, mean, std, n. NaN/inf are dropped."""
    a = np.asarray(values, dtype=np.float64)
    a = a[np.isfinite(a)]
    if a.size == 0:
        return {"median": None, "p25": None, "p75": None, "mean": None, "std": None, "n": 0}
    return {
        "median": float(np.median(a)),
        "p25": float(np.percentile(a, 25)),
        "p75": float(np.percentile(a, 75)),
        "mean": float(np.mean(a)),
        "std": float(np.std(a, ddof=1)) if a.size > 1 else 0.0,
        "n": int(a.size),
    }


def median_ci_bootstrap(values, n_boot=2000, seed=0, alpha=0.05):
    """Deterministic bootstrap CI of the median (fixed seed -> reproducible)."""
    a = np.asarray(values, dtype=np.float64)
    a = a[np.isfinite(a)]
    if a.size < 2:
        return {"lo": None, "hi": None, "n_boot": int(n_boot)}
    rng = np.random.default_rng(seed)
    meds = np.median(rng.choice(a, size=(n_boot, a.size), replace=True), axis=1)
    return {
        "lo": float(np.percentile(meds, 100 * alpha / 2)),
        "hi": float(np.percentile(meds, 100 * (1 - alpha / 2))),
        "n_boot": int(n_boot),
    }
