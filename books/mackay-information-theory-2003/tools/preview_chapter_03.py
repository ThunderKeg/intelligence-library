"""Preview unpublished chapter 3 through the existing reader, without registration."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
draft = BOOK / "chapter-03.draft.json"
chapter = json.loads((draft if draft.is_file() else BOOK / "chapter-03.partial.json").read_text(encoding="utf-8"))
intro = json.loads((BOOK / "chapter-03-intro.draft.json").read_text(encoding="utf-8"))
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
if (!mackayPreviewChapters.some(chapter => chapter.id === "03-intro")) mackayPreviewChapters.push(
  {id:"03-intro",number:"导页",title:"关于第 3 章",content:"books/mackay-information-theory-2003/chapter-03-intro.json"});
if (!mackayPreviewChapters.some(chapter => chapter.id === "03")) mackayPreviewChapters.push(
  {id:"03",number:"3",title:"进一步讨论推断",content:"books/mackay-information-theory-2003/chapter-03.json"});
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
            for stem, payload in (("chapter-03-intro.json", intro), ("chapter-03.json", chapter)):
                context.route(f"**/mackay-information-theory-2003/{stem}",
                              lambda route, request, data=payload: route.fulfill(
                                  body=json.dumps(data, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=03")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == len(chapter["blocks"])
            assert page.locator(".book-formula math").count() == sum(
                block["kind"] == "formula" for block in chapter["blocks"])
            assert page.locator(".formula-fallback").count() == 0
            figures = [block for block in chapter["blocks"] if block["kind"] == "figure"]
            assert page.locator(".book-figure img").count() == len(figures)
            for image in page.locator(".book-figure img").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
                assert page.request.get(image.get_attribute("src")).ok
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-section-link").count() >= len(chapter["toc"])
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 3 章").count() == 1
            assert not errors, errors
            context.close()
        browser.close()
    print(f"PASS: chapter 3 preview through PDF {chapter['sourcePdfPages'][1]}, {len(chapter['blocks'])} blocks")
finally:
    server.shutdown()
    server.server_close()
