# Baseline grades (development set, 33 questions)

Graded by Claude (Sonnet 5.5) reading each system answer against the workbook's reference answer in `report.md`. This is a single LLM grader, the same model family that produced the answers, so treat it as a first pass and spot-check. Held-out questions were not run or graded. Numbers were compared with the reference answer; I did not re-open the PDFs or re-run the SQL.

**Scale (0-4):** 4 = correct and complete; 3 = correct, minor omission or small overreach; 2 = about half the question answered, rest missing or honestly marked as not established; 1 = mostly missing or unhelpful; 0 = wrong or fabricated. For insufficient-evidence questions, 4 = correct abstention that also says what the paper does show.

## Summary

| Group | n | Score | % |
|---|---|---|---|
| Text-only, single paper (factual/conceptual) | 9 | 28 / 36 | 78% |
| Text-only, cross-paper | 8 | 12 / 32 | 38% |
| Insufficient evidence | 2 | 8 / 8 | 100% |
| Table-only | 7 | 27 / 28 | 96% |
| Text + table | 7 | 27 / 28 | 96% |
| **All development** | **33** | **102 / 132** | **77%** |

17 of 33 scored 4; 24 of 33 scored 3 or more; 9 scored 2 or less. All 9 low scorers are text-only, and all 9 have a retrieval page hit of 0.50 or lower.

## Per question

| ID | Type | Score | Why |
|---|---|---|---|
| Q01 | text, factual | 4 | All numbers, degradation problem, BN and gradient-norm argument, 3x iterations. |
| Q02 | text, factual | 3 | Text figures and Table 1 mismatch found. Offline CVCL row came back truncated ("31"), so the 57.45 vs 57.31 mismatch and the k=4 to k=8 gain were missed; speculates about why text and table differ. |
| Q03 | text, factual | 4 | M=4, both ranges, context block, masking the target-encoder output; adds the Table 11 ablation. |
| Q04 | text, factual | 3 | Counts, seven principles and threshold 13 correct. Omits the article-summary step and the 6 articles/day, 2+2 pairs per article; calls it four steps but lists three. |
| Q06 | text, conceptual | 1 | Retrieved the wrong part of the paper; no Table 1 comparison and no n < d condition. Honest about the gap. |
| Q07 | text, conceptual | 4 | EMA target and predictor, Table 5b collapse when either is removed, near-optimal predictor, target removable. |
| Q08 | text, conceptual | 3 | MNIST evidence, 14x fewer steps, extra changes (LR, dropout, L2) and the "not established" point. Misses the other changes and the Jacobian conjecture. |
| Q09 | text, conceptual | 3 | Geodesic proxy, conditioning, 20-60% / 20-30%, non-uniform results. Says the proof was not in the passages; table reading is vague. |
| Q11 | cross-paper | 2 | Input handling and position embeddings only. Norm placement, GELU vs ReLU, class token missing (Transformer passages not retrieved). |
| Q12 | cross-paper | 2 | I-JEPA side correct. MAE loss not stated; Table 7 numbers (66.9 vs 40.7) missing. |
| Q13 | cross-paper | 2 | BYOL and mean-teacher parts excellent. No distillation passages retrieved, so that half is absent. |
| Q14 | cross-paper | 2 | Temporal Straightening usage correct. Nothing on what ResNet, ViT or BYOL say. |
| Q15 | cross-paper | 1 | BabyCL blur/solarization correct. BYOL's probabilities and the negatives question not found. |
| Q16 | cross-paper | 1 | Abstains. Never found BM25 in Daily Oracle or the LIMIT result. |
| Q17 | cross-paper | 1 | Abstains. No kappa, accuracy or F1 for either paper. |
| Q18 | insufficient | 4 | Correct abstention, correct quote, notes the 4.4% ensemble result. |
| Q20 | insufficient | 4 | Correct abstention, quotes the future-work line, gives the oracle-retrieval rates. |
| Q42 | text, conceptual | 3 | All the comparisons and numbers correct. Headline says pretraining data matters "more than" parameters, stronger than the paper's "suggests"; no not-a-controlled-test caveat. |
| Q43 | cross-paper | 1 | Only FIRE-Bench covered, briefly. MMLU and SWE-bench checks not found. |
| Q21 | table | 4 | Three rows and values exactly right. |
| Q23 | table | 4 | Exact match, SQL overlap 1.00. |
| Q24 | table | 4 | Best mean tag and largest gap correct, all five tags listed. |
| Q25 | table | 3 | Right step (101 to 152, 0.135) and right values, but the query also matched resnet50-variant rows, so two spurious rows appear; the stated cause is a guess. |
| Q27 | table | 4 | All five drops correct; non-monotonic trend and largest drop (resnet50) correct. |
| Q29 | table | 4 | 82.776 / 86.444 / 90.056 and the gaps correct. Overlap score 0.20 is only because the SQL returned no model names. |
| Q30 | table | 4 | 26 frontier rows, 11 at 85% or above, list matches. |
| Q31 | text+table | 4 | N = 49/196/784, GMAC and throughput ratios exact. States the ViT passage was not retrieved but derives the expectation. |
| Q32 | text+table | 4 | Table and percentages exact, resnet50 largest, cause not asserted. |
| Q34 | text+table | 3 | hiera_huge, six-row trend and 75% masking correct. Pretraining description comes from figure captions; treats Hiera scaling as the MAE paper's finding and misses the Hiera-not-in-corpus caveat. |
| Q35 | text+table | 4 | All six gains exact, size dependence, ViT-paper link with caveat. |
| Q37 | text+table | 4 | Accuracy and throughput comparison right; correctly says it neither confirms nor refutes the pre-training-compute claim. |
| Q39 | text+table | 4 | 18/17/13 correct, with the right not-like-for-like caveats. |
| Q40 | text+table | 4 | Parameters, GMACs, throughput and accuracy right; lower FLOPs did not mean faster. |

## Reading the result

- No fabricated facts found in the answers checked. The failures are over-abstention after retrieval missed the key page, not hallucination.
- Table-only and text+table answers are strong because SQL is deterministic and the oracle routing tells the system which tool to use.
- Cross-paper questions fail because one query returns mostly one paper.
- Manual-review questions in this set: Q02 (3), Q09 (3), Q12 (2), Q30 (4), Q34 (3), Q35 (4), Q37 (4), Q39 (4). Their references are the least certain, so check these grades first. Q34's reference says robustness "decreases steadily with size" next to numbers that rise with size; the system's direction is the one the numbers support.
