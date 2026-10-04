"""Compile the page-checked MacKay chapter 36 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_36", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-36"
ASSETS = BOOK / "assets" / "chapter-36"
OUTPUT = BOOK / "chapter-36.draft.json"
PAGES = range(463, 469)
HEADING = re.compile(r"^(36\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-36/([\w.-]+\.png)$")
IMAGES = ["figure-36-1.png"]


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 36 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-36/{match.group(1)}"


def attach_table_captions(blocks: list[dict]) -> list[dict]:
    for number in (2, 3):
        matches = [index for index, block in enumerate(blocks)
                   if block["kind"] == "table" and block["pdfPage"] == 467
                   and len(block["rows"]) == 4 and not block.get("caption")]
        if not matches:
            raise ValueError(f"Table 36.{number} missing")
        index = matches[0]
        if index + 1 >= len(blocks):
            raise ValueError(f"Table 36.{number} caption missing")
        caption = blocks[index + 1]
        if caption["kind"] != "caption" or not caption["text"].startswith(f"表 36.{number}。"):
            raise ValueError(f"Table 36.{number} caption missing: {caption}")
        table = blocks[index]
        if [len(row) for row in table["rows"]] != [2, 3, 3, 3]:
            raise ValueError(f"Table 36.{number} rows malformed")
        table["rows"][0][1]["colspan"] = 2
        table["caption"] = caption["text"]
        table["captionSegments"] = caption["segments"]
        del blocks[index + 1]
    return blocks


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=463,
            chapter_number=36,
        )
    ]
    blocks = attach_table_captions(blocks)
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 36 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 36 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"36.{number}" for number in range(1, 4)]:
        raise ValueError(f"Chapter 36 sections missing or out of order: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(36.{number})" for number in range(1, 17)]:
        raise ValueError(f"Chapter 36 numbered formulas missing or out of order: {numbered}")
    if any(block["kind"] == "formula" and not block["number"] for block in blocks):
        raise ValueError("Source chapter 36 has no unnumbered display equations")
    exercises = [block for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"36\.\d+", block["label"]).group()
                        for block in exercises]
    if exercise_numbers != [f"36.{number}" for number in range(1, 10)]:
        raise ValueError(f"Chapter 36 exercises missing or out of order: {exercise_numbers}")
    recommended = [block["label"] for block in exercises if block.get("recommendedIcon")]
    if recommended != ["习题 36.2", "习题 36.3"]:
        raise ValueError(f"Chapter 36 rat-icon exercises missing: {recommended}")
    marked = [block["label"] for block in exercises if block["label"].startswith("▷")]
    if marked != [f"▷ 习题 36.{number}" for number in (1, 4, 5)]:
        raise ValueError(f"Chapter 36 triangle exercises missing: {marked}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if [Path(block["src"]).name for block in figures] != IMAGES:
        raise ValueError("Chapter 36 figure 36.1 missing")
    if not figures[0].get("caption", "").startswith("图 36.1。"):
        raise ValueError("Chapter 36 figure 36.1 caption missing")
    figures[0]["wide"] = True
    tables = [block for block in blocks if block["kind"] == "table"]
    if len(tables) != 2 or [block["pdfPage"] for block in tables] != [467, 467]:
        raise ValueError("Chapter 36 tables 36.2 and 36.3 missing")
    for number, table in zip((2, 3), tables):
        if not table.get("caption", "").startswith(f"表 36.{number}。"):
            raise ValueError(f"Table 36.{number} caption missing")
        if [len(row) for row in table["rows"]] != [2, 3, 3, 3]:
            raise ValueError(f"Table 36.{number} cell count wrong")
        if table["rows"][0][1].get("colspan") != 2:
            raise ValueError(f"Table 36.{number} two-column action heading missing")
    if any(block["kind"] in {"footnote", "code", "box", "list"} for block in blocks):
        raise ValueError("Source chapter 36 has no footnotes, code, boxes, or lists")
    toc = [{"number": "36", "title": "决策理论", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [463, 468],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbered)} numbered formulas, {len(figures)} figure, "
          f"{len(exercises)} exercises, {len(tables)} tables")


if __name__ == "__main__":
    main()
