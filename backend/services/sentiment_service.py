import os
from dotenv import load_dotenv
from google import genai

from backend.utils.json_validator import validate_json
from backend.models.sentiment_schema import SentimentResponse

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
You are a sentiment analysis engine.

Analyze the overall emotional sentiment of the given text
and infer the user's behavioral intent behind the feedback.

Behavior patterns (internal use only):
- Genuine feedback
- Mixed but constructive feedback
- Protest or leverage-based complaint
- Passive-aggressive tone
- Emotionally satisfied but critical
- Overreaction or exaggerated dissatisfaction

Rules:
- Choose the dominant sentiment based on full context.
- If positive and negative points are balanced, choose "neutral".
- Do NOT overestimate confidence:
  - >0.9 only for extremely clear sentiment
  - 0.6–0.8 for normal clarity
  - <0.6 for mixed, indirect, or behavior-driven cases
- Think internally but do NOT reveal reasoning.

Output ONLY valid JSON in the exact format below.
The summary must briefly explain both sentiment and detected behavior.

{{
  "sentiment": "positive | neutral | negative",
  "confidence": 0.0,
  "summary": "One concise sentence explaining sentiment and user behavior."
}}

Text:
"{text}"
"""

async def analyze_sentiment(text: str, retries: int = 3) -> SentimentResponse:
    """
    Sends text to the Gemini model, validates the response, retries if needed,
    and guarantees a valid structured SentimentResponse.
    """

    for _ in range(retries):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=PROMPT_TEMPLATE.format(text=text)
        )

        is_valid, parsed = validate_json(response.text)

        if is_valid:
            return SentimentResponse(**parsed)

    return SentimentResponse(
        sentiment="neutral",
        confidence=0.0,
        summary="The system was unable to confidently analyze the text."
    )
