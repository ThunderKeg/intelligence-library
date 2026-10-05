"""Cross-book browser checks for figure and equation previews.

Start a local HTTP server before running this script. LIBRARY_TEST_URL overrides
the default http://127.0.0.1:8787/ address.
"""

import os
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
OUTPUT = Path(os.environ.get("LIBRARY_TEST_OUTPUT", "tmp/browser-qa"))
OUTPUT.mkdir(parents=True, exist_ok=True)


def open_chapter(page, book, chapter):
    page.goto(f"{BASE}?book={book}&chapter={chapter}")
    page.locator("#reader-article .reading-block").first.wait_for()
    assert page.locator("#reader-status").is_hidden()


def preview(page, kind, number):
    link = page.locator(f'a[data-preview-kind="{kind}"][data-preview-number="{number}"]').first
    assert link.count() == 1, (kind, number)
    link.click()
    dialog = page.locator(".reference-preview-dialog")
    dialog.locator(".reference-preview-content").wait_for()
    assert dialog.evaluate("node => node.open")
    assert "预览暂时无法加载" not in dialog.inner_text()
    return link, dialog


with sync_playwright() as playwright:
    installed = sorted((Path.home() / "AppData/Local/ms-playwright").glob(
        "chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
    browser = playwright.chromium.launch(
        headless=True, **({"executable_path": str(installed[-1])} if installed else {}))
    context = browser.new_context(viewport={"width": 1280, "height": 800}, service_workers="block")
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))

    for book, chapter, number in (
        ("bishop-pattern-recognition-2006", "chapter-06", "6.13"),
        ("sutton-barto-reinforcement-learning-2e", "11", "11.13"),
        ("mackay-information-theory-2003", "20", "20.7"),
    ):
        open_chapter(page, book, chapter)
        _, dialog = preview(page, "formula", number)
        assert dialog.locator("math").count() >= 1
        assert dialog.locator(".book-formula").count() == 1
        page.keyboard.press("Escape")

    open_chapter(page, "mackay-information-theory-2003", "30")
    alias = page.locator("a.reading-reference").filter(has_text="图 30.1").first
    assert alias.count() == 1 and alias.get_attribute("data-preview-kind") is None
    assert alias.get_attribute("href").endswith("#read-p400-b001")

    open_chapter(page, "shannon-mathematical-theory-1948", "01")
    link, dialog = preview(page, "figure", "2")
    assert link.get_attribute("href").endswith("#fig-2")
    assert dialog.locator("figure img").evaluate("img => img.complete && img.naturalWidth > 0")
    assert "图 2" in dialog.locator("figcaption").inner_text()
    page.keyboard.press("Escape")

    open_chapter(page, "boyd-vandenberghe-convex-optimization-2004", "10")
    link, dialog = preview(page, "formula", "10.26")
    assert link.get_attribute("href").endswith("#eq-10-26")
    assert dialog.locator(".book-formula").count() == 1  # Its source block also has 10.27.
    assert "10.26" in dialog.inner_text() and "10.27" not in dialog.inner_text()
    assert dialog.locator("[id='eq-10-26']").count() == 0  # No duplicate IDs in the page.
    dialog.screenshot(path=str(OUTPUT / "boyd-formula-preview.png"))
    page.keyboard.press("Escape")

    open_chapter(page, "boyd-vandenberghe-convex-optimization-2004", "02")
    link = page.locator('a[data-preview-kind="figure"][data-preview-number="2.1"]').first
    link.hover()
    page.locator(".reference-preview-tooltip figure img").wait_for()
    assert page.locator(".reference-preview-tooltip figure").count() == 1
    _, dialog = preview(page, "figure", "2.1")
    assert dialog.locator("figure img").evaluate("img => img.complete && img.naturalWidth > 0")
    page.keyboard.press("Escape")

    mobile = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                                 has_touch=True, service_workers="block")
    phone = mobile.new_page()
    phone.on("pageerror", lambda error: errors.append(str(error)))
    open_chapter(phone, "shannon-mathematical-theory-1948", "01")
    _, dialog = preview(phone, "figure", "2")
    assert dialog.bounding_box()["width"] <= phone.evaluate("innerWidth")
    assert dialog.locator("figure img").evaluate("img => img.complete && img.naturalWidth > 0")
    phone.screenshot(path=str(OUTPUT / "shannon-figure-preview-mobile.png"))
    phone.keyboard.press("Escape")

    assert not errors, errors
    print("PASS: five books, nested formulas, exact rich targets, alias, hover, mobile, no page errors")
    browser.close()
