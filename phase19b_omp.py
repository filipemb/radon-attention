"""Extend parent NNLS-OMP prefixes without recomputing completed greedy steps."""
import phase19b_common
import time
import numpy as np
from scipy import linalg
from richlines_core import NNLSActive


def extend(b,dictionary,parent_results,checkpoints):
    begin=time.perf_counter();b=np.asarray(b,dtype=float);norm=float(np.linalg.norm(b));target=b/norm
    D=dictionary.D;parent={int(k):v for k,v in parent_results.items()}
    result={k:parent[k] for k in checkpoints if k in parent};needed=[k for k in checkpoints if k not in result]
    if not needed:return result,{"seconds":time.perf_counter()-begin,"extended_steps":0}
    first=min(needed);last=max(parent)
    # A stored later checkpoint contains the exact greedy index prefix, but
    # its amplitudes require an NNLS refit after truncation.
    start_count=min(first,last)
    later=parent[min(k for k in parent if k>=start_count)]
    selected=list(later["support"]["indices"][:start_count]);m=len(selected)
    G=np.zeros((max(checkpoints),max(checkpoints)))
    sub=D[selected];G[:m,:m]=(sub@sub.T).toarray();h_all=np.asarray(D@target)
    state=NNLSActive();x=np.zeros(m)
    if m:
        x,_=state.refit(G[:m,:m],h_all[selected],x)
    residual=target-np.asarray(D[selected].T@x).ravel()
    start_kkt=float(np.max(np.abs(np.minimum(G[:m,:m]@x-h_all[selected],x)))) if m else 0.
    if start_kkt>1e-7:raise AssertionError("Resumed prefix NNLS did not satisfy KKT")
    def snapshot(k,stationary=False):
        error=float(np.linalg.norm(residual));grad=G[:len(selected),:len(selected)]@x-h_all[selected]
        return {"relative":error,"absolute":norm*error,"selected":len(selected),
            "active":int((x>1e-9).sum()),"stationary":stationary,
            "active_nnls_kkt":float(np.max(np.abs(np.minimum(grad,x)))) if len(x) else 0.,
            "support":{"indices":selected.copy(),"amplitudes":(norm*x).tolist()}}
    if start_count in needed:result[start_count]=snapshot(start_count)
    executed=0
    for step in range(m+1,max(checkpoints)+1):
        corr=np.asarray(D@residual);corr[selected]=-np.inf;candidate=int(np.argmax(corr))
        if corr[candidate]<=1e-10:
            for k in needed:
                if k>=step:result[k]=snapshot(k,True)
            break
        atom=dictionary.atom(candidate)
        if selected:
            cross=np.asarray(D[selected]@atom);G[step-1,:step-1]=cross;G[:step-1,step-1]=cross
        G[step-1,step-1]=atom@atom;selected.append(candidate)
        x,_=state.refit(G[:step,:step],h_all[selected],np.r_[x,0.])
        residual=target-np.asarray(D[selected].T@x).ravel();executed+=1
        if step in needed:result[step]=snapshot(step)
    if set(result)!=set(checkpoints):raise AssertionError("Missing greedy initialization checkpoint")
    return result,{"seconds":time.perf_counter()-begin,"extended_steps":executed,
        "initial_selected_atoms":m,"initial_nnls_kkt":start_kkt,
        "rule":"same 180-angle dictionaries and nonnegative OMP; exact selected-index prefix, NNLS refit, then greedy continuation; parent snapshots retained verbatim"}
