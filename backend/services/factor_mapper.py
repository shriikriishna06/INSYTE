from typing import List

FACTOR_KEYWORDS = {
    "Delivery / Logistics": [
        "delivery", "delayed", "late", "shipping", "logistics",
        "courier", "packaging", "arrived"
    ],
    "Reliability / Performance": [
        "crash", "crashes", "slow", "lag", "bug", "bugs",
        "unreliable", "performance", "freeze", "hang"
    ],
    "UX / Usability": [
        "ui", "ux", "design", "navigation", "interface",
        "usability", "layout", "easy to use"
    ],
    "Checkout / Payments": [
        "checkout", "payment", "pay", "cart",
        "transaction", "purchase", "billing"
    ],
    "Customer Support": [
        "support", "customer service", "helpful",
        "response", "resolved", "follow-up"
    ],
    "Pricing / Value": [
        "price", "pricing", "cost", "expensive",
        "cheap", "value", "worth"
    ]
} 


def map_factors(text: str) -> List[str]:
    """
    Maps a summary or review text to concrete business factors.
    Guarantees meaningful factor output.
    """
    text_lower = text.lower()
    matched_factors = []

    for factor, keywords in FACTOR_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            matched_factors.append(factor)
    
    if matched_factors:
        return matched_factors
    
    if any(word in text_lower for word in ["bad", "poor", "issue", "problem", "unacceptable"]):
        return ["General Experience"]

    return ["General Feedback"]
