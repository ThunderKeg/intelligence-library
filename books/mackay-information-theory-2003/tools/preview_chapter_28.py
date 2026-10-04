"""Inspect chapter 28 in six Edge viewports; --formal uses the registered path."""

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
DRAFT_BYTES = (BOOK / "chapter-28.draft.json").read_bytes()
assert hashlib.sha256(DRAFT_BYTES).hexdigest() == (
    "fbf6baadc9716c887a91c3ea6528f3f0fd8c7bc557a0bf296ece5d67ebb12515"
), "draft differs from independently reviewed source"
FORMAL_BYTES = (BOOK / "chapter-28.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
TABLE = next(block for block in BLOCKS if block["kind"] == "table")
LISTS = [block for block in BLOCKS if block["kind"] == "list"]
assert CHAPTER["sourcePdfPages"] == [355, 367]
assert (len(BLOCKS), len(CHAPTER["toc"]), len(FORMULAS), len(FIGURES),
        len(EXERCISES), len(TABLE["rows"]), len(LISTS)) == (133, 5, 24, 11, 4, 5, 2)
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(28.{number})" for number in range(1, 23)]
assert [block["start"] for block in LISTS] == [1, 2]
assert BLOCKS[-1]["id"] == "p367-b004"

BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters28Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const old28 = chapters28Preview.findIndex(item => item.id === "28");
if (old28 >= 0) chapters28Preview.splice(old28, 1);
chapters28Preview.push({
  id: "28", number: "28", title: "模型比较与奥卡姆剃刀",
  content: "books/mackay-information-theory-2003/chapter-28.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch28-formal-qa" if FORMAL else "mackay-ch28-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p367-b004"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '28' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '28' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          scrollY: Math.round(scrollY)
        })""", last))
    assert len({position["top"] for position in positions}) == 1, positions
    assert len({position["scrollY"] for position in positions}) == 1, positions
    return positions


def inspect_viewport(browser, base, width, mode):
    suffix = f"{width}-{mode}"
    context = browser.new_context(
        viewport={"width": width, "height": 844}, color_scheme=mode,
        service_workers="block", permissions=["clipboard-read", "clipboard-write"],
    )
    if not FORMAL:
        context.route("**/books.js", lambda route: route.fulfill(
            body=BOOK_SCRIPT, content_type="application/javascript"))
    page = context.new_page()
    errors, failed_resources, requests = [], [], []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: requests.append(request.url))
    page.on("requestfailed", lambda request: failed_resources.append(
        f"{request.failure}: {request.url}") if request.failure != "net::ERR_ABORTED" else None)
    page.on("response", lambda response: failed_resources.append(
        f"{response.status}: {response.url}") if response.status >= 400 else None)
    page.goto(base + "?book=mackay-information-theory-2003&chapter=28")
    page.locator("#read-p367-b004").wait_for()
    if FORMAL:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith(
            "/books/mackay-information-theory-2003/chapter-28.json")
            for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for level, expected in ((1, 1), (2, 4), (3, 10)):
        assert page.locator(f".reading-heading h{level}").count() == expected
    assert page.locator(".reading-heading h3 em").count() == 9
    assert page.locator(".reading-heading h3").last.locator("em").count() == 0
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 4
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("item => item.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("item => item.open")
    for block_id in ("p357-b002", "p357-b003", "p361-b007", "p364-b008"):
        assert page.locator(f"#read-{block_id} em").count() >= 1
    assert page.locator(".book-exercise-label").all_text_contents() == [
        block["label"] for block in EXERCISES]
    for block in LISTS:
        assert page.locator(f"#read-{block['id']} ol").get_attribute("start") == str(block["start"])
    assert page.locator(".book-formula math").count() == 24
    assert page.locator("math merror, .formula-fallback").count() == 0
    assert page.locator(".book-figure img").count() == 11
    assert page.locator(".book-table").count() == 1
    assert page.locator(
        "#chapter-navigation .chapter-navigation-link[href*='chapter=27']").count() == 1

    formula_overflow, copies = [], 0
    for block in FORMULAS:
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        assert node.locator(".book-formula math").count() == 1
        assert node.locator(".formula-number").all_text_contents() == (
            [block["number"]] if block["number"] else [])
        metric = node.locator(".book-formula").evaluate("""node => {
          const scroll = node.querySelector('.formula-scroll');
          const math = scroll.querySelector('math');
          const number = node.querySelector('.formula-number');
          return {client: scroll.clientWidth, width: scroll.scrollWidth,
            height: scroll.getBoundingClientRect().height,
            mathHeight: math.getBoundingClientRect().height,
            numberSeparated: !number || number.getBoundingClientRect().left >=
              scroll.getBoundingClientRect().right - 1};
        }""")
        assert metric["height"] >= metric["mathHeight"] - 2, (block["id"], metric)
        assert metric["numberSeparated"], (block["id"], metric)
        if metric["width"] > metric["client"] + 2:
            formula_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".formula-view-hint").is_visible(), block["id"]
            scroller = node.locator(".formula-scroll")
            scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
            assert scroller.evaluate("item => item.scrollLeft") >= (
                metric["width"] - metric["client"] - 2)
            if block["number"] in ("(28.3)", "(28.8)", "(28.10)", "(28.18)"):
                scroller.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
            scroller.evaluate("item => item.scrollLeft = 0")
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.locator("math").select_text()
            page.keyboard.press("Control+C")
            copied = page.evaluate("navigator.clipboard.readText()")
            assert len(copied.strip()) >= 2, (block["id"], copied)
            page.evaluate("getSelection().removeAllRanges()")
            copies += 1
        if block["number"] in ("(28.3)", "(28.8)", "(28.10)", "(28.14)",
                               "(28.18)", "(28.22)") and (width, mode) in (
                                   (1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

    figure_metrics = {}
    topbar = page.locator(".reader-topbar")
    topbar.evaluate("item => item.style.visibility = 'hidden'")
    for block in FIGURES:
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        image = node.locator(".book-figure img")
        image.evaluate("item => item.decode()")
        assert image.evaluate("item => [item.naturalWidth, item.naturalHeight]") == [
            block["width"], block["height"]]
        assert image.get_attribute("alt") == block["alt"]
        assert node.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
        assert node.locator(".figure-caption").count() == bool(block.get("caption"))
        media = node.locator(".figure-media")
        metric = media.evaluate("item => ({client: item.clientWidth, width: item.scrollWidth})")
        figure_metrics[block["id"]] = metric
        if width <= 390 and block.get("wide"):
            assert metric["width"] > metric["client"] + 2, (block["id"], metric)
            assert node.locator(".figure-view-hint").is_visible()
            media.evaluate("item => item.scrollLeft = item.scrollWidth")
            assert media.evaluate("item => item.scrollLeft") >= metric["width"] - metric["client"] - 2
            if (width, mode) in ((390, "light"), (320, "dark")):
                media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
            media.evaluate("item => item.scrollLeft = 0")
        if (width, mode) in ((1440, "light"), (320, "dark")):
            media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
    topbar.evaluate("item => item.style.visibility = ''")

    table_node = page.locator(f"#read-{TABLE['id']}")
    rows = table_node.locator(".book-table tr")
    assert rows.count() == len(TABLE["rows"])
    for row_index, expected_row in enumerate(TABLE["rows"]):
        cells = rows.nth(row_index).locator("th, td")
        assert cells.count() == len(expected_row)
        for cell_index, expected in enumerate(expected_row):
            cell = cells.nth(cell_index)
            assert (cell.evaluate("item => item.tagName") == "TH") == expected["header"]
            assert cell.inner_text().strip() == expected["text"], (
                row_index, cell_index, cell.inner_text(), expected["text"])
    table_scroll = table_node.locator(".table-scroll")
    table_metric = table_scroll.evaluate("item => ({client: item.clientWidth, width: item.scrollWidth})")
    if table_metric["width"] > table_metric["client"] + 2:
        table_scroll.evaluate("item => item.scrollLeft = item.scrollWidth")
        assert table_scroll.evaluate("item => item.scrollLeft") >= (
            table_metric["width"] - table_metric["client"] - 2)
        table_scroll.screenshot(path=str(QA_DIR / f"table-{suffix}-right.png"))
        table_scroll.evaluate("item => item.scrollLeft = 0")
    table_node.screenshot(path=str(QA_DIR / f"table-{suffix}.png"))
    short_tails = []
    if width < 800:
        short_tails = page.locator(".reading-paragraph").evaluate_all("""elements => {
          const output = [];
          for (const element of elements) {
            const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
            const lines = [];
            let node;
            while ((node = walker.nextNode())) {
              const range = document.createRange();
              for (let i = 0; i < node.textContent.length; i++) {
                const char = node.textContent[i];
                if (!char.trim()) continue;
                range.setStart(node, i);
                range.setEnd(node, i + 1);
                const rect = range.getBoundingClientRect();
                if (!rect.width || !rect.height) continue;
                if (!lines.length || Math.abs(rect.top - lines[lines.length - 1].top) > 8) {
                  lines.push({top: rect.top, text: char});
                } else {
                  lines[lines.length - 1].text += char;
                }
              }
            }
            const tail = lines.at(-1)?.text.trim() || '';
            if (lines.length > 1 && [...tail].length <= 3) {
              output.push({id: element.id, tail, lineCount: lines.length});
            }
          }
          return output;
        }""")
        if mode == "light":
            topbar.evaluate("item => item.style.visibility = 'hidden'")
            for item in short_tails:
                if len(item["tail"]) <= 2:
                    page.locator(f"#{item['id']}").screenshot(
                        path=str(QA_DIR / f"short-tail-{item['id']}-{suffix}.png"))
            if width == 320:
                for block_id in ("p356-b002", "p356-b010"):
                    page.locator(f"#read-{block_id}").screenshot(
                        path=str(QA_DIR / f"fixed-line-{block_id}-{suffix}.png"))
            topbar.evaluate("item => item.style.visibility = ''")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.screenshot(path=str(QA_DIR / f"page-top-{suffix}.png"))

    progress = inspect_progress(page)
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.screenshot(path=str(QA_DIR / f"page-bottom-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)
    page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=27']").click()
    page.locator(".reading-block").first.wait_for()
    assert "chapter=27" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=28']").click()
    page.locator("#read-p367-b004").wait_for()
    assert "chapter=28" in page.url
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "formulas": len(FORMULAS),
        "formulaOverflow": formula_overflow, "formulaCopied": copies,
        "figures": figure_metrics, "table": table_metric, "progress": progress,
        "shortParagraphTails": short_tails,
        "errors": errors, "failedResources": failed_resources,
    }, ensure_ascii=True), flush=True)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0),
                                 partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            )
            for width, mode in VIEWPORTS:
                inspect_viewport(browser, f"http://127.0.0.1:{server.server_port}/",
                                 width, mode)
            browser.close()
        print(f"PASS: chapter 28 {'formal path' if FORMAL else 'draft'} six-viewport QA, "
              f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
