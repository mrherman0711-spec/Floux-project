# Floux Marketing Team — Orchestrator

This file defines the run order, trigger sequences, dependency graph, and done criteria for all 7 marketing agents. Read this before invoking any agent.

---

## Agent Registry

| # | Agent | Folder | Specialty | Run Type |
|---|-------|--------|-----------|----------|
| 1 | SEO & Content | `seo-content/` | Organic search, content production | Daily + Weekly |
| 2 | CRO | `cro/` | Conversion optimization, A/B tests | Daily + Weekly |
| 3 | Content & Copy | `content-copy/` | All written assets, brand voice | Daily + Weekly |
| 4 | Paid & Measurement | `paid-measurement/` | Ad campaigns, analytics, attribution | Daily + Weekly |
| 5 | Growth & Retention | `growth-retention/` | Client health, churn, referral | Daily + Weekly |
| 6 | Sales & GTM | `sales-gtm/` | Visit briefs, demo, pipeline | Daily + Weekly |
| 7 | Strategy | `strategy/` | Cross-agent synthesis, Max's brief | Daily + Weekly |

---

## Dependency Graph

```
                    ┌─────────────────────────────────────────┐
                    │    .agents/product-marketing-context.md  │
                    │         (ALL agents read first)          │
                    └──────────────────┬──────────────────────┘
                                       │
          ┌──────────┬─────────────────┼──────────────┬────────────┐
          ▼          ▼                 ▼              ▼            ▼
    ┌──────────┐ ┌──────────┐   ┌──────────┐  ┌──────────┐ ┌──────────┐
    │   SEO    │ │   CRO    │   │  Paid &  │  │ Growth & │ │ Sales &  │
    │ Content  │ │          │   │  Measmt  │  │Retention │ │   GTM    │
    └────┬─────┘ └────┬─────┘   └────┬─────┘  └────┬─────┘ └────┬─────┘
         │            │              │              │             │
         │            └──────┬───────┘              │             │
         │                   ▼                      │             │
         └──────────► ┌──────────┐ ◄────────────────┘             │
                      │ Content  │ ◄──────────────────────────────┘
                      │  & Copy  │
                      └────┬─────┘
                           │
                           ▼
                      ┌──────────┐
                      │ Strategy │ ◄── reads ALL agent outputs
                      └────┬─────┘
                           │
                           ▼
                          MAX
```

**Parallel (no dependencies, run simultaneously):**
- SEO & Content + CRO + Paid & Measurement + Growth & Retention + Sales & GTM

**Sequential (depends on upstream output):**
- Content & Copy runs AFTER SEO, CRO, Paid & Measurement, Sales & GTM have produced drafts
- Strategy runs AFTER all 6 other agents have submitted weekly outputs

---

## Daily Trigger Sequence

**Trigger:** Every day at start of session (Monday–Saturday)

### Wave 1 — Parallel (no dependencies)
Run simultaneously:

```
[seo-content]     → daily task checklist
[cro]             → daily task checklist
[paid-measurement]→ daily task checklist
[growth-retention]→ daily task checklist (client health check first)
[sales-gtm]       → daily task checklist (visit briefs for today's salons)
```

**Done criteria for Wave 1:**
- [ ] `seo-content`: keyword-log.md updated, content-backlog.md has at least 1 new entry
- [ ] `cro`: friction-log.md updated (or noted "no new field notes"), hypothesis-backlog.md has 1 new entry
- [ ] `paid-measurement`: conversion-log.md updated with today's events
- [ ] `growth-retention`: client-health.md overwritten with today's scores; Red interventions drafted if any
- [ ] `sales-gtm`: visit briefs created for all salons on today's list; pipeline.md updated

### Wave 2 — Sequential (depends on Wave 1)
Run after Wave 1 is complete:

```
[content-copy]    → daily inbox review: edit any draft copy flagged by Wave 1 agents
```

**Done criteria for Wave 2:**
- [ ] `content-copy`: all pending drafts from `.agents/outputs/` reviewed and returned with `-edited.md` suffix or approved

### Wave 3 — Sequential (depends on Wave 2)
Run after Wave 2 is complete:

```
[strategy]        → signal scan; check for blockers across all output folders
```

**Done criteria for Wave 3:**
- [ ] `strategy`: signal-log.md updated; blockers.md updated (or confirmed empty); any urgent flags surfaced to Max immediately

---

## Weekly Trigger Sequence

**Trigger:** Friday (all agents) + Saturday (Strategy only)

### Friday — Wave 1 (Parallel)
Run simultaneously:

```
[seo-content]     → produce weekly SEO article, update backlog, competitor content gap
[cro]             → run page audit, design A/B test, write weekly report
[paid-measurement]→ produce weekly metrics report, ad creative briefs, campaign brief
[growth-retention]→ client performance summaries, churn risk report, upsell opportunities, success story
[sales-gtm]       → update pipeline, update demo script, update objection doc, write weekly report
```

**Done criteria for Friday Wave 1:**
- [ ] `seo-content/weekly-report.md` overwritten
- [ ] `seo-content/articles/` has 1 new article draft
- [ ] `cro/weekly-report.md` overwritten; 1 audit in `cro/audits/`; 1 A/B test in `cro/ab-tests/`
- [ ] `paid-measurement/weekly-metrics.md` overwritten; 1 campaign brief updated or created
- [ ] `growth-retention/client-reports/` has 1 file per active client; `churn-risk.md` overwritten
- [ ] `sales-gtm/weekly-report.md` overwritten; `pipeline.md` current

### Friday — Wave 2 (Sequential, after Wave 1)
```
[content-copy]    → finalize SEO article, finalize social calendar, produce rotating weekly asset
```

**Done criteria for Friday Wave 2:**
- [ ] `content-copy/weekly-report.md` overwritten
- [ ] Weekly rotating asset saved (web copy / one-pager / outreach / email per cycle)
- [ ] SEO article returned as `[slug]-approved.md`

### Saturday — Wave 3 (Sequential, after all Friday outputs)
```
[strategy]        → read all weekly reports, produce weekly-synthesis.md, produce monday-brief.md
```

**Done criteria for Saturday Wave 3:**
- [ ] `strategy/weekly-synthesis.md` overwritten
- [ ] `strategy/monday-brief.md` overwritten and ready for Max to read Monday morning
- [ ] `strategy/tam-tracker.md` updated
- [ ] Any blockers flagged for Max

### Monday — Wave 0 (Before daily tasks)
```
[sales-gtm]       → produce weekly-visit-plan.md (before Max's first visit)
[strategy]        → monday-brief.md must already be ready (produced Saturday)
```

**Done criteria for Monday Wave 0:**
- [ ] `sales-gtm/weekly-visit-plan.md` ready before 9:00
- [ ] `strategy/monday-brief.md` available for Max to read

---

## Parallel vs. Sequential Rules

| Condition | Rule |
|-----------|------|
| No shared input dependency | Run in parallel |
| Agent B needs Agent A's output | Run A first, then B |
| Agent needs live field data from Max | Wait for Max's notes before running |
| Strategy agent | Always runs last (reads everyone else) |
| Content & Copy | Always runs after SEO, CRO, Sales GTM (edits their drafts) |
| Growth & Retention urgent flag | Run immediately, don't wait for wave |

---

## Context Inheritance Rule

All agents inherit the same ground truth from:

```
.agents/product-marketing-context.md
```

If this file is updated (e.g., new pricing, new ICP data, new objection), all agents automatically pick up the change on their next run. No agent-specific files need to be updated separately.

**Update protocol:** Only Max or the Strategy agent (with Max's approval) may update product-marketing-context.md.

---

## Escalation Flow

```
Agent detects blocker
    ↓
Prepend ⚠️ BLOCKER: to weekly-report.md
    ↓
Strategy agent detects flag during daily signal scan
    ↓
Strategy adds to blockers.md with recommended resolution
    ↓
Max is notified same-day (Strategy surfaces it)
    ↓
Max decides → Strategy updates product-marketing-context.md if needed
    ↓
All agents inherit the update on next run
```

Agents that bypass this flow (surface to Max directly):
- **Growth & Retention:** Red client churn risk (too time-sensitive for chain)
- **Sales & GTM:** Deal ready to close needing custom pricing (immediate revenue decision)
- **Paid & Measurement:** Budget approval needed (financial decision)
