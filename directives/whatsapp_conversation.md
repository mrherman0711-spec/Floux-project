# WhatsApp Conversation

Handle an incoming WhatsApp reply from a client. Load session, fetch availability, call AI, parse response, act on intent.

## Inputs

Twilio webhook POST body (incoming WhatsApp message):
- `From` — client WhatsApp number (e.g. `whatsapp:+34612345678`)
- `Body` — message text content
- `MediaUrl0` — present if client sent a voice note or image (handle as edge case)
- `NumMedia` — number of media attachments

## Scripts to Use

- `execution/normalize_phone.py` — normalize From number
- `execution/manage_session.py --action load` — load existing session
- `execution/check_availability.py` — fetch current slots before calling AI
- `execution/send_whatsapp.py` — send reply to client
- `execution/manage_session.py --action save` — persist updated session
- `execution/book_appointment.py` — when conversation_complete=true
- `execution/append_to_sheet.py` — log completed booking or escalation

## Process

### Step 1: Respond 200 immediately
Same as missed_call — return HTTP 200 with empty TwiML before any logic.

### Step 2: Normalize phone and load session
```bash
python3 execution/normalize_phone.py --phone "<From value, strip whatsapp: prefix>"
python3 execution/manage_session.py --action load --phone "<normalized phone>"
```
If no session found: client messaged without a missed call trigger. Create a new session and treat as greeting.
If session status is `booked` or `escalated`: reply "Tu cita ya está confirmada. Si necesitas algo más, llámanos." and stop.

### Step 3: Handle media (voice notes / images)
If `NumMedia > 0` or `Body` is empty:
```bash
python3 execution/send_whatsapp.py --to "<phone>" --message "Disculpa, no puedo escuchar audios. ¿Me lo puedes escribir? 😊"
```
(English: "Sorry, I can't listen to voice notes. Could you write it instead? 😊")
Save session with appended assistant message. Stop.

### Step 4: Fetch availability
```bash
python3 execution/check_availability.py \
  --salon-id "<salon_id from session>" \
  --service "<booking_data.service if known, else blank>" \
  --staff "<booking_data.staff_preference if known, else blank>"
```
Inject the returned slots into the system prompt as `AVAILABILITY_SLOTS`.

### Step 5: Call OpenAI
Build messages array:
- system: salonConfig.system_prompt with AVAILABILITY_SLOTS injected
- messages: session.conversation (all prior turns)
- Append new user message

Call OpenAI:
```
model: gpt-4o-mini
response_format: { type: "json_object" }
temperature: 0.3
```

### Step 6: Parse JSON response
Expected fields:
```json
{
  "reply": "texto para enviar al cliente",
  "language": "es | en",
  "intent": "booking | question | escalate | greeting",
  "booking_data": {
    "service": "",
    "datetime": "",
    "client_name": "",
    "staff_preference": "",
    "staff_assigned": ""
  },
  "escalate": false,
  "conversation_complete": false
}
```
If JSON is invalid or missing required fields: retry once with stricter prompt. If second failure: escalate to owner.

### Step 7: Route on intent

**If `escalate: true`:**
- Send client message: "Entendido, paso tu mensaje a [OWNER_NAME] ahora mismo. 😊"
- Send owner WhatsApp alert with full conversation context
- Update session status to `escalated`
- Log to Google Sheets
- Stop

**If `conversation_complete: true`:**
- Send confirmation message to client
- Run `execution/book_appointment.py` with booking_data
- Send owner notification with booking details
- Update session status to `booked`
- Log completed booking to Google Sheets
- Stop

**If ongoing conversation:**
- Send reply to client via send_whatsapp.py
- Append both user message and assistant reply to session.conversation
- Save session

### Step 8: Save session
```bash
python3 execution/manage_session.py --action save \
  --phone "<phone>" \
  --session-json "<updated session JSON>"
```

## Owner Notification Format

When booking complete or escalation triggered:
```
📱 NUEVA CITA

Cliente: {client_name}
Teléfono: {phone}
Servicio: {service}
Fecha/hora: {datetime}
Personal: {staff_assigned}
Estado: booked | escalated
Motivo (si escalado): {reason}
```

## Edge Cases

- **Session expired (>10 min inactivity):** Treat as new conversation, re-send greeting
- **Client sends "Hola" with no context:** Respond with greeting + ask what they need
- **Client asks price for unknown service:** Escalate to owner
- **Client requests staff that can't do the service:** Explain and offer alternatives from same staff pool
- **No availability in next 3 days:** Offer first available slot beyond that window
- **OpenAI returns empty reply field:** Do not send empty message. Log and retry once.

## Error Handling

- Invalid JSON from OpenAI (2nd failure): escalate to owner, close session
- check_availability.py fails: proceed without AVAILABILITY_SLOTS, note in system prompt that availability is temporarily unavailable, ask client to confirm datetime and verify manually
- send_whatsapp.py delivery failure: retry once after 30s, log if fails again
- manage_session.py save failure: log error, session will reload from last good state on next message

## Learnings

- Always fetch availability BEFORE calling AI — stale availability data causes hallucinated confirmations
- Temperature 0.3 keeps responses consistent; higher values cause tone drift mid-conversation
- session.conversation must include ALL turns (not just recent) to maintain context across messages
- 24-hour WhatsApp session window: after 24h without client message, only approved templates can be sent
