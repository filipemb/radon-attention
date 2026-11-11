"""P0 V3 alternating NNLS + low-rank decomposition on frozen V2 matrices.

The original five block-coordinate iterations are retained. An optional QR
reduction solves the identical NNLS objective with a smaller design matrix;
its equivalence is checked against the original dense fit before measurement.
"""
from sampling import MODELS
import time
import numpy as np
from scipy.optimize import nnls
from phase5_msclean import build_dict, fraction_metrics


def prepare_nnls(D):
    return np.linalg.qr(D, mode="reduced")


def srpca(A, D, r, iters=5, qr=None, return_components=False, timings=None):
    n = A.shape[0]
    b = A.ravel()
    normA = np.linalg.norm(b)
    if normA <= 0 or not np.isfinite(A).all():
        raise ValueError("Invalid reference matrix")
    L = np.zeros((n, n))
    coef = np.zeros(D.shape[1])
    trace = []
    for iteration in range(iters):
        started = time.perf_counter()
        target = b-L.ravel()
        coef, _ = nnls(D, target) if qr is None else nnls(qr[1], qr[0].T @ target)
        S = (D@coef).reshape(n, n)
        nnls_seconds = time.perf_counter()-started
        started = time.perf_counter()
        residual = A-S
        if r > 0:
            u, s, vh = np.linalg.svd(residual, full_matrices=False)
            L = (u[:, :r]*s[:r])@vh[:r]
        else:
            L = np.zeros_like(A)
        svd_seconds = time.perf_counter()-started
        objective = float(np.sum((A-S-L)**2)/(normA*normA))
        previous = trace[-1] if trace else 1.0
        if objective > previous + 1e-9:
            raise RuntimeError(f"Alternating objective increased: {previous} -> {objective}")
        trace.append(objective)
        if timings is not None:
            timings.append({"iteration": iteration, "nnls_seconds": nnls_seconds, "svd_seconds": svd_seconds})
    err = float(np.sqrt(trace[-1]))
    named_frac = float(np.linalg.norm(S)/normA)
    n_active = int((coef > 1e-4*(coef.max()+1e-12)).sum())
    result = (err, named_frac, n_active, coef)
    return (*result, S, L, trace) if return_components else result

def svd_err(A, k):
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    Ak = (U[:, :k] * s[:k]) @ Vt[:k]
    return float(np.linalg.norm(A - Ak) / (np.linalg.norm(A) + 1e-12))



def main():
    from phase26_p0_named import main as offline_main
    offline_main(default_methods=["srpca"])

if __name__ == "__main__":
    main()
