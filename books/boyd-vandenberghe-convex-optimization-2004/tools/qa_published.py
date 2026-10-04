"""Verify the published book from a fresh browser, then read unvisited content offline."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright
from common import BOOK, BOOK_ID, CHAPTERS, ROOT


def run(base: str, commit: str, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((BOOK / 'offline-images.json').read_text(encoding='utf-8'))
    errors, views = [], []
    with sync_playwright() as playwright:
        binaries = sorted((Path.home() / 'AppData/Local/ms-playwright').glob(
            'chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))
        browser = playwright.chromium.launch(headless=True, **({'executable_path': str(binaries[-1])} if binaries else {}))
        context = browser.new_context(viewport={'width': 390, 'height': 844}, color_scheme='dark', service_workers='allow')
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        # Only the front matter is visited before disconnecting; later figures
        # cannot have entered the cache through ordinary chapter navigation.
        page.goto(urljoin(base, f'?book={BOOK_ID}&chapter=frontmatter'))
        page.locator('.reading-block').first.wait_for()
        page.wait_for_function('navigator.serviceWorker.controller !== null', timeout=180000)
        page.wait_for_function("document.querySelector('#offline-panel')?.dataset.state === 'complete'", timeout=180000)
        sw = page.evaluate("async () => await (await fetch('sw.js', {cache:'no-store'})).text()")
        assert f'intelligence-library-{commit}' in sw, 'Published service worker has another build version'
        assert page.locator('#offline-panel').is_hidden()
        context.set_offline(True)
        hashes = page.evaluate('''async paths => {
            const result=[];
            for (const path of paths) {
                const r=await fetch(new URL(path,location.href));
                if (!r.ok) throw new Error(path+': '+r.status);
                const bytes=await r.arrayBuffer();
                const sha=await crypto.subtle.digest('SHA-256',bytes);
                result.push({path,bytes:bytes.byteLength,sha256:[...new Uint8Array(sha)].map(v=>v.toString(16).padStart(2,'0')).join('')});
            }
            return result;
        }''', manifest['assets'])
        for item in hashes:
            data = (ROOT / item['path']).read_bytes()
            assert len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256'], item
        # Verify every published JSON is the reviewed artifact, even offline.
        for chapter in CHAPTERS:
            path = f'books/{BOOK_ID}/chapter-{chapter.id}.json'
            actual = page.evaluate('async p => await (await fetch(p)).text()', path)
            assert actual == (ROOT/path).read_text(encoding='utf-8'), path
            page.goto(urljoin(base, f'?book={BOOK_ID}&chapter={chapter.id}'))
            page.locator('.reading-block').first.wait_for()
            page.evaluate('document.fonts.ready')
            assert page.locator('#reader-status').is_hidden()
            assert page.locator('merror').count() == 0
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            images = page.locator('#reader-article img').evaluate_all('''async images => Promise.all(images.map(async img => {
                img.loading='eager'; try { await img.decode(); return img.naturalWidth>0; } catch { return false; }
            }))''')
            assert all(images), chapter.id
            views.append({'chapter': chapter.id, 'images': len(images), 'offline': True})
        clicks = []
        for kind in ['chapter', 'section', 'formula', 'figure', 'example', 'exercise', 'algorithm', 'reference']:
            source_chapter = {'algorithm': 'C', 'example': '03'}.get(kind, '09')
            page.goto(urljoin(base, f'?book={BOOK_ID}&chapter={source_chapter}'))
            link = page.locator(f'#reader-article a[data-convex-reference="{kind}"]').first
            link.wait_for()
            href = link.get_attribute('href')
            target = href.split('#', 1)[1]
            label = link.inner_text()
            source_url = page.url
            source_block = link.evaluate("a => a.closest('.reading-block').id")
            link.click()
            page.wait_for_function('(id) => location.hash === "#"+id && !!document.getElementById(id)', arg=target)
            page.wait_for_function('(id) => {const r=document.getElementById(id).getBoundingClientRect();return r.top<innerHeight && r.bottom>0}', arg=target)
            page.reload()
            page.wait_for_function('(id) => {const n=document.getElementById(id);if(!n)return false;const r=n.getBoundingClientRect();return r.top<innerHeight && r.bottom>0}', arg=target)
            page.go_back()
            page.wait_for_url(source_url)
            page.wait_for_function('(id) => {const n=document.getElementById(id);if(!n)return false;const r=n.getBoundingClientRect();return r.top<innerHeight && r.bottom>0}', arg=source_block)
            clicks.append({'kind': kind, 'label': label, 'href': href, 'offline': True, 'reloadAndBack': True})
        page.screenshot(path=str(output/'published-mobile-dark.png'))
        assert not errors, errors
        browser.close()
    result = {'passed': True, 'url': base, 'commit': commit, 'onlineChaptersVisited': ['frontmatter'],
              'offlineImageHashesBeforeChapterVisits': hashes, 'offlineViews': views, 'offlineClicks': clicks, 'javascriptErrors': errors}
    (output/'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.url, args.commit, args.output)
    print(json.dumps({'passed': result['passed'], 'images': len(result['offlineImageHashesBeforeChapterVisits']),
                      'offlineViews': len(result['offlineViews']), 'offlineClicks': len(result['offlineClicks'])}))
