"""Cover both stated QK conventions using exactly the same underlying draws."""
import phase19c_common
import numpy as np
from phase19c_synthetic import specs as original_specs,make as original_make,freeze_decay_pool

def specs():
    plan=original_specs()
    additional=[]
    for s in plan["negative"]:
        if s["family"]=="random_qk_causal_softmax":
            additional.append({**s,"family":"random_qk_causal_softmax_unscaled","id":s["id"].replace("qk_","qk_unscaled_")})
    plan["negative"].extend(additional)
    return plan

def make(spec,pool=None):
    if spec.get("family")!="random_qk_causal_softmax_unscaled":return original_make(spec,pool)
    n=spec["n"];rng=np.random.default_rng(spec["seed"])
    q=rng.normal(size=(n,spec["d_k"]));k=rng.normal(size=(n,spec["d_k"]));logits=q@k.T
    logits[np.triu_indices(n,1)]=-np.inf;logits-=logits.max(axis=1,keepdims=True)
    a=np.exp(logits);a/=a.sum(axis=1,keepdims=True)
    return a,{"generation":"Same iid standard normal Q,K draws as scaled control, d_k64; QK^T without sqrt(d_k) division; stable causal softmax",
        "no_planted_line_structure":True,"reason":"The audit logit temperature was unspecified. Both conventions are reported separately without selecting one by its result."}
