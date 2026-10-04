"""Preview the independently source-reviewed About Chapter 10 page."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
chapter9 = json.loads((BOOK / "chapter-09.draft.json").read_text(encoding="utf-8"))
about = json.loads((BOOK / "chapter-10-intro.draft.json").read_text(encoding="utf-8"))
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const chapter of [
  {id:"09",number:"9",title:"有噪信道上的通信",content:"books/mackay-information-theory-2003/chapter-09.json"},
  {id:"10-intro",number:"导页",title:"关于第 10 章",content:"books/mackay-information-theory-2003/chapter-10-intro.json"}
]) if (!mackayPreviewChapters.some(existing => existing.id === chapter.id)) mackayPreviewChapters.push(chapter);
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
            for name, payload in (("chapter-09.json", chapter9), ("chapter-10-intro.json", about)):
                context.route(f"**/mackay-information-theory-2003/{name}",
                              lambda route, request, data=payload: route.fulfill(
                                  body=json.dumps(data, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=10-intro")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 5
            assert page.locator(".reading-quote").filter(has_text="技术译注（非原书正文）").count() == 1
            table = page.locator("#read-p173-b005 .table-scroll")
            assert table.locator("tr").count() == 13
            assert all(row.locator("th,td").count() == 2 for row in table.locator("tr").all())
            assert table.locator("math").count() == 18
            assert table.locator("tr").nth(2).locator("math mi").first.text_content() == "C"
            assert table.locator("tr").nth(4).locator("math mi").first.text_content() == "𝒞"
            assert table.locator("tr").nth(7).locator("math mi").first.text_content() == "s"
            assert table.locator("tr").nth(10).locator("math mi").first.text_content() == "𝐬"
            assert page.get_by_role("link", name="← 上一章 · 9 有噪信道上的通信").count() == 1
            assert page.locator(".formula-fallback").count() == 0
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        browser.close()
    print("PASS: About chapter 10 preview, 12 symbol rows, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
