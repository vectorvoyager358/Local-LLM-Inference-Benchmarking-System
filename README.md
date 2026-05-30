# Local LLM Inference & Benchmarking System

This project benchmarks small language models running locally with Ollama.

## Models Tested

- llama3.2:3b
- phi3:mini
- mistral:7b

## Metrics Collected

- Prompt evaluation duration
- Prompt token count
- Generation duration
- Generated token count
- Total duration
- Load duration
- Tokens per second

## Benchmark Output

Raw benchmark results are saved to:

```text
benchmark.csv
```

Aggregated benchmark results are saved to:

```text
benchmark_summary.csv
```

