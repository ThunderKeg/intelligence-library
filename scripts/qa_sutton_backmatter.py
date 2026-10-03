"""Preview the Sutton/Barto backmatter before registering reviewed sections."""

import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BOOK_ID = "sutton-barto-reinforcement-learning-2e"
BOOK = ROOT / "books" / BOOK_ID
BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
OUTPUT = ROOT / "tmp" / "browser-qa"
OUTPUT.mkdir(parents=True, exist_ok=True)
INDEX = (ROOT / "books.js").read_text(encoding="utf-8")
ANCHOR = f'      {{ id: "17", number: "17", title: "前沿问题", content: "books/{BOOK_ID}/chapter-17.json" }},'
assert INDEX.count(ANCHOR) == 1
SECTIONS = {"REF": (783, "参考文献"), "IDX": (531, "索引"), "SERIES": (26, "系列书目")}
ADDED = "\n".join(
    f'      {{ id: "{stem}", number: "", title: "{title}", content: "books/{BOOK_ID}/chapter-{stem}.json" }},'
    for stem, (_, title) in SECTIONS.items()
    if f'content: "books/{BOOK_ID}/chapter-{stem}.json"' not in INDEX
)
PREVIEW_INDEX = INDEX.replace(ANCHOR, ANCHOR + ("\n" + ADDED if ADDED else ""), 1)


with sync_playwright() as playwright:
    installed = sorted((Path.home() / "AppData/Local/ms-playwright").glob(
        "chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
    browser = playwright.chromium.launch(headless=True,
                                         **({"executable_path": str(installed[-1])} if installed else {}))
    for stem, (count, title) in SECTIONS.items():
        chapter = json.loads((BOOK / f"chapter-{stem}.json").read_text(encoding="utf-8"))
        assert len(chapter["blocks"]) == count, (stem, "source count")
        for label, width, height in (("desktop", 1440, 900), ("mobile-dark", 390, 844)):
            context = browser.new_context(viewport={"width": width, "height": height}, service_workers="block")
            context.route("**/books.js", lambda route: route.fulfill(body=PREVIEW_INDEX,
                                                               content_type="application/javascript"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(BASE + f"?book={BOOK_ID}&chapter={stem}")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == count, (stem, label, "render count")
            expected_heading = "自适应计算与机器学习" if stem == "SERIES" else title
            assert expected_heading in page.locator("#reader-article h1").inner_text()
            if stem == "REF":
                assert page.locator(".reading-reference-entry").count() == 782
                assert "Iinterference" in page.locator("#reader-article").inner_text()
            elif stem == "IDX":
                assert page.locator(".sutton-index-level-0").count() == 290
                assert page.locator(".reading-rich .index-entry").count() == 529
                assert page.locator(".reading-rich .index-entry a").count() > 600
                assert page.locator(".reading-rich .index-entry math").count() >= 5
                links = page.locator(".reading-rich .index-entry a")
                assert all(f"book={BOOK_ID}" in link.get_attribute("href") for link in links.all())
            else:
                assert page.locator(".reading-catalog-entry").count() == 24
                assert page.locator(".reading-catalog-entry em").count() == 24
            if label == "mobile-dark":
                page.locator("#theme-toggle").click()
                assert page.locator("html").get_attribute("data-theme") == "dark"
            dimensions = page.evaluate("({width:innerWidth, scroll:document.documentElement.scrollWidth})")
            assert dimensions["scroll"] <= dimensions["width"], (stem, label, dimensions)
            page.screenshot(path=str(OUTPUT / f"sutton-{stem}-{label}.png"))
            if stem == "IDX" and label == "desktop":
                page.locator(".reading-rich .index-entry a").first.click()
                page.locator("#reader-article h1").wait_for()
                assert "chapter=02" in page.url and "page=25" in page.url
                assert "第 2 章" in page.locator("#reader-article h1").inner_text()
            assert not errors, (stem, label, errors)
            print(f"PASS {stem} {label}: {count} blocks, no page overflow or JS errors")
            context.close()
    context = browser.new_context(viewport={"width": 1440, "height": 900}, service_workers="block")
    page = context.new_page()
    page.goto(BASE + f"?book={BOOK_ID}&chapter=00")
    page.locator(".reading-block").first.wait_for()
    contents_links = page.locator("#reader-article .contents-reader-link")
    assert contents_links.count() == 191, "Original contents should link to every listed chapter and section"
    page.locator('#reader-article a[href*="chapter=REF"]').click()
    assert "chapter=REF" in page.url
    assert "参考文献" in page.locator("#reader-article h1").inner_text()
    print("PASS original contents: 191 working reader links")
    context.close()
    browser.close()
