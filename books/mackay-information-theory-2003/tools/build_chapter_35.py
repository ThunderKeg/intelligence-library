"""Compile the page-checked MacKay chapter 35 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_35", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-35"
ASSETS = BOOK / "assets" / "chapter-35"
OUTPUT = BOOK / "chapter-35.draft.json"
PAGES = range(457, 463)
HEADING = re.compile(r"^(35\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-35/([\w.-]+\.png)$")
IMAGES = [
    "figure-35-1.png",
    "leading-digit-intervals.png",
    "exercise-35-8-data.png",
    "figure-35-2.png",
    "figure-35-3.png",
]


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 35 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-35/{match.group(1)}"


def group_chapter_title(block: dict) -> None:
    parts = ("第 35 章　", "若干推断专题")
    if block["text"] != "".join(parts):
        raise ValueError(f"Chapter 35 title changed unexpectedly: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch35-title-part">{part}</span>' for part in parts
    ) + "</h1>"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=457,
            chapter_number=35,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 35 title is missing")
    group_chapter_title(blocks[0])
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 35 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"35.{number}" for number in range(1, 6)]:
        raise ValueError(f"Chapter 35 sections missing or out of order: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(35.{number})" for number in range(1, 16)]:
        raise ValueError(f"Chapter 35 numbered formulas missing or out of order: {numbered}")
    unnumbered = [block for block in blocks
                  if block["kind"] == "formula" and not block["number"]]
    if [block["pdfPage"] for block in unnumbered] != [457, 457, 457, 460, 461]:
        raise ValueError("Chapter 35's five unnumbered display equations are missing")
    exercises = [block for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"35\.\d+", block["label"]).group()
                        for block in exercises]
    if exercise_numbers != [f"35.{number}" for number in range(2, 9)]:
        raise ValueError(f"Chapter 35 exercises missing or out of order: {exercise_numbers}")
    recommended = [block["label"] for block in exercises if block.get("recommendedIcon")]
    if recommended != ["习题 35.5"]:
        raise ValueError(f"Chapter 35 rat-icon exercise missing: {recommended}")
    marked = [block["label"] for block in exercises if block["label"].startswith("▷")]
    if marked != [f"▷ 习题 35.{number}" for number in (2, 3, 7, 8)]:
        raise ValueError(f"Chapter 35 triangle exercise markers missing: {marked}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    names = [Path(block["src"]).name for block in figures]
    if names != IMAGES:
        raise ValueError(f"Chapter 35 figures missing or out of order: {names}")
    for block in figures:
        if block["width"] >= 700:
            block["wide"] = True
    for number in (1, 2, 3):
        figure = next(block for block in figures if block["src"].endswith(f"figure-35-{number}.png"))
        if not figure.get("caption", "").lstrip("* ").startswith(f"图 35.{number}。"):
            raise ValueError(f"Figure 35.{number} caption missing")
    tables = [block for block in blocks if block["kind"] == "table"]
    if len(tables) != 1 or tables[0]["pdfPage"] != 460 or len(tables[0]["rows"]) != 8:
        raise ValueError("Exercise 35.7's 8-row data table is missing")
    if any(len(row) != 6 for row in tables[0]["rows"]):
        raise ValueError("Exercise 35.7 data table has a missing column")
    if sum(bool(cell["text"]) for row in tables[0]["rows"] for cell in row) != 43:
        raise ValueError("Exercise 35.7 data table should contain 43 strings")
    if any(cell["header"] for row in tables[0]["rows"] for cell in row):
        raise ValueError("Exercise 35.7 source table has no headers")
    tables[0]["codeTable"] = True
    footnotes = [block for block in blocks if block["kind"] == "footnote"]
    if [block["label"] for block in footnotes] != ["1"]:
        raise ValueError("Chapter 35 Octave source footnote missing")
    if any(block["kind"] in {"list", "code", "box"} for block in blocks):
        raise ValueError("Source chapter 35 has no lists, code, or separate boxes")
    toc = [{"number": "35", "title": "若干推断专题", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [457, 462],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbered)} numbered + {len(unnumbered)} unnumbered formulas, "
          f"{len(figures)} images, {len(exercises)} exercises, 1 table, "
          f"{len(footnotes)} footnote")


if __name__ == "__main__":
    main()
