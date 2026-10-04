"""Compile visually checked MacKay Appendix C as an unpublished reader draft."""

import importlib.util
import json
import re
from html import escape
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_appendix_c_builder", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "appendix-C"
ASSETS = BOOK / "assets" / "appendix-C"
OUTPUT = BOOK / "chapter-C.draft.json"
PAGES = range(617, 625)
TITLE = "附录 C　一些数学知识"
IMAGE_NAME = "table-C-4-numbers.png"
SECTION_TITLES = [
    "C.1　有限域理论",
    "C.2　特征向量与特征值",
    "C.3　微扰理论",
    "C.4　若干数值",
]
ITALIC_SUBHEADINGS = {
    "大多数线性码用伽罗瓦理论的语言表述",
    "对称矩阵", "一般方阵", "非负矩阵", "转移概率矩阵",
    "二阶微扰理论", "小结",
}
CAPTION_PAIRS = (
    ("p617-b012", "p617-b013", "表 C.1"),
    ("p617-b016-mult", "p617-b017", "表 C.2"),
    ("p617-b018", "p617-b019", "表 C.3"),
    ("p620-b001", "p620-b002", "表 C.4"),
    ("p620-b003", "p620-b004", "表 C.5"),
    ("p621-b001", "p621-b002", "表 C.6"),
)


def image_path(source: str) -> str:
    if source != f"../../assets/appendix-C/{IMAGE_NAME}":
        raise ValueError(f"Unexpected Appendix C image path: {source}")
    if not (ASSETS / IMAGE_NAME).is_file():
        raise FileNotFoundError(ASSETS / IMAGE_NAME)
    return f"assets/appendix-C/{IMAGE_NAME}"


def split_gf4_tables(blocks: list[dict]) -> None:
    """The source has two stacked 5×5 operation tables under one caption."""
    index = next(i for i, block in enumerate(blocks) if block["id"] == "p617-b016")
    combined = blocks[index]
    if combined["kind"] != "table" or len(combined["rows"]) != 10 or any(
        len(row) != 5 for row in combined["rows"]
    ):
        raise ValueError("GF(4) addition/multiplication table changed")
    multiplication = {**combined, "id": "p617-b016-mult", "rows": combined["rows"][5:]}
    for cell in multiplication["rows"][0]:
        cell["header"] = True
    combined["rows"] = combined["rows"][:5]
    blocks.insert(index + 1, multiplication)


def attach_captions(blocks: list[dict]) -> None:
    for table_id, caption_id, label in CAPTION_PAIRS:
        index = next((i for i, block in enumerate(blocks) if block["id"] == table_id), -1)
        if index < 0 or index + 1 >= len(blocks) or blocks[index + 1]["id"] != caption_id:
            raise ValueError(f"Table and caption became separated: {table_id}")
        table, caption = blocks[index], blocks[index + 1]
        if table["kind"] != "table" or caption["kind"] != "paragraph" or not caption["text"].startswith(label):
            raise ValueError(f"Unexpected caption structure: {caption_id}")
        table["caption"] = caption["text"]
        table["captionSegments"] = caption["segments"]
        blocks.pop(index + 1)


def preserve_headings(blocks: list[dict]) -> None:
    first = blocks[0]
    if first["kind"] != "heading" or first["level"] != 1 or first["text"] != TITLE:
        raise ValueError("Appendix C title changed")
    first["html"] = (
        '<h1 style="text-align:center">'
        '<span style="display:block;border-bottom:3px solid currentColor;'
        'padding-bottom:.45em;margin-bottom:.45em">附录 C</span>'
        '<span style="display:block;font-style:italic;white-space:nowrap">'
        '一些数学知识</span></h1>'
    )
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    if [block["text"] for block in sections] != SECTION_TITLES:
        raise ValueError("Appendix C section heading sequence changed")
    for block in sections:
        number, label = block["text"].split("　", 1)
        block["html"] = (
            '<h2><span aria-hidden="true">▶</span> '
            f'<span style="white-space:nowrap">{escape(number)}</span>　'
            f'<span style="white-space:nowrap">{escape(label)}</span></h2>'
        )
    subheadings = [block for block in blocks if block["kind"] == "heading" and block["level"] == 3]
    if {block["text"] for block in subheadings} != ITALIC_SUBHEADINGS or len(subheadings) != 7:
        raise ValueError("Appendix C italic subheadings changed")
    for block in subheadings:
        block["html"] = (
            '<h3 style="font-style:italic;font-weight:normal">'
            f'{escape(block["text"])}</h3>'
        )


def main() -> None:
    if {path.name for path in ASSETS.glob("*.png")} != {IMAGE_NAME}:
        raise ValueError("Appendix C asset set changed")
    blocks = [
        block for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=617, chapter_number=0,
        )
    ]
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Appendix C needs exactly one marked editor introduction")
    split_gf4_tables(blocks)
    # PDF624 has no header row. Drop the empty Markdown row used only to define columns.
    number_table = next(block for block in blocks if block["id"] == "p624-b003")
    if number_table["kind"] != "table" or len(number_table["rows"]) != 44 or any(
        cell["text"] for cell in number_table["rows"][0]
    ):
        raise ValueError("PDF624 no-header numeric table changed")
    number_table["rows"] = number_table["rows"][1:]
    BUILDER.compile_math(blocks)
    attach_captions(blocks)
    preserve_headings(blocks)
    formulas = [block for block in blocks if block["kind"] == "formula"]
    numbered = [block["number"] for block in formulas if block["number"]]
    if numbered != [f"(C.{n})" for n in range(1, 38)] or len(formulas) != 37:
        raise ValueError(f"Appendix C formula sequence changed: {numbered}")
    tables = [block for block in blocks if block["kind"] == "table"]
    if len(tables) != 10 or sum(bool(block.get("caption")) for block in tables) != 6:
        raise ValueError("Appendix C table count or captions changed")
    expected_table_rows = {
        "p617-b012": 3, "p617-b016": 5, "p617-b016-mult": 5,
        "p617-b018": 5, "p618-b002": 9, "p618-b003": 9,
        "p620-b001": 10, "p620-b003": 6, "p621-b001": 13,
        "p624-b003": 43,
    }
    if {block["id"]: len(block["rows"]) for block in tables} != expected_table_rows:
        raise ValueError("Appendix C table row structure changed")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if len(figures) != 1 or figures[0]["src"] != f"assets/appendix-C/{IMAGE_NAME}":
        raise ValueError("Appendix C numeric-table crop changed")
    figures[0]["wide"] = True
    if any(block["kind"] in {"exercise", "code", "footnote", "quote", "box"} for block in blocks):
        raise ValueError("Unexpected exercise, code, footnote, quote or box")
    if [block["pdfPage"] for block in blocks] != sorted(block["pdfPage"] for block in blocks):
        raise ValueError("Appendix C page order changed")
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": TITLE,
        "sourcePdfPages": [617, 624],
        "toc": [
            {"number": "C", "title": "一些数学知识", "block": "p617-b001"},
            *(
                {"number": text.split("　", 1)[0], "title": text.split("　", 1)[1], "block": block_id}
                for text, block_id in zip(SECTION_TITLES, ("p617-b003", "p618-b005", "p620-b011", "p624-b001"))
            ),
        ],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(
        f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(formulas)} numbered formulas, "
        f"{len(tables)} copyable tables, {len(figures)} original-layout asset"
    )


if __name__ == "__main__":
    main()
