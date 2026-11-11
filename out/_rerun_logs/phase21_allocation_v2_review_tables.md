**E4 v2 — alocação, teto de parâmetros e resíduo**

Fonte imutável: `out/phase21_allocation_v2_review.json`. Estado: `review_exact_full_dictionary_endpoint_candidates`.

As células estatísticas têm mediana sobre instâncias [IC 95% por documentos] / média das médias documentais, secundária. Os ICs vêm da função importada `phase24_p0_metrics.describe`, com 2000 reamostragens de documentos inteiros, seed 0. Cada população matricial contém 64 documentos; todas as instâncias do manifesto são mantidas.

Dicionário nomeado literal de `phase5_msclean.build_dict`, também usado em phase6: 17 átomos, sem alterações. NNLS no QR econômico, float64, limite 100×número de átomos e verificação KKT. A projeção matricial no cone finitamente gerado é única; os coeficientes são únicos se o dicionário tiver posto de colunas completo, como neste dicionário. O truncamento SVD tem garantia de unicidade quando há separação estrita no corte; os empates são contados no JSON.

**Energia nomeada no painel de alocação auditado: rank residual r=8**

Energia significa ||S||²/||A||². Este painel mantém o rank residual auditado; ele não é a comparação de capacidade K=8, que usa q=7.

| n | Modelo | named_first | lowrank_first | 5 iterações do Algoritmo 1 |
| --- | --- | --- | --- | --- |
| 128 | gpt2 | 0.7793 [0.7711; 0.7882] / 0.7569 | 0.0088 [0.0075; 0.0101] / 0.0802 | 0.7762 [0.7631; 0.7868] / 0.7389 |
| 128 | gpt2-medium | 0.8002 [0.7850; 0.8072] / 0.7513 | 0.0028 [0.0023; 0.0033] / 0.0428 | 0.7957 [0.7846; 0.8063] / 0.7349 |
| 128 | EleutherAI/pythia-410m | 0.6369 [0.6081; 0.6743] / 0.6086 | 0.0071 [0.0054; 0.0083] / 0.0503 | 0.6266 [0.5936; 0.6628] / 0.5864 |
| 128 | EleutherAI/pythia-1.4b | 0.5526 [0.5054; 0.6044] / 0.5717 | 0.0047 [0.0038; 0.0056] / 0.0479 | 0.5357 [0.4823; 0.5976] / 0.5514 |
| 128 | Qwen/Qwen2.5-0.5B | 0.7382 [0.7214; 0.7526] / 0.6810 | 0.0099 [0.0085; 0.0113] / 0.0818 | 0.7334 [0.7163; 0.7480] / 0.6611 |
| 128 | Qwen/Qwen2.5-3B | 0.7497 [0.7426; 0.7561] / 0.6865 | 0.0073 [0.0064; 0.0082] / 0.0703 | 0.7441 [0.7357; 0.7506] / 0.6708 |
| 256 | gpt2 | 0.7454 [0.7399; 0.7539] / 0.7221 | 0.0149 [0.0128; 0.0170] / 0.1046 | 0.7429 [0.7352; 0.7519] / 0.7095 |
| 256 | gpt2-medium | 0.7623 [0.7517; 0.7723] / 0.7105 | 0.0047 [0.0040; 0.0057] / 0.0595 | 0.7605 [0.7480; 0.7703] / 0.6989 |
| 256 | EleutherAI/pythia-410m | 0.5549 [0.5314; 0.5789] / 0.5204 | 0.0107 [0.0087; 0.0137] / 0.0672 | 0.5426 [0.5197; 0.5690] / 0.5050 |
| 256 | EleutherAI/pythia-1.4b | 0.4308 [0.4053; 0.4601] / 0.4536 | 0.0086 [0.0069; 0.0103] / 0.0641 | 0.4133 [0.3879; 0.4440] / 0.4397 |
| 256 | Qwen/Qwen2.5-0.5B | 0.7196 [0.7035; 0.7293] / 0.6529 | 0.0170 [0.0147; 0.0196] / 0.1045 | 0.7139 [0.7013; 0.7289] / 0.6405 |
| 256 | Qwen/Qwen2.5-3B | 0.7248 [0.7183; 0.7321] / 0.6545 | 0.0126 [0.0111; 0.0141] / 0.0882 | 0.7271 [0.7193; 0.7325] / 0.6462 |

ALT significa exatamente cinco iterações do Algoritmo 1, começando com L=0, sem parada antecipada; critério registrado: mudança relativa do objetivo <=1e-7. No painel auditado n=128, r=8, 17/9984 atingiram esse critério. Isso não demonstra convergência geral nem ótimo global.

**Capacidade K=8: S+L7, SVD8 e linhas sob o mesmo teto**

B=K(2n+1). S+L usa q=K-1 fixo e custa 2·count(c>0)+q(2n+1), verificando o teto em toda instância; sobra B−custo registrada. SVD usa K(2n+1). Linhas selecionam min(floor(B/2),2n+7) átomos do dicionário de `omp_profiled`, com custo 2 por átomo selecionado, incluindo coeficientes que o NNLS zera. Para K=8, B=2056/4104 em n=128/256; o dicionário de linhas esgota em 263/519 átomos e deixa sobra 1530/3066. O teto permitido é comum; o consumo efetivo e a saturação são explícitos.

Estado do protocolo de linhas: {"status":"user clarification pending; candidate computations explicitly separated"}

Quando o dicionário completo cabe, os valores candidatos de linhas são a solução NNLS terminal do OMP completo, calculada diretamente no mesmo cone. O `omp_profiled` original não foi editado. Os dois controles fixos executaram todo o OMP original: n=128 e 256, com diferença de erro zero frente ao endpoint. Isso não equivale a executar a trajetória OMP em todas as instâncias; o protocolo e sua escolha pendente aparecem explicitamente no JSON.

| n | Modelo | erro S+L7 | erro SVD8 | erro linhas |
| --- | --- | --- | --- | --- |
| 128 | gpt2 | 0.1676 [0.1583; 0.1765] / 0.2068 | 0.2074 [0.1889; 0.2193] / 0.3022 | 0.4535 [0.4413; 0.4639] / 0.4453 |
| 128 | gpt2-medium | 0.1308 [0.1230; 0.1390] / 0.1759 | 0.1438 [0.1313; 0.1545] / 0.2280 | 0.4327 [0.4222; 0.4457] / 0.4407 |
| 128 | EleutherAI/pythia-410m | 0.1731 [0.1625; 0.1879] / 0.2390 | 0.1943 [0.1765; 0.2110] / 0.2871 | 0.4711 [0.4517; 0.4864] / 0.4912 |
| 128 | EleutherAI/pythia-1.4b | 0.1738 [0.1599; 0.1847] / 0.2249 | 0.1832 [0.1702; 0.1957] / 0.2705 | 0.4841 [0.4699; 0.4955] / 0.5000 |
| 128 | Qwen/Qwen2.5-0.5B | 0.2453 [0.2366; 0.2548] / 0.2482 | 0.2718 [0.2614; 0.2833] / 0.3321 | 0.4939 [0.4815; 0.5068] / 0.4734 |
| 128 | Qwen/Qwen2.5-3B | 0.2054 [0.1995; 0.2124] / 0.2307 | 0.2222 [0.2127; 0.2330] / 0.3030 | 0.4728 [0.4666; 0.4813] / 0.4698 |
| 256 | gpt2 | 0.2128 [0.2021; 0.2220] / 0.2512 | 0.2582 [0.2475; 0.2709] / 0.3600 | 0.4930 [0.4834; 0.4984] / 0.4867 |
| 256 | gpt2-medium | 0.1690 [0.1602; 0.1785] / 0.2177 | 0.1919 [0.1775; 0.2011] / 0.2811 | 0.4752 [0.4639; 0.4868] / 0.4870 |
| 256 | EleutherAI/pythia-410m | 0.2337 [0.2240; 0.2453] / 0.2940 | 0.2568 [0.2388; 0.2759] / 0.3513 | 0.5213 [0.5101; 0.5331] / 0.5445 |
| 256 | EleutherAI/pythia-1.4b | 0.2312 [0.2183; 0.2442] / 0.2788 | 0.2495 [0.2397; 0.2683] / 0.3340 | 0.5341 [0.5244; 0.5420] / 0.5514 |
| 256 | Qwen/Qwen2.5-0.5B | 0.3030 [0.2912; 0.3096] / 0.3014 | 0.3506 [0.3364; 0.3643] / 0.3978 | 0.5155 [0.5065; 0.5297] / 0.5067 |
| 256 | Qwen/Qwen2.5-3B | 0.2549 [0.2462; 0.2600] / 0.2763 | 0.2823 [0.2731; 0.2914] / 0.3597 | 0.4964 [0.4914; 0.5022] / 0.4971 |

Diferença = erro do método − erro SVD; sinais positivos e rank-biserial positivo favorecem SVD. O Wilcoxon usa as 64 medianas documentais das diferenças pareadas, bilateral, zeros removidos pelo método wilcox e aproximação assintótica. Os p são não ajustados. O IC da diferença mediana usa as diferenças de todas as instâncias e o mesmo bootstrap de documentos; é um estimando diferente da mediana das 64 medianas. Fração SVD = vitória estrita em instâncias cabeça×documento / fração de cabeças distintas após mediana sobre documentos, secundária.

**S+L7 versus SVD8**

| n | Modelo | diferença pareada | p Wilcoxon | rank-biserial | vitórias do braço direito: instâncias / cabeças |
| --- | --- | --- | --- | --- | --- |
| 128 | gpt2 | -0.02530 [-0.02909; -0.02065] / -0.09539 | 3.5255e-12 | -1.0000 | 24.67% / 23.61% |
| 128 | gpt2-medium | -0.00471 [-0.00608; -0.00340] / -0.05208 | 8.3827e-11 | -0.9337 | 38.74% / 39.84% |
| 128 | EleutherAI/pythia-410m | -0.00787 [-0.01057; -0.00606] / -0.04814 | 1.8903e-11 | -0.9654 | 39.26% / 38.28% |
| 128 | EleutherAI/pythia-1.4b | -0.00318 [-0.00460; -0.00071] / -0.04561 | 0.00063242 | -0.4913 | 46.29% / 46.88% |
| 128 | Qwen/Qwen2.5-0.5B | -0.01585 [-0.01991; -0.01109] / -0.08391 | 4.6826e-12 | -0.9942 | 34.31% / 33.93% |
| 128 | Qwen/Qwen2.5-3B | -0.01212 [-0.01451; -0.01029] / -0.07233 | 3.5255e-12 | -1.0000 | 30.34% / 29.69% |
| 256 | gpt2 | -0.03536 [-0.04221; -0.03093] / -0.10884 | 3.5255e-12 | -1.0000 | 21.35% / 20.14% |
| 256 | gpt2-medium | -0.01092 [-0.01300; -0.00906] / -0.06343 | 3.5255e-12 | -1.0000 | 30.66% / 30.47% |
| 256 | EleutherAI/pythia-410m | -0.01561 [-0.01808; -0.01257] / -0.05731 | 4.6826e-12 | -0.9942 | 34.24% / 33.85% |
| 256 | EleutherAI/pythia-1.4b | -0.00941 [-0.01269; -0.00718] / -0.05521 | 6.1363e-11 | -0.9404 | 40.36% / 39.58% |
| 256 | Qwen/Qwen2.5-0.5B | -0.02623 [-0.03177; -0.02134] / -0.09642 | 3.876e-12 | -0.9981 | 28.58% / 27.68% |
| 256 | Qwen/Qwen2.5-3B | -0.02129 [-0.02376; -0.01903] / -0.08337 | 3.5255e-12 | -1.0000 | 20.40% / 18.92% |

**linhas versus SVD8**

| n | Modelo | diferença pareada | p Wilcoxon | rank-biserial | vitórias do braço direito: instâncias / cabeças |
| --- | --- | --- | --- | --- | --- |
| 128 | gpt2 | 0.20255 [0.19549; 0.20738] / 0.14311 | 3.5255e-12 | +1.0000 | 81.90% / 81.94% |
| 128 | gpt2-medium | 0.23871 [0.23000; 0.24870] / 0.21274 | 3.5255e-12 | +1.0000 | 90.23% / 90.36% |
| 128 | EleutherAI/pythia-410m | 0.23398 [0.22213; 0.24256] / 0.20411 | 3.5255e-12 | +1.0000 | 91.15% / 91.15% |
| 128 | EleutherAI/pythia-1.4b | 0.27358 [0.25553; 0.28797] / 0.22950 | 3.5255e-12 | +1.0000 | 90.23% / 90.62% |
| 128 | Qwen/Qwen2.5-0.5B | 0.20717 [0.19685; 0.21296] / 0.14124 | 3.5255e-12 | +1.0000 | 83.33% / 83.04% |
| 128 | Qwen/Qwen2.5-3B | 0.22202 [0.21728; 0.22756] / 0.16676 | 3.5255e-12 | +1.0000 | 85.46% / 85.76% |
| 256 | gpt2 | 0.19254 [0.18389; 0.19948] / 0.12666 | 3.5255e-12 | +1.0000 | 79.56% / 79.86% |
| 256 | gpt2-medium | 0.24537 [0.23778; 0.25477] / 0.20593 | 3.5255e-12 | +1.0000 | 88.02% / 87.76% |
| 256 | EleutherAI/pythia-410m | 0.23161 [0.22313; 0.24037] / 0.19324 | 3.5255e-12 | +1.0000 | 86.20% / 86.20% |
| 256 | EleutherAI/pythia-1.4b | 0.27429 [0.26219; 0.28550] / 0.21742 | 3.5255e-12 | +1.0000 | 86.98% / 86.46% |
| 256 | Qwen/Qwen2.5-0.5B | 0.18169 [0.17350; 0.18958] / 0.10891 | 3.5255e-12 | +1.0000 | 78.97% / 78.87% |
| 256 | Qwen/Qwen2.5-3B | 0.19994 [0.19463; 0.20566] / 0.13744 | 3.5255e-12 | +1.0000 | 83.03% / 83.33% |

**S+L7 versus linhas**

| n | Modelo | diferença pareada | p Wilcoxon | rank-biserial | vitórias do braço direito: instâncias / cabeças |
| --- | --- | --- | --- | --- | --- |
| 128 | gpt2 | -0.23600 [-0.24004; -0.23130] / -0.23850 | 3.5255e-12 | -1.0000 | 2.54% / 2.78% |
| 128 | gpt2-medium | -0.25902 [-0.26632; -0.25263] / -0.26481 | 3.5255e-12 | -1.0000 | 0.00% / 0.00% |
| 128 | EleutherAI/pythia-410m | -0.24978 [-0.25694; -0.24132] / -0.25225 | 3.5255e-12 | -1.0000 | 0.26% / 0.26% |
| 128 | EleutherAI/pythia-1.4b | -0.28538 [-0.29691; -0.27271] / -0.27511 | 3.5255e-12 | -1.0000 | 0.26% / 0.26% |
| 128 | Qwen/Qwen2.5-0.5B | -0.23810 [-0.24520; -0.23217] / -0.22515 | 3.5255e-12 | -1.0000 | 4.43% / 4.76% |
| 128 | Qwen/Qwen2.5-3B | -0.24899 [-0.25320; -0.24500] / -0.23909 | 3.5255e-12 | -1.0000 | 2.65% / 2.26% |
| 256 | gpt2 | -0.23149 [-0.23660; -0.22803] / -0.23549 | 3.5255e-12 | -1.0000 | 2.73% / 2.78% |
| 256 | gpt2-medium | -0.26445 [-0.27134; -0.25839] / -0.26936 | 3.5255e-12 | -1.0000 | 0.00% / 0.00% |
| 256 | EleutherAI/pythia-410m | -0.24968 [-0.25701; -0.24073] / -0.25055 | 3.5255e-12 | -1.0000 | 0.26% / 0.26% |
| 256 | EleutherAI/pythia-1.4b | -0.28533 [-0.29362; -0.27610] / -0.27263 | 3.5255e-12 | -1.0000 | 0.39% / 0.26% |
| 256 | Qwen/Qwen2.5-0.5B | -0.21719 [-0.22287; -0.21214] / -0.20533 | 3.5255e-12 | -1.0000 | 5.08% / 5.36% |
| 256 | Qwen/Qwen2.5-3B | -0.23050 [-0.23447; -0.22594] / -0.22080 | 3.5255e-12 | -1.0000 | 3.21% / 3.30% |

r=0 consta somente como descrição do canal nomeado. Não há comparação contra SVD de rank zero. `named_channel_only_error` representa ||A−S||/||A||, com custo próprio 2·átomos ativos; não é um braço com orçamento igual à SVD.

**Resíduo sob o teto K=8, q=7, named_first**

| n | Modelo | posto efetivo R | posto efetivo E | primeiras 4 colunas R | primeiras 4 colunas E | energia futura E |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | gpt2 | 5.06 | 40.13 | 65.15% | 3.04% | 8.15% |
| 128 | gpt2-medium | 4.08 | 36.07 | 67.26% | 3.04% | 9.71% |
| 128 | EleutherAI/pythia-410m | 5.58 | 37.93 | 36.22% | 2.58% | 9.07% |
| 128 | EleutherAI/pythia-1.4b | 4.99 | 36.59 | 36.13% | 2.26% | 8.22% |
| 128 | Qwen/Qwen2.5-0.5B | 8.22 | 35.79 | 50.74% | 3.23% | 7.48% |
| 128 | Qwen/Qwen2.5-3B | 6.88 | 37.23 | 53.14% | 2.70% | 6.64% |
| 256 | gpt2 | 6.60 | 65.35 | 64.67% | 1.62% | 5.50% |
| 256 | gpt2-medium | 4.90 | 54.91 | 67.10% | 1.57% | 7.01% |
| 256 | EleutherAI/pythia-410m | 6.72 | 56.34 | 27.19% | 1.38% | 6.20% |
| 256 | EleutherAI/pythia-1.4b | 5.51 | 54.69 | 25.70% | 1.10% | 5.22% |
| 256 | Qwen/Qwen2.5-0.5B | 12.09 | 58.30 | 48.03% | 1.70% | 4.83% |
| 256 | Qwen/Qwen2.5-3B | 9.37 | 60.12 | 51.61% | 1.47% | 4.25% |

R=A−S e E=A−S−L7. Posto efetivo = exp(entropia de Shannon dos sigma² normalizados). Frações espaciais têm como denominador a energia do próprio resíduo; também há valores normalizados por ||A||² no JSON. Faixas de i−j: <0, 0, 1, 2–3, 4–7, 8–15, 16–31, 32–63, 64–127, >=128. Espectros completos e ICs por posição singular estão nos resultados. O resíduo final é assinado e tem cauda mais difusa; estes números não demonstram que seja ruído nem semanticamente irrelevante.

**KL do último token e regra de linha vazia**

FALTA: injeção e KL do último token; estado `waiting_for_required_V1`. Arquivo exigido `out/phase2_downstream_v2.json`; início 2026-11-09T21:11:20+00:00, prazo 2026-11-10T00:11:20+00:00. Nenhuma KL ou contagem de conclusão do modelo foi imputada. Adaptador e controles CPU estão preparados; nenhum resultado CPU é apresentado como comportamento do modelo.

**Leitura dos resultados**

A ordem de alocação muda fortemente a energia atribuída ao canal nomeado. A projeção named_first define uma convenção reproduzível, mas não identifica uma única separação intrínseca S/L. A vantagem matricial de S+L7 nas medianas não implica vitória em toda cabeça nem preservação do comportamento; esta última exige a injeção concluída. O método de linhas satura seu dicionário antes de gastar o teto de K=8; sua comparação deve ser lida com a sobra registrada.

