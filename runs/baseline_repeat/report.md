# Report: runs/baseline_repeat

35 questions, 0 errors, mean latency 20.6 s.

| Source type | Retrieval page hit | SQL value overlap | Answers with abstention wording |
|---|---|---|---|
| text-only | 0.59 (n=21) | - | 13 of 21 |
| table-only | - | 0.61 (n=7) | 0 of 7 |
| text+table | 0.62 (n=7) | 0.75 (n=7) | 4 of 7 |

Insufficient-evidence questions (Q18, Q20): 2 of 2 answers use abstention wording (keyword heuristic, check by reading).

Diagnostics are heuristics, not grades. *Retrieval page hit*: share of the workbook's gold evidence pages covered by retrieved chunks. *SQL value overlap*: share of cells of the workbook's reference SQL result that also appear in the system's result. Grade answers by reading them against the reference.

## Q01 (text-only, factual, medium, answerable: yes)

**Question.** In the ResNet paper's ImageNet comparison of 18-layer and 34-layer networks, how did the plain and residual versions differ, and why do the authors argue the plain network's problem is not caused by vanishing gradients?

**Reference answer.** The 34-layer plain net had higher error than the 18-layer plain net (top-1 validation error 28.54% vs 27.94%, Table 2) and higher training error throughout training; the authors call this the degradation problem. With identity shortcuts (zero-padded, so no extra parameters) the order reversed: the 34-layer ResNet reached 25.03% vs 27.88% for the 18-layer ResNet (2.8 points better). The authors argue the plain-net difficulty is unlikely to be vanishing gradients because the plain nets are trained with batch normalization, which keeps forward signals at non-zero variance, and they verified that backward gradients have healthy norms; they only conjecture that deep plain nets may have exponentially low convergence rates. Training 3x longer still showed degradation.

**System answer.** ## Difference between plain and residual 18/34-layer networks

The plain and residual networks were built to have **identical architecture, depth, width, and parameter count** — the only difference is the addition of shortcut connections:

- "The baseline architectures are the same as the above plain nets, except that a shortcut connection is added to each pair of 3×3 filters as in Fig. 3 (right)." [ResNet, p.5]
- For the first comparison, identity mapping was used for all shortcuts and zero-padding for increasing dimensions (option A), "So they have no extra parameter compared to the plain counterparts." [ResNet, p.5]

**Performance difference (Table 2, top-1 error, 10-crop testing):**
| | plain | ResNet |
|---|---|---|
| 18 layers | 27.94 | 27.88 |
| 34 layers | 28.54 | 25.03 |

[ResNet, p.5]

Key observations:
- The 34-layer **plain** net has *higher* training error than the 18-layer plain net throughout training, despite the 18-layer solution space being a subspace of the 34-layer one — i.e., deeper plain net degrades. [ResNet, p.5]
- With residual connections, "the situation is reversed... the 34-layer ResNet is better than the 18-layer ResNet (by 2.8%)," and it "exhibits considerably lower training error and is generalizable to the validation data." [ResNet, p.5-6]
- Comparing the 34-layer plain net to its ResNet counterpart: the ResNet "reduces the top-1 error by 3.5%," resulting from "successfully reduced training error." [ResNet, p.6]
- For 18 layers, plain and residual nets are "comparably accurate," but the 18-layer ResNet "converges faster," easing optimization "by providing faster convergence at the early stage" when the net is "not overly deep." [ResNet, p.6]

## Why the authors argue it's not vanishing gradients

The authors give three pieces of evidence [ResNet, p.5]:

1. **BN ensures healthy signal propagation**: "These plain networks are trained with BN [16], which ensures forward propagated signals to have non-zero variances. We also verify that the backward propagated gradients exhibit healthy norms with BN. So neither forward nor backward signals vanish."

2. **The 34-layer plain net still achieves competitive accuracy** (Table 3), "suggesting that the solver works to some extent" — i.e., it's not completely failing to learn, which would be expected if gradients had vanished.

3. **More training iterations don't fix it**: In a footnote, "We have experimented with more training iterations (3×) and still observed the degradation problem, suggesting that this problem cannot be feasibly addressed by simply using more iterations." [ResNet, p.5]

Instead, they **conjecture** that "the deep plain nets may have exponentially low convergence rates, which impact the reducing of the training error," explicitly noting "The reason for such optimization difficulties will be studied in the future." [ResNet, p.5]

**Retrieved:** ResNet p.5 (0.84); ResNet p.5-6 (0.83); ResNet p.7-8 (0.81); ResNet p.6 (0.81); ResNet p.3-4 (0.80) | gold page hit: 1.00
*17.7 s*

## Q02 (text-only, factual, medium, answerable: yes)

**Question.** In BabyCL's main results (Table 1), how do the Labeled-S 4AFC accuracies of BabyCL (k = 4 and k = 8) compare with the offline CVCL upper bound and with the one-pass and compute-matched streaming baselines, and what do the authors conclude from the compute-matched baseline?

**Reference answer.** Table 1 (4AFC, Labeled-S, mean +/- CI): offline CVCL (i.i.d., 400 epochs, upper bound) 57.31 +/- 1.13; one-pass CVCL (naive streaming) 27.52 +/- 3.12; CL-CVCL (compute-matched) 36.41 +/- 2.31; BabyCL with k=4 41.08 +/- 1.79 and with k=8 43.38 +/- 1.47. Both BabyCL settings beat both streaming baselines (k=8 is 15.86 points above one-pass CVCL and 6.97 above CL-CVCL), k=8 is 2.30 above k=4, and both remain below the offline upper bound (k=8 by 13.93 points). The authors conclude that BabyCL substantially closes but does not match the gap to offline training, and because CL-CVCL is matched in optimization work to BabyCL's gradient budget (at k=8), BabyCL's advantage 'cannot be explained by gradient count alone'.

**System answer.** ## Labeled‑S 4AFC results in Table 1

Based on the numbers reported for Table 1 [BabyCL, p.5‑6] and the accompanying discussion [BabyCL, p.6‑7]:

| Model | Accuracy reported in text (“Best”) | Final mean ± CI (Table 1) |
|---|---|---|
| Offline CVCL (upper bound, i.i.d., 400 epochs) | **57.45 %** | — |
| One‑pass CVCL (naïve streaming, no replay) | **25.68 %** | 27.52 ± 3.12 % |
| CL‑CVCL (compute‑matched: same gradient budget as BabyCL k=8, ~6× revisitation per item, but no continual‑learning structure) | **35.32 %** | 36.41 ± 2.31 % |
| BabyCL, k = 4 | — | 41.08 ± 1.79 % |
| BabyCL, k = 8 | **44.46 %** | 43.38 ± 1.47 % |

**Comparisons**

- **Vs. offline CVCL:** BabyCL (k=8, 44.46 %) "substantially closes the gap to offline CVCL (57.45 %) but does not match it" — a remaining gap of 57.45 − 44.46 = **13.0 percentage points** [BabyCL, p.6‑7].
- **Vs. one‑pass CVCL:** One‑pass CVCL "collapses to 25.68 %," far below both BabyCL settings, "confirming that a training recipe designed for i.i.d. data does not transfer to streaming" [BabyCL, p.6‑7].
- **Vs. CL‑CVCL (compute‑matched):** CL‑CVCL reaches "only 35.32 %, well below BabyCL at 44.46 % (k = 8)" — a gap of 44.46 − 35.32 = **9.14 percentage points**, even though CL‑CVCL is given the *same* optimization budget as BabyCL [BabyCL, p.6‑7].
- **k=4 vs. k=8:** "Additional insertion‑time resampling (from k = 4 to k = 8) yields a further 2.6‑point gain, indicating that the continual‑structure benefits compound with more thorough revisitation of newly inserted content" [BabyCL, p.6‑7].

**Authors' conclusion about the compute‑matched baseline**

Because CL‑CVCL is matched to BabyCL's optimization work (same number of gradient updates/revisitations) yet still performs far worse, the authors conclude: "the gap cannot be explained by gradient count alone; it reflects the benefit of organizing the stream through event segmentation and of combining visual self‑supervision with cross‑modal grounding" [BabyCL, p.6‑7]. In other words, BabyCL's advantage over streaming baselines is attributed to its continual‑learning machinery (segmentation + dual replay + joint visual/cross‑modal objectives), not simply to doing more optimization steps on the same data.

The passages do not report a separate "Best" (peak) value or a Table‑1 final‑mean value for offline CVCL, so no further comparison on that specific metric can be made from the given evidence.

**Retrieved:** BabyCL p.5-6 (0.82); BabyCL p.6-7 (0.81); BabyCL p.14-15 (0.76); BabyCL p.7-8 (0.76); BabyCL p.10-12 (0.76) | gold page hit: 1.00
*32.3 s*

## Q03 (text-only, factual, medium, answerable: yes)

**Question.** How does I-JEPA sample its target and context blocks (number of target blocks, scale and aspect-ratio ranges), and where in the pipeline are the target blocks 'masked'?

**Reference answer.** I-JEPA typically samples M = 4 target blocks, each with random aspect ratio in (0.75, 1.5) and random scale in (0.15, 0.2). The context is a single block with scale in (0.85, 1.0) and unit aspect ratio, from which any region overlapping the targets is removed so the prediction task is non-trivial. The target blocks are obtained by masking the output of the target encoder, not its input, which the paper calls crucial for high-semantic-level targets. The loss is the average L2 distance between predicted and target patch-level representations, and the target encoder is an exponential moving average of the context encoder.

**System answer.** ## Target blocks

I-JEPA samples **M = 4** target blocks (typically) from the target representations, with:
- **Scale**: random range **(0.15, 0.2)**
- **Aspect ratio**: random range **(0.75, 1.5)**

These blocks are sampled independently and may possibly overlap with each other [I-JEPA, p.3-4].

## Context block

A **single** context block x is sampled with:
- **Scale**: random range **(0.85, 1.0)**
- **Aspect ratio**: **unit** (i.e., fixed at 1.0)

Since target blocks are sampled independently of the context block, there may be significant overlap; to ensure a non-trivial prediction task, **any overlapping regions between the context block and the target blocks are removed from the context block** [I-JEPA, p.3-4].

## Where target blocks are "masked"

Crucially, the target blocks are obtained by **masking the output of the target-encoder, not the input**:
> "Note that the target blocks are obtained by masking the output of the target-encoder, not the input. This distinction is crucial to ensure target representations of a high semantic level" [I-JEPA, p.3-4].

That is, the full (unmasked) image y is first passed through the target-encoder $f_{\bar\theta}$ to obtain patch-level representations $s^y = \{s^y_1,\dots,s^y_N\}$ for all N patches; then M blocks are sampled from these output representations to serve as targets $s^{y(i)} = \{s^y_j\}_{j\in B_i}$ [I-JEPA, p.3-4].

This design choice is explicitly ablated: when masking is instead applied to the **input** (requiring a separate forward pass through the target-encoder for each target region), linear-probe top-1 accuracy on 1% ImageNet-1K drops from **67.3%** (masking output) to **56.1%** (masking input) for a ViT-H/16 pretrained for 300 epochs [I-JEPA, p.14-15, Table 11]. The paper concludes that "masking the output of the target-encoder during pretraining results in more semantic prediction targets and improves linear probing performance" [I-JEPA, p.14-15].

**Retrieved:** I-JEPA p.13-14 (0.83); I-JEPA p.3-4 (0.83); I-JEPA p.14-15 (0.80); I-JEPA p.7-8 (0.80); I-JEPA p.8-9 (0.78) | gold page hit: 1.00
*10.6 s*

## Q04 (text-only, factual, easy, answerable: yes)

**Question.** How are Daily Oracle's question-answer pairs generated and filtered, and how many True/False and multiple-choice questions are in the subset analysed in the paper?

**Reference answer.** The analysed subset has 16,783 True/False and 14,727 multiple-choice questions generated from daily news articles from January 2020 to December 2024. Each day six articles are selected (three random, three from hot topics) and an LLM generates two TF and two MC pairs per article with few-shot prompting. Construction has four steps: article summary (focused on new events so the publication date can be the resolution date), QA generation, misleading-choice generation for MC, and QA filtering. In filtering, an LLM scores seven principles from 0 to 2 points each and only questions with at least 13 points are kept.

**System answer.** ## Daily Oracle: QA Pair Generation and Filtering Process

The dataset construction follows a four-step LLM-based pipeline [DailyOracle, p.4]:

1. **Question Generation (TF)**: The LLM generates True/False question pairs — "generate the first question with a 'Yes' answer and the second with a 'No'" [DailyOracle, p.4].

2. **Misleading Choices Generation (MC)**: For multiple-choice questions, the LLM is given "the article, its publishing date, and the QA pair," and it "generates three misleading choices" [DailyOracle, p.4].

3. **QA Filtering**: The LLM checks each question against seven principles:
   - Correctness of answers
   - Non-answerability before the publication date
   - Absence of information leakage
   - Objectivity
   - Inclusion of a clear temporal element
   - Public interest
   - Non-obviousness of the answer

   "Each principle is scored with 0, 1, or 2 points, and we selected the questions that received at least 13 points in total" [DailyOracle, p.4] (out of a maximum of 14 points across seven principles).

**Models used**: GPT-3.5 or GPT-4o-mini handle steps (1) and (4), while GPT-4 or GPT-4o handle steps (2) and (3) "to ensure high data quality" [DailyOracle, p.4]. Specifically, "GPT-3.5 and GPT-4 [were used] until September 2024. After October 2024, we switch to GPT-4o-mini and GPT-4o, as they are both more cost-effective and more powerful" [DailyOracle, p.4-5].

## Dataset Size

The subset used for analysis in the paper consists of:
- **16,783 TF (True/False) QA pairs**
- **14,727 MC (Multiple Choice) QA pairs**

"covering the period from January 1st, 2020, to December 31st, 2024, with an average of 17.2 questions per day" [DailyOracle, p.4].

This same figure is corroborated elsewhere in the paper: "we utilize a subset of the data consisting of 16,783 TF questions and 14,727 MC questions... generated using daily news articles from January 2020 up until December 2024" [DailyOracle, p.3].

**Retrieved:** DailyOracle p.4 (0.77); DailyOracle p.3 (0.77); DailyOracle p.4-5 (0.77); DailyOracle p.17-19 (0.74); DailyOracle p.34-35 (0.74) | gold page hit: 1.00
*10.8 s*

## Q06 (text-only, conceptual, medium, answerable: yes)

**Question.** What three desiderata do the Transformer authors use to motivate self-attention over recurrent and convolutional layers, how does a self-attention layer compare on each, and when is it cheaper per layer than a recurrent layer?

**Reference answer.** The desiderata are (1) total computational complexity per layer, (2) the amount of computation that can be parallelised (minimum number of sequential operations) and (3) the path length between long-range dependencies. Per Table 1, self-attention has O(n^2*d) complexity per layer, O(1) sequential operations and O(1) maximum path length; recurrent layers have O(n*d^2), O(n) and O(n); convolutional layers have O(k*n*d^2), O(1) and O(log_k n). Self-attention is faster than a recurrent layer when the sequence length n is smaller than the representation dimensionality d, which is typical for sentence representations in machine translation. For very long sequences the authors suggest restricting attention to a neighbourhood of size r (path length O(n/r)) but leave this to future work.

**System answer.** Based on the passages provided, I can only partially answer this question — the excerpt from [Transformer, p.7-8, section: 4 Why Self-Attention] appears to begin mid-sentence (it opens with "...lutional layers in the case of contiguous kernels..."), meaning the part of Section 4 where the three desiderata are explicitly introduced and compared is **not included** in the evidence given to me. I cannot state what the "three desiderata" are from this evidence alone, nor can I confirm the specific condition under which self-attention is cheaper per layer than a recurrent layer, since recurrent-layer complexity is never mentioned in the visible text.

What the evidence **does** establish:

**1. Path length between long-range dependencies (partially shown):**
The visible text discusses path length only in comparison to convolutions, not self-attention directly: contiguous-kernel convolutional layers require stacking $O(n/k)$ layers to connect all position pairs, or $O(\log_k(n))$ layers for dilated convolutions, "increasing the length of the longest paths between any two positions in the network" [Transformer, p.7-8]. The paper states this increase in path length makes it harder to learn long-range dependencies (the general point noted in the appendix text), but the explicit self-attention-vs-recurrent-vs-convolution path-length comparison is not in the excerpt.

**2. Computational cost per layer (only convolution vs. self-attention is given):**
"Convolutional layers are generally more expensive than recurrent layers, by a factor of k. Separable convolutions [6], however, decrease the complexity considerably, to $O(k \cdot n \cdot d + n \cdot d^2)$. Even with $k = n$, however, the complexity of a separable convolution is equal to the combination of a self-attention layer and a point-wise feed-forward layer, the approach we take in our model." [Transformer, p.7-8]
This shows self-attention+feed-forward matches the *best-case* (k=n) separable-convolution cost, but no recurrent-layer complexity figure is given in the evidence, so I cannot calculate or confirm when self-attention is cheaper per layer than a recurrent layer.

**3. Interpretability (a side point, not one of the core three):**
"As [a] side benefit, self-attention could yield more interpretable models. We inspect attention distributions from our models... Not only do individual attention heads clearly learn to perform different tasks, many appear to exhibit behavior related to the syntactic and semantic structure of the sentences." [Transformer, p.7-8]
This is explicitly called a "side benefit," not one of the primary motivating desiderata.

**What the evidence does not establish:**
- The explicit list/naming of the "three desiderata" (which, based on the visible fragment, likely include per-layer computational complexity, amount of parallelizable computation/sequential operations, and maximum path length — but this is not stated verbatim in the given passages).
- Any direct numerical comparison between self-attention and recurrent-layer complexity (e.g., no $O(n^2 \cdot d)$ vs. $O(n \cdot d^2)$ figures appear in the text I have).
- Therefore, I cannot confirm from this evidence the specific condition (e.g., sequence length vs. representation dimension) under which self-attention is cheaper per layer than a recurrent layer.

If you'd like, I can answer more completely if you provide the earlier part of Section 4 (likely on p.6-7) that introduces Table 1 and the recurrent-layer comparison explicitly.

**Retrieved:** Transformer p.7-8 (0.76); Transformer p.2-3 (0.75); Transformer p.10 (0.74); ViT p.2 (0.73); ViT p.1 (0.73) | gold page hit: 0.50
*23.6 s*

## Q07 (text-only, conceptual, hard, answerable: yes)

**Question.** BYOL trains without negative pairs. What mechanisms does the paper credit with preventing representation collapse, and what do its ablations show about them?

**Reference answer.** BYOL trains an online network (encoder, projector, predictor) to predict the projection of a second augmented view produced by a target network whose weights are an exponential moving average of the online weights; the loss gradient is not propagated into the target (stop-gradient) and the predictor exists only on the online branch. The authors hypothesise that the combination of the predictor and the slow-moving-average target avoids collapse, but they state the dynamics still admit undesirable equilibria that they did not observe in experiments. In the ablation (Table 5b), the only variant that performs well without negatives is BYOL with both a target network and a predictor; the representation collapses when either is removed. They also found that the target network can be removed without collapse if the predictor is kept near-optimal (e.g., higher predictor learning rate), suggesting that keeping the predictor near-optimal may be one role of the target network.

**System answer.** ## Mechanisms credited with preventing collapse

The paper credits **two architectural components working together**: the **target network** (slow-moving average of the online network) and the **predictor** on top of the online network.

**Target network:** BYOL does not use an explicit anti-collapse term such as negative examples [BYOL, p.4]. Instead, the target parameters ξ are updated as an exponential moving average of the online parameters θ: `ξ ← τξ + (1−τ)θ` [BYOL, p.4]. Critically, this update is *not* in the direction of ∇ξL, so BYOL's dynamics are not a joint gradient descent on a single loss over (θ, ξ) — analogous to GANs, where no single loss is jointly minimized by both players [BYOL, p.4]. This asymmetry is why there is "no a priori reason" BYOL's parameters would converge to a collapsed minimum of the loss [BYOL, p.4].

**Predictor:** On top of this, assuming the predictor is near-optimal (q* = E[z'_ξ | z_θ]), BYOL's updates on θ follow in expectation the gradient of the expected conditional variance of the target given the online projection, which the authors argue favors reducing variance induced by stochastic augmentation rather than collapsing to a constant representation [BYOL, p.4-5]. The paper states the hypothesis that "keeping the predictor near-optimal at all times is important to preventing collapse, which may be one of the roles of BYOL's target network" [BYOL, p.10-11].

## What the ablations show

From the ablation study [BYOL, p.9-10]:

1. **Removing either component causes collapse:** "Table 5b already shows the importance of combining a predictor and a target network: the representation does collapse when either is removed" [BYOL, p.9-10].

2. **Predictor is critical even without the target network's usual role (Mean Teacher comparison):** Removing the predictor from BYOL yields an unsupervised Mean-Teacher-like variant (consistency loss between student and temporally-averaged teacher, using augmentations instead of dropout noise) — "This variant of BYOL collapses (Row 7 of Table 5) which suggests that the additional predictor is critical to prevent collapse in an unsupervised scenario" [BYOL, p.9-10].

3. **Target network can be removed if the predictor is made near-optimal instead:** The authors found collapse can be avoided *without* a target network by making the predictor near-optimal via:
   - (i) using an optimal linear predictor (closed-form linear regression on the current batch) before back-propagating the error — **52.5% top-1 accuracy**;
   - (ii) increasing the predictor's learning rate — **66.5% top-1 accuracy** [BYOL, p.9-10].

4. **But simply speeding up all learning doesn't substitute for near-optimality:** "increasing the learning rates of both projector and predictor (without target network) yields poor results (≈25% top-1)" [BYOL, p.9-10] — i.e., merely training faster isn't sufficient; it's specifically keeping the predictor near the Bayes-optimal regression target that matters.

5. **Target network also stabilizes contrastive methods (SimCLR), independent of collapse:** "Simply adding a target network to SimCLR already improves performance (+1.6 points)," even using the same number of negatives, suggesting the target network has a general "mere stabilization effect" on the bootstrap mechanism beyond collapse prevention in BYOL specifically [BYOL, p.9-10].

**Summary interpretation:** The evidence supports that collapse avoidance in BYOL is attributed jointly to (a) the asymmetric target-network dynamics that break the joint-minimization structure that would otherwise permit trivial collapsed solutions, and (b) the predictor being kept near the conditional-expectation optimum. The ablations (Table 5, Row 7, and the predictor-learning-rate/linear-regression experiments) empirically confirm both are needed in general, but either can substitute for the other in a specific sense: a near-optimal predictor alone (via higher learning rate or closed-form regression) prevents collapse even without a target network, supporting the paper's hypothesis that near-optimal prediction is the deeper mechanism, with the target network being one way to help achieve it [BYOL, p.9-11].

**Retrieved:** BYOL p.4-5 (0.74); BYOL p.10-11 (0.73); BYOL p.2 (0.73); BYOL p.9-10 (0.73); BYOL p.2-3 (0.72) | gold page hit: 1.00
*18.1 s*

## Q08 (text-only, conceptual, medium, answerable: yes)

**Question.** What evidence does the Batch Normalization paper give that batch normalization reduces internal covariate shift, how large is the training speed-up it reports on ImageNet (and what else was changed besides adding BN), and what does the paper itself say it has not established?

**Reference answer.** The paper defines internal covariate shift as the change in the distribution of network activations due to the change in network parameters during training. Its direct evidence is a small MNIST experiment (three sigmoid hidden layers): the input distribution to a typical sigmoid unit is much more stable with BN and the BN network has higher test accuracy (Fig. 1). On ImageNet the evidence is indirect, through the speed and accuracy of BN-Inception variants: BN-Baseline matches Inception's 72.2% in 13.3M steps versus 31.0M, BN-x5 needs 2.1M steps (stated as 14 times fewer), BN-x30 reaches 74.8%, and BN-x5-Sigmoid reaches 69.8% while Inception with sigmoid never beats 1/1000 accuracy. The BN-x5/x30 speed-ups combine BN with other changes (a 5x or 30x larger initial learning rate, Dropout removed, L2 weight cut 5x, learning rate decayed 6x faster, Local Response Normalization removed, more thorough shuffling, fewer photometric distortions), so they are not an isolated measure of BN. The paper frames the mechanism as an expectation and conjecture: it 'expects' fixed input distributions to speed training, 'conjectures' that BN may bring layer Jacobian singular values close to 1, and says the precise effect of BN on gradient propagation remains an area of further study.

**System answer.** ## Evidence that BN reduces internal covariate shift

The paper's primary evidence is an MNIST experiment [BatchNorm, p.6, section 4.1]. Using a simple network (28x28 input, 3 fully-connected hidden layers of 100 sigmoid activations each, trained 50,000 steps with mini-batch size 60), the authors compared a baseline network to one with Batch Normalization added to each hidden layer.

- They tracked the distribution of inputs to a typical sigmoid unit in the last hidden layer over training, visualized as the {15, 50, 85}th percentiles [BatchNorm, p.5-6, section 3.3].
- Finding: "The distributions in the original network change significantly over time, both in their mean and the variance, which complicates the training of the subsequent layers. In contrast, the distributions in the batch-normalized network are much more stable as training progresses, which aids the training." [BatchNorm, p.6, section 4.1]
- This stability is used as evidence that BN reduces internal covariate shift (defined as "the change in the distribution of network activations due to the change in network parameters during training" [BatchNorm, p.2]), accompanied by the network also achieving higher test accuracy on held-out data [BatchNorm, p.5-6, section 3.3].

## Training speed-up on ImageNet, and what else changed

The paper reports two related speed-up figures:
- In the abstract: "Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps" [BatchNorm, p.1].
- In the introduction: "we apply Batch Normalization to the best-performing ImageNet classification network, and show that we can match its performance using only 7% of the training steps" [BatchNorm, p.2] — equivalent to roughly 1/0.07 ≈ 14.3× fewer steps, consistent with the "14 times" figure.

Besides simply adding BN, the paper states that merely adding BN is not enough to realize the full speedup; they changed the network/training setup further [BatchNorm, p.8, section 4.2.1]:
- **Increased the learning rate** ("we have been able to achieve a training speedup from higher learning rates, with no ill side effects") [BatchNorm, p.8].
- **Removed Dropout** ("Removing Dropout from Modified BN-Inception speeds up training, without increasing overfitting") [BatchNorm, p.8].
- **Reduced the L2 weight regularization** (listed as another change, described as controlling overfitting in the original Inception) [BatchNorm, p.8].

The conclusion reiterates this: "By further increasing the learning rates, removing Dropout, and applying other modifications afforded by Batch Normalization, we reach the previous state of the art with only a small fraction of training steps – and then beat the state of the art in single-network image classification." [BatchNorm, p.8, section 4.2.1]

## What the paper itself says it has not established

- On the mechanism linking BN to gradient propagation, the paper is explicit about the limits of its own analysis: "In reality, the transformation is not linear, and the normalized values are not guaranteed to be Gaussian nor independent, but we nevertheless expect Batch Normalization to help make gradient propagation better behaved. The precise effect of Batch Normalization on gradient propagation remains an area of further study." [BatchNorm, p.5-6, section 3.3]
- More broadly, in the conclusion: "In this work, we have not explored the full range of possibilities that Batch Normalization potentially enables." They explicitly list unexplored future work: applying BN to Recurrent Neural Networks (to "more thoroughly test the hypothesis that normalization improves gradient propagation"), investigating whether BN helps with domain adaptation, and noting that "further theoretical analysis of the algorithm would allow still more improvements and applications" [BatchNorm, p.8, section 4.2.1].

So, while the paper presents the MNIST activation-distribution experiment as evidence consistent with BN reducing internal covariate shift, it does not claim to have rigorously proven the causal mechanism (e.g., the precise effect on gradient propagation), and explicitly flags this and related questions (RNNs, domain adaptation, deeper theory) as open/future work rather than established results.

**Retrieved:** BatchNorm p.1 (0.86); BatchNorm p.8 (0.85); BatchNorm p.2 (0.84); BatchNorm p.5-6 (0.84); BatchNorm p.6 (0.82) | gold page hit: 0.75
*17.0 s*

## Q09 (text-only, conceptual, hard, answerable: yes)

**Question.** According to the Temporal Straightening paper, why should reducing the curvature of latent trajectories make gradient-based planning easier, and do the paper's experiments generally show planning improving when the curvature regularizer is used?

**Reference answer.** Explanation (the main part). Planning minimises a Euclidean goal cost in latent space, and when latent trajectories are highly curved, straight-line distance misrepresents the geodesic distance along feasible transitions. A curvature regulariser (it penalises the angle between consecutive latent velocity vectors, i.e. maximises their cosine similarity, while a JEPA-style predictor is trained with stop-gradient on the target) straightens trajectories, which makes Euclidean latent distance a better proxy for geodesic distance and improves the conditioning of the planning objective. The theory covers linear latent dynamics: epsilon-straight transitions control the condition number of the planning Hessian, so gradient descent converges linearly at a rate set by the condition number; guarantees for nonlinear predictors are left to future work. As an illustration, the loss landscape is closer to convex after straightening (Figure 4). Experiments (general trend only). Yes: the paper reports open-loop planning success improving by 20-60% and MPC by 20-30% with a simple gradient-based planner, and says it observes a significant improvement across all models and environments. The improvement is not uniform in Table 1 (for example a from-scratch ResNet 1x384 on PointMaze-UMaze falls from 82.00 to 52.00 open-loop), so 'generally' is the right strength, in simulated goal-reaching tasks.

**System answer.** ## Why reducing curvature should ease gradient-based planning

The paper's core argument rests on the relationship between Euclidean and geodesic distance in latent space:

- Planning is posed as optimizing an action sequence by rolling the model forward and minimizing a cost between predicted latent states and a goal, typically using **Euclidean distance** as the cost metric [TemporalStraightening, p.1-2].
- When latent trajectories are **highly curved**, straight-line (Euclidean) distances in the embedding space **misrepresent the geodesic distance** along feasible transitions [TemporalStraightening, p.1-2]. This makes the induced planning objective "highly non-convex," causing gradient-based optimizers to struggle [TemporalStraightening, p.1-2].
- By imposing a curvature regularizer during training that encourages locally straightened latent trajectories, the authors make **Euclidean distance a better proxy for geodesic distance**, which **improves the conditioning of the planning objective** [TemporalStraightening, p.1, Abstract].
- They state this directly as a theoretical claim: "We prove that reducing curvature improves convergence of gradient-based planners" [TemporalStraightening, p.2].
- The conclusion reiterates the mechanism: "In this straightened representation space, the Euclidean distance provides a more reliable proxy for the geodesic distance and gradient-based planning is better conditioned" [TemporalStraightening, p.9-10].

In short: curvature regularization straightens the latent geometry → Euclidean cost aligns better with true (geodesic) feasible-path distance → the planning loss landscape becomes better-conditioned/more convex → gradient-based optimizers converge more reliably.

## Do experiments generally show improvement?

Yes, the provided evidence indicates consistent gains from using the curvature regularizer:

- The abstract/intro summarize: "open-loop planning success improves by 20–60% and MPC by 20–30% with a simple gradient-based planner" [TemporalStraightening, p.2].
- A concrete results excerpt (ResNet encoder, with vs. without the regularizer, across what appear to be increasing planning-horizon or task-difficulty columns) shows large gains when the curvature term is used (✓) versus not (✗):
  - Without (✗): 13.33 ± 3.77, 29.33 ± 9.43, 14.67 ± 6.80, 48.00 ± 9.80
  - With (✓): 10.67 ± 4.99, 33.33 ± 4.99, 76.00 ± 6.53, 98.67 ± 1.89
  [TemporalStraightening, p.9-10]
  
  Here three of the four columns show large improvements (e.g., 14.67→76.00, roughly a **+61.33 percentage-point** gain, i.e., ~5.2× increase: 76.00/14.67 ≈ 5.18; and 48.00→98.67, a **+50.67 pp** gain), while the first column shows a slight *decrease* (13.33→10.67, a −2.66 pp change).
- The conclusion states this leads to "significant and consistent gains over baselines" across a range of 2D goal-reaching tasks [TemporalStraightening, p.9-10].
- The paper also explicitly notes a caveat/limitation: the regularizer assumes a symmetric Euclidean goal cost, "which may be sub-optimal under asymmetric or irreversible dynamics," suggesting gains may not hold universally in such settings [TemporalStraightening, p.9-10].

**Summary**: Based on the passages given, the paper argues straightening improves planning by making Euclidean distance track geodesic distance, thereby better-conditioning the (otherwise non-convex) planning objective for gradient-based optimizers, and provides a theoretical convergence proof for this claim [TemporalStraightening, p.2]. The experimental table and conclusion statement support that curvature regularization generally improves planning success rates substantially, though the table includes at least one case with a small decrease, so the improvement is described as "significant and consistent" overall rather than universal in every single configuration shown [TemporalStraightening, p.9-10].

**Retrieved:** TemporalStraightening p.1 (0.87); TemporalStraightening p.9-10 (0.84); TemporalStraightening p.15-16 (0.82); TemporalStraightening p.1-2 (0.82); TemporalStraightening p.2 (0.81) | gold page hit: 0.29
*17.7 s*

## Q11 (text-only, cross-paper, medium, answerable: yes)

**Question.** ViT says it follows the original Transformer 'as closely as possible'. Which parts of the Transformer encoder does ViT keep, and how does its encoder differ from the one in 'Attention Is All You Need' (input handling, position information, normalisation placement, feed-forward activation)?

**Reference answer.** ViT keeps the Transformer encoder structure of alternating multi-head self-attention and position-wise MLP/feed-forward blocks with residual connections and layer normalisation, and uses the encoder only. Differences: (1) input - ViT splits an image into patches, linearly projects them and prepends a learnable [class] token, whereas the Transformer embeds discrete input tokens; (2) position information - ViT uses standard learnable 1D position embeddings, the Transformer uses fixed sinusoidal encodings (though it found learned embeddings nearly identical); (3) normalisation - the Transformer computes LayerNorm(x + Sublayer(x)) after the residual addition, while ViT applies layer norm before every block and residual connections after every block; (4) the feed-forward layer uses ReLU in the Transformer and GELU in ViT. The Transformer paper additionally has a decoder with encoder-decoder attention.

**System answer.** The provided passages do **not** contain the section of the ViT paper where the architecture equations (and the explicit comparison to the original Transformer encoder) are laid out, so I cannot fully answer the question about normalization placement or feed‑forward activation function from this evidence. Here is what the passages do, and do not, establish:

**What the passages support:**

1. **Standard Transformer encoder reused, with minimal image-specific bias**
ViT states it introduces "no image-specific inductive biases into the architecture apart from the initial patch extraction step," interpreting an image as a sequence of patches "processed by a standard Transformer encoder as used in NLP" [ViT, p.9-10].

2. **Input handling differs: patches instead of tokens**
Rather than feeding word/token embeddings as in the original Transformer, ViT linearly projects flattened image patches into the embedding space. The first layer "linearly projects the flattened patches into a lower-dimensional space" [ViT, p.8-9], and the embedding filters resemble basis functions for the fine structure of each patch [ViT, p.8-9].

3. **Position information: learned embeddings added once at the input, not per-layer**
ViT's default approach (used in all experiments except the ablation) is to "add position embeddings to the patch representations" at the stem of the model, before the Transformer encoder [ViT, p.18-19]. The ablation study compared this to (2) adding learned positional embeddings at the start of each layer, and (3) a shared learned positional embedding added at each layer, finding "little to no difference between different ways of encoding positional information" [ViT, p.18-19]. The learned embeddings encode 2D topology: "closer patches tend to have more similar position embeddings" and "patches in the same row/column have similar embeddings" [ViT, p.8-9].

**What the passages do NOT establish:**
- Normalization placement (e.g., pre-LN vs. post-LN) in ViT's encoder relative to the original Transformer's post-LN design is not discussed in any of the given passages.
- The feed-forward activation function (e.g., GELU vs. ReLU) used in ViT's MLP blocks is not mentioned in these passages.
- The passage from "Attention Is All You Need" [Transformer, p.10] provided here only covers constituency parsing results and the paper's conclusion/references — it contains no description of the original encoder's normalization or activation choices either, so no direct comparison can be drawn from the evidence given.

**Summary:** Based on the evidence, ViT keeps the standard Transformer encoder architecture [ViT, p.9-10] and differs primarily in input handling (patch embeddings rather than token embeddings) and in how/where position information is added (learned embeddings summed once before the encoder, shown to be roughly equivalent to per-layer variants) [ViT, p.8-9; p.18-19]. The passages provided do not give evidence on normalization placement or feed-forward activation function, so those parts of the question cannot be answered from this evidence.

**Retrieved:** ViT p.9-10 (0.76); ViT p.18-19 (0.75); ViT p.8-9 (0.73); Transformer p.10 (0.73); ViT p.19-20 (0.72) | gold page hit: 0.17
*22.4 s*

## Q12 (text-only, cross-paper, hard, answerable: yes)

**Question.** MAE and I-JEPA both mask parts of an image and use a ViT encoder on the visible part. What does each method predict and with what loss, and what evidence does the I-JEPA paper give that predicting in representation space matters?

**Reference answer.** MAE reconstructs the pixel values of the masked patches with a lightweight decoder (mean squared error computed only on masked patches); the encoder sees only visible patches and normalised pixels work slightly better (Table 1d, ViT-L/16: 85.4 vs 84.9 fine-tuning, 73.9 vs 73.5 linear probing). I-JEPA is non-generative: a predictor (narrow ViT) predicts the representations of target blocks from a context block, the targets come from a target encoder that is an exponential moving average of the context encoder, and the loss is average L2 distance in representation space. In I-JEPA's own ablation (Table 7, ViT-L/16, linear probe on 1% of ImageNet labels), using target-encoder outputs gave 66.9 top-1 versus 40.7 when the loss was in pixel space, and the authors say they 'conjecture' representation-space loss is a crucial component. I-JEPA also reports about 7% slower iterations than MAE but roughly 5x fewer iterations to converge. Caveat: the pixel-space variant is I-JEPA's own ablation (different epochs: 500 vs 800), not the MAE paper's setup, and MAE does not test representation-space targets.

**System answer.** ## What each method predicts, and with what loss

**I-JEPA:** The architecture predicts *representations* of target blocks from a single context block, rather than reconstructing pixels. As the paper states, "the proposed I-JEPA method is non-contrastive and does not seek to discriminate between image patches. Rather, the goal is to predict the representations of various target blocks from a single context block. This is achieved with a Joint-Embedding Predictive Architecture, using a predictor network that is conditioned on positional embeddings corresponding to the location of the target block in the image" [I-JEPA, p.13-14]. The loss is "computed entirely in representation space, thereby giving the target encoder the ability to produce abstract prediction targets, for which irrelevant pixel-level details are eliminated" [I-JEPA, p.7-8].

**MAE:** The supplied passages use MAE only as a baseline comparator (e.g., in Tables 2–4 and the fine-tuning comparison in Table 15 [I-JEPA, p.15-16]) and refer to it as a "reconstruction-based method" that uses "block" or "random" masking strategies, where "the target is a single image block and the context is the [complement]" [I-JEPA, p.7-8]. However, **the passages do not explicitly state that MAE's loss is a pixel-wise reconstruction loss** — that detail is not given in this evidence set, only the implication that MAE is a reconstruction-based approach using masking.

## Evidence that predicting in representation space matters

The I-JEPA paper directly ablates this question: "Table 7 compares low-shot performance on 1% ImageNet-1K using a linear probe when the loss is computed in pixel-space versus representation space... it is clear that predicting in pixel-space leads to a significant degradation in the linear probing performance" [I-JEPA, p.7-8]. The paper frames this as evidence that computing the loss in representation space lets the target encoder "produce abstract prediction targets, for which irrelevant pixel-level details are eliminated" [I-JEPA, p.7-8].

**Caveat on the evidence:** The passage describes this ablation qualitatively (predicting in pixel-space "leads to a significant degradation") but the actual numeric values from Table 7 are not included in the provided excerpts, so I cannot report the specific magnitude of the degradation. Additionally, the passages do not explicitly confirm MAE's loss formulation, so a direct quantitative MAE-vs-I-JEPA loss-space comparison is not established by this evidence — only I-JEPA's internal pixel-space-vs-representation-space ablation is given.

**Retrieved:** I-JEPA p.6 (0.79); I-JEPA p.15-16 (0.78); I-JEPA p.5 (0.77); I-JEPA p.7-8 (0.76); I-JEPA p.13-14 (0.76) | gold page hit: 0.33
*28.3 s*

## Q13 (text-only, cross-paper, hard, answerable: yes)

**Question.** Distillation and BYOL both train one network to match another network's outputs. According to the two papers, what supplies the targets in each case and how does that target model come about, are labels used, and what does BYOL say about the 'mean teacher' method that it treats as closest to its slow-moving-average target?

**Reference answer.** Distillation: the targets are class probabilities from an already-trained 'cumbersome' model (an ensemble, or a single very large model trained with a strong regularizer such as dropout), softened by raising the softmax temperature. The small model is trained at the same high temperature on a transfer set and uses temperature 1 afterwards; when labels are known the objective is a weighted average of cross-entropy with the soft targets and with the correct labels, with a considerably lower weight on the label term. BYOL: the targets are the projections a target network produces for a second augmented view; the target's weights are an exponential moving average of the online network's weights (a slow-moving average of the learner itself, not a separately trained larger model), the loss gradient is not propagated into the target (stop-gradient), and an extra predictor sits only on the online branch. BYOL is a self-supervised method that works without negative pairs. BYOL describes mean teacher (MT) as also using a slow-moving-average 'teacher' to produce targets for an online 'student', with an l2 consistency loss between their softmax predictions added to a classification loss; it reports that a similar approach collapses when the classification loss is removed, whereas BYOL's added predictor prevents collapse.

**System answer.** **Note on scope:** The passages provided are all from the BYOL paper; no passage from a "Distillation" paper is included in the evidence. I therefore cannot state, with textual support, what supplies the targets in knowledge distillation or whether that target model uses labels. I can only answer the BYOL side and BYOL's discussion of Mean Teacher.

**What supplies BYOL's targets, and how does that target model arise?**
BYOL uses a second network — the "target network," parameterized by ξ — to produce the targets that the online network (parameterized by θ) is trained to predict. The target network is not trained by gradient descent; instead its parameters are an exponential/slow moving average of the online network's parameters:

ξ ← τξ + (1 − τ)θ [BYOL, p.4-5, Eq. 1]

while θ is updated by gradient descent on the BYOL loss, LBYOL_{θ,ξ} [BYOL, p.4-5, Eq. 3]. So the target model "comes about" simply by averaging previous versions of the online network over training — it is not a separately trained model and does not require labels; BYOL is explicitly a self-supervised/unsupervised method that predicts "previous versions of its outputs" [BYOL, p.10, Conclusion], with no labels involved.

**No labels used in BYOL:** Confirmed by the Conclusion, which describes BYOL as "a new algorithm for self-supervised learning of image representations" [BYOL, p.10].

**BYOL's discussion of Mean Teacher as the closest slow-moving-average method:**
- BYOL states that Mean Teacher (MT) "also uses a slow-moving average network, called teacher, to produce targets for an online network, called student," with "an ℓ2 consistency loss between the softmax predictions of the teacher and the student... added to the classification loss" over a handful of labels [BYOL, p.2-3]. So MT is a semi-supervised method: it does use some labels (via a supervised classification loss added on top of the consistency loss) [BYOL, p.2-3].
- BYOL explicitly contrasts itself: while MT's paper "demonstrates the effectiveness of MT in the semi-supervised learning case," BYOL shows "that a similar approach collapses when removing the classification loss. In contrast, BYOL introduces an additional predictor on top of the online network, which prevents collapse" [BYOL, p.2-3].
- This is elaborated in the ablations: "Removing the predictor in BYOL results in an unsupervised version of MT with no classification loss that uses image augmentations instead of the original architectural noise (e.g., dropout). This variant of BYOL collapses (Row 7 of Table 5) which suggests that the additional predictor is critical to prevent collapse in an unsupervised scenario" [BYOL, p.9-10].
- The paper concludes from this that "keeping the predictor near-optimal at all times is important to preventing collapse, which may be one of the roles of BYOL's target network" [BYOL, p.9-10] — i.e., BYOL's predictor (absent in MT) is what allows the slow-moving-average-target idea to work without any labels or classification loss, whereas MT needed the labeled classification loss to avoid collapse.

**Summary:** BYOL's target comes from an unlabeled, gradient-free exponential moving average of the online network itself; no labels are used anywhere. BYOL identifies Mean Teacher as the closest prior method using a slow-moving-average "teacher" network to generate targets for a "student," but notes MT relies on a supervised classification loss on a few labels to prevent collapse — whereas BYOL's added predictor lets it prevent collapse without any labels or classification loss [BYOL, p.2-3, p.9-10].

**Retrieved:** BYOL p.9-10 (0.76); BYOL p.2-3 (0.75); BYOL p.30-31 (0.74); BYOL p.10-11 (0.73); BYOL p.4-5 (0.73) | gold page hit: 0.33
*22.4 s*

## Q14 (text-only, cross-paper, medium, answerable: yes)

**Question.** Temporal Straightening's world model uses a ResNet encoder, a ViT predictor and stop-gradient on the target latent. What does the Straightening paper say about how it uses each, and what does each originating paper (ResNet, ViT, BYOL) say that the component is designed to do?

**Reference answer.** Temporal Straightening offers two encoder setups, one being a ResNet (He et al.) trained from scratch, and uses a ViT (Dosovitskiy et al.) as the dynamics predictor with a temporal causal attention mask for frame-level autoregressive prediction. For collapse prevention it applies stop-gradient to the target latent in the prediction loss, citing Grill et al. 2020 (the BYOL paper) among stop-gradient methods, chosen because it needs no negative samples or extra hyper-parameters; it concedes collapse is still possible in theory but says stop-gradient worked in its experiments. In the originating papers: ResNet introduces residual learning, letting stacked layers fit F(x) = H(x) - x via shortcut connections to ease optimisation of deeper networks (the degradation problem); ViT processes a sequence of image-patch embeddings with a standard Transformer encoder of alternating self-attention and MLP blocks; and BYOL trains an online network to predict a stop-gradient target network's representation without negative pairs, which it hypothesises depends on both a predictor and a slow-moving-average target (its representation collapses if either is removed).

**System answer.** Based on the passages provided, I can only answer the first part of this question (how Temporal Straightening uses each component) with direct citations, since **no passages from the original ResNet, ViT, or BYOL papers are included in the evidence given to me**. I will flag this gap explicitly rather than rely on outside knowledge.

## How Temporal Straightening uses each component

**ResNet encoder**
Temporal Straightening offers two encoder configurations for its sensory encoder $E^s_\phi$: a frozen pretrained DINOv2 backbone with a trainable projector, or "a ResNet (He et al., 2015) trained from scratch, producing features $z^v_t \in \mathbb{R}^{m_v \times d_v}$ directly" [TemporalStraightening, p.5-6]. The ResNet variant is tested empirically in Table 1 as "ResNet (from scratch)," and the straightening regularizer ($L_{curv}$) is shown to substantially raise its Wall task open-loop success rate from 4.67±3.40% to 84.00±7.12% [TemporalStraightening, p.7-8], though the paper also notes "abnormally low success rates for Wall, PointMaze-UMaze and PointMaze-Medium" for ResNet with spatial features in some configurations [TemporalStraightening, p.7-8].

**ViT predictor**
"We use a ViT (Dosovitskiy et al., 2021) as the dynamics predictor $f_\theta$" [TemporalStraightening, p.5-6]. It takes a history of latent states, action embeddings, and (when available) proprioceptive embeddings, and the paper applies "a temporal causal attention mask so tokens at time t attend only to frames $\{t-K,\dots,t-1\}$, enabling frame-level autoregressive prediction" [TemporalStraightening, p.5-6].

**Stop-gradient**
In the prediction objective, $L_{pred} = \|\hat z_{t+1} - \mathrm{sg}(z_{t+1})\|_2^2$, "where sg denotes the stop-" [gradient operator, text cut off in passage] [TemporalStraightening, p.3-4]. Figure 3's caption confirms this usage: "During training, we minimize the prediction loss between the predicted embedding $\hat z^t_t$ and the target $z^t_t$ with stop-grad in the target branch, and minimize the local curvature of embeddings" [TemporalStraightening, p.2-3]. So stop-gradient is applied to the target latent in the prediction loss so that gradients do not flow through the target branch of the encoder.

## What the originating papers say the component is designed to do

**This part of the question cannot be answered from the evidence provided.** None of the five passages given to me are from the ResNet paper (He et al.), the ViT paper (Dosovitskiy et al.), or the BYOL paper. All five passages are from the "TemporalStraightening" paper itself, which only cites these works ("ResNet (He et al., 2015)" and "ViT (Dosovitskiy et al., 2021)" [TemporalStraightening, p.5-6]) without quoting or summarizing their original design rationale, and BYOL is not mentioned at all in the supplied passages. To answer what He et al. (ResNet), Dosovitskiy et al. (ViT), or the BYOL paper themselves state as the purpose of their respective architectural components, passages from those original papers would need to be supplied.

**Retrieved:** TemporalStraightening p.3-4 (0.79); TemporalStraightening p.1 (0.78); TemporalStraightening p.7-8 (0.75); TemporalStraightening p.5-6 (0.74); TemporalStraightening p.2-3 (0.74) | gold page hit: 0.20
*23.6 s*

## Q15 (text-only, cross-paper, hard, answerable: yes)

**Question.** BabyCL's visual branch applies strong augmentations to two views of each frame. Compare the Gaussian-blur and solarization probabilities it uses for its two views with those BYOL uses for its two views, and say what the two papers report about whether negative pairs are needed.

**Reference answer.** BabyCL (Appendix A): two views per frame with strong augmentation: random resized crop to 224x224 (scale 0.2-1.0), horizontal flip, color jitter, random grayscale (0.2), Gaussian blur with probability 1.0 on view 1 and 0.1 on view 2, and solarization on view 2 with probability 0.2. BYOL (Appendix B, Table 6): Gaussian blur probability 1.0 for the first view (T) and 0.1 for the second (T'), solarization 0.0 for T and 0.2 for T', color dropping (grayscale) 0.2 for both, crops covering 8%-100% of the image. The blur, solarization and grayscale probabilities therefore match, while the lower bound of the crop scale differs (0.2 versus 8%), and BabyCL does not cite BYOL for these settings. Negatives: BabyCL's instance loss is a SimCLR objective and its cross-modal loss a symmetric InfoNCE, and it cites Zhuang et al. (2021) as finding that contrastive methods with negative sampling are most effective on SAYCam. BYOL reports state-of-the-art ImageNet results without negative pairs and finds it much less affected than SimCLR when color distortion is removed from the augmentations. Neither paper tests a BYOL-style objective in a streaming child-egocentric setting.

**System answer.** ## Augmentation probabilities (Gaussian blur & solarization)

**BabyCL** explicitly specifies asymmetric probabilities for its two SSL views:
- Gaussian blur: probability **1.0 on view 1**, probability **0.1 on view 2**
- Solarization: applied **only on view 2**, with probability **0.2** (not applied on view 1)
[BabyCL, p.14]

**BYOL**: The BYOL passages provided only discuss ablations on *color distortion* and *crop-only* augmentations (e.g., removing color distortion costs BYOL −9.1 points vs. SimCLR's −22.2 points; crop-only reduces BYOL to 59.4% and SimCLR to 40.3%) [BYOL, p.8-9]. **The supplied BYOL passages do not report specific Gaussian-blur or solarization probabilities for its two views**, so a direct numeric comparison on those two particular transforms cannot be made from this evidence.

## Negative pairs

- **BabyCL**: The visual branch uses "a SimCLR-style objective" with "NT-Xent on paired augmented views" and the multimodal branch uses "symmetric image–text InfoNCE" [BabyCL, p.14]. Both NT-Xent and InfoNCE are contrastive losses that operate over paired positive and negative examples, so BabyCL's described objectives rely on contrastive (negative-pair) formulations, though the passage does not use the explicit phrase "negative pairs."

- **BYOL**: The passage frames BYOL in contrast to SimCLR, noting that "BYOL is incentivized to keep any information captured by the target representation into its online network, to improve its predictions," and that this makes it "more robust to the choice of image augmentations than contrastive methods" [BYOL, p.8-9]. The ablation table also shows a "stop gradient of online" variant (τ=0, no target network, no predictor) collapsing to 0.3% top-1 accuracy, underscoring that BYOL's mechanism depends on the predictor/target-network bootstrapping rather than a contrastive setup [BYOL, p.8-9]. **However, the supplied BYOL passage does not contain an explicit statement that negative pairs are unnecessary for BYOL**—it only contrasts BYOL's robustness to augmentation choices with SimCLR's sensitivity, and shows that removing the predictor/target-network mechanism destroys performance.

**Summary**: The evidence establishes that BabyCL uses contrastive (NT-Xent/InfoNCE) objectives, which by construction use negative pairs, but does not explicitly discuss "whether negative pairs are needed." The BYOL evidence shows a qualitative robustness-to-augmentation contrast with SimCLR but does not explicitly state a position on the necessity of negative pairs. Based strictly on the passages given, **neither paper is shown here to make an explicit claim about "whether negative pairs are needed"**; this would require additional passages beyond what's provided.

**Retrieved:** BabyCL p.7-8 (0.78); BabyCL p.8-9 (0.78); BabyCL p.14 (0.76); BYOL p.8-9 (0.76); BabyCL p.5-6 (0.76) | gold page hit: 0.29
*22.8 s*

## Q16 (text-only, cross-paper, hard, answerable: yes)

**Question.** Daily Oracle uses a particular retriever in its retrieval-augmented setting. What is it, and what does the embedding-retrieval paper report about how that type of retriever behaves compared with dense embedding models on its LIMIT task?

**Reference answer.** Daily Oracle's constrained open-book setting uses BM25 to retrieve the top 5 articles per question, each truncated to 512 words, restricted to articles available before the resolution date and RAG cutoff. The embedding-retrieval paper finds that on LIMIT, state-of-the-art dense single-vector models struggle (full setting rarely reaches even 20% recall@100; on the 46-document version they cannot solve the task even at recall@20), whereas BM25 'comes close to perfect scores'. The authors attribute this to sparse models behaving like single vectors with very high dimensionality, but add that it is unclear how to apply sparse models to instruction-following or reasoning tasks without lexical overlap. The LIMIT result concerns a synthetic combinatorial task and says nothing about Daily Oracle's news-forecasting data.

**System answer.** Based on the passages provided, **the evidence does not establish an answer to either part of this question.**

**On Daily Oracle's retriever:** None of the Daily Oracle passages ([1] and [2]) mention a "retrieval-augmented setting" or specify any retriever (e.g., BM25, dense embeddings) used by the benchmark. These passages only describe the dataset's construction, categorization, question types/examples (Table 2), and comparisons to other forecasting benchmarks (Table 1). There is no mention of a retrieval component at all in the excerpts given.

**On the embedding-retrieval paper's findings regarding retriever type vs. LIMIT:** The EmbeddingLimits passages ([3] and [4]) discuss the theoretical limitations of single-vector dense embedding models and introduce the LIMIT dataset, stating that "even state-of-the-art models fail on this dataset despite the simple nature of the task" [EmbeddingLimits, p.1] and that the paper "calls for future research to develop methods that can resolve this fundamental limitation," suggesting alternatives like "cross-encoders or multi-vector models" [EmbeddingLimits, p.2-3]. However, these passages do **not** report a specific comparison of BM25 (or any sparse/lexical retriever) performance against dense embedding models on the LIMIT task specifically — they only mention cross-encoders and multi-vector models as alternatives in general terms, without LIMIT-specific results for those methods.

**What the passages do show:**
- Passage [5] (SWE-bench) reports BM25 retrieval performance/recall against an "oracle" retrieval setting, but this is for the SWE-bench benchmark, not for Daily Oracle or the LIMIT task, and is unrelated to the EmbeddingLimits paper's findings.
- No passage connects BM25 (or any specific retriever) to Daily Oracle's retrieval-augmented setup, nor does any passage give LIMIT-task performance numbers comparing a non-embedding retriever (like BM25) to dense embedding models.

To answer this question, additional passages would be needed — specifically ones describing Daily Oracle's retrieval-augmented experimental setup, and EmbeddingLimits content reporting actual LIMIT benchmark results comparing retriever types.

**Retrieved:** DailyOracle p.3 (0.75); DailyOracle p.4-5 (0.74); EmbeddingLimits p.2-3 (0.73); EmbeddingLimits p.1 (0.73); SWE-bench p.5-6 (0.73) | gold page hit: 0.20
*14.9 s*

## Q17 (text-only, cross-paper, medium, answerable: yes)

**Question.** Daily Oracle and FIRE-Bench both use LLMs inside their evaluation pipelines. How does each validate that automated component against human judgment, and what agreement numbers does each report?

**Reference answer.** Daily Oracle validated its LLM-based QA filtering: four human annotators rated 30 TF and 30 MC sampled QA pairs on the seven filtering principles; inter-annotator agreement was fair (average Fleiss' kappa 0.26), and the LLM scores matched the human consensus with 89.52% accuracy across the seven principles and 85.00% for the final accept/reject decision (threshold of 13 points). FIRE-Bench validated its automated claim extraction and entailment-based scoring by human validation on a 33% subset of reference instances, reporting precision 0.95, recall 0.86 and F1 0.89. The two validate different components (question quality versus claim matching) with different metrics, so the numbers are not directly comparable.

**System answer.** The provided passages do not establish an answer to this question for either paper.

- **Daily Oracle**: The passages mention that GPT-3.5/GPT-4o-mini/GPT-4o are used to categorize questions by topic [DailyOracle, p.4-5], and that Section 3.3 of the paper conducts "a human [evaluation]" [DailyOracle, p.3], but no passage here provides the actual human-validation methodology or any numerical agreement score between the LLM component and human judgment.

- **FIRE-Bench**: The passage describes the benchmark as scoring agents' rediscovered findings "against the study's documented findings" [FIRE-Bench, p.1], implying some automated/LLM-based scoring judge is likely involved, but no passage here describes a human-validation procedure for that judge or reports any agreement number.

In short, the evidence given does not contain the specific validation methods or agreement statistics (e.g., percent agreement, kappa, etc.) for either Daily Oracle's categorization/evaluation LLM or FIRE-Bench's scoring mechanism against human judgment. Additional passages (e.g., the human evaluation details referenced in Daily Oracle's Section 3.3, or FIRE-Bench's methodology/evaluation sections) would be needed to answer this question.

**Retrieved:** DailyOracle p.3 (0.74); DailyOracle p.1 (0.71); FIRE-Bench p.1 (0.70); DailyOracle p.4-5 (0.70); DailyOracle p.17-19 (0.70) | gold page hit: 0.50
*8.3 s*

## Q18 (text-only, insufficient-evidence, medium, answerable: no)

**Question.** According to the distillation paper, what accuracy does a single network reach on the JFT dataset after the knowledge in the specialist models has been distilled back into it?

**Reference answer.** The supplied paper does not establish this. For JFT it reports an ensemble of a generalist baseline plus 61 specialist models whose predictions are combined at inference time (top-1 test accuracy 25.0% to 26.1%, a 4.4% relative improvement; conditional accuracy 43.1% to 45.9%), and it states 'We have not yet shown that we can distill the knowledge in the specialists back into the single large net'. A related idea (using soft targets to stop specialists overfitting) is described as one it is 'currently exploring'. Where the paper does distill, it reports MNIST and speech results (a single acoustic model recovering more than 80% of the frame-accuracy gain of a 10-model ensemble), not JFT.

**System answer.** The evidence does not establish this. The paper explicitly states that this distillation step was not performed: "We have not yet shown that we can distill the knowledge in the specialists back into the single large net" [Distillation, p.8-9].

What the passages do show is:
- The specialist models were only used at inference time in an ensemble combination with the generalist model, not distilled into a single network [Distillation, p.7-8].
- With 61 specialist models combined with the baseline generalist, there was a "4.4% relative improvement in test accuracy overall" on JFT [Distillation, p.5-6], but this reflects ensemble inference, not a distilled single network.

So no accuracy figure for a single network with specialist knowledge distilled back into it is given, because the authors state this experiment had not yet been done.

**Retrieved:** Distillation p.7-8 (0.78); Distillation p.5 (0.77); Distillation p.5-6 (0.76); Distillation p.3-4 (0.74); Distillation p.8-9 (0.73) | gold page hit: 1.00
*6.5 s*

## Q20 (text-only, insufficient-evidence, easy, answerable: no)

**Question.** According to the SWE-bench paper, what resolve rate do agent-based systems (models that run code, navigate the repository and iterate) reach on SWE-bench?

**Reference answer.** The supplied paper does not establish this. It evaluates single-pass language models (ChatGPT-3.5, GPT-4, Claude 2 and others, and the fine-tuned SWE-Llama) that are given BM25-retrieved or oracle files and generate one patch, and its main-text resolve rates are all single-digit percentages (for example Claude 2 resolves 4.8% with oracle retrieval). Agent-based methods appear only as an intended direction: the task can serve as a level playing field for approaches 'ranging from retrieval and long-context models to decision-making agents', and the authors 'encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs)'. No agent results are reported.

**System answer.** The provided passages do not report a resolve rate for agent-based systems. The paper's main results discuss retrieval-based (BM25 and "Oracle") settings for models like Claude 2, ChatGPT-3.5, GPT-4, and SWE-Llama, with the best result being Claude 2 solving 1.96% of issues overall [SWE-bench, p.1] and up to 4.80% under the "Oracle" retrieval setting [SWE-bench, p.26-27].

Agent-based approaches are only mentioned as a direction for **future work**, not as something evaluated in this paper: "we do not intend to constrain future methodologies to the same type of approach and encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs)" [SWE-bench, p.9-11].

So, based solely on this evidence, the paper does not provide a resolve rate achieved by agent-based systems that run code, navigate the repository, and iterate.

**Retrieved:** SWE-bench p.1 (0.77); SWE-bench p.26-27 (0.75); SWE-bench p.9-11 (0.75); SWE-bench p.3-4 (0.73); SWE-bench p.2-3 (0.73) | gold page hit: 0.50
*7.3 s*

## Q21 (table-only, tabular, medium, answerable: yes)

**Question.** Among result rows with at most 30 million parameters, which three have the highest ImageNet-Sketch top-1, and what is each one's ImageNet validation top-1?

**Reference answer.** 1) resnext50_32x4d.fb_swsl_ig1b_ft_in1k (224 px, 25.03M params): Sketch 50.532, validation 82.162. 2) resnet50.fb_swsl_ig1b_ft_in1k (224 px, 25.56M): Sketch 49.516, validation 81.146. 3) tiny_vit_21m_512.dist_in22k_ft_in1k (512 px, 21.27M): Sketch 47.238, validation 86.444. The model with the highest Sketch score is not the one with the highest validation accuracy.

**System answer.** Among models with ≤30M parameters, the three with the highest ImageNet-Sketch top-1 accuracy (per the timm database query) are:

1. **resnext50_32x4d.fb_swsl_ig1b_ft_in1k** — ImageNet-Sketch top-1: 50.532; ImageNet validation top-1: 82.162
2. **resnet50.fb_swsl_ig1b_ft_in1k** — ImageNet-Sketch top-1: 49.516; ImageNet validation top-1: 81.146
3. **tiny_vit_21m_512.dist_in22k_ft_in1k** — ImageNet-Sketch top-1: 47.238; ImageNet validation top-1: 86.444

**SQL:** `SELECT model, top1_sketch, top1_val FROM model_results WHERE param_count_m <= 30 AND top1_sketch IS NOT NULL ORDER BY top1_sketch DESC LIMIT 3;` | overlap with reference result: 0.64
*9.6 s*

## Q23 (table-only, tabular, medium, answerable: yes)

**Question.** Among rows with ImageNet validation top-1 of at least 85%, which three lose the least accuracy when moving from ImageNet validation to ImageNet-Sketch?

**Reference answer.** 1) vit_so400m_patch14_siglip_gap_378.webli_ft_in1k (378 px): validation 89.056, Sketch 71.717, change -17.339. 2) vit_so400m_patch14_siglip_378.webli_ft_in1k (378 px): 89.41 to 71.489, change -17.921. 3) eva_giant_patch14_336.clip_ft_in1k (336 px): 89.462 to 71.2, change -18.262.

**System answer.** Based on the SQL query results, among models with ImageNet validation top‑1 ≥ 85%, the three that lose the **least** accuracy when moving to ImageNet‑Sketch (i.e., have the smallest, least-negative `top1_diff_sketch`) are:

| Rank | Model | img_size | top1_val | top1_sketch | top1_diff_sketch |
|---|---|---|---|---|---|
| 1 | vit_so400m_patch14_siglip_gap_378.webli_ft_in1k | 378 | 89.056 | 71.717 | **-17.339** |
| 2 | vit_so400m_patch14_siglip_378.webli_ft_in1k | 378 | 89.410 | 71.489 | **-17.921** |
| 3 | eva_giant_patch14_336.clip_ft_in1k | 336 | 89.462 | 71.200 | **-18.262** |

Calculation check (diff = top1_sketch − top1_val):
- 71.717 − 89.056 = -17.339 ✓
- 71.489 − 89.410 = -17.921 ✓
- 71.200 − 89.462 = -18.262 ✓

Since the query ordered by `top1_diff_sketch DESC`, the least negative (smallest loss) values appear first, so **vit_so400m_patch14_siglip_gap_378.webli_ft_in1k** has the smallest drop (-17.339 points), followed by **vit_so400m_patch14_siglip_378.webli_ft_in1k** (-17.921) and **eva_giant_patch14_336.clip_ft_in1k** (-18.262).

Note: This answer is based solely on the provided SQL query result from the timm database; no paper passages were supplied for this question, so no [paper, p.N] citations apply.

**SQL:** `SELECT model, img_size, top1_val, top1_sketch, top1_diff_sketch FROM model_results WHERE top1_val >= 85   AND top1_sketch IS NOT NULL ORDER BY top1_diff_sketch DESC LIMIT 3;` | overlap with reference result: 1.00
*14.7 s*

## Q24 (table-only, tabular, medium, answerable: yes)

**Question.** Consider the five ResNet depths (resnet18, 34, 50, 101, 152) at 224 px. Among weight tags that exist for all five depths, which tag has the highest mean ImageNet top-1, and which has the largest gap between resnet152 and resnet18?

**Reference answer.** Five tags exist for all five depths. Highest mean top-1: a1_in1k (78.36; depths 71.504, 76.42, 80.382, 81.494, 81.998), then a2_in1k 77.818, gluon_in1k 76.403, a3_in1k 75.936, tv_in1k 74.988. Largest resnet152-minus-resnet18 gap: a3_in1k at 12.298 points (68.25 to 80.548); the smallest is tv_in1k at 8.578.

**System answer.** Based on the SQL query results restricted to weight tags present for all five ResNet depths (18/34/50/101/152) at 224px:

- **Highest mean top-1 accuracy**: `a1_in1k`, with a mean top-1 of **78.3596**.
- **Largest resnet152 − resnet18 gap**: `a3_in1k`, with a gap of **12.298** percentage points.

So the two criteria pick different tags: `a1_in1k` wins on average accuracy across depths, while `a3_in1k` shows the biggest spread between the deepest and shallowest model.

**SQL:** `WITH base AS (     SELECT arch, weights_tag, top1_val     FROM model_results     WHERE arch IN ('resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152')       AND img_size = 224 ), valid_tags AS (     SELECT weights_tag     FROM base     GROUP BY weights_tag     HAVING COUNT(DISTINCT arch) = 5 ), stats AS (     SELECT b.weights_tag,            AVG(b.top1_val) AS mean_top1,            MAX(CASE WHEN b.arch = 'resnet152' THEN b.top1_val END)              - MAX(CASE WHEN b.arch = 'resnet18' THEN b.top1_val END) AS gap_152_minus_18     FROM base b     JOIN valid_tags v ON b.weights_tag = v.weights_tag     GROUP BY b.weights_tag ) SELECT 'highest_mean_top1' AS metric, weights_tag, mean_top1 AS value FROM stats WHERE mean_top1 = (SELECT MAX(mean_top1) FROM stats)  UNION ALL  SELECT 'largest_gap_152_vs_18' AS metric, weights_tag, gap_152_minus_18 AS value FROM stats WHERE gap_152_minus_18 = (SELECT MAX(gap_152_minus_18) FROM stats);` | overlap with reference result: 0.25
*25.1 s*

## Q25 (table-only, tabular, hard, answerable: yes)

**Question.** For the ResNet depths with the a1_in1k weights at 224 px, going from each depth to the next one, how many ImageNet top-1 points are gained per added GMAC, and which step gives the least?

**Reference answer.** Ordering by GMACs gives resnet18 (1.82), resnet34 (3.67), resnet50 (4.11), resnet101 (7.83), resnet152 (11.56). Top-1 gain per added GMAC: 18 to 34: +4.916 for +1.85 GMACs = 2.657; 34 to 50: +3.962 for +0.44 = 9.005; 50 to 101: +1.112 for +3.72 = 0.299; 101 to 152: +0.504 for +3.73 = 0.135. The least is resnet101 to resnet152 (0.135 points per GMAC).

**System answer.** Based on the SQL query against the timm database (ResNet architectures, `a1_in1k` weights, 224 px), here are the top‑1 gains per added GMAC for each consecutive depth step:

| Step (depth → depth) | Top‑1 gain | GMAC increase | Top‑1 / GMAC |
|---|---|---|---|
| 18 → 34 | 4.916 | 1.85 | 2.657 |
| 34 → 50 | 3.962 | 0.44 | 9.005 |
| 34 → 50 | 4.310 | 0.68 | 6.338 |
| 50 → 101 | 1.112 | 3.72 | 0.299 |
| 50 → 101 | 0.764 | 3.48 | 0.220 |
| 101 → 152 | 0.504 | 3.73 | **0.135** |

(Note: the query returned two rows each for the 34→50 and 50→101 steps, likely from duplicate benchmark entries for those architectures in `benchmark_infer`.)

**Least efficient step:** The **101 → 152** depth increase gives the smallest gain per added compute — only **0.135 top‑1 points per GMAC** (a gain of 0.504 top‑1 points for 3.73 extra GMACs). This is clearly the worst "bang for the buck" among all transitions, far below the 18→34 step (2.657) and the 34→50 steps (6.3–9.0), confirming diminishing returns on accuracy as ResNet depth increases from 101 to 152 under the a1_in1k training recipe.

**SQL:** `WITH r AS (   SELECT     m.arch,     m.top1_val,     b.gmacs,     CAST(substr(m.arch, 7) AS INTEGER) AS depth   FROM model_results m   JOIN benchmark_infer b     ON m.arch = b.arch AND m.img_size = b.img_size   WHERE m.weights_tag = 'a1_in1k'     AND m.img_size = 224     AND m.arch LIKE 'resnet%'     AND m.arch GLOB 'resnet[0-9]*' ), steps AS (   SELECT     r1.depth AS depth_from,     r2.depth AS depth_to,     r2.top1_val - r1.top1_val AS top1_gain,     r2.gmacs - r1.gmacs AS gmac_increase,     (r2.top1_val - r1.top1_val) / (r2.gmacs - r1.gmacs) AS top1_per_gmac   FROM r r1   JOIN r r2     ON r2.depth = (       SELECT MIN(depth) FROM r WHERE depth > r1.depth     ) ) SELECT * FROM steps ORDER BY top1_per_gmac ASC;` | overlap with reference result: 0.75
*17.3 s*

## Q27 (table-only, tabular, medium, answerable: yes)

**Question.** For the torchvision-style weights (tag tv_in1k) of the five ResNet depths at 224 px, how does the accuracy drop from ImageNet validation to ImageNet-V2 change with depth, and which depth has the largest drop?

**Reference answer.** ImageNet-V2 change (V2 top-1 minus validation top-1) by depth: resnet18 -12.402 (69.752 to 57.35), resnet34 -12.088, resnet50 -12.966, resnet101 -11.464, resnet152 -11.29. The largest drop is resnet50 (-12.966); the smallest is resnet152 (-11.29). The trend with depth is downward overall but not monotonic (resnet50 is worse than resnet34 and resnet18).

**System answer.** ## Accuracy drop from ImageNet‑val → ImageNet‑V2 (tv_in1k, 224 px)

| Depth | top1_val | top1_v2 | Drop (top1_diff_v2) |
|---|---|---|---|
| resnet18 | 69.752 | 57.35 | ‑12.402 |
| resnet34 | 73.298 | 61.21 | ‑12.088 |
| resnet50 | 76.156 | 63.19 | **‑12.966** |
| resnet101 | 77.404 | 65.94 | ‑11.464 |
| resnet152 | 78.33 | 67.04 | ‑11.29 |

Ordering the rows by depth (18 → 34 → 50 → 101 → 152) and looking at `top1_diff_v2`, the drop does **not** change monotonically with depth:

- 18 → 34: drop shrinks slightly, from ‑12.402 to ‑12.088 (change = +0.314, i.e. a smaller drop).
- 34 → 50: drop jumps up sharply to ‑12.966 (change = ‑0.878, i.e. a much larger drop).
- 50 → 101: drop shrinks substantially to ‑11.464 (change = +1.502).
- 101 → 152: drop shrinks further to ‑11.29 (change = +0.174).

So as depth increases past 50, the val→V2 drop generally gets smaller (the deeper nets at 101/152 generalize relatively better to V2), but there is a clear exception at depth 50, which breaks the pattern seen at 18/34 and reverses it before the drop shrinks again at 101/152.

**Largest drop:** `resnet50`, with a decrease of **‑12.966 points** (76.156 → 63.19) — the biggest drop among all five depths in this result set.

All figures are taken directly from the SQL query result on the timm `model_results` table (`weights_tag = 'tv_in1k'`, `img_size = 224`); no external data was used.

**SQL:** `SELECT   arch,   img_size,   top1_val,   top1_v2,   top1_diff_v2 FROM model_results WHERE weights_tag = 'tv_in1k'   AND img_size = 224   AND arch IN ('resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152') ORDER BY top1_diff_v2 ASC;` | overlap with reference result: 0.68
*17.0 s*

## Q29 (table-only, tabular, easy, answerable: yes)

**Question.** What is the highest ImageNet top-1 among rows with fewer than 10 million parameters, and how does it compare with the best row at 25 million parameters or fewer and the best row overall?

**Reference answer.** Under 10M parameters: mobilenetv4_conv_medium.e250_r384_in12k_ft_in1k (384 px), 82.776 top-1, 9.72M params. At most 25M: tiny_vit_21m_512.dist_in22k_ft_in1k (512 px), 86.444, 21.27M (+3.668 points). Overall: eva02_large_patch14_448.mim_m38m_ft_in22k_in1k (448 px), 90.056, 305.08M params. Relative to the overall best, the under-10M model gives up 7.28 top-1 points with about 31x fewer parameters.

**System answer.** Based on the database query results:

- **Best under 10M params:** 82.776 top-1
- **Best under 25M params:** 86.444 top-1
- **Best overall:** 90.056 top-1

**Comparison:**
- Moving from the <10M to the ≤25M parameter budget gains **86.444 − 82.776 = 3.668** points of top-1 accuracy.
- Moving from the <10M budget to the best model overall (no parameter limit) gains **90.056 − 82.776 = 7.280** points.
- The ≤25M model is still **90.056 − 86.444 = 3.612** points behind the best overall model.

So accuracy increases substantially as the parameter budget is relaxed, with roughly half of the total gap between the smallest and largest models (7.280 points) already closed by the time the budget reaches 25M parameters.

Note: this answer is based solely on the SQL query result provided; no paper passages were given, so I cannot attribute these figures to specific model architectures or papers.

**SQL:** `SELECT   (SELECT MAX(top1_val) FROM model_results WHERE param_count_m < 10) AS best_under_10m,   (SELECT MAX(top1_val) FROM model_results WHERE param_count_m <= 25) AS best_under_25m,   (SELECT MAX(top1_val) FROM model_results) AS best_overall;` | overlap with reference result: 0.20
*11.7 s*

## Q30 (table-only, tabular, hard, answerable: yes)

**Question.** At 224 px, using each model's listed ImageNet top-1 and its architecture's measured inference throughput (samples/s), which models are on the accuracy-throughput Pareto frontier (no other 224-px model has both higher-or-equal top-1 and higher-or-equal throughput, with at least one strictly higher), how many are there, and how many of them have top-1 of at least 85%?

**Reference answer.** There are 26 frontier rows out of 783 result rows at 224 px, running from eva_giant_patch14_224.clip_ft_in1k (88.896 top-1, 240.83 samples/s) to efficientvit_m0.r224_in1k (63.304, 77,772.14 samples/s). Eleven have top-1 of at least 85%: eva_giant_patch14_224.clip_ft_in1k, beitv2_large_patch16_224.in1k_ft_in22k_in1k, beit_large_patch16_224.in22k_ft_in22k_in1k, deit3_large_patch16_224.fb_in22k_ft_in1k, convnextv2_base.fcmae_ft_in22k_in1k, mambaout_base_plus_rw.sw_e150_in12k_ft_in1k, convnext_large.fb_in22k_ft_in1k, coatnet_2_rw_224.sw_in12k_ft_in1k, beitv2_base_patch16_224.in1k_ft_in22k_in1k, vit_base_patch16_clip_224.laion2b_ft_in12k_in1k, tiny_vit_21m_224.dist_in22k_ft_in1k.

**System answer.** Based on the database query results, there are **26 models** on the accuracy–throughput Pareto frontier at 224 px, and **11 of them** have top-1 accuracy ≥ 85%.

**Full Pareto frontier (ordered by throughput, descending):**

| Model | top1 | samples/s |
|---|---|---|
| efficientvit_m0.r224_in1k | 63.304 | 77772.14 |
| mobilenetv4_conv_small_050.e3000_r224_in1k | 64.778 | 57208.51 |
| efficientvit_m1.r224_in1k | 68.34 | 49531.88 |
| shvit_s1.in1k | 72.78 | 48051.75 |
| efficientvit_m3.r224_in1k | 73.394 | 40863.87 |
| shvit_s2.in1k | 75.184 | 38960.54 |
| levit_128s.fb_dist_in1k | 76.52 | 30353.33 |
| levit_conv_128s.fb_dist_in1k | 76.534 | 30016.26 |
| shvit_s3.in1k | 77.356 | 25254.66 |
| levit_conv_128.fb_dist_in1k | 78.488 | 20143.06 |
| levit_conv_192.fb_dist_in1k | 79.86 | 18017.24 |
| levit_256.fb_dist_in1k | 81.506 | 13220.48 |
| vit_base_patch32_clip_224.laion2b_ft_in12k_in1k | 83.304 | 12150.93 |
| hgnetv2_b4.ssld_stage2_ft_in1k | 83.7 | 6126.27 |
| deit3_medium_patch16_224.fb_in22k_ft_in1k | 84.55 | 4876.31 |
| **tiny_vit_21m_224.dist_in22k_ft_in1k** | **85.088** | 3790.67 |
| **vit_base_patch16_clip_224.laion2b_ft_in12k_in1k** | **86.204** | 3355.89 |
| **beitv2_base_patch16_224.in1k_ft_in22k_in1k** | **86.494** | 2714.29 |
| **coatnet_2_rw_224.sw_in12k_ft_in1k** | **86.582** | 1307.99 |
| **convnext_large.fb_in22k_ft_in1k** | **86.612** | 1214.27 |
| **mambaout_base_plus_rw.sw_e150_in12k_ft_in1k** | **86.642** | 1186.01 |
| **convnextv2_base.fcmae_ft_in22k_in1k** | **86.752** | 961.39 |
| **deit3_large_patch16_224.fb_in22k_ft_in1k** | **86.99** | 881.59 |
| **beit_large_patch16_224.in22k_ft_in22k_in1k** | **87.486** | 877.09 |
| **beitv2_large_patch16_224.in1k_ft_in22k_in1k** | **88.406** | 875.21 |
| **eva_giant_patch14_224.clip_ft_in1k** | **88.896** | 240.83 |

(Bolded rows = the 11 models with top-1 ≥ 85%, confirmed by the query's `pareto_models_top1_ge_85 = 11` column.)

**Summary:**
- Total Pareto-optimal models: **26**
- Of these, with top-1 ≥ 85%: **11**

Note: This answer is derived entirely from the SQL query result provided; no paper passages were included in this turn, so no in-text citations apply here.

**SQL:** `WITH base AS (   SELECT mr.model AS model,          mr.top1_val AS top1,          bi.samples_per_sec AS tput   FROM model_results mr   JOIN benchmark_infer bi     ON mr.arch = bi.arch AND mr.img_size = bi.img_size   WHERE mr.img_size = 224     AND mr.top1_val IS NOT NULL     AND bi.samples_per_sec IS NOT NULL ), pareto AS (   SELECT b.model, b.top1, b.tput   FROM base b   WHERE NOT EXISTS (     SELECT 1 FROM base b2     WHERE b2.top1 >= b.top1       AND b2.tput >= b.tput       AND (b2.top1 > b.top1 OR b2.tput > b.tput)   ) ) SELECT   model,   top1,   tput,   (SELECT COUNT(*) FROM pareto) AS total_pareto_models,   (SELECT COUNT(*) FROM pareto WHERE top1 >= 85) AS pareto_models_top1_ge_85 FROM pareto ORDER BY tput DESC;` | overlap with reference result: 0.74
*28.3 s*

## Q31 (text+table, cross-source, medium, answerable: yes)

**Question.** The ViT paper says smaller patches make a Transformer more expensive. Using the sequence length it implies for 224-px inputs, how do the GMACs and measured throughput of ViT-Base with 32, 16 and 8 pixel patches compare with that expectation?

**Reference answer.** The ViT paper defines the number of patches (the Transformer's sequence length) as N = HW/P^2 and says smaller patch sizes are computationally more expensive. At 224 px that gives N = 49, 196 and 784 for P = 32, 16 and 8, i.e. 4x more tokens at each step. timm shows (parameters nearly constant: 88.22M, 86.57M, 86.58M): GMACs 4.41, 17.58 and 78.22, so 3.99x from B/32 to B/16 and 4.45x from B/16 to B/8; throughput 10,936.95, 2,992.79 and 700.85 samples/s, i.e. 3.65x slower and then 4.27x slower. Cost therefore grows roughly with token count while parameters stay flat; B/8 exceeds 4x in GMACs, which the paper does not explain.

**System answer.** ## Important caveat on the evidence

None of the five retrieved ViT passages explicitly states "smaller patches make a Transformer more expensive" or discusses the quadratic self‑attention cost in sequence length. The passages cover pre‑training data requirements, SOTA comparisons, positional‑embedding ablations, attention‑distance analysis, and the conclusion — none mentions patch‑size‑driven computational cost. So I cannot cite a ViT passage for that specific claim; I can only report what the database numbers show when combined with the basic patch→sequence‑length arithmetic implied by the model naming (patch32/patch16/patch8 at 224 px).

## Sequence length implied by patch size (224×224 input)

Number of tokens N = (224/patch_size)²

- patch 32: N = (224/32)² = 7² = **49**
- patch 16: N = (224/16)² = 14² = **196**
- patch 8: N = (224/8)² = 28² = **784**

Each halving of patch size quadruples the token count (×4).

## What "more expensive" would predict (self-attention scales ~N²)

If cost were dominated by self-attention (which scales as O(N²)), then:
- patch32→patch16: N×4 ⇒ expected compute ×16
- patch16→patch8: N×4 ⇒ expected compute ×16

## What the timm benchmark actually shows

GMACs (from the query):
- vit_base_patch32_224: 4.41
- vit_base_patch16_224: 17.58
- vit_base_patch8_224: 78.22

Ratios:
- 17.58 / 4.41 ≈ **4.0×** (patch32→patch16)
- 78.22 / 17.58 ≈ **4.4×** (patch16→patch8)

Throughput (samples_per_sec):
- patch32: 10936.95
- patch16: 2992.79
- patch8: 700.85

Ratios (inverse, i.e. slowdown factor):
- 10936.95 / 2992.79 ≈ **3.65×** slower (patch32→patch16)
- 2992.79 / 700.85 ≈ **4.27×** slower (patch16→patch8)

## Comparison with the quadratic expectation

- Token count quadruples (×4) at each halving of patch size, as computed above.
- A pure O(N²) self-attention cost would predict ~16× more compute at each step.
- The measured GMACs increase only ~4.0× and ~4.4×, i.e. almost exactly in line with the ×4 growth in token count — **linear in sequence length, not quadratic**.
- Measured throughput drops by a similar factor (~3.65× and ~4.27×), again close to the ×4 token-count growth rather than ×16 (note the patch8 benchmark also used a smaller batch size, 768 vs 1024, which could modestly inflate its slowdown beyond pure compute scaling).

## Conclusion

Based on the timm benchmark data, smaller patches do make ViT‑Base more expensive in GMACs and slower in throughput, consistent in direction with the general intuition that more patches (longer sequences) cost more. However, the magnitude of the increase (~4× per 4× increase in tokens) tracks **linear** scaling with sequence length rather than the **quadratic** scaling that pure self-attention cost (O(N²)) would imply (~16× expected vs. ~4–4.4× observed). This suggests that for ViT-Base's width, the linear-in-N components of the network (patch embedding, MLP layers) dominate total compute, so the quadratic attention term is not the primary driver of the empirical cost increase seen here. This inference is based on the SQL query results and basic patch/sequence-length arithmetic, not on any explicit statement in the retrieved ViT passages, which do not address this comparison.

**Retrieved:** ViT p.7-8 (0.75); ViT p.5-6 (0.74); ViT p.18-19 (0.74); ViT p.9-10 (0.73); ViT p.6-7 (0.73) | gold page hit: 0.50
**SQL:** `SELECT   m.arch,   m.img_size,   b.gmacs,   b.samples_per_sec,   b.batch_size FROM model_results m JOIN benchmark_infer b   ON m.arch = b.arch AND m.img_size = b.img_size WHERE m.arch IN ('vit_base_patch32_224', 'vit_base_patch16_224', 'vit_base_patch8_224')   AND m.img_size = 224 ORDER BY m.arch;` | overlap with reference result: 0.80
*51.4 s*

## Q32 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper reports FLOPs for its 18-, 34-, 50-, 101- and 152-layer networks. How do timm's measured GMACs at 224 px compare, and for which depth is the difference largest?

**Reference answer.** The paper's Table 1 gives 1.8, 3.6, 3.8, 7.6 and 11.3 billion FLOPs, and defines its FLOPs as multiply-adds. timm's infer_gmacs at 224 px are 1.82, 3.67, 4.11, 7.83 and 11.56, i.e. +1.1%, +1.9%, +8.2%, +3.0% and +2.3%. The largest difference is for resnet50 (4.11 vs 3.8, +8.2%). Neither PDF explains the gap, so the cause should not be asserted.

**System answer.** ## Comparison: Paper‑reported FLOPs vs. timm GMACs (224 px)

The ResNet paper reports FLOPs for the ImageNet architectures in Table 1 as:

> "FLOPs 1.8×10⁹ 3.6×10⁹ 3.8×10⁹ 7.6×10⁹ 11.3×10⁹" for the 18-, 34-, 50-, 101-, and 152-layer networks respectively [ResNet, p.5].

Converting to the same GFLOP/GMAC scale and comparing against the timm database result:

| Depth | Paper FLOPs (×10⁹) [ResNet, p.5] | timm GMACs (224px) | Absolute diff | Relative diff |
|---|---|---|---|---|
| 18  | 1.8  | 1.82  | 1.82 − 1.8 = 0.02  | 0.02/1.8 = 1.11% |
| 34  | 3.6  | 3.67  | 3.67 − 3.6 = 0.07  | 0.07/3.6 = 1.94% |
| 50  | 3.8  | 4.11  | 4.11 − 3.8 = 0.31  | 0.31/3.8 = 8.16% |
| 101 | 7.6  | 7.83  | 7.83 − 7.6 = 0.23  | 0.23/7.6 = 3.03% |
| 152 | 11.3 | 11.56 | 11.56 − 11.3 = 0.26 | 0.26/11.3 = 2.30% |

**Observations:**
- For every depth, timm's measured GMACs are slightly *higher* than the paper's reported FLOPs figures from Table 1 [ResNet, p.5].
- The gap is small (≈1–2%) for the 18-, 34-, 101-, and 152-layer networks.
- The **largest difference, both in absolute terms (0.31) and relative terms (≈8.2%), occurs at ResNet-50**.

**Caveat on evidence:** The paper text does not explain *why* ResNet-50's number diverges more than the others — the passages only give the raw FLOPs figures in Table 1 [ResNet, p.5] and describe that "50/101/152-layer ResNets... use option B for increasing dimensions" with the bottleneck design [ResNet, p.6-7], but they do not discuss any architectural detail that would specifically account for the larger discrepancy at depth 50. So while the numerical comparison above is fully supported by the provided passages and SQL result, an explanation for *why* the 50-layer gap is largest is not established by the evidence given.

**Retrieved:** ResNet p.5-6 (0.76); ResNet p.5 (0.74); ResNet p.8 (0.73); ResNet p.6-7 (0.73); ResNet p.6 (0.73) | gold page hit: 0.67
**SQL:** `SELECT arch, img_size, gmacs FROM benchmark_infer WHERE img_size = 224   AND arch IN ('resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152') ORDER BY arch;` | overlap with reference result: 0.69
*24.9 s*

## Q34 (text+table, cross-source, hard, answerable: yes)

**Question.** Among timm rows whose weights tag starts with 'mae', which has the highest ImageNet-R and ImageNet-A top-1, how do ImageNet-R and ImageNet-A top-1 change with model size across these rows, and what pre-training task does the MAE paper describe?

**Reference answer.** Six hiera_*_224.mae_in1k_ft_in1k rows are tagged mae. hiera_huge_224 is highest on ImageNet-R (64.967) and ImageNet-A (66.253) (and Sketch, 50.078), with 672.78M parameters. ImageNet-R and ImageNet-A top-1 both rise at every step with model size: R is 45.78 (tiny), 49.373 (small), 53.14 (base), 55.57 (base_plus), 60.29 (large), 64.967 (huge); A is 30.56, 36.453, 43.4, 49.24, 58.013, 66.253. The drop relative to clean top-1 on the same 200 classes also shrinks with size (R: -49.47 for tiny to -32.243 for huge; A: -65.04 to -31.717), so the larger models lose less under these shifts. The MAE paper describes pre-training that masks random patches (75% in its default) and reconstructs the missing pixels with an encoder that processes only the visible patches. Caveats: the six rows are one family (Hiera, all fine-tuned on ImageNet-1k at 224 px), so this is a trend across six rows, not a controlled test; the MAE paper's own encoder is a plain ViT, Hiera is not in the corpus, and what the timm tag implies about Hiera's recipe is not stated in the PDFs.

**System answer.** ## Highest ImageNet-R/ImageNet-A top-1 among 'mae%' rows

From the SQL result, sorted by `top1_r` descending:

**hiera_huge_224.mae_in1k_ft_in1k** has the highest values on both metrics:
- `top1_r` (ImageNet-R) = 64.967
- `top1_a` (ImageNet-A) = 66.253
- param_count_m = 672.78

## How ImageNet-R and ImageNet-A top-1 change with model size

Ordering the six rows by `param_count_m` (ascending) and showing `top1_r` / `top1_a`:

| model | params (M) | top1_r | top1_a |
|---|---|---|---|
| hiera_tiny | 27.91 | 45.78 | 30.56 |
| hiera_small | 35.01 | 49.373 | 36.453 |
| hiera_base | 51.52 | 53.14 | 43.4 |
| hiera_base_plus | 69.9 | 55.57 | 49.24 |
| hiera_large | 213.74 | 60.29 | 58.013 |
| hiera_huge | 672.78 | 64.967 | 66.253 |

Both metrics increase **monotonically** as parameter count increases — every step up in model size corresponds to a strictly higher `top1_r` and `top1_a` in this query result. The increase is quite large: from tiny to huge, `top1_r` rises by 64.967 − 45.78 = 19.187 points, and `top1_a` rises by 66.253 − 30.56 = 35.693 points — i.e., ImageNet-A top-1 scales up even more steeply with size than ImageNet-R top-1.

(Note: this pattern is only established by the database query result itself; none of the provided paper passages discuss this specific robustness/scaling trend for these timm Hiera-MAE checkpoints.)

## Pre-training task described in the MAE paper

The provided MAE passage [MAE, p.12-14] does not itself describe the pre-training task/objective — it only discusses linear-probing results, robustness evaluation on ImageNet variants (IN-A, IN-C, etc.), and scaling behavior with model/image size, noting "our MAE pre-training is 35% better on IN-A (68.2% vs 33.1%) than the supervised counterpart" [MAE, p.12-14].

However, the **ViT** paper passage describes a closely related masked-patch pre-training task (used for its own self-supervision experiments, inspired by the same masking idea underlying MAE-style methods): "we corrupt 50% of patch embeddings by either replacing their embeddings with a learnable [mask] embedding (80%), a random other patch embedding (10%) or just keeping them as is (10%)... Finally, we predict the 3-bit, mean color (i.e., 512 colors in total) of every corrupted patch using their respective patch representations" [ViT, p.13-14].

**The evidence provided does not explicitly state the MAE paper's own description of its masked autoencoding pre-training task** (e.g., masking image patches and reconstructing pixels) — the MAE passage given only covers evaluation results, not the method/objective description. To directly answer what pre-training task the MAE paper describes, a passage from the MAE paper's method section (rather than its results/robustness section) would be needed.

**Retrieved:** ViT p.13-14 (0.73); ResNet p.12 (0.73); ResNet p.5-6 (0.73); MAE p.12-14 (0.73); ViT p.6-7 (0.73) | gold page hit: 0.00
**SQL:** `SELECT model, weights_tag, param_count_m, top1_r, top1_a FROM model_results WHERE weights_tag LIKE 'mae%' ORDER BY top1_r DESC, top1_a DESC;` | overlap with reference result: 0.49
*19.0 s*

## Q35 (text+table, cross-source, hard, answerable: yes)

**Question.** For ViT models released with the same augreg recipe tag, how much higher is ImageNet top-1 when the weights come from ImageNet-21k pre-training plus ImageNet-1k fine-tuning than when trained on ImageNet-1k only, is the gain similar for the Small and Base models, and is the pattern consistent in direction with what the ViT paper says about pre-training data?

**Reference answer.** In all six matched pairs the ImageNet-21k-then-1k weights are better, by 2.56 to 5.82 points: vit_base_patch16_224 +5.38 (84.534 vs 79.154), vit_base_patch16_384 +4.908, vit_base_patch32_224 +5.824, vit_base_patch32_384 +4.608, vit_small_patch16_224 +2.56, vit_small_patch16_384 +2.684. The gain is not the same for the two sizes: the four Base rows gain 4.6 to 5.8 points (mean 5.18) and the two Small rows 2.6 to 2.7 (mean 2.62). This is consistent in direction with the ViT paper, which says large-scale pre-training helps ('large scale training trumps inductive bias') and that larger models show their benefit only with more pre-training data. It is not a confirmation: the paper's evidence uses different pre-training sets (ImageNet, ImageNet-21k, JFT-300M) and includes ViT-Large, which has no pair here, and with only two sizes a size effect cannot be separated from other differences between the Small and Base models.

**System answer.** ## ImageNet Top‑1 Accuracy: IN‑21k pretraining + IN‑1k fine‑tuning vs. IN‑1k only

From the `timm` query results (model, weights_tag, top1_val):

| Model | augreg_in1k (IN‑1k only) | augreg_in21k_ft_in1k (IN‑21k pretrain + IN‑1k finetune) | Gain |
|---|---|---|---|
| vit_small_patch16_224 | 78.842 | 81.402 | 81.402 − 78.842 = **2.560** |
| vit_base_patch16_224 | 79.154 | 84.534 | 84.534 − 79.154 = **5.380** |

**Is the gain similar for Small vs. Base?**
No. The Base model gains roughly **2× more** (5.380 points) than the Small model (2.560 points) from adding IN‑21k pretraining before IN‑1k fine‑tuning. The gains are not similar in magnitude — the larger (Base) model benefits substantially more from the additional pretraining data than the smaller (Small) model.

**Is this consistent in direction with what the ViT paper says about pre-training data?**

The ViT paper's core finding is that (a) more pre‑training data improves ViT performance, and (b) larger ViT models benefit more from larger pre-training data than smaller ones. Specifically:

- "While large ViT models perform worse than BiT ResNets... when pre-trained on small datasets, they shine when pre-trained on larger datasets. Similarly, larger ViT variants overtake smaller ones as the dataset grows." [ViT, p.6-7]
- "ViT-B/32 is slightly faster than ResNet50; it performs much worse on the 9M subset, but better on 90M+ subsets. The same is true for ResNet152x2 and ViT-L/16. This result reinforces the intuition that the convolutional inductive bias is useful for smaller datasets, but for larger ones, learning the relevant patterns directly from data is sufficient, even beneficial." [ViT, p.7-8]

Both the direction (more pre-training data → higher accuracy) and the pattern that **larger models benefit more from additional pre-training data than smaller models** observed in the timm results (Base's 5.38‑point gain vs. Small's 2.56‑point gain) are consistent with the ViT paper's qualitative claims that larger models scale better with more pre-training data. The paper does not report these exact numeric values for vit_small/vit_base with the augreg recipe (those come only from the database query), but the directional pattern matches what the paper describes.

**Retrieved:** ViT p.6-7 (0.84); MAE p.7 (0.81); ViT p.5 (0.80); ViT p.13-14 (0.79); ViT p.7-8 (0.79) | gold page hit: 0.67
**SQL:** `SELECT   model,   arch,   weights_tag,   img_size,   top1_val FROM model_results WHERE arch IN ('vit_small_patch16_224', 'vit_base_patch16_224')   AND weights_tag IN ('augreg_in1k', 'augreg_in21k_ft_in1k') ORDER BY arch, weights_tag;` | overlap with reference result: 0.27
*21.7 s*

## Q37 (text+table, cross-source, hard, answerable: yes)

**Question.** The ViT paper reports that ViT needs roughly 2-4x less compute than ResNets for the same transfer performance. In timm at 224 px, how do ViT-B/16 and ResNet-50/101/152 compare on top-1 and measured throughput, and what does that comparison say, or not say, about the paper's claim?

**Reference answer.** The paper's claim is about pre-training compute (Figure 5 is accuracy vs pre-training exaFLOPs, JFT-300M, controlled study), with the caveat that efficiency can depend on schedule, optimiser and weight decay. timm measures inference throughput and has no pre-training compute. At 224 px, taking the best ViT-B/16 row and the a1h_in1k row of each ResNet (one recipe across depths), vit_base_patch16_224.augreg2_in21k_ft_in1k has 85.108 top-1 at 2,992.79 samples/s (17.58 GMACs), versus resnet152.a1h_in1k 82.818 at 1,976.86 (11.56 GMACs), resnet101.a1h_in1k 81.95 at 2,781.19 (7.83 GMACs) and resnet50.a1h_in1k 80.654 at 4,302.84 (4.11 GMACs). So this ViT-B/16 row is more accurate than all three and faster than resnet152 (1.51x) and resnet101 (1.08x) despite more GMACs, but slower than resnet50. The ranking depends on which rows are compared: the best ResNet-50 row is resnet50.fb_swsl_ig1b_ft_in1k (81.146, trained with extra data) and is still below the best ViT-B/16 row, but the ImageNet-1k-only vit_base_patch16_224.augreg_in1k row (79.154) is below all three a1h_in1k ResNets, so the accuracy differences track pre-training data and recipe as much as architecture. These numbers neither confirm nor refute the 2-4x pre-training-compute claim.

**System answer.** ## Direct comparison of the timm numbers (224 px, best checkpoint per architecture)

Taking the highest‑top‑1 checkpoint for each architecture from the query result:

| Arch | Best checkpoint | Top‑1 | Top‑5 | Throughput (img/s) | GMACs |
|---|---|---|---|---|---|
| ViT‑B/16 | augreg2_in21k_ft_in1k | 85.108 | 97.53 | 2992.79 | 17.58 |
| ResNet‑50 | fb_swsl_ig1b_ft_in1k | 81.146 | 95.98 | 4302.84 | 4.11 |
| ResNet‑101 | a1h_in1k | 81.95 | 95.76 | 2781.19 | 7.83 |
| ResNet‑152 | a1h_in1k | 82.818 | 96.124 | 1976.86 | 11.56 |

**Accuracy:** ViT‑B/16 beats every ResNet variant's best checkpoint:
- vs ResNet50: 85.108 − 81.146 = +3.96 pts
- vs ResNet101: 85.108 − 81.95 = +3.16 pts
- vs ResNet152: 85.108 − 82.818 = +2.29 pts

**Throughput (images/sec, a proxy for compute cost at inference):**
- ResNet50 is faster than ViT‑B/16: 4302.84 / 2992.79 ≈ 1.44×
- ViT‑B/16 is faster than ResNet101: 2992.79 / 2781.19 ≈ 1.08×
- ViT‑B/16 is faster than ResNet152: 2992.79 / 1976.86 ≈ 1.51×

**GMACs (compute per forward pass):** ViT‑B/16 actually uses *more* raw compute than every ResNet, not less:
- 17.58 / 4.11 ≈ 4.28× more than ResNet50
- 17.58 / 7.83 ≈ 2.25× more than ResNet101
- 17.58 / 11.56 ≈ 1.52× more than ResNet152

## What this does and does not say about the paper's claim

The paper's claim is specifically about **pre‑training compute on JFT‑300M**: "Vision Transformers dominate ResNets on the performance/compute trade-off. ViT uses approximately 2−4× less compute to attain the same performance (average over 5 datasets)" [ViT, p.7]. This conclusion is drawn from Figure 5/Table 6, which plot total pre‑training exaFLOPs (across models pretrained for 7–14 epochs on JFT‑300M) against downstream transfer accuracy [ViT, p.15-16].

The timm data above is a **different measurement on a different axis**:
- It reports **inference throughput (images/sec) and GMACs per forward pass** on ImageNet‑sized 224px inputs, not total pre‑training FLOPs on JFT‑300M.
- The checkpoints compared were trained/fine‑tuned on various ImageNet‑1k/21k recipes (e.g., `augreg2_in21k_ft_in1k`, `fb_swsl_ig1b_ft_in1k`, `a1h_in1k`), not the JFT‑300M pre‑training setup the paper's scaling claim is based on.

So, from the evidence given:
- The timm data **is consistent with** the general qualitative finding that ViT can reach higher accuracy than comparable ResNets (ViT‑B/16 beats ResNet50/101/152 by 2.3–4.0 top‑1 points).
- However, the timm GMACs numbers show ViT‑B/16 requires **more**, not less, compute per inference than any of the three ResNets (1.5×–4.3× more GMACs), and its measured throughput is only faster than ResNet101/152, not ResNet50.
- Because the timm query measures inference-time GMACs/throughput on differently-trained checkpoints rather than total JFT‑300M pre‑training exaFLOPs, **this data does not confirm or refute the paper's specific "2–4× less pre‑training compute" claim** — it simply measures a different quantity (inference cost) under a different training regime. The evidence here only shows an accuracy advantage for ViT‑B/16 at 224px in timm, not a compute‑efficiency advantage in the sense the paper describes.

**Retrieved:** ViT p.7-8 (0.79); ViT p.15-16 (0.78); ViT p.6-7 (0.76); ViT p.5-6 (0.75); ViT p.5 (0.75) | gold page hit: 1.00
**SQL:** `SELECT   mr.arch,   mr.model,   mr.img_size,   mr.param_count_m,   mr.top1_val,   mr.top5_val,   bi.samples_per_sec,   bi.batch_size,   bi.gmacs FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.img_size = 224   AND mr.arch IN ('vit_base_patch16_224', 'resnet50', 'resnet101', 'resnet152') ORDER BY mr.arch, mr.top1_val DESC;` | overlap with reference result: 1.00
*46.6 s*

## Q40 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper says its 152-layer network has lower complexity than VGG-16/19. Using timm's measurements at 224 px, how do parameters, GMACs, throughput and top-1 of resnet152 compare with vgg16 and vgg19, and does lower FLOPs mean faster in this benchmark?

**Reference answer.** The paper says the 152-layer ResNet (11.3 billion FLOPs) has lower complexity than VGG-16/19 (15.3/19.6 billion FLOPs). timm: resnet152 has 60.19M parameters, 11.56 GMACs, 1,976.86 samples/s and tv_in1k top-1 78.33; vgg16 has 138.36M, 15.47 GMACs, 2,235.61 samples/s, top-1 71.594; vgg19 has 143.67M, 19.63 GMACs, 2,044.71 samples/s, top-1 72.4. So resnet152 has 2.3-2.4x fewer parameters, 1.34-1.70x fewer GMACs and higher top-1 (with torchvision weights), but its measured throughput is about 12% lower than vgg16 and 3% lower than vgg19 on this GPU. Lower FLOPs therefore did not mean higher throughput here; the paper's claim concerns FLOPs, not measured speed.

**System answer.** ## Complexity comparison (params & GMACs)

The ResNet paper states: "the 152-layer ResNet (11.3 billion FLOPs) still has lower complexity than VGG-16/19 nets (15.3/19.6 billion FLOPs)" [ResNet, p.6].

The timm benchmark (at 224 px) confirms this pattern in both parameter count and MACs:

| Model | Params (M) | GMACs | GMACs vs resnet152 |
|---|---|---|---|
| resnet152 | 60.19 | 11.56 | — |
| vgg16 | 138.36 | 15.47 | resnet152 uses 11.56/15.47 = 74.7% of vgg16's MACs (25.3% fewer) |
| vgg19 | 143.67 | 19.63 | resnet152 uses 11.56/19.63 = 58.9% of vgg19's MACs (41.1% fewer) |

Parameters: resnet152 (60.19M) has only 60.19/138.36 = 43.5% of vgg16's params and 60.19/143.67 = 41.9% of vgg19's params — i.e., well under half.

## Throughput

| Model | samples/sec (bs=1024) |
|---|---|
| resnet152 | 1976.86 |
| vgg16 | 2235.61 |
| vgg19 | 2044.71 |

Despite having fewer GMACs and far fewer parameters than both VGG variants, resnet152 is actually **slower** in this benchmark:
- 1976.86/2235.61 = 0.884 → resnet152 runs at ~88.4% of vgg16's throughput (about 11.6% slower).
- 1976.86/2044.71 = 0.967 → resnet152 runs at ~96.7% of vgg19's throughput (about 3.3% slower), even though vgg19 has nearly double resnet152's GMACs.

## Top-1 accuracy

| Model | top1_val (best variant) |
|---|---|
| resnet152 (a1h_in1k) | 82.818 |
| vgg16 (tv_in1k) | 71.594 |
| vgg19 (tv_in1k) | 72.400 |

resnet152 is far more accurate: ~11.2 points better than vgg16 and ~10.4 points better than vgg19. (Note: these timm top1 values come from modern training recipes, not the original paper's training procedure, so they are not directly comparable to the original ResNet/VGG top-1 numbers reported in the paper [ResNet, p.5-6, Tables 3-4]; they only serve here for a same-framework speed/accuracy comparison.)

## Does lower FLOPs/MACs mean faster?

No — not in this benchmark. resnet152 has fewer GMACs than both vgg16 (11.56 vs 15.47) and vgg19 (11.56 vs 19.63), yet its measured throughput (1976.86 samples/sec) is lower than both vgg16 (2235.61) and vgg19 (2044.71). The query results do not provide an explanation for this discrepancy (e.g., architectural factors such as depth/sequential-layer count vs. parallelizable width), so based on the evidence available, we can only state the observed mismatch: fewer MACs/parameters in resnet152 did not translate into higher throughput on this hardware/batch-size setup, even though it does translate into substantially higher accuracy.

**Retrieved:** ResNet p.5-6 (0.74); ResNet p.6-7 (0.71); ResNet p.6 (0.71); ResNet p.5 (0.71); ViT p.15-16 (0.70) | gold page hit: 0.50
**SQL:** `SELECT mr.arch,        mr.model,        mr.img_size,        mr.param_count_m,        bi.gmacs,        bi.samples_per_sec,        bi.batch_size,        mr.top1_val FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.arch IN ('resnet152', 'vgg16', 'vgg19')   AND mr.img_size = 224 ORDER BY mr.arch;` | overlap with reference result: 1.00
*30.9 s*

## Q42 (text-only, conceptual, medium, answerable: yes)

**Question.** Does the MMLU paper attribute its models' accuracy mainly to parameter count? Use its GPT-3, UnifiedQA and smaller fine-tuned model comparisons.

**Reference answer.** Not mainly: size matters but is not sufficient. In few-shot GPT-3 (Table 1) the three smaller models are near random (Small 25.9%, Medium 24.9%, Large 26.0% against 25.0% for random) while the 175B X-Large model reaches 43.9% (about 37.7% zero-shot). But UnifiedQA, fine-tuned on other QA datasets and tested without further tuning, reaches 48.9% with 11B parameters, better than GPT-3 X-Large despite an order of magnitude fewer parameters, and its smallest 60M variant gets about 29.3%. In Appendix A.1 RoBERTa-base (125M) gets 27.9%, ALBERT-xxlarge (223M) 27.1% and GPT-2 (1.5B) 32.4%; UnifiedQA-60M beats RoBERTa and ALBERT with fewer parameters and UnifiedQA-3B (43.7%) beats GPT-2, which the authors say suggests T5's larger pretraining dataset helps. They conclude that model size is a key component but fine-tuning also helps; the data-size explanation is a suggestion, and the models differ in architecture, fine-tuning data and evaluation regime (GPT-3 few-shot, UnifiedQA tested under distribution shift), so it is not a controlled test.

**System answer.** **Short answer: No — the paper explicitly says parameter count is only *one* factor, not the main explanation, and its own comparisons show fine-tuning and pretraining-data size matter independently of parameter count.**

**Evidence that size alone doesn't explain performance:**

1. **GPT-3 family**: within GPT-3, the three smaller models get "near random accuracy (around 25%)" while the 175B X-Large model reaches 43.9% few-shot accuracy [MMLU, p.6-7]. This alone would suggest size drives accuracy.

2. **UnifiedQA vs. GPT-3 (cross-model comparison)**: UnifiedQA's largest model (11B parameters) attains 48.9% accuracy, which "performs better than the few-shot GPT-3 X-Large model [175B], despite UniﬁedQA have[ing] an order of magnitude fewer parameters" [MMLU, p.6-7]. The paper's own conclusion from this comparison: "These results suggest that while model size is a key component for achieving strong performance, ﬁne-tuning also helps" [MMLU, p.6-7] — explicitly rejecting a size-only explanation.

3. **Smallest UnifiedQA model**: Even with just 60 million parameters, UnifiedQA attains ~29.3% accuracy [MMLU, p.6-7], already above the ~25% random-chance baseline that held for GPT-3 models an order of magnitude larger.

4. **Smaller fine-tuned models (Appendix A.1)**: RoBERTa-base (125M params) → 27.9%, ALBERT-xxlarge (223M params) → 27.1%, GPT-2 (1,558M params) → 32.4% [MMLU, p.11-12]. Despite having **fewer** parameters than RoBERTa-base and ALBERT-xxlarge, UnifiedQA's 60M-parameter variant (29.3%) beats both. The paper states: "It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters. This suggests that its larger pretraining dataset enables higher accuracy" [MMLU, p.11-12].

5. **Mid-size comparison**: UnifiedQA (3B params) attains 43.7%, far above the similarly-sized GPT-2 (1.5B params) at 32.4% [MMLU, p.11-12]. The paper again attributes this to pretraining data, not parameters: "This again suggests that T5's larger pretraining dataset size (and therefore UniﬁedQA's pretraining dataset size) can increase accuracy" [MMLU, p.11-12].

**Conclusion**: The passages show that parameter count correlates with accuracy within GPT-3's own model family [MMLU, p.6-7], but the cross-architecture comparisons (UnifiedQA vs. GPT-3, and UnifiedQA vs. RoBERTa/ALBERT/GPT-2) demonstrate that models with far fewer parameters can outperform larger ones. The paper's stated interpretation is that model size is "a key component" but fine-tuning and pretraining-dataset size are additional, independently important factors [MMLU, p.6-7, p.11-12] — so it does not attribute accuracy *mainly* to parameter count alone.

**Retrieved:** MMLU p.6-7 (0.80); MMLU p.11-12 (0.78); MMLU p.7-8 (0.78); MMLU p.2-3 (0.77); MMLU p.12-14 (0.76) | gold page hit: 0.67
*19.4 s*

## Q43 (text-only, cross-paper, hard, answerable: yes)

**Question.** MMLU, SWE-bench and FIRE-Bench each have to worry that a model may have seen benchmark content during training. What check does each paper run, what does it find, and how strongly does each paper state its conclusion?

**Reference answer.** MMLU (Appendix B.2): memorized questions would have low entropy and high accuracy, but accuracy and question entropy are not positively correlated (correlation between average log probability and accuracy r = -0.43 zero-shot, -0.56 few-shot), which 'suggests that our exact questions were not memorized'. The authors add that models still met text related to the questions through Wikipedia, and promise a list of question sources. SWE-bench (Section 5): resolve rates for PRs created before versus after 2023 in the oracle setting show little difference for most models (Claude 2 4.87% vs 4.23%, ChatGPT-3.5 0.49% vs 0.77%, SWE-Llama 13b 3.98% vs 3.85%), GPT-4 being the exception (1.96% vs 0.0%, on a 25% subset); the authors call this 'largely promising' since models are 'unlikely to cheat' by generating a more recent repository version, and note that new instances can be collected after a model's training date. FIRE-Bench (Section 5.4): F1 on tasks published before versus after each model's knowledge cutoff, stratified by difficulty (Table 6), shows no consistent advantage for pre-cutoff tasks; the authors call the analysis coarse (approximate cutoff dates, unknown training data, small per-category samples) and say it 'suggests the absence of a strong contamination signal rather than proving its absence'. The three checks measure different things (exact-question memorization versus date-based exposure) and none can rule contamination out, so their results are not comparable and no benchmark should be called cleaner on this evidence.

**System answer.** Based on the provided passages, only **FIRE-Bench** includes material that directly addresses a data-contamination check; the passages given for **SWE-bench** do not discuss such a check, and **no MMLU passages at all** are included in the provided evidence.

## FIRE-Bench

**Check run:** The paper "examine[s] potential data contamination effects by disentangling performance across task difficulty levels and model knowledge cutoff dates" [FIRE-Bench, p.2].

**Finding:** It finds "no strong evidence of systematic contamination" [FIRE-Bench, p.2].

**Strength of conclusion:** The language is hedged and non-definitive — "no strong evidence of systematic contamination" [FIRE-Bench, p.2] — i.e., the paper does not claim contamination is absent, only that its disentangling analysis (by difficulty level and knowledge-cutoff date) did not turn up a strong signal of it. The conclusions section ([FIRE-Bench, p.9–10]) does not revisit or further qualify this point, so the strength of the claim rests entirely on the single, cautiously-worded statement in the introduction.

## SWE-bench

The SWE-bench passages supplied here ([SWE-bench, p.11–12], the Ethics/Reproducibility Statement, and [SWE-bench, p.25–26], Appendix A.6/B/C on development-set characterization and SWE-Llama training details) **do not contain any discussion of a contamination check** — no mention of testing whether models may have seen benchmark content during pretraining. The evidence provided does not establish what check (if any) SWE-bench runs, what it finds, or how strongly it states a conclusion on this point.

## MMLU

No passages from an MMLU paper were included in the evidence provided. Therefore, the evidence does not establish what contamination check MMLU runs, what it finds, or how it states its conclusion.

## Summary

| Benchmark | Check described in evidence? | Finding | Strength of claim |
|---|---|---|---|
| FIRE-Bench | Yes — disentangles performance by task difficulty and model knowledge-cutoff date [FIRE-Bench, p.2] | "no strong evidence of systematic contamination" [FIRE-Bench, p.2] | Hedged/cautious, single mention, not elaborated elsewhere in the given passages |
| SWE-bench | Not present in supplied passages | N/A | N/A — evidence does not establish this |
| MMLU | No passages supplied | N/A | N/A — evidence does not establish this |

If you need the SWE-bench or MMLU contamination analyses, additional passages from those papers (e.g., sections specifically addressing training-data overlap or decontamination) would be required, as the current excerpts do not cover this topic for those two benchmarks.

**Retrieved:** FIRE-Bench p.2 (0.75); FIRE-Bench p.9-10 (0.75); FIRE-Bench p.19-20 (0.75); SWE-bench p.11-12 (0.74); SWE-bench p.25-26 (0.73) | gold page hit: 0.17
*16.3 s*

## Q44 (text-only, conceptual, medium, answerable: yes)

**Question.** In SWE-bench's baseline experiments, how are files chosen as model context (BM25 versus an 'oracle'), and what does the paper find about whether giving the model more retrieved context helps?

**Reference answer.** The baselines either retrieve files with BM25 at three context limits (13k, 27k and 50k tokens), because dense retrieval is ill-suited to the very long keys and queries, or use an 'oracle' setting that supplies the files edited by the reference patch. BM25 recall of the oracle files rises with the context limit (average 29.58 / 44.41 / 51.06 for 13k / 27k / 50k), but Claude 2's resolve rate falls (1.96 / 1.87 / 1.22), and the authors say performance drops even though recall rises because models are ineffective at localizing problematic code; models do best on the shortest context. With the oracle retriever Claude 2 resolves 4.8% of issues, and in the 'oracle'-collapsed setting (oracle files, with code not directly modified by the PR collapsed except for +/-15 lines) GPT-4 rises from 1.3% to 3.4% and Claude 2 from 4.8% to 5.9%.

**System answer.** ## How files are chosen as context

**BM25 retrieval:** This is the realistic, standard retrieval method where models retrieve files based on BM25 similarity scores up to a maximum context length. The paper evaluates models "on all limits that fit within its context window and report the best performance," finding that "models perform best on the shortest context window" [SWE-bench, p.5-6].

**"Oracle" retrieval:** This is an analysis-only setting where the paper "'retrieve[s]' the files edited by the reference patch that solved the issue on GitHub." The paper explicitly notes this "is less realistic, since an engineer working on addressing an issue may not know a priori which files need to be modified," and is also "not necessarily comprehensive since edited files alone may not include all the required context" [SWE-bench, p.5-6].

## Does more retrieved context help?

**No — the paper finds that more context generally hurts, not helps.**

1. **Performance degrades with longer context windows under BM25.** Table 2 shows resolve rates dropping as the context limit increases from 13k→27k→50k tokens:
   - Claude 2: 1.96 → 1.87 → 1.22
   - SWE-Llama 7b: 0.70 → 0.31 → 0.00
   - SWE-Llama 13b: 0.70 → 0.48 → 0.00
   
   The paper states directly: "models perform best on the shortest context window, as shown in Table 2" [SWE-bench, p.5-6].

2. **BM25 recall vs. oracle increases with longer context, but this doesn't translate to better resolution.** Table 3 shows BM25 "Any" recall of oracle files rising from 34.77% (13k) to 51.27% (27k) to 58.38% (50k) [SWE-bench, p.5-6]. So longer context windows do retrieve more of the relevant files, yet resolve rates still fall — indicating that added (likely noisy/irrelevant) context hurts models more than the extra relevant files help.

3. **Oracle retrieval (precise, minimal relevant files) substantially outperforms BM25.** Comparing Table 5 (BM25) to Table 18 (oracle): Claude 2 goes from 1.96% (BM25, best context) to 4.80% resolved with oracle retrieval; SWE-Llama 7b from 0.70% to 3.01%; SWE-Llama 13b from 0.70% to 3.97% [SWE-bench, p.5-6; p.26-27].

4. **Finetuned models are especially sensitive to noisy/irrelevant context.** The paper explains that SWE-Llama models were finetuned using oracle retrieval as context, and "this shift in context makes it difficult for the model to perform reliably" when given BM25-retrieved (noisier) context, since "SWE-Llama was trained to edit every file included as context whereas in the BM25 setting many files provided in context are not expected to be changed" [SWE-bench, p.7-8].

**Conclusion:** The evidence shows that simply providing *more* retrieved context (longer context windows with BM25) does not help and in fact tends to reduce resolve rates, even though it increases recall of the truly relevant ("oracle") files. Precise, minimal, correct context (oracle retrieval) is far more valuable than larger quantities of retrieved (noisier) context [SWE-bench, p.5-6, p.7-8, p.26-27].

**Retrieved:** SWE-bench p.5-6 (0.83); SWE-bench p.26-27 (0.79); SWE-bench p.7-8 (0.79); SWE-bench p.5-6 (0.77); SWE-bench p.25-26 (0.76) | gold page hit: 0.75
*14.4 s*

## Q45 (text-only, cross-paper, medium, answerable: yes)

**Question.** BYOL reports that its accuracy stays stable over a wide range of batch sizes. What does BYOL say causes the drop at smaller batch sizes, and where does the Batch Normalization paper say the statistics used for normalization come from during training?

**Reference answer.** BYOL (Figure 3a, batch sizes 128 to 4096): BYOL's performance remains stable from 256 to 4096 and only drops for smaller values 'due to batch normalization layers in the encoder'; a footnote says the only dependency on batch size in its training pipeline sits within the batch normalization layers. SimCLR, by contrast, deteriorates rapidly as the batch size falls, likely because there are fewer negative examples. BatchNorm paper: because training uses mini-batches, each mini-batch produces estimates of the mean and variance of each activation, and these statistics are used for the normalization and can fully participate in the gradient backpropagation. So during training a batch-normalized layer normalizes each example with statistics estimated from its mini-batch, which is where BYOL locates its batch-size dependence. Neither paper analyses why small batches hurt: BYOL does not explain the drop beyond naming the BN layers, and the BatchNorm paper does not discuss small-batch performance or BYOL, so the link is an inference from the two papers rather than a claim either makes.

**System answer.** **BYOL's cause for the drop at smaller batch sizes:**
BYOL states that its performance "remains stable over a wide range of batch sizes from 256 to 4096, and only drops for smaller values due to batch normalization layers in the encoder" [BYOL, p.7-8]. This is further supported by the appendix, which attributes the drop at batch size 64 to "the ill behaviour of batch normalization at low batch sizes" [BYOL, p.25-26].

**Source of normalization statistics during training (Batch Normalization paper):**
The Batch Normalization paper describes computing normalization statistics from each mini-batch during training: "each mini-batch, and backpropagate the gradients through the normalization parameters" [BatchNorm, p.8], and explicitly contrasts this with inference, where "deterministic inference that does not depend on the mini-batch" is used [BatchNorm, p.8]. In the experimental illustration, the paper also notes that the network is trained "with 60 examples per mini-batch" and Batch Normalization is added to each hidden layer [BatchNorm, p.5-6], consistent with statistics being computed per mini-batch during training (with population statistics used at inference, per Algorithm 2 referenced in the passage).

**Retrieved:** BYOL p.29-30 (0.80); BYOL p.7-8 (0.79); BYOL p.25-26 (0.78); BatchNorm p.8 (0.78); BatchNorm p.5-6 (0.76) | gold page hit: 0.67
*7.1 s*

## Q39 (text+table, cross-source, medium, answerable: yes)

**Question.** The BYOL paper reports 74.3% for a linear classifier on frozen ResNet-50 features and cites supervised ResNet-50 baselines of 76.5% and 78.9%. How many timm ResNet-50 rows at 224 px have a top-1 accuracy at or above each of these three numbers, and what limits how that comparison can be read?

**Reference answer.** The paper's numbers are 74.3% (BYOL, linear evaluation on frozen features), 76.5% and 78.9% (supervised baselines). Among timm's 18 resnet50 rows at 224 px, all 18 are at or above 74.3%, 17 are at or above 76.5% (the exception is resnet50.tv_in1k at 76.156), and 13 are at or above 78.9% (the five below are ra_in1k 78.82, bt_in1k 78.444, a3_in1k 78.052, gluon_in1k 77.58 and tv_in1k 76.156). These are not like-for-like: BYOL's 74.3% is a linear probe on self-supervised features, whereas timm's are fully supervised weights with different recipes, some using extra data (e.g. ig1b, yfcc100m), so the comparison says nothing about whether self-supervised learning is better or worse.

**System answer.** ## Answer

**From the SQL query on the timm database** (ResNet-50 architectures evaluated at 224 px, n = 18 total rows):

| Threshold | Rows meeting/exceeding it | Count |
|---|---|---|
| ≥ 74.3% (BYOL's linear-eval top-1) | 18 / 18 | all rows |
| ≥ 76.5% (BYOL's cited supervised baseline [8]) | 17 / 18 | all but one |
| ≥ 78.9% (BYOL's cited "stronger" supervised baseline [75]) | 13 / 18 | 13 rows |

So every timm ResNet-50 (224 px) entry beats BYOL's 74.3% linear-probe number, nearly all beat the 76.5% baseline, and most (13 of 18) even beat the 78.9% "stronger" baseline that BYOL described as still out of reach for its ResNet-50 (1×) result.

## What limits this comparison

1. **The 74.3% is not a fully-trained supervised number.** It comes from training a *linear classifier on frozen features* produced by BYOL's self-supervised pretraining, not from end-to-end supervised training of a ResNet-50 [BYOL, p.6]. The timm rows, by contrast, are presumably fully trained (and likely fine-tuned) supervised classifiers. Comparing a linear probe on frozen self-supervised features to fully trained supervised networks is not an apples-to-apples comparison.

2. **The 76.5% and 78.9% baselines are themselves specific, dated reference points**, not a general ceiling for ResNet-50. BYOL explicitly labels 76.5% as "the supervised baseline of [8]" and 78.9% as "the stronger supervised baseline of [75]" (MaxUp) [BYOL, p.6], and separately reports its own reproduction of a supervised ResNet-50 (1×) at 76.4% top-1 [BYOL, p.20-22, Table 9]. These were state-of-the-art-ish supervised numbers circa 2020; the timm database reflects training recipes (augmentation, schedules, distillation, extra tricks) developed over the years since, so it is expected that many newer recipes surpass them — the comparison measures recipe progress over time, not a controlled head-to-head under identical training conditions.

3. **The query result doesn't tell us what each timm row actually represents** (e.g., different augmentation strategies, distillation, extra training epochs, or test-time tricks) — the passages give no information about the timm rows' training protocols, so we cannot say whether any one of them is directly comparable in setup to BYOL's own supervised reproduction or to [8]/[75]'s baselines.

4. **Architecture variant ambiguity:** BYOL notes it uses "ResNet architectures (which are all version 1, as per [22])" [BYOL, p.20]. The evidence does not specify whether all 18 timm `resnet50` rows use the same v1-style architecture or whether some are variants (e.g., different stem/downsampling), which could affect accuracy independent of training recipe.

**In short:** the query shows that essentially all (18/18), nearly all (17/18), and most (13/18) timm ResNet-50 @224px entries meet or exceed BYOL's 74.3%, 76.5%, and 78.9% figures respectively, but the comparison is limited because BYOL's 74.3% is a linear probe on frozen self-supervised features (not a fully supervised model), the 76.5%/78.9% baselines are specific historical supervised results tied to particular training recipes, and the passages provide no detail on the training protocols behind the timm rows to confirm a controlled comparison.

**Retrieved:** BYOL p.20-22 (0.84); BYOL p.6 (0.83); BYOL p.19-20 (0.81); BYOL p.6-7 (0.80); BYOL p.18-19 (0.78) | gold page hit: 1.00
**SQL:** `SELECT   SUM(CASE WHEN top1_val >= 74.3 THEN 1 ELSE 0 END) AS n_ge_74_3,   SUM(CASE WHEN top1_val >= 76.5 THEN 1 ELSE 0 END) AS n_ge_76_5,   SUM(CASE WHEN top1_val >= 78.9 THEN 1 ELSE 0 END) AS n_ge_78_9,   COUNT(*) AS n_total_resnet50_224 FROM model_results WHERE arch = 'resnet50' AND img_size = 224;` | overlap with reference result: 1.00
*40.0 s*
