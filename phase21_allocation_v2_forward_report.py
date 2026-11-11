"""Render the completed last-token E4 forward experiment without changing JSON."""
import json
from pathlib import Path

SOURCE=Path('out/phase21_allocation_v2_forward.json')
TARGET=Path('out/_rerun_logs/phase21_allocation_v2_forward_results.md')


def statistic(s):
    lo,hi=s['median_ci_document_bootstrap']
    return f"{s['median']:.5f} [{lo:.5f}; {hi:.5f}]"


def completed(c,last=False):
    a,b=('last_query_rows_completed','last_query_rows_total') if last else ('rows_completed','rows_total')
    return f"{c[a]} ({100*c[a]/c[b]:.6g}%)"


def table(lines,columns,rows):
    lines.append('| '+' | '.join(columns)+' |')
    lines.append('| '+' | '.join('---' for _ in columns)+' |')
    lines.extend('| '+' | '.join(str(v) for v in row)+' |' for row in rows)
    lines.append('')


def main():
    data=json.loads(SOURCE.read_text(encoding='utf-8'))
    if data['status']!='complete' or len(data['models'])!=6:raise ValueError('Wait for all six complete models')
    meta=data['_meta']
    if meta['protected_matrix_aggregate_sha256']!=meta['matrix_aggregate_sha256_after']:
        raise ValueError('Historical matrix aggregate changed')
    lines=['**E4 v2 — injeção no último token**','',
           'Prefixo de 128 tokens, mesmos 256 artigos, offsets, alvos, lote 2 e dtype por modelo do V1. Todas as camadas/cabeças são reconstruídas. KL = KL(distribuição nativa || distribuição injetada), em nats. O alvo e o sufixo são fisicamente excluídos pelo `last_logits` importado.','',
           'S+L usa named_first, NNLS float64 no dicionário inalterado de 17 átomos, seguido de SVD completa float32 do resíduo, rank K−1. Custo 2·átomos ativos +(K−1)(2n+1) <= K(2n+1), verificado por cabeça/camada. Remáscara, clamp, renormalização e preenchimento uniforme causal vêm integralmente do harness importado.','',
           'SVD8/SVD16 e referências uniforme/diagonal/sink são reutilizados dos pares imutáveis do V1, reagrupados com a função importada `phase24_p0_metrics.describe`. A execução nova confere a NLL nativa por artigo e a identidade exata em todos os lotes. GPU sob flock, um processo por modelo; o lock é liberado antes do resumo CPU e do modelo seguinte.','',
           'Estatística principal: mediana [IC95% de 2000 reamostragens de artigos inteiros], seed 0. Cada artigo contribui uma observação. Médias, IQRs e NLLs são secundários e constam no JSON. Teste pareado: Wilcoxon bilateral sobre as 256 diferenças por artigo, zero_method=wilcox, aproximação assintótica; p não ajustado. Rank-biserial positivo favorece SVD.','']
    rows=[];counts=[];means=[];deltas=[];references=[];denominators=[]
    for model,pop in data['models'].items():
        result=pop['128']
        if not result['identity_exact_in_every_batch']:raise ValueError('Identity sanity failed')
        for K in ('8','16'):
            b=result['budgets'][K];p=b['paired_KL_named_minus_SVD'];w=p['wilcoxon']
            if w['n_articles']!=256:raise ValueError('Wrong Wilcoxon sample size')
            rows.append((model,K,statistic(b['named_first_KL']),statistic(b['SVD_KL']),statistic(p),
                         f"{w['p_two_sided']:.6g}",f"{w['rank_biserial']:+.5f}"))
            deltas.append(p['median'])
            c=b['uniform_causal_completion_by_mode']
            counts.append((model,K,completed(c['named']),completed(c['named'],True),completed(c['svd']),completed(c['svd'],True)))
            means.append((model,K,f"{b['named_first_KL']['secondary_document_means']['mean']:.6f}",
                          f"{b['SVD_KL']['secondary_document_means']['mean']:.6f}",
                          f"{p['secondary_document_means']['mean']:+.6f}",
                          f"{100*w['fraction_articles_SVD_has_lower_KL']:.3f}%"))
        r=result['V1_scale_references']
        references.append((model,*[statistic(r[a]['KL']) for a in ('uniform','diagonal','sink')]))
        c=result['budgets']['8']['uniform_causal_completion_by_mode']['named']
        denominators.append((model,c['rows_total'],c['last_query_rows_total']))
    table(lines,['Modelo','K','KL S+L(K−1)','KL SVD(K)','diferença pareada S+L−SVD','p Wilcoxon (256 artigos)','rank-biserial'],rows)
    lines.extend(['**Linhas que receberam preenchimento uniforme causal**','',
                  'Cada célula é contagem (fração). Todas = todas as consultas × cabeças × camadas × artigos. Última = última consulta × cabeças × camadas × artigos. Os contadores de lote foram somados uma vez por lote, sem duplicá-los para cada artigo.',''])
    table(lines,['Modelo','K','S+L todas','S+L última','SVD todas','SVD última'],counts)
    table(lines,['Modelo','denominador: todas as linhas por braço/K','denominador: última consulta por braço/K'],denominators)
    lines.extend(['**Referências de escala do V1, sobre os mesmos artigos**',''])
    table(lines,['Modelo','uniforme causal','só diagonal','só sink'],references)
    lines.extend(['**Estatísticas secundárias**',''])
    table(lines,['Modelo','K','média KL S+L','média KL SVD','média da diferença','artigos com KL SVD menor'],means)
    lines.extend([f"A mediana das diferenças pareadas favorece S+L em {sum(v<0 for v in deltas)}/12 combinações modelo×K. A escala das KLs e as referências são necessárias para avaliar a magnitude: ganho relativo frente a SVD não demonstra preservação exata do modelo.",'',
                  '**Decisões**',''])
    table(lines,['Pergunta','Decisão','Certeza','Executou?'],[
        ('Qual ponto de avaliação?','Mesmo V1: n128, últimos logits, 256 artigos e mesmos alvos/offsets/lote/dtype.','alta','sim'),
        ('Como casar orçamento?','S+L(K−1) dentro de K(2n+1), K8/16, custos/sobras registrados por artigo.','alta','sim'),
        ('Como tratar causalidade e linhas vazias?','Importar o harness corrigido sem copiar/alterar sua lógica; uniforme causal.','alta','sim'),
        ('É preciso recalcular SVD e referências?','Reutilizar os pares V1 completos, com proveniência e NLL nativa verificadas.','alta','sim, reutilizados'),
        ('Qual unidade de inferência?','Um par por artigo, Wilcoxon sobre 256 diferenças, rank-biserial e bootstrap de artigos.','alta','sim'),
        ('Como compartilhar GPU?','Um processo sob flock por modelo; resumos CPU fora do lock.','alta','sim')])
    lines.extend([f"Fonte: `{SOURCE.as_posix()}`. Corpus SHA256: `{meta['corpus_manifest_sha256']}`. Agregado matricial preservado: `{meta['matrix_aggregate_sha256_after']}`.",''])
    with TARGET.open('x',encoding='utf-8') as out:out.write('\n'.join(lines))
    print(TARGET.as_posix(),flush=True)


if __name__=='__main__':main()
