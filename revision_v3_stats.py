"""Versioned statistics for the revision: immutable outputs, whole-unit resampling."""
from sampling import write_json_new, sha256_file, slug, MODELS, CORPUS_PATH
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
import math
import os
import numpy as np
from scipy.stats import binomtest, wilcoxon, rankdata, binom
from scipy.special import logsumexp

SEED=0
N_BOOT=2000
LOG=Path("out/_rerun_logs/v3_progress.md")

def progress(stage,message,seconds=None,command=None):
    LOG.parent.mkdir(parents=True,exist_ok=True)
    line=f"\n- {datetime.now(timezone.utc).isoformat(timespec='seconds')} | {stage}: {message}"
    if seconds is not None:line+=f" | elapsed_seconds={seconds:.6f}"
    if command is not None:line+=f" | command: {command}"
    fd=os.open(LOG,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o666)
    try:os.write(fd,(line+"\n").encode("utf-8"))
    finally:os.close(fd)

@lru_cache(maxsize=12)
def document_draws(n,seed=SEED):
    return np.random.default_rng(seed).integers(0,n,size=(N_BOOT,n))

def describe(values,document_indices,seed=SEED,document_universe=None):
    """phase24.describe, generalized to unequal/empty document blocks.

    Balanced blocks use the exact same RNG draws and pooled median. For
    ragged blocks, integer multiplicities compute the median of the actual
    concatenation of resampled blocks, without balancing or dropping heads.
    An empty bootstrap population makes the unconditional CI undefined.
    """
    a=np.asarray(values,dtype=np.float64);docs=np.asarray(document_indices)
    if a.ndim!=1 or docs.shape!=a.shape or not np.isfinite(a).all():
        raise ValueError("Invalid metric; nonfinite observations cannot be omitted")
    universe=np.unique(docs) if document_universe is None else np.asarray(document_universe)
    if universe.ndim!=1 or len(np.unique(universe))!=len(universe):
        raise ValueError("Document universe must be unique")
    mapping={v:i for i,v in enumerate(universe.tolist())}
    if any(d not in mapping for d in docs.tolist()):raise ValueError("Unknown document")
    inv=np.asarray([mapping[d] for d in docs.tolist()],dtype=np.int64)
    sizes=np.bincount(inv,minlength=len(universe))
    result={"median":float(np.median(a)) if len(a) else None,
        "p25":float(np.percentile(a,25)) if len(a) else None,
        "p75":float(np.percentile(a,75)) if len(a) else None,
        "mean":float(a.mean()) if len(a) else None,
        "std":float(a.std(ddof=1)) if len(a)>1 else None,
        "mean_of_document_means_secondary":float(np.mean([a[inv==i].mean() for i in range(len(universe)) if sizes[i]])) if len(a) else None,
        "n_instances":len(a),"n_documents":int(np.count_nonzero(sizes)),
        "n_document_blocks_resampled":len(universe),"document_block_sizes":sizes.tolist(),
        "bootstrap_seed":seed,"n_bootstrap":N_BOOT,"median_ci_document_bootstrap":None,
        "bootstrap_empty_draws":N_BOOT if not len(a) else 0,
        "block_rule":"whole original documents, including empty blocks after declared stratification/exclusion"}
    if not len(a):
        result["undefined_reason"]="No defined observations in this stratum"
        return result
    draws=document_draws(len(universe),seed)
    if sizes.min()==sizes.max() and sizes.min()>0:
        blocks=np.stack([a[inv==i] for i in range(len(universe))])
        boots=np.median(blocks[draws].reshape(N_BOOT,-1),axis=1)
    else:
        counts=np.zeros((N_BOOT,len(universe)),dtype=np.int64)
        np.add.at(counts,(np.arange(N_BOOT)[:,None],draws),1)
        order=np.argsort(a,kind="stable")
        cumulative=np.cumsum(counts[:,inv[order]],axis=1)
        totals=cumulative[:,-1];empty=totals==0
        result["bootstrap_empty_draws"]=int(empty.sum())
        left=np.argmax(cumulative>((totals-1)//2)[:,None],axis=1)
        right=np.argmax(cumulative>(totals//2)[:,None],axis=1)
        boots=(a[order[left]]+a[order[right]])/2
        if empty.any():
            result["undefined_reason"]="Some full-document bootstrap draws have no defined observations; no conditional CI substituted"
            return result
    result["median_ci_document_bootstrap"]=np.percentile(boots,[2.5,97.5]).tolist()
    return result

def fraction_summary(indicator,docs,document_universe):
    a=np.asarray(indicator,dtype=np.int64);docs=np.asarray(docs)
    universe=np.asarray(document_universe);mapping={v:i for i,v in enumerate(universe.tolist())}
    inv=np.asarray([mapping[d] for d in docs.tolist()])
    numerator=np.bincount(inv,weights=a,minlength=len(universe))
    denominator=np.bincount(inv,minlength=len(universe))
    draws=document_draws(len(universe))
    boots=numerator[draws].sum(1)/denominator[draws].sum(1)
    return {"n_instances":len(a),"n_in_stratum":int(a.sum()),"fraction":float(a.mean()),
            "fraction_ci_document_bootstrap":np.percentile(boots,[2.5,97.5]).tolist(),
            "n_documents":len(universe),"n_bootstrap":N_BOOT,"bootstrap_seed":SEED}

def paired_wilcoxon(differences,units):
    a=np.asarray(differences,dtype=np.float64);u=np.asarray(units)
    if not np.isfinite(a).all():raise ValueError("Nonfinite paired difference")
    unique=np.unique(u);per_unit=np.asarray([np.median(a[u==d]) for d in unique])
    nonzero=per_unit[per_unit!=0]
    if len(nonzero):
        test=wilcoxon(per_unit,zero_method="wilcox",alternative="two-sided",method="asymptotic")
        ranks=rankdata(np.abs(nonzero));effect=float((ranks[nonzero>0].sum()-ranks[nonzero<0].sum())/ranks.sum())
        statistic=float(test.statistic);pvalue=float(test.pvalue)
    else:statistic,pvalue,effect=0.,1.,0.
    return {"summary":describe(a,u),"n_independent_units":len(unique),
        "n_nonzero_units":len(nonzero),"zero_method":"wilcox",
        "statistic":statistic,"pvalue":pvalue,"rank_biserial_left_minus_right":effect,
        "method":"two-sided Wilcoxon on median paired difference per independent unit; asymptotic with tie correction"}

def holm(pvalues):
    values=np.asarray(pvalues,dtype=np.float64)
    if not np.isfinite(values).all() or ((values<0)|(values>1)).any():raise ValueError("Invalid p-value")
    result=np.empty_like(values);running=0.
    for rank,index in enumerate(np.argsort(values,kind="stable")):
        running=max(running,min(1.,(len(values)-rank)*values[index]));result[index]=running
    return result.tolist()

def mcnemar(baseline,edited):
    b=np.asarray(baseline,dtype=bool);e=np.asarray(edited,dtype=bool)
    if b.shape!=e.shape or b.ndim!=1:raise ValueError("Unpaired items")
    plus=int((~b&e).sum());minus=int((b&~e).sum())
    return {"n_pairs":len(b),"edited_only_correct":plus,"baseline_only_correct":minus,
            "baseline_n_correct":int(b.sum()),"edited_n_correct":int(e.sum()),
            "accuracy_gain":(plus-minus)/len(b),
            "mcnemar_exact_pvalue":float(binomtest(plus,plus+minus,.5).pvalue) if plus+minus else 1.}

def seed_stratified_permutation(seed_results):
    """Exact paired-label permutation, statistic median(seed accuracy gains).

    Labels swap within each item, retaining seed membership and denominators.
    Conditional on discordances, each seed's signed sum is 2*Binomial(d,.5)-d.
    For three seeds, a median tail requires at least two seed tails.
    """
    from fractions import Fraction
    if len(seed_results)!=3:raise ValueError("Predeclared combined test has three seed blocks")
    gains=[Fraction(r["edited_only_correct"]-r["baseline_only_correct"],r["n_pairs"]) for r in seed_results]
    observed=sorted(gains)[1];threshold=abs(observed)
    if threshold==0:logp=0.
    else:
        tails=[]
        for r in seed_results:
            n=r["edited_only_correct"]+r["baseline_only_correct"]
            k=math.ceil((Fraction(n)+threshold*r["n_pairs"])/2)
            tails.append(float(logsumexp(binom.logpmf(np.arange(k,n+1),n,.5))) if k<=n else -math.inf)
        terms=[]
        for i,j,k in [(0,1,2),(0,2,1),(1,2,0)]:
            terms.append(tails[i]+tails[j]+math.log1p(-math.exp(tails[k])))
        terms.append(sum(tails))
        logp=min(0.,math.log(2)+float(logsumexp(terms)))
    return {"statistic_median_seed_gain":float(observed),"pvalue":math.exp(logp),"log_pvalue":logp,
        "method":"exact paired label swaps within seed; median of three seed-specific accuracy gains",
        "n_seed_blocks":3,"n_pairs":sum(r["n_pairs"] for r in seed_results),
        "no_item_moves_between_seeds":True}

def bootstrap_item_gains(records):
    """Resample paired items within fixed seed x position cells."""
    seeds=sorted({r["seed"] for r in records});rng=np.random.default_rng(SEED)
    draws={s:np.zeros((N_BOOT,4),dtype=np.int64) for s in seeds};totals={}
    for seed in seeds:
        selected=[r for r in records if r["seed"]==seed];totals[seed]=len(selected)
        for pos in sorted({r["position"] for r in selected}):
            rows=[r for r in selected if r["position"]==pos]
            cats=[2*int(r["baseline_correct"])+int(r["edited_correct"]) for r in rows]
            counts=np.bincount(cats,minlength=4)
            draws[seed]+=rng.multinomial(len(rows),counts/len(rows),size=N_BOOT)
    effects=np.stack([(draws[s][:,1]-draws[s][:,2])/totals[s] for s in seeds],axis=1)
    point=[np.mean([int(r["edited_correct"])-int(r["baseline_correct"]) for r in records if r["seed"]==s]) for s in seeds]
    pooled=np.sum(np.stack([draws[s][:,1]-draws[s][:,2] for s in seeds],axis=1),axis=1)/len(records)
    d=np.asarray([int(r["edited_correct"])-int(r["baseline_correct"]) for r in records])
    return {"n_independent_items":len(records),"n_seed_blocks":len(seeds),
        "median_item_difference":float(np.median(d)),
        "median_seed_accuracy_gain":float(np.median(point)),
        "median_seed_gain_ci95_item_bootstrap":np.percentile(np.median(effects,axis=1),[2.5,97.5]).tolist(),
        "pooled_accuracy_gain_secondary":float(d.mean()),
        "pooled_gain_ci95_item_bootstrap_secondary":np.percentile(pooled,[2.5,97.5]).tolist(),
        "bootstrap_seed":SEED,"n_bootstrap":N_BOOT,
        "bootstrap_strata":"seed x position; paired Bernoulli cells resampled jointly as independent items",
        "binary_metric_note":"Accuracy is correct-count/n; raw binary medians and median seed gain are exposed, pooled mean gain is secondary."}
