#!/usr/bin/env bash
# Rebuild every output from the YAML SSOT.
# Usage:  ./rebuild_all.sh           # build CV + LinkedIn drafts + Website
#         ./rebuild_all.sh cv        # CV only
#         ./rebuild_all.sh site      # Website only
#         ./rebuild_all.sh sns       # LinkedIn drafts only

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

target="${1:-all}"

build_cv()   { echo "▸ CV (Typst)";   python3 "$ROOT/CV/build_cv.py"; }
build_sns()  { echo "▸ LinkedIn drafts"; python3 "$ROOT/SNS/generate_posts.py"; }
build_site() {
  echo "▸ Website (Astro)"
  # Copy the latest CV PDF into the site's public/ so /cv.pdf works.
  if [ -f "$ROOT/CV/build/cv.pdf" ]; then
    mkdir -p "$ROOT/Website/public"
    cp "$ROOT/CV/build/cv.pdf" "$ROOT/Website/public/cv.pdf"
  fi
  cd "$ROOT/Website" && npm run build
}

case "$target" in
  cv)   build_cv ;;
  sns)  build_sns ;;
  site) build_cv && build_site ;;
  all)  build_cv && build_sns && build_site ;;
  *) echo "unknown target: $target"; exit 1 ;;
esac

echo "✓ done"
