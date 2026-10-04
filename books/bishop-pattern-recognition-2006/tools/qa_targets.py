"""Capture focused reader targets; screenshots still require visual inspection."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BOOK=Path(__file__).resolve().parent.parent
ROOT=BOOK.parent.parent

def walk(blocks):
    for block in blocks:
        yield block
        yield from walk(block.get('blocks',[]))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('unit')
    ap.add_argument('targets',nargs='*')
    ap.add_argument('--base',default='http://127.0.0.1:8794')
    ap.add_argument('--figures',action='store_true')
    ap.add_argument('--output-dir',type=Path,help='Separate incremental screenshots from earlier evidence')
    ap.add_argument('--report-suffix',default='',help='Preserve earlier target reports')
    args=ap.parse_args()
    unit=json.loads((BOOK/f'{args.unit}.json').read_text(encoding='utf8'))
    blocks=list(walk(unit['blocks']))
    targets=list(args.targets)
    if args.figures:
        targets.extend(b['id'] for b in blocks if b['kind']=='figure')
    targets=list(dict.fromkeys(targets))
    out=args.output_dir or ROOT/'tmp/prml-targets'/args.unit
    out.mkdir(parents=True,exist_ok=True)
    results=[]
    with sync_playwright() as pw:
        exe=sorted((Path.home()/'AppData/Local/ms-playwright').glob('chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))[-1]
        browser=pw.chromium.launch(headless=True,executable_path=str(exe))
        for width,height,theme in [(1440,1000,'light'),(390,844,'dark')]:
            ctx=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme,service_workers='block')
            page=ctx.new_page()
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(args.base+'/?book='+BOOK.name+'&chapter='+args.unit)
            page.locator('.reading-block').first.wait_for()
            page.evaluate('document.fonts.ready')
            page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
            if page.locator('#reader-article math').count():
                assert page.evaluate('document.fonts.check(\'17px "PRML Math"\')')
            for img in page.locator('.book-figure img').all():
                img.evaluate("el=>{el.loading='eager';return el.decode();}")
            for target in targets:
                bid=next((b['id'] for b in blocks if b.get('number')=='('+target+')'),target)
                loc=page.locator('#read-'+bid)
                loc.evaluate("el=>el.scrollIntoView({block:'start',behavior:'instant'})")
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                images=[]
                def shot(suffix=''):
                    path=out/f'{target}-{width}-{theme}{suffix}.png'
                    page.screenshot(path=str(path))
                    images.append(str(path))
                shot()
                pans=[]
                for i,scroller in enumerate(loc.locator('.formula-scroll,.figure-media').all()):
                    dims=scroller.evaluate('el=>({client:el.clientWidth,scroll:el.scrollWidth})')
                    if dims['scroll']>dims['client']+2:
                        scroller.evaluate('el=>{el.scrollLeft=el.scrollWidth}')
                        amount=scroller.evaluate('el=>el.scrollLeft')
                        assert amount>0
                        shot(f'-pan-{i}')
                        pans.append({'scrollLeft':amount,**dims})
                        scroller.evaluate('el=>{el.scrollLeft=0}')
                rect=loc.bounding_box()
                step=height-150
                for chunk in range(1,int((rect['height']-1)//step)+1):
                    loc.evaluate("(el,offset)=>window.scrollTo({top:el.getBoundingClientRect().top+scrollY+offset,behavior:'instant'})",chunk*step)
                    shot(f'-continuation-{chunk}')
                results.append({'target':target,'block':bid,'width':width,'theme':theme,'images':images,'pans':pans})
            assert not errors,errors
            ctx.close()
        browser.close()
    report=BOOK/'reviews'/f'reader-qa-{args.unit}-targets{args.report_suffix}.json'
    report.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'checks':len(results),'screenshots':sum(len(x['images']) for x in results),'passed':True}))

if __name__=='__main__':
    main()
