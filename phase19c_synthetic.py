"""Fixed causal nulls and planted segments, declared before their fitting."""
import phase19c_common
import numpy as np
from phase19c_common import SEED,ROOT,read_json,write_json,tag
from phase19c_metrics import line_image

def specs():
    negatives=[];planted=[];lowrank=[]
    for n in (128,256):
        negatives.append({"id":f"uniform_n{n}","family":"uniform_causal","n":n,"trial":0,"seed":SEED+100000+n})
        for t in range(16):negatives.append({"id":f"qk_n{n}_t{t}","family":"random_qk_causal_softmax","n":n,"trial":t,"seed":SEED+200000+1000*n+t,"d_k":64})
        for k in (51,102,205):
            for trial in range(8):
                for noise in (0.,.01):planted.append({"id":f"segments_n{n}_k{k}_t{trial}_z{int(noise>0)}",
                    "family":"planted_thin_segments","n":n,"k":k,"trial":trial,"noise":noise,
                    "seed":SEED+300000+n*10000+k*100+trial,"fit_seed":SEED+400000+n*10000+k*100+trial,
                    "noise_seed":SEED+500000+n*10000+k*100+trial})
        for rank in (1,2,4,8,16):
            for trial in range(8):lowrank.append({"id":f"masked_rank_n{n}_r{rank}_t{trial}","n":n,"rank":rank,"trial":trial,
                "seed":SEED+600000+n*10000+rank*100+trial})
    return {"negative":negatives,"planted":planted,"masked_positive":lowrank}

def freeze_decay_pool():
    path=ROOT/"empirical_decay_pool.json"
    if path.exists():return read_json(path)
    source=read_json("out/phase19b_selection.json");pools={"128":[],"256":[]}
    for d in source["datasets"]:
        n=d["n"]
        for inst in d["instances"]:
            old=read_json(f"out/phase19b_cache/free/{tag(d['model_slug'],n,inst['archive_index'])}.json")
            for B in [(2*n+1)*r for r in (1,2,4)]:
                row=old["budget"][str(B)];p=np.asarray(row["parameters"])
                active=p[:,4]>1e-8*row["norm_frobenius"]
                pools[str(n)].extend(p[active][:,[0,3]].tolist())
    write_json(path,{"source":"All active free atoms in the first3 budgets of all192 fixed phase19b instances; no outcome filtering",
        "columns":["normal_angle_radians","signed_decay_per_n_pixels"],"pools":pools})
    return read_json(path)

def make(spec,pool=None):
    n=spec["n"];rng=np.random.default_rng(spec["seed"]);family=spec.get("family")
    if family=="uniform_causal":return np.tril(np.ones((n,n)))/np.arange(1,n+1)[:,None],{}
    if family=="random_qk_causal_softmax":
        q=rng.normal(size=(n,spec["d_k"]));k=rng.normal(size=(n,spec["d_k"]));logits=q@k.T/np.sqrt(spec["d_k"])
        logits[np.triu_indices(n,1)]=-np.inf;logits-=np.max(logits,axis=1,keepdims=True)
        a=np.exp(logits);a/=a.sum(axis=1,keepdims=True)
        return a,{"generation":"iid N(0,1) Q,K; QK^T/sqrt(64); exact causal mask then stable row softmax","no_planted_line_structure":True}
    if family=="planted_thin_segments":
        if pool is None:pool=freeze_decay_pool()
        empirical=np.asarray(pool["pools"][str(n)]);k=spec["k"];picked=empirical[rng.integers(len(empirical),size=k)]
        i,j=np.tril_indices(n);anchors=rng.integers(len(i),size=k);x=j[anchors]-(n-1)/2;y=i[anchors]-(n-1)/2
        theta=picked[:,0];rho=x*np.cos(theta)+y*np.sin(theta)
        sigma=np.exp(rng.uniform(np.log(.2),np.log(1.),k));amplitude=rng.lognormal(0,.5,k)/np.sqrt(k)
        truth=np.column_stack([theta,rho,sigma,picked[:,1],amplitude]);clean=line_image(truth,n)
        z=np.random.default_rng(spec["noise_seed"]).normal(size=len(i));z/=np.linalg.norm(z)
        a=clean.copy();a[i,j]+=spec["noise"]*np.linalg.norm(clean)*z
        return a,{"truth":truth.tolist(),"clean_norm_frobenius":float(np.linalg.norm(clean)),
            "generation":"Empirical joint(angle,decay); uniform causal pixel anchors guarantee nonempty footprints; log-uniform sigma[.2,1]; positive lognormal amplitudes",
            "recovery_definition":"relative reconstruction error <=.001 clean or <=.02 for1percent noise, unchanged from E2b; not parameter identifiability"}
    # Exactly masked rank r; row normalization rescales U and preserves masked rank.
    r=spec["rank"];u=rng.lognormal(0,.7,(n,r));v=rng.lognormal(0,.7,(n,r))
    a=np.tril(u@v.T);scale=a.sum(axis=1);u/=scale[:,None];a/=scale[:,None]
    return a,{"latent_U":u.tolist(),"latent_V":v.tolist(),"masked_rank":r,
        "meaning":"A=tril(UV^T), exact latent rank r; A itself generally has full ordinary matrix rank"}
