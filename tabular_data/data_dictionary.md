# Data dictionary — timm results (SQLite `timm_results.sqlite`)

Tables are built by `build_timm_db.py` from the unmodified CSVs in `raw/`. Key columns: `model_results` is unique on (`model`, `img_size`); `benchmark_infer` is unique on (`arch`, `img_size`); join them with `model_results.arch = benchmark_infer.arch AND model_results.img_size = benchmark_infer.img_size`. Accuracy values are percentages (0-100).


## `model_results`

| field | type | source column | description |
|---|---|---|---|
| `model` | text | model (all results-*.csv) | timm model identifier `<arch>.<weights_tag>`: one architecture plus one released pretrained-weights variant. Same string in all result files. |
| `arch` | text | derived | Architecture name: the part of `model` before the first '.'. Join key to benchmark_infer.arch. |
| `weights_tag` | text | derived | The part of `model` after the first '.': timm's label for the weights variant (training recipe and data). Meanings used in the questions are in the tag table below. |
| `img_size` | integer | img_size | Evaluation image size in pixels (square). The same model name can appear at several sizes; (model, img_size) is the row key. |
| `param_count_m` | real | param_count | Parameters in millions (includes the 1000-class head). Thousands separators in the source (e.g. '1,014.45') were removed. |
| `crop_pct` | real | crop_pct | Center-crop ratio used in evaluation. |
| `interpolation` | text | interpolation | Resize interpolation used in evaluation. |
| `top1_val` | real | top1 (results-imagenet.csv) | Top-1 accuracy (%) on the 50,000-image ImageNet-1k validation set (1000 classes). |
| `top5_val` | real | top5 (results-imagenet.csv) | Top-5 accuracy (%) on ImageNet-1k validation. |
| `top1_real` | real | top1 (results-imagenet-real.csv) | Top-1 (%) on ImageNet validation images with the re-assessed 'Real' labels. |
| `top1_diff_real` | real | top1_diff | top1_real minus top1_val (as computed by timm; reproduced here to within 0.001). |
| `top1_v2` | real | top1 (results-imagenetv2-matched-frequency.csv) | Top-1 (%) on ImageNetV2 matched-frequency (10,000 new images). |
| `top1_diff_v2` | real | top1_diff | top1_v2 minus top1_val. |
| `top1_sketch` | real | top1 (results-sketch.csv) | Top-1 (%) on ImageNet-Sketch (50,000 sketch-like images, 1000 classes). |
| `top1_diff_sketch` | real | top1_diff | top1_sketch minus top1_val. |
| `top1_a` | real | top1 (results-imagenet-a.csv) | Top-1 (%) on ImageNet-A (7,500 natural adversarial images, 200-class subset). NULL for resnet50.tv_in1k (absent from the source file). |
| `top1_diff_a` | real | top1_diff | top1_a minus clean top-1 on the same 200 classes (results-imagenet-a-clean.csv). NOT comparable to top1_val. |
| `top1_r` | real | top1 (results-imagenet-r.csv) | Top-1 (%) on ImageNet-R (30,000 renditions, 200-class subset). |
| `top1_diff_r` | real | top1_diff | top1_r minus clean top-1 on the same 200 classes (results-imagenet-r-clean.csv). NOT comparable to top1_val. |

## `benchmark_infer`

| field | type | source column | description |
|---|---|---|---|
| `arch` | text | model | Architecture name (no weights tag): throughput is measured per architecture and image size, so all weights of an architecture share it. |
| `img_size` | integer | infer_img_size | Image size (pixels) used for the inference benchmark. |
| `samples_per_sec` | real | infer_samples_per_sec | Inference throughput in images per second at `batch_size` (RTX 4090, AMP, NCHW, PyTorch 2.9.1, CUDA 12.8; hardware read from the file name). |
| `step_time_ms` | real | infer_step_time | Time per batch step (milliseconds, consistent with batch_size / samples_per_sec). |
| `batch_size` | integer | infer_batch_size | Batch size used for that row; it varies by row (e.g. 512, 768, 1024), which affects throughput comparability. |
| `param_count_m` | real | param_count | Parameters in millions. |
| `gmacs` | real | infer_gmacs | Giga multiply-accumulates per forward pass at img_size, as counted by timm's benchmark script. |
| `macts` | real | infer_macts | Millions of activations per forward pass (not used in the questions). |

## `model_metadata`

| field | type | source column | description |
|---|---|---|---|
| `arch, pretrain_label` | text | model_metadata-in1k.csv | Coarse per-architecture pre-training label (521 architectures). Loaded but not used in any question because it is per architecture, not per weights variant. |

## `weights_tag` values used in the questions

Meanings are taken from the timm model cards on Hugging Face (`https://huggingface.co/timm/<model>`), not from the CSVs. Tags not listed are not interpreted beyond their names.

| tag | meaning |
|---|---|
| `tv_in1k` | Trained on ImageNet-1k; original torchvision model weights (resnet50.tv_in1k, vgg16.tv_in1k cards). |
| `a1_in1k, a1h_in1k, a2_in1k, a3_in1k` | Trained on ImageNet-1k in timm with 'ResNet Strikes Back' A1/A2/A3 recipes (a1h: stronger dropout, stochastic depth and RandAugment). resnet50.a1_in1k card: train 224, test 288. |
| `gluon_in1k` | Trained on ImageNet-1k in Apache Gluon with Bag-of-Tricks recipes. |
| `orig_in21k_ft_in1k` | ViT weights trained on ImageNet-21k and fine-tuned on ImageNet-1k in JAX by the paper authors (original Google release), ported to PyTorch. |
| `augreg_in1k / augreg_in21k_ft_in1k` | ViT weights with additional augmentation and regularization (AugReg): trained on ImageNet-1k only, or pre-trained on ImageNet-21k then fine-tuned on ImageNet-1k. |
| `augreg2_in21k_ft_in1k` | ImageNet-21k pre-training by the paper authors, re-fine-tuned on ImageNet-1k with additional augmentation and regularization by the timm maintainer. |
| `mae_in1k_ft_in1k` | Hiera models pre-trained on ImageNet-1k with the self-supervised Masked Autoencoder (MAE) method, then fine-tuned on ImageNet-1k (hiera_base_224.mae_in1k_ft_in1k card). |
| `fb_swsl_ig1b_ft_in1k, fb_ssl_yfcc100m_ft_in1k, dist_in22k_ft_in1k, clip_ft_in1k, webli_ft_in1k, ...` | Other tags encode extra pre-training data or distillation (names as published by timm); not interpreted beyond the name. |

## Comparability notes

- `top1_diff_real`, `top1_diff_v2`, `top1_diff_sketch` are relative to `top1_val` (1000 classes). `top1_diff_a` and `top1_diff_r` are relative to clean top-1 on the same 200-class subsets, so `top1_a`/`top1_r` must not be subtracted from `top1_val`.
- Throughput and GMACs come from one benchmark run (single GPU and software stack) and are per architecture and image size; `batch_size` varies by row.
- Rows are released weights, not controlled experiments: pre-training data, recipe, image size and extra data differ between rows.
- ImageNet validation was used for model selection during timm training, so `top1_val` is not a clean held-out test.
