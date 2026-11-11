"""Recover an invalid native singular value from its finite core/vectors.

s_i = u_i^T C v_i, computed in FP32 on the same KxK core. Only invalid native
values are recomputed; every ordinary finite nonnegative native value is kept.
No ridge/rank/sweep changes, no zero imputation, no CPU ALS fallback.
"""
import torch
import phase50_fp32_als as als
import phase50_fp32_graph as base

_installed=False
_last=None

def corrected_values(a,left,s,vh):
    invalid=(~torch.isfinite(s))|(s<0)
    rayleigh=(left.transpose(-1,-2)@a@vh.transpose(-1,-2)).diagonal(dim1=-2,dim2=-1)
    selected=torch.where(invalid,rayleigh,s)
    signs=torch.where(selected<0,-torch.ones_like(selected),torch.ones_like(selected))
    return left,selected.abs(),vh*signs[:,:,None],invalid

def install():
    global _installed
    if _installed:return
    if base._cache:raise RuntimeError('Install numerical SVD correction before any graph is cached')
    old_init=base.SmallSVD.__init__;old_call=base.SmallSVD.__call__;old_execute=base.SweepGraph.execute;old_fit=als.fit
    def init(self,*args,**kwargs):
        old_init(self,*args,**kwargs);self.invalid_values_recomputed=torch.zeros(self.batch,device='cuda',dtype=torch.int64)
    def call(self,a):
        left,s,vh=old_call(self,a);ll,ss,rr,bad=corrected_values(a,left,s,vh)
        self.invalid_values_recomputed.add_(bad.sum(-1))
        return ll,ss,rr
    def execute(self,target,u,v):
        global _last
        self.svd.invalid_values_recomputed.zero_();result=old_execute(self,target,u,v)
        _last=self.svd.invalid_values_recomputed.cpu().tolist();return result
    def fit(a,rank,support,initial=None,backend='torch'):
        if backend!='graph':raise ValueError('The declared numerical correction uses the graph backend')
        product,infos=old_fit(a,rank,support,initial,backend)
        for j,info in enumerate(infos):
            info['invalid_native_core_singular_values_recomputed']=int(_last[j])
            info['core_SVD_numerical_correction']='Recompute invalid s_i as u_i.T @ core @ v_i in FP32; preserve every ordinary native value'
        return product,infos
    base.SmallSVD.__init__=init;base.SmallSVD.__call__=call;base.SweepGraph.execute=execute;als.fit=fit;_installed=True
