from typing import List, Dict
from collections import defaultdict

from backend.models.batch_schema import ReviewResult, AggregatedInsights


def aggregate_insights(results: List[ReviewResult]) -> AggregatedInsights:
    """
    Aggregates per-review analysis results into business-level insights
    and builds factor → supporting review mapping.
    """

    total_reviews = len(results)

    sentiment_count = defaultdict(int)
    confidence_sum = 0.0
    mixed_count = 0

    factor_mentions = defaultdict(int)
    factor_positive = defaultdict(int)
    factor_negative = defaultdict(int)

    factor_review_map = defaultdict(list)

    for r in results:
        sentiment_count[r.sentiment] += 1
        confidence_sum += r.confidence

        if r.sentiment == "neutral":
            mixed_count += 1

        for factor in r.factors:
            factor_mentions[factor] += 1
            factor_review_map[factor].append(r.review_id)

            if r.sentiment == "positive":
                factor_positive[factor] += 1
            elif r.sentiment == "negative":
                factor_negative[factor] += 1

    sentiment_distribution: Dict[str, float] = {
        k: round(v / total_reviews, 2) for k, v in sentiment_count.items()
    }

    average_confidence = round(confidence_sum / total_reviews, 2)

    pros = []
    cons = []

    for factor in factor_mentions:
        if factor_positive[factor] > factor_negative[factor]:
            pros.append(factor)
        elif factor_negative[factor] > factor_positive[factor]:
            cons.append(factor)

    mixed_feedback_ratio = round(mixed_count / total_reviews, 2)

    negative_ratio = sentiment_distribution.get("negative", 0.0)

    if negative_ratio >= 0.4:
        risk_level = "high"
    elif negative_ratio >= 0.2:
        risk_level = "medium"
    else:
        risk_level = "low"

    return AggregatedInsights(
        total_reviews=total_reviews,
        sentiment_distribution=sentiment_distribution,
        average_confidence=average_confidence,
        pros=pros,
        cons=cons,
        mixed_feedback_ratio=mixed_feedback_ratio,
        risk_level=risk_level,
        factor_review_map=dict(factor_review_map)
    )
