"""Same-item, coupled sink/non-sink mass controls for historical retrieval.

Only new artifacts are published. The five probe configurations use their
historical float32 precision; KV Qwen-3B uses bfloat16. No randomization is
chosen using outcomes. Both edited trajectories remove the same feasible q.
"""
from revision_v3_stats import (
    slug, sha256_file, write_json_new, describe, bootstrap_item_gains,
    mcnemar, seed_stratified_permutation, holm,
)
from revision_v3_probes import load_probe, paths, dtype_for, PROBE_MODELS, KV_MODELS, SEEDS
from phase37_mass_matched import Checks, matched_edit, random_order
import phase2_downstream as p2
import phase8_lostmiddle as p8
import argparse
from datetime import datetime, timezone
import gc
import json
import os
from pathlib import Path
import time
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AttentionInterface

torch.set_num_threads(4)
BETA = .25
FAMILY = [("phase8", m) for m in PROBE_MODELS] + [("phase11", m) for m in KV_MODELS]
PROTOCOL = Path("out/phase53_massmatched_retrieval_protocol_v3.json")
LOG = Path("out/_rerun_logs/massmatched_retrieval_v3_progress.md")
STATE = {}
SOURCE_FILES = ["phase53_massmatched_retrieval.py", "phase54_massmatched_retrieval_run.py",
    "phase37_mass_matched.py", "revision_v3_stats.py", "revision_v3_probes.py",
    "phase2_downstream.py", "phase8_lostmiddle.py", "sampling.py"]


def log(message):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(LOG, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o666)
    try:
        os.write(fd, ("\n- " + datetime.now(timezone.utc).isoformat(timespec="seconds")
                      + " | " + message + "\n").encode("utf-8"))
    finally:
        os.close(fd)


def hashes():
    return {p: sha256_file(p) for p in SOURCE_FILES}


def job_paths(task, model, seed, pilot=False):
    tag = (f"phase53_pilot_{task}" if pilot else f"{task}_massmatched_items")
    tag += f"_{slug(model)}_s{seed}_v3"
    return Path("out") / (tag + ".json"), Path("out/pairs") / (tag + ".jsonl")


def selected_indices(arrays, manifest):
    n = manifest["n"]
    selected = np.flatnonzero((arrays["positions"] >= .25*n) &
                              (arrays["positions"] <= .75*n))
    expected = 2000 if manifest["task"] == "phase8" else 600
    if len(selected) != expected:
        raise ValueError("Unexpected historical middle-window item count")
    return selected


def historical(task, model, seed, arrays, manifest):
    path = Path(f"out/{task}_items_{slug(model)}_s{seed}_historical_v3.json")
    meta = json.loads(path.read_text(encoding="utf-8"))
    pairpath = Path(meta["pairs_path"])
    assert sha256_file(pairpath) == meta["pairs_sha256"]
    assert meta["payload_sha256"] == manifest["payload_sha256"]
    assert meta["native_identity_logits_bit_equal"]
    rows = [json.loads(line) for line in pairpath.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 2*manifest["n_items"]
    by = {(r["arm"], r["trial_id"]): r for r in rows}
    assert len(by) == len(rows)
    for arm in ["1.0", "0.25"]:
        for i in range(manifest["n_items"]):
            r = by[arm, i]
            assert (r["position"], r["item"], r["target_id"]) == (
                int(arrays["positions"][i]), int(arrays["item_index"][i]), int(arrays["targets"][i]))
            assert r["correct"] == (r["prediction_id"] == r["target_id"])
    return by, {"job_path": path.as_posix(), "job_sha256": sha256_file(path),
                "pairs_path": pairpath.as_posix(), "pairs_sha256": meta["pairs_sha256"]}


def item_keys(task, model, seed, indices, arrays):
    return [f"{task}|{model}|seed{seed}|position{arrays['positions'][i]}|item{arrays['item_index'][i]}"
            for i in indices]


def reset(keys, disable=False):
    STATE.clear()
    STATE.update(keys=keys, layer=0, disable=disable, base=Checks(), sink=Checks(),
                 control=Checks(), mass=Checks())


def reconstruct(weights):
    b = len(STATE["keys"])
    if weights.shape[0] != 2*b:
        raise ValueError("Expected two matching batches, sink followed by control")
    layer = STATE["layer"]
    STATE["layer"] += 1
    p2.validate_attention(weights, STATE["base"])
    if STATE["disable"]:
        return weights
    h, q, k = weights.shape[1:]
    # Reuse phase37's exact random-order rule, separately keyed for every
    # item. Heads and queries have their own fixed random ordering; batching
    # cannot change an item's ordering, and targets are never inspected.
    order = torch.cat([random_order(key, layer, h, q, k, weights.device)
                       for key in STATE["keys"]], dim=0)
    sink, control, budget = matched_edit(weights[:b], weights[b:], BETA, order, STATE["mass"])
    output = []
    for before, edited, stats in [(weights[:b], sink, STATE["sink"]),
                                   (weights[b:], control, STATE["control"])]:
        normalized = p2.normalize_reconstruction(edited, before, stats, "uniform")
        # q=0 preserves the original native row exactly, including row 0,
        # sink-only rows and rounding in native bfloat16 distributions.
        result = torch.where((budget == 0)[..., None], before, normalized)
        stats.add_scalar("sink_edit_rows_preserved_no_alternative", (budget == 0).sum())
        stats.add_scalar("sink_edit_last_query_rows_preserved", (budget[..., -1] == 0).sum())
        if q == k:
            stats.add_scalar("sink_edit_first_row_changes", (result[..., 0, :] != before[..., 0, :]).sum())
        p2.validate_attention(result, stats)
        output.append(result)
    return torch.cat(output, dim=0)


def attention_forward(module, query, key, value, attention_mask, scaling=None, dropout=0., **kwargs):
    if module.training or dropout:
        raise RuntimeError("Evaluation requires eval mode and zero dropout")
    # Match the historical phase8 attention arithmetic, including BF16 KV.
    # This callback only changes the attention probabilities after softmax.
    if scaling is None:
        scaling = query.size(-1) ** -.5
    nrep = getattr(module, "num_key_value_groups", 1)
    key, value = p8._repeat_kv(key, nrep), p8._repeat_kv(value, nrep)
    weights = torch.matmul(query, key.transpose(-1, -2)) * scaling
    q, k = weights.shape[-2:]
    causal = torch.full((q, k), float("-inf"), device=weights.device, dtype=weights.dtype)
    weights = weights + torch.triu(causal, diagonal=1+k-q)
    weights = F.softmax(weights, dim=-1).type(value.dtype)
    weights = reconstruct(weights)
    return torch.matmul(weights, value).transpose(1, 2), weights


def finish(n_layers):
    assert STATE["layer"] == n_layers
    result = {}
    for key in ["base", "sink", "control", "mass"]:
        STATE[key].finalize("mass-matched retrieval " + key)
        result[key] = dict(STATE[key])
    return result


@torch.inference_mode()
def paired_forward(model_obj, ids, keys, disable=False):
    reset(keys, disable)
    model_obj.set_attn_implementation("revision_v3_retrieval_mass")
    x = torch.tensor(ids, device="cuda").repeat(2, 1)
    outputs = model_obj(x)
    scores = outputs.logits[:, -1, :].clone()
    del outputs, x
    stats = finish(model_obj.config.num_hidden_layers)
    if not bool(torch.isfinite(scores).all()):
        raise RuntimeError("Nonfinite logits; no omitted item or substituted prediction")
    return scores, stats


def cpu_checks():
    began = time.perf_counter()
    cases = 0
    for dtype in [torch.float32, torch.bfloat16]:
        for q, k in [(8, 8), (1, 9), (3, 9)]:
            gen = torch.Generator().manual_seed(0)
            weights = torch.rand((2, 3, q, k), generator=gen) * p2.causal_support(q, k, "cpu")
            weights = (weights/weights.sum(-1, keepdim=True)).to(dtype)
            order = torch.cat([random_order(key, 0, 3, q, k, "cpu") for key in ["a", "b"]])
            again = torch.cat([random_order(key, 0, 3, q, k, "cpu") for key in ["b", "a"]]).flip(0)
            assert torch.equal(order, again), "Item randomization depends on batch order"
            stats = Checks()
            s, c, budget = matched_edit(weights, weights.flip(0), BETA, order, stats)
            stats.finalize("CPU feasible equality")
            assert torch.equal(c[..., 0], weights.flip(0)[..., 0].double())
            for before, edited in [(weights, s), (weights.flip(0), c)]:
                st = Checks()
                normalized = p2.normalize_reconstruction(edited, before, st, "uniform")
                result = torch.where((budget == 0)[..., None], before, normalized)
                p2.validate_attention(result, st)
                st.finalize("CPU normalized")
                if q == k:
                    assert torch.equal(result[..., 0, :], before[..., 0, :])
            cases += 1
    # Analytic two-column row: requested .45, feasible .4. Sink -> (1/3,2/3),
    # control -> (1,0), with equal removal before the same normalization.
    a = torch.tensor([[[[1., 0.], [.6, .4]]]], dtype=torch.float64)
    st = Checks()
    s, c, budget = matched_edit(a, a, BETA, torch.zeros(1, 1, 2, 1, dtype=torch.long), st)
    st.finalize("analytic matching")
    assert torch.allclose(budget[0, 0], torch.tensor([0., .4], dtype=torch.float64), rtol=0., atol=1e-15)
    assert torch.allclose((s/s.sum(-1, keepdim=True))[0, 0, 1], torch.tensor([1/3, 2/3], dtype=torch.float64), rtol=0., atol=1e-15)
    assert torch.equal((c/c.sum(-1, keepdim=True))[0, 0, 1], torch.tensor([1., 0.], dtype=torch.float64))
    cases += 1
    for sink_only in [True, False]:
        a = torch.zeros(1, 2, 8, 8)
        if sink_only:
            a[..., 0] = 1
        else:
            a += torch.eye(8)
        st = Checks()
        s, c, budget = matched_edit(a, a, BETA, random_order("degenerate", 0, 2, 8, 8, "cpu"), st)
        st.finalize("no alternative")
        assert torch.equal(s, a.double()) and torch.equal(c, a.double()) and not bool(budget.any())
        cases += 1
    # Discordance-free paired contrasts must remain exactly null.
    null = mcnemar([True, False], [True, False])
    assert null["mcnemar_exact_pvalue"] == 1.
    assert seed_stratified_permutation([null]*3)["pvalue"] == 1.
    result = {"all_passed": True, "n_attention_cases": cases,
              "item_randomization_batch_invariant": True, "analytic_two_column_passed": True,
              "null_paired_statistics_passed": True, "source_hashes": hashes(),
              "elapsed_seconds": time.perf_counter()-began}
    write_json_new("out/phase53_massmatched_retrieval_cpu_checks_v3.json", result)
    log(f"CPU checks passed: {cases} attention cases; {result['elapsed_seconds']:.3f}s")


def freeze_protocol():
    jobs = []
    for task, model in FAMILY:
        for seed in SEEDS:
            arrays, meta = load_probe(task, model, seed)
            selected = selected_indices(arrays, meta)
            _, old = historical(task, model, seed, arrays, meta)
            jobs.append({"task": task, "model": model, "seed": seed,
                "n_independent_items": len(selected), "dtype": str(dtype_for(task, model, "historical")),
                "middle_positions": sorted(set(arrays["positions"][selected].tolist())),
                "manifest_path": paths(task, model, seed)[1].as_posix(),
                "manifest_sha256": sha256_file(paths(task, model, seed)[1]),
                "payload_sha256": meta["payload_sha256"], "historical": old})
    value = {"schema_version": 3, "beta": BETA, "jobs": jobs, "source_hashes": hashes(),
        "primary_family_7": [list(k) for k in FAMILY],
        "scope": "historical middle window only: phase8 6000/model, phase11 1800/model",
        "budget_rule": "q=min(.75*sink_sinkarm,nonsink_sinkarm,nonsink_controlarm); absolute row0 q=0",
        "randomization": "phase37.random_order; seed0 plus item(task/model/seed/position/item), layer, head and query; no targets",
        "normalization": "phase37 float64 removal and shared causal normalization; q0 rows preserved exactly",
        "coupling": "sink and control trajectories evaluated together at each layer/head/query; same feasible q after feedback",
        "precision": "historical: probe all five FP32; KV GPT2-medium FP32, Qwen3B BF16",
        "statistics": "2000 bootstrap draws seed0, paired items within seed x position; raw item median and median seed accuracy gain; pooled mean secondary",
        "primary_test": "exact paired label permutation within seed; statistic median three seed gains, sink minus control; Holm7",
        "per_seed_test": "exact McNemar on discordant items, sink minus control",
        "historical_uncapped_sink": "stored separately as a secondary reference; not substituted for the capped sink arm",
        "created_utc": datetime.now(timezone.utc).isoformat()}
    write_json_new(PROTOCOL, value)
    log("Protocol frozen before main inference: 21 jobs, all 7 configurations, fixed items/seeds/orders/precision/Holm7")


@torch.inference_mode()
def run_job(task, model, seed, pilot=False):
    began = time.perf_counter()
    output, pairpath = job_paths(task, model, seed, pilot)
    source = hashes()
    arrays, manifest = load_probe(task, model, seed)
    selected = selected_indices(arrays, manifest)
    old, old_meta = historical(task, model, seed, arrays, manifest)
    if output.exists():
        result = json.loads(output.read_text(encoding="utf-8"))
        assert result["source_hashes"] == source
        if not pilot:
            assert result["pairs_sha256"] == sha256_file(pairpath)
        return result
    if not pilot:
        protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
        assert protocol["source_hashes"] == source
        plan = next(j for j in protocol["jobs"] if (j["task"], j["model"], j["seed"]) == (task, model, seed))
        assert plan["payload_sha256"] == manifest["payload_sha256"] and plan["historical"] == old_meta
    dtype = dtype_for(task, model, "historical")
    batch = 16 if task == "phase8" else (4 if model == "Qwen/Qwen2.5-3B" else 8)
    model_obj = AutoModelForCausalLM.from_pretrained(model, revision=manifest["revision"],
        dtype=dtype, attn_implementation="eager", local_files_only=True).to("cuda").eval()
    AttentionInterface.register("revision_v3_retrieval_mass", attention_forward)
    n_layers = model_obj.config.num_hidden_layers
    n_heads = model_obj.config.num_attention_heads
    first = selected[:batch]
    keys = item_keys(task, model, seed, first, arrays)
    x = torch.tensor(arrays["input_ids"][first], device="cuda").repeat(2, 1)
    native = model_obj(x).logits[:, -1, :].clone()
    identity, identity_checks = paired_forward(model_obj, arrays["input_ids"][first], keys, disable=True)
    assert torch.equal(native, identity), "Disabled coupled callback changed native attention/logits"
    del x, native, identity
    if pilot:
        scores, checks = paired_forward(model_obj, arrays["input_ids"][first], keys)
        assert scores.shape[0] == 2*len(first)
        result = {"task": task, "model": model, "seed": seed, "dtype": str(dtype),
            "source_hashes": source, "native_identity_logits_bit_equal": True,
            "identity_checks": identity_checks, "edited_checks": checks,
            "batch_independent_items": batch, "same_item_edited_copies": 2,
            "peak_cuda_allocated_bytes": torch.cuda.max_memory_allocated(),
            "elapsed_seconds": time.perf_counter()-began}
        assert hashes() == source
        write_json_new(output, result)
        log(f"Pilot passed {task} {model} s{seed}: {result['elapsed_seconds']:.3f}s")
        print(json.dumps(result, allow_nan=False), flush=True)
        return result
    records = []
    validations = []
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    with pairpath.open("x", encoding="utf-8") as f:
        for position in sorted(set(arrays["positions"][selected].tolist())):
            group = selected[arrays["positions"][selected] == position]
            assert len(group) == manifest["n_per_position"]
            for offset in range(0, len(group), batch):
                indices = group[offset:offset+batch]
                keys = item_keys(task, model, seed, indices, arrays)
                ids = arrays["input_ids"][indices]
                # Identity retains its original batch and full historical LM
                # head shape. Check EVERY prediction against saved identity.
                model_obj.set_attn_implementation("eager")
                x = torch.tensor(ids, device="cuda")
                outputs = model_obj(x)
                scores = outputs.logits[:, -1, :]
                if not bool(torch.isfinite(scores).all()):
                    raise RuntimeError("Nonfinite identity logits")
                baseline = scores.argmax(-1).cpu().numpy()
                del outputs, scores, x
                for j, i in enumerate(indices):
                    assert int(baseline[j]) == old["1.0", int(i)]["prediction_id"], "Historical identity prediction changed"
                scores, checks = paired_forward(model_obj, ids, keys)
                predictions = scores.argmax(-1).cpu().numpy()
                del scores
                row_distributions = len(indices)*n_heads*n_layers
                assert checks["mass"]["mass_rows_total"] == row_distributions*manifest["n"]
                assert checks["mass"]["last_query_rows_total"] == row_distributions
                assert checks["sink"]["sink_edit_rows_preserved_no_alternative"] >= row_distributions
                assert checks["control"]["sink_edit_rows_preserved_no_alternative"] >= row_distributions
                validations.append({"batch_indices": indices.tolist(), "checks": checks})
                for j, i in enumerate(indices):
                    target = int(arrays["targets"][i])
                    row = {"task": task, "model": model, "seed": seed, "position": int(position),
                        "item": int(arrays["item_index"][i]), "trial_id": int(i), "target_id": target,
                        "payload_sha256": manifest["payload_sha256"], "item_randomization_key": keys[j],
                        "identity_prediction": int(baseline[j]), "sink_prediction": int(predictions[j]),
                        "control_prediction": int(predictions[len(indices)+j]),
                        "historical_uncapped_sink_prediction": old["0.25", int(i)]["prediction_id"]}
                    for arm in ["identity", "sink", "control", "historical_uncapped_sink"]:
                        row[arm+"_correct"] = row[arm+"_prediction"] == target
                    f.write(json.dumps(row, allow_nan=False)+"\n")
                    records.append(row)
                f.flush()
            print(f"MATCHED {task} {model} s{seed} position{position}: {len(records)} items; {time.perf_counter()-began:.1f}s", flush=True)
    del model_obj
    gc.collect()
    torch.cuda.empty_cache()
    assert len(records) == len(selected)
    assert hashes() == source
    result = {"schema_version": 3, "task": task, "model": model, "seed": seed,
        "dtype": str(dtype), "beta_nominal": BETA, "batch_independent_items": batch,
        "same_item_edited_copies": 2, "revision": manifest["revision"], "source_hashes": source,
        "protocol_sha256": sha256_file(PROTOCOL), "payload_sha256": manifest["payload_sha256"],
        "manifest_path": paths(task, model, seed)[1].as_posix(), "historical": old_meta,
        "n_independent_items": len(records), "n_forward_predictions": 3*len(records),
        "native_identity_logits_bit_equal": True, "all_historical_identity_predictions_exact": True,
        "identity_checks": identity_checks, "batch_checks": validations,
        "pairs_path": pairpath.as_posix(), "pairs_sha256": sha256_file(pairpath),
        "peak_cuda_allocated_bytes": torch.cuda.max_memory_allocated(),
        "elapsed_seconds": time.perf_counter()-began}
    write_json_new(output, result)
    log(f"Completed {task} {model} s{seed}: {len(records)} independent items, all three arms, {result['elapsed_seconds']:.3f}s")
    return result


def contrast(rows, left, right):
    paired = [{"seed": r["seed"], "position": r["position"],
               "baseline_correct": r[right+"_correct"], "edited_correct": r[left+"_correct"]}
              for r in rows]
    result = bootstrap_item_gains(paired)
    result["item_difference_describe"] = describe(
        [int(r["edited_correct"])-int(r["baseline_correct"]) for r in paired], np.arange(len(rows)))
    result["by_seed"] = []
    for seed in SEEDS:
        selected = [r for r in paired if r["seed"] == seed]
        result["by_seed"].append({"seed": seed, **mcnemar(
            [r["baseline_correct"] for r in selected], [r["edited_correct"] for r in selected])})
    result["combined_seed_stratified_permutation"] = seed_stratified_permutation(result["by_seed"])
    return result


def analyze(task, model):
    rows = []
    jobs = []
    mass_totals = {}
    max_error = 0.
    for seed in SEEDS:
        path, pairpath = job_paths(task, model, seed)
        job = json.loads(path.read_text(encoding="utf-8"))
        assert job["source_hashes"] == hashes() and job["protocol_sha256"] == sha256_file(PROTOCOL)
        assert job["pairs_sha256"] == sha256_file(pairpath)
        assert job["native_identity_logits_bit_equal"] and job["all_historical_identity_predictions_exact"]
        arrays, manifest = load_probe(task, model, seed)
        selected = selected_indices(arrays, manifest)
        current = [json.loads(line) for line in pairpath.read_text(encoding="utf-8").splitlines()]
        assert len(current) == len(selected) == job["n_independent_items"]
        assert [r["trial_id"] for r in current] == selected.tolist()
        for r, i in zip(current, selected):
            assert (r["target_id"], r["position"], r["item"]) == (int(arrays["targets"][i]),
                int(arrays["positions"][i]), int(arrays["item_index"][i]))
            assert r["payload_sha256"] == manifest["payload_sha256"]
            for arm in ["identity", "sink", "control", "historical_uncapped_sink"]:
                assert r[arm+"_correct"] == (r[arm+"_prediction"] == r["target_id"])
        for batch in job["batch_checks"]:
            for name, checks in batch["checks"].items():
                assert all(checks.get(k, 0) == 0 for k in Checks.violation_keys), (name, checks)
            m = batch["checks"]["mass"]
            max_error = max(max_error, m["max_mass_match_error"])
            for key in ["mass_rows_total", "mass_requested", "mass_removed_each_arm", "mass_rows_capped",
                        "mass_rows_zero_request", "last_query_mass_requested", "last_query_mass_removed_each_arm",
                        "last_query_rows_capped", "last_query_rows_total"]:
                mass_totals[key] = mass_totals.get(key, 0)+m[key]
        rows += current
        jobs.append({"path": path.as_posix(), "sha256": sha256_file(path),
                     "pairs_path": pairpath.as_posix(), "pairs_sha256": job["pairs_sha256"],
                     "elapsed_seconds": job["elapsed_seconds"], "n_independent_items": len(current)})
    assert len({(r["seed"], r["position"], r["item"]) for r in rows}) == len(rows)
    arms = {}
    for arm in ["identity", "sink", "control", "historical_uncapped_sink"]:
        per_seed = [{"seed": s, "n_items": sum(r["seed"] == s for r in rows),
                     "n_correct": sum(r[arm+"_correct"] for r in rows if r["seed"] == s)} for s in SEEDS]
        for s in per_seed:
            s["accuracy"] = s["n_correct"]/s["n_items"]
        arms[arm] = {"n_correct": sum(r[arm+"_correct"] for r in rows), "n_items": len(rows),
            "pooled_accuracy_secondary": float(np.mean([r[arm+"_correct"] for r in rows])),
            "median_seed_accuracy": float(np.median([s["accuracy"] for s in per_seed])), "by_seed": per_seed}
    mass_totals["max_mass_match_error"] = max_error
    mass_totals["removed_over_requested"] = mass_totals["mass_removed_each_arm"]/mass_totals["mass_requested"]
    mass_totals["fraction_rows_capped"] = mass_totals["mass_rows_capped"]/mass_totals["mass_rows_total"]
    return {"model": model, "task": task, "dtype": str(dtype_for(task, model, "historical")),
        "n_independent_items": len(rows), "seeds": SEEDS, "positions": sorted({r["position"] for r in rows}),
        "arms": arms, "sink_minus_identity": contrast(rows, "sink", "identity"),
        "control_minus_identity": contrast(rows, "control", "identity"),
        "sink_minus_control": contrast(rows, "sink", "control"),
        "historical_uncapped_sink_minus_identity_secondary": contrast(rows, "historical_uncapped_sink", "identity"),
        "mass_accounting": mass_totals, "jobs": jobs,
        "all_historical_identity_predictions_exact": True}


def aggregate():
    began = time.perf_counter()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["source_hashes"] == hashes()
    results = {k: analyze(*k) for k in FAMILY}
    corrected = holm([results[k]["sink_minus_control"]["combined_seed_stratified_permutation"]["pvalue"] for k in FAMILY])
    for k, p in zip(FAMILY, corrected):
        results[k]["sink_minus_control"]["combined_seed_stratified_permutation"]["p_holm_family_7"] = p
    for task, models in [("phase8", PROBE_MODELS), ("phase11", KV_MODELS)]:
        value = {"_meta": {"schema_version": 3, "protocol_path": PROTOCOL.as_posix(),
            "protocol_sha256": sha256_file(PROTOCOL), "source_hashes": hashes(),
            "beta_nominal": BETA, "all_items_retained": True,
            "primary_family_7": protocol["primary_family_7"], "primary_contrast": "sink minus mass-matched random non-sink control",
            "budget_rule": protocol["budget_rule"], "randomization": protocol["randomization"],
            "statistics": protocol["statistics"], "primary_test": protocol["primary_test"],
            "accuracy_note": "correct-count/n and median seed accuracy both given; gains and CIs computed as paired contrasts, not differences of marginal medians",
            "uncapped_reference_note": "historical beta=.25 arm differs from the feasible capped sink intervention; shown separately",
            "elapsed_seconds_joint_aggregation": time.perf_counter()-began},
            "models": {m: results[task, m] for m in models}}
        write_json_new(f"out/{task}_massmatched_items_v3.json", value)
    log(f"Final aggregation complete: 7 configurations, 33600 independent within-configuration items; {time.perf_counter()-began:.3f}s")
    print(json.dumps({"all_passed": True, "elapsed_seconds": time.perf_counter()-began,
        "results": [{"task": t, "model": m, "n": results[t, m]["n_independent_items"],
            "accuracy_secondary": {a: results[t, m]["arms"][a]["pooled_accuracy_secondary"] for a in ["identity", "sink", "control"]},
            "sink_minus_control": results[t, m]["sink_minus_control"]} for t, m in FAMILY]}, allow_nan=False), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu-checks", action="store_true")
    parser.add_argument("--freeze-protocol", action="store_true")
    parser.add_argument("--aggregate-only", action="store_true")
    parser.add_argument("--pilot-only", action="store_true")
    parser.add_argument("--task", choices=["phase8", "phase11"])
    parser.add_argument("--model")
    parser.add_argument("--seed", type=int, choices=SEEDS)
    args = parser.parse_args()
    if args.cpu_checks:
        cpu_checks()
    elif args.freeze_protocol:
        freeze_protocol()
    elif args.aggregate_only:
        aggregate()
    else:
        if (args.task, args.model) not in FAMILY or args.seed is None:
            parser.error("Inference requires a historical task/model pair and seed")
        run_job(args.task, args.model, args.seed, args.pilot_only)


if __name__ == "__main__":
    main()
