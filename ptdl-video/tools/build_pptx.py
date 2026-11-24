"""Assemble a narrated lesson pptx in the same structure as Bài 9/10:
 - new slide 1: HaUI "Bài giảng trực tuyến" intro (fullscreen mp4 + its audio), copied from Bài 10
 - every narrated slide: embedded m4a (narration, hidden in show), autoplay, auto-advance = audio length,
   fade transition 2 s (spd=slow, p14:dur=2000)
usage: build_pptx.py <work_dir> <lesson_no> <out.pptx>
"""
import json, os, re, shutil, sys, zipfile

W, N, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
SRC = f"{W}/gv/src/x{N}"            # unzipped source lesson pptx
REF = f"{W}/gv/b10"                 # unzipped Bài 10 (template for intro + audio element)
AUD = f"{W}/audio/b{N}"
TMP = f"{W}/build/b{N}"
shutil.rmtree(TMP, ignore_errors=True); shutil.copytree(SRC, TMP)
P = f"{TMP}/ppt"
durs = json.load(open(f"{AUD}/durations.json"))

R_AUDIO = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio"
R_VIDEO = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/video"
R_MEDIA = "http://schemas.microsoft.com/office/2007/relationships/media"
R_IMAGE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
R_SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
R_LAYOUT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"

def rels_read(path):
    x = open(path, encoding="utf-8").read() if os.path.exists(path) else \
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'
    return x

def next_rid(x):
    ids = [int(i) for i in re.findall(r'Id="rId(\d+)"', x)]
    return f"rId{max(ids, default=0) + 1}"

def add_rel(x, typ, target):
    rid = next_rid(x)
    x = x.replace("</Relationships>", f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/></Relationships>')
    return x, rid

os.makedirs(f"{P}/media", exist_ok=True)
# speaker icon used by PowerPoint for audio objects (from Bài 10)
shutil.copy(f"{REF}/ppt/media/image2.png", f"{P}/media/narr_icon.png")

# ---------- presentation order ----------
pres = open(f"{P}/presentation.xml", encoding="utf-8").read()
prels = open(f"{P}/_rels/presentation.xml.rels", encoding="utf-8").read()
rid2t = {}
for m in re.finditer(r'<Relationship [^>]*/>', prels):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(0)))
    rid2t[a["Id"]] = a["Target"]
order = [rid2t[r] for r in re.findall(r'<p:sldId [^>]*r:id="(rId\d+)"', pres)]

def strip_timing(x):
    x = re.sub(r'<mc:AlternateContent[^>]*>(?:(?!</mc:AlternateContent>).)*?<p:transition.*?</mc:AlternateContent>', '', x, flags=re.S)
    x = re.sub(r'<p:transition\b.*?(/>|</p:transition>)', '', x, flags=re.S)
    x = re.sub(r'<p:timing>.*?</p:timing>', '', x, flags=re.S)
    return x

def transition(adv_ms):
    adv = f' advTm="{adv_ms}"' if adv_ms else ''
    return ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
            '<mc:Choice xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" Requires="p14">'
            f'<p:transition spd="slow" p14:dur="2000"{adv}><p:fade/></p:transition></mc:Choice>'
            f'<mc:Fallback><p:transition spd="slow"{adv}><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')

def timing(spid):
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            '<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
            '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            '<p:par><p:cTn id="5" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="afterEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="6" dur="1" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>'
            '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
            '<p:audio isNarration="1"><p:cMediaNode vol="80000" showWhenStopped="0"><p:cTn id="7" fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>'
            '<p:endCondLst><p:cond evt="onStopAudio" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:endCondLst></p:cTn>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cMediaNode></p:audio></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')

def audio_pic(spid, r_link, r_embed, r_icon):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{spid}" name="Narration {spid}"><a:hlinkClick r:id="" action="ppaction://media"/></p:cNvPr>'
            '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
            f'<p:nvPr><a:audioFile r:link="{r_link}"/><p:extLst><p:ext uri="{{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}}">'
            f'<p14:media xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" r:embed="{r_embed}"/></p:ext></p:extLst></p:nvPr></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{r_icon}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            '<p:spPr><a:xfrm><a:off x="11582400" y="6248400"/><a:ext cx="457200" cy="457200"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')

def place_timing(x, trans, tim):
    x = strip_timing(x)
    anchor = '</p:clrMapOvr>' if '</p:clrMapOvr>' in x else '</p:cSld>'
    return x.replace(anchor, anchor + trans + tim, 1)

narrated = 0
for i, target in enumerate(order, 1):
    spath = f"{P}/{target}"
    x = open(spath, encoding="utf-8").read()
    if str(i) not in durs:
        continue
    rpath = f"{P}/slides/_rels/{os.path.basename(target)}.rels"
    rx = rels_read(rpath)
    mname = f"narr_b{N}_s{i:02d}.m4a"
    shutil.copy(f"{AUD}/s{i:02d}.m4a", f"{P}/media/{mname}")
    rx, r_media = add_rel(rx, R_MEDIA, f"../media/{mname}")
    rx, r_aud = add_rel(rx, R_AUDIO, f"../media/{mname}")
    rx, r_icon = add_rel(rx, R_IMAGE, "../media/narr_icon.png")
    open(rpath, "w", encoding="utf-8").write(rx)
    spid = max([int(v) for v in re.findall(r'<p:cNvPr id="(\d+)"', x)] + [1]) + 1
    if 'xmlns:r=' not in x[:2000]:
        x = x.replace('<p:sld ', '<p:sld xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    x = x.replace('</p:spTree>', audio_pic(spid, r_aud, r_media, r_icon) + '</p:spTree>', 1)
    adv = int(round(durs[str(i)] * 1000)) + 30
    x = place_timing(x, transition(adv), timing(spid))
    open(spath, "w", encoding="utf-8").write(x)
    narrated += 1

# ---------- intro slide (copied from Bài 10 slide 1) ----------
ix = open(f"{REF}/ppt/slides/slide1.xml", encoding="utf-8").read()
irx = open(f"{REF}/ppt/slides/_rels/slide1.xml.rels", encoding="utf-8").read()
new_rels = []
for m in re.finditer(r'<Relationship [^>]*/>', irx):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(0)))
    t = a["Target"]
    if a["Type"] == R_LAYOUT:
        t = "../slideLayouts/slideLayout1.xml"     # use this deck's own first layout
    elif "media/" in t:
        src = f"{REF}/ppt/media/{os.path.basename(t)}"
        nm = "intro_" + os.path.basename(t)
        shutil.copy(src, f"{P}/media/{nm}")
        t = f"../media/{nm}"
    if a["Type"].endswith("/notesSlide"):
        continue
    extra = ' TargetMode="External"' if a.get("TargetMode") == "External" else ''
    new_rels.append(f'<Relationship Id="{a["Id"]}" Type="{a["Type"]}" Target="{t}"{extra}/>')
slides_present = [int(n) for n in re.findall(r'slide(\d+)\.xml$', "\n".join(os.listdir(f"{P}/slides")), re.M)]
newno = max(slides_present) + 1
open(f"{P}/slides/slide{newno}.xml", "w", encoding="utf-8").write(ix)
open(f"{P}/slides/_rels/slide{newno}.xml.rels", "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    + "".join(new_rels) + "</Relationships>")
prels, r_new = add_rel(prels, R_SLIDE, f"slides/slide{newno}.xml")
open(f"{P}/_rels/presentation.xml.rels", "w", encoding="utf-8").write(prels)
maxid = max(int(v) for v in re.findall(r'<p:sldId id="(\d+)"', pres))
pres = re.sub(r'(<p:sldIdLst>)', rf'\1<p:sldId id="{maxid + 1}" r:id="{r_new}"/>', pres, 1)
open(f"{P}/presentation.xml", "w", encoding="utf-8").write(pres)

# ---------- content types ----------
ct = open(f"{TMP}/[Content_Types].xml", encoding="utf-8").read()
for ext, mime in [("m4a", "audio/mp4"), ("mp4", "video/mp4"), ("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg")]:
    if f'Extension="{ext}"' not in ct:
        ct = ct.replace("<Default ", f'<Default Extension="{ext}" ContentType="{mime}"/><Default ', 1)
ct = ct.replace("</Types>", f'<Override PartName="/ppt/slides/slide{newno}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>')
open(f"{TMP}/[Content_Types].xml", "w", encoding="utf-8").write(ct)

# ---------- zip ----------
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(f"{TMP}/[Content_Types].xml", "[Content_Types].xml")
    for root, _, files in os.walk(TMP):
        for f in files:
            full = os.path.join(root, f); arc = os.path.relpath(full, TMP)
            if arc == "[Content_Types].xml": continue
            comp = zipfile.ZIP_STORED if f.endswith((".m4a", ".mp4", ".jpg", ".png")) else zipfile.ZIP_DEFLATED
            z.write(full, arc, compress_type=comp)
print(OUT, "narrated slides:", narrated, "size MB:", round(os.path.getsize(OUT) / 1e6, 1),
      "audio min:", round(sum(durs.values()) / 60, 1))
