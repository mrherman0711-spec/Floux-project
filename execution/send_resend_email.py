#!/usr/bin/env python3
"""
Send one email through Resend.

Defaults to safe, explicit inputs. Use --dry-run before real outreach.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

RESEND_EMAILS_URL = "https://api.resend.com/emails"
DEFAULT_TIMEOUT_SECONDS = 30.0


@dataclass(frozen=True)
class SendEmailRequest:
    from_email: str
    to_email: str
    subject: str
    html: str | None = None
    text: str | None = None
    reply_to: str | None = None
    idempotency_key: str | None = None
    dry_run: bool = False

    def __post_init__(self) -> None:
        if not self.from_email.strip():
            raise ValueError("from_email is required")
        if not self.to_email.strip() or "@" not in self.to_email:
            raise ValueError("to_email must be a valid email address")
        if not self.subject.strip():
            raise ValueError("subject is required")
        if not (self.html and self.html.strip()) and not (self.text and self.text.strip()):
            raise ValueError("Provide html or text content")

    def payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "from": self.from_email,
            "to": [self.to_email],
            "subject": self.subject,
        }
        if self.html:
            payload["html"] = self.html
        if self.text:
            payload["text"] = self.text
        if self.reply_to:
            payload["reply_to"] = [self.reply_to]
        return payload


def _headers(api_key: str, idempotency_key: str | None = None) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    return headers


def send_email(
    request: SendEmailRequest,
    *,
    api_key: str | None = None,
    client: Any | None = None,
) -> dict[str, Any]:
    payload = request.payload()
    if request.dry_run:
        return {"status": "dry_run", "payload": payload}

    api_key = api_key if api_key is not None else os.getenv("RESEND_API_KEY", "")
    if not api_key:
        raise ValueError("RESEND_API_KEY is not set")

    if client is None:
        import httpx

        http_client = httpx
    else:
        http_client = client
    response = http_client.post(
        RESEND_EMAILS_URL,
        headers=_headers(api_key, request.idempotency_key),
        json=payload,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return {"status": "sent", "response": response.json()}


def _read_content(value: str | None, path: str | None) -> str | None:
    if value and path:
        raise ValueError("Use either inline content or a file path, not both")
    if path:
        return Path(path).read_text(encoding="utf-8")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one email through Resend")
    parser.add_argument("--from", dest="from_email", default=os.getenv("RESEND_FROM_EMAIL", "Floux <max@floux.es>"))
    parser.add_argument("--to", dest="to_email", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--html")
    parser.add_argument("--html-file")
    parser.add_argument("--text")
    parser.add_argument("--text-file")
    parser.add_argument("--reply-to", default=os.getenv("RESEND_REPLY_TO", "max@floux.es"))
    parser.add_argument("--idempotency-key")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        request = SendEmailRequest(
            from_email=args.from_email,
            to_email=args.to_email,
            subject=args.subject,
            html=_read_content(args.html, args.html_file),
            text=_read_content(args.text, args.text_file),
            reply_to=args.reply_to,
            idempotency_key=args.idempotency_key,
            dry_run=args.dry_run,
        )
        result = send_email(request)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
