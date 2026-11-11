"""E9 last-token forward, imported V1 harness, one model per GPU lock."""
import phase50_als as als
import argparse
from functools import partial
import gc
import json
from pathlib import Path
import time
import numpy as np
from scipy.optimize import nnls
import torch
from transformers import AutoModelForCausalLM, AttentionInterface
import phase2_downstream as harness
from phase21_allocation_v2_forward import SymmetricNamedFirst
from phase50_experiment import (read, jsonl, PROTOCOL, ARMS, FORWARD_COMPARISONS,
                                Dictionary, describe, paired, holm, summarize_diagnostics)
from sampling import MODELS, CORPUS_PATH, sha256_file, slug, write_json_new

torch.set_num_threads(4)


def source_records(model):
    protocol=read(PROTOCOL); corpus=read(CORPUS_PATH); source=read("out/phase2_downstream_v2.json")[model]
    cfg=protocol["datasets"][model]
    if (source["dtype"]!=cfg["dtype"] or source["batch"]!=cfg["batch"] or source["prefix_length"]!=128
            or source["n_documents_effective"]!=256 or source["corpus_manifest_sha256"]!=protocol["corpus_manifest_sha256"]):
        raise ValueError("Frozen model/dtype/batch/corpus/endpoints changed")
    basepath=Path(source["pairs_path"])
    e4path=Path(f"out/pairs/phase21_allocation_forward_{slug(model)}_n128_v2.jsonl")
    for path in (basepath,e4path):
        if sha256_file(path)!=protocol["source_files"][path.as_posix()]:
            raise ValueError("Immutable forward input changed")
    a={}; identity={}
    for row in jsonl(basepath):
        if row["arm"]=="phase2:identity": identity[row["document_index"]]=row
        if row["arm"] in ("phase2:svd:8","phase2:svd:16"):
            key=(row["rank"],row["document_index"])
            if key in a: raise ValueError("Duplicate V1 source record")
            a[key]=row
    d={}
    for row in jsonl(e4path):
        key=(row["budget_rank_K"],row["document_index"])
        if key in d: raise ValueError("Duplicate E4 source record")
        d[key]=row
    if len(a)!=512 or len(d)!=512 or len(identity)!=256:
        raise ValueError("All256 V1 and E4 articles required at both K")
    for (k,di), row in a.items():
        other=d[k,di]; doc=corpus["documents"][di]; window=corpus["models"][model]["documents"][di]
        if (row["model"]!=model or row["doc_id"]!=doc["doc_id"] or row["prefix_length"]!=128
                or row["arm"]!=f"phase2:svd:{k}"
                or row["corpus_manifest_sha256"]!=protocol["corpus_manifest_sha256"]
                or row["target_id"]!=window["token_ids"][128] or row["offset"]!=window["offset"]
                or row["empty_row_policy"]!="uniform" or row["evaluation_batch_size"]!=source["batch"]
                or row["evaluation_batch_start"]!=di-di%source["batch"]):
            raise ValueError("V1 forward provenance mismatch")
        if (other["doc_id"]!=row["doc_id"] or other["target_id"]!=row["target_id"]
                or other["residual_rank"]!=k-1 or other["common_cap_per_head_layer"]!=k*257
                or other["batch_start"]!=row["evaluation_batch_start"] or other["batch_size"]!=row["evaluation_batch_size"]
                or other["svd_KL"]!=row["kl"] or other["svd_NLL"]!=row["nll"]
                or not other["identity_exact"] or other["corpus_manifest_sha256"]!=protocol["corpus_manifest_sha256"]):
            raise ValueError("E4 reused SVD does not equal V1 exactly")
        ident=identity[di]
        if ident["kl"]!=0 or ident["nll"]!=ident["reference_nll"]:
            raise ValueError("V1 identity is not exact")
    return a,d,source,corpus


def reuse(model):
    """Immutable baseline observations, all documents, no conditional omission."""
    path=Path(f"out/phase50_reused_{slug(model)}.json")
    pairpath=Path(f"out/pairs/phase50_reused_{slug(model)}.jsonl")
    if path.exists():
        result=read(path)
        if result["protocol_sha256"]!=sha256_file(PROTOCOL) or result["pairs_sha256"]!=sha256_file(pairpath):
            raise ValueError("Reused output changed")
        return result
    a,d,source,corpus=source_records(model); protocol=read(PROTOCOL); ph=sha256_file(PROTOCOL)
    records=[]
    for k in (8,16):
        for di in range(256):
            base=a[k,di]; named=d[k,di]
            common={"model":model,"K":k,"document_index":di,"doc_id":base["doc_id"],"offset":base["offset"],
                    "target_id":base["target_id"],"n":128,"dtype":source["dtype"],"batch_start":base["evaluation_batch_start"],
                    "batch_size":base["evaluation_batch_size"],"protocol_sha256":ph,
                    "corpus_manifest_sha256":protocol["corpus_manifest_sha256"],"empty_row_policy":"uniform"}
            records.append({**common,"arm":"svd_K","kl":base["kl"],"nll":base["nll"],"reference_nll":base["reference_nll"],
                            "source_path":source["pairs_path"],"source_arm":base["arm"],"reused_exact":True,
                            "attention_validation_batch":base["attention_validation_batch"]})
            records.append({**common,"arm":"named_plus_svd","kl":named["named_KL"],"nll":named["named_NLL"],
                            "reference_nll":named["reference_NLL"],"source_path":f"out/pairs/phase21_allocation_forward_{slug(model)}_n128_v2.jsonl",
                            "source_arm":"S_named_first+L_K-1","reused_exact":True,
                            "attention_validation_batch":named["named_validation_batch"]})
    pairpath.parent.mkdir(parents=True,exist_ok=True)
    with pairpath.open("x",encoding="utf-8") as out:
        for row in records: out.write(json.dumps(row,allow_nan=False,separators=(",",":"))+"\n")
    result={"model":model,"protocol_sha256":ph,"pairs_path":pairpath.as_posix(),"pairs_sha256":sha256_file(pairpath),
            "n_records":len(records),"all_V1_E4_reused_SVD_equal_exact":True,"V1_identity_KL_exactly_zero":True}
    write_json_new(path,result)
    return result


class MaskedAdapter:
    def __init__(self,dictionary,diag_heads):
        self.dictionary=dictionary; self.diag_heads=set(map(tuple,diag_heads)); self.arm=None; self.k=None
        self.reset()

    def reset(self):
        self.stats=harness.DeferredStats(); self.calls=0; self.infos=[]; self.document_infos=None
        self.kkt=0.; self.max_active=0

    def project_named(self,w):
        vectors=w.cpu().numpy().astype(np.float64).reshape(len(w),-1)
        rhs=vectors@self.dictionary.Q
        coef=np.stack([nnls(self.dictionary.R,x,maxiter=100*len(self.dictionary.labels))[0] for x in rhs])
        gradient=coef@self.dictionary.G-rhs@self.dictionary.R; scale=np.linalg.norm(vectors,axis=1)
        violation=float(max((np.maximum(0.,-gradient.min(1))/scale).max(),
                            (np.max(np.abs(coef*gradient),axis=1)/scale**2).max(),max(0.,-coef.min())/scale.min()))
        if not np.isfinite(violation) or violation>1e-8: raise ArithmeticError(f"NNLS KKT failure {violation}")
        active=np.count_nonzero(coef>0,axis=1)
        if np.any(2*active+2*128*(self.k-1)>self.k*257): raise ValueError("S+masked common cap exceeded")
        self.kkt=max(self.kkt,violation); self.max_active=max(self.max_active,int(active.max()))
        # Exactly the float32 named S injected by the E4 adapter.
        return torch.from_numpy((coef@self.dictionary.D.T).reshape(w.shape)).to(device=w.device,dtype=torch.float32)

    @torch.inference_mode()
    def reconstruct(self,weights,module):
        b,h,q,n=weights.shape
        if q!=128 or n!=128: raise ValueError("E9 is the frozen128-token square prefill")
        self.calls+=1
        layer=getattr(module,"layer_idx",None)
        if layer is None:layer=getattr(module,"layer_index",None)
        if layer is None: raise ValueError("Cannot determine layer index")
        layer=int(layer)
        if self.arm=="svd_K_diag_exact":
            harness.RECON.update(mode="svd",k=self.k,stats=self.stats)
            rec=harness.reconstruct(weights)
            heads=[hh for ll,hh in self.diag_heads if ll==layer]
            if heads: rec[:,heads]=weights[:,heads]
            harness.validate_attention(rec,self.stats)
            return rec
        keep=torch.tensor([not (self.arm=="masked_K_diag_exact" and (layer,hh) in self.diag_heads) for hh in range(h)],device=weights.device)
        keep_heads=keep.nonzero().flatten().cpu().tolist()
        if not keep_heads:
            harness.record_reconstruction_rows(weights,self.stats); harness.validate_attention(weights,self.stats)
            return weights
        original=weights[:,keep].reshape(b*len(keep_heads),q,n)
        w=original.float()
        named=self.project_named(w) if self.arm=="named_plus_masked" else 0
        target=w.double()-(named.double() if torch.is_tensor(named) else 0)
        rank=self.k-1 if self.arm=="named_plus_masked" else self.k
        product,infos=als.fit_gpu(target,rank,harness.causal_support(q,n,w.device))
        if self.document_infos is None: self.document_infos=[[] for _ in range(b)]
        for bi in range(b):
            self.document_infos[bi].extend(infos[bi*len(keep_heads):(bi+1)*len(keep_heads)])
        for bi in range(b):
            for j,head in enumerate(keep_heads):
                self.infos.append({"batch_document":bi,"layer":layer,"head":head,**infos[bi*len(keep_heads)+j]})
        rec=harness.normalize_reconstruction(product+named,original,self.stats,"uniform").reshape(b,len(keep_heads),q,n)
        result=weights.clone(); result[:,keep]=rec
        if len(keep_heads)<h:
            harness.record_reconstruction_rows(weights[:,~keep],self.stats)
        harness.validate_attention(result,self.stats)
        return result


def attention(adapter,module,query,key,value,attention_mask,scaling=None,dropout=0.,**kwargs):
    return harness.attention_forward(module,query,key,value,attention_mask,scaling,dropout,
                                    reconstruct_fn=partial(adapter.reconstruct,module=module),**kwargs)


def finalize_model(name,elapsed_fallback=0.):
    protocol=read(PROTOCOL);ph=sha256_file(PROTOCOL);cfg=protocol["datasets"][name]
    target=Path(f"out/phase50_forward_{slug(name)}.json");pairpath=Path(f"out/pairs/phase50_forward_{slug(name)}.jsonl")
    if target.exists():
        previous=read(target)
        if previous["protocol_sha256"]!=ph or previous["pairs_sha256"]!=sha256_file(pairpath):raise ValueError("Completed model output changed")
        return previous
    modes=["masked_K","named_plus_masked"]+(["svd_K_diag_exact","masked_K_diag_exact"] if cfg["diagonal_heads"] else [])
    rows=jsonl(pairpath);keys={(r["arm"],r["K"],r["document_index"]) for r in rows}
    expected={(arm,k,i) for arm in modes for k in (8,16) for i in range(256)}
    if keys!=expected or len(rows)!=len(keys) or any(r["protocol_sha256"]!=ph or r["model"]!=name for r in rows):
        raise ValueError("Cannot finalize incomplete or mixed forward records")
    proof=Path(f"out/phase50_forward_sanity_{slug(name)}.json")
    if read(proof)["protocol_sha256"]!=ph:raise ValueError("Forward sanity/protocol mismatch")
    chunks=sorted(Path("out").glob(f"phase50_forward_chunk_{slug(name)}_*.json"))
    result={"model":name,"protocol_sha256":ph,"pairs_path":pairpath.as_posix(),"pairs_sha256":sha256_file(pairpath),
            "n_records":len(rows),"n_articles":256,"diagonal_heads":cfg["diagonal_heads"],"sanity_path":proof.as_posix(),
            "elapsed_seconds":sum(read(p)["elapsed_seconds"] for p in chunks) if chunks else elapsed_fallback,
            "dtype":cfg["dtype"],"arms_run":modes,"GPU_lock_released_between_chunks":bool(chunks),
            "chunk_paths":[p.as_posix() for p in chunks],
            "aliases":{} if cfg["diagonal_heads"] else {"svd_K_diag_exact":"svd_K","masked_K_diag_exact":"masked_K"}}
    write_json_new(target,result);return result


def gpu_model(name,start_doc=0,stop_doc=256):
    if not Path("out/phase50_matrix_summary.json").exists():
        raise RuntimeError("Complete CPU matrix stage before forward")
    validation=read(f"out/phase50_estimator_validation_{slug(name)}.json")
    if (not validation["passed"] or validation["n_matrices"]<32 or validation["protocol_sha256"]!=sha256_file(PROTOCOL)
            or validation["GPU_solver"]!=als.GPU_SOLVER
            or validation["correction_policy_sha256"]!=sha256_file("out/phase50_numerical_fallback.json")
            or validation["estimator_implementation_sha256"]!=sha256_file("phase50_als.py")):
        raise RuntimeError("32-matrix independent CPU-double/GPU-double validation required")
    reuse(name); a,d,source,corpus=source_records(name)
    protocol=read(PROTOCOL); ph=sha256_file(PROTOCOL); cfg=protocol["datasets"][name]
    target=Path(f"out/phase50_forward_{slug(name)}.json"); pairpath=Path(f"out/pairs/phase50_forward_{slug(name)}.jsonl")
    proofpath=Path(f"out/phase50_forward_sanity_{slug(name)}.json")
    chunkpath=Path(f"out/phase50_forward_chunk_{slug(name)}_{start_doc:03d}_{stop_doc:03d}.json")
    if not (0<=start_doc<stop_doc<=256 and start_doc%source["batch"]==0 and stop_doc%source["batch"]==0):
        raise ValueError("Chunk boundaries must respect the unchanged V1 batch and full corpus")
    if target.exists():
        old=read(target)
        if old["protocol_sha256"]!=ph or old["pairs_sha256"]!=sha256_file(pairpath): raise ValueError("Existing forward result changed")
        return old
    if chunkpath.exists():
        previous=read(chunkpath)
        if previous["protocol_sha256"]!=ph: raise ValueError("Chunk/protocol mismatch")
        with pairpath.open("rb") as inp:
            prefix=inp.read(previous["pairs_byte_length_at_chunk_completion"])
        import hashlib
        if hashlib.sha256(prefix).hexdigest()!=previous["pairs_prefix_sha256"]: raise ValueError("Completed chunk records changed")
        return previous
    dtype={"torch.float32":torch.float32,"torch.bfloat16":torch.bfloat16}[source["dtype"]]
    model=AutoModelForCausalLM.from_pretrained(name,revision=corpus["models"][name]["revision"],
            local_files_only=True,dtype=dtype,attn_implementation="eager").to("cuda").eval()
    torch.manual_seed(0)
    harness.RECON.update(empty_row_policy="uniform",svd_driver=None,parallel_svd=False)
    dictionary=Dictionary(128); adapter=MaskedAdapter(dictionary,cfg["diagonal_heads"])
    source_dictionary=read(f"out/phase21_allocation_v2_core_{slug(name)}_n128.json")["dictionary"]["sha256_float64_C_order"]
    if dictionary.digest!=source_dictionary:raise ValueError("Named dictionary changed from the E4 matrix/forward experiment")
    named_adapter=SymmetricNamedFirst(dictionary,harness,"uniform")
    AttentionInterface.register("p0_recon",harness.attention_forward)
    AttentionInterface.register("phase50_masked",partial(attention,adapter))
    AttentionInterface.register("phase50_named_svd",partial(harness.attention_forward,reconstruct_fn=named_adapter))
    windows=torch.tensor([x["token_ids"] for x in corpus["models"][name]["documents"]],dtype=torch.long)
    batch=source["batch"]; started=time.perf_counter()
    proof={"model":name,"protocol_sha256":ph,"identity_KL_exactly_zero":True,"baseline_checks":[],"harness_sha256":sha256_file("phase2_downstream.py")}
    if proof["harness_sha256"]!=protocol["harness_sha256_at_freeze"]: raise ValueError("Harness changed since freeze")
    # Baseline equality checked on the actual model/dtype/batch before new arms.
    sequences=windows[:batch]; targets=sequences[:,128]
    model.set_attn_implementation("eager"); reference=harness.last_logits(model,sequences,128)
    harness.activate(model,("phase2","identity",None),deferred=True)
    ident=harness.last_logits(model,sequences,128); harness.RECON["stats"].finalize("E9 identity")
    kl,nll=harness.kl_nll(reference,ident,targets)
    if not torch.equal(reference,ident) or np.any(kl!=0): raise AssertionError("Identity KL/logits failed")
    for k in (8,16):
        harness.activate(model,("phase2","svd",k),deferred=True)
        logits=harness.last_logits(model,sequences,128); harness.RECON["stats"].finalize("E9 reused SVD equality")
        ck,cn=harness.kl_nll(reference,logits,targets)
        named_adapter.rank_cap=k; named_adapter.reset(); model.set_attn_implementation("phase50_named_svd")
        logits=harness.last_logits(model,sequences,128); dk,dn=harness.kl_nll(reference,logits,targets)
        diffs={"svd_KL":max(abs(float(ck[i])-a[k,i]["kl"]) for i in range(batch)),
               "svd_NLL":max(abs(float(cn[i])-a[k,i]["nll"]) for i in range(batch)),
               "named_KL":max(abs(float(dk[i])-d[k,i]["named_KL"]) for i in range(batch)),
               "named_NLL":max(abs(float(dn[i])-d[k,i]["named_NLL"]) for i in range(batch))}
        if max(diffs.values())>2e-5: raise AssertionError(f"Baseline rerun disagreement {diffs}")
        proof["baseline_checks"].append({"K":k,"n_articles":batch,"max_absolute_differences":diffs,"bit_exact_scalar_values":all(v==0 for v in diffs.values())})
    if proofpath.exists():
        if read(proofpath)!=proof: raise ValueError("Existing forward sanity proof differs")
    else: write_json_new(proofpath,proof)
    rows=jsonl(pairpath) if pairpath.exists() else []; seen={(r["arm"],r["K"],r["document_index"]) for r in rows}
    if len(seen)!=len(rows) or any(r["protocol_sha256"]!=ph for r in rows): raise ValueError("Invalid forward resume")
    modes=["masked_K","named_plus_masked"]+(["svd_K_diag_exact","masked_K_diag_exact"] if cfg["diagonal_heads"] else [])
    als.enable_parallel_cpu_corrections(3)
    fit_policy_hash=sha256_file("out/phase50_numerical_fallback.json")
    estimator_source_hash=sha256_file("phase50_als.py")
    pairpath.parent.mkdir(parents=True,exist_ok=True)
    with pairpath.open("a",encoding="utf-8") as out:
        for start in range(start_doc,stop_doc,batch):
            if all((arm,k,i) in seen for arm in modes for k in (8,16) for i in range(start,start+batch)): continue
            sequences=windows[start:start+batch]; targets=sequences[:,128]
            model.set_attn_implementation("eager"); ref=harness.last_logits(model,sequences,128)
            _,refn=harness.kl_nll(ref,ref,targets)
            harness.activate(model,("phase2","identity",None),deferred=True)
            ident=harness.last_logits(model,sequences,128); harness.RECON["stats"].finalize("E9 per-batch identity")
            ik,_=harness.kl_nll(ref,ident,targets)
            if not torch.equal(ref,ident) or np.any(ik!=0): raise AssertionError("Per-batch identity failed")
            for k in (8,16):
                for arm in modes:
                    if all((arm,k,i) in seen for i in range(start,start+batch)): continue
                    adapter.arm=arm; adapter.k=k; adapter.reset(); model.set_attn_implementation("phase50_masked")
                    logits=harness.last_logits(model,sequences,128)
                    adapter.stats.finalize(f"E9 {name} {arm} K{k} articles{start}:{start+batch}")
                    layers=corpus["models"][name]["n_layers"];heads=corpus["models"][name]["n_heads"]
                    if adapter.calls!=layers or adapter.stats.get("reconstruction_rows_total")!=batch*heads*128*layers:
                        raise AssertionError("The injected estimator did not visit every declared head, row and layer")
                    kl,nll=harness.kl_nll(ref,logits,targets)
                    for bi in range(batch):
                        di=start+bi
                        if abs(float(refn[bi])-a[k,di]["reference_nll"])>2e-5: raise ValueError("Native V1 reference drift")
                        if (arm,k,di) in seen: continue
                        row={"model":name,"arm":arm,"K":k,"document_index":di,"doc_id":corpus["documents"][di]["doc_id"],
                             "offset":corpus["models"][name]["documents"][di]["offset"],"n":128,"target_id":int(targets[bi]),
                             "dtype":source["dtype"],"batch_start":start,"batch_size":batch,
                             "kl":float(kl[bi]),"nll":float(nll[bi]),"reference_nll":float(refn[bi]),
                             "identity_KL":float(ik[bi]),"protocol_sha256":ph,"empty_row_policy":"uniform",
                             "fit_policy_sha256":fit_policy_hash,"estimator_implementation_sha256":estimator_source_hash,
                             "corpus_manifest_sha256":protocol["corpus_manifest_sha256"],
                             "attention_validation_batch":dict(adapter.stats),"diagonal_heads":cfg["diagonal_heads"],
                             "max_NNLS_KKT":adapter.kkt,"max_active_atoms":adapter.max_active,
                             "ALS":summarize_diagnostics(adapter.document_infos[bi]) if adapter.document_infos else None}
                        out.write(json.dumps(row,allow_nan=False,separators=(",",":"))+"\n"); out.flush()
                        rows.append(row); seen.add((arm,k,di))
                    print(f"FORWARD {name} docs{start}:{start+batch} K{k} {arm}; elapsed={time.perf_counter()-started:.1f}s",flush=True)
    expected=256*2*len(modes)
    if start_doc!=0 or stop_doc!=256:
        if not all((arm,k,i) in seen for arm in modes for k in (8,16) for i in range(start_doc,stop_doc)):
            raise ValueError("Incomplete declared forward chunk")
        chunk={"model":name,"start_document":start_doc,"stop_document":stop_doc,"protocol_sha256":ph,
               "pairs_byte_length_at_chunk_completion":pairpath.stat().st_size,"pairs_prefix_sha256":sha256_file(pairpath),
               "elapsed_seconds":time.perf_counter()-started,"n_records_completed_so_far":len(rows)}
        write_json_new(chunkpath,chunk)
    if len(rows)!=expected:
        if start_doc==0 and stop_doc==256:raise ValueError("Incomplete full-model forward; preserve records")
        als.close_cpu_corrections();del model;gc.collect();torch.cuda.empty_cache()
        return chunk
    result=finalize_model(name,time.perf_counter()-started)
    als.close_cpu_corrections();del model;gc.collect();torch.cuda.empty_cache()
    return result


def aggregate():
    protocol=read(PROTOCOL); results={}; all_tests=[]
    for model in MODELS:
        meta=read(f"out/phase50_forward_{slug(model)}.json")
        reused=read(f"out/phase50_reused_{slug(model)}.json")
        records=jsonl(meta["pairs_path"])+jsonl(reused["pairs_path"])
        if sha256_file(meta["pairs_path"])!=meta["pairs_sha256"] or sha256_file(reused["pairs_path"])!=reused["pairs_sha256"]:
            raise ValueError("Forward records changed")
        groups={(arm,k):sorted([r for r in records if r["arm"]==arm and r["K"]==k],key=lambda r:r["document_index"]) for arm in ARMS for k in (8,16)}
        for alias,source in meta["aliases"].items():
            for k in (8,16): groups[alias,k]=groups[source,k]
        model_result={"diagonal_heads":meta["diagonal_heads"],"dtype":meta["dtype"],"K":{}}
        for k in (8,16):
            out={"arms":{},"paired":{}}
            for arm in ARMS:
                group=groups[arm,k]
                if [r["document_index"] for r in group]!=list(range(256)): raise ValueError("All256 paired articles required")
                out["arms"][arm]={"KL":describe([r["kl"] for r in group],range(256)),
                                  "NLL":describe([r["nll"] for r in group],range(256))}
                validation_totals={}; batches=set()
                for row in group:
                    key=(row["batch_start"],row["batch_size"])
                    if key in batches: continue
                    batches.add(key)
                    for key_,value in row["attention_validation_batch"].items():
                        if key_.startswith("max_"): validation_totals[key_]=max(validation_totals.get(key_,0),value)
                        else: validation_totals[key_]=validation_totals.get(key_,0)+value
                out["arms"][arm]["attention_validation"]=validation_totals
                out["arms"][arm]["uniform_completion"]=harness.completion_summary(validation_totals)
                if arm=="svd_K_diag_exact":
                    out["arms"][arm]["validation_scope_note"]="SVD candidate normalization counters include exempt heads before their exact overwrite, following phase36"
                if arm in meta["aliases"]: out["arms"][arm]["exact_alias_of"]=meta["aliases"][arm]
                if group[0].get("ALS"):
                    ds=[r["ALS"] for r in group]
                    out["arms"][arm]["ALS"]={"n_fits":sum(x["n_fits"] for x in ds),"converged":sum(x["converged"] for x in ds),
                                              "CPU_reference_fallback_fits":sum(x.get("CPU_reference_fallback_fits",0) for x in ds),
                                              "discarded_GPU_attempt_sweeps":sum(x.get("discarded_GPU_attempt_sweeps",0) for x in ds),
                                              "fits_with_rejections":sum(x["fits_with_rejections"] for x in ds),
                                              "maximum_absolute_factor":max(x["maximum_absolute_factor"] for x in ds),
                                              "maximum_dynamic_range":max(x["maximum_dynamic_range"] for x in ds),
                                              "maximum_QR_observed_product_error":max(x["maximum_QR_observed_product_error"] for x in ds)}
            for left,right in FORWARD_COMPARISONS:
                out["paired"][left+"__minus__"+right]=paired([x["kl"]-y["kl"] for x,y in zip(groups[left,k],groups[right,k])],range(256))
                all_tests.append(out["paired"][left+"__minus__"+right])
            model_result["K"][str(k)]=out
        results[model]=model_result
    if len(all_tests)!=36: raise ValueError("Forward Holm family incomplete")
    holm(all_tests)
    result={"protocol_sha256":sha256_file(PROTOCOL),"models":results,"Holm_family":36,"n_articles_per_model":256,"n":128}
    write_json_new("out/phase50_forward_summary.json",result)
    return result


if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("action",choices=("reuse","gpu-model","aggregate","finalize-model"))
    ap.add_argument("--model",choices=MODELS); ap.add_argument("--under-gpu-lock",action="store_true")
    ap.add_argument("--start-document",type=int,default=0);ap.add_argument("--stop-document",type=int,default=256)
    args=ap.parse_args()
    if args.action=="reuse":
        for name in MODELS: reuse(name)
    elif args.action=="aggregate": aggregate()
    elif args.action=="finalize-model":finalize_model(args.model)
    else:
        if not args.under_gpu_lock: raise RuntimeError("Launch only under flock /tmp/radon-gpu.lock")
        handoff=Path("out/phase50_handoff_request.json")
        if (handoff.exists() and not Path("out/phase50_handoff_ready.json").exists()
                and not Path("out/phase50_handoff_cancelled.json").exists()):
            request=read(handoff)
            if args.model==request["probe_model"] and args.start_document==0:
                stop=min(args.stop_document,request["probe_stop_document"])
                gpu_model(args.model,0,stop)
                write_json_new("out/phase50_handoff_ready.json",{"intentional_handoff":True,"model":args.model,
                               "completed_probe_documents":stop,"protocol_sha256":sha256_file(PROTOCOL),
                               "scientific_forward_still_requires_all256_articles":True})
                print("INTENTIONAL HANDOFF75: validated forward probe complete; detached coordinator will resume the full256 articles",flush=True)
                raise SystemExit(75)
        gpu_model(args.model,args.start_document,args.stop_document)
