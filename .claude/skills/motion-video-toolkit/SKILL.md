---
name: motion-video-toolkit
description: >
  Picks and sets up the right open-source library for 3D scenes, VFX, timeline animation, code-driven video,
  explainer math videos, Lottie playback, free sound effects/music, beat sync, word-level subtitles and video export.
  Covers Blender MCP (scenario-labs), Three.js, React Three Rapier, React Postprocessing, three.quarks, Tweakpane,
  GSAP, Remotion, Manim, lottie-web, the Openverse audio API, librosa, WhisperX and FFmpeg. Use whenever a task
  involves building a 3D scene, camera moves, physics, bloom/depth-of-field/film effects, particles, a live tweak
  panel, a GSAP timeline, rendering a video from code, an animated diagram or formula, finding royalty-free audio,
  syncing animation to music beats, generating timed captions, or compressing/exporting MP4/WebM/GIF.
---

# Motion & video toolkit

Choose the smallest tool that does the job, install it into the project that needs it (never globally into this
Jekyll site), and pin exact versions. For design taste (timing, easing, the 12 principles) read the `motion-design`
skill; for Motion/Framer Motion and CSS springs use `motion`; for Remotion specifics use the `remotion-*` skills.

## 3D and effects

| # | Tool | Use it for | Install |
|---|------|-----------|---------|
| 07 | Blender plugin (scenario-labs/blender-plugin) | A team of agents modelling/lighting/rendering inside Blender over MCP | Needs Blender on the user's own machine. Follow https://github.com/scenario-labs/blender-plugin README to install the add-on and register its MCP server with `claude mcp add`. Not usable in a headless cloud container. |
| 08 | Three.js | 3D scenes, materials, camera paths (`CatmullRomCurve3` + `lookAt`) | `npm i three` (CDN: `https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js`) |
| 09 | React Three Rapier | Real rigid-body physics in React Three Fiber | `npm i @react-three/fiber @react-three/drei @react-three/rapier` |
| 10 | React Postprocessing | Bloom, depth of field, noise, vignette, chromatic aberration | `npm i @react-three/postprocessing postprocessing` |
| 11 | three.quarks | Particle systems, trails, VFX | `npm i three.quarks` |
| 12 | Tweakpane | Live parameter panel for tuning a scene | `npm i tweakpane @tweakpane/plugin-essentials` |

Rules: cap `devicePixelRatio` at 2, dispose geometries/materials on unmount, respect `prefers-reduced-motion`.

## Motion and video

| # | Tool | Use it for | Install |
|---|------|-----------|---------|
| 13 | GSAP (all plugins free, incl. ScrollTrigger, SplitText, MorphSVG) | Sequenced timelines, scroll-driven animation | `npm i gsap` then `gsap.registerPlugin(ScrollTrigger)` |
| 14 | Remotion | Video as React components, rendered to MP4 | `npx create-video@latest`; render `npx remotion render`. Check license via `remotion-license` skill. |
| 15 | Manim (Community) | Math/diagram explainer videos | `pip install manim` (needs `ffmpeg`, plus LaTeX for `MathTex`); render `manim -pqh scene.py Scene` |
| 16 | lottie-web | Play lightweight After Effects/Lottie JSON | `npm i lottie-web` or the `@lottiefiles/dotlottie-web` player |

## Audio, subtitles, export

| # | Tool | Use it for | How |
|---|------|-----------|-----|
| 17 | Openverse API | Free CC-licensed sound effects, ambience, music | `GET https://api.openverse.org/v1/audio/?q=whoosh&license_type=commercial` — keep each result's `license`, `creator` and `foreign_landing_url` and write attribution into the project. |
| 18 | librosa | Beat/onset times so animation hits the beat | `pip install librosa`; `tempo, beats = librosa.beat.beat_track(y=y, sr=sr); times = librosa.frames_to_time(beats, sr=sr)` → export JSON of seconds, convert to frames (`round(t*fps)`). |
| 19 | WhisperX | Word-level timestamps for captions | `pip install whisperx`; `whisperx audio.wav --model large-v3 --output_format json` (GPU strongly preferred; use `--compute_type int8` on CPU). Feed words into Remotion captions (`remotion-captions` skill). |
| 20 | FFmpeg | Compress and export | Web MP4: `ffmpeg -i in.mov -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k out.mp4`. WebM: `-c:v libvpx-vp9 -crf 32 -b:v 0`. GIF: palettegen/paletteuse two-pass. |

## Typical pipeline

1. Music: Openverse → librosa beats JSON.
2. Voice: WhisperX word timings JSON.
3. Build the piece in Remotion (or Three.js/GSAP for web), keying cues to the beat and word JSON.
4. Render, then FFmpeg for final compression.
