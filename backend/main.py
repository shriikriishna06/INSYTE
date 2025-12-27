from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import time

from backend.models.sentiment_schema import SentimentResponse
from backend.models.batch_schema import (
    BatchAnalyzeRequest,
    BatchAnalyzeResponse
)

from backend.services.sentiment_service import analyze_sentiment
from backend.services.batch_sentiment_service import analyze_reviews_in_batch
from backend.services.factor_mapper import map_factors
from backend.services.aggregation_service import aggregate_insights
from backend.utils.confidence_calibrator import calibrate_confidence

from backend.core.config import (
    SINGLE_MODE_THRESHOLD,
    MAX_REVIEWS_PER_REQUEST,
    MAX_REVIEW_LENGTH,
    ENABLE_REQUEST_LOGGING
)

app = FastAPI(title="Sentiment Intelligence API")

# frontend_dir = Path(__file__).resolve().parents[1] / "frontend" / "public"

# @app.get("/")
# def root():
#     return FileResponse(frontend_dir / "landingpage.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
#   Single Review

@app.post("/api/analyze", response_model=SentimentResponse)
async def analyze_single(request: dict):
    """
    Analyze a single customer review.
    """
    if "text" not in request or not request["text"].strip():
        raise HTTPException(status_code=400, detail="Text is required")

    return await analyze_sentiment(request["text"])


# Batch Analysis  (currently used)

@app.post("/api/batch-analyze", response_model=BatchAnalyzeResponse)
async def analyze_batch(request: BatchAnalyzeRequest):
    """
    Analyze multiple customer reviews.
    Automatically decides single vs batch mode.
    """

    start_time = time.time()

    # Clean Input
    reviews = [r.strip() for r in request.reviews if r.strip()]

    if not reviews:
        raise HTTPException(status_code=400, detail="No valid reviews provided")

    # Request limit handler
    if len(reviews) > MAX_REVIEWS_PER_REQUEST:
        raise HTTPException(
            status_code=413,
            detail=f"Maximum {MAX_REVIEWS_PER_REQUEST} reviews allowed per request"
        )

    processed_reviews = []
    for r in reviews:
        if len(r) > MAX_REVIEW_LENGTH:
            processed_reviews.append(r[:MAX_REVIEW_LENGTH])
        else:
            processed_reviews.append(r)

    reviews = processed_reviews

    # Mode decision logic (single or in-batch)
    if len(reviews) <= SINGLE_MODE_THRESHOLD:
        # Single (accurate)
        results = []
        for idx, text in enumerate(reviews):
            r = await analyze_sentiment(text)
            factors = map_factors(r.summary)

            r.confidence = calibrate_confidence(
                confidence=r.confidence,
                sentiment=r.sentiment, 
                factors=factors
                )

            r.factors = factors

            results.append(
                {
                    "review_id": idx,
                    "sentiment": r.sentiment,
                    "confidence": r.confidence,
                    "summary": r.summary,
                    "factors": map_factors(r.summary)
                }
            )
    else:
        # Batch (fast)
        results = await analyze_reviews_in_batch(reviews)

    # Aggregation 
    insights = aggregate_insights(results)

    if ENABLE_REQUEST_LOGGING:
        duration = round(time.time() - start_time, 2)
        print(f"[BATCH] reviews={len(reviews)} | time={duration}s")

    return BatchAnalyzeResponse(
        results=results,
        insights=insights
    )

# app.mount(
#     "/",
#     StaticFiles(directory=str(frontend_dir)),
#     name="static"
# )
