def calibrate_confidence(confidence: float, sentiment: str, factors: list) -> float:
    confidence = min(confidence, 0.9)

    if sentiment == "neutral":
        confidence = min(confidence, 0.75)

    if len(factors) > 1:
        confidence = min(confidence, 0.85)

    return round(confidence, 2)
 