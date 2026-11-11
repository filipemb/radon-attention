"""Inspect the native small-core SVD at the first actual failure; no scoring."""
import phase50_fp32_als
import phase50_fp32_graph as gg
import argparse
import torch
import phase2_downstream as harness
from phase50_experiment import read
from phase50_declared_trace_failure import stage_update,summary
from sampling import write_json_new,sha256_file

@torch.inference_mode()
def main():
    p='out/phase50_declared_first_failure_trace.json';data=read(p)
    target=torch.tensor(data['target_normalized'],device='cuda',dtype=torch.float32)
    v=torch.tensor(data['pre_failure_V'],device='cuda',dtype=torch.float32)
    cu,first=stage_update(target,v,False);cv,second=stage_update(target.transpose(-1,-2),cu,True)
    q,r=gg.qr(torch.cat((cu,cv),0));qu,qv=q.chunk(2);ru,rv=r.chunk(2);core=ru@rv.transpose(-1,-2)
    solver=gg.SmallSVD(len(core),16);left,s,vh=solver(core)
    root=s.sqrt();uu=(qu@left)*root[:,None,:];vv=(qv@vh.transpose(-1,-2))*root[:,None,:]
    negatives=(s<0).nonzero().cpu().tolist();nonfinites=(~torch.isfinite(s)).nonzero().cpu().tolist()
    bad_batches=(~torch.isfinite(uu).all((-2,-1))|~torch.isfinite(vv).all((-2,-1))).nonzero().flatten().cpu().tolist()
    result={'first_failure_trace_sha256':sha256_file(p),'sweep':data['first_failed_sweep'],
        'core':summary(core),'native_info':solver.info.cpu().tolist(),'native_accumulated_failures':int(solver.failures),
        'native_left_vectors':summary(left),'native_right_vectors':summary(vh),'singular_values':summary(s),
        'negative_singular_indices':negatives,'nonfinite_singular_indices':nonfinites,'sqrt_singular_values':summary(root),
        'balanced_U':summary(uu),'balanced_V':summary(vv),'bad_matrix_indices':bad_batches,
        'singular_values_bits':s.contiguous().view(torch.int32).cpu().tolist(),
        'core_bits_for_bad_matrices':{str(b):core[b].contiguous().view(torch.int32).cpu().tolist() for b in bad_batches},
        'diagnostic_only_no_KL_NLL':True,'all_input_and_QR_values_finite':all(z['nonfinite']==0 for z in [summary(cu),summary(cv),summary(q),summary(r),summary(core)])}
    # Also preserve the actual captured cuSOLVER outputs. Rank-deficient
    # subnormal behavior can differ from an isolated eager library call.
    old_init=gg.SmallSVD.__init__;old_call=gg.SmallSVD.__call__
    def init(self,*args,**kwargs):
        old_init(self,*args,**kwargs);self.diagnostic_original_core=torch.empty_like(self.a)
    def call(self,a):
        self.diagnostic_original_core.copy_(a);return old_call(self,a)
    gg.SmallSVD.__init__=init;gg.SmallSVD.__call__=call
    iu=torch.tensor(data['initial_U_normalized'],device='cuda',dtype=torch.float32)
    iv=torch.tensor(data['initial_V_normalized'],device='cuda',dtype=torch.float32)
    graph=gg.SweepGraph(target,iu,iv,harness.causal_support(128,128,'cuda'))
    graph.target.copy_(target);graph.u.copy_(iu);graph.v.copy_(iv);graph.iteration.zero_()
    graph.failures.zero_();graph.nonfinite.zero_();graph.svd.failures.zero_()
    captured_step=None
    for step in range(1,201):
        graph.graph.replay()
        flags=torch.stack((graph.failures.long(),graph.nonfinite,graph.svd.failures)).cpu().tolist()
        if any(flags):captured_step=step;break
    cs=graph.svd.s;cl=graph.svd.v.transpose(-1,-2);cvh=graph.svd.u;ccore=graph.svd.diagnostic_original_core
    result['captured_replay']={'first_failed_sweep':captured_step,'flags':flags,
        'native_info':graph.svd.info.cpu().tolist(),'native_left_vectors':summary(cl),'native_right_vectors':summary(cvh),
        'singular_values':summary(cs),'negative_singular_indices':(cs<0).nonzero().cpu().tolist(),
        'nonfinite_singular_indices':(~torch.isfinite(cs)).nonzero().cpu().tolist(),
        'singular_values_bits':cs.contiguous().view(torch.int32).cpu().tolist(),
        'core_bits':ccore.contiguous().view(torch.int32).cpu().tolist(),
        'left_vector_bits':cl.contiguous().view(torch.int32).cpu().tolist(),
        'right_vector_bits':cvh.contiguous().view(torch.int32).cpu().tolist()}
    if negatives and not nonfinites and not result['native_left_vectors']['nonfinite'] and not result['native_right_vectors']['nonfinite']:
        sign=torch.where(s<0,-torch.ones_like(s),torch.ones_like(s));abs_s=s.abs();new_vh=vh*sign[:,:,None]
        signed_product=(left*s[:,None,:])@vh;positive_product=(left*abs_s[:,None,:])@new_vh
        rr=abs_s.sqrt()[:,None,:];new_u=(qu@left)*rr;new_v=(qv@new_vh.transpose(-1,-2))*rr
        result['signed_SVD_equivalent_reparameterization']={'core_product_bit_equal':torch.equal(signed_product,positive_product),
            'core_reconstruction_relative_error':float((positive_product.double()-core.double()).norm()/core.double().norm()),
            'finite_balanced_factors':bool(torch.isfinite(new_u).all() and torch.isfinite(new_v).all()),
            'same_signed_product_not_clamping_or_nan_replacement':True}
    write_json_new('out/phase50_declared_native_core_SVD_failure.json',result)
    print('CORE SVD DIAG',negatives,nonfinites,'bad matrices',bad_batches,'info',result['native_info'],flush=True)
    if 'signed_SVD_equivalent_reparameterization' in result:print(result['signed_SVD_equivalent_reparameterization'],flush=True)
    gg.SmallSVD.__init__=old_init;gg.SmallSVD.__call__=old_call
    captured=result['captured_replay']
    if (captured['negative_singular_indices'] and not captured['nonfinite_singular_indices']
            and not captured['native_left_vectors']['nonfinite'] and not captured['native_right_vectors']['nonfinite']):
        from phase50_declared_signed_core_control import run as validate_repair
        validate_repair()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--under-gpu-lock',action='store_true');a=p.parse_args()
    if not a.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
    main()
