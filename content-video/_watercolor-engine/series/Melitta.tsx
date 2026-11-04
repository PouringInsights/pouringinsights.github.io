import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { clamp, f, ramp, Wash } from "../watercolor/engine";
import { Block, FilmProps, Film, Ground, P, Painted, Svg, T } from "./kit";

const POT = "M-260,-120 L260,-120 L230,170 Q225,200 195,200 L-195,200 Q-225,200 -230,170 Z";

// ruled notebook sheet, optionally torn on its top edge
const Sheet: React.FC<{ w: number; h: number; torn?: boolean }> = ({ w, h, torn }) => {
  const top = torn
    ? Array.from({ length: 21 }, (_, i) => `${-w / 2 + (w * i) / 20},${-h / 2 + (i % 2 ? 10 : -6)}`).join(" L")
    : `${-w / 2},${-h / 2} L${w / 2},${-h / 2}`;
  return (
    <g>
      <path d={`M${top} L${w / 2},${h / 2} L${-w / 2},${h / 2} Z`} fill="#FBFBF8" stroke={P.greyblue} strokeWidth={4} />
      {Array.from({ length: Math.floor(h / 46) - 1 }, (_, i) => (
        <line key={i} x1={-w / 2 + 20} x2={w / 2 - 20} y1={-h / 2 + 46 * (i + 1)} y2={-h / 2 + 46 * (i + 1)} stroke={P.greyblue} strokeOpacity={0.55} strokeWidth={3} />
      ))}
      <line x1={-w / 2 + 70} x2={-w / 2 + 70} y1={-h / 2} y2={h / 2} stroke={P.crimson} strokeOpacity={0.6} strokeWidth={3} />
    </g>
  );
};

const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="mh" />
      <Svg><g transform={`translate(560 1060) rotate(${-6 + ramp(fr, 0, 20) * 3})`} opacity={ramp(fr, 0, 12)}><Sheet w={640} h={600} /></g></Svg>
      <Block top={240}><T size={150} color={P.payne} weight={900}>Giấy lọc</T></Block>
      <Block at={10} top={1440}><T size={60} color={P.payne} weight={600}>bắt đầu từ vở bài tập của một cậu bé</T></Block>
    </AbsoluteFill>
  );
};

const Dresden: React.FC = () => {
  const fr = useCurrentFrame();
  const specks = Array.from({ length: 26 }, (_, i) => ({ x: 200 + ((i * 137) % 700), y: 880 + ((i * 89) % 420), r: 10 + (i % 4) * 5 }));
  return (
    <AbsoluteFill>
      <Ground id="md" field={P.payne} ox={0} oy={0} seed={12} />
      <Svg>
        <Wash id="mdcup" seed={71} color={P.umber} cx={540} cy={1080} r={280} p={ramp(fr, 6, 26)} body={0.9} rim={0.5} distort={20} />
        {specks.map((s, i) => <circle key={i} cx={s.x} cy={s.y} r={s.r * ramp(fr, 40 + i, 52 + i)} fill="#1A120C" />)}
      </Svg>
      <Block top={240}><T size={92} color={P.paper}>Dresden, đầu thế kỷ 20</T></Block>
      <Block at={30} top={1450}><T size={60} color={P.paper} weight={600}>cà phê kiểu cũ: đắng, lợn cợn bã</T></Block>
    </AbsoluteFill>
  );
};

// signature: holes punched one by one, then a torn page drops in
const Pot: React.FC<{ paperAt: number }> = ({ paperAt }) => {
  const fr = useCurrentFrame();
  const holes = [-150, -90, -30, 30, 90, 150];
  const drop = interpolate(fr - paperAt, [0, 20], [-700, 0], { ...clamp, easing: (t) => 1 - (1 - t) ** 3 });
  return (
    <AbsoluteFill>
      <Ground id="mp" />
      <Svg>
        <g transform="translate(540 1120)">
          <Painted id="pot" d={POT} color={P.hansa} seed={81} stroke={P.payne} body={0.8} p={ramp(fr, 0, 12)} />
          {holes.map((x, i) => {
            const p = ramp(fr, 10 + i * 6, 14 + i * 6);
            return <circle key={i} cx={x} cy={190} r={12 * p} fill={P.payne} />;
          })}
          {/* the nail */}
          {fr < 10 + holes.length * 6 + 6 ? (
            <g transform={`translate(${holes[Math.min(holes.length - 1, Math.max(0, Math.floor((fr - 10) / 6)))]} ${240 + ((fr % 6) < 3 ? 0 : 30)})`}>
              <rect x={-6} y={0} width={12} height={150} fill={P.greyblue} />
              <rect x={-22} y={140} width={44} height={14} fill={P.greyblue} />
            </g>
          ) : null}
          {fr >= paperAt - 1 ? <g transform={`translate(0 ${drop - 30}) scale(0.72)`}><Sheet w={640} h={300} torn /></g> : null}
        </g>
      </Svg>
      <Block top={240}><T size={92} color={P.payne}>Nồi đồng thau + một cây đinh</T></Block>
      <Block at={paperAt + 6} top={1500}><T size={60} color={P.payne} weight={600}>+ giấy thấm xé từ vở của con trai</T></Block>
    </AbsoluteFill>
  );
};

const Flow: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="mf" field={P.hansa} ox={540} oy={1920} seed={7} />
      <Svg>
        <Wash id="clear" seed={91} color="#C98A3E" cx={540} cy={1060} r={300} p={ramp(fr, 10, 40)} body={0.7} rim={0.7} distort={24} />
        {[0, 1, 2].map((i) => {
          const t = ((fr - i * 8) % 24) / 24;
          return fr > i * 8 ? <circle key={i} cx={540} cy={560 + t * 300} r={11} fill="#C98A3E" /> : null;
        })}
      </Svg>
      <Block top={240}><T size={92} color={P.payne}>Nước đi qua.</T><T size={92} color={P.crimson}>Bã ở lại.</T></Block>
    </AbsoluteFill>
  );
};

const DateScene: React.FC = () => (
  <AbsoluteFill>
    <Ground id="mdt" field={P.crimson} ox={1080} oy={960} seed={15} />
    <Block top={700}><T size={170} color={P.paper} weight={900}>20.6.1908</T></Block>
    <Block at={20} top={1000}><T size={60} color={P.paper} weight={600}>đăng ký bảo hộ phát minh với cơ quan sáng chế Đức</T></Block>
  </AbsoluteFill>
);

const Capital: React.FC = () => {
  const fr = useCurrentFrame();
  const n = Math.round(interpolate(fr, [4, 30], [0, 72], clamp));
  return (
    <AbsoluteFill>
      <Ground id="mc" />
      <Svg>{[0, 1, 2].map((i) => <Wash key={i} id={`coin${i}`} seed={100 + i} color={P.hansa} cx={700 + i * 70} cy={1200 - i * 40} r={90} p={ramp(fr, 6 + i * 6, 24 + i * 6)} body={0.6} rim={0.8} distort={12} />)}</Svg>
      <Block top={600}><T size={230} color={P.crimson} weight={900}>{n} xu</T><T size={60} color={P.payne} weight={600}>vốn ban đầu của công ty</T></Block>
    </AbsoluteFill>
  );
};

const Brand: React.FC = () => (
  <AbsoluteFill>
    <Ground id="mb" field={P.sap} ox={0} oy={1920} seed={5} />
    <Block top={760}><T size={60} color={P.paper} weight={600}>công ty ấy giờ vẫn mang tên bà</T><T size={200} color={P.paper} weight={900}>Melitta</T></Block>
  </AbsoluteFill>
);

const Take: React.FC = () => (
  <AbsoluteFill>
    <Ground id="mt" />
    <Block top={520}><T size={92} color={P.payne}>Cả thế giới pour-over đứng trên một tờ giấy thấm của học trò.</T></Block>
  </AbsoluteFill>
);

const Question: React.FC<{ endAt: number }> = ({ endAt }) => {
  const fr = useCurrentFrame();
  const ended = fr >= endAt;
  return (
    <AbsoluteFill>
      <Ground id="mq" field={P.payne} ox={540} oy={1920} seed={12} />
      {!ended ? (
        <Block at={6} top={640}><T size={92} color={P.paper}>Team phin hay team giấy?</T><T size={60} color={P.hansa} weight={600} style={{ marginTop: 20 }}>Comment một chữ.</T></Block>
      ) : (
        <Block at={endAt} top={760}><T size={92} color={P.paper}>Từ cuốn vở</T><T size={150} color={P.hansa} weight={900}>tới ly của bạn.</T></Block>
      )}
    </AbsoluteFill>
  );
};

export const MelittaFilm: React.FC<FilmProps> = (props) => {
  const b = props.beats;
  return (
    <Film props={props} scenes={[
      { from: 0, to: b.dresden, el: <Hook /> },
      { from: b.dresden, to: b.pot, el: <Dresden /> },
      { from: b.pot, to: b.flow, el: <Pot paperAt={f(b.paper - b.pot)} /> },
      { from: b.flow, to: b.date, el: <Flow /> },
      { from: b.date, to: b.capital, el: <DateScene /> },
      { from: b.capital, to: b.brand, el: <Capital /> },
      { from: b.brand, to: b.take, el: <Brand /> },
      { from: b.take, to: b.question, el: <Take /> },
      { from: b.question, to: props.duration, el: <Question endAt={f(props.duration - 2.4 - b.question)} /> },
    ]} />
  );
};
