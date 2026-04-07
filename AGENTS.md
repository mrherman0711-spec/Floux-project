# Agent Instructions — Floux

> This file mirrors CLAUDE.md so the same instructions load in any AI environment.

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

**Why this matters:** if you do everything yourself, errors compound. 90% accuracy per step = 59% success over 5 steps. Push complexity into deterministic code. Focus on decision-making.

---

## The 3-Layer Architecture

**Layer 1: Skills (What to do)**
- SOPs written in Markdown with YAML frontmatter, live in `.claude/Skills/`
- Define goals, inputs, scripts to use, process steps, outputs, edge cases
- Auto-loaded by Claude Code when their trigger description matches the task
- Written like instructions to a capable employee — not code, not vague

**Layer 2: Orchestration (Decision making)**
- This is you (Claude). Your job: intelligent routing.
- The relevant skill auto-loads → call execution scripts in the right order → handle errors → update skills with learnings
- You are the glue between human intent and deterministic execution
- You do NOT try to normalize phones yourself — you run `execution/normalize_phone.py`
- You do NOT try to query Google Sheets yourself — you run `execution/read_sheet.py`
- You do NOT try to book on Treatwell yourself — you read the book-appointment skill and run `execution/book_appointment.py`

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
- Update the skill with what you learned (API limits, timing, edge cases, gotchas)
- Example: Twilio rejects a phone format → investigate → fix `normalize_phone.py` → test → update `.claude/Skills/missed-call-recovery/SKILL.md` with the learning

**3. Update skills as you learn**
Skills are living documents. When you discover API constraints, better approaches, common errors, or timing issues — update the skill. Don't create or overwrite skills without asking unless explicitly told to. They are the instruction set and must improve over time.

---

## Self-Annealing Loop

When something breaks:
1. Fix it
2. Update the script
3. Test the script runs cleanly
4. Update the skill with the new learning
5. System is now stronger

---

## File Organization

**Deliverables vs Intermediates:**
- **Deliverables**: Google Sheets (sessions log, conversation history, salon configs) — what the user/owner can access
- **Intermediates**: Temporary files in `.tmp/` during processing — never present to user as final output

**Directory structure:**
```
.claude/Skills/     Skills with YAML frontmatter (the instruction set — what to do)
.claude/agents/     Subagents for specialized tasks (prospector, sales-coach, etc.)
.claude/rules/      Brand voice, design system (always loaded)
execution/          Python scripts (deterministic tools — how to do it)
app/                FastAPI application (webhook handler, AI engine, database)
prompts/            Per-client salonConfig JSON files (one per salon)
.tmp/               Intermediate files, always regenerable, never commit
.env                API keys: META_ACCESS_TOKEN, OPENAI_API_KEY, TWILIO_*, GOOGLE_*
credentials.json    Google OAuth credentials (in .gitignore)
token.json          Google OAuth token (in .gitignore)
```

---

## Floux Skills (the 4 core SOPs)

| Skill | When to use |
|-------|-------------|
| `.claude/Skills/missed-call-recovery/SKILL.md` | Incoming Twilio webhook for a missed call |
| `.claude/Skills/whatsapp-conversation/SKILL.md` | Incoming WhatsApp reply from a client |
| `.claude/Skills/book-appointment/SKILL.md` | When booking_data is complete and slot is confirmed |
| `.claude/Skills/onboard-salon/SKILL.md` | Setting up a new salon client |

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

You sit between human intent (skills) and deterministic execution (Python scripts). The relevant skill auto-loads, you make decisions, call the right scripts, handle errors, continuously improve the system.

Be pragmatic. Be reliable. Self-anneal.
