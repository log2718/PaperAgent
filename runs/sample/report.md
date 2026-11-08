# Report: runs/sample

5 questions, 0 errors, mean latency 21.4 s.

| Source type | Retrieval page hit | SQL value overlap | Answers with abstention wording |
|---|---|---|---|
| text-only | 0.72 (n=3) | - | 2 of 3 |
| table-only | - | 0.86 (n=1) | 0 of 1 |
| text+table | 0.50 (n=1) | 1.00 (n=1) | 0 of 1 |

Insufficient-evidence questions (Q18): 1 of 1 answers use abstention wording (keyword heuristic, check by reading).

Diagnostics are heuristics, not grades. *Retrieval page hit*: share of the workbook's gold evidence pages covered by retrieved chunks. *SQL value overlap*: share of cells of the workbook's reference SQL result that also appear in the system's result. Grade answers by reading them against the reference.

## Q01 (text-only, factual, medium, answerable: yes)

**Question.** In the ResNet paper's ImageNet comparison of 18-layer and 34-layer networks, how did the plain and residual versions differ, and why do the authors argue the plain network's problem is not caused by vanishing gradients?

**Reference answer.** The 34-layer plain net had higher error than the 18-layer plain net (top-1 validation error 28.54% vs 27.94%, Table 2) and higher training error throughout training; the authors call this the degradation problem. With identity shortcuts (zero-padded, so no extra parameters) the order reversed: the 34-layer ResNet reached 25.03% vs 27.88% for the 18-layer ResNet (2.8 points better). The authors argue the plain-net difficulty is unlikely to be vanishing gradients because the plain nets are trained with batch normalization, which keeps forward signals at non-zero variance, and they verified that backward gradients have healthy norms; they only conjecture that deep plain nets may have exponentially low convergence rates. Training 3x longer still showed degradation.

**System answer.** ## How plain and residual 18- and 34-layer networks differed in results

For the plain networks, depth hurt performance: the 34-layer plain net showed "higher training error throughout the whole training procedure, even though the solution space of the 18-layer plain network is a subspace of that of the 34-layer one" [ResNet, p.5]. In terms of top-1 error (10-crop testing), the 34-layer plain net was *worse* than the 18-layer plain net: 28.54% vs. 27.94% [ResNet, p.5, Table 2].

For the residual networks, the situation was reversed — "the 34-layer ResNet is better than the 18-layer ResNet (by 2.8%)" [ResNet, p.5–6]. Concretely, top-1 error was 25.03% for ResNet-34 vs. 27.88% for ResNet-18 [ResNet, p.5, Table 2]. The paper notes "the 34-layer ResNet exhibits considerably lower training error and is generalizable to the validation data. This indicates that the degradation problem is well addressed in this setting" [ResNet, p.5–6]. Additionally, compared to its plain counterpart, "the 34-layer ResNet reduces the top-1 error by 3.5%" (28.54% → 25.03%) [ResNet, p.6].

The authors also note that for the 18-layer networks specifically, plain and residual nets were "comparably accurate" (27.94% vs. 27.88%), but "the 18-layer ResNet converges faster," easing optimization via faster convergence at the early stage when the net is "not overly deep" [ResNet, p.6].

## Why the authors argue this isn't vanishing gradients

The authors give two main reasons:

1. **BN ensures healthy signal propagation.** "These plain networks are trained with BN [16], which ensures forward propagated signals to have non-zero variances. We also verify that the backward propagated gradients exhibit healthy norms with BN. So neither forward nor backward signals vanish." [ResNet, p.5]

2. **The deep plain net can still train reasonably well, and more iterations don't fix the degradation.** "In fact, the 34-layer plain net is still able to achieve competitive accuracy (Table 3), suggesting that the solver works to some extent. We conjecture that the deep plain nets may have exponentially low convergence rates, which impact the reducing of the training error" [ResNet, p.5]. They further note (footnote): "We have experimented with more training iterations (3×) and still observed the degradation problem, suggesting that this problem cannot be feasibly addressed by simply using more iterations" [ResNet, p.5–6].

Based on this, the paper explicitly states the underlying cause is left unresolved: "The reason for such optimization difficulties will be studied in the future" [ResNet, p.5]. So the evidence establishes that the authors rule out vanishing gradients via the BN-signal-norm check and the persistence of the problem despite more iterations, but it does not establish what the true cause is.

**Retrieved:** ResNet p.5 (0.84); ResNet p.5-6 (0.83); ResNet p.7-8 (0.81); ResNet p.6 (0.81); ResNet p.3-4 (0.80) | gold page hit: 1.00
*17.4 s*

## Q11 (text-only, cross-paper, medium, answerable: yes)

**Question.** ViT says it follows the original Transformer 'as closely as possible'. Which parts of the Transformer encoder does ViT keep, and how does its encoder differ from the one in 'Attention Is All You Need' (input handling, position information, normalisation placement, feed-forward activation)?

**Reference answer.** ViT keeps the Transformer encoder structure of alternating multi-head self-attention and position-wise MLP/feed-forward blocks with residual connections and layer normalisation, and uses the encoder only. Differences: (1) input - ViT splits an image into patches, linearly projects them and prepends a learnable [class] token, whereas the Transformer embeds discrete input tokens; (2) position information - ViT uses standard learnable 1D position embeddings, the Transformer uses fixed sinusoidal encodings (though it found learned embeddings nearly identical); (3) normalisation - the Transformer computes LayerNorm(x + Sublayer(x)) after the residual addition, while ViT applies layer norm before every block and residual connections after every block; (4) the feed-forward layer uses ReLU in the Transformer and GELU in ViT. The Transformer paper additionally has a decoder with encoder-decoder attention.

**System answer.** The provided passages do **not** contain the specific architectural description (normally found in ViT's "Vision Transformer" method section, e.g. §3.1) where the paper states it follows the original Transformer "as closely as possible" and details differences like feed-forward activation (GELU vs. ReLU) or LayerNorm placement (pre-norm vs. post-norm). That section is not among the passages given, so I cannot confirm those specific comparisons from this evidence.

What the given passages **do** show, which is only partially relevant:

1. **Input handling / position information**: The ablation study passage states that ViT's default setup is to "add position embeddings to the patch representations" at "the stem of the model and before feeding the inputs to the Transformer encoder" [ViT, p.18-19]. This passage also notes alternative schemes were tested (adding positional embeddings at the beginning of each layer, with or without sharing across layers), but all performed similarly, with the key gap being only between "no positional embedding" and "any positional embedding" [ViT, p.18-19].

2. **How position embeddings are learned**: "the model learns to encode distance within the image in the similarity of position embeddings, i.e. closer patches tend to have more similar position embeddings... patches in the same row/column have similar embeddings... a sinusoidal structure is sometimes apparent for larger grids" [ViT, p.8-9]. This explains why "hand-crafted 2D-aware embedding variants do not yield improvements" [ViT, p.8-9] — i.e., ViT uses standard *learned* 1D position embeddings rather than the original Transformer's fixed sinusoidal encodings, but the passage does not explicitly contrast this against the original Transformer's method.

3. **Self-attention mechanics**: ViT's self-attention "allows ViT to integrate information across the entire image even in the lowest layers," with "attention distance" analogous to CNN receptive field size, and this distance "increases with network depth" [ViT, p.8-9]. No explicit statement compares this to the original Transformer encoder's self-attention design, since the mechanism itself (multi-head self-attention + MLP block) is presumably unchanged.

4. **Axial attention variant** (an experimental modification, not the main ViT model): this modifies the standard ViT encoder block to split self-attention into row-attention + MLP followed by column-attention + MLP [ViT, p.19-20]. This is described as a departure from the default ViT encoder, not as a comparison to the original Transformer.

**What is missing**: There is no passage here stating explicitly which parts of the Transformer encoder (e.g., multi-head self-attention, residual connections, LayerNorm, position-wise feed-forward) ViT retains unchanged, nor any explicit statement about normalization placement (pre-LN vs. post-LN) or feed-forward activation function (GELU) differences relative to "Attention Is All You Need." The Transformer paper passage provided [Transformer, p.10] only covers constituency parsing results and the conclusion, with no architectural details on normalization or activation functions either.

**Conclusion**: Based solely on the evidence given, I cannot fully answer which specific parts of the encoder ViT keeps versus modifies regarding input handling, position information, normalization placement, and feed-forward activation. The passages only establish that (a) ViT adds position embeddings before the encoder by default [ViT, p.18-19], and (b) these position embeddings are learned (not the original sinusoidal ones) and come to encode 2D spatial relationships [ViT, p.8-9]. The core §3.1 architectural comparison is not present in the supplied text.

**Retrieved:** ViT p.9-10 (0.76); ViT p.18-19 (0.75); ViT p.8-9 (0.73); Transformer p.10 (0.73); ViT p.19-20 (0.72) | gold page hit: 0.17
*22.3 s*

## Q18 (text-only, insufficient-evidence, medium, answerable: no)

**Question.** According to the distillation paper, what accuracy does a single network reach on the JFT dataset after the knowledge in the specialist models has been distilled back into it?

**Reference answer.** The supplied paper does not establish this. For JFT it reports an ensemble of a generalist baseline plus 61 specialist models whose predictions are combined at inference time (top-1 test accuracy 25.0% to 26.1%, a 4.4% relative improvement; conditional accuracy 43.1% to 45.9%), and it states 'We have not yet shown that we can distill the knowledge in the specialists back into the single large net'. A related idea (using soft targets to stop specialists overfitting) is described as one it is 'currently exploring'. Where the paper does distill, it reports MNIST and speech results (a single acoustic model recovering more than 80% of the frame-accuracy gain of a 10-model ensemble), not JFT.

**System answer.** The passages do not establish this. The paper explicitly states that this distillation step was not performed: "We have not yet shown that we can distill the knowledge in the specialists back into the single large net" [Distillation, p.8-9].

What the evidence does show is related but different results on JFT:
- With the trained baseline full network combined with 61 specialist models (not distilled back into a single net, but used as an ensemble at inference time), there is a 4.4% relative improvement in test accuracy overall [Distillation, p.7-8].
- Accuracy improvements from using specialists vary by how many specialists cover a class, e.g., classes covered by 10+ specialists show a +14.1% relative top-1 accuracy improvement [Distillation, p.7-8, Table 4].

So based on the given passages, no single-network accuracy figure after distilling specialist knowledge back into one net is reported, because the authors state this had not yet been done.

**Retrieved:** Distillation p.7-8 (0.78); Distillation p.5 (0.77); Distillation p.5-6 (0.76); Distillation p.3-4 (0.74); Distillation p.8-9 (0.73) | gold page hit: 1.00
*6.7 s*

## Q21 (table-only, tabular, medium, answerable: yes)

**Question.** Among result rows with at most 30 million parameters, which three have the highest ImageNet-Sketch top-1, and what is each one's ImageNet validation top-1?

**Reference answer.** 1) resnext50_32x4d.fb_swsl_ig1b_ft_in1k (224 px, 25.03M params): Sketch 50.532, validation 82.162. 2) resnet50.fb_swsl_ig1b_ft_in1k (224 px, 25.56M): Sketch 49.516, validation 81.146. 3) tiny_vit_21m_512.dist_in22k_ft_in1k (512 px, 21.27M): Sketch 47.238, validation 86.444. The model with the highest Sketch score is not the one with the highest validation accuracy.

**System answer.** Based on the database query results (models with ≤30M parameters, ranked by ImageNet-Sketch top-1 accuracy):

| Rank | Model | Params (M) | ImageNet-Sketch Top-1 | ImageNet Val Top-1 |
|------|-------|-----------|------------------------|---------------------|
| 1 | resnext50_32x4d.fb_swsl_ig1b_ft_in1k | 25.03 | 50.532 | **82.162** |
| 2 | resnet50.fb_swsl_ig1b_ft_in1k | 25.56 | 49.516 | **81.146** |
| 3 | tiny_vit_21m_512.dist_in22k_ft_in1k | 21.27 | 47.238 | **86.444** |

**Summary:** The top three models by ImageNet-Sketch top-1 accuracy (among those with ≤30M parameters) are resnext50_32x4d.fb_swsl_ig1b_ft_in1k (82.162 val top-1), resnet50.fb_swsl_ig1b_ft_in1k (81.146 val top-1), and tiny_vit_21m_512.dist_in22k_ft_in1k (86.444 val top-1). Notably, tiny_vit has the lowest Sketch top-1 of the three but the highest standard validation top-1.

**SQL:** `SELECT model, param_count_m, top1_sketch, top1_val FROM model_results WHERE param_count_m <= 30 ORDER BY top1_sketch DESC LIMIT 3;` | overlap with reference result: 0.86
*10.3 s*

## Q31 (text+table, cross-source, medium, answerable: yes)

**Question.** The ViT paper says smaller patches make a Transformer more expensive. Using the sequence length it implies for 224-px inputs, how do the GMACs and measured throughput of ViT-Base with 32, 16 and 8 pixel patches compare with that expectation?

**Reference answer.** The ViT paper defines the number of patches (the Transformer's sequence length) as N = HW/P^2 and says smaller patch sizes are computationally more expensive. At 224 px that gives N = 49, 196 and 784 for P = 32, 16 and 8, i.e. 4x more tokens at each step. timm shows (parameters nearly constant: 88.22M, 86.57M, 86.58M): GMACs 4.41, 17.58 and 78.22, so 3.99x from B/32 to B/16 and 4.45x from B/16 to B/8; throughput 10,936.95, 2,992.79 and 700.85 samples/s, i.e. 3.65x slower and then 4.27x slower. Cost therefore grows roughly with token count while parameters stay flat; B/8 exceeds 4x in GMACs, which the paper does not explain.

**System answer.** ## Sequence length implied by patch size

For a 224×224 input, the number of tokens (patches) scales as N = (224/P)² :

| Patch size P | Grid size | Sequence length N | Ratio vs P=32 |
|---|---|---|---|
| 32 | 224/32 = 7 → 7×7 | **49** | 1× |
| 16 | 224/16 = 14 → 14×14 | **196** | 4× |
| 8 | 224/8 = 28 → 28×28 | **784** | 16× |

So halving the patch side length quadruples the token count, and going from 32→8 multiplies it by 16×. Because self-attention cost grows with sequence length (quadratically in the attention term, linearly in the per-token MLP term), the expectation is that compute (GMACs) should rise and throughput (images/sec) should fall by at least this factor as patches shrink.

## What the timm database actually shows

From the SQL query result (ViT-Base, img_size=224):

| arch | GMACs | samples/sec | param_count_m |
|---|---|---|---|
| vit_base_patch32_224 | 4.41 | 10936.95 | 88.22 |
| vit_base_patch16_224 | 17.58 | 2992.79 | 86.57 |
| vit_base_patch8_224 | 78.22 | 700.85 | 86.58 |

**GMACs ratios:**
- 32→16: 17.58 / 4.41 = 3.99× (token ratio was 4×) → essentially matches the expected 4× increase.
- 16→8: 78.22 / 17.58 = 4.45× (token ratio was 4×) → slightly *more* than linear, i.e. a bit worse than the plain N-fold expectation.
- 32→8 overall: 78.22 / 4.41 = 17.7× (token ratio was 16×) → again modestly above the 16× implied by sequence length alone.

**Throughput ratios (inverse, since higher cost → lower speed):**
- 32→16: 10936.95 / 2992.79 = 3.65× slower (vs. expected 4×) → slightly *better* than the linear expectation.
- 16→8: 2992.79 / 700.85 = 4.27× slower (vs. expected 4×) → slightly worse than linear, i.e. extra slowdown.
- 32→8 overall: 10936.95 / 700.85 = 15.6× slower (vs. expected 16×) → close to, just under, the token-count ratio.

## Comparison with expectation

The measured GMACs and throughput changes track the sequence‑length‑implied expectation quite closely:
- Going from patch 32 → 16 (4× more tokens), GMACs increase almost exactly 4× (3.99×) and throughput drops by a comparable ~3.65×.
- Going from patch 16 → 8 (another 4× more tokens), the increase in GMACs (4.45×) and the drop in throughput (4.27×) are slightly *larger* than the plain 4× token-count ratio, i.e., costs grow a bit faster than linearly with sequence length at the smallest patch size — consistent with the quadratic self-attention term becoming non-negligible once N (784) approaches the model's hidden dimension.
- Overall (32→8, 16× more tokens), GMACs rise 17.7× and throughput falls 15.6×, both close to but on either side of the 16× implied by sequence length.

So the database numbers are quantitatively consistent with — and even mildly exceed at the smallest patch size — what the implied sequence-length scaling would predict: smaller patches do make ViT-Base measurably more expensive, in both compute (GMACs) and measured inference speed (samples/sec).

**Note on evidence:** None of the supplied ViT paper passages [1]–[5] explicitly state the claim "smaller patches make a Transformer more expensive" or give the sequence-length formula N=(H·W)/P²; that formula was used here as straightforward arithmetic from the patch/image sizes, not quoted from the passages. The passages provided (e.g., [ViT, p.18-19] Appendix D.5 "Empirical Computational Costs") mention that the paper measures real-world inference speed but do not give the specific patch-8/16/32 numbers — those come only from the timm database query result, not from the paper text excerpts shown.

**Retrieved:** ViT p.7-8 (0.75); ViT p.5-6 (0.74); ViT p.18-19 (0.74); ViT p.9-10 (0.73); ViT p.6-7 (0.73) | gold page hit: 0.50
**SQL:** `SELECT   mr.model,   mr.img_size,   bi.arch,   bi.gmacs,   bi.samples_per_sec,   bi.batch_size,   bi.param_count_m FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.arch IN ('vit_base_patch32_224', 'vit_base_patch16_224', 'vit_base_patch8_224')   AND mr.img_size = 224 ORDER BY mr.arch;` | overlap with reference result: 1.00
*50.5 s*
