"""Check the complete Shannon translation in the static reader.

Start `python -m http.server 8787 --bind 127.0.0.1` first.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "shannon-mathematical-theory-1948"
BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
OUTPUT = ROOT / "tmp" / "shannon-qa"
CHAPTERS = ("00", "01", "02", "a1-a4", "03", "04", "05", "a5-a7")
BOOK_ID = "shannon-mathematical-theory-1948"


def chapter_url(chapter: str) -> str:
    return f"{BASE}?book={BOOK_ID}&chapter={chapter}"


def browser_options() -> dict:
    installed = sorted(
        (Path.home() / "AppData/Local/ms-playwright").glob(
            "chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"
        )
    )
    return {"headless": True, **({"executable_path": str(installed[-1])} if installed else {})}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    documents = [
        json.loads((BOOK / f"chapter-{chapter}.json").read_text(encoding="utf-8"))
        for chapter in CHAPTERS
    ]
    pages = {page for document in documents for page in range(document["sourcePdfPages"][0], document["sourcePdfPages"][1] + 1)}
    sections = [entry["number"] for document in documents for entry in document["toc"] if re.fullmatch(r"\d+", entry["number"])]
    appendices = [entry["number"] for document in documents for entry in document["toc"] if re.fullmatch(r"附录 [1-7]", entry["number"])]
    images = [path for document in documents for path in document["images"]]
    expected_images = {f"books/{BOOK_ID}/assets/fig-{number}.png" for number in range(1, 13)}
    expected_images.add(f"books/{BOOK_ID}/assets/table-i-original.png")
    assert pages == set(range(1, 56))
    assert sections == [str(number) for number in range(1, 30)]
    assert appendices == [f"附录 {number}" for number in range(1, 8)]
    assert len(images) == 13 and set(images) == expected_images
    errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(**browser_options())
        mobile = browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=1,
            is_mobile=True,
            has_touch=True,
            service_workers="block",
        )
        page = mobile.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))

        for chapter, document in zip(CHAPTERS, documents):
            page.goto(chapter_url(chapter))
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == len(document["blocks"]), chapter
            assert page.locator(".reading-rich").count() > 0, chapter
            assert page.locator(".reading-intro").count() == 1, chapter
            assert page.locator(".reader-article figure").count() == len(document["images"]), chapter
            assert page.locator(".figure-translation").count() == len(document["images"]), chapter
            assert page.locator("#reader-toc-mobile .toc-link").count() == len(CHAPTERS) + len(document["toc"]) - 1, chapter
            size = page.evaluate("({width: innerWidth, content: document.documentElement.scrollWidth})")
            assert size["content"] <= size["width"], (chapter, size)
            math = page.evaluate(
                """() => [...document.querySelectorAll('.reader-article math')].every(
                    node => node.namespaceURI === 'http://www.w3.org/1998/Math/MathML'
                )"""
            )
            assert math, chapter
            assert page.locator(".reader-article math").count() > 0, chapter
            image_status = page.evaluate(
                """async () => Promise.all([...document.querySelectorAll('.reader-article img')].map(
                    async img => { img.loading = 'eager'; try { await img.decode(); return img.naturalWidth > 0; } catch { return false; } }
                ))"""
            )
            assert all(image_status), (chapter, image_status)
            broken = page.evaluate(
                """() => [...document.querySelectorAll('.reader-article a[href^="#"]')]
                    .filter(a => !document.getElementById(decodeURIComponent(a.hash.slice(1))))
                    .map(a => a.outerHTML)"""
            )
            assert not broken, (chapter, broken)
            if chapter == "01":
                assert page.locator(".book-code").count() == 11
                assert page.locator(".book-table").count() == 4
                page.locator("#fig-4").scroll_into_view_if_needed()
                page.screenshot(path=str(OUTPUT / "first-part-mobile.png"))
            elif chapter == "03":
                assert page.locator(".book-table").count() == 1
                page.locator(".book-table").scroll_into_view_if_needed()
                page.screenshot(path=str(OUTPUT / "table-i-mobile.png"))
            elif chapter == "05":
                assert page.locator(".reader-article ol > li").count() >= 5
            print(f"{chapter}: {len(document['blocks'])} blocks, {page.locator('.reader-article math').count()} MathML, {len(document['images'])} images")

        page.goto(chapter_url("01"))
        page.locator(".reading-block").first.wait_for()
        reserved = page.evaluate(
            """() => [...document.querySelectorAll('.reader-article img')].every(
                img => img.getBoundingClientRect().height > 0
            )"""
        )
        assert reserved, "Lazy images must reserve their layout height"
        page.locator('a[href="#fn:3"]').first.click()
        page.wait_for_function(
            """() => { const top = document.getElementById('fn:3').getBoundingClientRect().top;
                return top >= 60 && top < 160; }"""
        )
        page.goto(chapter_url("01"))
        page.locator(".reading-block").first.wait_for()
        page.get_by_role("button", name="目录", exact=True).click()
        assert page.locator("#toc-dialog").evaluate("dialog => dialog.open")
        tenth = page.locator("#reader-toc-mobile .toc-section-link").last
        target = tenth.get_attribute("href")
        tenth.click()
        page.wait_for_function(
            """hash => { const top = document.querySelector(hash).getBoundingClientRect().top;
                return top >= 60 && top < 160; }""",
            arg=target,
        )
        page.get_by_role("button", name="目录", exact=True).click()
        page.locator("#reader-toc-mobile a[href*='chapter=02']").click()
        page.locator(".reading-heading h1").get_by_text("第二篇").wait_for()
        assert "chapter=02" in page.url
        page.locator(".reading-block").last.scroll_into_view_if_needed()
        page.wait_for_function(
            f"JSON.parse(localStorage.getItem('intelligence-library:progress:v2:{BOOK_ID}'))?.chapter === '02'"
        )
        page.goto(BASE)
        assert "chapter=02" in page.get_by_role("link", name="继续阅读").get_attribute("href")
        page.goto(chapter_url("05"))
        page.locator('.reader-article a[href*="fig-10"]').click()
        page.locator("#fig-10").wait_for()
        page.wait_for_function(
            """() => { const box = document.querySelector('#fig-10').getBoundingClientRect();
                return box.top < innerHeight && box.bottom > 0; }"""
        )

        dark = browser.new_context(viewport={"width": 1440, "height": 900}, color_scheme="dark", service_workers="block")
        dark_page = dark.new_page()
        dark_page.on("pageerror", lambda error: errors.append(str(error)))
        dark_page.goto(chapter_url("03"))
        dark_page.locator(".reading-block").first.wait_for()
        assert dark_page.locator("html").get_attribute("data-theme") == "dark"
        dark_page.locator(".book-table").scroll_into_view_if_needed()
        dark_page.screenshot(path=str(OUTPUT / "table-i-dark-desktop.png"))

        online = browser.new_context()
        offline_page = online.new_page()
        offline_page.on("pageerror", lambda error: errors.append(str(error)))
        offline_page.goto(chapter_url("00"))
        offline_page.evaluate("navigator.serviceWorker.ready")
        offline_page.wait_for_function("navigator.serviceWorker.controller !== null")
        online.set_offline(True)
        offline_page.goto(chapter_url("a5-a7"))
        offline_page.locator(".reading-block").first.wait_for()
        assert offline_page.locator(".reader-article math").count() > 0
        offline_page.goto(chapter_url("02"))
        offline_page.locator(".reading-block").first.wait_for()
        offline_figure = offline_page.locator("#fig-12 img")
        offline_figure.scroll_into_view_if_needed()
        assert offline_figure.evaluate("async img => { await img.decode(); return img.naturalWidth > 0; }")
        assert not errors, errors
        print("Mobile, dark mode, navigation, progress, all images, and offline cache passed")
        browser.close()


if __name__ == "__main__":
    main()
