"""Per-slide narration with F5-TTS Vietnamese on a CUDA GPU (Manus voice clone).
Same outputs as narrate.py, so build_pptx.py works unchanged.

usage: python f5_narrate.py <work_dir> <lesson_no> [--only 1,2]
needs  <work>/scripts/b<N>_script.json
       <work>/manus/ref.wav            (Manus reference, 24 kHz mono, ~11.6 s)
       <work>/f5vi/model_last.pt, <work>/f5vi/vocab.txt   (hynt/F5-TTS-Vietnamese-ViVoice)
writes <work>/audio/b<N>/s<slide>.m4a (AAC 44.1k stereo 320k, -23 LUFS) + durations.json
"""
import json, os, re, subprocess, sys, time
import numpy as np, torch

W = sys.argv[1]; N = int(sys.argv[2])
only = None
if "--only" in sys.argv:
    only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
OUT_ROOT = os.environ.get("AUDIO_DIR", "audio")
NFE = int(os.environ.get("NFE", 32))
SPEED = float(os.environ.get("SPEED", 1.0))
SR = 24000
REF = f"{W}/manus/ref.wav"
REF_TEXT = ("ba ngành học là marketing, logistics và quản lý chuỗi cung ứng, phân tích dữ liệu kinh doanh. "
            "ba hướng đi khác nhau cùng đào tạo người trẻ có kiến thức, năng lực công nghệ, hiểu thực tiễn và sẵn sàng thích ứng.")

from f5_tts.api import F5TTS
dev = "cuda" if torch.cuda.is_available() else "cpu"
tts = F5TTS(model="F5TTS_Base", ckpt_file=f"{W}/f5vi/model_last.pt", vocab_file=f"{W}/f5vi/vocab.txt", device=dev)
print("device:", dev, torch.cuda.get_device_name(0) if dev == "cuda" else "", flush=True)

def chunks(text, max_words=45):
    """Sentences, merged up to ~max_words syllables (~10-12 s) so F5 stays stable on long slides."""
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    out, cur = [], ""
    for s in sents:
        if cur and len((cur + " " + s).split()) > max_words:
            out.append(cur); cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur: out.append(cur)
    return out

script = json.load(open(f"{W}/scripts/b{N}_script.json", encoding="utf-8"))
out = f"{W}/{OUT_ROOT}/b{N}"; os.makedirs(out, exist_ok=True)
dpath = f"{out}/durations.json"
durs = json.load(open(dpath)) if os.path.exists(dpath) else {}
for item in script:
    s, text = item["slide"], item["text"].strip()
    if not text or (only and s not in only): continue
    m4a = f"{out}/s{s:02d}.m4a"
    if os.path.exists(m4a) and str(s) in durs: continue
    t = time.time()
    parts = [np.zeros(int(0.35 * SR), np.float32)]
    for c in chunks(text):
        wav, sr, _ = tts.infer(ref_file=REF, ref_text=REF_TEXT, gen_text=c.lower(), nfe_step=NFE, speed=SPEED,
                               remove_silence=False, show_info=lambda *a: None)
        parts += [np.asarray(wav, np.float32), np.zeros(int(0.45 * SR), np.float32)]
    parts.append(np.zeros(int(0.3 * SR), np.float32))
    a = np.clip(np.concatenate(parts), -1, 1)
    raw = f"{out}/s{s:02d}.raw"
    (a * 32767).astype("<i2").tofile(raw)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", raw,
                    "-af", "loudnorm=I=-23:TP=-3:LRA=7,aresample=44100", "-ac", "2", "-c:a", "aac", "-b:a", "320k", m4a],
                   check=True)
    os.remove(raw)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", m4a],
                             capture_output=True, text=True).stdout)
    durs[str(s)] = d; json.dump(durs, open(dpath, "w"), indent=1)
    print(f"b{N} slide {s}: {d:.1f}s audio in {time.time()-t:.0f}s", flush=True)
print("done", N, round(sum(durs.values()) / 60, 1), "min")
