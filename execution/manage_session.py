#!/usr/bin/env python3
"""
Load, save, create, expire, or check-duplicate for WhatsApp conversation sessions.
Storage: Google Sheets "sessions" tab, keyed by phone number.

Usage:
  python3 manage_session.py --action load --phone "+34612345678"
  python3 manage_session.py --action create --phone "+34612345678" --call-sid "CAxx" --salon-id "salon_001"
  python3 manage_session.py --action save --phone "+34612345678" --session-json '{"status":"active",...}'
  python3 manage_session.py --action check-duplicate --call-sid "CAxx"
  python3 manage_session.py --action expire --phone "+34612345678"
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SESSIONS_SHEET_URL = os.getenv("SESSIONS_SHEET_URL")
SESSION_TIMEOUT_MINUTES = 10


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        try:
            with open("token.json", "r") as f:
                creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}", file=sys.stderr)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())

    return creds


def get_sessions_worksheet():
    creds = get_credentials()
    client = gspread.authorize(creds)
    sheet_url = SESSIONS_SHEET_URL
    if not sheet_url:
        print("Error: SESSIONS_SHEET_URL not set in .env", file=sys.stderr)
        sys.exit(1)
    sheet_id = sheet_url.split("/d/")[1].split("/")[0] if "/d/" in sheet_url else sheet_url
    spreadsheet = client.open_by_key(sheet_id)
    try:
        return spreadsheet.worksheet("sessions")
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title="sessions", rows=1000, cols=10)
        ws.append_row(["phone", "call_sid", "salon_id", "status", "created_at", "updated_at", "session_json"])
        return ws


def load_session(phone: str) -> dict:
    ws = get_sessions_worksheet()
    records = ws.get_all_records()
    now = datetime.now(timezone.utc)

    for i, row in enumerate(records):
        if row.get("phone") == phone:
            # Check session timeout
            updated_at_str = row.get("updated_at", "")
            if updated_at_str:
                try:
                    updated_at = datetime.fromisoformat(updated_at_str)
                    if updated_at.tzinfo is None:
                        updated_at = updated_at.replace(tzinfo=timezone.utc)
                    elapsed = (now - updated_at).total_seconds() / 60
                    if elapsed > SESSION_TIMEOUT_MINUTES and row.get("status") == "active":
                        # Mark as expired
                        row_num = i + 2  # +1 for header, +1 for 1-indexing
                        ws.update_cell(row_num, 4, "expired")
                        return {"found": False, "reason": "expired"}
                except Exception:
                    pass

            session_json_str = row.get("session_json", "{}")
            try:
                session = json.loads(session_json_str) if session_json_str else {}
            except Exception:
                session = {}

            session["phone"] = row.get("phone")
            session["call_sid"] = row.get("call_sid")
            session["salon_id"] = row.get("salon_id")
            session["status"] = row.get("status")
            session["created_at"] = row.get("created_at")
            session["updated_at"] = row.get("updated_at")
            return {"found": True, "session": session}

    return {"found": False, "reason": "not_found"}


def create_session(phone: str, call_sid: str, salon_id: str) -> dict:
    ws = get_sessions_worksheet()
    now = datetime.now(timezone.utc).isoformat()
    session = {
        "phone": phone,
        "call_sid": call_sid,
        "salon_id": salon_id,
        "status": "active",
        "conversation": [],
        "booking_data": {
            "service": "",
            "datetime": "",
            "client_name": "",
            "staff_preference": "",
            "staff_assigned": ""
        }
    }
    ws.append_row([
        phone,
        call_sid,
        salon_id,
        "active",
        now,
        now,
        json.dumps(session)
    ])
    return {"created": True, "session": session}


def save_session(phone: str, session_data: dict) -> dict:
    ws = get_sessions_worksheet()
    records = ws.get_all_records()
    now = datetime.now(timezone.utc).isoformat()

    for i, row in enumerate(records):
        if row.get("phone") == phone:
            row_num = i + 2
            session_data["updated_at"] = now
            ws.update_cell(row_num, 4, session_data.get("status", "active"))
            ws.update_cell(row_num, 6, now)
            ws.update_cell(row_num, 7, json.dumps(session_data))
            return {"saved": True}

    # Session not found — create it
    ws.append_row([
        phone,
        session_data.get("call_sid", ""),
        session_data.get("salon_id", ""),
        session_data.get("status", "active"),
        now,
        now,
        json.dumps(session_data)
    ])
    return {"saved": True, "created": True}


def check_duplicate(call_sid: str) -> dict:
    ws = get_sessions_worksheet()
    records = ws.get_all_records()
    for row in records:
        if row.get("call_sid") == call_sid:
            return {"duplicate": True}
    return {"duplicate": False}


def expire_session(phone: str) -> dict:
    ws = get_sessions_worksheet()
    records = ws.get_all_records()
    for i, row in enumerate(records):
        if row.get("phone") == phone:
            row_num = i + 2
            ws.update_cell(row_num, 4, "expired")
            return {"expired": True}
    return {"expired": False, "reason": "not_found"}


def main():
    parser = argparse.ArgumentParser(description="Manage WhatsApp conversation sessions")
    parser.add_argument("--action", required=True,
                        choices=["load", "create", "save", "check-duplicate", "expire"],
                        help="Action to perform")
    parser.add_argument("--phone", help="Phone number (E.164)")
    parser.add_argument("--call-sid", dest="call_sid", help="Twilio CallSid")
    parser.add_argument("--salon-id", dest="salon_id", help="Salon ID")
    parser.add_argument("--session-json", dest="session_json", help="Session JSON to save")
    args = parser.parse_args()

    if args.action == "load":
        if not args.phone:
            print(json.dumps({"error": "--phone required for load"}))
            return 1
        result = load_session(args.phone)

    elif args.action == "create":
        if not args.phone or not args.call_sid or not args.salon_id:
            print(json.dumps({"error": "--phone, --call-sid, --salon-id required for create"}))
            return 1
        result = create_session(args.phone, args.call_sid, args.salon_id)

    elif args.action == "save":
        if not args.phone or not args.session_json:
            print(json.dumps({"error": "--phone and --session-json required for save"}))
            return 1
        try:
            session_data = json.loads(args.session_json)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid session JSON: {e}"}))
            return 1
        result = save_session(args.phone, session_data)

    elif args.action == "check-duplicate":
        if not args.call_sid:
            print(json.dumps({"error": "--call-sid required for check-duplicate"}))
            return 1
        result = check_duplicate(args.call_sid)

    elif args.action == "expire":
        if not args.phone:
            print(json.dumps({"error": "--phone required for expire"}))
            return 1
        result = expire_session(args.phone)

    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
