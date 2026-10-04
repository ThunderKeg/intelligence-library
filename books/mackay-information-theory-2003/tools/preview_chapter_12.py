"""Check the unpublished MacKay chapter 12 draft in the real reader."""

import json
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
DRAFT = json.loads((BOOK / "chapter-12.draft.json").read_text(encoding="utf-8"))
BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapter12Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
if (!chapter12Preview.some(item => item.id === "12")) chapter12Preview.push({
  id: "12", number: "12", title: "哈希码：用于高效信息检索的编码",
  content: "books/mackay-information-theory-2003/chapter-12.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
FIGURE_IDS = tuple(block["id"] for block in DRAFT["blocks"] if block["kind"] == "figure")
CODE_BLOCKS = {block["id"]: block["text"] for block in DRAFT["blocks"] if block["kind"] == "code"}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/"

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        for width, dark in ((1440, False), (390, False), (390, True),
                            (350, False), (350, True)):
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme="dark" if dark else "light",
                service_workers="block",
                permissions=["clipboard-read", "clipboard-write"],
            )
            context.route("**/books.js", lambda route: route.fulfill(
                body=BOOK_SCRIPT, content_type="application/javascript"))
            context.route("**/mackay-information-theory-2003/chapter-12.json",
                          lambda route: route.fulfill(
                              body=json.dumps(DRAFT, ensure_ascii=False),
                              content_type="application/json"))
            page = context.new_page()
            errors = []
            failed_resources = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=12")
            page.locator(".reading-block").first.wait_for()

            assert page.locator(".reading-block").count() == 136
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".book-formula math").count() == 11
            assert page.locator(".formula-number").all_text_contents() == [
                f"(12.{number})" for number in range(1, 12)]
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 3
            assert page.locator(".book-figure figcaption").count() == 3
            assert page.locator(".book-exercise-label").count() == 8
            assert page.locator(".book-exercise-icon").count() == 3
            assert page.locator(".book-code code").count() == 2
            assert page.locator(".reading-quote .book-quote").count() == 6
            assert page.locator(".reading-footnote").count() == 1
            assert page.locator(".toc-chapter-link.chapter-current").count() == 2
            toc_targets = page.locator("#reader-toc .toc-section-link").evaluate_all(
                "links => links.map(link => link.hash.slice(1))")
            assert toc_targets == [f"read-{item['block']}" for item in DRAFT["toc"][1:]]
            assert all(page.locator(f"#{target}").count() == 1 for target in toc_targets)
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 12 章").count() == 1
            assert page.locator("#chapter-navigation .chapter-navigation-link").count() == 1

            formula_metrics = page.locator(".book-formula").evaluate_all("""items => items.map(item => {
              const scroller = item.querySelector('.formula-scroll');
              const number = item.querySelector('.formula-number');
              const hint = item.nextElementSibling;
              return {number: number?.textContent, client: scroller.clientWidth,
                scroll: scroller.scrollWidth,
                hint: !!(hint?.classList.contains('formula-view-hint') && !hint.hidden &&
                  getComputedStyle(hint).display !== 'none'),
                separated: number.getBoundingClientRect().left >=
                  scroller.getBoundingClientRect().right - 1};
            })""")
            assert all(item["separated"] for item in formula_metrics), formula_metrics
            assert all(item["scroll"] <= item["client"] + 2 or width > 800 or item["hint"]
                       for item in formula_metrics), formula_metrics
            for scroller in page.locator(".book-formula .formula-scroll").all():
                amount = scroller.evaluate("item => item.scrollWidth - item.clientWidth")
                if amount > 2:
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= amount - 2
                    scroller.evaluate("item => item.scrollLeft = 0")
            underlines = page.locator("#read-p213-b012 math munder").evaluate_all("""items => items.map(item => {
              const base = item.querySelector(':scope > mrow');
              const original = item.querySelector(':scope > mo');
              return {text: base.textContent, width: base.getBoundingClientRect().width,
                line: getComputedStyle(base).borderBottomWidth,
                original: getComputedStyle(original).visibility};
            })""")
            assert len(underlines) == 2 and all(
                item["text"] == "GCCCCC" and item["width"] >= 55 and
                item["line"] == "1px" and item["original"] == "hidden"
                for item in underlines), underlines
            for formula_id in ("p210-b013", "p213-b012", "p216-b006"):
                block = page.locator(f"#read-{formula_id}")
                block.scroll_into_view_if_needed()
                block.screenshot(path=str(Path(tempfile.gettempdir()) /
                                          f"mackay-ch12-formula-{formula_id}-{width}-{int(dark)}.png"))

            figure_metrics = {}
            for figure_id in FIGURE_IDS:
                block = page.locator(f"#read-{figure_id}")
                block.scroll_into_view_if_needed()
                image = block.locator(".book-figure img")
                image.evaluate("item => item.decode()")
                assert image.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
                media = block.locator(".figure-media")
                metric = media.evaluate("item => ({client: item.clientWidth, scroll: item.scrollWidth})")
                figure_metrics[figure_id] = metric
                assert block.locator(".figure-view-hint").count() == 1
                if metric["scroll"] > metric["client"] + 2:
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= metric["scroll"] - metric["client"] - 2
                    if width <= 390:
                        page.wait_for_timeout(100)
                        page.screenshot(path=str(Path(tempfile.gettempdir()) /
                                                 f"mackay-ch12-{figure_id}-{width}-{int(dark)}-right.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                page.wait_for_timeout(100)
                if figure_id == "p208-b005":
                    image.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
                    page.screenshot(path=str(Path(tempfile.gettempdir()) /
                                             f"mackay-ch12-{figure_id}-{width}-{int(dark)}-left.png"))
                else:
                    block.screenshot(path=str(Path(tempfile.gettempdir()) /
                                              f"mackay-ch12-{figure_id}-{width}-{int(dark)}.png"))
            for icon in page.locator(".book-exercise-icon").all():
                icon.scroll_into_view_if_needed()
                icon.evaluate("item => item.decode()")

            code_metrics = {}
            for code_id, source_text in CODE_BLOCKS.items():
                block = page.locator(f"#read-{code_id}")
                code = block.locator(".book-code code")
                assert code.text_content() == source_text
                pre = block.locator(".book-code")
                metric = pre.evaluate("""item => ({client: item.clientWidth, scroll: item.scrollWidth,
                  whiteSpace: getComputedStyle(item.querySelector('code')).whiteSpace})""")
                assert metric["whiteSpace"] == "pre", metric
                if metric["scroll"] > metric["client"] + 2:
                    assert width > 800 or block.locator(".code-view-hint:visible").count() == 1
                    pre.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert pre.evaluate("item => item.scrollLeft") >= metric["scroll"] - metric["client"] - 2
                    if code_id == "p208-b002":
                        pre.screenshot(path=str(Path(tempfile.gettempdir()) /
                                                f"mackay-ch12-code-{width}-{int(dark)}-right.png"))
                    pre.evaluate("item => item.scrollLeft = 0")
                block.scroll_into_view_if_needed()
                block.screenshot(path=str(Path(tempfile.gettempdir()) /
                                          f"mackay-ch12-code-{code_id}-{width}-{int(dark)}.png"))
                code_metrics[code_id] = metric
            code = page.locator("#read-p208-b002 code")
            code.select_text()
            page.keyboard.press("Control+C")
            copied = page.evaluate("navigator.clipboard.readText()")
            assert copied.replace("\r\n", "\n").rstrip("\n") == CODE_BLOCKS["p208-b002"].rstrip("\n")

            note = page.locator("#read-p208-b003")
            assert "非原书正文" in note.inner_text()
            for note_id in ("p208-b003", "p216-b001", "p216-b002"):
                note = page.locator(f"#read-{note_id}")
                note.scroll_into_view_if_needed()
                note.screenshot(path=str(Path(tempfile.gettempdir()) /
                                         f"mackay-ch12-note-{note_id}-{width}-{int(dark)}.png"))
            reference = page.locator("#read-p212-b001 .book-footnote-ref a")
            assert reference.count() == 1
            assert reference.get_attribute("href") == "#read-fn-12-1"
            reference.click()
            assert page.evaluate("location.hash") == "#read-fn-12-1"
            assert page.locator("#read-fn-12-1").count() == 1
            page.wait_for_function("""() => { const top = document.querySelector('#read-fn-12-1').getBoundingClientRect().top;
              return Math.abs(top - 85) <= 2; }""")
            page.evaluate("history.replaceState(null, '', location.pathname + location.search)")

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            target = page.locator("#read-p213-b012")
            target.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.wait_for_function("key => JSON.parse(localStorage.getItem(key) || '{}').block === 'read-p213-b012'",
                                   arg=PROGRESS_KEY)
            restored = []
            for _ in range(3):
                page.reload()
                page.wait_for_function("""() => { const item = document.querySelector('#read-p213-b012');
                  return item && Math.abs(item.getBoundingClientRect().top - 85) <= 2; }""")
                restored.append(page.evaluate("""key => ({
                  block: JSON.parse(localStorage.getItem(key)).block,
                  top: Math.round(document.querySelector('#read-p213-b012').getBoundingClientRect().top),
                  y: Math.round(scrollY)})""", PROGRESS_KEY))
            assert all(item["block"] == "read-p213-b012" and item["top"] == 85
                       for item in restored) and len({item["y"] for item in restored}) == 1
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            page.get_by_role("link", name="← 上一章 · 导页 关于第 12 章").click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=12-intro" in page.url and page.locator(".reading-block").count() == 5
            print(f"{width} {'dark' if dark else 'light'}: blocks=136 formulas=11 "
                  f"formula_overflow={sum(item['scroll'] > item['client'] + 2 for item in formula_metrics)} "
                  f"figures={figure_metrics} code={code_metrics} copied={len(copied)} progress={restored}")
            context.close()
        browser.close()
    print("PASS: chapter 12 unpublished draft, five viewports, figures/code/formulas/footnote/navigation/progress")
finally:
    server.shutdown()
    server.server_close()
