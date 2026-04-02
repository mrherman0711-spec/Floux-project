#!/usr/bin/env python3
"""
Execute an appointment booking on Treatwell, Booksy, or Google Calendar.
Reads salonConfig from prompts/{salon_id}.json to determine platform.

Usage:
  python3 book_appointment.py \
    --salon-id "villaviciosa_001" \
    --slot "2026-04-11T16:30:00" \
    --service "Manicura" \
    --staff "Laura" \
    --client-name "Ana García"

Output (success):
  {"booked": true, "reference": "TW-12345", "platform": "treatwell"}

Output (failure):
  {"booked": false, "error": "Slot no longer available", "platform": "treatwell"}
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


def get_platform_name(config: dict, staff_display_name: str) -> str:
    """Look up staff platform_name from salonConfig (may differ from display name)."""
    for member in config.get("staff", []):
        if member["name"].lower() == staff_display_name.lower():
            return member.get("platform_name", member["name"])
    return staff_display_name


def get_service_duration(config: dict, service_name: str) -> int:
    """Get service duration in minutes from salonConfig."""
    for svc in config.get("services", []):
        if svc["name"] == service_name:
            return svc.get("duration_min", 60)
    return 60


def book_treatwell(config: dict, slot: str, service: str, staff: str, client_name: str) -> dict:
    """
    Book appointment on Treatwell partner dashboard via Chrome DevTools MCP.

    Steps (browser automation):
    1. Navigate to config['platform_url']
    2. Login if session expired
    3. Go to New Booking
    4. Select service from catalog
    5. Select staff member (use platform_name)
    6. Select time slot
    7. Enter client name
    8. Confirm booking
    9. Extract booking reference (format: TW-XXXXXX)

    NOTE: This stub returns a placeholder — real execution uses Chrome DevTools MCP.
    """
    platform_name = get_platform_name(config, staff)
    print(f"INFO: Booking on Treatwell via Chrome DevTools MCP", file=sys.stderr)
    print(f"INFO: Dashboard URL: {config.get('platform_url')}", file=sys.stderr)
    print(f"INFO: Service: {service}, Staff: {platform_name} ({staff}), Slot: {slot}, Client: {client_name}", file=sys.stderr)

    # Real implementation: Claude uses Chrome DevTools MCP to navigate and book.
    # Return format when booked:
    # return {"booked": True, "reference": "TW-XXXXXX", "platform": "treatwell"}
    # Return format when failed:
    # return {"booked": False, "error": "Professional not available", "platform": "treatwell"}

    return {
        "booked": False,
        "error": "Browser automation required — run via Claude with Chrome DevTools MCP",
        "platform": "treatwell",
        "instructions": {
            "platform_url": config.get("platform_url"),
            "service": service,
            "staff_platform_name": platform_name,
            "slot": slot,
            "client_name": client_name
        }
    }


def book_booksy(config: dict, slot: str, service: str, staff: str, client_name: str) -> dict:
    """
    Book appointment on Booksy business dashboard via Chrome DevTools MCP.

    Steps (browser automation):
    1. Navigate to config['platform_url']
    2. Login if session expired
    3. Go to Calendar → New Appointment
    4. Select service
    5. Select employee (use platform_name)
    6. Select time slot
    7. Enter client info
    8. Save appointment
    9. Extract booking reference from appointment details

    NOTE: This stub returns a placeholder — real execution uses Chrome DevTools MCP.
    """
    platform_name = get_platform_name(config, staff)
    print(f"INFO: Booking on Booksy via Chrome DevTools MCP", file=sys.stderr)
    print(f"INFO: Dashboard URL: {config.get('platform_url')}", file=sys.stderr)

    return {
        "booked": False,
        "error": "Browser automation required — run via Claude with Chrome DevTools MCP",
        "platform": "booksy",
        "instructions": {
            "platform_url": config.get("platform_url"),
            "service": service,
            "staff_platform_name": platform_name,
            "slot": slot,
            "client_name": client_name
        }
    }


def book_google_calendar(config: dict, slot: str, service: str, staff: str, client_name: str) -> dict:
    """
    Create a Google Calendar event for the booking.
    Does NOT require browser automation — uses Google Calendar API directly.
    """
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request

        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None

        if os.path.exists("token.json"):
            with open("token.json", "r") as f:
                creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                return {"booked": False, "error": "No valid Google credentials", "platform": "google_calendar"}

        service_api = build("calendar", "v3", credentials=creds)

        # Parse slot datetime
        try:
            start_dt = datetime.fromisoformat(slot)
        except ValueError:
            return {"booked": False, "error": f"Invalid slot format: {slot}", "platform": "google_calendar"}

        duration_min = get_service_duration(config, service)
        end_dt = start_dt + timedelta(minutes=duration_min)

        # Set timezone
        tz = "Europe/Madrid"

        event = {
            "summary": f"{service} — {client_name}",
            "description": f"Reservado por Floux\nServicio: {service}\nCliente: {client_name}\nPersonal: {staff}",
            "start": {"dateTime": start_dt.isoformat(), "timeZone": tz},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": tz},
            "attendees": []
        }

        # Add owner as attendee
        owner_email = config.get("owner_email")
        if owner_email:
            event["attendees"].append({"email": owner_email})

        calendar_id = config.get("google_calendar_id", "primary")
        created_event = service_api.events().insert(calendarId=calendar_id, body=event).execute()

        return {
            "booked": True,
            "reference": created_event["id"],
            "platform": "google_calendar",
            "event_url": created_event.get("htmlLink", "")
        }

    except Exception as e:
        return {"booked": False, "error": str(e), "platform": "google_calendar"}


def main():
    parser = argparse.ArgumentParser(description="Execute appointment booking")
    parser.add_argument("--salon-id", dest="salon_id", required=True, help="Salon ID")
    parser.add_argument("--slot", required=True, help="ISO8601 datetime (e.g. 2026-04-11T16:30:00)")
    parser.add_argument("--service", required=True, help="Service name (must match salonConfig exactly)")
    parser.add_argument("--staff", required=True, help="Staff member name")
    parser.add_argument("--client-name", dest="client_name", required=True, help="Client full name")
    args = parser.parse_args()

    # Validate all fields
    for field, value in [("salon_id", args.salon_id), ("slot", args.slot),
                          ("service", args.service), ("staff", args.staff),
                          ("client_name", args.client_name)]:
        if not value or not value.strip():
            print(json.dumps({"booked": False, "error": f"Missing required field: {field}"}))
            return 1

    config = load_salon_config(args.salon_id)
    platform = config.get("platform", "google_calendar")

    if platform == "treatwell":
        result = book_treatwell(config, args.slot, args.service, args.staff, args.client_name)
    elif platform == "booksy":
        result = book_booksy(config, args.slot, args.service, args.staff, args.client_name)
    else:
        result = book_google_calendar(config, args.slot, args.service, args.staff, args.client_name)

    print(json.dumps(result))
    return 0 if result.get("booked") else 1


if __name__ == "__main__":
    sys.exit(main())
