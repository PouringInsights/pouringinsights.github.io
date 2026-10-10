// "Host": a flat-style female presenter in a white HaUI polo, rigged in SVG.
// Every joint is driven by props so scenes can choreograph her frame by frame.
import React from "react";

export type HostPose = {
  /** walk cycle phase in radians; undefined = standing */
  walk?: number;
  /** shoulder / elbow angles in degrees (0 = hanging down; positive = forward/up) */
  lShoulder?: number;
  lElbow?: number;
  rShoulder?: number;
  rElbow?: number;
  /** 0..1 mouth openness */
  mouth?: number;
  /** 0..1 eyelid closed */
  blink?: number;
  /** head tilt in degrees */
  tilt?: number;
  /** body bob in px */
  bob?: number;
  /** hold a tablet in the left hand */
  tablet?: boolean;
};

const SKIN = "#F5CDB0";
const SKIN_SH = "#E7B595";
const HAIR = "#2A1D1A";
const SHIRT = "#FFFFFF";
const SHIRT_SH = "#E3E8F2";
const NAVY = "#14286B";
const PANTS = "#1B2A55";
const SHOE = "#F4F4F4";
const LINE = "#1A1F36";

const Limb: React.FC<{
  x: number;
  y: number;
  a1: number;
  a2: number;
  l1: number;
  l2: number;
  w1: number;
  w2: number;
  c1: string;
  c2: string;
  end?: React.ReactNode;
  sleeve?: number;
}> = ({ x, y, a1, a2, l1, l2, w1, w2, c1, c2, end, sleeve }) => (
  <g transform={`translate(${x} ${y}) rotate(${a1})`}>
    <line x1={0} y1={0} x2={0} y2={l1} stroke={LINE} strokeWidth={w1 + 6} strokeLinecap="round" />
    <g transform={`translate(0 ${l1}) rotate(${a2})`}>
      <line x1={0} y1={0} x2={0} y2={l2} stroke={LINE} strokeWidth={w2 + 6} strokeLinecap="round" />
      <line x1={0} y1={0} x2={0} y2={l2} stroke={c2} strokeWidth={w2} strokeLinecap="round" />
    </g>
    <line x1={0} y1={0} x2={0} y2={l1} stroke={sleeve ? c2 : c1} strokeWidth={w1} strokeLinecap="round" />
    {sleeve ? <line x1={0} y1={0} x2={0} y2={l1 * sleeve} stroke={c1} strokeWidth={w1 + 8} strokeLinecap="butt" /> : null}
    <g transform={`translate(0 ${l1}) rotate(${a2})`}>
      <g transform={`translate(0 ${l2})`}>{end}</g>
    </g>
  </g>
);

export const Host: React.FC<{ pose: HostPose; height?: number; flip?: boolean }> = ({
  pose,
  height = 720,
  flip = false,
}) => {
  const walk = pose.walk;
  const sw = walk === undefined ? 0 : Math.sin(walk);
  const bob = (pose.bob ?? 0) + (walk === undefined ? 0 : -Math.abs(Math.cos(walk)) * 8);
  // legs: hips at (200, 520)
  const lHip = walk === undefined ? 3 : 24 * sw;
  const rHip = walk === undefined ? -3 : -24 * sw;
  const lKnee = walk === undefined ? 0 : Math.max(0, -30 * Math.cos(walk));
  const rKnee = walk === undefined ? 0 : Math.max(0, 30 * Math.cos(walk));
  // arms swing opposite the legs when walking unless overridden
  const ls = pose.lShoulder ?? (walk === undefined ? 8 : -18 * sw);
  const rs = pose.rShoulder ?? (walk === undefined ? -8 : 18 * sw);
  const le = pose.lElbow ?? 10;
  const re = pose.rElbow ?? -10;
  const mouth = pose.mouth ?? 0;
  const blink = pose.blink ?? 0;
  const tilt = pose.tilt ?? 0;

  const hand = <circle r={15} fill={SKIN} />;
  const shoe = (
    <g>
      <path d="M-16 -4 Q-18 14 0 16 L30 16 Q34 6 22 0 L8 -6 Z" fill={SHOE} stroke={LINE} strokeWidth={3} />
    </g>
  );

  return (
    <svg
      viewBox="0 0 400 900"
      width={(height * 400) / 900}
      height={height}
      style={{ overflow: "visible", transform: flip ? "scaleX(-1)" : undefined }}
    >
      {/* ground shadow */}
      <ellipse cx={200} cy={872} rx={110} ry={16} fill="rgba(0,0,0,0.18)" />
      <g transform={`translate(0 ${bob})`}>
        {/* back arm (right side of body from viewer = character's left) */}
        <Limb x={160} y={330} a1={-ls} a2={-le} l1={115} l2={110} w1={34} w2={28} c1={SHIRT_SH} c2={SKIN_SH} sleeve={0.5} end={pose.tablet ? <Tablet /> : <circle r={15} fill={SKIN_SH} />} />
        {/* legs */}
        <Limb x={175} y={540} a1={lHip} a2={lKnee} l1={150} l2={150} w1={52} w2={44} c1={PANTS} c2={PANTS} end={shoe} />
        <Limb x={225} y={540} a1={rHip} a2={rKnee} l1={150} l2={150} w1={52} w2={44} c1={PANTS} c2={PANTS} end={shoe} />
        {/* torso: polo */}
        <path d="M140 320 Q200 296 260 320 L272 470 Q276 548 252 556 L148 556 Q124 548 128 470 Z" fill={SHIRT} stroke={LINE} strokeWidth={4} />
        {/* polo collar + placket */}
        <path d="M172 312 L200 348 L228 312 L240 318 L212 362 L200 352 L188 362 L160 318 Z" fill={NAVY} />
        <line x1={200} y1={352} x2={200} y2={410} stroke={NAVY} strokeWidth={4} />
        <circle cx={200} cy={372} r={3.5} fill={NAVY} />
        <circle cx={200} cy={392} r={3.5} fill={NAVY} />
        {/* HaUI-style badge */}
        <rect x={218} y={376} width={30} height={14} rx={3} fill="#FFC93C" />
        <rect x={252} y={379} width={0} height={8} fill={NAVY} />
        {/* belt line */}
        <rect x={134} y={528} width={132} height={14} rx={6} fill={PANTS} />
        {/* neck */}
        <rect x={186} y={270} width={28} height={44} rx={10} fill={SKIN_SH} />
        {/* head */}
        <g transform={`rotate(${tilt} 200 260)`}>
          {/* back hair / ponytail */}
          <path d="M138 170 Q120 250 150 290 L250 290 Q280 250 262 170 Z" fill={HAIR} />
          <path d={`M254 176 Q300 ${200 + sw * 6} 288 ${270 + sw * 8} Q276 300 262 262 Q276 220 254 176 Z`} fill={HAIR} />
          {/* face */}
          <ellipse cx={200} cy={200} rx={66} ry={76} fill={SKIN} />
          <ellipse cx={136} cy={208} rx={10} ry={16} fill={SKIN_SH} />
          <ellipse cx={264} cy={208} rx={10} ry={16} fill={SKIN_SH} />
          {/* fringe */}
          <path d="M132 196 Q130 116 204 116 Q272 118 270 192 Q246 150 214 146 Q198 172 160 168 Q146 178 132 196 Z" fill={HAIR} />
          {/* brows */}
          <path d="M168 182 Q178 176 190 180" stroke={HAIR} strokeWidth={4} fill="none" strokeLinecap="round" />
          <path d="M210 180 Q222 176 232 182" stroke={HAIR} strokeWidth={4} fill="none" strokeLinecap="round" />
          {/* eyes */}
          {blink > 0.5 ? (
            <>
              <path d="M170 204 Q179 208 188 204" stroke={LINE} strokeWidth={4} fill="none" strokeLinecap="round" />
              <path d="M212 204 Q221 208 230 204" stroke={LINE} strokeWidth={4} fill="none" strokeLinecap="round" />
            </>
          ) : (
            <>
              <ellipse cx={179} cy={204} rx={7} ry={9} fill={LINE} />
              <ellipse cx={221} cy={204} rx={7} ry={9} fill={LINE} />
              <circle cx={181} cy={201} r={2.4} fill="#fff" />
              <circle cx={223} cy={201} r={2.4} fill="#fff" />
            </>
          )}
          {/* cheeks */}
          <ellipse cx={162} cy={228} rx={12} ry={7} fill="#F2A7A0" opacity={0.55} />
          <ellipse cx={238} cy={228} rx={12} ry={7} fill="#F2A7A0" opacity={0.55} />
          {/* mouth */}
          {mouth > 0.08 ? (
            <path d={`M186 238 Q200 ${240 + 18 * mouth} 214 238 Q200 ${236 + 4 * mouth} 186 238 Z`} fill="#B5474A" stroke={LINE} strokeWidth={2.5} />
          ) : (
            <path d="M186 238 Q200 250 214 238" stroke={LINE} strokeWidth={3.5} fill="none" strokeLinecap="round" />
          )}
        </g>
        {/* front arm (character's right) */}
        <Limb x={240} y={330} a1={rs} a2={re} l1={115} l2={110} w1={34} w2={28} c1={SHIRT} c2={SKIN} sleeve={0.5} end={hand} />
        {/* sleeve outlines */}
      </g>
    </svg>
  );
};

const Tablet: React.FC = () => (
  <g transform="rotate(-8)">
    <rect x={-46} y={-20} width={92} height={120} rx={10} fill={NAVY} stroke={LINE} strokeWidth={3} />
    <rect x={-38} y={-12} width={76} height={100} rx={5} fill="#7DB2FF" />
    <rect x={-30} y={50} width={12} height={30} fill="#FFC93C" />
    <rect x={-12} y={34} width={12} height={46} fill="#FFFFFF" />
    <rect x={6} y={20} width={12} height={60} fill="#FF6B4A" />
  </g>
);

// ---------------------------------------------------------------------------
// Pose helpers
// ---------------------------------------------------------------------------
export const blinkAt = (frame: number) => {
  const c = frame % 110;
  return c >= 100 && c <= 104 ? 1 : 0;
};
/** fake lip movement while `talking` (replaced by real audio amplitude later) */
export const talkMouth = (frame: number, talking: boolean) =>
  talking ? 0.25 + 0.55 * Math.abs(Math.sin(frame * 0.55) * Math.sin(frame * 0.23 + 1)) : 0;
