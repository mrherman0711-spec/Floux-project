# Website Improvement Consensus — 2026-04-08
## Status: AWAITING MAX APPROVAL

Instructions for Max:
- Mark each change: `[x] Approve` / `[x] Reject` / `[x] Modify → ___`
- Once done, say: "Execute the approved P1 changes from CONSENSUS.md"
- P1 = this cycle · P2 = next cycle · P3 = future

---

## P1 Changes — Implement This Cycle

---

### Change 1: Fix brand voice violation — #como intro `<p>`

**Section:** #como (process section intro)
**Element:** `<p>` inside the como intro div
**Skill justification:** brand-voice rule: NEVER use "automáticamente"
**Old:** `Cada llamada perdida es dinero que se va. Floux lo detiene automáticamente, en menos de 30 segundos.`
**New:** `Cada llamada perdida es dinero que se va. Floux actúa en menos de 30 segundos — antes de que ese cliente llame a la competencia.`
**Why:** "automáticamente" is an explicitly banned word in Floux brand rules. Replacement maintains urgency and adds competitive framing.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 2: Fix brand voice violation — #statement `<p>`

**Section:** #statement (promise section)
**Element:** `<p>` inside #statement
**Skill justification:** brand-voice rule: NEVER use "automáticamente"
**Old:** `Floux recupera automáticamente las llamadas perdidas de tu salón y las convierte en citas confirmadas. Sin que tengas que hacer nada.`
**New:** `Floux recoge esa llamada perdida y la convierte en una cita confirmada. Sin que tengas que hacer nada.`
**Why:** Removes banned word, makes the sentence more direct and human.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 3: Fix brand voice violation — #historia stat label "automática"

**Section:** #historia (founder + stats row)
**Element:** `.stat-label` for the 30s stat
**Skill justification:** brand-voice rule: NEVER use "automático/a"
**Old:** `Tiempo de respuesta<br>automática`
**New:** `Tiempo hasta la<br>primera respuesta`
**Why:** "automática" is a banned word. New label is more specific and factual.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 4: Fix brand voice violation — footer tagline "Automáticamente"

**Section:** Footer (`.footer-brand p`)
**Element:** Footer brand description paragraph
**Skill justification:** brand-voice rule: NEVER use "automáticamente"
**Old:** `Recuperamos las llamadas perdidas de tu salón. Automáticamente.`
**New:** `Recuperamos las llamadas perdidas de tu salón. En menos de 30 segundos.`
**Why:** Replaces banned word with the specific timing claim which is more credible and equally compelling.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 5: Fix brand voice violation — #porque card 03 h3 "no como un bot"

**Section:** #porque (why Floux section, card 3 — "Conversación natural")
**Element:** `<h3>` inside the third porque card
**Skill justification:** brand-voice rule: NEVER say "bot" in customer-facing copy
**Old:** `Suena como<br>tú, no como un bot.`
**New:** `Tus clientes<br>no notan nada.`
**Why:** "bot" directly names what we're supposed to never name. Replacement is simpler, more confident, and removes the negative framing.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 6: H1 — add "mientras trabajas"

**Section:** Hero (`#hero`)
**Element:** `<h1>` inside `.hero-copy`
**Skill justification:** copywriting — specificity + loss aversion; names WHY calls are missed
**Old:** `Recupera los<br>clientes que<br><em>pierdes</em>`
**New:** `Recupera los<br>clientes que<br><em>pierdes mientras trabajas</em>`
**Why:** "mientras trabajas" adds the key insight (you're busy, not negligent) and makes the headline more specific to the ICP. Minimal change, maximum impact. The italic wraps naturally around the new phrase.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 7: Hero — add ICP/definition subline below H1

**Section:** Hero (`#hero`)
**Element:** New `<p>` tag to insert between `</h1>` and `<div class="hero-btns">`
**Skill justification:** GEO definition statement requirement (first 100 words); CRO 5-second test — ICP self-selection
**Old:** *(nothing between h1 and hero-btns div)*
**New:** `<p style="color:rgba(255,255,255,0.7); font-size:1.0625rem; font-weight:300; line-height:1.7; max-width:540px; margin:20px 0 0;">El asistente de WhatsApp para salones de estética en Madrid Oeste. Cada llamada perdida, convertida en cita confirmada — en 30 segundos.</p>`
**Why:** Provides the "Floux es..." definition for GEO extraction (Perplexity, Google AI Overviews). Also clarifies ICP immediately so a 50-year-old salon owner knows within 5 seconds this is for her. Serves both SEO and CRO goals without any conflict.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 8: Statement section CTA — fix dead-end link

**Section:** #statement (promise section)
**Element:** `<a class="btn btn-primary">` inside #statement
**Skill justification:** CRO — forward CTA progression; link points backward to already-viewed section
**Old:** `<a href="#como" class="btn btn-primary">Ver cómo funciona →</a>`
**New:** `<a href="#contacto" class="btn btn-primary">Solicita tu demostración gratuita →</a>`
**Why:** Visitor is mid-page past #como when they see this CTA. Pointing back to #como is a dead end. Pointing to #contacto advances the funnel. Copy change also adds specificity ("gratuita").
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 9: Pricing CTAs — replace "Empezar" with plan-specific copy

**Section:** #precios (pricing section)
**Element:** Three `<a class="btn">` inside pricing cards
**Skill justification:** CRO + pricing-psychology — action specificity, commitment language
**Old (Básico):** `Empezar`
**New (Básico):** `Probar el plan Básico`
**Old (Agente):** `Empezar`
**New (Agente):** `Quiero el plan Agente`
**Old (Completo):** `Empezar`
**New (Completo):** `Quiero el plan Completo`
**Why:** "Empezar" communicates nothing. Plan-specific copy creates commitment identity ("I chose Agente") and makes each CTA distinct. "Quiero" for Agente is warmer and more decisive than "Probar."
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 10: Contact form submit button

**Section:** #contacto (contact/form section)
**Element:** `<button type="submit">` inside the contact form
**Skill justification:** CRO — benefit-focused CTA; form-cro: submit button copy is highest-impact form element
**Old:** `Enviar mensaje`
**New:** `Reservar mi demostración gratuita`
**Why:** "Enviar mensaje" describes the mechanical action. "Reservar mi demostración gratuita" describes the outcome the visitor wants. Small change, consistently shown to lift form completion 10-20%.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 11: Agente plan feature list — benefit rewrites

**Section:** #precios (Agente pricing card)
**Element:** `<ul class="plan-features">` inside the Agente pricing card
**Skill justification:** pricing-strategy + copywriting — features vs benefits; outcome-led copy
**Old:**
```
✓ Todo lo del plan Básico
✓ Conversación completa por WhatsApp
✓ Recoge servicio, día y nombre
✓ Resumen directo a tu móvil
```
**New:**
```
✓ Tu cliente queda apuntada. Tú no haces nada.
✓ Tu cliente elige servicio, día y hora — sin que intervengas
✓ Sabes quién viene, qué quiere y cuándo
✓ Te avisamos al momento — tú solo confirmas
```
**Why:** Features describe what Floux does. Benefits describe what the OWNER gets. All 4 agents agreed on this direction. The new list answers "what does this mean for me?" at the exact moment of decision.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 12: Agente plan setup fee — reframe as investment

**Section:** #precios (Agente pricing card)
**Element:** `.plan-sub` below the Agente price
**Skill justification:** pricing-psychology — frame cost as investment, reduce friction
**Old:** `+ €197 setup único`
**New:** `+ €197 instalación personalizada (único pago)`
**Why:** "Setup" is a tech term that feels like a cost. "Instalación personalizada" sounds like a service you're receiving. "Único pago" emphasizes it's one-time, reducing recurring cost anxiety.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 13: Completo plan setup fee — same reframe

**Section:** #precios (Completo pricing card)
**Element:** `.plan-sub` below the Completo price
**Skill justification:** pricing-psychology — consistency with Change 12
**Old:** `+ €297 setup único`
**New:** `+ €297 instalación personalizada (único pago)`
**Why:** Consistency with Agente card change above.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 14: Add risk reversal text below each pricing CTA

**Section:** #precios (all three pricing cards)
**Element:** Add a `<p>` below each CTA `<a>` tag in all three pricing cards
**Skill justification:** CRO + pricing-psychology — risk reversal reduces friction at decision point
**Old:** *(nothing after the CTA button)*
**New (add after each CTA `<a>`):** `<p style="font-size:0.6875rem; color:rgba(255,255,255,0.35); letter-spacing:0.1em; text-align:center; margin-top:12px;">Sin permanencia · Cancelas cuando quieras</p>`
**Why:** "Sin permanencia" is currently only in the pricing section intro subhead, easy to miss. Repeating it directly under each CTA is where it has maximum impact — at the moment of fear/hesitation.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 15: Stats row — fix "0 cambios" label

**Section:** #historia (founder stats row)
**Element:** Third `.stat-label` ("0" stat)
**Skill justification:** copywriting — specificity over vagueness; tech anxiety for ICP
**Old:** `Cambios que tú<br>necesitas hacer`
**New:** `Apps nuevas<br>que aprender`
**Why:** "0 cambios que tú necesitas hacer" is abstract. "0 Apps nuevas que aprender" directly names the fear of the 50-year-old ICP (learning new technology). More specific = more credible = more reassuring.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 16: Title tag — add Madrid

**Section:** `<head>`
**Element:** `<title>` tag
**Skill justification:** SEO — local keyword in title tag for Madrid searches
**Old:** `Floux — Recupera los clientes que pierdes`
**New:** `Floux Madrid — Recupera los Clientes que Pierdes`
**Why:** Adding "Madrid" to title tag is the single cheapest local SEO signal. 50 chars — within optimal range.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

### Change 17: Meta description — add to `<head>`

**Section:** `<head>`
**Element:** New `<meta name="description">` tag (currently missing entirely)
**Skill justification:** SEO — meta description is critical for search CTR and GEO definition extraction
**Old:** *(missing entirely — no meta description on the page)*
**New:** `<meta name="description" content="Floux recupera las llamadas perdidas de tu salón de estética en Madrid. Tu cliente recibe un WhatsApp en 30 segundos. Sin apps. Sin contratos. Desde €47/mes.">`
**Why:** Missing meta description = Google writes its own (often wrong). This 148-char description directly answers "qué es Floux," includes the local keyword (Madrid), the timeframe (30 segundos), key objection rebuttals (sin apps, sin contratos), and a price anchor. Also serves as GEO definition for AI engines.
**Max decision:** [ ] Approve  [ ] Reject  [ ] Modify → ___

---

## P2 Changes — Next Cycle

### P2-A: Schema markup (FAQPage + SoftwareApplication + LocalBusiness JSON-LD)
Add 2 JSON-LD `<script>` blocks before `</head>`. Full code blocks in [seo-findings.md](./../audits/seo-findings.md).
Note: Requires FAQ answers to be expanded to 100-250 words each first for GEO impact.
**Why:** 3.2× Google AI Overview inclusion with FAQPage schema. SoftwareApplication schema enables Perplexity to extract Floux's pricing and service description.

### P2-B: FAQ answer expansions (6 answers, 100-250 words each)
Current answers are 30-50 words. Expand each with a stat and direct answer format.
**Why:** GEO citability requires longer, stat-backed answers. Required for P2-A to have full impact.

### P2-C: Social proof near hero CTAs
Add 1 line below hero CTAs: `<p class="eyebrow" style="margin-top:20px; color:rgba(255,255,255,0.4);">Salones de Majadahonda, Pozuelo y Las Rozas ya recuperan clientes con Floux</p>`
**Why:** Zero trust signals above the fold is a conversion gap. This is low-effort social proof.

### P2-D: Founder bio — remove "10-15 horas / estudios" line
**Old P1 of founder bio:** "Emprendedor de Madrid Oeste, construyo Floux trabajando 10–15 horas a la semana fuera de mis estudios en la Universidad Europea."
**New P1:** "Soy Max Herman. Construyo Floux desde Madrid Oeste, después de ver el mismo patrón repetirse en decenas de salones."
**Why:** Part-time framing undermines authority at a critical trust section.

---

## P3 Changes — Future

- Add OG tags (`og:title`, `og:description`, `og:image`)
- Add Twitter Card tags
- Add `loading="lazy"` to all below-fold images
- Add `<meta name="author" content="Max Herman">`
- Add `<meta name="geo.region" content="ES-MD">`
- Add FAQ: "¿Por qué no uso Booksy?" with Floux complementarity answer
- Add FAQ: "¿No me basta con el contestador?" with 62% stat
- Consider daily cost reframe below Agente price: "Menos de €3.25 al día"
- Consider ROI calculation block near pricing: "2 clientes recuperados = plan pagado"
- Consider 30-day money-back guarantee on setup (pending Max policy decision)
- Scarcity frame: "Solo 1 salón por municipio" (only if operationally true)
- Loss aversion quantification in statement section: "Cada llamada perdida son €40-€80 que se van"
