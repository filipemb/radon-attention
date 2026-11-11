"""Independent numerical references for the E2 solvers and metric."""
import numpy as np
from scipy import sparse
from scipy.optimize import lsq_linear,nnls
from richlines_core import LineDictionary,NNLSActive,_radon_active_solve,svd_errors


def validate():
    rng=np.random.default_rng(19027)
    M=rng.normal(size=(80,24));b=rng.normal(size=80)
    G=M.T@M;h=M.T@b;x=np.empty(0);state=NNLSActive();differences=[]
    for k in range(1,25):
        x,_=state.refit(G[:k,:k],h[:k],np.r_[x,0.0])
        reference=nnls(M[:,:k],b)[0]
        differences.append(float(np.max(np.abs(x-reference))))
    if max(differences)>1e-8:
        raise AssertionError("Warm-start NNLS differs from independent SciPy NNLS")
    d=LineDictionary(8,angles=24)
    R=sparse.diags(np.sqrt(np.diff(d.D.indptr)))@d.D
    R=R.tocsr()
    truth=rng.uniform(0,1,R.shape[1]);s=R@truth
    order=np.argsort(-s);compressed=np.zeros_like(s);compressed[order[:7]]=s[order[:7]]
    ours,diag=_radon_active_solve(R,compressed)
    reference=lsq_linear(R,compressed,bounds=(0,np.inf),tol=1e-11,
        lsq_solver="lsmr",lsmr_tol=1e-13,lsmr_maxiter=1000,max_iter=300)
    objective_ours=float(np.linalg.norm(R@ours-compressed)**2)
    objective_ref=float(np.linalg.norm(R@reference.x-compressed)**2)
    if not diag["converged"] or not reference.success or abs(objective_ours-objective_ref)>1e-6:
        raise AssertionError(f"Constrained Radon reference mismatch: {objective_ours}, {objective_ref}, {diag}")
    A=np.tril(rng.random((12,12)))
    U,s,V=np.linalg.svd(A,full_matrices=False)
    reference_error=float(np.linalg.norm(A-(U[:,:3]*s[:3])@V[:3]))
    error=svd_errors(A,[3])[3]
    if abs(error["absolute"]-reference_error)>1e-10:
        raise AssertionError("SVD tail metric differs from explicit whole-matrix reconstruction")
    return {"incremental_nnls_max_coefficient_difference":max(differences),
            "radon_nnls_objective":objective_ours,"scipy_lsq_linear_objective":objective_ref,
            "radon_projected_kkt":diag["relative_projected_kkt"],
            "whole_matrix_svd_absolute_difference":abs(error["absolute"]-reference_error),"passed":True}
