# CV — Typst pipeline

Single-source-of-truth CV that compiles from the YAML files under `/Users/chihun/Code/홍보_SNS/SNS/data/`.

## Requirements

- **Typst** (`brew install typst` on macOS)
- **Python 3** with `pyyaml` (`pip install pyyaml`)

## Build

```bash
cd /Users/chihun/Code/홍보_SNS/SNS/CV
pip install pyyaml
python3 build_cv.py            # → build/cv.pdf
python3 build_cv.py --no-pdf   # just emit build/cv.typ
```

## Files

- `template.typ` — Typst template (page, fonts, helpers: `cv`, `section`, `entry`, `item`)
- `build_cv.py` — reads `../data/*.yaml`, renders `build/cv.typ`, compiles `build/cv.pdf`
- `build/` — generated outputs (ignored by git)

## Editing content

Edit only the YAML SSOT under `../data/`. The DOCX in this folder (`Curriculum Vitae Chihun Lee (2025.11).docx`) is a historical reference and is not used by the pipeline.
