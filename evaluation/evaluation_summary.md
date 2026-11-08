# Evaluation Candidates — Summary

Companion to `text_evaluation_candidates.xlsx` (sheets: `Papers`, `Questions`, `Evidence`, `TabularData`, `TabularBenchmark`, `TabularEvidence`, `TabularDictionary`). The workbook holds 43 candidate questions over 15 papers: 23 text-only (Q01–Q20, six of which were replaced in the five-paper update, plus Q41–Q43), 10 table-only (Q21–Q30) and 10 text+table (Q31–Q40). Everything up to "Possible Structured Data Needs" describes the text-only set; **Part 2** (last section) describes the table-only and text+table questions and the timm dataset behind them, which the five-paper update did not touch. The plan and reasoning for the update are in `new_papers_review.md`.

Text answers and `Evidence` rows come from the PDFs only; table answers come from the timm result CSVs (`tabular_data/`). Page numbers are 1-based PDF page indices (they matched the printed page numbers in every page I spot-checked). Each quoted passage was checked programmatically against the text of its cited page (242 evidence rows across the 15 PDFs, 0 mismatches). `[...]` joins non-contiguous snippets from the same page.

> **Source location.** The 15 PDFs were not in `VIP RAG Research/papers/`. I read them from `~/Desktop/ML/Papers/`; `pdf_filename` in the `Papers` sheet uses those file names (e.g. `byolpaper.pdf`, `viTpaper.pdf`, `batchnorm_paper.pdf`, `SWE_bench.pdf`).

## Update: five additional papers (P11–P15)

| ID | Paper | Category | Questions |
|---|---|---|---|
| P11 | BatchNorm: Batch Normalization (Ioffe & Szegedy) | Training Methods | Q08, Q41 |
| P12 | Distillation: Distilling the Knowledge in a Neural Network (Hinton et al.) | Training Methods | Q13, Q18 |
| P13 | BabyCL: Continual Visual and Verbal Learning Through a Child's Egocentric Input (Jiang et al.) | Representation Learning | Q02, Q15 |
| P14 | MMLU: Measuring Massive Multitask Language Understanding (Hendrycks et al.) | Retrieval & Evaluation | Q42, Q43 |
| P15 | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (Jimenez et al.) | Retrieval & Evaluation | Q20, Q43 |

Six existing IDs were reused for new questions so that IDs stay stable and Q21–Q40 are untouched; the old content of those IDs is retired and its evidence rows were removed.

| ID | Retired question | New question |
|---|---|---|
| Q02 | MAE default masking ratio and rationale (easy, widely known) | BabyCL: 4AFC accuracy against baselines, and the text/Table 1 conflict |
| Q08 | ViT: pre-training data size vs ResNets (overlapped Q35) | BatchNorm: evidence for covariate-shift reduction vs what was measured |
| Q13 | BYOL vs I-JEPA: prediction task and augmentation dependence | Distillation x BYOL: where targets come from, labels, mean teacher |
| Q15 | ViT vs MAE: masked-patch pre-training | BabyCL x BYOL: augmentation probabilities and negative pairs |
| Q18 | EmbeddingLimits: dimension needed for 10M documents (reused Q10's passages) | Distillation: JFT accuracy after distilling the specialists (insufficient evidence) |
| Q20 | FIRE-Bench: novel scientific discovery (easy, answer guessable) | SWE-bench: agent-based resolve rate (insufficient evidence) |

Q41 (BatchNorm x ResNet: inference statistics and frozen BN in detection), Q42 (MMLU: parameter count vs fine-tuning and pretraining data) and Q43 (MMLU x SWE-bench x FIRE-Bench: contamination checks) were added. One further candidate, a SWE-bench retrieval question (BM25 vs oracle files), is documented in `new_papers_review.md` as a reserve and is not in the workbook.

## Overview of all 43 questions

| `data_source_type` | Questions | Count | easy / medium / hard | `manual_review_needed` = yes |
|---|---|---|---|---|
| text-only | Q01–Q20, Q41–Q43 | 23 | 2 / 12 / 9 | Q02, Q09, Q12 |
| table-only | Q21–Q30 | 10 | 2 / 5 / 3 | Q30 |
| text+table | Q31–Q40 | 10 | 1 / 5 / 4 | Q34, Q35, Q37, Q39 |
| **Total** | Q01–Q43 | **43** | **5 / 22 / 16** | **8** |

- `split` is `development` for all 43 rows; held-out questions will be picked by hand later.
- Answerable = yes: 40; answerable = no: 3 (Q18, Q19, Q20, all text-only).
- 14 of the original Q01–Q20 are unchanged since the first pass, and Q21–Q40 are unchanged (compared against a backup of the workbook). `Evidence` has 242 rows: 151 carried over and 91 new.
- Manual-review flags went from 9 to 8: Q13 and Q15 are gone with their questions and Q02 is new.
- **Decision (2026-11-08): keep 43.** The set is 3 questions over the earlier 40 on purpose: five new papers each get two questions (four of the nine new questions, Q13, Q15, Q41 and Q43, are also cross-paper with older papers), and only weak, redundant or flagged questions were removed. The option of dropping Q41, Q42 and Q04 to restore exactly 40 is documented in `new_papers_review.md` but was not taken.

## Question counts (text-only, 23)

| Type | Count | | Difficulty | Count |
|---|---|---|---|---|
| factual | 5 | | easy | 2 |
| conceptual | 6 | | medium | 12 |
| cross-paper | 9 | | hard | 9 |
| insufficient-evidence | 3 | | | |

- Answerable = yes: 20; answerable = no: 3 (Q18–Q20).
- Flagged `manual_review_needed = yes`: 3 (Q02, Q09, Q12). Q09 and Q12 are flagged for claim-vs-evidence or not-like-for-like comparisons; Q02 because the paper's own text and Table 1 give different numbers and the paper does not reconcile them. Reasons are in `notes`.

## Questions involving each paper

| Paper | Text-only | Text+table (Q31–Q40) | Total |
|---|---|---|---|
| Transformer | Q06, Q11 | — | 2 |
| ResNet | Q01, Q14, Q41 | Q32, Q36, Q40 | 6 |
| ViT | Q11, Q14 | Q31, Q33, Q35, Q37, Q38 | 7 |
| BYOL | Q07, Q13, Q14, Q15 | Q39 | 5 |
| MAE | Q12 | Q34 | 2 |
| I-JEPA | Q03, Q12 | — | 2 |
| TemporalStraightening | Q09, Q14, Q19 | — | 3 |
| EmbeddingLimits | Q10, Q16 | — | 2 |
| DailyOracle | Q04, Q16, Q17 | — | 3 |
| FIRE-Bench | Q05, Q17, Q43 | — | 3 |
| BatchNorm | Q08, Q41 | — | 2 |
| Distillation | Q13, Q18 | — | 2 |
| BabyCL | Q02, Q15 | — | 2 |
| MMLU | Q42, Q43 | — | 2 |
| SWE-bench | Q20, Q43 | — | 2 |

The ten table-only questions (Q21–Q30) need no paper. Every one of the 15 papers appears in at least 2 questions. MAE, BYOL and I-JEPA together appear in 6 of the 23 text-only questions (Q03, Q07, Q12, Q13, Q14, Q15), down from 7 of 20: MAE falls from three text-only questions to one and I-JEPA from three to two, while BYOL rises from three to four because two of the most natural links for the new papers (Distillation and BabyCL) run through it. ViT falls from 9 appearances to 7. Only ResNet, ViT, MAE and BYOL have text+table questions, because the timm table overlaps only those papers (see Part 2).

## What kind of retrieval challenges the text-only set creates

1. **Look-alike concepts across papers.** Masking (MAE random patches vs I-JEPA multi-block vs ViT's masked-patch prediction), "predict a target network's output" (BYOL vs I-JEPA vs Temporal Straightening's stop-gradient), "targets from another network" (distillation's soft targets vs BYOL's moving-average target vs mean teacher), and "Transformer encoder" (Transformer vs ViT). Q03, Q07, Q12, Q13 only work if retrieval attributes passages to the right paper.
2. **Answers split across prose, tables, appendices and papers.** Q01 (ResNet Table 2 vs the vanishing-gradient argument), Q06 (Table 1 vs the "n < d" condition on the next page), Q09 (claim on p. 7 vs Table 1 on p. 8), Q05 (task construction on pp. 3–5), and from the new papers Q08 (BatchNorm pp. 2, 5–7 plus the Figure 3 table), Q15 (BabyCL Appendix A vs BYOL Appendix B), Q41 (BatchNorm §3.1 vs ResNet Appendix A), Q42 (MMLU Table 1, §4.2 and Appendix A.1) and Q43 (MMLU Appendix B.2, SWE-bench p. 7, FIRE-Bench §5.4). Chunking that separates captions, tables and appendices from nearby prose will fail these.
3. **Claim vs what the experiments establish.** Several sources hedge ("hypothesize", "conjecture", "intuition", "suggests": Q07, Q08, Q12, Q42), and some text claims are stronger than the tables: Temporal Straightening says gains hold "across all models and environments" but some Table 1 rows drop (Q09). BatchNorm's covariate-shift story rests on one MNIST experiment while its ImageNet speed-ups bundle several other changes (Q08).
4. **Contradictory evidence inside one document.** BabyCL's text and Table 1 give different numbers for the same systems (Q02); SWE-bench's text names Claude 2 as best while its Table 5 also lists Claude 3 Opus (noted in Q20); the Transformer paper reports 41.8 BLEU (EN-FR) in its abstract and Table 2 but 41.0 in Section 6.1 (p. 8), not used as a question but a useful probe.
5. **Cross-paper needs citation resolution and non-comparable numbers.** Q14 requires mapping "He et al., 2015", "Dosovitskiy et al., 2021" and "Grill et al., 2020" to the supplied PDFs. Q12 tempts a "method A beats method B" answer from numbers that use different epochs. Q43's three contamination checks measure different things and cannot be ranked; Q15's matching augmentation probabilities are an observation about two documents, not a claim by BabyCL's authors.
6. **Insufficient-evidence questions sit next to tempting numbers.** Q18 invites answering with Table 3's specialist-ensemble accuracy although the paper says it has not shown distillation back into one network; Q19 invites extending simulated results to robots; Q20 invites importing agent results on SWE-bench that are widely known outside the corpus. Related passages will be retrieved — the correct behaviour is to say what is not established.

### New retrieval challenges from the five added papers

- **BatchNorm (Q08, Q41).** A hedged mechanism (an "expectation" and a "conjecture") next to measured but confounded speed-ups; the Figure 3 table is only extractable as a row sequence, and its two-column text interleaves under default extraction. Q41 pairs a §3.1 rule with a ResNet appendix passage whose stated reason (memory) is easy to replace with an invented one.
- **Distillation (Q13, Q18).** Temperature and soft targets are well known, so the test is whether the answer stays within what the paper reports; the JFT specialist numbers are ensemble results, not distilled-model results. BYOL's mean-teacher paragraph is the only place the two corpora share vocabulary.
- **BabyCL / egocentric continual learning (Q02, Q15).** A 2026 preprint with low outside-knowledge leakage but internal inconsistencies (text vs tables, buffer sampling, loss weighting, and whether the backbone starts from pretrained weights); useful for contradictory-evidence handling. Its link to BYOL runs through two appendices.
- **MMLU (Q42, Q43).** Results are split between the main text and an appendix, and the paper's own explanation of size effects is hedged; the contamination analysis lives in Appendix B.2, far from the abstract.
- **SWE-bench (Q20, Q43).** A 52-page paper whose agent results are absent but widely known elsewhere; the contamination check is a single paragraph and table on p. 7.
- **Cross-cutting.** Q43 requires one passage from each of three evaluation papers on the same theme; none of the three claims to rule contamination out.

## Quality-control pass for the five-paper update

| Check | Result |
|---|---|
| 1. Answer supported by cited passage | Each new reference answer was written from the PDF text and backed by evidence rows: 91 new rows (Q02 7, Q08 15, Q13 13, Q15 10, Q18 6, Q20 7, Q41 9, Q42 10, Q43 14). |
| 2. Page numbers | All 242 evidence quotes were re-verified against their cited PDF pages (default, layout and `-raw` extraction; `-raw` was needed for BatchNorm's two-column text and its figure-tables). Table 7 of SWE-bench was also read from the rendered page to confirm column order. |
| 3. Cross-paper really needs multiple papers | Q13, Q15, Q41 and Q43 need passages from every listed paper, and a script confirmed that each question's evidence papers equal its required papers. |
| 4. General-knowledge leakage | Tagged in `notes`: high for Q20 (later SWE-bench agent results are widely known), medium for Q08, Q13, Q41, Q42, low-medium for Q43, low for Q02, Q15, Q18. |
| 5. Ambiguity | Q02 is flagged because the paper's text and Table 1 disagree; its reference answer reports both. Q20 avoids quoting a single "best" SWE-bench figure because the text and Table 5 differ. One further quirk was noted but not used: BabyCL says it trains from scratch yet also describes a DINO ResNeXt-50 backbone and pretrained checkpoints, without saying how the backbone is initialized. |
| 6. Causal / superiority claims | Q42 states that its model comparisons are not controlled; Q43 states that the three checks are not comparable; Q13 and Q15 make no performance comparison. |
| 7. Paper diversity | Every paper has at least two questions; MAE/BYOL/I-JEPA share of text-only questions 7/20 to 6/23 (see above). |

Known limits: single-reviewer pass; the SWE-bench appendix (pp. 16–52) was skimmed rather than read line by line, and the BabyCL and BatchNorm figure-tables were verified through text extraction.

## Quality-control pass on the original Q01–Q20 (first pass)

*This table records the first-pass review. Q02, Q08, Q13, Q15, Q18 and Q20 were later replaced (see the five-paper update), so IDs in it that are among those six refer to the retired questions.*

| Check | Result |
|---|---|
| 1. Answer supported by cited passage | Re-read every answer against its evidence. Added about 40 evidence rows for answer claims that were not yet backed (e.g., ResNet zero-padded shortcuts, MAE spatial-redundancy rationale, Daily Oracle distractor step). Softened Q09 ("20–60%" is not stated as absolute or relative). |
| 2. Page numbers | All 167 quote snippets verified against the cited PDF page text (2 initial mismatches — a table-text artifact and a footnote marker — fixed). Section headings corrected where wrong (MAE "Reconstruction target" is §3, Weller §5.6, Oracle §4.1, Weller §2.3). |
| 3. Cross-paper really needs multiple papers | Q11, Q15, Q16, Q17 need both papers. Q12 and Q13 are partly answerable from the I-JEPA paper alone (it describes MAE/BYOL briefly) but the method details need the MAE/BYOL PDFs. Q14 was rewritten so the purpose of each reused component must come from the originating papers. |
| 4. General-knowledge leakage | Tagged per question in `notes`. Medium risk: Q01, Q02, Q06, Q07, Q08, Q11, Q12, Q13, Q20 (well-known papers). Reference answers were kept to what the PDFs state; document-specific numbers (Q01 Table 2, Q06 Table 1, Q10 critical-n, Q12/Q13 table values) are the real test. |
| 5. Ambiguity | Q09 (absolute vs relative gains), Q12 (66.9 vs 40.7 compare different epochs) and Q15 (different model sizes) flagged for manual review; Q13 flagged for non-comparable backbones. |
| 6. Causal / superiority claims | Answers repeat the papers' own hedges and state caveats explicitly (Q02, Q07, Q08, Q12, Q13, Q15). No answer claims one method is better under controlled conditions. |
| 7. Paper diversity | Draft concentrated on MAE/BYOL/I-JEPA; replaced an SSL "which is best?" insufficient-evidence draft with a FIRE-Bench question and replaced a residual-connection question with the Temporal Straightening reuse question (Q14). Final: 2–4 questions per paper. |
| 8. Retrieval challenges | See the five observations above; Q02/Q03, Q12, Q13 and Q15 target the user-requested confusable-method cases. |

Known limits: single-reviewer pass; table text extraction is imperfect for Transformer Table 1 and I-JEPA Tables 1–2, so those rows were matched against both extraction modes and should be eyeballed in the PDF when auditing.

## Possible Structured Data Needs

Quantitative comparisons that came up while reading and could motivate the later tabular dataset:

1. **Self-supervised ImageNet results across papers** — method, backbone, pre-training epochs, label fraction / protocol (linear probe, 1% labels, full fine-tune), top-1. Sources: BYOL Tables 1–2 (e.g. 74.3 ResNet-50 linear; 71.2 ResNet-200 2x at 1% labels), I-JEPA Tables 1, 2, 15 (e.g. 73.3 ViT-H/14 at 1% labels; 87.1 fine-tune vs MAE 87.8), MAE Table 3, ViT §4.6 (79.9). Protocols differ, so the protocol columns matter.
2. **Compute and training cost** — ViT TPUv3-core-days (Table 2), I-JEPA GPU hours (Fig. 1/5, "<1200 GPU hours"), MAE wall-clock speed-ups (Table 2), Transformer training FLOPs and hardware (Table 2, §5.2).
3. **Model-size / architecture specs** — ViT Base/Large/Huge (layers, hidden size, MLP size, heads, params), ResNet-18…152 FLOPs (Table 1), Transformer base vs big (Table 3).
4. **Benchmark results by model/setting** — Transformer BLEU (EN-DE, EN-FR) and parsing F1 (note the 41.8 vs 41.0 inconsistency), Daily Oracle yearly accuracy and YoY change pre/post knowledge cutoff per model (Table 3), FIRE-Bench agent precision/recall/F1 and per-task F1 (Table 3, §5.1).
5. **Retrieval-limit data** — LIMIT critical-n per embedding dimension (500k @512 … 250M @4096), recall@k by model and dimension (Figs. 3–4), qrel-pattern comparison (e.g. E5-Mistral 40.4 → 4.8 recall@100 on dense qrels).
6. **Planning success rates** — Temporal Straightening Table 1 (encoder × feature dim × curvature loss × environment × open-loop/MPC), and long-horizon Table 2.
7. **Evaluation-validation statistics** — Daily Oracle (annotators, sample size, Fleiss' kappa 0.26, 89.52% / 85.00% LLM-human agreement) and FIRE-Bench (33% sample; precision 0.95, recall 0.86, F1 0.89); dataset-size facts (Daily Oracle 16,783 TF + 14,727 MC; FIRE-Bench 30 core + 10 cross-domain + 60 parsed = 100 papers).

Mixed-source questions that would need both the text and the table: Q16/Q17 (retrieval and validation numbers across papers). The earlier mixed-source candidates Q13 (BYOL vs I-JEPA numbers) and Q15 (ViT vs MAE masked pre-training) were replaced in the five-paper update.

*Status after Part 2:* the timm table covers only the model-size and compute items for ResNet and ViT (items 2–3, inference side only) and one BYOL number comparison (item 1, via Q39). Items 4–7 (Transformer BLEU, Daily Oracle, FIRE-Bench, LIMIT critical-n, Temporal Straightening planning rates, evaluation-validation statistics) and the I-JEPA/MAE self-supervised tables have no structured source yet and remain text-only.

8. **Benchmarks added with the five papers** (listed only; no second table has been built) — SWE-bench resolve rates by model and retrieval setting (Tables 2, 5–7, 18–21), MMLU per-subject accuracy by model (Figs. 6 and 9, Table 1), BabyCL results across seven tables (4AFC, replay policy, buffer size, linear probe, VTWT, Baby Winoground), BatchNorm steps-to-accuracy (Fig. 3) and error rates (Fig. 4), and the distillation experiments (Tables 1, 3–5). Distillation-trained weights also appear as `dist` tags in the timm table, a possible later text+table link.

---

# Part 2 — Table-only and text+table questions (Q21–Q40)

## Dataset selected: timm result CSVs

- **Source:** PyTorch Image Models (timm) `results/` folder, https://github.com/huggingface/pytorch-image-models/tree/main/results, Apache-2.0. Pinned to commit `03b76b6ed7d98a844afc5529669b761b3ac5f562`; retrieved 2026-11-01.
- **Files:** unmodified copies in `tabular_data/raw/` (SHA-256 in `tabular_data/raw_checksums_sha256.txt`). `tabular_data/build_timm_db.py` rebuilds `tabular_data/timm_results.sqlite`; cleaning is limited to splitting `model` into `arch` + `weights_tag`, removing thousands separators from `param_count`, renaming columns and joining the per-dataset files on (`model`, `img_size`). Details: `tabular_data/README.md`; fields: `tabular_data/data_dictionary.md`.
- **Tables:** `model_results` (1,556 rows, one per model × image size: ImageNet validation top-1/top-5; Real, V2, Sketch, A and R top-1 and their differences; parameters) and `benchmark_infer` (1,627 rows per architecture × image size: throughput, batch size, GMACs, parameters; RTX 4090, AMP, PyTorch 2.9.1, CUDA 12.8). In the workbook they are the sheets `TabularData` and `TabularBenchmark`; `TabularDictionary` holds the field definitions.
- **Why it won** (comparison in `tabular_data_candidates.md`): official source with a pinned commit, flat CSVs that join cleanly, numbers that do not appear in the papers (so cross-source answers cannot come from the PDFs alone), and enough columns for filter, rank, group-by, window and dominance queries.
- **Rejected:** the Papers With Code archive (reaches more of the corpus, but mostly repeats numbers printed in the papers, has no I-JEPA rows, weaker provenance, nested parquet), the MTEB results repo (no LIMIT result files for the Weller et al. models, so it overlaps only that paper) and torchvision weight metadata (clean but only 115 weights).

## Overlap with the paper corpus

| Paper | Overlap with timm | Questions |
|---|---|---|
| ResNet | 77 result rows for resnet18/34/50/101/152 across 19 weight tags; benchmark rows for the same architectures | Q32, Q36, Q40 |
| ViT | Original Google checkpoints (`orig_in21k_ft_in1k`, 4 rows, one a ResNet-50 hybrid) plus AugReg variants and several patch sizes | Q31, Q33, Q35, Q37, Q38 |
| MAE | Indirect: 6 `hiera_*.mae_in1k_ft_in1k` rows. Hiera is not in the corpus; the link rests on the timm model card | Q34 |
| BYOL | No BYOL weights; only the ResNet-50 architecture, which BYOL's quoted ImageNet numbers refer to | Q39 |
| Transformer, I-JEPA, TemporalStraightening, EmbeddingLimits, DailyOracle, FIRE-Bench, BatchNorm, Distillation, BabyCL, MMLU, SWE-bench | None (distillation-trained weights exist as `dist` tags but no question uses them) | stay text-only |

## The 20 questions

Table-only (no paper needed; every one is marked "needs the table" in `notes`):

| ID | Focus | Operations | Difficulty | Review |
|---|---|---|---|---|
| Q21 | Top 3 ImageNet-Sketch top-1 among rows with ≤30M parameters, with their validation top-1 | filter, rank | medium | no |
| Q22 | Fastest row with validation top-1 ≥80% and ≤25M parameters (levit_256.fb_dist_in1k, 13,220 samples/s) | join, two-sided filter, rank | medium | no |
| Q23 | Smallest validation→Sketch drop among rows with top-1 ≥85% | filter, difference, rank | medium | no |
| Q24 | Five ResNet depths at 224 px: highest mean top-1 and largest 152-vs-18 gap by weight tag | group-by, HAVING, aggregate | medium | no |
| Q25 | Top-1 gained per added GMAC between consecutive a1_in1k ResNet depths | join, window (LAG), ratio | hard | no |
| Q26 | resnet50.a1_in1k at 224 vs 288 px: top-1, GMACs, throughput | paired comparison | easy | no |
| Q27 | tv_in1k ResNets: validation→ImageNet-V2 drop by depth | filter, difference | medium | no |
| Q28 | Rows in the validation top 10 but not the ImageNet-R top 10, with both ranks | two RANK windows | hard | no |
| Q29 | Best top-1 under 10M parameters, at ≤25M, and overall | three constrained rankings | easy | no |
| Q30 | Accuracy–throughput Pareto frontier at 224 px (26 of 783 rows; 11 with top-1 ≥85%) | join, NOT EXISTS | hard | **yes** |

Text+table (each has `Evidence` rows from the paper and a `TabularEvidence` row with the SQL; Q39 has two SQL statements):

| ID | Paper | Focus | Difficulty | Review |
|---|---|---|---|---|
| Q31 | ViT | Patch size 32/16/8: GMACs and throughput against the paper's sequence-length formula | medium | no |
| Q32 | ResNet | Paper Table 1 FLOPs vs timm GMACs (largest gap: resnet50, +8.2%) | medium | no |
| Q33 | ViT | Original-checkpoint hybrid vs plain ViT-B/16 at 384 px | hard | no |
| Q34 | MAE | MAE-tagged Hiera rows: robustness by size, plus the pre-training task the MAE paper describes | hard | **yes** |
| Q35 | ViT | AugReg in21k→in1k vs in1k-only pairs, against the paper's pre-training-data claim | hard | **yes** |
| Q36 | ResNet | Does top-1 rise with depth in every weight tag, against the paper's depth claim | medium | no |
| Q37 | ViT | ViT-B/16 vs ResNet-50/101/152 on top-1 and throughput, against the paper's pre-training-compute claim | hard | **yes** |
| Q38 | ViT | Paper Table 1 parameter counts vs timm (all within 1%) | easy | no |
| Q39 | BYOL | BYOL's 74.3 / 76.5 / 78.9 vs 18 timm resnet50 rows (18 / 17 / 13 at or above each) | medium | **yes** |
| Q40 | ResNet | resnet152 vs vgg16/vgg19: parameters, GMACs, throughput, top-1, against the paper's complexity claim | medium | no |

## What these questions test

1. **Routing.** The ten table-only questions cannot be answered from the PDFs or from general ML knowledge; a system that retrieves passages for them has the wrong plan.
2. **Splitting a question across sources.** Q31–Q40 need a claim or number from a paper and a measurement from the table, then a statement of what the table does and does not show. In Q31, Q33, Q35 and Q37 the paper's quantity (sequence length, hybrid scaling, pre-training data, pre-training compute) is not what timm measures, so the right answer is "consistent in direction" or "neither confirms nor refutes".
3. **Entity resolution.** ViT-B/16, L/16, H/14 and the "hybrid" naming rule must be mapped to timm architecture names (`vit_base_patch16_224`, `vit_base_r50_s16_384`); BYOL's ResNet-50 must be mapped to 18 `resnet50.*` rows.
4. **Join keys.** Results are keyed by (model, img_size); the benchmark is keyed by (arch, img_size) and has no weights tag, so all weights of an architecture share one throughput.
5. **Tempting verdicts.** Q37 ("ViT is more efficient than ResNet"), Q39 ("supervised ResNet-50s beat BYOL") and Q32/Q38 (explaining the paper–timm gaps) invite conclusions the data cannot support.

## Comparability and provenance concerns

- The rows are released weights, not controlled experiments: pre-training data, recipe and image size differ by `weights_tag`. No answer claims one method or architecture is better.
- Throughput comes from one RTX 4090 run, per architecture, with batch sizes of 512, 768 or 1024 depending on the row (hardware read from the file name).
- `top1_diff_a` and `top1_diff_r` are relative to clean accuracy on the same 200-class subset, not to `top1_val`.
- `results-imagenet-a.csv` lacks `resnet50.tv_in1k` and has one extra row (`resmlp_24_224.fb_dino`) with no validation row; `top1_a` is NULL for the former and the latter is not loaded. Raw files are untouched.
- Weight-tag meanings (tv_in1k, a1/a2/a3, orig/augreg, hiera `mae_in1k_ft_in1k`) come from timm's Hugging Face model cards, which are outside the corpus and the CSVs; no values were taken from them.
- timm's GMACs are for timm's own implementations; the paper's counts are for the original architectures, and neither source explains the differences in Q32 and Q38.
- The data is one snapshot (pinned commit); results at another commit may differ.

## Manual review (Part 2)

| ID | Why |
|---|---|
| Q30 | The frontier depends on single-GPU throughput at batch sizes that vary by row, and on which weight tag has the best top-1 for each architecture. |
| Q34 | The MAE link rests on the timm model card and tag name; the MAE PDF does not cover Hiera. Six rows of one family; all fine-tuned on ImageNet-1k at 224 px. |
| Q35 | The two tags are different training pipelines; only Small and Base sizes have pairs, so a size trend cannot be separated from architecture. Answer should say "consistent in direction", not "confirms". |
| Q37 | Asks for a yes/no on pre-training compute, which the table does not contain; ViT weights use ImageNet-21k pre-training while the ResNets use ImageNet-1k recipes. |
| Q39 | Compares a linear probe on self-supervised features with fully supervised weights; BYOL's 76.5 and 78.9 baselines are cited from other papers. |

(The three text-only flags are Q02, Q09 and Q12; see the text-only sections above.)

## Checks run on Part 2

- All 21 SQL statements in `TabularEvidence` were re-run against `timm_results.sqlite` from the text saved in the workbook; each reproduced the stored `supporting_rows_or_result`.
- The 29 new `Evidence` quotes (Q31–Q40) were checked against the cited PDF pages like the original 167: 196 of 196 matched when Part 2 was written, and after the five-paper update all 242 evidence rows match.
- `TabularData` (1,556 rows) and `TabularBenchmark` (1,627 rows) match the row counts in the database. The database's `model_metadata` table (521 rows) is loaded but not exported to the workbook and not used by any question.
- Known limits: single-reviewer pass; the answers to Q21–Q30 are query results on one snapshot, so they should be re-run if the table is rebuilt from a different commit.
