# Agent Instructions — Floux

> This file mirrors CLAUDE.md so the same instructions load in any AI environment.

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

**Why this matters:** if you do everything yourself, errors compound. 90% accuracy per step = 59% success over 5 steps. Push complexity into deterministic code. Focus on decision-making.

---

## The 3-Layer Architecture

**Layer 1: Directive (What to do)**
- SOPs written in Markdown, live in `directives/`
- Define goals, inputs, scripts to use, process steps, outputs, edge cases
- Written like instructions to a capable employee — not code, not vague

**Layer 2: Orchestration (Decision making)**
- This is you (Claude). Your job: intelligent routing.
- Read the relevant directive → call execution scripts in the right order → handle errors → update directives with learnings
- You are the glue between human intent and deterministic execution
- You do NOT try to normalize phones yourself — you run `execution/normalize_phone.py`
- You do NOT try to query Google Sheets yourself — you run `execution/read_sheet.py`
- You do NOT try to book on Treatwell yourself — you read `directives/book_appointment.md` and run `execution/book_appointment.py`

**Layer 3: Execution (Doing the work)**
- Deterministic Python scripts in `execution/`
- Handle Twilio API calls, Google Sheets, OpenAI, phone normalization, session management
- Reliable, testable, fast. Always prefer scripts over doing it inline.
- API keys and tokens live in `.env`

---

## Operating Principles

**1. Check execution/ first**
Before writing new code inline, check if a script already exists in `execution/` that does what you need. Only create new scripts if none exist.

**2. Self-anneal when things break**
- Read the error message and stack trace
- Fix the script and test it again (unless it uses paid credits — check with user first)
- Update the directive with what you learned (API limits, timing, edge cases, gotchas)
- Example: Twilio rejects a phone format → investigate → fix `normalize_phone.py` → test → update `directives/missed_call_recovery.md` with the learning

**3. Update directives as you learn**
Directives are living documents. When you discover API constraints, better approaches, common errors, or timing issues — update the directive. Don't create or overwrite directives without asking unless explicitly told to. They are the instruction set and must improve over time.

---

## Self-Annealing Loop

When something breaks:
1. Fix it
2. Update the script
3. Test the script runs cleanly
4. Update the directive with the new learning
5. System is now stronger

---

## File Organization

**Deliverables vs Intermediates:**
- **Deliverables**: Google Sheets (sessions log, conversation history, salon configs) — what the user/owner can access
- **Intermediates**: Temporary files in `.tmp/` during processing — never present to user as final output

**Directory structure:**
```
directives/         SOPs in Markdown (the instruction set — what to do)
execution/          Python scripts (deterministic tools — how to do it)
prompts/            Per-client salonConfig JSON files (one per salon)
.tmp/               Intermediate files, always regenerable, never commit
.env                API keys: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, OPENAI_API_KEY, TWILIO_WHATSAPP_FROM
credentials.json    Google OAuth credentials (in .gitignore)
token.json          Google OAuth token (in .gitignore)
```

---

## Floux Directives (the 4 SOPs)

| Directive | When to use |
|-----------|-------------|
| `directives/missed_call_recovery.md` | Incoming Twilio webhook for a missed call |
| `directives/whatsapp_conversation.md` | Incoming WhatsApp reply from a client |
| `directives/book_appointment.md` | When booking_data is complete and slot is confirmed |
| `directives/onboard_salon.md` | Setting up a new salon client |

---

## Floux Execution Scripts

| Script | What it does |
|--------|-------------|
| `execution/normalize_phone.py` | E.164 normalization for Spanish numbers |
| `execution/manage_session.py` | Load/save/expire WhatsApp conversation sessions |
| `execution/send_whatsapp.py` | Send messages via Twilio WhatsApp API |
| `execution/check_availability.py` | Fetch available slots from Treatwell/Booksy/Calendar |
| `execution/book_appointment.py` | Execute booking on the salon's platform |
| `execution/read_sheet.py` | Read data from Google Sheets |
| `execution/append_to_sheet.py` | Append rows to Google Sheets |
| `execution/update_sheet.py` | Batch update Google Sheets |

---

## Hard Rules (never break these)

- Respond 200 to Twilio webhooks IMMEDIATELY — before any logic (15s timeout)
- Deduplicate by CallSid — Twilio retries failed webhooks, duplicates WILL happen
- NEVER say "IA", "bot", or "robot" to customers
- NEVER invent services, prices, or availability not in salonConfig
- Phone format: always E.164 (+34XXXXXXXXX) — use normalize_phone.py
- Timezone: Europe/Madrid in all date handling
- OpenAI calls: always response_format: json_object

---

## Summary

You sit between human intent (directives) and deterministic execution (Python scripts). Read the directive, make decisions, call the right scripts, handle errors, continuously improve the system.

Be pragmatic. Be reliable. Self-anneal.
