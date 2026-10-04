"""Preview the unpublished, independently source-reviewed About Chapter 11 page."""

import json
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
about = json.loads((BOOK / "chapter-11-intro.draft.json").read_text(encoding="utf-8"))
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const preview = {id:"11-intro",number:"导页",title:"关于第 11 章",content:"books/mackay-information-theory-2003/chapter-11-intro.json"};
if (!mackayPreviewChapters.some(existing => existing.id === preview.id)) mackayPreviewChapters.push(preview);
"""


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
        for width, dark in ((1440, False), (390, False), (390, True)):
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme="dark" if dark else "light",
                service_workers="block",
            )
            context.route("**/books.js", lambda route: route.fulfill(body=book_script, content_type="application/javascript"))
            context.route("**/mackay-information-theory-2003/chapter-11-intro.json",
                          lambda route: route.fulfill(body=json.dumps(about, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=11-intro")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 16
            assert page.locator(".book-formula").count() == 4
            assert page.locator(".book-formula math").count() == 4
            assert page.locator(".formula-number").all_text_contents() == [f"(11.{i})" for i in range(1, 5)]
            assert page.locator(".formula-fallback").count() == 0
            bold_symbols = page.locator("#read-p188-b011 math mi").all_text_contents()
            assert bold_symbols.count(chr(0x1D432)) >= 3  # bold y
            assert bold_symbols.count(chr(0x1D431)) >= 3  # bold x
            assert bold_symbols.count(chr(0x1D400)) >= 3  # bold A
            assert page.locator("#read-p188-b014 math mover").count() == 2
            assert page.locator("#read-p188-b014 math msub").count() >= 4
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 10 章").count() == 1
            assert page.locator("#chapter-navigation .chapter-navigation-link").count() == 1
            assert page.locator(".toc-chapter-link.chapter-current").count() == 2
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            formula_metrics = page.locator(".book-formula").evaluate_all("""items => items.map(item => {
              const s = item.querySelector('.formula-scroll');
              const hint = item.nextElementSibling;
              return {
                number: item.querySelector('.formula-number')?.textContent,
                client: s.clientWidth, scroll: s.scrollWidth,
                hint: !!(hint?.classList.contains('formula-view-hint') && !hint.hidden)
              };
            })""")
            assert all(m["scroll"] <= m["client"] + 2 or m["hint"] for m in formula_metrics)
            for scroller in page.locator(".book-formula .formula-scroll").all():
                overflow_amount = scroller.evaluate("item => item.scrollWidth - item.clientWidth")
                if overflow_amount > 2:
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= overflow_amount - 2
                    scroller.evaluate("item => item.scrollLeft = 0")
            assert not errors, errors
            mode = "dark" if dark else "light"
            screenshot = Path(tempfile.gettempdir()) / f"mackay-about-11-{width}-{mode}.png"
            page.screenshot(path=str(screenshot), full_page=True)
            print(f"{width} {mode}: blocks=16 formulas=4 scrollWidth={page.evaluate('document.documentElement.scrollWidth')} metrics={formula_metrics} screenshot={screenshot}")
            context.close()
        browser.close()
    print("PASS: About Chapter 11 draft preview, desktop and mobile light/dark")
finally:
    server.shutdown()
    server.server_close()
