"""Check native MathML column alignment in both reader layouts."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://127.0.0.1:8794')
    args = parser.parse_args()
    inventory = json.loads((BOOK/'source-inventory.json').read_text(encoding='utf-8'))
    units = [u['id'] for u in inventory['units'] if (BOOK/(u['id']+'.json')).is_file()]
    out = ROOT/'tmp/prml-math-alignment'
    out.mkdir(parents=True,exist_ok=True)
    results = []
    with sync_playwright() as pw:
        exe = sorted((Path.home()/'AppData/Local/ms-playwright').glob('chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))[-1]
        browser = pw.chromium.launch(headless=True,executable_path=str(exe))
        for width,height,theme in [(1440,1000,'light'),(390,844,'dark')]:
            context = browser.new_context(viewport={'width':width,'height':height},color_scheme=theme,service_workers='block')
            page = context.new_page()
            for unit in units:
                page.goto(args.base+'/?book='+BOOK.name+'&chapter='+unit)
                page.locator('.reading-block').first.wait_for()
                page.evaluate('document.fonts.ready')
                tables = page.evaluate('''() => Array.from(document.querySelectorAll('#reader-article math mtable[columnalign]')).filter(t=>['right left','left left','right'].includes(t.getAttribute('columnalign'))).map(t=>{
                  const align=t.getAttribute('columnalign').split(' ');
                  const rows=Array.from(t.children).filter(r=>r.localName==='mtr');
                  const cells=rows.flatMap(r=>Array.from(r.children).map((c,i)=>({expected:align[i]||align[align.length-1],actual:getComputedStyle(c).textAlign})));
                  const equals=align.join(' ')==='right left'?rows.map(r=>r.children[1]?.querySelector('mo')).filter(op=>op?.textContent==='=').map(op=>op.getBoundingClientRect().left):[];
                  return {block:t.closest('.reading-block').id,align:align.join(' '),cells,equals,delta:equals.length>1?Math.max(...equals)-Math.min(...equals):0};
                })''')
                for table in tables:
                    assert all(c['expected']==c['actual'] for c in table['cells']), (unit,table)
                    assert table['delta'] < 1, (unit,table)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), unit
                shots = []
                selected = {}
                for table in tables:
                    selected.setdefault(table['align'],table['block'])
                for alignment,bid in selected.items():
                    page.locator('#'+bid).evaluate('el=>el.scrollIntoView({block:"start",behavior:"instant"})')
                    shot=out/(unit+'-'+alignment.replace(' ','-')+f'-{width}-{theme}.png')
                    page.screenshot(path=str(shot))
                    shots.append(str(shot))
                results.append({'unit':unit,'width':width,'theme':theme,'tables':tables,'screenshots':shots})
            context.close()
        browser.close()
    (BOOK/'reviews/math-alignment-qa.json').write_text(json.dumps({'scope':'Geometry and stylesheet verification; screenshots require independent visual review.','results':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'units':len(units),'modes':2,'tablesChecked':sum(len(x['tables']) for x in results),'screenshots':sum(len(x['screenshots']) for x in results),'passed':True}))


if __name__ == '__main__':
    main()
