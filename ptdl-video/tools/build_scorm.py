"""Render a narrated lesson to MP4 (HaUI intro + one still per visible slide for its narration length,
0.4 s fade through black between slides) and wrap it as a SCORM 1.2 package.
usage: build_scorm.py <work_dir> <lesson_no> <out_dir>
needs: <work>/gv/src/x<N> (fixed deck), <work>/audio/b<N>/s<slide>.m4a + durations.json, <work>/gv/b10 (intro)
"""
import json, os, re, shutil, subprocess, sys, zipfile, html

W, N, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
TITLE = {1: "Tổng quan Phân tích dữ liệu Marketing", 3: "Phân tích khách hàng và sản phẩm bằng phân cụm",
         4: "Phân tích kết hợp và định giá dựa trên giá trị", 5: "Giá trị vòng đời khách hàng (CLV)",
         6: "Phân tích nhân tố về hành vi khách hàng", 7: "Hồi quy và đo lường hiệu quả kênh",
         8: "Mô hình cấu trúc tuyến tính (SEM)"}[N]
SRC = f"{W}/gv/src/x{N}"; AUD = f"{W}/audio/b{N}"; T = f"{W}/scorm_build/b{N}"
shutil.rmtree(T, ignore_errors=True); os.makedirs(f"{T}/seg"); os.makedirs(f"{T}/img")
durs = json.load(open(f"{AUD}/durations.json"))
FPS, FADE = 25, 0.4
run = lambda *a: subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

# 1) visible slides in presentation order
P = f"{SRC}/ppt"
pres = open(f"{P}/presentation.xml", encoding="utf-8").read()
rels = open(f"{P}/_rels/presentation.xml.rels", encoding="utf-8").read()
rid = {}
for m in re.finditer(r"<Relationship [^>]*/>", rels):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(0))); rid[a["Id"]] = a["Target"]
order = [rid[r] for r in re.findall(r'<p:sldId [^>]*r:id="(rId\d+)"', pres)]
visible = [i for i, t in enumerate(order, 1) if 'show="0"' not in open(f"{P}/{t}", encoding="utf-8").read()[:600]]

# 2) slide images from LibreOffice PDF export (hidden slides are skipped by the export)
deck = f"{T}/deck.pptx"
with zipfile.ZipFile(deck, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(SRC):
        for f in files:
            full = os.path.join(root, f); z.write(full, os.path.relpath(full, SRC))
run("soffice", "--headless", "--convert-to", "pdf", "--outdir", T, deck)
run("pdftoppm", "-r", "144", "-png", f"{T}/deck.pdf", f"{T}/img/p")
imgs = sorted(os.listdir(f"{T}/img"), key=lambda s: int(re.findall(r"\d+", s)[0]))
assert len(imgs) == len(visible), (len(imgs), len(visible))

# 3) segments
segs = []
intro = f"{W}/gv/b10/ppt/media/media1.mp4"
run("ffmpeg", "-y", "-i", intro, "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", f"{T}/seg/000.mp4")
segs.append(f"{T}/seg/000.mp4")
for k, (si, img) in enumerate(zip(visible, imgs), 1):
    if str(si) not in durs: continue
    d = durs[str(si)]; out = f"{T}/seg/{k:03d}.mp4"
    vf = (f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,fps={FPS},"
          f"fade=t=in:st=0:d={FADE},fade=t=out:st={d - FADE:.3f}:d={FADE},format=yuv420p")
    run("ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", f"{T}/img/{img}", "-i", f"{AUD}/s{si:02d}.m4a",
        "-t", f"{d:.3f}", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-crf", "22",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-shortest", out)
    segs.append(out)
open(f"{T}/list.txt", "w").write("".join(f"file '{s}'\n" for s in segs))
os.makedirs(f"{T}/pkg", exist_ok=True)
video = f"{T}/pkg/video.mp4"
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{T}/list.txt", "-c", "copy", "-movflags", "+faststart", video)
run("ffmpeg", "-y", "-i", f"{T}/img/{imgs[0]}", "-vf", "scale=1280:-2", f"{T}/pkg/poster.jpg")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                           capture_output=True, text=True).stdout)

# 4) SCORM 1.2 package
name = f"Bài {N}. {TITLE}"
ident = f"PTDL_MKT_B{N}"
open(f"{T}/pkg/imsmanifest.xml", "w", encoding="utf-8").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{ident}" version="1.0"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata><schema>ADL SCORM</schema><schemaversion>1.2</schemaversion></metadata>
  <organizations default="ORG_{ident}">
    <organization identifier="ORG_{ident}">
      <title>{html.escape(name)}</title>
      <item identifier="ITEM_{ident}" identifierref="RES_{ident}" isvisible="true">
        <title>{html.escape(name)}</title>
        <adlcp:masteryscore>100</adlcp:masteryscore>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_{ident}" type="webcontent" adlcp:scormtype="sco" href="index.html">
      <file href="index.html"/><file href="video.mp4"/><file href="poster.jpg"/>
    </resource>
  </resources>
</manifest>
""")
open(f"{T}/pkg/index.html", "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(name)}</title>
<style>
html,body{{margin:0;height:100%;background:#0b1f4d;font-family:Arial,Helvetica,sans-serif;color:#fff}}
.wrap{{max-width:1280px;margin:0 auto;padding:12px}}
h1{{font-size:18px;font-weight:600;margin:4px 0 10px}}
video{{width:100%;background:#000;display:block}}
.bar{{display:flex;justify-content:space-between;font-size:13px;opacity:.85;margin-top:8px}}
</style></head><body><div class="wrap">
<h1>{html.escape(name)} – Phân tích dữ liệu Marketing</h1>
<video id="v" controls preload="metadata" poster="poster.jpg" controlsList="nodownload"><source src="video.mp4" type="video/mp4"></video>
<div class="bar"><span>Khoa Kinh doanh số – Trường Kinh tế, Đại học Công nghiệp Hà Nội</span><span id="st">Đã xem 0%</span></div>
</div>
<script>
// Minimal SCORM 1.2 runtime: resume position, mark completed at 95% watched.
var api=null;function findAPI(w){{var n=0;while(w&&!w.API&&w.parent&&w.parent!=w&&n<10){{w=w.parent;n++;}}return w?w.API||null:null;}}
api=findAPI(window)||(window.opener?findAPI(window.opener):null);
function g(k){{try{{return api?api.LMSGetValue(k):"";}}catch(e){{return "";}}}}
function s(k,v){{try{{if(api)api.LMSSetValue(k,v);}}catch(e){{}}}}
function c(){{try{{if(api)api.LMSCommit("");}}catch(e){{}}}}
var v=document.getElementById("v"),st=document.getElementById("st"),done=false,maxT=0,last=0,t0=Date.now();
if(api){{api.LMSInitialize("");var ls=g("cmi.core.lesson_status");done=(ls=="completed"||ls=="passed");
 if(!done&&(ls==""||ls=="not attempted"))s("cmi.core.lesson_status","incomplete");
 var sd=g("cmi.suspend_data");if(sd){{try{{maxT=JSON.parse(sd).m||0;}}catch(e){{}}}} c();}}
v.addEventListener("loadedmetadata",function(){{var loc=parseFloat(g("cmi.core.lesson_location"));if(loc>5&&loc<v.duration-5)v.currentTime=loc;}});
v.addEventListener("timeupdate",function(){{
 if(v.currentTime<=maxT+2)maxT=Math.max(maxT,v.currentTime);
 var pct=v.duration?Math.min(100,Math.round(maxT/v.duration*100)):0;st.textContent="Đã xem "+pct+"%";
 if(Date.now()-last>15000){{last=Date.now();s("cmi.core.lesson_location",String(Math.floor(v.currentTime)));s("cmi.suspend_data",JSON.stringify({{m:Math.floor(maxT)}}));c();}}
 if(!done&&pct>=95){{done=true;s("cmi.core.score.raw","100");s("cmi.core.lesson_status","completed");c();}}
}});
v.addEventListener("ended",function(){{if(!done){{done=true;s("cmi.core.score.raw","100");s("cmi.core.lesson_status","completed");}}c();}});
function fin(){{if(!api)return;s("cmi.core.lesson_location",String(Math.floor(v.currentTime)));s("cmi.suspend_data",JSON.stringify({{m:Math.floor(maxT)}}));
 var sec=Math.floor((Date.now()-t0)/1000),h=Math.floor(sec/3600),m=Math.floor(sec%3600/60),x=sec%60;
 s("cmi.core.session_time",("000"+h).slice(-4)+":"+("0"+m).slice(-2)+":"+("0"+x).slice(-2));
 s("cmi.core.exit",done?"":"suspend");c();try{{api.LMSFinish("");}}catch(e){{}}api=null;}}
window.addEventListener("pagehide",fin);window.addEventListener("beforeunload",fin);
</script></body></html>
""")
os.makedirs(OUT, exist_ok=True)
zp = f"{OUT}/SCORM_Bai_{N}_PTDL_Marketing.zip"
if os.path.exists(zp): os.remove(zp)
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for f in ("imsmanifest.xml", "index.html", "poster.jpg"): z.write(f"{T}/pkg/{f}", f)
    z.write(video, "video.mp4", compress_type=zipfile.ZIP_STORED)
print(zp, f"video {dur/60:.1f} min", f"zip {os.path.getsize(zp)/1e6:.1f} MB", f"slides {len(segs)-1}")
