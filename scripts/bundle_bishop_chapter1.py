"""Build the text-only reading edition from the directly translated Markdown."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = ROOT / "books" / "bishop-deep-learning-2024" / "translation"
OUTPUT = ROOT / "books" / "bishop-deep-learning-2024" / "chapter-01.json"

TOC = [
    ("1", "深度学习革命"),
    ("1.1", "深度学习的影响"),
    ("1.1.1", "医学诊断"),
    ("1.1.2", "蛋白质结构"),
    ("1.1.3", "图像合成"),
    ("1.1.4", "大语言模型"),
    ("1.2", "一个教程示例"),
    ("1.2.1", "合成数据"),
    ("1.2.2", "线性模型"),
    ("1.2.3", "误差函数"),
    ("1.2.4", "模型复杂度"),
    ("1.2.5", "正则化"),
    ("1.2.6", "模型选择"),
    ("1.3", "机器学习简史"),
    ("1.3.1", "单层网络"),
    ("1.3.2", "反向传播"),
    ("1.3.3", "深层网络"),
]


def parse_translation(number: int) -> list[dict[str, str]]:
    path = TRANSLATION / f"page-{number:02d}.md"
    if not path.exists():
        raise SystemExit(f"Missing translation: {path}")
    paragraphs = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    blocks = []
    for index, paragraph in enumerate(paragraphs, 1):
        if paragraph.startswith("#"):
            kind, body = "heading", paragraph.lstrip("# ")
        elif paragraph.startswith(("图 1.", "表 1.")):
            kind, body = "caption", paragraph
        elif paragraph.startswith("式 (1."):
            kind, body = "formula", paragraph
        elif paragraph.startswith("|"):
            kind, body = "table", paragraph
        else:
            kind, body = "paragraph", paragraph
        blocks.append({"id": f"p{number:02d}-t{index:02d}", "kind": kind, "text": body})
    if not blocks:
        raise SystemExit(f"Empty translation: {path}")
    return blocks


source_pages = {number: parse_translation(number) for number in range(1, 23)}
blocks = []
for number in range(1, 23):
    if number == 6:
        # The printed page puts the example poem after the next section begins.
        # Place it with the language-model discussion in the continuous edition.
        order = source_pages[6][1:3] + source_pages[7] + source_pages[6][3:] + source_pages[6][:1]
    elif number == 7:
        continue
    else:
        order = source_pages[number]
    blocks.extend({**block, "page": int(block["id"][1:3])} for block in order)

headings = [block for block in blocks if block["kind"] == "heading"]
toc = []
for number, title in TOC:
    prefix = "第 1 章 " if number == "1" else number + " "
    match = next((block for block in headings if block["text"].startswith(prefix)), None)
    if match is None:
        raise SystemExit(f"Missing heading for {number} {title}")
    toc.append({"number": number, "title": title, "block": match["id"]})

chapter = {
    "bookId": "bishop-deep-learning-2024",
    "title": "第 1 章 深度学习革命",
    "toc": toc,
    "blocks": blocks,
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {OUTPUT}: {len(source_pages)} source sections, {len(blocks)} text blocks")
