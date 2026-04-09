# Website Improver — Master Orchestration

Runs a 4-wave debate loop where specialized agents audit `index.html`, debate improvements, reach a consensus, and an executor makes approved changes. Max approves before anything goes live.

---

## Prerequisites — Read First

```
.agents/product-marketing-context.md
2. `.agents/senior-cmo-knowledge.md` — 30 elite marketing frameworks (Ogilvy, Hormozi, Schwartz, Cialdini, Dunford, StoryBrand, JTBD, loss aversion, luxury positioning, WhatsApp data). Read Part 1-5. Think like a Senior CMO, not an auditor.
.claude/rules/design-system.md
index.html
```

---

## Site URL (Chrome MCP)

```
file:///Users/maxherman/Desktop/Floux%20Project/index.html
```

## Screenshot Sequence (all agents use this)

Open the site, then take screenshots at these scroll positions. Save to `.agents/outputs/website-improver/screenshots/[agent]-[section].png`:

| Section | Scroll Y | Content |
|---------|----------|---------|
| hero | 0 | Full hero, headline, CTAs |
| como | 800 | Cómo funciona — 3 cards |
| statement | 1600 | Promise section + CTA |
| porque | 2400 | Por qué Floux — 4 image cards |
| precios | 3400 | Pricing table — 3 tiers |
| historia | 4400 | Founder + stats row |
| faqs | 5200 | FAQ accordion |
| contacto | 6000 | Contact form |

---

## WAVE 1 — Parallel Audits (no dependencies)

Run all 4 agents simultaneously. Each reads `index.html` + takes screenshots + applies their skills.

```
[SEO Agent]     → .agents/marketing-team/website-improver/agents/SEO_AGENT.md
[CRO Agent]     → .agents/marketing-team/website-improver/agents/CRO_AGENT.md
[Copy Agent]    → .agents/marketing-team/website-improver/agents/COPY_AGENT.md
[Pricing Agent] → .agents/marketing-team/website-improver/agents/PRICING_AGENT.md
```

**Done when:** 4 files exist in `.agents/outputs/website-improver/audits/`
- `seo-findings.md`
- `cro-findings.md`
- `copy-findings.md`
- `pricing-findings.md`

---

## WAVE 2 — Debate (sequential, after Wave 1)

Strategy agent reads all 4 audit files and writes `DEBATE.md`.

**Format per change:**
```markdown
## Change #N: [Element — e.g., "Hero headline"]

**SEO position:** [finding + recommendation]
**CRO position:** [finding + recommendation]
**Copy position:** [finding + recommendation]
**Pricing position:** [finding + recommendation — skip if not relevant]

**Conflict:** Yes / No
**If yes:** [describe the disagreement]
**Resolution:** [which position wins and why, or synthesis of both]
**Priority:** P1 (this cycle) / P2 (next cycle) / P3 (future)
```

Save to: `.agents/outputs/website-improver/debate/DEBATE.md`

---

## WAVE 3 — Consensus Proposal (sequential, after Wave 2)

Strategy agent reads `DEBATE.md` and produces `CONSENSUS.md`. This is what Max reviews.

**Format:**
```markdown
# Website Improvement Consensus — [Date]
## Status: AWAITING MAX APPROVAL

---

### P1 Changes — Implement This Cycle

#### Change 1: [Title]
**Section:** [hero / pricing / contact / etc.]
**Element:** [h1 / p / button / meta tag / stat / etc.]
**Skill justification:** [which skill + which principle]
**Old:** `[exact current text from index.html]`
**New:** `[exact proposed replacement]`
**Why:** [1-2 sentences, data-backed where possible]
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

#### Change 2: [Title]
[same format]

---

### P2 Changes — Next Cycle
[same format, less detail]

### P3 Changes — Future
[brief bullet list only]
```

Save to: `.agents/outputs/website-improver/consensus/CONSENSUS.md`

**STOP HERE. Do not proceed to Wave 4 until Max has marked decisions in CONSENSUS.md.**

---

## WAVE 4 — Execution (only after Max approval)

Executor reads `CONSENSUS.md`, filters for `[x] Approve` items, then edits `index.html`.

### Executor Safety Rules

1. Read `index.html` fully before any edit
2. Read `.claude/rules/design-system.md` before any edit
3. Use `Edit` tool only — never full file rewrite
4. Make one change at a time, in P1 priority order
5. After each edit: confirm the changed text is correct
6. **Never change:** CSS variables, font families, border-radius, layout structure, JS logic
7. **Only change:** copy text, meta tags, button labels, stat numbers, aria-labels, alt text
8. Log every applied change to `.agents/outputs/website-improver/changesets/YYYY-MM-DD.md`

**Changeset log format:**
```markdown
# Changeset — [Date]

## Applied Changes

### 1. [Change title]
**Element:** [selector or description]
**Old:** `[text]`
**New:** `[text]`
**Applied:** [timestamp]
```

---

## Trigger Commands for Max

**Full cycle (audit → debate → consensus):**
```
Run the Floux website improvement cycle.
Read .agents/marketing-team/website-improver/INSTRUCTIONS.md.
Open index.html via Chrome MCP at file:///Users/maxherman/Desktop/Floux%20Project/index.html
Take screenshots of all 8 sections. Then run Wave 1 (all 4 agents in parallel), Wave 2 (debate), Wave 3 (consensus). Stop and wait for my approval before Wave 4.
```

**Single agent only:**
```
Run only the [SEO/CRO/Copy/Pricing] agent audit on the Floux website.
Read .agents/marketing-team/website-improver/agents/[AGENT_FILE].md
Save findings to .agents/outputs/website-improver/audits/[agent]-findings.md
```

**Execute approved changes:**
```
Execute the approved P1 changes from .agents/outputs/website-improver/consensus/CONSENSUS.md
Follow the Executor Safety Rules in .agents/marketing-team/website-improver/INSTRUCTIONS.md
Edit index.html using Edit tool only, one change at a time.
```
