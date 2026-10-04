"""Inspect chapter 29 in six Edge viewports; --formal uses the registered path."""

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
parser.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
args = parser.parse_args()
FORMAL = args.formal
ONLY = args.only
DRAFT_BYTES = (BOOK / "chapter-29.draft.json").read_bytes()
assert hashlib.sha256(DRAFT_BYTES).hexdigest() == (
    "b0dda7c7b61a9d58d60261e0acd5a87a7f77a512359fbdd3da900de0894cb35c"
), "draft differs from the source-stable QA candidate"
FORMAL_BYTES = (BOOK / "chapter-29.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]


def flattened(blocks):
    for block in blocks:
        if block["kind"] == "box":
            yield from flattened(block["blocks"])
        else:
            yield block


FLAT = list(flattened(BLOCKS))
FORMULAS = [block for block in FLAT if block["kind"] == "formula"]
FIGURES = [block for block in FLAT if block["kind"] == "figure"]
EXERCISES = [block for block in FLAT if block["kind"] == "exercise"]
FOOTNOTES = [block for block in FLAT if block["kind"] == "footnote"]
TABLES = [block for block in FLAT if block["kind"] == "table"]
CODES = [block for block in FLAT if block["kind"] == "code"]
BOXES = [block for block in BLOCKS if block["kind"] == "box"]
MATRIX = next(block for block in FORMULAS
              if block["pdfPage"] == 384 and not block["number"])
LAST = FLAT[-1]["id"]
assert CHAPTER["sourcePdfPages"] == [369, 398]
assert (len(BLOCKS), len(FLAT), len(CHAPTER["toc"]), len(FORMULAS),
        len(FIGURES), len(EXERCISES), len(FOOTNOTES), len(TABLES),
        len(CODES), len(BOXES)) == (340, 342, 13, 61, 20, 20, 3, 1, 5, 7)
assert sum(1 for _ in BLOCKS) + sum(len(box["blocks"]) for box in BOXES) == 349
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(29.{number})" for number in range(3, 63)]
assert [block["id"] for block in BOXES] == [
    "box-29-370", "box-29-379", "box-29-387-1", "box-29-387-2",
    "box-29-387-3", "box-29-390-1", "box-29-390-2"]
assert [block["id"] for block in FOOTNOTES] == ["fn-29-1", "fn-29-2", "fn-29-3"]
assert len(TABLES[0]["rows"]) == 5 and all(
    len(row) == 2 and all(cell["text"].strip() for cell in row)
    for row in TABLES[0]["rows"]), "PDF 389 operation table has a missing cell"
assert LAST == "p398-b012"

BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapter29Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const old29 = chapter29Preview.findIndex(item => item.id === "29");
if (old29 >= 0) chapter29Preview.splice(old29, 1);
chapter29Preview.push({
  id: "29", number: "29", title: "蒙特卡罗方法",
  content: "books/mackay-information-theory-2003/chapter-29.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch29-formal-qa" if FORMAL else "mackay-ch29-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def local_scroll(node):
    metric = node.evaluate("""item => ({client: item.clientWidth,
      width: item.scrollWidth, height: item.getBoundingClientRect().height})""")
    if metric["width"] > metric["client"] + 2:
        node.evaluate("item => item.scrollLeft = item.scrollWidth")
        assert node.evaluate("item => item.scrollLeft") >= (
            metric["width"] - metric["client"] - 2), metric
        node.evaluate("item => item.scrollLeft = 0")
    return metric


def inspect_progress(page):
    last = f"read-{LAST}"
    page.wait_for_function("""key => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '29';
    }""", arg=PROGRESS_KEY)
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '29' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '29' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last))
    assert len({position["top"] for position in positions}) == 1, positions
    assert len({position["y"] for position in positions}) == 1, positions
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
        f"{request.failure}: {request.url}")
        if request.failure != "net::ERR_ABORTED" else None)
    page.on("response", lambda response: failed_resources.append(
        f"{response.status}: {response.url}") if response.status >= 400 else None)
    page.goto(base + "?book=mackay-information-theory-2003&chapter=29")
    page.locator(f"#read-{LAST}").wait_for()
    if FORMAL:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith("/books/mackay-information-theory-2003/chapter-29.json")
                   for url in requests)
        assert not any(url.endswith("chapter-29.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-29.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in FLAT]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for level in (1, 2, 3):
        expected = sum(block["kind"] == "heading" and block["level"] == level
                       for block in FLAT)
        assert page.locator(f".reading-heading h{level}").count() == expected
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 12
        assert page.locator(f"{selector} .toc-chapter-link[href*='chapter=29-intro']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node => node.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("node => node.open")

    assert page.locator("math merror, .formula-fallback, .figure-error").count() == 0
    assert page.locator(".book-formula math").count() == len(FORMULAS)
    assert page.locator(".book-figure img").count() == len(FIGURES)
    assert page.locator(".book-exercise-label").all_text_contents() == [
        block["label"] for block in EXERCISES]
    assert page.locator(".book-footnote").count() == len(FOOTNOTES)
    assert page.locator(".book-box.outlined-box").count() == len(BOXES)
    assert page.locator(".book-code code").count() == len(CODES)
    for block in FOOTNOTES:
        note = page.locator(f"#read-{block['id']} .book-footnote")
        assert note.is_visible() and block["text"][:8] in note.inner_text()

    box_metrics = []
    for block in BOXES:
        box = page.locator(f"#read-{block['id']}")
        assert box.evaluate("node => getComputedStyle(node).borderTopStyle") == "solid"
        assert box.locator(".reading-block").count() == len(block["blocks"])
        if block["id"] == "box-29-379":
            assert box.locator(".reading-paragraph").count() == 2
            assert box.locator(".reading-formula .formula-number").all_text_contents() == ["(29.32)"]
        if block["id"] in ("box-29-370", "box-29-379"):
            assert box.locator(".book-quote").count() == 0
        box_metrics.append((block["id"], box.bounding_box()["width"]))
        if block["id"] in ("box-29-370", "box-29-379", "box-29-390-1") and (
                width, mode) in ((1440, "light"), (320, "dark")):
            box.screenshot(path=str(QA_DIR / f"{block['id']}-{suffix}.png"))

    formula_overflow = []
    copied = 0
    for block in FORMULAS:
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        assert node.locator(".formula-number").all_text_contents() == (
            [block["number"]] if block["number"] else [])
        assert node.locator(".book-formula").evaluate("""item => {
          const number = item.querySelector('.formula-number');
          const scroll = item.querySelector('.formula-scroll');
          return !number || number.getBoundingClientRect().left >=
            scroll.getBoundingClientRect().right - 1;
        }""")
        metric = local_scroll(node.locator(".formula-scroll"))
        if metric["width"] > metric["client"] + 2:
            formula_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".formula-view-hint").is_visible(), block["id"]
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert len(page.evaluate("navigator.clipboard.readText()").strip()) >= 2
            page.evaluate("getSelection().removeAllRanges()")
            copied += 1
        if (block["number"] in ("(29.4)", "(29.32)", "(29.40)", "(29.60)", "(29.62)")
                or block is MATRIX) and (width, mode) in ((1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))
    matrix_node = page.locator(f"#read-{MATRIX['id']} math mtable")
    assert matrix_node.count() == 1
    assert matrix_node.locator("mtr").count() == 21
    assert all(matrix_node.locator("mtr").nth(index).locator("mtd").count() == 21
               for index in range(21))
    if (width, mode) == (320, "dark"):
        matrix_scroll = page.locator(f"#read-{MATRIX['id']} .formula-scroll")
        matrix_scroll.evaluate("item => item.scrollLeft = item.scrollWidth")
        matrix_scroll.screenshot(path=str(QA_DIR / f"matrix-right-{suffix}.png"))
        matrix_scroll.evaluate("item => item.scrollLeft = 0")

    figure_overflow = []
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
        metric = local_scroll(media)
        if metric["width"] > metric["client"] + 2:
            figure_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".figure-view-hint").is_visible(), block["id"]
            if block["id"] in ("p380-b001", "p388-b001", "p398-b001") and (
                    width, mode) in ((390, "light"), (320, "dark")):
                media.evaluate("item => item.scrollLeft = item.scrollWidth")
                media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                media.evaluate("item => item.scrollLeft = 0")
        if block["id"] in ("p380-b001", "p388-b001", "p398-b001") and (
                width, mode) in ((1440, "light"), (390, "light"), (320, "dark")):
            media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
    topbar.evaluate("item => item.style.visibility = ''")

    code_overflow = []
    code_copies = 0
    for block in CODES:
        node = page.locator(f"#read-{block['id']}")
        code = node.locator(".book-code code")
        assert code.text_content() == block["text"]
        metric = local_scroll(node.locator(".book-code"))
        if metric["width"] > metric["client"] + 2:
            code_overflow.append((block["id"], metric["client"], metric["width"]))
            if width < 800:
                assert node.locator(".code-view-hint").is_visible(), block["id"]
            if block["id"] == "p390-b001" and (width, mode) == (320, "dark"):
                scroll = node.locator(".book-code")
                scroll.evaluate("item => item.scrollLeft = item.scrollWidth")
                scroll.screenshot(path=str(QA_DIR / f"code-{block['id']}-{suffix}-right.png"))
                scroll.evaluate("item => item.scrollLeft = 0")
        if (width, mode) in ((1440, "light"), (320, "dark")):
            code.select_text()
            page.keyboard.press("Control+C")
            assert len(page.evaluate("navigator.clipboard.readText()").strip()) >= 10
            page.evaluate("getSelection().removeAllRanges()")
            code_copies += 1
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"code-{block['id']}-{suffix}.png"))

    table = TABLES[0]
    table_node = page.locator(f"#read-{table['id']}")
    rows = table_node.locator(".book-table tr")
    assert rows.count() == 5
    for index, expected_row in enumerate(table["rows"]):
        cells = rows.nth(index).locator("th, td")
        assert cells.count() == 2
        assert all((cells.nth(j).evaluate("item => item.tagName") == "TH") == cell["header"]
                   for j, cell in enumerate(expected_row))
        assert all(cells.nth(j).inner_text().strip() for j in range(2))
    table_metric = local_scroll(table_node.locator(".table-scroll"))
    if (width, mode) in ((1440, "light"), (320, "dark")):
        table_node.screenshot(path=str(QA_DIR / f"table-{suffix}.png"))

    inline_metrics = page.locator(".inline-math").evaluate_all("""nodes => nodes.map(node => ({
      client: node.clientWidth, width: node.scrollWidth,
      hintVisible: !!node.nextElementSibling?.classList.contains('inline-math-view-hint') &&
        getComputedStyle(node.nextElementSibling).display !== 'none',
      focusable: node.tabIndex >= 0
    }))""")
    for metric in inline_metrics:
        overflows = metric["width"] > metric["client"] + 2
        assert metric["hintVisible"] == overflows, metric
        if overflows:
            assert metric["focusable"], metric

    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.screenshot(path=str(QA_DIR / f"page-top-{suffix}.png"))
    progress = inspect_progress(page)
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.screenshot(path=str(QA_DIR / f"page-bottom-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)

    previous = page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=29-intro']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p368-b010").wait_for()
    assert "chapter=29-intro" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=29']").click()
    page.locator(f"#read-{LAST}").wait_for()
    assert "chapter=29" in page.url
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "renderedBlocks": len(actual), "formulas": len(FORMULAS),
        "formulaOverflow": formula_overflow, "formulaCopied": copied,
        "figures": len(FIGURES), "figureOverflow": figure_overflow,
        "boxes": len(box_metrics), "codes": len(CODES),
        "codeOverflow": code_overflow, "codeCopied": code_copies,
        "table": table_metric, "inlineMath": len(inline_metrics),
        "inlineOverflow": sum(metric["width"] > metric["client"] + 2
                              for metric in inline_metrics), "progress": progress,
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
                if ONLY and f"{width}-{mode}" != ONLY:
                    continue
                inspect_viewport(browser, f"http://127.0.0.1:{server.server_port}/",
                                 width, mode)
            browser.close()
        print(f"PASS: chapter 29 {'formal' if FORMAL else 'draft'} "
              f"{'selected' if ONLY else 'six'}-viewport QA, "
              f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
