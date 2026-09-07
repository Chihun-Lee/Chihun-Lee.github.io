#!/usr/bin/env python
"""Build the Word CV from the YAML SSOT, in the layout of the user's own CV docx.

    python CV/build_cv_docx.py [--out "CV/Curriculum Vitae Chihun Lee (2026.09).docx"]

The original `Curriculum Vitae Chihun Lee (2025.11).docx` is the pre-2026 baseline
and is never touched — this writes a new dated file next to it, matching the user's
existing naming convention (2024.8 → 2024.10 → 2025.11 → …).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

BODY_PT = 10
NAME_PT = 16
HEAD_PT = 11


def load(name: str) -> dict:
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── date helpers ──────────────────────────────────────────────────────
MONTHS = ["", "Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.",
          "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]


def ym(v) -> str:
    """2020-04 → 'Apr. 2020'.  'present' → 'Present'."""
    s = str(v)
    if s.lower() in ("present", "current", ""):
        return "Present"
    parts = s.split("-")
    if len(parts) >= 2:
        return f"{MONTHS[int(parts[1])]} {parts[0]}"
    return s


def dot(v) -> str:
    """2020-04 → '2020.04'  (the numeric style used in the Research Projects list)."""
    s = str(v)
    if s.lower() in ("present", "current", ""):
        return "Present"
    parts = s.split("-")
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else s


# ── paragraph helpers ─────────────────────────────────────────────────
def para(doc, text="", *, size=BODY_PT, bold=False, italic=False,
         space_after=2, indent=0.0, hanging=0.0, align=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.05
    if indent:
        pf.left_indent = Pt(indent)
    if hanging:
        pf.first_line_indent = Pt(-hanging)
    p.alignment = align if align is not None else WD_ALIGN_PARAGRAPH.LEFT
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
    return p


def rich(doc, chunks, *, size=BODY_PT, space_after=2, indent=18, hanging=18):
    """chunks: list of (text, {'bold':bool,'italic':bool})."""
    p = para(doc, "", size=size, space_after=space_after, indent=indent, hanging=hanging)
    for text, fmt in chunks:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = fmt.get("bold", False)
        r.italic = fmt.get("italic", False)
    return p


def section(doc, title):
    p = para(doc, f"■ {title}", size=HEAD_PT, bold=True, space_after=3)
    p.paragraph_format.space_before = Pt(10)
    return p


# ── section builders ──────────────────────────────────────────────────
def build_header(doc, profile):
    p = para(doc, "", space_after=2)
    r = p.add_run(f"{profile['name']} ({profile['name_kr']}), {profile['honorific']}")
    r.font.size = Pt(NAME_PT)
    r.bold = True

    c = profile["contact"]
    lines = [
        f"{profile['affiliation']}, {profile['division']}",
        f"Position: {profile['title']}",
        f"Office: {c['office_phone']}   Mobile: {c['mobile']}",
        f"E-mail: {c['email']}   Nationality: {profile['nationality']}",
        f"Web: {profile['links']['website']}   Scholar: {profile['links']['scholar']}",
    ]
    for ln in lines:
        q = para(doc, ln, size=9, space_after=0)
        for r in q.runs:
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)


def build_education(doc, profile):
    section(doc, "Education")
    for ed in profile["education"]:
        bits = [f"{ym(ed['start'])} – {ym(ed['end'])}: {ed['degree']} "
                f"{ed['field']}, {ed['institution']}"]
        if ed.get("advisor"):
            bits.append(f" (Advisor: {ed['advisor']})")
        para(doc, "".join(bits), indent=18, hanging=18)


def build_experience(doc, profile):
    section(doc, "Experience")
    for ex in profile["experience"]:
        line = f"{ym(ex['start'])} – {ym(ex['end'])}: {ex['role']}, {ex['org']}"
        if ex.get("division"):
            line += f", {ex['division']}"
        if ex.get("pi"):
            line += f" (PI: {ex['pi']})"
        if ex.get("note"):
            line += f" — {ex['note']}"
        para(doc, line, indent=18, hanging=18)


def pub_chunks(n, p):
    authors = ", ".join(p.get("authors", []))
    bib = []
    if p.get("volume"):
        bib.append(str(p["volume"]))
    if p.get("issue"):
        bib.append(str(p["issue"]))
    if p.get("pages"):
        bib.append(str(p["pages"]))
    tail = ", ".join(bib)
    out = [(f"[{n}] {authors}, ", {}),
           (f"“{p['title']}”, ", {}),
           (p["venue"], {"italic": True})]
    if tail:
        out.append((f", {tail}", {}))
    out.append((f" ({p['year']})", {}))
    return out


def build_publications(doc, pubs):
    first = sorted([p for p in pubs if p.get("role") in ("first", "co_first", "corresponding")],
                   key=lambda p: -(p.get("year") or 0))
    co = sorted([p for p in pubs if p.get("role") == "co"],
                key=lambda p: -(p.get("year") or 0))

    section(doc, "First Author Peer-Reviewed Publications "
                 "(+: equal contributions, *: corresponding author)")
    for i, p in enumerate(first, 1):
        rich(doc, pub_chunks(i, p))

    section(doc, "Co-Author Peer-Reviewed Publications")
    for i, p in enumerate(co, 1):
        rich(doc, pub_chunks(i, p))


def build_projects(doc, projects):
    section(doc, "Research Projects")
    items = sorted(projects, key=lambda p: str(p.get("start", "")), reverse=True)
    for p in items:
        chunks = [(f"{dot(p['start'])} ~ {dot(p['end'])}: ", {}),
                  (f"“{p['title']}”", {}),
                  (f", {p['sponsor']} ({p['role']})", {})]
        rich(doc, chunks)


ROLE_LABEL = {
    "oral": "Oral Presenter",
    "poster": "Poster",
    "virtual_poster": "Virtual Poster",
    "invited": "Invited Talk",
    "keynote": "Keynote",
}


def build_talks(doc, talks):
    def block(title, kind):
        section(doc, title)
        rows = sorted([t for t in talks if t.get("type") == kind],
                      key=lambda t: str(t.get("date", "")), reverse=True)
        for i, t in enumerate(rows, 1):
            authors = ", ".join(t.get("authors", []))
            chunks = [(f"[{i}] {authors}, ", {}),
                      (f"“{t['title']}”, ", {}),
                      (t["venue"], {"italic": True}),
                      (f", {t.get('location', '')}, {ym(t['date'])} "
                       f"({ROLE_LABEL.get(t.get('role', ''), t.get('role', ''))})", {})]
            rich(doc, chunks)

    block("International Conference", "international")
    block("Domestic Conference", "domestic")


def build_patents(doc, patents):
    section(doc, "Patents")
    for i, p in enumerate(sorted(patents, key=lambda x: -(x.get("year") or 0)), 1):
        inv = ", ".join(p.get("inventors", []))
        tail = f"{p['number']}, {p['jurisdiction']}"
        if p.get("assignee"):
            tail += f", assignee: {p['assignee']}"
        rich(doc, [(f"[{i}] {inv}, ", {}),
                   (f"“{p['title']}”, ", {}),
                   (f"{tail} ({p['year']})", {})])


def build_specializations(doc, profile):
    section(doc, "Fields of Specialization and Interest")
    for line in profile["research_interests"]:
        para(doc, f"· {line}", indent=18, hanging=10)

    labels = [
        ("forward_simulation", "Nanophotonics forward simulation"),
        ("learning_and_optimization", "Deep learning and optimization"),
        ("manufacturing_apps", "Manufacturing applications"),
        ("nanophotonics_apps", "Nanophotonics applications"),
    ]
    for key, label in labels:
        items = profile["specializations"].get(key, [])
        if not items:
            continue
        rich(doc, [(f"{label}: ", {"bold": True}), ("; ".join(items), {})],
             indent=18, hanging=0)

    rich(doc, [("Co-work groups (non-funded): ", {"bold": True}), ("", {})],
         indent=18, hanging=0)
    for cw in profile["collaborations"]:
        para(doc, f"· {cw['lab']}, {cw['institution']} (PI: {cw['pi']}) — {cw['topic']}",
             indent=28, hanging=10)


# ── main ──────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    profile = load("profile.yaml")
    pubs = load("publications.yaml")["publications"]
    projects = load("projects.yaml")["projects"]
    talks = load("talks.yaml")["talks"]
    patents = load("patents.yaml")["patents"]

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.size = Pt(BODY_PT)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Pt(48)
        sec.left_margin = sec.right_margin = Pt(50)

    build_header(doc, profile)
    build_education(doc, profile)
    build_experience(doc, profile)
    build_publications(doc, pubs)
    build_projects(doc, projects)
    build_talks(doc, talks)
    build_patents(doc, patents)
    build_specializations(doc, profile)

    out = Path(args.out) if args.out else ROOT / "CV" / "Curriculum Vitae Chihun Lee (2026.09).docx"
    doc.save(out)
    print(f"OK  {out}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
