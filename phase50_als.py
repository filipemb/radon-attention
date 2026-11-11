"""E9 masked ALS in float64, with fixed sweeps and a product-preserving QR gauge.

This file contains only the estimator. Projection onto causal probabilities and
behavioral scoring are always imported from phase2_downstream.
"""
import os
for _key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_key] = "4"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import datasets  # Before torch, also before indirect torch imports.
import time
import math
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from numba import njit
import torch

SWEEPS = 200
LS_RCOND = 1e-12
GRAM_MIN_RATIO = 1e-6
MONOTONIC_TOL = 1e-9
CHECKPOINTS = (0, 1, 10, 25, 50, 100, 150, 180, 200)
GPU_SOLVER = "prefix_qr"
_solver_decision=Path("out/phase50_gpu_solver.json")
if _solver_decision.exists():
    GPU_SOLVER=json.loads(_solver_decision.read_text(encoding="utf-8"))["backend"]


@njit(cache=False)
def direct_blocks(a, f, indices, reverse):
    result = np.empty((len(indices), f.shape[1]))
    for j in range(len(indices)):
        i = indices[j]
        design = f[i:].copy() if reverse else f[:i+1].copy()
        rhs = a[i, i:].copy() if reverse else a[i, :i+1].copy()
        result[j] = np.linalg.lstsq(design, rhs, LS_RCOND)[0]
    return result


def balance_cpu(u, v):
    qu, ru = np.linalg.qr(u, mode="reduced")
    qv, rv = np.linalg.qr(v, mode="reduced")
    left, s, vh = np.linalg.svd(ru @ rv.T, full_matrices=False)
    root = np.sqrt(s)
    return (qu @ left) * root, (qv @ vh.T) * root


def update_cpu(a, f, reverse=False, direct=False):
    n = len(a)
    if direct:
        return direct_blocks(a, f, np.arange(n), reverse), n
    products = np.einsum("ni,nj->nij", f, f)
    gram = np.cumsum(products[::-1], axis=0)[::-1] if reverse else np.cumsum(products, axis=0)
    eig, rot = np.linalg.eigh(gram)
    good = (eig[:, 0] > GRAM_MIN_RATIO * eig[:, -1]) & (eig[:, -1] > 0)
    out = np.empty_like(f)
    rhs = a @ f
    if good.any():
        q = rot[good]
        def solve(h):
            return np.einsum("nij,nj->ni", q, np.einsum("nji,nj->ni", q, h) / eig[good])
        out[good] = solve(rhs[good])
    bad = np.flatnonzero(~good)
    if len(bad):
        out[bad] = direct_blocks(a, f, bad, reverse)
    if good.any():
        prediction = out @ f.T
        residual = a - (np.triu(prediction) if reverse else np.tril(prediction))
        out[good] += solve((residual @ f)[good])
    if not np.isfinite(out).all():
        raise FloatingPointError("Nonfinite CPU ALS least-squares solution")
    return out, len(bad)


def diagnostic(u, v, target, norm, losses, history, bad, retries, rejected, gauge_errors, seconds):
    residual = np.tril(u @ v.T) - target
    grad = float(np.hypot(np.linalg.norm(2 * residual @ v), np.linalg.norm(2 * residual.T @ u)))
    change = abs(losses[-21] - losses[-1]) / max(losses[-21], 1e-24)
    scale = np.sqrt(norm)
    factors = np.concatenate((np.abs(u.ravel()), np.abs(v.ravel()))) * scale
    nz = factors[factors > 0]
    maximum = float(factors.max())
    minimum = float(nz.min()) if len(nz) else None
    return {"sweeps": SWEEPS, "dtype": "float64", "initial_relative": float(np.sqrt(losses[0])),
            "final_relative": float(np.sqrt(losses[-1])), "history": history,
            "last20_relative_objective_change": float(change), "gradient_normalized_target": grad,
            "converged": bool(grad <= 1e-6 and (change <= 1e-7 or losses[-1] <= 1e-12) and (not rejected or losses[-1] <= 1e-12)),
            "direct_LS_blocks": int(bad), "direct_sweep_retries": int(retries),
            "rejected_sweeps": rejected, "maximum_absolute_factor": maximum,
            "minimum_nonzero_absolute_factor": minimum,
            "factor_dynamic_range": maximum / minimum if minimum is not None else 0.,
            "unmasked_product_norm_over_target": float(np.linalg.norm(u @ v.T)),
            "maximum_QR_observed_product_error": float(max(gauge_errors, default=0.)),
            "seconds": float(seconds)}


def fit_cpu(a, rank, initial=None):
    started = time.perf_counter()
    a = np.asarray(a, dtype=np.float64)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.isfinite(a).all() or np.any(np.triu(a, 1)):
        raise ValueError("ALS requires a finite square causal target (signed residuals allowed)")
    norm = float(np.linalg.norm(a))
    if norm == 0:
        u = np.zeros((len(a), rank)); v = u.copy(); target = a.copy()
        losses = [0.] * (SWEEPS + 1)
        hist = [{"sweep": i, "relative": 0.} for i in CHECKPOINTS]
        return a.copy(), diagnostic(u, v, target, 1., losses, hist, 0, 0, [], [], time.perf_counter()-started)
    target = a / norm
    if initial is None:
        left, s, vh = np.linalg.svd(a, full_matrices=False)
        root = np.sqrt(s[:rank] / norm)
        u, v = left[:, :rank] * root, vh[:rank].T * root
    else:
        u, v = (np.asarray(x, dtype=np.float64).copy() / np.sqrt(norm) for x in initial)
    loss = float(np.linalg.norm(np.tril(u @ v.T) - target) ** 2)
    losses = [loss]; hist = [{"sweep": 0, "relative": float(np.sqrt(loss))}]
    bad = retries = 0; rejected = []; gauge_errors = []
    for sweep in range(1, SWEEPS + 1):
        cu, count = update_cpu(target, v); bad += count
        cv, count = update_cpu(target.T, cu, True); bad += count
        before = np.tril(cu @ cv.T)
        cu, cv = balance_cpu(cu, cv)
        gauge_errors.append(float(np.linalg.norm(np.tril(cu @ cv.T) - before)))
        trial = float(np.linalg.norm(np.tril(cu @ cv.T) - target) ** 2)
        if not np.isfinite(trial):
            raise FloatingPointError("Nonfinite ALS objective; no replacement")
        if trial > loss + MONOTONIC_TOL * max(1., loss):
            retries += 1
            cu, count = update_cpu(target, v, direct=True); bad += count
            cv, count = update_cpu(target.T, cu, True, direct=True); bad += count
            before = np.tril(cu @ cv.T)
            cu, cv = balance_cpu(cu, cv)
            gauge_errors.append(float(np.linalg.norm(np.tril(cu @ cv.T) - before)))
            trial = float(np.linalg.norm(np.tril(cu @ cv.T) - target) ** 2)
            if not np.isfinite(trial):
                raise FloatingPointError("Nonfinite direct ALS retry")
            if trial > loss + MONOTONIC_TOL * max(1., loss):
                rejected.append({"sweep": sweep, "previous_loss": loss, "proposed_loss": trial})
                cu, cv, trial = u, v, loss
        u, v, loss = cu, cv, trial
        losses.append(loss)
        if sweep in CHECKPOINTS:
            hist.append({"sweep": sweep, "relative": float(np.sqrt(loss))})
    info = diagnostic(u, v, target, norm, losses, hist, bad, retries, rejected, gauge_errors, time.perf_counter()-started)
    return (u * np.sqrt(norm)) @ (v * np.sqrt(norm)).T, info


def balance_gpu(u, v):
    qu, ru = torch.linalg.qr(u, mode="reduced")
    qv, rv = torch.linalg.qr(v, mode="reduced")
    left, s, vh = torch.linalg.svd(ru @ rv.transpose(-1, -2), full_matrices=False)
    root = s.sqrt().unsqueeze(-2)
    return (qu @ left) * root, (qv @ vh.transpose(-1, -2)) * root


def update_gpu(a, f, support, reverse=False, direct=False):
    if GPU_SOLVER == "certified_qr":
        from phase50_certified_qr_cuda import update
        return update(a,f,support,reverse,direct)
    if GPU_SOLVER == "prefix_qr":
        from phase50_prefix_qr_cuda import update
        return update(a,f,support,reverse,direct)
    if direct:
        good = torch.zeros(f.shape[:2],device=f.device,dtype=torch.bool)
    else:
        products = f.unsqueeze(-1) * f.unsqueeze(-2)
        gram = products.flip(1).cumsum(1).flip(1) if reverse else products.cumsum(1)
        eig, rot = torch.linalg.eigh(gram)
        good = (eig[..., 0] > GRAM_MIN_RATIO * eig[..., -1]) & (eig[..., -1] > 0)
    # An explicit full-design SVD handles every ill-conditioned/rank-deficient
    # block, with the same 1e-12 singular-value cutoff as the CPU reference.
    rhs = a @ f
    if not direct:
        # Fixed-shape algebra avoids a separate CUDA size synchronization for
        # every Boolean gather/scatter. Ill-conditioned blocks are overwritten
        # by the direct QR/SVD solve below, never used as Gram solutions.
        denominator = torch.where(good.unsqueeze(-1),eig,torch.ones_like(eig))
        def solve(h):
            rotated = (rot.transpose(-1,-2) @ h.unsqueeze(-1)).squeeze(-1)/denominator
            return (rot @ rotated.unsqueeze(-1)).squeeze(-1)
        out = torch.where(good.unsqueeze(-1),solve(rhs),torch.zeros_like(f))
    else:
        out = torch.empty_like(f)
    idx = (~good).nonzero()
    if len(idx):
        b, i = idx.unbind(1)
        mask = support.T if reverse else support
        design = f[b] * mask[i].unsqueeze(-1)
        # Reduce the tall design first. CUDA's batched Jacobi SVD handles the
        # resulting <=16x16 R factors together; a tall SVD serializes cuSOLVER
        # calls. QR is an isometry, so this retains the direct-design singular
        # values and the declared cutoff without forming normal equations.
        design_q, design_r = torch.linalg.qr(design, mode="reduced")
        left, singular, vh = torch.linalg.svd(design_r, full_matrices=False)
        active = singular > LS_RCOND * singular[..., :1]
        inv = torch.where(active, singular.reciprocal(), 0.)
        transformed = design_q.transpose(-1, -2) @ a[b, i].unsqueeze(-1)
        out[b, i] = (vh.transpose(-1, -2) @ (inv * (left.transpose(-1, -2) @ transformed).squeeze(-1)).unsqueeze(-1)).squeeze(-1)
    if not direct:
        residual = a - (out @ f.transpose(-1, -2)) * (support.T if reverse else support)
        out += torch.where(good.unsqueeze(-1),solve(residual @ f),torch.zeros_like(f))
    return out, len(idx)


@torch.inference_mode()
def _fit_gpu_uncorrected(a, rank, support, initial=None):
    """Batched CUDA double ALS; support is supplied by the imported harness."""
    if GPU_SOLVER=="prefix_qr_graph":
        from phase50_graph_als_cuda import fit
        return fit(a,rank,support,initial)
    started = time.perf_counter(); a = a.double()
    norms = a.norm(dim=(-2, -1)); zero = norms == 0
    safe = torch.where(zero, 1., norms)
    target = a / safe[:, None, None]
    if initial is None:
        left, singular, vh = torch.linalg.svd(a, full_matrices=False)
        root = (singular[..., :rank] / safe[:, None]).sqrt().unsqueeze(-2)
        u, v = left[..., :rank] * root, vh[..., :rank, :].transpose(-1, -2) * root
    else:
        u, v = (x.double() / safe.sqrt()[:, None, None] for x in initial)
    loss = ((u @ v.transpose(-1, -2) - target) * support).square().sum((-2, -1))
    losses = [loss]; hist = {0: loss.sqrt()}; bad = retries = 0
    rejected = [[] for _ in a]; gauge_errors = []
    for sweep in range(1, SWEEPS + 1):
        cu, count = update_gpu(target, v, support); bad += count
        cv, count = update_gpu(target.transpose(-1, -2), cu, support, True); bad += count
        before = (cu @ cv.transpose(-1, -2)) * support
        cu, cv = balance_gpu(cu, cv)
        after = cu @ cv.transpose(-1,-2)
        gauge_errors.append((after * support - before).norm(dim=(-2, -1)))
        trial = ((after - target) * support).square().sum((-2, -1))
        need = trial > loss + MONOTONIC_TOL * torch.maximum(torch.ones_like(loss), loss)
        flag = int((2*(~torch.isfinite(trial)).to(torch.int32)+need.to(torch.int32)).max())
        if flag >= 2:
            raise FloatingPointError("Nonfinite GPU ALS objective")
        if flag:
            retries += int(need.sum())
            du, count = update_gpu(target[need], v[need], support, direct=True); bad += count
            dv, count = update_gpu(target[need].transpose(-1, -2), du, support, True, direct=True); bad += count
            du, dv = balance_gpu(du, dv)
            dl = ((du @ dv.transpose(-1, -2) - target[need]) * support).square().sum((-2, -1))
            if not bool(torch.isfinite(dl).all()):
                raise FloatingPointError("Nonfinite GPU direct ALS retry")
            cu[need], cv[need], trial[need] = du, dv, dl
            reject = trial > loss + MONOTONIC_TOL * torch.maximum(torch.ones_like(loss), loss)
            for j in reject.nonzero().flatten().cpu().tolist():
                rejected[j].append({"sweep": sweep, "previous_loss": float(loss[j]), "proposed_loss": float(trial[j])})
            u = torch.where(reject[:, None, None], u, cu)
            v = torch.where(reject[:, None, None], v, cv)
            loss = torch.where(reject, loss, trial)
        else:
            u,v,loss = cu,cv,trial
        losses.append(loss)
        if sweep in CHECKPOINTS:
            hist[sweep] = loss.sqrt()
            if os.environ.get("PHASE50_ALS_PROGRESS") == "1":
                print(f"ALS GPU batch={len(a)} rank={rank} sweep={sweep}/{SWEEPS} elapsed={time.perf_counter()-started:.2f}s direct_blocks={bad} retries={retries}", flush=True)
    product = (u * safe.sqrt()[:, None, None]) @ (v * safe.sqrt()[:, None, None]).transpose(-1, -2)
    if not bool(torch.isfinite(product).all()):
        raise FloatingPointError("Nonfinite GPU factors/product")
    # Keep diagnostic reductions on GPU. Copying factors and multiplying each
    # head on CPU would serialize the independent fits after every layer.
    raw_product=u@v.transpose(-1,-2); residual=(raw_product-target)*support
    gradient=(2*residual@v).square().sum((-2,-1))+(2*residual.transpose(-1,-2)@u).square().sum((-2,-1))
    change=(losses[-21]-losses[-1]).abs()/losses[-21].clamp_min(1e-24)
    factors=torch.cat((u.abs().flatten(1),v.abs().flatten(1)),1)*safe.sqrt()[:,None]
    minimum=torch.where(factors>0,factors,torch.full_like(factors,float("inf"))).amin(1)
    packed=torch.stack((factors.amax(1),minimum,gradient.sqrt(),change,raw_product.norm(dim=(-2,-1)),torch.stack(gauge_errors).amax(0)),1).cpu().tolist()
    lc=torch.stack(losses).cpu().tolist(); hc=torch.stack([hist[i] for i in CHECKPOINTS]).cpu().tolist()
    elapsed=time.perf_counter()-started; infos=[]
    for j, (maximum,minimum,grad,change,unmasked,gauge) in enumerate(packed):
        if minimum==float("inf") and maximum==0.:
            minimum=None  # Empty set: all factors exactly zero.
        elif not np.isfinite(minimum):
            raise FloatingPointError("Nonfinite minimum factor outside the explicit all-zero case")
        infos.append({"sweeps":SWEEPS,"dtype":"float64","GPU_solver":GPU_SOLVER,
                      "initial_relative":float(np.sqrt(lc[0][j])),"final_relative":float(np.sqrt(lc[-1][j])),
                      "history":[{"sweep":s,"relative":hc[i][j]} for i,s in enumerate(CHECKPOINTS)],
                      "last20_relative_objective_change":change,"gradient_normalized_target":grad,
                      "converged":bool(grad<=1e-6 and (change<=1e-7 or lc[-1][j]<=1e-12) and (not rejected[j] or lc[-1][j]<=1e-12)),
                      "direct_LS_blocks":bad,"direct_sweep_retries":retries,"counter_scope":"whole batch for LS blocks and retries",
                      "rejected_sweeps":rejected[j],"maximum_absolute_factor":maximum,"minimum_nonzero_absolute_factor":minimum,
                      "factor_dynamic_range":maximum/minimum if minimum is not None else 0.,
                      "unmasked_product_norm_over_target":unmasked,"maximum_QR_observed_product_error":gauge,"seconds":elapsed})
    return product, infos


_CPU_CORRECTION_POOL=None
_CPU_CORRECTION_WORKERS=1


def enable_parallel_cpu_corrections(workers=3):
    global _CPU_CORRECTION_WORKERS
    _CPU_CORRECTION_WORKERS=min(3,workers)


def close_cpu_corrections():
    global _CPU_CORRECTION_POOL
    if _CPU_CORRECTION_POOL is not None:
        _CPU_CORRECTION_POOL.shutdown(wait=True)
        _CPU_CORRECTION_POOL=None


def _cpu_correction_job(job):
    a,rank,initial=job
    return fit_cpu(a,rank,initial)


@torch.inference_mode()
def fit_gpu(a,rank,support,initial=None,return_uncorrected=False):
    """Run the GPU attempt; preserve diagnostics and use the CPU reference
    for finite QR-product changes above the existing harness tolerance.

    The returned CPU fit is restarted at the original SVD and runs200 sweeps;
    it never warm-starts from the discarded GPU attempt. A GPU exception or
    nonfinite value still propagates and stops the fit, rather than being
    swallowed by this finite-error correction policy.
    """
    global _CPU_CORRECTION_POOL
    product,raw_infos=_fit_gpu_uncorrected(a,rank,support,initial)
    def finite_diagnostics(value):
        if isinstance(value,float) and not math.isfinite(value):raise FloatingPointError("Nonfinite GPU diagnostic; CPU correction cannot suppress it")
        if isinstance(value,dict):
            for item in value.values():finite_diagnostics(item)
        elif isinstance(value,list):
            for item in value:finite_diagnostics(item)
    finite_diagnostics(raw_infos)
    raw_product=product; infos=[dict(x) for x in raw_infos]
    policy_path=Path("out/phase50_numerical_fallback.json")
    if policy_path.exists():
        policy=json.loads(policy_path.read_text(encoding="utf-8"))
        tolerance=policy["QR_observed_product_error_tolerance"]
        flags=[j for j,info in enumerate(raw_infos) if info["maximum_QR_observed_product_error"]>tolerance]
        if flags:
            cpu_targets=a[flags].double().cpu().numpy()
            if initial is None:cpu_initial=[None]*len(flags)
            else:
                left,right=(x[flags].double().cpu().numpy() for x in initial)
                cpu_initial=[(left[j],right[j]) for j in range(len(flags))]
            jobs=[(cpu_targets[j],rank,cpu_initial[j]) for j in range(len(flags))]
            if _CPU_CORRECTION_WORKERS>1:
                if _CPU_CORRECTION_POOL is None:_CPU_CORRECTION_POOL=ProcessPoolExecutor(max_workers=_CPU_CORRECTION_WORKERS)
                corrected=list(_CPU_CORRECTION_POOL.map(_cpu_correction_job,jobs))
            else:corrected=[_cpu_correction_job(job) for job in jobs]
            product=product.clone()
            for j,(cpu_product,cpu_info) in zip(flags,corrected):
                product[j]=torch.from_numpy(cpu_product).to(device=a.device,dtype=torch.float64)
                infos[j]={**cpu_info,"fit_backend":"CPU_float64_reference_recomputation",
                          "numerical_fallback":True,"numerical_fallback_tolerance":tolerance,
                          "GPU_solver_attempted":GPU_SOLVER,"uncorrected_GPU":raw_infos[j],
                          "returned_estimator_sweeps":SWEEPS,"discarded_GPU_attempt_sweeps":SWEEPS,
                          "initialization_after_fallback":"original truncated SVD; no warm start"}
        for j in range(len(infos)):
            if "numerical_fallback" not in infos[j]:
                infos[j]["numerical_fallback"]=False
                infos[j]["fit_backend"]="GPU_float64"
    if return_uncorrected:return product,infos,raw_product,raw_infos
    return product,infos
