"""Check the unpublished chapter 10 draft in the real reader at desktop and mobile widths."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
draft = json.loads((BOOK / "chapter-10.draft.json").read_text(encoding="utf-8"))
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const previewBook = books.find(item => item.id === "mackay-information-theory-2003");
previewBook.chapters.push({
  id: "10", number: "10", title: "有噪信道编码定理",
  content: "books/mackay-information-theory-2003/chapter-10.json"
});
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
            context.route("**/books.js", lambda route: route.fulfill(
                body=book_script, content_type="application/javascript"))
            context.route("**/mackay-information-theory-2003/chapter-10.json",
                          lambda route: route.fulfill(
                              body=json.dumps(draft, ensure_ascii=False),
                              content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=10")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 216
            assert page.locator(".book-formula math").count() == 41
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 15
            assert page.locator(".book-exercise-icon").count() == 1
            assert page.locator(".book-exercise-label").count() == 12
            assert page.locator(".reading-code").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 10 章").count() == 1
            for image in page.locator(".book-figure img, .book-exercise-icon").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        browser.close()
    print("PASS: chapter 10 draft, 216 blocks, 41 display formulas, 15 figures, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
