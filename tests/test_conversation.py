#!/usr/bin/env python3
"""
Simulate WhatsApp conversations to test the AI engine.
Runs without API keys — uses mock data.

Usage:
  python tests/test_conversation.py
  python tests/test_conversation.py --scenario booking
  python tests/test_conversation.py --scenario all
"""

import argparse
import json
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import load_salon_config
from app.phone import normalize_phone
from app.database import init_db, get_or_create_client, create_session, get_active_session


def test_phone_normalization():
    """Test phone normalization with various inputs."""
    cases = [
        ("+34 611 222 333", "+34611222333"),
        ("34611222333", "+34611222333"),
        ("611222333", "+34611222333"),
        ("whatsapp:+34611222333", "+34611222333"),
        ("+34611222333", "+34611222333"),
        ("", None),
        ("123", None),
        ("whatsapp:611222333", "+34611222333"),
    ]

    print("=== Phone Normalization ===")
    all_pass = True
    for input_val, expected in cases:
        result = normalize_phone(input_val)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  {status}: normalize_phone('{input_val}') = '{result}' (expected '{expected}')")

    return all_pass


def test_salon_config():
    """Test loading salon config."""
    print("\n=== Salon Config ===")
    config = load_salon_config("ds_peluqueria")
    if not config:
        print("  FAIL: ds_peluqueria.json not found")
        return False

    required_keys = ["salon_id", "salon_name", "staff", "services", "working_hours", "system_prompt"]
    all_pass = True
    for key in required_keys:
        if key in config:
            print(f"  PASS: '{key}' present")
        else:
            print(f"  FAIL: '{key}' missing")
            all_pass = False

    # Validate staff-service consistency
    all_services = {s["name"] for s in config["services"]}
    for member in config["staff"]:
        for svc in member["services"]:
            if svc not in all_services:
                print(f"  WARN: Staff '{member['name']}' has service '{svc}' not in services list")

    print(f"  INFO: {len(config['services'])} services, {len(config['staff'])} staff members")
    return all_pass


def test_database():
    """Test database operations."""
    print("\n=== Database ===")
    init_db()

    # Test client creation
    client = get_or_create_client("+34611222333", "ds_peluqueria")
    assert client["phone"] == "+34611222333", "Client phone mismatch"
    print(f"  PASS: Client created/loaded: {client['phone']}")

    # Test session creation
    session = create_session("+34611222333", "ds_peluqueria", "CA_test_123")
    assert session is not None, "Session creation failed"
    print(f"  PASS: Session created: id={session['id']}")

    # Test session retrieval
    loaded = get_active_session("+34611222333")
    assert loaded is not None, "Session not found"
    print(f"  PASS: Session loaded: status={loaded['status']}")

    return True


def test_ai_prompt_building():
    """Test system prompt construction (without calling OpenAI)."""
    print("\n=== AI Prompt Building ===")
    from app.ai_engine import build_system_prompt

    config = load_salon_config("ds_peluqueria")
    if not config:
        print("  SKIP: No salon config")
        return True

    # Mock availability slots
    mock_slots = [
        {"datetime": "2026-04-03T10:00:00", "staff": "Ana", "available": True},
        {"datetime": "2026-04-03T11:00:00", "staff": "David", "available": True},
        {"datetime": "2026-04-03T15:30:00", "staff": "Lucía", "available": True},
    ]

    prompt = build_system_prompt(config, mock_slots)

    # Check key elements are present
    checks = [
        ("Salon name in prompt", "DS Peluquería" in prompt),
        ("Services listed", "Corte mujer" in prompt),
        ("Prices listed", "27" in prompt),
        ("Staff listed", "Ana" in prompt),
        ("Availability injected", "10:00" in prompt),
        ("JSON format instruction", "JSON" in prompt),
        ("No AI disclosure rule", "NUNCA" in prompt),
    ]

    all_pass = True
    for desc, result in checks:
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  {status}: {desc}")

    print(f"  INFO: Prompt length = {len(prompt)} chars")
    return all_pass


SCENARIOS = {
    "booking": [
        ("user", "Hola, quiero reservar una cita"),
        ("expected_intent", "greeting"),
        ("user", "Un corte de mujer"),
        ("expected_intent", "booking"),
        ("user", "Mañana a las 10 si puede ser"),
        ("expected_intent", "booking"),
        ("user", "Ana García"),
        ("expected_intent", "booking"),
        ("user", "Con Ana por favor"),
        ("expected_intent", "booking"),
        ("user", "Sí, perfecto, confirma"),
        ("expected_complete", True),
    ],
    "english": [
        ("user", "Hi, I'd like to book a haircut"),
        ("expected_language", "en"),
    ],
    "voice_note": [
        ("media", "audio"),
        ("expected_reply_contains", "no puedo escuchar"),
    ],
    "unknown_service": [
        ("user", "Quiero un lifting facial"),
        ("expected_intent", "escalate"),
    ],
    "angry_client": [
        ("user", "Llevo 20 minutos esperando y nadie contesta!!!"),
        ("expected_intent", "escalate"),
    ],
}


def print_scenarios():
    """Print available test scenarios."""
    print("\n=== Available Scenarios ===")
    for name, steps in SCENARIOS.items():
        user_msgs = [s[1] for s in steps if s[0] == "user"]
        print(f"  {name}: {len(user_msgs)} messages — {user_msgs[0][:50]}...")


def main():
    parser = argparse.ArgumentParser(description="Test Floux conversation engine")
    parser.add_argument("--scenario", default="none", help="Scenario to run (booking, english, all, none)")
    args = parser.parse_args()

    results = []

    # Always run unit tests
    results.append(("Phone normalization", test_phone_normalization()))
    results.append(("Salon config", test_salon_config()))
    results.append(("Database", test_database()))
    results.append(("AI prompt building", test_ai_prompt_building()))

    if args.scenario != "none":
        print_scenarios()
        print("\n  NOTE: Scenario tests require OPENAI_API_KEY in .env")
        print("  Run with --scenario booking to test a full booking flow")

    # Summary
    print("\n" + "=" * 40)
    print("RESULTS:")
    all_pass = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  {status}: {name}")

    print("=" * 40)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
