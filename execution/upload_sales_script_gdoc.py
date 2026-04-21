#!/usr/bin/env python3
"""
Upload the Floux sales script CSV as a formatted Google Doc.
Uses Drive API (drive scope) to upload HTML converted to Google Doc.
"""

import csv
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execution.google_auth import get_google_credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

CSV_PATH = Path(__file__).resolve().parent.parent / "dream100" / "sales_script_floux.csv"
DOC_TITLE = "Floux — Sales Script Completo"


def read_csv():
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def esc(text):
    return html.escape(text)


def build_html(rows):
    """Build an HTML document from the CSV rows."""
    parts = []
    parts.append("""<html><head><meta charset="utf-8">
<style>
body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
h1 { color: #1a1a2e; border-bottom: 2px solid #16213e; padding-bottom: 8px; }
h2 { color: #0f3460; margin-top: 24px; }
.situacion { font-weight: bold; margin-top: 12px; }
.dialogo { color: #004488; margin: 4px 0 4px 16px; }
.instruccion { margin: 4px 0 4px 16px; }
.nota { color: #666; font-style: italic; font-size: 10pt; margin: 2px 0 12px 16px; }
.fase-box { background: #f0f4f8; border-left: 4px solid #0f3460; padding: 12px 16px; margin: 16px 0; }
</style></head><body>""")

    parts.append("<h1>FLOUX — SALES SCRIPT COMPLETO</h1>")
    parts.append("<p><em>Manual de campo para Max. Leer antes de entrar a cualquier salón.</em></p>")

    current_fase = None
    current_subfase = None

    for row in rows:
        fase = row.get("FASE", "").strip()
        subfase = row.get("SUBFASE", "").strip()
        situacion = row.get("SITUACIÓN", "").strip()
        que_decir = row.get("QUÉ DECIR (PALABRAS EXACTAS)", "").strip()
        notas = row.get("NOTAS / CONTEXTO", "").strip()

        if fase != current_fase:
            if current_fase is not None:
                parts.append("</div>")  # close previous fase-box
            current_fase = fase
            current_subfase = None
            parts.append(f'<h1>{esc(fase)}</h1>')
            parts.append('<div class="fase-box">')

        if subfase and subfase != current_subfase:
            current_subfase = subfase
            parts.append(f'<h2>{esc(subfase)}</h2>')

        if situacion:
            parts.append(f'<p class="situacion">📍 {esc(situacion)}</p>')

        if que_decir:
            if que_decir.startswith('"') or que_decir.startswith('\u201c'):
                parts.append(f'<p class="dialogo">💬 {esc(que_decir)}</p>')
            else:
                parts.append(f'<p class="instruccion">→ {esc(que_decir)}</p>')

        if notas:
            parts.append(f'<p class="nota">⚠️ {esc(notas)}</p>')

    if current_fase is not None:
        parts.append("</div>")

    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    creds = get_google_credentials(SCOPES)
    if not creds:
        print("ERROR: No valid Google credentials. Run setup_google_auth.py first.")
        sys.exit(1)

    print("Credentials OK. Building document...")

    rows = read_csv()
    html_content = build_html(rows)

    drive_service = build("drive", "v3", credentials=creds)

    # Upload HTML as Google Doc (Drive API converts it automatically)
    file_metadata = {
        "name": DOC_TITLE,
        "mimeType": "application/vnd.google-apps.document",
    }
    media = MediaInMemoryUpload(
        html_content.encode("utf-8"),
        mimetype="text/html",
        resumable=False,
    )

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,webViewLink",
    ).execute()

    doc_url = file.get("webViewLink", f"https://docs.google.com/document/d/{file['id']}/edit")
    print(f"\nGoogle Doc created successfully!")
    print(f"URL: {doc_url}")
    return doc_url


if __name__ == "__main__":
    main()
