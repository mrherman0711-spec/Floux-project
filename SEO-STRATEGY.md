# Estrategia SEO — Floux.es
**Versión:** 1.0 | **Fecha:** 2026-04-24 | **Objetivo:** 85–90/100 SEO Health Score  
**Baseline:** 46/100 (auditoría 2026-04-24)

---

## 1. Perfil del negocio

| Campo | Detalle |
|---|---|
| Empresa | Floux |
| Tipo | SaaS B2B + Service Area Business (SAB) |
| Producto | Agente WhatsApp IA para salones de estética y peluquerías |
| Mercado | Madrid Oeste — Majadahonda, Pozuelo, Las Rozas, Boadilla, Villaviciosa, Chamberí |
| Propuesta de valor | "Recupera los clientes que pierdes cuando no puedes coger el teléfono" |
| Precios | €47 / €97 / €147 por mes, sin permanencia |
| Fundador | Max Herman (UEM) |
| Email | max@floux.es · WhatsApp: +34632842510 |
| Stack | WhatsApp Business API + OpenAI + Twilio + FastAPI + Railway |
| Competencia SEO directa | AvisoVoz, Triviat, Salonexa |
| Competencia indirecta | Booksy, Fresha, Treatwell (booking platforms) |

---

## 2. Diagnóstico actual

### Score por categoría (auditoría 2026-04-24)

| Categoría | Score actual | Objetivo 12m |
|---|---|---|
| Technical SEO | 51/100 | 88/100 |
| Content / E-E-A-T | 58/100 | 82/100 |
| Schema Markup | 0/100 | 90/100 |
| Performance (CWV) | 45/100 | 76/100 |
| AI Search (GEO) | 31/100 | 74/100 |
| Local SEO | 31/100 | 70/100 |
| **Overall** | **46/100** | **85–90/100** |

### Gaps críticos identificados
1. **Cero schema markup** — mayor brecha absoluta (+85 pts potenciales)
2. **CTAs rotos en móvil** — todos los botones abren mailto:
3. **Riesgo legal RGPD** — sin política de privacidad
4. **Google Business Profile ausente** — 0/25 en local SEO
5. **GEO score 31/100** — invisible para ChatGPT, Perplexity, AI Overviews
6. **Mismatch de tipo de página** — Google premia contenido editorial para queries informacionales; Floux solo tiene una LP

### Fortalezas a mantener
- Copy en español de alta calidad, tono auténtico y local
- Diseño premium, zero JS bloat, Vercel edge (TTFB ~80ms)
- Densidad local orgánica (municipios de Madrid Oeste mencionados naturalmente)
- Frase de posicionamiento diferencial clara

---

## 3. Análisis de intención de búsqueda

### Mapa de keywords por etapa del funnel

#### Top of Funnel — Informacional (educación del mercado)
| Keyword | Vol. estimado | Dificultad | Tipo de página |
|---|---|---|---|
| cómo no perder clientes peluquería | Alto | Media | Artículo blog |
| llamadas perdidas solución negocio | Medio | Baja | Artículo blog |
| automatizar whatsapp salón belleza | Medio | Baja | Artículo blog |
| cuánto pierde un salón por llamadas sin respuesta | Bajo | Muy baja | Artículo blog |
| qué es un agente de whatsapp | Medio | Baja | Artículo definitional |

#### Middle of Funnel — Comercial investigativo
| Keyword | Vol. estimado | Dificultad | Tipo de página |
|---|---|---|---|
| software reservas salón madrid | Medio | Media | LP + comparativa |
| agente whatsapp salones | Bajo-medio | Baja | Homepage / LP |
| asistente whatsapp peluquería madrid | Bajo | Muy baja | Homepage |
| mejor software peluquería madrid 2026 | Bajo | Baja | Comparativa / roundup |
| alternativas booksy madrid | Bajo | Baja | Página comparativa |

#### Bottom of Funnel — Transaccional
| Keyword | Vol. estimado | Dificultad | Tipo de página |
|---|---|---|---|
| recuperar llamadas perdidas salón madrid | Muy bajo | Muy baja | Homepage |
| floux madrid | Branded | N/A | Homepage |
| agente whatsapp majadahonda | Muy bajo | Muy baja | Página de zona |
| recuperar clientes peluquería pozuelo | Muy bajo | Muy baja | Página de zona |

**Insight clave:** El volumen en BoFu es bajo porque la categoría es nueva (Floux la está creando). La estrategia correcta es capturar el tráfico informacional de ToFu y educarlo — no esperar a que exista volumen transaccional.

---

## 4. Estrategia de contenido

### Modelo de clusters temáticos

```
PILLAR 1: Recuperación de clientes perdidos
├── Hub: "Cómo recuperar clientes perdidos en peluquería y salón" (landing page)
├── "Cuánto pierde un salón por llamadas sin respuesta — calculadora"
├── "Por qué los clientes no vuelven a llamar tras una llamada perdida"
├── "5 formas de recuperar clientes que no contestaste"
└── "Caso de éxito: salón recupera 18 clientes al mes en Majadahonda"

PILLAR 2: WhatsApp para negocios de belleza
├── Hub: "WhatsApp Business para salones de estética — guía completa"
├── "Qué es un agente de WhatsApp y cómo funciona para un salón"
├── "Diferencia entre WhatsApp Business y un agente conversacional"
├── "Cómo automatizar respuestas de WhatsApp en tu peluquería"
└── "Ejemplos de conversaciones de WhatsApp para salones de belleza"

PILLAR 3: Software y herramientas para salones en Madrid
├── Hub: "Las mejores herramientas para salones de estética en Madrid 2026"
├── "Floux vs Booksy: qué necesita realmente tu salón"
├── "Floux vs Fresha: diferencias clave para salones en Madrid"
├── "Alternativas a Treatwell para peluquerías en Madrid"
└── "Cómo elegir el software de reservas para tu salón"

PILLAR 4: Páginas de zona (local SEO)
├── Hub: "Floux para salones de estética en Madrid Oeste"
├── /majadahonda — Agente WhatsApp para salones en Majadahonda
├── /pozuelo-de-alarcon — Agente WhatsApp para salones en Pozuelo
├── /las-rozas — Agente WhatsApp para salones en Las Rozas
├── /boadilla-del-monte — Agente WhatsApp para salones en Boadilla
└── /villaviciosa-de-odon — Agente WhatsApp para salones en Villaviciosa
```

### Criterios de calidad para cada pieza de contenido
- Mínimo 1.200 palabras por artículo de blog
- Al menos 1 estadística atribuida (fuente real o "estudio interno Floux")
- Al menos 1 CTA natural al producto integrado en el contenido
- Schema markup: Article + FAQPage en posts con FAQ
- Todas las respuestas de FAQ: 120–200 palabras con un dato cuantificado
- Imágenes: capturas reales del producto o conversaciones WhatsApp (no stock genérico)

---

## 5. Estrategia técnica

### Arquitectura de información objetivo

```
floux.es/
├── / (Homepage — LP principal)
├── /blog/
│   ├── /como-recuperar-clientes-peluqueria/
│   ├── /agente-whatsapp-salones-estetica/
│   ├── /cuanto-pierde-salon-llamadas-perdidas/
│   └── ... (8–12 posts en 12 meses)
├── /comparar/
│   ├── /floux-vs-booksy/
│   ├── /floux-vs-fresha/
│   └── /alternativas-treatwell-madrid/
├── /madrid-oeste/  (hub de zona)
│   ├── /majadahonda/
│   ├── /pozuelo-de-alarcon/
│   ├── /las-rozas/
│   ├── /boadilla-del-monte/
│   └── /villaviciosa-de-odon/
├── /privacidad/
├── /aviso-legal/
└── llms.txt
```

### Schema por tipo de página

| Página | Schema types |
|---|---|
| Homepage | WebSite + Organization + SoftwareApplication + Person + FAQPage |
| Blog posts | Article + BlogPosting + FAQPage (si tiene FAQ) |
| Páginas de zona | LocalBusiness (SAB) + ProfessionalService + FAQPage local |
| Comparativas | Article + FAQPage |
| /privacidad | WebPage |

### Core Web Vitals targets

| Métrica | Actual (estimado) | Target 3m | Target 12m |
|---|---|---|---|
| LCP | ~3.0s | < 2.5s | < 2.0s |
| INP | ~100ms | < 150ms | < 100ms |
| CLS | ~0.05 | < 0.05 | < 0.02 |
| TTFB | ~100ms | < 100ms | < 80ms |

---

## 6. Estrategia local SEO

### Google Business Profile (prioridad #1)
- Crear perfil SAB en business.google.com
- Categoría primaria: "Software Company"
- Añadir hasta 9 categorías secundarias (ej: "Business Management Software")
- Zonas: listar cada municipio individualmente (no "Madrid" como ciudad genérica)
- Subir 10+ fotos: logo, capturas de producto, foto del fundador, mockups de conversación
- Descripción: 750 chars, incluir keywords primarios
- Cadencia de posts GBP: 1 post/semana con CTA
- Objetivo: 5+ reseñas en primeros 60 días

### Estrategia de reseñas
1. Pedir reseña a cada cliente activo (Escultor Peluquería + futuros)
2. Crear link directo de reseña de Google y enviarlo por WhatsApp
3. Plantilla de solicitud: "Hola [nombre], ¿te ha ido bien Floux este mes? Si tienes 2 minutos, me ayudaría mucho una reseña aquí: [link]"
4. Objetivo: 1–2 reseñas/mes a partir del mes 2
5. Responder a todas las reseñas en < 48h

### Directorios de citas (NAP consistency)
Prioridad y orden de registro:
1. Google Business Profile (Critical)
2. Capterra España (High — SaaS-specific, citado por AI)
3. Bing Places for Business (High)
4. LinkedIn Company Page (High)
5. Páginas Amarillas (Medium)
6. Kompass España (Medium)
7. AXESOR (Medium)
8. G2 (Low — construir reseñas a partir del mes 6)

**NAP estándar a usar en todos:**
- Nombre: Floux
- Teléfono: +34 632 842 510
- Email: max@floux.es
- URL: https://floux.es
- Ciudad: Madrid (Majadahonda, Pozuelo de Alarcón, Las Rozas, Boadilla del Monte, Villaviciosa de Odón)

---

## 7. Estrategia GEO (AI Search)

### Objetivo: ser la fuente citada cuando alguien pregunta a ChatGPT/Perplexity "cómo recuperar clientes perdidos en una peluquería en Madrid"

### Acciones técnicas
- [ ] Implementar FAQPage schema con respuestas de 120–200 palabras
- [ ] Crear llms.txt con definición de entidad y links
- [ ] Añadir frase de definición en primer párrafo de homepage
- [ ] Actualizar robots.txt con GPTBot, ClaudeBot, PerplexityBot permitidos

### Acciones de contenido
- [ ] Artículo definitional: "Qué es un agente de WhatsApp para salones de estética" (500+ palabras, autorreferencial)
- [ ] Estadísticas propias atribuibles (llamadas perdidas, tasa de recuperación, ROI)
- [ ] Estructurar todas las páginas de blog con introducción en forma de respuesta directa en los primeros 60 words

### Señales de autoridad externa para AI
- Reddit: 2–3 respuestas en r/emprendedores y r/peluqueria (correlación AI alta)
- YouTube: 1 vídeo demo del flujo WhatsApp (correlación AI 0.737 — mayor señal disponible)
- LinkedIn: Company Page + artículo del fundador

---

## 8. KPIs y métricas de seguimiento

### Dashboard mensual

| Métrica | Baseline (Abr 2026) | Mes 3 | Mes 6 | Mes 12 |
|---|---|---|---|---|
| SEO Health Score | 46/100 | 65/100 | 75/100 | 85–90/100 |
| Tráfico orgánico/mes | ~0 (dominio nuevo) | 50+ | 200+ | 800+ |
| Keywords posicionadas top 10 | 0 | 3–5 | 10–15 | 30+ |
| Reseñas Google | 0 | 3 | 8 | 20+ |
| GBP: vistas de perfil/mes | 0 | 50+ | 200+ | 500+ |
| Demos solicitadas vía orgánico | 0 | 2–3 | 8–10 | 20–30 |
| Páginas indexadas | 1 | 5 | 12 | 20+ |
| Backlinks | 0 | 3–5 | 10+ | 25+ |
| GEO citations (AI search) | 0 | 1–2 | 5+ | 15+ |

### Herramientas de medición (gratuitas)
- Google Search Console — impresiones, clicks, posiciones, indexación
- Google Analytics 4 — tráfico, conversiones, fuentes
- Google Business Profile Insights — llamadas, vistas, rutas
- Ahrefs Free / Semrush Free — posiciones de keywords
- Rich Results Test — validación de schema tras cada deploy

---

## 9. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Dominio nuevo — sandbox de Google (3–6m sin rankings) | Alta | Medio | Crear contenido desde el día 1; links de directorios acelera el sandbox |
| Listicles de terceros dominan las SERPs | Alta | Alto | Outreach para inclusión en artículos existentes (L-12 en ACTION-PLAN) |
| Competidores (AvisoVoz, Triviat) tienen más DA | Alta | Medio | Ganar en niche local (Madrid Oeste específico) vs domain-wide |
| Contenido generado sin datos reales | Media | Medio | Usar datos reales de Escultor Peluquería desde el mes 1 |
| RGPD multa antes de política de privacidad | Media | Alto | Resolver en 48h (C-3 en ACTION-PLAN) |

---

## 10. Dependencias del plan

Antes de ejecutar la estrategia de contenido completa:
- [ ] **Escultor Peluquería**: obtener métricas reales (clientes recuperados/mes, testimonial firmado)
- [ ] **CIF de la empresa**: necesario para Aviso Legal y algunos directorios
- [ ] **Foto del fundador**: para Historia section y GBP
- [ ] **Capturas reales del producto**: conversación WhatsApp real (anonimizada) para mockup
- [ ] **Google Search Console**: activar y verificar floux.es
- [ ] **Google Analytics 4**: instalar antes de publicar contenido

---

*Este documento es la fuente de verdad estratégica. Todos los cambios de prioridad o scope se reflejan aquí primero.*
