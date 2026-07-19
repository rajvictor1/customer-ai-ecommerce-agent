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

## Production Deployment

1. Copy `.env.example` to `.env` and fill in real credentials.
2. Run with Docker:
   ```bash
   docker-compose up --build
   ```
3. Or deploy to Render / Fly.io / AWS / GCP / Azure using guides in `deploy/`.
4. Point Twilio WhatsApp webhook to `https://your-domain/api/webhook/whatsapp`.

## Production Checklist

- [ ] Replace stub auth in `app/auth.py` with real OAuth2/OIDC.
- [ ] Add `OPENAI_API_KEY` or switch to your own fine-tuned model.
- [ ] Connect `app/backend_mock.py` replacements to real OMS/EHR APIs.
- [ ] Use managed PostgreSQL instead of SQLite.
- [ ] Set strong `SECRET_KEY` and store all secrets in a vault.
- [ ] Enable HTTPS and configure CORS for known origins.
- [ ] Review HIPAA BAA (healthcare) or PCI-DSS scope (e-commerce).
