"""Independent six-viewport QA for MacKay Part V's title page.

Draft mode injects temporary entries into the browser's books.js response.
Formal mode loads the registered books.js and JSON without interception.
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
PARSER.add_argument("--sha256", required=True)
PARSER.add_argument("--formal", action="store_true")
PARSER.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
ARGS = PARSER.parse_args()

DRAFT_BYTES = (BOOK / "chapter-V.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Part V draft changed", SHA)
if ARGS.formal:
    FORMAL_BYTES = (BOOK / "chapter-V.json").read_bytes()
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal Part V differs from reviewed draft"
else:
    FORMAL_BYTES = None
PART = json.loads((FORMAL_BYTES or DRAFT_BYTES).decode("utf-8"))
assert PART["bookId"] == "mackay-information-theory-2003"
assert PART["sourcePdfPages"] == [479, 479]
assert len(PART["toc"]) == 1 and PART["toc"][0] == {
    "number": "第五部分", "title": "神经网络", "block": "p479-b001"}
assert len(PART["blocks"]) == 2
HEADING, FIGURE = PART["blocks"]
assert (HEADING["id"], HEADING["kind"], HEADING["level"], HEADING["text"]) == (
    "p479-b001", "heading", 1, "第五部分　神经网络")
assert HEADING["segments"] == ["第五部分\n神经网络"]
assert (FIGURE["id"], FIGURE["kind"], FIGURE["src"]) == (
    "p479-b002", "figure", "assets/part-V-emblem.png")
assert (FIGURE["width"], FIGURE["height"]) == (847, 930)
assert not FIGURE.get("caption") and not FIGURE.get("annotations")

if not ARGS.formal:
    BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const partVPreview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const id of ["37", "V"]) {
  const index = partVPreview.findIndex(item => item.id === id);
  if (index >= 0) partVPreview.splice(index, 1);
}
const after36 = partVPreview.findIndex(item => item.id === "36");
if (after36 < 0) throw Error("Cannot find chapter 36 for Part V draft preview");
partVPreview.splice(after36 + 1, 0,
  {id: "37", number: "37", title: "贝叶斯推断与抽样理论",
   content: "books/mackay-information-theory-2003/chapter-37.draft.json"},
  {id: "V", number: "第五部分", title: "神经网络",
   content: "books/mackay-information-theory-2003/chapter-V.draft.json"});
"""
else:
    BOOK_SCRIPT = None

PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-part-V-formal-qa" if ARGS.formal else "mackay-part-V-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_viewport(browser, base, width, mode):
    suffix = f"{width}-{mode}"
    context = browser.new_context(
        viewport={"width": width, "height": 844}, color_scheme=mode,
        service_workers="block")
    if not ARGS.formal:
        context.route("**/books.js", lambda route: route.fulfill(
            body=BOOK_SCRIPT, content_type="application/javascript"))
    page = context.new_page()
    errors, failed, requests = [], [], []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("console", lambda message: errors.append(message.text)
            if message.type == "error" else None)
    page.on("request", lambda request: requests.append(request.url))
    page.on("requestfailed", lambda request: failed.append(
        f"{request.failure}: {request.url}")
        if request.failure != "net::ERR_ABORTED" else None)
    page.on("response", lambda response: failed.append(
        f"{response.status}: {response.url}") if response.status >= 400 else None)
    page.goto(base + "?book=mackay-information-theory-2003&chapter=V")
    page.locator("#read-p479-b002 .book-figure img").wait_for()
    assert any(url.endswith("/books.js") for url in requests)
    expected_json = "chapter-V.json" if ARGS.formal else "chapter-V.draft.json"
    assert any(url.endswith(expected_json) for url in requests), requests
    if ARGS.formal:
        assert not any(url.endswith("chapter-V.draft.json") for url in requests)
    assert page.evaluate("document.documentElement.dataset.theme") == mode

    blocks = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert blocks == [["read-p479-b001", "reading-heading"],
                      ["read-p479-b002", "reading-figure"]]
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-block:not(.reading-heading):not(.reading-figure)").count() == 0
    assert page.locator(".book-formula, .book-exercise, .book-table, .book-footnote").count() == 0
    assert "".join(page.locator(".reading-heading h1").inner_text().split()) == "第五部分神经网络"
    lines = page.locator(".reading-heading h1").evaluate("""item => {
      const lines = new Map();
      const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        for (let i = 0; i < node.length; i++) {
          if (!node.textContent[i].trim()) continue;
          const range = document.createRange();
          range.setStart(node, i); range.setEnd(node, i + 1);
          const top = Math.round(range.getBoundingClientRect().top);
          lines.set(top, (lines.get(top) || '') + node.textContent[i]);
        }
      }
      return [...lines.values()];
    }""")
    page.screenshot(path=str(QA_DIR / f"top-{suffix}.png"))
    assert lines in (["第五部分神经网络"], ["第五部分", "神经网络"]), (suffix, lines)

    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 0
        assert page.locator(f"{selector} a[href='#read-p479-b001']").count() == 1
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=37']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("item => item.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("item => item.open")

    image = page.locator("#read-p479-b002 .book-figure img")
    image.evaluate("item => item.decode()")
    figure = image.evaluate("""item => ({
      naturalWidth: item.naturalWidth, naturalHeight: item.naturalHeight,
      width: item.getBoundingClientRect().width,
      height: item.getBoundingClientRect().height,
      left: item.getBoundingClientRect().left,
      right: item.getBoundingClientRect().right
    })""")
    assert (figure["naturalWidth"], figure["naturalHeight"]) == (847, 930)
    assert abs(figure["width"] / figure["height"] - 847 / 930) < .002
    assert figure["left"] >= -1 and figure["right"] <= width + 1
    assert page.locator("#read-p479-b002 .figure-image-link").get_attribute(
        "href").endswith(FIGURE["src"])
    assert image.get_attribute("alt") == FIGURE["alt"]
    assert page.locator("#read-p479-b002 figcaption").count() == 0
    assert page.locator("#read-p479-b002 .figure-media").evaluate(
        "item => item.scrollWidth <= item.clientWidth + 2")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"top-{suffix}.png"))
    page.screenshot(path=str(QA_DIR / f"full-{suffix}.png"), full_page=True)
    image.screenshot(path=str(QA_DIR / f"figure-{suffix}.png"))

    last = "read-p479-b002"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === 'V' && saved.page === 479 && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    restored = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === 'V' && saved.page === 479 && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        restored.append(page.evaluate("""last => ({
          y: Math.round(scrollY),
          top: Math.round(document.getElementById(last).getBoundingClientRect().top)
        })""", last))
    assert len({item["y"] for item in restored}) == 1, restored
    assert len({item["top"] for item in restored}) == 1, restored
    page.screenshot(path=str(QA_DIR / f"bottom-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed, (suffix, errors, failed)

    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=37']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p478-b009").wait_for()
    assert "chapter=37" in page.url
    next_link = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=V']")
    assert next_link.count() == 1
    next_link.click()
    page.locator("#read-p479-b002").wait_for()
    assert "chapter=V" in page.url
    assert not errors and not failed, (suffix, errors, failed)
    context.close()
    print(json.dumps({"viewport": suffix, "blocks": blocks, "titleLines": lines,
                      "figure": figure, "restored": restored,
                      "errors": errors, "failed": failed}, ensure_ascii=True), flush=True)


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
        print(f"PASS: Part V {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
