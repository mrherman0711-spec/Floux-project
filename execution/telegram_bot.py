#!/usr/bin/env python3
"""
Floux Telegram Bot — Asistente personal de Max
Responde a mensajes de texto + comandos específicos.
Usage: python3 execution/telegram_bot.py
"""
from __future__ import annotations
import os, sys, asyncio
from openai import OpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()

TOKEN    = os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "")
oai      = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

ZONE_MAP = {
    "boadilla": "Boadilla del Monte", "majadahonda": "Majadahonda",
    "pozuelo": "Pozuelo de Alarcón", "rozas": "Las Rozas de Madrid",
    "las rozas": "Las Rozas de Madrid", "villaviciosa": "Villaviciosa de Odón",
}
SYSTEM_PROMPT = """Eres el asistente personal de Max, fundador de Floux (agente WhatsApp de reservas para salones de belleza en west Madrid).
Tu trabajo es ayudarle con ventas, prospectos, análisis de mercado y operaciones de Floux.

Capacidades especiales (díselas si las pide):
- Prospectar salones en west Madrid → escribe "prospectar [zona]" o usa /prospectar
- Ver el último Google Sheet de leads → /sheet
- Ver estadísticas → /stats

Tono: directo, práctico, como un buen colaborador. En español siempre.
Contexto: Max tiene la API de Google Maps, OpenAI, WhatsApp de Meta, y credenciales de Google Sheets ya configuradas.
No inventes datos. Si no sabes algo, dilo."""


def is_admin(update: Update) -> bool:
    return not ADMIN_ID or str(update.effective_chat.id) == ADMIN_ID


def parse_zone(text: str) -> tuple[str | None, bool]:
    """Returns (zone_name, all_zones). zone_name=None means --all-zones."""
    t = text.lower()
    if "all" in t or "todas" in t or "todo" in t:
        return None, True
    for key, zone in ZONE_MAP.items():
        if key in t:
            return zone, False
    return "Villaviciosa de Odón", False  # default


async def run_prospector(chat_id: int, zone: str | None, all_zones: bool, app: Application):
    """Run prospect_salons.py as subprocess with live updates to Telegram."""
    script = os.path.join(os.path.dirname(__file__), "prospect_salons.py")
    cmd = [sys.executable, script]
    if all_zones:
        cmd.append("--all-zones")
    elif zone:
        cmd += ["--area", zone]
    cmd += ["--limit", "10"]

    # Append to existing sheet if one exists
    try:
        existing = open(".tmp/last_sheet.txt").read().strip()
        cmd += ["--sheet-url", existing]
    except FileNotFoundError:
        pass

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        leads_found = 0

        # Stream stdout line by line
        async for raw_line in proc.stdout:
            line = raw_line.decode().strip()
            if not line:
                continue

            # Send progress update every time a lead is found
            if "✅" in line and "Nuevos:" not in line:
                leads_found += 1
                # Send update every 3 leads to avoid spam
                if leads_found % 3 == 1:
                    await app.bot.send_message(
                        chat_id=chat_id,
                        text=f"⏳ Procesando... {leads_found} leads encontrados hasta ahora"
                    )

        await proc.wait()

        # Final result
        sheet_link = ""
        try:
            sheet_link = open(".tmp/last_sheet.txt").read().strip()
        except FileNotFoundError:
            pass

        if sheet_link:
            msg = (
                f"✅ *Prospección completada*\n"
                f"📊 {leads_found} leads añadidos al Sheet\n\n"
                f"[Abrir Google Sheet]({sheet_link})"
            )
        else:
            stderr = (await proc.stderr.read()).decode()
            msg = f"⚠️ Terminó pero no se generó sheet.\n```{stderr[-500:]}```"

        await app.bot.send_message(chat_id=chat_id, text=msg,
            parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        await app.bot.send_message(chat_id=chat_id, text=f"❌ Error: {e}")


async def cmd_prospectar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    text = " ".join(ctx.args) if ctx.args else ""
    zone, all_zones = parse_zone(text)
    label = "todas las zonas" if all_zones else (zone or "Villaviciosa de Odón")
    await update.message.reply_text(f"🔍 Buscando en *{label}*... te aviso cuando encuentre leads.", parse_mode="Markdown")
    asyncio.create_task(run_prospector(update.effective_chat.id, zone, all_zones, ctx.application))


async def cmd_sheet(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    try:
        link = open(".tmp/last_sheet.txt").read().strip()
        await update.message.reply_text(f"📊 Último Google Sheet:\n{link}")
    except FileNotFoundError:
        await update.message.reply_text("No hay sheet todavía. Usa /prospectar para generar uno.")


async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    try:
        link = open(".tmp/last_sheet.txt").read().strip()
        await update.message.reply_text(
            f"📈 *Stats Floux*\n\n"
            f"Sheet activo: {link}\n"
            f"Para ver leads por tier, abre el sheet y filtra por columna 'tier'.",
            parse_mode="Markdown"
        )
    except FileNotFoundError:
        await update.message.reply_text("Sin datos aún. Usa /prospectar primero.")


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Handle free-text messages using GPT-4o-mini as assistant."""
    if not is_admin(update): return
    user_msg = update.message.text or ""

    # Detect if user is asking to prospect without using the command
    prospect_keywords = ["prospecta", "busca salones", "busca leads", "buscar salones", "encuentra salones"]
    if any(kw in user_msg.lower() for kw in prospect_keywords):
        zone, all_zones = parse_zone(user_msg)
        label = "todas las zonas" if all_zones else (zone or "Villaviciosa de Odón")
        await update.message.reply_text(f"🔍 Buscando en *{label}*... te aviso cuando encuentre leads.", parse_mode="Markdown")
        asyncio.create_task(run_prospector(update.effective_chat.id, zone, all_zones, ctx.application))
        return

    # Otherwise: AI assistant response
    await ctx.application.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        r = oai.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=500,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
        )
        reply = r.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Error al procesar tu mensaje: {e}")


def main():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN no en .env"); sys.exit(1)

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("prospectar", cmd_prospectar))
    app.add_handler(CommandHandler("sheet", cmd_sheet))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Floux Bot iniciado. Ctrl+C para parar.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
