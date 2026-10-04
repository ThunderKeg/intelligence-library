"""Inspect chapter 32 draft or registered content in six Edge viewports."""

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
DRAFT_BYTES = (BOOK / "chapter-32.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
assert SHA == "75c062af6f29b372fa9521e8876f6647008a1a5c2ed711b999802a2dfc6ead82", (
    "Draft differs from source-stable QA candidate", SHA)
FORMAL_BYTES = (BOOK / "chapter-32.json").read_bytes() if args.formal else None
if args.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if args.formal else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
FOOTNOTES = [block for block in BLOCKS if block["kind"] == "footnote"]
INLINE_COUNT = sum(
    isinstance(segment, dict) and "mathml" in segment
    for block in BLOCKS for field in ("segments", "captionSegments")
    for segment in block.get(field, [])
)
LAST = BLOCKS[-1]["id"]
assert CHAPTER["sourcePdfPages"] == [425, 433]
assert (len(BLOCKS), len(CHAPTER["toc"]), len(FORMULAS), len(FIGURES),
        len(EXERCISES), len(FOOTNOTES), INLINE_COUNT) == (52, 6, 2, 6, 6, 2, 90)
assert [(block["pdfPage"], block["number"]) for block in FORMULAS] == [
    (431, ""), (431, "(32.1)")]
assert [block["src"] for block in FIGURES] == [
    f"assets/chapter-32/{name}" for name in (
        "figure-32-1.png", "figure-32-2.png", "figure-32-3.png",
        "algorithm-32-4.png", "figure-32-5.png", "figure-32-6.png")]
assert [block["label"] for block in EXERCISES] == [
    "▷ 习题 32.1", "▷ 习题 32.2", "习题 32.3", "习题 32.4",
    "▷ 习题 32.5", "习题 32.6"]
assert [block["id"] for block in FOOTNOTES] == ["fn-32-1", "fn-32-2"]
assert [block["label"] for block in FOOTNOTES] == ["1", "2"]
assert len([block for block in BLOCKS if block["kind"] == "heading"
            and block["level"] == 2]) == 5
assert not any(block["kind"] in ("table", "code", "box") for block in BLOCKS)
assert LAST == "p433-b005"

BOOK_SCRIPT = None if args.formal else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapter32Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const old32 = chapter32Preview.findIndex(item => item.id === "32");
if (old32 >= 0) chapter32Preview.splice(old32, 1);
chapter32Preview.push({
  id: "32", number: "32", title: "精确蒙特卡罗采样",
  content: "books/mackay-information-theory-2003/chapter-32.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch32-formal-qa" if args.formal else "mackay-ch32-draft-qa")
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
      return saved.chapter === '32' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '32' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last))
    assert len({position["top"] for position in positions}) == 1, positions
    assert len({position["y"] for position in positions}) == 1, positions
    saved = page.evaluate("""key => {
      const item = JSON.parse(localStorage.getItem(key) || '{}');
      return {chapter: item.chapter, page: item.page, block: item.block,
        updatedAtType: typeof item.updatedAt,
        width: document.querySelector('#reading-progress').style.width};
    }""", PROGRESS_KEY)
    assert saved == {"chapter": "32", "page": 433, "block": last,
                     "updatedAtType": "number", "width": "100%"}, saved
    return {"positions": positions, "saved": saved}


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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=32")
    page.locator(f"#read-{LAST}").wait_for()
    if args.formal:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith("/books/mackay-information-theory-2003/chapter-32.json")
                   for url in requests)
        assert not any(url.endswith("chapter-32.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-32.draft.json") for url in requests)

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
        assert page.locator(f"{selector} .toc-section-link").count() == 5
        assert page.locator(
            f"{selector} .toc-chapter-link[href$='chapter=31']").count() == 1
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
    assert page.locator(".book-footnote").count() == 2
    assert page.locator(".book-footnote-ref a").count() == 2
    for block in FOOTNOTES:
        note = page.locator(f"#read-{block['id']} .book-footnote")
        assert note.is_visible() and block["text"] in note.inner_text()
        link = note.locator("a[href]")
        assert link.count() == 1 and link.is_visible() and link.is_enabled()
        assert link.get_attribute("href") == block["text"]
        assert link.get_attribute("target") == "_blank"
        assert set(link.get_attribute("rel").split()) == {"noopener", "noreferrer"}
        assert link.evaluate("item => getComputedStyle(item).pointerEvents") != "none"
        assert page.locator(
            f".book-footnote-ref a[href='#read-{block['id']}']").count() == 1
        if (width, mode) in ((1440, "light"), (320, "dark")):
            note.screenshot(path=str(QA_DIR / f"footnote-{block['id']}-{suffix}.png"))
    assert page.locator(".book-table, .book-code, .book-box").count() == 0
    assert page.locator(".inline-math math").count() == INLINE_COUNT

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
        caption = node.locator(".figure-caption")
        assert caption.count() == 1 and caption.inner_text().strip()
        assert caption.evaluate("item => item.scrollWidth <= item.clientWidth + 2")
        media = node.locator(".figure-media")
        metric = local_scroll(media)
        if metric["width"] > metric["client"] + 2:
            figure_overflow.append((block["id"], metric["client"], metric["width"]))
            assert node.locator(".figure-view-hint").is_visible(), block["id"]
            if width < 800:
                media.evaluate("item => item.scrollLeft = item.scrollWidth")
                if (width, mode) == (320, "dark") and block["id"] in (
                        "p426-b001", "p428-b001", "p429-b001"):
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
                if (width, mode) in ((390, "light"), (320, "dark")):
                    media.screenshot(path=str(
                        QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                media.evaluate("item => item.scrollLeft = 0")
        if (width, mode) in ((1440, "light"), (390, "light"), (320, "dark")):
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
        for block_id in ("p432-b003", "p433-b002"):
            page.locator(f"#read-{block_id}").screenshot(
                path=str(QA_DIR / f"exercise-{block_id}-{suffix}.png"))
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.screenshot(path=str(QA_DIR / f"page-top-{suffix}.png"))
    progress = inspect_progress(page)
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.screenshot(path=str(QA_DIR / f"page-bottom-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)

    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=31']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p424-b006").wait_for()
    assert "chapter=31" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=32']").click()
    page.locator(f"#read-{LAST}").wait_for()
    assert "chapter=32" in page.url
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "formulas": len(FORMULAS),
        "formulaOverflow": formula_overflow, "formulaCopied": copied,
        "figures": len(FIGURES), "figureOverflow": figure_overflow,
        "exercises": len(EXERCISES), "footnotes": len(FOOTNOTES),
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
        print(f"PASS: chapter 32 {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
