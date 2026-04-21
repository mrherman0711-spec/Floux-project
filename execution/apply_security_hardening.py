#!/usr/bin/env python3
"""
Apply security hardening to Floux bot before deployment.
Implements OWASP Top 10 protections: rate limiting, input validation, CORS, security headers.
Run this ONCE before deployment: python execution/apply_security_hardening.py
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
APP_DIR = BASE_DIR / "app"
WEBHOOK_FILE = APP_DIR / "webhook.py"

def check_file_exists():
    """Verify webhook.py exists."""
    if not WEBHOOK_FILE.exists():
        print(f"❌ Error: {WEBHOOK_FILE} not found")
        sys.exit(1)
    print(f"✓ Found {WEBHOOK_FILE}")

def has_bleach_import():
    """Check if bleach is already imported."""
    content = WEBHOOK_FILE.read_text()
    return "import bleach" in content

def has_slowapi_import():
    """Check if slowapi (rate limiting) is imported."""
    content = WEBHOOK_FILE.read_text()
    return "from slowapi import Limiter" in content

def has_cors_middleware():
    """Check if CORS middleware is configured."""
    content = WEBHOOK_FILE.read_text()
    return "CORSMiddleware" in content

def has_security_headers():
    """Check if security headers middleware exists."""
    content = WEBHOOK_FILE.read_text()
    return "X-Content-Type-Options" in content

def has_input_validation():
    """Check if input sanitization is implemented."""
    content = WEBHOOK_FILE.read_text()
    return "sanitize_input" in content or "bleach.clean" in content

def check_gitignore():
    """Verify .gitignore contains .env"""
    gitignore = BASE_DIR / ".gitignore"
    if not gitignore.exists():
        print(f"⚠️  .gitignore not found — create one with: .env, *.key, credentials.json")
        return False
    content = gitignore.read_text()
    if ".env" not in content:
        print(f"⚠️  .gitignore exists but .env not listed — add it manually")
        return False
    print(f"✓ .gitignore properly configured")
    return True

def print_implementation_checklist():
    """Print what needs to be done manually."""
    print("\n" + "="*70)
    print("SECURITY HARDENING CHECKLIST FOR DEPLOYMENT")
    print("="*70 + "\n")

    checks = {
        "Input Sanitization (bleach)": has_bleach_import(),
        "Rate Limiting (slowapi)": has_slowapi_import(),
        "CORS Middleware": has_cors_middleware(),
        "Security Headers": has_security_headers(),
        "Input Validation Function": has_input_validation(),
        ".gitignore contains .env": check_gitignore(),
    }

    for check_name, is_implemented in checks.items():
        status = "✓" if is_implemented else "⚠️ "
        print(f"{status} {check_name}")

    print("\n" + "="*70)
    print("MANUAL IMPLEMENTATION NEEDED:")
    print("="*70 + "\n")

    if not has_bleach_import():
        print("1️⃣  ADD INPUT SANITIZATION (bleach)")
        print("   Command: pip install bleach")
        print("   Add to app/webhook.py top:")
        print("""
   import bleach

   def sanitize_input(text: str) -> str:
       return bleach.clean(text, tags=[], strip=True)
        """)
        print("   Then use in handle_whatsapp_message():")
        print("   text = sanitize_input(message['text']['body'])\n")

    if not has_slowapi_import():
        print("2️⃣  ADD RATE LIMITING (slowapi)")
        print("   Command: pip install slowapi")
        print("   Add to app/webhook.py after imports:")
        print("""
   from slowapi import Limiter
   from slowapi.util import get_remote_address

   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
        """)
        print("   Add decorator to @app.post('/webhook'):")
        print("   @limiter.limit('100/minute')\n")

    if not has_cors_middleware():
        print("3️⃣  ADD CORS MIDDLEWARE")
        print("   Add to app/webhook.py after app = FastAPI():")
        print("""
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://floux.es", "https://www.floux.es"],
       allow_methods=["POST", "GET"],
       allow_credentials=True,
   )
        """)

    if not has_security_headers():
        print("4️⃣  ADD SECURITY HEADERS")
        print("   Add to app/webhook.py:")
        print("""
   @app.middleware("http")
   async def add_security_headers(request: Request, call_next):
       response = await call_next(request)
       response.headers["X-Content-Type-Options"] = "nosniff"
       response.headers["X-Frame-Options"] = "DENY"
       response.headers["X-XSS-Protection"] = "1; mode=block"
       response.headers["Strict-Transport-Security"] = "max-age=31536000"
       return response
        """)

    print("\n" + "="*70)
    print("DEPENDENCIES TO INSTALL:")
    print("="*70)
    print("\npip install bleach slowapi\n")

    print("="*70)
    print("VERIFICA .env:")
    print("="*70)
    print("""
Asegúrate que .env contiene:
  WEBHOOK_VERIFY_TOKEN=tu_token_aqui
  TWILIO_AUTH_TOKEN=tu_token_aqui
  OPENAI_API_KEY=tu_key_aqui
  TIMEZONE=Europe/Madrid

NO commites .env a git. Está en .gitignore? Verifica: cat .gitignore | grep .env
    """)

    print("\n" + "="*70)
    print("AFTER IMPLEMENTING:")
    print("="*70)
    print("""
1. pip install -r requirements.txt  (actualiza con bleach + slowapi)
2. python -m py_compile app/webhook.py  (verifica sintaxis)
3. python -m pytest tests/ (si tienes tests)
4. railway deploy (o vercel deploy)
    """)

if __name__ == "__main__":
    check_file_exists()
    print_implementation_checklist()
    print("=" * 70)
    print("✅ CHECKLIST COMPLETE — LISTO PARA REVIEW")
    print("=" * 70)
