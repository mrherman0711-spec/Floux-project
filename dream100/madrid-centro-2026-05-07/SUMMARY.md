# Madrid Centro Cold-Call Run — SUMMARY

**Run ID:** madrid-centro-2026-05-07
**Fecha:** 2026-05-07 (para llamadas mañana 2026-05-08)
**Status:** PARCIAL — 2 de 6 barrios completados

---

## Lo que SÍ está listo (24 prospectos)

| Barrio | Total | T1 | T2 | T3 | Latinos confirmados |
|---|---|---|---|---|---|
| **Chamberí** | 12 | 4 | 5 | 3 | 2-3 (Div@ 🇨🇺, Barbería VIP, Studio 6 posible) |
| **Lavapiés** | 12 | 4 | 5 | 3 | 0 confirmados (varios "no_verificado") |
| **TOTAL** | **24** | **8** | **10** | **6** | **3+** |

**Top picks para llamar primero (latinos + T1):**
1. **Div@ Peluquería** (Chamberí, score 9, dueña cubana 🇨🇺) — `+34699883196`
2. **Barbería VIP Chamberí** (score 8, Andrés Felipe latino) — `+34659015394`
3. **La Guarida Barbería** (Lavapiés, score 9, sin booking activo) — `+34665173820`
4. **Studio 6 Hairdressing** (Chamberí, score 8, 461 reseñas 5.0) — `+34691316396`

---

## Lo que NO se completó

4 prospectores fueron marcados como "completed" por el sistema pero NO escribieron archivo (probable límite de tokens justo antes del Write):

- **Malasaña / Universidad** — pendiente
- **Chueca / Justicia** — pendiente
- **La Latina** — pendiente
- **Salamanca / Goya** — pendiente

**Recomendación:** relanzar mañana cuando se resetee la cuota a las 4:10am Madrid. Estos barrios añadirían ~48 prospectos más para llegar a los 60 originales.

---

## Patrón de Madrid centro (insights del run)

1. **Saturación de Fresha en Lavapiés:** ~25% de prospects activos. No supera umbral de 50% pero la zona ya está parcialmente cubierta.
2. **Triple plataforma común** (Booksy + Fresha + Treatwell) en barberías nuevas — Vikingos, Play Barbershop, Zhervo. Hook necesita ser específico (llamadas que caen entre canales).
3. **Modelo familiar madre-hijo** detectado en Chamberí (Charo Conector). Crítico hablar con el OPERADOR de IG (joven 25-35), NO con el dueño legal (50+).
4. **Pausa de mediodía 14-16h** universal en Madrid centro = ventana estructural de llamadas perdidas. Hook fuerte para todos.
5. **"Sin web" + "sin IG propio"** = señal más fuerte de ICP. Indica que el teléfono es canal real, no decorativo.

---

## Estructura del CSV (`madrid_centro_callsheet.csv`)

Columnas:
- `orden_llamada` — ya ordenado: latinos primero, luego T1, T2, T3
- `barrio` — para filtrar por zona
- `tier` / `score` — para priorizar visualmente
- `latino` — SI / no_verificado / no
- `negocio` / `rating` / `telefono` / `dueno`
- `direccion` — para el "si dice sí, paso por allí"
- `tiene` — qué plataformas usa (define la objeción que va a poner)
- `pain` — debilidades específicas con dato
- `sales_script` — 5 bullets adaptados (apertura → pain → oferta → objeción esperada → cierre)
- `gmaps_search` / `instagram` — para verificación rápida pre-llamada
- `notas_llamada` / `resultado` — vacíos, Max llena en vivo

---

## Cómo subir a Google Sheets (30 segundos)

1. Abrir [sheets.google.com](https://sheets.google.com), crear nuevo Sheet
2. `File → Import → Upload` → seleccionar `madrid_centro_callsheet.csv`
3. Replace spreadsheet + Detect automatically
4. `View → Freeze → 1 row` para fijar encabezados

---

## Verificación pre-llamada (recomendado)

Antes de llamar a cada T1:
1. **Abrir Google Maps** con `gmaps_search` → verificar horario actual + reseñas recientes
2. **Abrir IG** si está → confirmar que el negocio sigue activo (último post <2 semanas)
3. **Verificar nombre del dueño** si está como "no verificado" — chequear si responde a reseñas con su nombre

---

## Críticas honestas del run

- **Faltan 4 barrios** — solo tenemos 24 de los 60 prospectos planeados
- **Latino-detection fue pobre en Lavapiés** (todo "no_verificado") — segundo run debería forzar verificación más estricta
- **Algunos teléfonos sin verificar en Google Maps** — Barbería VIP y Barbería al Detalle no tienen rating Google confirmado, podría ser que el negocio cambió o cerró
- **Verificar duplicado Dr. Fourquet 39:** La Guarida + El Barberillo tienen la misma dirección. Confirmar en persona si son el mismo local en distintas plataformas o dos negocios separados antes de llamar a uno de ellos
