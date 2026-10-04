"""Inspect the MacKay chapter 23 draft in Edge; use --formal after registration."""

from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
from pathlib import Path
import tempfile
import threading

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
parser = ArgumentParser()
parser.add_argument("--formal", action="store_true")
FORMAL = parser.parse_args().formal
DRAFT_BYTES = (BOOK / "chapter-23.draft.json").read_bytes()
FORMAL_BYTES = (BOOK / "chapter-23.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "registered chapter differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
assert CHAPTER["sourcePdfPages"] == [323, 330]
assert (len(BLOCKS), len(CHAPTER["toc"]), len(FORMULAS), len(FIGURES),
        len(EXERCISES)) == (126, 7, 37, 9, 4)
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(23.{n})" for n in range(1, 36)]
assert sum(not block["number"] for block in FORMULAS) == 2
assert not any(block["kind"] == "box" for block in BLOCKS)
BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters23Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const oldChapter23 = chapters23Preview.findIndex(item => item.id === "23");
if (oldChapter23 >= 0) chapters23Preview.splice(oldChapter23, 1);
chapters23Preview.push({
  id: "23", number: "23", title: "常用的概率分布",
  content: "books/mackay-information-theory-2003/chapter-23.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch23-formal-qa" if FORMAL else "mackay-ch23-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p330-b007"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '23' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '23' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last))
    assert len({position["top"] for position in positions}) == 1, positions
    assert len({position["y"] for position in positions}) == 1, positions
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
            errors, failed_resources, requests = [], [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("request", lambda request: requests.append(request.url))
            page.on("requestfailed", lambda request: failed_resources.append(
                f"{request.failure}: {request.url}")
                if request.failure != "net::ERR_ABORTED" else None)
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=23")
            page.locator("#read-p330-b007").wait_for()
            if FORMAL:
                assert any(url.endswith("/books.js") for url in requests)
                assert any(url.endswith("/books/mackay-information-theory-2003/chapter-23.json")
                           for url in requests)

            actual = page.locator(".reading-block").evaluate_all("""items => items.map(
              item => [item.id, [...item.classList].find(name =>
                name.startsWith('reading-') && name !== 'reading-block')])""")
            assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                              for block in BLOCKS]
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").count() == 6
            assert page.locator(".reading-heading h3").count() == 7
            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 6
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")
            assert page.locator(".book-exercise-label").all_text_contents() == [
                block["label"] for block in EXERCISES]
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-formula math").count() == 37
            assert page.locator(".book-figure img").count() == 9
            assert page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=22']").count() == 1
            assert page.locator("#reader-article .outlined-box").count() == 0
            p329 = page.locator("#read-p329-b007")
            assert p329.inner_text().startswith("▷ 习题 23.3")
            assert "更省力的办法" in p329.inner_text()
            p329.screenshot(path=str(QA_DIR / f"exercise-23-3-{suffix}.png"))
            all_inline = page.locator("#reader-article .inline-math").evaluate_all("""items =>
              items.map((item, index) => {
                const hint = item.nextElementSibling;
                return {index, client: item.clientWidth, scroll: item.scrollWidth,
                  hintVisible: !!hint?.classList.contains('inline-math-view-hint') &&
                    !hint.hidden && getComputedStyle(hint).display !== 'none',
                  focusable: item.tabIndex >= 0};
              })""")
            for item in all_inline:
                overflows = item["scroll"] > item["client"] + 2
                assert item["hintVisible"] == overflows, (suffix, item)
                if overflows:
                    assert item["focusable"], (suffix, item)
            inline_metrics = p329.locator(".inline-math").evaluate_all("""items =>
              items.map((item, index) => ({index, client: item.clientWidth,
                scroll: item.scrollWidth, hintVisible:
                  !!item.nextElementSibling?.classList.contains('inline-math-view-hint') &&
                  !item.nextElementSibling.hidden,
                text: item.textContent.slice(0, 50)}))""")
            overflowing_inline = [item for item in inline_metrics
                                  if item["scroll"] > item["client"] + 2]
            for item in overflowing_inline:
                assert item["hintVisible"], (suffix, item)
                node = p329.locator(".inline-math").nth(item["index"])
                node.evaluate("item => item.scrollLeft = item.scrollWidth")
                assert node.evaluate("item => item.scrollLeft") >= (
                    item["scroll"] - item["client"] - 2)
                if width <= 390:
                    node.evaluate("item => item.scrollIntoView({block: 'center', behavior: 'instant'})")
                    node.evaluate("item => item.scrollLeft = item.scrollWidth")
                    page.wait_for_timeout(120)
                    page.screenshot(path=str(QA_DIR / f"exercise-23-3-integral-right-{suffix}.png"))
                node.evaluate("item => item.scrollLeft = 0")

            overflow_formulas, copied = [], 0
            for block in FORMULAS:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                assert node.locator(".book-formula math").count() == 1
                assert node.locator(".formula-number").all_text_contents() == (
                    [block["number"]] if block["number"] else [])
                formula = node.locator(".book-formula")
                metric = formula.evaluate("""node => {
                  const scroller = node.querySelector('.formula-scroll');
                  const math = scroller.querySelector('math');
                  const number = node.querySelector('.formula-number');
                  return {client: scroller.clientWidth, scroll: scroller.scrollWidth,
                    height: scroller.getBoundingClientRect().height,
                    mathHeight: math.getBoundingClientRect().height,
                    separated: !number || number.getBoundingClientRect().left >=
                      scroller.getBoundingClientRect().right - 1};
                }""")
                assert metric["height"] >= metric["mathHeight"] - 2, (block["id"], metric)
                assert metric["separated"], (block["id"], metric)
                if metric["scroll"] > metric["client"] + 2:
                    overflow_formulas.append(block["id"])
                    assert node.locator(".formula-view-hint").is_visible(), block["id"]
                    scroller = formula.locator(".formula-scroll")
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2)
                    if block["id"] in ("p324-b015", "p328-b015", "p329-b003"):
                        node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                if (width == 1440 and mode == "light") or (width == 320 and mode == "dark"):
                    node.locator("math").select_text()
                    page.keyboard.press("Control+C")
                    assert len(page.evaluate("navigator.clipboard.readText()").strip()) >= 2
                    page.evaluate("getSelection().removeAllRanges()")
                    copied += 1
                if block["id"] in ("p324-b015", "p328-b015", "p329-b003"):
                    node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

            figure_metrics = {}
            for block in FIGURES:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                img = node.locator(".book-figure img")
                img.evaluate("item => item.decode()")
                assert img.evaluate("item => [item.naturalWidth, item.naturalHeight]") == [
                    block["width"], block["height"]]
                assert img.get_attribute("alt") == block["alt"]
                assert node.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
                assert node.locator(".figure-caption").count() == 1
                media = node.locator(".figure-media")
                metric = media.evaluate("item => ({client: item.clientWidth, scroll: item.scrollWidth})")
                figure_metrics[block["id"]] = metric
                if width <= 390 and block.get("wide"):
                    assert metric["scroll"] > metric["client"] + 2, (block["id"], metric)
                    assert node.locator(".figure-view-hint").is_visible()
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2)
                    page.wait_for_timeout(120)
                    if block["id"] in ("p327-b001", "p329-b001", "p329-b005"):
                        node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                    if block["id"] in ("p329-b001", "p329-b005"):
                        media.evaluate("item => item.scrollIntoView({block: 'center', behavior: 'instant'})")
                        media.evaluate("item => item.scrollLeft = item.scrollWidth")
                        page.wait_for_timeout(120)
                        page.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right-page.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                if block["id"] in ("p327-b001", "p328-b010", "p329-b001", "p329-b005"):
                    node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
            caption = page.locator("#read-p327-b001 .figure-caption").inner_text()
            assert all(token in caption for token in ("原书图注", "图内横轴"))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            restored = inspect_progress(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=22']").click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=22" in page.url
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=23']").click()
            page.locator("#read-p330-b007").wait_for()
            assert "chapter=23" in page.url
            assert not errors and not failed_resources, (errors, failed_resources)
            print(json.dumps({"viewport": suffix, "blocks": len(actual),
                              "formulas": len(FORMULAS), "formulaOverflow": overflow_formulas,
                              "formulaCopied": copied, "figures": figure_metrics,
                              "inlineOverflowCount": sum(item["scroll"] > item["client"] + 2
                                                         for item in all_inline),
                              "exerciseInlineOverflow": overflowing_inline,
                              "bottom": restored, "errors": errors,
                              "failedResources": failed_resources}, ensure_ascii=False), flush=True)
            context.close()
        browser.close()
    print(f"PASS: chapter 23 {'formal path' if FORMAL else 'draft technical baseline'}, "
          f"six viewports, sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, "
          f"screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
