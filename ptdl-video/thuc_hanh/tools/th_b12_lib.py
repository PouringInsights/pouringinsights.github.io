"""Small extensions of kits.Dcbg/Deck for the practice lessons: Mục tiêu box, dot bullets, restartable reference list,
column widths, keep-with-next for captions, note placement under slide tables."""
import copy, sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
from kits import Dcbg, Deck, DOCX_T, WNS
from docx import Document

XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def set_text(p, text):
    runs = p.findall(".//" + WNS + "r")
    for r in runs[1:]:
        r.getparent().remove(r)
    if not runs:
        r0 = p.makeelement(WNS + "r", {}); p.append(r0)
    else:
        r0 = runs[0]
    for t in r0.findall(WNS + "t") + r0.findall(WNS + "tab") + r0.findall(WNS + "br"):
        r0.remove(t)
    t = r0.makeelement(WNS + "t", {}); t.text = text; t.set(XML_SPACE, "preserve"); r0.append(t)
    return p


class D(Dcbg):
    def __init__(self):
        super().__init__()
        src = Document(DOCX_T)
        els = list(src.element.body.iterchildren())
        self.box, self.blank, self.stars = (copy.deepcopy(els[i]) for i in (3, 4, 5))
        num = self.doc.part.numbering_part.element
        absmap = {n.get(WNS + "numId"): n.find(WNS + "abstractNumId").get(WNS + "val") for n in num.findall(WNS + "num")}
        abstracts = num.findall(WNS + "abstractNum")
        ids = [int(a.get(WNS + "abstractNumId")) for a in abstracts]
        nids = [int(n.get(WNS + "numId")) for n in num.findall(WNS + "num")]
        # bullet abstract cloned from the numbered list of numId 3
        a3 = next(a for a in abstracts if a.get(WNS + "abstractNumId") == absmap["3"])
        ab = copy.deepcopy(a3); new_a = max(ids) + 1
        ab.set(WNS + "abstractNumId", str(new_a))
        ns = ab.find(WNS + "nsid")
        if ns is not None: ns.set(WNS + "val", "%08X" % random.getrandbits(32))
        for lvl in ab.findall(WNS + "lvl"):
            lvl.find(WNS + "numFmt").set(WNS + "val", "bullet")
            lvl.find(WNS + "lvlText").set(WNS + "val", "•")
        abstracts[-1].addnext(ab)
        self.bul_id = str(max(nids) + 1); self.ref_id = str(max(nids) + 2)
        n1 = num.makeelement(WNS + "num", {WNS + "numId": self.bul_id})
        x = n1.makeelement(WNS + "abstractNumId", {WNS + "val": str(new_a)}); n1.append(x); num.append(n1)
        n2 = num.makeelement(WNS + "num", {WNS + "numId": self.ref_id})
        x = n2.makeelement(WNS + "abstractNumId", {WNS + "val": absmap["4"]}); n2.append(x)
        lo = n2.makeelement(WNS + "lvlOverride", {WNS + "ilvl": "0"})
        so = lo.makeelement(WNS + "startOverride", {WNS + "val": "1"}); lo.append(so); n2.append(lo)
        num.append(n2)

    def _numbered(self, text, nid):
        p = self._para("bullet", text)
        p.find(".//" + WNS + "numId").set(WNS + "val", nid)
        return p

    def dot(self, t): return self._numbered(t, self.bul_id)
    def ref(self, t): return self._numbered(t, self.ref_id)

    def objectives(self, intro, items):
        box = copy.deepcopy(self.box)
        tc = box.find(".//" + WNS + "tc")
        ps = tc.findall(WNS + "p")
        head, intro_p, proto = ps[0], ps[1], ps[2]
        for p in ps[2:]: tc.remove(p)
        set_text(intro_p, intro)
        for it in items:
            tc.append(set_text(copy.deepcopy(proto), it))
        self._add(box); self._add(copy.deepcopy(self.blank)); self._add(copy.deepcopy(self.stars))


class K(Deck):
    A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

    def table(self, title, rows, note=None, widths=None):
        import re
        s = super().table(title, rows, note)
        tshape = next(sh for sh in s.shapes if sh.has_table)
        tbl = tshape.table._tbl; A = self.A
        if widths:
            grid = tbl.find(A + "tblGrid"); gcs = grid.findall(A + "gridCol")
            total = sum(int(g.get("w")) for g in gcs)
            for g, w in zip(gcs, widths): g.set("w", str(int(total * w / sum(widths))))
        # numbers right-aligned (body rows only)
        for ri, tr in enumerate(tbl.findall(A + "tr")):
            if ri == 0: continue
            for tc in tr.findall(A + "tc"):
                txt = "".join(t.text or "" for t in tc.iter(A + "t")).strip()
                if re.fullmatch(r"[≈\d][\d.,\s%]*(tr|tr/năm|đồng)?(/năm)?", txt):
                    for p in tc.iter(A + "p"):
                        ppr = p.find(A + "pPr")
                        if ppr is None:
                            ppr = p.makeelement(A + "pPr", {}); p.insert(0, ppr)
                        ppr.set("algn", "r")
        if note:
            others = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip() == note]
            th = sum(int(tr.get("h", "370840")) for tr in tbl.findall(A + "tr"))
            for sh in others:
                sh.top = tshape.top + th + 150000
                sh.height = 900000
        return s


def _keep_next(p):
    ppr = p.find(WNS + "pPr")
    if ppr is None:
        ppr = p.makeelement(WNS + "pPr", {}); p.insert(0, ppr)
    if ppr.find(WNS + "keepNext") is None:
        k = ppr.makeelement(WNS + "keepNext", {})
        ps = ppr.find(WNS + "pStyle")
        (ps.addnext(k) if ps is not None else ppr.insert(0, k))


class D2(D):
    """caption/example keep with next; tables accept relative column widths and get a spacer paragraph."""
    def caption(self, t): _keep_next(self._para("caption", t))
    def example(self, t): _keep_next(self._para("example", t))
    def h1(self, t): _keep_next(self._para("h1", t))
    def h2(self, t): _keep_next(self._para("h2", t))

    def table(self, rows, widths=None):
        super().table(rows)
        tbl = [e for e in self.body if e.tag == WNS + "tbl"][-1]
        grid = tbl.find(WNS + "tblGrid"); cols = grid.findall(WNS + "gridCol")
        total = sum(int(c.get(WNS + "w")) for c in cols)
        if widths:
            ws = [int(total * w / sum(widths)) for w in widths]
            for c, w in zip(cols, ws): c.set(WNS + "w", str(w))
            for tr in tbl.findall(WNS + "tr"):
                for tc, w in zip(tr.findall(WNS + "tc"), ws):
                    tw = tc.find(".//" + WNS + "tcW")
                    if tw is not None: tw.set(WNS + "w", str(w)); tw.set(WNS + "type", "dxa")
        # keep rows together across page where possible: mark all but last row paragraphs keepNext
        trs = tbl.findall(WNS + "tr")
        if len(trs) <= 5:
            for tr in trs[:-1]:
                for p in tr.iter(WNS + "p"): _keep_next(p)
        sp = copy.deepcopy(self.ex["body"])
        for r in sp.findall(".//" + WNS + "r"): r.getparent().remove(r)
        old = sp.find(WNS + "pPr")
        if old is not None: sp.remove(old)
        ppr = sp.makeelement(WNS + "pPr", {})
        ppr.append(ppr.makeelement(WNS + "spacing", {WNS + "before": "0", WNS + "after": "0", WNS + "line": "200", WNS + "lineRule": "auto"}))
        sp.insert(0, ppr)
        self._add(sp)
