import base64, json, sys, time, urllib.request, wave, os
URL = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"
def tts(text, voice, out, model="gemini-3.8-flash-tts", tries=6):
    body = {"contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for k in range(tries):
        req = urllib.request.Request(URL.format(m=model), data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=300))
            part = r["candidates"][0]["content"]["parts"][0]["inlineData"]
            pcm = base64.b64decode(part["data"])
            with wave.open(out, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            return len(pcm) / 48000
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            print("HTTP", e.code, msg, file=sys.stderr, flush=True)
            if e.code in (429, 500, 503): time.sleep(25 * (k + 1)); continue
            raise
    raise RuntimeError("gave up")
if __name__ == "__main__":
    text = open(sys.argv[1]).read().strip(); outdir = sys.argv[2]
    for v in sys.argv[3].split(","):
        p = f"{outdir}/{v}.wav"
        if os.path.exists(p): continue
        print(v, round(tts(text, v, p), 1), flush=True)
