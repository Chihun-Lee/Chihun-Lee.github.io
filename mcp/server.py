#!/usr/bin/env python3
"""FastMCP server for managing the Chihun Lee CV/SNS SSOT.

Tools edit the YAML files under /Users/chihun/Code/SNS/data/ and trigger
the existing CV / Website / LinkedIn-post builders. All edits use
``ruamel.yaml`` round-trip mode when available so formatting and comments
are preserved; we fall back to PyYAML otherwise.
"""

from __future__ import annotations

import io
import re
import subprocess
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

# ──────────────────────────────────────────────────────────────────────────
# YAML round-trip (preferred) vs safe (fallback)
try:
    from ruamel.yaml import YAML

    _yaml_rt = YAML()
    _yaml_rt.preserve_quotes = True
    _yaml_rt.indent(mapping=2, sequence=4, offset=2)
    _USE_RUAMEL = True
except Exception:  # pragma: no cover
    import yaml as _pyyaml

    _USE_RUAMEL = False


def _load(path: Path) -> Any:
    if not path.exists():
        return {}
    with path.open() as f:
        if _USE_RUAMEL:
            return _yaml_rt.load(f) or {}
        return _pyyaml.safe_load(f) or {}


def _dump(path: Path, data: Any) -> None:
    if _USE_RUAMEL:
        with path.open("w") as f:
            _yaml_rt.dump(data, f)
    else:
        with path.open("w") as f:
            _pyyaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


# ──────────────────────────────────────────────────────────────────────────
# Paths
REPO = Path("/Users/chihun/Code/SNS")
DATA = REPO / "data"
PUBS_YAML = DATA / "publications.yaml"
TALKS_YAML = DATA / "talks.yaml"
PROJECTS_YAML = DATA / "projects.yaml"
NEWS_YAML = DATA / "news.yaml"
PROFILE_YAML = DATA / "profile.yaml"

CV_BUILD = REPO / "CV" / "build_cv.py"
WEBSITE_DIR = REPO / "Website"
SNS_GEN = REPO / "SNS" / "generate_posts.py"

# ──────────────────────────────────────────────────────────────────────────
mcp = FastMCP("chihun-cv-mcp")

# ──────────────────────────────────────────────────────────────────────────
# Helpers
_PILLARS = {"manufacturing", "nanophotonics", "materials", "autonomous-metal-lab"}
_ROLES_PUB = {"first", "corresponding", "co_first", "co"}
_ROLES_TALK = {"oral", "poster", "virtual_poster", "invited", "keynote"}
_TYPES_TALK = {"international", "domestic"}


def _slug_three(text: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    return "-".join(words[:3]) if words else "untitled"


def _validate_choice(name: str, value: str, allowed: set[str]) -> None:
    if value not in allowed:
        raise ValueError(
            f"Invalid {name}={value!r}. Allowed: {sorted(allowed)}"
        )


def _run(cmd: list[str], cwd: Path | None = None) -> dict:
    """Run a subprocess, return its stdout/stderr/returncode."""
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    return {
        "cmd": " ".join(cmd),
        "cwd": str(cwd) if cwd else "",
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


# ──────────────────────────────────────────────────────────────────────────
# 1. add_publication
@mcp.tool
def add_publication(
    title: str,
    authors: list[str],
    venue: str,
    year: int,
    pillar: str,
    role: str = "first",
    equal_contribution: bool = False,
    volume: str | None = None,
    issue: str | None = None,
    pages: str | None = None,
    doi: str | None = None,
    url: str | None = None,
    citations: int | None = None,
) -> dict:
    """Append a new publication to data/publications.yaml.

    The id is derived as ``lee<year>-<3-word-title-slug>``. Validation is
    performed on pillar and role. Returns the assigned id and a short echo.
    """
    if not title or not isinstance(title, str):
        raise ValueError("title is required (non-empty string)")
    if not authors or not isinstance(authors, list):
        raise ValueError("authors must be a non-empty list of strings")
    if not isinstance(year, int) or year < 1900 or year > 2100:
        raise ValueError("year must be a sensible integer (1900–2100)")
    _validate_choice("pillar", pillar, _PILLARS)
    _validate_choice("role", role, _ROLES_PUB)

    pub_id = f"lee{year}-{_slug_three(title)}"

    entry: dict[str, Any] = {
        "id": pub_id,
        "title": title,
        "authors": list(authors),
        "venue": venue,
        "year": year,
        "role": role,
        "pillar": pillar,
    }
    if volume is not None:
        entry["volume"] = str(volume)
    if issue is not None:
        entry["issue"] = str(issue)
    if pages is not None:
        entry["pages"] = str(pages)
    if equal_contribution:
        entry["equal_contribution"] = True
    if doi:
        entry["doi"] = doi
    if url:
        entry["url"] = url
    if citations is not None:
        entry["citations"] = int(citations)

    doc = _load(PUBS_YAML)
    pubs = doc.setdefault("publications", [])
    # Reject duplicate ids
    if any(p.get("id") == pub_id for p in pubs):
        raise ValueError(f"publication id {pub_id!r} already exists")
    pubs.append(entry)
    _dump(PUBS_YAML, doc)
    return {"ok": True, "id": pub_id, "count": len(pubs)}


# ──────────────────────────────────────────────────────────────────────────
# 2. add_talk
@mcp.tool
def add_talk(
    title: str,
    venue: str,
    location: str,
    date: str,
    role: str,
    type: str,
    authors: list[str] | None = None,
) -> dict:
    """Append a new talk to data/talks.yaml."""
    if not title or not venue:
        raise ValueError("title and venue are required")
    _validate_choice("role", role, _ROLES_TALK)
    _validate_choice("type", type, _TYPES_TALK)

    entry: dict[str, Any] = {
        "title": title,
        "venue": venue,
        "location": location,
        "date": date,
        "role": role,
        "type": type,
    }
    if authors:
        entry["authors"] = list(authors)

    doc = _load(TALKS_YAML)
    talks = doc.setdefault("talks", [])
    talks.append(entry)
    _dump(TALKS_YAML, doc)
    return {"ok": True, "count": len(talks)}


# ──────────────────────────────────────────────────────────────────────────
# 3. add_project
@mcp.tool
def add_project(
    title: str,
    sponsor: str,
    role: str,
    start: str,
    end: str,
    pillar: str,
) -> dict:
    """Append a new project entry to data/projects.yaml."""
    if not title or not sponsor:
        raise ValueError("title and sponsor are required")
    _validate_choice("pillar", pillar, _PILLARS)

    entry = {
        "title": title,
        "sponsor": sponsor,
        "role": role,
        "start": start,
        "end": end,
        "pillar": pillar,
    }

    doc = _load(PROJECTS_YAML)
    projects = doc.setdefault("projects", [])
    projects.append(entry)
    _dump(PROJECTS_YAML, doc)
    return {"ok": True, "count": len(projects)}


# ──────────────────────────────────────────────────────────────────────────
# 4. add_news (prepend — newest first)
@mcp.tool
def add_news(date: str, text: str) -> dict:
    """Prepend a news item to data/news.yaml (newest first)."""
    if not date or not text:
        raise ValueError("date and text are required")

    doc = _load(NEWS_YAML)
    items = doc.setdefault("news", [])
    items.insert(0, {"date": date, "text": text})
    _dump(NEWS_YAML, doc)
    return {"ok": True, "count": len(items)}


# ──────────────────────────────────────────────────────────────────────────
# 5. update_profile_field
@mcp.tool
def update_profile_field(path: str, value: Any) -> dict:
    """Update a dotted path inside data/profile.yaml.

    Example: ``update_profile_field("scholar_metrics.h_index", 13)``.
    The path must already exist (we do not create new branches blindly).
    """
    if not path:
        raise ValueError("path is required, e.g. 'scholar_metrics.h_index'")

    doc = _load(PROFILE_YAML)
    parts = path.split(".")
    cursor: Any = doc
    for p in parts[:-1]:
        if not isinstance(cursor, dict) or p not in cursor:
            raise ValueError(f"path segment {p!r} not found in profile.yaml")
        cursor = cursor[p]
    leaf = parts[-1]
    if not isinstance(cursor, dict) or leaf not in cursor:
        raise ValueError(f"leaf {leaf!r} not found at {path!r}")

    old = cursor[leaf]
    cursor[leaf] = value
    _dump(PROFILE_YAML, doc)
    return {"ok": True, "path": path, "old": old, "new": value}


# ──────────────────────────────────────────────────────────────────────────
# 6. list_publications
@mcp.tool
def list_publications(
    pillar: str | None = None,
    year: int | None = None,
    role: str | None = None,
) -> list[dict]:
    """Return publications filtered by pillar / year / role.

    Each entry is a minimal {id, title, year, venue, pillar, role} dict.
    """
    if pillar is not None:
        _validate_choice("pillar", pillar, _PILLARS)
    if role is not None:
        _validate_choice("role", role, _ROLES_PUB)

    doc = _load(PUBS_YAML)
    out = []
    for p in doc.get("publications", []) or []:
        if pillar and p.get("pillar") != pillar:
            continue
        if year and p.get("year") != year:
            continue
        if role and p.get("role") != role:
            continue
        out.append(
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "year": p.get("year"),
                "venue": p.get("venue"),
                "pillar": p.get("pillar"),
                "role": p.get("role"),
            }
        )
    return out


# ──────────────────────────────────────────────────────────────────────────
# 7. build_cv
@mcp.tool
def build_cv() -> dict:
    """Run the CV builder script.

    Returns the planned PDF path plus stdout/stderr/returncode. If the
    builder script does not exist yet, returns an explanatory error.
    """
    if not CV_BUILD.exists():
        return {
            "ok": False,
            "error": f"CV build script not found: {CV_BUILD}",
        }
    result = _run(["python3", str(CV_BUILD)], cwd=CV_BUILD.parent)
    result["pdf_path"] = str(CV_BUILD.parent / "cv.pdf")
    return result


# ──────────────────────────────────────────────────────────────────────────
# 8. build_site
@mcp.tool
def build_site() -> dict:
    """Run ``npm run build`` inside the Website project."""
    if not (WEBSITE_DIR / "package.json").exists():
        return {
            "ok": False,
            "error": f"package.json not found in {WEBSITE_DIR}",
        }
    result = _run(["npm", "run", "build"], cwd=WEBSITE_DIR)
    result["dist_path"] = str(WEBSITE_DIR / "dist")
    return result


# ──────────────────────────────────────────────────────────────────────────
# 9. generate_linkedin_posts
@mcp.tool
def generate_linkedin_posts() -> dict:
    """Run the LinkedIn post generator and report how many files exist."""
    if not SNS_GEN.exists():
        return {"ok": False, "error": f"generator not found: {SNS_GEN}"}
    result = _run(["python3", str(SNS_GEN)], cwd=SNS_GEN.parent)
    posts_dir = SNS_GEN.parent / "posts"
    if posts_dir.exists():
        files = [p.name for p in posts_dir.iterdir() if p.suffix == ".md"]
        result["post_count"] = len(files)
    else:
        result["post_count"] = 0
    return result


# ──────────────────────────────────────────────────────────────────────────
# 10. git_status
@mcp.tool
def git_status() -> dict:
    """Return ``git status --short`` of the SSOT repo (graceful if no repo)."""
    try:
        proc = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(REPO),
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return {"ok": False, "error": "git binary not found"}

    if proc.returncode != 0:
        # Most likely 'not a git repository'
        return {
            "ok": False,
            "is_repo": False,
            "stderr": proc.stderr.strip(),
        }
    return {
        "ok": True,
        "is_repo": True,
        "short": proc.stdout,
    }


# ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
