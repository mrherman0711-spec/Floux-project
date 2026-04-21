import os
import base64
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("EVOLUTION_BASE_URL", "").rstrip("/")
API_KEY = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE = "floux_salon_1"

HEADERS = {"apikey": API_KEY, "Content-Type": "application/json"}


def extract_qr(data: dict) -> str:
    """Extrae el base64 del QR desde cualquier estructura Evolution API v2."""
    if not isinstance(data, dict):
        return ""
    # v2.1.1 estructuras posibles
    candidates = [
        data.get("base64"),
        data.get("qrcode", {}).get("base64") if isinstance(data.get("qrcode"), dict) else None,
        data.get("qr", {}).get("base64") if isinstance(data.get("qr"), dict) else None,
        data.get("instance", {}).get("qrcode", {}).get("base64") if isinstance(data.get("instance"), dict) else None,
    ]
    for c in candidates:
        if c and isinstance(c, str) and len(c) > 100:
            return c
    return ""


def save_qr(qr_b64: str, path: str) -> bool:
    try:
        clean = qr_b64.split(",")[-1]
        with open(path, "wb") as f:
            f.write(base64.b64decode(clean))
        return True
    except Exception as e:
        print(f"   ❌ Error decodificando base64: {e}")
        return False


print("🧹 1. Limpiando instancia previa...")
try:
    r = requests.delete(f"{BASE_URL}/instance/delete/{INSTANCE}", headers=HEADERS, timeout=10)
    print(f"   → {r.status_code}")
except Exception as e:
    print(f"   (delete ignorado: {e})")
time.sleep(4)

print("✨ 2. Creando instancia nueva...")
r_create = requests.post(
    f"{BASE_URL}/instance/create",
    headers=HEADERS,
    json={"instanceName": INSTANCE, "qrcode": True, "integration": "WHATSAPP-BAILEYS"},
    timeout=30,
)
print(f"   → {r_create.status_code}")
create_data = r_create.json() if r_create.ok else {}

qr_path = f"qr_{INSTANCE}.png"

# Intento 1: QR viene en la respuesta del CREATE (lo más común en v2.1.1)
qr_b64 = extract_qr(create_data)
if qr_b64 and save_qr(qr_b64, qr_path):
    print(f"\n🎉 ¡QR OBTENIDO DEL CREATE! Guardado en: {qr_path}")
    print(f"👉 Abre '{qr_path}' en VS Code y escanea con WhatsApp.")
    raise SystemExit(0)

print("   (create no devolvió QR — hacemos polling al connect...)")

# Intento 2: polling al connect
print("\n⏳ 3. Polling a /instance/connect (hasta 12 intentos x 3s)...")
last_data = {}
for i in range(1, 13):
    try:
        r = requests.get(f"{BASE_URL}/instance/connect/{INSTANCE}", headers=HEADERS, timeout=15)
        last_data = r.json() if r.ok else {"_status": r.status_code, "_text": r.text[:200]}
    except Exception as e:
        last_data = {"_error": str(e)}
        print(f"   [{i:2d}/12] error: {e}")
        time.sleep(3)
        continue

    qr_b64 = extract_qr(last_data)
    print(f"   [{i:2d}/12] keys={list(last_data.keys())[:6]} qr={'SI' if qr_b64 else 'no'}")

    if qr_b64:
        if save_qr(qr_b64, qr_path):
            print(f"\n🎉 ¡QR OBTENIDO! Guardado en: {qr_path}")
            print(f"👉 Abre '{qr_path}' en VS Code y escanea con WhatsApp.")
            raise SystemExit(0)
    time.sleep(3)

# Intento 3: consultar estado de conexión y /instance/fetchInstances
print("\n🔍 4. Fallback: consultando fetchInstances...")
try:
    r = requests.get(f"{BASE_URL}/instance/fetchInstances?instanceName={INSTANCE}", headers=HEADERS, timeout=15)
    fetch_data = r.json()
    print(f"   → {r.status_code} — tipo: {type(fetch_data).__name__}")
    if isinstance(fetch_data, list) and fetch_data:
        qr_b64 = extract_qr(fetch_data[0])
    elif isinstance(fetch_data, dict):
        qr_b64 = extract_qr(fetch_data)

    if qr_b64 and save_qr(qr_b64, qr_path):
        print(f"\n🎉 ¡QR OBTENIDO DESDE FETCH! Guardado en: {qr_path}")
        raise SystemExit(0)
except Exception as e:
    print(f"   error: {e}")

print("\n❌ No se pudo obtener el QR tras todos los intentos.")
print(f"Última respuesta: {json.dumps(last_data, indent=2)[:500]}")
print(f"Respuesta create: {json.dumps(create_data, indent=2)[:500]}")
