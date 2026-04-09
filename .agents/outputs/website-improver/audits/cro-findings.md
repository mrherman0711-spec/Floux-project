# CRO Audit Findings — 2026-04-08

## 5-Second Test Result

**Result: BORDERLINE PASS (5s) / FAIL (purchase intent)**

A first-time visitor arriving cold from Google or Instagram will understand:
- ✓ "This is about recovering missed calls" (H1 is clear)
- ✓ There's a WhatsApp component (process section subtitle mentions it)
- ✗ Does NOT understand what Floux actually IS in 5 seconds — no definition statement, no "Floux es..."
- ✗ Does NOT know who this is for — "clientes que pierdes" is ambiguous (could be e-commerce, restaurant, any business)
- ✗ No trust signal visible above the fold — no client count, no reviews, no logos
- ✗ No specific outcome stated in hero: "+15 clients/month" is buried 4 scroll depths below
- ✗ Hero subline is missing entirely — there's a headline and 2 CTAs but nothing between them that adds specificity

The 50-year-old salon owner from Chamberí who found this via Instagram does NOT immediately understand "this is for my type of business."

---

## Quick Wins (implement now — low effort, high impact)

| Element | Issue | Fix | Psychology principle |
|---------|-------|-----|---------------------|
| Hero: no subheadline | H1 + immediate CTAs, nothing explaining what/for whom | Add 1-line subhead: "El asistente de WhatsApp para salones de estética en Madrid Oeste" | Specificity → credibility |
| Hero topbar | "Centros de estética · Madrid Oeste · Recuperamos tus llamadas perdidas" — hidden behind transparent header, only visible before scroll | Move key phrase into hero copy block as visible eyebrow/subtitle | ICP recognition — immediate self-selection |
| CTA "Ver demostración" | Good but a mailto link — visitor doesn't know it'll open their email app, not a video | Add `(por email)` or change to "Pide tu demo gratuita" to set expectation | Expectation management → reduces abandonment |
| Secondary CTA "Cómo funciona" | Gold outline — looks equal weight to primary white CTA; two same-prominence CTAs split attention | Make it a text link instead: `↓ Ver cómo funciona` | Attention hierarchy — one dominant CTA |
| Pricing CTA "Empezar" (×3) | Weakest possible CTA — no context, no benefit, no direction | Change to "Quiero este plan" or "Empezar con Agente" for featured card | Action specificity + commitment language |
| Form button "Enviar mensaje" | Functional but generic | Change to "Reservar mi demostración gratuita" | Benefit-focused CTA → higher click rate |
| No trust signal near hero CTA | Nothing: no client count, no neighborhoods, no testimonial | Add below hero CTAs: "Ya confían en Floux salones de Majadahonda, Pozuelo y Las Rozas" | Social proof + local recognition |
| Process section anchor text | "Se paga solo con un único cliente recuperado al mes" — written as a thin lowercase bar at the bottom of the section, very easy to miss | Move this ABOVE the process grid as a prominent eyebrow or repeat near pricing | Loss aversion anchor — highest-converting copy on the page |

---

## High-Impact Changes

| Element | Issue | Fix | Expected lift |
|---------|-------|-----|---------------|
| Hero: no specific outcome | H1 says what you lose (clients) but not what you gain (bookings, €€€) | Rewrite H1 or add subhead: "Recupera 15 clientes al mes que ahora se van a la competencia" | Specificity triggers believability — est. +20-30% scroll depth |
| No loss aversion used | Page talks about "recovering clients" but never puts a number on what inaction costs | Add to statement section: "Cada llamada perdida es €40-€80 que se va. Son 1-2 llamadas al día en un salón ocupado." | Loss framing is 2× more motivating than gain framing |
| No social proof near pricing | Pricing cards have features but zero proof (no testimonials, no client names, no before/after) | Add 1-2 testimonial quotes directly below or between pricing cards | Social proof at decision point — critical for high-ticket skeptics |
| Pricing: no risk reversal | "Sin permanencia. Sin letra pequeña." is in the eyebrow subhead but not repeated at the CTA level | Add below each pricing card CTA: "Sin permanencia · Cancelas cuando quieras" | Risk reversal reduces friction by ~15-25% at checkout |
| No scarcity/urgency | Nothing creates a reason to act now | Add: "Cupos limitados por zona — solo 1 salón por municipio" (if true) or "Próxima disponibilidad para Majadahonda: esta semana" | Urgency → action |
| FAQ section not converting | 7 FAQs with accordion UX — requires active engagement. Visitors who have doubts may leave instead of clicking + | Add a "¿Tienes más preguntas?" CTA after FAQs linking to contact form | Capture hesitant visitors at objection point |
| Contact form: 4 fields | Nombre + Salón + Teléfono + Mensaje (optional) — reasonable but "Mensaje" field may intimidate | Make Mensaje truly invisible (not even shown) until other 3 fields are filled, OR remove it entirely for a shorter form | Form length reduction → +15-20% completion rate |
| No reciprocity | Page asks for demo/action but gives nothing free first | Add a free resource: "Descarga: Los 5 errores que hacen perder clientes a los salones de Madrid" | Reciprocity principle → goodwill before ask |

---

## A/B Test Hypotheses

| Test | Control | Variant | Metric | Priority |
|------|---------|---------|--------|---------|
| Hero H1 | "Recupera los clientes que pierdes" | "Recupera 15 clientes al mes que ahora van a la competencia" | Scroll depth to #como | P1 |
| Primary CTA copy | "Ver demostración" | "Pide tu demo gratuita" | Mailto clicks | P1 |
| Pricing CTA | "Empezar" | "Quiero el plan Agente" | Pricing mailto clicks | P1 |
| Hero subheadline | None (control) | "El asistente de WhatsApp para salones de estética en Madrid Oeste" | Time on page + scroll depth | P2 |
| Social proof near CTA | None (control) | "Salones de Majadahonda, Pozuelo y Las Rozas ya recuperan clientes con Floux" | Demo request conversion | P2 |
| Risk reversal placement | In pricing subhead only | Repeated below each pricing CTA | Pricing CTA clicks | P2 |

---

## Copy Alternatives

### Hero CTA (primary)
1. "Pide tu demo gratuita" — sets expectation (email demo), removes mystery
2. "Ver Floux en acción" — implies video/live, higher curiosity
3. "Quiero recuperar mis clientes" — outcome-language, highest commitment signal

### Pricing CTA (Agente — featured)
1. "Quiero este plan" — specific intent
2. "Empezar con Agente" — names the plan
3. "Reservar mi instalación" — frames setup as investment, not cost

### Statement Section
Current: "Ver cómo funciona →" (points back to #como which visitor already scrolled past)
Fix: "Solicita tu demostración gratuita →" (advances to conversion)
