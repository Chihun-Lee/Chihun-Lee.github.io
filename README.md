# Chihun Lee — Research Identity Hub

One place to maintain your academic identity. Edit YAML → CV, website, and LinkedIn drafts all re-derive.

```
SNS/
├── data/                  ← Single source of truth (edit these)
│   ├── profile.yaml       identity, bio, education, experience, pillars
│   ├── publications.yaml  papers (pillar-tagged)
│   ├── projects.yaml      funded industry projects
│   ├── talks.yaml         conference talks & travel
│   ├── patents.yaml       patents
│   ├── news.yaml          homepage news feed
│   └── people.yaml        advisors & collaborators
│
├── CV/                    ← Typst → PDF
│   ├── build_cv.py
│   ├── template.typ
│   └── build/cv.pdf
│
├── Website/               ← Astro static site → chihun-lee.github.io
│   ├── src/{pages,layouts,styles,lib}
│   └── dist/              (build output)
│
├── SNS/                   ← LinkedIn post drafts
│   ├── generate_posts.py
│   └── posts/<id>.md      (one draft per paper/talk)
│
├── mcp/                   ← FastMCP server for AI-driven edits
│   └── server.py          add_publication, add_talk, build_cv, ...
│
├── .github/workflows/
│   └── deploy-website.yml (GitHub Pages auto-deploy)
│
└── rebuild_all.sh         ← One command for everything
```

## Quick start

```bash
# Edit the YAML you care about (publications, talks, profile, …)
$EDITOR data/publications.yaml

# Rebuild all outputs
./rebuild_all.sh             # CV + LinkedIn drafts + Website
./rebuild_all.sh cv          # only the PDF
./rebuild_all.sh site        # only the static site
./rebuild_all.sh sns         # only LinkedIn drafts
```

## Per-output details

### CV (Typst)
- Install once: `brew install typst && pip install pyyaml`
- Build: `python3 CV/build_cv.py` → `CV/build/cv.pdf`
- Reference: `CV/Curriculum Vitae Chihun Lee (2025.11).docx` (untouched)

### Website (Astro → GitHub Pages)
- Local dev: `cd Website && npm install && npm run dev`
- Build: `cd Website && npm run build` (output in `Website/dist/`)
- Deploys automatically on push to `main` via `.github/workflows/deploy-website.yml`
- Live URL: https://chihun-lee.github.io

Sections: People, Research (4 pillars), Publications, Talks & Travel, CV.

### LinkedIn drafts
- `python3 SNS/generate_posts.py` writes one markdown draft per publication/talk into `SNS/posts/`.
- Each file has a `status: draft` front matter — once you mark `status: published`, the generator skips it on rerun.
- v1 is copy-paste (no LinkedIn API). Use `--force` to regenerate published drafts.

### MCP server (for AI-driven edits)
A FastMCP server exposes tools like `add_publication`, `add_talk`, `update_profile_field`, `build_cv`, `build_site`, `generate_linkedin_posts`.

Register with Claude Code (`~/.claude.json`):
```jsonc
"mcpServers": {
  "chihun-cv-mcp": {
    "command": "python3",
    "args": ["/Users/chihun/Code/SNS/mcp/server.py"]
  }
}
```
Then ask Claude: *"add a new paper to my CV"* and it handles the YAML edit + rebuild.

## Research pillars

Defined in `data/profile.yaml → research_pillars`:

| id                       | English                       | Korean              |
| ------------------------ | ----------------------------- | ------------------- |
| `manufacturing`          | Manufacturing Optimization    | 제조 최적화         |
| `nanophotonics`          | Nanophotonics Optimization    | 나노포토닉스 최적화 |
| `materials`              | Materials Optimization        | 소재 최적화         |
| `autonomous-metal-lab`   | Metal Autonomous Laboratory   | 금속 자율실험실     |

Every publication and project carries a `pillar` field so the website can group them and the CV can highlight them.

## Editing conventions

- Author names: keep the existing convention — `C. Lee` for the author across all entries; `+` marks equal contribution, `*` marks corresponding author. The CV template bolds your name automatically.
- Dates: use `YYYY-MM` (or `YYYY-MM-DD` if exact) so sort order is reliable.
- New publication → add an entry to `data/publications.yaml`, give it a stable `id` like `lee2026-foo`, set `pillar`, then `./rebuild_all.sh`.
