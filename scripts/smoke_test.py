"""Local Chapter 1 browser smoke test. Requires a server on port 8787."""

import os
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
OUTPUT = Path(os.environ.get("LIBRARY_TEST_OUTPUT", "tmp/browser-qa"))
OUTPUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as playwright:
    installed = sorted((Path.home() / "AppData/Local/ms-playwright").glob("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
    options = {"headless": True}
    if installed:
        options["executable_path"] = str(installed[-1])
    browser = playwright.chromium.launch(**options)
    desktop = browser.new_context(viewport={"width": 1440, "height": 900})
    page = desktop.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(BASE)
    page.locator(".book-card").wait_for()
    assert page.locator(".book-card").count() == 1
    page.get_by_role("link", name="阅读第一章").click()
    page.locator(".reader-page-grid").wait_for()
    assert page.locator("#reader-count").inner_text() == "1 / 22"
    page.locator(".facsimile-link img").wait_for(state="visible")
    page.wait_for_function("document.querySelector('.facsimile-link img').naturalWidth > 0")
    assert "深度学习革命" in page.locator(".reader-page-translation").inner_text()
    page.screenshot(path=str(OUTPUT / "reader-desktop.png"), full_page=True)

    page.get_by_role("button", name="下一页").click()
    assert page.locator("#reader-count").inner_text() == "2 / 22"
    page.get_by_role("button", name="中文", exact=True).click()
    assert not page.locator(".reader-page-original").is_visible()
    assert page.locator(".reader-page-translation").is_visible()
    page.locator(".toc-link").last.click()
    assert page.locator("#reader-count").inner_text() == "20 / 22"
    page.get_by_role("button", name="下一页").click()
    page.get_by_role("button", name="下一页").click()
    assert page.locator("#reader-count").inner_text() == "22 / 22"
    assert "自动微分" in page.locator(".reader-page-translation").inner_text()
    page.reload()
    assert page.locator("#reader-count").inner_text() == "22 / 22"
    page.goto(BASE)
    assert page.get_by_role("link", name="继续阅读").is_visible()

    page.evaluate("navigator.serviceWorker.ready")
    desktop.set_offline(True)
    page.goto(BASE + "?book=bishop-deep-learning-2024")
    assert page.locator("#reader-count").inner_text() == "22 / 22"
    assert page.locator(".facsimile-link img").evaluate("image => image.complete && image.naturalWidth > 0")
    desktop.set_offline(False)

    mobile = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
    phone = mobile.new_page()
    phone.on("pageerror", lambda error: errors.append(str(error)))
    phone.goto(BASE + "?book=bishop-deep-learning-2024&page=14")
    phone.locator(".reader-page-grid").wait_for()
    assert phone.locator("#reader-count").inner_text() == "14 / 22"
    phone.screenshot(path=str(OUTPUT / "reader-mobile.png"), full_page=True)
    dimensions = phone.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
    assert dimensions["content"] <= dimensions["viewport"], dimensions
    assert not errors, errors
    print(f"PASS: 22 pages, bilingual toggle, resume, offline, mobile width {dimensions}, no page errors")
    browser.close()
