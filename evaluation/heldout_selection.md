# Held-out selection

10 of the 43 questions are marked `held-out` in the `split` column of `text_evaluation_candidates.xlsx`; the other 33 stay `development`. Set by `evaluation/set_split.py` (no other column was changed).

**Rule:** held-out questions are never used for tuning, prompt changes or failure-driven fixes. `src/evaluate.py` and `src/answer.py` run only `development` questions unless `--split held-out` is passed explicitly, which is not done until the final evaluation.

| ID | Source type | Type | Difficulty | Paper(s) |
|---|---|---|---|---|
| Q05 | text-only | factual | medium | FIRE-Bench |
| Q41 | text-only | cross-paper | medium | BatchNorm; ResNet |
| Q10 | text-only | conceptual | hard | EmbeddingLimits |
| Q19 | text-only | insufficient-evidence | medium | TemporalStraightening |
| Q22 | table-only | tabular | medium | none |
| Q26 | table-only | tabular | easy | none |
| Q28 | table-only | tabular | hard | none |
| Q33 | text+table | cross-source | hard | ViT |
| Q36 | text+table | cross-source | medium | ResNet |
| Q38 | text+table | cross-source | easy | ViT |

**Balance:** 4 text-only (one each factual, cross-paper, conceptual, insufficient-evidence), 3 table-only, 3 text+table; easy 2, medium 5, hard 3.

**Choices made:**
- None of the 8 manual-review questions is held out, so the held-out set has unambiguous ground truth.
- One of the three insufficient-evidence questions is held out (Q19); Q18 and Q20 stay in development.
- No paper loses all its development questions: BatchNorm and EmbeddingLimits keep one each (Q08, Q16), every other paper keeps two or more.

**Development set (33):** 19 text-only (including Q18, Q20 as insufficient-evidence), 7 table-only, 7 text+table.
