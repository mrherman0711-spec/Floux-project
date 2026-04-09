# Website Improvement Debate — 2026-04-08

Cross-agent conflict resolution. Strategy agent reads all 4 audit files and adjudicates.

---

## Change #1: Brand Voice Violations ("automáticamente", "bot")

**Copy Agent position:** 5 brand voice violations found (P1, fix immediately):
- #como intro: "Floux lo detiene automáticamente"
- #statement: "Floux recupera automáticamente las llamadas perdidas"
- #historia stat label: "Tiempo de respuesta automática"
- Footer: "Recuperamos las llamadas perdidas de tu salón. Automáticamente."
- #porque card 03 h3: "Suena como tú, no como un bot."

**SEO Agent position:** No conflict — SEO also flagged "automática" in stat label as needing removal.

**CRO Agent position:** Not flagged separately — defers to Copy on voice.

**Pricing Agent position:** Not relevant.

**Conflict:** No
**Resolution:** Fix all 5 violations. Copy Agent's exact proposed rewrites are correct:
- "automáticamente" → remove or replace with "en menos de 30 segundos" / "sin que tengas que hacer nada"
- "automática" (stat) → "primera respuesta"
- "no como un bot" → "tus clientes no notan nada"
- Footer: "Automáticamente." → "En menos de 30 segundos."
**Priority:** P1 — non-negotiable brand rule, fix before any other change

---

## Change #2: Hero Subheadline (ICP specificity)

**CRO Agent position:** Missing subheadline is a critical gap — visitor doesn't self-select in 5 seconds. Proposed: "El asistente de WhatsApp para salones de estética en Madrid Oeste"

**Copy Agent position:** Agrees — hero needs ICP identification. Proposes moving eyebrow from topbar (which disappears on scroll) to a visible line above H1.

**SEO Agent position:** Supports adding ICP/Madrid copy near hero for keyword density. "salón de estética · Madrid Oeste" in first 100 words improves local SEO.

**Pricing Agent position:** Not relevant.

**Conflict:** Minor — CRO wants it below H1 as subhead, Copy wants it above H1 as eyebrow.
**Resolution:** Both can coexist: eyebrow ABOVE H1 (already exists as hero-topbar, but make it visible in hero-copy block) + 1-sentence subhead BELOW H1. Keep hero-topbar but also add one line inside hero-copy after the H1.
Proposed hero copy block after change:
```
[eyebrow above h1] Para salones de estética · Madrid Oeste
[H1] Recupera los clientes que pierdes mientras trabajas
[subline] El asistente de WhatsApp que convierte llamadas perdidas en citas confirmadas — en 30 segundos.
[CTAs]
```
**Priority:** P1

---

## Change #3: Hero H1 Rewrite

**Copy Agent position:** Current H1 is strong but vague. Option C (minimal): "Recupera los clientes que pierdes *mientras trabajas*" — adds key insight about why calls are missed. Option A: "15 clientes al mes que se iban. Ahora se quedan."

**CRO Agent position:** Agrees H1 needs outcome specificity. Prefers a number in H1 or subhead: "Recupera 15 clientes al mes que ahora van a la competencia."

**SEO Agent position:** Prefers keeping H1 clean with primary keyword, adding numbers to subhead instead (H1 with numbers can look spammy for very branded searches).

**Conflict:** Yes — CRO wants number IN H1; SEO wants number in subhead; Copy offers both options.
**Resolution:** SEO wins on this one. Keep H1 as current brand statement but enhance: add "mientras trabajas" (Copy Option C) to the H1 for specificity without stuffing a number. Move "+15 clientes" specificity to the hero subline below H1.

Final H1: `Recupera los clientes que pierdes mientras trabajas`
Final subline: `Floux es el asistente de WhatsApp para salones de estética en Madrid Oeste. Cada llamada perdida se convierte en una cita confirmada — en 30 segundos.`

**Priority:** P1 (H1 tweak) + P1 (definition subline — also serves GEO definition requirement)

---

## Change #4: Statement Section CTA

**CRO Agent position:** "Ver cómo funciona →" points backward (visitor already passed #como). Should link to #contacto with benefit copy.

**Copy Agent position:** Same — "Solicita tu demostración gratuita →" (links to #contacto).

**SEO Agent position:** No conflict — internal link change, no SEO impact.

**Pricing Agent position:** Not relevant.

**Conflict:** No
**Resolution:** Change statement CTA from `href="#como"` to `href="#contacto"` and copy from "Ver cómo funciona →" to "Solicita tu demostración gratuita →"
**Priority:** P1 — dead-end CTA actively loses conversions

---

## Change #5: Pricing CTAs ("Empezar")

**CRO Agent position:** "Empezar" is the weakest CTA possible. Proposes: "Quiero este plan" or "Empezar con Agente."

**Copy Agent position:** Same assessment. Proposes per-plan specificity: "Probar el plan Básico" / "Quiero el plan Agente" / "Quiero el plan Completo."

**Pricing Agent position:** Agrees. Proposes: "Probar el plan Básico" / "Quiero el plan Agente" / "Quiero el plan Completo."

**Conflict:** No
**Resolution:** Use plan-specific CTAs. All 3 agents agree on the direction; Pricing Agent's per-plan names are clearest:
- Básico: "Probar el plan Básico"
- Agente (featured): "Quiero el plan Agente"
- Completo: "Quiero el plan Completo"
**Priority:** P1

---

## Change #6: Contact Form Button ("Enviar mensaje")

**CRO Agent position:** Change to "Reservar mi demostración gratuita."

**Copy Agent position:** Change to "Reservar mi demo gratuita."

**SEO Agent position:** No conflict.

**Pricing Agent position:** Not relevant.

**Conflict:** Minor wording difference.
**Resolution:** "Reservar mi demostración gratuita" (full word, more professional for the ICP).
**Priority:** P1

---

## Change #7: Meta Description

**SEO Agent position:** Missing entirely. Must add. Proposed: "Floux recupera las llamadas perdidas de tu salón de estética en Madrid. Tu cliente recibe un WhatsApp en 30 segundos. Sin apps. Sin contratos. €47/mes." (150 chars)

**CRO Agent position:** Supports — improves CTR from search.

**Copy Agent position:** No conflict — approves SEO's proposed text.

**Pricing Agent position:** Not relevant.

**Conflict:** No
**Resolution:** Add the SEO Agent's proposed meta description.
**Priority:** P1 — technical SEO baseline

---

## Change #8: Schema Markup (FAQPage + SoftwareApplication + LocalBusiness)

**SEO Agent position:** P1 for GEO — FAQPage JSON-LD gives 3.2× Google AI Overview inclusion. SoftwareApplication + LocalBusiness enables Perplexity and ChatGPT Search extraction. Complete JSON-LD blocks provided in seo-findings.md.

**CRO Agent position:** No direct conflict. Structured data is invisible to users but supports long-term discovery.

**Copy Agent position:** No conflict. Notes that FAQ answers must first be expanded (>100 words each) for the schema to have GEO impact.

**Pricing Agent position:** Supports — pricing in plain text (currently in HTML) will be LLM-extractable once schema is added.

**Conflict:** Dependency noted — Copy Agent correctly flags that schema alone won't deliver GEO lift if FAQ answers remain 30-50 words. SEO Agent's FAQ rewrites (100-250 words) must accompany schema.
**Resolution:** Add JSON-LD schema blocks AND expand FAQ answers together in the same change set.
**Priority:** P2 (requires more content work than a simple copy swap — do after P1 changes)

---

## Change #9: Agente Plan Feature → Benefit Rewrites

**Pricing Agent position:** All 4 Agente features are written as features, not benefits. Proposed rewrites in pricing-findings.md.

**Copy Agent position:** Same assessment with same proposed direction.

**CRO Agent position:** Supports — benefit language converts better at decision point.

**SEO Agent position:** No conflict.

**Conflict:** No
**Resolution:** Adopt Pricing Agent's rewrites (most specific version):
- "Conversación completa por WhatsApp" → "Tu cliente queda apuntada sin que tú toques el móvil"
- "Recoge servicio, día y nombre" → "Sabes quién viene, qué quiere y cuándo"
- "Resumen directo a tu móvil" → "Te avisamos al momento — tú solo confirmas"
- "Todo lo del plan Básico" → Remove; replace with "Tu cliente queda apuntada. Tú no haces nada."
**Priority:** P1

---

## Change #10: Setup Fee Framing

**Pricing Agent position:** "+ €197 setup único" sounds like a cost. Change to "+ €197 instalación personalizada (único pago)."

**Copy Agent position:** No specific flag — defers to Pricing.

**CRO Agent position:** Flagged setup fee as potential friction; supports reframing as investment.

**SEO Agent position:** No impact.

**Conflict:** No
**Resolution:** Change plan-sub text under Agente and Completo prices.
- Agente: "+ €197 instalación personalizada (único pago)"
- Completo: "+ €297 instalación personalizada (único pago)"
**Priority:** P1

---

## Change #11: Risk Reversal Near Pricing CTAs

**Pricing Agent position:** Add "Sin permanencia · Cancelas cuando quieras · Sin penalización" below each CTA button. Also proposes optional 30-day money-back guarantee.

**CRO Agent position:** Risk reversal at CTA level reduces friction by 15-25%. Strongly supports.

**Copy Agent position:** "Cancelas cuando quieras. Sin penalización." already exists in #porque card 4 — needs to be closer to the actual decision (pricing section).

**SEO Agent position:** No impact.

**Conflict:** No conflict on adding risk reversal to pricing. Minor debate on 30-day guarantee — Pricing suggests it, CRO supports, but it requires operational confirmation from Max.
**Resolution:** Add risk reversal text below ALL three pricing CTAs: "Sin permanencia · Sin penalización". Keep 30-day guarantee as P3 (pending Max confirmation of policy).
**Priority:** P1

---

## Change #12: Stat Label "0 Cambios"

**Copy Agent position:** "0 cambios que tú necesitas hacer" is feature framing with zero aspiration. Proposes: "0 Apps nuevas que aprender."

**CRO Agent position:** Agrees stat is weak.

**SEO Agent position:** No ranking impact.

**Pricing Agent position:** Not relevant.

**Conflict:** No
**Resolution:** Change to "0 Apps nuevas que aprender" — more specific, directly addresses tech-anxiety of 50-year-old ICP.
**Priority:** P1

---

## Change #13: "No como un bot" in #porque card 3

**Copy Agent position:** P1 brand violation — says "bot" directly.

**CRO Agent position:** Agrees.

**Resolution:** Change `<h3>` from "Suena como tú, no como un bot." to "Tus clientes no notan nada."
**Priority:** P1

---

## Change #14: Founder Bio — Remove "10-15 horas / estudios"

**Copy Agent position:** Mentioning part-time work undermines authority. Remove line about hours/studies.

**CRO Agent position:** Supports — trust signals should build confidence, not introduce doubt.

**SEO Agent position:** Has positive impact — author authority for GEO is better conveyed by credibility than schedule.

**Conflict:** No
**Resolution:** Remove "trabajando 10–15 horas a la semana fuera de mis estudios en la Universidad Europea" from P1 of founder bio.
New P1: "Soy Max Herman. Construyo Floux desde Madrid Oeste, después de ver el mismo patrón repetirse en decenas de salones: propietarias extraordinarias, con agenda llena y manos ocupadas, perdiendo clientes simplemente por no poder coger el teléfono."
**Priority:** P2 (softer impact than copy violations)

---

## Change #15: Title Tag — Add "Madrid"

**SEO Agent position:** Current: "Floux — Recupera los clientes que pierdes" (49 chars). Proposed: "Floux Madrid — Recupera los Clientes que Pierdes" (50 chars). Adds local signal without keyword stuffing.

**CRO Agent position:** No conflict.

**Copy Agent position:** Approved.

**Conflict:** No
**Resolution:** Update `<title>` tag.
**Priority:** P1

---

## P3 Changes (low effort, future cycle)

- Add OG tags (og:title, og:description, og:image)
- Add Twitter Card tags
- Add `loading="lazy"` to all below-fold images
- Add FAQ answer expansions (100-250 words each) for GEO
- Add `<meta name="geo.region" content="ES-MD">`
- Add reciprocity element (free download or ROI calculator)
- Add scarcity frame ("1 salón por municipio")
- Add Booksy/Treatwell competitive FAQ
- Consider 30-day money-back guarantee (pending Max approval)
- Add testimonial quotes near pricing section
