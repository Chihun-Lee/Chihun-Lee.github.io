#!/usr/bin/env python3
"""Build CV PDF from YAML SSOT.

Reads /Users/chihun/Code/홍보_SNS/SNS/data/*.yaml, renders Typst, compiles to PDF.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
BUILD = HERE / "build"

# Strings to bold in author lists (user's name in all forms)
SELF_NAMES = ["C. Lee", "Chihun Lee", "이치헌"]


# ─── Typst escaping helpers ────────────────────────────────────────────
def esc(s: str) -> str:
    """Escape a string for Typst markup context."""
    if s is None:
        return ""
    s = str(s)
    # Order matters: escape backslash first.
    s = s.replace("\\", "\\\\")
    # Characters that begin Typst markup
    for ch in ["#", "@", "$", "*", "_", "`", "<", ">", "/", "[", "]", "=", "~"]:
        s = s.replace(ch, "\\" + ch)
    # Quotes — keep as-is but normalize curly to straight to avoid font issues
    s = s.replace('"', '\\"')
    return s


def fmt_author(name: str) -> str:
    """Format a single author name with Typst markup.

    Preserves trailing markers: '+' (equal contrib), '*' (corresponding).
    Bolds the user's name.
    """
    raw = name.strip()
    # Pull off trailing markers
    markers = ""
    while raw and raw[-1] in "+*":
        markers = raw[-1] + markers
        raw = raw[:-1]
    base = raw.strip()
    base_esc = esc(base)
    marker_esc = esc(markers) if markers else ""
    if base in SELF_NAMES:
        return f"#strong[{base_esc}]{marker_esc}"
    return f"{base_esc}{marker_esc}"


def fmt_authors(authors: list[str]) -> str:
    return ", ".join(fmt_author(a) for a in authors)


def fmt_month_year(date_str: str) -> str:
    """Normalize date strings like '2024-09' or '2025-02' or 'present'."""
    if not date_str:
        return ""
    s = str(date_str).strip()
    if s.lower() in ("present", "ongoing"):
        return "Present"
    # YYYY-MM
    parts = s.split("-")
    months = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec",
    }
    if len(parts) >= 2 and parts[1] in months:
        return f"{months[parts[1]]} {parts[0]}"
    return s


def fmt_range(start: str, end: str) -> str:
    s = fmt_month_year(start)
    e = fmt_month_year(end)
    if s and e:
        return f"{s} – {e}"
    return s or e


# ─── Section renderers ─────────────────────────────────────────────────
def render_education(items: list[dict]) -> str:
    out = ["#section[Education]"]
    for ed in items:
        left_parts = [f"*{esc(ed['degree'])}*, {esc(ed['field'])}"]
        left_parts.append(esc(ed["institution"]))
        if ed.get("advisor"):
            left_parts.append(f"Advisor: {esc(ed['advisor'])}")
        left = " — ".join(left_parts)
        right = fmt_range(ed.get("start", ""), ed.get("end", ""))
        out.append(f"#entry[{left}][{right}]")
        out.append("#v(0.25em)")
    return "\n".join(out)


def render_experience(items: list[dict]) -> str:
    out = ["#section[Experience]"]
    for ex in items:
        left_parts = [f"*{esc(ex['role'])}*"]
        org = esc(ex["org"])
        if ex.get("division"):
            org = f"{org}, {esc(ex['division'])}"
        left_parts.append(org)
        if ex.get("pi"):
            left_parts.append(f"PI: {esc(ex['pi'])}")
        left = " — ".join(left_parts)
        right = fmt_range(ex.get("start", ""), ex.get("end", ""))
        out.append(f"#entry[{left}][{right}]")
        out.append("#v(0.25em)")
    return "\n".join(out)


def fmt_pub(n: int, pub: dict) -> str:
    authors = fmt_authors(pub.get("authors", []))
    title = esc(pub.get("title", ""))
    venue = esc(pub.get("venue", ""))
    bits = [f"\\\"{title}\\\""]
    bits.insert(0, authors)
    bib = []
    if pub.get("volume"):
        bib.append(f"Vol. {esc(pub['volume'])}")
    if pub.get("issue"):
        bib.append(f"Issue {esc(pub['issue'])}")
    if pub.get("pages"):
        bib.append(f"pp. {esc(str(pub['pages']))}")
    year = pub.get("year", "")
    venue_part = f"_{venue}_"
    tail_parts = [venue_part]
    if bib:
        tail_parts.append(", ".join(bib))
    tail = ", ".join(tail_parts)
    tail = f"{tail} ({esc(str(year))})." if year else f"{tail}."
    body = f"{authors}, \\\"{title}\\\", {tail}"
    return f"#item({n})[{body}]"


def render_publications(pubs: list[dict]) -> str:
    first = [p for p in pubs if p.get("role") in ("first", "co_first", "corresponding")]
    co = [p for p in pubs if p.get("role") == "co"]

    # Sort newest first within each
    first.sort(key=lambda p: (-(p.get("year") or 0)))
    co.sort(key=lambda p: (-(p.get("year") or 0)))

    out = []
    out.append("#section[First-Author & Co-First Publications]")
    for i, p in enumerate(first, 1):
        out.append(fmt_pub(i, p))
    out.append("#v(0.4em)")
    out.append("#section[Co-Author Publications]")
    for i, p in enumerate(co, 1):
        out.append(fmt_pub(i, p))
    out.append(
        "#v(0.4em) #text(size: 8.5pt, fill: rgb(\"#666666\"))[#emph[\\+ equal contribution \\u{00B7} \\* corresponding author]]"
    )
    return "\n".join(out)


def render_projects(items: list[dict]) -> str:
    out = ["#section[Industry & Funded Projects]"]
    # Sort newest first by start
    items_sorted = sorted(items, key=lambda x: str(x.get("start", "")), reverse=True)
    for i, p in enumerate(items_sorted, 1):
        title = esc(p.get("title", ""))
        sponsor = esc(p.get("sponsor", ""))
        role = esc(p.get("role", ""))
        period = fmt_range(p.get("start", ""), p.get("end", ""))
        body = f"*{title}* — {sponsor} ({role}). {period}."
        out.append(f"#item({i})[{body}]")
    return "\n".join(out)


def render_talks(items: list[dict]) -> str:
    intl = [t for t in items if t.get("type") == "international"]
    dom = [t for t in items if t.get("type") == "domestic"]
    intl.sort(key=lambda t: str(t.get("date", "")), reverse=True)
    dom.sort(key=lambda t: str(t.get("date", "")), reverse=True)

    def fmt_talk(n: int, t: dict) -> str:
        authors = fmt_authors(t.get("authors", []))
        title = esc(t.get("title", ""))
        venue = esc(t.get("venue", ""))
        loc = esc(t.get("location", ""))
        date = fmt_month_year(t.get("date", ""))
        role = esc(str(t.get("role", "")).replace("_", " "))
        body = (
            f"{authors}, \\\"{title}\\\", _{venue}_, {loc} ({date}) — {role}."
        )
        return f"#item({n})[{body}]"

    out = []
    out.append("#section[International Conference Presentations]")
    for i, t in enumerate(intl, 1):
        out.append(fmt_talk(i, t))
    out.append("#v(0.4em)")
    out.append("#section[Domestic Conference Presentations]")
    for i, t in enumerate(dom, 1):
        out.append(fmt_talk(i, t))
    return "\n".join(out)


def render_patents(items: list[dict]) -> str:
    out = ["#section[Patents]"]
    items_sorted = sorted(items, key=lambda p: -(p.get("year") or 0))
    for i, p in enumerate(items_sorted, 1):
        title_en = esc(p.get("title_en") or p.get("title", ""))
        number = esc(p.get("number", ""))
        jur = esc(p.get("jurisdiction", ""))
        year = p.get("year", "")
        assignee = p.get("assignee")
        tail_bits = [f"{number}", jur]
        if assignee:
            tail_bits.append(f"assignee: {esc(assignee)}")
        tail = ", ".join(b for b in tail_bits if b)
        body = f"*{title_en}* — {tail} ({esc(str(year))})."
        out.append(f"#item({i})[{body}]")
    return "\n".join(out)


def render_specializations(spec: dict) -> str:
    out = ["#section[Specializations]"]
    labels = {
        "forward_simulation": "Forward Simulation",
        "learning_and_optimization": "Learning & Optimization",
        "manufacturing_apps": "Manufacturing Applications",
        "nanophotonics_apps": "Nanophotonics Applications",
    }
    for key, label in labels.items():
        if key not in spec:
            continue
        items = ", ".join(esc(x) for x in spec[key])
        out.append(f"*{label}.* {items}")
        out.append("#v(0.2em)")
    return "\n".join(out)


def render_collaborations(items: list[dict]) -> str:
    out = ["#section[Active Collaborations]"]
    for c in items:
        lab = esc(c.get("lab", ""))
        inst = esc(c.get("institution", ""))
        pi = esc(c.get("pi", ""))
        topic = esc(c.get("topic", ""))
        body = f"*{lab}*, {inst} — PI: {pi}. {topic}."
        out.append(body + " \\")
    return "\n".join(out)


def render_research_interests(items: list[str]) -> str:
    out = ["#section[Research Interests]"]
    out.append(", ".join(esc(x) for x in items) + ".")
    return "\n".join(out)


def render_scholar(metrics: dict) -> str:
    if not metrics:
        return ""
    tc = metrics.get("total_citations", "")
    h = metrics.get("h_index", "")
    i10 = metrics.get("i10_index", "")
    updated = metrics.get("last_updated", "")
    body = (
        f"Total citations: *{esc(str(tc))}* · h-index: *{esc(str(h))}* · "
        f"i10-index: *{esc(str(i10))}* · as of {esc(str(updated))}."
    )
    return "#section[Google Scholar Metrics]\n" + body


# ─── Top-level build ───────────────────────────────────────────────────
def load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_typst() -> str:
    profile = load_yaml(DATA / "profile.yaml")
    pubs = load_yaml(DATA / "publications.yaml")["publications"]
    projects = load_yaml(DATA / "projects.yaml")["projects"]
    talks = load_yaml(DATA / "talks.yaml")["talks"]
    patents = load_yaml(DATA / "patents.yaml")["patents"]

    # Header bits
    name = esc(profile["name"])
    title = esc(profile["title"])
    affiliation = esc(profile["affiliation"])
    division = esc(profile.get("division", ""))

    contact = profile.get("contact", {})
    contact_bits = []
    if contact.get("email"):
        contact_bits.append(esc(contact["email"]))
    if contact.get("office_phone"):
        contact_bits.append(esc(contact["office_phone"]))
    if contact.get("location"):
        contact_bits.append(esc(contact["location"]))
    contact_line = " · ".join(contact_bits)

    links = profile.get("links", {})
    link_bits = []
    for label, key in [
        ("Scholar", "scholar"),
        ("Website", "website"),
        ("GitHub", "github"),
        ("ORCID", "orcid"),
        ("LinkedIn", "linkedin"),
    ]:
        v = links.get(key)
        if v:
            link_bits.append(f"{label}: {esc(v)}")
    links_line = " · ".join(link_bits)

    # Compose body sections in CV order
    body_parts = [
        render_education(profile["education"]),
        render_experience(profile["experience"]),
        render_publications(pubs),
        render_projects(projects),
        render_talks(talks),
        render_patents(patents),
        render_specializations(profile.get("specializations", {})),
        render_collaborations(profile.get("collaborations", [])),
        render_research_interests(profile.get("research_interests", [])),
        render_scholar(profile.get("scholar_metrics", {})),
    ]
    body = "\n\n".join(body_parts)

    template = (HERE / "template.typ").read_text(encoding="utf-8")

    typst_src = (
        template
        + "\n\n"
        + (
            f"#show: cv.with(\n"
            f"  name: \"{name}\",\n"
            f"  title: \"{title}\",\n"
            f"  affiliation: \"{affiliation}\",\n"
            f"  division: \"{division}\",\n"
            f"  contact_line: \"{contact_line}\",\n"
            f"  links_line: \"{links_line}\",\n"
            f")\n\n"
        )
        + body
        + "\n"
    )
    return typst_src


def main() -> int:
    ap = argparse.ArgumentParser(description="Build CV PDF from YAML SSOT.")
    ap.add_argument("--no-pdf", action="store_true", help="Only generate cv.typ")
    args = ap.parse_args()

    BUILD.mkdir(exist_ok=True)
    typ_path = BUILD / "cv.typ"
    pdf_path = BUILD / "cv.pdf"

    print(f"[1/2] Rendering Typst → {typ_path}")
    typ_path.write_text(build_typst(), encoding="utf-8")
    print(f"      wrote {typ_path.stat().st_size} bytes")

    if args.no_pdf:
        print("Done (--no-pdf).")
        return 0

    typst = shutil.which("typst")
    if not typst:
        print("ERROR: `typst` not found on PATH. Install with: brew install typst",
              file=sys.stderr)
        return 2

    print(f"[2/2] Compiling Typst → {pdf_path}")
    res = subprocess.run(
        [typst, "compile", str(typ_path), str(pdf_path)],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        print("Typst compile failed:", file=sys.stderr)
        print(res.stdout, file=sys.stderr)
        print(res.stderr, file=sys.stderr)
        return res.returncode
    print(f"      OK ({pdf_path.stat().st_size} bytes)")
    print("Success.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
