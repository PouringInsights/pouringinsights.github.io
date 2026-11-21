import React from "react";
import { Composition, registerRoot } from "remotion";
import { CraftCrema, CraftProps } from "./CraftCrema";

const base: CraftProps = { audio: "", music: null, duration: 58, words: [], beats: {} };
const Root: React.FC = () => (
  <Composition
    id="CraftCrema"
    component={CraftCrema as unknown as React.FC<Record<string, unknown>>}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={1760}
    defaultProps={base as unknown as Record<string, unknown>}
    calculateMetadata={({ props }) => ({ durationInFrames: Math.ceil((props as unknown as CraftProps).duration * 30) })}
  />
);
registerRoot(Root);
