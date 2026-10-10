import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Fonts } from "./common";
import { C, FONT } from "./bkit";
import { Variant, PersonPose, blink } from "./Cast";
import { Chibi as Person } from "./Chibi";

const Label: React.FC<{ t: string; s: string }> = ({ t, s }) => (
  <div style={{ textAlign: "center", fontFamily: FONT, color: C.navy }}>
    <div style={{ fontWeight: 800, fontSize: 30 }}>{t}</div>
    <div style={{ fontWeight: 600, fontSize: 22, opacity: 0.7 }}>{s}</div>
  </div>
);

export const CastSheet: React.FC = () => {
  const f = useCurrentFrame();
  const wave = Math.sin(f * 0.45) * 20;
  const row1: { v: Variant; t: string; s: string; pose: PersonPose }[] = [
    { v: "ponytail", t: "Sinh viên Marketing", s: "polo HaUI · quần be", pose: { rS: 125, rE: wave * 0.8, blink: blink(f, 1), tilt: 4 } },
    { v: "boy", t: "Sinh viên Logistics", s: "polo HaUI · quần kaki", pose: { blink: blink(f, 2) } },
    { v: "longHair", t: "Sinh viên Dữ liệu", s: "polo HaUI · quần be", pose: { blink: blink(f, 3), lS: 20, lE: 80 } },
    { v: "teacher", t: "Giảng viên", s: "blazer navy", pose: { rS: 70, rE: 30, blink: blink(f, 4), mouth: 0.5 } },
  ];
  const row2: { v: Variant; pose: PersonPose }[] = [
    { v: "ponytail", pose: { rS: 60, rE: 40, rHold: "megaphone", mouth: 0.7 } },
    { v: "boy", pose: { rS: 30, rE: 70, lS: 30, lE: 70, rHold: "box" } },
    { v: "longHair", pose: { lS: 30, lE: 80, lHold: "laptop", rS: 120, rE: -20 } },
    { v: "boy", pose: { walk: f * 0.3 } },
    { v: "ponytail", pose: { rS: 160, rE: 0, rHold: "cap", lS: 160, lE: 0, mouth: 0.6 } },
  ];
  return (
    <AbsoluteFill style={{ backgroundColor: C.cream }}>
      <Fonts />
      <div style={{ position: "absolute", left: 60, top: 30, fontFamily: FONT, fontWeight: 900, fontSize: 40, color: C.navy }}>Bộ nhân vật · bản C</div>
      <div style={{ position: "absolute", left: 20, top: 130, width: 1400, display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
        {row1.map((c, i) => (
          <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <Person v={c.v} pose={c.pose} height={600} />
            <Label t={c.t} s={c.s} />
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 1460, top: 40, fontFamily: FONT, fontWeight: 700, fontSize: 26, color: C.navy, opacity: 0.7 }}>Tư thế & đạo cụ</div>
      <div style={{ position: "absolute", left: 1450, top: 90, right: 10, display: "flex", flexWrap: "wrap", gap: 0 }}>
        {row2.map((c, i) => (
          <div key={i} style={{ width: 225, height: 320, display: "flex", justifyContent: "center" }}>
            <Person v={c.v} pose={c.pose} height={280} />
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
