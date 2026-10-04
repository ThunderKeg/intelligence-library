"""Align the original contents with reviewed headings and add reader links."""
import argparse
import json
from pathlib import Path
import re

BOOK = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Write the reviewed-heading links into the source')
    args = parser.parse_args()
    inventory = json.loads((BOOK/'source-inventory.json').read_text(encoding='utf-8'))
    targets = json.loads((BOOK/'reference-index.json').read_text(encoding='utf-8'))['targets']
    units = {u['id']:u for u in inventory['units']}
    missing = [key for key,u in units.items() if key != 'contents'
               and (not (BOOK/f'{key}.json').is_file() or u.get('review',{}).get('status') != 'accepted')]
    if missing:
        raise SystemExit('Finish independent content acceptance first: '+', '.join(missing))
    data = {key:json.loads((BOOK/f'{key}.json').read_text(encoding='utf-8')) for key in units}
    source = BOOK/'translation/contents.md'
    rows = []
    changes = []
    linked = []
    for line in source.read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'- (.+) — (\S+)',line)
        if not match:
            rows.append(line)
            continue
        marked,page_label = match.groups()
        strong = marked.startswith('**') and marked.endswith('**')
        title = marked[2:-2] if strong else marked
        existing_link = re.fullmatch(r'\[(.+)\]\([^\s]+\)',title)
        if existing_link:
            title = existing_link[1]
        pdf_page = int(page_label)+20 if page_label.isdigit() else {'vii':7,'xi':11,'xiii':13}[page_label]
        unit_key = next(key for key,u in units.items() if u['start'] <= pdf_page <= u['end'])
        contents = data[unit_key]['toc']
        numbered = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$',title)
        if numbered:
            number = numbered[1]
            kind = 'section' if '.' in number else 'chapter'
            target = targets[kind][number]
            if target['chapter'] != unit_key:
                raise ValueError(f'Contents unit/page mismatch: {title}, {page_label}, {target}')
            heading = next(h for h in contents if h['block'] == target['block'])
            final_title = number+' '+heading['title']
        elif title == '习题':
            heading = next(h for h in contents if h['title'] == '习题')
            final_title = title
        elif title.startswith('附录 '):
            heading = contents[0]
            final_title = data[unit_key]['title']
        else:
            heading = contents[0]
            final_title = title
        block = next(b for b in data[unit_key]['blocks'] if b['id'] == heading['block'])
        if block['pdfPage'] != pdf_page:
            raise ValueError(f'Contents printed page mismatch: {title}, expected {pdf_page}, actual {block["pdfPage"]}')
        href = f'?book={BOOK.name}&chapter={unit_key}#read-{heading["block"]}'
        label = f'[{final_title}]({href})'
        if strong:
            label = '**'+label+'**'
        rows.append('- '+label+' — '+page_label)
        if title != final_title:
            changes.append({'original':title,'aligned':final_title,'pageLabel':page_label,'target':href})
        linked.append({'title':final_title,'pageLabel':page_label,'pdfPage':pdf_page,'target':href})
    if len(linked) != 285:
        raise ValueError(f'Expected 285 original contents rows, got {len(linked)}')
    if args.write:
        source.write_text('\n'.join(rows)+'\n',encoding='utf-8')
        (BOOK/'reviews/contents-navigation-build.json').write_text(json.dumps({
            'scope':'Link and heading alignment only; independent editorial review remains required.',
            'rows':linked,'titleChanges':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'rows':len(linked),'alignedTitles':len(changes),'written':args.write},ensure_ascii=False))


if __name__ == '__main__':
    main()
