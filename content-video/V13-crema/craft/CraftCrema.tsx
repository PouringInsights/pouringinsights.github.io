import React, { useMemo } from "react";
import { AbsoluteFill, Audio, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { geoGraticule10, geoInterpolate, geoOrthographic, geoPath } from "d3-geo";
import { feature } from "topojson-client";
import "./anaktoria.css";
import { Wash, WashFilter } from "../watercolor/engine";
// eslint-disable-next-line @typescript-eslint/no-var-requires
const world = require("world-atlas/countries-110m.json");

// ── Brand palette, sampled from the channel logo ─────────────────────
// coffee tones for the page + ink, Earth blue/green as the only pops.
const B = {
  cream: "#FAF8F2", // page
  stripe: "#F1EADD", // vertical stripes
  latte: "#E2D6C3", // grainy blob behind drawings
  ink: "#2F2B2A", // hand-drawn line + text
  coffee: "#6B4A33",
  espresso: "#3A2414",
  crema: "#C58B4A",
  earthBlue: "#2F7DC4",
  earthGreen: "#5BA544",
};
const FONT = "'Anaktoria', serif";
const FPS = 30;
const f = (s: number) => Math.round(s * FPS);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const EASE = Easing.bezier(0.25, 0.8, 0.25, 1);
const ramp = (fr: number, a: number, b: number) => interpolate(fr, [a, b], [0, 1], { ...clamp, easing: EASE });

type Word = { text: string; start: number; end: number };
export type CraftProps = { audio: string; music: string | null; duration: number; words: Word[]; beats: Record<string, number> };

// ── craft-book atoms ─────────────────────────────────────────────────
const Page: React.FC<{ children?: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: `repeating-linear-gradient(90deg, ${B.cream} 0 30px, ${B.stripe} 30px 60px)` }}>
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.35, mixBlendMode: "multiply" }}>
      <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={4} /><feColorMatrix type="saturate" values="0" /></filter>
      <rect width={1080} height={1920} filter="url(#grain)" opacity={0.25} />
    </svg>
    {children}
  </AbsoluteFill>
);

// hand-drawn wobble applied to ink strokes
const HandDefs: React.FC = () => (
  <defs>
    <filter id="hand" filterUnits="userSpaceOnUse" x={-1500} y={-1500} width={4000} height={5000}>
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={9} result="t" />
      <feDisplacementMap in="SourceGraphic" in2="t" scale={7} xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
);

// an ink line that draws itself on
const Ink: React.FC<{ d: string; p: number; w?: number; color?: string; fill?: string }> = ({ d, p, w = 16, color = B.ink, fill }) => (
  <g filter="url(#hand)">
    {fill ? <path d={d} fill={fill} opacity={p} /> : null}
    <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
  </g>
);

// grainy latte blob, like the logo's backing shape
const Blob: React.FC<{ id: string; cx: number; cy: number; r: number; p: number; seed?: number; color?: string }> = ({ id, cx, cy, r, p, seed = 3, color = B.latte }) => (
  <Wash id={id} seed={seed} color={color} cx={cx} cy={cy} r={r} p={p} body={0.95} rim={0.1} distort={120} />
);

const Svg: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}><HandDefs />{children}</svg>
);

const Txt: React.FC<{ size: number; color?: string; style?: React.CSSProperties; children: React.ReactNode }> = ({ size, color = B.ink, style, children }) => (
  <div style={{ fontFamily: FONT, fontSize: size, color, lineHeight: 1.12, ...style }}>{children}</div>
);
const Show: React.FC<{ at?: number; top: number; left?: number; width?: number; children: React.ReactNode; align?: "left" | "right" }> = ({ at = 0, top, left = 90, width = 900, children, align = "left" }) => {
  const fr = useCurrentFrame();
  const p = ramp(fr, at, at + 12);
  return <div style={{ position: "absolute", top, left, width, textAlign: align, opacity: p, transform: `translateY(${(1 - p) * 18}px)` }}>{children}</div>;
};

// watercolour Earth stamp (the logo's globe), drawn with d3
const land = feature(world, world.objects.countries) as any;
const Globe: React.FC<{ cx: number; cy: number; r: number; lon: number; lat?: number; id: string; route?: [number, number][]; routeP?: number }> = ({ cx, cy, r, lon, lat = -15, id, route, routeP = 0 }) => {
  const proj = geoOrthographic().scale(r).translate([cx, cy]).rotate([-lon, -lat, 0]).clipAngle(90);
  const path = geoPath(proj);
  let trail = "";
  if (route && routeP > 0) {
    const ip = geoInterpolate(route[0], route[1]);
    const pts = Array.from({ length: 80 }, (_, i) => ip((i / 79) * routeP));
    trail = path({ type: "LineString", coordinates: pts } as any) || "";
  }
  return (
    <g>
      <defs>
        <WashFilter id={`${id}o`} seed={31} distort={10} body={0.85} rim={0.5} />
        <WashFilter id={`${id}l`} seed={33} distort={5} body={0.9} rim={0.4} grainFreq={0.8} />
      </defs>
      <g style={{ mixBlendMode: "multiply" }}><path d={path({ type: "Sphere" } as any) || ""} fill={B.earthBlue} filter={`url(#${id}o)`} /></g>
      <g style={{ mixBlendMode: "multiply" }} filter={`url(#${id}l)`}>{land.features.map((ft: any, i: number) => <path key={i} d={path(ft) || ""} fill={B.earthGreen} />)}</g>
      {r > 200 ? <path d={path(geoGraticule10()) || ""} fill="none" stroke={B.cream} strokeOpacity={0.25} strokeWidth={1.5} /> : null}
      {trail ? <path d={trail} fill="none" stroke={B.ink} strokeWidth={10} strokeLinecap="round" filter="url(#hand)" /> : null}
    </g>
  );
};

// cup + saucer + steam in the logo's hand (original drawing, same spirit)
const CUP = "M330,1010 C330,1180 420,1300 540,1300 C660,1300 750,1180 750,1010";
const CUP_RIM = "M300,1000 C330,940 750,920 780,990 C790,1040 320,1060 300,1000 Z";
const HANDLE = "M760,1040 C860,1000 900,1090 840,1140 C800,1170 770,1160 740,1150";
const SAUCER = "M250,1290 C300,1240 800,1220 850,1280 C880,1330 280,1380 250,1290 Z";
const STEAM = ["M450,880 C420,840 480,800 450,760 C420,720 480,690 455,650", "M540,870 C510,830 570,790 540,750 C510,710 570,680 545,640", "M630,880 C600,840 660,800 630,760 C600,720 660,690 635,650"];
const Cup: React.FC<{ p: number; crema: number; steam?: number; blobId: string }> = ({ p, crema, steam = 0, blobId }) => (
  <g>
    <Blob id={blobId} cx={560} cy={1080} r={430} p={Math.min(1, p * 1.6)} seed={7} />
    <Ink d={SAUCER} p={ramp(p * 30, 0, 18)} />
    <Ink d={CUP} p={ramp(p * 30, 4, 22)} />
    <Ink d={HANDLE} p={ramp(p * 30, 10, 26)} />
    <defs><clipPath id={`${blobId}clip`}><path d={CUP_RIM} /></clipPath></defs>
    <g opacity={crema} clipPath={`url(#${blobId}clip)`}>
      <path d={CUP_RIM} fill={B.espresso} />
      <Wash id={`${blobId}cr`} seed={44} color={B.crema} cx={545} cy={995} r={190} p={crema} body={0.9} rim={0.6} distort={20} blend="normal" />
    </g>
    <Ink d={CUP_RIM} p={ramp(p * 30, 8, 24)} />
    {STEAM.map((d, i) => <Ink key={i} d={d} p={ramp(steam * 30, i * 4, 14 + i * 4)} w={14} />)}
  </g>
);

// ── scenes ──────────────────────────────────────────────────────────
const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Cup p={ramp(fr, 0, 30)} crema={ramp(fr, 20, 50)} steam={ramp(fr, 26, 60)} blobId="hk" />
        <g opacity={ramp(fr, 60, 76)}><Globe id="hg" cx={230} cy={1470} r={92} lon={106} /></g>
      </Svg>
      <Show top={250}><Txt size={124}>crema kiểu Naples</Txt></Show>
      <Show at={60} top={1420} left={360} width={680}><Txt size={64}>& hạt Robusta Việt Nam</Txt></Show>
    </Page>
  );
};

const STEAMER = "M400,1300 L400,900 C400,780 680,780 680,900 L680,1300 Z M380,1300 L700,1300 M540,780 L540,720 M500,720 L580,720 M680,1060 L780,1060 L780,1120";
const Steam: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="sb" cx={560} cy={1040} r={400} p={ramp(fr, 0, 16)} seed={12} />
        <Ink d={STEAMER} p={ramp(fr, 2, 34)} />
        {[0, 1, 2].map((i) => {
          const y = -((fr * 2 + i * 40) % 110);
          return <Ink key={i} d={`M${470 + i * 70},${740 + y} c-25,-30 25,-60 0,-90`} p={1} w={12} />;
        })}
      </Svg>
      <Show top={250}><Txt size={170}>1938</Txt><Txt size={64}>máy espresso chạy hơi nước</Txt></Show>
      <Show at={40} top={1400}><Txt size={58}>áp lực thấp · mặt ly gần như trơn</Txt></Show>
    </Page>
  );
};

const Gaggia: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="gb" cx={540} cy={1000} r={380} p={ramp(fr, 0, 16)} seed={15} />
        <Ink d="M300,700 L780,700 L780,1300 L300,1300 Z" p={ramp(fr, 2, 24)} fill={B.cream} />
        {[0, 1, 2, 3, 4].map((i) => <Ink key={i} d={`M360,${800 + i * 80} L${700 - (i % 2) * 80},${800 + i * 80}`} p={ramp(fr, 14 + i * 4, 26 + i * 4)} w={9} />)}
        <Wash id="seal" seed={52} color={B.earthBlue} cx={690} cy={1210} r={60} p={ramp(fr, 40, 54)} body={0.9} rim={0.5} distort={12} blend="normal" />
      </Svg>
      <Show top={250}><Txt size={96}>Achille Gaggia, Milan</Txt><Txt size={60}>sáng chế bỏ hẳn hơi nước</Txt></Show>
    </Page>
  );
};

const Lever: React.FC = () => {
  const fr = useCurrentFrame();
  const a = interpolate(fr, [16, 52], [-65, 20], { ...clamp, easing: EASE });
  const crema = ramp(fr, 70, 110);
  return (
    <Page>
      <Svg>
        <Blob id="lb" cx={540} cy={1120} r={420} p={ramp(fr, 0, 16)} seed={18} />
        <Ink d="M380,820 L700,820 L700,1060 L380,1060 Z" p={ramp(fr, 0, 18)} fill={B.cream} />
        <Ink d="M470,1060 L470,1120 L610,1120 L610,1060 M440,1120 L640,1120" p={ramp(fr, 8, 24)} />
        <g transform={`translate(540 860) rotate(${a})`}><Ink d="M0,0 L0,-330" p={ramp(fr, 6, 20)} w={22} /><circle cx={0} cy={-340} r={34} fill={B.earthBlue} opacity={ramp(fr, 14, 20)} /></g>
        <Ink d="M450,1260 C450,1380 630,1380 630,1260 Z" p={ramp(fr, 30, 50)} fill={B.cream} />
        <Wash id="lcr" seed={61} color={B.crema} cx={540} cy={1268} r={86} p={crema} body={0.95} rim={0.5} distort={10} blend="normal" />
        {[0, 1, 2].map((i) => {
          const t = ((fr - 30 - i * 8) % 24) / 24;
          return fr > 30 + i * 8 && fr < 110 ? <circle key={i} cx={540} cy={1130 + t * 120} r={8} fill={B.espresso} /> : null;
        })}
      </Svg>
      <Show top={250}><Txt size={170}>1948</Txt><Txt size={60}>cần gạt piston: ép nước mạnh hơn hẳn</Txt></Show>
      <Show at={74} top={1460}><Txt size={64} color={B.coffee}>…và một lớp bọt vàng nâu</Txt></Show>
    </Page>
  );
};

const Sign: React.FC<{ renameAt: number }> = ({ renameAt }) => {
  const fr = useCurrentFrame();
  const swing = Math.sin(fr / 12) * 2.5 * (1 - ramp(fr, 0, 90));
  const strike = ramp(fr, renameAt + 6, renameAt + 18);
  return (
    <Page>
      <Svg>
        <Blob id="sgb" cx={540} cy={860} r={420} p={ramp(fr, 0, 16)} seed={21} />
        <g transform={`rotate(${swing} 540 520)`}>
          <Ink d="M380,520 L300,700 M700,520 L780,700" p={ramp(fr, 4, 16)} w={10} />
          <Ink d="M200,700 L880,700 L880,1060 L200,1060 Z" p={ramp(fr, 8, 28)} fill={B.cream} />
        </g>
      </Svg>
      <Show at={4} top={250}><Txt size={56} color={B.coffee}>theo lời kể, khách ngờ đó là váng…</Txt></Show>
      <div style={{ position: "absolute", left: 200, width: 680, top: 760, textAlign: "center", transform: `rotate(${swing}deg)`, transformOrigin: "340px -240px", opacity: ramp(fr, 26, 38) }}>
        <Txt size={104}>caffè crema</Txt>
        <Txt size={54} color={B.coffee}>kem cà phê tự nhiên</Txt>
      </div>
      <Show at={renameAt} top={1240}>
        <div style={{ position: "relative", display: "inline-block" }}>
          <Txt size={110} color={B.coffee}>váng</Txt>
          <div style={{ position: "absolute", left: -6, right: -6, top: "50%", height: 12, transform: `scaleX(${strike})`, transformOrigin: "left", background: B.earthBlue, borderRadius: 6 }} />
        </div>
        <Txt size={150}>thành kem.</Txt>
      </Show>
    </Page>
  );
};

const Science: React.FC = () => {
  const fr = useCurrentFrame();
  const bubbles = useMemo(() => Array.from({ length: 22 }, (_, i) => ({ x: 360 + ((i * 97) % 360), y: 1020 + ((i * 53) % 90), r: 8 + (i % 4) * 5, d: (i % 6) * 4 })), []);
  const labels = [
    { t: "CO2 từ lúc rang", y: 650, at: 10 },
    { t: "bung bọt khi tụt áp", y: 760, at: 60 },
    { t: "dầu + melanoidin giữ bọt", y: 1500, at: 120 },
  ];
  return (
    <Page>
      <Svg>
        <Blob id="scb" cx={540} cy={1120} r={400} p={ramp(fr, 0, 16)} seed={24} />
        <Ink d="M330,960 L360,1340 L720,1340 L750,960" p={ramp(fr, 2, 22)} />
        <rect x={350} y={1130} width={380} height={200} fill={B.espresso} opacity={ramp(fr, 14, 26)} filter="url(#hand)" />
        <rect x={340} y={1000} width={400} height={130} fill={B.crema} opacity={ramp(fr, 60, 80)} filter="url(#hand)" />
        {bubbles.map((b, i) => {
          const p = ramp(fr, 60 + b.d, 76 + b.d);
          return <circle key={i} cx={b.x} cy={b.y} r={b.r * p} fill="none" stroke={B.ink} strokeWidth={4} />;
        })}
      </Svg>
      <Show top={240}><Txt size={110}>crema là gì?</Txt></Show>
      {labels.map((l) => <Show key={l.t} at={l.at} top={l.y}><Txt size={58} color={l.at === 120 ? B.coffee : B.ink}>→ {l.t}</Txt></Show>)}
    </Page>
  );
};

const ARABICA = { body: "M0,-140 C95,-140 105,140 0,140 C-105,140 -95,-140 0,-140 Z", crease: "M0,-115 C45,-50 -45,50 0,115" };
const ROBUSTA = { body: "M0,-120 C120,-120 125,120 0,120 C-125,120 -120,-120 0,-120 Z", crease: "M0,-95 L0,95" };
const Robusta: React.FC = () => {
  const fr = useCurrentFrame();
  const beans = [{ x: 300, b: ARABICA, name: "Arabica", foam: 40, c: B.earthGreen }, { x: 780, b: ROBUSTA, name: "Robusta", foam: 110, c: B.earthBlue }];
  return (
    <Page>
      <Svg>
        {beans.map((bn, i) => (
          <g key={bn.name}>
            <Blob id={`rb${i}`} cx={bn.x} cy={900} r={210} p={ramp(fr, i * 8, 16 + i * 8)} seed={30 + i} />
            <g transform={`translate(${bn.x} 900) rotate(${i ? -12 : 14})`}>
              <Ink d={bn.b.body} p={ramp(fr, 4 + i * 8, 22 + i * 8)} fill={B.coffee} />
              <Ink d={bn.b.crease} p={ramp(fr, 14 + i * 8, 28 + i * 8)} w={12} color={B.cream} />
            </g>
            {/* crema thickness */}
            <rect x={bn.x - 130} y={1330 - bn.foam * ramp(fr, 40 + i * 14, 70 + i * 14)} width={260} height={bn.foam * ramp(fr, 40 + i * 14, 70 + i * 14)} fill={B.crema} filter="url(#hand)" />
            <rect x={bn.x - 130} y={1330} width={260} height={80} fill={B.espresso} filter="url(#hand)" opacity={ramp(fr, 30, 40)} />
          </g>
        ))}
      </Svg>
      <Show top={240}><Txt size={96}>bọt dày hơn với Robusta</Txt></Show>
      <Show at={10} top={1110} left={190} width={240}><Txt size={58}>Arabica</Txt></Show>
      <Show at={18} top={1110} left={660} width={260}><Txt size={58}>Robusta</Txt></Show>
      <Show at={100} top={1470}><Txt size={64} color={B.coffee}>blend kiểu Naples: 20–40% Robusta</Txt></Show>
    </Page>
  );
};

const Vietnam: React.FC = () => {
  const fr = useCurrentFrame();
  const t = ramp(fr, 10, 100);
  const lon = interpolate(t, [0, 1], [108, 40]);
  return (
    <Page>
      <Svg>
        <Blob id="vb" cx={540} cy={1000} r={470} p={ramp(fr, 0, 16)} seed={36} />
        <Globe id="vg" cx={540} cy={1000} r={360} lon={lon} lat={-25} route={[[108, 12.7], [14.25, 40.85]]} routeP={t} />
      </Svg>
      <Show top={240}><Txt size={96}>năm 2025</Txt><Txt size={64}>Ý: một trong 3 nước mua cà phê Việt nhiều nhất</Txt></Show>
      <Show at={40} top={1430}><Txt size={58} color={B.coffee}>Tây Nguyên → Naples</Txt></Show>
    </Page>
  );
};

const Take: React.FC<{ tasteAt: number }> = ({ tasteAt }) => {
  const steps = ["nếm riêng một thìa crema", "khuấy đều", "nếm lại"];
  return (
    <Page>
      <Svg><Blob id="tb" cx={560} cy={760} r={380} p={1} seed={40} /></Svg>
      <Show top={460}><Txt size={96}>crema dày = hạt tươi + đủ áp lực</Txt><Txt size={110} color={B.earthBlue} style={{ marginTop: 20 }}>≠ ngon</Txt></Show>
      {steps.map((s, i) => <Show key={s} at={tasteAt + i * 22} top={1080 + i * 110}><Txt size={64}>{i + 1}. {s}</Txt></Show>)}
    </Page>
  );
};

const End: React.FC<{ endAt: number }> = ({ endAt }) => {
  const fr = useCurrentFrame();
  const ended = fr >= endAt;
  return (
    <Page>
      {!ended ? (
        <Show at={4} top={640}><Txt size={110}>Bạn có khuấy crema không?</Txt><Txt size={64} color={B.earthBlue} style={{ marginTop: 24 }}>comment có hoặc không</Txt></Show>
      ) : (
        <>
          <Svg>
            <g transform="translate(0 -180)"><Cup p={ramp(fr - endAt, 0, 24)} crema={ramp(fr - endAt, 10, 30)} steam={ramp(fr - endAt, 14, 40)} blobId="eb" /></g>
            <g opacity={ramp(fr - endAt, 20, 32)}><Globe id="eg" cx={290} cy={1400} r={80} lon={106} /></g>
          </Svg>
          <Show at={endAt + 20} top={1320} left={400} width={640}><Txt size={110}>barista</Txt><Txt size={110}>sính ngoại</Txt></Show>
        </>
      )}
    </Page>
  );
};

// captions in the brand hand: ink words, active word in Earth blue, on a soft latte band
const Captions: React.FC<{ words: Word[]; hideFrom: number }> = ({ words, hideFrom }) => {
  const fr = useCurrentFrame();
  const t = fr / FPS;
  const chunks = useMemo(() => {
    const out: Word[][] = [];
    let cur: Word[] = [];
    words.forEach((w, i) => {
      cur.push(w);
      const gap = words[i + 1] ? words[i + 1].start - w.end > 0.2 : true;
      if (cur.length >= 4 || gap) { out.push(cur); cur = []; }
    });
    if (cur.length) out.push(cur);
    return out;
  }, [words]);
  if (t >= hideFrom) return null;
  const idx = chunks.findIndex((c, i) => t >= c[0].start - 0.05 && t < (chunks[i + 1] ? chunks[i + 1][0].start - 0.05 : c[c.length - 1].end + 0.6));
  if (idx < 0) return null;
  return (
    <AbsoluteFill style={{ top: 1610, height: 200, alignItems: "center", paddingLeft: 60, paddingRight: 150 }}>
      <div style={{ fontFamily: FONT, fontSize: 70, lineHeight: 1.1, color: B.ink, background: "rgba(250,248,242,0.92)", padding: "6px 26px 12px", borderRadius: 40, textAlign: "center" }}>
        {chunks[idx].map((w, i) => {
          const active = t >= w.start && t < w.end + 0.05;
          return <span key={i} style={{ color: active ? B.earthBlue : B.ink }}>{w.text}{i < chunks[idx].length - 1 ? " " : ""}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

// page-turn: each new page slides over the previous one with a soft edge shadow
const Turn: React.FC<{ children: React.ReactNode; first?: boolean }> = ({ children, first }) => {
  const fr = useCurrentFrame();
  const p = first ? 1 : ramp(fr, 0, 10);
  return (
    <AbsoluteFill style={{ transform: `translateX(${(1 - p) * 1080}px) rotate(${(1 - p) * 4}deg)`, transformOrigin: "0 1920px", boxShadow: p < 1 ? "-30px 0 50px rgba(47,43,42,0.25)" : "none" }}>
      {children}
    </AbsoluteFill>
  );
};

export const CraftCrema: React.FC<CraftProps> = (props) => {
  const b = props.beats;
  const scenes: [number, number, React.ReactNode][] = [
    [0, b.steam, <Hook />],
    [b.steam, b.gaggia, <Steam />],
    [b.gaggia, b.lever, <Gaggia />],
    [b.lever, b.sign, <Lever />],
    [b.sign, b.science, <Sign renameAt={f(b.rename - b.sign)} />],
    [b.science, b.robusta, <Science />],
    [b.robusta, b.vietnam, <Robusta />],
    [b.vietnam, b.take, <Vietnam />],
    [b.take, b.question, <Take tasteAt={f(b.taste - b.take)} />],
    [b.question, props.duration, <End endAt={f(props.duration - 2.8 - b.question)} />],
  ];
  return (
    <AbsoluteFill style={{ background: B.cream }}>
      {scenes.map(([from, to, el], i) => (
        <Sequence key={i} from={f(from)} durationInFrames={Math.max(1, f(to) - f(from) + (i < scenes.length - 1 ? 10 : 0))}>
          <Turn first={i === 0}>{el}</Turn>
        </Sequence>
      ))}
      <Captions words={props.words} hideFrom={props.duration - 2.6} />
      <Audio src={staticFile(props.audio)} />
      {props.music ? <Audio src={staticFile(props.music)} volume={0.12} /> : null}
    </AbsoluteFill>
  );
};
