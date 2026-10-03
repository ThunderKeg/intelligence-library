"""Preview built Sutton chapters without listing unreviewed chapters on the site."""

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
CHAPTERS = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
INDEX = (ROOT / "books.js").read_text(encoding="utf-8")
ANCHOR = f'      {{ id: "02", number: "2", title: "多臂赌博机", content: "books/{BOOK_ID}/chapter-02.json" }},'
assert INDEX.count(ANCHOR) == 1
ADDED = "\n".join(
    f'      {{ id: "{number:02d}", number: "{number}", title: "预览第 {number} 章", content: "books/{BOOK_ID}/chapter-{number:02d}.json" }},'
    for number in CHAPTERS
    if f'content: "books/{BOOK_ID}/chapter-{number:02d}.json"' not in INDEX
)
if f'content: "books/{BOOK_ID}/chapter-II.json"' not in INDEX:
    ADDED += f'\n      {{ id: "II", number: "第二部分", title: "近似求解方法", content: "books/{BOOK_ID}/chapter-II.json" }},'
PREVIEW_INDEX = INDEX.replace(ANCHOR, ANCHOR + ("\n" + ADDED if ADDED else ""), 1)


with sync_playwright() as playwright:
    installed = sorted((Path.home() / "AppData/Local/ms-playwright").glob("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
    browser = playwright.chromium.launch(headless=True, **({"executable_path": str(installed[-1])} if installed else {}))
    for number in CHAPTERS:
        chapter = json.loads((BOOK / f"chapter-{number:02d}.json").read_text(encoding="utf-8"))
        flat = [nested for block in chapter["blocks"] for nested in (block["blocks"] if block["kind"] == "box" else [block])]
        if number == 13:
            figure = next(block for block in flat if block["kind"] == "figure" and block["src"].endswith("fig-13-2.png"))
            assert "加入基线" in figure.get("caption", "")
            assert any(block["kind"] == "paragraph" and block["text"].startswith("图 13.2 对比") for block in flat)
        if number == 14:
            figures = {block["src"].rsplit("/", 1)[-1]: block for block in flat if block["kind"] == "figure"}
            assert "时间泛化" in figures["fig-14-1.png"].get("caption", "")
            assert "条件作用习得过程中" in figures["fig-14-4.png"].get("caption", "")
            assert figures["fig-14-5.png"].get("caption") and figures["fig-14-5.png"].get("annotations")
            assert any(block["kind"] == "paragraph" and block["text"].startswith("图 14.1 展示") for block in flat)
            assert any(block["kind"] == "paragraph" and block["text"].startswith("图 14.4 的 US 预测曲线") for block in flat)
        if number == 15:
            figures = {block["src"].rsplit("/", 1)[-1]: block for block in flat if block["kind"] == "figure"}
            assert len(figures) == 6
            assert all(figures[f"fig-15-{i}.png"].get("caption") and figures[f"fig-15-{i}.png"].get("annotations") for i in range(1, 6))
            assert sum(block["kind"] == "bibliographical-note" for block in flat) == 12
        if number == 16:
            figures = {block["src"].rsplit("/", 1)[-1]: block for block in flat if block["kind"] == "figure"}
            assert len(figures) == 12
            assert all(figure.get("caption") for figure in figures.values())
            assert all(figures[f"fig-16-{i}.png"].get("annotations") for i in (1, 2, 3, 4, 6, 7, 8, 9, 10))
            assert [block["number"] for block in flat if block["kind"] == "formula" and block.get("number")] == ["16.1", "16.2", "16.3", "16.4"]
        if number == 17:
            assert [block["number"] for block in flat if block["kind"] == "formula" and block.get("number")] == [f"17.{i}" for i in range(1, 12)]
            assert sum(block["kind"] == "bibliographical-note" for block in flat) == 5
            assert not any("$" in block.get("text", "") or "$" in block.get("caption", "") for block in flat)
        for label, width, height in (("desktop", 1440, 900), ("mobile-dark", 390, 844)):
            context = browser.new_context(viewport={"width": width, "height": height}, service_workers="block")
            context.route("**/books.js", lambda route: route.fulfill(body=PREVIEW_INDEX, content_type="application/javascript"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(BASE + f"?book={BOOK_ID}&chapter={number:02d}")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == len(flat), (number, "block count")
            assert page.locator(".book-formula math").count() == sum(block["kind"] == "formula" for block in flat), (number, "formula count")
            assert page.locator(".book-figure img").count() == sum(block["kind"] == "figure" for block in flat), (number, "figure count")
            assert page.locator(".book-exercise").count() == sum(block["kind"] == "exercise" for block in flat), (number, "exercise count")
            assert page.locator(".inline-math math").count() > 20, (number, "inline math")
            if number == 7:
                assert page.locator(".book-code").count() == 5, (number, "algorithm code")
                assert page.locator(".book-box").count() == 5, (number, "algorithm boxes")
                assert "```" not in page.locator("#reader-article").inner_text()
            if number == 9:
                assert page.locator(".toc-section-link math").count() >= 2, (number, "TOC MathML")
                assert page.locator(".book-box").count() == 9, (number, "source and algorithm boxes")
                lstd = page.locator("#read-p230-b01-box")
                assert lstd.locator(".reading-block").count() == 18
                assert lstd.locator("math").count() >= 15
                assert "$$" not in lstd.inner_text()
            if number == 10:
                assert page.locator(".book-box").count() == 5, (number, "source boxes")
                assert page.locator(".book-exercise").count() == 9, (number, "exercises")
                assert page.locator(".book-figure img").count() == 5, (number, "figures")
                assert page.locator(".book-footnote").count() == 2, (number, "footnotes")
                assert page.locator(".book-footnote").first.locator("code").all_inner_texts() == [
                    "iht=IHT(4096)",
                    "tiles(iht,8,[8*x/(0.5+1.2),8*xdot/(0.07+0.07)],[A])",
                ], (number, "tile coding source characters")
            if number == 11:
                assert page.locator(".book-box").count() == 4, (number, "source boxes")
                assert page.locator(".book-exercise").count() == 4, (number, "exercises")
                assert page.locator(".book-figure img").count() == 12, (number, "figures")
                assert page.locator(".book-footnote").count() == 4, (number, "footnotes")
            if number == 12:
                assert page.locator(".book-box").count() == 4, (number, "source boxes")
                assert page.locator(".algorithm-box").count() == 4, (number, "algorithm boxes")
                assert page.locator(".book-exercise").count() == 14, (number, "exercises")
                assert page.locator(".book-figure img").count() == 16, (number, "figures")
                assert page.locator(".reading-intro").count() == 1, (number, "chapter guide")
                assert page.locator(".reading-bibliographical-note-continuation").count() == 4, (number, "bibliographical continuations")
                assert page.locator("em math, strong math").count() >= 15, (number, "emphasized math")
                assert "\\(" not in page.locator("#reader-article").inner_text(), (number, "literal TeX delimiters")
            if number == 13:
                assert page.locator(".book-box").count() == 8, (number, "examples, proofs and algorithm boxes")
                assert page.locator(".algorithm-box").count() == 5, (number, "algorithm boxes")
                assert page.locator(".book-exercise").count() == 5, (number, "exercises")
                assert page.locator(".book-figure img").count() == 4, (number, "figures")
                assert page.locator(".book-footnote").count() == 1, (number, "footnote")
                assert page.locator(".reading-intro").count() == 1, (number, "chapter guide")
                assert page.locator(".reading-bibliographical-note-continuation").count() == 1, (number, "bibliographical continuation")
            if number == 14:
                assert page.locator(".book-figure img").count() == 9, (number, "figures and unnumbered illustrations")
                assert page.locator(".book-footnote").count() == 5, (number, "footnotes")
                assert page.locator(".book-quote").count() == 3, (number, "historical quotations")
                assert page.locator(".reading-intro").count() == 1, (number, "chapter guide")
            if number == 15:
                assert page.locator(".book-figure img").count() == 6, (number, "figures and unnumbered illustration")
                assert page.locator(".book-footnote").count() == 2, (number, "footnotes")
                assert page.locator(".book-quote").count() == 2, (number, "quotations")
                assert page.locator(".reading-intro").count() == 1, (number, "chapter guide")
            if number == 16:
                assert page.locator(".book-figure img").count() == 12, (number, "figures and unnumbered illustrations")
                assert page.locator(".book-footnote").count() == 4, (number, "footnotes")
                assert page.locator(".book-table").count() == 1, (number, "table")
                assert page.locator(".book-quote").count() == 1, (number, "quotation")
                assert page.locator(".reading-intro").count() == 1, (number, "chapter guide")
            if number == 17:
                assert page.locator(".book-formula math").count() == 13, (number, "display formulas")
                assert page.locator(".book-figure img").count() == 1, (number, "figure")
                assert page.locator(".book-exercise").count() == 1, (number, "exercise")
                assert page.locator(".book-footnote").count() == 1, (number, "footnote")
                assert page.locator(".reading-intro").count() == 1, (number, "chapter guide")
            for image in page.locator(".book-figure img").all():
                image.evaluate("img => { img.loading = 'eager'; return img.decode(); }")
                assert image.evaluate("img => img.naturalWidth > 0")
            if label == "mobile-dark":
                page.locator("#theme-toggle").click()
                assert page.locator("html").get_attribute("data-theme") == "dark"
                if number == 16:
                    table = page.locator("#read-p425-b03 .table-scroll")
                    sizing = table.evaluate("node => ({viewport: node.clientWidth, content: node.scrollWidth, headerHeight: node.querySelector('th').getBoundingClientRect().height})")
                    assert sizing["content"] > sizing["viewport"] + 100, (number, "table should scroll internally", sizing)
                    assert sizing["headerHeight"] < 70, (number, "table header should stay horizontal", sizing)
                    table.scroll_into_view_if_needed()
                    table.screenshot(path=str(OUTPUT / "sutton-ch16-table-mobile-dark.png"))
            dims = page.evaluate("({width:innerWidth, scroll:document.documentElement.scrollWidth})")
            assert dims["scroll"] <= dims["width"], (number, label, dims)
            if number == 8:
                boxes = page.locator(".algorithm-box")
                assert boxes.count() == 2, (number, "algorithm boxes")
                assert [box.locator(".reading-block").count() for box in boxes.all()] == [13, 17]
                assert all(box.locator(".inline-math math").count() >= 10 for box in boxes.all())
                for index, box in enumerate(boxes.all(), 1):
                    box.scroll_into_view_if_needed()
                    page.screenshot(path=str(OUTPUT / f"sutton-ch08-algorithm-{index}-{label}.png"))
                    box.screenshot(path=str(OUTPUT / f"sutton-ch08-algorithm-{index}-{label}-box.png"))
            if number == 9:
                lstd.scroll_into_view_if_needed()
                page.screenshot(path=str(OUTPUT / f"sutton-ch09-lstd-{label}.png"))
            page.locator(".book-formula").last.scroll_into_view_if_needed()
            page.screenshot(path=str(OUTPUT / f"sutton-ch{number:02d}-{label}.png"))
            assert not errors, (number, errors)
            context.close()
    for label, width, height in (("desktop", 1440, 900), ("mobile-dark", 390, 844)):
        context = browser.new_context(viewport={"width": width, "height": height}, service_workers="block")
        context.route("**/books.js", lambda route: route.fulfill(body=PREVIEW_INDEX, content_type="application/javascript"))
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(BASE + f"?book={BOOK_ID}&chapter=II")
        page.locator(".reading-block").first.wait_for()
        assert page.locator(".reading-block").count() == 5
        assert page.locator(".reading-heading h1").inner_text() == "第二部分 近似求解方法"
        assert "<!--" not in page.locator("#reader-article").inner_text()
        if label == "mobile-dark":
            page.locator("#theme-toggle").click()
            assert page.locator("html").get_attribute("data-theme") == "dark"
        dims = page.evaluate("({width:innerWidth, scroll:document.documentElement.scrollWidth})")
        assert dims["scroll"] <= dims["width"], ("II", label, dims)
        page.screenshot(path=str(OUTPUT / f"sutton-partII-{label}.png"))
        assert not errors, errors
        context.close()
    browser.close()

print("PASS: Sutton chapters 3–17 and Part II preview render, images, MathML, desktop and mobile dark")
