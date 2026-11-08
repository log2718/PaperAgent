# Tabular Data Candidates

Searched on 2026-11-01. All sizes, counts and example values below were measured by downloading or querying the sources that day, not taken from descriptions. The corpus is the 10 papers in `text_evaluation_candidates.xlsx` (Transformer, ResNet, ViT, BYOL, MAE, I-JEPA, Temporal Straightening, Embedding Limits, Daily Oracle, FIRE-Bench).

**Recommendation: Candidate 1 (timm result CSVs).** It is the only candidate that has official provenance, flat CSVs, many numeric columns, and numbers that are independent of what the papers print. It overlaps the corpus on ResNet, ViT and (partly) MAE only. Candidate 2 overlaps more papers but fails on provenance, redundancy with the papers, and ease of querying (details below).

## Summary comparison

| Criterion | 1. timm results | 2. Papers With Code archive | 3. MTEB results | 4. torchvision weights meta |
|---|---|---|---|---|
| Corpus papers overlapped | ResNet, ViT, MAE (partial) | ResNet, ViT, MAE, BYOL, Transformer (I-JEPA: 0 rows) | Embedding Limits only | ResNet, ViT |
| Provenance / quality | High (maintainer-run, reproducible script, versioned) | Medium-low (community-entered, archived snapshot) | High (official, CC0) | High (official) |
| Ease of SQL | Very easy (flat CSV, shared keys) | Hard (nested parquet, string-typed numbers) | Hard (thousands of nested JSON files) | Easy but tiny |
| Non-trivial numeric questions | Many (6 eval sets, params, GMACs, throughput) | Some (top-1, params, GFLOPs, 63% / 51% filled) | Some (scores by task, dims) | Few (4 numeric fields, 18 rows for corpus archs) |
| Cross-source questions that truly need both | Yes (numbers are independent of papers) | Weak (rows mostly repeat numbers printed in the papers) | Partial (no LIMIT scores in repo) | Weak (small, mostly overlaps timm) |
| Manual data construction | None | None, but heavy flattening/cleaning | Heavy download/flattening | None |

---

## Candidate 1 — timm (PyTorch Image Models) results and benchmark CSVs  *(recommended)*

- **Source:** Hugging Face `pytorch-image-models`, `results/` folder — https://github.com/huggingface/pytorch-image-models/tree/main/results (README: https://github.com/huggingface/pytorch-image-models/blob/main/results/README.md). Repo license Apache-2.0. `results-imagenet.csv` last changed 2025-10-30 (commit `4e5207c`); repo HEAD at retrieval `03b76b6` (2026-10-30).
- **Format:** CSV, plus the script `generate_csv_results.py` that computes the diff columns.
- **Size:** 1,556 rows (model, image-size) per evaluation file; 1,266 distinct model names, 900 distinct architectures. About 1.3 MB for all files used.
- **Files and key columns:**
  - `results-imagenet.csv`: `model` (architecture + `.weights_tag`), `img_size`, `top1`, `top5`, `param_count` (millions), `crop_pct`, `interpolation`.
  - `results-imagenet-real.csv`, `results-imagenetv2-matched-frequency.csv`, `results-sketch.csv`, `results-imagenet-a.csv`, `results-imagenet-r.csv`: same columns plus `top1_diff`, `top5_diff`, `rank_diff` against clean validation. The -a and -r sets use 200-class subsets (clean 200-class runs in `results-imagenet-a-clean.csv` / `-r-clean.csv`).
  - `benchmark-infer-amp-nchw-pt291-cu128-4090.csv`: `model`, `infer_img_size`, `infer_samples_per_sec`, `infer_step_time`, `infer_batch_size`, `param_count`, `infer_gmacs`, `infer_macts` (1,627 rows, RTX 4090, PyTorch 2.9.1, CUDA 12.8, AMP; hardware read from the file name). Training-throughput benchmarks also exist (not used).
  - `model_metadata-in1k.csv`: `model`, coarse `pretrain` label (521 architectures).
- **Overlap with the corpus (measured):**
  - *ResNet:* 77 result rows for the paper's five depths (resnet18/34/50/101/152) across 19 weight tags; the Hugging Face model cards of 154 timm models cite arXiv 1512.03385. timm's `param_count` and `infer_gmacs` can be compared with the paper's FLOPs.
  - *ViT:* 4 rows with `orig_in21k_ft_in1k` weights (the original ViT checkpoints, including the ResNet-50 hybrid `vit_base_r50_s16_384`); 14 plain `vit_*_patch*` architectures; patch-size variants B/8, B/16, B/32 with throughput; 205 timm model cards cite arXiv 2010.11929.
  - *MAE:* 6 rows `hiera_*.mae_in1k_ft_in1k` (MAE-pretrained then fine-tuned; Hiera is not a corpus paper) and 30 `convnextv2 ... fcmae` rows (fully convolutional masked autoencoder, also not a corpus paper). The 3 plain-ViT MAE checkpoints (`vit_*.mae`) are pretrain-only and have no result rows. 15 timm model cards cite arXiv 2111.06377.
  - *Transformer (via ViT/DeiT families), BYOL, I-JEPA, Temporal Straightening, Embedding Limits, Daily Oracle, FIRE-Bench:* no direct rows (searches for byol, simclr, jepa in the timm org returned nothing).
- **Example SQL questions:** (a) among ResNet-50 weight variants, which has the highest ImageNet-R top-1 and what is its drop from clean validation? (b) rank ViT patch sizes by inference throughput at 224 px; (c) which models with under 30M parameters exceed 80% top-1 and 70% ImageNet-Sketch top-1? (d) average top-1 by weight tag for ResNet-101.
- **Example text+table questions:** the ViT paper says smaller patches mean longer sequences and higher cost: does measured throughput for B/32, B/16, B/8 follow that? The ResNet paper reports 3.6 billion FLOPs for the 34-layer net: what is `infer_gmacs` for resnet34 at 224 px, and what does the paper count as FLOPs? Which MAE-pretrained model has the highest top-1, and what does the MAE paper say about the pre-training task?
- **Advantages:** official and reproducible; flat CSV with shared keys; every row has params, no nulls in key columns; robustness sets give numeric dimensions the papers lack; throughput and GMACs give compute trade-offs; numbers are independent re-evaluations, so a question needs the table even when the paper also reports a number.
- **Limitations:** overlaps 2–3 of 10 papers; weights vary in training recipe, extra data (JFT, LAION, WebLI) and image size, so most cross-model comparisons are uncontrolled; ImageNet validation was used for model selection; `pretrain` metadata is per architecture and coarse; benchmark numbers depend on one GPU / software stack; `results-imagenet-a.csv` has one (model, img_size) key that does not match the other files.
- **Preprocessing:** minimal. Split `model` into `arch` and `weights_tag`; join the six result files on (model, img_size) and the benchmark on (arch, img_size) (all 1,556 result rows match a benchmark row); store in SQLite. No manual values.

## Candidate 2 — Papers With Code evaluation tables (archived snapshot)

- **Source:** https://huggingface.co/datasets/pwc-archive/evaluation-tables (dataset card: snapshot retrieved 2025-07-28, "will not be updated"; license CC-BY-SA-4.0).
- **Format:** 4 parquet shards, about 138 MB; 2,254 task records with nested lists/dicts (task → datasets → leaderboard rows).
- **Important fields:** `model_name`, `paper_title`, `paper_date`, `uses_additional_data`, `metrics` (dict of strings such as `"87.8%"`, `"656M"`), model/code links.
- **Overlap (measured by exact paper-title match across all nested leaderboards; counts include duplicates across nested task/dataset views):** ResNet 75 rows, MAE 50, ViT 48, BYOL 19 (including ImageNet linear-eval and 1%-label leaderboards), Transformer 19 (WMT14 EN-DE/EN-FR); I-JEPA 0; Temporal Straightening, Embedding Limits, Daily Oracle, FIRE-Bench 0. The main ImageNet leaderboard has 1,060 rows but only 63% have parameter counts and 51% GFLOPs.
- **Example SQL questions:** number of leaderboard entries per paper-year; best top-1 among entries that use no extra data and have under 100M parameters.
- **Example text+table questions:** BYOL's ImageNet 1%-label rank among semi-supervised entries versus the paper's explanation of its method.
- **Advantages:** widest overlap with the corpus; includes self-supervised leaderboards (BYOL, MAE); permissive for research reuse (with attribution).
- **Limitations:** values were community-entered and are not reproducible by script; mixed protocols (extra data, resolution, backbone) inside one table; metrics are strings in mixed formats; archived, so no maintenance; for corpus papers the rows mostly repeat numbers already printed in the papers, so a text+table question is often answerable from the paper alone, which breaks the "needs both sources" rule; I-JEPA absent.
- **Preprocessing:** substantial (flatten nested structure, deduplicate nested views, parse `%`/`M`/`B` strings, resolve inconsistent column sets).

## Candidate 3 — MTEB results repository (embedding-model scores)

- **Source:** https://github.com/embeddings-benchmark/results (license CC0-1.0; repo about 630 MB; updated daily).
- **Format:** one JSON file per model × task under `results/<model>/<revision>/`, plus `model_meta.json` (`n_parameters`, `embed_dim`, `max_tokens`, `release_date`, `license`).
- **Overlap:** Embedding Limits only. Five of the six models that paper evaluated have result folders (E5-Mistral, GritLM-7B, Qwen3-Embedding-8B, Arctic-Embed-L-v2.0, Gemini-Embedding-001; Promptriever not found). **No LIMIT task result files exist** for these models, so the paper's central quantity (recall on LIMIT by embedding dimension) is not in this data.
- **Example SQL questions:** BEIR-style retrieval score versus `embed_dim` across models.
- **Example text+table questions:** a model's embedding dimension and retrieval score versus the paper's dimension-limit argument.
- **Advantages:** official, CC0, directly relevant to retrieval; embedding dimension is a real column.
- **Limitations:** one corpus paper; no LIMIT scores; thousands of nested JSON files; scores come from varying task sets and MTEB versions.
- **Preprocessing:** heavy (select tasks, parse per-model JSON, align versions) and not minimal.

## Candidate 4 — torchvision model-zoo metadata

- **Source:** https://docs.pytorch.org/vision/stable/models.html and the `torchvision` package (v0.25.0; BSD-3). Read locally from `weights.meta`; no weight files downloaded.
- **Format:** Python metadata (also an HTML table in the docs); 115 weight entries in the zoo.
- **Key fields:** `acc@1`, `acc@5`, `num_params`, `GFLOPS`, file size, training recipe URL.
- **Overlap:** ResNet (resnet18/34/50/101/152: 8 weight entries, V1 and V2 recipes) and ViT (vit_b_16/32, vit_l_16/32, vit_h_14: 10 entries including SWAG weights).
- **Example SQL question:** ratio of GFLOPS to top-1 across ResNet depths.
- **Example text+table question:** resnet34 GFLOPS (3.664) versus the paper's 3.6 billion FLOPs.
- **Advantages:** official and clean; values are consistent with timm (e.g., resnet50 V1 76.13 vs timm `resnet50.tv_in1k` 76.156).
- **Limitations:** tiny; only 18 rows relevant to the corpus; no robustness data; largely a subset of what timm already provides.
- **Preprocessing:** minimal, but needs a script to export the metadata.

---

## Decision

Candidate 1 wins on four of the six requested criteria (quality/provenance, ease of SQL, non-trivial questions, cross-source questions that cannot be answered from the paper alone) and ties with Candidate 2 on the sixth (minimal manual construction; neither needs hand-typed values, though Candidate 2 needs far more cleaning). It loses on overlap, where Candidate 2 reaches more papers, but that overlap is largely the papers' own printed numbers and comes with weaker provenance.

Consequences to plan for: the table can only support cross-source questions about ResNet, ViT and MAE-style pre-training. BYOL, I-JEPA, Temporal Straightening, Embedding Limits, Daily Oracle and FIRE-Bench stay text-only unless a second table is added later. Candidate 4 is a useful cross-check but not worth a separate table. Candidate 2 could supplement the self-supervised papers later, with its provenance caveats.
