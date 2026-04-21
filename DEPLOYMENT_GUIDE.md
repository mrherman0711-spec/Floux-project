# Floux — Deployment Guide (Producción Segura)
**Fecha:** 2026-04-19
**Objetivo:** Publicar el website + bot en producción accesible globalmente y seguro

---

## PARTE 1: Infraestructura & Hosting

### Opción A: Railway (Recomendado para Max — ya lo usas)
Railway ya hospeda el bot. Ahora necesitas:

1. **Agregar Static Files (Website)**
   - El `index.html` + `sitemap.xml` + `robots.txt` van en un servicio separate de Railway
   - O bien en un CDN como Vercel/Netlify (más rápido, más barato)

2. **Dominio Personalizado**
   - Registra `floux.es` en Namecheap, GoDaddy, o similiar
   - Costo: ~€8-15/año
   - Apunta DNS a Railway o Vercel (según donde hospedes)

### Opción B: Vercel + Railway (Recomendado — mejor performance)
- **Website (HTML)**: Vercel (CDN global, gratuito tier suficiente)
- **Bot API**: Railway (ya está ahí)
- **Dominio**: Cualquier registrador, apunta a ambos servicios

---

## PARTE 2: Configuración de DNS & HTTPS

### Paso 1: Registra el Dominio
```bash
# Ej: floux.es en Namecheap
# Precio: €8.88/año aprox
```

### Paso 2: SSL/TLS (Encriptación)
- **Vercel**: Ofrece SSL automático (Let's Encrypt) — GRATIS
- **Railway**: Ofrece SSL automático — GRATIS
- **No necesitas hacer nada** — ambos configuran HTTPS automáticamente

### Paso 3: Apunta DNS
```
Tu registrador (Namecheap) → DNS Settings
A Record: apunta a IP de Vercel o Railway
CNAME: apunta a dominio de Railway si es necesario

Vercel:
  Type: CNAME
  Name: @
  Value: cname.vercel-dns.com

Railway:
  Type: CNAME
  Name: *
  Value: proxy.railway.app
```

---

## PARTE 3: Seguridad Web (OWASP Top 10)

### 1. Protege contra inyección SQL
**Estado:** ✓ Ya seguro
- Tu código usa SQLite con parámetros (no concatenación de strings)
- Verifica en `app/database.py` que usa `?` placeholders, no f-strings

### 2. Protege contra XSS (Cross-Site Scripting)
**Estado:** ⚠️ Requiere validación en webhook
```python
# En app/webhook.py, antes de procesar mensaje:
import bleach

def sanitize_input(text):
    """Remove HTML/JS from user messages"""
    return bleach.clean(text, tags=[], strip=True)

# Úsalo en handle_whatsapp_message():
text = sanitize_input(message["text"]["body"])
```

### 3. Protege contra CSRF (Cross-Site Request Forgery)
**Estado:** ✓ Ya seguro
- Tu webhook usa token de verificación (`WEBHOOK_VERIFY_TOKEN`)
- FastAPI no requiere CSRF porque es API, no formularios tradicionales

### 4. Rate Limiting (prevenir abuso)
**Estado:** ⚠️ Implementar
```python
# Instala: pip install slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.post("/webhook")
@limiter.limit("100/minute")  # 100 requests/min por IP
async def meta_webhook(request: Request):
    ...
```

### 5. Secrets Management (API Keys seguros)
**Estado:** ✓ Parcialmente seguro
- ✓ Variables de entorno (.env) — BIEN
- ⚠️ `.env` debe estar en `.gitignore` — VERIFICA
- ✓ Railway usa secrets automáticamente

**En `.gitignore`, asegúrate que incluya:**
```
.env
.env.local
*.key
*.pem
credentials.json
```

### 6. Validación de Entrada
**Estado:** ⚠️ Mejorar
```python
# En app/phone.py
import re

def validate_phone(phone: str) -> bool:
    """Validar formato E.164 estricto"""
    pattern = r'^\+34\d{9}$'  # Solo España
    return bool(re.match(pattern, phone))

# En webhook:
if not validate_phone(phone):
    log.warning(f"Invalid phone format: {phone}")
    return Response(status_code=400)
```

### 7. Headers de Seguridad HTTP
**Estado:** ⚠️ Agregar a FastAPI
```python
# En app/webhook.py, después de app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Limitar CORS solo a dominios Floux
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://floux.es", "https://www.floux.es"],
    allow_methods=["POST", "GET"],
    allow_credentials=True,
)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["floux.es", "*.floux.es", "localhost"]
)

# Headers de seguridad
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### 8. Logging & Monitoreo
**Estado:** ✓ Básico (mejorable)
```python
# Ya tienes logging — asegúrate de NO loguear secrets
# NUNCA hagas: log.info(f"API KEY: {api_key}")

# En su lugar:
log.info(f"API call successful (key: {api_key[:4]}...)")
```

---

## PARTE 4: Pasos de Deployment

### Opción 1: Vercel (Para Website) + Railway (Para Bot)

#### 4.1 Sube website a Vercel
```bash
# 1. Crea cuenta en vercel.com
# 2. Conecta tu repo GitHub (o crea uno nuevo)

# Si no tienes repo, crear uno:
cd /Users/maxherman/Desktop/Floux\ Project
git init
git add index.html sitemap.xml robots.txt
git commit -m "Initial website deployment"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/floux-website.git
git push -u origin main

# 3. En Vercel UI:
#    - Conecta tu repo
#    - Deploy automático en cada push
#    - Configura dominio personalizado (floux.es)

# 4. Vercel configura HTTPS automáticamente
```

#### 4.2 Configura Railway para Bot API
```bash
# 1. Ya tienes el bot en Railway
# 2. Agrega variables de entorno en Railway Dashboard:
#    - WEBHOOK_VERIFY_TOKEN (Meta WhatsApp)
#    - TWILIO_AUTH_TOKEN
#    - OPENAI_API_KEY
#    - DATABASE_URL (si usas Postgres, sino SQLite local)
#    - TIMEZONE = "Europe/Madrid"

# 3. Obtén la URL pública de Railway:
#    railway.app/p/[project-id]
#    Algo como: https://floux-bot.railway.app

# 4. Configura webhooks en Meta/Twilio:
#    - Meta WhatsApp: https://floux.es/webhook (NO usar railway.app directamente)
#    - Twilio: https://floux.es/twilio/voice
```

#### 4.3 Apunta DNS
```
En tu registrador (Namecheap, etc.):

Para Vercel (website):
  Type: CNAME
  Name: @
  Value: cname.vercel-dns.com

Para Railway (bot):
  Type: CNAME
  Name: api
  Value: proxy.railway.app (o la URL específica que Railway te da)

Espera 24-48h para propagación DNS
```

---

## PARTE 5: Verificación Pre-Launch

### Checklist de Seguridad
- [ ] SSL/TLS activo (https://, no http://)
- [ ] WEBHOOK_VERIFY_TOKEN configurado en Meta/Twilio
- [ ] Rate limiting implementado
- [ ] Input validation en webhook
- [ ] CORS restringido solo a floux.es
- [ ] .env NO está en git (check .gitignore)
- [ ] Secrets en Railway, NO en código
- [ ] Logging NO contiene API keys/passwords
- [ ] Headers de seguridad agregados (X-Frame-Options, etc.)

### Checklist de Performance
- [ ] Lighthouse score 90+ (test en Chrome DevTools)
- [ ] Core Web Vitals: LCP <2.5s, INP <200ms, CLS <0.1
- [ ] Sitemap + robots.txt presentes
- [ ] Schema markup valida (test.schema.org)
- [ ] Imágenes optimizadas (WebP con fallback)
- [ ] Minify CSS/JS (opcional en Vercel, automático)

### Checklist de SEO
- [ ] Meta tags correctos
- [ ] Canonical URL set
- [ ] Open Graph tags
- [ ] H1 keyword-rich
- [ ] FAQPage schema valida
- [ ] Organization schema con areaServed

### Test Manual
```bash
# 1. Abre https://floux.es en navegador
# 2. Verifica que todo carga sin errores
# 3. Prueba los botones (mailto, demo booking)
# 4. Abre DevTools > Network y chequea:
#    - Todos los requests 200-300 status
#    - No hay CORS errors
#    - HTTPS en todos
# 5. Envía un WhatsApp a tu número de prueba
# 6. Verifica que el bot responde
```

---

## PARTE 6: Post-Launch Monitoring

### Herramientas Gratuitas
1. **Google Search Console** (https://search.google.com/search-console)
   - Verifica ownership del dominio
   - Envía sitemap.xml
   - Monitorea errors de indexación
   - Costo: GRATIS

2. **Google Analytics 4** (https://analytics.google.com)
   - Trackea visitas, comportamiento de usuarios
   - Costo: GRATIS (hasta 10M eventos/mes)
   ```html
   <!-- Agrega esto en <head> del index.html -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR-ID"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-YOUR-ID');
   </script>
   ```

3. **Sentry** (https://sentry.io)
   - Monitorea errores del bot en tiempo real
   - Costo: GRATIS tier (1 project, 5K errors/mes)
   ```python
   # En app/webhook.py (optional but recommended)
   import sentry_sdk
   sentry_sdk.init("https://YOUR_SENTRY_DSN@sentry.io/YOUR-PROJECT-ID")
   ```

4. **Uptime Monitoring**
   - Betterstack.com o similar
   - Te avisa si el sitio cae
   - Costo: GRATIS tier

---

## PARTE 7: Backup & Disaster Recovery

### Backup de Base de Datos
```bash
# SQLite local backup (cada día)
cp /path/to/floux.db /path/to/backups/floux-$(date +%Y%m%d).db

# O usar Railway: auto-backups incluidos
```

### Backup de Código
```bash
# Git remote (ya en GitHub)
git push origin main  # siempre

# Importa a GitHub si no está:
gh repo create floux-website --private
git push -u origin main
```

---

## PARTE 8: Costos Estimados (Mes 1)

| Servicio | Coste | Notas |
|----------|-------|-------|
| Dominio (floux.es) | €0.74/mes | ~€8.88/año, registrador |
| Vercel (website) | €0 | Gratuito tier suficiente |
| Railway (bot) | €5 | Starter tier, app.py siempre corriendo |
| Meta WhatsApp | €0 | Conversations tier, pagas por mensajes |
| OpenAI GPT-4o-mini | $0.15/1K in, $0.60/1K out | ~€0.50-1 por 100 chats |
| **TOTAL** | **~€6-8/mes** | Productivo, escalable |

---

## PARTE 9: Comandos Finales para Deploy

### Vercel Deploy (si usas CLI)
```bash
# 1. Instala Vercel CLI
npm install -g vercel

# 2. En folder del proyecto
cd /Users/maxherman/Desktop/Floux\ Project
vercel

# 3. Sigue prompts
# 4. Asigna dominio floux.es
```

### Railway Deploy (bot ya está, pero si necesitas re-deploy)
```bash
# Instala Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link a tu proyecto
railway link

# Deploy
railway up
```

---

## PARTE 10: Troubleshooting Post-Launch

| Problema | Solución |
|----------|----------|
| "Domain not found" (DNS) | Espera 24-48h, chequea DNS propagation en mxtoolbox.com |
| "SSL certificate pending" | Vercel/Railway auto-emite en 15 min. Recarga en 10 min |
| "Bot no responde" | Chequea que webhook URL apunta a floux.es, no railway.app |
| "Lighthouse score bajo" | Comprime imágenes (tinypng.com), minify CSS |
| "404 en sitemap.xml" | Verifica que sitemap.xml está en raíz, no en carpeta |
| "CORS errors en console" | Chequea CORSMiddleware allow_origins, agregar floux.es |

---

## RESUMEN: Timeline de Deployment

```
Día 1:
  ✓ Registra dominio floux.es (~5 min)
  ✓ Sube website a Vercel (~10 min)
  ✓ Configura DNS (~5 min)
  ✓ Implementa rate limiting + security headers (~30 min)

Día 2:
  ✓ Espera DNS propagación (automático, 24-48h)
  ✓ Test manual de website + bot
  ✓ Setup Google Search Console (~10 min)
  ✓ Setup Google Analytics (~5 min)

Día 3:
  ✓ Verifica que floux.es es accesible públicamente
  ✓ Checkea Lighthouse score
  ✓ Monitorea primeros errores con Sentry
  ✓ LAUNCH! 🚀
```

---

## Support & Resources

- **Vercel Docs:** vercel.com/docs
- **Railway Docs:** railway.app/docs
- **FastAPI Security:** fastapi.tiangolo.com/advanced/security
- **OWASP Top 10:** owasp.org/www-project-top-ten
- **Google Search Console Help:** support.google.com/webmasters
- **SSL/TLS Testing:** ssllabs.com/ssltest

---

**Preguntas?** Contacta a flouxaim@gmail.com o abre issue en GitHub.
¡Listo para ir a producción! 🎉
