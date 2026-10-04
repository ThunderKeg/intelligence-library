"""Compile the visually checked MacKay chapter 45 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_45", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-45"
ASSETS = BOOK / "assets" / "chapter-45"
OUTPUT = BOOK / "chapter-45.draft.json"
PAGES = range(547, 561)
HEADING = re.compile(r"^(45\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-45/(figure-45-[12]\.png)$")
IMAGES = {"figure-45-1.png", "figure-45-2.png"}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 45 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-45/{match.group(1)}"


def preserve_method_numbering(blocks: list[dict]) -> None:
    """The displayed equation between two list items must not restart numbering."""
    methods = [block for block in blocks if block["pdfPage"] == 558
               and block["kind"] == "list"]
    if len(methods) != 2 or any(not block["ordered"] or len(block["items"]) != 1
                                 for block in methods):
        raise ValueError("Expected two numbered approaches on PDF 558")
    methods[1]["start"] = 2


def preserve_section_terms(blocks: list[dict]) -> None:
    """Keep the original heading text and mark intact terms for narrow screens."""
    sections = {
        "p548-b004": ("45.1　非线性回归的", ("标准方法", True)),
        "p552-b001": ("45.2　从参数模型到", ("高斯过程", True)),
        "p554-b004": ("45.3　利用给定的", ("高斯过程模型", True), "进行回归"),
        "p557-b010": ("45.5　", ("高斯过程模型", True), "的", ("自适应调整", True)),
    }
    found = set()
    for block in blocks:
        if block["id"] not in sections:
            continue
        if block["kind"] != "heading" or block["level"] != 2:
            raise ValueError(f"Unexpected section block: {block['id']}")
        parts = sections[block["id"]]
        if block["text"] != "".join(part[0] if isinstance(part, tuple) else part
                                     for part in parts):
            raise ValueError(f"Section heading text changed: {block['id']}")
        block["html"] = "<h2>" + "".join(
            f'<span class="ch45-term">{part[0]}</span>' if isinstance(part, tuple)
            else part for part in parts
        ) + "</h2>"
        found.add(block["id"])
    if found != set(sections):
        raise ValueError(f"Missing chapter 45 section headings: {set(sections) - found}")


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=547,
            chapter_number=45,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 45 title is missing")
    if blocks[0]["text"] != "第 45 章　高斯过程":
        raise ValueError(f"Unexpected chapter title: {blocks[0]['text']}")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 45 needs one marked editor introduction")
    BUILDER.compile_math(blocks)
    preserve_method_numbering(blocks)
    preserve_section_terms(blocks)
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"45.{number}" for number in range(1, 8)]:
        raise ValueError(f"Section order error: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(45.{number})" for number in range(1, 57)]:
        raise ValueError(f"Formula sequence error: {numbered}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if len(figures) != len(IMAGES) or {Path(block["src"]).name for block in figures} != IMAGES:
        raise ValueError("One or more source graphics missing")
    if any(block["kind"] == "exercise" for block in blocks):
        raise ValueError("The chapter 45 exercise belongs on its independent prelude")
    toc = [{"number": "45", "title": "高斯过程", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [547, 560],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
