# Floux — Checklist de Ejecución (Semana 1 de Contenido)
**Para:** Max
**Fecha:** 2026-04-29
**Lanzamiento público:** Lunes 4 de mayo, 20:00

---

## Resumen ejecutivo

Tienes 25 posts diseñados, todos con copy refinado, prompts de Gemini listos para copy-paste y plan de grabación móvil. Coste total de APIs: **~$3** (22 imágenes + 2 clips B-roll). El resto se graba con tu móvil.

**Lo que ya está hecho:**
- ✅ Brand profile consolidado con tu historia personal Guatemala→Madrid
- ✅ Inspiration board con 9 cuentas virales y 5 mecánicas universales replicables
- ✅ 5 trend reports (IG, TikTok, LinkedIn, YouTube, Facebook)
- ✅ 6 estrategias de paid ads (listas para activar cuando haya budget)
- ✅ 25 posts con copy + prompts + plan de producción

**Lo que tienes que hacer tú:**
1. Sesión Gemini API (~1h)
2. Sesión maratón de grabación móvil (~2-3h)
3. Sesión CapCut edición (~3-4h)
4. Sesión programación (~1h)
5. Lanzar lunes 4 de mayo

---

## PASO 1 — Sesión Gemini API (1 hora)

> Imágenes una a una (restricción confirmada). Los prompts están en `social-content/PRODUCTION-PACKAGE.md`. Aquí tienes el bloque agrupado para que vayas pegando uno tras otro.

### Imágenes (22 prompts) — Gemini Imagen 4 Standard ($0.04 × 22 = $0.88)

| # | Post | Aspect | Prompt en archivo | Output esperado |
|---|------|--------|-------------------|-----------------|
| 1 | IG-3 slide 1 | 1:1 | PRODUCTION-PACKAGE.md → IG-3 → Slide 1 | `social-content/instagram/IG-3/slide-1.png` |
| 2 | IG-3 slide 2 | 1:1 | IG-3 → Slide 2 | `…/slide-2.png` |
| 3 | IG-3 slide 3 | 1:1 | IG-3 → Slide 3 | `…/slide-3.png` |
| 4 | IG-3 slide 4 | 1:1 | IG-3 → Slide 4 | `…/slide-4.png` |
| 5 | IG-3 slide 5 | 1:1 | IG-3 → Slide 5 | `…/slide-5.png` |
| 6 | IG-4 background | 9:16 | IG-4 | `social-content/instagram/IG-4/background.png` |
| 7 | LI-1 image | 1.91:1 | LI-1 | `social-content/linkedin/LI-1/image.png` |
| 8 | LI-2 slide 2 | 1:1 | LI-2 → Slide 2 imagen | `social-content/linkedin/LI-2/slide-2.png` |
| 9 | LI-2 slide 5 | 1:1 | LI-2 → Slide 5 imagen | `…/slide-5.png` |
| 10 | LI-2 slide 8 | 1:1 | LI-2 → Slide 8 imagen | `…/slide-8.png` |
| 11 | FB-2 placeholder | 1:1 | FB-2 | `social-content/facebook/FB-2/image.png` |
| 12 | FB-4 image | 1.91:1 | FB-4 | `social-content/facebook/FB-4/image.png` |

> **Nota sobre las 5 slides de carrusel LI-2 que no llevan prompt explícito (1, 3, 4, 6, 7):** son slides de texto puro sobre fondo charcoal. No requieren imagen generada — se montan directo en Canva/Figma con design-system.md (Cormorant Garamond + Inter, paleta charcoal/cream/gold).

### Vídeos B-roll (2 prompts) — Gemini Veo 3.1 Lite ($0.05/s × ~40s = $2)

| # | Post | Duración | Prompt en archivo | Output esperado |
|---|------|----------|-------------------|-----------------|
| 1 | IG-2 manos peluquera | 12-15s 9:16 | PRODUCTION-PACKAGE.md → IG-2 PROMPT VEO | `social-content/instagram/IG-2/broll.mp4` |
| 2 | TT-4 split-screen | 12-15s 9:16 | TT-4 PROMPT VEO | `social-content/tiktok/TT-4/broll.mp4` |

### Workflow recomendado para esta sesión
1. Abre `social-content/PRODUCTION-PACKAGE.md` en una pestaña
2. Abre Google AI Studio en otra pestaña
3. Para cada uno de los 12 prompts de imagen: copia → pega → ejecuta → descarga → guarda con el nombre indicado en la columna "Output esperado"
4. Lo mismo con los 2 prompts de vídeo
5. Si algún resultado no captura bien el estilo (charcoal/cream/gold + warm lighting + editorial), regenera. Imagen 4 a veces necesita 2-3 intentos para clavar el tono Aesop.

**Tiempo estimado: 60-75 minutos** (incluyendo regeneraciones si hace falta).

---

## PASO 2 — Sesión maratón de grabación móvil (2-3 horas)

> Bloquea una mañana o tarde con buena luz natural cálida. Idealmente entre 17:00-19:30 si grabas en interior con ventana al oeste.

### Setup técnico
- [ ] Móvil sobre trípode (o apoyado en libros con estabilidad)
- [ ] Auriculares con micrófono incorporado (mejor calidad de audio que el micro del móvil)
- [ ] Sitio silencioso, sin reverb (evita baños, cocinas vacías)
- [ ] Luz natural de ventana lateral cálida
- [ ] Vestuario: camisa lino crema o jersey lana gris claro. NO logos.
- [ ] Fondo neutro warm: pared crema, madera, planta. NO pared blanca con cuadros corporativos.

### Tomas a grabar (en este orden)

**Grupo A — Talking heads founder (40 min)**

| # | Post | Duración | Guión en archivo |
|---|------|----------|------------------|
| 1 | IG-5 | 45s | PRODUCTION-PACKAGE.md → IG-5 → Guión |
| 2 | TT-2 | 20s | PRODUCTION-PACKAGE.md → TT-2 → Guión |
| 3 | LI-3 | 60s | PRODUCTION-PACKAGE.md → LI-3 → Guión (60s, expansión del IG-5) |
| 4 | YT-3 | 60s | PRODUCTION-PACKAGE.md → YT-3 → Guión |

> Reglas: una sola toma por pieza. Si te equivocas en mitad, vuelve a empezar desde el inicio. NO cortes en mitad de frase. Necesitamos flow natural. Mira fija a cámara durante toda la toma.

**Grupo B — Stitch TikTok TT-3 (15 min)**

| # | Post | Duración | Cómo |
|---|------|----------|------|
| 5 | TT-3 | 18-22s | Primero busca en TikTok un vídeo viral reciente de "tener salón es agotador" en español. Stitch nativo desde la app. Después graba tu respuesta de 18-22s con móvil. |

**Grupo C — Demo screen recording (20 min)**

| # | Post | Cómo |
|---|------|------|
| 6 | IG-1 / TT-1 / YT-1 | Material base único: móvil con screen recording activado. Llamada al número Floux de Escultor → cuelgas → esperas 30s → llega WhatsApp → conversación de prueba hasta confirmar cita. **Guarda el screen recording bruto** — lo usamos en CapCut para 3 versiones distintas (Reel IG, TikTok, Short YouTube). |

**Grupo D — Day in the life (durante un día normal, no sesión maratón)**

| # | Post | Cómo |
|---|------|------|
| 7 | TT-5 | A lo largo de un día normal, graba 8-12 clips de 3-5s cada uno: pantalla del MacBook con código, plano cenital de tu mano escribiendo, captura WhatsApp Floux funcionando, móvil con Google Maps a Las Rozas, foto de un salón por fuera (sin grabar dentro), tu mano apuntando en cuaderno, plano nocturno del portátil iluminado. **Graba el voiceover por separado** con auriculares en sitio silencioso. |

**Grupo E — Vídeos largos YouTube (1.5h, sesión aparte)**

| # | Post | Duración | Notas |
|---|------|----------|-------|
| 8 | YT-2 | 5 min | Talking head + screen captures. Ver estructura en PRODUCTION-PACKAGE.md → YT-2 |
| 9 | YT-4 | 8 min | Tutorial. Semana 2, no urgente para lanzamiento. |

> Para el lanzamiento de la primera semana (lunes 4 mayo), **YT-2 es prioritario**. YT-4 puede ir en semana 2.

**Tiempo total estimado: 2-3 horas para Grupos A-D + 1.5h para Grupo E (puede ser otro día).**

---

## PASO 3 — Sesión CapCut edición (3-4 horas)

### Plantilla CapCut (configurar una vez, reusar)
- Resolución: 1080×1920 (9:16) por defecto
- Frame rate: 30fps
- Color grading preset: warm tone +15, saturación -10, exposición -5
- Música por defecto: track ambient warm de la biblioteca CapCut (categoría "lo-fi" / "cinematic ambient"). Volumen -25dB cuando hay voz, -12dB cuando solo hay imagen.
- Captions automáticos: Inter Bold blanco con sombra negra suave, safe zone superior 220px y inferior 380px (para no taparlos con UI de IG/TikTok)

### Frame final consistente (crear una vez, reusar en cada post)
1. Fondo charcoal `#1A1714` sólido
2. Logo Floux dorado `#9A7B4F` centrado
3. Tagline pequeño en cream Inter 16pt: "Recuperamos los clientes que pierdes cuando no puedes coger el teléfono"
4. URL `floux.es` en gold pequeño debajo
5. Eyebrow Cormorant SC dorado uppercase: "SIN PERMANENCIA · 97€/MES"
6. Duración: 2 segundos

> Guarda este frame como template `floux_endcard.mp4` y lo añades al final de cada post.

### Orden de edición recomendado

| Día | Sesión | Posts a editar |
|-----|--------|----------------|
| 1 | 90 min | IG-1 + TT-1 + YT-1 (todos del mismo material screen recording) |
| 2 | 60 min | IG-5 + TT-2 + LI-3 + YT-3 (todos talking head) |
| 3 | 60 min | IG-2 + TT-4 (los 2 con b-roll Veo) |
| 4 | 45 min | IG-3 carrusel (5 imágenes con texto overlay en Canva, no CapCut) + IG-4 story |
| 5 | 60 min | LI-2 PDF en Canva/Figma + LI-1 imagen + texto |
| 6 | 90 min | YT-2 vídeo largo de 5 min |
| 7 | 30 min | TT-3 stitch + TT-5 day in the life |

**Tiempo total: ~7-8 horas distribuibles en 4-5 sesiones.**

---

## PASO 4 — Sesión programación (1 hora)

### Antes de programar — checklist técnico

- [ ] Cuenta Instagram convertida a **Business** o **Creator** (sin esto Meta Business Suite no funciona)
- [ ] Página de Facebook conectada a la cuenta de Instagram
- [ ] Cuenta de TikTok creada y verificada (@flouxaim)
- [ ] Canal de YouTube @flouxaim creado
- [ ] Perfil personal LinkedIn de Max actualizado con bio Floux
- [ ] Pixel de Meta + TikTok Pixel + LinkedIn Insight Tag instalados en floux.es (para cuando se active paid)

### Stack de scheduling (todo gratis)

| Plataforma | Herramienta | Posts a programar |
|-----------|-------------|-------------------|
| Instagram + Facebook | **Meta Business Suite** | IG-1, IG-2, IG-3, IG-4, IG-5, FB-1, FB-3, FB-4, FB-5 |
| TikTok | **TikTok Studio app** (programa hasta 7 días) | TT-1, TT-2, TT-3, TT-4, TT-5 |
| YouTube | **YouTube Studio** | YT-1 (Short), YT-2 (vídeo largo), YT-3 (Short) |
| LinkedIn | **Manual** (no hay scheduling gratis nativo) | LI-1 mar 09:00, LI-2 jue 09:00, LI-3 dom 19:00 |

### Calendario maestro semana 1 (lanzamiento 4-mayo)

| Día | Hora | IG | TikTok | LinkedIn | YouTube | FB |
|-----|------|----|----|----|----|----|
| **Lun 4-may** | 20:00 | — | — | — | YT-1 | — |
| **Lun 4-may** | 20:30 | IG-1 | — | — | — | — |
| **Lun 4-may** | 21:00 | — | TT-1 | — | — | FB-1 |
| **Mar 5-may** | 09:00 | — | — | LI-1 | — | — |
| **Mié 6-may** | 12:00 | — | — | — | — | FB-4 |
| **Mié 6-may** | 20:30 | IG-2 | — | — | — | — |
| **Mié 6-may** | 21:00 | — | TT-2 | — | — | — |
| **Jue 7-may** | 09:00 | — | — | LI-2 (PDF) | — | — |
| **Jue 7-may** | 19:00 | — | — | — | YT-2 | — |
| **Jue 7-may** | 21:00 | — | TT-3 | — | — | — |
| **Vie 8-may** | 12:30 | IG-3 | — | — | — | — |
| **Sáb 9-may** | 11:30 | IG-4 (Story) | — | — | — | — |
| **Sáb 9-may** | 12:00 | — | TT-4 | — | — | FB-5 |
| **Sáb 9-may** | 19:00 | — | — | — | YT-3 | — |
| **Dom 10-may** | 19:00 | — | — | LI-3 | — | — |
| **Dom 10-may** | 20:00 | IG-5 | — | — | — | — |
| **Dom 10-may** | 21:00 | — | TT-5 | — | — | FB-3 |

**Total semana 1: 18 posts publicados.**

---

## PASO 5 — Engagement y respuesta primeras 2h por post

> Esta es la regla más infravalorada del game.

Después de cada post:
- [ ] 30 minutos después de publicar, abre el post y responde **TODOS** los comentarios. Aunque sea un emoji.
- [ ] Si aparece una pregunta de salón potencial → responde por DM con el calendly o el WhatsApp directo
- [ ] Anota en un cuaderno qué hook/post genera más engagement → eso informa qué replicar en semana 2

**Configuración de notificaciones recomendada:**
- Activa push notifications en IG, TikTok, LinkedIn, YouTube, FB (móvil)
- Configura email digest para no perder DMs durante el día

---

## Posts que requieren material adicional (Semana 2)

Estos están planificados pero requieren entradas que aún no existen:

| Post | Bloqueante | Cuándo activar |
|------|-----------|----------------|
| LI-4 | Necesita primer cliente real con permiso para citar | Cuando cierres primer cliente pagando |
| LI-5 | Listo, puede ir en semana 1 si quieres más volumen | Cualquier momento |
| YT-4 | Requiere grabar vídeo de 8 min + optimización SEO con skill `seo` | Semana 2 |
| YT-5 | Requiere screen captures comparativos | Semana 2 |
| FB-2 | Necesita primer testimonio real | Cuando cierres primer cliente |

---

## Métricas a trackear semana 1

| Métrica | Objetivo D7 | Cómo medir |
|---------|-------------|------------|
| Reach total IG | 5.000 | Insights nativo |
| Followers IG nuevos | +50 | Insights |
| Reach total TikTok | 10.000 | Analytics nativo |
| Followers TikTok nuevos | +100 | Analytics |
| Engagement rate medio | > 4% | (likes + comments + saves) / impressions |
| DMs entrantes de salones | 1-2 | Contar manual |
| Clicks a floux.es desde redes | 30 | Google Analytics + UTMs |
| Leads cualificados | 0-1 | Conversación con potencial cliente real |

> Si en D7 tienes 0 leads cualificados, NO es señal de fallo. Es semana 1. El target real es semana 4 (D30).

---

## Después de la primera semana

Cuando termines D7 con todos los posts publicados, **avísame**. Voy a:

1. Analizar qué formatos rindieron mejor (cara cámara vs B-roll Veo vs carrusel)
2. Diseñar la semana 2 con doble énfasis en lo que funcionó
3. **Recordarte que es momento de construir el skill `/launch`** que automatice este pipeline para que la semana 3 en adelante salga sola con un solo comando

---

## Archivos generados (todo en disco)

```
floux-project/
├── brand/
│   └── historia-floux.md                    # Tu historia personal Guatemala→Madrid
├── brand-profile.json                        # DNA consolidado de marca
├── social-research/
│   ├── inspiration-board.md                  # 9 cuentas virales + 5 mecánicas universales
│   ├── instagram-trends.md                   # Trends + hooks + horas IG abril 2026
│   ├── tiktok-trends.md                      # Sounds, hashtags, formatos TikTok
│   ├── linkedin-trends.md                    # PDF carousels, perfil personal vs página
│   ├── youtube-trends.md                     # Shorts + long form + SEO keywords
│   └── facebook-trends.md                    # Cross-post strategy + grupos
├── ads/
│   ├── PAID-STRATEGY.md                      # Funnel + budget tiers + roadmap
│   ├── meta-plan.md                          # Pixel + audiencias + creative direction
│   ├── tiktok-plan.md                        # Spark Ads + Smart+
│   ├── linkedin-plan.md                      # Sponsored Content + Lead Gen
│   ├── youtube-plan.md                       # Demand Gen + Shorts + Bumper
│   └── creative-brief.md                     # 5 hooks + do's/don'ts + copy TOFU/MOFU/BOFU
├── social-content/
│   ├── PRODUCTION-PACKAGE.md                 # ★ TODO el detalle de los 25 posts
│   ├── instagram/                            # (vacías, llenar al ejecutar)
│   ├── tiktok/
│   ├── linkedin/
│   ├── youtube/
│   └── facebook/
└── MAX-EXECUTION-CHECKLIST.md                # ★ ESTE archivo
```

**Empieza por:** abrir `social-content/PRODUCTION-PACKAGE.md` y leer de principio a fin (15 min). Después PASO 1 (Gemini API).

---

*— Generado 2026-04-29. Si algo no cuadra, dime y lo ajustamos antes de que empieces a producir.*
