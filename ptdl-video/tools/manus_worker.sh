#!/bin/bash
# Worker: Manus-voice (VieNeu v1) narration + pptx build. Lessons are claimed with a lock dir so
# two workers (forward / backward order) never do the same lesson.
S="$1"; shift; cd "$S"; . vn311/bin/activate
for n in "$@"; do
  [ -f "audio_manus/b$n/.complete" ] && [ -f "out/Bai_${n}_PTDL_Marketing_long_tieng.pptx" ] && continue
  mkdir -p locks; mkdir "locks/b$n" 2>/dev/null || continue
  AUDIO_DIR=audio_manus SIMPLE=1 python tools/narrate.py "$S" $n 2>&1 | grep --line-buffered -E "^done|Error|Traceback"
  if [ ${PIPESTATUS[0]} = 0 ]; then
    touch "audio_manus/b$n/.complete"
    rm -rf "audio/b$n"; mkdir -p audio; cp -r "audio_manus/b$n" "audio/b$n"
    python3 tools/build_pptx.py "$S" $n "$S/out/Bai_${n}_PTDL_Marketing_long_tieng.pptx" 2>&1 | grep -vi deprecat
    echo "LESSON_READY $n"
  fi
done
echo WORKER_DONE
