"""Verify that the public catalog and all PRML content work without a network."""
import argparse
import hashlib
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from qa_reader import walk

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://127.0.0.1:8795')
    parser.add_argument('--artifact-root', type=Path, default=ROOT,
                        help='Root containing the exact deployed resource bytes.')
    parser.add_argument('--output-dir', type=Path, default=ROOT/'tmp/prml-offline-final')
    parser.add_argument('--report', type=Path, default=BOOK/'reviews/offline-final-qa.json')
    parser.add_argument('--ready-timeout', type=int, default=60000)
    args = parser.parse_args()
    args.base = args.base.rstrip('/')
    asset_root = args.artifact_root.resolve()
    inventory = json.loads((BOOK/'source-inventory.json').read_text(encoding='utf8'))
    images = json.loads((BOOK/'offline-images.json').read_text(encoding='utf8'))
    resources = [f'books/{BOOK.name}/{x["id"]}.json' for x in inventory['units']]
    resources += [f'books/{BOOK.name}/{name}' for name in ('reference-index.json','offline-images.json','assets/fonts/STIXTwoMath-Regular.woff2')]
    resources += images['assets']
    expected_hashes={path:hashlib.sha256((asset_root/path).read_bytes()).hexdigest() for path in resources}
    catalog=json.loads((BOOK/'reviews/catalog-integration-plan.json').read_text(encoding='utf8'))
    labels={entry['id']:f"{entry['number']} {entry['title']}".strip() for entry in catalog['chapters']}
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        exe = sorted((Path.home()/'AppData/Local/ms-playwright').glob('chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))[-1]
        browser = pw.chromium.launch(headless=True, executable_path=str(exe))
        context = browser.new_context(viewport={'width':390,'height':844},color_scheme='dark')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(f'{args.base}/?book={BOOK.name}&chapter=frontmatter')
        page.locator('.reading-block').first.wait_for()
        page.wait_for_function('navigator.serviceWorker.controller !== null', timeout=args.ready_timeout)
        page.wait_for_function('document.querySelector("#offline-panel").dataset.state === "complete"', timeout=args.ready_timeout)
        cached = page.evaluate('''async paths => {
          const result=[];
          for(const path of paths) {
            const response=await caches.match(new URL(path,document.baseURI));
            const data=response?await response.arrayBuffer():new ArrayBuffer(0);
            const digest=await crypto.subtle.digest('SHA-256',data);
            const sha256=[...new Uint8Array(digest)].map(n=>n.toString(16).padStart(2,'0')).join('');
            result.push({path,cached:!!response,bytes:data.byteLength,sha256});
          }
          return result;
        }''', resources)
        assert all(x['cached'] for x in cached), [x for x in cached if not x['cached']]
        assert all(x['bytes']==(asset_root/x['path']).stat().st_size for x in cached)
        assert all(x['sha256']==expected_hashes[x['path']] for x in cached)
        context.set_offline(True)
        responses = []
        page.on('response', lambda r: responses.append({'url':r.url,'status':r.status,'fromServiceWorker':r.from_service_worker}))
        fetched = page.evaluate('''async paths => {
          const rows=[];
          for(const path of paths) {
            const response=await fetch(new URL(path,document.baseURI),{cache:'reload'});
            const data=await response.arrayBuffer();
            const digest=await crypto.subtle.digest('SHA-256',data);
            const sha256=[...new Uint8Array(digest)].map(n=>n.toString(16).padStart(2,'0')).join('');
            rows.push({path,status:response.status,bytes:data.byteLength,sha256});
          }
          return rows;
        }''',resources)
        assert all(x['status']==200 and x['bytes']==(asset_root/x['path']).stat().st_size for x in fetched)
        assert all(x['sha256']==expected_hashes[x['path']] for x in fetched)
        for index,unit in enumerate(inventory['units']):
            key=unit['id']
            compiled=json.loads((BOOK/f'{key}.json').read_text(encoding='utf8'))
            expected_blocks=sum('kind' in block and block['kind']!='box' for block in walk(compiled['blocks']))
            expected_math=sum('mathml' in block for block in walk(compiled['blocks']))
            expected_title=next(block['text'] for block in walk(compiled['blocks'])
                                if block.get('kind')=='heading' and block.get('level')==1)
            response=page.goto(f'{args.base}/?book={BOOK.name}&chapter={key}')
            assert response and response.from_service_worker and response.ok
            page.locator('.reading-block').first.wait_for()
            # The article is inserted before the asynchronous reference index
            # finishes; wait for the rest of renderReader before checking TOC.
            page.wait_for_function(
                '(count) => document.querySelectorAll("#reader-toc .toc-chapter-link").length === count',
                arg=len(inventory['units']))
            assert page.locator('#reader-article').get_attribute('data-book-id')==BOOK.name
            assert page.locator('#reader-article h1').inner_text()==expected_title
            assert page.locator('.reading-block').count()==expected_blocks
            assert page.locator('html').get_attribute('data-theme')=='dark'
            assert page.locator('#reader-toc .toc-chapter-link').count()==25
            current=page.locator('#reader-toc .chapter-current')
            assert current.count()==1 and current.get_attribute('href')=='#read-'+compiled['toc'][0]['block']
            assert current.inner_text().strip()==labels[key]
            adjacent=[inventory['units'][i]['id'] for i in (index-1,index+1) if 0<=i<len(inventory['units'])]
            expected_navigation=[f'{args.base}/?book={BOOK.name}&chapter={key}' for key in adjacent]
            assert page.locator('#chapter-navigation a').evaluate_all('els=>els.map(el=>el.href)')==expected_navigation
            expected_images=[f'{args.base}/books/{BOOK.name}/{b["src"]}' for b in walk(compiled['blocks']) if b.get('kind')=='figure']
            assert page.locator('.book-figure img').evaluate_all('els=>els.map(el=>el.src)')==expected_images
            for image in page.locator('.book-figure img').all():
                image.evaluate("img=>{img.loading='eager';return img.decode()}")
                assert image.evaluate('img=>img.naturalWidth>0')
            page.evaluate('document.fonts.ready')
            math=page.locator('#reader-article math').count()
            assert math==expected_math
            assert page.locator('.formula-fallback, .figure-error').count()==0
            if math:
                assert page.evaluate('document.fonts.check(\'17px "PRML Math"\')')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            row={'unit':key,'blocks':page.locator('.reading-block').count(),'math':math,
                 'images':page.locator('.book-figure img').count(),'navigationFromServiceWorker':True}
            if key in {'chapter-05','contents','index'}:
                page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
                path=out/f'{key}.png';page.screenshot(path=str(path))
                row.update(file=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            results.append(row)
        assert not errors, errors
        context.close();browser.close()
    assert all(x['fromServiceWorker'] and x['status']==200 for x in responses), [x for x in responses if not x['fromServiceWorker'] or x['status']!=200]
    report={'passed':True,'base':args.base,'artifactRoot':str(asset_root),
            'offlineResources':fetched,'cacheBeforeDisconnect':cached,
            'units':results,'responses':responses,'consoleErrors':errors}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'passed':True,'units':len(results),'offlineResources':len(resources),'images':len(images['assets'])}))


if __name__=='__main__':
    main()
