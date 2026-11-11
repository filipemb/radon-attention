"""Last-token E4 v2 injection. Run only under /tmp/radon-gpu.lock.

Import the completed V1 harness for attention, causal normalization, identity,
last-prefix-token logits and KL. Never copy/modify its causal or empty-row logic.
Use K-1 residual ranks at the same K(2n+1) cap as SVD. Evaluate n=128 and 256 on
all 256 fixed V2 documents. Reuse V1 SVD records at n=128, run its SVD at n=256.
"""
import phase21_allocation_v2 as e4
from datetime import datetime, timezone
from functools import partial
import gc
import json
from pathlib import Path
import time
import numpy as np
import torch
from scipy.optimize import nnls
from sampling import MODELS, CORPUS_PATH, sha256_file, slug


class SymmetricNamedFirst(e4.v1.ForwardNamedFirst):
    @torch.inference_mode()
    def __call__(self, weights):
        b,h,q,k=weights.shape
        if q!=k or q!=self.dictionary.n or self.rank_cap not in (8,16):
            raise ValueError("Declared square n128/256 prefill and budget K8/16 required")
        w=weights.reshape(b*h,q,k).float()
        vectors=w.cpu().numpy().astype(np.float64).reshape(b*h,q*k)
        rhs=vectors@self.dictionary.Q
        coef=np.stack([nnls(self.dictionary.R,v,maxiter=100*len(self.dictionary.labels))[0] for v in rhs])
        if not np.isfinite(coef).all() or not np.isfinite(rhs).all():
            raise ArithmeticError("Nonfinite forward NNLS statistic; no replacement")
        gradient=coef@self.dictionary.G-rhs@self.dictionary.R
        scales=np.linalg.norm(vectors,axis=1)
        if not np.isfinite(scales).all() or np.any(scales<=0):raise ArithmeticError("Invalid attention norm")
        dual=np.maximum(0.,-gradient.min(axis=1))/scales
        comp=np.max(np.abs(coef*gradient),axis=1)/scales**2
        violation=float(max(dual.max(),comp.max(),max(0.,-coef.min())/scales.min()))
        if not np.isfinite(violation) or violation>e4.v1.KKT_RTOL:
            raise ArithmeticError(f"Forward NNLS KKT failure {violation}")
        self.max_kkt_violation=max(self.max_kkt_violation,violation)
        active=np.count_nonzero(coef>0,axis=1)
        rank=self.rank_cap-1  # Fixed symmetric convention, never selected by error.
        budget=self.rank_cap*(2*q+1)
        costs=2*active+rank*(2*q+1)
        if np.any(costs>budget):raise ArithmeticError("Forward exceeds common storage cap")
        S_cpu=(coef@self.dictionary.D.T).reshape(b*h,q,k)
        S=torch.from_numpy(S_cpu).to(device=w.device,dtype=torch.float32)
        # Import the same full exact SVD and selected cuSOLVER backend as V1.
        # Causal masking, clamping, empty-row completion and normalization below
        # remain wholly inside the imported harness.
        u,s,vh=self.harness.factor_svd(w-S,self.harness.RECON["svd_driver"])
        L=(u[...,:rank]*s[...,None,:rank])@vh[...,:rank,:]
        if self.document_costs is None:
            self.document_costs=[{"head_layer_fits":0,"common_cap_total":0,"actual_parameters_total":0,
                                  "unused_parameters_total":0,"active_atom_counts":{},"residual_rank_counts":{}} for _ in range(b)]
        if len(self.document_costs)!=b:raise ArithmeticError("Reset estimator at each batch")
        for bi in range(b):
            counts=self.document_costs[bi];sl=slice(bi*h,(bi+1)*h)
            counts["head_layer_fits"]+=h;counts["common_cap_total"]+=budget*h
            counts["actual_parameters_total"]+=int(costs[sl].sum())
            counts["unused_parameters_total"]+=int((budget-costs[sl]).sum())
            vals,freqs=np.unique(active[sl],return_counts=True)
            for value,count in zip(vals,freqs):
                label=str(int(value));counts["active_atom_counts"][label]=counts["active_atom_counts"].get(label,0)+int(count)
            label=str(rank);counts["residual_rank_counts"][label]=counts["residual_rank_counts"].get(label,0)+h
        return self.harness.normalize_reconstruction(S+L,weights.reshape(b*h,q,k),self.stats,self.empty_policy).reshape(b,h,q,k)


def paths(model,n):
    return (Path("out")/f"phase21_allocation_v2_forward_{slug(model)}_n{n}.json",
            Path("out/pairs")/f"phase21_allocation_forward_{slug(model)}_n{n}_v2.jsonl")


def require_baseline():
    config = e4.freeze()
    path = Path("out/phase2_downstream_v2.json")
    if not path.exists():
        raise RuntimeError("FALTA: out/phase2_downstream_v2.json; do not inject before required completed V1")
    deadline = datetime.fromisoformat(config["waiting_for_V1_deadline_UTC"])
    if path.stat().st_mtime > deadline.timestamp():
        raise RuntimeError("FALTA: V1 appeared after the user-defined three-hour waiting window")
    baseline = json.loads(path.read_text(encoding="utf-8"))
    required = {"prefix_length","batch","dtype","identity_kl_exactly_zero","empty_row_policy","arms","pairs_path","n_documents_effective","corpus_manifest_sha256"}
    missing = [m for m in MODELS if m not in baseline or not required.issubset(baseline[m]) or "error" in baseline[m]]
    if missing:
        raise RuntimeError("FALTA: completed V1 models " + ", ".join(missing))
    if any(baseline[m]["empty_row_policy"] != "uniform" for m in MODELS):
        raise RuntimeError("V1 does not use the required uniform-causal empty-row policy")
    return baseline,sha256_file(path)


def read_svd_records(source,model,corpus_hash):
    result = {}
    with Path(source["pairs_path"]).open(encoding="utf-8") as inp:
        for line in inp:
            row = json.loads(line)
            if row["arm"] not in ("phase2:svd:8","phase2:svd:16"):
                continue
            if (row["model"] != model or row["corpus_manifest_sha256"] != corpus_hash
                    or row["prefix_length"] != 128 or row["empty_row_policy"] != "uniform"):
                raise ValueError("V1 paired record provenance mismatch")
            if "reconstruction_rows_total" not in row["attention_validation_batch"]:
                raise ValueError("V1 SVD counters are incomplete")
            key = (row["rank"],row["doc_id"])
            if key in result:
                raise ValueError("Duplicate V1 SVD document")
            result[key] = row
    if len(result) != 512:
        raise ValueError("Incomplete V1 SVD8/16; no conditional-subset reporting")
    return result


def sum_validation(rows,key,cap):
    result,seen = {},set()
    for row in rows:
        if row["budget_rank_K"] != cap:
            continue
        batch = (row["batch_start"],row["batch_size"])
        if batch in seen:
            continue
        seen.add(batch)
        for field,value in row[key].items():
            if isinstance(value,bool):
                result[field] = result.get(field,True) and value
            elif field.startswith("max_"):
                result[field] = max(result.get(field,0),value)
            else:
                result[field] = result.get(field,0)+value
    return result


def summarize_forward(rows,model,n,source,harness,harness_hash,corpus_hash,started,sanity,pairpath):
    result = {"schema_version":2,"model":model,"n":n,"n_documents":256,"last_token_only":True,
              "batch":source["batch"],"dtype":source["dtype"],"empty_row_policy":"uniform_causal",
              "budget_rule":"common cap B=K(2n+1); named first uses fixed q=K-1 and 2*count(c>0)+q(2n+1)",
              "imported_harness_sha256":harness_hash,"corpus_manifest_sha256":corpus_hash,
              "identity_exact_in_every_batch":True,"suffix_invariance":sanity,
              "svd_driver":harness.RECON["svd_driver"],
              "max_nnls_kkt_relative_violation":max(r["batch_max_nnls_kkt_relative_violation"] for r in rows),
              "pairs_path":pairpath.as_posix(),"pairs_sha256":sha256_file(pairpath),
              "SVD_source":"Completed V1 raw per-document SVD records" if n==128 else "New n256 evaluation through imported V1 SVD, same fixed corpus/dtype/batch/policy",
              "budgets":{},"elapsed_seconds":time.perf_counter()-started}
    for cap in (8,16):
        records = [r for r in rows if r["budget_rank_K"] == cap]
        if len(records) != 256 or len({r["doc_id"] for r in records}) != 256:
            raise ValueError("Incomplete E4 forward arm")
        docs = [r["document_index"] for r in records]
        stats = {mode:sum_validation(records,mode+"_validation_batch",cap) for mode in ("named","svd")}
        completion = {mode:harness.completion_summary(s) for mode,s in stats.items()}
        for mode,counts in completion.items():
            expected_last = sum(r["budget_accounting"]["head_layer_fits"] for r in records)
            if counts["rows_total"] != n*expected_last or counts["last_query_rows_total"] != expected_last:
                raise ArithmeticError(f"{mode} completion counters do not cover every layer/head/query row")
        result["budgets"][str(cap)] = {
            "common_parameters_per_head_layer":cap*(2*n+1),"named_residual_rank":cap-1,
            "named_first_KL":e4.summarize([r["named_KL"] for r in records],docs),
            "SVD_KL":e4.summarize([r["svd_KL"] for r in records],docs),
            "paired_KL_named_minus_SVD":e4.summarize([r["named_KL"]-r["svd_KL"] for r in records],docs),
            "named_first_NLL":e4.summarize([r["named_NLL"] for r in records],docs),
            "SVD_NLL":e4.summarize([r["svd_NLL"] for r in records],docs),
            "uniform_causal_completion_by_mode":completion,"attention_validation_by_mode":stats,
            "budget_accounting": {"actual_parameters_total":sum(r["budget_accounting"]["actual_parameters_total"] for r in records),
                                  "common_cap_total":sum(r["budget_accounting"]["common_cap_total"] for r in records),
                                  "unused_parameters_total":sum(r["budget_accounting"]["unused_parameters_total"] for r in records)},
            "V1_reference_NLL_check_applicable":n==128,
            "max_reference_NLL_difference_from_V1":max(r["reference_NLL_difference_from_V1"] for r in records) if n==128 else None}
    return result


def evaluate_length(model,model_name,n,source,baseline_records,corpus,harness,harness_hash,corpus_hash):
    from transformers import AttentionInterface
    target,pairpath = paths(model_name,n)
    if target.exists():
        existing = json.loads(target.read_text(encoding="utf-8"))
        if existing["imported_harness_sha256"] != harness_hash or existing["pairs_sha256"] != sha256_file(pairpath):
            raise ValueError("Preserve existing forward artifacts: source/hash mismatch")
        return existing
    started = time.perf_counter()
    dictionary = e4.v1.Dictionary(n)
    core = json.loads(e4.core_paths(model_name,n)[0].read_text(encoding="utf-8"))
    if core["dictionary"]["sha256_float64_C_order"] != dictionary.digest:
        raise ValueError("Forward dictionary differs from audited matrix allocation")
    adapter = SymmetricNamedFirst(dictionary,harness,"uniform")
    AttentionInterface.register("phase21_allocation_v2",partial(harness.attention_forward,reconstruct_fn=adapter))
    windows = torch.tensor([d["token_ids"] for d in corpus["models"][model_name]["documents"]],dtype=torch.long)
    batch = source["batch"]
    sanity = {}
    full = windows[:1,:n+16].clone()
    changed = full.clone()
    changed[:,n:] = (changed[:,n:]+7919)%model.config.vocab_size
    model.set_attn_implementation("phase21_allocation_v2")
    for cap in (8,16):
        adapter.rank_cap = cap
        adapter.reset(); a = harness.last_logits(model,full,n)
        adapter.reset(); b = harness.last_logits(model,changed,n)
        if not torch.equal(a,b):
            raise ArithmeticError("Suffix changes affected the evaluated last-prefix-token logit")
        sanity[str(cap)] = {"passed_exact":True,"max_logit_difference":float((a-b).abs().max())}
    rows = []
    if pairpath.exists():
        with pairpath.open(encoding="utf-8") as inp:
            rows = [json.loads(line) for line in inp]
        if any(r["imported_harness_sha256"] != harness_hash or r["corpus_manifest_sha256"] != corpus_hash
               or r["empty_row_policy"] != "uniform" or not r["identity_exact"] for r in rows):
            raise ValueError("Forward resume provenance mismatch")
    seen = {(r["budget_rank_K"],r["doc_id"]) for r in rows}
    if len(seen) != len(rows):
        raise ValueError("Duplicate E4 forward raw record")
    pairpath.parent.mkdir(parents=True,exist_ok=True)
    e4.log(f"FORWARD START {model_name} n={n}; 256 docs; K=8,16 q=7,15; uniform causal; shared V1 harness")
    with pairpath.open("a",encoding="utf-8") as out:
        for start in range(0,len(windows),batch):
            sequences = windows[start:start+batch]
            targets = sequences[:,n]
            ids = [d["doc_id"] for d in corpus["documents"][start:start+len(sequences)]]
            if all((cap,doc) in seen for cap in (8,16) for doc in ids):
                continue
            model.set_attn_implementation("eager")
            ref = harness.last_logits(model,sequences,n)
            _,ref_nll = harness.kl_nll(ref,ref,targets)
            harness.activate(model,("phase2","identity",None))
            identity = harness.last_logits(model,sequences,n)
            if not torch.equal(ref,identity):
                raise ArithmeticError("Imported harness identity differs from native eager")
            for cap in (8,16):
                if all((cap,doc) in seen for doc in ids):
                    continue
                adapter.rank_cap = cap
                adapter.reset()
                model.set_attn_implementation("phase21_allocation_v2")
                named = harness.last_logits(model,sequences,n)
                named_kl,named_nll = harness.kl_nll(ref,named,targets)
                named_stats = dict(adapter.stats)
                costs = adapter.document_costs
                if n == 256:
                    svd_stats = harness.activate(model,("phase2","svd",cap))
                    svd = harness.last_logits(model,sequences,n)
                    svd_kl,svd_nll = harness.kl_nll(ref,svd,targets)
                    svd_stats = dict(svd_stats)
                for bi,doc in enumerate(ids):
                    if (cap,doc) in seen:
                        continue
                    if n == 128:
                        base = baseline_records[cap,doc]
                        if (base["target_id"] != int(targets[bi]) or base["document_index"] != start+bi
                                or base["evaluation_batch_start"] != start or base["evaluation_batch_size"] != len(sequences)):
                            raise ValueError("V1 target/document/batch differs")
                        delta_ref = abs(float(ref_nll[bi])-base["reference_nll"])
                        if delta_ref > 2e-5:
                            raise ArithmeticError(f"V1 eager reference NLL differs: {delta_ref}")
                        svd_kl_i,svd_nll_i,svd_stats_i = base["kl"],base["nll"],base["attention_validation_batch"]
                    else:
                        delta_ref = None  # No n256 V1 reference exists; never impute zero agreement.
                        svd_kl_i,svd_nll_i,svd_stats_i = float(svd_kl[bi]),float(svd_nll[bi]),svd_stats
                    row = {"schema_version":2,"model":model_name,"n":n,"document_index":start+bi,"doc_id":doc,
                           "offset":corpus["models"][model_name]["documents"][start+bi]["offset"],
                           "target_id":int(targets[bi]),"budget_rank_K":cap,"residual_rank":cap-1,
                           "common_cap_per_head_layer":cap*(2*n+1),"budget_accounting":costs[bi],
                           "batch_start":start,"batch_size":len(sequences),"identity_exact":True,
                           "named_KL":float(named_kl[bi]),"svd_KL":float(svd_kl_i),
                           "named_NLL":float(named_nll[bi]),"svd_NLL":float(svd_nll_i),"reference_NLL":float(ref_nll[bi]),
                           "reference_NLL_difference_from_V1":delta_ref,
                           "named_validation_batch":named_stats,"svd_validation_batch":dict(svd_stats_i),
                           "batch_max_nnls_kkt_relative_violation":adapter.max_kkt_violation,
                           "svd_driver":harness.RECON["svd_driver"],
                           "empty_row_policy":"uniform","imported_harness_sha256":harness_hash,
                           "corpus_manifest_sha256":corpus_hash}
                    out.write(json.dumps(row,allow_nan=False,separators=(",",":"))+"\n")
                    rows.append(row); seen.add((cap,doc))
            out.flush()
            if (start+len(sequences))%16 == 0:
                e4.log(f"FORWARD {model_name} n={n}: {start+len(sequences)}/256 docs; seconds={time.perf_counter()-started:.1f}")
    result = summarize_forward(rows,model_name,n,source,harness,harness_hash,corpus_hash,started,sanity,pairpath)
    e4.write_new(target,result)
    e4.log(f"FORWARD DONE {model_name} n={n}: all 256 docs at K8/16; counters by mode saved")
    return result


def main():
    baseline,baseline_hash = require_baseline()
    import phase2_downstream as harness
    from transformers import AutoModelForCausalLM, AttentionInterface
    harness_hash = sha256_file("phase2_downstream.py")
    required = ("attention_forward","normalize_reconstruction","last_logits","kl_nll","completion_summary","factor_svd")
    if any(not hasattr(harness,name) for name in required):
        raise ValueError("Completed V1 lacks required reusable APIs")
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    corpus_hash = sha256_file(CORPUS_PATH)
    AttentionInterface.register("p0_recon",harness.attention_forward)
    harness.RECON["empty_row_policy"] = "uniform"
    # V1 is still being repaired by its owner. Tie the final adapter control
    # to the exact completed source version, without overwriting older checks.
    control_path=Path("out")/f"phase21_allocation_v2_injection_adapter_{harness_hash[:12]}.json"
    if not control_path.exists():
        from phase21_allocation_v2_checks import main as check_completed_harness
        check_completed_harness(control_path)
    control=json.loads(control_path.read_text(encoding="utf-8"))
    if not control["passed"] or control["imported_harness_sha256"]!=harness_hash:
        raise ValueError("Completed-harness estimator control failed or changed source")
    results = {}
    for name in MODELS:
        source = baseline[name]
        if source["corpus_manifest_sha256"] != corpus_hash or source["n_documents_effective"] != 256 or source["prefix_length"]!=128 or not source["identity_kl_exactly_zero"]:
            raise ValueError("V1 corpus/endpoints/identity mismatch")
        bases = read_svd_records(source,name,corpus_hash)
        driver=source.get("svd_implementation",{}).get("selected_driver")
        if any(row.get("svd_driver")!=driver for row in bases.values()):
            raise ValueError("V1 per-document and aggregate exact SVD backends differ")
        harness.RECON["svd_driver"]=driver
        if all(paths(name,n)[0].exists() for n in (128,256)):
            results[name] = {str(n):json.loads(paths(name,n)[0].read_text(encoding="utf-8")) for n in (128,256)}
            for n in (128,256):
                cached=results[name][str(n)]
                if (cached["imported_harness_sha256"]!=harness_hash or cached["corpus_manifest_sha256"]!=corpus_hash
                        or cached["pairs_sha256"]!=sha256_file(paths(name,n)[1])):
                    raise ValueError("Preserve existing forward artifacts: resume source/corpus/pairs mismatch")
            continue
        dtype = {"torch.float32":torch.float32,"torch.bfloat16":torch.bfloat16}[source["dtype"]]
        model = AutoModelForCausalLM.from_pretrained(name,revision=corpus["models"][name]["revision"],
            local_files_only=True,dtype=dtype,attn_implementation="eager").to("cuda").eval()
        torch.manual_seed(0)
        results[name] = {str(n):evaluate_length(model,name,n,source,bases,corpus,harness,harness_hash,corpus_hash) for n in (128,256)}
        del model
        gc.collect(); torch.cuda.empty_cache()
    if sha256_file("phase2_downstream.py") != harness_hash:
        raise ValueError("Harness source changed during injection; preserve records and audit")
    e4.write_new("out/phase21_allocation_v2_forward.json",{
        "_meta":{"source_V1_sha256":baseline_hash,"imported_harness_sha256":harness_hash,
                 "estimator_checks_path":control_path.as_posix(),"estimator_checks_sha256":sha256_file(control_path),
                 "allocation_adapter_source_sha256":sha256_file("phase21_allocation_v2_forward.py"),
                 "corpus_manifest_sha256":corpus_hash,"n_documents":256,"prefix_lengths":[128,256],
                 "uniform_causal_completion":True,"rank_rule":"q=K-1, K in {8,16}",
                 "GPU_command":"flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase21_allocation_v2_forward.py",
                 "primary_statistics":"Imported phase24.describe: instance median, 2000 document-block bootstrap; document means secondary"},
        "models":results})


if __name__ == "__main__":
    main()
