"""Index available PRML units without declaring unreviewed chapters complete."""
import hashlib
import json
from pathlib import Path
import re

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
NUMBER = r'(?:[A-E]|\d+)\.\d+'


def walk(blocks):
    for block in blocks:
        yield block
        yield from walk(block.get('blocks',[]))


def main():
    inventory = json.loads((BOOK/'source-inventory.json').read_text(encoding='utf-8'))
    targets = {kind:{} for kind in ('chapter','section','figure','table','formula','exercise','algorithm')}
    assets = []

    def add(kind, number, unit, block):
        entry = {'chapter':unit,'block':block}
        previous = targets[kind].setdefault(number,entry)
        if previous != entry:
            raise ValueError(f'Duplicate {kind} {number}: {previous} / {entry}')

    for unit in inventory['units']:
        key = unit['id']
        path = BOOK/f'{key}.json'
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        if key.startswith('chapter-'):
            add('chapter',str(int(key.split('-')[1])),key,data['blocks'][0]['id'])
        elif key.startswith('appendix-'):
            add('chapter',key[-1].upper(),key,data['blocks'][0]['id'])
        for b in walk(data['blocks']):
            text = b.get('text','')
            kind = b['kind']
            if kind == 'heading' and (m:=re.match(rf'^({NUMBER}(?:\.\d+)?)\s',text)):
                add('section',m[1],key,b['id'])
            elif kind == 'figure' and (m:=re.match(rf'^图\s*({NUMBER})(?!\d)',b.get('caption',''))):
                add('figure',m[1],key,b['id'])
            elif kind == 'table' and (m:=re.match(rf'^表\s*({NUMBER})(?!\d)',b.get('caption',''))):
                add('table',m[1],key,b['id'])
            elif kind == 'formula' and (m:=re.fullmatch(rf'\(({NUMBER})\)',b.get('number',''))):
                add('formula',m[1],key,b['id'])
            elif kind in {'paragraph','exercise'} and (m:=re.match(rf'^(?:习题\s*)?({NUMBER})[（(][⋆★*]+',text)):
                add('exercise',m[1],key,b['id'])
        assets.extend(data.get('images',[]))
    assets = sorted(set(assets))
    digest = hashlib.sha256()
    total_bytes = 0
    for asset in assets:
        if not asset.startswith(f'books/{BOOK.name}/assets/') or '..' in Path(asset).parts:
            raise ValueError(f'Invalid asset {asset}')
        contents = (ROOT/asset).read_bytes()
        digest.update(asset.encode('utf-8'))
        digest.update(hashlib.sha256(contents).digest())
        total_bytes += len(contents)
    (BOOK/'reference-index.json').write_text(json.dumps({'bookId':BOOK.name,'targets':targets},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (BOOK/'offline-images.json').write_text(json.dumps({'bookId':BOOK.name,'version':digest.hexdigest()[:20],
        'totalBytes':total_bytes,'assets':assets},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'targets':{k:len(v) for k,v in targets.items()},'images':len(assets),'imageBytes':total_bytes}))


if __name__ == '__main__':
    main()
