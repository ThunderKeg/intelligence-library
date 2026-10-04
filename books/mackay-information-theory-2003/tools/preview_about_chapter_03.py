"""Preview the independently sourced Chapter 3 introductory page."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
chapter = json.loads((BOOK / "chapter-03-intro.draft.json").read_text(encoding="utf-8"))
previous = json.loads((BOOK / "chapter-02.draft.json").read_text(encoding="utf-8"))
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
if (!mackayPreviewChapters.some(chapter => chapter.id === "02")) mackayPreviewChapters.push(
  {id:"02",number:"2",title:"概率、熵与推断",content:"books/mackay-information-theory-2003/chapter-02.json"});
if (!mackayPreviewChapters.some(chapter => chapter.id === "03-intro")) mackayPreviewChapters.push(
  {id:"03-intro",number:"导页",title:"关于第 3 章",content:"books/mackay-information-theory-2003/chapter-03-intro.json"});
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
            context.route("**/mackay-information-theory-2003/chapter-02.json", lambda route: route.fulfill(
                body=json.dumps(previous, ensure_ascii=False), content_type="application/json"))
            context.route("**/mackay-information-theory-2003/chapter-03-intro.json", lambda route: route.fulfill(
                body=json.dumps(chapter, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            page.goto(base + "?book=mackay-information-theory-2003&chapter=03-intro")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 10
            assert page.locator(".book-exercise-label").count() == 4
            assert page.locator(".book-figure img").count() == 1
            figure = page.locator(".book-figure img")
            figure.scroll_into_view_if_needed()
            figure.evaluate("image => image.decode()")
            assert page.request.get(figure.get_attribute("src")).ok
            table = page.locator(".book-table.notation-table")
            assert table.locator("tr").count() == 3
            assert all(row.locator("th,td").count() == 11 for row in table.locator("tr").all())
            if width < 800:
                widths = page.locator(".table-scroll").evaluate(
                    "el => ({client: el.clientWidth, scroll: el.scrollWidth})")
                assert widths["scroll"] > widths["client"], widths
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert page.locator("#chapter-navigation").get_by_role("link", name="上一章").count() == 1
            context.close()
        browser.close()
    print("PASS: About Chapter 3, four exercises, eleven-column table, decay image, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
