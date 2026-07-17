#!/usr/bin/env python3
"""Test Resend email send."""

import os
from pathlib import Path

# Load .env manually
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip())

import resend

resend.api_key = os.environ['RESEND_API_KEY']

html_body = (
    "<div style=\"font-family: 'Inter', sans-serif; background: #1A1714; color: #F2EDE6; "
    "padding: 40px; max-width: 560px; margin: 0 auto; border-radius: 8px;\">"
    "<h1 style=\"color: #9A7B4F; font-size: 24px; margin-bottom: 8px;\">Floux</h1>"
    "<p style=\"font-size: 14px; color: #9A7B4F; letter-spacing: 0.12em; text-transform: uppercase; "
    "margin-bottom: 24px;\">Prueba de Resend API</p>"
    "<p style=\"font-size: 16px; line-height: 1.6;\">Todo funciona. Envío transaccional vía "
    "<strong>Resend</strong> desde <strong>max@floux.es</strong> operativo.</p>"
    "<hr style=\"border: none; border-top: 1px solid #9A7B4F; margin: 24px 0; opacity: 0.3;\">"
    "<p style=\"font-size: 12px; color: #9A7B4F;\">Recuperamos los clientes que pierdes cuando "
    "no puedes coger el teléfono.</p>"
    "<p style=\"font-size: 12px;\">floux.es · 97€/mes · Sin permanencia</p>"
    "</div>"
)

params = {
    "from": os.environ.get("RESEND_FROM_EMAIL", "Floux <max@floux.es>"),
    "to": ["mrherman0711@gmail.com"],
    "reply_to": os.environ.get("RESEND_REPLY_TO", "max@floux.es"),
    "subject": "Test Floux — Resend API",
    "html": html_body,
}

result = resend.Emails.send(params)
print(f"Email sent via Resend. ID: {result['id']}")
