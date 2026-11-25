"""Format kits that reuse the exact formatting of Bài 8's ĐCBG (docx) and slide deck (pptx).

ĐCBG:
    from kits import Dcbg
    d = Dcbg()                         # template = Bài 8 ĐCBG, body cleared
    d.title("BÀI 13:", "PHÂN TÍCH ...")  # big centered title lines
    d.h1("13.1. ..."); d.h2("13.1.1. ...")
    d.para("Đoạn văn ..."); d.bullet("Ý gạch đầu dòng")
    d.caption("Bảng 13.1. ..."); d.table([["Cột 1","Cột 2"],["a","b"]])
    d.example("Ví dụ 13.1. ...");  d.plain_heading("Tóm tắt bài học")  # also "CÂU HỎI ÔN TẬP", "TÀI LIỆU THAM KHẢO"
    d.save("out.docx")

Slides:
    from kits import Deck
    k = Deck()                                     # template = Bài 8 deck (HaUI theme)
    k.cover("Tiêu đề bài", "Phân tích dữ liệu Marketing – Bài 13")
    k.section("13.1.  Tên mục")
    k.bullets("Tiêu đề slide", ["Ý 1", "Ý 2", ...])           # ≤ 7 ý, mỗi ý ≤ 25 từ
    k.table("Tiêu đề slide", [["H1","H2"],["a","b"]], note="câu kết (tuỳ chọn)")
    k.save("out.pptx")
"""
import copy, os, re
from docx import Document
from pptx import Presentation
from pptx.util import Pt

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
DOCX_T = f"{W}/dcbg/b8.docx"
PPTX_T = f"{W}/gv/src/b8.pptx"
WNS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


# ------------------------------------------------------------------ ĐCBG (docx)
class Dcbg:
    # element indices of exemplars in the Bài 8 template body
    EX = dict(title1=0, title2=1, h1=6, h2=7, body=8, caption=17, example=27, plain=181)

    def __init__(self, template=DOCX_T):
        self.doc = Document(template)
        body = self.doc.element.body
        els = list(body.iterchildren())
        self.ex = {k: copy.deepcopy(els[i]) for k, i in self.EX.items()}
        self.ex["bullet"] = next(copy.deepcopy(e) for e in els if e.tag == WNS + "p" and e.find(".//" + WNS + "numPr") is not None)
        self.ex["table"] = copy.deepcopy([e for e in els if e.tag == WNS + "tbl"][1])  # [0] is the one-cell "Mục tiêu" box
        self.sect = body.find(WNS + "sectPr")
        for e in els:
            if e is not self.sect: body.remove(e)
        self.body = body

    def _add(self, el):
        self.body.insert(list(self.body).index(self.sect), el); return el

    def _para(self, key, text):
        p = copy.deepcopy(self.ex[key])
        runs = p.findall(".//" + WNS + "r")
        for r in runs[1:]: r.getparent().remove(r)
        if not runs:
            return self._add(p)
        r0 = runs[0]
        for t in r0.findall(WNS + "t"): r0.remove(t)
        for extra in r0.findall(WNS + "tab") + r0.findall(WNS + "br"): r0.remove(extra)
        t = r0.makeelement(WNS + "t", {}); t.text = text
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve"); r0.append(t)
        # drop hyperlinks/fields leftovers
        for h in p.findall(WNS + "hyperlink"): p.remove(h)
        return self._add(p)

    def title(self, *lines):
        for i, l in enumerate(lines): self._para("title1" if i == 0 else "title2", l)
    def h1(self, t): self._para("h1", t)
    def h2(self, t): self._para("h2", t)
    def para(self, t): self._para("body", t)
    def bullet(self, t): self._para("bullet", t)
    def caption(self, t): self._para("caption", t)
    def example(self, t): self._para("example", t)
    def plain_heading(self, t): self._para("plain", t)

    def table(self, rows):
        tbl = copy.deepcopy(self.ex["table"])
        trs = tbl.findall(WNS + "tr")
        head_tr, body_tr = trs[0], (trs[1] if len(trs) > 1 else trs[0])
        for tr in trs: tbl.remove(tr)
        ncol = len(rows[0])
        grid = tbl.find(WNS + "tblGrid")
        if grid is not None:
            cols = grid.findall(WNS + "gridCol")
            total = sum(int(c.get(WNS + "w", "0")) for c in cols) or 9000
            for c in cols: grid.remove(c)
            for _ in range(ncol):
                g = grid.makeelement(WNS + "gridCol", {}); g.set(WNS + "w", str(total // ncol)); grid.append(g)
        for ri, row in enumerate(rows):
            tr = copy.deepcopy(head_tr if ri == 0 else body_tr)
            tcs = tr.findall(WNS + "tc")
            proto = tcs[0]
            for tc in tcs: tr.remove(tc)
            for val in row:
                tc = copy.deepcopy(proto)
                w = tc.find(".//" + WNS + "tcW")
                if w is not None and grid is not None: w.set(WNS + "w", str(total // ncol)); w.set(WNS + "type", "dxa")
                gs = tc.find(".//" + WNS + "gridSpan")
                if gs is not None: gs.getparent().remove(gs)
                ps = tc.findall(WNS + "p")
                for p in ps[1:]: tc.remove(p)
                p = ps[0]
                runs = p.findall(".//" + WNS + "r")
                for r in runs[1:]: r.getparent().remove(r)
                if runs:
                    r0 = runs[0]
                    for t in r0.findall(WNS + "t"): r0.remove(t)
                else:
                    r0 = p.makeelement(WNS + "r", {}); p.append(r0)
                t = r0.makeelement(WNS + "t", {}); t.text = str(val)
                t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve"); r0.append(t)
                tr.append(tc)
            tbl.append(tr)
        self._add(tbl)

    def save(self, path): self.doc.save(path)


# ------------------------------------------------------------------ Slides (pptx)
class Deck:
    """Clones exemplar slides of the Bài 8 deck and replaces their text."""
    EX = dict(cover=1, section=6, text=15, table=14)

    def __init__(self, template=PPTX_T):
        self.prs = Presentation(template)
        self.src = {k: self.prs.slides[i - 1] for k, i in self.EX.items()}
        self.n_template = len(self.prs.slides)

    def _clone(self, key):
        src = self.src[key]
        s = self.prs.slides.add_slide(src.slide_layout)
        for ph in list(s.placeholders): ph._element.getparent().remove(ph._element)
        for sh in src.shapes: s.shapes._spTree.append(copy.deepcopy(sh._element))
        for rel in src.part.rels.values():
            if "image" in rel.reltype or "media" in rel.reltype:
                s.part.rels.get_or_add(rel.reltype, rel._target)
        # keep rIds consistent: re-point blips to same rId names
        for blip in s.shapes._spTree.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"):
            old = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
            if old and old in src.part.rels:
                blip.set("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed",
                         s.part.relate_to(src.part.rels[old]._target, src.part.rels[old].reltype))
        bg = src._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}cSld/{http://schemas.openxmlformats.org/presentationml/2006/main}bg")
        if bg is not None:
            s._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}cSld").insert(0, copy.deepcopy(bg))
        return s

    @staticmethod
    def _text_shapes(s):
        return [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]

    @staticmethod
    def _set(tf, lines):
        if isinstance(lines, str): lines = [lines]
        paras = tf.paragraphs
        proto = copy.deepcopy(paras[min(1, len(paras) - 1)]._p) if len(paras) > 1 else copy.deepcopy(paras[0]._p)
        first = copy.deepcopy(paras[0]._p)
        for p in list(paras): p._p.getparent().remove(p._p)
        txBody = tf._txBody
        for i, line in enumerate(lines):
            p = copy.deepcopy(first if i == 0 else proto)
            rs = p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r")
            for r in rs[1:]: p.remove(r)
            for f in p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}fld"): p.remove(f)
            if rs:
                rs[0].find("{http://schemas.openxmlformats.org/drawingml/2006/main}t").text = line
            else:
                r = p.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}r", {})
                t = r.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}t", {}); t.text = line; r.append(t)
                p.append(r)
            txBody.append(p)

    def cover(self, title, subtitle, lecturer="Giảng viên: Nguyễn Bình Minh An"):
        s = self._clone("cover"); ts = self._text_shapes(s)
        self._set(ts[0].text_frame, title)
        if len(ts) > 1: self._set(ts[1].text_frame, subtitle)
        if len(ts) > 2: self._set(ts[2].text_frame, lecturer)
        return s

    def section(self, title):
        s = self._clone("section"); self._set(self._text_shapes(s)[0].text_frame, title); return s

    def bullets(self, title, items):
        s = self._clone("text"); ts = self._text_shapes(s)
        self._set(ts[0].text_frame, title)
        body = max(ts[1:], key=lambda sh: sh.width * sh.height) if len(ts) > 1 else None
        for sh in ts[1:]:
            if sh is not body: sh._element.getparent().remove(sh._element)
        if body is not None: self._set(body.text_frame, ["▪  " + x if not x.startswith("▪") else x for x in items])
        return s

    def table(self, title, rows, note=None):
        s = self._clone("table")
        tshape = next(sh for sh in s.shapes if sh.has_table)
        ts = [sh for sh in self._text_shapes(s)]
        title_sh = min(ts, key=lambda sh: sh.top) if ts else None
        if title_sh is not None: self._set(title_sh.text_frame, title)
        others = [sh for sh in ts if sh is not title_sh]
        for sh in others[1:]: sh._element.getparent().remove(sh._element)
        if others:
            if note: self._set(others[0].text_frame, note)
            else: others[0]._element.getparent().remove(others[0]._element)
        # rebuild table grid to rows x cols
        tbl = tshape.table
        A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
        tblx = tbl._tbl
        grid = tblx.find(A + "tblGrid"); gcols = grid.findall(A + "gridCol")
        width = sum(int(g.get("w")) for g in gcols); ncol = len(rows[0])
        for g in gcols: grid.remove(g)
        for _ in range(ncol):
            g = grid.makeelement(A + "gridCol", {}); g.set("w", str(width // ncol)); grid.append(g)
        trs = tblx.findall(A + "tr"); head, bodyr = trs[0], trs[1] if len(trs) > 1 else trs[0]
        for tr in trs: tblx.remove(tr)
        for ri, row in enumerate(rows):
            tr = copy.deepcopy(head if ri == 0 else bodyr)
            tcs = tr.findall(A + "tc"); proto = tcs[0]
            for tc in tcs: tr.remove(tc)
            for v in row:
                tc = copy.deepcopy(proto)
                for k in ("gridSpan", "hMerge", "rowSpan", "vMerge"):
                    if tc.get(k): del tc.attrib[k]
                txb = tc.find(A + "txBody"); ps = txb.findall(A + "p")
                for p in ps[1:]: txb.remove(p)
                p = ps[0]; rs = p.findall(A + "r")
                for r in rs[1:]: p.remove(r)
                if rs: rs[0].find(A + "t").text = str(v)
                else:
                    r = p.makeelement(A + "r", {}); t = r.makeelement(A + "t", {}); t.text = str(v); r.append(t); p.append(r)
                tr.append(tc)
            tblx.append(tr)
        return s

    def save(self, path):
        # drop the template's original slides
        sldIdLst = self.prs.slides._sldIdLst
        for sid in list(sldIdLst)[: self.n_template]:
            self.prs.part.drop_rel(sid.rId); sldIdLst.remove(sid)
        self.prs.save(path)
