"""Full Qwen3B identity reference in the same two-copy batch as edited arms."""
from revision_v3_stats import write_json_new, sha256_file
from revision_v3_probes import load_probe
from phase53_massmatched_retrieval import (historical, selected_indices, item_keys,
    paired_forward, attention_forward, log, hashes, PROTOCOL)
import argparse
import gc
import json
from pathlib import Path
import time
import torch
from transformers import AutoModelForCausalLM, AttentionInterface

torch.set_num_threads(4)
MODEL = "Qwen/Qwen2.5-3B"


def reference_paths(seed):
    tag = f"phase11_massmatched_fullbatch_identity_Qwen__Qwen2.5-3B_s{seed}_v3"
    return Path("out")/(tag+".json"), Path("out/pairs")/(tag+".jsonl")


@torch.inference_mode()
def run(seed):
    began = time.perf_counter()
    output, pairpath = reference_paths(seed)
    source = sha256_file(__file__)
    if output.exists():
        result = json.loads(output.read_text(encoding="utf-8"))
        assert result["source_sha256"] == source and result["pairs_sha256"] == sha256_file(pairpath)
        return result
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["source_hashes"] == hashes()
    arrays, manifest = load_probe("phase11", MODEL, seed)
    old, old_meta = historical("phase11", MODEL, seed, arrays, manifest)
    selected = selected_indices(arrays, manifest)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=manifest["revision"],
        dtype=torch.bfloat16, attn_implementation="eager", local_files_only=True).to("cuda").eval()
    AttentionInterface.register("revision_v3_retrieval_mass", attention_forward)
    first = selected[:4]
    keys = item_keys("phase11", MODEL, seed, first, arrays)
    x = torch.tensor(arrays["input_ids"][first], device="cuda").repeat(2, 1)
    native = model(x).logits[:, -1, :].clone()
    disabled, _ = paired_forward(model, arrays["input_ids"][first], keys, disable=True)
    assert torch.equal(native, disabled), "Zero-edit reference differs from same-batch native logits"
    del native, disabled, x
    rows = []
    checks = []
    pairpath.parent.mkdir(parents=True, exist_ok=True)
    with pairpath.open("x", encoding="utf-8") as f:
        for pos in sorted(set(arrays["positions"][selected].tolist())):
            group = selected[arrays["positions"][selected] == pos]
            for start in range(0, len(group), 4):
                indices = group[start:start+4]
                scores, stats = paired_forward(model, arrays["input_ids"][indices],
                    item_keys("phase11", MODEL, seed, indices, arrays), disable=True)
                pred = scores.argmax(-1).cpu().tolist()
                logit_equal = torch.equal(scores[:len(indices)], scores[len(indices):])
                del scores
                checks.append({"indices": indices.tolist(), "validation": stats,
                               "two_native_copies_logits_bit_equal": logit_equal})
                for j, i in enumerate(indices):
                    target = int(arrays["targets"][i])
                    r = {"seed": seed, "trial_id": int(i), "position": int(pos),
                        "item": int(arrays["item_index"][i]), "target_id": target,
                        "original_prediction": old["1.0", int(i)]["prediction_id"],
                        "copy1_prediction": pred[j], "copy2_prediction": pred[len(indices)+j],
                        "payload_sha256": manifest["payload_sha256"]}
                    for arm in ["original", "copy1", "copy2"]:
                        r[arm+"_correct"] = r[arm+"_prediction"] == target
                    rows.append(r)
                    f.write(json.dumps(r, allow_nan=False)+"\n")
                f.flush()
            print(f"FULL IDENTITY Qwen3B s{seed} pos{pos}: {len(rows)}/600 items", flush=True)
    del model
    gc.collect()
    torch.cuda.empty_cache()
    assert len(rows) == 600 and [r["trial_id"] for r in rows] == selected.tolist()
    assert sha256_file(__file__) == source
    result = {"model": MODEL, "seed": seed, "dtype": "torch.bfloat16", "original_batch": 4,
        "matched_batch": 8, "n_independent_items": len(rows), "native_same_batch_identity_exact": True,
        "source_sha256": source, "main_protocol_sha256": sha256_file(PROTOCOL),
        "payload_sha256": manifest["payload_sha256"], "historical": old_meta,
        "pairs_path": pairpath.as_posix(), "pairs_sha256": sha256_file(pairpath),
        "n_original_correct": sum(r["original_correct"] for r in rows),
        "n_copy1_correct": sum(r["copy1_correct"] for r in rows),
        "n_copy2_correct": sum(r["copy2_correct"] for r in rows),
        "n_argmax_changed_original_copy1": sum(r["original_prediction"] != r["copy1_prediction"] for r in rows),
        "n_correctness_changed_original_copy1": sum(r["original_correct"] != r["copy1_correct"] for r in rows),
        "n_correctness_changed_between_copies": sum(r["copy1_correct"] != r["copy2_correct"] for r in rows),
        "batch_checks": checks, "elapsed_seconds": time.perf_counter()-began}
    write_json_new(output, result)
    log(f"Full Qwen3B matched-batch identity s{seed}: {len(rows)} items; original/copy1/copy2 correct={result['n_original_correct']}/{result['n_copy1_correct']}/{result['n_copy2_correct']}; {result['elapsed_seconds']:.3f}s")
    print(json.dumps({k: v for k, v in result.items() if k != "batch_checks"}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True, type=int, choices=[0, 1, 2])
    run(parser.parse_args().seed)
