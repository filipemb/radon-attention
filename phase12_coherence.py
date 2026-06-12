"""
A1 — substancia o framing MCA/geometric-separation (pedido do revisor NN).

Calcula a coerencia mutua do dicionario nomeado de 15 atomos (max |<d_i,d_j>|
fora da diagonal) e o espectro do Gram. Coerencia baixa entre CLASSES (sink vs
banda vs diagonal) e a base matematica pra separacao; coerencia alta DENTRO da
classe de bandas (taus vizinhos) explica por que o OMP escolhe 1-2 bandas e para.

Tambem registra o ponto teorico do revisor: a coluna do sink e exatamente o tipo
de estrutura coerente que VIOLA as condicoes de incoerencia do RPCA classico
(uma coluna inteira correlacionada), o que justifica atribui-la explicitamente
ao canal estruturado em vez de deixar o L absorve-la.

CPU, sem modelo. Saida: out/phase12_coherence.json
"""
import json
import os
import numpy as np
from phase5_msclean import build_dict

n = 128
D, labels = build_dict(n)            # [n*n, m], colunas normalizadas
G = D.T @ D                          # Gram m x m
m = G.shape[0]
off = np.abs(G - np.eye(m))

names = [f"{k}_{v}" for (k, v) in labels]


def cls(lab):
    k, v = lab
    if k == "sink" or (k == "vert" and v == 0):
        return "sink"
    if k == "vert":
        return "vert"
    return "band" if k == "band" else "diag"


classes = [cls(l) for l in labels]
mu_global = float(off.max())
intra, inter = [], []
pairs_inter = []
for i in range(m):
    for j in range(i + 1, m):
        c = float(off[i, j])
        if classes[i] == classes[j]:
            intra.append(c)
        else:
            inter.append(c)
            pairs_inter.append((names[i], names[j], c))

pairs_inter.sort(key=lambda x: -x[2])
res = {
    "n_atoms": m,
    "mu_global": mu_global,
    "mu_intra_class_max": float(max(intra)),
    "mu_inter_class_max": float(max(inter)),
    "mu_inter_class_median": float(np.median(inter)),
    "top_inter_pairs": pairs_inter[:6],
}
os.makedirs("out", exist_ok=True)
json.dump(res, open("out/phase12_coherence.json", "w"), indent=2)
print(f"atomos: {m}")
print(f"coerencia global (max off-diag): {mu_global:.3f}")
print(f"  intra-classe (bandas entre si etc): max {max(intra):.3f}")
print(f"  ENTRE classes (sink vs banda vs diag): max {max(inter):.3f}, mediana {np.median(inter):.3f}")
print("top pares entre classes:")
for a, b, c in pairs_inter[:6]:
    print(f"  {a:>9} x {b:<9} = {c:.3f}")
