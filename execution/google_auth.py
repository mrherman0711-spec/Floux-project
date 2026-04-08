#!/usr/bin/env python3
"""
Google OAuth credentials helper.

Reads credentials and token from environment variables (production/Railway)
or from local files (development). Falls back gracefully.

Environment variables:
  GOOGLE_CREDENTIALS_JSON  — contents of credentials.json
  GOOGLE_TOKEN_JSON        — contents of token.json
"""

import json
import os
import tempfile

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def get_google_credentials(scopes: list[str]) -> Credentials | None:
    """
    Return valid Google credentials, refreshing if expired.

    Priority:
    1. GOOGLE_TOKEN_JSON env var (production)
    2. token.json file (development)

    Returns None if no credentials are available or refresh fails.
    """
    creds = None

    # Try env var first (Railway), then local file (dev)
    token_json = os.getenv("GOOGLE_TOKEN_JSON")
    if token_json:
        try:
            creds = Credentials.from_authorized_user_info(json.loads(token_json), scopes)
        except Exception as e:
            print(f"Warning: Failed to load GOOGLE_TOKEN_JSON: {e}", flush=True)
    elif os.path.exists("token.json"):
        with open("token.json", "r") as f:
            creds = Credentials.from_authorized_user_info(json.load(f), scopes)

    if not creds:
        return None

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            # Need credentials.json to refresh — try env var then file
            creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            if creds_json:
                # Write to a temp file so the Google client library can read it
                with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
                    tmp.write(creds_json)
                    tmp_path = tmp.name
                try:
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tmp_path
                    creds.refresh(Request())
                finally:
                    os.unlink(tmp_path)
            elif os.path.exists("credentials.json"):
                creds.refresh(Request())
            else:
                return None
        else:
            return None

    return creds
