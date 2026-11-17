# Report: runs/chunk_paragraph_matched

35 questions, 0 errors, mean latency 22.5 s.

| Source type | Retrieval page hit | SQL value overlap | Answers with abstention wording |
|---|---|---|---|
| text-only | 0.77 (n=21) | - | 11 of 21 |
| table-only | - | 0.71 (n=7) | 0 of 7 |
| text+table | 0.79 (n=7) | 0.78 (n=7) | 3 of 7 |

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

**System answer.** ## How plain vs. residual 18/34-layer networks differed

**Plain networks:** The deeper 34-layer plain net had *higher* validation error than the shallower 18-layer plain net, and the 34-layer plain net exhibited higher training error throughout training than the 18-layer one — even though the 18-layer network's solution space is a subspace of the 34-layer network's [ResNet, p.5]. This is the "degradation problem."

**Residual networks (ResNets):** The pattern reversed. The 34-layer ResNet outperformed the 18-layer ResNet by 2.8% (top-1 error), and the 34-layer ResNet showed "considerably lower training error" and generalized well to validation data — indicating the degradation problem was "well addressed" [ResNet, p.5]. Quantitatively, Table 2 shows:

- Plain: 18 layers = 27.94%, 34 layers = 28.54% (deeper is worse)
- ResNet: 18 layers = 27.88%, 34 layers = 25.03% (deeper is better) [ResNet, p.5]

Additionally, for the shallower 18-layer case, the plain and residual nets were "comparably accurate," but the 18-layer ResNet converged faster, since "the ResNet eases the optimization by providing faster convergence at the early stage" [ResNet, p.6].

## Why the authors argue it isn't vanishing gradients

The authors give three pieces of evidence [ResNet, p.5]:

1. **BN ensures healthy signal propagation:** "These plain networks are trained with BN [16], which ensures forward propagated signals to have non-zero variances."
2. **Gradients are verified healthy:** "We also verify that the backward propagated gradients exhibit healthy norms with BN. So neither forward nor backward signals vanish."
3. **The plain net still trains reasonably well overall:** "the 34-layer plain net is still able to achieve competitive accuracy (Table 3), suggesting that the solver works to some extent."

Based on this, they instead conjecture: "the deep plain nets may have exponentially low convergence rates, which impact the reducing of the training error," rather than vanishing gradients being the cause [ResNet, p.5]. They note the exact reason for this optimization difficulty "will be studied in the future" [ResNet, p.5].

**Retrieved:** ResNet p.5 (0.85); ResNet p.5 (0.84); ResNet p.5 (0.83); ResNet p.6 (0.82); ResNet p.5 (0.82); ResNet p.4 (0.82); ResNet p.3 (0.82); ResNet p.2 (0.81); ResNet p.5 (0.80); ResNet p.7 (0.79); ResNet p.8 (0.78); ResNet p.7 (0.78); ResNet p.7 (0.76); ResNet p.2 (0.76); ResNet p.6 (0.76); ResNet p.6 (0.76); ViT p.5 (0.75); ResNet p.7 (0.75); ResNet p.7 (0.75); ResNet p.10 (0.75); ResNet p.4 (0.75); ResNet p.1 (0.75); ResNet p.7 (0.75); BYOL p.18 (0.74) | gold page hit: 1.00
*17.8 s*

## Q02 (text-only, factual, medium, answerable: yes)

**Question.** In BabyCL's main results (Table 1), how do the Labeled-S 4AFC accuracies of BabyCL (k = 4 and k = 8) compare with the offline CVCL upper bound and with the one-pass and compute-matched streaming baselines, and what do the authors conclude from the compute-matched baseline?

**Reference answer.** Table 1 (4AFC, Labeled-S, mean +/- CI): offline CVCL (i.i.d., 400 epochs, upper bound) 57.31 +/- 1.13; one-pass CVCL (naive streaming) 27.52 +/- 3.12; CL-CVCL (compute-matched) 36.41 +/- 2.31; BabyCL with k=4 41.08 +/- 1.79 and with k=8 43.38 +/- 1.47. Both BabyCL settings beat both streaming baselines (k=8 is 15.86 points above one-pass CVCL and 6.97 above CL-CVCL), k=8 is 2.30 above k=4, and both remain below the offline upper bound (k=8 by 13.93 points). The authors conclude that BabyCL substantially closes but does not match the gap to offline training, and because CL-CVCL is matched in optimization work to BabyCL's gradient budget (at k=8), BabyCL's advantage 'cannot be explained by gradient count alone'.

**System answer.** ## Labeled‑S 4AFC results from Table 1

**Numbers reported in the "Main results" narrative of Table 1** [BabyCL, p.6, §4.2]:
- Offline CVCL (i.i.d. upper bound): **57.45%**
- One‑pass CVCL (naive streaming): **25.68%**
- CL‑CVCL (compute‑matched replay, k=8 gradient budget): **35.32%**
- BabyCL (k=8): **44.46%**

A companion presentation of the same comparison, with confidence intervals and the k=4 variant included [BabyCL, p.5, §3]:
- Offline CVCL: 57.31 ± 1.13%
- One‑pass CVCL: 27.52 ± 3.12%
- CL‑CVCL: 36.41 ± 2.31%
- BabyCL (k=4): 41.08 ± 1.79%
- BabyCL (k=8): 43.38 ± 1.47%

## Comparisons (using the §4.2 main-results figures)

- **Vs. offline upper bound:** BabyCL (k=8) at 44.46% is below Offline CVCL's 57.45% — a gap of 57.45 − 44.46 = **12.99 percentage points**. The authors explicitly frame offline CVCL as an "upper bound for what the CVCL objective can achieve when temporal structure is removed" [BabyCL, p.6, §4.2], and state that BabyCL "substantially closes the gap to offline CVCL... but does not match it" [BabyCL, p.6, §4.2].

- **Vs. one‑pass streaming baseline:** BabyCL (k=8) beats one‑pass CVCL (25.68%) by 44.46 − 25.68 = **18.78 points**, confirming that "a training recipe designed for i.i.d. data does not transfer to streaming" [BabyCL, p.6, §4.2].

- **Vs. compute‑matched baseline (CL‑CVCL):** BabyCL (k=8) exceeds CL‑CVCL (35.32%) by 44.46 − 35.32 = **9.14 points**, even though CL‑CVCL is matched to BabyCL's gradient budget ("approximately 6× revisitation per item") [BabyCL, p.6, §4.1].

- **k=4 vs. k=8:** Using the k=4/k=8 values from [BabyCL, p.5, §3] (41.08% → 43.38%), moving from k=4 to k=8 raises accuracy by roughly 2–2.6 points; the main‑results text states this additional insertion‑time resampling "yields a further 2.6‑point gain" [BabyCL, p.6, §4.2].

## Authors' conclusion about the compute-matched baseline

Because CL‑CVCL is given the **same optimization budget** as BabyCL (matched gradient/update count) but still trails BabyCL by about 9 points, the authors conclude that **"the gap cannot be explained by gradient count alone; it reflects the benefit of organizing the stream through event segmentation and of combining visual self‑supervision with cross‑modal grounding"** [BabyCL, p.6, §4.2]. In other words, BabyCL's advantage over CL‑CVCL is attributed to its continual‑learning architecture (segmentation‑driven replay plus joint visual/cross‑modal objectives), not merely to doing more optimization steps — and the additional gain from k=4→k=8 further suggests that "the continual‑structure benefits compound with more thorough revisitation of newly inserted content" [BabyCL, p.6, §4.2].

**Note on evidence:** the two passages ([BabyCL, p.5, §3] and [BabyCL, p.6, §4.2]) give slightly different numeric values for the same methods (e.g., Offline CVCL 57.31% vs. 57.45%; CL‑CVCL 36.41% vs. 35.32%; BabyCL k=8 43.38% vs. 44.46%). The qualitative ordering and conclusions are identical in both, but the exact percentage‑point gaps differ slightly depending on which passage's numbers are used (see calculations above for both sets).

**Retrieved:** BabyCL p.8 (0.82); BabyCL p.5 (0.81); BabyCL p.6 (0.81); BabyCL p.6 (0.80); BabyCL p.5 (0.80); BabyCL p.8 (0.79); BabyCL p.9 (0.78); BabyCL p.5 (0.77); BabyCL p.15 (0.76); BabyCL p.8 (0.76); BabyCL p.15 (0.75); BabyCL p.9 (0.75); BabyCL p.7 (0.74); BabyCL p.11 (0.74); BabyCL p.7 (0.74); BabyCL p.7 (0.72); BabyCL p.10 (0.72); BabyCL p.14 (0.72); BabyCL p.6 (0.72); BabyCL p.4 (0.71); BabyCL p.15 (0.71); BabyCL p.14 (0.71); BabyCL p.4 (0.71); BabyCL p.14 (0.70); BabyCL p.14 (0.70); BabyCL p.9 (0.70) | gold page hit: 1.00
*53.6 s*

## Q03 (text-only, factual, medium, answerable: yes)

**Question.** How does I-JEPA sample its target and context blocks (number of target blocks, scale and aspect-ratio ranges), and where in the pipeline are the target blocks 'masked'?

**Reference answer.** I-JEPA typically samples M = 4 target blocks, each with random aspect ratio in (0.75, 1.5) and random scale in (0.15, 0.2). The context is a single block with scale in (0.85, 1.0) and unit aspect ratio, from which any region overlapping the targets is removed so the prediction task is non-trivial. The target blocks are obtained by masking the output of the target encoder, not its input, which the paper calls crucial for high-semantic-level targets. The loss is the average L2 distance between predicted and target patch-level representations, and the target encoder is an exponential moving average of the context encoder.

**System answer.** # How I-JEPA Samples Target and Context Blocks

**Target blocks:**
- By default, I-JEPA samples **M = 4** (possibly overlapping) target blocks [I-JEPA, p.4, section 3. Method].
- Random **scale** range: **(0.15, 0.2)** [I-JEPA, p.12, section A.1. Pretraining; p.4].
- Random **aspect ratio** range: **(0.75, 1.5)** [I-JEPA, p.4, section 3. Method; p.12].
- These target blocks are sampled from the output of the target-encoder (applied to the full, non-overlapping-patch sequence of the image) [I-JEPA, p.3, section 3. Method].

**Context block:**
- **1** context block is sampled [I-JEPA, p.12, section A.1. Pretraining].
- Random **scale** range: **(0.85, 1.0)** [I-JEPA, p.4, section 3. Method; p.12].
- **Unit aspect ratio** (i.e., aspect ratio = 1) [I-JEPA, p.4, section 3. Method; p.12].
- Since target and context blocks are sampled independently, they may overlap; any regions of the context block overlapping with the 4 target blocks are **removed** from the context block "to ensure a non-trivial prediction task" [I-JEPA, p.4, section 3. Method; p.12, section A.1. Pretraining].

**Where the "masking" of target blocks happens in the pipeline:**
- Critically, target blocks are obtained by **masking the output of the target-encoder, not the input**. That is, the full image (as non-overlapping patches) is first passed entirely through the target-encoder to get patch-level representations sy = {sy1,...,syN}; only *after* this encoding step are the M target blocks (masks Bi) selected from these representations to form the targets sy(i) = {syj}j∈Bi [I-JEPA, p.3, section 3. Method; p.4, section 3. Method: "Note that the target blocks are obtained by masking the output of the target-encoder, not the input."].
- This design choice is explicitly flagged as important: "This distinction is crucial to ensure target representations of a high semantic level" [I-JEPA, p.4, section 3. Method].
- An ablation confirms this: masking the output (vs. the input, which requires a separate forward pass through the target-encoder for each target region) yields much better linear-probe performance — **67.3** top-1 (output masking) vs. **56.1** top-1 (input masking) for a ViT-H/16 pretrained 300 epochs, evaluated via linear probe on 1% ImageNet-1K [I-JEPA, p.14–15, Table 11, section C. Additional Ablations: "Masking the output of the target-encoder during pretraining results in more semantic prediction targets and improves linear probing performance."].

**Summary of the overall masking strategy:** Context mask and the 4 target masks are sampled independently for each image in a batch; overlap between the context mask and any target mask is removed from the context, making the context block "informative, yet sparse (efficient to process)" while target blocks remain "relatively semantic" [I-JEPA, p.4, Figure 4 caption, section 3. Method].

**Retrieved:** I-JEPA p.4 (0.88); I-JEPA p.3 (0.84); I-JEPA p.14 (0.84); I-JEPA p.2 (0.83); I-JEPA p.17 (0.80); I-JEPA p.14 (0.80); I-JEPA p.14 (0.79); I-JEPA p.12 (0.79); I-JEPA p.14 (0.79); I-JEPA p.4 (0.79); I-JEPA p.14 (0.78); I-JEPA p.3 (0.78); I-JEPA p.8 (0.78); I-JEPA p.16 (0.77); I-JEPA p.7 (0.77); I-JEPA p.8 (0.76); I-JEPA p.4 (0.76); I-JEPA p.15 (0.76); I-JEPA p.8 (0.76); I-JEPA p.12 (0.76); I-JEPA p.5 (0.76); I-JEPA p.8 (0.75); I-JEPA p.2 (0.75); I-JEPA p.1 (0.75); I-JEPA p.5 (0.75) | gold page hit: 1.00
*14.7 s*

## Q04 (text-only, factual, easy, answerable: yes)

**Question.** How are Daily Oracle's question-answer pairs generated and filtered, and how many True/False and multiple-choice questions are in the subset analysed in the paper?

**Reference answer.** The analysed subset has 16,783 True/False and 14,727 multiple-choice questions generated from daily news articles from January 2020 to December 2024. Each day six articles are selected (three random, three from hot topics) and an LLM generates two TF and two MC pairs per article with few-shot prompting. Construction has four steps: article summary (focused on new events so the publication date can be the resolution date), QA generation, misleading-choice generation for MC, and QA filtering. In filtering, an LLM scores seven principles from 0 to 2 points each and only questions with at least 13 points are kept.

**System answer.** ## Dataset Construction and Generation Process

Daily Oracle's QA pairs are generated through an **LLM-based four-step construction process** applied to daily news articles [DailyOracle, p.4]:

1. **Article Selection**: For each day, six articles are selected — three chosen randomly, and three selected from "hot topics" of the day. Hot topics are identified by applying the DBSCAN clustering algorithm to news articles based on TF-IDF representations, filtering out "chaotic" clusters with low average in-cluster cosine similarity, and taking the top three clusters by size (one article randomly picked from each) [DailyOracle, p.13].

2. **QA Generation**: For each selected article, an LLM generates two True/False (TF) QA pairs and two Multiple Choice (MC) QA pairs using a few-shot prompting technique [DailyOracle, p.4].

3. **Misleading Choices Generation**: For MC questions, the article, its publishing date, and the QA pair are given to the LLM, which generates three misleading (noising) choices. These must be "unambiguously incorrect" but still "plausible" and "make sense" [DailyOracle, p.4; p.28].

4. **QA Filtering**: The LLM checks each QA pair against **seven filtering principles**: (1) correctness of answers, (2) non-answerability before the publication date, (3) absence of information leakage, (4) objectivity, (5) inclusion of a clear temporal element, (6) public interest, and (7) non-obviousness of the answer. Each principle is scored 0, 1, or 2 points, and only questions scoring **at least 13 points in total** are retained [DailyOracle, p.4].

The underlying news corpus consists of 1,246,973 English articles spanning January 2019 to December 2024, and QA pairs themselves are generated from articles published between January 2020 and December 2024 [DailyOracle, p.4].

Quality was further verified via human evaluation: four annotators independently reviewed a randomly sampled subset of 30 TF and 30 MC QA pairs, following the same seven filtering principles used to prompt the LLM [DailyOracle, p.14].

## Dataset Size (Subset Used for Analysis)

The subset used in the paper's analysis consists of:
- **16,783 TF QA pairs**
- **14,727 MC QA pairs**

covering January 1, 2020, to December 31, 2024, with an average of 17.2 questions per day [DailyOracle, p.4; p.3].

**Calculation check**: 16,783 (TF) + 14,727 (MC) = **31,510 total QA pairs**, which matches the total reported in the benchmark comparison table [DailyOracle, p.3, Table 1: "31,510"].

Note: While Daily Oracle itself continues to generate new questions daily, the paper's experiments specifically use this subset generated through December 2024 [DailyOracle, p.3].

**Retrieved:** DailyOracle p.4 (0.80); DailyOracle p.3 (0.79); DailyOracle p.1 (0.79); DailyOracle p.3 (0.78); DailyOracle p.14 (0.73); DailyOracle p.2 (0.73); DailyOracle p.4 (0.72); DailyOracle p.13 (0.72); DailyOracle p.29 (0.71); DailyOracle p.28 (0.71); DailyOracle p.15 (0.70); DailyOracle p.1 (0.70); DailyOracle p.10 (0.70); DailyOracle p.4 (0.70); DailyOracle p.19 (0.70); DailyOracle p.3 (0.70); DailyOracle p.5 (0.69); DailyOracle p.20 (0.69); DailyOracle p.13 (0.69); DailyOracle p.7 (0.69); DailyOracle p.8 (0.69); DailyOracle p.17 (0.69); SWE-bench p.24 (0.69); DailyOracle p.9 (0.69); DailyOracle p.35 (0.68); SWE-bench p.27 (0.68); SWE-bench p.26 (0.68); DailyOracle p.4 (0.68); DailyOracle p.17 (0.68); DailyOracle p.26 (0.68) | gold page hit: 1.00
*12.8 s*

## Q06 (text-only, conceptual, medium, answerable: yes)

**Question.** What three desiderata do the Transformer authors use to motivate self-attention over recurrent and convolutional layers, how does a self-attention layer compare on each, and when is it cheaper per layer than a recurrent layer?

**Reference answer.** The desiderata are (1) total computational complexity per layer, (2) the amount of computation that can be parallelised (minimum number of sequential operations) and (3) the path length between long-range dependencies. Per Table 1, self-attention has O(n^2*d) complexity per layer, O(1) sequential operations and O(1) maximum path length; recurrent layers have O(n*d^2), O(n) and O(n); convolutional layers have O(k*n*d^2), O(1) and O(log_k n). Self-attention is faster than a recurrent layer when the sequence length n is smaller than the representation dimensionality d, which is typical for sentence representations in machine translation. For very long sequences the authors suggest restricting attention to a neighbourhood of size r (path length O(n/r)) but leave this to future work.

**System answer.** Based on the provided passages, the evidence on this topic is **incomplete** — the key passage that introduces the "three desiderata" is cut off before naming the third one, and the passage comparing per-layer cost to recurrent layers is also cut off before stating the exact condition. Here is what the passages do establish:

## The desiderata (as stated in the text)

[Transformer, p.6] states: "Motivating our use of self-attention we consider three desiderata. One is the total computational complexity per layer. Another is the amount of computation that can be parallelized, as measured by the minimum number of sequential operations required."

- Desideratum 1: **total computational complexity per layer**
- Desideratum 2: **amount of computation that can be parallelized** (measured by minimum number of sequential operations required)
- Desideratum 3: **Not stated in the supplied passages** — the sentence in [Transformer, p.6] is cut off right after the second item, so the evidence does not name the third desideratum. (A related, but separately framed, concern about the **length of paths between long-range dependencies** does appear elsewhere in the text — [Transformer, p.7] discusses how convolutional layers require a stack of "O(n/k)" or "O(log_k(n))" layers to connect all positions, "increasing the length of the longest paths between any two positions in the network" — but the passages never explicitly label this as the "third desideratum," so I cannot confirm it fills that role from the given evidence.)

## Comparison on each desideratum

**Parallelization / sequential operations** [Transformer, p.6]:
> "a self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations."

So self-attention needs only a **constant** number of sequential steps (highly parallelizable), while a recurrent layer needs **O(n)** sequential steps (n = sequence length), which is inherently sequential and less parallelizable.

**Total computational complexity per layer** [Transformer, p.6–7]:
The passages state that self-attention is compared to recurrent and convolutional layers on this axis (see Table 1 reference in [Transformer, p.6]), and separately note for convolutions: "Convolutional layers are generally more expensive than recurrent layers, by a factor of k... Even with k = n, the complexity of a separable convolution is equal to the combination of a self-attention layer and a point-wise feed-forward layer, the approach we take in our model" [Transformer, p.7]. However, the passages do **not** give the explicit complexity formulas for self-attention vs. recurrent layers (e.g., no O(·) expression for either is stated in the supplied text), so I cannot report the exact per-layer complexity comparison between self-attention and recurrent layers specifically.

## When self-attention is cheaper per layer than a recurrent layer

[Transformer, p.6] begins to answer this directly: "In terms of computational complexity, self-attention layers are faster than recurrent layers when the sequence..." — but the passage is **cut off at this exact point**, before stating the condition (e.g., a threshold relating sequence length to representation dimensionality). Based on the supplied evidence alone, I can confirm only that **such a condition exists and is tied to sequence length**, but the specific threshold is not recoverable from the given passages.

**Summary of evidentiary gaps:** The passages confirm two of the three desiderata explicitly and give a clear comparison for the "parallelization" criterion. They do not supply (a) the name of the third desideratum, (b) explicit complexity formulas for self-attention vs. recurrent layers, or (c) the precise condition under which self-attention is cheaper per layer than a recurrent layer — the relevant sentences in [Transformer, p.6] are truncated in the provided excerpts.

**Retrieved:** ViT p.10 (0.79); Transformer p.6 (0.77); Transformer p.6 (0.76); Transformer p.2 (0.76); ViT p.8 (0.75); Transformer p.6 (0.75); Transformer p.10 (0.74); ViT p.2 (0.74); Transformer p.7 (0.72); Transformer p.1 (0.72); Transformer p.2 (0.72); ViT p.1 (0.71); Transformer p.5 (0.71); ViT p.1 (0.71); ViT p.2 (0.70); Transformer p.2 (0.70); ViT p.2 (0.70); MAE p.9 (0.70); MAE p.10 (0.70); ViT p.1 (0.70); Transformer p.10 (0.70); Transformer p.3 (0.70); ViT p.3 (0.70); I-JEPA p.11 (0.69); ViT p.4 (0.69); I-JEPA p.11 (0.69); ViT p.8 (0.69) | gold page hit: 1.00
*27.7 s*

## Q07 (text-only, conceptual, hard, answerable: yes)

**Question.** BYOL trains without negative pairs. What mechanisms does the paper credit with preventing representation collapse, and what do its ablations show about them?

**Reference answer.** BYOL trains an online network (encoder, projector, predictor) to predict the projection of a second augmented view produced by a target network whose weights are an exponential moving average of the online weights; the loss gradient is not propagated into the target (stop-gradient) and the predictor exists only on the online branch. The authors hypothesise that the combination of the predictor and the slow-moving-average target avoids collapse, but they state the dynamics still admit undesirable equilibria that they did not observe in experiments. In the ablation (Table 5b), the only variant that performs well without negatives is BYOL with both a target network and a predictor; the representation collapses when either is removed. They also found that the target network can be removed without collapse if the predictor is kept near-optimal (e.g., higher predictor learning rate), suggesting that keeping the predictor near-optimal may be one role of the target network.

**System answer.** ## Mechanisms credited with preventing collapse

BYOL's authors hypothesize that collapse is avoided by the **combination of two architectural elements**:

1. **The addition of a predictor to the online network**
2. **Use of a slow-moving average (exponential moving average) of the online parameters as the target network**

As stated directly: "We hypothesize (see Section 3.2) that the combination of (i) the addition of a predictor to the online network and (ii) the use of a slow-moving average of the online parameters as the target network encourages encoding more and more information within the online projection and avoids collapsed solutions" [BYOL, p.2].

The paper also offers a theoretical intuition: BYOL avoids constant features because, for any constant $c$, $\text{Var}(z'_\xi \mid z_\theta) \le \text{Var}(z'_\xi \mid c)$, suggesting collapsed constant equilibria are unstable [BYOL, p.5]. More generally, the authors note there is likely **no single joint loss** $L_{\theta,\xi}$ that BYOL's dynamics perform gradient descent on (analogous to GANs), so there is "no a priori reason why BYOL's parameters would converge to" collapsed minima of $L^{BYOL}_{\theta,\xi}$, even though such equilibria exist in principle [BYOL, p.4].

## What the ablations show

**1. Removing either the predictor or the target network causes collapse.**
"Table 5b already shows the importance of combining a predictor and a target network: the representation does collapse when either is removed" [BYOL, p.10].

**2. The predictor is critical, even replacing dropout/noise variants.**
A variant using image augmentations instead of architectural noise (dropout) "collapses (Row 7 of Table 5) which suggests that the additional predictor is critical to prevent collapse in an unsupervised scenario" [BYOL, p.10].

**3. A near-optimal predictor can substitute for the target network.**
The authors found "we can remove the target network without collapse by making the predictor near-optimal," via (i) an optimal linear predictor obtained by linear regression on the current batch (52.5% top-1) or (ii) increasing the predictor's learning rate (66.5% top-1). However, increasing learning rates of *both* projector and predictor together (without a target network) "yields poor results (≈25% top-1)" [BYOL, p.10]. This suggests "keeping the predictor near-optimal at all times is important to preventing collapse, which may be one of the roles of BYOL's target network" [BYOL, p.10].

**4. Target network decay rate (τ) ablation shows a stability/improvement trade-off, not pure collapse-prevention.**
When τ=0 (instantaneous update), training is destabilized, "yielding very poor performance," while τ=1 (never updated) "makes the training stable but prevents iterative improvement, ending with low-quality final representation." Decay rates between 0.9 and 0.999 "yield performance above 68.4% top-1 accuracy at 300 epochs" [BYOL, p.8]. This indicates the moving-average target doesn't just prevent collapse outright but balances stability against representation quality.

**5. Even a fixed random network as target avoids collapse (but gives poor representations), supporting the bootstrapping motivation.**
"[W]e apply this procedure by predicting a fixed randomly initialized network and achieve 18.8% top-1 accuracy... whereas the randomly initialized network only achieves 1.4% by itself" [BYOL, p.3]. This shows collapse can be avoided with even a static target, but quality is far below BYOL's full mechanism, motivating the iterative bootstrapping via EMA.

**6. Negative pairs are not necessary when both mechanisms are present.**
"The only variant that performs well without negative examples (i.e., with β = 0) is BYOL, using both a bootstrap target network and a predictor" [BYOL, p.9], and adding negative pairs without retuning temperature actually hurts performance [BYOL, p.9], reinforcing that the predictor+target-network combination—not negative pairs—is doing the collapse-prevention work.

**Retrieved:** BYOL p.2 (0.76); BYOL p.4 (0.74); BYOL p.1 (0.74); BYOL p.9 (0.74); BYOL p.10 (0.73); BYOL p.3 (0.72); BYOL p.10 (0.72); BYOL p.3 (0.72); BYOL p.2 (0.71); BYOL p.3 (0.71); BYOL p.5 (0.70); BYOL p.3 (0.69); BYOL p.28 (0.69); BYOL p.2 (0.69); I-JEPA p.3 (0.69); BYOL p.6 (0.69); BYOL p.8 (0.69); I-JEPA p.13 (0.69); BYOL p.4 (0.68); BYOL p.4 (0.68); BYOL p.7 (0.68) | gold page hit: 1.00
*17.4 s*

## Q08 (text-only, conceptual, medium, answerable: yes)

**Question.** What evidence does the Batch Normalization paper give that batch normalization reduces internal covariate shift, how large is the training speed-up it reports on ImageNet (and what else was changed besides adding BN), and what does the paper itself say it has not established?

**Reference answer.** The paper defines internal covariate shift as the change in the distribution of network activations due to the change in network parameters during training. Its direct evidence is a small MNIST experiment (three sigmoid hidden layers): the input distribution to a typical sigmoid unit is much more stable with BN and the BN network has higher test accuracy (Fig. 1). On ImageNet the evidence is indirect, through the speed and accuracy of BN-Inception variants: BN-Baseline matches Inception's 72.2% in 13.3M steps versus 31.0M, BN-x5 needs 2.1M steps (stated as 14 times fewer), BN-x30 reaches 74.8%, and BN-x5-Sigmoid reaches 69.8% while Inception with sigmoid never beats 1/1000 accuracy. The BN-x5/x30 speed-ups combine BN with other changes (a 5x or 30x larger initial learning rate, Dropout removed, L2 weight cut 5x, learning rate decayed 6x faster, Local Response Normalization removed, more thorough shuffling, fewer photometric distortions), so they are not an isolated measure of BN. The paper frames the mechanism as an expectation and conjecture: it 'expects' fixed input distributions to speed training, 'conjectures' that BN may bring layer Jacobian singular values close to 1, and says the precise effect of BN on gradient propagation remains an area of further study.

**System answer.** ## Evidence that BN reduces internal covariate shift

The paper's main empirical demonstration is the MNIST experiment in Section 4.1: using "a very simple network, with a 28x28 binary image as input" to predict the digit class [BatchNorm, p.5], they compared training with and without BN and examined the distribution of inputs to a sigmoid unit over training. They report: "Batch Normalization makes the distribution more stable and reduces the internal covariate shift" [BatchNorm, p.6, Fig. 1 caption], shown via the {15,50,85}th percentiles of the sigmoid input distribution staying far more stable over 10K–50K steps with BN than without [BatchNorm, p.6].

A second piece of evidence comes from the ImageNet/Inception experiments with a sigmoid nonlinearity: "We also verified that the reduction in internal covariate shift allows deep networks with Batch Normalization to be trained when sigmoid is used as the nonlinearity, despite the well-known difficulty of training such networks. Indeed, BN-x5-Sigmoid achieves the accuracy of 69.8%. Without Batch Normalization, Inception with sigmoid never achieves better than 1/1000 accuracy" [BatchNorm, p.7].

## Reported training speed-up on ImageNet

- The abstract states: "Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps, and beats the original model by a significant margin" [BatchNorm, p.1].
- The results section details how this is reached:
  - "By only using Batch Normalization (BN-Baseline), we match the accuracy of Inception in less than half the number of training steps" [BatchNorm, p.7].
  - "By applying the modifications in Sec. 4.2.1, we significantly increase the training speed of the network. BN-x5 needs 14 times fewer steps than Inception to reach the 72.2% accuracy" [BatchNorm, p.7].
  - A further variant, BN-x30, trains somewhat slower initially but "reaches 74.8% after 6·10^6" steps, i.e., 5 times fewer steps than required by Inception to reach 72.2% [BatchNorm, p.7].

So the headline "14 times fewer steps" figure is **not from BN alone** but from the BN-x5 configuration, which combines BN with several other changes described in Sec. 4.2.1 "Accelerating BN Networks" [BatchNorm, p.6–7]:
- **Increase learning rate** — "we have been able to achieve a training speedup from higher learning rates, with no ill side effects" [BatchNorm, p.6].
- **Remove Dropout** — motivated by BN's regularizing effect [BatchNorm, p.5].
- **Reduce L2 weight regularization** (implied under "other modifications," though not separately quoted here beyond Dropout removal).
- **Accelerate the learning rate decay** — "we lower the learning rate 6 times faster" [BatchNorm, p.6].
- **Remove Local Response Normalization** — "we found that with Batch Normalization it is not necessary" [BatchNorm, p.6].
- **Shuffle training examples more thoroughly** — within-shard shuffling, giving "about 1% improvements in the validation accuracy" [BatchNorm, p.6].
- **Reduce the photometric distortions** — "we let the trainer focus on more 'real' images by distorting them less" [BatchNorm, p.6].

## What the paper itself says it has not established

In the Conclusion, the authors explicitly flag limits to what they have shown:
- "In this work, we have not explored the full range of possibilities that Batch Normalization potentially enables. Our future work includes applications of our method to Recurrent Neural Networks... where the internal covariate shift and the vanishing or exploding gradients may be especially severe, and which would allow us to more thoroughly test the hypothesis that normalization improves gradient propagation (Sec. 3.3)" [BatchNorm, p.8]. This indicates the gradient-propagation hypothesis has not been thoroughly tested (e.g., not on RNNs).
- "We plan to investigate whether Batch Normalization can help with domain adaptation, in its traditional sense" [BatchNorm, p.8] — i.e., this has not yet been established.
- "We believe that further theoretical analysis of the algorithm would allow still more improvements and applications" [BatchNorm, p.8] — indicating the theoretical underpinnings are not fully worked out.

The evidence given does not include a rigorous, quantitative measure of "internal covariate shift" itself (e.g., no explicit numerical metric of distributional shift is reported in these passages) — only qualitative distributional stability (Fig. 1) and indirect behavioral evidence (sigmoid trainability). This limitation is implicit in the authors' own acknowledgment that further theoretical analysis is still needed [BatchNorm, p.8].

**Retrieved:** BatchNorm p.7 (0.89); BatchNorm p.1 (0.88); BatchNorm p.2 (0.87); ViT p.11 (0.84); ResNet p.9 (0.83); BatchNorm p.8 (0.83); BatchNorm p.6 (0.82); BatchNorm p.6 (0.82); BatchNorm p.5 (0.82); BatchNorm p.2 (0.82); BatchNorm p.8 (0.82); BYOL p.13 (0.81); BatchNorm p.5 (0.81); BatchNorm p.8 (0.81); BatchNorm p.8 (0.81); BatchNorm p.7 (0.80); BatchNorm p.5 (0.80); BatchNorm p.7 (0.80); BatchNorm p.5 (0.80); BatchNorm p.4 (0.79); BatchNorm p.6 (0.78); ResNet p.4 (0.78); BatchNorm p.6 (0.78); MAE p.9 (0.78); BatchNorm p.2 (0.77); BatchNorm p.6 (0.77); BatchNorm p.6 (0.77) | gold page hit: 1.00
*27.5 s*

## Q09 (text-only, conceptual, hard, answerable: yes)

**Question.** According to the Temporal Straightening paper, why should reducing the curvature of latent trajectories make gradient-based planning easier, and do the paper's experiments generally show planning improving when the curvature regularizer is used?

**Reference answer.** Explanation (the main part). Planning minimises a Euclidean goal cost in latent space, and when latent trajectories are highly curved, straight-line distance misrepresents the geodesic distance along feasible transitions. A curvature regulariser (it penalises the angle between consecutive latent velocity vectors, i.e. maximises their cosine similarity, while a JEPA-style predictor is trained with stop-gradient on the target) straightens trajectories, which makes Euclidean latent distance a better proxy for geodesic distance and improves the conditioning of the planning objective. The theory covers linear latent dynamics: epsilon-straight transitions control the condition number of the planning Hessian, so gradient descent converges linearly at a rate set by the condition number; guarantees for nonlinear predictors are left to future work. As an illustration, the loss landscape is closer to convex after straightening (Figure 4). Experiments (general trend only). Yes: the paper reports open-loop planning success improving by 20-60% and MPC by 20-30% with a simple gradient-based planner, and says it observes a significant improvement across all models and environments. The improvement is not uniform in Table 1 (for example a from-scratch ResNet 1x384 on PointMaze-UMaze falls from 82.00 to 52.00 open-loop), so 'generally' is the right strength, in simulated goal-reaching tasks.

**System answer.** ## Why reducing curvature should ease gradient-based planning

**1. Euclidean distance becomes a better proxy for geodesic distance.**
When latent trajectories are highly curved, "straight-line distances in embedding space misrepresent the geodesic distance along feasible transitions" [TemporalStraightening, p.1, section: 1. Introduction]. Since planning typically uses a Euclidean-based goal cost (e.g., MSE to the target embedding), this misalignment misleads the optimizer. Straightening trajectories makes "the Euclidean distance in latent space a better proxy for the geodesic distance," so the cost function more accurately reflects true progress toward the goal [TemporalStraightening, p.1, section: Abstract; p.4, section: E.1. Distance Heatmaps/E.2.].

**2. It improves the conditioning of the planning objective / optimization landscape.**
The paper states that straightening "improves the conditioning of the planning objective" [TemporalStraightening, p.1, Abstract], and provides a theoretical analysis for linear dynamical systems showing that "reducing curvature improves convergence of gradient-based planners" [TemporalStraightening, p.2, section: 1. Introduction]. In their linear-system analysis, the planning Hessian is defined as H = ∇²_a L(a) = 2J_Φᵀ J_Φ ⪰ 0, where J_Φ depends on the dynamics matrices A, B [TemporalStraightening, p.5, section: 4. Planning with Straightened Dynamics] — curvature regularization shapes this Jacobian structure to make the objective less ill-conditioned for gradient descent.

**3. Empirically, it reduces non-convexity of the loss landscape.**
"We observe that straightening yields a loss landscape with reduced non-convexity under nonlinear dynamics" [TemporalStraightening, p.5, section: 4. Planning with Straightened Dynamics], which directly supports why gradient-based (as opposed to search-based) planners should perform better and more stably.

## Do the experiments generally show planning improving with the curvature regularizer?

Yes — the paper reports consistent, often large gains:

- **Headline numbers:** "open-loop planning success improves by 20–60% and MPC by 20–30% with a simple gradient-based planner" [TemporalStraightening, p.2, section: 1. Introduction].
- **Specific example:** "UMaze's open-loop success rate is improved from 44% to 94% with the projector, and 14.67% to 64.67% when training a ResNet from scratch" [TemporalStraightening, p.8, section: 5.3. Planning].
- **Near-perfect MPC results:** "our model reaches 100% success with MPC on Wall and UMaze within only a few steps" [TemporalStraightening, p.8, section: 5.3. Planning].
- **Consistency across methods:** "straightening consistently improves both GD and CEM across environments and model architectures," and importantly "largely reduces the performance gap between GD and CEM," indicating gradient-based planning specifically benefits and approaches the quality of the more expensive search-based CEM [TemporalStraightening, p.14, section: B.2. Hyperparameters].
- **Comparison to alternative regularizers:** smoothness and temporal-contrastive objectives did *not* reliably improve planning ("we do not observe improvements from adding smoothness or temporal contrastive objectives... larger weights generally hurt performance"), whereas straightening was "significantly more effective" [TemporalStraightening, p.15, section: B.5; p.8, section: 5.3].
- **Qualitative evidence:** In Teleported-PointMaze, "With straightening, the agent reaches the target within given step limit," while "without straightening, the agent gets stuck at the corner" [TemporalStraightening, p.29, section: F. Teleported-PointMaze].

One caveat noted in the evidence: for PushT, "success increases more slowly because we apply only the terminal loss within the horizon H = 5, yet straightening still yields substantial final gains" [TemporalStraightening, p.8, section: 5.3. Planning] — so the magnitude of improvement varies by environment/setup, but the direction (improvement) is consistent across all reported cases in the passages provided.

**Retrieved:** TemporalStraightening p.1 (0.88); TemporalStraightening p.2 (0.86); TemporalStraightening p.9 (0.86); TemporalStraightening p.22 (0.81); TemporalStraightening p.19 (0.81); TemporalStraightening p.3 (0.80); TemporalStraightening p.4 (0.80); TemporalStraightening p.29 (0.79); TemporalStraightening p.10 (0.79); TemporalStraightening p.7 (0.79); TemporalStraightening p.14 (0.78); TemporalStraightening p.11 (0.78); TemporalStraightening p.5 (0.78); TemporalStraightening p.16 (0.78); TemporalStraightening p.24 (0.78); TemporalStraightening p.20 (0.77); TemporalStraightening p.21 (0.77); TemporalStraightening p.26 (0.77); TemporalStraightening p.19 (0.77); TemporalStraightening p.15 (0.77); TemporalStraightening p.5 (0.77); TemporalStraightening p.25 (0.76); TemporalStraightening p.3 (0.76); TemporalStraightening p.12 (0.76); TemporalStraightening p.6 (0.76); TemporalStraightening p.8 (0.76); TemporalStraightening p.4 (0.76); TemporalStraightening p.1 (0.75) | gold page hit: 1.00
*17.3 s*

## Q11 (text-only, cross-paper, medium, answerable: yes)

**Question.** ViT says it follows the original Transformer 'as closely as possible'. Which parts of the Transformer encoder does ViT keep, and how does its encoder differ from the one in 'Attention Is All You Need' (input handling, position information, normalisation placement, feed-forward activation)?

**Reference answer.** ViT keeps the Transformer encoder structure of alternating multi-head self-attention and position-wise MLP/feed-forward blocks with residual connections and layer normalisation, and uses the encoder only. Differences: (1) input - ViT splits an image into patches, linearly projects them and prepends a learnable [class] token, whereas the Transformer embeds discrete input tokens; (2) position information - ViT uses standard learnable 1D position embeddings, the Transformer uses fixed sinusoidal encodings (though it found learned embeddings nearly identical); (3) normalisation - the Transformer computes LayerNorm(x + Sublayer(x)) after the residual addition, while ViT applies layer norm before every block and residual connections after every block; (4) the feed-forward layer uses ReLU in the Transformer and GELU in ViT. The Transformer paper additionally has a decoder with encoder-decoder attention.

**System answer.** Based on the passages provided, here is what the evidence does and does not establish about ViT's encoder relative to the original Transformer:

**What ViT keeps (explicitly stated):**
ViT's "Transformer encoder (Vaswani et al., 2017) consists of alternating layers of multiheaded self-attention (MSA, see Appendix A) and MLP blocks" [ViT, p.3]. So the core building blocks it retains from the original Transformer are:
- Multi-head self-attention layers
- MLP (feed-forward) blocks
- These are arranged in alternating fashion, as in the original encoder stack, which the Transformer paper describes as "stacked self-attention and point-wise, fully connected layers for both the encoder and decoder" [Transformer, p.3].

**Normalization placement (explicitly stated for ViT, but not contrasted in the passages with the original):**
ViT states: "Layernorm (LN) is applied before every block, and residual connections after every block (Wang et al., 2019; Baevski & Auli, 2019)" [ViT, p.3]. This tells us ViT uses a pre-norm design (LN before each sub-block). However, the passages given do **not** state what normalization placement the original "Attention Is All You Need" Transformer used, so the evidence does not let us confirm this is a difference — only that ViT made this specific choice and cited other works (not the original Transformer paper) as justification.

**Input handling (established for ViT only):**
ViT describes reshaping the image into "a sequence of flattened 2D patches," then using "a trainable linear projection" to map patches to D-dimensional "patch embeddings" [ViT, p.3]. The passages do not contain a description of how the original Transformer encoder in "Attention Is All You Need" handles its input embeddings (e.g., token embedding method), so no direct comparison can be drawn from the evidence — only that ViT's input is patch-based rather than token-based (implied by the overall framing in [ViT, p.1]: "a pure transformer applied directly to sequences of image patches").

**Position information:**
The passages discuss ViT's own ablation of different positional embedding schemes ("there is little to no difference between different ways of encoding positional information" for ViT-B/16) [ViT, p.18], but they do **not** describe or compare this to the positional encoding scheme used in the original Transformer paper. So this part of the question is **not established** by the given evidence.

**Feed-forward activation:**
None of the passages (from ViT or the Transformer paper) mention the activation function used in the feed-forward/MLP block for either model. This part of the question is **not established** by the given evidence.

**Summary:**
From the evidence, ViT retains the alternating multi-head self-attention + MLP block structure of the original Transformer encoder [ViT, p.3; Transformer, p.3]. The only explicitly stated encoder detail for ViT is that it applies LayerNorm before each block and places residual connections after each block [ViT, p.3]. However, the passages do not describe the original Transformer's normalization placement, input-embedding method (for contrast), positional-encoding method, or feed-forward activation function, so a full point-by-point comparison on those remaining aspects (input handling specifics, position information, and feed-forward activation) cannot be established from the evidence provided.

**Retrieved:** I-JEPA p.3 (0.77); ViT p.18 (0.75); ViT p.3 (0.75); Transformer p.5 (0.74); ViT p.20 (0.74); MAE p.11 (0.74); ViT p.8 (0.74); ViT p.1 (0.73); I-JEPA p.12 (0.73); ViT p.4 (0.73); ViT p.4 (0.73); MAE p.11 (0.73); ViT p.3 (0.73); ViT p.2 (0.72); MAE p.3 (0.72); ViT p.7 (0.72); ViT p.8 (0.72); ViT p.19 (0.72); Transformer p.2 (0.71); ViT p.8 (0.71); ViT p.5 (0.71); ViT p.3 (0.71); Transformer p.5 (0.71); Transformer p.10 (0.71); Transformer p.3 (0.71); Transformer p.10 (0.71) | gold page hit: 0.67
*29.2 s*

## Q12 (text-only, cross-paper, hard, answerable: yes)

**Question.** MAE and I-JEPA both mask parts of an image and use a ViT encoder on the visible part. What does each method predict and with what loss, and what evidence does the I-JEPA paper give that predicting in representation space matters?

**Reference answer.** MAE reconstructs the pixel values of the masked patches with a lightweight decoder (mean squared error computed only on masked patches); the encoder sees only visible patches and normalised pixels work slightly better (Table 1d, ViT-L/16: 85.4 vs 84.9 fine-tuning, 73.9 vs 73.5 linear probing). I-JEPA is non-generative: a predictor (narrow ViT) predicts the representations of target blocks from a context block, the targets come from a target encoder that is an exponential moving average of the context encoder, and the loss is average L2 distance in representation space. In I-JEPA's own ablation (Table 7, ViT-L/16, linear probe on 1% of ImageNet labels), using target-encoder outputs gave 66.9 top-1 versus 40.7 when the loss was in pixel space, and the authors say they 'conjecture' representation-space loss is a crucial component. I-JEPA also reports about 7% slower iterations than MAE but roughly 5x fewer iterations to converge. Caveat: the pixel-space variant is I-JEPA's own ablation (different epochs: 500 vs 800), not the MAE paper's setup, and MAE does not test representation-space targets.

**System answer.** ## What each method predicts

**MAE:**
- MAE "masks random patches from the input image and reconstructs the missing patches in the pixel space" [MAE, p.2, section 1. Introduction].
- The encoder (a ViT) "is applied only on visible, unmasked patches... Masked patches are removed; no mask tokens are used," while "the full set is handled by a lightweight decoder" [MAE, p.3, section 3. Approach] that reconstructs the missing patches in pixel space [MAE, p.2].
- The provided passages describe the target as pixel values but do not state the exact loss function (e.g., mean-squared error) used by MAE — that detail is not given in the excerpts.

**I-JEPA:**
- I-JEPA uses a context encoder, a target encoder, and a predictor. Given a context block, the predictor is asked "to predict the representations of various target blocks in the same image, where target representations are computed by a learned target-encoder network" [I-JEPA, p.2, section 1. Introduction].
- Crucially, the target blocks are produced by masking the *output* of the target encoder, not the input: "target blocks are obtained by masking the output of the target-encoder, not the input" [I-JEPA, p.14, section C. Additional Ablations].
- "I-JEPA is non-generative and the predictions are made in representation space" [I-JEPA, p.3, section 3. Method], and "the loss is computed entirely in representation space, thereby giving the target encoder the ability to produce abstract prediction targets, for which irrelevant pixel-level details are eliminated" [I-JEPA, p.7, section 9. Ablations]. The passages do not give the precise mathematical form of this loss (e.g., L2 distance) beyond stating it is computed in representation space.

## Evidence that predicting in representation space matters (from the I-JEPA paper)

1. **Direct ablation — pixel-space vs. representation-space loss (Table 7):** "Table 7 compares low-shot performance on 1% ImageNet-1K using a linear probe when the loss is computed in pixel-space versus representation space... predicting in pixel-space leads to a significant degradation in the linear probing performance" [I-JEPA, p.7, section 9. Ablations].

2. **Masking the target-encoder output vs. its input (Table 11):** "Masking the output of the target-encoder during pretraining results in more semantic prediction targets and improves linear probing performance" compared to masking the input and forward-propagating once per target region [I-JEPA, p.14, section C. Additional Ablations].

3. **Qualitative visualization evidence:** Decoding the I-JEPA predictor's representation-space outputs shows it "correctly capturing positional uncertainty and producing high-level object parts with a correct pose... while discard[ing] the precise low-level details as well as background information" [I-JEPA, p.8, section 9. Ablations]. Similarly, decoding the average-pooled target-encoder output shows it "correctly capture[s] the high-level information regarding objects and their poses" while discarding low-level details and background [I-JEPA, p.16–17, section E.1. Encoder Visualization].

4. **Downstream performance and efficiency comparisons:** I-JEPA, by predicting in representation space, "outperforms pixel-reconstruction methods such as MAE [36] on ImageNet-1K linear probing, semi-supervised 1% ImageNet-1K, and semantic transfer tasks" [I-JEPA, p.2, section 1. Introduction], and converges in "roughly 5× fewer iterations" than MAE despite a ~7% per-iteration overhead from computing targets in representation space [I-JEPA, p.6, section 7. Scalability].

Together, these ablations (Tables 7 and 11), the qualitative decoding experiments, and the comparative performance/efficiency results constitute the paper's evidence that predicting in an abstract representation space — rather than in pixel space — is central to I-JEPA's ability to learn more semantic representations.

**Retrieved:** I-JEPA p.2 (0.78); I-JEPA p.14 (0.78); I-JEPA p.7 (0.78); I-JEPA p.5 (0.77); I-JEPA p.5 (0.77); I-JEPA p.2 (0.77); I-JEPA p.16 (0.77); I-JEPA p.6 (0.77); I-JEPA p.8 (0.76); I-JEPA p.1 (0.76); I-JEPA p.16 (0.76); I-JEPA p.3 (0.76); I-JEPA p.17 (0.75); I-JEPA p.6 (0.75); MAE p.3 (0.75); I-JEPA p.8 (0.75); I-JEPA p.7 (0.75); I-JEPA p.16 (0.75); I-JEPA p.2 (0.74); I-JEPA p.15 (0.74); MAE p.7 (0.74); MAE p.2 (0.74); I-JEPA p.12 (0.74); I-JEPA p.6 (0.74); I-JEPA p.2 (0.73); I-JEPA p.2 (0.73); I-JEPA p.4 (0.73) | gold page hit: 0.67
*23.1 s*

## Q13 (text-only, cross-paper, hard, answerable: yes)

**Question.** Distillation and BYOL both train one network to match another network's outputs. According to the two papers, what supplies the targets in each case and how does that target model come about, are labels used, and what does BYOL say about the 'mean teacher' method that it treats as closest to its slow-moving-average target?

**Reference answer.** Distillation: the targets are class probabilities from an already-trained 'cumbersome' model (an ensemble, or a single very large model trained with a strong regularizer such as dropout), softened by raising the softmax temperature. The small model is trained at the same high temperature on a transfer set and uses temperature 1 afterwards; when labels are known the objective is a weighted average of cross-entropy with the soft targets and with the correct labels, with a considerably lower weight on the label term. BYOL: the targets are the projections a target network produces for a second augmented view; the target's weights are an exponential moving average of the online network's weights (a slow-moving average of the learner itself, not a separately trained larger model), the loss gradient is not propagated into the target (stop-gradient), and an extra predictor sits only on the online branch. BYOL is a self-supervised method that works without negative pairs. BYOL describes mean teacher (MT) as also using a slow-moving-average 'teacher' to produce targets for an online 'student', with an l2 consistency loss between their softmax predictions added to a classification loss; it reports that a similar approach collapses when the classification loss is removed, whereas BYOL's added predictor prevents collapse.

**System answer.** ## Source of targets in each method

**Distillation:** The targets are the soft output probabilities (soft target distribution) produced by a large, already-trained "cumbersome model" — either a single large highly regularized model or an ensemble of models — run at a high softmax temperature. "In the simplest form of distillation, knowledge is transferred to the distilled model by training it on a transfer set and using a soft target distribution for each case in the transfer set that is produced by using the cumbersome model with a high temperature in its softmax" [Distillation, p.3, Abstract]. This cumbersome/teacher model is trained separately and beforehand (e.g., as an ensemble of 10 models trained on hard labels), and its outputs are then transferred to the smaller distilled model: "our distillation approach is able to extract more useful information from the training set than simply using the hard labels to train a single model... the improvement in WER achieved by the ensemble is transferred to the distilled model" [Distillation, p.5]. So here hard labels ARE used — but to train the teacher model first; the student is then trained primarily on the teacher's soft targets (optionally combined with hard labels, as temperature reverts to 1 at deployment and training uses the high-temperature soft targets) [Distillation, p.3, Abstract; p.5].

**BYOL:** The targets come from a **target network** that has the identical architecture to the online network but a different set of weights ξ, which are not learned by gradient descent but are an **exponential moving average (EMA) of the online network's own weights θ**: "its parameters ξ are an exponential moving average of the online parameters θ" [BYOL, p.3, section 3.1]. No separate pre-trained model and no labels are used to produce these targets — they are "bootstrapped" from the network's own evolving representation: "we propose to directly bootstrap the representations... BYOL trains its online network to predict the target network's representation of another augmented view of the same image" [BYOL, p.2, Abstract]. The whole training pipeline is label-free (self-supervised); BYOL is only evaluated afterward using labels in the linear-evaluation/semi-supervised protocols [BYOL, p.2, Abstract], but the target-generation process itself uses no labels.

## BYOL's comparison to Mean Teacher

BYOL explicitly identifies Mean Teacher (MT) as the closest existing approach using a slow-moving average target network, but highlights two key differences:

1. **Mean Teacher is semi-supervised and uses labels; BYOL does not.** "In the semi-supervised setting..., an unsupervised loss is combined with a classification loss over a handful of labels... mean teacher (MT) also uses a slow-moving average network, called teacher, to produce targets for an online network, called student. An ℓ2 consistency loss between the softmax predictions of the teacher and the student is added to the classification loss" [BYOL, p.3, section 2].

2. **Without the classification loss, the MT-style approach collapses, whereas BYOL does not — because of BYOL's added predictor.** "While [20] demonstrates the effectiveness of MT in the semi-supervised learning case, in Section 5 we show that a similar approach collapses when removing the classification loss. In contrast, BYOL introduces an additional predictor on top of the online network, which prevents collapse" [BYOL, p.3, section 2].

This is reiterated later: "Removing the predictor in BYOL results in an unsupervised version of MT with no classification loss that" [collapses, continuing the ablation discussion] [BYOL, p.9, section 5]. Also note a structural difference: MT's consistency loss is computed directly on softmax/logit outputs of student vs. teacher [BYOL, p.3, section 2], whereas BYOL's online network has an extra predictor stage (fθ → gθ → qθ) beyond what the target network computes (fξ → gξ only) [BYOL, p.3, section 3.1], and BYOL's loss operates on projected representations rather than classification logits.

**Summary:** Distillation's targets come from an externally, separately pre-trained (and possibly label-trained) cumbersome teacher model's soft softmax outputs at high temperature [Distillation, p.3, p.5]. BYOL's targets come from an EMA of the online network's own weights, requiring no separate teacher and no labels [BYOL, p.3, section 3.1; p.2, Abstract]. BYOL treats Mean Teacher as the closest prior slow-moving-average-target method, but notes MT requires a classification loss on labels and collapses without it, whereas BYOL avoids collapse via its predictor and remains fully unsupervised [BYOL, p.3, section 2].

**Retrieved:** BYOL p.3 (0.78); BYOL p.3 (0.77); BYOL p.3 (0.77); Distillation p.5 (0.75); BYOL p.3 (0.75); BYOL p.2 (0.74); Distillation p.8 (0.74); BYOL p.10 (0.74); BYOL p.2 (0.74); BYOL p.3 (0.74); BYOL p.6 (0.74); BYOL p.2 (0.73); BYOL p.8 (0.73); BYOL p.5 (0.73); BYOL p.26 (0.73); Distillation p.5 (0.73); Distillation p.3 (0.73); BYOL p.9 (0.73); BYOL p.20 (0.73); BYOL p.25 (0.73); BYOL p.30 (0.72); BYOL p.28 (0.72) | gold page hit: 0.33
*18.5 s*

## Q14 (text-only, cross-paper, medium, answerable: yes)

**Question.** Temporal Straightening's world model uses a ResNet encoder, a ViT predictor and stop-gradient on the target latent. What does the Straightening paper say about how it uses each, and what does each originating paper (ResNet, ViT, BYOL) say that the component is designed to do?

**Reference answer.** Temporal Straightening offers two encoder setups, one being a ResNet (He et al.) trained from scratch, and uses a ViT (Dosovitskiy et al.) as the dynamics predictor with a temporal causal attention mask for frame-level autoregressive prediction. For collapse prevention it applies stop-gradient to the target latent in the prediction loss, citing Grill et al. 2020 (the BYOL paper) among stop-gradient methods, chosen because it needs no negative samples or extra hyper-parameters; it concedes collapse is still possible in theory but says stop-gradient worked in its experiments. In the originating papers: ResNet introduces residual learning, letting stacked layers fit F(x) = H(x) - x via shortcut connections to ease optimisation of deeper networks (the degradation problem); ViT processes a sequence of image-patch embeddings with a standard Transformer encoder of alternating self-attention and MLP blocks; and BYOL trains an online network to predict a stop-gradient target network's representation without negative pairs, which it hypothesises depends on both a predictor and a slow-moving-average target (its representation collapses if either is removed).

**System answer.** Based strictly on the passages provided, here is what the evidence does and does not establish.

## What the Temporal Straightening paper says about each component

**ResNet (encoder)**
The paper uses ResNet as one of the encoder architecture options, trained either from scratch or as a backbone alongside a projector, with its own learning rate in the training hyperparameters (Projector/ResNet lr = 1e-5, or 1e-6 without straightening) [TemporalStraightening, p.14]. It is evaluated with two feature types — "ResNet - spatial" and "ResNet - global" — under both straightening=True/False conditions in the distance-heatmap experiments [TemporalStraightening, p.21]. In planning results, straightening improves ResNet performance substantially: open-loop success on UMaze rises "from 44% to 94% with the projector, and 14.67% to 64.67% when training a ResNet from scratch" [TemporalStraightening, p.8]. The paper also notes "abnormally low success rates" for ResNet with spatial features on Wall, PointMaze-UMaze, and PointMaze-Medium [TemporalStraightening, p.7]. There is no statement in these passages about what the ResNet encoder is designed to do beyond serving as a visual feature extractor option for the world model.

**Predictor**
The world model "consists of three components: a sensory encoder, an action encoder, and a predictor" [TemporalStraightening, p.3]. The predictor fθ is trained jointly with the encoders Esϕ and Eaψ "to minimize prediction error and enforce straightened trajectories," specifically by minimizing "the MSE between the predicted and target latent states ẑt+1 and zt+1" [TemporalStraightening, p.4]. During planning, the paper "roll[s] out for the horizon T using the trained predictor and select[s] optimal actions that minimize the cost between the predicted terminal state and the goal in the embedding space" [TemporalStraightening, p.3]. **The provided passages do not identify the predictor as a ViT** — DINOv2 (a ViT-based model) appears only as an encoder option (e.g., "DINOv2 + spatial proj," "DINOv2 CLS embedding," "DINOv2 patch embedding") [TemporalStraightening, p.21], not as the predictor. No passage states that a ViT is used as the predictor.

**Stop-gradient on the target latent**
"We minimize the prediction loss between the predicted embedding ẑt t and the target zt t with stop-grad in the target branch, and minimize the local curvature of embeddings" [TemporalStraightening, p.3]. This is stated only as a training-objective detail (preventing the target branch from being updated via the prediction loss); no elaboration of its purpose is given beyond this.

## What the "originating papers" (ResNet, ViT, BYOL) say

**None of the supplied passages are excerpts from the original ResNet paper, the original ViT paper, or the BYOL paper.** All 30 passages are from "Temporal Straightening for Latent Planning." The only indirect connections are:
- A reference list entry noting a loosely related prior work on learning linearized representations by curvature regularization, Goroshin et al. 2015 [TemporalStraightening, p.14 / "S. D4rl" section], and a related-work discussion of "early work on learning linearized video representations also regularizes the curvature of latent trajectories (Goroshin et al., 2015)" [TemporalStraightening, p.3] — but this is not the ResNet, ViT, or BYOL paper.
- No passage cites or quotes He et al. (ResNet), Dosovitskiy et al. (ViT), or Grill et al. (BYOL) describing their components' intended design purpose (e.g., residual learning, patch-based self-attention, or stop-gradient as a collapse-prevention mechanism in self-supervised learning).

**Conclusion:** The evidence establishes how Temporal Straightening uses a ResNet as an encoder option and how it applies stop-gradient to the target branch in its prediction loss, and describes the predictor's general role in the JEPA world model — but it does **not** establish that the predictor is a ViT, nor does it contain any statements from the original ResNet, ViT, or BYOL papers about what those components are designed to do. Answering those parts would require passages from those source papers, which are not present in the provided evidence.

**Retrieved:** TemporalStraightening p.1 (0.78); TemporalStraightening p.14 (0.78); TemporalStraightening p.3 (0.78); TemporalStraightening p.19 (0.78); TemporalStraightening p.21 (0.78); TemporalStraightening p.4 (0.78); TemporalStraightening p.10 (0.77); TemporalStraightening p.7 (0.77); TemporalStraightening p.16 (0.77); TemporalStraightening p.15 (0.76); TemporalStraightening p.3 (0.76); TemporalStraightening p.6 (0.76); TemporalStraightening p.29 (0.76); TemporalStraightening p.11 (0.76); TemporalStraightening p.24 (0.75); TemporalStraightening p.12 (0.75); TemporalStraightening p.22 (0.75); TemporalStraightening p.26 (0.75); TemporalStraightening p.8 (0.75); TemporalStraightening p.3 (0.75); TemporalStraightening p.6 (0.75); TemporalStraightening p.2 (0.75); TemporalStraightening p.25 (0.74); TemporalStraightening p.20 (0.74); TemporalStraightening p.3 (0.74); TemporalStraightening p.27 (0.74); TemporalStraightening p.19 (0.74); TemporalStraightening p.7 (0.74); TemporalStraightening p.2 (0.73); TemporalStraightening p.13 (0.73) | gold page hit: 0.20
*32.1 s*

## Q15 (text-only, cross-paper, hard, answerable: yes)

**Question.** BabyCL's visual branch applies strong augmentations to two views of each frame. Compare the Gaussian-blur and solarization probabilities it uses for its two views with those BYOL uses for its two views, and say what the two papers report about whether negative pairs are needed.

**Reference answer.** BabyCL (Appendix A): two views per frame with strong augmentation: random resized crop to 224x224 (scale 0.2-1.0), horizontal flip, color jitter, random grayscale (0.2), Gaussian blur with probability 1.0 on view 1 and 0.1 on view 2, and solarization on view 2 with probability 0.2. BYOL (Appendix B, Table 6): Gaussian blur probability 1.0 for the first view (T) and 0.1 for the second (T'), solarization 0.0 for T and 0.2 for T', color dropping (grayscale) 0.2 for both, crops covering 8%-100% of the image. The blur, solarization and grayscale probabilities therefore match, while the lower bound of the crop scale differs (0.2 versus 8%), and BabyCL does not cite BYOL for these settings. Negatives: BabyCL's instance loss is a SimCLR objective and its cross-modal loss a symmetric InfoNCE, and it cites Zhuang et al. (2021) as finding that contrastive methods with negative sampling are most effective on SAYCam. BYOL reports state-of-the-art ImageNet results without negative pairs and finds it much less affected than SimCLR when color distortion is removed from the augmentations. Neither paper tests a BYOL-style objective in a streaming child-egocentric setting.

**System answer.** ## Gaussian-blur and solarization probabilities

**BabyCL** (for its two SSL views of a frame):
- View 1: Gaussian blur applied with probability **1.0**; no solarization mentioned.
- View 2: Gaussian blur applied with probability **0.1**; solarization applied with probability **0.2**.
[BabyCL, p.14]

**BYOL** (in its symmetric-parameter ablation, where both views T and T′ use the same settings):
- Both views: Gaussian blur with probability **0.5**, solarization with probability **0.2**.
[BYOL, p.26]

So BabyCL uses an *asymmetric* blur schedule across its two views (1.0 vs. 0.1), with solarization only on view 2 (p=0.2) and none on view 1. BYOL's reported symmetric ablation instead applies the *same* blur probability (0.5) and solarization probability (0.2) to both views [BYOL, p.26]. (Note: the passages do not give BYOL's default/asymmetric augmentation probabilities — only this symmetric-ablation setting — so a fully like-for-like comparison with BYOL's baseline recipe is not established by the evidence provided.)

## Whether negative pairs are needed

- **BYOL** explicitly states it learns representations "without using negative pairs" [BYOL, p.2, Abstract] and attributes its superior robustness to augmentation changes partly to this: "we suspect that not relying on negative pairs is one of the leading reasons for its improved robustness" [BYOL, p.2]. It also reports that removing color distortion hurts contrastive methods (e.g., SimCLR) far more than BYOL (−22.2 vs. −9.1 accuracy points) [BYOL, p.8], reinforcing that BYOL does not require negative pairs to avoid collapse or maintain performance.

- **BabyCL**, by contrast, uses a **SimCLR-style objective** for its visual branch, employing **NT-Xent** (normalized temperature-scaled cross-entropy) on paired augmented views [BabyCL, p.14, "streaming visual branch"], and its training objectives section confirms the "Instance loss ℒ𝐼" is "a SimCLR objective... on augmented views of frames" [BabyCL, p.4]. NT-Xent/SimCLR is a contrastive loss that relies on negative pairs within the batch to push apart dissimilar instances. The passages do not state that BabyCL avoids negative pairs — on the contrary, its described loss formulation (SimCLR/NT-Xent) is a negative-pair-based contrastive method, in contrast to BYOL's explicit claim of not needing negative pairs.

**Summary**: BabyCL applies asymmetric blur (1.0 vs. 0.1) and solarization (0 vs. 0.2) across its two views [BabyCL, p.14], while BYOL's reported symmetric setting uses equal blur (0.5) and solarization (0.2) probabilities for both views [BYOL, p.26]. On negative pairs, BYOL explicitly reports it does not need them [BYOL, p.2], whereas BabyCL's visual branch is built on a SimCLR/NT-Xent contrastive objective [BabyCL, p.4, p.14], which the evidence does not describe as negative-pair-free — the passages do not explicitly discuss whether BabyCL considers negative pairs necessary, but its method description relies on the standard contrastive (negative-pair-based) SimCLR formulation.

**Retrieved:** BabyCL p.14 (0.82); BYOL p.26 (0.80); BYOL p.2 (0.78); BabyCL p.14 (0.77); BabyCL p.9 (0.77); BYOL p.1 (0.77); BabyCL p.6 (0.76); BabyCL p.14 (0.76); BabyCL p.9 (0.76); BYOL p.8 (0.76); BYOL p.8 (0.76); BabyCL p.8 (0.75); BYOL p.7 (0.75); BYOL p.2 (0.75); BabyCL p.4 (0.75); BabyCL p.14 (0.74); BabyCL p.5 (0.74); BabyCL p.9 (0.74); BabyCL p.7 (0.74); BabyCL p.6 (0.74) | gold page hit: 0.57
*15.6 s*

## Q16 (text-only, cross-paper, hard, answerable: yes)

**Question.** Daily Oracle uses a particular retriever in its retrieval-augmented setting. What is it, and what does the embedding-retrieval paper report about how that type of retriever behaves compared with dense embedding models on its LIMIT task?

**Reference answer.** Daily Oracle's constrained open-book setting uses BM25 to retrieve the top 5 articles per question, each truncated to 512 words, restricted to articles available before the resolution date and RAG cutoff. The embedding-retrieval paper finds that on LIMIT, state-of-the-art dense single-vector models struggle (full setting rarely reaches even 20% recall@100; on the 46-document version they cannot solve the task even at recall@20), whereas BM25 'comes close to perfect scores'. The authors attribute this to sparse models behaving like single vectors with very high dimensionality, but add that it is unclear how to apply sparse models to instruction-following or reasoning tasks without lexical overlap. The LIMIT result concerns a synthetic combinatorial task and says nothing about Daily Oracle's news-forecasting data.

**System answer.** Based on the passages provided, I cannot fully answer this question — the evidence does not specify what retriever Daily Oracle uses in its RAG setting.

**What the passages do show:**
- Daily Oracle has a retrieval-augmented setting: "RAG mitigates the effect of outdated knowledge, [but] a strong and noticeable decline remains" [DailyOracle, p.9]. It also has a separate "gold article" setting where the source article is given directly, which is explicitly distinguished from the RAG setting [DailyOracle, p.7].
- None of the supplied Daily Oracle passages (sections 1, 2, 3.2, 4.2, 5) name the specific retriever (e.g., BM25, a dense embedder, etc.) used to fetch documents in that RAG setting.

**On the embedding-retrieval paper (EmbeddingLimits) and LIMIT:**
- The passages describe LIMIT as a dataset designed to stress-test *dense, single-vector embedding models*, showing "even state-of-the-art models fail on this dataset despite the simple nature of the task" [EmbeddingLimits, p.1], and that this stems from a theoretical limit on the number of top-k document combinations a fixed-dimension embedding can represent [EmbeddingLimits, p.12].
- The passages recommend alternatives to single-vector dense embeddings — "such as cross-encoders or multi-vector models" [EmbeddingLimits, p.3] — to handle the full range of instruction-based queries, but none of the provided passages report a direct empirical comparison of BM25 (or any sparse/lexical retriever) against dense embedding models' performance specifically on the LIMIT task.

**Conclusion:** The evidence given does not establish (a) which specific retriever Daily Oracle uses in its RAG setting, or (b) any reported comparison in the EmbeddingLimits paper between that retriever type and dense embedding models on LIMIT. What the passages do establish is that Daily Oracle's RAG setting reduces but does not eliminate performance decline from outdated knowledge [DailyOracle, p.9], and that EmbeddingLimits shows dense single-vector embedding models fail on LIMIT due to a dimensionality-based representational limit, suggesting non-single-vector alternatives (cross-encoders, multi-vector models) as potential fixes [EmbeddingLimits, p.3, p.12].

**Retrieved:** DailyOracle p.4 (0.74); DailyOracle p.2 (0.74); EmbeddingLimits p.3 (0.74); DailyOracle p.3 (0.73); DailyOracle p.3 (0.73); SWE-bench p.5 (0.72); EmbeddingLimits p.1 (0.72); DailyOracle p.10 (0.72); DailyOracle p.9 (0.72); DailyOracle p.1 (0.71); SWE-bench p.6 (0.71); SWE-bench p.25 (0.71); EmbeddingLimits p.8 (0.71); DailyOracle p.7 (0.71); EmbeddingLimits p.12 (0.71); EmbeddingLimits p.1 (0.71); DailyOracle p.3 (0.70); EmbeddingLimits p.2 (0.70); DailyOracle p.4 (0.70); SWE-bench p.30 (0.70); EmbeddingLimits p.3 (0.70); SWE-bench p.26 (0.70); EmbeddingLimits p.2 (0.70); EmbeddingLimits p.12 (0.70); EmbeddingLimits p.7 (0.70); EmbeddingLimits p.16 (0.69); SWE-bench p.6 (0.69) | gold page hit: 0.40
*19.9 s*

## Q17 (text-only, cross-paper, medium, answerable: yes)

**Question.** Daily Oracle and FIRE-Bench both use LLMs inside their evaluation pipelines. How does each validate that automated component against human judgment, and what agreement numbers does each report?

**Reference answer.** Daily Oracle validated its LLM-based QA filtering: four human annotators rated 30 TF and 30 MC sampled QA pairs on the seven filtering principles; inter-annotator agreement was fair (average Fleiss' kappa 0.26), and the LLM scores matched the human consensus with 89.52% accuracy across the seven principles and 85.00% for the final accept/reject decision (threshold of 13 points). FIRE-Bench validated its automated claim extraction and entailment-based scoring by human validation on a 33% subset of reference instances, reporting precision 0.95, recall 0.86 and F1 0.89. The two validate different components (question quality versus claim matching) with different metrics, so the numbers are not directly comparable.

**System answer.** Based on the provided passages, here's what can be established for each:

## Daily Oracle

Daily Oracle uses an LLM-based evaluator in its **QA Filtering** step of dataset construction [DailyOracle, p.4]. To validate this automated filtering step:

- "Four human annotators independently review a randomly sampled subset of Daily Oracle, consisting of 30 TF and 30 MC QA pairs. They follow the same instructions used to prompt the LLM and evaluate each QA pair based on the seven filtering principles listed in Appendix A.3." [DailyOracle, p.14]
- This is also referenced in the main text: "in Section 3.3, we conduct a human evaluation, similar to our QA filtering process, to verify the quality of the generated QA pairs." [DailyOracle, p.3]

**Agreement numbers:** The provided passages describe the human evaluation *procedure* (4 annotators, 30 TF + 30 MC pairs, same 7 filtering principles as the LLM) but **do not report a specific agreement number or statistic** (e.g., percentage agreement, Cohen's kappa) between the human annotators and the LLM filter. The evidence given does not establish this figure.

## FIRE-Bench

FIRE-Bench's core evaluation approach is different in kind: rather than validating an LLM-judge component against human raters, it uses human-authored findings as the ground-truth target that agent outputs are scored against:

- "Agent outcomes are evaluated by comparing synthesized conclusions against human-authored findings using claim-level precision, recall, and F1 scores." [FIRE-Bench, p.2]
- The reported headline result is agent performance against this human-grounded standard: "even the strongest reaches limited rediscovery success (<50 F1)" [FIRE-Bench, p.1], and "state-of-the-art agents reach only limited rediscovery success (<50 F1) with high run-to-run variance." [FIRE-Bench, p.9]

**Agreement numbers:** The passages do not describe a separate step where FIRE-Bench's automated/LLM-based scoring mechanism itself is validated against independent human judges (i.e., an inter-rater agreement check on the judge). The only "agreement-like" number provided is the **<50 F1** score, but this measures *agent* conclusions against human-authored findings, not the reliability of an automated judging component.

## Summary

| Benchmark | What's validated | Validation method | Agreement number in evidence |
|---|---|---|---|
| Daily Oracle | LLM-based QA filter | 4 human annotators re-check 30 TF + 30 MC pairs using same 7 principles [DailyOracle, p.14] | Not given in passages |
| FIRE-Bench | Agent-generated conclusions | Claim-level precision/recall/F1 against human-authored findings [FIRE-Bench, p.2] | <50 F1 for strongest agent [FIRE-Bench, p.1,9] (but this is agent performance, not judge-validation agreement) |

The evidence does not provide a numeric human-LLM agreement score for either benchmark's automated component specifically; it only shows the validation *procedure* for Daily Oracle and a *performance* metric (not a judge-agreement metric) for FIRE-Bench.

**Retrieved:** DailyOracle p.14 (0.74); DailyOracle p.1 (0.74); DailyOracle p.2 (0.74); DailyOracle p.10 (0.74); DailyOracle p.9 (0.73); DailyOracle p.3 (0.73); DailyOracle p.20 (0.73); FIRE-Bench p.2 (0.72); DailyOracle p.1 (0.72); DailyOracle p.3 (0.72); DailyOracle p.17 (0.72); DailyOracle p.15 (0.71); DailyOracle p.13 (0.71); DailyOracle p.29 (0.71); DailyOracle p.21 (0.71); FIRE-Bench p.10 (0.71); FIRE-Bench p.1 (0.71); FIRE-Bench p.5 (0.71); DailyOracle p.35 (0.70); DailyOracle p.11 (0.70); DailyOracle p.19 (0.70); DailyOracle p.18 (0.70); DailyOracle p.23 (0.70); DailyOracle p.6 (0.70); DailyOracle p.8 (0.70); DailyOracle p.3 (0.70); DailyOracle p.4 (0.70); FIRE-Bench p.1 (0.70); FIRE-Bench p.9 (0.70); DailyOracle p.16 (0.70) | gold page hit: 0.50
*21.6 s*

## Q18 (text-only, insufficient-evidence, medium, answerable: no)

**Question.** According to the distillation paper, what accuracy does a single network reach on the JFT dataset after the knowledge in the specialist models has been distilled back into it?

**Reference answer.** The supplied paper does not establish this. For JFT it reports an ensemble of a generalist baseline plus 61 specialist models whose predictions are combined at inference time (top-1 test accuracy 25.0% to 26.1%, a 4.4% relative improvement; conditional accuracy 43.1% to 45.9%), and it states 'We have not yet shown that we can distill the knowledge in the specialists back into the single large net'. A related idea (using soft targets to stop specialists overfitting) is described as one it is 'currently exploring'. Where the paper does distill, it reports MNIST and speech results (a single acoustic model recovering more than 80% of the frame-accuracy gain of a 10-model ensemble), not JFT.

**System answer.** The provided passages do not establish this. They report results on ensembles of specialist models combined with the baseline (e.g., 61 specialist models improving test accuracy from 25.0% to 26.1%, a 4.4% relative improvement [Distillation, p.7]), but none of the passages give a figure for the accuracy of a single distilled network after the specialists' knowledge has been distilled back into it on JFT. The paper mentions investigating ensembles of specialists "before investigating what happens when specialist models are distilled" [Distillation, p.6], implying such an experiment exists, but the actual distilled-single-model accuracy result for JFT is not present in the given passages.

**Retrieved:** Distillation p.7 (0.79); Distillation p.7 (0.79); Distillation p.7 (0.75); Distillation p.5 (0.75); Distillation p.8 (0.75); Distillation p.5 (0.75); Distillation p.7 (0.73); Distillation p.5 (0.73); ViT p.8 (0.73); Distillation p.4 (0.72); Distillation p.5 (0.72); Distillation p.3 (0.72); ViT p.2 (0.72); ResNet p.7 (0.72); Distillation p.5 (0.71); ViT p.7 (0.71); ViT p.15 (0.71); Distillation p.3 (0.71); ViT p.14 (0.71); Distillation p.1 (0.71); ViT p.15 (0.70); BatchNorm p.7 (0.70); BYOL p.27 (0.70); Distillation p.6 (0.70); MMLU p.7 (0.70) | gold page hit: 1.00
*6.4 s*

## Q20 (text-only, insufficient-evidence, easy, answerable: no)

**Question.** According to the SWE-bench paper, what resolve rate do agent-based systems (models that run code, navigate the repository and iterate) reach on SWE-bench?

**Reference answer.** The supplied paper does not establish this. It evaluates single-pass language models (ChatGPT-3.5, GPT-4, Claude 2 and others, and the fine-tuned SWE-Llama) that are given BM25-retrieved or oracle files and generate one patch, and its main-text resolve rates are all single-digit percentages (for example Claude 2 resolves 4.8% with oracle retrieval). Agent-based methods appear only as an intended direction: the task can serve as a level playing field for approaches 'ranging from retrieval and long-context models to decision-making agents', and the authors 'encourage future work to investigate different methods (e.g., agent-based approaches, tool augmented LMs)'. No agent results are reported.

**System answer.** The provided passages from the SWE-bench paper do not report a resolve rate specifically for agent-based systems (i.e., models that run code, navigate the repository, and iterate).

What the evidence does show is that the paper's actual experiments only evaluate two baseline approaches — a BM25 retrieval-based approach and an "oracle" retrieval approach — not agent-based methods [SWE-bench, p.4]. Under these baselines:

- Claude 2 resolves 1.96% of issues overall (the best-performing model in the main evaluation) [SWE-bench, p.1–2].
- With BM25 retrieval, Claude 2 resolves 1.96% of issues [SWE-bench, p.2].
- Per-repository "oracle" retrieval results show Claude 2 at 4.01% resolved and SWE-Llama 13b at 4.54% resolved [SWE-bench, p.27].

Regarding agent-based approaches specifically, the paper explicitly states these were *not* tested and are left for future work: "our experiments aim to establish a baseline of the simplest and most straight-forward approaches for this task; we do not intend to constrain future methodologies to the same type of approach and encourage future work to investigate different methods (e.g., **agent-based approaches**, tool augmented LMs)" [SWE-bench, p.10].

**Conclusion:** Based solely on the passages given, SWE-bench does not report a resolve rate for agent-based systems — the paper only evaluates retrieval-based (BM25 and oracle) methods, with the best result being Claude 2 at 1.96% (or up to ~4-4.5% under oracle retrieval settings). Agent-based evaluation is noted as a direction for future work, not something measured in this paper.

**Retrieved:** SWE-bench p.2 (0.76); SWE-bench p.16 (0.76); SWE-bench p.2 (0.76); SWE-bench p.1 (0.75); SWE-bench p.3 (0.75); SWE-bench p.6 (0.75); SWE-bench p.27 (0.75); SWE-bench p.4 (0.75); SWE-bench p.2 (0.74); SWE-bench p.10 (0.74); SWE-bench p.2 (0.74); SWE-bench p.26 (0.73); SWE-bench p.10 (0.73); SWE-bench p.3 (0.72); FIRE-Bench p.7 (0.72); SWE-bench p.9 (0.72); SWE-bench p.3 (0.72); SWE-bench p.1 (0.72); SWE-bench p.27 (0.72); SWE-bench p.24 (0.72); SWE-bench p.11 (0.72); SWE-bench p.51 (0.72); FIRE-Bench p.2 (0.72); FIRE-Bench p.6 (0.72) | gold page hit: 0.75
*9.3 s*

## Q31 (text+table, cross-source, medium, answerable: yes)

**Question.** The ViT paper says smaller patches make a Transformer more expensive. Using the sequence length it implies for 224-px inputs, how do the GMACs and measured throughput of ViT-Base with 32, 16 and 8 pixel patches compare with that expectation?

**Reference answer.** The ViT paper defines the number of patches (the Transformer's sequence length) as N = HW/P^2 and says smaller patch sizes are computationally more expensive. At 224 px that gives N = 49, 196 and 784 for P = 32, 16 and 8, i.e. 4x more tokens at each step. timm shows (parameters nearly constant: 88.22M, 86.57M, 86.58M): GMACs 4.41, 17.58 and 78.22, so 3.99x from B/32 to B/16 and 4.45x from B/16 to B/8; throughput 10,936.95, 2,992.79 and 700.85 samples/s, i.e. 3.65x slower and then 4.27x slower. Cost therefore grows roughly with token count while parameters stay flat; B/8 exceeds 4x in GMACs, which the paper does not explain.

**System answer.** ## The paper's claim

The ViT paper states that sequence length determines compute cost: "the Transformer's sequence length is inversely proportional to the square of the patch size, thus models with smaller patch size are computationally more expensive" [ViT, p.5]. The sequence length itself is defined as N = HW/P² [ViT, p.3].

## Step 1: Implied sequence lengths at 224×224 input

For H = W = 224:

- P = 32: N = (224×224)/32² = 50176/1024 = **49**
- P = 16: N = 50176/16² = 50176/256 = **196**
- P = 8: N = 50176/8² = 50176/64 = **784**

As predicted, halving the patch size quadruples N each time:
- N₁₆/N₃₂ = 196/49 = **4.0×**
- N₈/N₁₆ = 784/196 = **4.0×**

(exactly matching the inverse-square relationship, since (32/16)² = (16/8)² = 4)

## Step 2: Measured GMACs (from the timm benchmark query)

| arch | patch | GMACs |
|---|---|---|
| vit_base_patch32_224 | 32 | 4.41 |
| vit_base_patch16_224 | 16 | 17.58 |
| vit_base_patch8_224 | 8 | 78.22 |

Ratios:
- 17.58 / 4.41 = **3.99×**
- 78.22 / 17.58 = **4.45×**

So the *measured* compute (GMACs) grows by roughly 4× each time the patch size halves — this closely tracks the ~4× growth predicted for N itself, confirming the direction and rough magnitude of the "smaller patch = more expensive" claim. Note, however, that if cost scaled with full quadratic self-attention (O(N²)), we would expect ~16× growth (4²) per halving; the observed ~4× growth indicates that at ViT-Base's hidden size (D=768), overall MACs scale closer to *linearly* with N (dominated by the linear/MLP projections, O(N·D²)) rather than quadratically with N (O(N²·D)) — still consistent with the paper's qualitative "more expensive" claim, but not quadratically explosive in this regime.

## Step 3: Measured throughput (samples_per_sec)

| arch | patch | samples/sec |
|---|---|---|
| vit_base_patch32_224 | 32 | 10936.95 |
| vit_base_patch16_224 | 16 | 2992.79 |
| vit_base_patch8_224 | 8 | 700.85 |

Slowdown factors:
- 10936.95 / 2992.79 = **3.65×** slower going from P=32→16
- 2992.79 / 700.85 = **4.27×** slower going from P=16→8

These slowdowns again closely parallel the ~4× sequence-length (and GMACs) increase predicted by N ∝ 1/P².

## Conclusion

The ViT paper's qualitative claim — that smaller patches (and thus longer sequences, N ∝ 1/P²) make the model more computationally expensive [ViT, p.5] — is borne out quantitatively by the timm benchmark data: both GMACs (~4.0× and ~4.45× increases) and the inverse of throughput (~3.65× and ~4.27× slowdowns) track the ~4× growth in implied sequence length at each patch-size halving (49→196→784). The magnitude match (~4×, not ~16×) suggests that for ViT-Base specifically, overall compute scales closer to linearly with sequence length rather than quadratically, which the passages do not explicitly address — they only state the inverse-square relationship for sequence length and the general conclusion that smaller patches are "computationally more expensive" [ViT, p.5], without specifying the exact compute-scaling exponent.

**Retrieved:** ViT p.5 (0.78); ViT p.16 (0.78); ViT p.8 (0.74); ViT p.2 (0.73); ViT p.19 (0.73); ViT p.18 (0.73); ViT p.7 (0.73); ViT p.3 (0.73); MAE p.7 (0.72); MAE p.7 (0.72); ViT p.7 (0.72); ViT p.20 (0.71); ViT p.6 (0.71); ViT p.5 (0.71); ViT p.4 (0.71); ViT p.5 (0.70); ViT p.7 (0.70); ViT p.2 (0.70); ViT p.8 (0.70); ViT p.6 (0.70); MAE p.4 (0.70) | gold page hit: 1.00
**SQL:** `SELECT     arch,     img_size,     param_count_m,     gmacs,     macts,     samples_per_sec,     step_time_ms,     batch_size FROM benchmark_infer WHERE arch IN ('vit_base_patch32_224', 'vit_base_patch16_224', 'vit_base_patch8_224')   AND img_size = 224 ORDER BY arch;` | overlap with reference result: 1.00
*45.7 s*

## Q32 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper reports FLOPs for its 18-, 34-, 50-, 101- and 152-layer networks. How do timm's measured GMACs at 224 px compare, and for which depth is the difference largest?

**Reference answer.** The paper's Table 1 gives 1.8, 3.6, 3.8, 7.6 and 11.3 billion FLOPs, and defines its FLOPs as multiply-adds. timm's infer_gmacs at 224 px are 1.82, 3.67, 4.11, 7.83 and 11.56, i.e. +1.1%, +1.9%, +8.2%, +3.0% and +2.3%. The largest difference is for resnet50 (4.11 vs 3.8, +8.2%). Neither PDF explains the gap, so the cause should not be asserted.

**System answer.** ## timm GMACs vs. paper‑reported FLOPs at 224 px

The ResNet paper explicitly reports FLOPs (multiply‑adds) for three of the five depths in the passages provided:

- 34‑layer: 3.6 billion FLOPs [ResNet, p.3, section 3.3. Network Architectures]
- 50‑layer: 3.8 billion FLOPs [ResNet, p.7, section: 5.71 ResNet-34 C]
- 152‑layer: 11.3 billion FLOPs [ResNet, p.7, section: 5.71 ResNet-34 C]

The paper's values for 18‑ and 101‑layer (1.8 and 7.6 billion, respectively) appear only inside the SQL query's `CASE` statement — they are not stated in any of the provided passages, so I cannot independently verify them from the text evidence.

Using the SQL query result (timm GMACs at img_size=224 vs. these paper FLOPs figures), the differences (timm − paper) are:

| arch | timm GMACs (224px) | paper FLOPs (billion) | diff |
|---|---|---|---|
| resnet50 | 4.11 | 3.8 | **0.31** |
| resnet152 | 11.56 | 11.3 | 0.26 |
| resnet101 | 7.83 | 7.6 | 0.23 |
| resnet34 | 3.67 | 3.6 | 0.07 |
| resnet18 | 1.82 | 1.8 | 0.02 |

In every case, timm's measured GMACs are slightly **higher** than the paper's reported FLOPs, with the gap ranging from 0.02 billion (resnet18) up to 0.31 billion (resnet50).

**Largest difference:** resnet50, with timm reporting 4.11 GMACs vs. the paper's 3.8 billion FLOPs — a difference of 0.31 (billion), per the SQL query result. This is larger than the differences for resnet152 (0.26) and resnet101 (0.23), even though those are deeper/higher-FLOP networks.

**Caveat:** The passages directly confirm the paper's 3.6, 3.8, and 11.3 billion FLOPs figures for the 34-, 50-, and 152-layer models respectively. The 1.8 and 7.6 billion figures for 18- and 101-layer models come only from the SQL query's hardcoded values, not from any passage text, so their accuracy as "paper-reported" numbers is not independently verifiable from the evidence given.

**Retrieved:** ResNet p.7 (0.80); ResNet p.7 (0.80); ResNet p.8 (0.76); ResNet p.5 (0.75); ResNet p.6 (0.75); ResNet p.7 (0.75); ResNet p.10 (0.73); ResNet p.6 (0.73); ResNet p.5 (0.73); ResNet p.7 (0.72); ResNet p.4 (0.72); ResNet p.7 (0.72); ResNet p.10 (0.72); ResNet p.8 (0.72); ViT p.16 (0.72); BYOL p.5 (0.71); ResNet p.4 (0.71); ResNet p.6 (0.71); BYOL p.6 (0.71); ResNet p.8 (0.71); BYOL p.6 (0.70); ResNet p.5 (0.70); ViT p.19 (0.70); ViT p.19 (0.70); ResNet p.2 (0.70); ResNet p.3 (0.70) | gold page hit: 1.00
**SQL:** `SELECT   arch,   img_size,   gmacs AS timm_gmacs_224,   CASE arch     WHEN 'resnet18' THEN 1.8     WHEN 'resnet34' THEN 3.6     WHEN 'resnet50' THEN 3.8     WHEN 'resnet101' THEN 7.6     WHEN 'resnet152' THEN 11.3   END AS paper_flops_ga_billion,   gmacs - CASE arch     WHEN 'resnet18' THEN 1.8     WHEN 'resnet34' THEN 3.6     WHEN 'resnet50' THEN 3.8     WHEN 'resnet101' THEN 7.6     WHEN 'resnet152' THEN 11.3   END AS diff FROM benchmark_infer WHERE arch IN ('resnet18','resnet34','resnet50','resnet101','resnet152')   AND img_size = 224 ORDER BY diff DESC;` | overlap with reference result: 0.69
*23.7 s*

## Q34 (text+table, cross-source, hard, answerable: yes)

**Question.** Among timm rows whose weights tag starts with 'mae', which has the highest ImageNet-R and ImageNet-A top-1, how do ImageNet-R and ImageNet-A top-1 change with model size across these rows, and what pre-training task does the MAE paper describe?

**Reference answer.** Six hiera_*_224.mae_in1k_ft_in1k rows are tagged mae. hiera_huge_224 is highest on ImageNet-R (64.967) and ImageNet-A (66.253) (and Sketch, 50.078), with 672.78M parameters. ImageNet-R and ImageNet-A top-1 both rise at every step with model size: R is 45.78 (tiny), 49.373 (small), 53.14 (base), 55.57 (base_plus), 60.29 (large), 64.967 (huge); A is 30.56, 36.453, 43.4, 49.24, 58.013, 66.253. The drop relative to clean top-1 on the same 200 classes also shrinks with size (R: -49.47 for tiny to -32.243 for huge; A: -65.04 to -31.717), so the larger models lose less under these shifts. The MAE paper describes pre-training that masks random patches (75% in its default) and reconstructs the missing pixels with an encoder that processes only the visible patches. Caveats: the six rows are one family (Hiera, all fine-tuned on ImageNet-1k at 224 px), so this is a trend across six rows, not a controlled test; the MAE paper's own encoder is a plain ViT, Hiera is not in the corpus, and what the timm tag implies about Hiera's recipe is not stated in the PDFs.

**System answer.** ## Highest ImageNet‑R and ImageNet‑A top‑1 among MAE‑tagged timm rows

From the SQL result (rows with `weights_tag LIKE 'mae%'`), the row with the highest values on **both** ImageNet‑R (`top1_r`) and ImageNet‑A (`top1_a`) is the same model:

- **hiera_huge_224.mae_in1k_ft_in1k**: param_count_m = 672.78, top1_r = 64.967, top1_a = 66.253

This is higher than every other mae‑tagged row on both metrics.

## How top1_r and top1_a change with model size

Sorting the six rows by `param_count_m`:

| model | params (M) | top1_r | top1_a |
|---|---|---|---|
| hiera_tiny_224 | 27.91 | 45.780 | 30.560 |
| hiera_small_224 | 35.01 | 49.373 | 36.453 |
| hiera_base_224 | 51.52 | 53.140 | 43.400 |
| hiera_base_plus_224 | 69.90 | 55.570 | 49.240 |
| hiera_large_224 | 213.74 | 60.290 | 58.013 |
| hiera_huge_224 | 672.78 | 64.967 | 66.253 |

Both `top1_r` and `top1_a` increase **monotonically** as parameter count increases, from tiny → huge. Numerically:
- top1_r rises from 45.78 → 64.967 (Δ = 64.967 − 45.78 = 19.187 points)
- top1_a rises from 30.56 → 66.253 (Δ = 66.253 − 30.56 = 35.693 points)

ImageNet‑A improves by a larger absolute margin than ImageNet‑R as model size scales up, but both metrics track model size positively and consistently across every size step in this table.

## Pre-training task described in the MAE paper

The MAE paper's passages in the provided evidence describe the method as a **masked, pixel-reconstruction self-supervised pre-training task**: the model is pre-trained to reconstruct image content, specifically normalized pixels, from masked inputs — e.g., "our MAE reconstructs normalized pixels and is pre-trained for 1600 epochs" [MAE, p.7]. It is characterized as a **pixel-based** approach, contrasted with token-based masked pre-training methods like BEiT: "The pixel-based MAE is better than or on par with the token-based BEiT, while MAE is much simpler and faster" [MAE, p.8]. After this self-supervised masked pre-training, representations are evaluated "with (i) end-to-end fine-tuning or (ii) linear probing" on ImageNet-1K [MAE, p.4].

**Note:** The provided passages do not include an explicit, detailed description of the masking mechanism itself (e.g., mask ratio, patch size, random masking procedure); the evidence only establishes that MAE pre-trains by reconstructing normalized pixels in a pixel-based (non-tokenized) manner, evaluated via fine-tuning or linear probing.

**Retrieved:** MAE p.2 (0.79); MAE p.7 (0.76); MAE p.12 (0.75); ViT p.7 (0.75); MAE p.4 (0.74); I-JEPA p.5 (0.74); I-JEPA p.5 (0.74); ViT p.6 (0.74); MAE p.8 (0.74); BYOL p.18 (0.74); ViT p.13 (0.74); ResNet p.6 (0.73); BYOL p.18 (0.73); ResNet p.4 (0.73); MAE p.7 (0.73); BatchNorm p.2 (0.73); ViT p.4 (0.73); ViT p.2 (0.73); ViT p.5 (0.73); MAE p.12 (0.72); BYOL p.6 (0.72) | gold page hit: 0.00
**SQL:** `SELECT model, arch, weights_tag, param_count_m, top1_r, top1_a FROM model_results WHERE weights_tag LIKE 'mae%' ORDER BY top1_r DESC, top1_a DESC;` | overlap with reference result: 0.49
*23.7 s*

## Q35 (text+table, cross-source, hard, answerable: yes)

**Question.** For ViT models released with the same augreg recipe tag, how much higher is ImageNet top-1 when the weights come from ImageNet-21k pre-training plus ImageNet-1k fine-tuning than when trained on ImageNet-1k only, is the gain similar for the Small and Base models, and is the pattern consistent in direction with what the ViT paper says about pre-training data?

**Reference answer.** In all six matched pairs the ImageNet-21k-then-1k weights are better, by 2.56 to 5.82 points: vit_base_patch16_224 +5.38 (84.534 vs 79.154), vit_base_patch16_384 +4.908, vit_base_patch32_224 +5.824, vit_base_patch32_384 +4.608, vit_small_patch16_224 +2.56, vit_small_patch16_384 +2.684. The gain is not the same for the two sizes: the four Base rows gain 4.6 to 5.8 points (mean 5.18) and the two Small rows 2.6 to 2.7 (mean 2.62). This is consistent in direction with the ViT paper, which says large-scale pre-training helps ('large scale training trumps inductive bias') and that larger models show their benefit only with more pre-training data. It is not a confirmation: the paper's evidence uses different pre-training sets (ImageNet, ImageNet-21k, JFT-300M) and includes ViT-Large, which has no pair here, and with only two sizes a size effect cannot be separated from other differences between the Small and Base models.

**System answer.** ## Calculation

From the SQL results:

**ViT-Base/16:**
- augreg_in21k_ft_in1k: 84.534
- augreg_in1k: 79.154
- Gain = 84.534 − 79.154 = **5.38 points**

**ViT-Small/16:**
- augreg_in21k_ft_in1k: 81.402
- augreg_in1k: 78.842
- Gain = 81.402 − 78.842 = **2.56 points**

## Is the gain similar across sizes?

No. The Base model gains roughly **twice as much** (5.38 pts) from ImageNet-21k pre-training + ImageNet-1k fine-tuning as the Small model does (2.56 pts). The larger model benefits more from the additional pre-training data under this same AugReg recipe.

## Is this consistent with the ViT paper's findings?

Yes, directionally. The ViT paper reports that larger models need more pre-training data to show their advantage: "When pre-trained on the smallest dataset, ImageNet, ViT-Large models underperform compared to ViT-Base models... Only with JFT-300M, do we see the full benefit of larger models" [ViT, p.6]. It also states more generally that "the convolutional inductive bias is useful for smaller datasets, but for larger ones, learning the relevant patterns directly from data is sufficient, even beneficial" [ViT, p.7], and that "large scale training trumps inductive bias" [ViT, p.2].

The timm/AugReg numbers show the same qualitative pattern at a smaller scale comparison (Small vs. Base rather than Base vs. Large/Huge): both models improve with more pre-training data (IN-21k vs IN-1k only), and the larger of the two models (Base) shows the bigger improvement — consistent in direction with the ViT paper's claim that bigger models benefit more from larger-scale pre-training data.

**Caveat:** The ViT paper's own data-scaling experiments (Figure 3, Table 5) compare ImageNet, ImageNet-21k, and JFT-300M pre-training for ViT-B/L/H models [ViT, p.6–7, p.14]; it does not report the exact Small vs. Base IN1k-only vs. IN21k-ft-IN1k comparison from this SQL query, so the specific magnitudes here come only from the timm database, not directly from the paper's own numbers.

**Retrieved:** MAE p.7 (0.85); ViT p.7 (0.84); ViT p.6 (0.83); I-JEPA p.5 (0.79); I-JEPA p.7 (0.79); MAE p.2 (0.79); ViT p.5 (0.79); ViT p.7 (0.79); MAE p.12 (0.78); ViT p.7 (0.78); ViT p.14 (0.78); MAE p.11 (0.78); ViT p.6 (0.78); ViT p.2 (0.78); ViT p.13 (0.78); I-JEPA p.7 (0.78); MAE p.4 (0.78); I-JEPA p.6 (0.78); ViT p.5 (0.78); I-JEPA p.5 (0.77); MAE p.7 (0.77) | gold page hit: 1.00
**SQL:** `SELECT   arch,   weights_tag,   img_size,   top1_val FROM model_results WHERE arch IN ('vit_small_patch16_224', 'vit_base_patch16_224')   AND weights_tag IN ('augreg_in1k', 'augreg_in21k_ft_in1k') ORDER BY arch, weights_tag;` | overlap with reference result: 0.27
*22.8 s*

## Q37 (text+table, cross-source, hard, answerable: yes)

**Question.** The ViT paper reports that ViT needs roughly 2-4x less compute than ResNets for the same transfer performance. In timm at 224 px, how do ViT-B/16 and ResNet-50/101/152 compare on top-1 and measured throughput, and what does that comparison say, or not say, about the paper's claim?

**Reference answer.** The paper's claim is about pre-training compute (Figure 5 is accuracy vs pre-training exaFLOPs, JFT-300M, controlled study), with the caveat that efficiency can depend on schedule, optimiser and weight decay. timm measures inference throughput and has no pre-training compute. At 224 px, taking the best ViT-B/16 row and the a1h_in1k row of each ResNet (one recipe across depths), vit_base_patch16_224.augreg2_in21k_ft_in1k has 85.108 top-1 at 2,992.79 samples/s (17.58 GMACs), versus resnet152.a1h_in1k 82.818 at 1,976.86 (11.56 GMACs), resnet101.a1h_in1k 81.95 at 2,781.19 (7.83 GMACs) and resnet50.a1h_in1k 80.654 at 4,302.84 (4.11 GMACs). So this ViT-B/16 row is more accurate than all three and faster than resnet152 (1.51x) and resnet101 (1.08x) despite more GMACs, but slower than resnet50. The ranking depends on which rows are compared: the best ResNet-50 row is resnet50.fb_swsl_ig1b_ft_in1k (81.146, trained with extra data) and is still below the best ViT-B/16 row, but the ImageNet-1k-only vit_base_patch16_224.augreg_in1k row (79.154) is below all three a1h_in1k ResNets, so the accuracy differences track pre-training data and recipe as much as architecture. These numbers neither confirm nor refute the 2-4x pre-training-compute claim.

**System answer.** ## Data from the timm query

**ViT-B/16** (86.57M params, 17.58 GMACs, 2992.79 img/s @224px, batch 1024):
- Best top‑1 (augreg2_in21k_ft_in1k): 85.108%
- IN1k‑only recipe (augreg_in1k): 79.154%

**ResNet‑50** (25.56M params, 4.11 GMACs, 4302.84 img/s):
- Best top‑1 (fb_swsl_ig1b_ft_in1k, semi‑supervised extra data): 81.146%
- Comparable "a1h" recipe: 80.654%

**ResNet‑101** (44.55M params, 7.83 GMACs, 2781.19 img/s):
- Best top‑1 (a1h_in1k): 81.95%

**ResNet‑152** (60.19M params, 11.56 GMACs, 1976.86 img/s):
- Best top‑1 (a1h_in1k): 82.818%

## Head-to-head comparisons

**Accuracy (best weights for each arch):**
ViT‑B/16 (85.108) > ResNet152 (82.818) > ResNet101 (81.95) > ResNet50 (81.146)
ViT‑B/16's accuracy advantage over ResNet152 = 85.108 − 82.818 = 2.29 pts.

**Throughput ratios (img/sec):**
- vs ResNet50: 4302.84 / 2992.79 = 1.44× — ResNet50 is *faster* than ViT‑B/16.
- vs ResNet101: 2992.79 / 2781.19 = 1.08× — ViT‑B/16 is slightly faster.
- vs ResNet152: 2992.79 / 1976.86 = 1.51× — ViT‑B/16 is faster.

**GMACs (inference FLOPs) ratios:**
- ViT‑B/16 / ResNet50 = 17.58 / 4.11 = 4.28× **more** compute per forward pass
- ViT‑B/16 / ResNet101 = 17.58 / 7.83 = 2.25× **more**
- ViT‑B/16 / ResNet152 = 17.58 / 11.56 = 1.52× **more**

**Same-training-data comparison (ImageNet‑1k only, no extra pretraining):**
ViT‑B/16 (augreg_in1k, 79.154%) vs ResNet50 (a1h_in1k, 80.654%), ResNet101 (81.95%), ResNet152 (82.818%) — here ViT‑B/16 has the **lowest** accuracy of the four while also requiring the **most** GMACs (17.58 vs 4.11–11.56).

## What this does and does not say about the paper's claim

The ViT paper's claim — "ViT uses approximately 2–4× less compute to attain the same performance" [ViT, p.8] — is specifically about **total pre-training compute in exaFLOPs when pre-training on JFT‑300M**, averaged over 5 transfer datasets, in a controlled scaling study holding dataset and training recipe fixed [ViT, p.8, p.7 passage 6]. It also explicitly notes that on *smaller* pre-training datasets ResNets beat ViT, and only on large datasets does ViT pull ahead [ViT, p.7, passage 4].

The timm data **cannot directly confirm or refute this claim**, for several reasons:

1. **Metric mismatch.** The query gives single-forward-pass inference GMACs and inference throughput (img/sec) at 224px, not cumulative *pre-training* compute (exaFLOPs across pre-training epochs/dataset size) as used in the paper's Figure 5/Table 6 [ViT, p.15, passage 17]. In fact, by per-pass GMACs, ViT‑B/16 uses **more**, not less, compute than every ResNet variant (1.5×–4.3× more), which is the opposite direction of the paper's claim — but this is an inference-cost measure, not the training-cost measure the paper is talking about.

2. **Uncontrolled training recipes/datasets.** The "best" timm accuracies mix different pretraining sources (IN21k fine-tuning for ViT, semi-supervised IG-1B/YFCC100M for ResNet50, pure-IN1k "a1h" for ResNet101/152), unlike the paper's controlled JFT‑300M scaling study. When the comparison is restricted to models trained only on ImageNet‑1k (ViT‑B/16 augreg_in1k vs ResNet "a1h_in1k" variants), ViT‑B/16 actually has the **lowest** accuracy (79.154% vs 80.654–82.818%) while using the **most** GMACs — consistent instead with the paper's own caveat that ViT needs large-scale pretraining data to show an advantage [ViT, p.7, passage 4], not with the "2–4× less compute for same performance" headline result.

3. **Throughput ≠ compute-matched performance.** ViT‑B/16's throughput is faster than ResNet101/152 but slower than ResNet50 (passage above), and throughput reflects hardware efficiency of a given architecture at inference, not the "total pre-training compute" axis (x-axis of Figure 5 [ViT, p.7, passage 2]) on which the paper's claim is based.

**Bottom line:** The timm numbers show that, among the "best" available checkpoints (which use varied extra data/recipes), ViT‑B/16 reaches higher ImageNet top‑1 than ResNet50/101/152, and its inference throughput is competitive with (faster than) the larger ResNets despite higher GMACs. But because the timm query measures inference GMACs/throughput under heterogeneous training recipes rather than the paper's controlled JFT‑300M pre-training compute (exaFLOPs) comparison, this evidence neither confirms nor refutes the specific "2–4× less pre-training compute for equal transfer performance" claim in [ViT, p.8]. If anything, the ImageNet‑1k-only subset of the timm data (augreg_in1k vs a1h_in1k) is more consistent with the paper's separate finding that ViT needs large pretraining datasets to outperform ResNets and is not more compute-efficient on smaller/single datasets [ViT, p.7].

**Retrieved:** ViT p.8 (0.78); ViT p.7 (0.77); ViT p.7 (0.76); ViT p.7 (0.76); ViT p.19 (0.75); ViT p.8 (0.75); ViT p.19 (0.74); ViT p.14 (0.74); ViT p.5 (0.74); ViT p.19 (0.73); ViT p.7 (0.73); ViT p.5 (0.73); ResNet p.7 (0.72); ViT p.6 (0.72); MAE p.7 (0.72); ViT p.5 (0.72); ViT p.15 (0.72); MAE p.4 (0.71); ViT p.20 (0.71); ResNet p.7 (0.71); ViT p.5 (0.71); ViT p.4 (0.71); ResNet p.8 (0.71); ResNet p.5 (0.70); ViT p.5 (0.70) | gold page hit: 1.00
**SQL:** `SELECT     mr.arch,     mr.model,     mr.weights_tag,     mr.img_size,     mr.param_count_m,     mr.top1_val,     bi.samples_per_sec,     bi.step_time_ms,     bi.batch_size,     bi.gmacs FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.img_size = 224   AND mr.arch IN ('vit_base_patch16_224', 'resnet50', 'resnet101', 'resnet152') ORDER BY mr.arch, mr.top1_val DESC;` | overlap with reference result: 1.00
*59.3 s*

## Q40 (text+table, cross-source, medium, answerable: yes)

**Question.** The ResNet paper says its 152-layer network has lower complexity than VGG-16/19. Using timm's measurements at 224 px, how do parameters, GMACs, throughput and top-1 of resnet152 compare with vgg16 and vgg19, and does lower FLOPs mean faster in this benchmark?

**Reference answer.** The paper says the 152-layer ResNet (11.3 billion FLOPs) has lower complexity than VGG-16/19 (15.3/19.6 billion FLOPs). timm: resnet152 has 60.19M parameters, 11.56 GMACs, 1,976.86 samples/s and tv_in1k top-1 78.33; vgg16 has 138.36M, 15.47 GMACs, 2,235.61 samples/s, top-1 71.594; vgg19 has 143.67M, 19.63 GMACs, 2,044.71 samples/s, top-1 72.4. So resnet152 has 2.3-2.4x fewer parameters, 1.34-1.70x fewer GMACs and higher top-1 (with torchvision weights), but its measured throughput is about 12% lower than vgg16 and 3% lower than vgg19 on this GPU. Lower FLOPs therefore did not mean higher throughput here; the paper's claim concerns FLOPs, not measured speed.

**System answer.** ## Comparison using timm measurements (224px)

| Model | Params (M) | GMACs | Throughput (samples/sec) | Top‑1 (best variant) |
|---|---|---|---|---|
| resnet152 | 60.19 | 11.56 | 1976.86 | 82.818 (a1h_in1k) |
| vgg16 | 138.36 | 15.47 | 2235.61 | 71.594 |
| vgg19 | 143.67 | 19.63 | 2044.71 | 72.400 |

**Parameters:** resnet152 has far fewer parameters than either VGG model — 60.19M vs. 138.36M (vgg16) and 143.67M (vgg19), i.e. roughly 2.3× and 2.4× fewer, respectively.

**GMACs (complexity):** resnet152's 11.56 GMACs is lower than vgg16's 15.47 and vgg19's 19.63. This is consistent with the ResNet paper's own claim that "the 152-layer ResNet (11.3 billion FLOPs) still has lower complexity than VGG-16/19 nets (15.3/19.6 billion FLOPs)" [ResNet, p.7] — the timm GMACs figures (11.56/15.47/19.63) line up almost exactly with the paper's reported FLOPs (11.3/15.3/19.6).

**Top‑1 accuracy:** resnet152 is substantially more accurate than either VGG model in timm's benchmark (82.818% vs. 71.594% for vgg16 and 72.4% for vgg19), a far larger gap than the original paper's ImageNet comparison, which only reported ResNet vs. VGG-16/19 on the detection/FLOPs side (the main classification table only compares plain vs. residual nets and among ResNet depths) [ResNet, p.6, Table 3].

**Throughput — does lower FLOPs/GMACs mean faster?**
No, not in this benchmark. Despite having the fewest GMACs, resnet152 is actually the *slowest* of the three in samples/sec:
- vgg16: 2235.61 samples/sec (fastest, despite highest-but-one GMACs)
- vgg19: 2044.71 samples/sec
- resnet152: 1976.86 samples/sec (slowest, despite lowest GMACs: 11.56 vs. 15.47/19.63)

So even though resnet152 requires fewer multiply‑accumulate operations than vgg16 or vgg19, it runs at lower throughput than both on this hardware/benchmark setup. The paper's complexity comparison (by FLOPs/GMACs) does not translate into a wall‑clock speed advantage here — likely because resnet152's 152 sequential layers (vs. VGG's fewer, larger conv layers) create more overhead/less parallelism per FLOP, though the passages provided do not explicitly explain this; this conclusion is drawn only from the throughput numbers in the query result, not from any stated mechanism in the papers.

**Retrieved:** ResNet p.7 (0.79); ResNet p.10 (0.75); ResNet p.8 (0.74); ResNet p.6 (0.74); ResNet p.10 (0.74); ResNet p.6 (0.73); ResNet p.7 (0.73); ResNet p.6 (0.73); ResNet p.7 (0.72); ResNet p.5 (0.72); ResNet p.5 (0.70); ViT p.19 (0.70); ResNet p.11 (0.70); ResNet p.7 (0.70); ViT p.8 (0.69); ResNet p.6 (0.69); ResNet p.4 (0.69); ViT p.7 (0.69); BYOL p.19 (0.69); ViT p.5 (0.69); ResNet p.8 (0.69); ResNet p.6 (0.68); ViT p.7 (0.68); ResNet p.5 (0.68) | gold page hit: 0.50
**SQL:** `SELECT   mr.arch,   mr.model,   mr.img_size,   mr.param_count_m,   bi.gmacs,   bi.samples_per_sec,   bi.batch_size,   mr.top1_val FROM model_results mr JOIN benchmark_infer bi   ON mr.arch = bi.arch AND mr.img_size = bi.img_size WHERE mr.arch IN ('resnet152', 'vgg16', 'vgg19')   AND mr.img_size = 224 ORDER BY mr.arch;` | overlap with reference result: 1.00
*25.2 s*

## Q42 (text-only, conceptual, medium, answerable: yes)

**Question.** Does the MMLU paper attribute its models' accuracy mainly to parameter count? Use its GPT-3, UnifiedQA and smaller fine-tuned model comparisons.

**Reference answer.** Not mainly: size matters but is not sufficient. In few-shot GPT-3 (Table 1) the three smaller models are near random (Small 25.9%, Medium 24.9%, Large 26.0% against 25.0% for random) while the 175B X-Large model reaches 43.9% (about 37.7% zero-shot). But UnifiedQA, fine-tuned on other QA datasets and tested without further tuning, reaches 48.9% with 11B parameters, better than GPT-3 X-Large despite an order of magnitude fewer parameters, and its smallest 60M variant gets about 29.3%. In Appendix A.1 RoBERTa-base (125M) gets 27.9%, ALBERT-xxlarge (223M) 27.1% and GPT-2 (1.5B) 32.4%; UnifiedQA-60M beats RoBERTa and ALBERT with fewer parameters and UnifiedQA-3B (43.7%) beats GPT-2, which the authors say suggests T5's larger pretraining dataset helps. They conclude that model size is a key component but fine-tuning also helps; the data-size explanation is a suggestion, and the models differ in architecture, fine-tuning data and evaluation regime (GPT-3 few-shot, UnifiedQA tested under distribution shift), so it is not a controlled test.

**System answer.** **Short answer: No — the paper does not attribute accuracy mainly to parameter count. It explicitly argues that fine-tuning and pretraining-dataset size matter as much as or more than raw parameter count, based on exactly the comparisons you mention.**

**1. Within GPT-3 alone, size does predict accuracy:**
- "the three smaller GPT-3 models have near random accuracy (around 25%)... the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%" [MMLU, p.6]. This piece, taken alone, supports a size→accuracy story for GPT-3.

**2. But the UnifiedQA vs. GPT-3 comparison breaks the "size explains everything" story:**
- UnifiedQA (11B params) reaches 48.9% accuracy, "This performs better than the few-shot GPT-3 X-Large model [175B]... despite UniﬁedQA have an order of magnitude fewer parameters" [MMLU, p.6]. The paper's own conclusion: "These results suggest that while model size is a key component for achieving strong performance, ﬁne-tuning also helps" [MMLU, p.6].

**3. The UnifiedQA vs. smaller fine-tuned models (RoBERTa, ALBERT, GPT-2) comparison reinforces this:**
- UnifiedQA's smallest variant has 60M parameters and ~29.3% accuracy, which "obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters" — RoBERTa-base (125M params, 27.9% accuracy) and ALBERT-xxlarge (223M params, 27.1% accuracy) [MMLU, p.12; p.12]. Despite having roughly 2–4× fewer parameters, UnifiedQA-small beats both larger models.
  - Calculation: 29.3% (60M params) > 27.9% (125M params) and > 27.1% (223M params) — accuracy is inversely related to size here.
- The paper attributes this to pretraining data, not size: "This suggests that its larger pretraining dataset enables higher accuracy" [MMLU, p.12].

**4. Same pattern at larger scale:**
- "UniﬁedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy. This again suggests that T5's larger pretraining dataset size (and therefore UniﬁedQA's pretraining dataset size) can increase accuracy" [MMLU, p.12].
  - Calculation: 43.7% (3B params) vs. 32.4% (1.5B params) — UnifiedQA is ~2× the size of GPT-2 here, but the paper credits *pretraining data*, not parameter count, for the gap.

**Conclusion:** Across these three comparisons, the paper finds that parameter count correlates with accuracy for GPT-3 scaling alone [MMLU, p.6], but when comparing across model families (UnifiedQA vs. GPT-3, UnifiedQA vs. GPT-2/RoBERTa/ALBERT), larger pretraining datasets and fine-tuning repeatedly let smaller models outperform larger ones. The paper's explicit synthesis is that "model size is a key component for achieving strong performance" but **not the sole or main driver** — "ﬁne-tuning also helps" and larger pretraining datasets "can increase accuracy" independent of parameter count [MMLU, p.6; p.12].

**Retrieved:** MMLU p.12 (0.81); MMLU p.6 (0.79); MMLU p.6 (0.79); MMLU p.6 (0.79); MMLU p.2 (0.79); MMLU p.12 (0.79); MMLU p.5 (0.78); MMLU p.5 (0.78); MMLU p.12 (0.77); MMLU p.7 (0.77); MMLU p.1 (0.77); DailyOracle p.18 (0.77); MMLU p.2 (0.77); MMLU p.2 (0.75); MMLU p.11 (0.75); DailyOracle p.7 (0.75); FIRE-Bench p.26 (0.75); MMLU p.13 (0.74); MMLU p.7 (0.74); FIRE-Bench p.27 (0.74); DailyOracle p.15 (0.74) | gold page hit: 1.00
*22.7 s*

## Q43 (text-only, cross-paper, hard, answerable: yes)

**Question.** MMLU, SWE-bench and FIRE-Bench each have to worry that a model may have seen benchmark content during training. What check does each paper run, what does it find, and how strongly does each paper state its conclusion?

**Reference answer.** MMLU (Appendix B.2): memorized questions would have low entropy and high accuracy, but accuracy and question entropy are not positively correlated (correlation between average log probability and accuracy r = -0.43 zero-shot, -0.56 few-shot), which 'suggests that our exact questions were not memorized'. The authors add that models still met text related to the questions through Wikipedia, and promise a list of question sources. SWE-bench (Section 5): resolve rates for PRs created before versus after 2023 in the oracle setting show little difference for most models (Claude 2 4.87% vs 4.23%, ChatGPT-3.5 0.49% vs 0.77%, SWE-Llama 13b 3.98% vs 3.85%), GPT-4 being the exception (1.96% vs 0.0%, on a 25% subset); the authors call this 'largely promising' since models are 'unlikely to cheat' by generating a more recent repository version, and note that new instances can be collected after a model's training date. FIRE-Bench (Section 5.4): F1 on tasks published before versus after each model's knowledge cutoff, stratified by difficulty (Table 6), shows no consistent advantage for pre-cutoff tasks; the authors call the analysis coarse (approximate cutoff dates, unknown training data, small per-category samples) and say it 'suggests the absence of a strong contamination signal rather than proving its absence'. The three checks measure different things (exact-question memorization versus date-based exposure) and none can rule contamination out, so their results are not comparable and no benchmark should be called cleaner on this evidence.

**System answer.** Based on the provided passages, the evidence is uneven across the three benchmarks—only FIRE-Bench's own contamination check is actually documented, SWE-bench offers only a related design feature (not an empirical check), and MMLU is not covered by any passage at all.

**MMLU**
No passages about MMLU are provided in the evidence set. I cannot report what check, if any, the MMLU paper runs for training-data contamination, nor its findings or strength of conclusion.

**SWE-bench**
The passages given do not describe an explicit empirical contamination check (e.g., comparing performance on pre- vs. post-cutoff instances). What they do show is a structural/design feature meant to mitigate future contamination: SWE-bench's collection pipeline is described as "easily extensible to any open source code repositories," giving it "temporal robustness," because "as new language models trained on more recent source code are released over time, SWE-bench can simply be updated to produce new task instances based on PRs created after any LM's training date" [SWE-bench, p.16]. This is a forward-looking design claim about how the benchmark *could* avoid contamination for future models, not a reported test of whether current evaluated models (e.g., Claude 2, SWE-Llama) had seen the specific issues/PRs during training, and no finding or contamination result is stated. So: no explicit check or finding is given in the evidence, and no strength-of-conclusion language appears either.

**FIRE-Bench**
FIRE-Bench explicitly runs a contamination check: "We further examine potential data contamination effects by disentangling performance across task difficulty levels and model knowledge cutoff dates, and find no strong evidence of systematic contamination" [FIRE-Bench, p.2]. 
- **Check**: breaking down agent performance by (a) task difficulty level and (b) whether the backbone LLM's knowledge cutoff postdates the source paper.
- **Finding**: performance patterns across these splits do not show a strong effect, i.e., no sign that agents do better simply because the paper (and its findings) could have been in the model's training data.
- **Strength of conclusion**: hedged/cautious — the paper says only that it finds "no strong evidence of systematic contamination" [FIRE-Bench, p.2], not that contamination is ruled out or proven absent. This is a moderate, qualified claim rather than a strong, definitive one.

**Summary comparison**
- MMLU: not addressed by the evidence provided — cannot answer.
- SWE-bench: evidence shows only a design mitigation (continuous updates using post-cutoff PRs) [SWE-bench, p.16], not an executed check or empirical finding; no stated conclusion strength.
- FIRE-Bench: runs an explicit empirical check (difficulty × knowledge-cutoff disentanglement) and states a moderately-hedged conclusion of "no strong evidence of systematic contamination" [FIRE-Bench, p.2].

**Retrieved:** FIRE-Bench p.9 (0.77); FIRE-Bench p.2 (0.77); FIRE-Bench p.9 (0.77); FIRE-Bench p.2 (0.76); FIRE-Bench p.1 (0.76); FIRE-Bench p.5 (0.76); FIRE-Bench p.10 (0.75); FIRE-Bench p.3 (0.75); FIRE-Bench p.19 (0.74); FIRE-Bench p.4 (0.74); FIRE-Bench p.1 (0.74); SWE-bench p.3 (0.74); SWE-bench p.2 (0.73); SWE-bench p.2 (0.73); FIRE-Bench p.3 (0.73); SWE-bench p.3 (0.73); SWE-bench p.2 (0.73); FIRE-Bench p.5 (0.72); FIRE-Bench p.2 (0.72); FIRE-Bench p.19 (0.72); FIRE-Bench p.15 (0.72); SWE-bench p.4 (0.72); SWE-bench p.27 (0.72); SWE-bench p.4 (0.72); SWE-bench p.16 (0.72) | gold page hit: 0.33
*20.7 s*

## Q44 (text-only, conceptual, medium, answerable: yes)

**Question.** In SWE-bench's baseline experiments, how are files chosen as model context (BM25 versus an 'oracle'), and what does the paper find about whether giving the model more retrieved context helps?

**Reference answer.** The baselines either retrieve files with BM25 at three context limits (13k, 27k and 50k tokens), because dense retrieval is ill-suited to the very long keys and queries, or use an 'oracle' setting that supplies the files edited by the reference patch. BM25 recall of the oracle files rises with the context limit (average 29.58 / 44.41 / 51.06 for 13k / 27k / 50k), but Claude 2's resolve rate falls (1.96 / 1.87 / 1.22), and the authors say performance drops even though recall rises because models are ineffective at localizing problematic code; models do best on the shortest context. With the oracle retriever Claude 2 resolves 4.8% of issues, and in the 'oracle'-collapsed setting (oracle files, with code not directly modified by the PR collapsed except for +/-15 lines) GPT-4 rises from 1.3% to 3.4% and Claude 2 from 4.8% to 5.9%.

**System answer.** ## How context is selected: BM25 vs. "Oracle"

SWE-bench's task inputs consist of an issue description (short, ~195 words on average) plus a codebase that is far too large to fit in context (438K lines on average), so the authors needed a method to select relevant files [SWE-bench, p.4, sec. 4]. They evaluate models under **two context settings** [SWE-bench, p.5, sec. 4.1]:

1. **Sparse (BM25) retrieval**: "We choose to use BM25 retrieval (Robertson et al., 2009) to retrieve relevant files to provide as context for each task instance." Dense retrieval was deemed ill-suited because of the long key/query lengths and the unusual task of retrieving code via natural-language queries [SWE-bench, p.5, sec. 4.1]. They test **three maximum context limits (13k, 27k, 50k tokens)**, retrieving as many files as fit within each limit, and report the best-performing limit per model [SWE-bench, p.5, sec. 4.1].

2. **"Oracle" retrieval**: the model is given exactly "the full contents of files edited by the gold patch" — i.e., the ground-truth files that the actual PR solution modified — along with instructions and a diff-format example [SWE-bench, p.8, sec. 1.1 All Gold; p.5, sec. 4.1 lists this as the second setting].

## Does more retrieved context help?

The paper finds that **more context does not help — it tends to hurt performance**, for several interlocking reasons:

- **BM25 recall is imperfect and only partially overlaps with oracle files.** At the 27,000-token limit, BM25 retrieves a superset of the oracle files in ~40% of instances, but in nearly half of instances it retrieves *none* of the oracle files [SWE-bench, p.5, sec. 4.1]. Recall increases with context length (Table 4): Avg. recall is 29.58% at 13k, 44.41% at 27k, 51.06% at 50k [SWE-bench, p.5, Table 4].

- **But larger context windows reduce resolve rates despite better recall.** Table 2 shows resolve rates dropping as the max context limit grows [SWE-bench, p.5, sec. 4.2, Table 2]:
  - Claude 2: 1.96% (13k) → 1.87% (27k) → 1.22% (50k)
  - SWE-Llama 7b: 0.70% (13k) → 0.31% (27k) → 0.00% (50k)
  - SWE-Llama 13b: 0.70% (13k) → 0.48% (27k) → 0.00% (50k)
  
  The paper states directly: "From observation, models perform best on the shortest context window, as shown in Table 2" [SWE-bench, p.5, sec. 4.1].

- **This is explained by a context-length/localization problem, not just noise from irrelevant files.** "As total context length increases, Claude 2's performance drops considerably; behavior that is also observed in other models... models see a lot of code that may not be directly related to solving the issue at hand, and they seem to frequently struggle with localizing problematic code needing to be updated." The paper links this to broader findings that LMs "become distracted by additional context and may be sensitive to the relative location of target sequences (Liu et al., 2023b)." Critically, "even when increasing the maximum context size for BM25 would increase recall with respect to the oracle files, performance drops... as models are simply ineffective at localizing problematic code" [SWE-bench, p.6, sec. 1.22].

- **Oracle retrieval (the "right" files, no extra noise) improves performance over BM25**, consistent with this: "providing only the files edited by the reference solution's pull request, model performance improves compared to the noisier BM25 retrieval setting" [SWE-bench, p.25, sec. B.1/C.1]. For example, under oracle retrieval, Claude 2 resolves 4.01% (25% subset, Table 1) vs. 1.97%/BM25 on the full benchmark [SWE-bench, p.6, Table 5; p.27, Table 20], and SWE-Llama 13b rises from 0.70% (BM25, full set) to 4.54%/3.97% in oracle settings [SWE-bench, p.6, Table 5; p.27, Table 19/Table 17].

- **Fine-tuned models (SWE-Llama) are especially sensitive to this context mismatch.** Because SWE-Llama was fine-tuned using oracle-style context (and trained to edit every file given as context), it performs poorly when BM25 context includes files not meant to be changed: "this shift in context makes it difficult for the model to perform reliably... SWE-Llama was trained to edit every file included as context whereas in the BM25 setting many files provided in context are not expected to be changed" [SWE-bench, p.7, sec. 1.22].

**Summary**: Context is chosen either via BM25 sparse retrieval at varying token budgets or via an "oracle" setting that supplies exactly the gold-patch files. The paper's clear finding is that *more* retrieved context does **not** help and generally hurts — resolve rates fall as the BM25 context limit grows from 13k→27k→50k tokens even though recall of the true relevant files improves, because models struggle to localize the correct code amid additional, often irrelevant, content [SWE-bench, p.5–6].

**Retrieved:** SWE-bench p.27 (0.81); SWE-bench p.27 (0.81); SWE-bench p.26 (0.80); SWE-bench p.6 (0.80); SWE-bench p.5 (0.80); SWE-bench p.5 (0.79); SWE-bench p.4 (0.79); SWE-bench p.7 (0.78); SWE-bench p.5 (0.77); SWE-bench p.2 (0.77); SWE-bench p.25 (0.76); SWE-bench p.6 (0.76); SWE-bench p.24 (0.76); SWE-bench p.26 (0.76); SWE-bench p.24 (0.75); SWE-bench p.5 (0.74); SWE-bench p.8 (0.74); SWE-bench p.6 (0.74); SWE-bench p.9 (0.74); SWE-bench p.5 (0.74); SWE-bench p.45 (0.74); SWE-bench p.7 (0.74); SWE-bench p.29 (0.74); SWE-bench p.51 (0.73); SWE-bench p.43 (0.73); SWE-bench p.11 (0.73) | gold page hit: 1.00
*23.1 s*

## Q45 (text-only, cross-paper, medium, answerable: yes)

**Question.** BYOL reports that its accuracy stays stable over a wide range of batch sizes. What does BYOL say causes the drop at smaller batch sizes, and where does the Batch Normalization paper say the statistics used for normalization come from during training?

**Reference answer.** BYOL (Figure 3a, batch sizes 128 to 4096): BYOL's performance remains stable from 256 to 4096 and only drops for smaller values 'due to batch normalization layers in the encoder'; a footnote says the only dependency on batch size in its training pipeline sits within the batch normalization layers. SimCLR, by contrast, deteriorates rapidly as the batch size falls, likely because there are fewer negative examples. BatchNorm paper: because training uses mini-batches, each mini-batch produces estimates of the mean and variance of each activation, and these statistics are used for the normalization and can fully participate in the gradient backpropagation. So during training a batch-normalized layer normalizes each example with statistics estimated from its mini-batch, which is where BYOL locates its batch-size dependence. Neither paper analyses why small batches hurt: BYOL does not explain the drop beyond naming the BN layers, and the BatchNorm paper does not discuss small-batch performance or BYOL, so the link is an inference from the two papers rather than a claim either makes.

**System answer.** **BYOL's cause of the drop at smaller batch sizes:**
BYOL states that its performance "remains stable over a wide range of batch sizes from 256 to 4096, and only drops for smaller values due to batch normalization layers in the encoder" [BYOL, p.8]. This is reiterated in a footnote: "The only dependency on batch size in our training pipeline sits within the batch normalization layers" [BYOL, p.8]. Additionally, the appendix attributes the drop at batch size 64 specifically to "the ill behaviour of batch normalization at low batch sizes" [BYOL, p.25].

**Batch Normalization paper's source of statistics during training:**
During training, Batch Normalization computes statistics from the mini-batch itself: normalization uses "training mini-batches of size m" with their sample means and "σ²_B are their sample variances" [BatchNorm, p.4]. The passage contrasts this with inference, noting that "moving averages" of these mini-batch statistics are tracked and used instead at inference time, when "the means and variances are fixed" [BatchNorm, p.4]. So during training, the normalization statistics come from the current mini-batch (sample mean/variance), not a fixed or moving-average value.

**Retrieved:** BYOL p.25 (0.86); BYOL p.30 (0.83); BYOL p.8 (0.83); BYOL p.28 (0.82); BYOL p.8 (0.79); BatchNorm p.8 (0.78); BatchNorm p.5 (0.78); BatchNorm p.5 (0.77); BYOL p.26 (0.77); BYOL p.6 (0.77); BYOL p.8 (0.76); BYOL p.7 (0.76); BYOL p.8 (0.76); BatchNorm p.6 (0.76); BYOL p.2 (0.76); BYOL p.26 (0.76); BYOL p.20 (0.75); BatchNorm p.5 (0.75); BatchNorm p.4 (0.75); BYOL p.8 (0.75); BatchNorm p.1 (0.75); BatchNorm p.6 (0.74) | gold page hit: 0.67
*8.0 s*

## Q39 (text+table, cross-source, medium, answerable: yes)

**Question.** The BYOL paper reports 74.3% for a linear classifier on frozen ResNet-50 features and cites supervised ResNet-50 baselines of 76.5% and 78.9%. How many timm ResNet-50 rows at 224 px have a top-1 accuracy at or above each of these three numbers, and what limits how that comparison can be read?

**Reference answer.** The paper's numbers are 74.3% (BYOL, linear evaluation on frozen features), 76.5% and 78.9% (supervised baselines). Among timm's 18 resnet50 rows at 224 px, all 18 are at or above 74.3%, 17 are at or above 76.5% (the exception is resnet50.tv_in1k at 76.156), and 13 are at or above 78.9% (the five below are ra_in1k 78.82, bt_in1k 78.444, a3_in1k 78.052, gluon_in1k 77.58 and tv_in1k 76.156). These are not like-for-like: BYOL's 74.3% is a linear probe on self-supervised features, whereas timm's are fully supervised weights with different recipes, some using extra data (e.g. ig1b, yfcc100m), so the comparison says nothing about whether self-supervised learning is better or worse.

**System answer.** ## Results from the timm database query

Out of **18 total** ResNet-50 rows at 224px resolution in the timm database:

| Threshold | Count meeting/exceeding it | Source of threshold |
|---|---|---|
| ≥ 74.3% | 18 / 18 | BYOL's own linear-evaluation result on frozen ResNet-50 features [BYOL, p.2 / p.6] |
| ≥ 76.5% | 17 / 18 | Supervised ResNet-50 baseline from [8], as cited in BYOL [BYOL, p.6, p.20] |
| ≥ 78.9% | 13 / 18 | Supervised baseline reproduced by BYOL authors using RandAugment, for the ResNet-50 (4×) comparison [BYOL, p.6, p.20] |

## What limits how this comparison can be read

1. **Different training paradigms.** BYOL's 74.3% comes from training only a *linear classifier* on top of a *frozen* self-supervised representation [BYOL, p.6]. The timm rows, by contrast, almost certainly reflect fully *supervised* end-to-end training (standard timm benchmarking practice), which is a fundamentally different task than linear evaluation on frozen features. So "18/18 timm rows beat 74.3%" does not mean timm models beat BYOL at the same task — it's an apples-to-oranges comparison. The passages given do not state the training protocol used for the timm rows, so this cannot be confirmed from the evidence directly, only inferred from the nature of the number itself.

2. **The 76.5% and 78.9% baselines are architecture-multiplier-specific.** Per BYOL's own table [BYOL, p.20, Table 9], 76.5% is the supervised baseline for the **standard ResNet-50 (1×, 24M weights)**, while 78.9% is the supervised baseline for a **much larger ResNet-50 (4×, 375M weights)** — not the same architecture at all, despite sharing the "ResNet-50" name. The SQL query filtered only on `arch = 'resnet50'`, with no indication that it distinguishes width multipliers; if the timm database's "resnet50" entries are standard 1× models, comparing them to the 78.9% (4×) baseline conflates two different model sizes.

3. **Training recipe differences.** BYOL explicitly notes that even their own supervised reproduction depends heavily on augmentation choices (e.g., RandAugment) [BYOL, p.6, p.19–20], and that the original [8] baseline might be further improvable with better augmentations. timm models use a wide variety of training recipes (different augmentation, regularization, epoch counts, resolution handling) that are not characterized in the provided passages, so matching a timm row's accuracy to a BYOL-cited number does not establish they were trained comparably.

4. **"img_size = 224" filter vs. BYOL's evaluation resolution.** BYOL's evaluation protocol resizes to 256px then center-crops to 224×224 [BYOL, p.17], so this dimension appears consistent, but this is the only protocol detail the passages confirm matches.

**Bottom line:** The query shows raw counts (18, 17, 13 out of 18) of timm ResNet-50@224 entries at or above BYOL's three cited numbers, but the passages establish that these three numbers come from different evaluation protocols (frozen linear probe vs. full supervised training) and different model sizes (1× vs. 4× width), so the counts cannot be read as a fair "timm models beat BYOL/supervised baselines" comparison without further information about the timm rows' training protocol — information not present in the passages or query result.

**Retrieved:** BYOL p.19 (0.83); BYOL p.21 (0.81); BYOL p.6 (0.81); BYOL p.6 (0.80); BYOL p.2 (0.80); BYOL p.19 (0.79); BYOL p.25 (0.79); BYOL p.20 (0.79); BYOL p.18 (0.78); ResNet p.7 (0.77); ResNet p.5 (0.77); ResNet p.7 (0.77); BYOL p.19 (0.76); BYOL p.18 (0.76); BYOL p.25 (0.76); BYOL p.20 (0.75); BYOL p.17 (0.75); BYOL p.7 (0.75); BYOL p.1 (0.75); ResNet p.6 (0.74); ResNet p.7 (0.74) | gold page hit: 1.00
**SQL:** `SELECT   SUM(CASE WHEN top1_val >= 74.3 THEN 1 ELSE 0 END) AS n_ge_74_3,   SUM(CASE WHEN top1_val >= 76.5 THEN 1 ELSE 0 END) AS n_ge_76_5,   SUM(CASE WHEN top1_val >= 78.9 THEN 1 ELSE 0 END) AS n_ge_78_9,   COUNT(*) AS n_total_resnet50_224 FROM model_results WHERE arch = 'resnet50' AND img_size = 224;` | overlap with reference result: 1.00
*26.5 s*
