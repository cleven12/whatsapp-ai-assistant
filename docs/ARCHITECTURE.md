# Architecture Overview

The application follows a clean request/response flow using RAG + LLM with memory.

## Message Flow Diagram

```mermaid
sequenceDiagram
    participant User as User (WhatsApp)
    participant WA as WhatsApp Cloud API
    participant Webhook as Flask Webhook Handler
    participant DB as Database (User + Messages)
    participant RAG as RAG Service
    participant LLM as LLM Router
    participant WS as WhatsApp Service

    User->>WA: Send message
    WA->>Webhook: POST /webhook
    
    Webhook->>DB: Create/Get User + Save incoming message
    Webhook->>RAG: Retrieve relevant context
    RAG->>Pinecone[(Pinecone)]: Similarity search
    Pinecone-->>RAG: Top-k chunks
    RAG-->>Webhook: Context
    
    Webhook->>LLM: Select best available LLM
    LLM-->>Webhook: LLM instance (with fallback)
    
    Webhook->>DB: Load recent history
    Webhook->>LLM: Generate response (prompt + context + history)
    LLM-->>Webhook: AI text
    
    Webhook->>DB: Persist assistant reply
    Webhook->>WS: Send reply
    WS->>WA: POST message
    WA->>User: Reply delivered
```

## Design Principles

- **Stateless web process** — All state lives in external services
- **External vector database** — Pinecone for scalable semantic search
- **SQL for conversation memory** — SQLite (dev) or Postgres (prod)
- **Resilient LLM routing** — Automatic fallback across multiple providers

## Core Files

| Component       | File                          | Responsibility                     |
|-----------------|-------------------------------|------------------------------------|
| Webhook         | `app/routes/webhook.py`       | Main orchestration & memory        |
| RAG             | `app/rag/retriever.py`        | Document retrieval from Pinecone   |
| LLM Router      | `app/llm/router.py`           | Provider selection + fallbacks     |
| WhatsApp        | `app/services/whatsapp.py`    | Sending messages via Cloud API     |
| Models          | `app/models/__init__.py`      | User & Message persistence         |
| Ingestion       | `ingest_docs.py`              | Loading documents into vector DB   |

**Note:** Advanced CRM and multi-app integration layers are part of the **paid Pro offering**. See [ROADMAP.md](../ROADMAP.md) and the Pro section in the main README.

