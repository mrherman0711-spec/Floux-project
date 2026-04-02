# Book Appointment

Execute a booking on the salon's platform (Treatwell, Booksy, or Google Calendar) once booking_data is complete and the client has confirmed.

## Inputs

From session.booking_data:
- `service` — confirmed service name (must match salonConfig.services exactly)
- `datetime` — ISO8601 datetime string (e.g. "2026-04-11T16:30:00")
- `client_name` — client's full name
- `staff_assigned` — which staff member will do the service
- `staff_preference` — original client preference (may differ from assigned)

From salonConfig:
- `platform` — "treatwell" | "booksy" | "google_calendar"
- `platform_url` — URL to the salon's dashboard
- `service_durations` — duration in minutes per service

## Scripts to Use

- `execution/book_appointment.py` — main booking executor
- `execution/append_to_sheet.py` — log the completed booking

## Process

### Step 1: Validate booking_data completeness
All 4 fields must be non-empty: service, datetime, client_name, staff_assigned.
If any missing: do NOT attempt booking. Return error — conversation is not complete.

### Step 2: Run booking executor
```bash
python3 execution/book_appointment.py \
  --salon-id "<salon_id>" \
  --slot "<ISO8601 datetime>" \
  --service "<service name>" \
  --staff "<staff_assigned>" \
  --client-name "<client_name>"
```

Expected output:
```json
{"booked": true, "reference": "TW-12345", "platform": "treatwell"}
```
or
```json
{"booked": false, "error": "Slot no longer available", "platform": "treatwell"}
```

### Step 3: Handle booking result

**If `booked: true`:**
- Send confirmation to client (see confirmation format below)
- Send owner notification with booking reference
- Log to Google Sheets bookings tab
- Update session status to `booked`

**If `booked: false`:**
- Do NOT confirm to client
- Re-fetch availability: `execution/check_availability.py`
- Offer next 2-3 available slots to client
- Keep session status as `active`
- Update directive with the error type (common: slot taken by manual booking between check and execution)

### Confirmation Format (client)
```
ES:
¡Perfecto! Te confirmo tu cita:

📋 Servicio: {service}
📅 Fecha: {date formatted as "viernes 11 de abril"}
🕐 Hora: {time}
💇 Con: {staff_assigned}

Si necesitas cambiar algo, escríbeme. ¡Te esperamos! 😊

EN:
All set! Here's your confirmation:

📋 Service: {service}
📅 Date: {date formatted as "Friday 11 April"}
🕐 Time: {time}
💇 With: {staff_assigned}

If you need to change anything, just message me. See you then! 😊
```

## Platform-Specific Notes

### Treatwell
- Uses Chrome DevTools MCP to navigate the Treatwell partner dashboard
- Navigate to: New Booking → select service → select staff → select time → enter client name → confirm
- Booking reference appears in the confirmation screen (format: TW-XXXXXX)
- Common error: "Professional not available" — staff member was manually booked since availability check. Re-fetch slots.
- Do NOT use the public-facing Treatwell booking widget — use the partner/admin dashboard

### Booksy
- Uses Chrome DevTools MCP to navigate the Booksy business dashboard
- Navigate to: Calendar → New Appointment → select service → select employee → select time → enter client info → save
- Booking reference appears in appointment details
- Common error: "Time slot already booked" — same as Treatwell, re-fetch slots

### Google Calendar (fallback)
- Uses Google Calendar API directly (no browser automation needed)
- Create event: title = "{service} — {client_name}", calendar = salon's calendar
- Duration from salonConfig.service_durations[service]
- Add owner email as attendee for notification
- No booking reference — use event ID

## Edge Cases

- **Slot taken between check and booking (race condition):** Happens when salon manually books same slot. Re-fetch availability, offer alternatives.
- **Chrome DevTools MCP loses browser session:** Re-navigate from login URL in salonConfig.platform_url. Log the interruption.
- **Treatwell/Booksy session expired:** Re-authenticate using stored credentials. If credentials missing, escalate to owner to manually book.
- **Service name mismatch:** booking_data.service may be in client's language but platform expects exact catalog name. Map via salonConfig.services[].name.
- **Staff not found on platform:** Cross-reference salonConfig.staff[].platform_name if different from display name.

## Error Handling

- 3 failed booking attempts: escalate to owner with full booking_data, ask them to book manually
- Platform unavailable (503): retry after 60s, log incident
- Chrome DevTools MCP crash: restart browser session, retry once

## Learnings

- Always re-fetch availability immediately before executing — even if checked 30 seconds ago
- Treatwell platform_name for staff may differ from their display name — add platform_name field to salonConfig.staff[]
- Google Calendar bookings don't send automatic client confirmations — Floux handles that via WhatsApp
