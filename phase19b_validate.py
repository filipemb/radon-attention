"""Independent dense rendering, finite differences and energy accounting."""
import phase19b_common
import numpy as np
import torch
from richlines_parametric import DenseRenderLines,torch_grid
from phase19b_render import RecurrenceRenderLines
from phase19b_stats import decoded_statistics
from phase19b_common import SEED,write_json,progress


def validate():
    torch.set_num_threads(4);torch.set_num_interop_threads(4);torch.manual_seed(SEED)
    results=[]
    for n in (31,128,256):
        dtype=torch.float64;x,y=torch_grid(n,"cpu",dtype)
        generator=np.random.default_rng(SEED+n);shape=(4,12)
        values=[generator.uniform(-np.pi,2*np.pi,shape),generator.uniform(-n,n,shape),
                generator.uniform(np.log(.2),np.log(n),shape),generator.uniform(-32,32,shape),generator.uniform(0,1,shape)]
        params=[torch.nn.Parameter(torch.as_tensor(v,dtype=dtype).contiguous()) for v in values]
        dense=DenseRenderLines.apply(*params,x,y,n);weights=torch.randn_like(dense)
        (dense*weights).sum().backward();expected=[p.grad.clone() for p in params]
        for p in params:p.grad=None
        actual=RecurrenceRenderLines.apply(*params,x,y,n);(actual*weights).sum().backward()
        value=float((actual-dense).abs().max());gradient=max(float(((p.grad-g).abs()/(1+g.abs())).max()) for p,g in zip(params,expected))
        if value>2e-10 or gradient>2e-8:raise AssertionError(f"Renderer mismatch n={n}: {value}, {gradient}")
        results.append({"n":n,"forward_max_absolute":value,"gradient_max_scaled_absolute":gradient})
    n=7;x,y=torch_grid(n,"cpu",torch.float64)
    p=[torch.tensor(v,dtype=torch.float64,requires_grad=True) for v in
       ([[.3,1.2]],[[-1.,1.]],[[.2,-.1]],[[1.5,-.7]],[[.7,1.2]])]
    finite=bool(torch.autograd.gradcheck(lambda *v:RecurrenceRenderLines.apply(*v,x,y,n),tuple(p),atol=1e-5,rtol=1e-4))
    if not finite:raise AssertionError("Finite-difference backward failure")
    params=np.array([[.2,0,1.,1.,.7],[1.,2.,4.,-.5,.8]])
    stats=decoded_statistics(params,31,np.ones(31*32//2));s=stats["wide_energy"]["2.0"]
    if abs(s["additive_share"]*stats["reconstruction_energy"]-s["wide_self_energy"]-s["wide_thin_inner_product"])>1e-10:
        raise AssertionError("Cross-term accounting is not additive")
    result={"passed":True,"renderer_comparisons":results,"finite_difference_gradcheck":finite,
            "energy_cross_terms_verified":True,"value_tolerance":2e-10,"gradient_tolerance":2e-8}
    write_json("out/phase19b_numerical_validation.json",result);progress("PHASE19B numerical values, gradients and additive energy accounting passed")
    return result


if __name__=="__main__":validate()
