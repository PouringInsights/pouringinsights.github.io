import React, { useMemo } from "react";
import { AbsoluteFill, Audio, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { geoGraticule10, geoInterpolate, geoOrthographic, geoPath } from "d3-geo";
import { feature } from "topojson-client";
import "./anaktoria.css";
import { Wash, WashFilter } from "../watercolor/engine";
// eslint-disable-next-line @typescript-eslint/no-var-requires
const world = require("world-atlas/countries-110m.json");
export { Wash, WashFilter };
// ── Brand palette, sampled from the channel logo ─────────────────────
// coffee tones for the page + ink, Earth blue/green as the only pops.
export const B = {
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
export const FONT = "'Anaktoria', serif";
export const FPS = 30;
export const f = (s: number) => Math.round(s * FPS);
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const EASE = Easing.bezier(0.25, 0.8, 0.25, 1);
export const ramp = (fr: number, a: number, b: number) => interpolate(fr, [a, b], [0, 1], { ...clamp, easing: EASE });

export type Word = { text: string; start: number; end: number };
export type CraftProps = { audio: string; music: string | null; duration: number; words: Word[]; beats: Record<string, number> };

// ── craft-book atoms ─────────────────────────────────────────────────
export const Page: React.FC<{ children?: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: `repeating-linear-gradient(90deg, ${B.cream} 0 30px, ${B.stripe} 30px 60px)` }}>
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.35, mixBlendMode: "multiply" }}>
      <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={4} /><feColorMatrix type="saturate" values="0" /></filter>
      <rect width={1080} height={1920} filter="url(#grain)" opacity={0.25} />
    </svg>
    {children}
  </AbsoluteFill>
);

// hand-drawn wobble applied to ink strokes
export const HandDefs: React.FC = () => (
  <defs>
    <filter id="hand" filterUnits="userSpaceOnUse" x={-1500} y={-1500} width={4000} height={5000}>
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={9} result="t" />
      <feDisplacementMap in="SourceGraphic" in2="t" scale={7} xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
);

// an ink line that draws itself on
export const Ink: React.FC<{ d: string; p: number; w?: number; color?: string; fill?: string }> = ({ d, p, w = 16, color = B.ink, fill }) => (
  <g filter="url(#hand)">
    {fill ? <path d={d} fill={fill} opacity={p} /> : null}
    <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
  </g>
);

// grainy latte blob, like the logo's backing shape
export const Blob: React.FC<{ id: string; cx: number; cy: number; r: number; p: number; seed?: number; color?: string }> = ({ id, cx, cy, r, p, seed = 3, color = B.latte }) => (
  <Wash id={id} seed={seed} color={color} cx={cx} cy={cy} r={r} p={p} body={0.95} rim={0.1} distort={120} />
);

export const Svg: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}><HandDefs />{children}</svg>
);

export const Txt: React.FC<{ size: number; color?: string; style?: React.CSSProperties; children: React.ReactNode }> = ({ size, color = B.ink, style, children }) => (
  <div style={{ fontFamily: FONT, fontSize: size, color, lineHeight: 1.12, ...style }}>{children}</div>
);
export const Show: React.FC<{ at?: number; top: number; left?: number; width?: number; children: React.ReactNode; align?: "left" | "right" }> = ({ at = 0, top, left = 90, width = 900, children, align = "left" }) => {
  const fr = useCurrentFrame();
  const p = ramp(fr, at, at + 12);
  return <div style={{ position: "absolute", top, left, width, textAlign: align, opacity: p, transform: `translateY(${(1 - p) * 18}px)` }}>{children}</div>;
};

// watercolour Earth stamp (the logo's globe), drawn with d3
export const land = feature(world, world.objects.countries) as any;
export const Globe: React.FC<{ cx: number; cy: number; r: number; lon: number; lat?: number; id: string; route?: [number, number][]; routeP?: number }> = ({ cx, cy, r, lon, lat = -15, id, route, routeP = 0 }) => {
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
export const CUP = "M330,1010 C330,1180 420,1300 540,1300 C660,1300 750,1180 750,1010";
export const CUP_RIM = "M300,1000 C330,940 750,920 780,990 C790,1040 320,1060 300,1000 Z";
export const HANDLE = "M760,1040 C860,1000 900,1090 840,1140 C800,1170 770,1160 740,1150";
export const SAUCER = "M250,1290 C300,1240 800,1220 850,1280 C880,1330 280,1380 250,1290 Z";
export const STEAM = ["M450,880 C420,840 480,800 450,760 C420,720 480,690 455,650", "M540,870 C510,830 570,790 540,750 C510,710 570,680 545,640", "M630,880 C600,840 660,800 630,760 C600,720 660,690 635,650"];
export const Cup: React.FC<{ p: number; crema: number; steam?: number; blobId: string }> = ({ p, crema, steam = 0, blobId }) => (
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

// captions in the brand hand: ink words, active word in Earth blue, on a soft latte band
export const Captions: React.FC<{ words: Word[]; hideFrom: number }> = ({ words, hideFrom }) => {
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
export const Turn: React.FC<{ children: React.ReactNode; first?: boolean }> = ({ children, first }) => {
  const fr = useCurrentFrame();
  const p = first ? 1 : ramp(fr, 0, 10);
  return (
    <AbsoluteFill style={{ transform: `translateX(${(1 - p) * 1080}px) rotate(${(1 - p) * 4}deg)`, transformOrigin: "0 1920px", boxShadow: p < 1 ? "-30px 0 50px rgba(47,43,42,0.25)" : "none" }}>
      {children}
    </AbsoluteFill>
  );
};


export type SceneDef = [number, number, React.ReactNode];
export const CraftFilm: React.FC<{ props: CraftProps; scenes: SceneDef[] }> = ({ props, scenes }) => (
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

// closing lockup reused by every film: the logo cup + Earth + channel name
export const EndCard: React.FC<{ at: number; question: string; answer: string }> = ({ at, question, answer }) => {
  const fr = useCurrentFrame();
  if (fr < at) {
    return (
      <Page>
        <Show at={4} top={640}><Txt size={104}>{question}</Txt><Txt size={64} color={B.earthBlue} style={{ marginTop: 24 }}>{answer}</Txt></Show>
      </Page>
    );
  }
  return (
    <Page>
      <Svg>
        <g transform="translate(0 -180)"><Cup p={ramp(fr - at, 0, 24)} crema={ramp(fr - at, 10, 30)} steam={ramp(fr - at, 14, 40)} blobId="endc" /></g>
        <g opacity={ramp(fr - at, 20, 32)}><Globe id="endg" cx={290} cy={1400} r={80} lon={106} /></g>
      </Svg>
      <Show at={at + 20} top={1320} left={400} width={640}><Txt size={110}>barista</Txt><Txt size={110}>sính ngoại</Txt></Show>
    </Page>
  );
};
