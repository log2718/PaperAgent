# PaperAgent

An agentic system for reading research papers, querying structured experimental data, and answering questions with grounded evidence.

## Goal

Answer questions from 15 ML papers (embedding-based retrieval), from structured experimental data (SQL), or from both, and say so when the evidence does not establish an answer. Evaluation comes first: 43 questions with reference answers and verified evidence.

This repo currently holds the **first baseline only**: plain top-k retrieval and one LLM call per step. No agents, rerankers, hybrid search or prompt tuning yet.

## Layout

```
evaluation/    43-question workbook (text_evaluation_candidates.xlsx), summaries, held-out selection
tabular_data/  timm results: raw CSVs, checksums, build script, timm_results.sqlite, data dictionary
data/          chunks.jsonl (committed); index.faiss (rebuilt, git-ignored)
src/           ingest.py  retrieve.py  sql_tool.py  answer.py  evaluate.py
runs/          sample/ and baseline/ outputs: results.jsonl (full logs) and report.md
```

## Pipelines

**Text:** PDFs (`~/Desktop/ML/Papers/`, not in the repo) -> PyMuPDF text -> ~700-token chunks with ~100 overlap (tokens counted by the embedding model's tokenizer; metadata: paper, page range, approximate section) -> `nomic-embed-text-v1.5` embeddings (local) -> exact FAISS inner-product index -> `search_papers(query, k=5)` -> LLM answers from the retrieved chunks only, citing `[paper, p.N]`.

**Tabular:** timm result CSVs -> cleaned SQLite (`tabular_data/build_timm_db.py`) -> `query_timm(sql)`, read-only and SELECT-only (read-only connection plus a SQLite authorizer). `python src/sql_tool.py` re-runs the 21 SQL statements stored in the workbook and checks they reproduce the stored results.

**Answering (`src/answer.py`):** the path follows the question's `data_source_type` label: text-only = retrieve then answer; table-only = LLM writes SQL (given `data_dictionary.md`), run, then answer; text+table = retrieve, LLM writes SQL with the passages in view, then answer from both. The prompts allow an explicit "the evidence does not establish this". The LLM is the Claude Code CLI (`claude -p`, no tools, empty working directory), wrapped in one function, `llm()`, so it can be swapped for an API client.

## Evaluation setup

- 43 questions: 23 text-only, 10 table-only, 10 text+table; 8 flagged for manual review.
- `split` column: **10 held-out** (never used for tuning or failure-driven changes; selection in `evaluation/heldout_selection.md`) and **33 development**. `evaluate.py` refuses to run held-out questions unless `--split held-out` is passed.
- `report.md` lists reference and system answers side by side for manual grading, plus three heuristic diagnostics (retrieval page hit against the workbook's gold evidence pages, SQL value overlap with the reference result, abstention wording). It reports no overall accuracy.

## Run the baseline

Needs Python 3.11+, the `claude` CLI on PATH (logged in), and the PDFs in `~/Desktop/ML/Papers/`.

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/ingest.py                                    # PDFs -> data/chunks.jsonl
.venv/bin/python src/retrieve.py build                            # chunks -> data/index.faiss
.venv/bin/python src/retrieve.py "What does BYOL use as its target?"   # try retrieval
.venv/bin/python src/sql_tool.py                                  # SQL self-check
.venv/bin/python src/evaluate.py run --ids Q01 Q11 Q21 Q31 Q18 --out runs/sample
.venv/bin/python src/evaluate.py run --split development --out runs/baseline
```

Each line of `results.jsonl` logs question ID, question, source type, retrieved chunks, SQL attempts and results, answer, model and latency.

## Known baseline limits

One retrieval query per question (multi-paper questions mostly retrieve a single paper), a regex for section names (approximate), and routing taken from the question's label rather than predicted. These are left as-is on purpose; they are the starting point for improvement on the development set.
