"""Check the original CV position-boundary batches without changing its items."""
from revision_v3_probes import load_probe,sha256_file,write_json_new,progress
from phase2_downstream import DeferredStats
import revision_v3_probes as probes
import json
from pathlib import Path
import time

@probes.torch.inference_mode()
def main():
    began=time.perf_counter();model_name="gpt2";seed=0
    arrays,manifest=load_probe("phase18",model_name,seed)
    old=json.loads(Path(manifest["historical_source"]).read_text(encoding="utf-8"))[model_name]
    first=json.loads(Path("out/phase18_items_gpt2_s0_historical_b1.0_v3.json").read_text(encoding="utf-8"))
    previous=[json.loads(s) for s in Path(first["pairs_path"]).read_text(encoding="utf-8").splitlines()]
    model=probes.AutoModelForCausalLM.from_pretrained(model_name,revision=manifest["revision"],
        dtype=probes.torch.float32,attn_implementation="eager",local_files_only=True).to("cuda").eval()
    probes.AttentionInterface.register("revision_v3_cv_batchcheck",probes.p8.recon_attention_forward)
    model.set_attn_implementation("revision_v3_cv_batchcheck")
    results={};raw=[]
    for family in ["A","B"]:
        ids,targets,positions=[arrays[k+"_"+family] for k in ["input_ids","targets","positions"]]
        npp=manifest["n_per_position"];positions_grid=manifest["positions_"+family]
        for block,position in enumerate(positions_grid):
            lo,hi=block*npp,(block+1)*npp
            assert all(positions[lo:hi]==position)
            for start in range(lo,hi,8):
                stop=min(start+8,hi);stats=DeferredStats()
                probes.p8.RECON.update(beta=1.,stats=stats)
                output=model(probes.torch.tensor(ids[start:stop],device="cuda"))
                pred=output.logits[:,-1,:].argmax(-1).cpu().tolist();del output
                stats.finalize("Original CV position-boundary diagnostic")
                raw.extend({"family":family,"position":position,"trial_id":i,"target_id":int(targets[i]),
                    "prediction_id":pred[j],"correct":pred[j]==int(targets[i]),"batch_start":start,"batch_size":stop-start}
                    for j,i in enumerate(range(start,stop)))
        selected=[r for r in raw if r["family"]==family]
        acc={p:sum(r["correct"] for r in selected if r["position"]==p)/npp for p in positions_grid}
        rate=probes.p18.mid(acc,positions_grid)
        pmap={r["trial_id"]:r for r in previous if r["family"]==family}
        results[family]={"old_mid_accuracy":old["mid"+family]["1.0"],"current_position_batched_mid_accuracy":rate,
            "old_counts_reproduced":abs(rate-old["mid"+family]["1.0"])<1e-15,
            "n_prediction_differences_from_flat_batches":sum(r["prediction_id"]!=pmap[r["trial_id"]]["prediction_id"] for r in selected),
            "accuracy_by_position":acc}
    result={"results":results,"records":raw,"batch":8,"reset_batches_at_each_position":True,
        "n_records":len(raw),"all_attention_sanities_passed":True,"source_sha256":sha256_file(__file__),
        "input_payload_sha256":manifest["payload_sha256"],"elapsed_seconds":time.perf_counter()-began}
    write_json_new("out/phase18_batch_diagnostic_v3.json",result)
    progress("V3 CV original batch diagnostic",str(results),result["elapsed_seconds"],
        "flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase43_cv_batch_diagnostic.py")
    print(json.dumps(results),flush=True)

if __name__=="__main__":main()
