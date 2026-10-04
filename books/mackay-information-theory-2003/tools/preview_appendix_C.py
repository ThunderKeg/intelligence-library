"""Independent six-viewport Edge QA for MacKay Appendix C (PDF617–624)."""

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
PARSER.add_argument("--strict-local-scroll", action="store_true")
ARGS = PARSER.parse_args()

DRAFT = (BOOK / "chapter-C.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen Appendix C changed", SHA)
FORMAL = (BOOK / "chapter-C.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL == DRAFT, "Formal Appendix C differs from reviewed draft"
CHAPTER = json.loads((FORMAL if ARGS.formal else DRAFT).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]


def walk(blocks):
    for block in blocks:
        yield block
        yield from walk(block.get("blocks", []))


ALL = list(walk(BLOCKS))
FORMULAS = [block for block in ALL if block["kind"] == "formula"]
FIGURES = [block for block in ALL if block["kind"] == "figure"]
TABLES = [block for block in ALL if block["kind"] == "table"]
LISTS = [block for block in ALL if block["kind"] == "list"]
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
assert CHAPTER["sourcePdfPages"] == [617, 624]
assert CHAPTER["toc"] == [
    {"number": "C", "title": "一些数学知识", "block": "p617-b001"},
    {"number": "C.1", "title": "有限域理论", "block": "p617-b003"},
    {"number": "C.2", "title": "特征向量与特征值", "block": "p618-b005"},
    {"number": "C.3", "title": "微扰理论", "block": "p620-b011"},
    {"number": "C.4", "title": "若干数值", "block": "p624-b001"},
]
assert len(BLOCKS) == 125 and len(ALL) == 125 and len(HEADINGS) == 12
assert len(FORMULAS) == 37 and len(FIGURES) == 1 and len(TABLES) == 10
assert len(LISTS) == 3 and sum(len(block["items"]) for block in LISTS) == 9
assert [block["number"] for block in FORMULAS] == [
    f"(C.{index})" for index in range(1, 38)]
assert inline_count(BLOCKS) == 393
assert [block["src"] for block in FIGURES] == [
    "assets/appendix-C/table-C-4-numbers.png"]
assert FIGURES[0].get("wide") and (FIGURES[0]["width"],FIGURES[0]["height"]) == (2500,3020)
assert [len(block["rows"]) for block in TABLES] == [3,5,5,5,9,9,10,6,13,43]
assert [len(block["rows"][0]) for block in TABLES] == [7,5,5,3,3,9,4,4,4,4]
assert sum(len(row) for block in TABLES for row in block["rows"]) == 482
assert sum(bool(block.get("caption")) for block in TABLES) == 6
assert not any(cell.get("header") for row in TABLES[-1]["rows"] for cell in row)
assert BLOCKS[0]["id"] == "p617-b001" and BLOCKS[0]["text"] == "附录 C　一些数学知识"
assert BLOCKS[0]["kind"] == "heading" and BLOCKS[1]["kind"] == "intro"
assert BLOCKS[-1]["id"] == "p624-b003" and BLOCKS[-1]["pdfPage"] == 624
assert len({block["id"] for block in ALL}) == len(ALL)
assert all(617 <= block["pdfPage"] <= 624 for block in ALL)
assert not any(block["kind"] in ("box", "code", "exercise", "footnote", "quote")
               for block in ALL)

BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(
    encoding="utf-8") + """
const appendixCPreview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = appendixCPreview.findIndex(x => x.id === "C");
if (existing >= 0) appendixCPreview.splice(existing, 1);
const afterB = appendixCPreview.findIndex(x => x.id === "B");
if (afterB < 0) throw Error("Appendix B must precede Appendix C");
appendixCPreview.splice(afterB+1, 0,
  {id:"C",number:"C",title:"一些数学知识",
   content:"books/mackay-information-theory-2003/chapter-C.draft.json"});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-appendix-C-formal-qa" if ARGS.formal else "mackay-appendix-C-draft-qa")
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
      return saved.chapter==='C'&&saved.page===624&&
        saved.block==='read-p624-b003'&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""",arg=KEY)
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='C'&&saved.page===624&&
            saved.block==='read-p624-b003'&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""",arg=KEY)
        positions.append(page.evaluate("""() => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById('read-p624-b003').getBoundingClientRect().top)
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
    page.goto(base+"?book=mackay-information-theory-2003&chapter=C")
    page.locator("#read-p624-b003").wait_for()
    expected_json="chapter-C.json" if ARGS.formal else "chapter-C.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if ARGS.formal:
        assert not any(url.endswith("chapter-C.draft.json") for url in requests)
    assert page.evaluate("document.documentElement.dataset.theme")==mode
    rendered=page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    assert rendered==[[f"read-{block['id']}",f"reading-{block['kind']}"]
                     for block in ALL]
    h1=page.locator("#read-p617-b001 h1")
    title=text_lines(page,"#read-p617-b001 h1")[0]["lines"]
    assert title==["附录 C","一些数学知识"],(name,title)
    assert h1.evaluate("node=>getComputedStyle(node).textAlign")=="center"
    assert h1.locator("span").nth(0).evaluate(
        "node=>parseFloat(getComputedStyle(node).borderBottomWidth)")>=2.5
    assert h1.locator("span").nth(1).evaluate(
        "node=>getComputedStyle(node).fontStyle")=="italic"
    assert "编者导读" in page.locator(".reading-intro").inner_text()
    for block in HEADINGS[1:]:
        selector="h2" if block["level"]==2 else "h3"
        heading=page.locator(f"#read-{block['id']} {selector}")
        assert heading.text_content().replace("▶","").replace(" ","")==block["text"].replace(" ","")
        if selector=="h2":
            assert heading.locator("[aria-hidden='true']").inner_text()=="▶"
        else:
            assert heading.evaluate("node=>getComputedStyle(node).fontStyle")=="italic"
    assert page.locator(".reading-list").count()==3
    assert page.locator(".reading-list li").count()==9
    assert page.locator(".book-formula math").count()==37
    assert page.locator(".inline-math math").count()==393
    assert page.locator("math merror,.formula-fallback").count()==0
    assert page.locator(".book-figure img").count()==1
    assert page.locator(".book-table").count()==10
    assert page.locator(".book-exercise,.book-footnote,aside.book-box").count()==0
    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p617-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link").count()==4
        for entry in CHAPTER["toc"][1:]:
            assert page.locator(f"{selector} .toc-section-link[href='#read-{entry['block']}']").count()==1
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=B']").count()==1
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
    visual_spots={1440:("p617-b015","p623-b011"),
                  390:("p619-b005","p618-b009","p619-b017"),
                  320:("p617-b010","p619-b018")}
    if mode=="light" or width==320:
        for block_id in visual_spots[width]:
            page.locator(f"#read-{block_id}").screenshot(
                path=str(QA_DIR/f"spot-{block_id}-{name}.png"))
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
            if block["id"] in ("p622-b014","p623-b010","p623-b014"):
                item.screenshot(path=str(QA_DIR/f"formula-{block['id']}-{name}.png"))
    figure_overflow=[]
    for block in FIGURES:
        item=page.locator(f"#read-{block['id']}")
        image=item.locator(".book-figure img")
        image.scroll_into_view_if_needed()
        image.evaluate("node=>node.decode()")
        dimensions=image.evaluate("node=>({width:node.naturalWidth,height:node.naturalHeight})")
        assert dimensions=={"width":2500,"height":3020}
        assert image.get_attribute("src").endswith(block["src"])
        assert item.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
        assert image.get_attribute("alt")==block["alt"]
        assert item.locator(".figure-caption").count()==0
        metric=horizontal_scroll(item.locator(".figure-media"))
        if metric["width"]>metric["client"]+2:
            figure_overflow.append(block["id"])
            assert item.locator(".figure-view-hint").is_visible()
        if width<800 and ARGS.strict_local_scroll:
            assert metric["width"]>metric["client"]+2,(name,block["id"],metric)
        item.screenshot(path=str(QA_DIR/f"figure-{block['id']}-{name}.png"))
        if width<800 and metric["width"]>metric["client"]+2:
            media=item.locator(".figure-media")
            media.scroll_into_view_if_needed()
            media.evaluate("node=>node.scrollLeft=node.scrollWidth")
            page.screenshot(path=str(QA_DIR/f"figure-viewport-{block['id']}-{name}-right.png"))
            media.evaluate("node=>node.scrollLeft=0")
    table_overflow=[]
    target_wide={"p620-b001","p620-b003","p621-b001","p624-b003"}
    for block in TABLES:
        item=page.locator(f"#read-{block['id']}")
        table=item.locator(".book-table")
        rendered_rows=table.locator("tr").evaluate_all("""rows=>rows.map(row=>
          [...row.cells].map(cell=>({tag:cell.tagName,text:cell.textContent,
            math:cell.querySelectorAll('math').length})))""")
        assert len(rendered_rows)==len(block["rows"]),(block["id"],len(rendered_rows))
        for source_row,rendered_row in zip(block["rows"],rendered_rows):
            assert len(source_row)==len(rendered_row),(block["id"],len(rendered_row))
            for source_cell,rendered_cell in zip(source_row,rendered_row):
                assert rendered_cell["tag"]==("TH" if source_cell.get("header") else "TD")
                math_count=inline_count(source_cell.get("segments",[]))
                assert rendered_cell["math"]==math_count
                if math_count==0:
                    plain="".join(segment if isinstance(segment,str) else
                                  segment.get("text","")
                                  for segment in source_cell.get("segments",[]))
                    assert rendered_cell["text"].strip()==plain.strip(),(
                        block["id"],rendered_cell["text"],plain)
        assert table.locator("caption").count()==int(bool(block.get("caption")))
        metric=horizontal_scroll(item.locator(".table-scroll"))
        if metric["width"]>metric["client"]+2:
            table_overflow.append(block["id"])
        require_local=block["id"] in target_wide and (width<=360 or block["id"]!="p624-b003")
        if width<800 and require_local and ARGS.strict_local_scroll:
            assert metric["width"]>metric["client"]+2,(name,block["id"],metric)
        if block["id"] in target_wide:
            item.screenshot(path=str(QA_DIR/f"table-{block['id']}-{name}.png"))
            if width<800 and metric["width"]>metric["client"]+2:
                wrapper=item.locator(".table-scroll")
                wrapper.scroll_into_view_if_needed()
                wrapper.evaluate("node=>node.scrollLeft=node.scrollWidth")
                page.screenshot(path=str(QA_DIR/f"table-viewport-{block['id']}-{name}-right.png"))
                wrapper.evaluate("node=>node.scrollLeft=0")
    assert page.locator("#read-p624-b003 .book-table tr").count()==43
    assert page.locator("#read-p624-b003 .book-table th").count()==0
    unix=page.locator("#read-p624-b003 .book-table code")
    assert unix.count()==1 and unix.inner_text()=="unix"
    assert "mono" in unix.evaluate("node=>getComputedStyle(node).fontFamily").lower()
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
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=B']").click()
    page.locator("#read-p616-b002").wait_for()
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=C']").click()
    page.locator("#read-p624-b003").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(rendered),"toc":5,
                      "formulas":len(FORMULAS),"formulaCopied":copied,
                      "formulaOverflow":formula_overflow,"inlineMath":len(inline),
                      "inlineOverflow":sum(item["width"]>item["client"]+2 for item in inline),
                      "figures":len(FIGURES),"figureOverflow":figure_overflow,
                      "tables":len(TABLES),"tableOverflow":table_overflow,
                      "shortTails":short_tails,
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
        print(f"PASS: Appendix C {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, sha256={SHA}, "
              f"screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__=="__main__":
    main()
