# Grading rubric (0 / 1 / 2)

Used with `src/grade.py`. One score per system answer, judged against the question's `reference_answer`, the `Evidence` rows (gold passages) and the `TabularEvidence` result in `text_evaluation_candidates.xlsx`. The reference answer is the standard; do not credit or penalise anything because of which run or configuration produced the answer (packets are blind).

| Score | Meaning |
|---|---|
| **2** | Correct and complete: every part of the question is answered, every key point of the reference is present with correct values, nothing wrong, and paper-derived claims are cited to the right paper and a page that supports them. |
| **1** | Correct but incomplete: nothing central is wrong, but the answer misses a part of the question or some key points, or its sources are deficient (citations missing, to the wrong paper, to a page that does not support the claim, or to a page that was never retrieved). |
| **0** | Wrong or no answer: a central claim (the number, entity, direction or verdict the question asks for) is wrong or contradicts the reference or the evidence, or the answer contains nothing toward any key point (including a full "the evidence does not establish this" on an answerable question), or it answers an unanswerable question as if the evidence established it. |

## How to decide

1. **List the key points.** Split the reference answer into atomic points (each number, entity, relation, caveat that the question asks for). Caveats the reference adds beyond the question (for example "the paper does not explain why") are optional unless the question asks for them.
2. **Mark each point** as present and correct, missing, or wrong. An honest "the passages do not say X" counts as missing, not wrong.
3. **Check sources.** Every claim taken from a paper needs a citation in the form `[paper, p.N]`. The packet gives a mechanical check: cited pages that lie outside every retrieved passage, and cited papers that were never retrieved. A cited page that differs from the gold evidence page is fine if the retrieved passage supports the claim. Claims from the SQL result need no citation. Material outside knowledge presented as if from the papers is a source deficiency.
4. **Score.**
   - Any central point wrong: **0**.
   - Nothing correct toward the question (full abstention, off-topic): **0**.
   - Some points correct, others missing, or sources deficient, nothing central wrong: **1**.
   - All points present, nothing wrong, sources sound: **2**.
   - A wrong or spurious claim that is peripheral (not what the question asks, does not change the answer) caps the score at **1** and is listed in `wrong_claims`.
   - Between 1 and 2 choose 1; between 0 and 1 choose 0 only if the central ask is wrong or absent.
5. **Insufficient-evidence questions** (`answerable = no`): **2** = explicitly says the evidence does not establish the answer and, where the reference says so, states what the paper does show, correctly and with a supporting citation; **1** = abstains but omits what the paper shows, or the support is miscited; **0** = gives a substantive answer as though established.
6. **Mixed questions** (text+table): both halves count. Both right = 2; one half right and nothing wrong = 1; any central half wrong = 0.
7. **Equivalent values** count as correct (rounding of the same figure, 86.57 vs 86.6, a table figure vs the same figure in the text). Different values for a number the question asks for are wrong, except where the notes say a second source is acceptable (Q02).

## Fields a grader returns (checked by `grade.py check`)

`question_id`, `label`, `score` (0, 1 or 2), `failure_mode`, `missing_points` (list), `wrong_claims` (list), `citation_issues` (list), `rationale` (one or two sentences).

`failure_mode` is one of `none`, `retrieval_miss` (the needed passage was not retrieved and the answer lacks it), `partial_retrieval`, `generation_error` (evidence was present but the answer misread or omitted it), `sql_error`, `over_abstention`, `abstention_failure`, `citation_error`, `other`. Use `none` only with score 2.

Consistency rules enforced by `check`: score 2 needs empty `missing_points`, `wrong_claims` and `citation_issues` and `failure_mode = none`; score 1 needs at least one of those lists non-empty; score 0 needs a non-empty `wrong_claims` or a failure mode of `over_abstention`, `abstention_failure`, `retrieval_miss` or `sql_error`.

## Calibration patterns (from the earlier 0-4 pass, restated on this scale)

- Two-part cross-paper question, one half answered exactly, the other half honestly "not in the passages": **1**.
- Everything asked is present and exact but two spurious extra rows or a stronger causal claim than the paper makes: **1**.
- Whole answer is "the passages do not establish this" on an answerable question: **0**.
- Correct abstention on an unanswerable question, quoting the paper's own statement and what it does report: **2**.
- Table answer that reproduces the reference query result exactly: **2**.
- A number the question asks for differs from the reference: **0**.

The 0-4 grades in `runs/baseline/grades.md` are superseded by this scale; they are not mapped mechanically.
