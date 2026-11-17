# Grading brief, batch 4

Need: grade every candidate answer in one batch of questions on the 0/1/2 rubric. The answers come from different configurations of a
research-paper question-answering system. You are not told which candidate came from which, and you must not try to find out. Grade each
candidate on its own against the reference answer, never against the other candidates.

Steps
1. Read /Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/evaluation/grading_rubric.md in full. It is the only standard.
2. Read /Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/runs/_grading/batches/batch_4.jsonl. Each line is one question with its reference answer, `notes` (grader guidance:
   read it), `gold_evidence` (passages behind the reference), `gold_sql_result`, and `candidates` (label, answer, retrieved pages, a
   mechanical `citation_check`, and the SQL for table questions).
3. For each candidate: list the reference's key points, mark each present, missing or wrong, check the sources (citation_check and
   gold_evidence), then score.
4. Write one JSON object per candidate, one per line, to /Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/runs/_grading/grades_batch_4.jsonl with exactly the fields question_id,
   label, score, failure_mode, missing_points, wrong_claims, citation_issues, rationale. The rubric gives the allowed values and the
   consistency rules.
5. Run (the path contains spaces, keep the quotes)
   `"/Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/.venv/bin/python" "/Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/src/grade.py" check "/Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/runs/_grading/grades_batch_4.jsonl" --packets "/Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/runs/_grading/batches/batch_4.jsonl"`
   and fix every problem it prints. It must end with "0 problems".

Constraints: do not open anything else under /Users/liyanle/Desktop/NYU/26 fall/Research/VIP RAG Research/PaperAgent/runs/ (results, key.json, other grades), do not change any file except your output
file, do not edit code.

Report: how many candidates you graded, the output of the check command, and every candidate where you were unsure (question_id,
label, why).
