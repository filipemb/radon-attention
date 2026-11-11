"""E3 - outros baselines low-rank nas matrizes de atencao (experimento fechado).

Compara SVD truncada exata contra outros metodos low-rank (SVD randomizada,
CUR deterministico, CUR randomizado e esqueleto uniforme) nas mesmas matrizes
de atencao de data/attn/*.npz, mesmos ranks, mesmo erro (Frobenius, matriz
inteira, float64).

Metodos (rank alvo r, matriz A n x n):
  svd            SVD truncada exata (piso teorico).  storage = r*(2n+1)
  rsvd           SVD randomizada de Halko-Martinsson-Tropp (2011), Algoritmo
                 4.4 estabilizado: Y = A @ Omega; Q = qr(Y); repetir q=2 vezes
                 Z = A.T @ Q, Q' = qr(Z), Y = A @ Q', Q = qr(Y) (QR entre as
                 aplicacoes de A e A.T); B = Q.T @ A; SVD de B; U = Q @ Ub;
                 truncar em r. Oversampling p=10, gaussiana semente fixa 0.
                 storage = r*(2n+1)
  cur_det        CUR com leverage scores da SVD rank-r de A; top-r colunas e
                 linhas (deterministico). U = pinv(C) @ A @ pinv(R) (pinv padrao).
                 storage = n*r + r*n + r*r + 2*r
  cur_rand_mean / cur_rand_worst: mesmo que cur_det mas amostrando r colunas e
                 r linhas sem reposicao com prob. proporcional ao leverage;
                 5 sorteios (sementes 0..4); media e pior por matriz.
                 storage = n*r + r*n + r*r + 2*r
  skeleton_unif  marcos uniformes I = J = round(linspace(0, n-1, r));
                 A^ = C @ pinv(W, rcond=1e-6) @ R. storage = 2*n*r + r*r + 2*r

Controle positivo (roda primeiro; se falhar, PARA com exit 1 sem rodar o
experimento e sem ajustar tolerancia):
(a) posto 8 exato bem condicionado (n=128, produto de fatores gaussianos
    semente 123; mais versao nao-negativa via |.|). Com r=8, svd, rsvd,
    cur_det e skeleton_unif devem dar erro relativo < 1e-6.
(b) posto 8 exato com condicionamento 1e8 (n=128; A = Q1 @ diag(s) @ Q2.T
    com Q1, Q2 ortonormais e s geometrica de 1 a 1e-8, semente 123).
    Com r=8, svd e rsvd devem dar erro relativo < 1e-6.
(c) posto 8 (matriz do item b) mais ruido gaussiano de norma relativa 1e-3
    (||N||_F/||B||_F = 1e-3, semente 1001). Com r=8, svd, rsvd, cur_det,
    cur_rand_mean e cur_rand_worst devem dar erro relativo <= 2e-3;
    skeleton_unif so reporta.
(d) cur_rand nos casos (a) e (b) com as 5 sementes (0..4): so reporta o
    pior erro por matriz, sem criterio de falha.

Saidas v2 (nao sobrescrevem a v1): out/phase20_lowrank_baselines_v2.json e
out/pairs/phase20_lowrank_{slug}_n{n}_v2.jsonl. O JSON v2 tambem guarda, por
modelo e n, a mediana das razoes pareadas por instancia cur_det(2r)/svd(r)
e cur_rand_mean(2r)/svd(r) para r em {4, 8, 16} e a fracao com razao <= 1.1.

Uso: .venv/Scripts/python.exe phase20_lowrank_baselines.py [--jobs 2]
"""

import json
import os

# Threads BLAS/OpenMP: fixar antes de importar numpy.
os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")

import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent
DATA = REPO / "data" / "attn"
OUT = REPO / "out"
PAIRS = OUT / "pairs"

MODELS = ["gpt2", "gpt2-medium", "EleutherAI__pythia-410m",
          "EleutherAI__pythia-1.4b", "Qwen__Qwen2.5-0.5B", "Qwen__Qwen2.5-3B"]
NS = [128, 256]
RANKS = [1, 2, 4, 8, 16, 32]
RSVD_P = 10
RSVD_Q = 2
CUR_SEEDS = [0, 1, 2, 3, 4]
SKELETON_RCOND = 1e-6
CONTROL_TOL = 1e-6
CONTROL_NOISY_TOL = 2e-3
CONTROL_NOISE_REL = 1e-3
CONTROL_NOISE_SEED = 1001
CONTROL_COND = 1e8
RATIO_RS = (4, 8, 16)
RATIO_FRAC_THR = 1.1
OUT_TAG = "_v2"
METHODS = ("svd", "rsvd", "cur_det", "cur_rand_mean", "cur_rand_worst",
           "skeleton_unif")


# ---------------- metodos ----------------

def svd_reconstruct(U, S, Vt, r):
    return (U[:, :r] * S[:r]) @ Vt[:r, :]


def rsvd_reconstruct(A, r, p=RSVD_P, q=RSVD_Q):
    """SVD randomizada, Halko-Martinsson-Tropp (2011) Algoritmo 4.4.

    Y = A @ Omega (gaussiana, semente fixa 0); Q = qr(Y); repetir q vezes:
    Z = A.T @ Q; Qz = qr(Z); Y = A @ Qz; Q = qr(Y). Depois B = Q.T @ A,
    SVD de B, U = Q @ Ub, trunca em r. O QR entre as aplicacoes de A e A.T
    estabiliza a iteracao de subespaco (sem ele, as colunas de Y colapsam
    para o vetor singular dominante e posto-8 com cond 1e8 falha).
    """
    n = A.shape[0]
    rng = np.random.default_rng(0)
    ell = r + p
    Omega = rng.standard_normal((n, ell))
    Y = A @ Omega
    Q, _ = np.linalg.qr(Y)
    for _ in range(q):
        Z = A.T @ Q
        Qz, _ = np.linalg.qr(Z)
        Y = A @ Qz
        Q, _ = np.linalg.qr(Y)
    B = Q.T @ A
    Ub, Sb, Vbt = np.linalg.svd(B, full_matrices=False)
    return (Q @ Ub[:, :r] * Sb[:r]) @ Vbt[:r, :]


def leverage_scores(U, Vt, r):
    Ur = U[:, :r]
    Vr = Vt[:r, :].T
    row_lev = np.sum(Ur ** 2, axis=1)
    col_lev = np.sum(Vr ** 2, axis=1)
    return row_lev, col_lev


def topk_desc(x, k):
    return np.argsort(-x, kind="stable")[:k]


def cur_reconstruct(A, rows, cols):
    C = A[:, cols]
    R = A[rows, :]
    U = np.linalg.pinv(C) @ A @ np.linalg.pinv(R)
    return C @ U @ R


def skeleton_reconstruct(A, idx):
    C = A[:, idx]
    R = A[idx, :]
    W = A[np.ix_(idx, idx)]
    return C @ np.linalg.pinv(W, rcond=SKELETON_RCOND) @ R


def uniform_landmarks(n, r):
    return np.round(np.linspace(0, n - 1, r)).astype(int)


def rel_abs(A, Ahat):
    diff = float(np.linalg.norm(A - Ahat))
    denom = float(np.linalg.norm(A))
    return diff / denom, diff


def clean_float(x):
    # NaN/inf nunca viram zero: vao como null no JSON e sao contados.
    return None if not np.isfinite(x) else float(x)


# ---------------- controle positivo ----------------

def exact_rank8_ill(n=128, rank=8, cond=CONTROL_COND, seed=123):
    """Posto 8 exato com condicionamento `cond` (s geometrica 1..1/cond)."""
    rng = np.random.default_rng(seed)
    Q1, _ = np.linalg.qr(rng.standard_normal((n, rank)))
    Q2, _ = np.linalg.qr(rng.standard_normal((n, rank)))
    s = np.geomspace(1.0, 1.0 / cond, rank)
    return (Q1 * s) @ Q2.T


def cur_rand_draw_errors(A, rl, cl, r, seeds=CUR_SEEDS):
    """Erros relativos dos sorteios cur_rand (5 sementes)."""
    n = A.shape[0]
    pr = rl / rl.sum()
    pc = cl / cl.sum()
    draws = []
    for s in seeds:
        grng = np.random.default_rng(s)
        sr = grng.choice(n, size=r, replace=False, p=pr)
        sc = grng.choice(n, size=r, replace=False, p=pc)
        draws.append(rel_abs(A, cur_reconstruct(A, sr, sc))[0])
    return draws


def positive_control():
    n, rank = 128, 8
    rng = np.random.default_rng(123)
    G1 = rng.standard_normal((n, rank))
    G2 = rng.standard_normal((rank, n))
    A_gauss = G1 @ G2
    A_nonneg = np.abs(G1) @ np.abs(G2)
    A_ill = exact_rank8_ill(n, rank)
    # (c): matriz do item (b) + ruido gaussiano de norma relativa 1e-3.
    grng = np.random.default_rng(CONTROL_NOISE_SEED)
    N = grng.standard_normal(A_ill.shape)
    N *= (CONTROL_NOISE_REL * float(np.linalg.norm(A_ill))
          / float(np.linalg.norm(N)))
    A_noisy = A_ill + N
    print("[control] positivo em 4 partes (a)-(d), n=128, r=8", flush=True)
    results = {}
    ok_all = True

    # (a) posto 8 exato bem condicionado: svd, rsvd, cur_det, skeleton < 1e-6.
    for name, A in (("gauss", A_gauss), ("nonneg", A_nonneg)):
        U, S, Vt = np.linalg.svd(A, full_matrices=False)
        approx = {
            "svd": svd_reconstruct(U, S, Vt, rank),
            "rsvd": rsvd_reconstruct(A, rank),
        }
        rl, cl = leverage_scores(U, Vt, rank)
        approx["cur_det"] = cur_reconstruct(A, topk_desc(rl, rank),
                                            topk_desc(cl, rank))
        approx["skeleton_unif"] = skeleton_reconstruct(
            A, uniform_landmarks(n, rank))
        results[name] = {}
        for m, Ahat in approx.items():
            rel, _ = rel_abs(A, Ahat)
            passed = bool(rel < CONTROL_TOL)
            results[name][m] = {"rel": float(rel), "pass": passed}
            ok_all = ok_all and passed
            print(f"[control] (a) {name:>7} {m:>14}: rel={rel:.3e} "
                  f"{'OK' if passed else 'FAIL'} (< 1e-6)", flush=True)

    # (b) posto 8 exato, cond 1e8: svd e rsvd < 1e-6.
    U, S, Vt = np.linalg.svd(A_ill, full_matrices=False)
    cond = float(S[0] / S[rank - 1])
    results["ill_cond_1e8"] = {"cond_top8": cond}
    print(f"[control] (b) condicao top-8: {cond:.3e}", flush=True)
    approx_b = {"svd": svd_reconstruct(U, S, Vt, rank),
                "rsvd": rsvd_reconstruct(A_ill, rank)}
    for m, Ahat in approx_b.items():
        rel, _ = rel_abs(A_ill, Ahat)
        passed = bool(rel < CONTROL_TOL)
        results["ill_cond_1e8"][m] = {"rel": float(rel), "pass": passed}
        ok_all = ok_all and passed
        print(f"[control] (b) {'ill':>7} {m:>14}: rel={rel:.3e} "
              f"{'OK' if passed else 'FAIL'} (< 1e-6)", flush=True)

    # (c) posto 8 + ruido 1e-3: todos <= 2e-3, exceto esqueleto (report).
    U, S, Vt = np.linalg.svd(A_noisy, full_matrices=False)
    rl, cl = leverage_scores(U, Vt, rank)
    draws = cur_rand_draw_errors(A_noisy, rl, cl, rank)
    approx_c = {
        "svd": rel_abs(A_noisy, svd_reconstruct(U, S, Vt, rank))[0],
        "rsvd": rel_abs(A_noisy, rsvd_reconstruct(A_noisy, rank))[0],
        "cur_det": rel_abs(A_noisy, cur_reconstruct(
            A_noisy, topk_desc(rl, rank), topk_desc(cl, rank)))[0],
        "cur_rand_mean": float(np.mean(draws)),
        "cur_rand_worst": float(np.max(draws)),
    }
    idx = uniform_landmarks(n, rank)
    sk_rel, _ = rel_abs(A_noisy, skeleton_reconstruct(A_noisy, idx))
    results["noisy_1e-3"] = {"noise_rel": CONTROL_NOISE_REL,
                             "noise_seed": CONTROL_NOISE_SEED}
    for m, rel in approx_c.items():
        passed = bool(rel <= CONTROL_NOISY_TOL)
        results["noisy_1e-3"][m] = {"rel": float(rel), "pass": passed}
        ok_all = ok_all and passed
        print(f"[control] (c) {'noisy':>7} {m:>14}: rel={rel:.3e} "
              f"{'OK' if passed else 'FAIL'} (<= 2e-3)", flush=True)
    results["noisy_1e-3"]["skeleton_unif"] = {"rel": float(sk_rel),
                                              "pass": None}
    print(f"[control] (c) {'noisy':>7} {'skeleton_unif':>14}: "
          f"rel={sk_rel:.3e} REPORT", flush=True)

    # (d) cur_rand nas 5 sementes nos casos (a) e (b): so reporta o pior.
    results["cur_rand_5seeds_worst"] = {}
    for name, A in (("gauss", A_gauss), ("nonneg", A_nonneg),
                    ("ill_cond_1e8", A_ill)):
        U, S, Vt = np.linalg.svd(A, full_matrices=False)
        rl, cl = leverage_scores(U, Vt, rank)
        draws = cur_rand_draw_errors(A, rl, cl, rank)
        worst = float(np.max(draws))
        results["cur_rand_5seeds_worst"][name] = {
            "worst_rel": worst,
            "draws_rel": [float(d) for d in draws],
            "pass": None,
        }
        print(f"[control] (d) {name:>13} cur_rand pior-das-5: "
              f"rel={worst:.3e} REPORT", flush=True)

    if not ok_all:
        print("[control] FAIL: algum criterio (a)/(b)/(c) nao passou; "
              "parando sem ajustar tolerancia.", flush=True)
        sys.exit(1)
    print("[control] PASS: (a)<1e-6, (b)<1e-6, (c)<=2e-3.", flush=True)
    return results


# ---------------- experimento ----------------

def storage_of(method, n, r):
    if method in ("svd", "rsvd"):
        return r * (2 * n + 1)
    return n * r + r * n + r * r + 2 * r


def summarize(acc, n):
    out = {}
    for m in METHODS:
        out[m] = {}
        for r in RANKS:
            rel = np.array(acc[m][r]["rel"], dtype=np.float64)
            ab = np.array(acc[m][r]["abs"], dtype=np.float64)
            n_nan_rel = int(np.isnan(rel).sum())
            n_nan_abs = int(np.isnan(ab).sum())
            out[m][str(r)] = {
                "median_rel": clean_float(np.nanmedian(rel)),
                "p25_rel": clean_float(np.nanpercentile(rel, 25)),
                "p75_rel": clean_float(np.nanpercentile(rel, 75)),
                "mean_rel": clean_float(np.nanmean(rel)),
                "median_abs": clean_float(np.nanmedian(ab)),
                "p25_abs": clean_float(np.nanpercentile(ab, 25)),
                "p75_abs": clean_float(np.nanpercentile(ab, 75)),
                "mean_abs": clean_float(np.nanmean(ab)),
                "storage": storage_of(m, n, r),
                "n_matrices": len(rel),
                "n_nan_rel": n_nan_rel,
                "n_nan_abs": n_nan_abs,
            }
    return out


def process_file(slug, n):
    t0 = time.perf_counter()
    npz_path = DATA / f"{slug}_n{n}.npz"
    man_path = DATA / f"{slug}_n{n}.manifest.json"
    z = np.load(npz_path)
    att = z["attention"]
    doc_idx = z["document_index"]
    layers = z["layer"]
    heads = z["head"]
    man = json.loads(man_path.read_text(encoding="utf-8"))
    model = man["model"]
    inst = man["instances"]
    assert len(inst) == att.shape[0], (slug, n)
    for i, e in enumerate(inst):
        assert (e["document_index"] == int(doc_idx[i])
                and e["layer"] == int(layers[i])
                and e["head"] == int(heads[i])), (slug, n, i)

    acc = {m: {r: {"rel": [], "abs": []} for r in RANKS} for m in METHODS}
    prat = {m: {r: [] for r in RATIO_RS}
            for m in ("cur_det", "cur_rand_mean")}
    n_nonfinite = 0
    pair_path = PAIRS / f"phase20_lowrank_{slug}_n{n}{OUT_TAG}.jsonl"
    with open(pair_path, "w", encoding="utf-8") as fout:
        for i in range(att.shape[0]):
            A = att[i].astype(np.float64)
            U, S, Vt = np.linalg.svd(A, full_matrices=False)
            row = {}
            for r in RANKS:
                cell = {}
                cell["svd"] = rel_abs(A, svd_reconstruct(U, S, Vt, r))
                cell["rsvd"] = rel_abs(A, rsvd_reconstruct(A, r))
                rl, cl = leverage_scores(U, Vt, r)
                cell["cur_det"] = rel_abs(
                    A, cur_reconstruct(A, topk_desc(rl, r),
                                       topk_desc(cl, r)))
                pr = rl / rl.sum()
                pc = cl / cl.sum()
                draws = []
                for s in CUR_SEEDS:
                    grng = np.random.default_rng(s)
                    sr = grng.choice(n, size=r, replace=False, p=pr)
                    sc = grng.choice(n, size=r, replace=False, p=pc)
                    draws.append(rel_abs(A, cur_reconstruct(A, sr, sc)))
                relm = float(np.mean([d[0] for d in draws]))
                absm = float(np.mean([d[1] for d in draws]))
                relw = float(np.max([d[0] for d in draws]))
                absw = float(np.max([d[1] for d in draws]))
                cell["cur_rand_mean"] = (relm, absm)
                cell["cur_rand_worst"] = (relw, absw)
                idx = uniform_landmarks(n, r)
                cell["skeleton_unif"] = rel_abs(
                    A, skeleton_reconstruct(A, idx))
                row[str(r)] = cell
                for m, (vrel, vabs) in cell.items():
                    acc[m][r]["rel"].append(vrel)
                    acc[m][r]["abs"].append(vabs)
                    if not np.isfinite(vrel) or not np.isfinite(vabs):
                        n_nonfinite += 1
            line = {"doc": inst[i]["doc_id"],
                    "document_index": int(doc_idx[i]),
                    "layer": int(layers[i]), "head": int(heads[i]),
                    "instance_id": inst[i]["instance_id"], "n": n,
                    "errors": {m: {str(r): {
                        "rel": clean_float(row[str(r)][m][0]),
                        "abs": clean_float(row[str(r)][m][1])}
                        for r in RANKS} for m in METHODS}}
            fout.write(json.dumps(line) + "\n")
            for r in RATIO_RS:
                svd_r = row[str(r)]["svd"][0]
                if not np.isfinite(svd_r) or svd_r <= 0:
                    continue
                for m in ("cur_det", "cur_rand_mean"):
                    cur_2r = row[str(2 * r)][m][0]
                    if np.isfinite(cur_2r):
                        prat[m][r].append(cur_2r / svd_r)
    summary = summarize(acc, n)
    paired_ratios = {}
    for r in RATIO_RS:
        cell = {}
        for m in ("cur_det", "cur_rand_mean"):
            vals = np.array(prat[m][r], dtype=np.float64)
            finite = vals[np.isfinite(vals)]
            cell[f"{m}_r{2 * r}_over_svd_r{r}"] = {
                "median": clean_float(np.median(finite))
                if len(finite) else None,
                f"frac_le_{RATIO_FRAC_THR}": (
                    clean_float(float(np.mean(finite <= RATIO_FRAC_THR)))
                    if len(finite) else None),
                "n": int(len(finite)),
            }
        paired_ratios[str(r)] = cell
    elapsed = time.perf_counter() - t0
    print(f"[done] {slug} n={n}: {att.shape[0]} matrizes em "
          f"{elapsed:.1f}s (nao-finitos: {n_nonfinite})", flush=True)
    return {"model": model, "slug": slug, "n": n,
            "n_matrices": int(att.shape[0]), "summary": summary,
            "paired_ratios": paired_ratios,
            "elapsed_seconds": elapsed}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=2)
    args = ap.parse_args()
    jobs = max(1, min(args.jobs, 2))
    OUT.mkdir(exist_ok=True)
    PAIRS.mkdir(exist_ok=True)
    t_start = time.perf_counter()

    control = positive_control()

    tasks = [(slug, n) for slug in MODELS for n in NS]
    for slug, n in tasks:
        assert (DATA / f"{slug}_n{n}.npz").exists(), slug
        assert (DATA / f"{slug}_n{n}.manifest.json").exists(), slug

    file_results = []
    if jobs == 1:
        for slug, n in tasks:
            file_results.append(process_file(slug, n))
    else:
        with ProcessPoolExecutor(max_workers=jobs) as ex:
            futs = [ex.submit(process_file, slug, n) for slug, n in tasks]
            for f in futs:
                file_results.append(f.result())

    results = {}
    for fr in file_results:
        results.setdefault(fr["model"], {})[str(fr["n"])] = {
            "slug": fr["slug"], "n_matrices": fr["n_matrices"],
            "methods": fr["summary"],
            "paired_ratios": fr["paired_ratios"],
            "elapsed_seconds": fr["elapsed_seconds"],
        }
    payload = {
        "experiment": "phase20_lowrank_baselines",
        "output_tag": OUT_TAG,
        "ranks": RANKS,
        "methods": list(METHODS),
        "rsvd": {"oversampling_p": RSVD_P, "power_iterations_q": RSVD_Q,
                 "seed": 0, "stabilized_qr": True,
                 "algorithm": "Halko-Martinsson-Tropp (2011), Algoritmo 4.4: "
                 "Y = A @ Omega; Q = qr(Y); repetir q vezes Z = A.T @ Q, "
                 "Q' = qr(Z), Y = A @ Q', Q = qr(Y); B = Q.T @ A; SVD de B; "
                 "U = Q @ Ub; truncar em r (QR entre as aplicacoes de A e A.T)"},
        "cur_rand_seeds": CUR_SEEDS,
        "skeleton_rcond": SKELETON_RCOND,
        "positive_control": control,
        "paired_ratio_def": "por instancia: cur_det(2r)/svd(r) e "
            "cur_rand_mean(2r)/svd(r) (erros relativos); mediana e fracao "
            f"com razao <= {RATIO_FRAC_THR}, r em {list(RATIO_RS)}",
        "storage_formula": {
            "svd_rsvd": "r*(2n+1)",
            "cur_skeleton": "n*r + r*n + r*r + 2*r"},
        "error": "relativo ||A-A^||_F/||A||_F e absoluto ||A-A^||_F, "
                 "matriz inteira n x n, float64; NaN -> null (contado)",
        "results": results,
        "elapsed_seconds": time.perf_counter() - t_start,
    }
    out_name = f"phase20_lowrank_baselines{OUT_TAG}.json"
    with open(OUT / out_name, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"[json] {OUT / out_name} "
          f"total={payload['elapsed_seconds']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
