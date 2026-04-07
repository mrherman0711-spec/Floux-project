---
name: missed-call-recovery
description: "Handle an incoming Twilio missed-call webhook to send a WhatsApp greeting. Use ONLY when processing a raw Twilio CallStatus webhook with no-answer or busy status."
allowed-tools:
  - Bash
  - Read
---

# Missed Call Recovery

Detect a missed call from Twilio, identify the salon, and send a WhatsApp greeting to the client within 30 seconds.

## Inputs

Twilio webhook POST body:
- `From` — client phone number (raw, may include spaces/dashes)
- `To` — salon's Twilio number (used to identify which salon)
- `CallStatus` — must be `no-answer` or `busy` to proceed
- `CallSid` — unique call ID for deduplication

## Scripts to Use

- `execution/normalize_phone.py` — normalize client and salon numbers to E.164
- `execution/manage_session.py --action check-duplicate --call-sid` — deduplication check
- `execution/manage_session.py --action create` — open new session
- `execution/send_whatsapp.py` — send greeting message
- `execution/read_sheet.py` — load salonConfig if not in prompts/ (fallback)

## Process

### Step 1: Respond 200 immediately
Return HTTP 200 with empty TwiML body BEFORE any logic. Twilio times out at 15 seconds.
```xml
<?xml version="1.0" encoding="UTF-8"?><Response/>
```

### Step 2: Normalize phones
```bash
python3 execution/normalize_phone.py --phone "<From value>"
python3 execution/normalize_phone.py --phone "<To value>"
```
Both must return `valid: true`. If invalid, log and drop.

### Step 3: Filter call status
Only continue if `CallStatus` is `no-answer` or `busy`.
Drop silently if `completed`, `canceled`, `failed`, or anything else.

### Step 4: Deduplicate by CallSid
```bash
python3 execution/manage_session.py --action check-duplicate --call-sid "<CallSid>"
```
If already seen: drop silently. If new: mark as seen and continue.

### Step 5: Identify salon from Twilio number
Load `prompts/{salon_id}.json` where `twilio_number` matches the normalized `To`.
If no match found: log error, drop (unknown salon).

### Step 6: Open session
```bash
python3 execution/manage_session.py --action create \
  --phone "<normalized client phone>" \
  --call-sid "<CallSid>" \
  --salon-id "<salon_id>"
```

### Step 7: Send WhatsApp greeting
```bash
python3 execution/send_whatsapp.py \
  --to "<normalized client phone>" \
  --from-number "<salon twilio_whatsapp_number>" \
  --message "¡Hola! Hemos visto que nos has llamado a {SALON_NAME} y no hemos podido atenderte. 😊\n\n¿En qué podemos ayudarte? Si quieres reservar una cita, dime qué servicio te interesa y cuándo te vendría bien."
```
(Use English version if salon has `default_language: "en"`)

## Outputs

- HTTP 200 response to Twilio (immediate)
- WhatsApp message delivered to client
- Session created in Google Sheets sessions tab
- CallSid logged as processed

## Edge Cases

- **Same client calls twice (different CallSid):** Two sessions opened. Normal — client may have called from different context. Both will receive greeting.
- **Salon not found for Twilio number:** Log error with `To` number. Drop. Add salon mapping to fix.
- **Client phone invalid after normalization:** Log and drop. Cannot reply without valid number.
- **Twilio WhatsApp delivery failure (error 21211):** Phone not WhatsApp-enabled. Log, close session, no retry.
- **Client already has active session (called recently):** Check in manage_session — if session exists and status=active, skip greeting (they're already in conversation).

## Error Handling

- Twilio error 21211 (invalid number): drop session
- Twilio error 63016 (rate limit): retry once after 5 seconds
- Google Sheets auth error: check token.json validity, re-authenticate if needed
- Any unhandled exception: log full stack trace to .tmp/errors.log, return 200 to Twilio (never let Twilio retry on logic errors)

## Learnings

- `whatsapp:` prefix required on To/From in Twilio API — forgetting it = silent failure, no error
- Twilio retries webhooks if it doesn't get 200 within 15s — respond first, always
- CallSid deduplication is mandatory — Twilio WILL retry on network issues
