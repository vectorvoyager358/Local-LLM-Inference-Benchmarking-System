from app import query_model
from evaluation_prompts import EVALUATION_PROMPTS
import csv

prompts = EVALUATION_PROMPTS
models = [
    "llama3.2:3b",
    "phi3:mini",
    "mistral:7b"
]

csv_file = "quality_results.csv"

with open(csv_file, "a", newline="") as f:
    writer = csv.writer(f)

    if f.tell() == 0:
        writer.writerow(["model", "category", "prompt", "response"])

    for model in models:
        for category, prompts in EVALUATION_PROMPTS.items():
            for prompt in prompts:
                print(f"Running model: {model} with category: {category} and prompt: {prompt}")
                result = query_model(prompt, model)
                response = result["response"]
                if category == "system_design":
                    print(result)
                writer.writerow([model, category, prompt, response])
    print(f"Quality results saved to {csv_file}")