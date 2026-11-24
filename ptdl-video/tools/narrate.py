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

import re
# --- prosody tuning to match the original Manus narration (measured: 3.74 syl/s overall,
#     ~0.56 s pauses, F0 ~226 Hz; raw clone: 4.25 syl/s, fewer/shorter pauses, ~234 Hz)
SENT_GAP = float(os.environ.get("SENT_GAP", 0.62))     # pause between sentences (s)
PAUSE_MULT = float(os.environ.get("PAUSE_MULT", 1.7))  # lengthen in-sentence breath pauses
PAUSE_MIN = 0.09                                       # silence shorter than this is not a pause
PITCH = float(os.environ.get("PITCH_SEMI", -0.6))      # semitones

def sentences(text):
    parts = re.split(r'(?<=[.!?…])\s+', text.strip())
    return [p for p in parts if p.strip()]

def stretch_pauses(a):
    fr = int(0.01 * SR)
    n = len(a) // fr
    if n < 3: return a
    rms = np.sqrt(np.mean(a[:n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    thr = max(np.percentile(rms, 95) * 0.06, 1e-4)
    quiet = rms < thr
    out, i = [], 0
    while i < n:
        j = i
        while j < n and quiet[j] == quiet[i]: j += 1
        seg = a[i * fr:j * fr]
        dur = (j - i) * 0.01
        if quiet[i] and PAUSE_MIN <= dur and 0 < i and j < n:
            seg = np.zeros(int(len(seg) * PAUSE_MULT), dtype=np.float32)
        out.append(seg); i = j
    out.append(a[n * fr:])
    return np.concatenate(out)

def trim(a):
    idx = np.where(np.abs(a) > 0.01)[0]
    if len(idx) == 0: return a
    return a[max(idx[0] - int(0.03 * SR), 0): idx[-1] + int(0.08 * SR)]

durs = {}
dpath = f"{out}/durations.json"
if os.path.exists(dpath): durs = json.load(open(dpath))
for item in script:
    s, text = item["slide"], item["text"].strip()
    if not text or (only and s not in only): continue
    m4a = f"{out}/s{s:02d}.m4a"
    if os.path.exists(m4a) and str(s) in durs: continue
    t = time.time()
    pieces = [np.zeros(int(0.35 * SR), dtype=np.float32)]
    for k, sent in enumerate(sentences(text)):
        a = tts.infer(sent, ref_audio=REF, silence_p=0.25)
        pieces.append(stretch_pauses(trim(a.astype(np.float32))))
        pieces.append(np.zeros(int(SENT_GAP * SR), dtype=np.float32))
    pieces.append(np.zeros(int(0.3 * SR), dtype=np.float32))
    a = np.concatenate(pieces)
    raw = f"{out}/s{s:02d}.wav"; write_wav(raw, a)
    # pitch down slightly (formant-preserving), then loudness like Bài 9/10 (~ -23 LUFS, peaks < -3 dBTP)
    af = f"rubberband=pitch={2 ** (PITCH / 12):.5f}:formant=preserved,loudnorm=I=-23:TP=-3:LRA=7,aresample=44100"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af,
                    "-ac", "2", "-c:a", "aac", "-b:a", "320k", m4a], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", m4a],
                             capture_output=True, text=True).stdout)
    durs[str(s)] = d
    json.dump(durs, open(dpath, "w"), indent=1)
    print(f"b{N} slide {s}: {d:.1f}s audio in {time.time()-t:.0f}s", flush=True)
print("done", N, round(sum(durs.values()) / 60, 1), "min")
