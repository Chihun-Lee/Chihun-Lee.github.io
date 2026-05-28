# CLAUDE.md — SNS (Research Identity Hub)

## What this repo is

Single source of truth for the user's academic identity. **Edit `data/*.yaml` → CV (Typst), website (Astro), and LinkedIn drafts all re-derive.** Live at https://chihun-lee.github.io (public repo `Chihun-Lee/Chihun-Lee.github.io`, GitHub Pages = workflow source).

```
data/         SSOT — profile, publications, projects, talks, patents, news, people
CV/           Typst template + build_cv.py → build/cv.pdf
Website/      Astro static site, Claude design tokens (warm cream, Source Serif 4, #CC785C)
SNS/          LinkedIn post generator → posts/*.md drafts (copy-paste, no API)
mcp/          FastMCP server `chihun-cv-mcp` (registered in ~/.claude.json for this dir)
source/       LOCAL ONLY — internal proposals + paper PDFs, .gitignored, NEVER push
rebuild_all.sh  one command for everything
.github/workflows/deploy-website.yml  GH Action: install Typst, build CV, build site, deploy
```

## Critical rules

- **NEVER commit `source/`** — it contains active research proposals (e.g. "금속 소재 멀티모달 빅데이터 구축_2026_계획서"). Already gitignored. If you find anything proposal-like or unpublished, ask before staging.
- **NEVER push citation counts, mobile phone, or anything privacy-sensitive without checking** that it's already public on the user's existing CV/Scholar page. The current mobile in `data/profile.yaml` was already on the user's public CV docx.
- **Repo IS the GH Pages source.** Pages build type = workflow (not legacy Jekyll). Don't switch back to legacy.
- **Use `--force` carefully** on `SNS/generate_posts.py` — it overwrites drafts the user marked `status: published`.

## Common operations

```bash
# After editing data/*.yaml:
./rebuild_all.sh                # CV + LinkedIn drafts + Website
./rebuild_all.sh cv             # PDF only
./rebuild_all.sh site           # Astro only (builds CV first to copy /cv.pdf)

# Build CV directly:
/opt/homebrew/Caskroom/miniforge/base/envs/3dp/bin/python CV/build_cv.py

# Push → auto-deploys via GH Action (paths: Website/**, data/**, CV/**, workflow itself)
git push
```

The MCP server `chihun-cv-mcp` exposes `add_publication`, `add_talk`, `update_profile_field`, `build_cv`, `build_site`, `generate_linkedin_posts`, etc. It's registered in `~/.claude.json` under this project's `mcpServers` and uses the `3dp` miniforge env interpreter. Prefer the MCP tools over manual YAML edits when an agent is making changes — they validate enums (pillar, role, type) and reject duplicate IDs.

## Research pillars (the user's chosen taxonomy)

Defined in `data/profile.yaml → research_pillars`. Every publication and project carries one:

| id                       | English                       | Korean              |
| ------------------------ | ----------------------------- | ------------------- |
| `manufacturing`          | Manufacturing Optimization    | 제조 최적화         |
| `nanophotonics`          | Nanophotonics Optimization    | 나노포토닉스 최적화 |
| `materials`              | Materials Optimization        | 소재 최적화         |
| `autonomous-metal-lab`   | Metal Autonomous Laboratory   | 금속 자율실험실     |

When adding a new paper, pick the pillar carefully — the website filters and the LinkedIn hashtag set both depend on it.

## Sources of truth outside this repo

- Google Scholar (Na1nYPsAAAAJ) — authoritative for citation counts and paper presence
- The user's existing `CV/Curriculum Vitae Chihun Lee (2025.11).docx` — pre-2026 baseline of contact info, projects, patents; kept for reference, do not modify
