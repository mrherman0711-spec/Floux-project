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


def _pick_available_staff(eligible: list, slot_iso: str, booked_by_staff: dict) -> str | None:
    """
    Return the first eligible staff member not already booked at slot_iso.
    Rotates through the list to distribute load evenly.
    """
    slot_key = slot_iso[:16]  # "YYYY-MM-DDTHH:MM"
    for name in eligible:
        if slot_key not in booked_by_staff.get(name, []):
            return name
    return None  # all staff busy at this slot


def check_google_calendar(config: dict, service: str, staff_members: list) -> list:
    """
    Fetch availability from Google Calendar API.
    Uses working_hours from salonConfig to determine open slots.
    """
    try:
        from googleapiclient.discovery import build
        import sys as _sys
        _sys.path.insert(0, os.path.dirname(__file__))
        from google_auth import get_google_credentials

        SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
        creds = get_google_credentials(SCOPES)

        if not creds:
            print("Error: No valid Google credentials.", file=sys.stderr)
            return []

        service_obj = build("calendar", "v3", credentials=creds)

        # Get service duration
        service_duration = 60  # default
        for svc in config.get("services", []):
            if svc["name"] == service:
                service_duration = svc.get("duration_min", 60)
                break

        # Check next 7 days (all times in Europe/Madrid)
        TZ = ZoneInfo("Europe/Madrid")
        now = datetime.now(TZ)
        time_min = now.isoformat()
        time_max = (now + timedelta(days=7)).isoformat()

        # Get busy times from calendar
        calendar_id = config.get("google_calendar_id", "primary")
        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": calendar_id}]
        }
        freebusy = service_obj.freebusy().query(body=body).execute()
        busy_periods = freebusy.get("calendars", {}).get(calendar_id, {}).get("busy", [])

        # Generate candidate slots from working hours
        working_hours = config.get("working_hours", {})
        day_map = {
            0: "lunes", 1: "martes", 2: "miercoles",
            3: "jueves", 4: "viernes", 5: "sabado", 6: "domingo"
        }

        # Load booked appointments from local DB to know who is busy per slot
        booked_by_staff = _get_booked_slots_from_db()

        slots = []
        check_date = now.date() + timedelta(days=1)
        eligible_names = [m["name"] for m in staff_members] if staff_members else ["Cualquier profesional"]

        for day_offset in range(7):
            day = check_date + timedelta(days=day_offset)
            day_name = day_map[day.weekday()]
            hours = working_hours.get(day_name, "cerrado")

            if hours == "cerrado":
                continue

            # Support single "09:00-13:00" or double "09:00-13:00,17:00-21:00" franjas
            franjas = hours.split(",")
            for franja in franjas:
                open_time_str, close_time_str = franja.strip().split("-")
                open_h, open_m = map(int, open_time_str.split(":"))
                close_h, close_m = map(int, close_time_str.split(":"))

                slot_start = datetime(day.year, day.month, day.day, open_h, open_m, tzinfo=TZ)
                close_dt = datetime(day.year, day.month, day.day, close_h, close_m, tzinfo=TZ)

                while slot_start + timedelta(minutes=service_duration) <= close_dt:
                    slot_end = slot_start + timedelta(minutes=service_duration)
                    slot_iso = slot_start.strftime("%Y-%m-%dT%H:%M:%S")

                    # Check Google Calendar busy (whole salon)
                    calendar_busy = any(
                        slot_start < datetime.fromisoformat(b["end"].replace("Z", "+00:00"))
                        and slot_end > datetime.fromisoformat(b["start"].replace("Z", "+00:00"))
                        for b in busy_periods
                    )

                    if not calendar_busy:
                        # Find first available staff member for this slot
                        assigned = _pick_available_staff(eligible_names, slot_iso, booked_by_staff)
                        if assigned:
                            slots.append({
                                "datetime": slot_iso,
                                "staff": assigned,
                                "available": True
                            })

                    slot_start += timedelta(minutes=30)

        return slots[:10]  # Return max 10 slots

    except Exception as e:
        print(f"Error checking Google Calendar: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(description="Check appointment availability")
    parser.add_argument("--salon-id", dest="salon_id", required=True, help="Salon ID (matches prompts/{id}.json)")
    parser.add_argument("--service", default="", help="Service name to check (optional)")
    parser.add_argument("--staff", default="", help="Staff preference (optional)")
    args = parser.parse_args()

    config = load_salon_config(args.salon_id)
    platform = config.get("platform", "google_calendar")

    # Determine eligible staff
    eligible_staff = []
    if args.service:
        eligible_staff = get_eligible_staff(config, args.service, args.staff or None)
        if not eligible_staff and args.service:
            print(json.dumps({"slots": [], "error": f"No staff found for service: {args.service}"}))
            return 1

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
