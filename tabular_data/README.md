# timm results dataset — provenance and rebuild

## Source

- **Dataset:** PyTorch Image Models (timm) validation and benchmark results, `results/` folder.
- **URL:** https://github.com/huggingface/pytorch-image-models/tree/main/results (README: `raw/README.md`).
- **Pinned version:** repository commit `03b76b6ed7d98a844afc5529669b761b3ac5f562` (committed 2026-10-30 20:09 UTC; `results-imagenet.csv` last changed in commit `4e5207c7bb6592474ca56e28b2cf85be8f1a550f`, 2025-10-30). Files were downloaded from `https://raw.githubusercontent.com/huggingface/pytorch-image-models/03b76b6ed7d98a844afc5529669b761b3ac5f562/results/<file>`.
- **Retrieved:** 2026-11-01.
- **License:** Apache-2.0 (repository license as reported by GitHub).

## Files

- `raw/` — unmodified copies of the source files, with SHA-256 checksums in `raw_checksums_sha256.txt`:
  `results-imagenet.csv`, `results-imagenet-real.csv`, `results-imagenetv2-matched-frequency.csv`, `results-sketch.csv`, `results-imagenet-a.csv`, `results-imagenet-r.csv`, `results-imagenet-a-clean.csv`, `results-imagenet-r-clean.csv`, `benchmark-infer-amp-nchw-pt291-cu128-4090.csv`, `model_metadata-in1k.csv`, plus the source's `README.md` and `generate_csv_results.py`.
- `build_timm_db.py` — rebuilds `timm_results.sqlite` from `raw/` (`python3 -I build_timm_db.py`).
- `timm_results.sqlite` — cleaned tables `model_results` (1,556 rows), `benchmark_infer` (1,627 rows), `model_metadata` (521 rows).
- `data_dictionary.md` — field definitions and comparability notes.

## Cleaning applied (nothing else was changed or imputed)

1. `model` split at the first '.' into `arch` and `weights_tag`.
2. `param_count` strings with thousands separators (5 rows, e.g. `1,014.45`) converted to numbers.
3. Columns renamed (e.g. `infer_samples_per_sec` to `samples_per_sec`) and the five test-set files joined to the validation file on (`model`, `img_size`).
4. Diff columns kept exactly as provided by timm; consistency check: each reproduces (test top-1 minus clean top-1) to within 0.001.

## Known quirks

- `results-imagenet-a.csv` lacks `resnet50.tv_in1k` and contains one extra row (`resmlp_24_224.fb_dino`, 224 px) that has no validation row. The extra row stays in `raw/` but is not in `model_results`; `top1_a` is NULL for `resnet50.tv_in1k`.
- The benchmark file name encodes hardware and software (`pt291-cu128-4090`: PyTorch 2.9.1, CUDA 12.8, RTX 4090); this is the only place that information appears. Other benchmark files in the source (other GPUs, training throughput, CPU) were not copied.
- Weight-tag meanings are interpreted from timm's Hugging Face model cards (e.g. https://huggingface.co/timm/resnet50.tv_in1k, https://huggingface.co/timm/vit_base_patch16_224.orig_in21k_ft_in1k, https://huggingface.co/timm/hiera_base_224.mae_in1k_ft_in1k). Those cards are metadata only; no values were taken from them.
