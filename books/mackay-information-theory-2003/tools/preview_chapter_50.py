"""Independent Edge QA harness for MacKay chapter 50 after its draft freezes.

Draft mode inserts only a temporary browser-side book index entry. Formal mode
loads the registered books.js and formal JSON without interception or injection.
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
PARSER.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
PARSER.add_argument("--scan-tail", action="store_true")
PARSER.add_argument("--strict-tail", action="store_true")
ARGS = PARSER.parse_args()

DRAFT = (BOOK / "chapter-50.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen draft changed", SHA)
FORMAL = (BOOK / "chapter-50.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL == DRAFT, "Formal JSON differs from reviewed draft"
CHAPTER = json.loads((FORMAL if ARGS.formal else DRAFT).decode("utf-8"))


def walk(blocks):
    for block in blocks:
        yield block
        yield from walk(block.get("blocks", []))


BLOCKS = CHAPTER["blocks"]
ALL = list(walk(BLOCKS))
FORMULAS = [block for block in ALL if block["kind"] == "formula"]
FIGURES = [block for block in ALL if block["kind"] in ("figure", "image")]
TABLES = [block for block in ALL if block["kind"] == "table"]
BOXES = [block for block in ALL if block["kind"] == "box"]
EXERCISES = [block for block in ALL if block["kind"] == "exercise"]
HEADINGS = [block for block in ALL if block["kind"] == "heading"]
LAST = BLOCKS[-1]
LAST_READING = ALL[-1]
KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"


def inline_count(value):
    if isinstance(value, list):
        return sum(inline_count(item) for item in value)
    if isinstance(value, dict):
        if "mathml" in value and "kind" not in value:
            return 1
        return sum(inline_count(item) for key, item in value.items()
                   if key != "mathml")
    return 0


assert CHAPTER["bookId"] == "mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [601, 608]
assert len(BLOCKS) == 83 and len(ALL) == 92
assert len(CHAPTER["toc"]) == 8 and len(HEADINGS) == 8
assert len(FORMULAS) == 6 and len(FIGURES) == 4
assert len(EXERCISES) == 12 and len(BOXES) == 3
assert sum(block["kind"] == "list" for block in ALL) == 3
assert sum(block["kind"] == "quote" for block in ALL) == 1
assert BLOCKS[0]["id"] == "p601-b001" and BLOCKS[0]["kind"] == "heading"
assert LAST["pdfPage"] == 608
assert LAST["kind"] == "box" and LAST["id"] == "box-50-conclusion"
assert LAST_READING["id"] == "p608-b007"
assert len({block["id"] for block in ALL}) == len(ALL)
assert all(601 <= block["pdfPage"] <= 608 for block in ALL)
assert [block["number"] for block in FORMULAS if block.get("number")] == [
    f"(50.{index})" for index in range(1, 7)]
assert [block["src"] for block in FIGURES] == [
    f"assets/chapter-50/figure-50-{index}.png" for index in range(1, 5)]
assert len(TABLES) == 0
assert [block["id"] for block in BOXES] == [
    "box-50-encoder", "box-50-decoder", "box-50-conclusion"]
assert [len(block["blocks"]) for block in BOXES] == [2, 6, 1]
assert all(block.get("outlined") for block in BOXES)
assert BOXES[-1].get("shadow") is True
assert [entry["number"] for entry in CHAPTER["toc"][1:]] == [
    f"50.{index}" for index in range(1, 8)]
assert [block["id"] for block in HEADINGS if block["id"] in {
    entry["block"] for entry in CHAPTER["toc"]}] == [
    entry["block"] for entry in CHAPTER["toc"]]
assert len(EXERCISES) == 12
assert all(f"习题 50.{index}" in EXERCISES[index - 2]["label"]
           for index in range(2, 14))
assert [index for index in range(2,14)
        if EXERCISES[index-2]["label"].startswith("▷")] == [2,3,4,9,11,12,13]

BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(
    encoding="utf-8") + """
const ch50Preview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = ch50Preview.findIndex(x => x.id === "50");
if (existing >= 0) ch50Preview.splice(existing, 1);
const afterIntro = ch50Preview.findIndex(x => x.id === "50-intro");
if (afterIntro < 0) throw Error("PDF600 chapter 50 intro must precede chapter 50");
ch50Preview.splice(afterIntro+1, 0,
  {id:"50",number:"50",title:"数字喷泉码",
   content:"books/mackay-information-theory-2003/chapter-50.draft.json"});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch50-formal-qa" if ARGS.formal else "mackay-ch50-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
            pass


def horizontal_scroll(node):
    metric = node.evaluate("node => ({client:node.clientWidth,width:node.scrollWidth})")
    if metric["width"] > metric["client"] + 2:
        node.evaluate("node => node.scrollLeft=node.scrollWidth")
        assert node.evaluate("node => node.scrollLeft") >= (
            metric["width"] - metric["client"] - 2), metric
        node.evaluate("node => node.scrollLeft=0")
    return metric


def text_lines(page, selector=".reading-paragraph p,.figure-caption p,.book-exercise"):
    return page.locator(selector).evaluate_all(
        """items => items.map(item => {
          const lines = new Map();
          const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
          while (walker.nextNode()) {
            const node=walker.currentNode;
            if (node.parentElement?.closest('math')) continue;
            for (let i=0;i<node.length;i++) {
              const range=document.createRange();
              range.setStart(node,i);range.setEnd(node,i+1);
              const rect=range.getBoundingClientRect();
              if (rect.width<.1||rect.height<.1) continue;
              const top=Math.round(rect.top);
              lines.set(top,(lines.get(top)||'')+node.textContent[i]);
            }
          }
          return {id:item.closest('.reading-block')?.id,
            hasMath:!!item.querySelector('math'),
            lines:[...lines.entries()].sort((a,b)=>a[0]-b[0])
              .map(([_,line])=>line.trim()).filter(Boolean)};
        })""")


def bottom_progress(page):
    target = f"read-{LAST_READING['id']}"
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    page.wait_for_function("""({key,target}) => {
      const saved=JSON.parse(localStorage.getItem(key)||'{}');
      return saved.chapter==='50'&&saved.page===608&&saved.block===target&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""", arg={"key": KEY, "target": target})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key,target}) => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='50'&&saved.page===608&&saved.block===target&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""", arg={"key": KEY, "target": target})
        positions.append(page.evaluate("""target => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById(target).getBoundingClientRect().top)
        })""", target))
    assert len({tuple(item.values()) for item in positions}) == 1, positions
    return positions


def inspect(browser, base, width, mode):
    name = f"{width}-{mode}"
    context = browser.new_context(viewport={"width": width, "height": 844},
                                  color_scheme=mode, service_workers="block",
                                  permissions=["clipboard-read", "clipboard-write"])
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=50")
    page.locator(f"#read-{LAST_READING['id']}").wait_for()
    expected_json = "chapter-50.json" if ARGS.formal else "chapter-50.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/" + expected_json) for url in requests)
    if ARGS.formal:
        assert not any(url.endswith("chapter-50.draft.json") for url in requests)

    rendered = page.locator(".reading-block").evaluate_all("""items => items.map(node =>
      [node.id,[...node.classList].find(name =>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    expected = [[f"read-{block['id']}", f"reading-{block['kind']}"]
                for block in ALL if block["kind"] != "box"]
    assert rendered == expected, (name, len(rendered), len(expected))
    assert page.locator(".reading-heading h1").inner_text().replace("\n", "") == BLOCKS[0]["text"]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    assert page.locator("math merror,.formula-fallback,.figure-error").count() == 0
    assert page.locator(".book-formula math").count() == len(FORMULAS)
    assert page.locator(".inline-math math").count() == inline_count(BLOCKS)
    assert page.locator(".book-figure img").count() == len(FIGURES)
    assert page.locator(".book-exercise-label").count() == len(EXERCISES)
    assert page.locator("aside.book-box").count() == len(BOXES)
    assert page.locator(".book-table").count() == 0
    assert page.locator("#read-p607-b002 math msup").count() >= 1
    assert page.locator("#read-p607-b004 math msup").count() >= 1
    assert page.locator("#read-p607-b009 math msup").count() >= 1
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p601-b001']").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 7
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=50-intro']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()
    heading_lines=text_lines(page,".reading-heading h1,.reading-heading h2,.reading-heading h3")
    if width<800:
        for block in HEADINGS:
            page.locator(f"#read-{block['id']}").screenshot(
                path=str(QA_DIR/f"heading-{block['id']}-{name}.png"))

    short_tails = []
    if ARGS.scan_tail:
        short_tails = [item for item in text_lines(page)
                       if not item["hasMath"] and len(item["lines"]) > 1
                       and len(item["lines"][-1]) <= 2]
        for item in short_tails:
            page.locator(f"#{item['id']}").screenshot(
                path=str(QA_DIR / f"short-tail-{item['id']}-{name}.png"))
        if ARGS.strict_tail:
            assert not short_tails, (name, short_tails)
    if (width,mode) in ((1440,"light"),(320,"dark")):
        for block_id in ("p604-b001","p607-b006"):
            page.locator(f"#read-{block_id}").screenshot(
                path=str(QA_DIR/f"paragraph-{block_id}-{name}.png"))

    copied_formulas, formula_overflow = 0, []
    for block in FORMULAS:
        item = page.locator(f"#read-{block['id']}")
        if block.get("number"):
            assert item.locator(".formula-number").inner_text() == block["number"]
        else:
            assert item.locator(".formula-number").count() == 0
        metric = horizontal_scroll(item.locator(".formula-scroll"))
        if metric["width"] > metric["client"] + 2:
            formula_overflow.append(block.get("number") or block["id"])
            assert item.locator(".formula-view-hint").is_visible()
            if width<800:
                scroll=item.locator(".formula-scroll")
                scroll.scroll_into_view_if_needed()
                scroll.evaluate("node=>node.scrollLeft=node.scrollWidth")
                page.screenshot(path=str(QA_DIR/f"formula-viewport-{block['id']}-{name}-right.png"))
                scroll.evaluate("node=>node.scrollLeft=0")
        if (width, mode) in ((1440, "light"), (320, "dark")):
            item.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()").strip()
            page.evaluate("getSelection().removeAllRanges()")
            copied_formulas += 1

    figure_overflow = []
    for block in FIGURES:
        item = page.locator(f"#read-{block['id']}")
        image = item.locator(".book-figure img")
        image.scroll_into_view_if_needed()
        image.evaluate("node=>node.decode()")
        assert image.evaluate("node=>[node.naturalWidth,node.naturalHeight]") == [
            block["width"], block["height"]]
        assert image.get_attribute("alt") == block["alt"]
        assert item.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
        metric = horizontal_scroll(item.locator(".figure-media"))
        if metric["width"] > metric["client"] + 2:
            figure_overflow.append(block["id"])
            assert item.locator(".figure-view-hint").is_visible()
        if (width, mode) in ((1440, "light"), (320, "dark")):
            item.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{name}.png"))
            caption=item.locator(".figure-caption")
            if caption.count():
                caption.screenshot(path=str(QA_DIR/f"caption-{block['id']}-{name}.png"))
        if width < 800 and block.get("wide"):
            assert metric["width"] > metric["client"] + 2
            media=item.locator(".figure-media")
            media.evaluate("node=>node.scrollLeft=node.scrollWidth")
            right=media.evaluate("node=>node.scrollLeft")
            assert right>0
            page.screenshot(path=str(QA_DIR / f"figure-viewport-{block['id']}-{name}-right.png"))
            assert media.evaluate("node=>node.scrollLeft")>=right-2
            media.evaluate("node=>node.scrollLeft=0")

    for block in BOXES:
        item = page.locator(f"#read-{block['id']}")
        assert item.locator(".reading-block").count() == len(block.get("blocks", []))
        assert item.evaluate("node=>node.classList.contains('outlined-box')") == bool(
            block.get("outlined"))
        horizontal_scroll(item)
        if (width, mode) in ((1440, "light"), (320, "dark")):
            item.screenshot(path=str(QA_DIR / f"box-{block['id']}-{name}.png"))
    conclusion=page.locator("#read-box-50-conclusion")
    assert conclusion.evaluate("node=>getComputedStyle(node).boxShadow") != "none"
    assert conclusion.locator(".reading-paragraph p").evaluate(
        "node=>getComputedStyle(node).textAlign") == "center"
    for block in EXERCISES:
        assert block["label"] in page.locator(f"#read-{block['id']}").inner_text()

    inline = page.locator(".inline-math").evaluate_all("""items=>items.map(node=>({
      client:node.clientWidth,width:node.scrollWidth,focusable:node.tabIndex>=0,
      hint:!!node.nextElementSibling?.classList.contains('inline-math-view-hint')&&
        getComputedStyle(node.nextElementSibling).display!=='none'}))""")
    assert all((item["width"] > item["client"] + 2) == item["hint"] for item in inline)
    for index, item in enumerate(inline):
        if item["width"] > item["client"] + 2:
            assert item["focusable"]
            horizontal_scroll(page.locator(".inline-math").nth(index))
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(QA_DIR / f"page-{name}.png"), full_page=True)
    progress = bottom_progress(page)
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=50-intro']").click()
    page.locator("#read-p600-b007").wait_for()
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=50']").click()
    page.locator(f"#read-{LAST_READING['id']}").wait_for()
    assert not errors and not failed, (errors, failed)
    context.close()
    print(json.dumps({"viewport": name, "topBlocks": len(BLOCKS),
                      "recursiveNodes": len(ALL), "renderedBlocks": len(rendered),
                      "toc": len(CHAPTER["toc"]), "formulas": len(FORMULAS),
                      "copiedFormulas": copied_formulas,
                      "formulaOverflow": formula_overflow,
                      "figures": len(FIGURES), "figureOverflow": figure_overflow,
                      "boxes": len(BOXES), "exercises": len(EXERCISES),
                      "inlineMath": len(inline), "headingLines":heading_lines,
                      "inlineMathOverflow":sum(item["width"]>item["client"]+2 for item in inline),
                      "shortTails": short_tails,
                      "progress": progress, "errors": errors, "failed": failed}),
          flush=True)


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
                inspect(browser, f"http://127.0.0.1:{server.server_port}/", width, mode)
            browser.close()
        print(f"PASS: chapter 50 {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, sha256={SHA}, "
              f"screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
