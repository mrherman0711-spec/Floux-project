"""
Client database + session management — SQLite for speed and reliability.
Google Sheets was too slow for real-time conversation. SQLite handles it locally,
and we sync to Sheets for the owner's visibility.

Tables:
  - clients: permanent client records (name, phone, history, preferences)
  - sessions: active conversation sessions
  - appointments: all bookings (past + future)
  - messages: full conversation log
"""
from __future__ import annotations

import json
import sqlite3
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.config import DATA_DIR, TIMEZONE

log = logging.getLogger("floux.db")

DB_PATH = DATA_DIR / "floux.db"
TZ = ZoneInfo(TIMEZONE)


def _now() -> str:
    return datetime.now(TZ).isoformat()


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            name TEXT DEFAULT '',
            email TEXT DEFAULT '',
            language TEXT DEFAULT 'es',
            salon_id TEXT NOT NULL,
            notes TEXT DEFAULT '',
            allergies TEXT DEFAULT '',
            preferred_staff TEXT DEFAULT '',
            total_visits INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0,
            last_visit_at TEXT DEFAULT '',
            next_appointment_at TEXT DEFAULT '',
            reliability_score REAL DEFAULT 1.0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            salon_id TEXT NOT NULL,
            call_sid TEXT DEFAULT '',
            status TEXT DEFAULT 'active',
            conversation TEXT DEFAULT '[]',
            booking_data TEXT DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            client_name TEXT DEFAULT '',
            salon_id TEXT NOT NULL,
            service TEXT NOT NULL,
            staff TEXT DEFAULT '',
            datetime_start TEXT NOT NULL,
            datetime_end TEXT NOT NULL,
            price REAL DEFAULT 0.0,
            status TEXT DEFAULT 'confirmed',
            platform TEXT DEFAULT 'google_calendar',
            reference TEXT DEFAULT '',
            reminder_24h_sent INTEGER DEFAULT 0,
            reminder_1h_sent INTEGER DEFAULT 0,
            review_sent INTEGER DEFAULT 0,
            no_show INTEGER DEFAULT 0,
            cancelled_at TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            salon_id TEXT NOT NULL,
            direction TEXT NOT NULL,
            body TEXT NOT NULL,
            message_id TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_clients_phone ON clients(phone);
        CREATE INDEX IF NOT EXISTS idx_sessions_phone ON sessions(phone);
        CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
        CREATE INDEX IF NOT EXISTS idx_appointments_phone ON appointments(phone);
        CREATE INDEX IF NOT EXISTS idx_appointments_datetime ON appointments(datetime_start);
        CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);
        CREATE INDEX IF NOT EXISTS idx_messages_phone ON messages(phone);
    """)
    conn.commit()

    # Migrations — add columns that may not exist in older DBs
    for migration in [
        "ALTER TABLE clients ADD COLUMN email TEXT DEFAULT ''",
    ]:
        try:
            conn.execute(migration)
            conn.commit()
        except Exception:
            pass  # Column already exists

    conn.close()
    log.info("Database initialized")


# ── Clients ──────────────────────────────────────────────────

def get_or_create_client(phone: str, salon_id: str) -> dict:
    conn = get_db()
    row = conn.execute("SELECT * FROM clients WHERE phone = ?", (phone,)).fetchone()
    if row:
        conn.close()
        return dict(row)
    now = _now()
    conn.execute(
        "INSERT INTO clients (phone, salon_id, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (phone, salon_id, now, now),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM clients WHERE phone = ?", (phone,)).fetchone()
    conn.close()
    return dict(row)


def update_client(phone: str, **kwargs) -> None:
    conn = get_db()
    kwargs["updated_at"] = _now()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [phone]
    conn.execute(f"UPDATE clients SET {sets} WHERE phone = ?", values)
    conn.commit()
    conn.close()


def get_inactive_clients(salon_id: str, days: int = 30) -> list[dict]:
    """Clients who haven't visited in X days."""
    cutoff = (datetime.now(TZ) - timedelta(days=days)).isoformat()
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM clients WHERE salon_id = ? AND last_visit_at != '' AND last_visit_at < ? AND total_visits > 0",
        (salon_id, cutoff),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Sessions ─────────────────────────────────────────────────

def get_active_session(phone: str) -> dict | None:
    conn = get_db()
    # 'booked' sessions kept for 4h post-confirmation (follow-up questions, reviews).
    # After 4h or if cancelled, client starts fresh.
    four_hours_ago = (datetime.now(TZ) - timedelta(hours=4)).isoformat()
    row = conn.execute(
        """SELECT * FROM sessions WHERE phone = ?
           AND (
             status IN ('active', 'escalated')
             OR (status = 'booked' AND updated_at >= ?)
           )
           ORDER BY created_at DESC LIMIT 1""",
        (phone, four_hours_ago),
    ).fetchone()
    conn.close()
    if not row:
        return None
    session = dict(row)
    # Reactivate escalated sessions so the conversation continues
    if session["status"] == "escalated":
        conn2 = get_db()
        conn2.execute("UPDATE sessions SET status = 'active', updated_at = ? WHERE id = ?",
                      (_now(), session["id"]))
        conn2.commit()
        conn2.close()
        session["status"] = "active"
    session["conversation"] = json.loads(session["conversation"])
    session["booking_data"] = json.loads(session["booking_data"])
    return session


def create_session(phone: str, salon_id: str, call_sid: str = "") -> dict:
    now = _now()
    conn = get_db()
    conn.execute(
        "INSERT INTO sessions (phone, salon_id, call_sid, status, conversation, booking_data, created_at, updated_at) VALUES (?, ?, ?, 'active', '[]', '{}', ?, ?)",
        (phone, salon_id, call_sid, now, now),
    )
    conn.commit()
    conn.close()
    return get_active_session(phone)


def update_session(session_id: int, **kwargs) -> None:
    conn = get_db()
    if "conversation" in kwargs and isinstance(kwargs["conversation"], list):
        kwargs["conversation"] = json.dumps(kwargs["conversation"], ensure_ascii=False)
    if "booking_data" in kwargs and isinstance(kwargs["booking_data"], dict):
        kwargs["booking_data"] = json.dumps(kwargs["booking_data"], ensure_ascii=False)
    kwargs["updated_at"] = _now()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [session_id]
    conn.execute(f"UPDATE sessions SET {sets} WHERE id = ?", values)
    conn.commit()
    conn.close()


def check_duplicate_call(call_sid: str) -> bool:
    if not call_sid:
        return False
    conn = get_db()
    row = conn.execute("SELECT id FROM sessions WHERE call_sid = ?", (call_sid,)).fetchone()
    conn.close()
    return row is not None


# ── Appointments ─────────────────────────────────────────────

def create_appointment(phone: str, salon_id: str, service: str, staff: str,
                       datetime_start: str, datetime_end: str, price: float = 0.0,
                       client_name: str = "", platform: str = "google_calendar",
                       reference: str = "") -> dict:
    now = _now()
    conn = get_db()
    conn.execute(
        """INSERT INTO appointments
           (phone, client_name, salon_id, service, staff, datetime_start, datetime_end,
            price, platform, reference, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (phone, client_name, salon_id, service, staff, datetime_start, datetime_end,
         price, platform, reference, now),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM appointments WHERE rowid = last_insert_rowid()").fetchone()
    conn.close()
    return dict(row)


def get_upcoming_appointments(salon_id: str, hours_ahead: int = 24) -> list[dict]:
    """Appointments within the next N hours."""
    now = datetime.now(TZ)
    cutoff = (now + timedelta(hours=hours_ahead)).isoformat()
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM appointments WHERE salon_id = ? AND datetime_start > ? AND datetime_start <= ? AND status = 'confirmed'",
        (salon_id, now.isoformat(), cutoff),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_appointments_for_day(salon_id: str, date_str: str) -> list[dict]:
    """All appointments for a specific date (YYYY-MM-DD)."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM appointments WHERE salon_id = ? AND datetime_start LIKE ? AND status = 'confirmed' ORDER BY datetime_start",
        (salon_id, f"{date_str}%"),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_reminder_sent(appointment_id: int, reminder_type: str) -> None:
    conn = get_db()
    col = "reminder_24h_sent" if reminder_type == "24h" else "reminder_1h_sent"
    conn.execute(f"UPDATE appointments SET {col} = 1 WHERE id = ?", (appointment_id,))
    conn.commit()
    conn.close()


def mark_review_sent(appointment_id: int) -> None:
    conn = get_db()
    conn.execute("UPDATE appointments SET review_sent = 1 WHERE id = ?", (appointment_id,))
    conn.commit()
    conn.close()


def mark_no_show(appointment_id: int) -> None:
    conn = get_db()
    conn.execute("UPDATE appointments SET no_show = 1, status = 'no_show' WHERE id = ?", (appointment_id,))
    conn.commit()
    conn.close()


def cancel_appointment(appointment_id: int) -> None:
    conn = get_db()
    conn.execute(
        "UPDATE appointments SET status = 'cancelled', cancelled_at = ? WHERE id = ?",
        (_now(), appointment_id),
    )
    conn.commit()
    conn.close()


def get_past_appointments_needing_review(salon_id: str) -> list[dict]:
    """Appointments that ended 2+ hours ago and haven't had a review request."""
    cutoff = (datetime.now(TZ) - timedelta(hours=2)).isoformat()
    # Also require datetime_end is non-empty and looks like a real date (starts with 20)
    # to avoid triggering on appointments saved with empty end times due to parse errors
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM appointments WHERE salon_id = ? AND datetime_end != '' AND datetime_end LIKE '20%' AND datetime_end < ? AND review_sent = 0 AND status = 'confirmed'",
        (salon_id, cutoff),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Messages ─────────────────────────────────────────────────

def log_message(phone: str, salon_id: str, direction: str, body: str,
                message_id: str = "") -> None:
    conn = get_db()
    conn.execute(
        "INSERT INTO messages (phone, salon_id, direction, body, message_id, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (phone, salon_id, direction, body, message_id, _now()),
    )
    conn.commit()
    conn.close()


# ── Stats ────────────────────────────────────────────────────

def get_daily_stats(salon_id: str, date_str: str) -> dict:
    """Stats for owner daily digest."""
    conn = get_db()

    appointments = conn.execute(
        "SELECT COUNT(*) as count, COALESCE(SUM(price), 0) as revenue FROM appointments WHERE salon_id = ? AND datetime_start LIKE ? AND status = 'confirmed'",
        (salon_id, f"{date_str}%"),
    ).fetchone()

    no_shows = conn.execute(
        "SELECT COUNT(*) as count FROM appointments WHERE salon_id = ? AND datetime_start LIKE ? AND no_show = 1",
        (salon_id, f"{date_str}%"),
    ).fetchone()

    new_clients = conn.execute(
        "SELECT COUNT(*) as count FROM clients WHERE salon_id = ? AND created_at LIKE ?",
        (salon_id, f"{date_str}%"),
    ).fetchone()

    messages_count = conn.execute(
        "SELECT COUNT(*) as count FROM messages WHERE salon_id = ? AND created_at LIKE ?",
        (salon_id, f"{date_str}%"),
    ).fetchone()

    conn.close()

    return {
        "date": date_str,
        "appointments": dict(appointments)["count"],
        "revenue": dict(appointments)["revenue"],
        "no_shows": dict(no_shows)["count"],
        "new_clients": dict(new_clients)["count"],
        "messages": dict(messages_count)["count"],
    }
