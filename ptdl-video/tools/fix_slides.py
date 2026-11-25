"""Apply text fixes to unzipped lesson pptx sources (paragraph-level, works across split runs).
usage: fix_slides.py <src_root>   (src_root contains x1, x3, ... unzipped decks)
Each fix: (deck, part_glob, old, new). Prints every replacement; fails if an expected fix finds nothing.
"""
import glob, html, re, sys
R = sys.argv[1]
FIXES = [
    # Bài 1
    ("x1", "slides/*.xml", "độ tin cậu", "độ tin cậy"),
    ("x1", "slides/slide7.xml", "Marketing truyền thống", "Marketing truyền thống (EBM)"),
    ("x1", "slides/slide8.xml", "Tuy nhiên MDD đã biến", "Tuy nhiên marketing dựa trên dữ liệu (MDD) đã biến"),
    # Bài 3
    ("x3", "slides/slide3.xml", "3.3.2.  Mô hình RFM", "3.1.2.  Mô hình RFM"),
    ("x3", "slides/*.xml", "Mô hình RFM – phân khúc khách hàng theo hành vi giao dịch@TITLE7", None),
    ("x3", "slides/slide11.xml", "(R1-F3-M3)", "(R1-F4-M4)"),
    ("x3", "slides/slide4.xml", "Năm 2018, Netflix công bố", "Năm 2017, Netflix công bố"),
    # Bài 4
    ("x4", "slides/slide28.xml", "số mức của mỗi mức", "số mức của mỗi thuộc tính"),
    ("x4", "notesSlides/*.xml", "điểm bang quan", "điểm bàng quan"),
    ("x4", "slides/slide37.xml", "4.3.2. Định giá phân biệt", "4.3.3. Định giá phân biệt"),
    ("x4", "slides/slide38.xml", "4.3.3. Quy trình tích hợp", "4.3.4. Quy trình tích hợp"),
    ("x4", "notesSlides/notesSlide9.xml", "Conjoint (Compositional / Preference)", "Conjoint (Decompositional / Preference)"),
    # Bài 5: Pareto/NBD là của Schmittlein, Morrison & Colombo (1987)
    ("x5", "slides/slide13.xml", "Pareto/NBD và BG/NBD (Fader, Hardie & Lee, 2005)", "Pareto/NBD (Schmittlein và cộng sự, 1987) và BG/NBD (Fader, Hardie & Lee, 2005)"),
    # Bài 7: 3,38 × 0,25 = 0,845 ≈ 0,85
    ("x7", "slides/slide12.xml", "Facebook cũng chỉ 0,84.", "Facebook cũng chỉ 0,85."),
    # Bài 6
    ("x6", "slides/slide5.xml", "SmartPLS, AMOS, R (gói lavaan)", "AMOS, R (gói lavaan), Mplus"),
    # Bài 8: thống nhất ngưỡng theo Hair et al. (α, CR ≥ 0,70; AVE ≥ 0,50)
    ("x8", "slides/slide30.xml", "@CELL> 0,70", "≥ 0,70"),
    ("x8", "slides/slide34.xml", "@CELL> 0,70", "≥ 0,70"),
    ("x8", "slides/slide30.xml", "@CELL> 0,50", "≥ 0,50"),
]
P = re.compile(r'<a:p\b.*?</a:p>', re.S)
T = re.compile(r'(<a:t(?:\s[^>]*)?>)(.*?)(</a:t>)', re.S)

def fix_para(px, old, new):
    runs = list(T.finditer(px))
    texts = [html.unescape(m.group(2)) for m in runs]
    full = "".join(texts)
    i = full.find(old)
    if i < 0: return px, 0
    j = i + len(old)
    out, pos, done = [], 0, False
    for m, t in zip(runs, texts):
        a, b = pos, pos + len(t); pos = b
        if b <= i or a >= j: nt = t
        elif not done:
            nt = t[:max(i - a, 0)] + new + (t[j - a:] if j <= b else ""); done = True
        else:
            nt = t[j - a:] if j < b else ""
        out.append((m, nt))
    res, last = [], 0
    for m, nt in out:
        res.append(px[last:m.start(2)]); res.append(html.escape(nt, quote=False)); last = m.end(2)
    res.append(px[last:])
    return "".join(res), 1

total = 0
for deck, pat, old, new in FIXES:
    n = 0
    for f in sorted(glob.glob(f"{R}/{deck}/ppt/{pat}")):
        x = open(f, encoding="utf-8").read(); orig = x
        if old.endswith("@TITLE7"):      # add section number to the RFM section title slide (slide7)
            if not f.endswith("/slide7.xml"): continue
            base = old[:-7]
            x, k = P.sub(lambda m: fix_para(m.group(0), base, "3.1.2.  " + base)[0] if "3.1.2." not in m.group(0) else m.group(0), x), 0
            n += x != orig
        elif old.startswith("@CELL"):    # whole-cell exact match only
            o = old[5:]
            x = x.replace(f">{html.escape(o, quote=False)}</a:t>", f">{html.escape(new, quote=False)}</a:t>")
            n += orig.count(f">{html.escape(o, quote=False)}</a:t>")
        else:
            def rep(m):
                nonlocal_n[0] += 0
                return m.group(0)
            paras = []
            last = 0; cnt = 0
            for m in P.finditer(x):
                np_, c = fix_para(m.group(0), old, new); cnt += c
                paras.append(x[last:m.start()]); paras.append(np_); last = m.end()
            paras.append(x[last:]); x = "".join(paras); n += cnt
        if x != orig:
            open(f, "w", encoding="utf-8").write(x)
            print(f"{deck} {f.split('/ppt/')[1]}: '{old}' -> '{new}'")
    total += n
    if n == 0: print(f"!! not found: {deck} {pat} '{old}'")
print("total fixes", total)
