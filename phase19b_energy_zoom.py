"""Additional percent-scale view; preserve the original zero-to-one figure."""
import phase19b_common
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from phase19b_common import read_json,digest,write_json,RANKS,budgets


def main():
    report=read_json("out/phase19b_richlines.json")
    audit=read_json("out/phase19b_integrity_audit.json")
    if not audit["passed"] or digest("out/phase19b_richlines.json")!=audit["report_sha256"]:
        raise AssertionError("Audited report required")
    paths=[Path("out/phase19b_broad_energy_zoom."+ext) for ext in ("png","svg")]
    if any(p.exists() for p in paths) or Path("out/phase19b_energy_zoom.json").exists():
        raise FileExistsError("Energy zoom already exists")
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,n in zip(axes,(128,256)):
        summaries=report["extension_parameter_diagnostics_by_n"][str(n)]["free"]["by_budget"]
        upper=0.
        for threshold,color in zip((2.,8.,n/8),("#2864a0","#d17a18","#7c3fa3")):
            rows=[summaries[str(B)]["wide_energy_share"][str(threshold)]["additive_share"] for B in budgets(n)]
            y=[100*s["median"] for s in rows]
            low=[100*s["median_ci95_document_block"][0] for s in rows]
            high=[100*s["median_ci95_document_block"][1] for s in rows]
            upper=max(upper,max(high))
            ax.plot(RANKS,y,"o-",color=color,label=f"sigma > {threshold:g} px")
            ax.fill_between(RANKS,low,high,color=color,alpha=.13)
        ax.set_xscale("log",base=2);ax.set_xticks(RANKS,labels=[str(r) for r in RANKS])
        ax.set_ylim(0,1.15*upper if upper>0 else .01)
        ax.set_title(f"Livre | n={n} | 96 instâncias")
        ax.set_xlabel("Posto SVD equivalente: B = r(2n+1)")
        ax.set_ylabel("Energia atribuída a átomos largos (%)")
        ax.legend(fontsize=8);ax.grid(alpha=.2)
    fig.suptitle("Zoom percentual: <larga,total>/||total||²\nMediana e IC95% com blocos por documento; eixos verticais têm escalas distintas")
    fig.tight_layout()
    for p in paths:fig.savefig(p,dpi=160,bbox_inches="tight")
    plt.close(fig)
    write_json("out/phase19b_energy_zoom.json",{
        "source_sha256":digest(__file__),"report_sha256":digest("out/phase19b_richlines.json"),
        "no_statistical_or_fit_changes":True,"scale":"percent, vertical limits per n from largest95percentCI",
        "artifacts":[{"path":p.as_posix(),"sha256":digest(p)} for p in paths]})


if __name__=="__main__":main()
