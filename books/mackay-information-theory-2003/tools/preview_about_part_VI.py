"""Inspect PDF568 About Part VI in six Edge viewports, draft or formal."""

from argparse import ArgumentParser
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
parser = ArgumentParser()
parser.add_argument("--formal", action="store_true")
parser.add_argument("--expected-sha", help="Require the source-stable draft SHA-256")
parser.add_argument("--scan-tail", action="store_true")
parser.add_argument("--strict-tail", action="store_true")
parser.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
args = parser.parse_args()
DRAFT_BYTES = (BOOK / "chapter-VI-intro.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT_BYTES).hexdigest()
if args.expected_sha:
    assert SHA.lower() == args.expected_sha.lower(), "Draft changed after review freeze"
FORMAL_BYTES = (BOOK / "chapter-VI-intro.json").read_bytes() if args.formal else None
if args.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if args.formal else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
LAST = BLOCKS[-1]["id"]
assert CHAPTER["sourcePdfPages"] == [568, 568]
assert len(BLOCKS) == 5 and [block["kind"] for block in BLOCKS] == [
    "heading", "paragraph", "paragraph", "paragraph", "paragraph"]
assert BLOCKS[0]["level"] == 1 and LAST == "p568-b005"
assert BLOCKS[0]["text"] == "关于第六部分"
assert len(CHAPTER["toc"]) == 1 and CHAPTER["toc"][0]["block"] == BLOCKS[0]["id"]
assert not any(block["kind"] in ("figure", "formula", "exercise", "table", "code",
                                  "footnote", "box") for block in BLOCKS)

BOOK_SCRIPT = None if args.formal else (ROOT / "books.js").read_text(encoding="utf-8") + """
const aboutVIPreview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const existingIntro = aboutVIPreview.findIndex(item => item.id === "VI-intro");
if (existingIntro >= 0) aboutVIPreview.splice(existingIntro, 1);
let afterVI = aboutVIPreview.findIndex(item => item.id === "VI");
if (afterVI < 0) {
  const after46 = aboutVIPreview.findIndex(item => item.id === "46");
  if (after46 < 0) throw Error("Cannot find chapter 46 for Part VI intro draft preview");
  aboutVIPreview.splice(after46 + 1, 0,
    {id: "VI", number: "第六部分", title: "稀疏图码",
     content: "books/mackay-information-theory-2003/chapter-VI.draft.json"});
  afterVI = after46 + 1;
}
aboutVIPreview.splice(afterVI + 1, 0,
  {id: "VI-intro", number: "导页", title: "关于第六部分",
   content: "books/mackay-information-theory-2003/chapter-VI-intro.draft.json"});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-part-VI-intro-formal-qa" if args.formal else "mackay-part-VI-intro-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def text_lines(page, selector):
    return page.locator(selector).evaluate_all("""items => items.map(item => {
      const lines = new Map();
      const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        for (let i=0;i<node.length;i++) {
          const range = document.createRange();
          range.setStart(node,i); range.setEnd(node,i+1);
          const rect = range.getBoundingClientRect();
          if (rect.width<.1 || rect.height<.1) continue;
          const top = Math.round(rect.top);
          lines.set(top,(lines.get(top)||'')+node.textContent[i]);
        }
      }
      return {id:item.closest('.reading-block')?.id,
        lines:[...lines.entries()].sort((a,b)=>a[0]-b[0])
          .map(([_,line])=>line.trim()).filter(Boolean)};
    })""")


def inspect_progress(page):
    last = f"read-{LAST}"
    page.wait_for_function("""key => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === 'VI-intro';
    }""", arg=PROGRESS_KEY)
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    try:
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === 'VI-intro' && saved.page === 568 &&
            saved.block === last &&
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
          return saved.chapter === 'VI-intro' && saved.page === 568 &&
            saved.block === last &&
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
        permissions=["clipboard-read","clipboard-write"],
    )
    if not args.formal:
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
    page.goto(base + "?book=mackay-information-theory-2003&chapter=VI-intro")
    page.locator(f"#read-{LAST}").wait_for()
    if args.formal:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith(
            "/books/mackay-information-theory-2003/chapter-VI-intro.json")
            for url in requests)
        assert not any(url.endswith("chapter-VI-intro.draft.json") for url in requests)
    else:
        assert any(url.endswith("chapter-VI-intro.draft.json") for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-heading h2, .reading-heading h3").count() == 0
    assert page.locator(".reading-paragraph").count() == 4
    assert page.locator(".reading-heading h1").inner_text() == BLOCKS[0]["text"]
    assert page.locator(".reading-heading h1").evaluate("""node=>({
      align:getComputedStyle(node).textAlign,
      style:getComputedStyle(node).fontStyle,
      border:getComputedStyle(node).borderTopWidth})""") == {
        "align":"center","style":"italic","border":"3px"}
    assert page.locator(".reading-paragraph em").all_inner_texts() == [
        "稀疏图码","低密度奇偶校验码","Turbo 码",
        "重复—累加码（repeat–accumulate codes）","数字喷泉码"]
    assert page.locator(".inline-math math").count() == 5
    assert page.locator("math merror").count() == 0
    copied=0
    if (width,mode) in ((1440,"light"),(320,"dark")):
        for math in page.locator(".inline-math math").all():
            math.scroll_into_view_if_needed()
            math.select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()").strip()
            page.evaluate("getSelection().removeAllRanges()")
            copied+=1
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 0
        assert page.locator(
            f"{selector} .toc-chapter-link[href$='chapter=VI']").count() == 1
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p568-b001']"
        ).count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node => node.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("node => node.open")

    assert page.locator(".book-formula, .book-figure, .book-table, "
                        ".book-code, .book-exercise-label, .book-footnote").count() == 0
    short_tails=[]
    if args.scan_tail:
        for item in text_lines(page,".reading-paragraph p"):
            if (len(item["lines"])>1 and len(item["lines"][-1])<=2 and
                    re.search(r"[\u4e00-\u9fff。！？：；，、]$",item["lines"][-1])):
                short_tails.append({"id":item["id"],"tail":item["lines"][-1]})
                page.locator(f"#{item['id']}").screenshot(
                    path=str(QA_DIR/f"short-tail-{item['id']}-{suffix}.png"))
        if args.strict_tail:
            assert not short_tails,(suffix,short_tails)
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"page-top-{suffix}.png"))
    page.locator("#read-p568-b003").screenshot(
        path=str(QA_DIR / f"paragraph-2-{suffix}.png"))

    previous = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=VI']")
    assert previous.count() == 1
    previous.click()
    page.locator("#read-p567-b002").wait_for()
    assert "chapter=VI" in page.url
    next_link = page.locator(
        "#chapter-navigation .chapter-navigation-link[href$='chapter=VI-intro']")
    assert next_link.count() == 1
    next_link.click()
    page.locator(f"#read-{LAST}").wait_for()
    assert "chapter=VI-intro" in page.url
    progress = inspect_progress(page)
    page.screenshot(path=str(QA_DIR / f"page-bottom-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "paragraphs": 4,
        "copied":copied,"shortTails":short_tails,
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
        print(f"PASS: About Part VI {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, "
              f"sha256={SHA}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
