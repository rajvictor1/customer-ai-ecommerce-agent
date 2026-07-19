# E-Commerce Customer-Facing AI Agent — MVP

Self-contained FastAPI MVP for e-commerce customer support: order tracking, returns/refunds, product search, promotions.

## Run

```bash
cd /Users/mac/customer-ai-ecommerce-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn run:app --reload --port 8001
```

Open `http://localhost:8001` for chat and `http://localhost:8001/admin` for the dashboard.

## Files

- `app/main.py` — FastAPI routes + web UI.
- `app/router.py` — conversation orchestration.
- `app/classifier.py` — intent/entity/safety classifier (EC intents only).
- `app/policy.py` — guardrails and authentication rules.
- `app/response_engine.py` — response generation for e-commerce.
- `app/backend_mock.py` — mock OMS, customers, promos.
- `app/store.py` — SQLite persistence.
- `app/models.py` — Pydantic models.
- `templates/` — Jinja2 chat + admin templates.
- `requirements.txt` — dependencies.

## Supported intents

| Intent | Example |
|---|---|
| EC_ORDER_TRACK | "Where is my order #10001?" |
| EC_RETURN_REFUND | "I want to return my shoes" |
| EC_PRODUCT_SEARCH | "Find wireless earbuds under $50" |
| EC_FAQ | "Do you have any discount codes?" |

## Notes

This is a local MVP. Production needs real NLU, OAuth/MFA, OMS integration, PCI-DSS compliant payment handling, and proper secrets management.
