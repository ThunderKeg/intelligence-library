"""Record the integrator's explicit acceptance after reading an independent review.

This command does not perform or infer translation review. It binds a supplied
review decision to the current source, compiled content and image files.
"""
import argparse
import json
from pathlib import Path
from build import BOOK, review_fingerprint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('units',nargs='+')
    parser.add_argument('--review',required=True,help='Independent review record, relative to the book directory')
    parser.add_argument('--reviewer',default='prml_reviewer',help='Agent that did not translate this unit')
    args = parser.parse_args()
    record = Path(args.review)
    if record.is_absolute() or '..' in record.parts or not (BOOK/record).is_file():
        raise SystemExit('Review must be an existing file within the book directory')
    inventory_path = BOOK/'source-inventory.json'
    inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
    compiled_units = []
    for key in args.units:
        unit = next(u for u in inventory['units'] if u['id'] == key)
        source = BOOK/'translation'/f'{key}.md'
        compiled_path = BOOK/f'{key}.json'
        compiled = json.loads(compiled_path.read_text(encoding='utf-8'))
        unit['review'] = {'status':'accepted','reviewer':args.reviewer,'record':record.as_posix(),
                          **review_fingerprint(compiled,source)}
        for page in inventory['pages'][unit['start']-1:unit['end']]:
            page['verifiedAgainstPage'] = True
            page['reviewRecord'] = record.as_posix()
        compiled['editorialStatus'] = 'reviewed'
        compiled['reviewRecord'] = record.as_posix()
        compiled_units.append((compiled_path,compiled))
    inventory_path.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for target,compiled in compiled_units:
        target.write_text(json.dumps(compiled,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('Recorded independent acceptance: '+', '.join(args.units))


if __name__ == '__main__':
    main()
