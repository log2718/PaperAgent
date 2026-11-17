# Grades: runs/baseline_repeat

Score = points / (2 x questions); 0 wrong, 1 correct but incomplete, 2 correct and complete (evaluation/grading_rubric.md).

| Group | Score |
|---|---|
| all | 68.6% (n=35) |
| text-involving | 62.5% (n=28) |
| source: text-only | 57.1% (n=21) |
| source: table-only | 92.9% (n=7) |
| source: text+table | 78.6% (n=7) |
| type: conceptual | 58.3% (n=6) |
| type: cross-paper | 44.4% (n=9) |
| type: cross-source | 78.6% (n=7) |
| type: factual | 75.0% (n=4) |
| type: insufficient-evidence | 75.0% (n=2) |
| type: tabular | 92.9% (n=7) |

Distribution: 2 x 15, 1 x 18, 0 x 2.
Failure modes (score below 2): partial_retrieval 7, retrieval_miss 7, generation_error 4, citation_error 1, sql_error 1

| ID | Source | Score | Failure mode | Missing / wrong / citation issues |
|---|---|---|---|---|
| Q01 | text-only | 2 | none |  |
| Q02 | text-only | 1 | generation_error | Table 1 offline CVCL mean 57.31 +/- 1.13; States the passages give no Table 1 final-mean value for offline CVCL, although Table 1 on the retrieved p.5 lists 57.31 +/- 1.13; Labels the Section 4.2 text |
| Q03 | text-only | 2 | none |  |
| Q04 | text-only | 1 | partial_retrieval | article summary step; six articles per day (three random, three hot topics); two TF and two MC pairs per article; Assigns GPT-3.5/GPT-4o-mini to its step (1), which it calls question generation; in th |
| Q06 | text-only | 1 | retrieval_miss | the three desiderata stated as established; Table 1 complexity/sequential/path-length comparison; cheaper than recurrent when n < d; Guesses the desiderata ('likely include ...') without a supporting  |
| Q07 | text-only | 1 | generation_error | Summary says 'either can substitute for the other', but the ablations show removing the predictor causes collapse; only the target network can be replaced (by a near-optimal predictor) |
| Q08 | text-only | 1 | partial_retrieval | BN-Baseline vs Inception steps (13.3M vs 31.0M) and BN-x5 2.1M steps; BN-x30 74.8%; BN-x5-Sigmoid 69.8% vs Inception-sigmoid 1/1000; remaining changes: faster LR decay, LRN removed, more shuffling, fe |
| Q09 | text-only | 1 | partial_retrieval | linear-dynamics theory: epsilon-straight transitions bound the planning-Hessian condition number, giving linear GD convergence; loss landscape closer to convex after straightening (Figure 4) |
| Q11 | text-only | 1 | retrieval_miss | [class] token prepended to patch sequence; Transformer uses fixed sinusoidal position encodings (contrast missing); Normalisation placement: Transformer post-LN vs ViT pre-LN; Feed-forward activation: |
| Q12 | text-only | 1 | partial_retrieval | MAE predicts pixel values of masked patches with a lightweight decoder; MAE loss is MSE on masked patches; I-JEPA loss is average L2 distance; EMA target encoder; Table 7 figures 66.9 vs 40.7 |
| Q13 | text-only | 1 | retrieval_miss | Distillation targets: soft class probabilities from an already-trained cumbersome model at high temperature; Distillation label use (weighted average with hard-label cross-entropy) |
| Q14 | text-only | 1 | retrieval_miss | Stop-gradient purpose (collapse prevention), citation of Grill et al./BYOL, no negatives or extra hyper-parameters; ResNet paper: residual learning to ease training of deeper nets; ViT paper: patch em |
| Q15 | text-only | 1 | partial_retrieval | BYOL blur 1.0/0.1 and solarization 0.0/0.2; Comparison: probabilities match; BYOL achieves state of the art without negative pairs; BabyCL cites Zhuang et al. (2021) on negative sampling being most ef |
| Q16 | text-only | 0 | retrieval_miss | Daily Oracle uses BM25 (top 5 articles, 512 words); BM25 comes close to perfect scores on LIMIT while dense models struggle (<20% recall@100); Attributed to sparse models' very high dimensionality |
| Q17 | text-only | 0 | retrieval_miss | Daily Oracle validation method and numbers (kappa 0.26, 89.52%, 85.00%); FIRE-Bench 33% subset, precision 0.95, recall 0.86, F1 0.89 |
| Q18 | text-only | 1 | citation_error | The 4.4% relative improvement is cited to [Distillation, p.5-6]; it appears on p.7 (in the retrieved p.7-8 passage) |
| Q20 | text-only | 2 | none |  |
| Q21 | table-only | 2 | none |  |
| Q23 | table-only | 2 | none |  |
| Q24 | table-only | 2 | none |  |
| Q25 | table-only | 1 | sql_error | Spurious extra 34->50 row (4.310 gain / 0.68 GMACs = 6.338); Spurious extra 50->101 row (0.764 gain / 3.48 GMACs = 0.220) |
| Q27 | table-only | 2 | none |  |
| Q29 | table-only | 2 | none |  |
| Q30 | table-only | 2 | none |  |
| Q31 | text+table | 1 | generation_error | Paper's statement that smaller patches are more expensive (retrieved ViT p.5-6 contains it) and the N=HW/P^2 definition from the paper; No citations at all; the paper half is not sourced |
| Q32 | text+table | 2 | none |  |
| Q34 | text+table | 1 | retrieval_miss | MAE pre-training task: mask random patches (75%) and reconstruct missing pixels with a visible-only encoder |
| Q35 | text+table | 1 | generation_error | Pairs vit_base_patch16_384 (+4.908), vit_base_patch32_224 (+5.824), vit_base_patch32_384 (+4.608), vit_small_patch16_384 (+2.684); Overall range 2.56-5.82 and Base 4.6-5.8 vs Small 2.6-2.7 |
| Q37 | text+table | 2 | none |  |
| Q39 | text+table | 2 | none |  |
| Q40 | text+table | 2 | none |  |
| Q42 | text-only | 2 | none |  |
| Q43 | text-only | 1 | partial_retrieval | MMLU check (entropy/log-probability vs accuracy, r = -0.43 / -0.56), finding (exact questions not memorized) and hedge (Wikipedia-related exposure); SWE-bench before/after-2023 resolve-rate comparison |
| Q44 | text-only | 1 | partial_retrieval | Paper's own explanation that models are ineffective at localizing problematic code (answer gives its own noise-based inference instead); Oracle-collapsed results (GPT-4 1.3%->3.4%, Claude 2 4.8%->5.9% |
| Q45 | text-only | 2 | none |  |
