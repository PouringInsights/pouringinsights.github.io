import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { clamp, f, ramp, Wash } from "../watercolor/engine";
import { Block, FilmProps, Film, Ground, P, Painted, PRUSSIAN, Svg, T } from "./kit";

const KETTLE = "M-150,-150 Q-170,-260 0,-270 Q170,-260 150,-150 L190,180 Q195,220 150,220 L-150,220 Q-195,220 -190,180 Z M150,-60 Q300,-120 330,-260 L360,-250 Q340,-60 175,40 Z";

const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="sh" />
      <Svg>
        <g transform="translate(520 1080)"><Painted id="kettle" d={KETTLE} color={P.greyblue} seed={151} body={0.8} p={ramp(fr, 0, 14)} /></g>
        {/* mourning band */}
        <rect x={340} y={1000} width={370 * ramp(fr, 18, 34)} height={60} fill={P.payne} />
      </Svg>
      <Block top={240}><T size={200} color={P.payne} weight={900}>1794</T><T size={60} color={P.payne} weight={600}>đám tang cho bình pha cà phê</T></Block>
    </AbsoluteFill>
  );
};

const Law: React.FC = () => (
  <AbsoluteFill>
    <Ground id="sl" field={P.payne} ox={1080} oy={0} seed={12} />
    <Block top={700}><T size={92} color={P.paper}>Uống cà phê</T><T size={150} color={P.crimson} weight={900} style={{ color: "#F0A0B0" }}>= phạm luật</T></Block>
  </AbsoluteFill>
);

// signature: five ban periods painted on a 1750–1830 axis
const PERIODS: [number, number][] = [[1756, 1761], [1766, 1769], [1794, 1796], [1799, 1802], [1817, 1823]];
const Bans: React.FC = () => {
  const fr = useCurrentFrame();
  const x = (y: number) => 110 + ((y - 1750) / 80) * 860;
  return (
    <AbsoluteFill>
      <Ground id="sb" />
      <Svg>
        <rect x={110} y={1000} width={860 * ramp(fr, 0, 20)} height={8} fill={P.payne} />
        {PERIODS.map(([a, b], i) => (
          <g key={i}>
            <Wash id={`ban${i}`} seed={160 + i} color={P.crimson} cx={(x(a) + x(b)) / 2} cy={1004} r={Math.max(36, (x(b) - x(a)) / 2 + 18)} p={ramp(fr, 20 + i * 12, 36 + i * 12)} body={0.8} rim={0.6} distort={16} />
          </g>
        ))}
      </Svg>
      {PERIODS.map(([a], i) => (
        <div key={i} style={{ position: "absolute", left: x(a) - 50, top: i % 2 ? 1110 : 820, opacity: ramp(fr, 26 + i * 12, 36 + i * 12) }}>
          <T size={42} color={P.payne} weight={700}>{a}</T>
        </div>
      ))}
      <Block top={240}><T size={150} color={P.payne} weight={900}>5 lần cấm</T><T size={60} color={P.payne} weight={600}>1756–1823, qua ba đời vua</T></Block>
      <Block at={150} top={1330}><T size={60} color={P.payne} weight={600}>lý do: tốn tiền nhập khẩu, và giới cầm quyền tin nó có hại</T></Block>
    </AbsoluteFill>
  );
};

const Sneak: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="ss" field={PRUSSIAN} ox={0} oy={1920} seed={14} />
      <Svg>
        <Wash id="lamp" seed={171} color={P.hansa} cx={760} cy={1040} r={260} p={ramp(fr, 6, 30)} body={0.35} rim={0.6} distort={30} />
        <Wash id="cupS" seed={172} color={P.umber} cx={760} cy={1100} r={90} p={ramp(fr, 14, 30)} body={0.9} rim={0.5} distort={10} />
      </Svg>
      <Block top={240}><T size={92} color={P.paper}>Người ta uống lén.</T></Block>
      <Block at={60} top={1420}><T size={60} color={P.paper} weight={600}>cảnh sát Stockholm còn lưu hồ sơ bắt người uống cà phê</T></Block>
    </AbsoluteFill>
  );
};

const Twins: React.FC = () => {
  const fr = useCurrentFrame();
  const h1 = interpolate(fr, [60, 200], [0, 520], clamp);
  return (
    <AbsoluteFill>
      <Ground id="st" />
      <Svg>
        <Wash id="tw1" seed={181} color={P.umber} cx={330} cy={1420 - h1 / 2} r={130 + h1 / 6} p={ramp(fr, 50, 70)} body={0.8} rim={0.6} distort={18} />
        <Wash id="tw2" seed={182} color={P.leaf} cx={750} cy={1420 - h1 / 2} r={130 + h1 / 6} p={ramp(fr, 60, 80)} body={0.7} rim={0.6} distort={18} />
      </Svg>
      <Block top={240}><T size={150} color={P.crimson} weight={900}>Giai thoại</T><T size={60} color={P.payne} weight={600}>hai anh em sinh đôi phạm tội</T></Block>
      <Block at={60} top={1520} left={200} width={300}><T size={60} color={P.payne}>cà phê</T></Block>
      <Block at={70} top={1520} left={660} width={300}><T size={60} color={P.payne}>trà</T></Block>
    </AbsoluteFill>
  );
};

const Doctors: React.FC = () => {
  const rows = ["bác sĩ giám sát", "nhà vua (bị ám sát, 1792)"];
  return (
    <AbsoluteFill>
      <Ground id="sd" field={P.crimson} ox={1080} oy={960} seed={15} />
      <Block top={300}><T size={92} color={P.paper}>Ai chết trước?</T></Block>
      {rows.map((r, i) => (
        <Block key={r} at={14 + i * 40} top={700 + i * 180}><T size={60} color={P.paper}>{i + 1}. {r}</T></Block>
      ))}
    </AbsoluteFill>
  );
};

const Myth: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="sm" />
      <Block top={640}><T size={92} color={P.payne}>Nhiều nhà sử học:</T>
        <div style={{ position: "relative", display: "inline-block", marginTop: 20 }}>
          <T size={150} color={P.crimson} weight={900}>có thể là bịa</T>
        </div>
      </Block>
      <Block at={10} top={1100}><T size={42} color={P.payne} weight={600}>nên mình kể nó như một giai thoại</T></Block>
    </AbsoluteFill>
  );
};

const Fika: React.FC<{ fikaAt: number }> = ({ fikaAt }) => (
  <AbsoluteFill>
    <Ground id="sf" field={P.sap} ox={540} oy={1920} seed={5} />
    <Block top={300}><T size={150} color={P.paper} weight={900}>1823</T><T size={60} color={P.paper} weight={600}>lệnh cấm chấm dứt</T></Block>
    <Block at={fikaAt} top={900}><T size={60} color={P.paper} weight={600}>giờ nghỉ uống cà phê có hẳn một từ:</T><T size={230} color={P.hansa} weight={900}>fika</T></Block>
  </AbsoluteFill>
);

const Question: React.FC<{ endAt: number }> = ({ endAt }) => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="sq" field={P.payne} ox={540} oy={1920} seed={12} />
      {fr < endAt ? (
        <Block at={6} top={600}><T size={92} color={P.paper}>Việt Nam cấm cà phê một tuần, bạn trụ nổi không?</T><T size={60} color={P.hansa} weight={600} style={{ marginTop: 20 }}>Comment có hoặc không.</T></Block>
      ) : (
        <Block at={endAt} top={760}><T size={92} color={P.paper}>Cấm năm lần,</T><T size={150} color={P.hansa} weight={900}>thua cả năm.</T></Block>
      )}
    </AbsoluteFill>
  );
};

export const SwedenFilm: React.FC<FilmProps> = (props) => {
  const b = props.beats;
  return (
    <Film props={props} scenes={[
      { from: 0, to: b.law, el: <Hook /> },
      { from: b.law, to: b.bans, el: <Law /> },
      { from: b.bans, to: b.sneak, el: <Bans /> },
      { from: b.sneak, to: b.twins, el: <Sneak /> },
      { from: b.twins, to: b.doctors, el: <Twins /> },
      { from: b.doctors, to: b.myth, el: <Doctors /> },
      { from: b.myth, to: b.end, el: <Myth /> },
      { from: b.end, to: b.question, el: <Fika fikaAt={f(b.fika - b.end) - 20} /> },
      { from: b.question, to: props.duration, el: <Question endAt={f(props.duration - 2.6 - b.question)} /> },
    ]} />
  );
};
