"""
WhatsApp messaging via Evolution API (v2).
Twilio solo maneja voz (missed-call detection) — no se usa para mensajería.
"""
from __future__ import annotations

import asyncio
import httpx
import logging
from app.config import EVOLUTION_BASE_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE

log = logging.getLogger("floux.whatsapp")


def _headers() -> dict:
    return {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}


async def send_text(to: str, body: str) -> dict:
    """Send a WhatsApp text message via Evolution API."""
    to_clean = to.replace("whatsapp:", "").replace("+", "").strip()
    url = f"{EVOLUTION_BASE_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=_headers(),
                                  json={"number": to_clean, "text": body})
            r.raise_for_status()
            data = r.json()
            return {
                "message_id": data.get("key", {}).get("id", ""),
                "status": "sent",
                "provider": "evolution",
            }
    except httpx.HTTPStatusError as e:
        log.error(f"Evolution API error: {e.response.status_code} — {e.response.text}")
        return {"message_id": None, "status": "error", "error": str(e), "provider": "evolution"}
    except Exception as e:
        log.error(f"Evolution API exception: {e}")
        return {"message_id": None, "status": "error", "error": str(e), "provider": "evolution"}


async def send_template(to: str, template_name: str, language: str = "es",  # noqa: ARG001
                        body_params: list[str] | None = None) -> dict:
    """Evolution API no soporta templates Meta — enviar como texto plano."""
    text = " ".join(body_params) if body_params else template_name
    return await send_text(to, text)


async def send_with_presence(remote_jid: str, body: str) -> dict:
    """Read → wait 2s → typing indicator → send message."""
    await asyncio.sleep(2)
    await send_presence(remote_jid, "composing")
    await asyncio.sleep(1.5)
    await send_presence(remote_jid, "paused")
    return await send_text(remote_jid, body)


async def mark_as_read(remote_jid: str, message_id: str) -> None:
    """Mark a message as read (double blue tick) via Evolution API."""
    url = f"{EVOLUTION_BASE_URL}/chat/markMessageAsRead/{EVOLUTION_INSTANCE}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(url, headers=_headers(), json={
                "readMessages": [{"remoteJid": remote_jid, "id": message_id, "fromMe": False}]
            })
    except Exception as e:
        log.warning(f"mark_as_read failed: {e}")


async def send_presence(remote_jid: str, presence: str = "composing") -> None:
    """Emit a presence event (composing = typing indicator) via Evolution API."""
    url = f"{EVOLUTION_BASE_URL}/chat/sendPresence/{EVOLUTION_INSTANCE}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(url, headers=_headers(), json={
                "number": remote_jid,
                "options": {"presence": presence, "delay": 1200}
            })
    except Exception as e:
        log.warning(f"send_presence failed: {e}")
