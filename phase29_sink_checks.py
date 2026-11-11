"""CPU adversarial checks for reconstruction completion and sink editing."""
from sampling import write_json_new, progress
import argparse
import time
from types import SimpleNamespace
import torch
import phase2_downstream as p2
import phase8_lostmiddle as p8
import phase10_baselines as p10
import phase14_adaptive as p14

torch.set_num_threads(4)

def legacy_edit(weights,mode,beta):
    aw = weights.clone()
    if mode in ("oursink","fixed"):
        aw[...,0] *= beta
    elif mode=="adaptive":
        c0 = aw[...,0].mean(-1)
        med = c0.median(-1,keepdim=True).values
        aw[...,0] *= (med/c0.clamp_min(1e-9)).clamp(max=1).unsqueeze(-1)
    elif mode=="act":
        c = aw.mean(-2)
        threshold = c.mean(-1,keepdim=True)+3*c.std(-1,keepdim=True)
        aw = torch.where((c>threshold).unsqueeze(-2).expand_as(aw),aw*beta,aw)
    else:
        raise ValueError(mode)
    return aw/aw.sum(-1,keepdim=True).clamp_min(1e-9)

def check():
    torch.manual_seed(0)
    output = {"all_passed":False,"positive_beta_cases":[],"zero_beta_cases":[],
              "reconstruction_completion":[],"inheritance":{}}
    for dtype in (torch.float32,torch.bfloat16):
        logits = torch.randn(2,4,64,64).to(dtype)
        support = torch.ones(64,64,dtype=torch.bool).tril()
        weights = logits.masked_fill(~support,float("-inf")).softmax(-1)
        for beta in (.05,.1,.15,.25,.5,.75,1.):
            edited = weights.clone();edited[...,0] *= beta
            stats = {}
            new = p8.finish_sink_edit(weights,edited,stats)
            old = legacy_edit(weights,"oursink",beta)
            assert torch.equal(new,old)
            for module,modes in ((p10,("oursink","act")),(p14,("fixed","adaptive","act"))):
                for mode in modes:
                    module.RECON.update(mode=mode,beta=beta,stats={})
                    assert torch.equal(module.reconstruct(weights),legacy_edit(weights,mode,beta))
            output["positive_beta_cases"].append({"dtype":str(dtype),"beta":beta,
                "phase8_10_14_bit_equal_to_legacy":True,"max_absolute_difference":0.,
                "max_row_sum_error":stats["max_sink_edit_row_error"],
                "fixed_dtype_arithmetic_bound":stats["max_sink_edit_row_error_bound"]})
        before = torch.zeros(1,2,5,5,dtype=dtype)
        before[...,0,0]=1;before[...,1,0]=1
        before[...,2,0]=.3;before[...,2,1]=.2;before[...,2,2]=.5
        before[...,3,0]=1;before[...,4,0]=1;before[...,4,4]=1e-15
        edited = before.clone();edited[...,0]=0
        stats = {}
        new = p8.finish_sink_edit(before,edited,stats)
        assert torch.equal(new[...,:2,:],before[...,:2,:])
        assert torch.equal(new[...,3,:],before[...,3,:])
        assert (new[...,4,4]==1).all() and (new[...,4,0]==0).all()
        assert stats["sink_edit_rows_preserved_no_alternative"]==6
        assert stats["sink_edit_last_query_rows_preserved"]==0
        assert stats["sink_edit_positive_mass_below_legacy_clamp"]==2
        for module,modes in ((p10,("oursink","act")),(p14,("fixed","adaptive","act"))):
            for mode in modes:
                module.RECON.update(mode=mode,beta=0.,stats={})
                a = module.reconstruct(before)
                assert torch.equal(a[...,0,:],before[...,0,:])
                assert torch.isfinite(a).all() and (a>=0).all()
        output["zero_beta_cases"].append({"dtype":str(dtype),"first_and_other_no_alternative_rows_unchanged":True,
            "tiny_positive_mass_normalized_without_preserving_sink":True,"stats":stats})
    # Cached attention: the first query already has multiple causal keys.
    before = torch.ones(2,3,3,7).masked_fill(~torch.ones(3,7,dtype=torch.bool).tril(4),0)
    before /= before.sum(-1,keepdim=True)
    before[...,1,:]=0;before[...,1,0]=1
    edited = before.clone();edited[...,0]=0
    stats={};new = p8.finish_sink_edit(before,edited,stats)
    assert torch.equal(new[...,1,:],before[...,1,:])
    assert (new[...,0,0]==0).all() and (new[...,0,1:5]==.25).all()
    output["cached_sink_edit"]={"q":3,"k":7,"offset":4,"passed":True,"stats":stats}
    # Poisoned original values prove reconstruction completion never copies them.
    for q,k in ((5,5),(3,7),(1,7)):
        rec = torch.zeros(2,3,q,k)
        original = torch.full_like(rec,float("nan"))
        stats={}
        result = p2.normalize_reconstruction(rec,original,stats)
        support = torch.ones(q,k,dtype=torch.bool).tril(k-q)
        expected = support.float()/support.sum(-1,keepdim=True)
        assert torch.equal(result,expected.expand_as(result))
        counts = p2.completion_summary(stats)
        assert counts["rows_total"]==counts["rows_completed"]==2*3*q
        assert counts["last_query_rows_total"]==counts["last_query_rows_completed"]==6
        assert counts["fraction_rows_completed"]==counts["fraction_last_query_rows_completed"]==1.
        output["reconstruction_completion"].append({"q":q,"k":k,"uniform_even_with_poisoned_original":True,"counts":counts})
    # Nonfinite reconstruction is an error, not a reason to complete uniformly.
    bad = torch.eye(5).unsqueeze(0);bad[0,2,1]=float("nan")
    try:
        p2.normalize_reconstruction(bad,torch.eye(5).unsqueeze(0),{})
    except RuntimeError as e:
        assert "Nonfinite" in str(e)
        output["nonfinite_reconstruction_rejected"]=True
    else:
        raise AssertionError("Nonfinite reconstruction was accepted")
    for name in ("phase11_kv","phase16_longcontext","phase18_betacv"):
        mod=__import__(name)
        assert mod.recon_attention_forward is p8.recon_attention_forward
        assert mod.P8.RECON is p8.RECON
        output["inheritance"][name]="same repaired callback and state object"
    output["all_passed"]=True
    return output

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="out/phase29_sink_checks_v2.json")
    args=ap.parse_args()
    started=time.perf_counter()
    result=check();result["elapsed_seconds"]=time.perf_counter()-started
    write_json_new(args.out,result)
    progress("V1 sink regression", "Positive beta bit equality, beta0 no-alternative rows, cached offsets, tiny mass, uniform completion and inheritance passed",
             result["elapsed_seconds"],".venv/Scripts/python.exe -B phase29_sink_checks.py")
    print("All sink/completion regression checks passed",flush=True)

if __name__=="__main__":
    main()
