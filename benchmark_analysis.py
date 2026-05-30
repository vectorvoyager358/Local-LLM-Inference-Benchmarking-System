import pandas as pd

df = pd.read_csv("benchmark.csv")

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

summary.to_csv("benchmark_summary.csv", index=False)

print("\nSaved summary to benchmark_summary.csv")