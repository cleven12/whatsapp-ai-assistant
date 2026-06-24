# Architecture Overview

See README for diagram.

The app is intentionally simple:

- Stateless web process
- External vector DB (Pinecone)
- Local or external SQL DB for conversation state

This keeps it easy to deploy and reason about.

**Note:** Advanced CRM and multi-app integration layers are part of the paid Pro offering (contact details in README).
