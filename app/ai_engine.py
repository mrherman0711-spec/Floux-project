"""
AI conversation engine — builds prompts, calls OpenAI, parses responses.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL, TIMEZONE

log = logging.getLogger("floux.ai")

client = None


def _get_client() -> OpenAI:
    global client
    if client is None:
        client = OpenAI(api_key=OPENAI_API_KEY)
    return client


def build_system_prompt(salon_config: dict, availability_slots: list[dict] | None = None) -> str:
    """Build the system prompt with real data injected."""
    base_prompt = salon_config.get("system_prompt", "")

    # Build services list
    services_text = ""
    for svc in salon_config.get("services", []):
        services_text += f"- {svc['name']}: {svc['price']}€ ({svc['duration_min']} min)\n"

    # Build staff list
    staff_text = ""
    for member in salon_config.get("staff", []):
        services_str = ", ".join(member["services"])
        staff_text += f"- {member['name']}: {services_str}\n"

    # Build availability
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
    else:
        slots_text = "No se ha podido consultar la disponibilidad en este momento. Pregunta al cliente cuándo le vendría bien y confirma que verificarás el hueco."

    # Current datetime context
    now = datetime.now(ZoneInfo(TIMEZONE))
    day_names_es = {
        0: "lunes", 1: "martes", 2: "miércoles",
        3: "jueves", 4: "viernes", 5: "sábado", 6: "domingo"
    }
    date_context = f"Hoy es {day_names_es[now.weekday()]} {now.day}/{now.month}/{now.year}, son las {now.strftime('%H:%M')}."

    prompt = base_prompt.replace("{SERVICES_LIST}", services_text)
    prompt = prompt.replace("{STAFF_LIST}", staff_text)
    prompt = prompt.replace("{AVAILABILITY_SLOTS}", slots_text)
    prompt = f"{date_context}\n\n{prompt}"

    return prompt


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
    system_prompt = build_system_prompt(salon_config, availability_slots)

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
                temperature=0.3,
                max_tokens=500,
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
                    "staff_preference": "", "staff_assigned": "",
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
                # Add a nudge to the prompt
                messages.append({
                    "role": "system",
                    "content": "IMPORTANTE: Tu respuesta DEBE ser JSON válido. Inténtalo de nuevo."
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
