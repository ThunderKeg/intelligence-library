"""Inspect MacKay chapter 19 in the reader, optionally on the registered path."""

from argparse import ArgumentParser
import hashlib
import json
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
parser = ArgumentParser()
parser.add_argument("--formal", action="store_true",
                    help="inspect the registered chapter-19.json without intercepting books.js")
FORMAL = parser.parse_args().formal
DRAFT_BYTES = (BOOK / "chapter-19.draft.json").read_bytes()
FORMAL_BYTES = (BOOK / "chapter-19.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal chapter differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
DRAFT = json.loads(CHAPTER_BYTES.decode("utf-8"))


def reading_blocks(items):
    for item in items:
        if item["kind"] == "box":
            yield from reading_blocks(item["blocks"])
        else:
            yield item


BLOCKS = list(reading_blocks(DRAFT["blocks"]))
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
assert DRAFT["sourcePdfPages"] == [281, 292]
assert (len(DRAFT["blocks"]), len(BLOCKS), len(DRAFT["toc"]), len(FORMULAS),
        len(FIGURES), len(EXERCISES)) == (118, 131, 8, 27, 4, 6)
assert [(block["id"], len(block["blocks"])) for block in DRAFT["blocks"]
        if block["kind"] == "box"] == [("box-19-2", 14)]
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(19.{number})" for number in range(1, 22)]
assert sum(not block["number"] for block in FORMULAS) == 6
BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters19Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const oldChapter19 = chapters19Preview.findIndex(item => item.id === "19");
if (oldChapter19 >= 0) chapters19Preview.splice(oldChapter19, 1);
chapters19Preview.push({
  id: "19", number: "19", title: "为什么有性生殖？信息获取与进化",
  content: "books/mackay-information-theory-2003/chapter-19.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch19-formal-qa" if FORMAL else "mackay-ch19-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (390, "light"), (390, "dark"), (350, "light"), (350, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p292-b009"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '19' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '19' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last))
    assert len({item["top"] for item in positions}) == 1, positions
    assert len({item["y"] for item in positions}) == 1, positions
    return positions


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/"

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        for width, mode in VIEWPORTS:
            suffix = f"{width}-{mode}"
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme=mode,
                service_workers="block",
                permissions=["clipboard-read", "clipboard-write"],
            )
            if not FORMAL:
                context.route("**/books.js", lambda route: route.fulfill(
                    body=BOOK_SCRIPT, content_type="application/javascript"))
            page = context.new_page()
            errors, failed_resources, requested_urls = [], [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("request", lambda request: requested_urls.append(request.url))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=19")
            page.locator("#read-p292-b009").wait_for()
            if FORMAL:
                assert any(url.endswith("/books.js") for url in requested_urls)
                assert any(url.endswith(
                    "/books/mackay-information-theory-2003/chapter-19.json")
                    for url in requested_urls)

            actual = page.locator(".reading-block").evaluate_all("""items => items.map(
              item => [item.id, [...item.classList].find(name =>
                name.startsWith('reading-') && name !== 'reading-block')])""")
            assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                              for block in BLOCKS]
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").count() == 7
            assert page.locator(".reading-heading h3").count() == 6
            assert page.locator(".reading-heading h3 em").count() == 5
            assert page.locator(".book-exercise-label").all_text_contents() == [
                block["label"] for block in EXERCISES]
            assert page.locator("#read-p292-b008").inner_text().startswith("习题 19.1 的解答")
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator(".book-formula math").count() == 27
            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 7
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")
            else:
                assert page.locator("#reader-toc .toc-chapter-link.chapter-current").is_visible()
            previous = page.locator(
                "#chapter-navigation .chapter-navigation-link[href*='chapter=18']")
            assert previous.count() == 1

            # Box 19.2 occupies the whole original PDF page 286. Record actual grouping and outline.
            box = page.evaluate("""() => {
              const first = document.querySelector('#read-p286-b001');
              const last = document.querySelector('#read-p286-b014');
              const parent = first.parentElement;
              return {
                firstParent: parent.id || parent.className,
                lastParent: last.parentElement.id || last.parentElement.className,
                outlinedBoxCount: document.querySelectorAll('#reader-article .outlined-box').length,
                boxBorderLeft: getComputedStyle(parent).borderLeftWidth,
                boxBorderTop: getComputedStyle(parent).borderTopWidth,
                boxBackground: getComputedStyle(parent).backgroundColor
              };
            }""")
            assert box["firstParent"] == "read-box-19-2" and box["lastParent"] == "read-box-19-2", box
            assert box["outlinedBoxCount"] == 1
            assert box["boxBorderLeft"] != "0px" and box["boxBorderTop"] != "0px", box
            page.locator("#read-p286-b001").evaluate(
                "item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.screenshot(path=str(QA_DIR / f"box-19-2-top-{suffix}.png"))
            page.locator("#read-p286-b012").evaluate(
                "item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.screenshot(path=str(QA_DIR / f"box-19-2-bottom-{suffix}.png"))

            formula_overflow = []
            copied = 0
            for block in FORMULAS:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                assert node.locator(".book-formula math").count() == 1, block["id"]
                expected_number = [block["number"]] if block["number"] else []
                assert node.locator(".formula-number").all_text_contents() == expected_number
                formula = node.locator(".book-formula")
                metric = formula.evaluate("""node => {
                  const scroller = node.querySelector('.formula-scroll');
                  const number = node.querySelector('.formula-number');
                  return {
                    client: scroller.clientWidth, scroll: scroller.scrollWidth,
                    height: scroller.getBoundingClientRect().height,
                    mathHeight: scroller.querySelector('math').getBoundingClientRect().height,
                    numberSeparated: !number || number.getBoundingClientRect().left >=
                      scroller.getBoundingClientRect().right - 1
                  };
                }""")
                assert metric["height"] >= metric["mathHeight"] - 2
                assert metric["numberSeparated"], (block["id"], metric)
                if metric["scroll"] > metric["client"] + 2:
                    formula_overflow.append(block["id"])
                    if width <= 390:
                        assert node.locator(".formula-view-hint").is_visible()
                    scroller = formula.locator(".formula-scroll")
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2)
                    if block["id"] in ("p285-b008", "p286-b003", "p286-b006", "p287-b008") and width <= 390:
                        node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                if width == 1440 or (width == 350 and mode == "dark"):
                    node.locator("math").select_text()
                    page.keyboard.press("Control+C")
                    copied_text = page.evaluate("navigator.clipboard.readText()")
                    assert len(copied_text.strip()) >= 2, (block["id"], copied_text)
                    copied += 1
                    page.evaluate("getSelection().removeAllRanges()")
                if block["id"] in ("p283-b007", "p285-b008", "p286-b003", "p286-b006", "p287-b008"):
                    node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

            figure_metrics = {}
            for block in FIGURES:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                image = node.locator(".book-figure img")
                image.evaluate("item => item.decode()")
                assert image.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
                assert node.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
                media = node.locator(".figure-media")
                metric = media.evaluate("item => ({client: item.clientWidth, scroll: item.scrollWidth})")
                figure_metrics[block["id"]] = metric
                if width <= 390:
                    assert metric["scroll"] > metric["client"] + 2, (block["id"], metric)
                    assert node.locator(".figure-view-hint").is_visible()
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2)
                    node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                if width in (1440, 350):
                    node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            restored = inspect_progress(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            previous.click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=18" in page.url
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=19']").click()
            page.locator("#read-p292-b009").wait_for()
            assert "chapter=19" in page.url
            assert not errors and not failed_resources, (errors, failed_resources)
            print(json.dumps({
                "viewport": suffix, "blocks": len(actual), "toc": len(DRAFT["toc"]),
                "formulas": len(FORMULAS), "formulaOverflow": formula_overflow,
                "formulaCopied": copied, "figures": figure_metrics, "box19_2": box,
                "bottom": restored, "errors": errors, "failed_resources": failed_resources,
            }, ensure_ascii=False))
            context.close()
        browser.close()
    label = "formal path" if FORMAL else "draft technical baseline"
    print(f"PASS: chapter 19 {label}, five viewports, "
          f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
