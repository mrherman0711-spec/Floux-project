---
name: prospect-salons
description: "Find and score potential Floux clients in west Madrid. Use when prospecting new salon leads, running Google Maps searches, generating lead lists, or updating the prospect Google Sheet."
allowed-tools:
  - Bash
  - Read
---

# Prospect Salons

Busca salones en west Madrid, los enriquece con Claude Haiku, les asigna score ICP y los guarda en Google Sheets.

## Scripts

- `execution/prospect_salons.py` — Pipeline completo (GMaps → Claude → Sheets)
- `execution/telegram_bot.py` — Bot de Telegram para disparar el pipeline desde el móvil

## Usage

```bash
# Villaviciosa (default)
python3 execution/prospect_salons.py

# Zona específica
python3 execution/prospect_salons.py --area "Boadilla del Monte" --limit 20

# Todas las zonas
python3 execution/prospect_salons.py --all-zones --limit 10

# Añadir a sheet existente
python3 execution/prospect_salons.py --area "Majadahonda" --sheet-url "https://..."

# Iniciar bot de Telegram (lo deja corriendo)
python3 execution/telegram_bot.py
```

## ICP Scoring (Claude Haiku puntúa 0-100)

| Score | Tier | Acción |
|-------|------|--------|
| 70-100 | 1 | Contactar primero — ideal |
| 45-69  | 2 | Contactar después |
| 0-44   | 3 | Baja prioridad |

Red flags automáticos: Fresha, franquicia, solo 1 persona.

## Columnas en Google Sheets

`lead_id · fecha · nombre · categoria · localidad · direccion · telefono · website · tiene_website · maps_url · valoracion · resenas · horario · plataforma_reservas · num_empleados · manager · email · instagram · icp_score · tier · posible_prospecto · dificultad_venta · razon · red_flags · enfoque_venta · estado · notas`

## Env vars requeridas

- `GOOGLE_MAPS_API_KEY` — buscar salones
- `ANTHROPIC_API_KEY` — enriquecer con Claude Haiku
- `GOOGLE_APPLICATION_CREDENTIALS` + `token.json` — escribir en Sheets
- `USER_EMAIL` — compartir sheet automáticamente
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_ADMIN_CHAT_ID` — bot de Telegram

## Telegram commands (desde móvil)

- `/prospectar` → Villaviciosa
- `/prospectar Boadilla` → zona específica
- `/prospectar all` → todas las zonas
- `/sheet` → link del último Google Sheet generado

## Learnings

- Google Maps Places API requiere 2s de delay entre page_token requests
- Claude Haiku es suficiente para extracción estructurada — 10x más barato que Sonnet
- Deduplicación por `lead_id` (MD5 nombre+dirección) evita duplicados entre runs
- Fresha = red flag absoluto (incluye anti-missed-call nativo)
