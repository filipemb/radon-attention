"""Toy counterexamples ensure the primary statistic is genuinely paired."""
import phase19c_common
from phase19c_analysis import paired,holm
from phase19c_common import write_json

def main():
    t=paired([0.,10.,11.],[0.,1.,20.],["a","b","c"])
    if t["paired_effect"]["median"]!=0 or t["fraction_instances_a_wins"]!=1/3:raise AssertionError("Used difference of marginal medians")
    unequal=paired([1.,9.,4.],[0.,0.,0.],["a","a","b"])
    if unequal["paired_effect"]["median"]!=4.5:raise AssertionError("Documents were weighted by instance count")
    missing=paired([None,.1,.4],[.2,.2,.3],["a","b","c"])
    if missing["paired_effect"]["median"] is not None or missing["undefined_pairs"]!=1 or missing["paired_effect"]["undefined_count"]!=1:
        raise AssertionError("Undefined codec was imputed or excluded")
    family=[{"wilcoxon_p":v} for v in [.001,.01,.04,.2,None,None]];holm(family,6)
    expected=[.006,.05,.16,.6,None,None]
    for row,v in zip(family,expected):
        actual=row["wilcoxon_p_holm"]
        if (actual is None)!=(v is None) or actual is not None and abs(actual-v)>1e-12:raise AssertionError("Incorrect planned Holm family")
    ties=paired([1.,2.],[1.,2.],["a","b"])
    if ties["wilcoxon_p"]!=1 or ties["fraction_ties"]!=1:raise AssertionError("All-ties convention changed")
    write_json("out/phase19c_statistics_validation.json",{"passed":True,"paired_not_marginal":True,"document_weighting":True,
        "undefined_codec_not_imputed_or_conditioned":True,"Holm_uses_full_planned_family_with_missing_codecs":True,"all_ties_explicit":True})

if __name__=="__main__":main()
