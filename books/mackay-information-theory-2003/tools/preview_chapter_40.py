"""Independent Edge layout QA for MacKay chapter 40, draft or formal."""

from argparse import ArgumentParser
from collections import Counter
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
PARSER = ArgumentParser()
PARSER.add_argument("--formal", action="store_true")
PARSER.add_argument("--sha256", required=True)
PARSER.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
ARGS = PARSER.parse_args()
DRAFT_BYTES = (BOOK / "chapter-40.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen draft changed", SHA)
FORMAL_BYTES = (BOOK / "chapter-40.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal JSON differs from reviewed draft"
CHAPTER = json.loads((FORMAL_BYTES if ARGS.formal else DRAFT_BYTES).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
KINDS = Counter(block["kind"] for block in BLOCKS)
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
TABLES = [block for block in BLOCKS if block["kind"] == "table"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
LISTS = [block for block in BLOCKS if block["kind"] == "list"]
LAST = BLOCKS[-1]


def inline_count(value):
    if isinstance(value, list):
        return sum(inline_count(item) for item in value)
    if isinstance(value, dict):
        if "mathml" in value and "kind" not in value:
            return 1
        return sum(inline_count(item) for key, item in value.items()
                   if key != "mathml")
    return 0


INLINE_COUNT = inline_count(BLOCKS)
assert CHAPTER["bookId"] == "mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [495, 503]
assert len(BLOCKS) == 89 and len(CHAPTER["toc"]) == 6
assert KINDS == Counter({"paragraph": 54, "formula": 11, "figure": 8,
                         "heading": 6, "exercise": 6, "table": 2,
                         "intro": 1, "list": 1})
assert INLINE_COUNT == 246
assert [block["number"] for block in FORMULAS] == [
    f"(40.{index})" for index in range(1, 12)]
assert [block["src"] for block in FIGURES] == [
    f"assets/chapter-40/figure-40-{index}.png"
    for index in (1, 2, 3, 4, 5, 7, 9, 10)]
assert [block["id"] for block in TABLES] == ["p499-b003", "p500-b012"]
assert [block["label"] for block in EXERCISES] == [
    "▷ 习题 40.4", "习题 40.5", "习题 40.6", "▷ 习题 40.7",
    "习题 40.8", "▷ 习题 40.9"]
assert BLOCKS[0]["kind"] == "heading" and BLOCKS[0]["level"] == 1
assert BLOCKS[0]["text"] == "第 40 章\u3000单个神经元的容量"
assert LAST["id"] == "p503-b004" and LAST["pdfPage"] == 503
assert all(block.get("wide") for block in FIGURES if block["width"] >= 700)
assert len({block["id"] for block in BLOCKS}) == len(BLOCKS)
assert all(495 <= block["pdfPage"] <= 503 for block in BLOCKS)
for block in TABLES:
    assert len(block["rows"]) == 8
    assert [len(row) for row in block["rows"]] == [2] + [9] * 7
    assert block["rows"][0][1].get("colspan") == 8

if ARGS.formal:
    BOOK_SCRIPT = None
else:
    BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const ch40Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const existingCh40 = ch40Preview.findIndex(item => item.id === "40");
if (existingCh40 >= 0) ch40Preview.splice(existingCh40, 1);
const preludeIndex = ch40Preview.findIndex(item => item.id === "40-prelude");
if (preludeIndex < 0) throw Error("Chapter 40 prelude must precede chapter 40");
ch40Preview.splice(preludeIndex + 1, 0, {
  id: "40", number: "40", title: "单个神经元的容量",
  content: "books/mackay-information-theory-2003/chapter-40.draft.json"
});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch40-formal-qa" if ARGS.formal else "mackay-ch40-draft-qa")
QA_DIR.mkdir(exist_ok=True)
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
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
    last_id = f"read-{LAST['id']}"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '40' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last_id})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '40' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last_id})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last_id))
    assert len({item["top"] for item in positions}) == 1, positions
    assert len({item["y"] for item in positions}) == 1, positions
    saved = page.evaluate("""key => {
      const item = JSON.parse(localStorage.getItem(key) || '{}');
      return {chapter: item.chapter, page: item.page, block: item.block,
        width: document.querySelector('#reading-progress').style.width};
    }""", PROGRESS_KEY)
    assert saved == {"chapter": "40", "page": 503, "block": last_id,
                     "width": "100%"}, saved
    return {"positions": positions, "saved": saved}


def inspect_viewport(browser, base, width, mode):
    suffix = f"{width}-{mode}"
    context = browser.new_context(
        viewport={"width": width, "height": 844}, color_scheme=mode,
        service_workers="block", permissions=["clipboard-read", "clipboard-write"])
    if not ARGS.formal:
        context.route("**/books.js", lambda route: route.fulfill(
            body=BOOK_SCRIPT, content_type="application/javascript"))
    page = context.new_page()
    errors, failed_resources, requests = [], [], []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("console", lambda message: errors.append(message.text)
            if message.type == "error" else None)
    page.on("request", lambda request: requests.append(request.url))
    page.on("requestfailed", lambda request: failed_resources.append(
        f"{request.failure}: {request.url}")
        if request.failure != "net::ERR_ABORTED" else None)
    page.on("response", lambda response: failed_resources.append(
        f"{response.status}: {response.url}") if response.status >= 400 else None)
    page.goto(base + "?book=mackay-information-theory-2003&chapter=40")
    page.locator(f"#read-{LAST['id']}").wait_for()
    assert any(url.endswith("/books.js") for url in requests)
    if ARGS.formal:
        assert any(url.endswith("/books/mackay-information-theory-2003/chapter-40.json")
                   for url in requests)
        assert not any(url.endswith("chapter-40.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-40.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert page.locator(".reading-heading h1").text_content() == BLOCKS[0]["text"]
    assert page.locator(".reading-intro").count() == 1
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for level in (1, 2, 3):
        assert page.locator(f".reading-heading h{level}").count() == sum(
            block["level"] == level for block in BLOCKS if block["kind"] == "heading")
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current[href='#read-p495-b001']").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 5
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=40-prelude']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("item => item.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("item => item.open")

    assert page.locator(".book-formula math").count() == 11
    assert page.locator(".book-figure img").count() == 8
    assert page.locator(".book-table").count() == 2
    assert page.locator(".book-exercise-label").count() == 6
    assert page.locator(".inline-math math").count() == INLINE_COUNT
    assert page.locator("math merror, .formula-fallback, .figure-error").count() == 0
    for block in EXERCISES:
        assert block["label"] in page.locator(f"#read-{block['id']}").inner_text()
    for block in LISTS:
        node = page.locator(f"#read-{block['id']} .book-list")
        assert node.locator(":scope > li").count() == len(block["items"])
        assert [item.strip() for item in node.locator(":scope > li").all_text_contents()] == [
            item["text"] for item in block["items"]]

    formula_overflow, copied = [], 0
    for block in FORMULAS:
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        assert node.locator(".formula-number").all_text_contents() == [block["number"]]
        assert node.locator("math").count() == 1
        assert node.locator(".book-formula").evaluate("""item => {
          const number = item.querySelector('.formula-number');
          const scroll = item.querySelector('.formula-scroll');
          return number.getBoundingClientRect().left >=
            scroll.getBoundingClientRect().right - 1;
        }""")
        metric = local_scroll(node.locator(".formula-scroll"))
        if metric["width"] > metric["client"] + 2:
            formula_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".formula-view-hint").is_visible()
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()").strip()
            page.evaluate("getSelection().removeAllRanges()")
            copied += 1
            node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

    figure_overflow = []
    topbar = page.locator(".reader-topbar")
    topbar.evaluate("item => item.style.visibility = 'hidden'")
    for block in FIGURES:
        node = page.locator(f"#read-{block['id']}")
        image = node.locator(".book-figure img")
        image.scroll_into_view_if_needed()
        image.evaluate("item => item.decode()")
        assert image.evaluate("item => [item.naturalWidth, item.naturalHeight]") == [
            block["width"], block["height"]]
        assert image.get_attribute("alt") == block["alt"]
        assert node.locator(".figure-image-link").get_attribute("href").endswith(
            block["src"])
        assert node.locator(".figure-caption").count() == 1
        assert node.locator(".figure-caption").evaluate(
            "item => item.scrollWidth <= item.clientWidth + 2")
        metric = local_scroll(node.locator(".figure-media"))
        if width < 800 and block["width"] >= 700:
            assert block.get("wide") and metric["width"] > metric["client"] + 2
        if metric["width"] > metric["client"] + 2:
            figure_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".figure-view-hint").is_visible()
            if (width, mode) == (320, "dark") and block["id"] in (
                    "p495-b003", "p499-b004", "p501-b001"):
                page.evaluate("""id => { const item = document.getElementById(id);
                  window.scrollTo({top: scrollY + item.getBoundingClientRect().top - 20,
                    behavior: 'instant'}); }""", f"read-{block['id']}")
                node.locator(".figure-media").evaluate("item => item.scrollLeft = item.scrollWidth")
                page.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right-viewport.png"))
                assert node.locator(".figure-media").evaluate("item => item.scrollLeft") >= (
                    metric["width"] - metric["client"] - 2)
                node.locator(".figure-media").evaluate("item => item.scrollLeft = 0")
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
        if (width, mode) == (320, "dark") and metric["width"] > metric["client"] + 2:
            node.locator(".figure-media").evaluate("item => item.scrollLeft = item.scrollWidth")
            node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
            node.locator(".figure-media").evaluate("item => item.scrollLeft = 0")
    topbar.evaluate("item => item.style.visibility = ''")

    table_metrics = []
    for block in TABLES:
        node = page.locator(f"#read-{block['id']}")
        rows = node.locator(".book-table tr")
        assert rows.count() == 8
        for index, expected_row in enumerate(block["rows"]):
            cells = rows.nth(index).locator("th, td")
            assert cells.count() == len(expected_row)
            assert [item.strip() for item in cells.all_text_contents()] == [
                item["text"].strip() for item in expected_row]
            if index == 0:
                assert cells.nth(1).get_attribute("colspan") == "8"
                assert cells.evaluate_all("items => items.every(item => item.tagName === 'TH')")
            elif index == 1:
                assert cells.evaluate_all("items => items.every(item => item.tagName === 'TH')")
        assert block["caption"].split("　")[0] in node.locator("caption").inner_text()
        metric = local_scroll(node.locator(".table-scroll"))
        table_metrics.append((block["id"], metric["client"], metric["width"]))
        if width < 800:
            assert metric["width"] > metric["client"] + 2
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"table-{block['id']}-{suffix}.png"))
        if (width, mode) == (320, "dark"):
            node.locator(".table-scroll").evaluate("item => item.scrollLeft = item.scrollWidth")
            node.screenshot(path=str(QA_DIR / f"table-{block['id']}-{suffix}-right.png"))
            node.locator(".table-scroll").evaluate("item => item.scrollLeft = 0")

    inline_metrics = page.locator(".inline-math").evaluate_all("""items => items.map(
      item => ({client: item.clientWidth, width: item.scrollWidth,
        id: item.closest('.reading-block')?.id,
        focusable: item.tabIndex >= 0,
        hintVisible: !!item.nextElementSibling?.classList.contains('inline-math-view-hint') &&
          getComputedStyle(item.nextElementSibling).display !== 'none'}))""")
    for index, metric in enumerate(inline_metrics):
        overflow = metric["width"] > metric["client"] + 2
        assert metric["hintVisible"] == overflow, metric
        if overflow:
            assert metric["focusable"]
            local_scroll(page.locator(".inline-math").nth(index))
            if (width, mode) == (320, "dark"):
                page.locator(f"#{metric['id']}").screenshot(
                    path=str(QA_DIR / f"inline-overflow-{metric['id']}-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"page-top-{suffix}.png"))
    progress = inspect_progress(page)
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.screenshot(path=str(QA_DIR / f"page-bottom-{suffix}.png"))
    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=40-prelude']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p494-b006").wait_for()
    assert "chapter=40-prelude" in page.url
    page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=40']").click()
    page.locator(f"#read-{LAST['id']}").wait_for()
    assert "chapter=40" in page.url
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "toc": len(CHAPTER["toc"]),
        "formulas": len(FORMULAS), "formulaOverflow": formula_overflow,
        "formulaCopied": copied, "figures": len(FIGURES),
        "figureOverflow": figure_overflow, "tables": table_metrics,
        "exercises": len(EXERCISES), "inlineMath": len(inline_metrics),
        "inlineOverflow": sum(item["width"] > item["client"] + 2
                              for item in inline_metrics),
        "inlineOverflowIds": [item["id"] for item in inline_metrics
                              if item["width"] > item["client"] + 2],
        "progress": progress,
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
                executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            for width, mode in VIEWPORTS:
                if ARGS.only and f"{width}-{mode}" != ARGS.only:
                    continue
                inspect_viewport(browser, f"http://127.0.0.1:{server.server_port}/",
                                 width, mode)
            browser.close()
        print(f"PASS: chapter 40 {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
