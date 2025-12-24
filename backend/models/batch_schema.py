from pydantic import BaseModel, Field
from typing import List, Dict


class BatchAnalyzeRequest(BaseModel):
    """
    Request schema for batch sentiment analysis.
    Expects a list of raw customer review texts.
    """
    reviews: List[str] = Field(
        ...,
        min_items=1,
        description="List of customer review texts"
    )


class ReviewResult(BaseModel):
    """
    Analysis result for a single review.
    """
    review_id: int
    sentiment: str
    confidence: float
    summary: str
    factors: List[str]


class AggregatedInsights(BaseModel):
    """
    Aggregated business-level insights derived from batch analysis.
    """
    total_reviews: int
    sentiment_distribution: Dict[str, float]
    average_confidence: float
    pros: List[str]
    cons: List[str]
    mixed_feedback_ratio: float
    risk_level: str
    factor_review_map: Dict[str, List[int]]


class BatchAnalyzeResponse(BaseModel):
    """
    Final response schema for batch sentiment analysis.
    Includes per-review results and aggregated insights.
    """
    results: List[ReviewResult]
    insights: AggregatedInsights
