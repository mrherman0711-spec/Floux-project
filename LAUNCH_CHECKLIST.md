# 🚀 Floux Launch Checklist
**Fecha:** 2026-04-19
**Objetivo:** Publicar Floux en producción segura y accesible

---

## FASE 1: Configuración Previa (Hoy — 30 min)

### ☐ 1.1 Registra Dominio
- [ ] Ve a Namecheap.com o GoDaddy
- [ ] Busca `floux.es` 
- [ ] Precio: ~€8.88/año
- [ ] Completa la compra
- [ ] Guarda usuario/contraseña

### ☐ 1.2 Implementa Seguridad en Bot
```bash
# En tu terminal:
cd /Users/maxherman/Desktop/Floux\ Project

# Instala dependencias de seguridad
pip install bleach slowapi

# Abre app/webhook.py y agrega (ver detalles en DEPLOYMENT_GUIDE.md):
# 1. import bleach + sanitize_input()
# 2. Limiter + slowapi
# 3. CORSMiddleware
# 4. Security headers middleware
```

**Duración:** ~30 min siguiendo DEPLOYMENT_GUIDE.md sección PARTE 5

### ☐ 1.3 Verifica .env
```bash
cat .env | grep -E "WEBHOOK_VERIFY_TOKEN|OPENAI_API_KEY|TWILIO"
# Debe salir:
# WEBHOOK_VERIFY_TOKEN=xxx
# OPENAI_API_KEY=xxx
# TWILIO_AUTH_TOKEN=xxx
```

---

## FASE 2: Deploy Website (1-2 horas)

### ☐ 2.1 Sube Website a Vercel
```bash
# Opción A: Via GitHub (recomendado)
cd /Users/maxherman/Desktop/Floux\ Project
git add .
git commit -m "website: ready for production"
git push origin main

# Ve a vercel.com/new → conecta tu repo
# Selecciona /Users/maxherman/Desktop/Floux Project
# Deploy automático

# Opción B: Via CLI
npm i -g vercel
vercel  # sigue prompts
```

**Resultado esperado:** URL como https://floux-website.vercel.app (temporal)

### ☐ 2.2 Configura DNS en Namecheap
1. Ve a tu cuenta Namecheap
2. Busca tu dominio `floux.es`
3. Haz clic en "Manage" → "DNS"
4. **Para Vercel:**
   - Tipo: CNAME
   - Host: @
   - Value: cname.vercel-dns.com.
   - TTL: 3600
5. **Para Railway (Bot API):**
   - Tipo: CNAME
   - Host: api
   - Value: proxy.railway.app (o la URL que Railway te da)
   - TTL: 3600
6. **Guarda cambios** y espera 15-60 min (DNS propagation)

### ☐ 2.3 Configura Dominio en Vercel
1. Ve a Vercel Dashboard → tu proyecto
2. Settings → Domains
3. Agregar dominio: `floux.es`
4. Vercel auto-configura SSL/HTTPS
5. Espera "Connected" status

**Verificar:**
```bash
# Después de 30 min
curl -I https://floux.es
# Debe salir HTTP/2 200, con headers de seguridad
```

---

## FASE 3: Deploy Bot API (30 min)

### ☐ 3.1 Push Cambios de Seguridad a Railway
```bash
# Asegúrate que webhook.py tiene:
# ✓ bleach + sanitize_input
# ✓ slowapi + rate limiting
# ✓ CORSMiddleware
# ✓ security headers

python -m py_compile app/webhook.py  # verifica sintaxis
git add app/webhook.py
git commit -m "security: add OWASP hardening (bleach, rate limiting, CORS)"
git push origin main
```

### ☐ 3.2 Configura Variables de Entorno en Railway
1. Ve a https://railway.app/p/[tu-proyecto]
2. Variables → añade o edita:
   ```
   WEBHOOK_VERIFY_TOKEN = [de tu Meta WhatsApp config]
   OPENAI_API_KEY = [tu API key de OpenAI]
   TWILIO_AUTH_TOKEN = [tu token de Twilio]
   TIMEZONE = Europe/Madrid
   FLOUX_DOMAIN = https://floux.es
   ```

### ☐ 3.3 Deploy en Railway
```bash
# Automático si está en GitHub
# O manual:
npm i -g @railway/cli
railway login
railway link  # selecciona tu proyecto
railway up
```

**Verificar:**
```bash
# Test que el webhook responde
curl -X POST https://floux.es/webhook \
  -H "Content-Type: application/json" \
  -d '{"object":"whatsapp_business_account"}' \
  -v
# Debe salir 200, no errores
```

---

## FASE 4: Configurar Webhooks en Meta & Twilio (30 min)

### ☐ 4.1 Meta WhatsApp Cloud API
1. Ve a developers.facebook.com → tu app WhatsApp
2. Settings → Webhook → Edit
3. **URL:** `https://floux.es/webhook` (NO railway.app)
4. **Verify Token:** [el mismo que en Railway WEBHOOK_VERIFY_TOKEN]
5. **Subscribe to messages:** ✓
6. Guarda

**Test:**
```bash
# Meta enviará un GET /webhook?hub.challenge=xxx
# Si tu bot responde correctamente, webhook estará verificado
```

### ☐ 4.2 Twilio Voice
1. Ve a console.twilio.com → tu número
2. Voice → Webhook URLs
3. **When a call comes in:** `https://floux.es/twilio/voice`
4. Guarda

---

## FASE 5: Verificación de Seguridad (1 hora)

### ☐ 5.1 Chequea Headers de Seguridad
```bash
curl -I https://floux.es
# Busca en response headers:
# ✓ Strict-Transport-Security: max-age=31536000
# ✓ X-Content-Type-Options: nosniff
# ✓ X-Frame-Options: DENY
# ✓ X-XSS-Protection: 1; mode=block
```

### ☐ 5.2 Prueba Rate Limiting
```bash
# Envía 101 requests en 1 minuto (debe devolver 429 en #101)
for i in {1..101}; do
  curl -X POST https://floux.es/webhook \
    -H "Content-Type: application/json" \
    -d '{"object":"whatsapp_business_account"}' \
    -w "%{http_code}\n" -o /dev/null -s
done
# Los primeros 100 = 200, el 101 = 429 (Too Many Requests)
```

### ☐ 5.3 Chequea SSL Certificate
```bash
curl https://floux.es -vI 2>&1 | grep "subject="
# Debe salir: subject=CN=floux.es (Vercel auto-genera)
```

### ☐ 5.4 Test Input Sanitization
```bash
# Envía un mensaje con HTML/JS — debe ser removido
# (interna: bleach.clean() lo maneja)
```

---

## FASE 6: SEO & Indexación (1-2 días)

### ☐ 6.1 Google Search Console
1. Ve a https://search.google.com/search-console
2. Click "Add property"
3. Dominio: `https://floux.es`
4. Verifica ownership (Vercel → DNS CNAME record)
5. Sitemaps → agregar: `https://floux.es/sitemap.xml`

### ☐ 6.2 Google Analytics 4
1. Ve a https://analytics.google.com
2. Create property → nombre "Floux"
3. Obtendrás measurement ID: `G-XXXXXX`
4. Agrega a index.html (en `<head>`):
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXX');
</script>
```
5. Deploy en Vercel

### ☐ 6.3 Valida Schema Markup
```bash
# Ve a https://validator.schema.org
# Pega el HTML de https://floux.es
# Verifica que Organization, SoftwareApplication, FAQPage validan sin errors
```

### ☐ 6.4 Test Lighthouse
```bash
# En Chrome DevTools (F12) → Lighthouse
# Genera report
# Objetivos: Performance 90+, Accessibility 95+, Best Practices 90+
```

---

## FASE 7: Testing Manual (1 hora)

### ☐ 7.1 Website Tests
- [ ] Página carga en < 3s
- [ ] Todas las secciones scrollean smooth
- [ ] Botones "VER DEMOSTRACIÓN" y "CÓMO FUNCIONA" funcionan
- [ ] FAQs accordion abre/cierra sin errores
- [ ] Formulario de contacto envía (ve a console, debe loguear JSON)
- [ ] Responsive en mobile (F12 → toggle device toolbar)

### ☐ 7.2 Bot Tests
- [ ] Envía mensaje por WhatsApp a tu número de prueba
- [ ] Bot responde en < 10s
- [ ] Conversación fluye (entiende service, datetime, name)
- [ ] Booking confirmation funciona
- [ ] Owner recibe notificación en WhatsApp

### ☐ 7.3 Security Tests
- [ ] No hay mensajes CORS en console
- [ ] No hay warnings de SSL/TLS
- [ ] Inspecciona Network requests → todas son HTTPS (verde)

---

## FASE 8: Monitoring Setup (30 min)

### ☐ 8.1 Uptime Monitoring
- [ ] Ve a https://www.betterstack.com (free tier)
- [ ] Create monitor: `https://floux.es`
- [ ] Frequency: 5 min
- [ ] Alerts: tu email

### ☐ 8.2 Error Tracking (Sentry)
- [ ] Ve a https://sentry.io (free tier)
- [ ] Create project → Python + FastAPI
- [ ] Copia DSN
- [ ] Agrega a app/webhook.py:
```python
import sentry_sdk
sentry_sdk.init("https://YOUR_DSN@sentry.io/PROJECT")
```
- [ ] Deploy

### ☐ 8.3 Database Backups
```bash
# Si usas SQLite local:
# Configura cron job para backup diario
# crontab -e
# 0 2 * * * cp /path/to/floux.db /backups/floux-$(date +\%Y\%m\%d).db
```

---

## FASE 9: Launch Announcement (Opcional)

### ☐ 9.1 Social Media
- [ ] LinkedIn post: "Floux is now live: recovering missed calls for Madrid salons"
- [ ] Email a tu lista de prospects (si tienes)
- [ ] Discord/Slack communities de startups españolas

### ☐ 9.2 Directory Listings
- [ ] Capterra.es: agregar Floux como "salon booking software"
- [ ] GetApp.es: mismo
- [ ] Product Hunt: opcional (requiere setup)

---

## FASE 10: Post-Launch Monitoring (Primeros 7 días)

### ☐ 10.1 Chequea Diarios
```bash
# Día 1-3: Cada 4h
# - ¿Floux.es carga?
# - ¿Logs de Railway tiene errores?
# - ¿Google Search Console muestra indexación?

# Día 4-7: Diarios
# - Google Analytics: ¿traffic?
# - Sentry: ¿errors?
# - Uptime monitors: ¿100%?
```

### ☐ 10.2 Iteración Rápida
- [ ] Si hay errores, pushea fix a GitHub → auto-deploy en Railway + Vercel
- [ ] Si hay feedback de UX, actualiza index.html
- [ ] Si conversations mejoran, ajusta prompts en ai_engine.py

---

## CHECKLIST FINAL: Go/No-Go Decision

**Antes de hacer público, verifica:**

| Check | Status | Notes |
|-------|--------|-------|
| Website en HTTPS | ✓ | Vercel auto-SSL |
| Bot con rate limiting | ✓ | slowapi 100/min |
| Input sanitization | ✓ | bleach.clean() |
| CORS restringido | ✓ | allow_origins=["floux.es"] |
| Security headers | ✓ | X-Frame-Options, etc. |
| .env no en git | ✓ | .gitignore contiene .env |
| Domain resuelve | ✓ | DNS propagated |
| Webhooks configurados | ✓ | Meta + Twilio apuntan a floux.es |
| Bot responde en <10s | ✓ | Test manual |
| No CORS errors | ✓ | Chrome DevTools console limpia |
| Lighthouse 90+ | ✓ | o al menos 85+ |
| Google Search Console verificado | ✓ | Sitemap enviado |

---

## 🎉 LISTO PARA LAUNCH

Una vez completados todos los items, **Floux es accesible públicamente en https://floux.es**

Siguiente fase: **Growth & Marketing**
- Outreach a salones en Madrid Oeste
- A/B testing de messaging
- Optimizaciones basadas en feedback

---

**Duración total estimada:** 4-6 horas (spread over 2 días si esperas DNS)
**Costo mes 1:** ~€6-8
**ROI:** 1 cliente recuperado (€60+) = 10x payback

¡A por ello! 🚀
