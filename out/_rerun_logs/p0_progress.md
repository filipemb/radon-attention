
- 2026-11-09T19:10:28+00:00 | V2 corpus: Frozen 256 articles of 602 common eligible; sha256=fbdd1cdbbc1573c99497f6d50122db53cfbfecce76f143f18ad1cd593185d7f5 | elapsed_seconds=42.537 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B sampling.py prepare`

- 2026-11-09T19:11:31+00:00 | V2 implementation sanity: First capture attempt stopped before writing outputs: vanilla-logit equality failed because Transformers does not construct a mask for a custom AttentionInterface name. Explicit causal mask added; exact equality remains mandatory.

- 2026-11-09T19:11:40+00:00 | V2 extraction: gpt2, n=128, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=3.583 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models gpt2 --lengths 128 256`

- 2026-11-09T19:11:51+00:00 | V2 extraction: gpt2, n=256, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=8.138 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models gpt2 --lengths 128 256`

- 2026-11-09T19:12:06+00:00 | V2 extraction: gpt2-medium, n=128, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=6.678 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models gpt2-medium EleutherAI/pythia-410m EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:12:19+00:00 | V2 extraction: gpt2-medium, n=256, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=10.606 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models gpt2-medium EleutherAI/pythia-410m EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:12:25+00:00 | V2 extraction: EleutherAI/pythia-410m, n=128, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=5.024 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models gpt2-medium EleutherAI/pythia-410m EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:12:38+00:00 | V2 extraction: EleutherAI/pythia-410m, n=256, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=10.791 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models gpt2-medium EleutherAI/pythia-410m EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:12:48+00:00 | V2 extraction: EleutherAI/pythia-1.4b, n=128, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=9.291 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models gpt2-medium EleutherAI/pythia-410m EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:13:17+00:00 | V2 sampling checks: Six models: reproducibility, all strata, paired lengths and rejection of invalid inputs passed | elapsed_seconds=0.437 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --sampling`

- V2 filename regression stopped the run: pathlib.with_suffix interpreted decimal model names as extensions. Fixed by appending extensions; verified Pythia-1.4b n128 artifacts renamed without changing their contents. No JSON result overwritten.

- 2026-11-09T19:14:03+00:00 | V2 extraction: EleutherAI/pythia-1.4b, n=256, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=16.695 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:14:10+00:00 | V2 extraction: Qwen/Qwen2.5-0.5B, n=128, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=6.520 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:14:15+00:00 | V2 sampling checks: Six models: reproducibility, all strata, paired lengths and rejection of invalid inputs passed | elapsed_seconds=0.598 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --sampling`

- 2026-11-09T19:14:24+00:00 | V2 extraction: Qwen/Qwen2.5-0.5B, n=256, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=10.872 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:14:43+00:00 | V2 extraction: Qwen/Qwen2.5-3B, n=128, 64 documents, 2304 matrices; all checks passed | elapsed_seconds=17.948 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:15:08+00:00 | V2 extraction: Qwen/Qwen2.5-3B, n=256, 64 documents, 2304 matrices; all checks passed | elapsed_seconds=21.037 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models EleutherAI/pythia-1.4b Qwen/Qwen2.5-0.5B Qwen/Qwen2.5-3B --lengths 128 256 --ready`

- 2026-11-09T19:15:27+00:00 | V2 READY: All 12 archives verified; 19968 matrices, 695611186 bytes

- 2026-11-09T19:18:05+00:00 | V2 core metrics: gpt2-medium, n=128, 1536 raw pairs, 64 documents | elapsed_seconds=116.592 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models gpt2-medium --lengths 128`

- 2026-11-09T19:18:05+00:00 | V2 core metrics: gpt2, n=128, 1536 raw pairs, 64 documents | elapsed_seconds=116.676 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models gpt2 --lengths 128`

- 2026-11-09T19:19:30+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=4.695 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction`

- 2026-11-09T19:20:21+00:00 | V2 core metrics: EleutherAI/pythia-410m, n=128, 1536 raw pairs, 64 documents | elapsed_seconds=135.499 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models EleutherAI/pythia-410m --lengths 128`

- 2026-11-09T19:21:50+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=7.133 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction`

- 2026-11-09T19:23:22+00:00 | V2 core metrics: EleutherAI/pythia-1.4b, n=128, 1536 raw pairs, 64 documents | elapsed_seconds=181.243 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models EleutherAI/pythia-1.4b --lengths 128`

- V1 strict validation stopped the first downstream attempt before any aggregate JSON: remasked/clamped rank-4 SVD produced an empty causal row on the first batch. Corpus, seed, rank budgets and row-sum tolerances remain fixed. Investigating the invalid-row construction before resuming. Six raw endpoint records from completed arms remain preserved.

- 2026-11-09T19:27:35+00:00 | V2 core metrics: gpt2, n=256, 1536 raw pairs, 64 documents | elapsed_seconds=686.270 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models gpt2 --lengths 256`

- 2026-11-09T19:27:37+00:00 | V2 core metrics: gpt2-medium, n=256, 1536 raw pairs, 64 documents | elapsed_seconds=688.161 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models gpt2-medium --lengths 256`

- 2026-11-09T19:30:32+00:00 | V2 core metrics: Qwen/Qwen2.5-0.5B, n=128, 1536 raw pairs, 64 documents | elapsed_seconds=177.487 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models Qwen/Qwen2.5-0.5B --lengths 128`

- 2026-11-09T19:30:46+00:00 | V2 core metrics: EleutherAI/pythia-410m, n=256, 1536 raw pairs, 64 documents | elapsed_seconds=760.938 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models EleutherAI/pythia-410m --lengths 256`

- 2026-11-09T19:33:19+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=3.468 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction`

- 2026-11-09T19:34:58+00:00 | V2 core metrics: Qwen/Qwen2.5-3B, n=128, 2304 raw pairs, 64 documents | elapsed_seconds=265.720 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models Qwen/Qwen2.5-3B --lengths 128`

- Logging correction: the earlier phase25 retrieval and fraction/constancy checks were mislabeled as --reconstruction in the progress formatter. Actual commands were:
  - `.venv/Scripts/python.exe -B phase25_p0_checks.py --retrieval-audit --out out/phase25_retrieval_audit_v2.json` | elapsed_seconds=7.133
  - `.venv/Scripts/python.exe -B phase25_p0_checks.py --fractions-constancy --out out/phase25_fraction_constancy_checks_v2.json` | elapsed_seconds=3.468

- 2026-11-09T19:36:31+00:00 | V2 core metrics: EleutherAI/pythia-1.4b, n=256, 1536 raw pairs, 64 documents | elapsed_seconds=789.113 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models EleutherAI/pythia-1.4b --lengths 256`

- 2026-11-09T19:36:44+00:00 | V1 legacy mass: gpt2; all 1536 frozen matrices x six ranks | elapsed_seconds=13.742 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- V1 methodological decision pending user response: finite SVD rank-4 reconstruction produced an empty row after required causal mask + clamp, at flattened head index 11 / query index 15 / first GPT-2 batch. No completion rule was applied, no tolerance changed, and no affected behavioral result was generated. Suggested parameter-free completion: causal uniform, with counts reported equally for every method. Alternatives sent: retain original row, or record arm as invalid.

- V3/V4 implementation prepared while V1 choice is pending; full data runs remain queued after V1. Exact QR reduction retains the NNLS objective, ranks and five iterations. Analytic identities, scaling invariance and an averaging counterexample passed.

- 2026-11-09T19:36:57+00:00 | V1 legacy mass: gpt2-medium; all 1536 frozen matrices x six ranks | elapsed_seconds=12.869 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T19:37:12+00:00 | V1 legacy mass: EleutherAI/pythia-410m; all 1536 frozen matrices x six ranks | elapsed_seconds=14.429 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T19:37:26+00:00 | V1 legacy mass: EleutherAI/pythia-1.4b; all 1536 frozen matrices x six ranks | elapsed_seconds=14.231 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T19:37:39+00:00 | V1 legacy mass: Qwen/Qwen2.5-0.5B; all 1536 frozen matrices x six ranks | elapsed_seconds=13.436 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T19:37:59+00:00 | V1 legacy mass: Qwen/Qwen2.5-3B; all 2304 frozen matrices x six ranks | elapsed_seconds=19.957 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T19:38:01+00:00 | V2 metrics command complete: 6 datasets, workers=1, four CPU threads per worker | elapsed_seconds=96.391 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass --workers 1`

- 2026-11-09T19:38:38+00:00 | V2 extraction: gpt2, n=512, 64 documents, 1536 matrices; all checks passed | elapsed_seconds=63.239 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B extract_attn.py --models gpt2 --lengths 512`

- 2026-11-09T19:40:06+00:00 | V1 six-model identity: gpt2; 256 documents; both identity harnesses and suffix invariance exact | elapsed_seconds=20.712 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity`

- 2026-11-09T19:40:42+00:00 | V1 six-model identity: gpt2-medium; 256 documents; both identity harnesses and suffix invariance exact | elapsed_seconds=36.183 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity`

- 2026-11-09T19:41:19+00:00 | V1 six-model identity: EleutherAI/pythia-410m; 256 documents; both identity harnesses and suffix invariance exact | elapsed_seconds=36.960 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity`

- 2026-11-09T19:41:58+00:00 | V2 core metrics: Qwen/Qwen2.5-0.5B, n=256, 1536 raw pairs, 64 documents | elapsed_seconds=861.173 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models Qwen/Qwen2.5-0.5B --lengths 256`

- 2026-11-09T19:42:23+00:00 | V1 six-model identity: EleutherAI/pythia-1.4b; 256 documents; both identity harnesses and suffix invariance exact | elapsed_seconds=64.192 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity`

- 2026-11-09T19:43:06+00:00 | V1 six-model identity: Qwen/Qwen2.5-0.5B; 256 documents; both identity harnesses and suffix invariance exact | elapsed_seconds=42.654 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity`

- 2026-11-09T19:44:33+00:00 | V1 six-model identity: Qwen/Qwen2.5-3B; 256 documents; both identity harnesses and suffix invariance exact | elapsed_seconds=87.125 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity`

- 2026-11-09T19:44:33+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=299.628 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity --out out/phase25_identity_checks_v2.json`

- V1 identity and suffix checks finished for all six models, 256 documents per model, exactly zero KL/logit differences in both harnesses. Full reconstruction-arm run remains pending the user's empty-row policy. V3 full measurements started as independent work on the frozen V2 matrices; no V1 completion rule is assumed. Three CPU workers x four threads; V2's final 3B n256 core worker uses at most four more.

- 2026-11-09T19:48:23+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=10.208 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --geometry --out out/phase25_geometry_checks_v2.json`

- 2026-11-09T19:49:46+00:00 | V3 named metrics: gpt2, n=128, all 1536 instances and 15 configurations | elapsed_seconds=258.996 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models gpt2 --lengths 128`

- 2026-11-09T19:49:46+00:00 | V3 named metrics: gpt2-medium, n=128, all 1536 instances and 15 configurations | elapsed_seconds=259.326 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models gpt2-medium --lengths 128`

- 2026-11-09T19:54:55+00:00 | V3 named metrics: EleutherAI/pythia-410m, n=128, all 1536 instances and 15 configurations | elapsed_seconds=308.809 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models EleutherAI/pythia-410m --lengths 128`

- 2026-11-09T19:55:28+00:00 | V2 core metrics: Qwen/Qwen2.5-3B, n=256, 2304 raw pairs, 64 documents | elapsed_seconds=1482.111 | command: `OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B phase24_p0_metrics.py --models Qwen/Qwen2.5-3B --lengths 256`

- 2026-11-09T19:55:31+00:00 | V2 metrics command complete: 12 datasets, workers=4, four CPU threads per worker | elapsed_seconds=2366.203 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --workers 4`

- 2026-11-09T19:58:12+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=9.586 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction --out out/phase25_completion_options_checks_v2.json`

- 2026-11-09T20:01:42+00:00 | V3 named metrics: gpt2, n=256, all 1536 instances and 15 configurations | elapsed_seconds=974.681 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models gpt2 --lengths 256`

- 2026-11-09T20:07:09+00:00 | V3 named metrics: gpt2-medium, n=256, all 1536 instances and 15 configurations | elapsed_seconds=1043.259 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models gpt2-medium --lengths 256`

- 2026-11-09T20:07:12+00:00 | V1 legacy mass: gpt2; all 1536 frozen matrices x six ranks | elapsed_seconds=22.410 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T20:07:24+00:00 | V3 named metrics: EleutherAI/pythia-1.4b, n=128, all 1536 instances and 15 configurations | elapsed_seconds=342.606 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models EleutherAI/pythia-1.4b --lengths 128`

- 2026-11-09T20:07:35+00:00 | V1 legacy mass: gpt2-medium; all 1536 frozen matrices x six ranks | elapsed_seconds=21.984 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T20:07:51+00:00 | V1 legacy mass: EleutherAI/pythia-410m; all 1536 frozen matrices x six ranks | elapsed_seconds=16.280 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T20:08:08+00:00 | V1 legacy mass: EleutherAI/pythia-1.4b; all 1536 frozen matrices x six ranks | elapsed_seconds=16.798 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T20:08:25+00:00 | V1 legacy mass: Qwen/Qwen2.5-0.5B; all 1536 frozen matrices x six ranks | elapsed_seconds=17.238 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

- 2026-11-09T20:08:51+00:00 | V1 legacy mass: Qwen/Qwen2.5-3B; all 2304 frozen matrices x six ranks | elapsed_seconds=26.287 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass`

## Operational checkpoint
- V2 complete: 12 primary archives verified, READY published, 19,968 matrices, 64 articles per dataset. Core metrics and raw pairs complete; aggregate files phase1_multimodel_v2.json, phase3_robustness_v2.json, phase9_bigmodel_v2.json.
- V1 implemented; full reconstruction run stopped by strict empty-row validation. User question remains pending (uniform causal completion suggested; original-row completion or invalid-arm reporting are alternatives). Default stays error. No completion choice has been applied to scientific data.
- V1 identity and suffix checks: all 6 models x 256 articles, exact KL/logit equality in phase2 and phase7. Retrieval audit found no target leakage; phase8/10/11/14/16/18 unchanged. Additional phase8 beta=0 zero-row issue is documented outside the conditional edit scope.
- Legacy upper mass finished for all six models; rank8 medians 7.56%-10.65%. Additional source-matrix empty-row diagnostic is running independently.
- V3 full named metrics running: phase26_p0_named.py --workers 3. Every matrix is used for 12 greedy and 3 alternating configurations. Native CPU threads capped at four per worker. V4 and V5 implementations and tests are prepared; their full runs have not started.
- Extra GPT-2 n512 archive verified for V5; same 64 articles and balanced head/layer design. V5 predeclares one paired matrix per document (64 measurements per length), rank8, five iterations, dense and equivalent QR NNLS with counterbalanced timing order.
- Next independent commands after V3: phase15_interaction.py --workers 3 (V4), then phase17_efficiency.py (V5). Both CPU only. Full V1 command after user policy choice: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --empty-row-policy uniform (or original). The parser defaults to error; do not assume the pending choice.
- Reconstruction CPU tests, geometry projection equivalence, norm/energy/cross-term identities, per-sequence averaging counterexample, sampling balance/reproducibility and six-model identity checks have passed. Strict reconstruction checks reject empty rows by default; completion alternatives were unit-tested only on synthetic inputs.
- Final read-only audit: phase25_p0_checks.py --delivery-audit --out out/p0_delivery_v2.json. It explicitly marks missing V1 aggregate outputs as incomplete and inventories all source/data/result files. Run only once other requested outputs exist; choose a pending-specific filename if V1 remains unresolved.

- 2026-11-09T20:08:53+00:00 | V1 diagnostic command complete: 6 datasets, workers=1, four CPU threads per worker | elapsed_seconds=130.694 | command: `.venv/Scripts/python.exe -B phase24_p0_metrics.py --empty-row-diagnostic --workers 1`

- 2026-11-09T20:11:34+00:00 | V3 named metrics: EleutherAI/pythia-410m, n=256, all 1536 instances and 15 configurations | elapsed_seconds=999.153 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models EleutherAI/pythia-410m --lengths 256`

- 2026-11-09T20:11:44+00:00 | V3 named metrics: Qwen/Qwen2.5-0.5B, n=128, all 1536 instances and 15 configurations | elapsed_seconds=259.541 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models Qwen/Qwen2.5-0.5B --lengths 128`

- 2026-11-09T20:18:07+00:00 | V3 named metrics: Qwen/Qwen2.5-3B, n=128, all 2304 instances and 15 configurations | elapsed_seconds=382.679 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models Qwen/Qwen2.5-3B --lengths 128`

- 2026-11-09T20:20:48+00:00 | V3 named metrics: EleutherAI/pythia-1.4b, n=256, all 1536 instances and 15 configurations | elapsed_seconds=818.819 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models EleutherAI/pythia-1.4b --lengths 256`

- V4 per-forward constancy launched on the fourth CPU slot while V3 finishes the remaining datasets. It reads the same immutable archives and is independent of fitting and of the pending V1 completion policy. V5 timing will wait until the other P0 CPU calculations finish to avoid adding our own contention to the benchmark.

- 2026-11-09T20:21:07+00:00 | V4 constancy: gpt2, n=128; all 1536 individual forward matrices | elapsed_seconds=4.549 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models gpt2 --lengths 128`

- 2026-11-09T20:21:17+00:00 | V4 constancy: gpt2, n=256; all 1536 individual forward matrices | elapsed_seconds=9.826 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models gpt2 --lengths 256`

- 2026-11-09T20:21:22+00:00 | V4 constancy: gpt2-medium, n=128; all 1536 individual forward matrices | elapsed_seconds=4.634 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models gpt2-medium --lengths 128`

- 2026-11-09T20:21:33+00:00 | V4 constancy: gpt2-medium, n=256; all 1536 individual forward matrices | elapsed_seconds=10.812 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models gpt2-medium --lengths 256`

- 2026-11-09T20:21:37+00:00 | V2 native source audit: All regression checks passed | elapsed_seconds=42.920 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --capture-source --out out/phase25_native_source_checks_v2.json`

- 2026-11-09T20:21:37+00:00 | V4 constancy: EleutherAI/pythia-410m, n=128; all 1536 individual forward matrices | elapsed_seconds=4.731 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models EleutherAI/pythia-410m --lengths 128`

- 2026-11-09T20:21:48+00:00 | V4 constancy: EleutherAI/pythia-410m, n=256; all 1536 individual forward matrices | elapsed_seconds=10.603 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models EleutherAI/pythia-410m --lengths 256`

- 2026-11-09T20:21:53+00:00 | V4 constancy: EleutherAI/pythia-1.4b, n=128; all 1536 individual forward matrices | elapsed_seconds=4.441 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models EleutherAI/pythia-1.4b --lengths 128`

- 2026-11-09T20:22:03+00:00 | V4 constancy: EleutherAI/pythia-1.4b, n=256; all 1536 individual forward matrices | elapsed_seconds=10.000 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models EleutherAI/pythia-1.4b --lengths 256`

- 2026-11-09T20:22:07+00:00 | V4 constancy: Qwen/Qwen2.5-0.5B, n=128; all 1536 individual forward matrices | elapsed_seconds=4.629 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models Qwen/Qwen2.5-0.5B --lengths 128`

- 2026-11-09T20:22:17+00:00 | V4 constancy: Qwen/Qwen2.5-0.5B, n=256; all 1536 individual forward matrices | elapsed_seconds=9.991 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models Qwen/Qwen2.5-0.5B --lengths 256`

- 2026-11-09T20:22:24+00:00 | V4 constancy: Qwen/Qwen2.5-3B, n=128; all 2304 individual forward matrices | elapsed_seconds=6.770 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models Qwen/Qwen2.5-3B --lengths 128`

- 2026-11-09T20:22:39+00:00 | V4 constancy: Qwen/Qwen2.5-3B, n=256; all 2304 individual forward matrices | elapsed_seconds=15.147 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --models Qwen/Qwen2.5-3B --lengths 256`

- 2026-11-09T20:22:41+00:00 | V4 command complete: 12 datasets | elapsed_seconds=104.199 | command: `.venv/Scripts/python.exe -B phase15_interaction.py --workers 1`

- 2026-11-09T20:25:15+00:00 | V3 named metrics: Qwen/Qwen2.5-0.5B, n=256, all 1536 instances and 15 configurations | elapsed_seconds=820.593 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models Qwen/Qwen2.5-0.5B --lengths 256`

- 2026-11-09T20:31:46+00:00 | P0 comparison: Saved old/new core, norm/energy and constancy comparisons; old document counts explicitly unknown | elapsed_seconds=0.016 | command: `venv Python JSON comparison -> out/p0_comparison_v2.json`

- 2026-11-09T20:36:18+00:00 | V3 named metrics: Qwen/Qwen2.5-3B, n=256, all 2304 instances and 15 configurations | elapsed_seconds=1091.296 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --models Qwen/Qwen2.5-3B --lengths 256`

- 2026-11-09T20:36:20+00:00 | V3 command complete: 12 datasets; methods=['msclean', 'srpca'] | elapsed_seconds=3058.972 | command: `.venv/Scripts/python.exe -B phase26_p0_named.py --workers 3`

- 2026-11-09T20:37:23+00:00 | V5 analysis cost: n=128; 64 paired documents, rank=8, T=5, dense and QR NNLS | elapsed_seconds=8.115 | command: `.venv/Scripts/python.exe -B phase17_efficiency.py`

- 2026-11-09T20:37:47+00:00 | V5 analysis cost: n=256; 64 paired documents, rank=8, T=5, dense and QR NNLS | elapsed_seconds=24.251 | command: `.venv/Scripts/python.exe -B phase17_efficiency.py`

- 2026-11-09T20:39:50+00:00 | V5 analysis cost: n=512; 64 paired documents, rank=8, T=5, dense and QR NNLS | elapsed_seconds=122.358 | command: `.venv/Scripts/python.exe -B phase17_efficiency.py`

- 2026-11-09T20:39:50+00:00 | V5 command complete: All three lengths completed; analysis cost only | elapsed_seconds=154.784 | command: `.venv/Scripts/python.exe -B phase17_efficiency.py`

- 2026-11-09T20:42:56+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=7.114 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction --out out/phase25_final_reconstruction_checks_v2.json`

- 2026-11-09T20:43:24+00:00 | P0 delivery audit: Available audits passed; required pending outputs: ['out/phase2_downstream_v2.json', 'out/phase7_editability_v2.json'] | elapsed_seconds=33.106 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --delivery-audit --out out/p0_delivery_pending_v2.json`

## Entrega P0: resultados e pendência de V1

- Concluídos: V2 (dados e métricas núcleo), V3, V4 e custo de análise de V5.
- V1: código e sanidades implementados; identidade e invariância ao sufixo exatas nos seis modelos x 256 artigos. A medição completa dos braços de reconstrução permanece pendente da regra para linhas zeradas após máscara + clamp. A opção padrão continua sendo erro.
- Pergunta enviada e ainda sem resposta: completar linhas zeradas com uniforme causal, preservar a distribuição original ou registrar o braço como inválido. Nenhuma opção de completamento foi aplicada aos dados científicos.
- Arquivos antigos em out/ não foram sobrescritos. Os seis registros do primeiro ensaio interrompido estão preservados em out/pairs/downstream_gpt2_v2.jsonl e não constituem um resultado final de V1.

### Comparação em n=128

As diferenças combinam amostragem/corpus e definição da métrica. Não são ganhos isolados de algoritmo. Os documentos antigos não estavam contados nos JSONs antigos.

| Modelo | Matrizes antigas -> novas | Linha k8 antiga -> nova | SVD k8 antiga -> nova | M5 norma antiga -> nova | M5 energia nova | Sink desvio na média antigo -> por forward novo |
|---|---:|---:|---:|---:|---:|---:|
| gpt2 | 200 -> 1536 | 0.469 -> 0.460 | 0.225 -> 0.207 | 0.888 -> 0.905 | 0.819 | 3.9% -> 17.8% |
| gpt2-medium | 200 -> 1536 | 0.432 -> 0.439 | 0.119 -> 0.144 | 0.911 -> 0.907 | 0.822 | 3.0% -> 16.1% |
| EleutherAI/pythia-410m | 200 -> 1536 | 0.440 -> 0.476 | 0.175 -> 0.194 | 0.886 -> 0.816 | 0.666 | 2.2% -> 18.8% |
| EleutherAI/pythia-1.4b | 200 -> 1536 | 0.405 -> 0.489 | 0.146 -> 0.183 | 0.926 -> 0.765 | 0.585 | 2.1% -> 23.2% |
| Qwen/Qwen2.5-0.5B | 200 -> 1536 | 0.498 -> 0.501 | 0.268 -> 0.272 | 0.913 -> 0.880 | 0.775 | 6.3% -> 21.4% |
| Qwen/Qwen2.5-3B | 100 -> 2304 | 0.468 -> 0.481 | 0.225 -> 0.222 | 0.890 -> 0.881 | 0.776 | não disponível -> 19.6% |

Todos os conjuntos novos da tabela usam 64 artigos. Os cinco modelos menores têm 1.536 matrizes por comprimento e o 3B tem 2.304. V1 usa corpus previamente fixado de 256 artigos; 256 alvos finais por braço, quando a regra pendente for definida.

### Faixas novas das medianas por modelo em n=128

| Configuração | Razão de normas | Razão de energias |
|---|---:|---:|
| MS-CLEAN m=1 | 0.697 a 0.879 | 0.486 a 0.773 |
| MS-CLEAN m=5 | 0.765 a 0.907 | 0.585 a 0.822 |
| sRPCA r=8 | 0.732 a 0.892 | 0.536 a 0.796 |

Os JSONs também guardam os termos cruzados, redução de erro, distribuições e pares de todas as 15 configurações, em ambos os comprimentos, nos mesmos exemplos.

### Custo medido de ajuste: CPU, quatro threads, r=8, T=5

| n | Documentos/matrizes pareados | Mediana denso (ms) | Mediana QR (ms) |
|---:|---:|---:|---:|
| 128 | 64 | 84.640 | 36.483 |
| 256 | 64 | 245.285 | 118.781 |
| 512 | 64 | 1279.514 | 512.163 |

Os 64 trios documento/camada/cabeça são idênticos entre comprimentos. As duas implementações foram medidas em cada instância; ordem contrabalanceada. Setup, warmup declarado e tempos NNLS/SVD separados estão no JSON. É custo de análise, sem alegação de aceleração de inferência.

### Sanidades finais

- V2: forma e float16, >=64 artigos, >=1024 matrizes, igualdade de contagem por camada e equilíbrio de cabeças; 12 bases primárias, 19.968 matrizes; READY verificado.
- Nenhum NaN, infinito, peso negativo ou valor acima da diagonal nas bases. Soma de linhas respeita limite fixo de arredondamento IEEE float16; softmax fonte verificado a 2e-6. Não houve renormalização dos arquivos nem substituição de NaN por zero.
- Observador independente do softmax eager original: coincidência exata depois de float16 nas 312 matrizes selecionadas do primeiro artigo, todas as camadas dos 12 conjuntos.
- Identidade nos dois harnesses: KL e diferença de logits exatamente zero nos 6 modelos x 256 artigos. Invariância ao sufixo na identidade e teste que observa o corte físico do prefixo: passaram.
- 21 casos de reconstrução: máscara com cache/offset, positividade, soma de linha e primeira linha intacta na edição: passaram. Linhas vazias são rejeitadas por padrão; uniforme e original foram testados somente em dados sintéticos.
- Projeção geométrica com QR cacheado vs mínimos quadrados denso: erro relativo 7.413e-6, abaixo do limite fixado 1e-5. Tolerância de soma de linha permaneceu 2e-6.
- NNLS denso vs redução QR: equivalência passou antes de cada conjunto de V3 e em cada par do benchmark de V5 (limite 1e-9). Identidades norma/energia/termo cruzado passaram em todas as instâncias.
- Auditoria final: 36 grupos de pares brutos completos, IDs na ordem do manifesto, todas as configurações nos mesmos exemplos; 384 tempos pareados de V5, sem perda de documentos.
- Sanidade que interrompe V1: SVD rank-4, primeiro lote de GPT-2, consulta 15 de uma cabeça ficou vazia após máscara e clamp. Isso não é NaN e não foi escondido por denominador mínimo.

### Decisões

| Pergunta | Sugestão adotada ou pendente | Certeza | Executado |
|---|---|---|---|
| Como recuperar documentos reais? | Ler artigos do Arrow original do cache; selecionar universo comum de 602 elegíveis, congelar 256 e usar os primeiros 64 para matrizes. | alta | sim |
| Como salvar Qwen bf16 com probabilidade bem definida? | Capturar softmax fp32 anterior ao cast; gravar float16; manter o forward bf16 original exatamente igual. | alta | sim, conferido no eager nativo |
| Como acelerar o NNLS sem mudar o ajuste? | Reduzir o mesmo objetivo por QR, conferir contra NNLS denso e manter postos e cinco iterações. | alta | sim |
| Quais matrizes usar no custo? | Uma instância por cada um de 64 artigos, camadas balanceadas, trios idênticos em n=128/256/512, seed0; ordens denso/QR contrabalanceadas. | alta | sim, seleção declarada |
| Qual regra para linha vazia após reconstrução? | Sugestão: uniforme causal, sem parâmetros extras, contando ocorrências em todos os métodos. Alternativas: original ou braço inválido. | média | não; escolha do usuário pendente |
| Corrigir beta=0 da sonda antiga? | Há uma linha vazia em phase8 beta=0; não é vazamento do alvo. Preservar linha0 seria apropriado se esse escopo for autorizado. | alta sobre o achado | não; alterações nesses scripts estavam condicionadas a vazamento real, que não foi encontrado |

### Tempos registrados dos comandos

Tempos medidos dentro dos scripts, fora da fila do flock. Os registros por modelo acima distinguem os segmentos das chamadas agregadas. Tentativas iniciais que abortaram não tinham cronômetro de comando; nenhuma duração foi inventada.

| Comando/etapa registrada | Segundos |
|---|---:|
| OMP_NUM_THREADS=4 .venv/Scripts/python.exe -B sampling.py prepare (V2 corpus) | 42.537 |
| .venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction (V1 CPU checks) | 4.695 |
| .venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction (V1 CPU checks) | 7.133 |
| .venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction (V1 CPU checks) | 3.468 |
| .venv/Scripts/python.exe -B phase24_p0_metrics.py --legacy-mass --workers 1 (V2 metrics command complete) | 96.391 |
| .venv/Scripts/python.exe -B phase25_p0_checks.py --gpu-identity --out out/phase25_identity_checks_v2.json (V1 CPU checks) | 299.628 |
| .venv/Scripts/python.exe -B phase25_p0_checks.py --geometry --out out/phase25_geometry_checks_v2.json (V1 CPU checks) | 10.208 |
| .venv/Scripts/python.exe -B phase24_p0_metrics.py --workers 4 (V2 metrics command complete) | 2366.203 |
| .venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction --out out/phase25_completion_options_checks_v2.json (V1 CPU checks) | 9.586 |
| .venv/Scripts/python.exe -B phase24_p0_metrics.py --empty-row-diagnostic --workers 1 (V1 diagnostic command complete) | 130.694 |
| .venv/Scripts/python.exe -B phase25_p0_checks.py --capture-source --out out/phase25_native_source_checks_v2.json (V2 native source audit) | 42.920 |
| .venv/Scripts/python.exe -B phase15_interaction.py --workers 1 (V4 command complete) | 104.199 |
| .venv/Scripts/python.exe -B phase26_p0_named.py --workers 3 (V3 command complete) | 3058.972 |
| .venv/Scripts/python.exe -B phase17_efficiency.py (V5 command complete) | 154.784 |
| .venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction --out out/phase25_final_reconstruction_checks_v2.json (V1 CPU checks) | 7.114 |

Correção de rótulos de comandos antigos do formatador: as chamadas retrieval-audit e fractions-constancy foram registradas inicialmente como reconstruction; comandos verdadeiros e tempos constam na seção de correção acima. O comando GPU de identidade também teve o rótulo interno CPU no registro antigo, mas o comando contém --gpu-identity e foi executado sob flock.

### Arquivos criados/alterados: um por linha

Inventário com hashes: out/p0_delivery_pending_v2.json. O log de progresso é mutável e por isso não recebe hash. O próprio relatório de auditoria é listado abaixo, sem hash recursivo.

- `sampling.py`: artigos, manifesto, estratos, validação e utilitários imutáveis.
- `extract_attn.py`: captura original, arquivos NPZ, verificação e READY.
- `phase1_multimodel.py`: métricas multimodelo via arquivos congelados.
- `phase2_downstream.py`: último token, remáscara, processamento por lote, referências e regra vazia explícita.
- `phase3_robustness.py`: robustez de comprimento via arquivos congelados.
- `phase5_msclean.py`: norma, energia, termo cruzado e reduções de erro.
- `phase6_srpca.py`: mesmas cinco iterações, componentes e QR equivalente.
- `phase7_editability.py`: ANOVA, offset causal e preservação da primeira linha.
- `phase9_bigmodel.py`: replicação 3B via arquivos congelados.
- `phase15_interaction.py`: constância individual, distribuições e pares por sequência/cabeça.
- `phase17_efficiency.py`: custo de ajuste CPU pareado; análise.
- `phase24_p0_metrics.py`: métricas núcleo e diagnósticos da versão antiga.
- `phase25_p0_checks.py`: regressões, eager independente e auditoria final.
- `phase26_p0_named.py`: medições V3 completas e pares brutos.
- `data/attn/corpus_v2.manifest.json`: manifesto/proveniência.
- `data/attn/EleutherAI__pythia-1.4b_n128.manifest.json`: manifesto/proveniência.
- `data/attn/EleutherAI__pythia-1.4b_n128.npz`: matrizes float16.
- `data/attn/EleutherAI__pythia-1.4b_n256.manifest.json`: manifesto/proveniência.
- `data/attn/EleutherAI__pythia-1.4b_n256.npz`: matrizes float16.
- `data/attn/EleutherAI__pythia-410m_n128.manifest.json`: manifesto/proveniência.
- `data/attn/EleutherAI__pythia-410m_n128.npz`: matrizes float16.
- `data/attn/EleutherAI__pythia-410m_n256.manifest.json`: manifesto/proveniência.
- `data/attn/EleutherAI__pythia-410m_n256.npz`: matrizes float16.
- `data/attn/gpt2-medium_n128.manifest.json`: manifesto/proveniência.
- `data/attn/gpt2-medium_n128.npz`: matrizes float16.
- `data/attn/gpt2-medium_n256.manifest.json`: manifesto/proveniência.
- `data/attn/gpt2-medium_n256.npz`: matrizes float16.
- `data/attn/gpt2_n128.manifest.json`: manifesto/proveniência.
- `data/attn/gpt2_n128.npz`: matrizes float16.
- `data/attn/gpt2_n256.manifest.json`: manifesto/proveniência.
- `data/attn/gpt2_n256.npz`: matrizes float16.
- `data/attn/gpt2_n512.manifest.json`: manifesto/proveniência.
- `data/attn/gpt2_n512.npz`: matrizes float16.
- `data/attn/Qwen__Qwen2.5-0.5B_n128.manifest.json`: manifesto/proveniência.
- `data/attn/Qwen__Qwen2.5-0.5B_n128.npz`: matrizes float16.
- `data/attn/Qwen__Qwen2.5-0.5B_n256.manifest.json`: manifesto/proveniência.
- `data/attn/Qwen__Qwen2.5-0.5B_n256.npz`: matrizes float16.
- `data/attn/Qwen__Qwen2.5-3B_n128.manifest.json`: manifesto/proveniência.
- `data/attn/Qwen__Qwen2.5-3B_n128.npz`: matrizes float16.
- `data/attn/Qwen__Qwen2.5-3B_n256.manifest.json`: manifesto/proveniência.
- `data/attn/Qwen__Qwen2.5-3B_n256.npz`: matrizes float16.
- `data/attn/READY`: sinal de prontidão verificado.
- `out/p0_comparison_v2.json`: resultado, sanidade ou metadado versionado.
- `out/p0_environment_v2.json`: resultado, sanidade ou metadado versionado.
- `out/pairs/analysis_cost_v2.jsonl`: pares brutos.
- `out/pairs/constancy_EleutherAI__pythia-1.4b_n128_v2.jsonl`: pares brutos.
- `out/pairs/constancy_EleutherAI__pythia-1.4b_n256_v2.jsonl`: pares brutos.
- `out/pairs/constancy_EleutherAI__pythia-410m_n128_v2.jsonl`: pares brutos.
- `out/pairs/constancy_EleutherAI__pythia-410m_n256_v2.jsonl`: pares brutos.
- `out/pairs/constancy_gpt2-medium_n128_v2.jsonl`: pares brutos.
- `out/pairs/constancy_gpt2-medium_n256_v2.jsonl`: pares brutos.
- `out/pairs/constancy_gpt2_n128_v2.jsonl`: pares brutos.
- `out/pairs/constancy_gpt2_n256_v2.jsonl`: pares brutos.
- `out/pairs/constancy_Qwen__Qwen2.5-0.5B_n128_v2.jsonl`: pares brutos.
- `out/pairs/constancy_Qwen__Qwen2.5-0.5B_n256_v2.jsonl`: pares brutos.
- `out/pairs/constancy_Qwen__Qwen2.5-3B_n128_v2.jsonl`: pares brutos.
- `out/pairs/constancy_Qwen__Qwen2.5-3B_n256_v2.jsonl`: pares brutos.
- `out/pairs/core_EleutherAI__pythia-1.4b_n128_v2.jsonl`: pares brutos.
- `out/pairs/core_EleutherAI__pythia-1.4b_n256_v2.jsonl`: pares brutos.
- `out/pairs/core_EleutherAI__pythia-410m_n128_v2.jsonl`: pares brutos.
- `out/pairs/core_EleutherAI__pythia-410m_n256_v2.jsonl`: pares brutos.
- `out/pairs/core_gpt2-medium_n128_v2.jsonl`: pares brutos.
- `out/pairs/core_gpt2-medium_n256_v2.jsonl`: pares brutos.
- `out/pairs/core_gpt2_n128_v2.jsonl`: pares brutos.
- `out/pairs/core_gpt2_n256_v2.jsonl`: pares brutos.
- `out/pairs/core_Qwen__Qwen2.5-0.5B_n128_v2.jsonl`: pares brutos.
- `out/pairs/core_Qwen__Qwen2.5-0.5B_n256_v2.jsonl`: pares brutos.
- `out/pairs/core_Qwen__Qwen2.5-3B_n128_v2.jsonl`: pares brutos.
- `out/pairs/core_Qwen__Qwen2.5-3B_n256_v2.jsonl`: pares brutos.
- `out/pairs/downstream_gpt2_v2.jsonl`: seis registros preservados da tentativa interrompida; V1 incompleto.
- `out/pairs/empty_rows_EleutherAI__pythia-1.4b_v2.jsonl`: pares brutos.
- `out/pairs/empty_rows_EleutherAI__pythia-410m_v2.jsonl`: pares brutos.
- `out/pairs/empty_rows_gpt2-medium_v2.jsonl`: pares brutos.
- `out/pairs/empty_rows_gpt2_v2.jsonl`: pares brutos.
- `out/pairs/empty_rows_Qwen__Qwen2.5-0.5B_v2.jsonl`: pares brutos.
- `out/pairs/empty_rows_Qwen__Qwen2.5-3B_v2.jsonl`: pares brutos.
- `out/pairs/legacy_mass_EleutherAI__pythia-1.4b_v2.jsonl`: pares brutos.
- `out/pairs/legacy_mass_EleutherAI__pythia-410m_v2.jsonl`: pares brutos.
- `out/pairs/legacy_mass_gpt2-medium_v2.jsonl`: pares brutos.
- `out/pairs/legacy_mass_gpt2_v2.jsonl`: pares brutos.
- `out/pairs/legacy_mass_Qwen__Qwen2.5-0.5B_v2.jsonl`: pares brutos.
- `out/pairs/legacy_mass_Qwen__Qwen2.5-3B_v2.jsonl`: pares brutos.
- `out/pairs/named_EleutherAI__pythia-1.4b_n128_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_EleutherAI__pythia-1.4b_n256_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_EleutherAI__pythia-410m_n128_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_EleutherAI__pythia-410m_n256_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_gpt2-medium_n128_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_gpt2-medium_n256_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_gpt2_n128_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_gpt2_n256_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_Qwen__Qwen2.5-0.5B_n128_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_Qwen__Qwen2.5-0.5B_n256_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_Qwen__Qwen2.5-3B_n128_msclean_srpca_v2.jsonl`: pares brutos.
- `out/pairs/named_Qwen__Qwen2.5-3B_n256_msclean_srpca_v2.jsonl`: pares brutos.
- `out/phase15_EleutherAI__pythia-1.4b_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_EleutherAI__pythia-1.4b_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_EleutherAI__pythia-410m_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_EleutherAI__pythia-410m_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_gpt2-medium_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_gpt2-medium_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_gpt2_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_gpt2_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_interaction_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_Qwen__Qwen2.5-0.5B_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_Qwen__Qwen2.5-0.5B_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_Qwen__Qwen2.5-3B_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase15_Qwen__Qwen2.5-3B_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase17_efficiency_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase1_multimodel_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_EleutherAI__pythia-1.4b_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_EleutherAI__pythia-1.4b_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_EleutherAI__pythia-410m_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_EleutherAI__pythia-410m_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_gpt2-medium_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_gpt2-medium_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_gpt2_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_gpt2_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_Qwen__Qwen2.5-0.5B_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_Qwen__Qwen2.5-0.5B_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_Qwen__Qwen2.5-3B_n128_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase24_core_Qwen__Qwen2.5-3B_n256_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_completion_options_checks_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_final_reconstruction_checks_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_fraction_constancy_checks_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_geometry_checks_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_identity_checks_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_identity_EleutherAI__pythia-1.4b_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_identity_EleutherAI__pythia-410m_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_identity_gpt2-medium_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_identity_gpt2_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_identity_Qwen__Qwen2.5-0.5B_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_identity_Qwen__Qwen2.5-3B_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_native_source_checks_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_reconstruction_checks_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_retrieval_audit_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_sampling_checks_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase25_sampling_regressions_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_EleutherAI__pythia-1.4b_n128_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_EleutherAI__pythia-1.4b_n256_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_EleutherAI__pythia-410m_n128_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_EleutherAI__pythia-410m_n256_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_gpt2-medium_n128_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_gpt2-medium_n256_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_gpt2_n128_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_gpt2_n256_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_Qwen__Qwen2.5-0.5B_n128_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_Qwen__Qwen2.5-0.5B_n256_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_Qwen__Qwen2.5-3B_n128_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase26_named_Qwen__Qwen2.5-3B_n256_msclean_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_empty_rows_EleutherAI__pythia-1.4b_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_empty_rows_EleutherAI__pythia-410m_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_empty_rows_gpt2-medium_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_empty_rows_gpt2_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_empty_rows_Qwen__Qwen2.5-0.5B_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_empty_rows_Qwen__Qwen2.5-3B_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_empty_rows_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_legacy_mass_EleutherAI__pythia-1.4b_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_legacy_mass_EleutherAI__pythia-410m_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_legacy_mass_gpt2-medium_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_legacy_mass_gpt2_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_legacy_mass_Qwen__Qwen2.5-0.5B_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_legacy_mass_Qwen__Qwen2.5-3B_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase2_legacy_mass_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase3_robustness_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase5_msclean_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase6_srpca_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase9_bigmodel_named_v2.json`: resultado, sanidade ou metadado versionado.
- `out/phase9_bigmodel_v2.json`: resultado, sanidade ou metadado versionado.
- `out/_rerun_logs/p0_progress.md`: arquivo de progresso.
- `out/p0_delivery_pending_v2.json`: auditoria e inventário; completo=false somente pela pendência de V1.

FALTA: escolher a regra de V1 para linhas vazias. Os JSONs finais out/phase2_downstream_v2.json e out/phase7_editability_v2.json não foram produzidos. As contagens antigas de documentos e os tempos de comando das primeiras tentativas abortadas não estavam registrados.

- 2026-11-09T21:06:53+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=5.968 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction --out out/phase25_uniform_reconstruction_checks_v2.json`

- 2026-11-09T21:09:39+00:00 | V1 queue/start: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2 --batch 2

- 2026-11-09T21:15:49+00:00 | V1 beta0 probes: Five immutable probes; 3200 trials each; historical shared RNG order, no sample cut | elapsed_seconds=13.984 | command: `.venv/Scripts/python.exe -B phase28_beta0_retest.py --prepare-only`

- 2026-11-09T21:16:41+00:00 | V1 sink regression: Positive beta bit equality, beta0 no-alternative rows, cached offsets, tiny mass, uniform completion and inheritance passed | elapsed_seconds=0.337 | command: `.venv/Scripts/python.exe -B phase29_sink_checks.py`

- 2026-11-09T21:17:08+00:00 | V1 retrieval audit: All regression checks passed | elapsed_seconds=9.468 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --retrieval --out out/phase25_retrieval_fixed_v2.json`

- Continuação autorizada pelo usuário: conclusão uniforme causal em todas as reconstruções; contadores por modelo/modo/rank e última consulta. Edição do sink preserva a distribuição pré-edição somente em linhas sem alternativa; massa positiva minúscula é normalizada pelo total real, sem piso 1e-9. Correção compartilhada phase8/10/14, herdada por 11/16/18. Protocolo beta0: cinco modelos históricos, seed=0, 400 x 8 posições, baseline beta1 + beta0 corrigido + beta0 legado diagnóstico. Nenhum outro beta é reavaliado em grade.

- 2026-11-09T21:22:54+00:00 | V1 positive beta pretrained regression: GPT-2, beta=.25, two frozen probes, CPU; native identity and old/new positive-beta logits bit equal | elapsed_seconds=4.504 | command: `.venv/Scripts/python.exe -B phase28_beta0_retest.py --cpu-regression-only`

- 2026-11-09T22:04:48+00:00 | V1 CPU checks: All regression checks passed | elapsed_seconds=14.535 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --reconstruction --out out/phase25_exact_driver_api_checks_v2.json`

- 2026-11-09T22:21:25+00:00 | V1 downstream dependency audit: phase18 includes beta0; Pythia-1.4b selected beta0 on family B in all three saved seeds. Saved CV numbers were not recomputed, per explicit rerun scope. Evidence in out/phase18_beta0_dependency_audit_v2.json.

- 2026-11-09T22:24:15+00:00 | V1 queued remaining model; flock_pid=77763: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2-medium --batch 2

- 2026-11-09T22:24:15+00:00 | V1 queued remaining model; flock_pid=77764: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-410m --batch 2

- 2026-11-09T22:24:15+00:00 | V1 queued remaining model; flock_pid=77765: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-1.4b --batch 2

- 2026-11-09T22:24:15+00:00 | V1 queued remaining model; flock_pid=77766: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models Qwen/Qwen2.5-0.5B --batch 2

- 2026-11-09T22:24:15+00:00 | V1 queued remaining model; flock_pid=77767: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models Qwen/Qwen2.5-3B --batch 2

- 2026-11-09T22:25:35+00:00 | Engineering: replaced own waiting-only beta0 coordinator PID 3701 (no children, no numerical evaluation started) to queue the five future locked jobs together. No model/GPU process was terminated.

- 2026-11-09T22:30:47+00:00 | V1 downstream: gpt2; 256 independent articles; 15 arms; identity/suffix/attention checks passed | elapsed_seconds=2110.512 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2`

- 2026-11-09T22:30:47+00:00 | V1 command complete: 1 models, suites=('phase2', 'phase7') | elapsed_seconds=2110.546 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2 --batch 2`

- 2026-11-09T22:30:51+00:00 | V1 command wall including queue: elapsed_seconds=4694.311 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2 --batch 2`

- 2026-11-09T22:30:51+00:00 | V1 queue/start: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2-medium --batch 2

- 2026-11-09T22:54:50+00:00 | P0 atomic publication: Windows filesystem: complete publication, exclusive creation and temporary cleanup passed | elapsed_seconds=0.017 | command: `.venv/Scripts/python.exe -B - (atomic-publication check)`

- 2026-11-09T23:07:10+00:00 | Engineering decision: retained original torch default SVD in all models. Alternative-driver benchmark/switch was withdrawn before any GPU execution: optimal-error equality does not fix truncated subspaces at singular-value ties. Certainty medium; no scientific result or tolerance changed. Evidence out/phase2_driver_decision_v2.json.

- 2026-11-09T23:22:41+00:00 | V1 batched validation regression: All checks and counters retained; bit-identical reconstructed tensors and pretrained logits; invalid inputs and original tolerance boundaries rejected | elapsed_seconds=53.285 | command: `.venv/Scripts/python.exe -B phase33_validation_schedule.py`

- 2026-11-09T23:24:25+00:00 | V1 legacy counter schedule: 12 dtype/shape/beta cases; identical diagnostic outputs and exact counters | elapsed_seconds=0.019 | command: `.venv/Scripts/python.exe -B - (legacy-counter regression)`

- 2026-11-09T23:27:15+00:00 | V1 retrieval audit: All regression checks passed | elapsed_seconds=7.048 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --retrieval-audit --out out/phase25_retrieval_final_v2.json`

- 2026-11-09T23:41:55+00:00 | V1 fixed-shape validation: Same forbidden-region counts incl NaN/offsets; batched flags match per-document flags including ties | elapsed_seconds=0.005 | command: `.venv/Scripts/python.exe -B - (fixed-shape/flag regression)`

- 2026-11-09T23:41:56+00:00 | V1 retrieval audit: All regression checks passed | elapsed_seconds=6.201 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --retrieval-audit --out out/phase25_retrieval_completion_v2.json`

Loading weights:   0%|          | 0/292 [00:00<?, ?it/s]
Loading weights: 100%|##########| 292/292 [00:00<00:00, 5005.55it/s]
ARM start=0: phase2:identity
ARM start=0: phase2:svd:1
ARM start=0: phase2:svd:2
ARM start=0: phase2:svd:4
ARM start=0: phase2:svd:8
ARM start=0: phase2:svd:16
ARM start=0: phase2:svd:32
ARM start=0: phase2:geom
ARM start=0: phase2:uniform
ARM start=0: phase2:diagonal
ARM start=0: phase2:sink
ARM start=0: phase7:identity:8
ARM start=0: phase7:anova:8
ARM start=0: phase7:nosink:8
ARM start=0: phase7:zerocol_mid:8

- 2026-11-10T00:09:59+00:00 | V1 GPU validation equivalence completed: gpt2-medium, actual float32 CUDA, first batch 2 documents, all 15 arms; logits bit-equal and all common counters exact. Scientific ledger is created only after this required proof passes.
DOWNSTREAM gpt2-medium: 16/256 documents, elapsed=355.0s
DOWNSTREAM gpt2-medium: 32/256 documents, elapsed=610.2s
DOWNSTREAM gpt2-medium: 48/256 documents, elapsed=855.8s
DOWNSTREAM gpt2-medium: 64/256 documents, elapsed=1104.0s
DOWNSTREAM gpt2-medium: 80/256 documents, elapsed=1355.8s
DOWNSTREAM gpt2-medium: 96/256 documents, elapsed=1619.6s
DOWNSTREAM gpt2-medium: 112/256 documents, elapsed=1912.7s
DOWNSTREAM gpt2-medium: 128/256 documents, elapsed=2169.0s
DOWNSTREAM gpt2-medium: 144/256 documents, elapsed=2429.7s
DOWNSTREAM gpt2-medium: 160/256 documents, elapsed=2683.8s
DOWNSTREAM gpt2-medium: 176/256 documents, elapsed=2982.5s
DOWNSTREAM gpt2-medium: 192/256 documents, elapsed=3263.1s
DOWNSTREAM gpt2-medium: 208/256 documents, elapsed=3561.5s
DOWNSTREAM gpt2-medium: 224/256 documents, elapsed=3833.6s
DOWNSTREAM gpt2-medium: 240/256 documents, elapsed=4123.3s
DOWNSTREAM gpt2-medium: 256/256 documents, elapsed=4392.8s

- 2026-11-10T01:19:17+00:00 | V1 downstream: gpt2-medium; 256 independent articles; 15 arms; identity/suffix/attention checks passed | elapsed_seconds=4394.466 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2-medium`

- 2026-11-10T01:19:17+00:00 | V1 command complete: 1 models, suites=('phase2', 'phase7') | elapsed_seconds=4394.494 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2-medium --batch 2`

- 2026-11-10T01:19:24+00:00 | V1 queued model exit=0; gpt2-medium; command wall including queue: elapsed_seconds=10010.564 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2-medium --batch 2`

Loading weights:   0%|          | 0/292 [00:00<?, ?it/s]
Loading weights:   0%|          | 1/292 [00:00<00:59,  4.90it/s]
Loading weights:  37%|###6      | 108/292 [00:00<00:00, 422.76it/s]
Loading weights:  64%|######3   | 186/292 [00:00<00:00, 537.21it/s]
Loading weights:  86%|########6 | 252/292 [00:00<00:00, 549.81it/s]
Loading weights: 100%|##########| 292/292 [00:00<00:00, 489.14it/s]

- 2026-11-10T01:22:37+00:00 | V1 independent-head scheduling: EleutherAI/pythia-410m; selected_parallel=False; exact=True; sequential=36.537s, parallel=33.456s; all 15 arms retained
ARM start=0: phase2:identity
ARM start=0: phase2:svd:1
ARM start=0: phase2:svd:2
ARM start=0: phase2:svd:4
ARM start=0: phase2:svd:8
ARM start=0: phase2:svd:16
ARM start=0: phase2:svd:32
ARM start=0: phase2:geom
ARM start=0: phase2:uniform
ARM start=0: phase2:diagonal
ARM start=0: phase2:sink
ARM start=0: phase7:identity:8
ARM start=0: phase7:anova:8
ARM start=0: phase7:nosink:8
ARM start=0: phase7:zerocol_mid:8
DOWNSTREAM EleutherAI/pythia-410m: 16/256 documents, elapsed=453.0s
DOWNSTREAM EleutherAI/pythia-410m: 32/256 documents, elapsed=718.1s
DOWNSTREAM EleutherAI/pythia-410m: 48/256 documents, elapsed=994.8s
DOWNSTREAM EleutherAI/pythia-410m: 64/256 documents, elapsed=1270.3s
DOWNSTREAM EleutherAI/pythia-410m: 80/256 documents, elapsed=1557.0s
DOWNSTREAM EleutherAI/pythia-410m: 96/256 documents, elapsed=1892.4s
DOWNSTREAM EleutherAI/pythia-410m: 112/256 documents, elapsed=2218.2s
DOWNSTREAM EleutherAI/pythia-410m: 128/256 documents, elapsed=2539.8s
DOWNSTREAM EleutherAI/pythia-410m: 144/256 documents, elapsed=2846.4s
DOWNSTREAM EleutherAI/pythia-410m: 160/256 documents, elapsed=3141.7s
DOWNSTREAM EleutherAI/pythia-410m: 176/256 documents, elapsed=3467.7s
DOWNSTREAM EleutherAI/pythia-410m: 192/256 documents, elapsed=3784.5s
DOWNSTREAM EleutherAI/pythia-410m: 208/256 documents, elapsed=4078.8s
DOWNSTREAM EleutherAI/pythia-410m: 224/256 documents, elapsed=4396.9s
DOWNSTREAM EleutherAI/pythia-410m: 240/256 documents, elapsed=4700.4s
DOWNSTREAM EleutherAI/pythia-410m: 256/256 documents, elapsed=4996.9s

- 2026-11-10T02:42:48+00:00 | V1 downstream: EleutherAI/pythia-410m; 256 independent articles; 15 arms; identity/suffix/attention checks passed | elapsed_seconds=4997.960 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-410m`

- 2026-11-10T02:42:48+00:00 | V1 command complete: 1 models, suites=('phase2', 'phase7') | elapsed_seconds=4997.982 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-410m --batch 2`

- 2026-11-10T02:42:57+00:00 | V1 queued model exit=0; EleutherAI/pythia-410m; command wall including queue: elapsed_seconds=14730.907 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-410m --batch 2`

Loading weights:   0%|          | 0/292 [00:00<?, ?it/s]
Loading weights:   0%|          | 1/292 [00:00<02:02,  2.38it/s]
Loading weights:  19%|#9        | 56/292 [00:00<00:01, 135.59it/s]
Loading weights:  29%|##8       | 84/292 [00:00<00:01, 140.67it/s]
Loading weights:  36%|###6      | 106/292 [00:00<00:01, 156.31it/s]
Loading weights:  44%|####3     | 128/292 [00:00<00:01, 161.24it/s]
Loading weights:  51%|#####     | 148/292 [00:01<00:00, 151.17it/s]
Loading weights:  58%|#####8    | 170/292 [00:01<00:00, 157.40it/s]
Loading weights:  66%|######5   | 192/292 [00:01<00:00, 153.87it/s]
Loading weights:  74%|#######3  | 216/292 [00:01<00:00, 159.51it/s]
Loading weights:  81%|########  | 236/292 [00:01<00:00, 167.56it/s]
Loading weights:  87%|########6 | 254/292 [00:01<00:00, 156.05it/s]
Loading weights:  93%|#########2| 271/292 [00:01<00:00, 156.25it/s]
Loading weights:  99%|#########8| 288/292 [00:01<00:00, 153.91it/s]
Loading weights: 100%|##########| 292/292 [00:01<00:00, 146.01it/s]

- 2026-11-10T02:46:11+00:00 | V1 independent-head scheduling: EleutherAI/pythia-1.4b; selected_parallel=True; exact=True; sequential=39.380s, parallel=33.749s; all 15 arms retained
ARM start=0: phase2:identity
ARM start=0: phase2:svd:1
ARM start=0: phase2:svd:2
ARM start=0: phase2:svd:4
ARM start=0: phase2:svd:8
ARM start=0: phase2:svd:16
ARM start=0: phase2:svd:32
ARM start=0: phase2:geom
ARM start=0: phase2:uniform
ARM start=0: phase2:diagonal
ARM start=0: phase2:sink
ARM start=0: phase7:identity:8
ARM start=0: phase7:anova:8
ARM start=0: phase7:nosink:8
ARM start=0: phase7:zerocol_mid:8
DOWNSTREAM EleutherAI/pythia-1.4b: 16/256 documents, elapsed=456.0s
DOWNSTREAM EleutherAI/pythia-1.4b: 32/256 documents, elapsed=717.3s
DOWNSTREAM EleutherAI/pythia-1.4b: 48/256 documents, elapsed=978.9s
DOWNSTREAM EleutherAI/pythia-1.4b: 64/256 documents, elapsed=1257.4s
C:\Users\filip\radon-attention\phase34_parallel_svd.py:20: UserWarning: torch.linalg.svd: During SVD computation with the selected cusolver driver, batches 7 failed to converge. A more accurate method will be used to compute the SVD as a fallback. Check doc at https://pytorch.org/docs/stable/generated/torch.linalg.svd.html (Triggered internally at C:\actions-runner\_work\pytorch\pytorch\pytorch\aten\src\ATen\native\cuda\linalg\BatchLinearAlgebraLib.cpp:696.)
  return torch.linalg.svd(part,full_matrices=False,driver=driver)
DOWNSTREAM EleutherAI/pythia-1.4b: 80/256 documents, elapsed=1518.1s
DOWNSTREAM EleutherAI/pythia-1.4b: 96/256 documents, elapsed=1771.6s
DOWNSTREAM EleutherAI/pythia-1.4b: 112/256 documents, elapsed=2036.3s
DOWNSTREAM EleutherAI/pythia-1.4b: 128/256 documents, elapsed=2285.3s
DOWNSTREAM EleutherAI/pythia-1.4b: 144/256 documents, elapsed=2542.4s
DOWNSTREAM EleutherAI/pythia-1.4b: 160/256 documents, elapsed=2792.8s
DOWNSTREAM EleutherAI/pythia-1.4b: 176/256 documents, elapsed=3040.1s
DOWNSTREAM EleutherAI/pythia-1.4b: 192/256 documents, elapsed=3285.2s
DOWNSTREAM EleutherAI/pythia-1.4b: 208/256 documents, elapsed=3529.9s
DOWNSTREAM EleutherAI/pythia-1.4b: 224/256 documents, elapsed=3788.3s
DOWNSTREAM EleutherAI/pythia-1.4b: 240/256 documents, elapsed=4042.6s
DOWNSTREAM EleutherAI/pythia-1.4b: 256/256 documents, elapsed=4295.1s

- 2026-11-10T03:54:37+00:00 | V1 downstream: EleutherAI/pythia-1.4b; 256 independent articles; 15 arms; identity/suffix/attention checks passed | elapsed_seconds=4296.285 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-1.4b`

- 2026-11-10T03:54:37+00:00 | V1 command complete: 1 models, suites=('phase2', 'phase7') | elapsed_seconds=4296.317 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-1.4b --batch 2`

- 2026-11-10T03:54:42+00:00 | V1 queued model exit=0; EleutherAI/pythia-1.4b; command wall including queue: elapsed_seconds=18761.099 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-1.4b --batch 2`

Loading weights:   0%|          | 0/290 [00:00<?, ?it/s]
Loading weights: 100%|##########| 290/290 [00:00<00:00, 3444.15it/s]

- 2026-11-10T03:57:40+00:00 | V1 independent-head scheduling: Qwen/Qwen2.5-0.5B; selected_parallel=True; exact=True; sequential=30.948s, parallel=26.536s; all 15 arms retained
ARM start=0: phase2:identity
ARM start=0: phase2:svd:1
ARM start=0: phase2:svd:2
ARM start=0: phase2:svd:4
ARM start=0: phase2:svd:8
ARM start=0: phase2:svd:16
ARM start=0: phase2:svd:32
ARM start=0: phase2:geom
ARM start=0: phase2:uniform
ARM start=0: phase2:diagonal
ARM start=0: phase2:sink
ARM start=0: phase7:identity:8
ARM start=0: phase7:anova:8
ARM start=0: phase7:nosink:8
ARM start=0: phase7:zerocol_mid:8
DOWNSTREAM Qwen/Qwen2.5-0.5B: 16/256 documents, elapsed=382.1s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 32/256 documents, elapsed=585.9s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 48/256 documents, elapsed=794.1s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 64/256 documents, elapsed=1002.3s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 80/256 documents, elapsed=1205.7s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 96/256 documents, elapsed=1403.8s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 112/256 documents, elapsed=1595.1s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 128/256 documents, elapsed=1784.8s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 144/256 documents, elapsed=1970.3s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 160/256 documents, elapsed=2140.9s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 176/256 documents, elapsed=2313.0s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 192/256 documents, elapsed=2503.4s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 208/256 documents, elapsed=2708.3s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 224/256 documents, elapsed=2896.2s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 240/256 documents, elapsed=3083.5s
DOWNSTREAM Qwen/Qwen2.5-0.5B: 256/256 documents, elapsed=3269.5s

- 2026-11-10T04:49:21+00:00 | V1 downstream: Qwen/Qwen2.5-0.5B; 256 independent articles; 15 arms; identity/suffix/attention checks passed | elapsed_seconds=3270.292 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models Qwen/Qwen2.5-0.5B`

- 2026-11-10T04:49:21+00:00 | V1 command complete: 1 models, suites=('phase2', 'phase7') | elapsed_seconds=3270.313 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models Qwen/Qwen2.5-0.5B --batch 2`

- 2026-11-10T04:49:23+00:00 | V1 queued model exit=0; Qwen/Qwen2.5-0.5B; command wall including queue: elapsed_seconds=21821.179 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models Qwen/Qwen2.5-0.5B --batch 2`

Loading weights:   0%|          | 0/434 [00:00<?, ?it/s]
Loading weights:  38%|###8      | 166/434 [00:00<00:00, 1655.68it/s]
Loading weights: 100%|##########| 434/434 [00:00<00:00, 3133.53it/s]

- 2026-11-10T04:53:27+00:00 | V1 independent-head scheduling: Qwen/Qwen2.5-3B; selected_parallel=True; exact=True; sequential=43.200s, parallel=35.754s; all 15 arms retained
ARM start=0: phase2:identity
ARM start=0: phase2:svd:1
ARM start=0: phase2:svd:2
ARM start=0: phase2:svd:4
ARM start=0: phase2:svd:8
ARM start=0: phase2:svd:16
ARM start=0: phase2:svd:32
ARM start=0: phase2:geom
ARM start=0: phase2:uniform
ARM start=0: phase2:diagonal
ARM start=0: phase2:sink
ARM start=0: phase7:identity:8
ARM start=0: phase7:anova:8
ARM start=0: phase7:nosink:8
ARM start=0: phase7:zerocol_mid:8
DOWNSTREAM Qwen/Qwen2.5-3B: 16/256 documents, elapsed=508.0s
DOWNSTREAM Qwen/Qwen2.5-3B: 32/256 documents, elapsed=848.1s
DOWNSTREAM Qwen/Qwen2.5-3B: 48/256 documents, elapsed=1188.4s
DOWNSTREAM Qwen/Qwen2.5-3B: 64/256 documents, elapsed=1526.5s
DOWNSTREAM Qwen/Qwen2.5-3B: 80/256 documents, elapsed=1852.5s
DOWNSTREAM Qwen/Qwen2.5-3B: 96/256 documents, elapsed=2186.8s

- 2026-11-10T05:26:08+00:00 | Historical beta0 scope verified read-only: phase8_lostmiddle_s0.json contains beta={1,.5,.25,0}; s1/s2 contain only {1,.25}. Thus the planned full 400 x 8-position seed0 repeat covers every historical beta0 probe; no beta0 seed has been dropped. Three-seed pooled positive-beta results are distinct. Historical raw trial IDs remain unavailable.
DOWNSTREAM Qwen/Qwen2.5-3B: 112/256 documents, elapsed=2522.5s
DOWNSTREAM Qwen/Qwen2.5-3B: 128/256 documents, elapsed=2849.1s
DOWNSTREAM Qwen/Qwen2.5-3B: 144/256 documents, elapsed=3125.0s
DOWNSTREAM Qwen/Qwen2.5-3B: 160/256 documents, elapsed=3393.8s
DOWNSTREAM Qwen/Qwen2.5-3B: 176/256 documents, elapsed=3665.5s
DOWNSTREAM Qwen/Qwen2.5-3B: 192/256 documents, elapsed=3938.2s
DOWNSTREAM Qwen/Qwen2.5-3B: 208/256 documents, elapsed=4204.6s
DOWNSTREAM Qwen/Qwen2.5-3B: 224/256 documents, elapsed=4479.1s
DOWNSTREAM Qwen/Qwen2.5-3B: 240/256 documents, elapsed=4754.6s
DOWNSTREAM Qwen/Qwen2.5-3B: 256/256 documents, elapsed=5023.9s

- 2026-11-10T06:13:16+00:00 | V1 downstream: Qwen/Qwen2.5-3B; 256 independent articles; 15 arms; identity/suffix/attention checks passed | elapsed_seconds=5024.532 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models Qwen/Qwen2.5-3B`

- 2026-11-10T06:13:16+00:00 | V1 command complete: 1 models, suites=('phase2', 'phase7') | elapsed_seconds=5024.550 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models Qwen/Qwen2.5-3B --batch 2`

- 2026-11-10T06:13:22+00:00 | V1 queued model exit=0; Qwen/Qwen2.5-3B; command wall including queue: elapsed_seconds=26501.260 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models Qwen/Qwen2.5-3B --batch 2`

- 2026-11-10T06:13:24+00:00 | V1 command complete: 1 models, suites=('phase2', 'phase7') | elapsed_seconds=0.001 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2-medium --batch 2`

- 2026-11-10T06:13:24+00:00 | V1 command wall including queue: elapsed_seconds=26124.024 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models gpt2-medium --batch 2`

- 2026-11-10T06:13:24+00:00 | V1 queue/start: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models EleutherAI/pythia-410m --batch 2

- 2026-11-10T06:13:30+00:00 | V1 command complete: 6 models, suites=('phase2', 'phase7') | elapsed_seconds=0.028 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --aggregate-only`

- 2026-11-10T06:13:32+00:00 | V1 all-six aggregates published after the locked queue: elapsed_seconds=6.892 | command: `.venv/Scripts/python.exe -B phase2_downstream.py --aggregate-only`

- 2026-11-10T06:13:35+00:00 | Beta0 queued; flock_pid=54573: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models gpt2 --batch 16

- 2026-11-10T06:13:35+00:00 | Beta0 queued; flock_pid=54574: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models gpt2-medium --batch 16

- 2026-11-10T06:13:35+00:00 | Beta0 queued; flock_pid=54575: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models EleutherAI/pythia-410m --batch 16

- 2026-11-10T06:13:35+00:00 | Beta0 queued; flock_pid=54576: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models EleutherAI/pythia-1.4b --batch 16

- 2026-11-10T06:13:35+00:00 | Beta0 queued; flock_pid=54581: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models Qwen/Qwen2.5-0.5B --batch 16

- 2026-11-10T06:14:34+00:00 | Removed only own redundant cached-only coordinator PID 89914 and its verified waiting flock child PID 54404 (no children). Both global V1 aggregates already contain all six completed models with 256 documents. No GPU/model computation was terminated; no sample or output was removed. Beta0 supervisor continues independently. | elapsed_seconds=0.010

- 2026-11-10T06:17:02+00:00 | V1 raw validity audit: All V1 raw records reconciled; beta0 and full-delivery audit remain pending | elapsed_seconds=1.127 | command: `.venv/Scripts/python.exe -B phase30_validity_audit.py --v1-only`

- 2026-11-10T06:25:27+00:00 | V1 document intervals: 90 arms, 256 identical documents each; median and secondary mean KL intervals; one shared seed0 block bootstrap, no filtering | elapsed_seconds=1.814 | command: `.venv/Scripts/python.exe -B phase35_downstream_intervals.py`

- 2026-11-10T06:34:25+00:00 | Logging clarification: phase32 invoked the completed V1 aggregate with `.venv/Scripts/python.exe -B phase2_downstream.py --aggregate-only` (CPU, wall 6.892s). The inner phase2 progress formatter prefixes flock unconditionally even for this cached-only operation; the coordinator records the actual command. All numerical GPU invocations were under the shared flock. The legacy_upper_diagonal_mass field in both V1 aggregates references the old phase2 SVD/clamp/normalize formula on frozen V2 matrices; it does not claim old phase7 lacked a square causal mask.

Loading weights:   0%|          | 0/148 [00:00<?, ?it/s]
Loading weights: 100%|##########| 148/148 [00:00<00:00, 5764.19it/s]
BETA0 gpt2 baseline_beta1: 400/3200, elapsed=4.2s
BETA0 gpt2 baseline_beta1: 800/3200, elapsed=6.6s
BETA0 gpt2 baseline_beta1: 1200/3200, elapsed=9.0s
BETA0 gpt2 baseline_beta1: 1600/3200, elapsed=11.3s
BETA0 gpt2 baseline_beta1: 2000/3200, elapsed=13.7s
BETA0 gpt2 baseline_beta1: 2400/3200, elapsed=16.1s
BETA0 gpt2 baseline_beta1: 2800/3200, elapsed=18.5s
BETA0 gpt2 baseline_beta1: 3200/3200, elapsed=20.9s
BETA0 gpt2 corrected_beta0: 400/3200, elapsed=23.5s
BETA0 gpt2 corrected_beta0: 800/3200, elapsed=26.2s
BETA0 gpt2 corrected_beta0: 1200/3200, elapsed=28.9s
BETA0 gpt2 corrected_beta0: 1600/3200, elapsed=31.6s
BETA0 gpt2 corrected_beta0: 2000/3200, elapsed=34.3s
BETA0 gpt2 corrected_beta0: 2400/3200, elapsed=37.0s
BETA0 gpt2 corrected_beta0: 2800/3200, elapsed=39.7s
BETA0 gpt2 corrected_beta0: 3200/3200, elapsed=42.4s
BETA0 gpt2 legacy_beta0_diagnostic: 400/3200, elapsed=44.7s
BETA0 gpt2 legacy_beta0_diagnostic: 800/3200, elapsed=46.9s
BETA0 gpt2 legacy_beta0_diagnostic: 1200/3200, elapsed=49.1s
BETA0 gpt2 legacy_beta0_diagnostic: 1600/3200, elapsed=51.3s
BETA0 gpt2 legacy_beta0_diagnostic: 2000/3200, elapsed=53.6s
BETA0 gpt2 legacy_beta0_diagnostic: 2400/3200, elapsed=55.8s
BETA0 gpt2 legacy_beta0_diagnostic: 2800/3200, elapsed=58.0s
BETA0 gpt2 legacy_beta0_diagnostic: 3200/3200, elapsed=60.3s

- 2026-11-10T08:00:20+00:00 | V1 beta0 model: gpt2; 3200 matched trials x 3 arms; no trial dropped; checks passed | elapsed_seconds=60.447 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models gpt2 --batch 16`

- 2026-11-10T08:00:25+00:00 | Beta0 queued model exit=0; gpt2; command wall including queue: elapsed_seconds=5910.098 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models gpt2 --batch 16`

Loading weights:   0%|          | 0/292 [00:00<?, ?it/s]
Loading weights: 100%|##########| 292/292 [00:00<00:00, 6080.75it/s]
BETA0 gpt2-medium baseline_beta1: 400/3200, elapsed=9.5s
BETA0 gpt2-medium baseline_beta1: 800/3200, elapsed=16.4s
BETA0 gpt2-medium baseline_beta1: 1200/3200, elapsed=23.4s
BETA0 gpt2-medium baseline_beta1: 1600/3200, elapsed=30.3s
BETA0 gpt2-medium baseline_beta1: 2000/3200, elapsed=37.3s
BETA0 gpt2-medium baseline_beta1: 2400/3200, elapsed=44.3s
BETA0 gpt2-medium baseline_beta1: 2800/3200, elapsed=51.2s
BETA0 gpt2-medium baseline_beta1: 3200/3200, elapsed=58.2s
BETA0 gpt2-medium corrected_beta0: 400/3200, elapsed=65.9s
BETA0 gpt2-medium corrected_beta0: 800/3200, elapsed=73.6s
BETA0 gpt2-medium corrected_beta0: 1200/3200, elapsed=81.4s
BETA0 gpt2-medium corrected_beta0: 1600/3200, elapsed=89.1s
BETA0 gpt2-medium corrected_beta0: 2000/3200, elapsed=97.0s
BETA0 gpt2-medium corrected_beta0: 2400/3200, elapsed=104.7s
BETA0 gpt2-medium corrected_beta0: 2800/3200, elapsed=112.5s
BETA0 gpt2-medium corrected_beta0: 3200/3200, elapsed=120.2s
BETA0 gpt2-medium legacy_beta0_diagnostic: 400/3200, elapsed=126.7s
BETA0 gpt2-medium legacy_beta0_diagnostic: 800/3200, elapsed=133.3s
BETA0 gpt2-medium legacy_beta0_diagnostic: 1200/3200, elapsed=139.9s
BETA0 gpt2-medium legacy_beta0_diagnostic: 1600/3200, elapsed=146.4s
BETA0 gpt2-medium legacy_beta0_diagnostic: 2000/3200, elapsed=153.0s
BETA0 gpt2-medium legacy_beta0_diagnostic: 2400/3200, elapsed=159.6s
BETA0 gpt2-medium legacy_beta0_diagnostic: 2800/3200, elapsed=166.2s
BETA0 gpt2-medium legacy_beta0_diagnostic: 3200/3200, elapsed=172.7s

- 2026-11-10T08:03:19+00:00 | V1 beta0 model: gpt2-medium; 3200 matched trials x 3 arms; no trial dropped; checks passed | elapsed_seconds=172.937 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models gpt2-medium --batch 16`

Loading weights:   0%|          | 0/292 [00:00<?, ?it/s]
Loading weights:   0%|          | 1/292 [00:00<00:56,  5.17it/s]
Loading weights:  46%|####5     | 134/292 [00:00<00:00, 563.35it/s]
Loading weights:  73%|#######2  | 212/292 [00:00<00:00, 606.51it/s]
Loading weights:  99%|#########8| 288/292 [00:00<00:00, 653.59it/s]
Loading weights: 100%|##########| 292/292 [00:00<00:00, 565.82it/s]

- 2026-11-10T08:03:29+00:00 | Beta0 queued model exit=0; gpt2-medium; command wall including queue: elapsed_seconds=6080.089 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models gpt2-medium --batch 16`
BETA0 EleutherAI/pythia-410m baseline_beta1: 400/3200, elapsed=8.4s
BETA0 EleutherAI/pythia-410m baseline_beta1: 800/3200, elapsed=14.8s
BETA0 EleutherAI/pythia-410m baseline_beta1: 1200/3200, elapsed=21.2s
BETA0 EleutherAI/pythia-410m baseline_beta1: 1600/3200, elapsed=27.6s
BETA0 EleutherAI/pythia-410m baseline_beta1: 2000/3200, elapsed=34.1s
BETA0 EleutherAI/pythia-410m baseline_beta1: 2400/3200, elapsed=40.5s
BETA0 EleutherAI/pythia-410m baseline_beta1: 2800/3200, elapsed=46.9s
BETA0 EleutherAI/pythia-410m baseline_beta1: 3200/3200, elapsed=53.4s
BETA0 EleutherAI/pythia-410m corrected_beta0: 400/3200, elapsed=60.6s
BETA0 EleutherAI/pythia-410m corrected_beta0: 800/3200, elapsed=67.7s
BETA0 EleutherAI/pythia-410m corrected_beta0: 1200/3200, elapsed=74.9s
BETA0 EleutherAI/pythia-410m corrected_beta0: 1600/3200, elapsed=82.1s
BETA0 EleutherAI/pythia-410m corrected_beta0: 2000/3200, elapsed=89.2s
BETA0 EleutherAI/pythia-410m corrected_beta0: 2400/3200, elapsed=96.4s
BETA0 EleutherAI/pythia-410m corrected_beta0: 2800/3200, elapsed=103.6s
BETA0 EleutherAI/pythia-410m corrected_beta0: 3200/3200, elapsed=110.7s
BETA0 EleutherAI/pythia-410m legacy_beta0_diagnostic: 400/3200, elapsed=116.8s
BETA0 EleutherAI/pythia-410m legacy_beta0_diagnostic: 800/3200, elapsed=122.8s
BETA0 EleutherAI/pythia-410m legacy_beta0_diagnostic: 1200/3200, elapsed=128.9s
BETA0 EleutherAI/pythia-410m legacy_beta0_diagnostic: 1600/3200, elapsed=134.9s
BETA0 EleutherAI/pythia-410m legacy_beta0_diagnostic: 2000/3200, elapsed=141.0s
BETA0 EleutherAI/pythia-410m legacy_beta0_diagnostic: 2400/3200, elapsed=147.0s
BETA0 EleutherAI/pythia-410m legacy_beta0_diagnostic: 2800/3200, elapsed=153.0s
BETA0 EleutherAI/pythia-410m legacy_beta0_diagnostic: 3200/3200, elapsed=159.1s

- 2026-11-10T08:06:04+00:00 | V1 beta0 model: EleutherAI/pythia-410m; 3200 matched trials x 3 arms; no trial dropped; checks passed | elapsed_seconds=159.240 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models EleutherAI/pythia-410m --batch 16`

Loading weights:   0%|          | 0/292 [00:00<?, ?it/s]
Loading weights:   0%|          | 1/292 [00:00<01:48,  2.69it/s]
Loading weights:  37%|###6      | 108/292 [00:00<00:00, 286.06it/s]
Loading weights:  56%|#####5    | 163/292 [00:00<00:00, 252.24it/s]
Loading weights:  70%|######9   | 203/292 [00:00<00:00, 227.72it/s]
Loading weights:  80%|########  | 235/292 [00:01<00:00, 211.49it/s]
Loading weights:  90%|########9 | 262/292 [00:01<00:00, 210.56it/s]
Loading weights:  98%|#########8| 287/292 [00:01<00:00, 214.58it/s]
Loading weights: 100%|##########| 292/292 [00:01<00:00, 206.94it/s]

- 2026-11-10T08:06:12+00:00 | Beta0 queued model exit=0; EleutherAI/pythia-410m; command wall including queue: elapsed_seconds=6230.089 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models EleutherAI/pythia-410m --batch 16`
BETA0 EleutherAI/pythia-1.4b baseline_beta1: 400/3200, elapsed=24.4s
BETA0 EleutherAI/pythia-1.4b baseline_beta1: 800/3200, elapsed=45.1s
BETA0 EleutherAI/pythia-1.4b baseline_beta1: 1200/3200, elapsed=65.8s
BETA0 EleutherAI/pythia-1.4b baseline_beta1: 1600/3200, elapsed=86.4s
BETA0 EleutherAI/pythia-1.4b baseline_beta1: 2000/3200, elapsed=107.1s
BETA0 EleutherAI/pythia-1.4b baseline_beta1: 2400/3200, elapsed=127.8s
BETA0 EleutherAI/pythia-1.4b baseline_beta1: 2800/3200, elapsed=148.5s
BETA0 EleutherAI/pythia-1.4b baseline_beta1: 3200/3200, elapsed=169.2s
BETA0 EleutherAI/pythia-1.4b corrected_beta0: 400/3200, elapsed=190.5s
BETA0 EleutherAI/pythia-1.4b corrected_beta0: 800/3200, elapsed=211.9s
BETA0 EleutherAI/pythia-1.4b corrected_beta0: 1200/3200, elapsed=233.2s
BETA0 EleutherAI/pythia-1.4b corrected_beta0: 1600/3200, elapsed=254.6s
BETA0 EleutherAI/pythia-1.4b corrected_beta0: 2000/3200, elapsed=275.9s
BETA0 EleutherAI/pythia-1.4b corrected_beta0: 2400/3200, elapsed=297.3s
BETA0 EleutherAI/pythia-1.4b corrected_beta0: 2800/3200, elapsed=318.6s
BETA0 EleutherAI/pythia-1.4b corrected_beta0: 3200/3200, elapsed=340.0s
BETA0 EleutherAI/pythia-1.4b legacy_beta0_diagnostic: 400/3200, elapsed=360.3s
BETA0 EleutherAI/pythia-1.4b legacy_beta0_diagnostic: 800/3200, elapsed=380.5s
BETA0 EleutherAI/pythia-1.4b legacy_beta0_diagnostic: 1200/3200, elapsed=400.8s
BETA0 EleutherAI/pythia-1.4b legacy_beta0_diagnostic: 1600/3200, elapsed=421.1s
BETA0 EleutherAI/pythia-1.4b legacy_beta0_diagnostic: 2000/3200, elapsed=441.4s
BETA0 EleutherAI/pythia-1.4b legacy_beta0_diagnostic: 2400/3200, elapsed=461.7s
BETA0 EleutherAI/pythia-1.4b legacy_beta0_diagnostic: 2800/3200, elapsed=481.9s
BETA0 EleutherAI/pythia-1.4b legacy_beta0_diagnostic: 3200/3200, elapsed=502.2s

- 2026-11-10T08:14:33+00:00 | V1 beta0 model: EleutherAI/pythia-1.4b; 3200 matched trials x 3 arms; no trial dropped; checks passed | elapsed_seconds=502.500 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models EleutherAI/pythia-1.4b --batch 16`

Loading weights:   0%|          | 0/290 [00:00<?, ?it/s]
Loading weights: 100%|##########| 290/290 [00:00<00:00, 4330.89it/s]

- 2026-11-10T08:14:46+00:00 | Beta0 queued model exit=0; EleutherAI/pythia-1.4b; command wall including queue: elapsed_seconds=6700.092 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models EleutherAI/pythia-1.4b --batch 16`
BETA0 Qwen/Qwen2.5-0.5B baseline_beta1: 400/3200, elapsed=5.8s
BETA0 Qwen/Qwen2.5-0.5B baseline_beta1: 800/3200, elapsed=9.2s
BETA0 Qwen/Qwen2.5-0.5B baseline_beta1: 1200/3200, elapsed=12.6s
BETA0 Qwen/Qwen2.5-0.5B baseline_beta1: 1600/3200, elapsed=16.1s
BETA0 Qwen/Qwen2.5-0.5B baseline_beta1: 2000/3200, elapsed=19.5s
BETA0 Qwen/Qwen2.5-0.5B baseline_beta1: 2400/3200, elapsed=23.0s
BETA0 Qwen/Qwen2.5-0.5B baseline_beta1: 2800/3200, elapsed=26.4s
BETA0 Qwen/Qwen2.5-0.5B baseline_beta1: 3200/3200, elapsed=29.8s
BETA0 Qwen/Qwen2.5-0.5B corrected_beta0: 400/3200, elapsed=33.8s
BETA0 Qwen/Qwen2.5-0.5B corrected_beta0: 800/3200, elapsed=37.8s
BETA0 Qwen/Qwen2.5-0.5B corrected_beta0: 1200/3200, elapsed=41.8s
BETA0 Qwen/Qwen2.5-0.5B corrected_beta0: 1600/3200, elapsed=45.8s
BETA0 Qwen/Qwen2.5-0.5B corrected_beta0: 2000/3200, elapsed=49.8s
BETA0 Qwen/Qwen2.5-0.5B corrected_beta0: 2400/3200, elapsed=53.8s
BETA0 Qwen/Qwen2.5-0.5B corrected_beta0: 2800/3200, elapsed=57.8s
BETA0 Qwen/Qwen2.5-0.5B corrected_beta0: 3200/3200, elapsed=61.8s
BETA0 Qwen/Qwen2.5-0.5B legacy_beta0_diagnostic: 400/3200, elapsed=64.8s
BETA0 Qwen/Qwen2.5-0.5B legacy_beta0_diagnostic: 800/3200, elapsed=67.8s
BETA0 Qwen/Qwen2.5-0.5B legacy_beta0_diagnostic: 1200/3200, elapsed=70.8s
BETA0 Qwen/Qwen2.5-0.5B legacy_beta0_diagnostic: 1600/3200, elapsed=73.8s
BETA0 Qwen/Qwen2.5-0.5B legacy_beta0_diagnostic: 2000/3200, elapsed=76.8s
BETA0 Qwen/Qwen2.5-0.5B legacy_beta0_diagnostic: 2400/3200, elapsed=79.8s
BETA0 Qwen/Qwen2.5-0.5B legacy_beta0_diagnostic: 2800/3200, elapsed=82.8s
BETA0 Qwen/Qwen2.5-0.5B legacy_beta0_diagnostic: 3200/3200, elapsed=85.8s

- 2026-11-10T08:16:06+00:00 | V1 beta0 model: Qwen/Qwen2.5-0.5B; 3200 matched trials x 3 arms; no trial dropped; checks passed | elapsed_seconds=85.966 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models Qwen/Qwen2.5-0.5B --batch 16`

- 2026-11-10T08:16:14+00:00 | Beta0 queued model exit=0; Qwen/Qwen2.5-0.5B; command wall including queue: elapsed_seconds=6780.093 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models Qwen/Qwen2.5-0.5B --batch 16`

- 2026-11-10T08:16:14+00:00 | Queue/start: .venv/Scripts/python.exe -B phase28_beta0_retest.py --aggregate-only

- 2026-11-10T08:16:18+00:00 | V1 beta0 complete: Five models, 16000 distinct probes, paired baseline/corrected/legacy; aggregate saved

- 2026-11-10T08:16:19+00:00 | Command wall including queue: elapsed_seconds=5.465 | command: `.venv/Scripts/python.exe -B phase28_beta0_retest.py --aggregate-only`

- 2026-11-10T08:16:19+00:00 | Queue/start: .venv/Scripts/python.exe -B phase30_validity_audit.py

- 2026-11-10T08:16:21+00:00 | V1 final validity audit: All V1 arms and beta0 trials reconciled to raw ledgers; completion denominators, identity, masks, sums and paired populations passed | elapsed_seconds=0.927 | command: `.venv/Scripts/python.exe -B phase30_validity_audit.py`
Full validity audit passed in 0.927s

- 2026-11-10T08:16:21+00:00 | Command wall including queue: elapsed_seconds=1.902 | command: `.venv/Scripts/python.exe -B phase30_validity_audit.py`

- 2026-11-10T08:16:21+00:00 | Queue/start: .venv/Scripts/python.exe -B phase25_p0_checks.py --delivery-audit --out out/p0_delivery_v2.json

- 2026-11-10T08:16:45+00:00 | P0 delivery audit: Available audits passed; required pending outputs: [] | elapsed_seconds=22.988 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --delivery-audit --out out/p0_delivery_v2.json`
{"path": "out/p0_delivery_v2.json", "complete": true}

- 2026-11-10T08:16:46+00:00 | Command wall including queue: elapsed_seconds=22.265 | command: `.venv/Scripts/python.exe -B phase25_p0_checks.py --delivery-audit --out out/p0_delivery_v2.json`

- 2026-11-10T08:16:46+00:00 | V1/beta0 delivery complete: elapsed_seconds=33245.068 including prerequisite wait and GPU queues


## Entrega P0 concluída — 2026-11-10T08:26:45+00:00

Todas as saídas requeridas concluídas. Auditorias completas: verdadeiro; pendências requeridas: nenhuma. O inventário auditado tem 244 entradas, incluindo o log mutável. A lista abaixo também identifica os próprios manifestos de auditoria, que não podem conter seu próprio hash. Nenhum texto de paper/ foi editado e nenhum comando git foi executado nesta tarefa.

### 1. Arquivos, um por linha

- data/attn/EleutherAI__pythia-1.4b_n128.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/EleutherAI__pythia-1.4b_n128.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/EleutherAI__pythia-1.4b_n256.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/EleutherAI__pythia-1.4b_n256.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/EleutherAI__pythia-410m_n128.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/EleutherAI__pythia-410m_n128.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/EleutherAI__pythia-410m_n256.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/EleutherAI__pythia-410m_n256.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/Qwen__Qwen2.5-0.5B_n128.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/Qwen__Qwen2.5-0.5B_n128.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/Qwen__Qwen2.5-0.5B_n256.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/Qwen__Qwen2.5-0.5B_n256.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/Qwen__Qwen2.5-3B_n128.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/Qwen__Qwen2.5-3B_n128.npz: atenções float16: 2304 matrizes, 64 documentos.
- data/attn/Qwen__Qwen2.5-3B_n256.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/Qwen__Qwen2.5-3B_n256.npz: atenções float16: 2304 matrizes, 64 documentos.
- data/attn/READY: sinal e resumo das 12 amostras primárias verificadas.
- data/attn/beta0_probe_EleutherAI__pythia-1.4b_s0_v2.manifest.json: manifesto das 3200 sondas, seed, revisão e hashes.
- data/attn/beta0_probe_EleutherAI__pythia-1.4b_s0_v2.npz: sondas congeladas: 3200 itens inteiros.
- data/attn/beta0_probe_EleutherAI__pythia-410m_s0_v2.manifest.json: manifesto das 3200 sondas, seed, revisão e hashes.
- data/attn/beta0_probe_EleutherAI__pythia-410m_s0_v2.npz: sondas congeladas: 3200 itens inteiros.
- data/attn/beta0_probe_Qwen__Qwen2.5-0.5B_s0_v2.manifest.json: manifesto das 3200 sondas, seed, revisão e hashes.
- data/attn/beta0_probe_Qwen__Qwen2.5-0.5B_s0_v2.npz: sondas congeladas: 3200 itens inteiros.
- data/attn/beta0_probe_gpt2-medium_s0_v2.manifest.json: manifesto das 3200 sondas, seed, revisão e hashes.
- data/attn/beta0_probe_gpt2-medium_s0_v2.npz: sondas congeladas: 3200 itens inteiros.
- data/attn/beta0_probe_gpt2_s0_v2.manifest.json: manifesto das 3200 sondas, seed, revisão e hashes.
- data/attn/beta0_probe_gpt2_s0_v2.npz: sondas congeladas: 3200 itens inteiros.
- data/attn/corpus_v2.manifest.json: corpus fixado de 256 artigos, tokens dos seis modelos e revisões.
- data/attn/gpt2-medium_n128.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/gpt2-medium_n128.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/gpt2-medium_n256.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/gpt2-medium_n256.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/gpt2_n128.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/gpt2_n128.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/gpt2_n256.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/gpt2_n256.npz: atenções float16: 1536 matrizes, 64 documentos.
- data/attn/gpt2_n512.manifest.json: manifesto de seleção, camadas/cabeças, contagens efetivas e hashes da amostra.
- data/attn/gpt2_n512.npz: atenções float16: 1536 matrizes, 64 documentos.
- extract_attn.py: extração única, contagens, matrizes float16, manifestos e READY.
- out/_rerun_logs/p0_progress.md: histórico de execução, tempos, decisões e este relatório; arquivo mutável.
- out/p0_comparison_v2.json: comparações descritivas antigas/novas de V2/V3/V4.
- out/p0_delivery_pending_v2.json: auditoria inicial incompleta, preservada como histórico.
- out/p0_delivery_v2.json: auditoria completa e inventário com hashes; todos os requisitos concluídos.
- out/p0_environment_v2.json: versões, hardware, dtypes e limites de threads.
- out/pairs/analysis_cost_v2.jsonl: 384 ajustes medidos, 64 documentos x 3 comprimentos x 2 solvers.
- out/pairs/beta0_EleutherAI__pythia-1.4b_v2.jsonl: 9600 itens pareados: 3200 sondas x 3 braços.
- out/pairs/beta0_EleutherAI__pythia-410m_v2.jsonl: 9600 itens pareados: 3200 sondas x 3 braços.
- out/pairs/beta0_Qwen__Qwen2.5-0.5B_v2.jsonl: 9600 itens pareados: 3200 sondas x 3 braços.
- out/pairs/beta0_gpt2-medium_v2.jsonl: 9600 itens pareados: 3200 sondas x 3 braços.
- out/pairs/beta0_gpt2_v2.jsonl: 9600 itens pareados: 3200 sondas x 3 braços.
- out/pairs/constancy_EleutherAI__pythia-1.4b_n128_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_EleutherAI__pythia-1.4b_n256_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_EleutherAI__pythia-410m_n128_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_EleutherAI__pythia-410m_n256_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_Qwen__Qwen2.5-0.5B_n128_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_Qwen__Qwen2.5-0.5B_n256_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_Qwen__Qwen2.5-3B_n128_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_Qwen__Qwen2.5-3B_n256_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_gpt2-medium_n128_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_gpt2-medium_n256_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_gpt2_n128_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/constancy_gpt2_n256_v2.jsonl: constância por sequência/cabeça, controles e contagens.
- out/pairs/core_EleutherAI__pythia-1.4b_n128_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_EleutherAI__pythia-1.4b_n256_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_EleutherAI__pythia-410m_n128_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_EleutherAI__pythia-410m_n256_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_Qwen__Qwen2.5-0.5B_n128_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_Qwen__Qwen2.5-0.5B_n256_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_Qwen__Qwen2.5-3B_n128_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_Qwen__Qwen2.5-3B_n256_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_gpt2-medium_n128_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_gpt2-medium_n256_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_gpt2_n128_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/core_gpt2_n256_v2.jsonl: pares por instância: concentração de Radon, linhas e SVD.
- out/pairs/downstream_EleutherAI__pythia-1.4b_uniform_v2.jsonl: 3840 pares finais por modelo: 256 documentos x 15 modos.
- out/pairs/downstream_EleutherAI__pythia-410m_uniform_v2.jsonl: 3840 pares finais por modelo: 256 documentos x 15 modos.
- out/pairs/downstream_Qwen__Qwen2.5-0.5B_uniform_v2.jsonl: 3840 pares finais por modelo: 256 documentos x 15 modos.
- out/pairs/downstream_Qwen__Qwen2.5-3B_uniform_v2.jsonl: 3840 pares finais por modelo: 256 documentos x 15 modos.
- out/pairs/downstream_gpt2-medium_uniform_v2.jsonl: 3840 pares finais por modelo: 256 documentos x 15 modos.
- out/pairs/downstream_gpt2_uniform_v2.jsonl: 3840 pares finais por modelo: 256 documentos x 15 modos.
- out/pairs/downstream_gpt2_v2.jsonl: tentativa diagnóstica interrompida antes da regra uniforme; não entra nos agregados finais.
- out/pairs/empty_rows_EleutherAI__pythia-1.4b_v2.jsonl: diagnóstico estático de linhas vazias nas matrizes V2.
- out/pairs/empty_rows_EleutherAI__pythia-410m_v2.jsonl: diagnóstico estático de linhas vazias nas matrizes V2.
- out/pairs/empty_rows_Qwen__Qwen2.5-0.5B_v2.jsonl: diagnóstico estático de linhas vazias nas matrizes V2.
- out/pairs/empty_rows_Qwen__Qwen2.5-3B_v2.jsonl: diagnóstico estático de linhas vazias nas matrizes V2.
- out/pairs/empty_rows_gpt2-medium_v2.jsonl: diagnóstico estático de linhas vazias nas matrizes V2.
- out/pairs/empty_rows_gpt2_v2.jsonl: diagnóstico estático de linhas vazias nas matrizes V2.
- out/pairs/legacy_mass_EleutherAI__pythia-1.4b_v2.jsonl: massa acima da diagonal da fórmula antiga do phase2, seis postos.
- out/pairs/legacy_mass_EleutherAI__pythia-410m_v2.jsonl: massa acima da diagonal da fórmula antiga do phase2, seis postos.
- out/pairs/legacy_mass_Qwen__Qwen2.5-0.5B_v2.jsonl: massa acima da diagonal da fórmula antiga do phase2, seis postos.
- out/pairs/legacy_mass_Qwen__Qwen2.5-3B_v2.jsonl: massa acima da diagonal da fórmula antiga do phase2, seis postos.
- out/pairs/legacy_mass_gpt2-medium_v2.jsonl: massa acima da diagonal da fórmula antiga do phase2, seis postos.
- out/pairs/legacy_mass_gpt2_v2.jsonl: massa acima da diagonal da fórmula antiga do phase2, seis postos.
- out/pairs/named_EleutherAI__pythia-1.4b_n128_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_EleutherAI__pythia-1.4b_n256_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_EleutherAI__pythia-410m_n128_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_EleutherAI__pythia-410m_n256_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_Qwen__Qwen2.5-0.5B_n128_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_Qwen__Qwen2.5-0.5B_n256_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_Qwen__Qwen2.5-3B_n128_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_Qwen__Qwen2.5-3B_n256_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_gpt2-medium_n128_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_gpt2-medium_n256_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_gpt2_n128_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/pairs/named_gpt2_n256_msclean_srpca_v2.jsonl: pares por instância com 15 configurações de métricas nomeadas.
- out/phase15_EleutherAI__pythia-1.4b_n128_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_EleutherAI__pythia-1.4b_n256_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_EleutherAI__pythia-410m_n128_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_EleutherAI__pythia-410m_n256_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_Qwen__Qwen2.5-0.5B_n128_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_Qwen__Qwen2.5-0.5B_n256_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_Qwen__Qwen2.5-3B_n128_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_Qwen__Qwen2.5-3B_n256_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_gpt2-medium_n128_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_gpt2-medium_n256_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_gpt2_n128_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_gpt2_n256_v2.json: distribuição da constância por sequência/cabeça nesta amostra.
- out/phase15_interaction_v2.json: V4 agregado por forward, 19968 matrizes.
- out/phase17_efficiency_v2.json: custos de análise offline; não é medição de velocidade de inferência.
- out/phase18_beta0_dependency_audit_v2.json: dependência dos números antigos de CV em beta0; sem nova avaliação de CV.
- out/phase1_multimodel_v2.json: agregado das métricas núcleo, seis modelos.
- out/phase24_core_EleutherAI__pythia-1.4b_n128_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_EleutherAI__pythia-1.4b_n256_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_EleutherAI__pythia-410m_n128_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_EleutherAI__pythia-410m_n256_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_Qwen__Qwen2.5-0.5B_n128_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_Qwen__Qwen2.5-0.5B_n256_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_Qwen__Qwen2.5-3B_n128_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_Qwen__Qwen2.5-3B_n256_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_gpt2-medium_n128_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_gpt2-medium_n256_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_gpt2_n128_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase24_core_gpt2_n256_v2.json: métricas núcleo por modelo/comprimento e respectivos pares.
- out/phase25_completion_options_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_exact_driver_api_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_final_reconstruction_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_fraction_constancy_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_geometry_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_identity_EleutherAI__pythia-1.4b_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_identity_EleutherAI__pythia-410m_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_identity_Qwen__Qwen2.5-0.5B_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_identity_Qwen__Qwen2.5-3B_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_identity_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_identity_gpt2-medium_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_identity_gpt2_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_native_source_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_reconstruction_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_retrieval_audit_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_retrieval_completion_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_retrieval_final_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_retrieval_fixed_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_sampling_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_sampling_regressions_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase25_uniform_reconstruction_checks_v2.json: sanidade/auditoria versionada; veja os casos e resultados no JSON.
- out/phase26_named_EleutherAI__pythia-1.4b_n128_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_EleutherAI__pythia-1.4b_n256_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_EleutherAI__pythia-410m_n128_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_EleutherAI__pythia-410m_n256_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_Qwen__Qwen2.5-0.5B_n128_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_Qwen__Qwen2.5-0.5B_n256_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_Qwen__Qwen2.5-3B_n128_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_Qwen__Qwen2.5-3B_n256_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_gpt2-medium_n128_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_gpt2-medium_n256_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_gpt2_n128_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase26_named_gpt2_n256_msclean_srpca_v2.json: métricas nomeadas por modelo/comprimento, todas as 15 configurações.
- out/phase28_positive_beta_cpu_v2.json: regressão beta positivo em GPT-2 real, CPU, logits idênticos.
- out/phase29_publication_checks_v2.json: regressão do sink ou da publicação atômica; passou.
- out/phase29_sink_checks_v2.json: regressão do sink ou da publicação atômica; passou.
- out/phase2_EleutherAI__pythia-1.4b_v2.json: resultado downstream por modelo com contagens, escalas e sanidades.
- out/phase2_EleutherAI__pythia-410m_v2.json: resultado downstream por modelo com contagens, escalas e sanidades.
- out/phase2_Qwen__Qwen2.5-0.5B_v2.json: resultado downstream por modelo com contagens, escalas e sanidades.
- out/phase2_Qwen__Qwen2.5-3B_v2.json: resultado downstream por modelo com contagens, escalas e sanidades.
- out/phase2_document_statistics_v2.json: 90 modos, IC95% da mediana/média de KL por documento, 2000 reamostragens seed0.
- out/phase2_downstream_v2.json: V1 completo: seis modelos, 256 documentos, último token, referências e contadores.
- out/phase2_driver_decision_v2.json: troca de driver retirada antes de qualquer execução; driver padrão mantido.
- out/phase2_empty_rows_EleutherAI__pythia-1.4b_v2.json: diagnóstico estático antes da escolha da regra uniforme.
- out/phase2_empty_rows_EleutherAI__pythia-410m_v2.json: diagnóstico estático antes da escolha da regra uniforme.
- out/phase2_empty_rows_Qwen__Qwen2.5-0.5B_v2.json: diagnóstico estático antes da escolha da regra uniforme.
- out/phase2_empty_rows_Qwen__Qwen2.5-3B_v2.json: diagnóstico estático antes da escolha da regra uniforme.
- out/phase2_empty_rows_gpt2-medium_v2.json: diagnóstico estático antes da escolha da regra uniforme.
- out/phase2_empty_rows_gpt2_v2.json: diagnóstico estático antes da escolha da regra uniforme.
- out/phase2_empty_rows_v2.json: diagnóstico estático antes da escolha da regra uniforme.
- out/phase2_execution_gpt2-medium_v2.json: código efetivamente carregado pelos primeiros processos, antes das otimizações posteriores.
- out/phase2_execution_gpt2_v2.json: código efetivamente carregado pelos primeiros processos, antes das otimizações posteriores.
- out/phase2_gpt2-medium_v2.json: resultado downstream por modelo com contagens, escalas e sanidades.
- out/phase2_gpt2_v2.json: resultado downstream por modelo com contagens, escalas e sanidades.
- out/phase2_legacy_mass_EleutherAI__pythia-1.4b_v2.json: diagnóstico da fórmula antiga do phase2 sobre as amostras congeladas.
- out/phase2_legacy_mass_EleutherAI__pythia-410m_v2.json: diagnóstico da fórmula antiga do phase2 sobre as amostras congeladas.
- out/phase2_legacy_mass_Qwen__Qwen2.5-0.5B_v2.json: diagnóstico da fórmula antiga do phase2 sobre as amostras congeladas.
- out/phase2_legacy_mass_Qwen__Qwen2.5-3B_v2.json: diagnóstico da fórmula antiga do phase2 sobre as amostras congeladas.
- out/phase2_legacy_mass_gpt2-medium_v2.json: diagnóstico da fórmula antiga do phase2 sobre as amostras congeladas.
- out/phase2_legacy_mass_gpt2_v2.json: diagnóstico da fórmula antiga do phase2 sobre as amostras congeladas.
- out/phase2_legacy_mass_v2.json: diagnóstico da fórmula antiga do phase2 sobre as amostras congeladas.
- out/phase2_parallel_schedule_EleutherAI__pythia-1.4b_v2.json: prova GPU de logits e contadores idênticos, tempos e escolha da execução SVD.
- out/phase2_parallel_schedule_EleutherAI__pythia-410m_v2.json: prova GPU de logits e contadores idênticos, tempos e escolha da execução SVD.
- out/phase2_parallel_schedule_Qwen__Qwen2.5-0.5B_v2.json: prova GPU de logits e contadores idênticos, tempos e escolha da execução SVD.
- out/phase2_parallel_schedule_Qwen__Qwen2.5-3B_v2.json: prova GPU de logits e contadores idênticos, tempos e escolha da execução SVD.
- out/phase30_validity_audit_v2.json: auditoria final de 23040 registros V1 e 48000 itens beta0; passou.
- out/phase30_validity_v1_checks_v2.json: conciliação completa de V1; relatório parcial nunca marca a entrega total como concluída.
- out/phase33_fixedshape_checks_v2.json: regressão de equivalência, contadores e fronteiras das tolerâncias; passou.
- out/phase33_legacy_counter_checks_v2.json: regressão de equivalência, contadores e fronteiras das tolerâncias; passou.
- out/phase33_validation_schedule_checks_v2.json: regressão de equivalência, contadores e fronteiras das tolerâncias; passou.
- out/phase3_robustness_v2.json: agregado das 12 amostras e dois comprimentos.
- out/phase5_msclean_v2.json: V3 agregado para MS-CLEAN, todas as amostras.
- out/phase6_srpca_v2.json: V3 agregado para ajuste alternado, todas as amostras.
- out/phase7_EleutherAI__pythia-1.4b_v2.json: resultado de editabilidade por modelo, quatro modos e 256 documentos.
- out/phase7_EleutherAI__pythia-410m_v2.json: resultado de editabilidade por modelo, quatro modos e 256 documentos.
- out/phase7_Qwen__Qwen2.5-0.5B_v2.json: resultado de editabilidade por modelo, quatro modos e 256 documentos.
- out/phase7_Qwen__Qwen2.5-3B_v2.json: resultado de editabilidade por modelo, quatro modos e 256 documentos.
- out/phase7_editability_v2.json: edições completas nos mesmos seis modelos e documentos.
- out/phase7_gpt2-medium_v2.json: resultado de editabilidade por modelo, quatro modos e 256 documentos.
- out/phase7_gpt2_v2.json: resultado de editabilidade por modelo, quatro modos e 256 documentos.
- out/phase8_beta0_EleutherAI__pythia-1.4b_v2.json: resultado por modelo, 3200 sondas por braço e validações.
- out/phase8_beta0_EleutherAI__pythia-410m_v2.json: resultado por modelo, 3200 sondas por braço e validações.
- out/phase8_beta0_Qwen__Qwen2.5-0.5B_v2.json: resultado por modelo, 3200 sondas por braço e validações.
- out/phase8_beta0_gpt2-medium_v2.json: resultado por modelo, 3200 sondas por braço e validações.
- out/phase8_beta0_gpt2_v2.json: resultado por modelo, 3200 sondas por braço e validações.
- out/phase8_beta0_v2.json: cinco modelos x 3200 sondas x 3 braços, McNemar pareado e Holm.
- out/phase9_bigmodel_named_v2.json: métricas nomeadas do 3B nos dois comprimentos.
- out/phase9_bigmodel_v2.json: métricas núcleo do 3B nos dois comprimentos.
- phase10_baselines.py: edições do sink usam o helper comum corrigido.
- phase14_adaptive.py: edições fixas, adaptativas e ACT usam o helper comum corrigido.
- phase15_interaction.py: distribuição da constância por sequência e cabeça.
- phase17_efficiency.py: custo de ajuste offline NNLS+SVD em 128/256/512, com versões densa e QR.
- phase1_multimodel.py: métricas multimodelo sobre as amostras versionadas.
- phase24_p0_metrics.py: métricas núcleo e diagnósticos de massa antiga/linhas vazias, com pares por instância.
- phase25_p0_checks.py: regressões, auditorias de fontes/amostras/sondas e inventário final.
- phase26_p0_named.py: V3 em todas as matrizes, NNLS reduzido exato e identidades de energia.
- phase27_finish_v1.py: orquestrador inicial de V1, preservado para rastreabilidade.
- phase28_beta0_retest.py: reteste completo de beta0 na semente histórica 0, três braços pareados e regressão beta positivo.
- phase29_sink_checks.py: casos sem alternativa, massa positiva minúscula, offsets, dtypes e herança entre scripts.
- phase2_downstream.py: máscara com offset, uniforme causal, último token, contadores e sanidades nos seis modelos.
- phase30_validity_audit.py: conciliação de documentos, alvos, métricas, contadores e todos os pares de V1/beta0.
- phase31_finish_beta0.py: fila de cinco testes de beta0 e auditorias finais.
- phase32_queue_remaining_v1.py: fila dos modelos restantes de V1, um job de GPU por lock.
- phase33_validation_schedule.py: prova de equivalência das validações imediatas e deferidas.
- phase34_parallel_svd.py: mesma SVD exata em grupos independentes de cabeças, três streams e prova dos 15 modos.
- phase35_downstream_intervals.py: ICs da mediana principal e da média secundária de KL por documento.
- phase3_robustness.py: comparação entre comprimentos nas amostras V2.
- phase5_msclean.py: frações nomeadas com norma, energia, termo cruzado e redução de erro separados.
- phase6_srpca.py: mesmas métricas separadas para o ajuste alternado.
- phase7_editability.py: offset causal, normalização compartilhada e preservação da linha sem alternativa antes da edição.
- phase8_lostmiddle.py: helper comum para edição válida do sink, contadores e validações.
- phase9_bigmodel.py: métricas do modelo 3B sobre as amostras V2.
- sampling.py: amostragem, corpus imutável e publicação JSON atômica/exclusiva.

### 2. Comandos e tempos

Tempos internos: Python Windows/perf_counter, incluindo carga, verificações e agregação do modelo. Tempos com fila: supervisor WSL; os jobs foram enfileirados juntos, portanto esses tempos não devem ser somados. Todos os processos limitam threads a quatro.

Comando V1 para cada linha: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase2_downstream.py --models MODELO --batch 2
Comando beta0 para cada um dos cinco modelos históricos: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase28_beta0_retest.py --models MODELO --batch 16

| Modelo | V1 interno (s) | V1 com fila (s) | beta0 interno (s) | beta0 com fila (s) |
|---|---:|---:|---:|---:|
| gpt2 | 2109.577 | 4694.311 | 60.289 | 5910.098 |
| gpt2-medium | 4392.945 | 10010.564 | 172.761 | 6080.089 |
| EleutherAI/pythia-410m | 4997.106 | 14730.907 | 159.071 | 6230.089 |
| EleutherAI/pythia-1.4b | 4295.284 | 18761.099 | 502.245 | 6700.092 |
| Qwen/Qwen2.5-0.5B | 3269.676 | 21821.179 | 85.803 | 6780.093 |
| Qwen/Qwen2.5-3B | 5024.016 | 26501.260 | — | — |

Comandos CPU abaixo usam .venv/Scripts/python.exe -B. As verificações históricas adicionais, os comandos de preparação, as agregações e os comandos anteriores V2/V3/V4/V5 com seus tempos estão registrados cronologicamente acima.

| Comando CPU | Tempo interno (s) |
|---|---:|
| phase25_p0_checks.py --reconstruction --out out/phase25_uniform_reconstruction_checks_v2.json | 5.968253 |
| phase29_sink_checks.py | 0.337054 |
| phase28_beta0_retest.py --cpu-regression-only | 4.504267 |
| phase25_p0_checks.py --reconstruction --out out/phase25_exact_driver_api_checks_v2.json | 14.535282 |
| phase33_validation_schedule.py | 53.285375 |
| phase25_p0_checks.py --retrieval-audit --out out/phase25_retrieval_completion_v2.json | 6.201108 |
| phase30_validity_audit.py --v1-only | 1.127437 |
| phase35_downstream_intervals.py | 1.813848 |
| phase30_validity_audit.py | 0.927485 |
| phase25_p0_checks.py --delivery-audit --out out/p0_delivery_v2.json | 22.987806 |

Preparação das cinco sondas: phase28_beta0_retest.py --prepare-only, 13.984 s. Agregação V1, CPU: phase2_downstream.py --aggregate-only, 6.892 s de parede com inicialização. Agregação beta0: phase28_beta0_retest.py --aggregate-only, 5.465 s de parede. Publicação atômica: 0.017 s; regressão de contadores legados: 0.019 s; formas fixas e argmax: 0.005 s. A troca proposta de driver SVD não foi executada.

### 3. Números novos versus antigos

KL em nats. As médias antigas não são uma comparação causal pareada: o corpus, a avaliação por posição e, no Qwen, o dtype mudaram. Principal novo = mediana por documento com IC95% por 2000 reamostragens seed0; média como secundária. Todos os modos têm os mesmos 256 documentos por modelo.

| Modelo | Média KL SVD8 antiga → nova | Mediana nova SVD8 [IC95%] | Média KL ANOVA8 antiga → nova |
|---|---:|---:|---:|
| gpt2 | 2.192 → 2.435 | 2.027 [1.806, 2.177] | 1.050 → 2.068 |
| gpt2-medium | — → 1.896 | 1.472 [1.360, 1.625] | 1.052 → 1.873 |
| EleutherAI/pythia-410m | 2.041 → 2.569 | 2.112 [1.972, 2.323] | 1.616 → 2.533 |
| EleutherAI/pythia-1.4b | — → 2.333 | 2.028 [1.856, 2.270] | 1.602 → 2.312 |
| Qwen/Qwen2.5-0.5B | 1.971 → 2.510 | 2.208 [2.064, 2.357] | 1.693 → 2.389 |
| Qwen/Qwen2.5-3B | — → 8.003 | 6.941 [6.353, 7.523] | — → 7.265 |

Referências de escala, mesmas 256 sequências por modo:

| Modelo | Média KL uniforme causal | Só diagonal | Só sink |
|---|---:|---:|---:|
| gpt2 | 6.141 | 11.314 | 3.478 |
| gpt2-medium | 5.046 | 8.914 | 4.219 |
| EleutherAI/pythia-410m | 4.509 | 3.965 | 5.157 |
| EleutherAI/pythia-1.4b | 3.685 | 4.195 | 4.854 |
| Qwen/Qwen2.5-0.5B | 5.124 | 4.734 | 6.024 |
| Qwen/Qwen2.5-3B | 6.933 | 5.007 | 8.208 |

Qwen3B é mantido integralmente: SVD8 tem KL média 8.003, maior que a referência uniforme 6.933 e a geometria 4.856. Esse resultado impede alegar fidelidade funcional a partir de baixo erro matricial.

Regra uniforme na SVD8; todos os modos e postos estão detalhados nos agregados e pares:

| Modelo | Linhas completadas/total | Fração | Última consulta completada/total | Fração |
|---|---:|---:|---:|---:|
| gpt2 | 0/4718592 | 0 | 0/36864 | 0 |
| gpt2-medium | 0/12582912 | 0 | 0/98304 | 0 |
| EleutherAI/pythia-410m | 16/12582912 | 1.27156576e-06 | 0/98304 | 0 |
| EleutherAI/pythia-1.4b | 1/12582912 | 7.94728597e-08 | 0/98304 | 0 |
| Qwen/Qwen2.5-0.5B | 3323/11010048 | 0.000301815215 | 68/86016 | 0.000790550595 |
| Qwen/Qwen2.5-3B | 28666/18874368 | 0.00151877933 | 241/147456 | 0.00163438585 |

Beta0: acurácias em porcentagem; 3200 sondas por modelo/braço, 2000 no meio, oito posições, semente 0. Esta é a única semente histórica que incluiu beta0: sementes 1 e 2 testaram somente beta1 e beta0.25. O legado pareado é recalculado no mesmo dtype atual; o Qwen histórico usava fp32 e agora usa bf16.

| Modelo | Baseline atual beta1 | beta0 histórico | Legado pareado atual | beta0 corrigido | Diferença corrigido - baseline (pp) |
|---|---:|---:|---:|---:|---:|
| gpt2 | 35.93750 | 44.71875 | 44.71875 | 44.71875 | +8.78125 |
| gpt2-medium | 43.71875 | 9.62500 | 9.62500 | 9.68750 | -34.03125 |
| EleutherAI/pythia-410m | 48.06250 | 48.37500 | 48.37500 | 48.34375 | +0.28125 |
| EleutherAI/pythia-1.4b | 48.53125 | 48.90625 | 48.90625 | 49.09375 | +0.56250 |
| Qwen/Qwen2.5-0.5B | 52.09375 | 53.96875 | 53.15625 | 52.53125 | +0.43750 |

GPT2-medium: 1399/3200 → 310/3200 acertos, perda relativa de 77.841%; no meio, 43.40% → 11.75% (2000 itens). McNemar pareado com Holm nos cinco modelos: p=1.48e-220. O colapso de acurácia persiste com distribuições válidas. Outros quatro modelos não perdem acurácia global; não se conclui necessidade geral do sink nem instabilidade numérica.

### 4. Sanidades e resultados

- V1: 23040 registros = seis modelos x 256 documentos x 15 modos; população e alvos conciliados sem omissões/duplicações.
- Beta0: 48000 registros = 16000 sondas x três braços; população, alvos e correção conciliados; todos os itens retidos.
- Identidade V1: KL exatamente zero nos dois harnesses, em todos os seis modelos/documentos.
- Identidade da sonda: callback beta1 reproduz logits nativos exatamente nos cinco modelos, inclusive Qwen bf16.
- Beta positivo: GPT2 real em beta0.25, CPU e GPU, logits antigos/corrigidos bit a bit idênticos, diferença máxima zero.
- Sufixo: invariância exata nos 15 modos dos seis modelos, alvo fora da entrada; controle negativo com ajuste irrestrito registrado.
- Reconstruções: nenhum NaN/Inf/negativo ou valor acima da diagonal; máscara k-q antes de clamp/renormalização; limites por dtype fixos e fronteiras testadas.
- Uniforme: mesma regra causal para SVD/geometria/S+L via função compartilhada; original fornece apenas dtype; teste com original envenenado com NaN passou.
- Sink: linha absoluta 0 e qualquer linha sem alternativa ficam preservadas; massa positiva minúscula é normalizada pelo total real; offsets com cache testados.
- Nas cinco sondas beta0 corrigidas: 5222400 linhas preservadas em 668467200, exatamente as primeiras linhas por cabeça/camada; nenhuma na última consulta. O legado tem 5390353 linhas zeradas: 5222400 primeiras linhas e 167953 linhas adicionais em Pythia1.4B, incluindo 1078 na última consulta. São trajetórias de forward distintas; as contagens internas não precisam coincidir. O legado é diagnóstico explícito de atenção inválida.
- Massa positiva abaixo do antigo piso 1e-9: 52520 linhas no beta0 corrigido, contadas separadamente. Não são tratadas como linhas vazias.
- Validações deferidas: mesmos valores, contadores e rejeições dos casos inválidos; equivalência bit a bit dos logits confirmada nas provas CPU/GPU, sem afrouxar limites.
- Paralelismo: mesma SVD float32 completa e driver padrão; provas de 15 modos aprovadas. Usado em Pythia1.4B e nos dois Qwen; Pythia410M manteve execução sequencial porque ganho de tempo ficou abaixo de 10%. GPT2/GPT2-medium completaram sequencialmente.
- Um aviso interno de cuSOLVER no Pythia1.4B foi preservado no log; o PyTorch usou seu fallback padrão já integrante de driver=None. Nenhum caso foi descartado, substituído ou capturado por try/except do experimento.
- Publicação JSON atômica/exclusiva no Windows: completude, recusa de sobrescrita e limpeza de temporário passaram.
- V2/V3/V4/V5 anteriores: auditoria final reconferiu as 19968 matrizes primárias, 36 grupos de pares e os 384 ajustes de custo. Identidades de norma/energia/termo cruzado mantêm erro <=1e-12.
- Auditoria phase8/10/11/14/16/18: avaliações usam último token; não foi encontrado vazamento de alvo na sonda multi-token. A falha corrigida foi a distribuição inválida da edição beta0. Phase11/16/18 herdam o helper corrigido sem editar seus arquivos.
- Portão de outra família: esta execução fez auditorias automáticas sobre código e arquivos; não executou revisão independente de outra família antes de integração no artigo.

### 5. Decisões

| Pergunta | Sugestão/decisão | Certeza | Executou? |
|---|---|---|---|
| Como completar linha vazia? | Uniforme causal por suporte absoluto; nunca copiar a linha original nem descartar sequência. | Alta; decisão do usuário | Sim, todos os seis modelos/modos/postos. |
| Como editar sink sem alternativa? | Preservar a distribuição anterior à edição; normalizar qualquer massa positiva pelo seu total. | Alta | Sim, helper phase8/10/14 herdado por 11/16/18 e usado no phase7. |
| Como acelerar mantendo a matemática? | Adiar sincronizações de validação; mesma SVD em três streams somente após equivalência exata e ganho >=10%. | Alta após provas | Sim onde aprovado; sem trocar driver, precisão, posto ou população. |
| Trocar o driver SVD para acelerar? | Manter o padrão; igual erro de Frobenius não fixa subespaços truncados em empates. | Média | Não; proposta retirada antes de qualquer execução alternativa. |
| Qual agregação principal? | Mediana por documento com IC95%; média KL secundária, NLL média para verossimilhança. | Alta; convenção do plano | Sim, arquivo separado sem sobrescrever agregados. |
| Reavaliar CV antiga do phase18? | Necessário antes de citar os resultados: todas as 15 grades incluem beta0 e Pythia1.4B o selecionou em B nas três sementes. | Alta quanto à dependência | Não, fora do reteste explicitamente limitado ao phase8; helper já corrigido. |
| A frase do artigo sobre colapso sobrevive? | A queda de acurácia sobrevive no GPT2-medium; descrever o modelo/sonda e evitar inferência de instabilidade numérica ou necessidade geral do sink. | Alta sobre o reteste; interpretação além da sonda não estabelecida | Evidência produzida; paper/ permanece a cargo do usuário. |

FALTA: os JSONs antigos de phase2/phase7 não registram contagens efetivas de documentos; os IDs/inputs brutos das sondas históricas não foram salvos, então a reprodução é do protocolo e da semente, não uma prova criptográfica de identidade histórica. Tempos das primeiras tentativas abortadas anteriores à instrumentação também não estavam registrados.

Veredito: P0 concluído e auditado; o colapso de acurácia com beta0 permanece no GPT2-medium após a correção, com todas as distribuições válidas.

- 2026-11-10T08:33:32+00:00 | Correção da descrição final do legado: a checagem de consolidação rejeitou a suposição de que todas as linhas zeradas legadas eram primeiras linhas. Totais lidos dos JSONs: 5390353 zeradas, 1078 na última consulta (Pythia1.4B); corrigido preserva 5222400 sem alternativa, zero na última consulta. Somente a frase do relatório foi corrigida; nenhum resultado/JSON, tolerância, implementação ou teste científico foi alterado.

- 2026-11-10T11:29:47+00:00 | Phase36 exempt: gpt2; exempt=[]; arms=['phase2:svd:8'] | elapsed_seconds=131.170 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase36_exempt_heads.py --models gpt2`

- 2026-11-10T11:36:04+00:00 | Phase36 exempt: gpt2-medium; exempt=[]; arms=['phase2:svd:8'] | elapsed_seconds=351.811 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase36_exempt_heads.py --models gpt2-medium`

- 2026-11-10T11:41:58+00:00 | Phase36 exempt: EleutherAI/pythia-410m; exempt=[]; arms=['phase2:svd:8'] | elapsed_seconds=353.430 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase36_exempt_heads.py --models EleutherAI/pythia-410m`

- 2026-11-10T11:48:17+00:00 | Phase36 exempt: EleutherAI/pythia-1.4b; exempt=[]; arms=['phase2:svd:8'] | elapsed_seconds=379.261 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase36_exempt_heads.py --models EleutherAI/pythia-1.4b`

- 2026-11-10T12:19:15+00:00 | Phase36 exempt: Qwen/Qwen2.5-0.5B; exempt=[[0, 1], [8, 3], [23, 1]]; arms=['phase2:svd:1', 'phase2:svd:2', 'phase2:svd:4', 'phase2:svd:8', 'phase2:svd:16', 'phase2:svd:32', 'phase2:geom'] | elapsed_seconds=1851.432 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase36_exempt_heads.py --models Qwen/Qwen2.5-0.5B`

- 2026-11-10T13:11:20+00:00 | Phase36 exempt: Qwen/Qwen2.5-3B; exempt=[[0, 12], [27, 8]]; arms=['phase2:svd:1', 'phase2:svd:2', 'phase2:svd:4', 'phase2:svd:8', 'phase2:svd:16', 'phase2:svd:32', 'phase2:geom'] | elapsed_seconds=3117.438 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase36_exempt_heads.py --models Qwen/Qwen2.5-3B`

- 2026-11-10T13:19:53+00:00 | Phase36 empty sanity: Qwen/Qwen2.5-3B; exempt=[]; arms=['phase2:svd:8'] | elapsed_seconds=506.578 | command: `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase36_exempt_heads.py --models Qwen/Qwen2.5-3B`
