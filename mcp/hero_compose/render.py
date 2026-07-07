"""홈페이지 히어로(리뷰논문 Figure 1 스타일) 렌더러.

compose_hero.html(3기둥 다이어그램)을 Playwright로 2x 스크린샷 →
Website/public/assets/sdl-hero.png. 장비 사진 크롭은 ICML 포스터 equip.png에서,
nano/manu 패널 사진은 Gemini 생성(mcp/gen_sdl_hero.py 참조).

실행: conda ekp 환경 (playwright 설치됨)
  /opt/homebrew/Caskroom/miniforge/base/envs/ekp/bin/python render.py
"""
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent.parent / "Website" / "public" / "assets" / "sdl-hero.png"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1660, "height": 950}, device_scale_factor=2)
    pg.goto(f"file://{HERE}/compose_hero.html")
    pg.wait_for_timeout(500)
    pg.locator("#canvas").screenshot(path=str(OUT))
    b.close()
print(f"OK -> {OUT}")
