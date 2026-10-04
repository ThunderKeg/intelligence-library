"""Preview chapter 9 source draft before registration."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
chapter = json.loads((BOOK / "chapter-09.draft.json").read_text(encoding="utf-8"))
next_page = json.loads((BOOK / "chapter-10-intro.draft.json").read_text(encoding="utf-8"))
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
            for name, payload in (("chapter-09.json", chapter), ("chapter-10-intro.json", next_page)):
                context.route(f"**/mackay-information-theory-2003/{name}",
                              lambda route, request, data=payload: route.fulfill(
                                  body=json.dumps(data, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=09")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 240
            assert page.locator(".book-formula math").count() == 63
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 22
            assert page.locator(".book-exercise-icon").count() == 12
            assert page.locator(".book-table").count() == 3
            assert page.locator(".book-exercise-label").count() == 15
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 9 章").count() == 1
            assert page.get_by_role("link", name="下一章 → · 导页 关于第 10 章").count() == 1
            for figure in page.locator(".book-figure img, .book-exercise-icon").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            assert page.locator("#read-p159-b003 .table-scroll tr").count() == 6
            assert page.locator("#read-p159-b006 .table-scroll tr").count() == 6
            assert page.locator("#read-p165-b004 .table-scroll tr").count() == 6
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        browser.close()
    print("PASS: chapter 9 preview, 240 blocks, 63 display formulas, 22 figures, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
