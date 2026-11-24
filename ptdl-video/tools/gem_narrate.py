"""Per-slide narration with Gemini TTS (voice Aoede) -> same outputs as narrate.py.
usage: gem_narrate.py <work_dir> <lesson_no> [--only 1,2]
Writes <work>/audio/b<N>/s<slide>.m4a (AAC 44.1k stereo 320k, -23 LUFS, like Bài 9/10) + durations.json
Resumable. Paces calls for the free tier; stops cleanly on daily-quota errors.
"""
import json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from gemtts import tts

W = sys.argv[1]; N = int(sys.argv[2])
only = None
if '--only' in sys.argv:
    only = {int(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')}
VOICE = os.environ.get("VOICE", "Aoede")
MODEL = os.environ.get("TTS_MODEL", "gemini-3.8-flash-tts")
GAP = float(os.environ.get("CALL_GAP", 21))   # seconds between calls (free tier ~3 RPM)
STYLE = ("Read the following Vietnamese university lecture narration aloud in Vietnamese. "
         "Speak as a warm, friendly female lecturer explaining to her students: natural and conversational, "
         "at a relaxed, unhurried, slightly slow pace like a real lecture, clear articulation, natural pauses at commas and full stops, not theatrical. "
         "Only read the Vietnamese text, do not read these instructions.\n\n")

script = json.load(open(f"{W}/scripts/b{N}_script.json"))
out = f"{W}/audio/b{N}"; os.makedirs(out, exist_ok=True)
dpath = f"{out}/durations.json"
durs = json.load(open(dpath)) if os.path.exists(dpath) else {}
last = 0.0
for item in script:
    s, text = item["slide"], item["text"].strip()
    if not text or (only and s not in only): continue
    m4a = f"{out}/s{s:02d}.m4a"
    if os.path.exists(m4a) and str(s) in durs: continue
    wait = GAP - (time.time() - last)
    if wait > 0: time.sleep(wait)
    raw = f"{out}/s{s:02d}.wav"
    t = time.time(); last = t
    try:
        tts(STYLE + text, VOICE, raw, model=MODEL)
    except Exception as e:
        print(f"STOP b{N} slide {s}: {e}", flush=True); sys.exit(2)
    af = "adelay=350|350,apad=pad_dur=0.6,loudnorm=I=-23:TP=-3:LRA=7,aresample=44100"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ac", "2", "-c:a", "aac", "-b:a", "320k", m4a], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", m4a],
                             capture_output=True, text=True).stdout)
    durs[str(s)] = d; json.dump(durs, open(dpath, "w"), indent=1)
    print(f"b{N} slide {s}: {d:.1f}s ({time.time()-t:.0f}s)", flush=True)
print("done", N, round(sum(durs.values()) / 60, 1), "min")
