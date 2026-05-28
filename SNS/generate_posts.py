#!/usr/bin/env python3
"""LinkedIn post generator.

Reads the SSOT YAML files under /Users/chihun/Code/SNS/data/ (READ ONLY) and
emits one markdown draft per publication and per talk into ./posts/<id>.md.

A post whose front-matter already has `status: published` is left untouched
unless --force is passed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# ──────────────────────────────────────────────────────────────────────────
# Paths
ROOT = Path(__file__).resolve().parent           # …/SNS/SNS
DATA_DIR = ROOT.parent / "data"                  # …/SNS/data
POSTS_DIR = ROOT / "posts"

PUBS_YAML = DATA_DIR / "publications.yaml"
TALKS_YAML = DATA_DIR / "talks.yaml"
PROFILE_YAML = DATA_DIR / "profile.yaml"

# ──────────────────────────────────────────────────────────────────────────
# Pillar → (one-sentence hook, hashtag list)
PILLAR_HOOKS: dict[str, str] = {
    "manufacturing": "Another step toward AI-assisted manufacturing where data and physics drive real shop-floor decisions.",
    "nanophotonics": "Inverse design keeps showing that the right optimizer can pull manufacturable optics out of an enormous design space.",
    "materials": "Closing the gap between microstructure, processing, and property prediction with data-driven models.",
    "autonomous-metal-lab": "Closing the loop between simulation, optimization, and real metal experiments to find good process windows faster.",
}

PILLAR_HASHTAGS: dict[str, list[str]] = {
    "manufacturing": ["#AIforManufacturing", "#SmartManufacturing"],
    "nanophotonics": ["#Nanophotonics", "#Metasurface", "#InverseDesign"],
    "materials": ["#Materials", "#MaterialsInformatics"],
    "autonomous-metal-lab": ["#AutonomousLab", "#ActiveLearning", "#LPBF"],
}

DEFAULT_HOOK = (
    "Sharing a new piece of work from our group — happy to discuss with anyone "
    "working on related problems."
)
DEFAULT_HASHTAGS = ["#AIforMaterials", "#AIforManufacturing"]


# ──────────────────────────────────────────────────────────────────────────
def _slugify(text: str, max_words: int = 3) -> str:
    """3-word slug for ids: ‘Inverse Design of …’ → ‘inverse-design-of’."""
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    return "-".join(words[:max_words]) if words else "untitled"


def _format_authors(authors: list[str], my_name: str) -> str:
    """Render an author list, bolding any entry that resolves to me."""
    # CV style uses "C. Lee" or "C. Lee+" or "C. Lee*"
    my_initials = "C. Lee"
    out = []
    for a in authors:
        # strip equal/corresponding markers when matching
        stripped = a.replace("+", "").replace("*", "").strip()
        if stripped == my_initials:
            out.append(f"**{a}**")
        else:
            out.append(a)
    return ", ".join(out)


def _read_yaml(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def _read_existing_front_matter(path: Path) -> dict | None:
    """Return parsed front-matter of an existing post, or None."""
    if not path.exists():
        return None
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None


def _write_post(path: Path, front_matter: dict, body: str, force: bool) -> str:
    """Write a post unless it's already marked published.

    Returns one of: 'written', 'skipped-published', 'unchanged'.
    """
    existing = _read_existing_front_matter(path)
    if existing and existing.get("status") == "published" and not force:
        return "skipped-published"

    fm_yaml = yaml.safe_dump(front_matter, sort_keys=False).strip()
    content = f"---\n{fm_yaml}\n---\n\n{body.rstrip()}\n"
    path.write_text(content)
    return "written"


# ──────────────────────────────────────────────────────────────────────────
def render_publication(pub: dict, my_name: str) -> tuple[str, dict, str]:
    pid = pub.get("id") or f"pub-{_slugify(pub.get('title', 'untitled'))}"
    pillar = pub.get("pillar", "")
    hook = PILLAR_HOOKS.get(pillar, DEFAULT_HOOK)
    hashtags = PILLAR_HASHTAGS.get(pillar, DEFAULT_HASHTAGS)

    authors = pub.get("authors", []) or []
    authors_str = _format_authors(authors, my_name)
    venue = pub.get("venue", "")
    year = pub.get("year", "")
    venue_line = f"Venue: {venue}, {year}".rstrip(", ")

    link_line = ""
    if pub.get("doi"):
        link_line = f"DOI: {pub['doi']}"
    elif pub.get("url"):
        link_line = pub["url"]

    title = pub.get("title", "Untitled")

    parts = [
        f'📄 New paper out: "{title}"',
        "",
        hook,
        "",
        f"Authors: {authors_str}",
        venue_line,
    ]
    if link_line:
        parts.append(link_line)
    parts += [
        "",
        "<!-- TODO: write 2–3 sentences on what we did and why it matters -->",
        "",
        " ".join(hashtags),
    ]
    body = "\n".join(parts)

    front_matter = {
        "id": f"pub-{pid}",
        "type": "publication",
        "status": "draft",
        "source_id": pid,
    }
    return f"pub-{pid}.md", front_matter, body


def render_talk(talk: dict) -> tuple[str, dict, str]:
    title = talk.get("title", "Untitled talk")
    venue = talk.get("venue", "")
    location = talk.get("location", "")
    date = str(talk.get("date", ""))
    role = talk.get("role", "talk")
    slug = _slugify(f"{venue} {title}", max_words=4)

    role_verb = {
        "oral": "gave an oral talk",
        "poster": "presented a poster",
        "virtual_poster": "presented a virtual poster",
        "invited": "gave an invited talk",
        "keynote": "delivered a keynote",
    }.get(role, "spoke")

    parts = [
        f"🎤 Just {role_verb} at {venue}" + (f", {location}" if location else "") + ".",
        "",
        f'Topic: "{title}"',
    ]
    if date:
        parts.append(f"Date: {date}")
    parts += [
        "",
        "<!-- TODO: 1–2 sentences on the key message + photo placeholder -->",
        "",
        "#Conference #Research #AIforScience",
    ]
    body = "\n".join(parts)

    front_matter = {
        "id": f"talk-{slug}",
        "type": "talk",
        "status": "draft",
        "source_id": slug,
    }
    return f"talk-{slug}.md", front_matter, body


# ──────────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="Generate LinkedIn post drafts.")
    ap.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even posts marked status: published",
    )
    args = ap.parse_args()

    POSTS_DIR.mkdir(exist_ok=True)

    profile = _read_yaml(PROFILE_YAML) or {}
    my_name = profile.get("name", "Chihun Lee")

    pubs_doc = _read_yaml(PUBS_YAML) or {}
    talks_doc = _read_yaml(TALKS_YAML) or {}

    pubs = pubs_doc.get("publications", []) or []
    talks = talks_doc.get("talks", []) or []

    written = 0
    skipped = 0
    missing_info: list[str] = []

    for pub in pubs:
        # Light validation — warn if essential fields are missing
        for need in ("title", "authors", "venue", "year"):
            if not pub.get(need):
                missing_info.append(
                    f"publication id={pub.get('id', '?')} missing '{need}'"
                )
        fname, fm, body = render_publication(pub, my_name)
        outcome = _write_post(POSTS_DIR / fname, fm, body, args.force)
        if outcome == "written":
            written += 1
        else:
            skipped += 1

    for talk in talks:
        for need in ("title", "venue"):
            if not talk.get(need):
                missing_info.append(
                    f"talk title={talk.get('title', '?')} missing '{need}'"
                )
        fname, fm, body = render_talk(talk)
        outcome = _write_post(POSTS_DIR / fname, fm, body, args.force)
        if outcome == "written":
            written += 1
        else:
            skipped += 1

    print(f"Generated {written} post(s); skipped {skipped} already-published.")
    print(f"Total publications: {len(pubs)}, talks: {len(talks)}")
    if missing_info:
        print("\nRows lacking required fields:")
        for m in missing_info:
            print(f"  - {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
