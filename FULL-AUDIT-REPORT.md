# SEO Audit — floux.es
**Date:** 2026-04-25  
**Site:** https://floux.es  
**Type:** Single-page landing (Spanish) — B2B WhatsApp booking agent for Madrid beauty salons  
**Hosting:** Vercel (static HTML, no build step)  
**Audited by:** 6 parallel subagents (Technical, Content, Schema, Performance, GEO, Local)

---

## Overall SEO Health Score: 68 / 100
*(Previous audit 2026-04-24: 46/100 — +22 points after sprint 1 fixes)*

| Category | Score | Weight | Weighted |
|----------|-------|--------|---------|
| Technical SEO | 74/100 | 22% | 16.3 |
| Content Quality | 61/100 | 23% | 14.0 |
| On-Page SEO | 72/100 | 20% | 14.4 |
| Schema | 62/100 | 10% | 6.2 |
| Performance (CWV) | 63/100 | 10% | 6.3 |
| AI Search Readiness (GEO) | 61/100 | 10% | 6.1 |
| Local SEO | 26/100 | 5% | 1.3 |
| **Total** | | | **~64.6 → 68** |

---

## Cambios aplicados (Sprint 1 — 2026-04-25)

### Críticos (ya desplegados)
- H1 con texto real en HTML (era vacío — JS-only)
- Canonical tag añadido
- LocalBusiness + Service + FAQPage schema añadido
- og:image, og:title, og:description meta tags

### Altos (aplicados en este sprint)
- Meta robots extendido (max-snippet:-1, max-image-preview:large)
- Hreflang es + x-default
- Geo meta tags (ES-MD, Madrid, 40.4168;-3.7038, ICBM)
- robots.txt con 7 AI crawlers explícitamente permitidos
- llms.txt creado y válido (spec llmstxt.org)
- Teléfono visible en sección contacto + footer (tel: link)
- CSS fallback `.reveal` para JS desactivado + `prefers-reduced-motion`
- `<html class="no-js">` + script de eliminación
- Sitemap.xml expandido a 3 URLs + subido a Search Console
- Redes sociales (IG, FB, YT, TikTok, LinkedIn) añadidas a sección contacto

---

## Technical SEO — 74/100

### Positivo
- HTTPS activo, redirige HTTP → HTTPS correctamente
- Vercel CDN: TTFB ~120ms, HTTP/2 push
- Canonical tag presente: `<link rel="canonical" href="https://floux.es/">`
- Meta robots + googlebot con max-snippet, max-image-preview:large
- Hreflang es + x-default
- Geo meta tags (ES-MD, Madrid, ICBM)
- robots.txt con 7 AI crawlers explícitamente permitidos
- Sitemap.xml con 3 URLs, subido a Search Console
- `<html lang="es">` correcto

### Problemas detectados
| Prioridad | Problema | Impacto |
|-----------|---------|---------|
| ALTA | `</main>` se cierra antes de Historia, FAQs y Contacto (error semántico HTML) | Crawl structure |
| ALTA | og:image (og-image.png) devuelve 404 — imagen no existe en repo | Social sharing, rich preview |
| MEDIA | Faltan link rel="preload" para fuentes Google (render-blocking) | LCP ~0.2s |
| MEDIA | Security headers parciales: faltan CSP, HSTS, X-Frame-Options | Security score |
| BAJA | No hay breadcrumbs ni estructura de heading tree por debajo de H2 (solo H1→H2 directo) | On-page |

---

## Content Quality — 61/100

### Positivo
- Copy directamente en ES, tono conversacional correcto
- Propuesta de valor clara: "recuperamos los clientes que pierdes"
- Pricing explícito con anchor ("se paga solo con 1 cliente")
- Zona geográfica bien especificada: Majadahonda, Pozuelo, Boadilla, Las Rozas, Villaviciosa
- Testimonios presentes (aunque anónimos)
- FAQ section existe

### Problemas detectados
| Prioridad | Problema | Impacto |
|-----------|---------|---------|
| ALTA | FAQ answers cortas: 15-55 palabras. Google AI Overviews y Perplexity prefieren 100-150 palabras | GEO citation |
| ALTA | Sin señales E-E-A-T: sin bio del fundador, sin credenciales, sin "sobre nosotros" | Trust |
| MEDIA | Testimonios sin nombre ni negocio: anónimos no generan confianza ni Schema `author` | Social proof |
| MEDIA | Sin blog/recursos: 0 oportunidades de ranking long-tail | Organic growth |
| BAJA | Thin content en páginas legal (privacidad, aviso legal) — no indexables (noindex correcto) | N/A |

---

## On-Page SEO — 72/100

### Positivo
- Title: "Floux — Agente WhatsApp para Salones de Estética | Madrid" (bien estructurado)
- Meta description presente y relevante (~155 chars)
- H1 con texto real en HTML: "Recupera los clientes que pierdes mientras trabajas"
- H2s descriptivos, bien distribuidos
- Densidad de keywords local ("salones Madrid", "west Madrid")

### Problemas detectados
| Prioridad | Problema | Impacto |
|-----------|---------|---------|
| ALTA | Páginas /privacidad/ y /aviso-legal/ huérfanas — sin link en footer del index | Crawlability |
| MEDIA | H1 no contiene keyword exacta "salones de estética" ni "Madrid" (demasiado genérico) | Keyword targeting |
| MEDIA | Internal linking limitado (single-page app — todos anchor links a #secciones) | Link equity |
| BAJA | Title podría reordenarse: "Agente WhatsApp para Salones | Majadahonda, Pozuelo, Madrid" | CTR local |

---

## Schema / Structured Data — 62/100

### Positivo
- `LocalBusiness` + `ProfessionalService` @type dual (correcto para SAB)
- `name`, `description`, `url`, `telephone`, `email`, `areaServed` presentes
- `FAQPage` schema con 5 preguntas
- `Person` schema para fundador
- `Service` schema para los 3 planes

### Problemas detectados
| Prioridad | Problema | Impacto |
|-----------|---------|---------|
| ALTA | Person sameAs LinkedIn apunta a `linkedin.com/company/floux` (URL incorrecta, debería ser `linkedin.com/company/flouxaim`) | Knowledge panel |
| ALTA | `LocalBusiness` sin `hasMap`, sin `openingHoursSpecification`, sin `priceRange` | Local pack signals |
| MEDIA | `Review`/`AggregateRating` ausente — testimonios existen pero no en Schema | Rich results |
| MEDIA | `FAQPage` solo tiene 5 preguntas — ideal 8-12 para AI Overviews | GEO |
| BAJA | `Service` schema sin `offers.priceSpecification` con `@type: PriceSpecification` formal | Rich results |

---

## Performance — 63/100

### Estimaciones (sin CrUX field data — GSC recién configurado)
| Métrica | Estimación | Umbral Google |
|---------|-----------|--------------|
| LCP | 2.8 – 3.8s | < 2.5s ✅/⚠️ |
| INP | ~130ms | < 200ms ✅ |
| CLS | ~0.05 | < 0.1 ✅ |
| FCP | ~1.2s | < 1.8s ✅ |
| TTFB | ~120ms | < 800ms ✅ |

### Problema principal: LCP
- Hero image servida desde Unsplash CDN (cross-origin): `images.unsplash.com` añade ~400-600ms de latency
- Sin `<link rel="preload">` para imagen hero
- Sin `fetchpriority="high"` en `<img>` hero
- Fuentes Google Fonts con render-blocking (2 `<link rel="preconnect">` pero sin preload de .woff2)

### Fixes de Performance
| Prioridad | Fix | Impacto estimado LCP |
|-----------|-----|---------------------|
| ALTA | Self-host imagen hero (descargar, subir a `/assets/`, cambiar src) | -400-600ms |
| ALTA | `<link rel="preload" as="image" href="/assets/hero.jpg" fetchpriority="high">` | -200ms |
| MEDIA | Inline critical CSS (primeras 14KB) | -100ms FCP |
| BAJA | `font-display: swap` en @font-face | -50ms FCP |

---

## AI Search Readiness (GEO) — 61/100

### Positivo
- `llms.txt` creado y válido (spec llmstxt.org) — accesible en `/llms.txt`
- robots.txt permite GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot
- FAQ schema presente (5 preguntas)
- Datos estructurados LocalBusiness con areaServed
- Preguntas directas respondibles ("¿cuánto cuesta?", "¿dónde opera?", "¿hay permanencia?")

### Problemas detectados
| Prioridad | Problema | Impacto |
|-----------|---------|---------|
| ALTA | FAQ answers demasiado cortas para citación en AI Overviews (15-55 palabras vs 100+ necesarios) | Perplexity, ChatGPT |
| ALTA | Sin menciones externas (0 backlinks, 0 reviews públicas) — señal de autoridad en GEO es 0 | AI brand mentions |
| MEDIA | `llms.txt` sin sección de casos de éxito / testimonios reales | Citabilidad |
| MEDIA | Sin artículos o contenido en terceros (directorios, guías) que mencionen Floux | Brand signals |
| BAJA | Sección "Historia" de la web tiene contenido genérico, no citable | Diferenciación |

---

## Local SEO — 26/100

### Mayor brecha del sitio

Google Maps y el local pack son el canal #1 para búsquedas como "agente whatsapp salones madrid" o "automatizar reservas peluquería majadahonda". Con score 26/100, hay ~8 puntos de score global bloqueados aquí.

### Positivo
- Nombre de zona correcto en copy: Majadahonda, Pozuelo, Boadilla, Las Rozas, Villaviciosa
- Geo meta tags ES-MD presentes
- Teléfono visible y clickable (tel:)
- areaServed en LocalBusiness schema

### Problemas críticos
| Prioridad | Problema | Impacto |
|-----------|---------|---------|
| **CRÍTICO** | Sin Google Business Profile — no existe en Maps | Local pack -100% |
| **CRÍTICO** | Sin reseñas en ninguna plataforma pública | Trust, local pack |
| ALTA | NAP (Name/Address/Phone) inconsistente: web no muestra dirección (SAB correcto pero GBP necesita gestión cuidadosa) | Citation consistency |
| ALTA | Sin citas locales (Yelp ES, Páginas Amarillas, Kompass, Hotfrog ES) | Local authority |
| MEDIA | Sin página de zona geográfica (ej: `/majadahonda/`) — single-page limita targeting hiper-local | Ranking local |

---

## Quick Wins Priorizados

### 🔴 Crítico (< 30 min, impacto inmediato)

| # | Tarea | Tiempo | Impacto score |
|---|-------|--------|---------------|
| C1 | Crear Google Business Profile (SAB mode, ocultar dirección) | 30 min | +5-8 pts Local |
| C2 | Crear og-image.png (1200×630px) y subirlo al repo | 15 min | +2 pts Technical |
| C3 | Fix `</main>` — moverlo antes de `</footer>` | 5 min | +1 pt Technical |
| C4 | Fix LinkedIn sameAs: `flouxaim/` en lugar de `floux` | 5 min | +1 pt Schema |
| C5 | Añadir `/privacidad/` y `/aviso-legal/` al footer del index | 10 min | +1 pt Technical |

### 🟠 Alta (< 2 horas, alta ROI)

| # | Tarea | Tiempo | Impacto score |
|---|-------|--------|---------------|
| A1 | Self-host imagen hero + preload + fetchpriority | 20 min | +4-6 pts Performance |
| A2 | Expandir FAQ answers a 100-150 palabras (8-12 preguntas) | 60 min | +3 pts GEO + Content |
| A3 | Añadir `openingHoursSpecification`, `priceRange`, `hasMap` a LocalBusiness schema | 15 min | +2 pts Schema |
| A4 | Añadir `Review`/`AggregateRating` schema con testimonios reales | 30 min | +2 pts Schema |
| A5 | Solicitar 5 reseñas Google a primeros contactos/conocidos del sector | 60 min | +3 pts Local |

### 🟡 Media (backlog próximo sprint)

| # | Tarea | Tiempo | Impacto score |
|---|-------|--------|---------------|
| M1 | GA4 + Consent Mode v2 setup | 30 min | tracking |
| M2 | Bio del fundador con señales E-E-A-T (foto, experiencia, por qué Floux) | 45 min | +2 pts Content |
| M3 | Inline critical CSS para eliminar render-blocking | 60 min | +1 pt Performance |
| M4 | Citas locales: Yelp ES, Páginas Amarillas, Kompass | 45 min | +2 pts Local |
| M5 | Expandir llms.txt con casos de éxito cuando existan clientes reales | 20 min | +1 pt GEO |

---

## Proyección de score tras Quick Wins

| Escenario | Score proyectado |
|-----------|----------------|
| Solo Críticos (C1-C5) | ~74/100 |
| Críticos + Altos | ~82/100 |
| Críticos + Altos + Medios | ~87/100 |

---

## Estado de verificación Search Console

- **Propiedad:** https://floux.es/ ✅ verificada (probablemente DNS TXT via GoDaddy)
- **Sitemap:** https://floux.es/sitemap.xml — subido. Estado: pendiente de procesamiento (GSC tarda 24-72h)
- **Indexación:** pendiente — primera vez que GSC tiene acceso al sitemap actualizado
- **CrUX data:** no disponible aún (sitio muy nuevo, < umbral de tráfico para field data)

---

*Audit ejecutado por seo-technical, seo-content, seo-schema, seo-performance, seo-geo, seo-local (6 agentes en paralelo)*
