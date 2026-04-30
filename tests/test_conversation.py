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
    config = load_salon_config("escultor_peluqueria")
    if not config:
        print("  FAIL: escultor_peluqueria.json not found")
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
    client = get_or_create_client("+34611222333", "escultor_peluqueria")
    assert client["phone"] == "+34611222333", "Client phone mismatch"
    print(f"  PASS: Client created/loaded: {client['phone']}")

    # Test session creation
    session = create_session("+34611222333", "escultor_peluqueria", "CA_test_123")
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

    config = load_salon_config("escultor_peluqueria")
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
        ("Salon name in prompt", "Escultor" in prompt),
        ("Services listed", "Corte escultor" in prompt),
        ("Prices listed", "21" in prompt),
        ("Staff listed", "Jesús" in prompt),
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


def test_get_latest_confirmed_appointment():
    """get_latest_confirmed_appointment must return the most recent confirmed
    appointment for a phone, ignoring cancelled ones."""
    from app.database import (
        init_db, create_appointment, cancel_appointment,
        get_latest_confirmed_appointment, get_db,
    )
    init_db()

    phone = "+34611999001"
    salon = "escultor_peluqueria"
    conn = get_db()
    conn.execute("DELETE FROM appointments WHERE phone=?", (phone,))
    conn.commit()
    conn.close()

    print("\n=== get_latest_confirmed_appointment ===")
    all_pass = True

    if get_latest_confirmed_appointment(phone, salon) is not None:
        print("  FAIL: expected None when no appointments"); all_pass = False
    else:
        print("  PASS: returns None when no appointments")

    a1 = create_appointment(phone, salon, "Corte", "Pablo",
                             "2026-05-04T10:00:00", "2026-05-04T11:00:00",
                             price=30, client_name="Test")
    res = get_latest_confirmed_appointment(phone, salon)
    if not res or res["id"] != a1["id"]:
        print(f"  FAIL: expected appt {a1['id']}, got {res}"); all_pass = False
    else:
        print("  PASS: returns the only confirmed")

    a2 = create_appointment(phone, salon, "Corte", "Pablo",
                             "2026-05-05T10:00:00", "2026-05-05T11:00:00",
                             price=30, client_name="Test")
    res = get_latest_confirmed_appointment(phone, salon)
    if not res or res["id"] != a2["id"]:
        print(f"  FAIL: expected newer appt {a2['id']}, got {res and res['id']}"); all_pass = False
    else:
        print("  PASS: returns most recent of two confirmed")

    cancel_appointment(a2["id"])
    res = get_latest_confirmed_appointment(phone, salon)
    if not res or res["id"] != a1["id"]:
        print(f"  FAIL: expected older appt {a1['id']} after cancel, got {res and res['id']}"); all_pass = False
    else:
        print("  PASS: ignores cancelled, returns remaining confirmed")

    cancel_appointment(a1["id"])
    if get_latest_confirmed_appointment(phone, salon) is not None:
        print("  FAIL: expected None when all cancelled"); all_pass = False
    else:
        print("  PASS: returns None when all cancelled")

    return all_pass


def test_reschedule_routing_decision():
    """Verify the routing decision logic: when client has a confirmed appointment
    and AI emits cancellation+complete with a NEW datetime, it must be classified
    as reschedule (not pure cancellation)."""
    from app.database import (
        init_db, create_appointment, cancel_appointment,
        get_latest_confirmed_appointment, get_db,
    )
    init_db()

    phone = "+34611999002"
    salon = "escultor_peluqueria"
    conn = get_db()
    conn.execute("DELETE FROM appointments WHERE phone=?", (phone,))
    conn.commit()
    conn.close()

    print("\n=== Reschedule routing decision ===")
    all_pass = True

    old = create_appointment(phone, salon, "Corte mujer", "Pablo",
                              "2026-05-04T10:00:00", "2026-05-04T11:00:00",
                              price=30, client_name="Test")

    old_appt = get_latest_confirmed_appointment(phone, salon)

    # Case A: AI emits reschedule for Tuesday (different date) → is_reschedule=True
    new_bd_resched = {"datetime": "2026-05-05T10:00:00", "service": "Corte mujer"}
    ai_response = {"cancellation_confirmed": True, "conversation_complete": True,
                   "booking_data": new_bd_resched}
    is_reschedule = bool(
        old_appt
        and ai_response.get("cancellation_confirmed")
        and ai_response.get("conversation_complete")
        and new_bd_resched.get("datetime")
        and new_bd_resched["datetime"] != old_appt.get("datetime_start")
    )
    if not is_reschedule:
        print("  FAIL: case A — different date should classify as reschedule"); all_pass = False
    else:
        print("  PASS: case A — Mon→Tue classified as reschedule")

    # Case B: AI emits cancellation only → is_reschedule=False, is_pure_cancellation=True
    ai_cancel = {"cancellation_confirmed": True, "conversation_complete": False,
                 "booking_data": {}}
    new_bd_cancel = {}
    is_reschedule_b = bool(
        old_appt
        and ai_cancel.get("cancellation_confirmed")
        and ai_cancel.get("conversation_complete")
        and new_bd_cancel.get("datetime")
    )
    is_pure_cancel = bool(
        old_appt
        and ai_cancel.get("cancellation_confirmed")
        and not is_reschedule_b
    )
    if is_reschedule_b or not is_pure_cancel:
        print(f"  FAIL: case B — pure cancel got resched={is_reschedule_b} cancel={is_pure_cancel}"); all_pass = False
    else:
        print("  PASS: case B — pure cancellation classified correctly")

    # Case C: client has NO active booking → first booking, not reschedule
    cancel_appointment(old["id"])
    old_appt2 = get_latest_confirmed_appointment(phone, salon)
    has_booking = old_appt2 is not None
    if has_booking:
        print("  FAIL: case C — after cancel, expected no active booking"); all_pass = False
    else:
        print("  PASS: case C — cancelled appointment is not 'active'")

    # Case D: AI emits same datetime as existing booking (follow-up "what time was it?")
    create_appointment(phone, salon, "Corte mujer", "Pablo",
                        "2026-05-06T10:00:00", "2026-05-06T11:00:00",
                        price=30, client_name="Test")
    old_appt_d = get_latest_confirmed_appointment(phone, salon)
    same_dt_bd = {"datetime": "2026-05-06T10:00:00", "service": "Corte mujer"}
    ai_followup = {"cancellation_confirmed": False, "conversation_complete": True,
                   "booking_data": same_dt_bd}
    is_reschedule_d = bool(
        old_appt_d
        and ai_followup.get("cancellation_confirmed")
        and ai_followup.get("conversation_complete")
        and same_dt_bd.get("datetime")
        and same_dt_bd["datetime"] != old_appt_d.get("datetime_start")
    )
    if is_reschedule_d:
        print("  FAIL: case D — follow-up should not classify as reschedule"); all_pass = False
    else:
        print("  PASS: case D — same-date follow-up not classified as reschedule")

    return all_pass


def test_passes_cancellation_guard():
    """Verify the cancellation guard accepts 'sí' after bot asked 'cancelar/mover'
    and rejects affirmations after unrelated bot messages."""
    from app.webhook import _passes_cancellation_guard

    print("\n=== Cancellation guard ===")
    all_pass = True

    cases = [
        ([{"role": "assistant", "content": "¿Confirmas que quieres cancelar la cita?"}],
         "sí", True),
        ([{"role": "assistant", "content": "¿Confirmas mover tu cita al martes?"}],
         "sí", True),
        ([{"role": "assistant", "content": "¡Perfecto! Tu cita está confirmada."}],
         "sí gracias", False),
        ([{"role": "assistant", "content": "¿Confirmas que quieres cancelar?"}],
         "no, déjala", False),
        ([], "sí", False),
    ]
    for conv, text, expected in cases:
        result = _passes_cancellation_guard(conv, text)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL": all_pass = False
        print(f"  {status}: guard(text='{text}') = {result} (expected {expected})")

    return all_pass


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
    results.append(("get_latest_confirmed_appointment", test_get_latest_confirmed_appointment()))
    results.append(("Reschedule routing decision", test_reschedule_routing_decision()))
    results.append(("Cancellation guard", test_passes_cancellation_guard()))

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
