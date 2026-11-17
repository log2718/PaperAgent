# Report: runs/chunk_paragraph

35 questions, 0 errors, mean latency 18.6 s.

| Source type | Retrieval page hit | SQL value overlap | Answers with abstention wording |
|---|---|---|---|
| text-only | 0.45 (n=21) | - | 15 of 21 |
| table-only | - | 0.71 (n=7) | 0 of 7 |
| text+table | 0.57 (n=7) | 0.78 (n=7) | 5 of 7 |

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

**System answer.** ## How the plain and residual 18/34-layer networks differed in performance

**Plain networks:** The 34-layer plain net performed *worse* than the 18-layer plain net. Specifically, the 34-layer plain network had a higher top-1 error (28.54%) than the 18-layer plain network (27.94%) [ResNet, p.5]. The authors note that "34-layer plain net has higher training error throughout the whole training procedure, even though the solution space of the 18-layer plain network is a subspace of that of the 34-layer one" [ResNet, p.5] — this is the degradation problem.

**Residual networks:** The situation reversed. The 34-layer ResNet outperformed the 18-layer ResNet "by 2.8%" [ResNet, p.5], with error rates of 25.03% (34 layers) vs. 27.88% (18 layers) [ResNet, p.5]. The 34-layer ResNet also "exhibits considerably lower training error and is generalizable to the validation data," indicating the degradation problem was addressed and accuracy gains were obtained from increased depth [ResNet, p.5].

Additionally, even where plain and residual nets were comparably accurate (the 18-layer case), the ResNet converged faster: "the 18-layer ResNet converges faster (Fig. 4 right vs. left)... the ResNet eases the optimization by providing faster convergence at the early stage" [ResNet, p.6].

## Why the authors argue vanishing gradients are not the cause

The authors give several pieces of evidence [ResNet, p.5]:

1. **Batch normalization is used**, which "ensures forward propagated signals to have non-zero variances."
2. They **explicitly verified** that "the backward propagated gradients exhibit healthy norms with BN. So neither forward nor backward signals vanish."
3. The 34-layer plain net **"is still able to achieve competitive accuracy"** (referencing Table 3), which they say "suggest[s] that the solver works to some extent" — i.e., the network isn't simply failing to learn due to dead gradients.

Based on this, they instead **conjecture** that "the deep plain nets may have exponentially low convergence rates, which impact the reducing of the training error," and state that "the reason for such optimization difficulties will be studied in the future" [ResNet, p.5]. They also ruled out more training iterations as a fix: "We have experimented with more training iterations (3×) and still observed the degradation problem, suggesting that this problem cannot be feasibly addressed by simply using more iterations" [ResNet, p.5].

**Retrieved:** ResNet p.5 (0.85); ResNet p.5 (0.84); ResNet p.5 (0.83); ResNet p.6 (0.82); ResNet p.5 (0.82) | gold page hit: 0.50
*16.7 s*

## Q02 (text-only, factual, medium, answerable: yes)

**Question.** In BabyCL's main results (Table 1), how do the Labeled-S 4AFC accuracies of BabyCL (k = 4 and k = 8) compare with the offline CVCL upper bound and with the one-pass and compute-matched streaming baselines, and what do the authors conclude from the compute-matched baseline?

**Reference answer.** Table 1 (4AFC, Labeled-S, mean +/- CI): offline CVCL (i.i.d., 400 epochs, upper bound) 57.31 +/- 1.13; one-pass CVCL (naive streaming) 27.52 +/- 3.12; CL-CVCL (compute-matched) 36.41 +/- 2.31; BabyCL with k=4 41.08 +/- 1.79 and with k=8 43.38 +/- 1.47. Both BabyCL settings beat both streaming baselines (k=8 is 15.86 points above one-pass CVCL and 6.97 above CL-CVCL), k=8 is 2.30 above k=4, and both remain below the offline upper bound (k=8 by 13.93 points). The authors conclude that BabyCL substantially closes but does not match the gap to offline training, and because CL-CVCL is matched in optimization work to BabyCL's gradient budget (at k=8), BabyCL's advantage 'cannot be explained by gradient count alone'.

**System answer.** ## Labeled‑S 4AFC results in Table 1

Two passages report the Table 1 numbers (with the Method‑section table in [2] giving confidence intervals, and the Main‑results text in [4] giving the specific figures discussed by the authors):

| Method | 4AFC accuracy |
|---|---|
| Offline CVCL (i.i.d., 400 epochs) | 57.45% [BabyCL, p.6] (57.31 ± 1.13% in [BabyCL, p.5]) |
| One‑pass CVCL (naive streaming, no replay) | 25.68% [BabyCL, p.6] (27.52 ± 3.12% in [BabyCL, p.5]) |
| CL‑CVCL (compute‑matched replay, ~6× revisitation to match BabyCL k=8) | 35.32% [BabyCL, p.6] (36.41 ± 2.31% in [BabyCL, p.5]) |
| BabyCL (k = 4) | 41.08 ± 1.79% [BabyCL, p.5] |
| BabyCL (k = 8) | 44.46% [BabyCL, p.6] (43.38 ± 1.47% in [BabyCL, p.5]) |

**Comparisons (using the Main‑results figures in [BabyCL, p.6]):**

- **vs. one‑pass streaming:** BabyCL (k=8) beats one‑pass CVCL by 44.46 − 25.68 = **18.78 points**. The text states that one‑pass CVCL "collapses to 25.68%, confirming that a training recipe designed for i.i.d. data does not transfer to streaming" [BabyCL, p.6].
- **vs. compute‑matched CL‑CVCL:** BabyCL (k=8) beats CL‑CVCL by 44.46 − 35.32 = **9.14 points** [BabyCL, p.6].
- **vs. offline CVCL upper bound:** BabyCL (k=8) still trails offline CVCL by 57.45 − 44.46 = **12.99 points** [BabyCL, p.6], i.e., it "substantially closes the gap to offline CVCL... but does not match it."
- **k=4 vs k=8:** The text notes that going from k=4 to k=8 "yields a further 2.6‑point gain" [BabyCL, p.6], consistent with the k=4 vs k=8 difference reported in [BabyCL, p.5] (43.38 − 41.08 = 2.30 points, close to the stated 2.6‑point figure).

## Conclusion drawn from the compute‑matched baseline

The authors specifically designed CL‑CVCL to match BabyCL's gradient/update budget at k=8 (≈6× revisitation per item) while omitting BabyCL's continual‑learning machinery [BabyCL, p.6]. Since CL‑CVCL (35.32%) still falls well below BabyCL (44.46%) despite equal optimization work, the authors conclude that **"the gap cannot be explained by gradient count alone; it reflects the benefit of organizing the stream through event segmentation and of combining visual self‑supervision with cross‑modal grounding"** [BabyCL, p.6]. In other words, BabyCL's advantage over naive compute‑matched replay comes from its continual‑learning structure (event segmentation plus insertion‑synchronized revisitation), not merely from doing more gradient updates.

**Retrieved:** BabyCL p.8 (0.82); BabyCL p.5 (0.81); BabyCL p.6 (0.81); BabyCL p.6 (0.80); BabyCL p.5 (0.80) | gold page hit: 1.00
*33.4 s*

## Q03 (text-only, factual, medium, answerable: yes)

**Question.** How does I-JEPA sample its target and context blocks (number of target blocks, scale and aspect-ratio ranges), and where in the pipeline are the target blocks 'masked'?

**Reference answer.** I-JEPA typically samples M = 4 target blocks, each with random aspect ratio in (0.75, 1.5) and random scale in (0.15, 0.2). The context is a single block with scale in (0.85, 1.0) and unit aspect ratio, from which any region overlapping the targets is removed so the prediction task is non-trivial. The target blocks are obtained by masking the output of the target encoder, not its input, which the paper calls crucial for high-semantic-level targets. The loss is the average L2 distance between predicted and target patch-level representations, and the target encoder is an exponential moving average of the context encoder.

**System answer.** Based on the passages provided:

**Context block sampling:**
I-JEPA samples a **single** context block x from the image, using a random scale in the range **(0.85, 1.0)** and a **unit aspect ratio** [I-JEPA, p.4]. Any regions of this context block that overlap with the (independently sampled) target blocks are removed to avoid a trivial prediction task [I-JEPA, p.4].

**Target block sampling:**
The targets correspond to representations of image blocks. The image is first converted into a sequence of N non-overlapping patches and passed through the target-encoder to get patch-level representations. Then, **M (possibly overlapping) blocks** are randomly sampled from these target representations [I-JEPA, p.3]. The passages provided do not state the specific numeric value of M, nor the scale/aspect-ratio ranges used for sampling the target blocks — this information is not given in the excerpts available.

**Where masking occurs ("masked at the output"):**
A key design choice is that target blocks are obtained by **masking the output of the target-encoder, rather than masking the input image**. That is, the full (unmasked) image y is first passed through the target-encoder to produce patch-level representations sy, and only afterward are the M target blocks selected by masking (indexing) that output with masks Bi [I-JEPA, p.3; p.14]. The ablation in Table 11 confirms this is intentional: if masking is instead applied at the input (forward-propagating through the target-encoder separately for each target region), the resulting targets are less semantic and linear-probing performance is worse [I-JEPA, p.14]. This output-level masking, combined with predicting from abstract representations rather than pixels, is credited with pushing the model toward more semantic representations [I-JEPA, p.2].

**Summary:**
- Context: 1 block, scale ∈ (0.85, 1.0), unit aspect ratio, with target-overlap removed [I-JEPA, p.4].
- Target: M blocks (possibly overlapping), sampled from the *output* representations sy of the target-encoder — i.e., masking is applied after encoding, not to the raw input [I-JEPA, p.3; p.14]. The exact value of M and the scale/aspect-ratio ranges for target blocks are not specified in the given passages.

**Retrieved:** I-JEPA p.4 (0.88); I-JEPA p.3 (0.84); I-JEPA p.14 (0.84); I-JEPA p.2 (0.83); I-JEPA p.17 (0.80) | gold page hit: 1.00
*14.9 s*

## Q04 (text-only, factual, easy, answerable: yes)

**Question.** How are Daily Oracle's question-answer pairs generated and filtered, and how many True/False and multiple-choice questions are in the subset analysed in the paper?

**Reference answer.** The analysed subset has 16,783 True/False and 14,727 multiple-choice questions generated from daily news articles from January 2020 to December 2024. Each day six articles are selected (three random, three from hot topics) and an LLM generates two TF and two MC pairs per article with few-shot prompting. Construction has four steps: article summary (focused on new events so the publication date can be the resolution date), QA generation, misleading-choice generation for MC, and QA filtering. In filtering, an LLM scores seven principles from 0 to 2 points each and only questions with at least 13 points are kept.

**System answer.** ## Generation and Filtering Process

Daily Oracle's QA pairs are produced through an **LLM-based dataset construction pipeline** that automatically generates forecasting questions from **daily news articles** [DailyOracle, p.3]. The dataset is built via a **"four-step construction process"** (described in Section 3.1 of the paper), though the passages provided here do not detail each of the four steps individually [DailyOracle, p.3].

One of the steps in this pipeline is a **"QA Filtering" step**, in which an **LLM-based evaluator** checks each QA pair against **seven filtering principles** (listed in Appendix A.3, not included in the provided passages) [DailyOracle, p.14].

To verify the quality/reliability of this LLM-based filtering, the authors conducted a **human evaluation**: four human annotators independently reviewed a randomly sampled subset of 30 TF and 30 MC QA pairs, following the same instructions given to the LLM evaluator, and assessed each pair against the same seven filtering principles [DailyOracle, p.14].

The questions themselves are True/False (TF) and Multiple Choice (MC) questions spanning categories such as business, politics, and arts, and are designed to test LLMs' ability to predict future events from their existing knowledge (i.e., temporal generalization/forecasting ability), rather than reading comprehension [DailyOracle, p.1].

## Size of the Subset Analyzed in the Paper

The subset used for the paper's analysis consists of:
- **16,783 True/False (TF) QA pairs**
- **14,727 Multiple Choice (MC) QA pairs**

covering daily news from **January 1, 2020, to December 31, 2024**, averaging **17.2 questions per day** [DailyOracle, p.4; DailyOracle, p.3].

(Note: The full Daily Oracle dataset is continuously updated daily and continues generating new questions beyond this subset; the table total cited elsewhere is 31,510 questions for this analyzed period [DailyOracle, p.3].)

**What the evidence does not establish:** The specific sub-steps of the "four-step construction process" and the full list/content of the "seven filtering principles" are referenced but not spelled out in the passages provided, so I cannot describe those details further without additional source text.

**Retrieved:** DailyOracle p.4 (0.80); DailyOracle p.3 (0.79); DailyOracle p.1 (0.79); DailyOracle p.3 (0.78); DailyOracle p.14 (0.73) | gold page hit: 1.00
*14.1 s*

## Q06 (text-only, conceptual, medium, answerable: yes)

**Question.** What three desiderata do the Transformer authors use to motivate self-attention over recurrent and convolutional layers, how does a self-attention layer compare on each, and when is it cheaper per layer than a recurrent layer?

**Reference answer.** The desiderata are (1) total computational complexity per layer, (2) the amount of computation that can be parallelised (minimum number of sequential operations) and (3) the path length between long-range dependencies. Per Table 1, self-attention has O(n^2*d) complexity per layer, O(1) sequential operations and O(1) maximum path length; recurrent layers have O(n*d^2), O(n) and O(n); convolutional layers have O(k*n*d^2), O(1) and O(log_k n). Self-attention is faster than a recurrent layer when the sequence length n is smaller than the representation dimensionality d, which is typical for sentence representations in machine translation. For very long sequences the authors suggest restricting attention to a neighbourhood of size r (path length O(n/r)) but leave this to future work.

**System answer.** Based on the provided passages, the Transformer paper lists the desiderata and partial comparisons as follows:

**Three desiderata** [Transformer, p.6, section 4 Why Self-Attention]:
1. "the total computational complexity per layer"
2. "the amount of computation that can be parallelized, as measured by the minimum number of sequential operations required"
3. A third desideratum is referenced ("we consider three desiderata") but its specific content is **not given** in the supplied passages — only the first two are explicitly named in passage [3].

**Comparison on parallelization** [Transformer, p.6]: "a self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations." So on the "minimum sequential operations" desideratum, self-attention is O(1) versus O(n) for recurrence.

**Comparison on computational complexity per layer / when cheaper than recurrent**: Passage [2] states "self-attention layers are faster than recurrent layers when the sequence..." — the sentence is cut off in the passage provided, so the exact condition (the specific sequence-length threshold or relation to representation dimension) **is not given** in the evidence supplied.

**Summary of what the evidence does and does not establish:**
- It establishes two of the three desiderata (per-layer computational complexity; parallelizability via minimum sequential operations) [Transformer, p.6].
- It establishes that self-attention requires O(1) sequential operations vs. O(n) for recurrent layers [Transformer, p.6].
- It does **not** fully establish the third desideratum, nor does it give the complete condition under which self-attention is cheaper per layer than a recurrent layer, since the relevant sentence in passage [2] is truncated before the condition is stated. The evidence given is insufficient to answer these two parts fully.

**Retrieved:** ViT p.10 (0.79); Transformer p.6 (0.77); Transformer p.6 (0.76); Transformer p.2 (0.76); ViT p.8 (0.75) | gold page hit: 0.50
*12.6 s*

## Q07 (text-only, conceptual, hard, answerable: yes)

**Question.** BYOL trains without negative pairs. What mechanisms does the paper credit with preventing representation collapse, and what do its ablations show about them?

**Reference answer.** BYOL trains an online network (encoder, projector, predictor) to predict the projection of a second augmented view produced by a target network whose weights are an exponential moving average of the online weights; the loss gradient is not propagated into the target (stop-gradient) and the predictor exists only on the online branch. The authors hypothesise that the combination of the predictor and the slow-moving-average target avoids collapse, but they state the dynamics still admit undesirable equilibria that they did not observe in experiments. In the ablation (Table 5b), the only variant that performs well without negatives is BYOL with both a target network and a predictor; the representation collapses when either is removed. They also found that the target network can be removed without collapse if the predictor is kept near-optimal (e.g., higher predictor learning rate), suggesting that keeping the predictor near-optimal may be one role of the target network.

**System answer.** ## Mechanisms Credited with Preventing Collapse

The paper explicitly hypothesizes that collapse is avoided by the **combination of two mechanisms**:

1. **The addition of a predictor to the online network**
2. **The use of a slow-moving average of the online parameters as the target network**

As stated: "We hypothesize (see Section 3.2) that the combination of (i) the addition of a predictor to the online network and (ii) the use of a slow-moving average of the online parameters as the target network encourages encoding more and more information within the online projection and avoids collapsed solutions." [BYOL, p.2, Abstract]

The paper further notes that BYOL "does not use an explicit term to prevent collapse (such as negative examples)," yet empirically does not converge to collapsed solutions, and that the target network's updates are importantly *not* in the direction of the gradient of the loss with respect to the target parameters ξ — i.e., ξ is not simply minimizing the same loss as θ: "BYOL's target parameters ξ updates are not in the direction of ∇ξLBYOL" [BYOL, p.4, section 3.1].

## What the Ablations Show

The ablation study (Section 5) directly tests the necessity of these two components by varying whether a bootstrap target network and a predictor are present, and whether negative pairs (controlled by a coefficient β) are added back in:

- **"The only variant that performs well without negative examples (i.e., with β = 0) is BYOL, using both a bootstrap target network and a predictor."** [BYOL, p.9] — This indicates that removing either the target network's moving-average or the predictor (while keeping β=0) causes the method to fail, confirming both components are necessary together to prevent collapse without negative pairs.

- **"Adding the negative pairs to BYOL's loss without re-tuning the temperature parameter hurts its performance."** [BYOL, p.9] — showing negative pairs aren't needed and can even be counterproductive if not carefully tuned.

- However, the paper also notes that negative pairs *can* be added back and still match BYOL's performance with proper tuning: **"we show that we can add back negative pairs and still match the performance of BYOL with proper tuning of the temperature."** [BYOL, p.9] — This suggests negative pairs are not essential; they can substitute for but don't improve upon the predictor/target-network mechanism.

## Summary

The passages establish that collapse avoidance is attributed to the **predictor + slow-moving-average target network** combination, not to any explicit anti-collapse term. Ablations support this by showing BYOL only performs well without negative pairs when *both* of these components are present together [BYOL, p.9]. The evidence given does not provide the detailed numerical ablation results (e.g., specific accuracy drops when removing the predictor or target network individually), only the qualitative conclusion stated above.

**Retrieved:** BYOL p.2 (0.76); BYOL p.4 (0.74); BYOL p.1 (0.74); BYOL p.9 (0.74); BYOL p.10 (0.73) | gold page hit: 0.80
*12.8 s*

## Q08 (text-only, conceptual, medium, answerable: yes)

**Question.** What evidence does the Batch Normalization paper give that batch normalization reduces internal covariate shift, how large is the training speed-up it reports on ImageNet (and what else was changed besides adding BN), and what does the paper itself say it has not established?

**Reference answer.** The paper defines internal covariate shift as the change in the distribution of network activations due to the change in network parameters during training. Its direct evidence is a small MNIST experiment (three sigmoid hidden layers): the input distribution to a typical sigmoid unit is much more stable with BN and the BN network has higher test accuracy (Fig. 1). On ImageNet the evidence is indirect, through the speed and accuracy of BN-Inception variants: BN-Baseline matches Inception's 72.2% in 13.3M steps versus 31.0M, BN-x5 needs 2.1M steps (stated as 14 times fewer), BN-x30 reaches 74.8%, and BN-x5-Sigmoid reaches 69.8% while Inception with sigmoid never beats 1/1000 accuracy. The BN-x5/x30 speed-ups combine BN with other changes (a 5x or 30x larger initial learning rate, Dropout removed, L2 weight cut 5x, learning rate decayed 6x faster, Local Response Normalization removed, more thorough shuffling, fewer photometric distortions), so they are not an isolated measure of BN. The paper frames the mechanism as an expectation and conjecture: it 'expects' fixed input distributions to speed training, 'conjectures' that BN may bring layer Jacobian singular values close to 1, and says the precise effect of BN on gradient propagation remains an area of further study.

**System answer.** Based on the passages provided, here is what can be established and what cannot:

**Evidence that BN reduces internal covariate shift**

The passages do not contain a direct empirical demonstration (e.g., measured statistics showing reduced shift in activations). What they do provide is the paper's conceptual/mechanistic claim:

- The paper defines internal covariate shift as "the change in the distributions of internal nodes of a deep network, in the course of training" and states that Batch Normalization "takes a step towards reducing internal covariate shift... via a normalization step that fixes the means and variances of layer inputs" [BatchNorm, p.2].
- In the conclusion, it reiterates that the method "is based on the premise that covariate shift, which is known to complicate the training of machine learning systems, also ap[plies]..." [BatchNorm, p.7] (sentence is cut off in the passage).

**This evidence does not establish an empirical measurement of reduced covariate shift** — the passages only show the paper's stated mechanism and premise, not actual experimental evidence (e.g., any measured statistics or comparison plots showing shift reduction).

**Training speed-up on ImageNet, and what else changed**

The abstract states: "Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps, and beats the original model by a significant margin" [BatchNorm, p.1].

So the reported speed-up is **14×** fewer training steps to reach the same accuracy.

Regarding "what else was changed besides adding BN": the passages mention generally that BN "allows us to use much higher learning rates and be less careful about initialization" and "regularizes the model and reduces the need for Dropout" [BatchNorm, p.2], implying such changes are part of how the accelerated model is used. However, **the passages do not specify concretely what other modifications (e.g., exact learning rate increase, removal of Dropout) were made in the specific ImageNet experiment that produced the 14× figure.** That detail is not established by the evidence given.

**What the paper itself says it has not established**

None of the provided passages contain an explicit statement by the authors about limitations or claims they have *not* established. The evidence given does not address this part of the question at all — no passage contains language such as "we have not shown" or similar caveats.

**Retrieved:** BatchNorm p.7 (0.89); BatchNorm p.1 (0.88); BatchNorm p.2 (0.87); ViT p.11 (0.84); ResNet p.9 (0.83) | gold page hit: 0.50
*22.1 s*

## Q09 (text-only, conceptual, hard, answerable: yes)

**Question.** According to the Temporal Straightening paper, why should reducing the curvature of latent trajectories make gradient-based planning easier, and do the paper's experiments generally show planning improving when the curvature regularizer is used?

**Reference answer.** Explanation (the main part). Planning minimises a Euclidean goal cost in latent space, and when latent trajectories are highly curved, straight-line distance misrepresents the geodesic distance along feasible transitions. A curvature regulariser (it penalises the angle between consecutive latent velocity vectors, i.e. maximises their cosine similarity, while a JEPA-style predictor is trained with stop-gradient on the target) straightens trajectories, which makes Euclidean latent distance a better proxy for geodesic distance and improves the conditioning of the planning objective. The theory covers linear latent dynamics: epsilon-straight transitions control the condition number of the planning Hessian, so gradient descent converges linearly at a rate set by the condition number; guarantees for nonlinear predictors are left to future work. As an illustration, the loss landscape is closer to convex after straightening (Figure 4). Experiments (general trend only). Yes: the paper reports open-loop planning success improving by 20-60% and MPC by 20-30% with a simple gradient-based planner, and says it observes a significant improvement across all models and environments. The improvement is not uniform in Table 1 (for example a from-scratch ResNet 1x384 on PointMaze-UMaze falls from 82.00 to 52.00 open-loop), so 'generally' is the right strength, in simulated goal-reaching tasks.

**System answer.** ## Why reducing curvature should help gradient-based planning

The paper's core argument is that straightening latent trajectories makes **Euclidean distance in latent space a better proxy for geodesic distance**, which in turn **improves the conditioning of the planning objective** [TemporalStraightening, p.1, Abstract]. Specifically:

- The authors state they "prove that reducing curvature improves convergence of gradient-based planners" [TemporalStraightening, p.2, section 1. Introduction].
- With straighter trajectories, "the Euclidean distance is closer to the geodesic distance," and since MSE is squared Euclidean distance, it "becomes a more useful planning cost function that can reflect the true progress towards the target" [TemporalStraightening, p.22, section E.1/E.2]. A planning cost that accurately reflects true progress toward the goal gives more informative gradients, which should make gradient-based optimization of the plan more stable/well-conditioned.
- This is echoed in the conclusion: "In this straightened representation space, the Euclidean distance provides a more reliable proxy for the geodesic distance and gradient-based planning is better conditioned" [TemporalStraightening, p.9, section 6. Conclusion].

So the causal chain claimed is: curvature regularization → straighter latent trajectories → Euclidean distance ≈ geodesic distance → better-conditioned (more informative) planning cost landscape → easier/more stable gradient-based optimization.

## Do the experiments generally show improvement?

Yes, according to the passages, the empirical results support this:

- "The resulting encoded trajectories are significantly straighter, with Euclidean distances better aligned with geodesic distances (Figure 2)... we observe superior empirical gains across a suite of goal-reaching tasks: **open-loop planning success improves by 20–60% and MPC by 20–30%** with a simple gradient-based planner" [TemporalStraightening, p.2, section 1. Introduction].
- The abstract similarly claims that temporal straightening "makes gradient-based planning more stable and yields significantly higher success rates across a suite of goal-reaching tasks" [TemporalStraightening, p.1, Abstract].
- The conclusion reiterates "significant and consistent gains over baselines" across "a range of 2D goal-reaching tasks" [TemporalStraightening, p.9, section 6. Conclusion].

**Caveat on evidence scope:** The passages provided only give summary-level claims (abstract, introduction, conclusion) and a qualitative visualization description (p.22); none of the provided passages include the actual quantitative tables/figures breaking down results by environment or ablation (e.g., with vs. without the curvature regularizer specifically, isolated from the base JEPA objective). So while the text explicitly asserts consistent improvements, the passages given do not show the underlying numeric experimental tables themselves — only the paper's narrative summary of those results.

**Retrieved:** TemporalStraightening p.1 (0.88); TemporalStraightening p.2 (0.86); TemporalStraightening p.9 (0.86); TemporalStraightening p.22 (0.81); TemporalStraightening p.19 (0.81) | gold page hit: 0.29
*13.0 s*

## Q11 (text-only, cross-paper, medium, answerable: yes)

**Question.** ViT says it follows the original Transformer 'as closely as possible'. Which parts of the Transformer encoder does ViT keep, and how does its encoder differ from the one in 'Attention Is All You Need' (input handling, position information, normalisation placement, feed-forward activation)?

**Reference answer.** ViT keeps the Transformer encoder structure of alternating multi-head self-attention and position-wise MLP/feed-forward blocks with residual connections and layer normalisation, and uses the encoder only. Differences: (1) input - ViT splits an image into patches, linearly projects them and prepends a learnable [class] token, whereas the Transformer embeds discrete input tokens; (2) position information - ViT uses standard learnable 1D position embeddings, the Transformer uses fixed sinusoidal encodings (though it found learned embeddings nearly identical); (3) normalisation - the Transformer computes LayerNorm(x + Sublayer(x)) after the residual addition, while ViT applies layer norm before every block and residual connections after every block; (4) the feed-forward layer uses ReLU in the Transformer and GELU in ViT. The Transformer paper additionally has a decoder with encoder-decoder attention.

**System answer.** Based on the passages provided, the evidence only partially supports this question, and several specific points (normalisation placement and feed‑forward activation) are **not established** by what's given. Here is what the passages do and do not show:

**What the Transformer encoder structure ViT keeps (partially supported):**
- I-JEPA's description of ViT states "A ViT is composed of a stack of transformer layers, each consisting of a self-attention [66] operation followed by a fully-connected MLP" [I-JEPA, p.3]. This indicates ViT retains the core transformer-layer structure (self-attention → MLP) from the original Transformer encoder, but this detail comes from the I-JEPA paper's description of ViT, not from the ViT paper itself.

**Input handling (supported by ViT passage):**
- The ViT paper explains that, unlike the original Transformer which receives "a 1D sequence of token embeddings," ViT must handle 2D images, so it reshapes the image into a sequence of flattened 2D patches and maps them to a constant latent dimension D via "a trainable linear projection," producing what it calls "patch embeddings" [ViT, p.3]. This is the key input-handling difference the passage documents: patch-based linear projection instead of token embeddings.

**Position information (partially supported):**
- The ViT ablation study (D.4) discusses comparing different positional-embedding strategies, noting "there is a large gap between the performances of the model with no positional embedding and models with positional embedding, [but] there is little to no difference between different ways of encoding positional information" [ViT, p.18]. This tells us ViT uses learnable positional embeddings and that the specific encoding scheme matters little empirically, but the passage does **not** explicitly contrast this with the original Transformer's sinusoidal positional encoding scheme, so a direct comparison on "how it differs" from Vaswani et al.'s approach is not established by this evidence.

**Normalisation placement and feed-forward activation (not supported):**
- None of the five passages provided mention LayerNorm placement (e.g., pre-norm vs. post-norm) or the activation function used in the feed-forward/MLP block (e.g., GELU vs. ReLU) for either ViT or the original Transformer. The Transformer passage [4] only discusses the three applications of multi-head attention (including encoder-decoder attention), not normalization or activation details. Therefore, the evidence does **not** establish any claim about these two aspects.

**Summary of what the evidence establishes vs. does not:**
- Established: ViT retains the self-attention + MLP transformer-layer stack [I-JEPA, p.3]; ViT's key input difference is patch-based linear projection instead of 1D token embeddings [ViT, p.3]; ViT adds positional embeddings, and the specific encoding method matters little [ViT, p.18].
- Not established by these passages: the "as closely as possible" quote itself, and any details on normalisation placement or feed-forward activation functions in ViT's encoder versus the original Transformer encoder.

**Retrieved:** I-JEPA p.3 (0.77); ViT p.18 (0.75); ViT p.3 (0.75); Transformer p.5 (0.74); ViT p.20 (0.74) | gold page hit: 0.33
*20.3 s*

## Q12 (text-only, cross-paper, hard, answerable: yes)

**Question.** MAE and I-JEPA both mask parts of an image and use a ViT encoder on the visible part. What does each method predict and with what loss, and what evidence does the I-JEPA paper give that predicting in representation space matters?

**Reference answer.** MAE reconstructs the pixel values of the masked patches with a lightweight decoder (mean squared error computed only on masked patches); the encoder sees only visible patches and normalised pixels work slightly better (Table 1d, ViT-L/16: 85.4 vs 84.9 fine-tuning, 73.9 vs 73.5 linear probing). I-JEPA is non-generative: a predictor (narrow ViT) predicts the representations of target blocks from a context block, the targets come from a target encoder that is an exponential moving average of the context encoder, and the loss is average L2 distance in representation space. In I-JEPA's own ablation (Table 7, ViT-L/16, linear probe on 1% of ImageNet labels), using target-encoder outputs gave 66.9 top-1 versus 40.7 when the loss was in pixel space, and the authors say they 'conjecture' representation-space loss is a crucial component. I-JEPA also reports about 7% slower iterations than MAE but roughly 5x fewer iterations to converge. Caveat: the pixel-space variant is I-JEPA's own ablation (different epochs: 500 vs 800), not the MAE paper's setup, and MAE does not test representation-space targets.

**System answer.** Based on the passages:

**MAE (as referenced in the I-JEPA paper):**
The passages don't give a detailed technical description of MAE's loss function, but I-JEPA p.2 characterizes MAE as one of the "generative methods that predict in pixel/token space" [I-JEPA, p.2]. This implies MAE's prediction target and loss are computed directly on raw pixels, in contrast to I-JEPA's representation-space approach. The passages do not state MAE's exact loss formula (e.g., L1/L2 reconstruction loss), so that specific detail is not established by this evidence.

**I-JEPA:**
I-JEPA predicts in **representation (embedding) space**, not pixel space. As stated: "a crucial component of I-JEPA is that the loss is computed entirely in representation space, thereby giving the target encoder the ability to produce abstract prediction targets, for which irrelevant pixel-level details are eliminated" [I-JEPA, p.7]. Relatedly, I-JEPA "makes use of abstract prediction targets for which unnecessary pixel-level details are potentially eliminated, thereby leading the model to learn more semantic features" [I-JEPA, p.2]. The targets themselves are produced by masking the **output of a target-encoder** (rather than masking the input), which the paper shows "results in more semantic prediction targets and improves linear probing performance" [I-JEPA, p.14].

**Evidence that predicting in representation space matters:**
The paper runs a direct ablation (Table 7) comparing the same I-JEPA setup when the loss is computed in pixel space versus in representation space, evaluated via linear probing on 1% of ImageNet-1K. The result: "predicting in pixel-space leads to a significant degradation in the linear probing performance" [I-JEPA, p.7]. The passages do not give the exact numeric values from Table 7, so I can't report the precise magnitude of the degradation — only that the paper describes it as "significant."

**Summary comparison:**
- MAE → predicts pixel/token-level content (implied generative, pixel-space target) [I-JEPA, p.2]; exact loss formula not given in these passages.
- I-JEPA → predicts target-encoder output representations (abstract, semantic targets, masked at the output rather than input) [I-JEPA, p.2; p.14], with loss computed entirely in representation space [I-JEPA, p.7].
- Supporting evidence: I-JEPA's own ablation (Table 7) shows pixel-space loss significantly degrades 1% ImageNet-1K linear-probe performance compared to representation-space loss [I-JEPA, p.7], and masking the target-encoder's output (rather than its input) similarly improves semantic quality of learned representations [I-JEPA, p.14].

**Retrieved:** I-JEPA p.2 (0.78); I-JEPA p.14 (0.78); I-JEPA p.7 (0.78); I-JEPA p.5 (0.77); I-JEPA p.5 (0.77) | gold page hit: 0.22
*16.9 s*

## Q13 (text-only, cross-paper, hard, answerable: yes)

**Question.** Distillation and BYOL both train one network to match another network's outputs. According to the two papers, what supplies the targets in each case and how does that target model come about, are labels used, and what does BYOL say about the 'mean teacher' method that it treats as closest to its slow-moving-average target?

**Reference answer.** Distillation: the targets are class probabilities from an already-trained 'cumbersome' model (an ensemble, or a single very large model trained with a strong regularizer such as dropout), softened by raising the softmax temperature. The small model is trained at the same high temperature on a transfer set and uses temperature 1 afterwards; when labels are known the objective is a weighted average of cross-entropy with the soft targets and with the correct labels, with a considerably lower weight on the label term. BYOL: the targets are the projections a target network produces for a second augmented view; the target's weights are an exponential moving average of the online network's weights (a slow-moving average of the learner itself, not a separately trained larger model), the loss gradient is not propagated into the target (stop-gradient), and an extra predictor sits only on the online branch. BYOL is a self-supervised method that works without negative pairs. BYOL describes mean teacher (MT) as also using a slow-moving-average 'teacher' to produce targets for an online 'student', with an l2 consistency loss between their softmax predictions added to a classification loss; it reports that a similar approach collapses when the classification loss is removed, whereas BYOL's added predictor prevents collapse.

**System answer.** ## Where the targets come from

**Distillation:** The targets are produced by a *cumbersome model*—in the reported experiment, an **ensemble of 10 models**—rather than by a self-referential copy of the student network. The paper states that "our distillation approach is able to extract more useful information from the training set than simply using the hard labels to train a single model" and that improvements the 10-model ensemble achieves (in frame classification accuracy and WER) are largely transferred to the distilled model [Distillation, p.5]. This passage contrasts two uses of labels: (1) training a single model directly on the **hard labels**, versus (2) distilling knowledge from the ensemble. The evidence given does not state whether the ensemble members themselves were trained with hard labels or whether the distilled (student) model also uses hard labels alongside the distillation targets—only that the alternative to distillation is "using the hard labels to train a single model" [Distillation, p.5]. So the passage establishes that distillation targets come from an ensemble of separately-trained models, but it does not fully specify the labeling regime for either the ensemble or the student beyond this comparison.

**BYOL:** The targets come from a **target network** that has the same architecture as the online network but a different set of weights ξ. Critically, ξ is **not independently trained**—it is an **exponential moving average (EMA) of the online network's own weights θ**, updated after every training step according to a decay rate τ ∈ [0,1] [BYOL, p.3]. This is a purely self-referential ("bootstrap") mechanism: the online network fθ/gθ/qθ is trained to predict the output of a slowly-evolving copy of itself. Nothing in the provided passages indicates that labels are used to produce these targets—the target network's weights derive entirely from the online network's own parameter history [BYOL, p.3].

## Labels

- Distillation: hard labels are referenced only as the baseline alternative to distillation ("using the hard labels to train a single model") [Distillation, p.5]; the provided passage does not describe labels being used to generate the distillation targets themselves—those come from the ensemble's outputs.
- BYOL: no labels are involved in producing the target-network outputs; the target is purely an EMA of the online network's weights [BYOL, p.3].

## BYOL on "mean teacher" (its closest slow-moving-average analogue)

BYOL explicitly discusses Mean Teacher (MT) as a related slow-moving-average method: "mean teacher (MT) ... also uses a slow-moving average network, called teacher, to produce targets for an online network, called student. An ℓ2 consistency loss between the softmax predictions of the teacher and the student is added to the classification loss" [BYOL, p.3]. BYOL notes that while MT is effective in the **semi-supervised** setting (where labels are available via the classification loss), "a similar approach collapses when removing the classification loss" [BYOL, p.3]—i.e., without labels, an MT-style teacher/student setup degenerates to a trivial solution. BYOL's key claim is that it avoids this collapse purely through architecture: "BYOL introduces an additional predictor on top of the online network, which prevents collapse" [BYOL, p.3], allowing it to learn without any labels or classification loss, unlike MT.

## Summary comparison

| | Target source | How target model arises | Labels used for targets? |
|---|---|---|---|
| Distillation | Ensemble of 10 models | Separately trained cumbersome models | Baseline comparison uses hard labels; ensemble's role as target generator doesn't require labels per the distillation step itself (not fully specified in passages) [Distillation, p.5] |
| BYOL | Target network (EMA of online network) | Self-generated via exponential moving average of the online network's own weights θ, τ∈[0,1] | No labels; purely self-supervised [BYOL, p.3] |
| Mean Teacher (BYOL's comparison) | Teacher network (EMA of student) | Same EMA mechanism as BYOL | Yes—relies on a classification loss with labels; collapses without it, unlike BYOL which uses a predictor instead [BYOL, p.3] |

**Retrieved:** BYOL p.3 (0.78); BYOL p.3 (0.77); BYOL p.3 (0.77); Distillation p.5 (0.75); BYOL p.3 (0.75) | gold page hit: 0.17
*22.7 s*

## Q14 (text-only, cross-paper, medium, answerable: yes)

**Question.** Temporal Straightening's world model uses a ResNet encoder, a ViT predictor and stop-gradient on the target latent. What does the Straightening paper say about how it uses each, and what does each originating paper (ResNet, ViT, BYOL) say that the component is designed to do?

**Reference answer.** Temporal Straightening offers two encoder setups, one being a ResNet (He et al.) trained from scratch, and uses a ViT (Dosovitskiy et al.) as the dynamics predictor with a temporal causal attention mask for frame-level autoregressive prediction. For collapse prevention it applies stop-gradient to the target latent in the prediction loss, citing Grill et al. 2020 (the BYOL paper) among stop-gradient methods, chosen because it needs no negative samples or extra hyper-parameters; it concedes collapse is still possible in theory but says stop-gradient worked in its experiments. In the originating papers: ResNet introduces residual learning, letting stacked layers fit F(x) = H(x) - x via shortcut connections to ease optimisation of deeper networks (the degradation problem); ViT processes a sequence of image-patch embeddings with a standard Transformer encoder of alternating self-attention and MLP blocks; and BYOL trains an online network to predict a stop-gradient target network's representation without negative pairs, which it hypothesises depends on both a predictor and a slow-moving-average target (its representation collapses if either is removed).

**System answer.** The provided passages do not contain the information needed to fully answer this question. Specifically:

**What the Temporal Straightening passages actually show:**

- The paper describes jointly learning "an encoder and a predictor of a Joint-Embedding Predictive Architecture (JEPA) world model" using "a curvature regularizer that encourages locally straightened latent trajectories" [TemporalStraightening, p.1].
- The hyperparameter table lists a "Projector/ResNet" learning rate (1e-5, or 1e-6 "for no straightening") and a separate "Predictor lr" (5e-4), along with an "Action/Prop encoder lr" (5e-4) [TemporalStraightening, p.14]. This confirms a ResNet component and a separate predictor component are used, but the passage does not specify the predictor's architecture (i.e., it does not state the predictor is a ViT).
- Figure 16's caption (p.21) lists several encoder/ablation variants used in heatmap comparisons — e.g., "DINOv2 CLS embedding," "DINOv2 patch embedding," "ResNet - spatial," "ResNet - global" — but these are ablation configurations, not a statement that the main model's predictor is a ViT [TemporalStraightening, p.21].

**What is missing from the given passages:**

- None of the five passages explicitly state that the predictor is a ViT, nor do they mention or describe the use of a stop-gradient operation on the target latent anywhere in the excerpts provided.
- None of the passages quote or summarize the original ResNet, ViT, or BYOL papers' stated design purposes for these components (e.g., ResNet's residual-learning motivation, ViT's patch-based attention design, or BYOL's stop-gradient/momentum-target rationale). These three "originating papers" are not among the passages supplied at all.

**Conclusion:** Based solely on the evidence given, I can confirm that Temporal Straightening uses a ResNet-based projector/encoder and a separate predictor within a JEPA world model [TemporalStraightening, p.1; p.14], but the passages do not establish (a) that the predictor is specifically a ViT, (b) that stop-gradient is applied to the target latent, or (c) any content from the original ResNet, ViT, or BYOL papers describing what those components are designed to do. To answer the full question, additional passages from the paper's architecture section (not provided here) and from the ResNet, ViT, and BYOL papers themselves would be needed.

**Retrieved:** TemporalStraightening p.1 (0.78); TemporalStraightening p.14 (0.78); TemporalStraightening p.3 (0.78); TemporalStraightening p.19 (0.78); TemporalStraightening p.21 (0.78) | gold page hit: 0.00
*21.3 s*

## Q15 (text-only, cross-paper, hard, answerable: yes)

**Question.** BabyCL's visual branch applies strong augmentations to two views of each frame. Compare the Gaussian-blur and solarization probabilities it uses for its two views with those BYOL uses for its two views, and say what the two papers report about whether negative pairs are needed.

**Reference answer.** BabyCL (Appendix A): two views per frame with strong augmentation: random resized crop to 224x224 (scale 0.2-1.0), horizontal flip, color jitter, random grayscale (0.2), Gaussian blur with probability 1.0 on view 1 and 0.1 on view 2, and solarization on view 2 with probability 0.2. BYOL (Appendix B, Table 6): Gaussian blur probability 1.0 for the first view (T) and 0.1 for the second (T'), solarization 0.0 for T and 0.2 for T', color dropping (grayscale) 0.2 for both, crops covering 8%-100% of the image. The blur, solarization and grayscale probabilities therefore match, while the lower bound of the crop scale differs (0.2 versus 8%), and BabyCL does not cite BYOL for these settings. Negatives: BabyCL's instance loss is a SimCLR objective and its cross-modal loss a symmetric InfoNCE, and it cites Zhuang et al. (2021) as finding that contrastive methods with negative sampling are most effective on SAYCam. BYOL reports state-of-the-art ImageNet results without negative pairs and finds it much less affected than SimCLR when color distortion is removed from the augmentations. Neither paper tests a BYOL-style objective in a streaming child-egocentric setting.

**System answer.** ## Gaussian-blur and solarization probabilities

**BabyCL's visual branch** (two augmented views per frame):
- Gaussian blur: applied with probability **1.0 on view 1** and probability **0.1 on view 2**
- Solarization: applied **only on view 2**, with probability **0.2** (no solarization on view 1)
[BabyCL, p.14]

**BYOL's two views** — the passage only gives numbers for a *symmetric-parameter ablation* the authors ran for comparison purposes, not their main baseline config:
- Gaussian blur: probability **0.5 for both T and T′** (i.e., both views)
- Solarization: probability **0.2 for both T and T′** (i.e., both views)

The text notes this symmetric ablation "recover[s] very similar results compared to our baseline choice of parameters," implying the actual baseline (presumably asymmetric, like BabyCL's) differs, but the baseline's exact per-view probabilities are not given in this passage [BYOL, p.26].

**Comparison:** Where BabyCL applies asymmetric blur/solarization across its two views (blur 1.0/0.1; solarization 0/0.2), the BYOL numbers available here are from a *symmetric* ablation (blur 0.5/0.5; solarization 0.2/0.2 for both views) rather than BYOL's default per-view split, so a precise like-for-like comparison of BYOL's actual baseline view-1/view-2 probabilities cannot be made from the evidence provided.

## Negative pairs

- **BYOL** explicitly states it operates "**without using negative pairs**," bootstrapping a target network's output as the training target, and reports that "BYOL is more robust to the choice of image augmentations than contrastive methods," attributing this partly to not relying on negative pairs [BYOL, p.2].
- **BabyCL**'s visual branch, by contrast, is trained with the "visual NT-Xent temperature" [BabyCL, p.14], and NT-Xent is the contrastive loss that scores a positive pair against negative pairs in the batch — so, based on this evidence, BabyCL's SSL visual objective does rely on negative pairs, unlike BYOL's negative-pair-free approach. The passages do not provide further explicit discussion from BabyCL itself about whether negative pairs are "needed," so this inference rests only on the use of NT-Xent being named in [4].

**Retrieved:** BabyCL p.14 (0.82); BYOL p.26 (0.80); BYOL p.2 (0.78); BabyCL p.14 (0.77); BabyCL p.9 (0.77) | gold page hit: 0.14
*19.6 s*

## Q16 (text-only, cross-paper, hard, answerable: yes)

**Question.** Daily Oracle uses a particular retriever in its retrieval-augmented setting. What is it, and what does the embedding-retrieval paper report about how that type of retriever behaves compared with dense embedding models on its LIMIT task?

**Reference answer.** Daily Oracle's constrained open-book setting uses BM25 to retrieve the top 5 articles per question, each truncated to 512 words, restricted to articles available before the resolution date and RAG cutoff. The embedding-retrieval paper finds that on LIMIT, state-of-the-art dense single-vector models struggle (full setting rarely reaches even 20% recall@100; on the 46-document version they cannot solve the task even at recall@20), whereas BM25 'comes close to perfect scores'. The authors attribute this to sparse models behaving like single vectors with very high dimensionality, but add that it is unclear how to apply sparse models to instruction-following or reasoning tasks without lexical overlap. The LIMIT result concerns a synthetic combinatorial task and says nothing about Daily Oracle's news-forecasting data.

**System answer.** Based on the passages provided, I cannot answer this question. None of the five passages state which specific retriever Daily Oracle uses in its retrieval-augmented setting, and none describe findings from an "embedding-retrieval paper" about a retriever's behavior on a "LIMIT task" compared with dense embedding models.

What the passages do show:

- [DailyOracle, p.2] and [DailyOracle, p.3] describe Daily Oracle as a continuously updated QA forecasting benchmark built from daily news, with 16,783 TF and 14,727 MC questions generated from January 2020 to December 2024, but they do not mention a retrieval-augmented setting or name a retriever.
- [DailyOracle, p.4] mentions switching between GPT-4o-mini and GPT-4o for cost/performance reasons, but this concerns the LLM used, not a retriever.
- [EmbeddingLimits, p.3] discusses general trends in dense retrieval research (e.g., representing diverse domains, instructions, and reasoning over queries) but does not mention a "LIMIT task" or compare a specific retriever type (e.g., BM25 or sparse retrievers) against dense embedding models.

To answer this question, I would need additional passages—specifically ones identifying the exact retriever used in Daily Oracle's retrieval-augmented setup, and a passage from the embedding-limits paper that describes the "LIMIT task" and its comparative results between that retriever type and dense embedding models.

**Retrieved:** DailyOracle p.4 (0.74); DailyOracle p.2 (0.74); EmbeddingLimits p.3 (0.74); DailyOracle p.3 (0.73); DailyOracle p.3 (0.73) | gold page hit: 0.00
*10.4 s*

## Q17 (text-only, cross-paper, medium, answerable: yes)

**Question.** Daily Oracle and FIRE-Bench both use LLMs inside their evaluation pipelines. How does each validate that automated component against human judgment, and what agreement numbers does each report?

**Reference answer.** Daily Oracle validated its LLM-based QA filtering: four human annotators rated 30 TF and 30 MC sampled QA pairs on the seven filtering principles; inter-annotator agreement was fair (average Fleiss' kappa 0.26), and the LLM scores matched the human consensus with 89.52% accuracy across the seven principles and 85.00% for the final accept/reject decision (threshold of 13 points). FIRE-Bench validated its automated claim extraction and entailment-based scoring by human validation on a 33% subset of reference instances, reporting precision 0.95, recall 0.86 and F1 0.89. The two validate different components (question quality versus claim matching) with different metrics, so the numbers are not directly comparable.

**System answer.** Based on the passages provided, I can only address **Daily Oracle**; none of the passages mention FIRE-Bench at all, so I cannot answer that part of the question from the given evidence.

**Daily Oracle's validation approach:**
Daily Oracle uses an LLM-based evaluator as part of its "QA Filtering" step [DailyOracle, p.1]. To validate this automated component, the authors had four human annotators independently review a randomly sampled subset of the dataset — specifically 30 True/False (TF) and 30 Multiple Choice (MC) QA pairs. These annotators "follow the same instructions used to prompt the LLM and evaluate each QA pair based on the seven filtering principles listed in Appendix A.3" [DailyOracle, p.14].

**Agreement numbers for Daily Oracle:**
The provided passage [DailyOracle, p.14] describes the *setup* of the human evaluation (sample size, annotators, procedure) but does not report any specific agreement statistic (e.g., percentage agreement, Cohen's kappa, or inter-annotator agreement score) between the human annotators and the LLM evaluator. No such number appears in the passages given.

**FIRE-Bench:**
None of the supplied passages reference FIRE-Bench, its evaluation pipeline, or any human-validation procedure/agreement figures for it. I cannot provide any information on this part of the question based on the evidence available.

**Summary:** The evidence establishes the *method* Daily Oracle uses to validate its LLM-based QA filter (human review of a 60-pair sample against the same seven principles), but it does not establish a quantitative agreement score for Daily Oracle, and it provides no information whatsoever about FIRE-Bench's validation procedure or agreement numbers.

**Retrieved:** DailyOracle p.14 (0.74); DailyOracle p.1 (0.74); DailyOracle p.2 (0.74); DailyOracle p.10 (0.74); DailyOracle p.9 (0.73) | gold page hit: 0.00
*12.0 s*

## Q18 (text-only, insufficient-evidence, medium, answerable: no)

**Question.** According to the distillation paper, what accuracy does a single network reach on the JFT dataset after the knowledge in the specialist models has been distilled back into it?

**Reference answer.** The supplied paper does not establish this. For JFT it reports an ensemble of a generalist baseline plus 61 specialist models whose predictions are combined at inference time (top-1 test accuracy 25.0% to 26.1%, a 4.4% relative improvement; conditional accuracy 43.1% to 45.9%), and it states 'We have not yet shown that we can distill the knowledge in the specialists back into the single large net'. A related idea (using soft targets to stop specialists overfitting) is described as one it is 'currently exploring'. Where the paper does distill, it reports MNIST and speech results (a single acoustic model recovering more than 80% of the frame-accuracy gain of a 10-model ensemble), not JFT.

**System answer.** The provided passages do not establish this specific figure. They describe the specialist model setup and results in terms of relative improvements (e.g., "a 4.4% relative improvement in test accuracy overall" when combining the baseline with 61 specialist models [Distillation, p.7]) and mention conditional test accuracy on specialist classes [Distillation, p.7], but none of the passages give a numeric accuracy value for a *single distilled network* after the specialist knowledge has been distilled back into it. The passages instead focus on inference-time ensembling (Table 3, Table 4) rather than the distillation-back-into-one-network step itself.

If this information exists elsewhere in the paper (e.g., a later results table), it is not included in the passages provided here.

**Retrieved:** Distillation p.7 (0.79); Distillation p.7 (0.79); Distillation p.7 (0.75); Distillation p.5 (0.75); Distillation p.8 (0.75) | gold page hit: 1.00
*7.7 s*

## Q20 (text-only, insufficient-evidence, easy, answerable: no)

**Question.** According to the SWE-bench paper, what resolve rate do agent-based systems (models that run code, navigate the repository and iterate) reach on SWE-bench?

**Reference answer.** The supplied paper does not establish this. It evaluates single-pass language models (ChatGPT-3.5, GPT-4, Claude 2 and others, and the fine-tuned SWE-Llama) that are given BM25-retrieved or oracle files and generate one patch, and its main-text resolve rates are all single-digit percentages (for example Claude 2 resolves 4.8% with oracle retrieval). Agent-based methods appear only as an intended direction: the task can serve as a level playing field for approaches 'ranging from retrieval and long-context models to decision-making agents', and the authors 'encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs)'. No agent results are reported.

**System answer.** The provided passages do not report a resolve rate for agent-based systems. They only state results for retrieval-based evaluation: "Using a BM25 retriever, Claude 2 is only able to resolve 1.96% of the issues" [SWE-bench, p.2] and "The best-performing model, Claude 2, is able to solve a mere 1.96% of the issues" [SWE-bench, p.1]. None of the passages mention agent-based systems that run code, navigate the repository, and iterate, so I cannot determine their resolve rate from this evidence.

**Retrieved:** SWE-bench p.2 (0.76); SWE-bench p.16 (0.76); SWE-bench p.2 (0.76); SWE-bench p.1 (0.75); SWE-bench p.3 (0.75) | gold page hit: 0.25
*6.4 s*

## Q31 (text+table, cross-source, medium, answerable: yes)

**Question.** The ViT paper says smaller patches make a Transformer more expensive. Using the sequence length it implies for 224-px inputs, how do the GMACs and measured throughput of ViT-Base with 32, 16 and 8 pixel patches compare with that expectation?

**Reference answer.** The ViT paper defines the number of patches (the Transformer's sequence length) as N = HW/P^2 and says smaller patch sizes are computationally more expensive. At 224 px that gives N = 49, 196 and 784 for P = 32, 16 and 8, i.e. 4x more tokens at each step. timm shows (parameters nearly constant: 88.22M, 86.57M, 86.58M): GMACs 4.41, 17.58 and 78.22, so 3.99x from B/32 to B/16 and 4.45x from B/16 to B/8; throughput 10,936.95, 2,992.79 and 700.85 samples/s, i.e. 3.65x slower and then 4.27x slower. Cost therefore grows roughly with token count while parameters stay flat; B/8 exceeds 4x in GMACs, which the paper does not explain.

**System answer.** ## Sequence length implied by patch size (224‑px input)

The ViT paper states: *"the Transformer's sequence length is inversely proportional to the square of the patch size, thus models with smaller patch size are computationally more expensive"* [ViT, p.5].

For a 224×224 input, sequence length = (224/patch)²:

- Patch 32: (224/32)² = 7² = **49** tokens
- Patch 16: (224/16)² = 14² = **196** tokens
- Patch 8: (224/8)² = 28² = **784** tokens

So each time the patch size is halved (32→16→8), the sequence length grows by exactly **4×** (49→196→784), confirming the inverse‑square relationship the paper describes.

## Measured GMACs (compute)

From the timm benchmark query:

| Model | GMACs |
|---|---|
| vit_base_patch32_224 | 4.41 |
| vit_base_patch16_224 | 17.58 |
| vit_base_patch8_224 | 78.22 |

Ratios:
- 17.58 / 4.41 ≈ **3.99×**
- 78.22 / 17.58 ≈ **4.45×**

Both increases are close to the **4×** growth in sequence length, not the 16× one might expect if compute scaled with the *square* of sequence length (as pure self‑attention FLOPs would). This indicates that, for ViT‑Base, total model compute scales roughly **linearly** with sequence length (dominated by the linear patch‑embedding/MLP layers) rather than quadratically — but it still grows substantially as patch size shrinks, consistent with the paper's "more expensive" claim.

## Measured throughput

| Model | samples/sec |
|---|---|
| vit_base_patch32_224 | 10936.95 |
| vit_base_patch16_224 | 2992.79 |
| vit_base_patch8_224 | 700.85 |

Ratios (slowdown):
- 10936.95 / 2992.79 ≈ **3.65×** slower
- 2992.79 / 700.85 ≈ **4.27×** slower

These throughput drops closely mirror the GMACs increases (~4×), directly confirming empirically that smaller patches make the model more computationally expensive in practice, matching both the GMACs trend and the paper's statement about sequence length scaling [ViT, p.5].

## Summary

The data is consistent with the paper's qualitative claim: halving the patch size quadruples sequence length (49→196→784), and both GMACs and inverse throughput increase by a comparable ~4× factor at each step. The scaling observed (~4× per halving) is roughly **linear in sequence length**, not quadratic — suggesting that for ViT‑Base's non‑attention compute dominates total FLOPs — but the direction and rough magnitude still support the paper's assertion that smaller patches are "computationally more expensive" [ViT, p.5]. The paper itself does not provide exact GMAC/throughput numbers to compare against, so this quantitative check comes entirely from the timm benchmark query result, while the qualitative expectation comes from [ViT, p.5].

**Retrieved:** ViT p.5 (0.78); ViT p.16 (0.78); ViT p.8 (0.74); ViT p.2 (0.73); ViT p.19 (0.73) | gold page hit: 0.50
**SQL:** `SELECT   mr.arch,   mr.img_size,   bi.gmacs,   bi.samples_per_sec,   bi.batch_size,   bi.param_count_m FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.arch IN ('vit_base_patch32_224', 'vit_base_patch16_224', 'vit_base_patch8_224') GROUP BY mr.arch, mr.img_size ORDER BY mr.img_size, mr.arch;` | overlap with reference result: 1.00
*33.9 s*

## Q32 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper reports FLOPs for its 18-, 34-, 50-, 101- and 152-layer networks. How do timm's measured GMACs at 224 px compare, and for which depth is the difference largest?

**Reference answer.** The paper's Table 1 gives 1.8, 3.6, 3.8, 7.6 and 11.3 billion FLOPs, and defines its FLOPs as multiply-adds. timm's infer_gmacs at 224 px are 1.82, 3.67, 4.11, 7.83 and 11.56, i.e. +1.1%, +1.9%, +8.2%, +3.0% and +2.3%. The largest difference is for resnet50 (4.11 vs 3.8, +8.2%). Neither PDF explains the gap, so the cause should not be asserted.

**System answer.** ## What the evidence shows

The ResNet paper passages only report explicit FLOPs figures for two of the five depths:

- **50-layer ResNet: 3.8 billion FLOPs** [ResNet, p.7]
- **152-layer ResNet: 11.3 billion FLOPs** [ResNet, p.7], noted as still lower complexity than VGG-16/19 (15.3/19.6 billion FLOPs) [ResNet, p.7]

No FLOPs numbers for the 18-, 34-, or 101-layer variants appear in the supplied passages, so a full five-way comparison cannot be made from this evidence alone.

## Comparison with timm's measured GMACs (224 px)

| Depth | Paper FLOPs (billion) | timm GMACs | Difference (timm − paper) | % increase |
|---|---|---|---|---|
| 50 | 3.8 | 4.11 | **0.31** | ~8.2% |
| 152 | 11.3 | 11.56 | **0.26** | ~2.3% |

(Treating the paper's "FLOPs" count as directly comparable to timm's GMACs figure, since the values are of the same order of magnitude; if instead FLOPs = 2×MACs were applied, the paper's numbers would be roughly half of timm's, e.g., 50-layer: 8.22 vs. 3.8 GFLOPs, a difference of 4.42 — in that case 152-layer would show the larger absolute gap, 11.82 GFLOPs.)

## Answer

Using the paper's stated FLOPs at face value against timm's GMACs, the two measurements are quite close for both depths, but the **50-layer ResNet shows the larger discrepancy** (0.31 billion, ~8.2% higher in timm) compared to the 152-layer ResNet (0.26 billion, ~2.3% higher in timm).

**Caveat:** This conclusion is based on only two of the five depths, since the passages provided do not state FLOPs for ResNet-18, -34, or -101. To determine the depth with the largest difference across all five networks, the paper's FLOPs for those three models would be needed.

**Retrieved:** ResNet p.7 (0.80); ResNet p.7 (0.80); ResNet p.8 (0.76); ResNet p.5 (0.75); ResNet p.6 (0.75) | gold page hit: 0.67
**SQL:** `SELECT bi.arch, bi.img_size, bi.gmacs, bi.param_count_m FROM benchmark_infer bi WHERE bi.arch IN ('resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152')   AND bi.img_size = 224 ORDER BY bi.gmacs;` | overlap with reference result: 1.00
*25.8 s*

## Q34 (text+table, cross-source, hard, answerable: yes)

**Question.** Among timm rows whose weights tag starts with 'mae', which has the highest ImageNet-R and ImageNet-A top-1, how do ImageNet-R and ImageNet-A top-1 change with model size across these rows, and what pre-training task does the MAE paper describe?

**Reference answer.** Six hiera_*_224.mae_in1k_ft_in1k rows are tagged mae. hiera_huge_224 is highest on ImageNet-R (64.967) and ImageNet-A (66.253) (and Sketch, 50.078), with 672.78M parameters. ImageNet-R and ImageNet-A top-1 both rise at every step with model size: R is 45.78 (tiny), 49.373 (small), 53.14 (base), 55.57 (base_plus), 60.29 (large), 64.967 (huge); A is 30.56, 36.453, 43.4, 49.24, 58.013, 66.253. The drop relative to clean top-1 on the same 200 classes also shrinks with size (R: -49.47 for tiny to -32.243 for huge; A: -65.04 to -31.717), so the larger models lose less under these shifts. The MAE paper describes pre-training that masks random patches (75% in its default) and reconstructs the missing pixels with an encoder that processes only the visible patches. Caveats: the six rows are one family (Hiera, all fine-tuned on ImageNet-1k at 224 px), so this is a trend across six rows, not a controlled test; the MAE paper's own encoder is a plain ViT, Hiera is not in the corpus, and what the timm tag implies about Hiera's recipe is not stated in the PDFs.

**System answer.** ## Highest ImageNet‑R / ImageNet‑A among the `mae*` rows

From the query result (ordered by `top1_r` descending), the top row is:

- **hiera_huge_224.mae_in1k_ft_in1k** — top1_r = 64.967, top1_a = 66.253

This is simultaneously the highest on both ImageNet‑R (top1_r) and ImageNet‑A (top1_a) among the six `mae`-tagged rows returned.

## How top1_r / top1_a change with model size

Sorting the six rows by `param_count_m` (ascending):

| model | params (M) | top1_r | top1_a |
|---|---|---|---|
| hiera_tiny_224 | 27.91 | 45.780 | 30.560 |
| hiera_small_224 | 35.01 | 49.373 | 36.453 |
| hiera_base_224 | 51.52 | 53.140 | 43.400 |
| hiera_base_plus_224 | 69.90 | 55.570 | 49.240 |
| hiera_large_224 | 213.74 | 60.290 | 58.013 |
| hiera_huge_224 | 672.78 | 64.967 | 66.253 |

Both metrics **increase monotonically with model size** across all six rows — every step up in parameter count corresponds to a strictly higher top1_r and top1_a (e.g., going from tiny→huge, params rise ~24× (27.91M→672.78M) while top1_r rises from 45.78 to 64.967 (+19.19 pts) and top1_a rises from 30.56 to 66.253 (+35.69 pts)). This pattern is consistent with the MAE paper's own reported scaling behavior: "Table 13 shows that our method has strong scaling behavior: increasing the model sizes has significant gains" [MAE, p.12].

## Pre-training task described in the MAE paper

The provided passages indicate the MAE pre-training task centers on **reconstruction**: "our MAE reconstructs normalized pixels and is pre-trained for 1600 epochs" [MAE, p.7]. The paper frames this as self-supervised pre-training on ImageNet-1K, after which representations are evaluated via end-to-end fine-tuning or linear probing [MAE, p.4]. 

Note: the given passages do not include an explicit, detailed statement of the masking mechanism (e.g., what fraction of patches are masked or the encoder/decoder architecture) — only that the task is pixel reconstruction via self-supervised pre-training [MAE, p.7; MAE, p.4]. A fuller description of the masking procedure is not established by the evidence provided.

**Retrieved:** MAE p.2 (0.79); MAE p.7 (0.76); MAE p.12 (0.75); ViT p.7 (0.75); MAE p.4 (0.74) | gold page hit: 0.00
**SQL:** `SELECT model, arch, param_count_m, top1_r, top1_a FROM model_results WHERE weights_tag LIKE 'mae%' ORDER BY top1_r DESC, top1_a DESC;` | overlap with reference result: 0.49
*22.0 s*

## Q35 (text+table, cross-source, hard, answerable: yes)

**Question.** For ViT models released with the same augreg recipe tag, how much higher is ImageNet top-1 when the weights come from ImageNet-21k pre-training plus ImageNet-1k fine-tuning than when trained on ImageNet-1k only, is the gain similar for the Small and Base models, and is the pattern consistent in direction with what the ViT paper says about pre-training data?

**Reference answer.** In all six matched pairs the ImageNet-21k-then-1k weights are better, by 2.56 to 5.82 points: vit_base_patch16_224 +5.38 (84.534 vs 79.154), vit_base_patch16_384 +4.908, vit_base_patch32_224 +5.824, vit_base_patch32_384 +4.608, vit_small_patch16_224 +2.56, vit_small_patch16_384 +2.684. The gain is not the same for the two sizes: the four Base rows gain 4.6 to 5.8 points (mean 5.18) and the two Small rows 2.6 to 2.7 (mean 2.62). This is consistent in direction with the ViT paper, which says large-scale pre-training helps ('large scale training trumps inductive bias') and that larger models show their benefit only with more pre-training data. It is not a confirmation: the paper's evidence uses different pre-training sets (ImageNet, ImageNet-21k, JFT-300M) and includes ViT-Large, which has no pair here, and with only two sizes a size effect cannot be separated from other differences between the Small and Base models.

**System answer.** ## Gains from ImageNet-21k pre-training + ImageNet-1k fine-tuning vs. ImageNet-1k-only

Using the `augreg` recipe tag results from the timm database:

**ViT-Base/16**
- augreg_in21k_ft_in1k: 84.534
- augreg_in1k: 79.154
- Gain = 84.534 − 79.154 = **5.380 points**

**ViT-Small/16**
- augreg_in21k_ft_in1k: 81.402
- augreg_in1k: 78.842
- Gain = 81.402 − 78.842 = **2.560 points**

**Is the gain similar across sizes?**
No — the Base model's gain (5.38 pts) is roughly **2.1×** larger than the Small model's gain (2.56 pts). So within this same-recipe data, the larger (Base) model benefits considerably more from the IN‑21k→IN‑1k pipeline than the smaller (Small) model.

## Comparison with the ViT paper's stated pattern

The ViT paper reports that pre-training dataset size matters more for larger models: "When pre-trained on the smallest dataset, ImageNet, ViT-Large models underperform compared to ViT-Base models... With ImageNet-21k pre-training, their performances are similar. Only with JFT-300M, do we see the full benefit of larger models" and "larger ViT variants overtake smaller ones as the dataset grows" [ViT, p.6; ViT, p.7]. This describes larger models needing/benefiting more from larger pre-training data to reach (or exceed) the performance of smaller models.

The timm/augreg numbers are **directionally consistent** with that pattern: the larger model (Base) shows a bigger absolute improvement (5.38 pts) from moving to the larger pre-training source (IN‑21k) than the smaller model (Small, 2.56 pts) — i.e., the bigger model benefits more from more pre-training data, matching the qualitative trend described in the ViT paper.

**Caveat:** The passages provided from the ViT paper describe trends using JFT-300M/ImageNet-21k/ImageNet with ViT-Base/Large/Huge on the original (non-augreg) training recipe; they do not report exact numbers for ViT-Small or the specific "augreg" tagged checkpoints. So while the direction of the effect (bigger model → bigger relative benefit from more pre-training data) matches, the evidence does not establish that the *magnitude* or *mechanism* is identical to what's shown in the ViT paper's Figure 3 experiments — this is an inference drawn from the general pattern stated there, not a direct comparison in the passages.

**Retrieved:** MAE p.7 (0.85); ViT p.7 (0.84); ViT p.6 (0.83); I-JEPA p.5 (0.79); I-JEPA p.7 (0.79) | gold page hit: 0.67
**SQL:** `SELECT   arch,   weights_tag,   top1_val FROM model_results WHERE arch IN ('vit_small_patch16_224', 'vit_base_patch16_224')   AND weights_tag IN ('augreg_in1k', 'augreg_in21k_ft_in1k') ORDER BY arch, weights_tag;` | overlap with reference result: 0.23
*20.8 s*

## Q37 (text+table, cross-source, hard, answerable: yes)

**Question.** The ViT paper reports that ViT needs roughly 2-4x less compute than ResNets for the same transfer performance. In timm at 224 px, how do ViT-B/16 and ResNet-50/101/152 compare on top-1 and measured throughput, and what does that comparison say, or not say, about the paper's claim?

**Reference answer.** The paper's claim is about pre-training compute (Figure 5 is accuracy vs pre-training exaFLOPs, JFT-300M, controlled study), with the caveat that efficiency can depend on schedule, optimiser and weight decay. timm measures inference throughput and has no pre-training compute. At 224 px, taking the best ViT-B/16 row and the a1h_in1k row of each ResNet (one recipe across depths), vit_base_patch16_224.augreg2_in21k_ft_in1k has 85.108 top-1 at 2,992.79 samples/s (17.58 GMACs), versus resnet152.a1h_in1k 82.818 at 1,976.86 (11.56 GMACs), resnet101.a1h_in1k 81.95 at 2,781.19 (7.83 GMACs) and resnet50.a1h_in1k 80.654 at 4,302.84 (4.11 GMACs). So this ViT-B/16 row is more accurate than all three and faster than resnet152 (1.51x) and resnet101 (1.08x) despite more GMACs, but slower than resnet50. The ranking depends on which rows are compared: the best ResNet-50 row is resnet50.fb_swsl_ig1b_ft_in1k (81.146, trained with extra data) and is still below the best ViT-B/16 row, but the ImageNet-1k-only vit_base_patch16_224.augreg_in1k row (79.154) is below all three a1h_in1k ResNets, so the accuracy differences track pre-training data and recipe as much as architecture. These numbers neither confirm nor refute the 2-4x pre-training-compute claim.

**System answer.** ## Comparison of ViT-B/16 vs. ResNet-50/101/152 in the timm database (224 px)

| Model | Pretraining | Params (M) | Top‑1 | GMACs (inference) | Throughput (samples/sec, bs=1024) |
|---|---|---|---|---|---|
| ResNet‑50 | IN‑1k (tv_in1k) | 25.56 | 76.156 | 4.11 | 4302.84 |
| ResNet‑101 | IN‑1k (tv_in1k) | 44.55 | 77.404 | 7.83 | 2781.19 |
| ResNet‑152 | IN‑1k (tv_in1k) | 60.19 | 78.330 | 11.56 | 1976.86 |
| ViT‑B/16 | IN‑1k only (augreg_in1k) | 86.57 | 79.154 | 17.58 | 2992.79 |
| ViT‑B/16 | IN‑21k→IN‑1k ft (augreg2) | 86.57 | 85.108 | 17.58 | 2992.79 |

**Matching for comparable top‑1 ("same transfer performance"):**
The fairest single‑dataset match is ViT‑B/16 trained only on IN‑1k (79.154%) vs. ResNet‑152 (78.330%), since both were trained with no extra data.

- Compute (inference GMACs): ViT‑B/16 uses **more**, not less, compute: 17.58 / 11.56 ≈ **1.52× more GMACs** than ResNet‑152 — the opposite direction of the paper's "2–4× less compute" claim.
- Throughput: Despite using more GMACs, ViT‑B/16 is actually *faster* in measured throughput: 2992.79 / 1976.86 ≈ **1.51× higher samples/sec** than ResNet‑152, and about 1.08× faster than ResNet‑101 (2992.79/2781.19), though **1.44× slower** than ResNet‑50 (4302.84/2992.79).
- Against ResNet‑50/101, ViT‑B/16's top‑1 is clearly higher (79.154 vs 76.156 and 77.404, i.e. +2.998 and +1.75 points) but GMACs are 17.58/4.11 ≈ 4.28× and 17.58/7.83 ≈ 2.25× higher — again more, not less, compute.

If instead we use the fine‑tuned ViT‑B/16 (85.108%, pretrained on IN‑21k), it clearly dominates all three ResNets on top‑1 (+8.95, +7.70, +6.78 points respectively), but it is not a "same‑performance" comparison, and it uses even more inference compute than the IN‑1k‑only ViT would at the same architecture (GMACs unchanged at 17.58, since compute depends on architecture not pretraining data).

## What this does and doesn't say about the paper's claim

The ViT paper's "2–4× less compute" claim is about **total pre‑training compute (in exaFLOPs) versus transfer accuracy**, measured in Figure 5 across models of many sizes pretrained on JFT‑300M [ViT, p.8, §4.4; ViT, p.7, Fig. 3 caption]: "Vision Transformers dominate ResNets on the performance/compute trade-off. ViT uses approximately 2−4× less compute to attain the same performance (average over 5 datasets)" [ViT, p.8].

The timm query, by contrast, reports:
- **GMACs** = inference‑time multiply‑accumulate operations per forward pass on a single input, not cumulative pre‑training FLOPs over a large corpus like JFT‑300M.
- **samples_per_sec** = measured inference throughput on specific benchmark hardware/batch size, not training-time compute efficiency.

So the timm numbers do **not** directly test the paper's claim, because they measure a different quantity (per‑image inference compute/speed on ImageNet‑finetuned checkpoints) rather than total pre‑training compute on JFT‑300M as in the paper's Figure 5 analysis [ViT, p.7, Fig. 3; ViT, p.8, §4.4]. At best, the timm data shows that at comparable top‑1 (ViT‑B/16 IN‑1k‑only ≈79.15% vs ResNet‑152 ≈78.33%), ViT‑B/16 actually requires **more** inference-time GMACs (≈1.52×) though it achieves **higher measured throughput** on this hardware — a result that is not comparable to, and does not confirm or contradict, the paper's pre‑training-compute scaling claim.

**Retrieved:** ViT p.8 (0.78); ViT p.7 (0.77); ViT p.7 (0.76); ViT p.7 (0.76); ViT p.19 (0.75) | gold page hit: 0.67
**SQL:** `SELECT mr.model,        mr.arch,        mr.img_size,        mr.param_count_m,        mr.top1_val,        bi.samples_per_sec,        bi.gmacs,        bi.batch_size FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.img_size = 224   AND (        mr.arch = 'vit_base_patch16_224'        OR (mr.arch = 'resnet50' AND mr.weights_tag = 'tv_in1k')        OR (mr.arch = 'resnet101' AND mr.weights_tag = 'tv_in1k')        OR (mr.arch = 'resnet152' AND mr.weights_tag = 'tv_in1k')   ) ORDER BY mr.arch, mr.model;` | overlap with reference result: 0.71
*40.9 s*

## Q40 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper says its 152-layer network has lower complexity than VGG-16/19. Using timm's measurements at 224 px, how do parameters, GMACs, throughput and top-1 of resnet152 compare with vgg16 and vgg19, and does lower FLOPs mean faster in this benchmark?

**Reference answer.** The paper says the 152-layer ResNet (11.3 billion FLOPs) has lower complexity than VGG-16/19 (15.3/19.6 billion FLOPs). timm: resnet152 has 60.19M parameters, 11.56 GMACs, 1,976.86 samples/s and tv_in1k top-1 78.33; vgg16 has 138.36M, 15.47 GMACs, 2,235.61 samples/s, top-1 71.594; vgg19 has 143.67M, 19.63 GMACs, 2,044.71 samples/s, top-1 72.4. So resnet152 has 2.3-2.4x fewer parameters, 1.34-1.70x fewer GMACs and higher top-1 (with torchvision weights), but its measured throughput is about 12% lower than vgg16 and 3% lower than vgg19 on this GPU. Lower FLOPs therefore did not mean higher throughput here; the paper's claim concerns FLOPs, not measured speed.

**System answer.** ## Complexity claim in the paper

The ResNet paper states: "the 152-layer ResNet (11.3 billion FLOPs) still has lower complexity than VGG-16/19 nets (15.3/19.6 billion FLOPs)" [ResNet, p.7]. The timm benchmark numbers (GMACs, which correspond to roughly half the FLOPs count but are comparable ratios) confirm this ordering.

## timm measurements at 224 px

| Metric | resnet152 | vgg16 | vgg19 | resnet152 vs vgg16 | resnet152 vs vgg19 |
|---|---|---|---|---|---|
| Params (M) | 60.19 | 138.36 | 143.67 | 60.19/138.36 = **43.5%** of vgg16's params | 60.19/143.67 = **41.9%** of vgg19's params |
| GMACs | 11.56 | 15.47 | 19.63 | 11.56/15.47 = **74.7%** of vgg16's GMACs | 11.56/19.63 = **58.9%** of vgg19's GMACs |
| Throughput (samples/sec) | 1976.86 | 2235.61 | 2044.71 | 1976.86/2235.61 = **88.4%** → resnet152 is ~11.6% *slower* | 1976.86/2044.71 = **96.7%** → resnet152 is ~3.3% *slower* |
| Top‑1 (best variant: resnet152.a1h_in1k = 82.818) | 82.818 | 71.594 | 72.400 | 82.818 − 71.594 = **+11.22 pts** | 82.818 − 72.400 = **+10.42 pts** |

Even the weakest tv_in1k resnet152 checkpoint (78.33 top‑1) still beats both vgg16 (71.594) and vgg19 (72.4).

## Summary

- **Parameters**: resnet152 has far fewer parameters than either VGG model (~42–44% of the count), consistent with it being a "lower complexity" network as the paper describes.
- **GMACs**: resnet152 also has fewer multiply‑accumulate operations than vgg16 and vgg19 (about 75% of vgg16's and 59% of vgg19's), matching the paper's FLOPs comparison direction [ResNet, p.7].
- **Top‑1 accuracy**: resnet152 clearly outperforms both VGG models by roughly 10–11 points, matching the general narrative that deeper residual networks improve accuracy [ResNet, p.6, table of top‑1/top‑5 errors].
- **Throughput**: Despite having lower GMACs, resnet152 is measured as *slower* than both vgg16 and vgg19 in this timm benchmark (1976.86 samples/sec vs. 2235.61 and 2044.71 respectively). So in this benchmark, **lower FLOPs/GMACs did not translate into higher measured throughput**. The passages provided don't explain why (e.g., no discussion of memory-bound ops, kernel efficiency, or depth-related sequential overhead in the ResNet paper itself), so this discrepancy between theoretical complexity and actual measured speed is evident only from the timm query results, not from any explanation in the paper text supplied.

**Retrieved:** ResNet p.7 (0.79); ResNet p.10 (0.75); ResNet p.8 (0.74); ResNet p.6 (0.74); ResNet p.10 (0.74) | gold page hit: 0.50
**SQL:** `SELECT   mr.arch,   mr.model,   mr.top1_val,   bi.param_count_m,   bi.gmacs,   bi.samples_per_sec,   bi.batch_size FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.img_size = 224   AND mr.arch IN ('resnet152', 'vgg16', 'vgg19') ORDER BY mr.arch;` | overlap with reference result: 1.00
*24.7 s*

## Q42 (text-only, conceptual, medium, answerable: yes)

**Question.** Does the MMLU paper attribute its models' accuracy mainly to parameter count? Use its GPT-3, UnifiedQA and smaller fine-tuned model comparisons.

**Reference answer.** Not mainly: size matters but is not sufficient. In few-shot GPT-3 (Table 1) the three smaller models are near random (Small 25.9%, Medium 24.9%, Large 26.0% against 25.0% for random) while the 175B X-Large model reaches 43.9% (about 37.7% zero-shot). But UnifiedQA, fine-tuned on other QA datasets and tested without further tuning, reaches 48.9% with 11B parameters, better than GPT-3 X-Large despite an order of magnitude fewer parameters, and its smallest 60M variant gets about 29.3%. In Appendix A.1 RoBERTa-base (125M) gets 27.9%, ALBERT-xxlarge (223M) 27.1% and GPT-2 (1.5B) 32.4%; UnifiedQA-60M beats RoBERTa and ALBERT with fewer parameters and UnifiedQA-3B (43.7%) beats GPT-2, which the authors say suggests T5's larger pretraining dataset helps. They conclude that model size is a key component but fine-tuning also helps; the data-size explanation is a suggestion, and the models differ in architecture, fine-tuning data and evaluation regime (GPT-3 few-shot, UnifiedQA tested under distribution shift), so it is not a controlled test.

**System answer.** **Short answer: No — the paper treats parameter count as important but explicitly not the sole or even dominant factor; it credits pretraining-dataset size and fine-tuning with comparable or greater influence in several of its own comparisons.**

**Evidence that parameter count matters (within the GPT-3 family):**
- "few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy" [MMLU, p.2].
- "the three smaller GPT-3 models have near random accuracy (around 25%)... the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%" [MMLU, p.6].

So within a single model family (GPT-3), scaling parameters alone does raise accuracy — but this is the one case where architecture/pretraining data are held constant.

**Evidence that parameter count is NOT the main driver once you compare across models/training regimes:**

1. **UnifiedQA (11B) vs. GPT-3 X-Large (175B):** UnifiedQA "attains 48.9% accuracy. This performs better than the few-shot GPT-3 X-Large model, despite UnifiedQA have[ing] an order of magnitude fewer parameters" [MMLU, p.6].
 - Calculation: 175B / 11B ≈ 16× fewer parameters, yet 48.9% > 43.9%. A pure parameter-count explanation would predict the opposite.
 - The paper's own conclusion: "while model size is a key component for achieving strong performance, fine-tuning also helps" [MMLU, p.6] — i.e., fine-tuning, not just size, explains UnifiedQA's edge.

2. **UnifiedQA-small (60M) vs. RoBERTa/ALBERT:** "UnifiedQA's smallest variant, which has just 60 million parameters and approximately 29.3% accuracy... obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters. This suggests that its larger pretraining dataset enables higher accuracy" [MMLU, p.12].

3. **UnifiedQA (3B) vs. GPT-2 (1.5B):** "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy. This again suggests that T5's larger pretraining dataset size (and therefore UniﬁedQA's pretraining dataset size) can increase accuracy" [MMLU, p.12].

**Conclusion:** Using these three comparisons, the MMLU paper does *not* mainly attribute accuracy to parameter count. It shows parameter count correlates with accuracy within the homogeneous GPT-3 few-shot series [MMLU, p.2, p.6], but its UnifiedQA-vs-GPT-3, UnifiedQA-vs-RoBERTa/ALBERT, and UnifiedQA-vs-GPT-2 comparisons all show smaller models outperforming larger ones, which the paper explicitly attributes to larger pretraining-dataset size and fine-tuning rather than parameter count [MMLU, p.6; MMLU, p.12]. The paper's stated takeaway is that "model size is a key component... but fine-tuning also helps" [MMLU, p.6] — a joint, not parameter-count-dominant, explanation.

**Retrieved:** MMLU p.12 (0.81); MMLU p.6 (0.79); MMLU p.6 (0.79); MMLU p.6 (0.79); MMLU p.2 (0.79) | gold page hit: 0.67
*22.7 s*

## Q43 (text-only, cross-paper, hard, answerable: yes)

**Question.** MMLU, SWE-bench and FIRE-Bench each have to worry that a model may have seen benchmark content during training. What check does each paper run, what does it find, and how strongly does each paper state its conclusion?

**Reference answer.** MMLU (Appendix B.2): memorized questions would have low entropy and high accuracy, but accuracy and question entropy are not positively correlated (correlation between average log probability and accuracy r = -0.43 zero-shot, -0.56 few-shot), which 'suggests that our exact questions were not memorized'. The authors add that models still met text related to the questions through Wikipedia, and promise a list of question sources. SWE-bench (Section 5): resolve rates for PRs created before versus after 2023 in the oracle setting show little difference for most models (Claude 2 4.87% vs 4.23%, ChatGPT-3.5 0.49% vs 0.77%, SWE-Llama 13b 3.98% vs 3.85%), GPT-4 being the exception (1.96% vs 0.0%, on a 25% subset); the authors call this 'largely promising' since models are 'unlikely to cheat' by generating a more recent repository version, and note that new instances can be collected after a model's training date. FIRE-Bench (Section 5.4): F1 on tasks published before versus after each model's knowledge cutoff, stratified by difficulty (Table 6), shows no consistent advantage for pre-cutoff tasks; the authors call the analysis coarse (approximate cutoff dates, unknown training data, small per-category samples) and say it 'suggests the absence of a strong contamination signal rather than proving its absence'. The three checks measure different things (exact-question memorization versus date-based exposure) and none can rule contamination out, so their results are not comparable and no benchmark should be called cleaner on this evidence.

**System answer.** **What the evidence shows:**

Among the three benchmarks named in the question, the supplied passages only contain information about **FIRE-Bench's** contamination check. There are no passages in the provided material describing any contamination check for MMLU or SWE-bench, so I cannot report what those papers do or how strongly they state their conclusions — the evidence does not establish this for either benchmark.

**FIRE-Bench:**

- **Check run:** The paper reports that it "examine[s] potential data contamination effects by disentangling performance across task difficulty levels and model knowledge cutoff dates" [FIRE-Bench, p.2].
- **Finding:** Based on this disentangling analysis, the authors "find no strong evidence of systematic contamination" [FIRE-Bench, p.2].
- **Strength of claim:** The conclusion is stated in a hedged/qualified way — "no strong evidence of systematic contamination" — rather than a categorical denial that any contamination exists. The passage does not elaborate on effect sizes, statistical tests, or further caveats beyond this sentence, so the strength of the claim as given in the evidence is limited to this qualified statement [FIRE-Bench, p.2].

**MMLU and SWE-bench:** No passages about these benchmarks were provided, so no claim about their contamination checks, findings, or stated confidence can be supported from the given evidence.

**Retrieved:** FIRE-Bench p.9 (0.77); FIRE-Bench p.2 (0.77); FIRE-Bench p.9 (0.77); FIRE-Bench p.2 (0.76); FIRE-Bench p.1 (0.76) | gold page hit: 0.17
*11.5 s*

## Q44 (text-only, conceptual, medium, answerable: yes)

**Question.** In SWE-bench's baseline experiments, how are files chosen as model context (BM25 versus an 'oracle'), and what does the paper find about whether giving the model more retrieved context helps?

**Reference answer.** The baselines either retrieve files with BM25 at three context limits (13k, 27k and 50k tokens), because dense retrieval is ill-suited to the very long keys and queries, or use an 'oracle' setting that supplies the files edited by the reference patch. BM25 recall of the oracle files rises with the context limit (average 29.58 / 44.41 / 51.06 for 13k / 27k / 50k), but Claude 2's resolve rate falls (1.96 / 1.87 / 1.22), and the authors say performance drops even though recall rises because models are ineffective at localizing problematic code; models do best on the shortest context. With the oracle retriever Claude 2 resolves 4.8% of issues, and in the 'oracle'-collapsed setting (oracle files, with code not directly modified by the PR collapsed except for +/-15 lines) GPT-4 rises from 1.3% to 3.4% and Claude 2 from 4.8% to 5.9%.

**System answer.** # How Model Context is Chosen: BM25 vs. "Oracle"

**BM25 retrieval**: Files are selected automatically using the BM25 sparse retrieval algorithm, applied up to a context limit (e.g., the 27,000-token setting referenced in the passages) [SWE-bench, p.5, section 4.1].

**"Oracle" retrieval**: Rather than being retrieved algorithmically, the oracle setting directly uses the known ground-truth files — i.e., the files actually edited in the reference solution — as the context given to the model [SWE-bench, p.26, Table 18 caption; SWE-bench, p.27, Table 19].

The paper also notes a variant called "oracle"-collapsed, where the oracle files are retrieved but their content is collapsed except for the lines actually edited, as an input ablation [SWE-bench, p.6].

# Does More Retrieved Context Help?

The evidence indicates **no — more context does not straightforwardly help, and can hurt**:

- **BM25 often fails to recover the oracle files**: At the 27,000-token limit, BM25 retrieves a *superset* of the oracle files in only about 40% of instances, and in almost half of instances it retrieves *none* of the oracle files at all [SWE-bench, p.5, section 4.1]. So increasing the BM25 context budget does not reliably ensure the right files are included.

- **Performance drops as context length increases**: "As total context length increases, Claude 2's performance drops considerably; behavior that is also observed in other models" [SWE-bench, p.6]. The paper attributes this to models struggling to localize the problematic code within long, mostly irrelevant context, consistent with prior findings that models "become distracted by additional context and may be sensitive to the relative location of target sequences" [SWE-bench, p.6].

- **Even increasing BM25's context size to raise recall of oracle files doesn't help**: "Even when increasing the maximum context size for BM25 would increase recall with respect to the oracle files, performance drops, as shown in Table 2, as models are simply ineffective at localizing problematic code" [SWE-bench, p.6]. This directly shows that giving the model more (BM25-retrieved) context—even if it technically contains more of the correct files—does not improve, and in fact worsens, performance, because the core bottleneck is localization rather than retrieval/recall.

**Summary**: The paper distinguishes BM25 (algorithmic retrieval with a token budget) from oracle (ground-truth edited files given directly). It finds that simply expanding retrieved context does not help model performance — and tends to reduce it — because models struggle to localize the relevant code amid additional, often irrelevant, content [SWE-bench, p.5–6].

**Retrieved:** SWE-bench p.27 (0.81); SWE-bench p.27 (0.81); SWE-bench p.26 (0.80); SWE-bench p.6 (0.80); SWE-bench p.5 (0.80) | gold page hit: 0.50
*14.6 s*

## Q45 (text-only, cross-paper, medium, answerable: yes)

**Question.** BYOL reports that its accuracy stays stable over a wide range of batch sizes. What does BYOL say causes the drop at smaller batch sizes, and where does the Batch Normalization paper say the statistics used for normalization come from during training?

**Reference answer.** BYOL (Figure 3a, batch sizes 128 to 4096): BYOL's performance remains stable from 256 to 4096 and only drops for smaller values 'due to batch normalization layers in the encoder'; a footnote says the only dependency on batch size in its training pipeline sits within the batch normalization layers. SimCLR, by contrast, deteriorates rapidly as the batch size falls, likely because there are fewer negative examples. BatchNorm paper: because training uses mini-batches, each mini-batch produces estimates of the mean and variance of each activation, and these statistics are used for the normalization and can fully participate in the gradient backpropagation. So during training a batch-normalized layer normalizes each example with statistics estimated from its mini-batch, which is where BYOL locates its batch-size dependence. Neither paper analyses why small batches hurt: BYOL does not explain the drop beyond naming the BN layers, and the BatchNorm paper does not discuss small-batch performance or BYOL, so the link is an inference from the two papers rather than a claim either makes.

**System answer.** **What causes the drop at smaller batch sizes (per BYOL):**

BYOL attributes the performance drop at smaller batch sizes to batch normalization behaving poorly when batches are small. Specifically:

- "We think that the drop in performance at batch size 64 in table 16 is mainly related to the ill behaviour of batch normalization at low batch sizes" [BYOL, p.25].
- Similarly, "the performance of BYOL remains stable over a wide range of batch sizes from 256 to 4096, and only drops for smaller values due to batch normalization layers in the encoder" [BYOL, p.8].

**Where the Batch Normalization paper says normalization statistics come from during training:**

The evidence provided does not include any passage from the Batch Normalization paper itself — only passages from BYOL are given. Therefore, I cannot answer this part of the question based on the available evidence. The BYOL passages only reference batch normalization's "ill behaviour... at low batch sizes" [BYOL, p.25] without specifying how the original Batch Normalization paper describes the source of training-time statistics (e.g., whether computed per mini-batch). To answer that part, a passage from the actual Batch Normalization paper would be needed.

**Retrieved:** BYOL p.25 (0.86); BYOL p.30 (0.83); BYOL p.8 (0.83); BYOL p.28 (0.82); BYOL p.8 (0.79) | gold page hit: 0.33
*9.3 s*

## Q39 (text+table, cross-source, medium, answerable: yes)

**Question.** The BYOL paper reports 74.3% for a linear classifier on frozen ResNet-50 features and cites supervised ResNet-50 baselines of 76.5% and 78.9%. How many timm ResNet-50 rows at 224 px have a top-1 accuracy at or above each of these three numbers, and what limits how that comparison can be read?

**Reference answer.** The paper's numbers are 74.3% (BYOL, linear evaluation on frozen features), 76.5% and 78.9% (supervised baselines). Among timm's 18 resnet50 rows at 224 px, all 18 are at or above 74.3%, 17 are at or above 76.5% (the exception is resnet50.tv_in1k at 76.156), and 13 are at or above 78.9% (the five below are ra_in1k 78.82, bt_in1k 78.444, a3_in1k 78.052, gluon_in1k 77.58 and tv_in1k 76.156). These are not like-for-like: BYOL's 74.3% is a linear probe on self-supervised features, whereas timm's are fully supervised weights with different recipes, some using extra data (e.g. ig1b, yfcc100m), so the comparison says nothing about whether self-supervised learning is better or worse.

**System answer.** ## Results from the timm database query

For ResNet-50 at 224 px image size:

| Threshold | Number of timm ResNet-50 (224px) rows meeting/exceeding it |
|---|---|
| ≥ 74.3% (BYOL's own linear-eval result) | 18 |
| ≥ 76.5% (supervised baseline from [8]) | 17 |
| ≥ 78.9% (stronger supervised baseline from [75]) | 13 |

The BYOL paper states these three reference numbers directly: "With a standard ResNet-50 (×1) BYOL obtains 74.3% top-1 accuracy... This tightens the gap with respect to the supervised baseline of [8], 76.5%, but is still significantly below the stronger supervised baseline of [75], 78.9%" [BYOL, p.6].

## What limits how this comparison can be read

1. **Different training paradigms are being conflated.** The 74.3% BYOL figure is a *linear classifier trained on frozen self-supervised features* [BYOL, p.2, Abstract; p.6]. The timm database rows, by contrast, are presumably standard *end-to-end supervised* ResNet-50 training runs (the query makes no distinction and the passages give no indication timm contains linear-probe results). Comparing 18 timm models ≥74.3% to BYOL's 74.3% is therefore comparing fully-supervised fine-tuned accuracy to a frozen-backbone linear probe — not a like-for-like comparison.

2. **The 76.5% and 78.9% baselines are specific supervised numbers from specific papers ([8] and [75] respectively)**, not general claims about all ResNet-50 variants [BYOL, p.6]. The timm database likely contains many ResNet-50 variants trained with different recipes, augmentations, schedules, and training durations (e.g., the paper itself notes using RandAugment "suspecting that the supervised baselines' performance in [8] could be even further improved with appropriate data augmentations" [BYOL, p.19]). So the fact that 17 or 13 timm entries exceed these numbers doesn't contradict or confirm BYOL's claims — it just reflects that supervised ResNet-50 training has continued to improve since BYOL's baselines were set, consistent with BYOL's own observation that supervised numbers can be pushed higher with better augmentation [BYOL, p.19].

3. **No information in the passages specifies what "top1_val" in the timm database represents methodologically** (e.g., training recipe, epochs, augmentation strategy, or whether any are self-supervised/linear-probe results). Without that detail, the count of 18/17/13 rows only tells us how many *some* ResNet-50-224px configurations in timm reach those thresholds — it cannot be used to directly validate, refute, or recontextualize the specific comparisons BYOL makes against its two cited baselines.

**In short:** the passages establish only the three BYOL/baseline numbers themselves [BYOL, p.6]; the SQL result adds a count of 18, 17, and 13 timm ResNet-50 (224px) entries at or above each threshold respectively, but the evidence does not establish whether those timm entries are self-supervised, linear-probe, or supervised results, nor their training conditions — so the comparison can't be read as directly judging BYOL's claims against a comparable baseline set.

**Retrieved:** BYOL p.19 (0.83); BYOL p.21 (0.81); BYOL p.6 (0.81); BYOL p.6 (0.80); BYOL p.2 (0.80) | gold page hit: 1.00
**SQL:** `SELECT   SUM(CASE WHEN top1_val >= 74.3 THEN 1 ELSE 0 END) AS n_ge_74_3,   SUM(CASE WHEN top1_val >= 76.5 THEN 1 ELSE 0 END) AS n_ge_76_5,   SUM(CASE WHEN top1_val >= 78.9 THEN 1 ELSE 0 END) AS n_ge_78_9 FROM model_results WHERE arch = 'resnet50' AND img_size = 224;` | overlap with reference result: 1.00
*24.8 s*
