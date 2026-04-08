"""
Floux — AI-powered salon management via WhatsApp.
Entry point: starts the webhook server + scheduler.

Usage:
  python main.py                     # Production (port 8000)
  python main.py --port 3000         # Custom port
  python main.py --dev               # Dev mode with auto-reload
"""

import argparse
import logging
import os
import uvicorn

from app.webhook import app
from app.scheduler import setup_scheduler
from app.database import init_db

log = logging.getLogger("floux")


@app.on_event("startup")
async def on_startup():
    init_db()
    setup_scheduler()
    log.info("Floux is live")


def main():
    parser = argparse.ArgumentParser(description="Floux webhook server")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8000)), help="Port (default: $PORT or 8000)")
    parser.add_argument("--host", default="0.0.0.0", help="Host (default: 0.0.0.0)")
    parser.add_argument("--dev", action="store_true", help="Development mode with auto-reload")
    args = parser.parse_args()

    uvicorn.run(
        "main:app" if args.dev else app,
        host=args.host,
        port=args.port,
        reload=args.dev,
        log_level="info",
    )


if __name__ == "__main__":
    main()
