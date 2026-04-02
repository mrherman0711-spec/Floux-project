#!/usr/bin/env python3
"""
Normalize a phone number to E.164 format for Spanish numbers.
Usage: python3 normalize_phone.py --phone "+34 612 345 678"
Output: {"normalized": "+34612345678", "valid": true}
"""

import argparse
import json
import re
import sys


def normalize_phone(phone: str) -> dict:
    """
    Normalize a phone number to E.164 format.
    Handles Spanish numbers (landlines and mobiles).

    Args:
        phone: Raw phone number string (may include spaces, dashes, whatsapp: prefix)

    Returns:
        dict with 'normalized' (E.164 string) and 'valid' (bool)
    """
    if not phone:
        return {"normalized": None, "valid": False, "error": "Empty phone number"}

    # Strip whatsapp: prefix if present
    raw = phone.strip()
    if raw.lower().startswith("whatsapp:"):
        raw = raw[9:]

    # Remove all non-digit and non-plus characters
    cleaned = re.sub(r"[^\d+]", "", raw)

    # Already in E.164 with country code
    if cleaned.startswith("+"):
        e164 = cleaned
    # Has country code without +
    elif cleaned.startswith("34") and len(cleaned) == 11:
        e164 = "+" + cleaned
    # Spanish local number (9 digits starting with 6, 7, 8, or 9)
    elif re.match(r"^[6789]\d{8}$", cleaned):
        e164 = "+34" + cleaned
    # Spanish local number (9 digits starting with 9 — landlines)
    else:
        return {"normalized": None, "valid": False, "error": f"Cannot parse number: {phone}"}

    # Validate final format: + followed by 7-15 digits
    if not re.match(r"^\+\d{7,15}$", e164):
        return {"normalized": None, "valid": False, "error": f"Invalid E.164 format: {e164}"}

    # Additional validation for Spanish numbers
    # Mobile: +346XXXXXXXX or +347XXXXXXXX
    # Landline: +349XXXXXXXX
    # Special: +348XXXXXXXX
    if e164.startswith("+34"):
        local = e164[3:]
        if len(local) != 9:
            return {"normalized": None, "valid": False, "error": f"Spanish number must be 9 digits: {e164}"}

    return {"normalized": e164, "valid": True}


def main():
    parser = argparse.ArgumentParser(description="Normalize phone to E.164 format")
    parser.add_argument("--phone", required=True, help="Phone number to normalize")
    args = parser.parse_args()

    result = normalize_phone(args.phone)
    print(json.dumps(result))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
