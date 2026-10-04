"""Record and constrain the compiled changes from the final terminology pass."""
import json
from pathlib import Path
import re
from bs4 import BeautifulSoup
from build import review_fingerprint

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
BEFORE = ROOT/'tmp/prml-global-review/before'


def protected_nodes(value):
    if isinstance(value, dict):
        if 'mathml' in value or value.get('kind')=='code' or value.get('code') is True:
            yield value
        for child in value.values():
            yield from protected_nodes(child)
    elif isinstance(value,list):
        for child in value:
            yield from protected_nodes(child)


def differences(a, b, path=''):
    assert type(a) is type(b), (path, type(a), type(b))
    if isinstance(a, dict):
        assert a.keys()==b.keys(), (path,a.keys(),b.keys())
        for key in a:
            yield from differences(a[key],b[key],path+'/'+key)
    elif isinstance(a,list):
        assert len(a)==len(b), (path,len(a),len(b))
        for i,(x,y) in enumerate(zip(a,b)):
            yield from differences(x,y,path+'/'+str(i))
    elif a!=b:
        yield {'path':path,'before':a,'after':b}


def main():
    inventory=json.loads((BEFORE/'source-inventory.json').read_text(encoding='utf8'))
    results=[]
    for name in ('chapter-04','chapter-05','chapter-06','chapter-08','chapter-12','chapter-13','references'):
        old=json.loads((BEFORE/(name+'.json')).read_text(encoding='utf8'))
        new=json.loads((BOOK/(name+'.json')).read_text(encoding='utf8'))
        for data in (old,new):
            data.pop('editorialStatus',None);data.pop('reviewRecord',None)
        assert list(protected_nodes(old))==list(protected_nodes(new)), ('math or code changed',name)
        diffs=list(differences(old,new))
        for row in diffs:
            assert (row['path'].split('/')[-1] in {'text','title','alt','caption','html'}
                    or re.search(r'/(?:segments|captionSegments)/\d+$',row['path'])), row
            if row['path'].endswith('/html'):
                assert name=='references', row
                before=BeautifulSoup(row['before'],'html.parser')
                after=BeautifulSoup(row['after'],'html.parser')
                assert re.sub(r'〔[^〕]+〕','',str(before))==re.sub(r'〔[^〕]+〕','',str(after)), row
                assert re.findall(r'〔[^〕]+〕',str(before))==re.findall(r'〔[^〕]+〕',str(after)), row
                assert [str(x) for x in before.select('em,strong')]==[str(x) for x in after.select('em,strong')], row
        old_review=next(x for x in inventory['units'] if x['id']==name)['review']
        fingerprint=review_fingerprint(new,BOOK/'translation'/f'{name}.md')
        assert fingerprint['imagesSha256']==old_review['imagesSha256'], name
        results.append({'unit':name,'changedFields':len(diffs),'changes':diffs,**fingerprint})
    report={'scope':'Structural, math, image and bibliographic-field invariance only; semantic review remains independent.',
            'passed':True,'units':results}
    (BOOK/'reviews/global-delta-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'passed':True,'units':{x['unit']:x['changedFields'] for x in results}}))


if __name__=='__main__':
    main()
