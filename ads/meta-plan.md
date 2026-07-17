# Floux — Meta Ads (Instagram + Facebook)

**Cuenta:** Business Suite Floux (página FB conectada, IG @flouxaim).
**Pixel:** instalar en floux.es (ID a generar) + CAPI server-side desde el webhook FastAPI.
**Estado:** plan en reserva — activar tras primer cliente pagando.

---

## 1. Setup técnico (antes de lanzar 1€)

- **Pixel base + CAPI** en floux.es:
  - Eventos: `PageView`, `ViewContent` (vídeo demo), `Lead` (click-to-WhatsApp), `Contact` (WhatsApp message sent), `CompleteRegistration` (demo agendada), `Subscribe` (cliente paga).
  - Deduplicación pixel + CAPI con `event_id`.
- **Conversions API Gateway** o server-side desde FastAPI (`/app/webhook/meta_capi.py` por crear).
- **Domain verification** floux.es en Business Manager.
- **Aggregated Event Measurement:** priorizar `Subscribe` > `CompleteRegistration` > `Contact` > `Lead` > `ViewContent`.
- **iOS 14.5+** considerado: usar valores de conversión 0-7 mapeados a precio único 97€.

---

## 2. Audiencias

### Custom Audiences (crear primero)
- `Web visitors 90d` — todo floux.es
- `Web visitors page /demo` (alta intención)
- `IG/FB engagers 365d`
- `Video viewers ≥50% Reel founder` 180d
- `WhatsApp openers` (CTWA) que NO convirtieron 30d
- `Clientes pagando` (lista CSV manual desde Stripe/admin)

### Lookalikes
- LAL 1% España de `Clientes pagando` (cuando haya 30+ seeds).
- LAL 1-2% de `Video viewers ≥50%`.
- LAL 2% de `WhatsApp openers cualificados`.

### Saved Audience (cold)
- **Geo:** radio 20km Majadahonda + códigos postales 28220, 28223, 28224, 28232 (Pozuelo), 28660 (Boadilla), 28230 (Las Rozas), 28670 (Villaviciosa), 28935 (Móstoles).
- **Edad:** 35-58.
- **Género:** todos (skew femenino orgánico).
- **Intereses (any of):** Treatwell, Booksy, Fresha, Hair salon, Beauty salon, Salon (business), Esthetician, Small business owner, Self-employed, Entrepreneurship.
- **Detailed targeting expansion:** OFF al inicio (forzar señal limpia).

---

## 3. Estructura de campaña

**Recomendación:** **Advantage+ Sales (ASC)** con `Subscribe` como conversión. Probar en paralelo manual con audiencia geo-locked.

### Setup recomendado (escenario 500€/mes)
```
Campaign 1: ASC — Advantage+ Sales
  └ Ad Set 1: Audience presets (España, 35-58, Spanish)
       Optimization: Subscribe (fallback: Lead)
       Budget: 12€/día
       └ Ad 1: Reel founder POV 30s
       └ Ad 2: Reel demo conversación 20s
       └ Ad 3: Static carrusel chat screenshots
       └ Ad 4: Story 9:16 testimonio dueña

Campaign 2: Manual — Cold Madrid Oeste
  └ Ad Set 1: Geo 20km + intereses salones
       Optimization: Lead (Click-to-WhatsApp)
       Budget: 5€/día
       └ Ad 1: Reel "3 llamadas perdidas hoy"
       └ Ad 2: Reel founder explicando dolor

Campaign 3: Retargeting (cuando haya tráfico)
  └ Ad Set 1: Web 30d + Engagers 90d (excluir clientes)
       Optimization: Subscribe
       Budget: 3€/día
       └ Ad: BOFU 97€/mes + CTA WhatsApp
```

---

## 4. Budget mínimo viable

- **Mínimo absoluto:** 5€/día por ad set (Meta necesita ~50 conversions/semana para optimizar — aquí trabajamos con `Lead` como proxy).
- **Recomendado:** 15€/día = 450€/mes para tener señal en 14 días.
- **Aprendizaje:** ~7-10 días en Learning Phase. NO tocar creativos ni budget en ese período.

---

## 5. Formatos — prioridad

1. **Reels (vertical 9:16)** — formato #1. 60% del presupuesto creativo. Founder POV o B-roll salón.
2. **Stories Ads (9:16)** — segundo. Para retargeting con urgencia ("¿Sigues perdiendo llamadas?").
3. **Feed Ads (1:1 o 4:5)** — terceros. Carrusel de screenshots de chat real.
4. **NO usar:** Audience Network, Right Column, Marketplace placements iniciales (calidad baja para B2B).
   - Placement: **Manual → solo IG Reels + IG Stories + FB Reels + IG Feed.**

---

## 6. Creative direction — hooks específicos

(Ver `creative-brief.md` para guía completa de copy/visual.)

**Top 5 hooks Meta:**
1. "3 llamadas perdidas hoy. Ninguna volverá a llamar."
2. "Tu Treatwell pesca online. ¿Quién pesca el teléfono fijo?"
3. "Las dueñas no pierden clientes por mal servicio. Los pierden por estar dando un buen servicio."
4. "97€ al mes. Se paga solo con UNA clienta recuperada."
5. "Le mando un WhatsApp en 30 segundos a cada llamada que no coges. ¿Te lo enseño?"

**Frame final estándar:** logo Floux + "floux.es" + CTA "Habla por WhatsApp" (botón nativo en CTWA campaigns).

---

## 7. Métricas a vigilar (dashboard semanal)

| Métrica | Target | Kill si |
|---|---|---|
| CPM | 6-10€ | >15€ 7d |
| Hook rate (3s) | >35% | <20% |
| CTR (link) | >1.5% | <0.7% |
| CTWA conv rate | >8% | <3% |
| CPL (Lead) | <40€ | >80€ |
| CAC blended | <250€ | >500€ |
| Frequency | <3.0 | >4.5 → refresh creativo |
