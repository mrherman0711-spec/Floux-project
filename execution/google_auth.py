#!/usr/bin/env python3
"""
Google OAuth credentials helper.

Reads credentials and token from environment variables (production/Railway)
or from local files (development).

Environment variables:
  GOOGLE_CREDENTIALS_JSON  — contents of credentials.json
  GOOGLE_TOKEN_JSON        — contents of token.json
  RAILWAY_API_TOKEN        — Railway API token for persisting refreshed tokens
  RAILWAY_PROJECT_ID       — Railway project ID
  RAILWAY_SERVICE_ID       — Railway service ID
  RAILWAY_ENVIRONMENT_ID   — Railway environment ID (usually "production")
"""

import json
import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def _persist_token_to_railway(token_json: str) -> None:
    """Persist refreshed token back to Railway env var so it survives redeploys."""
    try:
        import urllib.request
        api_token = os.getenv("RAILWAY_API_TOKEN", "")
        project_id = os.getenv("RAILWAY_PROJECT_ID", "")
        environment_id = os.getenv("RAILWAY_ENVIRONMENT_ID", "")
        service_id = os.getenv("RAILWAY_SERVICE_ID", "")
        if not all([api_token, project_id, environment_id, service_id]):
            return  # not configured — skip silently

        mutation = """
        mutation variableUpsert($input: VariableUpsertInput!) {
          variableUpsert(input: $input)
        }
        """
        payload = json.dumps({
            "query": mutation,
            "variables": {
                "input": {
                    "projectId": project_id,
                    "environmentId": environment_id,
                    "serviceId": service_id,
                    "name": "GOOGLE_TOKEN_JSON",
                    "value": token_json,
                }
            }
        }).encode()

        req = urllib.request.Request(
            "https://backboard.railway.app/graphql/v2",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_token}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            if result.get("errors"):
                print(f"Warning: Railway token persist failed: {result['errors']}", flush=True)
            else:
                print("Google token persisted to Railway.", flush=True)
    except Exception as e:
        print(f"Warning: Could not persist token to Railway: {e}", flush=True)


def get_google_credentials(scopes: list[str] = None):  # noqa: ARG001 — kept for API compatibility
    """
    Return valid Google credentials, refreshing if expired.

    Priority:
    1. GOOGLE_TOKEN_JSON env var (Railway/production)
    2. token.json file (development)

    On successful refresh, persists the new token back to Railway
    so it survives the next redeploy without manual intervention.

    Returns None if no credentials available or refresh fails.
    """
    creds = None
    token_source = None  # "env" or "file"

    token_json = os.getenv("GOOGLE_TOKEN_JSON")
    if token_json:
        try:
            # Do NOT pass scopes — use whatever scopes are embedded in the token.
            # Passing explicit scopes causes invalid_scope errors when the token's
            # scopes don't exactly match the requested list.
            creds = Credentials.from_authorized_user_info(json.loads(token_json))
            token_source = "env"
        except Exception as e:
            print(f"Warning: Failed to load GOOGLE_TOKEN_JSON: {e}", flush=True)
            return None
    elif os.path.exists("token.json"):
        try:
            with open("token.json", "r") as f:
                creds = Credentials.from_authorized_user_info(json.load(f))
            token_source = "file"
        except Exception as e:
            print(f"Warning: Failed to load token.json: {e}", flush=True)
            return None

    if not creds:
        return None

    if creds.valid:
        return creds

    if not (creds.expired and creds.refresh_token):
        return None

    # Token expired — refresh it using client_id + client_secret from credentials.json
    try:
        creds_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if creds_json_str:
            creds_data = json.loads(creds_json_str)
            client_info = creds_data.get("installed") or creds_data.get("web", {})
            client_id = client_info.get("client_id", "")
            client_secret = client_info.get("client_secret", "")
            token_uri = client_info.get("token_uri", "https://oauth2.googleapis.com/token")

            # Rebuild without scopes argument — scopes come from the token itself
            creds = Credentials(
                token=creds.token,
                refresh_token=creds.refresh_token,
                token_uri=token_uri,
                client_id=client_id,
                client_secret=client_secret,
            )

        creds.refresh(Request())

        # Persist refreshed token so Railway has it on next deploy
        if token_source == "env":
            _persist_token_to_railway(creds.to_json())
        elif token_source == "file":
            try:
                with open("token.json", "w") as f:
                    f.write(creds.to_json())
            except Exception:
                pass

        return creds

    except Exception as e:
        print(f"Warning: Failed to refresh Google credentials: {e}", flush=True)
        return None
