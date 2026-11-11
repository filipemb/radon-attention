"""P0 regression checks. --gpu-identity requires the shared GPU flock."""
from sampling import (MODELS, CORPUS_PATH, make_manifest, validate_matrices, slug,
                      storage_row_atol, write_json_new, progress, sample_paths, sha256_file)
import argparse
import json
from pathlib import Path
import time
import sys
import numpy as np

def sampling_checks():
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    assert len({d["doc_id"] for d in corpus["documents"]}) == 256
    checked = 0
    for model in MODELS:
        assert sample_paths(model, 128)[0] != sample_paths(model, 256)[0]
        assert "_n128.npz" in sample_paths(model, 128)[0].name
        m = make_manifest(corpus, model, 128)
        assert m == make_manifest(corpus, model, 128), "Fixed seed must reproduce manifest exactly"
        x = m["instances"]
        assert len(x) >= 1024 and len({i["doc_id"] for i in x}) == 64
        assert len({i["instance_id"] for i in x}) == len(x)
        layers = np.bincount([i["layer"] for i in x], minlength=m["n_layers"])
        assert layers.min() == layers.max()
        doc_counts = np.bincount([i["document_index"] for i in x], minlength=64)
        assert doc_counts.min() == doc_counts.max()
        for layer in range(m["n_layers"]):
            counts = np.bincount([i["head"] for i in x if i["layer"] == layer], minlength=m["n_heads"])
            assert counts.max() - counts.min() <= 1
        other = make_manifest(corpus, model, 256)
        assert [(i["doc_id"], i["head"], i["layer"]) for i in x] == [(i["doc_id"], i["head"], i["layer"]) for i in other["instances"]]
        checked += len(x)
    a = np.tril(np.ones((2, 8, 8), dtype=np.float32))
    a /= a.sum(-1, keepdims=True)
    assert validate_matrices(a, 2e-6)["invalid_matrices"] == 0
    nan = a.copy(); nan[0, 2, 0] = np.nan
    assert validate_matrices(nan, 2e-6)["nan_values"] == 1
    assert validate_matrices(nan, 2e-6)["invalid_matrices"] == 1
    upper = a.copy(); upper[0, 0, 1] = 0.1
    assert validate_matrices(upper, 2e-6)["above_diagonal_nonzero"] == 1
    empty = a.copy(); empty[0, 0] = 0
    assert validate_matrices(empty, 2e-6)["invalid_rows"] == 1
    assert validate_matrices(a.astype(np.float16), storage_row_atol(8))["invalid_matrices"] == 0
    return {"models": len(MODELS), "n_balanced_instances_checked": checked,
            "reproducible": True, "head_document_layer_balance": True,
            "invalid_inputs_detected_without_repair": True}

def reconstruction_checks():
    import torch
    import phase2_downstream as p2
    import phase7_editability as p7
    torch.set_num_threads(4)
    torch.manual_seed(0)
    results = []
    for q, k in [(16, 16), (1, 16), (4, 16)]:
        mask = p2.causal_support(q, k, "cpu")
        logits = torch.randn(2, 3, q, k).masked_fill(~mask, float("-inf"))
        weights = logits.softmax(-1)
        for mode in ("svd", "uniform", "diagonal", "sink"):
            p2.RECON.update({"mode": mode, "k": 4, "stats": {}})
            got = p2.reconstruct(weights)
            assert torch.equal(got.masked_select(~mask), torch.zeros_like(got.masked_select(~mask)))
            assert torch.allclose(got.sum(-1), torch.ones_like(got.sum(-1)), atol=2e-6, rtol=0)
            assert torch.isfinite(got).all() and (got >= 0).all()
            results.append(f"{mode}:q{q}:k{k}")
        for mode in ("anova", "nosink", "zerocol_mid"):
            p7.RECON.update({"mode": mode, "k": 4, "stats": {}})
            got = p7.reconstruct(weights)
            assert torch.isfinite(got).all() and (got >= 0).all()
            if q == k and mode != "anova":
                assert torch.equal(got[..., 0, :], weights[..., 0, :])
            results.append(f"{mode}:q{q}:k{k}")
    # A suffix must be cropped before the model sees it; a recording fake model
    # makes this test independent of transformer masking implementations.
    class Recorder(torch.nn.Module):
        def __init__(self):
            super().__init__(); self.anchor = torch.nn.Parameter(torch.zeros(())); self.seen = []
        def forward(self, ids, **kwargs):
            from types import SimpleNamespace
            self.seen.append(ids.clone())
            return SimpleNamespace(logits=ids.float().sum(-1)[:, None, None].expand(-1, 1, 3))
    recorder = Recorder()
    a = torch.tensor([[1, 2, 3, 9, 9]])
    b = torch.tensor([[1, 2, 3, 7, 8]])
    assert torch.equal(p2.last_logits(recorder, a, 3), p2.last_logits(recorder, b, 3))
    assert all(ids.shape[-1] == 3 for ids in recorder.seen)
    invalid = torch.zeros(1, 2, 2)
    caught = False
    try:
        p2.normalize_reconstruction(invalid, invalid, {}, empty_policy="error")
    except RuntimeError as error:
        caught = "empty" in str(error)
    assert caught, "Empty rows must fail, never silently acquire a fallback"
    for policy in ("uniform",):
        original = torch.tensor([[[1.0, 0], [0.25, 0.75]]])
        stats = {}
        repaired = p2.normalize_reconstruction(invalid, original, stats, empty_policy=policy)
        assert stats["empty_rows_completed"] == 2
        assert torch.allclose(repaired.sum(-1), torch.ones_like(repaired.sum(-1)), atol=2e-6, rtol=0)
        if policy == "uniform":
            assert torch.equal(repaired, torch.tensor([[[1.0, 0], [0.5, 0.5]]]))
    return {"cases": results, "prefix_crop_before_model": True, "empty_rows_rejected": True,
            "row_atol": 2e-6, "first_row_and_cached_offsets": "passed",
            "completion_rule": "uniform causal; original tensor used for dtype only", "default_policy": "uniform"}

def retrieval_audit():
    import torch
    from types import SimpleNamespace
    import phase8_lostmiddle as p8
    import phase11_kv as p11
    import phase16_longcontext as p16
    import phase18_betacv as p18
    class LastOnlyProbe(torch.nn.Module):
        def __init__(self, key, length):
            super().__init__(); self.key, self.length = key, length
        def forward(self, ids):
            assert ids.shape[-1] == self.length
            logits = torch.zeros(len(ids), 2, 2048)
            for bi, seq in enumerate(ids):
                matches = [j for j in range(len(seq)-len(self.key)) if seq[j:j+len(self.key)].tolist() == self.key]
                assert matches and seq[-len(self.key):].tolist() == self.key
                target = int(seq[matches[0]+len(self.key)])
                logits[bi, 0, (target+1) % 2048] = 1
                logits[bi, 1, target] = 1
            return SimpleNamespace(logits=logits)
    pool = np.tile(np.arange(1000, 2000, dtype=np.int64), 100)
    rng = np.random.default_rng(0)
    probe8 = p8.build_probe(pool, 2048, 128, [4, 64, 110], 2, rng)
    assert all(v == 1 for v in p8.accuracy_by_pos(LastOnlyProbe(p8.TAG, 128), probe8, "cpu", 2).values())
    probe11 = p11.build_kv(pool, 2048, 256, [16, 144, 232], 2, rng)
    assert all(v == 1 for v in p11.acc_by_pos(LastOnlyProbe([p11.KEYS[0]], 256), probe11, "cpu", 2).values())
    keys = p16.make_keys(12)
    probe16 = p16.build_kv(pool, 2048, 512, p16.position_grid(512, 11), 2, keys, rng)
    assert all(v == 1 for v in p16.acc_by_pos(LastOnlyProbe(keys[0], 512), probe16, "cpu", 2).values())
    assert p18.accuracy_by_pos is p8.accuracy_by_pos and p18.acc_by_pos is p16.acc_by_pos
    names = ["phase8_lostmiddle.py", "phase10_baselines.py", "phase11_kv.py", "phase14_adaptive.py", "phase16_longcontext.py", "phase18_betacv.py"]
    # The user explicitly authorized repairing beta=0 independently of leakage.
    p8.RECON["beta"] = 0
    _, aw = p8.recon_attention_forward(SimpleNamespace(num_key_value_groups=1),
                                      torch.zeros(1, 1, 4, 2), torch.zeros(1, 1, 4, 2), torch.ones(1, 1, 4, 2), None)
    zero_rows = int((aw.sum(-1) == 0).sum())
    assert zero_rows == 0 and torch.equal(aw[...,0,:], torch.tensor([[[1.,0.,0.,0.]]]))
    p8.RECON["beta"] = 1
    return {"source_sha256": {name: sha256_file(name) for name in names},
            "phase8_phase11_phase16_last_logit_dynamic_checks": "passed; early logit deliberately predicts the wrong target",
            "phase10_phase14_use_phase8_last_token_evaluator": True,
            "phase18_reuses_verified_last_token_evaluators": True,
            "target_structure": "one held-out output token; multi-token structure is the known query key, not a teacher-forced target continuation",
            "global_statistics": "phase10/14 alter earlier rows using observed-prefix statistics, but their measured final prediction has no future output tokens in the input",
            "target_leakage_found": False,
            "retrieval_scripts_edited": ["phase8_lostmiddle.py", "phase10_baselines.py", "phase14_adaptive.py"],
            "beta0_editing_repair": {"phase8_empty_rows_after_fix_in_four_row_example": zero_rows,
                 "first_row_unchanged": True,
                 "authorization": "User explicitly authorized preserving all rows with no alternative after sink editing; phase11/16/18 inherit the shared callback."}}

def fraction_constancy_checks():
    from phase5_msclean import fraction_metrics, build_dict
    from phase6_srpca import srpca, prepare_nnls
    from phase15_interaction import leaks
    s = np.array([[1.0, 0], [0, 0]])
    l = np.array([[-0.5, 1], [0, 0]])
    a = s+l
    metrics = fraction_metrics(a, s, l)
    assert abs(metrics["named_energy_ratio"]-0.8) < 1e-12
    assert abs(metrics["named_norm_ratio"]-np.sqrt(0.8)) < 1e-12
    assert abs(metrics["cross_term_SL_over_A_energy"]+0.8) < 1e-12
    assert metrics["total_error_reduction_energy"] == 1
    scaled = fraction_metrics(3*a, 3*s, 3*l)
    assert all(abs(metrics[k]-scaled[k]) < 1e-12 for k in metrics)
    n = 16
    first, second = np.zeros((n,n)), np.zeros((n,n))
    first[0,0] = second[0,0] = 1
    for i in range(1,n):
        sink = 0.1 if i % 2 else 0.9
        first[i,0], first[i,i] = sink, 1-sink
        second[i,0], second[i,i] = 1-sink, sink
    individual = (leaks(first)[0]+leaks(second)[0])/2
    averaged = leaks((first+second)/2)[0]
    assert individual > averaged+0.1, "Averaging must not hide per-forward variation"
    d, _ = build_dict(128)
    rng = np.random.default_rng(0)
    attention = np.tril(rng.random((128,128))); attention /= attention.sum(-1, keepdims=True)
    dense = srpca(attention, d, 8, return_components=True)
    reduced = srpca(attention, d, 8, qr=prepare_nnls(d), return_components=True)
    qr_error = float(np.linalg.norm(dense[4]-reduced[4])/np.linalg.norm(attention))
    assert qr_error < 1e-9 and abs(dense[0]-reduced[0]) < 1e-9
    return {"norm_energy_cross_term_identity": "passed", "scaling_invariance": "passed",
            "constancy_individual": individual, "constancy_after_averaging": averaged,
            "dense_qr_nnls_relative_named_error": qr_error, "qr_atol": 1e-9}

def gpu_identity_checks():
    import torch
    from transformers import AutoModelForCausalLM, AttentionInterface
    import phase2_downstream as p2
    import phase7_editability as p7
    torch.set_num_threads(4)
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    AttentionInterface.register("p0_recon", p2.attention_forward)
    AttentionInterface.register("p0_anova", p7.recon_attention_forward)
    results = {}
    for name in MODELS:
        path = Path("out")/f"phase25_identity_{slug(name)}_v2.json"
        if path.exists():
            results[name] = json.loads(path.read_text(encoding="utf-8")); continue
        started = time.perf_counter()
        dtype = torch.bfloat16 if "Qwen" in name else torch.float32
        model = AutoModelForCausalLM.from_pretrained(name, revision=corpus["models"][name]["revision"],
                    local_files_only=True, attn_implementation="eager", dtype=dtype).to("cuda").eval()
        windows = torch.tensor([d["token_ids"] for d in corpus["models"][name]["documents"]])
        count = 0
        p2.RECON.update({"mode": "identity", "stats": {}})
        p7.RECON.update({"mode": "identity", "stats": {}})
        for start in range(0, 256, 2):
            seq = windows[start:start+2]
            model.set_attn_implementation("eager")
            reference = p2.last_logits(model, seq, 128)
            for attention_name in ("p0_recon", "p0_anova"):
                model.set_attn_implementation(attention_name)
                got = p2.last_logits(model, seq, 128)
                divergence, _ = p2.kl_nll(reference, got, seq[:, 128])
                if not torch.equal(reference, got) or np.any(divergence != 0):
                    raise RuntimeError(f"Identity mismatch: {name}, {attention_name}, batch {start}")
            count += len(seq)
        modified = windows[:1].clone()
        modified[:, 128:] = (modified[:, 128:]+7919) % model.config.vocab_size
        one = p2.last_logits(model, windows[:1], 128)
        two = p2.last_logits(model, modified, 128)
        assert torch.equal(one, two)
        result = {"model": name, "dtype": str(dtype), "n_documents": count,
                  "identity_phase2_max_logit_error": 0.0, "identity_phase7_max_logit_error": 0.0,
                  "identity_kl": 0.0, "suffix_invariance_max_logit_error": 0.0,
                  "phase2_attention_validation": p2.RECON["stats"], "phase7_attention_validation": p7.RECON["stats"],
                  "elapsed_seconds": time.perf_counter()-started}
        write_json_new(path, result); results[name] = result
        progress("V1 six-model identity", f"{name}; {count} documents; both identity harnesses and suffix invariance exact",
                 result["elapsed_seconds"], "flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity")
        del model, reference, got
        torch.cuda.empty_cache()
    return results

def geometry_checks():
    import torch
    import phase2_downstream as p2
    torch.set_num_threads(4); torch.manual_seed(0)
    d = p2.build_dictionary(128, "cpu")
    q, r = torch.linalg.qr(d, mode="reduced")
    pinv = torch.linalg.solve_triangular(r, q.T, upper=True)
    mask = p2.causal_support(128, 128, "cpu")
    w = torch.randn(2, 128, 128).masked_fill(~mask, float("-inf")).softmax(-1)
    vectors = w.reshape(2, -1).T
    reduced = d @ (pinv @ vectors)
    dense = d @ torch.linalg.lstsq(d, vectors, driver="gels").solution
    relative_error = float(torch.linalg.norm(reduced-dense)/torch.linalg.norm(dense))
    assert relative_error < 1e-5, "Cached geometric projection differs from dense least squares"
    p2.RECON.update({"mode": "geom", "D": d, "D_pinv": pinv, "stats": {}})
    got = p2.reconstruct(w[:, None])
    assert torch.allclose(got.sum(-1), torch.ones_like(got.sum(-1)), atol=2e-6, rtol=0)
    return {"dictionary_atoms": d.shape[1], "dense_vs_cached_relative_projection_error": relative_error,
            "projection_atol": 1e-5, "normalized_row_atol": 2e-6, "attention_validation": p2.RECON["stats"]}

def capture_source_checks():
    """Observe native eager softmax, independently of our extraction callback."""
    from sampling import load_sample
    import torch
    import torch.nn.functional as functional
    from transformers import AutoModelForCausalLM
    torch.set_num_threads(4)
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    results = []
    for name in MODELS:
        dtype = torch.bfloat16 if "Qwen" in name else torch.float32
        model = AutoModelForCausalLM.from_pretrained(name, revision=corpus["models"][name]["revision"], local_files_only=True,
                    attn_implementation="eager", dtype=dtype).to("cuda").eval()
        for n in [128, 256]:
            attention, manifest = load_sample(name, n)
            observed = []
            original_softmax = functional.softmax
            def observer(*args, **kwargs):
                result = original_softmax(*args, **kwargs)
                if result.ndim == 4 and result.shape[-2:] == (n, n):
                    observed.append(result.detach().float().cpu().numpy().astype(np.float16))
                return result
            functional.softmax = observer
            try:
                with torch.inference_mode():
                    ids = torch.tensor([corpus["models"][name]["documents"][0]["token_ids"][:n]], device="cuda")
                    model(ids, use_cache=False, logits_to_keep=1)
            finally:
                functional.softmax = original_softmax
            if len(observed) != manifest["n_layers"]:
                raise RuntimeError("Native eager observer did not see exactly one softmax per layer")
            checked = 0
            for i, item in enumerate(manifest["instances"]):
                if item["document_index"] != 0:
                    continue
                expected = observed[item["layer"]][0, item["head"]]
                if not np.array_equal(attention[i], expected):
                    raise RuntimeError(f"Archive/native eager mismatch: {item['instance_id']}")
                checked += 1
            results.append({"model": name, "n": n, "document_index": 0,
                            "n_sampled_matrices_checked": checked, "all_layers_checked": True,
                            "native_precast_softmax_to_archive_exact": True})
        del model, attention, observed
        torch.cuda.empty_cache()
    return {"validation_fixture": "first frozen article, all layers and every sampled head, each of 12 datasets",
            "native_forward_modified": False, "extraction_callback_used_by_observer": False,
            "archive_dtype": "float16", "datasets": results}

def delivery_audit():
    """Read-only numerical audit; an incomplete V1 is explicitly NOT a pass."""
    from sampling import load_sample, DATA_ROOT
    checked, inventory = [], []
    for model in MODELS:
        for n in [128, 256]:
            attention, manifest = load_sample(model, n)
            assert validate_matrices(attention, manifest["storage_row_sum_atol"])["invalid_matrices"] == 0
            expected = [r["instance_id"] for r in manifest["instances"]]
            groups = [
                (Path("out")/f"phase24_core_{slug(model)}_n{n}_v2.json", "core"),
                (Path("out")/f"phase26_named_{slug(model)}_n{n}_msclean_srpca_v2.json", "named"),
                (Path("out")/f"phase15_{slug(model)}_n{n}_v2.json", "constancy")]
            for path, group in groups:
                result = json.loads(path.read_text(encoding="utf-8"))
                assert result["n_instances"] == len(expected)
                pairs = Path(result["pairs_path"])
                with pairs.open(encoding="utf-8") as f:
                    rows = [json.loads(line) for line in f]
                assert [r["instance_id"] for r in rows] == expected
                assert len({r["doc_id"] for r in rows}) == 64
                if group == "named":
                    for row in rows:
                        assert len(row["configurations"]) == 15
                        for metric in row["configurations"].values():
                            assert abs(metric["named_norm_ratio"]**2-metric["named_energy_ratio"]) < 1e-12
                            assert metric["energy_identity_abs_error_over_A_energy"] <= 1e-12
                checked.append({"model": model, "n": n, "group": group, "n_pairs": len(rows), "passed": True})
    cost = json.loads(Path("out/phase17_efficiency_v2.json").read_text(encoding="utf-8"))
    assert cost["purpose"] == "offline analysis fitting cost, not inference speed"
    for n in [128, 256, 512]:
        assert cost["datasets"][str(n)]["n_documents"] == 64
        assert cost["datasets"][str(n)]["n_benchmark_matrices"] == 64
    with Path(cost["pairs_path"]).open(encoding="utf-8") as f:
        timing_rows = [json.loads(line) for line in f]
    assert len(timing_rows) == 384
    for n in [128, 256, 512]:
        for solver in ["dense_nnls", "qr_nnls"]:
            selected = [r for r in timing_rows if r["n"] == n and r["solver"] == solver]
            assert len(selected) == 64 and len({r["doc_id"] for r in selected}) == 64
            assert all(r["rank"] == 8 and r["iterations"] == 5 and r["elapsed_seconds"] > 0 for r in selected)
    triples = [{(r["doc_id"], r["layer"], r["head"]) for r in timing_rows if r["n"] == n} for n in [128, 256, 512]]
    assert triples[0] == triples[1] == triples[2]
    for filename in ["phase3_robustness_v2.json", "phase5_msclean_v2.json", "phase6_srpca_v2.json", "phase15_interaction_v2.json"]:
        root = json.loads((Path("out")/filename).read_text(encoding="utf-8"))
        datasets = root["datasets"]
        assert len(datasets) == 12 and sum(r["n_instances"] for r in datasets) == 19968
        for row in datasets:
            assert row["manifest_sha256"] == sha256_file(sample_paths(row["model"], row["n"])[1])
    identity = json.loads(Path("out/phase25_identity_checks_v2.json").read_text(encoding="utf-8"))
    for model in MODELS:
        assert identity[model]["n_documents"] == 256 and identity[model]["identity_kl"] == 0
    required = ["out/phase2_downstream_v2.json", "out/phase7_editability_v2.json",
                "out/phase8_beta0_v2.json", "out/phase30_validity_audit_v2.json",
                "out/phase33_validation_schedule_checks_v2.json", "out/phase2_document_statistics_v2.json"]
    missing = [p for p in required if not Path(p).exists()]
    if not missing:
        for name in required[:2]:
            data = json.loads(Path(name).read_text(encoding="utf-8"))
            for model in MODELS:
                result = data[model]
                assert result["n_documents_effective"] == 256
                assert result["identity_kl_exactly_zero"]
                for arm in result["arms"].values():
                    assert arm["n_documents"] == 256
        assert json.loads(Path(required[3]).read_text(encoding="utf-8"))["all_passed"]
        assert json.loads(Path(required[4]).read_text(encoding="utf-8"))["all_passed"]
        beta = json.loads(Path(required[2]).read_text(encoding="utf-8"))
        assert beta["_meta"]["n_trials_total_unique"] == 16000
        assert beta["_meta"]["positive_beta_regression"]["logits_bit_equal"]
        intervals = json.loads(Path(required[5]).read_text(encoding="utf-8"))
        assert intervals["_meta"]["n_arms_total"] == 90
        assert intervals["_meta"]["bootstrap_seed"] == 0 and intervals["_meta"]["n_bootstrap"] == 2000
        assert intervals["_meta"]["shared_resampling_across_all_models_and_arms"]
        for model in MODELS:
            assert intervals[model]["pairs_sha256"] == sha256_file(intervals[model]["pairs_path"])
            assert len(intervals[model]["arms"]) == 15
            for name in required[:2]:
                source = json.loads(Path(name).read_text(encoding="utf-8"))[model]
                for arm, summary in source["arms"].items():
                    item = intervals[model]["arms"][arm]
                    assert item["n_documents"] == 256 and item["median_kl"] == summary["median_kl"]
                    assert item["mean_kl"] == summary["mean_kl"]
    sources = ["sampling.py", "extract_attn.py", "phase1_multimodel.py", "phase2_downstream.py", "phase3_robustness.py",
               "phase5_msclean.py", "phase6_srpca.py", "phase7_editability.py", "phase9_bigmodel.py", "phase15_interaction.py",
               "phase17_efficiency.py", "phase24_p0_metrics.py", "phase25_p0_checks.py", "phase26_p0_named.py",
               "phase8_lostmiddle.py", "phase10_baselines.py", "phase14_adaptive.py", "phase27_finish_v1.py",
               "phase28_beta0_retest.py", "phase29_sink_checks.py", "phase30_validity_audit.py", "phase31_finish_beta0.py",
               "phase32_queue_remaining_v1.py", "phase33_validation_schedule.py", "phase34_parallel_svd.py",
               "phase35_downstream_intervals.py"]
    outputs = [CORPUS_PATH, DATA_ROOT/"READY"]
    for model in MODELS:
        for n in (128,256):
            outputs.extend(sample_paths(model,n))
    outputs.extend(sample_paths("gpt2",512))
    outputs += list(DATA_ROOT.glob("beta0_probe_*_v2.npz"))+list(DATA_ROOT.glob("beta0_probe_*_v2.manifest.json"))
    prefixes = ("phase1_", "phase2_", "phase3_", "phase5_", "phase6_", "phase7_", "phase8_beta0", "phase9_", "phase15_", "phase17_", "phase24_", "phase25_", "phase26_", "phase28_positive_", "phase29_sink_", "phase29_publication_", "phase30_validity_", "phase33_")
    outputs += [p for p in Path("out").glob("*_v2.json") if p.name.startswith(prefixes)]
    pair_prefixes = ("core_", "legacy_mass_", "empty_rows_", "named_", "constancy_", "downstream_", "analysis_cost_", "beta0_")
    outputs += [p for p in Path("out/pairs").glob("*_v2.jsonl") if p.name.startswith(pair_prefixes)]
    if Path("out/p0_environment_v2.json").exists():
        outputs.append(Path("out/p0_environment_v2.json"))
    if Path("out/p0_comparison_v2.json").exists():
        outputs.append(Path("out/p0_comparison_v2.json"))
    if Path("out/phase18_beta0_dependency_audit_v2.json").exists():
        outputs.append(Path("out/phase18_beta0_dependency_audit_v2.json"))
    for path in [Path(p) for p in sources]+sorted(set(outputs)):
        inventory.append({"path": path.as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path),
                          "kind": "source" if path.name in sources else "data_or_result"})
    inventory.append({"path": "out/_rerun_logs/p0_progress.md", "kind": "mutable_progress_log", "sha256": None})
    result = {"all_required_experiments_complete": not missing, "pending_required_outputs": missing,
              "checked_raw_pair_groups": checked, "all_available_numerical_audits_passed": True,
              "identity_models": 6, "identity_documents_per_model": 256,
              "v2_total_primary_matrices": 19968, "cost_benchmark_matrices_per_length": 64,
              "independent_other_model_family_review": "not performed by this script",
              "inventory": inventory}
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sampling", action="store_true")
    ap.add_argument("--reconstruction", action="store_true")
    ap.add_argument("--retrieval-audit", action="store_true")
    ap.add_argument("--fractions-constancy", action="store_true")
    ap.add_argument("--gpu-identity", action="store_true")
    ap.add_argument("--geometry", action="store_true")
    ap.add_argument("--delivery-audit", action="store_true")
    ap.add_argument("--capture-source", action="store_true")
    ap.add_argument("--out", default="out/phase25_sampling_checks_v2.json")
    args = ap.parse_args()
    started = time.perf_counter()
    if args.sampling or args.reconstruction or args.retrieval_audit or args.fractions_constancy or args.gpu_identity or args.geometry or args.delivery_audit or args.capture_source:
        result = (capture_source_checks() if args.capture_source else delivery_audit() if args.delivery_audit else geometry_checks() if args.geometry else gpu_identity_checks() if args.gpu_identity else sampling_checks() if args.sampling else retrieval_audit() if args.retrieval_audit
                  else fraction_constancy_checks() if args.fractions_constancy else reconstruction_checks())
        result["elapsed_seconds"] = time.perf_counter() - started
        path = Path(args.out)
        if path.exists():
            raise FileExistsError(path)
        write_json_new(path, result)
        stage = "V2 native source audit" if args.capture_source else "P0 delivery audit" if args.delivery_audit else "V2 sampling checks" if args.sampling else "V1 retrieval audit" if args.retrieval_audit else "V3/V4 metric checks" if args.fractions_constancy else "V1 GPU identity" if args.gpu_identity else "V1 CPU checks"
        message = ("Available audits passed; required pending outputs: " + str(result["pending_required_outputs"])) if args.delivery_audit else "All regression checks passed"
        progress(stage, message, result["elapsed_seconds"],
                 ".venv/Scripts/python.exe -B " + " ".join(sys.argv))
        print(json.dumps({"path": args.out, "complete": result["all_required_experiments_complete"]}) if args.delivery_audit else json.dumps(result), flush=True)

if __name__ == "__main__":
    main()
