---
name: agentic-workflow-principles
description: "Core principles for building Floux as an agentic system — not a chatbot. Use when designing the booking engine architecture, planning agent loops, managing session memory, building tools for Treatwell/Booksy automation, or deciding how to structure multi-step autonomous tasks."
allowed-tools:
  - Bash
  - Write
  - Read
---

# Agentic Workflow Principles — Applied to Floux

## The Core Distinction: Chatbot vs Agent

Floux is NOT a chatbot. It is an agent.

| Chatbot | Agent (Floux) |
|---------|--------------|
| Answers questions | Takes actions |
| Waits for human to act | Books the appointment itself |
| Copy-paste output | Writes to Treatwell/Booksy/Calendar |
| Bounded by the chat window | Interacts with real systems |

The missed-call → WhatsApp message → AI conversation → booking confirmation loop is a full agentic workflow. Every step must result in a real-world action, not just text output.

## The Agent Loop (PTMRO)

Every time Floux processes a WhatsApp message, it runs this loop internally:

1. **Planning** — break the client's message into what's needed: service? datetime? name? staff?
2. **Tools** — fetch availability from Treatwell/Booksy/Calendar; send WhatsApp via Twilio
3. **Memory** — load session state (conversation history, booking_data collected so far)
4. **Reflection** — does the response make sense? is the slot actually free? did I invent anything?
5. **Orchestration** — is this a single-step reply or do I need to trigger a subagent (e.g. booking executor)?

Claude runs this loop on every turn. The system prompt and session object are the scaffolding that makes it reliable.

## Planning is the Highest-ROI Human Input

From the course: *"If there was one place to exert your human intellect, it's at the planning stage."*

For Floux this means: **design the flow and edge cases yourself, then let Claude execute.**

- Design the conversation states (greeting → collecting → confirming → booked) before building
- Map every edge case (voice note, angry client, unknown service, English speaker) before prompting
- Define the exact JSON schema the AI must return before writing the system prompt
- Do NOT let the AI design the flow — it makes foundational errors that compound

Bad planning = small error at start → massive drift by end of conversation.

## Tools are Floux's Hands

The AI brain (GPT-4o-mini) can reason but cannot act. Tools are what make it real:

| Tool | What it does |
|------|-------------|
| Twilio send_whatsapp | Delivers messages to the client |
| Chrome DevTools MCP | Reads/writes Treatwell and Booksy UIs |
| Google Calendar API | Fallback booking for salons without a platform |
| Google Sheets write | Logs sessions, tracks leads |
| Session manager | Loads and saves conversation state by phone number |

Rule: **every tool must have a consistent input/output contract.** Probabilistic AI + inconsistent tools = unreliable system. Define exact input/output schemas for each tool before building.

## Memory Architecture for Floux

Agents have 3 types of memory. Floux uses all three:

| Type | Where stored | What it holds |
|------|-------------|--------------|
| Short-term | OpenAI context window | Current conversation messages |
| Mid-term | Session object (Google Sheets row) | booking_data, language, status across turns |
| Long-term | salonConfig JSON | Salon's services, staff, schedule, platform — never changes per session |

Session object is the critical one. Without it, the AI has no memory between WhatsApp messages. Always load session → append message → call AI → save session.

## Reliability over Flexibility

LLMs are probabilistic. Business requires reliability. The solution: constrain the AI with tools and structured output.

- `response_format: json_object` on every OpenAI call — no free-text responses ever
- Fixed JSON schema with defined fields: `reply`, `intent`, `booking_data`, `escalate`, `conversation_complete`
- AI can only output what the schema allows — anything else is a parsing error to catch and retry
- Tools handle the actual actions — AI just decides WHAT to do, tools handle HOW

## Horizontal Leverage — the Floux Scaling Model

From the course: *"Automating most of many roles is more valuable than automating all of one."*

For Floux: one instance of the booking agent can handle:
- Incoming WhatsApp from client A (collecting service)
- Confirmation send to client B (booking complete)
- Escalation alert to owner for client C (angry message)
- All simultaneously, across multiple salons

This is why the multi-salon architecture matters: salonConfig is loaded dynamically per phone number. Same codebase serves 50 salons. Each salon = pure margin.

## Self-Healing: What to Build In

Good agentic workflows recover from errors without human intervention:

| Failure | Recovery |
|---------|---------|
| OpenAI returns invalid JSON | Retry once with stricter prompt; escalate to owner on 2nd failure |
| Treatwell slot unavailable after booking attempt | Offer next 2 available slots, do not confirm the failed one |
| Twilio delivery failure | Log error, retry once after 60s |
| Session not found for phone number | Create new session, treat as fresh conversation |
| Chrome DevTools MCP loses browser session | Re-navigate from login; log incident |

Build these recovery paths before going live. They WILL happen.

## DO Framework Applied to Floux

**3-layer architecture — never collapse these layers:**

| Layer | What | Files |
|-------|------|-------|
| Directive | SOPs — what to do | `directives/*.md` |
| Orchestration | Claude — decision-making, routing, error handling | (this agent) |
| Execution | Python scripts — deterministic actions | `execution/*.py` |

**File structure:**
```
directives/               # SOPs (read before acting on any task)
  missed_call_recovery.md
  whatsapp_conversation.md
  book_appointment.md
  onboard_salon.md
execution/                # Deterministic Python scripts
  normalize_phone.py      # E.164 normalization
  manage_session.py       # load/save/expire sessions (Google Sheets)
  send_whatsapp.py        # send via Twilio API
  check_availability.py   # fetch slots from Treatwell/Booksy/Calendar
  book_appointment.py     # execute booking
  read_sheet.py           # read Google Sheets
  append_to_sheet.py      # append rows to Google Sheets
  update_sheet.py         # batch update Google Sheets
prompts/                  # Per-client salonConfig JSON (one per salon)
.tmp/                     # Intermediates — never present to user
```

**Operating rules:**
- Check `execution/` before writing any code inline — script probably already exists
- Claude does NOT normalize phones itself — runs `normalize_phone.py`
- Claude does NOT query Sheets itself — runs `read_sheet.py`
- Claude does NOT book on Treatwell itself — reads `directives/book_appointment.md` and runs `book_appointment.py`

**Self-annealing loop when something breaks:**
1. Fix the script
2. Test it runs cleanly
3. Update the directive with the new learning
4. System is now stronger

## Key Principle: Build Tools First, Prompt Second

From the course: *"The entire point of the intelligence is to help it use and build tools."*

For Floux build order:
1. Build `execution/` scripts (normalize_phone, manage_session, send_whatsapp, check_availability, book_appointment) ✓ done
2. Build session manager (load/save state by phone) ✓ done
3. Build availability fetcher (Chrome DevTools MCP → Treatwell/Booksy)
4. Build booking executor (Chrome DevTools MCP → submit booking)
5. THEN write the system prompt that orchestrates all of the above

A great prompt with broken tools = broken agent. Solid tools with a decent prompt = working agent.
