"""Check an unpublished MacKay chapter 13 draft in the reader."""

import argparse
import json
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--full", action="store_true", help="check the full 334-block draft")
args = parser.parse_args()
draft_name = "chapter-13.draft.json" if args.full else "chapter-13.partial.json"
DRAFT = json.loads((BOOK / draft_name).read_text(encoding="utf-8"))
BOOK_SCRIPT = (ROOT / "books.js").read_text(encoding="utf-8") + """
const chapters13Preview = books.find(item => item.id === "mackay-information-theory-2003").chapters;
const oldChapter13 = chapters13Preview.findIndex(item => item.id === "13");
if (oldChapter13 >= 0) chapters13Preview.splice(oldChapter13, 1);
chapters13Preview.push({
  id: "13", number: "13", title: "二元码",
  content: "books/mackay-information-theory-2003/" + """ + json.dumps(draft_name) + """
});
"""
PROGRESS_KEY = "intelligence-library:progress:v2:mackay-information-theory-2003"
FIGURE_IDS = tuple(block["id"] for block in DRAFT["blocks"] if block["kind"] == "figure")
EXERCISE_LABELS = [block["label"] for block in DRAFT["blocks"] if block["kind"] == "exercise"]
TABLE_13_16 = [
    ["0000000", "0101101", "1001110", "1100011"],
    ["0010111", "0111010", "1011001", "1110100"],
]
FORMULA_TARGETS = {
    "p229-b007": "(13.28)",
    "p231-b007": "(13.38)",
    "p233-b007": "(13.40)",
    "p233-b010": "(13.41)",
}
if args.full:
    FORMULA_TARGETS.update({
        "p235-b014": "(13.44)",
        "p238-b003": "",
        "p238-b005": "",
    })
EXPECTED = {
    "blocks": 334 if args.full else 246,
    "formulas": 58 if args.full else 41,
    "numbers": 56 if args.full else 41,
    "tables": 5 if args.full else 4,
    "exercises": 22 if args.full else 15,
    "toc": 15 if args.full else 14,
}
assert len(DRAFT["blocks"]) == EXPECTED["blocks"]
assert len(DRAFT["toc"]) == EXPECTED["toc"]
assert len(EXERCISE_LABELS) == EXPECTED["exercises"]
assert len(FIGURE_IDS) == 16


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/"

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        for width, dark in ((1440, False), (390, False), (390, True),
                            (350, False), (350, True)):
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme="dark" if dark else "light",
                service_workers="block",
                permissions=["clipboard-read", "clipboard-write"],
            )
            context.route("**/books.js", lambda route: route.fulfill(
                body=BOOK_SCRIPT, content_type="application/javascript"))
            page = context.new_page()
            errors = []
            failed_resources = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_resources.append(request.url))
            page.on("response", lambda response: failed_resources.append(
                f"{response.status}: {response.url}") if response.status >= 400 else None)
            page.goto(base + "?book=mackay-information-theory-2003&chapter=13")
            page.locator(".reading-block").first.wait_for()

            assert page.locator(".reading-block").count() == EXPECTED["blocks"]
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".book-formula math").count() == EXPECTED["formulas"]
            assert page.locator(".formula-number").all_text_contents() == [
                f"(13.{number})" for number in range(1, EXPECTED["numbers"] + 1)]
            assert page.locator("math merror, .formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 16
            assert page.locator(".book-table").count() == EXPECTED["tables"]
            for table_block in (block for block in DRAFT["blocks"] if block["kind"] == "table"):
                actual_rows = page.locator(f"#read-{table_block['id']} .book-table tr").evaluate_all(
                    "rows => rows.map(row => [...row.cells].map(cell => cell.textContent.trim()))")
                expected_rows = [[cell["text"] for cell in row] for row in table_block["rows"]]
                assert [len(row) for row in actual_rows] == [len(row) for row in expected_rows]
                mismatches = [(actual, expected)
                              for actual_row, expected_row in zip(actual_rows, expected_rows)
                              for actual, expected in zip(actual_row, expected_row)
                              if ("$" in expected and not actual) or
                              ("$" not in expected and actual != expected)]
                assert not mismatches, (table_block["id"], mismatches[:3])
            assert page.locator(".book-exercise-label").all_text_contents() == EXERCISE_LABELS
            assert page.locator(".book-exercise-icon").count() == sum(
                bool(block.get("recommendedIcon")) for block in DRAFT["blocks"])
            assert page.locator(".toc-chapter-link.chapter-current").count() == 2
            toc_targets = page.locator("#reader-toc .toc-section-link").evaluate_all(
                "links => links.map(link => link.hash.slice(1))")
            assert toc_targets == [f"read-{item['block']}" for item in DRAFT["toc"][1:]]
            assert all(page.locator(f"#{target}").count() == 1 for target in toc_targets)

            table = page.locator("#read-p229-b009")
            table.scroll_into_view_if_needed()
            cells = table.locator(".book-table tr").evaluate_all(
                "rows => rows.map(row => [...row.cells].map(cell => cell.textContent.trim()))")
            assert cells == TABLE_13_16
            table_metric = table.locator(".table-scroll").evaluate(
                "item => ({client: item.clientWidth, scroll: item.scrollWidth})")
            table.screenshot(path=str(Path(tempfile.gettempdir()) /
                                      f"mackay-ch13-table-13-16-{width}-{int(dark)}.png"))
            assert "表 13.16" in page.locator("#read-p229-b010").inner_text()
            if width <= 390:
                page.screenshot(path=str(Path(tempfile.gettempdir()) /
                                         f"mackay-ch13-table-13-16-context-{width}-{int(dark)}.png"))
            assert table_metric["scroll"] <= table_metric["client"] + 2, table_metric

            gf8_metric = None
            gf8_copied = None
            if args.full:
                gf8 = page.locator("#read-p236-b006")
                gf8.scroll_into_view_if_needed()
                expected_gf8 = [[cell["text"] for cell in row] for row in next(
                    block for block in DRAFT["blocks"] if block["id"] == "p236-b006")["rows"]]
                assert len(expected_gf8) == 8 and all(len(row) == 8 for row in expected_gf8)
                actual_gf8 = gf8.locator(".book-table tr").evaluate_all(
                    "rows => rows.map(row => [...row.cells].map(cell => cell.textContent.trim()))")
                assert actual_gf8 == expected_gf8
                assert gf8.locator(".book-table td code").count() == 64
                assert gf8.locator(".book-table td code").evaluate_all(
                    "items => items.every(item => getComputedStyle(item).whiteSpace === 'nowrap')")
                gf8_scroll = gf8.locator(".table-scroll")
                gf8_metric = gf8_scroll.evaluate("""item => ({
                  client: item.clientWidth, scroll: item.scrollWidth,
                  hint: getComputedStyle(item, '::before').content
                })""")
                gf8.screenshot(path=str(Path(tempfile.gettempdir()) /
                                        f"mackay-ch13-full-gf8-{width}-{int(dark)}-left.png"))
                if width <= 390:
                    assert gf8_metric["scroll"] > gf8_metric["client"] + 200, gf8_metric
                    assert "左右滑动查看完整码字表" in gf8_metric["hint"], gf8_metric
                    gf8_scroll.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert gf8_scroll.evaluate("item => item.scrollLeft") >= (
                        gf8_metric["scroll"] - gf8_metric["client"] - 2)
                    gf8.screenshot(path=str(Path(tempfile.gettempdir()) /
                                            f"mackay-ch13-full-gf8-{width}-{int(dark)}-right.png"))
                    gf8_scroll.evaluate("item => item.scrollLeft = 0")
                else:
                    assert gf8_metric["scroll"] <= gf8_metric["client"] + 2, gf8_metric
                gf8.locator(".book-table").evaluate("""item => {
                  const selection = getSelection();
                  selection.removeAllRanges();
                  const range = document.createRange();
                  range.selectNodeContents(item);
                  selection.addRange(range);
                }""")
                page.keyboard.press("Control+C")
                gf8_copied = page.evaluate("navigator.clipboard.readText()")
                assert all(word in gf8_copied for row in expected_gf8 for word in row)
                page.evaluate("getSelection().removeAllRanges()")

            formula_metrics = page.locator(".book-formula").evaluate_all("""items => items.map(item => {
              const scroller = item.querySelector('.formula-scroll');
              const number = item.querySelector('.formula-number');
              const hint = item.parentElement.querySelector('.formula-view-hint');
              return {number: number?.textContent, client: scroller.clientWidth,
                scroll: scroller.scrollWidth,
                hint: !!(hint && !hint.hidden && getComputedStyle(hint).display !== 'none'),
                separated: !number || number.getBoundingClientRect().left >=
                  scroller.getBoundingClientRect().right - 1};
            })""")
            assert all(item["separated"] for item in formula_metrics), formula_metrics
            assert all(item["scroll"] <= item["client"] + 2 or width > 800 or item["hint"]
                       for item in formula_metrics), formula_metrics
            for scroller in page.locator(".book-formula .formula-scroll").all():
                amount = scroller.evaluate("item => item.scrollWidth - item.clientWidth")
                if amount > 2:
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    assert scroller.evaluate("item => item.scrollLeft") >= amount - 2
                    scroller.evaluate("item => item.scrollLeft = 0")

            copied_lengths = {}
            target_metrics = {}
            for block_id, number in FORMULA_TARGETS.items():
                block = page.locator(f"#read-{block_id}")
                block.scroll_into_view_if_needed()
                if number:
                    assert block.locator(".formula-number").inner_text() == number
                else:
                    assert block.locator(".formula-number").count() == 0
                math = block.locator("math")
                assert math.locator("merror").count() == 0
                block.screenshot(path=str(Path(tempfile.gettempdir()) /
                                          f"mackay-ch13-formula-{block_id}-{width}-{int(dark)}.png"))
                scroller = block.locator(".formula-scroll")
                metric = scroller.evaluate(
                    "item => ({client: item.clientWidth, scroll: item.scrollWidth})")
                target_metrics[number] = metric
                if metric["scroll"] > metric["client"] + 2 and width <= 390:
                    scroller.evaluate("item => item.scrollLeft = item.scrollWidth")
                    page.screenshot(path=str(Path(tempfile.gettempdir()) /
                                             f"mackay-ch13-formula-{block_id}-{width}-{int(dark)}-right.png"))
                    scroller.evaluate("item => item.scrollLeft = 0")
                math.evaluate("""item => {
                  const selection = getSelection();
                  selection.removeAllRanges();
                  const range = document.createRange();
                  range.selectNodeContents(item);
                  selection.addRange(range);
                }""")
                selected = page.evaluate("getSelection().toString()")
                page.keyboard.press("Control+C")
                copied = page.evaluate("navigator.clipboard.readText()")
                assert len(copied) >= len(selected) and len(selected) > 15, (
                    block_id, len(selected), len(copied), copied[:80])
                if number:
                    assert "1" in copied and ("0" in copied or "⋅" in copied)
                copied_lengths[block_id] = len(copied)
                page.evaluate("getSelection().removeAllRanges()")
            line_38 = page.locator("#read-p231-b007 mtable mtr:first-child > mtd:nth-child(4)").evaluate(
                "item => getComputedStyle(item).borderRightWidth")
            line_41 = page.locator("#read-p233-b010 mtable").evaluate("""item => ({
              fifth: getComputedStyle(item.querySelector('mtr:first-child > mtd:nth-child(5)')).borderRightWidth,
              tenth: getComputedStyle(item.querySelector('mtr:first-child > mtd:nth-child(10)')).borderRightWidth,
              sixthRow: getComputedStyle(item.querySelector('mtr:nth-child(6) > mtd:first-child')).borderTopWidth
            })""")
            assert line_38 == "1px" and all(value == "1px" for value in line_41.values())
            if args.full:
                line_44 = page.locator("#read-p235-b014 mtable mtr:first-child").evaluate("""item => ({
                  fourth: getComputedStyle(item.querySelector('mtd:nth-child(4)')).borderRightWidth,
                  fifth: getComputedStyle(item.querySelector('mtd:nth-child(5)')).borderRightWidth
                })""")
                assert line_44 == {"fourth": "1px", "fifth": "0px"}, line_44

            for figure_id in FIGURE_IDS:
                figure = page.locator(f"#read-{figure_id}")
                figure.scroll_into_view_if_needed()
                image = figure.locator(".book-figure img")
                image.evaluate("item => item.decode()")
                assert image.evaluate("item => item.naturalWidth > 0 && item.naturalHeight > 0")
            figure17 = page.locator("#read-p233-b011")
            assert all(word in figure17.locator(".figure-caption").inner_text()
                       for word in ("图 13.17", "15", "10", "Petersen"))
            figure17.scroll_into_view_if_needed()
            figure17.screenshot(path=str(Path(tempfile.gettempdir()) /
                                         f"mackay-ch13-figure-13-17-{width}-{int(dark)}.png"))
            media = figure17.locator(".figure-media")
            figure_metric = media.evaluate(
                "item => ({client: item.clientWidth, scroll: item.scrollWidth})")
            if figure_metric["scroll"] > figure_metric["client"] + 2:
                assert figure17.locator(".figure-view-hint").count() == 1
                media.evaluate("item => item.scrollLeft = item.scrollWidth")
                assert media.evaluate("item => item.scrollLeft") >= (
                    figure_metric["scroll"] - figure_metric["client"] - 2)
                page.screenshot(path=str(Path(tempfile.gettempdir()) /
                                         f"mackay-ch13-figure-13-17-{width}-{int(dark)}-right.png"))
                media.evaluate("item => item.scrollLeft = 0")
            for icon in page.locator(".book-exercise-icon").all():
                icon.scroll_into_view_if_needed()
                icon.evaluate("item => item.decode()")
                assert icon.evaluate("item => item.naturalWidth > 0")
            for exercise_id in ("p222-b007", "p232-b011", "p233-b004", "p233-b013"):
                exercise = page.locator(f"#read-{exercise_id}")
                exercise.scroll_into_view_if_needed()
                exercise.screenshot(path=str(Path(tempfile.gettempdir()) /
                                             f"mackay-ch13-exercise-{exercise_id}-{width}-{int(dark)}.png"))

            if args.full:
                emphasis = {
                    "p234-b010": {"em": ("或反过来",)},
                    "p234-b014": {"strong": ("三人", "七人")},
                    "p235-b012": {"em": ("正交", "反之亦然")},
                    "p236-b001": {"em": ("任意",)},
                    "p238-b013": {"em": ("不同", "相同", "另一种")},
                    "p239-b001": {"em": ("另一种",)},
                }
                for block_id, tags in emphasis.items():
                    for tag, words in tags.items():
                        actual = page.locator(f"#read-{block_id} {tag}").all_text_contents()
                        assert all(word in actual for word in words), (block_id, tag, actual)
                assert page.locator("#read-p234-b014 strong").first.evaluate(
                    "item => Number(getComputedStyle(item).fontWeight) >= 600")
                assert page.locator("#read-p238-b013 em").first.evaluate(
                    "item => getComputedStyle(item).fontStyle === 'italic'")
                page.locator("#read-p238-b013").scroll_into_view_if_needed()
                page.locator("#read-p238-b013").screenshot(
                    path=str(Path(tempfile.gettempdir()) /
                             f"mackay-ch13-full-emphasis-{width}-{int(dark)}.png"))

            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            progress_target = page.locator("#read-p229-b009")
            progress_target.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.wait_for_function(
                "key => JSON.parse(localStorage.getItem(key) || '{}').block === 'read-p229-b009'",
                arg=PROGRESS_KEY)
            restored = []
            for _ in range(3):
                page.reload()
                page.wait_for_function("""() => {
                  const item = document.querySelector('#read-p229-b009');
                  return item && Math.abs(item.getBoundingClientRect().top - 85) <= 2;
                }""")
                restored.append(page.evaluate("""key => ({
                  block: JSON.parse(localStorage.getItem(key)).block,
                  top: Math.round(document.querySelector('#read-p229-b009').getBoundingClientRect().top),
                  y: Math.round(scrollY)
                })""", PROGRESS_KEY))
            assert all(item["block"] == "read-p229-b009" and item["top"] == 85
                       for item in restored) and len({item["y"] for item in restored}) == 1
            full_progress = {}
            if args.full:
                for target_id in ("p236-b006", "p239-b001"):
                    target = page.locator(f"#read-{target_id}")
                    target.evaluate("item => item.scrollIntoView({block: 'start', behavior: 'instant'})")
                    page.wait_for_function("""({key, block}) =>
                      JSON.parse(localStorage.getItem(key) || '{}').block === block""",
                      arg={"key": PROGRESS_KEY, "block": f"read-{target_id}"})
                    positions = []
                    for _ in range(3):
                        page.reload()
                        page.wait_for_function("""({key, block}) =>
                          document.querySelector('#' + block) &&
                          JSON.parse(localStorage.getItem(key) || '{}').block === block""",
                          arg={"key": PROGRESS_KEY, "block": f"read-{target_id}"})
                        positions.append(page.evaluate("""({key, block}) => ({
                          saved: JSON.parse(localStorage.getItem(key)).block,
                          top: Math.round(document.querySelector('#' + block).getBoundingClientRect().top),
                          y: Math.round(scrollY)
                        })""", {"key": PROGRESS_KEY, "block": f"read-{target_id}"}))
                    assert all(item["saved"] == f"read-{target_id}" for item in positions)
                    assert len({item["top"] for item in positions}) == 1, positions
                    assert len({item["y"] for item in positions}) == 1, positions
                    full_progress[target_id] = positions
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors and not failed_resources, (errors, failed_resources)
            page.get_by_role("link", name="← 上一章 · 导页 关于第 13 章").click()
            page.locator(".reading-block").first.wait_for()
            assert "chapter=13-intro" in page.url and page.locator(".reading-block").count() == 3
            if args.full:
                next_link = page.get_by_role("link", name="下一章 → · 13 二元码")
                assert next_link.count() == 1
                next_link.click()
                page.locator("#read-p239-b001").wait_for()
                assert "chapter=13" in page.url and page.locator(".reading-block").count() == 334

            print(f"{width} {'dark' if dark else 'light'}: "
                  f"{EXPECTED['blocks']} blocks, {EXPECTED['formulas']} formulas, "
                  f"formula_overflow={sum(item['scroll'] > item['client'] + 2 for item in formula_metrics)}, "
                  f"table={table_metric}, target_formulas={target_metrics}, "
                  f"copied={copied_lengths}, GF8={gf8_metric}, GF8_copy={len(gf8_copied or '')}, "
                  f"figure13.17={figure_metric}, progress={restored}, full_progress={full_progress}")
            context.close()
        browser.close()
    print(f"PASS: chapter 13 unpublished {'full' if args.full else 'partial'} draft, five viewports, "
          "tables/formulas/figures/exercises/navigation/progress")
finally:
    server.shutdown()
    server.server_close()
