# Comparison of runs

| Group | runs/baseline_repeat | runs/chunk_paper | runs/chunk_paragraph_matched | runs/baseline | runs/chunk_paragraph | runs/no_embedding |
|---|---|---|---|---|---|---|
| all | 68.6% (n=35) | 84.3% (n=35) | 67.1% (n=35) | 67.1% (n=35) | 60.0% (n=35) | 87.1% (n=35) |
| text-involving | 62.5% (n=28) | 83.9% (n=28) | 62.5% (n=28) | 62.5% (n=28) | 53.6% (n=28) | 87.5% (n=28) |
| source: text-only | 57.1% (n=21) | 88.1% (n=21) | 61.9% (n=21) | 57.1% (n=21) | 50.0% (n=21) | 88.1% (n=21) |
| source: table-only | 92.9% (n=7) | 85.7% (n=7) | 85.7% (n=7) | 85.7% (n=7) | 85.7% (n=7) | 85.7% (n=7) |
| source: text+table | 78.6% (n=7) | 71.4% (n=7) | 64.3% (n=7) | 78.6% (n=7) | 64.3% (n=7) | 85.7% (n=7) |
| type: conceptual | 58.3% (n=6) | 91.7% (n=6) | 66.7% (n=6) | 50.0% (n=6) | 50.0% (n=6) | 91.7% (n=6) |
| type: cross-paper | 44.4% (n=9) | 83.3% (n=9) | 50.0% (n=9) | 44.4% (n=9) | 38.9% (n=9) | 83.3% (n=9) |
| type: cross-source | 78.6% (n=7) | 71.4% (n=7) | 64.3% (n=7) | 78.6% (n=7) | 64.3% (n=7) | 85.7% (n=7) |
| type: factual | 75.0% (n=4) | 87.5% (n=4) | 87.5% (n=4) | 75.0% (n=4) | 75.0% (n=4) | 100.0% (n=4) |
| type: insufficient-evidence | 75.0% (n=2) | 100.0% (n=2) | 50.0% (n=2) | 100.0% (n=2) | 50.0% (n=2) | 75.0% (n=2) |
| type: tabular | 92.9% (n=7) | 85.7% (n=7) | 85.7% (n=7) | 85.7% (n=7) | 85.7% (n=7) | 85.7% (n=7) |

Answers scoring below 2, by failure mode:

| Failure mode | runs/baseline_repeat | runs/chunk_paper | runs/chunk_paragraph_matched | runs/baseline | runs/chunk_paragraph | runs/no_embedding |
|---|---|---|---|---|---|---|
| citation_error | 1 | 0 | 0 | 0 | 0 | 0 |
| generation_error | 4 | 7 | 10 | 5 | 6 | 6 |
| other | 0 | 1 | 0 | 0 | 0 | 0 |
| partial_retrieval | 7 | 0 | 7 | 8 | 13 | 1 |
| retrieval_miss | 7 | 1 | 2 | 6 | 5 | 0 |
| sql_error | 1 | 2 | 2 | 2 | 2 | 2 |

Paired against runs/baseline (questions graded in both; mean score difference on the 0-2 scale, bootstrap 95% interval):

| Run | Questions | Mean difference | 95% interval | Better / same / worse |
|---|---|---|---|---|
| runs/baseline_repeat | 35 | +0.03 | -0.06 to +0.11 | 2 / 32 / 1 |
| runs/chunk_paper | 35 | +0.34 | +0.11 to +0.60 | 13 / 19 / 3 |
| runs/chunk_paragraph_matched | 35 | +0.00 | -0.17 to +0.17 | 5 / 25 / 5 |
| runs/chunk_paragraph | 35 | -0.14 | -0.31 to +0.03 | 3 / 24 / 8 |
| runs/no_embedding | 35 | +0.40 | +0.20 to +0.60 | 14 / 20 / 1 |

Paired against runs/no_embedding (questions graded in both; mean score difference on the 0-2 scale, bootstrap 95% interval):

| Run | Questions | Mean difference | 95% interval | Better / same / worse |
|---|---|---|---|---|
| runs/chunk_paper | 35 | -0.06 | -0.23 to +0.11 | 4 / 25 / 6 |

| ID | runs/baseline_repeat | runs/chunk_paper | runs/chunk_paragraph_matched | runs/baseline | runs/chunk_paragraph | runs/no_embedding |
|---|---|---|---|---|---|---|
| Q01 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q02 | 1 | 1 | 2 | 1 | 2 | 2 |
| Q03 | 2 | 2 | 2 | 2 | 1 | 2 |
| Q04 | 1 | 2 | 1 | 1 | 1 | 2 |
| Q06 | 1 | 2 | 1 | 1 | 1 | 2 |
| Q07 | 1 | 2 | 2 | 1 | 1 | 2 |
| Q08 | 1 | 1 | 1 | 1 | 1 | 2 |
| Q09 | 1 | 2 | 2 | 1 | 1 | 1 |
| Q11 | 1 | 2 | 1 | 1 | 1 | 2 |
| Q12 | 1 | 2 | 1 | 1 | 1 | 2 |
| Q13 | 1 | 2 | 2 | 1 | 1 | 2 |
| Q14 | 1 | 1 | 1 | 1 | 0 | 1 |
| Q15 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q16 | 0 | 2 | 0 | 0 | 0 | 1 |
| Q17 | 0 | 2 | 0 | 0 | 1 | 2 |
| Q18 | 1 | 2 | 1 | 2 | 1 | 1 |
| Q20 | 2 | 2 | 1 | 2 | 1 | 2 |
| Q21 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q23 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q24 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q25 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q27 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q29 | 2 | 1 | 1 | 1 | 1 | 1 |
| Q30 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q31 | 1 | 2 | 2 | 1 | 2 | 1 |
| Q32 | 2 | 1 | 1 | 2 | 1 | 2 |
| Q34 | 1 | 2 | 1 | 1 | 1 | 2 |
| Q35 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q37 | 2 | 1 | 2 | 2 | 1 | 2 |
| Q39 | 2 | 2 | 1 | 2 | 2 | 2 |
| Q40 | 2 | 1 | 1 | 2 | 1 | 2 |
| Q42 | 2 | 2 | 1 | 1 | 1 | 2 |
| Q43 | 1 | 1 | 1 | 1 | 1 | 2 |
| Q44 | 1 | 2 | 1 | 1 | 1 | 2 |
| Q45 | 2 | 2 | 2 | 2 | 1 | 2 |
