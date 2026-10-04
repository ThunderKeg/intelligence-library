"""Independent six-viewport Edge QA for MacKay chapter 41.

Draft mode temporarily adds chapters 41 and its postscript to the browser's
books.js response. Formal mode loads the original index and registered JSON.
"""

from argparse import ArgumentParser
from collections import Counter
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
parser.add_argument("--trial-h2", choices=("balance", "22px", "all-22px", "all-20px", "all-balance", "all-pretty", "all-22-pretty"),
                    help="temporary browser-only PDF504 heading comparison")
parser.add_argument("--scan-tail", action="store_true",
                    help="report very short final text lines for visual follow-up")
parser.add_argument("--trial-short-pretty", action="store_true",
                    help="temporary browser-only short-tail comparison")
parser.add_argument("--trial-subheading-16", action="store_true",
                    help="temporary browser-only italic subheading comparison")
parser.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
args = parser.parse_args()
draft = (BOOK / "chapter-41.draft.json").read_bytes()
sha = hashlib.sha256(draft).hexdigest()
assert sha == args.sha256.lower(), ("Frozen draft changed", sha)
formal = (BOOK / "chapter-41.json").read_bytes() if args.formal else None
if args.formal:
    assert formal == draft, "Registered JSON differs from reviewed draft"
chapter = json.loads((formal if args.formal else draft).decode("utf-8"))
blocks = chapter["blocks"]
formulas = [block for block in blocks if block["kind"] == "formula"]
figures = [block for block in blocks if block["kind"] == "figure"]
boxes = [block for block in blocks if block["kind"] == "box"]
exercises = [block for block in blocks if block["kind"] == "exercise"]
last = blocks[-1]
progress_key = "intelligence-library:progress:v2:mackay-information-theory-2003"
assert chapter["bookId"] == "mackay-information-theory-2003"
assert chapter["sourcePdfPages"] == [504, 515]
assert len(blocks) == 124 and len(chapter["toc"]) == 6
assert Counter(block["kind"] for block in blocks) == Counter({
    "paragraph": 73, "formula": 30, "figure": 9, "heading": 6,
    "exercise": 3, "box": 2, "intro": 1})
assert [block["number"] for block in formulas] == [
    f"(41.{number})" for number in range(1, 31)]
assert [block["src"] for block in figures] == [
    f"assets/chapter-41/figure-41-{number}.png"
    for number in (1, 2, 3, 5, 6, 7, 9, 10, 11)]
assert [block["id"] for block in boxes] == [
    "box-41-algorithm-41-4", "box-41-algorithm-41-8"]
assert all(block["outlined"] and block["algorithm"] and
           len(block["blocks"]) == 1 and block["blocks"][0]["kind"] == "code"
           for block in boxes)
assert [block["label"] for block in exercises] == [
    "习题 41.1", "▷ 习题 41.2", "▷ 习题 41.3"]
assert blocks[0]["id"] == "p504-b001" and last["id"] == "p515-b004"
assert last["pdfPage"] == 515
assert all(block["wide"] for block in figures)

if args.formal:
    book_script = None
else:
    book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const ch41Preview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
for (const id of ["41", "41-postscript"]) {
  const at = ch41Preview.findIndex(x => x.id === id);
  if (at >= 0) ch41Preview.splice(at, 1);
}
const after40 = ch41Preview.findIndex(x => x.id === "40");
if (after40 < 0) throw Error("Chapter 40 must precede chapter 41");
ch41Preview.splice(after40 + 1, 0,
  {id:"41", number:"41", title:"将学习视为推断",
   content:"books/mackay-information-theory-2003/chapter-41.draft.json"},
  {id:"41-postscript", number:"附记", title:"有监督神经网络附记",
   content:"books/mackay-information-theory-2003/chapter-41-postscript.draft.json"});
"""

screenshots = Path(tempfile.gettempdir()) / (
    "mackay-ch41-formal-qa" if args.formal else "mackay-ch41-draft-qa")
screenshots.mkdir(exist_ok=True)
viewports = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def horizontal_scroll(node):
    size = node.evaluate("item => ({client: item.clientWidth, width: item.scrollWidth})")
    if size["width"] > size["client"] + 2:
        node.evaluate("item => item.scrollLeft = item.scrollWidth")
        assert node.evaluate("item => item.scrollLeft") >= (
            size["width"] - size["client"] - 2), size
        node.evaluate("item => item.scrollLeft = 0")
    return size


def progress_at_bottom(page):
    last_id = f"read-{last['id']}"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '41' && saved.page === 515 &&
        saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": progress_key, "last": last_id})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '41' && saved.page === 515 &&
            saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": progress_key, "last": last_id})
        positions.append(page.evaluate("""last => ({
          y: Math.round(scrollY),
          top: Math.round(document.getElementById(last).getBoundingClientRect().top)
        })""", last_id))
    assert len({tuple(position.values()) for position in positions}) == 1, positions
    return positions


def inspect(browser, base, width, mode):
    name = (f"{width}-{mode}" +
            (f"-h2-{args.trial_h2}" if args.trial_h2 else "") +
            ("-short-pretty" if args.trial_short_pretty else "") +
            ("-subheading-16" if args.trial_subheading_16 else ""))
    context = browser.new_context(
        viewport={"width": width, "height": 844}, color_scheme=mode,
        service_workers="block", permissions=["clipboard-read", "clipboard-write"])
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=41")
    page.locator(f"#read-{last['id']}").wait_for()
    if args.trial_h2 == "balance":
        page.add_style_tag(content="#read-p504-b003 h2 { text-wrap: balance; }")
    elif args.trial_h2 == "22px":
        page.add_style_tag(content="#read-p504-b003 h2 { font-size: 22px; }")
    elif args.trial_h2 == "all-22px":
        page.add_style_tag(content="#reader-article .reading-heading h2 { font-size: 22px; }")
    elif args.trial_h2 == "all-20px":
        page.add_style_tag(content="#reader-article .reading-heading h2 { font-size: 20px; }")
    elif args.trial_h2 == "all-balance":
        page.add_style_tag(content="#reader-article .reading-heading h2 { text-wrap: balance; }")
    elif args.trial_h2 == "all-pretty":
        page.add_style_tag(content="#reader-article .reading-heading h2 { text-wrap: pretty; }")
    elif args.trial_h2 == "all-22-pretty":
        page.add_style_tag(content="#reader-article .reading-heading h2 { font-size: 22px; text-wrap: pretty; }")
    if args.trial_short_pretty:
        page.add_style_tag(content="""
          #read-p504-b010 p, #read-p512-b004 p,
          #read-p512-b008 p, #read-p513-b006 p { text-wrap: pretty; }
        """)
    if args.trial_subheading_16:
        page.add_style_tag(content="#read-p512-b008 p { font-size:16px; }")
    expected_json = "chapter-41.json" if args.formal else "chapter-41.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/" + expected_json) for url in requests)
    if args.formal:
        assert not any(url.endswith("chapter-41.draft.json") for url in requests)

    rendered = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    expected = []
    for block in blocks:
        children = block["blocks"] if block["kind"] == "box" else [block]
        expected.extend((f"read-{child['id']}", f"reading-{child['kind']}")
                        for child in children)
    assert rendered == [list(item) for item in expected]
    assert page.locator(".reading-heading h1").inner_text() == blocks[0]["text"]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current[href='#read-p504-b001']").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 5
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=40']").count() == 1
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=41-postscript']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node => node.open")
        page.locator("#toc-close").click()

    heading_lines = page.locator(".reading-heading h1, .reading-heading h2").evaluate_all("""items =>
      items.map(item => {
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
        return {id: item.closest('.reading-block').id,
          lines: [...lines.values()].map(line => line.trim()).filter(Boolean)};
      })""")

    assert page.locator(".book-formula math").count() == 30
    assert page.locator(".book-figure img").count() == 9
    assert page.locator(".book-exercise-label").count() == 3
    assert page.locator("math merror, .formula-fallback, .figure-error").count() == 0
    formula_overflow, copied = [], 0
    for block in formulas:
        item = page.locator(f"#read-{block['id']}")
        assert item.locator(".formula-number").inner_text() == block["number"]
        assert item.locator("math").count() == 1
        assert item.locator(".book-formula").evaluate("""node =>
          node.querySelector('.formula-number').getBoundingClientRect().left >=
          node.querySelector('.formula-scroll').getBoundingClientRect().right - 1""")
        size = horizontal_scroll(item.locator(".formula-scroll"))
        if size["width"] > size["client"] + 2:
            formula_overflow.append(block["number"])
            assert item.locator(".formula-view-hint").is_visible()
        if (width, mode) in ((1440, "light"), (320, "dark")):
            item.locator("math").scroll_into_view_if_needed()
            item.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()").strip()
            page.evaluate("getSelection().removeAllRanges()")
            copied += 1
    for block in exercises:
        assert block["label"] in page.locator(f"#read-{block['id']}").inner_text()

    figure_overflow = []
    topbar = page.locator(".reader-topbar")
    topbar.evaluate("node => node.style.visibility = 'hidden'")
    for block in figures:
        item = page.locator(f"#read-{block['id']}")
        image = item.locator(".book-figure img")
        image.scroll_into_view_if_needed()
        image.evaluate("node => node.decode()")
        assert image.evaluate("node => [node.naturalWidth, node.naturalHeight]") == [
            block["width"], block["height"]]
        assert image.get_attribute("alt") == block["alt"]
        assert item.locator(".figure-caption").count() == 1
        assert item.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
        media = item.locator(".figure-media")
        size = horizontal_scroll(media)
        if width < 800:
            assert size["width"] > size["client"] + 2, (block["id"], size)
            assert item.locator(".figure-view-hint").is_visible()
        if size["width"] > size["client"] + 2:
            figure_overflow.append(block["id"])
        if (width, mode) in ((1440, "light"), (320, "dark")):
            item.screenshot(path=str(screenshots / f"figure-{block['id']}-{name}.png"))
        if block["id"] == "p511-b001" and width < 800:
            # All six rows and the rightmost of five panels remain reachable.
            assert image.evaluate("node => node.naturalHeight") == 1615
            media.evaluate("node => node.scrollLeft = node.scrollWidth")
            item.screenshot(path=str(screenshots / f"figure-41-6-right-{name}.png"))
            media.evaluate("node => node.scrollLeft = 0")
    box_overflow, code_copied = [], 0
    for block in boxes:
        item = page.locator(f"#read-{block['id']}")
        assert "outlined-box" in item.get_attribute("class")
        assert "algorithm-box" in item.get_attribute("class")
        code = item.locator(".book-code code")
        assert code.count() == 1
        assert code.text_content() == block["blocks"][0]["text"]
        size = horizontal_scroll(item.locator(".book-code"))
        if width < 800:
            assert size["width"] > size["client"] + 2, (block["id"], size)
            assert item.locator(".algorithm-view-hint").is_visible()
            assert item.locator(".code-view-hint").is_visible()
        if size["width"] > size["client"] + 2:
            box_overflow.append(block["id"])
        if (width, mode) in ((1440, "light"), (320, "dark")):
            code.select_text()
            page.keyboard.press("Control+C")
            copied_code = page.evaluate("navigator.clipboard.readText()").replace("\r\n", "\n").strip()
            expected_code = code.text_content().replace("\r\n", "\n").strip()
            assert copied_code == expected_code, (
                block["id"], repr(copied_code[:100]), repr(expected_code[:100]),
                len(copied_code), len(expected_code))
            page.evaluate("getSelection().removeAllRanges()")
            code_copied += 1
            item.screenshot(path=str(screenshots / f"algorithm-{block['id']}-{name}.png"))
        if (width, mode) == (320, "dark"):
            scroller = item.locator(".book-code")
            scroller.evaluate("node => node.scrollLeft = node.scrollWidth")
            item.screenshot(path=str(screenshots / f"algorithm-{block['id']}-{name}-right.png"))
            scroller.evaluate("node => node.scrollLeft = 0")
    topbar.evaluate("node => node.style.visibility = ''")

    inline = page.locator(".inline-math").evaluate_all("""items => items.map(
      node => ({client: node.clientWidth, width: node.scrollWidth,
        hint: !!node.nextElementSibling?.classList.contains('inline-math-view-hint') &&
          getComputedStyle(node.nextElementSibling).display !== 'none'}))""")
    assert len(inline) == 222, len(inline)
    assert all((item["width"] > item["client"] + 2) == item["hint"]
               for item in inline), inline
    short_tails = []
    if args.scan_tail:
        short_tails = page.locator(
            ".reading-paragraph p, .reading-intro p, .figure-caption p, .book-exercise"
        ).evaluate_all("""items => {
          const found = [];
          for (const item of items) {
            if (item.querySelector('math')) continue;
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
            const values = [...lines.entries()].sort((a,b) => a[0]-b[0])
              .map(([_,x]) => x.trim()).filter(Boolean);
            if (values.length > 1 && [...values.at(-1)].length <= 2)
              found.push({id:item.closest('.reading-block')?.id,
                prefix:item.textContent.trim().slice(0,30), tail:values.at(-1)});
          }
          return found;
        }""")
        for tail in short_tails:
            if tail["id"]:
                page.locator(f"#{tail['id']}").screenshot(
                    path=str(screenshots / f"short-tail-{tail['id']}-{name}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(screenshots / f"top-{name}.png"))
    positions = progress_at_bottom(page)
    if (width, mode) in ((1440, "light"), (320, "dark")):
        page.screenshot(path=str(screenshots / f"bottom-{name}.png"))

    assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=40']").count() == 1
    assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41-postscript']").count() == 1
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=40']").click()
    page.locator("#read-p503-b004").wait_for()
    assert "chapter=40" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41']").click()
    page.locator(f"#read-{last['id']}").wait_for()
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41-postscript']").click()
    page.locator("#read-p516-b005").wait_for()
    assert "chapter=41-postscript" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41']").click()
    page.locator(f"#read-{last['id']}").wait_for()
    assert not errors and not failed, (errors, failed)
    context.close()
    print(json.dumps({"viewport": name, "blocks": len(blocks), "formulas": len(formulas),
                      "formulaCopied": copied, "formulaOverflow": formula_overflow,
                      "figures": len(figures), "figureOverflow": figure_overflow,
                      "boxes": len(boxes), "boxOverflow": box_overflow,
                      "codeCopied": code_copied, "inlineMath": len(inline),
                      "headingLines": heading_lines,
                      "shortTails": short_tails,
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
        print(f"PASS: chapter 41 {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, sha256={sha}, "
              f"screenshots={screenshots}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
