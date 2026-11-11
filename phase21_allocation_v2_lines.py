"""Versioned line-arm implementation and exact-endpoint controls.

The imported omp_profiled is never edited or monkey-patched. At a complete
dictionary endpoint, its final NNLS projects onto every candidate; the unique
matrix projection and reconstruction error are independent of selection order.
Full-dictionary errors can be published after the terminal equivalence and
population/KKT controls pass. Partial OMP trajectories remain the unmodified
imported function; no scope waiver or user response is inferred.
"""
import phase21_allocation_v2 as e4
import ast
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import time
import numpy as np
from scipy.linalg import qr
from scipy.optimize import nnls
from sampling import MODELS, load_sample, sha256_file, sample_paths, slug
from phase06_profiled_lines import TAUS, atom_vector, omp_profiled, precompute_band_norms

DECISIONS = Path("out/phase21_allocation_v2_decisions.json")
_DICTIONARIES = {}


class FullLineEndpoint:
    def __init__(self,n):
        start = time.perf_counter()
        self.n = n
        self.labels = [("vert",c) for c in range(n)] + [("band",tau) for tau in TAUS] + [("diag",d) for d in range(n)]
        self.D = np.stack([atom_vector(kind,param,n) for kind,param in self.labels],axis=1)
        self.Q,self.R = qr(self.D,mode="economic",check_finite=True)
        self.setup_seconds = time.perf_counter()-start

    def project(self,A):
        b = A.ravel()
        norm = float(np.linalg.norm(b))
        if not np.isfinite(b).all() or norm<=0:
            raise ValueError("Invalid line-arm input; no replacement")
        coef,_ = nnls(self.R,self.Q.T@b,maxiter=100*len(self.labels))
        S = self.D@coef
        gradient = self.D.T@(S-b)
        dual = max(0.,float(-gradient.min()))/norm
        comp = float(np.max(np.abs(coef*gradient)))/(norm*norm)
        kkt = max(dual,comp,max(0.,float(-coef.min()))/norm)
        if not np.isfinite(coef).all() or not np.isfinite(kkt) or kkt>1e-8:
            raise ArithmeticError(f"Full-line endpoint KKT failure {kkt}")
        return {"error":float(np.linalg.norm(S-b)/(norm+1e-12)),
                "coefficients":coef.tolist(),"n_selected_atoms":len(self.labels),
                "n_positive_coefficients":int(np.count_nonzero(coef>0)),"nnls_kkt_relative_violation":kkt}


def dictionary(n):
    if n not in _DICTIONARIES:
        _DICTIONARIES[n] = FullLineEndpoint(n)
    return _DICTIONARIES[n]


def literal_benchmark_error(n):
    path = Path("out/phase21_allocation_v2_omp_benchmark.json")
    if path.exists():
        value = json.loads(path.read_text(encoding="utf-8"))
        rows = [r for r in value["records"] if r["n"] == n]
        if len(rows) != 1:
            raise ValueError("Benchmark controls incomplete")
        row = rows[0]
        return float(row["errors"][str(2*n+7)]),row["seconds"],sha256_file(path)
    # The long n256 pilot need not delay the completed n128 control record.
    logpath = Path("out/_rerun_logs/phase21_allocation_v2_omp_benchmark.log")
    marker = f"UNMODIFIED OMP DONE n={n}: "
    lines = [s for s in logpath.read_text(encoding="utf-8").splitlines() if s.startswith(marker)]
    if len(lines) != 1:
        raise RuntimeError(f"FALTA: completed literal OMP benchmark n={n}; control still running")
    prefix,error_text = lines[0].split(" errors=",1)
    errors = ast.literal_eval(error_text)
    seconds = float(prefix.split(": ")[-1].removesuffix("s"))
    return float(errors[2*n+7]),seconds,sha256_file(logpath)


def check(n):
    target = Path("out")/f"phase21_allocation_v2_line_endpoint_check_n{n}.json"
    if target.exists():
        return json.loads(target.read_text(encoding="utf-8"))
    attention,_ = load_sample("gpt2",n)
    endpoint = dictionary(n)
    benchmark_path=Path("out/phase21_allocation_v2_omp_benchmark.json")
    benchmark_log=Path("out/_rerun_logs/phase21_allocation_v2_omp_benchmark.log")
    literal_complete=(benchmark_path.exists() or any(s.startswith(f"UNMODIFIED OMP DONE n={n}: ")
                      for s in benchmark_log.read_text(encoding="utf-8").splitlines()))
    if literal_complete:
        reference,reference_seconds,reference_hash = literal_benchmark_error(n)
        reference_type="complete unmodified omp_profiled execution"
    else:
        # The long literal pilot continues independently. Verify its exact final
        # NNLS subproblem directly, with the same dense kernel and default limit.
        dense_start=time.perf_counter()
        b=attention[0].astype(np.float64).ravel()
        dense_coef,_=nnls(endpoint.D,b)
        reference=float(np.linalg.norm(endpoint.D@dense_coef-b)/(np.linalg.norm(b)+1e-12))
        reference_seconds=time.perf_counter()-dense_start
        reference_hash=sha256_file("phase06_profiled_lines.py")
        reference_type="dense NNLS final subproblem of full-dictionary OMP; same kernel/default limit; literal sequence still running"
    start = time.perf_counter()
    actual = endpoint.project(attention[0].astype(np.float64))
    seconds = time.perf_counter()-start
    difference = abs(actual["error"]-reference)
    if difference>1e-11:
        raise ArithmeticError(f"Endpoint differs from complete imported OMP: {difference}")
    result = {"n":n,"model":"gpt2","fixed_instance_index":0,"passed":True,
              "reference_type":reference_type,"reference_error":reference,
              "unmodified_full_OMP_error":reference if literal_complete else None,"direct_endpoint_error":actual["error"],
              "absolute_difference":difference,"predeclared_tolerance":1e-11,
              "reference_seconds":reference_seconds,"literal_OMP_seconds":reference_seconds if literal_complete else None,
              "endpoint_setup_seconds":endpoint.setup_seconds,
              "endpoint_projection_seconds":seconds,"n_atoms":2*n+7,
              "KKT":actual["nnls_kkt_relative_violation"],"benchmark_sha256":reference_hash,
              "source_OMP_sha256":sha256_file("phase06_profiled_lines.py"),
              "normalization":"Inherited unmodified OMP denominator ||A||+1e-12, applied identically to its exact endpoint",
              "equivalence":"After all 2n+7 candidates have been selected, imported OMP solves NNLS on a permutation of the same full dictionary. A finitely generated cone has a unique matrix projection; coefficient nonuniqueness does not change the error.",
              "production_substitution_authorized":False}
    e4.write_new(target,result)
    e4.log(f"LINE ENDPOINT CONTROL n={n}: reference={reference:.16g}, direct={actual['error']:.16g}, diff={difference:.3g}; reference={reference_seconds:.1f}s, direct={seconds:.3f}s; {reference_type}")
    return result


def paths(model,n):
    return (Path("out")/f"phase21_allocation_v2_{slug(model)}_n{n}.json",
            Path("out/pairs")/f"phase21_allocation_{slug(model)}_n{n}_v2.jsonl")


def reconcile_completed_literal_controls():
    """Add a new immutable record after both original OMP pilots complete."""
    target=Path("out/phase21_allocation_v2_complete_OMP_endpoint_controls.json")
    if target.exists():return json.loads(target.read_text(encoding="utf-8"))
    controls=[]
    for n in (128,256):
        prior_path=Path("out")/f"phase21_allocation_v2_line_endpoint_check_n{n}.json"
        prior=json.loads(prior_path.read_text(encoding="utf-8"))
        reference,seconds,benchmark_hash=literal_benchmark_error(n)
        actual=prior["direct_endpoint_error"]
        difference=abs(reference-actual)
        if difference>1e-11:raise ArithmeticError("Complete original OMP pilot and endpoint disagree")
        controls.append({"n":n,"model":"gpt2","fixed_instance_index":0,
                         "reference":"complete unmodified omp_profiled execution",
                         "unmodified_OMP_error":reference,"endpoint_error":actual,
                         "absolute_difference":difference,"tolerance":1e-11,
                         "literal_OMP_seconds":seconds,"benchmark_sha256":benchmark_hash,
                         "prior_endpoint_control_path":prior_path.as_posix(),
                         "prior_endpoint_control_sha256":sha256_file(prior_path)})
    result={"schema_version":2,"passed":True,"controls":controls,
            "scope":"Two fixed pilot instances. General endpoint equivalence follows from the identical full finite cone, not from two empirical controls.",
            "source_OMP_sha256":sha256_file("phase06_profiled_lines.py"),
            "partial_OMP_equivalence_claimed":False}
    e4.write_new(target,result)
    e4.log("COMPLETE OMP CONTROLS n128 and n256: both exact endpoint error differences zero; original source unchanged")
    return result


def promote_review(job):
    """Publish verified equivalent endpoints without repeating fits."""
    if not DECISIONS.exists():raise RuntimeError("Record the computational decision and equivalence evidence first")
    choice=json.loads(DECISIONS.read_text(encoding="utf-8"))
    if not choice["accept_exact_full_dictionary_endpoint"] or choice["capacity_budget_ranks_K"]!=[4,8,16]:
        raise ValueError("Endpoint publication only supports the complete finite-dictionary budgets")
    proof=json.loads(Path('out/phase21_allocation_v2_complete_OMP_endpoint_controls.json').read_text(encoding='utf-8'))
    integrity=json.loads(Path('out/phase21_allocation_v2_integrity_checks.json').read_text(encoding='utf-8'))
    if (not proof['passed'] or not integrity['passed'] or integrity['n_instances']!=19968
            or integrity['maximum_discrepancies']['full_lines_KKT']>1e-8
            or proof['source_OMP_sha256']!=sha256_file('phase06_profiled_lines.py')):
        raise ValueError('Full dictionary endpoint equivalence/population/source controls incomplete')
    model,n=job
    source=Path("out")/f"phase21_allocation_v2_endpoint_preview_{slug(model)}_n{n}.json"
    candidate=json.loads(source.read_text(encoding="utf-8"))
    source_pairs=Path(candidate["pairs_path"])
    if sha256_file(source_pairs)!=candidate["pairs_sha256"]:raise ValueError("Candidate pairs changed")
    target,pairs=paths(model,n)
    if target.exists():
        existing=json.loads(target.read_text(encoding="utf-8"))
        if sha256_file(pairs)!=existing["pairs_sha256"]:raise ValueError("Final pairs changed")
        return str(target)
    count=0
    with source_pairs.open(encoding="utf-8") as inp,pairs.open("x",encoding="utf-8") as out:
        for line in inp:
            row=json.loads(line)
            if row["line_result_status"]!="candidate_exact_endpoint_not_final_protocol":raise ValueError("Unexpected candidate state")
            row["line_result_status"]="verified_exact_full_dictionary_OMP_terminal_error"
            out.write(json.dumps(row,ensure_ascii=False,allow_nan=False,separators=(",",":"))+"\n")
            count+=1
    if count!=candidate["n_instances"]:raise ValueError("Incomplete promoted population")
    candidate.update(status="complete_full_dictionary_budget_panel",pairs_path=pairs.as_posix(),pairs_sha256=sha256_file(pairs),
                     promoted_from_path=source.as_posix(),promoted_from_sha256=sha256_file(source))
    candidate["line_arm"].update(candidate_only=False,decision_path=DECISIONS.as_posix(),
                                  completed_literal_controls_path="out/phase21_allocation_v2_complete_OMP_endpoint_controls.json",
                                  full_OMP_trajectory_executed_on_every_instance=False,
                                  computational_decision_source=choice['decision_source'],
                                  historical_control_authorization_field_is_control_time_only=True)
    e4.write_new(target,candidate)
    e4.log(f"VERIFIED ENDPOINTS PUBLISHED {model} n={n}; all {count} instances; unmodified full OMP terminal problem, exact direct NNLS; no user approval inferred")
    return str(target)


def run(job,preview=False):
    model,n = job
    if not preview and not DECISIONS.exists():
        raise RuntimeError("Pending user clarification: no production endpoint substitution before explicit choice")
    choice = ({"accept_exact_full_dictionary_endpoint":True,"capacity_budget_ranks_K":[4,8,16]}
              if preview else json.loads(DECISIONS.read_text(encoding="utf-8")))
    use_endpoint = choice["accept_exact_full_dictionary_endpoint"]
    budgets = tuple(choice["capacity_budget_ranks_K"])
    if any(K not in e4.BUDGET_RANKS for K in budgets):
        raise ValueError("Undeclared budget")
    target,pairpath = (paths(model,n) if not preview else (
        Path("out")/f"phase21_allocation_v2_endpoint_preview_{slug(model)}_n{n}.json",
        Path("out/pairs")/f"phase21_allocation_endpoint_preview_{slug(model)}_n{n}_v2.jsonl"))
    corepath,corepairs = e4.core_paths(model,n)
    core = json.loads(corepath.read_text(encoding="utf-8"))
    if core["pairs_sha256"] != sha256_file(corepairs):
        raise ValueError("Core pairs changed")
    if target.exists():
        result = json.loads(target.read_text(encoding="utf-8"))
        if result["pairs_sha256"] != sha256_file(pairpath):
            raise ValueError("Existing final v2 pairs mismatch")
        return str(target)
    check_record = check(n) if use_endpoint else None
    attention,manifest = load_sample(model,n)
    if sha256_file(sample_paths(model,n)[0]) != manifest["npz_sha256"]:
        raise ValueError("Input archive changed")
    endpoint = dictionary(n) if use_endpoint else None
    norms = precompute_band_norms(n)
    n_full = 2*n+7
    steps = {K:min(K*(2*n+1)//2,n_full) for K in budgets}
    partial_steps = {k for k in steps.values() if k<n_full or not use_endpoint}
    rows=[]
    if pairpath.exists():
        with pairpath.open(encoding="utf-8") as inp:
            rows=[json.loads(line) for line in inp]
    started=time.perf_counter()
    e4.log(f"LINES START {model} n={n}: budgets={budgets}, endpoint={use_endpoint}, partial_steps={sorted(partial_steps)}; all {len(attention)} instances")
    pairpath.parent.mkdir(parents=True,exist_ok=True)
    with corepairs.open(encoding="utf-8") as inp,pairpath.open("a",encoding="utf-8") as out:
        for i,line in enumerate(inp):
            if i<len(rows):
                continue
            row=json.loads(line)
            row["line_result_status"]="candidate_exact_endpoint_not_final_protocol" if preview else "final_protocol"
            row["allocation_comparisons"]={key.replace("alternating","algorithm_1_5_iterations"):value
                                            for key,value in row["allocation_comparisons"].items()}
            if row["instance_id"]!=manifest["instances"][i]["instance_id"]:
                raise ValueError("Core line-arm ordering mismatch")
            A=attention[i].astype(np.float64)
            if abs(float(np.linalg.norm(A))-row["attention_frobenius_norm"])>1e-12:
                raise ArithmeticError("Line arm and audited decompositions do not use identical matrices")
            full_result=endpoint.project(A) if use_endpoint and n_full in steps.values() else None
            partial_errors,partial_support=({},[])
            if partial_steps:
                partial_errors,partial_support=omp_profiled(A,max(partial_steps),n,partial_steps,norms)
            row["lines"]={"complete_dictionary_endpoint":full_result,
                           "partial_imported_OMP_support_at_largest_k":partial_support}
            original_capacity=row["capacity"]
            row["capacity"]={}
            for K in budgets:
                k=steps[K]
                item=dict(original_capacity[str(K)])
                item["line_error"] = full_result["error"] if use_endpoint and k==n_full else partial_errors[k]
                item["line_selected_atoms"]=k
                item["line_parameters"]=2*k
                item["line_unused_parameters"]=item["common_cap"]-2*k
                item["line_dictionary_exhausted"]=k==n_full
                item["paired_error_lines_minus_svd"]=item["line_error"]-item["svd_error"]
                item["paired_error_named_minus_lines"]=item["named_first_error"]-item["line_error"]
                row["capacity"][str(K)]=item
            out.write(json.dumps(row,allow_nan=False,ensure_ascii=False,separators=(",",":"))+"\n")
            rows.append(row)
            if (i+1)%64==0:
                out.flush();e4.log(f"LINES {model} n={n}: {i+1}/{len(attention)} seconds={time.perf_counter()-started:.1f}")
    if len(rows)!=manifest["n_matrices"]:
        raise ValueError("Incomplete line-arm population")
    docs=[r["document_index"] for r in rows]
    capacity={}
    for K in budgets:
        observations=[r["capacity"][str(K)] for r in rows]
        keys=("named_first_error","svd_error","line_error","named_first_parameters","named_first_unused_parameters",
              "line_parameters","line_unused_parameters","line_selected_atoms","named_channel_only_error","named_channel_parameters")
        capacity[str(K)]={"common_cap":K*(2*n+1),"budget_rank_K":K,"residual_rank":K-1,
                         "metrics":{key:e4.summarize([v[key] for v in observations],docs) for key in keys},
                         "comparisons":{
                             "named_minus_SVD":core["capacity_without_lines"][str(K)]["named_minus_svd"],
                             "lines_minus_SVD":e4.paired([v["paired_error_lines_minus_svd"] for v in observations],rows),
                             "named_minus_lines":e4.paired([v["paired_error_named_minus_lines"] for v in observations],rows)}}
    result={"schema_version":2,"model":model,"n":n,"n_instances":len(rows),"n_documents":len(set(docs)),
            "status":"candidate_exact_endpoint_waiting_user_choice" if preview else "complete",
            "source_core_path":str(corepath),"source_core_sha256":sha256_file(corepath),
            "source_manifest_sha256":core["manifest_sha256"],"dictionary":core["dictionary"],
            "allocation":core["allocation"],"capacity":capacity,
            "line_arm":{"imported_function":"phase06_profiled_lines.omp_profiled, unmodified",
                        "source_sha256":sha256_file("phase06_profiled_lines.py"),"finite_candidate_count":n_full,
                        "endpoint_equivalence_used":use_endpoint,"control":check_record,
                        "actual_computation":"Direct final NNLS projection when complete dictionary fits; literal unmodified OMP for partial dictionaries",
                        "max_k_by_budget":steps,"coefficient_count_in_budget":"2 per selected atom, including NNLS zeros, matching OMP budget convention; positive coefficients also retained",
                        "decision_path":None if preview else DECISIONS.as_posix(),
                        "candidate_only":preview},
            "pairs_path":pairpath.as_posix(),"pairs_sha256":sha256_file(pairpath),
            "elapsed_seconds":time.perf_counter()-started}
    e4.write_new(target,result)
    e4.log(f"LINES DONE {model} n={n}; all {len(rows)} matched instances; seconds={result['elapsed_seconds']:.1f}")
    return str(target)


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("check","run","preview","reconcile-controls","promote"))
    parser.add_argument("--length",type=int,choices=(128,256),default=128)
    parser.add_argument("--workers",type=int,choices=(1,2,3),default=1)
    args=parser.parse_args()
    if args.command=="reconcile-controls":
        reconcile_completed_literal_controls()
    elif args.command=="check":
        check(args.length)
    else:
        jobs=[(m,n) for n in (128,256) for m in MODELS]
        if args.workers==1:
            for job in jobs:
                if args.command=="promote":promote_review(job)
                else:run(job,preview=args.command=="preview")
        else:
            from functools import partial
            with ProcessPoolExecutor(max_workers=args.workers) as pool:
                action=promote_review if args.command=="promote" else partial(run,preview=args.command=="preview")
                for path in pool.map(action,jobs):print(f"SAVED {path}",flush=True)
