import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  Easing,
} from "remotion";
// @ts-ignore - no bundled types
import { geoNaturalEarth1, geoPath, geoInterpolate } from "d3-geo";
// @ts-ignore - no bundled types
import { feature } from "topojson-client";
// @ts-ignore - json module
import world from "world-atlas/countries-110m.json";
import { Fonts, MediaFill } from "./common";
import { Img } from "remotion";
import { Grade } from "./Cine";
import {
  B_TOTAL,
  Bg,
  C,
  Counter,
  FONT,
  FPS,
  Icon,
  KImg,
  PhotoCard,
  FitCard,
  Rise,
  SEGS,
  Sfx,
  Tag,
  Wipe,
  bt,
  ease,
  pop,
  sec,
} from "./bkit";

// Scene boundaries on the Version B timeline (seconds).
const SC = {
  hook: [0, 3.45],
  name: [3.45, 7.35],
  found: [7.35, 18.2],
  majors: [18.2, 24.3],
  faculty: [24.3, 35.0],
  learn: [35.0, 42.3],
  research: [42.3, 51.75],
  life: [51.75, 58.6],
  logi: [58.6, 67.7],
  mj: [67.7, 77.6],
  partners: [77.6, 90.05],
  questions: [90.05, 101.7],
  outcomes: [101.7, 108.65],
  outro: [108.65, 115.6],
  cheer: [115.6, B_TOTAL],
} as const;
type SceneId = keyof typeof SC;

/** local time (scene seconds) of a v1 word timestamp */
const L = (scene: SceneId, seg: keyof typeof SEGS, t: number) =>
  bt(seg, t) - SC[scene][0];

const W: React.CSSProperties = { position: "absolute" };

// ---------------------------------------------------------------------------
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const shots = [
    { src: "clip/v4_cheer.mp4", start: 6.4, word: "HỌC." },
    { src: "img/p18.jpg", word: "LÀM." },
    { src: "clip/v5_balloons.mp4", word: "KẾT NỐI." },
    { src: "img/p05.jpg", word: "TRƯỞNG THÀNH." },
  ];
  const each = 0.82;
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      {shots.map((s, i) => (
        <Sequence key={i} from={sec(i * each)} durationInFrames={sec(each) + 1}>
          <MediaFill
            m={{
              src: s.src,
              kind: s.src.endsWith(".mp4") ? "video" : "img",
              startFrom: (s as any).start ?? 0,
              still: true,
              autoFit: true,
            }}
            dur={sec(each)}
          />
          <AbsoluteFill style={{ backgroundColor: "rgba(10,26,74,0.35)" }} />
          <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
            <HookWord text={s.word} />
          </AbsoluteFill>
        </Sequence>
      ))}
      {shots.map((_, i) => (
        <Sfx key={i} at={i * each} name="click-soft" vol={0.45} />
      ))}
    </AbsoluteFill>
  );
};
const HookWord: React.FC<{ text: string }> = ({ text }) => {
  const f = useCurrentFrame();
  const p = pop(f, 0, FPS, 9);
  return (
    <div
      style={{
        fontFamily: FONT,
        fontWeight: 900,
        fontSize: 190,
        color: C.white,
        letterSpacing: -4,
        transform: `scale(${1.5 - 0.5 * p})`,
        opacity: Math.min(1, p * 2),
        textShadow: "0 12px 40px rgba(0,0,0,0.45)",
      }}
    >
      {text}
    </div>
  );
};

// ---------------------------------------------------------------------------
const Name: React.FC = () => {
  const f = useCurrentFrame();
  const t0 = L("name", "name", 11.06);
  const t1 = L("name", "name", 12.18);
  const bar = ease(f, t0, t0 + 0.6);
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <FitCard src="slide/s01.jpg" at={0.05} cx={1460} cy={540} maxW={760} maxH={780} rot={2} from="right" />
      <div style={{ ...W, left: 130, top: 300, width: 980 }}>
        <Tag text="HaUI · Trường Kinh tế" at={0.05} bg={C.yellow} size={34} />
        <Rise text="Khoa" at={t0} size={72} weight={600} color={C.sky} style={{ marginTop: 40 }} />
        <Rise text="Kinh doanh số" at={t0 + 0.12} size={128} style={{ whiteSpace: "nowrap" }} />
        <div style={{ height: 10, width: 560 * bar, backgroundColor: C.coral, borderRadius: 5, margin: "18px 0 30px" }} />
        <Rise
          text="Trường Kinh tế · Đại học Công nghiệp Hà Nội"
          at={t1}
          size={40}
          weight={600}
          stagger={0.04}
          color="rgba(255,255,255,0.85)"
        />
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Network: React.FC<{ opacity?: number }> = ({ opacity = 1 }) => {
  const f = useCurrentFrame();
  const nodes = Array.from({ length: 22 }, (_, i) => {
    const a = i * 2.39996;
    const r = 180 + ((i * 97) % 330);
    return {
      x: 960 + Math.cos(a + f / 400) * r * 1.6,
      y: 540 + Math.sin(a + f / 400) * r * 0.9,
    };
  });
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", opacity }}>
      {nodes.map((n, i) =>
        nodes.slice(i + 1).map((m, j) => {
          const d = Math.hypot(n.x - m.x, n.y - m.y);
          if (d > 330) return null;
          return (
            <line key={`${i}-${j}`} x1={n.x} y1={n.y} x2={m.x} y2={m.y} stroke={C.sky} strokeOpacity={0.25 * (1 - d / 330)} strokeWidth={2} />
          );
        }),
      )}
      {nodes.map((n, i) => (
        <circle key={i} cx={n.x} cy={n.y} r={i % 4 === 0 ? 7 : 4} fill={i % 5 === 0 ? C.yellow : C.sky} opacity={0.7} />
      ))}
    </svg>
  );
};

const Found: React.FC = () => {
  const f = useCurrentFrame();
  const tDate = L("found", "found", 20.56);
  const tNext = L("found", "found", 23.08);
  const tMission = L("found", "found", 26.1);
  const tTrain = L("found", "found", 28.48);
  const phase2 = ease(f, tMission - 0.3, tMission + 0.3);
  const digits = ["0", "1", ".", "0", "7", ".", "2", "0", "2", "4"];
  const dAt = [L("found", "found", 20.96), L("found", "found", 21.14), L("found", "found", 21.46)];
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <Network opacity={0.35 + 0.65 * phase2} />
      {/* date */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: 1 - phase2, transform: `translateY(${-160 * phase2}px)` }}>
        <Rise text="Thành lập" at={tDate - 0.3} size={56} weight={600} color={C.sky} />
        <div style={{ display: "flex", marginTop: 10 }}>
          {digits.map((d, i) => {
            const group = i < 2 ? 0 : i < 5 ? 1 : 2;
            const p = pop(f, dAt[group] + (i % 5) * 0.04, FPS, 11);
            return (
              <span key={i} style={{ fontFamily: FONT, fontWeight: 900, fontSize: 230, color: d === "." ? C.coral : C.white, letterSpacing: -6, display: "inline-block", transform: `translateY(${(1 - p) * 120}px)`, opacity: Math.min(1, p * 2) }}>
                {d}
              </span>
            );
          })}
        </div>
        <Rise text="Tiếp nối những nền tảng đã được vun đắp" at={tNext} size={44} weight={600} color="rgba(255,255,255,0.8)" stagger={0.05} />
      </AbsoluteFill>
      {/* mission */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: phase2 }}>
        <Tag text="Hướng đi rõ ràng" at={tMission} bg={C.coral} color={C.white} size={40} />
        <Rise
          text="Đào tạo nhân lực cho nền kinh tế số"
          at={tTrain}
          size={104}
          style={{ textAlign: "center", width: 1500, marginTop: 40 }}
          highlight={["kinh", "tế", "số"]}
        />
      </AbsoluteFill>
      <Sfx at={dAt[0]} name="pop" />
      <Sfx at={tTrain} name="whoosh-short" vol={0.25} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Majors: React.FC = () => {
  const f = useCurrentFrame();
  const items = [
    { name: "Marketing", sub: "", club: "CLB MC8", logo: "slide/s04.jpg", icon: "megaphone" as const, at: L("majors", "majors", 31.8), col: C.coral },
    { name: "Logistics &", sub: "Quản lý chuỗi cung ứng", club: "CLB SELOG", logo: "slide/s05.jpg", icon: "truck" as const, at: L("majors", "majors", 32.66), col: C.yellow },
    { name: "Phân tích", sub: "dữ liệu kinh doanh", club: "CLB SEAL", logo: "slide/s06.jpg", icon: "chart" as const, at: L("majors", "majors", 34.62), col: C.sky },
  ];
  return (
    <AbsoluteFill>
      <Bg tone="cream" />
      <div style={{ ...W, left: 0, right: 0, top: 110, textAlign: "center" }}>
        <Rise text="3 ngành học" at={0.1} size={80} color={C.navy} style={{ display: "inline-block" }} highlight={["3"]} accent={C.blue} />
      </div>
      <div style={{ ...W, left: 130, right: 130, top: 250, display: "flex", gap: 60 }}>
        {items.map((it, i) => {
          const p = pop(f, it.at, FPS, 12);
          const prog = ease(f, it.at, it.at + 1.4);
          return (
            <div
              key={i}
              style={{
                flex: 1,
                height: 720,
                backgroundColor: C.navy,
                borderRadius: 40,
                padding: "40px 36px",
                transform: `translateY(${(1 - p) * 300}px) scale(${0.85 + 0.15 * p})`,
                opacity: Math.min(1, p * 2),
                boxShadow: "0 30px 60px rgba(10,26,74,0.25)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "space-between",
                textAlign: "center",
                borderTop: `14px solid ${it.col}`,
              }}
            >
              <Icon kind={it.icon} size={170} color={it.col} progress={prog} />
              <div style={{ fontFamily: FONT, color: C.white, minHeight: 130 }}>
                <div style={{ fontWeight: 800, fontSize: 52, lineHeight: 1.1 }}>{it.name}</div>
                <div style={{ fontWeight: 600, fontSize: 34, lineHeight: 1.2, color: "rgba(255,255,255,0.75)", marginTop: 8 }}>{it.sub}</div>
              </div>
              <div style={{ width: "100%" }}>
                <div style={{ height: 170, backgroundColor: "#fff", borderRadius: 18, padding: 8 }}>
                  <Img src={staticFile(`kds/${it.logo}`)} style={{ width: "100%", height: "100%", objectFit: "contain" }} />
                </div>
                <div style={{ fontFamily: FONT, fontWeight: 700, fontSize: 30, color: it.col, marginTop: 14 }}>{it.club}</div>
              </div>
            </div>
          );
        })}
      </div>
      {items.map((it, i) => (
        <Sfx key={i} at={it.at} name="pop" />
      ))}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const WORLD = feature(world as any, (world as any).objects.countries);
const PROJ = geoNaturalEarth1().scale(205).translate([560, 300]);
const PATH = geoPath(PROJ);
const HOME: [number, number] = [105.8, 21.0];
const PINS = [
  { name: "Mỹ", ll: [-98, 39], at: 54.66, kind: "home" },
  { name: "Anh", ll: [-1.5, 52.5], at: 54.92, kind: "home", dx: -50, dy: -6 },
  { name: "Pháp", ll: [2.4, 46.6], at: 55.52, kind: "home", dx: 30, dy: 48 },
  { name: "Trung Quốc", ll: [104, 35], at: 55.98, kind: "home" },
  { name: "Úc", ll: [134, -25], at: 58.24, kind: "visit" },
  { name: "Canada", ll: [-106, 57], at: 58.7, kind: "visit" },
] as const;

const Faculty: React.FC = () => {
  const f = useCurrentFrame();
  const t19 = L("faculty", "faculty", 50.06);
  const tDr = L("faculty", "faculty", 51.38);
  const tMs = L("faculty", "faculty", 52.28);
  const tMap = L("faculty", "faculty", 53.38);
  const mapIn = ease(f, tMap - 0.2, tMap + 0.6);
  const [hx, hy] = PROJ(HOME);
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      {/* left: numbers */}
      <div style={{ ...W, left: 120, top: 190, width: 620 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 24 }}>
          <Counter to={19} at={t19} dur={0.6} size={260} color={C.yellow} />
          <Rise text="giảng viên" at={t19 + 0.2} size={60} />
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", width: 560, gap: 16, marginTop: 30 }}>
          {Array.from({ length: 19 }, (_, i) => {
            const isDr = i < 7;
            const p = pop(f, (isDr ? tDr : tMs) + (isDr ? i : i - 7) * 0.035, FPS, 12);
            return (
              <div key={i} style={{ width: 52, height: 52, borderRadius: 26, backgroundColor: isDr ? C.yellow : C.sky, transform: `scale(${p})` }} />
            );
          })}
        </div>
        <div style={{ display: "flex", gap: 50, marginTop: 34 }}>
          <Legend at={tDr} color={C.yellow} n="7" label="tiến sĩ" />
          <Legend at={tMs} color={C.sky} n="12" label="thạc sĩ" />
        </div>
      </div>
      {/* right: map */}
      <div style={{ ...W, left: 760, top: 200, width: 1120, height: 640, opacity: mapIn, transform: `translateX(${(1 - mapIn) * 120}px)` }}>
        <svg width={1120} height={640}>
          {(WORLD as any).features.map((ft: any, i: number) => (
            <path key={i} d={PATH(ft) || ""} fill="rgba(125,178,255,0.18)" stroke="rgba(125,178,255,0.35)" strokeWidth={0.8} />
          ))}
          {PINS.map((p, i) => {
            const at = L("faculty", "faculty", p.at);
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
                <circle cx={x} cy={y} r={11 + 22 * pp} fill="none" stroke={col} strokeOpacity={0.5 * (1 - pp) + 0.15} strokeWidth={2} />
                <text x={x + ((p as any).dx ?? 0)} y={y - 22 + ((p as any).dy ?? 0)} fill={C.white} fontFamily={FONT} fontWeight={800} fontSize={30} textAnchor="middle" opacity={pp}>
                  {p.name}
                </text>
              </g>
            );
          })}
          <circle cx={hx} cy={hy} r={13} fill={C.white} />
          <text x={hx + 18} y={hy + 36} fill={C.white} fontFamily={FONT} fontWeight={700} fontSize={26}>
            Hà Nội
          </text>
        </svg>
        <div style={{ display: "flex", gap: 40, fontFamily: FONT, fontWeight: 600, fontSize: 30, color: C.white, opacity: mapIn }}>
          <span><span style={{ color: C.yellow }}>●</span> nơi giảng viên được đào tạo</span>
          <span style={{ opacity: ease(f, L("faculty", "faculty", 57.26), L("faculty", "faculty", 57.8)) }}>
            <span style={{ color: C.coral }}>●</span> giảng viên thỉnh giảng quốc tế
          </span>
        </div>
      </div>
      <Sfx at={t19} name="impact-bass-1" vol={0.35} />
      {PINS.map((p, i) => (
        <Sfx key={i} at={L("faculty", "faculty", p.at) + 0.45} name="pop" vol={0.22} />
      ))}
    </AbsoluteFill>
  );
};
const Legend: React.FC<{ at: number; color: string; n: string; label: string }> = ({ at, color, n, label }) => {
  const f = useCurrentFrame();
  const p = pop(f, at, FPS, 14);
  return (
    <div style={{ fontFamily: FONT, color: C.white, opacity: p, transform: `translateY(${(1 - p) * 30}px)` }}>
      <span style={{ fontWeight: 900, fontSize: 72, color }}>{n}</span>
      <span style={{ fontWeight: 600, fontSize: 38, marginLeft: 12 }}>{label}</span>
    </div>
  );
};

// ---------------------------------------------------------------------------
const Learn: React.FC = () => {
  const f = useCurrentFrame();
  const lines = [
    { t: "Học không chỉ để biết", at: L("learn", "learn", 66.88), size: 84, color: "rgba(255,255,255,0.75)" },
    { t: "Học là để HIỂU", at: L("learn", "learn", 68.14), size: 120, hl: ["HIỂU"] },
    { t: "để LÀM", at: L("learn", "learn", 69.22), size: 120, hl: ["LÀM"] },
    { t: "và để SẴN SÀNG bước vào nghề", at: L("learn", "learn", 69.7), size: 92, hl: ["SẴN", "SÀNG"] },
  ];
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <FitCard src="slide/s12.jpg" at={0.2} cx={1520} cy={300} maxW={620} maxH={380} rot={2} from="right" />
      <FitCard src="slide/s40.jpg" at={1.2} cx={1650} cy={850} maxW={440} maxH={290} rot={-2} from="right" />
      <div style={{ ...W, left: 130, top: 170 }}>
        <Tag text="Ở Kinh doanh số" at={0.05} size={36} />
        <div style={{ marginTop: 40, display: "flex", flexDirection: "column", gap: 14 }}>
          {lines.map((l, i) => (
            <Rise key={i} text={l.t} at={l.at} size={l.size} color={l.color} highlight={l.hl} stagger={0.05} />
          ))}
        </div>
      </div>
      {lines.slice(1).map((l, i) => (
        <Sfx key={i} at={l.at} name="click-soft" vol={0.35} />
      ))}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Research: React.FC = () => {
  const stats = [
    { n: 50, suf: "+", label: "bài báo ISI & Scopus", at: L("research", "research", 79.96), col: C.yellow },
    { n: 125, pre: "~", label: "sinh viên NCKH mỗi năm", at: L("research", "research", 82.3), col: C.sky },
    { n: 25, label: "đề tài mỗi năm", at: L("research", "research", 83.78), col: C.coral },
  ];
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <FitCard src="slide/s15.jpg" at={0.1} cx={1440} cy={360} maxW={700} maxH={460} rot={-2} from="right" />
      <FitCard src="slide/s16.jpg" at={L("research", "research", 85.0) - 1.6} cx={1500} cy={800} maxW={560} maxH={340} rot={3} from="down" />
      <div style={{ ...W, left: 130, top: 150, width: 960 }}>
        <Rise text="Nghiên cứu khoa học" at={L("research", "research", 76.82)} size={80} style={{ whiteSpace: "nowrap" }} highlight={["khoa", "học"]} accent={C.sky} />
        <Rise text="một phần quan trọng của đời sống học thuật" at={L("research", "research", 78.0)} size={38} weight={600} color="rgba(255,255,255,0.75)" stagger={0.04} />
        <div style={{ marginTop: 60, display: "flex", flexDirection: "column", gap: 28 }}>
          {stats.map((s, i) => (
            <div key={i} style={{ display: "flex", alignItems: "baseline", gap: 28 }}>
              <div style={{ width: 330, textAlign: "right" }}>
                <Counter to={s.n} at={s.at} dur={0.8} size={130} color={s.col} prefix={s.pre} suffix={s.suf} />
              </div>
              <Rise text={s.label} at={s.at + 0.15} size={40} weight={600} stagger={0.04} style={{ whiteSpace: "nowrap" }} />
            </div>
          ))}
        </div>
      </div>
      {stats.map((s, i) => (
        <Sfx key={i} at={s.at} name="pop" />
      ))}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Life: React.FC = () => {
  const cuts = [
    { src: "clip/v5_banner.mp4", from: 0, to: L("life", "life", 95.0) },
    { src: "img/p02.jpg", from: L("life", "life", 95.0), to: L("life", "life", 96.42) },
    { src: "img/p19.jpg", from: L("life", "life", 96.42), to: L("life", "life", 97.14), portrait: true },
    { src: "img/p20.jpg", from: L("life", "life", 97.14), to: L("life", "life", 97.84), portrait: true },
    { src: "clip/v5_circle.mp4", from: L("life", "life", 97.84), to: L("life", "life", 98.82) },
    { src: "img/p21.jpg", from: L("life", "life", 98.82), to: SC.life[1] - SC.life[0] },
  ];
  const tags = [
    { t: "Cuộc thi", at: L("life", "life", 96.42), x: 150, y: 640, bg: C.yellow },
    { t: "Workshop", at: L("life", "life", 97.14), x: 520, y: 760, bg: C.coral, c: C.white },
    { t: "Ngoại khóa", at: L("life", "life", 97.84), x: 940, y: 650, bg: C.sky },
    { t: "Những người bạn", at: L("life", "life", 98.82), x: 1240, y: 790, bg: C.white },
  ];
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      {cuts.map((c, i) => (
        <Sequence key={i} from={sec(c.from)} durationInFrames={Math.max(1, sec(c.to - c.from))}>
          <MediaFill m={{ src: c.src, kind: c.src.endsWith(".mp4") ? "video" : "img", portrait: (c as any).portrait, still: true, autoFit: true }} dur={sec(c.to - c.from)} />
        </Sequence>
      ))}
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(10,26,74,0.75) 0%, rgba(10,26,74,0) 45%), linear-gradient(180deg, rgba(10,26,74,0.7) 0%, rgba(10,26,74,0) 40%)" }} />
      <div style={{ ...W, left: 130, top: 110 }}>
        <Rise text="Thanh xuân đại học" at={0.15} size={96} style={{ textShadow: "0 8px 30px rgba(0,0,0,0.5)" }} />
        <Rise text="không chỉ có giờ lên lớp" at={L("life", "life", 94.58)} size={56} weight={600} style={{ textShadow: "0 8px 30px rgba(0,0,0,0.5)" }} />
      </div>
      {tags.map((t, i) => (
        <div key={i} style={{ ...W, left: t.x, top: t.y }}>
          <Tag text={t.t} at={t.at} bg={t.bg} color={(t as any).c ?? C.ink} size={52} />
        </div>
      ))}
      {tags.map((t, i) => (
        <Sfx key={i} at={t.at} name="pop" vol={0.3} />
      ))}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Logi: React.FC = () => {
  const f = useCurrentFrame();
  const tTitle = L("logi", "logi", 100.4);
  const t2022 = L("logi", "logi", 102.16);
  const tSeasons = L("logi", "logi", 103.5);
  const tTeams = L("logi", "logi", 105.16);
  const tStud = L("logi", "logi", 106.44);
  const line = ease(f, t2022, tSeasons + 0.8);
  return (
    <AbsoluteFill>
      <Bg tone="cream" />
      <FitCard src="slide/s18.jpg" at={0.1} cx={1390} cy={400} maxW={820} maxH={540} rot={2} from="right" border={C.navy} />
      <div style={{ ...W, left: 130, top: 140, width: 820 }}>
        <Tag text="Với sinh viên Logistics" at={0.05} bg={C.navy} color={C.white} size={32} />
        <Rise text="HaUI LogiMaster" at={tTitle} size={104} color={C.navy} style={{ marginTop: 30 }} highlight={["LogiMaster"]} accent={C.blue} />
      </div>
      {/* timeline */}
      <div style={{ ...W, left: 130, top: 520, width: 760, height: 120 }}>
        <div style={{ ...W, left: 0, top: 50, height: 8, width: 740 * line, backgroundColor: C.navy, borderRadius: 4 }} />
        {[0, 1, 2, 3].map((i) => {
          const p = pop(f, tSeasons + i * 0.18, FPS, 10);
          return (
            <div key={i} style={{ ...W, left: i * 240 - 20, top: 30, textAlign: "center", width: 48 }}>
              <div style={{ width: 48, height: 48, borderRadius: 24, backgroundColor: i === 0 ? C.coral : C.blue, transform: `scale(${p})` }} />
              <div style={{ fontFamily: FONT, fontWeight: 700, fontSize: 26, color: C.navy, marginTop: 10, opacity: p, whiteSpace: "nowrap", marginLeft: i === 0 ? 0 : -10 }}>
                {i === 0 ? "2022" : `Mùa ${i + 1}`}
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ ...W, left: 130, top: 720, display: "flex", gap: 90 }}>
        <Stat at={tSeasons} n={4} label="mùa thi" />
        <Stat at={tTeams} n={25} pre="~" label="đội / mùa" />
        <Stat at={tStud} n={100} pre="~" label="sinh viên / mùa" />
      </div>
      <Sfx at={tTitle} name="whoosh-short" vol={0.25} />
      <Sfx at={tTeams} name="pop" />
      <Sfx at={tStud} name="pop" />
    </AbsoluteFill>
  );
};
const Stat: React.FC<{ at: number; n: number; label: string; pre?: string; color?: string; dark?: boolean }> = ({ at, n, label, pre, color = C.blue, dark }) => (
  <div>
    <Counter to={n} at={at} dur={0.7} size={120} color={color} prefix={pre} />
    <Rise text={label} at={at + 0.1} size={36} weight={600} color={dark ? C.white : C.navy} stagger={0.04} />
  </div>
);

// ---------------------------------------------------------------------------
const MJ: React.FC = () => {
  const f = useCurrentFrame();
  const tTitle = L("mj", "mj", 122.6);
  const t65 = L("mj", "mj", 123.82);
  const t124 = L("mj", "mj", 125.34);
  const t360 = L("mj", "mj", 127.08);
  const tUni = L("mj", "mj", 128.86);
  const maxH = 300;
  const bar = (at: number, v: number) => (maxH * v * ease(f, at, at + 0.9)) / 124;
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <FitCard src="slide/s19.jpg" at={0.1} cx={1460} cy={330} maxW={680} maxH={420} rot={-2} from="right" />
      <div style={{ ...W, left: 130, top: 120, width: 900 }}>
        <Tag text="Với sinh viên Marketing · CLB MC8" at={0.05} bg={C.coral} color={C.white} size={32} />
        <Rise text="Marketing Journey" at={tTitle} size={88} style={{ marginTop: 30, whiteSpace: "nowrap" }} highlight={["Journey"]} accent={C.coral} />
      </div>
      {/* bars */}
      <div style={{ ...W, left: 170, top: 420, width: 760, height: 580 }}>
        {[
          { label: "Mùa đầu", v: 65, at: t65, col: C.sky, x: 0 },
          { label: "Mùa tiếp theo", v: 124, at: t124, col: C.yellow, x: 340 },
        ].map((b, i) => {
          const h = bar(b.at, b.v);
          return (
            <div key={i} style={{ ...W, left: b.x, bottom: 70, width: 230 }}>
              <div style={{ textAlign: "center", marginBottom: 12 }}>
                <Counter to={b.v} at={b.at} dur={0.9} size={84} color={b.col} />
                <div style={{ fontFamily: FONT, fontWeight: 600, fontSize: 30, color: C.white, opacity: ease(f, b.at, b.at + 0.4) }}>đội thi</div>
              </div>
              <div style={{ height: h, backgroundColor: b.col, borderRadius: "18px 18px 0 0" }} />
              <div style={{ ...W, bottom: -56, width: 230, textAlign: "center", fontFamily: FONT, fontWeight: 700, fontSize: 30, color: "rgba(255,255,255,0.8)" }}>{b.label}</div>
            </div>
          );
        })}
        <div style={{ ...W, left: 0, bottom: 68, width: 600, height: 4, backgroundColor: "rgba(255,255,255,0.4)" }} />
      </div>
      <div style={{ ...W, left: 1120, top: 620 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 20 }}>
          <Counter to={360} at={t360} dur={0.9} size={130} color={C.yellow} suffix="+" />
          <Rise text="thí sinh" at={t360 + 0.2} size={52} />
        </div>
        <div style={{ display: "flex", gap: 18, marginTop: 30 }}>
          {["NEU", "FTU", "Học viện Ngân hàng", "…"].map((u, i) => (
            <Tag key={i} text={u} at={tUni + i * 0.15} bg={C.white} size={32} />
          ))}
        </div>
      </div>
      <Sfx at={t65} name="pop" />
      <Sfx at={t124} name="pop" />
      <Sfx at={t360} name="impact-bass-1" vol={0.3} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Partners: React.FC = () => {
  const f = useCurrentFrame();
  const tLine = L("partners", "partners", 141.78);
  const tNet = L("partners", "partners", 144.76);
  const fade1 = ease(f, tNet - 0.5, tNet + 0.1);
  const cx = 960;
  const cy = 600;
  const nodes = [
    { t: "Hiệp hội nghề nghiệp", at: L("partners", "partners", 145.56), a: 200, r: 380, col: C.sky },
    { t: "Cộng đồng chuyên môn", at: L("partners", "partners", 146.24), a: 245, r: 420, col: C.sky },
    { t: "Doanh nghiệp", at: L("partners", "partners", 147.26), a: 295, r: 380, col: C.sky },
    { t: "Viettel Post", at: L("partners", "partners", 148.24), a: 340, r: 560, col: C.yellow },
    { t: "Smartlog", at: L("partners", "partners", 149.2), a: 25, r: 520, col: C.yellow },
    { t: "MISA", at: L("partners", "partners", 150.02), a: 150, r: 520, col: C.white },
    { t: "TDS", at: L("partners", "partners", 150.68), a: 115, r: 500, col: C.white },
    { t: "Đối tác Marketing", at: L("partners", "partners", 151.62), a: 70, r: 420, col: C.coral },
  ];
  const pos = (a: number, r: number) => [cx + Math.cos((a * Math.PI) / 180) * r * 1.25, cy + Math.sin((a * Math.PI) / 180) * r * 0.62];
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <AbsoluteFill style={{ opacity: 1 - fade1 }}>
        <FitCard src="slide/s24.jpg" at={0} cx={1560} cy={540} maxW={620} maxH={700} rot={2} from="right" />
        <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(10,26,74,0.95) 0%, rgba(10,26,74,0.7) 60%, rgba(10,26,74,0.2) 100%)" }} />
        <div style={{ ...W, left: 130, top: 330, width: 1100 }}>
          <Rise text="Tri thức ý nghĩa hơn" at={tLine} size={104} />
          <Rise text="khi được kết nối với thực tiễn" at={tLine + 0.85} size={72} weight={600} highlight={["thực", "tiễn"]} />
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
        <div style={{ ...W, left: cx - 140, top: cy - 140, width: 280, height: 280, borderRadius: 140, backgroundColor: C.blue, border: `8px solid ${C.white}`, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", transform: `scale(${pop(f, tNet, FPS, 11)})`, boxShadow: "0 0 80px rgba(31,71,224,0.7)" }}>
          <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 72, color: C.white, lineHeight: 1 }}>KDS</div>
          <div style={{ fontFamily: FONT, fontWeight: 600, fontSize: 24, color: C.white, opacity: 0.85, textAlign: "center" }}>Khoa Kinh doanh số</div>
        </div>
        {nodes.map((n, i) => {
          const [x, y] = pos(n.a, n.r);
          return (
            <div key={i} style={{ ...W, left: x, top: y, transform: "translate(-50%, -50%)" }}>
              <Tag text={n.t} at={n.at + 0.2} bg={n.col} color={n.col === C.coral ? C.white : C.ink} size={i < 3 ? 34 : 44} />
            </div>
          );
        })}
        <div style={{ ...W, left: 130, top: 80 }}>
          <Rise text="Khoa đồng hành cùng" at={tNet} size={56} weight={700} />
        </div>
      </AbsoluteFill>
      {nodes.map((n, i) => (
        <Sfx key={i} at={n.at + 0.2} name="pop" vol={0.2} />
      ))}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Questions: React.FC = () => {
  const f = useCurrentFrame();
  const tQ = L("questions", "questions", 157.84);
  const out1 = ease(f, tQ - 0.2, tQ + 0.4);
  const acts = [
    { t: "Tham quan doanh nghiệp", at: L("questions", "questions", 154.04), src: "slide/s27.jpg", x: 480, y: 290, rot: -2 },
    { t: "Kiến tập", at: L("questions", "questions", 155.14), src: "slide/s26.jpg", x: 1400, y: 280, rot: 2 },
    { t: "Thực tập", at: L("questions", "questions", 155.8), src: "slide/s24.jpg", x: 560, y: 790, rot: 2 },
    { t: "Tọa đàm chuyên môn", at: L("questions", "questions", 156.64), src: "slide/s28.jpg", x: 1420, y: 780, rot: -2 },
  ];
  const qs = [
    { t: "Mình đang học gì?", at: L("questions", "questions", 159.86) },
    { t: "Mình có thể làm gì?", at: L("questions", "questions", 161.06) },
    { t: "Mình muốn trở thành ai?", at: L("questions", "questions", 162.54), hl: true },
  ];
  return (
    <AbsoluteFill>
      <Bg tone="navy" />
      <AbsoluteFill style={{ opacity: 1 - out1, transform: `scale(${1 + 0.1 * out1})` }}>
        {acts.map((a, i) => (
          <React.Fragment key={i}>
            <FitCard src={a.src} at={a.at} cx={a.x} cy={a.y} maxW={640} maxH={400} rot={a.rot} from={i % 2 ? "right" : "left"} />
            <div style={{ ...W, left: a.x - 200, top: a.y + 150 }}>
              <Tag text={a.t} at={a.at + 0.15} size={40} />
            </div>
          </React.Fragment>
        ))}
      </AbsoluteFill>
      <AbsoluteFill style={{ opacity: out1, justifyContent: "center", paddingLeft: 180 }}>
        <Rise text="3 câu hỏi" at={tQ} size={44} weight={700} color={C.sky} />
        <div style={{ display: "flex", flexDirection: "column", gap: 20, marginTop: 30 }}>
          {qs.map((q, i) => (
            <Rise key={i} text={q.t} at={q.at} size={q.hl ? 118 : 96} color={q.hl ? C.yellow : C.white} stagger={0.05} />
          ))}
        </div>
      </AbsoluteFill>
      {acts.map((a, i) => (
        <Sfx key={i} at={a.at} name="whoosh-short" vol={0.18} />
      ))}
      {qs.map((q, i) => (
        <Sfx key={`q${i}`} at={q.at} name="click-soft" vol={0.35} />
      ))}
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
      <KImg src="slide/s29.jpg" style={{ position: "absolute", inset: 0 }} zoom={0} />
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(10,26,74,0.97) 0%, rgba(10,26,74,0.9) 55%, rgba(10,26,74,0.45) 100%)" }} />
      <div style={{ ...W, left: 130, top: 120 }}>
        <Tag text="Thành quả" at={0.05} size={36} />
      </div>
      <div style={{ ...W, left: 130, right: 130, top: 500, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <Counter to={3} at={t3} dur={0.4} size={140} color={C.white} />
          <Rise text="chương trình đào tạo" at={t3 + 0.1} size={38} weight={600} />
        </div>
        <div>
          <Counter to={1000} at={t1000} dur={1.0} size={140} color={C.yellow} suffix="+" thousands />
          <Rise text="sinh viên tốt nghiệp" at={t1000 + 0.2} size={38} weight={600} />
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 30 }}>
          <div style={{ position: "relative", width: 2 * R + 40, height: 2 * R + 40 }}>
            <svg width={2 * R + 40} height={2 * R + 40}>
              <circle cx={R + 20} cy={R + 20} r={R} fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth={26} />
              <circle cx={R + 20} cy={R + 20} r={R} fill="none" stroke={C.coral} strokeWidth={26} strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - ring)} transform={`rotate(-90 ${R + 20} ${R + 20})`} />
            </svg>
            <div style={{ ...W, inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <Counter to={90} at={t90} dur={1.2} size={80} color={C.white} suffix="%" />
            </div>
          </div>
          <Rise text="sinh viên có việc làm sau 6 tháng" at={L("outcomes", "outcomes", 169.12)} size={38} weight={600} style={{ width: 300 }} />
        </div>
      </div>
      <Sfx at={t1000} name="pop" />
      <Sfx at={t90} name="riser" vol={0.18} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Outro: React.FC = () => {
  const f = useCurrentFrame();
  const pics = [
    "slide/s33.jpg", "img/p12.jpg", "slide/s39.jpg", "img/p14.jpg", "img/p05.jpg", "slide/s29.jpg",
    "img/p16.jpg", "slide/s01.jpg", "slide/s42.jpg", "img/p09.jpg", "slide/s19.jpg", "img/p21.jpg",
  ];
  const cols = 4;
  const cw = 1920 / cols;
  const ch = 1080 / 3;
  const tName = L("outro", "outro", 187.4);
  const tSub = L("outro", "outro", 188.74);
  const words = [
    { t: "Học tập", at: L("outro", "outro", 191.52), c: C.sky },
    { t: "Trải nghiệm", at: L("outro", "outro", 192.24), c: C.yellow },
    { t: "Trưởng thành", at: L("outro", "outro", 192.96), c: C.coral },
  ];
  const panel = pop(f, tName - 0.1, FPS, 16);
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      {pics.map((src, i) => (
        <FitCard key={i} src={src} at={i * 0.06} cx={(i % cols) * cw + cw / 2} cy={Math.floor(i / cols) * ch + ch / 2} maxW={cw - 50} maxH={ch - 50} rot={i % 2 ? 2.5 : -2.5} from="scale" />
      ))}
      <AbsoluteFill style={{ backgroundColor: `rgba(10,26,74,${0.55 * panel})` }} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <div style={{ backgroundColor: C.navy, borderRadius: 40, padding: "60px 90px", transform: `scale(${0.8 + 0.2 * panel})`, opacity: panel, textAlign: "center", boxShadow: "0 40px 100px rgba(0,0,0,0.5)", border: `6px solid ${C.yellow}` }}>
          <Rise text="Khoa Kinh doanh số" at={tName} size={120} style={{ justifyContent: "center" }} />
          <Rise text="Trường Kinh tế · Đại học Công nghiệp Hà Nội" at={tSub} size={40} weight={600} color="rgba(255,255,255,0.85)" stagger={0.04} />
          <div style={{ display: "flex", gap: 30, justifyContent: "center", marginTop: 40 }}>
            {words.map((w, i) => (
              <Tag key={i} text={w.t} at={w.at} bg={w.c} size={50} color={C.ink} />
            ))}
          </div>
        </div>
      </AbsoluteFill>
      {words.map((w, i) => (
        <Sfx key={i} at={w.at} name="pop" vol={0.3} />
      ))}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const Cheer: React.FC = () => {
  const f = useCurrentFrame();
  const p = pop(f, 0.6, FPS, 14);
  const end = interpolate(f, [sec(3.6), sec(4.3)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      <MediaFill m={{ src: "clip/v4_cheer.mp4", kind: "video", startFrom: 5.2 }} dur={sec(4.3)} />
      <Sequence from={0} layout="none">
        <Audio src={staticFile("kds/clip/v4_cheer.mp4")} startFrom={sec(5.2)} volume={(fr) => interpolate(fr, [0, 6, sec(3.4), sec(4.3)], [0, 0.85, 0.85, 0], { extrapolateRight: "clamp" })} />
      </Sequence>
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(10,26,74,0.85) 0%, rgba(10,26,74,0) 40%)" }} />
      <div style={{ ...W, left: 0, right: 0, bottom: 90, textAlign: "center", opacity: p, transform: `translateY(${(1 - p) * 40}px)` }}>
        <div style={{ fontFamily: FONT, fontWeight: 900, fontSize: 84, color: C.white }}>
          Chào mừng đến với <span style={{ color: C.yellow }}>Kinh doanh số!</span>
        </div>
      </div>
      <AbsoluteFill style={{ backgroundColor: C.navy, opacity: end }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
const SCENES: [SceneId, React.FC][] = [
  ["hook", Hook],
  ["name", Name],
  ["found", Found],
  ["majors", Majors],
  ["faculty", Faculty],
  ["learn", Learn],
  ["research", Research],
  ["life", Life],
  ["logi", Logi],
  ["mj", MJ],
  ["partners", Partners],
  ["questions", Questions],
  ["outcomes", Outcomes],
  ["outro", Outro],
  ["cheer", Cheer],
];

// Voice segments (for ducking the music bed)
const VOICE = Object.values(SEGS).map((s) => [s.at, s.at + s.dur]);
const musicVol = (fr: number) => {
  const t = fr / FPS;
  let duck = 0;
  for (const [a, b] of VOICE) {
    const k = interpolate(t, [a - 0.35, a, b, b + 0.5], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    duck = Math.max(duck, k);
  }
  const fadeTail = interpolate(t, [114.5, 116.5], [1, 0.25], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (1 - 0.45 * duck) * fadeTail;
};

export const VersionB: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: C.navy }}>
      <Fonts />
      {SCENES.map(([id, Comp]) => {
        const [a, b] = SC[id];
        return (
          <Sequence key={id} from={sec(a)} durationInFrames={sec(b) - sec(a)}>
            <Comp />
          </Sequence>
        );
      })}
      {/* wipes over each scene boundary (except into/out of the fast hook/life/cheer cuts) */}
      {(["name", "found", "majors", "faculty", "learn", "research", "life", "logi", "mj", "partners", "questions", "outcomes", "outro"] as SceneId[]).map((id, i) => (
        <Sequence key={`w${id}`} from={sec(SC[id][0]) - 7} durationInFrames={18}>
          <Wipe color={i % 2 ? C.yellow : C.coral} color2={i % 2 ? C.blue : C.yellow} />
        </Sequence>
      ))}
      {(["found", "faculty", "life", "mj", "questions", "outro"] as SceneId[]).map((id) => (
        <Sfx key={`ws${id}`} at={SC[id][0] - 0.25} name="whoosh" vol={0.18} />
      ))}
      <Grade />
      <Audio src={staticFile("kds/audio/voice_b.wav")} volume={1} />
      <Audio src={staticFile("kds/audio/music_b.wav")} volume={musicVol} />
    </AbsoluteFill>
  );
};
