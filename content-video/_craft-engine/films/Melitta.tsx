import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { B, Blob, clamp, CraftFilm, CraftProps, EndCard, f, Ink, Page, ramp, Show, Svg, Txt } from "../kit";

// round paper disc with a crimped edge
const disc = (cx: number, cy: number, r: number) => {
  const pts = Array.from({ length: 49 }, (_, i) => { const t = (i / 48) * Math.PI * 2; const rr = r + (i % 2 ? 10 : -6); return `${cx + Math.cos(t) * rr},${cy + Math.sin(t) * rr}`; });
  return `M${pts.join(" L")} Z`;
};

const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="mh" cx={540} cy={1040} r={420} p={ramp(fr, 0, 14)} seed={5} />
        <Ink d={disc(540, 1040, 240)} p={ramp(fr, 4, 30)} fill="#FFFDF8" />
        <Ink d="M540,1040 m-40,0 a40,40 0 1,0 80,0 a40,40 0 1,0 -80,0" p={ramp(fr, 20, 34)} w={8} />
      </Svg>
      <Show top={250}><Txt size={96}>giấy lọc đầu tiên</Txt><Txt size={64} color={B.coffee}>không phải hình nón</Txt></Show>
      <Show at={40} top={1400}><Txt size={64}>một tờ tròn, nằm phẳng dưới đáy</Txt></Show>
    </Page>
  );
};

const Dresden: React.FC = () => {
  const fr = useCurrentFrame();
  const specks = Array.from({ length: 18 }, (_, i) => ({ x: 380 + ((i * 97) % 320), y: 1000 + ((i * 53) % 120) }));
  return (
    <Page>
      <Svg>
        <Blob id="md" cx={540} cy={1060} r={400} p={ramp(fr, 0, 14)} seed={9} />
        <Ink d="M330,960 C330,1160 420,1260 540,1260 C660,1260 750,1160 750,960 Z" p={ramp(fr, 4, 26)} fill={B.espresso} />
        {specks.map((s, i) => <circle key={i} cx={s.x} cy={s.y} r={10 * ramp(fr, 30 + i, 40 + i)} fill={B.crema} />)}
      </Svg>
      <Show top={250}><Txt size={110}>Dresden, 1908</Txt><Txt size={60} color={B.coffee}>bà Melitta Bentz chán cà phê lợn cợn bã</Txt></Show>
    </Page>
  );
};

const POT = "M260,900 L820,900 L780,1240 L300,1240 Z";
const Pot: React.FC<{ paperAt: number }> = ({ paperAt }) => {
  const fr = useCurrentFrame();
  const holes = [-180, -110, -40, 30, 100, 170];
  const drop = interpolate(fr - paperAt, [0, 18], [-600, 0], clamp);
  return (
    <Page>
      <Svg>
        <Blob id="mp" cx={540} cy={1080} r={420} p={ramp(fr, 0, 14)} seed={12} />
        <Ink d={POT} p={ramp(fr, 2, 22)} fill={B.crema} />
        {holes.map((x, i) => <circle key={i} cx={540 + x} cy={1210} r={12 * ramp(fr, 14 + i * 5, 18 + i * 5)} fill={B.ink} />)}
        {fr >= paperAt ? (
          <g transform={`translate(0 ${drop})`}>
            <Ink d="M300,960 L780,960 L780,1100 L300,1100 Z" p={1} w={8} fill="#FFFDF8" />
            {[0, 1, 2].map((i) => <line key={i} x1={320} x2={760} y1={995 + i * 34} y2={995 + i * 34} stroke={B.earthBlue} strokeOpacity={0.5} strokeWidth={4} />)}
          </g>
        ) : null}
      </Svg>
      <Show top={250}><Txt size={92}>nồi đồng thau + đinh</Txt></Show>
      <Show at={paperAt} top={1340}><Txt size={64} color={B.coffee}>+ giấy thấm xé từ vở của con trai</Txt></Show>
    </Page>
  );
};

const DateScene: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="mdt" cx={540} cy={1000} r={400} p={ramp(fr, 0, 14)} seed={15} />
        <Ink d="M250,700 L830,700 L830,1320 L250,1320 Z" p={ramp(fr, 2, 22)} fill={B.cream} />
        <circle cx={720} cy={1220} r={60 * ramp(fr, 40, 54)} fill={B.earthBlue} filter="url(#hand)" />
      </Svg>
      <Show at={14} top={820} left={300} width={500}><Txt size={110}>20.6.1908</Txt><Txt size={52} color={B.coffee}>đăng ký bảo hộ với cơ quan sáng chế Đức</Txt></Show>
    </Page>
  );
};

const Capital: React.FC = () => {
  const fr = useCurrentFrame();
  const n = Math.round(interpolate(fr, [4, 34], [0, 72], clamp));
  return (
    <Page>
      <Svg>
        <Blob id="mc" cx={760} cy={1150} r={260} p={ramp(fr, 0, 14)} seed={18} />
        {[0, 1, 2].map((i) => <Ink key={i} d={`M${700 + i * 60},${1180 - i * 40} m-80,0 a80,80 0 1,0 160,0 a80,80 0 1,0 -160,0`} p={ramp(fr, 8 + i * 6, 24 + i * 6)} w={10} fill={B.crema} />)}
      </Svg>
      <Show top={620}><Txt size={200}>{n} xu</Txt><Txt size={60} color={B.coffee}>vốn ban đầu của công ty</Txt></Show>
    </Page>
  );
};

// three filters, three eras
const Evolution: React.FC<{ coneAt: number }> = ({ coneAt }) => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="me" cx={540} cy={1060} r={470} p={ramp(fr, 0, 14)} seed={21} />
        <Ink d={disc(230, 1060, 110)} p={ramp(fr, 4, 20)} fill="#FFFDF8" />
        <Ink d="M440,980 L640,980 L600,1160 L480,1160 Z" p={ramp(fr, 20, 40)} fill="#FFFDF8" />
        <Ink d="M730,960 L960,960 L860,1200 L830,1200 Z" p={ramp(fr, coneAt, coneAt + 20)} fill="#FFFDF8" />
      </Svg>
      <Show at={4} top={1260} left={150} width={200}><Txt size={52}>1908</Txt></Show>
      <Show at={20} top={1260} left={420} width={260}><Txt size={52}>đầu 1930s</Txt></Show>
      <Show at={coneAt} top={1260} left={730} width={300}><Txt size={52} color={B.earthBlue}>~1936–37</Txt></Show>
      <Show top={250}><Txt size={92}>từ đáy phẳng</Txt><Txt size={92}>tới hình nón</Txt></Show>
    </Page>
  );
};

const Years: React.FC = () => (
  <Page>
    <Svg><Blob id="my" cx={540} cy={900} r={360} p={1} seed={24} /></Svg>
    <Show top={640}><Txt size={200}>~30 năm</Txt><Txt size={64} color={B.coffee}>tranh luận đáy phẳng hay hình nón</Txt><Txt size={64} color={B.earthBlue}>có gốc từ rất sớm</Txt></Show>
  </Page>
);

const Take: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="mt" cx={540} cy={1100} r={400} p={1} seed={27} />
        <Ink d="M560,660 L860,660 L880,860 L540,860 Z M560,700 C460,680 420,740 380,800" p={ramp(fr, 0, 20)} fill={B.cream} />
        <Ink d="M380,800 C372,880 372,940 374,1000" p={ramp(fr, 18, 30)} w={8} color={B.earthBlue} />
        <Ink d="M200,980 L560,980 L410,1280 L350,1280 Z" p={ramp(fr, 6, 24)} fill="#FFFDF8" />
      </Svg>
      <Show top={250}><Txt size={92}>tráng giấy trước khi pha</Txt><Txt size={60} color={B.coffee}>chăm một phát minh hơn trăm tuổi</Txt></Show>
    </Page>
  );
};

export const MelittaCraft: React.FC<CraftProps> = (props) => {
  const b = props.beats;
  return (
    <CraftFilm props={props} scenes={[
      [0, b.dresden, <Hook />],
      [b.dresden, b.pot, <Dresden />],
      [b.pot, b.date, <Pot paperAt={f(b.paper - b.pot)} />],
      [b.date, b.capital, <DateScene />],
      [b.capital, b.taper, <Capital />],
      [b.taper, b.years, <Evolution coneAt={f(b.cone - b.taper)} />],
      [b.years, b.take, <Years />],
      [b.take, b.question, <Take />],
      [b.question, props.duration, <EndCard at={f(props.duration - 2.8 - b.question)} question="Team đáy phẳng hay hình nón?" answer="comment một chữ" />],
    ]} />
  );
};
