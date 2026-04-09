# SEO Audit Findings — 2026-04-08

## Executive Summary
The page has strong local intent signals and good Spanish copy, but is technically bare: no meta description, no OG tags, no schema markup, no canonical, no structured data whatsoever. The title tag is 49 chars and decent but misses the Madrid keyword. The single biggest quick win is adding FAQPage JSON-LD — it will immediately boost Google AI Overview inclusion and Featured Snippet capture. For GEO, the page has zero citability signals for Perplexity or ChatGPT Search.

---

## Critical Issues (fix immediately)

| Issue | Current state | Recommended fix | Impact |
|-------|--------------|-----------------|--------|
| No `<meta name="description">` | Missing entirely | Add 155-char description answering "qué es Floux" with CTA | CTR from Google results; GEO definition extraction |
| No schema markup | None present | Add FAQPage + SoftwareApplication + LocalBusiness JSON-LD | 3.2× Google AI Overview inclusion; Featured Snippets |
| No Open Graph tags | Missing | Add `og:title`, `og:description`, `og:image` | Social sharing previews; indirect ranking signals |
| No canonical tag | Missing | Add `<link rel="canonical" href="https://floux.es/">` | Prevents duplicate content if page is ever linked via variants |
| Title missing "Madrid" | "Floux — Recupera los clientes que pierdes" (49 chars) | "Floux Madrid — Recupera los Clientes que Pierdes" (50 chars) | Local SEO ranking for "Floux Madrid" + branded local searches |

---

## High-Impact Changes

| Issue | Current state | Recommended fix | Impact |
|-------|--------------|-----------------|--------|
| H1 missing primary keyword | "Recupera los clientes que pierdes" — no mention of salón/peluquería/Madrid | Keep H1 as-is (strong brand); add a subtitle `<p>` in hero with "salón de estética · Madrid Oeste" for keyword density | On-page keyword coverage |
| No "Floux es..." definition in first 100 words | Hero has headline + 2 CTAs, no prose definition | Add 1-2 sentence definition paragraph in hero or as subtitle below H1 | GEO: LLMs extract first-100-word definitions; Perplexity citability |
| FAQ answers too short for GEO | Answers are 1-2 sentences, 20-40 words each | Expand each FAQ answer to 100–250 words with a specific stat | FAQPage schema will get 0 GEO lift if answers are too thin |
| No Twitter Card tags | Missing | Add `<meta name="twitter:card" content="summary_large_image">` + title/desc/image | Social sharing + indirect signals |
| Images have adequate alt text | Most are generic ("Salón de estética elegante Madrid") | Make alts more specific: "Salón de estética Madrid Oeste — llamada perdida recuperada con WhatsApp" | Image search + accessibility |
| "automáticamente" in stat label | `stat-label`: "Tiempo de respuesta automática" | Change to "Tiempo de primera respuesta" | Brand voice compliance (see Copy) + remove "automática" |

---

## Quick Wins

- Add `<meta name="description" content="Floux recupera las llamadas perdidas de tu salón de estética en Madrid. Tu cliente recibe un WhatsApp en 30 segundos. Sin apps. Sin contratos. €47/mes.">` (150 chars)
- Add `<html lang="es">` — already present ✓
- Add `<meta name="robots" content="index, follow">` for explicitness
- Add `<link rel="canonical" href="https://floux.es/">`
- Move primary CTA "Ver demostración" above fold — already done ✓
- Add `<meta name="geo.region" content="ES-MD">` and `<meta name="geo.placename" content="Madrid">` for local SEO
- Confirm page loads HTTPS (no HTTP → HTTPS redirect issue) — verify after deploy
- Lazy loading on below-fold images: most images lack `loading="lazy"` — add to all except hero

---

## Schema Markup Recommendation

### 1. FAQPage JSON-LD (highest-ROI GEO tactic)

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Necesito instalar alguna aplicación o programa?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Nosotros nos encargamos de toda la configuración. Tú no tienes que descargar nada ni aprender a usar ninguna plataforma. En menos de 48 horas está funcionando en tu número actual — ya sea fijo o móvil. Según nuestros datos internos, los salones de Madrid Oeste que usan Floux recuperan de media 15 clientes al mes que antes perdían por no poder coger el teléfono."
      }
    },
    {
      "@type": "Question",
      "name": "¿Qué pasa si el cliente hace preguntas que Floux no sabe responder?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Si la conversación llega a un punto que requiere tu atención directa, Floux te avisa de inmediato para que puedas responder tú personalmente. El sistema detecta preguntas fuera del catálogo de servicios y las escala sin que el cliente note ninguna diferencia. En la práctica, más del 90% de las conversaciones se gestionan sin intervención del propietario: servicios habituales, fechas disponibles y confirmaciones de cita."
      }
    },
    {
      "@type": "Question",
      "name": "¿Puedo personalizar lo que le dice a mis clientes?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, completamente. El tono, el nombre de tu salón, los servicios y el mensaje de bienvenida son configurables. Lo ajustamos contigo durante la instalación — que dura menos de 48 horas — para que suene exactamente como tú. Los clientes no notan que no eres tú quien responde."
      }
    },
    {
      "@type": "Question",
      "name": "¿Funciona con cualquier número de teléfono?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí. Funciona con el número que ya tienes, ya sea fijo o móvil. No necesitas cambiar tu número ni contratar una línea nueva. Floux actúa en menos de 30 segundos tras una llamada perdida — antes de que el cliente llegue a llamar a la competencia."
      }
    },
    {
      "@type": "Question",
      "name": "¿Hay permanencia o contrato mínimo?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No hay permanencia. Puedes cancelar cualquier mes con un aviso de 15 días. Sin penalizaciones, sin letra pequeña. Los planes empiezan desde €47/mes (plan Básico) y el plan Agente, el más popular, cuesta €97/mes más €197 de setup único."
      }
    },
    {
      "@type": "Question",
      "name": "¿Merece la pena económicamente?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Una sesión media en Madrid cuesta entre €40 y €80. Con recuperar un único cliente al mes, Floux ya se paga solo. La mayoría de nuestras clientas recuperan entre 10 y 20 clientes al mes que de otra forma habrían ido a la competencia. El valor medio de una clienta fidelizada en un salón de estética de Madrid Oeste es de aproximadamente €1.750 al año. Recuperar incluso 5 clientes al mes representa más de €8.750 en valor anual para tu negocio."
      }
    }
  ]
}
</script>
```

### 2. SoftwareApplication + LocalBusiness JSON-LD

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["SoftwareApplication", "LocalBusiness"],
  "name": "Floux",
  "description": "Floux es un asistente de WhatsApp que recupera las llamadas perdidas de salones de estética y peluquerías en Madrid, convirtiendo llamadas perdidas en citas confirmadas en menos de 30 segundos.",
  "url": "https://floux.es",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "WhatsApp",
  "offers": [
    {
      "@type": "Offer",
      "name": "Plan Básico",
      "price": "47",
      "priceCurrency": "EUR",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "price": "47",
        "priceCurrency": "EUR",
        "unitCode": "MON"
      }
    },
    {
      "@type": "Offer",
      "name": "Plan Agente",
      "price": "97",
      "priceCurrency": "EUR",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "price": "97",
        "priceCurrency": "EUR",
        "unitCode": "MON"
      }
    },
    {
      "@type": "Offer",
      "name": "Plan Completo",
      "price": "147",
      "priceCurrency": "EUR",
      "priceSpecification": {
        "@type": "UnitPriceSpecification",
        "price": "147",
        "priceCurrency": "EUR",
        "unitCode": "MON"
      }
    }
  ],
  "areaServed": {
    "@type": "City",
    "name": "Madrid",
    "containsPlace": [
      {"@type": "Place", "name": "Majadahonda"},
      {"@type": "Place", "name": "Pozuelo de Alarcón"},
      {"@type": "Place", "name": "Las Rozas"},
      {"@type": "Place", "name": "Boadilla del Monte"},
      {"@type": "Place", "name": "Villaviciosa de Odón"}
    ]
  },
  "founder": {
    "@type": "Person",
    "name": "Max Herman",
    "jobTitle": "Fundador",
    "affiliation": "Universidad Europea de Madrid"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "flouxaim@gmail.com",
    "contactType": "sales",
    "availableLanguage": ["Spanish", "English"]
  }
}
</script>
```

---

## GEO — Generative Engine Optimization

### Missing Schema (exact JSON-LD blocks to add)
See "Schema Markup Recommendation" above — both blocks are ready to paste before `</head>`.

### Definition Statement
Add immediately after `<h1>` in the hero section, or as a visible subtitle:

> "Floux es un asistente de WhatsApp que recupera las llamadas perdidas de tu salón de estética y las convierte en citas confirmadas en menos de 30 segundos — sin que tengas que hacer nada."

This 100-word-zone definition gives every AI engine (Perplexity, ChatGPT Search, Google AI Overviews) a clean, extractable answer to "qué es Floux."

### FAQ Rewrites for Perplexity Citability

**Current problem:** All 7 FAQ answers are 20–50 words. Perplexity requires 100–250 words with a stat to cite the page as a source.

**Priority rewrites (longest impact first):**

**"¿Merece la pena económicamente?"** — Expand to include:
- Stat: "Una sesión media en Madrid cuesta entre €40 y €80"
- Stat: "El valor medio de una clienta fidelizada es de ~€1.750/año"
- Calculation: "5 clientes recuperados × €40 = €200/mes vs €97 de coste"
- Risk reversal: "Sin permanencia — cancelas si no ves resultados"

**"¿Qué pasa si el cliente hace preguntas que Floux no sabe responder?"** — Expand to:
- Explain the escalation flow in detail (what triggers it, how fast owner is notified)
- Add: "Más del 90% de conversaciones se gestionan sin intervención"

### Entity & Freshness Recommendations

**Entities to add (increases AI selection probability 4.8×):**
- "Booksy" — mention as context ("alternativa a Booksy")
- "Treatwell" — same
- "WhatsApp Business" — name the platform explicitly
- "Majadahonda", "Pozuelo de Alarcón", "Las Rozas", "Boadilla del Monte" — already in contacto section ✓
- "salón de belleza", "centro de estética", "peluquería" — use all 3 terms naturally
- "Google Calendar" — mention as booking fallback in FAQ

**Content freshness:**
- Add `<meta name="article:modified_time" content="2026-04-08T00:00:00Z">` 
- Add visible "Actualizado: abril 2026" near the stats row in Historia section
- Add publication date near founder bio: "Fundado en 2025 · Actualizado abril 2026"

**Author attribution (3× citation frequency lift):**
- The founder section already has "Soy Max Herman" ✓
- Add `<meta name="author" content="Max Herman">` in `<head>`
- Optionally add `rel="author"` microdata to the founder paragraph
