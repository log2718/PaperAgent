# Grades: runs/chunk_paragraph_matched

Score = points / (2 x questions); 0 wrong, 1 correct but incomplete, 2 correct and complete (evaluation/grading_rubric.md).

| Group | Score |
|---|---|
| all | 67.1% (n=35) |
| text-involving | 62.5% (n=28) |
| source: text-only | 61.9% (n=21) |
| source: table-only | 85.7% (n=7) |
| source: text+table | 64.3% (n=7) |
| type: conceptual | 66.7% (n=6) |
| type: cross-paper | 50.0% (n=9) |
| type: cross-source | 64.3% (n=7) |
| type: factual | 87.5% (n=4) |
| type: insufficient-evidence | 50.0% (n=2) |
| type: tabular | 85.7% (n=7) |

Distribution: 2 x 14, 1 x 19, 0 x 2.
Failure modes (score below 2): generation_error 10, partial_retrieval 7, retrieval_miss 2, sql_error 2

| ID | Source | Score | Failure mode | Missing / wrong / citation issues |
|---|---|---|---|---|
| Q01 | text-only | 2 | none |  |
| Q02 | text-only | 2 | none |  |
| Q03 | text-only | 2 | none |  |
| Q04 | text-only | 1 | generation_error | article summary step (focusing on new events so publication date is the resolution date); Lists 'Article Selection' as step 1 of the four-step construction process in place of the article summary step |
| Q06 | text-only | 1 | partial_retrieval | third desideratum (path length) stated as such; Table 1 complexity formulas for self-attention, recurrent and convolutional layers; cheaper than recurrent when n < d |
| Q07 | text-only | 2 | none |  |
| Q08 | text-only | 1 | generation_error | BN MNIST network reaches higher test accuracy; paper only conjectures BN brings layer Jacobian singular values near 1 and says the precise effect on gradient propagation remains for further study |
| Q09 | text-only | 2 | none |  |
| Q11 | text-only | 1 | partial_retrieval | [class] token; Transformer's post-LN placement (contrast); Position information: learned 1D vs sinusoidal; Feed-forward activation: GELU vs ReLU; Transformer's token-embedding input (contrast) |
| Q12 | text-only | 1 | partial_retrieval | MAE loss is MSE on masked patches; I-JEPA loss is average L2 distance; Table 7 figures 66.9 vs 40.7 (ViT-L/16, 1% linear probe); Target encoder is an EMA of the context encoder |
| Q13 | text-only | 2 | none |  |
| Q14 | text-only | 1 | retrieval_miss | ViT used as the dynamics predictor with temporal causal attention mask; Stop-gradient is for collapse prevention, cites Grill et al. (BYOL), chosen as it needs no negatives or extra hyper-parameters;  |
| Q15 | text-only | 1 | partial_retrieval | BYOL default probabilities: blur 1.0/0.1, solarization 0.0/0.2; Conclusion that the two papers' probabilities match; BabyCL cites Zhuang et al. (2021): contrastive methods with negative sampling most  |
| Q16 | text-only | 0 | retrieval_miss | Daily Oracle uses BM25; BM25 comes close to perfect scores on LIMIT while dense models struggle; Attributed to sparse models' high dimensionality |
| Q17 | text-only | 0 | partial_retrieval | Daily Oracle kappa 0.26, 89.52%, 85.00%; FIRE-Bench human validation on 33% subset; FIRE-Bench precision 0.95, recall 0.86, F1 0.89; Claims FIRE-Bench does not validate its automated scoring against h |
| Q18 | text-only | 1 | generation_error | Paper's explicit statement that distilling the specialists back into a single net has not yet been shown; Implies that a distillation-of-specialists experiment exists in the paper but is just missing  |
| Q20 | text-only | 1 | generation_error | Full-set oracle figure (Claude 2 4.8%) not given; the stated oracle 'best' of ~4-4.5% comes from a subset table; Describes Claude 2 4.01% / SWE-Llama 13b 4.54% as 'per-repository oracle retrieval resu |
| Q21 | table-only | 2 | none |  |
| Q23 | table-only | 2 | none |  |
| Q24 | table-only | 2 | none |  |
| Q25 | table-only | 1 | sql_error | Spurious extra 50->101 row (0.764 gain / 3.48 GMACs = 0.2195); Spurious extra 34->50 row (4.310 gain / 0.68 GMACs = 6.338) |
| Q27 | table-only | 2 | none |  |
| Q29 | table-only | 1 | sql_error | Identity of the best rows (mobilenetv4_conv_medium...384, tiny_vit_21m_512, eva02_large_patch14_448); Parameter counts / ~31x fewer parameters for the under-10M model vs the overall best; Says the lar |
| Q30 | table-only | 2 | none |  |
| Q31 | text+table | 2 | none |  |
| Q32 | text+table | 1 | generation_error | Relative (percentage) differences; Paper values 1.8 and 7.6 not sourced to the paper (answer says they are not in the passages although ResNet p.5 Table 1 was retrieved); 1.8 and 7.6 billion FLOPs tak |
| Q34 | text+table | 1 | partial_retrieval | Random patch masking at a high ratio (75%); Encoder that processes only the visible patches |
| Q35 | text+table | 1 | generation_error | Pairs vit_base_patch16_384 (+4.908), vit_base_patch32_224 (+5.824), vit_base_patch32_384 (+4.608), vit_small_patch16_384 (+2.684); Overall range 2.56-5.82 and Base 4.6-5.8 vs Small 2.6-2.7 |
| Q37 | text+table | 2 | none |  |
| Q39 | text+table | 1 | generation_error | Claims 78.9% is a supervised baseline reproduced by the BYOL authors with RandAugment for a ResNet-50 (4x, 375M) model, a different architecture; the paper cites 78.9% as the stronger supervised basel |
| Q40 | text+table | 1 | generation_error | Claims the paper's main classification table (Table 3) only compares plain vs residual nets and ResNet depths and compared VGG only on detection/FLOPs; Table 3 includes VGG-16 error rates |
| Q42 | text-only | 1 | generation_error | Says the paper argues fine-tuning and pretraining data matter 'as much as or more than' parameter count; the paper says size is a key component and only suggests data helps; 'Accuracy is inversely rel |
| Q43 | text-only | 1 | partial_retrieval | MMLU check (entropy/log-probability vs accuracy, r = -0.43 / -0.56), finding and hedge; SWE-bench empirical before/after-2023 resolve-rate comparison, little difference except GPT-4, 'largely promisin |
| Q44 | text-only | 1 | generation_error | Claude 2 resolves 4.8% with the oracle retriever; Oracle-collapsed results (GPT-4 1.3%->3.4%, Claude 2 4.8%->5.9%); Gives Claude 2's oracle result as 4.01% '(25% subset, Table 1)' instead of the 4.8%  |
| Q45 | text-only | 2 | none |  |
