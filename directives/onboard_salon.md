# Onboard New Salon

Set up a new salon client on Floux: collect their config, create their salonConfig JSON, generate and test their AI system prompt, verify the full flow works before going live.

## Inputs

Information to collect from salon owner (in-person or via WhatsApp):
- Salon name and address
- Owner name and WhatsApp number
- Services offered (name, duration in minutes, price in €)
- Staff members and which services each can do
- Working hours (per day of week)
- Booking platform: Treatwell, Booksy, or neither (→ Google Calendar)
- Platform URL (their dashboard login URL)
- Twilio number assigned to this salon

## Scripts to Use

- `execution/manage_session.py` — verify Google Sheets connection works
- `execution/read_sheet.py` — verify read access to logging sheet
- `execution/send_whatsapp.py` — test WhatsApp delivery
- `execution/check_availability.py` — verify platform access

## Process

### Step 1: Create salonConfig JSON
Create file: `prompts/{salon_id}.json`

Use this schema:
```json
{
  "salon_id": "villaviciosa_001",
  "name": "Centro de Estética Carmen",
  "address": "Calle Mayor 12, Villaviciosa de Odón",
  "owner_name": "Carmen",
  "owner_phone": "whatsapp:+34612345678",
  "owner_email": "carmen@example.com",
  "twilio_number": "+34911234567",
  "twilio_whatsapp_number": "whatsapp:+34911234567",
  "platform": "treatwell",
  "platform_url": "https://partners.treatwell.es/...",
  "default_language": "es",
  "working_hours": {
    "lunes": "10:00-20:00",
    "martes": "10:00-20:00",
    "miercoles": "10:00-20:00",
    "jueves": "10:00-20:00",
    "viernes": "10:00-20:00",
    "sabado": "10:00-14:00",
    "domingo": "cerrado"
  },
  "services": [
    {"name": "Manicura", "duration_min": 45, "price": 25},
    {"name": "Pedicura", "duration_min": 60, "price": 30},
    {"name": "Mechas", "duration_min": 90, "price": 65},
    {"name": "Tinte", "duration_min": 60, "price": 45},
    {"name": "Corte y peinado", "duration_min": 45, "price": 35}
  ],
  "staff": [
    {
      "name": "María",
      "platform_name": "María García",
      "services": ["Mechas", "Tinte", "Corte y peinado"]
    },
    {
      "name": "Laura",
      "platform_name": "Laura Martínez",
      "services": ["Manicura", "Pedicura"]
    }
  ],
  "system_prompt": ""
}
```

### Step 2: Generate system prompt
Use the prompt-engineer skill to generate the system prompt from this salonConfig.
Paste the generated prompt into `salonConfig.system_prompt`.

The prompt must include:
- Salon name, address, owner name
- SERVICES_LIST with prices
- SCHEDULE formatted as natural language
- STAFF_LIST with services per person
- AVAILABILITY_SLOTS placeholder (injected at runtime)
- All language and escalation rules

### Step 3: Test the system prompt (11 scenarios)
Run each test scenario manually (or via test_prompt.py once built):

1. "Hola, quiero una cita para manicura el jueves por la tarde"
2. "¿Cuánto cuesta un tinte?"
3. "Quiero una cita pero no sé cuándo"
4. [Simulate audio/voice note: Body empty, NumMedia=1]
5. "¿Eres un robot?"
6. "Estoy muy enfadada con el servicio del otro día"
7. "Quiero un tratamiento que no existe en la lista"
8. "Para mañana a las 9" (outside working hours)
9. "Me da igual la hora, cuando haya hueco"
10. "Quiero con María" (staff preference)
11. "Hi, I'd like a manicure on Friday afternoon" (English client)

Each must return valid JSON with correct `intent` and natural response in the right language.

### Step 4: Verify execution scripts
```bash
# Test phone normalization
python3 execution/normalize_phone.py --phone "+34 612 345 678"

# Test WhatsApp sending (use your own number for test)
python3 execution/send_whatsapp.py \
  --to "whatsapp:+34XXXXXXXXX" \
  --from-number "<salon twilio_whatsapp_number>" \
  --message "Test message — Floux onboarding check"

# Test Google Sheets access
python3 execution/read_sheet.py --url "<sessions sheet URL>"

# Test availability check (platform must be accessible)
python3 execution/check_availability.py \
  --salon-id "<salon_id>" \
  --service "Manicura"
```

All must return success before going live.

### Step 5: Simulate full conversation
Using Twilio sandbox or test number, simulate:
1. Missed call → WhatsApp greeting arrives within 30s ✓
2. Reply with service + date → AI responds with available slots ✓
3. Confirm booking → Booking executed on platform ✓
4. Confirmation sent to client ✓
5. Owner notification sent ✓

### Step 6: Go live checklist
- [ ] salonConfig JSON complete and valid
- [ ] system_prompt tested against all 11 scenarios
- [ ] Twilio number configured to forward missed calls to Floux webhook
- [ ] WhatsApp delivery confirmed working
- [ ] Google Sheets sessions tab accessible
- [ ] Platform credentials verified (Treatwell/Booksy login tested)
- [ ] Owner informed of how escalation notifications work
- [ ] Owner's WhatsApp number confirmed in salonConfig

## Outputs

- `prompts/{salon_id}.json` — complete salonConfig
- Salon live on Floux, receiving missed call recovery

## Edge Cases

- **Owner has no Treatwell/Booksy:** Use Google Calendar. Create a dedicated Google Calendar for the salon, share with owner.
- **Owner has multiple locations:** Create separate salonConfig per location with different salon_id and Twilio number.
- **Platform uses different language:** Treatwell Spain is in Spanish. Booksy Spain is in Spanish. Adjust platform_name fields accordingly.
- **Owner wants to keep manual booking:** Start with Básico tier (WhatsApp only, no AI). Upgrade to Agente when they trust it.

## Learnings

- Collect service durations precisely — wrong duration = double-booked slots
- Always verify owner's WhatsApp is active before going live (some owners use landlines)
- Treatwell platform_name for staff is their full name as it appears on the platform — ask owner to confirm spelling
