"""Paired tests on the V1 downstream results (last-token KL, 256 articles per model).

Compares rank-16 SVD with the 15-atom geometric reconstruction (matched component
count) per article: Wilcoxon signed-rank on the per-article KL difference, matched-pairs
rank-biserial correlation, and the share of articles in which the SVD has lower KL.
Reads out/phase2_downstream_v2.json and its pair ledgers; writes
out/phase32_downstream_tests.json (refuses to overwrite).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2")
import json
from pathlib import Path
import numpy as np
from scipy.stats import rankdata, wilcoxon

MODELS = ["gpt2", "gpt2-medium", "EleutherAI/pythia-410m", "EleutherAI/pythia-1.4b",
          "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-3B"]
PAIRS = [("phase2:svd:16", "phase2:geom"), ("phase2:svd:8", "phase2:geom")]


def rank_biserial(diff):
    nz = diff[diff != 0]
    r = rankdata(np.abs(nz))
    return float((r[nz > 0].sum() - r[nz < 0].sum()) / r.sum())


def main():
    src = json.loads(Path("out/phase2_downstream_v2.json").read_text(encoding="utf-8"))
    out = {"source": "out/phase2_downstream_v2.json", "unit": "article (last-token KL)",
           "test": "two-sided Wilcoxon signed-rank on per-article KL difference a-b",
           "effect_size": "matched-pairs rank-biserial; negative favors a", "results": {}}
    for model in MODELS:
        kl = {}
        for line in open(src[model]["pairs_path"], encoding="utf-8"):
            row = json.loads(line)
            kl.setdefault(row["arm"], {})[row["doc_id"]] = row["kl"]
        res = {}
        for a, b in PAIRS:
            docs = sorted(kl[b])
            if sorted(kl[a]) != docs:
                raise RuntimeError(f"{model}: article sets differ between {a} and {b}")
            diff = np.array([kl[a][x] - kl[b][x] for x in docs])
            res[f"{a} - {b}"] = {"n_articles": len(docs), "median_difference": float(np.median(diff)),
                                 "wilcoxon_p": float(wilcoxon(diff).pvalue),
                                 "rank_biserial": rank_biserial(diff),
                                 "share_a_lower": float((diff < 0).mean())}
        out["results"][model] = res
    target = Path("out/phase32_downstream_tests.json")
    if target.exists():
        raise RuntimeError(f"{target} exists; refusing to overwrite")
    target.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out["results"], indent=1))


if __name__ == "__main__":
    main()
