import json
import time
import csv
import requests


MODELS = [
    "llama3.2:3b",
    "phi3:mini",
    "mistral:7b"
]

PROMPT = "Explain the benefits of local AI inference in 5 sentences."


def warmup_model(model):
    requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": "warmup",
            "stream": False
        }
    )


def measure_ttft(model, prompt):
    start_time = time.time()
    first_token_time = None
    full_response = ""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            current_time = time.time()

            if first_token_time is None:
                first_token_time = current_time

            data = json.loads(line.decode("utf-8"))
            full_response += data.get("response", "")

    end_time = time.time()

    ttft = first_token_time - start_time if first_token_time else None
    total_latency = end_time - start_time

    return full_response, ttft, total_latency


if __name__ == "__main__":
    csv_file = "ttft_results.csv"

    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow([
                "model",
                "run_type",
                "ttft_seconds",
                "total_latency_seconds",
                "response_length"
            ])

        for model in MODELS:
            print(f"\nCold TTFT test for: {model}")

            response, ttft, total_latency = measure_ttft(model, PROMPT)

            writer.writerow([
                model,
                "cold",
                round(ttft, 2),
                round(total_latency, 2),
                len(response)
            ])

            print(f"Cold TTFT: {ttft:.2f} seconds")
            print(f"Cold total latency: {total_latency:.2f} seconds")

            print(f"\nWarming up model: {model}")
            warmup_model(model)

            print(f"Warm TTFT test for: {model}")

            response, ttft, total_latency = measure_ttft(model, PROMPT)

            writer.writerow([
                model,
                "warm",
                round(ttft, 2),
                round(total_latency, 2),
                len(response)
            ])

            print(f"Warm TTFT: {ttft:.2f} seconds")
            print(f"Warm total latency: {total_latency:.2f} seconds")

    print(f"\nTTFT results saved to {csv_file}")