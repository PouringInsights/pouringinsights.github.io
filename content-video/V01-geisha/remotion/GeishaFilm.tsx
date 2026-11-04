import React, { useMemo } from "react";
import { AbsoluteFill, Audio, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import "./fonts.css";
import { geoOrthographic, geoPath, geoGraticule10, geoInterpolate } from "d3-geo";
import { feature } from "topojson-client";
// eslint-disable-next-line @typescript-eslint/no-var-requires
const world = require("world-atlas/countries-110m.json");

const sans = "'Be Vietnam Pro'";

// Watercolour pigments, derived from the subject (see art-direction.md)
export const P = {
  paper: "#F3F2EE",
  payne: "#26303A",
  sap: "#2E5E3E",
  crimson: "#B0183F",
  cerulean: "#3B8FC2",
  hansa: "#F2C94C",
  leaf: "#8DB33A",
  greyblue: "#5E86A8",
  sienna: "#9C4A26",
  umber: "#5B3A22",
};

export type Word = { text: string; start: number; end: number };
export type Beats = {
  myth: number; reveal: number; map: number; rust: number; forgot: number;
  turn: number; record2004: number; payoff: number; cta: number; question: number;
};
export type GeishaProps = { audio: string; music: string | null; duration: number; words: Word[]; beats: Beats };
export const defaultProps: GeishaProps = {
  audio: "geisha/vo.wav", music: null, duration: 58, words: [],
  beats: { myth: 4, reveal: 8, map: 12, rust: 20, forgot: 26, turn: 30, record2004: 38, payoff: 42, cta: 50, question: 55 },
};

const FPS = 30;
const f = (s: number) => Math.round(s * FPS);
const EXPO = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ramp = (frame: number, a: number, b: number) => interpolate(frame, [a, b], [0, 1], { ...clamp, easing: EXPO });

// ── Watercolour engine ──────────────────────────────────────────────
// A wash = a shape pushed through turbulence (wobbly bleed edge), edge-darkened
// (pigment pools at the rim) and granulated (pigment settles into paper tooth).
const WashFilter: React.FC<{ id: string; seed: number; distort?: number; body?: number; rim?: number; grainFreq?: number }> = ({ id, seed, distort = 70, body = 0.6, rim = 0.85, grainFreq = 0.55 }) => (
  <filter id={id} x="-40%" y="-40%" width="180%" height="180%" colorInterpolationFilters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.007" numOctaves={3} seed={seed} result="warp" />
    <feDisplacementMap in="SourceGraphic" in2="warp" scale={distort} xChannelSelector="R" yChannelSelector="G" result="shape" />
    <feGaussianBlur in="shape" stdDeviation={9} result="soft" />
    <feComposite in="shape" in2="soft" operator="arithmetic" k1={0} k2={body + rim} k3={-rim} k4={0} result="rimmed" />
    <feTurbulence type="fractalNoise" baseFrequency={grainFreq} numOctaves={2} seed={seed + 7} result="gran" />
    <feColorMatrix in="gran" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 1.25" result="granA" />
    <feComposite in="rimmed" in2="granA" operator="in" />
  </filter>
);

type WashProps = { id: string; seed: number; color: string; cx: number; cy: number; r: number; p: number; body?: number; rim?: number; distort?: number };
const Wash: React.FC<WashProps> = ({ id, seed, color, cx, cy, r, p, body, rim, distort }) => (
  <g style={{ mixBlendMode: "multiply" }}>
    <defs><WashFilter id={id} seed={seed} body={body} rim={rim} distort={distort} /></defs>
    <circle cx={cx} cy={cy} r={Math.max(0.1, r * p)} fill={color} filter={`url(#${id})`} />
  </g>
);

// a full-bleed field that blooms from a point (the signature move)
const Field: React.FC<{ id: string; color: string; ox?: number; oy?: number; at?: number; seed?: number }> = ({ id, color, ox = 540, oy = 960, at = 0, seed = 3 }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - at, [0, 22], [0, 1], { ...clamp, easing: Easing.bezier(0.3, 0.7, 0.2, 1) });
  if (p <= 0) return null;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <Wash id={id} seed={seed} color={color} cx={ox} cy={oy} r={2300} p={p} body={1} rim={0.2} distort={160} />
    </svg>
  );
};

const Paper: React.FC = () => (
  <AbsoluteFill style={{ background: P.paper }}>
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.55, mixBlendMode: "multiply" }}>
      <filter id="paper">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={3} seed={11} result="n" />
        <feDiffuseLighting in="n" surfaceScale={1.6} lightingColor="#ffffff" result="lit">
          <feDistantLight azimuth={45} elevation={58} />
        </feDiffuseLighting>
      </filter>
      <rect width={1080} height={1920} filter="url(#paper)" />
    </svg>
  </AbsoluteFill>
);

const T: React.FC<{ size: number; color: string; weight?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ size, color, weight = 800, style, children }) => (
  <div style={{ fontFamily: sans, fontWeight: weight, fontSize: size, color, lineHeight: 1.08, letterSpacing: size > 120 ? -size * 0.03 : 0, fontVariantNumeric: "tabular-nums", ...style }}>{children}</div>
);

const Rise: React.FC<{ at?: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ at = 0, children, style }) => {
  const frame = useCurrentFrame();
  const p = ramp(frame, at, at + 14);
  return <div style={{ opacity: p, transform: `translateY(${(1 - p) * 24}px)`, ...style }}>{children}</div>;
};

// ── 1. Hook: the auction price on a crimson bloom ─────────────────────
const SceneHook: React.FC = () => {
  const frame = useCurrentFrame();
  const p = ramp(frame, 0, 26);
  const money = Math.round(interpolate(frame, [0, 40], [120000, 604080], { ...clamp, easing: EXPO }));
  return (
    <AbsoluteFill>
      <Paper />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <Wash id="hookA" seed={4} color={P.crimson} cx={560} cy={860} r={470} p={p} body={0.82} rim={0.4} />
        <Wash id="hookB" seed={9} color={P.crimson} cx={380} cy={1010} r={240} p={ramp(frame, 6, 30)} body={0.35} rim={0.5} />
      </svg>
      <T size={92} color={P.payne} style={{ position: "absolute", left: 80, top: 330 }}>20 ký cà phê</T>
      <T size={170} color={P.paper} weight={900} style={{ position: "absolute", left: 70, top: 780 }}>${money.toLocaleString("de-DE")}</T>
      <T size={42} color={P.payne} weight={600} style={{ position: "absolute", left: 80, top: 1330 }}>Đấu giá Best of Panama, 2025</T>
    </AbsoluteFill>
  );
};

// ── 2. The misread name: GEISHA loses its I, the forest floods in ─────
const SceneMyth: React.FC<{ revealAt: number }> = ({ revealAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const r = frame - revealAt;
  const drop = r > 0 ? Math.min(1, (r / fps) ** 2 * 1.8) : 0;
  const close = interpolate(r, [8, 22], [0, 1], { ...clamp, easing: EXPO });
  const flooded = r > 6;
  const sun = ramp(frame, 0, 24);
  const letters = ["G", "E", "I", "S", "H", "A"];
  return (
    <AbsoluteFill>
      <Paper />
      <svg width={1080} height={1920} style={{ position: "absolute", opacity: flooded ? 0 : 1 }}>
        <Wash id="sun" seed={21} color={P.crimson} cx={540} cy={560} r={250} p={sun} body={0.75} rim={0.6} distort={40} />
      </svg>
      <Field id="forest" color={P.sap} ox={540} oy={1500} at={revealAt + 2} seed={5} />
      <div style={{ position: "absolute", top: 860, width: "100%", display: "flex", justifyContent: "center", fontFamily: sans, fontWeight: 900, fontSize: 230, letterSpacing: -6, color: flooded ? P.paper : P.payne }}>
        {letters.map((l, i) =>
          i === 2 ? (
            <span key={i} style={{ display: "inline-block", width: interpolate(close, [0, 1], [74, 0]), transform: `translateY(${drop * 1100}px) rotate(${drop * 120}deg)`, color: P.crimson }}>{l}</span>
          ) : (
            <span key={i}>{l}</span>
          ),
        )}
      </div>
      {!flooded ? (
        <Rise at={12} style={{ position: "absolute", left: 80, top: 1180 }}>
          <T size={60} color={P.payne} weight={600}>kimono? trà đạo? Kyoto?</T>
        </Rise>
      ) : (
        <Rise at={revealAt + 16} style={{ position: "absolute", left: 80, top: 1160, width: 900 }}>
          <T size={92} color={P.paper}>Rừng Gesha</T>
          <T size={60} color={P.paper} weight={600} style={{ marginTop: 14 }}>tây nam Ethiopia, thập niên 1930</T>
        </Rise>
      )}
    </AbsoluteFill>
  );
};

// ── 3. The journey on a painted globe ───────────────────────────────
const land = feature(world, world.objects.countries) as any;
const STOPS = [
  { lon: 35.3, lat: 7.1 },
  { lon: -83.65, lat: 9.9 },
  { lon: -82.44, lat: 8.78 },
];
const SceneGlobe: React.FC<{ len: number }> = ({ len }) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [6, len - 10], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const segT = [0, 0.65, 1];
  const pts: [number, number][] = [];
  for (let s = 0; s < 2; s++) {
    const local = interpolate(t, [segT[s], segT[s + 1]], [0, 1], clamp);
    if (local <= 0) break;
    const ip = geoInterpolate([STOPS[s].lon, STOPS[s].lat], [STOPS[s + 1].lon, STOPS[s + 1].lat]);
    const n = Math.max(2, Math.round(120 * local));
    for (let k = 0; k <= n; k++) pts.push(ip((k / n) * local) as [number, number]);
  }
  const head = pts.length ? pts[pts.length - 1] : [STOPS[0].lon, STOPS[0].lat];
  const proj = geoOrthographic().scale(420).translate([540, 980]).rotate([-head[0], -10, 0]).clipAngle(90);
  const path = geoPath(proj);
  const trail = pts.length > 1 ? path({ type: "LineString", coordinates: pts } as any) || "" : "";
  const yr = t < 0.08 ? "1930s" : t < 0.65 ? "1953" : "1960s";
  const place = t < 0.08 ? "Gesha, Ethiopia" : t < 0.65 ? "trạm nghiên cứu ở Costa Rica" : "Panama";
  const dot = (lon: number, lat: number, color: string, id: string, seed: number) => {
    const p = proj([lon, lat]);
    const hidden = path({ type: "Point", coordinates: [lon, lat] } as any) === null;
    if (!p || hidden) return null;
    return <Wash id={id} seed={seed} color={color} cx={p[0]} cy={p[1]} r={34} p={1} body={0.9} rim={0.4} distort={18} />;
  };
  return (
    <AbsoluteFill>
      <Paper />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <defs>
          <WashFilter id="ocean" seed={31} distort={30} body={0.55} rim={0.7} />
          <WashFilter id="landw" seed={33} distort={8} body={0.7} rim={0.5} grainFreq={0.8} />
        </defs>
        <g style={{ mixBlendMode: "multiply" }}>
          <path d={path({ type: "Sphere" } as any) || ""} fill={P.cerulean} filter="url(#ocean)" />
        </g>
        <path d={path(geoGraticule10()) || ""} fill="none" stroke={P.paper} strokeOpacity={0.25} strokeWidth={1.5} />
        <g style={{ mixBlendMode: "multiply" }} filter="url(#landw)">
          {land.features.map((ft: any, i: number) => <path key={i} d={path(ft) || ""} fill={P.leaf} />)}
        </g>
        <path d={trail} fill="none" stroke={P.payne} strokeWidth={9} strokeLinecap="round" />
        {dot(STOPS[0].lon, STOPS[0].lat, P.sap, "d0", 41)}
        {t >= 0.64 ? dot(STOPS[1].lon, STOPS[1].lat, P.hansa, "d1", 42) : null}
        {t >= 0.99 ? dot(STOPS[2].lon, STOPS[2].lat, P.crimson, "d2", 43) : null}
      </svg>
      <T size={200} color={P.payne} weight={900} style={{ position: "absolute", left: 80, top: 230 }}>{yr}</T>
      <T size={60} color={P.payne} weight={600} style={{ position: "absolute", left: 80, top: 1450 }}>{place}</T>
    </AbsoluteFill>
  );
};

// ── 4. Rust, and forty years of nobody caring (Payne's grey field) ───
const SceneRust: React.FC<{ forgotAt: number }> = ({ forgotAt }) => {
  const frame = useCurrentFrame();
  const leaf = ramp(frame, 0, 24);
  const spots = [[-50, -60, 34], [40, 20, 44], [-20, 110, 26], [60, -130, 22], [-70, 150, 28]];
  const fade = interpolate(frame - forgotAt, [0, 36], [0, 1], clamp);
  const years = Math.round(interpolate(frame - forgotAt, [8, 66], [0, 40], clamp));
  return (
    <AbsoluteFill>
      <Paper />
      <Field id="payne" color={P.payne} ox={0} oy={0} seed={12} />
      <AbsoluteFill style={{ filter: `saturate(${1 - fade}) brightness(${1 - fade * 0.5})` }}>
        <svg width={1080} height={1920} style={{ position: "absolute" }}>
          <defs><WashFilter id="leafw" seed={51} distort={22} body={0.8} rim={0.6} /></defs>
          <g transform={`translate(520 1000) rotate(-24) scale(${0.6 + leaf * 0.9})`} opacity={leaf}>
            <path d="M0,-260 C170,-170 180,140 0,260 C-180,140 -170,-170 0,-260 Z" fill={P.leaf} filter="url(#leafw)" />
            {spots.map(([x, y, rr], i) => (
              <Wash key={i} id={`rust${i}`} seed={60 + i} color={P.sienna} cx={x} cy={y} r={rr} p={ramp(frame, 14 + i * 7, 40 + i * 7)} body={0.85} rim={0.5} distort={14} />
            ))}
          </g>
        </svg>
        <Rise at={4} style={{ position: "absolute", left: 80, top: 260, width: 880 }}>
          <T size={92} color={P.paper}>Nhiệm vụ: chống gỉ sắt lá</T>
        </Rise>
        <Rise at={40} style={{ position: "absolute", left: 80, top: 1440, width: 880 }}>
          <T size={60} color={P.paper} weight={600}>Năng suất thấp. Chẳng ai mặn mà.</T>
        </Rise>
      </AbsoluteFill>
      <AbsoluteFill style={{ opacity: fade, justifyContent: "center", paddingLeft: 80 }}>
        <T size={230} color={P.paper} weight={900}>~{years} năm</T>
        <T size={60} color={P.paper} weight={600} style={{ marginTop: 10 }}>bị bỏ xó</T>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── 5. The first sip: three glazes of flavour ─────────────────────────
const SceneTurn: React.FC<{ recordAt: number }> = ({ recordAt }) => {
  const frame = useCurrentFrame();
  const notes = [
    { t: "hoa nhài", c: P.hansa, x: 400, y: 760, r: 230, lx: 80, ly: 520 },
    { t: "cam bergamot", c: P.leaf, x: 700, y: 900, r: 220, lx: 600, ly: 600 },
    { t: "trà Earl Grey", c: P.greyblue, x: 500, y: 1080, r: 230, lx: 80, ly: 1300 },
  ];
  const rec = ramp(frame, recordAt, recordAt + 16);
  return (
    <AbsoluteFill>
      <Paper />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        {notes.map((n, i) => (
          <Wash key={n.t} id={`note${i}`} seed={70 + i} color={n.c} cx={n.x} cy={n.y} r={n.r} p={ramp(frame, 14 + i * 16, 44 + i * 16)} body={0.55} rim={0.7} />
        ))}
        <Wash id="cup" seed={80} color={P.umber} cx={560} cy={910} r={120} p={ramp(frame, 0, 20)} body={0.9} rim={0.6} distort={20} />
      </svg>
      <Rise style={{ position: "absolute", left: 80, top: 230, width: 900 }}>
        <T size={92} color={P.payne}>Ngụm đầu tiên</T>
        <T size={42} color={P.payne} weight={600} style={{ marginTop: 10 }}>chuyện tương truyền ở La Esmeralda, Panama</T>
      </Rise>
      {notes.map((n, i) => (
        <Rise key={n.t} at={22 + i * 16} style={{ position: "absolute", left: n.lx, top: n.ly }}>
          <T size={60} color={P.payne} style={{ whiteSpace: "nowrap" }}>{n.t}</T>
        </Rise>
      ))}
      <div style={{ position: "absolute", left: 80, top: 1420, opacity: rec, transform: `translateY(${(1 - rec) * 24}px)` }}>
        <div style={{ height: 12, width: 420 * rec, background: P.crimson, marginBottom: 18 }} />
        <T size={60} color={P.crimson} weight={900}>2004: phá kỷ lục đấu giá</T>
      </div>
    </AbsoluteFill>
  );
};

// ── 6. Payoff: the crimson field ─────────────────────────────────────
const ScenePayoff: React.FC = () => {
  const frame = useCurrentFrame();
  const n = Math.round(interpolate(frame, [6, 50], [21, 30204], { ...clamp, easing: Easing.out(Easing.exp) }));
  return (
    <AbsoluteFill>
      <Paper />
      <Field id="crim" color={P.crimson} ox={540} oy={960} seed={14} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", marginTop: -160 }}>
        <T size={230} color={P.paper} weight={900}>${n.toLocaleString("de-DE")}</T>
        <T size={92} color={P.paper} style={{ marginTop: 6 }}>cho 1 ký</T>
        <Rise at={40} style={{ marginTop: 60 }}>
          <T size={60} color={P.paper} weight={600}>Tháng 8/2025. Tới giờ chưa ai phá.</T>
        </Rise>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── 7. Barista maths, the question, and the loop back to the name ────
const SceneCTA: React.FC<{ qAt: number; endAt: number }> = ({ qAt, endAt }) => {
  const frame = useCurrentFrame();
  const ended = frame >= endAt + 8;
  return (
    <AbsoluteFill>
      <Paper />
      {!ended && (
        <>
          <svg width={1080} height={1920} style={{ position: "absolute" }}>
          </svg>
          <Rise style={{ position: "absolute", left: 80, top: 260, width: 900 }}>
            <T size={92} color={P.payne}>Barista tính nhẩm</T>
          </Rise>
          <Rise at={18} style={{ position: "absolute", left: 80, top: 440 }}>
            <T size={60} color={P.payne} weight={600}>15 g × $30.204/kg</T>
          </Rise>
          <Rise at={60} style={{ position: "absolute", left: 80, top: 560 }}>
            <T size={150} color={P.crimson} weight={900}>≈ $453</T>
            <T size={60} color={P.payne} weight={600}>tiền hạt cho một ly</T>
          </Rise>
          <Rise at={qAt} style={{ position: "absolute", left: 80, top: 1000, width: 900 }}>
            <T size={92} color={P.payne}>Bạn trả tối đa bao nhiêu?</T>
            <T size={60} color={P.payne} weight={600} style={{ marginTop: 16 }}>Comment một con số.</T>
          </Rise>
        </>
      )}
      <Field id="endf" color={P.sap} ox={540} oy={1920} at={endAt} seed={5} />
      {ended && (
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <Rise at={endAt + 10}>
            <T size={230} color={P.paper} weight={900} style={{ textAlign: "center" }}>Gesha</T>
            <T size={92} color={P.hansa} style={{ textAlign: "center" }}>không phải</T>
            <T size={230} color={P.paper} weight={900} style={{ textAlign: "center" }}>geisha</T>
          </Rise>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

// ── Captions: 2–4 word chunks, paper type with an ink outline, active word in Hansa yellow ──
const Captions: React.FC<{ words: Word[]; hideFrom: number }> = ({ words, hideFrom }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const chunks = useMemo(() => {
    const out: Word[][] = [];
    let cur: Word[] = [];
    words.forEach((w, i) => {
      cur.push(w);
      const gap = words[i + 1] ? words[i + 1].start - w.end > 0.2 : true;
      if (cur.length >= 4 || gap) { out.push(cur); cur = []; }
    });
    if (cur.length) out.push(cur);
    return out;
  }, [words]);
  if (t >= hideFrom) return null;
  const idx = chunks.findIndex((c, i) => t >= c[0].start - 0.05 && t < (chunks[i + 1] ? chunks[i + 1][0].start - 0.05 : c[c.length - 1].end + 0.6));
  if (idx < 0) return null;
  const chunk = chunks[idx];
  return (
    <AbsoluteFill style={{ top: 1600, height: 200, alignItems: "center", paddingLeft: 60, paddingRight: 150 }}>
      <div style={{ textAlign: "center", fontFamily: sans, fontWeight: 900, fontSize: 62, lineHeight: 1.15, color: P.paper, WebkitTextStroke: `8px ${P.payne}`, paintOrder: "stroke fill" }}>
        {chunk.map((w, i) => {
          const active = t >= w.start && t < w.end + 0.05;
          return <span key={i} style={{ color: active ? P.hansa : P.paper }}>{w.text}{i < chunk.length - 1 ? " " : ""}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

export const GeishaFilm: React.FC<GeishaProps> = ({ audio, music, duration, words, beats: b }) => {
  const scenes: { from: number; to: number; el: React.ReactNode }[] = [
    { from: 0, to: b.myth, el: <SceneHook /> },
    { from: b.myth, to: b.map, el: <SceneMyth revealAt={f(b.reveal - b.myth)} /> },
    { from: b.map, to: b.rust, el: <SceneGlobe len={f(b.rust - b.map)} /> },
    { from: b.rust, to: b.turn, el: <SceneRust forgotAt={f(b.forgot - b.rust)} /> },
    { from: b.turn, to: b.payoff, el: <SceneTurn recordAt={f(b.record2004 - b.turn)} /> },
    { from: b.payoff, to: b.cta, el: <ScenePayoff /> },
    { from: b.cta, to: duration, el: <SceneCTA qAt={f(b.question - b.cta)} endAt={f(duration - 2.6 - b.cta)} /> },
  ];
  return (
    <AbsoluteFill style={{ background: P.paper }}>
      {scenes.map((s, i) => (
        <Sequence key={i} from={f(s.from)} durationInFrames={Math.max(1, f(s.to) - f(s.from))}>
          {s.el}
        </Sequence>
      ))}
      <Captions words={words} hideFrom={duration - 2.4} />
      <Audio src={staticFile(audio)} />
      {music ? <Audio src={staticFile(music)} volume={0.13} /> : null}
    </AbsoluteFill>
  );
};
