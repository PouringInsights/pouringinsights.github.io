import React from "react";
import { Composition, registerRoot } from "remotion";
import { FPS } from "./common";
import { VersionA, V1_DURATION } from "./VersionA";
import { VersionB } from "./VersionB";
import { B_TOTAL } from "./bkit";

const KdsRoot: React.FC = () => (
  <>
    <Composition
      id="KDS-A"
      component={VersionA}
      durationInFrames={Math.floor(V1_DURATION * FPS)}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="KDS-B"
      component={VersionB}
      durationInFrames={Math.floor(B_TOTAL * FPS)}
      fps={FPS}
      width={1920}
      height={1080}
    />
  </>
);

registerRoot(KdsRoot);
