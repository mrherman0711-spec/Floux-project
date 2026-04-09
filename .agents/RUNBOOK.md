# Floux Marketing Team — Runbook

How to operate your 7-agent AI marketing team. Everything you need to trigger, review, update, and manage the system.

---

## System Overview

```
.agents/
├── product-marketing-context.md    ← Single source of truth (all agents read this)
├── marketing-team-playbook.md      ← Team structure overview (reference)
├── marketing-team/
│   ├── ORCHESTRATOR.md             ← Run order, sequences, done criteria
│   ├── seo-content/INSTRUCTIONS.md
│   ├── cro/INSTRUCTIONS.md
│   ├── content-copy/INSTRUCTIONS.md
│   ├── paid-measurement/INSTRUCTIONS.md
│   ├── growth-retention/INSTRUCTIONS.md
│   ├── sales-gtm/INSTRUCTIONS.md
│   └── strategy/INSTRUCTIONS.md
└── outputs/
    ├── seo-content/
    ├── cro/
    ├── content-copy/
    ├── paid-measurement/
    ├── growth-retention/
    ├── sales-gtm/
    └── strategy/

.agents/marketingskills/skills/     ← Skill library (agents load relevant skills)
```

---

## How to Trigger the Full Team

### Daily Run (Monday–Saturday)

Say to Claude:

```
Run the full Floux marketing team daily sequence.
Read .agents/marketing-team/ORCHESTRATOR.md for the run order,
then execute Wave 1 (parallel), Wave 2, and Wave 3 in sequence.
Today's date: [DATE]. Salons to visit today: [LIST or "check sales-gtm pipeline"].
```

Claude will:
1. Read `product-marketing-context.md`
2. Run Wave 1 agents in parallel (SEO, CRO, Paid, Growth, Sales)
3. Run Wave 2 (Content & Copy edits drafts)
4. Run Wave 3 (Strategy scans for blockers)
5. Surface any `⚠️` flags to you before finishing

### Weekly Run (Friday + Saturday)

Say to Claude:

```
Run the full Floux marketing team weekly sequence.
Read .agents/marketing-team/ORCHESTRATOR.md for the weekly trigger sequence.
Today is Friday [DATE]. Run all agents' weekly checklists, then Strategy's Saturday synthesis.
```

### Monday Kickoff

Say to Claude:

```
Good morning. Run the Floux Monday kickoff:
1. Read .agents/outputs/strategy/monday-brief.md and present it to me
2. Run sales-gtm weekly-visit-plan for this week
3. Flag any open blockers from .agents/outputs/strategy/blockers.md
```

---

## How to Trigger a Single Agent

Replace `[AGENT]` with the agent folder name and `[DAILY/WEEKLY]` with the checklist type:

```
Run the Floux [AGENT] agent [DAILY/WEEKLY] checklist.
Read .agents/product-marketing-context.md first.
Then read .agents/marketing-team/[AGENT]/INSTRUCTIONS.md and execute the [DAILY/WEEKLY] task checklist.
Save all outputs to .agents/outputs/[AGENT]/ as specified in the instructions.
```

### Examples

**Run only the Sales & GTM agent for today's visit briefs:**
```
Run the Floux sales-gtm agent daily checklist.
Read .agents/product-marketing-context.md first.
Then read .agents/marketing-team/sales-gtm/INSTRUCTIONS.md.
Today's salons to visit: [Salon Name, Address] and [Salon Name, Address].
Save visit briefs to .agents/outputs/sales-gtm/visit-briefs/
```

**Run only the Growth & Retention agent to check client health:**
```
Run the Floux growth-retention agent daily checklist.
Read .agents/product-marketing-context.md first.
Then read .agents/marketing-team/growth-retention/INSTRUCTIONS.md.
Check the Google Sheets log at [SHEET_URL] for all active clients.
Save health scores to .agents/outputs/growth-retention/client-health.md
```

**Run only Strategy to get Monday brief:**
```
Run the Floux strategy agent weekly synthesis.
Read .agents/product-marketing-context.md first.
Then read all agent weekly reports in .agents/outputs/*/weekly-report.md
Then read .agents/marketing-team/strategy/INSTRUCTIONS.md and produce monday-brief.md.
```

---

## How to Review Outputs

### Daily review (5 minutes)
1. Open `.agents/outputs/strategy/signal-log.md` — any patterns flagged today?
2. Open `.agents/outputs/strategy/blockers.md` — any `⚠️` flags needing your decision?
3. Open `.agents/outputs/sales-gtm/visit-briefs/` — read briefs for today's salons
4. Open `.agents/outputs/growth-retention/client-health.md` — any Red clients?

### Weekly review (30 minutes, Monday morning)
1. Read `.agents/outputs/strategy/monday-brief.md` — your 3 priorities for the week
2. Read `.agents/outputs/sales-gtm/weekly-visit-plan.md` — this week's salon list
3. Scan `.agents/outputs/content-copy/weekly-report.md` — what asset was produced?
4. Review `.agents/outputs/growth-retention/upsell-opportunities.md` — any upsell conversations to have?
5. Check `.agents/outputs/paid-measurement/weekly-metrics.md` — funnel health

### Reviewing a specific asset
All assets are in `.agents/outputs/[agent-folder]/`. File naming convention:
- Dated files: `YYYY-MM-DD-[description].md`
- Living documents: overwritten each cycle (always current)
- Append-only logs: grow over time (full history)

---

## How to Update the Product Marketing Context

All 7 agents inherit their ground truth from one file:

```
.agents/product-marketing-context.md
```

When something changes (new pricing, new objection, new ICP insight, new market data), update this file and all agents automatically pick it up on their next run.

### Update protocol

1. **Identify what changed** — pricing, positioning, ICP, competitive landscape, market data
2. **Edit the file** — find the relevant section and update it precisely; do not add sections not already in the structure
3. **Note the change** — add a comment at the top of the file or in the relevant section: `[Updated YYYY-MM-DD: reason]`
4. **Notify Strategy** — say to Claude:
   ```
   I updated product-marketing-context.md. The change was: [describe change].
   Run the strategy agent signal-log to note this update and flag any agents whose outputs may need to be refreshed.
   ```

### What to update and when

| Event | Section to update |
|-------|------------------|
| Pricing changes | "Pricing" section |
| New objection discovered in field | "Top 3 Objections" section |
| New market data (no-show rate, LTV) | "Market Data" section |
| ICP refinement (new salon type, age range) | "Target Customer" section |
| Competitor moves (Booksy adds feature) | "Competitive Landscape" section |
| New client case study | "Current Clients" section |
| Positioning change | "Positioning" section — requires Max approval |

### What NOT to update here
- Agent-specific task lists → update the agent's `INSTRUCTIONS.md`
- Output file formats → update the agent's `INSTRUCTIONS.md`
- Run sequences → update `ORCHESTRATOR.md`

---

## Troubleshooting

### An agent produced output that contradicts brand voice
→ Run `content-copy` agent with instruction: "Audit [filename] for brand voice violations against product-marketing-context.md"

### An agent's output file is missing
→ Check that the output folder exists: `.agents/outputs/[agent]/`
→ Re-run that agent's daily or weekly checklist in isolation

### Two agents gave conflicting recommendations
→ Run the `strategy` agent with: "Resolve conflict between [agent A] recommendation [X] and [agent B] recommendation [Y]. Read both output files and produce a resolution in blockers.md"

### The product-marketing-context.md feels stale
→ Say: "Run the strategy agent positioning review. Read current product-marketing-context.md against the latest sales-gtm field notes and growth-retention client data. Flag any sections that may need updating."

### A client is at risk of churning
→ Immediately run: `growth-retention` agent intervention task for that client
→ Max sends personal WhatsApp to the owner (human touch, not automated)

---

## Agent Quick Reference

| To do this... | Say this... |
|---------------|-------------|
| Prepare for today's salon visits | Run `sales-gtm` daily checklist with today's salon list |
| Check if clients are healthy | Run `growth-retention` daily checklist |
| Get Monday priorities | Read `strategy/monday-brief.md` |
| Write a new piece of web copy | Run `content-copy` with specific page request |
| Find out what's working in SEO | Run `seo-content` weekly checklist |
| Design an A/B test | Run `cro` weekly checklist |
| See full sales pipeline | Read `sales-gtm/pipeline.md` |
| Get a success story for pitching | Read `growth-retention/success-stories/` |
| Prepare a campaign when budget is ready | Read `paid-measurement/campaign-briefs/` |
| Understand the whole week at once | Run full Strategy weekly synthesis |
