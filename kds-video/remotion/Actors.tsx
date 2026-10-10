// Choreography helpers for the chibi cast + small illustrated set pieces.
import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, Easing } from "remotion";
import { Chibi } from "./Chibi";
import { blink, Prop, Variant, PersonPose } from "./Cast";
import { C, FONT } from "./bkit";

const FPS = 30;

export type Gest = "idle" | "wave" | "point" | "present" | "cheer" | "holdFront" | "megaphone" | "raise" | "hands";
export type ActC = { at: number; kind: Gest; dur?: number };

const POSES: Record<Gest, Partial<PersonPose>> = {
  idle: {},
  wave: { rS: 125, rE: 0 },
  point: { rS: 82, rE: 4 },
  present: { rS: 40, rE: 55 },
  cheer: { rS: 155, rE: 0, lS: 155, lE: 0 },
  holdFront: { rS: 22, rE: 75, lS: 22, lE: 75 },
  megaphone: { rS: 55, rE: 70 },
  raise: { rS: 160, rE: -10 },
  hands: { rS: 35, rE: 60, lS: 35, lE: 60 },
};

const mix = (a: number | undefined, b: number | undefined, k: number, base: number) =>
  (a ?? base) + ((b ?? base) - (a ?? base)) * k;

export const Actor: React.FC<{
  v: Variant;
  x: number;
  y: number;
  height?: number;
  walkIn?: [number, number];
  xFrom?: number;
  walkOut?: [number, number];
  xTo?: number;
  acts?: ActC[];
  base?: Gest;
  rHold?: Prop;
  lHold?: Prop;
  flip?: boolean;
  seed?: number;
  /** pop in (scale) at this local second instead of walking */
  popAt?: number;
  hop?: boolean;
}> = ({ v, x, y, height = 420, walkIn, xFrom, walkOut, xTo, acts = [], base = "idle", rHold, lHold, flip, seed = 0, popAt, hop }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  let px = x;
  let walking = false;
  if (walkIn && t < walkIn[1]) {
    px = interpolate(t, walkIn, [xFrom ?? -400, x], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) });
    walking = t >= walkIn[0];
  }
  if (walkOut && t >= walkOut[0]) {
    px = interpolate(t, walkOut, [x, xTo ?? 2300], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.quad) });
    walking = true;
  }
  const b = POSES[base];
  let pose: PersonPose = { ...b };
  for (const a of acts) {
    const dur = a.dur ?? 1.6;
    const k = interpolate(t, [a.at, a.at + 0.22, a.at + dur - 0.22, a.at + dur], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    if (k <= 0) continue;
    const g = POSES[a.kind];
    pose = {
      rS: mix(pose.rS, g.rS, k, 10),
      rE: mix(pose.rE, a.kind === "wave" ? Math.sin(f * 0.5) * 24 : g.rE, k, 6),
      lS: mix(pose.lS, g.lS, k, 10),
      lE: mix(pose.lE, g.lE, k, 6),
      tilt: (a.kind === "wave" || a.kind === "cheer" ? 5 : 0) * k,
      bob: a.kind === "cheer" ? -Math.abs(Math.sin(f * 0.35)) * 16 * k : 0,
    };
  }
  const p: PersonPose = walking
    ? { walk: t * 10, blink: blink(f, seed), rHold, lHold }
    : { ...pose, blink: blink(f, seed), rHold, lHold, bob: (pose.bob ?? 0) + Math.sin(f / 15 + seed) * 2 + (hop ? -Math.abs(Math.sin(f * 0.3)) * 14 : 0) };
  const sc = popAt === undefined ? 1 : spring({ frame: f - Math.round(popAt * FPS), fps: FPS, config: { damping: 11, stiffness: 140, mass: 0.7 } });
  const facing = walking ? (walkOut ? (xTo ?? 2300) < x : (xFrom ?? -400) > x) : flip;
  return (
    <div style={{ position: "absolute", left: px, top: y, transform: `scale(${sc})`, transformOrigin: "50% 100%", opacity: popAt === undefined ? 1 : Math.min(1, sc * 2) }}>
      <Chibi v={v} pose={p} height={height} flip={facing} />
    </div>
  );
};

// ---------------------------------------------------------------------------
// Set pieces
// ---------------------------------------------------------------------------
/** Flat illustration of the School of Economics building with its sign. */
export const SchoolGate: React.FC<{ reveal?: number }> = ({ reveal = 1 }) => (
  <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: "absolute" }}>
    <defs>
      <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#BFE0FF" />
        <stop offset="1" stopColor="#EAF5FF" />
      </linearGradient>
    </defs>
    <rect width={1920} height={1080} fill="url(#sky)" />
    <circle cx={1660} cy={170} r={70} fill="#FFE08A" opacity={0.9} />
    {[[220, 160, 1], [760, 110, 0.8], [1300, 190, 1.1]].map(([cx, cy, s], i) => (
      <g key={i} transform={`translate(${cx} ${cy}) scale(${s})`} opacity={0.9}>
        <ellipse cx={0} cy={0} rx={80} ry={30} fill="#fff" />
        <ellipse cx={50} cy={-16} rx={50} ry={30} fill="#fff" />
        <ellipse cx={-40} cy={-10} rx={44} ry={26} fill="#fff" />
      </g>
    ))}
    <g transform={`translate(0 ${(1 - reveal) * 300})`}>
      {/* building */}
      <rect x={260} y={300} width={1400} height={560} fill="#F6D776" />
      <rect x={260} y={300} width={1400} height={40} fill="#E9C15A" />
      {Array.from({ length: 3 }).map((_, r) =>
        Array.from({ length: 10 }).map((__, c) => (
          <rect key={`${r}-${c}`} x={310 + c * 134} y={370 + r * 120} width={70} height={80} rx={6} fill={c === 4 || c === 5 ? "#7FB4E6" : "#FFF4D4"} stroke="#D9AE4B" strokeWidth={4} />
        )),
      )}
      {/* green vines */}
      {Array.from({ length: 9 }).map((_, i) => (
        <path key={i} d={`M${330 + i * 150} 340 q 10 60 -6 120 q 14 50 0 90`} stroke="#5FA968" strokeWidth={10} fill="none" strokeLinecap="round" opacity={0.75} />
      ))}
      {/* sign */}
      <rect x={720} y={630} width={480} height={110} rx={10} fill="#1F47C8" stroke="#163495" strokeWidth={6} />
      <text x={960} y={672} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={22} fill="#fff">ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI</text>
      <text x={960} y={716} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={44} fill="#FFC93C">TRƯỜNG KINH TẾ</text>
      {/* columns + entrance */}
      <rect x={830} y={740} width={260} height={120} fill="#3C4A7A" />
      <rect x={780} y={620} width={34} height={240} fill="#FFFFFF" />
      <rect x={1106} y={620} width={34} height={240} fill="#FFFFFF" />
    </g>
    {/* ground */}
    <rect x={0} y={860} width={1920} height={220} fill="#D9DEE8" />
    <rect x={0} y={860} width={1920} height={14} fill="#C3C9D6" />
    {Array.from({ length: 14 }).map((_, i) => (
      <rect key={i} x={i * 150} y={940} width={90} height={8} rx={4} fill="#C8CEDA" />
    ))}
    {/* trees */}
    {[150, 1770].map((x, i) => (
      <g key={i}>
        <rect x={x - 14} y={640} width={28} height={230} fill="#8A6A4A" />
        <circle cx={x} cy={600} r={110} fill="#6FB678" />
        <circle cx={x - 60} cy={650} r={70} fill="#5FA968" />
        <circle cx={x + 60} cy={650} r={70} fill="#7CC285" />
      </g>
    ))}
  </svg>
);

export const Whiteboard: React.FC<{ progress: number }> = ({ progress }) => (
  <svg width={760} height={480} viewBox="0 0 760 480" style={{ overflow: "visible" }}>
    <rect x={10} y={10} width={740} height={420} rx={18} fill="#FFFFFF" stroke="#2F3B66" strokeWidth={14} />
    <rect x={250} y={430} width={260} height={16} rx={6} fill="#2F3B66" />
    <path d={`M70 340 L200 250 L320 290 L470 150 L640 110`} stroke="#1F47E0" strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={800} strokeDashoffset={800 * (1 - progress)} />
    {[110, 220, 330, 440, 560].map((x, i) => (
      <rect key={i} x={x} y={380 - (60 + i * 40) * Math.min(1, progress * 1.5)} width={46} height={(60 + i * 40) * Math.min(1, progress * 1.5)} rx={6} fill={i % 2 ? "#FFC93C" : "#7DB2FF"} opacity={0.85} />
    ))}
    <text x={60} y={80} fontFamily={FONT} fontWeight={800} fontSize={38} fill="#2F3B66" opacity={Math.min(1, progress * 3)}>Kinh doanh số 101</text>
  </svg>
);

export const Bulb: React.FC<{ at: number }> = ({ at }) => {
  const f = useCurrentFrame();
  const p = spring({ frame: f - Math.round(at * FPS), fps: FPS, config: { damping: 9, stiffness: 160 } });
  const glow = 0.4 + 0.3 * Math.sin(f / 5);
  return (
    <svg width={140} height={170} viewBox="0 0 140 170" style={{ transform: `scale(${p})`, transformOrigin: "50% 100%", overflow: "visible" }}>
      <circle cx={70} cy={66} r={70} fill="#FFE27A" opacity={glow * p} />
      <path d="M70 18 C30 18 20 56 34 80 C44 96 50 104 50 120 L90 120 C90 104 96 96 106 80 C120 56 110 18 70 18 Z" fill="#FFD93D" stroke="#3B2A33" strokeWidth={6} />
      <rect x={50} y={120} width={40} height={28} rx={6} fill="#9AA3B8" stroke="#3B2A33" strokeWidth={6} />
    </svg>
  );
};

export const Bubble: React.FC<{ text: string; at: number; done?: number; color?: string }> = ({ text, at, done, color = C.white }) => {
  const f = useCurrentFrame();
  const p = spring({ frame: f - Math.round(at * FPS), fps: FPS, config: { damping: 10, stiffness: 160 } });
  const d = done === undefined ? 0 : spring({ frame: f - Math.round(done * FPS), fps: FPS, config: { damping: 10, stiffness: 160 } });
  return (
    <div style={{ transform: `scale(${p})`, transformOrigin: "50% 100%", position: "relative" }}>
      <div style={{ background: d > 0.5 ? C.yellow : color, borderRadius: 30, padding: "16px 26px", fontFamily: FONT, fontWeight: 800, fontSize: 34, color: C.navy, boxShadow: "0 10px 24px rgba(0,0,0,0.25)", whiteSpace: "nowrap" }}>
        {d > 0.5 ? "✓ " : ""}
        {text}
      </div>
      <div style={{ position: "absolute", left: "50%", bottom: -16, width: 0, height: 0, borderLeft: "14px solid transparent", borderRight: "14px solid transparent", borderTop: `18px solid ${d > 0.5 ? C.yellow : color}`, transform: "translateX(-50%)" }} />
    </div>
  );
};

export const Trophy: React.FC<{ size?: number }> = ({ size = 140 }) => (
  <svg width={size} height={size} viewBox="0 0 140 140">
    <path d="M40 20 L100 20 L96 70 Q70 92 44 70 Z" fill="#FFC93C" stroke="#3B2A33" strokeWidth={6} strokeLinejoin="round" />
    <path d="M40 30 Q14 30 20 52 Q26 66 44 66 M100 30 Q126 30 120 52 Q114 66 96 66" stroke="#3B2A33" strokeWidth={6} fill="none" />
    <rect x={60} y={84} width={20} height={20} fill="#E2A92A" stroke="#3B2A33" strokeWidth={5} />
    <rect x={40} y={104} width={60} height={18} rx={4} fill="#1F3488" stroke="#3B2A33" strokeWidth={5} />
  </svg>
);

/** Curtain transition led by a running chibi (frame 24 = the cut). */
export const ChibiSweep: React.FC<{ v?: Variant }> = ({ v = "ponytail" }) => {
  const f = useCurrentFrame();
  const hx = interpolate(f, [0, 24], [1980, -520], { extrapolateRight: "clamp" });
  const out = interpolate(f, [24, 36], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const leftEdge = f < 24 ? Math.max(0, hx + 180) : -1920 * out;
  const rightEdge = f < 24 ? 1920 : 1920 - 1920 * out;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", top: 0, bottom: 0, left: Math.min(leftEdge, rightEdge), width: Math.max(0, rightEdge - leftEdge), backgroundColor: C.navy, boxShadow: `-14px 0 0 ${C.yellow}` }} />
      {f < 26 ? (
        <div style={{ position: "absolute", left: hx, top: 430 }}>
          <Chibi v={v} pose={{ walk: f * 0.55, rS: 70, rE: 40, lS: 30, lE: 20 }} height={520} flip />
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
