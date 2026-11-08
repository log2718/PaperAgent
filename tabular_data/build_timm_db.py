#!/usr/bin/env python3
"""Build timm_results.sqlite from the unmodified raw CSVs in ./raw.

Cleaning is limited to: splitting `model` into arch + weights_tag, removing thousands
separators from param_count, renaming columns, and joining the per-dataset files on (model, img_size). No values are
edited or imputed. Run:  python3 -I build_timm_db.py
"""
import os
import sqlite3
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "timm_results.sqlite")


def rd(name, **kw):
    return pd.read_csv(os.path.join(RAW, name), **kw)


KEY = ["model", "img_size"]

val = rd("results-imagenet.csv")
base = val[KEY + ["top1", "top5", "param_count", "crop_pct", "interpolation"]].rename(
    columns={"top1": "top1_val", "top5": "top5_val", "param_count": "param_count_m"}
)

# (file, column suffix, diff column suffix); diff columns are kept as provided by timm.
# real / v2 / sketch diffs are against the 1000-class validation top-1;
# A / R diffs are against clean top-1 on the same 200 classes (not top1_val).
others = [
    ("results-imagenet-real.csv", "real"),
    ("results-imagenetv2-matched-frequency.csv", "v2"),
    ("results-sketch.csv", "sketch"),
    ("results-imagenet-a.csv", "a"),
    ("results-imagenet-r.csv", "r"),
]
wide = base
for fname, tag in others:
    d = rd(fname)[KEY + ["top1", "top1_diff"]].rename(
        columns={"top1": f"top1_{tag}", "top1_diff": f"top1_diff_{tag}"}
    )
    # left join from the validation file: rows present only in another file are dropped
    wide = wide.merge(d, on=KEY, how="left", validate="one_to_one")

# param_count in the source uses thousands separators for values >= 1,000 (e.g. "1,014.45"); strip them.
wide["param_count_m"] = pd.to_numeric(wide["param_count_m"].astype(str).str.replace(",", "", regex=False))
wide.insert(1, "arch", wide["model"].str.split(".", n=1).str[0])
wide.insert(2, "weights_tag", wide["model"].str.split(".", n=1).str[1])
for c in [c for c in wide.columns if c.startswith("top1_diff_")]:
    wide[c] = pd.to_numeric(wide[c], errors="coerce")

bench = rd("benchmark-infer-amp-nchw-pt291-cu128-4090.csv").rename(
    columns={
        "model": "arch",
        "infer_img_size": "img_size",
        "infer_samples_per_sec": "samples_per_sec",
        "infer_step_time": "step_time_ms",
        "infer_batch_size": "batch_size",
        "param_count": "param_count_m",
        "infer_gmacs": "gmacs",
        "infer_macts": "macts",
    }
)
bench["img_size"] = bench["img_size"].astype(int)

meta = rd("model_metadata-in1k.csv").rename(columns={"model": "arch", "pretrain": "pretrain_label"})

if os.path.exists(OUT):
    os.remove(OUT)
con = sqlite3.connect(OUT)
wide.to_sql("model_results", con, index=False)
bench.to_sql("benchmark_infer", con, index=False)
meta.to_sql("model_metadata", con, index=False)
con.execute("CREATE UNIQUE INDEX ux_results ON model_results(model, img_size)")
con.execute("CREATE UNIQUE INDEX ux_bench ON benchmark_infer(arch, img_size)")
con.execute("CREATE INDEX ix_results_arch ON model_results(arch)")
con.commit()

for t in ("model_results", "benchmark_infer", "model_metadata"):
    n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(t, n)
print("results rows with no benchmark match:",
      con.execute("""SELECT COUNT(*) FROM model_results r LEFT JOIN benchmark_infer b
                     ON r.arch=b.arch AND r.img_size=b.img_size WHERE b.arch IS NULL""").fetchone()[0])
print("results rows with NULL top1_a:",
      con.execute("SELECT COUNT(*) FROM model_results WHERE top1_a IS NULL").fetchone()[0])
con.close()
