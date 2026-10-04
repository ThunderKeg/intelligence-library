"""Smoke check the unpublished MacKay chapter in the existing site reader."""

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
chapter = json.loads((BOOK / "chapter-01.draft.json").read_text(encoding="utf-8"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f"http://127.0.0.1:{server.server_port}/"

try:
    with sync_playwright() as playwright:
        edge = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
        browser = playwright.chromium.launch(headless=True, executable_path=str(edge))
        for name, width, height, dark in (("desktop", 1440, 900, False), ("mobile-dark", 390, 844, True)):
            context = browser.new_context(viewport={"width": width, "height": height},
                                          color_scheme="dark" if dark else "light",
                                          service_workers="block")
            context.route("**/mackay-information-theory-2003/chapter-01.json",
                          lambda route: route.fulfill(body=json.dumps(chapter, ensure_ascii=False),
                                                      content_type="application/json"))
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + "?book=mackay-information-theory-2003&chapter=01")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == len(chapter["blocks"])
            assert page.locator(".reading-intro").count() == 1
            assert page.locator("#read-p015-b003 .book-quote").count() == 1
            assert page.locator(".book-formula math").count() == 43
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 16
            assert page.locator(".book-exercise-icon").count() > 0
            for caption_id in ("p018-b002", "p021-b006", "p023-b003"):
                caption = page.locator(f"#read-{caption_id}.reading-caption")
                assert caption.count() == 1
                assert caption.locator("math").count() > 0
                assert "$" not in caption.inner_text()
                if width < 800:
                    bounds = caption.evaluate("el => ({client: el.clientWidth, scroll: el.scrollWidth})")
                    assert bounds["scroll"] <= bounds["client"], (caption_id, bounds)
            algorithm = page.locator("#read-p023-b002 .book-table")
            assert algorithm.get_attribute("class").find("notation-table") >= 0
            if width < 800:
                first_cell = algorithm.locator("tr").first.locator("th,td").first
                assert first_cell.evaluate("el => getComputedStyle(el).whiteSpace") == "nowrap"
                table_width = page.locator("#read-p023-b002 .table-scroll").evaluate(
                    "el => ({client: el.clientWidth, scroll: el.scrollWidth})")
                assert table_width["scroll"] > table_width["client"], table_width
            sources = page.locator(".book-figure img").evaluate_all("images => images.map(image => image.src)")
            broken = [source for source in sources if not page.request.get(source).ok]
            assert not broken, broken
            assert not errors, errors
            size = page.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
            assert size["content"] <= size["viewport"], size
            page.screenshot(path=str(OUT / f"{name}-top.png"))
            figure = next(block for block in chapter["blocks"] if block["kind"] == "figure" and block["pdfPage"] == 26)
            figure_node = page.locator(f"#read-{figure['id']}")
            figure_node.scroll_into_view_if_needed()
            figure_node.locator("img").evaluate("image => image.decode()")
            assert figure_node.locator("a.figure-image-link").get_attribute("href").endswith("figure-1-18.png")
            if width < 800:
                media_width = figure_node.locator(".figure-media").evaluate(
                    "el => ({client: el.clientWidth, scroll: el.scrollWidth})")
                assert media_width["scroll"] > media_width["client"], media_width
            page.screenshot(path=str(OUT / f"{name}-plot.png"))
            figure_node.screenshot(path=str(OUT / f"{name}-plot-element.png"))
            formula = next(block for block in chapter["blocks"] if block["kind"] == "formula" and block.get("number") == "(1.35)")
            page.locator(f"#read-{formula['id']}").scroll_into_view_if_needed()
            page.screenshot(path=str(OUT / f"{name}-formula.png"))
            formula_width = page.locator(f"#read-{formula['id']} .formula-scroll").evaluate(
                "el => ({client: el.clientWidth, scroll: el.scrollWidth})"
            )
            assert formula_width["scroll"] >= formula_width["client"]
            if width < 800:
                assert formula_width["scroll"] > formula_width["client"], formula_width
                scroll_end = page.locator(f"#read-{formula['id']} .formula-scroll").evaluate(
                    "el => { el.scrollLeft = el.scrollWidth; return el.scrollLeft; }")
                assert scroll_end > 0
            context.close()
        browser.close()
    print(f"PASS: {len(chapter['blocks'])} blocks, 43 formulas, 16 figures, desktop/mobile; screenshots {OUT}")
finally:
    server.shutdown()
    server.server_close()
