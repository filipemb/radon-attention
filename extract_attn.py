"""P0 V2 extraction. Run GPU commands under the shared flock; never repair NaNs."""
from sampling import (MODELS, DATA_ROOT, CORPUS_PATH, prepare_corpus, make_manifest,
                      sample_paths, validate_matrices, sha256_file, write_json_new, progress)
import argparse
import gc
import json
import sys
import time
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AttentionInterface

torch.set_num_threads(4)
torch.set_num_interop_threads(4)

CAPTURE = {"layer": 0, "batch_start": 0, "selected": {}, "output": None, "checks": []}

def repeat_kv(x, n):
    if n == 1:
        return x
    b, h, s, d = x.shape
    return x[:, :, None, :, :].expand(b, h, n, s, d).reshape(b, h * n, s, d)

def capture_attention(module, query, key, value, attention_mask, scaling=None, dropout=0.0, **kwargs):
    if module.training or dropout:
        raise RuntimeError("Extraction requires eval mode without dropout")
    nrep = getattr(module, "num_key_value_groups", 1)
    key, value = repeat_kv(key, nrep), repeat_kv(value, nrep)
    scores = query @ key.transpose(-1, -2) * (scaling if scaling is not None else query.size(-1) ** -0.5)
    if attention_mask is not None:
        scores = scores + attention_mask
    # Transformers does not automatically build a causal mask for a custom
    # AttentionInterface name. Inputs here have no padding; enforce causality.
    q, k = scores.shape[-2:]
    causal = torch.ones(q, k, device=scores.device, dtype=torch.bool).tril(k - q)
    scores = scores.masked_fill(~causal, float("-inf"))
    probs = F.softmax(scores, dim=-1, dtype=torch.float32)
    layer = CAPTURE["layer"]
    for bi in range(query.shape[0]):
        di = CAPTURE["batch_start"] + bi
        for oi, head in CAPTURE["selected"][di, layer]:
            a = probs[bi, head].detach().cpu().numpy()
            check = validate_matrices(a[None], 2e-6)
            CAPTURE["checks"].append(check)
            CAPTURE["output"][oi] = a.astype(np.float16)
    CAPTURE["layer"] += 1
    cast = probs.to(value.dtype)
    out = (cast @ value).transpose(1, 2)
    if module.config.model_type != "gpt2":
        out = out.contiguous()
    return out, cast

def set_attention(model, name):
    model.set_attn_implementation(name)

@torch.inference_mode()
def extract_one(model_name, n, batch=1, n_documents=64):
    start = time.perf_counter()
    corpus = prepare_corpus()
    path, mpath = sample_paths(model_name, n)
    if path.exists() or mpath.exists():
        if not (path.exists() and mpath.exists()):
            raise RuntimeError(f"Incomplete previous extraction: {path}")
        return verify_one(model_name, n)
    manifest = make_manifest(corpus, model_name, n, n_documents)
    cfg = corpus["models"][model_name]
    ids = torch.tensor([x["token_ids"][:n] for x in cfg["documents"][:n_documents]], dtype=torch.long)
    targets = np.array([x["token_ids"][n] for x in cfg["documents"][:n_documents]], dtype=np.int64)
    dtype = torch.bfloat16 if "Qwen" in model_name else torch.float32
    model = AutoModelForCausalLM.from_pretrained(model_name, revision=cfg["revision"], local_files_only=True,
                                                attn_implementation="eager", dtype=dtype).to("cuda").eval()
    sample = np.empty((manifest["n_matrices"], n, n), dtype=np.float16)
    selection = {(di, layer): [] for di in range(n_documents) for layer in range(manifest["n_layers"])}
    for i, item in enumerate(manifest["instances"]):
        selection[item["document_index"], item["layer"]].append((i, item["head"]))
    ref = model(ids[:batch].to("cuda"), use_cache=False, logits_to_keep=1).logits[:, -1].float().cpu()
    CAPTURE.update({"selected": selection, "output": sample, "checks": []})
    AttentionInterface.register("p0_capture", capture_attention)
    set_attention(model, "p0_capture")
    actual = 0
    for s in range(0, n_documents, batch):
        CAPTURE["layer"], CAPTURE["batch_start"] = 0, s
        out = model(ids[s:s + batch].to("cuda"), use_cache=False, logits_to_keep=1)
        if CAPTURE["layer"] != manifest["n_layers"]:
            raise RuntimeError(f"Attention calls {CAPTURE['layer']} != layers {manifest['n_layers']}")
        if s == 0:
            got = out.logits[:, -1].float().cpu()
            if not torch.equal(ref, got):
                raise RuntimeError(f"Capture changed vanilla eager logits, max error {(ref-got).abs().max().item()}")
        actual += ids[s:s + batch].shape[0]
        if actual % 16 == 0:
            print(f"{model_name} n={n}: {actual}/{n_documents} documents", flush=True)
    source_checks = CAPTURE["checks"]
    source_invalid = sum(c["invalid_matrices"] for c in source_checks)
    checks = validate_matrices(sample, manifest["storage_row_sum_atol"])
    manifest.update({"n_sequences_processed": actual, "n_documents_effective": actual,
                     "n_model_forward_sequences_including_identity": actual + len(ids[:batch]),
                     "model_dtype": str(dtype), "identity_capture_logits_exact": True,
                     "source_validation": {"invalid_matrices": source_invalid,
                                           "nan_values": sum(c["nan_values"] for c in source_checks),
                                           "inf_values": sum(c["inf_values"] for c in source_checks),
                                           "max_row_sum_abs_error": max(c["max_row_sum_abs_error"] for c in source_checks)},
                     "archive_validation": checks, "status": "verified" if source_invalid == 0 and checks["invalid_matrices"] == 0 else "invalid"})
    if source_invalid or checks["invalid_matrices"]:
        write_json_new(mpath, manifest)
        raise RuntimeError(f"Invalid extraction; counts preserved in {mpath}")
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".partial.npz")
    np.savez_compressed(temp, attention=sample, input_ids=ids.numpy(), next_token_ids=targets,
                        document_index=np.array([x["document_index"] for x in manifest["instances"]], dtype=np.int32),
                        layer=np.array([x["layer"] for x in manifest["instances"]], dtype=np.int16),
                        head=np.array([x["head"] for x in manifest["instances"]], dtype=np.int16))
    temp.rename(path)
    manifest.update({"npz_sha256": sha256_file(path), "npz_bytes": path.stat().st_size,
                     "elapsed_seconds": time.perf_counter() - start})
    write_json_new(mpath, manifest)
    del model, sample, ref, out
    CAPTURE["output"] = None
    gc.collect()
    torch.cuda.empty_cache()
    result = verify_one(model_name, n)
    progress("V2 extraction", f"{model_name}, n={n}, {actual} documents, {manifest['n_matrices']} matrices; all checks passed",
             manifest["elapsed_seconds"], "flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B " + " ".join(sys.argv))
    return result

def verify_one(model_name, n):
    path, mpath = sample_paths(model_name, n)
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
    print(f"VERIFIED {path}: {expected}, docs={manifest['n_documents_effective']}, row_error={check['max_row_sum_abs_error']:.3g}", flush=True)
    return {"model": model_name, "n": n, "n_documents": manifest["n_documents_effective"],
            "n_matrices": manifest["n_matrices"], "bytes": path.stat().st_size,
            "max_row_sum_abs_error": check["max_row_sum_abs_error"]}

def ready():
    rows = [verify_one(m, n) for m in MODELS for n in (128, 256)]
    path = DATA_ROOT / "READY"
    if path.exists():
        return
    summary = {"status": "verified", "corpus_manifest_sha256": sha256_file(CORPUS_PATH),
               "datasets": rows, "total_npz_bytes": sum(r["bytes"] for r in rows),
               "total_matrices": sum(r["n_matrices"] for r in rows),
               "all_nan_inf_negative_and_upper_triangle_counts": 0,
               "row_sum_policy": "Fixed IEEE fp16 rounding bound recorded per manifest; no renormalization or NaN replacement"}
    write_json_new(path, summary)
    progress("V2 READY", f"All 12 archives verified; {summary['total_matrices']} matrices, {summary['total_npz_bytes']} bytes")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--lengths", nargs="+", type=int, default=[128, 256])
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--ready", action="store_true")
    args = ap.parse_args()
    for name in args.models:
        for n in args.lengths:
            verify_one(name, n) if args.verify_only else extract_one(name, n, args.batch)
    if args.ready:
        ready()

if __name__ == "__main__":
    main()
