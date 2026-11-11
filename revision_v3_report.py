"""Operational timings and a reviewable report from immutable revision outputs.

No inference, decomposition, bootstrap or hypothesis test runs here.
Run --timings after all GPU jobs, then phase40, then --append-report.
"""
import os
for key in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="4"
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import shlex
import time

LOG=Path("out/_rerun_logs/v3_progress.md")
PY=".venv/Scripts/python.exe"

def read(path):return json.loads(Path(str(path).replace("\\","/")).read_text(encoding="utf-8"))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_new(path,data):
    with Path(path).open("x",encoding="utf-8") as f:json.dump(data,f,indent=2,ensure_ascii=False,allow_nan=False);f.write("\n")

def timings():
    began=time.perf_counter();records=[]
    patterns={"mass":"phase7_massmatched_*_d???_???_v3.json",
        "items8":"phase8_items_*_s*_*_v3.json","items11":"phase11_items_*_s*_*_v3.json",
        "cv":"phase18_posbatch_items_*_s*_*_b*_v3.json"}
    journal=LOG.read_text(encoding="utf-8");observed={}
    for seconds,cmd in re.findall(r"GPU result complete; observed_wait_and_run_seconds=([0-9.]+): ([^\r\n]+)",journal):observed[cmd]=float(seconds)
    for kind,pattern in patterns.items():
        for path in sorted(Path("out").glob(pattern)):
            d=read(path);argv=["flock","/tmp/radon-gpu.lock",PY,"-B"]
            if kind=="mass":argv +=["phase37_mass_matched.py","--model",d["model"],"--start",str(d["start"]),"--stop",str(d["stop"])]
            elif kind.startswith("items"):argv +=["phase38_paired_items.py","--task",d["task"],"--model",d["model"],"--seed",str(d["seed"]),"--variant",d["variant"]]
            else:argv +=["phase45_currentcv_items.py","--model",d["model"],"--seed",str(d["seed"]),"--variant",d["variant"],"--beta",d["arm"]]
            cmd=shlex.join(argv)
            records.append({"kind":"items" if kind.startswith("items") else kind,"result_path":path.as_posix(),
                "command":argv,"display_command":cmd,"reported_worker_seconds":d["elapsed_seconds"],
                "coordinator_observed_wait_and_run_seconds":observed.get(cmd),
                "model":d["model"],"n_raw_records":d["n_raw_records"]})
    assert {k:sum(r["kind"]==k for r in records)for k in ["mass","items","cv"]}=={"mass":96,"items":24,"cv":180}
    cpu=[{"command":cmd,"wall_seconds":float(seconds)}for seconds,cmd in
        re.findall(r"CPU complete; wall_seconds=([0-9.]+): ([^\r\n]+)",journal)]
    data={"gpu_jobs":records,"n_gpu_jobs":len(records),"cpu_commands_observed_so_far":cpu,
        "time_definition":"Worker seconds start inside the function after module imports and flock acquisition; include model setup, validation and writing. Coordinator observations also include queueing from observation start, which can be later than the original queue time for joined pilots.",
        "initial_pilot_queue_observation_may_be_incomplete":True,"no_inference_rerun":True,
        "source_sha256":sha(__file__),"created_utc":datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds":time.perf_counter()-began}
    write_new("out/revision_v3_timings.json",data)
    print(f"Timings: {len(records)} GPU commands, {len(cpu)} CPU observations, {data['elapsed_seconds']:.3f}s",flush=True)

def number(value,digits=3):return "undefined" if value is None else f"{value:.{digits}f}"
def probability(value):return "undefined" if value is None else ("<1e-300" if value==0 else f"{value:.3g}")
def interval(stat,scale=1):
    point=stat["median"];ci=stat["median_ci_document_bootstrap"]
    return number(point*scale) + (f" [{number(ci[0]*scale)}, {number(ci[1]*scale)}]" if ci is not None else " [undefined]") if point is not None else "undefined"
def gain(stat):
    lo,hi=stat["median_seed_gain_ci95_item_bootstrap"]
    return f"{100*stat['median_seed_accuracy_gain']:.3f} [{100*lo:.3f}, {100*hi:.3f}]"
def table(headers,rows):
    return "| "+" | ".join(headers)+" |\n| "+" | ".join("---" for _ in headers)+" |\n"+"".join("| "+" | ".join(str(c) for c in row)+" |\n" for row in rows)+"\n"
def betas(seeds,field):return "/".join(f"{s[field]:g}" for s in seeds)

def append_report(dry_run=False):
    began=time.perf_counter()
    if dry_run:
        # Only an in-memory formatting check; no readiness/completion artifact
        # is created before the scientific audit runs.
        delivery={"inventory":[]}
    else:
        delivery=read("out/revision_v3_delivery.json")
        assert delivery["all_passed"] and delivery["all_required_experiments_complete"]
        assert len(delivery["job_checks"])==300
    timing=read("out/revision_v3_timings.json")
    marker="RELATORIO FINAL DA REVISAO V3"
    existing=LOG.read_text(encoding="utf-8")
    if marker in existing:raise RuntimeError("Final report already appended; no duplicate or overwrite")
    lines=[f"\n\n{marker}\n\n",datetime.now(timezone.utc).isoformat()+"\n\n",
        "FALTA: itens e hashes do gerador historico da familia B da CV. Na identidade GPT-2 s0, A reproduz 214/600, B atual tem 123/600 contra 60/600 salvos. O diagnostico dos lotes originais preservou todas as 2400 predicoes. Comparacao antigo/corrigido nos mesmos itens atuais separada dos resultados antigos salvos.\n\n",
        "Agregacao: mediana de instancias com IC95 por bootstrap de documentos/itens independentes; 2000 repeticoes, semente0. Para acerto binario, mediana da diferenca por item e ganho de acuracia (contagem/n) sao mostrados separadamente; media agrupada e secundaria.\n\n"]
    const=read("out/phase15_constancy_v3.json");rows=[]
    for d in const["datasets"]:
        for stratum,s in d["strata"].items():
            rows.append([d["model"],d["n"],stratum,s["n_heads"],f"{100*s['fraction_of_all_heads']['fraction']:.2f}",
                f"{s['sink_nonconstancy']['n_instances']}/{s['control_column_nonconstancy_median']['n_instances']}",
                interval(s["sink_nonconstancy"]),interval(s["control_column_nonconstancy_median"]),
                interval(s["same_heads_comparison"]["sink_minus_control"]),s["n_zero_energy_control_columns"]])
    lines +=["Constancia estratificada; 64 documentos por modelo/comprimento. Ns/Nc explicita os conjuntos definidos; a diferenca pareada usa a intersecao de cabecas.\n\n",
        table(["modelo","n","estrato","cabecas","%","Ns/Nc","sink IC95","controle IC95","delta pareado IC95","colunas energia0"],rows)]
    named=read("out/phase26_named_v3_ci.json")
    lines +=[f"V3 nomeado: {sum(d['n_instances'] for d in named['datasets'])} matrizes em {len(named['datasets'])} datasets, 15 configuracoes cada; decomposicoes reutilizadas, estimativas pontuais preservadas, ICs de documento adicionados a todos os escalares.\n\n"]
    mass=read("out/phase7_editability_v3.json");rows=[];middle=[]
    for model,d in mass["models"].items():
        for context,c in d["contexts"].items():
            arms=c["arms"];middle.append([model,context,interval(arms["baseline"]["kl_true"]),interval(arms["zerocol_mid"]["kl_true"])])
            for beta,t in c["sink_vs_matched_control"].items():
                tag="beta0" if float(beta)==0 else "beta0.25"
                a,b=arms["sink_"+tag+"_matched"],arms["control_"+tag+"_matched"]
                rows.append([model,context,beta,256,interval(a["kl_true"]),interval(b["kl_true"]),interval(t["summary"]),
                    probability(t["pvalue"]),probability(t["p_holm_24_comparisons"]),number(t["rank_biserial_left_minus_right"])])
    lines +=["KL do ultimo token; todos os 256 artigos em cada braco. Delta = sink menos controle casado. Beta nominal limitado pela massa viavel comum; nao e a remocao completa do teste beta0.\n\n",
        table(["modelo","contexto","beta","artigos","KL sink IC95","KL casado IC95","delta pareado IC95","Wilcoxon p","Holm24 p","r_biserial"],rows),
        "Controle antigo e base preservados:\n\n",table(["modelo","contexto","base IC95","coluna meio IC95"],middle)]
    oldstats=read("out/phase13_stats.json");rows=[];seeds=[]
    for task,label in [("phase8","probe"),("phase11","kv")]:
        data=read(f"out/{task}_items_v3.json")
        entries=[(m,d,False)for m,d in data["models"].items()]
        if task=="phase8":entries.append(("Qwen/Qwen2.5-0.5B BF16 suplementar",data["standard_bf16_supplement"]["Qwen/Qwen2.5-0.5B"],True))
        for model,d,supp in entries:
            a=d["middle"];t=a["combined_seed_stratified_permutation"]
            rows.append([label,model,a["n_independent_items"],number(a["item_difference_describe"]["median"]),gain(a),
                "--" if supp else number(oldstats[label]["models"][model]["gain_pp"]),number(100*a["pooled_accuracy_gain_secondary"]),
                probability(t["pvalue"]),"--" if supp else probability(t["p_holm_7_task_model_comparisons"]),
                probability(t["p_holm_8_including_bf16_supplement_secondary"])])
            for s in a["by_seed"]:
                adj="p_holm_24_including_bf16_supplement_secondary" if supp else "p_holm_21_seed_comparisons"
                seeds.append([label,model,s["seed"],s["n_pairs"],s["edited_only_correct"],s["baseline_only_correct"],probability(s["mcnemar_exact_pvalue"]),probability(s[adj])])
    lines +=["Sonda e KV: janela canonica phase13; ganhos em pontos percentuais. IC de itens dentro de semente x posicao. Familia principal Holm7; familia de precisao Holm8 secundaria, registrada antes da agregacao.\n\n",
        table(["tarefa","modelo","itens","mediana delta item","mediana ganho semente IC95 pp","media antiga pp","media nova secundaria pp","permutacao p","Holm7 p","Holm8 secundario p"],rows),
        "Discordantes e McNemar exato por semente; Holm21 principal, Holm24 para suplemento:\n\n",
        table(["tarefa","modelo","semente","itens","so editado certo","so base certa","McNemar p","p ajustado"],seeds)]
    cv=read("out/phase18_betacv_v3.json");rows=[];gains=[]
    for model,d in cv["models"].items():
        for family,field in [("A","beta_selected_on_A"),("B","beta_selected_on_B")]:
            rows.append([model,family,betas(d["seeds"],"old_"+field),betas(d["seeds"],"legacy_replayed_"+field),betas(d["seeds"],field)])
        for family,h in d["heldout"].items():
            gains.append([model,family,1800,number(100*h["old_median_seed_gain"]),gain(h["legacy_on_same_current_items_gain"]),gain(h["new_gain"])])
    lines +=["CV completa, tres sementes e nove betas; lotes originais por posicao. Selecao em A avaliada em B e vice-versa. A janela da CV preserva mid() antigo baseado na ultima posicao testada. ICs condicionais ao beta escolhido na outra familia.\n\n",
        table(["modelo","familia de selecao","beta salvo s0/s1/s2","beta legado itens atuais","beta corrigido itens atuais"],rows),
        table(["modelo","familia held-out","itens","ganho antigo salvo pp","legado nos itens atuais IC95 pp","corrigido nos itens atuais IC95 pp"],gains)]
    beta0=read("out/phase8_beta0_statistics_v3.json");rows=[]
    for model,d in beta0["models"].items():
        s=d["all_positions"]
        rows.append([model,d["dtype"],3200,f"{d['baseline_n_correct']}/3200",f"{d['legacy_n_correct']}/3200",f"{d['corrected_n_correct']}/3200",gain(s),probability(s["paired_mcnemar"]["p_holm_five_models"])])
    lines +=["Beta0: reteste completo existente, semente0; ICs novos somente em CPU, nenhuma inferencia refeita.\n\n",
        table(["modelo","dtype","itens","base certa","legado beta0 certo","corrigido beta0 certo","ganho IC95 pp","McNemar Holm5 p"],rows),
        "O colapso de acuracia do GPT-2-medium persiste com atencao valida. As verificacoes numericas corrigidas passam; os outros quatro modelos nao apresentam queda global neste teste.\n\n"]
    timingrows=[]
    for kind in ["mass","items","cv"]:
        selected=[r for r in timing["gpu_jobs"]if r["kind"]==kind];values=[r["reported_worker_seconds"]for r in selected]
        timingrows.append([kind,len(values),number(sum(values)),number(min(values)),number(max(values))])
    lines +=["Tempos internos dos jobs, excluindo a fila e as importacoes iniciais; incluem modelo, validacao e gravacao. Tempos observados pelo coordenador incluem a fila e constam no JSON operacional. Nao sao uma alegacao de custo puro de CUDA.\n\n",
        table(["grupo","jobs GPU","soma segundos internos","min","max"],timingrows),
        "Comando e tempo de cada job:\n\n"]
    for r in timing["gpu_jobs"]:lines.append(f"- `{r['display_command']}` — {r['reported_worker_seconds']:.6f}s internos; observacao do coordenador={r['coordinator_observed_wait_and_run_seconds']}; resultado {r['result_path']}\n")
    lines +=["\nSanidades: auditoria final passou nos 300 jobs principais; identidades exatas, mascara e soma de linhas, linha0 preservada, igualdade de massa, pares/IDs/targets, hashes, bootstrap e testes. O braco legado beta0 e deliberadamente invalido e so diagnostico. A reproducao historica de B da CV falhou e permanece registrada, separada da validade numerica.\n\n",
        "Inventario de arquivos, um por linha, com tamanho e SHA256:\n\n"]
    for d in delivery["inventory"]:lines.append(f"- {d['path']} — {d['bytes']} bytes; SHA256 {d['sha256']}\n")
    lines.append(f"\nRelatorio gerado em {time.perf_counter()-began:.6f}s; nenhuma inferencia ou estatistica recalculada.\n")
    if dry_run:
        print(f"Report formatting passed: {sum(map(len,lines))} characters; nothing published or appended",flush=True)
        return
    start_line=existing.count("\n")+3
    with LOG.open("a",encoding="utf-8") as f:f.write("".join(lines))
    print(f"Complete report appended: {LOG.as_posix()}:{start_line}",flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument("--timings",action="store_true");p.add_argument("--append-report",action="store_true");p.add_argument("--check-render",action="store_true")
    args=p.parse_args()
    if args.timings:timings()
    elif args.append_report:append_report()
    elif args.check_render:append_report(dry_run=True)
    else:p.error("Choose --timings or --append-report")

if __name__=="__main__":main()
