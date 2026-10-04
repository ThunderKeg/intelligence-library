"""Add original-page and see-also links without changing index text or emphasis."""
import json
from pathlib import Path
import re

from bs4 import BeautifulSoup, NavigableString

BOOK = Path(__file__).resolve().parents[1]


def walk(blocks):
    for block in blocks:
        yield block
        yield from walk(block.get('blocks', []))


def key(value):
    return ' '.join(value.replace('’', "'").split())


def link_index(chapter):
    inventory = json.loads((BOOK/'source-inventory.json').read_text(encoding='utf8'))
    page_targets = {}
    for unit in inventory['units']:
        if unit['id'] == 'index':
            continue
        data = json.loads((BOOK/(unit['id']+'.json')).read_text(encoding='utf8'))
        blocks = list(walk(data['blocks']))
        for block in blocks:
            if block['kind'] == 'intro':
                continue
            target = {'chapter': unit['id'], 'block': block['id']}
            for page in [block.get('pdfPage'), *block.get('continuedPdfPages', [])]:
                if page is not None:
                    page_targets.setdefault(page, target)

    entries = []
    terms = {}
    for block in chapter['blocks']:
        if block['kind'] != 'rich':
            continue
        soup = BeautifulSoup(block['html'], 'html.parser')
        paragraph = soup.find('p', attrs={'data-index-key': True})
        if paragraph is None:
            raise ValueError(f'Index entry lacks a stable English key: {block["id"]}')
        term = key(paragraph['data-index-key'])
        if term in terms:
            raise ValueError(f'Duplicate index key: {term}')
        terms[term] = block['id']
        entries.append((block, soup, paragraph, term))

    links = []
    for block, soup, paragraph, term in entries:
        before_text = paragraph.get_text()
        before_bold = [n.get_text() for n in paragraph.find_all('strong')]
        before_italic = [n.get_text() for n in paragraph.find_all('em')]
        spans = paragraph.select('span.index-pages')
        see_spans = paragraph.select('[data-index-see]')
        has_children = any(name.startswith(term+'::') for name in terms)
        if (len(spans) > 1 or len(see_spans) > 1
                or (not spans and not see_spans and not has_children)):
            raise ValueError(f'Invalid index page/see structure in {term}')
        for span in spans:
            if span.find('a'):
                raise ValueError(f'Index source already contains page links: {term}')
            if not re.fullmatch(r'\s*(?:\d+|vii)(?:\s*[,，–\-]\s*(?:\d+|vii))*\s*', span.get_text()):
                raise ValueError(f'Unexpected page-list content in {term}: {span.get_text()}')
            for node in list(span.descendants):
                if not isinstance(node, NavigableString):
                    continue
                text = str(node)
                position = 0
                for match in re.finditer(r'\d+|vii', text):
                    if match.start() > position:
                        node.insert_before(NavigableString(text[position:match.start()]))
                    label = match.group()
                    page = int(label)+20 if label.isdigit() else 7
                    target = page_targets.get(page)
                    if target is None:
                        raise ValueError(f'No translated content for index page {label} ({term})')
                    href = f'?book={BOOK.name}&chapter={target["chapter"]}#read-{target["block"]}'
                    anchor = soup.new_tag('a', href=href)
                    anchor['class'] = ['index-page-link']
                    anchor.string = label
                    node.insert_before(anchor)
                    links.append({'kind':'page', 'term':term, 'sourceBlock':block['id'],
                                  'pageLabel':label, 'pdfPage':page, 'href':href,
                                  'targetChapter':target['chapter'], 'targetBlock':target['block']})
                    position = match.end()
                if position < len(text):
                    node.insert_before(NavigableString(text[position:]))
                node.extract()
        for span in see_spans:
            destination = key(span['data-index-see'])
            if destination not in terms:
                raise ValueError(f'Unknown see target {destination} from {term}')
            anchor = soup.new_tag('a', href='#read-'+terms[destination])
            anchor['class'] = ['index-see-link']
            for child in list(span.contents):
                anchor.append(child.extract())
            span.append(anchor)
            links.append({'kind':'see', 'term':term, 'block':block['id'],
                          'targetTerm':destination, 'href':anchor['href']})
        assert paragraph.get_text() == before_text, term
        assert [n.get_text() for n in paragraph.find_all('strong')] == before_bold, term
        assert [n.get_text() for n in paragraph.find_all('em')] == before_italic, term
        block['html'] = str(soup)
    report = {'scope':'Navigation only; original text, order and emphasis preserved.',
              'entries':len(entries), 'pageLinks':sum(x['kind']=='page' for x in links),
              'seeLinks':sum(x['kind']=='see' for x in links), 'links':links}
    (BOOK/'reviews/index-navigation-build.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
