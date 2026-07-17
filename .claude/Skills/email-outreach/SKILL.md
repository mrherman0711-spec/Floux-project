---
name: email-outreach
description: "Plan and execute Floux cold email outreach campaigns with Resend. Use when drafting campaign emails, selecting salon leads, running dry-runs, sending test emails, or sending production campaign emails."
allowed-tools:
  - Bash
  - Read
  - Edit
---

# Email Outreach

Use this skill for Floux cold email campaigns through Resend.

## Hard Rules

- Never print, paste, or commit `RESEND_API_KEY`.
- Always run a dry-run before sending a real email.
- Always send a test email to the owner before any prospect receives a campaign.
- Never invent salon facts, owner names, pain points, prices, or platform usage. Use prospect research, Google Sheets, or explicit user input.
- Include a clear human sender identity: Floux, Max, and a reply-to address.
- Use `Idempotency-Key` for real sends to avoid duplicate emails.
- For campaign sends, track status in a Sheet before scaling beyond a test.
- If a recipient asks to stop receiving emails, mark them as opted out and do not email them again.

## Scripts

- `execution/send_resend_email.py` — sends one email through Resend.
- `execution/read_sheet.py` — reads prospect rows from Google Sheets.
- `execution/update_sheet.py` — updates campaign status in Google Sheets.

## Environment

Required:

- `RESEND_API_KEY`

Recommended:

- `RESEND_FROM_EMAIL=Floux <max@floux.es>`
- `RESEND_REPLY_TO=max@floux.es`

## Usage

Dry-run:

```bash
python3 execution/send_resend_email.py \
  --to lead@example.com \
  --subject "Recupera las citas que se pierden cuando no puedes coger el teléfono" \
  --text "Hola, soy Max de Floux..." \
  --dry-run
```

Send one test email:

```bash
python3 execution/send_resend_email.py \
  --to max@floux.es \
  --subject "Test campaña Floux" \
  --html-file .tmp/email_test.html \
  --idempotency-key test-campaign-floux-001
```

## Campaign Workflow

1. Select leads from the Dream 100 or prospect Sheet.
2. Exclude rows without email or with opt-out status.
3. Draft the email copy in Spanish, short and direct.
4. Run `execution/send_resend_email.py --dry-run` for the exact payload.
5. Send one test to `RESEND_REPLY_TO` or the owner's email.
6. After approval, send a tiny production batch first.
7. Update the campaign Sheet with send result, Resend email ID, timestamp, and next follow-up date.

## Copy Guidance

- Lead with the salon owner's problem: missed calls become lost appointments.
- Keep the email under 120 words for first touch.
- Make the CTA simple: reply to the email or book a quick WhatsApp/call.
- Avoid sounding like a mass marketing blast.
- Do not use "IA", "bot", or "robot" in client-facing copy unless the user explicitly approves that positioning for cold outreach.

## Failure Modes

- Missing `RESEND_API_KEY`: stop and ask the user to add it to `.env`.
- Resend 4xx: fix payload or domain/sender setup before retrying.
- Resend 429/5xx: wait, retry later with the same idempotency key only if the previous send result is unknown.
- Unclear prospect data: do not personalize that field; use a generic sentence instead.
