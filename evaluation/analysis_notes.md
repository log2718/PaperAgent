# Analysis notes

Detail behind the README's Results section. Every number comes from the files linked in each section. The scores are one answer model (Sonnet through the Claude Code CLI) on the 35 development questions, so differences below about 0.2 points on the 0-2 scale are within noise.

## Run-to-run noise

Re-running the baseline changed 3 of 35 scores (2 up, 1 down). The mean difference is +0.03 with a 95% bootstrap interval of -0.06 to +0.11. Retrieval was identical for all 35 questions, so the changes come from the answer model. The seven table-only questions use no retrieval. The variants copy the baseline's answers to them and score 85.7%, while `baseline_repeat` answered them again and scores 92.9% (Q29 went from 1 to 2).

## Failure modes

Source: `runs/_grading/comparison.md`. Answers scoring below 2 are labelled by the graders as retrieval failures (`retrieval_miss` plus `partial_retrieval`) or as something else.

| Run | Retrieval failures | Generation errors | SQL errors |
|---|---|---|---|
| baseline | 14 | 5 | 2 |
| baseline_repeat | 14 | 4 | 1 |
| chunk_paragraph | 18 | 6 | 2 |
| chunk_paragraph_matched | 9 | 10 | 2 |
| chunk_paper | 1 | 7 | 2 |
| no_embedding | 1 | 6 | 2 |

Whole-paper context removes almost all retrieval failures. Generation and SQL errors do not fall with it. Three questions score 1 in all six runs: Q25 fails on SQL, Q35 on incomplete generation, and Q15 on partial retrieval in four runs and generation in two.

## Baseline retrieval on cross-paper questions

Cross-paper questions score 44.4% in the baseline. The cause is one pooled query with top 5 over all 498 chunks, not the embedding model: the papers a question names compete for five slots in a single ranking. Two failure modes appear:

- *A paper never appears* (Q12 no MAE, Q13 no Distillation, Q14 no ResNet, ViT or BYOL, Q43 no MMLU). One paper's chunks crowd out the rest.
- *Right paper, wrong page* (Q11, Q15, Q16, Q17). Several papers are reached but the passage that holds the answer is not in the top 5.

Candidate fixes, to be tried on development questions only: per-paper retrieval for the papers a question names, an LLM step that splits the question into one sub-query per paper or claim, and keyword search added to embeddings (for terms such as "BM25" or "Table 7").

## Retrieval-only metrics

Source: `runs/retrieval_metrics.md`. Gold pages covered is the share of the workbook's evidence (paper, page) pairs inside the retrieved units, over the 28 text-involving questions. Coverage orders the runs correctly but is not enough alone. The paragraph budget covers more gold pages than the baseline (0.77 against 0.59) and scores the same. At K=20 token chunks cover 0.81 of gold pages, still below whole papers at N=2 (0.93). No answer run was made at K=20, so the effect of more chunks on answer quality is not measured.

## Cost and context size

Source: `runs/cost_table.md`. Cost is the CLI's API list-price equivalent, not a bill. `no_embedding` costs about 59% of `chunk_paper` per question because the router often picks fewer than three papers (mean context 30,431 tokens against 59,069), even though it adds a second call. Both whole-paper runs fit the model's 1M-token context window at this corpus size (297k embedding-tokenizer tokens in total). They would not fit a larger corpus.

## Grader agreement and adjudication

Opus graded all 35 questions and a Sonnet grader with fresh context graded all 35 again (182 candidates). Exact agreement is 87.9% (160 of 182) and quadratic-weighted kappa is 0.819. Every disagreement was one point. Opus scored higher in 13 of the 22 disagreements and Sonnet in 9.

The 22 disagreements were settled against the rubric (`runs/_grading/adjudication.md`), which changed 7 scores. The README tables use the adjudicated grades. A language model settled them, not a person.

## Limits of the evaluation

- The graders and the adjudicator are language models from one family, so shared blind spots are not measured. A human read of the 22 disagreements is the next check.
- The 35 questions give wide intervals. Seven of them are table-only and identical across five of the six runs.
- Q39 no longer separates the configurations, because all six runs give the right counts. Its wording changed after development runs (from "reach" to "at or above"), because four of the six first runs read "reach" as an exact match. The reference answer is unchanged. Q39 is a development question.
- The first-pass Opus graders saw the reference SQL result cut at 800 characters and, for Q30 and Q39, the wrong variant. Q30 and Q39 were regraded on corrected packets, and the second grader saw the full result. Two first-pass graders also opened chunk files under `data/` to check pages, which the grader brief now forbids.
- No run used the held-out questions. There is no held-out score yet.
- The whole-paper runs depend on a 1M-token context window.
