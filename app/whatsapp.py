"""
WhatsApp messaging via Evolution API (v2).
Twilio solo maneja voz (missed-call detection) — no se usa para mensajería.
"""
from __future__ import annotations

import httpx
import logging
from app.config import EVOLUTION_BASE_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE

log = logging.getLogger("floux.whatsapp")


def _headers() -> dict:
    return {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}


async def _send_typing(to: str, state: str = "typing") -> None:
    """Send typing indicator (state: 'typing' or 'recording') to prevent ban."""
    to_clean = to.replace("whatsapp:", "").replace("+", "").strip()
    url = f"{EVOLUTION_BASE_URL}/chat/typing/{EVOLUTION_INSTANCE}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(url, headers=_headers(),
                            json={"number": to_clean, "typing": state == "typing", "recording": state == "recording"})
    except Exception as e:
        log.warning(f"Typing indicator failed: {e}")


async def send_text(to: str, body: str) -> dict:
    """Send a WhatsApp text message via Evolution API with typing indicator."""
    to_clean = to.replace("whatsapp:", "").replace("+", "").strip()

    # Send typing indicator first
    await _send_typing(to, "typing")

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


async def mark_as_read(message_id: str) -> None:
    """No-op: Evolution API gestiona el estado de lectura internamente."""
    pass
