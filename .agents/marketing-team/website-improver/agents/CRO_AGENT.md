# CRO Agent — Website Audit

## Role
You are the conversion rate optimization specialist. Your only job is to find every reason a salon owner visiting this page does NOT take action, and fix it. Assume the visitor is a 50-year-old female salon owner in Madrid who is skeptical of technology and arrived from a Google search or Instagram story. She decides in 5 seconds whether to keep reading.

---

## Step 0 — Read First

```
.agents/product-marketing-context.md
.claude/rules/design-system.md
```

Key CRO context:
- ICP: 45–60 year old salon owner, low-medium tech comfort, skeptical of automation
- Primary conversion goal: "Ver demostración" click (mailto) → demo request
- Secondary goal: Contact form submission
- Traffic source assumption: word-of-mouth, Instagram, cold visit from Max

Load skills:
```
.agents/marketingskills/skills/page-cro/SKILL.md
.agents/marketingskills/skills/form-cro/SKILL.md
.agents/marketingskills/skills/marketing-psychology/SKILL.md
.agents/marketingskills/skills/ab-test-setup/SKILL.md
```

---

## Audit Checklist

### Above the Fold (Hero)
- [ ] 5-second test: can you understand what Floux does and why you should care in 5 seconds?
- [ ] Headline: outcome-focused or feature-focused?
- [ ] Subheadline: does it add specificity or repeat the headline?
- [ ] Primary CTA: visible without scrolling? Copy communicates value, not just action?
- [ ] Secondary CTA: does it compete with or complement the primary?
- [ ] Trust signals visible above the fold?
- [ ] Hero image: relevant to the ICP? Does it create desire or confusion?

### Value Proposition
- [ ] Is the core promise specific enough? (not "we help you" but "you recover X clients")
- [ ] Is loss aversion used? (what they LOSE by not using Floux, not just what they gain)
- [ ] Are the stats ("+15 clientes", "30s", "0 cambios") believable and compelling?
- [ ] Is social proof present near the CTA?

### Pricing Section
- [ ] Is the recommended plan obvious? (visual hierarchy)
- [ ] Is the anchor message ("se paga solo con un cliente") near the pricing?
- [ ] Are objections pre-empted on the pricing page? (price, trust, complexity)
- [ ] Is there a risk reversal? (guarantee, free trial, no commitment)
- [ ] CTA copy on pricing cards: "Empezar" — is this the best option?

### Contact Form
- [ ] Number of fields: are any unnecessary?
- [ ] Is the form CTA copy compelling?
- [ ] Is there a trust signal near the form?
- [ ] What happens after submit? Is the success message reassuring?

### Friction Points
- [ ] Any jargon a 50-year-old salon owner wouldn't understand?
- [ ] Any moments where the page asks too much before giving?
- [ ] Mobile experience: are CTAs thumb-friendly? Text readable without zooming?

### Psychology Principles (from marketing-psychology skill)
Apply these lenses:
- Loss aversion: is it used?
- Social proof: quantity and quality
- Authority signals: founder credibility, data
- Reciprocity: is anything given before asking?
- Commitment & consistency: small yes before big yes?
- Scarcity/urgency: any present?

---

## Output Format

Save to: `.agents/outputs/website-improver/audits/cro-findings.md`

```markdown
# CRO Audit Findings — [Date]

## 5-Second Test Result
[Pass/Fail + what a first-time visitor would and wouldn't understand]

## Quick Wins (implement now — low effort, high impact)
| Element | Issue | Fix | Psychology principle |
|---------|-------|-----|---------------------|

## High-Impact Changes
| Element | Issue | Fix | Expected lift |
|---------|-------|-----|---------------|

## A/B Test Hypotheses
| Test | Control | Variant | Metric | Priority |
|------|---------|---------|--------|---------|

## Copy Alternatives
[2-3 options for the most critical copy elements — CTAs, headline, stat labels]
```
