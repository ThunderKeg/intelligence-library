"""Independently inspect MacKay PDF494 pre-chapter exercises in six Edge viewports.

Draft mode temporarily appends chapter 39 and the prelude in the browser's
books.js response. Formal mode uses the unmodified registered index and JSON.
"""

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
PARSER = ArgumentParser()
PARSER.add_argument("--formal", action="store_true")
PARSER.add_argument("--sha256", required=True)
PARSER.add_argument("--bare-scroll", action="store_true",
                    help="scroll as soon as the last DOM block appears")
PARSER.add_argument("--seed-interior", action="store_true",
                    help="seed a saved interior block then reopen and scroll early")
PARSER.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
ARGS = PARSER.parse_args()

DRAFT_BYTES = (BOOK / "chapter-40-prelude.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Draft differs from frozen SHA", SHA)
FORMAL_BYTES = (BOOK / "chapter-40-prelude.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal JSON differs from reviewed draft"
CHAPTER = json.loads((FORMAL_BYTES if ARGS.formal else DRAFT_BYTES).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
LAST = BLOCKS[-1]
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [494, 494]
assert len(BLOCKS) == 6
assert [block["kind"] for block in BLOCKS] == [
    "heading", "exercise", "paragraph", "exercise", "exercise", "paragraph"]
assert [block["id"] for block in BLOCKS] == [f"p494-b{n:03d}" for n in range(1, 7)]
assert [block["label"] for block in BLOCKS if block["kind"] == "exercise"] == [
    "▷ 习题 40.1", "▷ 习题 40.2", "▷ 习题 40.3"]
assert len(CHAPTER["toc"]) == 1 and CHAPTER["toc"][0]["block"] == "p494-b001"
assert LAST["id"] == "p494-b006"
assert not any(block["kind"] in ("figure", "formula", "table", "code",
                                  "footnote", "box") for block in BLOCKS)
assert sum(isinstance(segment, dict) and "mathml" in segment
           for block in BLOCKS for segment in block.get("segments", [])) == 5

BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(encoding="utf-8") + """
const ch40PreludePreview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
if (!ch40PreludePreview.some(item => item.id === "39")) ch40PreludePreview.push({
  id: "39", number: "39", title: "作为分类器的单个神经元",
  content: "books/mackay-information-theory-2003/chapter-39.draft.json"
});
const existingCh40Prelude = ch40PreludePreview.findIndex(item => item.id === "40-prelude");
if (existingCh40Prelude >= 0) ch40PreludePreview.splice(existingCh40Prelude, 1);
ch40PreludePreview.push({
  id: "40-prelude", number: "预习题", title: "阅读第 40 章之前的习题",
  content: "books/mackay-information-theory-2003/chapter-40-prelude.draft.json"
});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch40-prelude-formal-qa" if ARGS.formal else "mackay-ch40-prelude-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last_id = f"read-{LAST['id']}"
    if not ARGS.bare_scroll:
        page.evaluate("""async () => {
          await document.fonts.ready;
          await new Promise(resolve => requestAnimationFrame(() =>
            requestAnimationFrame(resolve)));
        }""")
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    try:
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '40-prelude' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last_id}, timeout=10000)
    except Exception:
        state = page.evaluate("""({key, last}) => ({
          saved: JSON.parse(localStorage.getItem(key) || '{}'),
          progress: document.querySelector('#reading-progress').style.width,
          scrollY, innerHeight, scrollHeight: document.documentElement.scrollHeight,
          lastTop: document.getElementById(last).getBoundingClientRect().top,
          url: location.href
        })""", {"key": PROGRESS_KEY, "last": last_id})
        raise AssertionError(f"Page-bottom progress mismatch: {state}")
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '40-prelude' && saved.block === last &&
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
    assert saved == {"chapter": "40-prelude", "page": 494, "block": last_id,
                     "updatedAtType": "number", "width": "100%"}, saved
    return {"positions": positions, "saved": saved}


def inspect_seeded_early_scroll(page):
    seeded = "read-p494-b003"
    page.evaluate("""({key, seeded}) => localStorage.setItem(key, JSON.stringify({
      chapter: '40-prelude', page: 494, block: seeded, updatedAt: Date.now()
    }))""", {"key": PROGRESS_KEY, "seeded": seeded})
    page.reload()
    page.locator(f"#read-{LAST['id']}").wait_for()
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    try:
        page.wait_for_function("""key => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '40-prelude' && saved.block === 'read-p494-b006' &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg=PROGRESS_KEY, timeout=10000)
    except Exception:
        state = page.evaluate("""key => ({
          saved: JSON.parse(localStorage.getItem(key) || '{}'),
          progress: document.querySelector('#reading-progress').style.width,
          y: scrollY, innerHeight, height: document.documentElement.scrollHeight,
          firstTop: document.getElementById('read-p494-b001').getBoundingClientRect().top,
          middleTop: document.getElementById('read-p494-b003').getBoundingClientRect().top,
          lastTop: document.getElementById('read-p494-b006').getBoundingClientRect().top
        })""", PROGRESS_KEY)
        raise AssertionError(f"Seeded early scroll mismatch: {state}")
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '40-prelude' && saved.block === 'read-p494-b006' &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg=PROGRESS_KEY)
        positions.append(page.evaluate("""() => ({
          top: Math.round(document.getElementById('read-p494-b006').getBoundingClientRect().top),
          y: Math.round(scrollY)
        })"""))
    assert len({item["top"] for item in positions}) == 1, positions
    assert len({item["y"] for item in positions}) == 1, positions
    return {"seeded": seeded, "positions": positions}


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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=40-prelude")
    page.locator(f"#read-{LAST['id']}").wait_for()
    assert any(url.endswith("/books.js") for url in requests)
    if ARGS.formal:
        assert any(url.endswith("/books/mackay-information-theory-2003/chapter-40-prelude.json")
                   for url in requests)
        assert not any(url.endswith("chapter-40-prelude.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-40-prelude.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-heading h1").inner_text() == BLOCKS[0]["text"]
    assert page.locator(".reading-heading h2, .reading-heading h3").count() == 0
    assert page.locator(".reading-paragraph").count() == 2
    assert page.locator(".book-exercise-label").count() == 3
    for block in BLOCKS:
        if block["kind"] == "exercise":
            node = page.locator(f"#read-{block['id']}")
            assert block["label"] in node.inner_text(), block["id"]
            assert "难度 2" in node.inner_text(), block["id"]
    assert "上方所有行" in page.locator("#read-p494-b004").inner_text()
    assert all(name in page.locator("#read-p494-b006").inner_text()
               for name in ("Polya", "Cover", "Yaser Abu-Mostafa"))
    assert page.locator(".book-figure, .book-formula, .book-table, .book-code, "
                        ".book-footnote").count() == 0
    assert page.locator(".inline-math math").count() == 5
    assert page.locator("math merror, .formula-fallback").count() == 0
    inline_metrics = page.locator(".inline-math").evaluate_all("""items => items.map(
      item => ({client: item.clientWidth, width: item.scrollWidth,
        focusable: item.tabIndex >= 0,
        hintVisible: !!item.nextElementSibling?.classList.contains('inline-math-view-hint') &&
          getComputedStyle(item.nextElementSibling).display !== 'none'}))""")
    for metric in inline_metrics:
        overflow = metric["width"] > metric["client"] + 2
        assert metric["hintVisible"] == overflow, metric
        if overflow:
            assert metric["focusable"], metric
    copied = 0
    if (width, mode) in ((1440, "light"), (320, "dark")):
        for node in page.locator(".inline-math math").all():
            node.scroll_into_view_if_needed()
            node.select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()").strip()
            page.evaluate("getSelection().removeAllRanges()")
            copied += 1

    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current[href='#read-p494-b001']").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 0
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=39']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("item => item.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("item => item.open")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"page-{suffix}.png"), full_page=True)

    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=39']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p493-b004").wait_for()
    assert "chapter=39" in page.url
    page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=40-prelude']").click()
    page.locator(f"#read-{LAST['id']}").wait_for()
    progress = inspect_progress(page)
    seeded_early = inspect_seeded_early_scroll(page) if ARGS.seed_interior else None
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "toc": len(CHAPTER["toc"]),
        "exercises": 3, "inlineMath": len(inline_metrics), "copied": copied,
        "inlineOverflow": sum(item["width"] > item["client"] + 2
                              for item in inline_metrics), "progress": progress,
        "seededEarly": seeded_early,
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
        print(f"PASS: chapter 40 prelude {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
