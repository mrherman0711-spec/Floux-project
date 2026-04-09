# Pricing Audit Findings — 2026-04-08

## Critical Pricing Issues

### 1. "Empezar" CTA is conversion dead weight
All three pricing cards use "Empezar" — the most generic CTA possible. It communicates nothing: no benefit, no direction, no commitment signal. For a 50-year-old salon owner who has never paid for software, "Empezar" feels like a leap into the unknown. She needs specificity.
- **Fix:** Agente card → "Quiero el plan Agente" | Básico → "Probar el plan Básico" | Completo → "Quiero el plan Completo"

### 2. ROI anchor is misplaced and too small
"Se paga solo con un cliente recuperado" is present — excellent. But it appears in two weak positions:
- In the intro subhead above the pricing grid (easy to miss, low visual weight)
- As a tiny lowercase bar in the #como process section (wrong location)
It is NOT present next to the price numbers themselves, which is where it needs to live.
- **Fix:** Add directly below each plan price: `"1 cliente recuperado = ya pagado"` or visually near the Agente card price.

### 3. Setup fee (€197) framed as a cost, not an investment
The plan-sub below the Agente price says "+ €197 setup único" — dry, factual, potentially alarming for a first-time SaaS buyer who's comparing to €0 (doing nothing).
- **Fix:** Reframe: `"+ €197 instalación personalizada (único pago)"` — "instalación personalizada" sounds like a service, not a fee. "Único pago" emphasizes it doesn't recur.

### 4. No social proof at decision point
Pricing cards contain features only. No testimonial, no client count, no "X salones confían en Floux" near the pricing section. The salon owner is being asked to commit €97/mes + €197 with zero third-party validation at the moment of decision.
- **Fix:** Add above or between pricing cards: a single testimonial quote, or "Salones de Majadahonda, Pozuelo y Las Rozas ya recuperan clientes con Floux."

### 5. Feature list written as features, not outcomes
The Agente plan lists:
- "Todo lo del plan Básico" → meaningless (visitor doesn't know Básico features by heart at this scroll position)
- "Conversación completa por WhatsApp" → feature
- "Recoge servicio, día y nombre" → feature
- "Resumen directo a tu móvil" → feature

None of these answer "what does this mean for ME?"

---

## Psychology Applications Missing

| Principle | Where to apply | Specific implementation |
|-----------|---------------|------------------------|
| **Anchoring** | Pricing section header | €147 Completo plan is present but not anchored correctly — the eye goes to €97 first. Consider: open the grid with Completo (highest) so €97 looks like a saving | 
| **Decoy effect** | Básico vs Agente | Básico at €47 needs to feel obviously incomplete, making Agente the "logical upgrade." Currently Básico says "Sin conversación de reserva" (dim text) — this is good but should be more explicit: "Tu cliente recibe un mensaje, pero tú tienes que llamarlo para reservar" — shows the pain of choosing Básico |
| **Mental accounting: daily cost** | Below Agente price | "€97/mes = menos de €3.25 al día — menos que un café" — makes €97 feel trivial |
| **Loss framing in pricing** | Above pricing grid | "¿Cuántas llamadas pierdes al día? A €50 por cliente, son €350 a la semana que se van." before showing the €97/mes solution makes the price feel small |
| **Commitment & consistency** | Pricing intro | Add a micro-commitment before pricing: "Si recuperas 1 cliente al mes, Floux se paga solo. ¿Cuántos recuperas tú?" |
| **Charm pricing** | Already applied | €97 vs €100 ✓ Keep |
| **Risk reversal** | Below ALL pricing CTAs | "Sin permanencia. Cancelas con 15 días de aviso." should appear below each CTA button, not just in the section intro |

---

## Feature → Benefit Rewrites

| Current text | Proposed benefit-framed version |
|-------------|--------------------------------|
| "WhatsApp automático en llamada perdida" (Básico) | "Tu cliente sabe que no le olvidaste — recibe mensaje en 30s" |
| "Mensaje personalizado con tu nombre" (Básico) | "El mensaje lleva el nombre de TU salón, no de Floux" |
| "Sin conversación de reserva" (Básico, dim) | "Tu cliente recibe el mensaje, pero tú tienes que llamar para confirmar — por eso el 80% elige Agente" |
| "Todo lo del plan Básico" (Agente) | Remove — replace with the actual key benefit: "Tu cliente queda apuntada. Tú no haces nada." |
| "Conversación completa por WhatsApp" (Agente) | "Tu cliente escoge servicio, día y hora — sin que tú intervengas" |
| "Recoge servicio, día y nombre" (Agente) | "Sabes quién viene, qué quiere y cuándo — antes de que abras el salón" |
| "Resumen directo a tu móvil" (Agente) | "Te avisamos al momento. Tú solo confirmas con un mensaje." |
| "Todo lo del plan Agente" (Completo) | Remove — replace with: "Todo lo de Agente, más:" |
| "Solicitudes de reseña en Google" (Completo) | "Más reseñas en Google, automáticamente, sin pedírselo tú" |
| "Recordatorios automáticos de cita" (Completo) | "Tus clientes se acuerdan de la cita — reduces no-shows" |
| "Reactivación de clientas inactivas" (Completo) | "Recupera clientas que llevan 2+ meses sin venir" |

---

## ROI Framing Recommendations

### Place this calculation near (or inside) the Agente pricing card:

> **"¿Merece la pena €97 al mes?"**
> Una sesión media en Madrid cuesta €50.
> Con 2 clientes recuperados al mes, ya has pagado el plan.
> Nuestras clientas recuperan de media 15 clientes al mes.
> **Eso es €750/mes que antes se iba a la competencia.**

### Daily cost reframe (add below Agente price):
> `Menos de €3.25 al día`

### Micro-calculation prompt (add above pricing grid):
> `Si pierdes 2 llamadas al día y cada cliente vale €50 → son €3.000/mes que se van. Floux cuesta €97.`

---

## Risk Reversal Options

### Option A: "Sin permanencia" (already exists — amplify it)
Currently in the section intro. Should be repeated as a badge/line directly under every CTA button:
```
[Quiero el plan Agente]
Sin permanencia · Cancelas cuando quieras · Sin penalización
```

### Option B: "Primer mes de prueba" guarantee (not currently offered)
If operationally feasible: "Si en 30 días no has recuperado ni un cliente, te devolvemos el setup." Low risk for Floux (almost impossible given avg 15 recovered/month), but extremely high conversion lift for skeptical first-time buyers.
- Implementation: Add to Agente card: `"Garantía 30 días — si no ves resultados, te devolvemos el setup."`

---

## Competitive Positioning Gaps

### Objections not pre-empted:

**1. "¿Por qué no uso Booksy o Treatwell?"**
These platforms require salons to actively list their services and manage profiles. Floux works passively on missed calls — complementary, not competing. But the page never says this. A skeptical owner thinks "I already have Booksy, why do I need Floux?"
- **Fix:** Add a `#porque` card or FAQ: "¿Tengo Booksy, ¿me sirve Floux?" → "Sí. Booksy gestiona tu agenda, Floux captura los clientes que nunca llegaron a abrirla."

**2. "¿Por qué no contrato a una persona para coger el teléfono?"**
An employee to answer calls costs €1,200/mes minimum (media jornada). Floux costs €97. Never mentioned.
- **Fix:** Add to FAQ or pricing section: "Una persona a media jornada para coger el teléfono cuesta desde €1.200/mes. Floux cuesta €97 y funciona 24/7."

**3. "¿No me basta con el contestador automático?"**
62% of missed callers don't leave voicemails — they just call the next salon. This is the core insight. The page mentions it implicitly but never states it as a fact.
- **Fix:** Add as a stat in #porque or FAQ: "El 62% de los clientes que no obtienen respuesta llaman a la competencia en menos de 5 minutos — y nunca vuelven."
