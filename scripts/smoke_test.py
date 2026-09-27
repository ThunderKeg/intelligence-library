"""Browser smoke test for the continuous text reader."""

import os
import json
from pathlib import Path

from playwright.sync_api import Error, sync_playwright


BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
OUTPUT = Path(os.environ.get("LIBRARY_TEST_OUTPUT", "tmp/browser-qa"))
ROOT = Path(__file__).resolve().parents[1]
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
    page.get_by_role("button", name="切换深色模式").click()
    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert page.locator("#theme-toggle").get_attribute("aria-pressed") == "true"
    page.reload()
    assert page.locator("html").get_attribute("data-theme") == "dark"
    page.get_by_role("link", name="开始阅读").click()
    page.locator(".reading-block").first.wait_for()
    assert page.locator(".reading-block").count() == 124
    assert page.locator("#reader-toc .toc-link").count() == 17
    assert page.locator("#reader-toc-mobile .toc-link").count() == 17
    assert page.locator(".reader-article img").count() == 0
    assert "独家授权" not in page.locator(".reader-article").inner_text()
    assert page.locator(".reading-heading h1").inner_text() == "第 1 章 深度学习革命"
    assert page.locator("#chapter-navigation").is_hidden()
    page.screenshot(path=str(OUTPUT / "reader-desktop.png"), full_page=False)

    page.locator("#reader-toc .toc-link").last.click()
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
    phone.get_by_role("button", name="目录", exact=True).click()
    assert phone.locator("#toc-dialog").evaluate("dialog => dialog.open")
    assert phone.locator("#toc-toggle").get_attribute("aria-expanded") == "true"
    phone.screenshot(path=str(OUTPUT / "reader-mobile-toc.png"), full_page=False)
    phone.locator("#reader-toc-mobile a[href='#read-p20-t03']").click()
    assert not phone.locator("#toc-dialog").evaluate("dialog => dialog.open")
    phone.wait_for_function("location.hash === '#read-p20-t03'")
    phone.wait_for_function("Math.abs(document.getElementById('read-p20-t03').getBoundingClientRect().top) < 140")
    phone.screenshot(path=str(OUTPUT / "reader-mobile.png"), full_page=False)
    dimensions = phone.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
    assert dimensions["content"] <= dimensions["viewport"], dimensions

    system = browser.new_context(color_scheme="dark", service_workers="block")
    system_page = system.new_page()
    system_page.goto(BASE)
    assert system_page.locator("html").get_attribute("data-theme") == "dark"
    system_page.get_by_role("button", name="切换浅色模式").wait_for()
    system_page.emulate_media(color_scheme="light")
    system_page.wait_for_function("document.documentElement.dataset.theme === 'light'")
    system.close()

    mock = browser.new_context(service_workers="block")
    mock_script = (ROOT / "books.js").read_text(encoding="utf-8") + '\nbooks[0].chapters.push({id:"02",number:"2",title:"测试章节",content:"books/bishop-deep-learning-2024/chapter-02.json"});'
    mock.route("**/books.js", lambda route: route.fulfill(body=mock_script, content_type="application/javascript"))
    second = json.loads((ROOT / "books/bishop-deep-learning-2024/chapter-01.json").read_text(encoding="utf-8"))
    second["toc"] = [{**entry, "number": "2" + entry["number"][1:]} for entry in second["toc"]]
    second["toc"][0]["title"] = "测试章节"
    second["blocks"][0]["text"] = "第 2 章 测试章节"
    mock.route("**/chapter-02.json", lambda route: route.fulfill(body=json.dumps(second, ensure_ascii=False), content_type="application/json"))
    mock_page = mock.new_page()
    mock_page.goto(BASE + "?book=bishop-deep-learning-2024&chapter=01")
    mock_page.locator(".reading-block").first.wait_for()
    assert mock_page.locator("#reader-toc .toc-chapter-link").count() == 2
    mock_page.get_by_role("link", name="下一章").click()
    mock_page.locator(".reading-heading h1").get_by_text("第 2 章 测试章节").wait_for()
    assert "chapter=02" in mock_page.url
    assert json.loads(mock_page.evaluate("localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')"))["chapter"] == "02"
    mock_page.goto(BASE)
    assert "chapter=02" in mock_page.get_by_role("link", name="继续阅读").get_attribute("href")
    mock.close()

    assert not errors, errors
    print(f"PASS: contents, themes, chapter navigation, resume, offline, mobile width {dimensions}, no page errors")
    browser.close()
