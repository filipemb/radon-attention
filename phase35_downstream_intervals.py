"""Document bootstrap intervals for the frozen V1 downstream ledgers.

Each arm has one evaluated token per article. One shared seed-0 document
resampling is used for all arms and models; no row or arm is filtered.
"""
from sampling import MODELS, CORPUS_PATH, sha256_file, write_json_new, progress
import hashlib
import json
from pathlib import Path
import time
import numpy as np


def main():
    started=time.perf_counter()
    corpus=json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    documents=[d["doc_id"] for d in corpus["documents"]]
    assert len(documents)==256 and len(set(documents))==256
    draws=np.random.default_rng(0).integers(0,256,size=(2000,256))
    result={"_meta":{"primary_statistic":"median KL per document",
        "secondary_statistic":"mean KL; mean NLL for likelihood/perplexity",
        "bootstrap_unit":"document; one evaluated next token per document per arm",
        "n_documents_per_arm":256,"n_bootstrap":2000,"bootstrap_seed":0,
        "shared_resampling_across_all_models_and_arms":True,
        "quantile_method":"linear; percentile interval at 2.5 and 97.5",
        "draws_sha256":hashlib.sha256(draws.astype("<i8").tobytes()).hexdigest(),
        "corpus_manifest_sha256":sha256_file(CORPUS_PATH),
        "source_aggregates":["out/phase2_downstream_v2.json","out/phase7_editability_v2.json"],
        "existing_aggregates_modified":False,"inferential_pvalues_added":False}}
    roots=[json.loads(Path(p).read_text(encoding="utf-8")) for p in result["_meta"]["source_aggregates"]]
    for name in MODELS:
        rawpath=Path(roots[0][name]["pairs_path"])
        assert roots[1][name]["pairs_path"]==str(rawpath).replace("\\","/")
        records=[json.loads(s) for s in rawpath.read_text(encoding="utf-8").splitlines()]
        arms={}
        for root in roots:
            source=root[name]
            assert source["corpus_manifest_sha256"]==result["_meta"]["corpus_manifest_sha256"]
            for arm,summary in source["arms"].items():
                rows=sorted((r for r in records if r["arm"]==arm),key=lambda r:r["document_index"])
                assert [r["doc_id"] for r in rows]==documents
                values=np.asarray([r["kl"] for r in rows],dtype=np.float64)
                nll=np.asarray([r["nll"] for r in rows],dtype=np.float64)
                assert np.isfinite(values).all() and np.isfinite(nll).all()
                assert abs(float(np.median(values))-summary["median_kl"])<=1e-12
                assert abs(float(np.mean(values))-summary["mean_kl"])<=1e-12
                assert abs(float(np.mean(nll))-summary["mean_nll"])<=1e-12
                sampled=values[draws]
                arms[arm]={"n_documents":256,"n_evaluated_tokens":256,
                    "median_kl":float(np.median(values)),
                    "median_kl_ci95_document_bootstrap":np.quantile(np.median(sampled,axis=1),[.025,.975],method="linear").tolist(),
                    "mean_kl":float(np.mean(values)),
                    "mean_kl_ci95_document_bootstrap":np.quantile(np.mean(sampled,axis=1),[.025,.975],method="linear").tolist(),
                    "mean_nll":float(np.mean(nll))}
        assert len(arms)==15
        result[name]={"pairs_path":rawpath.as_posix(),"pairs_sha256":sha256_file(rawpath),"arms":arms}
    result["_meta"]["n_arms_total"]=90
    result["_meta"]["n_raw_records_total"]=23040
    result["_meta"]["elapsed_seconds"]=time.perf_counter()-started
    write_json_new("out/phase2_document_statistics_v2.json",result)
    progress("V1 document intervals","90 arms, 256 identical documents each; median and secondary mean KL intervals; one shared seed0 block bootstrap, no filtering",
             result["_meta"]["elapsed_seconds"],".venv/Scripts/python.exe -B phase35_downstream_intervals.py")
    print(f"V1 document intervals saved: {result['_meta']['elapsed_seconds']:.3f}s",flush=True)


if __name__=="__main__":main()
