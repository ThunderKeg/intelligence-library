"""Inspect chapter 27 draft or registered path in six Edge viewports."""

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
DRAFT_BYTES = (BOOK / "chapter-27.draft.json").read_bytes()
FORMAL_BYTES = (BOOK / "chapter-27.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal JSON differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
CHAPTER = json.loads(CHAPTER_BYTES.decode("utf-8"))
BLOCKS = CHAPTER["blocks"]
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
assert CHAPTER["sourcePdfPages"] == [353, 354]
assert (len(BLOCKS), len(CHAPTER["toc"]), len(FORMULAS), len(FIGURES), len(EXERCISES)) == (
    41, 2, 14, 1, 3)
assert [block["number"] for block in FORMULAS] == [
    f"(27.{number})" for number in range(1, 15)]

BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters27Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const existing27 = chapters27Preview.findIndex(item => item.id === "27");
if (existing27 >= 0) chapters27Preview.splice(existing27, 1);
chapters27Preview.push({
  id: "27", number: "27", title: "拉普拉斯方法",
  content: "books/mackay-information-theory-2003/chapter-27.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch27-formal-qa" if FORMAL else "mackay-ch27-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (320, "light"), (320, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_viewport(browser, base, width, mode):
    suffix = f"{width}-{mode}"
    context = browser.new_context(
        viewport={"width": width, "height": 844}, color_scheme=mode,
        service_workers="block", permissions=["clipboard-read", "clipboard-write"],
    )
    if not FORMAL:
        context.route("**/books.js", lambda route: route.fulfill(
            body=BOOK_SCRIPT, content_type="application/javascript"))
    page = context.new_page()
    errors, failed_resources, requests = [], [], []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: requests.append(request.url))
    page.on("requestfailed", lambda request: failed_resources.append(
        f"{request.failure}: {request.url}") if request.failure != "net::ERR_ABORTED" else None)
    page.on("response", lambda response: failed_resources.append(
        f"{response.status}: {response.url}") if response.status >= 400 else None)
    page.goto(base + "?book=mackay-information-theory-2003&chapter=27")
    page.locator(f"#read-{BLOCKS[-1]['id']}").wait_for()
    if FORMAL:
        assert any(url.endswith("/books.js") for url in requests)
        assert any(url.endswith(
            "/books/mackay-information-theory-2003/chapter-27.json")
            for url in requests)

    actual = page.locator(".reading-block").evaluate_all("""items => items.map(
      item => [item.id, [...item.classList].find(name =>
        name.startsWith('reading-') && name !== 'reading-block')])""")
    assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                      for block in BLOCKS]
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-heading h2").count() == 1
    assert "非原书正文" in page.locator(".reading-intro").inner_text()
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").count() == 1
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("node => node.open")
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("node => node.open")

    assert page.locator(".book-exercise-label").all_text_contents() == [
        block["label"] for block in EXERCISES]
    icon = page.locator("#read-p354-b008 .book-exercise-icon")
    assert icon.count() == 1
    icon.evaluate("node => node.decode()")
    assert icon.evaluate("node => node.naturalWidth > 0 && node.naturalHeight > 0")
    assert page.locator(".book-exercise-icon").count() == 1
    assert page.locator(".book-formula math").count() == 14
    assert page.locator("math merror, .formula-fallback").count() == 0
    assert page.locator(".book-figure img").count() == 1

    formula_overflow = []
    formulas_copied = 0
    for block in FORMULAS:
        node = page.locator(f"#read-{block['id']}")
        node.scroll_into_view_if_needed()
        assert node.locator(".book-formula math").count() == 1
        assert node.locator(".formula-number").all_text_contents() == [block["number"]]
        metric = node.locator(".book-formula").evaluate("""node => {
          const scroll = node.querySelector('.formula-scroll');
          const math = scroll.querySelector('math');
          const number = node.querySelector('.formula-number');
          return {client: scroll.clientWidth, width: scroll.scrollWidth,
            height: scroll.getBoundingClientRect().height,
            mathHeight: math.getBoundingClientRect().height,
            numberSeparated: number.getBoundingClientRect().left >=
              scroll.getBoundingClientRect().right - 1};
        }""")
        assert metric["height"] >= metric["mathHeight"] - 2, (block["id"], metric)
        assert metric["numberSeparated"], (block["id"], metric)
        if metric["width"] > metric["client"] + 2:
            formula_overflow.append((block["number"], metric["client"], metric["width"]))
            assert node.locator(".formula-view-hint").is_visible(), block["id"]
            scroller = node.locator(".formula-scroll")
            scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
            assert scroller.evaluate("item => item.scrollLeft") >= (
                metric["width"] - metric["client"] - 2)
            if block["number"] in ("(27.8)", "(27.9)", "(27.12)"):
                scroller.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
            scroller.evaluate("item => item.scrollLeft = 0")
        if block["number"] in ("(27.8)", "(27.9)", "(27.12)"):
            node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))
        if (width, mode) in ((1440, "light"), (320, "dark")):
            node.locator("math").select_text()
            page.keyboard.press("Control+C")
            copied = page.evaluate("navigator.clipboard.readText()")
            assert len(copied.strip()) >= 2, (block["number"], copied)
            page.evaluate("getSelection().removeAllRanges()")
            formulas_copied += 1

    figure = FIGURES[0]
    figure_node = page.locator(f"#read-{figure['id']}")
    figure_node.scroll_into_view_if_needed()
    image = figure_node.locator(".book-figure img")
    image.evaluate("node => node.decode()")
    assert image.evaluate("node => [node.naturalWidth, node.naturalHeight]") == [
        figure["width"], figure["height"]]
    assert image.get_attribute("alt") == figure["alt"]
    assert figure_node.locator(".figure-image-link").get_attribute("href").endswith(
        figure["src"])
    figure_metric = image.evaluate("""node => ({displayWidth: Math.round(node.getBoundingClientRect().width),
      naturalWidth: node.naturalWidth, link: !!node.closest('a')})""")
    figure_node.screenshot(path=str(QA_DIR / f"figure-{suffix}.png"))
    page.locator("#read-p353-b014").screenshot(
        path=str(QA_DIR / f"diagram-note-{suffix}.png"))
    page.locator("#read-p354-b008").screenshot(
        path=str(QA_DIR / f"exercise-{suffix}.png"))
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    page.screenshot(path=str(QA_DIR / f"page-{suffix}.png"), full_page=True)

    last = f"read-{BLOCKS[-1]['id']}"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '27' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    progress = []
    for _ in range(3 if FORMAL else 1):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '27' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        progress.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          scrollY: Math.round(scrollY)
        })""", last))
    assert len({position["top"] for position in progress}) == 1, progress
    assert len({position["scrollY"] for position in progress}) == 1, progress
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert not errors and not failed_resources, (errors, failed_resources)
    if FORMAL:
        page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=26']").click()
        page.locator(".reading-block").first.wait_for()
        assert "chapter=26" in page.url
        page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=27']").click()
        page.locator(f"#{last}").wait_for()
        assert "chapter=27" in page.url
        assert not errors and not failed_resources, (errors, failed_resources)
    context.close()
    print(json.dumps({
        "viewport": suffix, "blocks": len(actual), "formulas": len(FORMULAS),
        "formulaOverflow": formula_overflow, "formulaCopied": formulas_copied,
        "figure": figure_metric,
        "progress": progress,
        "errors": errors, "failedResources": failed_resources,
    }, ensure_ascii=False), flush=True)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0),
                                 partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            )
            for width, mode in VIEWPORTS:
                inspect_viewport(browser, f"http://127.0.0.1:{server.server_port}/",
                                 width, mode)
            browser.close()
        print(f"PASS: chapter 27 {'formal path' if FORMAL else 'draft'} six-viewpoint QA, "
              f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
