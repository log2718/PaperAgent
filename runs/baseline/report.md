# Report: runs/baseline

33 questions, 0 errors, mean latency 21.4 s.

| Source type | Retrieval page hit | SQL value overlap | Answers with abstention wording |
|---|---|---|---|
| text-only | 0.58 (n=19) | - | 13 of 19 |
| table-only | - | 0.71 (n=7) | 0 of 7 |
| text+table | 0.62 (n=7) | 0.83 (n=7) | 5 of 7 |

Insufficient-evidence questions (Q18, Q20): 2 of 2 answers use abstention wording (keyword heuristic, check by reading).

Diagnostics are heuristics, not grades. *Retrieval page hit*: share of the workbook's gold evidence pages covered by retrieved chunks. *SQL value overlap*: share of cells of the workbook's reference SQL result that also appear in the system's result. Grade answers by reading them against the reference.

## Q01 (text-only, factual, medium, answerable: yes)

**Question.** In the ResNet paper's ImageNet comparison of 18-layer and 34-layer networks, how did the plain and residual versions differ, and why do the authors argue the plain network's problem is not caused by vanishing gradients?

**Reference answer.** The 34-layer plain net had higher error than the 18-layer plain net (top-1 validation error 28.54% vs 27.94%, Table 2) and higher training error throughout training; the authors call this the degradation problem. With identity shortcuts (zero-padded, so no extra parameters) the order reversed: the 34-layer ResNet reached 25.03% vs 27.88% for the 18-layer ResNet (2.8 points better). The authors argue the plain-net difficulty is unlikely to be vanishing gradients because the plain nets are trained with batch normalization, which keeps forward signals at non-zero variance, and they verified that backward gradients have healthy norms; they only conjecture that deep plain nets may have exponentially low convergence rates. Training 3x longer still showed degradation.

**System answer.** ## How the plain and residual versions differed

For the 18-layer and 34-layer comparison, the plain networks and ResNets had **identical architectures** except for the shortcut connections:

- "The baseline architectures are the same as the above plain nets, expect that a shortcut connection is added to each pair of 3×3 ﬁlters as in Fig. 3 (right)." [ResNet, p.5]
- For this first comparison, shortcuts used **identity mapping**, with **zero-padding for increasing dimensions (option A)**, so "they have no extra parameter compared to the plain counterparts." [ResNet, p.5]

In terms of results:
- Plain networks: 34-layer had *higher* training error than the 18-layer plain net throughout training, despite the 18-layer solution space being a subspace of the 34-layer one — i.e., the deeper plain net was harder to optimize (the "degradation problem"). [ResNet, p.5]
- Top-1 errors (Table 2, 10-crop): plain-18 = 27.94%, plain-34 = 28.54% (deeper plain net is *worse*); ResNet-18 = 27.88%, ResNet-34 = 25.03% (deeper ResNet is *better*, by 2.8% over ResNet-18). [ResNet, p.5]
- "the situation is reversed with residual learning – the 34-layer ResNet is better than the 18-layer ResNet (by 2.8%)... the 34-layer ResNet exhibits considerably lower training error and is generalizable to the validation data." [ResNet, p.5–6]
- Comparing the 34-layer ResNet to its plain counterpart: "the 34-layer ResNet reduces the top-1 error by 3.5% (Table 2), resulting from the successfully reduced training error." [ResNet, p.6]
- For the 18-layer case, plain and residual nets were "comparably accurate" (27.94% vs 27.88%), but "the 18-layer ResNet converges faster," easing optimization via faster early-stage convergence when the net is "not overly deep." [ResNet, p.6]

## Why not vanishing gradients

The authors give two pieces of evidence against vanishing gradients as the cause of the plain network's optimization difficulty:

1. **BN ensures healthy signal propagation**: "These plain networks are trained with BN [16], which ensures forward propagated signals to have non-zero variances. We also verify that the backward propagated gradients exhibit healthy norms with BN. So neither forward nor backward signals vanish." [ResNet, p.5]

2. **The deep plain net still achieves competitive accuracy**: "the 34-layer plain net is still able to achieve competitive accuracy (Table 3), suggesting that the solver works to some extent." [ResNet, p.5]

Based on this, they instead **conjecture** that "the deep plain nets may have exponentially low convergence rates, which impact the reducing of the training error," noting also that they tried training with 3× more iterations and still observed the degradation problem, "suggesting that this problem cannot be feasibly addressed by simply using more iterations" [ResNet, p.5]. They state "the reason for such optimization difﬁculties will be studied in the future" [ResNet, p.5] — i.e., the passages do not give a definitive mechanism, only evidence ruling out vanishing gradients and a tentative conjecture about convergence rate.

**Retrieved:** ResNet p.5 (0.84); ResNet p.5-6 (0.83); ResNet p.7-8 (0.81); ResNet p.6 (0.81); ResNet p.3-4 (0.80) | gold page hit: 1.00
*20.1 s*

## Q02 (text-only, factual, hard, answerable: yes)

**Question.** How does BabyCL's Labeled-S 4AFC accuracy compare with the offline CVCL upper bound and with the one-pass and compute-matched streaming baselines, and do the numbers in the text match those in Table 1?

**Reference answer.** Table 1 (4AFC, Labeled-S): Offline CVCL (i.i.d., 400 epochs) 57.31 +/- 1.13; One-pass CVCL (streaming) 27.52 +/- 3.12; CL-CVCL (compute-matched) 36.41 +/- 2.31; BabyCL with k=4 41.08 +/- 1.79 and with k=8 43.38 +/- 1.47. The authors conclude that BabyCL beats the streaming baselines under a matched optimization budget and substantially narrows, but does not close, the gap to offline training; since CL-CVCL matches BabyCL's gradient budget, the gap 'cannot be explained by gradient count alone'. The Section 4.2 text does not match Table 1: it gives One-pass CVCL 25.68%, CL-CVCL 35.32%, BabyCL 44.46% (k=8) and offline CVCL 57.45%, and a 2.6-point gain from k=4 to k=8 (Table 1 differs by 2.30). The paper does not explain the discrepancy.

**System answer.** ## Comparison of BabyCL to the baselines

**As reported in the text (Section 4.2, main results):**
- **Offline CVCL** (i.i.d., 400 epochs) = **57.45%** — serves as the upper bound [BabyCL, p.6-7].
- **One-pass CVCL** (naive streaming, no replay) = **25.68%** — "collapses," confirming that i.i.d.-style training does not transfer to streaming [BabyCL, p.6-7].
- **CL-CVCL** (compute-matched, replay added to match BabyCL's gradient budget at k=8) = **35.32%** [BabyCL, p.6-7].
- **BabyCL (k=8)** = **44.46%** [BabyCL, p.6-7].

From these text figures:
- BabyCL vs. offline upper bound: 57.45 − 44.46 = **12.99 points below** the offline ceiling, described as "substantially clos[ing] the gap... but does not match it" [BabyCL, p.6-7].
- BabyCL vs. compute-matched CL-CVCL: 44.46 − 35.32 = **9.14 points higher**, which the authors attribute to BabyCL's continual-learning structure (event segmentation + combined visual/cross-modal objectives) rather than extra gradient updates, since the two are optimization-matched [BabyCL, p.6-7].
- BabyCL vs. naive one-pass streaming: 44.46 − 25.68 = **18.78 points higher**.

**As shown in Table 1 (passage [1], partially visible):**
- Offline CVCL row: truncated, visible only as "**31 ± 1.13**" (the leading digits appear cut off in this excerpt, so the full value cannot be confirmed from the evidence given).
- One-pass CVCL (streaming): **27.52 ± 3.12**
- CL-CVCL (compute-matched): **36.41 ± 2.31**
- BabyCL (k=4): **41.08 ± 1.79**
- BabyCL (k=8): **43.38 ± 1.47**

## Do the text numbers match Table 1?

Not exactly — there are small but consistent discrepancies between the single-point values quoted in the running text and the "Final mean ± CI" values in Table 1:

| Model | Text value | Table 1 value | Difference |
|---|---|---|---|
| One-pass CVCL | 25.68% | 27.52 ± 3.12% | 1.84 pts |
| CL-CVCL | 35.32% | 36.41 ± 2.31% | 1.09 pts |
| BabyCL (k=8) | 44.46% | 43.38 ± 1.47% | 1.08 pts |
| Offline CVCL | 57.45% | "31 ± 1.13" (truncated) | cannot be verified from this excerpt |

Notably, the Table 1 value for BabyCL (k=8), **43.38 ± 1.47%**, is identical to the "Final mean ± CI" reported for BabyCL's default 25% multimodal-fraction setting in Table 2 [BabyCL, p.5-6]. This suggests Table 1 reports the mean ± 95% CI across the three seeds, whereas the text's narrative figures (e.g., 44.46% for BabyCL) appear to come from a different statistic (possibly a single representative run or a "best" value), since they don't align numerically with the Table 1 means.

**Caveat:** The evidence for the Offline CVCL row in Table 1 is incomplete (only "31 ± 1.13" is visible, likely due to truncation in the passage), so I cannot confirm whether the table's offline value does or does not match the text's 57.45% figure. Based on the available text, the exact numeric match between Table 1 and the narrative claims cannot be fully verified, and the three baselines/BabyCL values I can compare each differ from the Table 1 means by roughly 1–2 percentage points.

**Retrieved:** BabyCL p.5-6 (0.83); BabyCL p.6-7 (0.81); BabyCL p.7-8 (0.78); BabyCL p.14-15 (0.77); BabyCL p.10-12 (0.77) | gold page hit: 1.00
*34.4 s*

## Q03 (text-only, factual, medium, answerable: yes)

**Question.** How does I-JEPA sample its target and context blocks (number of target blocks, scale and aspect-ratio ranges), and where in the pipeline are the target blocks 'masked'?

**Reference answer.** I-JEPA typically samples M = 4 target blocks, each with random aspect ratio in (0.75, 1.5) and random scale in (0.15, 0.2). The context is a single block with scale in (0.85, 1.0) and unit aspect ratio, from which any region overlapping the targets is removed so the prediction task is non-trivial. The target blocks are obtained by masking the output of the target encoder, not its input, which the paper calls crucial for high-semantic-level targets. The loss is the average L2 distance between predicted and target patch-level representations, and the target encoder is an exponential moving average of the context encoder.

**System answer.** ## I-JEPA Target and Context Block Sampling

**Target blocks:**
- I-JEPA typically samples **M = 4** target blocks [I-JEPA, p.3-4].
- Each target block is sampled with a random **aspect ratio in the range (0.75, 1.5)** and a random **scale in the range (0.15, 0.2)** [I-JEPA, p.3-4].
- These M target blocks are sampled from the output representation sequence sy produced by the **target-encoder**, i.e., "we randomly sample M (possibly overlapping) blocks from the target representations sy" [I-JEPA, p.3-4].

**Context block:**
- A **single** context block x is sampled with a random **scale in the range (0.85, 1.0)** and **unit aspect ratio** [I-JEPA, p.3-4].
- Since target blocks are sampled independently of the context block, overlap may occur; any overlapping regions between the sampled context block and the target blocks are **removed from the context block** "to ensure a non-trivial prediction task" [I-JEPA, p.3-4].

**Where masking is applied — a key design choice:**
- "the target blocks are obtained by masking the output of the target-encoder, not the input" [I-JEPA, p.3-4]. That is, the full (unmasked) image is first fed through the target encoder to get patch-level representations sy = {sy1,...,syN}, and *then* the M target blocks are extracted (masked) from this already-computed representation — rather than masking the input image before encoding.
- The paper states this distinction is "crucial to ensure target representations of a high semantic level" [I-JEPA, p.3-4].
- This is confirmed by an ablation (Table 11): masking the input (forward-propagating through the target-encoder once per target region on a masked input) instead of masking the output drops linear-probe Top-1 accuracy on 1% ImageNet-1K from **67.3%** (masking output) to **56.1%** (masking input) for a ViT-H/16 pretrained for 300 epochs [I-JEPA, p.14-15]. The paper concludes "Masking the output of the target-encoder during pretraining results in more semantic prediction targets and improves linear probing performance" [I-JEPA, p.14-15].

**Summary:** 4 target blocks are sampled with scale (0.15, 0.2) and aspect ratio (0.75, 1.5) from the target-encoder's output (not the raw input), and 1 context block is sampled with scale (0.85, 1.0) and unit aspect ratio from the input image, with any overlap with target blocks removed before being passed to the context encoder [I-JEPA, p.3-4].

**Retrieved:** I-JEPA p.13-14 (0.83); I-JEPA p.3-4 (0.83); I-JEPA p.14-15 (0.80); I-JEPA p.7-8 (0.80); I-JEPA p.8-9 (0.78) | gold page hit: 1.00
*12.8 s*

## Q04 (text-only, factual, easy, answerable: yes)

**Question.** How are Daily Oracle's question-answer pairs generated and filtered, and how many True/False and multiple-choice questions are in the subset analysed in the paper?

**Reference answer.** The analysed subset has 16,783 True/False and 14,727 multiple-choice questions generated from daily news articles from January 2020 to December 2024. Each day six articles are selected (three random, three from hot topics) and an LLM generates two TF and two MC pairs per article with few-shot prompting. Construction has four steps: article summary (focused on new events so the publication date can be the resolution date), QA generation, misleading-choice generation for MC, and QA filtering. In filtering, an LLM scores seven principles from 0 to 2 points each and only questions with at least 13 points are kept.

**System answer.** ## Generation and Filtering Process

Daily Oracle's QA pairs are generated through a four-step LLM-based pipeline [DailyOracle, p.4]:

1. **Question Generation**: For True/False (TF) questions, the LLM generates a pair of questions on the same topic — "the first question with a 'Yes' answer and the second with a 'No'" [DailyOracle, p.4].

2. **Misleading Choices Generation**: For multiple-choice (MC) questions, the LLM is given "the article, its publishing date, and the QA pair" and generates "three misleading choices" [DailyOracle, p.4].

3. **QA Filtering**: The LLM checks each QA pair against seven principles:
   - correctness of answers
   - non-answerability before the publication date
   - absence of information leakage
   - objectivity
   - inclusion of a clear temporal element
   - public interest
   - non-obviousness of the answer

   Each principle is scored 0, 1, or 2 points, and only questions scoring **at least 13 points in total** are retained [DailyOracle, p.4].

**Models used**: GPT-3.5 or GPT-4o-mini are used for steps (1) and (4) (question generation and filtering), while GPT-4 or GPT-4o are used for steps (2) and (3) (misleading choices generation) "to ensure high data quality" [DailyOracle, p.4]. Specifically, "GPT-3.5 and GPT-4" were used until September 2024, after which the authors "switch to GPT-4o-mini and GPT-4o, as they are both more cost-effective and more powerful" [DailyOracle, p.4-5].

## Dataset Size

The subset used for the paper's analysis consists of:
- **16,783 TF (True/False) questions**
- **14,727 MC (Multiple Choice) questions**

This covers the period from January 1, 2020, to December 31, 2024, "with an average of 17.2 questions per day" [DailyOracle, p.4]. This same count is reiterated elsewhere: "we utilize a subset of the data consisting of 16,783 TF questions and 14,727 MC questions, covering a diverse range of forecasting topics, which are generated using daily news articles from January 2020 up until December 2024" [DailyOracle, p.3].

Note: The paper states that Daily Oracle itself "remains active, continuing to generate new questions daily from 2025 onward" [DailyOracle, p.3], so these figures represent the fixed analysis subset at the time of writing, not the dataset's total eventual size.

**Retrieved:** DailyOracle p.4 (0.77); DailyOracle p.3 (0.77); DailyOracle p.4-5 (0.77); DailyOracle p.17-19 (0.74); DailyOracle p.34-35 (0.74) | gold page hit: 1.00
*11.6 s*

## Q06 (text-only, conceptual, medium, answerable: yes)

**Question.** What three desiderata do the Transformer authors use to motivate self-attention over recurrent and convolutional layers, how does a self-attention layer compare on each, and when is it cheaper per layer than a recurrent layer?

**Reference answer.** The desiderata are (1) total computational complexity per layer, (2) the amount of computation that can be parallelised (minimum number of sequential operations) and (3) the path length between long-range dependencies. Per Table 1, self-attention has O(n^2*d) complexity per layer, O(1) sequential operations and O(1) maximum path length; recurrent layers have O(n*d^2), O(n) and O(n); convolutional layers have O(k*n*d^2), O(1) and O(log_k n). Self-attention is faster than a recurrent layer when the sequence length n is smaller than the representation dimensionality d, which is typical for sentence representations in machine translation. For very long sequences the authors suggest restricting attention to a neighbourhood of size r (path length O(n/r)) but leave this to future work.

**System answer.** Based on the passage provided from the Transformer paper's "Why Self-Attention" section [Transformer, p.7-8], the evidence is **incomplete** for fully answering this question. The excerpt begins mid-sentence ("lutional layers in the case of contiguous kernels...") and appears to pick up partway through the comparison, after the original listing of the three desiderata. The passage does not contain the explicit opening statement where the three desiderata (per-layer computational complexity, amount of parallelizable computation/minimum sequential operations, and maximum path length between long-range dependencies) are first introduced and defined.

What the passage **does** show:

1. **Path length between positions** (one of the implied desiderata): The excerpt discusses how convolutional layers require a stack of O(n/k) layers (contiguous kernels) or O(log_k(n)) layers (dilated convolutions) to connect all pairs of positions, which "increas[es] the length of the longest paths between any two positions in the network" [Transformer, p.7]. This implies self-attention is being contrasted favorably, since (per the surrounding context) self-attention connects all positions in O(1) layers — though the passage itself does not state this O(1) figure explicitly for self-attention.

2. **Per-layer computational complexity** (a second desideratum): The passage states "Convolutional layers are generally more expensive than recurrent layers, by a factor of k" [Transformer, p.7]. It further notes that separable convolutions reduce complexity to O(k·n·d + n·d²), and "even with k = n, ... the complexity of a separable convolution is equal to the combination of a self-attention layer and a point-wise feed-forward layer, the approach we take in our model" [Transformer, p.7-8]. This equates the self-attention+feed-forward combination's complexity to that of a separable convolution with k=n, but it does **not** directly state the self-attention-vs-recurrent-layer complexity comparison or give the specific condition under which self-attention is cheaper per layer than a recurrent layer.

**On the specific question of when self-attention is cheaper per layer than a recurrent layer:** The provided passage does not contain this comparison or condition. It only states the convolution-vs-recurrent relationship (convolutions more expensive "by a factor of k") and the convolution-vs-self-attention relationship (equal complexity under k=n). No sentence in the given excerpt directly compares self-attention's per-layer complexity to a recurrent layer's, nor specifies a condition (e.g., relating sequence length n and representation dimension d) under which one is cheaper than the other.

**Third desideratum (parallelizable computation):** Not addressed anywhere in the given passage.

**Summary:** The evidence provided only partially supports an answer. It documents comparisons involving convolutional vs. recurrent layers (cost factor k) and convolutional vs. self-attention+feed-forward (equal cost when k=n), plus a qualitative point about path-length growth in convolutional stacks. It does not supply the original three-desiderata framing, does not state self-attention's own per-layer complexity or parallelization properties explicitly, and does not state the condition under which self-attention is cheaper per layer than a recurrent layer. A complete answer would require passages from earlier/later in section 4 (e.g., a complexity table and the explicit n vs. d comparison), which are not included here.

**Retrieved:** Transformer p.7-8 (0.76); Transformer p.2-3 (0.75); Transformer p.10 (0.74); ViT p.2 (0.73); ViT p.1 (0.73) | gold page hit: 0.50
*27.0 s*

## Q07 (text-only, conceptual, hard, answerable: yes)

**Question.** BYOL trains without negative pairs. What mechanisms does the paper credit with preventing representation collapse, and what do its ablations show about them?

**Reference answer.** BYOL trains an online network (encoder, projector, predictor) to predict the projection of a second augmented view produced by a target network whose weights are an exponential moving average of the online weights; the loss gradient is not propagated into the target (stop-gradient) and the predictor exists only on the online branch. The authors hypothesise that the combination of the predictor and the slow-moving-average target avoids collapse, but they state the dynamics still admit undesirable equilibria that they did not observe in experiments. In the ablation (Table 5b), the only variant that performs well without negatives is BYOL with both a target network and a predictor; the representation collapses when either is removed. They also found that the target network can be removed without collapse if the predictor is kept near-optimal (e.g., higher predictor learning rate), suggesting that keeping the predictor near-optimal may be one role of the target network.

**System answer.** ## Mechanisms credited with preventing collapse

**1. The predictor combined with the target network (bootstrapping asymmetry)**
BYOL does not use an explicit anti-collapse term like negative pairs [BYOL, p.4]. Instead, the paper argues that because the target network's parameters ξ are *not* updated in the direction of ∇ξL_BYOL (only θ receives gradients, with ξ updated via a stop-gradient/moving-average rule), "there is no loss L_θ,ξ such that BYOL's dynamics is a gradient descent on L jointly over θ, ξ" [BYOL, p.4]. This asymmetry means the dynamics do not simply converge to a joint minimum of the loss (e.g., a collapsed constant representation) the way a naive joint gradient descent would.

**2. A near-optimal predictor is the key stabilizing ingredient**
When the predictor q_θ is assumed optimal (q⋆(z_θ) = E[z'_ξ | z_θ]), the paper shows that BYOL's updates on θ follow, in expectation, the gradient of the expected conditional variance: ∇θ E[Σ_i Var(z'_ξ,i | z_θ)] [BYOL, p.4-5]. Since Var(X|Y,Z) ≤ Var(X|Y) for any variables, adding stochastic variability (through augmentations and the predictor's imperfect prediction) tends to reduce this conditional variance rather than driving it toward a degenerate collapsed solution — leading the authors to hypothesize that "the undesirable equilibria are unstable" [BYOL, p.4-5]. This leads to the conclusion that "keeping the predictor near-optimal at all times is important to preventing collapse, which may be one of the roles of BYOL's target network" [BYOL, p.9-10, also repeated p.10-11].

## What the ablations show

- **Removing both predictor and target network causes collapse**: "Table 5b already shows the importance of combining a predictor and a target network: the representation does collapse when either is removed" [BYOL, p.9-10].

- **Predictor is critical even without the target network's "slowness," if made near-optimal**: The target network can be removed *without* collapse if the predictor is instead kept near-optimal, via:
  - (i) an optimal linear predictor obtained by linear regression on the current batch before back-propagating the error — 52.5% top-1 accuracy;
  - (ii) increasing the learning rate of the predictor — 66.5% top-1 accuracy [BYOL, p.9-10].
  
  In contrast, increasing the learning rates of *both* the projector and predictor (still without a target network) "yields poor results (≈25% top-1)" [BYOL, p.9-10], indicating that it's specifically a near-optimal predictor relative to the current online representation that matters, not just a higher learning rate everywhere.

- **Removing the predictor (keeping the target network) causes collapse, mirroring Mean Teacher**: Removing the predictor turns BYOL into an unsupervised variant of Mean Teacher (no classification loss, image augmentations instead of dropout noise), and "this variant of BYOL collapses (Row 7 of Table 5) which suggests that the additional predictor is critical to prevent collapse in an unsupervised scenario" [BYOL, p.9-10].

- **Target network also benefits contrastive methods via a general stabilization effect, not just anti-collapse**: "Simply adding a target network to SimCLR already improves performance (+1.6 points)... by mere stabilization effect, even when using the same number of negative examples, using a target network is beneficial" [BYOL, p.9-10]. This suggests the target network's role is broader than collapse-prevention alone — it also stabilizes bootstrapped training generally, paralleling its use in MoCo and deep RL target networks [BYOL, p.2-3].

## Summary

The paper credits two intertwined mechanisms — the **target network** (providing a stable, slow-moving bootstrap target so the dynamics aren't a joint gradient descent on one loss [BYOL, p.4]) and the **predictor** (which, when near-optimal, makes BYOL's updates approximate a conditional-variance-reduction process that disfavors degenerate collapsed solutions [BYOL, p.4-5]). The ablations confirm both are necessary in the standard setup (removing either causes collapse [BYOL, p.9-10]), but also show the target network can be substituted by directly forcing the predictor to be near-optimal (52.5%–66.5% top-1 without a target network) [BYOL, p.9-10], supporting the claim that near-optimality of the predictor — which the target network helps maintain — is the deeper mechanism preventing collapse.

**Retrieved:** BYOL p.4-5 (0.74); BYOL p.10-11 (0.73); BYOL p.2 (0.73); BYOL p.9-10 (0.73); BYOL p.2-3 (0.72) | gold page hit: 1.00
*19.0 s*

## Q08 (text-only, conceptual, medium, answerable: yes)

**Question.** What evidence does the Batch Normalization paper give that batch normalization reduces internal covariate shift, how large is the training speed-up it reports on ImageNet (and what else was changed besides adding BN), and what does the paper itself say it has not established?

**Reference answer.** The paper defines internal covariate shift as the change in the distribution of network activations due to the change in network parameters during training. Its direct evidence is a small MNIST experiment (three sigmoid hidden layers): the input distribution to a typical sigmoid unit is much more stable with BN and the BN network has higher test accuracy (Fig. 1). On ImageNet the evidence is indirect, through the speed and accuracy of BN-Inception variants: BN-Baseline matches Inception's 72.2% in 13.3M steps versus 31.0M, BN-x5 needs 2.1M steps (stated as 14 times fewer), BN-x30 reaches 74.8%, and BN-x5-Sigmoid reaches 69.8% while Inception with sigmoid never beats 1/1000 accuracy. The BN-x5/x30 speed-ups combine BN with other changes (a 5x or 30x larger initial learning rate, Dropout removed, L2 weight cut 5x, learning rate decayed 6x faster, Local Response Normalization removed, more thorough shuffling, fewer photometric distortions), so they are not an isolated measure of BN. The paper frames the mechanism as an expectation and conjecture: it 'expects' fixed input distributions to speed training, 'conjectures' that BN may bring layer Jacobian singular values close to 1, and says the precise effect of BN on gradient propagation remains an area of further study.

**System answer.** ## Evidence that BN reduces internal covariate shift

The paper's main empirical evidence comes from the MNIST experiment in Section 4.1. Using a simple network with 3 fully-connected sigmoid hidden layers (100 activations each), the authors compared the distribution of inputs to a typical sigmoid unit (last hidden layer) over training, with and without BN:

- "The distributions in the original network change significantly over time, both in their mean and the variance, which complicates the training of the subsequent layers. In contrast, the distributions in the batch-normalized network are much more stable as training progresses, which aids the training." [BatchNorm, p.6]
- This is visualized as the {15, 50, 85}th percentiles of the input distribution over training steps: "Batch Normalization makes the distribution more stable and reduces the internal covariate shift." [BatchNorm, p.5-6]

Alongside this, the batch-normalized MNIST network also achieved higher test accuracy over training steps than the unnormalized baseline [BatchNorm, p.5-6], which the authors present as corroborating evidence that reduced covariate shift aids training.

## ImageNet training speed-up and what else was changed

The abstract states: "Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps, and beats the original model by a significant margin." [BatchNorm, p.1]

Elsewhere (Section 2, restating the ImageNet result) the paper gives a different figure: "we can match its performance using only 7% of the training steps, and can further exceed its accuracy by a substantial margin." [BatchNorm, p.2] (7% of training steps ≈ a 1/0.07 ≈ 14.3-fold reduction, consistent with the "14 times fewer" figure in the abstract.)

Besides simply adding BN to the Inception network, the authors made additional modifications to fully exploit BN and achieve this speedup (Section 4.2.1, "Accelerating BN Networks"):
- **Increase learning rate** — "we have been able to achieve a training speedup from higher learning rates, with no ill side effects." [BatchNorm, p.8]
- **Remove Dropout** — "Removing Dropout from Modified BN-Inception speeds up training, without increasing overfitting." [BatchNorm, p.8]
- **Reduce the L2 weight regularization** [BatchNorm, p.8] (passage cuts off here, but this is listed as a third change).

So the "14x fewer steps" / "beats the original by a significant margin" result reflects not just adding BN, but BN combined with these additional training-recipe changes. The paper also explicitly frames this: "Merely adding Batch Normalization to a state-of-the-art image classification model yields a substantial speedup in training. By further increasing the learning rates, removing Dropout, and applying other modifications afforded by Batch Normalization, we reach the previous state of the art with only a small fraction of training steps – and then beat the state of the art." [BatchNorm, p.8]

## What the paper itself says it has not established

The paper is explicit about the limits of its own claims regarding gradient propagation and the normalized values:

- "In reality, the transformation is not linear, and the normalized values are not guaranteed to be Gaussian nor independent, but we nevertheless expect Batch Normalization to help make gradient propagation better behaved. The precise effect of Batch Normalization on gradient propagation remains an area of further study." [BatchNorm, p.5-6]

The passages provided do not show the paper directly quantifying or isolating "internal covariate shift" with a precise numerical metric separate from the qualitative percentile-stability plot — this evidence does not establish a rigorous, standalone measurement of internal covariate shift reduction independent from the training-stability/accuracy observations described above.

**Retrieved:** BatchNorm p.1 (0.86); BatchNorm p.8 (0.85); BatchNorm p.2 (0.84); BatchNorm p.5-6 (0.84); BatchNorm p.6 (0.82) | gold page hit: 0.75
*15.6 s*

## Q09 (text-only, conceptual, hard, answerable: yes)

**Question.** According to the Temporal Straightening paper, why should reducing the curvature of latent trajectories make gradient-based planning easier, and how well do the paper's experiments support that claim?

**Reference answer.** A curvature regulariser penalises the angle between consecutive latent velocity vectors (maximising their cosine similarity) while a JEPA-style predictor is trained with stop-gradient on the target. The authors argue this makes Euclidean latent distance a better proxy for geodesic distance and improves conditioning of the planning objective. Theory: under linear latent dynamics, epsilon-straight transitions bound the condition number of the planning Hessian, so gradient descent converges faster; guarantees for nonlinear predictors are left to future work. Empirically, the loss landscape looks closer to convex after straightening (Figure 4) and the paper reports open-loop planning success improving by 20-60% and MPC by 20-30% (without saying here whether these are absolute points or relative changes). However, Table 1 is not uniformly positive: e.g., for a from-scratch ResNet encoder (1x384) on PointMaze-UMaze, open-loop success falls from 82.00 to 52.00 when the curvature loss is added, so the improvement claim holds for the headline configurations rather than every row.

**System answer.** ## Why reducing curvature should help gradient-based planning

The paper's core argument rests on two linked claims:

1. **Euclidean distance as a proxy for geodesic distance.** Planning objectives typically minimize a Euclidean goal cost between predicted latent states and a target in latent space. If latent trajectories are highly curved, "straight-line distances in embedding space misrepresent the geodesic distance along feasible transitions" [TemporalStraightening, p.1-2]. By encouraging locally straightened latent trajectories via a curvature regularizer, the paper aims to make "the Euclidean distance in latent space a better proxy for the geodesic distance" [TemporalStraightening, p.1], so that minimizing Euclidean distance in the cost function actually corresponds to minimizing the true (feasible-path) distance to the goal.

2. **Conditioning of the optimization landscape.** The paper states that "reducing curvature this way... improves the conditioning of the planning objective" [TemporalStraightening, p.1] and explicitly claims to "prove that reducing curvature improves convergence of gradient-based planners" [TemporalStraightening, p.2]. The intuition is that a highly non-convex, curved latent landscape causes gradient-based optimizers to struggle [TemporalStraightening, p.1-2], whereas straighter trajectories (as visualized in Figure 2, where PCA plots show smoother curves and MSE-to-target decreasing more monotonically with time after straightening) yield a better-conditioned, more gradient-friendly objective [TemporalStraightening, p.1-2].

## How well do the experiments support this claim?

**Supporting evidence:**

- **Qualitative visualization**: Figure 2 shows latent trajectories (PushT rotation example, UMaze navigation example) before and after straightening — PCA projections show visibly less curved paths, and the MSE-to-target curves become smoother/more monotonic after straightening, consistent with Euclidean distance better tracking geodesic progress [TemporalStraightening, p.1-2].

- **Quantitative planning results**: The paper reports that with the curvature regularizer, "open-loop planning success improves by 20–60% and MPC by 20–30% with a simple gradient-based planner" [TemporalStraightening, p.2]. The results table shows large gains from adding straightening — e.g., for a ResNet-based model without regularization, success rates across four conditions were 13.33±3.77, 29.33±9.43, 14.67±6.80, 48.00±9.80, whereas with the curvature regularizer (✓) the same ResNet model achieved 10.67±4.99, 33.33±4.99, 76.00±6.53, 98.67±1.89 [TemporalStraightening, p.9-10]. The large jumps in the third and fourth conditions (14.67→76.00 and 48.00→98.67) are consistent with improved planning when curvature is reduced.

- **Distance-heatmap evidence**: The appendix states that "With straightening, the latent distance accurately reflects the minimum number of steps required to reach the target," compared against ground-truth A-star distance heatmaps [TemporalStraightening, p.19-20], directly supporting the claim that straightening improves the Euclidean-to-geodesic correspondence.

- **Formal convergence claim**: The paper asserts a proof that curvature reduction improves gradient-based planner convergence [TemporalStraightening, p.2], though the passages provided do not include the proof itself, so the mathematical substantiation cannot be verified from the given evidence.

**Caveats/limitations evident in the passages:**

- The ablation table [TemporalStraightening, p.9-10] shows the benefit is not uniform: in the first condition, the non-regularized ResNet (13.33±3.77) slightly outperforms the regularized one (10.67±4.99), and the "+Proj" variant (20.00±0.00) also beats the plain regularized ResNet (13.33±4.62) in that same condition. This indicates the improvement from curvature regularization is not consistent across all tested settings/conditions.

- The authors themselves note a limitation: the goal cost is symmetric Euclidean, "which may be sub-optimal under asymmetric or irreversible dynamics," and that regularization and planning may not operate in the same space, since "the gains from using an aggregation head for long-horizon planning suggest that regularization and planning objectives do not necessarily operate in the prediction latent space" [TemporalStraightening, p.9-10]. This suggests the straightening-improves-planning mechanism is more nuanced than a single global effect, and some gains come from combining straightening with a separate aggregation/projection head rather than curvature reduction alone.

**Summary**: The paper supports its claim with a mix of qualitative visualization (straighter PCA trajectories, better-aligned MSE-to-target curves), a stated (but not shown in these passages) theoretical convergence result, and quantitative gains in goal-reaching success rates (e.g., 14.67→76.00 and 48.00→98.67 in one ResNet setting) [TemporalStraightening, p.9-10]. However, the evidence given does not include the proof itself, and the ablation results show at least one condition where the non-regularized model outperforms the regularized one, so the empirical support, while generally strong in aggregate, is not uniformly consistent across all tested conditions based on the passages provided.

**Retrieved:** TemporalStraightening p.1 (0.86); TemporalStraightening p.9-10 (0.82); TemporalStraightening p.1-2 (0.79); TemporalStraightening p.2 (0.78); TemporalStraightening p.19-20 (0.78) | gold page hit: 0.29
*21.2 s*

## Q11 (text-only, cross-paper, medium, answerable: yes)

**Question.** ViT says it follows the original Transformer 'as closely as possible'. Which parts of the Transformer encoder does ViT keep, and how does its encoder differ from the one in 'Attention Is All You Need' (input handling, position information, normalisation placement, feed-forward activation)?

**Reference answer.** ViT keeps the Transformer encoder structure of alternating multi-head self-attention and position-wise MLP/feed-forward blocks with residual connections and layer normalisation, and uses the encoder only. Differences: (1) input - ViT splits an image into patches, linearly projects them and prepends a learnable [class] token, whereas the Transformer embeds discrete input tokens; (2) position information - ViT uses standard learnable 1D position embeddings, the Transformer uses fixed sinusoidal encodings (though it found learned embeddings nearly identical); (3) normalisation - the Transformer computes LayerNorm(x + Sublayer(x)) after the residual addition, while ViT applies layer norm before every block and residual connections after every block; (4) the feed-forward layer uses ReLU in the Transformer and GELU in ViT. The Transformer paper additionally has a decoder with encoder-decoder attention.

**System answer.** Based on the provided passages, the evidence only partially answers this question. Here is what is supported, and what is not covered.

**What ViT keeps from the standard Transformer encoder**

- ViT states it interprets an image as "a sequence of patches and process[es] it by a standard Transformer encoder as used in NLP" [ViT, p.9]. This indicates the encoder block structure itself (the Transformer encoder) is retained as-is.
- ViT retains the practice of adding a positional signal to the input representations before feeding them into the Transformer encoder: "a learned position embedding is added to the patch representations" [ViT, p.8-9], and position embeddings are "added... before feeding the inputs to the Transformer encoder (default across all other experiments in this paper)" [ViT, p.18-19].

**How ViT's encoder differs, per the passages**

- *Input handling*: Instead of token embeddings from text, "the first layer of the Vision Transformer linearly projects the flattened patches into a lower-dimensional space" [ViT, p.8-9], and the learned filters resemble "basis functions for a low-dimensional representation of the fine structure within each patch" [ViT, p.8-9]. So the input to the encoder is a linear projection of flattened image patches rather than word/subword tokens.
- *Position information*: ViT uses learned positional embeddings, and the paper explicitly ablates different ways of encoding positional information — no positional embedding, 1-D learned embeddings added at the stem (the default), embeddings added "at the beginning of each layer," and layer-shared embeddings added at each layer — finding "little to no difference between different ways of encoding positional information" for patch-level inputs [ViT, p.18-19]. The passages show the learned position embeddings encode 2D image topology (row/column structure, distance similarity) [ViT, p.8-9], which the paper uses to explain why "hand-crafted 2D-aware embedding variants do not yield improvements" [ViT, p.8-9].

**What the evidence does not establish**

The provided passages do not contain any statement about normalization placement (e.g., pre-norm vs. post-norm) in ViT's encoder relative to the original Transformer, nor do they mention the feed-forward activation function used in ViT's MLP blocks versus the original Transformer's. Passage [Transformer, p.10] (the "Attention Is All You Need" excerpt) only covers constituency-parsing results and the paper's conclusion/references — it contains no architectural description of the encoder's normalization or activation either. Therefore, based solely on the given evidence, I cannot confirm or describe differences in normalization placement or feed-forward activation between ViT's encoder and the original Transformer's.

**Retrieved:** ViT p.9-10 (0.76); ViT p.18-19 (0.75); ViT p.8-9 (0.73); Transformer p.10 (0.73); ViT p.19-20 (0.72) | gold page hit: 0.17
*25.0 s*

## Q12 (text-only, cross-paper, hard, answerable: yes)

**Question.** MAE and I-JEPA both mask parts of an image and use a ViT encoder on the visible part. What does each method predict and with what loss, and what evidence does the I-JEPA paper give that predicting in representation space matters?

**Reference answer.** MAE reconstructs the pixel values of the masked patches with a lightweight decoder (mean squared error computed only on masked patches); the encoder sees only visible patches and normalised pixels work slightly better. I-JEPA is non-generative: a predictor (narrow ViT) predicts the representations of target blocks from a context block, the targets come from a target encoder that is an exponential moving average of the context encoder, and the loss is average L2 distance in representation space. In I-JEPA's own ablation (Table 7, ViT-L/16, linear probe on 1% of ImageNet labels), using target-encoder outputs gave 66.9 top-1 versus 40.7 when the loss was in pixel space, and the authors say they 'conjecture' representation-space loss is a crucial component. I-JEPA also reports about 7% slower iterations than MAE but roughly 5x fewer iterations to converge. Caveat: the pixel-space variant is I-JEPA's own ablation (different epochs: 500 vs 800), not the MAE paper's setup, and MAE does not test representation-space targets.

**System answer.** Based on the passages provided, here is what can be established:

**I-JEPA: what it predicts and the loss**
I-JEPA does not reconstruct pixels. Instead, after masking, the context (visible patches) is processed by a ViT encoder, and a **predictor network**, conditioned on positional embeddings corresponding to the location of the target block, is used to **predict the representations of target blocks** (as output by a separate target-encoder) from the single context-block representation [I-JEPA, p.13-14]. The paper states explicitly: "the proposed I-JEPA method is non-contrastive and does not seek to discriminate between image patches. Rather, the goal is to predict the representations of various target blocks from a single context block... using a predictor network that is conditioned on positional embeddings" [I-JEPA, p.13-14]. The loss is computed **entirely in representation space**, not pixel space: "a crucial component of I-JEPA is that the loss is computed entirely in representation space, thereby giving the target encoder the ability to produce abstract prediction targets, for which irrelevant pixel-level details are eliminated" [I-JEPA, p.7-8].

**MAE: what it predicts**
The passages describe MAE only as a comparison baseline and reconstruction-based method (e.g., it is grouped with "block and random masking typically used in reconstruction-based methods" [I-JEPA, p.7-8], and it uses rand-augment-style augmentations and a ViT-H/14 encoder for fine-tuning [I-JEPA, p.15-16]). **The provided passages do not state MAE's explicit loss function or confirm it reconstructs pixel values** — this is not directly established by the text given, only implied by its classification as a "reconstruction-based method" contrasted with I-JEPA's representation-space prediction.

**Evidence that predicting in representation space matters**
The paper directly tests this via an ablation: "Table 7 compares low-shot performance on 1% ImageNet-1K using a linear probe when the loss is computed in pixel-space versus representation space... it is clear that predicting in pixel-space leads to a significant degradation in the linear probing performance" [I-JEPA, p.7-8]. However, the passages provided **do not include the actual numerical values from Table 7**, so the specific magnitude of the degradation cannot be quantified from this evidence—only the qualitative claim that representation-space prediction substantially outperforms pixel-space prediction on this low-shot (1% labels) linear-probe benchmark.

**Summary of what the evidence does and does not show:**
- ✅ Shown: I-JEPA predicts target-block *representations* (not pixels), conditioned via a predictor network on positional embeddings, with loss in representation space; an ablation confirms pixel-space loss degrades linear-probe performance on 1% ImageNet.
- ❌ Not shown: The exact loss formula/type used by MAE, or the numerical Table 7 results quantifying the representation-vs-pixel-space gap.

**Retrieved:** I-JEPA p.6 (0.79); I-JEPA p.15-16 (0.78); I-JEPA p.5 (0.77); I-JEPA p.7-8 (0.76); I-JEPA p.13-14 (0.76) | gold page hit: 0.43
*20.8 s*

## Q13 (text-only, cross-paper, hard, answerable: yes)

**Question.** Distillation and BYOL both train one network to match another network's outputs. According to the two papers, what supplies the targets in each case and how does that target model come about, are labels used, and what does BYOL say about the 'mean teacher' method that it treats as closest to its slow-moving-average target?

**Reference answer.** Distillation: the targets are class probabilities from an already-trained 'cumbersome' model (an ensemble, or a single very large model trained with a strong regularizer such as dropout), softened by raising the softmax temperature. The small model is trained at the same high temperature on a transfer set and uses temperature 1 afterwards; when labels are known the objective is a weighted average of cross-entropy with the soft targets and with the correct labels, with a considerably lower weight on the label term. BYOL: the targets are the projections a target network produces for a second augmented view; the target's weights are an exponential moving average of the online network's weights (a slow-moving average of the learner itself, not a separately trained larger model), the loss gradient is not propagated into the target (stop-gradient), and an extra predictor sits only on the online branch. BYOL is a self-supervised method that works without negative pairs. BYOL describes mean teacher (MT) as also using a slow-moving-average 'teacher' to produce targets for an online 'student', with an l2 consistency loss between their softmax predictions added to a classification loss; it reports that a similar approach collapses when the classification loss is removed, whereas BYOL's added predictor prevents collapse.

**System answer.** **What the evidence shows:**

**Distillation:** No passage from a paper on (knowledge) distillation is provided in the given excerpts — all five passages are from the BYOL paper. The evidence does not establish how targets are supplied in distillation, how that target model is constructed, or whether labels are used in that setting.

**BYOL's targets:**
- The targets for the online network come from a **target network**, which is parameterized by ξ. The target network is not a separately trained model but is derived from the online network itself via a **weighted/exponential moving average of the online network's past parameters**: "ξ ← τξ + (1 − τ)θ" [BYOL, p.4-5]. This is described as "a slow-moving average of its representation to provide its targets" [BYOL, p.2-3].
- This moving-average mechanism was "inspired by deep RL," where target networks stabilize bootstrapping updates; unlike most RL methods that use fixed target networks, "BYOL uses a weighted moving average of previous networks ... in order to provide smoother changes in the target representation" [BYOL, p.2-3].
- **No labels are used** to produce these targets — BYOL is explicitly a self-supervised method; the target network's output on one augmented view is predicted from the online network's output on another augmented view of the same image, with no classification/label signal involved in generating ξ [BYOL, p.2-3; p.4-5]. At the end of training, only the online encoder fθ is kept [BYOL, p.4-5].

**BYOL's discussion of Mean Teacher (MT) as closest antecedent:**
- MT is a **semi-supervised** approach: "an unsupervised loss is combined with a classiﬁcation loss over a handful of labels to ground the training" [BYOL, p.2-3]. Like BYOL, "mean teacher (MT) [20] also uses a slow-moving average network, called teacher, to produce targets for an online network, called student. An ℓ2 consistency loss between the softmax predictions of the teacher and the student is added to the classiﬁcation loss" [BYOL, p.2-3].
- BYOL notes a key difference: MT's effectiveness has only been demonstrated in the semi-supervised case with that classification loss present, and "a similar approach collapses when removing the classiﬁcation loss" [BYOL, p.2-3]. BYOL shows this explicitly: "Removing the predictor in BYOL results in an unsupervised version of MT with no classiﬁcation loss that uses image augmentations instead of the original architectural noise (e.g., dropout). This variant of BYOL collapses (Row 7 of Table 5) which suggests that the additional predictor is critical to prevent collapse in an unsupervised scenario" [BYOL, p.9-10].
- In contrast, "BYOL introduces an additional predictor on top of the online network, which prevents collapse" even without any labels/classification loss [BYOL, p.2-3]. So BYOL frames its relationship to MT as: same slow-moving-average-teacher mechanism, but BYOL replaces MT's label-dependent classification loss with an architectural element (the predictor) that enables target generation and collapse prevention **without labels**, whereas a label-free version of MT (= BYOL without a predictor) collapses [BYOL, p.9-10].

**Summary:** For BYOL, no labels are used anywhere; targets come from an EMA target network built from the online network's own weights. For distillation, the provided passages give no information — this would require evidence from a distillation paper, which is not among the passages supplied.

**Retrieved:** BYOL p.9-10 (0.76); BYOL p.2-3 (0.75); BYOL p.30-31 (0.74); BYOL p.10-11 (0.73); BYOL p.4-5 (0.73) | gold page hit: 0.33
*17.7 s*

## Q14 (text-only, cross-paper, medium, answerable: yes)

**Question.** Temporal Straightening's world model uses a ResNet encoder, a ViT predictor and stop-gradient on the target latent. What does the Straightening paper say about how it uses each, and what does each originating paper (ResNet, ViT, BYOL) say that the component is designed to do?

**Reference answer.** Temporal Straightening offers two encoder setups, one being a ResNet (He et al.) trained from scratch, and uses a ViT (Dosovitskiy et al.) as the dynamics predictor with a temporal causal attention mask for frame-level autoregressive prediction. For collapse prevention it applies stop-gradient to the target latent in the prediction loss, citing Grill et al. 2020 (the BYOL paper) among stop-gradient methods, chosen because it needs no negative samples or extra hyper-parameters; it concedes collapse is still possible in theory but says stop-gradient worked in its experiments. In the originating papers: ResNet introduces residual learning, letting stacked layers fit F(x) = H(x) - x via shortcut connections to ease optimisation of deeper networks (the degradation problem); ViT processes a sequence of image-patch embeddings with a standard Transformer encoder of alternating self-attention and MLP blocks; and BYOL trains an online network to predict a stop-gradient target network's representation without negative pairs, which it hypothesises depends on both a predictor and a slow-moving-average target (its representation collapses if either is removed).

**System answer.** **What the Temporal Straightening paper says about its own use of each component:**

- **ResNet encoder**: The paper uses "A ResNet (He et al., 2015) trained from scratch, producing features zv_t ∈ R^(mv×dv) directly" as one of the two visual encoder (Es_φ) options, the other being a frozen pretrained DINOv2 backbone with a trainable projector [TemporalStraightening, p.5-6]. In experiments, "ResNet (from scratch)" is run both without (✗) and with (✓) the curvature loss Lcurv, and with the curvature regularizer it achieves notably higher success rates, e.g. on Wall: Open-loop 84.00 ± 7.12% / MPC 100.00 ± 0.00% (vs. 4.67 ± 3.40% / 10.00 ± 1.63% without curvature) [TemporalStraightening, p.7-8].

- **ViT predictor**: "We use a ViT (Dosovitskiy et al., 2021) as the dynamics predictor fθ." Proprioceptive states and action embeddings are concatenated with visual spatial features before being passed to this ViT, and "a temporal causal attention mask [is applied] so tokens at time t attend only to frames {t−K, ..., t−1}, enabling frame-level autoregressive prediction." [TemporalStraightening, p.5-6]

- **Stop-gradient**: In the prediction objective, "We minimize the MSE between the predicted and target latent states ẑ_t+1 and z_t+1: L_pred = ||ẑ_t+1 − sg(z_t+1)||²₂, where sg denotes the stop-" (text is cut off at the passage boundary) [TemporalStraightening, p.3-4]. This indicates the stop-gradient is applied to the target latent z_t+1 in the predictor's MSE loss, consistent with the diagram description: "we minimize the prediction loss between the predicted embedding ẑ^t_t and the target z^t_t with stop-grad in the target branch" [TemporalStraightening, p.2-3].

**What the originating papers (ResNet, ViT, BYOL) say their components are designed to do:**

The provided passages are all from the Temporal Straightening paper itself. No passages from the original ResNet paper (He et al., 2015), ViT paper (Dosovitskiy et al., 2021), or BYOL paper are included in the evidence given. Therefore, I cannot state—based on the provided evidence—what those three originating papers themselves say about the design purpose of the ResNet architecture, the ViT architecture, or the stop-gradient mechanism (note also that none of the passages explicitly cite BYOL as the source of the stop-gradient operation; the term "sg" appears only in the Temporal Straightening paper's own loss definition). To answer that part of the question, passages from He et al. (2015), Dosovitskiy et al. (2021), and the BYOL paper would be needed.

**Retrieved:** TemporalStraightening p.3-4 (0.79); TemporalStraightening p.1 (0.78); TemporalStraightening p.7-8 (0.75); TemporalStraightening p.5-6 (0.74); TemporalStraightening p.2-3 (0.74) | gold page hit: 0.20
*17.5 s*

## Q15 (text-only, cross-paper, hard, answerable: yes)

**Question.** BabyCL's visual branch applies strong augmentations to two views of each frame. Compare the Gaussian-blur and solarization probabilities it uses for its two views with those BYOL uses for its two views, and say what the two papers report about whether negative pairs are needed.

**Reference answer.** BabyCL (Appendix A): two views per frame with strong augmentation: random resized crop to 224x224 (scale 0.2-1.0), horizontal flip, color jitter, random grayscale (0.2), Gaussian blur with probability 1.0 on view 1 and 0.1 on view 2, and solarization on view 2 with probability 0.2. BYOL (Appendix B, Table 6): Gaussian blur probability 1.0 for the first view (T) and 0.1 for the second (T'), solarization 0.0 for T and 0.2 for T', color dropping (grayscale) 0.2 for both, crops covering 8%-100% of the image. The blur, solarization and grayscale probabilities therefore match, while the lower bound of the crop scale differs (0.2 versus 8%), and BabyCL does not cite BYOL for these settings. Negatives: BabyCL's instance loss is a SimCLR objective and its cross-modal loss a symmetric InfoNCE, and it cites Zhuang et al. (2021) as finding that contrastive methods with negative sampling are most effective on SAYCam. BYOL reports state-of-the-art ImageNet results without negative pairs and finds it much less affected than SimCLR when color distortion is removed from the augmentations. Neither paper tests a BYOL-style objective in a streaming child-egocentric setting.

**System answer.** ## Augmentation probabilities: Gaussian blur & solarization

**BabyCL** states explicit probabilities for its two SSL views:
> "Gaussian blur (applied with probability 1.0 on view 1 and 0.1 on view 2), and solarization on view 2 with probability 0.2." [BabyCL, p.14]

So for BabyCL: Gaussian blur = 1.0 (view 1) / 0.1 (view 2); solarization = (not stated for view 1, implicitly 0) / 0.2 (view 2).

**BYOL**: The provided BYOL passage ([BYOL, p.8-9]) does **not** give explicit per-view Gaussian-blur or solarization probabilities. It only reports the *effect* of removing or restricting augmentations:
- Removing color distortion costs BYOL −9.1 accuracy points vs. −22.2 for SimCLR [BYOL, p.8-9].
- Reducing augmentations to random crops only: BYOL drops to 59.4% (−13.1 from 72.5%), SimCLR drops to 40.3% (−27.6 from 67.9%) [BYOL, p.8-9].

**Comparison conclusion:** The evidence only allows a direct numeric comparison of blur/solarization probabilities on BabyCL's side; the BYOL passage does not report these specific probabilities, so a like-for-like numerical comparison cannot be made from the given evidence. What the BYOL passage does show is that BYOL's performance is more robust to the removal of these kinds of augmentations than SimCLR's, which the authors attribute to BYOL "retaining additional features" beyond what contrastive losses like SimCLR need [BYOL, p.8-9].

## What the papers report about negative pairs

Neither passage contains an explicit statement using the term "negative pairs" to argue for or against their necessity, so this cannot be fully established from the given evidence. What the passages do show:

- **BabyCL**: Its visual branch loss is "NT-Xent on paired augmented views" (SimCLR-style) and its multimodal branch optimizes "symmetric image–text InfoNCE" [BabyCL, p.14]. Both NT-Xent and InfoNCE are contrastive losses that operate over paired positive and (implicitly) negative examples in a batch, but the passage does not explicitly discuss whether negative pairs are "needed" — it simply specifies the losses used.
- **BYOL**: The passage discusses ablations over the **predictor**, **target network**, and a **β** parameter in a table of "intermediate variants between BYOL and SimCLR" [BYOL, p.8-9], and separately shows that a stop-gradient target (τ=0) "destabilizes training, yielding very poor performance" [BYOL, p.8-9]. However, the passage text does not define what β represents, and it never explicitly states a conclusion about negative pairs being required or not.

**Bottom line:** The evidence establishes BabyCL's exact blur/solarization probabilities (1.0/0.1 for blur, —/0.2 for solarization) but not BYOL's equivalent numbers, and it does not contain an explicit statement from either paper about whether negative pairs are needed — only indirect signals (loss function names for BabyCL; an unexplained β-parameter ablation table for BYOL).

**Retrieved:** BabyCL p.7-8 (0.78); BabyCL p.8-9 (0.78); BabyCL p.14 (0.76); BYOL p.8-9 (0.76); BabyCL p.5-6 (0.76) | gold page hit: 0.29
*47.3 s*

## Q16 (text-only, cross-paper, hard, answerable: yes)

**Question.** Daily Oracle uses a particular retriever in its retrieval-augmented setting. What is it, and what does the embedding-retrieval paper report about how that type of retriever behaves compared with dense embedding models on its LIMIT task?

**Reference answer.** Daily Oracle's constrained open-book setting uses BM25 to retrieve the top 5 articles per question, each truncated to 512 words, restricted to articles available before the resolution date and RAG cutoff. The embedding-retrieval paper finds that on LIMIT, state-of-the-art dense single-vector models struggle (full setting rarely reaches even 20% recall@100; on the 46-document version they cannot solve the task even at recall@20), whereas BM25 'comes close to perfect scores'. The authors attribute this to sparse models behaving like single vectors with very high dimensionality, but add that it is unclear how to apply sparse models to instruction-following or reasoning tasks without lexical overlap. The LIMIT result concerns a synthetic combinatorial task and says nothing about Daily Oracle's news-forecasting data.

**System answer.** The provided passages do not establish an answer to this question.

**On Daily Oracle's retriever:** Passages [1] and [2] describe the Daily Oracle dataset (its construction, categories, example QA pairs, and temporal-frequency analysis) but contain no mention of a retrieval-augmented setting or which retriever Daily Oracle uses. Nothing in the given excerpts specifies this.

**On the embedding-limitations paper's LIMIT task:** Passages [3] and [4] describe the LIMIT dataset as a stress test showing that "even state-of-the-art [dense/single-vector] embedding models" fail or find it "impossible... with current optimization techniques for retrieval" [EmbeddingLimits, p.2-3] due to the dimensionality limits proven in the paper. The paper's abstract notes it "calls for future research to develop methods that can resolve this fundamental limitation" and suggests alternatives such as "cross-encoders or multi-vector models" [EmbeddingLimits, p.2-3]. However, none of the provided passages report a specific quantitative or qualitative comparison of BM25 (or any particular retriever type) against dense embedding models' performance specifically on the LIMIT task.

**What the evidence does show instead:** Passage [5] discusses BM25 as a retriever, but this is in the context of the SWE-bench paper (comparing BM25 retrieval recall against an "oracle" retrieval setting for code file retrieval), not in connection with Daily Oracle or the LIMIT dataset [SWE-bench, p.5-6].

**Conclusion:** Based solely on the passages given, I cannot identify which retriever Daily Oracle uses, nor can I report what EmbeddingLimits says about that retriever's behavior relative to dense embeddings on LIMIT — the passages simply do not contain this information.

**Retrieved:** DailyOracle p.3 (0.75); DailyOracle p.4-5 (0.74); EmbeddingLimits p.2-3 (0.73); EmbeddingLimits p.1 (0.73); SWE-bench p.5-6 (0.73) | gold page hit: 0.20
*14.1 s*

## Q17 (text-only, cross-paper, medium, answerable: yes)

**Question.** Daily Oracle and FIRE-Bench both use LLMs inside their evaluation pipelines. How does each validate that automated component against human judgment, and what agreement numbers does each report?

**Reference answer.** Daily Oracle validated its LLM-based QA filtering: four human annotators rated 30 TF and 30 MC sampled QA pairs on the seven filtering principles; inter-annotator agreement was fair (average Fleiss' kappa 0.26), and the LLM scores matched the human consensus with 89.52% accuracy across the seven principles and 85.00% for the final accept/reject decision (threshold of 13 points). FIRE-Bench validated its automated claim extraction and entailment-based scoring by human validation on a 33% subset of reference instances, reporting precision 0.95, recall 0.86 and F1 0.89. The two validate different components (question quality versus claim matching) with different metrics, so the numbers are not directly comparable.

**System answer.** Based on the provided passages, **neither paper's agreement numbers are given here**, though both mention validation-related elements:

**Daily Oracle:**
- The dataset uses an LLM-based pipeline for question generation, and a separate LLM (GPT-3.5) is used to categorize each question into topics, "based on the prompt from Halawi et al. (2024)" [DailyOracle, p.4-5].
- The paper explicitly signals a human-validation step: "Section 3.3, we conduct a human..." [DailyOracle, p.3], but the passage is cut off before describing the procedure or reporting any agreement statistic. **No numerical agreement value appears in the supplied excerpts.**

**FIRE-Bench:**
- The abstract states that FIRE-BENCH is designed specifically to move *away from* "LLM-as-judge scoring of generated papers," which it characterizes as a "coarse proxy for scientific reasoning" [FIRE-Bench, p.1]. Instead, agent outputs are "scored against the study's documented findings" [FIRE-Bench, p.1].
- The passage does not describe the internal mechanics of this scoring (e.g., whether it uses an LLM judge at all) or report any human-agreement statistic.

**Conclusion:** The evidence provided does not establish how either benchmark validates its automated/LLM components against human judgment, nor does it supply any agreement numbers (e.g., accuracy, Cohen's kappa, F1 vs. human annotators) for either Daily Oracle or FIRE-Bench. What the passages do show is that Daily Oracle references a human-related step in "Section 3.3" (content not included) and uses GPT-3.5 for question categorization, while FIRE-Bench explicitly critiques LLM-as-judge approaches and instead scores agents against documented study findings rather than human ratings — but no agreement figures are present in the excerpts given.

**Retrieved:** DailyOracle p.3 (0.74); DailyOracle p.1 (0.71); FIRE-Bench p.1 (0.70); DailyOracle p.4-5 (0.70); DailyOracle p.17-19 (0.70) | gold page hit: 0.50
*13.5 s*

## Q18 (text-only, insufficient-evidence, medium, answerable: no)

**Question.** According to the distillation paper, what accuracy does a single network reach on the JFT dataset after the knowledge in the specialist models has been distilled back into it?

**Reference answer.** The supplied paper does not establish this. For JFT it reports an ensemble of a generalist baseline plus 61 specialist models whose predictions are combined at inference time (top-1 test accuracy 25.0% to 26.1%, a 4.4% relative improvement; conditional accuracy 43.1% to 45.9%), and it states 'We have not yet shown that we can distill the knowledge in the specialists back into the single large net'. A related idea (using soft targets to stop specialists overfitting) is described as one it is 'currently exploring'. Where the paper does distill, it reports MNIST and speech results (a single acoustic model recovering more than 80% of the frame-accuracy gain of a 10-model ensemble), not JFT.

**System answer.** The evidence does not establish this. The paper explicitly states that distilling the specialists' knowledge back into the single large net has not yet been done: "We have not yet shown that we can distill the knowledge in the specialists back into the single large net." [Distillation, p.8-9]

What the passages *do* show on JFT is only the effect of running the ensemble (generalist + specialists) at inference time without any distillation step: with 61 specialist models, there is a 4.4% relative improvement in test accuracy overall compared to the baseline full network [Distillation, p.5-6/7-8]. No accuracy figure is given for a distilled single network incorporating the specialists' knowledge.

**Retrieved:** Distillation p.7-8 (0.78); Distillation p.5 (0.77); Distillation p.5-6 (0.76); Distillation p.3-4 (0.74); Distillation p.8-9 (0.73) | gold page hit: 1.00
*6.0 s*

## Q20 (text-only, insufficient-evidence, easy, answerable: no)

**Question.** According to the SWE-bench paper, what resolve rate do agent-based systems (models that run code, navigate the repository and iterate) reach on SWE-bench?

**Reference answer.** The supplied paper does not establish this. It evaluates single-pass language models (ChatGPT-3.5, GPT-4, Claude 2 and others, and the fine-tuned SWE-Llama) that are given BM25-retrieved or oracle files and generate one patch, and its main-text resolve rates are all single-digit percentages (for example Claude 2 resolves 4.8% with oracle retrieval). Agent-based methods appear only as an intended direction: the task can serve as a level playing field for approaches 'ranging from retrieval and long-context models to decision-making agents', and the authors 'encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs)'. No agent results are reported.

**System answer.** The provided passages do not report a resolve rate for agent-based systems on SWE-bench. The paper explicitly states that its experiments only establish baselines using "the simplest and most straight-forward approaches," and it defers agent-based evaluation to future work: "we do not intend to constrain future methodologies to the same type of approach and encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs)" [SWE-bench, p.9-11].

What the passages do show instead are results for the non-agentic models actually tested: under the "Oracle" retrieval setting, Claude 2 resolves 4.80%, SWE-Llama 13b resolves 3.97%, SWE-Llama 7b resolves 3.01%, GPT-4 resolves 1.74%, and ChatGPT-3.5 resolves 0.52% [SWE-bench, p.26-27, Table 18]. The abstract separately states the best-performing model overall, Claude 2, solves "a mere 1.96%" of issues (likely under the default BM25 retrieval setting) [SWE-bench, p.1].

So, based on the evidence given, there is no stated resolve rate for agent-based systems in this paper.

**Retrieved:** SWE-bench p.1 (0.77); SWE-bench p.26-27 (0.75); SWE-bench p.9-11 (0.75); SWE-bench p.3-4 (0.73); SWE-bench p.2-3 (0.73) | gold page hit: 0.50
*8.1 s*

## Q21 (table-only, tabular, medium, answerable: yes)

**Question.** Among result rows with at most 30 million parameters, which three have the highest ImageNet-Sketch top-1, and what is each one's ImageNet validation top-1?

**Reference answer.** 1) resnext50_32x4d.fb_swsl_ig1b_ft_in1k (224 px, 25.03M params): Sketch 50.532, validation 82.162. 2) resnet50.fb_swsl_ig1b_ft_in1k (224 px, 25.56M): Sketch 49.516, validation 81.146. 3) tiny_vit_21m_512.dist_in22k_ft_in1k (512 px, 21.27M): Sketch 47.238, validation 86.444. The model with the highest Sketch score is not the one with the highest validation accuracy.

**System answer.** Based on the database query results, among models with ≤30M parameters, the three with the highest ImageNet-Sketch top-1 accuracy are:

1. **resnext50_32x4d.fb_swsl_ig1b_ft_in1k** — ImageNet-Sketch top-1: 50.532; ImageNet validation top-1: 82.162
2. **resnet50.fb_swsl_ig1b_ft_in1k** — ImageNet-Sketch top-1: 49.516; ImageNet validation top-1: 81.146
3. **tiny_vit_21m_512.dist_in22k_ft_in1k** — ImageNet-Sketch top-1: 47.238; ImageNet validation top-1: 86.444

**SQL:** `SELECT model, top1_sketch, top1_val FROM model_results WHERE param_count_m <= 30 ORDER BY top1_sketch DESC LIMIT 3;` | overlap with reference result: 0.64
*9.0 s*

## Q23 (table-only, tabular, medium, answerable: yes)

**Question.** Among rows with ImageNet validation top-1 of at least 85%, which three lose the least accuracy when moving from ImageNet validation to ImageNet-Sketch?

**Reference answer.** 1) vit_so400m_patch14_siglip_gap_378.webli_ft_in1k (378 px): validation 89.056, Sketch 71.717, change -17.339. 2) vit_so400m_patch14_siglip_378.webli_ft_in1k (378 px): 89.41 to 71.489, change -17.921. 3) eva_giant_patch14_336.clip_ft_in1k (336 px): 89.462 to 71.2, change -18.262.

**System answer.** Based on the database query results, among models with ImageNet validation top-1 ≥ 85%, the three with the smallest accuracy drop (least negative top1_diff_sketch) moving to ImageNet-Sketch are:

| Rank | Model | Img Size | top1_val | top1_sketch | Drop (top1_diff_sketch) |
|---|---|---|---|---|---|
| 1 | vit_so400m_patch14_siglip_gap_378.webli_ft_in1k | 378 | 89.056 | 71.717 | -17.339 |
| 2 | vit_so400m_patch14_siglip_378.webli_ft_in1k | 378 | 89.41 | 71.489 | -17.921 |
| 3 | eva_giant_patch14_336.clip_ft_in1k | 336 | 89.462 | 71.2 | -18.262 |

So the ranking (least to slightly more loss) is:

1. **vit_so400m_patch14_siglip_gap_378.webli_ft_in1k** — drops 17.339 points (89.056 → 71.717)
2. **vit_so400m_patch14_siglip_378.webli_ft_in1k** — drops 17.921 points (89.41 → 71.489)
3. **eva_giant_patch14_336.clip_ft_in1k** — drops 18.262 points (89.462 → 71.2)

Interestingly, the model with the lowest absolute top1_val (89.056%) actually has the *smallest* drop to ImageNet-Sketch among these three, while the model with the highest top1_val (89.462%) has the largest drop — i.e., higher clean accuracy doesn't guarantee better sketch robustness in this top-tier group.

**SQL:** `SELECT model, img_size, top1_val, top1_sketch, top1_diff_sketch FROM model_results WHERE top1_val >= 85 AND top1_sketch IS NOT NULL ORDER BY top1_diff_sketch DESC LIMIT 3;` | overlap with reference result: 1.00
*12.8 s*

## Q24 (table-only, tabular, medium, answerable: yes)

**Question.** Consider the five ResNet depths (resnet18, 34, 50, 101, 152) at 224 px. Among weight tags that exist for all five depths, which tag has the highest mean ImageNet top-1, and which has the largest gap between resnet152 and resnet18?

**Reference answer.** Five tags exist for all five depths. Highest mean top-1: a1_in1k (78.36; depths 71.504, 76.42, 80.382, 81.494, 81.998), then a2_in1k 77.818, gluon_in1k 76.403, a3_in1k 75.936, tv_in1k 74.988. Largest resnet152-minus-resnet18 gap: a3_in1k at 12.298 points (68.25 to 80.548); the smallest is tv_in1k at 8.578.

**System answer.** Based on the database query results across the five weight tags that have entries for all five ResNet depths (18, 34, 50, 101, 152) at 224 px:

**Highest mean top-1 accuracy:** `a1_in1k`, with a mean top-1 of **78.3596%** across the five depths.

**Largest resnet152 − resnet18 gap:** `a3_in1k`, with a gap of **12.298** percentage points.

Supporting values from the query:

| weights_tag | mean_top1 | gap_152_18 |
|---|---|---|
| a1_in1k | 78.3596 | 10.494 |
| a2_in1k | 77.818 | 11.130 |
| gluon_in1k | 76.4032 | 8.868 |
| a3_in1k | 75.9364 | **12.298** |
| tv_in1k | 74.988 | 8.578 |

So `a1_in1k` is best on average accuracy, while `a3_in1k` shows the steepest improvement from resnet18 to resnet152, despite having the lowest mean top-1 of the five tags.

**SQL:** `WITH tagged AS (   SELECT     CASE       WHEN arch = 'resnet18' THEN 18       WHEN arch = 'resnet34' THEN 34       WHEN arch = 'resnet50' THEN 50       WHEN arch = 'resnet101' THEN 101       WHEN arch = 'resnet152' THEN 152     END AS depth,     weights_tag,     top1_val   FROM model_results   WHERE img_size = 224     AND arch IN ('resnet18','resnet34','resnet50','resnet101','resnet152') ), valid_tags AS (   SELECT weights_tag   FROM tagged   GROUP BY weights_tag   HAVING COUNT(DISTINCT depth) = 5 ), agg AS (   SELECT     t.weights_tag,     AVG(t.top1_val) AS mean_top1,     MAX(CASE WHEN t.depth = 152 THEN t.top1_val END) -     MAX(CASE WHEN t.depth = 18 THEN t.top1_val END) AS gap_152_18   FROM tagged t   JOIN valid_tags v ON t.weights_tag = v.weights_tag   GROUP BY t.weights_tag ) SELECT weights_tag, mean_top1, gap_152_18,   (SELECT weights_tag FROM agg ORDER BY mean_top1 DESC LIMIT 1) AS best_mean_tag,   (SELECT weights_tag FROM agg ORDER BY gap_152_18 DESC LIMIT 1) AS best_gap_tag FROM agg ORDER BY mean_top1 DESC;` | overlap with reference result: 0.94
*13.4 s*

## Q25 (table-only, tabular, hard, answerable: yes)

**Question.** For the ResNet depths with the a1_in1k weights at 224 px, going from each depth to the next one, how many ImageNet top-1 points are gained per added GMAC, and which step gives the least?

**Reference answer.** Ordering by GMACs gives resnet18 (1.82), resnet34 (3.67), resnet50 (4.11), resnet101 (7.83), resnet152 (11.56). Top-1 gain per added GMAC: 18 to 34: +4.916 for +1.85 GMACs = 2.657; 34 to 50: +3.962 for +0.44 = 9.005; 50 to 101: +1.112 for +3.72 = 0.299; 101 to 152: +0.504 for +3.73 = 0.135. The least is resnet101 to resnet152 (0.135 points per GMAC).

**System answer.** Based on the query over the `timm` database (ResNet architectures, `a1_in1k` weights, 224 px), here is the top‑1 gain per added GMAC for each consecutive depth transition (ordered ascending by top1_per_gmac):

| depth_from → depth_to | top1_gain (pts) | gmac_gain | top1 pts per GMAC |
|---|---|---|---|
| 101 → 152 | 0.504 | 3.73 | **0.1351** |
| 50 → 101 | 0.764 | 3.48 | 0.2195 |
| 50 → 101 | 1.112 | 3.72 | 0.2989 |
| 18 → 34 | 4.916 | 1.85 | 2.6573 |
| 34 → 50 | 4.310 | 0.68 | 6.3382 |
| 34 → 50 | 3.962 | 0.44 | 9.0045 |

(0.504/3.73 = 0.1351, 0.764/3.48 = 0.2195, 1.112/3.72 = 0.2989, 4.916/1.85 = 2.6573, 4.310/0.68 = 6.3382, 3.962/0.44 = 9.0045 — matching the `top1_per_gmac` column returned.)

**Least efficient step:** 101 → 152, at only ≈0.135 top‑1 points gained per added GMAC. This is the smallest value in the result set, meaning the jump from ResNet‑101 to ResNet‑152 buys the least accuracy improvement per unit of added compute among all the depth transitions in the table.

Note: the 50→101 and 34→50 transitions each appear twice with slightly different gains/GMACs — this is a direct artifact of the SQL result (likely from multiple matching architecture variants whose name encodes the same leading depth digits, e.g. different resnet50/resnet34 variants being grouped by `CAST(SUBSTR(arch,7) AS INTEGER)`), not something resolvable from the data given. The ranking and the identification of the worst step (101→152) are unaffected by this duplication.

**SQL:** `WITH r AS (   SELECT     mr.arch,     CAST(SUBSTR(mr.arch, 7) AS INTEGER) AS depth,     mr.top1_val,     bi.gmacs   FROM model_results mr   JOIN benchmark_infer bi     ON mr.arch = bi.arch AND mr.img_size = bi.img_size   WHERE mr.weights_tag = 'a1_in1k'     AND mr.img_size = 224     AND mr.arch LIKE 'resnet%'     AND SUBSTR(mr.arch, 7) GLOB '[0-9]*' ), steps AS (   SELECT     r1.depth AS depth_from,     r2.depth AS depth_to,     r2.top1_val - r1.top1_val AS top1_gain,     r2.gmacs - r1.gmacs AS gmac_gain,     (r2.top1_val - r1.top1_val) / (r2.gmacs - r1.gmacs) AS top1_per_gmac   FROM r r1   JOIN r r2     ON r2.depth = (       SELECT MIN(depth) FROM r r3 WHERE r3.depth > r1.depth     ) ) SELECT   depth_from,   depth_to,   top1_gain,   gmac_gain,   top1_per_gmac FROM steps ORDER BY top1_per_gmac ASC;` | overlap with reference result: 0.75
*23.5 s*

## Q27 (table-only, tabular, medium, answerable: yes)

**Question.** For the torchvision-style weights (tag tv_in1k) of the five ResNet depths at 224 px, how does the accuracy drop from ImageNet validation to ImageNet-V2 change with depth, and which depth has the largest drop?

**Reference answer.** ImageNet-V2 change (V2 top-1 minus validation top-1) by depth: resnet18 -12.402 (69.752 to 57.35), resnet34 -12.088, resnet50 -12.966, resnet101 -11.464, resnet152 -11.29. The largest drop is resnet50 (-12.966); the smallest is resnet152 (-11.29). The trend with depth is downward overall but not monotonic (resnet50 is worse than resnet34 and resnet18).

**System answer.** ## Accuracy drop (val → ImageNet‑V2) across ResNet depths (tv_in1k, 224 px)

| Depth | top1_val | top1_v2 | Drop (top1_diff_v2) |
|---|---|---|---|
| resnet18 | 69.752 | 57.35 | **‑12.402** |
| resnet34 | 73.298 | 61.21 | **‑12.088** |
| resnet50 | 76.156 | 63.19 | **‑12.966** |
| resnet101 | 77.404 | 65.94 | **‑11.464** |
| resnet152 | 78.33 | 67.04 | **‑11.290** |

(Values from the SQL query result on the `model_results` table, filtered to `weights_tag='tv_in1k'`, `img_size=224`, for the five `resnet*` architectures.)

### How the drop changes with depth
Ordering the rows by actual network depth (18 → 34 → 50 → 101 → 152), the magnitude of the val→V2 drop is **not monotonic**:

- 18 → 34: drop shrinks slightly (12.402 → 12.088)
- 34 → 50: drop jumps up (12.088 → 12.966), the biggest single‑step increase
- 50 → 101 → 152: drop shrinks steadily and substantially (12.966 → 11.464 → 11.290)

So the pattern is: a dip at resnet34, a peak at resnet50, and then a consistent decline for the two deepest models (101, 152), which have the smallest drops of the group.

### Largest drop
**resnet50** has the largest accuracy drop from ImageNet val to ImageNet‑V2: **76.156% → 63.19%, a fall of 12.966 percentage points** — larger than any of the other four depths (18, 34, 101, 152) in this result set.

**Caveat:** This is based only on the five rows returned by the query (single `tv_in1k` checkpoint per depth); the result does not explain *why* resnet50 shows the largest drop, since no additional passage evidence was provided beyond this table.

**SQL:** `SELECT model, arch, img_size, top1_val, top1_v2, top1_diff_v2 FROM model_results WHERE weights_tag = 'tv_in1k'   AND img_size = 224   AND arch IN ('resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152') ORDER BY arch;` | overlap with reference result: 0.68
*19.0 s*

## Q29 (table-only, tabular, easy, answerable: yes)

**Question.** What is the highest ImageNet top-1 among rows with fewer than 10 million parameters, and how does it compare with the best row at 25 million parameters or fewer and the best row overall?

**Reference answer.** Under 10M parameters: mobilenetv4_conv_medium.e250_r384_in12k_ft_in1k (384 px), 82.776 top-1, 9.72M params. At most 25M: tiny_vit_21m_512.dist_in22k_ft_in1k (512 px), 86.444, 21.27M (+3.668 points). Overall: eva02_large_patch14_448.mim_m38m_ft_in22k_in1k (448 px), 90.056, 305.08M params. Relative to the overall best, the under-10M model gives up 7.28 top-1 points with about 31x fewer parameters.

**System answer.** Based on the database query results:

- **Best under 10M parameters:** 82.776 top-1
- **Best under 25M parameters:** 86.444 top-1
- **Best overall:** 90.056 top-1

**Comparison:**
- Moving from the <10M to the ≤25M parameter tier, top-1 accuracy increases by 86.444 − 82.776 = **3.668 points**.
- Moving from the <10M tier to the best overall model, accuracy increases by 90.056 − 82.776 = **7.28 points**.
- The ≤25M tier is still 90.056 − 86.444 = **3.612 points** below the best overall result, indicating the top-performing model(s) in the database have more than 25M parameters.

So there is a clear trend of increasing top-1 accuracy with larger parameter budgets in this dataset, with the largest jump occurring between the sub-25M tier and the unrestricted best model.

**SQL:** `SELECT   (SELECT MAX(top1_val) FROM model_results WHERE param_count_m < 10) AS best_under_10m,   (SELECT MAX(top1_val) FROM model_results WHERE param_count_m <= 25) AS best_under_25m,   (SELECT MAX(top1_val) FROM model_results) AS best_overall;` | overlap with reference result: 0.20
*12.0 s*

## Q30 (table-only, tabular, hard, answerable: yes)

**Question.** At 224 px, which models are on the accuracy-throughput Pareto frontier (no other 224-px model has both higher-or-equal top-1 and higher-or-equal throughput, with at least one strictly higher), how many are there, and how many of them have top-1 of at least 85%?

**Reference answer.** There are 26 frontier rows out of 783 result rows at 224 px, running from eva_giant_patch14_224.clip_ft_in1k (88.896 top-1, 240.83 samples/s) to efficientvit_m0.r224_in1k (63.304, 77,772.14 samples/s). Eleven have top-1 of at least 85%: eva_giant_patch14_224.clip_ft_in1k, beitv2_large_patch16_224.in1k_ft_in22k_in1k, beit_large_patch16_224.in22k_ft_in22k_in1k, deit3_large_patch16_224.fb_in22k_ft_in1k, convnextv2_base.fcmae_ft_in22k_in1k, mambaout_base_plus_rw.sw_e150_in12k_ft_in1k, convnext_large.fb_in22k_ft_in1k, coatnet_2_rw_224.sw_in12k_ft_in1k, beitv2_base_patch16_224.in1k_ft_in22k_in1k, vit_base_patch16_clip_224.laion2b_ft_in12k_in1k, tiny_vit_21m_224.dist_in22k_ft_in1k.

**System answer.** Based on the SQL query results, there are **26 models** on the accuracy-throughput Pareto frontier at 224 px (`total_frontier_count = 26`), and **11 of them** have top-1 ≥ 85% (`frontier_ge85_count = 11`).

**The 26 frontier models, ordered by top-1 accuracy (descending):**

| Model | top1_val | samples_per_sec |
|---|---|---|
| eva_giant_patch14_224.clip_ft_in1k | 88.896 | 240.83 |
| beitv2_large_patch16_224.in1k_ft_in22k_in1k | 88.406 | 875.21 |
| beit_large_patch16_224.in22k_ft_in22k_in1k | 87.486 | 877.09 |
| deit3_large_patch16_224.fb_in22k_ft_in1k | 86.99 | 881.59 |
| convnextv2_base.fcmae_ft_in22k_in1k | 86.752 | 961.39 |
| mambaout_base_plus_rw.sw_e150_in12k_ft_in1k | 86.642 | 1186.01 |
| convnext_large.fb_in22k_ft_in1k | 86.612 | 1214.27 |
| coatnet_2_rw_224.sw_in12k_ft_in1k | 86.582 | 1307.99 |
| beitv2_base_patch16_224.in1k_ft_in22k_in1k | 86.494 | 2714.29 |
| vit_base_patch16_clip_224.laion2b_ft_in12k_in1k | 86.204 | 3355.89 |
| tiny_vit_21m_224.dist_in22k_ft_in1k | 85.088 | 3790.67 |
| deit3_medium_patch16_224.fb_in22k_ft_in1k | 84.55 | 4876.31 |
| hgnetv2_b4.ssld_stage2_ft_in1k | 83.7 | 6126.27 |
| vit_base_patch32_clip_224.laion2b_ft_in12k_in1k | 83.304 | 12150.93 |
| levit_256.fb_dist_in1k | 81.506 | 13220.48 |
| levit_conv_192.fb_dist_in1k | 79.86 | 18017.24 |
| levit_conv_128.fb_dist_in1k | 78.488 | 20143.06 |
| shvit_s3.in1k | 77.356 | 25254.66 |
| levit_conv_128s.fb_dist_in1k | 76.534 | 30016.26 |
| levit_128s.fb_dist_in1k | 76.52 | 30353.33 |
| shvit_s2.in1k | 75.184 | 38960.54 |
| efficientvit_m3.r224_in1k | 73.394 | 40863.87 |
| shvit_s1.in1k | 72.78 | 48051.75 |
| efficientvit_m1.r224_in1k | 68.34 | 49531.88 |
| mobilenetv4_conv_small_050.e3000_r224_in1k | 64.778 | 57208.51 |
| efficientvit_m0.r224_in1k | 63.304 | 77772.14 |

**Models with top-1 ≥ 85% (11 total)** — counting from the top of the list down through `tiny_vit_21m_224.dist_in22k_ft_in1k` (85.088):
eva_giant_patch14_224.clip_ft_in1k, beitv2_large_patch16_224.in1k_ft_in22k_in1k, beit_large_patch16_224.in22k_ft_in22k_in1k, deit3_large_patch16_224.fb_in22k_ft_in1k, convnextv2_base.fcmae_ft_in22k_in1k, mambaout_base_plus_rw.sw_e150_in12k_ft_in1k, convnext_large.fb_in22k_ft_in1k, coatnet_2_rw_224.sw_in12k_ft_in1k, beitv2_base_patch16_224.in1k_ft_in22k_in1k, vit_base_patch16_clip_224.laion2b_ft_in12k_in1k, tiny_vit_21m_224.dist_in22k_ft_in1k.

(Note: this evidence comes directly from the database query result, not from a paper passage, so no citation tag applies.)

**SQL:** `WITH points AS (   SELECT m.model, m.top1_val, b.samples_per_sec   FROM model_results m   JOIN benchmark_infer b     ON m.arch = b.arch AND m.img_size = b.img_size   WHERE m.img_size = 224     AND m.top1_val IS NOT NULL     AND b.samples_per_sec IS NOT NULL ), frontier AS (   SELECT p.*   FROM points p   WHERE NOT EXISTS (     SELECT 1 FROM points p2     WHERE p2.top1_val >= p.top1_val       AND p2.samples_per_sec >= p.samples_per_sec       AND (p2.top1_val > p.top1_val OR p2.samples_per_sec > p.samples_per_sec)   ) ) SELECT   model,   top1_val,   samples_per_sec,   (SELECT COUNT(*) FROM frontier) AS total_frontier_count,   (SELECT COUNT(*) FROM frontier WHERE top1_val >= 85) AS frontier_ge85_count FROM frontier ORDER BY top1_val DESC;` | overlap with reference result: 0.74
*32.0 s*

## Q31 (text+table, cross-source, medium, answerable: yes)

**Question.** The ViT paper says smaller patches make a Transformer more expensive. Using the sequence length it implies for 224-px inputs, how do the GMACs and measured throughput of ViT-Base with 32, 16 and 8 pixel patches compare with that expectation?

**Reference answer.** The ViT paper defines the number of patches (the Transformer's sequence length) as N = HW/P^2 and says smaller patch sizes are computationally more expensive. At 224 px that gives N = 49, 196 and 784 for P = 32, 16 and 8, i.e. 4x more tokens at each step. timm shows (parameters nearly constant: 88.22M, 86.57M, 86.58M): GMACs 4.41, 17.58 and 78.22, so 3.99x from B/32 to B/16 and 4.45x from B/16 to B/8; throughput 10,936.95, 2,992.79 and 700.85 samples/s, i.e. 3.65x slower and then 4.27x slower. Cost therefore grows roughly with token count while parameters stay flat; B/8 exceeds 4x in GMACs, which the paper does not explain.

**System answer.** ## What the ViT paper's claim implies about sequence length

None of the provided passages explicitly state the "smaller patches → more expensive" rationale with its underlying formula, so I cannot cite a specific passage for *why* it is true. The passages only discuss patch sizes in the context of the scaling study (e.g., "ViT-B/32, B/16, L/32, L/16, pre-trained for 7 epochs" [ViT, p.7-8]) and attention/positional-embedding analyses [ViT, p.18-19], without quantifying sequence length vs. patch size. I'll flag this gap and instead derive the implied sequence lengths from the architecture (image is split into non-overlapping P×P patches) and compare them against the database's measured compute/throughput.

For a 224×224 input, the number of patches (sequence length, ignoring the class token) is:

N = (224 / P)²

- P = 32 → N = (224/32)² = 7² = **49**
- P = 16 → N = (224/16)² = 14² = **196**
- P = 8 → N = (224/8)² = 28² = **784**

So halving the patch size quadruples the sequence length at each step (196/49 = 4, 784/196 = 4), and since self-attention cost scales with N² while the linear/MLP layers scale with N, the "expectation" is that compute should grow faster than linearly in N as patches shrink — potentially up to 16× per halving if attention dominated.

## Comparing against the database's GMACs and throughput

From the SQL query result:

| Model (patch) | GMACs | Samples/sec | Batch size |
|---|---|---|---|
| vit_base_patch32_224 | 4.41 | 10936.95 | 1024 |
| vit_base_patch16_224 | 17.58 | 2992.79 | 1024 |
| vit_base_patch8_224 | 78.22 | 700.85 | 768 |

**GMACs ratios:**
- 16 vs 32: 17.58 / 4.41 = 3.99 ≈ 4
- 8 vs 16: 78.22 / 17.58 = 4.45

**Throughput ratios (inverse of cost):**
- 32 vs 16: 10936.95 / 2992.79 = 3.65
- 16 vs 8: 2992.79 / 700.85 = 4.27

## Interpretation

- Directionally, the data confirms the expectation: smaller patches cost more — GMACs rise (4.41 → 17.58 → 78.22) and throughput falls (10936.95 → 2992.79 → 700.85) monotonically as patch size shrinks.
- However, the magnitude of the increase is much closer to the **linear-in-N** scaling (≈4× per halving, matching the 4× growth in sequence length) than to the full **quadratic-in-N** scaling that pure self-attention cost would imply (which would predict ≈16× per halving, since N² grows 16× when N grows 4×). This suggests that for ViT-Base at 224 px resolution, the linear projection/MLP terms (which scale with N) dominate total GMACs more than the N² attention term.
- There is a hint of super-linear growth specifically going from patch16→patch8 (GMACs ratio 4.45 and throughput-drop ratio 4.27, both slightly above the pure 4× sequence-length factor), consistent with the quadratic attention term beginning to contribute more as N grows from 196 to 784.
- Note: the patch8 benchmark uses a smaller batch size (768 vs. 1024), which could modestly affect the measured throughput ratio and should be considered when interpreting the "8 vs 16" throughput comparison.

**Caveat:** The provided passages do not contain an explicit statement/derivation of the "smaller patches are more expensive" claim or its quadratic-attention rationale, so the "expectation" above is constructed from the standard patch-count formula rather than quoted text. The comparison against GMACs/throughput is therefore based on the database query results plus this derived expectation, not a passage-level claim.

**Retrieved:** ViT p.7-8 (0.75); ViT p.5-6 (0.74); ViT p.18-19 (0.74); ViT p.9-10 (0.73); ViT p.6-7 (0.73) | gold page hit: 0.50
**SQL:** `SELECT   mr.model,   mr.img_size,   bi.gmacs,   bi.samples_per_sec,   bi.batch_size FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.img_size = 224   AND mr.arch IN ('vit_base_patch32_224', 'vit_base_patch16_224', 'vit_base_patch8_224') ORDER BY mr.arch;` | overlap with reference result: 0.60
*43.8 s*

## Q32 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper reports FLOPs for its 18-, 34-, 50-, 101- and 152-layer networks. How do timm's measured GMACs at 224 px compare, and for which depth is the difference largest?

**Reference answer.** The paper's Table 1 gives 1.8, 3.6, 3.8, 7.6 and 11.3 billion FLOPs, and defines its FLOPs as multiply-adds. timm's infer_gmacs at 224 px are 1.82, 3.67, 4.11, 7.83 and 11.56, i.e. +1.1%, +1.9%, +8.2%, +3.0% and +2.3%. The largest difference is for resnet50 (4.11 vs 3.8, +8.2%). Neither PDF explains the gap, so the cause should not be asserted.

**System answer.** ## Comparison: Paper FLOPs vs. timm GMACs (224px)

The ResNet paper reports the following FLOPs for ImageNet architectures [ResNet, p.5]:

| Depth | Paper FLOPs (×10⁹) | timm GMACs | Difference (timm − paper) | % difference |
|---|---|---|---|---|
| 18 | 1.8 | 1.82 | +0.02 | 1.1% |
| 34 | 3.6 | 3.67 | +0.07 | 1.9% |
| 50 | 3.8 | 4.11 | **+0.31** | **8.2%** |
| 101 | 7.6 | 7.83 | +0.23 | 3.0% |
| 152 | 11.3 | 11.56 | +0.26 | 2.3% |

**Calculations:**
- 18: 1.82 − 1.8 = 0.02; 0.02/1.8 = 1.11%
- 34: 3.67 − 3.6 = 0.07; 0.07/3.6 = 1.94%
- 50: 4.11 − 3.8 = 0.31; 0.31/3.8 = 8.16%
- 101: 7.83 − 7.6 = 0.23; 0.23/7.6 = 3.03%
- 152: 11.56 − 11.3 = 0.26; 0.26/11.3 = 2.30%

## Which depth differs most

The **ResNet-50** model shows the largest discrepancy, both in absolute terms (+0.31 GMACs) and in relative terms (+8.2%), compared to the paper's reported 3.8×10⁹ FLOPs [ResNet, p.6].

For context, the paper notes that ResNet-50/101/152 all use the bottleneck block design (three layers: 1×1, 3×3, 1×1) with "option B" shortcuts (projection shortcuts used only for increasing dimensions) [ResNet, p.6-7, "5.71 ResNet-34 C"]. The paper's own comparison table states that the 50-, 101-, and 152-layer bottleneck designs were chosen so that "both designs have similar time complexity" to the non-bottleneck version [ResNet, p.6]. However, the passages given do not explain the specific implementation details (e.g., stride placement, exact shortcut counting, or stem/downsampling conventions) that would account for why ResNet-50 in timm's measurement diverges proportionally more than the other depths — that explanation is not established by the evidence provided here.

**Retrieved:** ResNet p.5-6 (0.76); ResNet p.5 (0.74); ResNet p.8 (0.73); ResNet p.6-7 (0.73); ResNet p.6 (0.73) | gold page hit: 0.67
**SQL:** `SELECT arch, img_size, gmacs FROM benchmark_infer WHERE img_size = 224   AND arch IN ('resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152') ORDER BY arch;` | overlap with reference result: 0.69
*18.9 s*

## Q34 (text+table, cross-source, hard, answerable: yes)

**Question.** Among timm rows whose weights tag starts with 'mae', which has the highest ImageNet-R and ImageNet-A top-1, how does robustness change with model size, and what pre-training task does the MAE paper describe?

**Reference answer.** Six hiera_*_224.mae_in1k_ft_in1k rows are tagged mae. hiera_huge_224 is highest on ImageNet-R (64.967; change vs 200-class clean -32.243), ImageNet-A (66.253) and Sketch (50.078), with 672.78M parameters. Robustness decreases steadily with size: R top-1 is 64.967 (huge), 60.29 (large), 55.57 (base_plus), 53.14 (base), 49.373 (small), 45.78 (tiny). The MAE paper describes pre-training that masks random patches (75% in its default) and reconstructs the missing pixels with an encoder that processes only the visible patches. Caveat: the MAE paper's own encoder is a plain ViT; Hiera is not in the corpus, and what the timm tag implies about Hiera's recipe is not stated in the PDFs.

**System answer.** ## Highest ImageNet-R and ImageNet-A among `mae*` tagged timm models

From the SQL query results (ordered by top1_r then top1_a descending), the top row is:

**hiera_huge_224.mae_in1k_ft_in1k** — ImageNet-R (top1_r) = 64.967, ImageNet-A (top1_a) = 66.253, with 672.78M parameters at 224px.

This is the single highest-scoring model on both robustness benchmarks among the `mae*`-tagged rows.

## How robustness scales with model size

Sorting the 6 returned rows by parameter count (tiny → huge), both robustness metrics increase monotonically with model size:

| model | params (M) | top1_r | top1_a |
|---|---|---|---|
| hiera_tiny_224 | 27.91 | 45.78 | 30.56 |
| hiera_small_224 | 35.01 | 49.373 | 36.453 |
| hiera_base_224 | 51.52 | 53.14 | 43.4 |
| hiera_base_plus_224 | 69.9 | 55.57 | 49.24 |
| hiera_large_224 | 213.74 | 60.29 | 58.013 |
| hiera_huge_224 | 672.78 | 64.967 | 66.253 |

Calculation check (tiny → huge gain): top1_r increases by 64.967 − 45.78 = 19.187 points; top1_a increases by 66.253 − 30.56 = 35.693 points as parameters grow from 27.91M to 672.78M.

This monotonic increase matches the MAE paper's own finding: "our method has strong scaling behavior: increasing the model sizes has significant gains" on robustness evaluation (ImageNet-A, -R, -C, etc.), and the paper explicitly contrasts this with supervised training, e.g. "with ViT-H, our MAE pre-training is 35% better on IN-A (68.2% vs 33.1%) than the supervised counterpart" [MAE, p.12].

## Pre-training task described by the MAE paper

The provided MAE passages don't include a full methods-section description of the pretraining objective, but the figure captions give a direct characterization: the model is shown "masked image (left), our MAE reconstruction (middle), and the ground-truth (right)," with "masking ratio is 75%" on both ImageNet and COCO validation images [MAE, p.13-14]. This indicates the pre-training task is a masked-image reconstruction task — masking a large portion (75%) of image patches and training the model to reconstruct the original (ground-truth) image content from the visible patches.

**Caveat:** This description comes only from figure captions in the supplied passages, not from an explicit "Approach/Method" section, so the full architectural details (e.g., encoder-decoder design, loss function) of the MAE pretraining task are not established by the evidence given here.

**Retrieved:** MAE p.12-14 (0.79); ViT p.13-14 (0.74); ResNet p.5-6 (0.73); I-JEPA p.12-13 (0.73); MAE p.7-8 (0.73) | gold page hit: 0.00
**SQL:** `SELECT model, arch, img_size, param_count_m, top1_r, top1_a FROM model_results WHERE weights_tag LIKE 'mae%' ORDER BY top1_r DESC, top1_a DESC;` | overlap with reference result: 0.51
*23.1 s*

## Q35 (text+table, cross-source, hard, answerable: yes)

**Question.** For ViT models released with the same augreg recipe tag, how much higher is ImageNet top-1 when the weights come from ImageNet-21k pre-training plus ImageNet-1k fine-tuning than when trained on ImageNet-1k only, does the gain depend on model size, and how does this relate to what the ViT paper says about pre-training data?

**Reference answer.** In all six matched pairs the in21k-then-in1k weights are better: vit_base_patch16_224 +5.38 (84.534 vs 79.154), vit_base_patch16_384 +4.908, vit_base_patch32_224 +5.824, vit_base_patch32_384 +4.608, vit_small_patch16_224 +2.56, vit_small_patch16_384 +2.684. Base-size models gain about 5.2 points on average and Small about 2.6, so the gain is larger for the larger model. This is directionally consistent with the ViT paper, which says larger pre-training data helps ('large scale training trumps inductive bias') and that larger models only show their benefit with more data, but the paper's evidence is at different scales (ImageNet, ImageNet-21k, JFT-300M) and includes ViT-Large, which has no pair here.

**System answer.** ## ImageNet top‑1 gain: IN‑21k pre‑train + IN‑1k fine‑tune vs. IN‑1k‑only

From the database query (weights pairs matched by architecture, `augreg_in21k_ft_in1k` vs. `augreg_in1k`):

| arch | img_size | IN‑21k‑ft‑IN‑1k top‑1 | IN‑1k‑only top‑1 | Gain (pp) |
|---|---|---|---|---|
| vit_small_patch16 | 224 | 81.402 | 78.842 | **2.56** |
| vit_small_patch16 | 384 | 83.814 | 81.130 | **2.68** |
| vit_base_patch16 | 224 | 84.534 | 79.154 | **5.38** |
| vit_base_patch16 | 384 | 86.010 | 81.102 | **4.91** |
| vit_base_patch32 | 224 | 80.732 | 74.908 | **5.82** |
| vit_base_patch32 | 384 | 83.358 | 78.750 | **4.61** |

Calculations (gain = IN21k‑ft‑IN1k − IN1k‑only):
- small/16@224: 81.402 − 78.842 = 2.560
- small/16@384: 83.814 − 81.130 = 2.684
- base/16@224: 84.534 − 79.154 = 5.380
- base/16@384: 86.010 − 81.102 = 4.908
- base/32@224: 80.732 − 74.908 = 5.824
- base/32@384: 83.358 − 78.750 = 4.608

Mean gain across the six entries ≈ (2.560+2.684+5.380+4.908+5.824+4.608)/6 = 25.964/6 ≈ **4.33 pp**, with a range of roughly **2.56 to 5.82 pp**.

## Does the gain depend on model size?

Yes, based on this data: the **"small" variant gains only ~2.6 pp**, while the **"base" variants gain ~4.6–5.8 pp** — noticeably more. So the benefit of ImageNet‑21k pre‑training (before IN‑1k fine‑tuning) is larger for the bigger ("base") models than for the smaller ("small") models in this table. (Note: image resolution does not show a consistent one‑directional effect within a given architecture — e.g., base/16 gains slightly more at 224 than 384, while base/32 behaves similarly — so size of the backbone, not resolution, is the clearer driver here.)

## Relation to the ViT paper's claims on pre‑training data

This pattern is consistent with what the original ViT paper reports about pre-training data requirements:

- "When pre-trained on the smallest dataset, ImageNet, ViT-Large models underperform compared to ViT-Base models, despite (moderate) regularization. With ImageNet-21k pre-training, their performances are similar. Only with JFT-300M, do we see the full benefit of larger models." [ViT, p.6, section 4.3]
- "ResNets perform better with smaller pre-training datasets but plateau sooner than ViT, which performs better with larger pre-training." [ViT, p.6-7, Figure 4 caption]
- "Vision Transformers overfit more than ResNets with comparable computational cost on smaller datasets... This result reinforces the intuition that the convolutional inductive bias is useful for smaller datasets, but for larger ones, learning the relevant patterns directly from data is sufficient, even beneficial." [ViT, p.6-7]

The paper's core claim is that **larger ViT models need/benefit more from larger pre-training data** than smaller ViT models do. The timm/augreg numbers from the query support this directionally: moving from IN‑1k‑only training to IN‑21k pre‑training (a strictly larger pre-training corpus) followed by IN‑1k fine‑tuning yields a **larger absolute accuracy gain for the base-sized models than for the small-sized model**, mirroring the paper's observation that bigger models reap more benefit from bigger pre-training datasets.

**Caveat:** The evidence provided does not include a direct statement from the ViT paper quantifying pp gains for IN‑21k‑ft‑IN‑1k vs. IN‑1k‑only training specifically (the paper's own Figure 3/4 comparisons use ImageNet, ImageNet‑21k, and JFT‑300M as pre‑training-only settings, not this augreg fine‑tuning protocol), so the numeric match above is a pattern‑level comparison, not a value directly stated in the ViT paper passages given.

**Retrieved:** ViT p.6-7 (0.84); MAE p.7 (0.80); ViT p.5 (0.79); ViT p.5-6 (0.78); ViT p.6-7 (0.78) | gold page hit: 0.67
**SQL:** `SELECT   m21.arch,   m21.img_size,   m21.top1_val AS top1_val_in21k_ft_in1k,   m1.top1_val AS top1_val_in1k_only,   m21.top1_val - m1.top1_val AS gain FROM model_results m21 JOIN model_results m1   ON m1.arch = REPLACE(m21.arch, '-', '')   AND m1.arch || '.augreg_in1k' = SUBSTR(m21.arch,1,0) || m1.arch || '.augreg_in1k' WHERE m21.weights_tag = 'augreg_in21k_ft_in1k'   AND m1.weights_tag = 'augreg_in1k'   AND m21.arch = m1.arch ORDER BY m21.param_count_m;` | overlap with reference result: 1.00
*32.0 s*

## Q37 (text+table, cross-source, hard, answerable: yes)

**Question.** The ViT paper reports that ViT needs roughly 2-4x less compute than ResNets for the same transfer performance. In timm at 224 px, how do ViT-B/16 and ResNet-50/101/152 compare on top-1 and measured throughput, and does that data confirm the paper's claim?

**Reference answer.** The paper's claim is about pre-training compute (Figure 5 is accuracy vs pre-training exaFLOPs, JFT-300M, controlled study), with the caveat that efficiency can depend on schedule, optimiser and weight decay. timm measures inference throughput and has no pre-training compute. At 224 px, vit_base_patch16_224.augreg2_in21k_ft_in1k has 85.108 top-1 at 2,992.79 samples/s (17.58 GMACs), versus resnet152.a1h_in1k 82.818 at 1,976.86 (11.56 GMACs), resnet101.a1h_in1k 81.95 at 2,781.19 (7.83 GMACs) and resnet50.a1h_in1k 80.654 at 4,302.84 (4.11 GMACs). So ViT-B/16 is more accurate than all three and faster than resnet152 (1.51x) and resnet101 (1.08x) despite more GMACs, but slower than resnet50. These numbers neither confirm nor refute the 2-4x pre-training-compute claim.

**System answer.** ## Data from the timm query (img_size=224, best checkpoint per architecture)

| Architecture | Best checkpoint | Top‑1 | Throughput (img/s) | GMACs | Params (M) |
|---|---|---|---|---|---|
| ViT‑B/16 | augreg2_in21k_ft_in1k | **85.108** | 2992.79 | 17.58 | 86.57 |
| ResNet‑50 | fb_swsl_ig1b_ft_in1k | 81.146 | **4302.84** | 4.11 | 25.56 |
| ResNet‑101 | a1h_in1k | 81.950 | 2781.19 | 7.83 | 44.55 |
| ResNet‑152 | a1h_in1k | 82.818 | 1976.86 | 11.56 | 60.19 |

**Accuracy:** ViT‑B/16's best checkpoint beats every ResNet's best checkpoint: +3.96 pp over ResNet‑50 (85.108 − 81.146), +3.16 pp over ResNet‑101, +2.29 pp over ResNet‑152.

**Throughput (images/sec):**
- ResNet‑50 is faster than ViT‑B/16: 4302.84 / 2992.79 = 1.44×
- ViT‑B/16 is faster than ResNet‑101: 2992.79 / 2781.19 = 1.08×
- ViT‑B/16 is faster than ResNet‑152: 2992.79 / 1976.86 = 1.51×

**Raw per‑image compute (GMACs):** ViT‑B/16 (17.58) is actually *larger* than every ResNet's GMACs — 4.3× ResNet‑50's 4.11, 2.2× ResNet‑101's 7.83, 1.5× ResNet‑152's 11.56.

## Does this confirm the paper's "2–4× less compute" claim?

**Not directly, and the GMAC comparison points the opposite way.** The paper's statement — "Vision Transformers dominate ResNets on the performance/compute trade-off. ViT uses approximately 2−4× less compute to attain the same performance (average over 5 datasets)" [ViT, p.7] — comes from a specific controlled scaling study: transfer performance vs. total **pre-training compute in exaFLOPs**, using models pre-trained on JFT-300M for 7–14 epochs (ResNets R50x1…R200x3, ViT-B/32…H/14, and hybrids), as reported in Figure 5 and Table 6 [ViT, p.7-8; p.15-16]. That metric is cumulative pre-training FLOPs, not single-forward-pass GMACs or inference throughput on already-trained checkpoints.

The timm query instead compares **inference-time GMACs/throughput** for checkpoints trained with heterogeneous recipes on ImageNet-1k/21k (e.g., `augreg2_in21k_ft_in1k`, `fb_swsl_ig1b_ft_in1k`), not the JFT-300M pre-training scaling experiment the paper's claim is based on. These are different measurements on different training setups, so this query cannot confirm or refute the pre-training-compute claim as stated in the paper.

What the data **does** show:
- ViT-B/16 reaches higher top-1 accuracy than any ResNet-50/101/152 variant listed.
- But its single-pass compute (17.58 GMACs) is higher, not lower, than all three ResNets' GMACs — the opposite direction of "needs less compute."
- Its measured throughput is faster than ResNet-101/152 but slower than ResNet-50.

So the evidence here does not establish that ViT-B/16 needs 2–4× less compute than ResNets for equal performance; if anything, on a per-image GMACs basis in this table, ViT-B/16 costs *more* compute than the ResNets it outperforms. The paper's actual 2–4× efficiency claim rests on the separate JFT-300M total-pre-training-compute scaling study [ViT, p.7, Figure 5; p.15-16, Table 6], which this timm/ImageNet inference-cost query does not reproduce.

**Retrieved:** ViT p.7-8 (0.80); ViT p.15-16 (0.79); ViT p.6-7 (0.77); ViT p.5 (0.76); ViT p.5-6 (0.75) | gold page hit: 1.00
**SQL:** `SELECT   mr.model,   mr.arch,   mr.img_size,   mr.top1_val,   bi.samples_per_sec,   bi.batch_size,   bi.gmacs,   bi.param_count_m FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.img_size = 224   AND (     mr.arch = 'vit_base_patch16_224'     OR mr.arch IN ('resnet50', 'resnet101', 'resnet152')   ) ORDER BY mr.arch, mr.top1_val DESC;` | overlap with reference result: 1.00
*51.8 s*

## Q39 (text+table, cross-source, medium, answerable: yes)

**Question.** The BYOL paper reports 74.3% for a linear classifier on frozen ResNet-50 features and cites supervised ResNet-50 baselines of 76.5% and 78.9%. How many timm ResNet-50 weights at 224 px exceed each of these three numbers, and what must be kept in mind when reading that comparison?

**Reference answer.** The paper's numbers are 74.3% (BYOL, linear evaluation on frozen features), 76.5% and 78.9% (supervised baselines). Among timm's 18 resnet50 rows at 224 px, all 18 are above 74.3%, 17 are at or above 76.5% (the exception is resnet50.tv_in1k at 76.156), and 13 are at or above 78.9% (the five below are ra_in1k 78.82, bt_in1k 78.444, a3_in1k 78.052, gluon_in1k 77.58 and tv_in1k 76.156). These are not like-for-like: BYOL's 74.3% is a linear probe on self-supervised features, whereas timm's are fully supervised weights with different recipes, some using extra data (e.g. ig1b, yfcc100m), so the comparison says nothing about whether self-supervised learning is better or worse.

**System answer.** ## Numbers from the database query

Out of 18 total ResNet-50 weights in timm trained/evaluated at 224 px:

- **> 74.3%** (BYOL's self-supervised linear-eval number): **18 of 18** exceed it
- **> 76.5%** (SimCLR paper's cited supervised baseline [8]): **17 of 18** exceed it
- **> 78.9%** (MaxUp supervised baseline [75]): **13 of 18** exceed it

## What must be kept in mind when reading this comparison

1. **The BYOL numbers are not from timm.** BYOL's 74.3% top-1 is a *linear evaluation* result — a linear classifier trained on **frozen** self-supervised features — not an end-to-end fine-tuned supervised model [BYOL, p.6]. Comparing it directly to timm's fully-trained/fine-tuned ResNet-50 weights conflates two different training regimes (self-supervised pretraining + frozen-linear-probe vs. standard supervised training).

2. **The 76.5% and 78.9% baselines are specific supervised training recipes, not a ceiling.** They come from particular papers: 76.5% is the vanilla supervised baseline reported in [8] (SimCLR paper), and 78.9% is from MaxUp [75], described in BYOL's own Appendix C as "the stronger supervised baseline... which uses advanced supervised learning techniques" [BYOL, p.19-20]. BYOL explicitly notes these are just two reference points among many possible supervised results, not an upper bound — consistent with 13/18 timm models already exceeding even the stronger 78.9% baseline.

3. **timm's higher numbers likely reflect training-recipe improvements, not an unfair comparison to BYOL per se.** Since the database only returns aggregate counts (no model names, training details, or augmentation/schedule info), the passages and query result do not establish *why* timm models exceed these baselines — e.g., whether via longer training, stronger augmentation (BYOL itself notes RandAugment improved its own reproduced supervised baseline to 76.4% vs. the original 76.5% cited [BYOL, p.19-20]), different learning-rate schedules, or test-time tricks. The evidence does not specify timm's exact training setups.

4. **Image resolution and evaluation protocol matter.** The query filters to `img_size = 224`, matching BYOL's standard ResNet-50 (1×) evaluation [BYOL, p.6], but other factors (test-time augmentation, EMA weights, distillation, etc., common in some timm checkpoints) are not visible in the passages provided and could inflate timm accuracy relative to BYOL's and the original supervised baselines' simpler protocols.

**In short:** the query result shows all 18 timm ResNet-50@224 weights beat BYOL's linear-eval number, nearly all beat the vanilla supervised baseline (76.5%), and the majority beat even the strong MaxUp baseline (78.9%) — but the evidence does not establish *why*, and the comparison mixes a frozen-feature linear-evaluation result (BYOL) against presumably fully fine-tuned supervised timm models, which is not an apples-to-apples comparison.

**Retrieved:** BYOL p.20-22 (0.81); BYOL p.6 (0.81); BYOL p.19-20 (0.81); BYOL p.6-7 (0.80); BYOL p.18-19 (0.77) | gold page hit: 1.00
**SQL:** `SELECT   SUM(CASE WHEN top1_val > 74.3 THEN 1 ELSE 0 END) AS gt_74_3,   SUM(CASE WHEN top1_val > 76.5 THEN 1 ELSE 0 END) AS gt_76_5,   SUM(CASE WHEN top1_val > 78.9 THEN 1 ELSE 0 END) AS gt_78_9,   COUNT(*) AS total_resnet50_224 FROM model_results WHERE arch = 'resnet50' AND img_size = 224;` | overlap with reference result: 1.00
*20.1 s*

## Q40 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper says its 152-layer network has lower complexity than VGG-16/19. Using timm's measurements at 224 px, how do parameters, GMACs, throughput and top-1 of resnet152 compare with vgg16 and vgg19, and does lower FLOPs mean faster in this benchmark?

**Reference answer.** The paper says the 152-layer ResNet (11.3 billion FLOPs) has lower complexity than VGG-16/19 (15.3/19.6 billion FLOPs). timm: resnet152 has 60.19M parameters, 11.56 GMACs, 1,976.86 samples/s and tv_in1k top-1 78.33; vgg16 has 138.36M, 15.47 GMACs, 2,235.61 samples/s, top-1 71.594; vgg19 has 143.67M, 19.63 GMACs, 2,044.71 samples/s, top-1 72.4. So resnet152 has 2.3-2.4x fewer parameters, 1.34-1.70x fewer GMACs and higher top-1 (with torchvision weights), but its measured throughput is about 12% lower than vgg16 and 3% lower than vgg19 on this GPU. Lower FLOPs therefore did not mean higher throughput here; the paper's claim concerns FLOPs, not measured speed.

**System answer.** ## Comparison at 224px (from timm benchmark query)

| Model | Params (M) | GMACs | Throughput (samples/sec) | Top‑1 (best variant) |
|---|---|---|---|---|
| resnet152 | 60.19 | 11.56 | 1976.86 | 82.818 (a1h_in1k) |
| vgg16 | 138.36 | 15.47 | 2235.61 | 71.594 |
| vgg19 | 143.67 | 19.63 | 2044.71 | 72.400 |

**Parameters & compute (FLOPs/MACs):** resnet152 has far fewer parameters than either VGG (60.19M vs. 138.36M for vgg16, a 2.30× reduction, and vs. 143.67M for vgg19, a 2.39× reduction) and fewer GMACs (11.56 vs. 15.47 for vgg16, a 1.34× reduction, and vs. 19.63 for vgg19, a 1.70× reduction). This is directly in line with the ResNet paper's own claim that "the 152-layer ResNet (11.3 billion FLOPs) still has lower complexity than VGG-16/19 nets (15.3/19.6 billion FLOPs)" [ResNet, p.6]. The timm GMACs (11.56, 15.47, 19.63) closely match the paper's billion-FLOP figures (11.3, 15.3, 19.6), confirming the same ordering.

**Top‑1 accuracy:** Every resnet152 checkpoint in the query beats both VGG models by a wide margin — even the weakest resnet152 variant (tv_in1k, 78.33%) exceeds vgg19 (72.4%) and vgg16 (71.594%) by roughly 6–7 points, and the best resnet152 variant (a1h_in1k, 82.818%) exceeds vgg19 by about 10.4 points.

**Throughput — does lower FLOPs mean faster?** No, not in this benchmark. Despite having fewer GMACs and far fewer parameters, resnet152's throughput (1976.86 samples/sec) is *lower* than both vgg16 (2235.61 samples/sec, ~1.13× faster than resnet152) and vgg19 (2044.71 samples/sec, ~1.03× faster than resnet152).

Calculation check:
- vgg16/resnet152 throughput ratio = 2235.61 / 1976.86 ≈ 1.131 (vgg16 is ~13% faster)
- vgg19/resnet152 throughput ratio = 2044.71 / 1976.86 ≈ 1.034 (vgg19 is ~3% faster)
- while vgg16/resnet152 GMACs ratio = 15.47 / 11.56 ≈ 1.338 (vgg16 does 34% more MACs)
- and vgg19/resnet152 GMACs ratio = 19.63 / 11.56 ≈ 1.699 (vgg19 does 70% more MACs)

So resnet152 does substantially less computation (in MACs/FLOPs) than either VGG model, exactly as the ResNet paper states [ResNet, p.6], but it still runs slower in this timm inference benchmark. This shows that nominal compute (FLOPs/MACs) and measured hardware throughput can diverge — likely due to architectural factors (depth/sequential layers, memory-access patterns, parallelizability) not captured by FLOP counts alone. The provided evidence does not explain the specific cause of this discrepancy beyond showing it occurs; it only establishes the FLOPs/params/throughput/accuracy numbers themselves.

**Retrieved:** ResNet p.5-6 (0.74); ResNet p.6-7 (0.71); ResNet p.6 (0.71); ResNet p.5 (0.71); ViT p.15-16 (0.70) | gold page hit: 0.50
**SQL:** `SELECT mr.arch,        mr.model,        mr.img_size,        mr.param_count_m,        bi.gmacs,        bi.samples_per_sec,        bi.batch_size,        mr.top1_val FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.arch IN ('resnet152', 'vgg16', 'vgg19')   AND mr.img_size = 224 ORDER BY mr.arch;` | overlap with reference result: 1.00
*27.4 s*

## Q42 (text-only, conceptual, medium, answerable: yes)

**Question.** Does the MMLU paper attribute its models' accuracy mainly to parameter count? Use its GPT-3, UnifiedQA and smaller fine-tuned model comparisons.

**Reference answer.** Not mainly: size matters but is not sufficient. In few-shot GPT-3 (Table 1) the three smaller models are near random (Small 25.9%, Medium 24.9%, Large 26.0% against 25.0% for random) while the 175B X-Large model reaches 43.9% (about 37.7% zero-shot). But UnifiedQA, fine-tuned on other QA datasets and tested without further tuning, reaches 48.9% with 11B parameters, better than GPT-3 X-Large despite an order of magnitude fewer parameters, and its smallest 60M variant gets about 29.3%. In Appendix A.1 RoBERTa-base (125M) gets 27.9%, ALBERT-xxlarge (223M) 27.1% and GPT-2 (1.5B) 32.4%; UnifiedQA-60M beats RoBERTa and ALBERT with fewer parameters and UnifiedQA-3B (43.7%) beats GPT-2, which the authors say suggests T5's larger pretraining dataset helps. They conclude that model size is a key component but fine-tuning also helps; the data-size explanation is a suggestion, and the models differ in architecture, fine-tuning data and evaluation regime (GPT-3 few-shot, UnifiedQA tested under distribution shift), so it is not a controlled test.

**System answer.** **No — the paper explicitly rejects a "parameter-count-is-everything" explanation and instead attributes accuracy to a combination of scale, fine-tuning, and pretraining-data size.**

**1. Within GPT-3 alone, size does correlate with accuracy:**
"the three smaller GPT-3 models have near random accuracy (around 25%)... the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%" [MMLU, p.6-7]. This part is consistent with "bigger = better."

**2. But UnifiedQA breaks the pure parameter-count story:**
UnifiedQA (11B params) reaches 48.9%, beating few-shot GPT-3 (175B params) at 43.9%, "despite UnifiedQA have[ing] an order of magnitude fewer parameters" [MMLU, p.6-7].
- Calculation: 175B / 11B ≈ 16× more parameters for GPT-3, yet GPT-3's accuracy (43.9%) is *lower* than UnifiedQA's (48.9%).
The paper's own conclusion: "These results suggest that while model size is a key component for achieving strong performance, **fine-tuning also helps**" [MMLU, p.6-7] — i.e., size is not the sole driver.

**3. Smaller fine-tuned models reinforce this — pretraining data size matters more than raw parameters:**
- UnifiedQA's smallest variant (60M params) attains ~29.3% accuracy, which is *higher* than RoBERTa-base (125M params, 27.9%) and ALBERT-xxlarge (223M params, 27.1%) [MMLU, p.11-12] — despite having fewer parameters than both.
- Calculation: 60M params gives 29.3%, while 223M params (ALBERT, ~3.7× more parameters) gives only 27.1% — a larger model performing *worse*.
- The paper states: "It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters. This suggests that its larger pretraining dataset enables higher accuracy" [MMLU, p.11-12].
- Similarly, "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy. This again suggests that T5's larger pretraining dataset size... can increase accuracy" [MMLU, p.11-12] — here two models of comparable size produce an 11.3 percentage-point gap, attributed to pretraining data, not parameters.

**Conclusion:** The evidence shows the MMLU paper treats parameter count as only one contributing factor (useful within a single model family like GPT-3), but it explicitly uses the GPT-3/UnifiedQA comparison and the small-model comparisons (UnifiedQA-60M vs. RoBERTa/ALBERT; UnifiedQA-3B vs. GPT-2-1.5B) to argue that fine-tuning and pretraining dataset size can outweigh raw parameter count. So the paper does **not** attribute accuracy mainly to parameter count.

**Retrieved:** MMLU p.6-7 (0.80); MMLU p.11-12 (0.78); MMLU p.7-8 (0.78); MMLU p.2-3 (0.77); MMLU p.12-14 (0.76) | gold page hit: 0.67
*19.8 s*

## Q43 (text-only, cross-paper, hard, answerable: yes)

**Question.** MMLU, SWE-bench and FIRE-Bench each have to worry that a model may have seen benchmark content during training. What check does each paper run, what does it find, and how strongly does each paper state its conclusion?

**Reference answer.** MMLU (Appendix B.2): memorized questions would have low entropy and high accuracy, but accuracy and question entropy are not positively correlated (correlation between average log probability and accuracy r = -0.43 zero-shot, -0.56 few-shot), which 'suggests that our exact questions were not memorized'. The authors add that models still met text related to the questions through Wikipedia, and promise a list of question sources. SWE-bench (Section 5): resolve rates for PRs created before versus after 2023 in the oracle setting show little difference for most models (Claude 2 4.87% vs 4.23%, ChatGPT-3.5 0.49% vs 0.77%, SWE-Llama 13b 3.98% vs 3.85%), GPT-4 being the exception (1.96% vs 0.0%, on a 25% subset); the authors call this 'largely promising' since models are 'unlikely to cheat' by generating a more recent repository version, and note that new instances can be collected after a model's training date. FIRE-Bench (Section 5.4): F1 on tasks published before versus after each model's knowledge cutoff, stratified by difficulty (Table 6), shows no consistent advantage for pre-cutoff tasks; the authors call the analysis coarse (approximate cutoff dates, unknown training data, small per-category samples) and say it 'suggests the absence of a strong contamination signal rather than proving its absence'. The three checks measure different things (exact-question memorization versus date-based exposure) and none can rule contamination out, so their results are not comparable and no benchmark should be called cleaner on this evidence.

**System answer.** Based on the passages provided, only **FIRE-Bench** includes material addressing training-data contamination; no passage here from **MMLU** or **SWE-bench** discusses such a check, so I cannot report their methods or findings from this evidence.

## FIRE-Bench

**Check run:** The paper reports that it "examine[s] potential data contamination effects by disentangling performance across task difficulty levels and model knowledge cutoff dates" [FIRE-Bench, p.2]. This is reiterated in the conclusion as well, where the same disentanglement (difficulty levels vs. model knowledge cutoff dates) is described as the method used to probe contamination [FIRE-Bench, p.9-10].

**Finding:** The paper states it "find[s] no strong evidence of systematic contamination" [FIRE-Bench, p.2].

**Strength of claim:** The language is hedged rather than definitive — "no strong evidence of systematic contamination" [FIRE-Bench, p.2] — which is a negative/absence-of-evidence claim, not a positive proof that no contamination occurred. The passages do not report the actual quantitative breakdown (e.g., specific performance numbers by cutoff date or difficulty tier) that underlies this claim, so the evidentiary strength of the check itself cannot be assessed from what's given here.

## SWE-bench

The provided passages [SWE-bench, p.11-12 (Ethics/Reproducibility Statement) and p.25-26 (Appendix A.6–C.2, training details and repository breakdowns)] do not mention any check for training-data contamination or benchmark leakage. **The evidence does not establish what check, if any, SWE-bench's paper runs for this concern.**

## MMLU

No passages from an MMLU paper were included in the provided material. **The evidence does not establish what check, finding, or stated conclusion MMLU's paper offers regarding training-data contamination** — nothing can be reported here.

---

**Summary:** Of the three benchmarks, only FIRE-Bench's contamination check is evidenced in the passages supplied: it disentangles performance by difficulty and by model knowledge-cutoff date, and concludes — in hedged terms — that it finds "no strong evidence of systematic contamination" [FIRE-Bench, p.2, p.9-10]. No corresponding checks for MMLU or SWE-bench appear in the passages provided, so their methods, findings, and conclusion strength cannot be reported from this evidence alone.

**Retrieved:** FIRE-Bench p.2 (0.75); FIRE-Bench p.9-10 (0.75); FIRE-Bench p.19-20 (0.75); SWE-bench p.11-12 (0.74); SWE-bench p.25-26 (0.73) | gold page hit: 0.17
*14.7 s*
