import React, { useEffect, useState } from "react";
import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  Sequence,
  continueRender,
  delayRender,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { FONT_CSS } from "./fonts";
import DIMS from "./dims.json";

/** true when an image is not ~16:9 and would be cropped by a cover fit */
export const needsContain = (src: string) => {
  const d = (DIMS as Record<string, number[]>)[src];
  if (!d) return false;
  return Math.abs(d[0] / d[1] - 16 / 9) > 0.06;
};

export const FPS = 30;
export const sec = (s: number) => Math.round(s * FPS);

/** Injects local @font-face rules and blocks rendering until the fonts are ready. */
export const Fonts: React.FC = () => {
  const [handle] = useState(() => delayRender("kds-fonts"));
  useEffect(() => {
    const loads = [
      "400 20px 'Be Vietnam Pro'",
      "600 20px 'Be Vietnam Pro'",
      "800 20px 'Be Vietnam Pro'",
      "900 20px 'Be Vietnam Pro'",
      "400 20px 'Newsreader'",
      "italic 400 20px 'Newsreader'",
    ].map((f) => document.fonts.load(f, "Kinh doanh số ệ ữ ượ"));
    Promise.all(loads)
      .then(() => document.fonts.ready)
      .then(() => continueRender(handle))
      .catch(() => continueRender(handle));
  }, [handle]);
  return <style>{FONT_CSS}</style>;
};

export type Media = {
  src: string; // path under public/kds
  kind: "img" | "video";
  portrait?: boolean; // show contained over a blurred fill
  startFrom?: number; // seconds into the clip
  zoom?: "in" | "out";
  pan?: "left" | "right" | "up" | "none";
  focusY?: number; // object-position Y in % for cover crops
  still?: boolean; // no Ken Burns scale/pan
  autoFit?: boolean; // contain (with blurred fill) whenever a cover fit would crop
  inset?: number; // keep the whole picture inside a letterboxed band (px top & bottom)
};

/** One still or clip filling the frame, with a slow Ken Burns move. */
export const MediaFill: React.FC<{ m: Media; dur: number }> = ({ m, dur }) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [0, Math.max(dur, 1)], [0, 1], {
    extrapolateRight: "clamp",
  });
  const zoomIn = m.zoom !== "out";
  const scale = m.still ? 1 : zoomIn ? 1.04 + 0.08 * t : 1.12 - 0.08 * t;
  const panPx = m.still ? 0 : 40 * (t - 0.5);
  if (m.autoFit && m.kind === "img" && needsContain(m.src)) m = { ...m, portrait: true };
  if (m.inset) m = { ...m, portrait: true };
  const inset = m.inset ?? 0;
  const tx = m.pan === "left" ? -panPx : m.pan === "right" ? panPx : 0;
  const ty = m.pan === "up" ? -panPx : 0;
  const src = staticFile(`kds/${m.src}`);
  const objPos = `50% ${m.focusY ?? 50}%`;

  const body =
    m.kind === "img" ? (
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: m.portrait ? "contain" : "cover",
          objectPosition: objPos,
        }}
      />
    ) : (
      <OffthreadVideo
        src={src}
        muted
        startFrom={sec(m.startFrom ?? 0)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: m.portrait ? "contain" : "cover",
          objectPosition: objPos,
        }}
      />
    );

  return (
    <AbsoluteFill style={{ backgroundColor: "#111", overflow: "hidden" }}>
      {m.portrait && m.kind === "img" ? (
        <Img
          src={src}
          style={{
            position: "absolute",
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: "blur(40px) brightness(0.55) saturate(1.1)",
            transform: "scale(1.2)",
          }}
        />
      ) : null}
      <AbsoluteFill
        style={{ transform: `translate(${tx}px, ${ty}px) scale(${scale})`, top: inset, bottom: inset, height: "auto" }}
      >
        {body}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export type Shot = { m: Media; from: number; to: number }; // absolute seconds

/**
 * A run of shots that sits on top of the base layer. Fades the whole run in
 * and out, and cross-dissolves between shots.
 */
export const ShotRun: React.FC<{
  shots: Shot[];
  edgeFade?: number;
  xfade?: number;
  vignette?: boolean;
}> = ({ shots, edgeFade = 8, xfade = 5, vignette = true }) => {
  const frame = useCurrentFrame();
  const start = shots[0].from;
  const total = sec(shots[shots.length - 1].to - start);
  const opacity = interpolate(
    frame,
    [0, edgeFade, total - edgeFade, total],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  return (
    <AbsoluteFill style={{ opacity }}>
      {shots.map((s, i) => {
        const from = sec(s.from - start);
        const dur = sec(s.to - s.from) + (i < shots.length - 1 ? xfade : 0);
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <XFadeIn frames={i === 0 ? 0 : xfade}>
              <MediaFill m={s.m} dur={dur} />
            </XFadeIn>
          </Sequence>
        );
      })}
      {vignette ? (
        <AbsoluteFill
          style={{
            background:
              "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.35) 100%)",
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};

const XFadeIn: React.FC<{ frames: number; children: React.ReactNode }> = ({
  frames,
  children,
}) => {
  const frame = useCurrentFrame();
  const o =
    frames <= 0
      ? 1
      : interpolate(frame, [0, frames], [0, 1], {
          extrapolateRight: "clamp",
          easing: Easing.out(Easing.quad),
        });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};
