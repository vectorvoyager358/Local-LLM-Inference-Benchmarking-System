import requests
import csv

TEMPERATURE_PROMPTS = [
    "Explain recursion in exactly 2 sentences.",
    "Generate JSON for a user named Vijay who is a software engineer.",
    "Write a short product description for a local AI assistant.",
    "What is larger: 9.11 or 9.9?",
    "Summarize the benefits of local AI inference in 3 sentences."
]


def query_model(prompt, temperature):
    result = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
    )
    return result.json()


if __name__ == "__main__":
    csv_file = "temperature_study.csv"
    prompts = TEMPERATURE_PROMPTS
    temperatures = [0.0, 0.7]

    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(["prompt", "temperature", "response"])

        for prompt in prompts:
            for temperature in temperatures:
                result = query_model(prompt, temperature)
                response = result["response"]
                writer.writerow([prompt, temperature, response])

    print(f"Temperature study results saved to {csv_file}")