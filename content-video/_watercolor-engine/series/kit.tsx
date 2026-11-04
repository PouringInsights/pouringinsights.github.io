import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { Captions, f, Field, P, Paper, Rise, T, WashFilter, Word } from "../watercolor/engine";

export const PRUSSIAN = "#1F4E79";
export type FilmProps = { audio: string; music: string | null; duration: number; words: Word[]; beats: Record<string, number> };

// A scene ground: plain paper, or paper flooded by one pigment field (the bloom).
export const Ground: React.FC<{ field?: string; id: string; ox?: number; oy?: number; seed?: number }> = ({ field, id, ox, oy, seed }) => (
  <>
    <Paper />
    {field ? <Field id={id} color={field} ox={ox} oy={oy} seed={seed} /> : null}
  </>
);

// text block anchored left; ink chosen for the ground
export const Block: React.FC<{ at?: number; top: number; left?: number; width?: number; children: React.ReactNode }> = ({ at = 0, top, left = 80, width = 920, children }) => (
  <Rise at={at} style={{ position: "absolute", left, top, width }}>{children}</Rise>
);

export const Svg: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>{children}</svg>
);

// painted shape: wash fill through a watercolour filter + optional drawn contour
export const Painted: React.FC<{ id: string; d: string; color: string; seed: number; p?: number; stroke?: string; sw?: number; body?: number }> = ({ id, d, color, seed, p = 1, stroke, sw = 6, body = 0.6 }) => (
  <g opacity={p}>
    <defs><WashFilter id={id} seed={seed} distort={14} body={body} rim={0.7} /></defs>
    <g style={{ mixBlendMode: "multiply" }}><path d={d} fill={color} filter={`url(#${id})`} /></g>
    {stroke ? <path d={d} fill="none" stroke={stroke} strokeWidth={sw} strokeLinejoin="round" strokeLinecap="round" /> : null}
  </g>
);

export type SceneDef = { from: number; to: number; el: React.ReactNode };
export const Film: React.FC<{ props: FilmProps; scenes: SceneDef[] }> = ({ props, scenes }) => (
  <AbsoluteFill style={{ background: P.paper }}>
    {scenes.map((s, i) => (
      <Sequence key={i} from={f(s.from)} durationInFrames={Math.max(1, f(s.to) - f(s.from))}>{s.el}</Sequence>
    ))}
    <Captions words={props.words} hideFrom={props.duration - 2.4} />
    <Audio src={staticFile(props.audio)} />
    {props.music ? <Audio src={staticFile(props.music)} volume={0.13} /> : null}
  </AbsoluteFill>
);

export { P, T };
