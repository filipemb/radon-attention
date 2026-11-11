"""E4 v2: instance medians, document-block inference and symmetric budgets.

The audited v1 decompositions are immutable inputs. Reaggregate their exact raw
values; evaluate the new named-first storage comparison from their full spectra.
No v1 output or existing source is modified.
"""
import os
for _key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "4"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import datasets  # Before torch, including indirect imports.
import argparse
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import time
import numpy as np
from scipy.stats import wilcoxon, rankdata
import torch
from sampling import MODELS, CORPUS_PATH, load_sample, sample_paths, sha256_file, slug
from phase24_p0_metrics import describe  # User's project-wide primary estimator.
from phase06_profiled_lines import omp_profiled, precompute_band_norms, atom_vector
import phase21_allocation as v1

torch.set_num_threads(4)
RANKS = (0, 1, 2, 4, 8, 16)
BUDGET_RANKS = (1, 2, 4, 8, 16)
SEED = 0
N_BOOTSTRAP = 2000
ALT = "algorithm_1_5_iterations"
CONVENTIONS = ("named_first", "lowrank_first", ALT)
SOURCE_CONVENTION = {"named_first": "named_first", "lowrank_first": "lowrank_first", ALT: "alternating"}
LABELS = {"named_first": "named_first", "lowrank_first": "lowrank_first", ALT: "5 iterações do Algoritmo 1"}
LOG = Path("out/_rerun_logs/phase21_allocation_v2_progress.md")
RUN_PATH = Path("out/phase21_allocation_v2_run.json")
WAIT_START = "2026-11-09T21:11:20+00:00"
ALLOCATION_FIELDS = ("named_norm_ratio", "named_energy_ratio", "cross_energy_ratio",
                     "named_only_explained_energy", "relative_error", "n_active",
                     "nnls_kkt_violation", "nnls_complementarity", "lowrank_energy_ratio")


def log(message):
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as out:
        out.write(f"- {stamp} | {message}\n")
    print(f"E4v2 {message}", flush=True)


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as out:
        json.dump(value, out, ensure_ascii=False, indent=2, allow_nan=False)
        out.write("\n")


def freeze():
    if RUN_PATH.exists():
        return json.loads(RUN_PATH.read_text(encoding="utf-8"))
    start = datetime.fromisoformat(WAIT_START)
    result = {"schema_version": 2, "waiting_for_V1_started_UTC": start.isoformat(),
              "waiting_for_V1_deadline_UTC": (start + timedelta(hours=3)).isoformat(),
              "wait_limit_hours": 3, "seed": SEED, "n_bootstrap": N_BOOTSTRAP,
              "allocation_residual_ranks": list(RANKS), "capacity_budget_ranks_K": list(BUDGET_RANKS),
              "allocation_convention_labels": LABELS,
              "allocation_index_note": "r remains the residual rank for the audited allocation sweep, including the 17/9984 Alg1 diagnostic at r=8. Capacity uses the separate budget index K and residual rank K-1.",
              "capacity": {"common_cap": "B=K*(2n+1)", "named_first_rank": "q=K-1 (fixed, not tuned)",
                           "named_first_cost": "2*count(c>0)+(K-1)*(2n+1)",
                           "feasibility": "Require cost<=B on every instance; otherwise stop, never condition the median on feasible instances. With 17 atoms and n>=128, 2*m<=34<2n+1, hence every instance fits.",
                           "slack": "B-actual_cost, reported per instance and in aggregates",
                           "svd_cost": "K*(2n+1)", "line_atom_cost": 2,
                           "line_dictionary_size": "2n+7: n causal columns, n offset diagonals, seven profiled bands",
                           "line_steps_allowed": "min(floor(B/2),2n+7), finite-dictionary limit and unused cap explicit",
                           "no_SVD_rank_0_comparison": True},
              "statistics": {"primary": "Imported phase24_p0_metrics.describe: median across all instances; percentile 95% CI from 2000 resampled whole-document blocks",
                             "primary_source_sha256": sha256_file("phase24_p0_metrics.py"),
                             "secondary": "Mean of document means, plus median/IQR of document means and their bootstrap intervals, all explicitly secondary",
                             "paired_test": "Compute per-instance error difference; reduce each document to its median difference; two-sided Wilcoxon signed-rank across all 64 documents (zero_method=wilcox, asymptotic p)",
                             "effect": "rank-biserial=(W_positive-W_negative)/(W_positive+W_negative); positive method-minus-SVD difference favors SVD",
                             "paired_median_CI": "Same imported describe on all paired instance differences, resampling whole documents",
                             "fraction_SVD_wins": "Strict error_SVD<error_method on all head-document instances; also distinct (layer,head) fraction after within-head document median; exact ties and sensitivity at 1e-12 separately"},
              "ALT": {"label": LABELS[ALT], "T": 5, "L_initial": 0, "early_stopping": False,
                      "recorded_diagnostic_n128_r8": {"criterion_met": 17, "n_instances": 9984},
                      "claim": "Five fixed iterations; no claim of convergence/global optimum"},
              "immutable_v1_source": "out/pairs/phase21_allocation_{model}_n{n}.jsonl; independently audited values reused exactly",
              "new_files_only": True}
    write_new(RUN_PATH, result)
    log(f"FROZEN v2; primary=instance median, block bootstrap=2000 docs; deadline V1={(start+timedelta(hours=3)).isoformat()}; K={BUDGET_RANKS}; q=K-1")
    return result


def summarize(values, docs):
    a, docs = np.asarray(values, dtype=np.float64), np.asarray(docs)
    result = describe(a, docs, seed=SEED)
    result["iqr"] = result["p75"] - result["p25"]
    block_means = np.array([a[docs == doc].mean() for doc in np.unique(docs)])
    draws = np.random.default_rng(SEED).integers(0, len(block_means), (N_BOOTSTRAP, len(block_means)))
    result["secondary_document_means"] = {
        "mean": float(block_means.mean()), "median": float(np.median(block_means)),
        "p25": float(np.percentile(block_means, 25)), "p75": float(np.percentile(block_means, 75)),
        "mean_ci95_document_bootstrap": np.percentile(block_means[draws].mean(1), [2.5,97.5]).tolist(),
        "median_ci95_document_bootstrap": np.percentile(np.median(block_means[draws], axis=1), [2.5,97.5]).tolist()}
    return result


def paired(differences, rows):
    delta = np.asarray(differences, dtype=np.float64)
    docs = np.array([r["document_index"] for r in rows])
    unique = np.unique(docs)
    doc_medians = np.array([np.median(delta[docs == doc]) for doc in unique])
    nonzero = doc_medians[doc_medians != 0]
    if len(nonzero) == 0:
        Wplus = Wminus = statistic = effect = 0.
        pvalue = 1.
        method = "all 64 document medians exactly zero: explicit degenerate null, no NaN replacement"
    else:
        ranks = rankdata(np.abs(nonzero), method="average")
        Wplus = float(ranks[nonzero > 0].sum())
        Wminus = float(ranks[nonzero < 0].sum())
        effect = (Wplus - Wminus) / (Wplus + Wminus)
        test = wilcoxon(doc_medians, alternative="two-sided", zero_method="wilcox", method="asymptotic")
        statistic, pvalue = float(test.statistic), float(test.pvalue)
        method = "scipy.stats.wilcoxon; two-sided; zero_method=wilcox; method=asymptotic"
    if not np.isfinite([Wplus,Wminus,statistic,effect,pvalue]).all():
        raise ArithmeticError("Nonfinite paired test; no replacement or omitted document")
    indicators = (delta > 0).astype(float)
    doc_fractions = np.array([indicators[docs == doc].mean() for doc in unique])
    draws = np.random.default_rng(SEED).integers(0, len(unique), (N_BOOTSTRAP, len(unique)))
    heads = sorted({(r["layer"],r["head"]) for r in rows})
    head_medians = [float(np.median([d for d,r in zip(delta,rows) if (r["layer"],r["head"]) == head])) for head in heads]
    return {"paired_instance_difference": summarize(delta, docs),
            "document_median_differences": [{"document_index":int(doc), "median_difference":float(v)} for doc,v in zip(unique,doc_medians)],
            "wilcoxon": {"n_documents": len(unique), "n_zero_document_medians": int(len(unique)-len(nonzero)),
                         "statistic": statistic, "p_two_sided": pvalue, "method": method,
                         "W_positive": Wplus, "W_negative": Wminus, "rank_biserial": effect,
                         "positive_difference_favors": "right-hand comparison arm (SVD for method-minus-SVD)"},
            "right_arm_win_fraction_instances": float(indicators.mean()),
            "right_arm_win_fraction_instances_ci95_document_bootstrap": np.percentile(doc_fractions[draws].mean(1),[2.5,97.5]).tolist(),
            "n_exact_tied_instances": int(np.count_nonzero(delta == 0)),
            "right_arm_win_fraction_instances_with_margin_1e_12": float(np.mean(delta > 1e-12)),
            "distinct_head_secondary": {"aggregation":"median difference over sampled documents for each distinct (layer,head)",
                                        "n_heads":len(heads), "right_arm_win_fraction":float(np.mean(np.asarray(head_medians)>0))}}


def core_paths(model, n):
    return (Path("out") / f"phase21_allocation_v2_core_{slug(model)}_n{n}.json",
            Path("out/pairs") / f"phase21_allocation_core_{slug(model)}_n{n}_v2.jsonl")


def convert_record(old):
    n = old["n"]
    norm = old["attention_frobenius_norm"]
    sA = np.asarray(old["attention_singular_values"])
    sR = np.asarray(old["named_first_projection"]["residual_A_minus_S"]["singular_values"])
    coef = old["named_first_projection"]["coefficients"]
    active = int(np.count_nonzero(np.asarray(coef)>0))
    row = {k:old[k] for k in ("instance_id","model","document_index","doc_id","layer","head","offset","n","dictionary_sha256")}
    row.update({"schema_version":2, "attention_frobenius_norm":norm,
                "named_first_coefficients":coef, "attention_singular_values":sA.tolist(),
                "named_first_residual_singular_values":sR.tolist(),
                "allocation":{}, "capacity":{}, "allocation_comparisons":old["allocation_comparisons"]})
    for convention in CONVENTIONS:
        source = SOURCE_CONVENTION[convention]
        row["allocation"][convention] = {}
        for r in RANKS:
            obs = old["conventions"][source][str(r)]
            metrics = {k:obs["metrics"][k] for k in ALLOCATION_FIELDS}
            profile = v1.resolve_profile(old,source,r,"residual_A_minus_S")
            metrics["named_channel_only_error"] = float(np.sqrt(profile["energy_over_A"]))
            metrics["named_channel_parameters"] = 2*int(metrics["n_active"])
            metrics["decomposition_parameters"] = metrics["named_channel_parameters"] + r*(2*n+1)
            item = {"label":LABELS[convention], "residual_rank":r, "metrics":metrics,
                    "coefficients":obs["coefficients"], "lowrank_cutoff":obs["lowrank_cutoff"]}
            if convention == ALT:
                item["algorithm_1_diagnostics"] = obs["alternating_diagnostics"]
            row["allocation"][convention][str(r)] = item
    for K in BUDGET_RANKS:
        B, q = K*(2*n+1), K-1
        cost = 2*active + q*(2*n+1)
        if cost > B:
            raise ArithmeticError("Named-first S+L_(K-1) does not fit: no conditional-subset reporting")
        errSL = float(np.linalg.norm(sR[q:])/norm)
        errSVD = float(np.linalg.norm(sA[K:])/norm)
        row["capacity"][str(K)] = {"budget_rank_K":K, "common_cap":B, "residual_rank":q,
                                    "named_first_parameters":cost, "named_first_unused_parameters":B-cost,
                                    "named_first_active_atoms":active, "svd_parameters":B,
                                    "named_first_error":errSL, "svd_error":errSVD,
                                    "paired_error_named_minus_svd":errSL-errSVD,
                                    "named_channel_only_error":float(np.linalg.norm(sR)/norm),
                                    "named_channel_parameters":2*active,
                                    "line_max_selected_atoms":min(B//2,2*n+7),
                                    "line_unused_parameters_if_dictionary_exhausted":B-2*min(B//2,2*n+7)}
    return row


def core(job):
    model,n = job
    target,pairpath = core_paths(model,n)
    source_summary_path,source_pairs_path = v1.dataset_paths(model,n)
    source_summary = json.loads(source_summary_path.read_text(encoding="utf-8"))
    source_hash = sha256_file(source_pairs_path)
    if source_summary["pairs_sha256"] != source_hash:
        raise RuntimeError("Audited v1 pairs changed")
    if target.exists():
        existing = json.loads(target.read_text(encoding="utf-8"))
        if existing["source_pairs_sha256"] != source_hash or existing["pairs_sha256"] != sha256_file(pairpath):
            raise RuntimeError("Existing v2 core artifact mismatch; preserve and inspect")
        return str(target)
    manifest_path = sample_paths(model,n)[1]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = []
    start = time.perf_counter()
    log(f"CORE START {model} n={n}: exact audited allocation reused; instance medians/block bootstrap and symmetric q=K-1")
    pairpath.parent.mkdir(parents=True,exist_ok=True)
    if pairpath.exists():
        with pairpath.open(encoding="utf-8") as inp:
            rows = [json.loads(line) for line in inp]
    with source_pairs_path.open(encoding="utf-8") as inp, pairpath.open("a",encoding="utf-8") as out:
        for i,line in enumerate(inp):
            if i < len(rows):
                continue
            old = json.loads(line)
            if old["instance_id"] != manifest["instances"][i]["instance_id"]:
                raise ValueError("Manifest/source pair ordering mismatch")
            row = convert_record(old)
            out.write(json.dumps(row,allow_nan=False,ensure_ascii=False,separators=(",",":"))+"\n")
            rows.append(row)
    if len(rows) != manifest["n_matrices"]:
        raise ValueError("Incomplete population")
    docs = [r["document_index"] for r in rows]
    allocation = {}
    for convention in CONVENTIONS:
        allocation[convention] = {}
        for r in RANKS:
            obs = [row["allocation"][convention][str(r)] for row in rows]
            item = {"label":LABELS[convention], "residual_rank":r,
                    "metrics":{key:summarize([v["metrics"][key] for v in obs],docs) for key in obs[0]["metrics"]},
                    "cutoff_ties":{key:sum(int(v["lowrank_cutoff"][key]) for v in obs)
                                   for key in ("boundary_exists","exact_tie","numerical_tie","positive_numerical_tie")}}
            if convention == ALT:
                item["algorithm_1_diagnostics"] = {"iterations":5,"early_stopping":False,
                    "criterion_met_by_5":sum(int(v["algorithm_1_diagnostics"]["diagnostic_tolerance_met"]) for v in obs),
                    "n_instances":len(obs)}
            allocation[convention][str(r)] = item
        log(f"CORE aggregate {model} n={n} {LABELS[convention]}")
    capacity = {}
    for K in BUDGET_RANKS:
        observations = [row["capacity"][str(K)] for row in rows]
        keys = ("named_first_error","svd_error","named_first_parameters","named_first_unused_parameters",
                "named_first_active_atoms","named_channel_only_error","named_channel_parameters")
        capacity[str(K)] = {"common_cap":K*(2*n+1),"budget_rank_K":K,"residual_rank":K-1,
                            "metrics":{key:summarize([v[key] for v in observations],docs) for key in keys},
                            "named_minus_svd":paired([v["paired_error_named_minus_svd"] for v in observations],rows)}
    result = {"schema_version":2,"model":model,"n":n,"n_instances":len(rows),"n_documents":len(set(docs)),
              "source_summary_path":str(source_summary_path),"source_pairs_path":str(source_pairs_path),
              "source_pairs_sha256":source_hash,"manifest_sha256":sha256_file(manifest_path),
              "dictionary":source_summary["dictionary"],"pairs_path":pairpath.as_posix(),"pairs_sha256":sha256_file(pairpath),
              "allocation":allocation,"capacity_without_lines":capacity,
              "elapsed_seconds":time.perf_counter()-start}
    write_new(target,result)
    log(f"CORE DONE {model} n={n}; {len(rows)} instances, 64 documents, {result['elapsed_seconds']:.1f}s")
    return str(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("freeze","core"))
    parser.add_argument("--workers",type=int,default=2,choices=(1,2,3))
    parser.add_argument("--models",nargs="+",default=MODELS,choices=MODELS)
    parser.add_argument("--lengths",nargs="+",type=int,default=(128,256),choices=(128,256))
    args = parser.parse_args()
    freeze()
    if args.command == "core":
        jobs = [(m,n) for n in args.lengths for m in args.models]
        if args.workers == 1:
            for job in jobs:
                core(job)
        else:
            with ProcessPoolExecutor(max_workers=args.workers) as pool:
                for path in pool.map(core,jobs):
                    print(f"SAVED {path}",flush=True)


if __name__ == "__main__":
    main()
