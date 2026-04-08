#!/usr/bin/env python3
"""
Append rows to an existing Google Sheet.
Reads credentials from env vars (production) or local files (dev).
"""

import os
import sys
import json
import argparse
from dotenv import load_dotenv
import gspread

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def extract_sheet_id(url: str) -> str:
    if "/d/" in url:
        return url.split("/d/")[1].split("/")[0]
    return url


def append_row_direct(sheet_url: str, row_data: dict, worksheet_name: str | None = None) -> bool:
    """
    Append a single dict as a row to a Google Sheet.
    Callable directly from Python (not just CLI).

    Args:
        sheet_url: Google Sheets URL or ID
        row_data: Dict of {header: value} pairs
        worksheet_name: Specific worksheet name (default: first sheet)

    Returns:
        True on success, False on failure
    """
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from google_auth import get_google_credentials

        creds = get_google_credentials(SCOPES)
        if not creds:
            print("Error: No valid Google credentials.", file=sys.stderr)
            return False

        client = gspread.authorize(creds)
        sheet_id = extract_sheet_id(sheet_url)
        spreadsheet = client.open_by_key(sheet_id)

        worksheet = spreadsheet.worksheet(worksheet_name) if worksheet_name else spreadsheet.sheet1

        existing_headers = worksheet.row_values(1)
        if not existing_headers:
            print("Sheet has no headers.", file=sys.stderr)
            return False

        row = [row_data.get(h, "") for h in existing_headers]
        worksheet.append_row(row, value_input_option="RAW")
        return True

    except Exception as e:
        print(f"Error appending to sheet: {e}", file=sys.stderr)
        return False


def append_rows(sheet_url: str, json_file: str, worksheet_name: str | None = None) -> int:
    """Append rows from a JSON file to a Google Sheet. Returns count appended."""
    try:
        with open(json_file, "r") as f:
            data = json.load(f)

        if not data:
            print("No data in JSON file.")
            return 0

        count = 0
        for record in data:
            if append_row_direct(sheet_url, record, worksheet_name):
                count += 1
                print(f"Appended: {record.get('phone', record.get('ID', 'unknown'))}")

        print(f"Successfully appended {count} row(s).")
        return count

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 0


def main():
    parser = argparse.ArgumentParser(description="Append rows to a Google Sheet")
    parser.add_argument("--url", required=True, help="Google Sheets URL or ID")
    parser.add_argument("--json_file", required=True, help="Path to JSON file with rows to append")
    parser.add_argument("--worksheet", help="Worksheet name (default: first sheet)")
    args = parser.parse_args()

    result = append_rows(args.url, args.json_file, args.worksheet)
    return 0 if result > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
