// Choreography layer for the Host: walking in/out, gestures, lip-sync, and the
// "curtain" scene transition she walks across.
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, Easing } from "remotion";
import { Host, HostPose, blinkAt } from "./Host";
import ENV from "./voice_c_env.json";
import { C } from "./bkit";

const FPS = 30;
const env = ENV as number[];

export type Gesture = "idle" | "point" | "present" | "wave" | "pointUp";
export type Act = { at: number; kind: Gesture; dur?: number };

const ARM: Record<Gesture, { s: number; e: number }> = {
  idle: { s: -8, e: -10 },
  point: { s: -88, e: 4 },
  present: { s: -42, e: -48 },
  wave: { s: -150, e: 0 },
  pointUp: { s: -140, e: 10 },
};

/** Mouth openness from the narration envelope at an absolute (video) frame. */
export const mouthAt = (absFrame: number) => {
  const v = env[Math.max(0, Math.min(env.length - 1, absFrame))] ?? 0;
  return v > 0.12 ? Math.min(1, 0.2 + v * 0.8) : 0;
};

export const HostActor: React.FC<{
  /** absolute start (seconds) of the enclosing Sequence, for lip-sync */
  sceneStart: number;
  /** walk-in: [t0, t1] local seconds, from xFrom to x */
  walkIn?: [number, number];
  xFrom?: number;
  x: number;
  y?: number;
  height?: number;
  /** walk-out: [t0, t1] to xTo */
  walkOut?: [number, number];
  xTo?: number;
  acts?: Act[];
  /** mirror the character (faces / points left) */
  flip?: boolean;
  tablet?: boolean;
  talk?: boolean;
}> = ({
  sceneStart,
  walkIn,
  xFrom,
  x,
  y = 300,
  height = 700,
  walkOut,
  xTo,
  acts = [],
  flip = false,
  tablet = true,
  talk = true,
}) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  let px = x;
  let walking = false;
  if (walkIn && t < walkIn[1]) {
    px = interpolate(t, walkIn, [xFrom ?? -400, x], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.quad),
    });
    walking = t >= walkIn[0];
  }
  if (walkOut && t >= walkOut[0]) {
    px = interpolate(t, walkOut, [x, xTo ?? 2200], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.in(Easing.quad),
    });
    walking = true;
  }
  // gesture blending
  let s = ARM.idle.s;
  let e = ARM.idle.e;
  let tilt = 0;
  for (const a of acts) {
    const dur = a.dur ?? 1.6;
    const k = interpolate(t, [a.at, a.at + 0.25, a.at + dur - 0.25, a.at + dur], [0, 1, 1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    if (k <= 0) continue;
    const g = ARM[a.kind];
    let ge = g.e;
    if (a.kind === "wave") ge = Math.sin(f * 0.5) * 24;
    s = s + (g.s - s) * k;
    e = e + (ge - e) * k;
    if (a.kind === "wave" || a.kind === "present") tilt = 5 * k;
  }
  const pose: HostPose = walking
    ? { walk: t * 9, tablet, blink: blinkAt(f) }
    : {
        rShoulder: s,
        rElbow: e,
        lShoulder: tablet ? 18 : 8,
        lElbow: tablet ? 70 : 10,
        tablet,
        blink: blinkAt(f),
        tilt,
        bob: Math.sin(f / 14) * 2,
      };
  pose.mouth = talk && !walking ? mouthAt(Math.round((sceneStart + t) * FPS)) : 0;
  return (
    <div style={{ position: "absolute", left: px, top: y }}>
      <Host pose={pose} height={height} flip={walking ? (walkOut ? false : flip) : flip} />
    </div>
  );
};

/**
 * Curtain transition: a navy panel follows the host across the frame from
 * right to left. Place it so frame 0 is ~0.6s before the cut.
 */
export const HostSweep: React.FC<{ color?: string; accent?: string }> = ({
  color = C.navy,
  accent = C.yellow,
}) => {
  const f = useCurrentFrame();
  // frames 0..24: host walks right->left, panel trails behind her.
  // frame 24 (= the cut): panel covers the frame. 24..36: panel slides off left.
  const hx = interpolate(f, [0, 24], [1980, -620], { extrapolateRight: "clamp" });
  const out = interpolate(f, [24, 36], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.in(Easing.cubic),
  });
  const leftEdge = f < 24 ? Math.max(0, hx + 200) : -1920 * out;
  const rightEdge = f < 24 ? 1920 : 1920 - 1920 * out;
  const cover = 1;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: Math.min(leftEdge, rightEdge),
          width: Math.max(0, rightEdge - leftEdge),
          backgroundColor: color,
          opacity: cover > 0 ? 1 : 0,
          boxShadow: `-14px 0 0 ${accent}`,
        }}
      />
      <div style={{ position: "absolute", left: hx, top: 300 }}>
        <Host pose={{ walk: f * 0.3, tablet: true }} height={700} flip />
      </div>
    </AbsoluteFill>
  );
};
