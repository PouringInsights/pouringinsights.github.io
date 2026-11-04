import React from "react";
import { AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Captions, clamp, f, Field, P, Paper, ramp, Rise, T, Wash, WashFilter, Word } from "../watercolor/engine";

// V60 adds one pigment: Prussian blue, a deep glass-lab blue that carries paper ink at AA contrast.
const PRUSSIAN = "#1F4E79";

export type Beats = {
  lab: number; erlen: number; fold: number; cone: number; years: number; y2005: number;
  name: number; sixty: number; ribs: number; hole: number; take: number; slow: number; question: number;
};
export type V60Props = { audio: string; music: string | null; duration: number; words: Word[]; beats: Beats };
export const defaultProps: V60Props = {
  audio: "v60/vo.wav", music: null, duration: 52, words: [],
  beats: { lab: 4, erlen: 9, fold: 12.6, cone: 15.6, years: 22, y2005: 25.4, name: 28.5, sixty: 31.4, ribs: 33.2, hole: 36.2, take: 37, slow: 44.3, question: 46.2 },
};

// a painted glass shape: wash fill + a darker drawn contour
const Glass: React.FC<{ id: string; d: string; color: string; seed: number; p?: number; stroke?: string }> = ({ id, d, color, seed, p = 1, stroke = P.payne }) => (
  <g opacity={p}>
    <defs><WashFilter id={id} seed={seed} distort={14} body={0.5} rim={0.8} /></defs>
    <g style={{ mixBlendMode: "multiply" }}><path d={d} fill={color} filter={`url(#${id})`} /></g>
    <path d={d} fill="none" stroke={stroke} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" />
  </g>
);

// lab glass outlines, drawn around (0,0)
const FLASK = "M-40,-200 L40,-200 L40,-60 L150,170 Q160,200 130,200 L-130,200 Q-160,200 -150,170 L-40,-60 Z";
const FUNNEL = "M-170,-120 L170,-120 L30,60 L30,170 L-30,170 L-30,60 Z";
const BEAKER = "M-110,-150 L110,-150 L110,150 Q110,170 90,170 L-90,170 Q-110,170 -110,150 Z";
const DRIPPER = "M-210,-170 L210,-170 L40,150 L-40,150 Z";

// ── 1. Hook: a dripper and a flask, side by side ──────────────────────
const SceneHook: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <g transform="translate(330 1000)"><Glass id="hd" d={DRIPPER} color={P.crimson} seed={3} p={ramp(frame, 0, 14)} /></g>
        <g transform="translate(790 1010) scale(0.95)"><Glass id="hf" d={FLASK} color={P.cerulean} seed={5} p={ramp(frame, 8, 22)} /></g>
      </svg>
      <T size={230} color={P.payne} weight={900} style={{ position: "absolute", left: 80, top: 250 }}>V60</T>
      <Rise at={14} style={{ position: "absolute", left: 80, top: 1330, width: 900 }}>
        <T size={60} color={P.payne} weight={600}>bắt đầu từ phòng thí nghiệm hóa học</T>
      </Rise>
    </AbsoluteFill>
  );
};

// ── 2. 1921: a shelf of lab glass on a Payne's grey field ──────────────
const SceneLab: React.FC = () => {
  const frame = useCurrentFrame();
  const items = [
    { d: BEAKER, x: 250, s: 0.8, c: P.cerulean },
    { d: FLASK, x: 540, s: 0.75, c: P.leaf },
    { d: FUNNEL, x: 830, s: 0.8, c: P.hansa },
  ];
  return (
    <AbsoluteFill>
      <Paper />
      <Field id="lab" color={P.payne} ox={1080} oy={0} seed={12} />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        {items.map((it, i) => (
          <g key={i} transform={`translate(${it.x} 1080) scale(${it.s})`}>
            <Glass id={`lab${i}`} d={it.d} color={it.c} seed={20 + i} p={ramp(frame, 10 + i * 8, 24 + i * 8)} stroke={P.paper} />
          </g>
        ))}
        <rect x={80} y={1240} width={920} height={14} fill={P.paper} opacity={ramp(frame, 6, 20)} />
      </svg>
      <Rise at={4} style={{ position: "absolute", left: 80, top: 260 }}>
        <T size={230} color={P.paper} weight={900}>1921</T>
        <T size={60} color={P.paper} weight={600} style={{ marginTop: 10 }}>Hario, Tokyo: đồ thủy tinh cho phòng lab</T>
      </Rise>
    </AbsoluteFill>
  );
};

// ── 3. Signature: a round filter folded in quarters, opened into a cone ──
const sector = (r: number, a0: number, a1: number) => {
  const x0 = r * Math.cos(a0), y0 = r * Math.sin(a0), x1 = r * Math.cos(a1), y1 = r * Math.sin(a1);
  const large = a1 - a0 > Math.PI ? 1 : 0;
  return `M0,0 L${x0},${y0} A${r},${r} 0 ${large} 1 ${x1},${y1} Z`;
};
const SceneErlen: React.FC<{ foldAt: number }> = ({ foldAt }) => {
  const frame = useCurrentFrame();
  const r = frame - foldAt;
  // 0: full circle → 1: half → 2: quarter → 3: cone in funnel
  const k = interpolate(r, [0, 14, 26, 40, 56], [0, 1, 1, 2, 3], clamp);
  const span = k <= 1 ? 2 * Math.PI - k * Math.PI : k <= 2 ? Math.PI - (k - 1) * (Math.PI / 2) : Math.PI / 2;
  const toCone = Math.max(0, k - 2);
  const drip = interpolate(r, [56, 120], [0, 1], clamp);
  const paperX = interpolate(toCone, [0, 1], [540, 540]);
  const paperY = interpolate(toCone, [0, 1], [720, 860]);
  const rot = interpolate(toCone, [0, 1], [-90 - (span * 180) / Math.PI / 2, 45]);
  return (
    <AbsoluteFill>
      <Paper />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        {/* flask + funnel */}
        <g transform="translate(540 1330) scale(0.95)"><Glass id="ef" d={FLASK} color={P.cerulean} seed={31} p={ramp(frame, 0, 14)} /></g>
        <g transform="translate(540 960)"><Glass id="efu" d={FUNNEL} color={P.cerulean} seed={33} p={ramp(frame, 4, 18) * 0.9} /></g>
        {/* coffee collecting in the flask */}
        <Wash id="brew" seed={35} color={P.umber} cx={540} cy={1500} r={150} p={drip} body={0.85} rim={0.6} distort={12} />
        {[0, 1, 2].map((i) => {
          const t = ((r - 56 - i * 9) % 27) / 27;
          if (r < 56 + i * 9) return null;
          return <circle key={i} cx={540} cy={1140 + t * 220} r={9} fill={P.umber} opacity={1 - t * 0.5} />;
        })}
        {/* the filter paper */}
        <g transform={`translate(${paperX} ${paperY}) rotate(${rot}) scale(${1 - toCone * 0.35})`} opacity={ramp(frame, foldAt - 10, foldAt)}>
          <path d={sector(210, 0, span)} fill="#FBFBF8" stroke={P.greyblue} strokeWidth={6} strokeLinejoin="round" />
          {k > 0.9 && k < 2.9 ? <path d={`M0,0 L${210 * Math.cos(span / 2)},${210 * Math.sin(span / 2)}`} stroke={P.greyblue} strokeWidth={3} opacity={0.6} /> : null}
        </g>
      </svg>
      <Rise style={{ position: "absolute", left: 80, top: 230, width: 920 }}>
        <T size={92} color={P.payne}>Phễu Erlenmeyer</T>
        <T size={60} color={P.payne} weight={600} style={{ marginTop: 10 }}>+ giấy lọc gấp tư</T>
      </Rise>
      <Rise at={foldAt + 30} style={{ position: "absolute", left: 80, top: 450, width: 920 }}>
        <T size={42} color={P.payne} weight={600}>theo lời kể của chính Hario</T>
      </Rise>
    </AbsoluteFill>
  );
};

// ── 4. Why a cone: water converges, the bed gets deeper (Prussian field) ──
const SceneCone: React.FC = () => {
  const frame = useCurrentFrame();
  const draw = ramp(frame, 6, 36);
  const pts: string[] = [];
  for (let x = -1; x <= 1.0001; x += 0.02) pts.push(`${540 + x * 380},${1380 - x * x * 520}`);
  const len = 2200;
  return (
    <AbsoluteFill>
      <Paper />
      <Field id="pru" color={PRUSSIAN} ox={540} oy={1920} seed={14} />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <defs><clipPath id="bowl"><path d={`M${pts.join(" L")} Z`} /></clipPath></defs>
        <g clipPath="url(#bowl)">
          <Wash id="bed" seed={41} color={P.umber} cx={540} cy={1420} r={330} p={ramp(frame, 30, 60)} body={0.9} rim={0.6} distort={20} />
        </g>
        <path d={`M${pts.join(" L")}`} fill="none" stroke={P.paper} strokeWidth={10} strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - draw)} />
        {[-260, -130, 130, 260].map((x, i) => {
          const p = ramp(frame, 50 + i * 5, 80 + i * 5);
          const x1 = 540 + x, y1 = 780, x2 = 540 + x * (1 - p * 0.85), y2 = 780 + p * 520;
          return <path key={i} d={`M${x1},${y1} L${x2},${y2}`} stroke={P.hansa} strokeWidth={10} strokeLinecap="round" opacity={p > 0 ? 1 : 0} />;
        })}
      </svg>
      <Rise style={{ position: "absolute", left: 80, top: 250, width: 920 }}>
        <T size={92} color={P.paper}>Hình nón lọc tự nhiên nhất</T>
      </Rise>
      <Rise at={70} style={{ position: "absolute", left: 80, top: 1460, width: 920 }}>
        <T size={60} color={P.paper} weight={600}>nước dồn về giữa, lớp bột dày hơn, ngấm lâu hơn</T>
      </Rise>
    </AbsoluteFill>
  );
};

// ── 5. 1980 → 2005: one brush stroke of twenty-five years ──────────────
const SceneYears: React.FC<{ y2005At: number }> = ({ y2005At }) => {
  const frame = useCurrentFrame();
  const stroke = ramp(frame, 18, y2005At);
  return (
    <AbsoluteFill>
      <Paper />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <defs><WashFilter id="brush" seed={51} distort={26} body={0.8} rim={0.6} /></defs>
        <g style={{ mixBlendMode: "multiply" }}>
          <rect x={120} y={860} width={840 * stroke} height={70} rx={35} fill={P.greyblue} filter="url(#brush)" />
        </g>
      </svg>
      <Rise style={{ position: "absolute", left: 80, top: 420 }}>
        <T size={200} color={P.payne} weight={900}>1980</T>
        <T size={60} color={P.payne} weight={600}>chiếc phễu nón đầu tiên</T>
      </Rise>
      <Rise at={y2005At} style={{ position: "absolute", left: 80, top: 1060 }}>
        <T size={200} color={P.crimson} weight={900}>2005</T>
        <T size={60} color={P.payne} weight={600}>V60 ra đời</T>
      </Rise>
    </AbsoluteFill>
  );
};

// ── 6. Decoding the name on a crimson field: V, 60°, ribs, one hole ─────
const SceneName: React.FC<{ sixtyAt: number; ribsAt: number; holeAt: number }> = ({ sixtyAt, ribsAt, holeAt }) => {
  const frame = useCurrentFrame();
  const v = ramp(frame, 4, 26);
  const arc = ramp(frame, sixtyAt, sixtyAt + 20);
  const ribs = ramp(frame, ribsAt, ribsAt + 30);
  const hole = ramp(frame, holeAt, holeAt + 12);
  // apex at (540,1420), sides at ±30° from vertical (60° total), height 760
  const ax = 540, ay = 1420, h = 760, dx = h * Math.tan(Math.PI / 6);
  const L = 900;
  const arcR = 220;
  const a0 = -Math.PI / 2 - Math.PI / 6, a1 = -Math.PI / 2 - Math.PI / 6 + (Math.PI / 3) * arc;
  return (
    <AbsoluteFill>
      <Paper />
      <Field id="crimf" color={P.crimson} ox={0} oy={1920} seed={15} />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <path d={`M${ax - dx},${ay - h} L${ax},${ay} L${ax + dx},${ay - h}`} fill="none" stroke={P.paper} strokeWidth={16} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={L * 2} strokeDashoffset={L * 2 * (1 - v)} />
        {arc > 0 ? <path d={`M${ax + arcR * Math.cos(a0)},${ay + arcR * Math.sin(a0)} A${arcR},${arcR} 0 0 1 ${ax + arcR * Math.cos(a1)},${ay + arcR * Math.sin(a1)}`} fill="none" stroke={P.hansa} strokeWidth={10} strokeLinecap="round" /> : null}
        {[-0.62, -0.3, 0.02, 0.34, 0.66].map((o, i) => {
          const top = ay - h + 40, bottom = ay - 60;
          const x0 = ax + o * dx * 0.95;
          const len = 820;
          return (
            <path key={i} d={`M${x0},${top} Q${x0 + 120 * (o + 0.4)},${(top + bottom) / 2} ${ax + o * 30},${bottom}`} fill="none" stroke={P.paper} strokeOpacity={0.75} strokeWidth={6} strokeLinecap="round" strokeDasharray={len} strokeDashoffset={len * (1 - ribs)} />
          );
        })}
        {hole > 0 ? <circle cx={ax} cy={ay - 10} r={10 + hole * 34} fill={P.payne} stroke={P.paper} strokeWidth={6} /> : null}
      </svg>
      <T size={230} color={P.paper} weight={900} style={{ position: "absolute", left: 80, top: 200, opacity: v }}>V</T>
      <T size={150} color={P.hansa} weight={900} style={{ position: "absolute", left: 80, top: 1160, opacity: arc }}>60°</T>
      <Rise at={ribsAt + 6} style={{ position: "absolute", left: 640, top: 300 }}>
        <T size={60} color={P.paper} weight={600}>gân xoắn:<br />khí thoát ra<br />khi bột nở</T>
      </Rise>
      <Rise at={holeAt + 4} style={{ position: "absolute", left: 80, top: 1500 }}>
        <T size={92} color={P.paper}>một lỗ to</T>
      </Rise>
    </AbsoluteFill>
  );
};

// ── 7. The barista take: you set the speed ─────────────────────────────
const SceneTake: React.FC<{ slowAt: number }> = ({ slowAt }) => {
  const frame = useCurrentFrame();
  const fast = ramp(frame, 70, 100);
  const slow = ramp(frame, slowAt, slowAt + 30);
  return (
    <AbsoluteFill>
      <Paper />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <Wash id="fast" seed={61} color={P.hansa} cx={300} cy={1020} r={210} p={fast} body={0.45} rim={0.7} />
        <Wash id="slow" seed={63} color={P.umber} cx={780} cy={1080} r={210} p={slow} body={0.85} rim={0.6} />
        {/* pour streams: thin and quick vs thick and slow */}
        <rect x={296} y={620} width={8} height={330 * fast} fill={P.payne} />
        <rect x={770} y={620} width={20} height={360 * slow} fill={P.payne} />
      </svg>
      <Rise style={{ position: "absolute", left: 80, top: 240, width: 920 }}>
        <T size={92} color={P.payne}>Phễu không quyết định tốc độ.</T>
        <T size={92} color={P.crimson} style={{ marginTop: 10 }}>Bạn quyết định.</T>
      </Rise>
      <Rise at={70} style={{ position: "absolute", left: 80, top: 1330 }}>
        <T size={60} color={P.payne}>rót nhanh</T>
        <T size={42} color={P.payne} weight={600}>nhẹ và trong</T>
      </Rise>
      <Rise at={slowAt} style={{ position: "absolute", left: 600, top: 1330 }}>
        <T size={60} color={P.payne}>rót chậm</T>
        <T size={42} color={P.payne} weight={600}>đậm hơn</T>
      </Rise>
    </AbsoluteFill>
  );
};

// ── 8. The question, then the loop back to the lab ─────────────────────
const SceneEnd: React.FC<{ endAt: number }> = ({ endAt }) => {
  const frame = useCurrentFrame();
  const ended = frame >= endAt;
  return (
    <AbsoluteFill>
      <Paper />
      <Field id="sapf" color={P.sap} ox={540} oy={1920} seed={5} />
      {!ended ? (
        <Rise at={8} style={{ position: "absolute", left: 80, top: 640, width: 920 }}>
          <T size={92} color={P.paper}>Team rót nhanh hay rót chậm?</T>
          <T size={60} color={P.hansa} weight={600} style={{ marginTop: 20 }}>Comment một chữ thôi.</T>
        </Rise>
      ) : (
        <AbsoluteFill style={{ justifyContent: "center", paddingLeft: 80 }}>
          <Rise at={endAt}>
            <T size={92} color={P.paper}>Từ phòng lab</T>
            <T size={150} color={P.hansa} weight={900}>tới quầy bar.</T>
          </Rise>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

export const V60Film: React.FC<V60Props> = ({ audio, music, duration, words, beats: b }) => {
  const rel = (x: number, base: number) => f(x - base);
  const scenes: { from: number; to: number; el: React.ReactNode }[] = [
    { from: 0, to: b.lab, el: <SceneHook /> },
    { from: b.lab, to: b.erlen - 0.1, el: <SceneLab /> },
    { from: b.erlen - 0.1, to: b.cone, el: <SceneErlen foldAt={rel(b.fold, b.erlen - 0.1)} /> },
    { from: b.cone, to: b.years, el: <SceneCone /> },
    { from: b.years, to: b.name, el: <SceneYears y2005At={rel(b.y2005, b.years)} /> },
    { from: b.name, to: b.take, el: <SceneName sixtyAt={rel(b.sixty, b.name)} ribsAt={rel(b.ribs, b.name)} holeAt={rel(b.hole, b.name)} /> },
    { from: b.take, to: b.question, el: <SceneTake slowAt={rel(b.slow, b.take)} /> },
    { from: b.question, to: duration, el: <SceneEnd endAt={f(duration - 2.4 - b.question)} /> },
  ];
  return (
    <AbsoluteFill style={{ background: P.paper }}>
      {scenes.map((s, i) => (
        <Sequence key={i} from={f(s.from)} durationInFrames={Math.max(1, f(s.to) - f(s.from))}>{s.el}</Sequence>
      ))}
      <Captions words={words} hideFrom={duration - 2.4} />
      <Audio src={staticFile(audio)} />
      {music ? <Audio src={staticFile(music)} volume={0.13} /> : null}
    </AbsoluteFill>
  );
};
