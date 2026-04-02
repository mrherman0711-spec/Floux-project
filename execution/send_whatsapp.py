#!/usr/bin/env python3
"""
Send a WhatsApp message via Twilio API.
Usage: python3 send_whatsapp.py --to "+34612345678" --from-number "+34911234567" --message "Hola!"
Output: {"sid": "SMxxx", "status": "queued"}
"""

import argparse
import json
import os
import sys

from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()


def send_whatsapp(to: str, message: str, from_number: str = None) -> dict:
    """
    Send a WhatsApp message via Twilio.

    Args:
        to: Recipient phone number (E.164 or whatsapp: prefixed)
        message: Message text to send
        from_number: Sender Twilio number (E.164). Defaults to TWILIO_WHATSAPP_FROM env var.

    Returns:
        dict with 'sid', 'status', and optionally 'error'
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        return {"sid": None, "status": "error", "error": "TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not set"}

    # Resolve from number
    sender = from_number or os.getenv("TWILIO_WHATSAPP_FROM")
    if not sender:
        return {"sid": None, "status": "error", "error": "No from number provided and TWILIO_WHATSAPP_FROM not set"}

    # Ensure whatsapp: prefix on both numbers
    def ensure_whatsapp_prefix(number: str) -> str:
        number = number.strip()
        if not number.lower().startswith("whatsapp:"):
            return f"whatsapp:{number}"
        return number

    to_whatsapp = ensure_whatsapp_prefix(to)
    from_whatsapp = ensure_whatsapp_prefix(sender)

    try:
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=message,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        return {"sid": msg.sid, "status": msg.status}

    except TwilioRestException as e:
        return {"sid": None, "status": "error", "error": str(e), "code": e.code}
    except Exception as e:
        return {"sid": None, "status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Send WhatsApp message via Twilio")
    parser.add_argument("--to", required=True, help="Recipient phone (E.164 or whatsapp: prefixed)")
    parser.add_argument("--message", required=True, help="Message text to send")
    parser.add_argument("--from-number", dest="from_number", help="Sender Twilio number (overrides TWILIO_WHATSAPP_FROM)")
    args = parser.parse_args()

    result = send_whatsapp(args.to, args.message, args.from_number)
    print(json.dumps(result))
    return 0 if result["status"] not in ("error", "failed") else 1


if __name__ == "__main__":
    sys.exit(main())
