import React from "react";
import { Composition } from "remotion";
import { GeishaFilm, GeishaProps, defaultProps } from "./GeishaFilm";

export const Root: React.FC = () => (
  <Composition
    id="GeishaFilm"
    component={GeishaFilm as unknown as React.FC<Record<string, unknown>>}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={1740}
    defaultProps={defaultProps as unknown as Record<string, unknown>}
    calculateMetadata={({ props }) => {
      const p = props as unknown as GeishaProps;
      return { durationInFrames: Math.ceil(p.duration * 30) };
    }}
  />
);
