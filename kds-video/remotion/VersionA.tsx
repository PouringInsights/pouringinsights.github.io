import React from "react";
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile } from "remotion";
import { Fonts, Media, Shot, ShotRun, sec } from "./common";

// Version A: the original v1 cut (picture + Manus narration + music) untouched,
// with the faculty's own photos/clips cut in on the lines they illustrate.
// All times are seconds on the v1 timeline, aligned to word timings.

export const V1_DURATION = 199.433;

const img = (n: number, extra: Partial<Media> = {}): Media => ({
  src: `img/p${String(n).padStart(2, "0")}.jpg`,
  kind: "img",
  ...extra,
});
const clip = (name: string, extra: Partial<Media> = {}): Media => ({
  src: `clip/${name}.mp4`,
  kind: "video",
  ...extra,
});

export const INSERTS: Shot[][] = [
  // "Trẻ, năng động, nơi tri thức, công nghệ và sức trẻ cùng gặp nhau."
  [
    { m: img(18, { pan: "right" }), from: 15.55, to: 17.0 },
    { m: clip("v3_dance", { startFrom: 0.5 }), from: 17.0, to: 18.6 },
    { m: img(11, { zoom: "out" }), from: 18.6, to: 20.2 },
  ],
  // "Đằng sau mỗi giờ học là những thầy cô đưa tri thức ra khỏi trang giáo trình."
  [
    { m: img(6, { focusY: 40 }), from: 45.55, to: 47.5 },
    { m: clip("v5_gift"), from: 47.5, to: 49.4 },
  ],
  // "Những góc nhìn đa dạng, kiến thức mới và trải nghiệm thực tế ... từng lớp học."
  [{ m: img(17, { portrait: true }), from: 59.45, to: 65.45 }],
  // "Thanh xuân đại học không chỉ có giờ lên lớp, đó còn là cuộc thi, workshop,
  //  hoạt động ngoại khóa và những người bạn."
  [
    { m: clip("v5_banner"), from: 93.6, to: 95.0 },
    { m: clip("v5_game"), from: 95.0, to: 96.0 },
    { m: img(20, { portrait: true }), from: 96.0, to: 97.8 },
    { m: clip("v5_balloons"), from: 97.8, to: 98.8 },
    { m: img(21, { focusY: 35 }), from: 98.8, to: 100.1 },
  ],
  // "Mỗi cuộc thi là một lần thử sức, mỗi hoạt động là một trải nghiệm,
  //  và mỗi trải nghiệm góp thêm một mảnh ghép vào hành trình trưởng thành."
  [
    { m: img(15), from: 131.5, to: 133.45 },
    { m: clip("v5_night"), from: 133.45, to: 135.2 },
    { m: img(14, { zoom: "out" }), from: 135.2, to: 136.7 },
    { m: img(1, { pan: "left" }), from: 136.7, to: 138.5 },
  ],
  // "Và điều đáng quý nhất vẫn là con người, những thầy cô đồng hành, những người
  //  bạn cùng học, cùng làm, cùng trưởng thành, những giờ học, cuộc thi, chuyến đi
  //  và nụ cười."
  [
    { m: img(5), from: 177.1, to: 179.6 },
    { m: img(12, { focusY: 40 }), from: 179.6, to: 180.9 },
    { m: img(8, { focusY: 45 }), from: 180.9, to: 182.1 },
    { m: img(3), from: 182.1, to: 182.8 },
    { m: img(10, { focusY: 60 }), from: 182.8, to: 183.9 },
    { m: img(7, { focusY: 60 }), from: 183.9, to: 184.85 },
    { m: img(19, { portrait: true }), from: 184.85, to: 185.5 },
    { m: img(9), from: 185.5, to: 186.05 },
    { m: clip("v4_cheer", { startFrom: 6.2 }), from: 186.05, to: 187.4 },
  ],
];

export const VersionA: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Fonts />
      <OffthreadVideo src={staticFile("kds/v1.mp4")} />
      {INSERTS.map((shots, i) => {
        const from = sec(shots[0].from);
        const dur = sec(shots[shots.length - 1].to) - from;
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <ShotRun shots={shots} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
