"""Browser smoke test for the continuous text reader."""

import os
import json
from pathlib import Path

from playwright.sync_api import Error, sync_playwright


BASE = os.environ.get("LIBRARY_TEST_URL", "http://127.0.0.1:8787/")
OUTPUT = Path(os.environ.get("LIBRARY_TEST_OUTPUT", "tmp/browser-qa"))
ROOT = Path(__file__).resolve().parents[1]
OUTPUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as playwright:
    installed = sorted((Path.home() / "AppData/Local/ms-playwright").glob("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
    options = {"headless": True}
    if installed:
        options["executable_path"] = str(installed[-1])
    browser = playwright.chromium.launch(**options)
    desktop = browser.new_context(viewport={"width": 1440, "height": 900})
    page = desktop.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(BASE)
    page.locator(".book-card").first.wait_for()
    page.get_by_role("button", name="切换深色模式").click()
    assert page.locator("html").get_attribute("data-theme") == "dark"
    assert page.locator("#theme-toggle").get_attribute("aria-pressed") == "true"
    page.reload()
    assert page.locator("html").get_attribute("data-theme") == "dark"
    page.locator(".book-card").filter(has_text="深度学习：基础与概念").get_by_role("link", name="开始阅读").click()
    page.locator(".reading-block").first.wait_for()
    assert page.locator(".reading-heading h1").inner_text() == "封面与出版信息"
    assert page.locator(".reading-block").count() == 17
    page.wait_for_function("document.querySelector('.book-figure img').naturalWidth > 0")
    page.get_by_role("link", name="下一章").click()
    page.locator(".reading-heading h1").get_by_text("前言").wait_for()
    assert page.locator(".reading-block").count() == 38
    page.get_by_role("link", name="下一章").click()
    page.locator(".reading-heading h1").get_by_text("原书目录").wait_for()
    assert page.locator(".original-contents li").count() == 407
    assert page.locator(".contents-depth-0 strong").count() == 27
    page.get_by_role("link", name="下一章").click()
    page.locator(".reading-heading h1").get_by_text("第 1 章 深度学习革命").wait_for()
    assert page.locator(".reading-block").count() == 118
    assert page.locator("#reader-toc .toc-link").count() == 44
    assert page.locator("#reader-toc-mobile .toc-link").count() == 44
    assert page.locator(".book-figure img").count() == 17
    assert page.locator(".reading-intro").count() == 1
    assert page.locator(".book-formula").count() == 7
    assert page.locator(".book-table caption").count() == 2
    assert "独家授权" not in page.locator(".reader-article").inner_text()
    assert page.locator(".reading-heading h1").inner_text() == "第 1 章 深度学习革命"
    assert page.locator("#chapter-navigation").is_visible()
    page.screenshot(path=str(OUTPUT / "reader-desktop.png"), full_page=False)

    page.locator("#reader-toc .toc-section-link").last.click()
    page.wait_for_function("location.hash === '#read-p20-b003'")
    page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).page >= 20")
    try:
        page.reload()
    except Error as error:
        if "ERR_ABORTED" not in str(error):
            raise
        page.wait_for_load_state("load")
    page.locator(".reading-block").first.wait_for()
    page.wait_for_function("window.scrollY > 1000")
    page.goto(BASE)
    assert page.get_by_role("link", name="继续阅读").is_visible()

    page.evaluate("navigator.serviceWorker.ready")
    desktop.set_offline(True)
    page.goto(BASE + "?book=bishop-deep-learning-2024&chapter=frontmatter")
    page.wait_for_function("document.querySelector('.book-figure img').naturalWidth > 0")
    for chapter, count in (("frontmatter", 17), ("00", 38), ("contents", 12),
                           ("01", 118), ("02", 449), ("03", 587),
                           ("04", 217), ("05", 389), ("06", 314), ("07", 235),
                           ("08", 248), ("09", 281), ("10", 203), ("11", 281),
                           ("12", 346), ("13", 199), ("14", 263), ("15", 280),
                           ("16", 328), ("17", 85), ("18", 141), ("19", 123),
                           ("20", 265), ("A", 125), ("B", 30), ("C", 39),
                           ("bibliography", 332), ("index", 680)):
        page.goto(BASE + f"?book=bishop-deep-learning-2024&chapter={chapter}")
        page.wait_for_function("expected => document.querySelectorAll('.reading-block').length === expected", arg=count)
    desktop.set_offline(False)

    mobile = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
    phone = mobile.new_page()
    phone.on("pageerror", lambda error: errors.append(str(error)))
    phone.goto(BASE + "?book=bishop-deep-learning-2024&chapter=01#read-p14-b002")
    phone.locator(".reading-block").first.wait_for()
    phone.wait_for_function("Math.abs(document.getElementById('read-p14-b002').getBoundingClientRect().top) < 100")
    assert not phone.locator("#reader-menu").evaluate("menu => menu.open")
    phone.get_by_role("button", name="目录", exact=True).click()
    assert phone.locator("#toc-dialog").evaluate("dialog => dialog.open")
    assert phone.locator("#toc-toggle").get_attribute("aria-expanded") == "true"
    phone.screenshot(path=str(OUTPUT / "reader-mobile-toc.png"), full_page=False)
    phone.locator("#reader-toc-mobile a[href='#read-p20-b003']").click()
    assert not phone.locator("#toc-dialog").evaluate("dialog => dialog.open")
    phone.wait_for_function("location.hash === '#read-p20-b003'")
    phone.wait_for_function("Math.abs(document.getElementById('read-p20-b003').getBoundingClientRect().top) < 140")
    phone.screenshot(path=str(OUTPUT / "reader-mobile.png"), full_page=False)
    dimensions = phone.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
    assert dimensions["content"] <= dimensions["viewport"], dimensions

    system = browser.new_context(color_scheme="dark", service_workers="block")
    system_page = system.new_page()
    system_page.goto(BASE)
    assert system_page.locator("html").get_attribute("data-theme") == "dark"
    system_page.get_by_role("button", name="切换浅色模式").wait_for()
    system_page.emulate_media(color_scheme="light")
    system_page.wait_for_function("document.documentElement.dataset.theme === 'light'")
    system.close()

    chapters = browser.new_context(service_workers="block")
    chapter_page = chapters.new_page()
    chapter_page.goto(BASE + "?book=bishop-deep-learning-2024&page=14")
    chapter_page.locator(".reading-block").first.wait_for()
    assert chapter_page.locator(".reading-heading h1").inner_text() == "第 1 章 深度学习革命"
    assert chapter_page.locator("#reader-toc .toc-chapter-link").count() == 28
    chapter_page.get_by_role("link", name="下一章").click()
    chapter_page.locator(".reading-heading h1").get_by_text("第 2 章 概率").wait_for()
    assert "chapter=02" in chapter_page.url
    assert chapter_page.locator(".book-figure img").count() == 17
    assert chapter_page.locator(".book-formula").count() == 134
    assert chapter_page.locator(".book-table").count() == 2
    chapter_page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).chapter === '02'")
    chapter_page.get_by_role("link", name="下一章").click()
    chapter_page.locator(".reading-heading h1").get_by_text("第 3 章 标准分布").wait_for()
    assert "chapter=03" in chapter_page.url
    assert chapter_page.locator(".book-formula").count() == 218
    chapter_page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).chapter === '03'")
    chapter_page.get_by_role("link", name="下一章").click()
    chapter_page.locator(".reading-heading h1").get_by_text("第 4 章 单层网络：回归").wait_for()
    assert "chapter=04" in chapter_page.url
    assert chapter_page.locator(".book-formula").count() == 70
    chapter_page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).chapter === '04'")
    chapter_page.get_by_role("link", name="下一章").click()
    chapter_page.locator(".reading-heading h1").get_by_text("第 5 章 单层网络：分类").wait_for()
    assert "chapter=05" in chapter_page.url
    assert chapter_page.locator(".book-formula").count() == 107
    chapter_page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).chapter === '05'")
    chapter_page.get_by_role("link", name="下一章").click()
    chapter_page.locator(".reading-heading h1").get_by_text("第 6 章 深层神经网络").wait_for()
    assert "chapter=06" in chapter_page.url
    assert chapter_page.locator(".book-formula").count() == 66
    chapter_page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).chapter === '06'")
    chapter_page.get_by_role("link", name="下一章").click()
    chapter_page.locator(".reading-heading h1").get_by_text("第 7 章 梯度下降").wait_for()
    assert "chapter=07" in chapter_page.url
    assert chapter_page.locator(".book-formula").count() == 69
    chapter_page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).chapter === '07'")
    chapter_page.get_by_role("link", name="下一章").click()
    chapter_page.locator(".reading-heading h1").get_by_text("第 8 章 反向传播").wait_for()
    assert "chapter=08" in chapter_page.url
    assert chapter_page.locator(".book-formula").count() == 80
    chapter_page.wait_for_function("JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).chapter === '08'")
    for chapter, title in (("09", "正则化"), ("10", "卷积网络"), ("11", "结构化分布"),
                           ("12", "Transformer"), ("13", "图神经网络"), ("14", "采样"),
                           ("15", "离散潜变量"), ("16", "连续潜变量"),
                           ("17", "生成对抗网络"), ("18", "归一化流"),
                           ("19", "自编码器"), ("20", "扩散模型")):
        chapter_page.get_by_role("link", name="下一章").click()
        chapter_page.locator(".reading-heading h1").get_by_text(f"第 {int(chapter)} 章 {title}").wait_for()
        assert f"chapter={chapter}" in chapter_page.url
        chapter_page.wait_for_function(
            "expected => JSON.parse(localStorage.getItem('intelligence-library:progress:v2:bishop-deep-learning-2024')).chapter === expected",
            arg=chapter,
        )
    for chapter, title in (("A", "附录 A 线性代数"), ("B", "附录 B 变分法"),
                           ("C", "附录 C 拉格朗日乘子"),
                           ("bibliography", "参考文献"), ("index", "索引")):
        chapter_page.get_by_role("link", name="下一章").click()
        chapter_page.locator(".reading-heading h1").get_by_text(title).wait_for()
        assert f"chapter={chapter}" in chapter_page.url
    chapter_page.goto(BASE)
    assert "chapter=index" in chapter_page.get_by_role("link", name="继续阅读").get_attribute("href")
    chapters.close()

    rich = browser.new_context(service_workers="block")
    rich_script = (ROOT / "books.js").read_text(encoding="utf-8") + '\nbooks.push({id:"reader-fixture",title:"渲染测试",originalTitle:"Reader fixture",author:"Test",year:"2026",description:"",chapters:[{id:"01",number:"1",title:"测试章",content:"books/reader-fixture/chapter-01.json"}]});'
    rich.route("**/books.js", lambda route: route.fulfill(body=rich_script, content_type="application/javascript"))
    mathml = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mi>α</mi><mn>2</mn></mfrac></math>'
    rich_chapter = {
        "bookId": "reader-fixture",
        "title": "第 1 章 测试章",
        "toc": [{"number": "1", "title": "测试章", "block": "p01-t01"}],
        "blocks": [
            {"id": "p01-t01", "kind": "heading", "text": "第 1 章 测试章", "page": 1},
            {"id": "p01-t02", "kind": "intro", "text": "本章导读", "page": 1},
            {"id": "p01-t03", "kind": "figure", "src": "assets/fig.svg", "alt": "测试图", "caption": "图 1.1：测试", "annotations": ["Action：动作", "Reward：奖励"], "page": 1},
            {"id": "p01-t04", "kind": "formula", "text": "α/2", "mathml": mathml, "number": "(1.1)", "page": 1},
            {"id": "p01-t05", "kind": "code", "text": "if (x < 1):\n    return x & 1", "language": "python", "page": 1},
            {"id": "p01-t06", "kind": "list", "ordered": True, "items": ["第一项", {"text": "第二项", "children": ["子项"]}], "page": 1},
            {"id": "p01-t07", "kind": "paragraph", "segments": ["参见", {"text": "注 1", "ref": "p01-t08"}, "，令 ", {"text": "α/2", "mathml": mathml}], "page": 1},
            {"id": "p01-t08", "kind": "footnote", "label": "1", "text": "脚注内容", "page": 1},
            {"id": "p01-t09", "kind": "formula", "text": "无效标记回退", "mathml": "<math><script>bad</script></math>", "page": 1},
            {"id": "p01-t10", "kind": "table", "caption": "表 1.1：测试", "headers": ["状态", "数值"], "rows": [[{"text": "A|B", "colspan": 2}], ["下一行", "1\n2"]], "page": 1},
            {"id": "p01-t11", "kind": "quote", "text": "引文 <原样保留>", "page": 1},
            {"id": "p01-t12", "kind": "exercise", "label": "习题 1.1：测试。", "text": "求出 x < 1 时的值。", "page": 1},
            {"id": "p01-t13", "kind": "bibliographical-note", "label": "1.2", "text": "参考来源。", "page": 1},
        ],
    }
    rich.route("**/reader-fixture/chapter-01.json", lambda route: route.fulfill(body=json.dumps(rich_chapter, ensure_ascii=False), content_type="application/json"))
    rich.route("**/reader-fixture/assets/fig.svg", lambda route: route.fulfill(body='<svg xmlns="http://www.w3.org/2000/svg" width="320" height="160"><rect width="320" height="160" fill="#bcd"/></svg>', content_type="image/svg+xml"))
    rich_page = rich.new_page()
    rich_page.set_viewport_size({"width": 390, "height": 844})
    rich_page.on("pageerror", lambda error: errors.append(str(error)))
    rich_page.goto(BASE + "?book=reader-fixture")
    rich_page.locator(".reading-block").first.wait_for()
    assert rich_page.locator(".reading-intro").inner_text() == "本章导读"
    assert rich_page.locator(".book-figure img").get_attribute("alt") == "测试图"
    assert rich_page.locator(".book-figure img").evaluate("image => image.complete && image.naturalWidth > 0")
    assert rich_page.locator(".figure-annotations li").all_inner_texts() == ["Action：动作", "Reward：奖励"]
    assert rich_page.locator(".book-formula math").count() == 1
    assert rich_page.locator(".book-formula .formula-fallback").inner_text() == "无效标记回退"
    assert rich_page.locator(".book-formula script").count() == 0
    assert rich_page.locator(".book-code code").inner_text() == "if (x < 1):\n    return x & 1"
    assert rich_page.locator(".reading-list > .book-list > li").count() == 2
    assert rich_page.locator(".book-list .book-list li").inner_text() == "子项"
    assert rich_page.locator(".reading-reference").get_attribute("href") == "#read-p01-t08"
    assert rich_page.locator(".reading-paragraph math").count() == 1
    assert rich_page.locator(".book-footnote").inner_text() == "1脚注内容"
    assert rich_page.locator(".book-table caption").inner_text() == "表 1.1：测试"
    assert rich_page.locator(".book-table tbody tr").first.locator("td").get_attribute("colspan") == "2"
    assert rich_page.locator(".book-table tbody tr").first.inner_text() == "A|B"
    assert rich_page.locator(".book-quote").inner_text() == "引文 <原样保留>"
    assert rich_page.locator(".book-quote script").count() == 0
    assert rich_page.locator(".book-exercise-label").inner_text() == "习题 1.1：测试。"
    assert rich_page.locator(".book-exercise-body").inner_text() == "求出 x < 1 时的值。"
    assert rich_page.locator(".book-bibliographical-note-label").inner_text() == "1.2"
    rich_page.locator("#theme-toggle").click()
    assert rich_page.locator("html").get_attribute("data-theme") == "dark"
    rich_width = rich_page.evaluate("({viewport: innerWidth, content: document.documentElement.scrollWidth})")
    assert rich_width["content"] <= rich_width["viewport"], rich_width
    rich_page.screenshot(path=str(OUTPUT / "reader-rich-mobile.png"), full_page=True)
    rich.close()

    assert not errors, errors
    print(f"PASS: contents, themes, chapter navigation, resume, offline, mobile width {dimensions}, no page errors")
    browser.close()
