# Attention Is Concentrated but Not a Sum of Few Lines

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20673537.svg)](https://doi.org/10.5281/zenodo.20673537)

Code and result files for the paper *"Attention Is Concentrated but Not a Sum of
Few Lines: a Misleading Radon Signal and a Named-plus-Low-Rank Resolution"*
(earlier title: "... but Not Line-Decomposable ...").

Version 3.0.0 is the revision prepared after review. It replaces several earlier
numbers: the forward-pass injection is now causal by construction (reconstructions
restricted to the causal support and scored at the last position only), sampling
is stratified over articles, layers and heads with frozen manifests, the named
share is reported as an energy ratio under an explicit allocation convention, and
sink edits are compared with mass-matched controls. See "Revision pipeline" below.

Everything runs end-to-end on a single consumer GPU (tested on an NVIDIA RTX
3060, 12 GB). Models (GPT-2 small/medium, Pythia-410m/1.4b, Qwen2.5-0.5B/3B) and
data (WikiText-2) are public and downloaded automatically from the Hugging Face
Hub.

## Setup

```bash
python -m venv .venv && .venv/Scripts/activate   # (Windows) or source .venv/bin/activate
pip install -r requirements.txt
python make_corpus.py        # builds wikitext2_train.txt (used by all phases)
```

## Pipeline (one script per experiment)

| Script | Paper section | What it does |
|---|---|---|
| `phase0_radon_attention.py` | 4.1 | Radon concentration metric vs. causal controls (GPT-2) |
| `phase05_line_decomposition.py` | 4.2 | Uniform-line matching pursuit vs. rank-k SVD |
| `phase06_profiled_lines.py` | 4.2 | Profiled (exponential-band) dictionary variant |
| `phase1_multimodel.py` | 4.2, Table 1 | Five-model replication (concentration + reconstruction) |
| `phase2_downstream.py` | 4.4 | Forward-pass injection: KL of reconstructed attention |
| `phase3_robustness.py` | 4.3 | Length robustness 128/256/512 (streaming/reservoir) |
| `phase4_anova.py` | 7.1 | Functional-ANOVA: sink as rank-1 column effect |
| `phase5_msclean.py` | 7.2 | MS-CLEAN structured pursuit (named fraction) |
| `phase6_srpca.py` | 7.2 | Structured robust PCA (S named + L low-rank) |
| `phase7_editability.py` | 7.3 | Sink editing vs. random-column control (KL) |
| `phase8_lostmiddle.py` | 7.4 | Positional-retrieval probe + sink calibration (use `--tag`) |
| `phase9_bigmodel.py` | 4.2/7.1 | 3B replication (Qwen2.5-3B, bf16, streaming) |
| `phase10_baselines.py` | 7.4 | ACT-style adaptive baseline comparison |
| `phase11_kv.py` | 7.4, Fig. 12 | Multi-distractor key-value retrieval benchmark |
| `phase12_coherence.py` | 7 | Mutual coherence of the named dictionary |
| `phase13_stats.py` | Table 2 | Canonical aggregator: middle window, pooled z-tests, Holm |
| `phase14_adaptive.py` | 7.4 | Per-head adaptive beta ablation (negative result) |
| `phase15_interaction.py` | 7.1 | Sink-column constancy (non-tautology check) |
| `phase16_longcontext.py` | 7.4 | Long-context KV retrieval with U-shape diagnostic (n=512/1024, multi-token key) |
| `phase17_efficiency.py` | 4.x | Rate-distortion: parameters vs fidelity (line dictionary / SVD / two-channel) |
| `phase18_betacv.py` | 7.4 | Cross-validated sink-calibration beta (selected on one probe family, scored on a held-out one) |
| `phase_stats.py` | (shared) | Dispersion helpers: IQR, mean/std, bootstrap median CI (used by all phases) |
| `paper_figures*.py` | all figures | 300-dpi figure generation |

`out/` contains the per-seed result JSONs used in the paper (files tagged
`_s0/_s1/_s2` are the three seeds; `phase13_stats.json` is the canonical pooled
analysis). The middle window is defined once as positions $p$ with
$0.25L \le p \le 0.75L$; significance is two-proportion z with Holm correction
(see `phase13_stats.py`).

## Reproducing the headline numbers

```bash
# matrix-level (Table 1)
python phase1_multimodel.py
python phase9_bigmodel.py

# intervention (Table 2), three seeds
python phase8_lostmiddle.py --n_per_pos 400 --seed 0 --tag s0
python phase8_lostmiddle.py --n_per_pos 400 --seed 1 --betas 1.0 0.25 --tag s1
python phase8_lostmiddle.py --n_per_pos 400 --seed 2 --betas 1.0 0.25 --tag s2
python phase11_kv.py --seed 0 --tag s0   # idem s1, s2
python phase13_stats.py
```

## License

MIT.

## Revision pipeline (v3.0.0)

| Script | What it does |
|---|---|
| `sampling.py`, `extract_attn.py` | Frozen article manifests; stratified article x layer x head sampling; attention archives |
| `phase24_p0_metrics.py`, `phase9_bigmodel.py`, `phase3_robustness.py` | Concentration and line vs. SVD on the stratified samples |
| `phase2_downstream.py`, `phase7_editability.py`, `phase32_downstream_tests.py` | Causal forward-pass injection, last-position KL, paired tests |
| `phase19_richlines.py`, `phase19b_*`, `phase19c_*` | All-orientation lines, sinogram compression, learned segments, semiseparable baseline, controls |
| `phase20_lowrank_baselines.py` | Randomized SVD, CUR, Nystrom-type skeleton |
| `phase21_allocation_v2.py`, `phase21_allocation_v2_forward*.py` | Two-channel allocation conventions, fixed-budget comparison, forward injection |
| `phase22_sink_evolution.py` | Sink across Pythia training checkpoints; equalized-mass ablations |
| `phase27_qwen7b.py`, `phase30_anova_curves.py`, `phase54_rowshuffle_control.py` | Qwen2.5-7B replication, ANOVA and reconstruction curves, row-shuffled Radon control |
| `phase36_exempt_heads.py`, `phase50_*` | Nearly diagonal heads; semiseparable forward comparison |
| `phase37_mass_matched.py`, `phase38_paired_items.py`, `phase45_currentcv_items.py`, `revision_v3_*` | Mass-matched sink edits, paired item tests for retrieval, beta cross-validation |
| `paper_figures_v2.py` | Figures of the revised paper |

Aggregate results are in `out/*.json`. The attention archives and per-instance
ledgers (several GB) are archived separately on Zenodo; the archives can also be
regenerated from the manifests with `extract_attn.py`.

