from typing import Any, Optional

import httpx

from app.config import get_settings
from app.models import Customer


class EcommerceBackend:
    def __init__(self):
        self.settings = get_settings()
        self.customers = {
            "cust_456": Customer(
                id="cust_456",
                name="Ravi Gupta",
                phone="+919****3211",
                email="ravi@example.com",
                domain="ecommerce",
            ),
        }
        self.orders = {
            "cust_456": [
                {"id": "10001", "status": "Shipped", "eta": "2026-07-22", "items": ["Running Shoes"]},
                {"id": "10002", "status": "Processing", "eta": "2026-07-25", "items": ["Wireless Earbuds"]},
            ],
        }

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        if self.settings.OMS_API_BASE_URL:
            data = self._request("oms", "GET", f"/customers/{customer_id}")
            if data:
                return Customer(
                    id=str(data.get("id", customer_id)),
                    name=data.get("name"),
                    phone=data.get("phone"),
                    email=data.get("email"),
                    domain="ecommerce",
                    authenticated=bool(data.get("authenticated", False)),
                )
        return self.customers.get(customer_id)

    def track_order(self, customer_id: str, order_id: Optional[str] = None) -> str:
        orders = self._orders(customer_id)
        if not orders:
            return "I don't see any orders on your account."
        if order_id:
            for order in orders:
                if str(order.get("id")) == order_id:
                    return self._format_order(order)
            recent = ", ".join([f"#{order.get('id')}" for order in orders])
            return f"I couldn't find order #{order_id}. Your recent orders: {recent}"
        return self._format_order(orders[0], latest=True)

    def create_return(self, customer_id: str, order_id: Optional[str] = None) -> str:
        if not order_id:
            return "Please provide the order number you'd like to return (e.g., #10001)."
        if self.settings.RETURNS_API_BASE_URL:
            data = self._request(
                "returns",
                "POST",
                "/returns",
                json={"customer_id": customer_id, "order_id": order_id},
            )
            if data:
                status_text = data.get("status", "created")
                pickup = data.get("pickup_eta", "within 24 hours")
                return f"Return request {status_text} for order #{order_id}. Pickup: {pickup}."
        return f"Return request created for order #{order_id}. A pickup will be scheduled within 24 hours."

    def search_products(self, query: str) -> str:
        if self.settings.CATALOG_API_BASE_URL:
            data = self._request("catalog", "GET", "/products/search", params={"q": query})
            products = data.get("products", []) if data else []
            if products:
                top = products[0]
                name = top.get("name", "matching product")
                price = top.get("price")
                rating = top.get("rating")
                details = [name]
                if price:
                    details.append(f"${price}")
                if rating:
                    details.append(f"{rating} stars")
                return "Top product match: " + ", ".join(details) + "."
        return f"I found 3 products matching '{query}'. Top pick: Wireless Earbuds Pro - $45, 4.5 stars."

    def active_promos(self) -> str:
        if self.settings.PROMOTIONS_API_BASE_URL:
            data = self._request("promotions", "GET", "/promotions/active")
            promos = data.get("promotions", []) if data else []
            if promos:
                return "Current offers: " + ", ".join(
                    [promo.get("code", promo.get("name", "offer")) for promo in promos]
                )
        return "Current offers: SAVE20 (20% off orders over $50), FREESHIP on orders over $35."

    def _orders(self, customer_id: str) -> list[dict[str, Any]]:
        if self.settings.OMS_API_BASE_URL:
            data = self._request("oms", "GET", f"/customers/{customer_id}/orders")
            if data:
                return data.get("orders", [])
        return self.orders.get(customer_id, [])

    def _request(self, service: str, method: str, path: str, **kwargs) -> Optional[dict[str, Any]]:
        base_url, token = self._service_config(service)
        if not base_url:
            return None
        headers = kwargs.pop("headers", {})
        if token:
            headers["Authorization"] = f"Bearer {token}"
        url = base_url.rstrip("/") + path
        try:
            with httpx.Client(timeout=8.0) as client:
                response = client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError):
            return None

    def _service_config(self, service: str) -> tuple[str, str]:
        services = {
            "oms": (self.settings.OMS_API_BASE_URL, self.settings.OMS_API_TOKEN),
            "catalog": (self.settings.CATALOG_API_BASE_URL, self.settings.CATALOG_API_TOKEN),
            "returns": (self.settings.RETURNS_API_BASE_URL, self.settings.RETURNS_API_TOKEN),
            "promotions": (
                self.settings.PROMOTIONS_API_BASE_URL,
                self.settings.PROMOTIONS_API_TOKEN,
            ),
        }
        return services[service]

    def _format_order(self, order: dict[str, Any], latest: bool = False) -> str:
        items = ", ".join(order.get("items", [])) or "items"
        prefix = "Your latest order" if latest else "Order"
        return (
            f"{prefix} #{order.get('id')} ({items}) is **{order.get('status', 'unknown')}** "
            f"- estimated delivery {order.get('eta', 'pending')}."
        )


BACKEND = EcommerceBackend()
