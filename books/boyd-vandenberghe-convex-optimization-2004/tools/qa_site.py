"""Exercise this book through the real site registry and service worker."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import ThreadingHTTPServer
import hashlib
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

from common import BOOK, BOOK_ID, CHAPTERS, ROOT
from qa_reader import QuietHandler


def run(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    documents = {c.id: json.loads((BOOK / f"chapter-{c.id}.json").read_text(encoding="utf-8")) for c in CHAPTERS}
    manifest = json.loads((BOOK / "offline-images.json").read_text(encoding="utf-8"))
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/"
    errors = []
    views = []
    try:
        with sync_playwright() as playwright:
            binaries = sorted((Path.home() / "AppData/Local/ms-playwright").glob(
                "chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"))
            options = {"headless": True}
            if binaries:
                options["executable_path"] = str(binaries[-1])
            browser = playwright.chromium.launch(**options)
            context = browser.new_context(viewport={"width":1440,"height":960}, service_workers="allow")
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(base + f"?book={BOOK_ID}&chapter=frontmatter")
            page.locator(".reading-block").first.wait_for()
            # No books.js interception: this is the actual current registry.
            registered = page.evaluate("id => books.find(book => book.id === id)", BOOK_ID)
            assert [c["id"] for c in registered["chapters"]] == list(documents)
            page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=60000)
            page.wait_for_function("""async ({id,version}) => {
                const cache = await caches.open('intelligence-library-images-v1');
                const response = await cache.match(new URL('books/'+id+'/offline-images-version',location.href));
                return response && await response.text() === version;
            }""", arg={"id":BOOK_ID,"version":manifest["version"]}, timeout=60000)
            cached = page.evaluate("""async paths => {
                const results = [];
                for (const path of paths) {
                    const response = await caches.match(new URL(path,location.href));
                    results.push({path,ok:!!response && response.ok});
                }
                return results;
            }""", [c["content"] for c in registered["chapters"]] + [
                f"books/{BOOK_ID}/offline-images.json",f"books/{BOOK_ID}/assets/fonts/STIXTwoMath-Regular.woff2"])
            assert all(c["ok"] for c in cached), cached
            context.set_offline(True)
            for label,width,height,theme in [("desktop-light",1440,960,"light"),("mobile-light",390,844,"light"),
                                             ("mobile-dark",390,844,"dark"),("narrow-dark",320,740,"dark")]:
                page.set_viewport_size({"width":width,"height":height})
                page.emulate_media(color_scheme=theme)
                for chapter,doc in documents.items():
                    page.goto(base + f"?book={BOOK_ID}&chapter={chapter}")
                    page.locator(".reading-block").first.wait_for()
                    page.evaluate("document.fonts.load('18px \"Convex STIX Two Math\"')")
                    page.evaluate("document.fonts.ready")
                    assert page.locator("#reader-status").is_hidden(), (chapter,label)
                    assert page.locator("#reader-article .reading-block").count()==len(doc["blocks"])
                    assert page.locator("html").get_attribute("data-theme")==theme
                    assert page.locator("#reader-article merror").count()==0
                    dimensions=page.evaluate("({width:innerWidth,content:document.documentElement.scrollWidth})")
                    assert dimensions["content"]<=width,(chapter,label,dimensions)
                    images=page.locator("#reader-article img").evaluate_all("""async images => Promise.all(images.map(async img => {
                        img.loading='eager'; try { await img.decode(); return img.naturalWidth>0; } catch { return false; }
                    }))""")
                    assert len(images)==len(doc["images"]) and all(images),(chapter,label)
                    views.append({"chapter":chapter,"view":label,"offline":True,"blocks":len(doc["blocks"]),
                                  "math":page.locator("#reader-article math").count(),"images":len(images),"dimensions":dimensions})
                    if chapter in ['01','02','A','C','references','notation']:
                        page.evaluate("scrollTo({top:0,behavior:'instant'})")
                        page.screenshot(path=str(output/f'{chapter}-{label}.png'))
                if width<600:
                    page.get_by_role('button',name='目录',exact=True).click()
                    assert page.locator('#reader-toc-mobile .toc-chapter-link').count()==23
                    page.get_by_role('button',name='关闭',exact=True).click()
            # Read every cached image while offline, including never-visited figures,
            # and compare the actual response bytes with the workspace artifacts.
            image_hashes=page.evaluate("""async paths => {
                const results=[];
                for (const path of paths) {
                    const response=await fetch(new URL(path,location.href));
                    const bytes=await response.arrayBuffer();
                    const digest=await crypto.subtle.digest('SHA-256',bytes);
                    results.push({path,bytes:bytes.byteLength,sha256:[...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,'0')).join('')});
                }
                return results;
            }""",manifest['assets'])
            for record in image_hashes:
                data=(ROOT/record['path']).read_bytes()
                assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256']
            assert not errors,errors
            context.close()
            browser.close()
        result={'passed':True,'registryIntercepted':False,'serviceWorkerUsed':True,'offlineViews':views,
                'cachedCoreAssets':cached,'offlineImageHashes':image_hashes,'javascriptErrors':errors,
                'scope':'Real-site offline integration check; chapter semantics are covered by independent chapter reviews.'}
        (output/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        return result
    finally:
        server.shutdown()
        server.server_close()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'tmp/convex/site-qa')
    args=parser.parse_args()
    result=run(args.output)
    print(json.dumps({'passed':result['passed'],'offlineViews':len(result['offlineViews']),
                      'imagesHashChecked':len(result['offlineImageHashes'])}))
