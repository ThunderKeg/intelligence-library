"""Bundle the manually translated Markdown pages and PDF text into Chapter 1."""

import hashlib
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = ROOT / "books" / "bishop-deep-learning-2024" / "translation"
OUTPUT = ROOT / "books" / "bishop-deep-learning-2024" / "chapter-01.json"
PDF = ROOT / "Christopher M. Bishop, Hugh Bishop - Deep Learning_ Foundations and Concepts-Springer (2024).pdf"

TOC = [
    ("1", "深度学习革命", 1),
    ("1.1", "深度学习的影响", 2),
    ("1.1.1", "医学诊断", 2),
    ("1.1.2", "蛋白质结构", 3),
    ("1.1.3", "图像合成", 4),
    ("1.1.4", "大语言模型", 5),
    ("1.2", "一个教程示例", 6),
    ("1.2.1", "合成数据", 6),
    ("1.2.2", "线性模型", 8),
    ("1.2.3", "误差函数", 8),
    ("1.2.4", "模型复杂度", 9),
    ("1.2.5", "正则化", 12),
    ("1.2.6", "模型选择", 14),
    ("1.3", "机器学习简史", 16),
    ("1.3.1", "单层网络", 17),
    ("1.3.2", "反向传播", 18),
    ("1.3.3", "深层网络", 20),
]

def parse_translation(number: int) -> list[dict[str, str]]:
    path = TRANSLATION / f"page-{number:02d}.md"
    if not path.exists():
        raise SystemExit(f"Missing direct translation: {path}")
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
        blocks.append({"id": f"p{number:02d}-t{index:02d}", "kind": kind, "zh": body})
    if not blocks:
        raise SystemExit(f"Empty translation: {path}")
    return blocks


pages = []
with fitz.open(PDF) as document:
    for number in range(1, 23):
        pdf_page = number + 20
        image = ROOT / "books" / "bishop-deep-learning-2024" / "pages" / f"page-{number:02d}.webp"
        if not image.exists():
            raise SystemExit(f"Missing rendered source page: {image}")
        pages.append({
            "id": f"ch01-p{number:02d}",
            "number": number,
            "pdfPage": pdf_page,
            "image": image.relative_to(ROOT).as_posix(),
            "sourceText": document[pdf_page - 1].get_text(sort=True),
            "blocks": parse_translation(number),
        })

source_hash = hashlib.sha256(PDF.read_bytes()).hexdigest() if PDF.exists() else None
chapter = {
    "bookId": "bishop-deep-learning-2024",
    "title": "第 1 章 · 深度学习革命",
    "originalTitle": "The Deep Learning Revolution",
    "source": {
        "title": "Deep Learning: Foundations and Concepts",
        "authors": "Christopher M. Bishop and Hugh Bishop",
        "publisher": "Springer",
        "year": 2024,
        "isbn": "978-3-031-45468-4",
        "pdfPageRange": [21, 42],
        "sha256": source_hash,
    },
    "toc": [{"number": number, "title": title, "page": page} for number, title, page in TOC],
    "pages": pages,
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {OUTPUT}: {len(pages)} pages, {sum(len(page['blocks']) for page in pages)} blocks")
