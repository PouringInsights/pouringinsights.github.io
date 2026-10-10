import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, Easing } from "remotion";
import { Fonts } from "./common";
import { Bg, C, FONT, PhotoCard, Rise, Tag } from "./bkit";
import { Host, blinkAt, talkMouth } from "./Host";

// 5-second character test: walk in, wave, then present a photo.
export const HostPreview: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / 30;
  const walking = t < 1.6;
  const x = interpolate(t, [0, 1.6], [-380, 260], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  const waveK = interpolate(t, [1.6, 1.85, 2.6, 2.85], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const pointK = interpolate(t, [2.75, 3.05], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(1.5)),
  });
  const wiggle = Math.sin(f * 0.5) * 22;
  const rShoulder = -8 + waveK * (-150 + 8) + pointK * (-88 + 8) * (1 - waveK);
  const rElbow = -10 + waveK * (wiggle - 10 + 10) + pointK * 5;
  const pose = {
    walk: walking ? t * 9 : undefined,
    rShoulder: walking ? undefined : rShoulder,
    rElbow: walking ? undefined : rElbow,
    lShoulder: walking ? undefined : 18,
    lElbow: walking ? undefined : 70,
    tablet: true,
    blink: blinkAt(f),
    mouth: talkMouth(f, t > 2.9),
    tilt: waveK * 6,
    bob: walking ? 0 : Math.sin(f / 12) * 2,
  };
  return (
    <AbsoluteFill>
      <Fonts />
      <Bg tone="navy" />
      <div style={{ position: "absolute", left: x, top: 250 }}>
        <Host pose={pose} height={760} />
      </div>
      <PhotoCard src="slide/s38.jpg" at={2.9} x={880} y={170} w={880} h={560} rot={2} from="right" />
      <div style={{ position: "absolute", left: 900, top: 760 }}>
        <Tag text="Hội nghị sinh viên NCKH" at={3.3} size={42} />
      </div>
      <div style={{ position: "absolute", left: 120, top: 90 }}>
        <Rise text="Khoa Kinh doanh số" at={0.3} size={64} />
      </div>
      <div style={{ position: "absolute", right: 60, bottom: 30, fontFamily: FONT, color: C.sky, fontSize: 22 }}>
        bản thử nhân vật
      </div>
    </AbsoluteFill>
  );
};
