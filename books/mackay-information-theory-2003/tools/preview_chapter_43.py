"""Independent six-viewport Edge QA for MacKay chapter 43."""

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
args = parser.parse_args()
draft = (BOOK / "chapter-43.draft.json").read_bytes()
sha = hashlib.sha256(draft).hexdigest()
assert sha == args.sha256.lower(), ("Frozen draft changed", sha)
formal = (BOOK / "chapter-43.json").read_bytes() if args.formal else None
if args.formal:
    assert formal == draft, "Registered JSON differs from reviewed draft"
chapter = json.loads((formal if args.formal else draft).decode("utf-8"))
blocks = chapter["blocks"]
box = next(block for block in blocks if block["kind"] == "box")
formulas = [child for block in blocks
            for child in (block["blocks"] if block["kind"] == "box" else [block])
            if child["kind"] == "formula"]
figures = [block for block in blocks if block["kind"] == "figure"]
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
assert chapter["sourcePdfPages"] == [534, 538]
assert len(blocks) == 67 and len(chapter["toc"]) == 4
assert Counter(block["kind"] for block in blocks) == Counter({
    "paragraph":39,"formula":17,"heading":4,"exercise":3,"figure":2,
    "intro":1,"box":1})
assert blocks[0]["id"] == "p534-b001" and blocks[0]["text"] == "第 43 章　玻尔兹曼机"
assert last["id"] == "p538-b006" and last["pdfPage"] == 538
assert [block["number"] for block in formulas] == [
    f"(43.{index})" for index in range(1, 19)]
assert box["id"] == "box-43-activity-rule" and box["outlined"]
assert [child["kind"] for child in box["blocks"]] == [
    "paragraph", "formula", "paragraph"]
assert [child["id"] for child in box["blocks"]] == [
    "p534-b010", "p534-b011", "p534-b012"]
assert [block["src"] for block in figures] == [
    "assets/chapter-43/figure-43-1.png",
    "assets/chapter-43/figure-43-2.png"]
assert [block["label"] for block in exercises] == [
    "习题 43.1", "▷ 习题 43.2", "▷ 习题 43.3"]
assert inline_count(blocks) == 51
assert len({block["id"] for block in blocks}) == len(blocks)
assert all(534 <= block["pdfPage"] <= 538 for block in blocks)

if args.formal:
    book_script = None
else:
    book_script = (ROOT / "books.js").read_text(encoding="utf-8") + """
const ch43Preview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = ch43Preview.findIndex(x => x.id === "43");
if (existing >= 0) ch43Preview.splice(existing,1);
const after42 = ch43Preview.findIndex(x => x.id === "42");
if (after42 < 0) throw Error("Chapter 42 must precede chapter 43");
ch43Preview.splice(after42+1,0,
  {id:"43",number:"43",title:"玻尔兹曼机",
   content:"books/mackay-information-theory-2003/chapter-43.draft.json"});
"""

screenshots = Path(tempfile.gettempdir()) / (
    "mackay-ch43-formal-qa" if args.formal else "mackay-ch43-draft-qa")
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
    target = "read-p538-b006"
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    page.wait_for_function("""({key,target}) => {
      const saved=JSON.parse(localStorage.getItem(key)||'{}');
      return saved.chapter==='43'&&saved.page===538&&saved.block===target&&
        document.querySelector('#reading-progress').style.width==='100%';
    }""",arg={"key":progress_key,"target":target})
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key,target}) => {
          const saved=JSON.parse(localStorage.getItem(key)||'{}');
          return saved.chapter==='43'&&saved.page===538&&saved.block===target&&
            document.querySelector('#reading-progress').style.width==='100%';
        }""",arg={"key":progress_key,"target":target})
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
    page.goto(base+"?book=mackay-information-theory-2003&chapter=43")
    page.locator("#read-p538-b006").wait_for()
    expected_json="chapter-43.json" if args.formal else "chapter-43.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if args.formal:
        assert not any(url.endswith("chapter-43.draft.json") for url in requests)

    actual=page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    expected=[]
    for block in blocks:
        children=block["blocks"] if block["kind"]=="box" else [block]
        expected.extend((f"read-{child['id']}",f"reading-{child['kind']}")
                        for child in children)
    assert actual==[list(item) for item in expected]
    assert page.locator(".reading-heading h1").inner_text()==blocks[0]["text"]
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current[href='#read-p534-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link").count()==3
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=42']").count()==1
    if width<800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()

    headings=text_lines(page,".reading-heading h1,.reading-heading h2")
    for block in (item for item in blocks if item["kind"]=="heading"):
        assert page.locator(f"#read-{block['id']} h1,#read-{block['id']} h2").inner_text()==block["text"]
    for heading_id,terms in (("p534-b003",("网络","玻尔兹曼机")),
                             ("p537-b004",("隐单元","玻尔兹曼机"))):
        lines=next(item["lines"] for item in headings
                   if item["id"]==f"read-{heading_id}")
        assert all(any(term in line for line in lines) for term in terms),(
            heading_id,lines)
    if width<800:
        for heading_id in ("p534-b003","p537-b004"):
            page.locator(f"#read-{heading_id}").screenshot(
                path=str(screenshots/f"heading-{heading_id}-{name}.png"))
    short_tails=[]
    if args.scan_tail:
        for item in text_lines(page,
                ".reading-paragraph p:not(:has(math)), "
                ".figure-caption p:not(:has(math)), "
                ".book-exercise:not(:has(math))"):
            if len(item["lines"])>1 and len(item["lines"][-1])<=2:
                short_tails.append({"id":item["id"],"tail":item["lines"][-1]})
        for item in short_tails:
            if item["id"]:
                page.locator(f"#{item['id']}").screenshot(
                    path=str(screenshots/f"short-tail-{item['id']}-{name}.png"))
        assert not short_tails,(name,short_tails)

    assert page.locator(".book-formula math").count()==18
    assert page.locator(".inline-math math").count()==51
    assert page.locator(".book-figure img").count()==2
    assert page.locator(".book-exercise-label").count()==3
    assert page.locator("math merror,.formula-fallback,.figure-error").count()==0
    box_node=page.locator("#read-box-43-activity-rule")
    assert "outlined-box" in box_node.get_attribute("class")
    assert box_node.locator(".reading-paragraph").count()==2
    assert box_node.locator(".book-formula math").count()==1
    assert box_node.locator(".formula-number").inner_text()=="(43.3)"
    assert "玻尔兹曼机的活动规则" in box_node.inner_text()
    assert "否则将" in box_node.inner_text()
    if (width,mode) in ((1440,"light"),(320,"dark")):
        box_node.screenshot(path=str(screenshots/f"activity-rule-{name}.png"))

    formula_overflow,copied=[],0
    for block in formulas:
        item=page.locator(f"#read-{block['id']}")
        assert item.locator(".formula-number").inner_text()==block["number"]
        assert item.locator("math").count()==1
        assert item.locator(".book-formula").evaluate("""node=>
          node.querySelector('.formula-number').getBoundingClientRect().left>=
          node.querySelector('.formula-scroll').getBoundingClientRect().right-1""")
        metric=horizontal_scroll(item.locator(".formula-scroll"))
        if metric["width"]>metric["client"]+2:
            formula_overflow.append(block["number"])
            assert item.locator(".formula-view-hint").is_visible()
        if (width,mode) in ((1440,"light"),(320,"dark")):
            item.locator("math").scroll_into_view_if_needed()
            item.locator("math").select_text()
            page.keyboard.press("Control+C")
            assert page.evaluate("navigator.clipboard.readText()").strip()
            page.evaluate("getSelection().removeAllRanges()")
            copied+=1
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
        assert item.locator(".figure-caption").count()==1
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
            item.locator(".figure-media").evaluate("node=>node.scrollLeft=node.scrollWidth")
            item.screenshot(path=str(screenshots/f"figure-{block['id']}-{name}-right.png"))
            item.locator(".figure-media").evaluate("node=>node.scrollLeft=0")

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
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=42']").click()
    page.locator("#read-p533-b005").wait_for()
    assert "chapter=42" in page.url
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=43']").click()
    page.locator("#read-p538-b006").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(blocks),"toc":len(chapter["toc"]),
                      "formulas":len(formulas),"copied":copied,
                      "formulaOverflow":formula_overflow,"figures":len(figures),
                      "figureOverflow":figure_overflow,"exercises":len(exercises),
                      "headings":headings,"shortTails":short_tails,
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
        print(f"PASS: chapter 43 {'formal' if args.formal else 'draft'} "
              f"{'selected' if args.only else 'six'}-viewport QA, sha256={sha}, "
              f"screenshots={screenshots}")
    finally:
        server.shutdown()
        server.server_close()


if __name__=="__main__":
    main()
