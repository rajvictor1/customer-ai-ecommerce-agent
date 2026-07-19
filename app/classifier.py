import re
from typing import Tuple, Optional
from app.models import Customer, Message, Conversation, IncomingEvent

INTENT_PATTERNS = {
    "EC_ORDER_TRACK": [r"where is my order", r"track my order", r"order status", r"order #?\s*(\d+)"],
    "EC_RETURN_REFUND": [r"\breturn\b", r"\brefund\b", r"\bexchange\b", r"i want to send back"],
    "EC_PRODUCT_SEARCH": [r"find", r"looking for", r"search for", r"under \$?\d+"],
    "EC_FAQ": [r"hours", r"shipping", r"delivery", r"policy", r"discount", r"promo"],
}

SAFETY_PATTERNS = [
    (r"\bemergency\b|\bheart attack\b|\bstroke\b|\bcan.?t breathe\b|\bsuicide\b|\bkill myself\b", "SAFETY_EMERGENCY"),
    (r"my ssn\b|\bsocial security\b|\bpassword\b|\bcvv\b|\bcredit card number\b", "SAFETY_PII"),
]

ENTITY_PATTERNS = {
    "order_id": re.compile(r"\b#?(\d{4,})\b"),
    "date": re.compile(r"\b(today|tomorrow|next\s+\w+|\d{1,2}/\d{1,2}(?:/\d{2,4})?)\b", re.I),
}

class IntentClassifier:
    def classify(self, text: str) -> Tuple[str, float]:
        text_lower = text.lower()
        best_intent = "UNKNOWN"
        best_score = 0.0
        for intent, patterns in INTENT_PATTERNS.items():
            for pat in patterns:
                match = re.search(pat, text_lower)
                if match:
                    score = 0.85 + (0.05 if match.lastindex and match.group(1) else 0)
                    if score > best_score:
                        best_score = score
                        best_intent = intent
        return best_intent, round(min(best_score, 0.98), 2)

    def extract_entities(self, text: str) -> dict:
        entities = {}
        for key, pat in ENTITY_PATTERNS.items():
            m = pat.search(text)
            if m:
                entities[key] = m.group(1).strip() if m.lastindex else m.group(0).strip()
        return entities

    def safety_check(self, text: str) -> Tuple[bool, Optional[str]]:
        for pat, reason in SAFETY_PATTERNS:
            if re.search(pat, text, re.I):
                return True, reason
        return False, None
