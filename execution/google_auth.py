#!/usr/bin/env python3
"""
Google OAuth credentials helper.

Reads credentials and token from environment variables (production/Railway)
or from local files (development).

Environment variables:
  GOOGLE_CREDENTIALS_JSON  — contents of credentials.json
  GOOGLE_TOKEN_JSON        — contents of token.json
"""

import json
import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def get_google_credentials(scopes: list[str]) -> Credentials | None:
    """
    Return valid Google credentials, refreshing if expired.

    Priority:
    1. GOOGLE_TOKEN_JSON env var (Railway/production)
    2. token.json file (development)

    Returns None if no credentials available or refresh fails.
    """
    creds = None

    token_json = os.getenv("GOOGLE_TOKEN_JSON")
    if token_json:
        try:
            creds = Credentials.from_authorized_user_info(json.loads(token_json), scopes)
        except Exception as e:
            print(f"Warning: Failed to load GOOGLE_TOKEN_JSON: {e}", flush=True)
            return None
    elif os.path.exists("token.json"):
        try:
            with open("token.json", "r") as f:
                creds = Credentials.from_authorized_user_info(json.load(f), scopes)
        except Exception as e:
            print(f"Warning: Failed to load token.json: {e}", flush=True)
            return None

    if not creds:
        return None

    if creds.valid:
        return creds

    if not (creds.expired and creds.refresh_token):
        return None

    # Token expired — refresh it
    # For OAuth "installed" app credentials we need client_id + client_secret,
    # which live in credentials.json (not the token). Pass them explicitly.
    try:
        creds_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if creds_json_str:
            creds_data = json.loads(creds_json_str)
            # credentials.json has either "installed" or "web" key
            client_info = creds_data.get("installed") or creds_data.get("web", {})
            client_id = client_info.get("client_id", "")
            client_secret = client_info.get("client_secret", "")
            token_uri = client_info.get("token_uri", "https://oauth2.googleapis.com/token")

            # Rebuild credentials with client info so refresh works
            creds = Credentials(
                token=creds.token,
                refresh_token=creds.refresh_token,
                token_uri=token_uri,
                client_id=client_id,
                client_secret=client_secret,
                scopes=scopes,
            )

        creds.refresh(Request())
        return creds

    except Exception as e:
        print(f"Warning: Failed to refresh Google credentials: {e}", flush=True)
        return None
