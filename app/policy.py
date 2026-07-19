import re
from typing import Tuple
from app.models import Conversation, Message

class PolicyLayer:
    def apply(self, conversation: Conversation, user_text: str) -> Tuple[bool, str, str]:
        conv = conversation
        text = user_text

        # PII safety: do not process explicit sensitive data
        if re.search(r"\bmy ssn\b|\bsocial security\b|\bpassword\b|\bcvv\b|\bcredit card number\b", text, re.I):
            return True, "SAFETY_PII", "For your security, please don't share sensitive details like SSN, password, or CVV here. Contact support if needed."

        # Order tracking and returns don't require extra auth for demo customers
        user_msg = conv.messages[-1] if conv.messages else None
        if user_msg and user_msg.role == "user" and user_msg.intent in {"EC_ORDER_TRACK", "EC_RETURN_REFUND"}:
            conv.context["authenticated"] = True

        return False, "", ""
