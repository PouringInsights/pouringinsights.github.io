import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
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

// v1's slides drift behind the narration from ~0:49 onward. Inserts now cover ONLY the
// stretches where the slide on screen does not match what is being said, and carry a
// lower-third with the spoken fact, so every slide that is visible matches its line.
type Run = { shots: Shot[]; lower?: { from: number; to: number; lines: { at: number; text: string }[] } };
export const RUNS: Run[] = [
  // "Trẻ, năng động, nơi tri thức, công nghệ và sức trẻ cùng gặp nhau." (slide still says "ngôi nhà thứ hai")
  { shots: [{ m: img(18), from: 15.55, to: 19.05 }] },
  // "Khoa có 19 giảng viên, gồm 7 tiến sĩ và 12 thạc sĩ" (slide still says "Đằng sau mỗi giờ học")
  { shots: [{ m: slide(8), from: 49.35, to: 53.55 }], lower: { from: 49.6, to: 53.4, lines: [{ at: 49.6, text: "19 giảng viên · 7 tiến sĩ · 12 thạc sĩ" }] } },
  // "Những giờ học khuyến khích sinh viên chủ động, sáng tạo và vận dụng kiến thức vào thực tế."
  { shots: [{ m: slide(15), from: 72.15, to: 75.6 }], lower: { from: 72.4, to: 75.4, lines: [{ at: 72.4, text: "Chủ động · Sáng tạo · Vận dụng vào thực tế" }] } },
  // "...đó còn là cuộc thi, workshop, hoạt động ngoại khóa và những người bạn."
  { shots: [{ m: img(20), from: 96.0, to: 98.2 }, { m: img(21), from: 98.2, to: 100.45 }] },
  // "Sinh viên được vận dụng kiến thức logistics vào tình huống thực tế ... làm việc nhóm."
  { shots: [{ m: slide(17), from: 108.1, to: 111.25 }, { m: slide(22), from: 111.25, to: 114.45 }] },
  // "Mỗi cuộc thi là một lần thử sức ... hành trình trưởng thành." (slide is a step behind)
  { shots: [{ m: img(15), from: 131.5, to: 133.8 }, { m: img(13), from: 133.8, to: 136.1 }, { m: img(14), from: 136.1, to: 138.45 }] },
  // "Khoa đồng hành cùng các hiệp hội ... Viettel Post, Smartlog, MISA ... đối tác Marketing" (slide already shows the questions)
  { shots: [{ m: slide(24), from: 145.45, to: 149.4 }, { m: slide(27), from: 149.4, to: 153.45 }], lower: { from: 145.8, to: 153.3, lines: [{ at: 145.8, text: "Hiệp hội · Cộng đồng chuyên môn · Doanh nghiệp" }, { at: 148.1, text: "Viettel Post · Smartlog · MISA · Vietnamobile" }] } },
  // "sinh viên dần trả lời 3 câu hỏi: Mình đang học gì? ..." (slide already shows the results)
  { shots: [{ m: slide(28), from: 157.5, to: 161.2 }, { m: slide(26), from: 161.2, to: 164.9 }], lower: { from: 157.8, to: 164.8, lines: [{ at: 157.8, text: "3 câu hỏi" }, { at: 159.8, text: "Mình đang học gì?" }, { at: 161.0, text: "Mình có thể làm gì?" }, { at: 162.5, text: "Mình muốn trở thành ai?" }] } },
  // "...trên 90% có việc làm sau 6 tháng. Đó là những hành trình trưởng thành..." (slide already says "Điều đáng quý nhất")
  { shots: [{ m: slide(39), from: 168.5, to: 172.8 }, { m: slide(42), from: 172.8, to: 177.15 }], lower: { from: 168.5, to: 171.2, lines: [{ at: 168.5, text: "90%+ sinh viên có việc làm sau 6 tháng" }] } },
  // "...cùng làm, cùng trưởng thành, những giờ học, cuộc thi, chuyến đi và nụ cười." (end card arrived early)
  { shots: [{ m: img(12), from: 181.5, to: 184.4 }, { m: clip("v4_cheer", { startFrom: 6.2 }), from: 184.4, to: 187.35 }] },
];

const LowerThird: React.FC<{ from: number; lines: { at: number; text: string }[] }> = ({ from, lines }) => {
  const f = useCurrentFrame();
  const t = from + f / 30;
  const cur = [...lines].reverse().find((l) => t >= l.at);
  const o = interpolate(f, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  if (!cur) return null;
  const k = interpolate(t, [cur.at, cur.at + 0.25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", padding: "0 0 70px 90px", opacity: o }}>
      <div style={{ display: "inline-block", alignSelf: "flex-start", background: "rgba(246,241,231,0.95)", borderLeft: "8px solid #C8553D", padding: "18px 34px", borderRadius: 6, boxShadow: "0 10px 30px rgba(0,0,0,0.3)" }}>
        <div style={{ fontFamily: "'Newsreader', serif", fontStyle: "italic", fontSize: 50, color: "#1D2433", opacity: k, transform: `translateY(${(1 - k) * 10}px)` }}>{cur.text}</div>
      </div>
    </AbsoluteFill>
  );
};

export const VersionA: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Fonts />
      <OffthreadVideo src={staticFile("kds/v1.mp4")} muted />
      {RUNS.map((r, i) => {
        const shots = r.shots;
        const from = sec(shots[0].from);
        const dur = sec(shots[shots.length - 1].to) - from;
        return (
          <React.Fragment key={i}>
            <Sequence from={from} durationInFrames={dur}>
              <ShotRun shots={shots.map((x) => ({ ...x, m: { ...x.m, still: true, autoFit: true } }))} xfade={9} edgeFade={10} />
            </Sequence>
            {r.lower ? (
              <Sequence from={sec(r.lower.from)} durationInFrames={sec(r.lower.to - r.lower.from)}>
                <LowerThird from={r.lower.from} lines={r.lower.lines} />
              </Sequence>
            ) : null}
          </React.Fragment>
        );
      })}
      <Audio src={staticFile("kds/audio/a_mix.wav")} />
    </AbsoluteFill>
  );
};
