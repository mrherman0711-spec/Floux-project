# Floux

**AI-powered WhatsApp booking agent that recovers missed calls for beauty salons in Madrid, Spain.**

Floux answers the calls a small salon can't. When a call goes unanswered, Floux detects it, opens a WhatsApp conversation with the caller, understands what they want in natural Spanish or English, checks real availability, and books the appointment — no human in the loop.

This repo is the whole system: the production backend, the multi-agent GTM tooling that finds and onboards new salons, and the operating structure (skills/agents/rules) that lets Claude Code run most of the business end to end.

---

## What it does (end to end)

```
Missed call (Twilio) → respond 200 → normalize phone → filter no-answer/busy
  → dedupe by CallSid → WhatsApp greeting (Meta Cloud API)
  → AI conversation (GPT-4o-mini, bilingual, auto-detects ES/EN)
  → collect service + datetime + name + staff preference
  → check availability: Treatwell → Booksy → Google Calendar (fallback)
  → book appointment + assign staff
  → confirm to client + notify salon owner
```

Hard constraints the agent enforces on every conversation: never invent a service, price, or open slot that isn't in the salon's config; never say "AI", "bot", or "robot" to a customer; always reply in the language the customer used; always respond to Twilio within 15s before doing anything else; always dedupe retried webhooks by `CallSid`.

## Architecture

| Layer | Location | Purpose |
|---|---|---|
| **Backend** | [`app/`](app/) | FastAPI webhook handler, AI conversation engine, session DB, WhatsApp client, scheduler |
| **Deterministic tools** | [`execution/`](execution/) | Scripts agents call instead of writing inline code: booking, availability checks, phone normalization, session management, Google/Sheets auth, prospecting, email sending |
| **Skills (SOPs)** | [`.claude/Skills/`](.claude/Skills/) | Procedures Claude Code follows on demand — missed-call handling, WhatsApp conversation flows, salon onboarding, prompt engineering, Twilio setup |
| **Agents** | [`.claude/agents/`](.claude/agents/) | Specialized subagents for GTM, market/competitive research, client health monitoring, code review, test generation, bookkeeping |
| **Rules** | [`.claude/rules/`](.claude/rules/) | Brand voice and design-system constraints, always loaded |
| **Salon configs** | [`prompts/`](prompts/) | Per-client config (services, prices, staff, hours) — the only source of truth the agent is allowed to speak from |
| **Reference docs** | [`FLOUX_SOP.md`](FLOUX_SOP.md), [`AGENTS.md`](AGENTS.md) | Operating SOP and the 3-layer architecture writeup |

## The GTM automation (Dream 100 pipeline)

A 4-stage subagent pipeline turns "a neighborhood in Madrid" into a fully-personalized sales outreach batch, with no manual research:

1. **`dream100-prospector`** — pulls salons from Google Maps, scores fit 1–10 against the ICP
2. **`dream100-researcher`** — OSINT pass per prospect (reviews, Instagram, Treatwell/Booksy) → one specific hook per lead
3. **`dream100-outreach`** — writes the WhatsApp / email / in-person script personalized to that hook, plus follow-ups
4. **`dream100-deliverable`** — builds a working demo (real salon config + sample conversation) as the "free work upfront" sent to the owner

Run end to end via the `dream100` orchestrator agent, or any stage standalone. Output lands as CSV/DOCX — never raw markdown — because these are call sheets Max uses operationally, not docs.

## Other agents in production

- **`client-success`** — monitors live salons for churn risk, upsell opportunities, and setup drift
- **`market-analyst` / `competitive-analyst`** — Spain beauty-salon market sizing and competitor tracking
- **`code-reviewer`** — audits `app/`/`execution/` for race conditions and webhook-retry hazards specific to this pipeline
- **`test-writer`** — generates pytest coverage for the booking/cancellation/rescheduling flows
- **`accountant`** — tracks Floux's own operating spend in a structured ledger

## Stack

Claude Code (orchestration + all business logic) · Twilio (call detection) · Meta WhatsApp Cloud API (messaging) · OpenAI GPT-4o-mini (conversation, `response_format: json_object`) · SQLite (session state) · Google Sheets (owner-facing visibility) · Google Calendar (booking fallback) · Chrome DevTools MCP (Treatwell/Booksy browser automation) · FastAPI on Railway (24/7 webhook host)

## Notes on this repo

- `claude-seo/`, `codex-plugin-cc/`, `.claude/Skills/superpowers`, `.agents/marketingskills` are third-party tools wired in as git submodules (not this project's own code) — kept out of the main tree, properly attributed to their upstream repos.
- `finance/` (internal spend ledger) is excluded — not relevant to the technical build.
- Business/marketing working files (`ads/`, `social-*/`, `brand/`, planning docs) are included as-is since they were produced by the same agent stack described above.
