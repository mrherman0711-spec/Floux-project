"""
AI conversation engine — builds prompts, calls OpenAI, parses responses.
Self-learning: logs interpretation errors and injects them as context so the
bot doesn't repeat the same mistakes.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL, TIMEZONE, BASE_DIR

log = logging.getLogger("floux.ai")

client = None

# Where error learnings are stored per salon
LEARNINGS_DIR = BASE_DIR / "learnings"
LEARNINGS_DIR.mkdir(exist_ok=True)


def _get_client() -> OpenAI:
    global client
    if client is None:
        client = OpenAI(api_key=OPENAI_API_KEY)
    return client


# ── Self-learning error log ──────────────────────────────────

def load_learnings(salon_id: str) -> str:
    """Load past error learnings for this salon. Returns formatted string or ''."""
    path = LEARNINGS_DIR / f"{salon_id}.json"
    if not path.exists():
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            learnings = json.load(f)
        if not learnings:
            return ""
        # Only inject the 10 most recent learnings to keep prompt short
        recent = learnings[-10:]
        lines = "\n".join(f"- {l['lesson']}" for l in recent)
        return f"\nERRORES PASADOS A EVITAR:\n{lines}\n"
    except Exception:
        return ""


def save_learning(salon_id: str, user_message: str, wrong_reply: str, lesson: str) -> None:
    """Persist a learning so the bot avoids this mistake in future conversations."""
    path = LEARNINGS_DIR / f"{salon_id}.json"
    try:
        learnings = []
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                learnings = json.load(f)
        learnings.append({
            "ts": datetime.now(ZoneInfo(TIMEZONE)).isoformat(),
            "user_said": user_message,
            "bot_replied": wrong_reply,
            "lesson": lesson,
        })
        # Cap at 50 learnings per salon
        learnings = learnings[-50:]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(learnings, f, ensure_ascii=False, indent=2)
        log.info(f"Learning saved for {salon_id}: {lesson}")
    except Exception as e:
        log.error(f"Failed to save learning: {e}")


def extract_learning(salon_id: str, conversation: list[dict],
                     wrong_reply: str, user_correction: str) -> None:
    """
    Ask GPT to summarize what went wrong and store it as a lesson.
    Called when the bot detects it misunderstood the user.
    """
    try:
        ai_client = _get_client()
        recent = conversation[-6:] if len(conversation) > 6 else conversation
        ctx = "\n".join(
            f"{'Cliente' if t['role'] == 'user' else 'Bot'}: {t['content']}"
            for t in recent
        )
        r = ai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{
                "role": "user",
                "content": (
                    f"El bot cometió un error en esta conversación:\n\n{ctx}\n\n"
                    f"El bot respondió: \"{wrong_reply}\"\n"
                    f"El cliente corrigió o mostró confusión con: \"{user_correction}\"\n\n"
                    "Escribe UNA frase corta (máx 20 palabras) que describa la regla que el bot debe recordar "
                    "para no cometer este error de nuevo. Empieza con 'Cuando el cliente dice...' o 'No interpretar...' "
                    "o 'Si el contexto muestra...'. Solo la frase, sin explicación."
                ),
            }],
            temperature=0.1,
            max_tokens=60,
        )
        lesson = r.choices[0].message.content.strip().strip('"')
        save_learning(salon_id, user_correction, wrong_reply, lesson)
    except Exception as e:
        log.error(f"Learning extraction failed: {e}")


# ── Prompt builder ───────────────────────────────────────────

def build_system_prompt(salon_config: dict, availability_slots: list[dict] | None = None) -> str:
    """Build the system prompt with real data injected."""
    base_prompt = salon_config.get("system_prompt", "")
    salon_id = salon_config.get("salon_id", "")

    # Build services list
    services_text = ""
    for svc in salon_config.get("services", []):
        services_text += f"- {svc['name']}: {svc['price']}€ ({svc['duration_min']} min)\n"

    # Build staff list
    staff_text = ""
    for member in salon_config.get("staff", []):
        services_str = ", ".join(member["services"])
        staff_text += f"- {member['name']}: {services_str}\n"

    # Build availability (None=error, []=no slots, [...]= slots available)
    if availability_slots:
        slots_text = ""
        for slot in availability_slots[:10]:
            dt = slot.get("datetime", "")
            staff = slot.get("staff", "")
            try:
                dt_obj = datetime.fromisoformat(dt)
                day_names_es = {
                    0: "lunes", 1: "martes", 2: "miércoles",
                    3: "jueves", 4: "viernes", 5: "sábado", 6: "domingo"
                }
                day = day_names_es.get(dt_obj.weekday(), "")
                formatted = f"{day} {dt_obj.day}/{dt_obj.month} a las {dt_obj.strftime('%H:%M')}"
                slots_text += f"- {formatted} con {staff}\n"
            except (ValueError, AttributeError):
                slots_text += f"- {dt} con {staff}\n"
    elif availability_slots is not None:
        slots_text = "No hay huecos disponibles en los próximos 7 días. Comunícaselo al cliente con amabilidad y pídele que llame directamente al centro para buscar fecha."
    else:
        slots_text = "Sistema de disponibilidad no disponible temporalmente. Pregunta al cliente qué día y hora le viene bien y confirma la cita directamente."

    # Current datetime context
    now = datetime.now(ZoneInfo(TIMEZONE))
    day_names_es = {
        0: "lunes", 1: "martes", 2: "miércoles",
        3: "jueves", 4: "viernes", 5: "sábado", 6: "domingo"
    }
    date_context = f"Hoy es {day_names_es[now.weekday()]} {now.day}/{now.month}/{now.year}, son las {now.strftime('%H:%M')}."

    # Inject self-learned error lessons
    learnings = load_learnings(salon_id)

    prompt = base_prompt.replace("{SERVICES_LIST}", services_text)
    prompt = prompt.replace("{STAFF_LIST}", staff_text)
    prompt = prompt.replace("{AVAILABILITY_SLOTS}", slots_text)
    prompt = f"{date_context}\n\n{prompt}{learnings}"

    return prompt


# ── Ambiguity detection ──────────────────────────────────────

def _is_ambiguous_correction(text: str, prev_reply: str) -> bool:
    """
    Heuristic: detect if the client is correcting a bot misunderstanding.
    Signals: short message after a bot question, starts with negation,
    or repeats something differently.
    """
    text = text.strip().lower()
    correction_signals = [
        "no,", "no ", "eso no", "no era", "me refería", "quería decir",
        "quiero decir", "no eso", "no me refiero", "dije", "o sea",
    ]
    return any(text.startswith(s) for s in correction_signals)


# ── Main chat function ───────────────────────────────────────

def chat(salon_config: dict, conversation: list[dict],
         user_message: str, availability_slots: list[dict] | None = None) -> dict:
    """
    Run one turn of AI conversation.

    Args:
        salon_config: The salon's config dict
        conversation: List of {"role": "user"|"assistant", "content": "..."} dicts
        user_message: The new message from the client
        availability_slots: Current available slots

    Returns:
        Parsed JSON response dict with keys: reply, language, intent, booking_data, escalate, conversation_complete
    """
    salon_id = salon_config.get("salon_id", "")
    system_prompt = build_system_prompt(salon_config, availability_slots)

    # Detect if client is correcting a misunderstanding → trigger learning
    if conversation and _is_ambiguous_correction(user_message, ""):
        last_bot = next(
            (t["content"] for t in reversed(conversation) if t["role"] == "assistant"),
            None,
        )
        if last_bot:
            extract_learning(salon_id, conversation, last_bot, user_message)

    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history
    for turn in conversation:
        messages.append({"role": turn["role"], "content": turn["content"]})

    # Add new user message
    messages.append({"role": "user", "content": user_message})

    # Call OpenAI
    ai_client = _get_client()

    for attempt in range(2):
        try:
            response = ai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=800,
            )

            raw = response.choices[0].message.content
            parsed = json.loads(raw)

            # Validate required fields
            result = {
                "reply": parsed.get("reply", ""),
                "language": parsed.get("language", "es"),
                "intent": parsed.get("intent", "greeting"),
                "booking_data": parsed.get("booking_data", {
                    "service": "", "datetime": "", "client_name": "",
                    "staff_preference": "", "staff_assigned": "", "client_email": "",
                }),
                "escalate": parsed.get("escalate", False),
                "conversation_complete": parsed.get("conversation_complete", False),
            }

            if not result["reply"]:
                if attempt == 0:
                    log.warning("Empty reply from AI, retrying...")
                    continue
                result["reply"] = "Disculpa, no he entendido bien. ¿Puedes repetirlo?"

            return result

        except json.JSONDecodeError as e:
            log.error(f"JSON parse error from AI (attempt {attempt + 1}): {e}")
            if attempt == 0:
                messages.append({
                    "role": "system",
                    "content": "IMPORTANTE: Tu respuesta DEBE ser JSON válido. Inténtalo de nuevo.",
                })
                continue
        except Exception as e:
            log.error(f"OpenAI API error: {e}")
            break

    # Fallback if all attempts fail
    return {
        "reply": "Disculpa, tengo un problema técnico. ¿Podrías escribirme de nuevo en unos minutos?",
        "language": "es",
        "intent": "greeting",
        "booking_data": {},
        "escalate": True,
        "conversation_complete": False,
    }
