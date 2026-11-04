import React, { useMemo } from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import "./fonts.css";

export type Word = { text: string; start: number; end: number };
export const FPS = 30;
export const f = (s: number) => Math.round(s * FPS);
export const EXPO = Easing.bezier(0.16, 1, 0.3, 1);
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const ramp = (frame: number, a: number, b: number) => interpolate(frame, [a, b], [0, 1], { ...clamp, easing: EXPO });

export const sans = "'Be Vietnam Pro'";

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

// ── Watercolour engine ──────────────────────────────────────────────
// A wash = a shape pushed through turbulence (wobbly bleed edge), edge-darkened
// (pigment pools at the rim) and granulated (pigment settles into paper tooth).
export const WashFilter: React.FC<{ id: string; seed: number; distort?: number; body?: number; rim?: number; grainFreq?: number }> = ({ id, seed, distort = 70, body = 0.6, rim = 0.85, grainFreq = 0.55 }) => (
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

type WashProps = { id: string; seed: number; color: string; cx: number; cy: number; r: number; p: number; body?: number; rim?: number; distort?: number; blend?: "multiply" | "normal" };
export const Wash: React.FC<WashProps> = ({ id, seed, color, cx, cy, r, p, body, rim, distort, blend = "multiply" }) => (
  <g style={{ mixBlendMode: blend }}>
    <defs><WashFilter id={id} seed={seed} body={body} rim={rim} distort={distort} /></defs>
    <circle cx={cx} cy={cy} r={Math.max(0.1, r * p)} fill={color} filter={`url(#${id})`} />
  </g>
);

// a full-bleed field that blooms from a point (the signature move)
export const Field: React.FC<{ id: string; color: string; ox?: number; oy?: number; at?: number; seed?: number }> = ({ id, color, ox = 540, oy = 960, at = 0, seed = 3 }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - at, [0, 22], [0, 1], { ...clamp, easing: Easing.bezier(0.3, 0.7, 0.2, 1) });
  if (p <= 0) return null;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <Wash id={id} seed={seed} color={color} cx={ox} cy={oy} r={2300} p={p} body={1} rim={0.2} distort={160} />
    </svg>
  );
};

export const Paper: React.FC = () => (
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

export const T: React.FC<{ size: number; color: string; weight?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ size, color, weight = 800, style, children }) => (
  <div style={{ fontFamily: sans, fontWeight: weight, fontSize: size, color, lineHeight: 1.08, letterSpacing: size > 120 ? -size * 0.03 : 0, fontVariantNumeric: "tabular-nums", ...style }}>{children}</div>
);

export const Rise: React.FC<{ at?: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ at = 0, children, style }) => {
  const frame = useCurrentFrame();
  const p = ramp(frame, at, at + 14);
  return <div style={{ opacity: p, transform: `translateY(${(1 - p) * 24}px)`, ...style }}>{children}</div>;
};

// ── Captions: 2–4 word chunks, paper type with an ink outline, active word in Hansa yellow ──
export const Captions: React.FC<{ words: Word[]; hideFrom: number }> = ({ words, hideFrom }) => {
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

