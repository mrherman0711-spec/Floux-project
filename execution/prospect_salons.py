#!/usr/bin/env python3
"""
Floux Salon Prospector: Google Maps → Claude enrich → Google Sheets
Usage:
    python3 execution/prospect_salons.py                          # Villaviciosa default
    python3 execution/prospect_salons.py --area "Boadilla del Monte"
    python3 execution/prospect_salons.py --all-zones --limit 10
    python3 execution/prospect_salons.py --sheet-url "https://docs.google.com/..."
"""
from __future__ import annotations
import os, sys, json, re, hashlib, time, argparse
from datetime import datetime
import googlemaps, gspread
from openai import OpenAI
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import httpx

load_dotenv()

ZONES = ["Villaviciosa de Odón","Boadilla del Monte","Majadahonda","Pozuelo de Alarcón","Las Rozas de Madrid"]
TERMS = ["peluquería","centro de estética","salón de belleza"]
COLS  = ["lead_id","fecha","nombre","categoria","localidad","direccion","telefono",
         "website","tiene_website","maps_url","valoracion","resenas","horario",
         "plataforma_reservas","num_empleados","manager","email","instagram",
         "icp_score","tier","posible_prospecto","dificultad_venta","razon","red_flags",
         "enfoque_venta","estado","notas"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]


# ── Google Maps ───────────────────────────────────────────────────────────────
def search_zone(gm, zone, term, limit=15):
    try:
        r = gm.places(query=f"{term} en {zone} Madrid", language="es", region="es")
        return r.get("results", [])[:limit]
    except Exception as e:
        print(f"  GMaps error: {e}", file=sys.stderr); return []

def place_details(gm, place_id):
    try:
        r = gm.place(place_id=place_id, language="es",
            fields=["name","formatted_phone_number","website","opening_hours",
                    "rating","user_ratings_total","formatted_address","url"])
        return r.get("result", {})
    except: return {}


# ── Website ───────────────────────────────────────────────────────────────────
def scrape_site(url):
    if not url: return ""
    try:
        r = httpx.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=6, follow_redirects=True)
        return re.sub(r"\s+"," ", re.sub(r"<[^>]+>"," ", r.text)).strip()[:5000]
    except: return ""

def detect_platform(name, text):
    s = f"{name} {text}".lower()
    for p in ["fresha","treatwell","booksy"]:
        if p in s: return p
    return "ninguna"

def extract_ig(text):
    m = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", text)
    return f"@{m.group(1)}" if m else ""


# ── Claude enrichment ─────────────────────────────────────────────────────────
def enrich(oai, salon, web_text):
    prompt = f"""Analiza este salón de west Madrid para Floux (agente WhatsApp €97/mes).
Salón: {salon['name']} | {salon['address']} | Rating: {salon['rating']} ({salon['reviews']} reseñas)
Web: {salon['website'] or 'ninguna'} | Plataforma: {salon['platform']}
Contenido web: {web_text[:2000] or 'sin web'}

ICP ideal Floux: teléfono-dependiente, 2-5 empleados, sin reservas online, ticket €20+, west Madrid.
Red flags: Fresha, solo 1 persona, franquicia.

Devuelve SOLO JSON:
{{"manager":"nombre o desconocido","email":"o vacío","empleados":2,"icp_score":75,
"prospecto":"Sí|No|Dudoso","dificultad":"Fácil|Media|Difícil",
"razon":"1 frase","red_flags":"lista o vacío","enfoque":"apertura en español"}}"""
    try:
        r = oai.chat.completions.create(model="gpt-4o-mini", max_tokens=400,
            response_format={"type":"json_object"},
            messages=[{"role":"user","content":prompt}])
        return json.loads(r.choices[0].message.content)
    except: pass
    return {"manager":"desconocido","email":"","empleados":0,"icp_score":0,
            "prospecto":"Dudoso","dificultad":"Media","razon":"","red_flags":"","enfoque":""}


# ── Google Sheets ─────────────────────────────────────────────────────────────
def get_creds():
    creds = None
    if os.path.exists("token.json"):
        try: creds = Credentials.from_authorized_user_info(json.load(open("token.json")), SCOPES)
        except: pass
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS","credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        open("token.json","w").write(creds.to_json())
    return creds

def get_sheet(sheet_url=None):
    gc = gspread.authorize(get_creds())
    if sheet_url:
        sid = sheet_url.split("/d/")[1].split("/")[0]
        ss = gc.open_by_key(sid); ws = ss.sheet1
    else:
        ss = gc.create(f"Floux Prospectos {datetime.now().strftime('%Y-%m')}")
        ws = ss.sheet1; ws.update(values=[COLS], range_name="A1")
        ws.format("A1:Z1",{"textFormat":{"bold":True}})
        email = os.getenv("USER_EMAIL")
        if email: ss.share(email, perm_type="user", role="writer")
    return ss, ws

def is_dup(ws, lead_id):
    try: return ws.find(lead_id, in_column=1) is not None
    except: return False


# ── Main pipeline ─────────────────────────────────────────────────────────────
def run(zones, limit=15, sheet_url=None):
    gm = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY",""))
    oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY",""))
    ss, ws = get_sheet(sheet_url)
    new, dup = 0, 0
    print(f"\nFloux Prospector — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    for zone in zones:
        print(f"\n📍 {zone}")
        for term in TERMS:
            for place in search_zone(gm, zone, term, limit):
                d = place_details(gm, place.get("place_id",""))
                if not d: continue
                name = d.get("name","")
                addr = d.get("formatted_address","")
                web  = d.get("website","")
                hours_list = d.get("opening_hours",{}).get("weekday_text",[])
                salon = {"name":name,"address":addr,"website":web,
                         "rating":d.get("rating",""),"reviews":d.get("user_ratings_total",""),
                         "platform":detect_platform(name,"")}
                web_text = scrape_site(web)
                salon["platform"] = detect_platform(name, web_text)
                ai = enrich(oai, salon, web_text)
                lid = hashlib.md5(f"{name}|{addr}".lower().encode()).hexdigest()[:12]
                if is_dup(ws, lid): dup += 1; continue
                score = int(ai.get("icp_score",0))
                tier = "1" if score>=70 else "2" if score>=45 else "3"
                row_data = {
                    "lead_id":lid,"fecha":datetime.now().strftime("%Y-%m-%d"),
                    "nombre":name,"categoria":term,"localidad":zone,"direccion":addr,
                    "telefono":d.get("formatted_phone_number",""),"website":web,
                    "tiene_website":"Sí" if web else "No",
                    "maps_url":d.get("url",""),"valoracion":str(d.get("rating","")),
                    "resenas":str(d.get("user_ratings_total","")),"horario":" | ".join(hours_list)[:150],
                    "plataforma_reservas":salon["platform"],
                    "num_empleados":str(ai.get("empleados","")),
                    "manager":ai.get("manager","desconocido"),"email":ai.get("email",""),
                    "instagram":extract_ig(web_text),"icp_score":str(score),"tier":tier,
                    "posible_prospecto":ai.get("prospecto","Dudoso"),
                    "dificultad_venta":ai.get("dificultad","Media"),
                    "razon":ai.get("razon",""),"red_flags":ai.get("red_flags",""),
                    "enfoque_venta":ai.get("enfoque",""),"estado":"Sin contactar","notas":"",
                }
                ws.append_row([str(row_data.get(c,"")) for c in COLS], value_input_option="USER_ENTERED")
                print(f"  ✅ {name} — Tier {tier} (score {score})")
                new += 1; time.sleep(0.5)

    sheet_link = f"https://docs.google.com/spreadsheets/d/{ss.id}"
    print(f"\n{'='*50}\n✅ Nuevos: {new} | Duplicados: {dup}\n📊 {sheet_link}")
    os.makedirs(".tmp",exist_ok=True)
    open(".tmp/last_sheet.txt","w").write(sheet_link)
    return sheet_link

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--area"); p.add_argument("--all-zones", action="store_true")
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--sheet-url")
    a = p.parse_args()
    zones = ZONES if a.all_zones else ([a.area] if a.area else ["Villaviciosa de Odón"])
    run(zones, a.limit, a.sheet_url)
