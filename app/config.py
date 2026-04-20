"""
Central configuration — loads .env and salon configs.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"
TMP_DIR = BASE_DIR / ".tmp"
TMP_DIR.mkdir(exist_ok=True)

# ── Twilio (voice — missed-call detection only) ─────────────
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "floux-verify-2026")

# ── Evolution API (WhatsApp messaging via eSIM real) ─────────
EVOLUTION_BASE_URL = os.getenv("EVOLUTION_BASE_URL", "").rstrip("/")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "floux_salon_1")

# ── OpenAI ──────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"

# ── Google ──────────────────────────────────────────────────
SESSIONS_SHEET_URL = os.getenv("SESSIONS_SHEET_URL", "")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

# ── App settings ────────────────────────────────────────────
TIMEZONE = "Europe/Madrid"
SESSION_TIMEOUT_MINUTES = 30
REMINDER_HOURS_BEFORE = 24
REVIEW_DELAY_HOURS = 2
WINBACK_DAYS = 30


def load_salon_config(salon_id: str) -> dict | None:
    """Load a salon config from prompts/{salon_id}.json."""
    path = PROMPTS_DIR / f"{salon_id}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_salon_by_phone(phone: str) -> dict | None:
    """Find which salon owns a given Twilio number."""
    for config_file in PROMPTS_DIR.glob("*.json"):
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        if config.get("twilio_number") == phone:
            return config
    return None


def get_all_salons() -> list[dict]:
    """Return all salon configs."""
    salons = []
    for config_file in PROMPTS_DIR.glob("*.json"):
        with open(config_file, "r", encoding="utf-8") as f:
            salons.append(json.load(f))
    return salons
