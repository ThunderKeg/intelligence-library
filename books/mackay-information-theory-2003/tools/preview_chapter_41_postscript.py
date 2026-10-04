"""Independent six-viewport Edge QA for MacKay PDF516 postscript."""

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
parser.add_argument("--sha256", required=True)
parser.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
args = parser.parse_args()
draft = (BOOK / "chapter-41-postscript.draft.json").read_bytes()
sha = hashlib.sha256(draft).hexdigest()
assert sha == args.sha256.lower(), ("Frozen draft changed", sha)
formal = (BOOK / "chapter-41-postscript.json").read_bytes() if args.formal else None
if args.formal:
    assert formal == draft, "Registered JSON differs from reviewed draft"
chapter = json.loads((formal if args.formal else draft).decode("utf-8"))
blocks = chapter["blocks"]
progress_key = "intelligence-library:progress:v2:mackay-information-theory-2003"
assert chapter["bookId"] == "mackay-information-theory-2003"
assert chapter["sourcePdfPages"] == [516, 516]
assert len(chapter["toc"]) == 1 and chapter["toc"][0]["block"] == "p516-b001"
assert [block["id"] for block in blocks] == [f"p516-b{number:03d}" for number in range(1, 6)]
assert [block["kind"] for block in blocks] == [
    "heading", "paragraph", "quote", "paragraph", "quote"]
assert blocks[0]["text"] == "有监督神经网络附记"
assert all(block["pdfPage"] == 516 for block in blocks)

if args.formal:
    book_script = None
else:
    book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const postscriptPreview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
for (const id of ["41", "41-postscript"]) {
  const at = postscriptPreview.findIndex(x => x.id === id);
  if (at >= 0) postscriptPreview.splice(at, 1);
}
const after40 = postscriptPreview.findIndex(x => x.id === "40");
if (after40 < 0) throw Error("Chapter 40 must precede chapter 41");
postscriptPreview.splice(after40 + 1, 0,
  {id:"41", number:"41", title:"将学习视为推断",
   content:"books/mackay-information-theory-2003/chapter-41.draft.json"},
  {id:"41-postscript", number:"附记", title:"有监督神经网络附记",
   content:"books/mackay-information-theory-2003/chapter-41-postscript.draft.json"});
"""

screenshots = Path(tempfile.gettempdir()) / (
    "mackay-ch41-postscript-formal-qa" if args.formal
    else "mackay-ch41-postscript-draft-qa")
screenshots.mkdir(exist_ok=True)
viewports = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect(browser, base, width, mode):
    name = f"{width}-{mode}"
    context = browser.new_context(
        viewport={"width": width, "height": 844}, color_scheme=mode,
        service_workers="block")
    if not args.formal:
        context.route("**/books.js", lambda route: route.fulfill(
            body=book_script, content_type="application/javascript"))
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=41-postscript")
    page.locator("#read-p516-b005").wait_for()
    expected_json = ("chapter-41-postscript.json" if args.formal
                     else "chapter-41-postscript.draft.json")
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/" + expected_json) for url in requests)
    if args.formal:
        assert not any(url.endswith("chapter-41-postscript.draft.json")
                       for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      node => [node.id, [...node.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in blocks]
    assert page.locator(".reading-heading h1").inner_text() == blocks[0]["text"]
    assert page.locator(".reading-paragraph").count() == 2
    assert page.locator(".book-quote").count() == 2
    assert [text.strip() for text in page.locator(".book-quote p").all_text_contents()] == [
        blocks[2]["text"], blocks[4]["text"]]
    assert page.locator(".book-figure, .book-formula, .book-table, .book-code, "
                        ".book-exercise, .inline-math").count() == 0
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current[href='#read-p516-b001']").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 0
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=41']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node => node.open")
        page.locator("#toc-close").click()

    quote_metrics = page.locator(".book-quote").evaluate_all("""items => items.map(
      node => ({client: node.clientWidth, width: node.scrollWidth,
        padding: parseFloat(getComputedStyle(node).paddingLeft),
        border: parseFloat(getComputedStyle(node).borderLeftWidth),
        textLeft: node.querySelector('p').getBoundingClientRect().left,
        left: node.getBoundingClientRect().left,
        color: getComputedStyle(node.querySelector('p')).color,
        background: getComputedStyle(document.documentElement).backgroundColor}))""")
    assert all(item["width"] <= item["client"] + 2 and
               item["padding"] >= 16 and item["border"] >= 2 and
               item["textLeft"] - item["left"] >= 18
               for item in quote_metrics), quote_metrics
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(screenshots / f"postscript-{name}.png"), full_page=True)

    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""key => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '41-postscript' && saved.page === 516 &&
        saved.block === 'read-p516-b005' &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg=progress_key)
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '41-postscript' && saved.page === 516 &&
            saved.block === 'read-p516-b005' &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg=progress_key)
        positions.append(page.evaluate("""() => ({
          y: Math.round(scrollY),
          top: Math.round(document.getElementById('read-p516-b005').getBoundingClientRect().top)
        })"""))
    assert len({tuple(position.values()) for position in positions}) == 1, positions
    assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41']").count() == 1
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41']").click()
    page.locator("#read-p515-b004").wait_for()
    assert "chapter=41" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41-postscript']").click()
    page.locator("#read-p516-b005").wait_for()
    assert not errors and not failed, (errors, failed)
    context.close()
    print(json.dumps({"viewport": name, "blocks": len(actual), "quotes": quote_metrics,
                      "progress": positions, "errors": errors, "failed": failed}), flush=True)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0),
                                 partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            for width, mode in viewports:
                if args.only and f"{width}-{mode}" != args.only:
                    continue
                inspect(browser, f"http://127.0.0.1:{server.server_port}/", width, mode)
            browser.close()
        print(f"PASS: chapter 41 postscript {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, sha256={sha}, "
              f"screenshots={screenshots}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
