# Arquitectura del Sitio — Floux.es
**Versión:** 1.0 | **Fecha:** 2026-04-24  
**Estado actual:** 1 página (SPA) → **Objetivo 12m:** 20+ páginas

---

## Arquitectura objetivo (12 meses)

```
floux.es/
│
├── /                           ← Homepage (SPA principal) — EXISTE
│   ├── #como                   ← Anchor: Cómo funciona
│   ├── #porque                 ← Anchor: Por qué Floux
│   ├── #precios                ← Anchor: Precios
│   ├── #historia               ← Anchor: Fundador
│   ├── #faqs                   ← Anchor: FAQs
│   └── #contacto               ← Anchor: Contacto
│
├── /blog/                      ← Blog hub (nueva — mes 1)
│   ├── /cuanto-pierde-peluqueria-llamadas-sin-respuesta/   ← Post 1 (mayo)
│   ├── /agente-whatsapp-salones-estetica/                  ← Post 2 (mayo)
│   ├── /clientes-no-vuelven-llamar-peluqueria/             ← Post 3 (junio)
│   ├── /automatizar-whatsapp-peluqueria/                   ← Post 5 (agosto)
│   ├── /caso-exito-[nombre-salon]/                         ← Post 6 (sept)
│   ├── /mejores-herramientas-salones-madrid/               ← Post 7 (oct)
│   ├── /preparar-salon-navidad-dias-ocupados/              ← Post 9 (nov)
│   └── /tendencias-automatizacion-salones-2027/            ← Post 10 (ene 27)
│
├── /comparar/                  ← Hub de comparativas (nueva — mes 3)
│   ├── /floux-vs-booksy/                                   ← Post 4 (julio)
│   ├── /floux-vs-fresha/                                   ← Fase 3
│   └── /alternativas-treatwell-madrid/                     ← Post 8 (nov)
│
├── /madrid-oeste/              ← Hub local (nueva — mes 6)
│   ├── /majadahonda/           ← Zona 1 (junio)
│   ├── /pozuelo-de-alarcon/    ← Zona 2 (junio)
│   ├── /las-rozas/             ← Zona 3 (julio)
│   ├── /boadilla-del-monte/    ← Zona 4 (agosto)
│   └── /villaviciosa-de-odon/  ← Zona 5 (septiembre)
│
├── /privacidad/                ← Legal (nueva — semana 1) URGENTE
├── /aviso-legal/               ← Legal (nueva — semana 1) URGENTE
│
└── llms.txt                    ← AI crawler guide (nueva — semana 1)
```

---

## Páginas detalladas

### Homepage `/`
- **Tipo:** SPA landing page
- **Schema:** WebSite + Organization + SoftwareApplication + Person + FAQPage
- **Keywords primarios:** "agente whatsapp salones madrid", "recuperar clientes perdidos peluquería"
- **CTA principal:** Botón WhatsApp + Formulario de contacto
- **Internal links out:** → /blog/ → /majadahonda/ → /pozuelo-de-alarcon/ → /privacidad/ → /aviso-legal/

---

### Blog `/blog/`
- **Tipo:** Hub de contenido + listado de posts
- **Schema:** Blog + ItemList
- **Template por post:** Article + BlogPosting + FAQPage (mínimo 3 preguntas)
- **Autor:** Max Herman (Person schema con `@id` referenciando homepage)
- **Internal links:** Cada post enlaza a homepage, a 1–2 posts relacionados, y a 1 página de zona relevante

**Requisitos de calidad por post:**

| Elemento | Requisito |
|---|---|
| Longitud | 1.200+ palabras (objetivo 1.800–2.500) |
| Estadística atribuida | ≥ 1 por post |
| CTA interno | ≥ 1, natural en el contenido |
| FAQ section | ≥ 3 preguntas, respuestas 120+ palabras |
| Imagen | ≥ 1 imagen real (no stock genérico) |
| Autor | "Max Herman, fundador de Floux" con link |
| Schema | Article + FAQPage mínimo |

---

### Comparativas `/comparar/`
- **Tipo:** Comparison landing pages
- **Schema:** Article + FAQPage + tabla comparativa con structured data
- **Enfoque:** Complementario, no agresivo — "Floux y Booksy sirven para cosas distintas"
- **Internal links:** → Homepage → Post de blog relacionado → Página de zona

**Template de tabla comparativa:**

| Característica | Floux | [Competidor] |
|---|---|---|
| Problema que resuelve | Llamadas perdidas → cita automática | [X] |
| Canal | WhatsApp | [X] |
| Precio | Desde €47/mes fijo | [X] |
| Setup | 48h, sin apps | [X] |
| Permanencia | Sin contrato | [X] |
| Para quién | Salones que pierden clientes por teléfono | [X] |

---

### Páginas de zona `/madrid-oeste/[municipio]/`
- **Tipo:** Service Area landing pages
- **Schema:** LocalBusiness (SAB) + ProfessionalService + FAQPage
- **Longitud:** 700–900 palabras mínimo
- **Test doorway page:** 40%+ contenido único por página

**Elementos obligatorios de contenido único por zona:**

| Elemento | Majadahonda | Pozuelo | Las Rozas | Boadilla | Villaviciosa |
|---|---|---|---|---|---|
| Barrios/zonas específicos | ✓ | ✓ | ✓ | ✓ | ✓ |
| Nº salones en el municipio | ✓ | ✓ | ✓ | ✓ | ✓ |
| Referencia local única | ✓ | ✓ | ✓ | ✓ | ✓ |
| FAQ local (¿funciona en [ciudad]?) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Testimonial local (si disponible) | ✓ | — | — | — | — |

**Schema por página de zona:**
```json
{
  "@type": ["ProfessionalService", "LocalBusiness"],
  "name": "Floux — Agente WhatsApp para Salones en [Ciudad]",
  "serviceArea": {
    "@type": "City",
    "name": "[Ciudad]",
    "containedInPlace": {
      "@type": "AdministrativeArea",
      "name": "Comunidad de Madrid"
    }
  },
  "areaServed": { "@type": "City", "name": "[Ciudad]" },
  "url": "https://floux.es/[slug]/",
  "email": "max@floux.es",
  "telephone": "+34632842510"
}
```

---

### Páginas legales

**`/privacidad/`**
- Contenido mínimo RGPD:
  - Responsable del tratamiento: Max Herman / Floux
  - Datos recogidos: nombre, teléfono, nombre del salón
  - Finalidad: gestión de solicitudes de demo
  - Base legal: consentimiento del interesado
  - Tiempo de conservación: hasta solicitud de cancelación o 3 años
  - Derechos ARCO: acceso, rectificación, cancelación, oposición → max@floux.es
  - Derecho a reclamación ante AEPD

**`/aviso-legal/`**
- Contenido mínimo LSSICE:
  - Nombre del responsable: Max Herman
  - Domicilio: Madrid, España
  - Email: max@floux.es
  - CIF (si disponible)
  - Condiciones de uso

---

## Estrategia de internal linking

### Reglas de enlazado

1. **Homepage → Todo:** La homepage enlaza a /blog/ hub, /madrid-oeste/, /privacidad/, /aviso-legal/ desde el footer
2. **Cada post → 2 posts relacionados** mínimo (via sección "También te puede interesar")
3. **Cada post → 1 página de zona** relevante (si el post menciona Madrid, linkar a la zona más relevante)
4. **Páginas de zona → Homepage** (via CTA "Ver todos los planes") + **→ 2 posts del blog** relevantes
5. **Comparativas → Homepage** (CTA principal) + **→ posts relacionados**
6. **Blog hub → Todos los posts** (lista cronológica o por categoría)
7. **Footer global:** Blog | Comparativas | Majadahonda | Pozuelo | Las Rozas | Boadilla | Villaviciosa | Privacidad | Aviso Legal

### Anchor text guidelines
- Usar variación natural: "agente WhatsApp para salones", "recuperar clientes", "Floux", "cómo funciona"
- Evitar anchor text exacto repetido (dilución de señal)
- Links internos: mínimo 1 link por cada 300 palabras de contenido

---

## Estructura técnica por tipo de página

### Template de `<head>` para páginas internas (blog, zonas, comparativas)

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[Título página] | Floux — Madrid</title>
  <meta name="description" content="[Descripción 145–155 chars]" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="author" content="Max Herman" />
  <link rel="canonical" href="https://floux.es/[ruta]/" />
  <link rel="alternate" hreflang="es" href="https://floux.es/[ruta]/" />
  <link rel="alternate" hreflang="x-default" href="https://floux.es/[ruta]/" />
  
  <!-- Open Graph -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="[Título]" />
  <meta property="og:description" content="[Descripción]" />
  <meta property="og:url" content="https://floux.es/[ruta]/" />
  <meta property="og:image" content="https://floux.es/og-image.png" />
  <meta property="og:locale" content="es_ES" />
  <meta property="og:site_name" content="Floux" />
  
  <!-- Geo (solo páginas de zona) -->
  <meta name="geo.region" content="ES-MD" />
  <meta name="geo.placename" content="[Ciudad]" />
  
  <!-- Schema: ver sección de cada tipo de página -->
  <script type="application/ld+json">{ ... }</script>
</head>
```

---

## Sitemap objetivo (estado final mes 12)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  
  <!-- Core pages -->
  <url><loc>https://floux.es/</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>
  
  <!-- Blog -->
  <url><loc>https://floux.es/blog/</loc><priority>0.8</priority><changefreq>weekly</changefreq></url>
  <url><loc>https://floux.es/blog/cuanto-pierde-peluqueria-llamadas-sin-respuesta/</loc><priority>0.7</priority></url>
  <url><loc>https://floux.es/blog/agente-whatsapp-salones-estetica/</loc><priority>0.7</priority></url>
  <!-- ... resto de posts -->
  
  <!-- Comparativas -->
  <url><loc>https://floux.es/comparar/floux-vs-booksy/</loc><priority>0.7</priority></url>
  <url><loc>https://floux.es/comparar/alternativas-treatwell-madrid/</loc><priority>0.7</priority></url>
  
  <!-- Zonas -->
  <url><loc>https://floux.es/madrid-oeste/</loc><priority>0.8</priority></url>
  <url><loc>https://floux.es/madrid-oeste/majadahonda/</loc><priority>0.7</priority></url>
  <url><loc>https://floux.es/madrid-oeste/pozuelo-de-alarcon/</loc><priority>0.7</priority></url>
  <url><loc>https://floux.es/madrid-oeste/las-rozas/</loc><priority>0.7</priority></url>
  <url><loc>https://floux.es/madrid-oeste/boadilla-del-monte/</loc><priority>0.7</priority></url>
  <url><loc>https://floux.es/madrid-oeste/villaviciosa-de-odon/</loc><priority>0.7</priority></url>
  
  <!-- Legal -->
  <url><loc>https://floux.es/privacidad/</loc><priority>0.3</priority></url>
  <url><loc>https://floux.es/aviso-legal/</loc><priority>0.3</priority></url>
  
</urlset>
```

---

## Notas de implementación en Vercel

Floux usa Vercel para servir un sitio estático (HTML puro). Opciones para el blog y páginas internas:

**Opción A — HTML estático por página (recomendada para el estado actual)**
- Cada post es un archivo `.html` en la estructura de carpetas
- Sin framework, sin build step — consistente con el enfoque actual
- `/blog/primer-post/index.html` → sirve como `/blog/primer-post/`
- Pros: simplicidad, velocidad, zero JS overhead
- Cons: crear cada página manualmente (aceptable con 1–2 posts/mes)

**Opción B — Astro o 11ty (recomendada si el volumen crece > 20 posts)**
- Static site generator con soporte de templates y Markdown
- Genera HTML puro como output (sin JS en cliente)
- Integra perfectamente con Vercel
- Migración desde HTML puro: ~4h de setup

*Recomendación: Empezar con Opción A en Fase 1. Evaluar migración a Astro en mes 6 si hay > 8 posts publicados.*

---

*Este documento define la arquitectura. Los contenidos específicos de cada página están en CONTENT-CALENDAR.md.*
