"""Verify actual formula-reference clicks and capture their landing positions."""
import argparse
import hashlib
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from qa_reader import wait_for_scroll_settled

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('numbers', nargs='+')
    parser.add_argument('--base', default='http://127.0.0.1:8794')
    parser.add_argument('--name', default='formula-navigation')
    args = parser.parse_args()
    targets = json.loads((BOOK/'reference-index.json').read_text(encoding='utf8'))['targets']['formula']
    out = ROOT/'tmp/prml-reference-jumps'/args.name
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        exe = sorted((Path.home()/'AppData/Local/ms-playwright').glob('chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))[-1]
        browser = pw.chromium.launch(headless=True, executable_path=str(exe))
        for width, height, theme in [(1440,1000,'light'),(390,844,'dark')]:
            for number in args.numbers:
                target = targets[number]
                ctx = browser.new_context(viewport={'width':width,'height':height}, color_scheme=theme, service_workers='block')
                page = ctx.new_page()
                page.goto(f'{args.base}/?book={BOOK.name}&chapter={target["chapter"]}')
                page.locator('.reading-block').first.wait_for()
                page.evaluate('document.fonts.ready')
                href = '#read-'+target['block']
                link = page.locator(f'#reader-article a.reading-reference[href="{href}"]').first
                assert link.count(), (number, 'no rendered reference')
                label = link.inner_text()
                link.scroll_into_view_if_needed()
                link.click()
                page.wait_for_function('(h)=>location.hash===h', arg=href)
                wait_for_scroll_settled(page)
                geometry = page.locator(href).evaluate('el=>({top:el.getBoundingClientRect().top,bottom:el.getBoundingClientRect().bottom,bar:document.querySelector(".reader-topbar").getBoundingClientRect().bottom,viewport:innerHeight})')
                assert geometry['top'] >= geometry['bar'] and geometry['top'] < geometry['viewport'], geometry
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                path = out/f'{number}-{width}-{theme}.png'
                page.screenshot(path=str(path))
                results.append({'number':number,'unit':target['chapter'],'linkText':label,'href':href,'geometry':geometry,'width':width,'theme':theme,'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
                ctx.close()
        browser.close()
    (BOOK/'reviews'/f'{args.name}.json').write_text(json.dumps({'passed':True,'results':results},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'passed':True,'clicks':len(results),'screenshots':str(out)},ensure_ascii=False))


if __name__ == '__main__':
    main()
