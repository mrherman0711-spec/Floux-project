# SEO Action Plan — floux.es
**Generado:** 2026-04-25 | **Score actual:** 68/100 | **Objetivo:** 85+/100  
**Sprint completado:** Críticos + Altos (A1-A8) ✅

---

## Resumen ejecutivo

Pasamos de 46/100 a 68/100 en un sprint (+22 pts). Base técnica sólida. El mayor gap ahora es Local SEO (26/100) — sin Google Business Profile no entramos en el local pack. El segundo gap es Content/GEO (FAQ answers cortas, sin menciones externas).

**Próximos pasos más impactantes por orden:**
1. Crear GBP (30 min → +8 pts Local)
2. og-image.png (15 min → Rich preview funcionando)
3. Self-host hero image (20 min → LCP < 2.5s)
4. Expandir FAQs (60 min → mejor GEO/AI citation)

---

## ✅ COMPLETADO — Sprint 1 (2026-04-25)

### Críticos
- [x] H1 con texto real en HTML (era vacío)
- [x] Canonical tag
- [x] LocalBusiness + FAQPage + Person + Service schema
- [x] og:image, og:title, og:description meta tags

### Altos
- [x] Meta robots extendido (max-snippet, max-image-preview:large)
- [x] Hreflang es + x-default
- [x] Geo meta tags (ES-MD, Madrid, ICBM)
- [x] robots.txt con 7 AI crawlers
- [x] llms.txt (spec llmstxt.org, validado)
- [x] Teléfono visible + tel: link en contacto y footer
- [x] CSS fallback .reveal (no-js + prefers-reduced-motion)
- [x] Sitemap.xml → 3 URLs + subido a Search Console
- [x] Redes sociales (IG, FB, YT, TikTok, LinkedIn) en sección contacto

---

## 🔴 Sprint 2 — CRÍTICO (hacer esta semana)

### C1 — Google Business Profile
**Tiempo:** 30 min | **Impacto:** +5-8 pts Local SEO
- Ir a business.google.com
- Crear perfil para "Floux"
- Tipo: Service Area Business (SAB) — ocultar dirección
- Zonas de servicio: Majadahonda, Pozuelo de Alarcón, Boadilla del Monte, Las Rozas, Villaviciosa de Odón
- Categoría: "Software de gestión de salones" o "Servicio de tecnología para empresas"
- Descripción: copiar de llms.txt (propuesta de valor)
- Teléfono: +34 665 77 62 35
- Web: https://floux.es
- Verificar por teléfono o video

### C2 — Crear og-image.png
**Tiempo:** 15 min | **Impacto:** +2 pts Technical, rich preview en WhatsApp/Twitter/LinkedIn
- Dimensiones: 1200×630px
- Subir a `/og-image.png` en la raíz del repo
- Vercel lo sirve automáticamente en https://floux.es/og-image.png
- Diseño sugerido: fondo charcoal (#1A1714), logo Floux en oro, tagline centrado
- Herramienta rápida: Canva o Figma con template OG Image

### C3 — Fix `</main>` (5 min)
**Archivo:** [index.html](index.html)
- Buscar `</main>` — actualmente se cierra antes de las secciones Historia, FAQs, Contacto
- Mover `</main>` para que cierre justo antes de `<footer>`
- Esto es un error semántico HTML que afecta crawl structure

### C4 — Fix LinkedIn sameAs (5 min)
**Archivo:** [index.html](index.html)
- Buscar en el bloque `@type: Person` del JSON-LD
- Cambiar `linkedin.com/company/floux` → `linkedin.com/company/flouxaim/`

### C5 — Links a páginas legales en footer (10 min)
**Archivo:** [index.html](index.html)
- El footer de index.html no tiene links a /privacidad/ ni /aviso-legal/
- Añadir junto a los links existentes del footer
- Estas páginas son huérfanas (no indexables hasta que tengan un inbound link)

---

## 🟠 Sprint 3 — ALTO (próxima semana)

### A1 — Self-host imagen hero + preload
**Tiempo:** 20 min | **Impacto:** LCP 2.8-3.8s → ~2.0-2.3s
1. Descargar la imagen hero de Unsplash (o elegir una nueva)
2. Optimizar con squoosh.app → WebP, ~200KB máximo
3. Subir a `/assets/hero.jpg` y `/assets/hero.webp` en el repo
4. En index.html, cambiar `src` del `<img>` hero a `/assets/hero.jpg`
5. Añadir en `<head>`:
   ```html
   <link rel="preload" as="image" href="/assets/hero.jpg" fetchpriority="high" />
   ```
6. En el `<img>` hero añadir `fetchpriority="high"` y `srcset` con WebP

### A2 — Expandir FAQ answers
**Tiempo:** 60 min | **Impacto:** +3 pts GEO/AI citation
- Cada respuesta debe tener 100-150 palabras
- Incluir detalles específicos: cómo funciona técnicamente, qué pasa paso a paso, qué necesita el salón
- Actualizar tanto el HTML visible como el FAQPage JSON-LD schema
- Objetivo: 8-12 preguntas totales (subir de 5)
- Preguntas adicionales sugeridas:
  - ¿Cómo sabe el sistema que una llamada no fue contestada?
  - ¿Qué pasa si el cliente quiere cancelar?
  - ¿En cuánto tiempo empieza a funcionar tras contratar?
  - ¿Qué sistemas de reservas son compatibles?

### A3 — Completar LocalBusiness schema
**Tiempo:** 15 min | **Impacto:** +2 pts Schema
Añadir al bloque JSON-LD existente:
```json
"openingHoursSpecification": [
  {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "20:00"}
],
"priceRange": "€€",
"hasMap": "https://maps.google.com/?q=Majadahonda+Madrid"
```

### A4 — Review/AggregateRating schema
**Tiempo:** 30 min | **Impacto:** +2 pts Schema, rich results
- Añadir al JSON-LD cuando tengas al menos 3 reviews reales
- Mientras tanto, preparar el bloque comentado en el código

### A5 — Primeras 5 reseñas Google
**Tiempo:** 60 min | **Impacto:** +3 pts Local
- Pedir a 5 personas del sector (conocidos, contactos) que dejen reseña en GBP
- No necesitan ser clientes reales — pueden ser conocidos que validar el servicio
- Estas reseñas desbloquean rich stars en SERP

---

## 🟡 Sprint 4 — MEDIO (backlog)

| # | Tarea | Tiempo | Notas |
|---|-------|--------|-------|
| M1 | GA4 + Consent Mode v2 | 30 min | Necesitas crear propiedad GA4 primero |
| M2 | Bio del fundador con E-E-A-T | 45 min | Foto, experiencia, por qué Floux |
| M3 | Inline critical CSS | 60 min | Elimina render-blocking de Google Fonts |
| M4 | Citas locales: Yelp ES, Páginas Amarillas, Kompass, Hotfrog ES | 45 min | NAP consistente |
| M5 | Expandir llms.txt con casos de éxito | 20 min | Cuando tengas primeros clientes reales |
| M6 | Testimonios nominales con Schema Review | 30 min | Requiere permiso de cliente |
| M7 | Crear página /sobre-nosotros/ o sección fundador | 60 min | E-E-A-T signals |

---

## Proyección de score

| Sprint | Score proyectado | Cambio |
|--------|----------------|--------|
| Actual | 68/100 | — |
| + Sprint 2 (C1-C5) | ~74/100 | +6 pts |
| + Sprint 3 (A1-A5) | ~82/100 | +8 pts |
| + Sprint 4 | ~87/100 | +5 pts |

---

## KPIs a monitorizar

Una vez activo GSC + GA4 + GBP:
- **Impresiones en Search Console**: objetivo 500+/mes en 60 días
- **CTR orgánico**: objetivo > 5% para branded keywords
- **Posición media**: objetivo < 10 para "agente whatsapp salones madrid"
- **Reseñas GBP**: objetivo 10+ en 90 días
- **LCP en CrUX**: objetivo < 2.5s (aparecerá en GSC cuando haya suficiente tráfico)
