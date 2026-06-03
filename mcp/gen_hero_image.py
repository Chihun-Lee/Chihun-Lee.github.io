"""One-off: generate the homepage hero research-synthesis image via Gemini.
Reads the API key from SNS/.env.local (bare key or GEMINI_API_KEY=... line).
Writes Website/public/assets/research-hero.png. Not wired into any pipeline.
"""
import os
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "Website" / "public" / "assets" / "research-hero.png"

# --- key ---
key = os.environ.get("GEMINI_API_KEY", "").strip()
if not key:
    raw = (ROOT / ".env.local").read_text().strip()
    key = raw.split("=", 1)[1].strip() if raw.startswith("GEMINI_API_KEY") else raw
if not key:
    sys.exit("No GEMINI_API_KEY found")

PROMPT = (
    "A minimal, abstract editorial illustration on a warm cream background (#F4EFE6). "
    "An elegant, calm composition that synthesizes four scientific research themes into one "
    "cohesive abstract artwork with generous negative space: "
    "(1) precision manufacturing — subtle geometric optimization curves and a faint gear motif; "
    "(2) nanophotonics — a delicate metasurface lattice of tiny pillars softly diffracting light into a faint spectrum; "
    "(3) materials science — organic crystalline microstructure grain boundaries; "
    "(4) an autonomous laboratory — a clean closed-loop Bayesian-optimization curve. "
    "Limited warm palette of terracotta (#CC785C), bronze (#B8956A), sage (#7A8C7E), and slate (#5C6B7A) on cream. "
    "Thin elegant linework, flat minimal vector aesthetic, sophisticated and museum-quality, balanced composition, "
    "no text, no words, no letters."
)

from google import genai
from google.genai import types

client = genai.Client(api_key=key)

# Try Gemini image-generation models, then fall back to Imagen.
gemini_models = ["gemini-2.5-flash-image", "gemini-2.0-flash-preview-image-generation"]
imagen_models = ["imagen-4.0-generate-001", "imagen-3.0-generate-002"]

saved = False
errors = []

for m in gemini_models:
    try:
        resp = client.models.generate_content(
            model=m,
            contents=PROMPT,
            config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
        )
        for part in resp.candidates[0].content.parts:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                OUT.write_bytes(part.inline_data.data)
                print(f"OK via {m} -> {OUT} ({OUT.stat().st_size} bytes)")
                saved = True
                break
        if saved:
            break
        errors.append(f"{m}: no image part returned")
    except Exception as e:
        errors.append(f"{m}: {e}")

if not saved:
    for m in imagen_models:
        try:
            resp = client.models.generate_images(
                model=m,
                prompt=PROMPT,
                config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="1:1"),
            )
            img = resp.generated_images[0].image
            OUT.write_bytes(img.image_bytes)
            print(f"OK via {m} -> {OUT} ({OUT.stat().st_size} bytes)")
            saved = True
            break
        except Exception as e:
            errors.append(f"{m}: {e}")

if not saved:
    print("FAILED. Tried:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
