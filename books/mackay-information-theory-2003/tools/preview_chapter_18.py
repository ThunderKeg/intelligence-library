"""Check the MacKay chapter 18 draft or registered page in the real reader."""

import argparse
import hashlib
import json
import tempfile
import threading
from collections import Counter
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
PARSER = argparse.ArgumentParser()
PARSER.add_argument("--formal", action="store_true", help="Load unmodified books.js and chapter-18.json")
ARGS = PARSER.parse_args()
DRAFT_BYTES = (BOOK / "chapter-18.draft.json").read_bytes()
DRAFT = json.loads(DRAFT_BYTES.decode("utf-8"))
FORMAL_BYTES = (BOOK / "chapter-18.json").read_bytes() if ARGS.formal else None
if ARGS.formal:
    assert FORMAL_BYTES == DRAFT_BYTES, "Formal chapter 18 differs bytewise from reviewed draft"
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / ("mackay-ch18-formal-qa" if ARGS.formal else "mackay-ch18-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, False), (1440, True), (390, False), (390, True),
             (350, False), (350, True))
COUNTS = Counter(block["kind"] for block in DRAFT["blocks"])
assert DRAFT["sourcePdfPages"] == [272, 280] and len(DRAFT["blocks"]) == 118
assert len(DRAFT["toc"]) == 6
assert [COUNTS[k] for k in ("figure", "table", "exercise", "footnote", "intro", "formula")] == [6, 5, 3, 1, 1, 25]
assert [block["number"] for block in DRAFT["blocks"] if block["kind"] == "formula"] == [f"(18.{i})" for i in range(1, 26)]

BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters18Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const id of ["17", "18"]) {
  const index = chapters18Preview.findIndex(item => item.id === id);
  if (index >= 0) chapters18Preview.splice(index, 1);
}
chapters18Preview.push(
  {id: "17", number: "17", title: "受约束的无噪信道上的通信",
   content: "books/mackay-information-theory-2003/chapter-17.draft.json"},
  {id: "18", number: "18", title: "填字游戏与密码破解",
   content: "books/mackay-information-theory-2003/chapter-18.draft.json"}
);
"""


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def check_blocks(page):
    actual = page.locator(".reading-block").evaluate_all(
        "items => items.map(item => [item.id, [...item.classList].find(c => c.startsWith('reading-') && c !== 'reading-block')])")
    expected = [[f"read-{b['id']}", f"reading-{b['kind']}"] for b in DRAFT["blocks"]]
    assert actual == expected, (actual, expected)
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-heading h2").count() == 5
    assert page.locator(".reading-intro").count() == 1
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    assert page.locator(".book-figure img").count() == 6
    assert page.locator(".book-table").count() == 5
    assert page.locator(".book-exercise-label").all_text_contents() == [
        b["label"] for b in DRAFT["blocks"] if b["kind"] == "exercise"]
    assert page.locator(".book-footnote").count() == 1
    assert "Tony Sale" in page.locator(".book-footnote").inner_text()
    assert page.locator(".book-formula math").count() == 25
    assert page.locator(".formula-number").all_text_contents() == [f"(18.{i})" for i in range(1, 26)]
    assert page.locator("math merror, .formula-fallback").count() == 0
    for block in DRAFT["blocks"]:
        segments = block.get("segments", [])
        expected_em = [segment["text"] for segment in segments
                       if isinstance(segment, dict) and segment.get("em")]
        if expected_em:
            node = page.locator(f"#read-{block['id']}")
            if block["kind"] == "exercise":
                node = node.locator(".book-exercise-body")
            assert node.locator("em").all_text_contents() == expected_em, (
                block["id"], expected_em, node.locator("em").all_text_contents())
    return len(actual)


def check_toc(page, width):
    expected = [f"#read-{item['block']}" for item in DRAFT["toc"][1:]]
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").evaluate_all(
            "items => items.map(item => item.hash)") == expected
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("item => item.open")
        link = page.locator("#reader-toc-mobile .toc-section-link").nth(3)
    else:
        link = page.locator("#reader-toc .toc-section-link").nth(3)
    link.click()
    page.wait_for_function("() => location.hash === '#read-p277-b006'")
    if width < 800:
        assert not page.locator("#toc-dialog").evaluate("item => item.open")
    page.evaluate("history.replaceState(null, '', location.pathname + location.search)")


def check_figures(page, width, suffix):
    results = {}
    for block in (b for b in DRAFT["blocks"] if b["kind"] == "figure"):
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        image = node.locator(".book-figure img")
        image.evaluate("item => item.decode()")
        assert image.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
        assert node.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
        media = node.locator(".figure-media")
        metric = media.evaluate("item => ({client: item.clientWidth, scroll: item.scrollWidth})")
        if metric["scroll"] > metric["client"] + 2:
            assert node.locator(".figure-view-hint").is_visible()
            media.evaluate("item => item.scrollLeft = item.scrollWidth")
            assert media.evaluate("item => item.scrollLeft") >= metric["scroll"] - metric["client"] - 2
            media.evaluate("item => item.scrollLeft = 0")
        if width <= 390 and block.get("wide"):
            assert metric["scroll"] > metric["client"] + 2, (block["id"], metric)
        if block["id"] in ("p272-b007", "p274-b015", "p276-b001") or suffix.startswith("350"):
            node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
        results[block["id"]] = metric
    return results


def check_tables(page, suffix):
    results = {}
    for block in (b for b in DRAFT["blocks"] if b["kind"] == "table"):
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        dimensions = node.locator("tr").evaluate_all(
            "rows => rows.map(row => row.cells.length)")
        assert dimensions == [len(row) for row in block["rows"]], (block["id"], dimensions)
        scroller = node.locator(".table-scroll")
        metric = scroller.evaluate("item => ({client: item.clientWidth, scroll: item.scrollWidth})")
        if metric["scroll"] > metric["client"] + 2:
            scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
            assert scroller.evaluate("item => item.scrollLeft") >= metric["scroll"] - metric["client"] - 2
            if block["id"] == "p279-b001":
                node.screenshot(path=str(QA_DIR / f"table-18-9-right-{suffix}.png"))
            scroller.evaluate("item => item.scrollLeft = 0")
        if block["id"] == "p279-b001":
            strings = node.locator("tr:nth-child(n+2) td:last-child").all_text_contents()
            assert [len(item.strip()) for item in strings] == [72, 72, 72], strings
            assert strings[-1].count("*") == 12
            code_metrics = node.locator("tr:nth-child(n+2) td:last-child code").evaluate_all(
                "items => items.map(item => ({lineFragments: item.getClientRects().length, "
                "height: item.getBoundingClientRect().height}))")
            assert all(item["lineFragments"] == 1 for item in code_metrics), (
                "Table 18.9 position strings wrap and lose column alignment", code_metrics)
            if suffix.startswith(("390", "350")):
                assert metric["scroll"] > metric["client"] + 2, metric
                assert "左右滑动" in scroller.evaluate(
                    "item => getComputedStyle(item, '::before').content")
            node.screenshot(path=str(QA_DIR / f"table-18-9-{suffix}.png"))
        elif suffix.startswith(("390", "350")):
            node.screenshot(path=str(QA_DIR / f"table-{block['id']}-{suffix}.png"))
        results[block["id"]] = metric
    return results


def check_formulas(page, width, suffix):
    overflowing = []
    for block in (b for b in DRAFT["blocks"] if b["kind"] == "formula"):
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        metric = node.locator(".book-formula").evaluate("""item => {
          const scroller = item.querySelector('.formula-scroll');
          const number = item.querySelector('.formula-number');
          const hint = item.parentElement.querySelector('.formula-view-hint');
          return {client: scroller.clientWidth, scroll: scroller.scrollWidth,
            separated: number.getBoundingClientRect().left >=
              scroller.getBoundingClientRect().right - 1,
            hint: !!hint && !hint.hidden && getComputedStyle(hint).display !== 'none',
            height: item.getBoundingClientRect().height,
            mathHeight: scroller.querySelector('math').getBoundingClientRect().height};
        }""")
        assert metric["separated"] and metric["height"] >= metric["mathHeight"] - 2, (block["id"], metric)
        if metric["scroll"] > metric["client"] + 2:
            overflowing.append((block["number"], metric))
            if width <= 390:
                assert metric["hint"], (block["id"], metric)
            scroller = node.locator(".formula-scroll")
            scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
            assert scroller.evaluate("item => item.scrollLeft") >= metric["scroll"] - metric["client"] - 2
            scroller.evaluate("item => item.scrollLeft = 0")
        math = node.locator("math")
        math.select_text()
        page.keyboard.press("Control+C")
        copied = page.evaluate("navigator.clipboard.readText()")
        assert len(copied.strip()) >= 2, (block["id"], copied)
        page.evaluate("getSelection().removeAllRanges()")
        if block["number"] in ("(18.15)", "(18.23)", "(18.24)", "(18.25)"):
            node.screenshot(path=str(QA_DIR / f"formula-{block['number'][1:-1]}-{suffix}.png"))
    return overflowing


def check_progress(page):
    mid = page.locator("#read-p276-b003")
    mid.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
    page.wait_for_function("key => JSON.parse(localStorage.getItem(key) || '{}').block === 'read-p276-b003'", arg=PROGRESS_KEY)
    middle = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          const target = document.querySelector('#read-p276-b003');
          return saved.block === 'read-p276-b003' && target &&
            Math.abs(target.getBoundingClientRect().top - 85) <= 2;
        }""", arg=PROGRESS_KEY)
        middle.append(page.evaluate("""() => ({y: Math.round(scrollY),
          top: Math.round(document.querySelector('#read-p276-b003').getBoundingClientRect().top)})"""))
    assert len({item["y"] for item in middle}) == 1, middle
    assert len({item["top"] for item in middle}) == 1, middle
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""key => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '18' && saved.block === 'read-p280-b006' &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg=PROGRESS_KEY)
    bottom = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""key => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '18' && saved.block === 'read-p280-b006' &&
            document.querySelector('#reading-progress').style.width === '100%' &&
            scrollY > 0 && Math.abs(scrollY + innerHeight - document.documentElement.scrollHeight) <= 2;
        }""", arg=PROGRESS_KEY)
        bottom.append(page.evaluate("""() => ({y: Math.round(scrollY),
          top: Math.round(document.querySelector('#read-p280-b006').getBoundingClientRect().top),
          width: document.querySelector('#reading-progress').style.width})"""))
    assert len({item["y"] for item in bottom}) == 1, bottom
    assert len({item["top"] for item in bottom}) == 1, bottom
    return middle, bottom


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/"

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        for width, dark in VIEWPORTS:
            mode = "dark" if dark else "light"
            suffix = f"{width}-{mode}"
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme=mode,
                service_workers="block",
                permissions=["clipboard-read", "clipboard-write"],
            )
            if not ARGS.formal:
                context.route("**/books.js", lambda route: route.fulfill(
                    body=BOOK_SCRIPT, content_type="application/javascript"))
            page = context.new_page()
            errors, failed_resources = [], []
            responses = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("response", lambda response: responses.append(response))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=18")
            page.locator("#read-p280-b006").wait_for()
            if ARGS.formal:
                for path, expected in (("/books.js", (ROOT / "books.js").read_bytes()),
                                       ("/books/mackay-information-theory-2003/chapter-18.json", FORMAL_BYTES)):
                    matches = [response for response in responses if response.url.endswith(path)]
                    assert len(matches) == 1 and matches[0].status == 200, (path, matches)
                    assert matches[0].body() == expected, f"Browser did not load repository {path} bytes"
            blocks = check_blocks(page)
            check_toc(page, width)
            nav = page.locator("#chapter-navigation .chapter-navigation-link")
            assert nav.count() == 1 and "chapter=17" in nav.first.get_attribute("href")
            page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
            page.screenshot(path=str(QA_DIR / f"top-{suffix}.png"))
            figures = check_figures(page, width, suffix)
            tables = check_tables(page, suffix)
            formulas = check_formulas(page, width, suffix)
            page.locator("#read-fn-18-1").scroll_into_view_if_needed()
            page.locator("#read-fn-18-1").screenshot(path=str(QA_DIR / f"footnote-{suffix}.png"))
            if width == 350:
                for exercise in DRAFT["blocks"]:
                    if exercise["kind"] == "exercise":
                        page.locator(f"#read-{exercise['id']}").screenshot(
                            path=str(QA_DIR / f"exercise-{exercise['id']}-{suffix}.png"))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            middle, bottom = check_progress(page)
            page.screenshot(path=str(QA_DIR / f"bottom-{suffix}.png"))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            nav.click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=17" in page.url
            if ARGS.formal:
                next_links = page.locator("#chapter-navigation .chapter-navigation-link")
                chapter18_links = next_links.filter(has_text="18 填字游戏与密码破解")
                assert chapter18_links.count() == 1, next_links.all_text_contents()
                assert "chapter=18" in chapter18_links.first.get_attribute("href")
                chapter18_links.first.click()
                page.locator("#read-p280-b006").wait_for()
                assert "chapter=18" in page.url
                assert page.locator(".reading-block").count() == 118
            print(json.dumps({
                "viewport": suffix, "blocks": blocks, "figures": figures,
                "tables": tables, "formula_overflow": formulas,
                "middle": middle, "bottom": bottom,
                "errors": errors, "failed_resources": failed_resources,
            }, ensure_ascii=False))
            context.close()
        browser.close()
    print(f"PASS: chapter 18 {'registered page' if ARGS.formal else 'unpublished draft'}, six viewports, "
          f"sha256={hashlib.sha256(DRAFT_BYTES).hexdigest()}, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
