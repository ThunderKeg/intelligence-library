"""Independent six-viewport Edge QA for MacKay Appendix A (PDF610–612)."""

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

DRAFT = (BOOK / "chapter-A.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen Appendix A changed", SHA)
FORMAL = (BOOK / "chapter-A.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL == DRAFT, "Formal Appendix A differs from reviewed draft"
CHAPTER = json.loads((FORMAL if ARGS.formal else DRAFT).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
PARAGRAPHS = [block for block in BLOCKS if block["kind"] == "paragraph"]
KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"


def inline_count(value):
    if isinstance(value, list):
        return sum(inline_count(item) for item in value)
    if isinstance(value, dict):
        if "mathml" in value and "kind" not in value:
            return 1
        return sum(inline_count(item) for key, item in value.items() if key != "mathml")
    return 0


assert CHAPTER["bookId"] == "mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [610, 612]
assert CHAPTER["toc"] == [{"number": "A", "title": "记号", "block": "p610-b001"}]
assert len(BLOCKS) == 49 and len(FORMULAS) == 12 and len(PARAGRAPHS) == 35
assert [block["number"] for block in FORMULAS if block.get("number")] == [
    f"(A.{index})" for index in range(1, 12)]
assert sum(not block.get("number") for block in FORMULAS) == 1
assert [block["id"] for block in FORMULAS if not block.get("number")] == ["p612-b005"]
assert inline_count(BLOCKS) == 122
assert len([block for block in PARAGRAPHS
            if any(isinstance(segment, dict) and segment.get("strong")
                   for segment in block.get("segments", []))]) == 19
assert BLOCKS[0]["id"] == "p610-b001" and BLOCKS[0]["text"] == "附录 A　记号"
assert BLOCKS[0]["kind"] == "heading" and BLOCKS[1]["kind"] == "intro"
assert BLOCKS[-1]["id"] == "p612-b014" and BLOCKS[-1]["pdfPage"] == 612
assert len({block["id"] for block in BLOCKS}) == len(BLOCKS)
assert all(610 <= block["pdfPage"] <= 612 for block in BLOCKS)
assert not any(block["kind"] in ("figure", "image", "table", "code", "exercise",
                                 "footnote", "box") for block in BLOCKS)

BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(
    encoding="utf-8") + """
const appendixAPreview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = appendixAPreview.findIndex(x => x.id === "A");
if (existing >= 0) appendixAPreview.splice(existing, 1);
const afterVII = appendixAPreview.findIndex(x => x.id === "VII");
if (afterVII < 0) throw Error("Part VII must precede Appendix A");
appendixAPreview.splice(afterVII+1, 0,
  {id:"A",number:"A",title:"记号",
   content:"books/mackay-information-theory-2003/chapter-A.draft.json"});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-appendix-A-formal-qa" if ARGS.formal else "mackay-appendix-A-draft-qa")
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
      return {id:item.closest('.reading-block')?.id,hasMath:!!item.querySelector('math'),
        lines:[...lines.entries()].sort((a,b)=>a[0]-b[0])
          .map(([_,line])=>line.trim()).filter(Boolean)};
    })""")


def horizontal_scroll(node):
    metric=node.evaluate("node=>({client:node.clientWidth,width:node.scrollWidth})")
    if metric["width"]>metric["client"]+2:
        node.evaluate("node=>node.scrollLeft=node.scrollWidth")
        assert node.evaluate("node=>node.scrollLeft") >= (
            metric["width"]-metric["client"]-2),metric
        node.evaluate("node=>node.scrollLeft=0")
    return metric


def bottom_progress(page):
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    page.wait_for_function("""key => {
      const saved=JSON.parse(localStorage.getItem(key)||'{}');
      return saved.chapter==='A'&&saved.page===612&&
        saved.block==='read-p612-b014'&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""",arg=KEY)
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='A'&&saved.page===612&&
            saved.block==='read-p612-b014'&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""",arg=KEY)
        positions.append(page.evaluate("""() => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById('read-p612-b014').getBoundingClientRect().top)
        })"""))
    assert len({tuple(item.values()) for item in positions})==1,positions
    return positions


def inspect(browser,base,width,mode):
    name=f"{width}-{mode}"
    context=browser.new_context(viewport={"width":width,"height":844},
                                color_scheme=mode,service_workers="block",
                                permissions=["clipboard-read","clipboard-write"])
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
    page.goto(base+"?book=mackay-information-theory-2003&chapter=A")
    page.locator("#read-p612-b014").wait_for()
    expected_json="chapter-A.json" if ARGS.formal else "chapter-A.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if ARGS.formal:
        assert not any(url.endswith("chapter-A.draft.json") for url in requests)
    assert page.evaluate("document.documentElement.dataset.theme")==mode
    rendered=page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    assert rendered==[[f"read-{block['id']}",f"reading-{block['kind']}"]
                     for block in BLOCKS]
    h1=page.locator("#read-p610-b001 h1")
    title=text_lines(page,"#read-p610-b001 h1")[0]["lines"]
    assert title==["附录 A","记号"],(name,title)
    assert h1.evaluate("node=>getComputedStyle(node).textAlign")=="center"
    assert h1.locator("span").nth(0).evaluate(
        "node=>parseFloat(getComputedStyle(node).borderBottomWidth)")>=2.5
    assert h1.locator("span").nth(1).evaluate(
        "node=>getComputedStyle(node).fontStyle")=="italic"
    assert "编者导读" in page.locator(".reading-intro").inner_text()
    assert page.locator(".reading-paragraph strong").count()==23
    assert page.locator(".reading-paragraph:has(strong)").count()==19
    assert page.locator(".book-formula math").count()==12
    assert page.locator(".inline-math math").count()==122
    assert page.locator("math merror,.formula-fallback").count()==0
    assert page.locator(".book-figure,.book-table,.book-exercise,.book-footnote").count()==0
    assert page.locator("#read-p611-b018 .book-formula msup > mi[mathvariant='normal']").text_content()=="T"
    first_row=page.locator("#read-p612-b005 math mtr").nth(0).text_content()
    assert "," not in first_row
    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p610-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link").count()==0
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=VII']").count()==1
    if width<800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()
    short_tails=[]
    if ARGS.scan_tail:
        short_tails=[item for item in text_lines(page,".reading-paragraph p")
                     if not item["hasMath"] and len(item["lines"])>1
                     and len(item["lines"][-1])<=2]
        for item in short_tails:
            page.locator(f"#{item['id']}").screenshot(
                path=str(QA_DIR/f"short-tail-{item['id']}-{name}.png"))
        if ARGS.strict_tail:
            assert not short_tails,(name,short_tails)
    formula_overflow,copied=[],0
    for block in FORMULAS:
        item=page.locator(f"#read-{block['id']}")
        if block.get("number"):
            assert item.locator(".formula-number").inner_text()==block["number"]
        else:
            assert item.locator(".formula-number").count()==0
        scroll=item.locator(".formula-scroll")
        metric=horizontal_scroll(scroll)
        if metric["width"]>metric["client"]+2:
            formula_overflow.append(block.get("number") or block["id"])
            assert item.locator(".formula-view-hint").is_visible()
            if width<800:
                scroll.scroll_into_view_if_needed()
                scroll.evaluate("node=>node.scrollLeft=node.scrollWidth")
                page.screenshot(path=str(QA_DIR/f"formula-viewport-{block['id']}-{name}-right.png"))
                scroll.evaluate("node=>node.scrollLeft=0")
        if (width,mode) in ((1440,"light"),(320,"dark")):
            item.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()").strip()
            page.evaluate("getSelection().removeAllRanges()")
            copied+=1
            if block["id"] in ("p611-b018","p612-b005"):
                item.screenshot(path=str(QA_DIR/f"formula-{block['id']}-{name}.png"))
    inline=page.locator(".inline-math").evaluate_all("""items=>items.map(node=>({
      client:node.clientWidth,width:node.scrollWidth,focusable:node.tabIndex>=0,
      hint:!!node.nextElementSibling?.classList.contains('inline-math-view-hint')&&
        getComputedStyle(node.nextElementSibling).display!=='none'}))""")
    assert all((item["width"]>item["client"]+2)==item["hint"] for item in inline)
    for index,item in enumerate(inline):
        if item["width"]>item["client"]+2:
            assert item["focusable"]
            horizontal_scroll(page.locator(".inline-math").nth(index))
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(QA_DIR/f"page-{name}.png"),full_page=True)
    positions=bottom_progress(page)
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=VII']").click()
    page.locator("#read-p609-b002").wait_for()
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=A']").click()
    page.locator("#read-p612-b014").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(rendered),"toc":1,
                      "formulas":len(FORMULAS),"formulaCopied":copied,
                      "formulaOverflow":formula_overflow,"inlineMath":len(inline),
                      "inlineOverflow":sum(item["width"]>item["client"]+2 for item in inline),
                      "boldQuestions":19,"shortTails":short_tails,
                      "progress":positions,"errors":errors,"failed":failed}),flush=True)


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
        print(f"PASS: Appendix A {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, sha256={SHA}, "
              f"screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__=="__main__":
    main()
