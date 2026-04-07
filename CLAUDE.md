# Floux

AI-powered WhatsApp booking agent for beauty salons in west Madrid, Spain.
Brand email: flouxaim@gmail.com

## Stack
Claude Code (all logic) · Twilio (voice/missed-call detection) · Meta WhatsApp Cloud API (messaging) · OpenAI GPT-4o-mini · SQLite (sessions) · Google Sheets (owner visibility) · Chrome DevTools MCP (Treatwell/Booksy browser automation) · Google Calendar (fallback booking)

## V1 Flow
Missed call → Twilio webhook → respond 200 → normalize phone → filter no-answer/busy → deduplicate by CallSid → WhatsApp greeting → AI conversation (bilingual, auto-detect) → collect service/datetime/name/staff preference → check availability (Treatwell → Booksy → Google Calendar) → book appointment + assign staff → confirm to client + notify owner

## Hard Rules
- Customer-facing messages: SPANISH default, English if client writes in English (auto-detect)
- NEVER say "inteligencia artificial", "IA", "bot", or "robot" to customers
- NEVER invent services, prices, or availability — only use what's in client config
- NEVER compare Floux to a receptionist (triggers defensive reaction from owners)
- Respond 200 MUST be first action after any Twilio webhook (15s timeout)
- Deduplicate by CallSid always — Twilio retries failed webhooks
- Phone format: E.164 (+34XXXXXXXXX)
- Timezone: Europe/Madrid in all date handling
- OpenAI calls: always use response_format: json_object
- Positioning: "Recuperamos los clientes que pierdes cuando no puedes coger el teléfono"

## Architecture

| Layer | Location | Purpose |
|-------|----------|---------|
| Skills (SOPs) | `.claude/Skills/` | 9 Skills with YAML frontmatter — auto-loaded by trigger match |
| Agents | `.claude/agents/` | 6 subagents — invoke for specialized tasks |
| Rules | `.claude/rules/` | 2 rules (brand-voice, design-system) — always loaded |
| Execution | `execution/` | 8 Python scripts — deterministic tools, call these instead of inline code |
| App | `app/` | FastAPI webhook handler, AI engine, database, WhatsApp client, scheduler |
| Configs | `prompts/` | Per-salon salonConfig JSON files |
| Reference | `FLOUX_SOP.md` | Comprehensive operational SOP (read-only) |
| Reference | `AGENTS.md` | 3-layer architecture docs + script reference |

## Skills Index

| Skill | When to use |
|-------|-------------|
| book-appointment | Execute confirmed booking on platform |
| missed-call-recovery | Process Twilio missed-call webhook |
| onboard-salon | New salon client setup end-to-end |
| whatsapp-conversation | Handle inbound WhatsApp message webhook |
| prompt-engineer | System prompts, intent classifiers, datetime parsers |
| booking-engine | Webhook handler, session manager, backend logic |
| twilio-integration | Twilio webhooks, WhatsApp delivery, TwiML |
| whatsapp-booking-agent | Conversation flows, edge cases, dialogue UX |
| agentic-workflow-principles | Architecture decisions, agent loop design |
| chrome-devtools-mcp | Browser automation — scraping, screenshots, UI research, Treatwell/Booksy |

## Agents

| Agent | Purpose |
|-------|---------|
| prospector | Find and score salon leads in west Madrid |
| market-analyst | Market sizing, trends, opportunities |
| competitive-analyst | Competitor tracking and positioning |
| sales-coach | Scripts, objection handling, pitch optimization |
| client-success | Monitor salon health, churn risk, upsells |
| code-reviewer | Audit race conditions and reliability bugs |

## Build Philosophy
1. Plan before building (shift-tab for plan mode)
2. Task → Execute → VERIFY → Correct → Iterate
3. Check `execution/` before writing inline code — script probably exists
4. Self-anneal: fix script → test → update skill with learning
5. After any flow change: test 3+ simulated conversations before deploying
6. /clear when switching tasks, /compact when context heavy

## Rules
See `.claude/rules/` for brand voice and design system.
