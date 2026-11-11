"""Differentiable, nonnegative, causal tapered Gaussian line primitives for E2(c).

Five stored numbers per primitive: normal angle, centered offset in pixels,
transverse width in pixels, longitudinal decay per n pixels, amplitude. An
analytic autograd backward avoids retaining a pixels-by-atoms graph for every
budget and start. All starts and all budgets are fitted, without SVD guidance.
"""
from __future__ import annotations

import os
import time
import numpy as np
import torch
from scipy.optimize import minimize

from richlines_core import SEED


class DenseRenderLines(torch.autograd.Function):
    @staticmethod
    def forward(ctx, theta, rho, logwidth, decay, amplitude, x, y, n):
        ctx.save_for_backward(theta, rho, logwidth, decay, amplitude, x, y)
        ctx.n = n
        c, s = theta.cos()[..., None], theta.sin()[..., None]
        w = logwidth.exp()[..., None]
        q = (c * x + s * y - rho[..., None]) / w
        t = (-s * x + c * y) / n
        z = -0.5 * q.square() - decay[..., None] * t
        z=z+3*torch.clamp(1-q.square()/36,min=1e-30).log()
        z=torch.where(q.abs()<6,z,torch.full_like(z,-torch.inf))
        maximum=z.amax(dim=-1,keepdim=True)
        maximum=torch.where(torch.isfinite(maximum),maximum,torch.zeros_like(maximum))
        u=(z-maximum).exp()
        u = u / u.square().sum(dim=-1, keepdim=True).sqrt().clamp_min(1e-30)
        return (amplitude[..., None] * u).sum(dim=-2)

    @staticmethod
    def backward(ctx, grad_output):
        theta, rho, logwidth, decay, amplitude, x, y = ctx.saved_tensors
        n = ctx.n
        c, s = theta.cos()[..., None], theta.sin()[..., None]
        w = logwidth.exp()[..., None]
        q = (c * x + s * y - rho[..., None]) / w
        t = (-s * x + c * y) / n
        z = -0.5 * q.square() - decay[..., None] * t
        z=z+3*torch.clamp(1-q.square()/36,min=1e-30).log()
        z=torch.where(q.abs()<6,z,torch.full_like(z,-torch.inf))
        maximum=z.amax(dim=-1,keepdim=True)
        maximum=torch.where(torch.isfinite(maximum),maximum,torch.zeros_like(maximum))
        u=(z-maximum).exp()
        u = u / u.square().sum(dim=-1, keepdim=True).sqrt().clamp_min(1e-30)
        e = grad_output[..., None, :]
        eu = (e * u).sum(dim=-1)
        h = amplitude[..., None] * (e * u - u.square() * eu[..., None])
        f = -q-6*q/torch.clamp(36-q.square(), min=1e-8)
        theta_derivative = f*t*n/w + decay[..., None]*(rho[..., None]+w*q)/n
        return ((h * theta_derivative).sum(dim=-1), -(h*f/w).sum(dim=-1),
                -(h*f*q).sum(dim=-1), -(h * t).sum(dim=-1), eu,
                None, None, None)


def _sparse_atoms(theta, rho, logwidth, decay, n):
    """Exact compact support; the transverse taper is C2 at |q|=6.

    No pixel approximation is made: the dense rendering is identically zero
    outside these strips. Width buckets avoid padding every atom to the width
    of the broadest primitive. The dominant normal axis avoids small divisors.
    """
    shape = theta.shape
    theta,rho,logwidth,decay = [v.reshape(-1) for v in (theta,rho,logwidth,decay)]
    widths = logwidth.detach().exp().cpu().numpy()
    halfwidths = np.minimum(n, np.ceil(6*np.sqrt(2)*widths).astype(int)+1)
    buckets = np.minimum(n, 2**np.ceil(np.log2(np.maximum(halfwidths,1))).astype(int))
    axis = torch.arange(n,device=theta.device,dtype=theta.dtype)[None,:,None]
    center = (n-1)/2
    for half in np.unique(buckets):
        ids = torch.as_tensor(np.flatnonzero(buckets==half),device=theta.device)
        c,s = theta[ids].cos()[:,None,None],theta[ids].sin()[:,None,None]
        r,w = rho[ids,None,None],logwidth[ids,None,None].exp()
        dominant = c.abs()>=s.abs()
        denominator = torch.where(dominant,c,s)
        other = torch.where(dominant,s,c)
        intercept = ((r-other*(axis-center))/denominator+center).floor().long()
        offsets = torch.arange(-int(half)-1,int(half)+2,device=theta.device)[None,None,:]
        near = intercept+offsets
        a = axis.long().expand(len(ids),n,len(offsets[0,0]))
        ii,jj = torch.where(dominant,a,near),torch.where(dominant,near,a)
        valid = (jj>=0)&(ii>=0)&(ii<n)&(jj<n)&(jj<=ii)
        xx,yy = jj.to(theta.dtype)-center,ii.to(theta.dtype)-center
        q = (c*xx+s*yy-r)/w
        t = (-s*xx+c*yy)/n
        valid &= q.abs()<6
        z = -0.5*q.square()-decay[ids,None,None]*t
        z = torch.where(valid,z,torch.full_like(z,-torch.inf))
        maximum = z.amax(dim=(-2,-1),keepdim=True)
        maximum = torch.where(torch.isfinite(maximum),maximum,torch.zeros_like(maximum))
        u = (z-maximum).exp()*torch.clamp(1-q.square()/36,min=0).pow(3)
        u /= u.square().sum(dim=(-2,-1),keepdim=True).sqrt().clamp_min(1e-30)
        pix = (ii*(ii+1)//2+jj).clamp(0,n*(n+1)//2-1)
        yield ids,pix,u,q,t,w,r,shape


class RenderLines(torch.autograd.Function):
    @staticmethod
    def forward(ctx,theta,rho,logwidth,decay,amplitude,x,y,n):
        ctx.save_for_backward(theta,rho,logwidth,decay,amplitude,x,y)
        ctx.n = n
        starts,k = theta.shape
        pixels = n*(n+1)//2
        result = torch.zeros(starts*pixels,device=theta.device,dtype=theta.dtype)
        for ids,pix,u,q,t,w,r,shape in _sparse_atoms(theta,rho,logwidth,decay,n):
            dest = (ids//k)[:,None,None]*pixels+pix
            v = amplitude.reshape(-1)[ids,None,None]*u
            result.scatter_add_(0,dest.reshape(-1),v.reshape(-1))
        return result.reshape(starts,pixels)

    @staticmethod
    def backward(ctx,grad_output):
        theta,rho,logwidth,decay,amplitude,x,y = ctx.saved_tensors
        n = ctx.n
        k = theta.shape[1]
        grads = [torch.zeros_like(theta).reshape(-1) for _ in range(5)]
        for ids,pix,u,q,t,w,r,shape in _sparse_atoms(theta,rho,logwidth,decay,n):
            e = grad_output[ids[:,None,None]//k,pix]
            eu = (e*u).sum(dim=(-2,-1),keepdim=True)
            h = amplitude.reshape(-1)[ids,None,None]*(e*u-u.square()*eu)
            f = -q-6*q/torch.clamp(36-q.square(),min=1e-8)
            dtheta = f*t*n/w+decay.reshape(-1)[ids,None,None]*(r+w*q)/n
            grads[0][ids] = (h*dtheta).sum(dim=(-2,-1))
            grads[1][ids] = -(h*f/w).sum(dim=(-2,-1))
            grads[2][ids] = -(h*f*q).sum(dim=(-2,-1))
            grads[3][ids] = -(h*t).sum(dim=(-2,-1))
            grads[4][ids] = eu.reshape(-1)
        return *(g.reshape(theta.shape) for g in grads),None,None,None


def torch_grid(n, device, dtype=torch.float32):
    ii, jj = np.tril_indices(n)
    center = (n - 1) / 2
    return (torch.as_tensor(jj - center, device=device, dtype=dtype),
            torch.as_tensor(ii - center, device=device, dtype=dtype))


def render_numpy(parameters, n):
    # Used for synthetic generation and independent numerical checks.
    p = np.asarray(parameters, dtype=float)
    if not np.isfinite(p).all():
        raise ValueError("Nonfinite parametric line parameters")
    ii, jj = np.tril_indices(n)
    x, y = jj - (n - 1)/2, ii - (n - 1)/2
    q = (np.cos(p[:, 0, None])*x + np.sin(p[:, 0, None])*y - p[:, 1, None]) / p[:, 2, None]
    t = (-np.sin(p[:, 0, None])*x + np.cos(p[:, 0, None])*y) / n
    z = -0.5*q*q - p[:, 3, None]*t
    z=z+3*np.log(np.maximum(1-q*q/36,1e-300))
    z=np.where(np.abs(q)<6,z,-np.inf)
    maximum=z.max(axis=1,keepdims=True)
    maximum=np.where(np.isfinite(maximum),maximum,0)
    u=np.exp(z-maximum)
    u/=np.maximum(np.linalg.norm(u,axis=1,keepdims=True),1e-300)
    return p[:, 4] @ u


def from_dictionary(dictionary, support, k, norm, rng, target):
    ids = support["indices"][:k]
    amps = np.asarray(support["amplitudes"][:k]) / norm
    p = dictionary.parameters(ids, amps)
    if len(p):
        p[:, 1] -= (dictionary.n - 1)/2 * (np.cos(p[:, 0]) + np.sin(p[:, 0]))
    if len(p) < k:
        # Padding remains a valid k-component representation. Positive seeds
        # allow unused slots to move rather than dying at zero amplitude.
        extra = random_start(target, dictionary.n, k-len(p), rng)
        extra[:, 4] *= 0.1
        p = np.concatenate([p, extra])
    return p


def random_start(target, n, k, rng):
    i, j = np.tril_indices(n)
    weights = np.maximum(np.asarray(target), 0)**2
    weights /= weights.sum()
    ids = rng.choice(len(i), size=k, replace=True, p=weights)
    theta = rng.uniform(0, np.pi, k)
    x, y = j[ids]-(n-1)/2, i[ids]-(n-1)/2
    rho = np.cos(theta)*x + np.sin(theta)*y
    width = np.exp(rng.uniform(np.log(0.5), np.log(max(1, n/16)), k))
    decay = rng.uniform(-4, 4, k)
    amp = np.full(k, 1/max(1, k)**0.5)
    return np.stack([theta, rho, width, decay, amp], axis=1)


def fit_parametric(b, n, checkpoints, uniform, profiled, uniform_results, profiled_results,
                   seed, device="cuda", iterations=450, return_parameters=False,
                   oracle=None, refine_iterations=150):
    if device == "cuda" and os.environ.get("RICHLINE_GPU_LOCK") != "1":
        raise RuntimeError("CUDA execution requires the outer flock /tmp/radon-gpu.lock")
    start = time.perf_counter()
    norm = float(np.linalg.norm(b))
    target = np.asarray(b, dtype=float) / norm
    rng = np.random.default_rng(seed)
    renderer=RenderLines
    if device=="cuda":
        from richlines_cuda import CudaRenderLines
        renderer=CudaRenderLines
    x, y = torch_grid(n, device)
    bt = torch.as_tensor(target, device=device, dtype=torch.float32)
    groups = []
    rates=(0.35/n,0.35,0.04,0.06,0.025)
    optimizer_groups=[{"params":[],"lr":rate} for rate in rates]
    from richlines_initialization import MultiscaleInitializer
    initializer=getattr(uniform,"multiscale_initializer",None)
    if initializer is None:
        initializer=MultiscaleInitializer(uniform)
        uniform.multiscale_initializer=initializer
    coarse=initializer.fit(target,min(32,max(checkpoints)))
    names = ["uniform_omp", "profiled_omp", "random_importance", "multiscale_sinogram_proposal_nnls"]
    for k in checkpoints:
        starts = [from_dictionary(uniform, uniform_results[k]["support"], k, norm, rng, target),
                  from_dictionary(profiled, profiled_results[k]["support"], k, norm, rng, target),
                  random_start(target, n, k, rng)]
        wide=coarse[min(k,32)].copy()
        if k>32:
            padding=from_dictionary(uniform,uniform_results[k]["support"],k,norm,
                                   np.random.default_rng(seed+123457+k),target)[32:]
            wide=np.concatenate([wide,padding])
        starts.append(wide)
        initial = np.stack(starts)
        values = [initial[:, :, 0], initial[:, :, 1], np.log(initial[:, :, 2]),
                  initial[:, :, 3], initial[:, :, 4]]
        params = [torch.nn.Parameter(torch.as_tensor(v, device=device, dtype=torch.float32).contiguous()) for v in values]
        for bucket,param in zip(optimizer_groups,params):
            bucket["params"].append(param)
        groups.append({"k": k, "params": params, "history": [], "best": None,
                       "best_params": None, "best_iteration": None})
    optimizer = torch.optim.Adam(optimizer_groups,foreach=True)
    for iteration in range(iterations + 1):
        optimizer.zero_grad(set_to_none=True)
        losses = []
        for group in groups:
            p = group["params"]
            recon = renderer.apply(*p, x, y, n)
            loss = (recon-bt).square().sum(dim=-1)
            current = loss.detach()
            if group["best"] is None:
                group["best"] = current.clone()
                group["best_params"] = [v.detach().clone() for v in p]
                group["best_iteration"] = torch.zeros(len(current), device=device, dtype=torch.long)
            else:
                better = current < group["best"]
                group["best"] = torch.minimum(current, group["best"])
                for dest, src in zip(group["best_params"], p):
                    dest.copy_(torch.where(better[:,None],src.detach(),dest))
                group["best_iteration"] = torch.where(better,
                    torch.full_like(group["best_iteration"],iteration),group["best_iteration"])
            if iteration % 25 == 0 or iteration == iterations:
                group["history"].append({"iteration": iteration, "relative_errors": current.sqrt().cpu().tolist()})
            losses.append(loss.sum())
        if iteration == iterations:
            break
        total_loss=sum(losses)
        if not bool(torch.isfinite(total_loss)):
            raise FloatingPointError(f"Nonfinite parametric loss at Adam update {iteration}")
        total_loss.backward()
        optimizer.step()
        with torch.no_grad():
            for group in groups:
                theta, rho, logwidth, decay, amplitude = group["params"]
                # The orientation is periodic; keeping theta unconstrained avoids
                # a discontinuity at pi. Geometry is recorded modulo 2*pi.
                rho.clamp_(-n*np.sqrt(2), n*np.sqrt(2))
                logwidth.clamp_(np.log(0.2), np.log(n))
                decay.clamp_(-32, 32)
                # For unit-norm nonnegative atoms and ||target||=1, every
                # coordinatewise optimal nonnegative amplitude is at most 1:
                # <u,target-other_atoms> <= <u,target> <= 1. This bound preserves
                # the attainable optimum and prevents unbounded line-search trials.
                amplitude.clamp_(min=0,max=1)
    refinement={"enabled":bool(refine_iterations),"max_iterations":refine_iterations}
    if refine_iterations:
        layout=[];packed=[];bounds=[]
        scales=(n/2,1.0,1.0,1.0,1.0)
        limits=((None,None),(-n*np.sqrt(2),n*np.sqrt(2)),(np.log(0.2),np.log(n)),(-32,32),(0,1))
        position=0
        for group in groups:
            for coord,(p,best) in enumerate(zip(group["params"],group["best_params"])):
                p.data.copy_(best)
                values=best.detach().cpu().numpy().astype(float).ravel()*scales[coord]
                layout.append((p,position,position+len(values),scales[coord]))
                position+=len(values);packed.append(values)
                low,high=limits[coord]
                bounds.extend([(None if low is None else low*scales[coord],
                                None if high is None else high*scales[coord])]*len(values))
        evaluations=0
        def objective(vector):
            nonlocal evaluations
            evaluations+=1
            with torch.no_grad():
                for p,lo,hi,scale in layout:
                    source=torch.as_tensor((vector[lo:hi]/scale).reshape(p.shape),device=device,dtype=torch.float32)
                    p.copy_(source)
            optimizer.zero_grad(set_to_none=True)
            total=[]
            for group in groups:
                pred=renderer.apply(*group["params"],x,y,n)
                loss=(pred-bt).square().sum(dim=-1)
                current=loss.detach()
                better=current<group["best"]
                group["best"]=torch.minimum(current,group["best"])
                for dest,src in zip(group["best_params"],group["params"]):
                    dest.copy_(torch.where(better[:,None],src.detach(),dest))
                group["best_iteration"]=torch.where(better,
                    torch.full_like(group["best_iteration"],iterations+evaluations),group["best_iteration"])
                total.append(loss.sum())
            loss=sum(total)
            loss.backward()
            gradient=torch.cat([(p.grad/scale).reshape(-1) for p,lo,hi,scale in layout])
            value=float(loss.detach().cpu())
            gradient=gradient.detach().cpu().numpy().astype(float)
            if not np.isfinite(value) or not np.isfinite(gradient).all():
                raise FloatingPointError("Nonfinite L-BFGS-B objective or gradient")
            return value,gradient
        opt=minimize(objective,np.concatenate(packed),jac=True,method="L-BFGS-B",bounds=bounds,
            options={"maxiter":refine_iterations,"maxls":30,"maxcor":20,"gtol":1e-7,"ftol":1e-12})
        refinement.update({"success":bool(opt.success),"message":str(opt.message),"iterations":int(opt.nit),
                           "function_evaluations":int(opt.nfev),"objective":float(opt.fun),
                           "gradient_max_absolute":float(np.max(np.abs(opt.jac))),
                           "coordinate_scale_angle":n/2,"gtol":1e-7,"ftol":1e-12,
                           "best_snapshot_rule":"retain each start's best error over Adam and all L-BFGS-B evaluations"})
    result = {}
    for group in groups:
        best_params = group["best_params"]
        for p, best in zip(group["params"], best_params):
            p.data.copy_(best)
        optimizer.zero_grad(set_to_none=True)
        pred = renderer.apply(*group["params"], x, y, n)
        loss = (pred-bt).square().sum(dim=-1)
        loss.sum().backward()
        errors = group["best"].sqrt().cpu().numpy()
        real_errors = errors[:len(names)]
        winner = int(np.argmin(real_errors))
        gradients = torch.stack([p.grad.square().sum(dim=-1) for p in group["params"]]).sum(dim=0).sqrt().detach().cpu().numpy()
        last_hist = group["history"][-1]["relative_errors"]
        prev_hist = group["history"][-2]["relative_errors"]
        plateau = [abs(a-b)/max(b, 1e-8) < 1e-4 for a,b in zip(last_hist, prev_hist)]
        row = {"relative": float(real_errors[winner]), "absolute": norm*float(real_errors[winner]),
               "best_start": names[winner], "start_names": names,
               "start_relative_errors": real_errors.tolist(),
               "start_absolute_errors": (norm*real_errors).tolist(),
               "start_error_std": float(real_errors.std()),
               "start_error_range": [float(real_errors.min()), float(real_errors.max())],
               "iterations": iterations, "best_iterations": group["best_iteration"][:len(names)].cpu().tolist(),
               "gradient_l2_at_best": gradients[:len(names)].tolist(),
               "plateau_last_25": plateau[:len(names)],
               "converged": bool(gradients[winner] < 1e-4 or plateau[winner]),
               "convergence_definition": "gradient L2 < 1e-4 or relative error change < 1e-4 over last 25 updates",
               "history_every_25": group["history"]}
        row["refinement"]=refinement
        if return_parameters:
            p = np.stack([v.detach().cpu().numpy()[winner] for v in best_params], axis=1)
            p[:, 0] %= 2*np.pi
            p[:, 2] = np.exp(p[:, 2])
            p[:, 4] *= norm
            row["parameters"] = p.tolist()
        if oracle is not None:
            row["oracle_render_diagnostic_relative"] = float(np.linalg.norm(render_numpy(oracle,n)-b)/norm)
        result[group["k"]] = row
    if device == "cuda":
        torch.cuda.synchronize()
    return result, {"seconds": time.perf_counter()-start, "optimizer": "Adam with projected box constraints",
                    "iterations": iterations, "starts": names, "seed": seed,
                    "device": device, "dtype": "float32", "n_parameters_per_line": 5,
                    "learning_rates": {"angle": 0.35/n, "offset": 0.35, "log_width": 0.04,
                                       "decay": 0.06, "amplitude": 0.025},"refinement":refinement}


def gradient_check():
    torch.set_num_threads(4)
    x,y = torch_grid(7, "cpu", torch.float64)
    params = [torch.tensor(v, dtype=torch.float64, requires_grad=True) for v in
              ([[0.3, 1.2]], [[-1.0, 1.0]], [[0.2, -0.1]], [[1.5, -0.7]], [[0.7, 1.2]])]
    ok = torch.autograd.gradcheck(lambda *p: RenderLines.apply(*p, x, y, 7),
                                 tuple(params), atol=1e-5, rtol=1e-4)
    if not ok:
        raise AssertionError("Analytic renderer backward failed finite differences")
    return {"gradcheck": bool(ok), "atol": 1e-5, "rtol": 1e-4, "n": 7}
