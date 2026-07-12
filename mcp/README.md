# chihun-cv-mcp

FastMCP server that lets an AI agent (or Claude in another session) edit the
SSOT YAML files under `/Users/chihun/Code/홍보_SNS/SNS/data/` and trigger the CV,
website, and LinkedIn-post builders.

## Install

```bash
pip install -e /Users/chihun/Code/홍보_SNS/SNS/mcp
```

or, if you prefer pinning explicitly without an editable install:

```bash
pip install fastmcp pyyaml 'ruamel.yaml>=0.18'
```

(With the `3dp` miniforge env on this machine, the binary path is
`/opt/homebrew/Caskroom/miniforge/base/envs/3dp/bin/python`.)

## Register with Claude Code

Either run:

```bash
claude mcp add chihun-cv-mcp -- python3 /Users/chihun/Code/홍보_SNS/SNS/mcp/server.py
```

…or drop this into `~/.claude.json` under `"mcpServers"`:

```json
"chihun-cv-mcp": {
  "command": "python3",
  "args": ["/Users/chihun/Code/홍보_SNS/SNS/mcp/server.py"]
}
```

If you installed the conda env, point `command` at that python binary
explicitly (the system `python3` from Homebrew is PEP 668-managed and will
not see `fastmcp`).

## Tools exposed

| Tool | What it does |
| --- | --- |
| `add_publication` | Append a row to `data/publications.yaml`. Auto-derives `id` as `lee<year>-<3-word-slug>`. |
| `add_talk` | Append a row to `data/talks.yaml`. |
| `add_project` | Append a row to `data/projects.yaml`. |
| `add_news` | Prepend a row to `data/news.yaml` (newest first). |
| `update_profile_field` | Dotted-path update inside `data/profile.yaml` (path must exist). |
| `list_publications` | Filter publications by `pillar`, `year`, and/or `role`. |
| `build_cv` | Run `python3 CV/build_cv.py`. |
| `build_site` | Run `npm run build` inside `Website/`. |
| `generate_linkedin_posts` | Run `SNS/generate_posts.py`. |
| `git_status` | Run `git status --short` in the SSOT repo (handles "not a repo" gracefully). |

## Design notes

- Reads use **ruamel.yaml** round-trip mode (preserves comments and key order
  where possible). Falls back to PyYAML safe-load/safe-dump if ruamel is
  unavailable.
- All inputs are validated against allowed enums (`pillar`, `role`, `type`)
  before any YAML is written.
- Builders (`build_cv`, `build_site`, `generate_linkedin_posts`) **never**
  run implicitly after an edit — call them explicitly.
- The server does **not** mutate the LinkedIn post drafts in `SNS/posts/` —
  those are owned by `generate_posts.py`.
