#!/usr/bin/env python3
"""
Fetch available appointment slots from Treatwell, Booksy, or Google Calendar.
Reads salonConfig from prompts/{salon_id}.json to determine platform.

Usage:
  python3 check_availability.py --salon-id "villaviciosa_001" --service "Manicura"
  python3 check_availability.py --salon-id "villaviciosa_001" --service "Mechas" --staff "María"

Output:
  {"slots": [{"datetime": "2026-04-11T10:00:00", "staff": "María", "available": true}, ...]}
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


def load_salon_config(salon_id: str) -> dict:
    path = os.path.join(PROMPTS_DIR, f"{salon_id}.json")
    if not os.path.exists(path):
        print(f"Error: salonConfig not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_eligible_staff(config: dict, service: str, staff_preference: str = None) -> list:
    """Return list of staff names who can perform the service."""
    eligible = []
    for member in config.get("staff", []):
        if service in member.get("services", []):
            eligible.append(member)
    if staff_preference:
        preferred = [m for m in eligible if m["name"].lower() == staff_preference.lower()]
        if preferred:
            return preferred
    return eligible


def check_treatwell(config: dict, service: str, staff_members: list) -> list:
    """
    Fetch availability from Treatwell partner dashboard via Chrome DevTools MCP.
    This function is a stub — actual implementation uses browser automation.
    Returns slots in standard format.
    """
    # NOTE: Real implementation uses Chrome DevTools MCP to navigate Treatwell dashboard.
    # The platform_url in salonConfig points to the partner login.
    # Steps: login → calendar view → check available slots for service + staff.
    print("INFO: Treatwell availability check requires Chrome DevTools MCP (browser automation)", file=sys.stderr)
    print(f"INFO: Platform URL: {config.get('platform_url', 'not set')}", file=sys.stderr)

    # Return empty slots — Claude will use browser automation to fill this
    return []


def check_booksy(config: dict, service: str, staff_members: list) -> list:
    """
    Fetch availability from Booksy business dashboard via Chrome DevTools MCP.
    This function is a stub — actual implementation uses browser automation.
    """
    print("INFO: Booksy availability check requires Chrome DevTools MCP (browser automation)", file=sys.stderr)
    print(f"INFO: Platform URL: {config.get('platform_url', 'not set')}", file=sys.stderr)
    return []


def _get_booked_slots_from_db() -> dict:
    """
    Load already-booked slots from the local SQLite DB.
    Returns {staff_name: [datetime_start, ...]} so we can check per-person availability.
    """
    booked = {}
    try:
        import sqlite3
        db_path = os.path.join(os.path.dirname(__file__), "..", "floux.db")
        if not os.path.exists(db_path):
            return booked
        conn = sqlite3.connect(db_path)
        rows = conn.execute(
            "SELECT staff, datetime_start FROM appointments WHERE status != 'cancelled'"
        ).fetchall()
        conn.close()
        for staff_name, dt_start in rows:
            if staff_name not in booked:
                booked[staff_name] = []
            booked[staff_name].append(dt_start[:16])  # "YYYY-MM-DDTHH:MM"
    except Exception as e:
        print(f"Warning: could not load DB bookings: {e}", file=sys.stderr)
    return booked


def _pick_available_staff(eligible: list, slot_iso: str, booked_by_staff: dict):
    """
    Return the first eligible staff member not already booked at slot_iso.
    Always assigns someone — if preferred is busy, falls back to next available.
    """
    slot_key = slot_iso[:16]  # "YYYY-MM-DDTHH:MM"
    for name in eligible:
        if slot_key not in booked_by_staff.get(name, []):
            return name
    # All specific eligible staff busy — return first as fallback (rare edge case)
    return eligible[0]["name"] if eligible and isinstance(eligible[0], dict) else (eligible[0] if eligible else None)


def _generate_slots_from_schedule(config: dict, service: str, staff_members: list,
                                   busy_periods: list) -> list:
    """
    Generate 30-min slots from the salon's working_hours config.
    Filters out slots that overlap with busy_periods (from Calendar or DB).
    Always returns slots — busy_periods can be empty if Calendar is unavailable.
    """
    TZ = ZoneInfo("Europe/Madrid")
    now = datetime.now(TZ)

    service_duration = 30  # default to shortest slot
    if service:
        for svc in config.get("services", []):
            if svc["name"].lower().strip() == service.lower().strip():
                service_duration = svc.get("duration_min", 30)
                break

    working_hours = config.get("working_hours", {})
    day_map = {
        0: "lunes", 1: "martes", 2: "miercoles",
        3: "jueves", 4: "viernes", 5: "sabado", 6: "domingo"
    }

    booked_by_staff = _get_booked_slots_from_db()
    all_staff = config.get("staff", [])
    eligible_names = [m["name"] if isinstance(m, dict) else m for m in staff_members] if staff_members else [m["name"] for m in all_staff]
    if not eligible_names:
        eligible_names = ["Cualquier profesional"]
    print(f"INFO: eligible_names={eligible_names} service_duration={service_duration}", file=sys.stderr)

    slots = []
    check_date = now.date()  # include today if hours remain

    for day_offset in range(8):
        day = check_date + timedelta(days=day_offset)
        day_name = day_map[day.weekday()]
        hours = working_hours.get(day_name, "cerrado")

        if hours == "cerrado":
            continue

        for franja in hours.split(","):
            open_time_str, close_time_str = franja.strip().split("-")
            open_h, open_m = map(int, open_time_str.split(":"))
            close_h, close_m = map(int, close_time_str.split(":"))

            slot_start = datetime(day.year, day.month, day.day, open_h, open_m, tzinfo=TZ)
            close_dt = datetime(day.year, day.month, day.day, close_h, close_m, tzinfo=TZ)

            # Skip past slots for today
            if slot_start <= now:
                # Advance to next 30-min boundary after now
                minutes_ahead = int((now - slot_start).total_seconds() / 60) + 30
                minutes_ahead = (minutes_ahead // 30) * 30
                slot_start = datetime(day.year, day.month, day.day, open_h, open_m, tzinfo=TZ) + timedelta(minutes=minutes_ahead)

            while slot_start + timedelta(minutes=service_duration) <= close_dt:
                slot_end = slot_start + timedelta(minutes=service_duration)
                slot_iso = slot_start.strftime("%Y-%m-%dT%H:%M:%S")

                calendar_busy = any(
                    slot_start < datetime.fromisoformat(b["end"].replace("Z", "+00:00"))
                    and slot_end > datetime.fromisoformat(b["start"].replace("Z", "+00:00"))
                    for b in busy_periods
                )

                if not calendar_busy:
                    assigned = _pick_available_staff(eligible_names, slot_iso, booked_by_staff)
                    if assigned:
                        slots.append({
                            "datetime": slot_iso,
                            "staff": assigned,
                            "available": True,
                        })

                slot_start += timedelta(minutes=30)

    return slots[:10]


def check_google_calendar(config: dict, service: str, staff_members: list) -> list:
    """
    Generate available slots from the salon schedule.
    Uses Google Calendar freebusy to filter already-booked slots.
    Always returns slots — falls back to schedule-only if Calendar is unavailable.
    """
    busy_periods = []

    try:
        from googleapiclient.discovery import build
        import sys as _sys
        _sys.path.insert(0, os.path.dirname(__file__))
        from google_auth import get_google_credentials

        SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
        creds = get_google_credentials(SCOPES)

        if creds:
            TZ = ZoneInfo("Europe/Madrid")
            now = datetime.now(TZ)
            service_obj = build("calendar", "v3", credentials=creds)
            calendar_id = config.get("google_calendar_id", "primary")
            freebusy = service_obj.freebusy().query(body={
                "timeMin": now.isoformat(),
                "timeMax": (now + timedelta(days=7)).isoformat(),
                "items": [{"id": calendar_id}],
            }).execute()
            busy_periods = freebusy.get("calendars", {}).get(calendar_id, {}).get("busy", [])
            print(f"INFO: Calendar OK — {len(busy_periods)} busy periods", file=sys.stderr)
        else:
            print("INFO: No Google credentials — using schedule only", file=sys.stderr)

    except Exception as e:
        print(f"INFO: Calendar query failed ({e}) — using schedule only", file=sys.stderr)

    slots = _generate_slots_from_schedule(config, service, staff_members, busy_periods)
    print(f"INFO: Generated {len(slots)} slots for service='{service}'", file=sys.stderr)
    return slots


def main():
    parser = argparse.ArgumentParser(description="Check appointment availability")
    parser.add_argument("--salon-id", dest="salon_id", required=True, help="Salon ID (matches prompts/{id}.json)")
    parser.add_argument("--service", default="", help="Service name to check (optional)")
    parser.add_argument("--staff", default="", help="Staff preference (optional)")
    args = parser.parse_args()

    config = load_salon_config(args.salon_id)
    platform = config.get("platform", "google_calendar")

    # Determine eligible staff — if no service/preference, use all staff
    if args.service:
        eligible_staff = get_eligible_staff(config, args.service, args.staff or None)
        if not eligible_staff:
            print(json.dumps({"slots": [], "error": f"No staff found for service: {args.service}"}))
            return 1
    else:
        eligible_staff = config.get("staff", [])

    # Fetch slots based on platform
    if platform == "treatwell":
        slots = check_treatwell(config, args.service, eligible_staff)
    elif platform == "booksy":
        slots = check_booksy(config, args.service, eligible_staff)
    else:
        slots = check_google_calendar(config, args.service, eligible_staff)

    print(json.dumps({"slots": slots, "platform": platform, "salon_id": args.salon_id}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
