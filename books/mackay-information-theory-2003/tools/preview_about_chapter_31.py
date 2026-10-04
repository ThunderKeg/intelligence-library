"""Inspect About Chapter 31 in six Edge viewports, draft or formal."""

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
parser.add_argument("--expected-sha", help="Require the source-stable draft SHA-256")
parser.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
args = parser.parse_args()
DRAFT_BYTES = (BOOK / "chapter-31-intro.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
if args.expected_sha:
    assert SHA.lower() == args.expected_sha.lower(), "Draft changed after review freeze"
FORMAL_BYTES = (BOOK / "chapter-31-intro.json").read_bytes() if args.formal else None
if args.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if args.formal else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
LAST = BLOCKS[-1]["id"]
assert CHAPTER["sourcePdfPages"] == [411, 411]
assert len(BLOCKS) == 4 and [block["kind"] for block in BLOCKS] == [
    "heading", "paragraph", "paragraph", "paragraph"]
assert BLOCKS[0]["level"] == 1 and LAST == "p411-b004"
assert len(CHAPTER["toc"]) == 1 and CHAPTER["toc"][0]["block"] == BLOCKS[0]["id"]
assert not any(block["kind"] in ("figure", "formula", "exercise", "table", "code",
                                  "footnote", "box") for block in BLOCKS)

BOOK_SCRIPT = None if args.formal else (ROOT / "books.js").read_text(encoding="utf-8") + """
const about31PreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const existingAbout31 = about31PreviewChapters.findIndex(item => item.id === "31-intro");
if (existingAbout31 >= 0) about31PreviewChapters.splice(existingAbout31, 1);
about31PreviewChapters.push({
  id: "31-intro", number: "导页", title: "关于第 31 章",
  content: "books/mackay-information-theory-2003/chapter-31-intro.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch31-intro-formal-qa" if args.formal else "mackay-ch31-intro-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = f"read-{LAST}"
    page.wait_for_function("""key => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '31-intro';
    }""", arg=PROGRESS_KEY)
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    try:
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '31-intro' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last}, timeout=10000)
    except Exception:
        state = page.evaluate("""({key, last}) => ({
          saved: JSON.parse(localStorage.getItem(key) || '{}'),
          progress: document.querySelector('#reading-progress').style.width,
          y: Math.round(scrollY), height: innerHeight,
          scrollHeight: document.documentElement.scrollHeight,
          lastTop: Math.round(document.getElementById(last).getBoundingClientRect().top)
        })""", {"key": PROGRESS_KEY, "last": last})
        raise AssertionError(f"page-bottom progress mismatch: {state}")
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '31-intro' && saved.block === last &&
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
        service_workers="block",
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=31-intro")
    page.locator(f"#read-{LAST}").wait_for()
    if args.formal:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith(
            "/books/mackay-information-theory-2003/chapter-31-intro.json")
            for url in requests)
        assert not any(url.endswith("chapter-31-intro.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-31-intro.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-heading h2, .reading-heading h3").count() == 0
    assert page.locator(".reading-paragraph").count() == 3
    assert page.locator(".reading-heading h1").inner_text() == BLOCKS[0]["text"]
    assert "Ising" in page.locator("#read-p411-b002").inner_text()
    assert all(fragment in page.locator("#read-p411-b003").inner_text()
               for fragment in ("第 25 章", "第 17 章", "二维条码", "容量"))
    assert all(fragment in page.locator("#read-p411-b004").inner_text()
               for fragment in ("附录 B", "Reif", "1965"))
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 0
        assert page.locator(
            f"{selector} .toc-chapter-link[href$='chapter=30']").count() == 1
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p411-b001']"
        ).count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node => node.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("node => node.open")

    assert page.locator(".book-formula, .inline-math, .book-figure, .book-table, "
                        ".book-code, .book-exercise-label, .book-footnote").count() == 0
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"page-top-{suffix}.png"))
    page.locator("#read-p411-b003").screenshot(
        path=str(QA_DIR / f"paragraph-2-{suffix}.png"))

    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=30']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p410-b011").wait_for()
    assert "chapter=30" in page.url
    next_link = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=31-intro']")
    assert next_link.count() == 1
    next_link.click()
    page.locator(f"#read-{LAST}").wait_for()
    assert "chapter=31-intro" in page.url
    progress = inspect_progress(page)
    page.screenshot(path=str(QA_DIR / f"page-bottom-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "paragraphs": 3,
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
        print(f"PASS: About Chapter 31 {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
