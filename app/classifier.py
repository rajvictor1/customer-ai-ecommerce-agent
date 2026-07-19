import os
import re
import json
from typing import Tuple, Optional

# Lazy import OpenAI so the app starts without an API key
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

INTENT_PATTERNS = {
    "EC_RETURN_REFUND": [r"\breturn\b|\brefund\b|\bexchange\b|i want to send back"],
    "EC_ORDER_TRACK": [r"where is my order|track my order|order status|order\s+#?(\d+)"],
    "EC_PRODUCT_SEARCH": [r"find|looking for|search for|under \$?\d+"],
    "EC_FAQ": [r"hours|shipping|delivery|policy|discount|promo"],
}

# When both patterns match, prefer the intent with the lower priority number.
INTENT_PRIORITY = {
    "EC_RETURN_REFUND": 1,
    "EC_ORDER_TRACK": 2,
    "EC_PRODUCT_SEARCH": 3,
    "EC_FAQ": 4,
}

SAFETY_PATTERNS = [
    (r"\bpassword\b|\bcvv\b|\bcredit card number\b|\bmy ssn\b|\bsocial security\b", "SAFETY_PII"),
    (r"\bthreat\b|\blawsuit\b|\blegal action\b", "SAFETY_ABUSE"),
]

ENTITY_PATTERNS = {
    "order_id": re.compile(r"\b#?(\d{4,})\b"),
    "date": re.compile(r"\b(today|tomorrow|next\s+\w+|\d{1,2}/\d{1,2}(?:/\d{2,4})?)\b", re.I),
    "amount": re.compile(r"\$?\d+", re.I),
}


def _score_match(match_len: int) -> float:
    return 0.85 + min(match_len / 100, 0.1)


class IntentClassifier:
    def __init__(self, use_llm: bool = True, confidence_threshold: float = 0.75):
        self.use_llm = use_llm
        self.confidence_threshold = confidence_threshold

    def classify(self, text: str) -> Tuple[str, float]:
        if self.use_llm:
            llm_result = self._llm_classify(text)
            if llm_result:
                return llm_result[0], llm_result[1]

        text_lower = text.lower()
        candidates = []
        for intent, patterns in INTENT_PATTERNS.items():
            for pat in patterns:
                match = re.search(pat, text_lower)
                if match:
                    candidates.append((intent, len(match.group(0))))

        if not candidates:
            return "UNKNOWN", 0.0

        # Pick candidate by priority first, then by match length, then by original order.
        best = min(
            candidates,
            key=lambda item: (
                INTENT_PRIORITY.get(item[0], 99),
                -item[1],
                list(INTENT_PATTERNS.keys()).index(item[0]),
            ),
        )
        return best[0], round(_score_match(best[1]), 2)

    def _llm_classify(self, text: str) -> Optional[Tuple[str, float, dict]]:
        """Use OpenAI to classify intent and extract entities. Falls back to regex."""
        if not OpenAI or not os.environ.get("OPENAI_API_KEY"):
            return None

        domain = "ecommerce"
        intent_examples = "\n".join([f"- {k}" for k in INTENT_PATTERNS.keys()])

        prompt = f"""Classify the user message for a {domain} customer support AI agent.
Return ONLY a JSON object with keys: intent, confidence (0.0-1.0), entities (object).

Allowed intents:
{intent_examples}

Message: {text}
"""
        try:
            client = OpenAI()
            resp = client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.0,
            )
            content = resp.choices[0].message.content
            if content is None:
                return None
            data = json.loads(content)
            intent = data.get("intent", "UNKNOWN")
            confidence = float(data.get("confidence", 0.0))
            if intent not in INTENT_PATTERNS and intent != "UNKNOWN":
                intent = "UNKNOWN"
            if confidence < self.confidence_threshold:
                return None
            return intent, round(min(confidence, 0.99), 2), data.get("entities", {})
        except Exception:
            return None

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
