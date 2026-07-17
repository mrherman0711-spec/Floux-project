# Floux — TikTok Ads

**Cuenta:** @flouxaim (creada, sin contenido al 2026-04-28).
**Estado:** plan en reserva. Activar tras tener 5+ TikToks orgánicos publicados (no se hace ads sin orgánico que boostear).

---

## 1. Estrategia de fondo

TikTok premia **content-led acquisition**, no creative-led ads. Antes de pagar:
1. Publicar 10-15 vídeos orgánicos de Max (POV dueña, behind-the-scenes Floux, demos chat real).
2. Identificar el top 1-2 con mejor retención (>50% completion) y mayor save rate.
3. **Boostear esos vía Spark Ads** — no crear ads from scratch.

> Razón: el algoritmo TikTok detecta "ad-like creative" en 2 segundos y mata el CPM. Spark Ads conserva la señal orgánica del vídeo.

---

## 2. Spark Ads (boost de orgánico) — prioridad #1

- **Setup:** TikTok Ads Manager → Authorize post → seleccionar TikTok orgánico de @flouxaim.
- **Ventajas vs ads from scratch:**
  - CPM 30-50% más bajo (el algoritmo lo trata como contenido).
  - Acumula likes/comments/follows reales en la cuenta orgánica.
  - El watermark TikTok se mantiene → más confianza.
- **Cuándo:** todo vídeo orgánico que pase 3.000 views o 5%+ engagement rate → Spark Ad.

---

## 3. Smart+ Campaign (cuando haya tracking sólido)

- **Activar Smart+ después de:** Pixel TikTok + Events API instalados en floux.es + 50 conversiones reales en 28d.
- **Smart+ funciona con creative variants:** subir 5-10 variantes (mismo concepto, hooks/CTAs diferentes) y dejar que la IA mezcle.
- **Optimización:** `Complete Registration` (demo) o `Lead` (CTWA).

### Estructura recomendada
```
Campaign: Smart+ Campaign — Floux Demos
  Budget: 15€/día (mínimo recomendado TikTok)
  Optimization: Lead
  Geo: España (no se puede radio fino — limitación TikTok)
  └ Creative pool: 8-12 variantes (Reels reciclados + Sparks)
```

> **Limitación TikTok:** no permite geo-radio como Meta. Hay que filtrar Madrid en post-targeting con palabras clave en bio o usar audiencias custom de web visitors.

---

## 4. Targeting

### Cold (España general)
- **Edad:** 25-54 (TikTok skew más joven que Meta — capturar también empleadas que pueden recomendar a la dueña).
- **Género:** todos.
- **Intereses TikTok:** Beauty & Personal Care, Small Business, Entrepreneurship, Fashion & Accessories.
- **Hashtag interactions:** #salonbelleza #peluqueria #esteticaprofesional #dueñadenegocio #emprendedora.
- **Creator interactions:** seguidores de @beautypros, cuentas de educación para dueñas de salón.

### Custom Audiences
- Pixel: web visitors floux.es 30/60/90d.
- Engagement: video viewers @flouxaim 100% completion.
- Lookalike de clientes pagando (cuando haya 100+ seeds — TikTok mínimo).

---

## 5. Hooks específicos para TikTok

(Diferentes a Meta — TikTok premia autenticidad/POV bruto, no editorial.)

1. **Hook 1 (POV dueña):** "Esto es lo que pasa cuando no coges el teléfono en mi salón…" → corte a screenshot WhatsApp Floux respondiendo.
2. **Hook 2 (founder cara):** "Soy guatemalteco. Llamé a 40 salones en Madrid. 28 no contestaron. Por eso construí esto."
3. **Hook 3 (data shock):** "Madrid pierde 4M€ al año en llamadas a salones. Te enseño cómo recuperar tu trozo."
4. **Hook 4 (demo bruta):** Pantalla del móvil grabada — llamada perdida → 30 seg después WhatsApp de Floux → cliente confirma cita. Sin voz, solo texto en pantalla.
5. **Hook 5 (controversia)**: "Treatwell te cobra comisión por cliente. Floux te recupera el cliente que Treatwell no ve. 97€ fijos."

**Estructura visual obligatoria:**
- Primer frame ≤1.5s con hook visual fuerte (texto grande, cara, conflicto).
- Subtítulos siempre (85% TikTok se ve sin sonido).
- Vertical 9:16, safe zone respetada (texto entre 12% top y 18% bottom).
- Duración: 15-30s para ads, 45-60s para Spark Ads orgánicos largos que ya validaron.

---

## 6. Budget mínimo

- **Spark Ads:** desde 5€/día por ad. Recomendado 10€/día/ad para 3-5 ads activos = **30-50€/día = 900-1500€/mes** cuando se escale.
- **Smart+:** 15€/día mínimo. Mejor 20€ para señal.
- **Bootstrap (escenario 100€/mes):** un solo Spark Ad sobre el orgánico top a 3€/día. Solo si ya hay orgánico ganador.

---

## 7. KPIs

| Métrica | Target |
|---|---|
| CPM | 4-7€ (más barato que Meta en ES) |
| 6s view rate | >40% |
| CTR | >1.0% |
| CPL | <30€ |
| Engagement rate | >5% |

**Kill rule:** si un Spark Ad cae bajo 3% engagement rate tras 7 días → pausar y rotar a siguiente orgánico ganador.

---

## 8. Riesgo a vigilar

TikTok ES penaliza ads B2B sin contexto. **Posicionar Floux como historia humana (Max guatemalteco, dueña ocupada) más que como SaaS.** Si los primeros 3 ads tienen CPM >10€, replantear ángulo creativo antes de aumentar budget.
