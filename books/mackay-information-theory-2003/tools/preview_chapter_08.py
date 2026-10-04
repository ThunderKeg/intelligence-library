"""Preview the second-part title, chapter 8, and the next About page."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
sources = {
    "chapter-07.json": "chapter-07.draft.json",
    "chapter-II.json": "chapter-II.draft.json",
    "chapter-08.json": "chapter-08.draft.json",
    "chapter-09-intro.json": "chapter-09-intro.draft.json",
}
chapters = {target: json.loads((BOOK / source).read_text(encoding="utf-8")) for target, source in sources.items()}
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const chapter of [
  {id:"07",number:"7",title:"整数编码",content:"books/mackay-information-theory-2003/chapter-07.json"},
  {id:"II",number:"第二部分",title:"有噪信道编码",content:"books/mackay-information-theory-2003/chapter-II.json"},
  {id:"08",number:"8",title:"相依随机变量",content:"books/mackay-information-theory-2003/chapter-08.json"},
  {id:"09-intro",number:"导页",title:"关于第 9 章",content:"books/mackay-information-theory-2003/chapter-09-intro.json"}
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
            page.goto(base + "?book=mackay-information-theory-2003&chapter=II")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 2
            part_title = page.locator("#read-p149-b001 h1")
            assert part_title.inner_text() == "第二部分\n有噪信道编码"
            assert part_title.evaluate("node => getComputedStyle(node).whiteSpace") == "pre-line"
            emblem = page.locator(".book-figure img")
            assert emblem.count() == 1
            emblem.evaluate("image => image.decode()")
            assert page.get_by_role("link", name="← 上一章 · 7 整数编码").count() == 1
            assert page.get_by_role("link", name="下一章 → · 8 相依随机变量").count() == 1
            page.goto(base + "?book=mackay-information-theory-2003&chapter=08")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 120
            assert page.locator(".book-formula math").count() == 35
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".book-figure img").count() == 4
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            assert page.locator(".book-exercise-icon").count() == 5
            for icon in page.locator(".book-exercise-icon").all():
                icon.evaluate("image => image.decode()")
            table = page.locator("#read-p152-b014 .table-scroll")
            assert table.locator("tr").count() == 5
            assert all(row.locator("th,td").count() == 5 for row in table.locator("tr").all())
            assert page.locator(".reading-quote").filter(has_text="技术译注（非原书正文）").count() == 2
            assert page.get_by_role("link", name="← 上一章 · 第二部分 有噪信道编码").count() == 1
            assert page.get_by_role("link", name="下一章 → · 导页 关于第 9 章").count() == 1
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.goto(base + "?book=mackay-information-theory-2003&chapter=09-intro")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 2
            assert page.get_by_role("link", name="← 上一章 · 8 相依随机变量").count() == 1
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        browser.close()
    print("PASS: Part II, chapter 8, About 9 preview, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
