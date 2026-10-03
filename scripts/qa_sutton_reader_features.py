"""Check Sutton/Barto reference links and first-use offline reading in a browser."""

import os
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/").rstrip("/") + "/"
BOOK = "sutton-barto-reinforcement-learning-2e"
CHROME = sorted((Path.home() / "AppData/Local/ms-playwright").glob(
    "chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"
))


def url(chapter: str) -> str:
    return f"{BASE}?book={BOOK}&chapter={chapter}"


def ready(page, chapter: str) -> None:
    page.goto(url(chapter))
    page.locator(".reading-block").first.wait_for()


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=True, **({"executable_path": str(CHROME[-1])} if CHROME else {})
    )

    links_context = browser.new_context(service_workers="block", viewport={"width": 390, "height": 844})
    page = links_context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    ready(page, "08")
    figure = page.locator("#read-p164-b17 a.reading-reference", has_text="图 8.2")
    assert figure.count() == 1 and figure.get_attribute("href") == "#read-p165-b01"
    exercise = page.locator("#read-p179-b01 a.reading-reference", has_text="习题 5.12")
    assert exercise.count() == 1
    exercise.click()
    page.wait_for_url("**chapter=05#read-p111-b05")
    assert page.locator("#read-p111-b05").count() == 1
    ready(page, "07")
    assert "chapter=06#read-p125-b01" in page.locator(
        "#reader-article a.reading-reference", has_text="例 6.2"
    ).first.get_attribute("href")
    ready(page, "16")
    assert page.locator("#read-p425-b02 a.reading-reference", has_text="表 16.1").get_attribute("href") == "#read-p425-b03"
    ready(page, "03")
    assert page.locator("#read-p68-b04 a.reading-reference", has_text="10.3").count() == 1
    assert page.locator("#read-p68-b04 a.reading-reference", has_text="10.4").count() == 1
    ready(page, "02")
    assert page.locator("#reader-article a.reading-reference", has_text="第二部分").count() >= 1
    assert not errors, errors
    links_context.close()

    offline_context = browser.new_context(service_workers="allow")
    page = offline_context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    ready(page, "01")
    page.wait_for_function(
        "document.querySelector('#offline-panel')?.dataset.state === 'complete'",
        timeout=120000,
    )
    assert page.locator("#offline-panel").is_hidden()
    assert page.locator("#offline-status").inner_text() == ""
    assert page.evaluate("""async () => {
      const cache = await caches.open('intelligence-library-images-v1');
      return (await cache.keys()).filter((request) =>
        request.url.includes('/books/sutton-barto-reinforcement-learning-2e/assets/')).length;
    }""") == 156
    offline_context.set_offline(True)
    ready(page, "16")  # This chapter and its images have not been opened online.
    image = page.locator(".book-figure img").first
    image.scroll_into_view_if_needed()
    image.evaluate("(element) => element.decode()")
    assert image.evaluate("(element) => element.naturalWidth") > 0
    assert int(page.locator("#reader-article").get_attribute("data-reference-links")) > 0
    destination = page.locator("#reader-article a.reading-reference", has_text="图 9.15")
    assert destination.count() == 1
    destination.click()
    page.wait_for_url("**chapter=09#read-p227-b04")
    image = page.locator("#read-p227-b04 img")
    image.evaluate("(element) => element.decode()")
    assert image.evaluate("(element) => element.naturalWidth") > 0
    assert not errors, errors
    offline_context.close()
    browser.close()

print("PASS: Sutton reference jumps and all 156 images on an unvisited offline chapter")
