"""Independent six-viewport Edge QA for MacKay chapter 49.

Structure is locked from the frozen draft before final acceptance.
Draft mode inserts the chapter only into the browser's books.js response;
formal mode uses the original books.js and registered JSON.
"""

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
parser.add_argument("--sha256", required=True)
parser.add_argument("--only", choices=("1440-light", "1440-dark", "390-light",
                                       "390-dark", "320-light", "320-dark"))
parser.add_argument("--scan-tail", action="store_true")
parser.add_argument("--strict-tail", action="store_true")
args = parser.parse_args()
draft = (BOOK / "chapter-49.draft.json").read_bytes()
sha = hashlib.sha256(draft).hexdigest()
assert sha == args.sha256.lower(), ("Frozen draft changed", sha)
formal = (BOOK / "chapter-49.json").read_bytes() if args.formal else None
if args.formal:
    assert formal == draft, "Registered JSON differs from reviewed draft"
chapter = json.loads((formal if args.formal else draft).decode("utf-8"))
blocks = chapter["blocks"]


def walk(items):
    for block in items:
        yield block
        yield from walk(block.get("blocks", []))


all_blocks = list(walk(blocks))
formulas = [block for block in all_blocks if block["kind"] == "formula"]
figures = [block for block in all_blocks if block["kind"] in ("figure","image")]
tables = [block for block in all_blocks if block["kind"] == "table"]
boxes = [block for block in all_blocks if block["kind"] == "box"]
lists = [block for block in all_blocks if block["kind"] == "list"]
footnotes = [block for block in all_blocks if block["kind"] == "footnote"]
exercises = [block for block in all_blocks if block["kind"] == "exercise"]
headings = [block for block in all_blocks if block["kind"] == "heading"]
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
assert chapter["sourcePdfPages"] == [594,599]
assert len(blocks)==62 and len(all_blocks)==65
assert len(chapter["toc"])==6 and len(headings)==6
assert len(figures)==9 and len(tables)==0
assert len(formulas)==11 and len(exercises)==1 and len(lists)==3
assert len(boxes)==1 and len(footnotes)==0
assert blocks[0]["id"] == "p594-b001" and blocks[0]["kind"] == "heading"
assert blocks[0]["text"] == "第 49 章　重复—累积码"
assert blocks[0]["pdfPage"] == 594
assert last["pdfPage"] == chapter["sourcePdfPages"][1]
assert last["id"]=="p599-b008"
assert len({block["id"] for block in all_blocks}) == len(all_blocks)
assert all(594 <= block["pdfPage"] <= 599 for block in all_blocks)
assert [sum(block["pdfPage"]==page for block in blocks)
        for page in range(594,600)]==[9,7,7,11,20,8]
toc_heading_ids=[entry["block"] for entry in chapter["toc"]]
assert toc_heading_ids==[
    block["id"] for block in headings if block["id"] in toc_heading_ids]
assert [entry["number"] for entry in chapter["toc"][1:]]==[
    f"49.{index}" for index in range(1,6)]
assert boxes[0]["id"]=="box-49-encoder"
assert boxes[0]["pdfPage"]==594 and boxes[0].get("outlined")
assert [block["id"] for block in boxes[0]["blocks"]]==[
    "p594-b006","p594-b007","p594-b008"]
assert [len(block["items"]) for block in boxes[0]["blocks"]
        if block["kind"]=="list"]==[4,1]
assert any(block["pdfPage"]==597 and len(block["items"])==5 for block in lists)
numbered=[block["number"] for block in formulas if block.get("number")]
assert numbered==[f"(49.{index})" for index in range(1,12)]
assert [block["src"] for block in figures]==[
    f"assets/chapter-49/figure-49-{index}.png" for index in range(1,10)]
assert inline_count(blocks) == 102
assert exercises[0]["label"].startswith("习题 49.1")

if args.formal:
    book_script = None
else:
    book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const ch49Preview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = ch49Preview.findIndex(x => x.id === "49");
if (existing >= 0) ch49Preview.splice(existing,1);
const after48 = ch49Preview.findIndex(x => x.id === "48");
if (after48 < 0) throw Error("Chapter 48 must precede chapter 49");
ch49Preview.splice(after48+1,0,
  {id:"49",number:"49",title:"重复—累积码",
   content:"books/mackay-information-theory-2003/chapter-49.draft.json"});
"""

screenshots = Path(tempfile.gettempdir()) / (
    "mackay-ch49-formal-qa" if args.formal else "mackay-ch49-draft-qa")
screenshots.mkdir(exist_ok=True)
viewports = ((1440,"light"),(1440,"dark"),(390,"light"),
             (390,"dark"),(320,"light"),(320,"dark"))


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
    if metric["width"] > metric["client"]+2:
        node.evaluate("node => node.scrollLeft=node.scrollWidth")
        assert node.evaluate("node => node.scrollLeft") >= (
            metric["width"]-metric["client"]-2), metric
        node.evaluate("node => node.scrollLeft=0")
    return metric


def text_lines(page, selector):
    return page.locator(selector).evaluate_all("""items => items.map(item => {
      const lines = new Map();
      const walker = document.createTreeWalker(item,NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        for (let i=0;i<node.length;i++) {
          const range = document.createRange();
          range.setStart(node,i);range.setEnd(node,i+1);
          const rect = range.getBoundingClientRect();
          if (rect.width<.1||rect.height<.1) continue;
          const top = Math.round(rect.top);
          lines.set(top,(lines.get(top)||'')+node.textContent[i]);
        }
      }
      return {id:item.closest('.reading-block')?.id,
        lines:[...lines.entries()].sort((a,b)=>a[0]-b[0])
          .map(([_,line])=>line.trim()).filter(Boolean)};
    })""")


def bottom_progress(page):
    target = f"read-{last['id']}"
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    page.wait_for_function("""({key,target,pdfPage}) => {
      const saved=JSON.parse(localStorage.getItem(key)||'{}');
      return saved.chapter==='49'&&saved.page===pdfPage&&saved.block===target&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""",arg={"key":progress_key,"target":target,"pdfPage":last["pdfPage"]})
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key,target,pdfPage}) => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='49'&&saved.page===pdfPage&&saved.block===target&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""",arg={"key":progress_key,"target":target,"pdfPage":last["pdfPage"]})
        positions.append(page.evaluate("""target => ({
          y:Math.round(scrollY),
          top:Math.round(document.getElementById(target).getBoundingClientRect().top)
        })""",target))
    assert len({tuple(position.values()) for position in positions})==1,positions
    return positions


def inspect(browser, base, width, mode):
    name=f"{width}-{mode}"
    context=browser.new_context(viewport={"width":width,"height":844},
                                color_scheme=mode,service_workers="block",
                                permissions=["clipboard-read","clipboard-write"])
    if not args.formal:
        context.route("**/books.js",lambda route:route.fulfill(
            body=book_script,content_type="application/javascript"))
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
    page.goto(base+"?book=mackay-information-theory-2003&chapter=49")
    page.locator(f"#read-{last['id']}").wait_for()
    expected_json="chapter-49.json" if args.formal else "chapter-49.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if args.formal:
        assert not any(url.endswith("chapter-49.draft.json") for url in requests)

    actual=page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    expected=[(f"read-{block['id']}",f"reading-{block['kind']}")
              for block in all_blocks if block["kind"]!="box"]
    assert len(actual)==64
    assert actual==[list(item) for item in expected],(
        len(actual),len(expected),[(index,a,b) for index,(a,b) in enumerate(
            zip(actual,expected)) if a!=list(b)][:5])
    assert page.locator("aside.book-box").count()==len(boxes)
    for block in boxes:
        aside=page.locator(f"#read-{block['id']}")
        assert aside.locator(".reading-block").count()==len(block["blocks"])
        assert aside.evaluate("node=>node.classList.contains('outlined-box')")==bool(
            block.get("outlined"))
        assert aside.evaluate("node=>node.classList.contains('algorithm-box')")==bool(
            block.get("algorithm"))
        horizontal_scroll(aside)
        if block.get("algorithm") and width<800:
            assert aside.locator(".algorithm-view-hint").is_visible()
        if (width,mode) in ((1440,"light"),(320,"dark")):
            aside.screenshot(path=str(screenshots/f"box-{block['id']}-{name}.png"))
    assert page.locator(".reading-heading h1").inner_text().replace("\n","")==blocks[0]["text"]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current[href='#read-p594-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link").count()==len(chapter["toc"])-1
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=48']").count()==1
    if width<800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()

    heading_lines=text_lines(page,".reading-heading h1,.reading-heading h2,.reading-heading h3")
    toc_by_block={entry["block"]:entry for entry in chapter["toc"]}
    for block in headings:
        rendered=page.locator(
            f"#read-{block['id']} h1,#read-{block['id']} h2,#read-{block['id']} h3").inner_text()
        number=toc_by_block.get(block["id"],{}).get("number")
        if number and re.fullmatch(r"49\.\d+",number):
            assert "▶" in block.get("html", ""),(block["id"],number)
            icon=page.locator(f"#read-{block['id']} h2 [aria-hidden='true']")
            assert icon.count()==1 and icon.inner_text()=="▶"
            assert rendered.endswith(block["text"])
        else:
            assert rendered.replace("\n","")==block["text"]
    if width<800:
        for heading in headings:
            page.locator(f"#read-{heading['id']}").screenshot(
                path=str(screenshots/f"heading-{heading['id']}-{name}.png"))
    short_tails=[]
    if args.scan_tail:
        for item in text_lines(page,
                ".reading-paragraph p, "
                ".figure-caption p, "
                ".book-exercise"):
            if (len(item["lines"])>1 and len(item["lines"][-1])<=2
                    and re.search(r"[\u4e00-\u9fff。！？：；，、]$",item["lines"][-1])):
                short_tails.append({"id":item["id"],"tail":item["lines"][-1]})
        for item in short_tails:
            if item["id"]:
                page.locator(f"#{item['id']}").screenshot(
                    path=str(screenshots/f"short-tail-{item['id']}-{name}.png"))
        if args.strict_tail:
            assert not short_tails,(name,short_tails)

    assert page.locator(".book-formula math").count()==len(formulas)
    encoder_rows=page.locator("#read-p594-b007 math mtr")
    assert encoder_rows.count()==4
    assert all("," not in encoder_rows.nth(index).text_content()
               for index in (0,1))
    assert "." in encoder_rows.nth(3).text_content()
    assert page.locator(".inline-math math").count()==inline_count(blocks)
    assert page.locator(".book-figure img").count()==len(figures)
    assert page.locator(".book-table").count()==len(tables)
    assert page.locator(".book-exercise-label").count()==len(exercises)
    assert page.locator("math merror,.formula-fallback,.figure-error").count()==0
    assert page.locator(".reading-list .book-list").count()==len(lists)
    for block in lists:
        tag="ol" if block.get("ordered") else "ul"
        item=page.locator(f"#read-{block['id']} {tag}.book-list")
        assert item.count()==1
        if block.get("ordered"):
            assert item.evaluate("node=>node.start")==block.get("start",1)
        assert item.locator(":scope > li").count()==len(block["items"])
        if (width,mode) in ((1440,"light"),(320,"dark")):
            page.locator(f"#read-{block['id']}").screenshot(
                path=str(screenshots/f"list-{block['id']}-{name}.png"))
    assert page.locator(".book-footnote").count()==len(footnotes)
    for block in footnotes:
        item=page.locator(f"#read-{block['id']} .book-footnote")
        assert item.count()==1
        for segment in block.get("segments",[]):
            if isinstance(segment,dict) and segment.get("href","").startswith("http"):
                link=item.locator("a")
                assert link.get_attribute("href")==segment["href"]
                assert link.get_attribute("rel")=="noopener noreferrer"
    expected_refs=[segment["href"] for block in all_blocks
                   for segment in block.get("segments",[])
                   if isinstance(segment,dict) and segment.get("footnote")]
    assert page.locator(".book-footnote-ref a").evaluate_all(
        "items=>items.map(node=>node.getAttribute('href'))")==expected_refs
    if (width,mode) in ((1440,"light"),(320,"dark")):
        for block in footnotes:
            page.locator(f"#read-{block['id']}").screenshot(
                path=str(screenshots/f"footnote-{block['id']}-{name}.png"))

    formula_overflow,formula_metrics,copied=[],[],0
    for block in formulas:
        item=page.locator(f"#read-{block['id']}")
        if block.get("number"):
            assert item.locator(".formula-number").inner_text()==block["number"]
            assert item.locator(".book-formula").evaluate("""node=>
              node.querySelector('.formula-number').getBoundingClientRect().left>=
              node.querySelector('.formula-scroll').getBoundingClientRect().right-1""")
        else:
            assert item.locator(".formula-number").count()==0
        assert item.locator("math").count()==1
        metric=horizontal_scroll(item.locator(".formula-scroll"))
        formula_metrics.append((block,metric))
        if metric["width"]>metric["client"]+2:
            formula_overflow.append(block.get("number") or block["id"])
            assert item.locator(".formula-view-hint").is_visible()
        if (width,mode) in ((1440,"light"),(320,"dark")):
            item.locator("math").scroll_into_view_if_needed()
            item.locator("math").select_text()
            page.keyboard.press("Control+C")
            clipboard=page.evaluate("navigator.clipboard.readText()").strip()
            assert clipboard
            page.evaluate("getSelection().removeAllRanges()")
            copied+=1
    if formulas and (width,mode) in ((1440,"light"),(320,"dark")):
        widest=max(formula_metrics,key=lambda pair:pair[1]["width"])
        item=page.locator(f"#read-{widest[0]['id']}")
        item.screenshot(path=str(screenshots/f"formula-wide-{name}.png"))
        if width<800:
            scroll=item.locator(".formula-scroll")
            scroll.evaluate("node=>node.scrollLeft=node.scrollWidth")
            scroll.screenshot(path=str(screenshots/f"formula-wide-{name}-right.png"))
            scroll.evaluate("node=>node.scrollLeft=0")
    for block in exercises:
        assert block["label"] in page.locator(f"#read-{block['id']}").inner_text()

    figure_overflow=[]
    for block in figures:
        item=page.locator(f"#read-{block['id']}")
        image=item.locator(".book-figure img")
        image.scroll_into_view_if_needed()
        image.evaluate("node=>node.decode()")
        assert image.evaluate("node=>[node.naturalWidth,node.naturalHeight]")==[
            block["width"],block["height"]]
        assert image.get_attribute("alt")==block["alt"]
        assert item.locator(".figure-caption").count()==int(bool(
            block.get("caption") or block.get("annotations")))
        assert item.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
        metric=horizontal_scroll(item.locator(".figure-media"))
        if width<800 and block.get("wide"):
            assert metric["width"]>metric["client"]+2
            assert item.locator(".figure-view-hint").is_visible()
        if metric["width"]>metric["client"]+2:
            figure_overflow.append(block["id"])
        if (width,mode) in ((1440,"light"),(320,"dark")):
            item.screenshot(path=str(screenshots/f"figure-{block['id']}-{name}.png"))
        if width<800 and block.get("wide"):
            media=item.locator(".figure-media")
            media.evaluate("node=>node.scrollLeft=node.scrollWidth")
            assert media.evaluate("node=>node.scrollLeft>0")
            media.screenshot(path=str(screenshots/f"figure-media-{block['id']}-{name}-right.png"))
            item.screenshot(path=str(screenshots/f"figure-{block['id']}-{name}-right.png"))
            media.evaluate("node=>node.scrollLeft=0")

    algorithm=page.locator(f"#read-{boxes[0]['id']}")
    assert "就这样" in algorithm.inner_text()
    algorithm_copied=False
    if (width,mode) in ((1440,"light"),(320,"dark")):
        algorithm.select_text()
        page.keyboard.press("Control+C")
        assert "就这样" in page.evaluate("navigator.clipboard.readText()")
        page.evaluate("getSelection().removeAllRanges()")
        algorithm_copied=True

    table_metrics=[]
    for block in tables:
        item=page.locator(f"#read-{block['id']}")
        rows=item.locator(".book-table tr")
        expected_rows=len(block.get("rows",[]))+int(bool(block.get("headers")))
        assert rows.count()==expected_rows,(block["id"],rows.count(),expected_rows)
        source_rows=([block["headers"]] if block.get("headers") else [])+block.get("rows",[])
        for index,source_cells in enumerate(source_rows):
            cells=rows.nth(index).locator("th,td")
            assert cells.count()==len(source_cells),(block["id"],index)
            for cell_index,source_cell in enumerate(source_cells):
                source_cell=source_cell if isinstance(source_cell,dict) else {"text":str(source_cell)}
                rendered=cells.nth(cell_index)
                assert rendered.evaluate("node=>node.tagName")==(
                    "TH" if source_cell.get("header") else "TD")
                assert rendered.locator("math").count()==inline_count(
                    source_cell.get("segments",[]))
                expected_colspan=source_cell.get("colspan",1)
                expected_rowspan=source_cell.get("rowspan",1)
                assert rendered.get_attribute("colspan")==(
                    str(expected_colspan) if expected_colspan>1 else None)
                assert rendered.get_attribute("rowspan")==(
                    str(expected_rowspan) if expected_rowspan>1 else None)
                if source_cell.get("text") or source_cell.get("segments"):
                    assert rendered.inner_text().strip()
        metric=horizontal_scroll(item.locator(".table-scroll"))
        table_metrics.append((block["id"],metric["client"],metric["width"]))
        if (width,mode) in ((1440,"light"),(320,"dark")):
            item.screenshot(path=str(screenshots/f"table-{block['id']}-{name}.png"))
        if width<800 and metric["width"]>metric["client"]+2:
            wrapper=item.locator(".table-scroll")
            wrapper.evaluate("node=>node.scrollLeft=node.scrollWidth")
            wrapper.screenshot(path=str(screenshots/f"table-{block['id']}-{name}-right.png"))
            wrapper.evaluate("node=>node.scrollLeft=0")

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
    page.screenshot(path=str(screenshots/f"top-{name}.png"))
    progress=bottom_progress(page)
    if (width,mode) in ((1440,"light"),(320,"dark")):
        page.screenshot(path=str(screenshots/f"bottom-{name}.png"))
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=48']").click()
    page.locator("#read-p593-b012").wait_for()
    assert "chapter=48" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=49']").click()
    page.locator(f"#read-{last['id']}").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(blocks),
                      "recursiveNodes":len(all_blocks),"renderedBlocks":len(actual),
                      "toc":len(chapter["toc"]),
                      "formulas":len(formulas),"copied":copied,
                      "formulaOverflow":formula_overflow,"figures":len(figures),
                      "figureOverflow":figure_overflow,"tables":table_metrics,
                      "algorithmCopied":algorithm_copied,
                      "exercises":len(exercises),"footnotes":len(footnotes),
                      "headings":heading_lines,"shortTails":short_tails,
                      "inlineOverflow":sum(item["width"]>item["client"]+2 for item in inline),
                      "progress":progress,"errors":errors,"failed":failed}),flush=True)


def main():
    server=ThreadingHTTPServer(("127.0.0.1",0),
                               partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(
                headless=True,
                executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            for width,mode in viewports:
                if args.only and f"{width}-{mode}"!=args.only:
                    continue
                inspect(browser,f"http://127.0.0.1:{server.server_port}/",width,mode)
            browser.close()
        print(f"PASS: chapter 49 {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, sha256={sha}, "
              f"screenshots={screenshots}")
    finally:
        server.shutdown()
        server.server_close()


if __name__=="__main__":
    main()
