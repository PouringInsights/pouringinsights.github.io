"""Generate per-slide narration (Manus voice clone, VieNeu v3 Turbo) for one lesson.
usage: narrate.py <work_dir> <lesson_no> [--only 1,2]
Reads  <work>/scripts/b<N>_script.json, ref voice <work>/manus/ref48.wav
Writes <work>/audio/b<N>/s<slide>.m4a (AAC 44.1k stereo 320k, -23 LUFS) + durations.json
Resumable: existing m4a files are skipped.
"""
import json, os, sys, subprocess, time, wave
import numpy as np

W = sys.argv[1]; N = int(sys.argv[2])
only = None
if '--only' in sys.argv:
    only = {int(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')}
script = json.load(open(f"{W}/scripts/b{N}_script.json"))
out = f"{W}/audio/b{N}"; os.makedirs(out, exist_ok=True)
REF = f"{W}/manus/ref48.wav"
SR = 48000

from vieneu import Vieneu
tts = Vieneu(precision=os.environ.get("VN_PREC", "int8"))

def write_wav(path, a):
    a = np.clip(a, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((a * 32767).astype(np.int16).tobytes())

durs = {}
dpath = f"{out}/durations.json"
if os.path.exists(dpath): durs = json.load(open(dpath))
for item in script:
    s, text = item["slide"], item["text"].strip()
    if not text or (only and s not in only): continue
    m4a = f"{out}/s{s:02d}.m4a"
    if os.path.exists(m4a) and str(s) in durs: continue
    t = time.time()
    a = tts.infer(text, ref_audio=REF)
    a = np.concatenate([np.zeros(int(0.35 * SR)), a, np.zeros(int(0.6 * SR))]).astype(np.float32)
    raw = f"{out}/s{s:02d}.wav"; write_wav(raw, a)
    # two-pass-free loudness: loudnorm single pass to match Bài 9/10 (~ -23 LUFS, peaks < -3 dBTP)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "loudnorm=I=-23:TP=-3:LRA=7,aresample=44100",
                    "-ac", "2", "-c:a", "aac", "-b:a", "320k", m4a], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", m4a],
                             capture_output=True, text=True).stdout)
    durs[str(s)] = d
    json.dump(durs, open(dpath, "w"), indent=1)
    print(f"b{N} slide {s}: {d:.1f}s audio in {time.time()-t:.0f}s", flush=True)
print("done", N, round(sum(durs.values()) / 60, 1), "min")
