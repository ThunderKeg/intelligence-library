"""Compile the page-checked MacKay chapter 28 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_28", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-28"
ASSETS = BOOK / "assets" / "chapter-28"
OUTPUT = BOOK / "chapter-28.draft.json"
PAGES = range(355, 368)
HEADING = re.compile(r"^(28\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-28/([\w.-]+\.png)$")
IMAGES = {f"figure-28-{number}.png" for number in range(1, 10)} | {
    "exercise-28-1-distributions.png", "exercise-28-2-line.png",
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 28 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-28/{match.group(1)}"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=355, chapter_number=28,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 28 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 28 needs one clearly marked editor introduction")
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"28.{number}" for number in range(1, 5)]:
        raise ValueError(f"Chapter 28 sections missing or out of order: {section_numbers}")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if numbers != [f"(28.{number})" for number in range(1, 23)]:
        raise ValueError(f"Chapter 28 formulas missing or out of order: {numbers}")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"28\.\d+", label).group() for label in exercises]
    if exercise_numbers != [f"28.{number}" for number in range(1, 5)]:
        raise ValueError(f"Chapter 28 exercises missing or out of order: {exercises}")
    images = [block for block in blocks if block["kind"] == "figure"]
    if {Path(block["src"]).name for block in images} != IMAGES or len(images) != len(IMAGES):
        raise ValueError(f"Unexpected chapter 28 image set: {[block['src'] for block in images]}")
    for block in images:
        if block["width"] >= 800 and Path(block["src"]).name != "figure-28-1.png":
            block["wide"] = True
    tables = [block for block in blocks if block["kind"] == "table"]
    if len(tables) != 1 or len(tables[0]["rows"]) != 5 or any(len(row) != 4 for row in tables[0]["rows"]):
        raise ValueError(f"Unexpected chapter 28 table shape: {[len(table['rows']) for table in tables]}")
    lists = [block for block in blocks if block["kind"] == "list"]
    if len(lists) != 2 or [block["pdfPage"] for block in lists] != [359, 360] or not all(
        block["ordered"] and len(block["items"]) == 1 for block in lists
    ):
        raise ValueError(f"Unexpected chapter 28 two-part inference list: {lists}")
    for number, block in enumerate(lists, 1):
        block["start"] = number
    toc = [{"number": "28", "title": "模型比较与奥卡姆剃刀", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [355, 367],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbers)} numbered formulas, {len(images)} source images, "
          f"{len(exercises)} exercises, {len(tables)} table")


if __name__ == "__main__":
    main()
