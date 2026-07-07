"""One-off: generate the Welcome-page "Metal Alloy SDL with AI Agent" hero image via Gemini.
Concept v2 (2026-07): NOT abstract — looks like a workflow slide a researcher made in
PowerPoint: photographic equipment cutouts, rounded label pills, clean arrows.
Reference: ICML poster equip.png (real equipment workflow diagram).
Reads the API key from SNS/.env.local. Writes Website/public/assets/sdl-hero.png.
"""
import os
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "Website" / "public" / "assets" / "sdl-hero.png"

REFS = [
    pathlib.Path("/Users/chihun/Code/ICML_workshop/poster/final/poster_editable/equip.png"),
]

key = os.environ.get("GEMINI_API_KEY", "").strip()
if not key:
    raw = (ROOT / ".env.local").read_text().strip()
    key = raw.split("=", 1)[1].strip() if raw.startswith("GEMINI_API_KEY") else raw
if not key:
    sys.exit("No GEMINI_API_KEY found")

PROMPT = (
    "Recreate this equipment workflow diagram as a SIMPLIFIED, wide 16:9 hero version, in exactly "
    "the same visual language: a clean scientific workflow slide that a researcher made by hand in "
    "PowerPoint — photographic cutouts of real lab equipment, rounded-rectangle label pills, and "
    "simple straight arrows. Absolutely no abstract illustration, no isometric art, no painterly "
    "or AI-art style. "
    "Layout, left to right in one closed loop: "
    "(1) a rounded rectangle labeled 'AI Agent' → "
    "(2) glass vials of metal powders labeled 'Raw powders' → "
    "(3) a large industrial metal 3D printer machine labeled 'DED printing' → "
    "(4) a laboratory furnace labeled 'Heat treatment' → "
    "(5) a tensile testing machine with robot arm labeled 'Tensile test' → "
    "(6) microscopes/analysis instruments labeled 'SEM · XRD' → "
    "an arrow labeled 'Data' returning from the last station back to the 'AI Agent' box, closing "
    "the loop. "
    "Use SHORT labels exactly as given above, in a clean sans-serif font, spelled correctly. "
    "Background: plain very light warm cream (#F7F3EC). Label pills: terracotta (#CC785C) with "
    "white text; arrows: dark slate gray. Equipment images look like real photographs cut out on "
    "the plain background, similar to the reference. Flat, tidy, presentation-slide aesthetic with "
    "generous spacing. No watermark, no extra text beyond the labels listed."
)

from google import genai
from google.genai import types

client = genai.Client(api_key=key)

parts = []
for ref in REFS:
    if ref.exists():
        parts.append(types.Part.from_bytes(data=ref.read_bytes(), mime_type="image/png"))
    else:
        print(f"warn: missing reference {ref}")
parts.append(types.Part.from_text(text=PROMPT))

errors = []
saved = False
for cfg in (
    types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(aspect_ratio="16:9"),
    ),
    types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
):
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[types.Content(role="user", parts=parts)],
            config=cfg,
        )
        for part in resp.candidates[0].content.parts:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                OUT.write_bytes(part.inline_data.data)
                print(f"OK -> {OUT} ({OUT.stat().st_size} bytes)")
                saved = True
                break
        if saved:
            break
        errors.append("no image part returned")
    except Exception as e:
        errors.append(str(e)[:300])

if not saved:
    print("FAILED:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
