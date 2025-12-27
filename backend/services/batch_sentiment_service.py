import os
from typing import List
from dotenv import load_dotenv
from google import genai
import json 
import re
import asyncio
from google.genai.errors import ServerError
from backend.services.factor_mapper import map_factors
from backend.utils.confidence_calibrator import calibrate_confidence
from backend.models.batch_schema import ReviewResult
from backend.core.config import BATCH_SIZE

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

BATCH_PROMPT_TEMPLATE = """
You are a sentiment analysis engine.

Analyze EACH customer review independently.
Do NOT mix reviews.
Do NOT skip any review.

Return a STRICTLY VALID JSON ARRAY.
Each array element must correspond to the same index as the input review.

Each JSON object MUST have this format:
{{
  "sentiment": "positive | neutral | negative",
  "confidence": 0.0,
  "summary": "One concise sentence explaining sentiment and user behavior."
}}

Customer reviews:
{reviews}
"""


def _chunk_reviews(reviews: List[str], size: int) -> List[List[str]]:
    """
    Splits reviews into fixed-size chunks.
    """
    return [reviews[i:i + size] for i in range(0, len(reviews), size)]


async def analyze_reviews_in_batch(reviews: List[str]) -> List[ReviewResult]:
    """
    Performs true batch sentiment analysis using Gemini.
    Returns per-review results with stable ordering.
    """

    results: List[ReviewResult] = []
    review_chunks = _chunk_reviews(reviews, BATCH_SIZE)
    review_id = 0

    for chunk in review_chunks:
        formatted_reviews = "\n".join(
            [f"{idx}. {text}" for idx, text in enumerate(chunk)]
        )
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=BATCH_PROMPT_TEMPLATE.format(reviews=formatted_reviews)
            )
                break
            except ServerError:
                if attempt == 2:
                    raise RuntimeError("AI service temporarily unavailable")
                await asyncio.sleep(1.5 * (attempt + 1))       

        raw = response.text.strip()

        raw = re.sub(r"```json|```", "", raw).strip()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError("Invalid batch JSON response from Gemini")

        if not isinstance(parsed, list):
            raise ValueError("Batch response is not a JSON array")

        if len(parsed) != len(chunk):
            raise ValueError("Mismatch between input reviews and output results")

      
        for item in parsed:
            sentiment = item["sentiment"]
            raw_confidence = item["confidence"]
            summary = item["summary"]

            factors = map_factors(summary)

            confidence = calibrate_confidence(
                confidence=raw_confidence,
                sentiment=sentiment,
                factors=factors
            )

            results.append(
                ReviewResult(
                    review_id=review_id,
                    sentiment=sentiment,
                    confidence=confidence,
                    summary=summary,
                    factors=factors
                )
            )
            review_id += 1

    return results
