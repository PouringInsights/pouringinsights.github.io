#!/bin/bash
# Voice every lesson with Gemini Aoede; once the Gemini quota runs out, the interrupted lesson and all
# remaining lessons are redone entirely in the Manus clone voice (VieNeu, v1 settings). One voice per lesson.
S="$1"; shift; LESSONS="${@:-1 3 4 5 6 7 8}"
cd "$S"
GEM_OK=1
for n in $LESSONS; do
  if [ $GEM_OK = 1 ] && [ ! -f "audio/b$n/.manus" ]; then
    python3 tools/gem_narrate.py "$S" $n 2>&1 | grep --line-buffered -E "^done|STOP"
    if [ ${PIPESTATUS[0]} = 2 ]; then
      GEM_OK=0
      echo "Gemini quota exhausted at lesson $n -> switching to Manus voice"
      rm -rf "audio_gem_partial_b$n"; mv "audio/b$n" "audio_gem_partial_b$n"
    fi
  fi
  if [ $GEM_OK = 0 ] || [ -f "audio/b$n/.manus" ]; then
    mkdir -p "audio/b$n"
    # reuse the backup made in parallel (audio_manus/) when it is complete
    if [ -f "audio_manus/b$n/.complete" ]; then rm -rf "audio/b$n"; cp -r "audio_manus/b$n" "audio/b$n"; fi
    touch "audio/b$n/.manus"
    ( . vn311/bin/activate; SIMPLE=1 python tools/narrate.py "$S" $n 2>&1 | grep --line-buffered -E "^done|Error|Traceback" )
  fi
  voice=$([ -f "audio/b$n/.manus" ] && echo manus || echo aoede)
  python3 tools/build_pptx.py "$S" $n "$S/out/Bai_${n}_PTDL_Marketing_long_tieng.pptx" 2>&1 | grep -vi deprecat
  echo "lesson $n built with voice=$voice"
done
echo ALL_DONE
