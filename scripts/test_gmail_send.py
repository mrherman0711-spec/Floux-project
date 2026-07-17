#!/usr/bin/env python3
"""Test Gmail send using existing OAuth credentials."""

import json
import base64
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = os.path.join(os.path.dirname(__file__), '..', 'token.json')
CREDS_PATH = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')


def get_credentials():
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    with open(CREDS_PATH) as f:
        creds_data = json.load(f)['installed']

    creds = Credentials(
        token=token_data['token'],
        refresh_token=token_data['refresh_token'],
        token_uri=token_data['token_uri'],
        client_id=token_data['client_id'],
        client_secret=token_data['client_secret'],
        scopes=token_data['scopes'],
    )

    if creds.expired and creds.refresh_token:
        print("Token expired — refreshing...")
        creds.refresh(Request())
        token_data['token'] = creds.token
        token_data['expiry'] = creds.expiry.isoformat() if creds.expiry else None
        with open(TOKEN_PATH, 'w') as f:
            json.dump(token_data, f)
        print("Token refreshed and saved.")

    return creds


def send_test_email(to: str, subject: str, body_html: str):
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = to
    msg.attach(MIMEText(body_html, 'html'))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
    print(f"Email sent. Message ID: {result['id']}")
    return result


if __name__ == '__main__':
    send_test_email(
        to='mrherman0711@gmail.com',
        subject='Test Floux — Gmail API ✓',
        body_html="""
<div style="font-family: 'Inter', sans-serif; background: #1A1714; color: #F2EDE6; padding: 40px; max-width: 560px; margin: 0 auto; border-radius: 8px;">
  <h1 style="color: #9A7B4F; font-size: 24px; margin-bottom: 8px;">Floux</h1>
  <p style="font-size: 14px; color: #9A7B4F; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 24px;">Prueba de Gmail API</p>
  <p style="font-size: 16px; line-height: 1.6;">Todo funciona correctamente. El envío de emails desde <strong>max@floux.es</strong> vía OAuth2 está operativo.</p>
  <hr style="border: none; border-top: 1px solid #9A7B4F; margin: 24px 0; opacity: 0.3;">
  <p style="font-size: 12px; color: #9A7B4F;">Recuperamos los clientes que pierdes cuando no puedes coger el teléfono.</p>
  <p style="font-size: 12px;">floux.es · 97€/mes · Sin permanencia</p>
</div>
""",
    )
