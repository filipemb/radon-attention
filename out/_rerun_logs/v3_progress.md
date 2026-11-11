
- 2026-11-10T09:09:06+00:00 | V3 constancy: gpt2 n=128; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=4.432922

- 2026-11-10T09:09:10+00:00 | V3 named intervals: gpt2 n=128; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=8.069001

- 2026-11-10T09:09:17+00:00 | V3 constancy: gpt2 n=256; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=10.720771

- 2026-11-10T09:09:18+00:00 | V3 named intervals: gpt2 n=256; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=8.643465

- 2026-11-10T09:09:21+00:00 | V3 constancy: gpt2-medium n=128; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=4.595638

- 2026-11-10T09:09:27+00:00 | V3 named intervals: gpt2-medium n=128; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=8.479162

- 2026-11-10T09:09:33+00:00 | V3 constancy: gpt2-medium n=256; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=11.232230

- 2026-11-10T09:09:35+00:00 | V3 named intervals: gpt2-medium n=256; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=7.721988

- 2026-11-10T09:09:37+00:00 | V3 constancy: EleutherAI/pythia-410m n=128; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=4.698007

- 2026-11-10T09:09:42+00:00 | V3 named intervals: EleutherAI/pythia-410m n=128; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=7.247340

- 2026-11-10T09:09:49+00:00 | V3 constancy: EleutherAI/pythia-410m n=256; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=11.374132

- 2026-11-10T09:09:50+00:00 | V3 named intervals: EleutherAI/pythia-410m n=256; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=7.804719

- 2026-11-10T09:09:54+00:00 | V3 constancy: EleutherAI/pythia-1.4b n=128; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=4.857176

- 2026-11-10T09:09:58+00:00 | V3 named intervals: EleutherAI/pythia-1.4b n=128; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=8.568184

- 2026-11-10T09:10:05+00:00 | V3 constancy: EleutherAI/pythia-1.4b n=256; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=11.036389

- 2026-11-10T09:10:07+00:00 | V3 named intervals: EleutherAI/pythia-1.4b n=256; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=8.358302

- 2026-11-10T09:10:09+00:00 | V3 constancy: Qwen/Qwen2.5-0.5B n=128; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=4.572932

- 2026-11-10T09:10:15+00:00 | V3 named intervals: Qwen/Qwen2.5-0.5B n=128; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=8.014911

- 2026-11-10T09:10:20+00:00 | V3 constancy: Qwen/Qwen2.5-0.5B n=256; 1536 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=10.962621

- 2026-11-10T09:10:22+00:00 | V3 named intervals: Qwen/Qwen2.5-0.5B n=256; 1536 instances, 15 configurations; raw decompositions reused | elapsed_seconds=7.734499

- 2026-11-10T09:10:27+00:00 | V3 constancy: Qwen/Qwen2.5-3B n=128; 2304 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=6.971806

- 2026-11-10T09:10:34+00:00 | V3 named intervals: Qwen/Qwen2.5-3B n=128; 2304 instances, 15 configurations; raw decompositions reused | elapsed_seconds=11.617406

- 2026-11-10T09:10:44+00:00 | V3 constancy: Qwen/Qwen2.5-3B n=256; 2304 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=17.009620

- 2026-11-10T09:10:46+00:00 | V3 named intervals: Qwen/Qwen2.5-3B n=256; 2304 instances, 15 configurations; raw decompositions reused | elapsed_seconds=12.080953

- 2026-11-10T09:10:46+00:00 | V3 CPU complete: named; 12 datasets | elapsed_seconds=104.776482 | command: .venv/Scripts/python.exe -B phase36_constancy_named_ci.py --part named

- 2026-11-10T09:10:49+00:00 | V3 constancy: Qwen/Qwen2.5-7B n=128; 1792 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=5.187122

- 2026-11-10T09:11:01+00:00 | V3 constancy: Qwen/Qwen2.5-7B n=256; 1792 heads, two mass strata, zero energy excluded/counted | elapsed_seconds=11.897380

- 2026-11-10T09:11:01+00:00 | V3 CPU complete: constancy; 14 datasets | elapsed_seconds=119.754018 | command: .venv/Scripts/python.exe -B phase36_constancy_named_ci.py --part constancy

- 2026-11-10T09:33:48+00:00 | V3 frozen probes: 21 phase8/KV datasets and 15 two-family CV datasets; all seeds/models, seed0 matches v2 arrays exactly | elapsed_seconds=38.167562 | command: .venv/Scripts/python.exe -B phase38_paired_items.py --prepare-only

- 2026-11-10T09:40:00+00:00 | V3 matched CPU checks: 20 cases; exact mass construction, q0 identity, nonnegative and cached offsets | elapsed_seconds=0.024967

- 2026-11-10T10:08:02+00:00 | V3 full coordinator started: 300 short GPU jobs; release lock before each CPU verification

- 2026-11-10T10:08:02+00:00 | Join already queued initial job PID=7381: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 0 --stop 16

- 2026-11-10T11:25:39+00:00 | V3 items GPU: phase8 gpt2 s0 historical; 6400 records, no item omitted | elapsed_seconds=48.178443

- 2026-11-10T11:26:06+00:00 | V3 matched pilot: gpt2; native/ANOVA/suffix passed; parallel=True, exact=True

- 2026-11-10T11:26:55+00:00 | V3 matched chunk: gpt2; articles 0:16, all twelve arms retained | elapsed_seconds=69.993293 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 0 --stop 16

- 2026-11-10T11:27:02+00:00 | GPU result complete; observed_wait_and_run_seconds=4290.410: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 0 --stop 16

- 2026-11-10T11:27:02+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d000_016_v3.json

- 2026-11-10T11:27:08+00:00 | CPU complete; wall_seconds=6.039: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d000_016_v3.json

- 2026-11-10T11:27:08+00:00 | Cached completed output, CPU verification: out/phase8_items_gpt2_s0_historical_v3.json

- 2026-11-10T11:27:08+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2_s0_historical_v3.json

- 2026-11-10T11:27:14+00:00 | CPU complete; wall_seconds=6.021: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2_s0_historical_v3.json

- 2026-11-10T11:27:14+00:00 | Join already queued initial job PID=25545: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase39_betacv_items.py --model gpt2 --seed 0 --variant historical --beta 1.0

- 2026-11-10T11:27:30+00:00 | V3 CV beta job: gpt2 s0 historical beta=1.0; both full families, lock released after job | elapsed_seconds=28.627106 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase39_betacv_items.py --model gpt2 --seed 0 --variant historical --beta 1.0

- 2026-11-10T11:27:32+00:00 | GPU result complete; observed_wait_and_run_seconds=15.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase39_betacv_items.py --model gpt2 --seed 0 --variant historical --beta 1.0

- 2026-11-10T11:27:32+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-beta-job out/phase18_items_gpt2_s0_historical_b1.0_v3.json

- 2026-11-10T11:31:14+00:00 | V3 coordinator started: 120 short GPU jobs, kinds=['mass', 'items']; release lock before each CPU verification

- 2026-11-10T11:31:14+00:00 | Cached completed output, CPU verification: out/phase7_massmatched_gpt2_d000_016_v3.json

- 2026-11-10T11:31:14+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d000_016_v3.json

- 2026-11-10T11:31:23+00:00 | CPU complete; wall_seconds=6.575: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d000_016_v3.json

- 2026-11-10T11:31:23+00:00 | Cached completed output, CPU verification: out/phase8_items_gpt2_s0_historical_v3.json

- 2026-11-10T11:31:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2_s0_historical_v3.json

- 2026-11-10T11:31:31+00:00 | CPU complete; wall_seconds=7.213: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2_s0_historical_v3.json

- 2026-11-10T11:31:31+00:00 | GPU queue/start; flock_pid=29762: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 0 --stop 16

- 2026-11-10T11:35:10+00:00 | V3 CV equality checks: 54 random causal FP32/BF16 cases, all positive grid weights bit equal to legacy | elapsed_seconds=6.738820

- 2026-11-10T12:08:46+00:00 | V3 CV waiting without GPU lock for the already queued original-batch diagnostic

- 2026-11-10T13:20:51+00:00 | V3 matched pilot: gpt2-medium; native/ANOVA/suffix passed; parallel=True, exact=True

- 2026-11-10T13:22:54+00:00 | V3 matched chunk: gpt2-medium; articles 0:16, all twelve arms retained | elapsed_seconds=175.414587 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 0 --stop 16

- 2026-11-10T13:22:57+00:00 | GPU result complete; observed_wait_and_run_seconds=6030.169: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 0 --stop 16

- 2026-11-10T13:22:57+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d000_016_v3.json

- 2026-11-10T13:23:02+00:00 | CPU complete; wall_seconds=5.663: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d000_016_v3.json

- 2026-11-10T13:23:02+00:00 | GPU queue/start; flock_pid=56379: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 0 --variant historical

- 2026-11-10T13:23:29+00:00 | V3 CV original batch diagnostic: {'A': {'old_mid_accuracy': 0.3566666666666667, 'current_position_batched_mid_accuracy': 0.3566666666666667, 'old_counts_reproduced': True, 'n_prediction_differences_from_flat_batches': 0, 'accuracy_by_position': {4: 0.4, 16: 0.38666666666666666, 32: 0.3466666666666667, 48: 0.38, 64: 0.34, 80: 0.36, 96: 0.32666666666666666, 110: 0.3333333333333333}}, 'B': {'old_mid_accuracy': 0.09999999999999999, 'current_position_batched_mid_accuracy': 0.205, 'old_counts_reproduced': False, 'n_prediction_differences_from_flat_batches': 0, 'accuracy_by_position': {7: 0.11333333333333333, 40: 0.16666666666666666, 72: 0.18666666666666668, 105: 0.22666666666666666, 137: 0.22, 170: 0.18666666666666668, 202: 0.24, 235: 0.26666666666666666}}} | elapsed_seconds=28.496136 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase43_cv_batch_diagnostic.py

- 2026-11-10T13:23:31+00:00 | V3 current-generator CV coordinator: 180 short locked jobs; failed historical reproduction retained

- 2026-11-10T13:23:31+00:00 | GPU queue/start; flock_pid=57025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 1.0

- 2026-11-10T13:37:21+00:00 | V3 items GPU: phase8 gpt2-medium s0 historical; 6400 records, no item omitted | elapsed_seconds=128.315042

- 2026-11-10T13:37:24+00:00 | GPU result complete; observed_wait_and_run_seconds=775.034: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 0 --variant historical

- 2026-11-10T13:37:24+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2-medium_s0_historical_v3.json

- 2026-11-10T13:37:29+00:00 | CPU complete; wall_seconds=5.720: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2-medium_s0_historical_v3.json

- 2026-11-10T13:37:29+00:00 | GPU queue/start; flock_pid=72662: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 0 --stop 16

- 2026-11-10T13:38:00+00:00 | V3 CV beta job: gpt2 s0 historical beta=1.0; both full families, lock released after job | elapsed_seconds=32.385859 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 1.0

- 2026-11-10T13:38:03+00:00 | GPU result complete; observed_wait_and_run_seconds=785.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 1.0

- 2026-11-10T13:38:03+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b1.0_v3.json

- 2026-11-10T13:38:09+00:00 | CPU complete; wall_seconds=5.851: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b1.0_v3.json

- 2026-11-10T13:38:09+00:00 | GPU queue/start; flock_pid=73434: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 1.0

- 2026-11-10T13:58:43+00:00 | V3 matched pilot: EleutherAI/pythia-410m; native/ANOVA/suffix passed; parallel=True, exact=True

- 2026-11-10T14:00:53+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 0:16, all twelve arms retained | elapsed_seconds=183.596332 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 0 --stop 16

- 2026-11-10T14:00:54+00:00 | GPU result complete; observed_wait_and_run_seconds=1265.045: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 0 --stop 16

- 2026-11-10T14:00:54+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d000_016_v3.json

- 2026-11-10T14:01:00+00:00 | CPU complete; wall_seconds=5.677: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d000_016_v3.json

- 2026-11-10T14:01:00+00:00 | GPU queue/start; flock_pid=1032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 0 --variant historical

- 2026-11-10T14:02:25+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=1.0; both full families, lock released after job | elapsed_seconds=86.063078 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:02:30+00:00 | GPU result complete; observed_wait_and_run_seconds=1315.048: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:02:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b1.0_v3.json

- 2026-11-10T14:02:36+00:00 | CPU complete; wall_seconds=6.039: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b1.0_v3.json

- 2026-11-10T14:02:36+00:00 | GPU queue/start; flock_pid=3105: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:04:31+00:00 | V3 items GPU: phase8 EleutherAI/pythia-410m s0 historical; 6400 records, no item omitted | elapsed_seconds=119.972030

- 2026-11-10T14:04:38+00:00 | GPU result complete; observed_wait_and_run_seconds=195.024: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 0 --variant historical

- 2026-11-10T14:04:38+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-410m_s0_historical_v3.json

- 2026-11-10T14:04:45+00:00 | CPU complete; wall_seconds=6.546: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-410m_s0_historical_v3.json

- 2026-11-10T14:04:45+00:00 | GPU queue/start; flock_pid=6479: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 0 --stop 16

- 2026-11-10T14:05:58+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=1.0; both full families, lock released after job | elapsed_seconds=80.165697 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:06:01+00:00 | GPU result complete; observed_wait_and_run_seconds=185.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:06:01+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b1.0_v3.json

- 2026-11-10T14:06:13+00:00 | CPU complete; wall_seconds=8.221: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b1.0_v3.json

- 2026-11-10T14:06:13+00:00 | GPU queue/start; flock_pid=9052: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:07:06+00:00 | V3 matched pilot: EleutherAI/pythia-1.4b; native/ANOVA/suffix passed; parallel=True, exact=True

- 2026-11-10T14:09:31+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 0:16, all twelve arms retained | elapsed_seconds=204.076430 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 0 --stop 16

- 2026-11-10T14:09:35+00:00 | GPU result complete; observed_wait_and_run_seconds=260.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 0 --stop 16

- 2026-11-10T14:09:35+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d000_016_v3.json

- 2026-11-10T14:09:42+00:00 | CPU complete; wall_seconds=6.914: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d000_016_v3.json

- 2026-11-10T14:09:42+00:00 | GPU queue/start; flock_pid=13124: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 0 --variant historical

- 2026-11-10T14:13:14+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=1.0; both full families, lock released after job | elapsed_seconds=215.949124 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:13:18+00:00 | GPU result complete; observed_wait_and_run_seconds=385.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:13:18+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b1.0_v3.json

- 2026-11-10T14:13:28+00:00 | CPU complete; wall_seconds=6.438: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b1.0_v3.json

- 2026-11-10T14:13:28+00:00 | GPU queue/start; flock_pid=18869: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:19:20+00:00 | V3 items GPU: phase8 EleutherAI/pythia-1.4b s0 historical; 6400 records, no item omitted | elapsed_seconds=359.236830

- 2026-11-10T14:19:24+00:00 | GPU result complete; observed_wait_and_run_seconds=525.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 0 --variant historical

- 2026-11-10T14:19:24+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-1.4b_s0_historical_v3.json

- 2026-11-10T14:19:33+00:00 | CPU complete; wall_seconds=6.566: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-1.4b_s0_historical_v3.json

- 2026-11-10T14:19:33+00:00 | GPU queue/start; flock_pid=26959: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 0 --stop 16

- 2026-11-10T14:21:13+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=1.0; both full families, lock released after job | elapsed_seconds=105.662649 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:21:19+00:00 | GPU result complete; observed_wait_and_run_seconds=425.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 1.0

- 2026-11-10T14:21:19+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b1.0_v3.json

- 2026-11-10T14:21:26+00:00 | CPU complete; wall_seconds=6.207: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b1.0_v3.json

- 2026-11-10T14:21:26+00:00 | GPU queue/start; flock_pid=29064: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:22:07+00:00 | V3 matched pilot: Qwen/Qwen2.5-0.5B; native/ANOVA/suffix passed; parallel=True, exact=True

- 2026-11-10T14:24:19+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 0:16, all twelve arms retained | elapsed_seconds=179.239694 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 0 --stop 16

- 2026-11-10T14:24:20+00:00 | GPU result complete; observed_wait_and_run_seconds=260.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 0 --stop 16

- 2026-11-10T14:24:20+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d000_016_v3.json

- 2026-11-10T14:24:31+00:00 | CPU complete; wall_seconds=7.326: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d000_016_v3.json

- 2026-11-10T14:24:31+00:00 | GPU queue/start; flock_pid=32493: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical

- 2026-11-10T14:25:00+00:00 | V3 CV beta job: gpt2 s1 historical beta=1.0; both full families, lock released after job | elapsed_seconds=33.033496 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:25:04+00:00 | GPU result complete; observed_wait_and_run_seconds=195.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:25:04+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b1.0_v3.json

- 2026-11-10T14:25:11+00:00 | CPU complete; wall_seconds=7.348: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b1.0_v3.json

- 2026-11-10T14:25:11+00:00 | GPU queue/start; flock_pid=33205: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:32:54+00:00 | V3 items GPU: phase8 Qwen/Qwen2.5-0.5B s0 historical; 6400 records, no item omitted | elapsed_seconds=172.841842

- 2026-11-10T14:33:01+00:00 | GPU result complete; observed_wait_and_run_seconds=460.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical

- 2026-11-10T14:33:01+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s0_historical_v3.json

- 2026-11-10T14:33:08+00:00 | CPU complete; wall_seconds=7.085: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s0_historical_v3.json

- 2026-11-10T14:33:08+00:00 | GPU queue/start; flock_pid=41961: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 0 --stop 16

- 2026-11-10T14:34:29+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=1.0; both full families, lock released after job | elapsed_seconds=86.809669 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:34:33+00:00 | GPU result complete; observed_wait_and_run_seconds=505.037: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:34:33+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b1.0_v3.json

- 2026-11-10T14:34:40+00:00 | CPU complete; wall_seconds=6.908: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b1.0_v3.json

- 2026-11-10T14:34:40+00:00 | GPU queue/start; flock_pid=43527: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:36:59+00:00 | V3 matched pilot: Qwen/Qwen2.5-3B; native/ANOVA/suffix passed; parallel=True, exact=True

- 2026-11-10T14:40:25+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 0:16, all twelve arms retained | elapsed_seconds=293.461366 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 0 --stop 16

- 2026-11-10T14:40:26+00:00 | GPU result complete; observed_wait_and_run_seconds=395.060: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 0 --stop 16

- 2026-11-10T14:40:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d000_016_v3.json

- 2026-11-10T14:40:36+00:00 | CPU complete; wall_seconds=6.836: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d000_016_v3.json

- 2026-11-10T14:40:37+00:00 | GPU queue/start; flock_pid=49852: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 0 --variant historical

- 2026-11-10T14:41:52+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=1.0; both full families, lock released after job | elapsed_seconds=80.090774 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:41:58+00:00 | GPU result complete; observed_wait_and_run_seconds=395.086: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:41:58+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b1.0_v3.json

- 2026-11-10T14:42:05+00:00 | CPU complete; wall_seconds=6.990: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b1.0_v3.json

- 2026-11-10T14:42:05+00:00 | GPU queue/start; flock_pid=51500: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:44:20+00:00 | V3 items GPU: phase11 gpt2-medium s0 historical; 2400 records, no item omitted | elapsed_seconds=111.312785

- 2026-11-10T14:44:22+00:00 | GPU result complete; observed_wait_and_run_seconds=205.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 0 --variant historical

- 2026-11-10T14:44:22+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_gpt2-medium_s0_historical_v3.json

- 2026-11-10T14:44:33+00:00 | CPU complete; wall_seconds=7.765: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_gpt2-medium_s0_historical_v3.json

- 2026-11-10T14:44:33+00:00 | GPU queue/start; flock_pid=54135: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 16 --stop 32

- 2026-11-10T14:48:04+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=1.0; both full families, lock released after job | elapsed_seconds=216.971874 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:48:07+00:00 | GPU result complete; observed_wait_and_run_seconds=325.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:48:07+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b1.0_v3.json

- 2026-11-10T14:48:15+00:00 | CPU complete; wall_seconds=7.755: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b1.0_v3.json

- 2026-11-10T14:48:15+00:00 | GPU queue/start; flock_pid=58215: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:49:15+00:00 | V3 matched chunk: gpt2; articles 16:32, all twelve arms retained | elapsed_seconds=62.229503 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 16 --stop 32

- 2026-11-10T14:49:19+00:00 | GPU result complete; observed_wait_and_run_seconds=260.044: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 16 --stop 32

- 2026-11-10T14:49:19+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d016_032_v3.json

- 2026-11-10T14:49:30+00:00 | CPU complete; wall_seconds=7.037: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d016_032_v3.json

- 2026-11-10T14:49:30+00:00 | GPU queue/start; flock_pid=59557: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 0 --variant historical

- 2026-11-10T14:51:07+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=1.0; both full families, lock released after job | elapsed_seconds=105.056144 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:51:15+00:00 | GPU result complete; observed_wait_and_run_seconds=160.179: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 1.0

- 2026-11-10T14:51:15+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b1.0_v3.json

- 2026-11-10T14:51:22+00:00 | CPU complete; wall_seconds=6.701: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b1.0_v3.json

- 2026-11-10T14:51:22+00:00 | GPU queue/start; flock_pid=61737: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 1.0

- 2026-11-10T14:55:16+00:00 | V3 items GPU: phase11 Qwen/Qwen2.5-3B s0 historical; 2400 records, no item omitted | elapsed_seconds=241.267392

- 2026-11-10T14:55:18+00:00 | GPU result complete; observed_wait_and_run_seconds=315.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 0 --variant historical

- 2026-11-10T14:55:18+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_Qwen__Qwen2.5-3B_s0_historical_v3.json

- 2026-11-10T14:55:25+00:00 | CPU complete; wall_seconds=6.436: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_Qwen__Qwen2.5-3B_s0_historical_v3.json

- 2026-11-10T14:55:25+00:00 | GPU queue/start; flock_pid=66053: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 16 --stop 32

- 2026-11-10T14:56:04+00:00 | V3 CV beta job: gpt2 s2 historical beta=1.0; both full families, lock released after job | elapsed_seconds=32.848133 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 1.0

- 2026-11-10T14:56:12+00:00 | GPU result complete; observed_wait_and_run_seconds=260.023: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 1.0

- 2026-11-10T14:56:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b1.0_v3.json

- 2026-11-10T14:56:20+00:00 | CPU complete; wall_seconds=8.102: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b1.0_v3.json

- 2026-11-10T14:56:20+00:00 | GPU queue/start; flock_pid=67017: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 1.0

- 2026-11-10T14:58:35+00:00 | V3 matched chunk: gpt2-medium; articles 16:32, all twelve arms retained | elapsed_seconds=142.707851 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 16 --stop 32

- 2026-11-10T14:58:40+00:00 | GPU result complete; observed_wait_and_run_seconds=175.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 16 --stop 32

- 2026-11-10T14:58:40+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d016_032_v3.json

- 2026-11-10T14:58:46+00:00 | CPU complete; wall_seconds=6.320: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d016_032_v3.json

- 2026-11-10T14:58:46+00:00 | GPU queue/start; flock_pid=69708: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2 --seed 1 --variant historical

- 2026-11-10T15:00:21+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=1.0; both full families, lock released after job | elapsed_seconds=86.171990 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:00:23+00:00 | GPU result complete; observed_wait_and_run_seconds=220.024: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:00:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b1.0_v3.json

- 2026-11-10T15:00:30+00:00 | CPU complete; wall_seconds=6.819: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b1.0_v3.json

- 2026-11-10T15:00:30+00:00 | GPU queue/start; flock_pid=71547: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:01:17+00:00 | V3 items GPU: phase8 gpt2 s1 historical; 6400 records, no item omitted | elapsed_seconds=48.893135

- 2026-11-10T15:01:23+00:00 | GPU result complete; observed_wait_and_run_seconds=140.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2 --seed 1 --variant historical

- 2026-11-10T15:01:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2_s1_historical_v3.json

- 2026-11-10T15:01:30+00:00 | CPU complete; wall_seconds=7.150: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2_s1_historical_v3.json

- 2026-11-10T15:01:30+00:00 | GPU queue/start; flock_pid=72603: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 16 --stop 32

- 2026-11-10T15:02:44+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=1.0; both full families, lock released after job | elapsed_seconds=79.989197 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:02:52+00:00 | GPU result complete; observed_wait_and_run_seconds=125.024: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:02:52+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b1.0_v3.json

- 2026-11-10T15:02:59+00:00 | CPU complete; wall_seconds=7.233: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b1.0_v3.json

- 2026-11-10T15:02:59+00:00 | GPU queue/start; flock_pid=74260: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:05:16+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 16:32, all twelve arms retained | elapsed_seconds=144.838355 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 16 --stop 32

- 2026-11-10T15:05:18+00:00 | GPU result complete; observed_wait_and_run_seconds=205.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 16 --stop 32

- 2026-11-10T15:05:18+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d016_032_v3.json

- 2026-11-10T15:05:25+00:00 | CPU complete; wall_seconds=6.650: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d016_032_v3.json

- 2026-11-10T15:05:25+00:00 | GPU queue/start; flock_pid=76902: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 1 --variant historical

- 2026-11-10T15:09:23+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=1.0; both full families, lock released after job | elapsed_seconds=215.314154 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:09:27+00:00 | GPU result complete; observed_wait_and_run_seconds=350.046: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:09:27+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b1.0_v3.json

- 2026-11-10T15:09:36+00:00 | CPU complete; wall_seconds=6.604: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b1.0_v3.json

- 2026-11-10T15:09:36+00:00 | GPU queue/start; flock_pid=81311: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:11:39+00:00 | V3 items GPU: phase8 gpt2-medium s1 historical; 6400 records, no item omitted | elapsed_seconds=129.292817

- 2026-11-10T15:11:45+00:00 | GPU result complete; observed_wait_and_run_seconds=340.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 1 --variant historical

- 2026-11-10T15:11:45+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2-medium_s1_historical_v3.json

- 2026-11-10T15:11:51+00:00 | CPU complete; wall_seconds=6.478: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2-medium_s1_historical_v3.json

- 2026-11-10T15:11:51+00:00 | GPU queue/start; flock_pid=83677: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 16 --stop 32

- 2026-11-10T15:19:45+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=1.0; both full families, lock released after job | elapsed_seconds=105.595622 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:19:51+00:00 | GPU result complete; observed_wait_and_run_seconds=555.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 1.0

- 2026-11-10T15:19:51+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b1.0_v3.json

- 2026-11-10T15:19:58+00:00 | CPU complete; wall_seconds=7.763: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b1.0_v3.json

- 2026-11-10T15:19:58+00:00 | GPU queue/start; flock_pid=92644: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:22:23+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 16:32, all twelve arms retained | elapsed_seconds=150.664609 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 16 --stop 32

- 2026-11-10T15:22:30+00:00 | GPU result complete; observed_wait_and_run_seconds=575.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 16 --stop 32

- 2026-11-10T15:22:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d016_032_v3.json

- 2026-11-10T15:22:37+00:00 | CPU complete; wall_seconds=6.972: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d016_032_v3.json

- 2026-11-10T15:22:37+00:00 | GPU queue/start; flock_pid=95408: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 1 --variant historical

- 2026-11-10T15:24:23+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=1.0; both full families, lock released after job | elapsed_seconds=46.337675 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:24:25+00:00 | GPU result complete; observed_wait_and_run_seconds=240.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:24:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b1.0_v3.json

- 2026-11-10T15:24:36+00:00 | CPU complete; wall_seconds=8.073: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b1.0_v3.json

- 2026-11-10T15:24:37+00:00 | GPU queue/start; flock_pid=97733: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:26:49+00:00 | V3 items GPU: phase8 EleutherAI/pythia-410m s1 historical; 6400 records, no item omitted | elapsed_seconds=120.507492

- 2026-11-10T15:26:53+00:00 | GPU result complete; observed_wait_and_run_seconds=230.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 1 --variant historical

- 2026-11-10T15:26:53+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-410m_s1_historical_v3.json

- 2026-11-10T15:27:00+00:00 | CPU complete; wall_seconds=6.716: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-410m_s1_historical_v3.json

- 2026-11-10T15:27:00+00:00 | GPU queue/start; flock_pid=754: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 16 --stop 32

- 2026-11-10T15:27:42+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=1.0; both full families, lock released after job | elapsed_seconds=45.800079 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:27:43+00:00 | GPU result complete; observed_wait_and_run_seconds=170.039: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:27:43+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b1.0_v3.json

- 2026-11-10T15:27:53+00:00 | CPU complete; wall_seconds=6.753: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b1.0_v3.json

- 2026-11-10T15:27:53+00:00 | GPU queue/start; flock_pid=1726: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:31:11+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 16:32, all twelve arms retained | elapsed_seconds=124.912173 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 16 --stop 32

- 2026-11-10T15:31:17+00:00 | GPU result complete; observed_wait_and_run_seconds=230.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 16 --stop 32

- 2026-11-10T15:31:17+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d016_032_v3.json

- 2026-11-10T15:31:24+00:00 | CPU complete; wall_seconds=6.892: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d016_032_v3.json

- 2026-11-10T15:31:24+00:00 | GPU queue/start; flock_pid=5555: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 1 --variant historical

- 2026-11-10T15:32:04+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=1.0; both full families, lock released after job | elapsed_seconds=45.791605 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:32:07+00:00 | GPU result complete; observed_wait_and_run_seconds=230.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 1.0

- 2026-11-10T15:32:07+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b1.0_v3.json

- 2026-11-10T15:32:17+00:00 | CPU complete; wall_seconds=7.261: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b1.0_v3.json

- 2026-11-10T15:32:17+00:00 | GPU queue/start; flock_pid=6436: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:38:10+00:00 | V3 items GPU: phase8 EleutherAI/pythia-1.4b s1 historical; 6400 records, no item omitted | elapsed_seconds=359.286035

- 2026-11-10T15:38:14+00:00 | GPU result complete; observed_wait_and_run_seconds=370.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 1 --variant historical

- 2026-11-10T15:38:14+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-1.4b_s1_historical_v3.json

- 2026-11-10T15:38:24+00:00 | CPU complete; wall_seconds=6.466: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-1.4b_s1_historical_v3.json

- 2026-11-10T15:38:24+00:00 | GPU queue/start; flock_pid=13064: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 16 --stop 32

- 2026-11-10T15:38:56+00:00 | V3 CV beta job: gpt2 s0 historical beta=0.75; both full families, lock released after job | elapsed_seconds=38.302461 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:39:02+00:00 | GPU result complete; observed_wait_and_run_seconds=365.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:39:02+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.75_v3.json

- 2026-11-10T15:39:09+00:00 | CPU complete; wall_seconds=6.529: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.75_v3.json

- 2026-11-10T15:39:09+00:00 | GPU queue/start; flock_pid=13930: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:42:20+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 16:32, all twelve arms retained | elapsed_seconds=197.874126 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 16 --stop 32

- 2026-11-10T15:42:27+00:00 | GPU result complete; observed_wait_and_run_seconds=220.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 16 --stop 32

- 2026-11-10T15:42:27+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d016_032_v3.json

- 2026-11-10T15:42:33+00:00 | CPU complete; wall_seconds=6.401: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d016_032_v3.json

- 2026-11-10T15:42:33+00:00 | GPU queue/start; flock_pid=17546: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical

- 2026-11-10T15:44:07+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=0.75; both full families, lock released after job | elapsed_seconds=100.348061 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:44:14+00:00 | GPU result complete; observed_wait_and_run_seconds=275.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:44:14+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.75_v3.json

- 2026-11-10T15:44:21+00:00 | CPU complete; wall_seconds=7.071: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.75_v3.json

- 2026-11-10T15:44:21+00:00 | GPU queue/start; flock_pid=19502: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:47:45+00:00 | V3 items GPU: phase8 Qwen/Qwen2.5-0.5B s1 historical; 6400 records, no item omitted | elapsed_seconds=172.164788

- 2026-11-10T15:47:52+00:00 | GPU result complete; observed_wait_and_run_seconds=285.033: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical

- 2026-11-10T15:47:52+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s1_historical_v3.json

- 2026-11-10T15:47:57+00:00 | CPU complete; wall_seconds=5.808: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s1_historical_v3.json

- 2026-11-10T15:47:57+00:00 | GPU queue/start; flock_pid=23454: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 32 --stop 48

- 2026-11-10T15:49:25+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=0.75; both full families, lock released after job | elapsed_seconds=93.576499 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:49:29+00:00 | GPU result complete; observed_wait_and_run_seconds=275.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:49:29+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.75_v3.json

- 2026-11-10T15:49:35+00:00 | CPU complete; wall_seconds=5.774: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.75_v3.json

- 2026-11-10T15:49:35+00:00 | GPU queue/start; flock_pid=25336: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:50:22+00:00 | V3 matched chunk: gpt2; articles 32:48, all twelve arms retained | elapsed_seconds=50.068930 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 32 --stop 48

- 2026-11-10T15:50:26+00:00 | GPU result complete; observed_wait_and_run_seconds=135.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 32 --stop 48

- 2026-11-10T15:50:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d032_048_v3.json

- 2026-11-10T15:50:32+00:00 | CPU complete; wall_seconds=6.579: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d032_048_v3.json

- 2026-11-10T15:50:32+00:00 | GPU queue/start; flock_pid=26415: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 1 --variant historical

- 2026-11-10T15:54:17+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=0.75; both full families, lock released after job | elapsed_seconds=228.473898 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:54:22+00:00 | GPU result complete; observed_wait_and_run_seconds=260.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:54:22+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.75_v3.json

- 2026-11-10T15:54:31+00:00 | CPU complete; wall_seconds=5.736: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.75_v3.json

- 2026-11-10T15:54:31+00:00 | GPU queue/start; flock_pid=30696: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:56:15+00:00 | V3 items GPU: phase11 gpt2-medium s1 historical; 2400 records, no item omitted | elapsed_seconds=111.507290

- 2026-11-10T15:56:19+00:00 | GPU result complete; observed_wait_and_run_seconds=310.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 1 --variant historical

- 2026-11-10T15:56:19+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_gpt2-medium_s1_historical_v3.json

- 2026-11-10T15:56:25+00:00 | CPU complete; wall_seconds=5.729: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_gpt2-medium_s1_historical_v3.json

- 2026-11-10T15:56:25+00:00 | GPU queue/start; flock_pid=32822: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 32 --stop 48

- 2026-11-10T15:58:19+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=0.75; both full families, lock released after job | elapsed_seconds=118.008077 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:58:24+00:00 | GPU result complete; observed_wait_and_run_seconds=210.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.75

- 2026-11-10T15:58:24+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.75_v3.json

- 2026-11-10T15:58:30+00:00 | CPU complete; wall_seconds=5.716: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.75_v3.json

- 2026-11-10T15:58:30+00:00 | GPU queue/start; flock_pid=35096: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:00:30+00:00 | V3 matched chunk: gpt2-medium; articles 32:48, all twelve arms retained | elapsed_seconds=124.586242 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 32 --stop 48

- 2026-11-10T16:00:37+00:00 | GPU result complete; observed_wait_and_run_seconds=225.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 32 --stop 48

- 2026-11-10T16:00:37+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d032_048_v3.json

- 2026-11-10T16:00:43+00:00 | CPU complete; wall_seconds=6.005: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d032_048_v3.json

- 2026-11-10T16:00:43+00:00 | GPU queue/start; flock_pid=37538: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 1 --variant historical

- 2026-11-10T16:01:14+00:00 | V3 CV beta job: gpt2 s1 historical beta=0.75; both full families, lock released after job | elapsed_seconds=37.871420 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:01:17+00:00 | GPU result complete; observed_wait_and_run_seconds=150.037: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:01:17+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.75_v3.json

- 2026-11-10T16:01:22+00:00 | CPU complete; wall_seconds=5.718: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.75_v3.json

- 2026-11-10T16:01:22+00:00 | GPU queue/start; flock_pid=38258: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:06:54+00:00 | V3 items GPU: phase11 Qwen/Qwen2.5-3B s1 historical; 2400 records, no item omitted | elapsed_seconds=239.708356

- 2026-11-10T16:06:59+00:00 | GPU result complete; observed_wait_and_run_seconds=340.036: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 1 --variant historical

- 2026-11-10T16:06:59+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_Qwen__Qwen2.5-3B_s1_historical_v3.json

- 2026-11-10T16:07:05+00:00 | CPU complete; wall_seconds=5.661: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_Qwen__Qwen2.5-3B_s1_historical_v3.json

- 2026-11-10T16:07:05+00:00 | GPU queue/start; flock_pid=44442: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 32 --stop 48

- 2026-11-10T16:08:41+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=0.75; both full families, lock released after job | elapsed_seconds=100.433541 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:08:46+00:00 | GPU result complete; observed_wait_and_run_seconds=400.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:08:46+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.75_v3.json

- 2026-11-10T16:08:52+00:00 | CPU complete; wall_seconds=5.991: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.75_v3.json

- 2026-11-10T16:08:52+00:00 | GPU queue/start; flock_pid=46441: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:12:18+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 32:48, all twelve arms retained | elapsed_seconds=133.002735 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 32 --stop 48

- 2026-11-10T16:12:23+00:00 | GPU result complete; observed_wait_and_run_seconds=285.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 32 --stop 48

- 2026-11-10T16:12:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d032_048_v3.json

- 2026-11-10T16:12:29+00:00 | CPU complete; wall_seconds=6.057: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d032_048_v3.json

- 2026-11-10T16:12:29+00:00 | GPU queue/start; flock_pid=50355: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2 --seed 2 --variant historical

- 2026-11-10T16:13:57+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=0.75; both full families, lock released after job | elapsed_seconds=93.297391 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:14:05+00:00 | GPU result complete; observed_wait_and_run_seconds=280.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:14:05+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.75_v3.json

- 2026-11-10T16:14:11+00:00 | CPU complete; wall_seconds=6.150: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.75_v3.json

- 2026-11-10T16:14:11+00:00 | GPU queue/start; flock_pid=52193: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:15:36+00:00 | V3 items GPU: phase8 gpt2 s2 historical; 6400 records, no item omitted | elapsed_seconds=48.413833

- 2026-11-10T16:15:39+00:00 | GPU result complete; observed_wait_and_run_seconds=170.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2 --seed 2 --variant historical

- 2026-11-10T16:15:39+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2_s2_historical_v3.json

- 2026-11-10T16:15:46+00:00 | CPU complete; wall_seconds=6.383: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2_s2_historical_v3.json

- 2026-11-10T16:15:46+00:00 | GPU queue/start; flock_pid=53862: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 32 --stop 48

- 2026-11-10T16:19:31+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=0.75; both full families, lock released after job | elapsed_seconds=228.306656 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:19:35+00:00 | GPU result complete; observed_wait_and_run_seconds=290.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:19:35+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.75_v3.json

- 2026-11-10T16:19:40+00:00 | CPU complete; wall_seconds=5.807: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.75_v3.json

- 2026-11-10T16:19:40+00:00 | GPU queue/start; flock_pid=58135: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:22:58+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 32:48, all twelve arms retained | elapsed_seconds=140.913677 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 32 --stop 48

- 2026-11-10T16:23:04+00:00 | GPU result complete; observed_wait_and_run_seconds=395.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 32 --stop 48

- 2026-11-10T16:23:04+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d032_048_v3.json

- 2026-11-10T16:23:10+00:00 | CPU complete; wall_seconds=5.992: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d032_048_v3.json

- 2026-11-10T16:23:10+00:00 | GPU queue/start; flock_pid=61957: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 2 --variant historical

- 2026-11-10T16:25:02+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=0.75; both full families, lock released after job | elapsed_seconds=117.749021 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:25:09+00:00 | GPU result complete; observed_wait_and_run_seconds=295.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.75

- 2026-11-10T16:25:09+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.75_v3.json

- 2026-11-10T16:25:15+00:00 | CPU complete; wall_seconds=5.975: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.75_v3.json

- 2026-11-10T16:25:15+00:00 | GPU queue/start; flock_pid=64286: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:29:00+00:00 | V3 items GPU: phase8 gpt2-medium s2 historical; 6400 records, no item omitted | elapsed_seconds=128.119346

- 2026-11-10T16:29:07+00:00 | GPU result complete; observed_wait_and_run_seconds=320.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 2 --variant historical

- 2026-11-10T16:29:07+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2-medium_s2_historical_v3.json

- 2026-11-10T16:29:13+00:00 | CPU complete; wall_seconds=6.266: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_gpt2-medium_s2_historical_v3.json

- 2026-11-10T16:29:13+00:00 | GPU queue/start; flock_pid=68594: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 32 --stop 48

- 2026-11-10T16:29:44+00:00 | V3 CV beta job: gpt2 s2 historical beta=0.75; both full families, lock released after job | elapsed_seconds=38.075793 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:29:46+00:00 | GPU result complete; observed_wait_and_run_seconds=245.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:29:46+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.75_v3.json

- 2026-11-10T16:29:52+00:00 | CPU complete; wall_seconds=5.778: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.75_v3.json

- 2026-11-10T16:29:52+00:00 | GPU queue/start; flock_pid=69361: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:32:51+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 32:48, all twelve arms retained | elapsed_seconds=110.356166 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 32 --stop 48

- 2026-11-10T16:32:57+00:00 | GPU result complete; observed_wait_and_run_seconds=200.038: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 32 --stop 48

- 2026-11-10T16:32:57+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d032_048_v3.json

- 2026-11-10T16:33:02+00:00 | CPU complete; wall_seconds=5.809: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d032_048_v3.json

- 2026-11-10T16:33:02+00:00 | GPU queue/start; flock_pid=72835: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 2 --variant historical

- 2026-11-10T16:34:38+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=0.75; both full families, lock released after job | elapsed_seconds=100.317546 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:34:42+00:00 | GPU result complete; observed_wait_and_run_seconds=260.039: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:34:42+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.75_v3.json

- 2026-11-10T16:34:48+00:00 | CPU complete; wall_seconds=5.872: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.75_v3.json

- 2026-11-10T16:34:48+00:00 | GPU queue/start; flock_pid=74729: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:51:54+00:00 | V3 items GPU: phase8 EleutherAI/pythia-410m s2 historical; 6400 records, no item omitted | elapsed_seconds=119.190762

- 2026-11-10T16:52:01+00:00 | GPU result complete; observed_wait_and_run_seconds=1025.039: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 2 --variant historical

- 2026-11-10T16:52:01+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-410m_s2_historical_v3.json

- 2026-11-10T16:52:07+00:00 | CPU complete; wall_seconds=6.106: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-410m_s2_historical_v3.json

- 2026-11-10T16:52:07+00:00 | GPU queue/start; flock_pid=93253: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 32 --stop 48

- 2026-11-10T16:53:34+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=0.75; both full families, lock released after job | elapsed_seconds=93.452502 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:53:37+00:00 | GPU result complete; observed_wait_and_run_seconds=1015.042: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:53:37+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.75_v3.json

- 2026-11-10T16:53:42+00:00 | CPU complete; wall_seconds=5.780: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.75_v3.json

- 2026-11-10T16:53:42+00:00 | GPU queue/start; flock_pid=94902: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.75

- 2026-11-10T16:56:47+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 32:48, all twelve arms retained | elapsed_seconds=187.503100 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 32 --stop 48

- 2026-11-10T16:56:52+00:00 | GPU result complete; observed_wait_and_run_seconds=255.024: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 32 --stop 48

- 2026-11-10T16:56:52+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d032_048_v3.json

- 2026-11-10T16:56:58+00:00 | CPU complete; wall_seconds=6.397: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d032_048_v3.json

- 2026-11-10T16:56:58+00:00 | GPU queue/start; flock_pid=98514: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 2 --variant historical

- 2026-11-10T17:00:42+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=0.75; both full families, lock released after job | elapsed_seconds=228.071630 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.75

- 2026-11-10T17:00:46+00:00 | GPU result complete; observed_wait_and_run_seconds=380.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.75

- 2026-11-10T17:00:46+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.75_v3.json

- 2026-11-10T17:00:52+00:00 | CPU complete; wall_seconds=5.898: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.75_v3.json

- 2026-11-10T17:00:52+00:00 | GPU queue/start; flock_pid=3225: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.75

- 2026-11-10T17:28:40+00:00 | V3 items GPU: phase8 EleutherAI/pythia-1.4b s2 historical; 6400 records, no item omitted | elapsed_seconds=358.810234

- 2026-11-10T17:28:45+00:00 | GPU result complete; observed_wait_and_run_seconds=1810.063: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 2 --variant historical

- 2026-11-10T17:28:45+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-1.4b_s2_historical_v3.json

- 2026-11-10T17:28:52+00:00 | CPU complete; wall_seconds=7.305: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_EleutherAI__pythia-1.4b_s2_historical_v3.json

- 2026-11-10T17:28:52+00:00 | GPU queue/start; flock_pid=35174: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 48 --stop 64

- 2026-11-10T17:30:44+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=0.75; both full families, lock released after job | elapsed_seconds=118.073792 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.75

- 2026-11-10T17:30:50+00:00 | GPU result complete; observed_wait_and_run_seconds=1725.059: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.75

- 2026-11-10T17:30:50+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.75_v3.json

- 2026-11-10T17:30:57+00:00 | CPU complete; wall_seconds=6.814: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.75_v3.json

- 2026-11-10T17:30:57+00:00 | GPU queue/start; flock_pid=37770: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:43:00+00:00 | V3 matched chunk: gpt2; articles 48:64, all twelve arms retained | elapsed_seconds=48.977766 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 48 --stop 64

- 2026-11-10T17:43:03+00:00 | GPU result complete; observed_wait_and_run_seconds=850.049: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 48 --stop 64

- 2026-11-10T17:43:03+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d048_064_v3.json

- 2026-11-10T17:43:09+00:00 | CPU complete; wall_seconds=6.525: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d048_064_v3.json

- 2026-11-10T17:43:09+00:00 | GPU queue/start; flock_pid=53592: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical

- 2026-11-10T17:43:41+00:00 | V3 beta0 item intervals: Five completed seed0 probes; counts and exact McNemar unchanged, paired item CIs added without inference | elapsed_seconds=1.229136 | command: .venv/Scripts/python.exe -B beta0_statistics_v3.py

- 2026-11-10T17:44:02+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=0.75; both full families, lock released after job | elapsed_seconds=55.325005 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:44:07+00:00 | GPU result complete; observed_wait_and_run_seconds=790.050: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:44:07+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.75_v3.json

- 2026-11-10T17:44:14+00:00 | CPU complete; wall_seconds=6.554: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.75_v3.json

- 2026-11-10T17:44:14+00:00 | GPU queue/start; flock_pid=54938: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:47:00+00:00 | V3 items GPU: phase8 Qwen/Qwen2.5-0.5B s2 historical; 6400 records, no item omitted | elapsed_seconds=172.101386

- 2026-11-10T17:47:04+00:00 | GPU result complete; observed_wait_and_run_seconds=235.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical

- 2026-11-10T17:47:04+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s2_historical_v3.json

- 2026-11-10T17:47:12+00:00 | CPU complete; wall_seconds=7.053: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s2_historical_v3.json

- 2026-11-10T17:47:12+00:00 | GPU queue/start; flock_pid=58479: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 48 --stop 64

- 2026-11-10T17:48:02+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=0.75; both full families, lock released after job | elapsed_seconds=55.593222 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:48:04+00:00 | GPU result complete; observed_wait_and_run_seconds=230.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:48:04+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.75_v3.json

- 2026-11-10T17:48:10+00:00 | CPU complete; wall_seconds=6.287: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.75_v3.json

- 2026-11-10T17:48:10+00:00 | GPU queue/start; flock_pid=59699: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:50:20+00:00 | V3 matched chunk: gpt2-medium; articles 48:64, all twelve arms retained | elapsed_seconds=124.541257 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 48 --stop 64

- 2026-11-10T17:50:22+00:00 | GPU result complete; observed_wait_and_run_seconds=190.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 48 --stop 64

- 2026-11-10T17:50:22+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d048_064_v3.json

- 2026-11-10T17:50:28+00:00 | CPU complete; wall_seconds=6.334: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d048_064_v3.json

- 2026-11-10T17:50:28+00:00 | GPU queue/start; flock_pid=62395: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 2 --variant historical

- 2026-11-10T17:51:22+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=0.75; both full families, lock released after job | elapsed_seconds=55.618001 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:51:25+00:00 | GPU result complete; observed_wait_and_run_seconds=195.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.75

- 2026-11-10T17:51:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.75_v3.json

- 2026-11-10T17:51:33+00:00 | CPU complete; wall_seconds=7.361: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.75_v3.json

- 2026-11-10T17:51:33+00:00 | GPU queue/start; flock_pid=63749: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.5

- 2026-11-10T17:53:31+00:00 | V3 items GPU: phase11 gpt2-medium s2 historical; 2400 records, no item omitted | elapsed_seconds=111.010212

- 2026-11-10T17:53:33+00:00 | GPU result complete; observed_wait_and_run_seconds=185.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 2 --variant historical

- 2026-11-10T17:53:33+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_gpt2-medium_s2_historical_v3.json

- 2026-11-10T17:53:39+00:00 | CPU complete; wall_seconds=6.301: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_gpt2-medium_s2_historical_v3.json

- 2026-11-10T17:53:39+00:00 | GPU queue/start; flock_pid=66257: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 48 --stop 64

- 2026-11-10T17:54:15+00:00 | V3 CV beta job: gpt2 s0 historical beta=0.5; both full families, lock released after job | elapsed_seconds=37.919851 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.5

- 2026-11-10T17:54:18+00:00 | GPU result complete; observed_wait_and_run_seconds=165.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.5

- 2026-11-10T17:54:18+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.5_v3.json

- 2026-11-10T17:54:24+00:00 | CPU complete; wall_seconds=6.367: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.5_v3.json

- 2026-11-10T17:54:24+00:00 | GPU queue/start; flock_pid=67141: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.5

- 2026-11-10T17:56:42+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 48:64, all twelve arms retained | elapsed_seconds=131.428402 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 48 --stop 64

- 2026-11-10T17:56:45+00:00 | GPU result complete; observed_wait_and_run_seconds=185.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 48 --stop 64

- 2026-11-10T17:56:45+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d048_064_v3.json

- 2026-11-10T17:56:51+00:00 | CPU complete; wall_seconds=6.266: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d048_064_v3.json

- 2026-11-10T17:56:51+00:00 | GPU queue/start; flock_pid=69952: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 2 --variant historical

- 2026-11-10T17:58:28+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=0.5; both full families, lock released after job | elapsed_seconds=100.053543 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.5

- 2026-11-10T17:58:30+00:00 | GPU result complete; observed_wait_and_run_seconds=245.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.5

- 2026-11-10T17:58:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.5_v3.json

- 2026-11-10T17:58:36+00:00 | CPU complete; wall_seconds=6.316: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.5_v3.json

- 2026-11-10T17:58:36+00:00 | GPU queue/start; flock_pid=72042: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:02:44+00:00 | V3 items GPU: phase11 Qwen/Qwen2.5-3B s2 historical; 2400 records, no item omitted | elapsed_seconds=239.754153

- 2026-11-10T18:02:46+00:00 | GPU result complete; observed_wait_and_run_seconds=355.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 2 --variant historical

- 2026-11-10T18:02:46+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_Qwen__Qwen2.5-3B_s2_historical_v3.json

- 2026-11-10T18:02:53+00:00 | CPU complete; wall_seconds=6.526: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase11_items_Qwen__Qwen2.5-3B_s2_historical_v3.json

- 2026-11-10T18:02:53+00:00 | GPU queue/start; flock_pid=77304: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 48 --stop 64

- 2026-11-10T18:04:24+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=0.5; both full families, lock released after job | elapsed_seconds=93.522770 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:04:26+00:00 | GPU result complete; observed_wait_and_run_seconds=350.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:04:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.5_v3.json

- 2026-11-10T18:04:33+00:00 | CPU complete; wall_seconds=6.383: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.5_v3.json

- 2026-11-10T18:04:33+00:00 | GPU queue/start; flock_pid=79381: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:07:01+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 48:64, all twelve arms retained | elapsed_seconds=140.829583 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 48 --stop 64

- 2026-11-10T18:07:03+00:00 | GPU result complete; observed_wait_and_run_seconds=250.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 48 --stop 64

- 2026-11-10T18:07:03+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d048_064_v3.json

- 2026-11-10T18:07:10+00:00 | CPU complete; wall_seconds=7.087: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d048_064_v3.json

- 2026-11-10T18:07:10+00:00 | GPU queue/start; flock_pid=82484: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16

- 2026-11-10T18:10:56+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=0.5; both full families, lock released after job | elapsed_seconds=228.061035 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:10:58+00:00 | GPU result complete; observed_wait_and_run_seconds=385.038: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:10:58+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.5_v3.json

- 2026-11-10T18:11:04+00:00 | CPU complete; wall_seconds=6.375: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.5_v3.json

- 2026-11-10T18:11:04+00:00 | GPU queue/start; flock_pid=87205: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:12:17+00:00 | V3 items GPU: phase8 Qwen/Qwen2.5-0.5B s0 standard_bf16; 6400 records, no item omitted | elapsed_seconds=64.961088

- 2026-11-10T18:12:20+00:00 | GPU result complete; observed_wait_and_run_seconds=310.047: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16

- 2026-11-10T18:12:20+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_v3.json

- 2026-11-10T18:12:27+00:00 | CPU complete; wall_seconds=6.617: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_v3.json

- 2026-11-10T18:12:27+00:00 | GPU queue/start; flock_pid=88812: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 48 --stop 64

- 2026-11-10T18:14:21+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=0.5; both full families, lock released after job | elapsed_seconds=117.689592 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:14:25+00:00 | GPU result complete; observed_wait_and_run_seconds=200.033: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.5

- 2026-11-10T18:14:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.5_v3.json

- 2026-11-10T18:14:31+00:00 | CPU complete; wall_seconds=6.494: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.5_v3.json

- 2026-11-10T18:14:31+00:00 | GPU queue/start; flock_pid=91269: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:19:32+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 48:64, all twelve arms retained | elapsed_seconds=110.322608 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 48 --stop 64

- 2026-11-10T18:19:38+00:00 | GPU result complete; observed_wait_and_run_seconds=430.036: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 48 --stop 64

- 2026-11-10T18:19:38+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d048_064_v3.json

- 2026-11-10T18:19:44+00:00 | CPU complete; wall_seconds=6.643: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d048_064_v3.json

- 2026-11-10T18:19:44+00:00 | GPU queue/start; flock_pid=97717: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16

- 2026-11-10T18:20:16+00:00 | V3 CV beta job: gpt2 s1 historical beta=0.5; both full families, lock released after job | elapsed_seconds=37.806544 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:20:22+00:00 | GPU result complete; observed_wait_and_run_seconds=350.038: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:20:22+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.5_v3.json

- 2026-11-10T18:20:28+00:00 | CPU complete; wall_seconds=6.689: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.5_v3.json

- 2026-11-10T18:20:28+00:00 | GPU queue/start; flock_pid=98583: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:22:38+00:00 | V3 items GPU: phase8 Qwen/Qwen2.5-0.5B s1 standard_bf16; 6400 records, no item omitted | elapsed_seconds=64.896195

- 2026-11-10T18:22:40+00:00 | GPU result complete; observed_wait_and_run_seconds=175.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16

- 2026-11-10T18:22:40+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_v3.json

- 2026-11-10T18:22:46+00:00 | CPU complete; wall_seconds=6.268: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_v3.json

- 2026-11-10T18:22:46+00:00 | GPU queue/start; flock_pid=1685: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 48 --stop 64

- 2026-11-10T18:24:25+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=0.5; both full families, lock released after job | elapsed_seconds=100.338927 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:24:29+00:00 | GPU result complete; observed_wait_and_run_seconds=240.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:24:29+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.5_v3.json

- 2026-11-10T18:24:35+00:00 | CPU complete; wall_seconds=6.706: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.5_v3.json

- 2026-11-10T18:24:35+00:00 | GPU queue/start; flock_pid=3921: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:29:53+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 48:64, all twelve arms retained | elapsed_seconds=186.519360 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 48 --stop 64

- 2026-11-10T18:29:56+00:00 | GPU result complete; observed_wait_and_run_seconds=430.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 48 --stop 64

- 2026-11-10T18:29:56+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d048_064_v3.json

- 2026-11-10T18:30:03+00:00 | CPU complete; wall_seconds=6.505: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d048_064_v3.json

- 2026-11-10T18:30:03+00:00 | GPU queue/start; flock_pid=10539: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16

- 2026-11-10T18:31:33+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=0.5; both full families, lock released after job | elapsed_seconds=93.217379 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:31:36+00:00 | GPU result complete; observed_wait_and_run_seconds=420.069: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:31:36+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.5_v3.json

- 2026-11-10T18:31:43+00:00 | CPU complete; wall_seconds=6.555: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.5_v3.json

- 2026-11-10T18:31:43+00:00 | GPU queue/start; flock_pid=12564: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:34:21+00:00 | V3 items GPU: phase8 Qwen/Qwen2.5-0.5B s2 standard_bf16; 6400 records, no item omitted | elapsed_seconds=64.892456

- 2026-11-10T18:34:23+00:00 | GPU result complete; observed_wait_and_run_seconds=260.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16

- 2026-11-10T18:34:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_v3.json

- 2026-11-10T18:34:31+00:00 | CPU complete; wall_seconds=7.435: .venv/Scripts/python.exe -B phase40_v3_checks.py --items-job out/phase8_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_v3.json

- 2026-11-10T18:34:31+00:00 | CPU start: .venv/Scripts/python.exe -B phase38_paired_items.py --aggregate-only

- 2026-11-10T18:34:44+00:00 | V3 paired item statistics: probe five models + KV two models, three seeds; exact historical counts; paired permutations and prespecified Holm7 | elapsed_seconds=7.562730 | command: .venv/Scripts/python.exe -B phase38_paired_items.py --aggregate-only

- 2026-11-10T18:34:45+00:00 | CPU complete; wall_seconds=13.722: .venv/Scripts/python.exe -B phase38_paired_items.py --aggregate-only

- 2026-11-10T18:34:45+00:00 | GPU queue/start; flock_pid=16298: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 64 --stop 80

- 2026-11-10T18:38:17+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=0.5; both full families, lock released after job | elapsed_seconds=229.513588 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:38:18+00:00 | GPU result complete; observed_wait_and_run_seconds=395.110: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:38:18+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.5_v3.json

- 2026-11-10T18:38:25+00:00 | CPU complete; wall_seconds=6.460: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.5_v3.json

- 2026-11-10T18:38:25+00:00 | GPU queue/start; flock_pid=20714: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:40:54+00:00 | V3 matched chunk: gpt2; articles 64:80, all twelve arms retained | elapsed_seconds=49.208952 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 64 --stop 80

- 2026-11-10T18:40:55+00:00 | GPU result complete; observed_wait_and_run_seconds=370.033: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 64 --stop 80

- 2026-11-10T18:40:55+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d064_080_v3.json

- 2026-11-10T18:41:02+00:00 | CPU complete; wall_seconds=6.654: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d064_080_v3.json

- 2026-11-10T18:41:02+00:00 | GPU queue/start; flock_pid=23947: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 64 --stop 80

- 2026-11-10T18:42:58+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=0.5; both full families, lock released after job | elapsed_seconds=117.390463 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:43:00+00:00 | GPU result complete; observed_wait_and_run_seconds=275.041: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.5

- 2026-11-10T18:43:00+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.5_v3.json

- 2026-11-10T18:43:07+00:00 | CPU complete; wall_seconds=6.604: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.5_v3.json

- 2026-11-10T18:43:07+00:00 | GPU queue/start; flock_pid=26561: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.5

- 2026-11-10T18:47:24+00:00 | V3 matched chunk: gpt2-medium; articles 64:80, all twelve arms retained | elapsed_seconds=132.846783 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 64 --stop 80

- 2026-11-10T18:47:28+00:00 | GPU result complete; observed_wait_and_run_seconds=385.046: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 64 --stop 80

- 2026-11-10T18:47:28+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d064_080_v3.json

- 2026-11-10T18:47:34+00:00 | CPU complete; wall_seconds=6.806: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d064_080_v3.json

- 2026-11-10T18:47:34+00:00 | GPU queue/start; flock_pid=31983: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 64 --stop 80

- 2026-11-10T18:48:08+00:00 | V3 CV beta job: gpt2 s2 historical beta=0.5; both full families, lock released after job | elapsed_seconds=38.030598 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.5

- 2026-11-10T18:48:12+00:00 | GPU result complete; observed_wait_and_run_seconds=305.040: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.5

- 2026-11-10T18:48:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.5_v3.json

- 2026-11-10T18:48:19+00:00 | CPU complete; wall_seconds=6.813: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.5_v3.json

- 2026-11-10T18:48:19+00:00 | GPU queue/start; flock_pid=32916: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.5

- 2026-11-10T18:51:48+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 64:80, all twelve arms retained | elapsed_seconds=133.180833 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 64 --stop 80

- 2026-11-10T18:51:50+00:00 | GPU result complete; observed_wait_and_run_seconds=255.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 64 --stop 80

- 2026-11-10T18:51:50+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d064_080_v3.json

- 2026-11-10T18:51:56+00:00 | CPU complete; wall_seconds=6.354: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d064_080_v3.json

- 2026-11-10T18:51:56+00:00 | GPU queue/start; flock_pid=37233: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 64 --stop 80

- 2026-11-10T18:53:35+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=0.5; both full families, lock released after job | elapsed_seconds=100.318533 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.5

- 2026-11-10T18:53:40+00:00 | GPU result complete; observed_wait_and_run_seconds=320.041: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.5

- 2026-11-10T18:53:40+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.5_v3.json

- 2026-11-10T18:53:46+00:00 | CPU complete; wall_seconds=6.550: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.5_v3.json

- 2026-11-10T18:53:47+00:00 | GPU queue/start; flock_pid=39492: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.5

- 2026-11-10T18:59:24+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 64:80, all twelve arms retained | elapsed_seconds=141.191531 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 64 --stop 80

- 2026-11-10T18:59:27+00:00 | GPU result complete; observed_wait_and_run_seconds=450.051: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 64 --stop 80

- 2026-11-10T18:59:27+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d064_080_v3.json

- 2026-11-10T18:59:34+00:00 | CPU complete; wall_seconds=6.820: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d064_080_v3.json

- 2026-11-10T18:59:34+00:00 | GPU queue/start; flock_pid=46426: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 64 --stop 80

- 2026-11-10T19:01:04+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=0.5; both full families, lock released after job | elapsed_seconds=93.311793 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.5

- 2026-11-10T19:01:08+00:00 | GPU result complete; observed_wait_and_run_seconds=440.134: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.5

- 2026-11-10T19:01:08+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.5_v3.json

- 2026-11-10T19:01:15+00:00 | CPU complete; wall_seconds=7.113: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.5_v3.json

- 2026-11-10T19:01:15+00:00 | GPU queue/start; flock_pid=48582: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.5

- 2026-11-10T19:05:58+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 64:80, all twelve arms retained | elapsed_seconds=111.505325 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 64 --stop 80

- 2026-11-10T19:06:00+00:00 | GPU result complete; observed_wait_and_run_seconds=385.039: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 64 --stop 80

- 2026-11-10T19:06:00+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d064_080_v3.json

- 2026-11-10T19:06:07+00:00 | CPU complete; wall_seconds=6.740: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d064_080_v3.json

- 2026-11-10T19:06:07+00:00 | GPU queue/start; flock_pid=54431: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 64 --stop 80

- 2026-11-10T19:09:53+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=0.5; both full families, lock released after job | elapsed_seconds=228.018430 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.5

- 2026-11-10T19:09:56+00:00 | GPU result complete; observed_wait_and_run_seconds=520.034: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.5

- 2026-11-10T19:09:56+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.5_v3.json

- 2026-11-10T19:10:02+00:00 | CPU complete; wall_seconds=6.510: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.5_v3.json

- 2026-11-10T19:10:02+00:00 | GPU queue/start; flock_pid=59167: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.5

- 2026-11-10T19:18:01+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 64:80, all twelve arms retained | elapsed_seconds=185.401772 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 64 --stop 80

- 2026-11-10T19:18:03+00:00 | GPU result complete; observed_wait_and_run_seconds=715.055: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 64 --stop 80

- 2026-11-10T19:18:03+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d064_080_v3.json

- 2026-11-10T19:18:10+00:00 | CPU complete; wall_seconds=6.749: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d064_080_v3.json

- 2026-11-10T19:18:10+00:00 | GPU queue/start; flock_pid=68922: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 80 --stop 96

- 2026-11-10T19:20:04+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=0.5; both full families, lock released after job | elapsed_seconds=117.499132 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.5

- 2026-11-10T19:20:09+00:00 | GPU result complete; observed_wait_and_run_seconds=605.038: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.5

- 2026-11-10T19:20:09+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.5_v3.json

- 2026-11-10T19:20:15+00:00 | CPU complete; wall_seconds=6.444: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.5_v3.json

- 2026-11-10T19:20:15+00:00 | GPU queue/start; flock_pid=71394: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:21:00+00:00 | V3 matched chunk: gpt2; articles 80:96, all twelve arms retained | elapsed_seconds=48.985785 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 80 --stop 96

- 2026-11-10T19:21:05+00:00 | GPU result complete; observed_wait_and_run_seconds=175.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 80 --stop 96

- 2026-11-10T19:21:05+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d080_096_v3.json

- 2026-11-10T19:21:13+00:00 | CPU complete; wall_seconds=7.158: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d080_096_v3.json

- 2026-11-10T19:21:13+00:00 | GPU queue/start; flock_pid=73006: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 80 --stop 96

- 2026-11-10T19:22:02+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=0.5; both full families, lock released after job | elapsed_seconds=55.925119 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:22:06+00:00 | GPU result complete; observed_wait_and_run_seconds=110.123: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:22:06+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.5_v3.json

- 2026-11-10T19:22:12+00:00 | CPU complete; wall_seconds=6.340: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.5_v3.json

- 2026-11-10T19:22:12+00:00 | GPU queue/start; flock_pid=74749: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:24:12+00:00 | V3 matched chunk: gpt2-medium; articles 80:96, all twelve arms retained | elapsed_seconds=123.798942 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 80 --stop 96

- 2026-11-10T19:24:13+00:00 | GPU result complete; observed_wait_and_run_seconds=180.033: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 80 --stop 96

- 2026-11-10T19:24:13+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d080_096_v3.json

- 2026-11-10T19:24:19+00:00 | CPU complete; wall_seconds=6.285: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d080_096_v3.json

- 2026-11-10T19:24:19+00:00 | GPU queue/start; flock_pid=77242: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 80 --stop 96

- 2026-11-10T19:25:13+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=0.5; both full families, lock released after job | elapsed_seconds=55.026420 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:25:17+00:00 | GPU result complete; observed_wait_and_run_seconds=185.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:25:17+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.5_v3.json

- 2026-11-10T19:25:24+00:00 | CPU complete; wall_seconds=6.619: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.5_v3.json

- 2026-11-10T19:25:24+00:00 | GPU queue/start; flock_pid=78662: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:27:30+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 80:96, all twelve arms retained | elapsed_seconds=130.700096 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 80 --stop 96

- 2026-11-10T19:27:35+00:00 | GPU result complete; observed_wait_and_run_seconds=195.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 80 --stop 96

- 2026-11-10T19:27:35+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d080_096_v3.json

- 2026-11-10T19:27:42+00:00 | CPU complete; wall_seconds=6.808: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d080_096_v3.json

- 2026-11-10T19:27:42+00:00 | GPU queue/start; flock_pid=81312: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 80 --stop 96

- 2026-11-10T19:28:33+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=0.5; both full families, lock released after job | elapsed_seconds=56.951495 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:28:35+00:00 | GPU result complete; observed_wait_and_run_seconds=190.033: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.5

- 2026-11-10T19:28:35+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.5_v3.json

- 2026-11-10T19:28:42+00:00 | CPU complete; wall_seconds=7.059: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.5_v3.json

- 2026-11-10T19:28:42+00:00 | GPU queue/start; flock_pid=82603: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:31:02+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 80:96, all twelve arms retained | elapsed_seconds=142.747707 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 80 --stop 96

- 2026-11-10T19:31:07+00:00 | GPU result complete; observed_wait_and_run_seconds=205.037: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 80 --stop 96

- 2026-11-10T19:31:07+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d080_096_v3.json

- 2026-11-10T19:31:14+00:00 | CPU complete; wall_seconds=7.139: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d080_096_v3.json

- 2026-11-10T19:31:14+00:00 | GPU queue/start; flock_pid=85997: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 80 --stop 96

- 2026-11-10T19:31:48+00:00 | V3 CV beta job: gpt2 s0 historical beta=0.35; both full families, lock released after job | elapsed_seconds=38.463079 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:31:52+00:00 | GPU result complete; observed_wait_and_run_seconds=190.045: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:31:52+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.35_v3.json

- 2026-11-10T19:31:59+00:00 | CPU complete; wall_seconds=6.727: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.35_v3.json

- 2026-11-10T19:31:59+00:00 | GPU queue/start; flock_pid=87072: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:36:41+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 80:96, all twelve arms retained | elapsed_seconds=116.812364 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 80 --stop 96

- 2026-11-10T19:36:45+00:00 | GPU result complete; observed_wait_and_run_seconds=330.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 80 --stop 96

- 2026-11-10T19:36:45+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d080_096_v3.json

- 2026-11-10T19:36:52+00:00 | CPU complete; wall_seconds=6.551: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d080_096_v3.json

- 2026-11-10T19:36:52+00:00 | GPU queue/start; flock_pid=92397: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 80 --stop 96

- 2026-11-10T19:38:31+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=0.35; both full families, lock released after job | elapsed_seconds=103.849349 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:38:35+00:00 | GPU result complete; observed_wait_and_run_seconds=395.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:38:35+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.35_v3.json

- 2026-11-10T19:38:43+00:00 | CPU complete; wall_seconds=7.635: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.35_v3.json

- 2026-11-10T19:38:43+00:00 | GPU queue/start; flock_pid=94381: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:48:42+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 80:96, all twelve arms retained | elapsed_seconds=187.965033 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 80 --stop 96

- 2026-11-10T19:48:44+00:00 | GPU result complete; observed_wait_and_run_seconds=710.064: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 80 --stop 96

- 2026-11-10T19:48:44+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d080_096_v3.json

- 2026-11-10T19:48:50+00:00 | CPU complete; wall_seconds=6.465: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d080_096_v3.json

- 2026-11-10T19:48:50+00:00 | GPU queue/start; flock_pid=5806: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 96 --stop 112

- 2026-11-10T19:50:22+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=0.35; both full families, lock released after job | elapsed_seconds=93.714476 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:50:25+00:00 | GPU result complete; observed_wait_and_run_seconds=700.167: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:50:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.35_v3.json

- 2026-11-10T19:50:31+00:00 | CPU complete; wall_seconds=6.605: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.35_v3.json

- 2026-11-10T19:50:31+00:00 | GPU queue/start; flock_pid=7607: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:55:30+00:00 | V3 matched chunk: gpt2; articles 96:112, all twelve arms retained | elapsed_seconds=50.768014 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 96 --stop 112

- 2026-11-10T19:55:32+00:00 | GPU result complete; observed_wait_and_run_seconds=400.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 96 --stop 112

- 2026-11-10T19:55:32+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d096_112_v3.json

- 2026-11-10T19:55:39+00:00 | CPU complete; wall_seconds=7.205: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d096_112_v3.json

- 2026-11-10T19:55:39+00:00 | GPU queue/start; flock_pid=13271: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 96 --stop 112

- 2026-11-10T19:59:33+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=0.35; both full families, lock released after job | elapsed_seconds=235.772562 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:59:38+00:00 | GPU result complete; observed_wait_and_run_seconds=545.135: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.35

- 2026-11-10T19:59:38+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.35_v3.json

- 2026-11-10T19:59:48+00:00 | CPU complete; wall_seconds=9.276: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.35_v3.json

- 2026-11-10T19:59:48+00:00 | GPU queue/start; flock_pid=17759: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.35

- 2026-11-10T20:06:08+00:00 | V3 matched chunk: gpt2-medium; articles 96:112, all twelve arms retained | elapsed_seconds=123.017215 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 96 --stop 112

- 2026-11-10T20:06:11+00:00 | GPU result complete; observed_wait_and_run_seconds=630.042: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 96 --stop 112

- 2026-11-10T20:06:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d096_112_v3.json

- 2026-11-10T20:06:18+00:00 | CPU complete; wall_seconds=7.313: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d096_112_v3.json

- 2026-11-10T20:06:18+00:00 | GPU queue/start; flock_pid=24974: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 96 --stop 112

- 2026-11-10T20:08:13+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=0.35; both full families, lock released after job | elapsed_seconds=118.439861 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.35

- 2026-11-10T20:08:19+00:00 | GPU result complete; observed_wait_and_run_seconds=510.042: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.35

- 2026-11-10T20:08:19+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.35_v3.json

- 2026-11-10T20:08:26+00:00 | CPU complete; wall_seconds=7.032: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.35_v3.json

- 2026-11-10T20:08:26+00:00 | GPU queue/start; flock_pid=27336: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:12:52+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 96:112, all twelve arms retained | elapsed_seconds=131.607351 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 96 --stop 112

- 2026-11-10T20:12:55+00:00 | GPU result complete; observed_wait_and_run_seconds=395.045: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 96 --stop 112

- 2026-11-10T20:12:55+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d096_112_v3.json

- 2026-11-10T20:13:01+00:00 | CPU complete; wall_seconds=6.279: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d096_112_v3.json

- 2026-11-10T20:13:01+00:00 | GPU queue/start; flock_pid=32362: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 96 --stop 112

- 2026-11-10T20:13:37+00:00 | V3 CV beta job: gpt2 s1 historical beta=0.35; both full families, lock released after job | elapsed_seconds=38.043633 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:13:43+00:00 | GPU result complete; observed_wait_and_run_seconds=315.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:13:43+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.35_v3.json

- 2026-11-10T20:13:50+00:00 | CPU complete; wall_seconds=7.729: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.35_v3.json

- 2026-11-10T20:13:50+00:00 | GPU queue/start; flock_pid=33243: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:16:08+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 96:112, all twelve arms retained | elapsed_seconds=145.214130 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 96 --stop 112

- 2026-11-10T20:16:12+00:00 | GPU result complete; observed_wait_and_run_seconds=190.049: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 96 --stop 112

- 2026-11-10T20:16:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d096_112_v3.json

- 2026-11-10T20:16:20+00:00 | CPU complete; wall_seconds=7.831: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d096_112_v3.json

- 2026-11-10T20:16:20+00:00 | GPU queue/start; flock_pid=35929: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 96 --stop 112

- 2026-11-10T20:18:21+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=0.35; both full families, lock released after job | elapsed_seconds=100.553745 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:18:26+00:00 | GPU result complete; observed_wait_and_run_seconds=275.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:18:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.35_v3.json

- 2026-11-10T20:18:33+00:00 | CPU complete; wall_seconds=6.632: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.35_v3.json

- 2026-11-10T20:18:33+00:00 | GPU queue/start; flock_pid=38407: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:30:41+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 96:112, all twelve arms retained | elapsed_seconds=110.646193 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 96 --stop 112

- 2026-11-10T20:30:43+00:00 | GPU result complete; observed_wait_and_run_seconds=860.137: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 96 --stop 112

- 2026-11-10T20:30:43+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d096_112_v3.json

- 2026-11-10T20:30:50+00:00 | CPU complete; wall_seconds=6.619: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d096_112_v3.json

- 2026-11-10T20:30:50+00:00 | GPU queue/start; flock_pid=51917: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 96 --stop 112

- 2026-11-10T20:32:21+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=0.35; both full families, lock released after job | elapsed_seconds=93.622171 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:32:26+00:00 | GPU result complete; observed_wait_and_run_seconds=830.052: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:32:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.35_v3.json

- 2026-11-10T20:32:32+00:00 | CPU complete; wall_seconds=6.424: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.35_v3.json

- 2026-11-10T20:32:33+00:00 | GPU queue/start; flock_pid=53787: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:38:25+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 96:112, all twelve arms retained | elapsed_seconds=186.985542 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 96 --stop 112

- 2026-11-10T20:38:26+00:00 | GPU result complete; observed_wait_and_run_seconds=455.039: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 96 --stop 112

- 2026-11-10T20:38:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d096_112_v3.json

- 2026-11-10T20:38:34+00:00 | CPU complete; wall_seconds=7.154: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d096_112_v3.json

- 2026-11-10T20:38:34+00:00 | GPU queue/start; flock_pid=60409: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 112 --stop 128

- 2026-11-10T20:42:20+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=0.35; both full families, lock released after job | elapsed_seconds=228.729951 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:42:25+00:00 | GPU result complete; observed_wait_and_run_seconds=590.040: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:42:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.35_v3.json

- 2026-11-10T20:42:32+00:00 | CPU complete; wall_seconds=6.923: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.35_v3.json

- 2026-11-10T20:42:32+00:00 | GPU queue/start; flock_pid=64679: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:50:24+00:00 | V3 matched chunk: gpt2; articles 112:128, all twelve arms retained | elapsed_seconds=52.925080 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 112 --stop 128

- 2026-11-10T20:50:27+00:00 | GPU result complete; observed_wait_and_run_seconds=710.046: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 112 --stop 128

- 2026-11-10T20:50:27+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d112_128_v3.json

- 2026-11-10T20:50:33+00:00 | CPU complete; wall_seconds=6.886: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d112_128_v3.json

- 2026-11-10T20:50:34+00:00 | GPU queue/start; flock_pid=74452: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 112 --stop 128

- 2026-11-10T20:52:31+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=0.35; both full families, lock released after job | elapsed_seconds=119.973172 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:52:34+00:00 | GPU result complete; observed_wait_and_run_seconds=600.089: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.35

- 2026-11-10T20:52:34+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.35_v3.json

- 2026-11-10T20:52:42+00:00 | CPU complete; wall_seconds=7.218: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.35_v3.json

- 2026-11-10T20:52:42+00:00 | GPU queue/start; flock_pid=78003: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.35

- 2026-11-10T20:59:08+00:00 | V3 matched chunk: gpt2-medium; articles 112:128, all twelve arms retained | elapsed_seconds=127.353166 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 112 --stop 128

- 2026-11-10T20:59:11+00:00 | GPU result complete; observed_wait_and_run_seconds=515.048: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 112 --stop 128

- 2026-11-10T20:59:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d112_128_v3.json

- 2026-11-10T20:59:18+00:00 | CPU complete; wall_seconds=7.374: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d112_128_v3.json

- 2026-11-10T20:59:18+00:00 | GPU queue/start; flock_pid=88454: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 112 --stop 128

- 2026-11-10T20:59:54+00:00 | V3 CV beta job: gpt2 s2 historical beta=0.35; both full families, lock released after job | elapsed_seconds=39.217059 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.35

- 2026-11-10T20:59:59+00:00 | GPU result complete; observed_wait_and_run_seconds=435.049: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.35

- 2026-11-10T20:59:59+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.35_v3.json

- 2026-11-10T21:00:07+00:00 | CPU complete; wall_seconds=8.217: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.35_v3.json

- 2026-11-10T21:00:07+00:00 | GPU queue/start; flock_pid=91138: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:07:05+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 112:128, all twelve arms retained | elapsed_seconds=144.322521 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 112 --stop 128

- 2026-11-10T21:07:10+00:00 | GPU result complete; observed_wait_and_run_seconds=470.044: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 112 --stop 128

- 2026-11-10T21:07:10+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d112_128_v3.json

- 2026-11-10T21:07:17+00:00 | CPU complete; wall_seconds=6.848: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d112_128_v3.json

- 2026-11-10T21:07:17+00:00 | GPU queue/start; flock_pid=7203: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 112 --stop 128

- 2026-11-10T21:08:52+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=0.35; both full families, lock released after job | elapsed_seconds=100.625251 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:08:54+00:00 | GPU result complete; observed_wait_and_run_seconds=525.077: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:08:54+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.35_v3.json

- 2026-11-10T21:09:01+00:00 | CPU complete; wall_seconds=6.938: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.35_v3.json

- 2026-11-10T21:09:01+00:00 | GPU queue/start; flock_pid=9695: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:26:17+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 112:128, all twelve arms retained | elapsed_seconds=147.573121 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 112 --stop 128

- 2026-11-10T21:26:23+00:00 | GPU result complete; observed_wait_and_run_seconds=1140.070: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 112 --stop 128

- 2026-11-10T21:26:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d112_128_v3.json

- 2026-11-10T21:26:31+00:00 | CPU complete; wall_seconds=7.348: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d112_128_v3.json

- 2026-11-10T21:26:31+00:00 | GPU queue/start; flock_pid=42175: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 112 --stop 128

- 2026-11-10T21:27:59+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=0.35; both full families, lock released after job | elapsed_seconds=95.094888 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:28:03+00:00 | GPU result complete; observed_wait_and_run_seconds=1135.061: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:28:03+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.35_v3.json

- 2026-11-10T21:28:12+00:00 | CPU complete; wall_seconds=8.051: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.35_v3.json

- 2026-11-10T21:28:12+00:00 | GPU queue/start; flock_pid=45045: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:39:24+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 112:128, all twelve arms retained | elapsed_seconds=116.823548 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 112 --stop 128

- 2026-11-10T21:39:26+00:00 | GPU result complete; observed_wait_and_run_seconds=760.088: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 112 --stop 128

- 2026-11-10T21:39:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d112_128_v3.json

- 2026-11-10T21:39:33+00:00 | CPU complete; wall_seconds=7.079: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d112_128_v3.json

- 2026-11-10T21:39:33+00:00 | GPU queue/start; flock_pid=71229: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 112 --stop 128

- 2026-11-10T21:43:20+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=0.35; both full families, lock released after job | elapsed_seconds=228.955846 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:43:26+00:00 | GPU result complete; observed_wait_and_run_seconds=895.088: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.35

- 2026-11-10T21:43:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.35_v3.json

- 2026-11-10T21:43:33+00:00 | CPU complete; wall_seconds=7.081: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.35_v3.json

- 2026-11-10T21:43:33+00:00 | GPU queue/start; flock_pid=77219: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.35

- 2026-11-10T22:00:03+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 112:128, all twelve arms retained | elapsed_seconds=208.096368 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 112 --stop 128

- 2026-11-10T22:00:06+00:00 | GPU result complete; observed_wait_and_run_seconds=1205.067: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 112 --stop 128

- 2026-11-10T22:00:06+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d112_128_v3.json

- 2026-11-10T22:00:14+00:00 | CPU complete; wall_seconds=7.597: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d112_128_v3.json

- 2026-11-10T22:00:14+00:00 | GPU queue/start; flock_pid=6574: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 128 --stop 144

- 2026-11-10T22:02:15+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=0.35; both full families, lock released after job | elapsed_seconds=124.807862 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.35

- 2026-11-10T22:02:19+00:00 | GPU result complete; observed_wait_and_run_seconds=1100.054: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.35

- 2026-11-10T22:02:19+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.35_v3.json

- 2026-11-10T22:02:26+00:00 | CPU complete; wall_seconds=7.198: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.35_v3.json

- 2026-11-10T22:02:27+00:00 | GPU queue/start; flock_pid=11221: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:14:07+00:00 | V3 matched chunk: gpt2; articles 128:144, all twelve arms retained | elapsed_seconds=53.603728 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 128 --stop 144

- 2026-11-10T22:14:11+00:00 | GPU result complete; observed_wait_and_run_seconds=815.044: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 128 --stop 144

- 2026-11-10T22:14:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d128_144_v3.json

- 2026-11-10T22:14:18+00:00 | CPU complete; wall_seconds=7.039: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d128_144_v3.json

- 2026-11-10T22:14:18+00:00 | GPU queue/start; flock_pid=30419: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 128 --stop 144

- 2026-11-10T22:15:14+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=0.35; both full families, lock released after job | elapsed_seconds=59.562138 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:15:16+00:00 | GPU result complete; observed_wait_and_run_seconds=750.118: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:15:16+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.35_v3.json

- 2026-11-10T22:15:24+00:00 | CPU complete; wall_seconds=7.795: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.35_v3.json

- 2026-11-10T22:15:24+00:00 | GPU queue/start; flock_pid=32300: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:22:08+00:00 | V3 matched chunk: gpt2-medium; articles 128:144, all twelve arms retained | elapsed_seconds=133.115889 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 128 --stop 144

- 2026-11-10T22:22:10+00:00 | GPU result complete; observed_wait_and_run_seconds=460.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 128 --stop 144

- 2026-11-10T22:22:10+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d128_144_v3.json

- 2026-11-10T22:22:17+00:00 | CPU complete; wall_seconds=6.456: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d128_144_v3.json

- 2026-11-10T22:22:17+00:00 | GPU queue/start; flock_pid=43007: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 128 --stop 144

- 2026-11-10T22:23:10+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=0.35; both full families, lock released after job | elapsed_seconds=56.086006 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:23:11+00:00 | GPU result complete; observed_wait_and_run_seconds=455.043: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:23:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.35_v3.json

- 2026-11-10T22:23:19+00:00 | CPU complete; wall_seconds=7.395: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.35_v3.json

- 2026-11-10T22:23:19+00:00 | GPU queue/start; flock_pid=44881: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:36:06+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 128:144, all twelve arms retained | elapsed_seconds=134.225739 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 128 --stop 144

- 2026-11-10T22:36:09+00:00 | GPU result complete; observed_wait_and_run_seconds=810.049: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 128 --stop 144

- 2026-11-10T22:36:09+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d128_144_v3.json

- 2026-11-10T22:36:16+00:00 | CPU complete; wall_seconds=6.499: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d128_144_v3.json

- 2026-11-10T22:36:16+00:00 | GPU queue/start; flock_pid=63489: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 128 --stop 144

- 2026-11-10T22:37:09+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=0.35; both full families, lock released after job | elapsed_seconds=55.779095 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:37:12+00:00 | GPU result complete; observed_wait_and_run_seconds=810.048: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.35

- 2026-11-10T22:37:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.35_v3.json

- 2026-11-10T22:37:19+00:00 | CPU complete; wall_seconds=6.672: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.35_v3.json

- 2026-11-10T22:37:19+00:00 | GPU queue/start; flock_pid=64872: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.25

- 2026-11-10T22:42:33+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 128:144, all twelve arms retained | elapsed_seconds=145.802648 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 128 --stop 144

- 2026-11-10T22:42:36+00:00 | GPU result complete; observed_wait_and_run_seconds=370.049: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 128 --stop 144

- 2026-11-10T22:42:36+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d128_144_v3.json

- 2026-11-10T22:42:43+00:00 | CPU complete; wall_seconds=6.464: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d128_144_v3.json

- 2026-11-10T22:42:43+00:00 | GPU queue/start; flock_pid=71928: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 128 --stop 144

- 2026-11-10T22:43:18+00:00 | V3 CV beta job: gpt2 s0 historical beta=0.25; both full families, lock released after job | elapsed_seconds=38.027733 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.25

- 2026-11-10T22:43:23+00:00 | GPU result complete; observed_wait_and_run_seconds=355.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.25

- 2026-11-10T22:43:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.25_v3.json

- 2026-11-10T22:43:31+00:00 | CPU complete; wall_seconds=7.248: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.25_v3.json

- 2026-11-10T22:43:31+00:00 | GPU queue/start; flock_pid=73091: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.25

- 2026-11-10T22:52:22+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 128:144, all twelve arms retained | elapsed_seconds=118.900933 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 128 --stop 144

- 2026-11-10T22:52:25+00:00 | GPU result complete; observed_wait_and_run_seconds=565.055: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 128 --stop 144

- 2026-11-10T22:52:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d128_144_v3.json

- 2026-11-10T22:52:31+00:00 | CPU complete; wall_seconds=6.436: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d128_144_v3.json

- 2026-11-10T22:52:31+00:00 | GPU queue/start; flock_pid=85272: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 128 --stop 144

- 2026-11-10T22:54:20+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=0.25; both full families, lock released after job | elapsed_seconds=110.624043 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.25

- 2026-11-10T22:54:25+00:00 | GPU result complete; observed_wait_and_run_seconds=635.045: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.25

- 2026-11-10T22:54:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.25_v3.json

- 2026-11-10T22:54:33+00:00 | CPU complete; wall_seconds=7.627: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.25_v3.json

- 2026-11-10T22:54:33+00:00 | GPU queue/start; flock_pid=88061: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:01:57+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 128:144, all twelve arms retained | elapsed_seconds=191.186483 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 128 --stop 144

- 2026-11-10T23:01:59+00:00 | GPU result complete; observed_wait_and_run_seconds=550.034: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 128 --stop 144

- 2026-11-10T23:01:59+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d128_144_v3.json

- 2026-11-10T23:02:05+00:00 | CPU complete; wall_seconds=6.601: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d128_144_v3.json

- 2026-11-10T23:02:05+00:00 | GPU queue/start; flock_pid=98232: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 144 --stop 160

- 2026-11-10T23:03:37+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=0.25; both full families, lock released after job | elapsed_seconds=93.411324 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:03:39+00:00 | GPU result complete; observed_wait_and_run_seconds=530.045: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:03:39+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.25_v3.json

- 2026-11-10T23:03:46+00:00 | CPU complete; wall_seconds=7.137: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.25_v3.json

- 2026-11-10T23:03:46+00:00 | GPU queue/start; flock_pid=759: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:08:55+00:00 | V3 matched chunk: gpt2; articles 144:160, all twelve arms retained | elapsed_seconds=50.134126 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 144 --stop 160

- 2026-11-10T23:08:57+00:00 | GPU result complete; observed_wait_and_run_seconds=400.034: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 144 --stop 160

- 2026-11-10T23:08:57+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d144_160_v3.json

- 2026-11-10T23:09:05+00:00 | CPU complete; wall_seconds=7.132: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d144_160_v3.json

- 2026-11-10T23:09:05+00:00 | GPU queue/start; flock_pid=7826: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 144 --stop 160

- 2026-11-10T23:12:51+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=0.25; both full families, lock released after job | elapsed_seconds=228.761358 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:12:53+00:00 | GPU result complete; observed_wait_and_run_seconds=530.043: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:12:53+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.25_v3.json

- 2026-11-10T23:13:00+00:00 | CPU complete; wall_seconds=6.259: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.25_v3.json

- 2026-11-10T23:13:00+00:00 | GPU queue/start; flock_pid=13274: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:25:41+00:00 | V3 matched chunk: gpt2-medium; articles 144:160, all twelve arms retained | elapsed_seconds=133.478962 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 144 --stop 160

- 2026-11-10T23:25:47+00:00 | GPU result complete; observed_wait_and_run_seconds=970.048: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 144 --stop 160

- 2026-11-10T23:25:47+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d144_160_v3.json

- 2026-11-10T23:25:54+00:00 | CPU complete; wall_seconds=6.840: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d144_160_v3.json

- 2026-11-10T23:25:54+00:00 | GPU queue/start; flock_pid=30820: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 144 --stop 160

- 2026-11-10T23:27:46+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=0.25; both full families, lock released after job | elapsed_seconds=118.196052 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:27:48+00:00 | GPU result complete; observed_wait_and_run_seconds=860.045: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.25

- 2026-11-10T23:27:48+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.25_v3.json

- 2026-11-10T23:27:55+00:00 | CPU complete; wall_seconds=6.581: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.25_v3.json

- 2026-11-10T23:27:55+00:00 | GPU queue/start; flock_pid=33528: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:30:11+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 144:160, all twelve arms retained | elapsed_seconds=138.451452 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 144 --stop 160

- 2026-11-10T23:30:12+00:00 | GPU result complete; observed_wait_and_run_seconds=250.034: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 144 --stop 160

- 2026-11-10T23:30:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d144_160_v3.json

- 2026-11-10T23:30:19+00:00 | CPU complete; wall_seconds=6.175: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d144_160_v3.json

- 2026-11-10T23:30:19+00:00 | GPU queue/start; flock_pid=36528: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 144 --stop 160

- 2026-11-10T23:30:55+00:00 | V3 CV beta job: gpt2 s1 historical beta=0.25; both full families, lock released after job | elapsed_seconds=38.027192 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:31:01+00:00 | GPU result complete; observed_wait_and_run_seconds=180.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:31:01+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.25_v3.json

- 2026-11-10T23:31:08+00:00 | CPU complete; wall_seconds=7.426: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.25_v3.json

- 2026-11-10T23:31:08+00:00 | GPU queue/start; flock_pid=37787: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:33:27+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 144:160, all twelve arms retained | elapsed_seconds=145.675082 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 144 --stop 160

- 2026-11-10T23:33:30+00:00 | GPU result complete; observed_wait_and_run_seconds=185.036: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 144 --stop 160

- 2026-11-10T23:33:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d144_160_v3.json

- 2026-11-10T23:33:37+00:00 | CPU complete; wall_seconds=6.632: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d144_160_v3.json

- 2026-11-10T23:33:37+00:00 | GPU queue/start; flock_pid=42287: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 144 --stop 160

- 2026-11-10T23:35:15+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=0.25; both full families, lock released after job | elapsed_seconds=100.197484 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:35:17+00:00 | GPU result complete; observed_wait_and_run_seconds=240.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:35:17+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.25_v3.json

- 2026-11-10T23:35:23+00:00 | CPU complete; wall_seconds=6.306: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.25_v3.json

- 2026-11-10T23:35:23+00:00 | GPU queue/start; flock_pid=45157: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:37:28+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 144:160, all twelve arms retained | elapsed_seconds=126.620515 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 144 --stop 160

- 2026-11-10T23:37:29+00:00 | GPU result complete; observed_wait_and_run_seconds=225.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 144 --stop 160

- 2026-11-10T23:37:29+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d144_160_v3.json

- 2026-11-10T23:37:38+00:00 | CPU complete; wall_seconds=7.612: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d144_160_v3.json

- 2026-11-10T23:37:38+00:00 | GPU queue/start; flock_pid=48360: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 144 --stop 160

- 2026-11-10T23:39:11+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=0.25; both full families, lock released after job | elapsed_seconds=95.257564 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:39:16+00:00 | GPU result complete; observed_wait_and_run_seconds=225.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:39:16+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.25_v3.json

- 2026-11-10T23:39:24+00:00 | CPU complete; wall_seconds=7.646: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.25_v3.json

- 2026-11-10T23:39:24+00:00 | GPU queue/start; flock_pid=50711: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:42:53+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 144:160, all twelve arms retained | elapsed_seconds=214.402054 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 144 --stop 160

- 2026-11-10T23:42:58+00:00 | GPU result complete; observed_wait_and_run_seconds=310.046: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 144 --stop 160

- 2026-11-10T23:42:58+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d144_160_v3.json

- 2026-11-10T23:43:05+00:00 | CPU complete; wall_seconds=7.453: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d144_160_v3.json

- 2026-11-10T23:43:05+00:00 | GPU queue/start; flock_pid=56237: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 160 --stop 176

- 2026-11-10T23:47:11+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=0.25; both full families, lock released after job | elapsed_seconds=230.358067 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:47:15+00:00 | GPU result complete; observed_wait_and_run_seconds=455.062: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:47:15+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.25_v3.json

- 2026-11-10T23:47:22+00:00 | CPU complete; wall_seconds=6.339: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.25_v3.json

- 2026-11-10T23:47:22+00:00 | GPU queue/start; flock_pid=62503: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:48:10+00:00 | V3 matched chunk: gpt2; articles 160:176, all twelve arms retained | elapsed_seconds=51.585633 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 160 --stop 176

- 2026-11-10T23:48:11+00:00 | GPU result complete; observed_wait_and_run_seconds=295.042: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 160 --stop 176

- 2026-11-10T23:48:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d160_176_v3.json

- 2026-11-10T23:48:17+00:00 | CPU complete; wall_seconds=6.188: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d160_176_v3.json

- 2026-11-10T23:48:17+00:00 | GPU queue/start; flock_pid=63998: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 160 --stop 176

- 2026-11-10T23:52:56+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=0.25; both full families, lock released after job | elapsed_seconds=117.897700 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:52:58+00:00 | GPU result complete; observed_wait_and_run_seconds=325.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.25

- 2026-11-10T23:52:58+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.25_v3.json

- 2026-11-10T23:53:05+00:00 | CPU complete; wall_seconds=6.395: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.25_v3.json

- 2026-11-10T23:53:05+00:00 | GPU queue/start; flock_pid=71145: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.25

- 2026-11-10T23:55:09+00:00 | V3 matched chunk: gpt2-medium; articles 160:176, all twelve arms retained | elapsed_seconds=126.762227 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 160 --stop 176

- 2026-11-10T23:55:12+00:00 | GPU result complete; observed_wait_and_run_seconds=400.036: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 160 --stop 176

- 2026-11-10T23:55:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d160_176_v3.json

- 2026-11-10T23:55:19+00:00 | CPU complete; wall_seconds=6.674: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d160_176_v3.json

- 2026-11-10T23:55:19+00:00 | GPU queue/start; flock_pid=75342: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 160 --stop 176

- 2026-11-10T23:55:54+00:00 | V3 CV beta job: gpt2 s2 historical beta=0.25; both full families, lock released after job | elapsed_seconds=38.492265 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.25

- 2026-11-10T23:56:00+00:00 | GPU result complete; observed_wait_and_run_seconds=170.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.25

- 2026-11-10T23:56:00+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.25_v3.json

- 2026-11-10T23:56:09+00:00 | CPU complete; wall_seconds=7.858: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.25_v3.json

- 2026-11-10T23:56:09+00:00 | GPU queue/start; flock_pid=76495: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.25

- 2026-11-10T23:58:25+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 160:176, all twelve arms retained | elapsed_seconds=142.981252 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 160 --stop 176

- 2026-11-10T23:58:30+00:00 | GPU result complete; observed_wait_and_run_seconds=185.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 160 --stop 176

- 2026-11-10T23:58:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d160_176_v3.json

- 2026-11-10T23:58:37+00:00 | CPU complete; wall_seconds=6.409: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d160_176_v3.json

- 2026-11-10T23:58:37+00:00 | GPU queue/start; flock_pid=79764: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 160 --stop 176

- 2026-11-11T00:00:12+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=0.25; both full families, lock released after job | elapsed_seconds=101.366752 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:00:18+00:00 | GPU result complete; observed_wait_and_run_seconds=240.034: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:00:18+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.25_v3.json

- 2026-11-11T00:00:26+00:00 | CPU complete; wall_seconds=7.473: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.25_v3.json

- 2026-11-11T00:00:26+00:00 | GPU queue/start; flock_pid=82086: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:02:42+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 160:176, all twelve arms retained | elapsed_seconds=143.127479 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 160 --stop 176

- 2026-11-11T00:02:46+00:00 | GPU result complete; observed_wait_and_run_seconds=240.044: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 160 --stop 176

- 2026-11-11T00:02:46+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d160_176_v3.json

- 2026-11-11T00:02:52+00:00 | CPU complete; wall_seconds=6.271: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d160_176_v3.json

- 2026-11-11T00:02:52+00:00 | GPU queue/start; flock_pid=85320: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 160 --stop 176

- 2026-11-11T00:04:22+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=0.25; both full families, lock released after job | elapsed_seconds=93.109704 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:04:23+00:00 | GPU result complete; observed_wait_and_run_seconds=230.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:04:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.25_v3.json

- 2026-11-11T00:04:31+00:00 | CPU complete; wall_seconds=6.199: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.25_v3.json

- 2026-11-11T00:04:31+00:00 | GPU queue/start; flock_pid=87462: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:06:26+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 160:176, all twelve arms retained | elapsed_seconds=117.716977 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 160 --stop 176

- 2026-11-11T00:06:30+00:00 | GPU result complete; observed_wait_and_run_seconds=210.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 160 --stop 176

- 2026-11-11T00:06:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d160_176_v3.json

- 2026-11-11T00:06:39+00:00 | CPU complete; wall_seconds=8.027: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d160_176_v3.json

- 2026-11-11T00:06:39+00:00 | GPU queue/start; flock_pid=90244: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 160 --stop 176

- 2026-11-11T00:10:23+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=0.25; both full families, lock released after job | elapsed_seconds=229.114729 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:10:28+00:00 | GPU result complete; observed_wait_and_run_seconds=345.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:10:28+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.25_v3.json

- 2026-11-11T00:10:34+00:00 | CPU complete; wall_seconds=6.497: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.25_v3.json

- 2026-11-11T00:10:34+00:00 | GPU queue/start; flock_pid=95353: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:13:49+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 160:176, all twelve arms retained | elapsed_seconds=199.467025 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 160 --stop 176

- 2026-11-11T00:13:55+00:00 | GPU result complete; observed_wait_and_run_seconds=420.036: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 160 --stop 176

- 2026-11-11T00:13:55+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d160_176_v3.json

- 2026-11-11T00:14:01+00:00 | CPU complete; wall_seconds=6.907: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d160_176_v3.json

- 2026-11-11T00:14:01+00:00 | GPU queue/start; flock_pid=99897: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 176 --stop 192

- 2026-11-11T00:15:54+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=0.25; both full families, lock released after job | elapsed_seconds=118.323070 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:15:57+00:00 | GPU result complete; observed_wait_and_run_seconds=310.050: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.25

- 2026-11-11T00:15:57+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.25_v3.json

- 2026-11-11T00:16:03+00:00 | CPU complete; wall_seconds=6.384: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.25_v3.json

- 2026-11-11T00:16:03+00:00 | GPU queue/start; flock_pid=2841: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:16:51+00:00 | V3 matched chunk: gpt2; articles 176:192, all twelve arms retained | elapsed_seconds=50.460317 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 176 --stop 192

- 2026-11-11T00:16:52+00:00 | GPU result complete; observed_wait_and_run_seconds=165.040: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 176 --stop 192

- 2026-11-11T00:16:52+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d176_192_v3.json

- 2026-11-11T00:17:00+00:00 | CPU complete; wall_seconds=6.706: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d176_192_v3.json

- 2026-11-11T00:17:00+00:00 | GPU queue/start; flock_pid=4138: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 176 --stop 192

- 2026-11-11T00:17:54+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=0.25; both full families, lock released after job | elapsed_seconds=56.640283 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:17:58+00:00 | GPU result complete; observed_wait_and_run_seconds=110.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:17:58+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.25_v3.json

- 2026-11-11T00:18:04+00:00 | CPU complete; wall_seconds=6.217: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.25_v3.json

- 2026-11-11T00:18:04+00:00 | GPU queue/start; flock_pid=5522: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:20:07+00:00 | V3 matched chunk: gpt2-medium; articles 176:192, all twelve arms retained | elapsed_seconds=126.171741 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 176 --stop 192

- 2026-11-11T00:20:12+00:00 | GPU result complete; observed_wait_and_run_seconds=185.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 176 --stop 192

- 2026-11-11T00:20:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d176_192_v3.json

- 2026-11-11T00:20:18+00:00 | CPU complete; wall_seconds=6.482: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d176_192_v3.json

- 2026-11-11T00:20:18+00:00 | GPU queue/start; flock_pid=8466: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 176 --stop 192

- 2026-11-11T00:21:09+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=0.25; both full families, lock released after job | elapsed_seconds=55.851757 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:21:11+00:00 | GPU result complete; observed_wait_and_run_seconds=180.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:21:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.25_v3.json

- 2026-11-11T00:21:17+00:00 | CPU complete; wall_seconds=6.497: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.25_v3.json

- 2026-11-11T00:21:17+00:00 | GPU queue/start; flock_pid=9779: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:23:31+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 176:192, all twelve arms retained | elapsed_seconds=136.133905 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 176 --stop 192

- 2026-11-11T00:23:35+00:00 | GPU result complete; observed_wait_and_run_seconds=190.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 176 --stop 192

- 2026-11-11T00:23:35+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d176_192_v3.json

- 2026-11-11T00:23:43+00:00 | CPU complete; wall_seconds=6.500: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d176_192_v3.json

- 2026-11-11T00:23:43+00:00 | GPU queue/start; flock_pid=12924: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 176 --stop 192

- 2026-11-11T00:24:33+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=0.25; both full families, lock released after job | elapsed_seconds=55.598495 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:24:34+00:00 | GPU result complete; observed_wait_and_run_seconds=190.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.25

- 2026-11-11T00:24:34+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.25_v3.json

- 2026-11-11T00:24:42+00:00 | CPU complete; wall_seconds=6.669: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.25_v3.json

- 2026-11-11T00:24:42+00:00 | GPU queue/start; flock_pid=14168: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:27:02+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 176:192, all twelve arms retained | elapsed_seconds=142.110130 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 176 --stop 192

- 2026-11-11T00:27:05+00:00 | GPU result complete; observed_wait_and_run_seconds=195.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 176 --stop 192

- 2026-11-11T00:27:05+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d176_192_v3.json

- 2026-11-11T00:27:11+00:00 | CPU complete; wall_seconds=6.242: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d176_192_v3.json

- 2026-11-11T00:27:11+00:00 | GPU queue/start; flock_pid=17414: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 176 --stop 192

- 2026-11-11T00:27:47+00:00 | V3 CV beta job: gpt2 s0 historical beta=0.15; both full families, lock released after job | elapsed_seconds=38.148731 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:27:49+00:00 | GPU result complete; observed_wait_and_run_seconds=180.039: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:27:49+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.15_v3.json

- 2026-11-11T00:27:55+00:00 | CPU complete; wall_seconds=6.259: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.15_v3.json

- 2026-11-11T00:27:56+00:00 | GPU queue/start; flock_pid=18304: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:29:46+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 176:192, all twelve arms retained | elapsed_seconds=112.982608 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 176 --stop 192

- 2026-11-11T00:29:47+00:00 | GPU result complete; observed_wait_and_run_seconds=150.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 176 --stop 192

- 2026-11-11T00:29:47+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d176_192_v3.json

- 2026-11-11T00:29:54+00:00 | CPU complete; wall_seconds=6.095: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d176_192_v3.json

- 2026-11-11T00:29:54+00:00 | GPU queue/start; flock_pid=20829: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 176 --stop 192

- 2026-11-11T00:31:32+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=0.15; both full families, lock released after job | elapsed_seconds=100.131921 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:31:39+00:00 | GPU result complete; observed_wait_and_run_seconds=215.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:31:39+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.15_v3.json

- 2026-11-11T00:31:45+00:00 | CPU complete; wall_seconds=6.651: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.15_v3.json

- 2026-11-11T00:31:45+00:00 | GPU queue/start; flock_pid=23199: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:34:49+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 176:192, all twelve arms retained | elapsed_seconds=189.816437 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 176 --stop 192

- 2026-11-11T00:34:50+00:00 | GPU result complete; observed_wait_and_run_seconds=285.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 176 --stop 192

- 2026-11-11T00:34:50+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d176_192_v3.json

- 2026-11-11T00:34:57+00:00 | CPU complete; wall_seconds=6.561: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d176_192_v3.json

- 2026-11-11T00:34:57+00:00 | GPU queue/start; flock_pid=27388: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 192 --stop 208

- 2026-11-11T00:36:29+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=0.15; both full families, lock released after job | elapsed_seconds=93.890783 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:36:31+00:00 | GPU result complete; observed_wait_and_run_seconds=275.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:36:31+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.15_v3.json

- 2026-11-11T00:36:39+00:00 | CPU complete; wall_seconds=7.203: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.15_v3.json

- 2026-11-11T00:36:39+00:00 | GPU queue/start; flock_pid=29867: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:37:28+00:00 | V3 matched chunk: gpt2; articles 192:208, all twelve arms retained | elapsed_seconds=51.588124 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 192 --stop 208

- 2026-11-11T00:37:32+00:00 | GPU result complete; observed_wait_and_run_seconds=150.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 192 --stop 208

- 2026-11-11T00:37:32+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d192_208_v3.json

- 2026-11-11T00:37:41+00:00 | CPU complete; wall_seconds=7.113: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d192_208_v3.json

- 2026-11-11T00:37:41+00:00 | GPU queue/start; flock_pid=31223: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 192 --stop 208

- 2026-11-11T00:41:23+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=0.15; both full families, lock released after job | elapsed_seconds=228.303337 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:41:25+00:00 | GPU result complete; observed_wait_and_run_seconds=275.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:41:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.15_v3.json

- 2026-11-11T00:41:32+00:00 | CPU complete; wall_seconds=6.203: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.15_v3.json

- 2026-11-11T00:41:32+00:00 | GPU queue/start; flock_pid=36270: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:43:42+00:00 | V3 matched chunk: gpt2-medium; articles 192:208, all twelve arms retained | elapsed_seconds=132.022483 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 192 --stop 208

- 2026-11-11T00:43:44+00:00 | GPU result complete; observed_wait_and_run_seconds=350.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 192 --stop 208

- 2026-11-11T00:43:44+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d192_208_v3.json

- 2026-11-11T00:43:50+00:00 | CPU complete; wall_seconds=6.390: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d192_208_v3.json

- 2026-11-11T00:43:50+00:00 | GPU queue/start; flock_pid=39428: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 192 --stop 208

- 2026-11-11T00:45:47+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=0.15; both full families, lock released after job | elapsed_seconds=118.685290 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:45:51+00:00 | GPU result complete; observed_wait_and_run_seconds=250.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.15

- 2026-11-11T00:45:51+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.15_v3.json

- 2026-11-11T00:45:58+00:00 | CPU complete; wall_seconds=6.401: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.15_v3.json

- 2026-11-11T00:45:58+00:00 | GPU queue/start; flock_pid=42650: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:48:10+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 192:208, all twelve arms retained | elapsed_seconds=137.018969 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 192 --stop 208

- 2026-11-11T00:48:11+00:00 | GPU result complete; observed_wait_and_run_seconds=250.038: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 192 --stop 208

- 2026-11-11T00:48:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d192_208_v3.json

- 2026-11-11T00:48:18+00:00 | CPU complete; wall_seconds=6.328: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d192_208_v3.json

- 2026-11-11T00:48:18+00:00 | GPU queue/start; flock_pid=45782: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 192 --stop 208

- 2026-11-11T00:48:55+00:00 | V3 CV beta job: gpt2 s1 historical beta=0.15; both full families, lock released after job | elapsed_seconds=37.996791 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:49:00+00:00 | GPU result complete; observed_wait_and_run_seconds=175.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:49:00+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.15_v3.json

- 2026-11-11T00:49:09+00:00 | CPU complete; wall_seconds=8.196: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.15_v3.json

- 2026-11-11T00:49:10+00:00 | GPU queue/start; flock_pid=46951: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:51:25+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 192:208, all twelve arms retained | elapsed_seconds=144.186347 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 192 --stop 208

- 2026-11-11T00:51:30+00:00 | GPU result complete; observed_wait_and_run_seconds=185.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 192 --stop 208

- 2026-11-11T00:51:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d192_208_v3.json

- 2026-11-11T00:51:36+00:00 | CPU complete; wall_seconds=6.153: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d192_208_v3.json

- 2026-11-11T00:51:36+00:00 | GPU queue/start; flock_pid=50940: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 192 --stop 208

- 2026-11-11T00:53:12+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=0.15; both full families, lock released after job | elapsed_seconds=100.188475 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:53:13+00:00 | GPU result complete; observed_wait_and_run_seconds=235.043: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:53:13+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.15_v3.json

- 2026-11-11T00:53:21+00:00 | CPU complete; wall_seconds=6.158: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.15_v3.json

- 2026-11-11T00:53:21+00:00 | GPU queue/start; flock_pid=53176: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:55:15+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 192:208, all twelve arms retained | elapsed_seconds=116.359175 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 192 --stop 208

- 2026-11-11T00:55:20+00:00 | GPU result complete; observed_wait_and_run_seconds=215.030: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 192 --stop 208

- 2026-11-11T00:55:20+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d192_208_v3.json

- 2026-11-11T00:55:29+00:00 | CPU complete; wall_seconds=8.111: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d192_208_v3.json

- 2026-11-11T00:55:29+00:00 | GPU queue/start; flock_pid=55951: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 192 --stop 208

- 2026-11-11T00:56:57+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=0.15; both full families, lock released after job | elapsed_seconds=94.195206 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:56:59+00:00 | GPU result complete; observed_wait_and_run_seconds=210.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.15

- 2026-11-11T00:56:59+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.15_v3.json

- 2026-11-11T00:57:06+00:00 | CPU complete; wall_seconds=6.479: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.15_v3.json

- 2026-11-11T00:57:06+00:00 | GPU queue/start; flock_pid=58040: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.15

- 2026-11-11T01:00:12+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 192:208, all twelve arms retained | elapsed_seconds=188.767774 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 192 --stop 208

- 2026-11-11T01:00:16+00:00 | GPU result complete; observed_wait_and_run_seconds=275.036: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 192 --stop 208

- 2026-11-11T01:00:16+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d192_208_v3.json

- 2026-11-11T01:00:23+00:00 | CPU complete; wall_seconds=7.052: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d192_208_v3.json

- 2026-11-11T01:00:23+00:00 | GPU queue/start; flock_pid=62363: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 208 --stop 224

- 2026-11-11T01:04:06+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=0.15; both full families, lock released after job | elapsed_seconds=228.140925 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.15

- 2026-11-11T01:04:12+00:00 | GPU result complete; observed_wait_and_run_seconds=410.034: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.15

- 2026-11-11T01:04:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.15_v3.json

- 2026-11-11T01:04:20+00:00 | CPU complete; wall_seconds=6.503: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.15_v3.json

- 2026-11-11T01:04:20+00:00 | GPU queue/start; flock_pid=67618: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.15

- 2026-11-11T01:05:04+00:00 | V3 matched chunk: gpt2; articles 208:224, all twelve arms retained | elapsed_seconds=51.269444 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 208 --stop 224

- 2026-11-11T01:05:09+00:00 | GPU result complete; observed_wait_and_run_seconds=275.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 208 --stop 224

- 2026-11-11T01:05:09+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d208_224_v3.json

- 2026-11-11T01:05:17+00:00 | CPU complete; wall_seconds=7.018: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d208_224_v3.json

- 2026-11-11T01:05:17+00:00 | GPU queue/start; flock_pid=68863: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 208 --stop 224

- 2026-11-11T01:07:09+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=0.15; both full families, lock released after job | elapsed_seconds=117.939556 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.15

- 2026-11-11T01:07:11+00:00 | GPU result complete; observed_wait_and_run_seconds=165.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.15

- 2026-11-11T01:07:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.15_v3.json

- 2026-11-11T01:07:17+00:00 | CPU complete; wall_seconds=6.229: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.15_v3.json

- 2026-11-11T01:07:17+00:00 | GPU queue/start; flock_pid=71648: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:09:23+00:00 | V3 matched chunk: gpt2-medium; articles 208:224, all twelve arms retained | elapsed_seconds=127.674769 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 208 --stop 224

- 2026-11-11T01:09:28+00:00 | GPU result complete; observed_wait_and_run_seconds=240.053: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 208 --stop 224

- 2026-11-11T01:09:28+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d208_224_v3.json

- 2026-11-11T01:09:34+00:00 | CPU complete; wall_seconds=6.300: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d208_224_v3.json

- 2026-11-11T01:09:34+00:00 | GPU queue/start; flock_pid=74756: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 208 --stop 224

- 2026-11-11T01:10:07+00:00 | V3 CV beta job: gpt2 s2 historical beta=0.15; both full families, lock released after job | elapsed_seconds=37.898199 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:10:10+00:00 | GPU result complete; observed_wait_and_run_seconds=165.036: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:10:10+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.15_v3.json

- 2026-11-11T01:10:17+00:00 | CPU complete; wall_seconds=6.394: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.15_v3.json

- 2026-11-11T01:10:17+00:00 | GPU queue/start; flock_pid=75647: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:12:28+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 208:224, all twelve arms retained | elapsed_seconds=135.253778 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 208 --stop 224

- 2026-11-11T01:12:30+00:00 | GPU result complete; observed_wait_and_run_seconds=170.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 208 --stop 224

- 2026-11-11T01:12:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d208_224_v3.json

- 2026-11-11T01:12:38+00:00 | CPU complete; wall_seconds=6.288: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d208_224_v3.json

- 2026-11-11T01:12:38+00:00 | GPU queue/start; flock_pid=78882: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 208 --stop 224

- 2026-11-11T01:14:15+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=0.15; both full families, lock released after job | elapsed_seconds=100.466455 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:14:17+00:00 | GPU result complete; observed_wait_and_run_seconds=230.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:14:17+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.15_v3.json

- 2026-11-11T01:14:24+00:00 | CPU complete; wall_seconds=6.860: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.15_v3.json

- 2026-11-11T01:14:24+00:00 | GPU queue/start; flock_pid=81588: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:16:46+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 208:224, all twelve arms retained | elapsed_seconds=143.917824 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 208 --stop 224

- 2026-11-11T01:16:48+00:00 | GPU result complete; observed_wait_and_run_seconds=240.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 208 --stop 224

- 2026-11-11T01:16:48+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d208_224_v3.json

- 2026-11-11T01:16:55+00:00 | CPU complete; wall_seconds=6.242: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d208_224_v3.json

- 2026-11-11T01:16:55+00:00 | GPU queue/start; flock_pid=84800: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 208 --stop 224

- 2026-11-11T01:18:26+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=0.15; both full families, lock released after job | elapsed_seconds=93.113929 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:18:29+00:00 | GPU result complete; observed_wait_and_run_seconds=235.042: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:18:29+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.15_v3.json

- 2026-11-11T01:18:35+00:00 | CPU complete; wall_seconds=6.145: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.15_v3.json

- 2026-11-11T01:18:35+00:00 | GPU queue/start; flock_pid=86942: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:20:26+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 208:224, all twelve arms retained | elapsed_seconds=114.053151 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 208 --stop 224

- 2026-11-11T01:20:29+00:00 | GPU result complete; observed_wait_and_run_seconds=205.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 208 --stop 224

- 2026-11-11T01:20:29+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d208_224_v3.json

- 2026-11-11T01:20:36+00:00 | CPU complete; wall_seconds=6.722: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d208_224_v3.json

- 2026-11-11T01:20:36+00:00 | GPU queue/start; flock_pid=89543: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 208 --stop 224

- 2026-11-11T01:24:26+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=0.15; both full families, lock released after job | elapsed_seconds=233.291605 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:24:30+00:00 | GPU result complete; observed_wait_and_run_seconds=340.041: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:24:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.15_v3.json

- 2026-11-11T01:24:38+00:00 | CPU complete; wall_seconds=6.788: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.15_v3.json

- 2026-11-11T01:24:38+00:00 | GPU queue/start; flock_pid=94702: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:27:51+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 208:224, all twelve arms retained | elapsed_seconds=198.600189 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 208 --stop 224

- 2026-11-11T01:27:54+00:00 | GPU result complete; observed_wait_and_run_seconds=420.032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 208 --stop 224

- 2026-11-11T01:27:54+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d208_224_v3.json

- 2026-11-11T01:28:01+00:00 | CPU complete; wall_seconds=6.677: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d208_224_v3.json

- 2026-11-11T01:28:01+00:00 | GPU queue/start; flock_pid=99062: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 224 --stop 240

- 2026-11-11T01:30:00+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=0.15; both full families, lock released after job | elapsed_seconds=122.708388 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:30:06+00:00 | GPU result complete; observed_wait_and_run_seconds=315.033: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.15

- 2026-11-11T01:30:06+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.15_v3.json

- 2026-11-11T01:30:13+00:00 | CPU complete; wall_seconds=6.954: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.15_v3.json

- 2026-11-11T01:30:13+00:00 | GPU queue/start; flock_pid=2309: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:30:59+00:00 | V3 matched chunk: gpt2; articles 224:240, all twelve arms retained | elapsed_seconds=51.638585 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 224 --stop 240

- 2026-11-11T01:31:04+00:00 | GPU result complete; observed_wait_and_run_seconds=175.033: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 224 --stop 240

- 2026-11-11T01:31:04+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d224_240_v3.json

- 2026-11-11T01:31:11+00:00 | CPU complete; wall_seconds=6.747: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d224_240_v3.json

- 2026-11-11T01:31:11+00:00 | GPU queue/start; flock_pid=3567: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 224 --stop 240

- 2026-11-11T01:32:04+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=0.15; both full families, lock released after job | elapsed_seconds=58.639265 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:32:09+00:00 | GPU result complete; observed_wait_and_run_seconds=110.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:32:09+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.15_v3.json

- 2026-11-11T01:32:16+00:00 | CPU complete; wall_seconds=6.690: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.15_v3.json

- 2026-11-11T01:32:16+00:00 | GPU queue/start; flock_pid=4943: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:34:24+00:00 | V3 matched chunk: gpt2-medium; articles 224:240, all twelve arms retained | elapsed_seconds=133.247981 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 224 --stop 240

- 2026-11-11T01:34:30+00:00 | GPU result complete; observed_wait_and_run_seconds=190.062: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 224 --stop 240

- 2026-11-11T01:34:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d224_240_v3.json

- 2026-11-11T01:34:37+00:00 | CPU complete; wall_seconds=6.465: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d224_240_v3.json

- 2026-11-11T01:34:37+00:00 | GPU queue/start; flock_pid=7894: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 224 --stop 240

- 2026-11-11T01:35:28+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=0.15; both full families, lock released after job | elapsed_seconds=57.695476 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:35:29+00:00 | GPU result complete; observed_wait_and_run_seconds=185.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:35:29+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.15_v3.json

- 2026-11-11T01:35:37+00:00 | CPU complete; wall_seconds=6.607: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.15_v3.json

- 2026-11-11T01:35:37+00:00 | GPU queue/start; flock_pid=9172: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:37:57+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 224:240, all twelve arms retained | elapsed_seconds=142.468003 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 224 --stop 240

- 2026-11-11T01:38:00+00:00 | GPU result complete; observed_wait_and_run_seconds=195.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 224 --stop 240

- 2026-11-11T01:38:00+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d224_240_v3.json

- 2026-11-11T01:38:06+00:00 | CPU complete; wall_seconds=6.463: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d224_240_v3.json

- 2026-11-11T01:38:06+00:00 | GPU queue/start; flock_pid=12375: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 224 --stop 240

- 2026-11-11T01:39:01+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=0.15; both full families, lock released after job | elapsed_seconds=57.378815 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:39:05+00:00 | GPU result complete; observed_wait_and_run_seconds=200.061: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.15

- 2026-11-11T01:39:05+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.15_v3.json

- 2026-11-11T01:39:14+00:00 | CPU complete; wall_seconds=7.319: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.15_v3.json

- 2026-11-11T01:39:14+00:00 | GPU queue/start; flock_pid=13951: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:41:35+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 224:240, all twelve arms retained | elapsed_seconds=147.156709 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 224 --stop 240

- 2026-11-11T01:41:36+00:00 | GPU result complete; observed_wait_and_run_seconds=200.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 224 --stop 240

- 2026-11-11T01:41:36+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d224_240_v3.json

- 2026-11-11T01:41:42+00:00 | CPU complete; wall_seconds=6.185: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d224_240_v3.json

- 2026-11-11T01:41:42+00:00 | GPU queue/start; flock_pid=17138: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 224 --stop 240

- 2026-11-11T01:42:20+00:00 | V3 CV beta job: gpt2 s0 historical beta=0.1; both full families, lock released after job | elapsed_seconds=38.416258 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:42:22+00:00 | GPU result complete; observed_wait_and_run_seconds=180.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:42:22+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.1_v3.json

- 2026-11-11T01:42:28+00:00 | CPU complete; wall_seconds=6.147: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.1_v3.json

- 2026-11-11T01:42:28+00:00 | GPU queue/start; flock_pid=18071: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:44:20+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 224:240, all twelve arms retained | elapsed_seconds=113.887780 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 224 --stop 240

- 2026-11-11T01:44:24+00:00 | GPU result complete; observed_wait_and_run_seconds=155.024: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 224 --stop 240

- 2026-11-11T01:44:24+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d224_240_v3.json

- 2026-11-11T01:44:32+00:00 | CPU complete; wall_seconds=6.220: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d224_240_v3.json

- 2026-11-11T01:44:32+00:00 | GPU queue/start; flock_pid=20785: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 224 --stop 240

- 2026-11-11T01:46:06+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=0.1; both full families, lock released after job | elapsed_seconds=100.059380 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:46:08+00:00 | GPU result complete; observed_wait_and_run_seconds=210.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:46:08+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.1_v3.json

- 2026-11-11T01:46:14+00:00 | CPU complete; wall_seconds=6.519: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.1_v3.json

- 2026-11-11T01:46:14+00:00 | GPU queue/start; flock_pid=23112: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:49:23+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 224:240, all twelve arms retained | elapsed_seconds=189.937603 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 224 --stop 240

- 2026-11-11T01:49:24+00:00 | GPU result complete; observed_wait_and_run_seconds=280.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 224 --stop 240

- 2026-11-11T01:49:24+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d224_240_v3.json

- 2026-11-11T01:49:31+00:00 | CPU complete; wall_seconds=6.421: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d224_240_v3.json

- 2026-11-11T01:49:31+00:00 | GPU queue/start; flock_pid=27397: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 240 --stop 256

- 2026-11-11T01:51:02+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=0.1; both full families, lock released after job | elapsed_seconds=93.180562 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:51:07+00:00 | GPU result complete; observed_wait_and_run_seconds=280.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:51:07+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.1_v3.json

- 2026-11-11T01:51:14+00:00 | CPU complete; wall_seconds=6.381: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.1_v3.json

- 2026-11-11T01:51:15+00:00 | GPU queue/start; flock_pid=29771: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:51:59+00:00 | V3 matched chunk: gpt2; articles 240:256, all twelve arms retained | elapsed_seconds=50.300366 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 240 --stop 256

- 2026-11-11T01:52:03+00:00 | GPU result complete; observed_wait_and_run_seconds=145.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 240 --stop 256

- 2026-11-11T01:52:03+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d240_256_v3.json

- 2026-11-11T01:52:09+00:00 | CPU complete; wall_seconds=6.887: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2_d240_256_v3.json

- 2026-11-11T01:52:09+00:00 | GPU queue/start; flock_pid=30984: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 240 --stop 256

- 2026-11-11T01:55:53+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=0.1; both full families, lock released after job | elapsed_seconds=228.046933 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:55:57+00:00 | GPU result complete; observed_wait_and_run_seconds=270.034: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:55:57+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.1_v3.json

- 2026-11-11T01:56:04+00:00 | CPU complete; wall_seconds=6.359: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.1_v3.json

- 2026-11-11T01:56:04+00:00 | GPU queue/start; flock_pid=35952: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.1

- 2026-11-11T01:58:06+00:00 | V3 matched chunk: gpt2-medium; articles 240:256, all twelve arms retained | elapsed_seconds=126.667897 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 240 --stop 256

- 2026-11-11T01:58:11+00:00 | GPU result complete; observed_wait_and_run_seconds=345.029: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 240 --stop 256

- 2026-11-11T01:58:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d240_256_v3.json

- 2026-11-11T01:58:18+00:00 | CPU complete; wall_seconds=6.467: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_gpt2-medium_d240_256_v3.json

- 2026-11-11T01:58:18+00:00 | GPU queue/start; flock_pid=38939: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 240 --stop 256

- 2026-11-11T02:00:10+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=0.1; both full families, lock released after job | elapsed_seconds=117.152954 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.1

- 2026-11-11T02:00:15+00:00 | GPU result complete; observed_wait_and_run_seconds=240.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.1

- 2026-11-11T02:00:15+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.1_v3.json

- 2026-11-11T02:00:21+00:00 | CPU complete; wall_seconds=6.468: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.1_v3.json

- 2026-11-11T02:00:21+00:00 | GPU queue/start; flock_pid=41635: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:02:30+00:00 | V3 matched chunk: EleutherAI/pythia-410m; articles 240:256, all twelve arms retained | elapsed_seconds=133.995711 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 240 --stop 256

- 2026-11-11T02:02:34+00:00 | GPU result complete; observed_wait_and_run_seconds=245.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 240 --stop 256

- 2026-11-11T02:02:34+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d240_256_v3.json

- 2026-11-11T02:02:41+00:00 | CPU complete; wall_seconds=6.394: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-410m_d240_256_v3.json

- 2026-11-11T02:02:41+00:00 | GPU queue/start; flock_pid=44637: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 240 --stop 256

- 2026-11-11T02:03:14+00:00 | V3 CV beta job: gpt2 s1 historical beta=0.1; both full families, lock released after job | elapsed_seconds=37.900809 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:03:20+00:00 | GPU result complete; observed_wait_and_run_seconds=170.023: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:03:20+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.1_v3.json

- 2026-11-11T02:03:27+00:00 | CPU complete; wall_seconds=6.913: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.1_v3.json

- 2026-11-11T02:03:27+00:00 | GPU queue/start; flock_pid=45613: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:05:43+00:00 | V3 matched chunk: EleutherAI/pythia-1.4b; articles 240:256, all twelve arms retained | elapsed_seconds=143.316442 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 240 --stop 256

- 2026-11-11T02:05:45+00:00 | GPU result complete; observed_wait_and_run_seconds=175.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 240 --stop 256

- 2026-11-11T02:05:45+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d240_256_v3.json

- 2026-11-11T02:05:51+00:00 | CPU complete; wall_seconds=6.117: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_EleutherAI__pythia-1.4b_d240_256_v3.json

- 2026-11-11T02:05:51+00:00 | GPU queue/start; flock_pid=48720: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 240 --stop 256

- 2026-11-11T02:07:30+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=0.1; both full families, lock released after job | elapsed_seconds=100.019240 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:07:34+00:00 | GPU result complete; observed_wait_and_run_seconds=235.031: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:07:34+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.1_v3.json

- 2026-11-11T02:07:40+00:00 | CPU complete; wall_seconds=6.324: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.1_v3.json

- 2026-11-11T02:07:40+00:00 | GPU queue/start; flock_pid=51041: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:09:30+00:00 | V3 matched chunk: Qwen/Qwen2.5-0.5B; articles 240:256, all twelve arms retained | elapsed_seconds=113.069682 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 240 --stop 256

- 2026-11-11T02:09:31+00:00 | GPU result complete; observed_wait_and_run_seconds=210.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 240 --stop 256

- 2026-11-11T02:09:31+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d240_256_v3.json

- 2026-11-11T02:09:39+00:00 | CPU complete; wall_seconds=6.205: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d240_256_v3.json

- 2026-11-11T02:09:39+00:00 | GPU queue/start; flock_pid=53651: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 240 --stop 256

- 2026-11-11T02:11:09+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=0.1; both full families, lock released after job | elapsed_seconds=93.042343 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:11:15+00:00 | GPU result complete; observed_wait_and_run_seconds=205.056: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:11:15+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.1_v3.json

- 2026-11-11T02:11:22+00:00 | CPU complete; wall_seconds=6.777: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.1_v3.json

- 2026-11-11T02:11:22+00:00 | GPU queue/start; flock_pid=55950: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:14:26+00:00 | V3 matched chunk: Qwen/Qwen2.5-3B; articles 240:256, all twelve arms retained | elapsed_seconds=190.721250 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 240 --stop 256

- 2026-11-11T02:14:32+00:00 | GPU result complete; observed_wait_and_run_seconds=280.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 240 --stop 256

- 2026-11-11T02:14:32+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d240_256_v3.json

- 2026-11-11T02:14:39+00:00 | CPU complete; wall_seconds=6.891: .venv/Scripts/python.exe -B phase40_v3_checks.py --mass-chunk out/phase7_massmatched_Qwen__Qwen2.5-3B_d240_256_v3.json

- 2026-11-11T02:14:39+00:00 | CPU start: .venv/Scripts/python.exe -B phase37_mass_matched.py --aggregate-only

- 2026-11-11T02:14:48+00:00 | V3 matched complete: six models x 256 articles x twelve arms; Holm24, exact feasible mass equality | elapsed_seconds=3.583788

- 2026-11-11T02:14:50+00:00 | CPU complete; wall_seconds=9.619: .venv/Scripts/python.exe -B phase37_mass_matched.py --aggregate-only

- 2026-11-11T02:14:50+00:00 | V3 selected job kinds complete; elapsed_seconds=50350.644; counts={'mass': 96, 'items': 24, 'cv': 0}

- 2026-11-11T02:18:20+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=0.1; both full families, lock released after job | elapsed_seconds=227.930522 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:18:21+00:00 | GPU result complete; observed_wait_and_run_seconds=400.035: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:18:21+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.1_v3.json

- 2026-11-11T02:18:27+00:00 | CPU complete; wall_seconds=5.769: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.1_v3.json

- 2026-11-11T02:18:27+00:00 | GPU queue/start; flock_pid=65083: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:20:30+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=0.1; both full families, lock released after job | elapsed_seconds=117.459102 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:20:33+00:00 | GPU result complete; observed_wait_and_run_seconds=120.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.1

- 2026-11-11T02:20:33+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.1_v3.json

- 2026-11-11T02:20:40+00:00 | CPU complete; wall_seconds=5.816: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.1_v3.json

- 2026-11-11T02:20:40+00:00 | GPU queue/start; flock_pid=67915: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:21:23+00:00 | V3 CV beta job: gpt2 s2 historical beta=0.1; both full families, lock released after job | elapsed_seconds=37.824482 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:21:27+00:00 | GPU result complete; observed_wait_and_run_seconds=45.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:21:27+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.1_v3.json

- 2026-11-11T02:21:33+00:00 | CPU complete; wall_seconds=5.967: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.1_v3.json

- 2026-11-11T02:21:33+00:00 | GPU queue/start; flock_pid=69089: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:23:19+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=0.1; both full families, lock released after job | elapsed_seconds=100.166644 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:23:24+00:00 | GPU result complete; observed_wait_and_run_seconds=105.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:23:24+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.1_v3.json

- 2026-11-11T02:23:30+00:00 | CPU complete; wall_seconds=6.142: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.1_v3.json

- 2026-11-11T02:23:30+00:00 | GPU queue/start; flock_pid=71546: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:25:08+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=0.1; both full families, lock released after job | elapsed_seconds=93.202360 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:25:09+00:00 | GPU result complete; observed_wait_and_run_seconds=95.023: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:25:09+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.1_v3.json

- 2026-11-11T02:25:15+00:00 | CPU complete; wall_seconds=5.822: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.1_v3.json

- 2026-11-11T02:25:15+00:00 | GPU queue/start; flock_pid=73784: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:29:09+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=0.1; both full families, lock released after job | elapsed_seconds=228.191602 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:29:12+00:00 | GPU result complete; observed_wait_and_run_seconds=225.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:29:12+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.1_v3.json

- 2026-11-11T02:29:18+00:00 | CPU complete; wall_seconds=5.796: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.1_v3.json

- 2026-11-11T02:29:18+00:00 | GPU queue/start; flock_pid=79122: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:31:21+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=0.1; both full families, lock released after job | elapsed_seconds=117.432627 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:31:24+00:00 | GPU result complete; observed_wait_and_run_seconds=120.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.1

- 2026-11-11T02:31:24+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.1_v3.json

- 2026-11-11T02:31:30+00:00 | CPU complete; wall_seconds=5.734: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.1_v3.json

- 2026-11-11T02:31:30+00:00 | GPU queue/start; flock_pid=81949: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:32:31+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=0.1; both full families, lock released after job | elapsed_seconds=55.100925 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:32:33+00:00 | GPU result complete; observed_wait_and_run_seconds=60.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:32:33+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.1_v3.json

- 2026-11-11T02:32:40+00:00 | CPU complete; wall_seconds=5.949: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.1_v3.json

- 2026-11-11T02:32:40+00:00 | GPU queue/start; flock_pid=83440: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:33:40+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=0.1; both full families, lock released after job | elapsed_seconds=55.181344 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:33:43+00:00 | GPU result complete; observed_wait_and_run_seconds=60.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:33:43+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.1_v3.json

- 2026-11-11T02:33:49+00:00 | CPU complete; wall_seconds=5.785: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.1_v3.json

- 2026-11-11T02:33:49+00:00 | GPU queue/start; flock_pid=84943: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:34:49+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=0.1; both full families, lock released after job | elapsed_seconds=55.045104 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:34:52+00:00 | GPU result complete; observed_wait_and_run_seconds=60.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.1

- 2026-11-11T02:34:52+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.1_v3.json

- 2026-11-11T02:34:58+00:00 | CPU complete; wall_seconds=5.760: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.1_v3.json

- 2026-11-11T02:34:58+00:00 | GPU queue/start; flock_pid=86418: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:35:41+00:00 | V3 CV beta job: gpt2 s0 historical beta=0.05; both full families, lock released after job | elapsed_seconds=37.791953 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:35:45+00:00 | GPU result complete; observed_wait_and_run_seconds=45.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:35:45+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.05_v3.json

- 2026-11-11T02:35:52+00:00 | CPU complete; wall_seconds=5.906: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.05_v3.json

- 2026-11-11T02:35:52+00:00 | GPU queue/start; flock_pid=87539: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:37:37+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=0.05; both full families, lock released after job | elapsed_seconds=100.228022 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:37:42+00:00 | GPU result complete; observed_wait_and_run_seconds=105.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:37:42+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.05_v3.json

- 2026-11-11T02:37:47+00:00 | CPU complete; wall_seconds=5.783: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.05_v3.json

- 2026-11-11T02:37:47+00:00 | GPU queue/start; flock_pid=90037: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:39:26+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=0.05; both full families, lock released after job | elapsed_seconds=93.197386 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:39:27+00:00 | GPU result complete; observed_wait_and_run_seconds=95.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:39:27+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.05_v3.json

- 2026-11-11T02:39:35+00:00 | CPU complete; wall_seconds=5.971: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.05_v3.json

- 2026-11-11T02:39:35+00:00 | GPU queue/start; flock_pid=92263: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:43:27+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=0.05; both full families, lock released after job | elapsed_seconds=228.270517 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:43:30+00:00 | GPU result complete; observed_wait_and_run_seconds=225.023: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:43:30+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.05_v3.json

- 2026-11-11T02:43:36+00:00 | CPU complete; wall_seconds=5.711: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.05_v3.json

- 2026-11-11T02:43:36+00:00 | GPU queue/start; flock_pid=97749: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:45:39+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=0.05; both full families, lock released after job | elapsed_seconds=117.525713 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:45:42+00:00 | GPU result complete; observed_wait_and_run_seconds=120.023: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.05

- 2026-11-11T02:45:42+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.05_v3.json

- 2026-11-11T02:45:50+00:00 | CPU complete; wall_seconds=5.868: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.05_v3.json

- 2026-11-11T02:45:50+00:00 | GPU queue/start; flock_pid=888: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:46:32+00:00 | V3 CV beta job: gpt2 s1 historical beta=0.05; both full families, lock released after job | elapsed_seconds=37.899697 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:46:36+00:00 | GPU result complete; observed_wait_and_run_seconds=45.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:46:36+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.05_v3.json

- 2026-11-11T02:46:42+00:00 | CPU complete; wall_seconds=5.750: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.05_v3.json

- 2026-11-11T02:46:42+00:00 | GPU queue/start; flock_pid=2115: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:48:28+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=0.05; both full families, lock released after job | elapsed_seconds=100.136944 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:48:34+00:00 | GPU result complete; observed_wait_and_run_seconds=105.023: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:48:34+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.05_v3.json

- 2026-11-11T02:48:39+00:00 | CPU complete; wall_seconds=5.729: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.05_v3.json

- 2026-11-11T02:48:39+00:00 | GPU queue/start; flock_pid=4672: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:50:18+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=0.05; both full families, lock released after job | elapsed_seconds=93.255371 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:50:19+00:00 | GPU result complete; observed_wait_and_run_seconds=95.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:50:19+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.05_v3.json

- 2026-11-11T02:50:25+00:00 | CPU complete; wall_seconds=5.783: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.05_v3.json

- 2026-11-11T02:50:25+00:00 | GPU queue/start; flock_pid=6952: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:54:19+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=0.05; both full families, lock released after job | elapsed_seconds=228.141473 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:54:23+00:00 | GPU result complete; observed_wait_and_run_seconds=225.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:54:23+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.05_v3.json

- 2026-11-11T02:54:28+00:00 | CPU complete; wall_seconds=5.687: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.05_v3.json

- 2026-11-11T02:54:28+00:00 | GPU queue/start; flock_pid=12158: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:56:31+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=0.05; both full families, lock released after job | elapsed_seconds=117.437020 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:56:35+00:00 | GPU result complete; observed_wait_and_run_seconds=120.023: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.05

- 2026-11-11T02:56:35+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.05_v3.json

- 2026-11-11T02:56:40+00:00 | CPU complete; wall_seconds=5.844: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.05_v3.json

- 2026-11-11T02:56:40+00:00 | GPU queue/start; flock_pid=14970: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.05

- 2026-11-11T02:57:24+00:00 | V3 CV beta job: gpt2 s2 historical beta=0.05; both full families, lock released after job | elapsed_seconds=37.886342 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.05

- 2026-11-11T02:57:29+00:00 | GPU result complete; observed_wait_and_run_seconds=45.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.05

- 2026-11-11T02:57:29+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.05_v3.json

- 2026-11-11T02:57:34+00:00 | CPU complete; wall_seconds=5.798: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.05_v3.json

- 2026-11-11T02:57:34+00:00 | GPU queue/start; flock_pid=16147: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.05

- 2026-11-11T02:59:20+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=0.05; both full families, lock released after job | elapsed_seconds=100.180477 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.05

- 2026-11-11T02:59:24+00:00 | GPU result complete; observed_wait_and_run_seconds=105.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.05

- 2026-11-11T02:59:24+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.05_v3.json

- 2026-11-11T02:59:32+00:00 | CPU complete; wall_seconds=5.763: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.05_v3.json

- 2026-11-11T02:59:32+00:00 | GPU queue/start; flock_pid=18679: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:01:09+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=0.05; both full families, lock released after job | elapsed_seconds=93.223125 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:01:11+00:00 | GPU result complete; observed_wait_and_run_seconds=95.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:01:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.05_v3.json

- 2026-11-11T03:01:17+00:00 | CPU complete; wall_seconds=5.846: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.05_v3.json

- 2026-11-11T03:01:17+00:00 | GPU queue/start; flock_pid=20963: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:05:11+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=0.05; both full families, lock released after job | elapsed_seconds=228.431005 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:05:14+00:00 | GPU result complete; observed_wait_and_run_seconds=225.026: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:05:14+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.05_v3.json

- 2026-11-11T03:05:21+00:00 | CPU complete; wall_seconds=5.788: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.05_v3.json

- 2026-11-11T03:05:21+00:00 | GPU queue/start; flock_pid=26281: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:07:23+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=0.05; both full families, lock released after job | elapsed_seconds=117.484955 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:07:27+00:00 | GPU result complete; observed_wait_and_run_seconds=120.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.05

- 2026-11-11T03:07:27+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.05_v3.json

- 2026-11-11T03:07:33+00:00 | CPU complete; wall_seconds=6.026: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.05_v3.json

- 2026-11-11T03:07:33+00:00 | GPU queue/start; flock_pid=29162: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:08:34+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=0.05; both full families, lock released after job | elapsed_seconds=55.479720 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:08:37+00:00 | GPU result complete; observed_wait_and_run_seconds=60.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:08:37+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.05_v3.json

- 2026-11-11T03:08:42+00:00 | CPU complete; wall_seconds=5.791: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.05_v3.json

- 2026-11-11T03:08:43+00:00 | GPU queue/start; flock_pid=30631: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:09:43+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=0.05; both full families, lock released after job | elapsed_seconds=55.127961 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:09:46+00:00 | GPU result complete; observed_wait_and_run_seconds=60.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:09:46+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.05_v3.json

- 2026-11-11T03:09:51+00:00 | CPU complete; wall_seconds=5.730: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.05_v3.json

- 2026-11-11T03:09:51+00:00 | GPU queue/start; flock_pid=32135: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:10:52+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=0.05; both full families, lock released after job | elapsed_seconds=55.171117 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:10:55+00:00 | GPU result complete; observed_wait_and_run_seconds=60.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.05

- 2026-11-11T03:10:55+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.05_v3.json

- 2026-11-11T03:11:01+00:00 | CPU complete; wall_seconds=5.793: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.05_v3.json

- 2026-11-11T03:11:01+00:00 | GPU queue/start; flock_pid=33621: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:11:40+00:00 | V3 CV beta job: gpt2 s0 historical beta=0.0; both full families, lock released after job | elapsed_seconds=33.091660 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:11:44+00:00 | GPU result complete; observed_wait_and_run_seconds=40.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:11:44+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.0_v3.json

- 2026-11-11T03:11:50+00:00 | CPU complete; wall_seconds=5.782: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_b0.0_v3.json

- 2026-11-11T03:11:50+00:00 | GPU queue/start; flock_pid=34681: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:13:22+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=0.0; both full families, lock released after job | elapsed_seconds=87.807545 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:13:25+00:00 | GPU result complete; observed_wait_and_run_seconds=90.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:13:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.0_v3.json

- 2026-11-11T03:13:31+00:00 | CPU complete; wall_seconds=6.049: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.0_v3.json

- 2026-11-11T03:13:31+00:00 | GPU queue/start; flock_pid=36895: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:14:57+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=0.0; both full families, lock released after job | elapsed_seconds=81.474871 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:15:01+00:00 | GPU result complete; observed_wait_and_run_seconds=85.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:15:01+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.0_v3.json

- 2026-11-11T03:15:06+00:00 | CPU complete; wall_seconds=5.806: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.0_v3.json

- 2026-11-11T03:15:06+00:00 | GPU queue/start; flock_pid=39032: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:18:48+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=0.0; both full families, lock released after job | elapsed_seconds=216.035378 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:18:53+00:00 | GPU result complete; observed_wait_and_run_seconds=215.024: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:18:53+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.0_v3.json

- 2026-11-11T03:19:00+00:00 | CPU complete; wall_seconds=5.897: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.0_v3.json

- 2026-11-11T03:19:00+00:00 | GPU queue/start; flock_pid=44013: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:20:51+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=0.0; both full families, lock released after job | elapsed_seconds=106.406605 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:20:55+00:00 | GPU result complete; observed_wait_and_run_seconds=110.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.0

- 2026-11-11T03:20:55+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.0_v3.json

- 2026-11-11T03:21:01+00:00 | CPU complete; wall_seconds=5.825: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.0_v3.json

- 2026-11-11T03:21:01+00:00 | GPU queue/start; flock_pid=46669: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:21:40+00:00 | V3 CV beta job: gpt2 s1 historical beta=0.0; both full families, lock released after job | elapsed_seconds=33.129793 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:21:45+00:00 | GPU result complete; observed_wait_and_run_seconds=40.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:21:45+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.0_v3.json

- 2026-11-11T03:21:50+00:00 | CPU complete; wall_seconds=5.730: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_b0.0_v3.json

- 2026-11-11T03:21:50+00:00 | GPU queue/start; flock_pid=47752: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:23:23+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=0.0; both full families, lock released after job | elapsed_seconds=87.966330 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:23:25+00:00 | GPU result complete; observed_wait_and_run_seconds=90.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:23:25+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.0_v3.json

- 2026-11-11T03:23:31+00:00 | CPU complete; wall_seconds=6.026: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.0_v3.json

- 2026-11-11T03:23:31+00:00 | GPU queue/start; flock_pid=49822: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:24:58+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=0.0; both full families, lock released after job | elapsed_seconds=81.546086 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:25:01+00:00 | GPU result complete; observed_wait_and_run_seconds=85.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:25:01+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.0_v3.json

- 2026-11-11T03:25:07+00:00 | CPU complete; wall_seconds=5.864: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.0_v3.json

- 2026-11-11T03:25:07+00:00 | GPU queue/start; flock_pid=51961: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:28:49+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=0.0; both full families, lock released after job | elapsed_seconds=216.197458 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:28:54+00:00 | GPU result complete; observed_wait_and_run_seconds=215.028: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:28:54+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.0_v3.json

- 2026-11-11T03:29:02+00:00 | CPU complete; wall_seconds=5.867: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.0_v3.json

- 2026-11-11T03:29:02+00:00 | GPU queue/start; flock_pid=56926: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:30:52+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=0.0; both full families, lock released after job | elapsed_seconds=106.406914 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:30:57+00:00 | GPU result complete; observed_wait_and_run_seconds=110.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.0

- 2026-11-11T03:30:57+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.0_v3.json

- 2026-11-11T03:31:02+00:00 | CPU complete; wall_seconds=5.755: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.0_v3.json

- 2026-11-11T03:31:02+00:00 | GPU queue/start; flock_pid=59558: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:31:41+00:00 | V3 CV beta job: gpt2 s2 historical beta=0.0; both full families, lock released after job | elapsed_seconds=33.103086 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:31:46+00:00 | GPU result complete; observed_wait_and_run_seconds=40.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:31:46+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.0_v3.json

- 2026-11-11T03:31:52+00:00 | CPU complete; wall_seconds=5.802: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_b0.0_v3.json

- 2026-11-11T03:31:52+00:00 | GPU queue/start; flock_pid=60610: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:33:25+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=0.0; both full families, lock released after job | elapsed_seconds=87.891166 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:33:27+00:00 | GPU result complete; observed_wait_and_run_seconds=90.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:33:27+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.0_v3.json

- 2026-11-11T03:33:33+00:00 | CPU complete; wall_seconds=5.998: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.0_v3.json

- 2026-11-11T03:33:33+00:00 | GPU queue/start; flock_pid=62737: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:35:00+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=0.0; both full families, lock released after job | elapsed_seconds=81.464428 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:35:03+00:00 | GPU result complete; observed_wait_and_run_seconds=85.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:35:03+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.0_v3.json

- 2026-11-11T03:35:09+00:00 | CPU complete; wall_seconds=5.826: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.0_v3.json

- 2026-11-11T03:35:09+00:00 | GPU queue/start; flock_pid=64884: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:38:50+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=0.0; both full families, lock released after job | elapsed_seconds=215.973921 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:38:56+00:00 | GPU result complete; observed_wait_and_run_seconds=215.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:38:56+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.0_v3.json

- 2026-11-11T03:39:01+00:00 | CPU complete; wall_seconds=5.859: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.0_v3.json

- 2026-11-11T03:39:01+00:00 | GPU queue/start; flock_pid=69819: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:40:54+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=0.0; both full families, lock released after job | elapsed_seconds=106.299056 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:40:58+00:00 | GPU result complete; observed_wait_and_run_seconds=110.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.0

- 2026-11-11T03:40:58+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.0_v3.json

- 2026-11-11T03:41:04+00:00 | CPU complete; wall_seconds=5.883: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.0_v3.json

- 2026-11-11T03:41:04+00:00 | GPU queue/start; flock_pid=72403: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:41:57+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=0.0; both full families, lock released after job | elapsed_seconds=47.554020 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:42:03+00:00 | GPU result complete; observed_wait_and_run_seconds=55.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:42:03+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.0_v3.json

- 2026-11-11T03:42:09+00:00 | CPU complete; wall_seconds=5.980: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.0_v3.json

- 2026-11-11T03:42:09+00:00 | GPU queue/start; flock_pid=73765: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:43:02+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=0.0; both full families, lock released after job | elapsed_seconds=47.477622 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:43:07+00:00 | GPU result complete; observed_wait_and_run_seconds=55.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:43:07+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.0_v3.json

- 2026-11-11T03:43:13+00:00 | CPU complete; wall_seconds=5.833: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.0_v3.json

- 2026-11-11T03:43:13+00:00 | GPU queue/start; flock_pid=75233: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:44:06+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=0.0; both full families, lock released after job | elapsed_seconds=47.757716 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:44:11+00:00 | GPU result complete; observed_wait_and_run_seconds=55.023: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.0

- 2026-11-11T03:44:11+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.0_v3.json

- 2026-11-11T03:44:17+00:00 | CPU complete; wall_seconds=5.838: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.0_v3.json

- 2026-11-11T03:44:17+00:00 | GPU queue/start; flock_pid=76656: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:44:49+00:00 | V3 CV beta job: gpt2 s0 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=26.273932 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:44:56+00:00 | GPU result complete; observed_wait_and_run_seconds=35.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:44:56+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:45:01+00:00 | CPU complete; wall_seconds=5.673: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:45:01+00:00 | GPU queue/start; flock_pid=77616: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:46:17+00:00 | V3 CV beta job: gpt2-medium s0 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=70.572814 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:46:20+00:00 | GPU result complete; observed_wait_and_run_seconds=75.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:46:20+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:46:26+00:00 | CPU complete; wall_seconds=5.796: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:46:26+00:00 | GPU queue/start; flock_pid=79610: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:47:36+00:00 | V3 CV beta job: EleutherAI/pythia-410m s0 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=64.590636 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:47:41+00:00 | GPU result complete; observed_wait_and_run_seconds=70.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:47:41+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:47:46+00:00 | CPU complete; wall_seconds=5.747: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:47:46+00:00 | GPU queue/start; flock_pid=81283: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:51:12+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s0 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=200.163737 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:51:18+00:00 | GPU result complete; observed_wait_and_run_seconds=200.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:51:18+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:51:24+00:00 | CPU complete; wall_seconds=5.695: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:51:24+00:00 | GPU queue/start; flock_pid=85962: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:53:00+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=90.898178 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:53:04+00:00 | GPU result complete; observed_wait_and_run_seconds=95.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta legacy_beta0

- 2026-11-11T03:53:04+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:53:10+00:00 | CPU complete; wall_seconds=5.858: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_blegacy_beta0_v3.json

- 2026-11-11T03:53:10+00:00 | GPU queue/start; flock_pid=88293: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:53:42+00:00 | V3 CV beta job: gpt2 s1 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=26.304678 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:53:47+00:00 | GPU result complete; observed_wait_and_run_seconds=35.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:53:47+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T03:53:54+00:00 | CPU complete; wall_seconds=5.722: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T03:53:54+00:00 | GPU queue/start; flock_pid=89240: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:55:09+00:00 | V3 CV beta job: gpt2-medium s1 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=70.686879 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:55:13+00:00 | GPU result complete; observed_wait_and_run_seconds=75.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:55:13+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T03:55:19+00:00 | CPU complete; wall_seconds=5.725: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T03:55:19+00:00 | GPU queue/start; flock_pid=91043: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:56:29+00:00 | V3 CV beta job: EleutherAI/pythia-410m s1 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=64.623938 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:56:34+00:00 | GPU result complete; observed_wait_and_run_seconds=70.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T03:56:34+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T03:56:40+00:00 | CPU complete; wall_seconds=5.809: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T03:56:40+00:00 | GPU queue/start; flock_pid=92769: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T04:00:05+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s1 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=200.552371 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T04:00:10+00:00 | GPU result complete; observed_wait_and_run_seconds=200.025: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T04:00:10+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T04:00:18+00:00 | CPU complete; wall_seconds=5.784: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T04:00:18+00:00 | GPU queue/start; flock_pid=97452: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T04:01:53+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=90.820098 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T04:01:58+00:00 | GPU result complete; observed_wait_and_run_seconds=95.027: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta legacy_beta0

- 2026-11-11T04:01:58+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T04:02:04+00:00 | CPU complete; wall_seconds=5.781: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_blegacy_beta0_v3.json

- 2026-11-11T04:02:04+00:00 | GPU queue/start; flock_pid=99759: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:02:35+00:00 | V3 CV beta job: gpt2 s2 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=26.311001 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:02:40+00:00 | GPU result complete; observed_wait_and_run_seconds=35.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:02:40+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:02:46+00:00 | CPU complete; wall_seconds=5.779: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:02:46+00:00 | GPU queue/start; flock_pid=1086: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:04:03+00:00 | V3 CV beta job: gpt2-medium s2 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=70.593817 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:04:06+00:00 | GPU result complete; observed_wait_and_run_seconds=75.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:04:06+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:04:12+00:00 | CPU complete; wall_seconds=5.720: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_gpt2-medium_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:04:12+00:00 | GPU queue/start; flock_pid=2958: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:05:22+00:00 | V3 CV beta job: EleutherAI/pythia-410m s2 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=64.505870 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:05:26+00:00 | GPU result complete; observed_wait_and_run_seconds=70.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:05:26+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:05:33+00:00 | CPU complete; wall_seconds=5.699: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:05:33+00:00 | GPU queue/start; flock_pid=4717: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:08:58+00:00 | V3 CV beta job: EleutherAI/pythia-1.4b s2 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=200.294767 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:09:04+00:00 | GPU result complete; observed_wait_and_run_seconds=200.024: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:09:04+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:09:09+00:00 | CPU complete; wall_seconds=5.726: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:09:09+00:00 | GPU queue/start; flock_pid=9390: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:10:46+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 historical beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=90.692109 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:10:52+00:00 | GPU result complete; observed_wait_and_run_seconds=95.022: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta legacy_beta0

- 2026-11-11T04:10:52+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:10:57+00:00 | CPU complete; wall_seconds=5.756: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_blegacy_beta0_v3.json

- 2026-11-11T04:10:57+00:00 | GPU queue/start; flock_pid=11752: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:11:35+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s0 standard_bf16 beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=33.093733 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:11:39+00:00 | GPU result complete; observed_wait_and_run_seconds=40.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:11:39+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_blegacy_beta0_v3.json

- 2026-11-11T04:11:45+00:00 | CPU complete; wall_seconds=5.752: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_blegacy_beta0_v3.json

- 2026-11-11T04:11:45+00:00 | GPU queue/start; flock_pid=12774: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:12:24+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s1 standard_bf16 beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=33.042149 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:12:28+00:00 | GPU result complete; observed_wait_and_run_seconds=40.020: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:12:28+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_blegacy_beta0_v3.json

- 2026-11-11T04:12:34+00:00 | CPU complete; wall_seconds=5.805: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_blegacy_beta0_v3.json

- 2026-11-11T04:12:34+00:00 | GPU queue/start; flock_pid=13818: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:13:12+00:00 | V3 CV beta job: Qwen/Qwen2.5-0.5B s2 standard_bf16 beta=legacy_beta0; both full families, lock released after job | elapsed_seconds=33.003132 | command: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:13:16+00:00 | GPU result complete; observed_wait_and_run_seconds=40.021: flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta legacy_beta0

- 2026-11-11T04:13:16+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_blegacy_beta0_v3.json

- 2026-11-11T04:13:22+00:00 | CPU complete; wall_seconds=5.689: .venv/Scripts/python.exe -B phase40_v3_checks.py --cv-current-beta-job out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_blegacy_beta0_v3.json

- 2026-11-11T04:13:22+00:00 | CPU start: .venv/Scripts/python.exe -B phase45_currentcv_items.py --aggregate-only

- 2026-11-11T04:13:28+00:00 | V3 CV provenance limitation: gpt2 s0: out\phase18_historical_mismatch_gpt2_s0_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:28+00:00 | V3 CV provenance limitation: gpt2 s1: out\phase18_historical_mismatch_gpt2_s1_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:29+00:00 | V3 CV provenance limitation: gpt2 s2: out\phase18_historical_mismatch_gpt2_s2_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:29+00:00 | V3 CV provenance limitation: gpt2-medium s0: out\phase18_historical_mismatch_gpt2-medium_s0_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:30+00:00 | V3 CV provenance limitation: gpt2-medium s1: out\phase18_historical_mismatch_gpt2-medium_s1_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:30+00:00 | V3 CV provenance limitation: gpt2-medium s2: out\phase18_historical_mismatch_gpt2-medium_s2_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:31+00:00 | V3 CV provenance limitation: EleutherAI/pythia-410m s0: out\phase18_historical_mismatch_EleutherAI__pythia-410m_s0_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:31+00:00 | V3 CV provenance limitation: EleutherAI/pythia-410m s1: out\phase18_historical_mismatch_EleutherAI__pythia-410m_s1_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:31+00:00 | V3 CV provenance limitation: EleutherAI/pythia-410m s2: out\phase18_historical_mismatch_EleutherAI__pythia-410m_s2_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:33+00:00 | V3 CV provenance limitation: Qwen/Qwen2.5-0.5B s0: out\phase18_historical_mismatch_Qwen__Qwen2.5-0.5B_s0_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:33+00:00 | V3 CV provenance limitation: Qwen/Qwen2.5-0.5B s1: out\phase18_historical_mismatch_Qwen__Qwen2.5-0.5B_s1_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:34+00:00 | V3 CV provenance limitation: Qwen/Qwen2.5-0.5B s2: out\phase18_historical_mismatch_Qwen__Qwen2.5-0.5B_s2_v3.json; current-item counterfactual reported separately

- 2026-11-11T04:13:35+00:00 | V3 CV complete: all five models x three seeds x full nine-beta grid; strict attention sanity and full positive-beta legacy equality; failed historical counts explicit, same-item legacy/corrected CV compared | elapsed_seconds=7.678557 | command: .venv/Scripts/python.exe -B phase45_currentcv_items.py --aggregate-only

- 2026-11-11T04:13:36+00:00 | CPU complete; wall_seconds=12.909: .venv/Scripts/python.exe -B phase45_currentcv_items.py --aggregate-only

- 2026-11-11T04:13:36+00:00 | V3 current-generator CV complete; wall_seconds=55076.152; jobs=180

- 2026-11-11T04:15:18+00:00 | CPU start: .venv/Scripts/python.exe -B phase40_v3_checks.py

- 2026-11-11T04:16:13+00:00 | V3 delivery audit: all six required outputs and 300 jobs reconciled | elapsed_seconds=50.021679

- 2026-11-11T04:16:14+00:00 | CPU complete; wall_seconds=52.785: .venv/Scripts/python.exe -B phase40_v3_checks.py


RELATORIO FINAL DA REVISAO V3

2026-11-11T04:17:13.075503+00:00

FALTA: itens e hashes do gerador historico da familia B da CV. Na identidade GPT-2 s0, A reproduz 214/600, B atual tem 123/600 contra 60/600 salvos. O diagnostico dos lotes originais preservou todas as 2400 predicoes. Comparacao antigo/corrigido nos mesmos itens atuais separada dos resultados antigos salvos.

Agregacao: mediana de instancias com IC95 por bootstrap de documentos/itens independentes; 2000 repeticoes, semente0. Para acerto binario, mediana da diferenca por item e ganho de acuracia (contagem/n) sao mostrados separadamente; media agrupada e secundaria.

Constancia estratificada; 64 documentos por modelo/comprimento. Ns/Nc explicita os conjuntos definidos; a diferenca pareada usa a intersecao de cabecas.

| modelo | n | estrato | cabecas | % | Ns/Nc | sink IC95 | controle IC95 | delta pareado IC95 | colunas energia0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gpt2 | 128 | gt_0.3 | 1092 | 71.09 | 1092/1092 | 0.120 [0.110, 0.128] | 0.773 [0.757, 0.791] | -0.644 [-0.664, -0.631] | 0 |
| gpt2 | 128 | le_0.3 | 444 | 28.91 | 444/444 | 0.729 [0.702, 0.784] | 0.850 [0.788, 0.877] | 0.000 [-0.007, 0.010] | 0 |
| gpt2 | 256 | gt_0.3 | 1068 | 69.53 | 1068/1068 | 0.153 [0.145, 0.159] | 0.850 [0.836, 0.866] | -0.691 [-0.708, -0.680] | 0 |
| gpt2 | 256 | le_0.3 | 468 | 30.47 | 468/468 | 0.794 [0.752, 0.829] | 0.891 [0.874, 0.926] | -0.001 [-0.010, 0.002] | 0 |
| gpt2-medium | 128 | gt_0.3 | 1176 | 76.56 | 1176/1176 | 0.118 [0.111, 0.125] | 0.741 [0.728, 0.754] | -0.619 [-0.633, -0.606] | 0 |
| gpt2-medium | 128 | le_0.3 | 360 | 23.44 | 360/360 | 0.733 [0.696, 0.756] | 0.729 [0.675, 0.816] | 0.008 [-0.017, 0.033] | 0 |
| gpt2-medium | 256 | gt_0.3 | 1118 | 72.79 | 1118/1118 | 0.148 [0.141, 0.156] | 0.815 [0.800, 0.825] | -0.661 [-0.674, -0.648] | 1 |
| gpt2-medium | 256 | le_0.3 | 418 | 27.21 | 418/418 | 0.750 [0.721, 0.790] | 0.839 [0.801, 0.863] | -0.049 [-0.100, -0.009] | 0 |
| EleutherAI/pythia-410m | 128 | gt_0.3 | 1014 | 66.02 | 1014/1013 | 0.128 [0.115, 0.137] | 0.807 [0.796, 0.824] | -0.658 [-0.674, -0.648] | 466 |
| EleutherAI/pythia-410m | 128 | le_0.3 | 522 | 33.98 | 522/522 | 0.902 [0.879, 0.917] | 0.852 [0.836, 0.876] | 0.040 [0.028, 0.054] | 475 |
| EleutherAI/pythia-410m | 256 | gt_0.3 | 947 | 61.65 | 947/947 | 0.160 [0.152, 0.167] | 0.875 [0.863, 0.882] | -0.690 [-0.700, -0.672] | 919 |
| EleutherAI/pythia-410m | 256 | le_0.3 | 589 | 38.35 | 589/589 | 0.912 [0.897, 0.937] | 0.917 [0.901, 0.927] | 0.011 [0.003, 0.021] | 883 |
| EleutherAI/pythia-1.4b | 128 | gt_0.3 | 1080 | 70.31 | 1080/1080 | 0.187 [0.168, 0.203] | 0.817 [0.803, 0.829] | -0.619 [-0.642, -0.601] | 867 |
| EleutherAI/pythia-1.4b | 128 | le_0.3 | 456 | 29.69 | 456/456 | 0.805 [0.748, 0.850] | 0.832 [0.820, 0.849] | -0.008 [-0.084, 0.026] | 320 |
| EleutherAI/pythia-1.4b | 256 | gt_0.3 | 913 | 59.44 | 913/913 | 0.236 [0.222, 0.246] | 0.876 [0.867, 0.884] | -0.630 [-0.649, -0.613] | 1164 |
| EleutherAI/pythia-1.4b | 256 | le_0.3 | 623 | 40.56 | 623/623 | 0.587 [0.531, 0.711] | 0.890 [0.882, 0.905] | -0.272 [-0.350, -0.161] | 1290 |
| Qwen/Qwen2.5-0.5B | 128 | gt_0.3 | 959 | 62.43 | 959/959 | 0.134 [0.125, 0.144] | 0.829 [0.818, 0.841] | -0.673 [-0.692, -0.657] | 380 |
| Qwen/Qwen2.5-0.5B | 128 | le_0.3 | 577 | 37.57 | 577/577 | 0.812 [0.759, 0.849] | 0.816 [0.795, 0.838] | 0.007 [-0.002, 0.022] | 51 |
| Qwen/Qwen2.5-0.5B | 256 | gt_0.3 | 907 | 59.05 | 907/907 | 0.147 [0.137, 0.155] | 0.901 [0.889, 0.911] | -0.729 [-0.740, -0.716] | 604 |
| Qwen/Qwen2.5-0.5B | 256 | le_0.3 | 629 | 40.95 | 629/629 | 0.816 [0.650, 0.888] | 0.894 [0.875, 0.905] | -0.018 [-0.084, 0.003] | 56 |
| Qwen/Qwen2.5-3B | 128 | gt_0.3 | 1613 | 70.01 | 1613/1613 | 0.142 [0.137, 0.147] | 0.827 [0.818, 0.834] | -0.666 [-0.675, -0.655] | 0 |
| Qwen/Qwen2.5-3B | 128 | le_0.3 | 691 | 29.99 | 691/691 | 0.778 [0.739, 0.810] | 0.801 [0.785, 0.822] | -0.005 [-0.051, 0.010] | 0 |
| Qwen/Qwen2.5-3B | 256 | gt_0.3 | 1511 | 65.58 | 1511/1511 | 0.152 [0.146, 0.158] | 0.897 [0.888, 0.903] | -0.728 [-0.736, -0.720] | 0 |
| Qwen/Qwen2.5-3B | 256 | le_0.3 | 793 | 34.42 | 793/793 | 0.760 [0.664, 0.809] | 0.865 [0.854, 0.879] | -0.105 [-0.170, -0.057] | 0 |
| Qwen/Qwen2.5-7B | 128 | gt_0.3 | 1332 | 74.33 | 1332/1332 | 0.143 [0.137, 0.148] | 0.804 [0.793, 0.815] | -0.640 [-0.650, -0.628] | 0 |
| Qwen/Qwen2.5-7B | 128 | le_0.3 | 460 | 25.67 | 460/460 | 0.907 [0.821, 0.946] | 0.808 [0.783, 0.830] | 0.063 [0.042, 0.090] | 5 |
| Qwen/Qwen2.5-7B | 256 | gt_0.3 | 1269 | 70.81 | 1269/1269 | 0.160 [0.153, 0.166] | 0.878 [0.871, 0.884] | -0.692 [-0.701, -0.683] | 0 |
| Qwen/Qwen2.5-7B | 256 | le_0.3 | 523 | 29.19 | 523/523 | 0.907 [0.805, 0.958] | 0.869 [0.854, 0.886] | 0.019 [0.001, 0.037] | 7 |

V3 nomeado: 19968 matrizes em 12 datasets, 15 configuracoes cada; decomposicoes reutilizadas, estimativas pontuais preservadas, ICs de documento adicionados a todos os escalares.

KL do ultimo token; todos os 256 artigos em cada braco. Delta = sink menos controle casado. Beta nominal limitado pela massa viavel comum; nao e a remocao completa do teste beta0.

| modelo | contexto | beta | artigos | KL sink IC95 | KL casado IC95 | delta pareado IC95 | Wilcoxon p | Holm24 p | r_biserial |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gpt2 | identity | 0.0 | 256 | 0.078 [0.071, 0.086] | 0.100 [0.092, 0.114] | -0.011 [-0.020, -0.005] | 0.000404 | 0.00283 | -0.255 |
| gpt2 | identity | 0.25 | 256 | 0.039 [0.034, 0.043] | 0.072 [0.062, 0.087] | -0.030 [-0.038, -0.022] | 1.62e-22 | 2.91e-21 | -0.704 |
| gpt2 | anova | 0.0 | 256 | 1.795 [1.691, 1.969] | 1.653 [1.407, 1.761] | 0.313 [0.245, 0.374] | 9.8e-21 | 1.67e-19 | 0.673 |
| gpt2 | anova | 0.25 | 256 | 1.775 [1.617, 1.911] | 1.614 [1.383, 1.722] | 0.241 [0.181, 0.280] | 1.04e-17 | 1.56e-16 | 0.618 |
| gpt2-medium | identity | 0.0 | 256 | 0.045 [0.041, 0.051] | 0.060 [0.054, 0.075] | -0.013 [-0.021, -0.006] | 1.24e-08 | 1.74e-07 | -0.411 |
| gpt2-medium | identity | 0.25 | 256 | 0.024 [0.021, 0.027] | 0.047 [0.043, 0.058] | -0.020 [-0.026, -0.016] | 5.74e-28 | 1.15e-26 | -0.790 |
| gpt2-medium | anova | 0.0 | 256 | 1.527 [1.437, 1.667] | 1.558 [1.461, 1.697] | -0.059 [-0.092, -0.018] | 0.0015 | 0.00899 | -0.229 |
| gpt2-medium | anova | 0.25 | 256 | 1.479 [1.337, 1.604] | 1.565 [1.413, 1.686] | -0.065 [-0.110, -0.019] | 8.1e-05 | 0.000729 | -0.284 |
| EleutherAI/pythia-410m | identity | 0.0 | 256 | 0.014 [0.012, 0.015] | 0.056 [0.051, 0.066] | -0.036 [-0.042, -0.031] | 2.56e-35 | 5.62e-34 | -0.894 |
| EleutherAI/pythia-410m | identity | 0.25 | 256 | 0.007 [0.005, 0.008] | 0.039 [0.036, 0.043] | -0.029 [-0.034, -0.027] | 5.1e-40 | 1.22e-38 | -0.955 |
| EleutherAI/pythia-410m | anova | 0.0 | 256 | 2.176 [2.016, 2.338] | 2.149 [1.955, 2.377] | 0.032 [-0.002, 0.060] | 0.013 | 0.0648 | 0.179 |
| EleutherAI/pythia-410m | anova | 0.25 | 256 | 2.158 [1.945, 2.343] | 2.163 [1.961, 2.347] | -0.010 [-0.031, 0.022] | 0.619 | 1 | 0.036 |
| EleutherAI/pythia-1.4b | identity | 0.0 | 256 | 0.011 [0.010, 0.013] | 0.046 [0.041, 0.052] | -0.027 [-0.032, -0.021] | 5.65e-33 | 1.19e-31 | -0.862 |
| EleutherAI/pythia-1.4b | identity | 0.25 | 256 | 0.005 [0.005, 0.006] | 0.030 [0.026, 0.032] | -0.022 [-0.024, -0.019] | 3.64e-39 | 8.37e-38 | -0.944 |
| EleutherAI/pythia-1.4b | anova | 0.0 | 256 | 1.983 [1.810, 2.170] | 2.036 [1.849, 2.214] | -0.015 [-0.057, 0.016] | 0.277 | 0.831 | -0.078 |
| EleutherAI/pythia-1.4b | anova | 0.25 | 256 | 2.031 [1.815, 2.185] | 1.982 [1.831, 2.225] | -0.007 [-0.021, 0.013] | 0.831 | 1 | -0.015 |
| Qwen/Qwen2.5-0.5B | identity | 0.0 | 256 | 0.047 [0.042, 0.055] | 0.062 [0.054, 0.072] | -0.010 [-0.015, -0.005] | 3.75e-07 | 4.87e-06 | -0.366 |
| Qwen/Qwen2.5-0.5B | identity | 0.25 | 256 | 0.024 [0.021, 0.028] | 0.045 [0.041, 0.052] | -0.019 [-0.024, -0.014] | 7.27e-25 | 1.38e-23 | -0.742 |
| Qwen/Qwen2.5-0.5B | anova | 0.0 | 256 | 2.081 [1.943, 2.264] | 2.157 [1.968, 2.322] | -0.068 [-0.132, 0.014] | 0.0156 | 0.0648 | -0.174 |
| Qwen/Qwen2.5-0.5B | anova | 0.25 | 256 | 2.026 [1.874, 2.267] | 2.143 [2.011, 2.348] | -0.086 [-0.143, -0.050] | 0.000112 | 0.000893 | -0.279 |
| Qwen/Qwen2.5-3B | identity | 0.0 | 256 | 0.050 [0.041, 0.057] | 0.063 [0.054, 0.072] | -0.005 [-0.010, -0.001] | 6.23e-05 | 0.000623 | -0.289 |
| Qwen/Qwen2.5-3B | identity | 0.25 | 256 | 0.024 [0.021, 0.030] | 0.045 [0.041, 0.055] | -0.016 [-0.022, -0.010] | 5.64e-20 | 9.02e-19 | -0.660 |
| Qwen/Qwen2.5-3B | anova | 0.0 | 256 | 6.287 [5.897, 6.729] | 6.773 [6.359, 7.372] | -0.345 [-0.560, -0.100] | 2.64e-05 | 0.000316 | -0.303 |
| Qwen/Qwen2.5-3B | anova | 0.25 | 256 | 6.369 [5.857, 6.824] | 6.734 [6.062, 7.429] | -0.498 [-0.647, -0.178] | 2.95e-05 | 0.000324 | -0.301 |

Controle antigo e base preservados:

| modelo | contexto | base IC95 | coluna meio IC95 |
| --- | --- | --- | --- |
| gpt2 | identity | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| gpt2 | anova | 1.631 [1.476, 1.725] | 1.630 [1.537, 1.747] |
| gpt2-medium | identity | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.001] |
| gpt2-medium | anova | 1.466 [1.282, 1.629] | 1.464 [1.335, 1.606] |
| EleutherAI/pythia-410m | identity | 0.000 [0.000, 0.000] | 0.001 [0.001, 0.001] |
| EleutherAI/pythia-410m | anova | 2.137 [1.917, 2.307] | 2.137 [1.916, 2.284] |
| EleutherAI/pythia-1.4b | identity | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.001] |
| EleutherAI/pythia-1.4b | anova | 1.997 [1.824, 2.244] | 2.007 [1.816, 2.233] |
| Qwen/Qwen2.5-0.5B | identity | 0.000 [0.000, 0.000] | 0.002 [0.002, 0.003] |
| Qwen/Qwen2.5-0.5B | anova | 2.013 [1.871, 2.188] | 2.068 [1.847, 2.235] |
| Qwen/Qwen2.5-3B | identity | 0.000 [0.000, 0.000] | 0.002 [0.002, 0.003] |
| Qwen/Qwen2.5-3B | anova | 6.315 [5.796, 6.900] | 6.336 [5.729, 6.854] |

Sonda e KV: janela canonica phase13; ganhos em pontos percentuais. IC de itens dentro de semente x posicao. Familia principal Holm7; familia de precisao Holm8 secundaria, registrada antes da agregacao.

| tarefa | modelo | itens | mediana delta item | mediana ganho semente IC95 pp | media antiga pp | media nova secundaria pp | permutacao p | Holm7 p | Holm8 secundario p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| probe | gpt2 | 6000 | 0.000 | 11.800 [10.400, 12.850] | 11.500 | 11.500 | 2.26e-85 | 1.36e-84 | 1.58e-84 |
| probe | gpt2-medium | 6000 | 0.000 | 19.750 [18.400, 21.150] | 19.717 | 19.717 | 9.7e-187 | 6.79e-186 | 7.76e-186 |
| probe | EleutherAI/pythia-410m | 6000 | 0.000 | 3.250 [2.450, 4.100] | 3.317 | 3.317 | 5.93e-18 | 2.97e-17 | 2.97e-17 |
| probe | EleutherAI/pythia-1.4b | 6000 | 0.000 | 0.500 [-0.350, 1.200] | 0.433 | 0.433 | 0.216 | 0.216 | 0.216 |
| probe | Qwen/Qwen2.5-0.5B | 6000 | 0.000 | 4.600 [3.550, 5.600] | 4.617 | 4.617 | 2.19e-17 | 8.78e-17 | 8.78e-17 |
| probe | Qwen/Qwen2.5-0.5B BF16 suplementar | 6000 | 0.000 | 4.750 [3.450, 5.550] | -- | 4.533 | 1.32e-18 | -- | 7.91e-18 |
| kv | gpt2-medium | 1800 | 0.000 | 4.667 [3.500, 6.667] | 5.167 | 5.167 | 1.71e-09 | 5.13e-09 | 5.13e-09 |
| kv | Qwen/Qwen2.5-3B | 1800 | 0.000 | 4.167 [2.833, 6.167] | 4.667 | 4.667 | 5.41e-07 | 1.08e-06 | 1.08e-06 |

Discordantes e McNemar exato por semente; Holm21 principal, Holm24 para suplemento:

| tarefa | modelo | semente | itens | so editado certo | so base certa | McNemar p | p ajustado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| probe | gpt2 | 0 | 2000 | 256 | 44 | 1.59e-37 | 2.54e-36 |
| probe | gpt2 | 1 | 2000 | 280 | 38 | 1.02e-46 | 1.84e-45 |
| probe | gpt2 | 2 | 2000 | 285 | 49 | 1.28e-41 | 2.18e-40 |
| probe | gpt2-medium | 0 | 2000 | 435 | 21 | 9.54e-102 | 2e-100 |
| probe | gpt2-medium | 1 | 2000 | 399 | 25 | 7.45e-88 | 1.42e-86 |
| probe | gpt2-medium | 2 | 2000 | 416 | 21 | 2.01e-96 | 4.02e-95 |
| probe | EleutherAI/pythia-410m | 0 | 2000 | 104 | 25 | 1.2e-12 | 1.79e-11 |
| probe | EleutherAI/pythia-410m | 1 | 2000 | 81 | 26 | 9.37e-08 | 8.44e-07 |
| probe | EleutherAI/pythia-410m | 2 | 2000 | 91 | 26 | 1.21e-09 | 1.7e-08 |
| probe | EleutherAI/pythia-1.4b | 0 | 2000 | 73 | 57 | 0.188 | 0.564 |
| probe | EleutherAI/pythia-1.4b | 1 | 2000 | 56 | 56 | 1 | 1 |
| probe | EleutherAI/pythia-1.4b | 2 | 2000 | 62 | 52 | 0.399 | 0.799 |
| probe | Qwen/Qwen2.5-0.5B | 0 | 2000 | 179 | 84 | 4.65e-09 | 5.12e-08 |
| probe | Qwen/Qwen2.5-0.5B | 1 | 2000 | 164 | 74 | 5.29e-09 | 5.29e-08 |
| probe | Qwen/Qwen2.5-0.5B | 2 | 2000 | 163 | 71 | 1.68e-09 | 2.18e-08 |
| probe | Qwen/Qwen2.5-0.5B BF16 suplementar | 0 | 2000 | 178 | 83 | 4.04e-09 | 5.25e-08 |
| probe | Qwen/Qwen2.5-0.5B BF16 suplementar | 1 | 2000 | 164 | 69 | 4.25e-10 | 7.22e-09 |
| probe | Qwen/Qwen2.5-0.5B BF16 suplementar | 2 | 2000 | 156 | 74 | 6.78e-08 | 6.78e-07 |
| kv | gpt2-medium | 0 | 600 | 37 | 9 | 4.06e-05 | 0.000284 |
| kv | gpt2-medium | 1 | 600 | 40 | 3 | 3.02e-09 | 3.63e-08 |
| kv | gpt2-medium | 2 | 600 | 38 | 10 | 6.17e-05 | 0.00037 |
| kv | Qwen/Qwen2.5-3B | 0 | 600 | 38 | 14 | 0.0012 | 0.00478 |
| kv | Qwen/Qwen2.5-3B | 1 | 600 | 39 | 14 | 0.000802 | 0.00401 |
| kv | Qwen/Qwen2.5-3B | 2 | 600 | 43 | 8 | 6.87e-07 | 5.49e-06 |

CV completa, tres sementes e nove betas; lotes originais por posicao. Selecao em A avaliada em B e vice-versa. A janela da CV preserva mid() antigo baseado na ultima posicao testada. ICs condicionais ao beta escolhido na outra familia.

| modelo | familia de selecao | beta salvo s0/s1/s2 | beta legado itens atuais | beta corrigido itens atuais |
| --- | --- | --- | --- | --- |
| gpt2 | A | 0.05/0.05/0.05 | 0.05/0.05/0.05 | 0.05/0.05/0.05 |
| gpt2 | B | 0.05/0.05/0.1 | 0.5/0.5/0.5 | 0.5/0.5/0.5 |
| gpt2-medium | A | 0.15/0.15/0.15 | 0.15/0.15/0.15 | 0.15/0.15/0.15 |
| gpt2-medium | B | 0.1/0.1/0.05 | 0.5/0.5/0.75 | 0.5/0.5/0.75 |
| EleutherAI/pythia-410m | A | 0.05/0.1/0.1 | 0.05/0.1/0.1 | 0.05/0.1/0.1 |
| EleutherAI/pythia-410m | B | 0.1/0.1/0.1 | 0.1/0.1/0.05 | 0.1/0.1/0.05 |
| EleutherAI/pythia-1.4b | A | 1/0.25/0.15 | 1/0.25/0.15 | 1/0.25/0.15 |
| EleutherAI/pythia-1.4b | B | 0/0/0 | 0/0/0 | 1/0/0 |
| Qwen/Qwen2.5-0.5B | A | 0.1/0.05/0.05 | 0.1/0.05/0.05 | 0.1/0.05/0.05 |
| Qwen/Qwen2.5-0.5B | B | 0.1/0.25/0.1 | 0.05/0.05/0.05 | 0.05/0.05/0.05 |

| modelo | familia held-out | itens | ganho antigo salvo pp | legado nos itens atuais IC95 pp | corrigido nos itens atuais IC95 pp |
| --- | --- | --- | --- | --- | --- |
| gpt2 | A | 1800 | 19.333 | 5.667 [4.000, 7.000] | 5.667 [4.000, 7.000] |
| gpt2 | B | 1800 | 4.667 | -3.667 [-5.833, -0.667] | -3.667 [-5.833, -0.667] |
| gpt2-medium | A | 1800 | 23.667 | 10.833 [8.000, 12.500] | 10.833 [8.000, 12.500] |
| gpt2-medium | B | 1800 | 8.000 | -10.667 [-12.667, -7.667] | -10.667 [-12.667, -7.667] |
| EleutherAI/pythia-410m | A | 1800 | 5.667 | 5.667 [4.000, 7.833] | 5.667 [4.000, 7.833] |
| EleutherAI/pythia-410m | B | 1800 | 3.333 | 3.667 [2.333, 5.667] | 3.667 [2.333, 5.667] |
| EleutherAI/pythia-1.4b | A | 1800 | 0.000 | 0.000 [-1.333, 0.667] | -0.167 [-0.833, 0.500] |
| EleutherAI/pythia-1.4b | B | 1800 | -0.500 | -0.500 [-1.667, 0.000] | -0.500 [-1.667, 0.000] |
| Qwen/Qwen2.5-0.5B | A | 1800 | 7.333 | 9.500 [7.167, 11.500] | 9.500 [7.167, 11.500] |
| Qwen/Qwen2.5-0.5B | B | 1800 | 4.833 | 2.000 [0.000, 5.333] | 2.000 [0.000, 5.333] |

Beta0: reteste completo existente, semente0; ICs novos somente em CPU, nenhuma inferencia refeita.

| modelo | dtype | itens | base certa | legado beta0 certo | corrigido beta0 certo | ganho IC95 pp | McNemar Holm5 p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gpt2 | torch.float32 | 3200 | 1150/3200 | 1431/3200 | 1431/3200 | 8.781 [6.656, 10.812] | 5.17e-15 |
| gpt2-medium | torch.float32 | 3200 | 1399/3200 | 308/3200 | 310/3200 | -34.031 [-35.906, -32.031] | 1.48e-220 |
| EleutherAI/pythia-410m | torch.float32 | 3200 | 1538/3200 | 1548/3200 | 1547/3200 | 0.281 [-0.344, 0.844] | 0.537 |
| EleutherAI/pythia-1.4b | torch.float32 | 3200 | 1553/3200 | 1565/3200 | 1571/3200 | 0.562 [-0.062, 1.188] | 0.247 |
| Qwen/Qwen2.5-0.5B | torch.bfloat16 | 3200 | 1667/3200 | 1701/3200 | 1681/3200 | 0.438 [-0.312, 1.156] | 0.537 |

O colapso de acuracia do GPT-2-medium persiste com atencao valida. As verificacoes numericas corrigidas passam; os outros quatro modelos nao apresentam queda global neste teste.

Tempos internos dos jobs, excluindo a fila e as importacoes iniciais; incluem modelo, validacao e gravacao. Tempos observados pelo coordenador incluem a fila e constam no JSON operacional. Nao sao uma alegacao de custo puro de CUDA.

| grupo | jobs GPU | soma segundos internos | min | max |
| --- | --- | --- | --- | --- |
| mass | 96 | 12669.769 | 48.978 | 293.461 |
| items | 24 | 3734.634 | 48.178 | 359.286 |
| cv | 180 | 18237.715 | 26.274 | 235.773 |

Comando e tempo de cada job:

- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 0 --stop 16` — 204.076430s internos; observacao do coordenador=260.026; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d000_016_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 16 --stop 32` — 150.664609s internos; observacao do coordenador=575.035; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d016_032_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 32 --stop 48` — 140.913677s internos; observacao do coordenador=395.031; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d032_048_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 48 --stop 64` — 140.829583s internos; observacao do coordenador=250.029; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d048_064_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 64 --stop 80` — 141.191531s internos; observacao do coordenador=450.051; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d064_080_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 80 --stop 96` — 142.747707s internos; observacao do coordenador=205.037; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d080_096_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 96 --stop 112` — 145.214130s internos; observacao do coordenador=190.049; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d096_112_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 112 --stop 128` — 147.573121s internos; observacao do coordenador=1140.07; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d112_128_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 128 --stop 144` — 145.802648s internos; observacao do coordenador=370.049; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d128_144_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 144 --stop 160` — 145.675082s internos; observacao do coordenador=185.036; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d144_160_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 160 --stop 176` — 143.127479s internos; observacao do coordenador=240.044; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d160_176_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 176 --stop 192` — 142.110130s internos; observacao do coordenador=195.028; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d176_192_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 192 --stop 208` — 144.186347s internos; observacao do coordenador=185.028; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d192_208_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 208 --stop 224` — 143.917824s internos; observacao do coordenador=240.031; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d208_224_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 224 --stop 240` — 147.156709s internos; observacao do coordenador=200.029; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d224_240_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-1.4b --start 240 --stop 256` — 143.316442s internos; observacao do coordenador=175.026; resultado out/phase7_massmatched_EleutherAI__pythia-1.4b_d240_256_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 0 --stop 16` — 183.596332s internos; observacao do coordenador=1265.045; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d000_016_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 16 --stop 32` — 144.838355s internos; observacao do coordenador=205.026; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d016_032_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 32 --stop 48` — 133.002735s internos; observacao do coordenador=285.032; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d032_048_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 48 --stop 64` — 131.428402s internos; observacao do coordenador=185.031; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d048_064_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 64 --stop 80` — 133.180833s internos; observacao do coordenador=255.032; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d064_080_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 80 --stop 96` — 130.700096s internos; observacao do coordenador=195.026; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d080_096_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 96 --stop 112` — 131.607351s internos; observacao do coordenador=395.045; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d096_112_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 112 --stop 128` — 144.322521s internos; observacao do coordenador=470.044; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d112_128_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 128 --stop 144` — 134.225739s internos; observacao do coordenador=810.049; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d128_144_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 144 --stop 160` — 138.451452s internos; observacao do coordenador=250.034; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d144_160_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 160 --stop 176` — 142.981252s internos; observacao do coordenador=185.026; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d160_176_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 176 --stop 192` — 136.133905s internos; observacao do coordenador=190.03; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d176_192_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 192 --stop 208` — 137.018969s internos; observacao do coordenador=250.038; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d192_208_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 208 --stop 224` — 135.253778s internos; observacao do coordenador=170.028; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d208_224_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 224 --stop 240` — 142.468003s internos; observacao do coordenador=195.031; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d224_240_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model EleutherAI/pythia-410m --start 240 --stop 256` — 133.995711s internos; observacao do coordenador=245.025; resultado out/phase7_massmatched_EleutherAI__pythia-410m_d240_256_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 0 --stop 16` — 175.414587s internos; observacao do coordenador=6030.169; resultado out/phase7_massmatched_gpt2-medium_d000_016_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 16 --stop 32` — 142.707851s internos; observacao do coordenador=175.032; resultado out/phase7_massmatched_gpt2-medium_d016_032_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 32 --stop 48` — 124.586242s internos; observacao do coordenador=225.029; resultado out/phase7_massmatched_gpt2-medium_d032_048_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 48 --stop 64` — 124.541257s internos; observacao do coordenador=190.025; resultado out/phase7_massmatched_gpt2-medium_d048_064_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 64 --stop 80` — 132.846783s internos; observacao do coordenador=385.046; resultado out/phase7_massmatched_gpt2-medium_d064_080_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 80 --stop 96` — 123.798942s internos; observacao do coordenador=180.033; resultado out/phase7_massmatched_gpt2-medium_d080_096_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 96 --stop 112` — 123.017215s internos; observacao do coordenador=630.042; resultado out/phase7_massmatched_gpt2-medium_d096_112_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 112 --stop 128` — 127.353166s internos; observacao do coordenador=515.048; resultado out/phase7_massmatched_gpt2-medium_d112_128_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 128 --stop 144` — 133.115889s internos; observacao do coordenador=460.035; resultado out/phase7_massmatched_gpt2-medium_d128_144_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 144 --stop 160` — 133.478962s internos; observacao do coordenador=970.048; resultado out/phase7_massmatched_gpt2-medium_d144_160_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 160 --stop 176` — 126.762227s internos; observacao do coordenador=400.036; resultado out/phase7_massmatched_gpt2-medium_d160_176_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 176 --stop 192` — 126.171741s internos; observacao do coordenador=185.029; resultado out/phase7_massmatched_gpt2-medium_d176_192_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 192 --stop 208` — 132.022483s internos; observacao do coordenador=350.03; resultado out/phase7_massmatched_gpt2-medium_d192_208_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 208 --stop 224` — 127.674769s internos; observacao do coordenador=240.053; resultado out/phase7_massmatched_gpt2-medium_d208_224_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 224 --stop 240` — 133.247981s internos; observacao do coordenador=190.062; resultado out/phase7_massmatched_gpt2-medium_d224_240_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2-medium --start 240 --stop 256` — 126.667897s internos; observacao do coordenador=345.029; resultado out/phase7_massmatched_gpt2-medium_d240_256_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 0 --stop 16` — 69.993293s internos; observacao do coordenador=4290.41; resultado out/phase7_massmatched_gpt2_d000_016_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 16 --stop 32` — 62.229503s internos; observacao do coordenador=260.044; resultado out/phase7_massmatched_gpt2_d016_032_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 32 --stop 48` — 50.068930s internos; observacao do coordenador=135.022; resultado out/phase7_massmatched_gpt2_d032_048_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 48 --stop 64` — 48.977766s internos; observacao do coordenador=850.049; resultado out/phase7_massmatched_gpt2_d048_064_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 64 --stop 80` — 49.208952s internos; observacao do coordenador=370.033; resultado out/phase7_massmatched_gpt2_d064_080_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 80 --stop 96` — 48.985785s internos; observacao do coordenador=175.028; resultado out/phase7_massmatched_gpt2_d080_096_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 96 --stop 112` — 50.768014s internos; observacao do coordenador=400.031; resultado out/phase7_massmatched_gpt2_d096_112_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 112 --stop 128` — 52.925080s internos; observacao do coordenador=710.046; resultado out/phase7_massmatched_gpt2_d112_128_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 128 --stop 144` — 53.603728s internos; observacao do coordenador=815.044; resultado out/phase7_massmatched_gpt2_d128_144_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 144 --stop 160` — 50.134126s internos; observacao do coordenador=400.034; resultado out/phase7_massmatched_gpt2_d144_160_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 160 --stop 176` — 51.585633s internos; observacao do coordenador=295.042; resultado out/phase7_massmatched_gpt2_d160_176_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 176 --stop 192` — 50.460317s internos; observacao do coordenador=165.04; resultado out/phase7_massmatched_gpt2_d176_192_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 192 --stop 208` — 51.588124s internos; observacao do coordenador=150.026; resultado out/phase7_massmatched_gpt2_d192_208_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 208 --stop 224` — 51.269444s internos; observacao do coordenador=275.035; resultado out/phase7_massmatched_gpt2_d208_224_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 224 --stop 240` — 51.638585s internos; observacao do coordenador=175.033; resultado out/phase7_massmatched_gpt2_d224_240_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model gpt2 --start 240 --stop 256` — 50.300366s internos; observacao do coordenador=145.028; resultado out/phase7_massmatched_gpt2_d240_256_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 0 --stop 16` — 179.239694s internos; observacao do coordenador=260.031; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d000_016_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 16 --stop 32` — 124.912173s internos; observacao do coordenador=230.025; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d016_032_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 32 --stop 48` — 110.356166s internos; observacao do coordenador=200.038; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d032_048_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 48 --stop 64` — 110.322608s internos; observacao do coordenador=430.036; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d048_064_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 64 --stop 80` — 111.505325s internos; observacao do coordenador=385.039; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d064_080_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 80 --stop 96` — 116.812364s internos; observacao do coordenador=330.03; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d080_096_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 96 --stop 112` — 110.646193s internos; observacao do coordenador=860.137; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d096_112_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 112 --stop 128` — 116.823548s internos; observacao do coordenador=760.088; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d112_128_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 128 --stop 144` — 118.900933s internos; observacao do coordenador=565.055; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d128_144_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 144 --stop 160` — 126.620515s internos; observacao do coordenador=225.03; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d144_160_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 160 --stop 176` — 117.716977s internos; observacao do coordenador=210.027; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d160_176_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 176 --stop 192` — 112.982608s internos; observacao do coordenador=150.032; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d176_192_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 192 --stop 208` — 116.359175s internos; observacao do coordenador=215.03; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d192_208_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 208 --stop 224` — 114.053151s internos; observacao do coordenador=205.025; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d208_224_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 224 --stop 240` — 113.887780s internos; observacao do coordenador=155.024; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d224_240_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-0.5B --start 240 --stop 256` — 113.069682s internos; observacao do coordenador=210.025; resultado out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d240_256_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 0 --stop 16` — 293.461366s internos; observacao do coordenador=395.06; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d000_016_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 16 --stop 32` — 197.874126s internos; observacao do coordenador=220.029; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d016_032_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 32 --stop 48` — 187.503100s internos; observacao do coordenador=255.024; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d032_048_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 48 --stop 64` — 186.519360s internos; observacao do coordenador=430.035; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d048_064_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 64 --stop 80` — 185.401772s internos; observacao do coordenador=715.055; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d064_080_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 80 --stop 96` — 187.965033s internos; observacao do coordenador=710.064; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d080_096_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 96 --stop 112` — 186.985542s internos; observacao do coordenador=455.039; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d096_112_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 112 --stop 128` — 208.096368s internos; observacao do coordenador=1205.067; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d112_128_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 128 --stop 144` — 191.186483s internos; observacao do coordenador=550.034; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d128_144_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 144 --stop 160` — 214.402054s internos; observacao do coordenador=310.046; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d144_160_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 160 --stop 176` — 199.467025s internos; observacao do coordenador=420.036; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d160_176_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 176 --stop 192` — 189.816437s internos; observacao do coordenador=285.029; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d176_192_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 192 --stop 208` — 188.767774s internos; observacao do coordenador=275.036; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d192_208_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 208 --stop 224` — 198.600189s internos; observacao do coordenador=420.032; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d208_224_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 224 --stop 240` — 189.937603s internos; observacao do coordenador=280.035; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d224_240_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase37_mass_matched.py --model Qwen/Qwen2.5-3B --start 240 --stop 256` — 190.721250s internos; observacao do coordenador=280.026; resultado out/phase7_massmatched_Qwen__Qwen2.5-3B_d240_256_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 0 --variant historical` — 359.236830s internos; observacao do coordenador=525.031; resultado out/phase8_items_EleutherAI__pythia-1.4b_s0_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 1 --variant historical` — 359.286035s internos; observacao do coordenador=370.028; resultado out/phase8_items_EleutherAI__pythia-1.4b_s1_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-1.4b --seed 2 --variant historical` — 358.810234s internos; observacao do coordenador=1810.063; resultado out/phase8_items_EleutherAI__pythia-1.4b_s2_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 0 --variant historical` — 119.972030s internos; observacao do coordenador=195.024; resultado out/phase8_items_EleutherAI__pythia-410m_s0_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 1 --variant historical` — 120.507492s internos; observacao do coordenador=230.027; resultado out/phase8_items_EleutherAI__pythia-410m_s1_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model EleutherAI/pythia-410m --seed 2 --variant historical` — 119.190762s internos; observacao do coordenador=1025.039; resultado out/phase8_items_EleutherAI__pythia-410m_s2_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 0 --variant historical` — 128.315042s internos; observacao do coordenador=775.034; resultado out/phase8_items_gpt2-medium_s0_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 1 --variant historical` — 129.292817s internos; observacao do coordenador=340.03; resultado out/phase8_items_gpt2-medium_s1_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2-medium --seed 2 --variant historical` — 128.119346s internos; observacao do coordenador=320.027; resultado out/phase8_items_gpt2-medium_s2_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2 --seed 0 --variant historical` — 48.178443s internos; observacao do coordenador=None; resultado out/phase8_items_gpt2_s0_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2 --seed 1 --variant historical` — 48.893135s internos; observacao do coordenador=140.027; resultado out/phase8_items_gpt2_s1_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model gpt2 --seed 2 --variant historical` — 48.413833s internos; observacao do coordenador=170.025; resultado out/phase8_items_gpt2_s2_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical` — 172.841842s internos; observacao do coordenador=460.035; resultado out/phase8_items_Qwen__Qwen2.5-0.5B_s0_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16` — 64.961088s internos; observacao do coordenador=310.047; resultado out/phase8_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical` — 172.164788s internos; observacao do coordenador=285.033; resultado out/phase8_items_Qwen__Qwen2.5-0.5B_s1_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16` — 64.896195s internos; observacao do coordenador=175.026; resultado out/phase8_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical` — 172.101386s internos; observacao do coordenador=235.035; resultado out/phase8_items_Qwen__Qwen2.5-0.5B_s2_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase8 --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16` — 64.892456s internos; observacao do coordenador=260.03; resultado out/phase8_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 0 --variant historical` — 111.312785s internos; observacao do coordenador=205.026; resultado out/phase11_items_gpt2-medium_s0_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 1 --variant historical` — 111.507290s internos; observacao do coordenador=310.03; resultado out/phase11_items_gpt2-medium_s1_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model gpt2-medium --seed 2 --variant historical` — 111.010212s internos; observacao do coordenador=185.03; resultado out/phase11_items_gpt2-medium_s2_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 0 --variant historical` — 241.267392s internos; observacao do coordenador=315.026; resultado out/phase11_items_Qwen__Qwen2.5-3B_s0_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 1 --variant historical` — 239.708356s internos; observacao do coordenador=340.036; resultado out/phase11_items_Qwen__Qwen2.5-3B_s1_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase38_paired_items.py --task phase11 --model Qwen/Qwen2.5-3B --seed 2 --variant historical` — 239.754153s internos; observacao do coordenador=355.032; resultado out/phase11_items_Qwen__Qwen2.5-3B_s2_historical_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.05` — 228.270517s internos; observacao do coordenador=225.023; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.0` — 216.035378s internos; observacao do coordenador=215.024; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.15` — 228.303337s internos; observacao do coordenador=275.032; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.1` — 228.046933s internos; observacao do coordenador=270.034; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.25` — 228.761358s internos; observacao do coordenador=530.043; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.35` — 235.772562s internos; observacao do coordenador=545.135; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.5` — 228.061035s internos; observacao do coordenador=385.038; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 0.75` — 228.473898s internos; observacao do coordenador=260.031; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta 1.0` — 215.949124s internos; observacao do coordenador=385.03; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 0 --variant historical --beta legacy_beta0` — 200.163737s internos; observacao do coordenador=200.022; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.05` — 228.141473s internos; observacao do coordenador=225.025; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.0` — 216.197458s internos; observacao do coordenador=215.028; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.15` — 228.140925s internos; observacao do coordenador=410.034; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.1` — 227.930522s internos; observacao do coordenador=400.035; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.25` — 230.358067s internos; observacao do coordenador=455.062; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.35` — 228.729951s internos; observacao do coordenador=590.04; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.5` — 229.513588s internos; observacao do coordenador=395.11; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 0.75` — 228.306656s internos; observacao do coordenador=290.026; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta 1.0` — 216.971874s internos; observacao do coordenador=325.026; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 1 --variant historical --beta legacy_beta0` — 200.552371s internos; observacao do coordenador=200.025; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.05` — 228.431005s internos; observacao do coordenador=225.026; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.0` — 215.973921s internos; observacao do coordenador=215.025; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.15` — 233.291605s internos; observacao do coordenador=340.041; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.1` — 228.191602s internos; observacao do coordenador=225.025; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.25` — 229.114729s internos; observacao do coordenador=345.027; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.35` — 228.955846s internos; observacao do coordenador=895.088; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.5` — 228.018430s internos; observacao do coordenador=520.034; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 0.75` — 228.071630s internos; observacao do coordenador=380.027; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta 1.0` — 215.314154s internos; observacao do coordenador=350.046; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-1.4b --seed 2 --variant historical --beta legacy_beta0` — 200.294767s internos; observacao do coordenador=200.024; resultado out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.05` — 93.197386s internos; observacao do coordenador=95.02; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.0` — 81.474871s internos; observacao do coordenador=85.02; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.15` — 93.890783s internos; observacao do coordenador=275.03; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.1` — 93.180562s internos; observacao do coordenador=280.031; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.25` — 93.411324s internos; observacao do coordenador=530.045; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.35` — 93.714476s internos; observacao do coordenador=700.167; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.5` — 93.522770s internos; observacao do coordenador=350.031; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 0.75` — 93.576499s internos; observacao do coordenador=275.031; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta 1.0` — 80.165697s internos; observacao do coordenador=185.021; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 0 --variant historical --beta legacy_beta0` — 64.590636s internos; observacao do coordenador=70.022; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.05` — 93.255371s internos; observacao do coordenador=95.022; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.0` — 81.546086s internos; observacao do coordenador=85.022; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.15` — 94.195206s internos; observacao do coordenador=210.029; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.1` — 93.042343s internos; observacao do coordenador=205.056; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.25` — 95.257564s internos; observacao do coordenador=225.027; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.35` — 93.622171s internos; observacao do coordenador=830.052; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.5` — 93.217379s internos; observacao do coordenador=420.069; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 0.75` — 93.297391s internos; observacao do coordenador=280.025; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta 1.0` — 80.090774s internos; observacao do coordenador=395.086; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 1 --variant historical --beta legacy_beta0` — 64.623938s internos; observacao do coordenador=70.02; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.05` — 93.223125s internos; observacao do coordenador=95.022; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.0` — 81.464428s internos; observacao do coordenador=85.022; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.15` — 93.113929s internos; observacao do coordenador=235.042; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.1` — 93.202360s internos; observacao do coordenador=95.023; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.25` — 93.109704s internos; observacao do coordenador=230.031; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.35` — 95.094888s internos; observacao do coordenador=1135.061; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.5` — 93.311793s internos; observacao do coordenador=440.134; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 0.75` — 93.452502s internos; observacao do coordenador=1015.042; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta 1.0` — 79.989197s internos; observacao do coordenador=125.024; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model EleutherAI/pythia-410m --seed 2 --variant historical --beta legacy_beta0` — 64.505870s internos; observacao do coordenador=70.021; resultado out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.05` — 100.228022s internos; observacao do coordenador=105.022; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.0` — 87.807545s internos; observacao do coordenador=90.02; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.15` — 100.131921s internos; observacao do coordenador=215.03; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.1` — 100.059380s internos; observacao do coordenador=210.028; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.25` — 110.624043s internos; observacao do coordenador=635.045; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.35` — 103.849349s internos; observacao do coordenador=395.03; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.5` — 100.053543s internos; observacao do coordenador=245.032; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 0.75` — 100.348061s internos; observacao do coordenador=275.028; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta 1.0` — 86.063078s internos; observacao do coordenador=1315.048; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 0 --variant historical --beta legacy_beta0` — 70.572814s internos; observacao do coordenador=75.02; resultado out/phase18_posbatch_items_gpt2-medium_s0_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.05` — 100.136944s internos; observacao do coordenador=105.023; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.0` — 87.966330s internos; observacao do coordenador=90.027; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.15` — 100.188475s internos; observacao do coordenador=235.043; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.1` — 100.019240s internos; observacao do coordenador=235.031; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.25` — 100.197484s internos; observacao do coordenador=240.035; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.35` — 100.553745s internos; observacao do coordenador=275.029; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.5` — 100.338927s internos; observacao do coordenador=240.031; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 0.75` — 100.433541s internos; observacao do coordenador=400.031; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta 1.0` — 86.809669s internos; observacao do coordenador=505.037; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 1 --variant historical --beta legacy_beta0` — 70.686879s internos; observacao do coordenador=75.02; resultado out/phase18_posbatch_items_gpt2-medium_s1_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.05` — 100.180477s internos; observacao do coordenador=105.021; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.0` — 87.891166s internos; observacao do coordenador=90.02; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.15` — 100.466455s internos; observacao do coordenador=230.028; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.1` — 100.166644s internos; observacao do coordenador=105.022; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.25` — 101.366752s internos; observacao do coordenador=240.034; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.35` — 100.625251s internos; observacao do coordenador=525.077; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.5` — 100.318533s internos; observacao do coordenador=320.041; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 0.75` — 100.317546s internos; observacao do coordenador=260.039; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta 1.0` — 86.171990s internos; observacao do coordenador=220.024; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2-medium --seed 2 --variant historical --beta legacy_beta0` — 70.593817s internos; observacao do coordenador=75.021; resultado out/phase18_posbatch_items_gpt2-medium_s2_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.05` — 37.791953s internos; observacao do coordenador=45.021; resultado out/phase18_posbatch_items_gpt2_s0_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.0` — 33.091660s internos; observacao do coordenador=40.021; resultado out/phase18_posbatch_items_gpt2_s0_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.15` — 38.148731s internos; observacao do coordenador=180.039; resultado out/phase18_posbatch_items_gpt2_s0_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.1` — 38.416258s internos; observacao do coordenador=180.028; resultado out/phase18_posbatch_items_gpt2_s0_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.25` — 38.027733s internos; observacao do coordenador=355.035; resultado out/phase18_posbatch_items_gpt2_s0_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.35` — 38.463079s internos; observacao do coordenador=190.045; resultado out/phase18_posbatch_items_gpt2_s0_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.5` — 37.919851s internos; observacao do coordenador=165.027; resultado out/phase18_posbatch_items_gpt2_s0_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 0.75` — 38.302461s internos; observacao do coordenador=365.028; resultado out/phase18_posbatch_items_gpt2_s0_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta 1.0` — 32.385859s internos; observacao do coordenador=785.032; resultado out/phase18_posbatch_items_gpt2_s0_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 0 --variant historical --beta legacy_beta0` — 26.273932s internos; observacao do coordenador=35.021; resultado out/phase18_posbatch_items_gpt2_s0_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.05` — 37.899697s internos; observacao do coordenador=45.02; resultado out/phase18_posbatch_items_gpt2_s1_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.0` — 33.129793s internos; observacao do coordenador=40.021; resultado out/phase18_posbatch_items_gpt2_s1_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.15` — 37.996791s internos; observacao do coordenador=175.028; resultado out/phase18_posbatch_items_gpt2_s1_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.1` — 37.900809s internos; observacao do coordenador=170.023; resultado out/phase18_posbatch_items_gpt2_s1_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.25` — 38.027192s internos; observacao do coordenador=180.027; resultado out/phase18_posbatch_items_gpt2_s1_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.35` — 38.043633s internos; observacao do coordenador=315.03; resultado out/phase18_posbatch_items_gpt2_s1_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.5` — 37.806544s internos; observacao do coordenador=350.038; resultado out/phase18_posbatch_items_gpt2_s1_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 0.75` — 37.871420s internos; observacao do coordenador=150.037; resultado out/phase18_posbatch_items_gpt2_s1_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta 1.0` — 33.033496s internos; observacao do coordenador=195.026; resultado out/phase18_posbatch_items_gpt2_s1_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 1 --variant historical --beta legacy_beta0` — 26.304678s internos; observacao do coordenador=35.022; resultado out/phase18_posbatch_items_gpt2_s1_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.05` — 37.886342s internos; observacao do coordenador=45.02; resultado out/phase18_posbatch_items_gpt2_s2_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.0` — 33.103086s internos; observacao do coordenador=40.021; resultado out/phase18_posbatch_items_gpt2_s2_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.15` — 37.898199s internos; observacao do coordenador=165.036; resultado out/phase18_posbatch_items_gpt2_s2_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.1` — 37.824482s internos; observacao do coordenador=45.02; resultado out/phase18_posbatch_items_gpt2_s2_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.25` — 38.492265s internos; observacao do coordenador=170.03; resultado out/phase18_posbatch_items_gpt2_s2_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.35` — 39.217059s internos; observacao do coordenador=435.049; resultado out/phase18_posbatch_items_gpt2_s2_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.5` — 38.030598s internos; observacao do coordenador=305.04; resultado out/phase18_posbatch_items_gpt2_s2_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 0.75` — 38.075793s internos; observacao do coordenador=245.025; resultado out/phase18_posbatch_items_gpt2_s2_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta 1.0` — 32.848133s internos; observacao do coordenador=260.023; resultado out/phase18_posbatch_items_gpt2_s2_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model gpt2 --seed 2 --variant historical --beta legacy_beta0` — 26.311001s internos; observacao do coordenador=35.02; resultado out/phase18_posbatch_items_gpt2_s2_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.05` — 117.525713s internos; observacao do coordenador=120.023; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.0` — 106.406605s internos; observacao do coordenador=110.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.15` — 118.685290s internos; observacao do coordenador=250.031; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.1` — 117.152954s internos; observacao do coordenador=240.031; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.25` — 118.196052s internos; observacao do coordenador=860.045; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.35` — 118.439861s internos; observacao do coordenador=510.042; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.5` — 117.689592s internos; observacao do coordenador=200.033; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 0.75` — 118.008077s internos; observacao do coordenador=210.022; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta 1.0` — 105.662649s internos; observacao do coordenador=425.03; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant historical --beta legacy_beta0` — 90.898178s internos; observacao do coordenador=95.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.05` — 55.479720s internos; observacao do coordenador=60.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.0` — 47.554020s internos; observacao do coordenador=55.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.15` — 58.639265s internos; observacao do coordenador=110.025; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.1` — 55.100925s internos; observacao do coordenador=60.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.25` — 56.640283s internos; observacao do coordenador=110.029; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.35` — 59.562138s internos; observacao do coordenador=750.118; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.5` — 55.925119s internos; observacao do coordenador=110.123; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 0.75` — 55.325005s internos; observacao do coordenador=790.05; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta 1.0` — 46.337675s internos; observacao do coordenador=240.029; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 0 --variant standard_bf16 --beta legacy_beta0` — 33.093733s internos; observacao do coordenador=40.02; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.05` — 117.437020s internos; observacao do coordenador=120.023; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.0` — 106.406914s internos; observacao do coordenador=110.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.15` — 117.939556s internos; observacao do coordenador=165.031; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.1` — 117.459102s internos; observacao do coordenador=120.025; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.25` — 117.897700s internos; observacao do coordenador=325.032; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.35` — 119.973172s internos; observacao do coordenador=600.089; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.5` — 117.390463s internos; observacao do coordenador=275.041; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 0.75` — 117.749021s internos; observacao do coordenador=295.03; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta 1.0` — 105.056144s internos; observacao do coordenador=160.179; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant historical --beta legacy_beta0` — 90.820098s internos; observacao do coordenador=95.027; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.05` — 55.127961s internos; observacao do coordenador=60.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.0` — 47.477622s internos; observacao do coordenador=55.02; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.15` — 57.695476s internos; observacao do coordenador=185.027; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.1` — 55.181344s internos; observacao do coordenador=60.026; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.25` — 55.851757s internos; observacao do coordenador=180.026; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.35` — 56.086006s internos; observacao do coordenador=455.043; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.5` — 55.026420s internos; observacao do coordenador=185.026; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 0.75` — 55.593222s internos; observacao do coordenador=230.026; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta 1.0` — 45.800079s internos; observacao do coordenador=170.039; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 1 --variant standard_bf16 --beta legacy_beta0` — 33.042149s internos; observacao do coordenador=40.02; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.05` — 117.484955s internos; observacao do coordenador=120.022; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.0` — 106.299056s internos; observacao do coordenador=110.022; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.15` — 122.708388s internos; observacao do coordenador=315.033; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.1` — 117.432627s internos; observacao do coordenador=120.025; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.25` — 118.323070s internos; observacao do coordenador=310.05; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.35` — 124.807862s internos; observacao do coordenador=1100.054; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.5` — 117.499132s internos; observacao do coordenador=605.038; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 0.75` — 118.073792s internos; observacao do coordenador=1725.059; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta 1.0` — 105.595622s internos; observacao do coordenador=555.028; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant historical --beta legacy_beta0` — 90.692109s internos; observacao do coordenador=95.022; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_blegacy_beta0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.05` — 55.171117s internos; observacao do coordenador=60.02; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.05_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.0` — 47.757716s internos; observacao do coordenador=55.023; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.15` — 57.378815s internos; observacao do coordenador=200.061; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.15_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.1` — 55.045104s internos; observacao do coordenador=60.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.1_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.25` — 55.598495s internos; observacao do coordenador=190.028; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.25_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.35` — 55.779095s internos; observacao do coordenador=810.048; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.35_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.5` — 56.951495s internos; observacao do coordenador=190.033; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.5_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 0.75` — 55.618001s internos; observacao do coordenador=195.025; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.75_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta 1.0` — 45.791605s internos; observacao do coordenador=230.026; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b1.0_v3.json
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase45_currentcv_items.py --model Qwen/Qwen2.5-0.5B --seed 2 --variant standard_bf16 --beta legacy_beta0` — 33.003132s internos; observacao do coordenador=40.021; resultado out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_blegacy_beta0_v3.json

Sanidades: auditoria final passou nos 300 jobs principais; identidades exatas, mascara e soma de linhas, linha0 preservada, igualdade de massa, pares/IDs/targets, hashes, bootstrap e testes. O braco legado beta0 e deliberadamente invalido e so diagnostico. A reproducao historica de B da CV falhou e permanece registrada, separada da validade numerica.

Inventario de arquivos, um por linha, com tamanho e SHA256:

- beta0_statistics_v3.py — 3988 bytes; SHA256 8308dc3ab95219fd377fc657f0b95c1fa5be10f0649380579a04edb5dc35da5f
- data/attn/phase11_items_gpt2-medium_s0_v3.manifest.json — 1692 bytes; SHA256 191fee545fa5a1a439134f5fcfa1b665d6c467919db30bf043e63f5d40154cc9
- data/attn/phase11_items_gpt2-medium_s0_v3.npz — 598867 bytes; SHA256 923579724f3a4e259e3792860566b3a9d4a351df2f01a91dfa309bc24f5ddb96
- data/attn/phase11_items_gpt2-medium_s1_v3.manifest.json — 1692 bytes; SHA256 d213fd18dfc6514c8fc28c1c964cc3a2ea72b212370bfed93f595a4244b010d0
- data/attn/phase11_items_gpt2-medium_s1_v3.npz — 600238 bytes; SHA256 9a082a2fcb00d97b670d8d3055c5fbd96e871620787b5a4db77c4592b2f9293c
- data/attn/phase11_items_gpt2-medium_s2_v3.manifest.json — 1692 bytes; SHA256 17f3a1471ead11b3576a9e7858a78debc5686ea178a2f656d20f8f37ec03ad9e
- data/attn/phase11_items_gpt2-medium_s2_v3.npz — 598415 bytes; SHA256 9b7a12c852efadcab8005395a9f71d0374d66cd994635336495558068f9305ea
- data/attn/phase11_items_Qwen__Qwen2.5-3B_s0_v3.manifest.json — 1696 bytes; SHA256 8cf059a252e3935909da19d535b3ca766a430f7121bcc35c8ac54b4993107335
- data/attn/phase11_items_Qwen__Qwen2.5-3B_s0_v3.npz — 589599 bytes; SHA256 2a9e327655924cbec78cedf92eb4e69fa84b7ba8f8e594a996ea73242d24b63b
- data/attn/phase11_items_Qwen__Qwen2.5-3B_s1_v3.manifest.json — 1696 bytes; SHA256 ce562e034ae11e7a1e52884079a3dc1595df842b11e3017b981ac9f16fff32c6
- data/attn/phase11_items_Qwen__Qwen2.5-3B_s1_v3.npz — 589977 bytes; SHA256 c7326c2c0781f77b449514ea3c1212449988d7ff3701d2967c3795646b9d6ff1
- data/attn/phase11_items_Qwen__Qwen2.5-3B_s2_v3.manifest.json — 1696 bytes; SHA256 f766852eecc875532730fc9a2e486552df32b564a1272c0dc21576ff09c0a6eb
- data/attn/phase11_items_Qwen__Qwen2.5-3B_s2_v3.npz — 589592 bytes; SHA256 9d6196d27bcda471d513aa49701d427b435dfa7475e93378fb951c2f7f5c05a7
- data/attn/phase18_items_EleutherAI__pythia-1.4b_s0_v3.manifest.json — 2090 bytes; SHA256 fb1830b5305f40e50e445868d826d6e6b6be026cafd185dbb6fb3e26ffe509c4
- data/attn/phase18_items_EleutherAI__pythia-1.4b_s0_v3.npz — 850887 bytes; SHA256 311169eb0589a68144dca923734262aebead7b94acd58d0c85016febee344595
- data/attn/phase18_items_EleutherAI__pythia-1.4b_s1_v3.manifest.json — 2090 bytes; SHA256 82d30ed1b2c2849ad1c03a91ee356a0847e93e92d308d7e96a5e22a1710ec014
- data/attn/phase18_items_EleutherAI__pythia-1.4b_s1_v3.npz — 854105 bytes; SHA256 74a7d70ea3bfda3ea905b2b79076bc6f3489054c930bf6456729c1025f84aa21
- data/attn/phase18_items_EleutherAI__pythia-1.4b_s2_v3.manifest.json — 2090 bytes; SHA256 52ada35c5df606b2dcdd47f00f658d172615402547d34579bcc2a5e5c6e242f4
- data/attn/phase18_items_EleutherAI__pythia-1.4b_s2_v3.npz — 850197 bytes; SHA256 6cf7fb91c8dfb0d9c8740155bb32cefa4f4c29beed6126e763efe8a5544274fd
- data/attn/phase18_items_EleutherAI__pythia-410m_s0_v3.manifest.json — 2090 bytes; SHA256 d7f91f99013c8debb1b63e085da257e79c00bc299c10ce994a78ac28cd251672
- data/attn/phase18_items_EleutherAI__pythia-410m_s0_v3.npz — 850887 bytes; SHA256 311169eb0589a68144dca923734262aebead7b94acd58d0c85016febee344595
- data/attn/phase18_items_EleutherAI__pythia-410m_s1_v3.manifest.json — 2090 bytes; SHA256 e8dd823da876e01ba34b13666e1e34124fe029e58df518bd23ecdfea6b0a870e
- data/attn/phase18_items_EleutherAI__pythia-410m_s1_v3.npz — 854105 bytes; SHA256 74a7d70ea3bfda3ea905b2b79076bc6f3489054c930bf6456729c1025f84aa21
- data/attn/phase18_items_EleutherAI__pythia-410m_s2_v3.manifest.json — 2090 bytes; SHA256 a78ffbb5f5d1b55f60b7ff663b10b6e431b646e357bec8454c3d47372f4b1e93
- data/attn/phase18_items_EleutherAI__pythia-410m_s2_v3.npz — 850197 bytes; SHA256 6cf7fb91c8dfb0d9c8740155bb32cefa4f4c29beed6126e763efe8a5544274fd
- data/attn/phase18_items_gpt2-medium_s0_v3.manifest.json — 2079 bytes; SHA256 74ec2196b702bb9914defbc0f42094b8b2c1a3407355886776dfd767355e7851
- data/attn/phase18_items_gpt2-medium_s0_v3.npz — 846984 bytes; SHA256 d79ad016e37a8a97b04501302df530f855d91833a657ad716e79b86ccadba054
- data/attn/phase18_items_gpt2-medium_s1_v3.manifest.json — 2079 bytes; SHA256 a27ee0bc7f85a48c99ff2460670668c90649d8601f69c76b7e55cb1b84ef5078
- data/attn/phase18_items_gpt2-medium_s1_v3.npz — 848756 bytes; SHA256 9d3aaece34dea5ced4639b29048b318feb08c5015333253971c4d6e2f71c9eef
- data/attn/phase18_items_gpt2-medium_s2_v3.manifest.json — 2079 bytes; SHA256 ab9fd8b85c571b3694bae47e4a4f2a2801712d136ee4aae5774f64d86933de59
- data/attn/phase18_items_gpt2-medium_s2_v3.npz — 846197 bytes; SHA256 db0e04401998348a95bd58da17073092451594ca403c52490a2a2e0848a983e4
- data/attn/phase18_items_gpt2_s0_v3.manifest.json — 2072 bytes; SHA256 e003aef58f6c2ed2448b79d215e4eee65f33c9b4b16930a676b33d0d2d0b9fa4
- data/attn/phase18_items_gpt2_s0_v3.npz — 846984 bytes; SHA256 d79ad016e37a8a97b04501302df530f855d91833a657ad716e79b86ccadba054
- data/attn/phase18_items_gpt2_s1_v3.manifest.json — 2072 bytes; SHA256 3c4cfe603d8492a1d0afa8400da14e1f6823c3b4162d472ab5e0d1e4bab46225
- data/attn/phase18_items_gpt2_s1_v3.npz — 848756 bytes; SHA256 9d3aaece34dea5ced4639b29048b318feb08c5015333253971c4d6e2f71c9eef
- data/attn/phase18_items_gpt2_s2_v3.manifest.json — 2072 bytes; SHA256 70ff542b0e189538ee7435b0c03330ef15c2058e9d285d22097b0577e695783b
- data/attn/phase18_items_gpt2_s2_v3.npz — 846197 bytes; SHA256 db0e04401998348a95bd58da17073092451594ca403c52490a2a2e0848a983e4
- data/attn/phase18_items_Qwen__Qwen2.5-0.5B_s0_v3.manifest.json — 2085 bytes; SHA256 f70861e670cf4b2b9a8aedb24341580f099a850b6c9446cabcd6a7196f6974a0
- data/attn/phase18_items_Qwen__Qwen2.5-0.5B_s0_v3.npz — 829369 bytes; SHA256 7d621fd1039136bdcdd26b3b34e99422b2d6eb47e67d301c5f0818a1e412c1fa
- data/attn/phase18_items_Qwen__Qwen2.5-0.5B_s1_v3.manifest.json — 2085 bytes; SHA256 47d7c962759c7f581cf869e2300a1f334af6555126827d1c64302fa82c006858
- data/attn/phase18_items_Qwen__Qwen2.5-0.5B_s1_v3.npz — 831899 bytes; SHA256 6fa33d5d07edcb0d1e07994952e47d2144c991558a5df33eb676f624b2e38a31
- data/attn/phase18_items_Qwen__Qwen2.5-0.5B_s2_v3.manifest.json — 2085 bytes; SHA256 a4bcdf241115ea00e1901e1426a0197ce825cc2ef38eb65e8d2e33181c04ffa9
- data/attn/phase18_items_Qwen__Qwen2.5-0.5B_s2_v3.npz — 831793 bytes; SHA256 e24a4948e80d1a4bfebd814a3c299f995931c4aa02db3261c9e9ddf7ebf3aa44
- data/attn/phase8_items_EleutherAI__pythia-1.4b_s0_v3.manifest.json — 1801 bytes; SHA256 4f5e370448dcaf12f69e849d4fe957b0789f63580576ca84c7deddd466862c51
- data/attn/phase8_items_EleutherAI__pythia-1.4b_s0_v3.npz — 782602 bytes; SHA256 267a68f530989164200e4706653b7660e14c70128e0d8328f58419dc4785fd10
- data/attn/phase8_items_EleutherAI__pythia-1.4b_s1_v3.manifest.json — 1801 bytes; SHA256 5a6b531d51f38adaeb2b1fadc4a28b9cd54db4802dd56635e37b01fdc11078e1
- data/attn/phase8_items_EleutherAI__pythia-1.4b_s1_v3.npz — 781512 bytes; SHA256 ead205a33f50bd2b936888971df29fe5dffd6117d245d574025ed82bd9f3470a
- data/attn/phase8_items_EleutherAI__pythia-1.4b_s2_v3.manifest.json — 1801 bytes; SHA256 a825b686f4f3ac97e0ffea40cf0568f1cfe406ec641f9b62fb7b4623356ddbbe
- data/attn/phase8_items_EleutherAI__pythia-1.4b_s2_v3.npz — 783266 bytes; SHA256 a4a8377731a6b4e89c42eda41300936fbe4578def18ed7e50bb17eaff78681a5
- data/attn/phase8_items_EleutherAI__pythia-410m_s0_v3.manifest.json — 1801 bytes; SHA256 964d099541eb7a355d18cb062f35737f5216d6ebe8394989aa687851383d9028
- data/attn/phase8_items_EleutherAI__pythia-410m_s0_v3.npz — 785745 bytes; SHA256 9ac9ce4d30c3d2a715f10a14a05c8c926af7d61bfc60f04af39638d999d83bcf
- data/attn/phase8_items_EleutherAI__pythia-410m_s1_v3.manifest.json — 1801 bytes; SHA256 f74ae491dda372293129bcd3f0e29ae248a7f29e9bdb408df1020b0a1d67c1a4
- data/attn/phase8_items_EleutherAI__pythia-410m_s1_v3.npz — 783030 bytes; SHA256 594426553ea35bdc7fdd77b4219be25bcd2aad8fe4743c7b099332c6843e93dd
- data/attn/phase8_items_EleutherAI__pythia-410m_s2_v3.manifest.json — 1801 bytes; SHA256 dc90bc722a7f147464d25f40741bd08a8b39a1c33986712ba000c466e1c8b56b
- data/attn/phase8_items_EleutherAI__pythia-410m_s2_v3.npz — 782287 bytes; SHA256 deea693a8ae9532d1265080771d16aed798aa851eb4e460bd806fd102d24f39e
- data/attn/phase8_items_gpt2-medium_s0_v3.manifest.json — 1790 bytes; SHA256 ee33c023a023f8e11d8414978cc7aa666aad8bc5627e1296fa76a86ab12605ad
- data/attn/phase8_items_gpt2-medium_s0_v3.npz — 776715 bytes; SHA256 30f66a7979416bd6f05ca5d6c2ecec68479066c8e9efef5968ec026c4f22041f
- data/attn/phase8_items_gpt2-medium_s1_v3.manifest.json — 1790 bytes; SHA256 c63c281c0185a606312a259077a65b259e0a94ea695fd36aad731821c20ea3f9
- data/attn/phase8_items_gpt2-medium_s1_v3.npz — 780602 bytes; SHA256 f62d914f402426b6c5f50fcf4c95a993b3cf685f64dc0bf624da59af879b0ce2
- data/attn/phase8_items_gpt2-medium_s2_v3.manifest.json — 1790 bytes; SHA256 03a2b845f9f84d456c46ad2768f209ffb72e2943aeac1d088a5731fe295ba19a
- data/attn/phase8_items_gpt2-medium_s2_v3.npz — 773412 bytes; SHA256 d397c9d33489117da22150d52a4489b9bc40c7729f08d1f7a17df96ab3d2a01d
- data/attn/phase8_items_gpt2_s0_v3.manifest.json — 1783 bytes; SHA256 40dc4dc4fa27e987b565514c6bab271f5ae30c7a1a1fde765e40d17a7ccb64d7
- data/attn/phase8_items_gpt2_s0_v3.npz — 778885 bytes; SHA256 0c48392096a0d6cb5cd69b0ef33737880598b3caa94aa9164447398c0c836dad
- data/attn/phase8_items_gpt2_s1_v3.manifest.json — 1783 bytes; SHA256 ae83206dc8b5620c07bb3af42ebcf2aa144fb0bc34a834c0dd915862fb09e60e
- data/attn/phase8_items_gpt2_s1_v3.npz — 779125 bytes; SHA256 4f7b81ff55604be0be74b8cff64b553f9509cd243bbdfe568329031e2db07483
- data/attn/phase8_items_gpt2_s2_v3.manifest.json — 1783 bytes; SHA256 2a16bafa9f2c6f66f2cabe9b77638f047eda3fbbf4e2bc9f7c7f8ffd9156fe69
- data/attn/phase8_items_gpt2_s2_v3.npz — 780922 bytes; SHA256 bc5bff533df0f32eec37d8c5ad570cdc8550ebb3b497b72ea166f8f23d41fb61
- data/attn/phase8_items_Qwen__Qwen2.5-0.5B_s0_v3.manifest.json — 1796 bytes; SHA256 6afbd2aced89351e7cc798c7bdb56e470939a3f45481da26347cc3deb467905b
- data/attn/phase8_items_Qwen__Qwen2.5-0.5B_s0_v3.npz — 763352 bytes; SHA256 fa29ab8717e3da1e1c5012d3b46c4008de7daa85976f192c0fad33d002af03db
- data/attn/phase8_items_Qwen__Qwen2.5-0.5B_s1_v3.manifest.json — 1796 bytes; SHA256 06bdb77fbd2fc6388eea9e7d40e1abfebc652ecda5d6c0307bad90a8893402cd
- data/attn/phase8_items_Qwen__Qwen2.5-0.5B_s1_v3.npz — 762810 bytes; SHA256 a2b9fc29c2a9fdfa114456cda7445a787bb317935f7f5fbe765f8ffde9e60b6a
- data/attn/phase8_items_Qwen__Qwen2.5-0.5B_s2_v3.manifest.json — 1796 bytes; SHA256 bb81e5da67e8501df69bc37724da06d14e5d052bad6eaed3637e8d56bc2820dd
- data/attn/phase8_items_Qwen__Qwen2.5-0.5B_s2_v3.npz — 761560 bytes; SHA256 a8fc0c178ffc6076c424928f138e14764a76f70aa09f3ed51c088ebc12a4b208
- out/pairs/constancy_EleutherAI__pythia-1.4b_n128_v3.jsonl — 947416 bytes; SHA256 b9d3531c9cf50a1f9190cd7e2eaeca0ee9976a55e3be678d9470254409fb1998
- out/pairs/constancy_EleutherAI__pythia-1.4b_n256_v3.jsonl — 953912 bytes; SHA256 aad7b444285aee52a55596c0cf272cfb2a11b0718382f5c34ce9bf3afd885904
- out/pairs/constancy_EleutherAI__pythia-410m_n128_v3.jsonl — 946422 bytes; SHA256 d68196ac7e67256b196a62c2eff6abb5adab7554928245a32a37901a863b16f9
- out/pairs/constancy_EleutherAI__pythia-410m_n256_v3.jsonl — 950981 bytes; SHA256 2326402448dfc0965cd8a5ae4d01380d1fbb28935dbf2a0b12c20e3f12a64282
- out/pairs/constancy_gpt2-medium_n128_v3.jsonl — 924254 bytes; SHA256 bc6a4b3f417e419b90d6acdca6102fc1b5f7fcd5005bcb494b74ecaadf0a5ac3
- out/pairs/constancy_gpt2-medium_n256_v3.jsonl — 924432 bytes; SHA256 3ecb67d867f98b5205979f5e3ebd0bc7da621189228927d39d7e766180d5e686
- out/pairs/constancy_gpt2_n128_v3.jsonl — 911585 bytes; SHA256 fa389bb09fa3957f25de92b3d7a5ed9c3539426ec5a341911caa160cda1eea8a
- out/pairs/constancy_gpt2_n256_v3.jsonl — 911640 bytes; SHA256 cf6847c9135a2778fa1add0b27054e528ee41e5aeb27ea0d50bb509594ee5adc
- out/pairs/constancy_Qwen__Qwen2.5-0.5B_n128_v3.jsonl — 936560 bytes; SHA256 dac3e57bd447a356ba4f875416daf1743a19b328e846e1055876e463f2da3e6d
- out/pairs/constancy_Qwen__Qwen2.5-0.5B_n256_v3.jsonl — 937889 bytes; SHA256 759c164e842c9246126b31ddf1431b980efcc11eae8478774aefeac844fd8ac8
- out/pairs/constancy_Qwen__Qwen2.5-3B_n128_v3.jsonl — 1398428 bytes; SHA256 6c3010c2dc7fad9fd0766ed696c50c3da93d90320c85cc19ab9e8da189732205
- out/pairs/constancy_Qwen__Qwen2.5-3B_n256_v3.jsonl — 1398566 bytes; SHA256 ca8f449139b1dbabfabc8cc11bf2572e33d3cce85939360968f1ea4790eb2ab9
- out/pairs/constancy_Qwen__Qwen2.5-7B_n128_v3.jsonl — 1088456 bytes; SHA256 78db12332b9d0ee81b600246d9585fd01635cb17b5c60397b58f852d1c2b170e
- out/pairs/constancy_Qwen__Qwen2.5-7B_n256_v3.jsonl — 1088639 bytes; SHA256 4baed70718db1f409e3d409bb84a33a6af326d51deaa864716789500078efd89
- out/pairs/phase11_items_gpt2-medium_s0_historical_v3.jsonl — 1765501 bytes; SHA256 0b16363ddb306a3520f743537aceb1dc207d9152b4fa2634dbad0bbe62328947
- out/pairs/phase11_items_gpt2-medium_s1_historical_v3.jsonl — 1765597 bytes; SHA256 80e2acfce6c2fe61dcba3d310448492907f19267aac2af14549e73599166e77f
- out/pairs/phase11_items_gpt2-medium_s2_historical_v3.jsonl — 1765468 bytes; SHA256 c33c9c49c76374a779c33104566c3b28d6193fe477b6468ae01e8f78ae46714b
- out/pairs/phase11_items_Qwen__Qwen2.5-3B_s0_historical_v3.jsonl — 1773370 bytes; SHA256 db05c9a80d694e4108e54f30ab9e8642d7ced80edb216d44ba0312ffc531754a
- out/pairs/phase11_items_Qwen__Qwen2.5-3B_s1_historical_v3.jsonl — 1772886 bytes; SHA256 7a9916e97a3c8a7516f79a9657e255db496bb673807a659163678de4db543c0e
- out/pairs/phase11_items_Qwen__Qwen2.5-3B_s2_historical_v3.jsonl — 1773453 bytes; SHA256 3e1f5dd39f5e31e40e96ad5a1a9af0d042c66bb2081f7a94c74a6ce6a18946f5
- out/pairs/phase18_items_gpt2_s0_historical_b1.0_v3.jsonl — 1386104 bytes; SHA256 75d1e2c607bfa1d29d2ca491761f4763d17874792a02cf8a711657006ded2ead
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.05_v3.jsonl — 2361631 bytes; SHA256 d731f3d946dadff3d60b9955ec6c39db6cee54d20914f1ab5aa1bd84603b1daf
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.0_v3.jsonl — 2161710 bytes; SHA256 ca7e30da43a25faa66bd6814b86a59395a37c0de3de8dde28a9330e2a69dbd64
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.15_v3.jsonl — 2361375 bytes; SHA256 4fe2e10478cef398408733260a37905e3553395877853ddab8ae620f92c62266
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.1_v3.jsonl — 2356907 bytes; SHA256 cc99898e6bdf1bb4662d11dde38c77caf4a284ca4da035aba795897652e23745
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.25_v3.jsonl — 2361918 bytes; SHA256 9dad5f4428357f3e77463f4d5cfa327a06f132177192e12996917afe4bbb6349
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.35_v3.jsonl — 2362324 bytes; SHA256 edc4a3447bf9453e5ada6e5f05750acbf56847ce8eff0cfedca9c30b1ba98aeb
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.5_v3.jsonl — 2357508 bytes; SHA256 8f6752a4141a029bc3ad355dc8d89fb708c6c675d1c4d80f988a57a5fb800e1e
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.75_v3.jsonl — 2362323 bytes; SHA256 622712f4e674ec380c8b792502d3e720d0af8f33807f955005febace7bd8833a
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b1.0_v3.jsonl — 1629552 bytes; SHA256 56e2e95cfa97fc0e707f0875ba4934ba4662b25782f3a27c4430aa918e51000e
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_blegacy_beta0_v3.jsonl — 1375069 bytes; SHA256 09d86e4bce0034fd097a4bfc313803d06a1199dab2bc2ea023ebda229c49b88b
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.05_v3.jsonl — 2361465 bytes; SHA256 28cf6772245d433cdfa74834679e4e61ca5bb54800db45cea36807e8712f1862
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.0_v3.jsonl — 2161405 bytes; SHA256 f1952272f25d972e0d4d9aaf97daae4964e974ab05b2e4d0ce55ccc8c28de927
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.15_v3.jsonl — 2361355 bytes; SHA256 2e5a96f86740a56dbdfaa79194d16ad9b836e14a6899ce433807423bc664327e
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.1_v3.jsonl — 2356852 bytes; SHA256 780b6cbc110827ed365b8e143d7ec61b30e91181294b450526d3861ec16b142e
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.25_v3.jsonl — 2361743 bytes; SHA256 0535ab65f72de2c6f31011e30b03f45e9e2b11571095f5e9b5e1f93b5144bd87
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.35_v3.jsonl — 2362158 bytes; SHA256 9a10e1cb4696b699b1eb24e90732731e3fbf04ed0fb7076132e805da0cd98cdd
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.5_v3.jsonl — 2357361 bytes; SHA256 d55011a4e2b644c5bc9c3f48339a220dd4a09fd5032fb2a67dcc146616165083
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.75_v3.jsonl — 2362197 bytes; SHA256 513368020a1d400f6f312b6dc998d4cebdffd676111e0f5d9ed6cdc3b1576d62
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b1.0_v3.jsonl — 1629521 bytes; SHA256 a6467c9a377199ab522c62781683c623a262bacc5c686ae47c4c2172955034b0
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_blegacy_beta0_v3.jsonl — 1375028 bytes; SHA256 4d4384c12ca91a722180931e583ad913bf240aae62383b44a98b984f0095066a
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.05_v3.jsonl — 2361404 bytes; SHA256 f7de1b59634b5bba77d51071beff53f327b5adeb9014b5e763fe8bccabd8af73
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.0_v3.jsonl — 2161617 bytes; SHA256 ba37fe83a319ab9b609f4b9c86c81c17d6b831026771c925c4c59479969d73ae
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.15_v3.jsonl — 2361388 bytes; SHA256 43cc94641680148eeaf807a24c3e73f99a0f716a534e8b2ec44e5aca06f3109a
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.1_v3.jsonl — 2356921 bytes; SHA256 b9536c4aec7aaeb78f2d6ad4e3bf34cd0c739fd7baa244e01327e9f229467abf
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.25_v3.jsonl — 2361805 bytes; SHA256 0a3a2bb724be4984b8ff0ee9dcffe7882721037e75704b1de65b0b66116d0911
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.35_v3.jsonl — 2362167 bytes; SHA256 8bafb58c7b167f5b3ff67dc9e449acf12a996be30c09492a20e16c2604cdad84
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.5_v3.jsonl — 2357423 bytes; SHA256 8ff672c96384267b9df4b9e2142e051831a4825592b6a7c53c47bd84d1e5844b
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.75_v3.jsonl — 2362311 bytes; SHA256 55efe5977a00126358e60665f21c27dbe101ada330da8fb00608418c3525f45f
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b1.0_v3.jsonl — 1629644 bytes; SHA256 3580653c34a15710821de14c4af0e30fcf49848a61a7d3b39fe1d3aeade36bd6
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_blegacy_beta0_v3.jsonl — 1375130 bytes; SHA256 8208bba1f19929ba37794fa6042a767aa3fd55fb34d68a38d5586b5b678efac7
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.05_v3.jsonl — 2361512 bytes; SHA256 0dcf3555958e31df94cd1ba72721bf21f0e086211a196965c8e24f0efefaf0fd
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.0_v3.jsonl — 2161651 bytes; SHA256 7e2b5684289d225cba31743ea58af3158a53adf0faf69c44604f5abe0a7418fb
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.15_v3.jsonl — 2361585 bytes; SHA256 ff0b4d6e6d0147d6b1c4a67b3a4891f22c26d5bbd61724f990d0fd855c9bac2b
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.1_v3.jsonl — 2356813 bytes; SHA256 7aa44a0058b791fd98e4dc9953e7f251ef1f7c35b226d6766cd15d4a800d0376
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.25_v3.jsonl — 2361885 bytes; SHA256 b279a7b7be2f62e855ed902126bc3ece9cfa4380ac39a7b0ec279e9aeebb4157
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.35_v3.jsonl — 2362223 bytes; SHA256 b67a7b2c2203b7bfbc8352834beb6f643a8cdeeb10e567efdb5daf39cff5a154
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.5_v3.jsonl — 2357306 bytes; SHA256 ede8b8cc66da47bf1d34719e7d5a0c22f43bd760e72b44a4e28eab18e9d7daf4
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.75_v3.jsonl — 2362206 bytes; SHA256 cdf03208e723f55631fee14392c0813dc32ca17299e40565e5f1bc69f42315fd
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b1.0_v3.jsonl — 1629416 bytes; SHA256 c62a05e852cc478612ca92b8f5eab0d99c2058d79177bcad5a08ba577029d32a
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_blegacy_beta0_v3.jsonl — 1366607 bytes; SHA256 ff50d730f4945d08936d0d84b20cff5c17a59ca969de69035d4c02ea90d8c2f1
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.05_v3.jsonl — 2361359 bytes; SHA256 d8143aa08077c102e328255a0cfc23cc0022c3f54dd24a3687ab4691ae94a238
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.0_v3.jsonl — 2161303 bytes; SHA256 e2043b751a562d97ce131d63bff3fcb24955ccf24af642aecccf6795649552ea
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.15_v3.jsonl — 2361179 bytes; SHA256 afa1982246e49f6b36b2c3858ecd28eba54db8417dca09eac929d39b608160d3
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.1_v3.jsonl — 2356684 bytes; SHA256 a25f9398066f0a19aaf7b2a103e1f70f2ab62f518b47aac25a84378c2aae972f
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.25_v3.jsonl — 2361698 bytes; SHA256 f2ee49ec79452512076d5b26204fb292a436def2e1ce090e2a8f1ffd7687abdf
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.35_v3.jsonl — 2362107 bytes; SHA256 7182ac45aa0d66e4d4fc7e6748044d571e5750b53e5497f0275fa7221b6f4e0c
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.5_v3.jsonl — 2357132 bytes; SHA256 c974186dcff5e1ad20d8f84fe1f3d25a8118d8516c178d98b9ae38e1e459e8fe
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.75_v3.jsonl — 2362030 bytes; SHA256 fdeb43716b01da12162f43ced4152af6be80f26a06d260a5a1bbf68933841847
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b1.0_v3.jsonl — 1629341 bytes; SHA256 692ff1c452ba798854d83d2b6b8c204ba7b0d01938cfc57606f8df8f60fdca43
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_blegacy_beta0_v3.jsonl — 1366425 bytes; SHA256 81c7a9151dc5b27a3aee60a04711862e20fdae87f202b635a9f9c7282c69726a
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.05_v3.jsonl — 2361221 bytes; SHA256 1c5daaf6159e0b3375f1246c01d8dc1238a46922b5afc00214630d096c0b9585
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.0_v3.jsonl — 2161377 bytes; SHA256 925e0c51334a0020fa1f42c892ff57a4b9d03fce7cba38b6145ca2561a03755a
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.15_v3.jsonl — 2361243 bytes; SHA256 d5e06cb0668f381b99664173d7f19faaa55769e22957347d5f6d871a15850989
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.1_v3.jsonl — 2356658 bytes; SHA256 d323c5dfa11abdad3a74d4f16b8f5ba39882b0dc9665a246000a20a508282d0a
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.25_v3.jsonl — 2361689 bytes; SHA256 53b322f4e3f0502b0cd9d47036ef6f31d51729155c2e8ae5797cbad196d5ab2e
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.35_v3.jsonl — 2362116 bytes; SHA256 a444eec1c881dfbd3d8cda1ea073381d4699fc9487a8d30863aee1f8862456ed
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.5_v3.jsonl — 2357068 bytes; SHA256 8639fe18458452057bcead36c4b1c678639848ea5d2c9edffa792f94a325a0b1
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.75_v3.jsonl — 2362052 bytes; SHA256 4f1e1c3e40309d81385c7a4a91bbe7510b8c63135b62b97121f7b424709e2f5d
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b1.0_v3.jsonl — 1629333 bytes; SHA256 2911b9f610178353146c41453b98b38aaf0d5b52740c5257b24045f3550e571d
- out/pairs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_blegacy_beta0_v3.jsonl — 1366444 bytes; SHA256 abcd96737ba331d969a062a87518b33764e5aef1b1e8c71f5a03502f8032c0b7
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.05_v3.jsonl — 2335600 bytes; SHA256 07755e14da005e02f93435162f2d12165b5e12cd493bc258addfc1438911da79
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.0_v3.jsonl — 2140985 bytes; SHA256 02db465e3e01f67f27f97928803c6c6aaac9147656e8ce1244d2e2b55d37c2e4
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.15_v3.jsonl — 2335450 bytes; SHA256 fbc90c9fb556e18044b84eac138bd4bdea9e9755c4152c7568305f24d156e69b
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.1_v3.jsonl — 2330490 bytes; SHA256 6bfad894b946c27333f2409eff537966089b07805c27aec1e659d2fc9bc57a63
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.25_v3.jsonl — 2335435 bytes; SHA256 dcfb88d662fb25041673dd03d8516e559d0b92cc624f57a26d22a1b54fe1dd8e
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.35_v3.jsonl — 2335355 bytes; SHA256 f5a6b9de942b48d6c47f1098dabadba1d3e5cccd84aa4788cd0a699a6bb1950d
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.5_v3.jsonl — 2330259 bytes; SHA256 053bb15cc6745f9f08ce9bc418cc6cb8bf70b10e3d1526c8c0b8c584d4221e5c
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.75_v3.jsonl — 2335285 bytes; SHA256 96e49996b75bc262565e8de13b166f5150c25b3a08dfef3f110fb60b7e491490
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_b1.0_v3.jsonl — 1602702 bytes; SHA256 ad97922963a175567a44b29a596d3e301269434f4120533ab2b8eb26991a3947
- out/pairs/phase18_posbatch_items_gpt2-medium_s0_historical_blegacy_beta0_v3.jsonl — 1344960 bytes; SHA256 8bf529c568e11b6be112e99f0927411f7d30db0f3e8b4c6c06c7a1d064fc6947
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.05_v3.jsonl — 2335518 bytes; SHA256 0cdd7d2fe4453b67a0bd0af739a1c0fd8053cf0c7245616b19b4cb3ea22369d8
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.0_v3.jsonl — 2140801 bytes; SHA256 f3768e1dd2c66c7247d564a356b0a85c0d5a39a76f6a8abb5a15b312aae5f6a0
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.15_v3.jsonl — 2335503 bytes; SHA256 5bd795fd6c184209cb84e8731d167f9e9d8895abd6189c93d4d6a2dc1428e757
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.1_v3.jsonl — 2330589 bytes; SHA256 0b0374923a153bcbf6c95d208ad2c519e402c8462527f2aaa2854987d742005b
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.25_v3.jsonl — 2335500 bytes; SHA256 5b7027172d3e64d6bca17e55a6ab2db4e9c5a9f590f4dbd5b32950e80da916f9
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.35_v3.jsonl — 2335365 bytes; SHA256 2c10fe924e6cfb5cc5de95033955393122a7abe05344d9a14b57e617180f762a
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.5_v3.jsonl — 2330323 bytes; SHA256 a091ef368b6e6194c8599709fd3e66d66cdd734a6d458e8dd7fdf82d61277c62
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.75_v3.jsonl — 2335216 bytes; SHA256 54882738c4de45aa9ca46fbc7a90bb1d7ac081f339a38e045b51d237a4a7646e
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_b1.0_v3.jsonl — 1602782 bytes; SHA256 d5454b80fdc66a5e7eed6531d855e9ec17b47202e4733b6f08ce6dacb0716ffa
- out/pairs/phase18_posbatch_items_gpt2-medium_s1_historical_blegacy_beta0_v3.jsonl — 1344885 bytes; SHA256 501016213574d8daa372633ac4c5e0144bd885cd44d652d303b3896b8fef37db
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.05_v3.jsonl — 2335583 bytes; SHA256 4f02b35f434c330e2b284ce9659cfe166610cdff7bd0a05555484140418e33fe
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.0_v3.jsonl — 2140889 bytes; SHA256 a077a0b0ccff479973d321bfdbcac31699ec7c2b5af28b4f301caaf52af75c70
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.15_v3.jsonl — 2335430 bytes; SHA256 e975aeb12084aad818a3941cb27aafd6ff3c74188de7eb04796f42cf81a36fed
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.1_v3.jsonl — 2330650 bytes; SHA256 86797feb14c2bcb3008a9d3c1014f94a0ccf354164d49274f4da57562b12d19c
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.25_v3.jsonl — 2335457 bytes; SHA256 31ecfc7f22969826d8872d6c773006ad05b4baaf8a2b226f13bc9b447200a51a
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.35_v3.jsonl — 2335324 bytes; SHA256 905033d0a849a041dd2c06f1469f79887cb158ff6a6c3851bc26812f8c92c345
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.5_v3.jsonl — 2330238 bytes; SHA256 23ffb27b992d4d80b2f8355483756d062ca5ee6997c5e2bcbad937cc61074cb9
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.75_v3.jsonl — 2335267 bytes; SHA256 5a8b8a1b99cec2b6129e256ca6dff7b1fc9de9507698fab6c1dae479d5405a70
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_b1.0_v3.jsonl — 1602795 bytes; SHA256 bb5aec7bca4517970ae39353818dd9692c1d70425c13722ef90c7edbcefd7d6b
- out/pairs/phase18_posbatch_items_gpt2-medium_s2_historical_blegacy_beta0_v3.jsonl — 1344902 bytes; SHA256 4e0aa59eb9e78e92909011014ee30217e067fe49aeb7cd26c51920ec946bc577
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b0.05_v3.jsonl — 2318449 bytes; SHA256 fff83b60560de4b2d3cb9aa2403ba467383e14582f70947e03208137feb59870
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b0.0_v3.jsonl — 2118743 bytes; SHA256 9e387dd1bd72d273c970d2910c14c558badd71c5f95582c2cd4e3360ff38adae
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b0.15_v3.jsonl — 2319196 bytes; SHA256 dc82d62a2eb71bce4a4595d4f67db50fd2617e8f68b57cdf332b0cc3e71c1ae5
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b0.1_v3.jsonl — 2313617 bytes; SHA256 18234e55b7b8ddff818a6ae88b8fb497da6d702450350411cf7f02eb3d7323e9
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b0.25_v3.jsonl — 2318842 bytes; SHA256 ab78596aa85807aaad476225c2afa3dd56299e433c613693a761185eedaf5bf3
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b0.35_v3.jsonl — 2318933 bytes; SHA256 9b2f6e0bfd14e84c07cb6f779bb7ad3502383e55030bb5c7bec1681a2a47928b
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b0.5_v3.jsonl — 2313882 bytes; SHA256 a1c263f8c4df8850bca81262932e1cba5bcb339acc4ecbeca81662569d55dafb
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b0.75_v3.jsonl — 2318915 bytes; SHA256 79d74d6dc8c6ec8064e32e6a8e7ac928138db64149462b7e812948de200b0470
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_b1.0_v3.jsonl — 1587684 bytes; SHA256 d5f979644a0d78e0a226e70ba0440318e1e34a6a73c337edefab37394f05bceb
- out/pairs/phase18_posbatch_items_gpt2_s0_historical_blegacy_beta0_v3.jsonl — 1323249 bytes; SHA256 00621c89148e2f28e267468f1a1d10bc9a80124408823f16818e19e1074ab05d
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b0.05_v3.jsonl — 2318495 bytes; SHA256 8d867297f9c0397547740ea26e7ba6346cb568d84cabb3e5b6b75ce7d794d2cc
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b0.0_v3.jsonl — 2118733 bytes; SHA256 f86bb57ed7a70d5f7d4894a901a0413082365ba13454b294a891cd1b4aacf666
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b0.15_v3.jsonl — 2319233 bytes; SHA256 e6f305b3db0ecec43150367779d1fc3b453c1de9fe3edda0ea4dbb4f0e09cdf1
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b0.1_v3.jsonl — 2313811 bytes; SHA256 5b77409900a1b7e123e0fa2df6973a201664acb80b5fc603cdbbaf11422c7598
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b0.25_v3.jsonl — 2318911 bytes; SHA256 64b93bfcf376a5803fccc79007c81d983b4a56609f6192fed9287a81d18d8b41
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b0.35_v3.jsonl — 2318947 bytes; SHA256 68c058502eec2a084a4ca399674e0f0965ab05b7b5c3ac5af6c6867cb46c5f42
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b0.5_v3.jsonl — 2313887 bytes; SHA256 8f7eb55aba2eb6d867ffcf36cd4c46e418ef4f5bd9e064cd22f248eb140ebf54
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b0.75_v3.jsonl — 2318981 bytes; SHA256 d1172647ff4fd6a1a1f416fdcda647b2f9371f95afe402c3a7562866e875accb
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_b1.0_v3.jsonl — 1587789 bytes; SHA256 2453179a01a449900c0914340f8c94018be7439bc9f3da63518a060c547afb97
- out/pairs/phase18_posbatch_items_gpt2_s1_historical_blegacy_beta0_v3.jsonl — 1323259 bytes; SHA256 70c569b84ab040fffc7cdaef4ed546edf02db955486c422dff423244179d1f56
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b0.05_v3.jsonl — 2318491 bytes; SHA256 af09656d88744213c2c7034a3430735fa31fd0aea657fd39a780b0ccabacc77e
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b0.0_v3.jsonl — 2118893 bytes; SHA256 37a98b77b3439bc92af902a3b1c75c08051b929a8b6d9749e6849485b4303ff3
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b0.15_v3.jsonl — 2319245 bytes; SHA256 d8fcf9ac16272041513f0370c087708e7d0c4ffd4ba6fbb8a52df0a15cd5c121
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b0.1_v3.jsonl — 2313700 bytes; SHA256 bf3f2341635571a8d7cb023e2d1e9e73a93c2368a9c1cd24aeb9f0f45e27da8e
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b0.25_v3.jsonl — 2318829 bytes; SHA256 af3e98201bb0f450ae1856313adcbbab1554af1d03dc7b885c5778443f2e84b9
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b0.35_v3.jsonl — 2318931 bytes; SHA256 e3afb0e28dea7b6c37b82ca13a31bb854fa7fe3ffd329627fc1eabdbf8f1af2d
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b0.5_v3.jsonl — 2313872 bytes; SHA256 5dd703add87b01d8496b9960fc7e169881386dca80a362082cbca49d87a10c8b
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b0.75_v3.jsonl — 2318894 bytes; SHA256 8e8ee5236096a2a0b2be5bab9e40b18075308fa1cf72f550e550860fde4181ae
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_b1.0_v3.jsonl — 1587549 bytes; SHA256 0c087e15b0e00c848f16a628ecd0cf526c2159e9eed427112a6ff90a801c124f
- out/pairs/phase18_posbatch_items_gpt2_s2_historical_blegacy_beta0_v3.jsonl — 1323235 bytes; SHA256 bb3c222f997f2db395a4c819257a7d35f26e8ec2e25528ae418f1534e9bea1a9
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.05_v3.jsonl — 2349081 bytes; SHA256 b0abc8242f0dffbdf3c448fc7efe756eb40e1131d47f06a6d61187f9afc95875
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.0_v3.jsonl — 2150113 bytes; SHA256 175ed019304979c88769567bf2fbf0606bc382338407518b54649d7ca70c61ca
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.15_v3.jsonl — 2349598 bytes; SHA256 5ba61afa3afdd930592b1f843e7f77e2358dd051041e4526b50a8c12af9784be
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.1_v3.jsonl — 2344301 bytes; SHA256 bebea836e6437f289075ca1b953a1f7d21a691cae9895a073cd3851eb2821a54
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.25_v3.jsonl — 2349415 bytes; SHA256 296ea1afe2bce1837f7e2c107ae3fd9ebb9bd9290c8918f67bd3916135adf29b
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.35_v3.jsonl — 2349584 bytes; SHA256 0a5556c894fb3f6fdd52fa9264ebed800900aee979ee1ccaab5d9986b1c989d1
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.5_v3.jsonl — 2344684 bytes; SHA256 6af38bdf0c7c9f50d948dfab6221664f3e2f3d8749db52a90474b283ef189ad6
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.75_v3.jsonl — 2349564 bytes; SHA256 0efd45c41ff38035edae42f34b7f8629dfedf1e55446d758fc851efe17fc4798
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b1.0_v3.jsonl — 1617580 bytes; SHA256 f14aad87946d454c450fa4d927fd775523a32fe94b07b3a9e2ba6487b010cf29
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_blegacy_beta0_v3.jsonl — 1353971 bytes; SHA256 15ddac81a860990c58b66b8fceb098a8a53de4d73a51cbb1c3a51809f9bb1da6
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.05_v3.jsonl — 2348927 bytes; SHA256 ee81e4ae17ad3f6a3d53d38730b80f96a78c4a874e044055743ea1b8c306648d
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.0_v3.jsonl — 2144509 bytes; SHA256 9ab82090193b5fd3521767f3b8b669354419f447c5fab4d5ad334e1f8ecd9cbf
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.15_v3.jsonl — 2347731 bytes; SHA256 c40067b58c2003e1f8b54a747276cc0811df26b4b87747b9804859ac9dfed31b
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.1_v3.jsonl — 2342326 bytes; SHA256 0a60960592420603b625d9f97f434ebc9f005164634b30946ec80dfd0baf93eb
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.25_v3.jsonl — 2351064 bytes; SHA256 66dc3eceb4dfab0f7e920986a7fc59bdedd23418886b34bf497214b82e47bcb5
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.35_v3.jsonl — 2342110 bytes; SHA256 a4ecb4b5949578257b8400f909bb4c13e374bb415de1f7a64fefd58d21516021
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.5_v3.jsonl — 2335133 bytes; SHA256 0165ff4632f59200af572f564244be8815c3c37f50203433f17176c7322a183e
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.75_v3.jsonl — 2350750 bytes; SHA256 3e576902bc200ed5351f065f31d18972230f73fe96c511c7c3d3f7ecd2166f61
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b1.0_v3.jsonl — 1621499 bytes; SHA256 59228754beef5cd7c54fe8c26144bc6f17e9490ca835a40d493e778c6af96854
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_blegacy_beta0_v3.jsonl — 1363575 bytes; SHA256 5d4d9f214993fce8dda5e7ce0f64a9979a072aed155877393ede6bb235598f28
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.05_v3.jsonl — 2348856 bytes; SHA256 b86bc651954b24cc56c9adbb9129115911fa3b166a9f2582683464490fa7fefa
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.0_v3.jsonl — 2150168 bytes; SHA256 38e2c93c4a43544a64edcd05dafb8a1187b60db942b103d74e3b006740867b08
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.15_v3.jsonl — 2349529 bytes; SHA256 2c16ec43561c57b8528f330c6c0be8e49c8a5d088ebfdf572b823c716e535d6a
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.1_v3.jsonl — 2344254 bytes; SHA256 6b3ff72861dc79d967ff0935de6bc368b1d1cc06c59afe02c94c00c162572755
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.25_v3.jsonl — 2349407 bytes; SHA256 b94a9369cb0006de82a975d7b323d9402cf622deab04497291d293d0b819b5e0
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.35_v3.jsonl — 2349419 bytes; SHA256 5017095c99547bd33b2da4d229a78f6c4d22a0501cda2b80d2c5dc86c6ab8aa3
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.5_v3.jsonl — 2344609 bytes; SHA256 11f48b1176be31921c04bf7b88340c028c2f02c41d59e9c2654291ad6e7c848f
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.75_v3.jsonl — 2349546 bytes; SHA256 810d0d73a2a0312df068fdfb4b7e62552f679573fb530899d17151f6e3de737a
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b1.0_v3.jsonl — 1617468 bytes; SHA256 2fc4aeabcf21307907ce6a6488c949eff2c3b9870b018f3d0eebea0136f075a6
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_blegacy_beta0_v3.jsonl — 1353886 bytes; SHA256 9ed00a8a5c5b8032f60de14a918b68a3c05998b3892a5edc520c33c91a25b598
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.05_v3.jsonl — 2348683 bytes; SHA256 578a2cbcfc9c57efcd2022d6880bf85a977b43a36150b2deb75a56e960fc49b4
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.0_v3.jsonl — 2143160 bytes; SHA256 13c7518ceb873abfee420f74ececfd211186370a1e3eb58325180f67b975db86
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.15_v3.jsonl — 2348010 bytes; SHA256 5ccc99c747921f3db26c8ac1ed79e400bd478b63d2555b61bf332099c72f22d2
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.1_v3.jsonl — 2343380 bytes; SHA256 cf29e59570b58329570b3e4f49910ccbbb10d086fb9b363a878e23a534cabc8e
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.25_v3.jsonl — 2350114 bytes; SHA256 7132c0ce404e8eaa39d26d8c0195e9b38711257df69618c7804517498d322a79
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.35_v3.jsonl — 2341978 bytes; SHA256 5b235d96e55a4c4940b0839816cd23a8310a9b11d352d20fbb63c374ead2166c
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.5_v3.jsonl — 2334765 bytes; SHA256 91b50ec8c77078a976833824ed1a31729537b49e2e0e74ab294e36e4999dedae
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.75_v3.jsonl — 2350838 bytes; SHA256 ffd7143ee0c847cbea4795efd49f714bc11f62be9899bcbd306897fd555f8c67
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b1.0_v3.jsonl — 1621693 bytes; SHA256 7b8bab1bf4ae7420ab8cd24005475cc1f19b3dc6c6b0df226088030e983485b3
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_blegacy_beta0_v3.jsonl — 1363462 bytes; SHA256 e9bd9b8ffb140fc0ed6ed00d03da1cda1289b32d39de09496871fd7226766d4b
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.05_v3.jsonl — 2349016 bytes; SHA256 c98a2e29748ab45bdc1b3dbc9137dbe804152be846144d42c58d52999a78c8e8
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.0_v3.jsonl — 2150106 bytes; SHA256 7f9af58aabe9b06057547f25316b849a8daee8cfef3bd546fe1941dda8d85295
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.15_v3.jsonl — 2349550 bytes; SHA256 51068703cf95bbc50f07ef8dc3d717d7fc5660ea14f124520b8803bd7734de03
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.1_v3.jsonl — 2344119 bytes; SHA256 cb87a89e75a959f3c5eebbe7b2bd0bb5f6f8c2471f0c7601fb895f731cbfbe04
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.25_v3.jsonl — 2349403 bytes; SHA256 01f23a8d48287ab08ca243f71a9b8daf2079d32c7a37e9b0c846d94634ffb5a5
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.35_v3.jsonl — 2349428 bytes; SHA256 854ef2f41a418f428f1c14cfff517fde4d4cb95e8929bf3d3fb38e930639488f
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.5_v3.jsonl — 2344501 bytes; SHA256 8c83dcceb505ed9f721c81ee526c68273f7db3d5c77715da675045bbbc51b57e
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.75_v3.jsonl — 2349560 bytes; SHA256 f9d3c5d45c685ec48145f70a4170c80b21448711fcd6d6ebf8908628d0073d60
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b1.0_v3.jsonl — 1617404 bytes; SHA256 00e6956f1934517a71d146642980205ceed8fb6f8829a5db2dd5b5587aae51cf
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_blegacy_beta0_v3.jsonl — 1353904 bytes; SHA256 025bb8d11c12ceb22bc2a789c89b81a8d2f0378491ef245b3520ba7236accd54
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.05_v3.jsonl — 2349467 bytes; SHA256 0d80db509aabb852dee58043a149e1ccab7d0f0c3275e2abeb9e95d26c1cc089
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.0_v3.jsonl — 2143240 bytes; SHA256 256e90965c0c821cd7a9cd6c3ea7b95902f1ce0ec5baee9c39fc2920c1202da5
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.15_v3.jsonl — 2348709 bytes; SHA256 0529a4ddaa663c404b332bfc46e6f7cb93cb7a85ae8984f6460883a576abedd2
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.1_v3.jsonl — 2343599 bytes; SHA256 a33de5e0156e8d7fd6d16fc906dcaba0e367b86840db9726a1d79b0802d4cdcd
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.25_v3.jsonl — 2350160 bytes; SHA256 6e97716a6644295f00357a45c3b2bc71f9225cd8c5a681d7eee30b6c1b095449
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.35_v3.jsonl — 2341251 bytes; SHA256 f1c914e0f8a5fafe0137869bea9309e477c629f5e56e08f3bab7e52b7118f690
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.5_v3.jsonl — 2335706 bytes; SHA256 3bfa4da3320fd1da96d753902cba803d7d4409eb76eede48b476cabab4a1c0ed
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.75_v3.jsonl — 2350631 bytes; SHA256 4589822d039a4dae9355a9168294f7b8aa1a1c20640d6df949ab52f6a257f34c
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b1.0_v3.jsonl — 1621613 bytes; SHA256 8a886e0b0926b4fecb5525a77a37dfd1b98b9262c90f75d2c74240c2d400ff0d
- out/pairs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_blegacy_beta0_v3.jsonl — 1363494 bytes; SHA256 9bd964593032445f9f4d4d84d583c1ec4dafd1e6f852f0e2ca8ac1dd67d8c917
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d000_016_v3.jsonl — 298726 bytes; SHA256 894e92a996f3afd7cafcfa2d27806c1f38e9f58a9634b174f24218ef23bdd342
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d016_032_v3.jsonl — 298932 bytes; SHA256 10aa23eb0f02463aac502812f4822faae23cd96e475ff36646077960c01929a0
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d032_048_v3.jsonl — 298892 bytes; SHA256 8996d08f21b666fcec3bfe8e38589213798b942651e69f5b23b4a18e02163bdd
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d048_064_v3.jsonl — 298803 bytes; SHA256 cceb82607456cc397fd62dc04b6ff25b77bb393d9455a70063d74d7aa1862518
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d064_080_v3.jsonl — 298800 bytes; SHA256 b78fccfc636d044322e6beda90ea9a080cb1f8d64e333074c8852fcc2a93b6cd
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d080_096_v3.jsonl — 298790 bytes; SHA256 9d8d1a3410d4703d4797acfc6da6c6144e00bb30160881765122abdc54c541ea
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d096_112_v3.jsonl — 299220 bytes; SHA256 739e3318f534705a1dfadbadc04a545c00511fab35940f5573cb042006afa0ca
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d112_128_v3.jsonl — 299178 bytes; SHA256 a5c8672d1a87b03135ef3611a392b85a9f13f9b342b97a8924cce5b8d3709497
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d128_144_v3.jsonl — 298921 bytes; SHA256 e1e093d49eb437bd6ab45683f23f866174f3e6fbc1e0c6c73efa44f8b03512e5
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d144_160_v3.jsonl — 298813 bytes; SHA256 e20b650f677bbcae7ba31bd87e26f0861f0fa2c9425ce2f313baa649348a0cff
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d160_176_v3.jsonl — 299053 bytes; SHA256 90b83b953e92a052ac36014f34478d978dad2220ff0f55ec142401371f15cd6b
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d176_192_v3.jsonl — 298928 bytes; SHA256 5d60344eda46845ee7bdf6ede754e4830e180ae60c4926fcc9658e0d8c8c6d01
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d192_208_v3.jsonl — 299135 bytes; SHA256 c9bad125708c47a8653751859e021173dfd07386fd89f1a109920578225b814a
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d208_224_v3.jsonl — 299047 bytes; SHA256 a858f94a3b02d4831d0d6462de576ca2b46b6be980e0b067078a6432f74a564b
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d224_240_v3.jsonl — 298996 bytes; SHA256 d9cf7137a34e4dc60233c0ef8513c3cc50c7d6172d39e4456b1bb4c5651f6c1d
- out/pairs/phase7_massmatched_EleutherAI__pythia-1.4b_d240_256_v3.jsonl — 298956 bytes; SHA256 ed3debcb3cc51bfa278a56e5e29107890388530d3d8b07aa9f9d122005f53c3e
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d000_016_v3.jsonl — 299027 bytes; SHA256 3517dea6abc93522c3f0877604fe46e5515bf108f17545086b509fd2a1a5a13e
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d016_032_v3.jsonl — 298906 bytes; SHA256 776dd29242033214c65c1c9f7741b773d2b54a5d1cbae64858c1e2c52805c612
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d032_048_v3.jsonl — 298972 bytes; SHA256 f4c8b25d19865e4fc73ab6f135940d1cf7455132651f20a65b10e649da07edb1
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d048_064_v3.jsonl — 298810 bytes; SHA256 c83e007ca40c90f042ec3255250e1b562051e5805c129b96e435a9e25bfaa8f2
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d064_080_v3.jsonl — 298945 bytes; SHA256 fbde02f8ca2a5bca81e44dc7339484e97c20824018b5c3d5b9087af2efeb9f5c
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d080_096_v3.jsonl — 298744 bytes; SHA256 cb9bbf7f92aaad983de51b4a15f1d7568756d638d74c773173860608adca1675
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d096_112_v3.jsonl — 299408 bytes; SHA256 728446bcb9006ad0cfccff6bb7bca1e909ffe80699d943640c09a0345feef666
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d112_128_v3.jsonl — 299194 bytes; SHA256 4ff3b6a6f39ca38dd07b523c6f1ad71a6972f87d947053774a8a73da3cb65586
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d128_144_v3.jsonl — 299163 bytes; SHA256 5adb2428aa64e551d71240f6b168ac4938d7f982e49043629817e0af9b40867f
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d144_160_v3.jsonl — 298934 bytes; SHA256 187d1df880e1148e28410f14d1174a03421f0ed1da1fff916189be75e69a3501
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d160_176_v3.jsonl — 299052 bytes; SHA256 0882eedb4dc5b7a4313812468df1210e5a9f67cd5ce8bc55f41c529602b613fb
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d176_192_v3.jsonl — 299049 bytes; SHA256 b983430d107137497ee8d94899a734a2ef04b17ec255edb137e9509159483c6a
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d192_208_v3.jsonl — 299150 bytes; SHA256 ba923ef55baab2b198da4d48185c44d0b24262fc7661ee6f4789375e9a007176
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d208_224_v3.jsonl — 299152 bytes; SHA256 3f0f0f8762163b8d544fbeff62c532fe00dc12319698792a323bb69b0d30919e
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d224_240_v3.jsonl — 299098 bytes; SHA256 01f2068fd4a89f9dd203632810b4833307e789c68651baf7927a9df5e55229d2
- out/pairs/phase7_massmatched_EleutherAI__pythia-410m_d240_256_v3.jsonl — 299106 bytes; SHA256 f31d2b9ef6b7808e60bcf6f5cd3689c517b2a9b7be67e7a985059c5b093faf95
- out/pairs/phase7_massmatched_gpt2-medium_d000_016_v3.jsonl — 295686 bytes; SHA256 eb0ca04d68b25d338b3f190a16387f980486bfc4a6efbf2044caa3c648810b3a
- out/pairs/phase7_massmatched_gpt2-medium_d016_032_v3.jsonl — 295864 bytes; SHA256 846562a90626fa156d1b87add905fde9e3d4b65e892464d863d754c6ac68437c
- out/pairs/phase7_massmatched_gpt2-medium_d032_048_v3.jsonl — 295932 bytes; SHA256 27da4106dab7d32477145077e05c6b8018b4c8355fe932128c7676b34f82f850
- out/pairs/phase7_massmatched_gpt2-medium_d048_064_v3.jsonl — 295777 bytes; SHA256 7621ba1577bc8eefb0d991d3dbadcbd439fee02ff2033979b6b35faf1d7b4a33
- out/pairs/phase7_massmatched_gpt2-medium_d064_080_v3.jsonl — 295688 bytes; SHA256 99e03983c2309d34801a73050e209ee95a7836a83eda67871dd5bfc213f0cf53
- out/pairs/phase7_massmatched_gpt2-medium_d080_096_v3.jsonl — 295680 bytes; SHA256 be16efd2d126a5f3144da1b2c64e53bebe852199b8846d8d9f7669098801059b
- out/pairs/phase7_massmatched_gpt2-medium_d096_112_v3.jsonl — 296069 bytes; SHA256 6166d5bac6a22177752f0dc0f968ee11538513bd4cab9bf397592e3f460a8657
- out/pairs/phase7_massmatched_gpt2-medium_d112_128_v3.jsonl — 295974 bytes; SHA256 7de37700f9783619ad1138992eff7c12c9c22c7b4fde0e43a6da4a7e017c7a14
- out/pairs/phase7_massmatched_gpt2-medium_d128_144_v3.jsonl — 295944 bytes; SHA256 32fefe7cb8d65ceb1715b105edec038143254229524ca32dc5e2c38121e6e2e2
- out/pairs/phase7_massmatched_gpt2-medium_d144_160_v3.jsonl — 295977 bytes; SHA256 2bb91f99a3e5c6dbf173148e0e4e924f6220396d790e9a58b4ef560645b5ef7d
- out/pairs/phase7_massmatched_gpt2-medium_d160_176_v3.jsonl — 296004 bytes; SHA256 9b73451d631cfe72a4a8e7edc9ddeb391976e55f69704900c2ad0c582deb75af
- out/pairs/phase7_massmatched_gpt2-medium_d176_192_v3.jsonl — 296041 bytes; SHA256 f76085dde3b7718491a6d1814ded7187f9e467ca0ba4fdcb68e40aeb39a4cf82
- out/pairs/phase7_massmatched_gpt2-medium_d192_208_v3.jsonl — 296302 bytes; SHA256 c801eb8244bb8cb1426dff58ee907891b382ae80e4d7eaf942012410e3f74808
- out/pairs/phase7_massmatched_gpt2-medium_d208_224_v3.jsonl — 296166 bytes; SHA256 e33e1940f6424cce054553214eb269195d219c6fadff73abda2b4cb90ca05f4d
- out/pairs/phase7_massmatched_gpt2-medium_d224_240_v3.jsonl — 296035 bytes; SHA256 3e8ddfb7203b3c7da576d3631c6dddfb90c981a7d6d90cea205de9f66e180e3a
- out/pairs/phase7_massmatched_gpt2-medium_d240_256_v3.jsonl — 295883 bytes; SHA256 331eb3e30651ea1c3d458386b56792a5ea362b2f0eeca9f12793b207c5f6c847
- out/pairs/phase7_massmatched_gpt2_d000_016_v3.jsonl — 293700 bytes; SHA256 6dec0572508842be3406ed35b7d10e47666ca44e203a7e0cdd103a3b4b35f622
- out/pairs/phase7_massmatched_gpt2_d016_032_v3.jsonl — 293932 bytes; SHA256 c6c8528063e7b8f775822287bf69afd650f928ec75a43bc65c58d5ccddd550ae
- out/pairs/phase7_massmatched_gpt2_d032_048_v3.jsonl — 293849 bytes; SHA256 a685d07b0b96f467f8461063ec0a954da464619dc263045775251ccb708d13a6
- out/pairs/phase7_massmatched_gpt2_d048_064_v3.jsonl — 293771 bytes; SHA256 b81466d0f62d4070b8592dae1fd1c5540c1f4757ec313530e09aa690b9a38959
- out/pairs/phase7_massmatched_gpt2_d064_080_v3.jsonl — 293895 bytes; SHA256 6fee02cd567e4d3102cd535eab20ec250f3433ad8c9d0e642c31c8aca70c63fe
- out/pairs/phase7_massmatched_gpt2_d080_096_v3.jsonl — 293838 bytes; SHA256 5323273ab5be31648220a5cb380e5cba58445d7e01da18f71acce2e239b617d4
- out/pairs/phase7_massmatched_gpt2_d096_112_v3.jsonl — 294167 bytes; SHA256 786cb9b153f16d5d50d20d2dc3370c9ee49c576cc4a167abd9c76fa7319eb26b
- out/pairs/phase7_massmatched_gpt2_d112_128_v3.jsonl — 294042 bytes; SHA256 bcaf26b1a1cfa56135e9bc2b52b3c62051076c49ec21214902c566d0553dbae6
- out/pairs/phase7_massmatched_gpt2_d128_144_v3.jsonl — 294098 bytes; SHA256 8d454e4f9a524733c18520dd59afb63191c9eae861e88e8688c9547f051bf579
- out/pairs/phase7_massmatched_gpt2_d144_160_v3.jsonl — 294226 bytes; SHA256 61ea6b7ba312369e5df4329bead7649c8785745326dbe9b132c610df73e53ddb
- out/pairs/phase7_massmatched_gpt2_d160_176_v3.jsonl — 294053 bytes; SHA256 008876c700e36e32e55760cec35264aab365825de05574c72c0b57e4ace98472
- out/pairs/phase7_massmatched_gpt2_d176_192_v3.jsonl — 294276 bytes; SHA256 0bc68a0858cf04ac257648a8f04f3fab38bfe300191ba172e24681bd9d645e49
- out/pairs/phase7_massmatched_gpt2_d192_208_v3.jsonl — 294284 bytes; SHA256 0235a35939c157c520ecc70cd62a10e65dee7039161b58304f43d28f4386c6ee
- out/pairs/phase7_massmatched_gpt2_d208_224_v3.jsonl — 293986 bytes; SHA256 ea2d013fcaf7a34507265eee27046d479c66e466735c288161a6a9f5adb709e0
- out/pairs/phase7_massmatched_gpt2_d224_240_v3.jsonl — 294016 bytes; SHA256 6502ef8cbc0fbeb1660ecad4dd9e964b9dba31457b8d29926c22090cdce12fd5
- out/pairs/phase7_massmatched_gpt2_d240_256_v3.jsonl — 294050 bytes; SHA256 2a145fd9ef372a52b855adaaf39b31075eaf18be99e2fe902fb4411009b7693a
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d000_016_v3.jsonl — 296715 bytes; SHA256 b18f65f9c8b29d07e56ad4c6e6230887bdd8eb900cb6afc9d41e601897d4c9f1
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d016_032_v3.jsonl — 296593 bytes; SHA256 5c52d7a7e5835866e1a644568097c431a081263b75a732304ba43183cb5635f4
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d032_048_v3.jsonl — 296647 bytes; SHA256 c78432716e14e80648be7d01a78d30d0b44d677302a6785a60b140339a5625cc
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d048_064_v3.jsonl — 296674 bytes; SHA256 e048b5af19795fa620ff8f88e767787c71f3f7378512a953316718eae99fb224
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d064_080_v3.jsonl — 296780 bytes; SHA256 9548ca4ad36801b8a4048cf897a526dc5f02eec5e8ff4baab7fbfd36de8a2aa7
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d080_096_v3.jsonl — 296823 bytes; SHA256 15fd1d9b6108f2f24540fb07c186fb5a772f4877f48dcdba45fdee620252682e
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d096_112_v3.jsonl — 297164 bytes; SHA256 2bbf9486d178c022dc4d527483740ee246af34d5ffa09413637dc8e3d8d5e382
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d112_128_v3.jsonl — 297106 bytes; SHA256 fbc1fc917c9ae089e78880df67ab04ab9673b3ff84dc1273858bf84c9bda35b4
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d128_144_v3.jsonl — 296872 bytes; SHA256 fa4bf9ea837c6941db3d0be26da10d0a22c2bc3e3c95806fea636db228df43ca
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d144_160_v3.jsonl — 296790 bytes; SHA256 2dd8e2b0233f75c3b164d84b2685c0b2daf949f85a96a3fe0e6b54a92be3c4d1
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d160_176_v3.jsonl — 296884 bytes; SHA256 ff03ed098e3bf8e3dd8933ed809a68011f79505a4eecf4833de2b63a000af0cd
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d176_192_v3.jsonl — 296767 bytes; SHA256 91a79a75ef9c6e1fb5ac35f81d03849c07c062360ed32ba5f3e18fe52d3c95dd
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d192_208_v3.jsonl — 296881 bytes; SHA256 8f47e06ff0de8f8feb9f1d1006ee5f9e0873052f646797693894d0a93124c5ad
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d208_224_v3.jsonl — 296805 bytes; SHA256 959c1c5eb1034b76addb89f6d1c45834488be2685c422a2fcb4b82809ab73429
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d224_240_v3.jsonl — 296894 bytes; SHA256 56a586340a6b9ae08e5b45f06844841d26583eea80569e9927ea30a7539725f6
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d240_256_v3.jsonl — 297024 bytes; SHA256 82eab731f11eab4b3300090e76d9d605ec0a8fc15f9828e2430ab6fa81bde7ff
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d000_016_v3.jsonl — 296213 bytes; SHA256 85c974bc3d6b4565ceb930356e6004de734bed4c7e0ea5ca0e01c8375ab996cd
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d016_032_v3.jsonl — 296514 bytes; SHA256 02acf8b491eeb9296d6be26a57838981b07fee61c5f951d39b34d64584bc4540
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d032_048_v3.jsonl — 296707 bytes; SHA256 5c872fc7e17b6d85f4662e342afc5b8164a7e32cc14ad821ed591f0ef1d66d04
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d048_064_v3.jsonl — 296633 bytes; SHA256 ddcd8c6785625aae8e4633b89c44268d60a570da15edf0f7806468b72d9c6883
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d064_080_v3.jsonl — 296379 bytes; SHA256 20f22cb3390eb14fc413b4dd5f21c5a63e2b1a02f9da3ddf17de5153122a4963
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d080_096_v3.jsonl — 295861 bytes; SHA256 b2d61b814a5fa37872ab5e9b63c49eb7066f53fad638b2fccf898e20eea8af73
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d096_112_v3.jsonl — 296583 bytes; SHA256 59530ca878e6e50ed8e21599bcadde7347d85da911c3c28b4a06327c9df93e91
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d112_128_v3.jsonl — 296680 bytes; SHA256 f12f34a59fbe4903ac5b2d46fe38903b284c66c759acd6dc2ed78d6f5e8a53c2
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d128_144_v3.jsonl — 296754 bytes; SHA256 c10e3ee57178a234c484d3d6a8ae4cf2742581367bc9b9d9941a8dd9959ae36c
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d144_160_v3.jsonl — 296747 bytes; SHA256 d2c08c48a383a82e420ff346f399064acb5cd3268fa7aa5932d8d43ebd5edc40
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d160_176_v3.jsonl — 296281 bytes; SHA256 af84d94ac3f0dbeb6577797816da49d8d4bc6f61fd575ee4d7ee04167c51c9c5
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d176_192_v3.jsonl — 296549 bytes; SHA256 9750a3e5112ab47e79ba67cbf5c1955a70112ca33984c13eb55544939b35d1a0
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d192_208_v3.jsonl — 296571 bytes; SHA256 2ba937877bacfede343d7be2c724c2e7ff44fcb853fcaa57fb103415a9887564
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d208_224_v3.jsonl — 296125 bytes; SHA256 873dea3506dada2bc5aef43b17f58ae1ae6aa5014b94261a5cff66c8abd74685
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d224_240_v3.jsonl — 296629 bytes; SHA256 a31b1fc45a2e044585d5d90fdec516b515c66c693af56c43316c7dbf9a3fae17
- out/pairs/phase7_massmatched_Qwen__Qwen2.5-3B_d240_256_v3.jsonl — 296498 bytes; SHA256 be2cb47ef760d043b41fdc58793b618daed046883f752d9d7d5ff6a8828616c9
- out/pairs/phase8_items_EleutherAI__pythia-1.4b_s0_historical_v3.jsonl — 4799819 bytes; SHA256 8a80f8fa876cca831da6845eae13a2f9a5819426d91a79de15f6e93f23cc89db
- out/pairs/phase8_items_EleutherAI__pythia-1.4b_s1_historical_v3.jsonl — 4799736 bytes; SHA256 a28d1cdc75e1ee2a18678febed1683acf96080d6c29c414a008dd15aa95db9d5
- out/pairs/phase8_items_EleutherAI__pythia-1.4b_s2_historical_v3.jsonl — 4799904 bytes; SHA256 ccd7ec638988311d1bdc9f28007536d5c23e5c06b3c64d13d030628f853a20ce
- out/pairs/phase8_items_EleutherAI__pythia-410m_s0_historical_v3.jsonl — 4799939 bytes; SHA256 f9b341f1321be09700dd703f05d6dd89a46524542be3b841ff9af5c937b8adc0
- out/pairs/phase8_items_EleutherAI__pythia-410m_s1_historical_v3.jsonl — 4799594 bytes; SHA256 4ce9d466fc2b496a90e7b655208d6604600f4af8f2d5230d7d1cbfd6d826b4a9
- out/pairs/phase8_items_EleutherAI__pythia-410m_s2_historical_v3.jsonl — 4799511 bytes; SHA256 6a347d37e101bab108a8c37eb1ed15d2d50449a2142d3190e3287c057efcd496
- out/pairs/phase8_items_gpt2-medium_s0_historical_v3.jsonl — 4728679 bytes; SHA256 8edb8164a8e680d811d1d4f4c39c33671527ba97001d669606f774ad39e11769
- out/pairs/phase8_items_gpt2-medium_s1_historical_v3.jsonl — 4728944 bytes; SHA256 fcd2e83016fe3528f767d956318af9e1c67acdb25fb646f853df9cc610f34fd5
- out/pairs/phase8_items_gpt2-medium_s2_historical_v3.jsonl — 4728793 bytes; SHA256 0914fb3f4799b6d670d3c3affc177610f43c5e047be9ed095ff32dda4e65b312
- out/pairs/phase8_items_gpt2_s0_historical_v3.jsonl — 4686104 bytes; SHA256 782632809b3b240533c8c8c9b7ec763757152c957c3cf7fd28351dff0e30df72
- out/pairs/phase8_items_gpt2_s1_historical_v3.jsonl — 4685563 bytes; SHA256 3c9eebe8c54be7d88a3247b1a8d60b0e02e077a5d477493a755ee645b01b9374
- out/pairs/phase8_items_gpt2_s2_historical_v3.jsonl — 4685503 bytes; SHA256 f9141282b764fe12a6a4e79158dde0d8de41aa14a51fddb57ece015089db77ca
- out/pairs/phase8_items_Qwen__Qwen2.5-0.5B_s0_historical_v3.jsonl — 4768359 bytes; SHA256 263fd5054d33979e40467b5ccfed49c52b548fe7fcc320d763ca9602105a4ffb
- out/pairs/phase8_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_v3.jsonl — 4773681 bytes; SHA256 ccc00c6b2471b70abe703667987ee609de97c38d2f95201ccbf0ed49600657b5
- out/pairs/phase8_items_Qwen__Qwen2.5-0.5B_s1_historical_v3.jsonl — 4768476 bytes; SHA256 f1a4a4653c68705b58a0001a233cd69dea50d7860b3569152deb5a5b81084b17
- out/pairs/phase8_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_v3.jsonl — 4772548 bytes; SHA256 dc1945a7b79915f19bbc415042a5fb6e1cda9f3db60531a853fdad570e64de51
- out/pairs/phase8_items_Qwen__Qwen2.5-0.5B_s2_historical_v3.jsonl — 4768771 bytes; SHA256 9f415a3dadc5b97bfd8b95ba1b8340bb35c53a5d36ede2f9feb0a726e314371c
- out/pairs/phase8_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_v3.jsonl — 4773852 bytes; SHA256 90ecf22c2315fca292a0e4cbdb7507fc7d2e270f623cf8373da3656e5f9f0cff
- out/phase11_items_gpt2-medium_s0_historical_v3.json — 1366 bytes; SHA256 834580563628abe976e29146e96bb0700ed54acd1fed5aca4f92c8f46f6c741d
- out/phase11_items_gpt2-medium_s1_historical_v3.json — 1366 bytes; SHA256 371b38cefad2eb86bdd34f48053b01ecbaa53a10a9d05a6942c9182b4089e95e
- out/phase11_items_gpt2-medium_s2_historical_v3.json — 1365 bytes; SHA256 b10d95689215b200183729000959498b238dd8db45539a7d3916e75bfc973546
- out/phase11_items_Qwen__Qwen2.5-3B_s0_historical_v3.json — 1381 bytes; SHA256 e5c716b0fabc29b7557adb27c5cc10cf1396666514979b4f4709afeaca80da55
- out/phase11_items_Qwen__Qwen2.5-3B_s1_historical_v3.json — 1380 bytes; SHA256 9d4de1a6f9594665c4ee65f4d60921092d325b422d156e97fe8e5125d6a253d0
- out/phase11_items_Qwen__Qwen2.5-3B_s2_historical_v3.json — 1381 bytes; SHA256 fc2387ed9465f638749765d66ca4e12d5b6c9d44518ce0ad590fb55f6e38d3c0
- out/phase11_items_v3.json — 361882 bytes; SHA256 4a29db68b3b787fb0fa4830f0fe2faa02316f40ebf6445db961f22beabb0de66
- out/phase15_constancy_EleutherAI__pythia-1.4b_n128_v3.json — 27612 bytes; SHA256 1e02594ea2ffa4587155b9715dadc4773f3866cfdbb1fe5e0e8a2c1e405e7018
- out/phase15_constancy_EleutherAI__pythia-1.4b_n256_v3.json — 27668 bytes; SHA256 4bc9a98ac027eaedfab0c1aa7f8d3401b8e696f44d739d3d6a0a2e8d93da2e38
- out/phase15_constancy_EleutherAI__pythia-410m_n128_v3.json — 27631 bytes; SHA256 e1702d0f28fc1da7b1ea14dd848f065366e91caea0b8e66da1ebf20b01970cf2
- out/phase15_constancy_EleutherAI__pythia-410m_n256_v3.json — 27709 bytes; SHA256 de165ed6cd5870bf2ae7146528c3ef54e471f3172781eead4eac21d366f3d58f
- out/phase15_constancy_gpt2-medium_n128_v3.json — 27507 bytes; SHA256 1c1f788a884dc0ef2c426a179528c1059a435bdbd5b7c92ac573ff28d7f98f08
- out/phase15_constancy_gpt2-medium_n256_v3.json — 27546 bytes; SHA256 615894818e13eebc004d956de937048505dd368c062cbf4c39cfe072cc09d58a
- out/phase15_constancy_gpt2_n128_v3.json — 27511 bytes; SHA256 4c4a5e0abaf0071a1937f8349ca3927e7b575121366e65dd7919c0fb8ae52b2a
- out/phase15_constancy_gpt2_n256_v3.json — 27514 bytes; SHA256 4a782d3453ac8e3256b603f10884bc1909bf4f14439be347cd0e71cc3be7141a
- out/phase15_constancy_Qwen__Qwen2.5-0.5B_n128_v3.json — 27674 bytes; SHA256 86bdab8e848a52e458528c9bf20250069c5e8e3259a90a10030438350a1f257d
- out/phase15_constancy_Qwen__Qwen2.5-0.5B_n256_v3.json — 27763 bytes; SHA256 2b94f9e3babc5cdd6d697ac2c2e129a751bf49e0ab5b8b81300fd661b6a93005
- out/phase15_constancy_Qwen__Qwen2.5-3B_n128_v3.json — 27900 bytes; SHA256 9744c6de5ccd318c285f2f820fb415deb3622d3bcd6c9c07d26518a03916152f
- out/phase15_constancy_Qwen__Qwen2.5-3B_n256_v3.json — 27978 bytes; SHA256 5f7e3df609e92eb15f1f2b92d17f2a5232f4acbd9e4a932633c21d923f7e8eb3
- out/phase15_constancy_Qwen__Qwen2.5-7B_n128_v3.json — 27537 bytes; SHA256 af8762b0916d6d2d9f8d3e594e51256a62135eb11ed2525d92aa366e9d3db3cc
- out/phase15_constancy_Qwen__Qwen2.5-7B_n256_v3.json — 27585 bytes; SHA256 ef7fef4e9ef1c3c39ffe874c56063c0cf82b144ee0e352055bbee12185099b11
- out/phase15_constancy_v3.json — 458637 bytes; SHA256 73c443a6f39bb7130b73976a1f786d81fda3d4ab66e5de17bd00b296b80ee125
- out/phase18_batch_diagnostic_v3.json — 515537 bytes; SHA256 5cefac675d798360cf9f8ecf2615ec0939a99849349ccaf20c3e0e99e9c06219
- out/phase18_betacv_v3.json — 513355 bytes; SHA256 d93a80bc59e326aee6e397bb8f0b030361e4de190b65fe93b550d51c6528828d
- out/phase18_count_mismatch_gpt2_s0_b1.0_v3.json — 141 bytes; SHA256 36fa1fdb5f8fd885f790dddd251a059a615fcae940de137141f727a927bcbcc4
- out/phase18_historical_mismatch_EleutherAI__pythia-410m_s0_v3.json — 2104 bytes; SHA256 7a15f56edca4ea724ea223f8f4527c3f7a0b3a4405fb23ef0ff048d59cac9dc5
- out/phase18_historical_mismatch_EleutherAI__pythia-410m_s1_v3.json — 2104 bytes; SHA256 1c25d3f5676d7f5f0fd2651b633a853123926f70512eafc46a535af45c382087
- out/phase18_historical_mismatch_EleutherAI__pythia-410m_s2_v3.json — 2104 bytes; SHA256 668297bc8aebebf04188ded2abfc4cdd6d3e8750ad76006524735c2de1c8a2cf
- out/phase18_historical_mismatch_gpt2-medium_s0_v3.json — 1988 bytes; SHA256 cc1ee9c2c5d6c1359314067a273c52ec8f90ba4b96143b30a16ad987ccc890b8
- out/phase18_historical_mismatch_gpt2-medium_s1_v3.json — 1985 bytes; SHA256 dcae9b934239a0ef3dafa50bff314776f01f5e87e31c31861b7ed1e02af02b4f
- out/phase18_historical_mismatch_gpt2-medium_s2_v3.json — 1986 bytes; SHA256 f166bd645190157412d852455fe8027227cf8224de82a8ee147116d74ff56b25
- out/phase18_historical_mismatch_gpt2_s0_v3.json — 1913 bytes; SHA256 cc6bcf34bc990ed2c52a923a343da3c04c4c0edcc2d73bd7fcb1e9f5dde36106
- out/phase18_historical_mismatch_gpt2_s1_v3.json — 1913 bytes; SHA256 44f406e8d61f88195d412344e4a6b3adba96210af1e449d1c1ef6e780d7947b6
- out/phase18_historical_mismatch_gpt2_s2_v3.json — 1913 bytes; SHA256 4165b254ff99652ed9e8801b0f04d446a07af8f19df5a06b0ca9563b554feeee
- out/phase18_historical_mismatch_Qwen__Qwen2.5-0.5B_s0_v3.json — 2054 bytes; SHA256 cb673f12a244ab76d06ead91e2cfce48a064bea5994b53a46752683d3ade2a58
- out/phase18_historical_mismatch_Qwen__Qwen2.5-0.5B_s1_v3.json — 2054 bytes; SHA256 dd715f48f5acaba350fa7b7791b30fbe6d567eb1cf784be223e69c0dd29fb5f4
- out/phase18_historical_mismatch_Qwen__Qwen2.5-0.5B_s2_v3.json — 2055 bytes; SHA256 f22590d35daa6dd45881e0d92f57d768bbc89749059abfa3298862bcb46ee0f5
- out/phase18_items_gpt2_s0_historical_b1.0_v3.json — 1279 bytes; SHA256 bbcc925bb7eb516bb0dbe51442f1a06ce800ea770432723a64d814a88b8527a5
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.05_v3.json — 1747 bytes; SHA256 3077705e278db16cf8253aa864995229853574d93c5a43bab0531807afc897c4
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.0_v3.json — 1746 bytes; SHA256 52e379caeb9f70ee3a7e78a99a8465a510039390fb665081ffeb445a2f2e64c8
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.15_v3.json — 1746 bytes; SHA256 7af8ebbf2000ef46230ace10c5b7f7e7231278f0e70893b289ab5a66d56f8b30
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.1_v3.json — 1745 bytes; SHA256 0058d22ad02d5b4e5c4da3ccaa3ac0fd73766ea4e1e4bd56c15f1cd34338225d
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.25_v3.json — 1747 bytes; SHA256 2b5fe16f92724fc266385210ccc99b143fe3e456aaf162675639dbbcc652a1ff
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.35_v3.json — 1746 bytes; SHA256 f285596e4d4ef19cb35226f1fdb64a215d512f781c64ce4261d5ef6d1d484f31
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.5_v3.json — 1745 bytes; SHA256 96c383589aaffc6413d242d4ad365c48f8172a9cabe03fe23d27f05ab1b3e876
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.75_v3.json — 1747 bytes; SHA256 c31fee2fe76c230dbcac6b8b5399d0723d7e6f04bc43323c3760eba25d988e57
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b1.0_v3.json — 1745 bytes; SHA256 f9ac7138a521ae2bd548dc971eee91e11d95e7fd4c484f463be0cab0b3b95a23
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_blegacy_beta0_v3.json — 1764 bytes; SHA256 98a652a14a7a23daaa7599b470b8ff8b360bedf3b03afff9783b46329ee5513f
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.05_v3.json — 1745 bytes; SHA256 694f460facc174fc7d8dc4e1716fe5bf48842cc0379e5e959cc2b1452fef98d6
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.0_v3.json — 1746 bytes; SHA256 839b1bb3d1a0aa3a6747123e645e35903287c73b56caf52e224854bc20766d4e
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.15_v3.json — 1745 bytes; SHA256 affaabc0cdedba23938159922256d1e68626a5fb91d055bc54c4f43e3eee4d34
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.1_v3.json — 1745 bytes; SHA256 35fec6be5899ac6152f180fda785806dec6ea39896e6ca8afba363ddcea16e3c
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.25_v3.json — 1747 bytes; SHA256 1180b726386cf46f325c94ee62a9edde5350858f14164b4ed645481935286eca
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.35_v3.json — 1747 bytes; SHA256 7b2cdc65bddae4b7dfcf9961d1abb276b5250ca71e62d4db41104f4252ed79ed
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.5_v3.json — 1745 bytes; SHA256 f4ec69eda89ddde9d38fa0afb61b96dfa67c1bd26181522896c6b3a4b07b2a6d
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.75_v3.json — 1747 bytes; SHA256 e53975d6a1a060b9a5247b22f31c011a9b226ecb67050b70c5226b4facde45c6
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b1.0_v3.json — 1743 bytes; SHA256 0fbdc1bc87101e971284df7d9e65173a572e4b4c226501c7b2835edbc5ae2a2d
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_blegacy_beta0_v3.json — 1764 bytes; SHA256 eece444be78212a7a3060564447dda9fff8c0c17fc27389c49871d3d6801eae9
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.05_v3.json — 1747 bytes; SHA256 f326d755ec1ce46a9701f164a93469fe14486e45ab5394d43677fecaed334b85
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.0_v3.json — 1745 bytes; SHA256 9c8e3404b7dfdf6850370184c78df1f46f2a4bb741ccf1185c5d654020ba97a0
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.15_v3.json — 1747 bytes; SHA256 cce39bb2eed7b541b35633e3983413688a85dae38fffc9e34d04b9f95c32c851
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.1_v3.json — 1745 bytes; SHA256 ce77bd1e8c5166f55c97d67fbe2ffb5d8d74a067e71a5d92889c3358fa3adf97
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.25_v3.json — 1746 bytes; SHA256 9b696ffce9d48b8f7d2f0390174b7d86a56c1adb662fd45094252093fe98854a
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.35_v3.json — 1747 bytes; SHA256 19bfc5d5219f79d582e04ae605d0be0c68029604fd85999cd6586a05cc476b30
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.5_v3.json — 1745 bytes; SHA256 1e20ad239a7c6394b1366494ababf08c711604a79b0fe745cb5ae98c95bfa46b
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.75_v3.json — 1747 bytes; SHA256 e32f5ee96499c8973e2783bdd5f30335ae2a423c4147f6d5ddff885f9d374d87
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b1.0_v3.json — 1744 bytes; SHA256 ad8cd77f41317d76c879411ac130fcd2fea6119a6c3e9f3168dcb5079fc697de
- out/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_blegacy_beta0_v3.json — 1762 bytes; SHA256 bb8311edb67abf30b87cc79835cfe63a790d36bcfa6de3d5d3249cf6c84f84a4
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.05_v3.json — 1746 bytes; SHA256 9741b2522e842c0d646b1a6448a0825676db997d4da9986b6c6a5c6255105e77
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.0_v3.json — 1745 bytes; SHA256 58d9892e4166f026e7c9d3f72f62f43e809201d1f736be59653d06a9de2b6107
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.15_v3.json — 1746 bytes; SHA256 5fbdc609e588b024c66a2c5fa00ec56634e96e6a35eb68e55460629029bc88f2
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.1_v3.json — 1744 bytes; SHA256 f0d9cbbf1ecfc42eb5d3f58629e0c80da242d78393f6b98d196d488e5484c892
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.25_v3.json — 1745 bytes; SHA256 4ac8061e8846b8915f3db620d2970955936c5d5e5bbceb4982e706c668cb4703
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.35_v3.json — 1746 bytes; SHA256 b21816f1baa1e9932e13017f6b5df04972d86e04a659955be4bdd63e4b76221c
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.5_v3.json — 1744 bytes; SHA256 3387c958b2db743d8c83a15a322068044537276ff6f396198e1ff8875253d740
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.75_v3.json — 1746 bytes; SHA256 fc503a5d8675e4fb08a5eff35b350afe3261ab134759759af26dc568453fe9e6
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b1.0_v3.json — 1744 bytes; SHA256 6932f1d1c2bc24cedd1f3346a8d80946a5d89bb6e4b09cd9e52d2f6ff9f28499
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_blegacy_beta0_v3.json — 1763 bytes; SHA256 28c2c192f3fb2ee45cdeacde66d40b744e2b9d532b01d5aeec2d865ec55b3e6a
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.05_v3.json — 1746 bytes; SHA256 df712e622d2ad8f8df6ea48ab4cf31a73939c153f06424540898a3f7fbf5b8a1
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.0_v3.json — 1745 bytes; SHA256 b2a92adfc374354af941bceda7b3f991b9af5d33335e7d21fb7cbb7c0d9d2f17
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.15_v3.json — 1746 bytes; SHA256 bff92dd672f6afffbedee81b348848700d9920de699850d5aac21fab3f05452b
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.1_v3.json — 1744 bytes; SHA256 dd478d175296b24e000ae1dc6672dba1f9edc352c2eed88da3a6150f149fccb2
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.25_v3.json — 1746 bytes; SHA256 0c2c481779512facb12c262d296e553c2ecbf22acb7bb441cef9d8028c5d8e77
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.35_v3.json — 1746 bytes; SHA256 d3688fda3d1b139eaa14a72071df05e8a49bf8fa08a0044ebe8a7fdd294d3161
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.5_v3.json — 1744 bytes; SHA256 eb1e787f20c14ad7cc6f591fbd4e9f819390437c2ef69488b8d2ab4b1fc9a77c
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.75_v3.json — 1746 bytes; SHA256 f507d2a5d4e80f97ffc61666a805c7836cabdb99d4830aeb8af60c9cdcb84923
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b1.0_v3.json — 1744 bytes; SHA256 6257a7329ed0a75e39efc942cad1578d74b3e34cbd34c691b3ffaaafb993237b
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_blegacy_beta0_v3.json — 1763 bytes; SHA256 bcffc41a2a33350e50e58f8b1e05209c31355a373bfcd613153f3931b9aab4ee
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.05_v3.json — 1746 bytes; SHA256 26bd444c1ab279af893e770d9bf265caed4f88f137aa5be82f8da55b7f6aea4d
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.0_v3.json — 1745 bytes; SHA256 2d1576b92934cf2ba6e338a790ba0196830118c8080fc940511246e9be277d86
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.15_v3.json — 1746 bytes; SHA256 4b65387f8a87781c1a6e798b6550e77e47dde38cd645244738db1ba08c0d4a6d
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.1_v3.json — 1744 bytes; SHA256 bd65dc251423c09d407b470d3534327f6f48ec261908d822fc2e6ceb697431f1
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.25_v3.json — 1746 bytes; SHA256 23e9f6a8996f3817aba1c1db7ff2fe7dfbf26d2e2a77db5eeb3e8783dd03a433
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.35_v3.json — 1746 bytes; SHA256 c6721387a4053e012ef6d8e1241e3593c73a47e12e61b79412d944a5c76be109
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.5_v3.json — 1744 bytes; SHA256 5873936bbc7bce48a3ac3963b8206d904fdc595a5a727c7c97bacc5955f2c0c3
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.75_v3.json — 1746 bytes; SHA256 a2f70f85c47712f3ee5b35245909e23ab171976746551cd5c7554810493ed4fa
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b1.0_v3.json — 1744 bytes; SHA256 445a269907047c912d80e53af612177222dd593f6ee6b403f79c75784086a15b
- out/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_blegacy_beta0_v3.json — 1763 bytes; SHA256 ad91206f0df141cff360ba19a0fb208812bf5e95d0f24c6211fb45a63f8da14c
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.05_v3.json — 1723 bytes; SHA256 e6f77e7433d89a35f356f778cca1f61f8eb37eddcc97e66a7dd3e7c2c8390d20
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.0_v3.json — 1722 bytes; SHA256 558c824c13316d7217779d0094d445fdf74f95e8e19d65c9e38f575273d83aec
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.15_v3.json — 1724 bytes; SHA256 8611111d270c2a66bfdb1d1522d4c5e8c6802f7c5c382b2ca83f018577c48787
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.1_v3.json — 1721 bytes; SHA256 d002577ae44b25faa57660d838f35adad3416d8de30fb23f4205b62e06ae977e
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.25_v3.json — 1724 bytes; SHA256 d106480e6a49043d5b3fb5607f92773e0160bde2db2eb3b3b33a8704bafba7d9
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.35_v3.json — 1724 bytes; SHA256 5131dda95866c6f0cac5365b6f5f6ef7544d974b16e750d0fbe8d9ede3f7a383
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.5_v3.json — 1722 bytes; SHA256 76dcfd108462df5a8043df0e1d8066677e4c1a15354d270e5c234f4831fbdc7d
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b0.75_v3.json — 1724 bytes; SHA256 04056b89202e110c2de0fe09280c64403a347a5985a74c34c7eef46009ce393f
- out/phase18_posbatch_items_gpt2-medium_s0_historical_b1.0_v3.json — 1721 bytes; SHA256 a9426360c93b87d52f3188c3664e6569047b3beb2b1c04d31460bbb462f858d9
- out/phase18_posbatch_items_gpt2-medium_s0_historical_blegacy_beta0_v3.json — 1740 bytes; SHA256 1b155f67e77477d86cc7e5ffbd08e27be06fdb6baa1bcb0015313778bef3e532
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.05_v3.json — 1724 bytes; SHA256 e3faa4af5a63882d7ac6fcdb1115d118edbc81e40b2ed1cb4f85eaeaf6708c07
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.0_v3.json — 1721 bytes; SHA256 331f06bd4f3c628817bcca336a26f715031e7f2556f0b2c32798784b43a0cb5c
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.15_v3.json — 1724 bytes; SHA256 b48238cd8ce80dba71af9284c89b3d2e0565de89294ebf93c7244dc83463e90e
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.1_v3.json — 1722 bytes; SHA256 5e3c48e39033abe130a903185c3ed8af83d3b59507f82f2b4bdf993382fa3da0
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.25_v3.json — 1724 bytes; SHA256 5fb0c66b40f84b1c9622e96134f7e781806fce13b88120a98e42cacfb70935dc
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.35_v3.json — 1724 bytes; SHA256 9b7c49857d36a43cece35d3a93e91d1cfee9f152bd5fa7c69ef73e630bfd0b6b
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.5_v3.json — 1722 bytes; SHA256 7cca93e0d5d3df88134fe3b54c29ea7c3160696cf843cf4fe49a92ad1e98839e
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b0.75_v3.json — 1724 bytes; SHA256 d63a028f1cbd16cbe89464f533c63b1fbd7b740df280db351e3801c2cf332eb6
- out/phase18_posbatch_items_gpt2-medium_s1_historical_b1.0_v3.json — 1721 bytes; SHA256 a24a033681e20871d2c8c99c5ab2db267477c2892ffadb0c7f6dcec0c4acd1d2
- out/phase18_posbatch_items_gpt2-medium_s1_historical_blegacy_beta0_v3.json — 1740 bytes; SHA256 90a28514f89911b0319161ebf9b61903c6507af269f2a5c797f1e635d6c159ad
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.05_v3.json — 1724 bytes; SHA256 70daea95da3cd611539e92e793a9aa494630e44b51ecf218cc9f3ad90f0cd84e
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.0_v3.json — 1722 bytes; SHA256 dce24630f3ec4b0152218acd53ce52814f95bc02d6c28eb7a618bc569f98e7da
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.15_v3.json — 1724 bytes; SHA256 fc72514da4e9e5e6c869fc15d167cd6d97b11a6246c1a2b59859c66e61fb4285
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.1_v3.json — 1722 bytes; SHA256 3898c696a53378bc4c401f31dbe8416552f7e36daf1adecfa05273ffe246b824
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.25_v3.json — 1724 bytes; SHA256 346fc9fc7bb177b5b54caf4661bbd20539c430a661088e63f5455e4dcec224af
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.35_v3.json — 1724 bytes; SHA256 018dcfe50da363ba235ebdd8d61a74f863586710e98c9909ca1fa0414a4cfcfc
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.5_v3.json — 1722 bytes; SHA256 e3f8e70bc899336e1717652a52c8d6685d735ec902ae5da753d1e87617063aea
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b0.75_v3.json — 1724 bytes; SHA256 0f099103e0f9774bb4e20d60425fb40b0738eb0bedc5c38027ff010a084916b9
- out/phase18_posbatch_items_gpt2-medium_s2_historical_b1.0_v3.json — 1721 bytes; SHA256 fa1d47d9ea62166976661c9ea3e39d11c74aad185a2ce8579f3ff0aa2f3b5e7b
- out/phase18_posbatch_items_gpt2-medium_s2_historical_blegacy_beta0_v3.json — 1739 bytes; SHA256 81145658bcc9358f21f71923c5beefcd3a08b72ebf7efc04325a7c937bd40e5e
- out/phase18_posbatch_items_gpt2_s0_historical_b0.05_v3.json — 1709 bytes; SHA256 30243dde4274252bd830f338dcd73c391ca4dd394e50b5faf4cd6863086d273f
- out/phase18_posbatch_items_gpt2_s0_historical_b0.0_v3.json — 1708 bytes; SHA256 019c2d7f149a9ddea66dbb255a5653f9ea9bb04e887cc3382fe5050ab1d0cf98
- out/phase18_posbatch_items_gpt2_s0_historical_b0.15_v3.json — 1709 bytes; SHA256 e7b91cc2de7228f191f3ac273206fd2ff979511036f69779c8691a68a526132a
- out/phase18_posbatch_items_gpt2_s0_historical_b0.1_v3.json — 1707 bytes; SHA256 19df1233a590e222b44d352619be9da43b0171c2acb486aa7d1a9ab8df642971
- out/phase18_posbatch_items_gpt2_s0_historical_b0.25_v3.json — 1709 bytes; SHA256 b1a95ae6ab9c2ab3ff6804834e718fe69381e8d4be419851a76eab6156d9360e
- out/phase18_posbatch_items_gpt2_s0_historical_b0.35_v3.json — 1710 bytes; SHA256 964333c3fcc6573506527c271297241301a02e2b01c68cc098d778b12bcce638
- out/phase18_posbatch_items_gpt2_s0_historical_b0.5_v3.json — 1707 bytes; SHA256 a3ae79dee3e614a84b66fd3ba183fcf2ac0ebb55c30aa6147dbf3341df2b89a9
- out/phase18_posbatch_items_gpt2_s0_historical_b0.75_v3.json — 1709 bytes; SHA256 9c6be1628d6ba581d3984986c0062ff628c5c8d2e8508f052b48bd411ee44a8f
- out/phase18_posbatch_items_gpt2_s0_historical_b1.0_v3.json — 1707 bytes; SHA256 152cf75c1715160347893e2ae9c7965079230990b92e7d6407db4b7e6a428fbb
- out/phase18_posbatch_items_gpt2_s0_historical_blegacy_beta0_v3.json — 1727 bytes; SHA256 a7af6a70d2bc7680f86aaa010833f8cde490e59dffe04704512933fdeb914dc3
- out/phase18_posbatch_items_gpt2_s1_historical_b0.05_v3.json — 1710 bytes; SHA256 5600b8ee05da250032b241e31642afff3903fbf616a2b6755872be0b5d0ee4bb
- out/phase18_posbatch_items_gpt2_s1_historical_b0.0_v3.json — 1708 bytes; SHA256 a4bac996758f9d54cabc93e44ed1bbca6dcf2ae1dace190c7ccf299dbd0130a2
- out/phase18_posbatch_items_gpt2_s1_historical_b0.15_v3.json — 1709 bytes; SHA256 3c778e56ae5aa0a35ebc8426ec44fa10cc1cb9f1ebea91a23dc8c71142f40c3f
- out/phase18_posbatch_items_gpt2_s1_historical_b0.1_v3.json — 1708 bytes; SHA256 8cc1d20a81b191caa91c9c1ac64d7f826e3407c1565f9bd2be6b3ab2c4550bfe
- out/phase18_posbatch_items_gpt2_s1_historical_b0.25_v3.json — 1710 bytes; SHA256 85c49ab65be5ce82f2f907b69b237ab34688bd612df5d81cd0aa34c8b2ffeee7
- out/phase18_posbatch_items_gpt2_s1_historical_b0.35_v3.json — 1709 bytes; SHA256 ac0f4002c5a3cb614b8a329950b366f2620a939943089fc4ae5cdee67b11cd92
- out/phase18_posbatch_items_gpt2_s1_historical_b0.5_v3.json — 1708 bytes; SHA256 0b264c10a9f2e74304c506754baefb4da0a68f49b584153383264c0a2c407a22
- out/phase18_posbatch_items_gpt2_s1_historical_b0.75_v3.json — 1710 bytes; SHA256 4a8e5b85cf57c8427c068b8fd241d1a5af2508c4e792a8c6d2fc916fe204f10d
- out/phase18_posbatch_items_gpt2_s1_historical_b1.0_v3.json — 1708 bytes; SHA256 ef563ab47258a7a6d1317c05281a2550d39c4e17ba05c8c18e2796798db5e1ad
- out/phase18_posbatch_items_gpt2_s1_historical_blegacy_beta0_v3.json — 1725 bytes; SHA256 ddddaa93dd28c17c859485796d2cb71e97f5fea85ba1415b86c2a06e95c4edb6
- out/phase18_posbatch_items_gpt2_s2_historical_b0.05_v3.json — 1709 bytes; SHA256 86beb0446d4a07ca540d9f33bfdfddfaa5f648e52a746e647d3e6a164a604a67
- out/phase18_posbatch_items_gpt2_s2_historical_b0.0_v3.json — 1708 bytes; SHA256 b9979ef0b498c3bf7093b1e8169269d3527dbcc492f57bddb9d1c66115edc706
- out/phase18_posbatch_items_gpt2_s2_historical_b0.15_v3.json — 1709 bytes; SHA256 2c71f628928ac825e30c5441c16da8446cf87e456f755c2a375f7426dab43eca
- out/phase18_posbatch_items_gpt2_s2_historical_b0.1_v3.json — 1708 bytes; SHA256 c49d3201c0c8a56ed6adb39f79ad61727ee9222051e5446b0afe1f1f3f98be1a
- out/phase18_posbatch_items_gpt2_s2_historical_b0.25_v3.json — 1710 bytes; SHA256 a3c0fb2ca1be7695e385110ab3d7375f2d732c3bf3f1c1ea11af7a440a434cde
- out/phase18_posbatch_items_gpt2_s2_historical_b0.35_v3.json — 1709 bytes; SHA256 7f3a422f61b4a298062837f3800ccba51836f15cb89894e2d9cba2460503b5d6
- out/phase18_posbatch_items_gpt2_s2_historical_b0.5_v3.json — 1707 bytes; SHA256 5d7a24d89f9cf84a61d5dc30809cf620a05ce3d9163028652e758c2461625a28
- out/phase18_posbatch_items_gpt2_s2_historical_b0.75_v3.json — 1707 bytes; SHA256 db0ff92b5fb95eb8787319424bde73c13690757ced6aae45d83f5f4ea10e5ab4
- out/phase18_posbatch_items_gpt2_s2_historical_b1.0_v3.json — 1707 bytes; SHA256 d47ffd80a4990699e4b5733e5d1b4cf28a94c7ef45a2687392ec1d8e63214b69
- out/phase18_posbatch_items_gpt2_s2_historical_blegacy_beta0_v3.json — 1727 bytes; SHA256 4cb6c84b6d57e5aa51618a4102ed25cca572ea79084c619bec24d6aafd817cd8
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.05_v3.json — 1737 bytes; SHA256 a4d3941a621375a1742586d364fdeac1cc3f28b2e415ea78afe849147a4d9bab
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.0_v3.json — 1736 bytes; SHA256 c4cb5c1b94fe78ab5e1b6e1f8b17f69ae3269e8d150547947aed8935cde72f66
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.15_v3.json — 1737 bytes; SHA256 c666984de64b29792250c84e0e79d1727e8fb44a7a9aa2d6358841f6b0080579
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.1_v3.json — 1735 bytes; SHA256 5936f7d53bdc721e9aa929afa5db9bf6ef9b6b76db7356ca3f195f4b8d3edfe7
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.25_v3.json — 1737 bytes; SHA256 795b0689fbeaa24c28ee77df6d8e27e6629791fae2cd3d3fa05b588e12e368aa
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.35_v3.json — 1737 bytes; SHA256 981a0051507721ae10ddfd1b69d75cae42ab5c158993c055ed872b82a760ed0f
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.5_v3.json — 1735 bytes; SHA256 d6581b6a54f775729756654c1b0c2ac172b778ad96fdc20a5a044d042c6e8d04
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.75_v3.json — 1737 bytes; SHA256 a0d592bf1beb0dbd17f0512541d5b492a96301480260d578e0924bf191f63d3c
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b1.0_v3.json — 1735 bytes; SHA256 17c4c7a718cbc8a12bd4a2b19c7099a7bd45faa083e6e8b9835420503c7b57dc
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_blegacy_beta0_v3.json — 1752 bytes; SHA256 7ae371643a1dc3c5fed7d5b195a10ff97421b7cc677725a9d6e1f7e202aebfbb
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.05_v3.json — 1743 bytes; SHA256 07215889ccd4f4b32288dfe70db6c001ce3c8a61c438934f476a685aa7b1f5c3
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.0_v3.json — 1742 bytes; SHA256 dda7a22f91d1668d7b6688918509bf6c5c424c0a024e4fe45ce23ec78b03fc7e
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.15_v3.json — 1743 bytes; SHA256 a5194446bfa1cbd11a7a7774a09bbc24e972784d235460d1aaa67c83dae1367f
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.1_v3.json — 1741 bytes; SHA256 db2c56d7508c94ba3bd09bfd712d89d24ce85ac67f6b45de7aa3e55022b5a92e
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.25_v3.json — 1743 bytes; SHA256 11d188a11f5337ab5dad4f19066766d45b350891af991a53036b0fbe48028750
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.35_v3.json — 1743 bytes; SHA256 8c2ffc8e16045aa0c59fbff7753392dac1f9d2c354d028a6b806db898d3305fa
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.5_v3.json — 1742 bytes; SHA256 248b92585b183262d614ce1c3e9bcc22e5ccd0c18d19542ea82b204e10f41fa3
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.75_v3.json — 1744 bytes; SHA256 a0c156bfa03451ecb6fa81aa753230dbaa9e1eae87a4026d4cdb659243777130
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b1.0_v3.json — 1742 bytes; SHA256 9eefc40540f2afb0b3a400cc90dd3b020208bf07e9df6cf800b792836f22c194
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_blegacy_beta0_v3.json — 1759 bytes; SHA256 475d3c1de1bc2553d7b0bcdb3ada726eeed9d5a163ab04e098da6c2839d5550a
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.05_v3.json — 1737 bytes; SHA256 957aab9e5877307780e177c4ee2e7f9b9baebaee892896612ef9e30ba80e9975
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.0_v3.json — 1735 bytes; SHA256 48f23ff4afd2b5b7cdb41630a5e47ec0a87b47e0e46805686b86c05349f802fb
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.15_v3.json — 1737 bytes; SHA256 69f7c91ca9fda33ca440fa3c5bded71abc6ce75b97b18f459f27bf17d2a6db87
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.1_v3.json — 1735 bytes; SHA256 6f93fd7ae5a5af575a85dfe40a7fc0d54286ab2b30884450c54cd613aa3408be
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.25_v3.json — 1737 bytes; SHA256 6dd0119fb280d7b795814734a476e81b359768efd7b66f5699eb25718e41b212
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.35_v3.json — 1737 bytes; SHA256 83c339d66b7ea3b3dc57a56049654e7bb952ec1b1698457f95ddb1e53d7d6f3a
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.5_v3.json — 1735 bytes; SHA256 d3a960f33c88ff6b1e426a9a4608b2d5cea7b34d04d1e026927a0e10be16b6bc
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.75_v3.json — 1737 bytes; SHA256 7fe4165f247b2c362b4b93d9facf2ee68d58f1d7f9af4757aaba4da3a6d0cf27
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b1.0_v3.json — 1735 bytes; SHA256 5b68bfeb229f9e8f6b2219954ff9699d7c99e00577dc2c5be481543dd2dfe188
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_blegacy_beta0_v3.json — 1753 bytes; SHA256 81da18eba8a47fd4bdcc481e3fc40b6d732d68cb4df6d0694caa0aff10730084
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.05_v3.json — 1743 bytes; SHA256 a30f3d4dc4c6a11ae9766896288673a50126ca9a12893d2b51d684e6bfd951c9
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.0_v3.json — 1742 bytes; SHA256 e06620ae721a613daad8e9c89183bd6bf92c3b26d99e6355124ff84dd3fa161b
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.15_v3.json — 1743 bytes; SHA256 6ff683acb171f706c56865b8567aae584609ea99a69a9ee1fc4db81465ae44f4
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.1_v3.json — 1741 bytes; SHA256 7d02e1496080eba9bfd5b6add3bc040e587b51a4e6d7dacf45fafe4c67424f86
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.25_v3.json — 1743 bytes; SHA256 bce18dae0d3bc40c7e0641bd2921009951fef9db6f123687f6fccc2c3f6f9ab2
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.35_v3.json — 1743 bytes; SHA256 71ec2ae433a269d3d3f9024682c89fe0b97d63d70f74dc332b126b47bf50341d
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.5_v3.json — 1742 bytes; SHA256 c80ca19f78ca269f7a2a24ac5f563f97ee9a2e2b551c53d9375046f3eb901a05
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.75_v3.json — 1742 bytes; SHA256 fd935a00784270757de4b1cc3f008cc120f63d744c50b2d0865fce4dde2c4487
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b1.0_v3.json — 1741 bytes; SHA256 1d8ca309820b3d5539dce32b58aca442f8585b3ed3754d824d9c667f835312c1
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_blegacy_beta0_v3.json — 1761 bytes; SHA256 5886c25d4b9d3fe2b2b3aff08ba81b7941f48fbd529f23e0cd7b5ba95dba75d6
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.05_v3.json — 1737 bytes; SHA256 da2339eb930a68342dbfdbeff994217ea5a8ac6d6fc75a638402829aae97fa97
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.0_v3.json — 1736 bytes; SHA256 a6d932eaa30c273fa2e980aba2da7594da305cfcf04412448c420911bc969b17
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.15_v3.json — 1737 bytes; SHA256 ef4e37f9aa103a8ee99fd2e0dd811ba3b70c6490cbf3e75755e1049973a76b4b
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.1_v3.json — 1734 bytes; SHA256 79168a9fd2f7ce0a728468e6685f517de32f8c864db7553331dba91d213162bd
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.25_v3.json — 1737 bytes; SHA256 9692c884e343a4eff6f81b0678b9fcb3b89b5373da7d521a90c11f4294b4d881
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.35_v3.json — 1737 bytes; SHA256 5bf2e3a563172dca8f7056aa6d9b1ec17971ee12a44e2c30d064024ab7b17507
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.5_v3.json — 1735 bytes; SHA256 270bc33cf34db1bf4a7cb1cb11bbdb9cf6132fd59616146130794ca3a5c63784
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.75_v3.json — 1736 bytes; SHA256 30e4b0c1c28265ed9ce4fa4945a9379705b44ec2486b48a471025d17707f9eaa
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b1.0_v3.json — 1735 bytes; SHA256 566e4316246516574c794313ac2eac29eb30381f96f173038a6530a9bb8b8fa5
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_blegacy_beta0_v3.json — 1753 bytes; SHA256 21013dc6dae6f60db224ae7859b919af348e6b1ad6d4947fe77c946048f34cd6
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.05_v3.json — 1744 bytes; SHA256 567a7cfd9a9b387daa52e3d2205e36c68d2323c396bc80f5f060e09259754e58
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.0_v3.json — 1742 bytes; SHA256 909c9e77a518b423f3bfb677ddda840daf78bd5ef56737029fa91f1cf19fc4d1
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.15_v3.json — 1743 bytes; SHA256 5de21c74720f3d2dec4ce641f5218d4325753c59869b2e75013f980c113fd9bb
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.1_v3.json — 1741 bytes; SHA256 39ec13833a53373a6246414586cd764f9ea030fc1457d35038538e796e6ace88
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.25_v3.json — 1744 bytes; SHA256 2009b78d69ddf67acba3e962c2f1d558e8d859d8d21bfbefdd730d4658bd0e9e
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.35_v3.json — 1743 bytes; SHA256 3c269ec6a93aad2629e48df66131457724b47db975cc57cb9e2048a723b10755
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.5_v3.json — 1742 bytes; SHA256 6e59e09be1954ddfe1e44374754c50b5729fa39503ad5ac8f0fb2bd37d3e0f0e
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.75_v3.json — 1743 bytes; SHA256 935d8538fc927476c18bb0a43b2a3f5acdf1d9f5de9f0a09577c8c4c81699a6e
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b1.0_v3.json — 1742 bytes; SHA256 eae500b19aa055349af55e4b3ddc08a05351e555ed06a9a817583daff9268507
- out/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_blegacy_beta0_v3.json — 1760 bytes; SHA256 608b2a3912bb5ca08a453deb9417e8acc3d2bf1a3801bd32f2910b992e463154
- out/phase26_named_EleutherAI__pythia-1.4b_n128_ci_v3.json — 290569 bytes; SHA256 0b4a68d578447680245d07a4a760cff847389b2584f85e5006819c42d46a9a7c
- out/phase26_named_EleutherAI__pythia-1.4b_n256_ci_v3.json — 290613 bytes; SHA256 a759007a2a2186998ef09e3c6a0e44a71539c1f63725ea790890cd5e9a25c9bd
- out/phase26_named_EleutherAI__pythia-410m_n128_ci_v3.json — 290518 bytes; SHA256 c69ab3316a97a5f3322e2521082dde17763799de9da5f0a893770c624aa4abe7
- out/phase26_named_EleutherAI__pythia-410m_n256_ci_v3.json — 290569 bytes; SHA256 520df0ff093ed769528f8897c071bc0b0cfce8544bcddd8dc1a7014d439bf3ca
- out/phase26_named_gpt2-medium_n128_ci_v3.json — 290420 bytes; SHA256 d47b533a4d749d5aede679ed8f50fd223768d865bd873950d1b81bf3588f965e
- out/phase26_named_gpt2-medium_n256_ci_v3.json — 290408 bytes; SHA256 6a6833b26a83b93d869a3f3f168a05d1e8af0d4e59a01d0365e9b49de1b1a8e1
- out/phase26_named_gpt2_n128_ci_v3.json — 290333 bytes; SHA256 50a021877699dceb360dd5857bce3c563cc52752e290bc22d53cf15971065b09
- out/phase26_named_gpt2_n256_ci_v3.json — 290297 bytes; SHA256 8c2a39c9b0d0a74ea81b92629b7768bb6b0d808a269e75934e28e0b045d72a90
- out/phase26_named_Qwen__Qwen2.5-0.5B_n128_ci_v3.json — 290586 bytes; SHA256 729b46014ac0663d1ba507aed94b34a1053b01bc23a44707bc56903fb0d1a0c4
- out/phase26_named_Qwen__Qwen2.5-0.5B_n256_ci_v3.json — 290549 bytes; SHA256 a6398d667c4ec998d1674d98f0ef653748df63506523259cb4506fa3f8967520
- out/phase26_named_Qwen__Qwen2.5-3B_n128_ci_v3.json — 290559 bytes; SHA256 031df2ad5ebc3cc68b136949760adc242184260b8cd0f0a8691cb1753fdb4390
- out/phase26_named_Qwen__Qwen2.5-3B_n256_ci_v3.json — 290582 bytes; SHA256 967fddb7a7d4b957ac4b734b1c328ba0a9857e692327db453f24b968d7b6a6c1
- out/phase26_named_v3_ci.json — 4174320 bytes; SHA256 3c9cbf836cb4a55b8b0c3ce50a0cb61af23aab0dfe663b7d96818e6bf1dd315d
- out/phase37_mass_matched_checks_v3.json — 231 bytes; SHA256 c7da97cab0ff98b869dd57c5f34815d4f9f747255364fe47e23a0b4516f8ea5f
- out/phase45_positive_equality_checks_v3.json — 29376 bytes; SHA256 9a8626895fde69e8b77695956b77b813c2834b64c3364cc4eccc39a80d03acfa
- out/phase7_editability_v3.json — 1664178 bytes; SHA256 59644fa49e280ceffb998be279dc26abc99a17474aad9742c1603d65d578be4e
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d000_016_v3.json — 1291 bytes; SHA256 dfb67eaff5490378287766d1b98e381983a6b736809134df0b2d52ae0c72f475
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d016_032_v3.json — 1292 bytes; SHA256 62d756d6c4f413f09aeaa1db4d26794dd1d685a810dc5de4fe419fb0755526cd
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d032_048_v3.json — 1291 bytes; SHA256 e0a37acc5d18ee82747837b6c9a1225b91629ad06c7fa869de5f51cafe015c27
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d048_064_v3.json — 1292 bytes; SHA256 1cb54094bc578feec35abd94c12b275ffa2b24ab0b84f9f06ba5bb008faa7f7a
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d064_080_v3.json — 1292 bytes; SHA256 639201955b3110bba01b8e00add2b8d564e32a022f9024f3ad467c4e1ca005fa
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d080_096_v3.json — 1291 bytes; SHA256 556f620a0b47ae811ee4faf0a3d76d9c2455a133cf99e25426850461ab8f4b8d
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d096_112_v3.json — 1293 bytes; SHA256 1382d0feb93f8c1c5cf8fd4a3b43c2039e3be52e37dd8fa901d95324d690994f
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d112_128_v3.json — 1294 bytes; SHA256 eff7e5a6255a2d0fcc3b4a3d9aee657c1003ba4bc2da70d3d43d4d9a8e076bb7
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d128_144_v3.json — 1294 bytes; SHA256 046c2ff7ebe639e624b696637ca7bcd91c44f6e5f1e897dcb32bad771a94deac
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d144_160_v3.json — 1293 bytes; SHA256 4d51adb397bb4ac8f7bfabad185b748f2592280f967ef956fb8305c39689ef11
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d160_176_v3.json — 1292 bytes; SHA256 766fcfe7ec47af044bf25dc1e71c90f47cff12ed474d61a9b6de2b78ceba8982
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d176_192_v3.json — 1294 bytes; SHA256 3063fc8b71e74e64ca3d1dd0e4145c6fb91b20655652e526f0874a27a04b8456
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d192_208_v3.json — 1293 bytes; SHA256 a569a3f5f26e5e7da18863aec8e898516bc7cb041ef19d0b7d29040b9f8cd566
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d208_224_v3.json — 1294 bytes; SHA256 d023aa6a963fe109dd97f769ff145a8c01c31600c3e37953ff00a92256716abb
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d224_240_v3.json — 1294 bytes; SHA256 43c84ede87f6b40002cc7b6a56cc17b7a79d4f4daf2c580f5da775f25fae35c9
- out/phase7_massmatched_EleutherAI__pythia-1.4b_d240_256_v3.json — 1294 bytes; SHA256 8dee9019423537922c1b41d8df0227dfa01667d952c135dcb1088d8a8992b170
- out/phase7_massmatched_EleutherAI__pythia-410m_d000_016_v3.json — 1290 bytes; SHA256 295137d15f15bc1bd11a16daaea8adc6d0c296dadbf15c74dc144685b1c1f962
- out/phase7_massmatched_EleutherAI__pythia-410m_d016_032_v3.json — 1291 bytes; SHA256 ed37876efc17b1673444568e28ccf850ff0c9e06ac7c1910ae3f8238babe5207
- out/phase7_massmatched_EleutherAI__pythia-410m_d032_048_v3.json — 1292 bytes; SHA256 4ca1f3d9f7cf24a7339083a2d031d836337ceef6af3acbea8dbfc15f914f2a38
- out/phase7_massmatched_EleutherAI__pythia-410m_d048_064_v3.json — 1292 bytes; SHA256 09a12fe05224a4dbbe6d2fcbe4d92d0170dd22ffe8a3dda431d289d751eec08f
- out/phase7_massmatched_EleutherAI__pythia-410m_d064_080_v3.json — 1292 bytes; SHA256 92fc200b1c5b2d791726f084b090768d9bf242833303fbd042721e779d5e7b40
- out/phase7_massmatched_EleutherAI__pythia-410m_d080_096_v3.json — 1292 bytes; SHA256 28dda180d1ecb3f52ce28db1bc636afde7bca40d13f873485c3d50b9c2a6579a
- out/phase7_massmatched_EleutherAI__pythia-410m_d096_112_v3.json — 1293 bytes; SHA256 6eeed4a44e8dede9ed8bcffe25571c42468373cf03c64dfa6c537d1a6ea59986
- out/phase7_massmatched_EleutherAI__pythia-410m_d112_128_v3.json — 1293 bytes; SHA256 37162d024f9fe5ab7aea4f592891bbd7f0357ad6589569960f500a765bb86077
- out/phase7_massmatched_EleutherAI__pythia-410m_d128_144_v3.json — 1294 bytes; SHA256 5236a5909731c385c7e3adca2de7059b53cdfe8160c89a507abede48bbb43b29
- out/phase7_massmatched_EleutherAI__pythia-410m_d144_160_v3.json — 1294 bytes; SHA256 fca65489386294c865bcffa2e7c2e44f16e508730218779621d79bbe634629c6
- out/phase7_massmatched_EleutherAI__pythia-410m_d160_176_v3.json — 1294 bytes; SHA256 f550cfed2b6f75dca87e9506921d95a6b6598be99cfd9119b86171fffe3aa0a1
- out/phase7_massmatched_EleutherAI__pythia-410m_d176_192_v3.json — 1294 bytes; SHA256 d9c006e18546fe28f01272632ab86b995f5768b1c7f389e0d0a2c6573e9ebf7d
- out/phase7_massmatched_EleutherAI__pythia-410m_d192_208_v3.json — 1294 bytes; SHA256 572e96ecdb23f3ebc0fa2ce0f14e49951dc085178626b168025afad64a84fbe0
- out/phase7_massmatched_EleutherAI__pythia-410m_d208_224_v3.json — 1293 bytes; SHA256 c108dc5c9b5309ddedadc50907e8f149f906f4fb346244603525250d2eb33b13
- out/phase7_massmatched_EleutherAI__pythia-410m_d224_240_v3.json — 1294 bytes; SHA256 84abc9172d34bb2e8785ee0f0afc443281aaeea42bdeb97541b979b9406e6e0a
- out/phase7_massmatched_EleutherAI__pythia-410m_d240_256_v3.json — 1294 bytes; SHA256 67c27ad023814a9ceef96b8b9c1c5d6269e0819f2ddb4aa5b43dc9fa6f8979d1
- out/phase7_massmatched_gpt2-medium_d000_016_v3.json — 1256 bytes; SHA256 4936a6537ad9f90bf69a57c4ee210a31e1f1f824c0f8a841bfaaac7ecc4b5e58
- out/phase7_massmatched_gpt2-medium_d016_032_v3.json — 1256 bytes; SHA256 d03d925488cffb73cbd84b95a612c6748f3c77479bf8daecd3a058981b02e782
- out/phase7_massmatched_gpt2-medium_d032_048_v3.json — 1257 bytes; SHA256 7e5a35b2d2234689f9ee5392c08cc87e23ab090bceb8130491855a0a5a76d6a5
- out/phase7_massmatched_gpt2-medium_d048_064_v3.json — 1257 bytes; SHA256 4d6dc180e6c3197d56b866e54e1e19007e53a64b55214a1eaeb28cacd18bcb0f
- out/phase7_massmatched_gpt2-medium_d064_080_v3.json — 1257 bytes; SHA256 4f882d559f3fcf5fcd8118749473d7852381b31fdc3d0dc5f8bc0587684eae4f
- out/phase7_massmatched_gpt2-medium_d080_096_v3.json — 1257 bytes; SHA256 96fa81e5bcf47bb922e218b83d22a6384d852510d0347a21e4560e3077823c88
- out/phase7_massmatched_gpt2-medium_d096_112_v3.json — 1258 bytes; SHA256 cf8b06bedf06cf142a7909db61734338022dcd0e1dfff0aa6f9d6fcb081a734e
- out/phase7_massmatched_gpt2-medium_d112_128_v3.json — 1259 bytes; SHA256 4f858c5efe65c690080108f4d6cf5e4c583684a8d809a311575017d8e29b4424
- out/phase7_massmatched_gpt2-medium_d128_144_v3.json — 1259 bytes; SHA256 2c88dc1ee949b03ab9e0600e46d9653a2cb68adee58727445f558fdb30dce8e9
- out/phase7_massmatched_gpt2-medium_d144_160_v3.json — 1259 bytes; SHA256 874db092e190605b4d01d4ef65a78d535b1c51e4b3c07227df78a809337d648e
- out/phase7_massmatched_gpt2-medium_d160_176_v3.json — 1258 bytes; SHA256 fe593dea6039a599446676126c290ba2ada55b3289dc1f9c5f01ade7d5cb3a95
- out/phase7_massmatched_gpt2-medium_d176_192_v3.json — 1259 bytes; SHA256 7fbfe13f2513c357801d1e9a33f4a62f680537d7e8afb1169a38795994352cf2
- out/phase7_massmatched_gpt2-medium_d192_208_v3.json — 1259 bytes; SHA256 0be69349b5269462adbd1f003305c318bb02ed8003ad3886bc47c8bcb4f3ccf3
- out/phase7_massmatched_gpt2-medium_d208_224_v3.json — 1259 bytes; SHA256 66b81b9f9b2beb5bb86a622354e9a2875e1bae2ffad9d12244cd37fb774af9f7
- out/phase7_massmatched_gpt2-medium_d224_240_v3.json — 1258 bytes; SHA256 1826a5659922b1f90b22ae21e7ade915eb75f491b905d897fa14e1ce19846962
- out/phase7_massmatched_gpt2-medium_d240_256_v3.json — 1259 bytes; SHA256 409dbf2340dcbe75cd26dc746aadf608f1f839ddbdcc09c44f55de1f63bc2b6d
- out/phase7_massmatched_gpt2_d000_016_v3.json — 1234 bytes; SHA256 22addcb68bc0488c068a47b6390aab21710b0e7baa95d58ca360e51b3e2ee41f
- out/phase7_massmatched_gpt2_d016_032_v3.json — 1236 bytes; SHA256 e517c26b5587ed11e5016eb47064a5979477250aaa54d4226b351d9ce202bef1
- out/phase7_massmatched_gpt2_d032_048_v3.json — 1235 bytes; SHA256 637f943fa8acd7f5ef23b644fd531bdb51793939b3b8dcad417edda95f80a52d
- out/phase7_massmatched_gpt2_d048_064_v3.json — 1235 bytes; SHA256 80ef5208863dcae49442a34bfebb9fc7f4f64f491cc29c002f251cc14c26683a
- out/phase7_massmatched_gpt2_d064_080_v3.json — 1236 bytes; SHA256 816df247e8da79ba049a345a92c67a30cc05f7a83ef3096ae64d8f5ec557c53d
- out/phase7_massmatched_gpt2_d080_096_v3.json — 1234 bytes; SHA256 5a3b35a2474cc09cb3fac44e9fbb65ff3ee502697f6e491d5febb157d4f04e44
- out/phase7_massmatched_gpt2_d096_112_v3.json — 1236 bytes; SHA256 ef6a1206a7cee0a848f083f1b7a45e2aa46af7a73ec6948778538c4b130e4314
- out/phase7_massmatched_gpt2_d112_128_v3.json — 1237 bytes; SHA256 9a60779d9c9525f68495a937df1c52e0ccdd6813747c706c9bb73bd40c229f9d
- out/phase7_massmatched_gpt2_d128_144_v3.json — 1237 bytes; SHA256 9a2314af01e529a1b16f1cab9ff08e2bdd7f91e9f575d2d3a76643eeaaedafd8
- out/phase7_massmatched_gpt2_d144_160_v3.json — 1238 bytes; SHA256 805c0bdf15f5b8577e0f6ebd87620ee86bccfff6f7c596b3c3040f75b7d94e15
- out/phase7_massmatched_gpt2_d160_176_v3.json — 1238 bytes; SHA256 154d36442df00f3f0ca692bec49c641bd9d4e52bb8595e096690364df027c0fc
- out/phase7_massmatched_gpt2_d176_192_v3.json — 1237 bytes; SHA256 ed2fb89d7e79a34b54471b7470837fbc821a6df21c7768237a9068962b3cc87c
- out/phase7_massmatched_gpt2_d192_208_v3.json — 1238 bytes; SHA256 66d77927ae56fc7330ce9f6ce805bd2a3b73449f04f1381df0df836b5fd24b97
- out/phase7_massmatched_gpt2_d208_224_v3.json — 1237 bytes; SHA256 a483f79733a573d55bb8d687e68692a2ea770797f86fc28883b1e9c6a2faa4c1
- out/phase7_massmatched_gpt2_d224_240_v3.json — 1237 bytes; SHA256 c5acdaafa95c2b750d71e326a5ed8d1fb4e972a0b85be54f797016873069a3f4
- out/phase7_massmatched_gpt2_d240_256_v3.json — 1236 bytes; SHA256 dc59750c9c7ae7c016e20cd6e4a0b04907de6395ad828aea3e6dfe8f7db9f7df
- out/phase7_massmatched_pilot_EleutherAI__pythia-1.4b_v3.json — 101534 bytes; SHA256 6d48a41859d0532e3f23060c9ba4ddc897f85e008943cc543e697be7523ab1bb
- out/phase7_massmatched_pilot_EleutherAI__pythia-410m_v3.json — 101535 bytes; SHA256 23e426b9da0cdb43b74cab68de4416256aad0f85a5a377fb0844a8f65ce6508f
- out/phase7_massmatched_pilot_gpt2-medium_v3.json — 101524 bytes; SHA256 18365feee98bda906a35dad6fc8116d661e3812ebb7f6dc47eb6438a552446e2
- out/phase7_massmatched_pilot_gpt2_v3.json — 101518 bytes; SHA256 96771664ae9a085a1b7549e33706ce05f0383b9aa115dd3836f924b46db552f4
- out/phase7_massmatched_pilot_Qwen__Qwen2.5-0.5B_v3.json — 101530 bytes; SHA256 d99808945601d11cbbfeef9a8d0ac662970b1fc34940a260f12a58bdebdbb1b1
- out/phase7_massmatched_pilot_Qwen__Qwen2.5-3B_v3.json — 101530 bytes; SHA256 4041eb1dc5bf96752b7b7291c590a52d03c6bcaee22c9525184b465ae46a5bd7
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d000_016_v3.json — 1277 bytes; SHA256 57a994e8629879496ce4a284f93f44a961a714cd62d3430072dfdb858323fe70
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d016_032_v3.json — 1278 bytes; SHA256 5817b884dc895498a466d3d23d3842825dc04adce0d6603136872140d387c674
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d032_048_v3.json — 1278 bytes; SHA256 aaa3eda7a43cb5af11908d2cf4e03fe17d29cf5a1587fafbdc8f0268dad59f36
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d048_064_v3.json — 1278 bytes; SHA256 597c83da049d973217ae4396a7121a00d2d9c190ad28dababca49b44a0328166
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d064_080_v3.json — 1278 bytes; SHA256 59c0cfc4c44120f996ff6d24bb228af06e3aab9b32e9d4680bc7c1853cb9fa36
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d080_096_v3.json — 1278 bytes; SHA256 dab7941358fcc5d0d37283d08e2ebf52128433793be796677968d2c0b058e45d
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d096_112_v3.json — 1279 bytes; SHA256 43d2efebfe6dfc61ba9f755aa0690675486a4b6e756d76089f5ce6cab7adfab5
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d112_128_v3.json — 1280 bytes; SHA256 16a218d1a11f50c0dedeb0800e08b37b78fd7cc6e6da47dd70e36c190b909bfc
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d128_144_v3.json — 1280 bytes; SHA256 26c38d230fab29b0b1e7648c08c73a76a942e605fbb5efa6565cb1cbbc27b06c
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d144_160_v3.json — 1280 bytes; SHA256 ca4b06a6346cc6144dee80197fc4b6f894ce8a80a684ddfa825aa6dd8caca0fe
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d160_176_v3.json — 1280 bytes; SHA256 0eac838207b2f4fec4e4313bc66bf863f9e98b384c1f1819fd7bf221257ff343
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d176_192_v3.json — 1280 bytes; SHA256 4ebad8c3e8e02c045cb3362161e64f4214035c853a3c2dcf71d7405ee6cec976
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d192_208_v3.json — 1280 bytes; SHA256 f4e98e5a4c54fa791adb7c98d8605a6f4f8223b15b31e04bf8c146cc17788138
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d208_224_v3.json — 1279 bytes; SHA256 a7591068f3378acae533e6d8cd32a178708fa756da5a624c1016c80825420e48
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d224_240_v3.json — 1280 bytes; SHA256 44acf9bac251cb37f575ccba7dd19086316da7f08109bb3db105a8e7ee6a9707
- out/phase7_massmatched_Qwen__Qwen2.5-0.5B_d240_256_v3.json — 1280 bytes; SHA256 b6765ed7f4c0056857ba9752410e0e50b1851ed09c2f3a4f98392a8a5d8bffb4
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d000_016_v3.json — 1270 bytes; SHA256 c6483819774910674f1062c9915d731f77f8eb6b3c2eed1a091d4cc67d5eee7c
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d016_032_v3.json — 1272 bytes; SHA256 ed95ee0e3ff307da85fcb0f23be64c5defe21887c937aa6608533ee868bebaab
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d032_048_v3.json — 1272 bytes; SHA256 444fc268274de85efb758b4b80d668528ca2018623c145dd447a76ae360c31f9
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d048_064_v3.json — 1271 bytes; SHA256 f8f4e23b69402b7f3094c4578119cb763e150f3d888fb7b0b152a21e332244d9
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d064_080_v3.json — 1272 bytes; SHA256 063b7c6eb85d807c3107b46a207042fb9c9c8c7dde64f9d3ec45e531c31db992
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d080_096_v3.json — 1271 bytes; SHA256 308a4ba7b4d3b7e6861874eee904fa6a498a3223fad8dab6569478993ce580be
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d096_112_v3.json — 1273 bytes; SHA256 68af58114c902e59b36c3a186303dab5bd64de0e065a740a4649a95dcad02d49
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d112_128_v3.json — 1274 bytes; SHA256 58d694aad75882ab24dd82c9aa08ae804ad1be4adfeeb61ceaf2f6193903c539
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d128_144_v3.json — 1274 bytes; SHA256 edaad3c3da689930cebe82a9f153f103377bead73f0bab9b4d319e0d363d8153
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d144_160_v3.json — 1274 bytes; SHA256 274422c19ab5d6bbf2c3c16a86df0fd4199b95d866e57b1d81d5d2bc7e1b42a5
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d160_176_v3.json — 1274 bytes; SHA256 43ca7b521cdc948b3426c9a3e99bcbeb92e61c206ce2918d9aede06cb43e1dfa
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d176_192_v3.json — 1274 bytes; SHA256 efa3e5b0b52309cf9acfebeb901b377a51b19d09b43e7347f5198e7c88565312
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d192_208_v3.json — 1274 bytes; SHA256 17710be40e8304694afed1aff5cb816e4dcd3b2e8de980c818eeeace84593abd
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d208_224_v3.json — 1273 bytes; SHA256 33db7f8efec405c1a1c73833f7f16d4ea7ab6d2bd9f01855c47727a8f52b8f51
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d224_240_v3.json — 1274 bytes; SHA256 e0df058920417262b9a7dfd1f41f6a21e00b56a940262ced761dbedcf406c274
- out/phase7_massmatched_Qwen__Qwen2.5-3B_d240_256_v3.json — 1273 bytes; SHA256 1dc8d5eca6892e295764db6b1457cd818399d6414ae8435baa668f73e65fd608
- out/phase8_beta0_statistics_v3.json — 442392 bytes; SHA256 1289d603368367c2be9807d460b08377f0d71e0ced19d8ba6433b8a85ae2c774
- out/phase8_items_EleutherAI__pythia-1.4b_s0_historical_v3.json — 1399 bytes; SHA256 e890899dee31187ba995119a14987b81d78e86bfd4d620e54de0b6bc3e858d9b
- out/phase8_items_EleutherAI__pythia-1.4b_s1_historical_v3.json — 1398 bytes; SHA256 4efe0f0c058c9040a18ca3167db437993dca9017813afb23d9f5876cefc3928b
- out/phase8_items_EleutherAI__pythia-1.4b_s2_historical_v3.json — 1399 bytes; SHA256 45862cbd8f4e797ebbf94de32a9de92beca3ecc9c97c759af817f734c7b20fe9
- out/phase8_items_EleutherAI__pythia-410m_s0_historical_v3.json — 1399 bytes; SHA256 3577e9485a9bf359070d6680a7bd76c52c2e6be9a781ee857028dbd6c127c70a
- out/phase8_items_EleutherAI__pythia-410m_s1_historical_v3.json — 1399 bytes; SHA256 adb8d77061f7119f3d75d7f730ea686115ecff7a6ee4223e6d97cb6e4ef18676
- out/phase8_items_EleutherAI__pythia-410m_s2_historical_v3.json — 1398 bytes; SHA256 403881db42588f9239a37223326f7642997dc36464c2c3d701262a523d32c768
- out/phase8_items_gpt2-medium_s0_historical_v3.json — 1364 bytes; SHA256 adf42ffa368c42a3030b340df54568b75396c455c050b5f490acc294f5c88420
- out/phase8_items_gpt2-medium_s1_historical_v3.json — 1364 bytes; SHA256 4ef023437232c6003c359a709eac56aca551ae9dc468c706b1e3472731df51d8
- out/phase8_items_gpt2-medium_s2_historical_v3.json — 1364 bytes; SHA256 ead7435b6a5b2bc332baf6eee8bec93b99dfb92657f86aa7e3f64a544a46e4a1
- out/phase8_items_gpt2_s0_historical_v3.json — 1342 bytes; SHA256 cd58bcbdcf298efe1472ad09afce1dc1b5c35ddeb6f6214a5c663d9681937d53
- out/phase8_items_gpt2_s1_historical_v3.json — 1343 bytes; SHA256 ae933f8446e25d4b98947efcb59232497742466286aca1d963e58b5c0b66c029
- out/phase8_items_gpt2_s2_historical_v3.json — 1342 bytes; SHA256 f804c26dc57c9056a43687715404ac63ee09f9e0fe95ef4ab8de3a9283c7053d
- out/phase8_items_Qwen__Qwen2.5-0.5B_s0_historical_v3.json — 1384 bytes; SHA256 2f59d1c45d251ceb64fc30cb531acee557b140cca19ff9e63748198992d8c35b
- out/phase8_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_v3.json — 1390 bytes; SHA256 c9623a25f0cc9e62f0bce0db00edfd4b6a7c9c52ad14f1cfc08866c436dd788a
- out/phase8_items_Qwen__Qwen2.5-0.5B_s1_historical_v3.json — 1383 bytes; SHA256 4144de5b58c27bff8715a8ed9389ae2e4f723d24c99ab0a06e43dfdfc9f31053
- out/phase8_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_v3.json — 1390 bytes; SHA256 93340a3536e70ba95537f3f7569917a6e41324bfbe8cca05d172e6b7cc0d5493
- out/phase8_items_Qwen__Qwen2.5-0.5B_s2_historical_v3.json — 1383 bytes; SHA256 5d7cd57b2cc7268a7133fcce10353871445147bc97137e04d3ae51c08a73a134
- out/phase8_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_v3.json — 1390 bytes; SHA256 b98e2eaa6711f898837239326656799aa2b9d1e97d654e49f5ece98a702a97d2
- out/phase8_items_v3.json — 2755244 bytes; SHA256 2a31aabf4cf460423e1cebf36dad9ad0e825ff93e9fa90660266e1b64cd268a8
- out/revision_v3_cv_reproduction_protocol.json — 1908 bytes; SHA256 23d4a2e0829fde8cd53783257dd785eb7f3d32a65b90c43fce3dba1c555e37ab
- out/revision_v3_precision_family.json — 1036 bytes; SHA256 75db2f468b6e6b056e94b20f749061f3757f5766ba3eff9d1091cea16528c104
- out/revision_v3_protocol.json — 2185 bytes; SHA256 a1e06bd9f6269f7c38d66bbd3a3754c8a0737d36333e43e49490aee0de76aaa3
- out/revision_v3_statistics_checks.json — 267 bytes; SHA256 66189f81b1e01cb16705f14adc2d75e1762d0a3355113ec689451d537ed9479b
- out/revision_v3_timings.json — 299251 bytes; SHA256 0ea1cfb3b3019d0755d950b92b388eb8a186990c7ca475e8e70160ade3987969
- phase36_constancy_named_ci.py — 9060 bytes; SHA256 24e6bd7e36552aa85896db4ee878d2c8f0e9e69479b8f01a258dad7048c649b6
- phase37_mass_matched.py — 23144 bytes; SHA256 d4e0f302bc3dc0d21a446cf1eb581f679375972ede67a606555c084b1920dee5
- phase38_paired_items.py — 9448 bytes; SHA256 230f69b506619717ccf26cfffe6980b3dc24c62372d48f9a902f2323688bbb6c
- phase39_betacv_items.py — 14308 bytes; SHA256 adce1774c56e15e7d776a3f7182a9ba9ccfef8e0184df55a29d9456f242f57f4
- phase40_v3_checks.py — 14641 bytes; SHA256 8a5cc2df2fff631e241cd1bda1f6d870739c2e6f8940cae69110a9799745c833
- phase41_v3_run.py — 9058 bytes; SHA256 f85a4acdfdabd4b4cb8a4b58c70d00e50de7b10effd14407048280276c9a146f
- phase43_cv_batch_diagnostic.py — 3462 bytes; SHA256 094560242dbea6bdbf041df55530c1f72e0c02635ad3c097984f56015b0f6c5e
- phase45_currentcv_items.py — 18371 bytes; SHA256 8f61cd2e7623412175284ebbc8f1e0242ac3a4fe786c9f10c42163b73a2ccf7f
- phase46_currentcv_run.py — 3980 bytes; SHA256 095f3a44726ceb643686ea5f5275cc2962b754b82ac305cfacfcb8e44139d673
- revision_v3_probes.py — 13132 bytes; SHA256 8aab9a6b020a70af460a6d5170a14d706d3f991a844d77b1117448df814f2ec5
- revision_v3_report.py — 14204 bytes; SHA256 c096402046a85221a844a061b5eb93d51c85001f18b65e6da969fcd0e203188b
- revision_v3_stats.py — 10312 bytes; SHA256 fa53651d82018d93faaffa755d00c2d8b05a1166f6ef63cb5c3dfcc04e19f979

Relatorio gerado em 0.056593s; nenhuma inferencia ou estatistica recalculada.


COMPLEMENTO OPERACIONAL E DECISOES V3

Nota: a mensagem curta do auditor ainda diz "six required outputs"; o campo required_outputs do JSON contem sete arquivos, incluindo phase8_beta0_statistics_v3.json, e todos foram verificados. A reproducao historica de B e um resultado explicitamente falho para quatro modelos, separado das sanidades numericas.

Comandos CPU e diagnosticos (tempos internos da funcao, excluindo importacoes; paredes dos agregadores entre parenteses):

- `.venv/Scripts/python.exe -B phase36_constancy_named_ci.py --part constancy`: 119.754018 s.
- `.venv/Scripts/python.exe -B phase36_constancy_named_ci.py --part named`: 104.776482 s.
- `.venv/Scripts/python.exe -B phase38_paired_items.py --prepare-only`: 38.167562 s.
- `.venv/Scripts/python.exe -B phase37_mass_matched.py --cpu-checks`: 0.024967 s, 20 casos.
- Verificacao CPU inline de phase45_currentcv_items.verified_attention_forward: 6.738820 s incluindo importacoes; 54 casos, seed0, FP32/BF16, q/k=8/8,1/9,3/9, grade completa; comando preservado no historico da ferramenta, resultados em phase45_positive_equality_checks_v3.json.
- `.venv/Scripts/python.exe -B beta0_statistics_v3.py`: 1.229136 s.
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase39_betacv_items.py --model gpt2 --seed 0 --variant historical --beta 1.0`: 28.627106 s; tentativa inicial preservada como diagnostico de reproducao, fora dos 300 jobs principais.
- `flock /tmp/radon-gpu.lock .venv/Scripts/python.exe -B phase43_cv_batch_diagnostic.py`: 28.496136 s; diagnostico adicional, fora dos 300 jobs principais.
- `.venv/Scripts/python.exe -B phase37_mass_matched.py --aggregate-only`: 3.583788 s (parede 9.619 s).
- `.venv/Scripts/python.exe -B phase38_paired_items.py --aggregate-only`: 7.562730 s (parede 13.722 s).
- `.venv/Scripts/python.exe -B phase45_currentcv_items.py --aggregate-only`: 7.678557 s (parede 12.909 s).
- `.venv/Scripts/python.exe -B phase40_v3_checks.py`: 50.021679 s (parede 52.785 s).
- `.venv/Scripts/python.exe -B revision_v3_report.py --timings`: 0.052 s; --check-render aprovado sem publicar; --append-report: 0.056593 s.
- Coordenador `python3 -B phase41_v3_run.py --kinds mass items`: parede 50350.644 s, incluindo filas; `python3 -B phase46_currentcv_run.py`: parede 55076.152 s, incluindo espera pelo diagnostico e filas. Esses dois tempos se sobrepoem.

Perguntas/decisoes, sugestao, certeza e execucao:

| Pergunta | Sugestao/decisao | Certeza | Executou |
| --- | --- | --- | --- |
| Como manter massa igual apos feedback? | q comum viavel nas duas trajetorias; ordem aleatoria fixa por artigo/camada; mesma normalizacao; beta nominal e caps registrados. | alta | sim |
| Como tratar energia zero na constancia? | indefinida, excluir e contar; comparacao pareada em cabecas definidas em ambos os lados. | alta | sim |
| Qual precisao para Qwen0.5? | reproduzir fp32 historico e reportar bf16 padrao separadamente; Holm7 principal, Holm8 de precisao secundario. | alta para medir ambos | sim; escolha da versao para o texto fica com o autor |
| Restaurar limites dos lotes na CV? | resetar batch8 a cada posicao como nos avaliadores originais; o diagnostico mostrou zero predicoes diferentes. | alta | sim, novo executor/namespace; primeira tentativa preservada |
| A mudanca salva/atual em B pode ser atribuida ao bug? | usar contrafactual legado/corrigido nos mesmos itens atuais; os itens/hashes antigos faltam para quatro modelos. | alta quanto a limitacao; media quanto a causa historica | contrafactual executado; causa nao assumida nem gerador ajustado para casar numeros |
| A frase sobre beta0 sobrevive? | relatar colapso de acuracia do GPT2-medium nesta sonda; os dados corrigidos tem atencao valida. | alta nos dados; media na redacao | dados/ICs executados; texto nao alterado |

Arquivos operacionais adicionais (fora do inventario cientifico de 761 artefatos), um por linha:

- out/revision_v3_delivery.json — auditoria final e inventario.
- out/_rerun_logs/v3_progress.md — diario e relatorio completo, arquivo mutavel por append.
- out/_rerun_logs/beta0_statistics_v3.log — log operacional, 30 bytes.
- out/_rerun_logs/phase11_items_Qwen__Qwen2.5-3B_s0_historical_v3.log — log operacional, 291 bytes.
- out/_rerun_logs/phase11_items_Qwen__Qwen2.5-3B_s1_historical_v3.log — log operacional, 291 bytes.
- out/_rerun_logs/phase11_items_Qwen__Qwen2.5-3B_s2_historical_v3.log — log operacional, 292 bytes.
- out/_rerun_logs/phase11_items_gpt2-medium_s0_historical_v3.log — log operacional, 283 bytes.
- out/_rerun_logs/phase11_items_gpt2-medium_s1_historical_v3.log — log operacional, 283 bytes.
- out/_rerun_logs/phase11_items_gpt2-medium_s2_historical_v3.log — log operacional, 282 bytes.
- out/_rerun_logs/phase15_constancy_v3.log — log operacional, 723 bytes.
- out/_rerun_logs/phase18_batch_diagnostic_v3.log — log operacional, 891 bytes.
- out/_rerun_logs/phase18_items_gpt2_s0_b1.0_historical_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.05_v3.log — log operacional, 595 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.0_v3.log — log operacional, 526 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.15_v3.log — log operacional, 596 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.1_v3.log — log operacional, 594 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.25_v3.log — log operacional, 528 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.35_v3.log — log operacional, 664 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.5_v3.log — log operacional, 526 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b0.75_v3.log — log operacional, 596 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_b1.0_v3.log — log operacional, 594 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s0_historical_blegacy_beta0_v3.log — log operacional, 544 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.05_v3.log — log operacional, 528 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.0_v3.log — log operacional, 526 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.15_v3.log — log operacional, 596 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.1_v3.log — log operacional, 526 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.25_v3.log — log operacional, 663 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.35_v3.log — log operacional, 731 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.5_v3.log — log operacional, 594 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b0.75_v3.log — log operacional, 528 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_b1.0_v3.log — log operacional, 933 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s1_historical_blegacy_beta0_v3.log — log operacional, 544 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.05_v3.log — log operacional, 596 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.0_v3.log — log operacional, 526 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.15_v3.log — log operacional, 528 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.1_v3.log — log operacional, 526 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.25_v3.log — log operacional, 732 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.35_v3.log — log operacional, 866 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.5_v3.log — log operacional, 594 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b0.75_v3.log — log operacional, 528 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_b1.0_v3.log — log operacional, 594 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-1.4b_s2_historical_blegacy_beta0_v3.log — log operacional, 544 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.05_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.0_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.15_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.1_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.25_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.35_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.5_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b0.75_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_b1.0_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s0_historical_blegacy_beta0_v3.log — log operacional, 343 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.05_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.0_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.15_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.1_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.25_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.35_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.5_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b0.75_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_b1.0_v3.log — log operacional, 394 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s1_historical_blegacy_beta0_v3.log — log operacional, 343 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.05_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.0_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.15_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.1_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.25_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.35_v3.log — log operacional, 458 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.5_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b0.75_v3.log — log operacional, 327 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_b1.0_v3.log — log operacional, 325 bytes.
- out/_rerun_logs/phase18_posbatch_items_EleutherAI__pythia-410m_s2_historical_blegacy_beta0_v3.log — log operacional, 343 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.05_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.0_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.15_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.1_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.25_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.35_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.5_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b0.75_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_b1.0_v3.log — log operacional, 310 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_historical_blegacy_beta0_v3.log — log operacional, 333 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.05_v3.log — log operacional, 255 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.0_v3.log — log operacional, 252 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.15_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.1_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.25_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.35_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.5_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b0.75_v3.log — log operacional, 255 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_b1.0_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_blegacy_beta0_v3.log — log operacional, 271 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.05_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.0_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.15_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.1_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.25_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.35_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.5_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b0.75_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_b1.0_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_historical_blegacy_beta0_v3.log — log operacional, 333 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.05_v3.log — log operacional, 255 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.0_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.15_v3.log — log operacional, 255 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.1_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.25_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.35_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.5_v3.log — log operacional, 252 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b0.75_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_b1.0_v3.log — log operacional, 252 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_blegacy_beta0_v3.log — log operacional, 271 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.05_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.0_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.15_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.1_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.25_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.35_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.5_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b0.75_v3.log — log operacional, 317 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_b1.0_v3.log — log operacional, 315 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_historical_blegacy_beta0_v3.log — log operacional, 333 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.05_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.0_v3.log — log operacional, 252 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.15_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.1_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.25_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.35_v3.log — log operacional, 254 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.5_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b0.75_v3.log — log operacional, 255 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_b1.0_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_blegacy_beta0_v3.log — log operacional, 270 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.05_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.0_v3.log — log operacional, 234 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.15_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.1_v3.log — log operacional, 235 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.25_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.35_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.5_v3.log — log operacional, 235 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b0.75_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_b1.0_v3.log — log operacional, 235 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s0_historical_blegacy_beta0_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.05_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.0_v3.log — log operacional, 235 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.15_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.1_v3.log — log operacional, 234 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.25_v3.log — log operacional, 237 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.35_v3.log — log operacional, 237 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.5_v3.log — log operacional, 235 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b0.75_v3.log — log operacional, 237 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_b1.0_v3.log — log operacional, 234 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s1_historical_blegacy_beta0_v3.log — log operacional, 253 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.05_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.0_v3.log — log operacional, 234 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.15_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.1_v3.log — log operacional, 234 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.25_v3.log — log operacional, 236 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.35_v3.log — log operacional, 237 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.5_v3.log — log operacional, 235 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b0.75_v3.log — log operacional, 237 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_b1.0_v3.log — log operacional, 235 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2-medium_s2_historical_blegacy_beta0_v3.log — log operacional, 252 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b0.05_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b0.0_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b0.15_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b0.1_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b0.25_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b0.35_v3.log — log operacional, 222 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b0.5_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b0.75_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_b1.0_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s0_historical_blegacy_beta0_v3.log — log operacional, 239 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b0.05_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b0.0_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b0.15_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b0.1_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b0.25_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b0.35_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b0.5_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b0.75_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_b1.0_v3.log — log operacional, 220 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s1_historical_blegacy_beta0_v3.log — log operacional, 238 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b0.05_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b0.0_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b0.15_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b0.1_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b0.25_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b0.35_v3.log — log operacional, 223 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b0.5_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b0.75_v3.log — log operacional, 222 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_b1.0_v3.log — log operacional, 221 bytes.
- out/_rerun_logs/phase18_posbatch_items_gpt2_s2_historical_blegacy_beta0_v3.log — log operacional, 239 bytes.
- out/_rerun_logs/phase26_named_v3_ci.log — log operacional, 460 bytes.
- out/_rerun_logs/phase45_cpu_equality_checks_v3.log — log operacional, 29 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d000_016_v3.log — log operacional, 1817 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d016_032_v3.log — log operacional, 1483 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d032_048_v3.log — log operacional, 1347 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d048_064_v3.log — log operacional, 1483 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d064_080_v3.log — log operacional, 1878 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d080_096_v3.log — log operacional, 1946 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d096_112_v3.log — log operacional, 1496 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d112_128_v3.log — log operacional, 1702 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d128_144_v3.log — log operacional, 1702 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d144_160_v3.log — log operacional, 1432 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d160_176_v3.log — log operacional, 1363 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d176_192_v3.log — log operacional, 1499 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d192_208_v3.log — log operacional, 1431 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d208_224_v3.log — log operacional, 1895 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d224_240_v3.log — log operacional, 1364 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-1.4b_d240_256_v3.log — log operacional, 1363 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d000_016_v3.log — log operacional, 1208 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d016_032_v3.log — log operacional, 1147 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d032_048_v3.log — log operacional, 1145 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d048_064_v3.log — log operacional, 1144 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d064_080_v3.log — log operacional, 1145 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d080_096_v3.log — log operacional, 1144 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d096_112_v3.log — log operacional, 1157 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d112_128_v3.log — log operacional, 1163 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d128_144_v3.log — log operacional, 1161 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d144_160_v3.log — log operacional, 1161 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d160_176_v3.log — log operacional, 1163 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d176_192_v3.log — log operacional, 1162 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d192_208_v3.log — log operacional, 1162 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d208_224_v3.log — log operacional, 1161 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d224_240_v3.log — log operacional, 1162 bytes.
- out/_rerun_logs/phase7_massmatched_EleutherAI__pythia-410m_d240_256_v3.log — log operacional, 1162 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d000_016_v3.log — log operacional, 993 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d016_032_v3.log — log operacional, 995 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d032_048_v3.log — log operacional, 994 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d048_064_v3.log — log operacional, 994 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d064_080_v3.log — log operacional, 994 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d080_096_v3.log — log operacional, 994 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d096_112_v3.log — log operacional, 1006 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d112_128_v3.log — log operacional, 1010 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d128_144_v3.log — log operacional, 1010 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d144_160_v3.log — log operacional, 1011 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d160_176_v3.log — log operacional, 1011 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d176_192_v3.log — log operacional, 1010 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d192_208_v3.log — log operacional, 1010 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d208_224_v3.log — log operacional, 1010 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d224_240_v3.log — log operacional, 1009 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-0.5B_d240_256_v3.log — log operacional, 1010 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d000_016_v3.log — log operacional, 967 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d016_032_v3.log — log operacional, 969 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d032_048_v3.log — log operacional, 969 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d048_064_v3.log — log operacional, 969 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d064_080_v3.log — log operacional, 968 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d080_096_v3.log — log operacional, 968 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d096_112_v3.log — log operacional, 981 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d112_128_v3.log — log operacional, 985 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d128_144_v3.log — log operacional, 985 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d144_160_v3.log — log operacional, 986 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d160_176_v3.log — log operacional, 985 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d176_192_v3.log — log operacional, 984 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d192_208_v3.log — log operacional, 984 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d208_224_v3.log — log operacional, 986 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d224_240_v3.log — log operacional, 984 bytes.
- out/_rerun_logs/phase7_massmatched_Qwen__Qwen2.5-3B_d240_256_v3.log — log operacional, 984 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d000_016_v3.log — log operacional, 897 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d016_032_v3.log — log operacional, 902 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d032_048_v3.log — log operacional, 900 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d048_064_v3.log — log operacional, 899 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d064_080_v3.log — log operacional, 900 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d080_096_v3.log — log operacional, 900 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d096_112_v3.log — log operacional, 913 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d112_128_v3.log — log operacional, 916 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d128_144_v3.log — log operacional, 917 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d144_160_v3.log — log operacional, 917 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d160_176_v3.log — log operacional, 916 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d176_192_v3.log — log operacional, 915 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d192_208_v3.log — log operacional, 915 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d208_224_v3.log — log operacional, 915 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d224_240_v3.log — log operacional, 917 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2-medium_d240_256_v3.log — log operacional, 916 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d000_016_v3.log — log operacional, 776 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d016_032_v3.log — log operacional, 782 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d032_048_v3.log — log operacional, 783 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d048_064_v3.log — log operacional, 783 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d064_080_v3.log — log operacional, 783 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d080_096_v3.log — log operacional, 783 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d096_112_v3.log — log operacional, 795 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d112_128_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d128_144_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d144_160_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d160_176_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d176_192_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d192_208_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d208_224_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d224_240_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase7_massmatched_gpt2_d240_256_v3.log — log operacional, 799 bytes.
- out/_rerun_logs/phase8_items_EleutherAI__pythia-1.4b_s0_historical_v3.log — log operacional, 573 bytes.
- out/_rerun_logs/phase8_items_EleutherAI__pythia-1.4b_s1_historical_v3.log — log operacional, 573 bytes.
- out/_rerun_logs/phase8_items_EleutherAI__pythia-1.4b_s2_historical_v3.log — log operacional, 573 bytes.
- out/_rerun_logs/phase8_items_EleutherAI__pythia-410m_s0_historical_v3.log — log operacional, 371 bytes.
- out/_rerun_logs/phase8_items_EleutherAI__pythia-410m_s1_historical_v3.log — log operacional, 371 bytes.
- out/_rerun_logs/phase8_items_EleutherAI__pythia-410m_s2_historical_v3.log — log operacional, 371 bytes.
- out/_rerun_logs/phase8_items_Qwen__Qwen2.5-0.5B_s0_historical_v3.log — log operacional, 426 bytes.
- out/_rerun_logs/phase8_items_Qwen__Qwen2.5-0.5B_s0_standard_bf16_v3.log — log operacional, 298 bytes.
- out/_rerun_logs/phase8_items_Qwen__Qwen2.5-0.5B_s1_historical_v3.log — log operacional, 361 bytes.
- out/_rerun_logs/phase8_items_Qwen__Qwen2.5-0.5B_s1_standard_bf16_v3.log — log operacional, 297 bytes.
- out/_rerun_logs/phase8_items_Qwen__Qwen2.5-0.5B_s2_historical_v3.log — log operacional, 361 bytes.
- out/_rerun_logs/phase8_items_Qwen__Qwen2.5-0.5B_s2_standard_bf16_v3.log — log operacional, 298 bytes.
- out/_rerun_logs/phase8_items_gpt2-medium_s0_historical_v3.log — log operacional, 281 bytes.
- out/_rerun_logs/phase8_items_gpt2-medium_s1_historical_v3.log — log operacional, 280 bytes.
- out/_rerun_logs/phase8_items_gpt2-medium_s2_historical_v3.log — log operacional, 280 bytes.
- out/_rerun_logs/phase8_items_gpt2_s0_historical_v3.log — log operacional, 266 bytes.
- out/_rerun_logs/phase8_items_gpt2_s1_historical_v3.log — log operacional, 265 bytes.
- out/_rerun_logs/phase8_items_gpt2_s2_historical_v3.log — log operacional, 266 bytes.
- out/_rerun_logs/v3_coordinator.log — log operacional, 1044 bytes.
- out/_rerun_logs/v3_coordinator_currentcv.log — log operacional, 0 bytes.
- out/_rerun_logs/v3_coordinator_noncv.log — log operacional, 0 bytes.
- out/_rerun_logs/v3_cpu_aggregation.log — log operacional, 79445 bytes.
- out/_rerun_logs/v3_delivery_audit.log — log operacional, 0 bytes.
- out/_rerun_logs/v3_probe_preparation.log — log operacional, 1244 bytes.
