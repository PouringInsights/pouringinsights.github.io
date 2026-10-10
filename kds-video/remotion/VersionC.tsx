import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
// @ts-ignore - no bundled types
import { geoNaturalEarth1, geoPath, geoInterpolate } from "d3-geo";
// @ts-ignore - no bundled types
import { feature } from "topojson-client";
// @ts-ignore - json module
import world from "world-atlas/countries-110m.json";
import PLAN from "./plan_c.json";
import { Fonts, MediaFill } from "./common";
import { Bg, C, Counter, FONT, Icon, KImg, PhotoCard, Rise, Sfx, Tag, Wipe, ease, pop, sec } from "./bkit";
import { HostActor, HostSweep } from "./HostActor";

const FPS = 30;
type SegId = string;
const SEG: Record<SegId, { src: number; at: number; dur: number }> = Object.fromEntries(
  (PLAN as any).segments.map((s: any) => [s.id, { src: s.src, at: s.at, dur: s.dur }]),
);
/** C-timeline seconds of a v1 word timestamp inside segment `id` */
const ct = (id: SegId, t: number) => SEG[id].at + (t - SEG[id].src);

const SC = {
  open: [0, 7.7],
  intro: [7.7, 16.6],
  found: [16.6, 41.3],
  faculty: [41.3, 69.8],
  research: [69.8, 84.4],
  contests: [84.4, 122.8],
  experience: [122.8, 142.7],
  partners: [142.7, 167.5],
  outcomes: [167.5, 174.9],
  outro: [174.9, 182.3],
  chant: [182.3, 190.9],
} as const;
type SceneId = keyof typeof SC;
export const C_TOTAL = 190.9;
const L = (scene: SceneId, id: SegId, t: number) => ct(id, t) - SC[scene][0];
const W: React.CSSProperties = { position: "absolute" };
const slide = (n: number) => `slide/s${String(n).padStart(2, "0")}.jpg`;
const img = (n: number) => `img/p${String(n).padStart(2, "0")}.jpg`;

const Caption: React.FC<{ text: string; at: number; x: number; y: number }> = ({ text, at, x, y }) => (
  <div style={{ ...W, left: x, top: y }}>
    <Tag text={text} at={at} bg={C.white} color={C.navy} size={30} />
  </div>
);

// ---------------------------------------------------------------------------
const Open: React.FC = () => {
  const cuts = [
    { src: "clip/v3_dance.mp4", from: 0, to: 2.4, start: 0.3 },
    { src: "clip/v5_banner.mp4", from: 2.4, to: 3.8 },
    { src: img(18), from: 3.8, to: 5.4 },
    { src: img(10), from: 5.4, to: 7.7 },
  ];
  const f = useCurrentFrame();
  const title = pop(f, 5.6, FPS, 16);
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      {cuts.map((c, i) => (
        <Sequence key={i} from={sec(c.from)} durationInFrames={sec(c.to - c.from) + (i < cuts.length - 1 ? 5 : 0)}>
          <MediaFill m={{ src: c.src, kind: c.src.endsWith(".mp4") ? "video" : "img", startFrom: (c as any).start }} dur={sec(c.to - c.from)} />
        </Sequence>
      ))}
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(10,26,74,0.85) 0%, rgba(10,26,74,0) 50%)" }} />
      <div style={{ ...W, left: 120, bottom: 110, opacity: title, transform: `translateY(${(1 - title) * 40}px)` }}>
        <div style={{ fontFamily: FONT, fontWeight: 600, fontSize: 36, color: C.yellow, letterSpacing: 2 }}>TRƯỜNG KINH TẾ · ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI</div>
        <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 120, color: C.white, lineHeight: 1.05 }}>Khoa Kinh doanh số</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Intro: React.FC = () => {
  const s0 = SC.intro[0];
  const tName = L("intro", "name", 11.06);
  const tSub = L("intro", "name", 12.18);
  const chips = [
    { t: "Trẻ · năng động", at: L("intro", "young", 15.7), bg: C.white },
    { t: "Tri thức", at: L("intro", "young", 17.18), bg: C.sky },
    { t: "Công nghệ", at: L("intro", "young", 17.78), bg: C.yellow },
    { t: "Sức trẻ", at: L("intro", "young", 18.42), bg: C.coral, c: C.white },
  ];
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <PhotoCard src={slide(1)} at={0.05} x={90} y={130} w={900} h={720} rot={-2} from="left" />
      <div style={{ ...W, left: 1060, top: 170, width: 820 }}>
        <Rise text="Khoa Kinh doanh số" at={tName} size={86} style={{ whiteSpace: "nowrap" }} />
        <Rise text="Trường Kinh tế · Đại học Công nghiệp Hà Nội" at={tSub} size={34} weight={600} color="rgba(255,255,255,0.85)" stagger={0.04} />
        <div style={{ display: "flex", flexWrap: "wrap", gap: 18, marginTop: 40, width: 520 }}>
          {chips.map((c, i) => (
            <Tag key={i} text={c.t} at={c.at} bg={c.bg} color={(c as any).c ?? C.ink} size={36} />
          ))}
        </div>
      </div>
      <HostActor sceneStart={s0} walkIn={[0.2, 1.4]} xFrom={2000} x={1560} y={360} height={660} acts={[{ at: 1.5, kind: "wave", dur: 1.4 }, { at: 3.2, kind: "present", dur: 5 }]} />
      {chips.map((c, i) => (
        <Sfx key={i} at={c.at} name="click-soft" vol={0.25} />
      ))}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Network: React.FC<{ opacity?: number }> = ({ opacity = 1 }) => {
  const f = useCurrentFrame();
  const nodes = Array.from({ length: 22 }, (_, i) => {
    const a = i * 2.39996;
    const r = 180 + ((i * 97) % 330);
    return { x: 960 + Math.cos(a + f / 400) * r * 1.6, y: 540 + Math.sin(a + f / 400) * r * 0.9 };
  });
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", opacity }}>
      {nodes.map((n, i) =>
        nodes.slice(i + 1).map((m, j) => {
          const d = Math.hypot(n.x - m.x, n.y - m.y);
          return d > 330 ? null : <line key={`${i}-${j}`} x1={n.x} y1={n.y} x2={m.x} y2={m.y} stroke={C.sky} strokeOpacity={0.22 * (1 - d / 330)} strokeWidth={2} />;
        }),
      )}
      {nodes.map((n, i) => (
        <circle key={i} cx={n.x} cy={n.y} r={i % 4 === 0 ? 6 : 3.5} fill={i % 5 === 0 ? C.yellow : C.sky} opacity={0.6} />
      ))}
    </svg>
  );
};

const Found: React.FC = () => {
  const f = useCurrentFrame();
  const s0 = SC.found[0];
  const tDate = L("found", "found", 20.56);
  const tNext = L("found", "found", 23.84);
  const tMission = L("found", "found", 27.16);
  const tMajors = L("found", "majors", 30.95) - 0.4;
  const tAim = L("found", "aim", 36.1) - 0.3;
  const phaseB = ease(f, tMission - 0.3, tMission + 0.3);
  const dAt = [L("found", "found", 20.96), L("found", "found", 21.14), L("found", "found", 21.46)];
  const digits = ["0", "1", ".", "0", "7", ".", "2", "0", "2", "4"];
  const majors = [
    { name: "Marketing", club: "CLB MC8", logo: slide(4), icon: "megaphone" as const, at: L("found", "majors", 31.8), col: C.coral },
    { name: "Logistics & Quản lý chuỗi cung ứng", club: "CLB SELOG", logo: slide(5), icon: "truck" as const, at: L("found", "majors", 32.66), col: C.yellow },
    { name: "Phân tích dữ liệu kinh doanh", club: "CLB SEAL", logo: slide(6), icon: "chart" as const, at: L("found", "majors", 34.62), col: C.sky },
  ];
  const aims = [
    { t: "Kiến thức chuyên môn", at: L("found", "aim", 38.58) },
    { t: "Năng lực công nghệ", at: L("found", "aim", 39.28) },
    { t: "Hiểu thực tiễn", at: L("found", "aim", 40.32) },
    { t: "Sẵn sàng thích ứng", at: L("found", "aim", 41.32) },
  ];
  return (
    <AbsoluteFill>
      {/* A: founding + mission */}
      <Sequence durationInFrames={sec(tMajors) + 10}>
        <Bg tone="navy" />
        <Network opacity={0.3 + 0.7 * phaseB} />
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: 1 - phaseB, paddingLeft: 380 }}>
          <Rise text="Thành lập" at={tDate - 0.3} size={52} weight={600} color={C.sky} />
          <div style={{ display: "flex" }}>
            {digits.map((d, i) => {
              const g = i < 2 ? 0 : i < 5 ? 1 : 2;
              const p = pop(f, dAt[g] + (i % 5) * 0.04, FPS, 11);
              return (
                <span key={i} style={{ fontFamily: FONT, fontWeight: 900, fontSize: 200, color: d === "." ? C.yellow : C.white, letterSpacing: -6, display: "inline-block", transform: `translateY(${(1 - p) * 120}px)`, opacity: Math.min(1, p * 2) }}>
                  {d}
                </span>
              );
            })}
          </div>
          <Rise text="Tiếp nối những nền tảng đã được vun đắp" at={tNext} size={42} weight={600} color="rgba(255,255,255,0.8)" stagger={0.05} />
        </AbsoluteFill>
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: phaseB, paddingLeft: 380 }}>
          <Tag text="Định hướng" at={tMission} bg={C.yellow} size={36} />
          <Rise text="Đào tạo nguồn nhân lực cho nền kinh tế số" at={L("found", "found", 28.48)} size={92} style={{ textAlign: "center", width: 1300, marginTop: 36 }} highlight={["kinh", "tế", "số"]} />
        </AbsoluteFill>
        <HostActor sceneStart={s0} x={110} y={330} height={680} acts={[{ at: tDate, kind: "point", dur: 3.2 }, { at: tMission + 0.4, kind: "present", dur: 3.5 }]} />
        <Sfx at={dAt[0]} name="pop" vol={0.25} />
      </Sequence>
      {/* B: three majors */}
      <Sequence from={sec(tMajors)} durationInFrames={sec(tAim - tMajors) + 10}>
        <Bg tone="cream" />
        <div style={{ ...W, left: 0, right: 0, top: 80, textAlign: "center" }}>
          <Rise text="Ba ngành đào tạo" at={0.1} size={72} color={C.navy} style={{ display: "inline-block" }} />
        </div>
        <div style={{ ...W, left: 110, right: 110, top: 230, display: "flex", gap: 50 }}>
          {majors.map((m, i) => {
            const lt = m.at - tMajors;
            const p = pop(f - sec(tMajors), lt, FPS, 13);
            const prog = ease(f - sec(tMajors), lt, lt + 1.4);
            return (
              <div key={i} style={{ flex: 1, height: 720, backgroundColor: C.navy, borderRadius: 36, overflow: "hidden", transform: `translateY(${(1 - p) * 260}px)`, opacity: Math.min(1, p * 2), boxShadow: "0 30px 60px rgba(10,26,74,0.25)" }}>
                <div style={{ height: 300, overflow: "hidden", backgroundColor: "#fff" }}>
                  <KImg src={m.logo} style={{ width: "100%", height: "100%" }} zoom={0.02} fit="contain" />
                </div>
                <div style={{ padding: "26px 40px", display: "flex", flexDirection: "column", gap: 14 }}>
                  <Icon kind={m.icon} size={130} color={m.col} progress={prog} />
                  <div style={{ fontFamily: FONT, fontWeight: 800, fontSize: 46, color: C.white, lineHeight: 1.12 }}>{m.name}</div>
                  <div style={{ fontFamily: FONT, fontWeight: 600, fontSize: 28, color: m.col }}>{m.club}</div>
                </div>
              </div>
            );
          })}
        </div>
        {majors.map((m, i) => (
          <Sfx key={i} at={m.at - tMajors} name="pop" vol={0.25} />
        ))}
      </Sequence>
      {/* C: common aim */}
      <Sequence from={sec(tAim)}>
        <Bg tone="navy" />
        <PhotoCard src={slide(7)} at={0.05} x={110} y={170} w={860} h={580} rot={-2} from="left" />
        <div style={{ ...W, left: 1040, top: 150, width: 760 }}>
          <Rise text="Ba hướng đi, một mục tiêu chung" at={0.2} size={58} />
          <div style={{ display: "flex", flexDirection: "column", gap: 20, marginTop: 36 }}>
            {aims.map((a, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 18 }}>
                <Tick at={a.at - tAim} />
                <Rise text={a.t} at={a.at - tAim} size={46} weight={700} />
              </div>
            ))}
          </div>
        </div>
        {aims.map((a, i) => (
          <Sfx key={i} at={a.at - tAim} name="click-soft" vol={0.25} />
        ))}
      </Sequence>
    </AbsoluteFill>
  );
};
const Tick: React.FC<{ at: number }> = ({ at }) => {
  const f = useCurrentFrame();
  const p = pop(f, at, FPS, 10);
  return (
    <div style={{ width: 56, height: 56, borderRadius: 28, backgroundColor: C.yellow, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${p})` }}>
      <svg width={32} height={32} viewBox="0 0 32 32">
        <path d="M6 17 L13 24 L26 9" stroke={C.navy} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={40} strokeDashoffset={40 * (1 - p)} />
      </svg>
    </div>
  );
};

// ---------------------------------------------------------------------------
const WORLD = feature(world as any, (world as any).objects.countries);
const PROJ = geoNaturalEarth1().scale(190).translate([540, 290]);
const PATH = geoPath(PROJ);
const HOME: [number, number] = [105.8, 21.0];
const PINS = [
  { name: "Mỹ", ll: [-98, 39], at: 54.66, kind: "home" },
  { name: "Anh", ll: [-1.5, 52.5], at: 54.92, kind: "home", dx: -50, dy: -6 },
  { name: "Pháp", ll: [2.4, 46.6], at: 55.52, kind: "home", dx: 30, dy: 48 },
  { name: "Trung Quốc", ll: [104, 35], at: 55.98, kind: "home" },
  { name: "Úc", ll: [134, -25], at: 58.24, kind: "visit" },
  { name: "Canada", ll: [-106, 57], at: 58.7, kind: "visit" },
];

const Faculty: React.FC = () => {
  const f = useCurrentFrame();
  const s0 = SC.faculty[0];
  const tFac = L("faculty", "faculty", 49.39) - 0.2;
  const tViews = L("faculty", "views", 59.55) - 0.2;
  const tLearn = L("faculty", "learn", 65.8) - 0.2;
  const t19 = L("faculty", "faculty", 50.06) - tFac;
  const tDr = L("faculty", "faculty", 51.38) - tFac;
  const tMs = L("faculty", "faculty", 52.28) - tFac;
  const tMap = L("faculty", "faculty", 53.38) - tFac;
  return (
    <AbsoluteFill>
      {/* A: behind every class */}
      <Sequence durationInFrames={sec(tFac) + 8}>
        <Bg tone="navy" />
        <PhotoCard src={slide(11)} at={0.1} x={560} y={110} w={760} h={560} rot={-3} from="up" />
        <PhotoCard src={slide(8)} at={0.6} x={1120} y={330} w={700} h={460} rot={3} from="right" />
        <div style={{ ...W, left: 470, top: 840, width: 1400 }}>
          <Rise text="Đằng sau mỗi giờ học là những người thầy, người cô" at={0.3} size={42} weight={700} stagger={0.04} style={{ whiteSpace: "nowrap" }} />
        </div>
        <HostActor sceneStart={s0} x={120} y={330} height={680} acts={[{ at: 0.5, kind: "point", dur: 3 }]} />
      </Sequence>
      {/* B: numbers + map */}
      <Sequence from={sec(tFac)} durationInFrames={sec(tViews - tFac) + 8}>
        <FacultyMap t19={t19} tDr={tDr} tMs={tMs} tMap={tMap} base={tFac} />
      </Sequence>
      {/* C: diverse perspectives */}
      <Sequence from={sec(tViews)} durationInFrames={sec(tLearn - tViews) + 8}>
        <Bg tone="cream" />
        <PhotoCard src={slide(12)} at={0.05} x={90} y={120} w={880} h={520} rot={-2} from="left" border={C.navy} />
        <PhotoCard src={img(17)} at={0.4} x={1000} y={90} w={420} h={560} rot={3} from="up" border={C.navy} pos="50% 60%" />
        <PhotoCard src={slide(30)} at={0.8} x={1450} y={160} w={400} h={470} rot={-2} from="right" border={C.navy} />
        <div style={{ ...W, left: 110, top: 740, display: "flex", gap: 22 }}>
          <Tag text="Góc nhìn đa dạng" at={L("faculty", "views", 59.62) - tViews} bg={C.navy} color={C.white} size={44} />
          <Tag text="Kiến thức mới" at={L("faculty", "views", 60.76) - tViews} bg={C.blue} color={C.white} size={44} />
          <Tag text="Trải nghiệm thực tế" at={L("faculty", "views", 61.54) - tViews} bg={C.yellow} size={44} />
        </div>
        <div style={{ ...W, left: 110, top: 860 }}>
          <Rise text="trong từng chương trình, từng môn học, từng lớp học" at={L("faculty", "views", 63.08) - tViews} size={40} weight={600} color={C.navy} stagger={0.04} />
        </div>
      </Sequence>
      {/* D: learn to understand, to do */}
      <Sequence from={sec(tLearn)}>
        <Bg tone="navy" />
        <div style={{ ...W, left: 720, top: 200 }}>
          <Tag text="Ở Kinh doanh số" at={0.05} size={34} />
          <div style={{ marginTop: 34, display: "flex", flexDirection: "column", gap: 10 }}>
            <Rise text="Học không chỉ để biết." at={L("faculty", "learn", 66.88) - tLearn} size={72} color="rgba(255,255,255,0.7)" />
            <Rise text="Học là để HIỂU." at={L("faculty", "learn", 68.14) - tLearn} size={100} highlight={["HIỂU"]} />
            <Rise text="Để LÀM." at={L("faculty", "learn", 69.22) - tLearn} size={100} highlight={["LÀM"]} />
            <Rise text="Và để SẴN SÀNG bước vào nghề nghiệp." at={L("faculty", "learn", 69.7) - tLearn} size={64} highlight={["SẴN", "SÀNG"]} />
          </div>
        </div>
        <HostActor sceneStart={s0 + tLearn} x={200} y={330} height={680} acts={[{ at: 0.4, kind: "present", dur: 5.5 }]} />
      </Sequence>
    </AbsoluteFill>
  );
};

const FacultyMap: React.FC<{ t19: number; tDr: number; tMs: number; tMap: number; base: number }> = ({ t19, tDr, tMs, tMap, base }) => {
  const f = useCurrentFrame();
  const mapIn = ease(f, tMap - 0.2, tMap + 0.6);
  const [hx, hy] = PROJ(HOME);
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <div style={{ ...W, left: 110, top: 180, width: 620 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 24 }}>
          <Counter to={19} at={t19} dur={0.6} size={240} color={C.yellow} />
          <Rise text="giảng viên" at={t19 + 0.2} size={58} />
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", width: 560, gap: 16, marginTop: 30 }}>
          {Array.from({ length: 19 }, (_, i) => {
            const isDr = i < 7;
            const p = pop(f, (isDr ? tDr : tMs) + (isDr ? i : i - 7) * 0.035, FPS, 12);
            return <div key={i} style={{ width: 50, height: 50, borderRadius: 25, backgroundColor: isDr ? C.yellow : C.sky, transform: `scale(${p})` }} />;
          })}
        </div>
        <div style={{ display: "flex", gap: 50, marginTop: 34, fontFamily: FONT, color: C.white }}>
          <span style={{ opacity: pop(f, tDr, FPS, 14) }}><b style={{ fontSize: 70, color: C.yellow }}>7</b> <span style={{ fontSize: 36, fontWeight: 600 }}>tiến sĩ</span></span>
          <span style={{ opacity: pop(f, tMs, FPS, 14) }}><b style={{ fontSize: 70, color: C.sky }}>12</b> <span style={{ fontSize: 36, fontWeight: 600 }}>thạc sĩ</span></span>
        </div>
      </div>
      <div style={{ ...W, left: 780, top: 200, width: 1080, height: 640, opacity: mapIn, transform: `translateX(${(1 - mapIn) * 120}px)` }}>
        <svg width={1080} height={600}>
          {(WORLD as any).features.map((ft: any, i: number) => (
            <path key={i} d={PATH(ft) || ""} fill="rgba(125,178,255,0.18)" stroke="rgba(125,178,255,0.35)" strokeWidth={0.8} />
          ))}
          {PINS.map((p, i) => {
            const at = L("faculty", "faculty", p.at) - base;
            const k = ease(f, at - 0.15, at + 0.7);
            const interp = geoInterpolate(HOME, p.ll as any);
            const pts = Array.from({ length: 41 }, (_, j) => PROJ(interp((j / 40) * k)));
            const d = "M" + pts.map((q: number[]) => `${q[0]},${q[1]}`).join("L");
            const [x, y] = PROJ(p.ll as any);
            const pp = pop(f, at + 0.45, FPS, 9);
            const col = p.kind === "home" ? C.yellow : C.coral;
            return (
              <g key={i}>
                <path d={d} fill="none" stroke={col} strokeWidth={3} strokeDasharray="6 6" opacity={0.85} />
                <circle cx={x} cy={y} r={11 * pp} fill={col} />
                <text x={x + ((p as any).dx ?? 0)} y={y - 22 + ((p as any).dy ?? 0)} fill={C.white} fontFamily={FONT} fontWeight={800} fontSize={30} textAnchor="middle" opacity={pp}>{p.name}</text>
              </g>
            );
          })}
          <circle cx={hx} cy={hy} r={13} fill={C.white} />
          <text x={hx + 18} y={hy + 36} fill={C.white} fontFamily={FONT} fontWeight={700} fontSize={26}>Hà Nội</text>
        </svg>
        <div style={{ display: "flex", gap: 40, fontFamily: FONT, fontWeight: 600, fontSize: 28, color: C.white }}>
          <span><span style={{ color: C.yellow }}>●</span> nơi giảng viên được đào tạo</span>
          <span style={{ opacity: ease(f, L("faculty", "faculty", 57.26) - base, L("faculty", "faculty", 57.8) - base) }}><span style={{ color: C.coral }}>●</span> giảng viên thỉnh giảng quốc tế</span>
        </div>
      </div>
      <Sfx at={t19} name="impact-bass-1" vol={0.3} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Research: React.FC = () => {
  const f = useCurrentFrame();
  const s0 = SC.research[0];
  const tR = L("research", "research", 76.55) - 0.2;
  const stats = [
    { n: 50, suf: "+", label: "bài báo ISI & Scopus", at: L("research", "research", 79.96), col: C.yellow },
    { n: 125, pre: "~", label: "sinh viên NCKH mỗi năm", at: L("research", "research", 82.3), col: C.sky },
    { n: 25, label: "đề tài mỗi năm", at: L("research", "research", 83.78), col: C.coral },
  ];
  return (
    <AbsoluteFill>
      <Sequence durationInFrames={sec(tR) + 8}>
        <Bg tone="cream" />
        <PhotoCard src={slide(15)} at={0.05} x={90} y={110} w={1060} h={700} rot={-1.5} from="left" border={C.navy} />
        <div style={{ ...W, left: 1210, top: 200, width: 640 }}>
          <Rise text="Giờ học khuyến khích sinh viên" at={0.3} size={46} weight={700} color={C.navy} />
          <div style={{ display: "flex", flexDirection: "column", gap: 18, marginTop: 30, alignItems: "flex-start" }}>
            <Tag text="Chủ động" at={L("research", "classes", 73.56)} bg={C.navy} color={C.white} size={48} />
            <Tag text="Sáng tạo" at={L("research", "classes", 74.16)} bg={C.blue} color={C.white} size={48} />
            <Tag text="Vận dụng vào thực tế" at={L("research", "classes", 74.94)} bg={C.yellow} size={48} />
          </div>
        </div>
      </Sequence>
      <Sequence from={sec(tR)}>
        <Bg tone="navy" />
        <PhotoCard src={slide(38)} at={0.1} x={1120} y={90} w={700} h={520} rot={2.5} from="right" pos="50% 70%" />
        <PhotoCard src={slide(16)} at={0.9} x={1180} y={560} w={600} h={400} rot={-3} from="down" />
        <div style={{ ...W, left: 110, top: 120, width: 960 }}>
          <Rise text="Nghiên cứu khoa học" at={0.2} size={80} highlight={["khoa", "học"]} accent={C.sky} style={{ whiteSpace: "nowrap" }} />
          <Rise text="một phần quan trọng của đời sống học thuật" at={1.0} size={36} weight={600} color="rgba(255,255,255,0.75)" stagger={0.04} />
          <div style={{ marginTop: 50, display: "flex", flexDirection: "column", gap: 24 }}>
            {stats.map((s, i) => (
              <div key={i} style={{ display: "flex", alignItems: "baseline", gap: 28 }}>
                <div style={{ width: 320, textAlign: "right" }}>
                  <Counter to={s.n} at={s.at - tR} dur={0.8} size={124} color={s.col} prefix={(s as any).pre} suffix={(s as any).suf} />
                </div>
                <Rise text={s.label} at={s.at - tR + 0.15} size={38} weight={600} stagger={0.04} style={{ whiteSpace: "nowrap" }} />
              </div>
            ))}
          </div>
        </div>
        {stats.map((s, i) => (
          <Sfx key={i} at={s.at - tR} name="pop" vol={0.25} />
        ))}
      </Sequence>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Contests: React.FC = () => {
  const f = useCurrentFrame();
  const s0 = SC.contests[0];
  const tLogi = L("contests", "logi", 99.8) - 0.2;
  const tLogi2 = L("contests", "logi2", 108.16) - 0.15;
  const tMc8 = L("contests", "mc8", 114.55) - 0.2;
  const tMj = L("contests", "mj", 122.5) - 0.2;
  const lifeCuts = [
    { src: img(20), from: 0, to: L("contests", "life", 96.42), portrait: true },
    { src: "clip/v5_banner.mp4", from: L("contests", "life", 96.42), to: L("contests", "life", 97.84) },
    { src: img(19), from: L("contests", "life", 97.84), to: L("contests", "life", 98.82), portrait: true },
    { src: img(7), from: L("contests", "life", 98.82), to: tLogi },
  ];
  return (
    <AbsoluteFill>
      {/* A: student life beyond class */}
      <Sequence durationInFrames={sec(tLogi) + 8}>
        <AbsoluteFill style={{ backgroundColor: C.navy }}>
          {lifeCuts.map((c, i) => (
            <Sequence key={i} from={sec(c.from)} durationInFrames={Math.max(1, sec(c.to - c.from)) + 5}>
              <MediaFill m={{ src: c.src, kind: c.src.endsWith(".mp4") ? "video" : "img", portrait: (c as any).portrait }} dur={sec(c.to - c.from)} />
            </Sequence>
          ))}
          <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(10,26,74,0.75) 0%, rgba(10,26,74,0) 40%), linear-gradient(0deg, rgba(10,26,74,0.7) 0%, rgba(10,26,74,0) 35%)" }} />
          <div style={{ ...W, left: 110, top: 90 }}>
            <Rise text="Không chỉ có giờ lên lớp" at={0.2} size={80} style={{ textShadow: "0 8px 30px rgba(0,0,0,0.5)" }} />
          </div>
          <div style={{ ...W, left: 110, bottom: 90, display: "flex", gap: 20 }}>
            <Tag text="Cuộc thi" at={L("contests", "life", 96.42)} size={44} />
            <Tag text="Workshop" at={L("contests", "life", 97.14)} bg={C.white} size={44} />
            <Tag text="Ngoại khóa" at={L("contests", "life", 97.84)} bg={C.sky} size={44} />
            <Tag text="Bạn bè" at={L("contests", "life", 98.82)} bg={C.coral} color={C.white} size={44} />
          </div>
        </AbsoluteFill>
      </Sequence>
      {/* B: LogiMaster */}
      <Sequence from={sec(tLogi)} durationInFrames={sec(tMc8 - tLogi) + 8}>
        <LogiMaster base={tLogi} t2={tLogi2} s0={s0} />
      </Sequence>
      {/* C: MC8 + clubs */}
      <Sequence from={sec(tMc8)} durationInFrames={sec(tMj - tMc8) + 8}>
        <Bg tone="navy" />
        <PhotoCard src={slide(19)} at={0.1} x={980} y={130} w={840} h={500} rot={2} from="right" />
        <div style={{ ...W, left: 110, top: 150, width: 820 }}>
          <Tag text="Với sinh viên Marketing" at={0.05} bg={C.coral} color={C.white} size={32} />
          <Rise text="CLB MC8 & Marketing Journey" at={L("contests", "mc8", 115.84) - tMc8} size={70} style={{ marginTop: 26 }} />
          <div style={{ display: "flex", gap: 18, marginTop: 30 }}>
            <Tag text="Học hỏi" at={L("contests", "mc8", 118.6) - tMc8} bg={C.white} size={40} />
            <Tag text="Sáng tạo" at={L("contests", "mc8", 119.3) - tMc8} bg={C.yellow} size={40} />
          </div>
        </div>
        <div style={{ ...W, left: 110, top: 700, right: 110 }}>
          <Rise text="Câu lạc bộ học thuật của Khoa" at={1.2} size={34} weight={700} color={C.sky} />
          <div style={{ display: "flex", gap: 30, marginTop: 20 }}>
            {[slide(4), slide(5), slide(6)].map((s, i) => (
              <ClubLogo key={i} src={s} at={1.5 + i * 0.3} name={["MC8 · Marketing", "SELOG · Logistics", "SEAL · Phân tích dữ liệu"][i]} />
            ))}
          </div>
        </div>
      </Sequence>
      {/* D: Marketing Journey growth */}
      <Sequence from={sec(tMj)}>
        <MarketingJourney base={tMj} />
      </Sequence>
    </AbsoluteFill>
  );
};
const ClubLogo: React.FC<{ src: string; at: number; name: string }> = ({ src, at, name }) => {
  const f = useCurrentFrame();
  const p = pop(f, at, FPS, 13);
  return (
    <div style={{ width: 540, opacity: p, transform: `translateY(${(1 - p) * 60}px)` }}>
      <div style={{ height: 200, borderRadius: 22, overflow: "hidden", border: `5px solid ${C.white}` }}>
        <KImg src={src} style={{ width: "100%", height: "100%" }} zoom={0.04} />
      </div>
      <div style={{ fontFamily: FONT, fontWeight: 700, fontSize: 30, color: C.white, marginTop: 10 }}>{name}</div>
    </div>
  );
};

const LogiMaster: React.FC<{ base: number; t2: number; s0: number }> = ({ base, t2, s0 }) => {
  const f = useCurrentFrame();
  const tl = (t: number) => L("contests", "logi", t) - base;
  const tTitle = tl(100.4);
  const t2022 = tl(102.16);
  const tSeasons = tl(103.5);
  const tTeams = tl(105.16);
  const tStud = tl(106.44);
  const line = ease(f, t2022, tSeasons + 0.8);
  const phase2 = ease(f, t2 - base - 0.2, t2 - base + 0.3);
  const t2l = (t: number) => L("contests", "logi2", t) - base;
  return (
    <AbsoluteFill>
      <Bg tone="cream" />
      <AbsoluteFill style={{ opacity: 1 - phase2 }}>
        <PhotoCard src={slide(18)} at={0.1} x={980} y={120} w={840} h={560} rot={2.5} from="right" border={C.navy} />
        <div style={{ ...W, left: 110, top: 130, width: 840 }}>
          <Tag text="Với sinh viên Logistics" at={0.05} bg={C.navy} color={C.white} size={32} />
          <Rise text="HaUI LogiMaster" at={tTitle} size={100} color={C.navy} style={{ marginTop: 26 }} highlight={["LogiMaster"]} accent={C.blue} />
        </div>
        <div style={{ ...W, left: 120, top: 520, width: 760, height: 120 }}>
          <div style={{ ...W, left: 0, top: 50, height: 8, width: 740 * line, backgroundColor: C.navy, borderRadius: 4 }} />
          {[0, 1, 2, 3].map((i) => {
            const p = pop(f, tSeasons + i * 0.18, FPS, 10);
            return (
              <div key={i} style={{ ...W, left: i * 240 - 20, top: 30, width: 48 }}>
                <div style={{ width: 48, height: 48, borderRadius: 24, backgroundColor: i === 0 ? C.coral : C.blue, transform: `scale(${p})` }} />
                <div style={{ fontFamily: FONT, fontWeight: 700, fontSize: 26, color: C.navy, marginTop: 10, opacity: p, whiteSpace: "nowrap" }}>{i === 0 ? "2022" : `Mùa ${i + 1}`}</div>
              </div>
            );
          })}
        </div>
        <div style={{ ...W, left: 120, top: 720, display: "flex", gap: 90 }}>
          {[{ n: 4, l: "mùa thi", at: tSeasons }, { n: 25, l: "đội / mùa", at: tTeams, pre: "~" }, { n: 100, l: "sinh viên / mùa", at: tStud, pre: "~" }].map((s, i) => (
            <div key={i}>
              <Counter to={s.n} at={s.at} dur={0.7} size={116} color={C.blue} prefix={(s as any).pre} />
              <Rise text={s.l} at={s.at + 0.1} size={34} weight={600} color={C.navy} stagger={0.04} />
            </div>
          ))}
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ opacity: phase2 }}>
        <PhotoCard src={slide(22)} at={t2 - base} x={110} y={140} w={900} h={700} rot={-2} from="left" border={C.navy} />
        <PhotoCard src={slide(17)} at={t2 - base + 0.5} x={1060} y={110} w={760} h={420} rot={2} from="right" border={C.navy} />
        <div style={{ ...W, left: 1080, top: 590, display: "flex", flexDirection: "column", gap: 18, alignItems: "flex-start" }}>
          <Tag text="Tình huống thực tế" at={t2l(110.24)} bg={C.navy} color={C.white} size={44} />
          <Tag text="Giải quyết vấn đề" at={t2l(111.88)} bg={C.blue} color={C.white} size={44} />
          <Tag text="Làm việc nhóm" at={t2l(113.24)} bg={C.yellow} size={44} />
        </div>
      </AbsoluteFill>
      <Sfx at={tTeams} name="pop" vol={0.25} />
      <Sfx at={tStud} name="pop" vol={0.25} />
    </AbsoluteFill>
  );
};

const MarketingJourney: React.FC<{ base: number }> = ({ base }) => {
  const f = useCurrentFrame();
  const tl = (t: number) => L("contests", "mj", t) - base;
  const maxH = 320;
  const bar = (at: number, v: number) => (maxH * v * ease(f, at, at + 0.9)) / 124;
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <div style={{ ...W, left: 110, top: 110 }}>
        <Rise text="Marketing Journey" at={0.1} size={84} highlight={["Journey"]} accent={C.coral} style={{ whiteSpace: "nowrap" }} />
      </div>
      <div style={{ ...W, left: 150, top: 300, width: 760, height: 600 }}>
        {[{ l: "Mùa đầu", v: 65, at: tl(124.06), col: C.sky, x: 0, pre: "65+" }, { l: "Mùa tiếp theo", v: 124, at: tl(125.6), col: C.yellow, x: 340 }].map((b, i) => (
          <div key={i} style={{ ...W, left: b.x, bottom: 70, width: 230 }}>
            <div style={{ textAlign: "center", marginBottom: 12 }}>
              <Counter to={b.v} at={b.at} dur={0.9} size={84} color={b.col} suffix={i === 0 ? "+" : ""} />
              <div style={{ fontFamily: FONT, fontWeight: 600, fontSize: 30, color: C.white, opacity: ease(f, b.at, b.at + 0.4) }}>đội thi</div>
            </div>
            <div style={{ height: bar(b.at, b.v), backgroundColor: b.col, borderRadius: "18px 18px 0 0" }} />
            <div style={{ ...W, bottom: -56, width: 230, textAlign: "center", fontFamily: FONT, fontWeight: 700, fontSize: 30, color: "rgba(255,255,255,0.8)" }}>{b.l}</div>
          </div>
        ))}
        <div style={{ ...W, left: 0, bottom: 68, width: 600, height: 4, backgroundColor: "rgba(255,255,255,0.4)" }} />
      </div>
      <PhotoCard src={slide(20)} at={tl(127.32) - 0.6} x={1060} y={170} w={760} h={330} rot={-2} from="right" />
      <div style={{ ...W, left: 1060, top: 560 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 20 }}>
          <Counter to={360} at={tl(127.32)} dur={0.9} size={124} color={C.yellow} suffix="+" />
          <Rise text="thí sinh" at={tl(127.6)} size={50} />
        </div>
        <Rise text="từ nhiều trường đại học tại Hà Nội" at={tl(128.86)} size={34} weight={600} color="rgba(255,255,255,0.85)" stagger={0.04} />
        <div style={{ display: "flex", gap: 16, marginTop: 22 }}>
          {["NEU", "Ngoại thương", "Học viện Ngân hàng", "…"].map((u, i) => (
            <Tag key={i} text={u} at={tl(129.7) + i * 0.15} bg={C.white} size={30} />
          ))}
        </div>
      </div>
      <Sfx at={tl(124.06)} name="pop" vol={0.25} />
      <Sfx at={tl(125.6)} name="pop" vol={0.25} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Experience: React.FC = () => {
  const f = useCurrentFrame();
  const tiles = [img(2), img(15), img(13), img(12), img(9), img(14), img(16), img(21), img(5)];
  const tIn = (i: number) => L("experience", "pieces", 135.2) + i * 0.16;
  const montageStart = L("experience", "pieces", 138.4) + 0.4;
  const cuts = [
    "clip/v5_balloons.mp4", img(6), "clip/v5_circle.mp4", img(4), "clip/v5_gift.mp4", "clip/v5_bbqmeat.mp4",
    img(3), "clip/v5_night.mp4", img(11), img(18), "clip/v5_smoke.mp4", img(1), "clip/v5_laugh.mp4", img(8),
  ];
  const each = (SC.experience[1] - SC.experience[0] - montageStart) / cuts.length;
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      {/* first lines: two real moments */}
      <Sequence durationInFrames={sec(L("experience", "pieces", 133.5)) + 5}>
        <MediaFill m={{ src: slide(17), kind: "img" }} dur={sec(2.6)} />
      </Sequence>
      <Sequence from={sec(L("experience", "pieces", 133.5))} durationInFrames={sec(L("experience", "pieces", 135.2) - L("experience", "pieces", 133.5)) + 5}>
        <MediaFill m={{ src: img(2), kind: "img" }} dur={sec(2)} />
      </Sequence>
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(10,26,74,0.8) 0%, rgba(10,26,74,0) 40%)", opacity: f < sec(L("experience", "pieces", 135.2)) ? 1 : 0 }} />
      <div style={{ ...W, left: 110, bottom: 90, opacity: f < sec(L("experience", "pieces", 135.2)) ? 1 : 0 }}>
        <Rise text="Mỗi cuộc thi là một lần thử sức" at={L("experience", "pieces", 131.66)} size={58} />
        <Rise text="Mỗi hoạt động là một trải nghiệm" at={L("experience", "pieces", 133.5)} size={58} />
      </div>
      {/* mosaic: "mỗi trải nghiệm góp thêm một mảnh ghép" */}
      <Sequence from={sec(L("experience", "pieces", 135.2))} durationInFrames={sec(montageStart - L("experience", "pieces", 135.2)) + 6}>
        <AbsoluteFill style={{ backgroundColor: C.navy }}>
          {tiles.map((src, i) => {
            const p = pop(f - sec(L("experience", "pieces", 135.2)), i * 0.16, FPS, 14);
            const col = i % 3;
            const row = Math.floor(i / 3);
            return (
              <div key={i} style={{ ...W, left: 30 + col * 630, top: 30 + row * 345, width: 610, height: 330, transform: `scale(${p}) rotate(${(1 - p) * (i % 2 ? 8 : -8)}deg)`, opacity: p }}>
                <KImg src={src} style={{ width: "100%", height: "100%", borderRadius: 18 }} zoom={0.1} />
              </div>
            );
          })}
          <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
            <div style={{ backgroundColor: "rgba(10,26,74,0.88)", padding: "26px 50px", borderRadius: 28, opacity: pop(f - sec(L("experience", "pieces", 135.2)), 0.8, FPS, 14) }}>
              <Rise text="Mỗi trải nghiệm, một mảnh ghép của hành trình trưởng thành" at={0.8} size={50} stagger={0.04} />
            </div>
          </AbsoluteFill>
        </AbsoluteFill>
      </Sequence>
      {/* music-only montage */}
      {cuts.map((src, i) => (
        <Sequence key={i} from={sec(montageStart + i * each)} durationInFrames={sec(each) + 4}>
          <MediaFill m={{ src, kind: src.endsWith(".mp4") ? "video" : "img", zoom: i % 2 ? "out" : "in" }} dur={sec(each)} />
        </Sequence>
      ))}
      <div style={{ ...W, right: 60, bottom: 50, opacity: f > sec(montageStart) ? 1 : 0 }}>
        <Tag text="Hoạt động trải nghiệm của sinh viên KDS" at={montageStart + 0.3} bg="rgba(255,255,255,0.92)" color={C.navy} size={28} />
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Partners: React.FC = () => {
  const f = useCurrentFrame();
  const s0 = SC.partners[0];
  const tNet = L("partners", "partners", 144.76);
  const tQ0 = L("partners", "questions", 153.72) - 0.2;
  const tQ = L("partners", "questions", 157.84);
  const fade1 = ease(f, tNet - 0.5, tNet + 0.1);
  const cx = 1060, cy = 600;
  const nodes = [
    { t: "Hiệp hội nghề nghiệp", at: L("partners", "partners", 145.56), a: 200, r: 360, col: C.sky },
    { t: "Cộng đồng chuyên môn", at: L("partners", "partners", 146.24), a: 245, r: 400, col: C.sky },
    { t: "Doanh nghiệp", at: L("partners", "partners", 147.26), a: 295, r: 360, col: C.sky },
    { t: "Viettel Post", at: L("partners", "partners", 148.24), a: 340, r: 520, col: C.yellow },
    { t: "Smartlog", at: L("partners", "partners", 149.2), a: 25, r: 480, col: C.yellow },
    { t: "MISA", at: L("partners", "partners", 150.02), a: 150, r: 470, col: C.white },
    { t: "TDS", at: L("partners", "partners", 150.68), a: 115, r: 450, col: C.white },
    { t: "Đối tác Marketing", at: L("partners", "partners", 151.62), a: 68, r: 400, col: C.coral },
  ];
  const pos = (a: number, r: number) => [cx + Math.cos((a * Math.PI) / 180) * r * 1.2, cy + Math.sin((a * Math.PI) / 180) * r * 0.62];
  const acts = [
    { t: "Tham quan doanh nghiệp", at: L("partners", "questions", 154.04), src: slide(27), x: 110, y: 120, rot: -2 },
    { t: "Kiến tập", at: L("partners", "questions", 155.14), src: slide(26), x: 1010, y: 100, rot: 2 },
    { t: "Thực tập", at: L("partners", "questions", 155.8), src: slide(24), x: 190, y: 560, rot: 2 },
    { t: "Tọa đàm chuyên môn", at: L("partners", "questions", 156.64), src: slide(28), x: 1060, y: 540, rot: -2 },
  ];
  const out1 = ease(f, tQ - 0.2, tQ + 0.4);
  const qs = [
    { t: "Mình đang học gì?", at: L("partners", "questions", 159.86) },
    { t: "Mình có thể làm gì?", at: L("partners", "questions", 161.06) },
    { t: "Mình muốn trở thành ai?", at: L("partners", "questions", 162.54), hl: true },
  ];
  return (
    <AbsoluteFill>
      <Sequence durationInFrames={sec(tQ0) + 8}>
        <Bg tone="navy" />
        <AbsoluteFill style={{ opacity: 1 - fade1 }}>
          <KImg src={slide(24)} style={{ position: "absolute", inset: 0 }} pos="50% 35%" />
          <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(10,26,74,0.95) 0%, rgba(10,26,74,0.7) 60%, rgba(10,26,74,0.2) 100%)" }} />
          <div style={{ ...W, left: 110, top: 330, width: 1100 }}>
            <Rise text="Tri thức ý nghĩa hơn" at={L("partners", "partners", 141.78)} size={100} />
            <Rise text="khi được kết nối với thực tiễn" at={L("partners", "partners", 142.62)} size={70} weight={600} highlight={["thực", "tiễn"]} />
          </div>
        </AbsoluteFill>
        <AbsoluteFill style={{ opacity: fade1 }}>
          <svg width={1920} height={1080} style={{ position: "absolute" }}>
            {nodes.map((n, i) => {
              const [x, y] = pos(n.a, n.r);
              const k = ease(f, n.at - 0.1, n.at + 0.35);
              return <line key={i} x1={cx} y1={cy} x2={cx + (x - cx) * k} y2={cy + (y - cy) * k} stroke={n.col} strokeOpacity={0.55} strokeWidth={3} />;
            })}
          </svg>
          <div style={{ ...W, left: cx - 130, top: cy - 130, width: 260, height: 260, borderRadius: 130, backgroundColor: C.blue, border: `8px solid ${C.white}`, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", transform: `scale(${pop(f, tNet, FPS, 11)})` }}>
            <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 66, color: C.white, lineHeight: 1 }}>KDS</div>
            <div style={{ fontFamily: FONT, fontWeight: 600, fontSize: 22, color: C.white, opacity: 0.85, textAlign: "center" }}>Khoa Kinh doanh số</div>
          </div>
          {nodes.map((n, i) => {
            const [x, y] = pos(n.a, n.r);
            return (
              <div key={i} style={{ ...W, left: x, top: y, transform: "translate(-50%, -50%)" }}>
                <Tag text={n.t} at={n.at + 0.2} bg={n.col} color={n.col === C.coral ? C.white : C.ink} size={i < 3 ? 32 : 42} />
              </div>
            );
          })}
          <div style={{ ...W, left: 110, top: 80 }}>
            <Rise text="Khoa đồng hành cùng" at={tNet} size={54} weight={700} />
          </div>
          <HostActor sceneStart={s0} x={40} y={420} height={620} acts={[{ at: tNet + 0.2, kind: "present", dur: 7 }]} />
        </AbsoluteFill>
      </Sequence>
      <Sequence from={sec(tQ0)}>
        <Bg tone="navy" />
        <AbsoluteFill style={{ opacity: 1 - out1, transform: `scale(${1 + 0.1 * out1})` }}>
          {acts.map((a, i) => (
            <React.Fragment key={i}>
              <PhotoCard src={a.src} at={a.at - tQ0} x={a.x} y={a.y} w={700} h={400} rot={a.rot} from={i % 2 ? "right" : "left"} />
              <div style={{ ...W, left: a.x + 30, top: a.y + 320 }}>
                <Tag text={a.t} at={a.at - tQ0 + 0.15} size={38} />
              </div>
            </React.Fragment>
          ))}
        </AbsoluteFill>
        <AbsoluteFill style={{ opacity: out1 }}>
          <div style={{ ...W, left: 700, top: 270 }}>
            <Rise text="Định hướng rõ ràng" at={tQ - tQ0} size={42} weight={700} color={C.sky} />
            <div style={{ display: "flex", flexDirection: "column", gap: 18, marginTop: 26 }}>
              {qs.map((q, i) => (
                <Rise key={i} text={q.t} at={q.at - tQ0} size={q.hl ? 104 : 86} color={q.hl ? C.yellow : C.white} stagger={0.05} />
              ))}
            </div>
          </div>
          <HostActor sceneStart={s0 + tQ0} x={170} y={330} height={680} acts={[{ at: tQ - tQ0 + 0.3, kind: "present", dur: 6.5 }]} />
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Outcomes: React.FC = () => {
  const f = useCurrentFrame();
  const t3 = L("outcomes", "outcomes", 165.0);
  const t1000 = L("outcomes", "outcomes", 166.4);
  const t90 = L("outcomes", "outcomes", 168.26);
  const ring = ease(f, t90, t90 + 1.2) * 0.9;
  const R = 120;
  const circ = 2 * Math.PI * R;
  return (
    <AbsoluteFill>
      <KImg src={slide(29)} style={{ position: "absolute", inset: 0 }} pos="50% 35%" zoom={0.08} />
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(10,26,74,0.97) 0%, rgba(10,26,74,0.9) 50%, rgba(10,26,74,0.35) 100%)" }} />
      <div style={{ ...W, left: 110, top: 110 }}>
        <Tag text="Thành quả" at={0.05} size={36} />
      </div>
      <div style={{ ...W, left: 110, right: 110, top: 520, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <Counter to={3} at={t3} dur={0.4} size={140} color={C.white} />
          <Rise text="chương trình đào tạo" at={t3 + 0.1} size={36} weight={600} />
        </div>
        <div>
          <Counter to={1000} at={t1000} dur={1.0} size={140} color={C.yellow} suffix="+" thousands />
          <Rise text="sinh viên tốt nghiệp" at={t1000 + 0.2} size={36} weight={600} />
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 26 }}>
          <div style={{ position: "relative", width: 2 * R + 40, height: 2 * R + 40 }}>
            <svg width={2 * R + 40} height={2 * R + 40}>
              <circle cx={R + 20} cy={R + 20} r={R} fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth={24} />
              <circle cx={R + 20} cy={R + 20} r={R} fill="none" stroke={C.yellow} strokeWidth={24} strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - ring)} transform={`rotate(-90 ${R + 20} ${R + 20})`} />
            </svg>
            <div style={{ ...W, inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <Counter to={90} at={t90} dur={1.2} size={78} color={C.white} suffix="%" />
            </div>
          </div>
          <Rise text="có việc làm sau 6 tháng" at={L("outcomes", "outcomes", 169.12)} size={36} weight={600} style={{ width: 260 }} />
        </div>
      </div>
      <Sfx at={t1000} name="pop" vol={0.25} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Outro: React.FC = () => {
  const f = useCurrentFrame();
  const s0 = SC.outro[0];
  const pics = [slide(33), img(5), slide(39), img(14), slide(1), img(12), slide(29), img(9), slide(42), img(21), slide(11), img(16)];
  const cols = 4;
  const cw = 1920 / cols;
  const ch = 1080 / 3;
  const tName = L("outro", "outro", 187.4);
  const words = [
    { t: "Học tập", at: L("outro", "outro", 191.52), c: C.sky },
    { t: "Trải nghiệm", at: L("outro", "outro", 192.24), c: C.yellow },
    { t: "Trưởng thành", at: L("outro", "outro", 192.96), c: C.white },
  ];
  const panel = pop(f, tName - 0.1, FPS, 16);
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      {pics.map((src, i) => {
        const p = pop(f, i * 0.05, FPS, 14);
        return (
          <div key={i} style={{ ...W, left: (i % cols) * cw, top: Math.floor(i / cols) * ch, width: cw, height: ch, transform: `scale(${p})`, opacity: p, padding: 6 }}>
            <KImg src={src} style={{ width: "100%", height: "100%", borderRadius: 16 }} zoom={0.12} />
          </div>
        );
      })}
      <AbsoluteFill style={{ backgroundColor: `rgba(10,26,74,${0.6 * panel})` }} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <div style={{ backgroundColor: C.navy, borderRadius: 40, padding: "56px 90px", transform: `scale(${0.85 + 0.15 * panel})`, opacity: panel, textAlign: "center", boxShadow: "0 40px 100px rgba(0,0,0,0.5)", border: `5px solid ${C.yellow}` }}>
          <Rise text="Khoa Kinh doanh số" at={tName} size={112} />
          <Rise text="Trường Kinh tế · Đại học Công nghiệp Hà Nội" at={L("outro", "outro", 188.74)} size={38} weight={600} color="rgba(255,255,255,0.85)" stagger={0.04} />
          <div style={{ display: "flex", gap: 26, justifyContent: "center", marginTop: 38 }}>
            {words.map((w, i) => (
              <Tag key={i} text={w.t} at={w.at} bg={w.c} size={46} color={C.ink} />
            ))}
          </div>
        </div>
      </AbsoluteFill>
      <HostActor sceneStart={s0} walkIn={[4.6, 5.6]} xFrom={-400} x={70} y={420} height={620} acts={[{ at: 5.7, kind: "wave", dur: 1.6 }]} talk={false} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Chant: React.FC = () => {
  const f = useCurrentFrame();
  const len = SC.chant[1] - SC.chant[0];
  const p = pop(f, 4.0, FPS, 14);
  const end = interpolate(f, [sec(len - 0.7), sec(len)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      <MediaFill m={{ src: "clip/v4_cheer.mp4", kind: "video", startFrom: 0 }} dur={sec(len)} />
      <Audio src={staticFile("kds/clip/v4_cheer.mp4")} volume={(fr) => interpolate(fr, [0, 4, sec(len - 0.8), sec(len)], [0, 0.9, 0.9, 0], { extrapolateRight: "clamp" })} />
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(10,26,74,0.85) 0%, rgba(10,26,74,0) 40%)", opacity: p }} />
      <div style={{ ...W, left: 0, right: 0, bottom: 80, textAlign: "center", opacity: p, transform: `translateY(${(1 - p) * 40}px)` }}>
        <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 76, color: C.white }}>Khoa Kinh doanh số</div>
        <div style={{ fontFamily: FONT, fontWeight: 600, fontSize: 34, color: C.yellow, letterSpacing: 2 }}>TRƯỜNG KINH TẾ · ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI</div>
      </div>
      <AbsoluteFill style={{ backgroundColor: C.navy, opacity: end }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const SCENES: [SceneId, React.FC][] = [
  ["open", Open], ["intro", Intro], ["found", Found], ["faculty", Faculty], ["research", Research],
  ["contests", Contests], ["experience", Experience], ["partners", Partners], ["outcomes", Outcomes],
  ["outro", Outro], ["chant", Chant],
];
const SWEEPS: SceneId[] = ["found", "faculty", "contests", "partners", "outro"];
const WIPES: SceneId[] = ["intro", "research", "experience", "outcomes", "chant"];

const VOICE = (PLAN as any).segments.map((s: any) => [s.at, s.at + s.dur]);
const musicVol = (fr: number) => {
  const t = fr / FPS;
  let duck = 0;
  for (const [a, b] of VOICE) {
    duck = Math.max(duck, interpolate(t, [a - 0.35, a, b, b + 0.5], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  }
  const tail = interpolate(t, [181.5, 183.0], [1, 0.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const out = interpolate(t, [189.6, 190.9], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (1 - 0.5 * duck) * tail * out;
};

export const VersionC: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.navy }}>
    <Fonts />
    {SCENES.map(([id, Comp]) => (
      <Sequence key={id} from={sec(SC[id][0])} durationInFrames={sec(SC[id][1]) - sec(SC[id][0])}>
        <Comp />
      </Sequence>
    ))}
    {SWEEPS.map((id) => (
      <Sequence key={`s${id}`} from={sec(SC[id][0]) - 24} durationInFrames={36}>
        <HostSweep />
      </Sequence>
    ))}
    {SWEEPS.map((id) => (
      <Sfx key={`ss${id}`} at={SC[id][0] - 0.75} name="whoosh" vol={0.15} />
    ))}
    {WIPES.map((id) => (
      <Sequence key={`w${id}`} from={sec(SC[id][0]) - 7} durationInFrames={18}>
        <Wipe color={C.blue} color2={C.yellow} />
      </Sequence>
    ))}
    <Audio src={staticFile("kds/audio/voice_c.wav")} volume={1} />
    <Audio src={staticFile("kds/audio/music_c.wav")} volume={musicVol} />
  </AbsoluteFill>
);
