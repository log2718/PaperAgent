# PaperAgent

## Overview

PaperAgent answers questions about 15 machine-learning papers and about a table of image-model benchmark results (the timm database). It cites the passages it used, and it says so when the evidence does not establish an answer. The repository holds the system and an evaluation of one design question: how should the context given to the answer model be chosen?

- **Evaluation set.** 45 questions with reference answers and verified evidence pages. 35 are development questions and 10 are held out.
- **Baseline.** Top-5 retrieval over 700-token chunks scores 67.1% on the 35 development questions (0-1-2 grading, two blind graders).
- **Highest score.** Giving the model 3 whole papers scores 84.3% when an embedding index picks the papers and 87.1% when the model picks them from titles and abstracts. The two are not distinguishable on 35 questions.
- **Retrieval failures.** Answers lost to retrieval fall from 14 with the baseline to 1 with either whole-paper configuration. Generation and SQL errors do not fall.
- **Cost.** Whole-paper context sends 5 to 9 times more input tokens per question, and it only fits while the corpus fits in the model's context window.
- **Held-out questions.** None of the 10 held-out questions was run, graded or inspected, and nothing was tuned on them. There is no held-out score yet.

## System

The answer path follows each question's `data_source_type` label.

| Source type | Path |
|---|---|
| text-only | Retrieve passages, then the model answers from them and cites `[paper, p.N]`. |
| table-only | The model writes one SQL query against the timm database, the query runs read-only, then the model answers from the result. |
| text+table | Retrieve passages, the model writes SQL with the passages in view, then it answers from both. |

- **Text.** PDFs go through PyMuPDF into chunks (tokens counted with the embedding model's tokenizer, with page range and approximate section as metadata). `nomic-embed-text-v1.5` embeds them locally into an exact FAISS inner-product index.
- **Tables.** The timm result CSVs are cleaned into SQLite (`tabular_data/build_timm_db.py`). `query_timm` accepts only SELECT statements on a read-only connection. `python src/sql_tool.py` re-runs the 22 reference queries stored in the workbook and checks that they reproduce the stored results.
- **Model.** The Claude Code CLI (`claude -p --model sonnet`, no tools) behind one function, `llm()` in `src/answer.py`. The prompts are general, and the same model and prompts are used in every configuration.

The configurations change only what the model is shown (`--config`):

| Configuration | What the model sees |
|---|---|
| `token` (baseline) | Top 5 chunks of about 700 tokens, 100 overlap. |
| `paragraph` | Top 5 paragraph chunks. |
| `paragraph_matched` | Paragraph chunks in rank order until 3,460 tokens, the baseline's mean retrieved size. |
| `paper` | The 3 whole papers nearest the question, where a paper is represented by its title and first 300 abstract words. |
| `no_embedding` | The model picks up to 3 papers from titles and the first 150 abstract words, then sees those papers whole. No vectors are used. |

Table-only questions use no retrieval, so their baseline answers are copied into every variant except `baseline_repeat`.

## Evaluation

- **Questions.** 25 text-only, 10 table-only and 10 text+table, covering 15 papers and the timm database. The `split` column marks 10 held-out questions (selection in `evaluation/heldout_selection.md`) and 35 development questions. `src/evaluate.py` refuses to run held-out questions unless `--split held-out` is passed.
- **Grading.** A 0-1-2 scale (`evaluation/grading_rubric.md`): 0 wrong, 1 correct but incomplete in content or in sources cited, 2 correct and complete. A run's score is its points divided by twice the number of questions.
- **Blind grading.** For each question, the answers from all six runs were shuffled under anonymous labels, identical answers were merged, and a mechanical check of cited papers and pages against retrieved ones was attached. Opus graded every question, then Sonnet with fresh context graded every question again.
- **Agreement.** The two graders agreed on 160 of 182 answers (87.9%, quadratic-weighted kappa 0.819). All 22 disagreements were one point and were settled against the rubric (`runs/_grading/adjudication.md`).
- **Comparisons.** Runs are compared question by question with a paired bootstrap 95% interval on the mean score difference. A repeat of the baseline measures run-to-run noise.

## Results

Six runs on the 35 development questions. "Text-involving" excludes the 7 table-only questions, which use no retrieval.

| Run | All (n=35) | Text-involving (n=28) | Text-only (n=21) | Text+table (n=7) |
|---|---|---|---|---|
| `baseline`: 700-token chunks, top 5 | 67.1% | 62.5% | 57.1% | 78.6% |
| `baseline_repeat`: same configuration again | 68.6% | 62.5% | 57.1% | 78.6% |
| `chunk_paragraph`: top 5 paragraphs | 60.0% | 53.6% | 50.0% | 64.3% |
| `chunk_paragraph_matched`: paragraphs up to 3,460 tokens | 67.1% | 62.5% | 61.9% | 64.3% |
| `chunk_paper`: 3 whole papers chosen by embedding | 84.3% | 83.9% | 88.1% | 71.4% |
| `no_embedding`: 3 whole papers chosen by the model | 87.1% | 87.5% | 88.1% | 85.7% |

### Ablation comparisons

These are ablations that change what the model is shown while holding the model, prompts, SQL path and routing fixed. They are not all clean single-factor tests, as the third row shows.

| Comparison | Mean difference (0-2 scale) | 95% interval | Reading |
|---|---|---|---|
| `baseline_repeat` against `baseline` | +0.03 | -0.06 to +0.11 | Run-to-run noise. |
| `chunk_paragraph` against `baseline` | -0.14 | -0.31 to +0.03 | Smaller units at fixed K do not help, and may hurt. |
| `chunk_paragraph_matched` against `baseline` | +0.00 | -0.17 to +0.17 | With context size matched, paragraph and token chunks tie. |
| `chunk_paper` against `baseline` | +0.34 | +0.11 to +0.60 | Unit size and context size change together (59,069 against 3,460 tokens). |
| `no_embedding` against `baseline` | +0.40 | +0.20 to +0.60 | Same, with fewer tokens (30,431). |
| `chunk_paper` against `no_embedding` | -0.06 | -0.23 to +0.11 | Choosing papers by embedding or by model is not distinguishable here. |

- **Whole-paper context is not automatically better.** Its gain is large on text-only questions (57.1% to 88.1%) and on cross-paper questions (44.4% to 83.3%). `chunk_paper` scores below the baseline on the 7 text+table questions (71.4% against 78.6%, one point of 14). Table-only questions use no retrieval, so they are unchanged by design.
- **Size is confounded with unit.** The only size-matched control is for paragraphs. No run gives token chunks a large budget, for example K=20 (about 13,900 tokens), so the data cannot say how much of the whole-paper gain comes from whole papers and how much from more context. In the retrieval-only metrics below, token chunks at K=20 cover 0.81 of gold pages, against 0.93 for 2 whole papers.
- **Retrieval is not the whole story.** Retrieval failures fall from 14 (baseline) to 1 (each whole-paper run), but generation errors stay at 4 to 10 per run and SQL errors at 1 to 2.

### Retrieval-only metrics

No model calls. Gold pages covered is the share of the workbook's evidence (paper, page) pairs inside the retrieved units, over the 28 text-involving questions.

| Configuration | Gold pages covered | Mean context tokens | Graded score (text-involving) |
|---|---|---|---|
| paragraph, K=5 | 0.48 | 751 | 53.6% |
| token chunks, K=5 (baseline) | 0.59 | 3,460 | 62.5% |
| paragraph, token budget | 0.77 | 3,537 | 62.5% |
| 3 whole papers by embedding | 0.97 | 59,069 | 83.9% |
| `no_embedding` | 0.99 | 30,431 | 87.5% |

Coverage orders the runs but does not explain them alone: the paragraph budget covers more gold pages than the baseline and scores the same. A K sweep and an N sweep are in `runs/retrieval_metrics.md`.

### Cost

Per text-involving question, from `runs/cost_table.md`. Cost is the CLI's API list-price equivalent, not a bill.

| Run | Input tokens | Cost (USD) | Mean latency (s) |
|---|---|---|---|
| `chunk_paragraph` | 3,599 | 0.026 | 18.9 |
| `baseline_repeat` | 8,977 | 0.051 | 21.3 |
| `chunk_paragraph_matched` | 9,659 | 0.055 | 23.8 |
| `no_embedding` | 64,888 | 0.276 | 25.8 |
| `chunk_paper` | 113,583 | 0.471 | 23.4 |

### Limitations

- The 35 development questions give wide intervals, and 7 of them are table-only and identical across five of the six runs. Treat differences below about 0.2 points as noise.
- The graders and the adjudicator are language models from one family. A human read of the 22 disagreements is the next check.
- One development question (Q39) was reworded after development runs because the original wording was ambiguous. The reference answer is unchanged, and all six runs now answer it correctly.
- The whole-paper runs rely on the model's 1M-token context window and will not fit a much larger corpus.

Detail on noise, failure modes, baseline retrieval failures, grader agreement and these limits is in `evaluation/analysis_notes.md`. Full comparison tables are in `runs/_grading/comparison.md`.

## Repository structure

```
evaluation/    45-question workbook (text_evaluation_candidates.xlsx), grading rubric, held-out selection,
               question-set summary, analysis_notes.md
tabular_data/  timm results: raw CSVs, checksums, build script, timm_results.sqlite, data dictionary
data/          chunks.jsonl and stats.json (token chunks), paragraph/ and paper/ (same files);
               index.faiss files are rebuilt and git-ignored
src/           ingest.py  retrieve.py  sql_tool.py  answer.py  evaluate.py  grade.py  retrieval_metrics.py
runs/          one folder per configuration (results.jsonl, report.md, grades.md), cost_table.md,
               retrieval_metrics.md, _grading/ (packets, grader outputs, agreement, adjudication, comparison)
```

`runs/_run_state.md` and `evaluation/next_run_prompt.md` are working notes from the improvement runs. They are kept for reproducibility.

## Running the project

You need Python 3.11+ and the `claude` CLI on your PATH and logged in. The source PDFs are not in the repository. `ingest.py` reads them from `~/Desktop/ML/Papers/` (set `PDF_DIR` in `src/ingest.py` to change it). The chunk files in `data/` are committed, so you can rebuild the indexes and run the pipeline without the PDFs.

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/ingest.py                                    # PDFs -> data/chunks.jsonl
.venv/bin/python src/retrieve.py build                            # chunks -> data/index.faiss
.venv/bin/python src/retrieve.py "What does BYOL use as its target?"
.venv/bin/python src/sql_tool.py                                  # SQL self-check
.venv/bin/python src/evaluate.py run --split development --out runs/baseline
```

To rebuild the other indexes and rerun every configuration:

```bash
.venv/bin/python src/ingest.py --mode paragraph --out data/paragraph && .venv/bin/python src/retrieve.py build paragraph
.venv/bin/python src/ingest.py --mode paper --out data/paper && .venv/bin/python src/retrieve.py build paper
.venv/bin/python src/evaluate.py run --split development --config token --out runs/baseline_repeat
.venv/bin/python src/evaluate.py run --split development --config paragraph --reuse runs/baseline --out runs/chunk_paragraph
.venv/bin/python src/evaluate.py run --split development --config paragraph_matched --reuse runs/baseline --out runs/chunk_paragraph_matched
.venv/bin/python src/evaluate.py run --split development --config paper --reuse runs/baseline --out runs/chunk_paper
.venv/bin/python src/evaluate.py run --split development --config no_embedding --reuse runs/baseline --out runs/no_embedding
.venv/bin/python src/retrieval_metrics.py
.venv/bin/python src/evaluate.py cost runs/baseline_repeat runs/chunk_paragraph runs/chunk_paragraph_matched runs/chunk_paper runs/no_embedding
```

To regrade, build blind packets and give each batch brief to a fresh grader:

```bash
.venv/bin/python src/grade.py packet runs/baseline runs/baseline_repeat runs/chunk_paragraph runs/chunk_paragraph_matched runs/chunk_paper runs/no_embedding
.venv/bin/python src/grade.py batches --size 8                    # briefs in runs/_grading/briefs/
.venv/bin/python src/grade.py check runs/_grading/grades.jsonl
.venv/bin/python src/grade.py batches --size 10 --prefix s        # briefs for the second grader
.venv/bin/python src/grade.py agree runs/_grading/grades.jsonl runs/_grading/grades_second.jsonl
.venv/bin/python src/grade.py summarize runs/_grading/grades_adjudicated.jsonl
```

Each line of `results.jsonl` logs the question ID, source type, retrieved passages, SQL attempts and results, answer, model, latency and token usage. Grader output and the adjudicated grades are in `runs/_grading/`.
