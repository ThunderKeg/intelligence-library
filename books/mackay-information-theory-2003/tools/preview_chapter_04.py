"""Preview unpublished chapter 4 with the reviewed part and About page."""

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
}
chapters = {stem: json.loads((BOOK / source).read_text(encoding="utf-8")) for stem, source in payloads.items()}
chapter = chapters["chapter-04.json"]
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const chapter of [
  {id:"I",number:"第一部分",title:"数据压缩",content:"books/mackay-information-theory-2003/chapter-I.json"},
  {id:"04-intro",number:"导页",title:"关于第 4 章",content:"books/mackay-information-theory-2003/chapter-04-intro.json"},
  {id:"04",number:"4",title:"信源编码定理",content:"books/mackay-information-theory-2003/chapter-04.json"}
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
            page.goto(base + "?book=mackay-information-theory-2003&chapter=04")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == len(chapter["blocks"])
            assert page.locator(".book-formula math").count() == sum(
                block["kind"] == "formula" for block in chapter["blocks"])
            assert page.locator(".formula-fallback").count() == 0
            figures = [block for block in chapter["blocks"] if block["kind"] == "figure"]
            assert page.locator(".book-figure img").count() == len(figures)
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
                assert page.request.get(figure.get_attribute("src")).ok
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".book-inline-code").count() >= 10
            assert page.locator(".reading-block em").count() >= 5
            assert page.locator(".reading-block strong").count() >= 20
            assert page.locator(".reading-reference[href^='http']").count() >= 1
            assert page.locator(".book-footnote-ref a[href='#read-fn-4-1']").count() == 1
            assert page.locator("#read-fn-4-1.reading-footnote").count() == 1
            assert page.locator(".toc-section-link").count() >= len(chapter["toc"])
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 4 章").count() == 1
            assert not errors, errors
            context.close()
        browser.close()
    print(f"PASS: chapter 4 preview, {len(chapter['blocks'])} blocks, {len(figures)} figures, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
