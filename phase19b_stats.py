"""Widths, axial angles, signed decay and additive overlap-aware energy."""
import phase19b_common
import numpy as np
from scipy.optimize import brentq
from phase19b_render import forward
FWHM_FACTOR=2*brentq(lambda q:-q*q/2+3*np.log(1-q*q/36)+np.log(2),0,5.99)


def describe(values):
    a=np.asarray(values,dtype=float)
    if not np.isfinite(a).all():raise ValueError("Nonfinite parameter statistic")
    if not a.size:return None
    q=np.quantile(a,[.25,.5,.75])
    return {"n":int(a.size),"q25":float(q[0]),"median":float(q[1]),"q75":float(q[2]),
            "mean":float(a.mean()),"min":float(a.min()),"max":float(a.max())}


def parameter_distribution(p,n,norm):
    p=np.asarray(p,dtype=float)
    if p.ndim!=2 or p.shape[1]!=5 or not np.isfinite(p).all() or (p[:,2]<=0).any() or (p[:,4]<0).any():
        raise ValueError("Invalid five-parameter representation")
    active=p[:,4]>1e-8*norm
    output={"n_atoms":len(p),"n_active_atoms":int(active.sum()),"active_definition":"amplitude > 1e-8*||A||_F"}
    for label,mask in (("all_atoms",np.ones(len(p),dtype=bool)),("active_atoms",active)):
        v=p[mask];theta=np.remainder(v[:,0],np.pi)
        parity=np.remainder(np.floor(v[:,0]/np.pi).astype(np.int64),2)
        decay=v[:,3]*np.where(parity==1,-1,1)
        record={"width_pixels":describe(v[:,2]),"transverse_fwhm_pixels":describe(FWHM_FACTOR*v[:,2]),"decay_signed_canonical":describe(decay),
                "absolute_decay":describe(np.abs(decay)),"normal_angle_degrees_mod_180":describe(np.rad2deg(theta)),
                "width_fraction_greater_than":{str(t):float(np.mean(v[:,2]>t)) if len(v) else None for t in (2.,8.,n/8)},
                "angle_histogram_edges_degrees":list(range(0,181,15)),
                "angle_histogram_counts":np.histogram(np.rad2deg(theta),bins=np.arange(0,181,15))[0].tolist()}
        if len(v):
            z=np.mean(np.exp(2j*theta));anchor=(.5*np.angle(z))%np.pi
            unwrapped=anchor+(theta-anchor+np.pi/2)%np.pi-np.pi/2
            record["axial_angle_unwrapped_degrees"]=describe(np.rad2deg(unwrapped))
            record["axial_anchor_degrees"]=float(np.rad2deg(anchor));record["axial_resultant_length"]=float(abs(z))
        output[label]=record
    return output


def decoded_statistics(parameters,n,b):
    p=np.asarray(parameters,dtype=float);b=np.asarray(b,dtype=float);norm=float(np.linalg.norm(b))
    if not norm>0 or not np.isfinite(b).all():raise ValueError("Invalid attention target")
    params=[np.ascontiguousarray(np.repeat(p[None,:,j],4,axis=0)) for j in (0,1,2,3,4)]
    params[2]=np.log(params[2]);thresholds=(2.,8.,n/8)
    for row,threshold in enumerate(thresholds,1):params[4][row]*=p[:,2]>threshold
    images,_=forward(*params,n);hat=images[0]
    if not np.isfinite(images).all():raise FloatingPointError("Nonfinite decoded image")
    energy=float(hat@hat);residual=float(np.linalg.norm(hat-b))
    result={"relative":residual/norm,"absolute":residual,"norm_frobenius":norm,
        "parameters":p.tolist(),"parameter_distribution":parameter_distribution(p,n,norm),
        "reconstruction_energy":energy,"wide_energy":{}}
    for index,threshold in enumerate(thresholds,1):
        wide=images[index];thin=hat-wide;own=float(wide@wide);cross=float(wide@thin)
        share=float(wide@hat)/energy if energy>0 else None
        if share is not None and not -1e-10<=share<=1+1e-10:raise AssertionError("Invalid additive energy share")
        result["wide_energy"][str(threshold)]={"additive_share":share,
            "self_energy_share":own/energy if energy>0 else None,
            "deletion_share":(own+2*cross)/energy if energy>0 else None,
            "wide_self_energy":own,"wide_thin_inner_product":cross,
            "definition":"<sum_wide a*u, Ahat>/||Ahat||^2; splits every pair cross term equally and adds to one over complementary groups"}
    result["zero_reconstruction"]=energy==0
    return result
