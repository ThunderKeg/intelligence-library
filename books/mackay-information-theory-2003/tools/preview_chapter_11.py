"""Independently check the unpublished chapter 11 draft in the real reader."""

import json
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
DRAFT = json.loads((BOOK / "chapter-11.draft.json").read_text(encoding="utf-8"))
BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapter11Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
if (!chapter11Preview.some(item => item.id === "11")) chapter11Preview.push({
  id: "11", number: "11", title: "纠错码与实值信道",
  content: "books/mackay-information-theory-2003/chapter-11.json"
});
"""
FIGURE_IDS = [block["id"] for block in DRAFT["blocks"] if block["kind"] == "figure"]
FORMULA_SAMPLE_IDS = ("p191-b017", "p201-b006", "p202-b006", "p202-b009")
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"


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
        for width, dark in ((1440, False), (390, False), (390, True),
                            (350, False), (350, True)):
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme="dark" if dark else "light",
                service_workers="block",
            )
            context.route("**/books.js", lambda route: route.fulfill(
                body=BOOK_SCRIPT, content_type="application/javascript"))
            context.route("**/mackay-information-theory-2003/chapter-11.json",
                          lambda route: route.fulfill(
                              body=json.dumps(DRAFT, ensure_ascii=False),
                              content_type="application/json"))
            page = context.new_page()
            errors = []
            failed_resources = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=11")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 225
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".book-formula").count() == 44
            assert page.locator(".book-formula math").count() == 44
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".formula-number").all_text_contents() == [
                f"(11.{number})" for number in range(5, 48)]
            assert page.locator(".book-figure img").count() == 11
            assert page.locator(".book-figure figcaption").count() == 9
            assert page.locator(".figure-error").count() == 0
            assert page.locator(".book-exercise-label").count() == 10
            assert page.locator(".reading-code, .reading-table").count() == 0
            assert page.locator(".reading-quote .book-quote").count() == 5
            assert page.locator(".toc-chapter-link.chapter-current").count() == 2
            toc_targets = page.locator("#reader-toc .toc-section-link").evaluate_all(
                "links => links.map(link => link.hash.slice(1))")
            assert toc_targets == [f"read-{item['block']}" for item in DRAFT["toc"][1:]]
            assert all(page.locator(f"#{target}").count() == 1 for target in toc_targets)
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 11 章").count() == 1
            assert page.locator("#chapter-navigation .chapter-navigation-link").count() == 1
            toc_target = toc_targets[3]
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator(f"#reader-toc-mobile a[href='#{toc_target}']").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")
            else:
                page.locator(f"#reader-toc a[href='#{toc_target}']").click()
            assert page.evaluate("location.hash") == f"#{toc_target}"
            page.evaluate("history.replaceState(null, '', location.pathname + location.search)")

            formula_metrics = page.locator(".book-formula").evaluate_all("""items => items.map(item => {
              const scroller = item.querySelector('.formula-scroll');
              const number = item.querySelector('.formula-number');
              const hint = item.nextElementSibling;
              return {id: item.closest('.reading-block').id, number: number?.textContent || '',
                client: scroller.clientWidth, scroll: scroller.scrollWidth,
                hint: !!(hint?.classList.contains('formula-view-hint') && !hint.hidden &&
                  getComputedStyle(hint).display !== 'none'),
                separated: !number || number.getBoundingClientRect().left >=
                  scroller.getBoundingClientRect().right - 1};
            })""")
            assert all(item["separated"] for item in formula_metrics), formula_metrics
            assert all(item["scroll"] <= item["client"] + 2 or width > 800 or item["hint"]
                       for item in formula_metrics), formula_metrics
            for scroller in page.locator(".book-formula .formula-scroll").all():
                amount = scroller.evaluate("item => item.scrollWidth - item.clientWidth")
                if amount > 2:
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= amount - 2
                    scroller.evaluate("item => item.scrollLeft = 0")

            for formula_id in FORMULA_SAMPLE_IDS:
                block = page.locator(f"#read-{formula_id}")
                block.scroll_into_view_if_needed()
                screenshot = Path(tempfile.gettempdir()) / (
                    f"mackay-ch11-formula-{formula_id}-{width}-{int(dark)}.png")
                block.screenshot(path=str(screenshot))
            note = page.locator("#read-p202-b010")
            note.scroll_into_view_if_needed()
            note.screenshot(path=str(Path(tempfile.gettempdir()) /
                                     f"mackay-ch11-note-p202-b010-{width}-{int(dark)}.png"))

            figure_metrics = []
            for figure_id in FIGURE_IDS:
                block = page.locator(f"#read-{figure_id}")
                block.scroll_into_view_if_needed()
                image = block.locator(".book-figure img")
                image.evaluate("item => item.decode()")
                assert image.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
                metric = block.locator(".book-figure").evaluate("""figure => {
                  const media = figure.querySelector('.figure-media');
                  const image = figure.querySelector('img');
                  return {client: media.clientWidth, scroll: media.scrollWidth,
                    rendered: Math.round(image.getBoundingClientRect().width),
                    natural: image.naturalWidth, wide: figure.classList.contains('wide-figure'),
                    caption: !!figure.querySelector('figcaption'),
                    hint: !!figure.querySelector('.figure-view-hint')};
                }""")
                if metric["wide"]:
                    assert metric["hint"]
                    if metric["scroll"] > metric["client"] + 2:
                        media = block.locator(".figure-media")
                        media.evaluate("item => item.scrollLeft = item.scrollWidth")
                        assert media.evaluate("item => item.scrollLeft") >= (
                            metric["scroll"] - metric["client"] - 2)
                        if figure_id == "p199-b006" and width == 350:
                            page.wait_for_timeout(100)
                            page.screenshot(path=str(Path(tempfile.gettempdir()) /
                                                     f"mackay-ch11-{figure_id}-{width}-{int(dark)}-right-viewport.png"))
                        media.evaluate("item => item.scrollLeft = 0")
                else:
                    assert metric["scroll"] <= metric["client"] + 2, (figure_id, metric)
                figure_metrics.append((figure_id, metric))
                # Chromium may decode a lazy image before its pixels reach the next paint.
                page.wait_for_timeout(100)
                screenshot = Path(tempfile.gettempdir()) / (
                    f"mackay-ch11-{figure_id}-{width}-{int(dark)}.png")
                block.screenshot(path=str(screenshot))

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            target = page.locator("#read-p202-b011")
            target.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.wait_for_function("key => JSON.parse(localStorage.getItem(key) || '{}').block === 'read-p202-b011'", arg=PROGRESS_KEY)
            restored = []
            for _ in range(3):
                page.reload()
                page.wait_for_function("""() => { const element = document.querySelector('#read-p202-b011');
                  return element && Math.abs(element.getBoundingClientRect().top - 85) <= 2; }""")
                restored.append(page.evaluate("""key => ({
                  block: JSON.parse(localStorage.getItem(key)).block,
                  top: Math.round(document.querySelector('#read-p202-b011').getBoundingClientRect().top),
                  y: Math.round(scrollY)})""", PROGRESS_KEY))
            assert all(item["block"] == "read-p202-b011" and abs(item["top"] - 85) <= 2
                       for item in restored), restored
            assert len({item["y"] for item in restored}) == 1, restored
            assert not errors and not failed_resources, (errors, failed_resources)
            page.get_by_role("link", name="← 上一章 · 导页 关于第 11 章").click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=11-intro" in page.url
            assert page.locator(".reading-block").count() == 16
            print(f"{width} {'dark' if dark else 'light'}: "
                  f"formulas={len(formula_metrics)}, formula_overflow="
                  f"{sum(item['scroll'] > item['client'] + 2 for item in formula_metrics)}, "
                  f"figures={len(figure_metrics)}, wide_figures="
                  f"{sum(item[1]['wide'] for item in figure_metrics)}, "
                  f"progress={restored}, figure_metrics={figure_metrics}")
            context.close()
        browser.close()
    print("PASS: chapter 11 unpublished draft, five viewports, formulas/images/navigation/progress")
finally:
    server.shutdown()
    server.server_close()
