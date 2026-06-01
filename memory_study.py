import csv
import time
import psutil
import requests


MODELS = [
    "llama3.2:3b",
    "phi3:mini",
    "mistral:7b"
]


def get_ollama_ram_mb():
    total_ram = 0

    for process in psutil.process_iter(["name", "memory_info"]):
        try:
            process_name = process.info["name"]

            if process_name and "ollama" in process_name.lower():
                total_ram += process.info["memory_info"].rss

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return total_ram / (1024 * 1024)


def load_model(model):
    requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": "warmup",
            "stream": False
        }
    )


if __name__ == "__main__":
    csv_file = "memory_results.csv"

    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow([
                "model",
                "ram_before_mb",
                "ram_after_mb",
                "ram_delta_mb"
            ])

        for model in MODELS:
            print(f"\nTesting model: {model}")

            ram_before = get_ollama_ram_mb()

            load_model(model)

            time.sleep(2)

            ram_after = get_ollama_ram_mb()

            ram_delta = ram_after - ram_before

            print(f"RAM before: {ram_before:.2f} MB")
            print(f"RAM after: {ram_after:.2f} MB")
            print(f"RAM delta: {ram_delta:.2f} MB")

            writer.writerow([
                model,
                round(ram_before, 2),
                round(ram_after, 2),
                round(ram_delta, 2)
            ])

    print(f"\nMemory results saved to {csv_file}")