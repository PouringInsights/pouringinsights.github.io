#!/bin/bash
# Pre-generate Manus-voice (v1) backups on the otherwise idle CPU, last lesson first.
S="$1"; cd "$S"; . vn311/bin/activate
for n in 8 7 6 5 4 3 1; do
  [ -f "audio_manus/b$n/.complete" ] && continue
  AUDIO_DIR=audio_manus SIMPLE=1 python tools/narrate.py "$S" $n 2>&1 | grep --line-buffered -E "^done|Error|Traceback" && touch "audio_manus/b$n/.complete"
done
echo BACKUP_DONE
