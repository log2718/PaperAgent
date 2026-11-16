You are continuing the PaperAgent project in `/Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/`. Before anything else read `README.md`, `evaluation/grading_rubric.md`, the header of `src/grade.py`, `evaluation/heldout_selection.md`, `runs/baseline/report.md` and your project memory. After any context reset, re-read `runs/_run_state.md` (below) and continue from its "next step" line.

## Goal
Run six configurations of the answer pipeline on the **35 development questions**, grade every answer on one 0/1/2 scale, and compare them, with retrieval-only metrics and a cost table alongside. The configurations: `baseline` (token chunks, current), `baseline_repeat` (the same again, to measure run-to-run noise), `chunk_paragraph`, `chunk_paragraph_matched` (paragraphs with the retrieved context matched to the baseline's size), `chunk_paper` (whole papers) and `no_embedding`. Do not start any other item from the professor's list (other embedding models, Gemini, scaling/HPC); I will ask for those separately.

## Rules
- Held-out questions are never run, graded or inspected. `evaluate.py` already refuses them; do not pass `--split held-out`.
- Never `git push`. Do not commit unless I ask. No new dependencies without asking. Keep code small and plain, in the style of `src/*.py`. Run the `simplify` skill over the code you changed at the end.
- Change one factor at a time. The answer model stays `claude -p --model sonnet` with the existing prompts, oracle routing by `data_source_type`, and the existing SQL path. Do not tune anything on a failure.
- Fixes go straight into the existing files (workbook, `runs/baseline/`). Each other configuration gets its own folder under `runs/`, named as above, which is the repo's convention.
- Keep `runs/_run_state.md` current: decisions, exact commands, status per phase, one "next step" line. Update it after every phase. Keep a task list with update_plan.
- Stop and ask me before continuing if a phase would use more than about 4M input tokens, the `claude` CLI errors repeatedly, or a design choice below turns out to be impossible.

## Phase 0: usage logging
Probe one call with `claude -p --output-format json` and look at what it returns. If it reports token usage and cost, change `llm()` in `src/answer.py` to use it and add a `usage` field to each record (`calls`, `input_tokens`, `output_tokens`, cache tokens if given, `cost_usd`, summed over the question's calls). If it does not, estimate tokens from character counts and label them as estimates. Note that `cost_usd` is an API-equivalent figure, not my actual bill. Records already in `runs/baseline/` have no usage; the cost table uses `baseline_repeat` for the baseline row.

## Phase 1: baseline top-up and repeat
1. In place in `runs/baseline/`: reworded or new questions are Q02, Q09, Q30, Q34, Q35, Q37, Q39 (answers are stale) and Q44, Q45 (new). Move the seven stale records into `runs/baseline/superseded.jsonl`, keep every other record untouched, then run `python src/evaluate.py run --ids Q02 Q09 Q30 Q34 Q35 Q37 Q39 Q44 Q45 --out runs/baseline`. Confirm the file ends with exactly the 35 development questions and no errors.
2. `runs/baseline_repeat`: run all 35 development questions again from scratch with identical settings.

## Phase 2: paragraph chunks
Add `--mode token|paragraph|paper` to `src/ingest.py`, writing `data/<mode>/chunks.jsonl`; leave `data/chunks.jsonl` and the token baseline as they are. Let `retrieve.py` take the chunk and index location (argument or environment variable, default unchanged), and add the new index files to `.gitignore`. Paragraphs: PyMuPDF blocks, consecutive fragments under about 40 words merged into the next paragraph, paragraphs over about 350 tokens split at sentence boundaries, heading lines attached to the paragraph below, same metadata schema (paper, pages, section, chunk_id). Same embedding model and prefixes, K=5. Report chunk count, the token-length distribution, and the wall time and size of chunking plus index build.

Run the 28 text-involving development questions into `runs/chunk_paragraph`. The 7 table-only questions do not depend on retrieval, so copy their baseline records unchanged into every configuration except `baseline_repeat`, and say so in the state file.

Matched context: compute the mean retrieved-context size in tokens of the baseline at K=5 over the 28 text-involving questions. For `chunk_paragraph_matched`, take paragraphs in rank order until the cumulative size reaches that budget (cap 30 paragraphs), and run the same 28 questions.

## Phase 3: whole-paper chunks
One unit per paper: the full text with `[page N]` markers. Nomic's window is 8192 tokens, so embed the title plus the first ~300 words of the abstract as the paper vector (document this). Retrieve the top 3 papers per question and give the model their full text, capped at about 100k tokens (log any truncation). Citations must still use `[paper, p.N]`. Log `retrieved` in the same schema (`paper`, `pages` such as "1-31", `score`, `chunk_id`) but store character counts instead of the full text, so `grade.py` works and the JSONL stays small. Before running, print an estimate of total input tokens (my measure: papers are 8k to 36k tokens; whole corpus about 270k) and apply the stop rule above. Run the 28 text-involving questions into `runs/chunk_paper`.

## Phase 4: no embeddings
Same downstream as Phase 3 (full text of the selected papers, same prompts and cap). Only the selector changes: one `llm()` call that sees the question and a catalogue of the 15 papers (short name, title, first ~150 words of the abstract) and returns up to 3 short names as JSON. No vectors and no index anywhere. Log the router output. Report whether the whole corpus fits the model's context; do not attempt all papers at once unless it does. Run the 28 text-involving questions into `runs/no_embedding`.

## Phase 5: retrieval-only metrics and cost table (no answer-model calls)
- `src/retrieval_metrics.py` writes `runs/retrieval_metrics.md`. For each retrieval configuration and each of the 28 text-involving questions, using the workbook's gold evidence (paper, page): share of gold pages covered, share of required papers retrieved, MRR of the first retrieved unit that covers a gold page, and context size in tokens. Sweep K in {1, 3, 5, 10, 20} for token and paragraph chunks, and N in {1, 2, 3, 5} papers for the paper-level index. For `no_embedding` use the logged router choices (paper recall only). Report by question type, and say which questions have no retrieved gold page under every configuration.
- `python src/evaluate.py cost ...` (add this small subcommand) writes `runs/cost_table.md` over the 28 text-involving questions for `baseline_repeat`, `chunk_paragraph`, `chunk_paragraph_matched`, `chunk_paper` and `no_embedding`: mean and total latency, LLM calls, input and output tokens, API-equivalent cost, plus the one-time chunking and indexing time and index size per configuration.

## Phase 6: grading (consistency matters more than speed)
Grade only after all six runs are complete, so every configuration is judged in the same way.
1. `python src/grade.py packet runs/baseline runs/baseline_repeat runs/chunk_paragraph runs/chunk_paragraph_matched runs/chunk_paper runs/no_embedding` builds one blind packet per question with all configurations' answers shuffled and identical answers merged.
2. Use the `lab-core:subagent-briefs` skill. Write each grader brief to a file under `runs/_grading/briefs/` first. Spawn fresh grader subagents (Agent tool, `model: opus`), each given the rubric text, about 8 packets, and the output schema, and nothing about which run is which. They return JSONL with the fields in the rubric. Concatenate into `runs/_grading/grades.jsonl`; `python src/grade.py check runs/_grading/grades.jsonl` must report 0 problems (send failures back to a grader).
3. Reliability: a second grader (`model: sonnet`, fresh context) re-grades a random 25% of candidates. Report exact agreement and quadratic-weighted kappa, adjudicate every disagreement yourself against the rubric, and record the adjudications.
4. `python src/grade.py summarize runs/_grading/grades.jsonl` writes each run's `grades.jsonl` and `grades.md` (it overwrites the old 0-4 `runs/baseline/grades.md`, which stays in git history) and `runs/_grading/comparison.md`. The difference between `baseline` and `baseline_repeat` is the noise estimate; treat configuration differences smaller than it as noise.

## Phase 7: report and housekeeping
- Add a short results section to `README.md` using the `lab-core:docs-writing` skill (read its guide, then run its `scripts/check.py --type readme` on the file). One table with overall, text-involving and by-question-type scores per configuration, the paired bootstrap interval against the baseline, the noise estimate, chunk statistics, the retrieval-only and cost tables in short form, and how to reproduce each configuration. Keep it brief.
- Update the project memory note. Do not commit.
- Final message: the score table, which configuration is best and by how much, whether differences exceed the noise estimate (35 questions is small), how retrieval-only metrics line up with graded scores, the cost trade-off, the failure modes that changed, grader agreement, wall-clock time and approximate token use, and anything you were unsure about.

## Done when
`results.jsonl` in each of the six run folders has the 35 development questions (the four non-baseline variants include the copied table-only rows) and no errors; no held-out ID appears in any run, grade or metric file; `grade.py check` passes; every number in the README matches a generated file; `runs/_run_state.md` shows all phases complete.
