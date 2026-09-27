"""Local browser smoke test. Requires Playwright and a running server on port 8787."""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright


BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
OUTPUT = Path(os.environ.get("LIBRARY_TEST_OUTPUT", "tmp/browser-qa"))
OUTPUT.mkdir(parents=True, exist_ok=True)


with sync_playwright() as playwright:
    launch_options = {"headless": True}
    if EDGE.exists():
        launch_options["executable_path"] = str(EDGE)
    browser = playwright.chromium.launch(**launch_options)
    desktop = browser.new_context(viewport={"width": 1440, "height": 900})
    page = desktop.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(BASE)
    page.locator(".book-card").wait_for()
    assert page.locator(".book-card").count() == 1
    page.screenshot(path=str(OUTPUT / "library-desktop.png"), full_page=True)

    page.get_by_role("link", name="阅读样章").click()
    page.locator("#reader-section-title").get_by_text("01 · 从十个点开始").wait_for()
    assert page.locator(".copy-en").count() == page.locator(".copy-zh").count() == 3
    page.screenshot(path=str(OUTPUT / "reader-desktop.png"), full_page=True)

    page.get_by_role("button", name="中文", exact=True).click()
    assert not page.locator(".copy-en").first.is_visible()
    assert page.locator(".copy-zh").first.is_visible()
    page.locator(".toc-link").nth(3).click()
    assert page.locator("#reader-section-title").inner_text() == "04 · 拟合与过拟合"
    page.reload()
    assert page.locator("#reader-section-title").inner_text() == "04 · 拟合与过拟合"
    page.goto(BASE)
    assert page.get_by_role("link", name="继续阅读").is_visible()

    page.evaluate("navigator.serviceWorker.ready")
    desktop.set_offline(True)
    page.goto(BASE + "?book=bishop-deep-learning-2024")
    assert page.locator("#reader-section-title").inner_text() == "04 · 拟合与过拟合"
    desktop.set_offline(False)

    mobile = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
    phone = mobile.new_page()
    phone.on("pageerror", lambda error: errors.append(str(error)))
    phone.goto(BASE + "?book=bishop-deep-learning-2024")
    phone.locator("#reader-section-title").get_by_text("01 · 从十个点开始").wait_for()
    phone.screenshot(path=str(OUTPUT / "reader-mobile.png"), full_page=True)
    dimensions = phone.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
    assert dimensions["content"] <= dimensions["viewport"], dimensions
    assert not errors, errors
    print(f"PASS: shelf, bilingual toggle, per-book resume, mobile width {dimensions}, no page errors")
    browser.close()
