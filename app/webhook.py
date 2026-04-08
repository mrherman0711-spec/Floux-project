"""
Webhook handler — receives Twilio voice webhooks and Meta WhatsApp webhooks.
This is the central nervous system of Floux.
"""

import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Request, Response, Query, BackgroundTasks

from app.config import (
    WEBHOOK_VERIFY_TOKEN, TIMEZONE, BASE_DIR, load_salon_config, find_salon_by_phone,
)

# Make execution/ scripts importable
sys.path.insert(0, str(BASE_DIR / "execution"))
from app import database as db
from app import whatsapp
from app import ai_engine
from app.phone import normalize_phone

log = logging.getLogger("floux")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")

app = FastAPI(title="Floux", version="1.0.0")
TZ = ZoneInfo(TIMEZONE)


@app.on_event("startup")
async def startup():
    db.init_db()
    log.info("Floux started")


# ── Meta WhatsApp webhook verification ───────────────────────

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        log.info("Webhook verified")
        return Response(content=hub_challenge, media_type="text/plain")
    return Response(status_code=403)


# ── Meta WhatsApp incoming messages ──────────────────────────

@app.post("/webhook")
async def meta_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle incoming WhatsApp messages from Meta Cloud API."""
    body = await request.json()

    if body.get("object") != "whatsapp_business_account":
        return Response(status_code=200)

    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})

            # Handle incoming messages
            for message in value.get("messages", []):
                sender = message.get("from", "")
                msg_type = message.get("type", "")
                msg_id = message.get("id", "")

                if msg_type == "text":
                    text = message["text"]["body"]
                    background_tasks.add_task(
                        handle_whatsapp_message, f"+{sender}", text, msg_id
                    )
                elif msg_type in ("audio", "voice", "image", "video", "document", "sticker"):
                    background_tasks.add_task(
                        handle_media_message, f"+{sender}", msg_type, msg_id
                    )

            # Handle status updates (delivery receipts)
            for status in value.get("statuses", []):
                status_value = status.get("status", "")
                if status_value == "failed":
                    errors = status.get("errors", [])
                    for err in errors:
                        log.error(f"Delivery failed: {err.get('code')} — {err.get('title')}")

    return Response(status_code=200)


# ── Twilio voice webhook (missed call detection) ────────────

@app.post("/twilio/voice")
async def twilio_voice_webhook(request: Request, background_tasks: BackgroundTasks):
    """Detect missed calls via Twilio voice webhook. Respond 200 IMMEDIATELY."""
    form = await request.form()

    call_status = form.get("CallStatus", "")
    caller = form.get("From", "")
    called = form.get("To", "")
    call_sid = form.get("CallSid", "")

    log.info(f"Twilio voice: {call_status} from {caller} to {called} (SID: {call_sid})")

    # Only process missed calls
    if call_status in ("no-answer", "busy"):
        background_tasks.add_task(handle_missed_call, caller, called, call_sid)

    # ALWAYS respond with empty TwiML immediately
    return Response(
        content='<?xml version="1.0" encoding="UTF-8"?><Response/>',
        media_type="application/xml",
    )


# ── Twilio WhatsApp webhook (fallback if not using Meta API) ─

@app.post("/twilio/whatsapp")
async def twilio_whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle incoming WhatsApp via Twilio (fallback)."""
    form = await request.form()

    sender = form.get("From", "").replace("whatsapp:", "")
    body = form.get("Body", "")
    num_media = int(form.get("NumMedia", "0"))
    msg_sid = form.get("MessageSid", "")

    if num_media > 0 or not body:
        background_tasks.add_task(handle_media_message, sender, "audio", msg_sid)
    else:
        background_tasks.add_task(handle_whatsapp_message, sender, body, msg_sid)

    return Response(
        content='<?xml version="1.0" encoding="UTF-8"?><Response/>',
        media_type="application/xml",
    )


# ── Core logic ───────────────────────────────────────────────

async def handle_missed_call(caller: str, called: str, call_sid: str):
    """Process a missed call → send WhatsApp greeting."""
    try:
        # Normalize phones
        caller_normalized = normalize_phone(caller)
        called_normalized = normalize_phone(called)

        if not caller_normalized or not called_normalized:
            log.error(f"Invalid phone: caller={caller}, called={called}")
            return

        # Deduplicate by CallSid
        if db.check_duplicate_call(call_sid):
            log.info(f"Duplicate call {call_sid}, skipping")
            return

        # Find salon by Twilio number
        salon_config = find_salon_by_phone(called_normalized)
        if not salon_config:
            log.error(f"No salon found for number {called_normalized}")
            return

        salon_id = salon_config["salon_id"]
        salon_name = salon_config["salon_name"]

        # Check for existing active session
        existing = db.get_active_session(caller_normalized)
        if existing:
            log.info(f"Active session exists for {caller_normalized}, skipping greeting")
            return

        # Create client record + session
        db.get_or_create_client(caller_normalized, salon_id)
        db.create_session(caller_normalized, salon_id, call_sid)

        # Send greeting
        greeting = (
            f"Hola! 👋 Hemos visto que llamaste a {salon_name} y no pudimos atenderte.\n\n"
            f"¿En qué te puedo ayudar? Si quieres reservar una cita, dime qué servicio te interesa y cuándo te vendría bien."
        )

        result = await whatsapp.send_text(caller_normalized, greeting)
        db.log_message(caller_normalized, salon_id, "outbound", greeting, result.get("message_id", ""))

        log.info(f"Greeting sent to {caller_normalized} for {salon_name}")

    except Exception as e:
        log.error(f"Error handling missed call: {e}", exc_info=True)


async def handle_whatsapp_message(sender: str, text: str, msg_id: str):
    """Process an incoming WhatsApp text message."""
    try:
        phone = normalize_phone(sender)
        if not phone:
            log.error(f"Invalid sender phone: {sender}")
            return

        # Mark as read
        await whatsapp.mark_as_read(msg_id)

        # Load or create session
        session = db.get_active_session(phone)

        if not session:
            # Client messaged without a missed call — find their salon or use default
            client = db.get_or_create_client(phone, "ds_peluqueria")
            session = db.create_session(phone, client["salon_id"])

        salon_id = session["salon_id"]
        salon_config = load_salon_config(salon_id)
        if not salon_config:
            log.error(f"Salon config not found: {salon_id}")
            return

        # Log incoming message
        db.log_message(phone, salon_id, "inbound", text, msg_id)

        # Check if session is in a terminal state
        if session["status"] in ("booked", "escalated"):
            reply = "Tu cita ya está confirmada. Si necesitas cambiar algo, escríbenos y te ayudamos."
            result = await whatsapp.send_text(phone, reply)
            db.log_message(phone, salon_id, "outbound", reply, result.get("message_id", ""))
            return

        # Fetch availability (non-blocking, but OK to wait)
        availability = _get_availability(salon_config, session.get("booking_data", {}))

        # Run AI conversation
        conversation = session.get("conversation", [])
        ai_response = ai_engine.chat(salon_config, conversation, text, availability)

        reply = ai_response["reply"]

        # Update conversation history
        conversation.append({"role": "user", "content": text})
        conversation.append({"role": "assistant", "content": reply})

        # Route on intent
        if ai_response.get("escalate"):
            await _handle_escalation(phone, salon_config, conversation, text)
            db.update_session(session["id"], status="escalated", conversation=conversation)
        elif ai_response.get("conversation_complete"):
            await _handle_booking_complete(phone, salon_config, ai_response, conversation)
            db.update_session(session["id"], status="booked", conversation=conversation,
                            booking_data=ai_response.get("booking_data", {}))
        else:
            db.update_session(session["id"], conversation=conversation,
                            booking_data=ai_response.get("booking_data", {}))

        # Update client language if detected
        if ai_response.get("language"):
            db.update_client(phone, language=ai_response["language"])

        # Update client name if collected
        client_name = ai_response.get("booking_data", {}).get("client_name", "")
        if client_name:
            db.update_client(phone, name=client_name)

        # Send reply
        result = await whatsapp.send_text(phone, reply)
        db.log_message(phone, salon_id, "outbound", reply, result.get("message_id", ""))

        log.info(f"Reply sent to {phone}: {reply[:50]}...")

    except Exception as e:
        log.error(f"Error handling message from {sender}: {e}", exc_info=True)


async def handle_media_message(sender: str, media_type: str, msg_id: str):
    """Handle voice notes, images, etc. — ask client to type instead."""
    phone = normalize_phone(sender)
    if not phone:
        return

    await whatsapp.mark_as_read(msg_id)

    session = db.get_active_session(phone)
    salon_id = session["salon_id"] if session else "ds_peluqueria"

    if media_type in ("audio", "voice"):
        reply = "Disculpa, no puedo escuchar audios. Me lo puedes escribir?"
    elif media_type in ("image", "video"):
        reply = "Gracias por la imagen. Para poder ayudarte mejor, me puedes escribir qué necesitas?"
    else:
        reply = "Disculpa, solo puedo leer mensajes de texto. Me escribes qué necesitas?"

    result = await whatsapp.send_text(phone, reply)
    db.log_message(phone, salon_id, "outbound", reply, result.get("message_id", ""))


async def _handle_escalation(phone: str, salon_config: dict, conversation: list, last_message: str):
    """Escalate to salon owner."""
    owner_phone = salon_config.get("owner_phone", "")
    if not owner_phone:
        log.error(f"No owner phone for {salon_config.get('salon_id')}")
        return

    # Build context summary
    recent = conversation[-6:] if len(conversation) > 6 else conversation
    context = "\n".join(f"{'Cliente' if t['role'] == 'user' else 'Floux'}: {t['content']}" for t in recent)

    alert = (
        f"ESCALADO — {salon_config['salon_name']}\n\n"
        f"Cliente: {phone}\n"
        f"Último mensaje: {last_message}\n\n"
        f"Conversación reciente:\n{context}"
    )

    await whatsapp.send_text(owner_phone, alert)
    log.info(f"Escalated to owner {owner_phone}")


async def _handle_booking_complete(phone: str, salon_config: dict, ai_response: dict, conversation: list):
    """Process a completed booking."""
    bd = ai_response.get("booking_data", {})
    salon_id = salon_config["salon_id"]

    # Find service price and duration
    price = 0.0
    duration = 60
    for svc in salon_config.get("services", []):
        if svc["name"] == bd.get("service", ""):
            price = svc.get("price", 0)
            duration = svc.get("duration_min", 60)
            break

    # Calculate end time
    try:
        start = datetime.fromisoformat(bd.get("datetime", ""))
        end = start + timedelta(minutes=duration)
    except (ValueError, TypeError):
        end_str = ""
        start_str = bd.get("datetime", "")
    else:
        end_str = end.isoformat()
        start_str = start.isoformat()

    # Create appointment in DB
    appointment = db.create_appointment(
        phone=phone,
        salon_id=salon_id,
        service=bd.get("service", ""),
        staff=bd.get("staff_assigned", bd.get("staff_preference", "")),
        datetime_start=start_str,
        datetime_end=end_str,
        price=price,
        client_name=bd.get("client_name", ""),
    )

    # Update client record
    db.update_client(phone, name=bd.get("client_name", ""), next_appointment_at=start_str)

    staff_name = bd.get("staff_assigned", bd.get("staff_preference", "Sin preferencia"))

    # Create Google Calendar event
    await asyncio.to_thread(
        _create_calendar_event, salon_config, bd, start_str, end_str, staff_name, price
    )

    # Save client to Google Sheets
    await asyncio.to_thread(
        _save_to_sheet, salon_config, phone, bd, start_str, staff_name, price
    )

    # Notify owner via WhatsApp
    owner_phone = salon_config.get("owner_phone", "")
    if owner_phone:
        notification = (
            f"NUEVA CITA — {salon_config['salon_name']}\n\n"
            f"Cliente: {bd.get('client_name', phone)}\n"
            f"Tel: {phone}\n"
            f"Servicio: {bd.get('service', '')}\n"
            f"Fecha: {start_str}\n"
            f"Personal: {staff_name}\n"
            f"Precio: {price}€"
        )
        await whatsapp.send_text(owner_phone, notification)

    log.info(f"Booking created: {appointment}")


def _create_calendar_event(salon_config: dict, bd: dict, start_str: str, end_str: str,
                            staff_name: str, price: float):
    """Create a Google Calendar event for the confirmed booking."""
    try:
        from google_auth import get_google_credentials
        from googleapiclient.discovery import build

        SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
        ]
        creds = get_google_credentials(SCOPES)
        if not creds:
            log.warning("Google Calendar: no credentials, skipping event creation")
            return

        service = build("calendar", "v3", credentials=creds)
        calendar_id = salon_config.get("google_calendar_id", "primary")
        tz = salon_config.get("timezone", "Europe/Madrid")
        client_name = bd.get("client_name", "Cliente")
        svc_name = bd.get("service", "Cita")

        event = {
            "summary": f"{svc_name} — {client_name}",
            "description": (
                f"Reservado por Floux\n"
                f"Servicio: {svc_name}\n"
                f"Cliente: {client_name}\n"
                f"Personal: {staff_name}\n"
                f"Precio: {price}€"
            ),
            "start": {"dateTime": start_str, "timeZone": tz},
            "end": {"dateTime": end_str, "timeZone": tz},
            "attendees": [],
            "reminders": {"useDefault": True},
        }

        created = service.events().insert(calendarId=calendar_id, body=event).execute()
        event_url = created.get("htmlLink", "")
        log.info(f"Calendar event created: {event_url}")

        # Send email notification via Gmail
        owner_email = salon_config.get("owner_email")
        if owner_email:
            _send_booking_email(creds, owner_email, svc_name, client_name,
                                bd.get("phone", ""), start_str, staff_name, price, event_url)

    except Exception as e:
        log.error(f"Calendar event creation failed: {e}")


def _send_booking_email(creds, to_email: str, service: str, client_name: str,
                        phone: str, start_str: str, staff_name: str, price: float, event_url: str):
    """Send booking confirmation email via Gmail API."""
    import base64
    from email.mime.text import MIMEText
    from googleapiclient.discovery import build

    try:
        gmail = build("gmail", "v1", credentials=creds)

        body = (
            f"Nueva cita confirmada\n\n"
            f"Servicio: {service}\n"
            f"Cliente: {client_name}\n"
            f"Teléfono: {phone}\n"
            f"Fecha: {start_str}\n"
            f"Personal: {staff_name}\n"
            f"Precio: {price}€\n"
        )
        if event_url:
            body += f"\nVer en Calendar: {event_url}"

        msg = MIMEText(body)
        msg["to"] = to_email
        msg["subject"] = f"Nueva cita — {service} ({client_name})"
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        gmail.users().messages().send(userId="me", body={"raw": raw}).execute()
        log.info(f"Booking email sent to {to_email}")

    except Exception as e:
        log.error(f"Gmail send failed: {e}")


def _save_to_sheet(salon_config: dict, phone: str, bd: dict, start_str: str,
                   staff_name: str, price: float):
    """Save booking data to Google Sheets."""
    sheet_url = salon_config.get("google_sheet_url", "")
    if not sheet_url:
        log.info("No google_sheet_url in salon config, skipping Sheets logging")
        return

    try:
        from append_to_sheet import append_row_direct

        row = {
            "Fecha": start_str,
            "Cliente": bd.get("client_name", ""),
            "Teléfono": phone,
            "Servicio": bd.get("service", ""),
            "Personal": staff_name,
            "Precio": f"{price}€",
            "Estado": "Confirmada",
        }
        ok = append_row_direct(sheet_url, row)
        if ok:
            log.info("Booking saved to Google Sheets")
        else:
            log.warning("Failed to save booking to Google Sheets")

    except Exception as e:
        log.error(f"Google Sheets save failed: {e}")


def _get_availability(salon_config: dict, booking_data: dict) -> list[dict]:
    """Get availability slots — runs the existing execution script."""
    import subprocess
    salon_id = salon_config["salon_id"]
    service = booking_data.get("service", "")
    staff = booking_data.get("staff_preference", "")

    cmd = ["python3", "execution/check_availability.py", "--salon-id", salon_id]
    if service:
        cmd.extend(["--service", service])
    if staff:
        cmd.extend(["--staff", staff])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, cwd=str(BASE_DIR))
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("slots", [])
    except Exception as e:
        log.warning(f"Availability check failed: {e}")

    return []


# ── Health check ─────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now(TZ).isoformat()}
