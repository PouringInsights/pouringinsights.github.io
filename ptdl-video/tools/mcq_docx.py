"""Render bN_mcq_final.json to docx in the layout of the lecturer's Bài 9 quiz file, then PDF via LibreOffice.
usage: mcq_docx.py <scripts_dir> <out_dir>
"""
import json, os, subprocess, sys
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

D, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
FONT = "Times New Roman"
COLS = [("STT", 1.3), ("Mã câu hỏi", 2.2), ("Nội dung câu hỏi", 6.2), ("Độ khó", 1.8),
        ("Các phương án trả lời", 6.6), ("Đáp án", 1.5), ("Phản hồi", 6.6)]

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr(); s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hexcolor); tcPr.append(s)

def para(cell_or_doc, text, bold=False, size=11, align=None, first=False):
    p = cell_or_doc.paragraphs[0] if first and cell_or_doc.paragraphs and not cell_or_doc.paragraphs[0].text else cell_or_doc.add_paragraph()
    r = p.add_run(text); r.bold = bold; r.font.size = Pt(size); r.font.name = FONT
    r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    if align is not None: p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    return p

def repeat_header(row):
    trPr = row._tr.get_or_add_trPr(); h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)

for n in [1, 3, 4, 5, 6, 7, 8]:
    qs = json.load(open(f"{D}/b{n}_mcq_final.json", encoding="utf-8"))
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE; sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
    for m in ("left_margin", "right_margin"): setattr(sec, m, Cm(1.5))
    sec.top_margin = sec.bottom_margin = Cm(1.5)
    st = doc.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    # header like the template: school left, course right
    hp = sec.header.paragraphs[0]; hp.text = ""
    r = hp.add_run("Trường Kinh tế, Đại học Công nghiệp Hà Nội\tPhân tích dữ liệu Marketing"); r.font.size = Pt(10); r.font.name = FONT
    hp.style = doc.styles['Normal']
    for ts in list(hp.paragraph_format.tab_stops): pass
    hp.paragraph_format.tab_stops.add_tab_stop(Cm(26.7), WD_TAB_ALIGNMENT.RIGHT)
    # page number footer
    fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for t, v in (("begin", None), (None, "PAGE"), ("end", None)):
        if t: el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), t)
        else: el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = v
        rr = fp.add_run(); rr._r.append(el)

    para(doc, f"CÂU HỎI TRẮC NGHIỆM BÀI {n}", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, first=True)
    para(doc, "Tên học phần: Phân tích dữ liệu Marketing", size=12)
    para(doc, "Giảng viên biên soạn: ThS. Nguyễn Bình Minh An", size=12)
    doc.add_paragraph()
    t = doc.add_table(rows=1, cols=len(COLS)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    tblPr = t._tbl.tblPr; lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    grid = t._tbl.tblGrid
    for gc, (_, w) in zip(grid.findall(qn("w:gridCol")), COLS): gc.set(qn("w:w"), str(int(w / 2.54 * 1440)))
    for i, (h, w) in enumerate(COLS):
        c = t.rows[0].cells[i]; c.width = Cm(w); shade(c, "D9E2F3")
        para(c, h, bold=True, size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, first=True)
    repeat_header(t.rows[0])
    for k, q in enumerate(qs, 1):
        cells = t.add_row().cells
        opts = "; ".join(f"{L}. {q[L]}" for L in "ABCD")
        fb = f"Đáp án đúng là: {q['dap_an']}. Vì: {q['vi'].rstrip('.')}. Tham khảo: Bài {n}, mục {q['muc']}."
        vals = [str(k), q["ma"], q["cau_hoi"], q["do_kho"], None, q["dap_an"], fb]
        for i, (v, (_, w)) in enumerate(zip(vals, COLS)):
            cells[i].width = Cm(w)
            if i == 4:
                for j, L in enumerate("ABCD"):
                    para(cells[i], f"{L}. {q[L]}" + (";" if L != "D" else ""), size=10.5, first=(j == 0))
            else:
                al = WD_ALIGN_PARAGRAPH.CENTER if i in (0, 1, 3, 5) else None
                para(cells[i], v, size=10.5, align=al, first=True, bold=(i == 5))
    path = f"{OUT}/Bai_{n}_Cau_hoi_trac_nghiem.docx"; doc.save(path); print(path)
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", OUT] +
               [f"{OUT}/Bai_{n}_Cau_hoi_trac_nghiem.docx" for n in [1, 3, 4, 5, 6, 7, 8]],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
print("pdf done")
