"""E9 immutable protocol, CPU matrix experiment and document-level inference."""
import phase50_als as als  # Thread limits and datasets before torch.
import argparse
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from itertools import combinations
import json
from pathlib import Path
import time
import numpy as np
import torch
from scipy.stats import rankdata, wilcoxon
import phase2_downstream as harness
from phase21_allocation import Dictionary
from phase24_p0_metrics import describe
from sampling import MODELS, CORPUS_PATH, load_sample, sample_paths, sha256_file, slug, write_json_new

torch.set_num_threads(4)
PROTOCOL = Path("out/phase50_protocol.json")
ARMS = ("svd_K", "masked_K", "named_plus_masked", "named_plus_svd", "svd_K_diag_exact", "masked_K_diag_exact")
MATRIX_COMPARISONS = list(combinations(ARMS[:4], 2))
FORWARD_COMPARISONS = [("masked_K", "named_plus_svd"), ("named_plus_masked", "named_plus_svd"), ("named_plus_masked", "masked_K")]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def jsonl(path):
    with Path(path).open(encoding="utf-8") as inp:
        return [json.loads(line) for line in inp if line.strip()]


def freeze():
    if PROTOCOL.exists():
        return read(PROTOCOL)
    ch = sha256_file(CORPUS_PATH)
    corpus = read(CORPUS_PATH)
    baseline = read("out/phase2_downstream_v2.json")
    result = {"created_UTC": datetime.now(timezone.utc).isoformat(), "experiment": "E9", "seed": 50,
              "models": MODELS, "K": [8, 16], "n": 128, "n_articles_forward": 256,
              "ALS": {"sweeps": als.SWEEPS, "early_stop": False, "dtype": "float64_CPU_and_GPU",
                      "initialization": "truncated ordinary float64 SVD; singular values split by square root",
                      "objective": "min ||tril(A - U V^T)||_F^2; residual A-S for named_plus_masked",
                      "gauge": "QR of both factors then SVD of the small product each sweep; balanced factors; algebraically preserves U V^T",
                      "LS_rcond": als.LS_RCOND, "Gram_min_eigenvalue_ratio": als.GRAM_MIN_RATIO,
                      "solver": "well-conditioned Gram solve plus observed-residual refinement; otherwise direct design SVD least squares",
                      "numerical_sweep_policy": "If objective increases by >1e-9*max(1,previous), retry whole sweep with direct LS; if still increasing retain previous finite factors and record rejection; always attempt all 200 sweeps",
                      "convergence": "normalized gradient<=1e-6 AND (last20 relative loss change<=1e-7 OR relative error<=1e-6); rejected sweeps count as nonconverged unless error<=1e-6",
                      "checkpoints": list(als.CHECKPOINTS)},
              "matrix_sampling": {"n_per_model": 384, "n_documents": 64, "n_per_document": 6,
                                  "design": "six equal-width layer strata per document; offset cycles systematically over all layers across documents; uniformly random archived head within chosen document/layer, seed=50+model_index",
                                  "selection_fixed_before_fits": True},
              "diagonal": {"criterion": "median over ALL archived matrices of each head of max(mean-row offset0 mass,mean-row offset1 mass)) > 0.9",
                           "threshold": 0.9, "offset1_first_row": "zero (no previous token); both sums divided by n=128",
                           "offset1_does_not_include_wraparound": True},
              "storage": {"cap": "K*(2n+1)", "a_d": "SVD cost K*(2n+1); named S cost 2*active_atoms plus (K-1)*(2n+1)",
                          "b_c": "masked cost 2*n*K; named S cost 2*active_atoms plus 2*n*(K-1)",
                          "e_f": "same rank cap on reconstructed heads; identical heads kept exact in both ablations (extra exact-head storage, not a globally fixed-cap compression claim)"},
              "statistics": {"primary": "phase24.describe instance median; 2000 whole-document bootstrap samples, seed0",
                             "paired": "per-instance differences -> median per document -> two-sided Wilcoxon, wilcox zeros, asymptotic p; signed rank-biserial positive favors right arm",
                             "forward_comparisons": FORWARD_COMPARISONS, "forward_Holm_family": 36,
                             "matrix_comparisons": MATRIX_COMPARISONS, "matrix_Holm_family": 144,
                             "matrix_metrics": ["relative_frobenius_after_causal_normalization", "mean_row_TV_after_causal_normalization"],
                             "matrix_reference": "fp16 archived A normalized by imported harness in float64; raw pre-normalization objective also retained"},
              "sanities": {"planted": "n=128, ranks8/16, seed5001, positive lognormal(0,0.7) factors, row-normalized; 200 sweeps, relative recovery tolerance 0.01 declared before running",
                           "CPU_GPU": "32 matrices/model, first selected matrix in documents0..31, both K and plain/named residual; compare GPU double against independent CPU double fits and identical initial factors; report maximum raw and normalized error difference",
                           "CPU_GPU_error_tolerance": 0.01,
                           "baseline_reuse": "all256 article identities/targets/batches/dtypes/reference NLL matched; V1 SVD observations agree exactly with E4 reused SVD; rerun firstbatch all K a/d with max KL/NLL discrepancy<=2e-5",
                           "identity": "native eager and imported identity logits exactly equal; KL exactly0"},
              "corpus_manifest_sha256": ch, "harness_sha256_at_freeze": sha256_file("phase2_downstream.py"),
              "source_files": {}, "datasets": {}}
    for mi, model in enumerate(MODELS):
        a, manifest = load_sample(model, 128)
        if manifest["corpus_manifest_sha256"] != ch:
            raise ValueError("Archive/corpus mismatch")
        instances = manifest["instances"]; rng = np.random.default_rng(50 + mi)
        indices = []
        for doc in range(64):
            phase = (doc % manifest["n_layers"]) / manifest["n_layers"]
            layers = np.floor((np.arange(6) + phase) * manifest["n_layers"] / 6).astype(int)
            for layer in layers:
                candidates = [i for i, r in enumerate(instances) if r["document_index"] == doc and r["layer"] == layer]
                indices.append(int(rng.choice(candidates)))
        if len(indices) != 384 or len(set(indices)) != 384:
            raise ValueError("Invalid predeclared matrix selection")
        layer_counts = {str(l): sum(instances[i]["layer"] == l for i in indices) for l in range(manifest["n_layers"])}
        if min(layer_counts.values()) <= 0:
            raise ValueError("Stratified subset must represent every layer")
        head_stats = []
        for layer in range(manifest["n_layers"]):
            for head in range(manifest["n_heads"]):
                selected = [i for i, r in enumerate(instances) if (r["layer"], r["head"]) == (layer, head)]
                if not selected:
                    raise ValueError("Diagonal-head classification has a missing head")
                mats = a[selected].astype(np.float64)
                d0 = mats.diagonal(axis1=-2, axis2=-1).sum(-1) / 128
                d1 = mats.diagonal(offset=-1, axis1=-2, axis2=-1).sum(-1) / 128
                median = float(np.median(np.maximum(d0, d1)))
                head_stats.append({"layer": layer, "head": head, "n_matrices": len(selected),
                                   "median_max_offset_mass": median, "median_offset0_mass": float(np.median(d0)),
                                   "median_offset1_mass": float(np.median(d1)), "exempt": median > 0.9})
        result["datasets"][model] = {"archive_sha256": manifest["npz_sha256"],
                                    "manifest_sha256": sha256_file(sample_paths(model,128)[1]),
                                    "matrix_archive_indices": indices, "layer_counts": layer_counts,
                                    "GPU_validation_indices": indices[::6][:32], "all_head_statistics": head_stats,
                                    "diagonal_heads": [[s["layer"], s["head"]] for s in head_stats if s["exempt"]],
                                    "dtype": baseline[model]["dtype"], "batch": baseline[model]["batch"]}
        for path in (baseline[model]["pairs_path"], f"out/pairs/phase21_allocation_forward_{slug(model)}_n128_v2.jsonl",
                     f"out/pairs/phase21_allocation_core_{slug(model)}_n128_v2.jsonl"):
            result["source_files"][path] = sha256_file(path)
        if len(corpus["models"][model]["documents"]) != 256:
            raise ValueError("Forward requires all256 articles")
    write_json_new(PROTOCOL, result)
    print(f"FROZEN {PROTOCOL}; 200 sweeps, double, 384 matrices/model, no result inspected", flush=True)
    for model in MODELS:
        print(model, "exempt", result["datasets"][model]["diagonal_heads"], flush=True)
    return result


def paired(values, docs):
    delta = np.asarray(values, dtype=np.float64); docs = np.asarray(docs)
    if not np.isfinite(delta).all():
        raise ValueError("Nonfinite paired difference")
    medians = np.array([np.median(delta[docs == d]) for d in np.unique(docs)])
    nz = medians[medians != 0]
    if len(nz):
        ranks = rankdata(np.abs(nz)); plus = float(ranks[nz > 0].sum()); minus = float(ranks[nz < 0].sum())
        test = wilcoxon(medians, alternative="two-sided", zero_method="wilcox", method="asymptotic")
        stat, p = float(test.statistic), float(test.pvalue); effect = (plus-minus)/(plus+minus)
    else:
        stat = plus = minus = effect = 0.; p = 1.
    return {"difference": describe(delta, docs), "document_median_differences": medians.tolist(),
            "n_documents": len(medians), "statistic": stat, "p_two_sided": p,
            "W_positive": plus, "W_negative": minus, "rank_biserial": effect,
            "positive_difference_favors": "right arm", "fraction_left_lower": float(np.mean(delta < 0))}


def holm(tests):
    order = sorted(range(len(tests)), key=lambda i: tests[i]["p_two_sided"])
    running = 0.
    for j, i in enumerate(order):
        running = max(running, (len(tests)-j) * tests[i]["p_two_sided"])
        tests[i]["p_Holm"] = min(1., running)
        tests[i]["Holm_family_size"] = len(tests)


def normalize_cpu(product, original):
    stats = {}
    rec = harness.normalize_reconstruction(torch.from_numpy(np.ascontiguousarray(product)),
                                          torch.from_numpy(original), stats, "uniform", cast_to_original=False)
    return rec.numpy(), stats


def metrics(product, a, reference):
    rec, stats = normalize_cpu(product, a)
    return {"frobenius": float(np.linalg.norm(rec-reference)/np.linalg.norm(reference)),
            "TV": float(np.abs(rec-reference).sum(-1).mean()/2),
            "raw_causal_frobenius": float(np.linalg.norm(np.tril(product)-a)/max(np.linalg.norm(a), np.finfo(float).tiny)),
            "raw_unmasked_frobenius": float(np.linalg.norm(product-a)/max(np.linalg.norm(a), np.finfo(float).tiny)),
            "normalization_validation": stats}


def summarize_diagnostics(infos):
    return {"n_fits": len(infos), "converged": sum(d["converged"] for d in infos),
            "CPU_reference_fallback_fits":sum(bool(d.get("numerical_fallback",False)) for d in infos),
            "discarded_GPU_attempt_sweeps":sum(d.get("discarded_GPU_attempt_sweeps",0) for d in infos),
            "maximum_discarded_GPU_QR_product_error":max((d.get("uncorrected_GPU",{}).get("maximum_QR_observed_product_error",0.) for d in infos),default=0.),
            "fits_with_rejections": sum(bool(d["rejected_sweeps"]) for d in infos),
            "rejected_sweeps": sum(len(d["rejected_sweeps"]) for d in infos),
            "maximum_absolute_factor": max(d["maximum_absolute_factor"] for d in infos),
            "maximum_dynamic_range": max(d["factor_dynamic_range"] for d in infos),
            "maximum_QR_observed_product_error": max(d["maximum_QR_observed_product_error"] for d in infos),
            "median_initial_relative": float(np.median([d["initial_relative"] for d in infos])),
            "median_final_relative": float(np.median([d["final_relative"] for d in infos])),
            "median_last20_relative_objective_change": float(np.median([d["last20_relative_objective_change"] for d in infos])),
            "median_history": [{"sweep": s, "relative": float(np.median([next(x["relative"] for x in d["history"] if x["sweep"] == s) for d in infos]))} for s in als.CHECKPOINTS]}


def matrix_summary(model, rows, pairpath, elapsed):
    result = {"model": model, "n": 128, "n_matrices": 384, "n_documents": 64,
              "protocol_sha256": sha256_file(PROTOCOL), "pairs_path": str(pairpath), "pairs_sha256": sha256_file(pairpath),
              "elapsed_seconds": elapsed, "K": {}}
    for k in (8, 16):
        group = [r for r in rows if r["K"] == k]
        if len(group) != 384:
            raise ValueError("Incomplete matrix arm; no conditional summary")
        docs = [r["document_index"] for r in group]
        out = {"arms": {}, "paired": {}}
        for arm in ARMS[:4]:
            out["arms"][arm] = {m: describe([r["arms"][arm][m] for r in group], docs) for m in ("frobenius", "TV", "raw_causal_frobenius")}
            if arm in ("masked_K", "named_plus_masked"):
                out["arms"][arm]["ALS"] = summarize_diagnostics([r["arms"][arm]["ALS"] for r in group])
        for left, right in MATRIX_COMPARISONS:
            out["paired"][left+"__minus__"+right] = {m: paired([r["arms"][left][m]-r["arms"][right][m] for r in group], docs) for m in ("frobenius", "TV")}
        result["K"][str(k)] = out
    return result


def run_matrix(model):
    protocol = read(PROTOCOL); cfg = protocol["datasets"][model]
    target = Path(f"out/phase50_matrix_{slug(model)}.json")
    pairpath = Path(f"out/pairs/phase50_matrix_{slug(model)}.jsonl")
    if target.exists():
        previous = read(target)
        if previous["protocol_sha256"] != sha256_file(PROTOCOL) or previous["pairs_sha256"] != sha256_file(pairpath):
            raise ValueError("Existing matrix result mismatch")
        return str(target)
    a_all, manifest = load_sample(model, 128); dictionary = Dictionary(128)
    source = Path(f"out/pairs/phase21_allocation_core_{slug(model)}_n128_v2.jsonl")
    expected_ids = {manifest["instances"][i]["instance_id"] for i in cfg["matrix_archive_indices"]}
    prior = {}
    with source.open(encoding="utf-8") as inp:
        for line in inp:
            row = json.loads(line)
            if row["instance_id"] in expected_ids:
                prior[row["instance_id"]] = row
    if len(prior) != 384:
        raise ValueError("Missing E4 matrix references")
    rows = jsonl(pairpath) if pairpath.exists() else []
    seen = {(r["archive_index"], r["K"]) for r in rows}
    if len(rows) != len(seen) or any(r["protocol_sha256"] != sha256_file(PROTOCOL) for r in rows):
        raise ValueError("Invalid matrix resume records")
    started = time.perf_counter(); ph = sha256_file(PROTOCOL)
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    with pairpath.open("a", encoding="utf-8") as out:
        for ordinal, idx in enumerate(cfg["matrix_archive_indices"]):
            if all((idx, k) in seen for k in (8,16)):
                continue
            a = a_all[idx].astype(np.float64); ref, _ = normalize_cpu(a, a)
            named, coef, kkt = dictionary.project(a); res = a-named
            fu, fs, fv = np.linalg.svd(a, full_matrices=False)
            ru, rs, rv = np.linalg.svd(res, full_matrices=False)
            for k in (8,16):
                if (idx, k) in seen:
                    continue
                if 2*np.count_nonzero(coef > 0) + (k-1)*257 > k*257:
                    raise ValueError("Named-channel common budget exceeded")
                svd = (fu[:,:k]*fs[:k]) @ fv[:k]
                ns = named + (ru[:,:k-1]*rs[:k-1]) @ rv[:k-1]
                arms = {"svd_K": metrics(svd,a,ref), "named_plus_svd": metrics(ns,a,ref)}
                old = prior[manifest["instances"][idx]["instance_id"]]
                raw_diff = {"svd": abs(arms["svd_K"]["raw_unmasked_frobenius"]-old["capacity"][str(k)]["svd_error"]),
                            "named": abs(arms["named_plus_svd"]["raw_unmasked_frobenius"]-old["capacity"][str(k)]["named_first_error"]),
                            "coefficients": float(np.max(np.abs(coef-np.array(old["named_first_coefficients"]))))}
                if max(raw_diff.values()) > 2e-9:
                    raise ValueError(f"E4 matrix reconstruction mismatch: {raw_diff}")
                for arm, target_a, rank in (("masked_K", a, k), ("named_plus_masked", res, k-1)):
                    product, info = als.fit_cpu(target_a,rank)
                    arms[arm] = {**metrics(product+(named if arm=="named_plus_masked" else 0),a,ref), "ALS": info}
                row = {**manifest["instances"][idx], "model": model, "archive_index": idx, "K": k,
                       "protocol_sha256": ph, "arms": arms, "E4_raw_reconstruction_differences": raw_diff,
                       "named_projection_KKT": kkt, "active_atoms": int(np.count_nonzero(coef>0)),
                       "cap": k*257, "masked_parameters": 256*k,
                       "named_masked_parameters": 2*int(np.count_nonzero(coef>0))+256*(k-1)}
                out.write(json.dumps(row,allow_nan=False,separators=(",",":"))+"\n"); out.flush()
                rows.append(row); seen.add((idx,k))
            if (ordinal+1)%8 == 0:
                print(f"MATRIX {model} {ordinal+1}/384 {time.perf_counter()-started:.1f}s", flush=True)
    result = matrix_summary(model, rows, pairpath, time.perf_counter()-started)
    write_json_new(target,result)
    print(f"MATRIX DONE {model}", flush=True)
    return str(target)


def controls():
    path = Path("out/phase50_CPU_controls.json")
    if path.exists():
        return read(path)
    rng = np.random.default_rng(5001); rows = []
    for k in (8,16):
        u, v = rng.lognormal(0,.7,(128,k)), rng.lognormal(0,.7,(128,k))
        a = np.tril(u @ v.T); a /= a.sum(-1,keepdims=True)
        product, info = als.fit_cpu(a,k)
        error = float(np.linalg.norm(np.tril(product)-a)/np.linalg.norm(a))
        rows.append({"n":128,"K":k,"relative_error":error,"passed":error<=.01,"ALS":info})
        print("PLANTED",k,error,"seconds",info["seconds"],flush=True)
    # A cached, rectangular query checks offset masking and empty rows through
    # the exact imported normalizer; no alternate causal implementation.
    original = torch.ones(2,3,5,dtype=torch.float64)
    st = {}; p = harness.normalize_reconstruction(torch.zeros_like(original),original,st,"uniform")
    if not torch.equal(p[0,0],torch.tensor([1/3,1/3,1/3,0,0],dtype=torch.float64)):
        raise AssertionError("Imported cached-offset uniform completion failed")
    result = {"protocol_sha256":sha256_file(PROTOCOL),"planted":rows,"all_passed":all(r["passed"] for r in rows),
              "imported_offset_empty_row_control":st}
    write_json_new(path,result)
    if not result["all_passed"]:
        raise AssertionError("Planted control failed at fixed200 sweeps; preserve evidence, do not change sweeps")
    return result


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("action",choices=("freeze","controls","matrices","matrix-one"))
    ap.add_argument("--model",choices=MODELS); ap.add_argument("--workers",type=int,default=3)
    args = ap.parse_args()
    if args.action == "freeze":
        freeze()
    elif args.action == "controls":
        controls()
    elif args.action == "matrix-one":
        run_matrix(args.model)
    else:
        if not read("out/phase50_CPU_controls.json")["all_passed"]:
            raise ValueError("Positive control required")
        with ProcessPoolExecutor(max_workers=min(3,args.workers)) as pool:
            paths = list(pool.map(run_matrix,MODELS))
        results = [read(p) for p in paths]
        tests = [test for result in results for v in result["K"].values() for metrics_ in v["paired"].values() for test in metrics_.values()]
        if len(tests) != 144:
            raise ValueError("Matrix Holm family incomplete")
        holm(tests)
        write_json_new("out/phase50_matrix_summary.json",{"protocol_sha256":sha256_file(PROTOCOL),"models":{r["model"]:r for r in results},"Holm_family":144})


if __name__ == "__main__":
    main()
