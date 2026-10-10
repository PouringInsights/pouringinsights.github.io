// Cast for Version C: chibi-proportioned characters in the HaUI white polo
// (navy collar & sleeve cuffs with a red tipping line, HaUI badge on the left
// chest, wide-leg trousers). Every joint is a prop so scenes can animate them.
import React from "react";

export type Variant = "longHair" | "ponytail" | "boy" | "teacher";

export type PersonPose = {
  walk?: number; // walk phase (radians); undefined = standing
  // shoulder / elbow, degrees. 0 = arm hanging. Positive = arm swings outward
  // (away from the body) for both arms.
  rS?: number;
  rE?: number;
  lS?: number;
  lE?: number;
  mouth?: number; // 0..1
  blink?: number; // 0..1
  tilt?: number; // head tilt deg
  look?: number; // eye shift -1..1
  bob?: number;
  smile?: boolean;
  rHold?: Prop;
  lHold?: Prop;
};
export type Prop = "laptop" | "megaphone" | "box" | "tablet" | "cap" | "phone" | "none";

const INK = "#2B2238";
const NAVY = "#1C2F7A";
const RED = "#D7263D";
const WHITE = "#FFFFFF";
const SHADE = "#E6E9F2";

const PAL: Record<Variant, { skin: string; skinSh: string; hair: string; hairHi: string; pants: string; pantsSh: string; shoe: string; top: "polo" | "blazer" }> = {
  longHair: { skin: "#F7D5BE", skinSh: "#EDBDA2", hair: "#3B2620", hairHi: "#5A3A2E", pants: "#E9E1D2", pantsSh: "#D6CCBA", shoe: "#FFFFFF", top: "polo" },
  ponytail: { skin: "#F5CFB4", skinSh: "#E8B796", hair: "#2A1C18", hairHi: "#4A3028", pants: "#CFC2A6", pantsSh: "#B9AB8D", shoe: "#FFFFFF", top: "polo" },
  boy: { skin: "#EFC6A8", skinSh: "#DDAA88", hair: "#1E1A1A", hairHi: "#3A3333", pants: "#A79B82", pantsSh: "#8F846C", shoe: "#F2F2F2", top: "polo" },
  teacher: { skin: "#F6D2BA", skinSh: "#E8B99E", hair: "#2C1F1B", hairHi: "#4B342C", pants: "#2B3352", pantsSh: "#20273F", shoe: "#3A3F55", top: "blazer" },
};

// ---------------------------------------------------------------------------
const Arm: React.FC<{ x: number; y: number; s: number; e: number; side: 1 | -1; skin: string; skinSh: string; top: "polo" | "blazer"; hold?: Prop; back?: boolean }> = ({ x, y, s, e, side, skin, skinSh, top, hold, back }) => {
  // side: +1 = arm on the viewer's right. Outward rotation = -side*angle
  const a1 = -side * s;
  const a2 = -side * e;
  const skinC = back ? skinSh : skin;
  const sleeve = top === "polo" ? (back ? SHADE : WHITE) : back ? "#18295F" : NAVY;
  return (
    <g transform={`translate(${x} ${y}) rotate(${a1})`}>
      {/* upper arm */}
      <rect x={-21} y={-6} width={42} height={112} rx={21} fill={top === "polo" ? skinC : sleeve} stroke={INK} strokeWidth={4} />
      {/* forearm + hand */}
      <g transform={`translate(0 100) rotate(${a2})`}>
        <rect x={-18} y={-10} width={36} height={98} rx={18} fill={top === "polo" ? skinC : sleeve} stroke={INK} strokeWidth={4} />
        {top === "blazer" ? <rect x={-20} y={60} width={40} height={16} rx={6} fill={WHITE} stroke={INK} strokeWidth={3} /> : null}
        <g transform="translate(0 92)">
          <HoldProp prop={hold} side={side} />
          <ellipse cx={0} cy={8} rx={20} ry={22} fill={skinC} stroke={INK} strokeWidth={4} />
          <ellipse cx={side * -14} cy={0} rx={8} ry={12} fill={skinC} stroke={INK} strokeWidth={3.5} transform={`rotate(${side * 30} ${side * -14} 0)`} />
        </g>
      </g>
      {/* short polo sleeve over the upper arm: navy cuff + red tipping */}
      {top === "polo" ? (
        <g>
          <path d="M-30 -10 Q-4 -34 30 -12 L36 50 L-30 50 Z" fill={sleeve} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
          <rect x={-34} y={44} width={68} height={16} rx={4} fill={NAVY} stroke={INK} strokeWidth={3} />
          <rect x={-33} y={52} width={66} height={3} fill={RED} />
        </g>
      ) : (
        <path d="M-27 -14 Q0 -28 27 -14 L25 70 L-25 70 Z" fill={sleeve} stroke={INK} strokeWidth={4} />
      )}
    </g>
  );
};

const HoldProp: React.FC<{ prop?: Prop; side: 1 | -1 }> = ({ prop, side }) => {
  if (!prop || prop === "none") return null;
  if (prop === "laptop")
    return (
      <g transform={`translate(${side * -40} -30) rotate(${side * -8})`}>
        <rect x={-70} y={-10} width={140} height={90} rx={8} fill="#C9D3E8" stroke={INK} strokeWidth={4} />
        <rect x={-60} y={0} width={120} height={70} rx={4} fill="#7DB2FF" />
        <rect x={-50} y={44} width={14} height={20} fill="#FFC93C" />
        <rect x={-30} y={30} width={14} height={34} fill="#FFFFFF" />
        <rect x={-10} y={18} width={14} height={46} fill="#FF6B4A" />
        <path d="M10 50 L30 30 L50 38" stroke="#FFFFFF" strokeWidth={4} fill="none" />
      </g>
    );
  if (prop === "megaphone")
    return (
      <g transform={`translate(${side * 10} -6) rotate(${side * -70})`}>
        <path d="M0 -14 L80 -46 L80 46 L0 14 Z" fill="#FF6B4A" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
        <rect x={-18} y={-16} width={22} height={32} rx={6} fill="#FFC93C" stroke={INK} strokeWidth={4} />
        <ellipse cx={80} cy={0} rx={10} ry={46} fill="#FFD9CF" stroke={INK} strokeWidth={4} />
      </g>
    );
  if (prop === "box")
    return (
      <g transform="translate(0 -40)">
        <rect x={-62} y={-20} width={124} height={96} rx={6} fill="#D9A866" stroke={INK} strokeWidth={4} />
        <rect x={-62} y={-20} width={124} height={20} fill="#C99550" stroke={INK} strokeWidth={4} />
        <rect x={-12} y={-20} width={24} height={96} fill="#EFD3A5" />
      </g>
    );
  if (prop === "tablet")
    return (
      <g transform={`translate(${side * -30} -40) rotate(${side * -10})`}>
        <rect x={-46} y={-20} width={92} height={124} rx={10} fill={NAVY} stroke={INK} strokeWidth={4} />
        <rect x={-38} y={-12} width={76} height={104} rx={5} fill="#7DB2FF" />
        <rect x={-28} y={48} width={12} height={34} fill="#FFC93C" />
        <rect x={-10} y={30} width={12} height={52} fill="#FFFFFF" />
        <rect x={8} y={14} width={12} height={68} fill="#FF6B4A" />
      </g>
    );
  if (prop === "phone")
    return <rect x={-16} y={-34} width={32} height={58} rx={6} fill="#222" stroke={INK} strokeWidth={3} />;
  if (prop === "cap")
    return (
      <g transform="translate(0 -26)">
        <path d="M-60 0 L0 -26 L60 0 L0 26 Z" fill="#1B1B2E" stroke={INK} strokeWidth={4} />
        <path d="M30 6 L44 40" stroke="#FFC93C" strokeWidth={5} />
      </g>
    );
  return null;
};

const Leg: React.FC<{ x: number; y: number; a: number; c: string; cs: string; shoe: string; front?: boolean }> = ({ x, y, a, c, cs, shoe, front }) => (
  <g transform={`translate(${x} ${y}) rotate(${a})`}>
    {/* wide-leg trouser */}
    <path d="M-36 -10 L36 -10 L50 300 L-48 300 Z" fill={front ? c : cs} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
    <path d="M6 20 L10 290" stroke={cs} strokeWidth={3} opacity={0.8} />
    {/* shoe */}
    <path d="M-40 296 Q-46 330 -10 334 L46 334 Q58 330 54 312 Q50 298 34 298 Z" fill={shoe} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
  </g>
);

// ---------------------------------------------------------------------------
const HairBack: React.FC<{ v: Variant; c: string; sway: number }> = ({ v, c, sway }) => {
  if (v === "longHair")
    return <path d={`M92 180 Q84 320 ${110 + sway} 410 L${292 + sway} 410 Q318 320 308 180 Z`} fill={c} stroke={INK} strokeWidth={4} />;
  if (v === "ponytail")
    return (
      <g>
        <path d={`M286 130 Q350 ${170 + sway} 334 ${280 + sway * 2} Q322 330 300 300 Q324 230 286 160 Z`} fill={c} stroke={INK} strokeWidth={4} />
        <circle cx={292} cy={140} r={14} fill="#1C2F7A" stroke={INK} strokeWidth={3} />
      </g>
    );
  if (v === "teacher")
    return <path d="M96 190 Q96 300 140 310 L260 310 Q304 300 304 190 Z" fill={c} stroke={INK} strokeWidth={4} />;
  return null;
};

const HairFront: React.FC<{ v: Variant; c: string; hi: string }> = ({ v, c, hi }) => {
  if (v === "boy")
    return (
      <g>
        <path d="M94 186 Q86 70 200 64 Q318 68 306 190 Q296 150 272 132 Q250 160 210 140 Q186 166 150 146 Q118 160 94 186 Z" fill={c} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
        <path d="M150 92 Q190 76 236 90" stroke={hi} strokeWidth={6} fill="none" strokeLinecap="round" />
      </g>
    );
  if (v === "teacher")
    return (
      <g>
        <path d="M92 214 Q78 80 200 72 Q324 80 308 214 Q296 150 240 128 Q210 150 160 150 Q118 160 92 214 Z" fill={c} stroke={INK} strokeWidth={4} />
        <circle cx={200} cy={68} r={30} fill={c} stroke={INK} strokeWidth={4} />
        <path d="M150 96 Q196 82 246 98" stroke={hi} strokeWidth={6} fill="none" strokeLinecap="round" />
      </g>
    );
  // girls: straight fringe with centre part
  return (
    <g>
      <path d="M90 230 Q76 76 200 70 Q324 76 310 230 Q300 170 280 140 Q244 120 204 128 L200 104 L196 128 Q150 124 120 142 Q100 170 90 230 Z" fill={c} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      <path d="M140 98 Q172 84 196 90" stroke={hi} strokeWidth={6} fill="none" strokeLinecap="round" />
      <path d="M210 90 Q240 84 262 100" stroke={hi} strokeWidth={6} fill="none" strokeLinecap="round" />
    </g>
  );
};

const Face: React.FC<{ v: Variant; skin: string; skinSh: string; pose: PersonPose }> = ({ v, skin, skinSh, pose }) => {
  const blink = pose.blink ?? 0;
  const look = (pose.look ?? 0) * 6;
  const mouth = pose.mouth ?? 0;
  const glasses = v === "teacher" || v === "longHair";
  return (
    <g>
      <ellipse cx={200} cy={196} rx={108} ry={116} fill={skin} stroke={INK} strokeWidth={4} />
      <ellipse cx={93} cy={206} rx={14} ry={22} fill={skinSh} stroke={INK} strokeWidth={3.5} />
      <ellipse cx={307} cy={206} rx={14} ry={22} fill={skinSh} stroke={INK} strokeWidth={3.5} />
      {/* brows */}
      <path d="M140 170 Q158 160 176 166" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
      <path d="M224 166 Q242 160 260 170" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
      {/* eyes */}
      {blink > 0.5 ? (
        <>
          <path d="M142 206 Q158 214 174 206" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
          <path d="M226 206 Q242 214 258 206" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
        </>
      ) : (
        <>
          {[158, 242].map((cx) => (
            <g key={cx}>
              <ellipse cx={cx + look} cy={206} rx={15} ry={19} fill={INK} />
              <ellipse cx={cx + look} cy={212} rx={11} ry={10} fill="#5B4A7A" />
              <circle cx={cx + look + 5} cy={199} r={5.5} fill={WHITE} />
              <circle cx={cx + look - 5} cy={215} r={2.5} fill={WHITE} />
            </g>
          ))}
        </>
      )}
      {glasses ? (
        <g fill="none" stroke={v === "teacher" ? "#7A5A3A" : "#B8A9C9"} strokeWidth={4}>
          <rect x={128} y={182} width={60} height={50} rx={18} />
          <rect x={212} y={182} width={60} height={50} rx={18} />
          <path d="M188 204 Q200 198 212 204" />
        </g>
      ) : null}
      {/* nose + cheeks */}
      <path d="M198 232 Q202 238 206 234" stroke={skinSh} strokeWidth={4} fill="none" strokeLinecap="round" />
      <ellipse cx={136} cy={246} rx={17} ry={9} fill="#F4A3A0" opacity={0.6} />
      <ellipse cx={264} cy={246} rx={17} ry={9} fill="#F4A3A0" opacity={0.6} />
      {/* mouth */}
      {mouth > 0.08 ? (
        <path d={`M182 256 Q200 ${258 + 26 * mouth} 218 256 Q200 ${254 + 4 * mouth} 182 256 Z`} fill="#B84A55" stroke={INK} strokeWidth={3.5} strokeLinejoin="round" />
      ) : (
        <path d="M182 254 Q200 270 218 254" stroke={INK} strokeWidth={4.5} fill="none" strokeLinecap="round" />
      )}
    </g>
  );
};

const Torso: React.FC<{ top: "polo" | "blazer"; female: boolean }> = ({ top, female }) => {
  const waist = female ? 10 : 0;
  if (top === "blazer")
    return (
      <g>
        <path d={`M118 330 Q200 306 282 330 L${292 - waist} 470 L292 590 L108 590 L${108 + waist} 470 Z`} fill={NAVY} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
        <path d="M168 318 L200 400 L232 318 Z" fill={WHITE} stroke={INK} strokeWidth={3} />
        <path d="M160 322 L200 420 L188 590 M240 322 L200 420 L212 590" stroke={INK} strokeWidth={3} fill="none" />
        <circle cx={200} cy={470} r={6} fill="#C9A44A" stroke={INK} strokeWidth={2} />
        <rect x={238} y={400} width={30} height={6} rx={2} fill="#C9A44A" />
      </g>
    );
  return (
    <g>
      {/* white polo body */}
      <path d={`M116 336 Q200 312 284 336 L${290 - waist} 470 Q${296 - waist / 2} 560 286 596 L114 596 Q${104 + waist / 2} 560 ${110 + waist} 470 Z`} fill={WHITE} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      <path d="M118 560 Q200 576 282 560" stroke={SHADE} strokeWidth={8} fill="none" />
      {/* placket + buttons */}
      <rect x={190} y={330} width={20} height={90} rx={4} fill={WHITE} stroke={INK} strokeWidth={3} />
      <circle cx={200} cy={360} r={4.5} fill="#E3E7EF" stroke={INK} strokeWidth={2} />
      <circle cx={200} cy={394} r={4.5} fill="#E3E7EF" stroke={INK} strokeWidth={2} />
      {/* navy collar with red tipping */}
      <path d="M150 318 Q200 300 250 318 L264 330 L216 366 L200 336 L184 366 L136 330 Z" fill={NAVY} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      <path d="M140 331 L184 362 M260 331 L216 362" stroke={RED} strokeWidth={3} />
      {/* HaUI badge on the left chest (viewer's right) */}
      <g transform="translate(212 420)">
        <rect x={0} y={0} width={12} height={12} rx={2} fill="#F2B21B" />
        <text x={15} y={11.5} fontFamily="'Be Vietnam Pro', sans-serif" fontWeight={800} fontSize={13} fill={NAVY}>HaUI</text>
      </g>
    </g>
  );
};

// ---------------------------------------------------------------------------
export const Person: React.FC<{ v: Variant; pose?: PersonPose; height?: number; flip?: boolean }> = ({ v, pose = {}, height = 600, flip }) => {
  const p = PAL[v];
  const female = v !== "boy";
  const w = pose.walk;
  const sw = w === undefined ? 0 : Math.sin(w);
  const bob = (pose.bob ?? 0) + (w === undefined ? 0 : -Math.abs(Math.cos(w)) * 10);
  const rS = pose.rS ?? (w === undefined ? 6 : 16 * sw);
  const lS = pose.lS ?? (w === undefined ? 6 : -16 * sw);
  const rE = pose.rE ?? 8;
  const lE = pose.lE ?? 8;
  const tilt = pose.tilt ?? 0;
  return (
    <svg viewBox="0 0 400 1000" width={height * 0.4} height={height} style={{ overflow: "visible", transform: flip ? "scaleX(-1)" : undefined }}>
      <ellipse cx={200} cy={958} rx={130} ry={18} fill="rgba(0,0,0,0.16)" />
      <g transform={`translate(0 ${bob})`}>
        <g transform={`rotate(${tilt} 200 300)`}>
          <HairBack v={v} c={p.hair} sway={sw * 6} />
        </g>
        <Arm x={128} y={354} s={lS} e={lE} side={-1} skin={p.skin} skinSh={p.skinSh} top={p.top} hold={pose.lHold} back />
        <Leg x={160} y={600} a={w === undefined ? 2 : 14 * sw} c={p.pants} cs={p.pantsSh} shoe={p.shoe} />
        <Leg x={240} y={600} a={w === undefined ? -2 : -14 * sw} c={p.pants} cs={p.pantsSh} shoe={p.shoe} front />
        {/* waistband */}
        <rect x={108} y={584} width={184} height={26} rx={8} fill={p.pants} stroke={INK} strokeWidth={4} />
        {/* neck */}
        <rect x={180} y={286} width={40} height={50} rx={14} fill={p.skinSh} stroke={INK} strokeWidth={4} />
        <Torso top={p.top} female={female} />
        <g transform={`rotate(${tilt} 200 300)`}>
          <Face v={v} skin={p.skin} skinSh={p.skinSh} pose={pose} />
          <HairFront v={v} c={p.hair} hi={p.hairHi} />
          {v === "longHair" ? (
            <g>
              <path d={`M96 210 Q92 320 ${118 + sw * 4} 420 L150 420 Q132 320 130 220 Z`} fill={p.hair} stroke={INK} strokeWidth={4} />
              <path d={`M304 210 Q308 320 ${282 + sw * 4} 420 L250 420 Q268 320 270 220 Z`} fill={p.hair} stroke={INK} strokeWidth={4} />
            </g>
          ) : null}
        </g>
        <Arm x={272} y={354} s={rS} e={rE} side={1} skin={p.skin} skinSh={p.skinSh} top={p.top} hold={pose.rHold} />
      </g>
    </svg>
  );
};

export const blink = (frame: number, seed = 0) => {
  const c = (frame + seed * 37) % 120;
  return c >= 110 && c <= 114 ? 1 : 0;
};
