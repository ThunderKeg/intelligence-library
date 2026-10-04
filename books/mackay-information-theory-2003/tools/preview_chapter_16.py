"""Inspect the unpublished MacKay chapter 16 draft in the actual reader."""

import json
import hashlib
import sys
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
assert len(sys.argv) == 1 or sys.argv[1:] == ["--formal"], "usage: preview_chapter_16.py [--formal]"
FORMAL = sys.argv[1:] == ["--formal"]
draft_bytes = (BOOK / "chapter-16.draft.json").read_bytes()
formal_bytes = (BOOK / "chapter-16.json").read_bytes() if FORMAL else None
if FORMAL:
    assert formal_bytes == draft_bytes, "formal chapter JSON differs from reviewed draft"
DRAFT = json.loads((formal_bytes if FORMAL else draft_bytes).decode("utf-8"))
BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters16Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const oldChapter16 = chapters16Preview.findIndex(item => item.id === "16");
if (oldChapter16 >= 0) chapters16Preview.splice(oldChapter16, 1);
chapters16Preview.push({
  id: "16", number: "16", title: "消息传递",
  content: "books/mackay-information-theory-2003/chapter-16.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch16-formal-qa" if FORMAL else "mackay-ch16-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, False), (390, False), (390, True), (350, False), (350, True))
FIGURES = [block for block in DRAFT["blocks"] if block["kind"] == "figure"]
EXERCISES = [block for block in DRAFT["blocks"] if block["kind"] == "exercise"]
assert len(DRAFT["blocks"]) == 71 and DRAFT["sourcePdfPages"] == [253, 259]
assert len(DRAFT["toc"]) == 7 and len(FIGURES) == 12 and len(EXERCISES) == 4
assert [block["number"] for block in DRAFT["blocks"] if block["kind"] == "formula"] == ["(16.1)"]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p259-b003"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '16' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    restored = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '16' && saved.block === last &&
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
            if not FORMAL:
                context.route("**/books.js", lambda route: route.fulfill(
                    body=BOOK_SCRIPT, content_type="application/javascript"))
            page = context.new_page()
            errors, failed_resources = [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=" + (
                "15" if FORMAL else "16"))
            if FORMAL:
                page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=16']").click()
                assert "chapter=16" in page.url
            page.locator("#read-p259-b003").wait_for()

            actual_blocks = page.locator(".reading-block").evaluate_all(
                "items => items.map(item => [item.id, [...item.classList].find(name => name.startsWith('reading-') && name !== 'reading-block')])")
            assert actual_blocks == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                                     for block in DRAFT["blocks"]]
            assert page.locator(".reading-intro").count() == 1
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").count() == 6
            assert page.locator(".book-exercise-label").all_text_contents() == [
                block["label"] for block in EXERCISES]
            assert page.locator(".book-table").count() == 1
            assert page.locator(".book-figure img").count() == 12
            assert page.locator(".book-formula math").count() == 1
            assert page.locator(".formula-number").inner_text() == "(16.1)"
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator("#read-p259-b002").inner_text().startswith("习题 16.1 的解答")
            assert page.locator("#read-p259-b003").inner_text().startswith("习题 16.2 的解答")

            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 6
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")
            else:
                assert page.locator("#reader-toc .toc-chapter-link.chapter-current").is_visible()
            nav = page.locator("#chapter-navigation .chapter-navigation-link")
            assert nav.count() == 1 and "chapter=15" in nav.first.get_attribute("href")

            table = page.locator("#read-p254-b001")
            table.scroll_into_view_if_needed()
            rows = table.locator("tr").evaluate_all(
                "items => items.map(row => [...row.cells].map(cell => cell.textContent.trim()))")
            assert rows == [[cell["text"] for cell in row] for row in next(
                block for block in DRAFT["blocks"] if block["id"] == "p254-b001")["rows"]]
            table_metric = table.locator(".table-scroll").evaluate(
                "item => ({client: item.clientWidth, scroll: item.scrollWidth})")
            if table_metric["scroll"] > table_metric["client"] + 2:
                table.locator(".table-scroll").evaluate("item => item.scrollLeft = item.scrollWidth")
                assert table.locator(".table-scroll").evaluate("item => item.scrollLeft") > 0
                table.locator(".table-scroll").evaluate("item => item.scrollLeft = 0")
            table.screenshot(path=str(QA_DIR / f"table-{suffix}.png"))

            assert page.locator("#read-p253-b009 .book-list > li").count() == 3
            assert page.locator("#read-p255-b003 .book-list > li").count() == 4
            page.locator("#read-p253-b008").evaluate(
                "item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.screenshot(path=str(QA_DIR / f"algorithm-16-1-context-{suffix}.png"))
            algorithm = page.locator("#read-p255-b003")
            algorithm.scroll_into_view_if_needed()
            hierarchy = page.evaluate("""() => {
              const left = selector => Math.round(document.querySelector(selector).getBoundingClientRect().left);
              return {
                step4: left('#read-p255-b003 li:nth-child(4)'),
                a: left('#read-p255-b004 p'),
                b: left('#read-p255-b005 p'),
                parent: left('#read-p255-b003'),
                linebreaks: document.querySelector('#read-p255-b005').textContent.split(String.fromCharCode(10)).length - 1,
                whitespace: getComputedStyle(document.querySelector('#read-p255-b005 p')).whiteSpace,
                text: document.querySelector('#read-p255-b005').textContent
              };
            }""")
            assert hierarchy["linebreaks"] == 2 and "邻居" in hierarchy["text"], hierarchy
            assert hierarchy["a"] >= hierarchy["step4"] - 2, hierarchy
            assert hierarchy["b"] >= hierarchy["step4"] - 2, hierarchy
            page.locator("#read-p255-b002").evaluate(
                "item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.screenshot(path=str(QA_DIR / f"algorithm-16-5-context-{suffix}.png"))
            page.locator("#read-p255-b003").screenshot(path=str(QA_DIR / f"algorithm-16-5-list-{suffix}.png"))
            page.locator("#read-p255-b004").screenshot(path=str(QA_DIR / f"algorithm-16-5-a-{suffix}.png"))
            page.locator("#read-p255-b005").screenshot(path=str(QA_DIR / f"algorithm-16-5-b-{suffix}.png"))

            figure_metrics = {}
            for block in FIGURES:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                image = node.locator(".book-figure img")
                image.evaluate("item => item.decode()")
                assert image.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
                assert node.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
                media = node.locator(".figure-media")
                metric = media.evaluate("item => ({client: item.clientWidth, scroll: item.scrollWidth})")
                figure_metrics[block["src"].split("/")[-1]] = metric
                if block.get("wide") and width <= 390:
                    assert metric["scroll"] > metric["client"] + 2, (block["id"], metric)
                    assert node.locator(".figure-view-hint").is_visible()
                if metric["scroll"] > metric["client"] + 2:
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= metric["scroll"] - metric["client"] - 2
                    if block["id"] in ("p257-b003", "p258-b002") and width <= 390:
                        node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                if block["id"] in ("p257-b003", "p258-b002"):
                    node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))

            formula = page.locator("#read-p258-b014")
            formula.scroll_into_view_if_needed()
            formula_metric = formula.locator(".formula-scroll").evaluate(
                "item => ({client: item.clientWidth, scroll: item.scrollWidth, mathHeight: item.querySelector('math').getBoundingClientRect().height})")
            if formula_metric["scroll"] > formula_metric["client"] + 2:
                assert formula.locator(".formula-view-hint").count() == 1
                formula.locator(".formula-scroll").evaluate("item => item.scrollLeft = item.scrollWidth")
                assert formula.locator(".formula-scroll").evaluate("item => item.scrollLeft") > 0
            formula.locator("math").select_text()
            page.keyboard.press("Control+C")
            copied = page.evaluate("navigator.clipboard.readText()")
            assert len(copied.strip()) >= 5, copied
            page.evaluate("getSelection().removeAllRanges()")
            formula.screenshot(path=str(QA_DIR / f"formula-16-1-{suffix}.png"))

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            restored = inspect_progress(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.screenshot(path=str(QA_DIR / f"bottom-{suffix}.png"))
            assert not errors and not failed_resources, (errors, failed_resources)
            nav.click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=15" in page.url
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=16']").click()
            page.locator("#read-p259-b003").wait_for()
            assert "chapter=16" in page.url
            print(json.dumps({
                "viewport": suffix, "blocks": len(actual_blocks), "toc": len(DRAFT["toc"]),
                "table": table_metric, "algorithm16_5": hierarchy,
                "figures": figure_metrics, "formula": formula_metric,
                "formula_copied": copied, "bottom": restored,
                "errors": errors, "failed_resources": failed_resources,
            }, ensure_ascii=False))
            context.close()
        browser.close()
    digest = hashlib.sha256(formal_bytes if FORMAL else draft_bytes).hexdigest()
    print(f"PASS: chapter 16 {'formal route' if FORMAL else 'unpublished draft'}, "
          f"five viewports, sha256={digest}, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
