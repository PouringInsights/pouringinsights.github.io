import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { B, Blob, clamp, CraftFilm, CraftProps, EndCard, f, Ink, Page, ramp, Show, Svg, Txt } from "../kit";

// staff with coffee-bean notes
const Staff: React.FC<{ y: number; at?: number }> = ({ y, at = 0 }) => {
  const fr = useCurrentFrame();
  const notes = [[230, 3], [350, 2], [470, 4], [590, 1], [710, 3], [830, 2]];
  return (
    <g>
      {[0, 1, 2, 3, 4].map((i) => <Ink key={i} d={`M100,${y + i * 38} L980,${y + i * 38}`} p={ramp(fr, at, at + 18)} w={6} />)}
      {notes.map(([x, l], i) => {
        const p = ramp(fr, at + 12 + i * 5, at + 22 + i * 5);
        return (
          <g key={i} transform={`translate(${x} ${y + l * 38}) rotate(-20) scale(${p})`}>
            <ellipse rx={32} ry={22} fill={B.coffee} stroke={B.ink} strokeWidth={6} />
            <path d="M-22,4 Q0,-8 22,-4" stroke={B.cream} strokeWidth={4} fill="none" />
            <rect x={26} y={-140} width={8} height={140} fill={B.ink} />
          </g>
        );
      })}
    </g>
  );
};

const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg><Blob id="bh" cx={540} cy={1000} r={460} p={ramp(fr, 0, 14)} seed={5} /><Staff y={920} /></Svg>
      <Show top={250}><Txt size={92}>quán cà phê Leipzig</Txt><Txt size={92} color={B.earthBlue}>= phòng hòa nhạc</Txt></Show>
      <Show at={40} top={1360}><Txt size={64} color={B.coffee}>người chỉ huy: Bach</Txt></Show>
    </Page>
  );
};

const Collegium: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="bc" cx={540} cy={1080} r={420} p={ramp(fr, 0, 14)} seed={9} />
        {/* music stand */}
        <Ink d="M380,820 L700,820 L680,1020 L400,1020 Z M540,1020 L540,1360 M440,1360 L640,1360" p={ramp(fr, 4, 30)} fill={B.cream} />
        {[0, 1, 2].map((i) => <Ink key={i} d={`M420,${870 + i * 45} L660,${870 + i * 45}`} p={ramp(fr, 24 + i * 4, 34 + i * 4)} w={6} />)}
      </Svg>
      <Show top={250}><Txt size={150}>1729</Txt><Txt size={60} color={B.coffee}>Collegium Musicum · quán Zimmermann</Txt></Show>
    </Page>
  );
};

const Owner: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="bo" cx={540} cy={1060} r={380} p={ramp(fr, 0, 12)} seed={12} />
        <Ink d="M380,960 C380,1140 450,1220 540,1220 C630,1220 700,1140 700,960 Z" p={ramp(fr, 2, 20)} fill={B.espresso} />
        {[0, 1].map((i) => <Ink key={i} d={`M${760 + i * 60},${1160 - i * 30} m-60,0 a60,60 0 1,0 120,0 a60,60 0 1,0 -120,0`} p={ramp(fr, 14 + i * 6, 28 + i * 6)} w={8} fill={B.crema} />)}
      </Svg>
      <Show top={250}><Txt size={92}>chủ quán lời nhờ</Txt><Txt size={92} color={B.earthBlue}>bán cà phê</Txt></Show>
    </Page>
  );
};

const FATHER = "M-70,-330 L70,-330 L70,-250 L110,-250 L110,-230 L60,-230 Q120,-150 110,60 L90,330 L-90,330 L-110,60 Q-120,-150 -60,-230 L-110,-230 L-110,-250 L-70,-250 Z";
const DAUGHTER = "M0,-300 a62,62 0 1 1 0.1,0 Z M-60,-160 L60,-160 L190,330 L-190,330 Z";
const Cantata: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="bn1" cx={300} cy={1080} r={260} p={ramp(fr, 0, 14)} seed={15} />
        <Blob id="bn2" cx={780} cy={1080} r={260} p={ramp(fr, 6, 20)} seed={16} />
        <g transform="translate(300 1080) scale(0.85)"><Ink d={FATHER} p={ramp(fr, 4, 30)} fill={B.cream} /></g>
        <g transform="translate(780 1100) scale(0.85)"><Ink d={DAUGHTER} p={ramp(fr, 14, 40)} fill={B.earthBlue} /></g>
      </Svg>
      <Show top={250}><Txt size={92}>~1734 · lời Picander</Txt><Txt size={60} color={B.coffee}>bố cấm con gái uống cà phê</Txt></Show>
      <Show at={20} top={1420} left={130} width={360}><Txt size={56}>Schlendrian</Txt></Show>
      <Show at={30} top={1420} left={640} width={360}><Txt size={56}>Lieschen</Txt></Show>
    </Page>
  );
};

const Argue: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="ba" cx={540} cy={1040} r={420} p={ramp(fr, 0, 14)} seed={18} />
        {[0, 1, 2].map((i) => <Ink key={i} d={`M${170 + i * 270},960 C${170 + i * 270},1120 ${230 + i * 270},1170 ${270 + i * 270},1170 C${310 + i * 270},1170 ${370 + i * 270},1120 ${370 + i * 270},960 Z`} p={ramp(fr, 6 + i * 8, 24 + i * 8)} fill={B.espresso} />)}
      </Svg>
      <Show top={250}><Txt size={150}>3 tách / ngày</Txt><Txt size={60} color={B.coffee}>không thì…</Txt></Show>
      <Show at={40} top={1300}><Txt size={80}>héo như thịt dê nướng</Txt></Show>
    </Page>
  );
};

const Threat: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="bt" cx={540} cy={1100} r={360} p={ramp(fr, 0, 14)} seed={21} />
        <Ink d="M540,1100 m-150,0 a150,150 0 1,0 300,0 a150,150 0 1,0 -300,0" p={ramp(fr, 4, 24)} w={22} color={B.crema} />
        <Ink d="M360,920 L720,1280" p={ramp(fr, 30, 44)} w={18} color={B.earthBlue} />
      </Svg>
      <Show top={300}><Txt size={92}>còn uống thì</Txt><Txt size={110}>đừng hòng lấy chồng</Txt></Show>
    </Page>
  );
};

const Twist: React.FC = () => {
  const fr = useCurrentFrame();
  const write = interpolate(fr, [30, 70], [0, 1], clamp);
  return (
    <Page>
      <Svg>
        <Blob id="bw" cx={540} cy={1040} r={440} p={ramp(fr, 0, 14)} seed={24} />
        <Ink d="M220,700 L860,700 L860,1380 L220,1380 Z" p={ramp(fr, 2, 22)} fill={B.cream} />
        {[0, 1, 2, 3].map((i) => <Ink key={i} d={`M280,${800 + i * 80} L${780 - (i % 2) * 90},${800 + i * 80}`} p={ramp(fr, 10 + i * 4, 22 + i * 4)} w={6} />)}
      </Svg>
      <Show top={250}><Txt size={92}>cú lừa trong hôn ước</Txt><Txt size={56} color={B.coffee}>chi tiết Bach thêm vào bản của mình</Txt></Show>
      <div style={{ position: "absolute", left: 280, top: 1150, width: 560, overflow: "hidden" }}>
        <div style={{ width: `${write * 100}%`, overflow: "hidden", whiteSpace: "nowrap" }}><Txt size={64} color={B.earthBlue}>+ được uống cà phê</Txt></div>
      </div>
    </Page>
  );
};

const Moral: React.FC = () => (
  <Page>
    <Svg><Blob id="bm" cx={540} cy={960} r={420} p={1} seed={27} /></Svg>
    <Show top={700}><Txt size={92}>mèo không bỏ được chuột,</Txt><Txt size={92} color={B.earthBlue} style={{ marginTop: 20 }}>con gái không bỏ được cà phê</Txt></Show>
  </Page>
);

const Ad: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="bad" cx={540} cy={1150} r={420} p={ramp(fr, 0, 14)} seed={30} />
        <Staff y={760} at={4} />
        {[0, 1, 2].map((i) => <Ink key={i} d={`M${200 + i * 260},1180 C${200 + i * 260},1320 ${250 + i * 260},1360 ${290 + i * 260},1360 C${330 + i * 260},1360 ${380 + i * 260},1320 ${380 + i * 260},1180 Z`} p={ramp(fr, 30 + i * 8, 50 + i * 8)} fill={B.espresso} />)}
      </Svg>
      <Show top={250}><Txt size={84}>khán giả cầm đúng thứ</Txt><Txt size={84}>đang bị đem ra chọc</Txt></Show>
      <Show at={70} top={1460}><Txt size={72} color={B.earthBlue}>một kiểu quảng cáo cho quán?</Txt></Show>
    </Page>
  );
};

export const BachCraft: React.FC<CraftProps> = (props) => {
  const b = props.beats;
  return (
    <CraftFilm props={props} scenes={[
      [0, b.collegium, <Hook />],
      [b.collegium, b.owner, <Collegium />],
      [b.owner, b.cantata, <Owner />],
      [b.cantata, b.argue, <Cantata />],
      [b.argue, b.threat, <Argue />],
      [b.threat, b.twist, <Threat />],
      [b.twist, b.moral, <Twist />],
      [b.moral, b.ad, <Moral />],
      [b.ad, b.question, <Ad />],
      [b.question, props.duration, <EndCard at={f(props.duration - 2.8 - b.question)} question="Bố mẹ từng cấm bạn uống cà phê chưa?" answer="comment có hoặc chưa" />],
    ]} />
  );
};
