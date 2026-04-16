"""
Scheduled tasks — reminders, review requests, win-back, daily digest.
Runs alongside the webhook server using APScheduler.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.config import TIMEZONE, get_all_salons, load_salon_config
from app import database as db
from app import whatsapp

log = logging.getLogger("floux.scheduler")
TZ = ZoneInfo(TIMEZONE)


# ── Appointment Reminders ────────────────────────────────────

async def send_reminders():
    """Send 24h and 1h appointment reminders. Runs every 15 minutes."""
    now = datetime.now(TZ)

    for salon in get_all_salons():
        salon_id = salon["salon_id"]

        # 24h reminders
        upcoming_24h = db.get_upcoming_appointments(salon_id, hours_ahead=25)
        for apt in upcoming_24h:
            if apt["reminder_24h_sent"]:
                continue

            apt_time = datetime.fromisoformat(apt["datetime_start"])
            if not apt_time.tzinfo:
                apt_time = apt_time.replace(tzinfo=TZ)

            hours_until = (apt_time - now).total_seconds() / 3600
            if 23 <= hours_until <= 25:
                day_names_es = {
                    0: "lunes", 1: "martes", 2: "miércoles",
                    3: "jueves", 4: "viernes", 5: "sábado", 6: "domingo",
                }
                day = day_names_es.get(apt_time.weekday(), "")
                time_str = apt_time.strftime("%H:%M")
                name = apt["client_name"] or "cliente"

                msg = (
                    f"Hola {name}! Te recordamos tu cita mañana {day} a las {time_str} "
                    f"en {salon['salon_name']}.\n\n"
                    f"Servicio: {apt['service']}\n"
                    f"Con: {apt['staff']}\n\n"
                    f"Si necesitas cancelar o cambiar, avísanos con al menos 4 horas de antelación."
                )

                # Skip if client phone == owner phone (test bookings)
                if apt["phone"] == salon.get("owner_phone", ""):
                    log.info(f"Skipping 24h reminder — client phone is owner phone ({apt['phone']})")
                    db.mark_reminder_sent(apt["id"], "24h")
                    continue

                await whatsapp.send_text(apt["phone"], msg)
                db.mark_reminder_sent(apt["id"], "24h")
                db.log_message(apt["phone"], salon_id, "outbound", msg)
                log.info(f"24h reminder sent to {apt['phone']}")

        # 1h reminders
        upcoming_1h = db.get_upcoming_appointments(salon_id, hours_ahead=2)
        for apt in upcoming_1h:
            if apt["reminder_1h_sent"]:
                continue

            apt_time = datetime.fromisoformat(apt["datetime_start"])
            if not apt_time.tzinfo:
                apt_time = apt_time.replace(tzinfo=TZ)

            hours_until = (apt_time - now).total_seconds() / 3600
            if 0.75 <= hours_until <= 1.25:
                time_str = apt_time.strftime("%H:%M")
                name = apt["client_name"] or ""
                greeting = f"Hola {name}! " if name else "Hola! "

                msg = f"{greeting}Tu cita es en 1 hora, a las {time_str}. Te esperamos!"

                # Skip if client phone == owner phone (test bookings)
                if apt["phone"] == salon.get("owner_phone", ""):
                    log.info(f"Skipping 1h reminder — client phone is owner phone ({apt['phone']})")
                    db.mark_reminder_sent(apt["id"], "1h")
                    continue

                await whatsapp.send_text(apt["phone"], msg)
                db.mark_reminder_sent(apt["id"], "1h")
                db.log_message(apt["phone"], salon_id, "outbound", msg)
                log.info(f"1h reminder sent to {apt['phone']}")


# ── Post-Visit Review Requests ───────────────────────────────

async def send_review_requests():
    """Ask for reviews 2 hours after appointment ended. Runs every 30 minutes."""
    for salon in get_all_salons():
        salon_id = salon["salon_id"]
        appointments = db.get_past_appointments_needing_review(salon_id)

        for apt in appointments:
            name = apt["client_name"] or ""
            greeting = f"Hola {name}! " if name else "Hola! "

            msg = (
                f"{greeting}Esperamos que te haya gustado tu visita a {salon['salon_name']} hoy.\n\n"
                f"Tu opinión nos ayuda mucho. Si tienes un momento, nos encantaría que nos dejaras una reseña:\n"
                f"[Enlace a Google Reviews]\n\n"
                f"Gracias!"
            )

            # TODO: Replace [Enlace a Google Reviews] with actual Google review link from salon config

            # Skip if client phone == owner phone (test bookings)
            if apt["phone"] == salon.get("owner_phone", ""):
                log.info(f"Skipping review request — client phone is owner phone ({apt['phone']})")
                db.mark_review_sent(apt["id"])
                continue

            await whatsapp.send_text(apt["phone"], msg)
            db.mark_review_sent(apt["id"])
            db.log_message(apt["phone"], salon_id, "outbound", msg)
            log.info(f"Review request sent to {apt['phone']}")


# ── Win-Back (Inactive Clients) ──────────────────────────────

async def send_winback_messages():
    """Re-engage clients who haven't visited in 30+ days. Runs daily at 11:00."""
    for salon in get_all_salons():
        salon_id = salon["salon_id"]
        inactive = db.get_inactive_clients(salon_id, days=30)

        for client in inactive[:5]:  # Max 5 per day per salon to avoid spam
            name = client["name"] or ""
            greeting = f"Hola {name}! " if name else "Hola! "

            msg = (
                f"{greeting}Hace tiempo que no te vemos por {salon['salon_name']}.\n\n"
                f"Te reservamos tu cita? Dime qué día te viene bien y lo organizamos."
            )

            await whatsapp.send_text(client["phone"], msg)
            db.log_message(client["phone"], salon_id, "outbound", msg)
            log.info(f"Win-back sent to {client['phone']}")


# ── Owner Daily Digest ───────────────────────────────────────

async def send_daily_digest():
    """Send the owner a summary of tomorrow's appointments + today's stats. Runs at 21:00."""
    now = datetime.now(TZ)
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    for salon in get_all_salons():
        salon_id = salon["salon_id"]
        owner_phone = salon.get("owner_phone", "")
        if not owner_phone:
            continue
        if not salon.get("scheduler_enabled", True):
            log.info(f"Scheduler disabled for {salon_id} — skipping daily digest")
            continue

        # Today's stats
        stats = db.get_daily_stats(salon_id, today)

        # Tomorrow's appointments
        tomorrow_apts = db.get_appointments_for_day(salon_id, tomorrow)

        # Build message
        day_names_es = {
            0: "lunes", 1: "martes", 2: "miércoles",
            3: "jueves", 4: "viernes", 5: "sábado", 6: "domingo",
        }
        tomorrow_dt = now + timedelta(days=1)
        tomorrow_day = day_names_es.get(tomorrow_dt.weekday(), "")

        msg = f"RESUMEN DEL DÍA — {salon['salon_name']}\n\n"

        # Today's stats
        msg += f"HOY:\n"
        msg += f"  Citas: {stats['appointments']}\n"
        msg += f"  Facturado: {stats['revenue']}€\n"
        if stats["no_shows"] > 0:
            msg += f"  No-shows: {stats['no_shows']}\n"
        if stats["new_clients"] > 0:
            msg += f"  Clientes nuevos: {stats['new_clients']}\n"
        msg += f"  Mensajes WhatsApp: {stats['messages']}\n\n"

        # Tomorrow's agenda
        if tomorrow_apts:
            msg += f"MAÑANA ({tomorrow_day} {tomorrow_dt.day}/{tomorrow_dt.month}):\n"
            for apt in tomorrow_apts:
                apt_time = datetime.fromisoformat(apt["datetime_start"])
                msg += f"  {apt_time.strftime('%H:%M')} — {apt['service']} ({apt['client_name'] or 'Sin nombre'}) con {apt['staff']}\n"
            msg += f"\n  Total: {len(tomorrow_apts)} citas"
        else:
            msg += f"MAÑANA ({tomorrow_day}): Sin citas programadas"

        await whatsapp.send_text(owner_phone, msg)
        log.info(f"Daily digest sent to owner {owner_phone}")


# ── Morning Briefing ─────────────────────────────────────────

async def send_morning_briefing():
    """Send the owner today's agenda at 8:30. Runs daily at 8:30."""
    now = datetime.now(TZ)
    today = now.strftime("%Y-%m-%d")

    for salon in get_all_salons():
        salon_id = salon["salon_id"]
        owner_phone = salon.get("owner_phone", "")
        if not owner_phone:
            continue
        if not salon.get("scheduler_enabled", True):
            log.info(f"Scheduler disabled for {salon_id} — skipping morning briefing")
            continue

        today_apts = db.get_appointments_for_day(salon_id, today)

        if not today_apts:
            msg = f"Buenos días! Hoy no tienes citas programadas en {salon['salon_name']}."
        else:
            msg = f"Buenos días! Tu agenda de hoy en {salon['salon_name']}:\n\n"
            for apt in today_apts:
                apt_time = datetime.fromisoformat(apt["datetime_start"])
                msg += f"  {apt_time.strftime('%H:%M')} — {apt['service']} ({apt['client_name'] or 'Cliente'}) con {apt['staff']}\n"
            msg += f"\nTotal: {len(today_apts)} citas. Buen día!"

        await whatsapp.send_text(owner_phone, msg)
        log.info(f"Morning briefing sent to owner {owner_phone}")


# ── Scheduler setup ──────────────────────────────────────────

def setup_scheduler():
    """Configure APScheduler with all recurring tasks."""
    from apscheduler.schedulers.asyncio import AsyncIOScheduler

    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    # Reminders: every 15 minutes
    scheduler.add_job(send_reminders, "interval", minutes=15, id="reminders")

    # Review requests: every 30 minutes
    scheduler.add_job(send_review_requests, "interval", minutes=30, id="reviews")

    # Win-back: daily at 11:00
    scheduler.add_job(send_winback_messages, "cron", hour=11, minute=0, id="winback")

    # Owner daily digest: 21:00
    scheduler.add_job(send_daily_digest, "cron", hour=21, minute=0, id="daily_digest")

    # Morning briefing: 8:30
    scheduler.add_job(send_morning_briefing, "cron", hour=8, minute=30, id="morning_briefing")

    scheduler.start()
    log.info("Scheduler started with 5 recurring tasks")
    return scheduler
