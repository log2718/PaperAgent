# New papers review: BatchNorm, Distillation, BabyCL, MMLU, SWE-bench

Status: **plan written before any workbook edit**; the outcome of applying it is recorded in section 7. Sources are the five PDFs in `~/Desktop/ML/Papers/` (`batchnorm_paper.pdf`, `Distill_Knowledge.pdf`, `Continual_learning_child.pdf`, `MMLU_paper.pdf`, `SWE_bench.pdf`). Every supporting passage quoted below was checked programmatically against the text of its cited PDF page (100 passages, 0 mismatches); page numbers are 1-based PDF pages and matched the printed numbers. `[...]` joins non-contiguous snippets from the same page.

## Recommendation in brief

- Add the five papers as P11-P15 and select **9 of the 10 candidates**. The reserve candidate (SW1, a SWE-bench retrieval question) is documented but not placed in the workbook.
- Replace **6** existing text-only questions (Q02, Q08, Q13, Q15, Q18, Q20); the new questions take over those IDs. Three further questions are added as Q41-Q43.
- Result: **43 questions** (23 text-only, 10 table-only, 10 text+table), up 3 from 40. The reason is coverage: five new papers each get two questions, four of the nine (Q13, Q15, Q41, Q43) are cross-paper with older papers (so they also strengthen those papers), and only questions that were weak, redundant or flagged were removed. Section 5 shows how to land on exactly 40 if you prefer.
- Q21-Q40, the timm database and all other sheets are untouched.

## 1. Reading notes

All five PDFs are complete (page counts 11, 9, 15, 27 and 52; each last page ends inside its own appendix or reference list; every figure and table number has a caption).

### P11 BatchNorm
*Ioffe & Szegedy, arXiv:1502.03167v3, 11 pp.*

- **Main contribution:** Normalizes each activation over the mini-batch with learned scale and shift (Alg. 1), motivated as reducing 'internal covariate shift'; allows much higher learning rates, less careful initialization, acts as a regularizer, and makes saturating nonlinearities trainable.
- **Method / design:** BN placed before the nonlinearity, bias dropped, convolutional layers normalize over all spatial locations with per-feature-map scale and shift (Sec. 3.2); inference uses population statistics (Alg. 2, Sec. 3.1).
- **Important experiments:** MNIST activation study (Fig. 1); ImageNet with Inception variants (Fig. 2-3: BN-x5 reaches 72.2% in 14x fewer steps, BN-x30 74.8%, sigmoid variant 69.8%); ensemble of 6 reaches 4.9% top-5 validation error (4.82% test).
- **Limitations / caveats (from the paper):** Covariate-shift reduction is measured only on MNIST; the Jacobian argument is a conjecture and the effect on gradient propagation 'remains an area of further study'; ImageNet speed-ups bundle several non-BN changes; RNNs and domain adaptation are future work.
- **Relationships to the corpus:** ResNet adopts BN after each convolution, lists BN-Inception in its Tables 4-5, and fixes BN statistics for detection. BYOL attributes its small-batch degradation to BN layers.
- **Document notes:** Two-column text interleaves in default extraction; `pdftotext -raw` used for verification. The figure-tables (Figs. 3-4) are quoted from raw order.

### P12 Distillation
*Hinton, Vinyals & Dean, arXiv:1503.02531v1, 9 pp.*

- **Main contribution:** 'Distillation': train a small model on the temperature-softened class probabilities of a large model or ensemble; matching logits is a special case; plus ensembles of specialist models for very large label sets.
- **Method / design:** Softmax with temperature T (Eq. 1); weighted soft-target and hard-label objectives; gradient analysis (Sec. 2.1); specialists with a dustbin class chosen by clustering confusable classes; KL-based inference over active specialists.
- **Important experiments:** MNIST (67 / 146 / 74 test errors; omitted-digit-3 experiment: 206 errors, 109 after a bias correction); speech acoustic model (Table 1: 58.9 / 61.1 / 60.8 frame accuracy, over 80% of the ensemble gain transferred); JFT with 61 specialists (Table 3: 25.0% to 26.1% top-1); soft targets as regularizers (Table 5: 44.5% vs 57.0% from 3% of the data).
- **Limitations / caveats (from the paper):** Distilling the specialists back into one network is not shown; the soft-target fix for specialist overfitting is still being explored; JFT is an internal dataset; the WER gain is smaller than the frame-accuracy gain.
- **Relationships to the corpus:** BYOL discusses mean teacher (teacher/student, slow-moving average) as related work; I-JEPA and MAE cite DeiT's 'distillation through attention' only in their references. The timm table has distillation-trained weights tags (possible later text+table link, not used here).
- **Document notes:** Complete 9 pp.; no extraction problems.

### P13 BabyCL
*Jiang, Yang, Norman, Lake & Ren, arXiv:2606.05115v1, 15 pp.*

- **Main contribution:** BabyCL: continual visual-and-verbal learning from SAYCam in a single chronological pass, combining streaming visual self-supervision (temporal segmentation, two-tier replay) with an image-text contrastive loss on a shared ResNeXt-50, using dual replay buffers.
- **Method / design:** Three losses (SimCLR instance loss, event-segment classification, symmetric InfoNCE cross-modal), equal per-loss weights (Eq. 1), resampling at insertion (k = 4 or 8), buffers of 10% / 50% of the stream.
- **Important experiments:** Labeled-S 4AFC (Table 1), multimodal fraction (Table 2), replay policy (Table 3), buffer size (Table 4), linear probes (Table 5), VTWT (Table 6), Baby Winoground (Table 7), nearest-neighbour retrieval and Grad-CAM++.
- **Limitations / caveats (from the paper):** A gap to offline CVCL remains; the replay buffers are large relative to the stream; more compositionality benchmarks are needed.
- **Relationships to the corpus:** BYOL: matching blur/solarization probabilities and the negative-pair question. I-JEPA, MAE: label-free visual representation learning. Temporal Straightening cites Memory Storyboard, the streaming method BabyCL builds on.
- **Document notes:** Internal inconsistencies noted for manual review: text vs Table 1 values; Sec. 4.3 range vs Table 3; Sec. 3 'sample equally from the two buffers' vs the Appendix (96 SSL frames : 32 multimodal) and Table 2; Eq. 1 vs 'weighted equally'; 'trained from scratch' (Sec. 1) vs 'DINO ResNeXt-50 vision backbone' and 'pretrained vision backbones' (App. A, C), with the initialization left unspecified.

### P14 MMLU
*Hendrycks et al., ICLR 2021, arXiv:2009.03300v3, 27 pp.*

- **Main contribution:** A 57-task multiple-choice test of knowledge and problem solving (15,908 questions: 5 dev per subject, 1,540 validation, 14,079 test) evaluated zero-shot and few-shot, to measure what models learn in pretraining.
- **Method / design:** Four-option questions from freely available exam and textbook sources; prompt ends 'Answer:'; prediction is the highest-probability token among A-D; accuracy averaged over all questions.
- **Important experiments:** GPT-3 few-shot 43.9% (175B) vs near random for the smaller sizes; UnifiedQA 48.9%; per-task range (about 69% to 26% for GPT-3); calibration up to 24% off; law-specialization attempt (32.8% with 2,000 extra examples, 36.1% after pretraining on 1.6M legal summaries); contamination check (App. B.2).
- **Limitations / caveats (from the paper):** Every model is below expert level on every task; text-only; related text may still have been seen in pretraining; unclear whether scaling alone will solve the test; humans: 34.5% (Mechanical Turk) and an estimated 89.8% expert level.
- **Relationships to the corpus:** SWE-bench and FIRE-Bench address leakage and verification differently (see Q43). SWE-bench's 'Hendrycks et al., 2021' citation is APPS (its reference list), not MMLU, so no SWE-bench critique of MMLU is assumed.
- **Document notes:** Complete 27 pp.; pp. 15-27 are the task table and one example per task.

### P15 SWE-bench
*Jimenez et al., ICLR 2024, arXiv:2310.06770v3, 52 pp.*

- **Main contribution:** 2,294 real GitHub issue-PR task instances from 12 Python repositories, scored by executing the repository's tests; also SWE-bench Lite (300), SWE-bench-train (19,000 instances from 37 repositories) and fine-tuned SWE-Llama 7b/13b.
- **Method / design:** Three-stage construction (scrape about 90,000 PRs, attribute filter, execution filter requiring a fail-to-pass test); the model gets the issue and a codebase (BM25-retrieved or oracle files) and returns a patch; resolved if the patch applies and all tests pass.
- **Important experiments:** BM25 vs oracle retrieval; resolve rate falls as context grows although recall rises (Tables 2-3); oracle-collapsed ablation (Table 6); before/after-2023 split (Table 7); patch vs whole-file generation; patch-size statistics; qualitative error analysis.
- **Limitations / caveats (from the paper):** Python only; baselines are simple single-pass approaches (agents are future work); execution tests alone do not guarantee quality; some issues embed images.
- **Relationships to the corpus:** FIRE-Bench (agentic, executable verification; contamination check), Daily Oracle (continual refresh to avoid leakage), Daily Oracle and EmbeddingLimits (BM25), MMLU (leakage).
- **Document notes:** Complete 52 pp.; main text (pp. 1-11) read in full, appendix skimmed (construction, per-repository and temporal tables, qualitative examples). Text names Claude 2 (1.96%) as best while Table 5 also lists Claude 3 Opus (3.79%).

## 2. New paper coverage: the ten candidates

Each candidate lists its target ID, type, difficulty, required papers, answerability, review flag, a concise reference answer and why it is useful. The exact supporting passages (page, section, quote) for all ten are in the appendix. Full reference answers and evidence rows for the nine selected candidates go into the workbook.

### P11 BatchNorm

**BN1 (selected; target ID Q08)** What evidence does the Batch Normalization paper give that batch normalization reduces internal covariate shift, how large is the training speed-up it reports on ImageNet (and what else was changed besides adding BN), and what does the paper itself say it has not established?

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| conceptual | medium | BatchNorm | yes | no | Q08 |

- **Concise reference answer:** Covariate-shift reduction is shown directly only on MNIST (sigmoid inputs more stable with BN, higher test accuracy). On ImageNet, BN-Baseline matches Inception's 72.2% in 13.3M vs 31.0M steps, BN-x5 in 2.1M (14x fewer), BN-x30 peaks at 74.8%, BN-x5-Sigmoid reaches 69.8% where Inception+sigmoid never beats 1/1000. The fast variants also raise the learning rate, drop Dropout, cut L2 5x, decay the rate 6x faster, etc., so speed-ups are not BN alone. The mechanism is an 'expectation' and 'conjecture'; the effect on gradient propagation 'remains an area of further study'.
- **Why it is useful:** Tests whether a system separates a paper's hypothesis from what it measured: the covariate-shift claim rests on one small experiment and the headline speed-ups bundle several changes. Evidence is spread over four pages and a figure-table.
- **Ambiguity / comparability:** Claim-vs-evidence question: covariate-shift reduction is shown only on MNIST, and the ImageNet gains are confounded with the other training changes listed in Sec. 4.2.1. Retrieval challenge: the evidence is spread over pp. 2 and 5-7, including the Figure 3 table. [General-knowledge risk: medium.]

**BN2 (selected; target ID Q41)** The Batch Normalization paper says that once a network is trained, BN should no longer use mini-batch statistics. What does it use instead, and how does the ResNet paper handle its BN layers when fine-tuning for object detection, and why?

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| cross-paper | medium | BatchNorm; ResNet | yes | no | - |

- **Concise reference answer:** BatchNorm: batch-dependent normalization is 'neither necessary nor desirable during inference'; a trained network uses population statistics, so BN becomes a fixed linear transform per activation. ResNet (Appendix A): computes BN statistics on the ImageNet training set after pre-training, then fixes the BN layers during detection fine-tuning (they act as linear layers with constant offsets and scales), mainly to reduce memory in Faster R-CNN training.
- **Why it is useful:** Needs one passage from each paper, and the ResNet one is in an appendix far from where ResNet introduces BN. Checks that the reason (memory) is reported rather than an invented one.
- **Ambiguity / comparability:** Cross-paper: the BatchNorm paper supplies the inference-time rule, the ResNet paper a concrete use in an appendix; ResNet cites BN [16] for its architecture (p. 4) but does not restate the formula. The stated reason is memory, so an answer should not claim an accuracy reason. Retrieval challenge: the ResNet passage sits in Appendix A (p. 10), far from where ResNet introduces BN. [General-knowledge risk: medium.]

### P12 Distillation

**KD1 (selected; target ID Q13)** Distillation and BYOL both train one network to match another network's outputs. According to the two papers, what supplies the targets in each case and how does that target model come about, are labels used, and what does BYOL say about the 'mean teacher' method that it treats as closest to its slow-moving-average target?

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| cross-paper | hard | Distillation; BYOL | yes | no | Q13 |

- **Concise reference answer:** Distillation: targets are temperature-softened class probabilities of an already-trained cumbersome model (ensemble or very large regularized net); labels enter as a lower-weighted second cross-entropy term. BYOL: targets are a target network's projections of another augmented view; the target is an exponential moving average of the online network, with stop-gradient and an online-only predictor; no labels or negative pairs. BYOL says mean teacher also uses a slow-moving-average teacher but adds a classification loss and collapses without it, whereas BYOL's predictor prevents collapse.
- **Why it is useful:** A natural conceptual link (targets from another network) whose answer needs both papers' mechanisms, including BYOL's own mean-teacher paragraph. Guards against 'BYOL is just distillation'.
- **Ambiguity / comparability:** Conceptual cross-paper link built from each paper's own description: the distillation paper never mentions self-supervised methods, and BYOL uses 'teacher/student' wording only for mean teacher. Do not claim that BYOL 'is' distillation; the targets differ (a fixed, already-trained larger model versus a moving average of the learner). BYOL results are on ImageNet, distillation results on MNIST, speech and JFT, so no performance comparison is implied. [General-knowledge risk: medium.]

**KD2 (selected; target ID Q18)** According to the distillation paper, what accuracy does a single network reach on the JFT dataset after the knowledge in the specialist models has been distilled back into it?

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| insufficient-evidence | medium | Distillation | no | no | Q18 |

- **Concise reference answer:** Not established. JFT results are for a generalist plus 61 specialists combined at inference (top-1 25.0% to 26.1%, 4.4% relative gain); the authors state they 'have not yet shown' that the specialists can be distilled back into one net and are 'currently exploring' a related idea. Distillation itself is reported only on MNIST and speech.
- **Why it is useful:** Insufficient-evidence test with an explicit sentence in the paper and a tempting nearby number (Table 3's specialist-ensemble result).
- **Ambiguity / comparability:** Insufficient-evidence trap: Table 3's specialist numbers are ensemble results and tempt the answer '26.1%'. A correct response separates the ensemble result from the distillation step the authors say they have not shown. [General-knowledge risk: low.]

### P13 BabyCL

**CL1 (selected; target ID Q02)** How does BabyCL's Labeled-S 4AFC accuracy compare with the offline CVCL upper bound and with the one-pass and compute-matched streaming baselines, and do the numbers in the text match those in Table 1?

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| factual | hard | BabyCL | yes | yes | Q02 |

- **Concise reference answer:** Table 1: Offline CVCL 57.31, One-pass 27.52, CL-CVCL 36.41, BabyCL k=4 41.08, k=8 43.38. BabyCL beats the matched-budget baseline and narrows, but does not close, the gap to offline training. The text gives different values (25.68, 35.32, 44.46, 57.45) and a 2.6-point k=4-to-8 gain (Table 1: 2.30); the paper does not reconcile them.
- **Why it is useful:** Contradictory evidence inside one document (text vs table). Tests whether a system reports both values or flags the conflict; a 2026 preprint, so little outside-knowledge leakage.
- **Ambiguity / comparability:** MANUAL REVIEW: the text and Table 1 report different values for the same systems and the paper does not reconcile them, so the reference answer reports both; a system should give both sets or flag the conflict rather than silently choose one. Related inconsistencies, not needed for grading: Sec. 4.3 says the four replay policies fall within 43.90%-44.46% while Table 3 lists values up to 45.00, and the 45.00 in Tables 2-4 matches Table 2's 'Best' column rather than Table 1's mean. [General-knowledge risk: low (2026 preprint).]

**CL2 (selected; target ID Q15)** BabyCL's visual branch applies strong augmentations to two views of each frame. Compare the Gaussian-blur and solarization probabilities it uses for its two views with those BYOL uses for its two views, and say what the two papers report about whether negative pairs are needed.

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| cross-paper | hard | BabyCL; BYOL | yes | no | Q15 |

- **Concise reference answer:** BabyCL (App. A): blur probability 1.0 on view 1 and 0.1 on view 2, solarization 0.2 on view 2, grayscale 0.2, crop scale 0.2-1.0. BYOL (App. B, Table 6): blur 1.0/0.1, solarization 0.0/0.2, grayscale 0.2, crops 8%-100%. Blur, solarization and grayscale probabilities match; crop lower bound differs; BabyCL does not cite BYOL. BabyCL uses SimCLR and InfoNCE losses and cites Zhuang et al. (negatives most effective on SAYCam); BYOL reports state of the art without negative pairs. Neither paper tests BYOL's objective in BabyCL's setting.
- **Why it is useful:** Two appendices from two papers must be matched on specific parameters; also tests restraint, since the similarity is not claimed by the authors and no performance inference is supported.
- **Ambiguity / comparability:** Cross-paper comparison drawn from two appendices. BabyCL's reference list does not include BYOL, so the similarity is an observation about the two documents, not a claim by the authors; color-jitter strengths are parameterised differently and are deliberately not compared. Do not infer that BYOL's objective would or would not work in BabyCL's setting. [General-knowledge risk: low.]

### P14 MMLU

**MM1 (selected; target ID Q42)** Does the MMLU paper attribute its models' accuracy mainly to parameter count? Use its GPT-3, UnifiedQA and smaller fine-tuned model comparisons.

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| conceptual | medium | MMLU | yes | no | - |

- **Concise reference answer:** Not mainly. Few-shot GPT-3: three smaller sizes near random (25.9/24.9/26.0), 175B reaches 43.9%. UnifiedQA (11B, fine-tuned on other QA data) reaches 48.9% and its 60M variant ~29.3%; in Appendix A.1 it beats RoBERTa-base (27.9%) and ALBERT-xxlarge (27.1%) with fewer parameters, and UnifiedQA-3B (43.7%) beats GPT-2 (32.4%). Authors: size is key but fine-tuning also helps; larger pretraining data 'suggests' the gap. Models and regimes differ, so not a controlled test.
- **Why it is useful:** Numbers sit in Table 1, Section 4.2 and Appendix A.1; the paper's own explanation is hedged, so the answer must not claim a controlled finding.
- **Ambiguity / comparability:** Claim-vs-evidence: the paper's explanation is hedged ('suggests') and the comparisons are not controlled. Retrieval challenge: the numbers are split across Table 1 (p. 5), Section 4.2 (p. 6) and Appendix A.1 (p. 12). [General-knowledge risk: medium (MMLU and GPT-3 results are widely discussed).]

**MM2 (selected; target ID Q43)** MMLU, SWE-bench and FIRE-Bench each have to worry that a model may have seen benchmark content during training. What check does each paper run, what does it find, and how strongly does each paper state its conclusion?

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| cross-paper | hard | MMLU; SWE-bench; FIRE-Bench | yes | no | - |

- **Concise reference answer:** MMLU (App. B.2): accuracy and question entropy are not positively correlated (r = -0.43 zero-shot, -0.56 few-shot), which 'suggests' exact questions were not memorized; related text was still seen via Wikipedia. SWE-bench (Sec. 5): before/after-2023 resolve rates differ little for most models (GPT-4 the exception, 25% subset); 'largely promising'. FIRE-Bench (Sec. 5.4): no consistent advantage for pre-cutoff tasks; 'suggests the absence of a strong contamination signal rather than proving its absence'. Different checks, none conclusive, not comparable.
- **Why it is useful:** Three papers, one theme (benchmark leakage), three different checks with different levels of hedging; requires an appendix, a results paragraph and a discussion section.
- **Ambiguity / comparability:** Three papers, three different checks, each hedged to a different degree; the evidence sits in an appendix (MMLU B.2, pp. 13-14), the results section (SWE-bench p. 7) and Section 5.4 (FIRE-Bench pp. 8-9). The SWE-bench GPT-4 column is a 25% random subset. Do not rank the benchmarks by contamination risk. [General-knowledge risk: low-medium.]

### P15 SWE-bench

**SW1 (**reserve (not placed in the workbook)**; target ID none)** In SWE-bench's baseline experiments, how are files chosen as model context (BM25 versus an 'oracle'), and what does the paper find about whether giving the model more retrieved context helps?

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| conceptual | medium | SWE-bench | yes | no | - |

- **Concise reference answer:** Baselines retrieve files with BM25 (13k/27k/50k tokens) or use an 'oracle' of the reference patch's files. BM25 recall of oracle files rises (29.58/44.41/51.06 average) but Claude 2's resolve rate falls (1.96/1.87/1.22); models localize poorly. Oracle: Claude 2 4.8%; oracle-collapsed lifts GPT-4 1.3% to 3.4% and Claude 2 to 5.9%.
- **Why it is useful:** Directly relevant to RAG evaluation: higher retrieval recall did not give better answers. Kept as a reserve because SWE-bench already appears in Q20 and Q43.
- **Ambiguity / comparability:** Retrieval-relevant result for a RAG evaluation set: higher recall did not mean better answers. Reserve candidate, not placed in the workbook (SWE-bench already appears in Q20 and Q43). Table 5 in this version also lists Claude 3 Opus, so avoid calling Claude 2 'the best model'. [General-knowledge risk: low-medium.]

**SW2 (selected; target ID Q20)** According to the SWE-bench paper, what resolve rate do agent-based systems (models that run code, navigate the repository and iterate) reach on SWE-bench?

| Type | Difficulty | Required papers | Answerable | Manual review | Replaces |
|---|---|---|---|---|---|
| insufficient-evidence | easy | SWE-bench | no | no | Q20 |

- **Concise reference answer:** Not established. The paper evaluates single-pass LMs given BM25 or oracle files; main-text resolve rates are single-digit (Claude 2 4.8% with oracle retrieval). Agents appear only as a 'level playing field' use and as future work; no agent results are reported.
- **Why it is useful:** Abstention test where outside knowledge is widely available (later agent results), so a system that imports it should fail.
- **Ambiguity / comparability:** Insufficient-evidence trap: results for later agent systems on SWE-bench are widely known outside the corpus and a system may import them. The paper's text names Claude 2 (1.96%) as best while its Table 5 also lists Claude 3 Opus at 3.79%, so the reference answer avoids a single 'best' figure. [General-knowledge risk: high.]

## 3. Review of the existing Q01-Q20

Criteria: redundancy, concentration on MAE/BYOL/I-JEPA, retrieval value, answerable from general ML knowledge, ambiguity, evidence quality, overlap with stronger new questions. Overlaps with Q21-Q40 were also checked (those questions are not edited).

| ID | Papers | Assessment | Verdict |
|---|---|---|---|
| Q01 | ResNet | Strong: Table 2 numbers separated from the prose; document-specific. Its vanishing-gradient half is why BN x ResNet was built on BN's inference rule instead. | Keep |
| Q02 | MAE | Easy; the 75% masking ratio is widely known; MAE already has Q12 and Q34, and Q34's reference answer restates the same 75% passage. | **Replace** |
| Q03 | I-JEPA | Document-specific hyperparameters, low leakage; I-JEPA otherwise appears only in Q12. | Keep |
| Q04 | DailyOracle | Easy factual with exact counts; the only easy slot among the Daily Oracle questions. | Keep |
| Q05 | FIRE-Bench | Multi-page methodology answer; good chunking test. | Keep |
| Q06 | Transformer | Good Table 1 plus prose test; one of only two Transformer questions. | Keep |
| Q07 | BYOL | Strong, hedged conceptual question; hypothesis vs ablation. | Keep |
| Q08 | ViT | ViT is the most-used paper (9 of 40 questions), and Q35 (text+table) already uses the same 'large-scale training trumps inductive bias' passage; medium leakage risk. | **Replace** |
| Q09 | TemporalStraightening | Strong claim-vs-table question; flagged for the 'all models and environments' wording; no better substitute. | Keep (flag stays) |
| Q10 | EmbeddingLimits | Strong theory question; its passages are reused by Q18. | Keep |
| Q11 | Transformer; ViT | Only cross-paper question for the Transformer; reference answer restricted to the PDFs. | Keep |
| Q12 | MAE; I-JEPA | Flagged for non-comparable epochs, but it is the only masking-confusion test and the only MAE text question left after Q02/Q15 are replaced. | Keep (flag stays) |
| Q13 | BYOL; I-JEPA | Same structure as Q12 and Q07 (predict a target network's output); flagged for non-like-for-like numbers; adds BYOL/I-JEPA concentration. | **Replace** |
| Q14 | TemporalStraightening; ResNet; ViT; BYOL | Rewritten earlier to need the originating papers; strong. | Keep |
| Q15 | ViT; MAE | Flagged (not like-for-like); ViT/MAE concentration; ViT's masked-patch experiment is preliminary, so the answer is mostly hedging. | **Replace** |
| Q16 | DailyOracle; EmbeddingLimits | BM25 link is modest but explicit in both papers. | Keep |
| Q17 | DailyOracle; FIRE-Bench | Two validation setups with exact agreement numbers; no overlap with the new items. | Keep |
| Q18 | EmbeddingLimits | Insufficient-evidence variant built on Q10's passages (redundant evidence); Embedding Limits keeps Q10 and Q16. | **Replace** |
| Q19 | TemporalStraightening | Clear simulated-vs-real trap; keep as the one retained insufficient-evidence question. | Keep |
| Q20 | FIRE-Bench | Easy; 'No' is the default guess; FIRE-Bench's scope is better covered by Q05, Q17 and the new Q43. | **Replace** |

Concentration: before, 7 of the 20 text-only questions involved MAE, BYOL or I-JEPA (Q02, Q03, Q07, Q12, Q13, Q14, Q15). After the plan, 6 of 23 do (Q03, Q07, Q12, Q13, Q14, Q15): MAE falls from three text-only questions to one and I-JEPA from three to two, but BYOL rises from three to four because two of the most natural links for the new papers (Distillation, BabyCL) run through it. ViT falls from 9 appearances across the full set to 7.

## 4. Proposed replacement plan

| Existing ID | Why remove | Proposed new question | Why it improves the set |
|---|---|---|---|
| Q02 | easy, general-knowledge, MAE-heavy; overlaps Q34 | Q02 <- BabyCL 4AFC results and the text/Table 1 conflict (factual, hard, review) | Replaces a widely known fact with a document-specific question on a 2026 preprint and adds contradictory-evidence handling. |
| Q08 | ViT-heavy; same passage as Q35 | Q08 <- BatchNorm: evidence for covariate-shift reduction vs what was measured (conceptual, medium) | Moves a conceptual slot from the most-used paper to a hedged-claim question on a new paper (Training Methods). |
| Q13 | redundant SSL cross-paper; flagged | Q13 <- Distillation x BYOL: where targets come from, labels, mean teacher (cross-paper, hard) | Different mechanism from Q12; needs both papers' own descriptions; no numeric comparison to misread. |
| Q15 | flagged; ViT/MAE concentration | Q15 <- BabyCL x BYOL: augmentation probabilities and negative pairs (cross-paper, hard) | Verifiable parameters from two appendices instead of non-comparable accuracy numbers. |
| Q18 | evidence duplicates Q10 | Q18 <- Distillation: JFT accuracy after distilling specialists (insufficient-evidence, medium) | Keeps three abstention questions with no shared passages. |
| Q20 | easy; answer guessable | Q20 <- SWE-bench: agent-based resolve rate (insufficient-evidence, easy) | Abstention test where outside results are widely known. |

New IDs for the remaining selected candidates (existing IDs are kept, so these go after Q40):

| New ID | Question | Why added rather than swapped in |
|---|---|---|
| Q41 | BatchNorm x ResNet: inference-time statistics and ResNet's frozen BN in detection (cross-paper, medium) | Second BatchNorm question; cross-paper with an old paper |
| Q42 | MMLU: is accuracy attributed to parameter count? (conceptual, medium) | First of two MMLU questions |
| Q43 | MMLU x SWE-bench x FIRE-Bench: contamination checks (cross-paper, hard) | Second MMLU and second SWE-bench question; also adds a FIRE-Bench appearance |

Pairings considered and not used:

- **SWE-bench's critique of 'potpourri' benchmarks vs MMLU:** SWE-bench cites 'Hendrycks et al., 2021', which its reference list shows is APPS, not MMLU, so the critique is not about MMLU.
- **BatchNorm x ResNet on vanishing gradients:** ResNet's half is already Q01's answer, so Q41 uses the inference-time BN rule instead.
- **BatchNorm x BYOL on batch size:** natural (BYOL says its only batch-size dependence sits in BN layers; BatchNorm explains why BN depends on the batch), but it would add a fifth BYOL question. Kept as a spare.
- **MMLU or SWE-bench x Daily Oracle:** no textual link to MMLU; the temporal-split idea shared with SWE-bench is covered in Q43 without adding a fourth Daily Oracle question.
- **BabyCL x I-JEPA / MAE:** no explicit link in either text.
- **Distillation x timm 'dist' weights tags:** a possible later text+table question; out of scope here.

## 5. Recommended final composition

| Source type | Questions | Count |
|---|---|---|
| text-only | Q01-Q20 (6 replaced in place) and Q41-Q43 | 23 |
| table-only | Q21-Q30 (unchanged) | 10 |
| text+table | Q31-Q40 (unchanged) | 10 |
| **Total** | | **43** |

Text-only types: factual 5, conceptual 6, cross-paper 9, insufficient-evidence 3 (answerable = no: Q18, Q19, Q20). Text-only difficulty: easy 2, medium 12, hard 9. Whole set: easy 5, medium 22, hard 16. Manual review: 8 questions in the whole set, Q02 (new), Q09, Q12, Q30, Q34, Q35, Q37, Q39; the two removed flags were Q13 and Q15.

| Paper | Questions | Count |
|---|---|---|
| Transformer | Q06, Q11 | 2 |
| ResNet | Q01, Q14, Q41, Q32, Q36, Q40 | 6 |
| ViT | Q11, Q14, Q31, Q33, Q35, Q37, Q38 | 7 |
| BYOL | Q07, Q13, Q14, Q15, Q39 | 5 |
| MAE | Q12, Q34 | 2 |
| I-JEPA | Q03, Q12 | 2 |
| TemporalStraightening | Q09, Q14, Q19 | 3 |
| EmbeddingLimits | Q10, Q16 | 2 |
| DailyOracle | Q04, Q16, Q17 | 3 |
| FIRE-Bench | Q05, Q17, Q43 | 3 |
| BatchNorm | Q08, Q41 | 2 |
| Distillation | Q13, Q18 | 2 |
| BabyCL | Q02, Q15 | 2 |
| MMLU | Q42, Q43 | 2 |
| SWE-bench | Q20, Q43 | 2 |

Still thin (two questions each): Transformer, MAE, I-JEPA, EmbeddingLimits and all five new papers. MAE has no cross-source question beyond Q34, and the Transformer has none at all. ViT, ResNet and BYOL remain the most-used papers; the table can only support ResNet, ViT, MAE and BYOL, so that skew in the cross-source questions is structural.

**Landing on exactly 40.** If a 20/10/10 split matters more than two questions per new paper, drop Q41, Q42 and Q04. That leaves BatchNorm and MMLU with one question each (Q08 and Q43) and Daily Oracle with two. I did not do this by default because Q04 is a sound easy question and the other two are among the better new ones.

## 6. Not changed

Q21-Q40, `TabularData`, `TabularBenchmark`, `TabularEvidence`, `TabularDictionary`, the timm database and `tabular_data/`. `split` stays `development` and `data_source_type` stays `text-only` for every text question.

## 7. Outcome (applied to the workbook)

- `text_evaluation_candidates.xlsx` now has 15 rows in `Papers` (P11-P15 added), 43 rows in `Questions` (23 text-only, 10 table-only, 10 text+table) and 242 rows in `Evidence`: 151 carried over unchanged, 91 new, and the 45 rows that belonged to the six replaced questions removed.
- Replaced in place: Q02, Q08, Q13, Q15, Q18, Q20. Added: Q41, Q42, Q43. Not placed: the SWE-bench reserve (SW1).
- Checked after the update: all 242 quotes match their cited PDF pages; Q21-Q40 and the four `Tabular*` sheets are cell-for-cell identical to the pre-change workbook; the 14 kept text questions and their evidence rows are identical; `data_source_type` is `text-only` for every text question and `split` is `development` for all 43; each question's evidence papers equal its required papers; the timm database is unmodified (1,556 / 1,627 / 521 rows).
- New manual-review flag: Q02 (text and Table 1 disagree). Removed with their questions: Q13, Q15.
- Decision (2026-11-08): the 43-question set was kept; the trim to exactly 40 described in section 5 was not applied.
- Retired question text is kept in Appendix B so the change can be reviewed or reversed; their 45 evidence rows were removed as instructed.

## Appendix A: exact supporting passages (all verified against the PDFs)

### BN1: What evidence does the Batch Normalization paper give that batch normalization reduces internal covariate shift, how large is the training speed-up it reports on ImageNet (and what else was changed besides adding BN), and what does the paper itself say it has not established?

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| BatchNorm | 2 | 2 Towards Reducing Internal Covariate Shift | We define Internal Covariate Shift as the change in the distribution of network activations due to the change in network parameters during training. | defines internal covariate shift |
| BatchNorm | 2 | 2 Towards Reducing Internal Covariate Shift | By fixing the distribution of the layer inputs x as the training progresses, we expect to improve the training speed. | states expectation (not a measured result) |
| BatchNorm | 5 | 3.3 Batch Normalization enables higher learning rates | We further conjecture that Batch Normalization may lead the layer Jacobians to have singular values close to 1 | states conjecture |
| BatchNorm | 5 | 3.3 Batch Normalization enables higher learning rates | The precise effect of Batch Normalization on gradient propagation remains an area of further study. | states open question |
| BatchNorm | 6 | 4.1 Activations over time | The batch-normalized network enjoys the higher test accuracy. | reports MNIST result |
| BatchNorm | 6 | 4.1 Activations over time | In contrast, the distributions in the batch-normalized network are much more stable as training progresses, which aids the training. | reports direct evidence on input distributions (MNIST only) |
| BatchNorm | 6 | 4.2.1 Accelerating BN Networks | Simply adding Batch Normalization to a network does not take full advantage of our method. To do so, we further changed the network and its training parameters | states other changes accompany BN in the fast variants |
| BatchNorm | 6 | 4.2.1 Accelerating BN Networks | Increase learning rate. [...] Remove Dropout. [...] Reduce the L2 weight regularization. [...] Accelerate the learning rate decay. [...] Remove Local Response Normalization [...] Shuffle training examples more thoroughly. [...] Reduce the photometric distortions. | lists the non-BN changes |
| BatchNorm | 6 | 4.2.1 Accelerating BN Networks | the weight of this loss is reduced by a factor of 5 [...] we lower the learning rate 6 times faster | gives sizes of two of the changes |
| BatchNorm | 7 | 4.2.2 Single-Network Classification | Model Steps to 72.2% Max accuracy Inception 31.0 · 106 72.2% BN-Baseline 13.3 · 106 72.7% BN-x5 2.1 · 106 73.0% BN-x30 2.7 · 106 74.8% BN-x5-Sigmoid 69.8% | reports steps to 72.2% and maximum accuracy (Figure 3 table) |
| BatchNorm | 7 | 4.2.2 Single-Network Classification | BN-x5 needs 14 times fewer steps than Inception to reach the 72.2% accuracy. | reports headline speed-up |
| BatchNorm | 7 | 4.2.2 Single-Network Classification | By only using Batch Normalization (BN-Baseline), we match the accuracy of Inception in less than half the number of training steps. | reports BN-only result |
| BatchNorm | 7 | 4.2.2 Single-Network Classification | It reaches 74.8% after 6·106 steps, i.e. 5 times fewer steps than required by Inception to reach 72.2%. | reports BN-x30 result |
| BatchNorm | 7 | 4.2.2 Single-Network Classification | BN-x5-Sigmoid achieves the accuracy of 69.8%. Without Batch Normalization, Inception with sigmoid never achieves better than 1/1000 accuracy. | reports sigmoid result |
| BatchNorm | 7 | 4.2.2 Single-Network Classification | We also verified that the reduction in internal covariate shift allows deep networks with Batch Normalization to be trained when sigmoid is used as the nonlinearity | states the paper's own interpretation of the sigmoid result |

### BN2: The Batch Normalization paper says that once a network is trained, BN should no longer use mini-batch statistics. What does it use instead, and how does the ResNet paper handle its BN layers when fine-tuning for object detection, and why?

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| BatchNorm | 4 | 3.1 Training and Inference with Batch-Normalized Networks | The normalization of activations that depends on the mini-batch allows efficient training, but is neither necessary nor desirable during inference | states why inference differs |
| BatchNorm | 4 | 3.1 Training and Inference with Batch-Normalized Networks | using the population, rather than mini-batch, statistics. | states the inference rule |
| BatchNorm | 4 | 3.1 Training and Inference with Batch-Normalized Networks | We use the unbiased variance estimate | states how the population variance is estimated |
| BatchNorm | 4 | 3.1 Training and Inference with Batch-Normalized Networks | Since the means and variances are fixed during inference, the normalization is simply a linear transform applied to each activation. | states inference-time BN is a linear transform |
| BatchNorm | 4 | 3.1 Training and Inference with Batch-Normalized Networks | to yield a single linear transform that replaces BN(x). | states it can be folded into one transform |
| ResNet | 4 | 3.4 Implementation | We adopt batch normalization (BN) [16] right after each convolution and before activation, following [16]. | shows ResNet takes BN from the BatchNorm paper |
| ResNet | 10 | A. Object Detection Baselines | For the usage of BN layers, after pre-training, we compute the BN statistics (means and variances) for each layer on the ImageNet training set. Then the BN layers are fixed during fine-tuning for object detection. | states how ResNet handles BN in detection fine-tuning |
| ResNet | 10 | A. Object Detection Baselines | As such, the BN layers become linear activations with constant offsets and scales, and BN statistics are not updated by fine-tuning. | states the consequence |
| ResNet | 10 | A. Object Detection Baselines | We fix the BN layers mainly for reducing memory consumption in Faster R-CNN training. | states the reason |

### KD1: Distillation and BYOL both train one network to match another network's outputs. According to the two papers, what supplies the targets in each case and how does that target model come about, are labels used, and what does BYOL say about the 'mean teacher' method that it treats as closest to its slow-moving-average target?

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| Distillation | 1 | 1 Introduction | The cumbersome model could be an ensemble of separately trained models or a single very large model trained with a very strong regularizer such as dropout [9]. | defines the source of the targets |
| Distillation | 2 | 1 Introduction | is to use the class probabilities produced by the cumbersome model as “soft targets” for training the small model. | defines soft targets |
| Distillation | 2 | 1 Introduction | Our more general solution, called “distillation”, is to raise the temperature of the final softmax until the cumbersome model produces a suitably soft set of targets. | defines the temperature mechanism |
| Distillation | 3 | 2 Distillation | The same high temperature is used when training the distilled model, but after it has been trained it uses a temperature of 1. | states training and test temperature |
| Distillation | 3 | 2 Distillation | a weighted average of two different objective functions [...] using a condiderably lower weight on the second objective function | states how labels are combined with soft targets |
| BYOL | 1 | Abstract | BYOL relies on two neural networks, referred to as online and target networks, that interact and learn from each other. | describes BYOL's two networks |
| BYOL | 1 | Abstract | we update the target network with a slow-moving average of the online network. | states how the target model is obtained |
| BYOL | 1 | Abstract | While state-of-the art methods rely on negative pairs, BYOL achieves a new state of the art without them. | states BYOL works without negative pairs |
| BYOL | 4 | 3.1 Description of BYOL (Figure 2 caption) | ξ are an exponential moving average of θ and sg means stop-gradient. | defines target update and stop-gradient |
| BYOL | 4 | 3.1 Description of BYOL | Note that this predictor is only applied to the online branch | states the predictor sits only on the online branch |
| BYOL | 3 | 2 Related work | mean teacher (MT) [20] also uses a slow-moving average network, called teacher, to produce targets for an online network, called student. | describes mean teacher |
| BYOL | 3 | 2 Related work | consistency loss between the softmax predictions of the teacher and the student is added to the classification loss. | describes mean teacher's loss |
| BYOL | 3 | 2 Related work | in Section 5 we show that a similar approach collapses when removing the classification loss. In contrast, BYOL introduces an additional predictor on top of the online network, which prevents collapse. | states BYOL's comparison with mean teacher |

### KD2: According to the distillation paper, what accuracy does a single network reach on the JFT dataset after the knowledge in the specialist models has been distilled back into it?

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| Distillation | 8 | 8 Discussion | We have not yet shown that we can distill the knowledge in the specialists back into the single large net. | states the missing result |
| Distillation | 8 | 8 Discussion | the performance of a single really big net that has been trained for a very long time can be significantly improved by learning a large number of specialist nets | states what the paper does claim for specialists |
| Distillation | 8 | 6.1 Using soft targets to prevent specialists from overfitting | The soft targets can be provided by the generalist. We are currently exploring this approach. | states the related idea is still being explored |
| Distillation | 7 | 5.5 Results | With 61 specialist models, there is a 4.4% relative improvement in test accuracy overall. | reports the specialist-ensemble result |
| Distillation | 7 | 5.5 Results | System Conditional Test Accuracy Test Accuracy Baseline 43.1% 25.0% + 61 Specialist models 45.9% 26.1% | reports Table 3 values (ensemble, not distilled) |
| Distillation | 5 | 4.1 Results | More than 80% of the improvement in frame classification accuracy achieved by using an ensemble of 10 models is transferred to the distilled model | reports where distillation was actually tested (speech) |

### CL1: How does BabyCL's Labeled-S 4AFC accuracy compare with the offline CVCL upper bound and with the one-pass and compute-matched streaming baselines, and do the numbers in the text match those in Table 1?

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| BabyCL | 5 | 4.2 Main results - Table 1 | Offline CVCL (i.i.d.) 57.31 ± 1.13 One-pass CVCL (streaming) 27.52 ± 3.12 CL-CVCL (compute-matched) 36.41 ± 2.31 BabyCL (k = 4) 41.08 ± 1.79 BabyCL (k = 8) 43.38 ± 1.47 | reports Table 1 4AFC accuracies |
| BabyCL | 5 | 4.2 Main results - Table 1 caption | Offline CVCL serves as an upper bound (i.i.d., 400 epochs); one-pass CVCL represents naive streaming. CL-CVCL matches BabyCL’s gradient budget at k = 8. | defines what each baseline is |
| BabyCL | 6 | 4.2 Main results | One-pass CVCL collapses to 25.68% | reports text value that differs from Table 1 |
| BabyCL | 6 | 4.2 Main results | reaches only 35.32%, well below BabyCL at 44.46% (k = 8) | reports text values that differ from Table 1 |
| BabyCL | 6 | 4.2 Main results | yields a further 2.6-point gain | reports k=4 to k=8 gain in the text |
| BabyCL | 6 | 4.2 Main results | BabyCL substantially closes the gap to offline CVCL (57.45%) but does not match it | states the conclusion and a text value for offline CVCL |
| BabyCL | 6 | 4.2 Main results | Because CL-CVCL is matched in optimization work, the gap cannot be explained by gradient count alone | states the matched-budget argument |

### CL2: BabyCL's visual branch applies strong augmentations to two views of each frame. Compare the Gaussian-blur and solarization probabilities it uses for its two views with those BYOL uses for its two views, and say what the two papers report about whether negative pairs are needed.

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| BabyCL | 14 | A Implementation details - BabyCL: data augmentation | For SSL we generate two views per frame using strong augmentation | states two-view augmentation |
| BabyCL | 14 | A Implementation details - BabyCL: data augmentation | random resized crop to 224 × 224 (scale 0.2–1.0), random horizontal flip | gives crop scale |
| BabyCL | 14 | A Implementation details - BabyCL: data augmentation | random grayscale (0.2), Gaussian blur (applied with probability 1.0 on view 1 and 0.1 on view 2), and solarization on view 2 with probability 0.2. | gives blur, grayscale and solarization probabilities |
| BabyCL | 2 | 1 Introduction | finding that contrastive methods that leverage negative sampling from sampling are most effective | states the cited finding about negatives on SAYCam |
| BabyCL | 4 | 3 Method - Training objectives | Instance loss [...] a SimCLR objective [...] on augmented views of frames sampled from the visual buffer. | defines the visual loss |
| BabyCL | 4 | 3 Method - Training objectives | a symmetric InfoNCE loss on utterance-frame pairs drawn from the multimodal buffer | defines the cross-modal loss |
| BYOL | 16 | B Image augmentations | with an area uniformly sampled between 8% and 100% of that of the original image | gives BYOL crop scale |
| BYOL | 17 | B Image augmentations - Table 6 | Color dropping probability 0.2 0.2 Gaussian blurring probability 1.0 0.1 Solarization probability 0.0 0.2 | gives BYOL grayscale, blur and solarization probabilities for T and T' |
| BYOL | 1 | Abstract | While state-of-the art methods rely on negative pairs, BYOL achieves a new state of the art without them. | states BYOL works without negative pairs |
| BYOL | 8 | 5 Building intuitions with ablations - Image augmentations | the performance of BYOL is much less affected than the performance of SimCLR when removing color distortions from the set of image augmentations | reports BYOL's robustness to augmentation removal |

### MM1: Does the MMLU paper attribute its models' accuracy mainly to parameter count? Use its GPT-3, UnifiedQA and smaller fine-tuned model comparisons.

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| MMLU | 5 | 4.1 Setup - Table 1 | GPT-3 Small (few-shot) 24.4 30.9 26.0 24.1 25.9 GPT-3 Medium (few-shot) 26.1 21.6 25.6 25.5 24.9 GPT-3 Large (few-shot) 27.1 25.6 24.3 26.5 26.0 GPT-3 X-Large (few-shot) 40.8 50.4 36.7 48.8 43.9 | reports Table 1 GPT-3 averages by size |
| MMLU | 5 | 4.1 Setup | Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy. | states how UnifiedQA is evaluated |
| MMLU | 5 | 4.1 Setup - Table 1 caption | GPT-3 uses few-shot learning and UnifiedQA is tested under distribution shift. | states the evaluation regimes differ |
| MMLU | 6 | 4.2 Results - Model Size and Accuracy | We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%. | reports GPT-3 size effect |
| MMLU | 6 | 4.2 Results - Model Size and Accuracy | the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7% | reports zero-shot result |
| MMLU | 6 | 4.2 Results - Model Size and Accuracy | we show in Table 1 that it attains 48.9% accuracy. This performs better than the few-shot GPT-3 X-Large model, despite UnifiedQA have an order of magnitude fewer parameters. | reports UnifiedQA vs GPT-3 |
| MMLU | 6 | 4.2 Results - Model Size and Accuracy | We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy. These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps. | states the paper's conclusion |
| MMLU | 12 | A.1 Analysis with More Fine-Tuned Models | RoBERTa-base attains an overall accuracy of 27.9% [...] ALBERT-xxlarge attains an accuracy of 27.1% [...] GPT-2 attains an accuracy of 32.4% | reports smaller fine-tuned models |
| MMLU | 12 | A.1 Analysis with More Fine-Tuned Models | It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters. This suggests that its larger pretraining dataset enables higher accuracy. | states hedged explanation |
| MMLU | 12 | A.1 Analysis with More Fine-Tuned Models | UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy. | reports UnifiedQA-3B vs GPT-2 |

### MM2: MMLU, SWE-bench and FIRE-Bench each have to worry that a model may have seen benchmark content during training. What check does each paper run, what does it find, and how strongly does each paper state its conclusion?

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| MMLU | 13 | B.2 Exact Question and Answer Contamination | If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. | states what memorization would look like |
| MMLU | 14 | B.2 Exact Question and Answer Contamination | we see that accuracy and question entropy are not positively correlated, suggesting that the test’s low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers. This suggests that our exact questions were not memorized. | reports the check and conclusion |
| MMLU | 14 | B.2 Exact Question and Answer Contamination | However, during pretraining models encountered text related to our questions through processing Wikipedia. | states caveat |
| MMLU | 14 | B.2 Exact Question and Answer Contamination | we will provide a list of question sources | states planned mitigation |
| MMLU | 14 | B.2 Exact Question and Answer Contamination (Figure 13 caption) | In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56. | reports correlations |
| SWE-bench | 7 | 5 Results - Difficulty does not correlate with issue resolution date | partitioned by date, for PRs created before or after 2023. We find that for most models there’s little difference in performance before or after this date, with the exception of GPT-4. | reports the before/after-2023 check |
| SWE-bench | 7 | 5 Results - Difficulty does not correlate with issue resolution date | We consider this result to be largely promising as it suggests that despite models having been exposed to some version of an repository’s codebase, they are unlikely to “cheat” | states conclusion and its strength |
| SWE-bench | 7 | 5 Results - Table 7 | 4.87 4.23 0.49 0.77 1.96 0.0 2.95 3.46 3.98 3.85 | reports Table 7 values (columns: Claude 2, ChatGPT-3.5, GPT-4, SWE-Llama 7b, SWE-Llama 13b) |
| SWE-bench | 7 | 5 Results - Table 7 caption | Due to budget constraints, GPT-4 is evaluated on a 25% random subset of SWE-bench tasks, which may impact performance. | states GPT-4 column caveat |
| SWE-bench | 3 | 2.3 Features of SWE-bench | evaluate LMs on issues created after their training date, which ensures that the solution was not included in their training corpus. | states design-level mitigation |
| FIRE-Bench | 8 | 5.4. Data Contamination Analysis | A central concern for rediscovery-based evaluation is whether agent performance is inflated by memorization of benchmark papers that may appear in model training data. | states the concern |
| FIRE-Bench | 9 | 5.4. Data Contamination Analysis | While publication date does not guarantee inclusion or exclusion from training data, a strong contamination effect would be expected to manifest as consistently higher performance on pre-cutoff tasks within the same difficulty category. | states the check's logic |
| FIRE-Bench | 9 | 5.4. Data Contamination Analysis | Across difficulty levels, we observe no consistent advantage for pre-cutoff tasks. | reports the result |
| FIRE-Bench | 9 | 5.4. Data Contamination Analysis | This analysis is necessarily coarse (knowledge cutoff dates are approximate, training data composition is unknown, and per-category sample sizes are limited), so the result suggests the absence of a strong contamination signal rather than proving its absence. | states conclusion and its strength |

### SW1: In SWE-bench's baseline experiments, how are files chosen as model context (BM25 versus an 'oracle'), and what does the paper find about whether giving the model more retrieved context helps?

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| SWE-bench | 4 | 4 Experimental Setup | codebases consist of many more tokens (438K lines on average) than can typically be fit into an LMs context window | states why retrieval is needed |
| SWE-bench | 5 | 4.1 Retrieval-Based Approach | Dense retrieval methods are ill-suited to our setting due to very long key and query lengths | states why BM25 is used |
| SWE-bench | 5 | 4.1 Retrieval-Based Approach | we “retrieve” the files edited by the reference patch that solved the issue on GitHub | defines the oracle setting |
| SWE-bench | 5 | 4.1 Retrieval-Based Approach | From observation, models perform best on the shortest context window, as shown in Table 2. | states the context-length finding |
| SWE-bench | 5 | 4.1 Retrieval-Based Approach - Table 2 | Claude 2 1.96 1.87 1.22 | reports Claude 2 resolve rate at 13k/27k/50k BM25 context |
| SWE-bench | 5 | 4.1 Retrieval-Based Approach - Table 3 | BM25 Recall 13k 27k 50k Avg. 29.58 44.41 51.06 | reports BM25 recall of oracle files |
| SWE-bench | 6 | 5 Results | Even when increasing the maximum context size for BM25 would increase recall with respect to the oracle files, performance drops, as shown in Table 2, as models are simply ineffective at localizing problematic code. | states the result |
| SWE-bench | 6 | 5 Results | There, Claude 2 is able to resolve 4.8% of issues using the “oracle” retriever. | reports oracle result |
| SWE-bench | 7 | 5 Results | GPT-4 jumping from 1.3% to 3.4% and Claude 2 from 4.8% to 5.9% | reports oracle-collapsed result |

### SW2: According to the SWE-bench paper, what resolve rate do agent-based systems (models that run code, navigate the repository and iterate) reach on SWE-bench?

| Paper | Page | Section | Passage | Role |
|---|---|---|---|---|
| SWE-bench | 3 | 2.3 Features of SWE-bench | can serve as a level playing field to compare approaches ranging from retrieval and long-context models to decisionmaking agents, which could reason and act in code. | states agents are an intended use, not evaluated |
| SWE-bench | 10 | 7 Discussion | our experiments aim to establish a baseline of the simplest and most straight-forward approaches for this task | states the experiments are simple baselines |
| SWE-bench | 10 | 7 Discussion | encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs) | states agents are future work |
| SWE-bench | 5 | 4.3 Models | we evaluate ChatGPT-3.5 (gpt-3.5-turbo-16k-0613), GPT-4 (gpt-4-32k-0613), Claude 2, and SWE-Llama | lists the evaluated models |
| SWE-bench | 3 | 2.2 Task Formulation | In practice, we represent edits as patch files, which specify which lines in the codebase to modify in order to resolve the issue. | states the single-patch output format |
| SWE-bench | 6 | 5 Results | Across the board, models struggle significantly to resolve issues. | reports overall result |
| SWE-bench | 6 | 5 Results | There, Claude 2 is able to resolve 4.8% of issues using the “oracle” retriever. | reports oracle result |

## Appendix B: retired questions (full text as they were before the update)

### Q02 (factual, easy, papers: MAE, review: no)

**Question.** What masking ratio does MAE use by default, how does that compare with BERT and earlier vision work, and what reasoning do the authors give for masking so much of the image?

**Reference answer.** MAE masks 75% of the image patches by default. The paper contrasts this with BERT's typical 15% and with 20-50% in related vision work. The reasoning is that images have heavy spatial redundancy (a missing patch can be recovered from neighbours), so masking a very high portion of random patches removes that redundancy and yields a task requiring holistic understanding; because the encoder sees only the visible ~25% of patches, it also cuts pre-training time by 3x or more. 75% works well for both linear probing and fine-tuning, but fine-tuning is less sensitive (40-80% all work well) while linear probing improves steadily up to the sweet spot. The authors only 'hypothesize' that the reasoning-like behaviour is linked to useful representations.

**Notes.** Good easy retrieval target but with hedging: do not state as proven that high masking causes better representations. Hard negative for retrieval: I-JEPA also uses masking (block-based) but with different ratios/targets. [General-knowledge risk: medium.]

### Q08 (conceptual, medium, papers: ViT, review: no)

**Question.** How does the ViT paper explain the relationship between pre-training dataset size and ViT's performance compared with ResNets, and how much weight do the authors put on this explanation?

**Reference answer.** On mid-sized data (ImageNet) without strong regularisation ViT is a few percentage points below comparable ResNets; the authors attribute this to Transformers lacking CNN inductive biases such as translation equivariance and locality, so they do not generalise well on insufficient data. With larger pre-training (ImageNet-21k, JFT-300M) ViT approaches or beats the state of the art ('large scale training trumps inductive bias'). Their dataset-subset experiment shows ViTs overfit more than ResNets on small subsets (e.g., ViT-B/32 is much worse than ResNet50 on 9M images but better on 90M+), which they describe as reinforcing 'the intuition' that convolutional bias helps on small data but is unnecessary or even harmful at scale. They also caution that pre-training efficiency comparisons may be affected by schedule, optimiser and weight decay, not only architecture.

**Notes.** Claim-vs-evidence question: the inductive-bias explanation is framed as intuition, not a controlled causal test. The efficiency comparison (2-4x less compute) is reported with an explicit caveat on page 6 and a controlled study in Section 4.4. [General-knowledge risk: medium.]

### Q13 (cross-paper, hard, papers: BYOL; I-JEPA, review: yes)

**Question.** BYOL and I-JEPA both predict the output of a slowly-updated target network rather than pixels. How do they differ in how the prediction task is built and how much they depend on hand-crafted image augmentations, and how does the I-JEPA paper position BYOL in its comparisons?

**Reference answer.** BYOL builds its task from two augmented views of the same image (SimCLR-style augmentations): the online network (encoder, projector, predictor) predicts the target network's projection of the other view, with the target an exponential moving average of the online network. The BYOL paper concludes it 'remains dependent on existing sets of augmentations'. I-JEPA works on a single image: a context block predicts the patch-level representations of several target blocks in the same image, again with an exponential-moving-average target encoder (which the paper says was essential), and it aims to avoid hand-crafted view augmentations. The I-JEPA paper groups BYOL with 'methods using extra view data augmentations' and lists BYOL (ResNet-200 2x, 800 epochs) at 71.2% top-1 with 1% ImageNet labels versus 73.3% for I-JEPA ViT-H/14; BYOL's own Table 2 gives the same 71.2% for ResNet-200 (2x). These are different backbones and pre-training setups, so the numbers do not isolate the method.

**Notes.** MANUAL REVIEW: avoid superiority claims (different architectures, epochs and protocols). Candidate for the later tabular dataset (method, backbone, epochs, label fraction, top-1). The user-requested BYOL vs I-JEPA retrieval challenge. [General-knowledge risk: medium.]

### Q15 (cross-paper, medium, papers: ViT; MAE, review: yes)

**Question.** What did the original ViT paper find about self-supervised masked-patch pre-training, and how does the MAE paper relate its results to ViT's findings about training on ImageNet-1K alone?

**Reference answer.** The ViT paper ran only a preliminary masked-patch-prediction experiment (mimicking BERT): ViT-B/16 reached 79.9% on ImageNet, 2% better than training from scratch but 4% behind supervised pre-training, and the authors say a large gap to large-scale supervised pre-training remains. The MAE paper cites ViT as having studied masked patch prediction, notes that in the original ViT paper ViT-L degrades when trained on ImageNet-1K only, and reports that its own supervised baseline works better but saturates, whereas MAE pre-training on ImageNet-1K only generalises better with larger gains for higher-capacity models (ViT-L from scratch 82.5% vs 84.9% with MAE; ViT-H 87.8%). Caveat: the ViT-B/16 79.9% and MAE's ViT-L/H numbers come from different model sizes and recipes, so the papers do not give a controlled comparison.

**Notes.** MANUAL REVIEW: cross-paper numbers are not like-for-like; answer should not claim MAE 'beats' ViT's masked-patch result. The MAE section 'Comparisons with supervised pre-training' is the bridge passage. [General-knowledge risk: low.]

### Q18 (insufficient-evidence, hard, papers: EmbeddingLimits, review: no)

**Question.** Based on the embedding-retrieval paper, what is the minimum embedding dimension needed to reliably retrieve the right documents over a 10-million-document corpus with realistic user queries?

**Reference answer.** The supplied paper does not establish this. It gives a theoretical lower bound in terms of sign-rank and a best-case 'free embedding' experiment for k = 2 over all document pairs, extrapolating a critical corpus size per dimension (about 4M at d = 1024 and 107M at d = 3072). These are test-set-optimised, extrapolated, maximal-combination results that the authors say real models cannot reach: a real embedding model with 64 dimensions could not solve the 46-document LIMIT task that free embeddings solve with 12 dimensions. The paper does not give a required dimension for realistic query distributions, so reading a number off the extrapolated curve (e.g., interpolating between 1024 and 3072) would be unsupported.

**Notes.** Insufficient-evidence trap: tempting to interpolate the critical-n numbers. Correct response states the limitation. The same passages support Q10 but for a different purpose. [General-knowledge risk: low.]

### Q20 (insufficient-evidence, easy, papers: FIRE-Bench, review: no)

**Question.** Does FIRE-Bench show that current AI agents can make genuinely novel scientific discoveries that have not already been published?

**Reference answer.** No. FIRE-Bench deliberately avoids asking agents for novel, unverified claims; it asks them to rediscover established findings from published ML papers, scored against the papers' documented findings, because validating novel findings would require costly real-world verification. Even on rediscovery the best agent (Claude Code with Claude-4-Sonnet) averaged only 46.7 F1 with high run-to-run variance, so the paper provides evidence about rediscovery success, not about novel discovery.

**Notes.** Insufficient-evidence question: the title/abstract language ('open-ended discovery can be evaluated') could mislead a system into answering yes. Correct response identifies the scope limit. [General-knowledge risk: medium.]

