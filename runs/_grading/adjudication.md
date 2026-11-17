# Adjudication of grader disagreements

Every one of the 35 development questions was graded blind by two graders: Opus (`grades.jsonl`) and Sonnet with fresh context (`grades_second.jsonl`). They gave the same score for 160 of 182 candidates (`agreement.md`). The 22 disagreements, all of one point, were settled against the rubric by reading the reference, the notes and the candidate answers. The settling was done by the model that ran this session, not by a person. `grades_adjudicated.jsonl` is `grades.jsonl` with the 7 changes, which take the second grader's record. The first ten rows were settled in the earlier pass on 9 questions and are unchanged.

| Candidate | Opus | Sonnet | Final | Reason |
|---|---|---|---|---|
| Q01 B, C, E | 2 | 1 | 2 | The missing points (zero-padded identity shortcuts, the 3x longer training check) are asides in the reference, not what the question asks. |
| Q13 A, B, D | 2 | 1 | 2 | The missing details (lower weight on the label term, temperature 1 afterwards, stop-gradient) go beyond the asked points. A states the label use loosely but not wrongly. |
| Q20 E | 2 | 1 | 2 | Calls Claude 2 at 1.96% the best BM25 result, which is the paper's own wording and is cited. Candidates B and F make the same statement and score 2. |
| Q32 E | 1 | 2 | 2 | Floats a bottleneck explanation but marks it unconfirmed. The reference only forbids asserting a cause. Candidate C asserts it more strongly and stays at 1. |
| Q45 A, D | 1 | 2 | 2 | The mini-batch-statistics claim is correct and supported by the retrieved p.8 text they quote. The BYOL half is complete. |
| Q02 E | 2 | 1 | 1 | Says the 2.30 table gain "matches" the text's 2.6-point gain. The notes say the two sources disagree, and the answer itself listed the differing text figures. A wrong peripheral claim caps the score at 1. |
| Q06 B, D | 1 | 0 | 1 | Both retrieved only p.7-8 and mostly abstain, but they report correct convolution facts from the passage (cost and path length), and B names the three desiderata. That is something toward the key points, so not a full abstention. |
| Q07 E | 1 | 2 | 1 | The closing summary says either component "can substitute for the other", but only the target network can be replaced (by a near-optimal predictor). A loose peripheral claim caps the score at 1. |
| Q08 A | 1 | 2 | 1 | Omits the higher test accuracy on MNIST, the 13.3M against 31.0M step counts, and the gradient-propagation caveat on p.5. Its "not established" part comes only from the conclusion. |
| Q08 C | 1 | 2 | 1 | Complete except the ImageNet sigmoid result (BN-x5-Sigmoid 69.8% against Inception never above 1/1000), which the reference lists as evidence. |
| Q09 A | 2 | 1 | 2 | The notes say the explanation is graded mainly and the "not uniform" concern is no longer graded in detail. A gives the Euclidean-versus-geodesic point, conditioning, the linear-dynamics analysis and the loss landscape, and quotes the paper's own "consistently improves". |
| Q29 B | 1 | 2 | 2 | The question asks for three top-1 values and how they compare. All values and differences are correct. The model names and parameter counts are in the reference but not asked for, and the query returned only maxima. |
| Q37 A | 2 | 1 | 1 | Calls the ResNet rows "standard ImageNet-1k-trained" although its own best ResNet-50 row (fb_swsl_ig1b_ft_in1k) uses extra data. It also never says the accuracy gap tracks pre-training data and recipe. |
| Q37 C | 2 | 1 | 2 | Names the rows with correct values and ratios, says the data compare inference with pre-training compute on different checkpoints and recipes, and says it neither confirms nor refutes the claim. Candidate E does the same and scores 2 under both graders. |
| Q40 C | 1 | 2 | 1 | Says the paper's main classification table only compares plain against residual nets and ResNet depths. Table 3 lists VGG-16 error rates. A wrong peripheral claim caps the score at 1. |
| Q43 C | 1 | 2 | 2 | Gives all three checks, findings and hedges, including the r values, the pre- and post-2023 split with the GPT-4 exception, and the "rather than proving its absence" wording. The missing items (the promised list of question sources, collecting new instances later) are asides, as in Q01. |

Summary: of 22 disagreements, Opus scored higher in 13 and Sonnet in 9. The final score matches Opus in 15 and Sonnet in 7.
