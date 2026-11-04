import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { clamp, f, ramp, Wash } from "../watercolor/engine";
import { Block, FilmProps, Film, Ground, P, Painted, Svg, T } from "./kit";

// signature: a staff whose notes are coffee beans
const BeanNote: React.FC<{ x: number; y: number; p: number }> = ({ x, y, p }) => (
  <g transform={`translate(${x} ${y}) rotate(-20) scale(${p})`}>
    <ellipse rx={34} ry={24} fill={P.umber} />
    <path d="M-26,4 Q0,-10 26,-4" stroke={P.paper} strokeWidth={4} fill="none" />
    <rect x={28} y={-150} width={7} height={150} fill={P.payne} />
  </g>
);
const Staff: React.FC<{ y: number; at?: number }> = ({ y, at = 0 }) => {
  const fr = useCurrentFrame();
  const notes = [[220, 3], [340, 2], [460, 4], [580, 1], [700, 3], [820, 2]];
  return (
    <g>
      {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={80} y={y + i * 40} width={920 * ramp(fr, at, at + 18)} height={5} fill={P.payne} opacity={0.8} />)}
      {notes.map(([x, l], i) => <BeanNote key={i} x={x} y={y + l * 40} p={ramp(fr, at + 12 + i * 5, at + 22 + i * 5)} />)}
    </g>
  );
};

const Hook: React.FC = () => (
  <AbsoluteFill>
    <Ground id="bh" />
    <Svg><Staff y={900} /></Svg>
    <Block top={240}><T size={230} color={P.payne} weight={900}>Bach</T></Block>
    <Block at={14} top={1300}><T size={60} color={P.payne} weight={600}>viết vở hài về một cô gái nghiện cà phê</T></Block>
  </AbsoluteFill>
);

const Leipzig: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="bl" field={P.payne} ox={1080} oy={0} seed={12} />
      <Svg>
        <Wash id="blcup" seed={111} color={P.umber} cx={540} cy={1100} r={230} p={ramp(fr, 10, 30)} body={0.9} rim={0.5} distort={18} />
        <Wash id="blrim" seed={112} color={P.paper} cx={540} cy={1100} r={300} p={ramp(fr, 4, 20)} body={0.25} rim={0.9} distort={18} />
      </Svg>
      <Block top={240}><T size={92} color={P.paper}>Leipzig, khoảng 1734</T><T size={60} color={P.paper} weight={600} style={{ marginTop: 14 }}>quán cà phê Zimmermann, nơi Bach thường chỉ huy nhạc</T></Block>
    </AbsoluteFill>
  );
};

// two original painted figures: a tall hat (the father), a wide skirt (the daughter)
const FATHER = "M-70,-330 L70,-330 L70,-250 L110,-250 L110,-230 L60,-230 Q120,-150 110,60 L90,330 L-90,330 L-110,60 Q-120,-150 -60,-230 L-110,-230 L-110,-250 L-70,-250 Z";
const DAUGHTER = "M0,-300 a62,62 0 1 1 0.1,0 Z M-60,-160 L60,-160 L190,330 L-190,330 Z";
const Cast: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="bc" />
      <Svg>
        <g transform="translate(300 1080)"><Painted id="fa" d={FATHER} color={P.greyblue} seed={121} p={ramp(fr, 0, 14)} body={0.8} /></g>
        <g transform="translate(780 1100)"><Painted id="da" d={DAUGHTER} color={P.crimson} seed={122} p={ramp(fr, 10, 24)} body={0.75} /></g>
      </Svg>
      <Block at={4} top={1480} left={120} width={400}><T size={60} color={P.payne}>bố Schlendrian</T></Block>
      <Block at={14} top={1480} left={600} width={420}><T size={60} color={P.crimson}>con gái Lieschen</T></Block>
      <Block top={240}><T size={92} color={P.payne}>Bố cấm cà phê.</T></Block>
    </AbsoluteFill>
  );
};

const Argue: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="ba" field={P.hansa} ox={540} oy={960} seed={7} />
      <Svg>{[0, 1, 2].map((i) => <Wash key={i} id={`bcup${i}`} seed={130 + i} color={P.umber} cx={260 + i * 280} cy={1000} r={110} p={ramp(fr, 8 + i * 8, 26 + i * 8)} body={0.9} rim={0.5} distort={14} />)}</Svg>
      <Block top={300}><T size={200} color={P.payne} weight={900}>3 tách</T><T size={60} color={P.payne} weight={600}>mỗi ngày, không thì…</T></Block>
      <Block at={50} top={1300}><T size={92} color={P.payne}>héo như thịt dê nướng</T></Block>
    </AbsoluteFill>
  );
};

const Threat: React.FC = () => (
  <AbsoluteFill>
    <Ground id="bt" field={P.crimson} ox={0} oy={960} seed={15} />
    <Block top={640}><T size={92} color={P.paper}>Còn uống thì</T><T size={150} color={P.paper} weight={900}>đừng hòng lấy chồng.</T></Block>
  </AbsoluteFill>
);

const Twist: React.FC = () => {
  const fr = useCurrentFrame();
  const write = interpolate(fr, [40, 80], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Ground id="bw" />
      <Svg>
        <Painted id="scroll" d="M180,600 L900,600 L900,1400 L180,1400 Z" color={P.hansa} seed={141} body={0.35} p={ramp(fr, 0, 12)} />
        {[0, 1, 2, 3].map((i) => <rect key={i} x={250} y={700 + i * 90} width={560 * ramp(fr, 6 + i * 4, 18 + i * 4)} height={14} fill={P.greyblue} opacity={0.6} />)}
      </Svg>
      <Block top={240}><T size={92} color={P.payne}>Cú lừa trong hôn ước</T></Block>
      <Block at={40} top={1090} left={250} width={640}>
        <div style={{ overflow: "hidden", width: `${write * 100}%`, whiteSpace: "nowrap" }}><T size={60} color={P.crimson} weight={900}>+ được uống cà phê</T></div>
      </Block>
      <Block at={10} top={1480}><T size={42} color={P.payne} weight={600}>chi tiết Bach thêm vào bản của mình</T></Block>
    </AbsoluteFill>
  );
};

const Moral: React.FC = () => (
  <AbsoluteFill>
    <Ground id="bm" field={P.sap} ox={540} oy={1920} seed={5} />
    <Block top={560}><T size={92} color={P.paper}>Mèo không bỏ được chuột,</T><T size={92} color={P.hansa} style={{ marginTop: 20 }}>con gái không bỏ được cà phê.</T></Block>
  </AbsoluteFill>
);

const Take: React.FC = () => (
  <AbsoluteFill>
    <Ground id="bk" />
    <Svg><Staff y={1150} at={0} /></Svg>
    <Block top={300}><T size={200} color={P.payne} weight={900}>~300 năm</T><T size={60} color={P.payne} weight={600}>phụ huynh bảo bớt cà phê, con thì không</T></Block>
  </AbsoluteFill>
);

const Question: React.FC<{ endAt: number }> = ({ endAt }) => {
  const fr = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Ground id="bq" field={P.payne} ox={540} oy={1920} seed={12} />
      {fr < endAt ? (
        <Block at={6} top={640}><T size={92} color={P.paper}>Bố mẹ từng cấm bạn uống cà phê chưa?</T><T size={60} color={P.hansa} weight={600} style={{ marginTop: 20 }}>Comment có hoặc chưa.</T></Block>
      ) : (
        <Block at={endAt} top={760}><T size={92} color={P.paper}>Cả vở kết luận:</T><T size={150} color={P.hansa} weight={900}>uống cà phê là chuyện tự nhiên.</T></Block>
      )}
    </AbsoluteFill>
  );
};

export const BachFilm: React.FC<FilmProps> = (props) => {
  const b = props.beats;
  return (
    <Film props={props} scenes={[
      { from: 0, to: b.leipzig, el: <Hook /> },
      { from: b.leipzig, to: b.cast, el: <Leipzig /> },
      { from: b.cast, to: b.argue, el: <Cast /> },
      { from: b.argue, to: b.threat, el: <Argue /> },
      { from: b.threat, to: b.twist, el: <Threat /> },
      { from: b.twist, to: b.moral, el: <Twist /> },
      { from: b.moral, to: b.take, el: <Moral /> },
      { from: b.take, to: b.question, el: <Take /> },
      { from: b.question, to: props.duration, el: <Question endAt={f(props.duration - 2.6 - b.question)} /> },
    ]} />
  );
};
