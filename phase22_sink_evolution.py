"""E5: contribuicao do sink para a metrica de concentracao.

Parte A (GPU): evolucao no treino do Pythia-410m. Extrai as mesmas matrizes de
  data/attn/EleutherAI__pythia-410m_n128 (mesmos input_ids e instancias) nos
  checkpoints publicos step0/step1000/step4000/step16000/step64000/step143000,
  salva em data/attn_ckpt/ e mede sink + concentracao por revisao.
Parte B (CPU): ablacoes do sink nas matrizes salvas n=128 dos 6 modelos, com
  controles de massa casada.
Parte B2 (CPU, auditoria): equalizacao de massa por linha entre eq_sink_v e
  eq_ctrl_v para v em {atten_b0, atten_b025, const_rm}. Nao sobrescreve
  out/phase22_sink_evolution.json nem out/pairs/phase22_abl_* / phase22_ckpt_*.

Uso:
  flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase22_sink_evolution.py --part-a
  OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase22_sink_evolution.py --part-b
  OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase22_sink_evolution.py --part-b2
"""
import os
for _key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "4"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from sampling import (MODELS, DATA_ROOT, slug, sample_paths, validate_matrices,
                      storage_row_atol, load_sample, sha256_file, prepare_corpus)
import argparse
from concurrent.futures import ProcessPoolExecutor
import gc
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AttentionInterface
from extract_attn import capture_attention, set_attention, CAPTURE
from phase0_radon_attention import radon_support_fraction, make_controls
from phase06_profiled_lines import omp_profiled, precompute_band_norms
from phase24_p0_metrics import describe, svd_relative_error

CKPT_MODEL = "EleutherAI/pythia-410m"
REVISIONS = ["step0", "step1000", "step4000", "step16000", "step64000", "step143000"]
N = 128
K_LINE = 8
N_CONTROLS = 40
CONTROL_SEED = [0, N, 331]
CKPT_DIR = Path("data/attn_ckpt")
OUT_JSON = Path("out/phase22_sink_evolution.json")
PAIRS_DIR = Path("out/pairs")
LOG_PATH = Path("out/_rerun_logs/e5_progress.md")
SANITY_ATOL = 1e-3
VARIANTS = ["orig", "atten_b0", "atten_b025", "const_rm",
            "ctrl_atten_b0", "ctrl_atten_b025", "ctrl_const_rm"]
BETAS = {"atten_b0": 0.0, "atten_b025": 0.25}
# Parte B2 (auditoria): nao altera VARIANTS/BETAS acima.
EQ_BASE = ["atten_b0", "atten_b025", "const_rm"]
EQ_VARIANTS = ["orig"] + [f"eq_sink_{v}" for v in EQ_BASE] + [f"eq_ctrl_{v}" for v in EQ_BASE]
OUT_EQ_JSON = Path("out/phase22_sink_equalized.json")
EQ_PAIRS_PREFIX = "phase22_eq_"
EQ_MASS_TOL = 1e-12
EQ_ROW_TOL = 1e-12


def log(stage, message, seconds=None):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"\n- {stamp} | {stage}: {message}")
        if seconds is not None:
            f.write(f" | elapsed_seconds={seconds:.3f}")
        f.write("\n")


def ckpt_npz_path(rev):
    return CKPT_DIR / f"pythia-410m_{rev}_n{N}.npz"


def sink_mass_of(a):
    return float(a[1:, 0].mean())


def sink_frac_of_column_effect(a):
    mu = a.mean()
    c = a.mean(axis=0)
    cc = c - mu
    return float(cc[0] ** 2 / np.dot(cc, cc))


def base_metrics(a, theta, norms):
    support = radon_support_fraction(a, theta)[0]
    prof, _ = omp_profiled(a, K_LINE, N, {K_LINE}, norms)
    return float(support), float(prof[K_LINE]), float(svd_relative_error(a, K_LINE))


def renormalize_changed(b, changed):
    for i in np.flatnonzero(changed):
        s = b[i].sum()
        if not np.isfinite(s) or s < 0:
            raise ValueError(f"Cannot renormalize row {i}: sum={s}")
        if s == 0.0:
            continue  # whole row mass was sink and got removed; stays exactly zero
        b[i] /= s
    return b


def validate_ablated(stack, atol, where):
    if not np.isfinite(stack).all():
        raise ValueError(f"Nonfinite ablated values at {where}")
    if (stack < 0).any():
        raise ValueError(f"Negative ablated values at {where}")
    if np.count_nonzero(np.triu(stack, 1)) > 0:
        raise ValueError(f"Non-causal ablated values at {where}")
    sums = stack.sum(-1)
    allzero = (stack == 0).all(-1)
    ok = allzero | (np.abs(sums - 1) <= atol)
    if not bool(ok.all()):
        bad = np.argwhere(~ok)
        raise ValueError(f"Ablated rows neither normalized nor empty at {where}: {bad[:8].tolist()}")
    return {"n_matrices": stack.shape[0], "n_empty_rows": int(allzero.sum())}


def atten_variant(a, beta):
    n = a.shape[0]
    b = a.copy()
    b[1:, 0] = beta * b[1:, 0]
    removed = np.zeros(n)
    removed[1:] = a[1:, 0] - b[1:, 0]
    changed = removed != 0.0
    changed[0] = False
    return renormalize_changed(b, changed), removed


def const_rm_variant(a):
    n = a.shape[0]
    b = a.copy()
    c0 = float(a[1:, 0].mean())
    b[1:, 0] = np.maximum(b[1:, 0] - c0, 0.0)
    removed = np.zeros(n)
    removed[1:] = a[1:, 0] - b[1:, 0]
    clipped = float(np.maximum(c0 - a[1:, 0], 0.0).sum())
    changed = removed != 0.0
    changed[0] = False
    return renormalize_changed(b, changed), removed, c0, clipped


def control_variant(a, removed, rng):
    n = a.shape[0]
    b = a.copy()
    taken = np.zeros(n)
    for i in range(1, n):
        m = float(removed[i])
        if m == 0.0:
            continue
        if m < 0.0:
            raise ValueError(f"Negative removed mass at row {i}: {m}")
        perm = rng.permutation(np.arange(1, i + 1))
        rem = m
        for j in perm:
            avail = float(b[i, int(j)])
            if avail < 0.0:
                raise ValueError(f"Negative attention value at ({i},{j})")
            take = avail if avail < rem else rem
            b[i, int(j)] = avail - take
            rem -= take
            if rem <= 0.0:
                break
        taken[i] = m - rem
    total = float(removed[1:].sum())
    matched = float(taken[1:].sum() / total) if total > 0.0 else 1.0
    return renormalize_changed(b, taken > 0.0), matched, taken


def check_beta1_identity(a):
    b, _ = atten_variant(a, 1.0)
    return float(np.abs(b - a).max())


def eq_removed_mass(a, base_v):
    """Massa pre-renormalizacao que a variante base tira do sink (mesmo que parte B).

    Reusa atten_variant/const_rm_variant para garantir m_i identico ao controle
    de massa casada atual. Retorna (removed, c0_ou_None, clipped_ou_None).
    """
    if base_v == "atten_b0":
        _, removed = atten_variant(a, BETAS["atten_b0"])[:2]
        return removed, None, None
    if base_v == "atten_b025":
        _, removed = atten_variant(a, BETAS["atten_b025"])[:2]
        return removed, None, None
    if base_v == "const_rm":
        _, removed, c0, clipped = const_rm_variant(a)
        return removed, c0, clipped
    raise ValueError(f"base variant desconhecida: {base_v}")


def eq_q_vector(a, removed):
    """q_i = min(m_i, soma de A[i,j] para j em 1..i), i>=1; q_0 = 0."""
    n = a.shape[0]
    q = np.zeros(n)
    for i in range(1, n):
        nonsink = float(a[i, 1:i + 1].sum())
        m = float(removed[i])
        q[i] = m if m < nonsink else nonsink
    return q


def eq_sink_build(a, q):
    """Tira exatamente q_i do sink; linha 0 intacta. Retorna (b_pre, b_pos)."""
    b_pre = a.copy()
    b_pre[1:, 0] -= q[1:]
    if (b_pre[1:, 0] < -1e-15).any():
        raise ValueError("eq_sink deixou sink negativo")
    changed = q != 0.0
    changed[0] = False
    b_pos = renormalize_changed(b_pre.copy(), changed)
    return b_pre, b_pos, changed


def renormalize_changed_unif(b, changed):
    """Sensibilidade: linhas zeradas viram uniforme em 1..i; resto renormaliza."""
    for i in np.flatnonzero(changed):
        s = b[i].sum()
        if not np.isfinite(s) or s < 0:
            raise ValueError(f"Cannot renormalize row {i}: sum={s}")
        if s == 0.0:
            if i == 0:
                raise ValueError("Linha 0 zerada na sensibilidade uniforme")
            b[i, 1:i + 1] = 1.0 / float(i)
        else:
            b[i] /= s
    return b


def eq_sanity_instance(a, q_by_base, sink_pre_by_base, sink_pos_by_base,
                       ctrl_taken_by_base, ctrl_pos_by_base):
    """Sanidade por instancia: soma das linhas, linha 0, massa removida == q.

    Retorna dict com contagens de linhas zeradas e erros maximos observados.
    Levanta ValueError se qualquer tolerancia (1e-12) for violada.
    """
    n = a.shape[0]
    if not np.array_equal(sink_pos_by_base[EQ_BASE[0]][0], a[0]):
        pass  # checagem explicita abaixo por braco
    errs = {}
    zero_counts = {}
    for v in EQ_BASE:
        q = q_by_base[v]
        b_pre_s, b_s = sink_pre_by_base[v], sink_pos_by_base[v]
        taken_c, b_c = ctrl_taken_by_base[v], ctrl_pos_by_base[v]
        # linha 0 intacta (exata: nao tocamos na linha 0)
        if float(np.abs(b_s[0] - a[0]).max()) != 0.0:
            raise ValueError(f"eq_sink_{v}: linha 0 alterada")
        if float(np.abs(b_c[0] - a[0]).max()) != 0.0:
            raise ValueError(f"eq_ctrl_{v}: linha 0 alterada")
        # massa tirada do sink == q
        e_sink = float(np.abs((a[1:, 0] - b_pre_s[1:, 0]) - q[1:]).max()) if n > 1 else 0.0
        # massa tirada do nao-sink == q (taken retornado pelo mesmo procedimento do controle atual)
        e_ctrl = float(np.abs(taken_c - q).max())
        if not (e_sink <= EQ_MASS_TOL):
            raise ValueError(f"eq_sink_{v}: massa != q (err={e_sink})")
        if not (e_ctrl <= EQ_MASS_TOL):
            raise ValueError(f"eq_ctrl_{v}: massa != q (err={e_ctrl})")
        errs[v] = {"sink_mass_err": e_sink, "ctrl_mass_err": e_ctrl}
        # soma das linhas: linhas alteradas (q_i>0) renormalizadas em float64
        # devem somar 1 com erro <= 1e-12; linhas intactas (q_i==0) herdam o
        # erro fp16 do arquivo e usam storage_row_atol(N); zeradas sao contadas.
        store_atol = float(storage_row_atol(n))
        for name, b in (("sink", b_s), ("ctrl", b_c)):
            sums = b.sum(-1)
            allzero = (b == 0).all(-1)
            changed_mask = q != 0.0
            changed_mask[0] = False
            tol = np.where(changed_mask, EQ_ROW_TOL, store_atol)
            ok = allzero | (np.abs(sums - 1) <= tol)
            if bool((~ok).any()):
                idx = np.argwhere(~ok)[:8].ravel().tolist()
                raise ValueError(f"eq_{name}_{v}: linhas nem normalizadas nem vazias: {idx}")
            key = f"eq_{name}_{v}"
            zero_counts[key] = int(allzero.sum())
    return {"mass_errs": errs, "zero_rows_primary": zero_counts}


def eq_wilcoxon_signed_rank(x):
    """Wilcoxon signed-rank bicaudal sobre medianas por documento + rank-biserial.

   Zeros sao descartados (zero_method='wilcox'), method='auto'.
    rank-biserial de Kerby (simple difference): r = (T+ - T-)/(T+ + T-),
    com ranks medios em empates. Retorna dict serializavel.
    """
    from scipy.stats import wilcoxon, rankdata
    x = np.asarray(x, dtype=np.float64)
    n_docs = int(x.size)
    nz = x[x != 0.0]
    n_eff = int(nz.size)
    if n_eff == 0:
        return {"n_docs": n_docs, "n_eff": 0, "statistic": 0.0, "p_value": 1.0,
                "rank_biserial_kerby": 0.0, "T_plus": 0.0, "T_minus": 0.0,
                "zero_method": "wilcox", "method": "auto", "alternative": "two-sided"}
    ranks = rankdata(np.abs(nz), method="average")
    t_plus = float(ranks[nz > 0].sum())
    t_minus = float(ranks[nz < 0].sum())
    denom = t_plus + t_minus
    r_rb = float((t_plus - t_minus) / denom) if denom > 0 else 0.0
    res = wilcoxon(x, zero_method="wilcox", alternative="two-sided", method="auto")
    return {"n_docs": n_docs, "n_eff": n_eff, "statistic": float(res.statistic),
            "p_value": float(res.pvalue), "rank_biserial_kerby": r_rb,
            "T_plus": t_plus, "T_minus": t_minus,
            "zero_method": "wilcox", "method": "auto", "alternative": "two-sided"}


def extract_revision(rev, ids, instances, n_layers, n_matrices):
    target = ckpt_npz_path(rev)
    if target.exists():
        with np.load(target, allow_pickle=False) as z:
            avail = z["attention"]
            if avail.shape != (n_matrices, N, N) or avail.dtype != np.float16:
                raise RuntimeError(f"Existing checkpoint archive has wrong shape/dtype: {target}")
            check = validate_matrices(avail, storage_row_atol(N))
        if check["invalid_matrices"]:
            raise RuntimeError(f"Existing checkpoint archive invalid: {target}: {check}")
        log("E5 extract", f"{rev} already present and valid; skipping forward pass")
        return {"revision": rev, "skipped": True, "path": target.as_posix()}
    t0 = time.perf_counter()
    model = AutoModelForCausalLM.from_pretrained(
        CKPT_MODEL, revision=rev, local_files_only=True,
        attn_implementation="eager", dtype=torch.float32).to("cuda").eval()
    selection = {(di, layer): [] for di in range(ids.shape[0]) for layer in range(n_layers)}
    for oi, item in enumerate(instances):
        selection[item["document_index"], item["layer"]].append((oi, item["head"]))
    sample = np.empty((n_matrices, N, N), dtype=np.float16)
    ref = model(ids[:1].to("cuda"), use_cache=False, logits_to_keep=1).logits[:, -1].float().cpu()
    CAPTURE.update({"selected": selection, "output": sample, "checks": []})
    AttentionInterface.register("p0_capture", capture_attention)
    set_attention(model, "p0_capture")
    for s in range(ids.shape[0]):
        CAPTURE["layer"], CAPTURE["batch_start"] = 0, s
        out = model(ids[s:s + 1].to("cuda"), use_cache=False, logits_to_keep=1)
        if CAPTURE["layer"] != n_layers:
            raise RuntimeError(f"Attention calls {CAPTURE['layer']} != layers {n_layers}")
        if s == 0:
            got = out.logits[:, -1].float().cpu()
            if not torch.equal(ref, got):
                raise RuntimeError("Capture changed vanilla eager logits for " + rev)
        if (s + 1) % 16 == 0:
            print(f"E5 extract {rev}: {s + 1}/{ids.shape[0]} documents", flush=True)
    source_invalid = sum(c["invalid_matrices"] for c in CAPTURE["checks"])
    check = validate_matrices(sample, storage_row_atol(N))
    if source_invalid or check["invalid_matrices"]:
        raise RuntimeError(f"Invalid extraction for {rev}: source={source_invalid} archive={check}")
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = CKPT_DIR / f"e5_partial_pythia-410m_{rev}_n{N}.npz"
    if tmp.exists():
        raise RuntimeError(f"Stale partial file present, inspect before rerun: {tmp}")
    with np.load(sample_paths(CKPT_MODEL, N)[0], allow_pickle=False) as z:
        input_ids, next_tokens = z["input_ids"], z["next_token_ids"]
        doc_idx = np.array([x["document_index"] for x in instances], dtype=np.int32)
        layer_a = np.array([x["layer"] for x in instances], dtype=np.int16)
        head_a = np.array([x["head"] for x in instances], dtype=np.int16)
    np.savez_compressed(tmp, attention=sample, input_ids=input_ids, next_token_ids=next_tokens,
                        document_index=doc_idx, layer=layer_a, head=head_a)
    tmp.rename(target)
    del model, sample, ref, out
    CAPTURE["output"] = None
    gc.collect()
    torch.cuda.empty_cache()
    secs = time.perf_counter() - t0
    log("E5 extract", f"{rev}: {n_matrices} matrices from {ids.shape[0]} documents; all checks passed", secs)
    return {"revision": rev, "skipped": False, "path": target.as_posix(),
            "elapsed_seconds": secs, "max_row_sum_abs_error": check["max_row_sum_abs_error"]}


def run_part_a():
    t0 = time.perf_counter()
    base_npz = DATA_ROOT / f"{slug(CKPT_MODEL)}_n{N}.npz"
    with np.load(base_npz, allow_pickle=False) as z:
        attention0 = z["attention"]
        ids = torch.tensor(z["input_ids"], dtype=torch.long)
    manifest = json.loads(sample_paths(CKPT_MODEL, N)[1].read_text(encoding="utf-8"))
    instances = manifest["instances"]
    n_layers = manifest["n_layers"]
    if attention0.shape != (len(instances), N, N) or attention0.dtype != np.float16:
        raise RuntimeError("Base archive does not match its manifest")
    corpus = prepare_corpus()
    cfg = corpus["models"][CKPT_MODEL]
    corpus_ids = np.array([x["token_ids"][:N] for x in cfg["documents"][:64]], dtype=np.int64)
    if not np.array_equal(np.asarray(ids), corpus_ids):
        raise RuntimeError("Base archive input_ids differ from corpus manifest windows")
    for rev in REVISIONS:
        extract_revision(rev, ids, instances, n_layers, len(instances))
    with np.load(ckpt_npz_path("step143000"), allow_pickle=False) as z:
        attention_final = z["attention"]
    maxdiff = float(np.abs(attention_final.astype(np.float64)
                           - attention0.astype(np.float64)).max())
    sanity_pass = maxdiff <= SANITY_ATOL
    log("E5 sanity A", f"step143000 vs data/attn archive: max_abs_diff={maxdiff:.6g} "
        f"(tol={SANITY_ATOL}); pass={sanity_pass}")
    print(f"E5 sanity A: max_abs_diff={maxdiff:.6g} pass={sanity_pass}", flush=True)
    if not sanity_pass:
        raise RuntimeError(f" Refusing to continue: {maxdiff}")
    theta = np.arange(0.0, 180.0, 2.0)
    norms = precompute_band_norms(N)
    _, randoms = make_controls(N, N_CONTROLS, np.random.default_rng(np.random.SeedSequence(CONTROL_SEED)))
    random_median = float(np.median([radon_support_fraction(a, theta)[0] for a in randoms]))
    docs = [x["document_index"] for x in instances]
    part = {}
    for rev in REVISIONS:
        with np.load(ckpt_npz_path(rev), allow_pickle=False) as z:
            att = z["attention"]
        pairs_path = PAIRS_DIR / f"phase22_ckpt_{rev}_n{N}.jsonl"
        if pairs_path.exists():
            raise RuntimeError(f"Unfinished prior pairs file, inspect before rerun: {pairs_path}")
        rows = []
        PAIRS_DIR.mkdir(parents=True, exist_ok=True)
        with pairs_path.open("x", encoding="utf-8") as out:
            for oi, raw in enumerate(att):
                a = raw.astype(np.float64)
                norm = np.linalg.norm(a)
                if not np.isfinite(a).all() or norm <= 0:
                    raise ValueError(f"Invalid instance {oi} in {rev}")
                support, line_k8, svd_k8 = base_metrics(a, theta, norms)
                row = {k: instances[oi][k] for k in
                       ("instance_id", "document_index", "doc_id", "layer", "head", "offset", "n")}
                row.update({"sink_mass": sink_mass_of(a), "radon_support": support,
                            "profiled_line_k8_relative_error": line_k8,
                            "svd_k8_relative_error": svd_k8,
                            "sink_frac_of_column_effect_energy": sink_frac_of_column_effect(a)})
                out.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                rows.append(row)
        metrics = {k: describe([r[k] for r in rows], docs) for k in
                   ("sink_mass", "radon_support", "profiled_line_k8_relative_error",
                    "svd_k8_relative_error", "sink_frac_of_column_effect_energy")}
        part[rev] = {"ckpt_path": ckpt_npz_path(rev).as_posix(), "n_instances": len(rows),
                     "n_documents": len(set(docs)), "metrics": metrics,
                     "random_support_median": random_median,
                     "concentration_real_to_random_ratio":
                         metrics["radon_support"]["median"] / random_median,
                     "pairs_path": pairs_path.as_posix(), "pairs_sha256": sha256_file(pairs_path)}
        print(f"E5 metrics {rev}: sink_mass={metrics['sink_mass']['median']:.4f} "
              f"ratio={part[rev]['concentration_real_to_random_ratio']:.4f}", flush=True)
    secs = time.perf_counter() - t0
    log("E5 part A complete", f"{len(REVISIONS)} revisions, random_median={random_median:.6f}", secs)
    return part, {"max_abs_diff": maxdiff, "tol": SANITY_ATOL, "pass": sanity_pass}, random_median, secs


def run_part_b_model(model):
    t0 = time.perf_counter()
    theta = np.arange(0.0, 180.0, 2.0)
    norms = precompute_band_norms(N)
    _, randoms = make_controls(N, N_CONTROLS, np.random.default_rng(np.random.SeedSequence(CONTROL_SEED)))
    random_median = float(np.median([radon_support_fraction(a, theta)[0] for a in randoms]))
    attention, manifest = load_sample(model, N)
    instances = manifest["instances"]
    docs = [x["document_index"] for x in instances]
    pairs_path = PAIRS_DIR / f"phase22_abl_{slug(model)}_n{N}.jsonl"
    PAIRS_DIR.mkdir(parents=True, exist_ok=True)
    by_variant = {v: {"radon_support": [], "line_k8": [], "svd_k8": []} for v in VARIANTS}
    matched = {"ctrl_atten_b0": [], "ctrl_atten_b025": [], "ctrl_const_rm": []}
    clipped = []
    zero_rows = {v: [] for v in VARIANTS}
    n_done = 0
    if pairs_path.exists():
        stored = [json.loads(line) for line in
                  pairs_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(stored) != len(instances) or any(
                s.get("instance_id") != instances[k]["instance_id"]
                for k, s in enumerate(stored)):
            raise RuntimeError(f"Unfinished prior pairs file, inspect before rerun: {pairs_path}")
        for s in stored:
            for v in VARIANTS:
                for k in ("radon_support", "line_k8", "svd_k8"):
                    by_variant[v][k].append(s["variants"][v][k])
            for c in matched:
                matched[c].append(s["control_matched_fraction"][c])
            clipped.append(s["const_rm_clipped_mass"])
            zr = s.get("zero_rows") or {}
            for v in VARIANTS:
                zero_rows[v].append(int(zr.get(v, 0)))
            n_done += 1
        log("E5 ablate", f"{model} n={N}: resumed {len(stored)} stored instances, no recompute")
    else:
        with pairs_path.open("x", encoding="utf-8") as out:
            for oi, raw in enumerate(attention):
                a = raw.astype(np.float64)
                norm = np.linalg.norm(a)
                if not np.isfinite(a).all() or norm <= 0:
                    raise ValueError(f"Invalid instance {oi} in {model}")
                built = {}
                built["orig"] = a
                built["atten_b0"], rem_b0 = atten_variant(a, BETAS["atten_b0"])[:2]
                built["atten_b025"], rem_b025 = atten_variant(a, BETAS["atten_b025"])[:2]
                built["const_rm"], rem_c, c0, clip = const_rm_variant(a)
                built["ctrl_atten_b0"], m_b0, _ = control_variant(
                    a, rem_b0, np.random.default_rng([oi, 7]))
                built["ctrl_atten_b025"], m_b025, _ = control_variant(
                    a, rem_b025, np.random.default_rng([oi, 7]))
                built["ctrl_const_rm"], m_cc, _ = control_variant(
                    a, rem_c, np.random.default_rng([oi, 7]))
                vcheck = validate_ablated(np.stack([built[v] for v in VARIANTS]),
                                          storage_row_atol(N), f"{model} instance {oi}")
                if vcheck["n_matrices"] != len(VARIANTS):
                    raise RuntimeError(f"Ablated stack shape wrong at {model} instance {oi}")
                vmets, zr = {}, {}
                for v in VARIANTS:
                    support, line_k8, svd_k8 = base_metrics(built[v], theta, norms)
                    vmets[v] = {"radon_support": support, "line_k8": line_k8, "svd_k8": svd_k8}
                    by_variant[v]["radon_support"].append(support)
                    by_variant[v]["line_k8"].append(line_k8)
                    by_variant[v]["svd_k8"].append(svd_k8)
                    zr[v] = int((built[v] == 0).all(axis=-1).sum())
                    zero_rows[v].append(zr[v])
                matched["ctrl_atten_b0"].append(m_b0)
                matched["ctrl_atten_b025"].append(m_b025)
                matched["ctrl_const_rm"].append(m_cc)
                clipped.append(clip)
                row = {k: instances[oi][k] for k in
                       ("instance_id", "document_index", "doc_id", "layer", "head", "offset", "n")}
                row.update({"variants": vmets, "const_rm_c0": c0, "const_rm_clipped_mass": clip,
                            "control_matched_fraction":
                                {"ctrl_atten_b0": m_b0, "ctrl_atten_b025": m_b025,
                                 "ctrl_const_rm": m_cc},
                            "zero_rows": zr})
                out.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                n_done += 1
                if n_done % 256 == 0:
                    out.flush()
                    print(f"E5 ablate {model}: {n_done}/{len(instances)}", flush=True)
    summary = {}
    for v in VARIANTS:
        entry = {"metrics": {k: describe(by_variant[v][k], docs) for k in
                             ("radon_support", "line_k8", "svd_k8")},
                 "concentration_real_to_random_ratio":
                     float(np.median(by_variant[v]["radon_support"]) / random_median),
                 "matched_fraction": None, "clipped_mass": None,
                 "n_zero_rows_total": int(np.sum(zero_rows[v])),
                 "n_instances_with_zero_rows": int(np.count_nonzero(zero_rows[v]))}
        if v in matched:
            entry["matched_fraction"] = describe(matched[v], docs)
        if v == "const_rm":
            entry["clipped_mass"] = describe(clipped, docs)
        summary[v] = entry
    secs = time.perf_counter() - t0
    log("E5 ablate", f"{model} n={N}: {n_done} instances x {len(VARIANTS)} variants", secs)
    return {"model": model, "n_instances": n_done, "n_documents": len(set(docs)),
            "random_support_median": random_median, "variants": summary,
            "pairs_path": pairs_path.as_posix(), "pairs_sha256": sha256_file(pairs_path),
            "elapsed_seconds": secs}


def run_part_b():
    t0 = time.perf_counter()
    attention, _ = load_sample(CKPT_MODEL, N)
    worst = 0.0
    for oi in (0, len(attention) // 2, len(attention) - 1):
        worst = max(worst, check_beta1_identity(attention[oi].astype(np.float64)))
    log("E5 sanity B", f"atten beta=1 vs orig: max_abs_diff={worst:.6g} over 3 instances; "
        f"pass={worst == 0.0}")
    print(f"E5 sanity B: beta1 max_abs_diff={worst:.6g} pass={worst == 0.0}", flush=True)
    if worst != 0.0:
        raise RuntimeError(f"Refusing to continue: {worst}")
    del attention
    gc.collect()
    with ProcessPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run_part_b_model, MODELS))
    secs = time.perf_counter() - t0
    log("E5 part B complete", f"{len(results)} models", secs)
    sanity = {"beta1_max_abs_diff": worst, "pass": True}
    return {r["model"]: r for r in results}, sanity, secs


def eq_pairs_path(model):
    return PAIRS_DIR / f"{EQ_PAIRS_PREFIX}{slug(model)}_n{N}.jsonl"


def run_part_b2_model(model):
    t0 = time.perf_counter()
    theta = np.arange(0.0, 180.0, 2.0)
    norms = precompute_band_norms(N)
    _, randoms = make_controls(N, N_CONTROLS, np.random.default_rng(np.random.SeedSequence(CONTROL_SEED)))
    random_median = float(np.median([radon_support_fraction(a, theta)[0] for a in randoms]))
    attention, manifest = load_sample(model, N)
    instances = manifest["instances"]
    docs = [x["document_index"] for x in instances]
    pairs_path = eq_pairs_path(model)
    PAIRS_DIR.mkdir(parents=True, exist_ok=True)
    by_variant = {v: {"radon_support": [], "line_k8": [], "svd_k8": []} for v in EQ_VARIANTS}
    by_unif = {v: {"radon_support": [], "line_k8": [], "svd_k8": []}
               for v in EQ_VARIANTS if v != "orig"}
    zero_rows = {v: [] for v in EQ_VARIANTS}
    # linhas redistribuidas na sensibilidade uniforme (por instancia, por variante eq)
    redist_rows = {v: [] for v in EQ_VARIANTS if v != "orig"}
    qsum = {v: [] for v in EQ_BASE}
    max_sink_err = 0.0
    max_ctrl_err = 0.0
    n_done = 0
    if pairs_path.exists():
        stored = [json.loads(line) for line in
                  pairs_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(stored) != len(instances) or any(
                s.get("instance_id") != instances[k]["instance_id"]
                for k, s in enumerate(stored)):
            raise RuntimeError(f"Unfinished prior pairs file, inspect before rerun: {pairs_path}")
        for s in stored:
            for v in EQ_VARIANTS:
                for k in ("radon_support", "line_k8", "svd_k8"):
                    by_variant[v][k].append(s["variants"][v][k])
            zr = s.get("zero_rows") or {}
            for v in EQ_VARIANTS:
                zero_rows[v].append(int(zr.get(v, 0)))
            zu = s.get("zero_rows_unif") or s.get("redistributed_rows") or {}
            for v in by_unif:
                uv = (s.get("variants_unif") or {}).get(v)
                if uv is None:
                    for k in ("radon_support", "line_k8", "svd_k8"):
                        by_unif[v][k].append(by_variant[v][k][len(by_unif[v][k])])
                else:
                    for k in ("radon_support", "line_k8", "svd_k8"):
                        by_unif[v][k].append(uv[k])
                redist_rows[v].append(int(zu.get(v, zr.get(v, 0))))
            for v in EQ_BASE:
                qsum[v].append(float(s["eq_q_sum"][v]))
            me = s.get("mass_errs") or {}
            for v in EQ_BASE:
                if v in me:
                    max_sink_err = max(max_sink_err, float(me[v].get("sink_mass_err", 0.0)))
                    max_ctrl_err = max(max_ctrl_err, float(me[v].get("ctrl_mass_err", 0.0)))
            n_done += 1
        log("E5B2 ablate", f"{model} n={N}: resumed {len(stored)} stored instances, no recompute")
    else:
        with pairs_path.open("x", encoding="utf-8") as out:
            for oi, raw in enumerate(attention):
                a = raw.astype(np.float64)
                norm = np.linalg.norm(a)
                if not np.isfinite(a).all() or norm <= 0:
                    raise ValueError(f"Invalid instance {oi} in {model}")
                q_by, sink_pre, sink_pos, ctrl_taken, ctrl_pos = {}, {}, {}, {}, {}
                for v in EQ_BASE:
                    removed, _, _ = eq_removed_mass(a, v)
                    q = eq_q_vector(a, removed)
                    q_by[v] = q
                    b_pre_s, b_s, _ = eq_sink_build(a, q)
                    sink_pre[v] = b_pre_s
                    sink_pos[v] = b_s
                    b_c, _, taken_c = control_variant(a, q, np.random.default_rng([oi, 7]))
                    ctrl_taken[v] = taken_c
                    ctrl_pos[v] = b_c
                san = eq_sanity_instance(a, q_by, sink_pre, sink_pos, ctrl_taken, ctrl_pos)
                for v in EQ_BASE:
                    max_sink_err = max(max_sink_err, san["mass_errs"][v]["sink_mass_err"])
                    max_ctrl_err = max(max_ctrl_err, san["mass_errs"][v]["ctrl_mass_err"])
                    qsum[v].append(float(q_by[v][1:].sum()))
                built = {"orig": a}
                for v in EQ_BASE:
                    built[f"eq_sink_{v}"] = sink_pos[v]
                    built[f"eq_ctrl_{v}"] = ctrl_pos[v]
                vcheck = validate_ablated(np.stack([built[v] for v in EQ_VARIANTS]),
                                          storage_row_atol(N), f"{model} B2 instance {oi}")
                if vcheck["n_matrices"] != len(EQ_VARIANTS):
                    raise RuntimeError(f"Ablated stack shape wrong at {model} B2 instance {oi}")
                vmets, zr, umets, zu = {}, {}, {}, {}
                for v in EQ_VARIANTS:
                    support, line_k8, svd_k8 = base_metrics(built[v], theta, norms)
                    vmets[v] = {"radon_support": support, "line_k8": line_k8, "svd_k8": svd_k8}
                    by_variant[v]["radon_support"].append(support)
                    by_variant[v]["line_k8"].append(line_k8)
                    by_variant[v]["svd_k8"].append(svd_k8)
                    zc = int((built[v] == 0).all(axis=-1).sum())
                    zr[v] = zc
                    zero_rows[v].append(zc)
                # sensibilidade uniforme: so difere se houver linha zerada; caso contrario, identica
                for v in EQ_VARIANTS:
                    if v == "orig":
                        continue
                    zc = zr[v]
                    zu[v] = zc
                    redist_rows[v].append(zc)
                    if zc == 0:
                        umets[v] = vmets[v]
                        for k in ("radon_support", "line_k8", "svd_k8"):
                            by_unif[v][k].append(vmets[v][k])
                    else:
                        b_unif = built[v].copy()
                        zmask = (b_unif == 0).all(axis=-1)
                        for i in np.flatnonzero(zmask):
                            b_unif[i, 1:i + 1] = 1.0 / float(i)
                        base_v = v.split("_", 2)[2] if v.startswith("eq_sink_") else v.split("_", 2)[2]
                        qq = q_by[base_v]
                        chm = qq != 0.0
                        chm[0] = False
                        chm = chm | zmask
                        tol_u = np.where(chm, EQ_ROW_TOL, float(storage_row_atol(N)))
                        sums_u = b_unif.sum(-1)
                        if bool(((np.abs(sums_u - 1) <= tol_u)).all()) is False:
                            raise ValueError(f"unif rows not normalized at {model} instance {oi} {v}")
                        support_u, line_u, svd_u = base_metrics(b_unif, theta, norms)
                        umets[v] = {"radon_support": support_u, "line_k8": line_u, "svd_k8": svd_u}
                        for k, val in (("radon_support", support_u), ("line_k8", line_u),
                                        ("svd_k8", svd_u)):
                            by_unif[v][k].append(val)
                row = {k: instances[oi][k] for k in
                       ("instance_id", "document_index", "doc_id", "layer", "head", "offset", "n")}
                row.update({"variants": vmets, "variants_unif": umets,
                            "zero_rows": zr, "zero_rows_unif": zu,
                            "eq_q_sum": {v: float(q_by[v][1:].sum()) for v in EQ_BASE},
                            "mass_errs": san["mass_errs"]})
                out.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                n_done += 1
                if n_done % 256 == 0:
                    out.flush()
                    print(f"E5B2 ablate {model}: {n_done}/{len(instances)}", flush=True)
    summary = {}
    for v in EQ_VARIANTS:
        entry = {"metrics": {k: describe(by_variant[v][k], docs) for k in
                             ("radon_support", "line_k8", "svd_k8")},
                 "concentration_real_to_random_ratio":
                     float(np.median(by_variant[v]["radon_support"]) / random_median),
                 "n_zero_rows_total": int(np.sum(zero_rows[v])),
                 "n_instances_with_zero_rows": int(np.count_nonzero(zero_rows[v]))}
        if v != "orig":
            entry["metrics_unif_sensitivity"] = {
                k: describe(by_unif[v][k], docs) for k in ("radon_support", "line_k8", "svd_k8")}
            entry["concentration_real_to_random_ratio_unif"] = float(
                np.median(by_unif[v]["radon_support"]) / random_median)
            entry["n_redistributed_rows_unif_total"] = int(np.sum(redist_rows[v]))
            entry["n_instances_redistributed_unif"] = int(np.count_nonzero(redist_rows[v]))
        summary[v] = entry
    paired = {}
    uniq_docs = sorted(set(docs))
    doc_arr = np.asarray(docs)
    for v in EQ_BASE:
        sk, ck = f"eq_sink_{v}", f"eq_ctrl_{v}"
        d_sup = (np.asarray(by_variant[sk]["radon_support"])
                 - np.asarray(by_variant[ck]["radon_support"]))
        d_line = (np.asarray(by_variant[sk]["line_k8"])
                  - np.asarray(by_variant[ck]["line_k8"]))
        med_sup_doc = np.array([float(np.median(d_sup[doc_arr == d])) for d in uniq_docs])
        med_line_doc = np.array([float(np.median(d_line[doc_arr == d])) for d in uniq_docs])
        paired[v] = {
            "support_diff_eq_sink_minus_eq_ctrl": {
                "describe": describe(d_sup.tolist(), docs),
                "doc_medians": med_sup_doc.tolist(),
                "wilcoxon_signed_rank_over_doc_medians": eq_wilcoxon_signed_rank(med_sup_doc)},
            "line_k8_diff_eq_sink_minus_eq_ctrl": {
                "describe": describe(d_line.tolist(), docs),
                "doc_medians": med_line_doc.tolist(),
                "wilcoxon_signed_rank_over_doc_medians": eq_wilcoxon_signed_rank(med_line_doc)}}
    secs = time.perf_counter() - t0
    log("E5B2 ablate", f"{model} n={N}: {n_done} instances x {len(EQ_VARIANTS)} variants", secs)
    return {"model": model, "n_instances": n_done, "n_documents": len(set(docs)),
            "random_support_median": random_median, "variants": summary,
            "paired": paired,
            "eq_q_sum": {v: describe(qsum[v], docs) for v in EQ_BASE},
            "sanity": {"mass_tol": EQ_MASS_TOL, "row_tol": EQ_ROW_TOL,
                       "max_sink_mass_err": max_sink_err, "max_ctrl_mass_err": max_ctrl_err,
                       "pass": bool(max_sink_err <= EQ_MASS_TOL and max_ctrl_err <= EQ_MASS_TOL)},
            "pairs_path": pairs_path.as_posix(), "pairs_sha256": sha256_file(pairs_path),
            "elapsed_seconds": secs}


def run_part_b2():
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run_part_b2_model, MODELS))
    secs = time.perf_counter() - t0
    log("E5B2 part complete", f"{len(results)} models", secs)
    part = {r["model"]: r for r in results}
    sanity = {"pass": all(r["sanity"]["pass"] for r in results),
              "max_sink_mass_err": max(r["sanity"]["max_sink_mass_err"] for r in results),
              "max_ctrl_mass_err": max(r["sanity"]["max_ctrl_mass_err"] for r in results)}
    return part, sanity, secs


PARTIAL_A = Path("e5_part_a.json")
PARTIAL_B = Path("e5_part_b.json")


def write_partial(path, payload):
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite existing partial output, inspect first: {path}")
    with path.open("x", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")


def merge_partials():
    if OUT_JSON.exists():
        raise RuntimeError(f"Refusing to overwrite existing output, inspect first: {OUT_JSON}")
    a = json.loads(PARTIAL_A.read_text(encoding="utf-8"))
    b = json.loads(PARTIAL_B.read_text(encoding="utf-8"))
    result = {"experiment": "E5 sink contribution to Radon concentration",
              "n": N, "k_line": K_LINE, "theta_degrees": np.arange(0.0, 180.0, 2.0).tolist(),
              "random_controls": {"n_controls": N_CONTROLS, "seed": CONTROL_SEED},
              "ckpt_model": CKPT_MODEL, "ckpt_revisions": REVISIONS,
              "sanity": {"part_a_step143000_vs_archive": a["sanity_a"],
                         "part_b_beta1_identity": b["sanity_b"]},
              "random_support_median_n128": a["random_support_median_n128"],
              "part_a": a["part_a"], "part_b": b["part_b"],
              "timing_seconds": {"part_a": a["timing_seconds"], "part_b": b["timing_seconds"],
                                 "total": a["timing_seconds"] + b["timing_seconds"]}}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")
    log("E5 merge", f"wrote {OUT_JSON} from {PARTIAL_A} + {PARTIAL_B}")
    print(f"E5 merged -> {OUT_JSON}", flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part-a", action="store_true")
    ap.add_argument("--part-b", action="store_true")
    ap.add_argument("--part-b2", action="store_true")
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()
    if args.merge:
        merge_partials()
        return
    if args.part_b2 and (args.part_a or args.part_b):
        raise RuntimeError("--part-b2 nao combina com --part-a/--part-b")
    if args.part_b2:
        t0 = time.perf_counter()
        log("E5B2 start", f"command: `{' '.join(sys.argv)}`")
        if OUT_EQ_JSON.exists():
            raise RuntimeError(f"Refusing to overwrite existing output, inspect first: {OUT_EQ_JSON}")
        # pares phase22_eq_* novos: nunca tocam nos pares existentes phase22_abl_*/ckpt_*;
        # se um phase22_eq_* parcial existir, run_part_b2_model recusa/aproveita como a parte B.
        part_b2, sanity_b2, secs_b2 = run_part_b2()
        result = {"experiment": "E5B2 sink equalizado por linha (auditoria)",
                  "n": N, "k_line": K_LINE,
                  "theta_degrees": np.arange(0.0, 180.0, 2.0).tolist(),
                  "random_controls": {"n_controls": N_CONTROLS, "seed": CONTROL_SEED},
                  "sanity": sanity_b2,
                  "random_support_median_n128": part_b2[MODELS[0]]["random_support_median"],
                  "part_b2": part_b2,
                  "timing_seconds": secs_b2,
                  "audit_reference_expected": {
                      "model": "EleutherAI/pythia-410m", "base": "atten_b0",
                      "ratio_orig_eq_sink_eq_ctrl": [0.01759, 0.04252, 0.00640],
                      "line_k8_orig_eq_sink_eq_ctrl": [0.47597, 0.65466, 0.45820]}}
        OUT_EQ_JSON.parent.mkdir(parents=True, exist_ok=True)
        with OUT_EQ_JSON.open("x", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, allow_nan=False)
            f.write("\n")
        log("E5B2 done", f"wrote {OUT_EQ_JSON}", time.perf_counter() - t0)
        print(f"E5B2 complete in {time.perf_counter() - t0:.1f}s -> {OUT_EQ_JSON}", flush=True)
        return
    do_a = args.part_a or not (args.part_a or args.part_b)
    do_b = args.part_b or not (args.part_a or args.part_b)
    t0 = time.perf_counter()
    log("E5 start", f"part_a={do_a} part_b={do_b} | command: `{' '.join(sys.argv)}`")
    if do_a and not do_b:
        if not torch.cuda.is_available():
            raise RuntimeError("Part A requires CUDA")
        part, sanity_a, random_median, secs_a = run_part_a()
        write_partial(PARTIAL_A, {"part_a": part, "sanity_a": sanity_a,
                                  "random_support_median_n128": random_median,
                                  "timing_seconds": secs_a})
        log("E5 part A stored", f"wrote {PARTIAL_A}", time.perf_counter() - t0)
        return
    if do_b and not do_a:
        part_b, sanity_b, secs_b = run_part_b()
        write_partial(PARTIAL_B, {"part_b": part_b, "sanity_b": sanity_b,
                                  "timing_seconds": secs_b})
        log("E5 part B stored", f"wrote {PARTIAL_B}", time.perf_counter() - t0)
        return
    result = {"experiment": "E5 sink contribution to Radon concentration",
              "n": N, "k_line": K_LINE, "theta_degrees": np.arange(0.0, 180.0, 2.0).tolist(),
              "random_controls": {"n_controls": N_CONTROLS, "seed": CONTROL_SEED},
              "ckpt_model": CKPT_MODEL, "ckpt_revisions": REVISIONS,
              "sanity": {}, "part_a": {}, "part_b": {}, "timing_seconds": {}}
    if do_a:
        if not torch.cuda.is_available():
            raise RuntimeError("Part A requires CUDA")
        part, sanity_a, random_median, secs_a = run_part_a()
        result["part_a"] = part
        result["sanity"]["part_a_step143000_vs_archive"] = sanity_a
        result["random_support_median_n128"] = random_median
        result["timing_seconds"]["part_a"] = secs_a
    if do_b:
        part_b, sanity_b, secs_b = run_part_b()
        result["part_b"] = part_b
        result["sanity"]["part_b_beta1_identity"] = sanity_b
        result["timing_seconds"]["part_b"] = secs_b
    result["timing_seconds"]["total"] = time.perf_counter() - t0
    if OUT_JSON.exists():
        raise RuntimeError(f"Refusing to overwrite existing output, inspect first: {OUT_JSON}")
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")
    log("E5 done", f"wrote {OUT_JSON} with part_a={sorted(result['part_a'])} "
        f"part_b={sorted(result['part_b'])}", result["timing_seconds"]["total"])
    print(f"E5 complete in {result['timing_seconds']['total']:.1f}s -> {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
