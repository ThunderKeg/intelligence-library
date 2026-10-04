"""Independent Edge QA for MacKay chapter 42, draft and registered paths.

The draft is temporarily inserted after the registered PDF516 postscript only
in the browser's books.js response. Formal mode uses unmodified site files.
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
parser.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
parser.add_argument("--scan-tail", action="store_true")
parser.add_argument("--trial-h2", choices=("pretty","balance","22px","22pretty","focused"),
                    help="temporary browser-only heading comparison")
parser.add_argument("--trial-short-pretty", action="store_true",
                    help="temporary browser-only short-tail comparison")
parser.add_argument("--trial-subheads-balance", action="store_true",
                    help="temporary browser-only italic/bold subheading comparison")
args = parser.parse_args()
draft = (BOOK / "chapter-42.draft.json").read_bytes()
sha = hashlib.sha256(draft).hexdigest()
assert sha == args.sha256.lower(), ("Frozen draft changed", sha)
formal = (BOOK / "chapter-42.json").read_bytes() if args.formal else None
if args.formal:
    assert formal == draft, "Registered JSON differs from reviewed draft"
chapter = json.loads((formal if args.formal else draft).decode("utf-8"))
blocks = chapter["blocks"]
formulas = [block for block in blocks if block["kind"] == "formula"]
figures = [block for block in blocks if block["kind"] in ("figure", "image")]
boxes = [block for block in blocks if block["kind"] == "box"]
exercises = [block for block in blocks if block["kind"] == "exercise"]
last = blocks[-1]
progress_key = "intelligence-library:progress:v2:mackay-information-theory-2003"


def inline_count(value):
    if isinstance(value, list):
        return sum(inline_count(item) for item in value)
    if isinstance(value, dict):
        if "mathml" in value and "kind" not in value:
            return 1
        return sum(inline_count(item) for key, item in value.items() if key != "mathml")
    return 0


assert chapter["bookId"] == "mackay-information-theory-2003"
assert chapter["sourcePdfPages"] == [517, 533]
assert len(blocks) == 207
assert len(chapter["toc"]) == 12  # chapter + sections 42.1–42.11
assert Counter(block["kind"] for block in blocks) == Counter({
    "paragraph":126,"formula":35,"figure":18,"heading":12,
    "exercise":12,"list":2,"intro":1,"box":1})
assert blocks[0]["id"] == "p517-b001" and blocks[0]["kind"] == "heading"
assert blocks[0]["text"] == "第 42 章　Hopfield 网络"
assert last["id"] == "p533-b005" and last["pdfPage"] == 533
assert [block["number"] for block in formulas] == [
    f"(42.{number})" for number in range(1, 36)]
assert len(boxes) == 1 and boxes[0]["outlined"] and boxes[0]["algorithm"]
assert len(boxes[0]["blocks"]) == 1 and boxes[0]["blocks"][0]["kind"] == "code"
assert boxes[0]["pdfPage"] == 528
assert [block["label"].split("习题 ")[-1].split("。")[0] for block in exercises] == [
    f"42.{number}" for number in range(1, 13)]
assert len({block["id"] for block in blocks}) == len(blocks)
assert all(517 <= block["pdfPage"] <= 533 for block in blocks)
assert [block["src"] for block in figures] == [
    f"assets/chapter-42/figure-42-{stem}.png" for stem in (
        "1","2","3a","3b","3c","3d","4a","4b-f","5","6","7","8",
        "10","11a","11b","12","13","14")]

if args.formal:
    book_script = None
else:
    book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const ch42Preview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = ch42Preview.findIndex(x => x.id === "42");
if (existing >= 0) ch42Preview.splice(existing, 1);
const afterPostscript = ch42Preview.findIndex(x => x.id === "41-postscript");
if (afterPostscript < 0) throw Error("The PDF516 postscript must precede chapter 42");
ch42Preview.splice(afterPostscript + 1, 0,
  {id:"42", number:"42", title:"Hopfield 网络",
   content:"books/mackay-information-theory-2003/chapter-42.draft.json"});
"""

screenshots = Path(tempfile.gettempdir()) / (
    "mackay-ch42-formal-qa" if args.formal else "mackay-ch42-draft-qa")
screenshots.mkdir(exist_ok=True)
viewports = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def horizontal_scroll(node):
    metric = node.evaluate("node => ({client:node.clientWidth, width:node.scrollWidth})")
    if metric["width"] > metric["client"] + 2:
        node.evaluate("node => node.scrollLeft = node.scrollWidth")
        assert node.evaluate("node => node.scrollLeft") >= (
            metric["width"] - metric["client"] - 2), metric
        node.evaluate("node => node.scrollLeft = 0")
    return metric


def text_lines(page, selector):
    return page.locator(selector).evaluate_all("""items => items.map(item => {
      const lines = new Map();
      const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        for (let i = 0; i < node.length; i++) {
          const range = document.createRange();
          range.setStart(node,i); range.setEnd(node,i+1);
          const rect = range.getBoundingClientRect();
          if (rect.width < .1 || rect.height < .1) continue;
          const top = Math.round(rect.top);
          lines.set(top, (lines.get(top)||'') + node.textContent[i]);
        }
      }
      return {id:item.closest('.reading-block')?.id,
        lines:[...lines.entries()].sort((a,b)=>a[0]-b[0])
          .map(([_,line])=>line.trim()).filter(Boolean)};
    })""")


def bottom_progress(page):
    target = f"read-{last['id']}"
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    page.wait_for_function("""({key,target}) => {
      const saved = JSON.parse(localStorage.getItem(key)||'{}');
      return saved.chapter==='42' && saved.page===533 && saved.block===target &&
        document.querySelector('#reading-progress').style.width==='100%';
    }""", arg={"key": progress_key, "target": target})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key,target}) => {
          const saved = JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='42' && saved.page===533 && saved.block===target &&
            document.querySelector('#reading-progress').style.width==='100%';
        }""", arg={"key": progress_key, "target": target})
        positions.append(page.evaluate("""target => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById(target).getBoundingClientRect().top)
        })""", target))
    assert len({tuple(position.values()) for position in positions}) == 1, positions
    return positions


def inspect(browser, base, width, mode):
    name = (f"{width}-{mode}" + (f"-h2-{args.trial_h2}" if args.trial_h2 else "") +
            ("-short-pretty" if args.trial_short_pretty else ""))
    if args.trial_subheads_balance:
        name += "-subheads-balance"
    context = browser.new_context(
        viewport={"width":width,"height":844}, color_scheme=mode,
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=42")
    page.locator(f"#read-{last['id']}").wait_for()
    if args.trial_h2 == "pretty":
        page.add_style_tag(content="#reader-article .reading-heading h2 { text-wrap:pretty; }")
    elif args.trial_h2 == "balance":
        page.add_style_tag(content="#reader-article .reading-heading h2 { text-wrap:balance; }")
    elif args.trial_h2 == "22px":
        page.add_style_tag(content="#reader-article .reading-heading h2 { font-size:22px; }")
    elif args.trial_h2 == "22pretty":
        page.add_style_tag(content="#reader-article .reading-heading h2 { font-size:22px; text-wrap:pretty; }")
    elif args.trial_h2 == "focused" and width <= 360:
        page.add_style_tag(content="""
          #read-p518-b003 h2 { text-wrap:balance; }
          #read-p522-b001 h2, #read-p527-b013 h2 { text-wrap:pretty; }
        """)
    if args.trial_short_pretty:
        ids = ("p517-b003","p518-b009","p519-b016","p520-b019","p530-b005",
               "p531-b002","p517-b005","p522-b010","p525-b003","p529-b004",
               "p532-b006","p527-b014","p533-b004")
        page.add_style_tag(content=",".join(f"#read-{item} p" for item in ids) +
                           " { text-wrap:pretty; }")
    if args.trial_subheads_balance:
        page.add_style_tag(content="""
          #read-p518-b009 p, #read-p525-b003 p { text-wrap:balance; }
        """)
    expected_json = "chapter-42.json" if args.formal else "chapter-42.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/" + expected_json) for url in requests)
    if args.formal:
        assert not any(url.endswith("chapter-42.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(node =>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    expected = []
    for block in blocks:
        children = block["blocks"] if block["kind"] == "box" else [block]
        expected.extend((f"read-{child['id']}", f"reading-{child['kind']}")
                        for child in children)
    assert actual == [list(item) for item in expected]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current[href='#read-p517-b001']").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 11
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=41-postscript']").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()

    heading_lines = text_lines(page, ".reading-heading h1, .reading-heading h2")
    if width < 800 and mode == "dark":
        for block_id in ("p518-b003","p522-b001","p527-b013"):
            page.locator(f"#read-{block_id}").screenshot(
                path=str(screenshots / f"heading-{block_id}-{name}.png"))
    short_tails = []
    if args.scan_tail:
        for item in text_lines(page,
                ".reading-paragraph p:not(:has(math)), "
                ".figure-caption p:not(:has(math)), "
                ".book-exercise:not(:has(math))"):
            if len(item["lines"]) > 1 and len(item["lines"][-1]) <= 2:
                short_tails.append({"id":item["id"], "tail":item["lines"][-1]})
        for item in short_tails:
            if item["id"]:
                page.locator(f"#{item['id']}").screenshot(
                    path=str(screenshots / f"short-tail-{item['id']}-{name}.png"))
    if args.trial_subheads_balance:
        for block_id in ("p518-b009","p525-b003"):
            page.locator(f"#read-{block_id}").screenshot(
                path=str(screenshots / f"subheading-{block_id}-{name}.png"))

    assert page.locator(".book-formula math").count() == len(formulas)
    assert page.locator(".book-figure img").count() == len(figures)
    assert page.locator(".book-exercise-label").count() == len(exercises)
    assert page.locator(".inline-math math").count() == inline_count(blocks)
    assert page.locator("math merror, .formula-fallback, .figure-error").count() == 0
    inline_metrics = page.locator(".inline-math").evaluate_all("""items => items.map(node => ({
      id:node.closest('.reading-block')?.id,
      client:node.clientWidth, width:node.scrollWidth,
      focusable:node.tabIndex>=0,
      hint:!!node.nextElementSibling?.classList.contains('inline-math-view-hint') &&
        getComputedStyle(node.nextElementSibling).display!=='none'
    }))""")
    for index, metric in enumerate(inline_metrics):
        overflow = metric["width"] > metric["client"] + 2
        assert metric["hint"] == overflow, metric
        if overflow:
            assert metric["focusable"], metric
            horizontal_scroll(page.locator(".inline-math").nth(index))
    formula_overflow, copied = [], 0
    for block in formulas:
        item = page.locator(f"#read-{block['id']}")
        assert item.locator(".formula-number").inner_text() == block["number"]
        assert item.locator("math").count() == 1
        assert item.locator(".book-formula").evaluate("""node =>
          node.querySelector('.formula-number').getBoundingClientRect().left >=
          node.querySelector('.formula-scroll').getBoundingClientRect().right-1""")
        metric = horizontal_scroll(item.locator(".formula-scroll"))
        if metric["width"] > metric["client"] + 2:
            formula_overflow.append(block["number"])
            assert item.locator(".formula-view-hint").is_visible()
        if (width, mode) in ((1440,"light"),(320,"dark")):
            item.locator("math").scroll_into_view_if_needed()
            item.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()").strip()
            page.evaluate("getSelection().removeAllRanges()")
            copied += 1
    for block in exercises:
        assert block["label"] in page.locator(f"#read-{block['id']}").inner_text()

    figure_overflow = []
    for block in figures:
        item = page.locator(f"#read-{block['id']}")
        image = item.locator(".book-figure img")
        image.scroll_into_view_if_needed()
        image.evaluate("node=>node.decode()")
        assert image.evaluate("node=>[node.naturalWidth,node.naturalHeight]") == [
            block["width"],block["height"]]
        assert image.get_attribute("alt") == block["alt"]
        assert item.locator(".figure-caption").count() == bool(block.get("caption"))
        assert item.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
        metric = horizontal_scroll(item.locator(".figure-media"))
        if width < 800 and block.get("wide"):
            assert metric["width"] > metric["client"] + 2, (block["id"],metric)
            assert item.locator(".figure-view-hint").is_visible()
        if metric["width"] > metric["client"] + 2:
            figure_overflow.append(block["id"])
        if (width, mode) in ((1440,"light"),(320,"dark")):
            item.screenshot(path=str(screenshots / f"figure-{block['id']}-{name}.png"))
        if width < 800 and block.get("wide") and (
                "42-3" in block["src"] or "42-4" in block["src"] or
                "42-11" in block["src"]):
            media = item.locator(".figure-media")
            media.evaluate("node=>node.scrollLeft=node.scrollWidth")
            item.screenshot(path=str(screenshots / f"figure-{block['id']}-{name}-right.png"))
            media.evaluate("node=>node.scrollLeft=0")

    code_copied = 0
    for block in boxes:
        item = page.locator(f"#read-{block['id']}")
        assert "outlined-box" in item.get_attribute("class")
        assert "algorithm-box" in item.get_attribute("class")
        code = item.locator(".book-code code")
        assert code.count() == 1
        assert code.text_content() == block["blocks"][0]["text"]
        metric = horizontal_scroll(item.locator(".book-code"))
        if width < 800:
            assert metric["width"] > metric["client"] + 2
            assert item.locator(".code-view-hint").is_visible()
        if (width, mode) in ((1440,"light"),(320,"dark")):
            code.select_text()
            page.keyboard.press("Control+C")
            assert (page.evaluate("navigator.clipboard.readText()")
                    .replace("\r\n","\n").strip() == code.text_content().strip())
            page.evaluate("getSelection().removeAllRanges()")
            code_copied += 1
            item.screenshot(path=str(screenshots / f"algorithm-{name}.png"))
        if (width, mode) == (320,"dark"):
            item.locator(".book-code").evaluate("node=>node.scrollLeft=node.scrollWidth")
            item.screenshot(path=str(screenshots / f"algorithm-{name}-right.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(screenshots / f"top-{name}.png"))
    progress = bottom_progress(page)
    if (width, mode) in ((1440,"light"),(320,"dark")):
        page.screenshot(path=str(screenshots / f"bottom-{name}.png"))
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41-postscript']").click()
    page.locator("#read-p516-b005").wait_for()
    assert "chapter=41-postscript" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=42']").click()
    page.locator(f"#read-{last['id']}").wait_for()
    assert not errors and not failed, (errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(blocks),"toc":len(chapter["toc"]),
                      "kinds":dict(Counter(block["kind"] for block in blocks)),
                      "formulas":len(formulas),"formulaCopied":copied,
                      "formulaOverflow":formula_overflow,"figures":len(figures),
                      "figureOverflow":figure_overflow,"exercises":len(exercises),
                      "inlineMath":inline_count(blocks),"codeCopied":code_copied,
                      "inlineOverflow":[metric["id"] for metric in inline_metrics
                                        if metric["width"] > metric["client"] + 2],
                      "headingLines":heading_lines,"shortTails":short_tails,
                      "progress":progress,"errors":errors,"failed":failed}),flush=True)


def main():
    server = ThreadingHTTPServer(("127.0.0.1",0),
                                 partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            for width, mode in viewports:
                if args.only and f"{width}-{mode}" != args.only:
                    continue
                inspect(browser,f"http://127.0.0.1:{server.server_port}/",width,mode)
            browser.close()
        print(f"PASS: chapter 42 {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, sha256={sha}, "
              f"screenshots={screenshots}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
