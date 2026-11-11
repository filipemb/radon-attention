"""E7: replicate matrix metrics on Qwen/Qwen2.5-7B (device-map offload, no quantize).

Stages: pilot (1 doc, n=128) -> tokenizer assert + in-memory manifest ->
extraction to data/attn_7b (same capture logic as extract_attn.py) ->
CPU metrics (same calls as phase24 run_core + phase21 named_first energy).
 corpus_v2.manifest.json, sampling.py, extract_attn.py, phase24/phase21 are
read/imported only, never modified.
"""
import os
for _key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "4"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import argparse
import copy
import gc
import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from sampling import (make_manifest, validate_matrices, sha256_file,  # first: pyarrow DLL must load before torch
                      write_json_new, slug, read_articles)
import numpy as np
import torch

from extract_attn import capture_attention, set_attention, CAPTURE
from transformers import (AutoModelForCausalLM, AutoConfig, AutoTokenizer,
                          AttentionInterface)

MODEL7 = "Qwen/Qwen2.5-7B"
MODEL3 = "Qwen/Qwen2.5-3B"
CORPUS_PATH = Path("data/attn/corpus_v2.manifest.json")
DATA7 = Path("data/attn_7b")
OUT_JSON = Path("out/phase27_qwen7b.json")
LOG_PATH = Path("out/_rerun_logs/e7_progress.md")
QUOTAS = ["9GiB", "8GiB", "7GiB"]
N_DOCS = 64


def log(stage, message):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"\n- {stamp} | E7 {stage}: {message}\n")
    print(f"E7 {stage}: {message}", flush=True)


def load_corpus():
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def pilot_stage(n=128):
    """1 document, batch 1. Returns (attempts, winning_quota). Raises if all OOM."""
    import psutil
    corpus = load_corpus()
    ids1 = torch.tensor([corpus["models"][MODEL3]["documents"][0]["token_ids"][:n]],
                        dtype=torch.long)
    proc = psutil.Process()
    attempts = []
    for quota in QUOTAS:
        torch.cuda.reset_peak_memory_stats()
        gc.collect()
        torch.cuda.empty_cache()
        try:
            t0 = time.perf_counter()
            model = AutoModelForCausalLM.from_pretrained(
                MODEL7, local_files_only=True, attn_implementation="eager",
                dtype=torch.bfloat16, device_map="auto",
                max_memory={0: quota, "cpu": "24GiB"})
            model.eval()
            load_s = time.perf_counter() - t0
            devs = Counter(str(v) for v in model.hf_device_map.values())
            with torch.inference_mode():
                model(ids1.to("cuda"), use_cache=False, logits_to_keep=1)
                torch.cuda.synchronize()
                times = []
                for _ in range(3):
                    a = time.perf_counter()
                    model(ids1.to("cuda"), use_cache=False, logits_to_keep=1)
                    torch.cuda.synchronize()
                    times.append(time.perf_counter() - a)
            rec = {"quota": quota, "status": "ok",
                   "load_seconds": round(load_s, 1),
                   "sec_per_forward": round(float(np.mean(times)), 3),
                   "peak_vram_GiB": round(torch.cuda.max_memory_allocated() / 2**30, 3),
                   "proc_rss_GiB": round(proc.memory_info().rss / 2**30, 3),
                   "device_counts": dict(devs)}
            log("pilot", f"quota={quota} OK " + json.dumps(rec))
            attempts.append(rec)
            del model
            gc.collect()
            torch.cuda.empty_cache()
            return attempts, quota
        except torch.OutOfMemoryError as e:
            rec = {"quota": quota, "status": "oom",
                   "error": str(e)[:200]}
            log("pilot", f"quota={quota} OOM")
            attempts.append(rec)
            gc.collect()
            torch.cuda.empty_cache()
    raise RuntimeError(f"E7 pilot: all quotas OOM: {attempts}")


def tokenizer_check(corpus):
    """Assert 7B tokenizer yields exactly the 3B stored ids on all 64 docs."""
    tok3 = AutoTokenizer.from_pretrained(MODEL3, local_files_only=True)
    tok7 = AutoTokenizer.from_pretrained(MODEL7, local_files_only=True)
    cfg3 = corpus["models"][MODEL3]
    docs, _ = read_articles()
    by_id = {d["doc_id"]: d["text"] for d in docs}
    for di in range(N_DOCS):
        meta = corpus["documents"][di]
        text = by_id[meta["doc_id"]]
        full3 = tok3(text, add_special_tokens=False)["input_ids"]
        full7 = tok7(text, add_special_tokens=False)["input_ids"]
        if full7 != full3:
            raise ValueError(f"Tokenizer mismatch on document {di} {meta['doc_id']}")
        off = cfg3["documents"][di]["offset"]
        if full7[off:off + corpus["window_tokens"]] != cfg3["documents"][di]["token_ids"]:
            raise ValueError(f"Window mismatch on document {di} {meta['doc_id']}")
    log("tokenizer", f"7B tokenizer identical to 3B on all {N_DOCS} documents "
                     f"({type(tok7).__name__})")
    return {"compared_documents": N_DOCS, "identical": True,
            "tokenizer_class_7b": type(tok7).__name__,
            "tokenizer_class_3b": type(tok3).__name__}


def build_corpus7(corpus):
    cfg7auto = AutoConfig.from_pretrained(MODEL7, local_files_only=True)
    cfg3 = corpus["models"][MODEL3]
    cfg7 = copy.deepcopy(cfg3)
    cfg7["revision"] = cfg7auto._commit_hash
    cfg7["n_layers"] = cfg7auto.num_hidden_layers
    cfg7["n_heads"] = cfg7auto.num_attention_heads
    corpus7 = dict(corpus)
    corpus7["models"] = dict(corpus["models"])
    corpus7["models"][MODEL7] = cfg7
    info = {"revision": cfg7["revision"], "n_layers": cfg7["n_layers"],
            "n_heads": cfg7["n_heads"],
            "n_kv_heads": cfg7auto.num_key_value_heads,
            "tokenizer_class": cfg7["tokenizer_class"]}
    log("manifest", f"cfg7 in-memory: {json.dumps(info)}")
    return corpus7, info


def paths7(n):
    base = DATA7 / f"{slug(MODEL7)}_n{n}"
    return Path(str(base) + ".npz"), Path(str(base) + ".manifest.json")


@torch.inference_mode()
def extract_7b(corpus7, n, quota, batch=1):
    start = time.perf_counter()
    path, mpath = paths7(n)
    if path.exists() or mpath.exists():
        if not (path.exists() and mpath.exists()):
            raise RuntimeError(f"Incomplete prior E7 extraction: {path}")
        return verify_7b(n)
    manifest = make_manifest(corpus7, MODEL7, n, N_DOCS)
    cfg = corpus7["models"][MODEL7]
    ids = torch.tensor([x["token_ids"][:n] for x in cfg["documents"][:N_DOCS]],
                       dtype=torch.long)
    targets = np.array([x["token_ids"][n] for x in cfg["documents"][:N_DOCS]],
                       dtype=np.int64)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL7, revision=cfg["revision"], local_files_only=True,
        attn_implementation="eager", dtype=torch.bfloat16,
        device_map="auto", max_memory={0: quota, "cpu": "24GiB"}).eval()
    sample = np.empty((manifest["n_matrices"], n, n), dtype=np.float16)
    selection = {(di, layer): [] for di in range(N_DOCS)
                 for layer in range(manifest["n_layers"])}
    for i, item in enumerate(manifest["instances"]):
        selection[item["document_index"], item["layer"]].append((i, item["head"]))
    ref = model(ids[:batch].to("cuda"), use_cache=False,
                logits_to_keep=1).logits[:, -1].float().cpu()
    CAPTURE.update({"selected": selection, "output": sample, "checks": []})
    AttentionInterface.register("p0_capture", capture_attention)
    set_attention(model, "p0_capture")
    actual = 0
    for s in range(0, N_DOCS, batch):
        CAPTURE["layer"], CAPTURE["batch_start"] = 0, s
        out = model(ids[s:s + batch].to("cuda"), use_cache=False, logits_to_keep=1)
        if CAPTURE["layer"] != manifest["n_layers"]:
            raise RuntimeError(f"Attention calls {CAPTURE['layer']} != layers {manifest['n_layers']}")
        if s == 0:
            got = out.logits[:, -1].float().cpu()
            if not torch.equal(ref, got):
                raise RuntimeError(
                    f"Capture changed vanilla eager logits, max error {(ref - got).abs().max().item()}")
        actual += ids[s:s + batch].shape[0]
        if actual % 16 == 0:
            print(f"{MODEL7} n={n}: {actual}/{N_DOCS} documents", flush=True)
    source_checks = CAPTURE["checks"]
    source_invalid = sum(c["invalid_matrices"] for c in source_checks)
    checks = validate_matrices(sample, manifest["storage_row_sum_atol"])
    manifest.update({"n_sequences_processed": actual,
                     "n_documents_effective": actual,
                     "n_model_forward_sequences_including_identity": actual + len(ids[:batch]),
                     "model_dtype": str(torch.bfloat16),
                     "identity_capture_logits_exact": True,
                     "gpu_quota": quota,
                     "source_validation": {
                         "invalid_matrices": source_invalid,
                         "nan_values": sum(c["nan_values"] for c in source_checks),
                         "inf_values": sum(c["inf_values"] for c in source_checks),
                         "max_row_sum_abs_error": max(c["max_row_sum_abs_error"] for c in source_checks)},
                     "archive_validation": checks,
                     "status": "verified" if source_invalid == 0 and checks["invalid_matrices"] == 0 else "invalid"})
    if source_invalid or checks["invalid_matrices"]:
        write_json_new(mpath, manifest)
        raise RuntimeError(f"Invalid E7 extraction; counts preserved in {mpath}")
    DATA7.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".partial.npz")
    np.savez_compressed(temp, attention=sample, input_ids=ids.numpy(),
                        next_token_ids=targets,
                        document_index=np.array([x["document_index"] for x in manifest["instances"]],
                                                dtype=np.int32),
                        layer=np.array([x["layer"] for x in manifest["instances"]], dtype=np.int16),
                        head=np.array([x["head"] for x in manifest["instances"]], dtype=np.int16))
    temp.rename(path)
    manifest.update({"npz_sha256": sha256_file(path),
                     "npz_bytes": path.stat().st_size,
                     "elapsed_seconds": time.perf_counter() - start})
    write_json_new(mpath, manifest)
    log("extract", f"{MODEL7} n={n}: {actual} docs, {manifest['n_matrices']} matrices, "
                   f"elapsed={manifest['elapsed_seconds']:.1f}s sha={manifest['npz_sha256'][:12]}")
    del model, sample, ref, out
    CAPTURE["output"] = None
    gc.collect()
    torch.cuda.empty_cache()
    return verify_7b(n)


def verify_7b(n):
    path, mpath = paths7(n)
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    if sha256_file(path) != manifest["npz_sha256"]:
        raise RuntimeError(f"Hash mismatch: {path}")
    with np.load(path, allow_pickle=False) as z:
        a = z["attention"]
        expected = (manifest["n_matrices"], n, n)
        if a.shape != expected or a.dtype != np.float16:
            raise RuntimeError(f"Invalid archive: {a.shape}, {a.dtype}, expected {expected}")
        check = validate_matrices(a, manifest["storage_row_sum_atol"])
        if check["invalid_matrices"]:
            raise RuntimeError(f"Archive validation failed: {path}: {check}")
        for key in ("document_index", "layer", "head"):
            if not np.array_equal(z[key], [x[key] for x in manifest["instances"]]):
                raise RuntimeError(f"Archive/manifest ordering mismatch for {key}: {path}")
        counts = np.bincount(z["layer"], minlength=manifest["n_layers"])
        if counts.min() != counts.max() or manifest["n_documents_effective"] < 64 or a.shape[0] < 1024:
            raise RuntimeError(f"Stratification/count failure: {path}")
    print(f"VERIFIED {path}: {expected}, docs={manifest['n_documents_effective']}, "
          f"row_error={check['max_row_sum_abs_error']:.3g}", flush=True)
    return {"model": MODEL7, "n": n, "n_documents": manifest["n_documents_effective"],
            "n_matrices": manifest["n_matrices"], "bytes": path.stat().st_size,
            "matrices_per_layer": manifest["matrices_per_layer"],
            "manifest_sha256": sha256_file(mpath),
            "max_row_sum_abs_error": check["max_row_sum_abs_error"]}


def metrics_7b(n):
    from phase24_p0_metrics import describe, svd_relative_error
    from phase0_radon_attention import radon_support_fraction, make_controls
    from phase06_profiled_lines import omp_profiled, precompute_band_norms
    from phase5_msclean import build_dict, msclean
    from phase21_allocation import Dictionary, evaluate_instance
    started = time.perf_counter()
    pairpath = Path("out/pairs") / f"phase27_qwen7b_n{n}.jsonl"
    path, mpath = paths7(n)
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    if manifest.get("status") != "verified":
        raise RuntimeError(f"Unverified E7 sample {path}")
    if sha256_file(path) != manifest["npz_sha256"]:
        raise RuntimeError(f"Archive hash differs from verified manifest: {path}")
    with np.load(path, allow_pickle=False) as z:
        attention = z["attention"].astype(np.float64)
    theta = np.arange(0.0, 180.0, 2.0)
    norms = precompute_band_norms(n)
    _, randoms = make_controls(n, 40, np.random.default_rng(np.random.SeedSequence([0, n, 331])))
    random_support = [radon_support_fraction(a, theta)[0] for a in randoms]
    d, labels = build_dict(n)
    dictionary = Dictionary(n)
    rows = []
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    with pairpath.open("x", encoding="utf-8") as out:
        for i, a in enumerate(attention):
            norm = np.linalg.norm(a)
            if not np.isfinite(a).all() or norm <= 0:
                raise ValueError(f"Invalid input instance {i}")
            prof, support = omp_profiled(a, 8, n, {8}, norms)
            err_svd = svd_relative_error(a, 8)
            row = {**manifest["instances"][i],
                   "radon_support": radon_support_fraction(a, theta)[0],
                   "profiled_line_k8_relative_error": prof[8],
                   "svd_k8_relative_error": err_svd,
                   "profiled_line_k8_absolute_error": prof[8] * norm,
                   "svd_k8_absolute_error": err_svd * norm,
                   "paired_relative_error_line_minus_svd": prof[8] - err_svd,
                   "attention_frobenius_norm": float(norm),
                   "line_support": support}
            mu, r, c = a.mean(), a.mean(-1, keepdims=True), a.mean(-2, keepdims=True)
            additive = r + c - mu
            theta_s = np.linalg.svd(a - additive, compute_uv=False)
            cc = c.ravel() - mu
            clean, _ = msclean(a, d, labels, 5)
            row.update({
                "anova_addrank8_relative_error": float(np.linalg.norm(theta_s[8:]) / norm),
                "sink_frac_of_column_effect_energy": float(cc[0] ** 2 / np.dot(cc, cc)),
                "named_m5_norm_ratio": float(np.linalg.norm(clean) / norm)})
            ev = evaluate_instance(a, dictionary)
            row["named_first_energy_ratio_r8"] = ev["conventions"]["named_first"]["8"]["metrics"]["named_energy_ratio"]
            out.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
            rows.append(row)
            if (i + 1) % 128 == 0:
                out.flush()
                print(f"E7 metrics n={n}: {i + 1}/{len(attention)}, "
                      f"seconds={time.perf_counter() - started:.1f}", flush=True)
    docs = [r["document_index"] for r in rows]
    keys = ["radon_support", "profiled_line_k8_relative_error", "svd_k8_relative_error",
            "profiled_line_k8_absolute_error", "svd_k8_absolute_error",
            "paired_relative_error_line_minus_svd",
            "anova_addrank8_relative_error", "sink_frac_of_column_effect_energy",
            "named_m5_norm_ratio", "named_first_energy_ratio_r8"]
    result = {"n_sequences_effective": manifest["n_sequences_processed"],
              "n_documents_effective": manifest["n_documents_effective"],
              "n_instances": len(rows), "matrices_per_layer": manifest["matrices_per_layer"],
              "seed": manifest["seed"], "manifest_sha256": sha256_file(mpath),
              "pairs_path": pairpath.as_posix(), "pairs_sha256": sha256_file(pairpath),
              "theta_degrees": theta.tolist(),
              "random_control_n": len(random_support),
              "random_support_median": float(np.median(random_support)),
              "metrics": {key: describe([r[key] for r in rows], docs) for key in keys},
              "elapsed_seconds": time.perf_counter() - started}
    result["concentration_real_to_random_ratio"] = (
        result["metrics"]["radon_support"]["median"] / result["random_support_median"])
    log("metrics", f"n={n}: {len(rows)} pairs, {len(set(docs))} docs, "
                   f"elapsed={result['elapsed_seconds']:.1f}s")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lengths", nargs="+", type=int, default=[128, 256])
    ap.add_argument("--batch", type=int, default=1)
    args = ap.parse_args()
    t_all = time.perf_counter()
    corpus = load_corpus()
    attempts, quota = pilot_stage()
    tok = tokenizer_check(corpus)
    corpus7, cfginfo = build_corpus7(corpus)
    datasets = {}
    for n in args.lengths:
        try:
            counts = extract_7b(corpus7, n, quota, args.batch)
        except torch.OutOfMemoryError as e:
            if n == 128:
                raise
            msg = f"n=256 skipped: OOM under quota {quota}: {str(e)[:160]}"
            log("extract", msg)
            datasets[str(n)] = {"status": "skipped_oom", "quota": quota,
                                "detail": str(e)[:300]}
            continue
        met = metrics_7b(n)
        met.update(counts)
        met["status"] = "verified"
        datasets[str(n)] = met
    result = {"schema_version": 1, "experiment": "E7", "model": MODEL7,
              "pilot": {"n": 128, "batch": 1, "documents": 1,
                       "attempts": attempts, "chosen_quota": quota},
              "tokenizer_check": tok, "config_7b": cfginfo,
              "corpus_manifest_sha256": sha256_file(CORPUS_PATH),
              "datasets": datasets,
              "elapsed_seconds": time.perf_counter() - t_all}
    if OUT_JSON.exists():
        raise RuntimeError(f"Refusing to overwrite {OUT_JSON}; remove it to rerun")
    write_json_new(OUT_JSON, result)
    log("done", f"E7 complete: lengths={sorted(datasets)}, "
                f"total_elapsed={result['elapsed_seconds']:.1f}s")
    print(f"E7 COMPLETE -> {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
