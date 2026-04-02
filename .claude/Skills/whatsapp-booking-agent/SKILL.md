---
name: whatsapp-booking-agent
description: "Designs WhatsApp conversation flows for Floux salon clients. Use when writing WhatsApp message templates, creating conversation scripts, handling edge cases (voice notes, angry clients, unknown services, after-hours, English-speaking clients), building dialogue for any salon client, or designing the user experience of the booking agent."
allowed-tools:
  - Bash
  - Write
  - Read
---

# Floux WhatsApp Booking Agent

## Language Rules

The AI auto-detects language from the client's FIRST reply and responds in that language for the entire conversation.
- Default: Spanish (castellano)
- Switch to English if client's first reply is in English
- Mixed language (Spanglish): follow whichever language dominates the first message
- NEVER switch language mid-conversation unless client explicitly asks

## Message Templates

### missed_call_recovery — Spanish (sent within 30 seconds of missed call)
```
¡Hola! Hemos visto que nos has llamado a {SALON_NAME} y no hemos podido atenderte. 😊

¿En qué podemos ayudarte? Si quieres reservar una cita, dime qué servicio te interesa y cuándo te vendría bien.
```

### missed_call_recovery — English
```
Hi! We saw you called {SALON_NAME} and we couldn't pick up. 😊

How can we help? If you'd like to book an appointment, just let me know which service you're interested in and when works for you.
```

### appointment_reminder — Spanish (24h before — V2 feature)
```
¡Hola {CLIENT_NAME}! Te recordamos que mañana tienes cita en {SALON_NAME}:

📋 {SERVICE}
🕐 {TIME}

Si necesitas cambiar o cancelar, avísanos. ¡Te esperamos!
```

### review_request — Spanish (2h after appointment — V2 feature)
```
¡Hola {CLIENT_NAME}! Esperamos que hayas disfrutado de tu visita a {SALON_NAME}. 😊

¿Nos dejarías una reseña? Nos ayuda muchísimo:
{GOOGLE_REVIEW_LINK}

¡Gracias y hasta pronto!
```

## Conversation Flow — Happy Path (Spanish)

```
1. Sistema: [missed_call_recovery message]
2. Cliente: "Hola, quiero una cita para mechas el viernes"
3. AI: "¡Genial! ¿Tienes preferencia de hora para el viernes? Tenemos mañana y tarde disponible."
4. Cliente: "Por la tarde mejor"
5. AI: "Perfecto. ¿Me dices tu nombre para apuntar la cita?"
6. Cliente: "Ana García"
7. AI: "¡Perfecto! Te confirmo tu cita:
   📋 Servicio: Mechas
   📅 Fecha: viernes 11 de abril
   🕐 Hora: 16:30
   💇 Con: Laura
   Si necesitas cambiar algo, escríbeme. ¡Te esperamos! 😊"
```

## Conversation Flow — Happy Path (English)

```
1. System: [missed_call_recovery English message]
2. Client: "Hi, I'd like an appointment for a manicure on Friday"
3. AI: "Great! Do you have a time preference on Friday? We have morning and afternoon slots."
4. Client: "Afternoon please"
5. AI: "Perfect. Could I get your name to book the appointment?"
6. Client: "Sarah"
7. AI: "All set! Here's your appointment confirmation:
   📋 Service: Manicure
   📅 Date: Friday 11 April
   🕐 Time: 16:30
   💅 With: Laura
   If you need to change anything, just message me. See you then! 😊"
```

## Edge Case Responses

### Voice note received
```
ES: Disculpa, no puedo escuchar audios. ¿Me lo puedes escribir? 😊
EN: Sorry, I can't listen to voice notes. Could you write it instead? 😊
```

### "¿Eres un robot?" / "Are you a bot?"
```
ES: Soy el asistente de reservas de {SALON_NAME}. ¿En qué puedo ayudarte? 😊
EN: I'm the booking assistant for {SALON_NAME}. How can I help? 😊
```

### Service not in catalog
```
ES: Ese servicio no lo tengo en mi lista. Déjame consultarlo con {OWNER_NAME} y te respondo enseguida.
EN: I don't have that service in my list. Let me check with {OWNER_NAME} and get back to you.
```
→ Trigger: escalate=true, notify owner

### Client is angry / complaining
```
ES: Entendido, siento mucho lo ocurrido. Paso tu mensaje a {OWNER_NAME} ahora mismo para que te ayude personalmente.
EN: Understood, I'm really sorry about that. I'm passing your message to {OWNER_NAME} right now so they can help you directly.
```
→ Trigger: escalate=true, send full context to owner

### After hours
```
ES: ¡Hola! Ahora mismo estamos fuera de horario. Nuestro horario es {SCHEDULE}. Dime qué necesitas y te respondo en cuanto abramos. 😊
EN: Hi! We're currently outside our opening hours. Our schedule is {SCHEDULE}. Let me know what you need and we'll get back to you when we open. 😊
```

### Client sends only "Hola" / "Hi"
```
ES: ¡Hola! 😊 ¿Quieres reservar una cita o tienes alguna consulta? Estoy aquí para ayudarte.
EN: Hi! 😊 Would you like to book an appointment or do you have a question? I'm here to help.
```

### Client asks price without booking intent
```
ES: {SERVICE} tiene un precio de {PRICE}. ¿Te gustaría reservar una cita? 😊
EN: {SERVICE} is {PRICE}. Would you like to book an appointment? 😊
```

## Phone Number Normalization

Spanish numbers must be in E.164 format for Twilio:
```javascript
const raw = from || body.From;
const cleaned = raw.replace(/[\s\-\(\)]/g, '');
const normalized = cleaned.startsWith('+') ? cleaned
  : cleaned.startsWith('34') ? '+' + cleaned
  : '+34' + cleaned;
// Result: +34XXXXXXXXX
```

## 24-Hour Session Window Rule

WhatsApp Business API only allows free-form messages within 24 hours of the customer's last message. After 24h:
- Can ONLY send pre-approved template messages
- Templates must be submitted to Meta for approval (24-48h)
- For V1: if session expires, re-send missed_call_recovery template to re-engage

## Owner Notification Format

When booking is complete or escalation triggered:
```
📱 NUEVA CITA / ESCALACIÓN

Cliente: {client_name}
Teléfono: {phone}
Servicio: {service}
Fecha/hora: {datetime}
Personal: {staff}
Estado: {booked | escalated}
Motivo (si escalado): {reason}
```

## Production Testing Checklist

Before going live with a new salon client:
- [ ] Missed call triggers WhatsApp within 30 seconds
- [ ] AI responds correctly to greeting in Spanish
- [ ] AI responds in English when client writes in English
- [ ] Client mixing languages gets consistent response
- [ ] AI collects service + datetime + name
- [ ] AI confirms booking with emoji format
- [ ] Voice note gets text-only response
- [ ] "Eres un robot" / "Are you a bot" gets deflection response
- [ ] Unknown service triggers escalation to owner
- [ ] Angry message triggers escalation with full context
- [ ] Owner receives notification with all booking data
- [ ] Duplicate calls (same CallSid) are filtered
