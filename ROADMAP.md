# Roadmap & Feature Tiers

This document outlines the current state and future direction of the WhatsApp AI Assistant.

## Current (Free / Open Source - v0.2.x)

- WhatsApp Cloud API webhook (text messages)
- RAG over your documents with Pinecone + sentence-transformers
- Intelligent multi-LLM fallback router (Groq, Gemini, OpenAI, Claude, xAI)
- Persistent per-user conversation memory (SQLite / Postgres)
- Basic ingestion script (`ingest_docs.py`)
- Docker + docker-compose support
- Health endpoint + professional dashboard
- Basic test suite

See the [visual architecture diagram](https://github.com/cleven12/whatsapp-ai-assistant#architecture) (Mermaid sequence diagram) in the README.

## Pro / Enterprise Features (Paid)

These features are **not included** in the free open-source version. They are offered as professional services or licensed upgrades.

### Integrations
- **CRM Sync**: HubSpot, Salesforce, Pipedrive, Zoho, custom CRMs
  - Automatic contact/lead creation
  - Full conversation history logging
  - Deal stage updates triggered from WhatsApp
- **Third-party Apps**
  - Slack / Microsoft Teams notifications & commands
  - Google Sheets / Notion logging
  - Zapier, Make, n8n native support
  - Custom webhooks and REST API connectors
- Calendar booking, Stripe payments, ticketing (Zendesk, Intercom, etc.)

### Advanced Capabilities
- Full analytics dashboard + usage reports
- Multi-number support and team inboxes
- Priority email + WhatsApp support with SLA
- Custom LLM fine-tuning or private deployments
- On-premise / VPC / air-gapped options
- White-label / full rebranding
- Voice note transcription + media message support
- Advanced guardrails, PII redaction, and compliance (GDPR, HIPAA-ready)

### Support & Services
- Dedicated onboarding & knowledge base setup
- Custom development for your specific CRM or internal tools
- Hosted / managed version available

**Interested?**  
Email: clevengodsontech@gmail.com  
WhatsApp: +255 692 654 000  
Sponsor the project: https://snippe.me/pay/support-cleven

## Planned Free Improvements (Community + Maintainer)

- Better error handling and retry logic
- Support for image / document WhatsApp messages (basic)
- Improved dashboard UI (Flask templates + HTMX or simple React)
- PostgreSQL migration helpers
- More LLM providers + local models (Ollama, etc.)
- Rate limiting and abuse protection
- Docker production examples (with Traefik / Caddy)
- More comprehensive test coverage + CI

## Longer Term

- Plugin / extension system
- Multi-tenant support
- Self-hosted vector DB options (Chroma, Weaviate, Qdrant)
- Streaming responses
- Voice + video call integration (WhatsApp Business API)

---

**Note**: Pro features are developed and maintained separately to keep the open-source core lean and free for everyone.

Contributions to the free core (bug fixes, docs, new LLM providers, UI improvements) are always welcome via PRs!
