"""Inventory the repository PDF; extraction is an aid, never a reviewed source."""
from pathlib import Path
import hashlib
import json
import re
import fitz

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
PDF = ROOT / 'Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf'
TMP = ROOT / 'tmp' / 'prml-source'
TITLES = ['绪论', '概率分布', '用于回归的线性模型', '用于分类的线性模型', '神经网络',
          '核方法', '稀疏核机器', '图模型', '混合模型与 EM', '近似推断', '采样方法',
          '连续潜变量', '序列数据', '模型组合']


def main():
    if (BOOK / 'TASKS.md').exists() or (BOOK / 'source-inventory.json').exists():
        raise SystemExit('Inventory already exists; refusing to overwrite reviewed progress')
    TMP.mkdir(parents=True, exist_ok=True)
    d = fitz.open(PDF)
    toc = [{'level': level, 'title': title.replace('\r', ' ').strip(), 'pdfPage': page}
           for level, title, page in d.get_toc()]
    tops = [t for t in toc if t['level'] == 1]
    units = []
    for i, t in enumerate(tops):
        start, end = t['pdfPage'], tops[i + 1]['pdfPage'] - 1 if i + 1 < len(tops) else len(d)
        match = re.match(r'^(\d+)\.', t['title'])
        appendix = re.match(r'Appendix ([A-E])', t['title'])
        if match:
            num = int(match[1]); key = f'chapter-{num:02d}'; zh = f'第 {num} 章 {TITLES[num-1]}'
        elif appendix:
            key = 'appendix-' + appendix[1].lower(); zh = {'A':'数据集','B':'概率分布','C':'矩阵的性质','D':'变分法','E':'拉格朗日乘子'}[appendix[1]]
            zh = f'附录 {appendix[1]} {zh}'
        else:
            key, zh = {'COVER': ('frontmatter', '封面与出版信息'), 'Preface': ('preface', '前言'),
                       'Mathematical notation': ('notation', '数学记号'), 'Contents': ('contents', '原书目录'),
                       'References': ('references', '参考文献'), 'Index': ('index', '索引')}[t['title']]
        units.append({'id': key, 'title': zh, 'originalTitle': t['title'], 'start': start, 'end': end,
                      'sections': [x for x in toc if x['level'] > 1 and start <= x['pdfPage'] <= end]})
    pages = []
    for page in d:
        n = page.number + 1
        raw = page.get_text('text', sort=False)
        (TMP / f'page-{n:03d}.txt').write_text(raw, encoding='utf-8')
        eq = sorted(set(re.findall(r'^\(([A-E]|\d+)\.(\d+)\)\s*$', raw, re.M)), key=lambda x: (x[0], int(x[1])))
        figs = sorted(set(re.findall(r'^Figure\s+([A-E]|\d+)\.(\d+)\b', raw, re.M)), key=lambda x: (x[0], int(x[1])))
        tables = sorted(set(re.findall(r'^Table\s+([A-E]|\d+)\.(\d+)\b', raw, re.M)), key=lambda x: (x[0], int(x[1])))
        pages.append({'pdfPage':n, 'printedPage': n-20 if n >= 21 else None, 'characters':len(raw),
                      'equationCandidates':['.'.join(x) for x in eq], 'figureCandidates':['.'.join(x) for x in figs],
                      'tableCandidates':['.'.join(x) for x in tables], 'verifiedAgainstPage':False})
    inventory = {'source':PDF.name, 'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(), 'pdfPages':len(d),
                 'note':'书签与提取文本仅用于任务定位；逐页视觉核对后才能确认完整性。', 'units':units, 'pages':pages}
    (BOOK / 'source-inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    tasks = ['# 《模式识别与机器学习》翻译与编撰任务', '',
             '唯一正文依据：仓库 `Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf`，共 758 个物理页。',
             '状态：未完成。原文提取、任务登记和自动检查均不等于译文或独立审查通过。', '',
             '## 工作约定', '',
             '- [x] 确认原书文件、页数、章节范围及现有译稿状态。',
             '- [x] 建立全书任务清单和原页映射。',
             '- [ ] 14 章与全部卷首、附录、书后材料完成逐页翻译。',
             '- [ ] 所有章节通过未参与初译的 Agent 独立审查并修复问题。',
             '- [ ] 全书一致性审查、桌面/窄屏/深色模式检查和站点接入。', '',
             '中文导读与正文分开。数学使用可复制的 TeX/MathML，图示采用原图裁切与完整中文图注、图内文字译注。',
             '初译按原书顺序推进；同章文件可分段由不同 Agent 负责。审查记录写入 `reviews/`，不得自审自验收。',
             '仅修改本书目录；公共文件由主 Agent 协调最小修改。不撤销、暂存或提交其他 Agent 的工作。', '',
             '## 分工与格式', '',
             '- 主 Agent：清单、卷首、构建与集成；可独立审查未参与初译的章节。',
             '- 协作 Agent：按明确指派的互不重叠章节分段写作；每次交接记录范围。',
             '- 审查 Agent：对照原页审查，问题与已验证范围写入审查记录。',
             '- 译稿：`translation/<unit>.md`；分段：`translation/parts/<unit>-<part>.md`。',
             '- 每个物理页以 `<!-- pdf-page: N -->` 定位，跨页续段以 `<!-- join-previous-paragraph -->` 连接。', '',
             '## 验收清单', '']
    for u in units:
        tasks += [f"### {u['title']}（PDF {u['start']}–{u['end']}）", '',
                  '- [ ] 逐页核对原文，保留全部段落、脚注、列表、习题与引用。']
        if u['id'].startswith(('chapter-', 'appendix-')):
            tasks += ['- [ ] 增加与原书正文明确分开的简短中文导读。', '- [ ] 翻译章首正文。']
        for s in u['sections']:
            tasks.append(f"{'  ' * (s['level'] - 2)}- [ ] {s['title']}（PDF {s['pdfPage']} 起）")
        for category, label in [('figureCandidates', '图'), ('tableCandidates', '表'), ('equationCandidates', '公式')]:
            vals = []
            for p in pages[u['start']-1:u['end']]:
                vals.extend(p[category])
            vals = list(dict.fromkeys(vals))
            if vals:
                tasks += [f"- [ ] {label}候选编号（须逐项对照原页确认）：" + '、'.join(vals) + '。']
            else:
                tasks += [f'- [ ] 核对本部分{label}，确认有无提取遗漏。']
        tasks += ['- [ ] 图内英文、图注、表格单元格与章首装饰图全部保留并翻译。',
                  '- [ ] 公式、上下标、编号、算法/代码逐一核对，MathML 编译通过。',
                  '- [ ] 排版、目录导航、窄屏和深色模式检查。',
                  '- [ ] 未参与本部分初译的 Agent 独立审查并记录问题。',
                  '- [ ] 修复全部问题后验收。', '']
    tasks += ['## 全书整体 review', '', '- [ ] 跨章术语、变量与符号一致。',
              '- [ ] 章节/图/表/公式/习题编号、引用与阅读跳转完整。',
              '- [ ] 全书目录、页码映射、导读风格与阅读进度一致。',
              '- [ ] 全部图片可加载，窄屏无页面横向溢出，深色模式可读。',
              '- [ ] 独立整体审查、修复与复查记录齐全。',
              '- [ ] 所有材料通过验收后更新公共索引中的完成状态。', '']
    target = BOOK / 'TASKS.md'
    if target.exists():
        raise SystemExit('TASKS.md already exists; refusing to overwrite progress')
    target.write_text('\n'.join(tasks), encoding='utf-8')
    print(json.dumps({'pages':len(d), 'units':len(units), 'tasks':str(target), 'sourceText':str(TMP)}))


if __name__ == '__main__':
    main()
