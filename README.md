# E-Commerce Customer-Facing AI Agent — MVP

Self-contained FastAPI MVP for e-commerce customer support: order tracking, returns/refunds, product search, promotions.

Includes e-commerce guardrails: no payment detail capture, PII redirection, and escalation paths.

## Run locally

```bash
cd /Users/mac/customer-ai-ecommerce-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn run:app --reload --port 8001
```

Open `http://localhost:8001` for chat and `http://localhost:8001/admin` for the dashboard.

Or use Docker:

```bash
docker-compose up --build
```

The app will be available at `http://localhost:8001`.

## Files

- `app/main.py` — FastAPI routes + web UI.
- `app/router.py` — conversation orchestration.
- `app/classifier.py` — intent/entity/safety classifier (EC intents only).
- `app/policy.py` — e-commerce guardrails.
- `app/response_engine.py` — response generation for e-commerce.
- `app/backend_mock.py` — mock OMS, products, promotions.
- `app/store.py` — SQLite persistence.
- `app/models.py` — Pydantic models.
- `app/auth.py` — OAuth2/OIDC stub.
- `app/whatsapp.py` — Twilio WhatsApp adapter.
- `app/config.py` — Pydantic settings.
- `app/logging.py` — structured JSON logging.
- `templates/` — Jinja2 chat + admin templates.
- `tests/` — pytest test suite.

## Supported intents

| Intent | Example |
|---|---|
| EC_ORDER_TRACK | "Where is my order #12345?" |
| EC_RETURN_REFUND | "I want to return my shoes" |
| EC_PRODUCT_SEARCH | "Find wireless earbuds under $50" |
| EC_FAQ | "Is there a discount code?" |

## Safety rules

- Never asks for or stores CVV, full card numbers, or passwords.
- Redirects payment issues to secure hosted checkout.
- Escalates abuse or legal-threat phrases to a human.

## Configuration

Copy `.env.example` to `.env` and fill in real values:

```bash
cp .env.example .env
```

## Notes

This is a local MVP. Production needs real NLU, OAuth/MFA, OMS integration, PCI-DSS compliant payment handling, and proper secrets management.

## Production Deployment

See `deploy/` for platform-specific guides (Render, Fly.io, AWS, GCP, Azure).

## Production Checklist

- [ ] Replace stub auth in `app/auth.py` with real OAuth2/OIDC.
- [ ] Add `OPENAI_API_KEY` or switch to your own fine-tuned model.
- [ ] Connect `app/backend_mock.py` replacements to real OMS/product/payment APIs.
- [ ] Use managed PostgreSQL instead of SQLite.
- [ ] Set strong `SECRET_KEY` and store all secrets in a vault.
- [ ] Enable HTTPS and configure CORS for known origins.
- [ ] Review PCI-DSS scope before handling payment data.
