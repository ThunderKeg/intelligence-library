"""Preview the unpublished chapter 2 draft in the existing reader."""

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
OUT = ROOT / "tmp" / "mackay-qa"
OUT.mkdir(parents=True, exist_ok=True)
draft = BOOK / "chapter-02.draft.json"
chapter = json.loads((draft if draft.is_file() else BOOK / "chapter-02.partial.json").read_text(encoding="utf-8"))


def leaf_blocks(blocks):
    for block in blocks:
        if block["kind"] == "box":
            yield from leaf_blocks(block["blocks"])
        else:
            yield block


leaves = list(leaf_blocks(chapter["blocks"]))
book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const mackayPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
if (!mackayPreviewChapters.some(chapter => chapter.id === "02")) mackayPreviewChapters.push({
  id:"02",number:"2",title:"概率、熵与推断",
  content:"books/mackay-information-theory-2003/chapter-02.json"});
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
        for label, width, dark in (("desktop", 1440, False), ("mobile-dark", 390, True)):
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme="dark" if dark else "light",
                service_workers="block",
            )
            context.route("**/books.js", lambda route: route.fulfill(body=book_script, content_type="application/javascript"))
            context.route("**/mackay-information-theory-2003/chapter-02.json", lambda route: route.fulfill(
                body=json.dumps(chapter, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=02")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == len(leaves)
            assert page.locator(".book-formula math").count() == sum(
                block["kind"] == "formula" for block in leaves)
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == sum(
                block["kind"] == "figure" for block in leaves)
            for image in page.locator(".book-figure img").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            for source in page.locator(".book-figure img").evaluate_all("images => images.map(image => image.src)"):
                assert page.request.get(source).ok, source
            assert page.locator(".book-code code").count() == 1
            assert page.locator(".book-code code").inner_text().count("1") == 29
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            assert page.locator("#read-box-2-4.outlined-box .reading-block").count() == 7
            box = page.locator("#read-box-2-4.outlined-box")
            assert box.evaluate("el => getComputedStyle(el).borderTopWidth") != "0px"
            assert box.locator("p strong").count() == 4
            box.screenshot(path=str(OUT / f"ch2-{label}-box-2-4.png"))
            assert page.locator(".book-exercise-label").filter(has_text="习题 2.28").count() == 1
            assert page.locator("#read-p050-b002 .figure-caption math").count() == 8
            figure = next(block for block in leaves if block["kind"] == "figure" and block["pdfPage"] == 47)
            page.locator(f"#read-{figure['id']}").scroll_into_view_if_needed()
            page.locator(f"#read-{figure['id']}").screenshot(path=str(OUT / f"ch2-{label}-figure-2-10.png"))
            context.close()
        browser.close()
    print(f"PASS: chapter 2 preview through PDF {chapter['sourcePdfPages'][1]}, {len(chapter['blocks'])} blocks")
finally:
    server.shutdown()
    server.server_close()
