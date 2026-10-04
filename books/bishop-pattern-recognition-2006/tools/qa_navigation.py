"""Exercise completed contents and index links in the actual reader."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlsplit

from playwright.sync_api import sync_playwright
from qa_reader import wait_for_scroll_settled

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://127.0.0.1:8794')
    parser.add_argument('--name', default='book-navigation')
    parser.add_argument('--scope', choices=('all','index','contents'), default='all')
    args = parser.parse_args()
    index = json.loads((BOOK/'reviews/index-navigation-build.json').read_text(encoding='utf8'))
    contents = (json.loads((BOOK/'reviews/contents-navigation-build.json').read_text(encoding='utf8'))
                if args.scope!='index' else {'rows':[]})
    # Cover each destination unit, the Roman frontmatter page and every see link.
    destinations = {}
    for item in index['links']:
        if item['kind'] == 'page':
            destinations.setdefault(item['targetChapter'], item)
    cases = [{'unit':'index', 'href':x['href'], 'kind':'page', 'label':x['term'], 'sourceBlock':x['sourceBlock'],
              'capture':x['targetChapter'] in {'preface','appendix-e','chapter-05'}}
             for x in destinations.values()]
    cases.extend({'unit':'index', 'href':x['href'], 'kind':'see', 'label':x['term'], 'sourceBlock':x['block'],
                  'capture':x['term'] in {'GEM','statistical learning theory','IRLS'}}
                 for x in index['links'] if x['kind']=='see')
    toc_units = {}
    for item in contents['rows']:
        toc_units.setdefault(item['target'].split('&chapter=')[1].split('#')[0], item)
    cases.extend({'unit':'contents', 'href':x['target'], 'kind':'contents',
                  'label':x['title'], 'capture':False} for x in toc_units.values())
    if args.scope!='all':
        cases = [case for case in cases if case['unit']==args.scope]
    out = ROOT/'tmp/prml-navigation'/args.name
    out.mkdir(parents=True, exist_ok=True)
    results = []
    compiled = {x['id']:json.loads((BOOK/(x['id']+'.json')).read_text(encoding='utf8'))
                for x in json.loads((BOOK/'source-inventory.json').read_text(encoding='utf8'))['units']}
    with sync_playwright() as pw:
        exe = sorted((Path.home()/'AppData/Local/ms-playwright').glob('chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))[-1]
        browser = pw.chromium.launch(headless=True, executable_path=str(exe))
        for width,height,theme in [(1440,1000,'light'),(390,844,'dark')]:
            context = browser.new_context(viewport={'width':width,'height':height}, color_scheme=theme, service_workers='block')
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            for number,case in enumerate(cases):
                page.goto(f'{args.base}/?book={BOOK.name}&chapter={case["unit"]}')
                page.locator('.reading-block').first.wait_for()
                if case['unit']=='index':
                    assert page.locator('#reader-article .index-page-link').count() == index['pageLinks']
                    assert page.locator('#reader-article .index-see-link').count() == index['seeLinks']
                else:
                    assert page.locator('#reader-article .contents-reader-link').count() == 285
                scope = '#read-'+case['sourceBlock'] if case.get('sourceBlock') else '#reader-article'
                link = page.locator(f'{scope} a[href="{case["href"]}"]').first
                assert link.count(), case
                link.scroll_into_view_if_needed()
                link.click()
                expected_url = urlsplit(urljoin(f'{args.base}/?book={BOOK.name}&chapter={case["unit"]}',case['href']))
                fragment = '#'+urlsplit(case['href']).fragment
                page.wait_for_function('(h)=>location.hash===h', arg=fragment)
                page.locator(fragment).wait_for()
                actual_url = urlsplit(page.url)
                assert (actual_url.scheme,actual_url.netloc,actual_url.path,parse_qs(actual_url.query)) == (
                    expected_url.scheme,expected_url.netloc,expected_url.path,parse_qs(expected_url.query)), (case,page.url)
                target_unit = parse_qs(expected_url.query)['chapter'][0]
                assert page.locator('#reader-article').get_attribute('data-book-id') == BOOK.name
                assert page.locator('#reader-article h1').inner_text() == compiled[target_unit]['title'], (case,page.url)
                page.evaluate('document.fonts.ready')
                wait_for_scroll_settled(page)
                geometry = page.locator(fragment).evaluate('el=>({top:el.getBoundingClientRect().top,bottom:el.getBoundingClientRect().bottom,bar:document.querySelector(".reader-topbar").getBoundingClientRect().bottom,viewport:innerHeight})')
                assert geometry['top'] >= geometry['bar']-1 and geometry['top'] < geometry['viewport'], (case,geometry)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                row = {**case, 'width':width,'theme':theme,'geometry':geometry,'finalUrl':page.url}
                if case['capture']:
                    path = out/f'{number:03}-{width}-{theme}.png'
                    page.screenshot(path=str(path))
                    row.update(file=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
                results.append(row)
            assert not errors, errors
            context.close()
        browser.close()
    report = {'passed':True,'scope':args.scope,'casesPerScreen':len(cases),'indexDestinationUnits':len(destinations),
              'contentsDestinationUnits':len(toc_units),'seeLinks':index['seeLinks'],'results':results}
    (BOOK/'reviews'/f'{args.name}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'passed':True,'clicks':len(results),'screenshots':sum('file' in x for x in results)}))


if __name__=='__main__':
    main()
