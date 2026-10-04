"""Inspect chapter 30 draft or registered content in six Edge viewports."""

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
parser.add_argument("--formal", action="store_true", help="Use real books.js and formal JSON")
parser.add_argument("--expected-sha", help="Require the source-stable draft SHA-256")
parser.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
args = parser.parse_args()
DRAFT_BYTES = (BOOK / "chapter-30.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
if args.expected_sha:
    assert SHA.lower() == args.expected_sha.lower(), "Draft changed after review freeze"
FORMAL_BYTES = (BOOK / "chapter-30.json").read_bytes() if args.formal else None
if args.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if args.formal else DRAFT_BYTES
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
CODES = [block for block in FLAT if block["kind"] == "code"]
BOXES = [block for block in BLOCKS if block["kind"] == "box"]
FOOTNOTES = [block for block in FLAT if block["kind"] == "footnote"]
LAST = FLAT[-1]["id"]
assert CHAPTER["sourcePdfPages"] == [399, 410]
assert (len(BLOCKS), len(FLAT), len(CHAPTER["toc"]), len(FORMULAS),
        len(FIGURES), len(EXERCISES), len(CODES), len(BOXES),
        len(FOOTNOTES)) == (126, 126, 10, 19, 4, 11, 1, 1, 0)
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(30.{number})" for number in range(1, 19)]
assert [block["pdfPage"] for block in FORMULAS if not block["number"]] == [409]
assert [block["src"] for block in FIGURES] == [
    f"assets/chapter-30/{name}" for name in (
        "figure-30-2.png", "figure-30-3.png", "leapfrog-geometry.png",
        "exercise-30-12-slice-direction.png")]
assert BOXES[0]["id"] == "box-30-1" and BOXES[0]["blocks"] == CODES
assert CODES[0]["pdfPage"] == 400 and LAST == "p410-b011"
assert len([block for block in FLAT if block["kind"] == "heading"
            and block["level"] == 2]) == 9
assert not any(block["kind"] == "table" for block in FLAT)

BOOK_SCRIPT = None if args.formal else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapter30Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const old30 = chapter30Preview.findIndex(item => item.id === "30");
if (old30 >= 0) chapter30Preview.splice(old30, 1);
chapter30Preview.push({
  id: "30", number: "30", title: "高效蒙特卡罗方法",
  content: "books/mackay-information-theory-2003/chapter-30.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch30-formal-qa" if args.formal else "mackay-ch30-draft-qa")
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
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '30' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '30' && saved.block === last &&
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
    if not args.formal:
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=30")
    page.locator(f"#read-{LAST}").wait_for()
    if args.formal:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith("/books/mackay-information-theory-2003/chapter-30.json")
                   for url in requests)
        assert not any(url.endswith("chapter-30.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-30.draft.json") for url in requests)

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
        assert page.locator(f"{selector} .toc-section-link").count() == 9
        assert page.locator(
            f"{selector} .toc-chapter-link[href$='chapter=29']").count() == 1
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
    assert page.locator(".book-footnote").count() == 0
    assert page.locator(".book-box.outlined-box").count() == 1
    assert page.locator(".book-code code").count() == 1
    assert page.get_by_text("延伸阅读", exact=True).count() >= 1
    assert page.get_by_text("30.9　解答", exact=True).count() >= 1
    assert "Neal（1993b）" in page.locator("#read-p409-b009").inner_text()
    assert "习题 30.3 的解答" in page.locator("#read-p410-b005").inner_text()
    assert "图内标记译注" in page.locator("#read-p410-b003").inner_text()

    box = page.locator("#read-box-30-1")
    assert box.evaluate("node => getComputedStyle(node).borderTopStyle") == "solid"
    assert box.locator(".reading-block").count() == 1
    assert box.locator(".book-code").count() == 1
    assert box.locator(".book-quote").count() == 0
    code = page.locator(f"#read-{CODES[0]['id']}")
    assert code.locator(".book-code code").text_content() == CODES[0]["text"]
    code_metric = local_scroll(code.locator(".book-code"))
    if code_metric["width"] > code_metric["client"] + 2 and width < 800:
        assert code.locator(".code-view-hint").is_visible()
    code_copied = False
    if (width, mode) in ((1440, "light"), (320, "dark")):
        code.locator("code").select_text()
        page.keyboard.press("Control+C")
        assert page.evaluate("navigator.clipboard.readText()").startswith("g = gradE")
        page.evaluate("getSelection().removeAllRanges()")
        code_copied = True
        box.screenshot(path=str(QA_DIR / f"algorithm-30-1-{suffix}.png"))
    if (width, mode) == (320, "dark"):
        scroll = code.locator(".book-code")
        scroll.evaluate("item => item.scrollLeft = item.scrollWidth")
        scroll.screenshot(path=str(QA_DIR / f"algorithm-30-1-{suffix}-right.png"))
        scroll.evaluate("item => item.scrollLeft = 0")

    formula_overflow = []
    formula_copied = 0
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
        if (block["number"] in ("(30.4)", "(30.5)", "(30.13)", "(30.18)")
                or not block["number"]) and (width, mode) in (
                    (1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

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
        assert node.locator(".figure-image-link").get_attribute("href").endswith(
            block["src"])
        assert node.locator(".figure-caption").count() == bool(block.get("caption"))
        media = node.locator(".figure-media")
        metric = local_scroll(media)
        if metric["width"] > metric["client"] + 2:
            figure_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".figure-view-hint").is_visible(), block["id"]
            if width < 800:
                media.evaluate("item => item.scrollLeft = item.scrollWidth")
                if block["id"] == "p402-b001" and (width, mode) == (320, "dark"):
                    page.evaluate("""id => { const item = document.getElementById(id);
                      window.scrollTo({top: scrollY + item.getBoundingClientRect().top - 20,
                        behavior: 'instant'}); }""", f"read-{block['id']}")
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    page.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-top-right-viewport.png"))
                    page.evaluate("window.scrollBy({top: 650, behavior: 'instant'})")
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    page.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-bottom-right-viewport.png"))
                if (width, mode) in ((390, "light"), (320, "dark")):
                    media.screenshot(path=str(
                        QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                media.evaluate("item => item.scrollLeft = 0")
        if (width, mode) in ((1440, "light"), (390, "light"), (320, "dark")):
            media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
    topbar.evaluate("item => item.style.visibility = ''")

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

    previous = page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=29']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p398-b012").wait_for()
    assert "chapter=29" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=30']").click()
    page.locator(f"#read-{LAST}").wait_for()
    assert "chapter=30" in page.url
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "renderedBlocks": len(actual),
        "formulas": len(FORMULAS), "formulaOverflow": formula_overflow,
        "formulaCopied": formula_copied, "figures": len(FIGURES),
        "figureOverflow": figure_overflow, "exercises": len(EXERCISES),
        "code": code_metric, "codeCopied": code_copied,
        "inlineMath": len(inline_metrics),
        "inlineOverflow": sum(metric["width"] > metric["client"] + 2
                              for metric in inline_metrics),
        "progress": progress, "errors": errors,
        "failedResources": failed_resources,
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
                if args.only and f"{width}-{mode}" != args.only:
                    continue
                inspect_viewport(browser, f"http://127.0.0.1:{server.server_port}/",
                                 width, mode)
            browser.close()
        print(f"PASS: chapter 30 {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
