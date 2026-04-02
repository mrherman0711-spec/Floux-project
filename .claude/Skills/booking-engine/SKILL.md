---
name: booking-engine
description: "Builds the Floux booking engine in Claude Code. Use when building the webhook handler, conversation session manager, Treatwell/Booksy availability checker, Google Calendar fallback, staff assignment logic, or any core backend logic for the missed-call recovery system."
allowed-tools:
  - Bash
  - Write
  - Read
---

# Floux Booking Engine — Architecture Reference

## Request Handler Chain

```
POST /missed-call (Twilio webhook)
  → respond 200 immediately (before any logic — 15s timeout)
  → normalize phone to E.164
  → filter: only CallStatus "no-answer" | "busy" → else drop
  → deduplicate: check CallSid in seen_calls store → if seen, drop
  → mark CallSid as seen
  → send WhatsApp greeting via Twilio
  → open session keyed by phone number

POST /whatsapp-reply (Twilio incoming message webhook)
  → load session by phone number
  → append client message to conversation history
  → fetch current availability slots from booking system
  → call OpenAI with system prompt + history + availability
  → parse JSON response
  → if escalate=true → send owner alert → close session
  → if conversation_complete=true → book appointment → send confirmation → notify owner → close session
  → else → send reply → save updated session
```

## Session Object Schema

```json
{
  "phone": "+34612345678",
  "call_sid": "CA1234abc...",
  "language": "es",
  "created_at": "ISO8601",
  "last_active": "ISO8601",
  "conversation": [
    { "role": "assistant", "content": "¡Hola! Hemos visto..." },
    { "role": "user", "content": "Hola, quiero una cita..." }
  ],
  "booking_data": {
    "service": "",
    "datetime": "",
    "client_name": "",
    "staff_preference": "",
    "staff_assigned": ""
  },
  "status": "active | booked | escalated | expired"
}
```

Session storage: Google Sheets (one row per session, JSON in a cell) or in-memory for dev.
Session timeout: 10 minutes of inactivity → mark expired, optionally send follow-up.

## Availability Fetching

```
function getAvailability(salonConfig, requestedService, staffPreference):
  if salonConfig.platform == "treatwell":
    → Chrome DevTools MCP: navigate to Treatwell dashboard
    → read calendar grid for next 3 days
    → filter slots by service duration + staff capable of service
    → return slot list in standard format
  elif salonConfig.platform == "booksy":
    → Chrome DevTools MCP: navigate to Booksy dashboard
    → same extraction approach
  else:
    → Google Calendar API: list events in salon calendar
    → compute free slots based on working hours - existing events
    → return slot list in standard format

Standard slot format:
"viernes 11 abril: 10:00(María), 12:30(Laura), 16:00(María) | sábado 12 abril: 10:00(María)"
```

## Staff Assignment Logic

```
1. Look up which staff can perform requested_service (from salonConfig.staff)
2. If client expressed staff_preference:
   a. Check if preferred staff can do the service → if not, explain and offer alternatives
   b. Filter availability slots to preferred staff only
3. If no preference:
   a. Filter slots to any qualified staff
   b. Assign first available
4. Confirm assigned staff in booking_data.staff_assigned
```

## Booking Execution

```
if salonConfig.platform == "treatwell":
  → Chrome DevTools MCP: navigate to new booking form
  → fill service, date, time, client name, staff
  → submit and confirm booking reference

elif salonConfig.platform == "booksy":
  → Chrome DevTools MCP: same approach

else (Google Calendar):
  → Create event via Calendar API
  → Event title: "{service} — {client_name}"
  → Attendees: salon owner email
  → Duration: from salonConfig.service_durations[service]
```

## OpenAI Call Config

```javascript
{
  model: "gpt-4o-mini",
  response_format: { type: "json_object" },
  temperature: 0.3,
  messages: [
    { role: "system", content: systemPrompt },  // loaded from salonConfig, NOT hardcoded
    ...session.conversation
  ]
}
```

## Twilio Critical Rules

- `whatsapp:` prefix required on all To/From fields — forgetting it = silent failure
- Respond 200 MUST be first action — Twilio retries if no response within 15s
- CallSid deduplication — Twilio retries failed webhooks, duplicates WILL happen
- Filter: ONLY process `no-answer` and `busy` — never `completed` or `canceled`

## Verification Checklist

After any change, test these 3 conversations minimum:
1. Happy path (ES): greeting → service + date → staff assigned → availability confirmed → booking → owner notification
2. Happy path (EN): same flow but client writes in English
3. Escalation: angry message → owner gets full conversation context
4. Edge case: same CallSid sent twice → second one dropped silently
