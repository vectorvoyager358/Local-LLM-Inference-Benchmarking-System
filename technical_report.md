# Local LLM Inference and Evaluation Study

## 1. Executive Summary

This project explored the practical trade-offs of running Small Language Models (SLMs) entirely offline using Ollama. The objective was to evaluate local inference performance, output quality, structured output reliability, and model selection decisions using empirical measurements rather than subjective preference.

Three models were evaluated:

- Llama 3.2 3B
- Phi3 Mini
- Mistral 7B

The study focused on:

- Inference performance
- Throughput
- Time To First Token (TTFT)
- Structured output reliability
- Model quality evaluation
- Memory consumption
- Temperature sensitivity

The final objective was to identify the model that provided the best balance between performance, quality, and resource consumption on consumer hardware.

---

# 2. Problem Statement

Most AI applications today rely on hosted APIs such as GPT, Claude, or Gemini.

However, many real-world environments require:

- Offline operation
- Reduced latency
- Privacy preservation
- Regulatory compliance
- Cost control
- Edge deployment

These constraints make local model execution an increasingly important engineering capability.

The purpose of this project was to understand the engineering challenges associated with deploying and operating local language models while evaluating their practical trade-offs.

---

# 3. Test Environment

## Hardware

- Machine: MacBook Pro (13-inch, 2022)
- Processor: Apple M2
- Memory: 8 GB Unified Memory
- GPU: Apple Silicon Integrated GPU

## Software

- Operating System: macOS Tahoe 26.4.1
- Ollama: 0.20.7
- Python: 3.11.15

---

# 4. Methodology

The project was divided into five phases:

### Phase 1 — Local Model Deployment

Objectives:

- Install Ollama
- Run local models
- Build a benchmarking CLI

Models:

- llama3.2:3b
- phi3:mini
- mistral:7b

---

### Phase 2 — Performance Benchmarking

Objectives:

- Measure latency
- Measure throughput
- Compare model responsiveness

Metrics collected:

- Prompt evaluation duration
- Prompt token count
- Generation duration
- Generated token count
- Total latency
- Tokens per second

A standardized prompt set was used across all models to ensure consistency.

---

### Phase 2.5 — Model Quality Evaluation

Objectives:

- Evaluate response quality
- Compare models beyond performance metrics

Evaluation categories:

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

Each response was manually scored across:

- Correctness
- Clarity
- Conciseness
- Instruction Following

using a 1–5 rating scale.

---

### Phase 3 — Structured Output Reliability

Objectives:

- Enforce deterministic outputs
- Validate model responses
- Recover from invalid outputs

Implementation:

Prompt
→ JSON Response
→ Pydantic Validation
→ Retry on Failure
→ Success / Failure

A retry mechanism was implemented that automatically reprompted the model when validation failed.

---

### Phase 4 — Temperature Study

Objectives:

- Understand output variability
- Compare deterministic and creative generation

Temperatures evaluated:

- 0.0
- 0.7

A shared prompt set was used to compare output consistency.

---

### Phase 5 — TTFT and Memory Evaluation

Objectives:

- Measure user-perceived responsiveness
- Evaluate model resource consumption

Metrics:

- Cold Start TTFT
- Warm Start TTFT
- Memory Usage

# 5. Benchmark Results

## Throughput Results

Average throughput was calculated using generated tokens divided by generation duration.

| Model       | Avg Tokens/Sec |
| ----------- | -------------: |
| llama3.2:3b |          41.82 |
| phi3:mini   |          38.35 |
| mistral:7b  |          19.33 |

### Observations

Llama 3.2 3B achieved the highest throughput while also maintaining relatively low latency.

Phi3 Mini produced competitive throughput but did not significantly outperform Llama despite its smaller perceived size.

Mistral 7B produced approximately half the throughput of Llama 3.2 3B, demonstrating the performance cost associated with larger models.

---

## Latency Results

Cold and warm inference behavior showed significant differences across all models.

Large portions of perceived latency were attributed to model initialization and loading rather than token generation itself.

### Key Observation

Throughput alone is not sufficient for model selection.

Two models can produce tokens at similar rates while exhibiting very different startup behavior.

---

# 6. Time To First Token (TTFT) Results

TTFT was measured under two scenarios:

### Cold Start

Model not already loaded into memory.

### Warm Start

Model already loaded and initialized.

| Model       | Cold TTFT (s) | Warm TTFT (s) |
| ----------- | ------------: | ------------: |
| llama3.2:3b |          3.04 |          0.19 |
| phi3:mini   |          3.20 |          0.14 |
| mistral:7b  |         10.34 |          0.68 |

### Observations

Mistral 7B exhibited the largest cold-start overhead.

However, warm-start measurements revealed that most of the observed delay originated from model loading rather than token generation.

This distinction became an important finding because it demonstrated that model responsiveness depends heavily on deployment configuration.

---

# 7. Model Quality Evaluation

Performance alone was not considered sufficient for model selection.

A separate quality evaluation was performed across multiple categories.

Categories:

* Reasoning
* Coding
* Summarization
* JSON Generation
* Instruction Following
* Technical Explanation
* Creativity
* Security
* System Design
* Edge Cases

Responses were manually scored using the following criteria:

* Correctness
* Clarity
* Conciseness
* Instruction Following

Each metric was evaluated on a 1–5 scale.

## Category Winners

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

### Observations

Mistral 7B consistently produced the strongest natural-language responses and demonstrated superior reasoning and explanation quality.

Llama 3.2 3B produced the strongest coding responses and delivered the best overall balance between performance and quality.

Phi3 Mini performed well in structured-output tasks but frequently produced overly verbose responses.

---

# 8. Temperature Study

A temperature comparison was performed using:

* Temperature = 0.0
* Temperature = 0.7

### Findings

Deterministic factual prompts showed little variation between temperatures.

Creative prompts exhibited noticeable changes in wording, tone, and structure.

Incorrect reasoning generally remained incorrect across temperature settings.

Temperature adjustments improved output diversity but did not improve reasoning quality or structured output reliability.

### Engineering Insight

Temperature influences randomness, not intelligence.

Lower temperatures are preferable when deterministic behavior is required.

Higher temperatures are useful when creativity and output diversity are desired.

---

# 9. Memory Measurement Methodology

## Initial Approach: Process RSS Measurement

The first memory measurement strategy used Python's `psutil` library to inspect the Resident Set Size (RSS) of the Ollama process.

Procedure:

1. Measure memory before loading a model.
2. Load the model using a warm-up request.
3. Measure memory again.
4. Compute the difference.

### Initial Results

| Model       | RAM Before (MB) | RAM After (MB) | Delta (MB) |
| ----------- | --------------: | -------------: | ---------: |
| llama3.2:3b |           24.61 |        2094.41 |   +2069.80 |
| phi3:mini   |         2094.41 |        3536.30 |   +1441.89 |
| mistral:7b  |         3536.30 |         727.00 |   -2809.30 |

### Problem Encountered

The Mistral measurement produced a negative memory delta.

This result was not physically meaningful and suggested that the methodology was not accurately measuring model memory requirements.

Further investigation revealed that Ollama dynamically:

* Loads models into memory
* Unloads inactive models
* Reuses memory allocations
* Maintains internal caching behavior

As a result:

Process RSS Delta ≠ Actual Model Memory Requirement

---

## Revised Approach: Controlled Single-Model Measurement

A second methodology was adopted using:

```bash
ollama ps
```

Procedure:

1. Stop all loaded models.
2. Load a single model.
3. Measure memory usage using `ollama ps`.
4. Stop the model.
5. Repeat for each model.

This ensured that only one model was resident in memory at a time.

### Final Memory Results

| Model       | Memory Usage |
| ----------- | -----------: |
| llama3.2:3b |       2.8 GB |
| phi3:mini   |       4.0 GB |
| mistral:7b  |       5.1 GB |

### Observations

Mistral 7B consumed the most memory.

Llama 3.2 3B consumed the least memory while also delivering the strongest overall performance profile.

Phi3 Mini required more memory than initially expected relative to its perceived model size.

---

# 10. Engineering Challenges Encountered

This project exposed several practical engineering challenges that are frequently encountered in real-world AI systems.

## Challenge 1: Measuring Memory Correctly

Initial memory measurements appeared incorrect.

Investigation revealed that process-level metrics were affected by Ollama's internal model management.

A revised methodology was developed to obtain more reliable measurements.

### Lesson Learned

Measurement methodology is often as important as the metric itself.

---

## Challenge 2: Structured Output Reliability

Even when instructed to return JSON, models occasionally generated:

* Error objects
* Additional fields
* Incorrect schemas

Examples included:

```json
{
  "error": "Invalid request",
  "message": "..."
}
```

instead of the required structure.

### Solution

A validation pipeline was implemented using:

* Pydantic
* Schema enforcement
* Retry logic
* Graceful failure handling

### Lesson Learned

Prompting alone is insufficient for reliable production systems.

Validation is mandatory.

---

## Challenge 3: Prompt Design

The wording of prompts significantly affected output quality.

For example, use of the term:

```text
schema
```

unexpectedly encouraged models to generate API-style error responses.

Replacing:

```text
Schema
```

with:

```text
Required Output Format
```

substantially improved reliability.

### Lesson Learned

Prompt phrasing can materially influence model behavior.

---

## Challenge 4: Cold vs Warm Performance

Initial latency measurements appeared to indicate that Mistral 7B was dramatically slower than other models.

Further investigation revealed that most of the delay originated from model loading rather than generation speed.

### Lesson Learned

Cold-start and warm-start measurements should be evaluated separately.

---

# 11. Final Recommendation

Based on all experiments, three conclusions emerged.

## Mistral 7B

Strengths:

* Best reasoning
* Best technical explanations
* Best summarization
* Best instruction following

Weaknesses:

* Highest memory consumption
* Slowest throughput
* Largest cold-start overhead

---

## Phi3 Mini

Strengths:

* Strong structured output generation
* Fast warm TTFT
* Competitive throughput

Weaknesses:

* Verbose responses
* Lower overall response quality

---

## Llama 3.2 3B

Strengths:

* Highest throughput
* Lowest memory consumption
* Strong coding performance
* Strong instruction following
* Excellent responsiveness

Weaknesses:

* Occasionally weaker reasoning than Mistral

---

## Recommended Model

For the tested hardware configuration:

```text
Llama 3.2 3B
```

provided the strongest overall balance between:

* Performance
* Memory consumption
* Throughput
* Response quality

and was therefore selected as the recommended model for local deployment.

---

# 12. Conclusion

This project demonstrated that local language models are capable of delivering useful performance while preserving privacy and reducing dependency on external services.

The study also highlighted that model selection should not be based solely on popularity or parameter count.

Through systematic benchmarking, quality evaluation, structured output validation, TTFT analysis, temperature studies, and memory measurements, a more complete understanding of local inference trade-offs was achieved.

The project successfully replicated several engineering patterns commonly used in production AI systems, including structured output enforcement, validation pipelines, retry mechanisms, and performance benchmarking.

These findings provide a practical foundation for future work involving local AI assistants, agent systems, quantized models, and edge deployments.

