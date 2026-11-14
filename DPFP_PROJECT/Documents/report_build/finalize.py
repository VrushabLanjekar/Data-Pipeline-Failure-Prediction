# -*- coding: utf-8 -*-
"""finalize.py draft.docx draft.pdf out.docx : fills '#' page numbers in Index, List of Figures, List of Tables."""
import sys, re, pymupdf, docx

src, pdfp, out = sys.argv[1:4]
pages = [p.get_text() for p in pymupdf.open(pdfp)]
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
# first body page: the page that starts with CHAPTER I + INTRODUCTION
body0 = next(i for i, t in enumerate(pages) if re.match(r"\s*\d*\s*CHAPTER I\s*\n\s*INTRODUCTION", t))
print("body starts at pdf page", body0 + 1)


def arabic(i): return str(i - body0 + 1)


def find(pat, start=0, end=None):
    for i in range(start, end or len(pages)):
        if re.search(pat, pages[i]): return i
    raise LookupError(pat)


# chapter start pages
roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
starts = [next(i for i in range(body0, len(pages)) if re.match(rf"\s*\d*\s*CHAPTER {r}\s*\n", pages[i])) for r in roman]
ann = next(i for i in range(body0, len(pages)) if re.match(r"\s*\d*\s*ANNEXURES", pages[i]))
ends = [starts[k + 1] - 1 for k in range(7)] + [ann - 1]
rng = lambda a, b: arabic(a) if a == b else f"{arabic(a)}-{arabic(b)}"
chap_pages = [rng(a, b) for a, b in zip(starts, ends)]
ann_pages = rng(ann, len(pages) - 1)
lof = next(i for i in range(body0) if "LIST OF FIGURES" in pages[i] and "Figure 4.1" in pages[i])
lot = next(i for i in range(body0) if "LIST OF TABLES" in pages[i] and "Table 2.1" in pages[i])
front = ["I", "II", "III", "IV", "V-VI", f"{ROMAN[lof + 1]}-{ROMAN[body0]}"]

d = docx.Document(src)
t = d.tables[0]
vals = front + chap_pages + [ann_pages]
for row, v in zip(t.rows, vals):
    cell = row.cells[2]
    for r in cell.paragraphs[0].runs:
        if "#" in r.text: r.text = r.text.replace("#", v)
print("index:", vals)

# lists of figures / tables
def label(par):
    m = re.match(r"(Figure|Table) ([A-Z0-9]+\.\d+):", par.text)
    return m and f"{m.group(1)} {m.group(2)}:"


miss = 0
for p in d.paragraphs:
    if p.text.endswith("\t#"):
        lab = label(p)
        if not lab: continue
        try:
            pg = next(i for i in range(body0, len(pages)) if lab in pages[i])
        except StopIteration:
            miss += 1; continue
        for r in p.runs:
            if r.text.endswith("#"): r.text = r.text[:-1] + arabic(pg)
print("unresolved list entries:", miss)
d.save(out)
print("saved", out)
