import sys, certifi
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
import asyncio, edge_tts
voice, rate, pitch, text_file, out = sys.argv[1:6]
async def main():
    c = edge_tts.Communicate(open(text_file).read(), voice, rate=rate, pitch=pitch, boundary="WordBoundary")
    subs = edge_tts.SubMaker()
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] in ("WordBoundary","SentenceBoundary"): subs.feed(ch)
    open(out.rsplit(".",1)[0]+".srt","w").write(subs.get_srt())
asyncio.run(main())
