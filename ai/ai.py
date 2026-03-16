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
You analyze feedback entries about one person.

First, internally identify patterns or recurring themes across the feedback entries.
Look for behaviors, actions, or examples that suggest broader strengths.

Then summarize these patterns into exactly three strengths.

Do not just repeat words from the feedback.
Instead infer broader strengths from the behaviors described.

Example:
If feedback mentions painting, music, imagination or ideas, the strength could be "Creativity".

Rules:
- Return exactly 3 strengths.
- Each strength name must be short (1–2 words).
- Each reason must be very short.
- Prefer strengths supported by multiple feedback entries.
- Return ONLY valid JSON in this format:

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