"""Inspect the unpublished MacKay chapter 14 drafts in the real reader."""

import json
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
INTRO = json.loads((BOOK / "chapter-14-intro.draft.json").read_text(encoding="utf-8"))
CHAPTER = json.loads((BOOK / "chapter-14.draft.json").read_text(encoding="utf-8"))
BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters14Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const id of ["14-intro", "14"]) {
  const previous = chapters14Preview.findIndex(item => item.id === id);
  if (previous >= 0) chapters14Preview.splice(previous, 1);
}
chapters14Preview.push(
  {id: "14-intro", number: "导页", title: "关于第 14 章",
   content: "books/mackay-information-theory-2003/chapter-14-intro.draft.json"},
  {id: "14", number: "14", title: "存在非常好的线性码",
   content: "books/mackay-information-theory-2003/chapter-14.draft.json"}
);
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / "mackay-ch14-draft-qa"
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, False), (390, False), (390, True), (350, False), (350, True))
FORMULAS = [block for block in CHAPTER["blocks"] if block["kind"] == "formula"]
assert len(INTRO["blocks"]) == 4 and len(CHAPTER["blocks"]) == 56
assert [block["number"] for block in FORMULAS] == [f"(14.{i})" for i in range(1, 20)]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def assert_blocks(page, draft):
    expected = draft["blocks"]
    actual = page.locator(".reading-block").evaluate_all(
        "items => items.map(item => ({id: item.id, kind: item.className.split(' ').find(x => x.startsWith('reading-') && x !== 'reading-block')}))"
    )
    assert actual == [
        {"id": f"read-{block['id']}", "kind": f"reading-{block['kind']}"}
        for block in expected
    ], (actual, expected)
    for block in expected:
        if block["kind"] == "formula":
            continue
        node = page.locator(f"#read-{block['id']}")
        segments = block.get("segments", [])
        assert node.locator("math").count() == sum(
            isinstance(segment, dict) and "mathml" in segment for segment in segments
        ), block["id"]
        rendered = node.inner_text()
        for segment in segments:
            if isinstance(segment, str):
                assert segment in rendered, (block["id"], segment, rendered)
            elif "mathml" not in segment:
                assert segment["text"] in rendered, (block["id"], segment, rendered)
        for tag in ("em", "strong"):
            expected_text = [segment["text"] for segment in segments
                             if isinstance(segment, dict) and segment.get(tag)]
            content = node.locator(".book-exercise-body") if block["kind"] == "exercise" else node
            assert content.locator(tag).all_text_contents() == expected_text, (
                block["id"], tag, expected_text, content.locator(tag).all_text_contents()
            )


def check_toc(page, draft, width):
    expected = [f"#read-{item['block']}" for item in draft["toc"][1:]]
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        assert page.locator(f"{selector} .toc-chapter-link.chapter-current").count() == 1
        assert page.locator(f"{selector} .toc-section-link").evaluate_all(
            "items => items.map(item => item.hash)") == expected
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("item => item.open")
        assert page.locator("#reader-toc-mobile .toc-chapter-link.chapter-current").is_visible()
        page.locator("#toc-close").click()
        assert not page.locator("#toc-dialog").evaluate("item => item.open")
    else:
        assert page.locator("#reader-toc .toc-chapter-link.chapter-current").is_visible()


def check_bottom(page, chapter_id, last_id):
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    page.wait_for_function("""({key, chapter, block}) => {
      const saved = JSON.parse(localStorage.getItem(key) || '{}');
      return saved.chapter === chapter && saved.block === block &&
        document.querySelector('#reading-progress').style.width === '100%';
    }""", arg={"key": PROGRESS_KEY, "chapter": chapter_id,
               "block": f"read-{last_id}"})
    restored = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, chapter, block}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === chapter && saved.block === block &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "chapter": chapter_id,
                   "block": f"read-{last_id}"})
        restored.append(page.evaluate("""({key, block}) => ({
          saved: JSON.parse(localStorage.getItem(key)).block,
          y: Math.round(scrollY),
          top: Math.round(document.querySelector('#' + block).getBoundingClientRect().top),
          width: document.querySelector('#reading-progress').style.width
        })""", {"key": PROGRESS_KEY, "block": f"read-{last_id}"}))
    assert len({item["y"] for item in restored}) == 1, restored
    assert len({item["top"] for item in restored}) == 1, restored
    return restored


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
            context.route("**/books.js", lambda route: route.fulfill(
                body=BOOK_SCRIPT, content_type="application/javascript"))
            page = context.new_page()
            errors, failed_resources = [], []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)

            page.goto(base + "?book=mackay-information-theory-2003&chapter=14-intro")
            page.locator("#read-p240-b004").wait_for()
            assert_blocks(page, INTRO)
            check_toc(page, INTRO, width)
            assert page.locator("#read-p240-b003 em").all_text_contents() == ["线性"]
            assert page.locator("#read-p240-b004 em").all_text_contents() == ["随机线性哈希函数"]
            assert page.locator("#read-p240-b003 em").evaluate(
                "item => getComputedStyle(item).fontStyle") == "italic"
            assert page.locator("#read-p240-b004 em").evaluate(
                "item => getComputedStyle(item).fontStyle") == "italic"
            intro_nav = page.locator("#chapter-navigation .chapter-navigation-link")
            assert intro_nav.count() == 2
            previous_href = intro_nav.nth(0).get_attribute("href")
            assert "chapter=13" in previous_href
            assert "chapter=14" in intro_nav.nth(1).get_attribute("href")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.screenshot(path=str(QA_DIR / f"intro-{suffix}.png"), full_page=True)
            intro_progress = check_bottom(page, "14-intro", "p240-b004")

            page.locator("#chapter-navigation .chapter-navigation-link").nth(0).click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=13" in page.url and page.locator(".reading-block").count() >= 3
            page.goto(base + "?book=mackay-information-theory-2003&chapter=14-intro")
            page.locator("#read-p240-b004").wait_for()
            page.locator("#chapter-navigation .chapter-navigation-link").nth(1).click()
            page.locator("#read-p244-b002").wait_for()
            assert "chapter=14" in page.url
            assert_blocks(page, CHAPTER)
            check_toc(page, CHAPTER, width)
            assert page.locator(".reading-intro").count() == 1
            assert "非原书正文" in page.locator(".reading-intro").inner_text()
            assert page.locator(".reading-heading").count() == 4
            assert page.locator(".reading-exercise").count() == 1
            assert page.locator(".book-exercise-label").all_text_contents() == ["习题 14.1"]
            assert page.locator(".reading-quote").count() == 4
            assert page.locator(".book-figure, .book-table").count() == 0
            assert page.locator(".book-formula math").count() == 19
            assert page.locator(".formula-number").all_text_contents() == [
                f"(14.{number})" for number in range(1, 20)]
            assert page.locator("math merror, .formula-fallback").count() == 0
            body_nav = page.locator("#chapter-navigation .chapter-navigation-link")
            assert body_nav.count() == 1
            assert "chapter=14-intro" in body_nav.first.get_attribute("href")
            toc_link = page.locator("#reader-toc-mobile .toc-section-link").last if width < 800 else page.locator("#reader-toc .toc-section-link").last
            if width < 800:
                page.locator("#toc-toggle").click()
            toc_link.click()
            page.wait_for_function("""() =>
              location.hash === '#read-p243-b014' &&
              Math.abs(document.querySelector('#read-p243-b014').getBoundingClientRect().top - 85) <= 2""")
            if width < 800:
                assert not page.locator("#toc-dialog").evaluate("item => item.open")
            page.evaluate("history.replaceState(null, '', location.pathname + location.search)")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")

            formula_metrics = []
            for block in FORMULAS:
                formula = page.locator(f"#read-{block['id']}")
                formula.scroll_into_view_if_needed()
                metric = formula.locator(".book-formula").evaluate("""item => {
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
                assert metric["separated"], (block["id"], metric)
                assert metric["height"] >= metric["mathHeight"] - 2, (block["id"], metric)
                if metric["scroll"] > metric["client"] + 2:
                    assert width > 800 or metric["hint"], (block["id"], metric)
                    scroller = formula.locator(".formula-scroll")
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= (
                        metric["scroll"] - metric["client"] - 2), (block["id"], metric)
                    if width <= 390:
                        formula.screenshot(path=str(QA_DIR / f"formula-{block['number'][1:-1]}-{suffix}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                math = formula.locator(".book-formula math")
                math.select_text()
                page.keyboard.press("Control+C")
                copied = page.evaluate("navigator.clipboard.readText()")
                assert len(copied.strip()) >= 2, (block["id"], copied)
                page.evaluate("window.getSelection()?.removeAllRanges()")
                metric["id"], metric["number"], metric["copied"] = (
                    block["id"], block["number"], len(copied))
                formula_metrics.append(metric)
                if width in (1440, 350):
                    formula.screenshot(path=str(QA_DIR / f"formula-{block['number'][1:-1]}-{suffix}.png"))

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            body_snap_positions = {}
            for block_id, name in (("p241-b001", "top"),
                                   ("p243-b013", "exercise-14-1"),
                                   ("p243-b014", "section-14-2"),
                                   ("p244-b001", "notes")):
                block = page.locator(f"#read-{block_id}")
                block.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
                body_snap_positions[name] = block.evaluate("""item => ({
                  top: Math.round(item.getBoundingClientRect().top),
                  y: Math.round(scrollY),
                  height: Math.round(item.getBoundingClientRect().height)
                })""")
                assert body_snap_positions[name]["top"] < 844, body_snap_positions[name]
                page.screenshot(path=str(QA_DIR / f"body-{name}-{suffix}.png"))

            progress_target = page.locator("#read-p242-b015")
            progress_target.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.wait_for_function(
                "key => JSON.parse(localStorage.getItem(key) || '{}').block === 'read-p242-b015'",
                arg=PROGRESS_KEY)
            mid_progress = []
            for _ in range(3):
                page.reload()
                page.wait_for_function("""key => {
                  const item = document.querySelector('#read-p242-b015');
                  return item && JSON.parse(localStorage.getItem(key) || '{}').block ===
                    'read-p242-b015' && Math.abs(item.getBoundingClientRect().top - 85) <= 2;
                }""", arg=PROGRESS_KEY)
                mid_progress.append(page.evaluate("""() => ({
                  y: Math.round(scrollY),
                  top: Math.round(document.querySelector('#read-p242-b015').getBoundingClientRect().top)
                })"""))
            assert len({item["y"] for item in mid_progress}) == 1, mid_progress
            body_progress = check_bottom(page, "14", "p244-b002")
            page.screenshot(path=str(QA_DIR / f"body-bottom-{suffix}.png"))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            body_nav = page.locator("#chapter-navigation .chapter-navigation-link")
            body_nav.click()
            page.locator("#read-p240-b004").wait_for()
            assert "chapter=14-intro" in page.url
            assert page.locator(".reading-block").count() == 4

            print(json.dumps({
                "viewport": suffix,
                "intro_blocks": 4,
                "intro_bottom": intro_progress,
                "body_blocks": 56,
                "formula_count": 19,
                "formula_overflow": [item["number"] for item in formula_metrics
                                     if item["scroll"] > item["client"] + 2],
                "largest_formula": max(formula_metrics, key=lambda item: item["scroll"]),
                "all_formula_copied": all(item["copied"] >= 2 for item in formula_metrics),
                "body_mid": mid_progress,
                "body_bottom": body_progress,
                "body_snap_positions": body_snap_positions,
                "errors": errors,
                "failed_resources": failed_resources,
            }, ensure_ascii=False))
            context.close()
        browser.close()
    print(f"PASS: chapter 14 unpublished drafts, five viewports, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
