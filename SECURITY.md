# Security Policy

## Supported Versions

We currently support the latest version on the `main` branch.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue.

Instead:

- Email: cleven.noreplay@gmail.com (or open a private security advisory on GitHub if available)
- Provide as much detail as possible (steps to reproduce, affected component)

We will respond within 48 hours and work with you to resolve the issue responsibly.

## Best Practices for Users

- Never commit your `.env` file
- Rotate WhatsApp tokens and API keys regularly
- Use strong `SECRET_KEY` in production
- Consider rate limiting and webhook signature verification (future enhancement)

Thank you for helping keep the project secure!
