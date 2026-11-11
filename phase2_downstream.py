"""P0 V1: causal remasking and last-prefix-token behavioral evaluation.

All targets and suffix tokens are excluded from the model input. Raw paired
per-document KL/NLL records are streamed to exclusive, versioned JSONL files.
"""
from sampling import (MODELS, CORPUS_PATH, prepare_corpus, sha256_file,
                      write_json_new, progress, slug)
import argparse
import gc
import json
import math
from pathlib import Path
import sys
import time
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AttentionInterface

torch.set_num_threads(4)
RECON = {"mode": "identity", "k": 8, "D": None, "D_pinv": None, "stats": {}, "empty_row_policy": "uniform", "svd_driver": None, "parallel_svd": False}
RANKS = [1, 2, 4, 8, 16, 32]
NORMALIZED_ROW_ATOL = 2e-6

class DeferredStats(dict):
    """Keep scalar checks on device; synchronize and fail before scoring/writing.

    The checks still inspect every value/row at the original fixed tolerances.
    Only their transfer to Python is deferred. Plain dict callers retain the
    immediate-validation API, including external S+L adapters.
    """
    defer_validation = True
    violation_keys = ("negative_nan_inf_upper_nonzero", "row_sum_violations",
                      "reconstruction_nonfinite_values", "reconstruction_invalid_denominators",
                      "sink_edit_invalid_values", "sink_edit_invalid_totals",
                      "sink_edit_noncausal_values", "sink_edit_row_sum_violations",
                      "sink_edit_first_row_changes")

    def add_scalar(self, key, value):
        self[key] = self.get(key, 0) + value

    def max_scalar(self, key, value):
        previous = self.get(key)
        if previous is None:
            self[key] = value
        elif torch.is_tensor(value):
            previous = previous if torch.is_tensor(previous) else value.new_tensor(previous)
            self[key] = torch.maximum(previous, value)
        else:
            self[key] = max(previous, value)

    def check_attention(self, weights):
        validate_attention(weights, self)

    def finalize(self, context=""):
        names = [key for key,value in self.items() if torch.is_tensor(value)]
        if names:
            floating = [self[key].dtype.is_floating_point for key in names]
            # Float64 preserves every float32 row error and all integer counters
            # exactly; a single small device-to-host transfer serves the batch.
            packed = torch.stack([self[key].to(torch.float64) for key in names]).cpu().tolist()
            for key,value,is_float in zip(names,packed,floating):
                self[key] = float(value) if is_float else int(value)
        bad = {key:self[key] for key in self.violation_keys if self.get(key,0) != 0}
        nonfinite = {key:value for key,value in self.items() if isinstance(value,float) and not math.isfinite(value)}
        if bad or nonfinite:
            raise RuntimeError(f"Attention sanity failed before scoring/writing {context}: violations={bad}; nonfinite={nonfinite}")
        return self

def factor_svd(weights, driver=None, parallel=False):
    """Full, exact float32 SVD; only its cuSOLVER implementation may differ."""
    driver = driver if weights.device.type == "cuda" else None
    if parallel and weights.device.type=="cuda":
        from phase34_parallel_svd import parallel_svd
        return parallel_svd(weights,driver)
    return torch.linalg.svd(weights, full_matrices=False, driver=driver)


def _repeat_kv(x, n_rep):
    if n_rep == 1:
        return x
    b, h, s, d = x.shape
    return x[:, :, None, :, :].expand(b, h, n_rep, s, d).reshape(b, h * n_rep, s, d)

def causal_support(q, k, device):
    if k < q:
        raise ValueError("Causal cached attention requires k >= q")
    return torch.ones(q, k, device=device, dtype=torch.bool).tril(k - q)

def validate_attention(weights, stats, normalized_fp32=False):
    q, k = weights.shape[-2:]
    if getattr(stats, "defer_validation", False):
        allowed = causal_support(q, k, weights.device)
        bad_values = ((~torch.isfinite(weights)) | (weights < 0)).sum()
        # Fixed-shape masking avoids masked_select's device-to-host size query.
        upper_nonzero = ((weights != 0) & ~allowed).sum()
        stats.add_scalar("negative_nan_inf_upper_nonzero", bad_values + upper_nonzero)
        errors = (weights.float().sum(-1)-1).abs()
        atol = NORMALIZED_ROW_ATOL if normalized_fp32 else NORMALIZED_ROW_ATOL + torch.finfo(weights.dtype).eps/2
        # Compare in float64 to reproduce the old Python-double threshold,
        # without even a float32 rounding relaxation of the tolerance.
        stats.add_scalar("row_sum_violations", ((~torch.isfinite(errors)) | (errors.double() > atol)).sum())
        key = "max_row_error_before_cast" if normalized_fp32 else "max_row_error_after_cast"
        stats.max_scalar(key, errors.max())
        stats.add_scalar("rows_checked", weights.numel()//k)
        return
    if not bool(torch.isfinite(weights).all()) or bool((weights < 0).any()):
        raise RuntimeError("Nonfinite or negative injected attention")
    allowed = causal_support(q, k, weights.device)
    if bool((weights.masked_select(~allowed) != 0).any()):
        raise RuntimeError("Injected attention above causal diagonal")
    error = float((weights.float().sum(-1) - 1).abs().max())
    atol = NORMALIZED_ROW_ATOL if normalized_fp32 else NORMALIZED_ROW_ATOL + torch.finfo(weights.dtype).eps / 2
    if error > atol:
        raise RuntimeError(f"Invalid row sum: {error} exceeds fixed dtype bound {atol}")
    key = "max_row_error_before_cast" if normalized_fp32 else "max_row_error_after_cast"
    stats[key] = max(stats.get(key, 0.0), error)
    stats["rows_checked"] = stats.get("rows_checked", 0) + weights.numel() // k
    stats["negative_nan_inf_upper_nonzero"] = 0

def record_reconstruction_rows(weights, stats, empty=None):
    """Count attention rows once, independently of repeated validity checks."""
    q, k = weights.shape[-2:]
    rows = weights.numel() // k
    last_rows = rows // q
    stats["reconstruction_rows_total"] = stats.get("reconstruction_rows_total", 0) + rows
    stats["last_query_rows_total"] = stats.get("last_query_rows_total", 0) + last_rows
    stats["reconstruction_layer_calls"] = stats.get("reconstruction_layer_calls", 0) + 1
    deferred = getattr(stats, "defer_validation", False)
    completed = (empty.sum() if deferred else int(empty.sum())) if empty is not None else 0
    last_completed = (empty[..., -1, :].sum() if deferred else int(empty[..., -1, :].sum())) if empty is not None else 0
    stats["empty_rows_completed"] = stats.get("empty_rows_completed", 0) + completed
    stats["empty_rows_completed_at_last_query"] = stats.get("empty_rows_completed_at_last_query", 0) + last_completed

def completion_summary(stats):
    total = stats["reconstruction_rows_total"]
    last_total = stats["last_query_rows_total"]
    return {"policy": "uniform_causal", "rows_total": total,
            "rows_completed": stats["empty_rows_completed"],
            "fraction_rows_completed": stats["empty_rows_completed"] / total,
            "last_query_rows_total": last_total,
            "last_query_rows_completed": stats["empty_rows_completed_at_last_query"],
            "fraction_last_query_rows_completed": stats["empty_rows_completed_at_last_query"] / last_total}

def normalize_reconstruction(rec, original, stats, empty_policy="uniform", cast_to_original=True):
    """Shared SVD/geometric/S+L projection. Empty finite rows use only causal
    support, never original row values: 1/(k-q+i+1) for j <= k-q+i.
    The original tensor supplies the output dtype only.
    """
    if empty_policy not in ("uniform", "error"):
        raise ValueError("Original-row completion is forbidden; use uniform causal")
    deferred = getattr(stats, "defer_validation", False)
    if deferred:
        stats.add_scalar("reconstruction_nonfinite_values", (~torch.isfinite(rec)).sum())
    elif not bool(torch.isfinite(rec).all()):
        raise RuntimeError("Nonfinite reconstructed attention; replacement is forbidden")
    q, k = rec.shape[-2:]
    rec = rec * causal_support(q, k, rec.device)
    rec = rec.clamp(min=0)
    sums = rec.sum(-1, keepdim=True)
    if not deferred and not bool(torch.isfinite(sums).all()):
        raise RuntimeError("Nonfinite reconstructed attention; replacement is forbidden")
    empty = sums <= 0
    record_reconstruction_rows(rec, stats, empty)
    if empty_policy == "error" and bool(empty.any()):
        bad = torch.nonzero((sums <= 0) | ~torch.isfinite(sums)).tolist()
        raise RuntimeError(f"Reconstruction contains an empty/nonfinite causal row; no silent fallback; indices={bad[:8]}")
    # For strided geometric projections retain the old conditional layout;
    # changing a reduction's layout can change its float32 summation order.
    if (deferred and rec.is_contiguous()) or bool(empty.any()):
        fill = causal_support(q, k, rec.device).to(rec.dtype).expand_as(rec)
        rec = torch.where(empty, fill, rec)
        sums = rec.sum(-1, keepdim=True)
        if deferred:
            stats.add_scalar("reconstruction_invalid_denominators", ((sums <= 0) | ~torch.isfinite(sums)).sum())
        elif bool((sums <= 0).any()) or not bool(torch.isfinite(sums).all()):
            raise RuntimeError("Chosen completion policy did not yield a valid row")
    rec = rec / sums
    validate_attention(rec, stats, normalized_fp32=True)
    if not cast_to_original:
        return rec
    cast = rec.to(original.dtype)
    validate_attention(cast, stats)
    return cast

def reconstruct(weights):
    mode = RECON["mode"]
    if mode == "identity":
        record_reconstruction_rows(weights, RECON["stats"])
        validate_attention(weights, RECON["stats"])
        return weights
    b, h, q, k = weights.shape
    w = weights.reshape(b * h, q, k).float()
    if mode == "svd":
        u, s, vh = factor_svd(w, RECON["svd_driver"], RECON["parallel_svd"])
        rank = min(RECON["k"], q, k)
        rec = (u[..., :rank] * s[..., None, :rank]) @ vh[..., :rank, :]
    elif mode == "geom":
        if q != k or RECON["D"].shape[0] != q * k:
            raise ValueError("The fixed geometric dictionary is defined for a square prefill")
        vectors = w.reshape(b * h, q * k).T
        coef = RECON["D_pinv"] @ vectors
        rec = (RECON["D"] @ coef).T.reshape(b * h, q, k)
    elif mode == "uniform":
        rec = causal_support(q, k, w.device).float().expand_as(w)
    elif mode == "diagonal":
        rec = torch.zeros_like(w)
        rows = torch.arange(q, device=w.device)
        rec[:, rows, rows + k - q] = 1
    elif mode == "sink":
        rec = torch.zeros_like(w)
        rec[..., 0] = 1
    else:
        raise ValueError(f"Unknown reconstruction mode {mode}")
    return normalize_reconstruction(rec, weights.reshape(b * h, q, k), RECON["stats"], RECON["empty_row_policy"]).reshape(b, h, q, k)

def attention_forward(module, query, key, value, attention_mask, scaling=None, dropout=0.0, reconstruct_fn=None, **kwargs):
    if module.training or dropout:
        raise RuntimeError("Evaluation requires eval mode and zero dropout")
    nrep = getattr(module, "num_key_value_groups", 1)
    key, value = _repeat_kv(key, nrep), _repeat_kv(value, nrep)
    scores = query @ key.transpose(-1, -2) * (scaling if scaling is not None else query.size(-1) ** -0.5)
    q, k = scores.shape[-2:]
    scores = scores.masked_fill(~causal_support(q, k, scores.device), float("-inf"))
    aw = F.softmax(scores, dim=-1, dtype=torch.float32).to(value.dtype)
    aw = (reconstruct_fn or reconstruct)(aw)
    out = (aw @ value).transpose(1, 2)
    if module.config.model_type != "gpt2":
        out = out.contiguous()
    return out, aw

recon_attention_forward = attention_forward

def build_dictionary(n, device):
    cols = []
    for c in [0, 1, 2]:
        m = torch.zeros(n, n); idx = torch.arange(c, n); m[idx, c] = 1
        cols.append(m)
    for tau in [1, 2, 4, 8, 16, 32, 64]:
        m = torch.zeros(n, n)
        for off in range(n):
            weight = float(np.exp(-off / tau))
            if weight < 1e-6:
                break
            ii = torch.arange(off, n); m[ii, ii-off] = weight
        cols.append(m)
    for d in [4, 8, 16, 32, 64]:
        m = torch.zeros(n, n); ii = torch.arange(d, n); m[ii, ii-d] = 1
        cols.append(m)
    d = torch.stack([m.ravel() for m in cols], 1).to(device)
    return d / d.norm(dim=0, keepdim=True)

@torch.inference_mode()
def last_logits(model, sequences, cutoff):
    """The sole behavioral evaluator: physically excludes target and suffix."""
    if not 1 <= cutoff <= sequences.shape[1]:
        raise ValueError("Invalid prefix cutoff")
    device = next(model.parameters()).device
    return model(sequences[:, :cutoff].to(device), use_cache=False, logits_to_keep=1).logits[:, -1].float()

def kl_nll(ref, other, targets):
    logp = F.log_softmax(ref.double(), -1)
    logq = F.log_softmax(other.double(), -1)
    divergence = (logp.exp() * (logp - logq)).sum(-1)
    nll = -logq.gather(-1, targets.to(other.device)[:, None]).squeeze(-1)
    if not bool(torch.isfinite(divergence).all() and torch.isfinite(nll).all()):
        raise RuntimeError("Nonfinite KL/NLL")
    return divergence.cpu().numpy(), nll.cpu().numpy()

def mode_specs(suites):
    modes = []
    if "phase2" in suites:
        modes = [("phase2", "identity", None)] + [("phase2", "svd", k) for k in RANKS]
        modes += [("phase2", name, None) for name in ("geom", "uniform", "diagonal", "sink")]
    if "phase7" in suites:
        modes += [("phase7", name, 8) for name in ("identity", "anova", "nosink", "zerocol_mid")]
    return modes

def activate(model, spec, deferred=False):
    suite, mode, rank = spec
    if suite == "phase7":
        import phase7_editability as p7
        p7.RECON.update({"mode": mode, "k": rank, "stats": DeferredStats() if deferred else {}, "empty_row_policy": RECON["empty_row_policy"],
                         "svd_driver": RECON["svd_driver"], "parallel_svd": RECON["parallel_svd"]})
        model.set_attn_implementation("p0_anova")
        return p7.RECON["stats"]
    RECON.update({"mode": mode, "k": rank, "stats": DeferredStats() if deferred else {}})
    model.set_attn_implementation("p0_recon")
    return RECON["stats"]

def arm_label(spec):
    return f"{spec[0]}:{spec[1]}" + (f":{spec[2]}" if spec[2] is not None else "")

@torch.inference_mode()
def validation_schedule_sanity(model, windows, n, specs, batch):
    """On the actual GPU/dtype, prove deferred checks do not change logits."""
    sequences = windows[:batch]
    result = {}
    for spec in specs:
        strict = activate(model,spec)
        a = last_logits(model,sequences,n)
        old = dict(strict)
        deferred = activate(model,spec,deferred=True)
        b = last_logits(model,sequences,n)
        deferred.finalize(context=f"validation-schedule equivalence {arm_label(spec)}")
        if not torch.equal(a,b):
            raise RuntimeError(f"Deferred validation changed GPU logits: {arm_label(spec)}")
        if any(deferred[key] != value for key,value in old.items()):
            raise RuntimeError(f"Deferred validation changed GPU counters: {arm_label(spec)}")
        result[arm_label(spec)] = {"logits_bit_equal":True,"common_counters_exact":True,"max_logit_difference":0.}
    return {"n_documents":len(sequences),"all_arms":result,"all_passed":True}

@torch.inference_mode()
def parallel_svd_schedule_sanity(name, model, windows, n, specs, batch, corpus_hash):
    """Enable independent streams only after exact full-model equivalence.

    If timing or bit equality rejects the optimization, keep the original
    sequential execution for the entire model. No scientific case is omitted.
    """
    from phase34_parallel_svd import WORKERS
    path=Path("out")/f"phase2_parallel_schedule_{slug(name)}_v2.json"
    if path.exists():
        result=json.loads(path.read_text(encoding="utf-8"))
        if result["corpus_manifest_sha256"]!=corpus_hash or result["parallel_module_sha256"]!=sha256_file("phase34_parallel_svd.py"):
            raise RuntimeError("Preserve existing schedule proof: corpus/parallel implementation changed")
        RECON["parallel_svd"]=result["selected"]
        return result
    sequences=windows[:batch];checks={};serial_time=parallel_time=0.
    for spec in specs:
        RECON["parallel_svd"]=False
        old_stats=activate(model,spec,deferred=True)
        torch.cuda.synchronize();start=time.perf_counter()
        a=last_logits(model,sequences,n);old_stats.finalize("sequential SVD scheduling reference")
        serial=time.perf_counter()-start
        RECON["parallel_svd"]=True
        new_stats=activate(model,spec,deferred=True)
        torch.cuda.synchronize();start=time.perf_counter()
        b=last_logits(model,sequences,n);new_stats.finalize("parallel SVD scheduling candidate")
        parallel=time.perf_counter()-start
        bit_equal=torch.equal(a,b)
        counters_equal=dict(old_stats)==dict(new_stats)
        label=arm_label(spec)
        checks[label]={"logits_bit_equal":bit_equal,"all_counters_exact":counters_equal,
                       "max_logit_difference":float((a-b).abs().max()),
                       "sequential_seconds":serial,"parallel_seconds":parallel}
        serial_time+=serial;parallel_time+=parallel
    exact=all(r["logits_bit_equal"] and r["all_counters_exact"] for r in checks.values())
    selected=exact and parallel_time < .9*serial_time
    result={"model":name,"n_documents":len(sequences),"n_arms":len(specs),"selected":selected,
            "all_candidate_logits_bit_equal":exact,"same_svd_driver_dtype_and_rank":True,
            "driver":None,"workers_plus_main_thread":WORKERS+1,"cuda_streams":WORKERS,
            "checks":checks,"sequential_seconds_total":serial_time,"parallel_seconds_total":parallel_time,
            "selection_rule":"Use parallel streams only if every logit and every counter is exact and total test time improves >=10%; otherwise original sequential execution for all 256 documents",
            "selection_uses_accuracy_or_KL":False,"scientific_samples_or_budgets_changed":False,
            "corpus_manifest_sha256":corpus_hash,"parallel_module_sha256":sha256_file("phase34_parallel_svd.py")}
    write_json_new(path,result)
    RECON["parallel_svd"]=selected
    progress("V1 independent-head scheduling",f"{name}; selected_parallel={selected}; exact={exact}; sequential={serial_time:.3f}s, parallel={parallel_time:.3f}s; all 15 arms retained")
    return result

@torch.inference_mode()
def suffix_sanity(model, windows, n, specs):
    full = windows[:1, :n+16].clone()
    changed = full.clone()
    changed[:, n:] = (changed[:, n:] + 7919) % model.config.vocab_size
    results = {}
    for spec in specs:
        activate(model, spec)
        a = last_logits(model, full, n)
        b = last_logits(model, changed, n)
        error = float((a-b).abs().max())
        if not torch.equal(a, b):
            raise RuntimeError(f"Suffix invariance failed for evaluated prefix {arm_label(spec)}: {error}")
        results[arm_label(spec)] = {"max_logit_difference": error, "passed_exact": True}
    # Negative control: a full-matrix reconstruction can change an earlier
    # position if the evaluator incorrectly includes the suffix.
    activate(model, ("phase2", "svd", 8))
    old_a = model(full.to(next(model.parameters()).device), use_cache=False).logits[:, n-1].float()
    old_b = model(changed.to(next(model.parameters()).device), use_cache=False).logits[:, n-1].float()
    counterexample = float((old_a-old_b).abs().max())
    return {"evaluation_policy": "physically crop to cutoff before model.forward; only final prefix logit",
            "arms": results, "unrestricted_full_matrix_svd8_suffix_max_logit_difference": counterexample,
            "counterexample_detected": counterexample > 0}

def summarize_records(records):
    kl = np.array([r["kl"] for r in records])
    nll = np.array([r["nll"] for r in records])
    if len({r["doc_id"] for r in records}) != len(records):
        raise RuntimeError("Expected one endpoint per independent document")
    rng = np.random.default_rng(0)
    boots = kl[rng.integers(0, len(kl), size=(2000, len(kl)))].mean(1)
    return {"n_documents": len(records), "n_evaluated_next_tokens": len(records),
            "mean_kl": float(kl.mean()), "median_kl": float(np.median(kl)),
            "mean_kl_ci_document_bootstrap": np.percentile(boots, [2.5, 97.5]).tolist(),
            "mean_nll": float(nll.mean()), "last_token_perplexity": float(np.exp(nll.mean())),
            "argmax_agreement_with_reference": float(np.mean([r["argmax_agrees"] for r in records])),
            "next_token_accuracy": float(np.mean([r["correct"] for r in records]))}

def run_model(name, n=128, batch=2, suites=("phase2", "phase7"), empty_policy="uniform"):
    if empty_policy != "uniform":
        raise ValueError("The declared scientific protocol requires uniform causal completion")
    started = time.perf_counter()
    outputs = {s: Path("out") / f"{s}_{slug(name)}_v2.json" for s in suites}
    if all(p.exists() for p in outputs.values()):
        existing = {s: json.loads(p.read_text(encoding="utf-8")) for s, p in outputs.items()}
        if any(r["empty_row_policy"] != empty_policy for r in existing.values()):
            raise RuntimeError("Existing immutable output uses another completion policy")
        return existing
    corpus = prepare_corpus()
    corpus_hash = sha256_file(CORPUS_PATH)
    if n != 128:
        raise ValueError("This predeclared P0 downstream run uses prefix length 128")
    windows = torch.tensor([r["token_ids"] for r in corpus["models"][name]["documents"]], dtype=torch.long)
    dtype = torch.bfloat16 if "Qwen" in name else torch.float32
    model = AutoModelForCausalLM.from_pretrained(name, revision=corpus["models"][name]["revision"], local_files_only=True,
                                               dtype=dtype, attn_implementation="eager").to("cuda").eval()
    svd_implementation = {"selected_driver": None, "convention": "fixed torch default full exact SVD, unchanged from original harness",
                          "runtime_driver_selection": False}
    torch.manual_seed(0)
    specs = mode_specs(suites)
    RECON.update(empty_row_policy=empty_policy, parallel_svd=False, svd_driver=None)
    RECON["D"] = build_dictionary(n, "cuda")
    q, r = torch.linalg.qr(RECON["D"], mode="reduced")
    RECON["D_pinv"] = torch.linalg.solve_triangular(r, q.T, upper=True)
    AttentionInterface.register("p0_recon", attention_forward)
    import phase7_editability as p7
    AttentionInterface.register("p0_anova", p7.recon_attention_forward)
    sanity = suffix_sanity(model, windows, n, specs)
    schedule_sanity = validation_schedule_sanity(model,windows,n,specs,batch)
    parallel_sanity = parallel_svd_schedule_sanity(name,model,windows,n,specs,batch,corpus_hash)
    svd_implementation["parallel_schedule"]=parallel_sanity
    pairpath = Path("out/pairs") / f"downstream_{slug(name)}_{empty_policy}_v2.jsonl"
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if pairpath.exists():
        with pairpath.open(encoding="utf-8") as f:
            rows = [json.loads(line) for line in f]
        if any(r["corpus_manifest_sha256"] != corpus_hash for r in rows):
            raise RuntimeError("Partial records belong to another frozen corpus")
        if any(r["empty_row_policy"] != empty_policy for r in rows):
            raise RuntimeError("Partial records use another completion policy")
        if any(r.get("svd_driver") != RECON["svd_driver"] for r in rows):
            raise RuntimeError("Partial records use another exact-SVD backend; mixing backends within an arm is forbidden")
        if any(r.get("svd_parallel_schedule",False) != RECON["parallel_svd"] for r in rows):
            raise RuntimeError("Partial records use another pinned execution schedule")
    seen = {(r["arm"], r["doc_id"]) for r in rows}
    if len(seen) != len(rows):
        raise RuntimeError("Duplicate downstream raw records")
    with pairpath.open("a", encoding="utf-8") as out:
        for start in range(0, len(windows), batch):
            sequences = windows[start:start+batch]
            targets = sequences[:, n]
            model.set_attn_implementation("eager")
            ref = last_logits(model, sequences, n)
            _, ref_nll = kl_nll(ref, ref, targets)
            ref_predictions = ref.argmax(-1)
            device_targets = targets.to(ref.device)
            for spec in specs:
                label = arm_label(spec)
                ids = [corpus["documents"][i]["doc_id"] for i in range(start, min(start+batch, len(windows)))]
                if all((label, di) in seen for di in ids):
                    continue
                stats = activate(model, spec, deferred=True)
                if start == 0:
                    print(f"ARM start={start}: {label}", flush=True)
                other = last_logits(model, sequences, n)
                stats.finalize(context=f"{name} {label} documents {start}:{start+len(sequences)}")
                divergence, nll = kl_nll(ref, other, targets)
                if spec[1] == "identity" and (not torch.equal(ref, other) or np.any(divergence != 0)):
                    raise RuntimeError(f"Identity must exactly match vanilla eager for {name}, {label}")
                predictions = other.argmax(-1)
                flags = torch.stack((predictions == ref_predictions, predictions == device_targets),dim=-1).cpu().tolist()
                for bi, di in enumerate(ids):
                    if (label, di) in seen:
                        continue
                    row = {"model": name, "arm": label, "suite": spec[0], "mode": spec[1], "rank": spec[2],
                           "doc_id": di, "document_index": start+bi, "offset": corpus["models"][name]["documents"][start+bi]["offset"],
                           "prefix_length": n, "target_id": int(targets[bi]), "kl": float(divergence[bi]),
                           "nll": float(nll[bi]), "reference_nll": float(ref_nll[bi]),
                           "argmax_agrees": flags[bi][0],
                           "correct": flags[bi][1],
                           "empty_row_policy": empty_policy,
                           "svd_driver": RECON["svd_driver"],
                           "svd_parallel_schedule": RECON["parallel_svd"],
                           "evaluation_batch_start": start, "evaluation_batch_size": len(sequences),
                           "attention_validation_batch": dict(stats),
                           "corpus_manifest_sha256": corpus_hash}
                    out.write(json.dumps(row, allow_nan=False) + "\n")
                    rows.append(row); seen.add((label, di))
            out.flush()
            if (start + len(sequences)) % 16 == 0:
                print(f"DOWNSTREAM {name}: {start+len(sequences)}/{len(windows)} documents, elapsed={time.perf_counter()-started:.1f}s", flush=True)
    # Rebuild checks from the raw ledger so a resumed process retains checks
    # performed before the interruption as well as those performed now.
    validation = {}
    checked_batches = set()
    for row in rows:
        batch_key = (row["arm"], row["evaluation_batch_start"], row["evaluation_batch_size"])
        if batch_key in checked_batches:
            continue
        checked_batches.add(batch_key)
        dest = validation.setdefault(row["arm"], {})
        for key, value in row["attention_validation_batch"].items():
            if isinstance(value, bool):
                dest[key] = dest.get(key, True) and value
            elif key.startswith("max_"):
                dest[key] = max(dest.get(key, 0), value)
            else:
                dest[key] = dest.get(key, 0) + value
    results = {}
    for suite, path in outputs.items():
        if path.exists():
            results[suite] = json.loads(path.read_text(encoding="utf-8"))
            continue
        arms = {arm_label(spec): summarize_records([r for r in rows if r["arm"] == arm_label(spec)]) for spec in specs if spec[0] == suite}
        for label, arm in arms.items():
            arm["uniform_completion"] = completion_summary(validation[label])
            expected_last = len(windows)*model.config.num_hidden_layers*model.config.num_attention_heads
            if (arm["uniform_completion"]["rows_total"] != n*expected_last
                    or arm["uniform_completion"]["last_query_rows_total"] != expected_last):
                raise RuntimeError("Completion counters do not cover all layer/head/query rows")
        if any(v["n_documents"] != 256 for v in arms.values()):
            raise RuntimeError("Incomplete arm; no conditional-subset reporting")
        result = {"schema_version": 2, "model": name, "dtype": str(dtype), "prefix_length": n,
                  "n_documents_effective": 256, "n_prefix_tokens": 256*n, "n_evaluated_next_tokens_per_arm": 256,
                  "batch": batch, "seed": 0, "corpus_manifest_sha256": corpus_hash,
                  "target_excluded_from_model_input": True, "identity_kl_exactly_zero": True,
                  "empty_row_policy": empty_policy,
                  "rank_definition": "factorization rank before causal mask, clamp and row normalization",
                  "same_empty_row_policy_for_all_reconstructions": True,
                  "validation_schedule": "Every row/value checked on device; counters and violations synchronized and validated after each forward, before KL/NLL or raw writes",
                  "validation_schedule_equivalence": schedule_sanity,
                  "svd_implementation": svd_implementation,
                  "uniform_completion_formula": "1/(k-q+i+1) at j<=k-q+i; no original-row completion",
                  "legacy_upper_diagonal_mass": json.loads(Path("out/phase2_legacy_mass_v2.json").read_text(encoding="utf-8"))[name],
                  "suffix_invariance": sanity, "attention_validation": validation,
                  "normalized_fp32_row_atol": NORMALIZED_ROW_ATOL,
                  "cast_row_atol": NORMALIZED_ROW_ATOL + torch.finfo(dtype).eps/2,
                  "pairs_path": pairpath.as_posix(), "arms": arms, "elapsed_seconds": time.perf_counter()-started}
        write_json_new(path, result)
        results[suite] = result
    del model, ref, other
    gc.collect(); torch.cuda.empty_cache()
    progress("V1 downstream", f"{name}; 256 independent articles; {len(specs)} arms; identity/suffix/attention checks passed", time.perf_counter()-started,
             "flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models " + name)
    return results

def run_suite(models=MODELS, suites=("phase2", "phase7"), batch=2, empty_policy="uniform"):
    started = time.perf_counter()
    results = {s: {} for s in suites}
    for name in models:
        for suite, result in run_model(name, batch=batch, suites=suites, empty_policy=empty_policy).items():
            results[suite][name] = result
    if list(models) == MODELS:
        for suite in suites:
            target = Path("out") / ("phase2_downstream_v2.json" if suite == "phase2" else "phase7_editability_v2.json")
            if not target.exists():
                write_json_new(target, {"_meta": {"n_documents_per_model": 256, "prefix_length": 128, "last_token_only": True}, **results[suite]})
    progress("V1 command complete", f"{len(models)} models, suites={suites}", time.perf_counter()-started,
             "flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B " + " ".join(sys.argv))
    return results

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--suites", nargs="+", choices=["phase2", "phase7"], default=["phase2", "phase7"])
    ap.add_argument("--empty-row-policy", choices=["uniform"], default="uniform")
    ap.add_argument("--aggregate-only", action="store_true", help="CPU-only: require all per-model results before aggregation")
    args = ap.parse_args()
    if args.aggregate_only:
        missing = [str(Path("out")/f"{s}_{slug(m)}_v2.json") for m in args.models for s in args.suites
                   if not (Path("out")/f"{s}_{slug(m)}_v2.json").exists()]
        if missing:
            raise FileNotFoundError(f"Cannot aggregate incomplete results: {missing}")
    run_suite(args.models, tuple(args.suites), args.batch, args.empty_row_policy)

if __name__ == "__main__":
    main()
