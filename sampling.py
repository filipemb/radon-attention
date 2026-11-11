"""P0: immutable corpus manifests and balanced document/layer/head sampling.

The sampling unit is a complete WikiText article, recovered from the cached raw
dataset (the old text export discarded article boundaries). No GPU is used here.
"""
import os
for _key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "4"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import datasets  # Must precede torch, including indirect transformers imports.
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import time
import tempfile
from datetime import datetime, timezone
import numpy as np

MODELS = ["gpt2", "gpt2-medium", "EleutherAI/pythia-410m",
          "EleutherAI/pythia-1.4b", "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-3B"]
DATA_ROOT = Path("data/attn")
CORPUS_PATH = DATA_ROOT / "corpus_v2.manifest.json"
PROGRESS_PATH = Path("out/_rerun_logs/p0_progress.md")
SOURCE_ROW_ATOL = 2e-6
# IEEE half rounding: relative error <= eps/2, plus n subnormal roundings.
# This bound is fixed before extraction; extraction captures fp32 softmax before
# the model's value-dtype cast, while its actual forward remains unchanged.
def storage_row_atol(n):
    return float(np.finfo(np.float16).eps / 2 + n * np.nextafter(np.float16(0), np.float16(1)).item() / 2 + SOURCE_ROW_ATOL)

def slug(model):
    return model.replace("/", "__")

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def write_json_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # A completed aggregate's existence is also an inter-agent readiness signal.
    # Publish the complete file by an exclusive hard link, on the same volume:
    # no partially written JSON becomes visible and an existing file is never
    # replaced. All temporary work remains inside the requested repo directory.
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix="."+path.name+".", suffix=".tmp")
    temporary = Path(temporary)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.link(temporary, path)  # FileExistsError preserves prior outputs.
    finally:
        temporary.unlink(missing_ok=True)

def progress(stage, message, seconds=None, command=None):
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with PROGRESS_PATH.open("a", encoding="utf-8") as f:
        f.write(f"\n- {stamp} | {stage}: {message}")
        if seconds is not None:
            f.write(f" | elapsed_seconds={seconds:.3f}")
        if command:
            f.write(f" | command: `{command}`")
        f.write("\n")

def read_articles():
    roots = sorted((Path.home() / ".cache/huggingface/datasets/Salesforce___wikitext/wikitext-2-raw-v1").glob("**/wikitext-train.arrow"))
    if len(roots) != 1:
        raise RuntimeError(f"Expected exactly one cached raw training split, found {roots}")
    source = roots[0]
    ds = datasets.Dataset.from_file(str(source))
    docs, chunks, title, start = [], [], None, None
    def finish(end):
        if title is not None:
            text = "\n".join(chunks)
            docs.append({"doc_id": f"wikitext-train-article-{start}", "title": title,
                         "source_row_start": start, "source_row_end_exclusive": end,
                         "text": text, "text_sha256": hashlib.sha256(text.encode()).hexdigest()})
    for i, text in enumerate(ds["text"]):
        stripped = text.strip()
        if re.fullmatch(r"= [^=].*? =", stripped):
            finish(i)
            title, start, chunks = stripped[2:-2].strip(), i, [stripped]
        elif title is not None and stripped:
            chunks.append(stripped)
    finish(len(ds))
    if len(docs) < 256:
        raise RuntimeError(f"Article parsing produced only {len(docs)} articles")
    return docs, {"dataset": "Salesforce/wikitext", "config": "wikitext-2-raw-v1", "split": "train",
                  "arrow_path": str(source), "arrow_sha256": sha256_file(source), "n_source_articles": len(docs)}

def prepare_corpus(seed=0, n_documents=256, window_tokens=513):
    if CORPUS_PATH.exists():
        result = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
        if (result["seed"], result["n_documents"], result["window_tokens"]) != (seed, n_documents, window_tokens):
            raise RuntimeError("Existing immutable corpus manifest has different settings")
        return result
    from transformers import AutoTokenizer, AutoConfig
    start = time.perf_counter()
    docs, source = read_articles()
    tokenizers = {m: AutoTokenizer.from_pretrained(m, local_files_only=True) for m in MODELS}
    eligible = []
    for i, doc in enumerate(docs):
        lengths = [len(tok(doc["text"], add_special_tokens=False, truncation=True,
                           max_length=window_tokens, verbose=False)["input_ids"]) for tok in tokenizers.values()]
        if min(lengths) >= window_tokens:
            eligible.append(i)
    if len(eligible) < n_documents:
        raise RuntimeError(f"Only {len(eligible)} common eligible articles for {n_documents} requested")
    indices = np.random.default_rng(seed).choice(eligible, size=n_documents, replace=False)
    selected = [{k: v for k, v in docs[int(i)].items() if k != "text"} for i in indices]
    model_windows = {}
    for mi, (name, tok) in enumerate(tokenizers.items()):
        rng = np.random.default_rng(np.random.SeedSequence([seed, mi, 103]))
        windows = []
        for index in indices:
            ids = tok(docs[int(index)]["text"], add_special_tokens=False, verbose=False)["input_ids"]
            offset = int(rng.integers(0, len(ids) - window_tokens + 1))
            windows.append({"offset": offset, "n_document_tokens": len(ids),
                            "token_ids": ids[offset:offset + window_tokens]})
        config = AutoConfig.from_pretrained(name, local_files_only=True)
        model_windows[name] = {"revision": config._commit_hash, "tokenizer_class": type(tok).__name__,
                               "n_layers": config.num_hidden_layers, "n_heads": config.num_attention_heads,
                               "documents": windows}
    result = {"schema_version": 2, "seed": seed, "n_documents": n_documents,
              "window_tokens": window_tokens, "source": source,
              "eligibility": f"At least {window_tokens} tokens under every one of the six tokenizers",
              "n_common_eligible_articles": len(eligible), "sampling": "uniform without replacement among common eligible articles",
              "documents": selected, "models": model_windows,
              "matrix_document_selection": "first 64 entries of this pre-shuffled manifest",
              "downstream_document_selection": "all 256 entries, prefix length 128 and following held-out token",
              "old_text_export_sha256": sha256_file("wikitext2_train.txt")}
    write_json_new(CORPUS_PATH, result)
    progress("V2 corpus", f"Frozen {n_documents} articles of {len(eligible)} common eligible; sha256={sha256_file(CORPUS_PATH)}",
             time.perf_counter() - start, "OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B sampling.py prepare")
    return result

def make_manifest(corpus, model, n, n_documents=64, min_matrices=1024):
    cfg = corpus["models"][model]
    layers, heads = cfg["n_layers"], cfg["n_heads"]
    per_doc_layer = math.ceil(min_matrices / (n_documents * layers))
    if per_doc_layer > heads or n + 1 > corpus["window_tokens"]:
        raise ValueError("Requested sample exceeds head or token universe")
    rng = np.random.default_rng(np.random.SeedSequence([corpus["seed"], layers, heads, 211]))
    selected_heads = {}
    for layer in range(layers):
        head_perm, doc_perm = rng.permutation(heads), rng.permutation(n_documents)
        for ordinal, doc in enumerate(doc_perm):
            selected_heads[int(doc), layer] = sorted(int(head_perm[(ordinal * per_doc_layer + j) % heads]) for j in range(per_doc_layer))
    instances = []
    for di, doc in enumerate(corpus["documents"][:n_documents]):
        for layer in range(layers):
            for head in selected_heads[di, layer]:
                instances.append({"instance_id": f"{slug(model)}_n{n}_{doc['doc_id']}_l{layer}_h{head}",
                                  "document_index": di, "doc_id": doc["doc_id"], "layer": layer, "head": head,
                                  "offset": cfg["documents"][di]["offset"], "n": n})
    return {"schema_version": 2, "model": model, "model_slug": slug(model), "revision": cfg["revision"], "n": n,
            "seed": corpus["seed"], "corpus_manifest_sha256": sha256_file(CORPUS_PATH),
            "n_documents_requested": n_documents, "n_matrices": len(instances), "n_layers": layers, "n_heads": heads,
            "design": "every document x every layer; balanced randomized distinct heads within each layer",
            "heads_per_document_layer": per_doc_layer, "matrices_per_layer": n_documents * per_doc_layer,
            "head_count_range_per_layer": [n_documents * per_doc_layer // heads, math.ceil(n_documents * per_doc_layer / heads)],
            "inclusion_probability_per_document_layer_head": per_doc_layer / heads,
            "source_row_sum_atol": SOURCE_ROW_ATOL, "storage_row_sum_atol": storage_row_atol(n),
            "precision": "fp32 softmax before value-dtype cast; fp16 archive; model forward uses original value dtype",
            "documents": corpus["documents"][:n_documents], "instances": instances}

def sample_paths(model, n):
    base = DATA_ROOT / f"{slug(model)}_n{n}"
    # Model names contain decimal points (1.4b, Qwen2.5): append, do not replace
    # their suffix, otherwise different sequence lengths collide.
    return Path(str(base) + ".npz"), Path(str(base) + ".manifest.json")

def validate_matrices(attention, atol):
    if attention.ndim != 3 or attention.shape[-1] != attention.shape[-2]:
        raise ValueError(f"Invalid matrix shape {attention.shape}")
    bad = {"nan_values": int(np.isnan(attention).sum()), "inf_values": int(np.isinf(attention).sum()),
           "negative_values": int((attention < 0).sum()), "above_diagonal_nonzero": 0,
           "invalid_rows": 0, "invalid_matrices": 0, "max_row_sum_abs_error": 0.0}
    for a in attention:
        upper = int(np.count_nonzero(np.triu(a, 1)))
        sums = a.astype(np.float64).sum(-1)
        errors = np.abs(sums - 1)
        row_bad = (~np.isfinite(sums)) | (errors > atol)
        bad["above_diagonal_nonzero"] += upper
        bad["invalid_rows"] += int(row_bad.sum())
        bad["invalid_matrices"] += int(upper > 0 or row_bad.any() or not np.isfinite(a).all() or (a < 0).any())
        if np.isfinite(errors).all():
            bad["max_row_sum_abs_error"] = max(bad["max_row_sum_abs_error"], float(errors.max()))
    return bad

def load_sample(model, n, root=DATA_ROOT):
    base = Path(root) / f"{slug(model)}_n{n}"
    manifest = json.loads(Path(str(base) + ".manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "verified":
        raise RuntimeError(f"Unverified sample {base}")
    archive = Path(str(base) + ".npz")
    if sha256_file(archive) != manifest["npz_sha256"]:
        raise RuntimeError(f"Archive hash differs from verified manifest: {archive}")
    with np.load(archive, allow_pickle=False) as z:
        a = z["attention"]
    if a.shape != (manifest["n_matrices"], n, n) or a.dtype != np.float16:
        raise RuntimeError(f"Archive does not match manifest: {base}")
    return a, manifest

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["prepare"])
    args = ap.parse_args()
    prepare_corpus()

if __name__ == "__main__":
    main()
