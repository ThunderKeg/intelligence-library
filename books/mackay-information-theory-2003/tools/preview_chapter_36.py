"""Independently inspect MacKay chapter 36 in six Edge viewports.

The draft path injects one temporary books.js entry in the browser. --formal
uses the registered index and JSON without modifying either response.
"""

from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
from pathlib import Path
import re
import tempfile
import threading

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
PARSER = ArgumentParser()
PARSER.add_argument("--formal", action="store_true")
PARSER.add_argument("--sha256", required=True, help="source-stable draft SHA-256")
PARSER.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
ARGS = PARSER.parse_args()

DRAFT_BYTES = (BOOK / "chapter-36.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Draft differs from stable QA candidate", SHA)
FORMAL_BYTES = (BOOK / "chapter-36.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal JSON differs from reviewed draft"
CHAPTER = json.loads((FORMAL_BYTES if ARGS.formal else DRAFT_BYTES).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]


def flatten(blocks):
    for block in blocks:
        if block["kind"] == "box":
            yield from flatten(block["blocks"])
        else:
            yield block


def count_inline(value):
    if isinstance(value, list):
        return sum(count_inline(item) for item in value)
    if isinstance(value, dict):
        if "mathml" in value and "kind" not in value:
            return 1
        return sum(count_inline(item) for key, item in value.items()
                   if key != "mathml")
    return 0


FLAT = list(flatten(BLOCKS))
KINDS = {kind: [block for block in FLAT if block["kind"] == kind]
         for kind in ("formula", "figure", "image", "exercise", "footnote",
                      "code", "table", "list", "heading")}
FORMULAS = KINDS["formula"]
FIGURES = KINDS["figure"] + KINDS["image"]
EXERCISES = KINDS["exercise"]
FOOTNOTES = KINDS["footnote"]
CODES = KINDS["code"]
TABLES = KINDS["table"]
LISTS = KINDS["list"]
BOXES = [block for block in BLOCKS if block["kind"] == "box"]
INLINE_COUNT = count_inline(BLOCKS)
LAST = FLAT[-1]
EXPECTED_TABLES = {
    "p467-b005": {
        "caption": "表 36.2。彩票问题中的效用。",
        "rows": [["", "行动"], ["结果", "买", "不买"],
                 ["未中奖", "−1", "0"], ["中奖", "+9", "0"]],
    },
    "p467-b008": {
        "caption": "表 36.3。彩票问题中的后悔程度。",
        "rows": [["", "行动"], ["结果", "买", "不买"],
                 ["未中奖", "1", "0"], ["中奖", "0", "9"]],
    },
}
assert CHAPTER["bookId"] == "mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [463, 468]
assert BLOCKS[0]["kind"] == "heading" and BLOCKS[0]["level"] == 1
assert sum(block["kind"] == "intro" for block in FLAT) == 1
assert CHAPTER["toc"][0]["number"] == "36"
assert LAST["pdfPage"] == 468 and LAST["id"] == "p468-b009"
assert (len(BLOCKS), len(FLAT), len(CHAPTER["toc"]), len(FORMULAS),
        len(FIGURES), len(EXERCISES), len(TABLES), len(BOXES),
        len(LISTS)) == (93, 93, 4, 16, 1, 9, 2, 0, 0)
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(36.{index})" for index in range(1, 17)]
assert [block["src"] for block in FIGURES] == [
    "assets/chapter-36/figure-36-1.png"]
assert all(block.get("wide") is True and block.get("caption") for block in FIGURES)
assert [block["id"] for block in TABLES] == list(EXPECTED_TABLES)
for block in TABLES:
    expected = EXPECTED_TABLES[block["id"]]
    assert block["caption"] == expected["caption"]
    assert [[cell["text"] for cell in row] for row in block["rows"]] == expected["rows"]
    assert block["rows"][0][1]["colspan"] == 2
assert not CODES and not FOOTNOTES and not BOXES and not LISTS
assert len({block["id"] for block in FLAT + BOXES}) == len(FLAT) + len(BOXES)
assert all(463 <= block["pdfPage"] <= 468 for block in FLAT)
assert all(re.fullmatch(r"\(36\.\d+\)", block["number"])
           for block in FORMULAS if block["number"])

if not ARGS.formal:
    TITLE = CHAPTER["toc"][0]["title"]
    BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + f"""
const chapter36Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const old36 = chapter36Preview.findIndex(item => item.id === "36");
if (old36 >= 0) chapter36Preview.splice(old36, 1);
const chapter35Index = chapter36Preview.findIndex(item => item.id === "35");
chapter36Preview.splice(chapter35Index + 1, 0, {{
  id: "36", number: "36", title: {json.dumps(TITLE, ensure_ascii=False)},
  content: "books/mackay-information-theory-2003/chapter-36.draft.json"
}});
"""
else:
    BOOK_SCRIPT = None

PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch36-formal-qa" if ARGS.formal else "mackay-ch36-draft-qa")
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
    last_id = f"read-{LAST['id']}"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '36' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last_id})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '36' && saved.block === last &&
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
        updatedAtType: typeof item.updatedAt,
        width: document.querySelector('#reading-progress').style.width};
    }""", PROGRESS_KEY)
    assert saved == {"chapter": "36", "page": 468, "block": last_id,
                     "updatedAtType": "number", "width": "100%"}, saved
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=36")
    page.locator(f"#read-{LAST['id']}").wait_for()
    assert any(url.endswith("/books.js") for url in requests)
    if ARGS.formal:
        assert any(url.endswith("/books/mackay-information-theory-2003/chapter-36.json")
                   for url in requests)
        assert not any(url.endswith("chapter-36.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-36.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in FLAT]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for level in (1, 2, 3):
        expected = sum(block["level"] == level for block in KINDS["heading"])
        assert page.locator(f".reading-heading h{level}").count() == expected
    title_tail = page.locator(".reading-heading h1").evaluate("""item => {
      const chars = [];
      const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        for (let index = 0; index < node.textContent.length; index++) {
          const char = node.textContent[index];
          if (!char.trim()) continue;
          const range = document.createRange();
          range.setStart(node, index); range.setEnd(node, index + 1);
          chars.push({char, top: Math.round(range.getBoundingClientRect().top)});
        }
      }
      return chars.slice(-4);
    }""")
    if len(title_tail) == 4 and len({item["top"] for item in title_tail}) != 1:
        page.screenshot(path=str(QA_DIR / f"page-top-{suffix}-orphan.png"))
    assert [item["char"] for item in title_tail] == list("决策理论")
    assert len({item["top"] for item in title_tail}) == 1, (
        "Split title phrase 决策理论", suffix, title_tail)
    for block in KINDS["heading"]:
        if any(isinstance(segment, dict) and segment.get("em") is True
               for segment in block.get("segments", [])):
            assert page.locator(f"#read-{block['id']} em").count() >= 1
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == len(CHAPTER["toc"]) - 1
        assert page.locator(
            f"{selector} .toc-chapter-link[href$='chapter=35']").count() == 1
        for entry in CHAPTER["toc"]:
            assert page.locator(f"#read-{entry['block']}").count() == 1
            assert page.locator(f"{selector} a[href='#read-{entry['block']}']").count() == 1
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
    for number in ("36.2", "36.3"):
        block = next(item for item in EXERCISES if number in item["label"])
        icon = page.locator(f"#read-{block['id']} .book-exercise-icon")
        assert icon.count() == 1
        assert icon.get_attribute("alt") == "原书推荐习题图标"
        assert icon.evaluate("item => item.naturalWidth > 0")
    assert page.locator(".book-footnote").count() == len(FOOTNOTES)
    assert page.locator(".book-code code").count() == len(CODES)
    assert page.locator(".book-table").count() == len(TABLES)
    assert page.locator(".book-box").count() == len(BOXES)
    assert page.locator(".inline-math math").count() == INLINE_COUNT
    for block in FOOTNOTES:
        node = page.locator(f"#read-{block['id']}")
        assert block["text"][:8] in node.inner_text()
    for block in LISTS:
        node = page.locator(f"#read-{block['id']} .book-list")
        assert node.first.locator(":scope > li").count() == len(block["items"])
        if (width, mode) in ((1440, "light"), (320, "dark")):
            page.locator(f"#read-{block['id']}").screenshot(
                path=str(QA_DIR / f"list-{block['id']}-{suffix}.png"))
    for block in BOXES:
        node = page.locator(f"#read-{block['id']}")
        assert node.locator(".reading-block").count() == len(list(flatten(block["blocks"])))
        assert node.evaluate("item => item.classList.contains('outlined-box')")
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"box-{block['id']}-{suffix}.png"))

    formula_overflow, formula_copied = [], 0
    risk_formula_ids = {block["id"] for block in sorted(
        FORMULAS, key=lambda item: len(item.get("mathml", "")), reverse=True)[:8]}
    risk_formula_ids.update(block["id"] for block in FORMULAS
                            if block["number"] in {
                                "(36.1)", "(36.8)", "(36.12)", "(36.13)",
                                "(36.14)", "(36.16)"})
    if FORMULAS:
        risk_formula_ids.update((FORMULAS[0]["id"], FORMULAS[-1]["id"]))
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
            formula_copied += 1
            if block["id"] in risk_formula_ids:
                node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))
        if (width, mode) == (320, "dark") and block["number"] in (
                "(36.8)", "(36.12)", "(36.14)"):
            page.evaluate("""id => { const item = document.getElementById(id);
              window.scrollTo({top: scrollY + item.getBoundingClientRect().top - 80,
                behavior: 'instant'}); }""", f"read-{block['id']}")
            scroller = node.locator(".formula-scroll")
            scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
            assert scroller.evaluate("item => item.scrollLeft") >= (
                metric["width"] - metric["client"] - 2)
            page.screenshot(path=str(
                QA_DIR / f"formula-{block['id']}-{suffix}-right-viewport.png"))
            scroller.evaluate("item => item.scrollLeft = 0")

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
        caption = node.locator(".figure-caption")
        assert caption.count() == bool(block.get("caption") or block.get("annotations"))
        if caption.count():
            assert caption.evaluate("item => item.scrollWidth <= item.clientWidth + 2")
        media = node.locator(".figure-media")
        metric = local_scroll(media)
        if width < 800 and block["width"] >= 700:
            assert block.get("wide") is True, (block["id"], "large figure not wide")
            assert metric["width"] > metric["client"] + 2, (
                block["id"], "large figure shrunk on phone", metric)
        if metric["width"] > metric["client"] + 2:
            figure_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".figure-view-hint").is_visible(), block["id"]
            if (width, mode) == (320, "dark") and "figure-36-1" in block["src"]:
                page.evaluate("""id => { const item = document.getElementById(id);
                  window.scrollTo({top: scrollY + item.getBoundingClientRect().top - 20,
                    behavior: 'instant'}); }""", f"read-{block['id']}")
                media.evaluate("item => item.scrollLeft = (item.scrollWidth - item.clientWidth) / 2")
                page.screenshot(path=str(QA_DIR /
                                         f"figure-{block['id']}-{suffix}-middle-viewport.png"))
                media.evaluate("item => item.scrollLeft = 0")
            if (width, mode) in ((390, "light"), (320, "dark")):
                page.evaluate("""id => { const item = document.getElementById(id);
                  window.scrollTo({top: scrollY + item.getBoundingClientRect().top - 20,
                    behavior: 'instant'}); }""", f"read-{block['id']}")
                media.evaluate("item => item.scrollLeft = item.scrollWidth")
                assert media.evaluate("item => item.scrollLeft") >= (
                    metric["width"] - metric["client"] - 2)
                page.screenshot(path=str(
                    QA_DIR / f"figure-{block['id']}-{suffix}-top-right-viewport.png"))
                assert media.evaluate("item => item.scrollLeft") >= (
                    metric["width"] - metric["client"] - 2)
                if block["height"] > 800 and (width, mode) == (320, "dark"):
                    page.evaluate("window.scrollBy({top: 650, behavior: 'instant'})")
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    page.screenshot(path=str(QA_DIR /
                                             f"figure-{block['id']}-{suffix}-bottom-right-viewport.png"))
                media.evaluate("item => item.scrollLeft = 0")
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
    topbar.evaluate("item => item.style.visibility = ''")

    code_overflow, code_copied = [], 0
    for block in CODES:
        node = page.locator(f"#read-{block['id']}")
        code = node.locator(".book-code code")
        assert code.text_content() == block["text"]
        metric = local_scroll(node.locator(".book-code"))
        if metric["width"] > metric["client"] + 2:
            code_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".code-view-hint").is_visible(), block["id"]
        if (width, mode) in ((1440, "light"), (320, "dark")):
            code.select_text()
            page.keyboard.press("Control+C")
            assert len(page.evaluate("navigator.clipboard.readText()").strip()) >= 2
            page.evaluate("getSelection().removeAllRanges()")
            code_copied += 1
            node.screenshot(path=str(QA_DIR / f"code-{block['id']}-{suffix}.png"))

    table_metrics = []
    for block in TABLES:
        node = page.locator(f"#read-{block['id']}")
        rows = node.locator(".book-table tr")
        expected = EXPECTED_TABLES[block["id"]]
        expected_rows = expected["rows"]
        assert rows.count() == len(expected_rows)
        for index, row in enumerate(expected_rows):
            cells = rows.nth(index).locator("th, td")
            assert cells.count() == len(row)
            assert [item.strip() for item in cells.all_text_contents()] == row
        assert rows.first.locator("th, td").nth(1).get_attribute("colspan") == "2"
        assert node.locator(".book-table caption").inner_text() == expected["caption"]
        table_metrics.append((block["id"], local_scroll(node.locator(".table-scroll"))))
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"table-{block['id']}-{suffix}.png"))

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
    for index, metric in enumerate(inline_metrics):
        if metric["width"] > metric["client"] + 2:
            local_scroll(page.locator(".inline-math").nth(index))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    if (width, mode) in ((1440, "light"), (320, "light"), (320, "dark")):
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.screenshot(path=str(QA_DIR / f"page-top-{suffix}.png"))
    progress = inspect_progress(page)
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.screenshot(path=str(QA_DIR / f"page-bottom-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)

    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=35']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-fn-35-1").wait_for()
    assert "chapter=35" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=36']").click()
    page.locator(f"#read-{LAST['id']}").wait_for()
    assert "chapter=36" in page.url
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "topLevelBlocks": len(BLOCKS),
        "renderedBlocks": len(actual), "toc": len(CHAPTER["toc"]),
        "formulas": len(FORMULAS), "formulaOverflow": formula_overflow,
        "formulaCopied": formula_copied, "figures": len(FIGURES),
        "figureOverflow": figure_overflow, "exercises": len(EXERCISES),
        "footnotes": len(FOOTNOTES), "codes": len(CODES),
        "codeOverflow": code_overflow, "codeCopied": code_copied,
        "tables": table_metrics, "boxes": len(BOXES),
        "inlineMath": len(inline_metrics),
        "inlineOverflow": sum(item["width"] > item["client"] + 2
                              for item in inline_metrics), "progress": progress,
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
        print(f"PASS: chapter 36 {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
