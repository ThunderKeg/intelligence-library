"""Verify current full-book acceptance, source coverage and navigation artifacts.

This audit checks recorded decisions and their fingerprints. It does not make
editorial decisions or replace the independent page and reader reviews.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit

from bs4 import BeautifulSoup
from build import review_fingerprint

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]


def walk(blocks):
    for block in blocks:
        yield block
        yield from walk(block.get('blocks', []))


def main():
    inventory = json.loads((BOOK/'source-inventory.json').read_text(encoding='utf8'))
    assert hashlib.sha256((ROOT/inventory['source']).read_bytes()).hexdigest() == inventory['sha256']
    expected = list(range(1, inventory['pdfPages']+1))
    assert [p for u in inventory['units'] for p in range(u['start'], u['end']+1)] == expected
    assert len(inventory['units']) == 25
    assert len(inventory['pages']) == len(expected)
    assert all(p.get('verifiedAgainstPage') is True for p in inventory['pages'])
    data = {u['id']: json.loads((BOOK/(u['id']+'.json')).read_text(encoding='utf8'))
            for u in inventory['units']}
    ids = {name: {b['id'] for b in walk(chapter['blocks'])} for name, chapter in data.items()}
    results = []
    all_images = set()
    totals = Counter()
    for unit in inventory['units']:
        name = unit['id']
        chapter = data[name]
        source = BOOK/'translation'/f'{name}.md'
        fingerprint = review_fingerprint(chapter, source)
        review = unit.get('review', {})
        assert review.get('status') == 'accepted' and chapter['editorialStatus'] == 'reviewed', name
        assert all(review.get(k) == v for k, v in fingerprint.items()), ('stale acceptance', name)
        assert (BOOK/review['record']).is_file(), name
        assert chapter['reviewRecord'] == review['record'], name
        for record in review.get('renderingAddenda', [])+review.get('structuralAddenda', []):
            assert (BOOK/record).is_file(), record
        for previous in review.get('previousReviews', []):
            assert previous.get('status')=='accepted' and (BOOK/previous['record']).is_file(), name
            for record in previous.get('renderingAddenda', []):
                assert (BOOK/record).is_file(), record
        blocks = list(walk(chapter['blocks']))
        counts = Counter(b['kind'] for b in blocks)
        expected_guides = 1 if name.startswith(('chapter-', 'appendix-')) else 0
        assert counts['intro'] == expected_guides, ('guide count', name, counts['intro'])
        assert sum(b['kind']=='heading' and b['level']==1 for b in blocks) == 1, name
        all_images.update(chapter['images'])
        totals.update(counts)
        results.append({'unit':name, 'pdfPages':[unit['start'],unit['end']],
                        'blocks':len(blocks), 'images':len(chapter['images']), **fingerprint,
                        'review':review['record']})

    def check_href(href, unit):
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc:
            return False
        assert parsed.path == '' and re.fullmatch(
            r'(?:\?book=[\w-]+&chapter=[\w-]+)?#read-[\w-]+', href), href
        query = parse_qs(parsed.query)
        destination = query.get('chapter', [unit])[0]
        assert query.get('book', [BOOK.name])[0] == BOOK.name, href
        assert destination in ids and parsed.fragment.startswith('read-'), href
        assert parsed.fragment[5:] in ids[destination], href
        return True

    link_counts = Counter()
    for name in ('contents', 'index'):
        for block in data[name]['blocks']:
            if block.get('originalContents'):
                for item in block['items']:
                    assert check_href(item['href'], name)
                    link_counts['contents'] += 1
            if block['kind'] == 'rich':
                for anchor in BeautifulSoup(block['html'], 'html.parser').find_all('a', href=True):
                    if check_href(anchor['href'], name):
                        link_counts['index'] += 1
    assert link_counts['contents'] == 285
    navigation = json.loads((BOOK/'reviews/index-navigation-build.json').read_text(encoding='utf8'))
    assert link_counts['index'] == navigation['pageLinks']+navigation['seeLinks']
    references = [b for b in data['references']['blocks'] if b['kind']=='rich']
    assert len(references) == 408
    assert all('reference-entry' in b['html'] for b in references)

    targets = json.loads((BOOK/'reference-index.json').read_text(encoding='utf8'))['targets']
    for kind, entries in targets.items():
        for number, target in entries.items():
            assert target['chapter'] in ids and target['block'] in ids[target['chapter']], (kind, number)
    offline = json.loads((BOOK/'offline-images.json').read_text(encoding='utf8'))
    assert set(offline['assets']) == all_images and len(offline['assets']) == len(all_images)
    assert all((ROOT/path).is_file() for path in all_images)
    assert sum((ROOT/path).stat().st_size for path in all_images) == offline['totalBytes']
    output = {'status':'passed', 'scope':__doc__, 'sourcePdfSha256':inventory['sha256'],
              'sourcePages':len(expected), 'units':results, 'blockKinds':dict(totals),
              'images':len(all_images), 'navigationLinks':dict(link_counts),
              'referenceTargets':{kind:len(entries) for kind,entries in targets.items()},
              'references':len(references), 'indexEntries':navigation['entries']}
    (BOOK/'reviews/full-book-verification.json').write_text(
        json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    print(json.dumps({k:v for k,v in output.items() if k not in ('scope','units')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
