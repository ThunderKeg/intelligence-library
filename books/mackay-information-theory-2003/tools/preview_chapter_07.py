"""Preview the independently source-reviewed seventh chapter before registration."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
chapter = json.loads((BOOK / "chapter-07.draft.json").read_text(encoding="utf-8"))
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
if (!mackayPreviewChapters.some(existing => existing.id === "07"))
  mackayPreviewChapters.push({id:"07",number:"7",title:"整数编码",content:"books/mackay-information-theory-2003/chapter-07.json"});
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
        for width, dark in ((1440, False), (390, True)):
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme="dark" if dark else "light",
                service_workers="block",
            )
            context.route("**/books.js", lambda route: route.fulfill(body=book_script, content_type="application/javascript"))
            context.route("**/mackay-information-theory-2003/chapter-07.json",
                          lambda route: route.fulfill(
                              body=json.dumps(chapter, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=07")
            page.locator(".reading-block").first.wait_for()
            rendered = sum(len(block["blocks"]) if block["kind"] == "box" else 1 for block in chapter["blocks"])
            assert rendered == 74
            assert page.locator(".reading-block").count() == rendered
            assert page.locator(".book-formula math").count() == 7
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-table.code-table").count() == 5
            assert page.locator("#read-box-7-4.book-box.outlined-box .reading-code").count() == 1
            assert page.locator("#read-box-7-4.book-box.outlined-box .reading-paragraph").count() == 1
            binary = page.locator("#read-p146-b016.reading-code")
            assert binary.count() == 1
            assert binary.inner_text().count("\n") >= 1
            assert "text" not in binary.inner_text()
            assert page.locator(".reading-quote").filter(has_text="译注（非原书正文）").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".book-figure img").count() == 0
            assert page.get_by_role("link", name="← 上一章 · 6 流编码").count() == 1
            code_table = page.locator("#read-p148-b002 .table-scroll")
            assert code_table.locator("tr").count() == 9
            assert all(row.locator("th,td").count() == 8 for row in code_table.locator("tr").all())
            if width == 390:
                assert code_table.evaluate("node => node.scrollWidth > node.clientWidth")
                assert code_table.locator(".book-inline-code").first.evaluate(
                    "node => getComputedStyle(node).whiteSpace === 'nowrap'")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        browser.close()
    print(f"PASS: chapter 7 preview, {len(chapter['blocks'])} top-level blocks, {rendered} rendered, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
