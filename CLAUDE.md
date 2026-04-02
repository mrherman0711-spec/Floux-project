# Floux

AI-powered WhatsApp booking agent for beauty salons in west Madrid, Spain.
Brand email: hello@floux.es

## Stack
Claude Code (all logic) · Twilio (phone + WhatsApp) · WhatsApp Business API · OpenAI GPT-4o-mini · Google Sheets (logging) · Chrome DevTools MCP (Treatwell/Booksy browser automation) · Google Calendar (fallback booking)

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

## Treatwell / Booksy Integration
- NO public API — use Chrome DevTools MCP for browser automation
- Read calendar → check availability → book through UI programmatically
- Fallback: Google Calendar API for salons without either platform

## Multi-Staff Assignment
- AI determines which staff can do the requested service
- Respect client preference ("quiero con María") → check that person's availability
- No preference → assign first available qualified staff

## Website (index.html)
- Design: Four Seasons aesthetic — dark charcoal (#1A1714), gold (#9A7B4F), cream (#F2EDE6)
- Fonts: Cormorant Garamond (headings) + Inter (body)
- Contact: flouxaim@gmail.com
- Sections: Hero, Cómo funciona, Por qué Floux, Precios, Nuestra historia, FAQs, Contacto

## Build Philosophy
1. Plan before building (shift-tab for plan mode)
2. Task → Execute → VERIFY → Correct → Iterate
3. After any flow change: test 3+ simulated conversations before deploying
4. /clear when switching tasks, /compact when context heavy

## What NOT to include in skills
- Generic API docs Claude already knows (Twilio, OpenAI, Calendar)
- Tutorial steps ("Go to Console → Click X")
- Content Claude would generate identically without the reference

## Architecture (DO Framework)
See AGENTS.md for full instructions. Short version:
- `directives/` = SOPs (what to do) — read before acting on any task
- `execution/` = Python scripts (how to do it) — call these instead of doing things inline
- Claude = orchestrator between directives and execution
- Self-anneal: fix script → test → update directive with learning

## Rules
See .claude/rules/ for brand voice, design system, page structure, deployment.
