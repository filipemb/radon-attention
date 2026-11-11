"""Frozen phase19 optimizer with explicit width cap and float64 parameter export."""
import phase19c_common
import os,time,hashlib
import numpy as np
import torch
from scipy.optimize import minimize
from richlines_parametric import from_dictionary,random_start,torch_grid,render_numpy
from phase19c_render import RecurrenceRenderLines

def fit_parametric(b, n, checkpoints, uniform, profiled, uniform_results, profiled_results,
                   seed, device="cuda", iterations=450, return_parameters=False,
                   oracle=None, refine_iterations=150, sigma_max=None, legacy_bounds=False):
    if device == "cuda" and os.environ.get("RICHLINE_GPU_LOCK") != "1":
        raise RuntimeError("CUDA execution requires the outer flock /tmp/radon-gpu.lock")
    cap=float(n if sigma_max is None else sigma_max)
    if not .2<=cap<=n:raise ValueError("Invalid width cap")
    lo_log=float(np.float32(np.log(.2)))
    hi_log=float(np.float32(np.log(cap)))
    if not legacy_bounds:
        if np.exp(lo_log)<.2:lo_log=float(np.nextafter(np.float32(lo_log),np.float32(np.inf)))
        if np.exp(hi_log)>cap:hi_log=float(np.nextafter(np.float32(hi_log),np.float32(-np.inf)))
    else:
        lo_log=np.log(.2);hi_log=np.log(n)
    initial_hashes={}
    start = time.perf_counter()
    norm = float(np.linalg.norm(b))
    target = np.asarray(b, dtype=float) / norm
    rng = np.random.default_rng(seed)
    renderer=RecurrenceRenderLines
    if device=="cuda":
        from phase19c_cuda import CudaRenderLines
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
        initial_hashes[str(k)]=hashlib.sha256(initial.tobytes()).hexdigest()
        if not legacy_bounds:initial[:,:,2]=np.clip(initial[:,:,2],np.exp(lo_log),np.exp(hi_log))
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
                logwidth.clamp_(lo_log,hi_log)
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
        limits=((None,None),(-n*np.sqrt(2),n*np.sqrt(2)),(lo_log,hi_log),(-32,32),(0,1))
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
            p = np.stack([v.detach().cpu().numpy()[winner].astype(np.float64) for v in best_params], axis=1)
            p[:, 0] %= 2*np.pi
            p[:, 2] = np.exp(p[:, 2])
            p[:, 4] *= norm
            row["parameters"] = p.tolist()
        if oracle is not None:
            row["oracle_render_diagnostic_relative"] = float(np.linalg.norm(render_numpy(oracle,n)-b)/norm)
        result[group["k"]] = row
    if device == "cuda":
        torch.cuda.synchronize()
    for row in result.values():
        row["width_cap_intended"]=cap
        row["effective_width_bounds"]=[float(np.exp(lo_log)),float(np.exp(hi_log))]
    return result, {"initialization_hashes_before_width_projection":initial_hashes,"width_cap":cap,"legacy_width_clamping":legacy_bounds,"seconds": time.perf_counter()-start, "optimizer": "Adam with projected box constraints",
                    "iterations": iterations, "starts": names, "seed": seed,
                    "device": device, "dtype": "float32", "n_parameters_per_line": 5,
                    "learning_rates": {"angle": 0.35/n, "offset": 0.35, "log_width": 0.04,
                                       "decay": 0.06, "amplitude": 0.025},"refinement":refinement}

