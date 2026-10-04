"""Check that reader MathML preserves every source mspace width."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from playwright.sync_api import sync_playwright
from qa_reader import walk

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
WIDTH = re.compile(r'<mspace\b[^>]*\bwidth="([^"]+)"')


def main():
    inventory = json.loads((BOOK/'source-inventory.json').read_text(encoding='utf8'))
    out = ROOT/'tmp/prml-math-spacing'
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        exe = sorted((Path.home()/'AppData/Local/ms-playwright').glob('chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))[-1]
        browser = pw.chromium.launch(headless=True, executable_path=str(exe))
        for unit in inventory['units']:
            key = unit['id']
            path = BOOK/f'{key}.json'
            if not path.exists():
                continue
            data = json.loads(path.read_text(encoding='utf8'))
            nodes = list(walk(data['blocks']))
            expected = [w for n in nodes for w in WIDTH.findall(n.get('mathml',''))]
            if not expected:
                continue
            candidates = [n for n in nodes if n.get('kind')=='formula' and WIDTH.search(n.get('mathml',''))]
            candidate = max(candidates, key=lambda n:max(float(re.match(r'-?[\d.]+',w)[0]) for w in WIDTH.findall(n['mathml']))) if candidates else next(n for n in nodes if n.get('id') and any(WIDTH.search(v.get('mathml','')) for v in walk(n)))
            for width, height, theme in [(1440,1000,'light'),(390,844,'dark')]:
                ctx = browser.new_context(viewport={'width':width,'height':height},color_scheme=theme,service_workers='block')
                page = ctx.new_page()
                page.goto(f'http://127.0.0.1:8794/?book={BOOK.name}&chapter={key}')
                page.locator('.reading-block').first.wait_for()
                page.evaluate('document.fonts.ready')
                page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
                actual = page.locator('#reader-article mspace').evaluate_all('els=>els.map(el=>({width:el.getAttribute("width"),pixels:el.getBoundingClientRect().width,block:el.closest(".reading-block").id}))')
                actual = [x for x in actual if x['width'] is not None]
                assert Counter(x['width'] for x in actual)==Counter(expected), (key, Counter(expected),Counter(x['width'] for x in actual))
                assert all(x['pixels']>0 for x in actual if float(re.match(r'-?[\d.]+',x['width'])[0])>0), (key, actual)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), key
                gaps = page.locator('.formula-scroll').evaluate_all('els=>els.filter(el=>el.scrollWidth>el.clientWidth+2).filter(el=>{const h=el.closest(".book-formula").nextElementSibling;return !h?.classList.contains("formula-view-hint")||h.hidden;}).map(el=>el.closest(".reading-block").id)')
                assert not gaps, (key, gaps)
                target = page.locator('#read-'+candidate['id'])
                target.evaluate('el=>el.scrollIntoView({block:"start",behavior:"instant"})')
                shot = out/f'{key}-{width}-{theme}.png'
                page.screenshot(path=str(shot))
                results.append({'unit':key,'width':width,'theme':theme,'spaces':len(expected),'allWidthsPreserved':True,'positiveSpaceGeometry':True,'noPageOverflow':True,'target':candidate['id'],'number':candidate.get('number'),'file':str(shot),'sha256':hashlib.sha256(shot.read_bytes()).hexdigest()})
                ctx.close()
        browser.close()
    report = {'passed':True,'checks':len(results),'spaces':sum(x['spaces'] for x in results),'results':results}
    (BOOK/'reviews/math-spacing-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}))


if __name__ == '__main__':
    main()
