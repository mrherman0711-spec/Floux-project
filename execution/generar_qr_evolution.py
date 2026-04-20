#!/usr/bin/env python3
"""
Onboarding de eSIM con Evolution API.
Ejecutar UNA VEZ por salón al activar la eSIM prepago.

Usage:
  python3 execution/generar_qr_evolution.py
"""
import os
import sys
import base64
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("EVOLUTION_BASE_URL", "").rstrip("/")
API_KEY  = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "floux_salon_1")

if not BASE_URL or not API_KEY:
    print("ERROR: EVOLUTION_BASE_URL y EVOLUTION_API_KEY deben estar en .env")
    sys.exit(1)

HEADERS = {"apikey": API_KEY, "Content-Type": "application/json"}

# Paso 1: Crear instancia
print(f"[1/2] Creando instancia '{INSTANCE}'...")
r = requests.post(f"{BASE_URL}/instance/create", headers=HEADERS, json={
    "instanceName": INSTANCE,
    "qrcode": True,
    "integration": "WHATSAPP-BAILEYS",
})
print(f"     → {r.status_code}: {r.text[:300]}")

# Paso 2: Obtener QR
print(f"\n[2/2] Obteniendo QR para '{INSTANCE}'...")
r2 = requests.get(f"{BASE_URL}/instance/connect/{INSTANCE}", headers=HEADERS)
data = r2.json()

qr_b64 = data.get("base64") or data.get("qrcode", {}).get("base64", "")
if not qr_b64:
    print(f"ERROR: No se encontró base64 en la respuesta:\n{json.dumps(data, indent=2)}")
    sys.exit(1)

qr_path = f"qr_{INSTANCE}.png"
with open(qr_path, "wb") as f:
    f.write(base64.b64decode(qr_b64.split(",")[-1]))

print(f"\n✅ QR guardado en: {qr_path}")
print("→ Abre el archivo y escanéalo con WhatsApp en la eSIM prepago.")
print("→ La sesión queda activa en Evolution API (SQLite interno del contenedor).")
