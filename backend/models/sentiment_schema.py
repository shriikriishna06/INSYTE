from pydantic import BaseModel, Field


class SentimentResponse(BaseModel):
    """Schema representing the sentiment analysis result returned to clients."""
    
    sentiment: str = Field(..., description="Sentiment label: positive, neutral, or negative.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1.")
    summary: str = Field(..., description="Short explanation for classification.")

