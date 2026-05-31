import json
import requests
from pydantic import ValidationError
from schemas import TaskSummary

"""
Generates structured JSON output from a local LLM.

Flow:
1. Generate response
2. Parse JSON
3. Validate with Pydantic
4. Retry once if validation fails
5. Return structured success/failure result
"""

def get_schema_prompt():
    return """
Output format:

{
  "title": "...",
  "priority": "high",
  "summary": "..."
}

Required fields:
- title
- priority
- summary

Allowed priority values:
- high
- medium
- low

Do not add any other fields.
"""

def query_model(prompt, model="llama3.2:3b"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
    )

    return response.json()["response"]


def validate_response(response):
    parsed_json = json.loads(response)
    return TaskSummary.model_validate(parsed_json)


def generate_structured_output(prompt, model="llama3.2:3b"):
    max_attempts = 2
    last_response = None
    last_error = None

    for attempt in range(max_attempts):
        try:
            response = query_model(prompt, model)
            last_response = response

            print(f"\nAttempt {attempt + 1}")
            print("\nRaw Response:")
            print(response)

            validated_output = validate_response(response)

            return {
                "success": True,
                "data": validated_output,
                "attempts": attempt + 1,
                "error": None,
                "last_response": response
            }

        except (json.JSONDecodeError, ValidationError) as e:
            last_error = str(e)

            print("\nValidation Failed")
            print(e)

            prompt = f"""
Your previous JSON did not match the required output format.

Validation Error:
{e}

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.

Required output format:
{get_schema_prompt()}

Task description:
Customer login page is failing for some users after deployment.
"""

    return {
        "success": False,
        "data": None,
        "attempts": max_attempts,
        "error": last_error,
        "last_response": last_response
    }

if __name__ == "__main__":

    prompt = f"""
You are extracting a task summary.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.

Required output format:
{get_schema_prompt()}

Task description:
Customer login page is failing for some users after deployment.
"""

    result = generate_structured_output(prompt)

    print("\nFinal Result:")
    print(result)