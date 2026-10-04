"""Inspect chapter 24 in the reader; use --formal after registration."""

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
DRAFT_BYTES = (BOOK / "chapter-24.draft.json").read_bytes()
FORMAL_BYTES = (BOOK / "chapter-24.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
assert CHAPTER["sourcePdfPages"] == [331, 335]
assert (len(BLOCKS), len(CHAPTER["toc"]), len(FORMULAS), len(FIGURES), len(EXERCISES)) == (
    64, 4, 17, 2, 3)
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(24.{number})" for number in range(1, 16)]
assert sum(not block["number"] for block in FORMULAS) == 2

BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters24Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const id of ["23", "24"]) {
  const old = chapters24Preview.findIndex(item => item.id === id);
  if (old >= 0) chapters24Preview.splice(old, 1);
}
chapters24Preview.push({
  id: "23", number: "23", title: "常用的概率分布",
  content: "books/mackay-information-theory-2003/chapter-23.draft.json"
});
chapters24Preview.push({
  id: "24", number: "24", title: "精确边缘化",
  content: "books/mackay-information-theory-2003/chapter-24.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch24-formal-qa" if FORMAL else "mackay-ch24-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p335-b015"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '24' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '24' && saved.block === last &&
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
            page.goto(base + "?book=mackay-information-theory-2003&chapter=24")
            page.locator("#read-p335-b015").wait_for()
            if FORMAL:
                assert any(url.endswith("/books.js") for url in requests)
                assert any(url.endswith(
                    "/books/mackay-information-theory-2003/chapter-24.json")
                    for url in requests)

            actual = page.locator(".reading-block").evaluate_all("""items => items.map(
              item => [item.id, [...item.classList].find(name =>
                name.startsWith('reading-') && name !== 'reading-block')])""")
            assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                              for block in BLOCKS]
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").count() == 3
            assert page.locator(".reading-heading h3").count() == 3
            assert all(page.locator(".reading-heading h3").nth(index).locator("em").count()
                       >= 1 for index in (0, 1))
            assert page.locator(".reading-heading h3").nth(2).locator("em").count() == 0
            assert "延伸阅读" in page.locator("#read-p335-b005 h3").inner_text()
            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(
                    f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 3
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")

            assert page.locator(".book-exercise-label").all_text_contents() == [
                block["label"] for block in EXERCISES]
            icon = page.locator("#read-p333-b003 .book-exercise-icon")
            assert icon.count() == 1
            icon.evaluate("item => item.decode()")
            assert icon.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
            assert page.locator(".book-formula math").count() == 17
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 2
            assert page.locator(
                "#chapter-navigation .chapter-navigation-link[href*='chapter=23']").count() == 1
            for block_id in (
                "p331-b009", "p332-b003", "p332-b008", "p333-b003",
                "p335-b003", "p335-b005", "p335-b008", "p335-b010",
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
                    if block["id"] in ("p331-b007", "p333-b006", "p334-b011"):
                        node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                if (width == 1440 and mode == "light") or (width == 320 and mode == "dark"):
                    node.locator("math").select_text()
                    page.keyboard.press("Control+C")
                    copied = page.evaluate("navigator.clipboard.readText()")
                    assert len(copied.strip()) >= 2, (block["id"], copied)
                    if block["id"] in ("p331-b007", "p333-b006", "p333-b007", "p334-b011"):
                        assert ("σ" in copied or "sigma" in copied), (block["id"], copied)
                        assert ("π" in copied or "pi" in copied), (block["id"], copied)
                    page.evaluate("getSelection().removeAllRanges()")
                    copies += 1
                if block["id"] in ("p331-b007", "p333-b006", "p333-b007", "p334-b011"):
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
                    media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    if block["id"] == "p333-b001":
                        media.evaluate("item => item.scrollLeft = (item.scrollWidth - item.clientWidth) / 2")
                        media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-middle.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                media.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))
                topbar.evaluate("item => item.style.visibility = ''")

            caption = page.locator("#read-p333-b001 .figure-caption").inner_text()
            assert all(label in caption for label in (
                "均值", "标准差", "mu=1", "mu=1.25", "mu=1.5", "P(sigma|D)"))
            note = page.locator("#read-p335-b010").inner_text()
            assert all(label in note for label in ("30", "20", "A", "B", "C", "D", "G"))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            bottom = inspect_progress(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)

            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=23']").click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=23" in page.url
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=24']").click()
            page.locator("#read-p335-b015").wait_for()
            assert "chapter=24" in page.url
            assert not errors and not failed_resources, (errors, failed_resources)
            print(json.dumps({
                "viewport": suffix, "blocks": len(actual), "formulas": len(FORMULAS),
                "formulaOverflow": overflow, "formulaCopied": copies,
                "figures": figure_metrics, "bottom": bottom,
                "errors": errors, "failedResources": failed_resources,
            }, ensure_ascii=False), flush=True)
            context.close()
        browser.close()
    label = "formal path" if FORMAL else "draft technical baseline"
    print(f"PASS: chapter 24 {label}, six viewports, "
          f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
