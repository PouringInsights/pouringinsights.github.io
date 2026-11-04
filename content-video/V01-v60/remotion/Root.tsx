import React from "react";
import { Composition } from "remotion";
import { V60Film, V60Props, defaultProps } from "./V60Film";

export const Root: React.FC = () => (
  <Composition
    id="V60Film"
    component={V60Film as unknown as React.FC<Record<string, unknown>>}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={1560}
    defaultProps={defaultProps as unknown as Record<string, unknown>}
    calculateMetadata={({ props }) => ({ durationInFrames: Math.ceil((props as unknown as V60Props).duration * 30) })}
  />
);
