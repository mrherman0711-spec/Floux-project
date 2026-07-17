import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const DARK = "#1A1714";
const DARKER = "#0E0C0A";
const CREAM = "#F2EDE6";
const LIGHT = "#DED8D0";
const GOLD = "#9A7B4F";
const BODY = "#AAA29A";
const GREEN = "#86B88B";
const RED = "#B86D61";

const clamp = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

const ease = Easing.bezier(0.16, 1, 0.3, 1);

const fadeIn = (frame: number, start: number, duration = 24) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    ...clamp,
    easing: ease,
  });

const rise = (frame: number, start: number, amount = 26, duration = 30) =>
  interpolate(frame, [start, start + duration], [amount, 0], {
    ...clamp,
    easing: ease,
  });

const pct = (frame: number, start: number, duration: number) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    ...clamp,
    easing: ease,
  });

const titleFont =
  '"Cormorant Garamond", "Times New Roman", Georgia, serif';

const SceneWrap: React.FC<{
  children: React.ReactNode;
  localFrame: number;
}> = ({ children, localFrame }) => {
  const intro = fadeIn(localFrame, 0, 18);
  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 18% 20%, rgba(154,123,79,0.20), transparent 32%), radial-gradient(circle at 84% 12%, rgba(242,237,230,0.08), transparent 28%), linear-gradient(135deg, #1A1714 0%, #11100E 55%, #0E0C0A 100%)",
        color: CREAM,
        opacity: intro,
        overflow: "hidden",
      }}
    >
      <Grid localFrame={localFrame} />
      <div
        style={{
          position: "absolute",
          inset: 42,
          border: "1px solid rgba(154,123,79,0.24)",
        }}
      />
      {children}
    </AbsoluteFill>
  );
};

const Grid: React.FC<{ localFrame: number }> = ({ localFrame }) => {
  const drift = interpolate(localFrame, [0, 240], [0, 32], clamp);
  return (
    <>
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: 0.16,
          backgroundImage:
            "linear-gradient(rgba(242,237,230,0.10) 1px, transparent 1px), linear-gradient(90deg, rgba(242,237,230,0.10) 1px, transparent 1px)",
          backgroundSize: "64px 64px",
          transform: `translate(${drift}px, ${drift * 0.5}px)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(90deg, rgba(26,23,20,0.94), rgba(26,23,20,0.35), rgba(26,23,20,0.92))",
        }}
      />
    </>
  );
};

const Eyebrow: React.FC<{ children: React.ReactNode; frame: number; delay?: number }> = ({
  children,
  frame,
  delay = 0,
}) => (
  <div
    style={{
      opacity: fadeIn(frame, delay),
      transform: `translateY(${rise(frame, delay, 14)}px)`,
      color: GOLD,
      fontSize: 13,
      letterSpacing: "0.26em",
      textTransform: "uppercase",
      fontWeight: 600,
    }}
  >
    {children}
  </div>
);

const SceneTitle: React.FC<{
  children: React.ReactNode;
  frame: number;
  delay?: number;
  width?: number;
}> = ({ children, frame, delay = 8, width = 700 }) => (
  <div
    style={{
      width,
      opacity: fadeIn(frame, delay),
      transform: `translateY(${rise(frame, delay, 30)}px)`,
      fontFamily: titleFont,
      fontSize: 58,
      lineHeight: 0.96,
      fontWeight: 300,
      marginTop: 20,
    }}
  >
    {children}
  </div>
);

const TextLine: React.FC<{
  children: React.ReactNode;
  frame: number;
  delay?: number;
  width?: number;
}> = ({ children, frame, delay = 20, width = 520 }) => (
  <div
    style={{
      width,
      opacity: fadeIn(frame, delay),
      transform: `translateY(${rise(frame, delay, 22)}px)`,
      color: LIGHT,
      fontSize: 23,
      lineHeight: 1.42,
      marginTop: 28,
      fontWeight: 300,
    }}
  >
    {children}
  </div>
);

const FlouxLogo: React.FC<{ size?: number; animatedFrame?: number }> = ({
  size = 96,
  animatedFrame = 999,
}) => {
  const line = (delay: number) => pct(animatedFrame, delay, 22);
  const drawLine = (progress: number) => ({
    strokeDasharray: 60,
    strokeDashoffset: 60 - 60 * progress,
  });

  return (
    <svg width={size} height={size} viewBox="0 0 100 100">
      <ellipse cx="50" cy="17" rx="6" ry="9" fill="#9A9A9A" opacity="0.75" />
      {[32, 47, 62].map((y, i) => (
        <polyline
          key={y}
          points={`30,${y} 50,${y + 14} 70,${y}`}
          fill="none"
          stroke={GOLD}
          strokeWidth="7"
          strokeLinecap="round"
          strokeLinejoin="round"
          style={drawLine(line(i * 8))}
        />
      ))}
    </svg>
  );
};

const IconPhone: React.FC<{ color?: string }> = ({ color = GOLD }) => (
  <svg width="34" height="34" viewBox="0 0 34 34" fill="none">
    <path
      d="M11 6.5c1.4 7.1 4.7 12.4 11.8 16.4l3.8-3.1 4.3 2.5c.8.5 1.2 1.5.9 2.4-1 3.1-3.2 4.8-6.2 4.8C13.1 29.5 4.5 20.2 4.5 8.9c0-2.9 1.6-5.1 4.6-6 .9-.3 1.9.1 2.4.9L14 8l-3 3.5Z"
      stroke={color}
      strokeWidth="2.2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const IconMessage: React.FC<{ color?: string }> = ({ color = GOLD }) => (
  <svg width="34" height="34" viewBox="0 0 34 34" fill="none">
    <path
      d="M6 8.5c0-1.7 1.3-3 3-3h16c1.7 0 3 1.3 3 3v10.8c0 1.7-1.3 3-3 3h-9.1l-7 5v-5H9c-1.7 0-3-1.3-3-3V8.5Z"
      stroke={color}
      strokeWidth="2.2"
      strokeLinejoin="round"
    />
    <path d="M11 12h12M11 17h8" stroke={color} strokeWidth="2.2" strokeLinecap="round" />
  </svg>
);

const IconCalendar: React.FC<{ color?: string }> = ({ color = GOLD }) => (
  <svg width="34" height="34" viewBox="0 0 34 34" fill="none">
    <rect x="5.5" y="7.5" width="23" height="21" rx="3" stroke={color} strokeWidth="2.2" />
    <path d="M10 5v5M24 5v5M6 14h22" stroke={color} strokeWidth="2.2" strokeLinecap="round" />
    <path d="m12 22 3 3 7-8" stroke={GREEN} strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const Pill: React.FC<{
  children: React.ReactNode;
  frame: number;
  delay: number;
  left: number;
  top: number;
  icon?: React.ReactNode;
}> = ({ children, frame, delay, left, top, icon }) => (
  <div
    style={{
      position: "absolute",
      left,
      top,
      height: 54,
      display: "flex",
      alignItems: "center",
      gap: 13,
      padding: "0 20px",
      color: CREAM,
      border: "1px solid rgba(154,123,79,0.42)",
      background: "rgba(14,12,10,0.82)",
      boxShadow: "0 24px 70px rgba(0,0,0,0.32)",
      opacity: fadeIn(frame, delay, 18),
      transform: `translateY(${rise(frame, delay, 20)}px)`,
      fontSize: 17,
    }}
  >
    {icon}
    {children}
  </div>
);

const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const sweep = interpolate(frame, [35, 135], [-380, 1350], clamp);
  return (
    <SceneWrap localFrame={frame}>
      <div style={{ position: "absolute", left: 86, top: 94 }}>
        <Eyebrow frame={frame}>Video para salones</Eyebrow>
        <SceneTitle frame={frame} width={780}>
          De llamada perdida a cita confirmada.
        </SceneTitle>
        <TextLine frame={frame} width={610}>
          Floux enseña al cliente que el salón responde por WhatsApp mientras el equipo sigue atendiendo.
        </TextLine>
      </div>

      <div
        style={{
          position: "absolute",
          right: 90,
          top: 116,
          width: 310,
          height: 500,
          border: "1px solid rgba(242,237,230,0.18)",
          background: "linear-gradient(180deg, rgba(242,237,230,0.08), rgba(154,123,79,0.08))",
          boxShadow: "0 34px 100px rgba(0,0,0,0.38)",
          opacity: fadeIn(frame, 16),
          transform: `translateY(${rise(frame, 16, 44)}px)`,
        }}
      >
        <div style={{ position: "absolute", left: 30, top: 34 }}>
          <FlouxLogo size={66} animatedFrame={frame - 22} />
        </div>
        <div style={{ position: "absolute", left: 30, top: 132, color: CREAM, fontSize: 28, lineHeight: 1.1 }}>
          Sistema de recuperación
          <br />
          por WhatsApp
        </div>
        <div style={{ position: "absolute", left: 30, bottom: 38, color: BODY, fontSize: 16, lineHeight: 1.5, width: 230 }}>
          Diseñado para salones que no pueden parar el servicio cada vez que suena el teléfono.
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          top: 0,
          left: sweep,
          width: 180,
          height: 720,
          transform: "skewX(-18deg)",
          background: "linear-gradient(90deg, transparent, rgba(242,237,230,0.16), transparent)",
          opacity: 0.8,
        }}
      />
    </SceneWrap>
  );
};

const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const ring = Math.sin(frame / 3) * interpolate(frame, [36, 85, 160], [0, 1, 0], clamp);
  return (
    <SceneWrap localFrame={frame}>
      <div style={{ position: "absolute", left: 78, top: 82 }}>
        <Eyebrow frame={frame}>El momento crítico</Eyebrow>
        <SceneTitle frame={frame} width={600}>
          La llamada entra cuando nadie puede cogerla.
        </SceneTitle>
        <TextLine frame={frame} delay={22} width={520}>
          La clienta está delante. El servicio no se interrumpe. La oportunidad no se pierde.
        </TextLine>
      </div>

      <div
        style={{
          position: "absolute",
          right: 82,
          top: 88,
          width: 500,
          height: 520,
          border: "1px solid rgba(154,123,79,0.28)",
          background: "rgba(14,12,10,0.78)",
          overflow: "hidden",
          opacity: fadeIn(frame, 12),
        }}
      >
        <div style={{ position: "absolute", left: 42, top: 52, width: 416, height: 250, background: "linear-gradient(135deg, rgba(242,237,230,0.10), rgba(154,123,79,0.12))" }} />
        <div style={{ position: "absolute", left: 72, top: 97, width: 110, height: 110, borderRadius: 70, background: "rgba(242,237,230,0.18)" }} />
        <div style={{ position: "absolute", left: 250, top: 110, width: 105, height: 105, borderRadius: 70, background: "rgba(154,123,79,0.24)" }} />
        <div style={{ position: "absolute", left: 86, top: 228, width: 300, height: 16, background: "rgba(242,237,230,0.24)" }} />
        <div style={{ position: "absolute", left: 118, top: 260, width: 230, height: 11, background: "rgba(154,123,79,0.36)" }} />

        <div
          style={{
            position: "absolute",
            left: 162,
            bottom: 52,
            width: 176,
            height: 176,
            border: "1px solid rgba(242,237,230,0.22)",
            background: "#181512",
            boxShadow: "0 28px 80px rgba(0,0,0,0.46)",
            transform: `rotate(${ring * 5}deg)`,
          }}
        >
          <div style={{ position: "absolute", inset: 14, border: "1px solid rgba(154,123,79,0.34)" }} />
          <div style={{ position: "absolute", left: 57, top: 36 }}>
            <IconPhone color={CREAM} />
          </div>
          <div style={{ position: "absolute", left: 36, top: 92, color: CREAM, fontSize: 17 }}>Llamada entrante</div>
          <div style={{ position: "absolute", left: 54, top: 121, color: RED, fontSize: 13, letterSpacing: "0.14em", textTransform: "uppercase" }}>
            sin coger
          </div>
        </div>
      </div>

      <Pill frame={frame} delay={76} left={92} top={546} icon={<IconPhone />}>
        El salón sigue trabajando
      </Pill>
    </SceneWrap>
  );
};

const WhatsAppScene: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <SceneWrap localFrame={frame}>
      <div style={{ position: "absolute", left: 78, top: 88 }}>
        <Eyebrow frame={frame}>Respuesta inmediata</Eyebrow>
        <SceneTitle frame={frame} width={560}>
          Floux continúa la conversación por WhatsApp.
        </SceneTitle>
        <TextLine frame={frame} delay={20} width={500}>
          Pregunta servicio, preferencia horaria y confirma los datos sin poner presión al equipo.
        </TextLine>
      </div>

      <PhoneMockup frame={frame} left={760} top={52} scale={1.02} />
      <Pill frame={frame} delay={92} left={96} top={550} icon={<IconMessage />}>
        Tono natural, en español de España
      </Pill>
    </SceneWrap>
  );
};

const PhoneMockup: React.FC<{ frame: number; left: number; top: number; scale?: number }> = ({
  frame,
  left,
  top,
  scale = 1,
}) => {
  const messages = [
    { delay: 34, text: "Hola, soy el asistente de Escultor Peluquería. ¿Quieres reservar cita?", side: "left" },
    { delay: 76, text: "Sí, corte y peinado para esta semana.", side: "right" },
    { delay: 116, text: "Perfecto. Tengo hueco mañana a las 17:30 o el viernes a las 11:00.", side: "left" },
    { delay: 158, text: "Mañana a las 17:30 me viene bien.", side: "right" },
    { delay: 196, text: "Listo. Cita confirmada para mañana a las 17:30.", side: "left" },
  ];

  return (
    <div
      style={{
        position: "absolute",
        left,
        top,
        width: 340,
        height: 616,
        transform: `scale(${scale}) translateY(${rise(frame, 8, 34)}px)`,
        transformOrigin: "top left",
        opacity: fadeIn(frame, 8),
        border: "1px solid rgba(242,237,230,0.26)",
        borderRadius: 38,
        padding: 18,
        background: "linear-gradient(180deg, #211D19, #0E0C0A)",
        boxShadow: "0 42px 110px rgba(0,0,0,0.48)",
      }}
    >
      <div
        style={{
          height: "100%",
          borderRadius: 24,
          overflow: "hidden",
          background: "#F2EDE6",
          color: "#1A1714",
          position: "relative",
        }}
      >
        <div
          style={{
            height: 78,
            background: "#171411",
            color: CREAM,
            display: "flex",
            alignItems: "center",
            padding: "0 20px",
            gap: 12,
            fontSize: 15,
          }}
        >
          <div style={{ width: 35, height: 35 }}>
            <FlouxLogo size={35} animatedFrame={999} />
          </div>
          <div>
            <div style={{ fontWeight: 600 }}>Escultor Peluquería</div>
            <div style={{ color: GOLD, fontSize: 12 }}>WhatsApp</div>
          </div>
        </div>
        <div style={{ position: "absolute", inset: "78px 0 0", padding: 18, background: "#E8E1D8" }}>
          {messages.map((message, index) => {
            const isRight = message.side === "right";
            const width = isRight ? 206 : 242;
            return (
              <div
                key={message.text}
                style={{
                  width,
                  marginLeft: isRight ? "auto" : 0,
                  marginTop: index === 0 ? 4 : 13,
                  padding: "12px 13px",
                  borderRadius: isRight ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
                  background: isRight ? "#DCF3DD" : "#FFFFFF",
                  boxShadow: "0 6px 16px rgba(26,23,20,0.10)",
                  fontSize: 13.5,
                  lineHeight: 1.3,
                  opacity: fadeIn(frame, message.delay, 12),
                  transform: `translateY(${rise(frame, message.delay, 14)}px)`,
                }}
              >
                {message.text}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

const FlowScene: React.FC = () => {
  const frame = useCurrentFrame();
  const items = [
    { title: "Llamada perdida", subtitle: "Detectada al momento", icon: <IconPhone />, delay: 36 },
    { title: "WhatsApp", subtitle: "Conversación natural", icon: <IconMessage />, delay: 76 },
    { title: "Disponibilidad", subtitle: "Huecos reales del salón", icon: <IconCalendar />, delay: 116 },
    { title: "Cita confirmada", subtitle: "Agenda actualizada", icon: <IconCalendar color={GREEN} />, delay: 156 },
  ];
  return (
    <SceneWrap localFrame={frame}>
      <div style={{ position: "absolute", left: 76, top: 74, right: 76 }}>
        <Eyebrow frame={frame}>Así funciona</Eyebrow>
        <SceneTitle frame={frame} width={860}>
          Un flujo completo, sin añadir trabajo al salón.
        </SceneTitle>
      </div>
      <div style={{ position: "absolute", left: 98, right: 98, top: 360, height: 2, background: "rgba(154,123,79,0.22)" }} />
      <div
        style={{
          position: "absolute",
          left: 98,
          top: 359,
          height: 3,
          width: interpolate(frame, [42, 182], [0, 1084], clamp),
          background: `linear-gradient(90deg, ${GOLD}, ${CREAM})`,
        }}
      />
      {items.map((item, index) => (
        <FlowNode
          key={item.title}
          frame={frame}
          delay={item.delay}
          left={98 + index * 330}
          title={item.title}
          subtitle={item.subtitle}
          icon={item.icon}
        />
      ))}
    </SceneWrap>
  );
};

const FlowNode: React.FC<{
  frame: number;
  delay: number;
  left: number;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
}> = ({ frame, delay, left, title, subtitle, icon }) => {
  const scale = spring({ frame: frame - delay, fps: 30, config: { damping: 18, stiffness: 120 } });
  return (
    <div
      style={{
        position: "absolute",
        left,
        top: 260,
        width: 230,
        opacity: fadeIn(frame, delay - 4),
        transform: `translateY(${rise(frame, delay, 26)}px) scale(${0.92 + scale * 0.08})`,
      }}
    >
      <div
        style={{
          width: 84,
          height: 84,
          display: "grid",
          placeItems: "center",
          background: "rgba(14,12,10,0.92)",
          border: "1px solid rgba(154,123,79,0.52)",
          boxShadow: "0 20px 55px rgba(0,0,0,0.34)",
          marginBottom: 28,
        }}
      >
        {icon}
      </div>
      <div style={{ fontSize: 24, color: CREAM, marginBottom: 8 }}>{title}</div>
      <div style={{ fontSize: 16, color: BODY, lineHeight: 1.35 }}>{subtitle}</div>
    </div>
  );
};

const ProofScene: React.FC = () => {
  const frame = useCurrentFrame();
  const rows = [
    ["10:42", "Corte y peinado", "Mañana 17:30", "Confirmada"],
    ["11:08", "Color", "Viernes 11:00", "Pendiente"],
    ["11:31", "Manicura", "Hoy 18:15", "Confirmada"],
  ];
  return (
    <SceneWrap localFrame={frame}>
      <div style={{ position: "absolute", left: 78, top: 84 }}>
        <Eyebrow frame={frame}>Control para el dueño</Eyebrow>
        <SceneTitle frame={frame} width={560}>
          Cada oportunidad queda visible.
        </SceneTitle>
        <TextLine frame={frame} delay={20} width={500}>
          El salón recibe aviso, ve el historial y sabe qué citas han sido recuperadas.
        </TextLine>
      </div>
      <div
        style={{
          position: "absolute",
          right: 76,
          top: 102,
          width: 586,
          height: 444,
          border: "1px solid rgba(154,123,79,0.32)",
          background: "rgba(14,12,10,0.86)",
          opacity: fadeIn(frame, 14),
          transform: `translateY(${rise(frame, 14, 34)}px)`,
          boxShadow: "0 35px 90px rgba(0,0,0,0.38)",
        }}
      >
        <div style={{ height: 72, borderBottom: "1px solid rgba(154,123,79,0.22)", display: "flex", alignItems: "center", padding: "0 24px", gap: 14 }}>
          <FlouxLogo size={40} animatedFrame={999} />
          <div>
            <div style={{ fontSize: 20 }}>Panel de citas recuperadas</div>
            <div style={{ color: BODY, fontSize: 13, marginTop: 3 }}>Resumen del día</div>
          </div>
        </div>
        <div style={{ padding: 24 }}>
          <div style={{ display: "grid", gridTemplateColumns: "72px 1fr 130px 110px", color: GOLD, fontSize: 12, letterSpacing: "0.12em", textTransform: "uppercase", paddingBottom: 12 }}>
            <div>Hora</div>
            <div>Servicio</div>
            <div>Cita</div>
            <div>Estado</div>
          </div>
          {rows.map((row, index) => (
            <div
              key={row.join("-")}
              style={{
                display: "grid",
                gridTemplateColumns: "72px 1fr 130px 110px",
                alignItems: "center",
                minHeight: 68,
                borderTop: "1px solid rgba(242,237,230,0.10)",
                fontSize: 15,
                color: LIGHT,
                opacity: fadeIn(frame, 52 + index * 22),
                transform: `translateX(${interpolate(frame, [52 + index * 22, 76 + index * 22], [20, 0], { ...clamp, easing: ease })}px)`,
              }}
            >
              <div style={{ color: BODY }}>{row[0]}</div>
              <div>{row[1]}</div>
              <div>{row[2]}</div>
              <div style={{ color: row[3] === "Confirmada" ? GREEN : GOLD }}>{row[3]}</div>
            </div>
          ))}
        </div>
      </div>
      <Pill frame={frame} delay={122} left={96} top={548} icon={<IconCalendar color={GREEN} />}>
        Menos llamadas perdidas. Más citas cerradas.
      </Pill>
    </SceneWrap>
  );
};

const OutcomeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const counters = [
    { value: "1", label: "cliente recuperado puede pagar el mes", delay: 42 },
    { value: "24h", label: "seguimiento por WhatsApp", delay: 70 },
    { value: "0", label: "interrupciones durante el servicio", delay: 98 },
  ];
  return (
    <SceneWrap localFrame={frame}>
      <div style={{ position: "absolute", left: 80, top: 78 }}>
        <Eyebrow frame={frame}>Resultado</Eyebrow>
        <SceneTitle frame={frame} width={780}>
          Una experiencia seria para salones que viven de cada cita.
        </SceneTitle>
      </div>
      <div style={{ position: "absolute", left: 90, right: 90, top: 380, display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 24 }}>
        {counters.map((counter) => (
          <div
            key={counter.label}
            style={{
              height: 168,
              border: "1px solid rgba(154,123,79,0.30)",
              background: "rgba(14,12,10,0.78)",
              padding: 26,
              opacity: fadeIn(frame, counter.delay),
              transform: `translateY(${rise(frame, counter.delay, 28)}px)`,
            }}
          >
            <div style={{ color: GOLD, fontFamily: titleFont, fontSize: 62, lineHeight: 0.9 }}>{counter.value}</div>
            <div style={{ color: LIGHT, fontSize: 18, lineHeight: 1.35, marginTop: 20 }}>{counter.label}</div>
          </div>
        ))}
      </div>
    </SceneWrap>
  );
};

const EndScene: React.FC = () => {
  const frame = useCurrentFrame();
  const logoScale = spring({ frame: frame - 18, fps: 30, config: { damping: 22, stiffness: 95 } });
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 36%, rgba(154,123,79,0.22), transparent 34%), ${DARK}`,
        display: "grid",
        placeItems: "center",
        color: CREAM,
      }}
    >
      <div style={{ textAlign: "center", opacity: fadeIn(frame, 0), transform: `scale(${0.92 + logoScale * 0.08})` }}>
        <div style={{ margin: "0 auto 22px", width: 132, height: 132 }}>
          <FlouxLogo size={132} animatedFrame={frame - 14} />
        </div>
        <div style={{ fontFamily: titleFont, fontSize: 78, lineHeight: 0.9, fontWeight: 300 }}>Floux</div>
        <div style={{ marginTop: 24, color: LIGHT, fontSize: 24, fontWeight: 300 }}>
          Recuperamos los clientes que pierdes cuando no puedes coger el teléfono.
        </div>
        <div
          style={{
            margin: "34px auto 0",
            width: 340,
            height: 1,
            background: `linear-gradient(90deg, transparent, ${GOLD}, transparent)`,
            opacity: fadeIn(frame, 62),
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

export const FlouxSalesVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = (seconds: number) => Math.round(seconds * fps);

  return (
    <AbsoluteFill style={{ background: DARKER }}>
      <Sequence from={s(0)} durationInFrames={s(6)}>
        <IntroScene />
      </Sequence>
      <Sequence from={s(6)} durationInFrames={s(7)}>
        <ProblemScene />
      </Sequence>
      <Sequence from={s(13)} durationInFrames={s(9)}>
        <WhatsAppScene />
      </Sequence>
      <Sequence from={s(22)} durationInFrames={s(7)}>
        <FlowScene />
      </Sequence>
      <Sequence from={s(29)} durationInFrames={s(7)}>
        <ProofScene />
      </Sequence>
      <Sequence from={s(36)} durationInFrames={s(4)}>
        <OutcomeScene />
      </Sequence>
      <Sequence from={s(40)} durationInFrames={s(2)}>
        <EndScene />
      </Sequence>
      <div
        style={{
          position: "absolute",
          left: 54,
          bottom: 30,
          color: "rgba(242,237,230,0.46)",
          fontSize: 12,
          letterSpacing: "0.16em",
          textTransform: "uppercase",
          opacity: frame < s(39.6) ? 1 : interpolate(frame, [s(39.6), s(40.2)], [1, 0], clamp),
        }}
      >
        Floux
      </div>
    </AbsoluteFill>
  );
};
