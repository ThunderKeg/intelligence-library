"""Check the Sutton/Barto front matter and chapter 2 in the reader."""

import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
OUTPUT = Path(os.environ.get("LIBRARY_TEST_OUTPUT", "tmp/browser-qa"))
OUTPUT.mkdir(parents=True, exist_ok=True)
BOOK_ID = "sutton-barto-reinforcement-learning-2e"
BOOK = ROOT / "books" / BOOK_ID
FRONT = json.loads((BOOK / "chapter-00.json").read_text(encoding="utf-8"))
CHAPTER = json.loads((BOOK / "chapter-02.json").read_text(encoding="utf-8"))


with sync_playwright() as playwright:
    installed = sorted((Path.home() / "AppData/Local/ms-playwright").glob("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
    browser = playwright.chromium.launch(headless=True, **({"executable_path": str(installed[-1])} if installed else {}))
    for chapter_id, label, expected in (("00", "front", FRONT), ("02", "chapter2", CHAPTER)):
        for screen, width, height in (("desktop", 1440, 900), ("mobile", 390, 844)):
            context = browser.new_context(viewport={"width": width, "height": height}, service_workers="block")
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(BASE + f"?book={BOOK_ID}&chapter={chapter_id}")
            page.locator(".reading-block").first.wait_for()
            if chapter_id == "00":
                assert page.locator(".reading-block").count() == len(expected["blocks"])
                assert page.locator(".book-table").count() == 17
                assert page.locator(".book-table math").count() >= 20
                assert page.locator(".book-list li").count() == 171
                assert page.locator(".book-list .book-list li").count() > 0
                assert page.locator(".book-figure img").count() == 1
                page.locator(".book-figure img").evaluate("img => img.decode()")
                assert page.locator(".book-figure img").evaluate("img => img.naturalWidth > 0")
                assert "树备份" in page.locator(".reader-article").inner_text()
                assert "树回溯" not in page.locator(".reader-article").inner_text()
            else:
                assert page.locator(".reading-block").count() == 158
                assert page.locator(".book-figure img").count() == 6
                assert page.locator(".book-formula math").count() == 13
                assert page.locator(".book-exercise").count() == 11
                assert page.locator(".book-box").count() == 1
                assert page.locator(".book-code").count() == 1
                for image in page.locator(".book-figure img").all():
                    image.evaluate("img => { img.loading = 'eager'; return img.decode(); }")
                    assert image.evaluate("img => img.naturalWidth > 0")
                text = page.locator(".reader-article").inner_text()
                assert "*k*" not in text and "∑ᵦ" not in text
            if screen == "mobile":
                page.locator("#theme-toggle").click()
                assert page.locator("html").get_attribute("data-theme") == "dark"
            if chapter_id == "00":
                page.locator(".book-table").last.scroll_into_view_if_needed()
            else:
                page.locator(".book-box").scroll_into_view_if_needed()
            dims = page.evaluate("({width: innerWidth, scroll: document.documentElement.scrollWidth})")
            assert dims["scroll"] <= dims["width"], dims
            page.screenshot(path=str(OUTPUT / f"reader-sutton-{label}-{screen}.png"))
            assert not errors, errors
            context.close()
    browser.close()

print("PASS: registered front matter and chapter 2, source assets, math, code, box, desktop and mobile")
