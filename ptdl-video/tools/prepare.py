"""Set up a work dir on any machine (Windows/Linux): lesson pptx from Drive (public links), unzipped
sources for build_pptx.py, Bài 10 template, scripts and the Manus reference voice.
usage: python prepare.py <work_dir>      (run from the repo root)
"""
import os, shutil, sys, urllib.request, zipfile
W = sys.argv[1]; R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = {1: "18kA19efnc_BNywltwLEgNipqzaCPt4Qh", 3: "1feNkvUQGD0lUUgoSHirwcSX4HASMo_ho", 4: "16teRGfmDSlJ-D8HCvleWryzrkvUmQeQL",
       5: "1BugIwVlBFwKGUS6hSCp2RNFMXJOR5cox", 6: "1GO_VmBN3UgpS5_j2vGE0oFUcRq7h-cB-", 7: "1RKUveehJaxbYkFTnvvm8Hrtx8HMg71uQ",
       8: "1huJGm6XzFMevy-OqqUBdEW0liy9D7wkm", 10: "12rw23i6yJtXsnpyDn_vvnDyb6mCKDb8h"}
URL = "https://drive.usercontent.google.com/download?id={}&export=download&confirm=t"
os.makedirs(f"{W}/gv/src", exist_ok=True); os.makedirs(f"{W}/out", exist_ok=True)
for n, i in IDS.items():
    p = f"{W}/gv/src/b{n}.pptx"
    if not os.path.exists(p):
        print("download", n, flush=True); urllib.request.urlretrieve(URL.format(i), p)
    d = f"{W}/gv/b10" if n == 10 else f"{W}/gv/src/x{n}"
    if not os.path.isdir(d): zipfile.ZipFile(p).extractall(d)
shutil.copytree(f"{R}/ptdl-video/scripts", f"{W}/scripts", dirs_exist_ok=True)
os.makedirs(f"{W}/manus", exist_ok=True)
for f in ("ref.wav", "ref48.wav"): shutil.copy(f"{R}/ptdl-video/voice_ref/{f}", f"{W}/manus/{f}")
print("ready:", W)
