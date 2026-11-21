#!/usr/bin/env bash
# One-command setup for the motion/video toolkit. Safe to re-run.
# Usage: bash motion-lab/setup.sh            (everything)
#        bash motion-lab/setup.sh js         (JS only: Three.js, GSAP, Remotion...)
#        bash motion-lab/setup.sh py         (Python only: Manim, librosa, WhisperX)
set -uo pipefail
cd "$(dirname "$0")"
WHAT="${1:-all}"

if [ "$WHAT" != "py" ]; then
  echo "== JS libraries"
  npm ci --no-audit --no-fund || npm install --no-audit --no-fund
fi

if [ "$WHAT" != "js" ]; then
  echo "== System libraries (ffmpeg, cairo/pango for Manim)"
  if command -v apt-get >/dev/null && [ "$(id -u)" = 0 ]; then
    apt-get update -qq && apt-get install -y -qq ffmpeg libpango1.0-dev libcairo2-dev pkg-config >/dev/null \
      || echo "!! apt-get failed; Manim may not build"
  else
    echo "!! no root/apt: make sure ffmpeg and pango/cairo dev libs are installed"
  fi
  echo "== Python libraries"
  [ -d .venv ] || python3 -m venv .venv
  . .venv/bin/activate
  pip install -q --upgrade pip
  pip install -q torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cpu
  pip install -q -r requirements.txt
fi

echo "== Check"
[ "$WHAT" != "py" ] && node -e "const fs=require('fs');for (const p of ['three','gsap','remotion','three.quarks','tweakpane','lottie-web','motion','@react-three/fiber','@react-three/rapier']) console.log('ok', p, JSON.parse(fs.readFileSync('node_modules/'+p+'/package.json')).version)"
[ "$WHAT" != "js" ] && python -c "import manim, librosa, whisperx; print('ok manim', manim.__version__, '| librosa', librosa.__version__)"
command -v ffmpeg >/dev/null && echo "ok ffmpeg" || echo "!! ffmpeg missing"
echo "Done. Python: source motion-lab/.venv/bin/activate"
