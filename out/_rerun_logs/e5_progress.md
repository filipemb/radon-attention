
- 2026-11-09T21:47:05+00:00 | E5 start: part_a=False part_b=True | command: `phase22_sink_evolution.py --part-b`

- 2026-11-09T21:47:05+00:00 | E5 sanity B: atten beta=1 vs orig: max_abs_diff=0 over 3 instances; pass=True

- 2026-11-09T22:31:03+00:00 | E5 start: part_a=True part_b=False | command: `phase22_sink_evolution.py --part-a`

- 2026-11-09T22:31:19+00:00 | E5 extract: step0: 1536 matrices from 64 documents; all checks passed | elapsed_seconds=15.987

- 2026-11-09T22:31:33+00:00 | E5 extract: step1000: 1536 matrices from 64 documents; all checks passed | elapsed_seconds=13.560

- 2026-11-09T22:31:42+00:00 | E5 ablate: Qwen/Qwen2.5-3B n=128: 2304 instances x 7 variants | elapsed_seconds=2599.705

- 2026-11-09T22:31:47+00:00 | E5 extract: step4000: 1536 matrices from 64 documents; all checks passed | elapsed_seconds=13.577

- 2026-11-09T22:32:00+00:00 | E5 extract: step16000: 1536 matrices from 64 documents; all checks passed | elapsed_seconds=13.875

- 2026-11-09T22:32:09+00:00 | E5 extract: step64000: 1536 matrices from 64 documents; all checks passed | elapsed_seconds=8.705

- 2026-11-09T22:32:17+00:00 | E5 extract: step143000: 1536 matrices from 64 documents; all checks passed | elapsed_seconds=8.196

- 2026-11-09T22:32:18+00:00 | E5 sanity A: step143000 vs data/attn archive: max_abs_diff=0 (tol=0.001); pass=True

- 2026-11-09T22:36:22+00:00 | E5 start: part_a=False part_b=True | command: `phase22_sink_evolution.py --part-b`

- 2026-11-09T22:36:23+00:00 | E5 sanity B: atten beta=1 vs orig: max_abs_diff=0 over 3 instances; pass=True

- 2026-11-09T22:47:47+00:00 | E5 part A complete: 6 revisions, random_median=0.150320 | elapsed_seconds=1004.372

- 2026-11-09T22:47:47+00:00 | E5 part A stored: wrote e5_part_a.json | elapsed_seconds=1004.446

- 2026-11-09T22:55:55+00:00 | E5 ablate: gpt2-medium n=128: 1536 instances x 7 variants | elapsed_seconds=1164.060

- 2026-11-09T22:55:57+00:00 | E5 ablate: gpt2 n=128: 1536 instances x 7 variants | elapsed_seconds=1165.892

- 2026-11-09T23:18:01+00:00 | E5 ablate: EleutherAI/pythia-410m n=128: 1536 instances x 7 variants | elapsed_seconds=1325.692

- 2026-11-09T23:18:01+00:00 | E5 ablate: EleutherAI/pythia-1.4b n=128: 1536 instances x 7 variants | elapsed_seconds=1324.175

- 2026-11-09T23:18:06+00:00 | E5 ablate: Qwen/Qwen2.5-3B n=128: resumed 2304 stored instances, no recompute

- 2026-11-09T23:18:10+00:00 | E5 ablate: Qwen/Qwen2.5-3B n=128: 2304 instances x 7 variants | elapsed_seconds=8.861

- 2026-11-09T23:35:52+00:00 | E5 ablate: Qwen/Qwen2.5-0.5B n=128: 1536 instances x 7 variants | elapsed_seconds=1071.544

- 2026-11-09T23:35:55+00:00 | E5 part B complete: 6 models | elapsed_seconds=3572.419

- 2026-11-09T23:35:55+00:00 | E5 part B stored: wrote e5_part_b.json | elapsed_seconds=3572.435

- 2026-11-09T23:36:12+00:00 | E5 merge: wrote out\phase22_sink_evolution.json from e5_part_a.json + e5_part_b.json

- 2026-11-09T23:59:06+00:00 | E5B2 start: command: `phase22_sink_evolution.py --part-b2`

- 2026-11-10T00:04:35+00:00 | E5B2 start: command: `phase22_sink_evolution.py --part-b2`

- 2026-11-10T00:21:28+00:00 | E5B2 ablate: gpt2 n=128: 1536 instances x 7 variants | elapsed_seconds=1005.156

- 2026-11-10T00:21:30+00:00 | E5B2 ablate: gpt2-medium n=128: 1536 instances x 7 variants | elapsed_seconds=1007.421

- 2026-11-10T00:40:52+00:00 | E5B2 ablate: EleutherAI/pythia-410m n=128: 1536 instances x 7 variants | elapsed_seconds=1163.275

- 2026-11-10T00:41:27+00:00 | E5B2 ablate: EleutherAI/pythia-1.4b n=128: 1536 instances x 7 variants | elapsed_seconds=1196.752

- 2026-11-10T01:10:23+00:00 | E5B2 ablate: Qwen/Qwen2.5-0.5B n=128: 1536 instances x 7 variants | elapsed_seconds=1770.770

- 2026-11-10T01:28:14+00:00 | E5B2 ablate: Qwen/Qwen2.5-3B n=128: 2304 instances x 7 variants | elapsed_seconds=2806.285

- 2026-11-10T01:28:18+00:00 | E5B2 part complete: 6 models | elapsed_seconds=5023.222

- 2026-11-10T01:28:18+00:00 | E5B2 done: wrote out\phase22_sink_equalized.json | elapsed_seconds=5023.250
