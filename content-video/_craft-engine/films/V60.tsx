import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { B, Blob, clamp, CraftFilm, CraftProps, EndCard, f, Ink, Page, ramp, Show, Svg, Txt, Wash } from "../kit";

const DRIPPER = "M300,820 L780,820 L590,1200 L490,1200 Z";
const FUNNEL = "M640,880 L940,880 L820,1060 L820,1200 L760,1200 L760,1060 Z";
const FLASK = "M500,1000 L580,1000 L580,1130 L700,1360 L380,1360 L500,1130 Z";

const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="vh" cx={540} cy={1040} r={440} p={ramp(fr, 0, 14)} seed={5} />
        <g transform="translate(-120 0)"><Ink d={DRIPPER} p={ramp(fr, 2, 24)} fill={B.cream} /></g>
        <Ink d={FUNNEL} p={ramp(fr, 14, 36)} fill={B.cream} />
      </Svg>
      <Show top={250}><Txt size={200}>V60</Txt></Show>
      <Show at={30} top={1330}><Txt size={64} color={B.coffee}>tổ tiên: một cái phễu phòng lab</Txt></Show>
    </Page>
  );
};

const Lab: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="vl" cx={540} cy={1080} r={420} p={ramp(fr, 0, 14)} seed={9} />
        <Ink d="M180,820 L380,820 L380,1220 L180,1220 Z" p={ramp(fr, 4, 22)} fill={B.cream} />
        <g transform="translate(40 -140)"><Ink d={FLASK} p={ramp(fr, 10, 30)} fill={B.cream} /></g>
        <g transform="translate(-60 20)"><Ink d={FUNNEL} p={ramp(fr, 16, 36)} fill={B.cream} /></g>
        <Ink d="M120,1240 L960,1240" p={ramp(fr, 0, 16)} w={14} />
      </Svg>
      <Show top={250}><Txt size={170}>1921</Txt><Txt size={60} color={B.coffee}>Hario, Tokyo · đồ thủy tinh cho phòng lab</Txt></Show>
    </Page>
  );
};

const sector = (r: number, span: number) => `M0,0 L${r},0 A${r},${r} 0 ${span > Math.PI ? 1 : 0} 1 ${r * Math.cos(span)},${r * Math.sin(span)} Z`;
const Erlen: React.FC = () => {
  const fr = useCurrentFrame();
  const k = interpolate(fr, [20, 34, 44, 58], [0, 1, 1, 2], clamp);
  const span = k <= 1 ? 2 * Math.PI - k * Math.PI : Math.PI - (k - 1) * (Math.PI / 2);
  return (
    <Page>
      <Svg>
        <Blob id="ve" cx={540} cy={1060} r={420} p={ramp(fr, 0, 14)} seed={12} />
        <g transform="translate(-260 -10)"><Ink d={FUNNEL} p={ramp(fr, 0, 18)} fill={B.cream} /></g>
        <g transform="translate(-260 -130)"><Ink d={FLASK} p={ramp(fr, 6, 24)} fill={B.cream} /></g>
        <g transform="translate(760 1000) rotate(-60)" opacity={ramp(fr, 14, 22)}>
          <path d={sector(150, span - 0.001)} fill="#FFFDF8" stroke={B.ink} strokeWidth={10} strokeLinejoin="round" filter="url(#hand)" />
        </g>
      </Svg>
      <Show top={250}><Txt size={96}>phễu Erlenmeyer</Txt><Txt size={60} color={B.coffee}>+ giấy lọc gấp tư · theo lời Hario</Txt></Show>
    </Page>
  );
};

const Cone: React.FC = () => {
  const fr = useCurrentFrame();
  const bed = ramp(fr, 40, 80);
  return (
    <Page>
      <Svg>
        <Blob id="vc1" cx={290} cy={1060} r={240} p={ramp(fr, 0, 14)} seed={15} />
        <Blob id="vc2" cx={790} cy={1060} r={240} p={ramp(fr, 6, 20)} seed={16} />
        {/* flat bottom: shallow bed */}
        <clipPath id="fb"><path d="M120,860 L460,860 L400,1220 L180,1220 Z" /></clipPath>
        <rect clipPath="url(#fb)" x={100} y={1220 - 110 * bed} width={400} height={110 * bed} fill={B.coffee} />
        <Ink d="M120,860 L460,860 L400,1220 L180,1220 Z" p={ramp(fr, 4, 24)} />
        {/* cone: deeper bed */}
        <clipPath id="cn"><path d="M600,860 L980,860 L800,1260 Z" /></clipPath>
        <rect clipPath="url(#cn)" x={590} y={1260 - 230 * bed} width={400} height={230 * bed} fill={B.coffee} />
        <Ink d="M600,860 L980,860 L800,1260 Z" p={ramp(fr, 10, 30)} />
        {[-120, 0, 120].map((dx, i) => <Ink key={i} d={`M${790 + dx},760 L${790 + dx * 0.2},960`} p={ramp(fr, 90 + i * 6, 110 + i * 6)} w={10} color={B.earthBlue} />)}
      </Svg>
      <Show at={10} top={1300} left={150} width={340}><Txt size={54}>đáy phẳng</Txt></Show>
      <Show at={16} top={1300} left={680} width={340}><Txt size={54}>hình nón</Txt></Show>
      <Show top={250}><Txt size={92}>nước dồn về tâm</Txt><Txt size={60} color={B.coffee}>lớp bột dày hơn, tiếp xúc lâu hơn</Txt></Show>
    </Page>
  );
};

const Years: React.FC<{ at2005: number }> = ({ at2005 }) => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg><Blob id="vy" cx={540} cy={980} r={380} p={ramp(fr, 0, 14)} seed={18} /><Ink d="M300,980 C450,900 620,1060 780,980 M740,940 L790,980 L740,1020" p={ramp(fr, 10, at2005)} w={14} /></Svg>
      <Show top={760}><Txt size={140}>1980</Txt><Txt size={54} color={B.coffee}>phễu nón đầu tiên</Txt></Show>
      <Show at={at2005} top={1100} left={560} width={480}><Txt size={140} color={B.earthBlue}>2005</Txt><Txt size={54} color={B.coffee}>V60 thành hình</Txt></Show>
    </Page>
  );
};

const Anatomy: React.FC<{ ribsAt: number; holeAt: number }> = ({ ribsAt, holeAt }) => {
  const fr = useCurrentFrame();
  const ax = 540, ay = 1360, h = 640, dx = h * Math.tan(Math.PI / 6);
  return (
    <Page>
      <Svg>
        <Blob id="va" cx={540} cy={1050} r={460} p={ramp(fr, 0, 14)} seed={21} />
        <Ink d={`M${ax - dx},${ay - h} L${ax},${ay} L${ax + dx},${ay - h}`} p={ramp(fr, 2, 24)} w={18} />
        <Ink d={`M${ax - 95},${ay - 165} A190,190 0 0 1 ${ax + 95},${ay - 165}`} p={ramp(fr, 20, 36)} w={10} color={B.earthBlue} />
        {[-0.6, -0.25, 0.1, 0.45].map((o, i) => <Ink key={i} d={`M${ax + o * dx},${ay - h + 30} Q${ax + o * dx + 90},${ay - h / 2} ${ax + o * 20},${ay - 60}`} p={ramp(fr, ribsAt + i * 4, ribsAt + 20 + i * 4)} w={8} color={B.coffee} />)}
        {fr >= holeAt ? <circle cx={ax} cy={ay - 14} r={14 + ramp(fr, holeAt, holeAt + 12) * 30} fill={B.ink} /> : null}
      </Svg>
      <Show top={250}><Txt size={110}>60°</Txt></Show>
      <Show at={ribsAt} top={420}><Txt size={58} color={B.coffee}>gân xoắn tới miệng phễu: khí thoát khi bột nở</Txt></Show>
      <Show at={holeAt} top={1440}><Txt size={80}>một lỗ, rất to</Txt></Show>
    </Page>
  );
};

const Flow: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="vf" cx={540} cy={1100} r={420} p={ramp(fr, 0, 14)} seed={24} />
        {/* kettle */}
        <Ink d="M560,620 L860,620 L880,820 L540,820 Z M560,660 C460,640 420,700 380,760" p={ramp(fr, 2, 22)} fill={B.cream} />
        <Ink d="M380,760 C370,860 370,930 372,980" p={ramp(fr, 20, 34)} w={8} color={B.earthBlue} />
        <Ink d="M200,960 L560,960 L410,1260 L350,1260 Z" p={ramp(fr, 6, 26)} fill={B.cream} />
        <Ink d="M380,1260 L380,1400" p={ramp(fr, 36, 50)} w={14} color={B.coffee} />
      </Svg>
      <Show top={250}><Txt size={92}>phễu không hãm dòng</Txt></Show>
      <Show at={40} top={1000} left={600} width={440}><Txt size={64}>tốc độ =</Txt><Txt size={64} color={B.earthBlue}>cỡ xay</Txt><Txt size={64} color={B.earthBlue}>+ cách rót</Txt></Show>
    </Page>
  );
};

const Tip: React.FC = () => {
  const fr = useCurrentFrame();
  const a = interpolate(fr, [30, 70], [0, -50], clamp);
  return (
    <Page>
      <Svg>
        <Blob id="vt" cx={540} cy={1060} r={400} p={1} seed={27} />
        <Ink d="M540,1060 m-230,0 a230,230 0 1,0 460,0 a230,230 0 1,0 -460,0" p={ramp(fr, 0, 20)} fill={B.cream} />
        {Array.from({ length: 12 }, (_, i) => { const t = (i / 12) * Math.PI * 2; return <Ink key={i} d={`M${540 + Math.cos(t) * 190},${1060 + Math.sin(t) * 190} L${540 + Math.cos(t) * 225},${1060 + Math.sin(t) * 225}`} p={ramp(fr, 8, 20)} w={8} />; })}
        <g transform={`rotate(${a} 540 1060)`}><Ink d="M540,1060 L540,880" p={ramp(fr, 14, 26)} w={16} color={B.earthBlue} /></g>
      </Svg>
      <Show top={250}><Txt size={92}>nước rút quá nhanh?</Txt><Txt size={64} color={B.coffee}>chỉnh cỡ xay trước, đừng vội đổ lỗi cho giấy</Txt></Show>
      <Show at={60} top={1360}><Txt size={64} color={B.earthBlue}>→ xay mịn hơn</Txt></Show>
    </Page>
  );
};

export const V60Craft: React.FC<CraftProps> = (props) => {
  const b = props.beats;
  return (
    <CraftFilm props={props} scenes={[
      [0, b.lab, <Hook />],
      [b.lab, b.erlen, <Lab />],
      [b.erlen, b.cone, <Erlen />],
      [b.cone, b.y1980, <Cone />],
      [b.y1980, b.ribs - 0.6, <Years at2005={f(b.y2005 - b.y1980)} />],
      [b.ribs - 0.6, b.flow, <Anatomy ribsAt={f(0.6)} holeAt={f(b.hole - b.ribs + 0.6)} />],
      [b.flow, b.tip, <Flow />],
      [b.tip, b.question, <Tip />],
      [b.question, props.duration, <EndCard at={f(props.duration - 2.8 - b.question)} question="Chỉnh cỡ xay hay cách rót trước?" answer="comment một chữ" />],
    ]} />
  );
};
