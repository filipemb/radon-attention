"""CPU-double diagnostic of factor scales on a preserved failed FP32 input.

This is not a forward estimator or a replacement of any missing KL.
"""
import phase50_als
import time
import numpy as np
from phase50_experiment import read
from sampling import write_json_new,sha256_file

def main():
    p='out/phase50_declared_failed_ALS_input_Qwen05_docs4_6.json';src=read(p)
    a=np.array(src['input_A'],dtype=np.float64);norms=np.linalg.norm(a,axis=(-2,-1));target=a/norms[:,None,None]
    u=np.array(src['initial_U_recomputed'],dtype=np.float64)/np.sqrt(norms[:,None,None])
    v=np.array(src['initial_V_recomputed'],dtype=np.float64)/np.sqrt(norms[:,None,None])
    eye=np.eye(16);hist=[];tick=time.perf_counter();threshold=np.sqrt(np.finfo(np.float32).max)
    def update(aa,f,reverse=False):
        pp=f[:,:,:,None]*f[:,:,None,:]
        g=np.cumsum(pp[:,::-1],axis=1)[:,::-1] if reverse else np.cumsum(pp,axis=1)
        lam=np.maximum(1e-6*np.trace(g,axis1=-2,axis2=-1),1e-30)
        return np.linalg.solve(g+lam[:,: ,None,None]*eye,(aa@f)[...,None])[...,0]
    for step in range(1,201):
        cu=update(target,v);cv=update(target.transpose(0,2,1),cu,True)
        qu,ru=np.linalg.qr(cu);qv,rv=np.linalg.qr(cv)
        left,s,vh=np.linalg.svd(ru@rv.transpose(0,2,1),full_matrices=False)
        root=np.sqrt(s)[:,None,:];u=(qu@left)*root;v=(qv@vh.transpose(0,2,1))*root
        norms_u=np.linalg.norm(cu,axis=1);norms_v=np.linalg.norm(cv,axis=1)
        hist.append({'sweep':step,'pre_QR_max_abs_U':float(np.abs(cu).max()),'pre_QR_max_abs_V':float(np.abs(cv).max()),
            'pre_QR_max_column_norm_U':float(norms_u.max()),'pre_QR_max_column_norm_V':float(norms_v.max()),
            'columns_with_norm_square_beyond_FP32_range':int((norms_u>threshold).sum()+(norms_v>threshold).sum()),
            'balanced_maximum_absolute_factor':float(max(np.abs(u).max(),np.abs(v).max())),
            'maximum_raw_causal_relative_residual':float(np.linalg.norm(np.tril(u@v.transpose(0,2,1))-target,axis=(-2,-1)).max())})
    out={'diagnostic_only_no_behavioral_score':True,'input_sha256':sha256_file(p),'dtype':'float64_CPU',
        'same_trace_ridge':1e-6,'sweeps':200,'different_precision_trajectory_not_asserted_identical_to_failed_FP32':True,
        'FP32_naive_square_norm_overflow_column_norm_threshold':float(threshold),'history':hist,'elapsed_seconds':time.perf_counter()-tick}
    write_json_new('out/phase50_declared_CPU_failure_geometry.json',out)
    print('CPU diagnostic complete; max U/V',max(h['pre_QR_max_abs_U'] for h in hist),max(h['pre_QR_max_abs_V'] for h in hist),flush=True)

if __name__=='__main__':main()
