"""Independent six-viewport Edge QA for MacKay PDF546 prelude."""

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
ARGS = PARSER.parse_args()

DRAFT = (BOOK / "chapter-45-prelude.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen draft changed", SHA)
FORMAL = (BOOK / "chapter-45-prelude.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL == DRAFT, "Formal JSON differs from reviewed draft"
CHAPTER = json.loads((FORMAL if ARGS.formal else DRAFT).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
URLS = ("http://www.inference.phy.cam.ac.uk/mackay/itprnn/software.html",
        "http://www.cs.toronto.edu/~radford/")
KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"

assert CHAPTER["bookId"] == "mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [546, 546]
assert CHAPTER["title"] == "关于第 45 章"
assert len(BLOCKS) == 7
assert [block["id"] for block in BLOCKS] == [f"p546-b{index:03d}" for index in range(1, 8)]
assert [block["kind"] for block in BLOCKS] == [
    "heading", "paragraph", "paragraph", "paragraph", "exercise",
    "paragraph", "paragraph"]
assert all(block["pdfPage"] == 546 for block in BLOCKS)
assert len(CHAPTER["toc"]) == 1 and CHAPTER["toc"][0]["block"] == "p546-b001"
assert BLOCKS[0]["text"] == "关于第 45 章"
assert BLOCKS[4]["label"] == "▷ 习题 45.1"
assert "难度 3" in BLOCKS[4]["text"]
assert not any(block["kind"] in ("figure", "formula", "table", "code",
                                  "footnote", "box", "intro") for block in BLOCKS)
assert not any(isinstance(segment, dict) and "mathml" in segment
               for block in BLOCKS for segment in block.get("segments", []))
assert [segment["href"] for block in BLOCKS for segment in block.get("segments", [])
        if isinstance(segment, dict) and "href" in segment] == list(URLS)
assert [segment["text"] for block in BLOCKS for segment in block.get("segments", [])
        if isinstance(segment, dict) and "href" in segment] == list(URLS)
assert any(isinstance(segment, dict) and segment.get("code")
           and segment.get("text") == "octave" for segment in BLOCKS[5]["segments"])

BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(encoding="utf-8") + """
const ch45PreludePreview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = ch45PreludePreview.findIndex(x => x.id === "45-prelude");
if (existing >= 0) ch45PreludePreview.splice(existing, 1);
const after44 = ch45PreludePreview.findIndex(x => x.id === "44");
if (after44 < 0) throw Error("Chapter 44 must precede the PDF546 prelude");
ch45PreludePreview.splice(after44+1, 0,
  {id:"45-prelude",number:"45-prelude",title:"关于第 45 章",
   content:"books/mackay-information-theory-2003/chapter-45-prelude.draft.json"});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch45-prelude-formal-qa" if ARGS.formal else "mackay-ch45-prelude-draft-qa")
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


def bottom_progress(page):
    target = "read-p546-b007"
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    page.wait_for_function("""({key,target}) => {
      const saved=JSON.parse(localStorage.getItem(key)||'{}');
      return saved.chapter==='45-prelude'&&saved.page===546&&saved.block===target&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""", arg={"key": KEY, "target": target})
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key,target}) => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='45-prelude'&&saved.page===546&&saved.block===target&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""", arg={"key": KEY, "target": target})
        positions.append(page.evaluate("""target => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById(target).getBoundingClientRect().top)
        })""", target))
    assert len({tuple(item.values()) for item in positions}) == 1, positions
    return positions


def inspect(browser, base, width, mode):
    name=f"{width}-{mode}"
    context=browser.new_context(viewport={"width":width,"height":844},
                                color_scheme=mode,service_workers="block")
    if not ARGS.formal:
        context.route("**/books.js", lambda route:route.fulfill(
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
    page.goto(base+"?book=mackay-information-theory-2003&chapter=45-prelude")
    page.locator("#read-p546-b007").wait_for()
    expected_json="chapter-45-prelude.json" if ARGS.formal else "chapter-45-prelude.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if ARGS.formal:
        assert not any(url.endswith("chapter-45-prelude.draft.json") for url in requests)

    actual=page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    assert actual==[[f"read-{block['id']}",f"reading-{block['kind']}"]
                   for block in BLOCKS]
    heading=page.locator("#read-p546-b001 h1")
    assert heading.count()==1 and heading.inner_text()==BLOCKS[0]["text"]
    style=heading.evaluate("""node=>({
      italic:getComputedStyle(node).fontStyle,
      align:getComputedStyle(node).textAlign,
      border:getComputedStyle(node).borderTopWidth,
      width:node.getBoundingClientRect().width,
      textWidth:(()=>{const r=document.createRange();r.selectNodeContents(node);
        return r.getBoundingClientRect().width})()
    })""")
    assert style["italic"]=="italic" and style["align"]=="center",style
    assert float(style["border"].removesuffix("px"))>=2.5,style
    assert page.locator(".reading-paragraph").count()==5
    exercise=page.locator("#read-p546-b005")
    assert exercise.locator(".book-exercise-label").inner_text()=="▷ 习题 45.1"
    assert "难度 3" in exercise.inner_text()
    assert page.locator(".book-figure,.book-formula,.book-table,.book-code,.book-footnote,.inline-math").count()==0
    assert page.locator("math merror,.formula-fallback,.figure-error").count()==0
    assert page.locator("#read-p546-b006 code").inner_text()=="octave"

    anchors=page.locator("#read-p546-b006 a,#read-p546-b007 a")
    assert anchors.count()==2
    assert [anchor.get_attribute("href") for anchor in anchors.all()]==list(URLS)
    assert [anchor.inner_text() for anchor in anchors.all()]==list(URLS)
    assert all(anchor.is_visible() and anchor.is_enabled() for anchor in anchors.all())
    page.evaluate("""() => {
      window.__qaClicked=[];
      document.addEventListener('click',event=>{
        const anchor=event.target.closest('a');
        if (anchor && anchor.href.startsWith('http')) {
          event.preventDefault(); window.__qaClicked.push(anchor.href);
        }
      },true);
    }""")
    for anchor in anchors.all():
        anchor.click()
    assert page.evaluate("window.__qaClicked")==list(URLS)
    assert all(page.locator(f"#read-p546-b00{index}").inner_text().endswith("。")
               for index in (6,7))

    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current[href='#read-p546-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link").count()==0
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=44']").count()==1
    if width<800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()
    short_tails=[item for item in text_lines(page,".reading-paragraph p,.book-exercise")
                 if len(item["lines"])>1 and len(item["lines"][-1])<=2]
    assert not short_tails,(name,short_tails)
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(QA_DIR/f"page-{name}.png"),full_page=True)
    progress=bottom_progress(page)

    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=44']").click()
    page.locator("#read-p545-b015").wait_for()
    assert "chapter=44" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=45-prelude']").click()
    page.locator("#read-p546-b007").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(actual),"toc":1,
                      "titleStyle":style,"urls":list(URLS),
                      "shortTails":short_tails,"progress":progress,
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
        print(f"PASS: chapter 45 prelude {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, sha256={SHA}, "
              f"screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
