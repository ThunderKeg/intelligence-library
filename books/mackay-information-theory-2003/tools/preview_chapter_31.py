"""Inspect chapter 31 draft or registered content in six Edge viewports."""

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
DRAFT_BYTES = (BOOK / "chapter-31.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
assert SHA == "210e574184023956fcbbc43aff57652be64ad041a46cfe44ad863d731d0955b3", (
    "Draft differs from source-stable QA candidate", SHA)
FORMAL_BYTES = (BOOK / "chapter-31.json").read_bytes() if args.formal else None
if args.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if args.formal else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
INLINE_COUNT = sum(
    isinstance(segment, dict) and "mathml" in segment
    for block in BLOCKS
    for field in ("segments", "captionSegments")
    for segment in block.get(field, [])
)
LAST = BLOCKS[-1]["id"]
assert CHAPTER["sourcePdfPages"] == [412, 424]
assert (len(BLOCKS), len(CHAPTER["toc"]), len(FORMULAS), len(FIGURES),
        len(EXERCISES), INLINE_COUNT) == (140, 4, 34, 19, 3, 248)
assert [block["number"] for block in FORMULAS] == [
    f"(31.{number})" for number in range(1, 35)]
assert [block["src"] for block in FIGURES] == [
    f"assets/chapter-31/figure-31-{number}.png" for number in range(1, 20)]
assert [block["label"] for block in EXERCISES] == [
    "▷ 习题 31.1", "▷ 习题 31.2", "习题 31.3"]
assert [block["id"] for block in EXERCISES if block.get("recommendedIcon")] == [
    "p424-b005"]
assert len([block for block in BLOCKS if block["kind"] == "heading"
            and block["level"] == 2]) == 3
assert not any(block["kind"] in ("table", "code", "box", "footnote")
               for block in BLOCKS)
assert LAST == "p424-b006"

BOOK_SCRIPT = None if args.formal else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapter31Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const old31 = chapter31Preview.findIndex(item => item.id === "31");
if (old31 >= 0) chapter31Preview.splice(old31, 1);
chapter31Preview.push({
  id: "31", number: "31", title: "Ising 模型",
  content: "books/mackay-information-theory-2003/chapter-31.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch31-formal-qa" if args.formal else "mackay-ch31-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))
KEY_FIGURES = {"p415-b006", "p416-b001", "p417-b001", "p419-b002",
               "p420-b001", "p421-b007", "p422-b001", "p422-b004", "p423-b002",
               "p423-b006"}


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
      return saved.chapter === '31' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '31' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last))
    assert len({position["top"] for position in positions}) == 1, positions
    assert len({position["y"] for position in positions}) == 1, positions
    state = page.evaluate("""key => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return {chapter: saved.chapter, page: saved.page, block: saved.block,
        updatedAtType: typeof saved.updatedAt,
        width: document.querySelector('#reading-progress').style.width};
    }""", PROGRESS_KEY)
    assert state == {"chapter": "31", "page": 424, "block": last,
                     "updatedAtType": "number", "width": "100%"}, state
    return {"positions": positions, "saved": state}


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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=31")
    page.locator(f"#read-{LAST}").wait_for()
    if args.formal:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith("/books/mackay-information-theory-2003/chapter-31.json")
                   for url in requests)
        assert not any(url.endswith("chapter-31.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-31.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for level in (1, 2, 3):
        expected = sum(block["kind"] == "heading" and block["level"] == level
                       for block in BLOCKS)
        assert page.locator(f".reading-heading h{level}").count() == expected
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 3
        assert page.locator(
            f"{selector} .toc-chapter-link[href$='chapter=31-intro']").count() == 1
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
    assert page.locator(".book-exercise-icon").count() == 1
    icon = page.locator("#read-p424-b005 .book-exercise-icon")
    icon.evaluate("item => item.decode()")
    assert icon.get_attribute("src").endswith("assets/shared/exercise-rat.png")
    assert page.locator(".book-table, .book-code, .book-footnote, .book-box").count() == 0
    assert page.locator(".inline-math math").count() == INLINE_COUNT

    formula_overflow = []
    formula_copied = 0
    for block in FORMULAS:
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        assert node.locator(".formula-number").all_text_contents() == [block["number"]]
        assert node.locator(".book-formula").evaluate("""item => {
          const number = item.querySelector('.formula-number');
          const scroll = item.querySelector('.formula-scroll');
          return number.getBoundingClientRect().left >=
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
        if block["number"] in ("(31.12)", "(31.20)", "(31.28)", "(31.34)") and (
                width, mode) in ((1440, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))
        if block["number"] == "(31.28)" and (width, mode) == (320, "dark"):
            scroll = node.locator(".formula-scroll")
            scroll.evaluate("item => item.scrollLeft = item.scrollWidth")
            scroll.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
            scroll.evaluate("item => item.scrollLeft = 0")

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
        assert node.locator(".figure-caption").count() == 1
        assert node.locator(".figure-caption").inner_text().strip()
        assert node.locator(".figure-caption").evaluate(
            "item => item.scrollWidth <= item.clientWidth + 2"), block["id"]
        media = node.locator(".figure-media")
        metric = local_scroll(media)
        if metric["width"] > metric["client"] + 2:
            figure_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".figure-view-hint").is_visible(), block["id"]
            if width < 800:
                media.evaluate("item => item.scrollLeft = item.scrollWidth")
                if (width, mode) == (320, "dark") and block["id"] in (
                        "p417-b001", "p420-b001"):
                    page.evaluate("""id => { const item = document.getElementById(id);
                      window.scrollTo({top: scrollY + item.getBoundingClientRect().top - 20,
                        behavior: 'instant'}); }""", f"read-{block['id']}")
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    page.screenshot(path=str(
                        QA_DIR / f"figure-{block['id']}-{suffix}-top-right-viewport.png"))
                    page.evaluate("window.scrollBy({top: 650, behavior: 'instant'})")
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    page.screenshot(path=str(
                        QA_DIR / f"figure-{block['id']}-{suffix}-bottom-right-viewport.png"))
                if block["id"] in KEY_FIGURES and (width, mode) in (
                        (390, "light"), (320, "dark")):
                    media.screenshot(path=str(
                        QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                media.evaluate("item => item.scrollLeft = 0")
        if block["id"] in KEY_FIGURES and (width, mode) in (
                (1440, "light"), (390, "light"), (320, "dark")):
            node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
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
        page.locator("#read-p424-b005").screenshot(
            path=str(QA_DIR / f"exercise-31-3-{suffix}.png"))
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.screenshot(path=str(QA_DIR / f"page-top-{suffix}.png"))
    progress = inspect_progress(page)
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.screenshot(path=str(QA_DIR / f"page-bottom-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)

    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=31-intro']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p411-b004").wait_for()
    assert "chapter=31-intro" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=31']").click()
    page.locator(f"#read-{LAST}").wait_for()
    assert "chapter=31" in page.url
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "formulas": len(FORMULAS),
        "formulaOverflow": formula_overflow, "formulaCopied": formula_copied,
        "figures": len(FIGURES), "figureOverflow": figure_overflow,
        "exercises": len(EXERCISES), "inlineMath": len(inline_metrics),
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
        print(f"PASS: chapter 31 {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
