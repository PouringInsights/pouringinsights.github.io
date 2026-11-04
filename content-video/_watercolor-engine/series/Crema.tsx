import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { clamp, f, ramp, Wash } from "../watercolor/engine";
import { Block, FilmProps, Film, Ground, P, Painted, PRUSSIAN, Svg, T } from "./kit";

// espresso cup seen from above: rim, coffee, crema glazes
const Cup: React.FC<{ cx: number; cy: number; crema: number; fr: number; id: string }> = ({ cx, cy, crema, id }) => (
  <g>
    <Wash id={`${id}r`} seed={201} color={P.greyblue} cx={cx} cy={cy} r={250} p={1} body={0.18} rim={0.9} distort={14} />
    <Wash id={`${id}c`} seed={202} color="#3A2414" cx={cx} cy={cy} r={190} p={1} body={0.95} rim={0.4} distort={10} />
    <Wash id={`${id}k`} seed={203} color="#C98A3E" cx={cx} cy={cy} r={180} p={crema} body={0.85} rim={0.6} distort={26} blend="normal" />
    <Wash id={`${id}t`} seed={204} color={P.hansa} cx={cx - 30} cy={cy - 20} r={110} p={crema} body={0.45} rim={0.6} distort={30} blend="normal" />
  </g>
);

const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="ch" />
      <Svg><Cup cx={540} cy={1020} crema={ramp(fr, 4, 30)} fr={fr} id="hc" /></Svg>
      <Block top={240}><T size={230} color={P.payne} weight={900}>Crema</T></Block>
      <Block at={14} top={1380}><T size={60} color={P.payne} weight={600}>từng cần cả một tấm biển để giải thích</T></Block>
    </AbsoluteFill>
  );
};

const Steam: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="cs" field={P.payne} ox={0} oy={0} seed={12} />
      <Svg>
        {[0, 1, 2, 3].map((i) => {
          const t = ((fr + i * 22) % 88) / 88;
          return <Wash key={i} id={`st${i}`} seed={210 + i} color={P.paper} cx={420 + i * 80} cy={1300 - t * 600} r={70 + t * 80} p={1} body={0.45 * (1 - t)} rim={0.4 * (1 - t)} distort={30} blend="normal" />;
        })}
      </Svg>
      <Block top={240}><T size={92} color={P.paper}>Trước đó: máy hơi nước</T></Block>
      <Block at={30} top={1420}><T size={60} color={P.paper} weight={600}>nước gần sôi, áp lực thấp, dễ khét, gần như không bọt</T></Block>
    </AbsoluteFill>
  );
};

const Patent: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="cp" />
      <Svg>
        <Painted id="doc" d="M260,640 L820,640 L820,1380 L260,1380 Z" color={P.greyblue} seed={221} body={0.25} p={ramp(fr, 0, 12)} />
        {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={330} y={760 + i * 90} width={420 * ramp(fr, 8 + i * 4, 20 + i * 4)} height={14} fill={P.payne} opacity={0.45} />)}
        <Wash id="seal" seed={222} color={P.crimson} cx={700} cy={1260} r={70} p={ramp(fr, 40, 56)} body={0.85} rim={0.5} distort={12} />
      </Svg>
      <Block top={240}><T size={150} color={P.payne} weight={900}>1938, Milan</T><T size={60} color={P.payne} weight={600}>Gaggia: bằng sáng chế không dùng hơi nước</T></Block>
    </AbsoluteFill>
  );
};

// signature: the lever is pulled down
const Lever: React.FC = () => {
  const fr = useCurrentFrame();
  const a = interpolate(fr, [20, 60], [-70, 25], { ...clamp, easing: (t) => 1 - (1 - t) ** 3 });
  return (
    <AbsoluteFill>
      <Ground id="cl" field={PRUSSIAN} ox={1080} oy={1920} seed={14} />
      <Svg>
        <rect x={420} y={1080} width={240} height={420} fill={P.greyblue} opacity={0.9} />
        <rect x={400} y={1500} width={280} height={40} fill={P.paper} />
        <g transform={`translate(540 1120) rotate(${a})`}>
          <rect x={-14} y={-520} width={28} height={520} rx={14} fill={P.paper} />
          <circle cx={0} cy={-520} r={42} fill={P.crimson} />
        </g>
      </Svg>
      <Block top={240}><T size={150} color={P.paper} weight={900}>1948</T><T size={60} color={P.paper} weight={600}>cần gạt piston: áp lực cao hơn hẳn</T></Block>
    </AbsoluteFill>
  );
};

const Foam: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="cf" />
      <Svg><Cup cx={540} cy={1000} crema={ramp(fr, 0, 40)} fr={fr} id="fc" /></Svg>
      <Block top={240}><T size={92} color={P.payne}>Một lớp bọt vàng nâu</T></Block>
    </AbsoluteFill>
  );
};

const Sign: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="cg" field={P.crimson} ox={0} oy={960} seed={15} />
      <Svg><rect x={120} y={560} width={840} height={520} fill={P.paper} opacity={ramp(fr, 20, 34)} /><rect x={120} y={560} width={840} height={520} fill="none" stroke={P.payne} strokeWidth={12} opacity={ramp(fr, 20, 34)} /></Svg>
      <Block top={240}><T size={60} color={P.paper} weight={600}>theo lời kể: khách ngờ là váng bẩn</T></Block>
      <Block at={34} top={660} left={170} width={760}><T size={92} color={P.payne} weight={900}>caffè crema</T><T size={60} color={P.payne} weight={600} style={{ marginTop: 10 }}>kem cà phê tự nhiên</T></Block>
      <Block at={50} top={1200}><T size={60} color={P.paper} weight={600}>tấm biển Gaggia treo ở quán</T></Block>
    </AbsoluteFill>
  );
};

const Rename: React.FC = () => {
  const fr = useCurrentFrame();
  const strike = ramp(fr, 14, 28);
  return (
    <AbsoluteFill>
      <Ground id="cr" />
      <Block top={600}>
        <div style={{ position: "relative", display: "inline-block" }}>
          <T size={150} color={P.greyblue} weight={900}>váng</T>
          <div style={{ position: "absolute", left: 0, top: "52%", height: 16, width: `${strike * 100}%`, background: P.crimson }} />
        </div>
        <T size={230} color={P.payne} weight={900}>kem.</T>
      </Block>
      <Block at={40} top={1200}><T size={60} color={P.payne} weight={600}>đổi một cái tên, đổi cả cách người ta nhìn</T></Block>
    </AbsoluteFill>
  );
};

const Take: React.FC = () => (
  <AbsoluteFill>
    <Ground id="ct" field={P.sap} ox={540} oy={1920} seed={5} />
    <Block top={300}><T size={92} color={P.paper}>Từ quầy bar:</T><T size={150} color={P.hansa} weight={900}>crema dày chưa chắc ngon</T></Block>
    <Block at={60} top={1000}><T size={60} color={P.paper} weight={600}>nó cho biết hạt còn tươi và áp lực đủ, chứ không nói hộ vị</T></Block>
  </AbsoluteFill>
);

const Question: React.FC<{ endAt: number }> = ({ endAt }) => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="cq" />
      {fr < endAt ? (
        <Block at={6} top={600}><T size={92} color={P.payne}>Bạn có khuấy crema trước khi uống không?</T><T size={60} color={P.crimson} weight={700} style={{ marginTop: 20 }}>Comment có hoặc không.</T></Block>
      ) : (
        <>
          <Svg><Cup cx={540} cy={1250} crema={1} fr={fr} id="ec" /></Svg>
          <Block at={endAt} top={420}><T size={92} color={P.payne}>Váng hay kem?</T><T size={150} color={P.crimson} weight={900}>Tùy cái tên.</T></Block>
        </>
      )}
    </AbsoluteFill>
  );
};

export const CremaFilm: React.FC<FilmProps> = (props) => {
  const b = props.beats;
  return (
    <Film props={props} scenes={[
      { from: 0, to: b.steam, el: <Hook /> },
      { from: b.steam, to: b.patent, el: <Steam /> },
      { from: b.patent, to: b.lever, el: <Patent /> },
      { from: b.lever, to: b.foam, el: <Lever /> },
      { from: b.foam, to: b.sign, el: <Foam /> },
      { from: b.sign, to: b.rename, el: <Sign /> },
      { from: b.rename, to: b.take, el: <Rename /> },
      { from: b.take, to: b.question, el: <Take /> },
      { from: b.question, to: props.duration, el: <Question endAt={f(props.duration - 2.6 - b.question)} /> },
    ]} />
  );
};
