# SNS — LinkedIn post drafts

Tiny generator that turns every entry in the SSOT YAML (`/Users/chihun/Code/SNS/data/`)
into a copy-paste-ready LinkedIn post draft under `posts/`.

There is **no LinkedIn API integration** in v1. The flow is:

1. Run the generator — it reads `data/publications.yaml` and `data/talks.yaml`
   (read-only) and writes one markdown file per row.
2. Open the file in `posts/`, edit the `<!-- TODO -->` placeholders, tweak the
   hook / hashtags.
3. Copy the body (everything below the YAML front matter) into LinkedIn.
4. Flip `status: draft` → `status: published` in the front matter so the next
   regeneration leaves your edits alone.

## Usage

```bash
cd /Users/chihun/Code/SNS/SNS
pip install --quiet pyyaml
python3 generate_posts.py
```

Force-regenerate **every** post (overwriting any `status: published` posts —
use with care):

```bash
python3 generate_posts.py --force
```

## File naming

- Publications → `posts/pub-<publication-id>.md` (id comes from the YAML).
- Talks → `posts/talk-<venue+title-slug>.md`.

## Pillar-aware hooks

Each publication's `pillar:` field picks both:
- a one-sentence framing hook ("Inverse design keeps showing…", etc.), and
- a hashtag set:

| pillar | hashtags |
| --- | --- |
| `manufacturing` | `#AIforManufacturing #SmartManufacturing` |
| `nanophotonics` | `#Nanophotonics #Metasurface #InverseDesign` |
| `materials` | `#Materials #MaterialsInformatics` |
| `autonomous-metal-lab` | `#AutonomousLab #ActiveLearning #LPBF` |

Anything else falls back to `#AIforMaterials #AIforManufacturing`.

## Author bolding

`C. Lee` is wrapped in `**…**` so it stands out in the rendered preview. The
‘+’ and ‘*’ markers (equal contribution, corresponding) are preserved.

## Skipping already-published posts

The generator opens any existing `posts/<id>.md`, parses the front matter, and
skips writing if `status: published`. Mark a post as published once you've
actually posted it on LinkedIn:

```yaml
---
id: pub-lee2025-benchmarking
type: publication
status: published       # ← change this
source_id: lee2025-benchmarking
---
```
