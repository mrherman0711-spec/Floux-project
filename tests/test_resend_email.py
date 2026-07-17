#!/usr/bin/env python3
"""Tests for the Resend email execution script."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class FakeResponse:
    def __init__(self, status_code: int, payload: dict) -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = str(payload)

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}: {self.text}")


class FakeClient:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.calls: list[dict] = []

    def post(self, url: str, *, headers: dict, json: dict, timeout: float) -> FakeResponse:
        self.calls.append({
            "url": url,
            "headers": headers,
            "json": json,
            "timeout": timeout,
        })
        return self.response


class ResendEmailTests(unittest.TestCase):
    def setUp(self) -> None:
        os.environ.pop("RESEND_API_KEY", None)

    def test_dry_run_returns_payload_without_network_call(self) -> None:
        from execution.send_resend_email import SendEmailRequest, send_email

        client = FakeClient(FakeResponse(200, {"id": "unused"}))
        result = send_email(
            SendEmailRequest(
                from_email="Floux <hello@floux.es>",
                to_email="lead@example.com",
                subject="Llamadas perdidas en tu salon",
                html="<p>Hola</p>",
                reply_to="max@floux.es",
                dry_run=True,
            ),
            api_key="",
            client=client,
        )

        self.assertEqual(result["status"], "dry_run")
        self.assertEqual(result["payload"]["to"], ["lead@example.com"])
        self.assertEqual(result["payload"]["reply_to"], ["max@floux.es"])
        self.assertEqual(client.calls, [])

    def test_send_uses_resend_endpoint_and_idempotency_header(self) -> None:
        from execution.send_resend_email import SendEmailRequest, send_email

        client = FakeClient(FakeResponse(200, {"id": "email_123"}))
        result = send_email(
            SendEmailRequest(
                from_email="Floux <hello@floux.es>",
                to_email="lead@example.com",
                subject="Recupera citas perdidas",
                text="Hola",
                idempotency_key="campaign-1-lead-example",
            ),
            api_key="test-api-key",
            client=client,
        )

        self.assertEqual(result["status"], "sent")
        self.assertEqual(result["response"], {"id": "email_123"})
        self.assertEqual(client.calls[0]["url"], "https://api.resend.com/emails")
        self.assertEqual(client.calls[0]["headers"]["Authorization"], "Bearer test-api-key")
        self.assertEqual(client.calls[0]["headers"]["Idempotency-Key"], "campaign-1-lead-example")
        self.assertEqual(client.calls[0]["json"]["text"], "Hola")

    def test_requires_html_or_text(self) -> None:
        from execution.send_resend_email import SendEmailRequest

        with self.assertRaises(ValueError):
            SendEmailRequest(
                from_email="Floux <hello@floux.es>",
                to_email="lead@example.com",
                subject="Hola",
            )

    def test_missing_api_key_fails_before_network_call(self) -> None:
        from execution.send_resend_email import SendEmailRequest, send_email

        client = FakeClient(FakeResponse(200, {"id": "unused"}))
        with self.assertRaises(ValueError):
            send_email(
                SendEmailRequest(
                    from_email="Floux <hello@floux.es>",
                    to_email="lead@example.com",
                    subject="Hola",
                    text="Hola",
                ),
                api_key="",
                client=client,
            )

        self.assertEqual(client.calls, [])


if __name__ == "__main__":
    unittest.main()
