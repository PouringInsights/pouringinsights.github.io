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

const slide = (n: number): Media => ({ src: `slide/s${String(n).padStart(2, "0")}.jpg`, kind: "img" });

// Shots hold 2.3–6 s each (never sub-second flashes). Extra inserts land on the
// long static stretches of v1 slides, mostly with slide-deck photos v1 never showed.
export const INSERTS: Shot[][] = [
  // "Trẻ, năng động, nơi tri thức, công nghệ và sức trẻ cùng gặp nhau."
  [
    { m: img(18), from: 15.55, to: 17.9 },
    { m: img(11), from: 17.9, to: 20.2 },
  ],
  // "Đằng sau mỗi giờ học là những thầy cô đưa tri thức ra khỏi trang giáo trình."
  [{ m: img(6), from: 45.55, to: 49.4 }],
  // "Những góc nhìn đa dạng, kiến thức mới và trải nghiệm thực tế ... từng lớp học."
  // + "Ở kinh doanh số, học không chỉ để biết, học là để hiểu, để làm ... nghề nghiệp."
  [
    { m: img(17), from: 59.45, to: 65.75 },
    { m: slide(40), from: 65.75, to: 68.95 },
    { m: slide(41), from: 68.95, to: 72.15 },
  ],
  // "Điều đáng giá nhất ... dám nghĩ, dám tìm tòi, dám thử nghiệm."
  [
    { m: slide(38), from: 85.4, to: 87.95 },
    { m: slide(16), from: 87.95, to: 90.5 },
  ],
  // "Thanh xuân đại học ... cuộc thi, workshop, hoạt động ngoại khóa và những người bạn."
  [
    { m: img(20), from: 93.6, to: 95.8 },
    { m: img(2), from: 95.8, to: 97.8 },
    { m: img(21), from: 97.8, to: 100.1 },
  ],
  // "Sinh viên được vận dụng kiến thức logistics vào tình huống thực tế ... làm việc nhóm."
  [
    { m: slide(17), from: 108.1, to: 111.2 },
    { m: slide(22), from: 111.2, to: 114.4 },
  ],
  // "Mỗi cuộc thi là một lần thử sức ... hành trình trưởng thành."
  [
    { m: img(15), from: 131.5, to: 133.8 },
    { m: img(13), from: 133.8, to: 136.1 },
    { m: img(14), from: 136.1, to: 138.5 },
  ],
  // "Từ tham quan doanh nghiệp, kiến tập, thực tập đến tọa đàm chuyên môn"
  [{ m: slide(27), from: 153.7, to: 157.7 }],
  // "Đó là những hành trình trưởng thành, những ước mơ nghề nghiệp ... xã hội."
  [
    { m: slide(39), from: 170.9, to: 173.8 },
    { m: slide(42), from: 173.8, to: 176.8 },
  ],
  // "điều đáng quý nhất vẫn là con người ... chuyến đi và nụ cười."
  [
    { m: img(5), from: 177.1, to: 179.6 },
    { m: img(12), from: 179.6, to: 182.1 },
    { m: img(10), from: 182.1, to: 184.7 },
    { m: clip("v4_cheer", { startFrom: 6.2 }), from: 184.7, to: 187.4 },
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
            <ShotRun shots={shots.map((x) => ({ ...x, m: { ...x.m, still: true, autoFit: true } }))} xfade={9} edgeFade={10} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
