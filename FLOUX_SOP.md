# FLOUX — Standard Operating Procedures & Company Bible

## 1. COMPANY OVERVIEW

**What is Floux?**
Floux is an AI-powered WhatsApp booking agent for local service businesses in Spain. When a business misses a phone call, Floux sends the customer a WhatsApp message within 30 seconds, has a full AI conversation (in Spanish or English, auto-detected), qualifies the booking, checks real availability in the salon's system (Treatwell, Booksy, or Google Calendar), books the appointment, assigns the correct staff member, and notifies the business owner.

**Official email:** flouxaim@gmail.com
**Brand email:** hello@floux.es
**Positioning:** "Recuperamos los clientes que pierdes cuando no puedes coger el teléfono."
**What Floux is NOT:** An AI receptionist, a booking platform, or a Fresha/Booksy competitor. Floux sits upstream — catches the phone crowd that existing booking tools miss.

**Founded by:** Max, based in west Madrid (Villaviciosa de Odón area), student at Universidad Europea de Madrid.

---

## 2. TARGET MARKET

### V1 — Beauty Salons & Aesthetic Centers (NOW)

**Geography:** Villaviciosa de Odón, Boadilla del Monte, Majadahonda, Pozuelo, Las Rozas — west Madrid suburbs.

**ICP:**
- Centros de estética y belleza, 2-8 employees
- Owner-operated (typically señoras 40-60, Spanish)
- Phone-dependent — many don't have websites
- Already using WhatsApp manually with clients
- Many use Treatwell or Booksy for online bookings (Floux integrates with these)
- Know they lose clients from missed calls but have no solution

**Bilingual support:** Villaviciosa is a university town. Many clients speak English. The AI auto-detects language and responds accordingly. Default is Spanish (castellano).

**Key insight:** Don't cite "40% missed call rate" — no rigorous Spain-specific data. Use the free audit: "¿Cuántas llamadas se te escapan a la semana?"

### V2 — Real Estate Agencies (after case studies)
Core: Missed call → AI lead qualification | Extra: Lead nurturing drip | Price: €247/month

### V3 — Clinics / Dental (with track record)
Core: Missed call → AI booking | Extra: No-show reduction | Price: €147/month

---

## 3. PRODUCT ARCHITECTURE

### Tech Stack
| Component | Tool | Notes |
|-----------|------|-------|
| Build everything | Claude Code | Replaces n8n — all logic built in code |
| Phone/SMS | Twilio | Missed-call detection + WhatsApp messaging |
| Messaging | WhatsApp Business API | ✅ Already have API access |
| AI brain | OpenAI GPT-4o-mini | Conversation + intent classification |
| Data (V1) | Google Sheets | Logging conversations, tracking leads |
| Booking (if salon uses) | Treatwell / Booksy | Via Chrome DevTools MCP (no API available) |
| Booking (fallback) | Google Calendar | If salon doesn't use Treatwell/Booksy |
| Design/Debug | Claude / Claude Code | Primary development tool |

### V1 Workflow
```
Client calls salon → No answer → Call forwards to Twilio
→ Twilio fires webhook
→ System responds 200 immediately
→ Normalize phone (E.164)
→ Filter: only "no-answer" or "busy"
→ Deduplicate by CallSid
→ Send WhatsApp greeting (language detected from first reply)
→ AI conversation collects: service + datetime + name + staff preference
→ Check availability in salon's system:
  - Treatwell → Chrome DevTools browser automation
  - Booksy → Chrome DevTools browser automation
  - Neither → Google Calendar API
→ Book appointment + assign staff member
→ Send confirmation to client (in their language)
→ Send notification to owner
```

### Treatwell Integration (V1 — MANDATORY)
Treatwell has NO public API. Integration approach:
- Chrome DevTools MCP controls a browser instance
- Navigates to salon's Treatwell dashboard
- Reads calendar for availability
- Books appointments through the UI programmatically
- Same approach for Booksy
- Fallback: Google Calendar for salons without any platform

### Multi-Staff Assignment (V1)
- AI determines which staff members can do the requested service
- Client can express preference ("quiero con María")
- Checks that specific staff member's availability
- If no preference → assigns first available qualified staff
- Booking goes into the correct person's schedule

---

## 4. PRICING

| Tier | Monthly | Setup | Includes |
|------|---------|-------|----------|
| Básico | €47 | €0 | Missed-call WhatsApp only, no AI |
| Agente | €97 | €197 | Full AI booking agent + staff assignment + Treatwell/Booksy integration + owner notifications |
| Completo | €147 | €297 | Tier 1 + review automation + reminders |

**Cost per client:** €18-28/month | **Margins:** 70-85% | **Breakeven:** 2-3 clients

---

## 5. COMPETITIVE LANDSCAPE

~20-30 AI agencies in Spain. Key: Bookline (Barcelona, hospitality), HydrAI Labs (Marbella, €297/mo), Ario (Madrid, €297/mo). **ZERO competitors with physical presence in west Madrid.** The real competitor is inertia — señoras doing nothing.

---

## 6. SALES APPROACH

**Rules:** Sell pain not tech. Never say "IA" in first conversation. Never compare to receptionist. Target: "¿Cuántas llamadas se te escapan a la semana?"

**Discovery Questions:** (1) Calls per day? (2) What happens when busy? (3) Ever lost a client from missed call? (4) Use WhatsApp? (5) Online booking system? (6) What would recovering those calls be worth? (7) How many staff / who does what?

**Sales Script Skill:** NOT yet built — deferred until first 3-5 real salon conversations.

---

## 7. FINANCIAL MODEL

| Clients | Revenue | Profit | Milestone |
|---------|---------|--------|-----------|
| 3 | €291 | ~€210 | Covers autónomo |
| 10 | €970 | ~€700 | Living basics |
| 25 | €2,425 | ~€1,750 | Full-time viable |
| 50 | €4,850 | ~€3,500 | First salesperson |

Scaling (month 6+): Commission-based salesforce — 20% MRR first 12 months, then 5%.

---

## 8. LEGAL & TAX (SPAIN)

Register as autónomo BEFORE first invoice. Tarifa plana: €80/month (12 months). Quarterly: Modelo 303 (IVA) + Modelo 130 (IRPF). Hire gestoría €50-80/month. RGPD: privacy policy needed for WhatsApp data processing.

---

## 9. ACCOUNTS STATUS

| Account | Status |
|---------|--------|
| Meta Business | ✅ Created ("Floux" portfolio) |
| Twilio | ✅ Created (trial credit) |
| WhatsApp Business API | ✅ Ready |
| OpenAI | ✅ Available |
| Gmail (flouxaim@gmail.com) | ✅ Active |
| Google Workspace | ⬜ Sheets + Calendar needed |
| Autónomo | ⬜ Before first client payment |
| Domain (floux.es) | ⬜ Website not built yet |

---

## 10. CLAUDE CODE WORKSPACE

```
floux-project/
├── .claude/
│   ├── CLAUDE.md
│   └── skills/
│       ├── prompt-engineer/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       ├── generate_prompt.py
│       │       └── test_prompt.py
│       ├── whatsapp-booking-agent/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── check_availability.py
│       ├── twilio-integration/
│       │   └── SKILL.md
│       └── research-agent/
│           ├── SKILL.md
│           └── scripts/
│               └── research_prospect.py
├── future/
│   └── google-calendar-ops.md
├── prompts/
│   └── (per-client prompt configs as JSON)
└── docs/
    └── FLOUX_SOP.md
```

### Claude Code Principles
1. Plan before building (shift-tab for plan mode)
2. Task → Execute → VERIFY → Correct → Iterate
3. CLAUDE.md = ship's trajectory — concise, dense, guardrails at top
4. Skills = SKILL.md orchestrator + scripts/ folder (only output enters context)
5. MCP for exploration → convert to skills for production
6. Subagents for parallelization and context separation
7. /clear, /compact, /cost for context hygiene
8. Screenshot-compare loop for web design
9. Voice dictation → compress before sending
10. Security: human reviews all auth, payments, user data

### Prompt Engineering (Anthropic Official)
- Use XML tags: <instructions>, <context>, <examples>, <output_format>
- Give role in system prompt (one line)
- 3-5 examples in <example> tags
- response_format: json_object for structured outputs
- Tell what TO DO not what NOT to do
- Longform context at top, query at bottom
- Be explicit about desired actions ("book it" not "can you suggest")
