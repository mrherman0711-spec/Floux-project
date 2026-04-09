# Copy Audit Findings — 2026-04-08

## Brand Voice Violations Found

**P1 — Fix immediately:**

| Location | Violating text | Rule violated |
|----------|---------------|----------------|
| `#como` section intro `<p>` | "Floux lo detiene **automáticamente**, en menos de 30 segundos." | NEVER use "automáticamente"/"automático" |
| `#statement` section `<p>` | "Floux recupera **automáticamente** las llamadas perdidas de tu salón" | NEVER use "automáticamente"/"automático" |
| `#historia` stat label | "Tiempo de respuesta **automática**" | NEVER use "automático/a" |
| Footer brand tagline | "Recuperamos las llamadas perdidas de tu salón. **Automáticamente**." | NEVER use "automáticamente" |
| `#porque` card 03 `<h3>` | "Suena como tú, **no como un bot**." | NEVER say "bot" — this directly names what we're supposed to avoid naming |

**Count: 5 brand voice violations. All P1.**

---

## Headline Analysis

**Current H1:** "Recupera los clientes que pierdes"

**Issue:** Strong loss framing, but:
- "Clientes que pierdes" is universal — doesn't self-select the salon ICP immediately
- No specificity about HOW or HOW MANY — no number, no timeframe
- Doesn't mention Madrid or salon/estética — cold visitor doesn't know if this is for them
- "Recupera" is imperative (command) — works, but could be even stronger with outcome specificity

**Proposed alternatives:**
- Option A: "15 clientes al mes que se iban. Ahora se quedan." — Specific number, outcome flip, past→present tense creates urgency. Rationale: specificity is more credible than a vague promise.
- Option B: "Tu salón pierde €600 al mes en llamadas perdidas." — Pure loss framing with €€€. Rationale: money is the most visceral motivator for an owner-operator.
- Option C: "Recupera los clientes que pierdes *mientras trabajas*" — Minimal change, adds the key insight (you're losing them because you're busy, not negligent). Rationale: lowest-friction improvement, keeps current energy.

**Recommendation: Option C as P1 (minimal change), test Option A as P2 variant.**

---

## Section-by-Section Issues

| Section | Element | Issue | Proposed copy |
|---------|---------|-------|---------------|
| Hero | Missing subheadline | No copy between H1 and CTAs — no context for WHO this is for | Add: `<p class="eyebrow">Para salones de estética y peluquerías · Madrid Oeste</p>` below H1 |
| Hero | Topbar | "Centros de estética · Madrid Oeste · Recuperamos tus llamadas perdidas" is good but invisible at scroll = 0 (transparent) and disappears on scroll | Move key phrase into visible hero copy as an eyebrow *above* H1 |
| #como intro | `<p>` | "Floux lo detiene **automáticamente**" — brand violation + "detiene" is odd (stops, blocks) not quite accurate | "Floux actúa en menos de 30 segundos — antes de que ese cliente llame a la competencia." |
| #como | Card 01 `<p>` | "Antes, ese cliente llamaba a otro salón. Ahora Floux actúa." — good tension, but passive on "Floux actúa" | "Antes, ese cliente llamaba a otro salón. Ahora te lo recuperamos." (más personal, dueña como protagonista) |
| #como | Card 03 `<p>` | "Sin apps nuevas. Sin complicaciones." — fine but weak close for card 3 which should seal the deal | "Tú solo confirmas. Nosotros ya hicimos todo lo demás." |
| #statement | `<p>` | "Floux recupera **automáticamente**..." — brand violation | "Floux recoge esa llamada perdida y la convierte en una cita confirmada. Sin que tengas que hacer nada." |
| #statement | CTA | "Ver cómo funciona →" — visitor already scrolled past the "how it works" section. This is a dead-end CTA | "Solicita tu demostración gratuita →" (links to #contacto) |
| #porque | Card 03 h3 | "Suena como tú, **no como un bot**." — names "bot", violates brand rules | "Suena exactamente como tú — tus clientes no notan nada." |
| #precios | Eyebrow | "INVERSIÓN" — Cormorant SC eyebrow label above pricing section | Good framing — keep ✓ |
| #precios | Plan features (Agente) | "Conversación completa por WhatsApp" — feature, not benefit | "Tu cliente queda apuntada sin que tú toques el móvil" |
| #precios | Plan features (Agente) | "Recoge servicio, día y nombre" — feature | "Sabes exactamente quién viene, qué quiere y cuándo" |
| #precios | Plan features (Agente) | "Resumen directo a tu móvil" — feature | "Te avisamos al momento — tú solo confirmas" |
| #historia | Stats | "+15 clientes recuperados de media al mes" — strongest stat | Keep ✓ but add "en salones de Madrid Oeste" for credibility |
| #historia | Stats | "30s tiempo de respuesta automática" — brand violation | "30s hasta la primera respuesta" |
| #historia | Stats | "0 cambios que tú necesitas hacer" — this is a feature/negative framing (zero isn't aspirational) | "0 Apps nuevas que aprender" (more specific and resonant) |
| #historia | Founder bio P1 | "Emprendedor de Madrid Oeste, construyo Floux trabajando 10–15 horas a la semana fuera de mis estudios en la Universidad Europea." — oversharing about part-time builds doubt | Shorten to: "Construyo Floux desde Madrid Oeste, después de ver el mismo patrón repetirse en decenas de salones." (leads with insight, not schedule) |
| #faqs | Q: "¿Necesito instalar...?" | "En menos de 48 horas está funcionando." — this is the best line in the FAQs | Keep ✓ but add "sin que tengas que hacer nada" to reinforce |
| #faqs | Q: "¿Merece la pena?" | "La mayoría de nuestras **clientas** recuperan entre 10 y 20 clientes al mes" — "clientas" is good (gendered to ICP) | ✓ Keep — smart ICP targeting. Add: "Lo que antes se iba a la competencia, ahora es tuyo." |
| #contacto | H2 | "Hablemos. Sin presión." — excellent | Keep ✓ |
| #contacto | Form subhead | "Reserva una demostración gratuita" — good | Keep ✓ |
| Footer | Brand tagline | "Recuperamos las llamadas perdidas de tu salón. Automáticamente." | Remove "Automáticamente." → "Recuperamos las llamadas perdidas de tu salón. En menos de 30 segundos." |

---

## CTA Copy Recommendations

| Current CTA | Issue | Proposed alternatives |
|-------------|-------|----------------------|
| "Ver demostración" (nav + hero) | Vague — implies video, but it's a mailto | "Pide tu demo gratuita" / "Solicita una demostración" |
| "Cómo funciona" (hero secondary) | Functional, not motivating | Convert to text link: `↓ Ver cómo funciona` |
| "Empezar" (pricing ×3) | Weakest CTA possible | Básico: "Empezar con Básico" · Agente: "Quiero el plan Agente" · Completo: "Quiero el plan Completo" |
| "Ver cómo funciona →" (statement) | Links backward to section already scrolled | "Solicita tu demostración gratuita →" (link to #contacto) |
| "Enviar mensaje" (contact form) | Generic | "Reservar mi demo gratuita" |

---

## Psychology Gaps

**Missing principles (each one is a missed opportunity):**

1. **Loss aversion quantified:** The page says "clientes que pierdes" but NEVER puts a number on the daily loss. A 50-year-old salon owner needs to feel the pain concretely: "Si recibes 3 llamadas perdidas al día a €50 cada una, son €4.500 al mes que se van." Add this to the statement section or as a callout near pricing.

2. **Social proof — specificity missing:** "Salones de Majadahonda, Pozuelo y Las Rozas ya confían en Floux" is mentioned in contacto but not above the fold. Testimonials or even salon names with neighborhoods would dramatically increase trust for cold traffic.

3. **Commitment & consistency:** The page jumps from hero to 3-step process to pricing. There's no small "yes" ladder. Consider: add a quiz/self-assessment ("¿Cuántas llamadas pierdes al día?") or a micro-CTA ("Calcula lo que pierdes") before pricing — primes the visitor for the €97 anchor.

4. **Authority — founder credibility undersold:** Max walking Madrid Oeste streets is a great story, but "working 10-15 hours outside my studies" undermines authority. Replace with the insight he gained, not the hours he worked.

5. **Reciprocity — nothing free offered:** The page only asks (demo request, contact form). Offering a free "Cálculo de clientes perdidos" PDF or a "5 errores" resource would trigger reciprocity before the ask.

6. **Scarcity — completely absent:** No urgency mechanism. If Max really does service salons one by one personally, "Solo 1 salón por municipio" is both true and a powerful scarcity frame.

---

## Strongest Lines on the Page

These are working — don't touch:

- **"Recupera los clientes que pierdes"** (H1) — loss frame, imperative, clean
- **"Ningún negocio debería perder un cliente por estar trabajando"** (statement H2) — this is the emotional heart of the page. Perfect.
- **"Hablemos. Sin presión."** (contact H2) — exactly the right tone for a skeptical ICP
- **"Cancelas cuando quieras. Sin penalización."** (porque card 4) — addresses the #1 contract objection preemptively
- **"En menos de 48 horas está funcionando."** (FAQ) — specificity builds confidence
- **"Tus clientas no notan la diferencia."** (porque card 3 — after removing "bot") — powerful reassurance
- **"No vengo de Silicon Valley — vengo de las calles de Majadahonda, Boadilla y Pozuelo."** — excellent local credibility line, keep exactly as-is
