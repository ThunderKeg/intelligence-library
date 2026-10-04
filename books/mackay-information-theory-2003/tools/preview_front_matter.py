"""Check the unpublished front matter in the existing reader at two sizes."""

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
front = json.loads((BOOK / "chapter-00.draft.json").read_text(encoding="utf-8"))
first = json.loads((BOOK / "chapter-01.draft.json").read_text(encoding="utf-8"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f"http://127.0.0.1:{server.server_port}/"

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        for name, width, height, dark in (("desktop", 1440, 900, False), ("mobile-dark", 390, 844, True)):
            context = browser.new_context(viewport={"width": width, "height": height},
                                          color_scheme="dark" if dark else "light",
                                          service_workers="block")
            context.route("**/mackay-information-theory-2003/chapter-00.json",
                          lambda route: route.fulfill(body=json.dumps(front, ensure_ascii=False), content_type="application/json"))
            context.route("**/mackay-information-theory-2003/chapter-01.json",
                          lambda route: route.fulfill(body=json.dumps(first, ensure_ascii=False), content_type="application/json"))
            page = context.new_page()
            page.goto(base + "?book=mackay-information-theory-2003&chapter=00")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == len(front["blocks"])
            assert page.locator(".book-formula math").count() == 17
            assert page.locator(".formula-fallback").count() == 0
            images = page.locator(".book-figure img")
            assert images.count() == 10
            broken = [src for src in images.evaluate_all("items => items.map(item => item.src)")
                      if not page.request.get(src).ok]
            assert not broken, broken
            size = page.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
            assert size["content"] <= size["viewport"], size
            roadmap = next(block for block in front["blocks"] if block["kind"] == "figure" and block["pdfPage"] == 7)
            roadmap_node = page.locator(f"#read-{roadmap['id']}")
            roadmap_node.scroll_into_view_if_needed()
            roadmap_node.locator("img").evaluate("image => image.decode()")
            roadmap_node.screenshot(path=str(OUT / f"{name}-roadmap-element.png"))
            assert roadmap_node.locator("a.figure-image-link").get_attribute("href").endswith("roadmap-07.png")
            if width < 800:
                media_width = roadmap_node.locator(".figure-media").evaluate(
                    "el => ({client: el.clientWidth, scroll: el.scrollWidth})")
                assert media_width["scroll"] > media_width["client"], media_width
            page.screenshot(path=str(OUT / f"{name}-roadmap.png"))
            assert page.locator("#chapter-navigation").get_by_role("link", name="下一章").count() == 1
            page.locator("#chapter-navigation").get_by_role("link", name="下一章").click()
            page.locator(".reading-heading h1").get_by_text("第 1 章 信息论导论").wait_for()
            context.close()
        browser.close()
    print(f"PASS: {len(front['blocks'])} front blocks, 17 formulas, 10 figures, chapter navigation")
finally:
    server.shutdown()
    server.server_close()
