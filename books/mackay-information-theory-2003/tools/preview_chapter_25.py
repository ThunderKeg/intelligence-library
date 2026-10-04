"""Inspect chapter 25 in the reader; use --formal after registration."""

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
arguments = ArgumentParser()
arguments.add_argument("--formal", action="store_true")
FORMAL = arguments.parse_args().formal
DRAFT_BYTES = (BOOK / "chapter-25.draft.json").read_bytes()
FORMAL_BYTES = (BOOK / "chapter-25.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
TABLES = [block for block in BLOCKS if block["kind"] == "table"]
LISTS = [block for block in BLOCKS if block["kind"] == "list"]
assert CHAPTER["sourcePdfPages"] == [336, 345]
assert (len(BLOCKS), len(CHAPTER["toc"]), len(FORMULAS), len(FIGURES), len(EXERCISES)) == (
    134, 6, 22, 6, 8)
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(25.{number})" for number in range(1, 21)]
assert sum(not block["number"] for block in FORMULAS) == 2
assert [len(block["rows"]) for block in TABLES] == [4, 3, 17, 8]
assert [block["start"] for block in LISTS] == [1, 2]

BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters25Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const id of ["23", "24", "25"]) {
  const old = chapters25Preview.findIndex(item => item.id === id);
  if (old >= 0) chapters25Preview.splice(old, 1);
}
chapters25Preview.push({
  id: "23", number: "23", title: "常用的概率分布",
  content: "books/mackay-information-theory-2003/chapter-23.draft.json"
});
chapters25Preview.push({
  id: "24", number: "24", title: "精确边缘化",
  content: "books/mackay-information-theory-2003/chapter-24.draft.json"
});
chapters25Preview.push({
  id: "25", number: "25", title: "格形图中的精确边缘化",
  content: "books/mackay-information-theory-2003/chapter-25.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch25-formal-qa" if FORMAL else "mackay-ch25-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p345-b010"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '25' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '25' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last))
    assert len({position["top"] for position in positions}) == 1, positions
    assert len({position["y"] for position in positions}) == 1, positions
    return positions


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/"

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        for width, mode in VIEWPORTS:
            suffix = f"{width}-{mode}"
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme=mode,
                service_workers="block",
                permissions=["clipboard-read", "clipboard-write"],
            )
            if not FORMAL:
                context.route("**/books.js", lambda route: route.fulfill(
                    body=BOOK_SCRIPT, content_type="application/javascript"))
            page = context.new_page()
            errors, failed_resources, requests = [], [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("request", lambda request: requests.append(request.url))
            page.on("requestfailed", lambda request: failed_resources.append(
                f"{request.failure}: {request.url}")
                if request.failure != "net::ERR_ABORTED" else None)
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=25")
            page.locator("#read-p345-b010").wait_for()
            if FORMAL:
                assert any(url.endswith("/books.js") for url in requests)
                assert any(url.endswith(
                    "/books/mackay-information-theory-2003/chapter-25.json")
                    for url in requests)

            actual = page.locator(".reading-block").evaluate_all("""items => items.map(
              item => [item.id, [...item.classList].find(name =>
                name.startsWith('reading-') && name !== 'reading-block')])""")
            assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                              for block in BLOCKS]
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").count() == 5
            assert page.locator(".reading-heading h3").count() == 8
            assert all(page.locator(".reading-heading h3").nth(index).locator("em").count()
                       >= 1 for index in range(8))
            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(
                    f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 5
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")

            assert page.locator(".book-exercise-label").all_text_contents() == [
                block["label"] for block in EXERCISES]
            for block_id in ("p337-b005", "p341-b002"):
                icon = page.locator(f"#read-{block_id} .book-exercise-icon")
                assert icon.count() == 1
                icon.evaluate("item => item.decode()")
                assert icon.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
            assert page.locator(".book-formula math").count() == 22
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 6
            assert page.locator(".book-table").count() == 4
            assert page.locator(
                "#chapter-navigation .chapter-navigation-link[href*='chapter=24']").count() == 1
            for block_id in (
                "p336-b009", "p337-b005", "p339-b005", "p341-b002",
                "p342-b020", "p343-b005", "p345-b005", "p345-b007",
                "p345-b009", "p345-b010",
            ):
                page.locator(f"#read-{block_id}").screenshot(
                    path=str(QA_DIR / f"block-{block_id}-{suffix}.png"))

            overflow, copies = [], 0
            for block in FORMULAS:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                assert node.locator(".book-formula math").count() == 1
                assert node.locator(".formula-number").all_text_contents() == (
                    [block["number"]] if block["number"] else [])
                formula = node.locator(".book-formula")
                metric = formula.evaluate("""node => {
                  const scroll = node.querySelector('.formula-scroll');
                  const math = scroll.querySelector('math');
                  const number = node.querySelector('.formula-number');
                  return {client: scroll.clientWidth, width: scroll.scrollWidth,
                    height: scroll.getBoundingClientRect().height,
                    mathHeight: math.getBoundingClientRect().height,
                    numberSeparated: !number || number.getBoundingClientRect().left >=
                      scroll.getBoundingClientRect().right - 1};
                }""")
                assert metric["height"] >= metric["mathHeight"] - 2, (block["id"], metric)
                assert metric["numberSeparated"], (block["id"], metric)
                if metric["width"] > metric["client"] + 2:
                    overflow.append((block["id"], metric["client"], metric["width"]))
                    assert node.locator(".formula-view-hint").is_visible(), block["id"]
                    scroller = formula.locator(".formula-scroll")
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    if block["number"] in ("(25.17)", "(25.18)", "(25.19)", "(25.20)"):
                        node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                if (width == 1440 and mode == "light") or (width == 320 and mode == "dark"):
                    node.locator("math").select_text()
                    page.keyboard.press("Control+C")
                    copied = page.evaluate("navigator.clipboard.readText()")
                    assert len(copied.strip()) >= 2, (block["id"], copied)
                    page.evaluate("getSelection().removeAllRanges()")
                    copies += 1
                if block["number"] in ("(25.17)", "(25.18)", "(25.19)", "(25.20)"):
                    matrix_rows = node.locator("math mtable > mtr").count()
                    assert matrix_rows == (3 if block["number"] == "(25.20)" else 4), (
                        block["id"], matrix_rows)
                    assert all(node.locator("math mtable > mtr").nth(index).locator("mtd").count() == 7
                               for index in range(matrix_rows)), block["id"]
                    node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

            figure_metrics = {}
            for block in FIGURES:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                image = node.locator(".book-figure img")
                image.evaluate("item => item.decode()")
                assert image.evaluate("item => [item.naturalWidth, item.naturalHeight]") == [
                    block["width"], block["height"]]
                assert image.get_attribute("alt") == block["alt"]
                assert node.locator(".figure-image-link").get_attribute("href").endswith(
                    block["src"])
                media = node.locator(".figure-media")
                media.evaluate("item => item.scrollIntoView({block: 'start', inline: 'nearest'})")
                metric = media.evaluate("item => ({client: item.clientWidth, width: item.scrollWidth})")
                figure_metrics[block["id"]] = metric
                assert node.locator(".figure-caption").count() == bool(block.get("caption"))
                topbar = page.locator(".reader-topbar")
                topbar.evaluate("item => item.style.visibility = 'hidden'")
                if width <= 390 and block.get("wide"):
                    assert metric["width"] > metric["client"] + 2, (block["id"], metric)
                    assert node.locator(".figure-view-hint").is_visible()
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    page.screenshot(
                        path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"),
                        clip=media.bounding_box())
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    media.evaluate("item => item.scrollLeft = 0")
                media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
                topbar.evaluate("item => item.style.visibility = ''")

            table_metrics = {}
            for block in TABLES:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                rows = node.locator(".book-table tr")
                assert rows.count() == len(block["rows"]), block["id"]
                for row_index, expected_row in enumerate(block["rows"]):
                    cells = rows.nth(row_index).locator("th, td")
                    assert cells.count() == len(expected_row), (block["id"], row_index)
                    for cell_index, expected in enumerate(expected_row):
                        cell = cells.nth(cell_index)
                        assert (cell.evaluate("item => item.tagName") == "TH") == expected["header"], (
                            block["id"], row_index, cell_index)
                        math_count = sum(isinstance(segment, dict) and "tex" in segment
                                         for segment in expected["segments"])
                        assert cell.locator("math").count() == math_count, (
                            block["id"], row_index, cell_index)
                        if not math_count:
                            assert cell.inner_text().strip() == expected["text"], (
                                block["id"], row_index, cell_index,
                                cell.inner_text(), expected["text"])
                        if block["id"] == "p343-b005" and cell.locator("code").count():
                            assert cell.locator("code").evaluate(
                                "item => item.getClientRects().length") == 1, (
                                    block["id"], row_index, cell_index, "codeword wrapped")
                        assert cell.locator("merror").count() == 0
                scroll = node.locator(".table-scroll")
                metric = scroll.evaluate("item => ({client: item.clientWidth, width: item.scrollWidth})")
                table_metrics[block["id"]] = metric
                if metric["width"] > metric["client"] + 2:
                    scroll.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroll.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    scroll.screenshot(path=str(QA_DIR / f"table-{block['id']}-{suffix}-right.png"))
                    scroll.evaluate("item => item.scrollLeft = 0")
                else:
                    assert scroll.evaluate("""item => {
                      const table = item.querySelector('table');
                      return table.getBoundingClientRect().right <=
                        item.getBoundingClientRect().right + 2;
                    }"""), (block["id"], metric)
                node.screenshot(path=str(QA_DIR / f"table-{block['id']}-{suffix}.png"))

            assert page.locator("#read-p345-b005 .book-table tr").count() == 17
            for block in LISTS:
                ordered = page.locator(f"#read-{block['id']} ol")
                assert ordered.count() == 1
                assert ordered.get_attribute("start") == str(block["start"])
            note = page.locator("#read-p345-b010")
            assert [item.strip()[-1] for item in note.locator("math").all_text_contents()] == [
                "1", "2", "3"]
            assert "下标" in note.inner_text()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            bottom = inspect_progress(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)

            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=24']").click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=24" in page.url
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=25']").click()
            page.locator("#read-p345-b010").wait_for()
            assert "chapter=25" in page.url
            assert not errors and not failed_resources, (errors, failed_resources)
            print(json.dumps({
                "viewport": suffix, "blocks": len(actual), "formulas": len(FORMULAS),
                "formulaOverflow": overflow, "formulaCopied": copies,
                "figures": figure_metrics, "tables": table_metrics, "bottom": bottom,
                "errors": errors, "failedResources": failed_resources,
            }, ensure_ascii=False), flush=True)
            context.close()
        browser.close()
    label = "formal path" if FORMAL else "draft technical baseline"
    print(f"PASS: chapter 25 {label}, six viewports, "
          f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
