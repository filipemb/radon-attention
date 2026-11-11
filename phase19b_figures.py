"""Standalone descriptive figures from the completed, audited E2b experiment.

All error points use the same predeclared192cases. Parameter CDFs pool active
atoms (equal atom weights); energy/error intervals resample whole documents.
These plots neither select cases nor alter any fit or statistical comparison.
"""
import phase19b_common
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from phase19b_common import read_json,cache_path,RANKS,budgets,write_json,digest

COLORS={"svd":"#2864a0","free":"#228052","thin":"#d17a18"}
LABELS={"svd":"SVD","free":"livre","thin":"fina"}


def save(fig,stem):
    paths=[]
    for suffix in ("svg","png"):
        p=Path("out")/(stem+"."+suffix)
        if p.exists():raise FileExistsError(p)
        fig.savefig(p,dpi=160,bbox_inches="tight")
        paths.append({"path":p.as_posix(),"sha256":digest(p)})
    plt.close(fig)
    return paths


def cdf(ax,values,**kwargs):
    values=np.sort(np.asarray(values,dtype=float))
    if not len(values) or not np.isfinite(values).all():raise ValueError("Undefined CDF")
    ax.step(values,np.arange(1,len(values)+1)/len(values),where="post",**kwargs)


def main():
    report=read_json("out/phase19b_richlines.json")
    audit=read_json("out/phase19b_integrity_audit.json")
    if not audit["passed"] or digest("out/phase19b_richlines.json")!=audit["report_sha256"]:
        raise AssertionError("Figures require the completed audited report")
    stems=("phase19b_errors","phase19b_parameters","phase19b_broad_energy")
    for stem in stems:
        for ext in ("svg","png"):
            p=Path("out")/(stem+"."+ext)
            if p.exists():raise FileExistsError(p)
    if Path("out/phase19b_figures.json").exists():raise FileExistsError("out/phase19b_figures.json")
    plt.rcParams.update({"font.size":9,"axes.spines.top":False,"axes.spines.right":False})
    models=list(dict.fromkeys(d["model"] for d in report["comparisons_192"]))
    fig,axes=plt.subplots(6,2,figsize=(11,17),sharex=True,squeeze=False)
    for d in report["comparisons_192"]:
        ax=axes[models.index(d["model"]),int(d["n"]==256)]
        for arm in ("svd","free","thin"):
            summaries=[d["budget"][str(B)]["methods"][arm]["relative"] for B in budgets(d["n"])]
            y=[s["median"] for s in summaries];low=[s["median_ci95_document_block"][0] for s in summaries]
            high=[s["median_ci95_document_block"][1] for s in summaries]
            ax.plot(RANKS,y,"o-",color=COLORS[arm],label=LABELS[arm],markersize=3)
            ax.fill_between(RANKS,low,high,color=COLORS[arm],alpha=.12)
        ax.set_title(f"{d['model']} | n={d['n']} | 16 documentos")
        ax.set_xscale("log",base=2);ax.set_xticks(RANKS,labels=[str(r) for r in RANKS]);ax.set_ylim(bottom=0)
        ax.grid(alpha=.2)
        if d["n"]==128:ax.set_ylabel("Erro relativo de Frobenius")
    for ax in axes[-1]:ax.set_xlabel("Posto SVD equivalente: B = r(2n+1)")
    axes[0,0].legend(ncol=3)
    fig.suptitle("Mesmos documentos e orçamentos | mediana e IC95% em blocos por documento",y=1.005)
    fig.tight_layout();artifacts=save(fig,stems[0])
    pooled={n:{str(B):[] for B in budgets(n)} for n in (128,256)}
    selection=report["selection"]
    for d in selection["datasets"]:
        for inst in d["instances"]:
            row=read_json(cache_path("free",d["model_slug"],d["n"],inst["archive_index"]))
            for B,v in row["budget"].items():
                p=np.asarray(v["parameters"]);active=p[:,4]>1e-8*v["norm_frobenius"]
                pooled[d["n"]][B].append(p[active])
    fig,axes=plt.subplots(2,3,figsize=(14,7),squeeze=False)
    palette=plt.get_cmap("viridis")(np.linspace(.08,.9,5))
    for row,n in enumerate((128,256)):
        for B,color in zip(budgets(n),palette):
            p=np.concatenate(pooled[n][str(B)])
            label=f"B={B}; k={B//5}"
            cdf(axes[row,0],p[:,2],color=color,label=label)
            cdf(axes[row,1],np.abs(p[:,3]),color=color,label=label)
            hist,_=np.histogram(np.degrees(p[:,0]%np.pi),bins=np.arange(0,181,15))
            axes[row,2].step(np.arange(7.5,180,15),hist/hist.sum(),where="mid",color=color,label=label)
        axes[row,0].set_xscale("log");axes[row,0].set_xlim(.19,n)
        for threshold in (2,8,n/8):axes[row,0].axvline(threshold,ls=":",lw=.8,color="gray")
        axes[row,0].set_xlabel("Largura transversal sigma (pixels)")
        axes[row,1].set_xlabel("Decaimento absoluto |beta|");axes[row,1].set_xlim(0,32)
        axes[row,2].set_xlabel("Ângulo da normal, módulo 180 graus");axes[row,2].set_xlim(0,180)
        for col in range(2):axes[row,col].set_ylabel(f"n={n}: fração acumulada");axes[row,col].set_ylim(0,1)
        axes[row,2].set_ylabel(f"n={n}: fração por intervalo de15 graus")
        for ax in axes[row]:ax.grid(alpha=.2)
        axes[row,0].legend(fontsize=7)
    fig.suptitle("Braço livre: átomos ativos das 96 instâncias por n, com peso igual por átomo\nSigma é o parâmetro do perfil: FWHM = 2.1775 sigma; decaimento = exp(-beta × distância longitudinal/n)")
    fig.tight_layout();artifacts.extend(save(fig,stems[1]))
    fig,axes=plt.subplots(1,2,figsize=(10,4),squeeze=False)
    for ax,n in zip(axes[0],(128,256)):
        summaries=report["extension_parameter_diagnostics_by_n"][str(n)]["free"]["by_budget"]
        for threshold,color in zip((2.,8.,n/8),("#2864a0","#d17a18","#7c3fa3")):
            values=[summaries[str(B)]["wide_energy_share"][str(threshold)]["additive_share"] for B in budgets(n)]
            ax.plot(RANKS,[s["median"] for s in values],"o-",color=color,label=f"sigma>{threshold:g}px")
            ax.fill_between(RANKS,[s["median_ci95_document_block"][0] for s in values],
                [s["median_ci95_document_block"][1] for s in values],color=color,alpha=.12)
        ax.set_xscale("log",base=2);ax.set_xticks(RANKS,labels=[str(r) for r in RANKS]);ax.set_ylim(0,1)
        ax.set_title(f"Livre | n={n} | 96 instâncias")
        ax.set_xlabel("Posto SVD equivalente: B = r(2n+1)");ax.set_ylabel("Parcela da energia reconstruída")
        ax.legend();ax.grid(alpha=.2)
    fig.suptitle("<Reconstrução larga, reconstrução total> / ||Reconstrução total||²\nMediana e IC95% com blocos por documento; fina tem parcela larga zero")
    fig.tight_layout();artifacts.extend(save(fig,stems[2]))
    write_json("out/phase19b_figures.json",{"report_sha256":digest("out/phase19b_richlines.json"),
        "source_sha256":digest(__file__),"artifacts":artifacts,"selection_or_fit_changes":False})
    print("Created six standalone figure files",flush=True)


if __name__=="__main__":main()
