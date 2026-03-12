import json
import os

from openai import OpenAI
from core.analysis import feedback_to_prompt 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_strengths(feedback_list: list[dict]) -> dict:
    # 1. Guard
    if len(feedback_list) < 5:
        raise ValueError("At least 5 feedback entries are required for analysis.")

    # 2. Gör om feedback till text-rader
    prompt_lines = feedback_to_prompt(feedback_list)

    # 3. Instruktion till modellen
    instructions = """
You analyze feedback entries about one person from other persons.

Your task is to identify exactly three recurring strengths based on patterns across the feedback.

Rules:
- Return exactly 3 strengths.
- Each strength name must be short.
- Each reason must be very short.
- Do not include weaknesses.
- Return ONLY valid JSON in this exact format:

{
  "strengths": [
    {"name": "string", "reason": "string"},
    {"name": "string", "reason": "string"},
    {"name": "string", "reason": "string"}
  ]
}
"""

    # 4. OpenAI-anrop
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "system",
                "content": instructions,
            },
            {
                "role": "user",
                "content": f"Here are the feedback entries:\n\n{prompt_lines}",
            },
        ],
        text={
            "format": {
                "type": "json_object"
            }
        },
    )

    # 5. Gör JSON-text till Python-dict
    return json.loads(response.output_text)