"""Inspect MacKay Part IV title and introduction drafts or registered pages."""

import hashlib
import json
import re
import sys
import tempfile
import threading
from collections import Counter
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
assert sys.argv[1:] in ([], ["--formal"]), "usage: preview_part_IV.py [--formal]"
FORMAL = sys.argv[1:] == ["--formal"]
PART_DRAFT_BYTES = (BOOK / "chapter-IV.draft.json").read_bytes()
INTRO_DRAFT_BYTES = (BOOK / "chapter-IV-intro.draft.json").read_bytes()
PART_BYTES = (BOOK / "chapter-IV.json").read_bytes() if FORMAL else PART_DRAFT_BYTES
INTRO_BYTES = (BOOK / "chapter-IV-intro.json").read_bytes() if FORMAL else INTRO_DRAFT_BYTES
if FORMAL:
    assert PART_BYTES == PART_DRAFT_BYTES, "registered Part IV differs from reviewed draft"
    assert INTRO_BYTES == INTRO_DRAFT_BYTES, "registered Part IV intro differs from reviewed draft"
PART = json.loads(PART_BYTES.decode("utf-8"))
INTRO = json.loads(INTRO_BYTES.decode("utf-8"))
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
QA_DIR = Path(tempfile.gettempdir()) / (
    "mackay-part-IV-formal-qa" if FORMAL else "mackay-part-IV-draft-qa")
QA_DIR.mkdir(exist_ok=True)
VIEWPORTS = ((1440, "light"), (1440, "dark"), (390, "light"),
             (390, "dark"), (350, "light"), (350, "dark"))

assert PART["sourcePdfPages"] == [293, 293] and len(PART["blocks"]) == 2
assert Counter(b["kind"] for b in PART["blocks"]) == {"heading": 1, "figure": 1}
assert INTRO["sourcePdfPages"] == [294, 295] and len(INTRO["blocks"]) == 18
assert Counter(b["kind"] for b in INTRO["blocks"]) == {
    "heading": 3, "paragraph": 14, "list": 1}

BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const partIVPreviewChapters = books.find(item => item.id === "mackay-information-theory-2003").chapters;
for (const id of ["19", "IV", "IV-intro"]) {
  const index = partIVPreviewChapters.findIndex(item => item.id === id);
  if (index >= 0) partIVPreviewChapters.splice(index, 1);
}
partIVPreviewChapters.push(
  {id: "19", number: "19", title: "为什么有性生殖？信息获取与进化",
   content: "books/mackay-information-theory-2003/chapter-19.draft.json"},
  {id: "IV", number: "第四部分", title: "概率与推断",
   content: "books/mackay-information-theory-2003/chapter-IV.draft.json"},
  {id: "IV-intro", number: "导页", title: "关于第四部分",
   content: "books/mackay-information-theory-2003/chapter-IV-intro.draft.json"}
);
"""


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def expected_marks(segments, name):
    return [item["text"] for item in segments
            if isinstance(item, dict) and item.get(name)]


def check_structure(page, draft, chapter_id):
    actual = page.locator(".reading-block").evaluate_all(
        "items => items.map(item => [item.id, [...item.classList].find("
        "name => name.startsWith('reading-') && name !== 'reading-block')])")
    expected = [[f"read-{b['id']}", f"reading-{b['kind']}"] for b in draft["blocks"]]
    assert actual == expected, (chapter_id, actual, expected)
    assert page.locator(".reading-heading h1").count() == 1
    assert page.locator(".reading-heading h2").count() == (2 if chapter_id == "IV-intro" else 0)
    for block in draft["blocks"]:
        node = page.locator(f"#read-{block['id']}")
        if block["kind"] == "list":
            assert node.locator("ol.book-list > li").count() == 2
            assert node.locator("ol.book-list").evaluate(
                "item => getComputedStyle(item).listStyleType") == "decimal"
            for item, li in zip(block["items"], node.locator("ol.book-list > li").all()):
                assert li.inner_text().strip() == item["text"]
                assert li.locator("strong").all_text_contents() == expected_marks(
                    item["segments"], "strong")
        elif block["kind"] != "figure":
            assert re.sub(r"\s+", "", node.inner_text()) == re.sub(
                r"\s+", "", block["text"]), block["id"]
        if block["kind"] not in ("list", "figure"):
            assert node.locator("strong").all_text_contents() == expected_marks(
                block.get("segments", []), "strong"), block["id"]
            assert node.locator("em").all_text_contents() == expected_marks(
                block.get("segments", []), "em"), block["id"]
    for selector in ("#reader-toc", "#reader-toc-mobile"):
        current = page.locator(f"{selector} .toc-chapter-link.chapter-current")
        assert current.count() == 1, (chapter_id, selector)
        assert page.locator(f"{selector} .toc-section-link").count() == 0
    return len(actual)


def check_figure(page, suffix):
    image = page.locator("#read-p293-b002 .book-figure img")
    assert image.count() == 1
    image.evaluate("item => item.decode()")
    metric = image.evaluate("""item => ({naturalWidth: item.naturalWidth,
      naturalHeight: item.naturalHeight, width: item.getBoundingClientRect().width,
      height: item.getBoundingClientRect().height,
      right: item.getBoundingClientRect().right})""")
    assert metric["naturalWidth"] > 0 and metric["naturalHeight"] > 0
    assert metric["right"] <= page.viewport_size["width"] + 2
    assert page.locator("#read-p293-b002 .figure-image-link").get_attribute(
        "href").endswith("assets/part-IV-emblem.png")
    assert page.locator("#read-p293-b002 figcaption").count() == 0
    image.screenshot(path=str(QA_DIR / f"figure-{suffix}.png"))
    return metric


def check_toc(page, width):
    if width < 800:
        page.locator("#toc-toggle").click()
        assert page.locator("#toc-dialog").evaluate("item => item.open")
        page.locator("#reader-toc-mobile .toc-chapter-link.chapter-current").click()
        assert not page.locator("#toc-dialog").evaluate("item => item.open")
        page.evaluate("history.replaceState(null, '', location.pathname + location.search)")
    else:
        assert page.locator("#reader-toc .toc-chapter-link.chapter-current").is_visible()


def check_progress(page, chapter_id, last):
    page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    try:
        page.wait_for_function("""({key, chapter, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === chapter && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "chapter": chapter_id, "last": last}, timeout=5000)
    except PlaywrightTimeoutError:
        state = page.evaluate("""key => ({
          saved: localStorage.getItem(key), progress: document.querySelector('#reading-progress').style.width,
          y: scrollY, inner: innerHeight, height: document.documentElement.scrollHeight,
          hash: location.hash, lastTop: document.querySelector('#read-p293-b002')?.getBoundingClientRect().top
        })""", PROGRESS_KEY)
        print("PROGRESS_DEBUG", chapter_id, json.dumps(state, ensure_ascii=True), flush=True)
        raise
    restored = []
    for _ in range(3):
        page.reload()
        page.wait_for_function("""({key, chapter, last}) => {
          const saved = JSON.parse(localStorage.getItem(key) || '{}');
          return saved.chapter === chapter && saved.block === last &&
            document.querySelector('#reading-progress').style.width === '100%';
        }""", arg={"key": PROGRESS_KEY, "chapter": chapter_id, "last": last})
        restored.append(page.evaluate("""last => ({
          y: Math.round(scrollY),
          top: Math.round(document.querySelector('#' + last).getBoundingClientRect().top),
          progress: document.querySelector('#reading-progress').style.width
        })""", last))
    assert len({item["y"] for item in restored}) == 1, restored
    assert len({item["top"] for item in restored}) == 1, restored
    return restored


def check_navigation(page, chapter_id):
    nav = page.locator("#chapter-navigation .chapter-navigation-link")
    hrefs = nav.evaluate_all("items => items.map(item => item.getAttribute('href'))")
    if chapter_id == "IV":
        assert len(hrefs) == 2 and "chapter=19" in hrefs[0] and "chapter=IV-intro" in hrefs[1], hrefs
        nav.nth(1).click()
        page.locator("#read-p295-b008").wait_for()
        assert "chapter=IV-intro" in page.url
    else:
        assert len(hrefs) == 1 and "chapter=IV" in hrefs[0], hrefs
        nav.first.click()
        page.locator("#read-p293-b002").wait_for()
        assert "chapter=IV" in page.url
    return hrefs


def short_last_lines(page):
    return page.locator(".reading-block:not(.reading-figure):not(.reading-list)").evaluate_all("""items => {
      const results = [];
      for (const item of items) {
        const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
        const lines = new Map();
        while (walker.nextNode()) {
          const node = walker.currentNode;
          for (let i = 0; i < node.length; i++) {
            const range = document.createRange();
            range.setStart(node, i);
            range.setEnd(node, i + 1);
            const rect = range.getBoundingClientRect();
            if (rect.width < 0.1 || rect.height < 0.1) continue;
            const key = Math.round(rect.top);
            lines.set(key, (lines.get(key) || '') + node.textContent[i]);
          }
        }
        const rendered = [...lines.values()].map(line => line.trim()).filter(Boolean);
        const last = rendered.at(-1) || '';
        if (rendered.length > 1 && [...last].length <= 3)
          results.push({id: item.id, last, lines: rendered.length});
      }
      return results;
    }""")


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
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme=mode,
                service_workers="block",
            )
            if not FORMAL:
                context.route("**/books.js", lambda route: route.fulfill(
                    body=BOOK_SCRIPT, content_type="application/javascript"))
            for chapter_id, draft in (("IV", PART), ("IV-intro", INTRO)):
                page = context.new_page()
                errors, failed = [], []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on("requestfailed", lambda request: failed.append(request.url))
                page.on("response", lambda response: failed.append(
                    f"{response.status}: {response.url}") if response.status >= 400 else None)
                if FORMAL:
                    page.goto(base + "?book=mackay-information-theory-2003&chapter=19")
                    page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=IV']").click()
                    page.locator("#read-p293-b002").wait_for()
                    if chapter_id == "IV-intro":
                        page.locator("#chapter-navigation .chapter-navigation-link[href*='chapter=IV-intro']").click()
                else:
                    page.goto(base + f"?book=mackay-information-theory-2003&chapter={chapter_id}")
                last = f"read-{draft['blocks'][-1]['id']}"
                page.locator(f"#{last}").wait_for()
                assert f"chapter={chapter_id}" in page.url
                assert page.evaluate("document.documentElement.dataset.theme") == mode
                suffix = f"{chapter_id}-{width}-{mode}"
                blocks = check_structure(page, draft, chapter_id)
                check_toc(page, width)
                figure = check_figure(page, suffix) if chapter_id == "IV" else None
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
                page.screenshot(path=str(QA_DIR / f"top-{suffix}.png"))
                page.screenshot(path=str(QA_DIR / f"full-{suffix}.png"), full_page=True)
                if chapter_id == "IV-intro":
                    page.locator("#read-p294-b005").screenshot(path=str(QA_DIR / f"list-{suffix}.png"))
                    page.locator("#read-p295-b005").scroll_into_view_if_needed()
                    page.screenshot(path=str(QA_DIR / f"theme-{suffix}.png"))
                restored = check_progress(page, chapter_id, last)
                page.screenshot(path=str(QA_DIR / f"bottom-{suffix}.png"))
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                assert not errors and not failed, (suffix, errors, failed)
                short_lines = short_last_lines(page)
                assert not [item for item in short_lines if len(item["last"]) <= 2], (
                    suffix, short_lines)
                navigation = check_navigation(page, chapter_id)
                print(json.dumps({"view": suffix, "blocks": blocks, "figure": figure,
                                  "navigation": navigation, "restored": restored,
                                  "short_last_lines": short_lines,
                                  "errors": errors, "failed": failed}, ensure_ascii=True))
                page.close()
            context.close()
        browser.close()
    print(f"PASS: Part IV {'registered pages' if FORMAL else 'unpublished drafts'}, six viewports, "
          f"part_sha256={hashlib.sha256(PART_BYTES).hexdigest()}, "
          f"intro_sha256={hashlib.sha256(INTRO_BYTES).hexdigest()}, screenshots={QA_DIR}")
finally:
    server.shutdown()
    server.server_close()
