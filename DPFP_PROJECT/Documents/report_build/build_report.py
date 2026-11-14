# -*- coding: utf-8 -*-
"""Builds Documents/DPFP_Project_Report_draft.docx from a copy of the college template.
Run from D:/DPFP_PROJECT:  python Documents/report_build/build_report.py <template.docx> <out.docx>"""
import sys, re, copy, shutil
from pathlib import Path
import openpyxl
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_TAB_ALIGNMENT, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

sys.path.insert(0, str(Path(__file__).parent))
import content as C

TEMPLATE, OUTFILE = sys.argv[1], sys.argv[2]
shutil.copy(TEMPLATE, OUTFILE)
doc = docx.Document(OUTFILE)
body = doc.element.body
EL = list(body.iterchildren())
P = {i: docx.text.paragraph.Paragraph(e, doc) for i, e in enumerate(EL) if e.tag == qn("w:p")}
FONT = "Calibri"
PH = re.compile(r"(\[[A-Z][A-Z0-9 ,/'().-]*\]|\[Edit this statement[^\]]*\]|\[Plagiarism report[^\]]*\])")


# ------------------------------------------------------------------ helpers
def set_font(run, size=None, bold=None, italic=None):
    run.font.name = FONT
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(k), FONT)
    for k in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(k)) is not None:
            del rf.attrib[qn(k)]
    if size: run.font.size = Pt(size)
    if bold is not None: run.font.bold = bold
    if italic is not None: run.font.italic = italic


def add_runs(p, text, proto_rpr=None, size=None, bold=None, italic=None):
    """Add text to p, yellow-highlighting [PLACEHOLDERS]."""
    for part in PH.split(text):
        if not part:
            continue
        r = p.add_run(part)
        if proto_rpr is not None:
            r._element.insert(0, copy.deepcopy(proto_rpr))
        set_font(r, size, bold, italic)
        r.font.highlight_color = WD_COLOR_INDEX.YELLOW if PH.fullmatch(part) else None
        if not PH.fullmatch(part):
            rpr = r._element.get_or_add_rPr(); h = rpr.find(qn("w:highlight"))
            if h is not None: rpr.remove(h)


def set_text(p, text, align=None, bold=None):
    proto = None
    if p.runs and p.runs[0]._element.rPr is not None:
        proto = copy.deepcopy(p.runs[0]._element.rPr)
    for r in list(p._element):
        if r.tag in (qn("w:r"), qn("w:hyperlink"), qn("w:bookmarkStart"), qn("w:bookmarkEnd")):
            if r.tag == qn("w:r"): p._element.remove(r)
    if proto is not None:
        h = proto.find(qn("w:highlight"))
        if h is not None: proto.remove(h)
    add_runs(p, text, proto, bold=bold)
    if align is not None: p.alignment = align
    pf = p.paragraph_format
    pf.first_line_indent = None


def delete(i):
    e = EL[i]
    if e.getparent() is not None: e.getparent().remove(e)


def page_break_before(p):
    p.paragraph_format.page_break_before = True


def tabs(p, positions):
    pf = p.paragraph_format
    pf.left_indent = Inches(0); pf.first_line_indent = Inches(0)
    for pos, al in positions:
        pf.tab_stops.add_tab_stop(Inches(pos), al)


# ------------------------------------------------------------------ front matter
T = C.TITLE
CEN = WD_ALIGN_PARAGRAPH.CENTER
set_text(P[6], T)
set_text(P[16], "APPLIED STATISTICS (DATA SCIENCE)", CEN)
set_text(P[19], "[STUDENT NAME]\t[PRN]"); tabs(P[19], [(1.9, WD_TAB_ALIGNMENT.CENTER)]); P[19].alignment = CEN
set_text(P[19], "[STUDENT NAME]     [PRN]", CEN)
set_text(P[26], "[GUIDE NAME]")
set_text(P[28], "[MONTH, YEAR]")
for i in (20, 31, 32): delete(i)
page_break_before(P[33])

set_text(P[37], "DEPARTMENT OF APPLIED SCIENCE & HUMANITIES", CEN)
_r = P[37].runs[-1]; _r.add_break(); _r2 = P[37].add_run("RAJBAUG, LONI KALBHOR, PUNE-412201"); _r2._element.insert(0, copy.deepcopy(_r._element.rPr))
set_text(P[36], "SCHOOL OF ENGINEERING & SCIENCE", CEN)
set_text(P[39], "This is to certify that the Research Project-[PROJECT CODE] entitled")
set_text(P[40], T)
set_text(P[42], "Submitted by")
set_text(P[43], "[STUDENT NAME]     [PRN]", CEN)
delete(44)
set_text(P[46], "is a bonafide work carried out by the student under the supervision of the guide, and it is "
                "submitted towards the partial fulfilment of the requirement of MIT Art, Design and Technology "
                "University, Pune for the award of the Master of Science in Applied Statistics (Data Science).",
         WD_ALIGN_PARAGRAPH.JUSTIFY)
two_col = [(1.8, WD_TAB_ALIGNMENT.CENTER), (5.4, WD_TAB_ALIGNMENT.CENTER)]
for i, txt in [(51, "\t[GUIDE NAME]\t[PROGRAM CO-ORDINATOR NAME]"), (52, "\tGuide\tProgram Co-ordinator"),
               (55, "\t[HOD NAME]\t[DEAN NAME]"), (56, "\tHOD,\tDean, Faculty of Engg. and Science,"),
               (57, "\tApplied Sciences & Humanities\tMIT School of Engineering & Science")]:
    set_text(P[i], txt, WD_ALIGN_PARAGRAPH.LEFT); tabs(P[i], two_col)
set_text(P[60], "Date:\tExternal Examiner", WD_ALIGN_PARAGRAPH.LEFT); tabs(P[60], [(5.4, WD_TAB_ALIGNMENT.CENTER)])
delete(62)
page_break_before(P[65])

set_text(P[67], f"I hereby declare that the project entitled \u201c{T}\u201d, submitted towards the partial fulfilment "
                "of the requirement of MIT-ADT University, Pune for the award of the Master of Science in Applied "
                "Statistics (Data Science), is a record of bonafide work carried out by me under the supervision of "
                "[GUIDE NAME], Department of Applied Science & Humanities, MIT School of Engineering & Science, Pune.")
set_text(P[68], "I further declare that the work reported in this report has not been submitted, and will not be "
                "submitted, either in part or in full, for the award of any other degree or diploma in this institute "
                "or any other institute or university.")
ai = copy.deepcopy(P[68]._element); P[68]._element.addnext(ai)
set_text(docx.text.paragraph.Paragraph(ai, doc), C.DECLARATION_AI)
set_text(P[71], "Place: Pune", WD_ALIGN_PARAGRAPH.LEFT)
set_text(P[72], "Student's Name and Signature", WD_ALIGN_PARAGRAPH.RIGHT)
set_text(P[73], "\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026", WD_ALIGN_PARAGRAPH.RIGHT)
set_text(P[74], "([STUDENT NAME])", WD_ALIGN_PARAGRAPH.RIGHT)
for i in (69, 70, 75, 76, 77, 78, 79, 80): delete(i)
page_break_before(P[81])

set_text(P[84], "I thank all the teaching and non-teaching staff of the Department of Applied Science & Humanities "
                "and my classmates. I am grateful to my guide, [GUIDE NAME], for guidance throughout this project. "
                "I also thank [HOD NAME], Head of the Department of Applied Science & Humanities, MIT Art, Design and "
                "Technology University, Pune, for providing the necessary facilities. Finally, I thank Open-Meteo "
                "and the Copernicus Atmosphere Monitoring Service for making the air-quality data freely available.",
         WD_ALIGN_PARAGRAPH.JUSTIFY)
set_text(P[87], "[STUDENT NAME]", WD_ALIGN_PARAGRAPH.RIGHT)
for i in (88, 100): delete(i)
set_text(P[101], "ABSTRACT", CEN); page_break_before(P[101])
for i, txt in zip((102, 103, 104), C.ABSTRACT):
    set_text(P[i], txt, WD_ALIGN_PARAGRAPH.JUSTIFY)
for i in (105, 106, 107): delete(i)
set_text(P[109], C.KEYWORDS, WD_ALIGN_PARAGRAPH.JUSTIFY); P[108].paragraph_format.keep_with_next = True
for i in range(110, 122): delete(i)
page_break_before(P[122])

# ------------------------------------------------------------------ index table
tbl = doc.tables[0]


def cell_lines(cell, lines):
    ps = cell.paragraphs
    for extra in ps[1:]:
        extra._element.getparent().remove(extra._element)
    first = cell.paragraphs[0]
    set_text(first, lines[0])
    prev = first._element
    for ln in lines[1:]:
        e = copy.deepcopy(first._element); prev.addnext(e); prev = e
        set_text(docx.text.paragraph.Paragraph(e, doc), ln)
    for cp in cell.paragraphs:
        cp.paragraph_format.space_after = Pt(2); cp.paragraph_format.space_before = Pt(0); cp.paragraph_format.line_spacing = 1.0


lof_row = copy.deepcopy(tbl.rows[4]._tr); tbl.rows[4]._tr.addnext(lof_row)
rows = tbl.rows
front = ["TITLE PAGE", "CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "LIST OF FIGURES AND TABLES"]
for r, name in zip(rows[:6], front):
    cell_lines(r.cells[1], [name]); cell_lines(r.cells[2], ["#"])
chap = [("Chapter-I", ["Introduction"]), ("Chapter-II", ["Literature Review"]), ("Chapter-III", ["Objectives of the Study"]),
        ("Chapter-IV", ["Methodology", "4.1. Data Description", "4.2. Computational Tools", "4.3. Data Pre-processing and Validation",
                        "4.4. Feature Engineering", "4.5. Exploratory Analysis and Chronological Split"]),
        ("Chapter-V", ["Analysis and Result", "5.1. Leakage-Free Setup and Leakage Demonstration", "5.2. Model and Imbalance Selection",
                       "5.3. Probability Calibration", "5.4. Baselines and Data-vs-Infrastructure Ablation",
                       "5.5. Operating Point", "5.6. Lead Time and 3-Day Outlook", "5.7. Per-Failure-Type Predictability Map",
                       "5.8. Cross-City Test", "5.9. Explainability", "5.10. The Deployed System"]),
        ("Chapter-VI", ["Result and Discussion"]), ("Chapter-VII", ["Limitation and Future Scope"]), ("Chapter-VIII", ["References"])]
for r, (lab, lines) in zip(rows[6:14], chap):
    cell_lines(r.cells[0], [lab]); cell_lines(r.cells[1], lines); cell_lines(r.cells[2], ["#"])
cell_lines(rows[14].cells[0], ["Annexures"])
cell_lines(rows[14].cells[1], ["A. Repository and Dashboard Links", "B. Dashboard Screenshots", "C. Sample of forecast_log.csv", "D. Plagiarism Report"])
for cp in rows[14].cells[1].paragraphs:
    pPr = cp._element.pPr
    if pPr is not None and pPr.find(qn("w:numPr")) is not None: pPr.remove(pPr.find(qn("w:numPr")))
    cp.paragraph_format.left_indent = Inches(0.1)
cell_lines(rows[14].cells[2], ["#"])

# fonts and highlights across the front matter
for p in doc.paragraphs:
    for r in p.runs:
        set_font(r)
        if not PH.fullmatch(r.text or "") and r.font.highlight_color is not None and "[" not in (r.text or ""):
            r.font.highlight_color = None
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs: set_font(r)
for sname in ("Normal", "Heading 1", "Heading 2", "Heading 3"):
    st = doc.styles[sname]; st.font.name = FONT
    rpr = st.element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
    if rf is None: rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(qn(k), FONT)
    for k in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(k)) is not None: del rf.attrib[qn(k)]
    st.font.color.rgb = RGBColor(0, 0, 0)

# ------------------------------------------------------------------ citations (IEEE, order of first appearance)
wb = openpyxl.load_workbook(C.PAPERS_FILE, read_only=True)
PAPERS = {}
for r in list(wb["Findings"].iter_rows(values_only=True))[1:]:
    if r[0] is None: continue
    sr, yr, _, title, authors = r[0], r[1], r[2], r[3], r[4]
    doi, url = r[11], r[12]
    al = [a.strip() for a in str(authors).split(",") if a.strip()]

    def ieee(name):
        parts = name.replace(".", ". ").split()
        if len(parts) >= 2 and len(parts[-1]) > 2 and not parts[-1].endswith("."):
            ini = " ".join(w[0] + "." for w in parts[:-1] if w[0].isalpha())
            return f"{ini} {parts[-1]}"
        return name
    al = [ieee(a) for a in al]
    if len(al) > 6: au = al[0] + " et al."
    elif len(al) > 1: au = ", ".join(al[:-1]) + " and " + al[-1]
    else: au = al[0]
    ref = f'{au}, "{title.strip()}," {yr}.'
    if doi and str(doi) != "None": ref += f" doi: {doi}."
    if url: ref += f" [Online]. Available: {url}"
    PAPERS[f"P{int(sr)}"] = ref
REFTEXT = dict(PAPERS); REFTEXT.update(C.EXTRA_REFS)
ORDER = []


def cite(text):
    text = re.sub(r"\[(P\d+)\]", r"{\1}", text)

    def num(k):
        if not re.fullmatch(r"P\d+", k) or k not in REFTEXT: raise KeyError(k)
        if k not in ORDER: ORDER.append(k)
        return int(k[1:])

    def grp(m):
        keys = re.findall(r"\{([A-Za-z0-9]+)\}", m.group(0))
        return ", ".join(f"[{num(k)}]" for k in keys)
    return re.sub(r"(?:\{[A-Za-z0-9]+\})+", grp, text)


# ------------------------------------------------------------------ main-body writers
CAPTIONS = {"fig": [], "table": []}


def para(text, size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=6, line=1.5,
         keep_next=False, indent=None):
    p = doc.add_paragraph()
    add_runs(p, cite(text), size=size, bold=bold, italic=italic)
    pf = p.paragraph_format; p.alignment = align
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = line; pf.keep_with_next = keep_next
    if indent is not None: pf.left_indent = Inches(indent)
    return p


def heading(text, level):
    p = doc.add_paragraph(style=f"Heading {level}")
    add_runs(p, text, size={1: 16, 2: 13, 3: 12}[level], bold=True, italic=(level == 3))
    for r in p.runs: r.font.color.rgb = RGBColor(0, 0, 0)
    pf = p.paragraph_format; pf.keep_with_next = True
    pf.space_before = Pt({1: 0, 2: 12, 3: 8}[level]); pf.space_after = Pt({1: 18, 2: 6, 3: 4}[level])
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if level == 1 else WD_ALIGN_PARAGRAPH.LEFT
    return p


def chapter(n, title, first=False):
    roman = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII"][n]
    p = heading(f"CHAPTER {roman}", 1); p.paragraph_format.space_after = Pt(4)
    if not first: page_break_before(p)
    heading(title.upper(), 1)


def set_cell_shade(cell, hexcolor):
    tcPr = cell._element.get_or_add_tcPr(); sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcolor); tcPr.append(sh)


def table(caption, header, rows, widths):
    CAPTIONS["table"].append(caption)
    cap = para(caption, size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, before=6, after=4, line=1.0, keep_next=True)
    total = sum(widths); scale = min(1.0, 7.0 / total); widths = [w * scale for w in widths]
    t = doc.add_table(rows=1 + len(rows), cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for col, w in zip(t.columns, widths): col.width = Inches(w)
    tblPr = t._element.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), str(int(sum(widths) * 1440))); tw.set(qn("w:type"), "dxa")
    old = tblPr.find(qn("w:tblW"))
    if old is not None: tblPr.remove(old)
    tblPr.append(tw)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "808080")
        borders.append(e)
    tblPr.append(borders)
    order_t = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize", "tblW", "jc",
               "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook"]
    kids = list(tblPr); seen = set()
    for k in kids: tblPr.remove(k)
    for name in order_t:
        for k in kids:
            if k.tag == qn(f"w:{name}") and name not in seen:
                tblPr.append(k); seen.add(name)
    for ri, row in enumerate([header] + rows):
        tr = t.rows[ri]
        trPr = tr._tr.get_or_add_trPr(); cs = OxmlElement("w:cantSplit"); trPr.append(cs)
        if ri == 0:
            th = OxmlElement("w:tblHeader"); trPr.append(th)
        for ci, val in enumerate(row):
            c = tr.cells[ci]; c.width = Inches(widths[ci])
            p = c.paragraphs[0]
            add_runs(p, cite(str(val)), size=10, bold=(ri == 0))
            p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.left_indent = Inches(0); p.paragraph_format.right_indent = Inches(0)
            p.paragraph_format.first_line_indent = Inches(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if ci == 0 or len(str(val)) > 18 else WD_ALIGN_PARAGRAPH.CENTER
            if ri == 0: set_cell_shade(c, "D9E2F3")
            if ri < len(rows): p.paragraph_format.keep_with_next = True
    para("", after=4, line=1.0)
    return t


def figure(path, caption, width):
    CAPTIONS["fig"].append(caption)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True; p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(path, width=Inches(width))
    para(caption, size=10, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=10, line=1.0)


def numbered(items):
    for i, it in enumerate(items, 1):
        p = para(f"{i}.\t{it}", indent=0.35)
        p.paragraph_format.first_line_indent = Inches(-0.35)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(0.35))


def render(blocks, start_chapter=None):
    n = start_chapter or 0
    first = True
    for b in blocks:
        k = b[0]
        if k == "h1":
            n += 1; chapter(n, b[1], first=first); first = False
        elif k == "h2": heading(b[1], 2)
        elif k == "h3": heading(b[1], 3)
        elif k == "pbi":
            p = doc.add_paragraph()
            add_runs(p, b[1] + ", ", size=12, bold=True, italic=True)
            add_runs(p, cite(b[2]) + f"[{b[3]}].", size=12)
            pf = p.paragraph_format; p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf.space_before = Pt(0); pf.space_after = Pt(6); pf.line_spacing = 1.5
        elif k == "p":
            text = b[1]
            if text.startswith("PSI ="):
                para(text, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
            else:
                para(text)
        elif k == "pi": para(b[1], size=10, italic=True, after=8, line=1.0)
        elif k == "num": numbered(b[1])
        elif k == "table": table(b[1], b[2], b[3], b[4])
        elif k == "fig": figure(b[1], b[2], b[3])
        first = False if k != "h1" else first


# ------------------------------------------------------------------ lists of figures and tables (front matter)
# Built after the body so all captions are known; placeholder paragraph marks the position.
lot_anchor = doc.add_paragraph()
page_break_before(lot_anchor)

# ------------------------------------------------------------------ main section
doc.add_section(WD_SECTION.NEW_PAGE)
render(C.CH)

# references
p = heading("CHAPTER VIII", 1); page_break_before(p); p.paragraph_format.space_after = Pt(4)
heading("REFERENCES", 1)
# annexures first pass to register their citations (none expected) before printing the list
for i in range(1, 48):
    k = f"P{i}"
    rp = para(f"[{i}]\t{REFTEXT[k]}", size=11, align=WD_ALIGN_PARAGRAPH.LEFT, after=4, line=1.15, indent=0.45)
    rp.paragraph_format.first_line_indent = Inches(-0.45); rp.paragraph_format.tab_stops.add_tab_stop(Inches(0.45))
unused = [k for k in REFTEXT if k not in ORDER]
if unused: print("UNCITED references (not listed):", unused)

p = heading("ANNEXURES", 1); page_break_before(p)
for blk in C.ANNEX:
    if blk[0] == "h2" and blk[1].startswith("Annexure D"):
        hp = heading(blk[1], 2); page_break_before(hp)
    elif blk[0] == "h2": heading(blk[1], 2)
    elif blk[0] == "p": para(blk[1])
    elif blk[0] == "fig": figure(blk[1], blk[2], blk[3])
    elif blk[0] == "table": table(blk[1], blk[2], blk[3], blk[4])

# fill the lists of figures and tables at the anchor (front matter section)
def front_para(text, size=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, after=2, pagebreak=False):
    p = doc.add_paragraph(); add_runs(p, text, size=size, bold=bold); p.alignment = align
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.line_spacing = 1.0
    if pagebreak: page_break_before(p)
    return p

items = []
items.append(front_para("LIST OF FIGURES", 14, True, WD_ALIGN_PARAGRAPH.CENTER, 12))
for cap in CAPTIONS["fig"]:
    short = re.split(r" \(|; ", cap)[0]
    q = front_para(short + "\t#", 11)
    q.paragraph_format.tab_stops.add_tab_stop(Inches(7.0), WD_TAB_ALIGNMENT.RIGHT, 1)
    items.append(q)
items.append(front_para("LIST OF TABLES", 14, True, WD_ALIGN_PARAGRAPH.CENTER, 12, pagebreak=True))
for cap in CAPTIONS["table"]:
    short = cap.split(" (")[0]
    q = front_para(short + "\t#", 11)
    q.paragraph_format.tab_stops.add_tab_stop(Inches(7.0), WD_TAB_ALIGNMENT.RIGHT, 1)
    items.append(q)
prev = lot_anchor._element
for it in items:
    prev.addnext(it._element); prev = it._element
items[0].paragraph_format.page_break_before = True
lot_anchor._element.getparent().remove(lot_anchor._element)

# ------------------------------------------------------------------ page numbering (footers)
s1, s2 = doc.sections[0], doc.sections[-1]


def pgnum(section, fmt):
    sp = section._sectPr
    old = sp.find(qn("w:pgNumType"))
    if old is not None: sp.remove(old)
    e = OxmlElement("w:pgNumType"); e.set(qn("w:start"), "1")
    if fmt: e.set(qn("w:fmt"), fmt)
    sp.append(e)


pgnum(s1, "upperRoman"); pgnum(s2, "decimal")


def page_field(footer):
    for p in footer.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    for t in footer.tables:
        t._element.getparent().remove(t._element)
    p = footer.paragraphs[0]
    for r in list(p.runs): r._element.getparent().remove(r._element)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(); set_font(r, 11)
    for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), tag); r._element.append(f)
        else:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; r._element.append(it)


for f in (s1.footer, s1.even_page_footer, s1.first_page_footer):
    page_field(f)
s2.footer.is_linked_to_previous = True
s2.even_page_footer.is_linked_to_previous = True
s2.first_page_footer.is_linked_to_previous = True

doc.save(OUTFILE)
print("saved", OUTFILE, "| refs cited:", len(ORDER), "| figures:", len(CAPTIONS["fig"]), "| tables:", len(CAPTIONS["table"]))
