"""Independent six-viewport Edge QA for MacKay Part VII title page."""

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

DRAFT = (BOOK / "chapter-VII.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen draft changed", SHA)
FORMAL = (BOOK / "chapter-VII.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL == DRAFT, "Formal JSON differs from reviewed draft"
PART = json.loads((FORMAL if ARGS.formal else DRAFT).decode("utf-8"))
assert PART["bookId"] == "mackay-information-theory-2003"
assert PART["sourcePdfPages"] == [609, 609]
assert PART["toc"] == [{"number": "第七部分", "title": "附录", "block": "p609-b001"}]
assert len(PART["blocks"]) == 2
HEADING, FIGURE = PART["blocks"]
assert (HEADING["id"], HEADING["kind"], HEADING["level"], HEADING["text"]) == (
    "p609-b001", "heading", 1, "第七部分　附录")
assert HEADING["segments"] == ["第七部分\n附录"]
assert (FIGURE["id"], FIGURE["kind"], FIGURE["src"]) == (
    "p609-b002", "figure", "assets/part-VII-emblem.png")
assert (FIGURE["width"], FIGURE["height"]) == (2590, 2620)
assert FIGURE.get("wide") is True
assert not FIGURE.get("caption") and not FIGURE.get("annotations")

BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(
    encoding="utf-8") + """
const partVIIPreview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
for (const id of ["50", "VII"]) {
  const existing = partVIIPreview.findIndex(x => x.id === id);
  if (existing >= 0) partVIIPreview.splice(existing, 1);
}
const afterIntro = partVIIPreview.findIndex(x => x.id === "50-intro");
if (afterIntro < 0) throw Error("PDF600 chapter 50 intro must precede Part VII");
partVIIPreview.splice(afterIntro+1, 0,
  {id:"50",number:"50",title:"数字喷泉码",
   content:"books/mackay-information-theory-2003/chapter-50.draft.json"},
  {id:"VII",number:"第七部分",title:"附录",
   content:"books/mackay-information-theory-2003/chapter-VII.draft.json"});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-part-VII-formal-qa" if ARGS.formal else "mackay-part-VII-draft-qa")
QA_DIR.mkdir(exist_ok=True)
KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
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


def title_lines(page):
    return page.locator("#read-p609-b001 h1").evaluate("""item => {
      const lines=new Map();
      const walker=document.createTreeWalker(item,NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node=walker.currentNode;
        for (let i=0;i<node.length;i++) {
          if (!node.textContent[i].trim()) continue;
          const range=document.createRange();
          range.setStart(node,i);range.setEnd(node,i+1);
          const top=Math.round(range.getBoundingClientRect().top);
          lines.set(top,(lines.get(top)||'')+node.textContent[i]);
        }
      }
      return [...lines.entries()].sort((a,b)=>a[0]-b[0]).map(([_,line])=>line.trim());
    }""")


def bottom_progress(page):
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    page.wait_for_function("""key => {
      const saved=JSON.parse(localStorage.getItem(key)||'{}');
      return saved.chapter==='VII'&&saved.page===609&&
        saved.block==='read-p609-b002'&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""", arg=KEY)
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='VII'&&saved.page===609&&
            saved.block==='read-p609-b002'&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""", arg=KEY)
        positions.append(page.evaluate("""() => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById('read-p609-b002').getBoundingClientRect().top)
        })"""))
    assert len({tuple(item.values()) for item in positions})==1,positions
    return positions


def inspect(browser, base, width, mode):
    name=f"{width}-{mode}"
    context=browser.new_context(viewport={"width":width,"height":844},
                                color_scheme=mode,service_workers="block")
    if not ARGS.formal:
        context.route("**/books.js",lambda route:route.fulfill(
            body=BOOK_SCRIPT,content_type="application/javascript"))
    page=context.new_page()
    errors,failed,requests=[],[],[]
    page.on("pageerror",lambda error:errors.append(str(error)))
    page.on("console",lambda message:errors.append(message.text)
            if message.type=="error" else None)
    page.on("request",lambda request:requests.append(request.url))
    page.on("requestfailed",lambda request:failed.append(
        f"{request.failure}: {request.url}")
        if request.failure!="net::ERR_ABORTED" else None)
    page.on("response",lambda response:failed.append(
        f"{response.status}: {response.url}") if response.status>=400 else None)
    page.goto(base+"?book=mackay-information-theory-2003&chapter=VII")
    page.locator("#read-p609-b002 .book-figure img").wait_for()
    expected_json="chapter-VII.json" if ARGS.formal else "chapter-VII.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if ARGS.formal:
        assert not any(url.endswith("chapter-VII.draft.json") for url in requests)
    assert page.evaluate("document.documentElement.dataset.theme")==mode
    assert page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")==[
        ["read-p609-b001","reading-heading"],["read-p609-b002","reading-figure"]]
    assert page.locator(".reading-block:not(.reading-heading):not(.reading-figure)").count()==0
    assert page.locator(".book-formula,.book-exercise,.book-table,.book-footnote").count()==0
    assert title_lines(page)==["第七部分","附录"],(name,title_lines(page))
    assert page.locator("#read-p609-b001 h1").evaluate(
        "node=>getComputedStyle(node).whiteSpace")=="pre-line"
    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p609-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link").count()==0
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=50']").count()==1
    if width<800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()
    image=page.locator("#read-p609-b002 .book-figure img")
    image.scroll_into_view_if_needed()
    image.evaluate("node=>node.decode()")
    assert image.evaluate("node=>[node.naturalWidth,node.naturalHeight]")==[2590,2620]
    assert image.get_attribute("alt")==FIGURE["alt"]
    assert page.locator("#read-p609-b002 .figure-image-link").get_attribute(
        "href").endswith(FIGURE["src"])
    assert page.locator("#read-p609-b002 figcaption").count()==0
    media=page.locator("#read-p609-b002 .figure-media")
    metrics=media.evaluate("node=>({client:node.clientWidth,width:node.scrollWidth})")
    hint=page.locator("#read-p609-b002 .figure-view-hint")
    hint_style=hint.evaluate("""node=>({height:node.getBoundingClientRect().height,
      font:getComputedStyle(node).fontSize,
      line:getComputedStyle(node).lineHeight})""")
    if ARGS.scan_tail and ARGS.strict_tail:
        assert hint_style["height"]<float(hint_style["line"].removesuffix("px"))*1.2,(
            name,hint_style)
    if width<800:
        assert metrics["width"]>metrics["client"]+2
        assert hint.is_visible()
        media.evaluate("node=>node.scrollLeft=node.scrollWidth")
        assert media.evaluate("node=>node.scrollLeft>0")
        page.screenshot(path=str(QA_DIR/f"figure-viewport-right-{name}.png"))
        media.evaluate("node=>node.scrollLeft=0")
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(QA_DIR/f"page-{name}.png"),full_page=True)
    image.screenshot(path=str(QA_DIR/f"figure-{name}.png"))
    positions=bottom_progress(page)
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=50']").click()
    page.locator("#read-p608-b007").wait_for()
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=VII']").click()
    page.locator("#read-p609-b002").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"titleLines":["第七部分","附录"],
                      "figure":metrics,"hint":hint_style,"progress":positions,
                      "errors":errors,"failed":failed}),flush=True)


def main():
    server=ThreadingHTTPServer(("127.0.0.1",0),
                               partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(
                headless=True,
                executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            for width,mode in VIEWPORTS:
                if ARGS.only and f"{width}-{mode}"!=ARGS.only:
                    continue
                inspect(browser,f"http://127.0.0.1:{server.server_port}/",width,mode)
            browser.close()
        print(f"PASS: Part VII {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, sha256={SHA}, "
              f"screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__=="__main__":
    main()
