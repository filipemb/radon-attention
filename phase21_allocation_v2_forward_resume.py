"""Resume the authorized E4 forward arm after the completed V1 became available.

CPU preflight/summaries are separate from one GPU process per model. Reuse the
unchanged E4 estimator/evaluator and import V1 causal reconstruction throughout.
This continuation evaluates the V1 prefix length (128) on its 256 articles.
Never update the historical matrix aggregate or the old three-hour deadline.
"""
import phase21_allocation_v2 as e4  # datasets before torch; four CPU threads.
import phase21_allocation_v2_forward as forward
import phase2_downstream as harness
from phase24_p0_metrics import describe
from sampling import MODELS,CORPUS_PATH,sha256_file,slug,write_json_new
from datetime import datetime,timezone
from pathlib import Path
from scipy.stats import rankdata,wilcoxon
import argparse
import gc
import json
import numpy as np
import torch

RUN=Path('out/phase21_allocation_v2_forward_run.json')
BASE=Path('out/phase2_downstream_v2.json')
MATRIX=Path('out/phase21_allocation_v2.json')
REFERENCES=Path('out/phase21_allocation_v2_forward_V1_references.json')
OUTPUT=Path('out/phase21_allocation_v2_forward.json')
e4.LOG=Path('out/_rerun_logs/phase21_allocation_v2_forward_progress.md')
RANKS=(8,16)
REFS=('uniform','diagonal','sink')
ARMS=('phase2:identity','phase2:svd:8','phase2:svd:16',*(f'phase2:{m}' for m in REFS))


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def stats(values,articles):
    # Preserve the project-wide imported estimator, including its exact draws.
    return e4.summarize(values,articles)


def paired_articles(differences):
    delta=np.asarray(differences,dtype=np.float64)
    if delta.shape!=(256,) or not np.isfinite(delta).all():
        raise ValueError('Exactly 256 finite paired article differences required')
    nonzero=delta[delta!=0]
    if len(nonzero)==0:
        plus=minus=statistic=effect=0.;pvalue=1.
        method='All article differences exactly zero: explicit degenerate null'
    else:
        ranks=rankdata(np.abs(nonzero),method='average')
        plus=float(ranks[nonzero>0].sum());minus=float(ranks[nonzero<0].sum())
        effect=(plus-minus)/(plus+minus)
        test=wilcoxon(delta,zero_method='wilcox',alternative='two-sided',method='asymptotic')
        statistic=float(test.statistic);pvalue=float(test.pvalue)
        method='scipy.stats.wilcoxon; two-sided; zero_method=wilcox; method=asymptotic; p unadjusted'
    if not np.isfinite([plus,minus,statistic,effect,pvalue]).all():
        raise ArithmeticError('Nonfinite signed-rank inference; no replacement')
    return {'n_articles':256,'n_zero_differences':int(np.count_nonzero(delta==0)),
            'statistic':statistic,'p_two_sided':pvalue,'W_positive':plus,'W_negative':minus,
            'rank_biserial':effect,'positive_difference_favors':'SVD',
            'method':method,'fraction_articles_SVD_has_lower_KL':float(np.mean(delta>0))}


def batch_statistics(records):
    result={};seen={}
    for row in records:
        key=(row['evaluation_batch_start'],row['evaluation_batch_size'])
        values=row['attention_validation_batch']
        if key in seen:
            if seen[key]!=values:raise ValueError('V1 batch counters disagree between articles')
            continue
        seen[key]=values
        for field,value in values.items():
            if isinstance(value,bool):result[field]=result.get(field,True) and value
            elif field.startswith('max_'):result[field]=max(result.get(field,0),value)
            else:result[field]=result.get(field,0)+value
    return result


def source_records(model,baseline,corpus):
    source=baseline[model];n=source['prefix_length'];ch=sha256_file(CORPUS_PATH)
    groups={a:{} for a in ARMS}
    with Path(source['pairs_path']).open(encoding='utf-8') as inp:
        for line in inp:
            row=json.loads(line)
            if row['arm'] not in groups:continue
            i=row['document_index']
            if not isinstance(i,int) or not 0<=i<256:raise ValueError('Invalid V1 article index')
            expected=corpus['documents'][i]['doc_id']
            window=corpus['models'][model]['documents'][i]
            if (row['model']!=model or row['corpus_manifest_sha256']!=ch or row['prefix_length']!=n
                    or row['empty_row_policy']!='uniform' or row['doc_id']!=expected
                    or row['offset']!=window['offset'] or row['target_id']!=window['token_ids'][n]):
                raise ValueError('V1 source/corpus/offset/last-token target mismatch')
            if row.get('svd_driver') is not None:raise ValueError('V1 changed the fixed exact SVD driver')
            if not np.isfinite([row['kl'],row['nll'],row['reference_nll']]).all():
                raise ValueError('Nonfinite V1 observation; no replacement')
            if i in groups[row['arm']]:raise ValueError('Duplicate V1 arm/article')
            groups[row['arm']][i]=row
    for arm,by_article in groups.items():
        if set(by_article)!=set(range(256)):raise ValueError(f'Incomplete V1 {model}: {arm}')
    ordered={a:[v[i] for i in range(256)] for a,v in groups.items()}
    for i in range(256):
        native=ordered['phase2:identity'][i]
        if native['kl']!=0 or native['nll']!=native['reference_nll']:
            raise ValueError('V1 identity is not exactly native')
        for arm in ARMS:
            row=ordered[arm][i]
            if (row['reference_nll']!=native['reference_nll']
                    or row['evaluation_batch_start']!=native['evaluation_batch_start']
                    or row['evaluation_batch_size']!=native['evaluation_batch_size']):
                raise ValueError('V1 arms do not share a native reference and batch')
    return ordered


def validate_inputs():
    baseline=read(BASE);corpus=read(CORPUS_PATH);ch=sha256_file(CORPUS_PATH)
    for model in MODELS:
        s=baseline[model]
        if (s['prefix_length']!=128 or s['n_documents_effective']!=256 or s['batch']!=2
                or s['empty_row_policy']!='uniform' or not s['identity_kl_exactly_zero']
                or s['corpus_manifest_sha256']!=ch):raise ValueError('Completed V1 contract mismatch')
        if s['dtype']!=('torch.bfloat16' if 'Qwen' in model else 'torch.float32'):
            raise ValueError('Unexpected model dtype; do not silently substitute')
        if s.get('svd_implementation',{}).get('selected_driver') is not None:
            raise ValueError('Fixed original SVD convention required')
    if len(corpus['documents'])!=256 or len({d['doc_id'] for d in corpus['documents']})!=256:
        raise ValueError('Corpus must contain 256 distinct articles')
    return baseline,corpus


def guard():
    config=read(RUN)
    inputs={'source_V1_sha256':BASE,'corpus_manifest_sha256':CORPUS_PATH,
            'imported_harness_sha256':Path('phase2_downstream.py'),
            'primary_statistics_sha256':Path('phase24_p0_metrics.py'),
            'allocation_estimator_source_sha256':Path('phase21_allocation_v2_forward.py'),
            'protected_matrix_aggregate_sha256':MATRIX,
            'continuation_source_sha256':Path(__file__)}
    for key,path in inputs.items():
        if sha256_file(path)!=config[key]:raise ValueError(f'Preserve existing output: changed input/source {key}')
    return config


def preflight():
    if OUTPUT.exists():raise FileExistsError('Requested new forward aggregate already exists')
    baseline,corpus=validate_inputs()
    if RUN.exists():guard();return
    config={'schema_version':2,'started_UTC':datetime.now(timezone.utc).isoformat(),
            'authorization':'User explicitly resumed the deferred injection after completed V1; historical three-hour timeout remains untouched',
            'source_V1_sha256':sha256_file(BASE),'corpus_manifest_sha256':sha256_file(CORPUS_PATH),
            'imported_harness_sha256':sha256_file('phase2_downstream.py'),
            'primary_statistics_sha256':sha256_file('phase24_p0_metrics.py'),
            'allocation_estimator_source_sha256':sha256_file('phase21_allocation_v2_forward.py'),
            'continuation_source_sha256':sha256_file(__file__),
            'protected_matrix_aggregate_sha256':sha256_file(MATRIX),
            'models':list(MODELS),'prefix_length':128,'batch_by_model':{m:baseline[m]['batch'] for m in MODELS},
            'n_articles':256,'K':[8,16],'rank_rule':'q=K-1; cost=2*count(c>0)+q*(2n+1)<=K*(2n+1)',
            'GPU_lock':'/tmp/radon-gpu.lock','lock_scope':'one child process per model, released before CPU summary and the next model',
            'SVD_and_scale_references':'Reused immutable V1 per-article observations on identical corpus/targets/dtype/batch',
            'S_plus_L_SVD':'Imported factor_svd; fixed torch default exact float32 SVD, sequential schedule',
            'matrix_aggregate_modified':False,'n_bootstrap':2000,'seed':0,
            'source_pairs_sha256':{m:sha256_file(baseline[m]['pairs_path']) for m in MODELS}}
    controls=Path('out')/f"phase21_allocation_v2_forward_controls_{config['imported_harness_sha256'][:12]}.json"
    if not controls.exists():
        from phase21_allocation_v2_checks import main as check_adapter
        check_adapter(controls)
    control=read(controls)
    if not control['passed'] or control['imported_harness_sha256']!=config['imported_harness_sha256']:
        raise ValueError('Current-harness CPU adapter control failed')
    positive=paired_articles(np.arange(1,257,dtype=float))
    null=paired_articles(np.zeros(256))
    if positive['n_articles']!=256 or positive['rank_biserial']!=1 or positive['statistic']!=0:
        raise AssertionError('Signed-rank article unit/direction control failed')
    if null['rank_biserial']!=0 or null['p_two_sided']!=1:
        raise AssertionError('Explicit all-zero signed-rank control failed')
    references={'_meta':{'source_V1_sha256':config['source_V1_sha256'],'corpus_manifest_sha256':config['corpus_manifest_sha256'],
                        'prefix_length':128,'n_articles':256,'statistics':'Imported phase24.describe; median and 2000 whole-article bootstrap samples; means secondary'},'models':{}}
    for model in MODELS:
        groups=source_records(model,baseline,corpus);arms={}
        for arm,records in groups.items():
            validation=batch_statistics(records);completion=harness.completion_summary(validation)
            s=stats([r['kl'] for r in records],range(256))
            old=baseline[model]['arms'][arm]
            if abs(s['median']-old['median_kl'])>1e-12 or abs(s['mean']-old['mean_kl'])>1e-12:
                raise ArithmeticError('V1 reaggregation changed its per-article values')
            if completion!=old['uniform_completion']:raise ArithmeticError('V1 completion counters disagree')
            arms[arm]={'KL':s,'uniform_causal_completion':completion,'attention_validation':validation}
        references['models'][model]={'arms':arms,'source_pairs_path':baseline[model]['pairs_path'],
                                    'source_pairs_sha256':config['source_pairs_sha256'][model]}
    config['estimator_checks_path']=controls.as_posix();config['estimator_checks_sha256']=sha256_file(controls)
    config['signed_rank_controls']={'positive':positive,'all_zero':null}
    write_json_new(REFERENCES,references)
    config['references_path']=REFERENCES.as_posix();config['references_sha256']=sha256_file(REFERENCES)
    write_json_new(RUN,config)
    e4.log('FORWARD PREFLIGHT PASSED: completed V1 six models; all 256 articles per arm; imported current harness; CPU estimator/counters and 256-article signed-rank controls; historical matrix file unchanged')


def gpu_model(name,under_lock):
    if not under_lock:raise RuntimeError('Launch this worker only with flock /tmp/radon-gpu.lock and --under-gpu-lock')
    config=guard();baseline,corpus=validate_inputs();source=baseline[name]
    if sha256_file(source['pairs_path'])!=config['source_pairs_sha256'][name]:raise ValueError('V1 pairs changed')
    target,_=forward.paths(name,128)
    if target.exists():
        cached=read(target)
        if cached['imported_harness_sha256']!=config['imported_harness_sha256'] or sha256_file(cached['pairs_path'])!=cached['pairs_sha256']:
            raise ValueError('Existing forward result source/pairs mismatch')
        e4.log(f'FORWARD MODEL ALREADY COMPLETE {name}; no GPU model loaded');return
    from transformers import AutoModelForCausalLM,AttentionInterface
    bases=forward.read_svd_records(source,name,config['corpus_manifest_sha256'])
    harness.RECON.update(empty_row_policy='uniform',svd_driver=None,parallel_svd=False)
    AttentionInterface.register('p0_recon',harness.attention_forward)
    dtype={'torch.float32':torch.float32,'torch.bfloat16':torch.bfloat16}[source['dtype']]
    e4.log(f'GPU MODEL START {name}: n128, batch={source["batch"]}, dtype={source["dtype"]}; per-model flock process')
    model=AutoModelForCausalLM.from_pretrained(name,revision=corpus['models'][name]['revision'],
           local_files_only=True,dtype=dtype,attn_implementation='eager').to('cuda').eval()
    torch.manual_seed(0)
    forward.evaluate_length(model,name,128,source,bases,corpus,harness,
                            config['imported_harness_sha256'],config['corpus_manifest_sha256'])
    del model
    gc.collect();torch.cuda.empty_cache()
    guard()
    e4.log(f'GPU MODEL FINISHED {name}; model deleted, CUDA cache cleared; process exits and releases flock')


def enhanced_path(model):
    return Path('out')/f'phase21_allocation_v2_forward_resume_{slug(model)}_n128.json'


def summarize_model(model):
    config=guard();target=enhanced_path(model)
    if target.exists():return read(target)
    original,_=forward.paths(model,128);data=read(original)
    if data['imported_harness_sha256']!=config['imported_harness_sha256'] or sha256_file(data['pairs_path'])!=data['pairs_sha256']:
        raise ValueError('Forward source/pairs hash mismatch')
    with Path(data['pairs_path']).open(encoding='utf-8') as inp:rows=[json.loads(line) for line in inp]
    corpus=read(CORPUS_PATH)
    if len(rows)!=512:raise ValueError('Exactly 256 articles for both K required')
    for K in RANKS:
        selected=sorted((r for r in rows if r['budget_rank_K']==K),key=lambda r:r['document_index'])
        if [r['document_index'] for r in selected]!=list(range(256)):raise ValueError('Incomplete/duplicate article cohort')
        differences=[];points=[]
        for i,row in enumerate(selected):
            if row['doc_id']!=corpus['documents'][i]['doc_id']:raise ValueError('Forward article identity mismatch')
            value=row['named_KL']-row['svd_KL'];differences.append(value)
            points.append({'document_index':i,'doc_id':row['doc_id'],'difference_KL_named_minus_SVD':value})
        pair=data['budgets'][str(K)]['paired_KL_named_minus_SVD']
        pair['wilcoxon']=paired_articles(differences)
        data['budgets'][str(K)]['paired_differences_by_article']=points
    refs=read(REFERENCES)['models'][model]['arms']
    data['V1_scale_references']={mode:refs[f'phase2:{mode}'] for mode in REFS}
    for K in RANKS:
        b=data['budgets'][str(K)];ref=refs[f'phase2:svd:{K}']
        if b['SVD_KL']!=ref['KL'] or b['uniform_causal_completion_by_mode']['svd']!=ref['uniform_causal_completion']:
            raise ArithmeticError('Reused SVD per-article statistics/counters changed')
    data['source_forward_summary_path']=original.as_posix();data['source_forward_summary_sha256']=sha256_file(original)
    data['continuation_run_path']=RUN.as_posix();data['SVD_and_reference_arms_recomputed']=False
    data['n_articles_for_signed_rank']=256;data['summary_device']='CPU outside GPU lock'
    write_json_new(target,data)
    e4.log(f'CPU FORWARD SUMMARY COMPLETE {model}: 256 paired articles, K8/16, Wilcoxon/rank-biserial and V1 reference medians/CIs')
    return data


def assemble():
    config=guard()
    results={m:{'128':summarize_model(m)} for m in MODELS}
    result={'schema_version':2,'status':'complete','_meta':{**config,'finished_UTC':datetime.now(timezone.utc).isoformat(),
            'prefix_lengths':[128],'last_token_only':True,'uniform_causal_completion':True,
            'primary_statistics':'Imported phase24_p0_metrics.describe; 2000 whole-article bootstrap samples; medians primary, means secondary',
            'paired_test':'Wilcoxon signed-rank on all 256 article differences; rank-biserial; positive S+L minus SVD favors SVD',
            'GPU_command':'flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase21_allocation_v2_forward_resume.py model --model MODEL --under-gpu-lock',
            'matrix_aggregate_sha256_after':sha256_file(MATRIX)},'models':results}
    write_json_new(OUTPUT,result)
    e4.log(f'FORWARD COMPLETE {OUTPUT}: all six models, both K, 256 matched articles, complete row counters; matrix aggregate unchanged')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('preflight','model','summarize-model','assemble'))
    parser.add_argument('--model',choices=MODELS)
    parser.add_argument('--under-gpu-lock',action='store_true')
    args=parser.parse_args()
    if args.command=='preflight':preflight()
    elif args.command=='assemble':assemble()
    elif not args.model:parser.error('--model required')
    elif args.command=='model':gpu_model(args.model,args.under_gpu_lock)
    else:summarize_model(args.model)
