"""Independent six-viewport Edge QA for MacKay bibliography (PDF625–631)."""

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
PARSER = ArgumentParser()
PARSER.add_argument("--formal", action="store_true")
PARSER.add_argument("--sha256", required=True)
PARSER.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
PARSER.add_argument("--scan-tail", action="store_true")
PARSER.add_argument("--strict-tail", action="store_true")
ARGS = PARSER.parse_args()

DRAFT = (BOOK / "chapter-REF.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen bibliography changed", SHA)
FORMAL = (BOOK / "chapter-REF.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL == DRAFT, "Formal bibliography differs from reviewed draft"
CHAPTER = json.loads((FORMAL if ARGS.formal else DRAFT).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
ENTRIES = BLOCKS[1:]
KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
PER_PAGE = {625: 37, 626: 49, 627: 44, 628: 47, 629: 47, 630: 49, 631: 45}

assert CHAPTER["bookId"] == "mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [625, 631]
assert CHAPTER["toc"] == [{"number": "", "title": "参考文献", "block": "p625-b001"}]
assert len(BLOCKS) == 319 and len(ENTRIES) == 318
assert BLOCKS[0]["kind"] == "heading" and BLOCKS[0]["text"] == "参考文献"
assert BLOCKS[0]["id"] == "p625-b001" and BLOCKS[0]["level"] == 1
assert all(block["kind"] == "reference-entry" for block in ENTRIES)
assert Counter(block["pdfPage"] for block in ENTRIES) == PER_PAGE
assert len({block["id"] for block in BLOCKS}) == len(BLOCKS)
assert ENTRIES[0]["text"].startswith("Abrahamsen, P. (1997)")
assert ENTRIES[-1]["text"].startswith("Ziv, J., and Lempel, A. (1978)")
assert ENTRIES[-1]["id"] == "p631-b045"
assert sum(isinstance(segment, dict) and segment.get("em", False)
           for block in ENTRIES for segment in block["segments"]) == 226
assert all(block["text"] == "".join(
    segment if isinstance(segment, str) else segment["text"]
    for segment in block["segments"]) for block in ENTRIES)

BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(
    encoding="utf-8") + """
const bibliographyPreview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = bibliographyPreview.findIndex(x => x.id === "REF");
if (existing >= 0) bibliographyPreview.splice(existing, 1);
const afterC = bibliographyPreview.findIndex(x => x.id === "C");
if (afterC < 0) throw Error("Appendix C must precede bibliography");
bibliographyPreview.splice(afterC+1, 0,
  {id:"REF",number:"书后",title:"参考文献",
   content:"books/mackay-information-theory-2003/chapter-REF.draft.json"});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-bibliography-formal-qa" if ARGS.formal else "mackay-bibliography-draft-qa")
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
      const lines=new Map();
      const walker=document.createTreeWalker(item,NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node=walker.currentNode;
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
        lines:[...lines.entries()].sort((a,b)=>a[0]-b[0])
          .map(([_,line])=>line.trim()).filter(Boolean)};
    })""")


def bottom_progress(page):
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    page.wait_for_function("""key => {
      const saved=JSON.parse(localStorage.getItem(key)||'{}');
      return saved.chapter==='REF'&&saved.page===631&&
        saved.block==='read-p631-b045'&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""", arg=KEY)
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='REF'&&saved.page===631&&
            saved.block==='read-p631-b045'&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""", arg=KEY)
        positions.append(page.evaluate("""() => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById('read-p631-b045').getBoundingClientRect().top)
        })"""))
    assert len({tuple(item.values()) for item in positions})==1,positions
    return positions


def inspect(browser,base,width,mode):
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
    page.goto(base+"?book=mackay-information-theory-2003&chapter=REF")
    page.locator("#read-p631-b045").wait_for()
    expected_json="chapter-REF.json" if ARGS.formal else "chapter-REF.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if ARGS.formal:
        assert not any(url.endswith("chapter-REF.draft.json") for url in requests)
    assert page.evaluate("document.documentElement.dataset.theme")==mode
    rendered=page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    assert rendered==[[f"read-{block['id']}",f"reading-{block['kind']}"]
                     for block in BLOCKS]
    h1=page.locator("#read-p625-b001 h1")
    assert h1.inner_text()=="参考文献"
    assert h1.evaluate("node=>getComputedStyle(node).textAlign")=="center"
    assert h1.evaluate("node=>getComputedStyle(node).fontStyle")=="italic"
    assert h1.evaluate("node=>parseFloat(getComputedStyle(node).borderTopWidth)")>=2.5
    h1.screenshot(path=str(QA_DIR/f"heading-{name}.png"))
    assert page.locator(".reading-reference-entry p").count()==318
    assert page.locator(".reading-reference-entry em").count()==226
    assert page.locator(".reading-heading").count()==1
    assert page.locator("math,.book-formula,.book-figure,.book-table,.book-exercise,.book-footnote").count()==0
    for block in ENTRIES:
        item=page.locator(f"#read-{block['id']} p")
        assert item.text_content()==block["text"],block["id"]
    indent=page.locator("#read-p625-b002 p").evaluate("""node=>({
      padding:parseFloat(getComputedStyle(node).paddingLeft),
      indent:parseFloat(getComputedStyle(node).textIndent)})""")
    assert indent["padding"]>=20 and indent["indent"]<=-20,indent
    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p625-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link").count()==0
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=C']").count()==1
    if width<800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()
    short_tails=[]
    if ARGS.scan_tail:
        lines=text_lines(page,".reading-reference-entry p")
        short_tails=[item for item in lines if len(item["lines"])>1
                     and len(item["lines"][-1])<=2]
        for item in short_tails:
            page.locator(f"#{item['id']}").screenshot(
                path=str(QA_DIR/f"short-tail-{item['id']}-{name}.png"))
        if ARGS.strict_tail:
            assert not short_tails,(name,short_tails)
    spots={ENTRIES[0]["id"],ENTRIES[36]["id"],ENTRIES[37]["id"],
           ENTRIES[85]["id"],ENTRIES[130]["id"],ENTRIES[177]["id"],
           ENTRIES[224]["id"],ENTRIES[273]["id"],ENTRIES[-1]["id"],
           "p629-b040","p631-b024","p627-b009"}
    for block_id in spots:
        page.locator(f"#read-{block_id}").screenshot(
            path=str(QA_DIR/f"entry-{block_id}-{name}.png"))
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(QA_DIR/f"page-{name}.png"),full_page=True)
    positions=bottom_progress(page)
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=C']").click()
    page.locator("#read-p624-b003").wait_for()
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=REF']").click()
    page.locator("#read-p631-b045").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(rendered),"toc":1,
                      "entries":len(ENTRIES),"emphasis":226,
                      "shortTails":short_tails,"progress":positions,
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
        print(f"PASS: bibliography {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, sha256={SHA}, "
              f"screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
