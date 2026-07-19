from fastapi.testclient import TestClient
from run import app

client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_chat_order_track():
    resp = client.post("/api/chat", json={
        "message": "Where is my order #10001?",
        "customer_id": "cust_456",
        "channel": "web"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
    assert data["intent"] == "EC_ORDER_TRACK"
    assert "10001" in data["response"]


def test_chat_product_search():
    resp = client.post("/api/chat", json={
        "message": "Find wireless earbuds under $50",
        "customer_id": "cust_456",
        "channel": "web"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "EC_PRODUCT_SEARCH"
    assert "earbuds" in data["response"].lower()


def test_chat_return():
    resp = client.post("/api/chat", json={
        "message": "I want to return order #10001",
        "customer_id": "cust_456",
        "channel": "web"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "EC_RETURN_REFUND"
    assert "return request" in data["response"].lower()
