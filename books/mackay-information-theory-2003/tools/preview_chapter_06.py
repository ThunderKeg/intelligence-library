"""Preview the unpublished sixth chapter and its preceding pages."""

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
    "chapter-05.json": "chapter-05.draft.json",
    "chapter-06-intro.json": "chapter-06-intro.draft.json",
    "chapter-06.json": "chapter-06.draft.json",
}
chapters = {stem: json.loads((BOOK / source).read_text(encoding="utf-8")) for stem, source in payloads.items()}
chapter = chapters["chapter-06.json"]
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const chapter of [
  {id:"I",number:"第一部分",title:"数据压缩",content:"books/mackay-information-theory-2003/chapter-I.json"},
  {id:"04-intro",number:"导页",title:"关于第 4 章",content:"books/mackay-information-theory-2003/chapter-04-intro.json"},
  {id:"04",number:"4",title:"信源编码定理",content:"books/mackay-information-theory-2003/chapter-04.json"},
  {id:"05-intro",number:"导页",title:"关于第 5 章",content:"books/mackay-information-theory-2003/chapter-05-intro.json"},
  {id:"05",number:"5",title:"符号编码",content:"books/mackay-information-theory-2003/chapter-05.json"},
  {id:"06-intro",number:"导页",title:"关于第 6 章",content:"books/mackay-information-theory-2003/chapter-06-intro.json"},
  {id:"06",number:"6",title:"流编码",content:"books/mackay-information-theory-2003/chapter-06.json"}
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
            page.goto(base + "?book=mackay-information-theory-2003&chapter=06")
            page.locator(".reading-block").first.wait_for()
            rendered_blocks = sum(len(block["blocks"]) if block["kind"] == "box" else 1
                                  for block in chapter["blocks"])
            assert page.locator(".reading-block").count() == rendered_blocks
            assert page.locator(".book-formula math").count() == sum(
                block["kind"] == "formula" for block in chapter["blocks"])
            assert page.locator(".formula-fallback").count() == 0
            figures = [block for block in chapter["blocks"] if block["kind"] == "figure"]
            assert page.locator(".book-figure img").count() == len(figures)
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
                assert page.request.get(figure.get_attribute("src")).ok
            assert page.locator(".book-exercise-icon").count() == 8
            for icon in page.locator(".book-exercise-icon").all():
                icon.evaluate("image => image.decode()")
            algorithm = page.locator("#read-box-6-3.book-box.outlined-box")
            assert algorithm.count() == 1
            assert algorithm.locator(".reading-paragraph").count() == 1
            assert algorithm.locator(".reading-code").count() == 1
            assert page.locator(".book-table.code-table").count() == 4
            assert page.locator(".book-footnote-ref a").count() == 5
            assert page.locator(".reading-footnote").count() == 5
            assert page.locator(".book-footnote-ref a").first.get_attribute("href") == "#read-fn-6-1"
            assert page.locator("#read-fn-6-1").count() == 1
            code_table = page.locator("#read-p131-b006 .table-scroll")
            assert code_table.locator("tr").count() == 4
            assert all(row.locator("th,td").count() == 9 for row in code_table.locator("tr").all())
            if width == 390:
                assert code_table.evaluate("node => node.scrollWidth > node.clientWidth")
                assert code_table.locator(".book-inline-code").first.evaluate(
                    "node => getComputedStyle(node).whiteSpace === 'nowrap'")
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-section-link").count() >= len(chapter["toc"])
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 6 章").count() == 1
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        browser.close()
    print(f"PASS: chapter 6 preview, {len(chapter['blocks'])} blocks, {len(figures)} figures, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
