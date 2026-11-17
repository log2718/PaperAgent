# Grades: runs/no_embedding

Score = points / (2 x questions); 0 wrong, 1 correct but incomplete, 2 correct and complete (evaluation/grading_rubric.md).

| Group | Score |
|---|---|
| all | 87.1% (n=35) |
| text-involving | 87.5% (n=28) |
| source: text-only | 88.1% (n=21) |
| source: table-only | 85.7% (n=7) |
| source: text+table | 85.7% (n=7) |
| type: conceptual | 91.7% (n=6) |
| type: cross-paper | 83.3% (n=9) |
| type: cross-source | 85.7% (n=7) |
| type: factual | 100.0% (n=4) |
| type: insufficient-evidence | 75.0% (n=2) |
| type: tabular | 85.7% (n=7) |

Distribution: 2 x 26, 1 x 9, 0 x 0.
Failure modes (score below 2): generation_error 6, sql_error 2, partial_retrieval 1

| ID | Source | Score | Failure mode | Missing / wrong / citation issues |
|---|---|---|---|---|
| Q01 | text-only | 2 | none |  |
| Q02 | text-only | 2 | none |  |
| Q03 | text-only | 2 | none |  |
| Q04 | text-only | 2 | none |  |
| Q06 | text-only | 2 | none |  |
| Q07 | text-only | 2 | none |  |
| Q08 | text-only | 2 | none |  |
| Q09 | text-only | 1 | generation_error | States after 're-checking' that all rows in Table 1 increase with the curvature regularizer; Table 1 has decreases (e.g., ResNet 1x384 PointMaze-UMaze open-loop 82.00 to 52.00) |
| Q11 | text-only | 2 | none |  |
| Q12 | text-only | 2 | none |  |
| Q13 | text-only | 2 | none |  |
| Q14 | text-only | 1 | partial_retrieval | BYOL paper: predicting a stop-gradient target network's representation without negatives; predictor plus slow-moving-average target needed to avoid collapse |
| Q15 | text-only | 1 | generation_error | BabyCL cites Zhuang et al. (2021) finding contrastive methods with negative sampling most effective on SAYCam; BYOL much less affected than SimCLR when color distortion is removed |
| Q16 | text-only | 1 | generation_error | Calls Gemini Embed (10.0 recall@100) the best dense model tested; Table 5 shows Promptriever reaching 18.9 |
| Q17 | text-only | 2 | none |  |
| Q18 | text-only | 1 | generation_error | What the paper does show: generalist + 61 specialists ensemble result on JFT (25.0% to 26.1%, 4.4% relative) |
| Q20 | text-only | 2 | none |  |
| Q21 | table-only | 2 | none |  |
| Q23 | table-only | 2 | none |  |
| Q24 | table-only | 2 | none |  |
| Q25 | table-only | 1 | sql_error | Spurious extra 50->101 row (0.764 gain / 3.48 GMACs = 0.2195); Spurious extra 34->50 row (4.310 gain / 0.68 GMACs = 6.338) |
| Q27 | table-only | 2 | none |  |
| Q29 | table-only | 1 | sql_error | Identity of the best rows (mobilenetv4_conv_medium...384, tiny_vit_21m_512, eva02_large_patch14_448); Parameter counts / ~31x fewer parameters for the under-10M model vs the overall best; Says the lar |
| Q30 | table-only | 2 | none |  |
| Q31 | text+table | 1 | generation_error | States the batch-size difference (768 vs 1024) does not matter because samples_per_sec already normalises it, so the comparison is 'valid'; the B/8 throughput ratio is only approximate |
| Q32 | text+table | 2 | none |  |
| Q34 | text+table | 2 | none |  |
| Q35 | text+table | 1 | generation_error | Pairs vit_base_patch16_384 (+4.908), vit_base_patch32_224 (+5.824), vit_base_patch32_384 (+4.608), vit_small_patch16_384 (+2.684); Overall range 2.56-5.82 and Base 4.6-5.8 vs Small 2.6-2.7 |
| Q37 | text+table | 2 | none |  |
| Q39 | text+table | 2 | none |  |
| Q40 | text+table | 2 | none |  |
| Q42 | text-only | 2 | none |  |
| Q43 | text-only | 2 | none |  |
| Q44 | text-only | 2 | none |  |
| Q45 | text-only | 2 | none |  |
