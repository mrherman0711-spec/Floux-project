# Floux — LinkedIn Ads

**Página:** linkedin.com/company/flouxaim/
**Estado:** plan en reserva. **NO activar hasta fase 3** (post 5 clientes pagando, validación ICP B2B verticales nuevos).

---

## 1. Por qué LinkedIn aunque la audiencia primaria NO esté ahí

La dueña de salón en Majadahonda **no usa LinkedIn**. Meta + TikTok ganan ese ICP.

LinkedIn justifica su presupuesto **solo cuando se activan los nichos B2B futuros del brand profile**:
- **Electricistas / fontaneros / oficios** (mismo dolor: en obra → no cogen el teléfono).
- **Dentistas / clínicas privadas** (recepcionista satura → leads se pierden).
- **Inmobiliarias** (agentes en visita → no contestan).

LinkedIn es el único canal donde se puede targetear **"Owner / Self-employed" + título profesional específico** con precisión real. **Por eso se prepara ahora pero se activa después.**

---

## 2. Setup técnico

- **Insight Tag** instalada en floux.es (script base + conversion tags).
- **Conversion API LinkedIn** (server-side) — activar cuando haya volumen.
- **Lead Gen Form templates** creados con campos: nombre, empresa, teléfono móvil, ciudad, "¿cuántas llamadas pierdes al día?".
- **Matched Audiences:**
  - Web retargeting visitors floux.es 90/180/365d.
  - Lista contactos (clientes pagando + leads cualificados) → upload manual.
  - Company list (subir nombres de salones/clínicas/instaladoras objetivo).

---

## 3. Audiencias por fase

### Fase 3a — Salones (validación cruzada con Meta)
- **Job titles:** Owner, Founder, Director, Propietario, Esthetician Owner, Salon Owner, Hair Salon Owner.
- **Industry:** Personal Care Services, Cosmetics, Wellness and Fitness Services.
- **Geo:** Comunidad de Madrid + 50km.
- **Company size:** 1-10 empleados.
- **Estimación audiencia:** 8-15k. Pequeña pero útil para retargeting.

### Fase 3b — Electricistas / oficios (B2B futuro #1)
- **Job titles:** Electrician (Owner), Electrical Contractor, Plumber Owner, Self-employed (con filtro skills).
- **Industry:** Construction, Electrical/Electronic Manufacturing, Facilities Services.
- **Geo:** España.
- **Company size:** 1-10.
- **Estimación:** 25-40k.

### Fase 3c — Dentistas / clínicas
- **Job titles:** Dentist Owner, Clinic Director, Practice Manager, Dueño Clínica.
- **Industry:** Hospital & Health Care, Medical Practice.
- **Geo:** Comunidad de Madrid.
- **Company size:** 1-10.
- **Estimación:** 5-8k.

### Predictive Audiences
Activar predictive audiences de LinkedIn (LAL evolucionado) **a partir de 300 leads en CRM** subidos.

---

## 4. Formatos recomendados

1. **Sponsored Content + Lead Gen Forms** — formato #1. Form pre-rellenado dentro de LinkedIn = CPL más bajo.
2. **Document Ads (PDF carrusel)** — funciona muy bien para casos de éxito ("Cómo el Salón X recuperó 1.200€ en 30 días con Floux"). High dwell time.
3. **Single Image Ad** — para retargeting con oferta directa.
4. **Thought Leader Ads** — boostear posts orgánicos de Max (founder voice) — mejor CPC que ads de la company page.
5. **Video Ads** — solo si el creative es nativo (subtitulado, vertical o square, <60s).

**NO usar inicialmente:** Message Ads / Conversation Ads (CPL altísimo + percibido como spam).

---

## 5. Estructura de campaña

```
Campaign Group: Floux — Salones ES (Fase 3a)
  └ Campaign 1: SC + Lead Gen — Salon Owners Madrid
       Objective: Lead Generation
       Budget: 15€/día (mínimo LinkedIn 10€)
       Bidding: Maximum Delivery (auto)
       └ Ad 1: Document Ad — caso éxito
       └ Ad 2: SC video — founder Max
       └ Ad 3: SC single image — "97€ recupera 1 cliente"

Campaign Group: Floux — Electricistas ES (Fase 3b)
  └ Campaign 1: SC + Lead Gen — Electrician Owners
       Budget: 20€/día
       └ Creative específico al vertical (NO reciclar de salones)
```

---

## 6. Budget mínimo

- **Mínimo viable LinkedIn:** 10€/día por campaign (oficial LI). Realmente útil **20€/día** para señal.
- **Bootstrap:** **NO entrar con menos de 300€/mes total.** Por debajo, no hay aprendizaje.
- **Recomendado fase 3:** 500€/mes split en 2 verticales (1 salones + 1 oficios).

---

## 7. Creative direction LinkedIn

**Tono más sobrio que Meta/TikTok.** Aquí Max es **founder/CEO**, no protagonista TikTok.

**Hooks B2B específicos:**
1. "El 67% de las llamadas que recibe un salón fuera de horario nunca se devuelven. Ese ingreso fantasma tiene solución."
2. "Construí Floux después de hablar con 40 dueñas. Esto es lo que aprendí sobre pérdida de clientes en negocios de servicio."
3. "Caso: Salón en Pozuelo. 8 llamadas perdidas/día → 23 citas recuperadas/mes con Floux. ROI 14x."
4. "Si eres electricista y estás en obra, este post es para ti."
5. "Sin permanencia. 97€/mes. Funciona o cancelas."

**Frame final:** Max + nombre + título + floux.es + CTA "Reservar demo 10 min".

---

## 8. KPIs LinkedIn (más caros que Meta — esperado)

| Métrica | Target |
|---|---|
| CPM | 25-50€ (LinkedIn ES) |
| CTR Sponsored Content | >0.6% |
| CPL Lead Gen Form | <25€ |
| Lead → demo agendada | >40% |
| Demo → cliente | >30% (B2B nicho cualificado) |
| CAC LinkedIn | <350€ aceptable (LTV mayor en oficios/clínicas) |

---

## 9. Kill criteria

Si tras **300€ gastados** en una campaign no hay 5+ leads cualificados, matar y replantear creative o audiencia. LinkedIn castiga budgets bajos con CPM hinchado.
