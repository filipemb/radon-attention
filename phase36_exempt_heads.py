"""Phase36: isencao de cabecas diagonais (identidade) sem reconstruir.

Importa o harness corrigido de phase2_downstream SEM alterar a logica de
causalidade: reutiliza causal_support, factor_svd, normalize_reconstruction
(mascara, clamp, renormalizacao), validate_attention, last_logits (avaliacao
so no ultimo token com crop fisico), kl_nll, DeferredStats, mesma politica de
linha vazia uniforme, mesmos 256 artigos do V1, mesmo prefixo 128.

Unica mudanca: cabecas da lista do passo 1 (mediana da massa diagonal media
> 0.9 em data/attn/{slug}_n128.npz) recebem reconstrucao identidade (atencao
verdadeira) em vez da SVD/geom; as demais sao reconstruidas exatamente como
antes (SVD/geom full-batch via p2.reconstruct, depois overwrite das isentas).
Com lista vazia delega integralmente a p2.reconstruct (bit-identico ao v2).
"""
from sampling import CORPUS_PATH, prepare_corpus, sha256_file, write_json_new, progress, slug
import argparse
import gc
import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AttentionInterface

import phase2_downstream as p2

torch.set_num_threads(4)

# Lista do passo 1 (criterio > 0.9 declarado antes de rodar j2_diag_pass1.py).
# Mediana sobre matrizes amostradas de mean_i A[i,i]; n_matrizes entre parenteses:
#  Qwen2.5-0.5B: (0,1) 0.985753 n=5; (8,3) 0.995975 n=4; (23,1) 0.995144 n=5
#  Qwen2.5-3B:   (0,12) 0.997271 n=4; (27,8) 0.999998 n=4
#  Demais modelos: nenhuma cabeca > 0.9 (maximos: gpt2 0.8676, gpt2-medium
#  0.4702, py410m 0.8400, py1.4b 0.6685). Qwen2.5-7B (fora do downstream):
#  (18,7) 0.999958 n=3; (19,0) 0.999928 n=3. missing=0 em todos.
CRITERION = "median(mean_i A[i,i] over sampled matrices) > 0.9"
THRESHOLD = 0.9
EXEMPT_BY_MODEL = {
    "gpt2": [],
    "gpt2-medium": [],
    "EleutherAI/pythia-410m": [],
    "EleutherAI/pythia-1.4b": [],
    "Qwen/Qwen2.5-0.5B": [[0, 1], [8, 3], [23, 1]],
    "Qwen/Qwen2.5-3B": [[0, 12], [27, 8]],
}

EXEMPT = set()


def p36_reconstruct(weights, module):
    mode = p2.RECON["mode"]
    if mode == "identity":
        return p2.reconstruct(weights)
    layer = getattr(module, "layer_idx", None)
    if layer is None:
        layer = getattr(module, "layer_index", None)
    if layer is None:
        raise RuntimeError("Cannot determine layer index for exemption")
    layer = int(layer)
    exempt_h = [h for (ll, h) in EXEMPT if ll == layer]
    if not exempt_h:
        return p2.reconstruct(weights)
    rec = p2.reconstruct(weights)
    rec[:, exempt_h] = weights[:, exempt_h]
    tmp = p2.DeferredStats() if isinstance(p2.RECON["stats"], p2.DeferredStats) else {}
    p2.validate_attention(rec, tmp)
    if isinstance(tmp, p2.DeferredStats):
        tmp.finalize(context=f"phase36 exempt final validation layer {layer}")
    return rec


def p36_attention_forward(module, query, key, value, attention_mask, scaling=None, dropout=0.0, reconstruct_fn=None, **kwargs):
    if module.training or dropout:
        raise RuntimeError("Evaluation requires eval mode and zero dropout")
    nrep = getattr(module, "num_key_value_groups", 1)
    key, value = p2._repeat_kv(key, nrep), p2._repeat_kv(value, nrep)
    scores = query @ key.transpose(-1, -2) * (scaling if scaling is not None else query.size(-1) ** -0.5)
    q, k = scores.shape[-2:]
    scores = scores.masked_fill(~p2.causal_support(q, k, scores.device), float("-inf"))
    aw = F.softmax(scores, dim=-1, dtype=torch.float32).to(value.dtype)
    aw = p36_reconstruct(aw, module)
    out = (aw @ value).transpose(1, 2)
    if module.config.model_type != "gpt2":
        out = out.contiguous()
    return out, aw


def arm_label(mode, rank):
    return f"phase2:{mode}" + (f":{rank}" if rank is not None else "")


def activate_exempt(mode, rank, deferred=True):
    p2.RECON.update({"mode": mode, "k": rank,
                     "stats": p2.DeferredStats() if deferred else {}})
    return p2.RECON["stats"]


def run_one_model(name, exempt_list, arms, batch=2, pairs_tag="exempt"):
    global EXEMPT
    EXEMPT = set((int(a), int(b)) for (a, b) in exempt_list)
    started = time.perf_counter()
    corpus = prepare_corpus()
    corpus_hash = sha256_file(CORPUS_PATH)
    n = 128
    windows = torch.tensor([r["token_ids"] for r in corpus["models"][name]["documents"]], dtype=torch.long)
    assert len(windows) == 256
    dtype = torch.bfloat16 if "Qwen" in name else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        name, revision=corpus["models"][name]["revision"], local_files_only=True,
        dtype=dtype, attn_implementation="eager").to("cuda").eval()
    torch.manual_seed(0)
    p2.RECON.update(empty_row_policy="uniform", parallel_svd=False, svd_driver=None)
    p2.RECON["D"] = p2.build_dictionary(n, "cuda")
    q, r = torch.linalg.qr(p2.RECON["D"], mode="reduced")
    p2.RECON["D_pinv"] = torch.linalg.solve_triangular(r, q.T, upper=True)
    AttentionInterface.register("p36_exempt", p36_attention_forward)
    pairpath = Path("out/pairs") / f"phase36_{slug(name)}_{pairs_tag}.jsonl"
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if pairpath.exists():
        with pairpath.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        if any(r["corpus_manifest_sha256"] != corpus_hash for r in rows):
            raise RuntimeError("Partial phase36 records belong to another corpus")
        if any(r.get("exempt_heads") != [[int(a), int(b)] for (a, b) in exempt_list] for r in rows):
            raise RuntimeError("Partial phase36 records use another exempt list")
    seen = {(r["arm"], r["doc_id"]) for r in rows}
    if len(seen) != len(rows):
        raise RuntimeError("Duplicate phase36 raw records")
    specs = arms  # list of (mode, rank)
    with pairpath.open("a", encoding="utf-8") as out:
        for start in range(0, len(windows), batch):
            sequences = windows[start:start + batch]
            targets = sequences[:, n]
            model.set_attn_implementation("eager")
            ref = p2.last_logits(model, sequences, n)
            _, ref_nll = p2.kl_nll(ref, ref, targets)
            ref_predictions = ref.argmax(-1)
            device_targets = targets.to(ref.device)
            for (mode, rank) in specs:
                label = arm_label(mode, rank)
                ids = [corpus["documents"][i]["doc_id"] for i in range(start, min(start + batch, len(windows)))]
                if all((label, di) in seen for di in ids):
                    continue
                stats = activate_exempt(mode, rank, deferred=True)
                # Switch implementation AFTER computing ref, BEFORE injected forward.
                model.set_attn_implementation("p36_exempt")
                if start == 0:
                    print(f"ARM start={start}: {label} exempt={sorted(EXEMPT)}", flush=True)
                other = p2.last_logits(model, sequences, n)
                stats.finalize(context=f"{name} {label} documents {start}:{start+len(sequences)}")
                divergence, nll = p2.kl_nll(ref, other, targets)
                predictions = other.argmax(-1)
                flags = torch.stack((predictions == ref_predictions, predictions == device_targets), dim=-1).cpu().tolist()
                for bi, di in enumerate(ids):
                    if (label, di) in seen:
                        continue
                    row = {"model": name, "arm": label, "mode": mode, "rank": rank,
                           "doc_id": di, "document_index": start + bi,
                           "offset": corpus["models"][name]["documents"][start + bi]["offset"],
                           "prefix_length": n, "target_id": int(targets[bi]),
                           "kl": float(divergence[bi]), "nll": float(nll[bi]),
                           "reference_nll": float(ref_nll[bi]),
                           "argmax_agrees": flags[bi][0], "correct": flags[bi][1],
                           "empty_row_policy": "uniform",
                           "exempt_heads": [[int(a), int(b)] for (a, b) in sorted(EXEMPT)],
                           "criterion": CRITERION, "threshold": THRESHOLD,
                           "evaluation_batch_start": start, "evaluation_batch_size": len(sequences),
                           "attention_validation_batch": dict(stats),
                           "corpus_manifest_sha256": corpus_hash}
                    # NB: nll acima e o NLL do braco injetado; reference_nll e do eager.
                    out.write(json.dumps(row, allow_nan=False) + "\n")
                    rows.append(row)
                    seen.add((label, di))
            out.flush()
            if (start + len(sequences)) % 16 == 0:
                print(f"PHASE36 {name}: {start+len(sequences)}/{len(windows)} docs, elapsed={time.perf_counter()-started:.1f}s", flush=True)
    # Aggregate per arm with shared seed-0 document bootstrap for MEDIAN (phase35 method).
    draws = np.random.default_rng(0).integers(0, 256, size=(2000, 256))
    documents = [d["doc_id"] for d in corpus["documents"]]
    arms_out = {}
    for (mode, rank) in specs:
        label = arm_label(mode, rank)
        recs = sorted((r for r in rows if r["arm"] == label), key=lambda r: r["document_index"])
        if len(recs) != 256:
            raise RuntimeError(f"Incomplete arm {label}: {len(recs)} != 256")
        if [r["doc_id"] for r in recs] != documents:
            raise RuntimeError(f"Document order mismatch for {label}")
        kl = np.asarray([r["kl"] for r in recs], dtype=np.float64)
        nll = np.asarray([r["nll"] for r in recs], dtype=np.float64)
        if not (np.isfinite(kl).all() and np.isfinite(nll).all()):
            raise RuntimeError(f"Nonfinite KL/NLL in {label}")
        med_boots = np.median(kl[draws], axis=1)
        mean_boots = np.mean(kl[draws], axis=1)
        arms_out[label] = {
            "n_documents": 256, "n_evaluated_next_tokens": 256,
            "mean_kl": float(np.mean(kl)), "median_kl": float(np.median(kl)),
            "median_kl_ci95_document_bootstrap": np.quantile(med_boots, [0.025, 0.975], method="linear").tolist(),
            "mean_kl_ci95_document_bootstrap": np.quantile(mean_boots, [0.025, 0.975], method="linear").tolist(),
            "mean_nll": float(np.mean(nll)),
            "last_token_perplexity": float(np.exp(np.mean(nll))),
            "argmax_agreement_with_reference": float(np.mean([r["argmax_agrees"] for r in recs])),
            "next_token_accuracy": float(np.mean([r["correct"] for r in recs])),
            "bootstrap_seed": 0, "n_bootstrap": 2000,
        }
    result = {"model": name, "criterion": CRITERION, "threshold": THRESHOLD,
              "exempt_heads": [[int(a), int(b)] for (a, b) in sorted(EXEMPT)],
              "prefix_length": n, "n_documents": 256, "batch": batch,
              "dtype": str(dtype), "corpus_manifest_sha256": corpus_hash,
              "pairs_path": pairpath.as_posix(), "arms": arms_out,
              "elapsed_seconds": time.perf_counter() - started}
    del model
    gc.collect()
    torch.cuda.empty_cache()
    return result, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=list(EXEMPT_BY_MODEL.keys()))
    ap.add_argument("--ranks", nargs="+", type=int, default=[1, 2, 4, 8, 16, 32])
    ap.add_argument("--geom", action="store_true", default=True)
    ap.add_argument("--no-geom", dest="geom", action="store_false")
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--empty-exempt", action="store_true",
                    help="Sanity: ignore step-1 list and use empty exempt list")
    ap.add_argument("--output", default="out/phase36_exempt_heads.json")
    args = ap.parse_args()
    arms = [("svd", k) for k in args.ranks]
    if args.geom:
        arms.append(("geom", None))
    all_results = {}
    pairs_tag = "empty_sanity" if args.empty_exempt else "exempt"
    for name in args.models:
        if name not in EXEMPT_BY_MODEL:
            raise ValueError(f"Unknown model {name}")
        exempt = [] if args.empty_exempt else EXEMPT_BY_MODEL[name]
        result, _ = run_one_model(name, exempt, arms, batch=args.batch, pairs_tag=pairs_tag)
        all_results[name] = result
        progress("Phase36 exempt" if not args.empty_exempt else "Phase36 empty sanity",
                 f"{name}; exempt={exempt}; arms={[arm_label(m, r) for m, r in arms]}",
                 result["elapsed_seconds"],
                 f"flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase36_exempt_heads.py --models {name}")
    if not args.empty_exempt:
        out = {"_meta": {"criterion": CRITERION, "threshold": THRESHOLD,
                         "prefix_length": 128, "n_documents_per_model": 256,
                         "last_token_only": True, "empty_row_policy": "uniform",
                         "exempt_lists": EXEMPT_BY_MODEL},
               **all_results}
        op = Path(args.output)
        if op.exists():
            # Our own phase36 aggregate: merge incrementally (pre-existing v2 JSONs untouched).
            prev = json.loads(op.read_text(encoding="utf-8"))
            merged_meta = out["_meta"]
            merged = {"_meta": merged_meta}
            for k, v in prev.items():
                if not k.startswith("_"):
                    merged[k] = v
            merged.update(all_results)
            tmp = op.with_suffix(".tmp")
            tmp.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
            tmp.replace(op)
            print(f"updated {op} with {list(all_results.keys())}", flush=True)
        else:
            write_json_new(op, out)
    else:
        print(json.dumps({k: v["arms"] for k, v in all_results.items()}, indent=2)[:2000], flush=True)


if __name__ == "__main__":
    main()
