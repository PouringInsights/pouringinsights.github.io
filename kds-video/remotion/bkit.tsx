// Shared motion-graphics kit for Version B.
import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { FPS, sec } from "./common";

export const C = {
  navy: "#0A1A4A",
  navy2: "#11286B",
  blue: "#1F47E0",
  sky: "#7DB2FF",
  yellow: "#FFC93C",
  coral: "#FF6B4A",
  cream: "#FFF8EC",
  white: "#FFFFFF",
  ink: "#0B1433",
};
export const FONT = "'Be Vietnam Pro', sans-serif";

// ---------------------------------------------------------------------------
// Narration plan: each segment of the v1 voice and where it lands in Version B.
// bt(id, t) converts a v1 timestamp (word timing) into Version B seconds.
// ---------------------------------------------------------------------------
export const SEGS: Record<string, { src: number; at: number; dur: number }> = {
  name: { src: 11.0, at: 3.6, dur: 3.065 },
  found: { src: 20.2, at: 7.565, dur: 10.22 },
  majors: { src: 30.915, at: 18.385, dur: 5.105 },
  faculty: { src: 49.45, at: 24.49, dur: 9.77 },
  learn: { src: 65.8, at: 35.16, dur: 6.4 },
  research: { src: 76.7, at: 42.46, dur: 8.45 },
  life: { src: 93.66, at: 51.91, dur: 5.96 },
  logi: { src: 99.8, at: 58.77, dur: 8.28 },
  mj: { src: 122.5, at: 67.85, dur: 8.9 },
  partners: { src: 141.66, at: 77.75, dur: 11.64 },
  questions: { src: 153.72, at: 90.19, dur: 11.14 },
  outcomes: { src: 164.86, at: 101.83, dur: 5.78 },
  outro: { src: 187.3, at: 108.81, dur: 6.6 },
};
export const B_TOTAL = 119.91;
export const bt = (id: keyof typeof SEGS, t: number) =>
  SEGS[id].at + (t - SEGS[id].src);

// Frame helpers relative to a scene that starts at `scene0` (B seconds).
export const useT = () => useCurrentFrame() / FPS;

export const pop = (frame: number, at: number, fps = FPS, damping = 12) =>
  spring({
    frame: frame - Math.round(at * fps),
    fps,
    config: { damping, stiffness: 140, mass: 0.7 },
  });

export const ease = (frame: number, a: number, b: number) =>
  interpolate(frame, [Math.round(a * FPS), Math.round(b * FPS)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });

// ---------------------------------------------------------------------------
// Backgrounds
// ---------------------------------------------------------------------------
export const Bg: React.FC<{ tone?: "navy" | "cream" | "blue" }> = ({
  tone = "navy",
}) => {
  const f = useCurrentFrame();
  const base = tone === "navy" ? C.navy : tone === "blue" ? C.blue : C.cream;
  const blobA = tone === "cream" ? "rgba(31,71,224,0.10)" : "rgba(125,178,255,0.22)";
  const blobB = tone === "cream" ? "rgba(255,201,60,0.22)" : "rgba(255,107,74,0.18)";
  const dot = tone === "cream" ? "rgba(10,26,74,0.10)" : "rgba(255,255,255,0.07)";
  const x1 = 30 + 8 * Math.sin(f / 90);
  const y1 = 30 + 6 * Math.cos(f / 110);
  const x2 = 75 + 7 * Math.cos(f / 100);
  const y2 = 72 + 8 * Math.sin(f / 80);
  return (
    <AbsoluteFill style={{ backgroundColor: base, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at ${x1}% ${y1}%, ${blobA} 0, transparent 38%), radial-gradient(circle at ${x2}% ${y2}%, ${blobB} 0, transparent 34%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage: `radial-gradient(${dot} 2px, transparent 2px)`,
          backgroundSize: "36px 36px",
          backgroundPosition: `${(f * 0.4) % 36}px ${(f * 0.25) % 36}px`,
        }}
      />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Media
// ---------------------------------------------------------------------------
export const KImg: React.FC<{
  src: string;
  style?: React.CSSProperties;
  zoom?: number; // total zoom over the life of the element
  pos?: string;
}> = ({ src, style, zoom = 0.08, pos = "50% 50%" }) => {
  const f = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const s = 1.02 + zoom * (f / Math.max(durationInFrames, 1));
  const isVid = src.endsWith(".mp4");
  const common: React.CSSProperties = {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    objectPosition: pos,
    transform: `scale(${s})`,
  };
  return (
    <div style={{ overflow: "hidden", ...style }}>
      {isVid ? (
        <OffthreadVideo src={staticFile(`kds/${src}`)} muted style={common} />
      ) : (
        <Img src={staticFile(`kds/${src}`)} style={common} />
      )}
    </div>
  );
};

/** Rounded photo card that springs in at `at` (scene seconds). */
export const PhotoCard: React.FC<{
  src: string;
  at: number;
  x: number;
  y: number;
  w: number;
  h: number;
  rot?: number;
  from?: "left" | "right" | "up" | "down" | "scale";
  pos?: string;
  border?: string;
}> = ({ src, at, x, y, w, h, rot = 0, from = "scale", pos, border = C.white }) => {
  const f = useCurrentFrame();
  const p = pop(f, at, FPS, 14);
  const off = (1 - p) * 220;
  const tx = from === "left" ? -off : from === "right" ? off : 0;
  const ty = from === "up" ? -off : from === "down" ? off : 0;
  const sc = from === "scale" ? 0.6 + 0.4 * p : 1;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        opacity: Math.min(1, p * 1.6),
        transform: `translate(${tx}px, ${ty}px) rotate(${rot * p}deg) scale(${sc})`,
        borderRadius: 28,
        border: `10px solid ${border}`,
        boxShadow: "0 30px 60px rgba(0,0,0,0.35)",
        overflow: "hidden",
        backgroundColor: "#222",
      }}
    >
      <KImg src={src} style={{ width: "100%", height: "100%" }} pos={pos} />
    </div>
  );
};

// ---------------------------------------------------------------------------
// Type
// ---------------------------------------------------------------------------
/** Text that rises in word by word, starting at `at`. */
export const Rise: React.FC<{
  text: string;
  at: number;
  size: number;
  color?: string;
  weight?: number;
  stagger?: number;
  style?: React.CSSProperties;
  highlight?: string[]; // words to paint in accent
  accent?: string;
}> = ({
  text,
  at,
  size,
  color = C.white,
  weight = 800,
  stagger = 0.06,
  style,
  highlight = [],
  accent = C.yellow,
}) => {
  const f = useCurrentFrame();
  const words = text.split(" ");
  return (
    <div
      style={{
        fontFamily: FONT,
        fontWeight: weight,
        fontSize: size,
        lineHeight: 1.12,
        color,
        letterSpacing: -0.5,
        ...style,
      }}
    >
      {words.map((w, i) => {
        const p = pop(f, at + i * stagger, FPS, 15);
        const hl = highlight.includes(w.replace(/[.,?!:]/g, ""));
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              marginRight: size * 0.26,
              opacity: Math.min(1, p * 1.5),
              transform: `translateY(${(1 - p) * size * 0.6}px)`,
              color: hl ? accent : undefined,
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  );
};

export const Tag: React.FC<{
  text: string;
  at: number;
  bg?: string;
  color?: string;
  size?: number;
  style?: React.CSSProperties;
}> = ({ text, at, bg = C.yellow, color = C.ink, size = 40, style }) => {
  const f = useCurrentFrame();
  const p = pop(f, at, FPS, 10);
  return (
    <div
      style={{
        display: "inline-block",
        fontFamily: FONT,
        fontWeight: 800,
        fontSize: size,
        color,
        backgroundColor: bg,
        padding: `${size * 0.3}px ${size * 0.6}px`,
        borderRadius: size,
        transform: `scale(${p}) rotate(${(1 - p) * -8}deg)`,
        opacity: Math.min(1, p * 2),
        boxShadow: "0 10px 24px rgba(0,0,0,0.25)",
        whiteSpace: "nowrap",
        ...style,
      }}
    >
      {text}
    </div>
  );
};

/** Number that counts up from 0 starting at `at`. */
export const Counter: React.FC<{
  to: number;
  at: number;
  dur?: number;
  size: number;
  color?: string;
  prefix?: string;
  suffix?: string;
  thousands?: boolean;
}> = ({ to, at, dur = 1.0, size, color = C.white, prefix = "", suffix = "", thousands }) => {
  const f = useCurrentFrame();
  const k = ease(f, at, at + dur);
  const p = pop(f, at, FPS, 12);
  const n = Math.round(to * k);
  const s = thousands ? n.toLocaleString("de-DE") : String(n);
  return (
    <span
      style={{
        fontFamily: FONT,
        fontWeight: 900,
        fontSize: size,
        color,
        lineHeight: 1,
        display: "inline-block",
        transform: `scale(${0.7 + 0.3 * p})`,
        opacity: Math.min(1, p * 2),
        letterSpacing: -2,
        fontVariantNumeric: "tabular-nums",
      }}
    >
      {prefix}
      {s}
      {suffix}
    </span>
  );
};

// ---------------------------------------------------------------------------
// Transitions + sound
// ---------------------------------------------------------------------------
/** Diagonal colour wipe that covers the cut at the very end/start of scenes. */
export const Wipe: React.FC<{ color?: string; color2?: string }> = ({
  color = C.yellow,
  color2 = C.blue,
}) => {
  const f = useCurrentFrame();
  // 0..14 frames: panel sweeps across left->right
  const a = interpolate(f, [0, 7, 14], [-130, 0, 130], {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const b = interpolate(f, [2, 9, 16], [-130, 0, 130], {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill
        style={{
          backgroundColor: color2,
          transform: `translateX(${b}%) skewX(-12deg) scaleX(1.3)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundColor: color,
          transform: `translateX(${a}%) skewX(-12deg) scaleX(1.3)`,
        }}
      />
    </AbsoluteFill>
  );
};

export const Sfx: React.FC<{ at: number; name: string; vol?: number }> = ({
  at,
  name,
  vol = 0.3,
}) => (
  <Sequence from={Math.max(0, sec(at))} durationInFrames={sec(2.5)} layout="none">
    <Audio src={staticFile(`kds/sfx/${name}.mp3`)} volume={vol} />
  </Sequence>
);

// Simple line icons (stroke follows `color`)
export const Icon: React.FC<{
  kind: "megaphone" | "truck" | "chart";
  size: number;
  color: string;
  progress: number; // 0..1 drives internal animation
}> = ({ kind, size, color, progress }) => {
  const sw = 5;
  if (kind === "megaphone") {
    const w = (i: number) => Math.max(0, Math.min(1, progress * 3 - i));
    return (
      <svg width={size} height={size} viewBox="0 0 100 100" fill="none" stroke={color} strokeWidth={sw} strokeLinejoin="round" strokeLinecap="round">
        <path d="M18 42 L18 58 L32 58 L60 74 L60 26 L32 42 Z" />
        <path d="M32 58 L38 80 L48 80 L44 62" />
        {[0, 1, 2].map((i) => (
          <path key={i} d={`M${68 + i * 9} ${38 - i * 6} Q ${76 + i * 11} 50 ${68 + i * 9} ${62 + i * 6}`} opacity={w(i)} />
        ))}
      </svg>
    );
  }
  if (kind === "truck") {
    const dx = (1 - Math.min(1, progress)) * -30;
    const spin = progress * 720;
    return (
      <svg width={size} height={size} viewBox="0 0 100 100" fill="none" stroke={color} strokeWidth={sw} strokeLinejoin="round" strokeLinecap="round">
        <g transform={`translate(${dx},0)`}>
          <rect x="10" y="30" width="48" height="34" rx="3" />
          <path d="M58 42 L76 42 L88 54 L88 64 L58 64" />
          <g transform={`rotate(${spin} 28 68)`}><circle cx="28" cy="68" r="8" fill="none" /><path d="M28 62 L28 74" /></g>
          <g transform={`rotate(${spin} 74 68)`}><circle cx="74" cy="68" r="8" fill="none" /><path d="M74 62 L74 74" /></g>
        </g>
        <path d="M6 82 L94 82" opacity={0.5} />
      </svg>
    );
  }
  const hs = [0.45, 0.7, 0.55, 0.9];
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none" stroke={color} strokeWidth={sw} strokeLinejoin="round" strokeLinecap="round">
      <path d="M12 86 L90 86" />
      {hs.map((h, i) => {
        const hh = 62 * h * Math.min(1, Math.max(0, progress * 2 - i * 0.25));
        return <rect key={i} x={18 + i * 18} y={86 - hh} width="10" height={hh} rx="2" />;
      })}
      <path
        d={`M18 ${70} L36 ${52} L54 ${60} L80 ${28}`}
        strokeDasharray="120"
        strokeDashoffset={120 * (1 - Math.min(1, Math.max(0, progress * 1.5 - 0.5)))}
        stroke={C.yellow}
      />
    </svg>
  );
};

export { FPS, sec };
