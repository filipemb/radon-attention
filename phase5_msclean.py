"""P0 V3 named greedy decomposition; explicit norms, energies and overlap.

The greedy fitting rule is unchanged. Matrix experiments consume the immutable
V2 archives; no model loading, silent NaN replacement, or old JSON writes.
"""
from sampling import MODELS
import numpy as np
from phase06_profiled_lines import atom_vector

TAUS = [1, 2, 4, 8, 16, 32, 64]
DIAGS = [1, 2, 4, 8, 16, 32, 64]
VERTS = [0, 1, 2]


def build_dict(n):
    cols, labels = [], []
    for c in VERTS:
        cols.append(atom_vector("vert", c, n)); labels.append(("sink" if c == 0 else "vert", c))
    for tau in TAUS:
        cols.append(atom_vector("band", tau, n)); labels.append(("band", tau))
    for d in DIAGS:
        cols.append(atom_vector("diag", d, n)); labels.append(("diag", d))
    return np.stack(cols, axis=1), labels   # D: [n*n, m_atoms]


def msclean(A, D, labels, max_m):
    """MP guloso nomeado. Retorna clean (n*n,), lista de (label, coef)."""
    b = A.ravel().copy()
    R = b.copy()
    clean = np.zeros_like(b)
    chosen = set(); picks = []
    for _ in range(max_m):
        corr = D.T @ R                     # atomos normalizados -> corr = <R, atom>
        for j in chosen:
            corr[j] = -np.inf
        j = int(np.argmax(corr))
        if corr[j] <= 0:
            break
        coef = float(corr[j])
        clean += coef * D[:, j]
        R = b - clean
        chosen.add(j); picks.append((labels[j], coef))
    return clean, picks


def svd_rankk_err(residual_mat, A, clean, ks):
    normA = np.linalg.norm(A) + 1e-12
    U, S, Vt = np.linalg.svd(residual_mat, full_matrices=False)
    out = {}
    for k in ks:
        Rk = (U[:, :k] * S[:k]) @ Vt[:k] if k > 0 else np.zeros_like(residual_mat)
        recon = clean + Rk
        out[k] = float(np.linalg.norm(A - recon) / normA)
    return out



def fraction_metrics(A, S, L):
    """Report overlapping channels without calling a norm ratio an energy share."""
    A, S, L = (np.asarray(x, dtype=np.float64) for x in (A, S, L))
    if not all(np.isfinite(x).all() for x in (A, S, L)):
        raise ValueError("Nonfinite component; no silent replacement")
    a2 = float(np.sum(A*A))
    if a2 <= 0:
        raise ValueError("Zero reference energy")
    s2, l2 = float(np.sum(S*S)), float(np.sum(L*L))
    cross = float(2*np.sum(S*L))
    error2 = float(np.sum((A-S-L)**2))
    named_error2 = float(np.sum((A-S)**2))
    identity = float(np.sum((S+L)**2)) - s2 - l2 - cross
    if abs(identity) / a2 > 1e-12:
        raise RuntimeError("Component energy accounting identity failed")
    return {"named_norm_ratio": float(np.sqrt(s2/a2)), "named_energy_ratio": s2/a2,
            "lowrank_energy_ratio": l2/a2, "cross_term_SL_over_A_energy": cross/a2,
            "named_only_relative_error": float(np.sqrt(named_error2/a2)),
            "reconstruction_relative_error": float(np.sqrt(error2/a2)),
            "named_error_reduction_energy": 1-named_error2/a2,
            "total_error_reduction_energy": 1-error2/a2,
            "named_marginal_error_reduction_given_L": (float(np.sum((A-L)**2))-error2)/a2,
            "energy_identity_abs_error_over_A_energy": abs(identity)/a2}

def main():
    from phase26_p0_named import main as offline_main
    offline_main(default_methods=["msclean"])

if __name__ == "__main__":
    main()
