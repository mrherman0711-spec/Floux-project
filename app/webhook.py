"""
Webhook handler — receives Twilio voice webhooks and Meta WhatsApp webhooks.
This is the central nervous system of Floux.
"""

import asyncio
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
from app.scheduler import get_scheduler, send_abandonment_followup

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
    """Detect missed calls via Twilio voice webhook. Respond 200 IMMEDIATELY.

    With call forwarding: the mobile forwards to Twilio, so Twilio receives
    the call as "ringing"/"in-progress" — never "no-answer". We treat any
    incoming call to our number as a missed call and trigger WhatsApp recovery.
    """
    form = await request.form()

    call_status = form.get("CallStatus", "")
    caller = form.get("From", "")
    called = form.get("To", "")
    call_sid = form.get("CallSid", "")
    direction = form.get("Direction", "")

    log.info(f"Twilio voice: {call_status} dir={direction} from {caller} to {called} (SID: {call_sid})")

    # Trigger WhatsApp on any inbound call — the mobile forwarding already
    # means the salon couldn't answer. Skip outbound legs.
    if direction != "outbound-dial" and call_status in ("ringing", "in-progress", "no-answer", "busy"):
        background_tasks.add_task(handle_missed_call, caller, called, call_sid)

    # ALWAYS respond with empty TwiML immediately — hangs up cleanly
    return Response(
        content='<?xml version="1.0" encoding="UTF-8"?><Response/>',
        media_type="application/xml",
    )


# ── Evolution API WhatsApp webhook (new number) ───────────────

@app.post("/webhook/evolution")
async def evolution_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle incoming WhatsApp messages from Evolution API."""
    body = await request.json()

    # Evolution API payload: {"event": "messages.upsert", "instance": "floux_salon_1", "data": {"key": {"remoteJid": "+34..."}, "message": {"conversation": "hola"}}}
    event = body.get("event", "")
    if event != "messages.upsert":
        return Response(status_code=200)

    try:
        data = body.get("data", {})
        key = data.get("key", {})
        message = data.get("message", {})

        remote_jid = key.get("remoteJid", "")  # "+34XXXXXXXXX@s.whatsapp.net"
        from_me = key.get("fromMe", False)

        if from_me:  # Ignore our own messages
            return Response(status_code=200)

        # Extract phone and text
        if "@" in remote_jid:
            phone = remote_jid.split("@")[0]
        else:
            phone = remote_jid

        text = message.get("conversation", "")
        msg_id = key.get("id", "")

        if text:
            background_tasks.add_task(handle_whatsapp_message, f"+{phone}", text, msg_id, remote_jid)

    except Exception as e:
        log.error(f"Evolution webhook error: {e}", exc_info=True)

    return Response(status_code=200)


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


async def handle_whatsapp_message(sender: str, text: str, msg_id: str, remote_jid: str = ""):
    """Process an incoming WhatsApp text message."""
    try:
        phone = normalize_phone(sender)
        if not phone:
            log.error(f"Invalid sender phone: {sender}")
            return

        # Mark as read (double blue tick) — requires remote_jid for Evolution API
        jid = remote_jid or f"{phone.lstrip('+')}@s.whatsapp.net"
        await whatsapp.mark_as_read(jid, msg_id)

        # Cancel any pending abandonment follow-up — client is back
        _cancel_followup_job(phone)

        # Load or create session
        session = db.get_active_session(phone)

        if not session:
            # Client messaged without a missed call — find their salon or use default
            client = db.get_or_create_client(phone, "escultor_peluqueria")
            session = db.create_session(phone, client["salon_id"])

        salon_id = session["salon_id"]
        salon_config = load_salon_config(salon_id)
        if not salon_config:
            log.error(f"Salon config not found: {salon_id}")
            return

        # Log incoming message
        db.log_message(phone, salon_id, "inbound", text, msg_id)

        # If session is booked, reopen it so the client can ask follow-up questions
        # (e.g. "¿a qué hora era?", "¿puedo cambiarla?") with full context.
        # Track this so we don't trigger a duplicate booking from post-booking messages.
        was_booked = session["status"] == "booked"
        if was_booked:
            db.update_session(session["id"], status="active")
            session["status"] = "active"

        # Also check if the client has a confirmed appointment in DB (future OR recent past)
        # e.g. session expired but they booked in a previous session, or appointment is today.
        # Pre-fill booking_data so cancellation confirmation shows real service+date.
        db_appointment_bd: dict = {}
        if not was_booked:
            conn_tmp = db.get_db()
            appt_row = conn_tmp.execute(
                "SELECT * FROM appointments WHERE phone = ? AND salon_id = ? AND status = 'confirmed' ORDER BY datetime_start DESC LIMIT 1",
                (phone, salon_id),
            ).fetchone()
            conn_tmp.close()
            if appt_row:
                appt = dict(appt_row)
                was_booked = True
                db_appointment_bd = {
                    "service": appt.get("service", ""),
                    "datetime": appt.get("datetime_start", ""),
                    "client_name": appt.get("client_name", ""),
                    "staff_assigned": appt.get("staff", ""),
                }

        # Merge saved booking_data — never overwrite existing fields with empty values
        # If we detected a DB appointment (session expired), seed current_bd from it.
        saved_bd = session.get("booking_data") or {}
        current_bd = dict(db_appointment_bd)  # start from DB appointment if any
        for k, v in saved_bd.items():
            if v:  # session data wins over DB if non-empty
                current_bd[k] = v
        if not current_bd.get("service"):
            catalog = salon_config.get("services", [])
            matches = ai_engine.find_matching_services(catalog, text)
            if len(matches) == 1:
                current_bd["service"] = matches[0]["name"]
            elif len(matches) > 1:
                log.info(f"[service] AMBIGUOUS — {len(matches)} matches for text, leaving blank for AI to disambiguate")

        # Only fetch availability once we know the service — saves ~1-2s per message
        conversation_so_far = session.get("conversation", [])
        needs_availability = bool(current_bd.get("service")) or len(conversation_so_far) >= 2
        if needs_availability:
            availability = _get_availability(salon_config, current_bd)
        else:
            # Service not yet known — pass empty list (not None) so the AI focuses on
            # asking about the service rather than seeing "sistema no disponible".
            availability = []

        # Run AI conversation
        conversation = conversation_so_far

        # When re-entering a booked session, prepend a context note to the user message
        # so the AI knows the appointment is already confirmed and doesn't ask for info again.
        # We don't save this note to conversation history — it's a one-turn hint only.
        ai_user_message = text
        if was_booked and current_bd.get("service") and current_bd.get("datetime"):
            staff = current_bd.get("staff_assigned") or current_bd.get("staff_preference") or ""
            ai_user_message = (
                f"[Sistema: cita ya confirmada — {current_bd.get('service')} "
                f"el {current_bd.get('datetime')}"
                f"{' con ' + staff if staff else ''}. "
                f"No vuelvas a pedir datos ni marques conversation_complete. "
                f"Responde solo la pregunta del cliente.]\n\n"
                f"{text}"
            )

        ai_response = ai_engine.chat(salon_config, conversation, ai_user_message, availability)

        reply = ai_response["reply"]

        # Update conversation history
        conversation.append({"role": "user", "content": text})
        conversation.append({"role": "assistant", "content": reply})

        # Merge AI booking_data with saved — never lose previously collected fields
        new_bd = ai_response.get("booking_data", {})
        merged_bd = dict(current_bd)
        for k, v in new_bd.items():
            if v:  # only overwrite if AI returned a non-empty value
                merged_bd[k] = v

        # Route on intent
        log.info(f"[ai] complete={ai_response.get('conversation_complete')} escalate={ai_response.get('escalate')} cancellation={ai_response.get('cancellation_confirmed')} was_booked={was_booked} bd={ai_response.get('booking_data')}")
        if ai_response.get("escalate"):
            await _handle_escalation(phone, salon_config, conversation, text)
            db.update_session(session["id"], status="escalated", conversation=conversation,
                            booking_data=merged_bd)
        elif ai_response.get("cancellation_confirmed") and was_booked:
            # Guard: only allow cancellation if the bot's previous message asked
            # for explicit confirmation (contains "cancelar"/"cancel") AND the
            # client's reply is a short affirmation — prevents accidental cancel
            # from post-booking thank-you/closing messages.
            prev_bot_msg = ""
            for turn in reversed(conversation_so_far):
                if turn["role"] == "assistant":
                    prev_bot_msg = turn["content"].lower()
                    break
            user_msg_lower = text.lower().strip()
            bot_asked_to_cancel = any(w in prev_bot_msg for w in ["cancelar", "cancel", "cancela"])
            user_said_affirm = any(
                user_msg_lower.startswith(w) or user_msg_lower == w
                for w in ["sí", "si", "yes", "ok", "okay", "dale", "venga",
                          "claro", "exacto", "confirmo", "confirm"]
            ) or any(w in user_msg_lower for w in ["sí cancela", "si cancela",
                                                    "confirmo cancel", "cancela",
                                                    "cancel it", "confirm cancel"])

            if not (bot_asked_to_cancel and user_said_affirm):
                log.warning(
                    f"[cancellation] BLOCKED — GPT hallucinated cancellation_confirmed. "
                    f"bot_asked={bot_asked_to_cancel} user_affirm={user_said_affirm} "
                    f"prev_bot='{prev_bot_msg[:80]}' user='{user_msg_lower[:80]}'"
                )
                db.update_session(session["id"], conversation=conversation,
                                booking_data=merged_bd)
            else:
                # Client confirmed cancellation of an existing appointment
                ai_response["booking_data"] = merged_bd
                try:
                    await _handle_cancellation(phone, salon_config, ai_response)
                except Exception as e:
                    log.error(f"[cancellation] _handle_cancellation failed: {e}", exc_info=True)
                db.update_session(session["id"], status="cancelled", conversation=conversation,
                                booking_data=merged_bd)
        elif ai_response.get("conversation_complete") and not was_booked:
            # Only process a new booking if this session wasn't already booked.
            # was_booked=True means the client sent a follow-up message after booking
            # (e.g. asking for the time again) — don't create a duplicate appointment.
            ai_response["booking_data"] = merged_bd
            log.info(f"[booking] conversation_complete=true, booking_data={merged_bd}")
            try:
                await _handle_booking_complete(phone, salon_config, ai_response, conversation)
            except Exception as e:
                log.error(f"[booking] _handle_booking_complete failed: {e}", exc_info=True)
            db.update_session(session["id"], status="booked", conversation=conversation,
                            booking_data=merged_bd)
        elif ai_response.get("conversation_complete") and was_booked:
            log.info(f"[booking] conversation_complete suppressed — session was already booked (follow-up message)")
        else:
            db.update_session(session["id"], conversation=conversation,
                            booking_data=merged_bd)
            # Schedule abandonment follow-up (replaces any previous pending job)
            _schedule_followup(phone, session["id"], salon_config, merged_bd)

        # Update client language if detected
        if ai_response.get("language"):
            db.update_client(phone, language=ai_response["language"])

        # Update client name and email if collected
        client_name = merged_bd.get("client_name", "")
        if client_name:
            db.update_client(phone, name=client_name)

        client_email = merged_bd.get("client_email", "")
        if client_email and "@" in client_email:
            db.update_client(phone, email=client_email)
            # If the session was already booked and the client just provided/corrected
            # their email, send the confirmation email now (it was skipped at booking time).
            if was_booked:
                existing_appt = None
                try:
                    conn_tmp = db.get_db()
                    existing_appt = conn_tmp.execute(
                        "SELECT * FROM appointments WHERE phone = ? AND salon_id = ? AND status = 'confirmed' ORDER BY datetime_start ASC LIMIT 1",
                        (phone, salon_id),
                    ).fetchone()
                    conn_tmp.close()
                except Exception:
                    pass
                if existing_appt:
                    appt = dict(existing_appt)
                    await asyncio.to_thread(
                        _send_client_confirmation_email,
                        salon_config, client_email,
                        {"service": appt["service"], "client_name": appt["client_name"],
                         "client_email": client_email},
                        appt["datetime_start"], appt["staff"], appt["price"],
                    )
                    log.info(f"[booking] Resent confirmation email to {client_email} (post-booking email update)")

        # Send reply with presence simulation (read → 2s wait → typing → send)
        result = await whatsapp.send_with_presence(jid, reply)
        db.log_message(phone, salon_id, "outbound", reply, result.get("message_id", ""))

        log.info(f"Reply sent to {phone}: {reply[:50]}...")

    except Exception as e:
        log.error(f"Error handling message from {sender}: {e}", exc_info=True)


async def handle_media_message(sender: str, media_type: str, msg_id: str, remote_jid: str = ""):
    """Handle voice notes, images, etc. — ask client to type instead."""
    phone = normalize_phone(sender)
    if not phone:
        return

    jid = remote_jid or f"{phone.lstrip('+')}@s.whatsapp.net"
    await whatsapp.mark_as_read(jid, msg_id)

    session = db.get_active_session(phone)
    salon_id = session["salon_id"] if session else "escultor_peluqueria"

    if media_type in ("audio", "voice"):
        reply = "Disculpa, no puedo escuchar audios. Me lo puedes escribir?"
    elif media_type in ("image", "video"):
        reply = "Gracias por la imagen. Para poder ayudarte mejor, me puedes escribir qué necesitas?"
    else:
        reply = "Disculpa, solo puedo leer mensajes de texto. Me escribes qué necesitas?"

    result = await whatsapp.send_with_presence(jid, reply)
    db.log_message(phone, salon_id, "outbound", reply, result.get("message_id", ""))



def _cancel_followup_job(phone: str) -> None:
    """Cancel any pending abandonment follow-up for this phone."""
    scheduler = get_scheduler()
    if not scheduler:
        return
    try:
        scheduler.remove_job(f"followup_{phone}")
        log.info(f"[followup] Cancelled pending job for {phone}")
    except Exception:
        pass


def _schedule_followup(phone: str, session_id: int,
                       salon_config: dict, booking_data: dict) -> None:
    """Schedule a one-shot abandonment follow-up 5 minutes from now."""
    scheduler = get_scheduler()
    if not scheduler:
        log.warning("[followup] Scheduler not running — cannot schedule follow-up")
        return

    job_id = f"followup_{phone}"

    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass

    run_at = datetime.now(TZ) + timedelta(minutes=5)
    scheduler.add_job(
        send_abandonment_followup,
        trigger="date",
        run_date=run_at,
        id=job_id,
        kwargs={
            "phone": phone,
            "session_id": session_id,
            "salon_config": salon_config,
            "booking_data": booking_data,
        },
        replace_existing=True,
    )
    log.info(f"[followup] Scheduled for {phone} at {run_at.isoformat()}")


async def _handle_escalation(phone: str, salon_config: dict, _conversation: list, last_message: str):
    """Escalate to salon owner — short message, just what they need to act."""
    owner_phone = salon_config.get("owner_phone", "")
    if not owner_phone:
        log.error(f"No owner phone for {salon_config.get('salon_id')}")
        return

    alert = (
        f"Atención — cliente necesita ayuda\n"
        f"Tel: {phone}\n"
        f"Dice: {last_message[:120]}"
    )

    await whatsapp.send_text(owner_phone, alert)
    log.info(f"Escalated to owner {owner_phone}")


async def _handle_booking_complete(phone: str, salon_config: dict, ai_response: dict, _conversation: list):
    """Process a completed booking."""
    bd = ai_response.get("booking_data", {})
    salon_id = salon_config["salon_id"]

    # Guard: never create a booking with missing required fields
    if not bd.get("service") or not bd.get("datetime") or not bd.get("client_name"):
        log.error(
            f"[booking] BLOCKED — missing required fields: "
            f"service='{bd.get('service', '')}' datetime='{bd.get('datetime', '')}' "
            f"client_name='{bd.get('client_name', '')}'"
        )
        return

    # Normalize service name to exact catalog match — BLOCK if ambiguous
    catalog_services = salon_config.get("services", [])
    matches = ai_engine.find_matching_services(catalog_services, bd.get("service", ""))
    if len(matches) == 0:
        log.error(f"[booking] BLOCKED — service '{bd.get('service')}' not found in catalog")
        return
    if len(matches) > 1:
        names = [m["name"] for m in matches]
        log.error(f"[booking] BLOCKED — AMBIGUOUS SERVICE '{bd.get('service')}' matches {names}. Bot must disambiguate before booking.")
        return
    matched_service = matches[0]["name"]
    if matched_service != bd.get("service"):
        log.info(f"[booking] service normalized: '{bd.get('service')}' → '{matched_service}'")
        bd["service"] = matched_service

    # Find service price and duration — case-insensitive match
    price = 0.0
    duration = 60
    service_name_lower = bd.get("service", "").lower().strip()
    for svc in salon_config.get("services", []):
        if svc["name"].lower().strip() == service_name_lower:
            price = svc.get("price", 0)
            duration = svc.get("duration_min", 60)
            break

    # Calculate end time
    try:
        start = datetime.fromisoformat(bd.get("datetime", ""))
        end = start + timedelta(minutes=duration)
    except (ValueError, TypeError):
        log.error(f"[booking] datetime not ISO format: '{bd.get('datetime', '')}' — using empty strings to avoid corrupted review triggers")
        end_str = "0000-00-00T00:00:00"
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

    # Create Google Calendar event and save the event_id to DB for later cancellation
    event_id = await asyncio.to_thread(
        _create_calendar_event, salon_config, bd, start_str, end_str, staff_name, price
    )
    if event_id and appointment:
        try:
            conn_ref = db.get_db()
            conn_ref.execute("UPDATE appointments SET reference = ? WHERE id = ?",
                             (event_id, appointment["id"]))
            conn_ref.commit()
            conn_ref.close()
            log.info(f"[booking] Calendar event_id {event_id} saved to appointment {appointment['id']}")
        except Exception as e:
            log.error(f"[booking] Failed to save event_id to DB: {e}")

    # Save client to Google Sheets
    await asyncio.to_thread(
        _save_to_sheet, salon_config, phone, bd, start_str, staff_name, price
    )

    # Notify owner via WhatsApp
    owner_phone = salon_config.get("owner_phone", "")
    if owner_phone:
        notification = (
            f"Nueva cita confirmada\n\n"
            f"Cliente: {bd.get('client_name', phone)}\n"
            f"Tel: {phone}\n"
            f"Servicio: {bd.get('service', '')}\n"
            f"Fecha: {start_str}\n"
            f"Precio: {price}€"
        )
        await whatsapp.send_text(owner_phone, notification)

    # Send confirmation email to client if email was collected
    # Prefer email from booking_data; fall back to stored client record
    client_email = bd.get("client_email", "")
    if not client_email or "@" not in client_email:
        client_record = db.get_or_create_client(phone, salon_id)
        client_email = client_record.get("email", "")
        if client_email:
            log.info(f"[booking] client_email not in booking_data, using stored email: {client_email}")
    log.info(f"[booking] client_email='{client_email}' bd_keys={list(bd.keys())}")
    if client_email and "@" in client_email:
        await asyncio.to_thread(
            _send_client_confirmation_email,
            salon_config, client_email, bd, start_str, staff_name, price,
        )
    else:
        log.warning(f"[booking] No client email found — confirmation email not sent for {phone}")

    log.info(f"Booking created: {appointment}")


async def _handle_cancellation(phone: str, salon_config: dict, ai_response: dict):
    """Cancel an existing appointment end-to-end: DB + Calendar + Sheets + emails
    (owner + client) + WhatsApp notifications. Each step is isolated so one
    failure doesn't block the rest. Logs a per-step summary at the end."""
    bd = ai_response.get("booking_data", {})
    salon_id = salon_config["salon_id"]

    log.info(f"[cancel] START phone={phone} salon={salon_id}")

    # Find the confirmed appointment for this phone
    conn = db.get_db()
    row = conn.execute(
        "SELECT * FROM appointments WHERE phone = ? AND salon_id = ? AND status = 'confirmed' ORDER BY datetime_start ASC LIMIT 1",
        (phone, salon_id),
    ).fetchone()
    conn.close()

    if not row:
        log.warning(f"[cancel] No confirmed appointment found for {phone} — aborting")
        return

    appt = dict(row)
    appt_id = appt["id"]
    service = appt.get("service", bd.get("service", ""))
    start_str = appt.get("datetime_start", "")
    staff_name = appt.get("staff", "")
    client_name = appt.get("client_name", bd.get("client_name", phone))
    reference = appt.get("reference", "")

    # Lookup client email upfront (for cancellation email)
    client_email = ""
    try:
        client_record = db.get_or_create_client(phone, salon_id)
        client_email = client_record.get("email", "") or ""
    except Exception as e:
        log.error(f"[cancel] Could not load client email: {e}")

    log.info(f"[cancel] appt={appt_id} service='{service}' start={start_str} staff={staff_name} email={client_email} reference={reference}")

    results = {"db": False, "cal": False, "sheet": False,
               "mail_client": False, "wa_owner": False, "wa_client": False}

    # 1. Mark cancelled in DB
    try:
        db.cancel_appointment(appt_id)
        results["db"] = True
        log.info(f"[cancel] step1 DB: appointment {appt_id} marked cancelled")
    except Exception as e:
        log.error(f"[cancel] step1 DB FAILED: {e}", exc_info=True)

    # 2. Delete / cancel Google Calendar event
    try:
        ok = await asyncio.to_thread(
            _cancel_calendar_event, salon_config, reference, appt
        )
        results["cal"] = bool(ok)
        log.info(f"[cancel] step2 Calendar: ok={results['cal']}")
    except Exception as e:
        log.error(f"[cancel] step2 Calendar FAILED: {e}", exc_info=True)

    # 3. Update Sheets row status to Cancelada (red)
    try:
        ok = await asyncio.to_thread(
            _update_sheet_cancellation, salon_config, phone, start_str
        )
        results["sheet"] = bool(ok)
        log.info(f"[cancel] step3 Sheets: ok={results['sheet']}")
    except Exception as e:
        log.error(f"[cancel] step3 Sheets FAILED: {e}", exc_info=True)

    # 4. Send cancellation email to client via Gmail (if email known)
    if client_email and "@" in client_email:
        try:
            ok = await asyncio.to_thread(
                _send_client_cancellation_email, salon_config, client_email,
                service, client_name, start_str, staff_name,
            )
            results["mail_client"] = bool(ok)
            log.info(f"[cancel] step5 Mail client: ok={results['mail_client']}")
        except Exception as e:
            log.error(f"[cancel] step5 Mail client FAILED: {e}", exc_info=True)
    else:
        log.info(f"[cancel] step5 Mail client skipped — no email on file")

    # 6. Notify owner via WhatsApp
    owner_phone = salon_config.get("owner_phone", "")
    if owner_phone:
        try:
            notification = (
                f"Cita cancelada\n\n"
                f"Cliente: {client_name}\n"
                f"Tel: {phone}\n"
                f"Servicio: {service}\n"
                f"Fecha: {start_str}"
            )
            await whatsapp.send_text(owner_phone, notification)
            results["wa_owner"] = True
        except Exception as e:
            log.error(f"[cancel] step6 WhatsApp owner FAILED: {e}", exc_info=True)

    # 7. Confirm cancellation to client via WhatsApp
    try:
        # Format date nicely for the message
        fecha_legible = start_str
        try:
            dt_obj = datetime.fromisoformat(start_str)
            day_names = {0:"lunes",1:"martes",2:"miércoles",3:"jueves",4:"viernes",5:"sábado",6:"domingo"}
            month_names = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",
                           7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
            fecha_legible = f"{day_names[dt_obj.weekday()]} {dt_obj.day} de {month_names[dt_obj.month]} a las {dt_obj.strftime('%H:%M')}"
        except Exception:
            pass

        client_msg = (
            f"Listo, tu cita de {service} del {fecha_legible} ha sido cancelada. "
            f"Si quieres reservar otra, escríbenos cuando quieras. ¡Te esperamos!"
        )
        await whatsapp.send_text(phone, client_msg)
        results["wa_client"] = True
    except Exception as e:
        log.error(f"[cancel] step7 WhatsApp client FAILED: {e}", exc_info=True)

    log.info(
        f"[cancel] DONE db={results['db']} cal={results['cal']} "
        f"sheet={results['sheet']} mail_owner={results['mail_owner']} "
        f"mail_client={results['mail_client']} wa_owner={results['wa_owner']} "
        f"wa_client={results['wa_client']}"
    )


def _cancel_calendar_event(salon_config: dict, event_reference: str,
                           appt: dict | None = None) -> bool:
    """Delete the Google Calendar event. Uses event_reference (id) if available,
    falls back to searching by title+date when reference is missing.
    Returns True on successful deletion, False otherwise."""
    try:
        from google_auth import get_google_credentials
        from googleapiclient.discovery import build

        ALL_SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = get_google_credentials(ALL_SCOPES)
        if not creds:
            log.warning("[cancel] Calendar: no credentials")
            return False

        cal = build("calendar", "v3", credentials=creds)
        calendar_id = salon_config.get("google_calendar_id", "primary")

        # Fast path: delete by known event id
        if event_reference:
            try:
                cal.events().delete(calendarId=calendar_id, eventId=event_reference).execute()
                log.info(f"[cancel] Calendar event {event_reference} deleted by id")
                return True
            except Exception as e:
                log.warning(f"[cancel] Calendar delete-by-id failed ({e}); trying search fallback")

        # Fallback: search by appointment date and match by title
        if not appt:
            log.warning("[cancel] Calendar: no reference and no appt — cannot search")
            return False

        start_str = appt.get("datetime_start", "")
        client_name = appt.get("client_name", "") or ""
        service_name = appt.get("service", "") or ""
        if not start_str:
            log.warning("[cancel] Calendar: appt has no datetime_start")
            return False

        try:
            from datetime import datetime as _dt, timedelta as _td
            dt = _dt.fromisoformat(start_str)
            time_min = (dt - _td(minutes=5)).isoformat()
            time_max = (dt + _td(minutes=5)).isoformat()
        except Exception:
            log.warning(f"[cancel] Calendar: cannot parse datetime {start_str}")
            return False

        results = cal.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
        ).execute()

        events = results.get("items", [])
        log.info(f"[cancel] Calendar search: {len(events)} events in range [{time_min}, {time_max}]")

        # Preferred format (see _create_calendar_event): "{service} — {client_name}"
        expected_summary = f"{service_name} — {client_name}".lower().strip()
        matched_id = None
        for ev in events:
            summary = (ev.get("summary", "") or "").lower().strip()
            if summary == expected_summary:
                matched_id = ev["id"]
                break
        if not matched_id:
            # Weaker match: summary contains client_name (unique enough)
            for ev in events:
                summary = (ev.get("summary", "") or "").lower()
                if client_name and client_name.lower() in summary:
                    matched_id = ev["id"]
                    break
        if not matched_id and len(events) == 1:
            # Single event at this exact time slot → assume it's ours
            matched_id = events[0]["id"]

        if matched_id:
            cal.events().delete(calendarId=calendar_id, eventId=matched_id).execute()
            log.info(f"[cancel] Calendar event {matched_id} deleted via search fallback")
            # Persist the event_id back to DB so future operations are faster
            try:
                conn = db.get_db()
                conn.execute("UPDATE appointments SET reference = ? WHERE id = ?",
                             (matched_id, appt.get("id")))
                conn.commit()
                conn.close()
            except Exception as e:
                log.warning(f"[cancel] Could not persist found event_id: {e}")
            return True

        log.warning(f"[cancel] Calendar: no event matched for {start_str} / {client_name}")
        return False

    except Exception as e:
        log.error(f"[cancel] Calendar deletion failed: {e}", exc_info=True)
        return False


def _normalize_phone_for_sheet(p: str) -> str:
    """Strip common prefixes/whitespace so phone comparison is reliable."""
    if not p:
        return ""
    return p.replace("whatsapp:", "").replace(" ", "").replace("-", "").strip()


def _update_sheet_cancellation(salon_config: dict, phone: str, datetime_start: str) -> bool:
    """Find the row matching this phone and set Estado = Cancelada with red background.
    Returns True on success, False otherwise.

    Matching strategy (3-tier fallback):
    1. phone + date-prefix match (best)
    2. phone only, most recent "Confirmada" row
    3. phone only, last row
    """
    sheet_url = salon_config.get("google_sheet_url", "")
    if not sheet_url:
        log.warning("[cancel] Sheets: no google_sheet_url in config")
        return False

    try:
        import sys as _sys
        _sys.path.insert(0, str(BASE_DIR / "execution"))
        from google_auth import get_google_credentials
        import gspread
        from gspread.utils import rowcol_to_a1

        ALL_SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = get_google_credentials(ALL_SCOPES)
        if not creds:
            log.warning("[cancel] Sheets: no credentials")
            return False

        gc = gspread.authorize(creds)
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        spreadsheet = gc.open_by_key(sheet_id)
        ws = spreadsheet.sheet1

        all_values = ws.get_all_values()
        if not all_values or len(all_values) < 2:
            log.warning(f"[cancel] Sheets: empty or header-only ({len(all_values)} rows)")
            return False

        headers = all_values[0]
        try:
            phone_col = headers.index("Telefono")
            estado_col = headers.index("Estado")
        except ValueError:
            log.warning(f"[cancel] Sheets headers missing — got {headers}")
            return False

        fecha_col = headers.index("Fecha") if "Fecha" in headers else -1
        date_prefix = datetime_start[:10] if datetime_start else ""
        phone_norm = _normalize_phone_for_sheet(phone)

        # Collect all phone-matching rows (reverse so we scan newest first)
        candidates = []  # list of (row_index, estado_value, fecha_value)
        for i, row in enumerate(all_values[1:], start=2):
            row_phone = row[phone_col] if phone_col < len(row) else ""
            if _normalize_phone_for_sheet(row_phone) != phone_norm:
                continue
            row_estado = row[estado_col] if estado_col < len(row) else ""
            row_fecha = row[fecha_col] if fecha_col >= 0 and fecha_col < len(row) else ""
            candidates.append((i, row_estado, row_fecha))

        log.info(f"[cancel] Sheets: {len(candidates)} rows match phone {phone_norm}")
        if not candidates:
            return False

        # Tier 1: phone + date-prefix, status still Confirmada
        target_row = None
        for idx, estado, fecha in reversed(candidates):
            if date_prefix and fecha.startswith(date_prefix) and estado.strip().lower() == "confirmada":
                target_row = idx
                break
        # Tier 2: phone + status Confirmada (most recent)
        if not target_row:
            for idx, estado, _ in reversed(candidates):
                if estado.strip().lower() == "confirmada":
                    target_row = idx
                    break
        # Tier 3: last phone-matching row
        if not target_row:
            target_row = candidates[-1][0]
            log.info(f"[cancel] Sheets: tier-3 fallback → last row ({target_row})")

        # Update Estado column — gspread v6+ requires values=[[...]] kwarg form
        estado_cell = rowcol_to_a1(target_row, estado_col + 1)
        ws.update(range_name=estado_cell, values=[["Cancelada"]])

        # Apply red background to entire row
        num_cols = len(headers) or 7
        last_col_letter = chr(ord("A") + num_cols - 1)
        ws.format(
            f"A{target_row}:{last_col_letter}{target_row}",
            {"backgroundColor": {"red": 0.96, "green": 0.80, "blue": 0.80}},
        )
        log.info(f"[cancel] Sheets row {target_row} → Cancelada (red)")
        return True

    except Exception as e:
        log.error(f"[cancel] Sheets update failed: {e}", exc_info=True)
        return False


def _send_cancellation_email(salon_config: dict, service: str, client_name: str,
                              start_str: str, staff_name: str, price: float) -> bool:
    """Send HTML cancellation notification email to the salon owner via Gmail.
    Returns True on success, False otherwise."""
    import base64
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import sys as _sys
    _sys.path.insert(0, str(BASE_DIR / "execution"))
    from google_auth import get_google_credentials
    from googleapiclient.discovery import build

    owner_email = salon_config.get("owner_email", "")
    if not owner_email:
        log.warning("[cancel] Mail owner: no owner_email in config")
        return False

    try:
        ALL_SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = get_google_credentials(ALL_SCOPES)
        if not creds:
            log.warning("[cancellation] Gmail: no credentials, skipping")
            return

        gmail = build("gmail", "v1", credentials=creds)
        salon_name = salon_config.get("salon_name", "el salón")
        salon_address = salon_config.get("address", "")

        # Format date
        try:
            from datetime import datetime as _dt
            dt_obj = _dt.fromisoformat(start_str)
            day_names = {0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}
            month_names = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",
                           7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
            fecha = f"{day_names[dt_obj.weekday()]}, {dt_obj.day} de {month_names[dt_obj.month]} de {dt_obj.year}"
            hora = dt_obj.strftime("%H:%M")
        except Exception:
            fecha = start_str
            hora = ""

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#f5f0eb;font-family:'Georgia',serif;">

  <!-- Header -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#1a1a1a;">
    <tr>
      <td align="center" style="padding:36px 24px 28px;">
        <p style="margin:0;font-size:11px;letter-spacing:4px;color:#e07070;text-transform:uppercase;">Cita cancelada</p>
        <h1 style="margin:10px 0 0;font-size:26px;font-weight:400;color:#ffffff;letter-spacing:1px;">{salon_name}</h1>
      </td>
    </tr>
  </table>

  <!-- Main card -->
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;margin:0 auto;">
    <tr>
      <td style="padding:0 24px;">

        <!-- Red bar -->
        <div style="height:3px;background:linear-gradient(90deg,#c0392b,#e74c3c,#c0392b);margin-bottom:0;"></div>

        <!-- Details card -->
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:0 0 8px 8px;">
          <tr>
            <td style="padding:36px 40px 32px;">

              <p style="margin:0 0 24px;font-size:16px;color:#2c2c2c;line-height:1.6;">
                La siguiente cita ha sido <strong>cancelada por el cliente</strong>.<br>
                El hueco ha quedado libre en el calendario.
              </p>

              <!-- Detail rows -->
              <table width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid #f0ebe4;">

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;width:38%;">Cliente</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;font-weight:600;">{client_name}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;">Servicio</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{service}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;">Fecha</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{fecha}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;">Hora</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{hora}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;">Profesional</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{staff_name}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;">Precio perdido</td>
                  <td style="padding:14px 0;font-size:15px;color:#c0392b;font-weight:600;">{price}€</td>
                </tr>

              </table>

              {"" if not salon_address else f'<p style="margin:24px 0 0;font-size:13px;color:#888;line-height:1.6;">📍 {salon_address}</p>'}

            </td>
          </tr>
        </table>

        <!-- Footer -->
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td align="center" style="padding:28px 24px;">
              <p style="margin:0;font-size:12px;color:#aaa;letter-spacing:1px;">Gestión automática por <strong style="color:#c9a96e;">Floux</strong></p>
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""

        plain = (
            f"Cita cancelada — {salon_name}\n\n"
            f"Cliente: {client_name}\n"
            f"Servicio: {service}\n"
            f"Fecha: {fecha} a las {hora}\n"
            f"Profesional: {staff_name}\n"
            f"Precio perdido: {price}€\n\n"
            f"El hueco ha quedado libre en el calendario."
        )

        msg = MIMEMultipart("alternative")
        msg["to"] = owner_email
        msg["subject"] = f"❌ Cita cancelada — {service} ({client_name})"
        msg.attach(MIMEText(plain, "plain"))
        msg.attach(MIMEText(html, "html"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        gmail.users().messages().send(userId="me", body={"raw": raw}).execute()
        log.info(f"[cancel] Owner cancellation email sent to {owner_email}")
        return True

    except Exception as e:
        log.error(f"[cancel] Gmail owner send failed: {e}", exc_info=True)
        return False


def _send_client_cancellation_email(salon_config: dict, client_email: str,
                                     service: str, client_name: str,
                                     start_str: str, staff_name: str) -> bool:
    """Send HTML cancellation email to the client via Gmail API.
    Red accent (#c0392b). Returns True on success."""
    import base64
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import sys as _sys
    _sys.path.insert(0, str(BASE_DIR / "execution"))
    from google_auth import get_google_credentials
    from googleapiclient.discovery import build

    if not client_email or "@" not in client_email:
        log.info("[cancel] Client email: skipped (no email)")
        return False

    try:
        ALL_SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = get_google_credentials(ALL_SCOPES)
        if not creds:
            log.warning("[cancel] Client email: no Google credentials")
            return False

        gmail = build("gmail", "v1", credentials=creds)
        salon_name = salon_config.get("salon_name", "el salón")
        salon_address = salon_config.get("address", "")

        try:
            from datetime import datetime as _dt
            dt_obj = _dt.fromisoformat(start_str)
            day_names = {0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}
            month_names = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",
                           7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
            fecha = f"{day_names[dt_obj.weekday()]}, {dt_obj.day} de {month_names[dt_obj.month]} de {dt_obj.year}"
            hora = dt_obj.strftime("%H:%M")
        except Exception:
            fecha = start_str
            hora = ""

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#f5f0eb;font-family:'Georgia',serif;">

  <!-- Header -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#1a1a1a;">
    <tr>
      <td align="center" style="padding:36px 24px 28px;">
        <p style="margin:0;font-size:11px;letter-spacing:4px;color:#e07070;text-transform:uppercase;">Tu cita ha sido cancelada</p>
        <h1 style="margin:10px 0 0;font-size:26px;font-weight:400;color:#ffffff;letter-spacing:1px;">{salon_name}</h1>
      </td>
    </tr>
  </table>

  <!-- Main card -->
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;margin:0 auto;">
    <tr>
      <td style="padding:0 24px;">

        <!-- Red bar -->
        <div style="height:3px;background:linear-gradient(90deg,#c0392b,#e74c3c,#c0392b);margin-bottom:0;"></div>

        <!-- Details card -->
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:0 0 8px 8px;">
          <tr>
            <td style="padding:36px 40px 32px;">

              <p style="margin:0 0 24px;font-size:16px;color:#2c2c2c;line-height:1.6;">
                Hola <strong>{client_name}</strong>,<br>
                Tu cita en {salon_name} ha sido <strong>cancelada correctamente</strong>.<br><br>
                Si quieres reservar otra cita, escríbenos por WhatsApp cuando quieras. ¡Te esperamos!
              </p>

              <!-- Detail rows -->
              <table width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid #f0ebe4;">

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;width:38%;">Servicio cancelado</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;font-weight:600;">{service}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;">Fecha</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{fecha}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;">Hora</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{hora}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;font-size:12px;letter-spacing:2px;color:#c0392b;text-transform:uppercase;">Profesional</td>
                  <td style="padding:14px 0;font-size:15px;color:#1a1a1a;">{staff_name}</td>
                </tr>

              </table>

              {"" if not salon_address else f'<p style="margin:24px 0 0;font-size:13px;color:#888;line-height:1.6;">📍 {salon_address}</p>'}

              <p style="margin:24px 0 0;padding:16px 20px;background:#fdf4f3;border-left:3px solid #c0392b;font-size:13px;color:#666;line-height:1.7;">
                Si la cancelación es un error, escríbenos por WhatsApp y te ayudamos a reservar de nuevo.
              </p>

            </td>
          </tr>
        </table>

        <!-- Footer -->
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td align="center" style="padding:28px 24px;">
              <p style="margin:0;font-size:12px;color:#aaa;letter-spacing:1px;">Gestión automática por <strong style="color:#c9a96e;">Floux</strong></p>
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""

        plain = (
            f"Hola {client_name},\n\n"
            f"Tu cita en {salon_name} ha sido cancelada correctamente.\n\n"
            f"Servicio: {service}\n"
            f"Fecha: {fecha}\n"
            f"Hora: {hora}\n"
            f"Profesional: {staff_name}\n\n"
            f"Si quieres reservar otra cita, escríbenos por WhatsApp cuando quieras. ¡Te esperamos!"
        )

        msg = MIMEMultipart("alternative")
        msg["to"] = client_email
        msg["subject"] = f"❌ Cita cancelada — {service} en {salon_name}"
        msg.attach(MIMEText(plain, "plain"))
        msg.attach(MIMEText(html, "html"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        gmail.users().messages().send(userId="me", body={"raw": raw}).execute()
        log.info(f"[cancel] Client cancellation email sent to {client_email}")
        return True

    except Exception as e:
        log.error(f"[cancel] Client cancellation email failed: {e}", exc_info=True)
        return False


def _create_calendar_event(salon_config: dict, bd: dict, start_str: str, end_str: str,
                            staff_name: str, price: float):
    """Create a Google Calendar event for the confirmed booking."""
    try:
        from google_auth import get_google_credentials
        from googleapiclient.discovery import build

        ALL_SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = get_google_credentials(ALL_SCOPES)
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
            "description": f"Reservado por Floux\nServicio: {svc_name}\nCliente: {client_name}\nPersonal: {staff_name}\nPrecio: {price}€",
            "start": {"dateTime": start_str, "timeZone": tz},
            "end": {"dateTime": end_str, "timeZone": tz},
            "reminders": {"useDefault": True},
        }

        created = service.events().insert(
            calendarId=calendar_id, body=event, sendUpdates="all"
        ).execute()
        event_id = created.get("id", "")
        event_url = created.get("htmlLink", "")
        log.info(f"Calendar event created: {event_url} (id={event_id})")

        # Send email notification via Gmail
        owner_email = salon_config.get("owner_email")
        if owner_email:
            _send_booking_email(creds, owner_email, svc_name, client_name,
                                start_str, staff_name, price, event_url)

        return event_id

    except Exception as e:
        log.error(f"Calendar event creation failed: {e}")
    return None


def _send_booking_email(creds, to_email: str, service: str, client_name: str,
                        start_str: str, staff_name: str, price: float, event_url: str):
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


def _send_client_confirmation_email(salon_config: dict, client_email: str, bd: dict,
                                    start_str: str, staff_name: str, price: float):
    """Send a styled HTML confirmation email to the client via Gmail API."""
    import base64
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import sys as _sys
    _sys.path.insert(0, str(BASE_DIR / "execution"))
    from google_auth import get_google_credentials
    from googleapiclient.discovery import build

    try:
        ALL_SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = get_google_credentials(ALL_SCOPES)
        if not creds:
            log.warning("Client confirmation email: no Google credentials, skipping")
            return

        gmail = build("gmail", "v1", credentials=creds)
        salon_name = salon_config.get("salon_name", "el salón")
        salon_address = salon_config.get("address", "")
        service = bd.get("service", "")
        client_name = bd.get("client_name", "")

        # Format date
        try:
            from datetime import datetime as _dt
            dt_obj = _dt.fromisoformat(start_str)
            day_names = {0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}
            month_names = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",
                           7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
            fecha = f"{day_names[dt_obj.weekday()]}, {dt_obj.day} de {month_names[dt_obj.month]} de {dt_obj.year}"
            hora = dt_obj.strftime("%H:%M")
        except Exception:
            fecha = start_str
            hora = ""

        # ── HTML email ───────────────────────────────────────
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#f5f0eb;font-family:'Georgia',serif;">

  <!-- Header -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#1a1a1a;">
    <tr>
      <td align="center" style="padding:36px 24px 28px;">
        <p style="margin:0;font-size:11px;letter-spacing:4px;color:#c9a96e;text-transform:uppercase;">Tu cita está confirmada</p>
        <h1 style="margin:10px 0 0;font-size:26px;font-weight:400;color:#ffffff;letter-spacing:1px;">{salon_name}</h1>
      </td>
    </tr>
  </table>

  <!-- Main card -->
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;margin:0 auto;">
    <tr>
      <td style="padding:0 24px;">

        <!-- Gold bar -->
        <div style="height:3px;background:linear-gradient(90deg,#c9a96e,#e8d5a3,#c9a96e);margin-bottom:0;"></div>

        <!-- Details card -->
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:0 0 8px 8px;">
          <tr>
            <td style="padding:36px 40px 32px;">

              <p style="margin:0 0 24px;font-size:16px;color:#2c2c2c;line-height:1.6;">
                Hola <strong>{client_name}</strong>, ✨<br>
                Estamos encantados de verte pronto. Aquí tienes los detalles de tu cita:
              </p>

              <!-- Detail rows -->
              <table width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid #f0ebe4;">

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c9a96e;text-transform:uppercase;width:38%;">Servicio</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;font-weight:600;">{service}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c9a96e;text-transform:uppercase;">Fecha</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{fecha}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c9a96e;text-transform:uppercase;">Hora</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{hora}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:12px;letter-spacing:2px;color:#c9a96e;text-transform:uppercase;">Profesional</td>
                  <td style="padding:14px 0;border-bottom:1px solid #f0ebe4;font-size:15px;color:#1a1a1a;">{staff_name}</td>
                </tr>

                <tr>
                  <td style="padding:14px 0;font-size:12px;letter-spacing:2px;color:#c9a96e;text-transform:uppercase;">Precio</td>
                  <td style="padding:14px 0;font-size:15px;color:#1a1a1a;font-weight:600;">{price}€</td>
                </tr>

              </table>

              <!-- Address -->
              {"" if not salon_address else f'<p style="margin:24px 0 0;font-size:13px;color:#888;line-height:1.6;">📍 {salon_address}</p>'}

              <!-- Note -->
              <p style="margin:24px 0 0;padding:16px 20px;background:#faf7f3;border-left:3px solid #c9a96e;font-size:13px;color:#666;line-height:1.7;">
                Si necesitas cancelar o cambiar tu cita, avísanos con al menos <strong>4 horas de antelación</strong> por WhatsApp.
              </p>

            </td>
          </tr>
        </table>

        <!-- Footer -->
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td align="center" style="padding:28px 24px;">
              <p style="margin:0;font-size:12px;color:#aaa;letter-spacing:1px;">Reserva gestionada por <strong style="color:#c9a96e;">Floux</strong></p>
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""

        # Plain text fallback
        plain = (
            f"Hola {client_name},\n\n"
            f"Tu cita en {salon_name} está confirmada.\n\n"
            f"Servicio: {service}\n"
            f"Fecha: {fecha}\n"
            f"Hora: {hora}\n"
            f"Profesional: {staff_name}\n"
            f"Precio: {price}€\n"
            f"{salon_address}\n\n"
            f"Si necesitas cancelar, avísanos con 4h de antelación por WhatsApp.\n\n"
            f"¡Nos vemos pronto!"
        )

        msg = MIMEMultipart("alternative")
        msg["to"] = client_email
        msg["subject"] = f"✅ Cita confirmada — {service} en {salon_name}"
        msg.attach(MIMEText(plain, "plain"))
        msg.attach(MIMEText(html, "html"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        gmail.users().messages().send(userId="me", body={"raw": raw}).execute()
        log.info(f"Client confirmation email sent to {client_email}")

    except Exception as e:
        log.error(f"Client confirmation email failed: {e}")


def _save_to_sheet(salon_config: dict, phone: str, bd: dict, start_str: str,
                   staff_name: str, price: float):
    """Save booking data to Google Sheets, creating headers if the sheet is empty."""
    sheet_url = salon_config.get("google_sheet_url", "")
    if not sheet_url:
        return

    HEADERS = ["Fecha", "Cliente", "Telefono", "Servicio", "Personal", "Precio", "Estado"]

    try:
        import sys as _sys
        _sys.path.insert(0, str(BASE_DIR / "execution"))
        from google_auth import get_google_credentials
        import gspread

        ALL_SCOPES = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = get_google_credentials(ALL_SCOPES)
        if not creds:
            log.warning("Sheets: no credentials, skipping")
            return

        client = gspread.authorize(creds)
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        spreadsheet = client.open_by_key(sheet_id)
        ws = spreadsheet.sheet1

        # Create or update headers
        existing = ws.row_values(1)
        if not existing:
            ws.append_row(HEADERS)
        elif existing != HEADERS:
            ws.update("A1", [HEADERS])

        row = [
            start_str,
            bd.get("client_name", ""),
            phone,
            bd.get("service", ""),
            staff_name,
            f"{price}€",
            "Confirmada",
        ]
        ws.append_row(row, value_input_option="RAW")

        # Apply green background to the new confirmed row
        last_row = len(ws.get_all_values())
        green_format = {
            "backgroundColor": {"red": 0.78, "green": 0.93, "blue": 0.80}
        }
        ws.format(f"A{last_row}:G{last_row}", green_format)
        log.info("Booking saved to Google Sheets (green)")

    except Exception as e:
        log.error(f"Google Sheets save failed: {e}")


def _get_availability(salon_config: dict, booking_data: dict) -> list[dict] | None:
    """Get availability slots from schedule. Works for any platform — always returns slots."""
    try:
        from check_availability import get_eligible_staff, check_google_calendar

        service = booking_data.get("service", "")
        staff_pref = booking_data.get("staff_preference", "")

        if service:
            eligible = get_eligible_staff(salon_config, service, staff_pref or None)
            if not eligible:
                log.warning(f"No eligible staff for service: {service}")
                eligible = salon_config.get("staff", [])
        else:
            eligible = salon_config.get("staff", [])

        # Always use check_google_calendar — it falls back to schedule-only
        # if Google Calendar is unavailable, and works regardless of platform.
        # Treatwell/Booksy browser automation is not available in production.
        slots = check_google_calendar(salon_config, service, eligible)

        log.info(f"Availability: {len(slots)} slots returned")
        return slots

    except Exception as e:
        log.error(f"Availability check failed: {e}", exc_info=True)
        return None  # None = system error, tells AI to ask client for preference


# ── Health check ─────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now(TZ).isoformat()}
