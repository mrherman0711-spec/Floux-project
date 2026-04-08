#!/usr/bin/env python3
"""
One-time script to generate token.json with all required Google scopes.
Run this locally on your Mac — opens browser for OAuth consent.

Usage:
  python3 execution/setup_google_auth.py
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_PATH = BASE_DIR / "token.json"
CREDS_PATH = BASE_DIR / "credentials.json"


def main():
    creds = None

    if TOKEN_PATH.exists():
        with open(TOKEN_PATH) as f:
            creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS_PATH.exists():
                print(f"ERROR: credentials.json not found at {CREDS_PATH}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
        print(f"token.json saved to {TOKEN_PATH}")

    print("All scopes authorized:")
    for s in creds.scopes or SCOPES:
        print(f"  {s}")

    print("\nNext step: copy the contents of token.json into Railway env var GOOGLE_TOKEN_JSON")
    print(f"\ntoken.json contents:\n")
    with open(TOKEN_PATH) as f:
        print(f.read())


if __name__ == "__main__":
    main()
