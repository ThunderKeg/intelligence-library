"""Capture one requested reader block for a review finding."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]


def walk_blocks(blocks):
    for block in blocks:
        yield block
        yield from walk_blocks(block.get('blocks', []))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('unit')
    parser.add_argument('target', help='Block ID or equation number such as 1.70')
    parser.add_argument('--width', type=int, default=390)
    parser.add_argument('--height', type=int, default=844)
    parser.add_argument('--theme', choices=['light','dark'], default='dark')
    args = parser.parse_args()
    data = json.loads((BOOK/f'{args.unit}.json').read_text(encoding='utf-8'))
    blocks = list(walk_blocks(data['blocks']))
    target = next((b['id'] for b in blocks if b.get('number')==f'({args.target})'),args.target)
    if not any(b.get('id') == target for b in blocks):
        raise ValueError(f'Unknown block or equation {args.target} in {args.unit}')
    output = ROOT/'tmp/prml-browser-qa'/f'{args.unit}-target-{args.target}-{args.width}-{args.theme}.png'
    with sync_playwright() as runner:
        installed = sorted((Path.home()/'AppData/Local/ms-playwright').glob('chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe'))
        browser = runner.chromium.launch(headless=True, **({'executable_path':str(installed[-1])} if installed else {}))
        context = browser.new_context(viewport={'width':args.width,'height':args.height},color_scheme=args.theme,service_workers='block')
        page = context.new_page()
        page.goto(f'http://127.0.0.1:8794/?book={BOOK.name}&chapter={args.unit}#read-{target}')
        block = page.locator('#read-'+target)
        block.wait_for()
        page.evaluate('document.fonts.ready')
        if page.locator('#reader-article math').count():
            assert page.evaluate('document.fonts.check(\'17px "PRML Math"\')'), 'PRML math font not loaded'
        for image in page.locator('.book-figure img').all():
            image.evaluate("img=>{img.loading='eager';return img.decode();}")
        block.evaluate("el=>el.scrollIntoView({block:'start',behavior:'instant'})")
        page.wait_for_function('(id)=>{const r=document.getElementById(id).getBoundingClientRect();return r.top<innerHeight&&r.bottom>0;}',arg='read-'+target)
        page.screenshot(path=str(output))
        print(json.dumps({'image':str(output),'block':target,'text':block.inner_text()},ensure_ascii=False))
        browser.close()


if __name__ == '__main__':
    main()
