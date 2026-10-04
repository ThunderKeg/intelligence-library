"""Preview the standalone About Chapter 5 page before registration."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
payloads = {
    "chapter-I.json": "chapter-I.draft.json",
    "chapter-04-intro.json": "chapter-04-intro.draft.json",
    "chapter-04.json": "chapter-04.draft.json",
    "chapter-05-intro.json": "chapter-05-intro.draft.json",
}
chapters = {stem: json.loads((BOOK / source).read_text(encoding="utf-8")) for stem, source in payloads.items()}
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const chapter of [
  {id:"I",number:"第一部分",title:"数据压缩",content:"books/mackay-information-theory-2003/chapter-I.json"},
  {id:"04-intro",number:"导页",title:"关于第 4 章",content:"books/mackay-information-theory-2003/chapter-04-intro.json"},
  {id:"04",number:"4",title:"信源编码定理",content:"books/mackay-information-theory-2003/chapter-04.json"},
  {id:"05-intro",number:"导页",title:"关于第 5 章",content:"books/mackay-information-theory-2003/chapter-05-intro.json"}
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
            for stem, payload in chapters.items():
                context.route(f"**/mackay-information-theory-2003/{stem}",
                              lambda route, request, data=payload: route.fulfill(
                                  body=json.dumps(data, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=05-intro")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 7
            assert page.locator(".book-exercise-label").count() == 0
            table = page.locator(".book-table.notation-table")
            assert table.locator("tr").count() == 3
            assert all(row.locator("th,td").count() == 2 for row in table.locator("tr").all())
            assert page.locator("math").count() >= 10
            assert page.get_by_role("link", name="← 上一章 · 4 信源编码定理").count() == 1
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        browser.close()
    print("PASS: About Chapter 5, interval notation, source-coding summary, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
