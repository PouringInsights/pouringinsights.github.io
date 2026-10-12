// Cinematic finishing layer: grade, vignette, film grain, letterbox, light leaks, camera drift.
import React from "react";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";

export const CamDrift: React.FC<{ children: React.ReactNode; amount?: number; dir?: number }> = ({ children, amount = 0.035, dir = 1 }) => {
  const f = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = Math.min(1, f / Math.max(1, durationInFrames));
  const s = 1 + amount * Easing.inOut(Easing.sin)(t);
  const tx = dir * 14 * (t - 0.5);
  return <AbsoluteFill style={{ transform: `translateX(${tx}px) scale(${s})` }}>{children}</AbsoluteFill>;
};

export const Grade: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: "linear-gradient(135deg, rgba(0,90,130,0.16) 0%, rgba(0,0,0,0) 45%, rgba(255,150,60,0.14) 100%)", mixBlendMode: "soft-light" }} />
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(5,8,20,0.42) 100%)" }} />
  </>
);

export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.07 }) => {
  const f = useCurrentFrame();
  const i = Math.floor(f / 2) % 6;
  const ox = (f * 137) % 512;
  const oy = (f * 251) % 512;
  return (
    <AbsoluteFill
      style={{
        backgroundImage: `url(${staticFile(`kds/fx/grain${i}.png`)})`,
        backgroundSize: "512px 512px",
        backgroundPosition: `${ox}px ${oy}px`,
        opacity,
        mixBlendMode: "overlay",
        pointerEvents: "none",
      }}
    />
  );
};

/** amount 0..1 -> bars up to 2.39:1 */
export const Letterbox: React.FC<{ amount: number }> = ({ amount }) => {
  const h = 128 * amount;
  if (h <= 0.5) return null;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: h, backgroundColor: "#000" }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: h, backgroundColor: "#000" }} />
    </AbsoluteFill>
  );
};

/** warm light leak sweeping across, ~1s; mount so the peak sits on the cut */
export const LightLeak: React.FC<{ hue?: "warm" | "gold" }> = ({ hue = "warm" }) => {
  const f = useCurrentFrame();
  const k = interpolate(f, [0, 12, 30], [0, 1, 0], { extrapolateRight: "clamp" });
  const x = interpolate(f, [0, 30], [-20, 120]);
  const c1 = hue === "gold" ? "rgba(255,214,120,0.85)" : "rgba(255,150,70,0.8)";
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "screen", opacity: k }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 45% 70% at ${x}% 40%, ${c1} 0%, rgba(255,90,40,0.35) 40%, rgba(0,0,0,0) 75%)` }} />
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 20% 30% at ${x + 18}% 70%, rgba(255,240,200,0.6) 0%, rgba(0,0,0,0) 70%)` }} />
    </AbsoluteFill>
  );
};

/** Opening light sweep across a black frame */
export const LightSweep: React.FC = () => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 36], [-30, 130], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const o = interpolate(f, [0, 8, 28, 40], [0, 1, 1, 0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: o, mixBlendMode: "screen" }}>
      <AbsoluteFill style={{ background: `linear-gradient(100deg, rgba(0,0,0,0) ${x - 12}%, rgba(255,220,150,0.9) ${x}%, rgba(0,0,0,0) ${x + 12}%)` }} />
    </AbsoluteFill>
  );
};

/** Burned-in subtitles for sound-off viewing (most social video is watched muted). */
export type Cue = { from: number; to: number; text: string };
export const Captions: React.FC<{ cues: Cue[]; fps?: number }> = ({ cues, fps = 30 }) => {
  const f = useCurrentFrame();
  const t = f / fps;
  const cue = cues.find((c) => t >= c.from && t < c.to);
  if (!cue) return null;
  const o = Math.min(1, (t - cue.from) * 8, (cue.to - t) * 8);
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 30, pointerEvents: "none" }}>
      <div
        style={{
          opacity: o,
          maxWidth: 1560,
          textAlign: "center",
          fontFamily: "'Be Vietnam Pro', sans-serif",
          fontWeight: 600,
          fontSize: 38,
          lineHeight: 1.3,
          color: "#fff",
          background: "rgba(5,8,20,0.62)",
          padding: "8px 22px",
          borderRadius: 12,
          textShadow: "0 2px 6px rgba(0,0,0,0.6)",
        }}
      >
        {cue.text}
      </div>
    </AbsoluteFill>
  );
};
