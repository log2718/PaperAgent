# Grades: runs/chunk_paper

Score = points / (2 x questions); 0 wrong, 1 correct but incomplete, 2 correct and complete (evaluation/grading_rubric.md).

| Group | Score |
|---|---|
| all | 84.3% (n=35) |
| text-involving | 83.9% (n=28) |
| source: text-only | 88.1% (n=21) |
| source: table-only | 85.7% (n=7) |
| source: text+table | 71.4% (n=7) |
| type: conceptual | 91.7% (n=6) |
| type: cross-paper | 83.3% (n=9) |
| type: cross-source | 71.4% (n=7) |
| type: factual | 87.5% (n=4) |
| type: insufficient-evidence | 100.0% (n=2) |
| type: tabular | 85.7% (n=7) |

Distribution: 2 x 24, 1 x 11, 0 x 0.
Failure modes (score below 2): generation_error 7, sql_error 2, retrieval_miss 1, other 1

| ID | Source | Score | Failure mode | Missing / wrong / citation issues |
|---|---|---|---|---|
| Q01 | text-only | 2 | none |  |
| Q02 | text-only | 1 | generation_error | Says the Section 4.2 text figures and Table 1 figures are drawn from the same passage (p.6); the table is on p.5; Says the 2.30 table gain matches the text claim of a 2.6-point gain, when the two disa |
| Q03 | text-only | 2 | none |  |
| Q04 | text-only | 2 | none |  |
| Q06 | text-only | 2 | none |  |
| Q07 | text-only | 2 | none |  |
| Q08 | text-only | 1 | generation_error | BN-x5-Sigmoid 69.8% vs Inception with sigmoid never above 1/1000 |
| Q09 | text-only | 2 | none |  |
| Q11 | text-only | 2 | none |  |
| Q12 | text-only | 2 | none |  |
| Q13 | text-only | 2 | none |  |
| Q14 | text-only | 1 | retrieval_miss | ResNet paper: residual learning with shortcut connections to ease optimisation of deeper nets; ViT paper: patch embeddings processed by a standard Transformer encoder (alternating MSA/MLP); BYOL paper |
| Q15 | text-only | 1 | generation_error | BabyCL cites Zhuang et al. (2021) finding contrastive methods with negative sampling most effective on SAYCam; BYOL Table 6 augmentation probabilities cited to p.16; the table is on p.17 |
| Q16 | text-only | 2 | none |  |
| Q17 | text-only | 2 | none |  |
| Q18 | text-only | 2 | none |  |
| Q20 | text-only | 2 | none |  |
| Q21 | table-only | 2 | none |  |
| Q23 | table-only | 2 | none |  |
| Q24 | table-only | 2 | none |  |
| Q25 | table-only | 1 | sql_error | Spurious extra 50->101 row (0.764 gain / 3.48 GMACs = 0.2195); Spurious extra 34->50 row (4.310 gain / 0.68 GMACs = 6.338) |
| Q27 | table-only | 2 | none |  |
| Q29 | table-only | 1 | sql_error | Identity of the best rows (mobilenetv4_conv_medium...384, tiny_vit_21m_512, eva02_large_patch14_448); Parameter counts / ~31x fewer parameters for the under-10M model vs the overall best; Says the lar |
| Q30 | table-only | 2 | none |  |
| Q31 | text+table | 2 | none |  |
| Q32 | text+table | 1 | generation_error | Suggests the paper's 3.8 GFLOPs was a rounded estimate and timm's 4.11 'reflects the actual bottleneck computation more precisely', using the 'similar time complexity' block-design remark as support;  |
| Q34 | text+table | 2 | none |  |
| Q35 | text+table | 1 | generation_error | Calls the gain 'clearly size-dependent' and says bigger models extract more value from more data; with only two sizes (and patch-size order flipping between resolutions) the table cannot isolate a siz |
| Q37 | text+table | 1 | other | Statement that accuracy gaps are confounded with pre-training data and recipe (e.g. the ImageNet-1k-only ViT-B/16 row 79.154 is below all a1h ResNets); The paper's caveat that efficiency depends on sc |
| Q39 | text+table | 2 | none |  |
| Q40 | text+table | 1 | generation_error | Parenthetical says the paper reports '11.3%/9.33% top-5 for VGG-16/ResNet'; Table 3 gives VGG-16 top-5 error 9.33 and ResNet-152 5.71, and 11.3 is the FLOPs figure |
| Q42 | text-only | 2 | none |  |
| Q43 | text-only | 1 | generation_error | Unsupported outside claim that a date-based check is 'not applicable' to MMLU because 'GPT-3 training data predates/overlaps the test by construction'; Describes the entropy-accuracy and log-probabili |
| Q44 | text-only | 2 | none |  |
| Q45 | text-only | 2 | none |  |
