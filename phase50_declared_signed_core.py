"""Canonicalize a signed native SVD without changing its matrix product.

L diag(s) Vh = L diag(abs(s)) (diag(sign(s)) Vh). This handles a
negative finite native singular value before taking its square root. No
clamping, no NaN replacement, no ALS parameter or positive-path change.
"""
import torch
import phase50_fp32_als as als
import phase50_fp32_graph as base

_installed=False
_last=None

def canonical(left,s,vh):
    signs=torch.where(s<0,-torch.ones_like(s),torch.ones_like(s))
    return left,s.abs(),vh*signs[:,:,None]

def install():
    global _installed
    if _installed:return
    if base._cache:raise RuntimeError('Install signed-core canonicalization before any graph is cached')
    old_init=base.SmallSVD.__init__;old_call=base.SmallSVD.__call__;old_execute=base.SweepGraph.execute;old_fit=als.fit
    def init(self,*args,**kwargs):
        old_init(self,*args,**kwargs)
        self.negative_finite_singular_values=torch.zeros(self.batch,device='cuda',dtype=torch.int64)
    def call(self,a):
        left,s,vh=old_call(self,a)
        self.negative_finite_singular_values.add_(((s<0)&torch.isfinite(s)).sum(-1))
        return canonical(left,s,vh)
    def execute(self,target,u,v):
        global _last
        self.svd.negative_finite_singular_values.zero_()
        result=old_execute(self,target,u,v)
        _last=self.svd.negative_finite_singular_values.cpu().tolist()
        return result
    def fit(a,rank,support,initial=None,backend='torch'):
        if backend!='graph':raise ValueError('Declared signed-core implementation uses graph backend')
        product,infos=old_fit(a,rank,support,initial,backend)
        for j,info in enumerate(infos):
            info['core_SVD_signed_values_reparameterized']=int(_last[j])
            info['core_SVD_repair']='move a negative finite singular-value sign to its right singular vector before sqrt; product preserved'
        return product,infos
    base.SmallSVD.__init__=init;base.SmallSVD.__call__=call;base.SweepGraph.execute=execute;als.fit=fit;_installed=True
