import React from "react";
import { Composition, registerRoot } from "remotion";
import { CraftProps } from "./kit";
import { GeishaCraft } from "./films/Geisha";
import { V60Craft } from "./films/V60";
import { MelittaCraft } from "./films/Melitta";
import { BachCraft } from "./films/Bach";
import { SwedenCraft } from "./films/Sweden";

const base: CraftProps = { audio: "", music: null, duration: 50, words: [], beats: {} };
const FILMS: [string, React.FC<CraftProps>][] = [
  ["Geisha", GeishaCraft],
  ["V60", V60Craft],
  ["Melitta", MelittaCraft],
  ["Bach", BachCraft],
  ["Sweden", SwedenCraft],
];

const Root: React.FC = () => (
  <>
    {FILMS.map(([id, C]) => (
      <Composition
        key={id}
        id={id}
        component={C as unknown as React.FC<Record<string, unknown>>}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={1500}
        defaultProps={base as unknown as Record<string, unknown>}
        calculateMetadata={({ props }) => ({ durationInFrames: Math.ceil((props as unknown as CraftProps).duration * 30) })}
      />
    ))}
  </>
);
registerRoot(Root);
