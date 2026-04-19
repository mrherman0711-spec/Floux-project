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
    Load already-booked slots from the SQLite DB.
    Returns {staff_name: [datetime_start, ...]} so we can check per-person availability.
    Tries multiple paths to find floux.db — works both locally and on Railway.
    """
    booked = {}
    try:
        import sqlite3

        # Try multiple candidate paths: Railway runs from /app, local runs from project root
        candidates = [
            os.path.join(os.path.dirname(__file__), "..", "floux.db"),  # local dev
            "/app/floux.db",                                              # Railway
            os.path.join(os.getcwd(), "floux.db"),                       # fallback cwd
        ]
        db_path = next((p for p in candidates if os.path.exists(p)), None)
        if not db_path:
            print("INFO: floux.db not found — no booked slots loaded", file=sys.stderr)
            return booked

        conn = sqlite3.connect(db_path)
        # Only block future appointments — past ones don't matter for availability
        rows = conn.execute(
            "SELECT staff, datetime_start FROM appointments WHERE status != 'cancelled' AND datetime_start > datetime('now')"
        ).fetchall()
        conn.close()
        for staff_name, dt_start in rows:
            if staff_name not in booked:
                booked[staff_name] = []
            booked[staff_name].append(dt_start[:16])  # "YYYY-MM-DDTHH:MM"
        print(f"INFO: Loaded {sum(len(v) for v in booked.values())} booked slots from DB", file=sys.stderr)
    except Exception as e:
        print(f"Warning: could not load DB bookings: {e}", file=sys.stderr)
    return booked


def _pick_available_staff(eligible: list, slot_iso: str, booked_by_staff: dict):
    """
    Return the least-busy eligible staff member not already booked at slot_iso.
    Uses round-robin by workload count to distribute evenly across the team.
    Always assigns someone — if preferred is busy, falls back to next available.
    """
    slot_key = slot_iso[:16]  # "YYYY-MM-DDTHH:MM"

    # Sort eligible by number of already-booked future slots (ascending = least busy first)
    eligible_sorted = sorted(
        eligible,
        key=lambda name: len(booked_by_staff.get(name, []))
    )

    for name in eligible_sorted:
        if slot_key not in booked_by_staff.get(name, []):
            return name

    # All specific eligible staff busy at this slot — return least busy as fallback
    return eligible_sorted[0] if eligible_sorted else None


def _generate_slots_from_schedule(config: dict, service: str, staff_members: list,
                                   busy_periods: list) -> list:
    """
    Generate 30-min slots from the salon's working_hours config.
    Filters out slots that overlap with busy_periods (from Calendar or DB).
    Always returns slots — busy_periods can be empty if Calendar is unavailable.
    """
    TZ = ZoneInfo("Europe/Madrid")
    now = datetime.now(TZ)

    booking_interval = config.get("booking_interval_min", 30)
    service_duration = booking_interval  # default to interval
    if service:
        for svc in config.get("services", []):
            if svc["name"].lower().strip() == service.lower().strip():
                service_duration = svc.get("duration_min", booking_interval)
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
    check_date = now.date()  # start from today
    # Minimum buffer: never offer a slot starting in less than 30 minutes from now
    earliest_slot = now + timedelta(minutes=30)
    # Max slots per day — ensures we spread across multiple days (better UX)
    MAX_SLOTS_PER_DAY = 3
    open_days_with_slots = 0

    for day_offset in range(21):  # scan up to 3 weeks to find enough open days
        day = check_date + timedelta(days=day_offset)
        day_name = day_map[day.weekday()]
        hours = working_hours.get(day_name, "cerrado")

        if hours == "cerrado":
            continue

        day_slots = []

        for franja in hours.split(","):
            open_time_str, close_time_str = franja.strip().split("-")
            open_h, open_m = map(int, open_time_str.split(":"))
            close_h, close_m = map(int, close_time_str.split(":"))

            slot_start = datetime(day.year, day.month, day.day, open_h, open_m, tzinfo=TZ)
            close_dt = datetime(day.year, day.month, day.day, close_h, close_m, tzinfo=TZ)

            # If entire day is in the past, skip it
            if close_dt <= now:
                continue

            # Advance slot_start to the first booking_interval boundary after earliest_slot
            if slot_start < earliest_slot:
                delta_min = int((earliest_slot - slot_start).total_seconds() / 60)
                rounded = ((delta_min + booking_interval - 1) // booking_interval) * booking_interval
                slot_start = slot_start + timedelta(minutes=rounded)

            while slot_start + timedelta(minutes=service_duration) <= close_dt:
                slot_end = slot_start + timedelta(minutes=service_duration)
                slot_iso = slot_start.strftime("%Y-%m-%dT%H:%M:%S")

                # Double-check slot is in the future (safety net)
                if slot_start <= now:
                    slot_start += timedelta(minutes=booking_interval)
                    continue

                calendar_busy = any(
                    slot_start < datetime.fromisoformat(b["end"].replace("Z", "+00:00"))
                    and slot_end > datetime.fromisoformat(b["start"].replace("Z", "+00:00"))
                    for b in busy_periods
                )

                if not calendar_busy:
                    assigned = _pick_available_staff(eligible_names, slot_iso, booked_by_staff)
                    if assigned:
                        day_slots.append({
                            "datetime": slot_iso,
                            "staff": assigned,
                            "available": True,
                        })

                # Always advance by booking_interval (30 min), not service_duration.
                # This allows back-to-back bookings at clean 30-min boundaries.
                slot_start += timedelta(minutes=booking_interval)

                if len(day_slots) >= MAX_SLOTS_PER_DAY:
                    break  # enough slots for this day

            if len(day_slots) >= MAX_SLOTS_PER_DAY:
                break

        if day_slots:
            slots.extend(day_slots)
            open_days_with_slots += 1

        if len(slots) >= 10 and open_days_with_slots >= 3:
            break  # at least 3 different days covered

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
