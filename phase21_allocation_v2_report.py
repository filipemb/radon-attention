"""Render the requested E4 v2 numerical tables from immutable aggregate JSON."""
import argparse
import json
from pathlib import Path

MODELS=("gpt2","gpt2-medium","EleutherAI/pythia-410m","EleutherAI/pythia-1.4b","Qwen/Qwen2.5-0.5B","Qwen/Qwen2.5-3B")
METHODS=("named_first","lowrank_first","algorithm_1_5_iterations")


def cell(s,digits=4,secondary=True):
    lo,hi=s["median_ci_document_bootstrap"]
    text=f"{s['median']:.{digits}f} [{lo:.{digits}f}; {hi:.{digits}f}]"
    if secondary:text+=f" / {s['secondary_document_means']['mean']:.{digits}f}"
    return text


def table(lines,headers,rows):
    lines.append("| "+" | ".join(headers)+" |")
    lines.append("| "+" | ".join("---" for _ in headers)+" |")
    lines.extend("| "+" | ".join(str(c) for c in row)+" |" for row in rows)
    lines.append("")


def render(source,destination):
    source=Path(source);destination=Path(destination)
    if not destination.name.startswith("phase21_allocation_v2") or destination.suffix!=".md":
        raise ValueError("Use a new phase21_allocation_v2*.md report")
    data=json.loads(source.read_text(encoding="utf-8"))
    config=data["_meta"]
    lines=["**E4 v2 — alocação, teto de parâmetros e resíduo**","",
           f"Fonte imutável: `{source.as_posix()}`. Estado: `{data['status']}`.","",
           "As células estatísticas têm mediana sobre instâncias [IC 95% por documentos] / média das médias documentais, secundária. Os ICs vêm da função importada `phase24_p0_metrics.describe`, com 2000 reamostragens de documentos inteiros, seed 0. Cada população matricial contém 64 documentos; todas as instâncias do manifesto são mantidas.","",
           "Dicionário nomeado literal de `phase5_msclean.build_dict`, também usado em phase6: 17 átomos, sem alterações. NNLS no QR econômico, float64, limite 100×número de átomos e verificação KKT. A projeção matricial no cone finitamente gerado é única; os coeficientes são únicos se o dicionário tiver posto de colunas completo, como neste dicionário. O truncamento SVD tem garantia de unicidade quando há separação estrita no corte; os empates são contados no JSON.","",
           "**Energia nomeada no painel de alocação auditado: rank residual r=8**","",
           "Energia significa ||S||²/||A||². Este painel mantém o rank residual auditado; ele não é a comparação de capacidade K=8, que usa q=7.",""]
    headers=["n","Modelo","named_first","lowrank_first","5 iterações do Algoritmo 1"]
    table(lines,headers,[(n,m,*[cell(data['matrices'][m][str(n)]['allocation'][a]['8']['metrics']['named_energy_ratio']) for a in METHODS])
                         for n in (128,256) for m in MODELS])
    common=data.get("allocation_at_common_K8_q7_supplement",{})
    if all(str(n) in common.get(m,{}) for n in (128,256) for m in MODELS):
        lines.extend(["**Energia nomeada também sob o teto K=8: rank residual q=7 para as três convenções**",""])
        table(lines,headers,[(n,m,*[cell(common[m][str(n)]['conventions'][a]['metrics']['named_energy_ratio']) for a in METHODS])
                             for n in (128,256) for m in MODELS])
        counts={n:sum(common[m][str(n)]['conventions'][METHODS[2]]['criterion_met_by_5'] for m in MODELS) for n in (128,256)}
        lines.append(f"O critério de parada foi atingido em {counts[128]}/9984 instâncias no suplemento q=7, n=128, e {counts[256]}/9984 em n=256. São diagnósticos separados do registro auditado 17/9984 em n=128, rank residual r=8.")
        lines.append("")
    lines.extend(["ALT significa exatamente cinco iterações do Algoritmo 1, começando com L=0, sem parada antecipada; critério registrado: mudança relativa do objetivo <=1e-7. No painel auditado n=128, r=8, 17/9984 atingiram esse critério. Isso não demonstra convergência geral nem ótimo global.","",
                  "**Capacidade K=8: S+L7, SVD8 e linhas sob o mesmo teto**","",
                  "B=K(2n+1). S+L usa q=K-1 fixo e custa 2·count(c>0)+q(2n+1), verificando o teto em toda instância; sobra B−custo registrada. SVD usa K(2n+1). Linhas selecionam min(floor(B/2),2n+7) átomos do dicionário de `omp_profiled`, com custo 2 por átomo selecionado, incluindo coeficientes que o NNLS zera. Para K=8, B=2056/4104 em n=128/256; o dicionário de linhas esgota em 263/519 átomos e deixa sobra 1530/3066. O teto permitido é comum; o consumo efetivo e a saturação são explícitos.","",
                  "Estado do protocolo de linhas: "+json.dumps(data["line_protocol_choice"],ensure_ascii=False,separators=(",",":")),"",
                  "Quando o dicionário completo cabe, os valores de linhas são a solução NNLS terminal do OMP completo, calculada diretamente no mesmo cone. O `omp_profiled` original não foi editado. Os dois controles fixos executaram todo o OMP original: n=128 e 256, com diferença de erro zero frente ao endpoint. Todas as projeções terminais têm certificado KKT. A trajetória OMP não foi executada em todas as instâncias; a equivalência para a métrica terminal, a decisão de implementação e os controles aparecem explicitamente no JSON. Nenhuma resposta ou aprovação do usuário é presumida.",""])
    table(lines,["n","Modelo","erro S+L7","erro SVD8","erro linhas"],
          [(n,m,*[cell(data['matrices'][m][str(n)]['capacity']['8']['metrics'][k]) for k in ('named_first_error','svd_error','line_error')])
           for n in (128,256) for m in MODELS])
    lines.extend(["Diferença = erro do método − erro SVD; sinais positivos e rank-biserial positivo favorecem SVD. O Wilcoxon usa as 64 medianas documentais das diferenças pareadas, bilateral, zeros removidos pelo método wilcox e aproximação assintótica. Os p são não ajustados. O IC da diferença mediana usa as diferenças de todas as instâncias e o mesmo bootstrap de documentos; é um estimando diferente da mediana das 64 medianas. Fração SVD = vitória estrita em instâncias cabeça×documento / fração de cabeças distintas após mediana sobre documentos, secundária.",""])
    for comparison,title in (("named_minus_SVD","S+L7 versus SVD8"),("lines_minus_SVD","linhas versus SVD8"),("named_minus_lines","S+L7 versus linhas")):
        lines.extend(["**"+title+"**",""])
        rows=[]
        for n in (128,256):
            for m in MODELS:
                p=data['matrices'][m][str(n)]['capacity']['8']['comparisons'][comparison]
                rows.append((n,m,cell(p['paired_instance_difference'],digits=5),f"{p['wilcoxon']['p_two_sided']:.5g}",
                             f"{p['wilcoxon']['rank_biserial']:+.4f}",
                             f"{100*p['right_arm_win_fraction_instances']:.2f}% / {100*p['distinct_head_secondary']['right_arm_win_fraction']:.2f}%"))
        table(lines,["n","Modelo","diferença pareada","p Wilcoxon","rank-biserial","vitórias do braço direito: instâncias / cabeças"],rows)
    lines.extend(["r=0 consta somente como descrição do canal nomeado. Não há comparação contra SVD de rank zero. `named_channel_only_error` representa ||A−S||/||A||, com custo próprio 2·átomos ativos; não é um braço com orçamento igual à SVD.","",
                  "**Comparação secundária por rank, separada do teto comum**",""])
    rank_panels=data.get('secondary_rank_matched_comparisons',{})
    if all(str(n) in rank_panels.get(m,{}) for n in (128,256) for m in MODELS):
        rows=[]
        for n in (128,256):
            for m in MODELS:
                p=rank_panels[m][str(n)]['named_first_common_K8_q7'];s=p['metrics'];test=p['paired_method_minus_r_plus_atoms_SVD']
                rows.append((n,m,*[f"{s[key]['median']:.5f}" for key in ('method_error','svd_same_r_error','svd_r_plus_atoms_error')],
                             f"{s['svd_r_plus_atoms_rank']['median']:.0f}",
                             f"{s['method_parameters']['median']:.0f} / {s['svd_r_plus_atoms_parameters']['median']:.0f}",
                             f"{test['wilcoxon']['p_two_sided']:.5g}",f"{test['wilcoxon']['rank_biserial']:+.4f}"))
        table(lines,['n','Modelo','erro S+L7','erro SVD7','erro SVD(7+m)','rank 7+m mediano','parâmetros método / SVD(7+m)','p pareado','rank-biserial'],rows)
        lines.extend(['Aqui m é o número de átomos nomeados ativos, por instância. Este painel usa orçamentos diferentes explicitamente e não substitui a comparação principal. Os JSONs secundários também contêm todas as três convenções em cada rank residual positivo original, com ICs e testes por documento.',''])
    lines.extend(["**Resíduo sob o teto K=8, q=7, named_first**",""])
    rows=[]
    for n in (128,256):
        for m in MODELS:
            p=data['principal_symmetric_residuals_K8_q7'][m][str(n)]['metrics']
            rows.append((n,m,*[f"{p[a]['effective_rank']['median']:.2f}" for a in ('R','E')],
                         *[f"{100*p[a]['first4_columns_fraction_of_residual']['median']:.2f}%" for a in ('R','E')],
                         f"{100*p['E']['distance_fraction_of_residual'][0]['median']:.2f}%"))
    table(lines,["n","Modelo","posto efetivo R","posto efetivo E","primeiras 4 colunas R","primeiras 4 colunas E","energia futura E"],rows)
    lines.extend(["R=A−S e E=A−S−L7. Posto efetivo = exp(entropia de Shannon dos sigma² normalizados). Frações espaciais têm como denominador a energia do próprio resíduo; também há valores normalizados por ||A||² no JSON. Faixas de i−j: <0, 0, 1, 2–3, 4–7, 8–15, 16–31, 32–63, 64–127, >=128. Espectros completos e ICs por posição singular estão nos resultados. O resíduo final é assinado e tem cauda mais difusa; estes números não demonstram que seja ruído nem semanticamente irrelevante.","",
                  "**KL do último token e regra de linha vazia**",""])
    forward=data['forward']
    if 'models' in forward:
        rows=[];counts=[]
        for n in (128,256):
            for m in MODELS:
                for K in (8,16):
                    b=forward['models'][m][str(n)]['budgets'][str(K)]
                    rows.append((n,m,K,cell(b['named_first_KL'],digits=6),cell(b['SVD_KL'],digits=6),
                                 cell(b['paired_KL_named_minus_SVD'],digits=6)))
                    for mode,c in b['uniform_causal_completion_by_mode'].items():
                        counts.append((n,m,K,mode,c['rows_completed'],c['rows_total'],c['last_query_rows_completed'],c['last_query_rows_total']))
        table(lines,["n","Modelo","K","KL S+L(K−1)","KL SVD(K)","diferença KL pareada"],rows)
        lines.extend(["Conclusão uniforme causal por modo, contada uma única vez por linha, incluindo todas as camadas/cabeças e a última consulta separadamente:",""])
        table(lines,["n","Modelo","K","modo","linhas completadas","linhas totais","últimas completadas","últimas totais"],counts)
    else:
        lines.append(f"FALTA: injeção e KL do último token; estado `{forward.get('status')}`. Arquivo exigido `{forward.get('required_path')}`; início {config['waiting_for_V1_started_UTC']}, prazo {config['waiting_for_V1_deadline_UTC']}. Nenhuma KL ou contagem de conclusão do modelo foi imputada. Adaptador e controles CPU estão preparados; nenhum resultado CPU é apresentado como comportamento do modelo.")
        lines.append("")
    for K,status in data.get('line_low_budget_status',{}).items():
        if status.startswith('FALTA'):lines.extend([f"FALTA: linhas no teto K={K}: {status.removeprefix('FALTA: ')}. Comparações S+L(K−1) versus SVD(K) e todos os ranks de alocação permanecem disponíveis.",""])
    lines.extend(["**Leitura dos resultados**","",
                  "A ordem de alocação muda fortemente a energia atribuída ao canal nomeado. A projeção named_first define uma convenção reproduzível, mas não identifica uma única separação intrínseca S/L. A vantagem matricial de S+L7 nas medianas não implica vitória em toda cabeça nem preservação do comportamento; esta última exige a injeção concluída. O método de linhas satura seu dicionário antes de gastar o teto de K=8; sua comparação deve ser lida com a sobra registrada.",""])
    broader=data.get('named_first_vs_SVD_all_positive_budgets',{})
    if broader:
        c=broader['EleutherAI/pythia-1.4b']['128']['16'];m=c['metrics'];p=c['named_minus_svd']
        lines.extend([f"A vantagem no teto K=8 não se estende uniformemente aos demais tetos, todos preservados no JSON. Por exemplo, Pythia-1.4b em n=128, K=16: erro mediano S+L15={m['named_first_error']['median']:.6f}, SVD16={m['svd_error']['median']:.6f}; diferença pareada mediana {cell(p['paired_instance_difference'],digits=6)}, p={p['wilcoxon']['p_two_sided']:.5g}, rank-biserial={p['wilcoxon']['rank_biserial']:+.4f}, favorecendo SVD. Os ICs da mediana pareada e o teste das medianas documentais têm estimandos diferentes; concordância entre eles não é presumida.",""])
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('x',encoding='utf-8') as out:out.write('\n'.join(lines)+'\n')
    print(destination.as_posix(),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    render(args.input,args.output)
