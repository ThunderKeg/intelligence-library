"""Inspect About Chapter 29 in six Edge viewports; --formal uses the registered path."""

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
arguments.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                        "390-dark", "320-light", "320-dark"))
args = arguments.parse_args()
FORMAL = args.formal
ONLY = args.only
DRAFT_BYTES = (BOOK / "chapter-29-intro.draft.json").read_bytes()
assert hashlib.sha256(DRAFT_BYTES).hexdigest() == (
    "352c87f220c19a60bfb52bcf6e39c48c7b94058d17c95a162b1becfdfdd9a637"
), "draft differs from independently reviewed source"
FORMAL_BYTES = (BOOK / "chapter-29-intro.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
PARAGRAPHS = [block for block in BLOCKS if block["kind"] == "paragraph"]
INLINE_COUNT = sum(
    isinstance(segment, dict) and "mathml" in segment
    for block in BLOCKS for segment in block.get("segments", [])
)
assert CHAPTER["sourcePdfPages"] == [368, 368]
assert (len(BLOCKS), len(PARAGRAPHS), len(FORMULAS), len(CHAPTER["toc"]),
        INLINE_COUNT) == (10, 7, 2, 1, 14)
assert [block["number"] for block in FORMULAS] == ["(29.1)", "(29.2)"]

BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const about29PreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const existingAbout29 = about29PreviewChapters.findIndex(item => item.id === "29-intro");
if (existingAbout29 >= 0) about29PreviewChapters.splice(existingAbout29, 1);
about29PreviewChapters.push({
  id: "29-intro", number: "导页", title: "关于第 29 章",
  content: "books/mackay-information-theory-2003/chapter-29-intro.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch29-intro-formal-qa" if FORMAL else "mackay-ch29-intro-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p368-b010"
    # The reader starts tracking after fonts load; wait for its initial save before scrolling.
    page.wait_for_function("""key => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '29-intro';
    }""", arg=PROGRESS_KEY)
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    try:
        page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '29-intro' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last}, timeout=10000)
    except Exception:
        state = page.evaluate("""key => ({
          saved: JSON.parse(localStorage.getItem(key) || '{}'),
          progress: document.querySelector('#reading-progress').style.width,
          y: Math.round(scrollY), height: innerHeight,
          scrollHeight: document.documentElement.scrollHeight,
          lastTop: Math.round(document.querySelector('#read-p368-b010').getBoundingClientRect().top)
        })""", PROGRESS_KEY)
        raise AssertionError(f"page-bottom progress mismatch: {state}")
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '29-intro' && saved.block === last &&
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=29-intro")
    page.locator("#read-p368-b010").wait_for()
    if FORMAL:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith(
            "/books/mackay-information-theory-2003/chapter-29-intro.json")
            for url in requests)
        assert not any(url.endswith("chapter-29-intro.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-29-intro.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-heading h2, .reading-heading h3").count() == 0
    assert page.locator(".reading-paragraph").count() == 7
    assert page.locator("#read-p368-b003 em").count() == 5
    assert "Metropolis" in page.locator("#read-p368-b003").inner_text()
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 0
        assert page.locator(
            f"{selector} .toc-chapter-link[href*='chapter=28']").count() == 1
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p368-b001']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node => node.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("node => node.open")

    assert page.locator(".book-formula math").count() == 2
    assert page.locator(".inline-math math").count() == INLINE_COUNT
    assert page.locator("math merror, .formula-fallback").count() == 0
    assert page.locator(".book-figure img, .book-table, .book-exercise-label").count() == 0
    assert page.locator("#read-p368-b007 math").text_content() == "𝐮=𝐌𝐯"
    assert page.locator("#read-p368-b009 math msup").count() == 3
    assert page.locator("#read-p368-b010 .inline-math").count() == 11
    for index in (0, 1):
        assert page.locator("#read-p368-b010 .inline-math").nth(index).locator(
            "msub").count() == 1
    assert "π" in page.locator("#read-p368-b010 .inline-math").last.text_content()
    formula_metrics = []
    copied = 0
    for block in FORMULAS:
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        assert node.locator(".formula-number").all_text_contents() == [block["number"]]
        metric = node.locator(".book-formula").evaluate("""node => {
          const scroll = node.querySelector('.formula-scroll');
          const math = scroll.querySelector('math');
          const number = node.querySelector('.formula-number');
          return {client: scroll.clientWidth, width: scroll.scrollWidth,
            height: scroll.getBoundingClientRect().height,
            mathHeight: math.getBoundingClientRect().height,
            separated: number.getBoundingClientRect().left >=
              scroll.getBoundingClientRect().right - 1,
            mathText: math.textContent};
        }""")
        assert metric["height"] >= metric["mathHeight"] - 2, metric
        assert metric["separated"], metric
        if metric["width"] > metric["client"] + 2:
            assert node.locator(".formula-view-hint").is_visible(), block["id"]
            scroller = node.locator(".formula-scroll")
            scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
            assert scroller.evaluate("item => item.scrollLeft") >= (
                metric["width"] - metric["client"] - 2)
            scroller.evaluate("item => item.scrollLeft = 0")
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert len(page.evaluate("navigator.clipboard.readText()").strip()) >= 3
            page.evaluate("getSelection().removeAllRanges()")
            copied += 1
        node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))
        formula_metrics.append(metric)

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
    inline_copied = 0
    if (width, mode) == (320, "dark"):
        for index in (0, 1, 6, 10):
            node = page.locator("#read-p368-b010 .inline-math").nth(index)
            node.scroll_into_view_if_needed()
            node.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert len(page.evaluate("navigator.clipboard.readText()").strip()) >= 2
            page.evaluate("getSelection().removeAllRanges()")
            inline_copied += 1
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.locator("#read-p368-b003").screenshot(path=str(QA_DIR / f"methods-{suffix}.png"))
    page.locator("#read-p368-b010").screenshot(path=str(QA_DIR / f"transition-{suffix}.png"))
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"page-{suffix}.png"), full_page=True)

    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href*='chapter=28']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p367-b004").wait_for()
    assert "chapter=28" in page.url
    assert page.locator(
        "#chapter-navigation .chapter-navigation-link[href*='chapter=29-intro']"
    ).count() == 1
    page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=29-intro']").click()
    page.locator("#read-p368-b010").wait_for()
    assert "chapter=29-intro" in page.url
    progress = inspect_progress(page)
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "formulas": formula_metrics,
        "formulaCopied": copied, "inlineCopied": inline_copied, "inlineOverflow": sum(
            metric["width"] > metric["client"] + 2 for metric in inline_metrics),
        "progress": progress, "errors": errors, "failedResources": failed_resources,
    }, ensure_ascii=False), flush=True)


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
        print("PASS: About Chapter 29 " + ("formal" if FORMAL else "draft") +
              (" selected-viewport QA, " if ONLY else " six-viewpoint QA, ") +
              f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
