"""Structural checks against source inventory; never a substitute for translation review."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from build import protect_math, TAG
import fitz

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('units', nargs='+')
    parser.add_argument('--report-name', help='Short report filename for a full-book run')
    args = parser.parse_args()
    inventory = json.loads((BOOK/'source-inventory.json').read_text(encoding='utf-8'))
    results = []
    for key in args.units:
        unit = next(u for u in inventory['units'] if u['id'] == key)
        source = (BOOK/'translation'/f'{key}.md').read_text(encoding='utf-8')
        compiled = json.loads((BOOK/f'{key}.json').read_text(encoding='utf-8'))
        nodes = list(walk(compiled['blocks']))
        blocks = [n for n in nodes if 'kind' in n]
        ids = [n['id'] for n in blocks]
        assert len(ids) == len(set(ids)), ('duplicate IDs',key)
        markers = [int(n) for n in re.findall(r'<!--\s*pdf-page:\s*(\d+)\s*-->',source)]
        assert markers == list(range(unit['start'],unit['end']+1)), ('source page markers',key)
        assert compiled['sourcePdfSha256'] == inventory['sha256']
        assert not re.search(r'BISHOPMATH|\b(?:TODO|TBD)\b|此处略|待补',json.dumps(compiled,ensure_ascii=False))
        _, expressions = protect_math(source)
        source_math = Counter(TAG.sub('', tex).strip() if display else tex
                              for tex, display in expressions.values())
        compiled_math = Counter(n['tex'] for n in nodes if 'tex' in n)
        assert source_math == compiled_math, ('source/JSON mathematics differ', key,
                                              source_math-compiled_math, compiled_math-source_math)
        for n in nodes:
            if 'tex' in n:
                assert 'mathml' in n, ('uncompiled mathematics',key,n.get('tex'))
                ET.fromstring(n['mathml'])
                for letter in re.findall(r'\\boldsymbol\{\\mathsf\{([A-Za-z])\}\}',n['tex']):
                    glyph = chr((0x1D5D4+ord(letter)-65) if letter.isupper() else (0x1D5EE+ord(letter)-97))
                    assert f'mathvariant="bold-sans-serif">{glyph}</mi>' in n['mathml'], ('lost bold sans serif',key,n['tex'])
            if n.get('kind') == 'figure':
                assert n.get('alt'), ('missing alt',key,n['id'])
                assert (BOOK/n['src']).is_file(), ('missing image',key,n['src'])
        figures = [n for n in blocks if n['kind']=='figure']
        formulas = [n for n in blocks if n['kind']=='formula' and 'number' in n]
        actual_numbers = [n['number'].strip('()') for n in formulas]
        assert len(actual_numbers) == len(set(actual_numbers)), ('duplicate equation labels',key)
        manual_path = BOOK/'reviews'/f'source-checks-{key}.json'
        manual = None
        if manual_path.is_file():
            manual = json.loads(manual_path.read_text(encoding='utf-8'))
            assert manual['sourcePdfSha256'] == inventory['sha256'], ('manual source PDF mismatch',key)
            assert manual['unit'] == key and manual['pdfPages'] == [unit['start'],unit['end']], ('manual source range',key)
            assert (BOOK/manual['record']).is_file(), ('missing manual source record',key)
        if key.startswith('chapter-'):
            chapter = str(int(key.split('-')[1]))
            with fitz.open(ROOT/inventory['source']) as pdf:
                raw_pages = '\n'.join(pdf[p-1].get_text() for p in range(unit['start'], unit['end']+1))
            source_exercises = re.findall(rf'(?m)^({chapter}\.\d+)\s*\(([⋆★*]+)\)\s*(www)?', raw_pages)
            compiled_exercises = []
            for block in blocks:
                if block['kind'] not in {'paragraph', 'exercise'}:
                    continue
                match = re.match(rf'^(?:习题\s*)?({chapter}\.\d+)[（(]([⋆★*]+)[）)]\s*(www)?', block.get('text',''))
                if match:
                    compiled_exercises.append((match[1],match[2],match[3] or ''))
            # Scanned source pages can lose stars, www labels and even whole
            # exercise IDs in OCR. Use explicitly recorded page-inspection facts
            # when provided, never infer missing marks from the translation.
            expected_exercises = ([(x['number'],x['stars'],x['www']) for x in manual['exercises']]
                                  if manual else [(n,len(stars),bool(www)) for n,stars,www in source_exercises])
            actual_exercises = [(n,len(stars),bool(www)) for n,stars,www in compiled_exercises]
            assert expected_exercises and expected_exercises == actual_exercises, ('exercise IDs, difficulty or www markers', key)
            expected = {n for p in inventory['pages'][unit['start']-1:unit['end']] for n in p['equationCandidates'] if n.startswith(chapter+'.')}
            # This book numbers each chapter's equations consecutively, including exercises.
            if expected:
                end = max(int(n.split('.')[1]) for n in expected)
                expected.update(f'{chapter}.{n}' for n in range(1,end+1))
            if manual:
                expected = set(manual['numberedEquations'])
            assert set(actual_numbers) == expected, ('equation coverage',key,sorted(expected-set(actual_numbers)),sorted(set(actual_numbers)-expected))
            expected_figs = {n for p in inventory['pages'][unit['start']-1:unit['end']] for n in p['figureCandidates'] if n.startswith(chapter+'.')}
            if manual:
                expected_figs = set(manual['figures'])
            actual_figs = [m[1] for n in figures if (m:=re.match(r'图\s*(\d+\.\d+)',n.get('caption','')))]
            assert set(actual_figs) == expected_figs and len(actual_figs) == len(set(actual_figs)), ('figure coverage',key)
        if key.startswith('appendix-'):
            letter = key[-1].upper()
            expected = {n for p in inventory['pages'][unit['start']-1:unit['end']]
                        for n in p['equationCandidates'] if n.startswith(letter+'.')}
            if expected:
                end = max(int(n.split('.')[1]) for n in expected)
                expected.update(f'{letter}.{n}' for n in range(1,end+1))
            if manual:
                expected = set(manual['numberedEquations'])
            assert set(actual_numbers) == expected, ('appendix equation coverage',key,
                sorted(expected-set(actual_numbers)),sorted(set(actual_numbers)-expected))
            expected_figs = {n for p in inventory['pages'][unit['start']-1:unit['end']]
                             for n in p['figureCandidates'] if n.startswith(letter+'.')}
            if manual:
                expected_figs = set(manual['figures'])
            actual_figs = [m[1] for n in figures
                           if (m:=re.match(r'图\s*([A-E]\.\d+)',n.get('caption','')))]
            assert set(actual_figs) == expected_figs and len(actual_figs) == len(set(actual_figs)), ('appendix figure coverage',key)
        if key == 'chapter-01':
            assert len(figures) == 36 and len(formulas) == 152
            assert sum(n['kind']=='table' and re.match(r'表\s*1\.\d+', n.get('caption','')) is not None for n in blocks) == 3
            exercise_ids = re.findall(r'^\*\*(1\.\d+)（',source,re.M)
            assert exercise_ids == [f'1.{n}' for n in range(1,42)], ('exercise coverage',exercise_ids)
        results.append({'unit':key,'sourceNormalizedSha256':hashlib.sha256(source.encode('utf-8')).hexdigest(),
                        'sourceFileSha256':hashlib.sha256((BOOK/'translation'/f'{key}.md').read_bytes()).hexdigest(),
                        'rootBlocks':len(compiled['blocks']), 'blockKinds':dict(Counter(n['kind'] for n in blocks)),
                        'numberedEquations':len(formulas),'images':len(figures),
                        'mathFragments':sum('tex' in n for n in nodes),
                        'sourceMathRoundTrip':True,
                        'sourceInventoryBasis':str(manual_path.relative_to(BOOK)) if manual else 'PDF text candidates with independent page review',
                        'exercises':len(compiled_exercises) if key.startswith('chapter-') else None,
                        'status':'structural-checks-passed'})
    report_name = args.report_name or ('content-qa-'+'-'.join(args.units)+'.json')
    if not re.fullmatch(r'[a-z0-9-]+\.json', report_name):
        raise ValueError('Report name must be a simple JSON filename')
    output = BOOK/'reviews'/report_name
    output.write_text(json.dumps({'scope':'Structural checks only; no automatic semantic or editorial acceptance.','units':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False))


if __name__ == '__main__':
    main()
