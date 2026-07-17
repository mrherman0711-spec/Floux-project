# Plan de Implementación SEO — Floux.es
**Período:** Mayo 2026 – Abril 2027  
**Objetivo:** 85–90/100 SEO Health Score  
**Baseline:** 46/100 (2026-04-24)

---

## Resumen de fases

| Fase | Período | Focus | Score objetivo |
|---|---|---|---|
| Fase 1: Foundation | Semanas 1–4 (Mayo 2026) | Técnico + schema + infraestructura legal | 65/100 |
| Fase 2: Expansion | Semanas 5–12 (Jun–Jul 2026) | Contenido + local SEO + GBP | 72/100 |
| Fase 3: Scale | Semanas 13–24 (Ago–Oct 2026) | Casos de éxito + zonas + links | 78/100 |
| Fase 4: Authority | Meses 7–12 (Nov 2026–Abr 2027) | Thought leadership + PR + GEO avanzado | 85–90/100 |

---

## FASE 1 — Foundation (Semanas 1–4)
**Objetivo:** Resolver todos los Críticos + Altos del ACTION-PLAN. Score: 46 → 65.

### Semana 1 (28 abril – 4 mayo 2026)

#### Día 1–2: Correcciones en index.html + infraestructura
**Tiempo estimado: 4h**

- [ ] **Eliminar meta description duplicada** (línea 6 de index.html) — 2 min
- [ ] **Añadir `<meta name="robots">` con directivas extendidas** — 2 min
  ```html
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  ```
- [ ] **Añadir hreflang** — 3 min
- [ ] **Añadir geo meta tags + author** — 3 min
- [ ] **Añadir los 5 bloques JSON-LD** (WebSite + Organization + SoftwareApplication + Person + FAQPage) — 45 min
  - Verificar consistencia 95% vs 90% antes de añadir al FAQPage
  - Validar en https://search.google.com/test/rich-results tras el deploy
- [ ] **Arreglar CTAs mailto → #contacto + botón WhatsApp** — 30 min
  - Cambiar todos los `href="mailto:..."` en botones CTA a `href="#contacto"`
  - Añadir `<a href="https://wa.me/34632842510">` en sección contacto
  - Añadir barra flotante móvil con CTA WhatsApp
- [ ] **Crear vercel.json** con security headers — 20 min
- [ ] **Fix scroll-reveal CSS** (opacity: 0 → 1 por defecto) — 15 min
- [ ] **Mover `</main>`** para envolver Historia + FAQs + Contacto — 5 min
- [ ] **Deploy y validar** — 10 min
  - Rich Results Test
  - Verificar CTAs en móvil (iOS Safari + Android Chrome)

#### Día 3–4: Infraestructura GEO + local
- [ ] **Crear llms.txt** en raíz del proyecto — 20 min
- [ ] **Actualizar robots.txt** con AI crawlers — 5 min
- [ ] **Añadir número de teléfono** a sección contacto y footer — 5 min
- [ ] **Añadir frase de definición** bajo el H1 del hero — 15 min

#### Día 5–7: Legal + tracking
- [ ] **Crear política de privacidad** (`/privacidad`) — 2h
- [ ] **Crear aviso legal** (`/aviso-legal`) — 1h
- [ ] **Añadir enlace en footer** a ambas páginas
- [ ] **Añadir checkbox RGPD** en el formulario de contacto
- [ ] **Instalar Google Analytics 4** (sin cookies por defecto, modo consent v2) — 30 min
- [ ] **Configurar Google Search Console** + verificar floux.es — 15 min
- [ ] **Enviar sitemap a GSC** — 5 min

---

### Semana 2 (5–11 mayo 2026)

#### Google Business Profile
- [ ] **Crear GBP** en business.google.com — 30 min
  - Tipo: Service Area Business
  - Categoría: "Software Company"
  - Zonas: las 5 municipios + Madrid
  - Email: max@floux.es | Teléfono: +34 632 842 510
- [ ] **Verificar GBP** (video verification — preparar vídeo mostrando el producto/pantalla) — 1h
- [ ] **Completar perfil GBP** (descripción, fotos, servicios) — 1h
- [ ] **Configurar mensajería WhatsApp** en GBP (integración nativa disponible)

#### Optimizaciones técnicas de performance
- [ ] **Preload hero image** + `fetchpriority="high"` — 10 min
- [ ] **Google Fonts no-blocking** (media=print trick) — 10 min
- [ ] **`loading="lazy"` + `width`/`height`** en todas las imágenes excepto hero — 10 min
- [ ] **Añadir `&fm=webp&q=80`** a todas las URLs de Unsplash — 15 min
- [ ] **Renderizar H1 en HTML** (quitar JS split-text) — 20 min

---

### Semana 3 (12–18 mayo 2026)

#### Contenido copy fixes
- [ ] **Fix voseo** "Pagás" → "Pagas" — 2 min
- [ ] **Reconciliar porcentajes** 95%/90% — 5 min
- [ ] **Añadir "peluquería"** en footer y FAQ — 5 min
- [ ] **Reencuadrar Historia** — primero resultados, luego story — 30 min
- [ ] **Mockup conversación WhatsApp** en homepage — 1h
- [ ] **Añadir `<meta name="author">`** — 2 min

#### Directorios Tier 1
- [ ] **Capterra España** — crear listing gratuito — 20 min
- [ ] **Bing Places for Business** — sync con GBP — 15 min
- [ ] **LinkedIn Company Page** — crear + enlazar desde footer — 30 min

---

### Semana 4 (19–25 mayo 2026)

#### Primer artículo de blog + infraestructura de blog
- [ ] **Crear estructura de blog** en Vercel (nueva sección `/blog/`) — 2h
  - HTML template para posts (con schema Article + FAQPage integrado)
  - Navegación y links internos
- [ ] **Escribir Post 1**: "Cuánto pierde una peluquería al mes por llamadas sin respuesta" — 3h
  - Usar datos reales de Escultor Peluquería
  - Publicar con schema Article + FAQPage
- [ ] **Actualizar sitemap.xml** para incluir el nuevo post

**Checkpoint Fase 1 — KPIs esperados:**
- SEO Health Score: 65/100
- Schema markup: Funcionando (verificado en Rich Results Test)
- GBP: Creado y en proceso de verificación
- GSC: Configurado, site indexado
- GA4: Instalado, tracking conversiones básico
- Primer artículo publicado

---

## FASE 2 — Expansion (Semanas 5–12)
**Objetivo:** Contenido + local + GBP activo. Score: 65 → 72.

### Semana 5–6 (26 mayo – 8 junio)
- [ ] **Post 2**: "Qué es un agente de WhatsApp para salones de estética" — 3h
  - Requiere capturas reales de conversación
- [ ] **Página de zona Majadahonda** (`/majadahonda/`) — 2h
- [ ] **Solicitar primera reseña** a Escultor Peluquería (link directo GBP)
- [ ] **GBP: primer post** semanal (comenzar cadencia)

### Semana 7–8 (9–22 junio)
- [ ] **Post 3**: "Por qué los clientes no vuelven a llamar tras una llamada perdida" — 3h
- [ ] **Página de zona Pozuelo** (`/pozuelo-de-alarcon/`) — 2h
- [ ] **Capterra**: completar perfil, solicitar primera reseña
- [ ] **Outreach Tier 1**: contactar 2 artículos que rankean sin mencionar Floux

### Semana 9–10 (23 junio – 6 julio)
- [ ] **Post 4**: "Floux vs Booksy — cuál necesita tu salón" — 3h
- [ ] **Submisión a directorios Tier 2**: Páginas Amarillas, Kompass, AXESOR — 1h
- [ ] **GSC review**: analizar primeras impresiones, ajustar keywords si necesario

### Semana 11–12 (7–20 julio)
- [ ] **Página de zona Las Rozas** (`/las-rozas/`) — 2h
- [ ] **Testimonios**: recopilar 2–3 testimonios de clientes para homepage
- [ ] **Añadir sección testimonios** a homepage con aggregateRating schema
- [ ] **IndexNow key**: registrar en Bing + automatizar via deploy hook

**Checkpoint Fase 2 — KPIs esperados:**
- Tráfico orgánico: 50+ visitas/mes
- Keywords posicionadas: 3–5 en top 20
- GBP: Verificado + 3+ reseñas
- Posts publicados: 4
- Páginas de zona: 3

---

## FASE 3 — Scale (Semanas 13–24)
**Objetivo:** Autoridad local + casos de éxito + distribución. Score: 72 → 78.

### Mes 4 (Agosto 2026)
- [ ] **Post 5**: "Cómo automatizar WhatsApp en tu peluquería" — 3h
- [ ] **Página de zona Boadilla** (`/boadilla-del-monte/`) — 2h
- [ ] **Actualizar homepage** con datos reales (reemplazar "15 clientes" genérico por dato real con atribución)
- [ ] **Video demo** (prioridad alta en agosto — correlación GEO 0.737): grabar flujo WhatsApp de 2 min, publicar en YouTube + incrustar en homepage

### Mes 5 (Septiembre 2026)
- [ ] **Post 6 — Caso de éxito real** — 3h (requiere testimonial firmado de cliente activo)
- [ ] **Página de zona Villaviciosa** (`/villaviciosa-de-odon/`) — 2h
- [ ] **Outreach Tier 1**: segunda ronda de contacto a listicles (seguimiento)
- [ ] **Reddit**: publicar 2–3 respuestas útiles en r/emprendedores y r/peluqueria

### Mes 6 (Octubre 2026)
- [ ] **Post 7**: "Las mejores herramientas para salones de estética en Madrid 2026" — 3h
- [ ] **Añadir página hub `/madrid-oeste/`** que enlaza a todas las páginas de zona
- [ ] **G2 listing**: crear perfil básico en g2.com
- [ ] **GSC deep review**: identificar queries con impresiones pero sin clicks (títulos/metas a optimizar)

**Checkpoint Fase 3 — KPIs esperados:**
- Tráfico orgánico: 200+ visitas/mes
- Keywords posicionadas top 10: 10–15
- GBP: 8+ reseñas, perfil completo
- Posts publicados: 7
- Páginas de zona: 5 (completas)
- Primer caso de éxito publicado
- Video demo en YouTube

---

## FASE 4 — Authority (Meses 7–12)
**Objetivo:** Thought leadership + AI citation + dominio de queries locales. Score: 78 → 85–90.

### Mes 7–8 (Nov–Dic 2026)
- [ ] **Post 8**: "Alternativas a Treatwell para peluquerías en Madrid" — 3h
- [ ] **Post 9**: Contenido estacional navidades — 2h
- [ ] **Outreach Tier 2**: Estetica Magazine, Bellezaconecta — pitch artículo de opinión o datos exclusivos
- [ ] **Actualizar todos los posts** con datos frescos (Q3 Floux data)
- [ ] **Implementar schema HowTo** en posts con pasos claros
- [ ] **Reddit AMA** en r/emprendedores: "Monté un agente WhatsApp para peluquerías en Madrid — AMA" — alto impacto GEO

### Mes 9–10 (Ene–Feb 2027)
- [ ] **Post 10**: "Tendencias automatización salones 2027" — 3h
- [ ] **Informe original**: "El mercado de salones de estética en Madrid Oeste — datos Floux 2026" — pieza de linkbuilding de alto valor
- [ ] **Outreach Tier 3**: medios locales Madrid Oeste (hook: emprendedor local)
- [ ] **Actualizar llms.txt** con nuevas páginas y estadísticas
- [ ] **Calcular GEO score** con herramienta manual: buscar "agente whatsapp salones madrid" en ChatGPT/Perplexity y verificar si Floux es citado

### Mes 11–12 (Mar–Abr 2027)
- [ ] **Segundo caso de éxito** — 2h
- [ ] **Optimización avanzada** basada en datos GSC de 12 meses:
  - Expandir posts con alto CTR pero baja posición
  - Añadir FAQ sections a posts que rankean sin FAQPage
  - Actualizar schema con aggregateRating real (objetivo: 10+ reseñas)
- [ ] **Auditoría SEO de seguimiento** — comparar vs baseline 2026-04-24

**Checkpoint Final — KPIs esperados (Abril 2027):**
- SEO Health Score: 85–90/100
- Tráfico orgánico: 800+ visitas/mes
- Keywords top 10: 30+
- GBP: 20+ reseñas
- Posts publicados: 12+
- Páginas indexadas: 20+
- Backlinks: 25+
- Demos vía orgánico: 20–30/mes
- AI citations: 15+ (verificadas manualmente en ChatGPT/Perplexity)

---

## Dependencias críticas del plan

| Dependencia | Bloqueante para | Fecha límite |
|---|---|---|
| Capturas reales de conversación WhatsApp | Post 2 + mockup homepage | 1 mayo 2026 |
| Datos Escultor Peluquería (llamadas/mes, recuperaciones) | Post 1 | 1 mayo 2026 |
| Foto del fundador | Historia section + GBP + posts | 15 mayo 2026 |
| Testimonial firmado (cliente activo) | Post caso de éxito | 1 septiembre 2026 |
| CIF de empresa (si aplica) | Aviso Legal completo | 7 mayo 2026 |
| GSC + GA4 instalados | Medir todo el contenido | 7 mayo 2026 |

---

## Recursos requeridos

| Tarea | Tiempo estimado | Frecuencia |
|---|---|---|
| Correcciones técnicas index.html | 4h | Una vez (semana 1) |
| Infraestructura blog (template) | 2h | Una vez (semana 4) |
| Post de blog | 3–4h | 1–2 por mes |
| Página de zona | 2h | 1 por mes (meses 2–6) |
| GBP gestión (posts + responder reseñas) | 30 min/semana | Semanal |
| GSC review + optimización | 1h | Mensual |
| Outreach directorios y listicles | 1–2h | Mensual |
| **Total mes 1** | **~25h** | — |
| **Total meses 2–6** | **~12h/mes** | — |
| **Total meses 7–12** | **~8h/mes** | — |

---

*Revisar este roadmap mensualmente. Prioridades pueden cambiar según datos reales de GSC y GSC insights.*
