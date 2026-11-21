import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { B, Blob, clamp, CraftFilm, CraftProps, EndCard, f, Globe, Ink, Page, ramp, Show, Svg, Txt } from "../kit";

const KETTLE = "M380,900 Q370,780 540,770 Q710,780 700,900 L740,1240 L340,1240 Z M700,980 Q840,930 870,800";

const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="sh" cx={540} cy={1030} r={420} p={ramp(fr, 0, 14)} seed={5} />
        <Ink d={KETTLE} p={ramp(fr, 2, 28)} fill={B.cream} />
        <Ink d="M360,1060 L720,1060" p={ramp(fr, 26, 40)} w={46} />
        <Ink d="M540,1060 L500,1160 M540,1060 L580,1160" p={ramp(fr, 36, 46)} w={14} />
      </Svg>
      <Show top={250}><Txt size={120}>1.8.1794</Txt><Txt size={60} color={B.coffee}>đám tang cho bình pha cà phê</Txt></Show>
    </Page>
  );
};

const PERIODS: [number, number][] = [[1756, 1761], [1766, 1769], [1794, 1796], [1799, 1802], [1817, 1823]];
const Bans: React.FC = () => {
  const fr = useCurrentFrame();
  const x = (y: number) => 110 + ((y - 1750) / 80) * 860;
  return (
    <Page>
      <Svg>
        <Blob id="sb" cx={540} cy={1020} r={480} p={ramp(fr, 0, 14)} seed={9} />
        <Ink d="M110,1020 L970,1020" p={ramp(fr, 0, 20)} w={10} />
        {PERIODS.map(([a, b], i) => <rect key={i} x={x(a)} y={960} width={Math.max(26, x(b) - x(a))} height={120} rx={14} fill={B.earthBlue} opacity={ramp(fr, 20 + i * 12, 32 + i * 12)} filter="url(#hand)" />)}
      </Svg>
      {PERIODS.map(([a], i) => (
        <div key={i} style={{ position: "absolute", left: x(a) - 40, top: i % 2 ? 1110 : 860, opacity: ramp(fr, 26 + i * 12, 36 + i * 12) }}>
          <Txt size={46}>{a}</Txt>
        </div>
      ))}
      <Show top={250}><Txt size={150}>5 lần cấm</Txt><Txt size={60} color={B.coffee}>1756–1823 · ba đời vua</Txt></Show>
    </Page>
  );
};

const Why: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="sw" cx={540} cy={1040} r={460} p={ramp(fr, 0, 14)} seed={12} />
        <Globe id="swg" cx={540} cy={1040} r={330} lon={15} lat={55} />
        {[0, 1, 2, 3].map((i) => { const p = ramp(fr, 30 + i * 12, 60 + i * 12); return <Ink key={i} d={`M${640 + p * 240},${800 + i * 34} m-40,0 a40,40 0 1,0 80,0 a40,40 0 1,0 -80,0`} p={p > 0 ? 1 : 0} w={8} fill={B.crema} />; })}
        <Ink d="M600,740 C720,690 820,700 900,750 M860,712 L905,752 L850,770" p={ramp(fr, 20, 40)} w={12} color={B.earthBlue} />
      </Svg>
      <Show top={250}><Txt size={92}>lý do rất kinh tế</Txt><Txt size={60} color={B.coffee}>hạt nhập khẩu, tiền chảy ra nước ngoài</Txt></Show>
      <Show at={90} top={1450}><Txt size={60}>+ giới cầm quyền tin nó có hại</Txt></Show>
    </Page>
  );
};

const Sneak: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="ss" cx={540} cy={1060} r={420} p={ramp(fr, 0, 14)} seed={15} />
        <Ink d="M240,760 L760,760 L760,1360 L240,1360 Z" p={ramp(fr, 4, 24)} fill={B.cream} />
        {[0, 1, 2, 3].map((i) => <Ink key={i} d={`M300,${860 + i * 80} L${680 - (i % 2) * 100},${860 + i * 80}`} p={ramp(fr, 14 + i * 4, 26 + i * 4)} w={6} />)}
        <circle cx={660} cy={1250} r={56 * ramp(fr, 40, 54)} fill={B.earthBlue} filter="url(#hand)" />
      </Svg>
      <Show top={250}><Txt size={92}>người ta uống lén</Txt></Show>
      <Show at={30} top={1420}><Txt size={60} color={B.coffee}>hồ sơ cảnh sát Stockholm còn lưu lại</Txt></Show>
    </Page>
  );
};

const Twins: React.FC = () => {
  const fr = useCurrentFrame();
  const cup = (cx: number, fill: string, at: number) => <Ink d={`M${cx - 120},1080 C${cx - 120},1240 ${cx - 60},1290 ${cx},1290 C${cx + 60},1290 ${cx + 120},1240 ${cx + 120},1080 Z`} p={ramp(fr, at, at + 20)} fill={fill} />;
  return (
    <Page>
      <Svg>
        <Blob id="st" cx={540} cy={1140} r={420} p={ramp(fr, 0, 14)} seed={18} />
        {cup(330, B.espresso, 30)}
        {cup(750, B.earthGreen, 44)}
      </Svg>
      <Show top={250}><Txt size={120} color={B.earthBlue}>giai thoại</Txt><Txt size={60} color={B.coffee}>Gustav III và hai anh em sinh đôi</Txt></Show>
      <Show at={30} top={1340} left={230} width={300}><Txt size={56}>cà phê</Txt></Show>
      <Show at={44} top={1340} left={690} width={300}><Txt size={56}>trà</Txt></Show>
    </Page>
  );
};

const Doctors: React.FC = () => (
  <Page>
    <Svg><Blob id="sd" cx={540} cy={1000} r={380} p={1} seed={21} /></Svg>
    <Show top={300}><Txt size={92}>ai chết trước?</Txt></Show>
    <Show at={6} top={800}><Txt size={70}>1. bác sĩ giám sát</Txt></Show>
    <Show at={30} top={940}><Txt size={70}>2. nhà vua (bị ám sát, 1792)</Txt></Show>
  </Page>
);

const Myth: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Show top={640}><Txt size={80}>nhiều nhà sử học:</Txt></Show>
      <div style={{ position: "absolute", left: 150, top: 820, transform: `rotate(-6deg) scale(${1.6 - 0.6 * ramp(fr, 10, 24)})`, opacity: ramp(fr, 10, 20), border: `10px solid ${B.earthBlue}`, borderRadius: 20, padding: "10px 40px" }}>
        <Txt size={110} color={B.earthBlue}>có thể là bịa</Txt>
      </div>
    </Page>
  );
};

const Fika: React.FC<{ fikaAt: number }> = ({ fikaAt }) => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="sf" cx={540} cy={1160} r={420} p={ramp(fr, 0, 14)} seed={24} />
        <Ink d="M300,1100 C300,1260 360,1310 420,1310 C480,1310 540,1260 540,1100 Z" p={ramp(fr, fikaAt, fikaAt + 20)} fill={B.espresso} />
        {/* cinnamon bun */}
        <Ink d="M760,1210 m-150,0 a150,110 0 1,0 300,0 a150,110 0 1,0 -300,0" p={ramp(fr, fikaAt + 10, fikaAt + 30)} fill={B.crema} />
        <Ink d="M760,1210 c40,0 50,40 0,50 c-70,10 -90,-60 -20,-80 c90,-20 140,70 60,110" p={ramp(fr, fikaAt + 24, fikaAt + 44)} w={10} color={B.coffee} />
      </Svg>
      <Show top={250}><Txt size={120}>1823</Txt><Txt size={60} color={B.coffee}>lệnh cấm chấm dứt</Txt></Show>
      <Show at={fikaAt} top={600}><Txt size={200} color={B.earthBlue}>fika</Txt></Show>
    </Page>
  );
};

export const SwedenCraft: React.FC<CraftProps> = (props) => {
  const b = props.beats;
  return (
    <CraftFilm props={props} scenes={[
      [0, b.law, <Hook />],
      [b.law, b.why, <Bans />],
      [b.why, b.sneak, <Why />],
      [b.sneak, b.twins, <Sneak />],
      [b.twins, b.doctors, <Twins />],
      [b.doctors, b.myth, <Doctors />],
      [b.myth, b.end, <Myth />],
      [b.end, b.question, <Fika fikaAt={f(b.fika - b.end) - 18} />],
      [b.question, props.duration, <EndCard at={f(props.duration - 2.8 - b.question)} question="Việt Nam cấm cà phê một tuần, bạn trụ nổi không?" answer="comment có hoặc không" />],
    ]} />
  );
};
