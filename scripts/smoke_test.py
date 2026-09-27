"""Browser smoke test for the continuous text reader."""

import os
from pathlib import Path

from playwright.sync_api import Error, sync_playwright


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
    page.locator(".book-card").first.wait_for()
    assert page.locator(".book-card").count() == 1
    page.get_by_role("link", name="开始阅读").click()
    page.locator(".reading-block").first.wait_for()
    assert page.locator(".reading-block").count() == 124
    assert page.locator(".toc-link").count() == 17
    assert page.locator(".reader-article img").count() == 0
    assert "独家授权" not in page.locator(".reader-article").inner_text()
    assert page.locator(".reading-heading h1").inner_text() == "第 1 章 深度学习革命"
    page.screenshot(path=str(OUTPUT / "reader-desktop.png"), full_page=False)

    page.locator(".toc-link").last.click()
    page.wait_for_function("location.hash === '#read-p20-t03'")
    page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).page >= 20")
    try:
        page.reload()
    except Error as error:
        if "ERR_ABORTED" not in str(error):
            raise
        page.wait_for_load_state("load")
    page.locator(".reading-block").first.wait_for()
    page.wait_for_function("window.scrollY > 1000")
    page.goto(BASE)
    assert page.get_by_role("link", name="继续阅读").is_visible()

    page.evaluate("navigator.serviceWorker.ready")
    desktop.set_offline(True)
    page.goto(BASE + "?book=bishop-deep-learning-2024")
    assert page.locator(".reading-block").count() == 124
    desktop.set_offline(False)

    mobile = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
    phone = mobile.new_page()
    phone.on("pageerror", lambda error: errors.append(str(error)))
    phone.goto(BASE + "?book=bishop-deep-learning-2024#read-p14-t06")
    phone.locator(".reading-block").first.wait_for()
    phone.wait_for_function("Math.abs(document.getElementById('read-p14-t06').getBoundingClientRect().top) < 100")
    assert not phone.locator("#reader-menu").evaluate("menu => menu.open")
    phone.screenshot(path=str(OUTPUT / "reader-mobile.png"), full_page=False)
    dimensions = phone.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
    assert dimensions["content"] <= dimensions["viewport"], dimensions
    assert not errors, errors
    print(f"PASS: 124 text blocks, 17 contents links, resume, offline, mobile width {dimensions}, no page errors")
    browser.close()
