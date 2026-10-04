"""Compile the page-checked MacKay chapter 25 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_25", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-25"
ASSETS = BOOK / "assets" / "chapter-25"
OUTPUT = BOOK / "chapter-25.draft.json"
PAGES = range(336, 346)
HEADING = re.compile(r"^(25\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-25/([\w.-]+\.png)$")
IMAGES = {
    "figure-25-1.png", "figure-25-2.png", "figure-25-3.png",
    "figure-25-6.png", "figure-25-7.png", "table-25-8.png",
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 25 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-25/{match.group(1)}"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=336, chapter_number=25,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 25 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 25 needs one clearly marked editor introduction")
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"25.{i}" for i in range(1, 6)]:
        raise ValueError(f"Chapter 25 sections missing or out of order: {section_numbers}")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if numbers != [f"(25.{i})" for i in range(1, 21)]:
        raise ValueError(f"Chapter 25 formulas missing or out of order: {numbers}")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"25\.\d+", label).group() for label in exercises]
    if exercise_numbers != ["25.1", "25.2", "25.4", "25.5", "25.6", "25.7", "25.8", "25.9"]:
        raise ValueError(f"Chapter 25 exercises missing or out of order: {exercises}")
    images = [block for block in blocks if block["kind"] == "figure"]
    if {Path(block["src"]).name for block in images} != IMAGES or len(images) != len(IMAGES):
        raise ValueError(f"Unexpected chapter 25 image set: {[block['src'] for block in images]}")
    for block in images:
        if block["width"] >= 800:
            block["wide"] = True
    tables = [block for block in blocks if block["kind"] == "table"]
    if len(tables) != 4 or sorted(len(table["rows"]) for table in tables) != [3, 4, 8, 17]:
        raise ValueError(f"Unexpected chapter 25 table shapes: {[len(table['rows']) for table in tables]}")
    # The seven-bit codewords in table 25.5 must stay on one line in narrow viewports.
    codeword_table = next(table for table in tables if table["id"] == "p343-b005")
    codeword_table["codeTable"] = True
    # Example 25.3 has two numbered items separated by their own paragraphs.
    lists = [block for block in blocks if block["kind"] == "list"]
    if len(lists) != 2 or any(block["pdfPage"] != 340 or not block["ordered"] or
                              len(block["items"]) != 1 for block in lists):
        raise ValueError(f"Unexpected example 25.3 list structure: {lists}")
    for number, block in enumerate(lists, 1):
        block["start"] = number
    toc = [{"number": "25", "title": "格形图中的精确边缘化", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [336, 345],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbers)} numbered formulas, {len(images)} source images, "
          f"{len(exercises)} exercises, {len(tables)} tables")


if __name__ == "__main__":
    main()
