import React from "react";
import { Composition, registerRoot } from "remotion";
import { FilmProps } from "./kit";
import { MelittaFilm } from "./Melitta";
import { BachFilm } from "./Bach";
import { SwedenFilm } from "./Sweden";
import { CremaFilm } from "./Crema";

const base: FilmProps = { audio: "", music: null, duration: 45, words: [], beats: {} };
const FILMS: [string, React.FC<FilmProps>][] = [
  ["Melitta", MelittaFilm],
  ["Bach", BachFilm],
  ["Sweden", SwedenFilm],
  ["Crema", CremaFilm],
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
        durationInFrames={1350}
        defaultProps={base as unknown as Record<string, unknown>}
        calculateMetadata={({ props }) => ({ durationInFrames: Math.ceil((props as unknown as FilmProps).duration * 30) })}
      />
    ))}
  </>
);

registerRoot(Root);
