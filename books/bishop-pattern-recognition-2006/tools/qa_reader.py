"""Check compiled PRML units in the real reader, including mobile dark mode."""
import argparse
import json
from pathlib import Path
import re
from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
OUTPUT = ROOT / 'tmp/prml-browser-qa'
BOOK_ID = BOOK.name


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def wait_for_scroll_settled(page):
    page.evaluate('''() => new Promise((resolve, reject) => {
      let previous = scrollY, stable = 0;
      const started = performance.now();
      function frame() {
        stable = Math.abs(scrollY - previous) < 0.1 ? stable + 1 : 0;
        previous = scrollY;
        if (stable >= 8) return resolve();
        if (performance.now() - started > 10000) return reject(new Error('Scroll did not settle'));
        requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    })''')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('units', nargs='+')
    parser.add_argument('--base', default='http://127.0.0.1:8794/')
    parser.add_argument('--details', action='store_true', help='Capture demanding formulas, tables, biographies and reference jumps')
    parser.add_argument('--output-dir', type=Path, default=OUTPUT, help='Separate screenshots for incremental review')
    parser.add_argument('--report-suffix', default='', help='Preserve earlier evidence reports')
    parser.add_argument('--report-name', help='Short JSON filename for full-book checks on Windows')
    parser.add_argument('--require-reference', action='store_true', help='Require a real within-unit reference jump, including appendices')
    args = parser.parse_args()
    if args.report_name and not re.fullmatch(r'[a-z0-9-]+\.json', args.report_name):
        parser.error('--report-name must be a simple lowercase JSON filename')
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as runner:
        installed = sorted((Path.home()/'AppData/Local/ms-playwright').glob(
            'chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))
        browser = runner.chromium.launch(headless=True, **({'executable_path':str(installed[-1])} if installed else {}))
        for key in args.units:
            unit = json.loads((BOOK/f'{key}.json').read_text(encoding='utf-8'))
            for screen, width, height, theme in [('desktop-light',1440,1000,'light'),('mobile-dark',390,844,'dark')]:
                context = browser.new_context(viewport={'width':width,'height':height}, service_workers='block', color_scheme=theme)
                page = context.new_page()
                errors = []
                page.on('pageerror',lambda error: errors.append(str(error)))
                page.goto(f'{args.base}?book={BOOK_ID}&chapter={key}')
                page.locator('.reading-block').first.wait_for()
                page.evaluate('document.fonts.ready')
                math_font_loaded = (page.evaluate('document.fonts.check(\'17px "PRML Math"\')')
                                    if page.locator('#reader-article math').count() else None)
                assert math_font_loaded is not False, 'PRML math font not loaded'
                expected_blocks = sum('kind' in value and value['kind'] != 'box' for value in walk(unit['blocks']))
                assert page.locator('.reading-block').count() == expected_blocks, (key,expected_blocks)
                assert page.locator('html').get_attribute('data-theme') == theme
                for pic in page.locator('.book-figure img').all():
                    pic.evaluate("img => { img.loading='eager'; return img.decode(); }")
                    assert pic.evaluate('img => img.naturalWidth > 0'), key
                expected_math = sum('mathml' in value for value in walk(unit['blocks']))
                assert page.locator('#reader-article math').count() == expected_math, (key,expected_math)
                assert page.locator('.formula-fallback, .figure-error').count() == 0, key
                fences = page.evaluate('''() => [...document.querySelectorAll('#reader-article mtable')].flatMap(table => {
                  if (table.children.length < 2) return [];
                  return [...table.parentElement.children].filter(node => node.tagName === 'mo' &&
                    node.getAttribute('fence') === 'true' && node.getAttribute('stretchy') !== 'false')
                    .map(node => ({glyph:node.textContent, fenceHeight:node.getBoundingClientRect().height,
                      tableHeight:table.getBoundingClientRect().height}));
                })''')
                assert all(f['fenceHeight'] >= .85 * f['tableHeight'] for f in fences), (key, fences)
                fraction_fences = page.evaluate('''() => [...document.querySelectorAll('#reader-article mo[fence="true"]')]
                  .filter(node => node.textContent === '∣').flatMap(node => {
                    const row = node.closest('mrow');
                    const fractions = row ? [...row.children].filter(child => child.tagName === 'mfrac') : [];
                    if (!fractions.length) return [];
                    return [{block:node.closest('.reading-block').id,
                      fenceHeight:node.getBoundingClientRect().height,
                      fractionHeight:Math.max(...fractions.map(child => child.getBoundingClientRect().height))}];
                  })''')
                assert all(f['fenceHeight'] >= .85 * f['fractionHeight'] for f in fraction_fences), (key, fraction_fences)
                assert not errors, errors
                text = page.locator('#reader-article').inner_text()
                assert 'BISHOPMATH' not in text and '\\tag{' not in text, key
                dims = page.evaluate('({width:innerWidth, scroll:document.documentElement.scrollWidth})')
                assert dims['scroll'] <= dims['width'], (key,dims)
                page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                page.screenshot(path=str(output/f'{key}-start-{screen}.png'))
                # Exercise real within-chapter navigation rather than just counting links.
                toc = page.locator('#reader-toc-mobile' if screen.startswith('mobile') else '#reader-toc')
                section = toc.locator('.toc-section-link').last
                toc_landing = None
                if section.count():
                    if screen.startswith('mobile'):
                        page.locator('#toc-toggle').click()
                    href = section.get_attribute('href')
                    section.click()
                    assert page.locator(href).count() == 1
                    page.wait_for_function('(hash) => location.hash === hash', arg=href)
                    wait_for_scroll_settled(page)
                    page.wait_for_function('(id) => { const r=document.querySelector(id).getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; }',arg=href)
                    toc_landing = page.evaluate('''id => {
                      const r=document.querySelector(id).getBoundingClientRect();
                      const bar=document.querySelector('.reader-topbar').getBoundingClientRect();
                      return {target:id,top:r.top,bottom:r.bottom,toolbarBottom:bar.bottom,viewport:innerHeight,scrollY};
                    }''',href)
                    assert toc_landing['top'] >= toc_landing['toolbarBottom'], toc_landing
                    assert toc_landing['bottom'] <= toc_landing['viewport'], toc_landing
                    if screen.startswith('mobile'):
                        assert not page.locator('#toc-dialog').is_visible()
                page.screenshot(path=str(output/f'{key}-{screen}.png'))
                # Confirm later text, not just the first viewport, and progress restoration.
                last_block = page.locator('#reader-article > :last-child')
                last_block.scroll_into_view_if_needed()
                page.evaluate('window.scrollTo({top:document.documentElement.scrollHeight,behavior:"instant"})')
                last_id = last_block.get_attribute('id')
                page.wait_for_function('([key,id]) => JSON.parse(localStorage.getItem(key) || "null")?.block === id',
                                       arg=[f'intelligence-library:progress:v2:{BOOK_ID}',last_id])
                saved = page.evaluate('(key) => JSON.parse(localStorage.getItem(key))',f'intelligence-library:progress:v2:{BOOK_ID}')
                assert saved['chapter'] == key
                page.screenshot(path=str(output/f'{key}-end-{screen}.png'))
                if key == 'frontmatter':
                    page.locator('img[alt="Springer 出版社标志"]').scroll_into_view_if_needed()
                    page.screenshot(path=str(output/f'{key}-publisher-{screen}.png'))
                    page.evaluate('window.scrollTo({top:document.documentElement.scrollHeight,behavior:"instant"})')
                    page.wait_for_function('([key,id]) => JSON.parse(localStorage.getItem(key) || "null")?.block === id',
                                           arg=[f'intelligence-library:progress:v2:{BOOK_ID}',last_id])
                # Remove a preceding navigation hash so the saved position controls reload.
                page.evaluate('history.replaceState(null,"",location.pathname+location.search)')
                page.reload()
                page.locator('.reading-block').first.wait_for()
                page.wait_for_function('(id) => {const r=document.getElementById(id).getBoundingClientRect();return r.top<innerHeight && r.bottom>0;}',arg=last_id)
                formula = page.locator('.book-formula').first
                if formula.count():
                    formula.scroll_into_view_if_needed()
                    page.screenshot(path=str(output/f'{key}-formula-{screen}.png'))
                details = []
                reference_checked = False
                if args.details:
                    candidates = [b for b in walk(unit['blocks']) if b.get('kind')=='formula']
                    candidates.sort(key=lambda b:len(b.get('tex','')),reverse=True)
                    selected = candidates[:3]
                    selected += [b for b in walk(unit['blocks']) if b.get('kind') in {'table','box'}]
                    for block in selected:
                        locator = page.locator('#read-'+block['id'])
                        locator.scroll_into_view_if_needed()
                        page.wait_for_function('(id) => {const r=document.getElementById(id).getBoundingClientRect();return r.top<innerHeight && r.bottom>0;}',arg='read-'+block['id'])
                        scroller = locator.locator('.formula-scroll').first
                        if scroller.count() and scroller.evaluate('el=>el.scrollWidth>el.clientWidth+2'):
                            scroller.evaluate('el=>{el.scrollLeft=el.scrollWidth}')
                            assert scroller.evaluate('el=>el.scrollLeft>0'), block['id']
                            scroller.evaluate('el=>{el.scrollLeft=0}')
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                        page.screenshot(path=str(output/f'{key}-{block["id"]}-{screen}.png'))
                        details.append(block['id'])
                    link = page.locator('#reader-article a.reading-reference[href^="#read-"]').first
                    if link.count():
                        href = link.get_attribute('href')
                        link.scroll_into_view_if_needed()
                        link.click()
                        page.wait_for_function('(h)=>location.hash===h',arg=href)
                        wait_for_scroll_settled(page)
                        page.wait_for_function('(id)=>{const r=document.querySelector(id).getBoundingClientRect();return r.top<innerHeight&&r.bottom>0;}',arg=href)
                        reference_checked = True
                    if key.startswith('chapter-') or args.require_reference:
                        assert reference_checked, f'{key}: no in-chapter reference link was available to verify'
                results.append({'unit':key,'screen':screen,'blocks':len(unit['blocks']),
                                'images':page.locator('.book-figure img').count(),'math':expected_math,
                                'mathFontLoaded':math_font_loaded,'matrixFenceGeometry':fences,
                                'fractionFenceGeometry':fraction_fences,
                                'pageWidth':dims['width'],'scrollWidth':dims['scroll'],'consoleErrors':errors,
                                'savedEndBlock':saved['block'],'restoredEndBlockVisible':True,
                                'settledTocLanding':toc_landing,
                                'detailBlocks':details,'inChapterReferenceJump':reference_checked})
                context.close()
        browser.close()
    target = BOOK/'reviews'/(args.report_name or ('reader-qa-'+'-'.join(args.units)+args.report_suffix+'.json'))
    target.write_text(json.dumps({'results':results,'screenshots':str(output),'scope':'Rendering checks only; source fidelity requires independent review.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(results),'pass':True,'report':str(target)},ensure_ascii=False))


if __name__ == '__main__':
    main()
