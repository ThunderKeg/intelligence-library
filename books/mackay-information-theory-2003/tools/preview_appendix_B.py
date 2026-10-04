"""Independent six-viewport Edge QA for MacKay Appendix B (PDF613–616)."""

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

DRAFT = (BOOK / "chapter-B.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen Appendix B changed", SHA)
FORMAL = (BOOK / "chapter-B.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL == DRAFT, "Formal Appendix B differs from reviewed draft"
CHAPTER = json.loads((FORMAL if ARGS.formal else DRAFT).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]


def walk(blocks):
    for block in blocks:
        yield block
        yield from walk(block.get("blocks", []))


ALL = list(walk(BLOCKS))
FORMULAS = [block for block in ALL if block["kind"] == "formula"]
FIGURES = [block for block in ALL if block["kind"] == "figure"]
BOXES = [block for block in ALL if block["kind"] == "box"]
HEADINGS = [block for block in ALL if block["kind"] == "heading"]
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
assert CHAPTER["sourcePdfPages"] == [613, 616]
assert CHAPTER["toc"] == [
    {"number": "B", "title": "一些物理学知识", "block": "p613-b001"},
    {"number": "B.1", "title": "关于相变", "block": "p613-b003"},
]
assert len(BLOCKS) == 53 and len(ALL) == 55 and len(HEADINGS) == 5
assert len(FORMULAS) == 12 and len(FIGURES) == 2 and len(BOXES) == 2
assert [block["number"] for block in FORMULAS] == [
    f"(B.{index})" for index in range(1, 13)]
assert inline_count(BLOCKS) == 71
assert [block["src"] for block in FIGURES] == [
    f"assets/appendix-B/figure-B-{index}.png" for index in (1, 2)]
assert all(block.get("wide") and block.get("caption") for block in FIGURES)
assert [block["id"] for block in BOXES] == [
    "box-b-infinite-states", "box-b-long-range-correlations"]
assert all(block.get("outlined") and block.get("shadow") and
           len(block["blocks"]) == 1 for block in BOXES)
assert BLOCKS[0]["id"] == "p613-b001" and BLOCKS[0]["text"] == "附录 B　一些物理学知识"
assert BLOCKS[0]["kind"] == "heading" and BLOCKS[1]["kind"] == "intro"
assert BLOCKS[-1]["id"] == "p616-b002" and BLOCKS[-1]["pdfPage"] == 616
assert len({block["id"] for block in ALL}) == len(ALL)
assert all(613 <= block["pdfPage"] <= 616 for block in ALL)
assert not any(block["kind"] in ("table", "code", "exercise", "footnote", "quote")
               for block in ALL)

BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(
    encoding="utf-8") + """
const appendixBPreview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = appendixBPreview.findIndex(x => x.id === "B");
if (existing >= 0) appendixBPreview.splice(existing, 1);
const afterA = appendixBPreview.findIndex(x => x.id === "A");
if (afterA < 0) throw Error("Appendix A must precede Appendix B");
appendixBPreview.splice(afterA+1, 0,
  {id:"B",number:"B",title:"一些物理学知识",
   content:"books/mackay-information-theory-2003/chapter-B.draft.json"});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-appendix-B-formal-qa" if ARGS.formal else "mackay-appendix-B-draft-qa")
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
      return saved.chapter==='B'&&saved.page===616&&
        saved.block==='read-p616-b002'&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""",arg=KEY)
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='B'&&saved.page===616&&
            saved.block==='read-p616-b002'&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""",arg=KEY)
        positions.append(page.evaluate("""() => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById('read-p616-b002').getBoundingClientRect().top)
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
    page.goto(base+"?book=mackay-information-theory-2003&chapter=B")
    page.locator("#read-p616-b002").wait_for()
    expected_json="chapter-B.json" if ARGS.formal else "chapter-B.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if ARGS.formal:
        assert not any(url.endswith("chapter-B.draft.json") for url in requests)
    assert page.evaluate("document.documentElement.dataset.theme")==mode
    rendered=page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    assert rendered==[[f"read-{block['id']}",f"reading-{block['kind']}"]
                     for block in ALL if block["kind"] != "box"]
    h1=page.locator("#read-p613-b001 h1")
    title=text_lines(page,"#read-p613-b001 h1")[0]["lines"]
    assert title==["附录 B","一些物理学知识"],(name,title)
    assert h1.evaluate("node=>getComputedStyle(node).textAlign")=="center"
    assert h1.locator("span").nth(0).evaluate(
        "node=>parseFloat(getComputedStyle(node).borderBottomWidth)")>=2.5
    assert h1.locator("span").nth(1).evaluate(
        "node=>getComputedStyle(node).fontStyle")=="italic"
    assert "编者导读" in page.locator(".reading-intro").inner_text()
    section=page.locator("#read-p613-b003 h2")
    assert section.text_content().replace(" ","")=="▶B.1\u3000关于相变"
    assert page.locator("#read-p613-b003 h2 [aria-hidden='true']").inner_text()=="▶"
    for block in HEADINGS[2:]:
        heading=page.locator(f"#read-{block['id']} h3")
        assert heading.text_content()==block["text"]
        assert heading.evaluate("node=>getComputedStyle(node).fontStyle")=="italic"
    assert page.locator("#read-p616-b002 em").inner_text()=="反之亦然"
    assert page.locator("aside.book-box").count()==2
    for block in BOXES:
        aside=page.locator(f"#read-{block['id']}")
        assert aside.evaluate("node=>node.classList.contains('outlined-box')")
        assert aside.locator(".reading-block").count()==1
        assert aside.evaluate("node=>getComputedStyle(node).boxShadow")!="none"
        aside.screenshot(path=str(QA_DIR/f"box-{block['id']}-{name}.png"))
    if width==390:
        assert page.locator("#read-p614-b002 p").evaluate(
            "node=>getComputedStyle(node).textWrap")=="balance"
    assert page.locator(".book-formula math").count()==12
    assert page.locator(".inline-math math").count()==71
    assert page.locator("math merror,.formula-fallback").count()==0
    assert page.locator(".book-figure img").count()==2
    assert page.locator(".book-table,.book-exercise,.book-footnote").count()==0
    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p613-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link[href='#read-p613-b003']").count()==1
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=A']").count()==1
    if width<800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()
    short_tails=[]
    math_tail_candidates=[]
    if ARGS.scan_tail:
        lines=text_lines(page,".reading-paragraph p,.figure-caption p")
        short_tails=[item for item in lines
                     if not item["hasMath"] and len(item["lines"])>1
                     and len(item["lines"][-1])<=2]
        math_tail_candidates=[item for item in lines
                              if item["hasMath"] and len(item["lines"])>1
                              and len(item["lines"][-1])<=2]
        for item in short_tails:
            page.locator(f"#{item['id']}").screenshot(
                path=str(QA_DIR/f"short-tail-{item['id']}-{name}.png"))
        for item in math_tail_candidates:
            page.locator(f"#{item['id']}").screenshot(
                path=str(QA_DIR/f"math-tail-candidate-{item['id']}-{name}.png"))
        if ARGS.strict_tail:
            assert not short_tails,(name,short_tails)
    if width==320:
        for block_id in ("p613-b015","p615-b011"):
            page.locator(f"#read-{block_id}").screenshot(
                path=str(QA_DIR/f"revised-{block_id}-{name}.png"))
    formula_overflow,copied=[],0
    for block in FORMULAS:
        item=page.locator(f"#read-{block['id']}")
        assert item.locator(".formula-number").inner_text()==block["number"]
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
            if block["id"] in ("p613-b016","p614-b014","p615-b006"):
                item.screenshot(path=str(QA_DIR/f"formula-{block['id']}-{name}.png"))
    figure_overflow=[]
    for block in FIGURES:
        item=page.locator(f"#read-{block['id']}")
        image=item.locator(".book-figure img")
        image.scroll_into_view_if_needed()
        image.evaluate("node=>node.decode()")
        dimensions=image.evaluate("node=>({width:node.naturalWidth,height:node.naturalHeight})")
        assert dimensions==({"width":1658,"height":1462} if block["id"]=="p615-b001"
                            else {"width":1658,"height":780})
        assert image.get_attribute("src").endswith(block["src"])
        assert item.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
        caption=item.locator(".figure-caption")
        assert caption.inner_text().startswith(f"图 B.{FIGURES.index(block)+1}")
        assert "图内文字译注" in caption.inner_text()
        assert caption.locator(".inline-math math").count()==inline_count(
            block["captionSegments"])
        metric=horizontal_scroll(item.locator(".figure-media"))
        if metric["width"]>metric["client"]+2:
            figure_overflow.append(block["id"])
            assert item.locator(".figure-view-hint").is_visible()
            if width<=360 and ARGS.strict_tail:
                hint_lines=text_lines(page,f"#read-{block['id']} .figure-view-hint")[0]["lines"]
                assert len(hint_lines)==1,(name,block["id"],hint_lines)
        item.screenshot(path=str(QA_DIR/f"figure-{block['id']}-{name}.png"))
        if width<800 and metric["width"]>metric["client"]+2:
            media=item.locator(".figure-media")
            media.scroll_into_view_if_needed()
            media.evaluate("node=>node.scrollLeft=node.scrollWidth")
            page.screenshot(path=str(QA_DIR/f"figure-viewport-{block['id']}-{name}-right.png"))
            media.evaluate("node=>node.scrollLeft=0")
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
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=A']").click()
    page.locator("#read-p612-b014").wait_for()
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=B']").click()
    page.locator("#read-p616-b002").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(rendered),"toc":2,
                      "formulas":len(FORMULAS),"formulaCopied":copied,
                      "formulaOverflow":formula_overflow,"inlineMath":len(inline),
                      "inlineOverflow":sum(item["width"]>item["client"]+2 for item in inline),
                      "figures":len(FIGURES),"figureOverflow":figure_overflow,
                      "boxes":len(BOXES),"shortTails":short_tails,
                      "mathTailCandidates":[item["id"] for item in math_tail_candidates],
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
        print(f"PASS: Appendix B {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, sha256={SHA}, "
              f"screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__=="__main__":
    main()
