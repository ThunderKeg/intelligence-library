"""Check the actual Sutton/Barto chapter in the reader."""

import json
import os
import unicodedata
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
OUTPUT = Path(os.environ.get("LIBRARY_TEST_OUTPUT", "tmp/browser-qa"))
OUTPUT.mkdir(parents=True, exist_ok=True)
BOOK_ID = "sutton-barto-reinforcement-learning-2e"
CHAPTER = json.loads((ROOT / "books" / BOOK_ID / "chapter-01.json").read_text(encoding="utf-8"))

with sync_playwright() as playwright:
    installed = sorted((Path.home() / "AppData/Local/ms-playwright").glob("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
    browser = playwright.chromium.launch(headless=True, **({"executable_path": str(installed[-1])} if installed else {}))
    for label, width, height in (("desktop", 1440, 900), ("mobile", 390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height}, service_workers="block")
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(BASE + "?book=" + BOOK_ID + "&chapter=01")
        page.locator(".reading-block").first.wait_for()
        assert page.locator(".reading-block").count() == len(CHAPTER["blocks"])
        assert page.locator("#reader-toc .toc-section-link").count() == 7
        assert page.locator(".reading-intro").count() == 1
        assert page.locator(".book-figure img").count() == 2
        for image in page.locator(".book-figure img").all():
            image.scroll_into_view_if_needed()
            image.evaluate("img => { img.loading = 'eager'; return img.decode(); }")
            assert image.evaluate("img => img.naturalWidth > 0")
        assert page.locator(".book-formula math").count() == 1
        selected_formula = page.locator(".book-formula math").evaluate(
            "math => { const range = document.createRange(); range.selectNodeContents(math); "
            "const selection = getSelection(); selection.removeAllRanges(); selection.addRange(range); "
            "const result = selection.toString(); selection.removeAllRanges(); return result; }"
        )
        normalized_formula = unicodedata.normalize("NFKC", selected_formula)
        assert "V" in normalized_formula and "α" in normalized_formula, selected_formula
        assert "习题 1.5" in page.locator(".reader-article").inner_text()
        if label == "mobile":
            page.locator("#theme-toggle").click()
            assert page.locator("html").get_attribute("data-theme") == "dark"
            page.locator(".book-formula").scroll_into_view_if_needed()
            page.screenshot(path=str(OUTPUT / "reader-sutton-mobile-formula.png"))
            page.locator(".book-figure").last.scroll_into_view_if_needed()
        else:
            page.evaluate("document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, 0)")
        dimensions = page.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
        assert dimensions["content"] <= dimensions["viewport"], dimensions
        page.screenshot(path=str(OUTPUT / f"reader-sutton-{label}.png"))
        assert not errors, errors
        context.close()
    browser.close()

print(f"PASS: chapter {len(CHAPTER['blocks'])} blocks, two images, MathML, mobile and desktop")
