"""Verify reviewed MacKay chapters through their real reader URLs and files."""

import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
BOOK_ID = "mackay-information-theory-2003"
EXPECTED_TOC_LINKS = 162  # 81 registered entries in each of the desktop and mobile menus


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
        for width, dark in ((1440, False), (390, True)):
            context = browser.new_context(
                viewport={"width": width, "height": 844},
                color_scheme="dark" if dark else "light",
                service_workers="block",
            )
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base)
            shelf = page.get_by_text("信息论、推断与学习算法").first
            assert shelf.count() == 1
            page.goto(base + f"?book={BOOK_ID}&chapter=00")
            page.locator(".reading-block").first.wait_for()
            assert page.locator(".reading-block").count() == 132
            assert page.locator(".book-formula math").count() == 17
            assert page.locator(".book-figure img").count() == 10
            assert page.locator("#reader-status:not([hidden])").count() == 0
            for image in page.locator(".book-figure img").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            page.get_by_role("link", name="下一章 → · 1 信息论导论").click()
            page.locator(".reading-heading h1").get_by_text("第 1 章 信息论导论").wait_for()
            assert page.locator(".reading-block").count() == 252
            assert page.locator(".book-formula math").count() == 43
            assert page.locator(".book-figure img").count() == 16
            assert page.locator(".book-exercise-icon").count() == 8
            assert page.locator("#reader-status:not([hidden])").count() == 0
            assert page.get_by_role("link", name="← 上一章 · 前置 前言与第一章预备知识").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS  # desktop and mobile menus
            for image in page.locator(".book-figure img").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            target = page.locator("#read-p023-b002")
            target.scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '01'",
                arg=BOOK_ID,
            )
            saved = page.evaluate(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id))",
                BOOK_ID,
            )
            assert saved["block"].startswith("read-p"), saved
            page.goto(base + f"?book={BOOK_ID}")
            page.locator(".reading-heading h1").get_by_text("第 1 章 信息论导论").wait_for()
            page.get_by_role("link", name="下一章 → · 2 概率、熵与推断").click()
            page.locator(".reading-heading h1").get_by_text("第 2 章 概率、熵与推断").wait_for()
            assert page.locator(".reading-block").count() == 457
            assert page.locator(".book-formula math").count() == 122
            assert page.locator(".book-figure img").count() == 13
            assert page.locator(".book-exercise-icon").count() == 10
            assert page.locator("#reader-status:not([hidden])").count() == 0
            assert page.get_by_role("link", name="← 上一章 · 1 信息论导论").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS  # desktop and mobile menus
            assert page.locator("#read-box-2-4 strong").count() == 4
            assert page.locator("#read-p050-b002 figcaption math").count() == 8
            for image in page.locator(".book-figure img").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            target = page.locator("#read-p043-b008")
            target.scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '02'",
                arg=BOOK_ID,
            )
            page.goto(base + f"?book={BOOK_ID}")
            page.locator(".reading-heading h1").get_by_text("第 2 章 概率、熵与推断").wait_for()
            page.get_by_role("link", name="下一章 → · 导页 关于第 3 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 3 章").wait_for()
            assert page.locator(".reading-block").count() == 10
            assert page.locator(".book-exercise-label").count() == 4
            intro_image = page.locator(".book-figure img")
            assert intro_image.count() == 1
            intro_image.evaluate("image => image.decode()")
            assert page.get_by_role("link", name="← 上一章 · 2 概率、熵与推断").count() == 1
            page.get_by_role("link", name="下一章 → · 3 进一步讨论推断").click()
            page.locator(".reading-heading h1").get_by_text("第 3 章 进一步讨论推断").wait_for()
            assert page.locator(".reading-block").count() == 226
            assert page.locator(".book-formula math").count() == 48
            assert page.locator(".book-figure img").count() == 12
            assert page.locator(".book-exercise-icon").count() == 3
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 3 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for image in page.locator(".book-figure img").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            page.locator("#read-p075-b010").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '03'",
                arg=BOOK_ID,
            )
            page.goto(base + f"?book={BOOK_ID}")
            page.locator(".reading-heading h1").get_by_text("第 3 章 进一步讨论推断").wait_for()
            assert page.locator("#reader-status:not([hidden])").count() == 0
            page.get_by_role("link", name="下一章 → · 第一部分 数据压缩").click()
            page.locator(".reading-heading h1").get_by_text("第一部分 数据压缩").wait_for()
            assert page.locator(".reading-block").count() == 2
            emblem = page.locator(".book-figure img")
            assert emblem.count() == 1
            emblem.evaluate("image => image.decode()")
            page.get_by_role("link", name="下一章 → · 导页 关于第 4 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 4 章").wait_for()
            assert page.locator(".reading-block").count() == 11
            assert page.locator(".book-exercise-label").count() == 1
            assert page.locator(".book-table.notation-table tr").count() == 7
            page.get_by_role("link", name="下一章 → · 4 信源编码定理").click()
            page.locator(".reading-heading h1").get_by_text("第 4 章 信源编码定理").wait_for()
            assert page.locator(".reading-block").count() == 301
            assert page.locator(".book-formula math").count() == 55
            assert page.locator(".book-figure img").count() == 15
            assert page.locator(".book-inline-code").count() >= 10
            assert page.locator(".reading-block em").count() >= 5
            assert page.locator(".reading-block strong").count() >= 20
            assert page.locator(".reading-reference[href^='http']").count() >= 1
            assert page.locator(".book-footnote-ref a[href='#read-fn-4-1']").count() == 1
            assert page.locator("#read-fn-4-1.reading-footnote").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 4 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for image in page.locator(".book-figure img").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            page.locator("#read-p099-b010").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '04'",
                arg=BOOK_ID,
            )
            page.goto(base + f"?book={BOOK_ID}")
            page.locator(".reading-heading h1").get_by_text("第 4 章 信源编码定理").wait_for()
            assert page.locator("#reader-status:not([hidden])").count() == 0
            page.get_by_role("link", name="下一章 → · 导页 关于第 5 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 5 章").wait_for()
            assert page.locator(".reading-block").count() == 7
            assert page.locator(".book-table.notation-table tr").count() == 3
            assert page.locator(".inline-math math").count() == 13
            page.get_by_role("link", name="下一章 → · 5 符号编码").click()
            page.locator(".reading-heading h1").get_by_text("第 5 章 符号编码").wait_for()
            assert page.locator(".reading-block").count() == 281
            assert page.locator(".book-formula math").count() == 48
            assert page.locator(".book-figure img").count() == 8
            assert page.locator(".book-exercise-icon").count() == 6
            assert page.locator(".book-table").count() == 10
            algorithm = page.locator("#read-box-5-4.book-box.outlined-box")
            assert algorithm.count() == 1 and algorithm.locator("ol > li").count() == 2
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 5 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for image in page.locator(".book-figure img, .book-exercise-icon").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            page.locator("#read-p118-b013").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '05'",
                arg=BOOK_ID,
            )
            page.goto(base + f"?book={BOOK_ID}")
            page.locator(".reading-heading h1").get_by_text("第 5 章 符号编码").wait_for()
            assert page.locator("#reader-status:not([hidden])").count() == 0
            page.get_by_role("link", name="下一章 → · 导页 关于第 6 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 6 章").wait_for()
            assert page.locator(".reading-block").count() == 3
            page.get_by_role("link", name="下一章 → · 6 流编码").click()
            page.locator(".reading-heading h1").get_by_text("第 6 章 流编码").wait_for()
            assert page.locator(".reading-block").count() == 273
            assert page.locator(".book-formula math").count() == 32
            assert page.locator(".book-figure img").count() == 11
            assert page.locator(".book-exercise-icon").count() == 8
            assert page.locator(".book-table.code-table").count() == 4
            assert page.locator("#read-box-6-3.book-box.outlined-box .reading-code").count() == 1
            assert page.locator(".book-footnote-ref a").count() == 5
            assert page.locator(".reading-footnote").count() == 5
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 6 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for image in page.locator(".book-figure img, .book-exercise-icon").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            if width == 390:
                assert page.locator("#read-p131-b006 .table-scroll").evaluate(
                    "node => node.scrollWidth > node.clientWidth")
            page.locator("#read-p143-b010").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '06'",
                arg=BOOK_ID,
            )
            page.goto(base + f"?book={BOOK_ID}")
            page.locator(".reading-heading h1").get_by_text("第 6 章 流编码").wait_for()
            assert page.locator("#reader-status:not([hidden])").count() == 0
            page.get_by_role("link", name="下一章 → · 7 整数编码").click()
            page.locator(".reading-heading h1").get_by_text("第 7 章 整数编码").wait_for()
            assert page.locator(".reading-block").count() == 74
            assert page.locator(".book-formula math").count() == 7
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-table.code-table").count() == 5
            assert page.locator("#read-box-7-4.book-box.outlined-box .reading-code").count() == 1
            assert page.locator("#read-p146-b016.reading-code").count() == 1
            assert page.locator(".reading-quote").filter(has_text="译注（非原书正文）").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 6 流编码").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            if width == 390:
                assert page.locator("#read-p148-b002 .table-scroll").evaluate(
                    "node => node.scrollWidth > node.clientWidth")
            page.locator("#read-p148-b002").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '07'",
                arg=BOOK_ID,
            )
            page.goto(base + f"?book={BOOK_ID}")
            page.locator(".reading-heading h1").get_by_text("第 7 章 整数编码").wait_for()
            assert page.locator("#reader-status:not([hidden])").count() == 0
            page.get_by_role("link", name="下一章 → · 第二部分 有噪信道编码").click()
            page.locator("#read-p149-b001 h1").wait_for()
            assert page.locator(".reading-block").count() == 2
            assert page.locator("#read-p149-b001 h1").inner_text() == "第二部分\n有噪信道编码"
            emblem = page.locator(".book-figure img")
            assert emblem.count() == 1
            emblem.evaluate("image => image.decode()")
            assert page.get_by_role("link", name="← 上一章 · 7 整数编码").count() == 1
            page.get_by_role("link", name="下一章 → · 8 相依随机变量").click()
            page.locator(".reading-heading h1").get_by_text("第 8 章 相依随机变量").wait_for()
            assert page.locator(".reading-block").count() == 120
            assert page.locator(".book-formula math").count() == 35
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator(".book-exercise-icon").count() == 5
            assert page.locator(".reading-quote").filter(has_text="技术译注（非原书正文）").count() == 2
            table = page.locator("#read-p152-b014 .table-scroll")
            assert table.locator("tr").count() == 5
            assert all(row.locator("th,td").count() == 5 for row in table.locator("tr").all())
            for image in page.locator(".book-figure img, .book-exercise-icon").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            assert page.get_by_role("link", name="← 上一章 · 第二部分 有噪信道编码").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.locator("#read-p156-b012").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '08'",
                arg=BOOK_ID,
            )
            page.goto(base + f"?book={BOOK_ID}")
            page.locator(".reading-heading h1").get_by_text("第 8 章 相依随机变量").wait_for()
            page.get_by_role("link", name="下一章 → · 导页 关于第 9 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 9 章").wait_for()
            assert page.locator(".reading-block").count() == 2
            assert page.get_by_role("link", name="← 上一章 · 8 相依随机变量").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 9 有噪信道上的通信").click()
            page.locator(".reading-heading h1").get_by_text("第 9 章　有噪信道上的通信").wait_for()
            assert page.locator(".reading-block").count() == 240
            assert page.locator(".book-formula math").count() == 63
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 22
            assert page.locator(".book-exercise-icon").count() == 12
            assert page.locator(".book-table").count() == 3
            assert page.locator(".book-exercise-label").count() == 15
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".reading-quote").filter(has_text="技术译注（非原书正文）").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 9 章").count() == 1
            for image in page.locator(".book-figure img, .book-exercise-icon").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            for table_id in ("p159-b003", "p159-b006", "p165-b004"):
                assert page.locator(f"#read-{table_id} .table-scroll tr").count() == 6
            page.locator("#read-p171-b014").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '09'",
                arg=BOOK_ID,
            )
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 导页 关于第 10 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 10 章").wait_for()
            assert page.locator(".reading-block").count() == 5
            assert page.locator(".reading-quote").filter(has_text="技术译注（非原书正文）").count() == 1
            table = page.locator("#read-p173-b005 .table-scroll")
            assert table.locator("tr").count() == 13
            assert all(row.locator("th,td").count() == 2 for row in table.locator("tr").all())
            assert table.locator("math").count() == 18
            for row, symbol in ((2, "C"), (4, "𝒞"), (7, "s"), (10, "𝐬")):
                assert table.locator("tr").nth(row).locator("math mi").first.text_content() == symbol
            assert page.get_by_role("link", name="← 上一章 · 9 有噪信道上的通信").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator(".formula-fallback").count() == 0
            page.locator("#read-p173-b005").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '10-intro'",
                arg=BOOK_ID,
            )
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 10 有噪信道编码定理").click()
            page.locator(".reading-heading h1").get_by_text("第 10 章　有噪信道编码定理").wait_for()
            assert page.locator(".reading-block").count() == 216
            assert page.locator(".book-formula math").count() == 41
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 15
            assert page.locator(".book-exercise-icon").count() == 1
            assert page.locator(".book-exercise-label").count() == 12
            assert page.locator(".reading-code").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 10 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for image in page.locator(".book-figure img, .book-exercise-icon").all():
                image.scroll_into_view_if_needed()
                image.evaluate("image => image.decode()")
            formula = page.locator("#read-p182-b014 math")
            assert formula.count() == 1
            assert formula.locator("mtable").evaluate(
                "node => getComputedStyle(node).borderTopWidth === '1px' && getComputedStyle(node).borderBottomWidth === '1px'")
            assert formula.locator("mtr").nth(2).locator("mtd").first.evaluate(
                "node => getComputedStyle(node).borderTopWidth === '1px'")
            page.locator("#read-p187-b007").scroll_into_view_if_needed()
            page.wait_for_function(
                "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').chapter === '10'",
                arg=BOOK_ID,
            )
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 导页 关于第 11 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 11 章").wait_for()
            assert page.locator(".reading-block").count() == 16
            assert page.locator(".book-formula math").count() == 4
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.get_by_role("link", name="← 上一章 · 10 有噪信道编码定理").count() == 1
            page.locator("#read-p188-b007").evaluate(
                "node => node.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '11-intro' && progress.block === 'read-p188-b007'; }",
                arg=BOOK_ID,
            )
            for _ in range(3):
                page.reload()
                page.locator("#read-p188-b007").wait_for()
                page.wait_for_function(
                    "id => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}').block === 'read-p188-b007'",
                    arg=BOOK_ID,
                )
                assert abs(page.locator("#read-p188-b007").bounding_box()["y"] - 85) <= 3
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 11 纠错码与实值信道").click()
            page.locator(".reading-heading h1").get_by_text("第 11 章　纠错码与实值信道").wait_for()
            assert page.locator(".reading-block").count() == 225
            assert page.locator(".book-formula math").count() == 44
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 11
            assert page.locator(".book-exercise-label").count() == 10
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 11 章").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            assert page.locator("#read-p199-b006 img").get_attribute("src").endswith("figure-11-8-enhanced.png")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 第三部分 信息论的更多主题").click()
            page.locator(".reading-heading h1").get_by_text("第三部分　信息论的更多主题").wait_for()
            assert page.locator(".reading-block").count() == 2
            assert page.locator(".book-figure img").count() == 1
            page.locator(".book-figure img").evaluate("image => image.decode()")
            assert page.get_by_role("link", name="← 上一章 · 11 纠错码与实值信道").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'III' && progress.block === 'read-p203-b002'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 导页 关于第 12 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 12 章").wait_for()
            assert page.locator(".reading-block").count() == 5
            assert page.locator(".reading-block em").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 第三部分 信息论的更多主题").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '12-intro' && progress.block === 'read-p204-b005'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            page.reload()
            page.locator("#read-p204-b005").wait_for()
            page.wait_for_function("document.querySelector('#reading-progress')?.style.width === '100%'")
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 12 哈希码：用于高效信息检索的编码").click()
            page.locator(".reading-heading h1").get_by_text("第 12 章　哈希码：用于高效信息检索的编码").wait_for()
            assert page.locator(".reading-block").count() == 136
            assert page.locator(".book-formula math").count() == 11
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 3
            assert page.locator(".book-exercise-icon").count() == 3
            assert page.locator(".book-exercise-label").count() == 8
            assert page.locator(".reading-code").count() == 2
            assert page.locator(".book-footnote-ref a").count() == 1
            assert page.locator(".reading-footnote").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 12 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            assert page.locator("#read-p213-b012 munder > mrow").count() == 2
            assert all(item.evaluate("node => getComputedStyle(node).borderBottomWidth") == "1px"
                       for item in page.locator("#read-p213-b012 munder > mrow").all())
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 导页 关于第 13 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 13 章").wait_for()
            assert page.locator(".reading-block").count() == 3
            assert page.locator(".reading-block em").count() == 1
            assert page.locator(".reading-block math").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 12 哈希码：用于高效信息检索的编码").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 13 二元码").click()
            page.locator(".reading-heading h1").get_by_text("第 13 章　二元码").wait_for()
            assert page.locator(".reading-block").count() == 334
            assert page.locator(".book-formula math").count() == 58
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 16
            assert page.locator(".book-exercise-icon").count() == 3
            assert page.locator(".book-exercise-label").count() == 22
            assert page.locator(".book-table").count() == 5
            assert page.locator("#read-p236-b006 .book-inline-code").count() == 64
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 13 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            for block, column in (("p231-b007", 4), ("p233-b010", 5),
                                  ("p233-b010", 10), ("p235-b014", 4)):
                cell = page.locator(f"#read-{block} .book-formula math mtr:first-child > mtd:nth-child({column})")
                assert cell.evaluate("node => getComputedStyle(node).borderRightWidth") == "1px"
            assert page.locator("#read-p233-b010 .book-formula math mtr:nth-child(6) > mtd:first-child").evaluate(
                "node => getComputedStyle(node).borderTopWidth") == "1px"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 导页 关于第 14 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 14 章").wait_for()
            assert page.locator(".reading-block").count() == 4
            assert page.locator(".reading-block em").count() == 2
            assert page.get_by_role("link", name="← 上一章 · 13 二元码").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 14 存在非常好的线性码").click()
            page.locator(".reading-heading h1").get_by_text("第 14 章　存在非常好的线性码").wait_for()
            assert page.locator(".reading-block").count() == 56
            assert page.locator(".book-formula math").count() == 19
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 0
            assert page.locator(".book-table").count() == 0
            assert page.locator(".book-exercise-label").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 14 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 15 信息论补充习题").click()
            page.locator(".reading-heading h1").get_by_text("第 15 章　信息论补充习题").wait_for()
            assert page.locator(".reading-block").count() == 102
            assert page.locator(".book-formula math").count() == 11
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 10
            assert page.locator(".book-table").count() == 1
            assert page.locator(".book-exercise-label").count() == 21
            assert page.locator(".book-exercise-icon").count() == 4
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 14 存在非常好的线性码").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            assert page.locator("#read-p248-b017 .book-formula math mtr:first-child > mtd:first-child").evaluate(
                "node => getComputedStyle(node).borderRightWidth") == "1px"
            assert page.locator("#read-p248-b017 .book-formula math mtr:nth-child(2) > mtd:nth-child(2)").evaluate(
                "node => getComputedStyle(node).borderTopWidth") == "1px"
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '15' && progress.block === 'read-p252-b001'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 16 消息传递").click()
            page.locator(".reading-heading h1").get_by_text("第 16 章　消息传递").wait_for()
            assert page.locator(".reading-block").count() == 71
            assert page.locator(".book-formula math").count() == 1
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 12
            assert page.locator(".book-table").count() == 1
            assert page.locator(".book-exercise-label").count() == 4
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 15 信息论补充习题").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            for subitem in ("p255-b004", "p255-b005"):
                assert page.locator(f"#read-{subitem}").evaluate(
                    "node => getComputedStyle(node).marginLeft") == "30px"
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '16' && progress.block === 'read-p259-b003'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 17 受约束的无噪信道上的通信").click()
            page.locator(".reading-heading h1").get_by_text("第 17 章　受约束的无噪信道上的通信").wait_for()
            assert page.locator(".reading-block").count() == 184
            assert page.locator(".book-formula math").count() == 36
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 9
            assert page.locator(".book-table").count() == 6
            assert page.locator(".book-exercise-label").count() == 12
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 16 消息传递").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '17' && progress.block === 'read-p271-b014'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 18 填字游戏与密码破解").click()
            page.locator(".reading-heading h1").get_by_text("第 18 章　填字游戏与密码破解").wait_for()
            assert page.locator(".reading-block").count() == 118
            assert page.locator(".book-formula math").count() == 25
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 6
            assert page.locator(".book-table").count() == 5
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 17 受约束的无噪信道上的通信").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            if width == 390:
                assert page.locator("#read-p279-b001 .table-scroll").evaluate(
                    "node => node.scrollWidth > node.clientWidth")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '18' && progress.block === 'read-p280-b006'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 19 为什么有性生殖？信息获取与进化").click()
            page.locator(".reading-heading h1").get_by_text("第 19 章　为什么有性生殖？信息获取与进化").wait_for()
            assert page.locator(".reading-block").count() == 131
            assert page.locator(".book-formula math").count() == 27
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator(".book-box.outlined-box#read-box-19-2").count() == 1
            assert page.locator("#read-box-19-2 .reading-block").count() == 14
            assert page.locator(".book-exercise-label").count() == 6
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 18 填字游戏与密码破解").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '19' && progress.block === 'read-p292-b009'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 第四部分 概率与推断").click()
            page.locator(".reading-heading h1").filter(has_text="概率与推断").wait_for()
            assert page.locator(".reading-block").count() == 2
            assert page.locator(".book-figure img").count() == 1
            page.locator(".book-figure img").evaluate("image => image.decode()")
            assert page.get_by_role("link", name="← 上一章 · 19 为什么有性生殖？信息获取与进化").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.get_by_role("link", name="下一章 → · 导页 关于第四部分").click()
            page.locator(".reading-heading h1").get_by_text("关于第四部分").wait_for()
            assert page.locator(".reading-block").count() == 18
            assert page.locator(".reading-heading h2").count() == 2
            assert page.locator("ol.book-list").count() == 1
            assert page.locator(".book-formula").count() == 0
            assert page.get_by_role("link", name="← 上一章 · 第四部分 概率与推断").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'IV-intro' && progress.block === 'read-p295-b008'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 20 一个推断任务示例：聚类").click()
            page.locator(".reading-heading h1").get_by_text("第 20 章　一个推断任务示例：聚类").wait_for()
            assert page.locator(".reading-block").count() == 100
            assert page.locator(".book-formula math").count() == 23
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 10
            assert page.locator(".book-box.outlined-box").count() == 2
            assert page.locator(".book-exercise-label").count() == 5
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第四部分").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '20' && progress.block === 'read-p304-b014'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 21 通过完全枚举进行精确推断").click()
            page.locator(".reading-heading h1").get_by_text("第 21 章　通过完全枚举进行精确推断").wait_for()
            assert page.locator(".reading-block").count() == 62
            assert page.locator(".book-formula math").count() == 13
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 7
            assert page.locator(".book-exercise-label").count() == 2
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 20 一个推断任务示例：聚类").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '21' && progress.block === 'read-p311-b002'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 22 最大似然与聚类").click()
            page.locator(".reading-heading h1").get_by_text("第 22 章　最大似然与聚类").wait_for()
            assert page.locator(".reading-block").count() == 160
            assert page.locator(".book-formula math").count() == 42
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 11
            assert page.locator(".book-exercise-label").count() == 13
            assert page.locator(".book-table").count() == 1
            assert page.locator(".book-box.outlined-box").count() == 2
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 21 通过完全枚举进行精确推断").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '22' && progress.block === 'read-p322-b016'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 23 常用的概率分布").click()
            page.locator(".reading-heading h1").get_by_text("第 23 章　常用的概率分布").wait_for()
            assert page.locator(".reading-block").count() == 126
            assert page.locator(".book-formula math").count() == 37
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 9
            assert page.locator(".book-exercise-label").count() == 4
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 22 最大似然与聚类").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '23' && progress.block === 'read-p330-b007'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 24 精确边缘化").click()
            page.locator(".reading-heading h1").get_by_text("第 24 章　精确边缘化").wait_for()
            assert page.locator(".reading-block").count() == 64
            assert page.locator(".book-formula math").count() == 17
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 2
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 23 常用的概率分布").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '24' && progress.block === 'read-p335-b015'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 25 格形图中的精确边缘化").click()
            page.locator(".reading-heading h1").get_by_text("第 25 章　格形图中的精确边缘化").wait_for()
            assert page.locator(".reading-block").count() == 134
            assert page.locator(".book-formula math").count() == 22
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 6
            assert page.locator(".book-exercise-label").count() == 8
            assert page.locator(".book-table").count() == 4
            assert page.locator("#read-p343-b005 .book-table.code-table").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 24 精确边缘化").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '25' && progress.block === 'read-p345-b010'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 26 图中的精确边缘化").click()
            page.locator(".reading-heading h1").get_by_text("第 26 章　图中的精确边缘化").wait_for()
            assert page.locator(".reading-block").count() == 114
            assert page.locator(".book-formula math").count() == 26
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator(".book-exercise-label").count() == 8
            assert page.locator(".book-box.outlined-box#read-box-26-rules").count() == 1
            assert page.locator("#read-box-26-rules .reading-block").count() == 4
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 25 格形图中的精确边缘化").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '26' && progress.block === 'read-p352-b011'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 27 拉普拉斯方法").click()
            page.locator(".reading-heading h1").get_by_text("第 27 章　拉普拉斯方法").wait_for()
            assert page.locator(".reading-block").count() == 41
            assert page.locator(".book-formula math").count() == 14
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 1
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 26 图中的精确边缘化").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.locator(".book-figure img").evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '27' && progress.block === 'read-p354-b020'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 28 模型比较与奥卡姆剃刀").click()
            page.locator(".reading-heading h1").get_by_text("第 28 章　模型比较与奥卡姆剃刀").wait_for()
            assert page.locator(".reading-block").count() == 133
            assert page.locator(".book-formula math").count() == 24
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 11
            assert page.locator(".book-exercise-label").count() == 4
            assert page.locator(".book-table").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 27 拉普拉斯方法").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '28' && progress.block === 'read-p367-b004'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 导页 关于第 29 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 29 章").wait_for()
            assert page.locator(".reading-block").count() == 10
            assert page.locator(".book-formula math").count() == 2
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 0
            assert page.locator(".book-exercise-label").count() == 0
            assert page.get_by_role("link", name="← 上一章 · 28 模型比较与奥卡姆剃刀").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '29-intro' && progress.block === 'read-p368-b010'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 29 蒙特卡罗方法").click()
            page.locator(".reading-heading h1").get_by_text("第 29 章　蒙特卡罗方法").wait_for()
            assert page.locator(".reading-block").count() == 342
            assert page.locator(".book-formula math").count() == 61
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 20
            assert page.locator(".book-exercise-label").count() == 20
            assert page.locator(".book-box.outlined-box").count() == 7
            assert page.locator(".book-code").count() == 5
            assert page.locator(".book-table").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 29 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '29' && progress.block === 'read-p398-b012'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 30 高效蒙特卡罗方法").click()
            page.locator(".reading-heading h1").get_by_text("第 30 章　高效蒙特卡罗方法").wait_for()
            assert page.locator(".reading-block").count() == 126
            assert page.locator(".book-formula math").count() == 19
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator(".book-exercise-label").count() == 11
            assert page.locator(".book-box.outlined-box").count() == 1
            assert page.locator(".book-code").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 29 蒙特卡罗方法").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '30' && progress.block === 'read-p410-b011'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 导页 关于第 31 章").click()
            page.locator(".reading-heading h1").get_by_text("关于第 31 章").wait_for()
            assert page.locator(".reading-block").count() == 4
            assert page.locator(".book-formula math").count() == 0
            assert page.locator(".book-figure img").count() == 0
            assert page.locator(".book-exercise-label").count() == 0
            assert page.get_by_role("link", name="← 上一章 · 30 高效蒙特卡罗方法").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '31-intro' && progress.block === 'read-p411-b004'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 31 Ising 模型").click()
            page.locator(".reading-heading h1").get_by_text("第 31 章　Ising 模型").wait_for()
            assert page.locator(".reading-block").count() == 140
            assert page.locator(".book-formula math").count() == 34
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 19
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 关于第 31 章").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '31' && progress.block === 'read-p424-b006'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 32 精确蒙特卡罗采样").click()
            page.locator(".reading-heading h1").get_by_text("第 32 章　精确蒙特卡罗采样").wait_for()
            assert page.locator(".reading-block").count() == 52
            assert page.locator(".book-formula math").count() == 2
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 6
            assert page.locator(".book-exercise-label").count() == 6
            assert page.locator(".book-footnote").count() == 2
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 31 Ising 模型").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '32' && progress.block === 'read-p433-b005'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 33 变分方法").click()
            page.locator(".reading-heading h1").get_by_text("第 33 章　变分方法").wait_for()
            assert page.locator(".reading-block").count() == 216
            assert page.locator(".book-formula math").count() == 65
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 6
            assert page.locator(".book-exercise-label").count() == 7
            assert page.locator(".book-table").count() == 1
            assert page.locator(".book-box.outlined-box").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 32 精确蒙特卡罗采样").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '33' && progress.block === 'read-p448-b010'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 34 独立成分分析与隐变量建模").click()
            page.locator(".reading-heading h1").get_by_text("第 34 章　独立成分分析与隐变量建模").wait_for()
            assert page.locator(".reading-block").count() == 109
            assert page.locator(".book-formula math").count() == 30
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator(".book-exercise-label").count() == 5
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 33 变分方法").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '34' && progress.block === 'read-p456-b011'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 35 若干推断专题").click()
            page.locator(".reading-heading h1").get_by_text("第 35 章　若干推断专题").wait_for()
            assert page.locator(".reading-block").count() == 84
            assert page.locator(".book-formula math").count() == 20
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 5
            assert page.locator(".book-exercise-label").count() == 7
            assert page.locator(".book-table").count() == 1
            assert page.locator(".book-footnote").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 34 独立成分分析与隐变量建模").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '35' && progress.page === 462 && progress.block === 'read-fn-35-1'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 36 决策理论").click()
            page.locator(".reading-heading h1").get_by_text("第 36 章　决策理论").wait_for()
            assert page.locator(".reading-block").count() == 93
            assert page.locator(".book-formula math").count() == 16
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 1
            assert page.locator(".book-exercise-label").count() == 9
            assert page.locator(".book-table").count() == 2
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 35 若干推断专题").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '36' && progress.page === 468 && progress.block === 'read-p468-b009'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 37 贝叶斯推断与抽样理论").click()
            page.locator(".reading-heading h1").get_by_text("第 37 章　贝叶斯推断与抽样理论").wait_for()
            assert page.locator(".reading-block").count() == 137
            assert page.locator(".book-formula math").count() == 35
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".book-table").count() == 1
            assert page.locator(".book-list").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 36 决策理论").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '37' && progress.page === 478 && progress.block === 'read-p478-b009'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 第五部分 神经网络").click()
            page.locator(".reading-heading h1").get_by_text("第五部分　神经网络").wait_for()
            assert page.locator(".reading-block").count() == 2
            assert page.locator(".book-figure img").count() == 1
            assert page.locator(".book-formula math").count() == 0
            assert page.locator(".reading-intro").count() == 0
            assert page.get_by_role("link", name="← 上一章 · 37 贝叶斯推断与抽样理论").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.locator(".book-figure img").evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'V' && progress.page === 479 && progress.block === 'read-p479-b002'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 38 神经网络导论").click()
            page.locator(".reading-heading h1").get_by_text("第 38 章　神经网络导论").wait_for()
            assert page.locator(".reading-block").count() == 25
            assert page.locator(".reading-list").count() == 3
            assert page.locator(".book-formula math").count() == 0
            assert page.locator(".book-figure img").count() == 0
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 第五部分 神经网络").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '38' && progress.page === 482 && progress.block === 'read-p482-b010'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 39 作为分类器的单个神经元").click()
            page.locator(".reading-heading h1").get_by_text("第 39 章　作为分类器的单个神经元").wait_for()
            assert page.locator(".reading-block").count() == 129
            assert page.locator(".book-formula math").count() == 28
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 10
            assert page.locator(".book-exercise-label").count() == 6
            assert page.locator(".book-code code").count() == 2
            assert page.locator(".book-box.outlined-box").count() == 2
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 38 神经网络导论").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '39' && progress.page === 493 && progress.block === 'read-p493-b004'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 导页 阅读第 40 章之前的习题").click()
            page.locator(".reading-heading h1").get_by_text("阅读第 40 章之前的习题").wait_for()
            assert page.locator(".reading-block").count() == 6
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".book-formula math").count() == 0
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".inline-math math").count() == 5
            assert page.locator(".reading-intro").count() == 0
            assert page.get_by_role("link", name="← 上一章 · 39 作为分类器的单个神经元").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '40-prelude' && progress.page === 494 && progress.block === 'read-p494-b006'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.get_by_role("link", name="下一章 → · 40 单个神经元的容量").click()
            page.locator(".reading-heading h1").get_by_text("第 40 章　单个神经元的容量").wait_for()
            assert page.locator(".reading-block").count() == 89
            assert page.locator(".book-formula math").count() == 11
            assert page.locator(".formula-fallback").count() == 0
            assert page.locator(".book-figure img").count() == 8
            assert page.locator(".book-exercise-label").count() == 6
            assert page.locator(".book-exercise-icon").count() == 3
            assert page.locator(".book-table").count() == 2
            assert page.locator(".reading-intro").count() == 1
            assert page.get_by_role("link", name="← 上一章 · 导页 阅读第 40 章之前的习题").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '40' && progress.page === 503 && progress.block === 'read-p503-b004'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41']").click()
            page.locator(".reading-heading h1").get_by_text("第 41 章　将学习视为推断").wait_for()
            assert page.locator(".reading-block").count() == 124
            assert page.locator(".book-formula math").count() == 30
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 9
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".book-box.outlined-box.algorithm-box").count() == 2
            assert page.locator(".book-code code").count() == 2
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '41' && progress.page === 515 && progress.block === 'read-p515-b004'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41-postscript']").click()
            page.locator(".reading-heading h1").get_by_text("有监督神经网络附记").wait_for()
            assert page.locator(".reading-block").count() == 5
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator(".book-figure, .book-formula, .book-table, .book-code, .book-exercise").count() == 0
            assert page.locator(".reading-intro").count() == 0
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41']").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '41-postscript' && progress.page === 516 && progress.block === 'read-p516-b005'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=42']").click()
            page.locator(".reading-heading h1").get_by_text("第 42 章　Hopfield 网络").wait_for()
            assert page.locator(".reading-block").count() == 207
            assert page.locator(".book-formula math").count() == 35
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 18
            assert page.locator(".book-exercise-label").count() == 12
            assert page.locator(".book-box.outlined-box.algorithm-box").count() == 1
            assert page.locator(".book-code code").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=41-postscript']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '42' && progress.page === 533 && progress.block === 'read-p533-b005'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=43']").click()
            page.locator(".reading-heading h1").get_by_text("第 43 章　玻尔兹曼机").wait_for()
            assert page.locator(".reading-block").count() == 69
            assert page.locator(".book-formula math").count() == 18
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 2
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".book-box.outlined-box").count() == 1
            assert page.locator(".book-box.outlined-box .book-formula math").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=42']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '43' && progress.page === 538 && progress.block === 'read-p538-b006'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=44']").click()
            page.locator(".reading-heading h1").get_by_text("第 44 章　多层网络中的监督学习").wait_for()
            assert page.locator(".reading-block").count() == 89
            assert page.locator(".book-formula math").count() == 12
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 7
            assert page.locator(".book-table").count() == 5
            assert page.locator(".book-exercise-label").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=43']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '44' && progress.page === 545 && progress.block === 'read-p545-b015'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=45-prelude']").click()
            page.locator(".reading-heading h1").get_by_text("关于第 45 章").wait_for()
            assert page.locator(".reading-block").count() == 7
            assert page.locator(".book-exercise-label").count() == 1
            assert page.locator(".book-formula, .book-figure, .book-table, .book-code").count() == 0
            assert page.locator(".reading-intro").count() == 0
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=44']").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '45-prelude' && progress.page === 546 && progress.block === 'read-p546-b007'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=45']").click()
            page.locator(".reading-heading h1").get_by_text("第 45 章　高斯过程").wait_for()
            assert page.locator(".reading-block").count() == 195
            assert page.locator(".book-formula math").count() == 56
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 2
            assert page.locator(".book-list").count() == 2
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=45-prelude']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '45' && progress.page === 560 && progress.block === 'read-p560-b007'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=46']").click()
            page.locator(".reading-heading h1").get_by_text("第 46 章　去卷积").wait_for()
            assert page.locator(".reading-block").count() == 67
            assert page.locator(".book-formula math").count() == 16
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure, .book-table, .book-code").count() == 0
            assert page.locator(".book-exercise-label").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=45']").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '46' && progress.page === 566 && progress.block === 'read-p566-b004'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=VI']").click()
            page.locator(".reading-heading h1").get_by_text("第六部分").wait_for()
            assert page.locator(".reading-block").count() == 2
            assert page.locator(".book-figure img").count() == 1
            assert page.locator(".book-formula, .book-table, .book-code, .book-exercise-label").count() == 0
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=46']").count() == 1
            page.locator(".book-figure img").evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'VI' && progress.page === 567 && progress.block === 'read-p567-b002'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=VI-intro']").click()
            page.locator(".reading-heading h1").get_by_text("关于第六部分").wait_for()
            assert page.locator(".reading-block").count() == 5
            assert page.locator(".book-formula, .book-figure, .book-table, .book-code, .book-exercise-label").count() == 0
            assert page.locator(".reading-intro").count() == 0
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=VI']").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'VI-intro' && progress.page === 568 && progress.block === 'read-p568-b005'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=47']").click()
            page.locator(".reading-heading h1").get_by_text("第 47 章　低密度奇偶校验码").wait_for()
            assert page.locator(".reading-block").count() == 202
            assert page.locator(".book-formula math").count() == 34
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 16
            assert page.locator(".book-table").count() == 4
            assert page.locator(".book-exercise-label").count() == 4
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=VI-intro']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '47' && progress.page === 585 && progress.block === 'read-p585-b009'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=48']").click()
            page.locator(".reading-heading h1").get_by_text("第 48 章　卷积码与 Turbo 码").wait_for()
            assert page.locator(".reading-block").count() == 69
            assert page.locator(".book-formula math").count() == 3
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 11
            assert page.locator(".book-table").count() == 0
            assert page.locator(".book-exercise-label").count() == 3
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=47']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '48' && progress.page === 593 && progress.block === 'read-p593-b012'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=49']").click()
            page.locator(".reading-heading h1").get_by_text("第 49 章　重复—累积码").wait_for()
            assert page.locator(".reading-block").count() == 64
            assert page.locator("aside.book-box.outlined-box").count() == 1
            assert page.locator(".book-formula math").count() == 11
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 9
            assert page.locator(".book-table").count() == 0
            assert page.locator(".book-exercise-label").count() == 1
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=48']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '49' && progress.page === 599 && progress.block === 'read-p599-b008'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=50-intro']").click()
            page.locator(".reading-heading h1").get_by_text("关于第 50 章").wait_for()
            assert page.locator(".reading-block").count() == 7
            assert page.locator(".book-formula math").count() == 0
            assert page.locator(".inline-math math").count() == 9
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 0
            assert page.locator(".book-table").count() == 0
            assert page.locator(".book-exercise-label").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=49']").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '50-intro' && progress.page === 600 && progress.block === 'read-p600-b007'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=50']").click()
            page.locator(".reading-heading h1").get_by_text("第 50 章　数字喷泉码").wait_for()
            assert page.locator(".reading-block").count() == 89
            assert page.locator("aside.book-box.outlined-box").count() == 3
            assert page.locator("#read-box-50-conclusion").count() == 1
            assert page.locator(".book-formula math").count() == 6
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 4
            assert page.locator(".book-table").count() == 0
            assert page.locator(".book-exercise-label").count() == 12
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=50-intro']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === '50' && progress.page === 608 && progress.block === 'read-p608-b007'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=VII']").click()
            page.locator(".reading-heading h1").get_by_text("第七部分").wait_for()
            assert page.locator(".reading-block").count() == 2
            assert page.locator(".book-figure img").count() == 1
            assert page.locator(".book-formula math, .book-table, .book-exercise-label").count() == 0
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=50']").count() == 1
            page.locator(".book-figure img").evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'VII' && progress.page === 609 && progress.block === 'read-p609-b002'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=A']").click()
            page.locator(".reading-heading h1").get_by_text("附录 A").wait_for()
            assert page.locator(".reading-block").count() == 49
            assert page.locator(".book-formula math").count() == 12
            assert page.locator(".inline-math math").count() == 122
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img, .book-table, .book-exercise-label").count() == 0
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=VII']").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'A' && progress.page === 612 && progress.block === 'read-p612-b014'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=B']").click()
            page.locator(".reading-heading h1").get_by_text("附录 B").wait_for()
            assert page.locator(".reading-block").count() == 53
            assert page.locator("aside.book-box.outlined-box").count() == 2
            assert page.locator("#read-box-b-infinite-states, #read-box-b-long-range-correlations").count() == 2
            assert page.locator(".book-formula math").count() == 12
            assert page.locator(".inline-math math").count() == 71
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 2
            assert page.locator(".book-table, .book-exercise-label").count() == 0
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=A']").count() == 1
            for figure in page.locator(".book-figure img").all():
                figure.scroll_into_view_if_needed()
                figure.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'B' && progress.page === 616 && progress.block === 'read-p616-b002'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=C']").click()
            page.locator(".reading-heading h1").get_by_text("附录 C").wait_for()
            assert page.locator(".reading-block").count() == 125
            assert page.locator(".book-formula math").count() == 37
            assert page.locator(".inline-math math").count() == 393
            assert page.locator(".formula-fallback, math merror").count() == 0
            assert page.locator(".book-figure img").count() == 1
            assert page.locator(".book-table").count() == 10
            assert page.locator(".book-exercise-label").count() == 0
            assert page.locator(".reading-intro").count() == 1
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=B']").count() == 1
            page.locator(".book-figure img").evaluate("image => image.decode()")
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'C' && progress.page === 624 && progress.block === 'read-p624-b003'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=REF']").click()
            page.locator(".reading-heading h1").get_by_text("参考文献").wait_for()
            assert page.locator(".reading-block").count() == 319
            assert page.locator(".reading-reference-entry p").count() == 318
            assert page.locator(".book-formula math, .book-figure img, .book-table, .book-exercise-label").count() == 0
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=C']").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'REF' && progress.page === 631 && progress.block === 'read-p631-b045'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=IDX']").click()
            page.locator(".reading-heading h1").get_by_text("索引").wait_for()
            assert page.locator(".reading-block").count() == 1150
            assert page.locator(".reading-rich p.index-entry, .reading-rich p.index-subentry").count() == 1599
            assert page.locator(".toc-chapter-link").count() == EXPECTED_TOC_LINKS
            assert page.locator("#chapter-navigation .chapter-navigation-link[href$='chapter=REF']").count() == 1
            page.evaluate("window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
            page.wait_for_function(
                "id => { const progress = JSON.parse(localStorage.getItem('intelligence-library:progress:v2:' + id) || '{}'); return progress.chapter === 'IDX' && progress.page === 640 && progress.block === 'read-p640-b169'; }",
                arg=BOOK_ID,
            )
            assert page.locator("#reading-progress").evaluate("node => node.style.width") == "100%"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert not errors, errors
            context.close()
        browser.close()
    print("PASS: real paths through index, figures, formulas, tables, navigation, progress, desktop/mobile")
finally:
    server.shutdown()
    server.server_close()
