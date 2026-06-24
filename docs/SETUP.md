# Detailed Setup Guide

See main README for quick start.

## Manual Pinecone Index Creation

Use the dashboard or `setup_pinecone.py`.

## Webhook URL Registration

1. Go to Meta for Developers → Your App → WhatsApp → Configuration
2. Set Callback URL to your public HTTPS endpoint + `/webhook/`
3. Use the same verify token as in `.env`

## Production Notes

- Always use HTTPS
- Set strong secret
- Use a real database
