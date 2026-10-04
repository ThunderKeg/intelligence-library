"""Inspect MacKay chapter 20 in the reader, optionally on the registered path."""

from argparse import ArgumentParser
import hashlib
import json
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
parser = ArgumentParser()
parser.add_argument("--formal", action="store_true",
                    help="inspect the registered chapter-20.json without intercepting books.js")
FORMAL = parser.parse_args().formal
DRAFT_BYTES = (BOOK / "chapter-20.draft.json").read_bytes()
FORMAL_BYTES = (BOOK / "chapter-20.json").read_bytes() if FORMAL else None
if FORMAL:
    assert FORMAL_BYTES == DRAFT_BYTES, "formal chapter differs from reviewed draft"
CHAPTER_BYTES = FORMAL_BYTES if FORMAL else DRAFT_BYTES
DRAFT = json.loads(CHAPTER_BYTES.decode("utf-8"))


def reading_blocks(items):
    for item in items:
        if item["kind"] == "box":
            yield from reading_blocks(item["blocks"])
        else:
            yield item


BLOCKS = list(reading_blocks(DRAFT["blocks"]))
FORMULAS = [block for block in BLOCKS if block["kind"] == "formula"]
FIGURES = [block for block in BLOCKS if block["kind"] == "figure"]
EXERCISES = [block for block in BLOCKS if block["kind"] == "exercise"]
assert DRAFT["sourcePdfPages"] == [296, 304]
assert (len(DRAFT["blocks"]), len(BLOCKS), len(DRAFT["toc"]), len(FORMULAS),
        len(FIGURES), len(EXERCISES)) == (83, 100, 6, 23, 10, 5)
assert [(block["id"], len(block["blocks"])) for block in DRAFT["blocks"]
        if block["kind"] == "box"] == [("box-20-2", 12), ("box-20-7", 7)]
assert [block["number"] for block in FORMULAS if block["number"]] == [
    f"(20.{number})" for number in range(1, 24)]
assert all(block["number"] for block in FORMULAS)
BOOK_SCRIPT = None if FORMAL else (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters20Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const oldChapter20 = chapters20Preview.findIndex(item => item.id === "20");
if (oldChapter20 >= 0) chapters20Preview.splice(oldChapter20, 1);
chapters20Preview.push({
  id: "20", number: "20", title: "一个推断任务示例：聚类",
  content: "books/mackay-information-theory-2003/chapter-20.draft.json"
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-ch20-formal-qa" if FORMAL else "mackay-ch20-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (390, "light"), (390, "dark"), (350, "light"), (350, "dark"))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def inspect_progress(page):
    last = "read-p304-b014"
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, last}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === '20' && saved.block === last &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "last": last})
    positions = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === '20' && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "last": last})
        positions.append(page.evaluate("""last => ({
          top: Math.round(document.getElementById(last).getBoundingClientRect().top),
          y: Math.round(scrollY)
        })""", last))
    assert len({item["top"] for item in positions}) == 1, positions
    assert len({item["y"] for item in positions}) == 1, positions
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
            errors, failed_resources, requested_urls = [], [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("request", lambda request: requested_urls.append(request.url))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=20")
            page.locator("#read-p304-b014").wait_for()
            if FORMAL:
                assert any(url.endswith("/books.js") for url in requested_urls)
                assert any(url.endswith(
                    "/books/mackay-information-theory-2003/chapter-20.json")
                    for url in requested_urls)

            actual = page.locator(".reading-block").evaluate_all("""items => items.map(
              item => [item.id, [...item.classList].find(name =>
                name.startsWith('reading-') && name !== 'reading-block')])""")
            assert actual == [[f"read-{block['id']}", f"reading-{block['kind']}"]
                              for block in BLOCKS]
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading h1").count() == 1
            assert page.locator(".reading-heading h2").count() == 5
            assert page.locator(".reading-heading h3").count() == 3
            assert page.locator(".reading-heading h3 em").count() == 2
            assert page.locator(".book-exercise-label").all_text_contents() == [
                block["label"] for block in EXERCISES]
            first_exercise = page.locator("#read-p299-b003")
            first_exercise_text = first_exercise.locator("p").text_content()
            assert "。\n[提示：" in first_exercise_text
            assert "。]\n[李雅普诺夫函数" in first_exercise_text
            assert first_exercise.locator("p").evaluate(
                "item => getComputedStyle(item).whiteSpace") == "pre-wrap"
            first_exercise.screenshot(
                path=str(QA_DIR / f"exercise-20-1-hints-{suffix}.png"))
            assert page.locator("#read-p300-b006 em").all_text_contents() == [
                "在一定程度上"]
            page.locator("#read-p300-b006").screenshot(
                path=str(QA_DIR / f"p300-italic-{suffix}.png"))
            for block_id, answer in (
                ("p303-b002", "习题 20.1 的解答"),
                ("p303-b004", "习题 20.3 的解答"),
                ("p304-b013", "习题 20.5 的解答"),
            ):
                assert page.locator(f"#read-{block_id}").inner_text().startswith(answer)
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 10
            assert page.locator(".book-formula math").count() == 23
            for selector in ("#reader-toc", "#reader-toc-mobile"):
                assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
                assert page.locator(f"{selector} .toc-section-link").count() == 5
            if width < 800:
                page.locator("#toc-toggle").click()
                assert page.locator("#toc-dialog").evaluate("item => item.open")
                page.locator("#toc-close").click()
                assert not page.locator("#toc-dialog").evaluate("item => item.open")
            else:
                assert page.locator("#reader-toc .toc-chapter-link.chapter-current").is_visible()
            previous = page.locator(
                "#chapter-navigation .chapter-navigation-link[href*='chapter=IV-intro']")
            assert previous.count() == 1

            # Algorithms 20.2 and 20.7 must remain complete outlined units.
            box_metrics = {}
            assert page.locator("#reader-article .outlined-box").count() == 2
            for number, first_id, last_id, caption_id in (
                ("20-2", "p298-b001", "p298-b012", "p298-b013"),
                ("20-7", "p301-b003", "p301-b009", "p301-b010"),
            ):
                box = page.evaluate("""({firstId, lastId}) => {
                  const first = document.getElementById('read-' + firstId);
                  const last = document.getElementById('read-' + lastId);
                  const parent = first.parentElement;
                  return {
                    firstParent: parent.id, lastParent: last.parentElement.id,
                    childBlocks: parent.querySelectorAll('.reading-block').length,
                    borderLeft: getComputedStyle(parent).borderLeftWidth,
                    borderTop: getComputedStyle(parent).borderTopWidth,
                    borderBottom: getComputedStyle(parent).borderBottomWidth,
                    background: getComputedStyle(parent).backgroundColor
                  };
                }""", {"firstId": first_id, "lastId": last_id})
                assert box["firstParent"] == f"read-box-{number}", box
                assert box["lastParent"] == f"read-box-{number}", box
                assert box["childBlocks"] == (12 if number == "20-2" else 7), box
                assert all(box[key] != "0px" for key in
                           ("borderLeft", "borderTop", "borderBottom")), box
                assert page.locator(f"#read-{caption_id}").inner_text().startswith(
                    f"算法 {number.replace('-', '.')}")
                box_metrics[number] = box
                page.locator(f"#read-{first_id}").evaluate(
                    "item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
                page.screenshot(path=str(QA_DIR / f"algorithm-{number}-top-{suffix}.png"))
                page.locator(f"#read-{caption_id}").evaluate(
                    "item => item.scrollIntoView({block: 'end', behavior: 'instant'})")
                page.screenshot(path=str(QA_DIR / f"algorithm-{number}-bottom-{suffix}.png"))

            formula_overflow = []
            copied = 0
            for block in FORMULAS:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                assert node.locator(".book-formula math").count() == 1, block["id"]
                expected_number = [block["number"]] if block["number"] else []
                assert node.locator(".formula-number").all_text_contents() == expected_number
                formula = node.locator(".book-formula")
                metric = formula.evaluate("""node => {
                  const scroller = node.querySelector('.formula-scroll');
                  const number = node.querySelector('.formula-number');
                  return {
                    client: scroller.clientWidth, scroll: scroller.scrollWidth,
                    height: scroller.getBoundingClientRect().height,
                    mathHeight: scroller.querySelector('math').getBoundingClientRect().height,
                    numberSeparated: !number || number.getBoundingClientRect().left >=
                      scroller.getBoundingClientRect().right - 1
                  };
                }""")
                assert metric["height"] >= metric["mathHeight"] - 2
                assert metric["numberSeparated"], (block["id"], metric)
                if metric["scroll"] > metric["client"] + 2:
                    formula_overflow.append(block["id"])
                    if width <= 390:
                        assert node.locator(".formula-view-hint").is_visible()
                    scroller = formula.locator(".formula-scroll")
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2)
                    if block["id"] in ("p298-b005", "p301-b004", "p303-b005", "p304-b014") and width <= 390:
                        node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                if width == 1440 or (width == 350 and mode == "dark"):
                    node.locator("math").select_text()
                    page.keyboard.press("Control+C")
                    copied_text = page.evaluate("navigator.clipboard.readText()")
                    assert len(copied_text.strip()) >= 2, (block["id"], copied_text)
                    copied += 1
                    page.evaluate("getSelection().removeAllRanges()")
                if block["id"] in ("p298-b005", "p301-b004", "p303-b005", "p304-b014"):
                    node.screenshot(path=str(QA_DIR / f"formula-{block['id']}-{suffix}.png"))

            figure_metrics = {}
            for block in FIGURES:
                node = page.locator(f"#read-{block['id']}")
                node.scroll_into_view_if_needed()
                image = node.locator(".book-figure img")
                image.evaluate("item => item.decode()")
                assert image.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
                assert image.evaluate("item => [item.naturalWidth, item.naturalHeight]") == [
                    block["width"], block["height"]]
                assert image.get_attribute("alt") == block["alt"]
                assert node.locator(".figure-image-link").get_attribute("href").endswith(block["src"])
                media = node.locator(".figure-media")
                metric = media.evaluate("item => ({client: item.clientWidth, scroll: item.scrollWidth})")
                figure_metrics[block["id"]] = metric
                if block.get("caption"):
                    assert node.locator(".figure-caption").count() == 1
                else:
                    assert node.locator(".figure-caption").count() == 0
                if width <= 390 and block.get("wide"):
                    assert metric["scroll"] > metric["client"] + 2, (block["id"], metric)
                    assert node.locator(".figure-view-hint").is_visible()
                    media.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert media.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2)
                    if block["id"] == "p302-b001":
                        media.evaluate("""item => {
                          item.scrollIntoView({block: 'start', behavior: 'instant'});
                          item.scrollLeft = item.scrollWidth;
                        }""")
                        page.screenshot(
                            path=str(QA_DIR / f"figure-20-8-mobile-right-page-{suffix}.png"))
                    node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}-right.png"))
                    media.evaluate("item => item.scrollLeft = 0")
                elif width <= 390:
                    assert metric["scroll"] <= metric["client"] + 2, (block["id"], metric)
                    assert node.locator(".figure-view-hint").count() == 0
                if width in (1440, 350):
                    node.screenshot(path=str(QA_DIR / f"figure-{block['id']}-{suffix}.png"))

            for figure_id, translated_labels in {
                "p299-b001": ("数据", "分配", "更新"),
                "p299-b002": ("第 1 次运行", "第 2 次运行"),
                "p302-b001": ("较大的", "较小的"),
                "p303-b019": ("数据密度", "均值位置"),
                "p303-b020": ("数据密度", "均值位置"),
            }.items():
                caption_text = page.locator(
                    f"#read-{figure_id} .figure-caption").inner_text()
                assert all(label in caption_text for label in translated_labels), (
                    figure_id, caption_text)

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            restored = inspect_progress(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            previous.click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=IV-intro" in page.url
            page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=20']").click()
            page.locator("#read-p304-b014").wait_for()
            assert "chapter=20" in page.url
            assert not errors and not failed_resources, (errors, failed_resources)
            print(json.dumps({
                "viewport": suffix, "blocks": len(actual), "toc": len(DRAFT["toc"]),
                "formulas": len(FORMULAS), "formulaOverflow": formula_overflow,
                "formulaCopied": copied, "figures": figure_metrics, "algorithms": box_metrics,
                "bottom": restored, "errors": errors, "failed_resources": failed_resources,
            }, ensure_ascii=False))
            context.close()
        browser.close()
    label = "formal path" if FORMAL else "draft technical baseline"
    print(f"PASS: chapter 20 {label}, five viewports, "
          f"sha256={hashlib.sha256(CHAPTER_BYTES).hexdigest()}, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
