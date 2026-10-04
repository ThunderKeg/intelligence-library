"""Compile the visually checked MacKay chapter 40 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_40", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-40"
ASSETS = BOOK / "assets" / "chapter-40"
OUTPUT = BOOK / "chapter-40.draft.json"
PAGES = range(495, 504)
HEADING = re.compile(r"^(40\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-40/([\w.-]+\.png)$")
IMAGES = {
    "figure-40-1.png", "figure-40-2.png", "figure-40-3.png",
    "figure-40-4.png", "figure-40-5.png", "figure-40-7.png",
    "figure-40-9.png", "figure-40-10.png",
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 40 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-40/{match.group(1)}"


def group_chapter_title(block: dict) -> None:
    parts = ("第 40 章　", "单个神经元的容量")
    if block["text"] != "".join(parts):
        raise ValueError(f"Unexpected chapter title: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch40-title-part">{part}</span>' for part in parts
    ) + "</h1>"


def preserve_tables(blocks: list[dict]) -> list[dict]:
    for page, caption_prefix in ((499, "表 40.6"), (500, "表 40.8")):
        positions = [i for i, block in enumerate(blocks)
                     if block["kind"] == "table" and block["pdfPage"] == page]
        if len(positions) != 1:
            raise ValueError(f"Expected one table on PDF {page}: {positions}")
        index = positions[0]
        table = blocks[index]
        caption = blocks[index - 1]
        if caption["kind"] != "paragraph" or not caption["text"].startswith(caption_prefix):
            raise ValueError(f"Missing caption before {caption_prefix}")
        rows = table["rows"]
        if len(rows) != 8 or len(rows[0]) != 2 or any(len(row) != 9 for row in rows[1:]):
            raise ValueError(f"Malformed two-level table {caption_prefix}")
        if rows[0][0]["text"] or rows[0][1]["text"] != "K" or rows[1][0]["text"] != "N":
            raise ValueError(f"Missing K/N table header {caption_prefix}")
        rows[0][1]["colspan"] = 8
        table["caption"] = caption["text"]
        table["captionSegments"] = caption["segments"]
        del blocks[index - 1]
    return blocks


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=495,
            chapter_number=40,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 40 title is missing")
    group_chapter_title(blocks[0])
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 40 needs one marked editor introduction")
    BUILDER.compile_math(blocks)
    blocks = preserve_tables(blocks)
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"40.{number}" for number in range(1, 6)]:
        raise ValueError(f"Section order error: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(40.{number})" for number in range(1, 12)]:
        raise ValueError(f"Formula sequence error: {numbered}")
    if sum(block["kind"] == "figure" for block in blocks) != len(IMAGES):
        raise ValueError("One or more source graphics missing")
    if sum(block["kind"] == "table" for block in blocks) != 2:
        raise ValueError("Both source tables are required")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"40\.\d+", label).group() for label in exercises] != [
            f"40.{number}" for number in range(4, 10)]:
        raise ValueError(f"Exercise sequence error: {exercises}")
    if sum(block.get("recommendedIcon", "").endswith("exercise-rat.png")
           for block in blocks) != 3:
        raise ValueError("Three recommended exercise icons are required")
    toc = [{"number": "40", "title": "单个神经元的容量", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [495, 503],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
