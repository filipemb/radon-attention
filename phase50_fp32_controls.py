"""Non-archive FP32 algebra/product/planted controls before validation."""
import phase50_fp32_als as als
import argparse,time
import numpy as np
import torch
from phase50_experiment import read
from sampling import sha256_file,write_json_new
import phase2_downstream as harness

def run():
    from phase50_fp32_graph import qr,SmallSVD,solve
    rng=np.random.default_rng(5004);checks=[];support=harness.causal_support(128,128,'cuda')
    for rank in (7,8,15,16):
        a=torch.from_numpy(rng.normal(size=(2,128,rank)).astype('float32')).cuda()
        q,r=qr(a);svd=SmallSVD(2,rank);u,s,vh=svd(r)
        prod=float((q@r-a).norm()/a.norm());orth=float((q.transpose(-1,-2)@q-torch.eye(rank,device='cuda')).norm())
        sd=float(((u*s[:,None,:])@vh-r).norm()/r.norm())
        if int(svd.failures):raise AssertionError('FP32 SVD control status')
        checks.append({'rank':rank,'QR_product_relative_error':prod,'Q_orthogonality_error':orth,'SVD_product_relative_error':sd,
                       'passed':prod<=2e-5 and orth<=2e-5 and sd<=2e-5})
        for reverse in (False,True):
            target=torch.from_numpy(np.tril(rng.normal(size=(2,128,128))).astype('float32')).cuda()
            if reverse:target=target.transpose(-1,-2)
            outer=a.unsqueeze(-1)*a.unsqueeze(-2)
            gram=outer.flip(1).cumsum(1).flip(1) if reverse else outer.cumsum(1)
            rhs=target@a;failed=torch.zeros((),device='cuda',dtype=torch.int32)
            actual=solve(gram,rhs,failed)
            # CPU double solves of the SAME FP32 cumulative Grams and RHS.
            gg=gram.double().cpu().numpy();hh=rhs.double().cpu().numpy()
            trace=np.trace(gg,axis1=-2,axis2=-1)
            # Lambda rounding agrees with FP32 definition before double solve.
            lam=(gram.diagonal(dim1=-2,dim2=-1).sum(-1)*als.RIDGE).clamp_min(1e-30).double().cpu().numpy()
            ref=np.linalg.solve(gg+lam[...,None,None]*np.eye(rank),hh[...,None])[...,0]
            prediction=actual@a.transpose(-1,-2);expected=torch.from_numpy(ref).cuda()@a.double().transpose(-1,-2)
            rel=float(((prediction.double()-expected)*(support.T if reverse else support)).norm()/target.norm())
            checks.append({'rank':rank,'reverse':reverse,'closed_form_prediction_error':rel,'Cholesky_failures':int(failed),
                           'passed':int(failed)==0 and rel<=2e-3})
    rng=np.random.default_rng(5001);planted=[]
    for rank in (8,16):
        uu=rng.lognormal(0,.7,(128,rank));vv=rng.lognormal(0,.7,(128,rank))
        raw=np.tril(uu@vv.T);raw/=raw.sum(-1,keepdims=True)
        a=torch.from_numpy(raw[None]).cuda();init=np.linalg.svd(raw,full_matrices=False)
        initial=(torch.from_numpy((init[0][:,:rank]*np.sqrt(init[1][:rank]))[None]).cuda(),
                 torch.from_numpy((init[2][:rank].T*np.sqrt(init[1][:rank]))[None]).cuda())
        start=time.perf_counter();product,infos=als.fit(a,rank,support,initial,backend='graph')
        err=float(((product.double()-a)*support).norm()/a.norm())
        planted.append({'rank':rank,'relative_recovery_error':err,'passed':err<=.01,'ALS':infos[0],
                        'cold_seconds':time.perf_counter()-start})
        again,ii=als.fit(a,rank,support,initial,backend='graph')
        if not torch.equal(product,again):raise AssertionError('Graph repeated fit changed')
    passed=all(c['passed'] for c in checks) and all(c['passed'] for c in planted)
    result={'passed':passed,'component_checks':checks,'planted':planted,
            'planted_tolerance_declared_in_parent_protocol':.01,'component_tolerance_declared_before_execution':True,
            'protocol_sha256':sha256_file('out/phase50_fp32_protocol.json'),
            'sources':{p:sha256_file(p) for p in ('phase50_fp32_als.py','phase50_fp32_graph.py')},
            'selected_backend':'graph','repeated_graph_fits_bit_equal':True}
    write_json_new('out/phase50_fp32_controls.json',result)
    print('FP32 CONTROL',passed,'planted',[(x['rank'],x['relative_recovery_error']) for x in planted],flush=True)
    if not passed:raise AssertionError('FP32 numerical controls failed; preserved')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--under-gpu-lock',action='store_true');a=p.parse_args()
    if not a.under_gpu_lock:raise RuntimeError('Launch under flock /tmp/radon-gpu.lock')
    run()
