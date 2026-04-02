"""
Phone normalization — reuses logic from execution/normalize_phone.py but as importable function.
"""
from __future__ import annotations

import re


def normalize_phone(phone: str) -> str | None:
    """
    Normalize to E.164 format. Returns None if invalid.

    Handles:
    - whatsapp: prefix
    - Spaces, dashes, parens
    - Spanish numbers (6xx, 7xx, 8xx, 9xx)
    - Already-formatted +34 numbers
    - Meta format without + (e.g. "34611222333")
    """
    if not phone:
        return None

    raw = phone.strip()

    # Strip whatsapp: prefix
    if raw.lower().startswith("whatsapp:"):
        raw = raw[9:]

    # Remove all non-digit and non-plus chars
    cleaned = re.sub(r"[^\d+]", "", raw)

    # Already E.164
    if cleaned.startswith("+"):
        e164 = cleaned
    # Country code without +
    elif cleaned.startswith("34") and len(cleaned) == 11:
        e164 = "+" + cleaned
    # Spanish local (9 digits starting with 6, 7, 8, 9)
    elif re.match(r"^[6789]\d{8}$", cleaned):
        e164 = "+34" + cleaned
    else:
        return None

    # Validate
    if not re.match(r"^\+\d{7,15}$", e164):
        return None

    # Spanish-specific: must be 9 digits after +34
    if e164.startswith("+34"):
        if len(e164[3:]) != 9:
            return None

    return e164
