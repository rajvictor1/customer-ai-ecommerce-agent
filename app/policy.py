import re
from typing import Tuple
from app.models import Conversation


class PolicyLayer:
    def apply(self, conversation: Conversation, user_text: str) -> Tuple[bool, str, str]:
        conv = conversation
        text = user_text

        # E-commerce guardrails
        if re.search(r"\b(cvv|credit card number|my password|full card)\b", text, re.I):
            return True, "ECOMMERCE_PII", "For your security, please don't share payment details here. Use our secure checkout or payment portal."

        # Authentication requirement for sensitive actions
        sensitive_intents = set()
        user_msg = conv.messages[-1] if conv.messages else None
        if user_msg and user_msg.role == "user" and user_msg.intent in sensitive_intents and not conv.context.get("authenticated"):
            return True, "AUTH_REQUIRED", "To proceed, I need to verify your identity. Please provide your 4-digit PIN or customer ID."

        return False, "", ""

    def looks_like_auth(self, text: str) -> bool:
        return bool(re.search(r"\b\d{4,10}\b", text))
