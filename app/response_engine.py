from typing import Dict, Any
from app.models import Conversation
from app.backend_mock import BACKEND

class ResponseEngine:
    def generate(self, conversation: Conversation, intent: str, entities: Dict[str, Any]) -> str:
        user = BACKEND.get_customer(conversation.customer_id)
        if user:
            conversation.context.setdefault("name", user.name)
            conversation.context.setdefault("domain", user.domain)

        name = conversation.context.get("name", "there")

        if intent.startswith("EC_"):
            return self._ecommerce(conversation, intent, entities, name)
        else:
            return self._fallback(conversation, name)

    def _ecommerce(self, conv: Conversation, intent: str, entities: Dict[str, Any], name: str) -> str:
        if intent == "EC_ORDER_TRACK":
            order_id = entities.get("order_id")
            return BACKEND.track_order(conv.customer_id, order_id)
        if intent == "EC_RETURN_REFUND":
            return BACKEND.create_return(conv.customer_id, entities.get("order_id"))
        if intent == "EC_PRODUCT_SEARCH":
            return BACKEND.search_products(conv.messages[-1].content)
        if intent == "EC_FAQ":
            return BACKEND.active_promos()
        return f"Hi {name}, I can help with orders, returns, product searches, and current offers. What do you need?"

    def _fallback(self, conv: Conversation, name: str) -> str:
        return f"Hi {name}, I'm your AI assistant. I can help with orders, returns, product searches, and current offers. What would you like to do?"

ENGINE = ResponseEngine()
