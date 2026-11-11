"""Sparse digital-line synthesis and nonnegative Radon inversion for E2.

Only causal pixels are variables. A normal angle theta and integer offset rho
define the strip round(j*cos(theta) + i*sin(theta)) == rho. Each pixel belongs
to exactly one strip per angle. No attention extractor is imported.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
from scipy import linalg, sparse
from scipy.optimize import minimize
from scipy.sparse.linalg import LinearOperator, eigsh, lsmr
from skimage.transform import iradon, radon


SEED = 19027
COMPONENTS = (1, 2, 4, 8, 16, 32)
PROFILES = (0.0, 1.0, -1.0, 4.0, -4.0)


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    """Exclusive creation prevents overwriting any existing experiment JSON."""
    with open(path, "x", encoding="utf-8") as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write("\n")


def progress(message):
    path = Path("out/_rerun_logs/e2_progress.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(f"- {time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    print(message, flush=True)


def grids(n):
    # Three complete ranks, including the rank-one regime. Larger component
    # counts are afforded to lines by the same storage constraint.
    return [2 * n + 1, 2 * (2 * n + 1), 4 * (2 * n + 1)]


def counts(n):
    budgets = grids(n)
    return {
        "uniform": sorted(set(COMPONENTS) | {b // 2 for b in budgets}),
        "profiled": sorted(set(COMPONENTS) | {b // 3 for b in budgets}),
        "parametric": sorted(set(COMPONENTS) | {b // 5 for b in budgets}),
        "radon": sorted(set(COMPONENTS) | {b // 2 for b in budgets}),
        "svd": sorted(set(COMPONENTS) | {b // (2 * n + 1) for b in budgets}),
    }


class LineDictionary:
    def __init__(self, n, angles=180, profiles=(0.0,)):
        self.n = n
        self.angles = angles
        self.profiles = tuple(profiles)
        self.i, self.j = np.tril_indices(n)
        self.p = len(self.i)
        self.theta = np.arange(angles, dtype=float) * (np.pi / angles)
        row_blocks, value_blocks = [], []
        angle_ids, offsets, profile_ids = [], [], []
        base = 0
        for ai, theta in enumerate(self.theta):
            q = self.j * np.cos(theta) + self.i * np.sin(theta)
            bins = np.floor(q + 0.5).astype(np.int32)
            lo, hi = int(bins.min()), int(bins.max())
            ids = bins - lo
            m = hi - lo + 1
            t = (-self.j * np.sin(theta) + self.i * np.cos(theta)) / n
            for profile_id, decay in enumerate(profiles):
                # Subtract the extremum on each strip before exponentiation.
                # Positive/negative decay covers both longitudinal directions.
                v = -decay * t
                maxima = np.full(m, -np.inf)
                np.maximum.at(maxima, ids, v)
                v = np.exp(v - maxima[ids])
                norms = np.bincount(ids, weights=v * v, minlength=m) ** 0.5
                values = v / norms[ids]
                row_blocks.append(ids + base)
                value_blocks.append(values)
                angle_ids.extend([ai] * m)
                offsets.extend(range(lo, hi + 1))
                profile_ids.extend([profile_id] * m)
                base += m
        rows = np.concatenate(row_blocks)
        cols = np.tile(np.arange(self.p, dtype=np.int32), angles * len(profiles))
        self.D = sparse.csr_matrix((np.concatenate(value_blocks), (rows, cols)),
                                   shape=(base, self.p))
        # Empty strips would have zero norm and are not useful atoms.
        nonempty = np.diff(self.D.indptr) != 0
        self.angle_id = np.asarray(angle_ids, dtype=np.int16)[nonempty]
        self.offset = np.asarray(offsets, dtype=np.int32)[nonempty]
        self.profile_id = np.asarray(profile_ids, dtype=np.int8)[nonempty]
        self.D = self.D[nonempty].tocsr()
        self.meta = {"n": n, "normal_angles": angles, "angle_step_degrees": 180 / angles,
                     "angle_interval": "[0, pi)", "offset_step_pixels": 1,
                     "strip_rule": "floor(j*cos(theta)+i*sin(theta)+0.5)==rho",
                     "causal_pixels": self.p, "n_atoms": self.D.shape[0],
                     "nonzeros": self.D.nnz, "decay_rates_per_n_pixels": list(profiles),
                     "normalization": "unit Frobenius norm after causal restriction"}

    def atom(self, index):
        return self.D.getrow(int(index)).toarray().ravel()

    def parameters(self, indices, coefs):
        indices = np.asarray(indices, dtype=int)
        return np.stack([self.theta[self.angle_id[indices]], self.offset[indices],
                         np.full(len(indices), 0.42),
                         np.asarray(self.profiles)[self.profile_id[indices]],
                         coefs], axis=1)


def _nnls_warm(G, h, x, tol=1e-10):
    """Lawson-Hanson on a Gram matrix, with a feasible warm start.

    The quadratic is x'Gx/2 - h'x, not ||Gx-h||^2. The latter would be an
    incorrect NNLS refit. A least-squares fallback handles duplicate atoms.
    """
    x = np.maximum(x, 0.0)
    passive = x > tol
    iterations = 0
    for _ in range(6 * len(h) + 20):
        grad = h - G @ x
        inactive = np.flatnonzero(~passive)
        if not len(inactive) or grad[inactive].max() <= tol:
            return x, iterations
        passive[inactive[np.argmax(grad[inactive])]] = True
        while True:
            ids = np.flatnonzero(passive)
            sub = G[np.ix_(ids, ids)]
            # Rank-revealing least squares is robust for highly coherent strips.
            z = np.zeros_like(x)
            z[ids] = linalg.lstsq(sub, h[ids], cond=1e-11,
                                 lapack_driver="gelsy", check_finite=False)[0]
            iterations += 1
            if np.all(z[ids] > tol):
                x = z
                break
            bad = ids[z[ids] <= tol]
            den = x[bad] - z[bad]
            valid = den > 0
            alpha = min(1.0, float(np.min(x[bad][valid] / den[valid]))) if valid.any() else 0.0
            x += alpha * (z - x)
            drop = passive & (x <= tol)
            x[drop] = 0
            passive[drop] = False
    raise RuntimeError("NNLS active-set refit did not converge")


class NNLSActive:
    """Incremental Cholesky NNLS; repeated OMP refits cost O(k^2) normally."""
    def __init__(self, tol=1e-10):
        self.ids = []
        self.L = np.empty((0, 0))
        self.tol = tol

    def refit(self, G, h, x):
        x = np.maximum(x, 0)
        iterations = 0
        for _ in range(6*len(h)+20):
            grad = h-G@x
            available = np.ones(len(h), dtype=bool)
            available[self.ids] = False
            outside = np.flatnonzero(available)
            if not len(outside) or grad[outside].max() <= self.tol:
                return x, iterations
            new = int(outside[np.argmax(grad[outside])])
            if self.L is not None:
                v = linalg.solve_triangular(self.L, G[self.ids, new], lower=True,
                                            check_finite=False) if self.ids else np.empty(0)
                diagonal = float(G[new,new]-v@v)
                if diagonal > 1e-11:
                    m = len(self.ids)
                    Lnew = np.zeros((m+1,m+1))
                    Lnew[:m,:m] = self.L
                    Lnew[m,:m] = v
                    Lnew[m,m] = np.sqrt(diagonal)
                    self.L = Lnew
                else:
                    self.L = None
            self.ids.append(new)
            while True:
                z = np.zeros_like(x)
                if self.L is not None:
                    z[self.ids] = linalg.cho_solve((self.L,True), h[self.ids], check_finite=False)
                else:
                    z[self.ids] = linalg.lstsq(G[np.ix_(self.ids,self.ids)],h[self.ids],
                                               cond=1e-11,lapack_driver="gelsy",check_finite=False)[0]
                iterations += 1
                ids = np.asarray(self.ids)
                if np.all(z[ids] > self.tol):
                    x = z
                    break
                bad = ids[z[ids] <= self.tol]
                den = x[bad]-z[bad]
                valid = den > 0
                alpha = min(1.0,float(np.min(x[bad][valid]/den[valid]))) if valid.any() else 0.0
                x += alpha*(z-x)
                drop = ids[x[ids] <= self.tol]
                x[drop] = 0
                self.ids = [int(i) for i in ids if i not in set(drop)]
                if self.L is not None:
                    self.L = linalg.cholesky(G[np.ix_(self.ids,self.ids)],lower=True,check_finite=False)
        raise RuntimeError("Incremental NNLS did not reach active-set KKT conditions")


def omp(b, dictionary, checkpoints, save_support=False):
    start = time.perf_counter()
    b = np.asarray(b, dtype=float)
    norm = float(np.linalg.norm(b))
    if not norm > 0 or not np.isfinite(b).all():
        raise ValueError("OMP requires finite nonzero data")
    target = b / norm
    D = dictionary.D
    h_all = np.asarray(D @ target)
    chosen, result = [], {}
    G = np.zeros((max(checkpoints), max(checkpoints)))
    x = np.empty(0)
    residual = target.copy()
    refit_iterations = 0
    nnls_state = NNLSActive()
    stopped = False
    for step in range(1, max(checkpoints) + 1):
        corr = np.asarray(D @ residual)
        corr[chosen] = -np.inf
        candidate = int(np.argmax(corr))
        if corr[candidate] <= 1e-10:
            stopped = True
            for k in checkpoints:
                if k >= step:
                    result[k] = {"relative": float(np.linalg.norm(residual)),
                                 "absolute": float(norm * np.linalg.norm(residual)),
                                 "selected": len(chosen), "active": int((x > 1e-9).sum()),
                                 "stationary": True}
                    if save_support:
                        result[k]["support"] = {"indices": chosen.copy(), "amplitudes": (x * norm).tolist()}
            break
        atom = dictionary.atom(candidate)
        if chosen:
            cross = np.asarray(D[chosen] @ atom)
            G[step - 1, :step - 1] = cross
            G[:step - 1, step - 1] = cross
        G[step - 1, step - 1] = atom @ atom
        chosen.append(candidate)
        x, nit = nnls_state.refit(G[:step, :step], h_all[chosen], np.r_[x, 0.0])
        refit_iterations += nit
        residual = target - np.asarray(D[chosen].T @ x).ravel()
        if step in checkpoints:
            r = float(np.linalg.norm(residual))
            grad = G[:step, :step] @ x - h_all[chosen]
            kkt = float(np.max(np.abs(np.minimum(grad, x))))
            result[step] = {"relative": r, "absolute": norm * r,
                            "selected": step, "active": int((x > 1e-9).sum()),
                            "active_nnls_kkt": kkt, "stationary": False}
            if save_support:
                result[step]["support"] = {"indices": chosen.copy(), "amplitudes": (x * norm).tolist()}
    return result, {"seconds": time.perf_counter() - start, "refit_iterations": refit_iterations,
                    "cone_stationary": stopped, "nnls_tolerance": 1e-10}


def make_radon(n):
    # An angular sample per image diameter, rounded to a multiple of 180.
    # The row/column count is checked and the extremal singular values measured.
    d = LineDictionary(n, angles=180 if n == 128 else 360)
    lengths = np.sqrt(np.diff(d.D.indptr))
    R = sparse.diags(lengths) @ d.D
    R = R.tocsr()
    return d, R


def radon_spectrum(R):
    p = R.shape[1]
    op = LinearOperator((p, p), matvec=lambda x: R.T @ (R @ x), dtype=float)
    v0 = np.random.default_rng(SEED).normal(size=p)
    top = eigsh(op, k=1, which="LA", tol=1e-4, v0=v0,
                maxiter=1500, return_eigenvectors=False)[0]
    bottom = eigsh(op, k=1, which="SA", tol=1e-3, v0=v0,
                   maxiter=3000, return_eigenvectors=False)[0]
    return {"shape": list(R.shape), "nonzeros": R.nnz, "unknowns": p,
            "overdetermination_ratio": R.shape[0] / p,
            "lambda_max_RtR": float(top), "lambda_min_RtR_estimate": float(bottom),
            "condition_2_estimate": float(np.sqrt(top / bottom)) if bottom > 0 else None,
            "rank_evidence": "positive smallest Ritz value; numerical estimate, not exact rank proof",
            "eigensolver_tolerances": {"largest": 1e-4, "smallest": 1e-3}}


def radon_decode_fista(b, R, checkpoints, lipschitz, tol=1e-6, maxiter=3000):
    """Batched projected accelerated gradient for nonnegative least squares.

    All columns minimize ||R x - s_k||^2/2. The full sinogram is also inverted
    from zero, without exposing b to the inverse. Projected KKT residuals,
    objective and stopping status are retained for every column.
    """
    start = time.perf_counter()
    norm = float(np.linalg.norm(b))
    sino = np.asarray(R @ (b / norm))
    order = np.argsort(-np.abs(sino), kind="stable")
    keys = list(checkpoints) + ["all"]
    S = np.zeros((R.shape[0], len(keys)))
    for col, k in enumerate(keys):
        ids = order if k == "all" else order[:k]
        S[ids, col] = sino[ids]
    H = np.asarray(R.T @ S)
    X = np.zeros_like(H)
    Y = X.copy()
    t = np.ones(len(keys))
    finished = np.zeros(len(keys), dtype=bool)
    iters = np.zeros(len(keys), dtype=int)
    scale = np.maximum(np.max(np.abs(H), axis=0), 1e-12)
    for iteration in range(1, maxiter + 1):
        grad = np.asarray(R.T @ (R @ Y)) - H
        Z = np.maximum(Y - grad / lipschitz, 0.0)
        # Gradient restart avoids oscillations at the active boundary.
        restart = np.sum((Y - Z) * (Z - X), axis=0) > 0
        tn = (1 + np.sqrt(1 + 4 * t * t)) / 2
        tn[restart] = 1.0
        Yn = Z + ((t - 1) / tn)[None, :] * (Z - X)
        Yn[:, restart] = Z[:, restart]
        X, Y, t = Z, Yn, tn
        if iteration % 10 == 0 or iteration == maxiter:
            g = np.asarray(R.T @ (R @ X)) - H
            kkt = np.max(np.abs(np.minimum(X * lipschitz, g)), axis=0) / scale
            newly = (~finished) & (kkt <= tol)
            iters[newly] = iteration
            finished |= newly
            if np.all(kkt <= tol):
                break
    g = np.asarray(R.T @ (R @ X)) - H
    kkt = np.max(np.abs(np.minimum(X * lipschitz, g)), axis=0) / scale
    residuals = np.asarray(R @ X) - S
    result = {}
    for col, k in enumerate(keys):
        err = float(np.linalg.norm(X[:, col] - b / norm))
        result[k] = {"relative": err, "absolute": norm * err,
                     "iterations": int(iters[col] or iteration),
                     "iterations_executed": iteration, "converged": bool(kkt[col] <= tol),
                     "relative_projected_kkt": float(kkt[col]),
                     "sinogram_residual_absolute": float(norm * np.linalg.norm(residuals[:, col])),
                     "compression_distance_to_full_inverse_relative":
                         float(np.linalg.norm(X[:, col] - X[:, -1]))}
    return result, {"seconds": time.perf_counter() - start, "solver": "projected FISTA with gradient restart",
                    "constraint": "x>=0; variables only at j<=i", "kkt_tolerance": tol,
                    "max_iterations": maxiter, "lipschitz": lipschitz}


def _radon_active_solve(R, s, tol=1e-6):
    """Working-set NNLS, with full-variable KKT verification after every solve.

    Columns having zero R' s can be excluded exactly: R is nonnegative, hence
    adding one can never lower the objective at a nonnegative feasible point.
    Other exclusions are temporary and verified by the full projected gradient.
    """
    h = np.asarray(R.T @ s).ravel()
    scale = max(float(np.max(h)), 1e-12)
    x = np.zeros(R.shape[1])
    selected = np.empty(0, dtype=int)
    nit, nfev, expansions = 0, 0, 0
    eligible = h > 0
    grad = -h
    for expansion in range(1, 65):
        violations = eligible.copy()
        violations[selected] = False
        ids = np.flatnonzero(violations & (grad < -tol*scale))
        if not len(ids) and not len(selected):
            return x, {"converged": True, "iterations": 0, "working_set": 0,
                       "relative_projected_kkt": 0.0, "working_set_expansions": 0}
        if len(ids):
            ids = ids[np.argsort(grad[ids], kind="stable")[:128]]
            selected = np.r_[selected, ids]
        sub = R[:, selected]
        G = (sub.T @ sub).toarray()
        hs = h[selected]
        def fun(z):
            gz = G @ z
            return 0.5*float(z @ gz) - float(hs @ z), gz-hs
        opt = minimize(fun, x[selected], jac=True, method="L-BFGS-B",
                       bounds=[(0.0, None)]*len(selected),
                       options={"gtol": tol*scale*0.02, "ftol": 1e-15,
                                "maxiter": 4000, "maxcor": 20, "maxls": 50})
        nit += int(opt.nit)
        nfev += int(opt.nfev)
        x[selected] = opt.x
        grad = np.asarray(R.T @ (R @ x)).ravel()-h
        pg = np.where(x > 1e-10, grad, np.minimum(grad, 0.0))
        kkt = float(np.max(np.abs(pg))/scale)
        expansions = expansion
        if kkt <= tol:
            break
        # Keep a failed optimization visible. No conversion to a successful status.
        if not len(ids) and not opt.success:
            break
    return x, {"converged": bool(kkt <= tol), "iterations": nit, "function_evaluations": nfev,
               "working_set": len(selected), "working_set_expansions": expansions,
               "relative_projected_kkt": kkt,
               "inner_solver_success": bool(opt.success), "inner_solver_message": str(opt.message)}


def radon_decode(b, R, checkpoints, lipschitz, tol=1e-6, maxiter=3000):
    start = time.perf_counter()
    norm = float(np.linalg.norm(b))
    sino = np.asarray(R @ (b/norm)).ravel()
    order = np.argsort(-np.abs(sino), kind="stable")
    # The inverse sees only R and the complete sinogram, initialized at zero by
    # LSMR. Projected iterations enforce exact nonnegativity after this warm start.
    ls = lsmr(R, sino, atol=1e-10, btol=1e-10, maxiter=2000)
    full = np.maximum(ls[0], 0.0)
    scale = max(float(np.max(np.abs(R.T @ sino))), 1e-12)
    yf = full.copy()
    t = 1.0
    for inv_it in range(1, maxiter+1):
        g = np.asarray(R.T @ (R @ yf - sino)).ravel()
        z = np.maximum(yf-g/lipschitz, 0)
        tn = (1+np.sqrt(1+4*t*t))/2
        yn = z+(t-1)/tn*(z-full)
        if (yf-z) @ (z-full) > 0:
            tn,yn = 1.0,z.copy()
        full,yf,t = z,yn,tn
        if inv_it % 10 == 0 or inv_it == 1:
            g = np.asarray(R.T @ (R @ full-sino)).ravel()
            pg = np.where(full > 1e-10, g, np.minimum(g, 0.0))
            kkt = float(np.max(np.abs(pg))/scale)
            if kkt <= tol:
                break
    err = float(np.linalg.norm(full-b/norm))
    result = {"all": {"relative": err, "absolute": norm*err, "converged": kkt <= tol,
                       "iterations": inv_it, "lsmr_iterations": int(ls[2]), "lsmr_stop": int(ls[1]),
                       "lsmr_condition_estimate": float(ls[6]), "relative_projected_kkt": kkt,
                       "sinogram_residual_absolute": norm*float(np.linalg.norm(R@full-sino)),
                       "compression_distance_to_full_inverse_relative": 0.0}}
    for k in checkpoints:
        s = np.zeros_like(sino)
        s[order[:k]] = sino[order[:k]]
        x, diag = _radon_active_solve(R,s,tol)
        err = float(np.linalg.norm(x-b/norm))
        result[k] = {"relative": err, "absolute": norm*err, **diag,
                     "sinogram_residual_absolute": norm*float(np.linalg.norm(R@x-s)),
                     "compression_distance_to_full_inverse_relative": float(np.linalg.norm(x-full))}
    return result, {"seconds": time.perf_counter()-start,
                    "solver": "nonnegative least squares, working-set L-BFGS-B with full KKT check",
                    "full_inverse": "LSMR from zero then projected FISTA",
                    "constraint": "x>=0; variables only at j<=i", "kkt_tolerance": tol,
                    "max_inverse_iterations": maxiter, "lipschitz": lipschitz}


def fbp_reference(A, checkpoints):
    theta = np.arange(0, 180, 2, dtype=float)
    sino = radon(A, theta=theta, circle=False, preserve_range=True)
    order = np.argsort(-np.abs(sino.ravel()), kind="stable")
    norm = float(np.linalg.norm(A))
    result = {}
    for k in list(checkpoints) + ["all"]:
        s = np.zeros(sino.size)
        ids = order if k == "all" else order[:k]
        s[ids] = sino.ravel()[ids]
        rec = iradon(s.reshape(sino.shape), theta=theta, circle=False,
                     filter_name="ramp", output_size=len(A), preserve_range=True)
        e = float(np.linalg.norm(rec - A))
        result[k] = {"relative": e / norm, "absolute": e}
    return result


def svd_errors(A, checkpoints):
    norm = float(np.linalg.norm(A))
    s = linalg.svdvals(A, check_finite=False)
    return {k: {"relative": float(np.linalg.norm(s[k:]) / norm),
                "absolute": float(np.linalg.norm(s[k:]))} for k in checkpoints}


def block_summary(values, documents, bootstrap=2000):
    values = np.asarray(values, dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Nonfinite values cannot be aggregated")
    docs = np.unique(documents)
    groups = [np.flatnonzero(np.asarray(documents) == doc) for doc in docs]
    rng = np.random.default_rng(SEED)
    samples = rng.integers(0, len(groups), size=(bootstrap, len(groups)))
    if len({len(g) for g in groups})==1:
        indices=np.asarray(groups)[samples].reshape(bootstrap,-1)
        medians=np.median(values[indices],axis=1)
    else:
        medians = [np.median(values[np.concatenate([groups[g] for g in row])]) for row in samples]
    q1, median, q3 = np.quantile(values, [0.25, 0.5, 0.75])
    return {"n_instances": len(values), "n_documents": len(docs), "median": float(median),
            "q25": float(q1), "q75": float(q3), "iqr": float(q3 - q1),
            "median_ci95_document_block": np.quantile(medians, [0.025, 0.975]).tolist(),
            "bootstrap_replicates": bootstrap, "bootstrap_seed": SEED}
