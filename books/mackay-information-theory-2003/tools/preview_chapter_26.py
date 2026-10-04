"""Inspect chapter 26 draft in the reader; use --formal after registration."""

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
arguments = ArgumentParser()
arguments.add_argument("--formal", action="store_true")
FORMAL = arguments.parse_args().formal
DRAFT_BYTES = (BOOK / "chapter-26.draft.json").read_bytes()
FORMAL_BYTES = (BOOK / "chapter-26.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]


def flatten(blocks):
    for block in blocks:
        if block["kind"] == "box":
            yield from flatten(block["blocks"])
        else:
            yield block


VISIBLE_BLOCKS = list(flatten(BLOCKS))
FORMULAS = [block for block in VISIBLE_BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in VISIBLE_BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in VISIBLE_BLOCKS if block["kind"] == "exercise"]
HEADINGS = [block for block in VISIBLE_BLOCKS if block["kind"] == "heading"]
assert CHAPTER["sourcePdfPages"] == [346, 352]
assert (len(BLOCKS), len(VISIBLE_BLOCKS), len(CHAPTER["toc"]),
        len(FORMULAS), len(FIGURES), len(EXERCISES)) == (111, 114, 6, 26, 4, 8)
assert [block["number"] for block in FORMULAS] == [
    f"(26.{number})" for number in range(1, 27)]
assert len([block for block in BLOCKS if block["kind"] == "box"]) == 1
assert BLOCKS[-1]["id"] == "p352-b011"

BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters26Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const id of ["23", "24", "25", "26"]) {
  const old = chapters26Preview.findIndex(item => item.id === id);
  if (old >= 0) chapters26Preview.splice(old, 1);
}
chapters26Preview.push({
  id: "23", number: "23", title: "常用的概率分布",
  content: "books/mackay-information-theory-2003/chapter-23.draft.json"
});
chapters26Preview.push({
  id: "24", number: "24", title: "精确边缘化",
  content: "books/mackay-information-theory-2003/chapter-24.draft.json"
});
chapters26Preview.push({
  id: "25", number: "25", title: "格形图中的精确边缘化",
  content: "books/mackay-information-theory-2003/chapter-25.draft.json"
});
chapters26Preview.push({
  id: "26", number: "26", title: "图中的精确边缘化",
  content: "books/mackay-information-theory-2003/chapter-26.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch26-formal-qa" if FORMAL else "mackay-ch26-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p352-b011"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '26' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '26' && saved.block === last &&
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
            page.goto(base + "?book=mackay-information-theory-2003&chapter=26")
            page.locator("#read-p352-b011").wait_for()
            if FORMAL:
                assert any(url.endswith("/books.js") for url in requests)
                assert any(url.endswith(
                    "/books/mackay-information-theory-2003/chapter-26.json")
                    for url in requests)

            actual = page.locator(".reading-block").evaluate_all("""items => items.map(
              item => [item.id, [...item.classList].find(name =>
                name.startsWith('reading-') && name !== 'reading-block')])""")
            assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                              for block in VISIBLE_BLOCKS]
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").count() == 5
            assert page.locator(".reading-heading h3").count() == 10
            assert all(page.locator(".reading-heading h3").nth(index).locator("em").count()
                       == 1 for index in range(9))
            assert page.locator(".reading-heading h3").nth(9).locator("em").count() == 0
            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(
                    f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 5
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")

            assert page.locator(".book-exercise-label").all_text_contents() == [
                block["label"] for block in EXERCISES]
            assert page.locator(".book-formula math").count() == 26
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator("aside#read-box-26-rules.outlined-box").count() == 1
            assert page.locator("#read-box-26-rules .book-formula math").count() == 2
            assert page.locator("#read-box-26-rules strong").count() == 2
            assert page.locator(
                "#chapter-navigation .chapter-navigation-link[href*='chapter=25']").count() == 1
            for block_id in (
                "p346-b012", "p347-b004", "p348-b002", "p348-b010",
                "p349-b002", "p350-b014", "p351-b001", "p352-b003", "p352-b004",
                "p352-b009", "p352-b011",
            ):
                page.locator(f"#read-{block_id}").screenshot(
                    path=str(QA_DIR / f"block-{block_id}-{suffix}.png"))
            page.locator("#read-box-26-rules").screenshot(
                path=str(QA_DIR / f"box-rules-{suffix}.png"))

            overflow, copies = [], 0
            for block in FORMULAS:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                assert node.locator(".book-formula math").count() == 1
                assert node.locator(".formula-number").all_text_contents() == [block["number"]]
                formula = node.locator(".book-formula")
                metric = formula.evaluate("""node => {
                  const scroll = node.querySelector('.formula-scroll');
                  const math = scroll.querySelector('math');
                  const number = node.querySelector('.formula-number');
                  return {client: scroll.clientWidth, width: scroll.scrollWidth,
                    height: scroll.getBoundingClientRect().height,
                    mathHeight: math.getBoundingClientRect().height,
                    numberSeparated: number.getBoundingClientRect().left >=
                      scroll.getBoundingClientRect().right - 1};
                }""")
                assert metric["height"] >= metric["mathHeight"] - 2, (block["id"], metric)
                assert metric["numberSeparated"], (block["id"], metric)
                if metric["width"] > metric["client"] + 2:
                    overflow.append((block["id"], metric["client"], metric["width"]))
                    assert node.locator(".formula-view-hint").is_visible(), block["id"]
                    scroller = formula.locator(".formula-scroll")
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    if block["number"] in ("(26.4)", "(26.11)", "(26.12)", "(26.22)"):
                        scroller.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                if (width == 1440 and mode == "light") or (width == 320 and mode == "dark"):
                    node.locator("math").select_text()
                    page.keyboard.press("Control+C")
                    copied = page.evaluate("navigator.clipboard.readText()")
                    assert len(copied.strip()) >= 2, (block["id"], copied)
                    page.evaluate("getSelection().removeAllRanges()")
                    copies += 1
                if block["number"] in ("(26.4)", "(26.11)", "(26.12)", "(26.22)"):
                    node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

            figure_metrics = {}
            for block in FIGURES:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                image = node.locator(".book-figure img")
                image.evaluate("item => item.decode()")
                assert image.evaluate("item => [item.naturalWidth, item.naturalHeight]") == [
                    block["width"], block["height"]]
                assert image.get_attribute("alt") == block["alt"]
                assert node.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
                media = node.locator(".figure-media")
                metric = media.evaluate("item => ({client: item.clientWidth, width: item.scrollWidth})")
                figure_metrics[block["id"]] = metric
                assert node.locator(".figure-caption").count() == 1
                if width <= 390:
                    assert metric["width"] > metric["client"] + 2, (block["id"], metric)
                    assert node.locator(".figure-view-hint").is_visible()
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            bottom = inspect_progress(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=25']").click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=25" in page.url
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=26']").click()
            page.locator("#read-p352-b011").wait_for()
            assert "chapter=26" in page.url
            assert not errors and not failed_resources, (errors, failed_resources)
            print(json.dumps({
                "viewport": suffix, "blocks": len(actual), "formulas": len(FORMULAS),
                "formulaOverflow": overflow, "formulaCopied": copies,
                "figures": figure_metrics, "bottom": bottom,
                "errors": errors, "failedResources": failed_resources,
            }, ensure_ascii=False), flush=True)
            context.close()
        browser.close()
    label = "formal path" if FORMAL else "draft technical baseline"
    print(f"PASS: chapter 26 {label}, six viewports, "
          f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
