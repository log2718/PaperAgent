# Cost per configuration

Per-question figures are means over the text-involving development questions that were run (not copied from another run) with usage logged. `cost_usd` is the API list-price equivalent reported by the CLI, not an actual bill. Input tokens are uncached + cache-creation + cache-read. One-time cost is chunking (and for the vector configurations the embedding and index build) on this machine; `no_embedding` only needs the paper texts.

| Run | Questions | Mean latency (s) | Total latency (min) | LLM calls | Input tokens | Output tokens | Cost (USD) mean | Cost (USD) total | One-time chunk (s) | One-time index (s) | Index size |
|---|---|---|---|---|---|---|---|---|---|---|---|
| runs/baseline_repeat | 28 | 21.3 | 9.9 | 1.2 | 8,977 | 1,743 | 0.051 | 1.42 | 5.4 | 52.3 | 1.53 MB |
| runs/chunk_paragraph | 28 | 18.9 | 8.8 | 1.2 | 3,599 | 1,434 | 0.026 | 0.73 | 5.7 | 61.5 | 7.24 MB |
| runs/chunk_paragraph_matched | 28 | 23.8 | 11.1 | 1.2 | 9,659 | 1,957 | 0.055 | 1.55 | 5.7 | 61.5 | 7.24 MB |
| runs/chunk_paper | 28 | 23.4 | 10.9 | 1.2 | 113,583 | 1,903 | 0.471 | 13.18 | 4.5 | 7.5 | 0.05 MB |
| runs/no_embedding | 28 | 25.8 | 12.0 | 2.3 | 64,888 | 1,906 | 0.276 | 7.73 | 4.5 | - | - |
