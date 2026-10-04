"""Compile the visually checked MacKay chapter 41 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_41", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-41"
ASSETS = BOOK / "assets" / "chapter-41"
OUTPUT = BOOK / "chapter-41.draft.json"
PAGES = range(504, 516)
HEADING = re.compile(r"^(41\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-41/([\w.-]+\.png)$")
IMAGES = {f"figure-41-{n}.png" for n in (1, 2, 3, 5, 6, 7, 9, 10, 11)}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 41 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-41/{match.group(1)}"


def preserve_title(block: dict) -> None:
    parts = ("第 41 章　", "将学习视为推断")
    if block["text"] != "".join(parts):
        raise ValueError(f"Unexpected chapter title: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch41-title-part" style="white-space:nowrap">{part}</span>'
        for part in parts
    ) + "</h1>"


def outline_algorithms(blocks: list[dict]) -> list[dict]:
    """Keep the book's two full-border algorithm frames and copyable code."""
    for page, number in ((509, "41.4"), (512, "41.8")):
        positions = [i for i, b in enumerate(blocks)
                     if b["pdfPage"] == page and b["kind"] == "code"]
        if len(positions) != 1:
            raise ValueError(f"Expected one algorithm code block on PDF {page}: {positions}")
        index = positions[0]
        caption = blocks[index + 1]
        if caption["kind"] != "paragraph" or not caption["text"].startswith(f"算法 {number}"):
            raise ValueError(f"Missing algorithm {number} caption")
        blocks[index] = {
            "id": f"box-41-algorithm-{number.replace('.', '-')}",
            "kind": "box", "pdfPage": page, "page": page - 504 + 1,
            "outlined": True, "algorithm": True, "blocks": [blocks[index]],
        }
    return blocks


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=504,
            chapter_number=41,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 41 title is missing")
    preserve_title(blocks[0])
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 41 needs one marked editor introduction")
    BUILDER.compile_math(blocks)
    blocks = outline_algorithms(blocks)
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"41.{n}" for n in range(1, 6)]:
        raise ValueError(f"Section order error: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(41.{n})" for n in range(1, 31)]:
        raise ValueError(f"Formula sequence error: {numbered}")
    if sum(block["kind"] == "figure" for block in blocks) != len(IMAGES):
        raise ValueError("One or more source graphics missing")
    if sum(block["kind"] == "box" and block.get("algorithm") for block in blocks) != 2:
        raise ValueError("Both outlined algorithm frames are required")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"41\.\d+", label).group() for label in exercises] != [
            "41.1", "41.2", "41.3"]:
        raise ValueError(f"Exercise sequence error: {exercises}")
    if sum(block.get("recommendedIcon", "").endswith("exercise-rat.png")
           for block in blocks) != 1:
        raise ValueError("Exercise 41.1 recommended icon is required")
    toc = [{"number": "41", "title": "将学习视为推断", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [504, 515],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
