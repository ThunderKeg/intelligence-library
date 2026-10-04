"""Compile the page-checked MacKay chapter 21 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_21", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-21"
ASSETS = BOOK / "assets" / "chapter-21"
OUTPUT = BOOK / "chapter-21.draft.json"
PAGES = range(305, 312)
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-21/(figure-21-[1-7]\.png)$")
HEADING = re.compile(r"^(21\.\d+)\s+(.+)$")
FIGURES = {f"figure-21-{number}.png" for number in range(1, 8)}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected chapter 21 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-21/{match.group(1)}"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=305, chapter_number=21,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 21 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 21 needs one clearly marked editor introduction")
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    if [HEADING.match(block["text"]).group(1) for block in sections] != ["21.1", "21.2"]:
        raise ValueError(f"Chapter 21 sections missing or out of order: {sections}")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if numbers != [f"(21.{number})" for number in range(1, 10)]:
        raise ValueError(f"Chapter 21 formulas missing or out of order: {numbers}")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"21\.\d+", label).group() for label in exercises] != ["21.2", "21.3"]:
        raise ValueError(f"Chapter 21 exercises missing or out of order: {exercises}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if {Path(block["src"]).name for block in figures} != FIGURES or len(figures) != len(FIGURES):
        raise ValueError(f"Unexpected chapter 21 figures: {[block['src'] for block in figures]}")
    for block in figures:
        if Path(block["src"]).name != "figure-21-3.png" and block["width"] >= 560:
            block["wide"] = True

    # The three items in the burglar-alarm example straddle displays and pages.
    # Preserve their source numbering in the three separate list blocks.
    lists = [block for block in blocks if block["kind"] == "list"]
    if len(lists) != 3 or [block["pdfPage"] for block in lists] != [305, 305, 306]:
        raise ValueError(f"Unexpected burglar-alarm list structure: {lists}")
    for number, block in enumerate(lists, 1):
        if not block["ordered"] or len(block["items"]) != 1:
            raise ValueError(f"Unexpected list item {number}: {block}")
        block["start"] = number

    toc = [{"number": "21", "title": "通过完全枚举进行精确推断", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [305, 311],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbers)} numbered formulas, {len(figures)} source figures, "
          f"{len(exercises)} exercises")


if __name__ == "__main__":
    main()
