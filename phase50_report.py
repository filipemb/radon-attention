"""E9 complete machine-readable tables and a deliberately limited reading."""
import phase50_als
from pathlib import Path
import numpy as np
from phase50_experiment import read, PROTOCOL, ARMS, FORWARD_COMPARISONS
from sampling import MODELS, slug, sha256_file, write_json_new


def render(result):
    labels={"gpt2":"GPT-2","gpt2-medium":"GPT-2-M","EleutherAI/pythia-410m":"Pythia410M",
            "EleutherAI/pythia-1.4b":"Pythia1.4B","Qwen/Qwen2.5-0.5B":"Qwen0.5B","Qwen/Qwen2.5-3B":"Qwen3B"}
    def interval(stats):
        lo,hi=stats["CI95_articles"]
        return f'{stats["median"]:.4g} [{lo:.4g}, {hi:.4g}]'
    parts=["E9 completo: prefixo128,256 artigos por modelo,K8/16; mascaramento e KL/NLL importados de phase2_downstream.",
           "a=svd_K; b=masked_K; c=named_plus_masked; d=named_plus_svd; e=svd_K_diag_exact; f=masked_K_diag_exact.",
           "KL mediana [IC95 por artigos]\n\n| Modelo | K | a | b | c | d | e | f |\n|---|---:|---|---|---|---|---|---|"]
    for row in result["forward_KL_table"]:
        parts[-1]+="\n| "+" | ".join([labels[row["model"]],str(row["K"])]+[interval(row["arms"][a]) for a in ARMS])+" |"
    tests={(r["model"],r["K"],r["left"],r["right"]):r for r in result["forward_paired_tests"]}
    parts.append("Wilcoxon pareado sobre256 artigos; p de Holm na familia36 e rank-biserial. Efeito positivo favorece o braco da direita.\n\n| Modelo | K | b-d: pH; rb | c-d: pH; rb | c-b: pH; rb |\n|---|---:|---|---|---|")
    for row in result["forward_KL_table"]:
        cells=[labels[row["model"]],str(row["K"])]
        for left,right in FORWARD_COMPARISONS:
            t=tests[row["model"],row["K"],left,right];cells.append(f'{t["p_Holm"]:.3g}; {t["rank_biserial"]:+.4f}')
        parts[-1]+="\n| "+" | ".join(cells)+" |"
    parts.append("Matriz: Frobenius relativo / TV media por linha, apos normalizacao causal;384 matrizes por modelo,64 documentos. ICs e todos os testes estao nos JSONs.\n\n| Modelo | K | a | b | c | d |\n|---|---:|---|---|---|---|")
    for row in result["matrix_table"]:
        cells=[labels[row["model"]],str(row["K"])]+[f'{row["arms"][a]["frobenius_median"]:.5f}/{row["arms"][a]["TV_median"]:.5f}' for a in ARMS[:4]]
        parts[-1]+="\n| "+" | ".join(cells)+" |"
    parts.append("Cabecas quase diagonais, indices de camada/cabeca com inicio em zero:\n\n"+"\n".join(
        f'- {labels[m]}: '+(", ".join(f"({l},{h})" for l,h in result["quasi_diagonal_heads"][m]) or "nenhuma") for m in MODELS))
    parts.append("Checagem float64 em32 matrizes/modelo,128 ajustes: GPU original e estimador devolvido apos a recomputacao CPU sao mostrados separadamente.\n\n| Modelo | Max. diferenca GPU original | Max. diferenca final | Recomputados CPU /128 |\n|---|---:|---:|---:|")
    for model in MODELS:
        v=result["numerics_and_convergence"][model]
        parts[-1]+=f'\n| {labels[model]} | {v["uncorrected_GPU_max_error_difference"]:.4g} | {v["final_estimator_validation"]["max_raw_error_difference"]:.4g} | {v["CPU_reference_recomputed_validation_fits"]} |'
    parts.extend(result["honest_reading"])
    parts.append("Decisoes, certeza e execucao:\n\n"+"\n".join(f'- {d["decision"]}: certeza {d["certainty"]}; executou={d["executed"]}.' for d in result["decisions"]))
    return "\n\n".join(parts)


def main():
    protocol=read(PROTOCOL); forward=read("out/phase50_forward_summary.json"); matrix=read("out/phase50_matrix_summary.json")
    ph=sha256_file(PROTOCOL)
    if forward["protocol_sha256"]!=ph or matrix["protocol_sha256"]!=ph:
        raise ValueError("Report/protocol mismatch")
    ft=[]; mt=[]; tests=[]; nums={}; comparisons={}
    for left,right in FORWARD_COMPARISONS:
        comparisons[left+"__minus__"+right]={"left_lower_median":0,"right_lower_median":0,"significant_left":0,"significant_right":0}
    for model in MODELS:
        validation=read(f"out/phase50_estimator_validation_{slug(model)}.json")
        sanity=read(f"out/phase50_forward_sanity_{slug(model)}.json")
        nums[model]={"final_estimator_validation":{"n_matrices":validation["n_matrices"],"n_fits":validation["n_fits"],
                                        "max_raw_error_difference":validation["max_raw_error_difference"],
                                        "max_normalized_frobenius_difference":validation["max_normalized_frobenius_difference"],
                                        "max_TV_difference":validation["max_TV_difference"],"passed":validation["passed"]},
                     "uncorrected_GPU_max_error_difference":validation["max_uncorrected_GPU_CPU_error_difference"],
                     "uncorrected_GPU_passed":validation["uncorrected_GPU_passed"],
                     "CPU_reference_recomputed_validation_fits":validation["CPU_reference_recomputed_fits"],
                     "identity_KL_exactly_zero":sanity["identity_KL_exactly_zero"],"baseline_rerun_checks":sanity["baseline_checks"],"K":{}}
        for k in (8,16):
            fw=forward["models"][model]["K"][str(k)]; mm=matrix["models"][model]["K"][str(k)]
            ft.append({"model":model,"K":k,"arms":{a:{"median":fw["arms"][a]["KL"]["median"],
                                                           "CI95_articles":fw["arms"][a]["KL"]["median_ci_document_bootstrap"]} for a in ARMS}})
            mt.append({"model":model,"K":k,"n_matrices":384,"n_documents":64,
                       "arms":{a:{"frobenius_median":mm["arms"][a]["frobenius"]["median"],
                                   "frobenius_CI95_documents":mm["arms"][a]["frobenius"]["median_ci_document_bootstrap"],
                                   "TV_median":mm["arms"][a]["TV"]["median"],
                                   "TV_CI95_documents":mm["arms"][a]["TV"]["median_ci_document_bootstrap"]} for a in ARMS[:4]}})
            for left,right in FORWARD_COMPARISONS:
                label=left+"__minus__"+right; test=fw["paired"][label]
                tests.append({"model":model,"K":k,"left":left,"right":right,**test})
                bucket=comparisons[label]
                l=fw["arms"][left]["KL"]["median"]; r=fw["arms"][right]["KL"]["median"]
                bucket["left_lower_median"]+=int(l<r); bucket["right_lower_median"]+=int(r<l)
                bucket["significant_left"]+=int(test["p_Holm"]<.05 and test["rank_biserial"]<0)
                bucket["significant_right"]+=int(test["p_Holm"]<.05 and test["rank_biserial"]>0)
            nums[model]["K"][str(k)]={"matrix":{a:mm["arms"][a]["ALS"] for a in ("masked_K","named_plus_masked")},
                                        "forward":{a:fw["arms"][a].get("ALS") for a in ("masked_K","named_plus_masked","masked_K_diag_exact")}}
    result={"experiment":"E9","status":"all_results_available","protocol_path":PROTOCOL.as_posix(),"protocol_sha256":ph,
            "GPU_solver_decision":read("out/phase50_gpu_solver.json"),
            "numerical_fallback_policy":read("out/phase50_numerical_fallback.json"),
            "forward_KL_table":ft,"forward_paired_tests":tests,"forward_comparison_counts_out_of12":comparisons,
            "matrix_table":mt,"matrix_paired_tests_path":"out/phase50_matrix_summary.json",
            "quasi_diagonal_heads":{m:protocol["datasets"][m]["diagonal_heads"] for m in MODELS},
            "numerics_and_convergence":nums,"planted_controls":read("out/phase50_CPU_controls.json"),
            "interpretation_limits":[
                "O contraste principal se refere aos estimadores efetivamente ajustados em200 varreduras ALS; nao prova optimalidade global no conjunto de matrizes de postoK sob a mascara.",
                "QR controla a representacao dos fatores, mas nao fornece limite para a norma da completacao nao observada; rejeicoes e falta de convergencia devem acompanhar qualquer conclusao comportamental.",
                "Os bracos e/f sao ablacoes com exatamente as mesmas cabecas preservadas; essas cabecas exatas tem armazenamento adicional e nao sustentam uma alegacao global de compressao no mesmo cap.",
                "Os intervalos e testes usam artigos como unidades independentes; as matrizes possuem seis instancias por documento em64 documentos, e o forward usa os256 artigos fixos.",
                "As cabecas isentas foram selecionadas antes dos ajustes usando todas as amostras, com limiar0.9 e offsets0/1; nao foram escolhidas por KL."],
            "decisions":[
                {"decision":"200 fixed ALS sweeps; no early stop or post-result change","certainty":"alta","executed":True},
                {"decision":"float64 CPU and GPU, QR plus small SVD gauge every sweep","certainty":"alta","executed":True},
                {"decision":"384 matrices/model, fixed document/layer stratification, all256 forward articles","certainty":"alta","executed":True},
                {"decision":"reuse V1 SVD and E4 named+SVD values exactly; verify provenance and first GPU batch","certainty":"alta","executed":True},
                {"decision":"Holm36 for forward and Holm144 for matrix paired tests","certainty":"alta","executed":True},
                {"decision":"independent GPU-vs-CPU double comparison on32 matrices/model, both ranks and targets","certainty":"alta","executed":True},
                {"decision":"preserve the uncorrected GPU failure; recompute finite QR-product preservation failures with the CPU float64 reference from the original SVD for200 sweeps; report the resulting estimator and raw GPU separately","certainty":"alta","executed":True},
                {"decision":"no claim that finite-sweep nonconvex ALS finds the best possible causal low-rank model","certainty":"alta","executed":True}],
            "source_summary_files":{"forward":"out/phase50_forward_summary.json","matrix":"out/phase50_matrix_summary.json"}}
    reading=[]
    for left,right in FORWARD_COMPARISONS:
        c=comparisons[left+"__minus__"+right]
        reading.append(f'{left} teve KL mediana menor que {right} em {c["left_lower_median"]}/12 combinacoes; o sentido oposto ocorreu em {c["right_lower_median"]}/12. Nos testes pareados com Holm, {c["significant_left"]}/12 favorecem o primeiro e {c["significant_right"]}/12 favorecem o segundo.')
    reading.append("Esses contrastes avaliam o ajustador declarado de200 varreduras, incluindo a recomputacao CPU float64 quando o QR perde fidelidade numerica. A falha da GPU original foi preservada. A estatistica por artigos nao representa incerteza sobre todos os otimos locais ou sobre toda a classe de completacoes causais de postoK.")
    reading.append("Na matriz, os dois canais nomeados perderam para masked_K nas medianas dos12 cenarios deste protocolo. O resultado comportamental deve ser lido junto da ablacao com cabecas exatas, da convergencia e das magnitudes dos fatores; esses controles delimitam a explicacao do efeito do S+L.")
    cpu_infos=[x for m in nums.values() for k in m["K"].values() for x in k["matrix"].values()]
    fw_infos=[x for model in MODELS for k in forward["models"][model]["K"].values() for arm,v in k["arms"].items()
              if (x:=v.get("ALS")) is not None and not v.get("exact_alias_of")]
    reading.append(f'Convergencia matricial: {sum(x["converged"] for x in cpu_infos)}/{sum(x["n_fits"] for x in cpu_infos)} ajustes atendem ao criterio; maior fator absoluto {max(x["maximum_absolute_factor"] for x in cpu_infos):.6g}; maior razao maximo/minimo nao nulo {max(x["maximum_dynamic_range"] for x in cpu_infos):.6g}. No forward: {sum(x["converged"] for x in fw_infos)}/{sum(x["n_fits"] for x in fw_infos)}, maior fator {max(x["maximum_absolute_factor"] for x in fw_infos):.6g}; {sum(x.get("CPU_reference_fallback_fits",0) for x in fw_infos)} ajustes recomputados na CPU. Esses numeros nao equivalem a uma garantia de otimo global.')
    result["honest_reading"]=reading
    result["rendered_tables_markdown"]=render(result)
    write_json_new("out/phase50_report.json",result)
    print("E9 complete: out/phase50_report.json",flush=True)
    from phase50_audit import main as audit
    audit()
    write_json_new("out/phase50_complete.json",{"status":"complete","protocol_sha256":ph,
                                               "report_path":"out/phase50_report.json","report_sha256":sha256_file("out/phase50_report.json"),
                                               "integrity_audit_path":"out/phase50_integrity_audit.json",
                                               "integrity_audit_sha256":sha256_file("out/phase50_integrity_audit.json")})
    print(result["rendered_tables_markdown"],flush=True)


if __name__=="__main__": main()
