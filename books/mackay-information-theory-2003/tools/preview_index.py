"""Independent six-viewport Edge QA for MacKay index (PDF632–640)."""

from argparse import ArgumentParser
from collections import Counter
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
from pathlib import Path
import re
import tempfile
import threading
from urllib.parse import parse_qs, urlsplit

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

DRAFT = (BOOK / "chapter-IDX.draft.json").read_bytes()
SHA = hashlib.sha256(DRAFT).hexdigest()
assert SHA == ARGS.sha256.lower(), ("Frozen index changed", SHA)
FORMAL = (BOOK / "chapter-IDX.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL == DRAFT, "Formal index differs from reviewed draft"
CHAPTER = json.loads((FORMAL if ARGS.formal else DRAFT).decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
GROUPS = BLOCKS[1:]
KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"

assert CHAPTER["bookId"] == "mackay-information-theory-2003"
assert CHAPTER["sourcePdfPages"] == [632, 640]
assert CHAPTER["toc"] == [{"number": "", "title": "索引", "block": "p632-b001"}]
assert BLOCKS[0]["kind"] == "heading" and BLOCKS[0]["level"] == 1
assert BLOCKS[0]["id"] == "p632-b001" and BLOCKS[0]["text"] == "索引"
assert all(block["kind"] == "rich" for block in GROUPS)
assert len(BLOCKS)==1150
assert len({block["id"] for block in BLOCKS}) == len(BLOCKS)
assert [block["pdfPage"] for block in BLOCKS] == sorted(
    block["pdfPage"] for block in BLOCKS)
assert set(block["pdfPage"] for block in GROUPS) == set(range(632, 641))
assert all(isinstance(block.get("indexColumns"), list)
           and block["indexColumns"]
           and all(column in ("左", "中", "右")
                   for column in block["indexColumns"])
           and block["indexEntryCount"] >= 1 for block in GROUPS)
assert [(block["id"], block["indexColumns"]) for block in GROUPS
        if len(block["indexColumns"]) > 1] == [("p633-b047", ["左", "中"])]
assert all(len(re.findall(r'<p id="idx-p\d+-e\d+"', block["html"])) ==
           block["indexEntryCount"] for block in GROUPS)
ENTRY_COUNT = sum(block["indexEntryCount"] for block in GROUPS)
assert ENTRY_COUNT==1599
PER_PAGE = Counter(block["pdfPage"] for block in GROUPS)
assert all(PER_PAGE[page] >= 3 for page in range(632, 641))
LAST_ID = BLOCKS[-1]["id"]


def chapter_routes():
    source = (ROOT / "books.js").read_text(encoding="utf-8")
    marker = 'id: "mackay-information-theory-2003"'
    assert source.count(marker) == 1
    section = source.split(marker, 1)[1].split('\n  {\n    id: "', 1)[0]
    return dict(re.findall(
        r'\{\s*id:\s*"([\w-]+)"[^{}]*?content:\s*"'
        r'(books/mackay-information-theory-2003/chapter-[\w-]+\.json)"\s*\}',
        section))


ROUTES = chapter_routes()
assert "REF" in ROUTES
BOOK_SCRIPT = None if ARGS.formal else (ROOT / "books.js").read_text(
    encoding="utf-8") + """
const indexPreview = books.find(x => x.id === "mackay-information-theory-2003").chapters;
const existing = indexPreview.findIndex(x => x.id === "IDX");
if (existing >= 0) indexPreview.splice(existing, 1);
const afterREF = indexPreview.findIndex(x => x.id === "REF");
if (afterREF < 0) throw Error("Bibliography must precede index");
indexPreview.splice(afterREF+1, 0,
  {id:"IDX",number:"书后",title:"索引",
   content:"books/mackay-information-theory-2003/chapter-IDX.draft.json"});
"""
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-index-formal-qa" if ARGS.formal else "mackay-index-draft-qa")
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
      return {id:item.id,hasMath:!!item.querySelector('math'),
        lines:[...lines.entries()].sort((a,b)=>a[0]-b[0])
          .map(([_,line])=>line.trim()).filter(Boolean)};
    })""")


def target_ids():
    result = {}
    for chapter_id, relative in ROUTES.items():
        path = ROOT / relative
        assert path.is_file(), path
        data = json.loads(path.read_text(encoding="utf-8"))
        ids = set()
        stack = list(data["blocks"])
        while stack:
            block = stack.pop()
            ids.add(f"read-{block['id']}")
            stack.extend(block.get("blocks", []))
        result[chapter_id] = ids
    return result


TARGET_IDS = target_ids()


def bottom_progress(page):
    page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    wait_for_bottom="""data => {
      const saved=JSON.parse(localStorage.getItem(data.key)||'{}');
      return saved.chapter==='IDX'&&saved.page===640&&
        saved.block==='read-'+data.last&&
        document.querySelector('#reading-progress').style.width==='100%';
    }"""
    page.wait_for_function(wait_for_bottom,arg={"key":KEY,"last":LAST_ID},timeout=10000)
    positions=[]
    for _ in range(3):
        page.reload()
        page.wait_for_function(wait_for_bottom,arg={"key":KEY,"last":LAST_ID},timeout=10000)
        page.wait_for_timeout(300)
        position=page.evaluate("""data => {
          const saved=JSON.parse(localStorage.getItem(data.key)||'{}');
          const top=document.getElementById('read-'+data.last).getBoundingClientRect().top;
          return {y:Math.round(scrollY),top:Math.round(top),
            gap:Math.round(document.documentElement.scrollHeight-scrollY-innerHeight),
            block:saved.block,progress:document.querySelector('#reading-progress').style.width};
        }""", {"key":KEY,"last":LAST_ID})
        assert position["block"]==f"read-{LAST_ID}" and position["progress"]=="100%",position
        assert position["gap"]<=64 and position["top"]<844,position
        positions.append(position)
    assert max(item["y"] for item in positions)-min(item["y"] for item in positions)<=64,positions
    return positions


def click_samples(page, base, width, mode):
    if (width,mode) not in ((1440,"light"),(320,"dark")):
        return 0
    tested=0
    index_url=base+"?book=mackay-information-theory-2003&chapter=IDX"
    labels=("xi","xii","148","574") if width==1440 else ("xii","148")
    for label in labels:
        link=page.locator(f'.reading-rich a.reading-reference[title="原书印刷页 {label}"]').first
        assert link.count()==1,label
        href=link.get_attribute("href")
        parsed=urlsplit(href)
        target=parse_qs(parsed.query)["chapter"][0]
        link.click()
        page.wait_for_function("""data =>
          new URLSearchParams(location.search).get('chapter')===data.chapter &&
          location.hash==='#'+data.anchor""",
          arg={"chapter":target,"anchor":parsed.fragment})
        page.locator(f"#{parsed.fragment}").wait_for()
        page.goto(index_url)
        page.locator(f"#read-{LAST_ID}").wait_for()
        tested+=1
    see=page.locator('.reading-rich a.reading-reference[href^="#"]').first
    assert see.count()==1
    target=see.get_attribute("href")
    see.click()
    page.wait_for_function("anchor=>location.hash===anchor",arg=target)
    assert page.locator(target).count()==1
    page.goto(index_url)
    page.locator(f"#read-{LAST_ID}").wait_for()
    return tested+1


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
    page.goto(base+"?book=mackay-information-theory-2003&chapter=IDX")
    page.locator(f"#read-{LAST_ID}").wait_for()
    expected_json="chapter-IDX.json" if ARGS.formal else "chapter-IDX.draft.json"
    assert any(url.endswith("/books.js") for url in requests)
    assert any(url.endswith("/"+expected_json) for url in requests)
    if ARGS.formal:
        assert not any(url.endswith("chapter-IDX.draft.json") for url in requests)
    assert page.evaluate("document.documentElement.dataset.theme")==mode
    rendered=page.locator(".reading-block").evaluate_all("""items => items.map(node=>
      [node.id,[...node.classList].find(name=>
        name.startsWith('reading-')&&name!=='reading-block')])""")
    assert rendered==[[f"read-{block['id']}",f"reading-{block['kind']}"]
                     for block in BLOCKS]
    h1=page.locator("#read-p632-b001 h1")
    assert h1.inner_text()=="索引"
    assert h1.evaluate("node=>getComputedStyle(node).textAlign")=="center"
    assert h1.evaluate("node=>getComputedStyle(node).fontStyle")=="italic"
    assert h1.evaluate("node=>parseFloat(getComputedStyle(node).borderTopWidth)")>=2.5
    h1.screenshot(path=str(QA_DIR/f"heading-{name}.png"))
    rendered_counts=page.locator(".reading-rich").evaluate_all("""items=>items.map(node=>
      node.querySelectorAll('p.index-entry,p.index-subentry').length)""")
    assert rendered_counts==[group["indexEntryCount"] for group in GROUPS]
    assert page.locator(".reading-rich math").count()==19
    assert page.locator(".reading-rich strong").count()==70
    assert page.locator(".reading-rich code").count()==9
    assert page.locator("math merror,.formula-fallback").count()==0
    assert page.locator(".book-formula,.book-figure,.book-table,.book-exercise,.book-footnote").count()==0
    for selector in ("#reader-toc","#reader-toc-mobile"):
        assert page.locator(
            f"{selector} .toc-chapter-link.chapter-current[href='#read-p632-b001']").count()==1
        assert page.locator(f"{selector} .toc-section-link").count()==0
        assert page.locator(f"{selector} .toc-chapter-link[href$='chapter=REF']").count()==1
    if width<800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node=>node.open")
        page.locator("#toc-close").click()
    links=page.locator(".reading-rich a.reading-reference").evaluate_all(
        "items=>items.map(node=>node.getAttribute('href'))")
    own_ids=set(page.locator("#reader-article [id]").evaluate_all(
        "items=>items.map(node=>node.id)"))
    cross_refs=page_refs=0
    for href in links:
        url=urlsplit(href)
        if not url.query:
            assert url.fragment in own_ids,("unresolved index see",href)
            cross_refs+=1
        else:
            query=parse_qs(url.query)
            assert query.get("book")==["mackay-information-theory-2003"],href
            chapter_id=query.get("chapter",[None])[0]
            assert url.fragment in TARGET_IDS[chapter_id],("unresolved printed page",href)
            page_refs+=1
    assert (page_refs,cross_refs)==(2435,101),(page_refs,cross_refs)
    short_tails=[]
    math_tail_candidates=[]
    if ARGS.scan_tail:
        lines=text_lines(page,".reading-rich p.index-entry,.reading-rich p.index-subentry")
        short_tails=[item for item in lines if not item["hasMath"]
                     and len(item["lines"])>1 and len(item["lines"][-1])<=2]
        math_tail_candidates=[item for item in lines if item["hasMath"]
                              and len(item["lines"])>1 and len(item["lines"][-1])<=2]
        for item in short_tails+math_tail_candidates:
            page.locator(f"#{item['id']}").screenshot(
                path=str(QA_DIR/f"tail-{item['id']}-{name}.png"))
        if ARGS.strict_tail:
            assert not short_tails,(name,short_tails)
    for pdf_page in range(632,641):
        page_groups=[block for block in GROUPS if block["pdfPage"]==pdf_page]
        for group in (page_groups[0],page_groups[-1]):
            page.locator(f"#read-{group['id']}").screenshot(
                path=str(QA_DIR/f"group-{group['id']}-{name}.png"))
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
    for fraction,label in ((0,"top"),(.33,"upper"),(.66,"lower"),(1,"bottom")):
        page.evaluate("fraction=>window.scrollTo({top:document.documentElement.scrollHeight*fraction,behavior:'instant'})",fraction)
        page.screenshot(path=str(QA_DIR/f"viewport-{name}-{label}.png"))
    positions=bottom_progress(page)
    clicked=click_samples(page,base,width,mode)
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=REF']").click()
    page.locator("#read-p631-b045").wait_for()
    page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=IDX']").click()
    page.locator(f"#read-{LAST_ID}").wait_for()
    assert not errors and not failed,(errors,failed)
    context.close()
    print(json.dumps({"viewport":name,"blocks":len(rendered),"entries":ENTRY_COUNT,
                      "toc":1,"pageRefs":page_refs,"seeLinks":cross_refs,
                      "clickedLinks":clicked,
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
        print(f"PASS: index {'formal' if ARGS.formal else 'draft'} "
              f"{'selected' if ARGS.only else 'six'}-viewport QA, sha256={SHA}, "
              f"screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
