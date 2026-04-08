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
from datetime import datetime, timedelta, timezone

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

        # Check next 7 days
        now = datetime.now(timezone.utc)
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

        slots = []
        check_date = now.date() + timedelta(days=1)

        for day_offset in range(7):
            day = check_date + timedelta(days=day_offset)
            day_name = day_map[day.weekday()]
            hours = working_hours.get(day_name, "cerrado")

            if hours == "cerrado":
                continue

            open_time_str, close_time_str = hours.split("-")
            open_h, open_m = map(int, open_time_str.split(":"))
            close_h, close_m = map(int, close_time_str.split(":"))

            slot_start = datetime(day.year, day.month, day.day, open_h, open_m, tzinfo=timezone.utc)
            close_dt = datetime(day.year, day.month, day.day, close_h, close_m, tzinfo=timezone.utc)

            while slot_start + timedelta(minutes=service_duration) <= close_dt:
                slot_end = slot_start + timedelta(minutes=service_duration)

                # Check if slot overlaps with busy periods
                is_busy = False
                for busy in busy_periods:
                    busy_start = datetime.fromisoformat(busy["start"].replace("Z", "+00:00"))
                    busy_end = datetime.fromisoformat(busy["end"].replace("Z", "+00:00"))
                    if slot_start < busy_end and slot_end > busy_start:
                        is_busy = True
                        break

                if not is_busy:
                    staff_name = staff_members[0]["name"] if staff_members else "Cualquier profesional"
                    slots.append({
                        "datetime": slot_start.strftime("%Y-%m-%dT%H:%M:%S"),
                        "staff": staff_name,
                        "available": True
                    })

                slot_start += timedelta(minutes=30)  # 30-min granularity

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
