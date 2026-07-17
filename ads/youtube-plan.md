# Floux — YouTube Ads

**Cuenta:** @flouxaim (creada, sin contenido al 2026-04-28).
**Estado:** plan en reserva. Activar en fase 3 (post 5 clientes), después de subir mínimo 5 vídeos largos al canal.

---

## 1. Estrategia general

YouTube en 2026 = **Demand Gen** (sustituyó VAC y Discovery Ads). El stack moderno:
1. **Demand Gen** — TOFU/MOFU multi-formato (in-feed, in-stream, Shorts, Gmail).
2. **Shorts Ads** — TOFU corto, complementario a TikTok/Reels.
3. **Bumper 6s** — frequency builder, brand recall.
4. **Skippable in-stream 30s** — storytelling Max founder, conversiones.

> Migración importante: **Video Action Campaigns (VAC) deprecadas** → todo conversión-driven en Demand Gen.

---

## 2. Setup técnico

- **Google Ads tag** (gtag.js) en floux.es + GA4 vinculado a Google Ads.
- **Conversion actions:**
  - `Demo agendada` (primary, value 50€)
  - `WhatsApp click` (secondary)
  - `Subscribe paid` (primary, value 970€ = LTV 12m × 0.85)
- **Enhanced conversions** activadas (hashed email/phone server-side).
- **YouTube channel link** entre Google Ads y @flouxaim para ver earned actions (subs, likes orgánicos derivados de ads).

---

## 3. Formatos — prioridad

### A. Demand Gen (60% del budget YouTube)
- Activos: 3-5 vídeos verticales 9:16 + 2-3 horizontales 16:9 + 5+ imágenes + headlines/descriptions.
- **Optimization:** `Demo agendada` o `Subscribe`.
- Reemplaza VAC. Funciona en Shorts feed, Watch feed, Gmail promotions, Discover.

### B. Shorts Ads (25%)
- Reciclar Reels/TikToks 9:16 que ya validaron.
- Duración 15-30s.
- **CTA:** sticker visible "floux.es" + caja de descripción con WhatsApp.

### C. Bumper 6s (10%)
- Solo brand recall. Cuatro variantes:
  1. Logo + "Floux. Recuperamos los clientes que no contestas."
  2. Pantalla móvil sonando ignorado + "Esto cuesta 1.200€/mes."
  3. Founder cara: "97€. Sin permanencia. Mira floux.es."
  4. Chat WhatsApp animándose + tagline.

### D. Skippable in-stream 30s (5%)
- Storytelling founder Max (origen Guatemala → frustración → Floux).
- Hook en primer 5s OBLIGATORIO (antes del skip).

---

## 4. Targeting

### Keyword targeting (in-stream + Demand Gen)
**Intención salón:**
- "agente whatsapp"
- "responder whatsapp automático"
- "perder clientes salón"
- "reservas peluquería online"
- "treatwell vs booksy"
- "no dar abasto al teléfono"
- "software gestión salón estética"
- "recuperar clientes perdidos"

**Intención oficios (fase 3+):**
- "agenda electricista"
- "no perder llamadas obra"
- "asistente whatsapp negocio"

### Audience targeting
- **Custom Segments** (keywords + URLs):
  - URLs: treatwell.es, booksy.com, fresha.com, mindbodyonline.com.
  - Search behavior: usuarios que buscaron las keywords arriba en últimos 7d.
- **In-Market:** Business Services > Marketing & Advertising; Beauty Products & Services.
- **Affinity:** Small Business Owners, Beauty Mavens.
- **Customer Match:** lista de clientes pagando + leads (mínimo 1.000 — empezar acumulando).
- **Similar Audiences:** auto-generated post-Customer Match.

### Geo
- **Comunidad de Madrid** (radio 30km Madrid centro) — fase 3a.
- **España completa** — fase 3b/c (oficios, clínicas).

---

## 5. Estructura de campaña

```
Campaign 1: Demand Gen — Floux Demos Madrid
  Objective: Sales/Leads (Demo agendada)
  Budget: 20€/día
  Bidding: Maximize Conversions
  └ Ad Group 1: Salones cold
       Audience: Custom Segment + In-Market Beauty
       Geo: Madrid 30km
       Assets: 5 videos + 5 images + 5 headlines + 3 descriptions

Campaign 2: Shorts Ads — Reels recycle
  Format: Vertical 9:16 only
  Budget: 8€/día
  └ Single ad group, 4-6 videos

Campaign 3: Bumper Brand
  Format: 6s non-skippable
  Budget: 4€/día (CPM bidding)
  Geo: Madrid Oeste códigos postales
```

---

## 6. Budget mínimo

- **Demand Gen mínimo viable:** 15-20€/día = 450-600€/mes (Google necesita ~30 conversions/mes).
- **Shorts:** desde 5€/día.
- **Bumper:** desde 3€/día (CPM-based, low-cost).
- **Bootstrap:** NO entrar en YouTube con <400€/mes total. Por debajo, no se mueve la aguja.

---

## 7. Hooks específicos YouTube

(YouTube permite más narrativa que TikTok — usar duración.)

**Skippable 30s — Max founder:**
> "Llamé a 40 salones en Madrid buscando una cita. 28 no contestaron. Cuando volví a llamar, ya tenía cita en otro sitio. Soy Max, soy guatemalteco, y eso me costó tiempo. A las dueñas les cuesta dinero. Por eso construí Floux. Cuando no puedes coger el teléfono, Floux responde por WhatsApp en 30 segundos y agenda la cita. Sin permanencia, 97€ al mes. floux.es."

**Bumper 6s:**
> [Móvil sonando ignorado en mostrador. Texto: "Cada llamada perdida son 60€."] "Floux la recupera. floux.es."

**Shorts 15s:**
> [Pantalla salón con manos trabajando.] "Tú haces lo que sabes hacer. Floux contesta el teléfono."

---

## 8. KPIs

| Métrica | Target |
|---|---|
| CPV (skippable) | <0.04€ |
| View rate | >25% |
| CPM Shorts | <5€ |
| CTR Demand Gen | >0.8% |
| CPL | <45€ |
| Conv rate landing → demo | >5% |

---

## 9. Frame final / CTA

End screen estándar todos los formatos:
- Logo Floux dorado #9A7B4F sobre charcoal #1A1714.
- "floux.es"
- Botón "Reservar demo en WhatsApp" (link en descripción).
- NO mencionar "IA" ni "bot" en ningún voiceover.
