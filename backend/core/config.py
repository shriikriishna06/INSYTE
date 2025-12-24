"""
Central configuration for the Sentiment Intelligence SaaS.

IMPORTANT:
- Only constants and thresholds live here
- NO logic
- NO API calls
"""

# MODE SELECTION

# Force batching during build/testing to control cost & speed
# In production (paid), you can safely raise this (e.g. 50)
SINGLE_MODE_THRESHOLD = 0


# BATCHING CONFIGURATION

# Number of reviews sent per Gemini call
# 5 = safest, 10 = faster but slightly riskier
BATCH_SIZE = 5


# REQUEST SAFETY LIMITS (CRITICAL FOR SAAS)

# Hard cap to prevent abuse or accidental huge uploads
MAX_REVIEWS_PER_REQUEST = 1000

# Max characters allowed per review (optional safety)
MAX_REVIEW_LENGTH = 2000


# RISK & INSIGHT THRESHOLDS

# Negative sentiment ratio thresholds
RISK_HIGH_THRESHOLD = 0.40      # >= 40% negative → HIGH risk
RISK_MEDIUM_THRESHOLD = 0.20   # >= 20% negative → MEDIUM risk


# CONFIDENCE & OUTPUT CONTROL

# Decimal precision for confidence values
CONFIDENCE_PRECISION = 2


# CONTRACT SAFETY

# Allowed sentiment labels (defensive programming)
VALID_SENTIMENTS = {"positive", "neutral", "negative"}


# LOGGING / OBSERVABILITY

# Enable lightweight console logging
ENABLE_REQUEST_LOGGING = True
