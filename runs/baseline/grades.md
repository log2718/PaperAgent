# Grades: runs/baseline

Score = points / (2 x questions); 0 wrong, 1 correct but incomplete, 2 correct and complete (evaluation/grading_rubric.md).

| Group | Score |
|---|---|
| all | 67.1% (n=35) |
| text-involving | 62.5% (n=28) |
| source: text-only | 57.1% (n=21) |
| source: table-only | 85.7% (n=7) |
| source: text+table | 78.6% (n=7) |
| type: conceptual | 50.0% (n=6) |
| type: cross-paper | 44.4% (n=9) |
| type: cross-source | 78.6% (n=7) |
| type: factual | 75.0% (n=4) |
| type: insufficient-evidence | 100.0% (n=2) |
| type: tabular | 85.7% (n=7) |

Distribution: 2 x 14, 1 x 19, 0 x 2.
Failure modes (score below 2): partial_retrieval 8, retrieval_miss 6, generation_error 5, sql_error 2

| ID | Source | Score | Failure mode | Missing / wrong / citation issues |
|---|---|---|---|---|
| Q01 | text-only | 2 | none |  |
| Q02 | text-only | 1 | generation_error | Table 1 offline CVCL value 57.31 +/- 1.13 (only the Section 4.2 text figure 57.45 is given, placed in the 'Table 1' table without saying it is the text figure) |
| Q03 | text-only | 2 | none |  |
| Q04 | text-only | 1 | partial_retrieval | article summary step; six articles per day (three random, three hot topics); two TF and two MC pairs per article; Says GPT-3.5/GPT-4o-mini are used for question generation and GPT-4/GPT-4o for mislead |
| Q06 | text-only | 1 | retrieval_miss | self-attention O(n^2 d), O(1), O(1) vs recurrent O(n d^2), O(n), O(n) comparison; cheaper than recurrent when n < d; restricted attention to neighbourhood r; Names the three desiderata and self-attent |
| Q07 | text-only | 1 | generation_error | Explains the conditional-variance argument as 'adding stochastic variability tends to reduce this conditional variance', misstating the paper's point that discarding information cannot lower the condi |
| Q08 | text-only | 1 | partial_retrieval | BN-Baseline vs Inception steps and BN-x5 2.1M steps; BN-x30 74.8%; BN-x5-Sigmoid 69.8% vs 1/1000; remaining changes: faster LR decay, LRN removed, more shuffling, fewer photometric distortions; Sec. 4 |
| Q09 | text-only | 1 | partial_retrieval | linear-dynamics theory: epsilon-straight transitions bound the planning-Hessian condition number, giving linear GD convergence; loss landscape closer to convex after straightening |
| Q11 | text-only | 1 | retrieval_miss | [class] token; Transformer uses sinusoidal position encodings (contrast); Normalisation placement: post-LN vs pre-LN; Feed-forward activation: ReLU vs GELU; Explicit kept components (alternating MSA/M |
| Q12 | text-only | 1 | partial_retrieval | MAE predicts pixel values of masked patches with a lightweight decoder; MAE loss is MSE on masked patches; I-JEPA loss is average L2 distance; EMA target encoder; Table 7 figures 66.9 vs 40.7 |
| Q13 | text-only | 1 | retrieval_miss | Distillation targets: soft class probabilities from an already-trained cumbersome model at high temperature; Distillation label use (weighted average with hard-label cross-entropy) |
| Q14 | text-only | 1 | retrieval_miss | Stop-gradient purpose (collapse prevention), citation of Grill et al./BYOL, no negatives or extra hyper-parameters; ResNet paper: residual learning to ease training of deeper nets; ViT paper: patch em |
| Q15 | text-only | 1 | partial_retrieval | BYOL blur 1.0/0.1 and solarization 0.0/0.2; Comparison: probabilities match; BYOL achieves state of the art without negative pairs; BabyCL cites Zhuang et al. (2021) on negative sampling being most ef |
| Q16 | text-only | 0 | retrieval_miss | Daily Oracle uses BM25; BM25 comes close to perfect scores on LIMIT while dense models struggle; Attributed to sparse models' high dimensionality |
| Q17 | text-only | 0 | retrieval_miss | Daily Oracle validation method (4 annotators, 30 TF + 30 MC, seven principles); Daily Oracle kappa 0.26, 89.52%, 85.00%; FIRE-Bench 33% human validation subset; FIRE-Bench precision 0.95, recall 0.86, |
| Q18 | text-only | 2 | none |  |
| Q20 | text-only | 2 | none |  |
| Q21 | table-only | 2 | none |  |
| Q23 | table-only | 2 | none |  |
| Q24 | table-only | 2 | none |  |
| Q25 | table-only | 1 | sql_error | Spurious extra 50->101 row (0.764 gain / 3.48 GMACs = 0.2195); Spurious extra 34->50 row (4.310 gain / 0.68 GMACs = 6.338) |
| Q27 | table-only | 2 | none |  |
| Q29 | table-only | 1 | sql_error | Identity of the best rows (mobilenetv4_conv_medium...384, tiny_vit_21m_512, eva02_large_patch14_448); Parameter counts / ~31x fewer parameters for the under-10M model vs the overall best; Says the lar |
| Q30 | table-only | 2 | none |  |
| Q31 | text+table | 1 | generation_error | Paper's own statement that smaller patches are more expensive / N=HW/P^2 not attributed to the paper (claims passages lack it although ViT p.5-6 was retrieved); Sequence-length formula and 'smaller pa |
| Q32 | text+table | 2 | none |  |
| Q34 | text+table | 1 | partial_retrieval | Encoder processes only visible patches; Masked units are random patches |
| Q35 | text+table | 1 | generation_error | Pairs vit_base_patch16_384 (+4.908), vit_base_patch32_224 (+5.824), vit_base_patch32_384 (+4.608), vit_small_patch16_384 (+2.684); Overall range 2.56-5.82 and Base 4.6-5.8 vs Small 2.6-2.7; Says the p |
| Q37 | text+table | 2 | none |  |
| Q39 | text+table | 2 | none |  |
| Q40 | text+table | 2 | none |  |
| Q42 | text-only | 1 | generation_error | Says the paper 'explicitly rejects' a parameter-count explanation and that pretraining data size 'matters more than raw parameters'; the paper calls size a key component and only suggests data helps |
| Q43 | text-only | 1 | partial_retrieval | MMLU check (entropy/log-probability vs accuracy, r = -0.43 / -0.56), finding and hedge; SWE-bench before/after-2023 resolve-rate comparison, little difference except GPT-4 (25% subset), 'largely promi |
| Q44 | text-only | 1 | partial_retrieval | Paper's explanation that performance drops despite higher recall because models are ineffective at localizing problematic code; Oracle-collapsed results (GPT-4 1.3%->3.4%, Claude 2 4.8%->5.9%) |
| Q45 | text-only | 2 | none |  |
