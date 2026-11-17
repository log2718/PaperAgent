# Retrieval-only metrics

28 text-involving development questions. Gold evidence = the workbook's (paper, page) pairs. A whole paper covers all its pages, so for paper-level configurations 'gold pages covered' equals the share of gold pairs whose paper was retrieved. `no_embedding` uses the router's logged choices.

| Configuration | Questions | Gold pages covered | Papers retrieved | MRR | Mean context tokens |
|---|---|---|---|---|---|
| token K=1 | 28 | 0.23 | 0.79 | 0.54 | 700 |
| token K=3 | 28 | 0.48 | 0.82 | 0.71 | 2,091 |
| token K=5 | 28 | 0.59 | 0.93 | 0.72 | 3,460 |
| token K=10 | 28 | 0.67 | 0.94 | 0.72 | 6,929 |
| token K=20 | 28 | 0.81 | 0.98 | 0.72 | 13,925 |
| paragraph K=1 | 28 | 0.20 | 0.74 | 0.57 | 149 |
| paragraph K=3 | 28 | 0.39 | 0.86 | 0.66 | 451 |
| paragraph K=5 | 28 | 0.48 | 0.90 | 0.68 | 751 |
| paragraph K=10 | 28 | 0.65 | 0.93 | 0.68 | 1,499 |
| paragraph K=20 | 28 | 0.74 | 0.96 | 0.69 | 2,930 |
| paper N=1 | 28 | 0.69 | 0.68 | 0.86 | 18,824 |
| paper N=2 | 28 | 0.93 | 0.93 | 0.91 | 39,408 |
| paper N=3 | 28 | 0.97 | 0.97 | 0.92 | 59,069 |
| paper N=5 | 28 | 0.99 | 0.99 | 0.92 | 94,106 |
| paragraph budget | 28 | 0.77 | 0.96 | 0.69 | 3,537 |
| no_embedding | 28 | 0.99 | 0.99 | 1.00 | 30,431 |

Gold pages covered by question type, at the default settings:

| Configuration | conceptual (n=6) | cross-paper (n=9) | cross-source (n=7) | factual (n=4) | insufficient-evidence (n=2) |
|---|---|---|---|---|---|
| token K=5 | 0.66 | 0.32 | 0.62 | 1.00 | 0.75 |
| paragraph K=5 | 0.54 | 0.15 | 0.57 | 0.88 | 0.62 |
| paragraph budget | 1.00 | 0.48 | 0.79 | 1.00 | 0.88 |
| paper N=3 | 1.00 | 0.92 | 1.00 | 1.00 | 1.00 |
| no_embedding | 1.00 | 0.97 | 1.00 | 1.00 | 1.00 |

Gold pages covered per question at the default settings:

| ID | Type | token K=5 | paragraph K=5 | paragraph budget | paper N=3 | no_embedding |
|---|---|---|---|---|---|---|
| Q01 | factual | 1.00 | 0.50 | 1.00 | 1.00 | 1.00 |
| Q02 | factual | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Q03 | factual | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Q04 | factual | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Q06 | conceptual | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 |
| Q07 | conceptual | 1.00 | 0.80 | 1.00 | 1.00 | 1.00 |
| Q08 | conceptual | 0.75 | 0.50 | 1.00 | 1.00 | 1.00 |
| Q09 | conceptual | 0.29 | 0.29 | 1.00 | 1.00 | 1.00 |
| Q11 | cross-paper | 0.17 | 0.33 | 0.67 | 1.00 | 1.00 |
| Q12 | cross-paper | 0.33 | 0.22 | 0.67 | 1.00 | 1.00 |
| Q13 | cross-paper | 0.33 | 0.17 | 0.33 | 1.00 | 1.00 |
| Q14 | cross-paper | 0.20 | 0.00 | 0.20 | 0.30 | 0.70 |
| Q15 | cross-paper | 0.29 | 0.14 | 0.57 | 1.00 | 1.00 |
| Q16 | cross-paper | 0.20 | 0.00 | 0.40 | 1.00 | 1.00 |
| Q17 | cross-paper | 0.50 | 0.00 | 0.50 | 1.00 | 1.00 |
| Q18 | insufficient-evidence | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Q20 | insufficient-evidence | 0.50 | 0.25 | 0.75 | 1.00 | 1.00 |
| Q31 | cross-source | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 |
| Q32 | cross-source | 0.67 | 0.67 | 1.00 | 1.00 | 1.00 |
| Q34 | cross-source | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| Q35 | cross-source | 0.67 | 0.67 | 1.00 | 1.00 | 1.00 |
| Q37 | cross-source | 1.00 | 0.67 | 1.00 | 1.00 | 1.00 |
| Q39 | cross-source | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Q40 | cross-source | 0.50 | 0.50 | 0.50 | 1.00 | 1.00 |
| Q42 | conceptual | 0.67 | 0.67 | 1.00 | 1.00 | 1.00 |
| Q43 | cross-paper | 0.17 | 0.17 | 0.33 | 1.00 | 1.00 |
| Q44 | conceptual | 0.75 | 0.50 | 1.00 | 1.00 | 1.00 |
| Q45 | cross-paper | 0.67 | 0.33 | 0.67 | 1.00 | 1.00 |

Questions with no gold page retrieved under every default configuration: none.
