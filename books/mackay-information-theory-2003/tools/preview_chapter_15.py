"""Inspect the unpublished MacKay chapter 15 draft in the real reader."""

import json
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
DRAFT = json.loads((BOOK / "chapter-15.draft.json").read_text(encoding="utf-8"))
BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters15Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const oldChapter15 = chapters15Preview.findIndex(item => item.id === "15");
if (oldChapter15 >= 0) chapters15Preview.splice(oldChapter15, 1);
chapters15Preview.push({
  id: "15", number: "15", title: "信息论补充习题",
  content: "books/mackay-information-theory-2003/chapter-15.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / "mackay-ch15-draft-qa"
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, False), (390, False), (390, True), (350, False), (350, True))
FIGURES = [block for block in DRAFT["blocks"] if block["kind"] == "figure"]
FORMULAS = [block for block in DRAFT["blocks"] if block["kind"] == "formula"]
EXERCISES = [block for block in DRAFT["blocks"] if block["kind"] == "exercise"]
assert len(DRAFT["blocks"]) == 102 and DRAFT["sourcePdfPages"] == [245, 252]
assert len(DRAFT["toc"]) == 1 and len(EXERCISES) == 21
assert len(FIGURES) == 10 and len(FORMULAS) == 11
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(15.{number})" for number in range(1, 5)]
assert sum(not block["number"] for block in FORMULAS) == 7


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p252-b001"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '15' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    restored = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '15' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        restored.append(page.evaluate("""({key, last}) => ({
          block: JSON.parse(localStorage.getItem(key)).block,
          top: Math.round(document.querySelector('#' + last).getBoundingClientRect().top),
          y: Math.round(scrollY),
          width: document.querySelector('#reading-progress').style.width
        })""", {"key": PROGRESS_KEY, "last": last}))
    assert len({item["top"] for item in restored}) == 1, restored
    assert len({item["y"] for item in restored}) == 1, restored
    return restored


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/"

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        for width, dark in VIEWPORTS:
            mode = "dark" if dark else "light"
            suffix = f"{width}-{mode}"
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme=mode,
                service_workers="block",
                permissions=["clipboard-read", "clipboard-write"],
            )
            context.route("**/books.js", lambda route: route.fulfill(
                body=BOOK_SCRIPT, content_type="application/javascript"))
            page = context.new_page()
            errors, failed_resources = [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=15")
            page.locator("#read-p252-b001").wait_for()

            actual_blocks = page.locator(".reading-block").evaluate_all(
                "items => items.map(item => [item.id, [...item.classList].find(name => name.startsWith('reading-') && name !== 'reading-block')])")
            assert actual_blocks == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                                     for block in DRAFT["blocks"]]
            assert page.locator(".reading-intro").count() == 1
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").all_text_contents() == [
                "信源编码与有噪信道复习题", "信息论的更多故事", "解答"]
            assert page.locator("#read-p245-b004 h2 em").inner_text() == "信源编码与有噪信道复习题"
            assert page.locator("#read-p248-b014 h2 em").inner_text() == "信息论的更多故事"
            assert page.locator("#read-p245-b004 h2 em").evaluate(
                "item => getComputedStyle(item).fontStyle") == "italic"
            assert page.locator("#read-p248-b014 h2 em").evaluate(
                "item => getComputedStyle(item).fontStyle") == "italic"
            assert page.locator(".book-exercise-label").all_text_contents() == [
                block["label"] for block in EXERCISES]
            assert page.locator(".book-exercise-icon").count() == 4
            assert page.locator(".book-formula math").count() == 11
            assert page.locator(".formula-number").all_text_contents() == [
                f"(15.{number})" for number in range(1, 5)]
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 10
            assert page.locator(".book-table").count() == 1

            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 0
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")
            else:
                assert page.locator("#reader-toc .toc-chapter-link.chapter-current").is_visible()
            nav = page.locator("#chapter-navigation .chapter-navigation-link")
            assert nav.count() == 1 and "chapter=14" in nav.first.get_attribute("href")

            isbn = page.locator("#read-p247-b009")
            isbn.scroll_into_view_if_needed()
            isbn_rows = isbn.locator(".book-table tr").evaluate_all(
                "rows => rows.map(row => [...row.cells].map(cell => cell.textContent.trim()))")
            assert isbn_rows == [["0-521-64298-1"], ["1-010-00000-4"]]
            assert "表 15.1" in page.locator("#read-p247-b010").inner_text()
            isbn.screenshot(path=str(QA_DIR / f"isbn-{suffix}.png"))

            formula_metrics = []
            for block in FORMULAS:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                number = node.locator(".formula-number")
                assert number.inner_text() == block["number"] if block["number"] else number.count() == 0
                formula = node.locator(".book-formula")
                metric = formula.evaluate("""item => {
                  const scroll = item.querySelector('.formula-scroll');
                  const number = item.querySelector('.formula-number');
                  const hint = item.parentElement.querySelector('.formula-view-hint');
                  return {client: scroll.clientWidth, scroll: scroll.scrollWidth,
                    separated: !number || number.getBoundingClientRect().left >=
                      scroll.getBoundingClientRect().right - 1,
                    hint: !!hint && !hint.hidden && getComputedStyle(hint).display !== 'none',
                    height: item.getBoundingClientRect().height,
                    mathHeight: scroll.querySelector('math').getBoundingClientRect().height};
                }""")
                assert metric["separated"] and metric["height"] >= metric["mathHeight"] - 2, (
                    block["id"], metric)
                if metric["scroll"] > metric["client"] + 2:
                    assert width > 800 or metric["hint"], (block["id"], metric)
                    scroller = formula.locator(".formula-scroll")
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2)
                    if width <= 390:
                        node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                math = formula.locator("math")
                math.select_text()
                page.keyboard.press("Control+C")
                copied = page.evaluate("navigator.clipboard.readText()")
                assert len(copied.strip()) >= 2, (block["id"], copied)
                if block["id"] == "p248-b017":
                    assert copied.count("0.49") == 2 and copied.count("0.01") == 2, copied
                page.evaluate("getSelection().removeAllRanges()")
                metric.update({"id": block["id"], "number": block["number"], "copied": len(copied)})
                formula_metrics.append(metric)
                if width in (1440, 350):
                    node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

            matrix_153 = page.locator("#read-p248-b017 mtable")
            matrix_lines = matrix_153.evaluate("""item => ({
              firstColumn: [...item.querySelectorAll('mtr > mtd:first-child')].map(cell =>
                getComputedStyle(cell).borderRightWidth),
              header: [2, 3].map(column => getComputedStyle(
                item.querySelector(`mtr:nth-child(2) mtd:nth-child(${column})`)).borderTopWidth),
              noExtra: getComputedStyle(item.querySelector('mtr:nth-child(2) mtd:first-child')).borderTopWidth
            })""")
            assert matrix_lines == {"firstColumn": ["1px"] * 3,
                                    "header": ["1px", "1px"], "noExtra": "0px"}, matrix_lines

            figure_metrics = {}
            for block in FIGURES:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                picture = node.locator(".book-figure img")
                picture.evaluate("item => item.decode()")
                assert picture.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
                assert node.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
                media = node.locator(".figure-media")
                metric = media.evaluate("item => ({client: item.clientWidth, scroll: item.scrollWidth})")
                figure_metrics[block["src"].split("/")[-1]] = metric
                if block.get("wide") and width <= 390:
                    assert metric["scroll"] > metric["client"] + 2, (block["id"], metric)
                    assert node.locator(".figure-view-hint").count() == 1
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2)
                    if block["id"] in ("p250-b001", "p252-b001"):
                        node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                    if block["id"] == "p252-b001" and dark:
                        media.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
                        media.evaluate("item => item.scrollLeft = item.scrollWidth")
                        assert media.evaluate("item => item.scrollLeft") >= (
                            metric["scroll"] - metric["client"] - 2)
                        page.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right-viewport.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                if block["id"] in ("p249-b010", "p250-b001", "p252-b001"):
                    node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
            assert [block["src"].split("/")[-1] for block in FIGURES].index("figure-15-4.png") < [
                block["src"].split("/")[-1] for block in FIGURES].index("figure-15-3.png")
            figure159 = page.locator("#read-p252-b001")
            caption159 = figure159.locator(".figure-caption").inner_text()
            assert all(text in caption159 for text in ("图 15.9", "(a)", "(b)", "(c)", "Achievable")), caption159
            for icon in page.locator(".book-exercise-icon").all():
                icon.scroll_into_view_if_needed()
                icon.evaluate("item => item.decode()")
                assert icon.evaluate("item => item.naturalWidth > 0")

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            restored = inspect_progress(page)
            page.screenshot(path=str(QA_DIR / f"bottom-{suffix}.png"))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            nav = page.locator("#chapter-navigation .chapter-navigation-link")
            nav.click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=14" in page.url
            print(json.dumps({
                "viewport": suffix,
                "blocks": len(actual_blocks),
                "exercises": len(EXERCISES),
                "formulas": len(FORMULAS),
                "formula_overflow": [item["id"] for item in formula_metrics
                                     if item["scroll"] > item["client"] + 2],
                "all_formula_copied": all(item["copied"] >= 2 for item in formula_metrics),
                "matrix_15_3_lines": matrix_lines,
                "figures": figure_metrics,
                "bottom": restored,
                "errors": errors,
                "failed_resources": failed_resources,
            }, ensure_ascii=False))
            context.close()
        browser.close()
    print(f"PASS: chapter 15 unpublished draft, five viewports, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
