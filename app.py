import subprocess
import time
import csv
import requests
from prompts import TEST_PROMPTS


def query_model(prompt, model):

    result = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return result.json()


def timed_query(prompt, model):
    start = time.time()
    response = query_model(prompt, model)
    end = time.time()

    latency = end - start
    return response, latency


if __name__ == "__main__":
    prompts = TEST_PROMPTS

    models = [
        "llama3.2:3b",
        "phi3:mini",
        "mistral:7b"
    ]

    csv_file = "benchmark.csv"

    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow([
                "model",
                "prompt",
                "prompt_eval_duration",
                "prompt_eval_count",
                "eval_duration",
                "eval_count",
                "total_duration",
                "load_duration",
                "tokens_per_second"
            ])

        for model in models:
            for prompt in prompts:
                print(f"\nRunning model: {model}")
                print(f"Prompt: {prompt}")

                response = query_model(prompt, model)
                prompt_eval_duration = response["prompt_eval_duration"]/1000000000
                eval_duration = response["eval_duration"]/1000000000
                total_duration = response["total_duration"]/1000000000
                load_duration = response["load_duration"]/1000000000
                prompt_eval_count = response["prompt_eval_count"]
                eval_count = response["eval_count"]
                tokens_per_second = eval_count / eval_duration

                writer.writerow([
                    model,
                    prompt,
                    prompt_eval_duration,
                    prompt_eval_count,
                    eval_duration,
                    eval_count,
                    total_duration,
                    load_duration,
                    tokens_per_second
                ])
    print(f"\nBenchmark results saved to {csv_file}")