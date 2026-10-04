"""Inspect the MacKay chapter 22 draft in Edge; use --formal after registration."""

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
args = ArgumentParser()
args.add_argument("--formal", action="store_true")
FORMAL = args.parse_args().formal
DRAFT_BYTES = (BOOK / "chapter-22.draft.json").read_bytes()
FORMAL_BYTES = (BOOK / "chapter-22.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal JSON differs from reviewed draft"
CHAPTER = json.loads((FORMAL_BYTES if FORMAL else DRAFT_BYTES).decode("utf-8"))


def reading_blocks(items):
    for item in items:
        if item["kind"] == "box":
            yield from reading_blocks(item["blocks"])
        else:
            yield item


BLOCKS = list(reading_blocks(CHAPTER["blocks"]))
FORMULAS = [item for item in BLOCKS if item["kind"] == "formula"]
FIGURES = [item for item in BLOCKS if item["kind"] == "figure"]
EXERCISES = [item for item in BLOCKS if item["kind"] == "exercise"]
assert CHAPTER["sourcePdfPages"] == [312, 322]
assert (len(CHAPTER["blocks"]), len(BLOCKS), len(CHAPTER["toc"]),
        len(FORMULAS), len(FIGURES), len(EXERCISES)) == (151, 160, 7, 42, 11, 13)
assert [item["number"] for item in FORMULAS if item["number"]] == [
    f"(22.{n})" for n in range(1, 42)]
assert sum(not item["number"] for item in FORMULAS) == 1
assert [(item["id"], len(item["blocks"])) for item in CHAPTER["blocks"]
        if item["kind"] == "box"] == [("box-22-2", 9), ("box-22-4", 2)]
assert Counter(item["kind"] for item in BLOCKS)["table"] == 1

BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters22Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const oldChapter22 = chapters22Preview.findIndex(item => item.id === "22");
if (oldChapter22 >= 0) chapters22Preview.splice(oldChapter22, 1);
chapters22Preview.push({
  id: "22", number: "22", title: "最大似然与聚类",
  content: "books/mackay-information-theory-2003/chapter-22.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch22-formal-qa" if FORMAL else "mackay-ch22-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p322-b016"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '22' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '22' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last))
    assert len({pos["top"] for pos in positions}) == 1, positions
    assert len({pos["y"] for pos in positions}) == 1, positions
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
            page.goto(base + "?book=mackay-information-theory-2003&chapter=22")
            page.locator("#read-p322-b016").wait_for()
            if FORMAL:
                assert any(url.endswith("/books.js") for url in requests)
                assert any(url.endswith("/books/mackay-information-theory-2003/chapter-22.json")
                           for url in requests)

            actual = page.locator(".reading-block").evaluate_all("""items => items.map(
              item => [item.id, [...item.classList].find(name =>
                name.startsWith('reading-') && name !== 'reading-block')])""")
            assert actual == [[f"read-{item['id']}", f"reading-{item['kind']}"]
                              for item in BLOCKS]
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").count() == 6
            assert page.locator(".reading-heading h3").count() == 5
            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 6
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")
            assert page.locator(".book-exercise-label").all_text_contents() == [
                item["label"] for item in EXERCISES]
            icon = page.locator("#read-p314-b014 .book-exercise-icon")
            assert icon.count() == 1
            icon.evaluate("item => item.decode()")
            assert icon.evaluate("item => item.naturalWidth > 0")
            assert page.locator("#read-p319-b012 .book-exercise-icon").count() == 0
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-formula math").count() == 42
            assert page.locator(".book-figure img").count() == 11
            assert page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=21']").count() == 1

            box_metrics = {}
            assert page.locator("#reader-article .outlined-box").count() == 2
            for number, first, last, caption, total in (
                ("22-2", "p316-b001", "p316-b009", "p316-b010", 9),
                ("22-4", "p316-b013", "p316-b014", "p316-b015", 2),
            ):
                metric = page.evaluate("""({first, last}) => {
                  const a = document.getElementById('read-' + first);
                  const b = document.getElementById('read-' + last);
                  const box = a.parentElement;
                  return {firstParent: box.id, lastParent: b.parentElement.id,
                    children: box.querySelectorAll('.reading-block').length,
                    border: getComputedStyle(box).borderTopWidth};
                }""", {"first": first, "last": last})
                assert metric["firstParent"] == f"read-box-{number}", metric
                assert metric["lastParent"] == f"read-box-{number}", metric
                assert metric["children"] == total, metric
                assert metric["border"] != "0px"
                assert page.locator(f"#read-{caption}").inner_text().startswith(
                    f"算法 {number.replace('-', '.')}")
                box_metrics[number] = metric
                page.locator(f"#read-box-{number}").screenshot(
                    path=str(QA_DIR / f"algorithm-{number}-{suffix}.png"))

            formula_overflow, copied = [], 0
            for item in FORMULAS:
                node = page.locator(f"#read-{item['id']}")
                node.scroll_into_view_if_needed()
                assert node.locator(".book-formula math").count() == 1
                assert node.locator(".formula-number").all_text_contents() == (
                    [item["number"]] if item["number"] else [])
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
                assert metric["height"] >= metric["mathHeight"] - 2, (item["id"], metric)
                assert metric["numberSeparated"], (item["id"], metric)
                if metric["width"] > metric["client"] + 2:
                    formula_overflow.append(item["id"])
                    assert node.locator(".formula-view-hint").is_visible(), item["id"]
                    scroller = formula.locator(".formula-scroll")
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    if item["id"] in ("p316-b002", "p316-b013", "p322-b012"):
                        node.screenshot(path=str(QA_DIR / f"formula-{item['id']}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                if (width == 1440 and mode == "light") or (width == 320 and mode == "dark"):
                    node.locator("math").select_text()
                    page.keyboard.press("Control+C")
                    assert len(page.evaluate("navigator.clipboard.readText()").strip()) >= 2
                    page.evaluate("getSelection().removeAllRanges()")
                    copied += 1
                if item["id"] in ("p316-b002", "p316-b013", "p322-b012"):
                    node.screenshot(path=str(QA_DIR / f"formula-{item['id']}-{suffix}.png"))

            figure_metrics = {}
            for item in FIGURES:
                node = page.locator(f"#read-{item['id']}")
                node.scroll_into_view_if_needed()
                img = node.locator(".book-figure img")
                img.evaluate("item => item.decode()")
                assert img.evaluate("item => [item.naturalWidth, item.naturalHeight]") == [
                    item["width"], item["height"]]
                assert img.get_attribute("alt") == item["alt"]
                assert node.locator(".figure-image-link").get_attribute("href").endswith(item["src"])
                media = node.locator(".figure-media")
                metric = media.evaluate("item => ({client: item.clientWidth, width: item.scrollWidth})")
                figure_metrics[item["id"]] = metric
                assert node.locator(".figure-caption").count() == bool(item.get("caption"))
                if width <= 390 and item.get("wide"):
                    assert metric["width"] > metric["client"] + 2, (item["id"], metric)
                    assert node.locator(".figure-view-hint").is_visible()
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["width"] - metric["client"] - 2)
                    if item["id"] in ("p316-b012", "p317-b002"):
                        node.screenshot(path=str(QA_DIR / f"figure-{item['id']}-{suffix}-right.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                if item["id"] in ("p313-b001", "p316-b011", "p316-b012",
                                  "p321-b009", "p322-b007"):
                    node.screenshot(path=str(QA_DIR / f"figure-{item['id']}-{suffix}.png"))

            table = page.locator("#read-p321-b010 table")
            assert table.count() == 1
            assert table.locator("tr").count() == 8
            assert table.locator("tr:last-child").inner_text().strip().endswith("10.056")
            table.screenshot(path=str(QA_DIR / f"scientists-table-{suffix}.png"))
            page.locator("#read-p322-b007").screenshot(
                path=str(QA_DIR / f"figure-22-10-axis-{suffix}.png"))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            restored = inspect_progress(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=21']").click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=21" in page.url
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=22']").click()
            page.locator("#read-p322-b016").wait_for()
            assert "chapter=22" in page.url
            assert not errors and not failed_resources, (errors, failed_resources)
            print(json.dumps({"viewport": suffix, "blocks": len(actual),
                              "formulas": len(FORMULAS), "formulaOverflow": formula_overflow,
                              "formulaCopied": copied, "figures": figure_metrics,
                              "algorithms": box_metrics, "bottom": restored,
                              "errors": errors, "failedResources": failed_resources},
                             ensure_ascii=False), flush=True)
            context.close()
        browser.close()
    label = "formal path" if FORMAL else "draft technical baseline"
    print(f"PASS: chapter 22 {label}, six viewports, "
          f"sha256={hashlib.sha256((FORMAL_BYTES if FORMAL else DRAFT_BYTES)).hexdigest()}, "
          f"screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
