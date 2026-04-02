---
name: twilio-integration
description: "Configures Twilio for Floux missed-call detection and WhatsApp messaging. Use when setting up Twilio webhooks, debugging WhatsApp delivery, handling TwiML responses, filtering call statuses, configuring sandbox, or troubleshooting Twilio errors."
allowed-tools:
  - Bash
  - Read
  - Write
---

# Floux Twilio Integration — Gotchas Only

## Script: send_whatsapp.py

All WhatsApp sends go through `execution/send_whatsapp.py`:
```bash
python3 execution/send_whatsapp.py \
  --to "whatsapp:+34612345678" \
  --from-number "whatsapp:+34911234567" \
  --message "¡Hola! ..."
```
Output: `{"sid": "SMxxx", "status": "queued"}` or `{"status": "error", "error": "...", "code": 21211}`

## TwiML Response (must return this immediately)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response/>
```
Return this BEFORE any logic. Empty response = acknowledge receipt. Twilio times out at 15 seconds — respond first, always.

## Webhook Payload Fields We Use

| Field | Example | Use |
|-------|---------|-----|
| `From` | `+34612345678` | Client phone — use for WhatsApp reply |
| `To` | `+34911234567` | Salon's Twilio number |
| `CallStatus` | `no-answer` | Filter: ONLY process `no-answer` and `busy` |
| `CallSid` | `CA1234abc...` | Unique call ID — deduplicate with this |

## Critical Rules

1. **whatsapp: prefix required.** Twilio WhatsApp messages use `whatsapp:+34612345678` format for both To and From. Forgetting the prefix = silent failure, no error.

2. **CallStatus filter: ONLY `no-answer` and `busy`.** NEVER trigger on `completed` (that means someone answered), `canceled`, or `failed`.

3. **Respond 200 = first action.** Always. No exceptions. Return HTTP 200 before any logic. Twilio will retry if it doesn't get a 200 within 15 seconds.

4. **CallSid deduplication.** Twilio retries webhooks on failure. Use an IF node with a KV store (or Google Sheet column) to check if CallSid was already processed. Skip if seen.

## Sandbox Limitations (V1 development)

- Users must send "join [keyword]" to the sandbox number first
- Only pre-joined users receive messages
- 50 messages/day limit on trial
- Sandbox number changes periodically — check Twilio console
- Template messages not available in sandbox — only session messages

## Common Errors

| Code | Meaning | Fix |
|------|---------|-----|
| 63015 | Template not found/approved | Check template name matches exactly, wait for Meta approval |
| 21211 | Invalid phone number | Ensure E.164 format with whatsapp: prefix |
| 63016 | WhatsApp rate limit | Reduce message frequency, check daily limits |
| 21608 | Unverified number (trial) | User hasn't joined sandbox or number not verified |
| Timeout | No 200 response in 15s | Ensure HTTP 200 is returned before any logic |
