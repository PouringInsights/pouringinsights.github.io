// Chibi cast v2: big head (~45% of height), anime eyes, layered hair with
// shading, short rounded limbs, HaUI white polo (navy collar + cuffs with red
// tipping, badge on the left chest). Same pose API as Cast.tsx.
import React from "react";
import type { PersonPose, Prop, Variant } from "./Cast";

const OL = "#3B2A33"; // warm dark outline
const W = "#FFFFFF";
const SH = "#E4E8F3"; // cloth shadow
const NAVY = "#1F3488";
const RED = "#D7263D";

type Pal = { skin: string; skinSh: string; hair: string; hairSh: string; hairHi: string; iris: string; iris2: string; pants: string; pantsSh: string; shoe: string };
const PAL: Record<Variant, Pal> = {
  ponytail: { skin: "#FFE3D3", skinSh: "#F6C7B4", hair: "#4A2E2A", hairSh: "#341F1D", hairHi: "#7A5048", iris: "#3A2A5C", iris2: "#8B6FC2", pants: "#EDE4D3", pantsSh: "#D8CDB8", shoe: "#FFFFFF" },
  longHair: { skin: "#FFE6D8", skinSh: "#F5C9B8", hair: "#2E2230", hairSh: "#1E1620", hairHi: "#5B4560", iris: "#2F3A66", iris2: "#6C8BD6", pants: "#E9E0CC", pantsSh: "#D3C7AE", shoe: "#FFFFFF" },
  boy: { skin: "#FADBC6", skinSh: "#EDBFA5", hair: "#2A2326", hairSh: "#18131A", hairHi: "#4F4448", iris: "#3A2B22", iris2: "#9A6B48", pants: "#B8AA8C", pantsSh: "#9F9275", shoe: "#FFFFFF" },
  teacher: { skin: "#FFE2D2", skinSh: "#F3C5B1", hair: "#3A2522", hairSh: "#26181A", hairHi: "#6B4A42", iris: "#3E2A22", iris2: "#A0704C", pants: "#2C3557", pantsSh: "#212945", shoe: "#3B3F58" },
};

const rot = (x: number, y: number, deg: number): [number, number] => {
  const r = (deg * Math.PI) / 180;
  return [x * Math.cos(r) - y * Math.sin(r), x * Math.sin(r) + y * Math.cos(r)];
};
const tube = (pts: [number, number][], ws: number[]) => {
  const n = pts.length;
  const nm = pts.map((_, i) => {
    const a = pts[Math.max(0, i - 1)];
    const b = pts[Math.min(n - 1, i + 1)];
    const dx = b[0] - a[0];
    const dy = b[1] - a[1];
    const l = Math.hypot(dx, dy) || 1;
    return [-dy / l, dx / l];
  });
  const Lp = pts.map((p, i) => [p[0] + nm[i][0] * ws[i], p[1] + nm[i][1] * ws[i]]);
  const Rp = pts.map((p, i) => [p[0] - nm[i][0] * ws[i], p[1] - nm[i][1] * ws[i]]);
  const f = (q: number[]) => `${q[0].toFixed(1)} ${q[1].toFixed(1)}`;
  return `M${f(Lp[0])} Q${f(Lp[1])} ${f(Lp[2])} A${ws[2]} ${ws[2]} 0 0 1 ${f(Rp[2])} Q${f(Rp[1])} ${f(Rp[0])} A${ws[0]} ${ws[0]} 0 0 1 ${f(Lp[0])} Z`;
};

// ---------------------------------------------------------------------------
const Held: React.FC<{ prop?: Prop; side: 1 | -1 }> = ({ prop, side }) => {
  if (!prop || prop === "none") return null;
  switch (prop) {
    case "megaphone":
      return (
        <g transform={`translate(${side * 4} -4) rotate(${side * -75})`}>
          <path d="M0 -12 L70 -40 L70 40 L0 12 Z" fill="#FF7A59" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <ellipse cx={70} cy={0} rx={9} ry={40} fill="#FFD3C4" stroke={OL} strokeWidth={4} />
          <rect x={-16} y={-14} width={20} height={28} rx={6} fill="#FFC93C" stroke={OL} strokeWidth={4} />
        </g>
      );
    case "box":
      return (
        <g transform="translate(0 -36)">
          <rect x={-56} y={-16} width={112} height={84} rx={6} fill="#E0AE6E" stroke={OL} strokeWidth={4} />
          <rect x={-56} y={-16} width={112} height={18} fill="#CC9654" stroke={OL} strokeWidth={4} />
          <rect x={-10} y={-16} width={20} height={84} fill="#F3D8AE" />
        </g>
      );
    case "laptop":
    case "tablet":
      return (
        <g transform={`translate(${side * -26} -30) rotate(${side * -10})`}>
          <rect x={-44} y={-18} width={88} height={112} rx={10} fill={NAVY} stroke={OL} strokeWidth={4} />
          <rect x={-36} y={-10} width={72} height={94} rx={5} fill="#8EC1FF" />
          <rect x={-26} y={44} width={11} height={30} fill="#FFC93C" />
          <rect x={-9} y={28} width={11} height={46} fill={W} />
          <rect x={8} y={14} width={11} height={60} fill="#FF7A59" />
        </g>
      );
    case "cap":
      return (
        <g transform="translate(0 -24)">
          <path d="M-54 0 L0 -24 L54 0 L0 24 Z" fill="#20203A" stroke={OL} strokeWidth={4} />
          <path d="M28 6 L40 36" stroke="#FFC93C" strokeWidth={5} strokeLinecap="round" />
        </g>
      );
    case "phone":
      return <rect x={-14} y={-30} width={28} height={50} rx={6} fill="#2A2A2A" stroke={OL} strokeWidth={3} />;
  }
  return null;
};

const Arm: React.FC<{ x: number; y: number; s: number; e: number; side: 1 | -1; p: Pal; blazer: boolean; hold?: Prop; back?: boolean }> = ({ x, y, s, e, side, p, blazer, hold, back }) => {
  const a1 = -side * s;
  const a2 = a1 - side * e;
  const [ex, ey] = rot(0, 62, a1);
  const [wx, wy] = rot(0, 54, a2);
  const Wr: [number, number] = [ex + wx, ey + wy];
  const skin = back ? p.skinSh : p.skin;
  const sleeve = blazer ? (back ? "#182A6E" : NAVY) : back ? SH : W;
  return (
    <g transform={`translate(${x} ${y})`}>
      <path d={tube([[0, 0], [ex, ey], Wr], [24, 21, 19])} fill={blazer ? sleeve : skin} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      <g transform={`translate(${Wr[0]} ${Wr[1]}) rotate(${a2})`}>
        <Held prop={hold} side={side} />
        {blazer ? <path d="M-19 -6 Q0 2 19 -6" stroke={W} strokeWidth={6} fill="none" /> : null}
        {/* chibi mitten hand */}
        <ellipse cx={0} cy={8} rx={21} ry={20} fill={skin} stroke={OL} strokeWidth={4} />
        <path d={`M${side * -16} 2 Q${side * -24} 10 ${side * -16} 16`} fill="none" stroke={OL} strokeWidth={3} strokeLinecap="round" />
      </g>
      <g transform={`rotate(${a1})`}>
        {blazer ? (
          <path d="M-28 -16 Q0 -30 28 -16 Q31 20 28 52 Q0 58 -28 52 Q-31 20 -28 -16 Z" fill={sleeve} stroke={OL} strokeWidth={4} />
        ) : (
          <g>
            <path d="M-30 -18 Q0 -34 30 -18 Q33 10 34 38 Q0 46 -34 38 Q-33 10 -30 -18 Z" fill={sleeve} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
            <path d="M-34 28 Q0 36 34 28 L34 42 Q0 50 -34 42 Z" fill={NAVY} stroke={OL} strokeWidth={3} />
            <path d="M-33 35 Q0 43 33 35" stroke={RED} strokeWidth={2.6} fill="none" />
          </g>
        )}
      </g>
    </g>
  );
};

const Leg: React.FC<{ x: number; y: number; a: number; p: Pal; front?: boolean }> = ({ x, y, a, p, front }) => (
  <g transform={`translate(${x} ${y}) rotate(${a})`}>
    <path d="M-34 -10 Q-38 60 -38 112 Q0 120 38 112 Q38 60 34 -10 Z" fill={front ? p.pants : p.pantsSh} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
    <path d="M-36 112 Q-44 140 -8 142 L30 142 Q50 140 44 122 Q40 110 24 110 Z" fill={p.shoe} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
    <path d="M-34 132 Q4 138 44 130" stroke="#D9DCE6" strokeWidth={4} fill="none" />
  </g>
);

// ---------------------------------------------------------------------------
const Eye: React.FC<{ cx: number; p: Pal; blink: number; look: number; side: 1 | -1 }> = ({ cx, p, blink, look, side }) => {
  const cy = 236;
  if (blink > 0.5)
    return <path d={`M${cx - 26} ${cy} Q${cx} ${cy + 14} ${cx + 26} ${cy}`} stroke={OL} strokeWidth={6} fill="none" strokeLinecap="round" />;
  const id = `ir${cx}${p.iris.slice(1)}`;
  return (
    <g>
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={p.iris} />
          <stop offset="1" stopColor={p.iris2} />
        </linearGradient>
      </defs>
      <ellipse cx={cx} cy={cy} rx={27} ry={34} fill={W} stroke={OL} strokeWidth={3} />
      <ellipse cx={cx + look} cy={cy + 3} rx={23} ry={30} fill={`url(#${id})`} />
      <ellipse cx={cx + look} cy={cy + 6} rx={11} ry={14} fill={OL} opacity={0.75} />
      <circle cx={cx + look - 9} cy={cy - 11} r={9} fill={W} />
      <circle cx={cx + look + 10} cy={cy + 14} r={4} fill={W} opacity={0.9} />
      {/* upper lash line with outer flick */}
      <path d={side < 0 ? `M${cx + 26} ${cy - 22} Q${cx} ${cy - 44} ${cx - 30} ${cy - 22} L${cx - 38} ${cy - 30}` : `M${cx - 26} ${cy - 22} Q${cx} ${cy - 44} ${cx + 30} ${cy - 22} L${cx + 38} ${cy - 30}`} stroke={OL} strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </g>
  );
};

const Face: React.FC<{ v: Variant; p: Pal; pose: PersonPose }> = ({ v, p, pose }) => {
  const blink = pose.blink ?? 0;
  const look = (pose.look ?? 0) * 7;
  const m = pose.mouth ?? 0;
  return (
    <g>
      {/* face: soft mochi shape */}
      <path d="M72 200 Q72 70 200 70 Q328 70 328 200 Q328 318 200 330 Q72 318 72 200 Z" fill={p.skin} stroke={OL} strokeWidth={4.5} />
      <ellipse cx={70} cy={222} rx={16} ry={24} fill={p.skinSh} stroke={OL} strokeWidth={4} />
      <ellipse cx={330} cy={222} rx={16} ry={24} fill={p.skinSh} stroke={OL} strokeWidth={4} />
      <Eye cx={140} p={p} blink={blink} look={look} side={-1} />
      <Eye cx={260} p={p} blink={blink} look={look} side={1} />
      {/* brows */}
      <path d="M116 182 Q138 172 160 178" stroke={p.hairSh} strokeWidth={5} fill="none" strokeLinecap="round" />
      <path d="M240 178 Q262 172 284 182" stroke={p.hairSh} strokeWidth={5} fill="none" strokeLinecap="round" />
      {v === "teacher" || v === "longHair" ? (
        <g fill="none" stroke={v === "teacher" ? "#8A5A3C" : "#C0B4D6"} strokeWidth={4.5}>
          <rect x={102} y={196} width={76} height={70} rx={24} />
          <rect x={222} y={196} width={76} height={70} rx={24} />
          <path d="M178 228 Q200 220 222 228" />
        </g>
      ) : null}
      {/* blush with hatching */}
      <ellipse cx={112} cy={286} rx={24} ry={12} fill="#FF9EA6" opacity={0.55} />
      <ellipse cx={288} cy={286} rx={24} ry={12} fill="#FF9EA6" opacity={0.55} />
      <path d="M102 290 L108 280 M112 292 L118 282 M122 290 L128 280" stroke="#F47C8A" strokeWidth={2.4} strokeLinecap="round" />
      <path d="M278 290 L284 280 M288 292 L294 282 M298 290 L304 280" stroke="#F47C8A" strokeWidth={2.4} strokeLinecap="round" />
      {/* mouth */}
      {m > 0.08 ? (
        <path d={`M186 290 Q200 ${294 + 22 * m} 214 290 Q200 ${287 + 3 * m} 186 290 Z`} fill="#C9505E" stroke={OL} strokeWidth={3.4} strokeLinejoin="round" />
      ) : pose.smile === false ? (
        <path d="M190 292 L210 292" stroke={OL} strokeWidth={4} strokeLinecap="round" />
      ) : (
        <path d="M184 288 Q192 298 200 290 Q208 298 216 288" stroke={OL} strokeWidth={4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      )}
    </g>
  );
};

const HairBack: React.FC<{ v: Variant; p: Pal; sway: number }> = ({ v, p, sway }) => {
  if (v === "longHair")
    return <path d={`M64 190 Q48 360 ${86 + sway} 470 Q200 494 ${314 + sway} 470 Q352 360 336 190 Z`} fill={p.hairSh} stroke={OL} strokeWidth={4.5} />;
  if (v === "ponytail")
    return (
      <g>
        <path d={`M300 110 Q392 ${150 + sway} 374 ${270 + sway * 2} Q362 340 ${330 + sway} 360 Q356 ${280 + sway} 318 200 Z`} fill={p.hair} stroke={OL} strokeWidth={4.5} strokeLinejoin="round" />
        <path d={`M330 140 Q370 ${190 + sway} 356 ${270 + sway}`} stroke={p.hairHi} strokeWidth={6} fill="none" strokeLinecap="round" opacity={0.6} />
        <path d="M296 100 Q326 80 338 110 Q330 134 300 128 Z" fill="#2F57C8" stroke={OL} strokeWidth={4} />
      </g>
    );
  if (v === "teacher")
    return <circle cx={200} cy={58} r={46} fill={p.hair} stroke={OL} strokeWidth={4.5} />;
  return null;
};

const HairFront: React.FC<{ v: Variant; p: Pal }> = ({ v, p }) => {
  const shine = <path d="M110 110 Q200 72 290 110" stroke={p.hairHi} strokeWidth={9} fill="none" strokeLinecap="round" opacity={0.55} />;
  if (v === "boy")
    return (
      <g>
        <path d="M64 214 Q50 54 200 46 Q350 54 336 214 Q326 160 300 140 L292 176 L268 132 L244 170 L222 128 L196 168 L170 126 L148 170 L128 136 L106 178 Q84 160 64 214 Z" fill={p.hair} stroke={OL} strokeWidth={4.5} strokeLinejoin="round" />
        {shine}
      </g>
    );
  if (v === "teacher")
    return (
      <g>
        <path d="M66 240 Q50 60 200 54 Q350 60 334 240 Q322 150 270 120 Q238 150 186 140 Q130 150 104 176 Q78 200 66 240 Z" fill={p.hair} stroke={OL} strokeWidth={4.5} strokeLinejoin="round" />
        <path d="M84 230 Q80 300 96 330 L112 320 Q100 280 104 220 Z" fill={p.hair} stroke={OL} strokeWidth={4} />
        <path d="M316 230 Q320 300 304 330 L288 320 Q300 280 296 220 Z" fill={p.hair} stroke={OL} strokeWidth={4} />
        {shine}
      </g>
    );
  // girls: cap + bangs made of pointed locks
  return (
    <g>
      <path d="M62 250 Q46 56 200 48 Q354 56 338 250 Q336 200 318 166 Q312 200 288 214 Q292 176 266 150 Q254 186 226 196 Q230 160 206 140 Q190 178 160 192 Q162 160 146 146 Q132 182 104 200 Q108 170 104 156 Q82 190 80 228 Z" fill={p.hair} stroke={OL} strokeWidth={4.5} strokeLinejoin="round" />
      <path d="M70 230 Q64 320 84 372 L106 360 Q92 300 98 226 Z" fill={p.hair} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      <path d="M330 230 Q336 320 316 372 L294 360 Q308 300 302 226 Z" fill={p.hair} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      {shine}
    </g>
  );
};

const Torso: React.FC<{ blazer: boolean }> = ({ blazer }) =>
  blazer ? (
    <g>
      <path d="M120 360 Q200 340 280 360 Q292 440 286 520 Q200 532 114 520 Q108 440 120 360 Z" fill={NAVY} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      <path d="M172 348 L200 420 L228 348 Z" fill={W} stroke={OL} strokeWidth={3} />
      <path d="M164 352 L200 432 L192 524 M236 352 L200 432 L208 524" stroke="#14235F" strokeWidth={4} fill="none" />
      <circle cx={200} cy={470} r={6} fill="#D8B24A" stroke={OL} strokeWidth={2} />
    </g>
  ) : (
    <g>
      <path d="M118 362 Q200 338 282 362 Q294 440 290 524 Q200 538 110 524 Q106 440 118 362 Z" fill={W} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      {/* soft shadow on one side + hem */}
      <path d="M252 368 Q282 372 284 400 Q290 460 288 520 Q270 526 254 528 Q262 450 252 368 Z" fill={SH} />
      <path d="M116 506 Q200 520 288 506" stroke={SH} strokeWidth={7} fill="none" />
      {/* placket */}
      <rect x={191} y={356} width={18} height={68} rx={4} fill={W} stroke={OL} strokeWidth={3} />
      <circle cx={200} cy={380} r={4} fill="#DCE1EC" stroke={OL} strokeWidth={2} />
      <circle cx={200} cy={406} r={4} fill="#DCE1EC" stroke={OL} strokeWidth={2} />
      {/* navy collar with red tipping */}
      <path d="M150 346 Q200 330 250 346 L266 358 L218 392 L200 362 L182 392 L134 358 Z" fill={NAVY} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      <path d="M140 360 L183 388 M260 360 L217 388" stroke={RED} strokeWidth={3} />
      {/* HaUI badge, left chest */}
      <g transform="translate(206 446)">
        <rect x={0} y={0} width={13} height={13} rx={2} fill="#F2B21B" />
        <text x={16} y={12} fontFamily="'Be Vietnam Pro', sans-serif" fontWeight={800} fontSize={14} fill={NAVY}>HaUI</text>
      </g>
    </g>
  );

// ---------------------------------------------------------------------------
export const Chibi: React.FC<{ v: Variant; pose?: PersonPose; height?: number; flip?: boolean }> = ({ v, pose = {}, height = 500, flip }) => {
  const p = PAL[v];
  const blazer = v === "teacher";
  const w = pose.walk;
  const sw = w === undefined ? 0 : Math.sin(w);
  const bob = (pose.bob ?? 0) + (w === undefined ? 0 : -Math.abs(Math.cos(w)) * 10);
  const rS = pose.rS ?? (w === undefined ? 10 : 22 * sw);
  const lS = pose.lS ?? (w === undefined ? 10 : -22 * sw);
  const rE = pose.rE ?? 6;
  const lE = pose.lE ?? 6;
  const tilt = pose.tilt ?? 0;
  return (
    <svg viewBox="0 0 400 700" width={(height * 400) / 700} height={height} style={{ overflow: "visible", transform: flip ? "scaleX(-1)" : undefined }}>
      <ellipse cx={200} cy={684} rx={110} ry={14} fill="rgba(0,0,0,0.15)" />
      <g transform={`translate(0 ${bob})`}>
        <g transform={`rotate(${tilt} 200 340)`}>
          <HairBack v={v} p={p} sway={sw * 6} />
        </g>
        <Arm x={128} y={378} s={lS} e={lE} side={-1} p={p} blazer={blazer} hold={pose.lHold} back />
        <Leg x={164} y={526} a={w === undefined ? 1 : 16 * sw} p={p} />
        <Leg x={236} y={526} a={w === undefined ? -1 : -16 * sw} p={p} front />
        <Torso blazer={blazer} />
        <g transform={`rotate(${tilt} 200 340)`}>
          <Face v={v} p={p} pose={pose} />
          <HairFront v={v} p={p} />
        </g>
        <Arm x={272} y={378} s={rS} e={rE} side={1} p={p} blazer={blazer} hold={pose.rHold} />
      </g>
    </svg>
  );
};
