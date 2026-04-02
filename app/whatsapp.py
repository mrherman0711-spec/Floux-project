"""
WhatsApp messaging — supports both Meta Cloud API (primary) and Twilio (fallback).
"""
from __future__ import annotations

import httpx
import logging
from app.config import (
    META_ACCESS_TOKEN, META_API_BASE, WHATSAPP_PHONE_NUMBER_ID,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM,
)

log = logging.getLogger("floux.whatsapp")


def _use_meta_api() -> bool:
    """Use Meta Cloud API if configured, otherwise fall back to Twilio."""
    return bool(META_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID)


# ── Meta Cloud API ───────────────────────────────────────────

async def send_text(to: str, body: str) -> dict:
    """
    Send a WhatsApp text message.

    Args:
        to: Phone number WITHOUT '+' prefix (e.g. "34611222333")
        body: Message text (max 4096 chars)
    """
    if _use_meta_api():
        return await _meta_send_text(to, body)
    return _twilio_send_text(to, body)


async def send_template(to: str, template_name: str, language: str = "es",
                        body_params: list[str] | None = None) -> dict:
    """Send an approved template message (for outside 24h window)."""
    if not _use_meta_api():
        # Twilio doesn't support templates the same way — send as regular message
        log.warning("Template messages require Meta Cloud API. Falling back to regular message.")
        return _twilio_send_text(to, f"[Template: {template_name}]")
    return await _meta_send_template(to, template_name, language, body_params)


async def mark_as_read(message_id: str) -> None:
    """Mark a message as read (blue ticks). Meta API only."""
    if not _use_meta_api():
        return
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(
                META_API_BASE,
                headers={"Authorization": f"Bearer {META_ACCESS_TOKEN}"},
                json={
                    "messaging_product": "whatsapp",
                    "status": "read",
                    "message_id": message_id,
                },
            )
    except Exception as e:
        log.warning(f"Failed to mark as read: {e}")


async def _meta_send_text(to: str, body: str) -> dict:
    """Send text via Meta Cloud API."""
    # Strip '+' if present
    to_clean = to.lstrip("+")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                META_API_BASE,
                headers={
                    "Authorization": f"Bearer {META_ACCESS_TOKEN}",
                    "Content-Type": "application/json",
                },
                json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": to_clean,
                    "type": "text",
                    "text": {"preview_url": False, "body": body},
                },
            )
            r.raise_for_status()
            data = r.json()
            msg_id = data.get("messages", [{}])[0].get("id", "")
            return {"message_id": msg_id, "status": "sent", "provider": "meta"}
    except httpx.HTTPStatusError as e:
        log.error(f"Meta API error: {e.response.status_code} — {e.response.text}")
        return {"message_id": None, "status": "error", "error": str(e), "provider": "meta"}
    except Exception as e:
        log.error(f"Meta API exception: {e}")
        return {"message_id": None, "status": "error", "error": str(e), "provider": "meta"}


async def _meta_send_template(to: str, template_name: str, language: str,
                               body_params: list[str] | None) -> dict:
    """Send template via Meta Cloud API."""
    to_clean = to.lstrip("+")
    components = []
    if body_params:
        components.append({
            "type": "body",
            "parameters": [{"type": "text", "text": p} for p in body_params],
        })
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                META_API_BASE,
                headers={
                    "Authorization": f"Bearer {META_ACCESS_TOKEN}",
                    "Content-Type": "application/json",
                },
                json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": to_clean,
                    "type": "template",
                    "template": {
                        "name": template_name,
                        "language": {"code": language},
                        "components": components,
                    },
                },
            )
            r.raise_for_status()
            data = r.json()
            msg_id = data.get("messages", [{}])[0].get("id", "")
            return {"message_id": msg_id, "status": "sent", "provider": "meta"}
    except Exception as e:
        log.error(f"Meta template send error: {e}")
        return {"message_id": None, "status": "error", "error": str(e), "provider": "meta"}


# ── Twilio fallback ──────────────────────────────────────────

def _twilio_send_text(to: str, body: str) -> dict:
    """Send text via Twilio WhatsApp API (synchronous fallback)."""
    try:
        from twilio.rest import Client

        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            return {"message_id": None, "status": "error", "error": "Twilio credentials not set", "provider": "twilio"}

        sender = TWILIO_WHATSAPP_FROM
        if not sender:
            return {"message_id": None, "status": "error", "error": "TWILIO_WHATSAPP_FROM not set", "provider": "twilio"}

        # Ensure whatsapp: prefix
        to_wa = to if to.startswith("whatsapp:") else f"whatsapp:{to}"
        from_wa = sender if sender.startswith("whatsapp:") else f"whatsapp:{sender}"

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(body=body, from_=from_wa, to=to_wa)
        return {"message_id": msg.sid, "status": msg.status, "provider": "twilio"}

    except Exception as e:
        log.error(f"Twilio send error: {e}")
        return {"message_id": None, "status": "error", "error": str(e), "provider": "twilio"}
