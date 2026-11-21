import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { B, Blob, clamp, CraftFilm, CraftProps, EndCard, f, Globe, Ink, Page, ramp, Show, Svg, Txt } from "../kit";

const Hook: React.FC = () => {
  const fr = useCurrentFrame();
  const money = Math.round(interpolate(fr, [6, 46], [120000, 604080], clamp));
  return (
    <Page>
      <Svg>
        <Blob id="gh" cx={540} cy={980} r={430} p={ramp(fr, 0, 16)} seed={5} />
        {/* auction tag */}
        <Ink d="M260,760 L760,760 L860,980 L760,1200 L260,1200 Z" p={ramp(fr, 0, 22)} fill={B.cream} />
        <Ink d="M790,980 m-26,0 a26,26 0 1,0 52,0 a26,26 0 1,0 -52,0" p={ramp(fr, 14, 26)} w={10} />
        <Ink d="M816,980 C900,900 950,860 1000,820" p={ramp(fr, 20, 32)} w={8} />
      </Svg>
      <Show top={810} left={290} width={470}><Txt size={60} color={B.coffee}>20 ký Geisha</Txt><Txt size={100}>${money.toLocaleString("de-DE")}</Txt></Show>
      <Show at={30} top={1260}><Txt size={58} color={B.coffee}>Best of Panama, 2025</Txt></Show>
      <Show at={56} top={260}><Txt size={110}>…và một cái tên viết chệch</Txt></Show>
    </Page>
  );
};

const Origin: React.FC = () => {
  const fr = useCurrentFrame();
  const { fps } = useVideoConfig();
  const r = fr - 16;
  const drop = r > 0 ? Math.min(1, (r / fps) ** 2 * 1.8) : 0;
  const close = interpolate(r, [8, 22], [0, 1], clamp);
  return (
    <Page>
      <Svg>
        <Blob id="go" cx={540} cy={1250} r={330} p={ramp(fr, 0, 14)} seed={9} />
        <g opacity={ramp(fr, 24, 36)}><Globe id="gog" cx={540} cy={1260} r={230} lon={35} lat={-5} /></g>
      </Svg>
      <div style={{ position: "absolute", top: 520, width: "100%", display: "flex", justifyContent: "center", fontFamily: "'Anaktoria', serif", fontSize: 230, color: B.ink }}>
        {"GEISHA".split("").map((l, i) =>
          i === 2 ? <span key={i} style={{ display: "inline-block", width: interpolate(close, [0, 1], [70, 0]), transform: `translateY(${drop * 1200}px) rotate(${drop * 120}deg)`, color: B.earthBlue }}>{l}</span> : <span key={i}>{l}</span>,
        )}
      </div>
      <Show top={250}><Txt size={64} color={B.coffee}>gốc là</Txt></Show>
      <Show at={30} top={390}><Txt size={60}>rừng Gesha, tây nam Ethiopia · 1930s</Txt></Show>
    </Page>
  );
};

const Route: React.FC<{ catieAt: number }> = ({ catieAt }) => {
  const fr = useCurrentFrame();
  const leg1 = ramp(fr, 6, catieAt);
  const leg2 = ramp(fr, catieAt, catieAt + 90);
  const lon = leg2 > 0 ? interpolate(leg2, [0, 1], [37, -60]) : 37;
  const atCatie = fr >= catieAt;
  return (
    <Page>
      <Svg>
        <Blob id="gr" cx={540} cy={1000} r={460} p={ramp(fr, 0, 14)} seed={12} />
        <Globe id="grg" cx={540} cy={1000} r={340} lon={lon} lat={-5} route={atCatie ? [[37.2, -3.2], [-83.6, 9.9]] : [[35.3, 7.1], [37.2, -3.2]]} routeP={atCatie ? leg2 : leg1} />
      </Svg>
      {!atCatie ? (
        <Show top={250}><Txt size={96}>trạm Lyamungu</Txt><Txt size={60} color={B.coffee}>Tanzania</Txt></Show>
      ) : (
        <Show at={catieAt} top={250}><Txt size={96}>1953 · CATIE</Txt><Txt size={60} color={B.coffee}>ngân hàng gen ở Costa Rica</Txt></Show>
      )}
      {atCatie ? (
        <Show at={catieAt + 30} top={1440} left={300} width={500}>
          <div style={{ border: `8px solid ${B.ink}`, borderRadius: 18, padding: "10px 30px", background: B.cream, textAlign: "center" }}><Txt size={96}>T2722</Txt></div>
        </Show>
      ) : null}
    </Page>
  );
};

const Panama: React.FC = () => {
  const fr = useCurrentFrame();
  const years = Math.round(interpolate(fr, [60, 140], [0, 40], clamp));
  const leaves = Array.from({ length: 6 }, (_, i) => i);
  return (
    <Page>
      <Svg>
        <Blob id="gp" cx={420} cy={1050} r={360} p={ramp(fr, 0, 14)} seed={15} />
        <Ink d="M420,1400 C410,1200 430,950 420,700" p={ramp(fr, 4, 30)} />
        {leaves.map((i) => {
          const y = 1300 - i * 100, s = i % 2 ? 1 : -1;
          return <Ink key={i} d={`M420,${y} C${420 + s * 60},${y - 60} ${420 + s * 150},${y - 40} ${420 + s * 170},${y - 10} C${420 + s * 120},${y + 20} ${420 + s * 60},${y + 10} 420,${y}`} p={ramp(fr, 14 + i * 5, 30 + i * 5)} w={10} fill={B.earthGreen} />;
        })}
      </Svg>
      <Show top={250}><Txt size={96}>Boquete, Panama</Txt><Txt size={60} color={B.coffee}>thập niên 60 · năng suất thấp</Txt></Show>
      <Show at={60} top={1000} left={640} width={420}><Txt size={170}>~{years}</Txt><Txt size={60}>năm bị bỏ mặc</Txt></Show>
    </Page>
  );
};

const Esmeralda: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="ge" cx={540} cy={1000} r={400} p={ramp(fr, 0, 14)} seed={18} />
        {/* rosette */}
        <Ink d="M440,1120 L380,1400 L460,1350 L500,1430 L540,1140 M640,1120 L700,1400 L620,1350 L580,1430 L540,1140" p={ramp(fr, 40, 66)} w={12} fill={B.earthBlue} />
        <Ink d="M540,1000 m-170,0 a170,170 0 1,0 340,0 a170,170 0 1,0 -340,0" p={ramp(fr, 20, 50)} fill={B.cream} />
      </Svg>
      <Show top={250}><Txt size={96}>nhà Peterson, La Esmeralda</Txt><Txt size={60} color={B.coffee}>tách riêng lô cây bị bỏ quên</Txt></Show>
      <Show at={44} top={920} left={390} width={300}><Txt size={110} style={{ textAlign: "center" }}>2004</Txt></Show>
      <Show at={70} top={1480}><Txt size={64}>Best of Panama · kỷ lục đấu giá</Txt></Show>
    </Page>
  );
};

// signature for knowledgeable viewers: same name, different DNA
const Genetic: React.FC = () => {
  const fr = useCurrentFrame();
  const ref = [B.coffee, B.earthGreen, B.crema, B.earthBlue, B.coffee, B.crema, B.earthGreen, B.earthBlue, B.coffee, B.crema];
  const other = ref.map((c, i) => ([2, 5, 8].includes(i) ? B.ink : c));
  const Row: React.FC<{ y: number; cols: string[]; at: number }> = ({ y, cols, at }) => (
    <>
      {cols.map((c, i) => <rect key={i} x={120 + i * 84} y={y} width={70} height={150} rx={12} fill={c} opacity={ramp(fr, at + i * 3, at + 10 + i * 3)} filter="url(#hand)" />)}
    </>
  );
  return (
    <Page>
      <Svg>
        <Blob id="gg" cx={540} cy={1000} r={460} p={ramp(fr, 0, 14)} seed={21} />
        <Row y={760} cols={ref} at={20} />
        <Row y={1100} cols={other} at={70} />
        {[2, 5, 8].map((i) => <Ink key={i} d={`M${155 + i * 84},${1270} l0,60`} p={ramp(fr, 130, 150)} w={10} color={B.earthBlue} />)}
      </Svg>
      <Show top={250}><Txt size={92}>World Coffee Research</Txt><Txt size={60} color={B.coffee}>kiểm tra di truyền các cây "Gesha"</Txt></Show>
      <Show at={20} top={680}><Txt size={54}>mẫu T2722</Txt></Show>
      <Show at={70} top={1020}><Txt size={54}>cây cũng gọi là Gesha</Txt></Show>
      <Show at={150} top={1400}><Txt size={96}>cùng tên ≠ cùng cây</Txt></Show>
    </Page>
  );
};

const Take: React.FC = () => {
  const fr = useCurrentFrame();
  return (
    <Page>
      <Svg>
        <Blob id="gt" cx={540} cy={1000} r={420} p={1} seed={24} />
        <Ink d="M220,620 L860,620 L860,1380 L220,1380 Z" p={ramp(fr, 0, 20)} fill={B.cream} />
      </Svg>
      <Show at={6} top={680} left={280} width={540}><Txt size={64} style={{ textAlign: "center" }}>menu</Txt></Show>
      <Show at={14} top={820} left={280} width={540}><Txt size={72}>Geisha ··········· ?</Txt></Show>
      <Show at={40} top={980} left={300} width={540}><Txt size={60} color={B.earthBlue}>vườn nào?</Txt></Show>
      <Show at={60} top={1080} left={300} width={540}><Txt size={60} color={B.earthBlue}>giống từ đâu?</Txt></Show>
    </Page>
  );
};

export const GeishaCraft: React.FC<CraftProps> = (props) => {
  const b = props.beats;
  return (
    <CraftFilm props={props} scenes={[
      [0, b.origin, <Hook />],
      [b.origin, b.route, <Origin />],
      [b.route, b.panama, <Route catieAt={f(b.catie - b.route)} />],
      [b.panama, b.esmeralda, <Panama />],
      [b.esmeralda, b.genetic, <Esmeralda />],
      [b.genetic, b.take, <Genetic />],
      [b.take, b.question, <Take />],
      [b.question, props.duration, <EndCard at={f(props.duration - 2.8 - b.question)} question="Bạn từng uống Gesha chưa?" answer="comment có hoặc chưa" />],
    ]} />
  );
};
