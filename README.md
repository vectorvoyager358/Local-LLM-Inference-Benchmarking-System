# Local LLM Inference & Benchmarking System

## Repository Structure

src/     -> benchmarking and evaluation scripts
data/    -> benchmark outputs and evaluation scores
docs/    -> supporting documentation

Run scripts from the repository root, for example:

```bash
python src/app.py
python src/benchmark_analysis.py
python src/quality_evaluation.py
```

---

A local AI benchmarking project that evaluates Small Language Models (SLMs) running entirely offline using Ollama.

The project compares model performance, throughput, latency, and response quality across multiple local models.

For the full methodology, analysis, and conclusions, see the [Technical Report](technical_report.md).

---

## Models Evaluated

- llama3.2:3b
- phi3:mini
- mistral:7b

---

## Test Environment

### Hardware

- Machine: MacBook Pro (13-inch, 2022)
- Processor: Apple M2
- Memory: 8 GB Unified Memory
- GPU: Integrated Apple M2 GPU

### Software

- Operating System: macOS Tahoe 26.4.1
- Python: 3.11.5
- Ollama: 0.20.7

---

## Benchmark Configuration

### Performance Benchmark

- 25 benchmark prompts
- Local inference using Ollama
- Stream disabled
- Metrics collected:
  - Prompt evaluation duration
  - Prompt token count
  - Generation duration
  - Generated token count
  - Total duration
  - Load duration
  - Tokens per second

### Quality Evaluation

- 10 evaluation prompts
- Categories:
  - Reasoning
  - Coding
  - Summarization
  - JSON Generation
  - Instruction Following
  - Technical Explanation
  - Creativity
  - Security
  - System Design
  - Edge Cases

---

## Benchmark Results


| Model       | Avg Tokens/Sec |
| ----------- | -------------- |
| llama3.2:3b | 41.82          |
| phi3:mini   | 38.35          |
| mistral:7b  | 19.33          |


### Performance Ranking

1. llama3.2:3b
2. phi3:mini
3. mistral:7b

---

## Quality Evaluation Results

### Average Scores


| Model       | Correctness | Clarity | Conciseness | Instruction Following |
| ----------- | ----------- | ------- | ----------- | --------------------- |
| mistral:7b  | 4.6         | 4.9     | 4.3         | 4.7                   |
| phi3:mini   | 4.3         | 3.6     | 2.9         | 4.5                   |
| llama3.2:3b | 4.1         | 4.7     | 3.7         | 4.8                   |


### Category Winners


| Category              | Winner                   |
| --------------------- | ------------------------ |
| Reasoning             | mistral:7b               |
| Coding                | llama3.2:3b              |
| Summarization         | mistral:7b               |
| JSON Generation       | phi3:mini                |
| Instruction Following | mistral:7b               |
| Technical Explanation | mistral:7b               |
| Creativity            | llama3.2:3b              |
| Security              | llama3.2:3b / mistral:7b |
| System Design         | mistral:7b               |
| Edge Case             | phi3:mini                |


---

## Key Findings

### llama3.2:3b

- Fastest model tested
- Best throughput
- Strong coding performance
- Best balance between speed and quality

### phi3:mini

- Strong structured output generation
- Good throughput
- Often verbose in explanations

### mistral:7b

- Highest overall response quality
- Strongest reasoning and technical explanations
- Lowest throughput among tested models

---

## Conclusion

Mistral 7B produced the strongest overall response quality, while Llama 3.2 3B provided the best balance between performance and quality.

For local inference on the tested hardware, Llama 3.2 3B was the recommended model due to its significantly higher throughput while maintaining strong response quality.

---

### Benchmark Constraints

All benchmarks were executed on a MacBook Pro (M2, 8 GB RAM). Results may vary significantly on systems with more memory, discrete GPUs, or different CPU architectures.

---

## Structured Output Validation

Implemented a structured output pipeline for local language models.

Features:

- JSON-only responses
- Pydantic schema validation
- Automatic retry on validation failure
- Graceful failure handling after retry exhaustion

Workflow:

Prompt
→ JSON Response
→ Validation
→ Retry
→ Success / Failure

Example Schema:

{
  "title": "string",
  "priority": "high | medium | low",
  "summary": "string"
}

---

## Temperature Study

A comparison was performed using temperature 0.0 and 0.7.

### Observations

- Factual prompts showed little variation between temperatures.
- Creative prompts produced noticeably different wording and structure.
- Incorrect reasoning remained incorrect across temperatures.
- Temperature changes did not improve structured output reliability.
- Lower temperatures produced more deterministic outputs and are preferred for structured generation workflows.

---

## Time To First Token (TTFT) Study

TTFT measures how long it takes for the first token of a response to be generated after a request is sent.

Two scenarios were measured:

### Cold Start

Model is not already loaded into memory.

### Warm Start

Model is already loaded and initialized.

### Results

| Model | Cold TTFT (s) | Warm TTFT (s) |
|---------|---------:|---------:|
| llama3.2:3b | 3.04 | 0.19 |
| phi3:mini | 3.20 | 0.14 |
| mistral:7b | 10.34 | 0.68 |

### Observations

- Mistral 7B experienced the largest cold-start overhead.
- Warm-start TTFT was significantly lower for all models.
- Most of Mistral's perceived delay came from model loading rather than token generation.
- Llama 3.2 3B provided the best overall balance between throughput, latency, and response quality.

---

## Memory Usage Comparison

Memory measurements were collected using a controlled single-model loading approach with `ollama ps`.

| Model | Memory Usage |
|---------|---------:|
| llama3.2:3b | 2.8 GB |
| phi3:mini | 4.0 GB |
| mistral:7b | 5.1 GB |

### Key Findings

- Mistral 7B consumed the most memory.
- Llama 3.2 3B consumed the least memory among the tested models.
- Llama 3.2 3B provided the strongest overall balance between memory usage, throughput, and response quality.