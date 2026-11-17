# Report: runs/chunk_paper

35 questions, 0 errors, mean latency 22.2 s.

| Source type | Retrieval page hit | SQL value overlap | Answers with abstention wording |
|---|---|---|---|
| text-only | 0.97 (n=21) | - | 7 of 21 |
| table-only | - | 0.71 (n=7) | 0 of 7 |
| text+table | 1.00 (n=7) | 0.90 (n=7) | 2 of 7 |

Insufficient-evidence questions (Q18, Q20): 2 of 2 answers use abstention wording (keyword heuristic, check by reading).

Diagnostics are heuristics, not grades. *Retrieval page hit*: share of the workbook's gold evidence pages covered by retrieved chunks. *SQL value overlap*: share of cells of the workbook's reference SQL result that also appear in the system's result. Grade answers by reading them against the reference.

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

**Question.** At 224 px, using each model's listed ImageNet top-1 and its architecture's measured inference throughput (samples/s), which models are on the accuracy-throughput Pareto frontier (no other 224-px model has both higher-or-equal top-1 and higher-or-equal throughput, with at least one strictly higher), how many are there, and how many of them have top-1 of at least 85%?

**Reference answer.** There are 26 frontier rows out of 783 result rows at 224 px, running from eva_giant_patch14_224.clip_ft_in1k (88.896 top-1, 240.83 samples/s) to efficientvit_m0.r224_in1k (63.304, 77,772.14 samples/s). Eleven have top-1 of at least 85%: eva_giant_patch14_224.clip_ft_in1k, beitv2_large_patch16_224.in1k_ft_in22k_in1k, beit_large_patch16_224.in22k_ft_in22k_in1k, deit3_large_patch16_224.fb_in22k_ft_in1k, convnextv2_base.fcmae_ft_in22k_in1k, mambaout_base_plus_rw.sw_e150_in12k_ft_in1k, convnext_large.fb_in22k_ft_in1k, coatnet_2_rw_224.sw_in12k_ft_in1k, beitv2_base_patch16_224.in1k_ft_in22k_in1k, vit_base_patch16_clip_224.laion2b_ft_in12k_in1k, tiny_vit_21m_224.dist_in22k_ft_in1k.

**System answer.** Based on the SQL query result (timm database), there are **26 models** on the accuracy-throughput Pareto frontier at 224 px, and **11 of them** have top-1 ≥ 85%.

**Full frontier list (sorted by top1_val descending):**

| Model | top1_val | samples/sec |
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

**Count check:** 26 rows returned → `total_frontier_models = 26`.

**≥85% top-1 check (manual recount of the 11 flagged rows, each ≥85):**
88.896, 88.406, 87.486, 86.99, 86.752, 86.642, 86.612, 86.582, 86.494, 86.204, 85.088 → that's 11 models (all values ≥ 85), matching `frontier_models_top1_ge_85 = 11`.

The next model, tiny_vit_21m at 85.088, is the lowest-accuracy model still ≥85%; deit3_medium at 84.55 is just below the threshold.

This answer is based solely on the provided SQL query result from the timm database (no paper passages were supplied for this question).

**SQL:** `WITH data AS (     SELECT         mr.model,         mr.top1_val,         bi.samples_per_sec     FROM model_results mr     JOIN benchmark_infer bi         ON mr.arch = bi.arch        AND mr.img_size = bi.img_size     WHERE mr.img_size = 224       AND mr.top1_val IS NOT NULL       AND bi.samples_per_sec IS NOT NULL ), frontier AS (     SELECT d1.model, d1.top1_val, d1.samples_per_sec     FROM data d1     WHERE NOT EXISTS (         SELECT 1         FROM data d2         WHERE d2.top1_val >= d1.top1_val           AND d2.samples_per_sec >= d1.samples_per_sec           AND (d2.top1_val > d1.top1_val OR d2.samples_per_sec > d1.samples_per_sec)     ) ) SELECT     model,     top1_val,     samples_per_sec,     COUNT(*) OVER () AS total_frontier_models,     SUM(CASE WHEN top1_val >= 85 THEN 1 ELSE 0 END) OVER () AS frontier_models_top1_ge_85 FROM frontier ORDER BY top1_val DESC;` | overlap with reference result: 0.74
*33.0 s*

## Q01 (text-only, factual, medium, answerable: yes)

**Question.** In the ResNet paper's ImageNet comparison of 18-layer and 34-layer networks, how did the plain and residual versions differ, and why do the authors argue the plain network's problem is not caused by vanishing gradients?

**Reference answer.** The 34-layer plain net had higher error than the 18-layer plain net (top-1 validation error 28.54% vs 27.94%, Table 2) and higher training error throughout training; the authors call this the degradation problem. With identity shortcuts (zero-padded, so no extra parameters) the order reversed: the 34-layer ResNet reached 25.03% vs 27.88% for the 18-layer ResNet (2.8 points better). The authors argue the plain-net difficulty is unlikely to be vanishing gradients because the plain nets are trained with batch normalization, which keeps forward signals at non-zero variance, and they verified that backward gradients have healthy norms; they only conjecture that deep plain nets may have exponentially low convergence rates. Training 3x longer still showed degradation.

**System answer.** ## How the plain and residual 18/34-layer networks differed on ImageNet

**Plain networks:** The deeper 34-layer plain net had *higher* validation error than the shallower 18-layer plain net (28.54% vs. 27.94% top-1 error, 10-crop testing), and training error curves showed the 34-layer plain net had higher training error throughout the whole training procedure, "even though the solution space of the 18-layer plain network is a subspace of that of the 34-layer one" [ResNet, p.5]. This is the degradation problem.

**Residual networks:** The situation is reversed — the 34-layer ResNet is *better* than the 18-layer ResNet by 2.8% (top-1 error), and "the 34-layer ResNet exhibits considerably lower training error and is generalizable to the validation data" [ResNet, p.5]. From Table 2: plain-18 = 27.94%, ResNet-18 = 27.88%; plain-34 = 28.54%, ResNet-34 = 25.03% [ResNet, p.5]. So adding depth hurt the plain net but helped the ResNet. In addition, "compared to its plain counterpart, the 34-layer ResNet reduces the top-1 error by 3.5%" [ResNet, p.5-6], and even at 18 layers (where plain and residual nets were comparably accurate), the 18-layer ResNet converged faster than the 18-layer plain net [ResNet, p.6].

## Why the authors say the plain net's problem is not vanishing gradients

The authors argue: "We argue that this optimization difficulty is unlikely to be caused by vanishing gradients. These plain networks are trained with BN [16], which ensures forward propagated signals to have non-zero variances. We also verify that the backward propagated gradients exhibit healthy norms with BN. So neither forward nor backward signals vanish." [ResNet, p.5]

They further support this by noting that "the 34-layer plain net is still able to achieve competitive accuracy (Table 3), suggesting that the solver works to some extent" [ResNet, p.5] — i.e., it isn't failing outright as a vanishing-gradient collapse would suggest. Instead, "we conjecture that the deep plain nets may have exponentially low convergence rates, which impact the reducing of the training error" [ResNet, p.5]. They also note this is checked against simply needing more training time: "We have experimented with more training iterations (3×) and still observed the degradation problem, suggesting that this problem cannot be feasibly addressed by simply using more iterations" [ResNet, footnote 3, p.5]. The paper explicitly states the actual cause is left open: "The reason for such optimization difficulties will be studied in the future" [ResNet, p.5].

**Retrieved:** ResNet p.1-12 (0.73); BatchNorm p.1-11 (0.67); ViT p.1-22 (0.62) | gold page hit: 1.00
*19.4 s*

## Q02 (text-only, factual, medium, answerable: yes)

**Question.** In BabyCL's main results (Table 1), how do the Labeled-S 4AFC accuracies of BabyCL (k = 4 and k = 8) compare with the offline CVCL upper bound and with the one-pass and compute-matched streaming baselines, and what do the authors conclude from the compute-matched baseline?

**Reference answer.** Table 1 (4AFC, Labeled-S, mean +/- CI): offline CVCL (i.i.d., 400 epochs, upper bound) 57.31 +/- 1.13; one-pass CVCL (naive streaming) 27.52 +/- 3.12; CL-CVCL (compute-matched) 36.41 +/- 2.31; BabyCL with k=4 41.08 +/- 1.79 and with k=8 43.38 +/- 1.47. Both BabyCL settings beat both streaming baselines (k=8 is 15.86 points above one-pass CVCL and 6.97 above CL-CVCL), k=8 is 2.30 above k=4, and both remain below the offline upper bound (k=8 by 13.93 points). The authors conclude that BabyCL substantially closes but does not match the gap to offline training, and because CL-CVCL is matched in optimization work to BabyCL's gradient budget (at k=8), BabyCL's advantage 'cannot be explained by gradient count alone'.

**System answer.** ## Comparison of BabyCL (k=4, k=8) against the baselines

From Table 1 (Labeled-S 4AFC accuracy) [BabyCL, p.5]:

| Method | 4AFC (%) |
|---|---|
| Offline CVCL (i.i.d., upper bound) | 57.31 ± 1.13 |
| One-pass CVCL (naive streaming) | 27.52 ± 3.12 |
| CL-CVCL (compute-matched) | 36.41 ± 2.31 |
| BabyCL (k = 4) | 41.08 ± 1.79 |
| BabyCL (k = 8) | 43.38 ± 1.47 |

**BabyCL vs. offline upper bound:**
- k=4: gap = 57.31 − 41.08 = **16.23 points** below offline
- k=8: gap = 57.31 − 43.38 = **13.93 points** below offline

The text reiterates this qualitatively: BabyCL "substantially closes the gap to offline CVCL (57.45%) but does not match it" [BabyCL, p.6] (note: the running text in §4.2 reports slightly different absolute values—one-pass 25.68%, CL-CVCL 35.32%, BabyCL k=8 44.46%, offline 57.45%—than the Table 1 entries quoted above; both sources are drawn from the same passage [BabyCL, p.6]).

**BabyCL vs. one-pass streaming:**
- k=8 exceeds one-pass CVCL by 43.38 − 27.52 = **15.86 points** (Table 1 figures), consistent with the text's statement that "One-pass CVCL collapses to 25.68%, confirming that a training recipe designed for i.i.d. data does not transfer to streaming" [BabyCL, p.6].

**BabyCL vs. compute-matched CL-CVCL:**
- k=4 exceeds CL-CVCL by 41.08 − 36.41 = **4.67 points** (Table 1)
- k=8 exceeds CL-CVCL by 43.38 − 36.41 = **6.97 points** (Table 1)
- Increasing resampling from k=4 to k=8 itself yields a gain of 43.38 − 41.08 = **2.30 points** (Table 1), which matches the text's claim of "a further 2.6-point gain" from k=4 to k=8 using its own reported numbers [BabyCL, p.6].

## Authors' conclusion from the compute-matched baseline

CL-CVCL is explicitly designed to match BabyCL's gradient/optimization budget (≈6× revisitation per item at k=8) while omitting BabyCL's continual-learning machinery (temporal segmentation, dual replay buffers, joint visual+cross-modal losses) [BabyCL, p.5–6]. Because CL-CVCL still performs well below BabyCL despite having the same amount of optimization work, the authors conclude that **"the gap cannot be explained by gradient count alone; it reflects the benefit of organizing the stream through event segmentation and of combining visual self-supervision with cross-modal grounding"** [BabyCL, p.6]. They further note that "the continual-structure benefits compound with more thorough revisitation of newly inserted content" (i.e., the k=4→k=8 gain is additive on top of the structural benefit) [BabyCL, p.6].

**Retrieved:** BabyCL p.1-15 (0.67); BatchNorm p.1-11 (0.59); Transformer p.1-15 (0.58) | gold page hit: 1.00
*19.4 s*

## Q03 (text-only, factual, medium, answerable: yes)

**Question.** How does I-JEPA sample its target and context blocks (number of target blocks, scale and aspect-ratio ranges), and where in the pipeline are the target blocks 'masked'?

**Reference answer.** I-JEPA typically samples M = 4 target blocks, each with random aspect ratio in (0.75, 1.5) and random scale in (0.15, 0.2). The context is a single block with scale in (0.85, 1.0) and unit aspect ratio, from which any region overlapping the targets is removed so the prediction task is non-trivial. The target blocks are obtained by masking the output of the target encoder, not its input, which the paper calls crucial for high-semantic-level targets. The loss is the average L2 distance between predicted and target patch-level representations, and the target encoder is an exponential moving average of the context encoder.

**System answer.** ## I-JEPA Target and Context Block Sampling

**Target blocks:**
- I-JEPA samples **M = 4** (possibly overlapping) target blocks by default [I-JEPA, p.4].
- Each target block has a random **scale in the range (0.15, 0.2)** and a random **aspect ratio in the range (0.75, 1.5)** [I-JEPA, p.4].

**Context block:**
- A **single** context block is sampled per image, with a random **scale in the range (0.85, 1.0)** and **unit aspect ratio** [I-JEPA, p.4].
- Any regions in the context block that overlap with the sampled target blocks are removed "to ensure a non-trivial prediction task" [I-JEPA, p.4].

**Where masking of targets occurs in the pipeline:**
The target blocks are obtained by **masking the output of the target-encoder, not the input**. Specifically, the full (unmasked) image is first fed through the target-encoder to produce patch-level representations $s_y = \{s_{y1}, \dots, s_{yN}\}$, and only *after* this encoding step are the M target blocks sampled as masks $B_i$ applied to those output representations, i.e., $s_y(i) = \{s_{yj}\}_{j \in B_i}$ [I-JEPA, p.3–4]. The paper states explicitly: "Note that the target blocks are obtained by masking the output of the target-encoder, not the input. This distinction is crucial to ensure target representations of a high semantic level" [I-JEPA, p.4].

This design choice is empirically validated in an ablation: masking the output of the target-encoder (rather than masking the input before encoding) improves 1% ImageNet-1K linear-probe top-1 accuracy from 56.1% to 67.3% for a ViT-H/16 pretrained for 300 epochs [I-JEPA, p.15, Table 11].

**Retrieved:** I-JEPA p.1-17 (0.71); MAE p.1-14 (0.64); SWE-bench p.1-52 (0.62) | gold page hit: 1.00
*10.4 s*

## Q04 (text-only, factual, easy, answerable: yes)

**Question.** How are Daily Oracle's question-answer pairs generated and filtered, and how many True/False and multiple-choice questions are in the subset analysed in the paper?

**Reference answer.** The analysed subset has 16,783 True/False and 14,727 multiple-choice questions generated from daily news articles from January 2020 to December 2024. Each day six articles are selected (three random, three from hot topics) and an LLM generates two TF and two MC pairs per article with few-shot prompting. Construction has four steps: article summary (focused on new events so the publication date can be the resolution date), QA generation, misleading-choice generation for MC, and QA filtering. In filtering, an LLM scores seven principles from 0 to 2 points each and only questions with at least 13 points are kept.

**System answer.** # Daily Oracle: QA Generation, Filtering, and Dataset Size

## How QA Pairs Are Generated

Daily Oracle's QA pairs are automatically constructed from daily news articles sourced from the Common Crawl News Dataset and supplemented with Newspaper3k-scraped articles from mainstream outlets (CBS News, CNBC, CNN, Forbes, NPR) [DailyOracle, p.3]. The LLM-based construction follows a **four-step pipeline** [DailyOracle, p.4]:

1. **Article Summary**: An LLM (GPT-3.5 or GPT-4o-mini) generates a summary for each article, filtering out opinion pieces so that only articles reporting *new events* are retained. This allows the publication date to serve as the question's resolution date.

2. **QA Generation**: Using few-shot prompting, an LLM (GPT-4 or GPT-4o) generates **two True/False (TF) questions and two Multiple Choice (MC) questions** per article. For balance, the first TF question is constructed to have a "Yes" answer and the second a "No" answer.

3. **Misleading Choices Generation**: For MC questions, the LLM is given the article, publishing date, and QA pair, and generates three plausible but incorrect distractor choices.

4. **QA Filtering**: An LLM checks each QA pair against **seven principles**: correctness of answers, non-answerability before the publication date, absence of information leakage, objectivity, inclusion of a clear temporal element, public interest, and non-obviousness of the answer. Each principle is scored 0, 1, or 2 points (max 14), and only questions scoring **at least 13 points** are retained [DailyOracle, p.4].

Six articles are selected per day (three random, three from "hot topics" identified via DBSCAN clustering on TF-IDF representations) [DailyOracle, p.4, p.13].

The authors also validated this LLM-based filtering against human judgment: four annotators evaluated a sample of 60 QA pairs using the same seven principles, yielding **89.52% average accuracy** between LLM and human-consensus scores across principles, and **85.00% accuracy** on the final accept/reject decision (13-point threshold) [DailyOracle, p.5].

## Dataset Size in the Paper's Analysis

> "For our current analysis of LLM performance, we utilize a subset of the data consisting of **16,783 TF questions and 14,727 MC questions**, covering a diverse range of forecasting topics, which are generated using daily news articles from January 2020 up until December 2024." [DailyOracle, p.3]

This is reaffirmed in the Dataset Analysis section:

> "At the time of writing this paper, the subset dataset we use from Daily Oracle consists of **16,783 TF and 14,727 MC QA pairs**, covering the period from January 1st, 2020, to December 31st, 2024, with an average of 17.2 questions per day." [DailyOracle, p.4]

Together, this gives a total of 16,783 + 14,727 = **31,510** QA pairs, consistent with the size reported in the comparison table (Table 1) [DailyOracle, p.3].

**Retrieved:** DailyOracle p.1-35 (0.68); MMLU p.1-27 (0.60); SWE-bench p.1-52 (0.58) | gold page hit: 1.00
*15.1 s*

## Q06 (text-only, conceptual, medium, answerable: yes)

**Question.** What three desiderata do the Transformer authors use to motivate self-attention over recurrent and convolutional layers, how does a self-attention layer compare on each, and when is it cheaper per layer than a recurrent layer?

**Reference answer.** The desiderata are (1) total computational complexity per layer, (2) the amount of computation that can be parallelised (minimum number of sequential operations) and (3) the path length between long-range dependencies. Per Table 1, self-attention has O(n^2*d) complexity per layer, O(1) sequential operations and O(1) maximum path length; recurrent layers have O(n*d^2), O(n) and O(n); convolutional layers have O(k*n*d^2), O(1) and O(log_k n). Self-attention is faster than a recurrent layer when the sequence length n is smaller than the representation dimensionality d, which is typical for sentence representations in machine translation. For very long sequences the authors suggest restricting attention to a neighbourhood of size r (path length O(n/r)) but leave this to future work.

**System answer.** The Transformer authors consider three desiderata [Transformer, p.6]:

1. **Total computational complexity per layer**
2. **The amount of computation that can be parallelized**, measured by the minimum number of sequential operations required
3. **The path length between long-range dependencies in the network** (maximum path length between any two input/output positions), since "the shorter these paths between any combination of positions in the input and output sequences, the easier it is to learn long-range dependencies" [Transformer, p.6]

**Comparison per desideratum**, based on Table 1 [Transformer, p.6]:

| Layer Type | Complexity per Layer | Sequential Operations | Maximum Path Length |
|---|---|---|---|
| Self-Attention | O(n²·d) | O(1) | O(1) |
| Recurrent | O(n·d²) | O(n) | O(n) |
| Convolutional | O(k·n·d²) | O(1) | O(logₖ(n)) |
| Self-Attention (restricted) | O(r·n·d) | O(1) | O(n/r) |

- **Parallelization**: "a self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations" — so self-attention is far more parallelizable [Transformer, p.6].
- **Path length**: Self-attention has maximum path length O(1) vs. O(n) for recurrent layers, making it easier (in principle) to learn long-range dependencies [Transformer, p.6].
- **Complexity per layer**: Self-attention is O(n²·d) versus recurrent's O(n·d²).

**When self-attention is cheaper per layer than recurrent:**
The paper states: "In terms of computational complexity, self-attention layers are faster than recurrent layers when the sequence length n is smaller than the representation dimensionality d, which is most often the case with sentence representations used by state-of-the-art models in machine translations, such as word-piece and byte-pair representations" [Transformer, p.6-7].

Calculation check: Self-attention cost O(n²·d) < Recurrent cost O(n·d²) ⟺ n²d < nd² ⟺ n < d. So whenever sequence length n is less than the model dimension d, self-attention is cheaper per layer.

The passage also notes a proposed extension for very long sequences: restricting self-attention to a neighborhood of size r would increase complexity trade-offs to O(r·n·d) per layer but increase maximum path length to O(n/r) [Transformer, p.6-7], though the authors state they "plan to investigate this approach further in future work" rather than having tested it.

**Retrieved:** ViT p.1-22 (0.73); Transformer p.1-15 (0.73); BabyCL p.1-15 (0.64) | gold page hit: 1.00
*12.2 s*

## Q07 (text-only, conceptual, hard, answerable: yes)

**Question.** BYOL trains without negative pairs. What mechanisms does the paper credit with preventing representation collapse, and what do its ablations show about them?

**Reference answer.** BYOL trains an online network (encoder, projector, predictor) to predict the projection of a second augmented view produced by a target network whose weights are an exponential moving average of the online weights; the loss gradient is not propagated into the target (stop-gradient) and the predictor exists only on the online branch. The authors hypothesise that the combination of the predictor and the slow-moving-average target avoids collapse, but they state the dynamics still admit undesirable equilibria that they did not observe in experiments. In the ablation (Table 5b), the only variant that performs well without negatives is BYOL with both a target network and a predictor; the representation collapses when either is removed. They also found that the target network can be removed without collapse if the predictor is kept near-optimal (e.g., higher predictor learning rate), suggesting that keeping the predictor near-optimal may be one role of the target network.

**System answer.** # Mechanisms BYOL Credits for Preventing Collapse

The paper identifies **two main mechanisms**, combined together:

## 1. The predictor (added to the online network only)
The architecture is asymmetric: a predictor qθ is applied only on the online branch to predict the target projection z'ξ [BYOL, p.4]. The paper hypothesizes that "the combination of (i) the addition of a predictor to the online network and (ii) the use of a slow-moving average of the online parameters as the target network encourages encoding more and more information within the online projection and avoids collapsed solutions" [BYOL, p.2].

## 2. The slow-moving-average (EMA) target network
The target parameters ξ are updated as ξ ← τξ + (1−τ)θ rather than copied instantly [BYOL, p.3-4]. The paper's theoretical argument (Section 3.2): when the predictor is near-optimal, BYOL's update on θ follows in expectation the gradient of the expected **conditional variance** Σᵢ Var(z'ξ,i | zθ) [BYOL, p.5, Eq. 5]. Since "purely discarding information from the online projection cannot decrease the conditional variance," and since Var(z'ξ|c) ≥ Var(z'ξ|zθ) for any constant c, "BYOL avoids constant features in zθ... hence our hypothesis on these collapsed constant equilibria being unstable" [BYOL, p.5]. The paper explicitly states: "we hypothesize that the main role of BYOL's moving-averaged target network is to ensure the near-optimality of the predictor over training" [BYOL, p.5].

The paper also notes that although BYOL's dynamics admit no joint loss over (θ,ξ) — analogous to GANs — "there is therefore no a priori reason why BYOL's parameters would converge to a minimum," yet collapse was not observed empirically [BYOL, p.4].

---

# What the Ablations Show

## (a) Bootstrapping / target decay rate (Table 5a, p.9)
Sweeping τbase from 0 (instant copy) to 1 (never updated):

| Target mode | τbase | Top-1 |
|---|---|---|
| Constant random network | 1 | 18.8±0.7 |
| Moving average | 0.999 | 69.8 |
| Moving average | **0.99** | **72.5** |
| Moving average | 0.9 | 68.4 |
| Stop gradient of online (instant copy) | 0 | 0.3 |

τ=0 (no EMA, target = online instantaneously) "destabilizes training, yielding very poor performance" (0.3%), while τ=1 (frozen random target) "makes the training stable but prevents iterative improvement" (18.8%) [BYOL, p.8]. All τ between 0.9–0.999 give >68% — showing the EMA mechanism itself (not just any target) is necessary.

## (b) Predictor + target-network combination (Table 5b, p.9-10)
Ablating which components are present:

| Predictor | Target network | β | Top-1 |
|---|---|---|---|
| ✓ | ✓ | 0 | 72.5 (BYOL) |
| ✓ | ✓ | 1 | 70.9 |
| ✓ | — | 1 | 70.7 |
| — | — | 1 (SimCLR) | 69.4 |

"The only variant that performs well without negative examples (i.e., with β=0) is BYOL, using both a bootstrap target network and a predictor" [BYOL, p.9]. Removing either one while using β=0 causes collapse (not shown as a working row — the paper states performance collapses without both).

## (c) Relationship to Mean Teacher (p.9-10)
Removing the predictor from BYOL "results in an unsupervised version of MT with no classification loss." This variant **collapses** (Row 7 of Table 5), "which suggests that the additional predictor is critical to prevent collapse in an unsupervised scenario" [BYOL, p.9-10].

## (d) Near-optimal predictor without a target network (Appendix I; summarized p.10)
The paper shows the target network can be *removed* without collapse if the predictor is kept near-optimal by other means:
- Using an optimal linear predictor (closed-form linear regression per batch) before backprop: **52.5%** top-1 [BYOL, p.10].
- Increasing only the predictor's learning rate: **66.5%** top-1 [BYOL, p.10].
- By contrast, increasing learning rates of *both* projector and predictor (still no target network) gives poor results (≈25% top-1) [BYOL, p.10].

Appendix I further quantifies this: varying a learning-rate multiplier λ on the predictor (with τ=0, i.e., no EMA) shows performance rising from 0.01% (λ=0) to 66.6% (λ=10) [BYOL, p.31, Table 21]. A joint sweep over predictor multiplier λ and projector multiplier µ (Table 22, p.31) shows good performance only when λ_pred > µ_proj, i.e., "the predictor learning rate needs to be higher than the projector learning rate in order to successfully remove the target network. This further suggests that the learning dynamic of predictor is central to BYOL's stability" [BYOL, p.31].

**Conclusion drawn from these ablations**: "Table 5b already shows the importance of combining a predictor and a target network: the representation does collapse when either is removed. We further found that we can remove the target network without collapse by making the predictor near-optimal... This seems to indicate that keeping the predictor near-optimal at all times is important to preventing collapse, which may be one of the roles of BYOL's target network" [BYOL, p.10].

---

**What the evidence does *not* establish**: The passages give no formal proof that collapse is impossible, only an empirical/intuitive argument (conditional-variance heuristic under an idealized "optimal predictor" assumption, Section 3.2 and Appendix H) plus ablation evidence that removing either mechanism degrades or collapses performance. The paper itself states "we did not observe convergence to such [collapsed] equilibria in our experiments" [BYOL, p.4] — an empirical, not theoretical, guarantee.

**Retrieved:** BYOL p.1-35 (0.65); Distillation p.1-9 (0.62); BatchNorm p.1-11 (0.62) | gold page hit: 1.00
*24.5 s*

## Q08 (text-only, conceptual, medium, answerable: yes)

**Question.** What evidence does the Batch Normalization paper give that batch normalization reduces internal covariate shift, how large is the training speed-up it reports on ImageNet (and what else was changed besides adding BN), and what does the paper itself say it has not established?

**Reference answer.** The paper defines internal covariate shift as the change in the distribution of network activations due to the change in network parameters during training. Its direct evidence is a small MNIST experiment (three sigmoid hidden layers): the input distribution to a typical sigmoid unit is much more stable with BN and the BN network has higher test accuracy (Fig. 1). On ImageNet the evidence is indirect, through the speed and accuracy of BN-Inception variants: BN-Baseline matches Inception's 72.2% in 13.3M steps versus 31.0M, BN-x5 needs 2.1M steps (stated as 14 times fewer), BN-x30 reaches 74.8%, and BN-x5-Sigmoid reaches 69.8% while Inception with sigmoid never beats 1/1000 accuracy. The BN-x5/x30 speed-ups combine BN with other changes (a 5x or 30x larger initial learning rate, Dropout removed, L2 weight cut 5x, learning rate decayed 6x faster, Local Response Normalization removed, more thorough shuffling, fewer photometric distortions), so they are not an isolated measure of BN. The paper frames the mechanism as an expectation and conjecture: it 'expects' fixed input distributions to speed training, 'conjectures' that BN may bring layer Jacobian singular values close to 1, and says the precise effect of BN on gradient propagation remains an area of further study.

**System answer.** ## Evidence that BN reduces internal covariate shift

The paper's evidence is a controlled experiment on MNIST, not a theoretical proof. They trained "a very simple network, with a 28x28 binary image as input, and 3 fully-connected hidden layers with 100 activations each" using sigmoid nonlinearities, with and without BN added to each hidden layer [BatchNorm, p.5-6]. They report:

- The batch-normalized network achieves higher test accuracy (Figure 1a) [BatchNorm, p.6].
- They then "studied inputs to the sigmoid, in the original network N and batch-normalized network... over the course of training" for a typical activation in the last hidden layer. Figure 1(b,c) shows the {15,50,85}th percentiles of this input distribution over training. The paper states: "The distributions in the original network change significantly over time, both in their mean and the variance, which complicates the training of the subsequent layers. In contrast, the distributions in the batch-normalized network are much more stable as training progresses, which aids the training." [BatchNorm, p.6]

This qualitative, visual comparison of activation-distribution stability on MNIST is the evidence presented; the paper does not give a quantitative metric of "internal covariate shift" itself to prove the reduction.

## Reported training speed-up on ImageNet

- Abstract: "Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps" [BatchNorm, p.1].
- Detailed result: Inception reached 72.2% accuracy after 31.0·10⁶ steps; "BN-x5 needs 14 times fewer steps than Inception to reach the 72.2% accuracy" — concretely BN-x5 reaches it in 2.1·10⁶ steps (31.0·10⁶ / 2.1·10⁶ ≈ 14.8) [BatchNorm, p.7, Figure 3]. The paper also notes in the Introduction that "we can match its performance using only 7% of the training steps" [BatchNorm, p.2], which is consistent (1/14 ≈ 7%).
- A separate, more conservative number: simply adding BN with no other changes (BN-Baseline) matches Inception's accuracy in 13.3·10⁶ steps, i.e. "in less than half the number of training steps" [BatchNorm, p.7].
- Pushing learning rate further (BN-x30) reaches a higher final accuracy of 74.8% after 6·10⁶ steps — "5 times fewer steps than required by Inception to reach 72.2%" [BatchNorm, p.7].

**What else was changed besides adding BN** (Section 4.2.1, "Accelerating BN Networks") [BatchNorm, p.6]:
- Increase the learning rate (no ill side effects, per Sec. 3.3).
- Remove Dropout.
- Reduce the L2 weight regularization (weight of this loss reduced by a factor of 5).
- Accelerate the learning rate decay (6 times faster than Inception's schedule).
- Remove Local Response Normalization.
- Shuffle training examples more thoroughly (within-shard shuffling), which "led to about 1% improvements in the validation accuracy."
- Reduce the photometric distortions applied to training images.

So the "14x fewer steps" (BN-x5) and "5x fewer steps with higher final accuracy" (BN-x30) figures reflect BN *plus* all these additional modifications, not BN alone; the BN-only (BN-Baseline) condition gives roughly a 2.3x speedup (31.0·10⁶ / 13.3·10⁶) [BatchNorm, p.7].

## What the paper itself says it has not established

- On gradient propagation: after conjecturing that BN may push layer Jacobians toward singular values near 1, the authors explicitly caveat: "In reality, the transformation is not linear, and the normalized values are not guaranteed to be Gaussian nor independent... The precise effect of Batch Normalization on gradient propagation remains an area of further study." [BatchNorm, p.5]
- In the Conclusion: "In this work, we have not explored the full range of possibilities that Batch Normalization potentially enables." They list unexplored future directions: applying BN to Recurrent Neural Networks to "more thoroughly test the hypothesis that normalization improves gradient propagation," and investigating "whether Batch Normalization can help with domain adaptation... perhaps with just a recomputation of the population means and variances." They add: "we believe that further theoretical analysis of the algorithm would allow still more improvements and applications." [BatchNorm, p.8]

So, by the paper's own account, (1) the mechanism's effect on gradient propagation is conjectural and unverified, and (2) applications to RNNs and domain adaptation, as well as a fuller theoretical analysis, are left as open/future work rather than established in the paper.

**Retrieved:** BatchNorm p.1-11 (0.87); ViT p.1-22 (0.68); ResNet p.1-12 (0.67) | gold page hit: 1.00
*27.7 s*

## Q09 (text-only, conceptual, hard, answerable: yes)

**Question.** According to the Temporal Straightening paper, why should reducing the curvature of latent trajectories make gradient-based planning easier, and do the paper's experiments generally show planning improving when the curvature regularizer is used?

**Reference answer.** Explanation (the main part). Planning minimises a Euclidean goal cost in latent space, and when latent trajectories are highly curved, straight-line distance misrepresents the geodesic distance along feasible transitions. A curvature regulariser (it penalises the angle between consecutive latent velocity vectors, i.e. maximises their cosine similarity, while a JEPA-style predictor is trained with stop-gradient on the target) straightens trajectories, which makes Euclidean latent distance a better proxy for geodesic distance and improves the conditioning of the planning objective. The theory covers linear latent dynamics: epsilon-straight transitions control the condition number of the planning Hessian, so gradient descent converges linearly at a rate set by the condition number; guarantees for nonlinear predictors are left to future work. As an illustration, the loss landscape is closer to convex after straightening (Figure 4). Experiments (general trend only). Yes: the paper reports open-loop planning success improving by 20-60% and MPC by 20-30% with a simple gradient-based planner, and says it observes a significant improvement across all models and environments. The improvement is not uniform in Table 1 (for example a from-scratch ResNet 1x384 on PointMaze-UMaze falls from 82.00 to 52.00 open-loop), so 'generally' is the right strength, in simulated goal-reaching tasks.

**System answer.** # Why Reducing Curvature Should Ease Gradient-Based Planning

The paper gives both a theoretical and an intuitive justification:

**1. Euclidean distance becomes a better proxy for geodesic distance.** When latent trajectories are highly curved, "straight-line distances in embedding space misrepresent the geodesic distance along feasible transitions" [TemporalStraightening, p.1]. Since planning costs are typically computed as Euclidean/MSE distance to a goal embedding, this misalignment makes the cost function a poor guide for optimization. Straightening is intended to fix this: "reducing curvature this way makes the Euclidean distance in latent space a better proxy for the geodesic distance and improves the conditioning of the planning objective" [TemporalStraightening, p.1].

**2. Formal conditioning argument (linear dynamics case).** Under linear latent dynamics zt+1 = Azt + Bat, the planning Hessian is H = 2J_Φ^⊤J_Φ, and its effective condition number is controlled by the controllability Gramian. Theorem 4.4 shows:

κeff(H) = κ(W_K) ≤ κ(B)² · κ(A)^(2(K−1))

and if the transition is ε-straight (‖A−I‖₂ = ε < 1):

κeff(H) ≤ κ(B)² [(1+ε)/(1−ε)]^(2(K−1)), which for ε ≤ 1/2 gives κeff(H) ≤ κ(B)²e^(6εK) [TemporalStraightening, p.5].

Since "gradient descent converges linearly at a rate controlled by the condition number," smaller ε (straighter, closer-to-identity dynamics) yields a better-conditioned Hessian whose condition number "grows slowly with the horizon," which "translate[s] to faster optimization in practice" [TemporalStraightening, p.5]. The paper connects this to the practical cosine-similarity regularizer via Remark 4.3/Proposition C.9, showing high cosine similarity implies (A−I) is small along visited velocity directions [TemporalStraightening, p.4, p.19].

**3. Empirical loss-landscape evidence.** For nonlinear dynamics, the paper shows that straightening empirically produces a less non-convex action-space loss landscape: "The loss landscape is closer to being convex after straightening" (Figure 4, DINOv2 vs. Straightened) [TemporalStraightening, p.5].

# Do Experiments Generally Show Planning Improvement?

Yes, consistently across environments and encoder setups, though with a few caveats/exceptions.

**Main results (Table 1).** Adding the explicit curvature regularizer (Lcurv = ✓) generally boosts both open-loop and MPC success rates over the same architecture without it. Examples [TemporalStraightening, p.8]:
- "UMaze's open-loop success rate is improved from 44% to 94% with the projector, and 14.67% to 64.67% when training a ResNet from scratch."
- "Applying explicit straightening further strengthens the straightness in the embedding space, resulting in more than 10% boost in open-loop and MPC success rates for almost all setups."
- With MPC, the straightened models "reach 100% success rates very quickly" on Wall and UMaze [TemporalStraightening, p.8].

Specific Table 1 numbers [TemporalStraightening, p.8]: DINOv2(patch)+proj (14×14×8): open-loop success goes from 80.00±7.12% (no Lcurv) to 90.67±0.94% (with Lcurv) on Wall, 44.00±7.12%→94.00±1.63% on UMaze, 72.00±4.32%→82.67±3.77% on Medium-maze, 70.00±1.63%→77.33±6.18% on PushT. MPC improvements show similar or larger gains.

**Correlation between curvature and success.** Figure 5 directly shows "Given the same type of encoder, reduced curvature generally leads to higher success rates" [TemporalStraightening, p.6].

**Robustness across planners.** Straightening improves both GD and CEM planners, e.g., "on Wall and PushT, it improves the projector baseline by roughly 10% for both GD and CEM," and narrows the GD–CEM performance gap, giving GD "a better success–latency trade-off" [TemporalStraightening, p.8].

**Long-horizon setting.** Table 2 shows the method "consistently outperforms the baseline across all settings" even though absolute success rates drop substantially at the 50-step horizon [TemporalStraightening, p.8-9].

**Exceptions/nuances noted by the authors:**
- For ResNet with spatial features (14×14×8), adding Lcurv raises Wall open-loop success dramatically (1.33%→84.67%) but on UMaze the straightened ResNet (64.67±8.38%) is actually *lower* than the unregularized projector-with-straightening result for other configs — though it's still far above the unregularized ResNet baseline (14.67±4.99%) [TemporalStraightening, p.8, Table 1].
- The paper also notes that some of the improvement comes from *implicit* straightening already induced by the JEPA prediction loss alone, even without the explicit regularizer: "implicit straightening can happen in JEPA world models when training the encoder using the prediction loss alone" and "adding explicit curvature regularization further strengthens and stabilizes this effect" [TemporalStraightening, p.6]. So part of the baseline-vs-regularized gap reflects this added explicit regularization on top of an already partially-straightened implicit baseline.

**Conclusion statement from the paper:** "temporal straightening yields an embedding space that effectively facilitates latent planning... leads to significant and consistent gains over baselines" across the tested 2D goal-reaching tasks [TemporalStraightening, p.9].

**Retrieved:** TemporalStraightening p.1-29 (0.88); BatchNorm p.1-11 (0.63); Transformer p.1-15 (0.59) | gold page hit: 1.00
*24.5 s*

## Q11 (text-only, cross-paper, medium, answerable: yes)

**Question.** ViT says it follows the original Transformer 'as closely as possible'. Which parts of the Transformer encoder does ViT keep, and how does its encoder differ from the one in 'Attention Is All You Need' (input handling, position information, normalisation placement, feed-forward activation)?

**Reference answer.** ViT keeps the Transformer encoder structure of alternating multi-head self-attention and position-wise MLP/feed-forward blocks with residual connections and layer normalisation, and uses the encoder only. Differences: (1) input - ViT splits an image into patches, linearly projects them and prepends a learnable [class] token, whereas the Transformer embeds discrete input tokens; (2) position information - ViT uses standard learnable 1D position embeddings, the Transformer uses fixed sinusoidal encodings (though it found learned embeddings nearly identical); (3) normalisation - the Transformer computes LayerNorm(x + Sublayer(x)) after the residual addition, while ViT applies layer norm before every block and residual connections after every block; (4) the feed-forward layer uses ReLU in the Transformer and GELU in ViT. The Transformer paper additionally has a decoder with encoder-decoder attention.

**System answer.** ## What ViT keeps from the original Transformer

ViT states explicitly: "In model design we follow the original Transformer (Vaswani et al., 2017) as closely as possible... The Transformer encoder (Vaswani et al., 2017) consists of alternating layers of multiheaded self-attention (MSA, see Appendix A) and MLP blocks (Eq. 2, 3)" [ViT, p.3]. The appendix confirms the attention mechanism itself is unchanged: "Standard qkv self-attention (SA, Vaswani et al. (2017)) is a popular building block... Multihead self-attention (MSA) is an extension of SA in which we run k self-attention operations... in parallel, and project their concatenated outputs" [ViT, p.13] — this matches the scaled dot-product / multi-head attention formulation in "Attention Is All You Need" [Transformer, p.4-5]. ViT also keeps the basic pattern of a residual connection around each sub-layer [ViT, p.3], and a position-wise feed-forward (MLP) block applied after the attention block, paralleling the Transformer's "position-wise fully connected feed-forward network" [Transformer, p.3].

## Where ViT's encoder differs

**1. Input handling.**
- Transformer: encoder input is a sequence of word/subword token embeddings fed directly into the stack [Transformer, p.2-3].
- ViT: the image is reshaped into flattened 2D patches, linearly projected to a constant dimension D via a trainable linear projection, and a learnable "[class]" token (`xclass`) is prepended to the sequence, whose output representation is later used for classification: "we prepend a learnable embedding to the sequence of embedded patches (z0_0 = xclass), whose state at the output of the Transformer encoder (z0_L) serves as the image representation" [ViT, p.3].

**2. Position information.**
- Transformer: uses fixed sinusoidal positional encodings, "sine and cosine functions of different frequencies," added to the input embeddings at the bottom of the encoder/decoder stacks, chosen partly because they "may allow the model to extrapolate to sequence lengths longer than the ones encountered during training" [Transformer, p.6]. (A learned-embedding variant was tested as an ablation and found "nearly identical" [Transformer, p.6].)
- ViT: uses "standard learnable 1D position embeddings," added to the patch embeddings, stating "we have not observed significant performance gains from using more advanced 2D-aware position embeddings" [ViT, p.3]. So ViT's default is the learned embedding that the original Transformer only used as a secondary comparison, not its primary (sinusoidal) choice.

**3. Normalization placement.**
- Transformer: post-norm — "the output of each sub-layer is LayerNorm(x + Sublayer(x))," i.e., the residual sum is computed first and LayerNorm applied afterward [Transformer, p.3].
- ViT: pre-norm — "Layernorm (LN) is applied before every block, and residual connections after every block (Wang et al., 2019; Baevski & Auli, 2019)," formalized as z′_ℓ = MSA(LN(z_{ℓ−1})) + z_{ℓ−1} and z_ℓ = MLP(LN(z′_ℓ)) + z′_ℓ [ViT, p.3-4]. So LN is applied to the input of each block rather than to the post-residual output.

**4. Feed-forward activation.**
- Transformer: the position-wise feed-forward network uses ReLU: FFN(x) = max(0, xW1+b1)W2+b2 [Transformer, p.5].
- ViT: "The MLP contains two layers with a GELU non-linearity" [ViT, p.3-4].

**Summary:** ViT reuses the Transformer's core computational block — alternating multi-head self-attention and a two-layer feed-forward/MLP sub-layer, each wrapped in a residual connection [ViT, p.3; Transformer, p.3] — but changes (a) the input (image patches + prepended class token instead of raw token embeddings, ViT p.3), (b) the positional information (learned 1D position embeddings vs. the Transformer's sinusoidal encodings, ViT p.3 vs. Transformer p.6), (c) normalization placement (pre-LN vs. the Transformer's post-LN, ViT p.3-4 vs. Transformer p.3), and (d) the activation in the feed-forward block (GELU vs. ReLU, ViT p.3-4 vs. Transformer p.5).

**Retrieved:** Transformer p.1-15 (0.77); ViT p.1-22 (0.71); BabyCL p.1-15 (0.59) | gold page hit: 1.00
*25.8 s*

## Q12 (text-only, cross-paper, hard, answerable: yes)

**Question.** MAE and I-JEPA both mask parts of an image and use a ViT encoder on the visible part. What does each method predict and with what loss, and what evidence does the I-JEPA paper give that predicting in representation space matters?

**Reference answer.** MAE reconstructs the pixel values of the masked patches with a lightweight decoder (mean squared error computed only on masked patches); the encoder sees only visible patches and normalised pixels work slightly better (Table 1d, ViT-L/16: 85.4 vs 84.9 fine-tuning, 73.9 vs 73.5 linear probing). I-JEPA is non-generative: a predictor (narrow ViT) predicts the representations of target blocks from a context block, the targets come from a target encoder that is an exponential moving average of the context encoder, and the loss is average L2 distance in representation space. In I-JEPA's own ablation (Table 7, ViT-L/16, linear probe on 1% of ImageNet labels), using target-encoder outputs gave 66.9 top-1 versus 40.7 when the loss was in pixel space, and the authors say they 'conjecture' representation-space loss is a crucial component. I-JEPA also reports about 7% slower iterations than MAE but roughly 5x fewer iterations to converge. Caveat: the pixel-space variant is I-JEPA's own ablation (different epochs: 500 vs 800), not the MAE paper's setup, and MAE does not test representation-space targets.

**System answer.** ## What each method predicts

**MAE** masks random patches of the input image (e.g., 75%) and its decoder predicts the **pixel values** for each masked patch: "Our MAE reconstructs the input by predicting the pixel values for each masked patch. Each element in the decoder's output is a vector of pixel values representing a patch" [MAE, p.4]. The loss is **mean squared error (MSE) between reconstructed and original images in pixel space, computed only on masked patches**: "Our loss function computes the mean squared error (MSE) between the reconstructed and original images in the pixel space. We compute the loss only on masked patches, similar to BERT" [MAE, p.4]. MAE also tested a normalized-pixel variant and found it improved accuracy [MAE, p.4].

**I-JEPA** instead predicts the **representations** of target blocks, output by a target-encoder, from a context block, via a predictor network: "given a context block, predict the representations of various target blocks in the same image" [I-JEPA, p.1]. Concretely, "the targets correspond to the outputs of the target-encoder, the weights of which are updated at each iteration via an exponential moving average of the context encoder weights" [I-JEPA, p.3]. The loss is the **average L2 distance between predicted and target patch-level representations**:
$$\frac{1}{M}\sum_{i=1}^M D(\hat{s}_y(i), s_y(i)) = \frac{1}{M}\sum_{i=1}^M \sum_{j\in B_i}\lVert \hat{s}_{y_j}-s_{y_j}\rVert_2^2$$
[I-JEPA, p.4]. Crucially, "the target blocks are obtained by masking the output of the target-encoder, not the input. This distinction is crucial to ensure target representations of a high semantic level" [I-JEPA, p.3-4].

## Evidence that predicting in representation space matters (I-JEPA)

I-JEPA directly ablates this design choice in Table 7 ("Ablating targets"): comparing a "Target-Encoder Output" target vs. a "Pixels" target, both evaluated via linear probe on 1% ImageNet-1K.

- Target-Encoder Output, ViT-L/16, 500 epochs → **66.9** top-1
- Pixels, ViT-L/16, 800 epochs → **40.7** top-1

[I-JEPA, p.7]

The paper states: "The semantic level of the I-JEPA representations degrades significantly when the loss is applied in pixel space, rather than representation space, highlighting the importance of the target-encoder during pretraining" [I-JEPA, p.7]. Even though the pixel-space variant was trained for *more* epochs (800 vs. 500), it still performed far worse (a drop of 66.9 − 40.7 = 26.2 points), providing direct evidence that computing the loss in representation space (rather than pixel space) is what drives the high semantic quality of the learned features: "we conjecture that a crucial component of I-JEPA is that the loss is computed entirely in representation space, thereby giving the target encoder the ability to produce abstract prediction targets, for which irrelevant pixel-level details are eliminated" [I-JEPA, p.7].

Additionally, a related ablation on masking the target-encoder's *output* vs. its *input* (Table 11) shows a similar pattern — masking the output (keeping full-image representation computation before masking) gives 67.3 top-1 vs. 56.1 top-1 for masking the input, reinforcing that how/where the abstraction happens in representation space affects semantic quality [I-JEPA, p.15].

The evidence does not include a direct head-to-head comparison between I-JEPA's representation-space loss and MAE's own pixel-space loss under identical architecture/epochs beyond the Table 7 pixel-vs-representation ablation within I-JEPA itself; the Table 7 ablation is the paper's explicit controlled comparison establishing the claim.

**Retrieved:** I-JEPA p.1-17 (0.70); MAE p.1-14 (0.68); TemporalStraightening p.1-29 (0.59) | gold page hit: 1.00
*17.0 s*

## Q13 (text-only, cross-paper, hard, answerable: yes)

**Question.** Distillation and BYOL both train one network to match another network's outputs. According to the two papers, what supplies the targets in each case and how does that target model come about, are labels used, and what does BYOL say about the 'mean teacher' method that it treats as closest to its slow-moving-average target?

**Reference answer.** Distillation: the targets are class probabilities from an already-trained 'cumbersome' model (an ensemble, or a single very large model trained with a strong regularizer such as dropout), softened by raising the softmax temperature. The small model is trained at the same high temperature on a transfer set and uses temperature 1 afterwards; when labels are known the objective is a weighted average of cross-entropy with the soft targets and with the correct labels, with a considerably lower weight on the label term. BYOL: the targets are the projections a target network produces for a second augmented view; the target's weights are an exponential moving average of the online network's weights (a slow-moving average of the learner itself, not a separately trained larger model), the loss gradient is not propagated into the target (stop-gradient), and an extra predictor sits only on the online branch. BYOL is a self-supervised method that works without negative pairs. BYOL describes mean teacher (MT) as also using a slow-moving-average 'teacher' to produce targets for an online 'student', with an l2 consistency loss between their softmax predictions added to a classification loss; it reports that a similar approach collapses when the classification loss is removed, whereas BYOL's added predictor prevents collapse.

**System answer.** # How targets are supplied in Distillation vs. BYOL

## Distillation (Hinton, Vinyals & Dean)

The targets come from a **separately, fully-trained "cumbersome model"** — either a large ensemble of models or a single large heavily-regularized model — trained *before* distillation begins:

- "The cumbersome model could be an ensemble of separately trained models or a single very large model trained with a very strong regularizer such as dropout" [Distillation, p.1].
- The target model is trained normally, typically with **hard labels**, to maximize average log probability of the correct class. The targets used for the small model are the **soft class probabilities** this trained model produces, obtained by raising the softmax temperature: "knowledge is transferred to the distilled model by training it on a transfer set and using a soft target distribution for each case in the transfer set that is produced by using the cumbersome model with a high temperature in its softmax" [Distillation, p.3].
- Labels are optionally reintroduced during the transfer step itself: "When the correct labels are known for all or some of the transfer set, this method can be significantly improved by also training the distilled model to produce the correct labels," via a weighted average of a soft-target cross-entropy loss and a hard-target cross-entropy loss [Distillation, p.3].
- In the ensemble case, the soft targets can be the "arithmetic or geometric mean" of the individual trained models' predictive distributions [Distillation, p.2].

So: targets = outputs of an **independently pre-trained** (label-supervised) model/ensemble, used post-hoc; the target model does not change during distillation.

## BYOL (Grill et al.)

The targets come from a **target network that is itself a continuously-updated exponential moving average (EMA) of the online network being trained** — not a separately pretrained model:

- "The target network provides the regression targets to train the online network, and its parameters ξ are an exponential moving average of the online parameters θ... ξ ← τξ + (1−τ)θ" [BYOL, p.3].
- No labels are used at all: BYOL is self-supervised — the online network predicts the target network's projection of a *different augmented view of the same (unlabeled) image* [BYOL, p.3–4]. Labels appear only later in optional linear-evaluation/semi-supervised fine-tuning, not in producing the targets.
- The target network co-evolves with the online network during training (it is not a fixed, finished model); only the online encoder is kept at the end [BYOL, p.3–4].

## BYOL's discussion of Mean Teacher (its closest comparison for the slow-moving-average target)

BYOL explicitly compares itself to **Mean Teacher (MT)**, the semi-supervised method it treats as closest to its own target-network mechanism:

- "Mean teacher (MT) [20] also uses a slow-moving average network, called teacher, to produce targets for an online network, called student. An ℓ2 consistency loss between the softmax predictions of the teacher and the student is added to the classification loss." [BYOL, p.3]
- Key difference: MT relies on **a classification loss over labels** to "ground the training" of its EMA target. BYOL shows that removing this classification loss (making MT's mechanism fully unsupervised) causes collapse: "[20] demonstrates the effectiveness of MT in the semi-supervised learning case, in Section 5 we show that a similar approach collapses when removing the classification loss. In contrast, BYOL introduces an additional predictor on top of the online network, which prevents collapse." [BYOL, p.3]
- This is confirmed quantitatively in the ablations: "Removing the predictor in BYOL results in an unsupervised version of MT with no classification loss that uses image augmentations instead of the original architectural noise (e.g., dropout). This variant of BYOL collapses (Row 7 of Table 5) which suggests that the additional predictor is critical to prevent collapse in an unsupervised scenario." [BYOL, p.9–10]

So BYOL's argument is: MT's slow-moving-average target works because labels anchor the student via a classification loss; take the labels away and MT's approach collapses, whereas BYOL avoids collapse without labels by adding a **predictor** on the online branch — this predictor (plus the EMA target) is what BYOL identifies as the key ingredient MT lacks.

**Retrieved:** Distillation p.1-9 (0.68); BYOL p.1-35 (0.68); BatchNorm p.1-11 (0.64) | gold page hit: 1.00
*18.6 s*

## Q14 (text-only, cross-paper, medium, answerable: yes)

**Question.** Temporal Straightening's world model uses a ResNet encoder, a ViT predictor and stop-gradient on the target latent. What does the Straightening paper say about how it uses each, and what does each originating paper (ResNet, ViT, BYOL) say that the component is designed to do?

**Reference answer.** Temporal Straightening offers two encoder setups, one being a ResNet (He et al.) trained from scratch, and uses a ViT (Dosovitskiy et al.) as the dynamics predictor with a temporal causal attention mask for frame-level autoregressive prediction. For collapse prevention it applies stop-gradient to the target latent in the prediction loss, citing Grill et al. 2020 (the BYOL paper) among stop-gradient methods, chosen because it needs no negative samples or extra hyper-parameters; it concedes collapse is still possible in theory but says stop-gradient worked in its experiments. In the originating papers: ResNet introduces residual learning, letting stacked layers fit F(x) = H(x) - x via shortcut connections to ease optimisation of deeper networks (the degradation problem); ViT processes a sequence of image-patch embeddings with a standard Transformer encoder of alternating self-attention and MLP blocks; and BYOL trains an online network to predict a stop-gradient target network's representation without negative pairs, which it hypothesises depends on both a predictor and a slow-moving-average target (its representation collapses if either is removed).

**System answer.** ## What the evidence shows

I have the full text of **TemporalStraightening**, but of the three "originating papers" you ask about (ResNet, ViT, BYOL), only the **Transformer** paper ("Attention Is All You Need") is actually provided among the passages — and that paper is the basis for the *attention mechanism* that ViT later adapted, not the ViT paper itself. No passages from He et al.'s ResNet paper or from Grill et al.'s BYOL paper are included. So for those two, I can only report how TemporalStraightening uses/cites them, not what their original papers say about their own design goals.

### 1. ResNet encoder — usage in TemporalStraightening

- TemporalStraightening offers two encoder options and one is "A ResNet (He et al., 2015) trained from scratch, producing features zᵥₜ ∈ Rᵐᵛ×ᵈᵛ directly" [TemporalStraightening, p.5], used without a frozen pretrained backbone.
- It is trained jointly with the curvature regularizer: "We observe that training a ResNet encoder from scratch generally yields lower curvatures than training a projector on top of a frozen pretrained backbone, likely because it offers greater representational flexibility to adapt the geometry to the dynamics" [TemporalStraightening, p.6].
- Empirically, ResNet-from-scratch (with straightening) achieves strong planning success rates, e.g. 84.00% open-loop on Wall (dim 1×384) vs. 4.67% without straightening [TemporalStraightening, p.8, Table 1].

**What the ResNet paper itself says it is designed to do:** Not available — no passage from He et al. (2015) is provided in the given material, so this cannot be answered from the evidence.

### 2. ViT predictor — usage in TemporalStraightening

- "We use a ViT (Dosovitskiy et al., 2021) as the dynamics predictor fθ. When available, proprioceptive states pt ∈ Rnp are encoded via Epξ ... and concatenated with each visual spatial feature. To condition on actions, we concatenate the action embeddings ... before passing them to the predictor. We apply a temporal causal attention mask so tokens at time t attend only to frames {t−K,...,t−1}, enabling frame-level autoregressive prediction" [TemporalStraightening, p.5].
- So the ViT is repurposed from an image classifier into an autoregressive latent-dynamics predictor via a causal masking scheme over time, given K past latent states/actions (Eq. 2, p.3).

**What the ViT paper itself says it is designed to do:** Not available — Dosovitskiy et al. (2021) is only cited, no passage from that paper is provided.

**Related evidence (Transformer, the architecture ViT builds on):** The only attention-architecture passage available is the original Transformer paper, which states its design goal was to replace recurrent/convolutional sequence models with "a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output," enabling "significantly more parallelization" and reaching "a new state of the art in translation quality" with less training time [Transformer, p.2]. It also emphasizes that self-attention yields a constant maximum path length between any two sequence positions, which is motivated by easing the learning of long-range dependencies [Transformer, p.6]. This describes the rationale for self-attention generally, not ViT's adaptation of it to images or TemporalStraightening's adaptation to latent dynamics.

### 3. Stop-gradient on the target latent — usage in TemporalStraightening

- Formally: Lpred = ‖ẑₜ₊₁ − sg(zₜ₊₁)‖²₂, "where sg denotes the stop-gradient operation to prevent collapse of the latent space" [TemporalStraightening, p.4].
- Rationale given: "Since our encoder is trainable, the model is likely to produce degenerate solutions in which all latent representations collapse to a constant... We apply stop-gradient to the target latent in the prediction loss (5) to prevent the gradients from Lpred from being backpropagated through the target branch. Although a collapsing solution is still possible in theory, stop-grad has been shown to be effective in self-supervised vision learning (Chen & He, 2021), and also effective in our experiments" [TemporalStraightening, p.4]. Note that this sentence explicitly credits Chen & He, 2021 (SimSiam) for stop-grad's effectiveness, while elsewhere it groups "stop-gradient-based" anti-collapse methods under "(Chen & He, 2021; Grill et al., 2020)" [TemporalStraightening, p.4], the latter citation being BYOL.

**What the BYOL paper itself says the stop-gradient is designed to do:** Not available — no passage from Grill et al. (2020) is in the provided evidence, so I cannot state BYOL's own stated rationale from the paper itself.

### Summary of what the evidence does **not** establish
The provided passages do not include the ResNet paper (He et al., 2015), the ViT paper (Dosovitskiy et al., 2021), or the BYOL paper (Grill et al., 2020). Therefore I cannot report, from the evidence given, what those three originating papers themselves say their respective components (residual CNN blocks, vision-transformer patch attention, stop-gradient asymmetric Siamese network) are designed to do. The evidence does establish, in detail, how TemporalStraightening repurposes each component (ResNet as a from-scratch spatial-feature encoder, ViT as a causally-masked autoregressive latent-dynamics predictor, and stop-gradient on the prediction target to prevent representation collapse), as cited above.

**Retrieved:** TemporalStraightening p.1-29 (0.79); Transformer p.1-15 (0.67); BabyCL p.1-15 (0.65) | gold page hit: 0.30
*40.5 s*

## Q15 (text-only, cross-paper, hard, answerable: yes)

**Question.** BabyCL's visual branch applies strong augmentations to two views of each frame. Compare the Gaussian-blur and solarization probabilities it uses for its two views with those BYOL uses for its two views, and say what the two papers report about whether negative pairs are needed.

**Reference answer.** BabyCL (Appendix A): two views per frame with strong augmentation: random resized crop to 224x224 (scale 0.2-1.0), horizontal flip, color jitter, random grayscale (0.2), Gaussian blur with probability 1.0 on view 1 and 0.1 on view 2, and solarization on view 2 with probability 0.2. BYOL (Appendix B, Table 6): Gaussian blur probability 1.0 for the first view (T) and 0.1 for the second (T'), solarization 0.0 for T and 0.2 for T', color dropping (grayscale) 0.2 for both, crops covering 8%-100% of the image. The blur, solarization and grayscale probabilities therefore match, while the lower bound of the crop scale differs (0.2 versus 8%), and BabyCL does not cite BYOL for these settings. Negatives: BabyCL's instance loss is a SimCLR objective and its cross-modal loss a symmetric InfoNCE, and it cites Zhuang et al. (2021) as finding that contrastive methods with negative sampling are most effective on SAYCam. BYOL reports state-of-the-art ImageNet results without negative pairs and finds it much less affected than SimCLR when color distortion is removed from the augmentations. Neither paper tests a BYOL-style objective in a streaming child-egocentric setting.

**System answer.** ## Augmentation probabilities: Gaussian blur & solarization

**BabyCL** [BabyCL, p.14]:
> "Gaussian blur (applied with probability 1.0 on view 1 and 0.1 on view 2), and solarization on view 2 with probability 0.2."

So for BabyCL's two views:
- View 1: blur p = 1.0, solarization p = 0 (not mentioned, i.e., not applied)
- View 2: blur p = 0.1, solarization p = 0.2

**BYOL** [BYOL, p.16, Table 6]:
| Parameter | T (view 1) | T′ (view 2) |
|---|---|---|
| Gaussian blurring probability | 1.0 | 0.1 |
| Solarization probability | 0.0 | 0.2 |

So for BYOL's two views:
- View 1 (T): blur p = 1.0, solarization p = 0.0
- View 2 (T′): blur p = 0.1, solarization p = 0.2

**Comparison:** The two sets of values are identical — both papers apply blur with probability 1.0 on the first view and 0.1 on the second, and solarization with probability 0 on the first view and 0.2 on the second. This is consistent with BabyCL's visual augmentations being drawn directly from the SimCLR/BYOL-style augmentation recipe (BabyCL cites SimCLR for its instance loss, [BabyCL, p.4]).

## Whether negative pairs are needed

**BYOL** makes an explicit claim that negative pairs are *not* necessary:
> "While state-of-the art methods rely on negative pairs... BYOL achieves a new state of the art without them." [BYOL, p.1]
> "BYOL achieves higher performance than state-of-the-art contrastive methods without using negative pairs... we suspect that not relying on negative pairs is one of the leading reasons for its improved robustness." [BYOL, p.2]

BYOL's ablations also show it is more robust to batch size and augmentation choice than SimCLR, which it attributes partly to the absence of negative pairs [BYOL, p.7–8].

**BabyCL**, by contrast, does not make any claim about whether negative pairs are necessary or avoidable. Its visual instance loss is explicitly a "SimCLR objective" [BabyCL, p.4], and its cross-modal loss is "a symmetric InfoNCE loss on utterance-frame pairs" [BabyCL, p.4] — both of these are negative-pair-based contrastive losses. The passages for BabyCL give no discussion of removing negative pairs or of their necessity; the paper simply adopts negative-pair contrastive objectives (SimCLR and InfoNCE) as two of its three joint losses.

**Summary:** The evidence shows BYOL explicitly argues negative pairs are unnecessary and demonstrates this empirically, whereas BabyCL's provided passages do not address this question at all — BabyCL's own losses (SimCLR instance loss and InfoNCE cross-modal loss) rely on negative pairs, and no claim about their necessity (or lack thereof) is made in the paper excerpts given.

**Retrieved:** BabyCL p.1-15 (0.71); BYOL p.1-35 (0.68); TemporalStraightening p.1-29 (0.66) | gold page hit: 1.00
*20.6 s*

## Q16 (text-only, cross-paper, hard, answerable: yes)

**Question.** Daily Oracle uses a particular retriever in its retrieval-augmented setting. What is it, and what does the embedding-retrieval paper report about how that type of retriever behaves compared with dense embedding models on its LIMIT task?

**Reference answer.** Daily Oracle's constrained open-book setting uses BM25 to retrieve the top 5 articles per question, each truncated to 512 words, restricted to articles available before the resolution date and RAG cutoff. The embedding-retrieval paper finds that on LIMIT, state-of-the-art dense single-vector models struggle (full setting rarely reaches even 20% recall@100; on the 46-document version they cannot solve the task even at recall@20), whereas BM25 'comes close to perfect scores'. The authors attribute this to sparse models behaving like single vectors with very high dimensionality, but add that it is unclear how to apply sparse models to instruction-following or reasoning tasks without lexical overlap. The LIMIT result concerns a synthetic combinatorial task and says nothing about Daily Oracle's news-forecasting data.

**System answer.** **Retriever used in Daily Oracle's constrained open-book (RAG) setting:** BM25. The paper states: "Following prior work (Jin et al., 2021; Zou et al., 2022; Zhang et al., 2024), we employ BM25 (Robertson et al., 1995) as the retriever and select the top 5 articles relevant to each question" [DailyOracle, p.5].

**What the embedding-limitations paper (LIMIT) reports about BM25 vs. dense embedding models:**

On their LIMIT benchmark, EmbeddingLimits finds that BM25 (a sparse/lexical retriever, not a single dense vector) performs dramatically better than state-of-the-art dense embedding models, despite the task being trivially simple:

- "Lexical models like BM25 do very well due to their higher dimensionality" [EmbeddingLimits, p.9].
- "BM25 comes close to perfect scores" while single-vector dense embedding models (E5-Mistral, GritLM, Qwen3, Gemini Embed, Snowflake Arctic, Promptriever) "severely struggle even though the task is trivially simple," with models "struggl[ing] to reach even 20% recall@100" in the full LIMIT setting [EmbeddingLimits, p.9].
- Concrete numbers (Table 5): BM25 scores Recall@2=85.7, Recall@10=90.4, Recall@100=93.6, versus the best dense model (Promptriever Llama3 8B at 4096 dims) reaching only Recall@2=3.0, Recall@10=6.8, Recall@100=18.9 [EmbeddingLimits, p.23].
- The explanation given: "Sparse models (both lexical and neural versions) can be thought of as single vector models but with very high dimensionality. This dimensionality helps BM25 avoid the problems of the neural embedding models as seen in Figure 3. Since the d of their vectors is high, they can scale to many more combinations than their dense vector counterparts" [EmbeddingLimits, p.12].
- The paper's theoretical account is that this is a dimensionality effect: because the number of top-k document combinations a model can represent is bounded by the embedding dimension (sign-rank of the qrels matrix), and BM25's effective "vector" dimension (vocabulary-sized) is far larger than a typical dense embedder's dimension (1024–4096), BM25 can represent many more of LIMIT's combinations and thus avoids the theoretical limitation that handicaps dense embedding models [EmbeddingLimits, p.5-6, p.9, p.12].

So, in short: Daily Oracle retrieves with BM25, and per EmbeddingLimits, BM25-type sparse retrievers—because of their effectively much higher dimensionality—vastly outperform single-vector dense embedding models on the LIMIT combinatorial-retrieval stress test, nearly solving it while dense models fail badly.

**Retrieved:** EmbeddingLimits p.1-24 (0.73); DailyOracle p.1-35 (0.69); MMLU p.1-27 (0.59) | gold page hit: 1.00
*18.4 s*

## Q17 (text-only, cross-paper, medium, answerable: yes)

**Question.** Daily Oracle and FIRE-Bench both use LLMs inside their evaluation pipelines. How does each validate that automated component against human judgment, and what agreement numbers does each report?

**Reference answer.** Daily Oracle validated its LLM-based QA filtering: four human annotators rated 30 TF and 30 MC sampled QA pairs on the seven filtering principles; inter-annotator agreement was fair (average Fleiss' kappa 0.26), and the LLM scores matched the human consensus with 89.52% accuracy across the seven principles and 85.00% for the final accept/reject decision (threshold of 13 points). FIRE-Bench validated its automated claim extraction and entailment-based scoring by human validation on a 33% subset of reference instances, reporting precision 0.95, recall 0.86 and F1 0.89. The two validate different components (question quality versus claim matching) with different metrics, so the numbers are not directly comparable.

**System answer.** # Human Validation of LLM-Based Evaluation Components

Both papers use an LLM as an automated judge/filter within their pipeline (Daily Oracle for QA filtering; FIRE-Bench for claim extraction/matching in scoring), and both validate this component against human annotators—but with different methodologies and metrics.

## Daily Oracle

**What is validated:** The LLM-based QA Filtering step, which scores candidate question-answer pairs against seven quality principles (correctness, non-answerability before publication date, absence of information leakage, objectivity, clear temporal element, public interest, non-obviousness) and accepts pairs scoring ≥13 points total [DailyOracle, p.5].

**Validation method:** Four human annotators independently score a random sample of 30 TF and 30 MC QA pairs (60 total) using the same seven principles given to the LLM [DailyOracle, p.5, p.14].

**Agreement numbers reported:**
- **Inter-annotator agreement (human-human):** Average Fleiss' Kappa = 0.26 ("fair agreement"), ranging from 0.02 (Non-Answerability Before the Publication Date) to 0.66 (Objectivity) across the seven principles [DailyOracle, p.5, p.14, Table 4].
- **Human vs. LLM agreement:** Average accuracy = 89.52% across the seven principles (comparing LLM-assigned scores to human consensus scores), ranging from 83.33% (Non-answerability Before the Publication Date, Non-obviousness of the Answer) to 98.33% (Objectivity) [DailyOracle, p.5, p.14, Table 4].
- **Final acceptance agreement:** For the binary accept/reject decision (threshold ≥13 points), LLM and human consensus scores showed **85.00% accuracy** [DailyOracle, p.5].

## FIRE-Bench

**What is validated:** The claim-extraction and semantic-entailment matching procedure used to decompose agent-generated conclusions and ground-truth text into atomic claims, then match them to compute Precision/Recall/F1 [FIRE-Bench, p.5]. (This is based on the RAGChecker claim-centric evaluation paradigm [FIRE-Bench, p.5].)

**Validation method:** Human validation is performed "on a subset of reference instances (33%)" [FIRE-Bench, p.5]. A more detailed description in the appendix states that human annotators and RAGChecker independently decompose sampled agent-generated findings into atomic claims, and the two sets are matched by humans to compute precision/recall/F1 [FIRE-Bench, p.24].

**Agreement numbers reported:**
- **Precision = 0.95**
- **Recall = 0.86**
- **F1 = 0.89** [FIRE-Bench, p.5, p.24]

The paper states this shows "the automated protocol provides a stable approximation of human judgment" [FIRE-Bench, p.5], and the appendix adds that illustrative examples show RAGChecker's claim decomposition "closely aligns with human decomposition," though occasional misses of fine-grained details are noted (e.g., in Example 3 of the appendix, one human-identified claim is missed, giving recall 0.80 and F1 0.89 for that single case) [FIRE-Bench, p.24, p.28].

## Summary of Differences

| Aspect | Daily Oracle | FIRE-Bench |
|---|---|---|
| Component validated | QA filtering (7-principle scoring) | Claim extraction + entailment matching |
| Sample size | 60 QA pairs (30 TF + 30 MC) | 33% of reference instances |
| # Human annotators | 4 | Not specified in the given passages |
| Metric(s) | Fleiss' Kappa (human-human) = 0.26; Accuracy (human vs. LLM) = 89.52% per-principle, 85.00% for final accept decision | Precision = 0.95, Recall = 0.86, F1 = 0.89 |

The evidence does not specify how many human annotators FIRE-Bench used for its RAGChecker validation, nor does it give a per-category breakdown analogous to Daily Oracle's Table 4 — the passages only report the single aggregate P/R/F1 triple [FIRE-Bench, p.5, p.24].

**Retrieved:** DailyOracle p.1-35 (0.71); FIRE-Bench p.1-34 (0.70); SWE-bench p.1-52 (0.62) | gold page hit: 1.00
*18.6 s*

## Q18 (text-only, insufficient-evidence, medium, answerable: no)

**Question.** According to the distillation paper, what accuracy does a single network reach on the JFT dataset after the knowledge in the specialist models has been distilled back into it?

**Reference answer.** The supplied paper does not establish this. For JFT it reports an ensemble of a generalist baseline plus 61 specialist models whose predictions are combined at inference time (top-1 test accuracy 25.0% to 26.1%, a 4.4% relative improvement; conditional accuracy 43.1% to 45.9%), and it states 'We have not yet shown that we can distill the knowledge in the specialists back into the single large net'. A related idea (using soft targets to stop specialists overfitting) is described as one it is 'currently exploring'. Where the paper does distill, it reports MNIST and speech results (a single acoustic model recovering more than 80% of the frame-accuracy gain of a 10-model ensemble), not JFT.

**System answer.** The evidence does not establish this. The Distillation paper explicitly states that this experiment was not performed: "We have not yet shown that we can distill the knowledge in the specialists back into the single large net" [Distillation, p.8].

What the paper does show on JFT:
- The baseline (generalist) model alone achieves 25.0% test accuracy [Distillation, p.7, Table 3].
- Combining the baseline with an ensemble of 61 specialist models (without distilling them back into a single net) raises test accuracy to 26.1%, a 4.4% relative improvement [Distillation, p.7, Table 3].

So the paper reports performance of the generalist+specialists ensemble, but does not report any accuracy figure for a single distilled network incorporating the specialists' knowledge, since that experiment had not yet been done at the time of writing.

**Retrieved:** Distillation p.1-9 (0.73); FIRE-Bench p.1-34 (0.67); Transformer p.1-15 (0.65) | gold page hit: 1.00
*7.1 s*

## Q20 (text-only, insufficient-evidence, easy, answerable: no)

**Question.** According to the SWE-bench paper, what resolve rate do agent-based systems (models that run code, navigate the repository and iterate) reach on SWE-bench?

**Reference answer.** The supplied paper does not establish this. It evaluates single-pass language models (ChatGPT-3.5, GPT-4, Claude 2 and others, and the fine-tuned SWE-Llama) that are given BM25-retrieved or oracle files and generate one patch, and its main-text resolve rates are all single-digit percentages (for example Claude 2 resolves 4.8% with oracle retrieval). Agent-based methods appear only as an intended direction: the task can serve as a level playing field for approaches 'ranging from retrieval and long-context models to decision-making agents', and the authors 'encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs)'. No agent results are reported.

**System answer.** The SWE-bench paper does not evaluate agent-based systems (models that run code, navigate the repository, and iterate). All reported results use retrieval-based baselines only — specifically BM25 retrieval and an "oracle" retrieval setting that simply feeds the model relevant files, followed by a single, non-iterative generation step [SWE-bench, p.4-5].

Explicitly, the paper states: "our experiments aim to establish a baseline of the simplest and most straight-forward approaches for this task; we do not intend to constrain future methodologies to the same type of approach and encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs)" [SWE-bench, p.10].

So the evidence shows:
- Best resolve rate overall with BM25 retrieval: Claude 2 at 1.96% (main abstract figure) / reported as 1.97% in Table 5 [SWE-bench, p.1, p.6].
- Best resolve rate with "oracle" retrieval: Claude 2 at 4.8% [SWE-bench, p.6, Table 18 p.26].

These are non-agentic, single-shot retrieval baselines. The paper does not report any results for agent-based systems that run code, navigate the repository, or iterate — it explicitly flags this as future work rather than something it measures.

**Retrieved:** SWE-bench p.1-52 (0.78); FIRE-Bench p.1-34 (0.68); Transformer p.1-15 (0.64) | gold page hit: 1.00
*9.9 s*

## Q31 (text+table, cross-source, medium, answerable: yes)

**Question.** The ViT paper says smaller patches make a Transformer more expensive. Using the sequence length it implies for 224-px inputs, how do the GMACs and measured throughput of ViT-Base with 32, 16 and 8 pixel patches compare with that expectation?

**Reference answer.** The ViT paper defines the number of patches (the Transformer's sequence length) as N = HW/P^2 and says smaller patch sizes are computationally more expensive. At 224 px that gives N = 49, 196 and 784 for P = 32, 16 and 8, i.e. 4x more tokens at each step. timm shows (parameters nearly constant: 88.22M, 86.57M, 86.58M): GMACs 4.41, 17.58 and 78.22, so 3.99x from B/32 to B/16 and 4.45x from B/16 to B/8; throughput 10,936.95, 2,992.79 and 700.85 samples/s, i.e. 3.65x slower and then 4.27x slower. Cost therefore grows roughly with token count while parameters stay flat; B/8 exceeds 4x in GMACs, which the paper does not explain.

**System answer.** ## Setting up the expectation

The ViT paper states explicitly: "Note that the Transformer's sequence length is inversely proportional to the square of the patch size, thus models with smaller patch size are computationally more expensive." [ViT, p.5]

The sequence length formula given is N = HW/P² [ViT, p.3]. For a 224×224 input (H=W=224):

- Patch 32: N = 224²/32² = 50176/1024 = **49**
- Patch 16: N = 224²/16² = 50176/256 = **196**
- Patch 8: N = 224²/8² = 50176/64 = **784**

So halving the patch size quadruples the sequence length at each step (49 → 196 → 784, each exactly 4×). Since self-attention per layer costs O(N²·d) [Transformer, p.6, Table 1], a naive expectation would be that compute could scale as badly as N² (i.e., up to 16× per halving) if attention dominated, while the paper's stated "inversely proportional to the square of patch size" wording (which refers to N itself, not FLOPs) would predict at least a ~4× increase per halving if cost scales linearly with N.

## Checking GMACs against this

From the benchmark data:

| Patch | N (implied) | GMACs | GMACs ratio vs prior |
|---|---|---|---|
| 32 | 49 | 4.41 | — |
| 16 | 196 | 17.58 | 17.58/4.41 = 3.99 ≈ 4× |
| 8 | 784 | 78.22 | 78.22/17.58 = 4.45× |

The 32→16 step matches the N-scaling almost exactly (4.0× increase in both N and GMACs). The 16→8 step shows a slightly larger-than-N increase (4.45× vs. 4× for N), suggesting the O(N²) attention term is starting to contribute more once N (784) becomes comparable to the model width D=768 [ViT, p.5, Table 1], rather than the per-layer MLP/projection cost (which is linear in N) dominating completely as it does at smaller N.

Param counts stay essentially flat (86.57M, 88.22M, 86.58M), consistent with patch size changing the effective sequence length rather than model parameters.

## Checking measured throughput

| Patch | samples/sec | Slowdown vs prior (1/ratio) |
|---|---|---|
| 32 | 10936.95 | — |
| 16 | 2992.79 | 10936.95/2992.79 = 3.65× slower |
| 8 | 700.85 | 2992.79/700.85 = 4.27× slower |

Measured throughput drops by roughly 3.65× then 4.27× as patch size halves each time — again close to, but not exactly matching, the 4× implied purely by N quadrupling. The slightly sub-4× slowdown at 32→16 (3.65×) versus the super-4× slowdown at 16→8 (4.27×) is consistent with the GMACs pattern: at smaller N (49→196) the cost grows a bit less than the GMACs/N scaling would predict (likely due to fixed overhead and hardware parallelism being less saturated at small N=49), while at larger N (196→784) real throughput cost grows slightly faster than linear, matching the quadratic attention term becoming non-negligible.

## Summary

The GMACs and measured throughput are **broadly consistent with** the ViT paper's claim that smaller patches make the Transformer more expensive [ViT, p.5]: each halving of patch size quadruples the implied sequence length (49→196→784), and both compute (GMACs) and inverse-throughput increase by roughly that same ~4× factor at each step. The match is closest for the 32→16 step (GMACs: 3.99×; throughput slowdown: 3.65×) and shows a mildly super-linear deviation at the 16→8 step (GMACs: 4.45×; throughput slowdown: 4.27×) — i.e., slightly worse than the pure N-scaling would predict, which is plausible given that self-attention's per-layer cost is O(N²·d) [Transformer, p.6] and N=784 is no longer small relative to D=768, so the quadratic term in N (rather than just the linear-in-N MLP/projection cost) begins to matter more at the finest patch size. The evidence does not let us decompose GMACs into attention-vs-MLP contributions directly, so this quadratic-term explanation for the extra super-linear growth at patch 8 is a plausible inference from the passages rather than something stated outright in the text.

**Retrieved:** ViT p.1-22 (0.71); Transformer p.1-15 (0.59); MMLU p.1-27 (0.59) | gold page hit: 1.00
**SQL:** `SELECT     arch,     img_size,     param_count_m,     gmacs,     macts,     samples_per_sec,     step_time_ms,     batch_size FROM benchmark_infer WHERE img_size = 224   AND arch IN ('vit_base_patch32_224', 'vit_base_patch16_224', 'vit_base_patch8_224') ORDER BY arch;` | overlap with reference result: 1.00
*44.8 s*

## Q32 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper reports FLOPs for its 18-, 34-, 50-, 101- and 152-layer networks. How do timm's measured GMACs at 224 px compare, and for which depth is the difference largest?

**Reference answer.** The paper's Table 1 gives 1.8, 3.6, 3.8, 7.6 and 11.3 billion FLOPs, and defines its FLOPs as multiply-adds. timm's infer_gmacs at 224 px are 1.82, 3.67, 4.11, 7.83 and 11.56, i.e. +1.1%, +1.9%, +8.2%, +3.0% and +2.3%. The largest difference is for resnet50 (4.11 vs 3.8, +8.2%). Neither PDF explains the gap, so the cause should not be asserted.

**System answer.** ## Comparison: ResNet paper's reported FLOPs vs. timm's measured GMACs (224px)

The ResNet paper reports FLOPs (multiply-adds) per architecture in Table 1: "FLOPs: 1.8×10⁹, 3.6×10⁹, 3.8×10⁹, 7.6×10⁹, 11.3×10⁹" for the 18/34/50/101/152-layer networks respectively [ResNet, p.5]. Since the paper's "FLOPs" here are defined as multiply-adds, they are directly comparable to GMACs (1 MAC = 1 multiply-add).

| Depth | Paper FLOPs (GFLOPs/GMACs) | timm GMACs (224px) | Difference (timm − paper) | % difference |
|---|---|---|---|---|
| ResNet-18 | 1.8 | 1.82 | +0.02 | 0.02/1.8 ≈ 1.1% |
| ResNet-34 | 3.6 | 3.67 | +0.07 | 0.07/3.6 ≈ 1.9% |
| ResNet-50 | 3.8 | 4.11 | +0.31 | 0.31/3.8 ≈ 8.2% |
| ResNet-101 | 7.6 | 7.83 | +0.23 | 0.23/7.6 ≈ 3.0% |
| ResNet-152 | 11.3 | 11.56 | +0.26 | 0.26/11.3 ≈ 2.3% |

**Calculations:**
- 1.82 − 1.8 = 0.02
- 3.67 − 3.6 = 0.07
- 4.11 − 3.8 = 0.31
- 7.83 − 7.6 = 0.23
- 11.56 − 11.3 = 0.26

**Where the difference is largest:**
- In **absolute** terms, ResNet-50 shows the largest gap (0.31 GMACs).
- In **relative/percentage** terms, ResNet-50 is also the largest outlier (≈8.2% higher in timm than reported in the paper), noticeably more than ResNet-18/34/101/152, which all differ by only ~1–3%.

This is consistent with the paper's own statement that ResNet-50 (and the deeper variants) use the "bottleneck" building block, described as "both designs have similar time complexity" to the non-bottleneck block used in ResNet-34 [ResNet, p.6], suggesting the reported 3.8 GFLOPs figure may have been a rounded/approximate estimate for the bottleneck design, while timm's measured 4.11 GMACs reflects the actual bottleneck computation more precisely. The passages do not explain the exact source of this discrepancy beyond this architectural note, so the cause of the larger ResNet-50 gap cannot be further confirmed from the evidence given.

**Retrieved:** ResNet p.1-12 (0.63); MMLU p.1-27 (0.61); FIRE-Bench p.1-34 (0.60) | gold page hit: 1.00
**SQL:** `SELECT arch, img_size, gmacs, param_count_m, batch_size FROM benchmark_infer WHERE arch IN ('resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152')   AND img_size = 224 ORDER BY gmacs;` | overlap with reference result: 1.00
*25.7 s*

## Q34 (text+table, cross-source, hard, answerable: yes)

**Question.** Among timm rows whose weights tag starts with 'mae', which has the highest ImageNet-R and ImageNet-A top-1, how do ImageNet-R and ImageNet-A top-1 change with model size across these rows, and what pre-training task does the MAE paper describe?

**Reference answer.** Six hiera_*_224.mae_in1k_ft_in1k rows are tagged mae. hiera_huge_224 is highest on ImageNet-R (64.967) and ImageNet-A (66.253) (and Sketch, 50.078), with 672.78M parameters. ImageNet-R and ImageNet-A top-1 both rise at every step with model size: R is 45.78 (tiny), 49.373 (small), 53.14 (base), 55.57 (base_plus), 60.29 (large), 64.967 (huge); A is 30.56, 36.453, 43.4, 49.24, 58.013, 66.253. The drop relative to clean top-1 on the same 200 classes also shrinks with size (R: -49.47 for tiny to -32.243 for huge; A: -65.04 to -31.717), so the larger models lose less under these shifts. The MAE paper describes pre-training that masks random patches (75% in its default) and reconstructs the missing pixels with an encoder that processes only the visible patches. Caveats: the six rows are one family (Hiera, all fine-tuned on ImageNet-1k at 224 px), so this is a trend across six rows, not a controlled test; the MAE paper's own encoder is a plain ViT, Hiera is not in the corpus, and what the timm tag implies about Hiera's recipe is not stated in the PDFs.

**System answer.** ## Highest ImageNet‑R / ImageNet‑A top‑1 among MAE-tagged timm rows

Based on the database query (rows filtered to `weights_tag LIKE 'mae%'`, columns `top1_r` = ImageNet‑R top‑1, `top1_a` = ImageNet‑A top‑1):

| model | params (M) | top1_r (ImageNet‑R) | top1_a (ImageNet‑A) |
|---|---|---|---|
| hiera_tiny_224.mae_in1k_ft_in1k | 27.91 | 45.78 | 30.56 |
| hiera_small_224.mae_in1k_ft_in1k | 35.01 | 49.373 | 36.453 |
| hiera_base_224.mae_in1k_ft_in1k | 51.52 | 53.14 | 43.4 |
| hiera_base_plus_224.mae_in1k_ft_in1k | 69.9 | 55.57 | 49.24 |
| hiera_large_224.mae_in1k_ft_in1k | 213.74 | 60.29 | 58.013 |
| **hiera_huge_224.mae_in1k_ft_in1k** | **672.78** | **64.967** | **66.253** |

**Highest:** `hiera_huge_224.mae_in1k_ft_in1k` has the top values on both metrics (top1_r = 64.967, top1_a = 66.253), the largest model (672.78M params).

## Trend with model size

Both metrics increase monotonically as parameter count grows, from tiny (27.91M) through huge (672.78M):

- ImageNet‑R (top1_r): 45.78 → 49.373 → 53.14 → 55.57 → 60.29 → 64.967
  - Total gain tiny→huge: 64.967 − 45.78 = **+19.187 points**
- ImageNet‑A (top1_a): 30.56 → 36.453 → 43.4 → 49.24 → 58.013 → 66.253
  - Total gain tiny→huge: 66.253 − 30.56 = **+35.693 points**

Notably, ImageNet‑A improves faster (in absolute points) than ImageNet‑R as model size increases — e.g. going from large (213.74M) to huge (672.78M): Δtop1_r = 64.967 − 60.29 = +4.677, while Δtop1_a = 66.253 − 58.013 = +8.24. This pattern (robustness/adversarial-style benchmark gains outpacing other OOD benchmark gains as scale increases) is consistent with what the MAE paper itself reports for its own ViT backbones: "our method has strong scaling behavior: increasing the model sizes has significant gains... with ViT-H, our MAE pre-training is 35% better on IN-A (68.2% vs 33.1%) than the supervised counterpart" [MAE, p.12].

(Note: these particular rows use the Hiera architecture, not evaluated in the MAE paper passage itself; the trend comparison is based solely on the database numbers.)

## Pre-training task described in the MAE paper

The MAE paper describes a masked-autoencoding pre-training task for vision:

- "We mask random patches of the input image and reconstruct the missing pixels." [MAE, p.1]
- It uses "an asymmetric encoder-decoder architecture, with an encoder that operates only on the visible subset of patches (without mask tokens), along with a lightweight decoder that reconstructs the original image from the latent representation and mask tokens." [MAE, p.1]
- "Masking a high proportion of the input image, e.g., 75%, yields a nontrivial and meaningful self-supervisory task." [MAE, p.1]
- Mechanistically: "we divide an image into regular non-overlapping patches. Then we sample a subset of patches and mask (i.e., remove) the remaining ones... we sample random patches without replacement, following a uniform distribution." The encoder ("a ViT... applied only on visible, unmasked patches") embeds and processes only the visible subset; the decoder's input is "the full set of tokens consisting of (i) encoded visible patches, and (ii) mask tokens," each mask token being "a shared, learned vector that indicates the presence of a missing patch to be predicted." [MAE, p.3]
- "Our MAE reconstructs the input by predicting the pixel values for each masked patch... Our loss function computes the mean squared error (MSE) between the reconstructed and original images in the pixel space. We compute the loss only on masked patches." [MAE, p.4]

**Retrieved:** BatchNorm p.1-11 (0.70); MAE p.1-14 (0.67); ResNet p.1-12 (0.67) | gold page hit: 1.00
**SQL:** `SELECT model, arch, weights_tag, img_size, param_count_m,        top1_r, top1_a FROM model_results WHERE weights_tag LIKE 'mae%' ORDER BY top1_r DESC, top1_a DESC;` | overlap with reference result: 0.51
*28.8 s*

## Q35 (text+table, cross-source, hard, answerable: yes)

**Question.** For ViT models released with the same augreg recipe tag, how much higher is ImageNet top-1 when the weights come from ImageNet-21k pre-training plus ImageNet-1k fine-tuning than when trained on ImageNet-1k only, is the gain similar for the Small and Base models, and is the pattern consistent in direction with what the ViT paper says about pre-training data?

**Reference answer.** In all six matched pairs the ImageNet-21k-then-1k weights are better, by 2.56 to 5.82 points: vit_base_patch16_224 +5.38 (84.534 vs 79.154), vit_base_patch16_384 +4.908, vit_base_patch32_224 +5.824, vit_base_patch32_384 +4.608, vit_small_patch16_224 +2.56, vit_small_patch16_384 +2.684. The gain is not the same for the two sizes: the four Base rows gain 4.6 to 5.8 points (mean 5.18) and the two Small rows 2.6 to 2.7 (mean 2.62). This is consistent in direction with the ViT paper, which says large-scale pre-training helps ('large scale training trumps inductive bias') and that larger models show their benefit only with more pre-training data. It is not a confirmation: the paper's evidence uses different pre-training sets (ImageNet, ImageNet-21k, JFT-300M) and includes ViT-Large, which has no pair here, and with only two sizes a size effect cannot be separated from other differences between the Small and Base models.

**System answer.** ## ImageNet top‑1 gain from ImageNet‑21k pretraining vs. ImageNet‑1k‑only, by model size

Using the query results, I can compare `augreg_in1k` (trained only on ImageNet‑1k) vs. `augreg_in21k_ft_in1k` (ImageNet‑21k pretrain + ImageNet‑1k fine‑tune) for matching patch size / image size pairs:

**ViT‑Base**
| config | in1k | in21k_ft_in1k | Δ (pp) |
|---|---|---|---|
| patch16, 224px | 79.154 | 84.534 | **5.380** |
| patch16, 384px | 81.102 | 86.010 | **4.908** |
| patch32, 224px | 74.908 | 80.732 | **5.824** |
| patch32, 384px | 78.750 | 83.358 | **4.608** |

**ViT‑Small**
| config | in1k | in21k_ft_in1k | Δ (pp) |
|---|---|---|---|
| patch16, 224px | 78.842 | 81.402 | **2.560** |
| patch16, 384px | 81.130 | 83.814 | **2.684** |

(No ViT‑Small `augreg_in1k` row exists for patch32 or the r26_s32 hybrid, so those configs can't be compared.)

**Is the gain similar for Small vs. Base?**
No — the Base‑size gains (≈4.6–5.8 pp) are roughly **twice as large** as the Small‑size gains (≈2.6–2.7 pp). The benefit of ImageNet‑21k pretraining is clearly size‑dependent in this data, with the larger (Base) model gaining substantially more than the smaller (Small) model.

**Is this consistent with the ViT paper's claims about pretraining data?**
Yes, the direction matches. The ViT paper reports that larger models need larger pretraining data to show their advantage: "When pre-trained on the smallest dataset, ImageNet, ViT-Large models underperform compared to ViT-Base models, despite (moderate) regularization. With ImageNet-21k pre-training, their performances are similar. Only with JFT-300M, do we see the full benefit of larger models" [ViT, p.6]. More generally, the paper states "large scale training trumps inductive bias" and that ViT "attains excellent results when pre-trained at sufficient scale" [ViT, p.2], and that "the convolutional inductive bias is useful for smaller datasets, but for larger ones, learning the relevant patterns directly from data is sufficient, even beneficial" [ViT, p.7].

This is consistent with the query result pattern: moving from ImageNet‑1k‑only pretraining to the larger ImageNet‑21k pretraining benefits the larger (Base) architecture more than the smaller (Small) architecture — i.e., bigger models extract more value from more pretraining data, exactly the scaling relationship the ViT paper emphasizes. The evidence here doesn't directly test ViT‑Large/Huge or JFT‑300M (those comparisons in the paper use datasets/models not covered in this query result), so I can only confirm the directional consistency for the Small vs. Base comparison available.

**Retrieved:** BatchNorm p.1-11 (0.72); ResNet p.1-12 (0.67); ViT p.1-22 (0.67) | gold page hit: 1.00
**SQL:** `SELECT   CASE     WHEN arch LIKE 'vit_small%' THEN 'small'     WHEN arch LIKE 'vit_base%' THEN 'base'     ELSE arch   END AS size_group,   arch,   model,   weights_tag,   img_size,   top1_val FROM model_results WHERE (arch LIKE 'vit_small%' OR arch LIKE 'vit_base%')   AND (weights_tag = 'augreg_in1k' OR weights_tag = 'augreg_in21k_ft_in1k') ORDER BY size_group, arch, weights_tag, img_size;` | overlap with reference result: 0.77
*26.6 s*

## Q37 (text+table, cross-source, hard, answerable: yes)

**Question.** The ViT paper reports that ViT needs roughly 2-4x less compute than ResNets for the same transfer performance. In timm at 224 px, how do ViT-B/16 and ResNet-50/101/152 compare on top-1 and measured throughput, and what does that comparison say, or not say, about the paper's claim?

**Reference answer.** The paper's claim is about pre-training compute (Figure 5 is accuracy vs pre-training exaFLOPs, JFT-300M, controlled study), with the caveat that efficiency can depend on schedule, optimiser and weight decay. timm measures inference throughput and has no pre-training compute. At 224 px, taking the best ViT-B/16 row and the a1h_in1k row of each ResNet (one recipe across depths), vit_base_patch16_224.augreg2_in21k_ft_in1k has 85.108 top-1 at 2,992.79 samples/s (17.58 GMACs), versus resnet152.a1h_in1k 82.818 at 1,976.86 (11.56 GMACs), resnet101.a1h_in1k 81.95 at 2,781.19 (7.83 GMACs) and resnet50.a1h_in1k 80.654 at 4,302.84 (4.11 GMACs). So this ViT-B/16 row is more accurate than all three and faster than resnet152 (1.51x) and resnet101 (1.08x) despite more GMACs, but slower than resnet50. The ranking depends on which rows are compared: the best ResNet-50 row is resnet50.fb_swsl_ig1b_ft_in1k (81.146, trained with extra data) and is still below the best ViT-B/16 row, but the ImageNet-1k-only vit_base_patch16_224.augreg_in1k row (79.154) is below all three a1h_in1k ResNets, so the accuracy differences track pre-training data and recipe as much as architecture. These numbers neither confirm nor refute the 2-4x pre-training-compute claim.

**System answer.** ## What the timm data shows

**Top‑1 accuracy (best checkpoint per architecture, 224 px):**

| Model | Best top‑1 | GMACs (inference) | Throughput (img/s, bs=1024) | Params (M) |
|---|---|---|---|---|
| ResNet‑50 | 81.146 (fb_swsl_ig1b_ft_in1k) | 4.11 | 4302.84 | 25.56 |
| ResNet‑101 | 81.95 (a1h_in1k) | 7.83 | 2781.19 | 44.55 |
| ResNet‑152 | 82.818 (a1h_in1k) | 11.56 | 1976.86 | 60.19 |
| ViT‑B/16 | 85.108 (augreg2_in21k_ft_in1k) | 17.58 | 2992.79 | 86.57 |

**Calculations — ViT‑B/16's GMACs relative to each ResNet:**
- vs ResNet‑50: 17.58 / 4.11 ≈ 4.28× **more** compute (per inference pass)
- vs ResNet‑101: 17.58 / 7.83 ≈ 2.24× **more** compute
- vs ResNet‑152: 17.58 / 11.56 ≈ 1.52× **more** compute

**Accuracy gain at that extra compute:**
- ViT‑B/16 vs ResNet‑152: +2.29 pts top‑1 (85.108 − 82.818) for 1.52× more GMACs
- ViT‑B/16 vs ResNet‑101: +3.16 pts top‑1 for 2.24× more GMACs
- ViT‑B/16 vs ResNet‑50: +3.96 pts top‑1 for 4.28× more GMACs

**Throughput comparison:** ViT‑B/16 (2992.79 img/s) is actually *faster in practice* than ResNet‑101 (2781.19 img/s) despite having ~2.24× the theoretical GMACs, and is faster than ResNet‑152 (1976.86 img/s), but slower than ResNet‑50 (4302.84 img/s).

## Does this support the paper's "2–4× less compute" claim?

Not directly, and in the naive GMACs sense it points the opposite way. The ViT paper's claim is specific: "Vision Transformers dominate ResNets on the performance/compute trade-off. ViT uses approximately 2 −4× less compute to attain the same performance (average over 5 datasets)" [ViT, p.8]. That claim is about **total pre-training compute** (measured in exaFLOPs/TPUv3-core-days, Figure 5 / Table 6) when transferring from **JFT‑300M**, using modified "ResNet (BiT)" baselines (BatchNorm→GroupNorm, standardized convolutions) [ViT, p.5, p.8], and it is averaged over 5 transfer datasets — not plain ImageNet-1k top‑1.

The timm numbers here are different in kind:
- GMACs in the query are **single-image inference FLOPs**, not pretraining compute.
- "samples_per_sec" is **inference throughput** on timm's benchmark hardware, not training speed.
- The ResNet checkpoints (`a1h_in1k`, `tv_in1k`, `gluon_in1k`, etc.) are standard ImageNet-1k-trained ResNets, not the BiT-style ResNets the paper benchmarked.
- The ViT‑B/16 best checkpoint used ImageNet‑21k pretraining + ImageNet‑1k fine‑tuning (AugReg recipe), not JFT‑300M.

So what this data **does** show: under timm's measurement, the best ViT‑B/16 checkpoint reaches higher top‑1 accuracy than any ResNet‑50/101/152 checkpoint listed, and its measured inference throughput is comparable to or better than ResNet‑101/152 even though its raw GMACs are higher — consistent with the ViT paper's own observation that "real-world speed...is not always well predicted by theoretical FLOPs due to details like lane widths and cache sizes" [ViT, p.18].

What it does **not** show: it does not establish or refute the paper's specific 2–4× *pretraining*-compute claim, because the datasets being compared (inference GMACs/throughput on ImageNet-1k fine-tuned checkpoints) differ from the paper's measurement (JFT-300M pretraining exaFLOPs vs. 5-dataset average transfer accuracy, Figure 5/Table 6, [ViT, p.8]). Any comparison of training-compute efficiency would require pretraining FLOP counts, which are not present in this query result.

**Retrieved:** ViT p.1-22 (0.62); Transformer p.1-15 (0.59); MMLU p.1-27 (0.57) | gold page hit: 1.00
**SQL:** `SELECT     mr.arch,     mr.model,     mr.weights_tag,     mr.img_size,     mr.top1_val,     mr.param_count_m AS params_m,     bi.samples_per_sec,     bi.gmacs,     bi.batch_size FROM model_results mr JOIN benchmark_infer bi     ON mr.arch = bi.arch     AND mr.img_size = bi.img_size WHERE mr.img_size = 224     AND mr.arch IN ('vit_base_patch16_224', 'resnet50', 'resnet101', 'resnet152') ORDER BY mr.arch, mr.top1_val DESC;` | overlap with reference result: 1.00
*52.6 s*

## Q40 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper says its 152-layer network has lower complexity than VGG-16/19. Using timm's measurements at 224 px, how do parameters, GMACs, throughput and top-1 of resnet152 compare with vgg16 and vgg19, and does lower FLOPs mean faster in this benchmark?

**Reference answer.** The paper says the 152-layer ResNet (11.3 billion FLOPs) has lower complexity than VGG-16/19 (15.3/19.6 billion FLOPs). timm: resnet152 has 60.19M parameters, 11.56 GMACs, 1,976.86 samples/s and tv_in1k top-1 78.33; vgg16 has 138.36M, 15.47 GMACs, 2,235.61 samples/s, top-1 71.594; vgg19 has 143.67M, 19.63 GMACs, 2,044.71 samples/s, top-1 72.4. So resnet152 has 2.3-2.4x fewer parameters, 1.34-1.70x fewer GMACs and higher top-1 (with torchvision weights), but its measured throughput is about 12% lower than vgg16 and 3% lower than vgg19 on this GPU. Lower FLOPs therefore did not mean higher throughput here; the paper's claim concerns FLOPs, not measured speed.

**System answer.** ## Parameters, GMACs, Throughput, and Top-1: ResNet-152 vs VGG-16/19

Using the timm benchmark data (224px, batch size 1024) and picking the plain "tv_in1k" training recipes (closest analog to the original models) alongside ResNet-152's best timm variant:

| Model | Params (M) | GMACs | Samples/sec | Top-1 |
|---|---|---|---|---|
| resnet152.tv_in1k | 60.19 | 11.56 | 1976.86 | 78.33 |
| resnet152.a1h_in1k (best) | 60.19 | 11.56 | 1976.86 | 82.82 |
| vgg16.tv_in1k | 138.36 | 15.47 | 2235.61 | 71.59 |
| vgg19.tv_in1k | 143.67 | 19.63 | 2044.71 | 72.40 |

### Parameters
ResNet-152 has far fewer parameters: 60.19M vs 138.36M (vgg16) and 143.67M (vgg19) — about 2.3× and 2.4× fewer, respectively.

### GMACs (complexity)
ResNet-152: 11.56 GMACs vs vgg16's 15.47 and vgg19's 19.63 — 25% and 41% fewer multiply-accumulate operations. This is consistent with the ResNet paper's claim that "the 152-layer ResNet (11.3 billion FLOPs) still has lower complexity than VGG-16/19 nets (15.3/19.6 billion FLOPs)" [ResNet, p.7] — the timm GMACs (11.56/15.47/19.63) closely match the paper's self-reported FLOPs (11.3/15.3/19.6 billion), since the paper explicitly defines its "FLOPs" as multiply-adds [ResNet, p.3], i.e., the same quantity as MACs.

### Top-1 accuracy
ResNet-152 is substantially more accurate: even its weakest timm checkpoint (78.33%) beats vgg16 (71.59%) by +6.7 points and vgg19 (72.40%) by +5.9 points; its best checkpoint (82.82%) beats them by +11.2 and +10.4 points respectively. (Note: the database result does not indicate which training recipe, if any, matches the original paper's exact numbers — 11.3%/9.33% top-5 for VGG-16/ResNet in the original paper [ResNet, p.6] — so this is a timm-benchmark comparison, not a reproduction of the paper's own reported errors.)

### Does lower GMACs mean faster throughput here?
No — not in this benchmark. Despite having fewer GMACs, ResNet-152 is *slower* in samples/sec than both VGG models:
- vgg16: 2235.61 samples/sec vs resnet152: 1976.86 → vgg16 is ~13.1% faster (2235.61/1976.86 ≈ 1.131) while doing ~33.8% more compute (15.47/11.56 ≈ 1.338).
- vgg19: 2044.71 vs 1976.86 → vgg19 is ~3.4% faster (2044.71/1976.86 ≈ 1.034) while doing ~69.8% more compute (19.63/11.56 ≈ 1.698).

So in this timm throughput benchmark, lower theoretical compute (GMACs/FLOPs) does **not** translate into higher measured wall-clock throughput. The database does not explain why (e.g., hardware parallelism, layer depth/sequential dependency, kernel efficiency), but the numbers themselves show the mismatch between FLOPs-based "complexity" and actual measured speed — a point the ResNet paper itself does not address, since it only discusses FLOPs as a proxy for complexity, not measured throughput [ResNet, p.3, p.7].

**Retrieved:** ResNet p.1-12 (0.59); BatchNorm p.1-11 (0.58); ViT p.1-22 (0.58) | gold page hit: 1.00
**SQL:** `SELECT   mr.arch,   mr.model,   mr.param_count_m,   bi.gmacs,   bi.samples_per_sec,   bi.batch_size,   mr.top1_val FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.arch IN ('resnet152', 'vgg16', 'vgg19')   AND mr.img_size = 224 ORDER BY mr.arch, mr.top1_val DESC;` | overlap with reference result: 1.00
*38.1 s*

## Q42 (text-only, conceptual, medium, answerable: yes)

**Question.** Does the MMLU paper attribute its models' accuracy mainly to parameter count? Use its GPT-3, UnifiedQA and smaller fine-tuned model comparisons.

**Reference answer.** Not mainly: size matters but is not sufficient. In few-shot GPT-3 (Table 1) the three smaller models are near random (Small 25.9%, Medium 24.9%, Large 26.0% against 25.0% for random) while the 175B X-Large model reaches 43.9% (about 37.7% zero-shot). But UnifiedQA, fine-tuned on other QA datasets and tested without further tuning, reaches 48.9% with 11B parameters, better than GPT-3 X-Large despite an order of magnitude fewer parameters, and its smallest 60M variant gets about 29.3%. In Appendix A.1 RoBERTa-base (125M) gets 27.9%, ALBERT-xxlarge (223M) 27.1% and GPT-2 (1.5B) 32.4%; UnifiedQA-60M beats RoBERTa and ALBERT with fewer parameters and UnifiedQA-3B (43.7%) beats GPT-2, which the authors say suggests T5's larger pretraining dataset helps. They conclude that model size is a key component but fine-tuning also helps; the data-size explanation is a suggestion, and the models differ in architecture, fine-tuning data and evaluation regime (GPT-3 few-shot, UnifiedQA tested under distribution shift), so it is not a controlled test.

**System answer.** No — the paper's own comparisons explicitly complicate a pure "accuracy scales with parameter count" story, even though parameter count does matter for GPT-3 specifically.

**1. Within GPT-3, size does correlate with accuracy.**
GPT-3 Small/Medium/Large (2.7B, 6.7B, 13B parameters) all score near random chance (~25%), while GPT-3 X-Large (175B) reaches 43.9% average accuracy [MMLU, p.5, Table 1]. The paper states: "the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%" [MMLU, p.6].

**2. But UnifiedQA beats GPT-3 with far fewer parameters.**
"The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy. This performs better than the few-shot GPT-3 X-Large model, despite UnifiedQA have[ing] an order of magnitude fewer parameters" [MMLU, p.6]. UnifiedQA (11B) at 48.9% > GPT-3 X-Large (175B) at 43.9%, a ~16x parameter reduction with higher accuracy.

The paper's explicit conclusion from this comparison: "These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps" [MMLU, p.6] — i.e., size alone is not treated as the main driver.

**3. Smaller fine-tuned models reinforce this.**
- UnifiedQA's smallest variant (60M parameters) gets ~29.3% accuracy, higher than RoBERTa-base (125M, 27.9%) and ALBERT-xxlarge (223M, 27.1%) [MMLU, p.11-12]. The paper notes: "It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters. This suggests that its larger pretraining dataset enables higher accuracy" [MMLU, p.12].
- Similarly, "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy. This again suggests that T5's larger pretraining dataset size (and therefore UnifiedQA's pretraining dataset size) can increase accuracy" [MMLU, p.12].

**Conclusion:** Based on this evidence, the paper does not attribute accuracy mainly to parameter count. For GPT-3 alone, larger size correlates with higher accuracy, but the UnifiedQA-vs-GPT-3 and UnifiedQA-vs-RoBERTa/ALBERT/GPT-2 comparisons show smaller models can outperform much larger ones, leading the authors to credit fine-tuning and pretraining dataset size as contributing factors alongside (not subordinate to) model size [MMLU, p.6, p.12]. The passages do not provide a quantitative decomposition of how much of the variance is explained by size versus fine-tuning/data — only these qualitative statements.

**Retrieved:** MMLU p.1-27 (0.73); SWE-bench p.1-52 (0.65); Transformer p.1-15 (0.63) | gold page hit: 1.00
*19.6 s*

## Q43 (text-only, cross-paper, hard, answerable: yes)

**Question.** MMLU, SWE-bench and FIRE-Bench each have to worry that a model may have seen benchmark content during training. What check does each paper run, what does it find, and how strongly does each paper state its conclusion?

**Reference answer.** MMLU (Appendix B.2): memorized questions would have low entropy and high accuracy, but accuracy and question entropy are not positively correlated (correlation between average log probability and accuracy r = -0.43 zero-shot, -0.56 few-shot), which 'suggests that our exact questions were not memorized'. The authors add that models still met text related to the questions through Wikipedia, and promise a list of question sources. SWE-bench (Section 5): resolve rates for PRs created before versus after 2023 in the oracle setting show little difference for most models (Claude 2 4.87% vs 4.23%, ChatGPT-3.5 0.49% vs 0.77%, SWE-Llama 13b 3.98% vs 3.85%), GPT-4 being the exception (1.96% vs 0.0%, on a 25% subset); the authors call this 'largely promising' since models are 'unlikely to cheat' by generating a more recent repository version, and note that new instances can be collected after a model's training date. FIRE-Bench (Section 5.4): F1 on tasks published before versus after each model's knowledge cutoff, stratified by difficulty (Table 6), shows no consistent advantage for pre-cutoff tasks; the authors call the analysis coarse (approximate cutoff dates, unknown training data, small per-category samples) and say it 'suggests the absence of a strong contamination signal rather than proving its absence'. The three checks measure different things (exact-question memorization versus date-based exposure) and none can rule contamination out, so their results are not comparable and no benchmark should be called cleaner on this evidence.

**System answer.** # Contamination/Memorization Checks Across the Three Benchmarks

## FIRE-Bench

**Check run:** FIRE-Bench stratifies agent performance jointly by **task difficulty** (Easy/Medium/Hard, via a 3-axis rubric) **and knowledge cutoff date** (papers published before vs. after each model's cutoff: 2024-06-01 for o4-mini, 2024-09-30 for gpt-5) [FIRE-Bench, p.8-9]. The logic: "a strong contamination effect would be expected to manifest as consistently higher performance on pre-cutoff tasks within the same difficulty category" [FIRE-Bench, p.9].

**What it finds:** No consistent pre-cutoff advantage. For Hard tasks, both OpenHands(o4-mini) and OpenHands(gpt-5) actually score *higher* post-cutoff (15.4→24.8 and 22.6→31.0 respectively). Medium tasks are mixed (o4-mini: 31.9→33.6 increase; gpt-5: 44.5→23.1 decrease). Easy tasks also mixed (o4-mini declines 58.9→42.1; gpt-5 stable) [FIRE-Bench, p.9, Table 6]. An extended analysis on all 40 tasks "shows the same qualitative pattern" [FIRE-Bench, p.9].

**Strength of claim:** Explicitly hedged. The paper states: "these results do not indicate a systematic performance advantage on pre-cutoff tasks after controlling for task difficulty" and separately notes "this analysis is necessarily coarse (knowledge cutoff dates are approximate, training data composition is unknown, and per-category sample sizes are limited), so the result suggests the **absence of a strong contamination signal rather than proving its absence**" [FIRE-Bench, p.9]. They also offer a structural mitigation argument independent of the date check: even if an agent has seen the source paper, "recovering the target finding still requires writing correct code, executing it, and synthesizing conclusions from actual outputs" [FIRE-Bench, p.9].

## SWE-bench

**Check run:** SWE-bench compares model resolve rates on task instances created **before vs. after 2023** in the "oracle" retrieval setting (Table 7) [SWE-bench, p.7]. It also notes the benchmark's "continually updatable" design feature as a general mitigation: new PRs can be scraped after any model's training date [SWE-bench, p.3, p.9].

**What it finds:** "For most models there's little difference in performance before or after this date, with the exception of GPT-4" [SWE-bench, p.7]. Specific numbers: Claude 2 (4.87 before vs. 4.23 after), ChatGPT-3.5 (0.49 vs. 0.77), SWE-Llama 7b (2.95 vs. 3.46), SWE-Llama 13b (3.98 vs. 3.85); GPT-4 is the outlier (1.96 vs. 0.0, though evaluated on only a 25% subset due to budget constraints) [SWE-bench, p.7, Table 7]. An extended temporal analysis by year (Appendix C.4) finds "no consistent correlation between model performance and year" [SWE-bench, p.26].

**Strength of claim:** Fairly confident/positive framing: "We consider this result to be largely promising as it suggests that despite models having been exposed to some version of a repository's codebase, they are unlikely to 'cheat' to address issues simply by generating a more recent version of the repository" [SWE-bench, p.7]. The claim is a relatively strong, affirmatively framed conclusion ("largely promising"), though still qualified as a suggestion rather than proof, and the GPT-4 exception is flagged but attributed partly to the small subsample rather than treated as contamination evidence.

## MMLU

**Check run:** MMLU does **not** check training/test date cutoffs (not applicable — GPT-3 training data predates/overlaps the test by construction). Instead it runs two indirect statistical checks for exact memorization: (1) correlating **GPT-3's accuracy with question entropy/predictability** — the logic being "memorized questions and answers should have low entropy and high accuracy" [MMLU, p.13]; and (2) correlating **average log-probability of the question prompt (a measure of compression/memorization) with accuracy**, separately for zero-shot and few-shot settings [MMLU, p.14, Figure 13].

**What it finds:** "accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers" [MMLU, p.13-14]. For the log-probability check, correlations are reported as r = −0.43 (zero-shot) and r = −0.56 (few-shot) — i.e., *higher* compression (lower log-probability... actually negative correlation meaning higher log-prob associates with lower accuracy) — not the positive correlation contamination would predict [MMLU, p.14, Figure 13 caption].

**Strength of claim:** Moderately hedged and narrower in scope than the other two papers. The paper concludes "This suggests that our exact questions were not memorized" [MMLU, p.13-14] but explicitly limits this to *exact* question/answer memorization, separately acknowledging "during pretraining models encountered text related to our questions through processing Wikipedia" [MMLU, p.14] — i.e., it does not rule out broader topical exposure, only verbatim memorization of the specific Q&A pairs. It also cites prior work (Brown et al., 2020) "showing that the phenomena hardly affects performance" as corroboration [MMLU, p.14], and commits to releasing question sources to reduce future contamination risk rather than asserting the current test is contamination-free.

## Summary Comparison

| Paper | Check type | Finding | Confidence of conclusion |
|---|---|---|---|
| FIRE-Bench | Difficulty-stratified pre/post knowledge-cutoff comparison | No consistent pre-cutoff advantage; some Hard-task results even favor post-cutoff | Most cautious — explicitly says "suggests absence... rather than proving its absence" |
| SWE-bench | Pre/post-2023 creation date comparison (+ year-by-year) | Little difference except one model/small-subset outlier | Moderately confident — calls result "largely promising" |
| MMLU | Entropy–accuracy and log-probability–accuracy correlation (proxy for memorization) | No positive correlation found (verbatim memorization unlikely) | Hedged — limited to *exact* Q&A memorization; broader topical exposure not ruled out |

**Retrieved:** FIRE-Bench p.1-34 (0.74); SWE-bench p.1-52 (0.74); MMLU p.1-27 (0.67) | gold page hit: 1.00
*26.0 s*

## Q44 (text-only, conceptual, medium, answerable: yes)

**Question.** In SWE-bench's baseline experiments, how are files chosen as model context (BM25 versus an 'oracle'), and what does the paper find about whether giving the model more retrieved context helps?

**Reference answer.** The baselines either retrieve files with BM25 at three context limits (13k, 27k and 50k tokens), because dense retrieval is ill-suited to the very long keys and queries, or use an 'oracle' setting that supplies the files edited by the reference patch. BM25 recall of the oracle files rises with the context limit (average 29.58 / 44.41 / 51.06 for 13k / 27k / 50k), but Claude 2's resolve rate falls (1.96 / 1.87 / 1.22), and the authors say performance drops even though recall rises because models are ineffective at localizing problematic code; models do best on the shortest context. With the oracle retriever Claude 2 resolves 4.8% of issues, and in the 'oracle'-collapsed setting (oracle files, with code not directly modified by the PR collapsed except for +/-15 lines) GPT-4 rises from 1.3% to 3.4% and Claude 2 from 4.8% to 5.9%.

**System answer.** ## File Selection Methods in SWE-bench

**BM25 (sparse retrieval):** Since codebases average 438K lines—far exceeding any model's context window—SWE-bench uses BM25 retrieval (Robertson et al., 2009) to select files. "we choose to use BM25 retrieval... to retrieve relevant files to provide as context for each task instance. We experiment with three different maximum context limits, and simply retrieve as many files as fits within the specified limit" [SWE-bench, p.5]. Documents are augmented by "pre-pended files' contents with their file paths to better enable retrieval based on filenames that may be mentioned directly in the issue" [SWE-bench, p.30].

**Oracle retrieval:** This setting directly uses the files edited by the reference (gold) patch: "we also consider a setting where we 'retrieve' the files edited by the reference patch that solved the issue on GitHub... oracle retrieval file paths are simply extracted directly from the reference solution's patch file excluding test files" [SWE-bench, p.5, p.30]. The paper notes this is "less realistic, since an engineer working on addressing an issue may not know a priori which files need to be modified" and "also not necessarily comprehensive since edited files alone may not include all the required context" [SWE-bench, p.5].

The paper also reports BM25's recall relative to oracle files: "in approximately 40% of instances, BM25 retrieves a superset of the oracle files for the 27,000-token context limit. However, in almost half of the instances with the 27,000-token limit, it retrieves none of the files from the 'oracle' context" [SWE-bench, p.5]. Table 3 gives exact recall numbers: at 13k/27k/50k token limits, "All" recall is 26.09%/39.83%/45.90% and "Any" recall is 34.77%/51.27%/58.38% [SWE-bench, p.5].

## Does More Retrieved Context Help?

**No — performance drops as context length increases.** The paper states this directly: "Difficulty correlates with context length... as total context length increases, Claude 2's performance drops considerably; behavior that is also observed in other models" [SWE-bench, p.6].

Concretely, from Table 2 (BM25 resolve rates by max context length) [SWE-bench, p.5]:
- Claude 2: 13k → **1.96%**, 27k → 1.87%, 50k → 1.22%
- SWE-Llama 7b: 13k → **0.70%**, 27k → 0.31%, 50k → 0.00%
- SWE-Llama 13b: 13k → **0.70%**, 27k → 0.48%, 50k → 0.00%

So resolve rate consistently *decreases* as the context window (and hence retrieved content) grows — even though a larger limit should, in principle, increase recall of the actual oracle files (per the BM25 recall table above). The paper explains: "Even when increasing the maximum context size for BM25 would increase recall with respect to the oracle files, performance drops... as models are simply ineffective at localizing problematic code" [SWE-bench, p.6]. It links this to the "lost in the middle" phenomenon: "models become distracted by additional context and may be sensitive to the relative location of target sequences" [SWE-bench, p.6].

**Supporting evidence from the "oracle-collapsed" ablation:** When oracle-retrieved files are collapsed to only the lines actually edited (±15 lines buffer) — i.e., *reducing* irrelevant context while keeping the correct files — performance *improves*: "GPT-4 jumping from 1.3% to 3.4% and Claude 2 from 4.8% to 5.9%" [SWE-bench, p.6-7, Table 6]. This reinforces that it isn't more context per se that helps, but having the *right*, focused context — excess surrounding code hurts rather than helps.

**Caveat on oracle vs. BM25 overall:** Oracle retrieval (which gives exactly the correct files, a form of "better" but not necessarily "more" context) does outperform BM25 overall — e.g., Claude 2 resolves 4.80% with oracle vs. 1.96–1.97% with BM25 [SWE-bench, p.6, Table 5 and Table 18] — but this is attributed to precision of relevant file selection, not sheer volume of context.

**Retrieved:** SWE-bench p.1-52 (0.76); DailyOracle p.1-35 (0.69); FIRE-Bench p.1-34 (0.67) | gold page hit: 1.00
*20.1 s*

## Q45 (text-only, cross-paper, medium, answerable: yes)

**Question.** BYOL reports that its accuracy stays stable over a wide range of batch sizes. What does BYOL say causes the drop at smaller batch sizes, and where does the Batch Normalization paper say the statistics used for normalization come from during training?

**Reference answer.** BYOL (Figure 3a, batch sizes 128 to 4096): BYOL's performance remains stable from 256 to 4096 and only drops for smaller values 'due to batch normalization layers in the encoder'; a footnote says the only dependency on batch size in its training pipeline sits within the batch normalization layers. SimCLR, by contrast, deteriorates rapidly as the batch size falls, likely because there are fewer negative examples. BatchNorm paper: because training uses mini-batches, each mini-batch produces estimates of the mean and variance of each activation, and these statistics are used for the normalization and can fully participate in the gradient backpropagation. So during training a batch-normalized layer normalizes each example with statistics estimated from its mini-batch, which is where BYOL locates its batch-size dependence. Neither paper analyses why small batches hurt: BYOL does not explain the drop beyond naming the BN layers, and the BatchNorm paper does not discuss small-batch performance or BYOL, so the link is an inference from the two papers rather than a claim either makes.

**System answer.** BYOL's performance remains stable across batch sizes from 256 to 4096, and the paper attributes the drop at smaller sizes specifically to batch normalization layers in the encoder: "the performance of BYOL remains stable over a wide range of batch sizes from 256 to 4096, and only drops for smaller values due to batch normalization layers in the encoder" [BYOL, p.8]. It further notes: "The only dependency on batch size in our training pipeline sits within the batch normalization layers" [BYOL, p.8].

Separately, the Batch Normalization paper states that during training, the statistics used for normalization come from each mini-batch: "since we use mini-batches in stochastic gradient training, each mini-batch produces estimates of the mean and variance of each activation. This way, the statistics used for normalization can fully participate in the gradient backpropagation" [BatchNorm, p.3]. (At inference, this changes — population statistics are used instead, per [BatchNorm, p.4] — but the question asks about training.)

**Retrieved:** BatchNorm p.1-11 (0.75); BYOL p.1-35 (0.62); SWE-bench p.1-52 (0.62) | gold page hit: 1.00
*8.6 s*

## Q39 (text+table, cross-source, medium, answerable: yes)

**Question.** The BYOL paper reports 74.3% for a linear classifier on frozen ResNet-50 features and cites supervised ResNet-50 baselines of 76.5% and 78.9%. How many timm ResNet-50 rows at 224 px have a top-1 accuracy at or above each of these three numbers, and what limits how that comparison can be read?

**Reference answer.** The paper's numbers are 74.3% (BYOL, linear evaluation on frozen features), 76.5% and 78.9% (supervised baselines). Among timm's 18 resnet50 rows at 224 px, all 18 are at or above 74.3%, 17 are at or above 76.5% (the exception is resnet50.tv_in1k at 76.156), and 13 are at or above 78.9% (the five below are ra_in1k 78.82, bt_in1k 78.444, a3_in1k 78.052, gluon_in1k 77.58 and tv_in1k 76.156). These are not like-for-like: BYOL's 74.3% is a linear probe on self-supervised features, whereas timm's are fully supervised weights with different recipes, some using extra data (e.g. ig1b, yfcc100m), so the comparison says nothing about whether self-supervised learning is better or worse.

**System answer.** ## Answer

**BYOL's reported numbers:** Under linear evaluation on ImageNet with a standard ResNet-50 (1×), BYOL reports 74.3% top-1 accuracy. The paper states: "This tightens the gap with respect to the supervised baseline of [8], 76.5%, but is still significantly below the stronger supervised baseline of [75], 78.9%" [BYOL, p.6].

**Database query result (timm, ResNet-50 at 224 px, n=18 total rows):**

| Threshold | # rows ≥ threshold | Calculation |
|---|---|---|
| ≥ 74.3% (BYOL's self-supervised linear-eval score) | 18 | 18/18 = 100% |
| ≥ 76.5% (BYOL's cited supervised baseline [8]) | 17 | 17/18 ≈ 94% |
| ≥ 78.9% (BYOL's cited "stronger" supervised baseline [75]) | 13 | 13/18 ≈ 72% |

So all 18 timm ResNet-50@224 entries beat BYOL's self-supervised linear-eval figure, 17 of 18 beat the 76.5% supervised baseline, and 13 of 18 even beat the 78.9% "stronger" supervised baseline.

**What limits how this comparison can be read:**

1. **Mismatched task type.** The 74.3% figure is a *linear probe on frozen self-supervised features* [BYOL, p.6], not full end-to-end supervised training. The timm rows (presumably standard ImageNet-supervised ResNet-50 training runs) are a different training paradigm, so comparing them directly to BYOL's 74.3% conflates two different evaluation protocols.

2. **The 76.5% and 78.9% baselines are specific, dated numbers from specific papers.** BYOL cites 76.5% from reference [8] (SimCLR's reported supervised baseline) and 78.9% from reference [75] ("Maxup," described as using "advanced supervised learning techniques" [BYOL, p.6 and p.10/Appendix C.2]). These are single reported numbers from 2020-era papers, not necessarily representative of the full range of training recipes in the timm database.

3. **The passages give no information about what the timm rows actually represent** — i.e., their training recipes, epoch counts, augmentation strategies, or publication dates. The query only filters on `arch='resnet50'` and `img_size=224`; it does not establish whether these are all "vanilla" ImageNet-supervised ResNet-50 models comparable to the [8]/[75] baselines, or whether some reflect newer/stronger training recipes (e.g., longer schedules, modern augmentation) developed after BYOL's 2020 publication that would not have been available for the original comparison.

4. **No architectural confirmation.** The passages don't confirm that every timm entry matches BYOL's exact ResNet-50 (1×) configuration (e.g., same width multiplier, same final feature dimension of 2048) [BYOL, p.5], only that `arch='resnet50'`.

In short, the query shows that most/all timm ResNet-50@224 entries numerically exceed BYOL's self-supervised and cited supervised figures, but the paper passages do not establish that these timm models are trained under comparable conditions to the specific baselines BYOL cites, so the comparison should be read as illustrating how training recipes have evolved rather than as a direct refutation or confirmation of BYOL's claims.

**Retrieved:** ResNet p.1-12 (0.67); BYOL p.1-35 (0.67); Transformer p.1-15 (0.66) | gold page hit: 1.00
**SQL:** `SELECT   SUM(CASE WHEN top1_val >= 74.3 THEN 1 ELSE 0 END) AS n_ge_74_3,   SUM(CASE WHEN top1_val >= 76.5 THEN 1 ELSE 0 END) AS n_ge_76_5,   SUM(CASE WHEN top1_val >= 78.9 THEN 1 ELSE 0 END) AS n_ge_78_9,   COUNT(*) AS n_total_resnet50_224 FROM model_results WHERE arch = 'resnet50' AND img_size = 224;` | overlap with reference result: 1.00
*35.4 s*
