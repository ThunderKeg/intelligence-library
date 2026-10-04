"""Check this book in the current reader without changing the shared book registry.

Uses the repository's installed headless Playwright test browser. The native
Browser plugin failed to initialize (node:process import is unavailable), so this
is an isolated application test, not a connection to a user's browser session.
"""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import threading

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


ROOT = Path(__file__).resolve().parents[3]
BOOK_ID = "boyd-vandenberghe-convex-optimization-2004"
BOOK = ROOT / "books" / BOOK_ID
OUTPUT = ROOT / "tmp" / "convex" / "reader-qa"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def run(chapters: list[str]) -> dict:
    documents = []
    for chapter in chapters:
        path = BOOK / f"chapter-{chapter}.json"
        documents.append(json.loads(path.read_text(encoding="utf-8")))
    registry = {
        "id": BOOK_ID,
        "title": "凸优化",
        "originalTitle": "Convex Optimization",
        "author": "Stephen Boyd · Lieven Vandenberghe",
        "year": "2004／2009",
        "description": "凸优化中文译文",
        "chapters": [
            {"id": chapter, "number": str(int(chapter)) if chapter.isdigit() else "",
             "title": re.sub(r"^(?:第\s*\d+\s*章|附录\s*[A-C])\s*", "", document["title"]),
             "content": f"books/{BOOK_ID}/chapter-{chapter}.json"}
            for chapter, document in zip(chapters, documents)
        ],
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}/"
    results = []
    errors: list[str] = []
    try:
        with sync_playwright() as playwright:
            installed = sorted((Path.home() / "AppData/Local/ms-playwright").glob(
                "chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
            options = {"headless": True}
            if installed:
                options["executable_path"] = str(installed[-1])
            browser = playwright.chromium.launch(**options)
            for label, width, height, theme in (
                ("desktop-light", 1440, 960, "light"),
                ("mobile-light", 390, 844, "light"),
                ("mobile-dark", 390, 844, "dark"),
                ("narrow-dark", 320, 740, "dark"),
            ):
                context = browser.new_context(
                    viewport={"width": width, "height": height},
                    color_scheme=theme, service_workers="block",
                    is_mobile=width < 600, has_touch=width < 600,
                )
                context.route("**/books.js", lambda route: route.fulfill(
                    status=200, content_type="application/javascript",
                    body="const books = " + json.dumps([registry], ensure_ascii=False) + ";"))
                page = context.new_page()
                page.on("pageerror", lambda error: errors.append(str(error)))
                for chapter, document in zip(chapters, documents):
                    url = base + f"?book={BOOK_ID}&chapter={chapter}"
                    page.goto(url)
                    page.locator(".reading-block").first.wait_for()
                    page.wait_for_function("[...document.fonts].some(font => font.family.includes('Convex STIX Two Math'))")
                    page.evaluate("document.fonts.load('18px \"Convex STIX Two Math\"')")
                    page.evaluate("document.fonts.ready")
                    assert page.evaluate("document.fonts.check('18px \"Convex STIX Two Math\"')"), (label, chapter, "math font failed")
                    assert page.locator("#reader-status").is_hidden(), (label, chapter, "reader error")
                    assert page.locator("html").get_attribute("data-theme") == theme
                    assert page.locator("#reader-article .reading-block").count() == len(document["blocks"])
                    dimensions = page.evaluate("({width:innerWidth,content:document.documentElement.scrollWidth})")
                    assert dimensions["content"] <= dimensions["width"], (label, chapter, dimensions)
                    assert page.locator("#reader-article merror").count() == 0
                    compressed_labels = page.locator("#reader-article mtext").evaluate_all("""nodes => nodes.filter(node => {
                        const count = (node.textContent.match(/[\\u4e00-\\u9fff]/g) || []).length;
                        return count > 1 && node.getBoundingClientRect().width + 1 <
                            count * parseFloat(getComputedStyle(node).fontSize) * .8;
                    }).map(node => ({text:node.textContent,width:node.getBoundingClientRect().width}))""")
                    assert not compressed_labels, (label, chapter, "compressed CJK formula labels", compressed_labels)
                    small_fences = page.locator("#reader-article mrow").evaluate_all("""rows => rows.flatMap(row => {
                        const table = [...row.children].find(el => el.localName==='mtable');
                        if (!table || table.querySelectorAll(':scope > mtr').length < 2) return [];
                        const height = table.getBoundingClientRect().height;
                        return [...row.children].filter(el => el.localName==='mo' && el.getAttribute('fence')==='true' &&
                            el.getAttribute('stretchy')!=='false' && el.getBoundingClientRect().height < height*.8)
                            .map(el => ({fence:el.textContent,height:el.getBoundingClientRect().height,table:height}));
                    })""")
                    assert not small_fences, (label, chapter, "matrix fence does not enclose matrix", small_fences)
                    misaligned_cells = page.locator("#reader-article mtd").evaluate_all("""cells => cells.flatMap(cell => {
                        const style = getComputedStyle(cell);
                        const align = style.textAlign.replace('-webkit-', '');
                        const children = [...cell.children].map(el => el.getBoundingClientRect()).filter(box => box.width > 0);
                        if (!children.length || !['left','right','center'].includes(align)) return [];
                        const box = cell.getBoundingClientRect();
                        const left = box.left + parseFloat(style.paddingLeft), right = box.right - parseFloat(style.paddingRight);
                        const contentLeft = Math.min(...children.map(box => box.left));
                        const contentRight = Math.max(...children.map(box => box.right));
                        const drift = align === 'left' ? contentLeft-left : align === 'right' ? right-contentRight :
                            (contentLeft+contentRight-left-right)/2;
                        return Math.abs(drift) <= 1 ? [] : [{align,drift,text:cell.textContent,
                            tex:cell.closest('math').getAttribute('data-tex')}];
                    })""")
                    assert not misaligned_cells, (label, chapter, "MathML cell alignment", misaligned_cells)
                    unresolved = page.locator("#reader-article").inner_text()
                    assert not re.search(r"CONVEXMATH|SHANNONMATH|BISHOPMATH|\\\\(?:begin|tag|frac)\{", unresolved)
                    image_results = page.locator("#reader-article img").evaluate_all("""async images => Promise.all(images.map(async img => {
                        img.loading='eager'; try { await img.decode(); return {src:img.getAttribute('src'),ok:img.naturalWidth>0}; }
                        catch { return {src:img.getAttribute('src'),ok:false}; }
                    }))""")
                    assert all(image["ok"] for image in image_results), (label, chapter, image_results)
                    assert len(image_results) == len(document.get("images", [])), (label, chapter, "image count")
                    assert page.locator("#reader-article iframe, #reader-article object, #reader-article embed").count() == 0
                    broken = page.locator("#reader-article a[href^='#']").evaluate_all("""links => links.filter(
                        a => a.hash && !document.getElementById(decodeURIComponent(a.hash.slice(1))))
                        .map(a => a.getAttribute('href'))""")
                    assert not broken, (label, chapter, broken)
                    math_count = page.locator("#reader-article math").count()
                    page.screenshot(path=str(OUTPUT / f"{chapter}-{label}-opening.png"))
                    formulas = page.locator("#reader-article .book-formula")
                    if formulas.count():
                        formulas.first.scroll_into_view_if_needed()
                        page.screenshot(path=str(OUTPUT / f"{chapter}-{label}-formula.png"))
                    figures = page.locator("#reader-article figure")
                    if figures.count():
                        figures.last.scroll_into_view_if_needed()
                        page.screenshot(path=str(OUTPUT / f"{chapter}-{label}-figure.png"))
                    tables = page.locator("#reader-article table")
                    if tables.count():
                        clipped = page.locator("#reader-article th, #reader-article td").evaluate_all("""cells => cells.filter(cell => {
                            const range = document.createRange(); range.selectNodeContents(cell);
                            const text = range.getBoundingClientRect(), box = cell.getBoundingClientRect();
                            return text.right > box.right + 1 || text.left < box.left - 1;
                        }).map(cell => cell.textContent)""")
                        assert not clipped, (label, chapter, "clipped contents cells", clipped)
                        oversized_compact = tables.evaluate_all("""tables => tables.filter(table =>
                            table.style.minWidth === '0px' &&
                            table.getBoundingClientRect().width > table.parentElement.getBoundingClientRect().width + 1
                        ).map(table => ({width:table.getBoundingClientRect().width,
                            available:table.parentElement.getBoundingClientRect().width}))""")
                        assert not oversized_compact, (label, chapter, "compact table exceeds available width", oversized_compact)
                    if tables.count():
                        tables.last.scroll_into_view_if_needed()
                        page.screenshot(path=str(OUTPUT / f"{chapter}-{label}-table.png"))
                    results.append({"chapter": chapter, "view": label, "mathCount": math_count,
                                    "images": image_results, "dimensions": dimensions})
                # Store an interior reading position, reload the real reader,
                # and verify both the stored block and its restored position.
                if len(documents[-1]["blocks"]) > 3:
                    saved_block = "read-" + documents[-1]["blocks"][len(documents[-1]["blocks"]) // 2]["id"]
                    progress_key = "intelligence-library:progress:v2:" + BOOK_ID
                    page.locator("[id='" + saved_block + "']").evaluate(
                        "node => node.scrollIntoView({block:'start',behavior:'instant'})")
                    page.wait_for_function("""({key,id}) => JSON.parse(localStorage.getItem(key)||'null')?.block === id""",
                                           arg={"key": progress_key, "id": saved_block})
                    page.reload()
                    page.locator(".reading-block").first.wait_for()
                    page.wait_for_function("[...document.fonts].some(font => font.family.includes('Convex STIX Two Math'))")
                    page.evaluate("document.fonts.load('18px \"Convex STIX Two Math\"')")
                    page.evaluate("document.fonts.ready")
                    try:
                        page.wait_for_function("""id => {
                            const node = document.getElementById(id);
                            return node && Math.abs(node.getBoundingClientRect().top - parseFloat(getComputedStyle(node).scrollMarginTop)) <= 2;
                        }""", arg=saved_block, timeout=5000)
                    except PlaywrightTimeoutError:
                        diagnostic = page.evaluate("""({id,key}) => {
                            const node = document.getElementById(id);
                            return {id,scrollY,top:node?.getBoundingClientRect().top,
                                margin:node&&getComputedStyle(node).scrollMarginTop,
                                saved:JSON.parse(localStorage.getItem(key)),url:location.href};
                        }""", {"id":saved_block,"key":progress_key})
                        (OUTPUT / f"{chapters[-1]}-{label}-progress-failure.json").write_text(
                            json.dumps(diagnostic,ensure_ascii=False,indent=2),encoding="utf-8")
                        page.screenshot(path=str(OUTPUT / f"{chapters[-1]}-{label}-progress-failure.png"))
                        raise
                    restored = page.evaluate("key => JSON.parse(localStorage.getItem(key))", progress_key)
                    assert restored["block"] == saved_block and restored["chapter"] == chapters[-1], (label, restored)
                    results[-1]["progressRestored"] = saved_block
                # Exercise the actual mobile chapter menu and next-chapter link.
                if width < 600:
                    page.get_by_role("button", name="目录", exact=True).click()
                    assert page.locator("#toc-dialog").evaluate("dialog=>dialog.open")
                    assert page.locator("#reader-toc-mobile .toc-chapter-link").count() == len(chapters)
                    page.get_by_role("button", name="关闭", exact=True).click()
                if len(chapters) > 1:
                    page.goto(base + f"?book={BOOK_ID}&chapter={chapters[0]}")
                    page.locator(".reading-block").first.wait_for()
                    page.get_by_role("link", name="下一章").click()
                    page.wait_for_url("**chapter=" + chapters[1])
                    page.locator(".reading-block").first.wait_for()
                context.close()
            browser.close()
        assert not errors, errors
        result = {"checksPassed": True, "contentReviewPassed": False,
                  "note": "Automated rendering checks do not establish translation completeness or semantic accuracy.",
                  "chapters": chapters, "results": results, "errors": errors}
        (OUTPUT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("chapters", nargs="+", help="Existing chapter JSON ids, in reading order")
    arguments = parser.parse_args()
    report = run(arguments.chapters)
    print(json.dumps({"checksPassed": report["checksPassed"], "chapters": report["chapters"],
                      "viewChecks": len(report["results"]), "output": str(OUTPUT)}, ensure_ascii=False))
