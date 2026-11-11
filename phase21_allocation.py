"""E4: allocation conventions, storage capacity and residual diagnostics.

The dictionary is imported literally from phase5 (also used by phase6). The
current source has 17, not 15, atoms; no atom is added, removed or redefined.
All matrices in each immutable V2 manifest are evaluated. No GPU in `matrices`.

Statistics: means across all sampled heads/layers within each document, then
median/IQR and a percentile bootstrap of whole documents (2,000 draws, seed 0).
The pooled instance median/IQR are also reported, with a separate label.
"""
import os
for _thread_key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_thread_key] = "4"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import datasets  # Required before torch, including phase5's indirect imports.
import argparse
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from functools import partial
from pathlib import Path
import sys
import time
import numpy as np
import scipy
from scipy.linalg import qr, svd, svdvals
from scipy.optimize import nnls
import torch
from phase5_msclean import build_dict
from sampling import MODELS, CORPUS_PATH, load_sample, sample_paths, sha256_file, slug, validate_matrices

torch.set_num_threads(4)
RANKS = (0, 1, 2, 4, 8, 16)
CONVENTIONS = ("named_first", "lowrank_first", "alternating")
ITERATIONS = 5
SEED = 0
N_BOOTSTRAP = 2000
STOP_RTOL = 1e-7
KKT_RTOL = 1e-8
PROGRESS = Path("out/_rerun_logs/e4_progress.md")
DISTANCE_LABELS = ("future_d<0", "d=0", "d=1", "d=2..3", "d=4..7", "d=8..15",
                   "d=16..31", "d=32..63", "d=64..127", "d>=128")
MAIN_METRICS = ("named_norm_ratio", "named_energy_ratio", "cross_energy_ratio",
                "named_only_explained_energy", "relative_error", "n_active", "parameters",
                "svd_budget_rank", "svd_budget_parameters", "budget_unused_by_svd",
                "svd_budget_error", "error_minus_svd_budget", "svd_same_r_error",
                "svd_r_plus_atoms_rank", "svd_r_plus_atoms_error", "error_minus_svd_r_plus_atoms",
                "named_only_error_same_budget", "nnls_kkt_violation", "nnls_complementarity",
                "lowrank_energy_ratio", "final_energy_identity_discrepancy")


def progress(message):
    PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with PROGRESS.open("a", encoding="utf-8") as out:
        out.write(f"- {stamp} | {message}\n")
    print(f"E4 {message}", flush=True)


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as out:
        json.dump(value, out, indent=2, ensure_ascii=False, allow_nan=False)
        out.write("\n")


def metadata():
    return {"schema_version": 1, "ranks": list(RANKS), "conventions": list(CONVENTIONS),
            "alternating": {"initial_L": 0, "fixed_T": ITERATIONS,
                            "early_stopping": False, "diagnostic_relative_objective_change": STOP_RTOL,
                            "criterion": "abs(previous_error_squared-current_error_squared)/max(previous_error_squared, float64_tiny) <= tolerance; diagnostic only; always run T"},
            "nnls": {"solver": "scipy.optimize.nnls on economic QR of the unchanged dictionary",
                     "equivalence": "||Dc-b||^2 = ||Rc-Q.T b||^2 + ||(I-QQ.T)b||^2",
                     "maxiter": "100 * number_of_atoms", "dtype": "float64",
                     "active_definition_for_budget": "coefficient > 0, including every positive small coefficient; no pruning",
                     "kkt_relative_tolerance": KKT_RTOL},
            "svd": {"solver": "scipy.linalg.svd, gesdd, full_matrices=False, float64",
                    "boundary_tie_numerical_tolerance": "64 * float64_eps * n * sigma_1",
                    "exact_and_numerical_ties_reported_separately": True},
            "uniqueness": {"S_named_first": "Unique Euclidean projection onto a finitely generated closed convex cone. Coefficients need not be unique in general.",
                           "L": "Rank-r truncation unique at a positive cutoff if sigma_r > sigma_(r+1). L=0 for r=0; an already rank<=r residual is reconstructed uniquely. No joint identifiability or alternating global optimum claimed.",
                           "allocation": "Operational convention, not intrinsic separation: vertical atoms are rank one and overlap with the low-rank family."},
            "budget": {"S_plus_L": "2 * all_strictly_positive_coefficients + r * (2n+1)",
                       "svd_rank_at_same_cap": "min(n, floor(S_plus_L_parameters/(2n+1)))",
                       "unused_budget": "Reported explicitly; no fractional singular vectors or conditional subsets",
                       "legacy_rank_comparison": "SVD r and SVD (r + number_of_active_atoms), separately; this is not parameter matching or an actual rank bound for full-rank band atoms"},
            "aggregation": {"primary_unit": "document mean across every sampled layer/head in that document",
                            "primary_statistics": "median, p25, p75, IQR across document means; percentile 95% CI of this median",
                            "bootstrap": "resample document IDs with replacement, preserving all instances per block",
                            "n_bootstrap": N_BOOTSTRAP, "seed": SEED,
                            "secondary_statistics": "Pooled instance median, p25, p75, IQR; descriptive only",
                            "paired_differences": "Per-instance differences first, then document means, then the same statistics"},
            "residual": {"distance_bins": list(DISTANCE_LABELS),
                         "energy": "sum of squared entries, signed residuals retained",
                         "spectrum": "all n singular values; final spectrum equals R spectrum with first r removed for named_first/alternating",
                         "effective_rank": "exp(-sum p_i log p_i), p_i=sigma_i^2/sum sigma^2; exactly zero residual: entropy=0, effective_rank=0",
                         "exact_zero_residual_policy": "Flagged explicitly; normalized spatial/spectral energy profiles are defined as all zero, entropy=0 and effective_rank=0. No 0/0 is formed, no NaN is replaced, and zero-residual instances remain in every aggregate.",
                         "normalization": "both fraction of residual energy and energy/||A||^2; first four columns also individually",
                         "future_entries": "Included in final residual diagnostics, since low-rank truncation need not be causal. No matrix remasking in this in-sample experiment."},
            "software": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__, "torch": torch.__version__},
            "scope": "Only newly created phase21_/allocation_ artifacts and the requested e4_progress.md; inputs unchanged"}


class Dictionary:
    def __init__(self, n):
        self.n = n
        self.D, self.labels = build_dict(n)
        self.Q, self.R = qr(self.D, mode="economic", check_finite=True)
        self.G = self.D.T @ self.D
        self.singular_values = svdvals(self.D)
        self.digest = hashlib.sha256(self.D.tobytes(order="C")).hexdigest()
        i, j = np.indices((n, n))
        d = i - j
        self.distance_bins = np.searchsorted(np.array([0, 1, 2, 4, 8, 16, 32, 64, 128]), d, side="right").ravel()

    def project(self, target):
        b = target.ravel()
        c, _ = nnls(self.R, self.Q.T @ b, maxiter=100 * self.D.shape[1])
        if not np.isfinite(c).all():
            raise ArithmeticError("Nonfinite NNLS coefficient; no replacement or omitted atom")
        S = (self.D @ c).reshape(target.shape)
        gradient = self.D.T @ (S.ravel() - b)
        scale = max(float(np.linalg.norm(b)), np.finfo(float).tiny)
        primal = max(0., float(-c.min())) / scale
        dual = max(0., float(-gradient.min())) / scale
        comp = float(np.max(np.abs(c * gradient))) / (scale * scale)
        violation = max(primal, dual, comp)
        if not np.isfinite(violation) or violation > KKT_RTOL:
            raise ArithmeticError(f"NNLS KKT failure: {violation}, comp={comp}")
        return S, c, {"nnls_kkt_violation": violation, "nnls_complementarity": comp}

    def describe(self):
        off = np.abs(self.G - np.eye(len(self.labels)))
        return {"source": "phase5_msclean.build_dict (unchanged; also imported by phase6)",
                "n_atoms": len(self.labels), "labels": self.labels, "sha256_float64_C_order": self.digest,
                "singular_values": self.singular_values.tolist(), "numerical_column_rank": int(np.linalg.matrix_rank(self.R)),
                "gram_eigenvalues": np.linalg.eigvalsh(self.G).tolist(), "maximum_coherence": float(off.max()),
                "requested_count_discrepancy": "Prompt says 15; literal phase5/6 build_dict returns 3+7+7=17. No change to source dictionary."}


def factor(A):
    return svd(A, full_matrices=False, check_finite=False, lapack_driver="gesdd")


def truncate(factors, rank):
    u, s, vh = factors
    if rank == 0:
        return np.zeros((u.shape[0], vh.shape[1]), dtype=np.float64)
    return (u[:, :rank] * s[:rank]) @ vh[:rank]


def cutoff(s, rank, n):
    if rank == 0:
        return {"rank": 0, "zero_rank_unique": True, "boundary_exists": False,
                "exact_tie": False, "numerical_tie": False, "positive_numerical_tie": False}
    tolerance = 64 * np.finfo(float).eps * n * float(s[0])
    gap = float(s[rank - 1] - s[rank])
    return {"rank": rank, "boundary_exists": True, "sigma_r": float(s[rank - 1]),
            "sigma_r_plus_1": float(s[rank]), "gap": gap, "numerical_tolerance": tolerance,
            "exact_tie": bool(gap == 0), "numerical_tie": bool(gap <= tolerance),
            "positive_numerical_tie": bool(gap <= tolerance and s[rank - 1] > tolerance)}


def residual_profile(M, singular_values, denominator, dictionary, spectrum_reference=None, drop=0):
    s = np.asarray(singular_values, dtype=np.float64)[drop:]
    energy = float(np.sum(M * M))
    spectral_energy = float(np.dot(s, s))
    if abs(energy - spectral_energy) > 2e-9 * max(denominator, energy):
        raise ArithmeticError("Residual spectrum/energy disagree")
    if energy == 0:
        entropy = 0.
        effective_rank = 0.
        fractions = np.zeros(len(s))
    else:
        fractions = s * s / spectral_energy
        p = fractions[fractions > 0]
        entropy = float(-np.dot(p, np.log(p)))
        effective_rank = float(np.exp(entropy))
    e_by_d = np.bincount(dictionary.distance_bins, weights=(M * M).ravel(), minlength=len(DISTANCE_LABELS))
    e_by_col = np.sum(M[:, :4] ** 2, axis=0)
    divisor = energy if energy > 0 else 1.
    out = {"energy_over_A": energy / denominator, "shannon_entropy_sigma_squared": entropy,
           "effective_rank": effective_rank, "exact_zero_energy": energy == 0,
           "distance_fraction_of_residual": (e_by_d / divisor).tolist(),
           "distance_energy_over_A": (e_by_d / denominator).tolist(),
           "first4_columns_fraction_of_residual": float(e_by_col.sum() / divisor),
           "first4_columns_energy_over_A": float(e_by_col.sum() / denominator),
           "columns_0_to_3_fraction_of_residual": (e_by_col / divisor).tolist(),
           "negative_entries_energy_fraction": float(np.sum(M[M < 0] ** 2) / divisor),
           "top_1_4_8_16_spectral_energy_fraction": [float(fractions[:k].sum()) for k in (1, 4, 8, 16)]}
    if spectrum_reference is None:
        out["singular_values"] = np.asarray(singular_values).tolist()
        out["spectrum_drop_first"] = drop
    else:
        out["spectrum_reference"] = spectrum_reference
        out["spectrum_drop_first"] = drop
    return out


def svd_error(s, rank, norm):
    return float(np.linalg.norm(s[min(rank, len(s)):]) / norm)


def observation(A, S, L, c, solver, sA, rank, dictionary, residual_factors=None,
                residual_reference=None, trace=None):
    n = A.shape[0]
    eA = float(np.sum(A * A))
    norm = np.sqrt(eA)
    R = A - S
    E = R - L
    active = int(np.count_nonzero(c > 0))
    params = 2 * active + rank * (2 * n + 1)
    svd_rank = min(n, params // (2 * n + 1))
    same_rank = min(n, rank + active)
    normS2, normL2 = float(np.sum(S * S)), float(np.sum(L * L))
    cross = float(2 * np.sum(S * L) / eA)
    err = float(np.linalg.norm(E) / norm)
    metrics = {"named_norm_ratio": float(np.sqrt(normS2 / eA)), "named_energy_ratio": normS2 / eA,
               "cross_energy_ratio": cross, "named_only_explained_energy": 1 - float(np.sum(R * R) / eA),
               "relative_error": err, "n_active": active, "parameters": params,
               "svd_budget_rank": svd_rank, "svd_budget_parameters": svd_rank * (2 * n + 1),
               "budget_unused_by_svd": params - svd_rank * (2 * n + 1),
               "svd_budget_error": svd_error(sA, svd_rank, norm),
               "svd_same_r_error": svd_error(sA, rank, norm),
               "svd_r_plus_atoms_rank": same_rank, "svd_r_plus_atoms_error": svd_error(sA, same_rank, norm),
               "lowrank_energy_ratio": normL2 / eA, **solver}
    metrics["error_minus_svd_budget"] = err - metrics["svd_budget_error"]
    metrics["error_minus_svd_r_plus_atoms"] = err - metrics["svd_r_plus_atoms_error"]
    metrics["final_energy_identity_discrepancy"] = abs(float(np.sum((S + L) ** 2) / eA) - (normS2 / eA + normL2 / eA + cross))
    out = {"metrics": metrics, "coefficients": c.tolist()}
    if residual_factors is not None:
        sR = residual_factors[1]
        out["lowrank_cutoff"] = cutoff(sR, rank, n)
        out["residual_A_minus_S"] = ({"profile_reference": residual_reference}
                                      if residual_reference is not None else residual_profile(R, sR, eA, dictionary))
        ref = residual_reference if residual_reference else "self.residual_A_minus_S"
        out["residual_A_minus_S_minus_L"] = residual_profile(E, sR, eA, dictionary, ref, rank)
    else:
        sR = svdvals(R, check_finite=False)
        sE = svdvals(E, check_finite=False)
        out["lowrank_cutoff"] = cutoff(sA, rank, n)
        out["residual_A_minus_S"] = residual_profile(R, sR, eA, dictionary)
        out["residual_A_minus_S_minus_L"] = residual_profile(E, sE, eA, dictionary)
    if trace is not None:
        out["alternating_diagnostics"] = trace
    return out


def evaluate_instance(A, dictionary):
    n = A.shape[0]
    eA = float(np.sum(A * A))
    if not np.isfinite(A).all() or eA <= 0:
        raise ValueError("Nonfinite/zero input: never replace, omit, or zero NaNs")
    fA = factor(A)
    S0, c0, solve0 = dictionary.project(A)
    R0 = A - S0
    f0 = factor(R0)
    proj_discrepancy = abs(float(np.sum(S0 * S0) + np.sum(R0 * R0) - eA)) / eA
    if proj_discrepancy > 2e-8:
        raise ArithmeticError("Euclidean cone projection failed Moreau/Pythagorean check")
    row = {"attention_singular_values": fA[1].tolist(),
           "attention_frobenius_norm": float(np.sqrt(eA)),
           "named_first_projection": {"coefficients": c0.tolist(), "pythagorean_relative_discrepancy": proj_discrepancy,
                                      "residual_A_minus_S": residual_profile(R0, f0[1], eA, dictionary)},
           "conventions": {c: {} for c in CONVENTIONS}, "allocation_comparisons": {}}
    for rank in RANKS:
        L0 = truncate(f0, rank)
        nf = observation(A, S0, L0, c0, solve0, fA[1], rank, dictionary, f0,
                         "named_first_projection.residual_A_minus_S")
        nf["metrics"]["named_only_error_same_budget"] = float(np.linalg.norm(R0) / np.sqrt(eA))
        row["conventions"]["named_first"][str(rank)] = nf
        La = truncate(fA, rank)
        Sl, cl, solvel = dictionary.project(A - La)
        lr = observation(A, Sl, La, cl, solvel, fA[1], rank, dictionary)
        lr["metrics"]["named_only_error_same_budget"] = nf["metrics"]["named_only_error_same_budget"]
        row["conventions"]["lowrank_first"][str(rank)] = lr
        S, L, coef, sol, fR = S0, L0, c0, solve0, f0
        objectives = [float(np.sum((R0 - L0) ** 2) / eA)]
        diagnostic_at = None
        updates_with_exact_tie = int(cutoff(f0[1], rank, n)["exact_tie"])
        updates_with_numerical_tie = int(cutoff(f0[1], rank, n)["numerical_tie"])
        for it in range(1, ITERATIONS):
            S, coef, sol = dictionary.project(A - L)
            fR = factor(A - S)
            L = truncate(fR, rank)
            obj = float(np.sum((A - S - L) ** 2) / eA)
            previous = objectives[-1]
            if obj > previous + 2e-9:
                raise ArithmeticError(f"Alternating objective increased: {previous} -> {obj}")
            if diagnostic_at is None and abs(previous - obj) / max(previous, np.finfo(float).tiny) <= STOP_RTOL:
                diagnostic_at = it + 1
            objectives.append(obj)
            gap = cutoff(fR[1], rank, n)
            updates_with_exact_tie += int(gap["exact_tie"])
            updates_with_numerical_tie += int(gap["numerical_tie"])
        trace = {"iterations_run": ITERATIONS, "stop_reason": "fixed_T",
                 "relative_squared_error_by_iteration": objectives,
                 "diagnostic_tolerance_first_met_at": diagnostic_at,
                 "diagnostic_tolerance_met": diagnostic_at is not None,
                 "SVD_updates_with_exact_tie": updates_with_exact_tie,
                 "SVD_updates_with_numerical_tie": updates_with_numerical_tie}
        alt = observation(A, S, L, coef, sol, fA[1], rank, dictionary, fR, trace=trace)
        alt["metrics"]["named_only_error_same_budget"] = nf["metrics"]["named_only_error_same_budget"]
        row["conventions"]["alternating"][str(rank)] = alt
        row["allocation_comparisons"][str(rank)] = {
            "S_lowrank_first_minus_named_first_norm_over_A": float(np.linalg.norm(Sl - S0) / np.sqrt(eA)),
            "S_alternating_minus_named_first_norm_over_A": float(np.linalg.norm(S - S0) / np.sqrt(eA)),
            "named_energy_lowrank_first_minus_named_first": lr["metrics"]["named_energy_ratio"] - nf["metrics"]["named_energy_ratio"],
            "named_energy_alternating_minus_named_first": alt["metrics"]["named_energy_ratio"] - nf["metrics"]["named_energy_ratio"],
            "error_alternating_minus_named_first": alt["metrics"]["relative_error"] - nf["metrics"]["relative_error"]}
    return row


def describe_columns(values, document_indices):
    a = np.asarray(values, dtype=np.float64)
    if a.ndim == 1:
        a = a[:, None]
    if a.ndim != 2 or not np.isfinite(a).all():
        raise ValueError("Nonfinite metric or unsupported statistic shape")
    docs = np.asarray(document_indices)
    unique = np.unique(docs)
    blocks = np.stack([a[docs == d].mean(axis=0) for d in unique])
    draws = np.random.default_rng(SEED).integers(0, len(unique), size=(N_BOOTSTRAP, len(unique)))
    lo, med, hi = np.percentile(blocks, [25, 50, 75], axis=0)
    ilo, imed, ihi = np.percentile(a, [25, 50, 75], axis=0)
    cis = []
    for start in range(0, a.shape[1], 16):
        bs = np.median(blocks[draws, start:start + 16], axis=1)
        cis.extend(np.percentile(bs, [2.5, 97.5], axis=0).T.tolist())
    return [{"median": float(med[j]), "p25": float(lo[j]), "p75": float(hi[j]), "iqr": float(hi[j] - lo[j]),
             "ci95_document_block_bootstrap": cis[j], "mean": float(blocks[:, j].mean()),
             "n_documents": len(unique), "n_instances": len(a),
             "instance_distribution": {"median": float(imed[j]), "p25": float(ilo[j]), "p75": float(ihi[j]),
                                       "iqr": float(ihi[j] - ilo[j])}}
            for j in range(a.shape[1])]


def aggregate_named(records, docs):
    keys = list(records[0])
    result = {}
    scalar_keys = [k for k in keys if isinstance(records[0][k], (int, float, bool))]
    descriptions = describe_columns([[r[k] for k in scalar_keys] for r in records], docs)
    result.update(zip(scalar_keys, descriptions))
    for key in keys:
        if isinstance(records[0][key], list):
            result[key] = describe_columns([r[key] for r in records], docs)
    return result


def resolve_profile(row, convention, rank, key):
    profile = row["conventions"][convention][str(rank)][key]
    if "profile_reference" in profile:
        return row["named_first_projection"]["residual_A_minus_S"]
    return profile


def resolved_spectrum(row, convention, rank, key):
    profile = resolve_profile(row, convention, rank, key)
    if "singular_values" in profile:
        spectrum = np.asarray(profile["singular_values"])
    elif profile["spectrum_reference"] == "named_first_projection.residual_A_minus_S":
        spectrum = np.asarray(row["named_first_projection"]["residual_A_minus_S"]["singular_values"])
    else:
        source = row["conventions"][convention][str(rank)]["residual_A_minus_S"]
        spectrum = np.asarray(source["singular_values"])
    spectrum = spectrum[profile.get("spectrum_drop_first", 0):]
    return np.pad(spectrum, (0, row["n"] - len(spectrum)))


def summarize_dataset(rows, dictionary):
    docs = [row["document_index"] for row in rows]
    result = {"conventions": {}, "allocation_comparisons": {}}
    for convention in CONVENTIONS:
        result["conventions"][convention] = {}
        for rank in RANKS:
            obs = [row["conventions"][convention][str(rank)] for row in rows]
            item = {"metrics": aggregate_named([o["metrics"] for o in obs], docs),
                    "cutoff_ties": {key: sum(int(o["lowrank_cutoff"][key]) for o in obs)
                                    for key in ("boundary_exists", "exact_tie", "numerical_tie", "positive_numerical_tie")},
                    "all_instances_paired": True}
            for residual in ("residual_A_minus_S", "residual_A_minus_S_minus_L"):
                profiles = [resolve_profile(row, convention, rank, residual) for row in rows]
                # Spectrum references are resolved once; do not duplicate padded zeros in JSONL.
                clean = [{k: v for k, v in p.items() if k not in ("singular_values", "spectrum_reference", "spectrum_drop_first")}
                         for p in profiles]
                item[residual] = aggregate_named(clean, docs)
                spectra = np.stack([resolved_spectrum(row, convention, rank, residual) for row in rows])
                item[residual]["singular_values"] = describe_columns(spectra, docs)
                norms = np.asarray([row["attention_frobenius_norm"] for row in rows])
                item[residual]["singular_values_over_A_norm"] = describe_columns(spectra / norms[:, None], docs)
            if convention == "alternating":
                traces = [o["alternating_diagnostics"] for o in obs]
                item["alternating_diagnostics"] = {
                    "fixed_T": ITERATIONS, "early_stopped_instances": 0,
                    "instances_meeting_diagnostic_tolerance_by_T": sum(t["diagnostic_tolerance_met"] for t in traces),
                    "SVD_updates_with_exact_tie": sum(t["SVD_updates_with_exact_tie"] for t in traces),
                    "SVD_updates_with_numerical_tie": sum(t["SVD_updates_with_numerical_tie"] for t in traces),
                    "squared_error_by_iteration": describe_columns([t["relative_squared_error_by_iteration"] for t in traces], docs)}
            result["conventions"][convention][str(rank)] = item
        progress(f"aggregated {rows[0]['model']} n={dictionary.n} convention={convention}")
    for rank in RANKS:
        result["allocation_comparisons"][str(rank)] = aggregate_named([r["allocation_comparisons"][str(rank)] for r in rows], docs)
    return result


def dataset_paths(model, n):
    stem = f"phase21_allocation_{slug(model)}_n{n}"
    return Path("out") / f"{stem}.json", Path("out/pairs") / f"{stem}.jsonl"


def run_dataset(job):
    model, n = job
    started = time.perf_counter()
    target, pairs_path = dataset_paths(model, n)
    if target.exists():
        existing = json.loads(target.read_text(encoding="utf-8"))
        if existing["manifest_sha256"] != sha256_file(sample_paths(model, n)[1]):
            raise RuntimeError(f"Stale manifest: {target}")
        if existing["pairs_sha256"] != sha256_file(pairs_path):
            raise RuntimeError(f"Stale pairs: {pairs_path}")
        return str(target)
    attention, manifest = load_sample(model, n)
    validation = validate_matrices(attention, manifest["storage_row_sum_atol"])
    if validation["invalid_matrices"] or validation["nan_values"] or validation["inf_values"] or validation["negative_values"]:
        raise ValueError(f"Invalid archive {model}, n={n}: {validation}")
    if sha256_file(sample_paths(model, n)[0]) != manifest["npz_sha256"]:
        raise ValueError("Archive hash mismatch")
    dictionary = Dictionary(n)
    rows = []
    if pairs_path.exists():
        with pairs_path.open(encoding="utf-8") as inp:
            for i, line in enumerate(inp):
                row = json.loads(line)
                if row["instance_id"] != manifest["instances"][i]["instance_id"] or row["dictionary_sha256"] != dictionary.digest:
                    raise ValueError("Resume mismatch; preserve partial file and inspect")
                rows.append(row)
    progress(f"START {model} n={n}, {len(attention)} instances, 64 document blocks, resume={len(rows)}, T={ITERATIONS}, atoms={len(dictionary.labels)}")
    pairs_path.parent.mkdir(parents=True, exist_ok=True)
    with pairs_path.open("a", encoding="utf-8") as out:
        for i in range(len(rows), len(attention)):
            row = {**manifest["instances"][i], "model": model, "dictionary_sha256": dictionary.digest,
                   **evaluate_instance(attention[i].astype(np.float64), dictionary)}
            out.write(json.dumps(row, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n")
            rows.append(row)
            if (i + 1) % 64 == 0:
                out.flush()
                progress(f"MATRICES {model} n={n}: {i+1}/{len(attention)}, seconds={time.perf_counter()-started:.1f}")
    if len(rows) != manifest["n_matrices"]:
        raise RuntimeError("Incomplete same-instance population")
    summaries = summarize_dataset(rows, dictionary)
    result = {"schema_version": 1, "model": model, "n": n, "n_instances": len(rows),
              "n_documents": len(set(r["doc_id"] for r in rows)), "all_manifest_instances_used": True,
              "manifest_sha256": sha256_file(sample_paths(model, n)[1]), "npz_sha256": manifest["npz_sha256"],
              "corpus_manifest_sha256": manifest["corpus_manifest_sha256"],
              "pairs_path": pairs_path.as_posix(), "pairs_sha256": sha256_file(pairs_path),
              "dictionary": dictionary.describe(), "input_validation": validation,
              "settings": metadata(), **summaries, "elapsed_seconds": time.perf_counter() - started}
    write_new(target, result)
    progress(f"DONE {model} n={n}, seconds={result['elapsed_seconds']:.1f}, pairs_bytes={pairs_path.stat().st_size}")
    return str(target)


def check():
    started = time.perf_counter()
    checks = []
    for n in (128, 256):
        dictionary = Dictionary(n)
        attention, _ = load_sample("gpt2", n)
        for i in (0, len(attention) // 2, len(attention) - 1):
            A = attention[i].astype(np.float64)
            S, c, diagnostics = dictionary.project(A)
            direct, _ = nnls(dictionary.D, A.ravel(), maxiter=100 * dictionary.D.shape[1])
            discrepancy = float(np.linalg.norm(S.ravel() - dictionary.D @ direct) / np.linalg.norm(A))
            if discrepancy > 1e-9:
                raise AssertionError("QR and original full NNLS projections differ")
            begin = time.perf_counter()
            row = evaluate_instance(A, dictionary)
            # Named first's projection is independent of r, unlike the joint fit.
            for rank in RANKS:
                m = row["conventions"]["named_first"][str(rank)]["metrics"]
                if abs(m["named_energy_ratio"] - m["named_only_explained_energy"]) > 2e-8:
                    raise AssertionError("Projection identity failed")
                if m["svd_budget_parameters"] > m["parameters"]:
                    raise AssertionError("Budget violation")
            checks.append({"n": n, "instance_index": i, "QR_vs_full_NNLS_relative_difference": discrepancy,
                           "full_three_conventions_seconds": time.perf_counter() - begin, **diagnostics})
        # Sink is explicitly both a named atom and rank-one: intrinsic separation fails.
        sink = dictionary.D[:, 0].reshape(n, n)
        c = np.zeros(dictionary.D.shape[1]); c[0] = 1
        if np.linalg.norm(dictionary.D @ c - sink.ravel()) != 0 or np.linalg.matrix_rank(sink) != 1:
            raise AssertionError("Sink overlap control failed")
    result = {"checks": checks, "sink_shared_between_channels_control_passed": True,
              "settings": metadata(), "elapsed_seconds": time.perf_counter() - started}
    write_new("out/phase21_allocation_checks.json", result)
    progress(f"CHECKS PASSED, {len(checks)} fixed real instances plus sink overlap controls; {result['elapsed_seconds']:.2f}s")
    return result


class ForwardNamedFirst:
    """Only the estimator; causal support/normalization belong to imported V1.

    NNLS is float64 on CPU, with shared batched sufficient statistics. The
    residual SVD is batched float32 on GPU, just as V1's SVD arm is float32.
    """
    def __init__(self, dictionary, harness, empty_policy):
        self.dictionary = dictionary
        self.harness = harness
        self.empty_policy = empty_policy
        self.rank_cap = None
        self.reset()

    def reset(self):
        self.stats = {}
        self.document_costs = None
        self.max_kkt_violation = 0.

    @torch.inference_mode()
    def __call__(self, weights):
        b, h, q, k = weights.shape
        if q != k or q != self.dictionary.n or self.rank_cap not in (8, 16):
            raise ValueError("E4 requires the declared square n=128 prefill and rank cap 8 or 16")
        w = weights.reshape(b * h, q, k).float()
        vectors = w.cpu().numpy().astype(np.float64).reshape(b * h, q * k)
        rhs = vectors @ self.dictionary.Q
        coef = np.stack([nnls(self.dictionary.R, v, maxiter=100 * len(self.dictionary.labels))[0] for v in rhs])
        if not np.isfinite(coef).all() or not np.isfinite(rhs).all():
            raise ArithmeticError("Nonfinite forward NNLS coefficient/statistic; no replacement")
        gradient = coef @ self.dictionary.G - rhs @ self.dictionary.R
        scales = np.linalg.norm(vectors, axis=1)
        if not np.isfinite(scales).all() or np.any(scales <= 0):
            raise ArithmeticError("Invalid forward attention; no NaN replacement")
        dual = np.maximum(0., -gradient.min(axis=1)) / scales
        comp = np.max(np.abs(coef * gradient), axis=1) / scales ** 2
        violation = float(max(dual.max(), comp.max(), max(0., -coef.min()) / scales.min()))
        if not np.isfinite(violation) or violation > KKT_RTOL:
            raise ArithmeticError(f"Batched forward NNLS KKT failure: {violation}")
        self.max_kkt_violation = max(self.max_kkt_violation, violation)
        active = np.count_nonzero(coef > 0, axis=1)
        budget = self.rank_cap * (2 * q + 1)
        ranks = np.minimum(q, (budget - 2 * active) // (2 * q + 1))
        if np.any(ranks < 0):
            raise ArithmeticError("The named component alone exceeds the declared cap")
        costs = 2 * active + ranks * (2 * q + 1)
        if np.any(costs > budget) or np.any(costs + (2 * q + 1) <= budget):
            raise ArithmeticError("Residual rank is not the largest integer allowed by the common cap")
        S_cpu = (coef @ self.dictionary.D.T).reshape(b * h, q, k)
        S = torch.from_numpy(S_cpu).to(device=w.device, dtype=torch.float32)
        u, s, vh = torch.linalg.svd(w - S, full_matrices=False)
        max_rank = int(ranks.max())
        selected = torch.arange(max_rank, device=w.device)[None, :] < torch.as_tensor(ranks, device=w.device)[:, None]
        L = (u[..., :max_rank] * (s[..., :max_rank] * selected)[:, None, :]) @ vh[..., :max_rank, :]
        rec = S + L
        if self.document_costs is None:
            self.document_costs = [{"head_layer_fits": 0, "common_cap_total": 0, "actual_parameters_total": 0,
                                    "unused_parameters_total": 0, "active_atom_counts": {}, "residual_rank_counts": {}}
                                   for _ in range(b)]
        if len(self.document_costs) != b:
            raise ArithmeticError("Reset estimator at each new forward/batch")
        for bi in range(b):
            counts = self.document_costs[bi]
            sl = slice(bi * h, (bi + 1) * h)
            counts["head_layer_fits"] += h
            counts["common_cap_total"] += budget * h
            counts["actual_parameters_total"] += int(costs[sl].sum())
            counts["unused_parameters_total"] += int((budget - costs[sl]).sum())
            for key, values in (("active_atom_counts", active), ("residual_rank_counts", ranks)):
                vals, frequencies = np.unique(values[sl], return_counts=True)
                for value, count in zip(vals, frequencies):
                    label = str(int(value))
                    counts[key][label] = counts[key].get(label, 0) + int(count)
        # This call is the SAME remask/clamp/normalize/dtype/validation used by
        # V1 SVD. No causal logic is copied into E4.
        return self.harness.normalize_reconstruction(rec, weights.reshape(b * h, q, k), self.stats,
                                                     self.empty_policy).reshape(b, h, q, k)


def forward_paths(model):
    return (Path("out") / f"phase21_allocation_forward_{slug(model)}.json",
            Path("out/pairs") / f"phase21_allocation_forward_{slug(model)}_n128.jsonl")


def check_adapter_cpu():
    """Estimator implementation control; not a model forward or behavioral KL.

    Exercise the current imported normalizer's declared default on CPU. This
    does not choose the pending V1 scientific completion policy; real injection
    still requires its completed JSON and uses the policy from that JSON.
    """
    import phase2_downstream as harness
    harness_hash = sha256_file("phase2_downstream.py")
    default_policy = harness.RECON["empty_row_policy"]
    dictionary = Dictionary(128)
    attention, _ = load_sample("gpt2", 128)
    sink = np.zeros((128, 128), dtype=np.float32)
    sink[:, 0] = 1.
    cases = [sink, attention[0].astype(np.float32), attention[-1].astype(np.float32)]
    weights = torch.tensor(np.stack(cases))[:, None]
    estimator = ForwardNamedFirst(dictionary, harness, default_policy)
    comparisons = []
    for rank_cap in (8, 16):
        estimator.reset()
        estimator.rank_cap = rank_cap
        actual = estimator(weights).numpy()[:, 0]
        for i, raw in enumerate(cases):
            A = raw.astype(np.float64)
            S, coef, _ = dictionary.project(A)
            active = int(np.count_nonzero(coef > 0))
            rank = (rank_cap * 257 - 2 * active) // 257
            reference = S + truncate(factor(A - S), rank)
            stats = {}
            expected = harness.normalize_reconstruction(torch.tensor(reference[None], dtype=torch.float32),
                                                        weights[i], stats, default_policy).numpy()[0]
            difference = float(np.linalg.norm(actual[i] - expected) / np.linalg.norm(expected))
            if not np.isfinite(difference) or difference > 5e-5:
                raise AssertionError(f"Batched float32 estimator differs from independent scalar float64 SVD reference: {difference}")
            comparisons.append({"svd_rank_cap": rank_cap, "case": i, "residual_rank": rank,
                                "relative_difference_from_scalar_float64_reference": difference})
    if sha256_file("phase2_downstream.py") != harness_hash:
        raise RuntimeError("Harness changed during estimator control")
    result = {"passed": True, "device": "CPU", "LM_forward_executed": False, "behavioral_KL_computed": False,
              "current_harness_default_policy_for_control_only": default_policy,
              "actual_V1_scientific_policy_chosen_by_E4": False, "float32_vs_float64_tolerance": 5e-5,
              "cases": "exact sink; fixed gpt2 n128 instance 0; fixed final gpt2 n128 instance",
              "imported_harness_sha256": harness_hash, "comparisons": comparisons}
    write_new("out/phase21_allocation_adapter_checks.json", result)
    progress("CPU ADAPTER CHECKS PASSED: batched float32 estimator vs scalar float64 reference; no model forward/KL; V1 dependency unchanged")


def check_forward_estimator(harness, empty_policy):
    path = Path("out/phase21_allocation_forward_checks.json")
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if (existing["empty_row_policy_from_V1"] != empty_policy
                or existing["imported_harness_sha256"] != sha256_file("phase2_downstream.py")):
            raise RuntimeError("Preserve existing controls; V1 completion policy changed")
        return existing
    dictionary = Dictionary(128)
    attention, _ = load_sample("gpt2", 128)
    sink = np.zeros((128, 128), dtype=np.float32)
    sink[:, 0] = 1.
    cases = [sink, attention[0].astype(np.float32), attention[-1].astype(np.float32)]
    estimator = ForwardNamedFirst(dictionary, harness, empty_policy)
    results = []
    for rank_cap in (8, 16):
        estimator.rank_cap = rank_cap
        estimator.reset()
        weights = torch.tensor(np.stack(cases))[:, None]
        reconstructed = estimator(weights)
        sink_error = float((reconstructed[0, 0] - weights[0, 0]).abs().max())
        if sink_error > 2e-6:
            raise AssertionError("Exact named rank-one control was not preserved")
        results.append({"svd_rank_cap": rank_cap, "n_fixed_controls": len(cases),
                        "sink_max_entry_error": sink_error, "max_kkt_violation": estimator.max_kkt_violation,
                        "attention_validation": estimator.stats, "budget_accounting": estimator.document_costs})
    result = {"controls": results, "empty_row_policy_from_V1": empty_policy,
              "imported_harness_sha256": sha256_file("phase2_downstream.py"),
              "normalization": "Imported corrected V1 normalization, including its validation", "passed": True}
    write_new(path, result)
    progress("FORWARD ESTIMATOR CHECKS PASSED: fixed sink and two fixed real controls at both storage caps")
    return result


def run_forward_model(model_name, v2, harness, corpus, harness_hash):
    import gc
    from transformers import AutoModelForCausalLM, AttentionInterface
    started = time.perf_counter()
    target, pairpath = forward_paths(model_name)
    source = v2[model_name]
    corpus_hash = sha256_file(CORPUS_PATH)
    if target.exists():
        existing = json.loads(target.read_text(encoding="utf-8"))
        if (existing["corpus_manifest_sha256"] != corpus_hash or existing["pairs_sha256"] != sha256_file(pairpath)
                or existing["imported_harness_sha256"] != harness_hash):
            raise RuntimeError("Existing E4 forward artifact is stale; do not overwrite")
        return existing
    if source["prefix_length"] != 128 or source["n_documents_effective"] != 256 or not source["identity_kl_exactly_zero"]:
        raise RuntimeError("V1 output does not meet the declared endpoint/sanity contract")
    if source["corpus_manifest_sha256"] != corpus_hash:
        raise RuntimeError("V1 and E4 corpus differ")
    n, batch = source["prefix_length"], source["batch"]
    reference_pairs = Path(source["pairs_path"])
    baselines = {}
    with reference_pairs.open(encoding="utf-8") as inp:
        for line in inp:
            record = json.loads(line)
            if record["arm"] in ("phase2:svd:8", "phase2:svd:16"):
                if (record["model"] != model_name or record["corpus_manifest_sha256"] != corpus_hash or record["prefix_length"] != n
                        or record["empty_row_policy"] != source["empty_row_policy"]):
                    raise RuntimeError("V1 raw baseline model/corpus/endpoint mismatch")
                key = (record["rank"], record["doc_id"])
                if key in baselines:
                    raise RuntimeError("Duplicate V1 baseline document")
                baselines[key] = record
    if len(baselines) != 512:
        raise RuntimeError("FALTA: complete 256-document paired V1 SVD8/SVD16 baselines")
    dictionary = Dictionary(n)
    matrix_result_path = dataset_paths(model_name, n)[0]
    if not matrix_result_path.exists():
        raise RuntimeError("FALTA: completed n128 E4 matrix result needed to verify the unchanged dictionary before injection")
    matrix_dictionary = json.loads(matrix_result_path.read_text(encoding="utf-8"))["dictionary"]
    if matrix_dictionary["sha256_float64_C_order"] != dictionary.digest:
        raise RuntimeError("Forward dictionary differs from the matrix experiment; do not silently change atoms")
    estimator = ForwardNamedFirst(dictionary, harness, source["empty_row_policy"])
    harness.RECON["empty_row_policy"] = source["empty_row_policy"]
    dtype = {"torch.float32": torch.float32, "torch.bfloat16": torch.bfloat16}[source["dtype"]]
    windows = torch.tensor([d["token_ids"] for d in corpus["models"][model_name]["documents"]], dtype=torch.long)
    model = AutoModelForCausalLM.from_pretrained(model_name, revision=corpus["models"][model_name]["revision"],
                                                local_files_only=True, dtype=dtype, attn_implementation="eager").to("cuda").eval()
    torch.manual_seed(SEED)
    AttentionInterface.register("p0_recon", harness.attention_forward)
    AttentionInterface.register("phase21_allocation", partial(harness.attention_forward, reconstruct_fn=estimator))
    model.set_attn_implementation("phase21_allocation")
    suffix_sanity = {}
    full = windows[:1, :n + 16].clone()
    changed = full.clone()
    changed[:, n:] = (changed[:, n:] + 7919) % model.config.vocab_size
    for rank_cap in (8, 16):
        estimator.rank_cap = rank_cap
        estimator.reset()
        a = harness.last_logits(model, full, n)
        estimator.reset()
        b = harness.last_logits(model, changed, n)
        if not torch.equal(a, b):
            raise RuntimeError("E4 suffix invariance failed")
        suffix_sanity[str(rank_cap)] = {"passed_exact": True, "max_logit_difference": float((a - b).abs().max())}
    rows = []
    if pairpath.exists():
        with pairpath.open(encoding="utf-8") as inp:
            rows = [json.loads(line) for line in inp]
        if any(r["corpus_manifest_sha256"] != corpus_hash or r["imported_harness_sha256"] != harness_hash
               or r["empty_row_policy"] != source["empty_row_policy"] or not r["identity_exact_for_batch"] for r in rows):
            raise RuntimeError("Forward resume corpus/harness/policy/identity mismatch")
    seen = {(r["svd_rank_cap"], r["doc_id"]) for r in rows}
    if len(seen) != len(rows):
        raise RuntimeError("Duplicate E4 forward record")
    validation = {}
    max_reference_nll_difference = 0.
    max_kkt = 0.
    ref = identical = other = None
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    progress(f"FORWARD START {model_name}: 256 documents, n={n}, batch={batch}, dtype={dtype}; imported V1 attention_forward/last_logits/normalize_reconstruction/kl_nll; GPU under flock")
    with pairpath.open("a", encoding="utf-8") as out:
        for start in range(0, len(windows), batch):
            sequences = windows[start:start + batch]
            targets = sequences[:, n]
            doc_ids = [d["doc_id"] for d in corpus["documents"][start:start + len(sequences)]]
            if all((k, d) in seen for k in (8, 16) for d in doc_ids):
                continue
            model.set_attn_implementation("eager")
            ref = harness.last_logits(model, sequences, n)
            _, ref_nll = harness.kl_nll(ref, ref, targets)
            harness.activate(model, ("phase2", "identity", None))
            identical = harness.last_logits(model, sequences, n)
            if not torch.equal(ref, identical):
                raise RuntimeError("E4 imported V1 identity must exactly match native eager")
            for rank_cap in (8, 16):
                if all((rank_cap, d) in seen for d in doc_ids):
                    continue
                estimator.rank_cap = rank_cap
                estimator.reset()
                model.set_attn_implementation("phase21_allocation")
                other = harness.last_logits(model, sequences, n)
                divergence, nll = harness.kl_nll(ref, other, targets)
                max_kkt = max(max_kkt, estimator.max_kkt_violation)
                arm_stats = validation.setdefault(str(rank_cap), {})
                for key, value in estimator.stats.items():
                    arm_stats[key] = max(arm_stats.get(key, 0), value) if key.startswith("max_") else arm_stats.get(key, 0) + value
                for bi, doc_id in enumerate(doc_ids):
                    if (rank_cap, doc_id) in seen:
                        continue
                    baseline = baselines[rank_cap, doc_id]
                    if baseline["target_id"] != int(targets[bi]) or baseline["document_index"] != start + bi:
                        raise RuntimeError("V1 and E4 document/token ordering differ")
                    ref_delta = abs(float(ref_nll[bi]) - baseline["reference_nll"])
                    max_reference_nll_difference = max(max_reference_nll_difference, ref_delta)
                    if ref_delta > 2e-5:
                        raise RuntimeError(f"V1 reference differs despite same corpus/batch/dtype: {ref_delta}")
                    budget = rank_cap * (2 * n + 1)
                    row = {"model": model_name, "doc_id": doc_id, "document_index": start + bi,
                           "batch_start_document_index": start, "identity_exact_for_batch": True,
                           "imported_harness_sha256": harness_hash,
                           "batch_attention_validation": dict(estimator.stats),
                           "batch_max_nnls_kkt_violation": estimator.max_kkt_violation,
                           "offset": corpus["models"][model_name]["documents"][start + bi]["offset"],
                           "prefix_length": n, "target_id": int(targets[bi]), "svd_rank_cap": rank_cap,
                           "empty_row_policy": source["empty_row_policy"],
                           "common_parameters_per_head_layer": budget,
                           "named_first_kl": float(divergence[bi]), "svd_same_budget_kl": baseline["kl"],
                           "paired_KL_named_minus_svd": float(divergence[bi]) - baseline["kl"],
                           "named_first_nll": float(nll[bi]), "svd_same_budget_nll": baseline["nll"],
                           "reference_nll": float(ref_nll[bi]), "reference_nll_difference_from_V1": ref_delta,
                           "named_argmax_agrees": bool(other[bi].argmax() == ref[bi].argmax()),
                           "named_next_token_correct": bool(other[bi].argmax() == targets[bi].to(other.device)),
                           "budget_accounting": estimator.document_costs[bi],
                           "corpus_manifest_sha256": corpus_hash}
                    out.write(json.dumps(row, allow_nan=False, separators=(",", ":")) + "\n")
                    rows.append(row)
                    seen.add((rank_cap, doc_id))
            out.flush()
            if (start + len(sequences)) % 16 == 0:
                progress(f"FORWARD {model_name}: {start+len(sequences)}/256 documents, seconds={time.perf_counter()-started:.1f}")
    # Rebuild from all raw records, including earlier validated batches after a
    # resume. Count each batch once, even though its records include each doc.
    validation = {}
    validated_batches = set()
    max_reference_nll_difference = max(r["reference_nll_difference_from_V1"] for r in rows)
    max_kkt = max(r["batch_max_nnls_kkt_violation"] for r in rows)
    for row in rows:
        key = (row["svd_rank_cap"], row["batch_start_document_index"])
        if key in validated_batches:
            continue
        validated_batches.add(key)
        stats = validation.setdefault(str(row["svd_rank_cap"]), {})
        for field, value in row["batch_attention_validation"].items():
            stats[field] = max(stats.get(field, 0), value) if field.startswith("max_") else stats.get(field, 0) + value
    result = {"model": model_name, "prefix_length": n, "dtype": str(dtype), "batch": batch,
              "empty_row_policy": source["empty_row_policy"],
              "imported_harness_sha256": harness_hash,
              "n_documents": 256, "corpus_manifest_sha256": corpus_hash,
              "V1_model_result_sha256": sha256_file(Path("out") / f"phase2_{slug(model_name)}_v2.json"),
              "V1_baseline_pairs_path": str(reference_pairs), "V1_baseline_pairs_sha256": sha256_file(reference_pairs),
              "paired_SVD_baseline": "Reused all 256 raw last-token SVD records at each rank from completed V1; identical corpus/batch/dtype/revision; eager reference NLL checked again per document",
              "dictionary": dictionary.describe(), "identity_exact_in_every_batch": True,
              "V1_KL_scale_references": {arm: source["arms"]["phase2:" + arm]
                                          for arm in ("identity", "uniform", "diagonal", "sink")},
              "suffix_invariance": suffix_sanity, "attention_validation": validation,
              "max_reference_nll_difference_from_V1": max_reference_nll_difference,
              "max_nnls_kkt_violation": max_kkt, "pairs_path": pairpath.as_posix(), "pairs_sha256": sha256_file(pairpath),
              "budgets": {}, "elapsed_seconds": time.perf_counter() - started}
    for rank_cap in (8, 16):
        records = [r for r in rows if r["svd_rank_cap"] == rank_cap]
        if len(records) != 256 or len({r["doc_id"] for r in records}) != 256:
            raise RuntimeError("Incomplete forward arm; cannot condition summary on available documents")
        docs = [r["document_index"] for r in records]
        keys = ("named_first_kl", "svd_same_budget_kl", "paired_KL_named_minus_svd", "named_first_nll", "svd_same_budget_nll")
        item = dict(zip(keys, describe_columns([[r[k] for k in keys] for r in records], docs)))
        for label, kl_key, nll_key in (("named_first", "named_first_kl", "named_first_nll"), ("svd", "svd_same_budget_kl", "svd_same_budget_nll")):
            kl_values = np.array([r[kl_key] for r in records])
            nll_values = np.array([r[nll_key] for r in records])
            draws = np.random.default_rng(SEED).integers(0, len(records), (N_BOOTSTRAP, len(records)))
            item[label + "_mean_kl"] = float(kl_values.mean())
            item[label + "_mean_kl_ci95_document_bootstrap"] = np.percentile(kl_values[draws].mean(1), [2.5, 97.5]).tolist()
            item[label + "_last_token_perplexity"] = float(np.exp(nll_values.mean()))
        item["budget_accounting"] = {
            "common_parameters_per_head_layer": rank_cap * (2 * n + 1),
            "active_atom_counts": {}, "residual_rank_counts": {},
            "actual_parameters_total": sum(r["budget_accounting"]["actual_parameters_total"] for r in records),
            "unused_parameters_total": sum(r["budget_accounting"]["unused_parameters_total"] for r in records),
            "common_cap_total": sum(r["budget_accounting"]["common_cap_total"] for r in records)}
        delta = np.array([r["paired_KL_named_minus_svd"] for r in records])
        item["paired_mean_KL_named_minus_svd"] = float(delta.mean())
        item["paired_mean_KL_difference_ci95_document_bootstrap"] = np.percentile(delta[draws].mean(1), [2.5, 97.5]).tolist()
        for key in ("active_atom_counts", "residual_rank_counts"):
            for row in records:
                for value, count in row["budget_accounting"][key].items():
                    item["budget_accounting"][key][value] = item["budget_accounting"][key].get(value, 0) + count
        result["budgets"][str(rank_cap)] = item
    write_new(target, result)
    del model, ref, identical, other
    gc.collect()
    torch.cuda.empty_cache()
    progress(f"FORWARD DONE {model_name}: {result['elapsed_seconds']:.1f}s; all 256 paired documents at caps 8/16")
    return result


def run_forward():
    v2path = Path("out/phase2_downstream_v2.json")
    if not v2path.exists():
        raise RuntimeError("FALTA: out/phase2_downstream_v2.json; wait for the corrected harness before GPU work")
    v2hash = sha256_file(v2path)
    v2 = json.loads(v2path.read_text(encoding="utf-8"))
    required_result = {"prefix_length", "n_documents_effective", "identity_kl_exactly_zero", "batch", "dtype",
                       "corpus_manifest_sha256", "pairs_path", "arms", "empty_row_policy"}
    unavailable = [m for m in MODELS if m not in v2 or not required_result.issubset(v2[m]) or "error" in v2[m]]
    if unavailable:
        raise RuntimeError("FALTA: complete corrected V1 results for " + ", ".join(unavailable))
    import phase2_downstream as harness
    harness_hash = sha256_file("phase2_downstream.py")
    required = ("attention_forward", "normalize_reconstruction", "last_logits", "kl_nll", "activate")
    if any(not hasattr(harness, name) for name in required):
        raise RuntimeError("Corrected V1 harness lacks its required reusable API")
    policies = {v2[m]["empty_row_policy"] for m in MODELS}
    if len(policies) != 1:
        raise RuntimeError("V1 uses different empty-row policies across models; inspect before claiming a uniform comparison")
    estimator_checks = check_forward_estimator(harness, next(iter(policies)))
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    results = {m: run_forward_model(m, v2, harness, corpus, harness_hash) for m in MODELS}
    if sha256_file("phase2_downstream.py") != harness_hash:
        raise RuntimeError("V1 harness changed during E4; preserve artifacts and audit")
    write_new("out/phase21_allocation_forward.json", {
        "_meta": {"V1_result_path": v2path.as_posix(), "V1_result_sha256": v2hash,
                  "imported_harness_path": "phase2_downstream.py", "imported_harness_sha256": harness_hash,
                  "common_budget": "SVD K costs K(2n+1); named_first residual rank is floor((K(2n+1)-2*active)/(2n+1)) per head/layer, normally K-1",
                  "budget_applies_to": "Representation before the shared causal projection/clamp/row normalization; the harness materializes dense attention, with no inference speedup claimed",
                  "unused_budget_reported": True, "last_token_only": True, "n_documents_per_model": 256,
                  "nnls_dtype": "float64 CPU", "lowrank_SVD_dtype": "float32 GPU, same as V1 SVD",
                  "causality_and_normalization": "Imported V1 attention_forward and normalize_reconstruction; no copied mask logic",
                  "estimator_checks": estimator_checks,
                  "empty_row_policy_imported_from_V1": next(iter(policies)),
                  "statistics": metadata()["aggregation"], "GPU_command": "flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase21_allocation.py forward"},
        **results})


def assemble(allow_missing_forward=False, output="out/phase21_allocation.json"):
    missing = [str(dataset_paths(m, n)[0]) for m in MODELS for n in (128, 256) if not dataset_paths(m, n)[0].exists()]
    forward = Path("out/phase21_allocation_forward.json")
    if not forward.exists() and not allow_missing_forward:
        missing.append(str(forward))
    if missing:
        raise RuntimeError("FALTA: " + ", ".join(missing))
    if not forward.exists() and Path("out/phase2_downstream_v2.json").exists():
        raise RuntimeError("V1 aggregate now exists: run the authorized forward experiment before assembling")
    destination = Path(output)
    if (destination.parent.resolve() != Path("out").resolve() or destination.suffix != ".json"
            or not destination.name.startswith(("phase21_", "allocation_"))):
        raise ValueError("Aggregate destination must be a new phase21_/allocation_ JSON under out/")
    results = {model: {str(n): json.loads(dataset_paths(model, n)[0].read_text(encoding="utf-8"))
                       for n in (128, 256)} for model in MODELS}
    ready = json.loads(Path("data/attn/READY").read_text(encoding="utf-8"))
    expected = {(d["model"], d["n"]): d["n_matrices"] for d in ready["datasets"]}
    audit = {"n_populations": 0, "n_matrices": 0, "n_convention_rank_fits": 0,
             "input_invalid_matrices": 0, "final_cutoff_exact_ties": 0,
             "final_cutoff_numerical_ties": 0, "final_cutoff_positive_numerical_ties": 0}
    for model in MODELS:
        for n in (128, 256):
            result = results[model][str(n)]
            if result["n_instances"] != expected[model, n] or result["n_documents"] != 64:
                raise RuntimeError("Final audit: population differs from READY")
            if result["manifest_sha256"] != sha256_file(sample_paths(model, n)[1]):
                raise RuntimeError("Final audit: manifest changed")
            if result["dictionary"]["n_atoms"] != 17:
                raise RuntimeError("Final audit: source dictionary changed; inspect, do not silently adapt")
            audit["n_populations"] += 1
            audit["n_matrices"] += result["n_instances"]
            audit["input_invalid_matrices"] += result["input_validation"]["invalid_matrices"]
            for convention in CONVENTIONS:
                for rank in RANKS:
                    item = result["conventions"][convention][str(rank)]
                    audit["n_convention_rank_fits"] += result["n_instances"]
                    for key in ("exact_tie", "numerical_tie", "positive_numerical_tie"):
                        audit["final_cutoff_" + key.replace("tie", "ties")] += item["cutoff_ties"][key]
                    if any(metric["n_instances"] != result["n_instances"] or metric["n_documents"] != 64
                           for metric in item["metrics"].values()):
                        raise RuntimeError("Final audit: conditional-subset aggregate")
    if audit["n_matrices"] != ready["total_matrices"] or audit["input_invalid_matrices"] != 0:
        raise RuntimeError("Final audit: incomplete or invalid matrix data")
    audit["dictionary_hashes_by_length"] = {}
    for n in (128, 256):
        digests = {results[m][str(n)]["dictionary"]["sha256_float64_C_order"] for m in MODELS}
        if len(digests) != 1 or next(iter(digests)) != Dictionary(n).digest:
            raise RuntimeError("Final audit: dictionary changed across models or differs from current source")
        audit["dictionary_hashes_by_length"][str(n)] = next(iter(digests))
    if forward.exists():
        downstream = json.loads(forward.read_text(encoding="utf-8"))
        status = "complete"
    else:
        status = "matrix_complete_forward_waiting_for_external_V1"
        downstream = {"status": "FALTA", "required_baseline": "out/phase2_downstream_v2.json",
                      "reason": "Required external V1 aggregate is absent. Per the requested dependency, no injection or last-token KL was run, and no alternative harness/policy or old KL was substituted.",
                      "expected_results_path": forward.as_posix(), "models_pending": MODELS,
                      "last_token_KL_values": None,
                      "resume_after_V1_exists": [
                          "flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase21_allocation.py forward",
                          ".venv/Scripts/python.exe -B phase21_allocation.py assemble --output out/phase21_allocation_complete.json"]}
    final = {"_meta": metadata(), "status": status, "matrices": results,
             "forward": downstream, "integrity_audit": audit}
    write_new(destination, final)
    if status == "complete":
        progress(f"COMPLETE {destination}; all 12 populations and downstream paired comparison present")
    else:
        progress(f"MATRICES COMPLETE {destination}; FALTA: external out/phase2_downstream_v2.json and last-token KL; all 12 populations retained")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "check-adapter", "matrices", "forward", "assemble"))
    parser.add_argument("--models", nargs="+", default=MODELS, choices=MODELS)
    parser.add_argument("--lengths", nargs="+", type=int, default=[128, 256], choices=[128, 256])
    parser.add_argument("--workers", type=int, default=3, choices=[1, 2, 3])
    parser.add_argument("--allow-missing-forward", action="store_true",
                        help="assemble only: mark KL FALTA if the required external V1 aggregate is still absent; every matrix population must be complete")
    parser.add_argument("--output", default="out/phase21_allocation.json",
                        help="assemble only: new aggregate file; never overwrite an existing result")
    args = parser.parse_args()
    if args.command == "check":
        check()
    elif args.command == "check-adapter":
        check_adapter_cpu()
    elif args.command == "matrices":
        jobs = [(m, n) for n in args.lengths for m in args.models]
        progress(f"FROZEN run: T={ITERATIONS}, ranks={RANKS}, seed={SEED}, bootstrap={N_BOOTSTRAP}, every manifest instance; workers={args.workers}, threads=4")
        if args.workers == 1:
            for job in jobs:
                run_dataset(job)
        else:
            with ProcessPoolExecutor(max_workers=args.workers) as pool:
                for path in pool.map(run_dataset, jobs):
                    print(f"SAVED {path}", flush=True)
    elif args.command == "forward":
        run_forward()
    else:
        assemble(args.allow_missing_forward, args.output)


if __name__ == "__main__":
    main()
