import pandas as pd

from paths import DATA_DIR

df = pd.read_csv(DATA_DIR / "benchmark.csv")

summary = df.groupby("model").agg({
    "prompt_eval_duration": "mean",
    "eval_duration": "mean",
    "total_duration": "mean",
    "load_duration": "mean",
    "tokens_per_second": "mean",
    "eval_count": "mean"
}).reset_index()

summary = summary.round(2)

print("\nModel Benchmark Summary:\n")
print(summary)

summary_path = DATA_DIR / "benchmark_summary.csv"
summary.to_csv(summary_path, index=False)

print(f"\nSaved summary to {summary_path}")