import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import "./fonts.css";
import { geoOrthographic, geoPath, geoGraticule10, geoInterpolate } from "d3-geo";
import { feature } from "topojson-client";
// eslint-disable-next-line @typescript-eslint/no-var-requires
const world = require("world-atlas/countries-110m.json");

const sans = "'Be Vietnam Pro'";
const serif = "'Fraunces'";
const serifUp = "'Fraunces'";
// ── Palette (split-complementary around coffee-cherry red, on a roast-dark base) ──
export const C = {
  roast: "#16100D", // 60% base
  roast2: "#241914",
  mocha: "#A47864", // 30% (Pantone 2025 Mocha Mousse family)
  cloud: "#F0EEE9", // text (Pantone 2026 Cloud Dancer family)
  cherry: "#FF5A3C", // 10% hot accent – coffee cherry, price, hook
  jade: "#1FB59A", // complement – Gesha forest, the truth
  jasmine: "#FFE6A7", // highlight – aroma, flavour
};

export type Word = { text: string; start: number; end: number };
export type Beats = {
  myth: number; reveal: number; map: number; rust: number; forgot: number;
  turn: number; record2004: number; payoff: number; cta: number; question: number;
};
export type GeishaProps = {
  audio: string; music: string | null; duration: number; words: Word[]; beats: Beats;
};
export const defaultProps: GeishaProps = {
  audio: "vo.mp3", music: null, duration: 58,
  words: [],
  beats: { myth: 4, reveal: 8, map: 12, rust: 20, forgot: 26, turn: 30, record2004: 38, payoff: 42, cta: 50, question: 55 },
};

const FPS = 30;
const f = (s: number) => Math.round(s * FPS);

// ── shared atoms ──
const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  const seed = frame % 6;
  return (
    <AbsoluteFill style={{ pointerEvents: "none", opacity: 0.07, mixBlendMode: "overlay" }}>
      <svg width="100%" height="100%">
        <filter id={`n${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={seed} />
        </filter>
        <rect width="100%" height="100%" filter={`url(#n${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};

const Kicker: React.FC<{ children: React.ReactNode; color?: string; delay?: number }> = ({ children, color = C.mocha, delay = 0 }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame - delay, [0, 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 34, letterSpacing: 6, textTransform: "uppercase", color, opacity: o, transform: `translateY(${(1 - o) * 14}px)` }}>
      {children}
    </div>
  );
};

const useSpring = (delay = 0, damping = 14) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: { damping, stiffness: 140, mass: 0.8 } });
};

// ── Scene 1: auction evidence (hook) ──
const SceneHook: React.FC = () => {
  const frame = useCurrentFrame();
  const pop = useSpring(0, 11);
  const money = Math.round(interpolate(frame, [0, 40], [120000, 604080], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }));
  const tilt = interpolate(frame, [0, 120], [-4, -1.5]);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 38%, ${C.roast2} 0%, ${C.roast} 70%)`, alignItems: "center", justifyContent: "center" }}>
      <div style={{ transform: `translateY(-170px) rotate(${tilt}deg) scale(${0.9 + pop * 0.1})`, background: C.cloud, color: C.roast, borderRadius: 28, padding: "54px 64px", width: 820, boxShadow: `0 40px 120px rgba(0,0,0,.55), 0 0 0 6px ${C.cherry}` }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontFamily: sans, fontWeight: 800, fontSize: 30, letterSpacing: 4, color: C.mocha }}>
          <span>LÔ ĐẤU GIÁ</span><span>2025</span>
        </div>
        <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 150, lineHeight: 1, marginTop: 18 }}>20 KG</div>
        <div style={{ height: 4, background: C.roast, opacity: 0.12, margin: "26px 0" }} />
        <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 116, color: C.cherry, fontVariantNumeric: "tabular-nums", lineHeight: 1 }}>
          ${money.toLocaleString("de-DE")}
        </div>
        <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 30, marginTop: 14, color: C.mocha }}>Best of Panama · Geisha</div>
      </div>
    </AbsoluteFill>
  );
};

// ── Scene 2: the misread name (signature device: the falling "I") ──
const SceneMyth: React.FC<{ revealAt: number }> = ({ revealAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inn = useSpring(0, 13);
  const r = frame - revealAt;
  const drop = r > 0 ? Math.min(1, (r / fps) ** 2 * 1.6) : 0;
  const close = spring({ frame: r - 10, fps, config: { damping: 15 } });
  const sunOut = interpolate(r, [0, 14], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const green = interpolate(r, [8, 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const letters = ["G", "E", "I", "S", "H", "A"];
  const tagO = interpolate(r, [18, 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const chips = ["kimono?", "trà đạo?", "Kyoto?"];
  return (
    <AbsoluteFill style={{ background: C.roast, alignItems: "center", justifyContent: "center" }}>
      {/* rising sun cue, fades on reveal */}
      <div style={{ position: "absolute", top: 470, width: 520, height: 520, borderRadius: "50%", background: C.cherry, opacity: 0.9 * sunOut * inn, transform: `scale(${0.7 + inn * 0.3})` }} />
      {/* forest glow on reveal */}
      <div style={{ position: "absolute", top: 380, width: 800, height: 800, borderRadius: "50%", background: `radial-gradient(circle, ${C.jade}55 0%, transparent 65%)`, opacity: green }} />
      <div style={{ position: "absolute", top: 560, display: "flex", fontFamily: serifUp, fontWeight: 900, fontSize: 230, color: green > 0.5 ? C.jade : C.cloud, letterSpacing: -4 }}>
        {letters.map((l, i) => {
          const isI = i === 2;
          const shift = i > 2 ? -close * 84 : 0;
          const style: React.CSSProperties = isI
            ? { display: "inline-block", width: interpolate(close, [0, 1], [84, 0]), transform: `translateY(${drop * 1100}px) rotate(${drop * 140}deg)`, color: C.cherry, opacity: 1 - drop * 0.2 }
            : { display: "inline-block", transform: `translateX(${shift * 0}px)` };
          return <span key={i} style={style}>{l}</span>;
        })}
      </div>
      <div style={{ position: "absolute", top: 860, display: "flex", gap: 18, opacity: sunOut }}>
        {chips.map((c, i) => {
          const o = interpolate(frame, [10 + i * 8, 20 + i * 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <div key={c} style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 600, fontSize: 44, color: C.cloud, border: `3px solid ${C.mocha}`, borderRadius: 60, padding: "8px 28px", opacity: o }}>{c}</div>
          );
        })}
      </div>
      <div style={{ position: "absolute", top: 870, textAlign: "center", opacity: tagO }}>
        <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 600, fontSize: 58, color: C.cloud }}>rừng Gesha</div>
        <Kicker color={C.jade}>Tây Nam Ethiopia · thập niên 1930</Kicker>
      </div>
    </AbsoluteFill>
  );
};

// ── Scene 3: globe journey ──
const land = feature(world, world.objects.countries) as any;
const STOPS = [
  { name: "Gesha, Ethiopia", year: "1930s", lon: 35.3, lat: 7.1 },
  { name: "CATIE, Costa Rica", year: "1953", lon: -83.65, lat: 9.9 },
  { name: "Panama", year: "1960s", lon: -82.44, lat: 8.78 },
];
const SceneGlobe: React.FC<{ len: number }> = ({ len }) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [6, len - 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  // segments: 0-1 (E→EA) 0..0.15, 1-2 (EA→CR) 0.15..0.85, 2-3 0.85..1
  const segT = [0, 0.65, 1];
  const pts: [number, number][] = [];
  const steps = 120;
  for (let s = 0; s < 2; s++) {
    const a = STOPS[s], b = STOPS[s + 1];
    const local = interpolate(t, [segT[s], segT[s + 1]], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    if (local <= 0) break;
    const ip = geoInterpolate([a.lon, a.lat], [b.lon, b.lat]);
    const n = Math.max(2, Math.round(steps * local));
    for (let k = 0; k <= n; k++) pts.push(ip((k / n) * local) as [number, number]);
  }
  const head = pts.length ? pts[pts.length - 1] : [STOPS[0].lon, STOPS[0].lat];
  const rotLon = -head[0];
  const proj = geoOrthographic().scale(430).translate([540, 900]).rotate([rotLon, -10, 0]).clipAngle(90);
  const path = geoPath(proj);
  const grat = geoGraticule10();
  const sphere = path({ type: "Sphere" } as any) || "";
  const trail = pts.length > 1 ? path({ type: "LineString", coordinates: pts } as any) || "" : "";
  const visibleStops = STOPS.map((s, i) => ({ ...s, i, reached: t >= (i === 0 ? 0 : segT[i]) - 0.001 }));
  const yr = t < 0.08 ? "1930s" : t < 0.65 ? "1953" : "1960s";
  return (
    <AbsoluteFill style={{ background: C.roast }}>
      <svg width={1080} height={1920}>
        <defs>
          <radialGradient id="sea" cx="40%" cy="35%" r="70%">
            <stop offset="0%" stopColor="#2E211B" />
            <stop offset="100%" stopColor={C.roast} />
          </radialGradient>
        </defs>
        <path d={sphere} fill="url(#sea)" stroke={C.mocha} strokeOpacity={0.35} strokeWidth={2} />
        <path d={path(grat) || ""} fill="none" stroke={C.mocha} strokeOpacity={0.12} strokeWidth={1} />
        {land.features.map((ft: any, i: number) => (
          <path key={i} d={path(ft) || ""} fill={C.mocha} fillOpacity={0.55} stroke={C.roast} strokeWidth={0.8} />
        ))}
        <path d={trail} fill="none" stroke={C.jasmine} strokeWidth={7} strokeLinecap="round" strokeDasharray="2 16" />
        {visibleStops.map((s) => {
          const p = proj([s.lon, s.lat]);
          const back = path({ type: "Point", coordinates: [s.lon, s.lat] } as any) === null;
          if (!p || back || !s.reached) return null;
          const col = s.i === 0 ? C.jade : s.i === 2 ? C.cherry : C.jasmine;
          return (
            <g key={s.name}>
              <circle cx={p[0]} cy={p[1]} r={16} fill={col} />
              <circle cx={p[0]} cy={p[1]} r={30 + (frame % 30)} fill="none" stroke={col} strokeOpacity={1 - (frame % 30) / 30} strokeWidth={3} />
            </g>
          );
        })}
      </svg>
      <AbsoluteFill style={{ top: 250, alignItems: "center" }}>
        <Kicker color={C.mocha}>Hành trình của hạt giống</Kicker>
        <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 150, color: C.cloud, marginTop: 6, fontVariantNumeric: "tabular-nums" }}>{yr}</div>
      </AbsoluteFill>
      <AbsoluteFill style={{ top: 1360, alignItems: "center" }}>
        <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 600, fontSize: 56, color: t < 0.08 ? C.jade : t < 0.65 ? C.jasmine : C.cherry }}>
          {t < 0.08 ? "Gesha, Ethiopia" : t < 0.65 ? "trạm nghiên cứu · Costa Rica" : "Panama"}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Scene 4: the boring mission & being forgotten ──
const SceneRust: React.FC<{ forgotAt: number }> = ({ forgotAt }) => {
  const frame = useCurrentFrame();
  const leafIn = useSpring(0, 12);
  const spots = [[-60, -40, 26], [40, 30, 34], [-20, 80, 20], [70, -90, 18], [-80, 120, 22], [10, -10, 16]];
  const plant = interpolate(frame, [30, 90], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) });
  const fade = interpolate(frame - forgotAt, [0, 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const years = Math.round(interpolate(frame - forgotAt, [10, 70], [0, 40], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <AbsoluteFill style={{ background: C.roast }}>
      <AbsoluteFill style={{ filter: `grayscale(${fade}) brightness(${1 - fade * 0.55})`, }}>
        {/* leaf, intimate close-up, left third */}
        <svg width={1080} height={1920} style={{ position: "absolute" }}>
          <g transform={`translate(380 900) rotate(-28) scale(${leafIn * 1.5})`}>
            <path d="M0,-230 C150,-150 160,120 0,230 C-160,120 -150,-150 0,-230 Z" fill="#2F7D5B" />
            <path d="M0,-220 L0,220" stroke="#1B4D38" strokeWidth={8} />
            {[...Array(6)].map((_, i) => (
              <path key={i} d={`M0,${-150 + i * 60} q ${i % 2 ? 90 : -90} -20 ${i % 2 ? 120 : -120} -70`} stroke="#1B4D38" strokeWidth={5} fill="none" />
            ))}
            {spots.map(([x, y, rr], i) => {
              const g = interpolate(frame, [12 + i * 6, 40 + i * 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
              return <circle key={i} cx={x} cy={y} r={rr * g} fill="#E08A2E" opacity={0.95} />;
            })}
          </g>
          {/* tall lanky plant, right side */}
          <g transform="translate(820 1500)">
            <line x1={0} y1={0} x2={0} y2={-900 * plant} stroke={C.mocha} strokeWidth={10} strokeLinecap="round" />
            {[...Array(7)].map((_, i) => {
              const y = -120 - i * 120;
              const on = -y < 900 * plant;
              return on ? <ellipse key={i} cx={i % 2 ? 46 : -46} cy={y} rx={42} ry={16} fill="#2F7D5B" transform={`rotate(${i % 2 ? -25 : 25} ${i % 2 ? 46 : -46} ${y})`} /> : null;
            })}
            <circle cx={0} cy={-900 * plant} r={10} fill={C.cherry} opacity={plant} />
          </g>
        </svg>
        <div style={{ position: "absolute", left: 80, top: 300 }}>
          <Kicker color={C.cherry}>Nhiệm vụ ở Panama</Kicker>
          <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 92, color: C.cloud, lineHeight: 1.05, marginTop: 10, width: 640 }}>chống bệnh<br />gỉ sắt lá</div>
        </div>
        <div style={{ position: "absolute", left: 80, fontFamily: sans, fontWeight: 700, fontSize: 40, color: C.cloud, opacity: plant, top: 1260 }}>
          năng suất: <span style={{ color: C.cherry }}>thấp</span><br />chẳng ai <span style={{ color: C.cherry }}>mặn mà</span>
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: fade }}>
        <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 260, color: C.cloud, fontVariantNumeric: "tabular-nums", lineHeight: 1 }}>~{years}</div>
        <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 600, fontSize: 60, color: C.mocha }}>năm bị bỏ xó</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Scene 5: the first sip ──
const SceneTurn: React.FC<{ recordAt: number }> = ({ recordAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cup = useSpring(0, 16);
  const notes = [
    { t: "hoa nhài", c: C.jasmine, x: -250, y: -360 },
    { t: "cam bergamot", c: C.cherry, x: 230, y: -290 },
    { t: "trà Earl Grey", c: C.jade, x: -220, y: 250 },
  ];
  const stamp = spring({ frame: frame - recordAt, fps, config: { damping: 9, stiffness: 180 } });
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 48%, #3A2A20 0%, ${C.roast} 62%)`, alignItems: "center", justifyContent: "center" }}>
      <AbsoluteFill style={{ top: 230, alignItems: "center" }}>
        <Kicker color={C.mocha}>La Esmeralda · Panama</Kicker>
        <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 800, fontSize: 84, color: C.cloud, marginTop: 8 }}>ngụm đầu tiên</div>
        <div style={{ marginTop: 10, fontFamily: sans, fontWeight: 700, fontSize: 28, letterSpacing: 4, color: C.cloud, opacity: 0.7, border: `2px solid ${C.mocha}`, borderRadius: 40, padding: "6px 20px" }}>TƯƠNG TRUYỀN</div>
      </AbsoluteFill>
      <div style={{ position: "absolute", top: 900 - 260, width: 520, height: 520, borderRadius: "50%", background: C.cloud, transform: `scale(${cup})`, boxShadow: "0 50px 120px rgba(0,0,0,.6)" }}>
        <div style={{ position: "absolute", inset: 46, borderRadius: "50%", background: "radial-gradient(circle at 45% 40%, #C9823F 0%, #8A4E22 55%, #5A3115 100%)" }} />
        {[0, 1, 2].map((i) => {
          const a = (frame / 60 + i / 3) * Math.PI * 2;
          return <div key={i} style={{ position: "absolute", left: 260 + Math.cos(a) * 120 - 50, top: 260 + Math.sin(a) * 120 - 6, width: 100, height: 12, borderRadius: 6, background: "rgba(255,230,167,.35)", transform: `rotate(${(a * 180) / Math.PI + 90}deg)` }} />;
        })}
      </div>
      {notes.map((n, i) => {
        const s = spring({ frame: frame - 18 - i * 14, fps, config: { damping: 11 } });
        return (
          <div key={n.t} style={{ position: "absolute", left: 540 + n.x, top: 900 + n.y, transform: `translate(-50%,-50%) scale(${s})`, background: n.c, color: C.roast, fontFamily: sans, fontWeight: 800, fontSize: 46, padding: "14px 34px", borderRadius: 60 }}>
            {n.t}
          </div>
        );
      })}
      <div style={{ position: "absolute", top: 1270, transform: `rotate(-6deg) scale(${2 - stamp})`, opacity: Math.min(1, stamp * 1.5), border: `8px solid ${C.cherry}`, color: C.cherry, borderRadius: 18, padding: "14px 34px", textAlign: "center" }}>
        <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 70, letterSpacing: 3, lineHeight: 1 }}>2004 · KỶ LỤC</div>
        <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 30, letterSpacing: 4 }}>BEST OF PANAMA</div>
      </div>
    </AbsoluteFill>
  );
};

// ── Scene 6: payoff number ──
const ScenePayoff: React.FC = () => {
  const frame = useCurrentFrame();
  const n = Math.round(interpolate(frame, [4, 50], [21, 30204], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.exp) }));
  const sub = interpolate(frame, [50, 64], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: C.cherry, alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "absolute", top: 420 }}><Kicker color={C.roast}>08/2025 · Best of Panama</Kicker></div>
      <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 250, color: C.roast, letterSpacing: -8, fontVariantNumeric: "tabular-nums", lineHeight: 1, marginTop: -120 }}>
        ${n.toLocaleString("de-DE")}
      </div>
      <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 800, fontSize: 96, color: C.cloud, marginTop: 6 }}>cho 1 ký</div>
      <div style={{ position: "absolute", top: 1240, opacity: sub, fontFamily: sans, fontWeight: 700, fontSize: 38, color: C.roast, background: C.cloud, padding: "12px 28px", borderRadius: 14 }}>
        kỷ lục · tới giờ chưa ai phá
      </div>
    </AbsoluteFill>
  );
};

// ── Scene 7: barista math + question + loop back to the name ──
const SceneCTA: React.FC<{ qAt: number; endAt: number }> = ({ qAt, endAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = useSpring(0, 14);
  const rows = [
    { k: "liều pha", v: "15 g" },
    { k: "giá hạt", v: "$30.204 / kg" },
  ];
  const res = spring({ frame: frame - 70, fps, config: { damping: 12 } });
  const q = spring({ frame: frame - qAt, fps, config: { damping: 12 } });
  const end = spring({ frame: frame - endAt, fps, config: { damping: 14 } });
  return (
    <AbsoluteFill style={{ background: C.roast, alignItems: "center" }}>
      <div style={{ position: "absolute", top: 250, width: 860, opacity: a * (1 - end), transform: `translateY(${(1 - a) * 40}px)` }}>
        <Kicker color={C.mocha}>barista tính nhẩm</Kicker>
        {rows.map((r, i) => {
          const o = interpolate(frame, [12 + i * 18, 24 + i * 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <div key={r.k} style={{ display: "flex", justifyContent: "space-between", fontFamily: sans, fontWeight: 800, fontSize: 56, color: C.cloud, borderBottom: `3px dashed ${C.mocha}`, padding: "18px 0", opacity: o }}>
              <span style={{ color: C.mocha }}>{r.k}</span><span>{r.v}</span>
            </div>
          );
        })}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", fontFamily: sans, fontWeight: 900, color: C.cherry, padding: "22px 0", transform: `scale(${0.8 + res * 0.2})`, opacity: res }}>
          <span style={{ fontSize: 50 }}>tiền hạt / ly</span><span style={{ fontSize: 120 }}>≈ $453</span>
        </div>
      </div>
      <div style={{ position: "absolute", top: 960, width: 860, transform: `translateY(${(1 - q) * 80}px)`, opacity: q * (1 - end), background: C.cloud, borderRadius: 32, padding: "40px 48px", textAlign: "center" }}>
        <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 64, color: C.roast, lineHeight: 1.15 }}>Bạn trả tối đa bao nhiêu cho <span style={{ color: C.cherry }}>1 ly</span>?</div>
        <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 34, color: C.mocha, marginTop: 14 }}>comment 1 con số 👇</div>
      </div>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: end }}>
        <div style={{ fontFamily: serifUp, fontWeight: 900, fontSize: 170, color: C.jade, lineHeight: 1 }}>Gesha</div>
        <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 120, color: C.cherry, lineHeight: 1.1 }}>≠</div>
        <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 600, fontSize: 130, color: C.cloud, lineHeight: 1 }}>geisha</div>
        <div style={{ marginTop: 50, fontFamily: sans, fontWeight: 700, fontSize: 32, letterSpacing: 6, color: C.mocha }}>BARISTA SÍNH NGOẠI</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── TikTok-style captions: 3–4 word chunks, active word in cherry ──
const Captions: React.FC<{ words: Word[]; hideFrom: number; hideTo: number }> = ({ words, hideFrom, hideTo }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const chunks = useMemo(() => {
    const out: Word[][] = [];
    let cur: Word[] = [];
    words.forEach((w, i) => {
      cur.push(w);
      const punct = /[.,!?…:]$/.test(w.text);
      const gap = words[i + 1] ? words[i + 1].start - w.end > 0.25 : true;
      if (cur.length >= 4 || punct || gap) { out.push(cur); cur = []; }
    });
    if (cur.length) out.push(cur);
    return out;
  }, [words]);
  if (t >= hideFrom && t < hideTo) return null;
  const chunk = chunks.find((c, i) => t >= c[0].start - 0.05 && t < (chunks[i + 1] ? chunks[i + 1][0].start - 0.05 : c[c.length - 1].end + 0.6));
  if (!chunk) return null;
  const start = chunk[0].start;
  const pop = interpolate(t - start, [0, 0.12], [0.85, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ top: 1500, height: 260, alignItems: "center", justifyContent: "flex-start", paddingLeft: 60, paddingRight: 150 }}>
      <div style={{ transform: `scale(${pop})`, textAlign: "center", fontFamily: sans, fontWeight: 900, fontSize: 64, lineHeight: 1.15, color: C.cloud, textShadow: "0 4px 0 rgba(0,0,0,.55), 0 0 30px rgba(0,0,0,.6)", WebkitTextStroke: `2px ${C.roast}` }}>
        {chunk.map((w, i) => {
          const active = t >= w.start && t < w.end + 0.05;
          return <span key={i} style={{ color: active ? C.jasmine : C.cloud }}>{w.text.replace(/[,.…]$/, "")}{i < chunk.length - 1 ? " " : ""}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

export const GeishaFilm: React.FC<GeishaProps> = ({ audio, music, duration, words, beats }) => {
  const b = beats;
  const scenes: { from: number; to: number; el: React.ReactNode }[] = [
    { from: 0, to: b.myth, el: <SceneHook /> },
    { from: b.myth, to: b.map, el: <SceneMyth revealAt={f(b.reveal - b.myth)} /> },
    { from: b.map, to: b.rust, el: <SceneGlobe len={f(b.rust - b.map)} /> },
    { from: b.rust, to: b.turn, el: <SceneRust forgotAt={f(b.forgot - b.rust)} /> },
    { from: b.turn, to: b.payoff, el: <SceneTurn recordAt={f(b.record2004 - b.turn)} /> },
    { from: b.payoff, to: b.cta, el: <ScenePayoff /> },
    { from: b.cta, to: duration, el: <SceneCTA qAt={f(b.question - b.cta)} endAt={f(duration - 2.4 - b.cta)} /> },
  ];
  return (
    <AbsoluteFill style={{ background: C.roast }}>
      {scenes.map((s, i) => (
        <Sequence key={i} from={f(s.from)} durationInFrames={Math.max(1, f(s.to) - f(s.from))}>
          <SceneWipe>{s.el}</SceneWipe>
        </Sequence>
      ))}
      <Captions words={words} hideFrom={duration - 2.4} hideTo={duration + 1} />
      <Grain />
      <Audio src={staticFile(audio)} />
      {music ? <Audio src={staticFile(music)} volume={0.13} /> : null}
    </AbsoluteFill>
  );
};

// quick punch-in at every cut (TikTok pacing)
const SceneWipe: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 8], [1.06, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const o = interpolate(frame, [0, 4], [0.4, 1], { extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ transform: `scale(${s})`, opacity: o }}>{children}</AbsoluteFill>;
};
