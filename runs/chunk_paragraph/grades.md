# Grades: runs/chunk_paragraph

Score = points / (2 x questions); 0 wrong, 1 correct but incomplete, 2 correct and complete (evaluation/grading_rubric.md).

| Group | Score |
|---|---|
| all | 60.0% (n=35) |
| text-involving | 53.6% (n=28) |
| source: text-only | 50.0% (n=21) |
| source: table-only | 85.7% (n=7) |
| source: text+table | 64.3% (n=7) |
| type: conceptual | 50.0% (n=6) |
| type: cross-paper | 38.9% (n=9) |
| type: cross-source | 64.3% (n=7) |
| type: factual | 75.0% (n=4) |
| type: insufficient-evidence | 50.0% (n=2) |
| type: tabular | 85.7% (n=7) |

Distribution: 2 x 9, 1 x 24, 0 x 2.
Failure modes (score below 2): partial_retrieval 13, generation_error 6, retrieval_miss 5, sql_error 2

| ID | Source | Score | Failure mode | Missing / wrong / citation issues |
|---|---|---|---|---|
| Q01 | text-only | 2 | none |  |
| Q02 | text-only | 2 | none |  |
| Q03 | text-only | 1 | generation_error | M = 4 target blocks; target scale range (0.15, 0.2); target aspect-ratio range (0.75, 1.5) |
| Q04 | text-only | 1 | partial_retrieval | six articles per day (three random, three hot topics); two TF and two MC pairs per article with few-shot prompting; the four construction steps (summary, QA generation, misleading choices, filtering); |
| Q06 | text-only | 1 | partial_retrieval | third desideratum (path length between long-range dependencies); complexity and path-length comparison from Table 1; cheaper than recurrent when n < d |
| Q07 | text-only | 1 | partial_retrieval | target network can be removed without collapse if the predictor is kept near-optimal (e.g., higher predictor learning rate); dynamics admit undesirable equilibria not observed in experiments |
| Q08 | text-only | 1 | retrieval_miss | MNIST sigmoid-input stability and higher test accuracy; BN-Baseline / BN-x5 / BN-x30 / sigmoid results; the seven additional changes; the conjecture / further-study caveat |
| Q09 | text-only | 1 | partial_retrieval | linear-dynamics theory: epsilon-straight transitions bound the planning-Hessian condition number, giving linear GD convergence; loss landscape closer to convex after straightening |
| Q11 | text-only | 1 | partial_retrieval | [class] token; Position information: learned 1D vs sinusoidal contrast; Normalisation placement (pre-LN vs post-LN); Feed-forward activation (GELU vs ReLU); Residual connections and LayerNorm kept |
| Q12 | text-only | 1 | partial_retrieval | MAE's lightweight decoder predicting masked-patch pixels with MSE loss on masked patches; I-JEPA loss is average L2 distance; Table 7 figures 66.9 vs 40.7 (ViT-L/16); Target encoder is an EMA of the c |
| Q13 | text-only | 1 | partial_retrieval | Distillation targets are temperature-softened class probabilities; Distilled model may also be trained on correct labels via a weighted average objective; Cumbersome model can be a single large regula |
| Q14 | text-only | 0 | retrieval_miss | ViT used as the dynamics predictor with temporal causal mask; Stop-gradient on the target latent for collapse prevention, citing BYOL; ResNet trained from scratch as one of two encoder setups; ResNet  |
| Q15 | text-only | 1 | partial_retrieval | BYOL default probabilities: blur 1.0/0.1, solarization 0.0/0.2 (Table 6); Conclusion that BabyCL's and BYOL's blur/solarization probabilities match; BabyCL cites Zhuang et al. (2021): contrastive meth |
| Q16 | text-only | 0 | retrieval_miss | Daily Oracle uses BM25; BM25 comes close to perfect scores on LIMIT while dense models struggle; Attributed to sparse models' high dimensionality |
| Q17 | text-only | 1 | retrieval_miss | Daily Oracle Fleiss' kappa 0.26 (fair); Daily Oracle 89.52% accuracy across seven principles; Daily Oracle 85.00% accuracy on final accept/reject; FIRE-Bench human validation on 33% subset; FIRE-Bench |
| Q18 | text-only | 1 | partial_retrieval | Paper's explicit statement that distilling the specialists back into a single net has not yet been shown |
| Q20 | text-only | 1 | partial_retrieval | Agent-based approaches appear only as a future direction the authors encourage; no agent results reported; Evaluated systems are single-pass LMs given BM25/oracle files (e.g. Claude 2 4.8% with oracle |
| Q21 | table-only | 2 | none |  |
| Q23 | table-only | 2 | none |  |
| Q24 | table-only | 2 | none |  |
| Q25 | table-only | 1 | sql_error | Spurious extra 50->101 row (0.764 gain / 3.48 GMACs = 0.2195); Spurious extra 34->50 row (4.310 gain / 0.68 GMACs = 6.338) |
| Q27 | table-only | 2 | none |  |
| Q29 | table-only | 1 | sql_error | Identity of the best rows (mobilenetv4_conv_medium...384, tiny_vit_21m_512, eva02_large_patch14_448); Parameter counts / ~31x fewer parameters for the under-10M model vs the overall best; Says the lar |
| Q30 | table-only | 2 | none |  |
| Q31 | text+table | 2 | none |  |
| Q32 | text+table | 1 | generation_error | Paper FLOPs and comparisons for ResNet-18, -34 and -101 (Table 1 on retrieved p.5 was missed); Alternative reading that paper FLOPs = 2x MACs (the paper defines FLOPs as multiply-adds), with confused  |
| Q34 | text+table | 1 | partial_retrieval | MAE masks random patches (75% default); Encoder processes only visible patches |
| Q35 | text+table | 1 | generation_error | Pairs vit_base_patch16_384 (+4.908), vit_base_patch32_224 (+5.824), vit_base_patch32_384 (+4.608), vit_small_patch16_384 (+2.684); Overall range 2.56-5.82 and Base 4.6-5.8 vs Small 2.6-2.7 |
| Q37 | text+table | 1 | generation_error | Accuracy differences depend on which rows/recipes are compared (e.g. ImageNet-1k-only ViT is below the a1h ResNets); recipe/pre-training-data confound not stated |
| Q39 | text+table | 2 | none |  |
| Q40 | text+table | 1 | generation_error | Says timm GMACs correspond to roughly half the paper's FLOPs; the paper's FLOPs are multiply-adds and the values nearly coincide (11.56 vs 11.3) |
| Q42 | text-only | 1 | generation_error | Says the paper credits pretraining data and fine-tuning with 'comparable or greater influence' than parameter count; the paper says size is a key component and only suggests data helps |
| Q43 | text-only | 1 | partial_retrieval | MMLU check (entropy/log-probability vs accuracy, r = -0.43 / -0.56), finding (exact questions not memorized) and hedge (Wikipedia-related exposure); SWE-bench before/after-2023 resolve-rate comparison |
| Q44 | text-only | 1 | partial_retrieval | Three BM25 context limits (13k/27k/50k); BM25 recall figures rising with context limit; Claude 2 resolve rates 1.96/1.87/1.22; Claude 2 resolves 4.8% with oracle retrieval; Oracle-collapsed results (G |
| Q45 | text-only | 1 | retrieval_miss | BatchNorm half: statistics during training are mini-batch estimates of each activation's mean and variance; BYOL footnote: only batch-size dependency sits within the BN layers |
