from datetime import datetime, timedelta, timezone
from typing import Optional
from app.models import Customer


class MockBackend:
    def __init__(self):
        self.customers = {
            "cust_456": Customer(id="cust_456", name="Ravi Gupta", phone="+919****3211", email="ravi@example.com", domain="ecommerce"),
        }
        self.orders = {
            "cust_456": [
                {"id": "10001", "status": "Shipped", "eta": "2026-07-22", "items": ["Running Shoes"]},
                {"id": "10002", "status": "Processing", "eta": "2026-07-25", "items": ["Wireless Earbuds"]},
            ]
        }

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        return self.customers.get(customer_id)

    def track_order(self, customer_id: str, order_id: Optional[str] = None) -> str:
        orders = self.orders.get(customer_id, [])
        if not orders:
            return "I don't see any orders on your account."
        if order_id:
            for o in orders:
                if str(o["id"]) == order_id:
                    return f"Order #{o['id']} ({', '.join(o['items'])}) is **{o['status']}** — estimated delivery {o['eta']}."
            return f"I couldn't find order #{order_id}. Your recent orders: " + ", ".join([f"#{o['id']}" for o in orders])
        o = orders[0]
        return f"Your latest order #{o['id']} ({', '.join(o['items'])}) is **{o['status']}** — estimated delivery {o['eta']}."

    def create_return(self, customer_id: str, order_id: Optional[str] = None) -> str:
        if not order_id:
            return "Please provide the order number you'd like to return (e.g., #10001)."
        return f"Return request created for order #{order_id}. A pickup will be scheduled within 24 hours."

    def search_products(self, query: str) -> str:
        return f"I found 3 products matching '{query}'. Top pick: Wireless Earbuds Pro — $45, 4.5★."

    def active_promos(self) -> str:
        return "Current offers: SAVE20 (20% off orders over $50), FREESHIP on orders over $35."

    def _suggest_slot(self, date_hint: Optional[str]) -> str:
        base = datetime.now(timezone.utc) + timedelta(days=2)
        if date_hint and date_hint.lower() == "tomorrow":
            base = datetime.now(timezone.utc) + timedelta(days=1)
        return base.strftime("%Y-%m-%d at 10:00 AM")


BACKEND = MockBackend()
