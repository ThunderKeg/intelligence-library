"""Independent six-viewport site QA for MacKay chapter 38.

Draft mode inserts one temporary chapter in the browser's books.js response.
Formal mode reads the registered index and JSON without interception.
"""

from argparse import ArgumentParser
from collections import Counter
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
PARSER.add_argument("--sha256", required=True)
PARSER.add_argument("--formal", action="store_true")
PARSER.add_argument("--allow-short", action="store_true",
                    help="exploratory run while reported short tail lines await repair")
PARSER.add_argument("--allow-title-split", action="store_true",
                    help="exploratory run while chapter title wrap awaits repair")
PARSER.add_argument("--trial-list-wrap", choices=("pretty", "balance"),
                    help="temporary browser-only CSS on chapter 38 list items")
PARSER.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
ARGS = PARSER.parse_args()

DRAFT_BYTES = (BOOK / "chapter-38.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
assert SHA == ARGS.sha256.lower(), ("chapter 38 draft changed", SHA)
if ARGS.formal:
    FORMAL_BYTES = (BOOK / "chapter-38.json").read_bytes()
    assert FORMAL_BYTES == DRAFT_BYTES, "formal chapter 38 differs from reviewed draft"
else:
    FORMAL_BYTES = None
CHAPTER = json.loads((FORMAL_BYTES or DRAFT_BYTES).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
LISTS = [block for block in BLOCKS if block["kind"] == "list"]
assert CHAPTER["bookId"] == "mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [480, 482]
assert len(BLOCKS) == 25 and len(CHAPTER["toc"]) == 3
assert Counter(block["kind"] for block in BLOCKS) == {
    "paragraph": 18, "heading": 3, "list": 3, "intro": 1}
assert [block["id"] for block in LISTS] == ["p480-b009", "p481-b001", "p481-b004"]
assert [block["ordered"] for block in LISTS] == [False, True, True]
assert [len(block["items"]) for block in LISTS] == [3, 3, 3]
assert len(LISTS[2]["items"][1]["children"]) == 2
assert not any(block["kind"] in {"figure", "formula", "table", "exercise", "footnote"}
               for block in BLOCKS)
assert BLOCKS[-1]["id"] == "p482-b010"
assert [entry["number"] for entry in CHAPTER["toc"]] == ["38", "38.1", "38.2"]
assert all(any(block["id"] == entry["block"] for block in BLOCKS)
           for entry in CHAPTER["toc"])

if not ARGS.formal:
    BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapter38Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const old38 = chapter38Preview.findIndex(item => item.id === "38");
if (old38 >= 0) chapter38Preview.splice(old38, 1);
const partVIndex = chapter38Preview.findIndex(item => item.id === "V");
if (partVIndex < 0) throw Error("Cannot find registered Part V");
chapter38Preview.splice(partVIndex + 1, 0,
  {id: "38", number: "38", title: "神经网络导论",
   content: "books/mackay-information-theory-2003/chapter-38.draft.json"});
"""
else:
    BOOK_SCRIPT = None

PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch38-formal-qa" if ARGS.formal else "mackay-ch38-draft-qa")
if ARGS.trial_list_wrap:
    QA_DIR = QA_DIR.with_name(QA_DIR.name + "-" + ARGS.trial_list_wrap)
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def normalized(value):
    return re.sub(r"\s+", "", value)


def marks(segments, mark):
    return [item["text"] for item in segments
            if isinstance(item, dict) and item.get(mark)]


def check_item(item, li, width):
    text = li.locator(":scope > span")
    assert text.count() == 1
    if not any(isinstance(seg, dict) and "mathml" in seg
               for seg in item.get("segments", [])):
        assert normalized(text.inner_text()) == normalized(item["text"])
    assert text.locator("em").all_text_contents() == marks(item["segments"], "em")
    assert text.locator("strong").all_text_contents() == marks(item["segments"], "strong")
    child = li.locator(":scope > .book-list")
    children = item.get("children", [])
    assert child.count() == bool(children)
    if children:
        assert child.evaluate("node => node.tagName") == (
            "OL" if item.get("ordered") else "UL")
        assert child.locator(":scope > li").count() == len(children)
        parent_left = li.evaluate("node => node.getBoundingClientRect().left")
        child_left = child.locator(":scope > li").first.evaluate(
            "node => node.getBoundingClientRect().left")
        assert child_left > parent_left + 10, (width, parent_left, child_left)
        for expected, actual in zip(children, child.locator(":scope > li").all()):
            check_item(expected, actual, width)


def check_list(block, page, width, mode):
    node = page.locator(f"#read-{block['id']}")
    list_node = node.locator(":scope > .book-list")
    assert list_node.count() == 1
    assert list_node.evaluate("item => item.tagName") == (
        "OL" if block["ordered"] else "UL")
    items = list_node.locator(":scope > li")
    assert items.count() == len(block["items"])
    assert list_node.evaluate("item => item.getBoundingClientRect().right") <= width + 1
    for expected, actual in zip(block["items"], items.all()):
        check_item(expected, actual, width)
    if (width, mode) in ((1440, "light"), (390, "light"), (320, "dark")):
        topbar = page.locator(".reader-topbar")
        topbar.evaluate("item => item.style.visibility = 'hidden'")
        node.screenshot(path=str(QA_DIR / f"list-{block['id']}-{width}-{mode}.png"))
        topbar.evaluate("item => item.style.visibility = ''")


def short_tail_lines(page):
    return page.locator(
        ".reading-paragraph, .reading-intro, .reading-list .book-list li > span"
    ).evaluate_all("""items => {
      const short = [];
      for (const item of items) {
        const lines = new Map();
        const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
        while (walker.nextNode()) {
          const node = walker.currentNode;
          for (let i = 0; i < node.length; i++) {
            const range = document.createRange();
            range.setStart(node, i); range.setEnd(node, i + 1);
            const rect = range.getBoundingClientRect();
            if (rect.width < .1 || rect.height < .1) continue;
            const top = Math.round(rect.top);
            lines.set(top, (lines.get(top) || '') + node.textContent[i]);
          }
        }
        const values = [...lines.values()].map(v => v.trim()).filter(Boolean);
        if (values.length > 1 && [...values.at(-1)].length <= 2)
          short.push({id: item.id || item.closest('.reading-block')?.id,
            prefix: item.textContent.trim().slice(0, 22), tail: values.at(-1)});
      }
      return short;
    }""")


def inspect_viewport(browser, base, width, mode):
    suffix = f"{width}-{mode}"
    context = browser.new_context(
        viewport={"width": width, "height": 844}, color_scheme=mode,
        service_workers="block", permissions=["clipboard-read", "clipboard-write"])
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=38")
    page.locator("#read-p482-b010").wait_for()
    if ARGS.trial_list_wrap:
        page.add_style_tag(content=(
            '#reader-article[data-book-id="mackay-information-theory-2003"] '
            f'.reading-list .book-list li {{ text-wrap: {ARGS.trial_list_wrap}; }}'))
    assert any(url.endswith("/books.js") for url in requests)
    source = "chapter-38.json" if ARGS.formal else "chapter-38.draft.json"
    assert any(url.endswith(source) for url in requests), requests
    if ARGS.formal:
        assert not any(url.endswith("chapter-38.draft.json") for url in requests)
    assert page.evaluate("document.documentElement.dataset.theme") == mode

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-heading h2").count() == 2
    assert page.locator(".book-figure, .book-formula, .book-exercise, .book-table").count() == 0
    assert page.locator("math merror, .formula-fallback, .figure-error").count() == 0
    assert page.locator(".inline-math math").count() == 2
    copied_math = 0
    for math in page.locator(".inline-math math").all():
        if (width, mode) in ((1440, "light"), (320, "dark")):
            math.select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()")
            page.evaluate("getSelection().removeAllRanges()")
            copied_math += 1
    for block in BLOCKS:
        if block["kind"] == "list":
            check_list(block, page, width, mode)
            continue
        node = page.locator(f"#read-{block['id']}")
        assert node.locator("em").all_text_contents() == marks(
            block.get("segments", []), "em"), block["id"]
        assert node.locator("strong").all_text_contents() == marks(
            block.get("segments", []), "strong"), block["id"]
        if not any(isinstance(seg, dict) and "mathml" in seg
                   for seg in block.get("segments", [])):
            assert normalized(node.inner_text()) == normalized(block["text"]), block["id"]

    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 2
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=V']").count() == 1
        for entry in CHAPTER["toc"]:
            assert page.locator(f"{selector} a[href='#read-{entry['block']}']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("item => item.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("item => item.open")

    title_tail = page.locator(".reading-heading h1").evaluate("""item => {
      const chars = [];
      const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        for (let i = 0; i < node.length; i++) {
          const c = node.textContent[i];
          if (!c.trim()) continue;
          const r = document.createRange();
          r.setStart(node, i); r.setEnd(node, i + 1);
          chars.push({char: c, top: Math.round(r.getBoundingClientRect().top)});
        }
      }
      return chars.slice(-6);
    }""")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"top-{suffix}.png"))
    assert [item["char"] for item in title_tail] == list("神经网络导论")
    if not ARGS.allow_title_split:
        assert len({item["top"] for item in title_tail}) == 1, (suffix, title_tail)
    short_tails = short_tail_lines(page)
    for item in short_tails:
        page.locator(f"#{item['id']}").screenshot(
            path=str(QA_DIR / f"short-{item['id']}-{suffix}.png"))
    if not ARGS.allow_short:
        assert not short_tails, (suffix, short_tails)
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"top-{suffix}.png"))
    if (width, mode) in ((1440, "light"), (390, "light"), (320, "dark")):
        page.screenshot(path=str(QA_DIR / f"full-{suffix}.png"), full_page=True)

    last = "read-p482-b010"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '38' && saved.page === 482 && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    restored = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '38' && saved.page === 482 && saved.block === last &&
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
        "#chapter-navigation .chapter-navigation-link[href$='chapter=V']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p479-b002").wait_for()
    assert "chapter=V" in page.url
    page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=38']").click()
    page.locator("#read-p482-b010").wait_for()
    assert "chapter=38" in page.url
    assert not errors and not failed, (suffix, errors, failed)
    context.close()
    print(json.dumps({"viewport": suffix, "blocks": len(actual), "toc": 3,
                      "lists": [len(block["items"]) for block in LISTS],
                      "nested": len(LISTS[2]["items"][1]["children"]),
                      "inlineMath": 2, "copiedMath": copied_math, "restored": restored,
                      "shortTails": short_tails, "errors": errors, "failed": failed},
                     ensure_ascii=True), flush=True)


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
        label = "EXPLORATORY" if (ARGS.allow_short or ARGS.allow_title_split or
                                   ARGS.trial_list_wrap) else "PASS"
        print(f"{label}: chapter 38 {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
