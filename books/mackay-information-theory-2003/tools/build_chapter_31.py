"""Compile the page-checked MacKay chapter 31 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_31", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-31"
ASSETS = BOOK / "assets" / "chapter-31"
OUTPUT = BOOK / "chapter-31.draft.json"
PAGES = range(412, 425)
HEADING = re.compile(r"^(31\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-31/(figure-31-\d+\.png)$")
IMAGES = {f"figure-31-{number}.png" for number in range(1, 20)}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 31 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-31/{match.group(1)}"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=412,
            chapter_number=31,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 31 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 31 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"31.{number}" for number in range(1, 4)]:
        raise ValueError(f"Chapter 31 sections missing or out of order: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(31.{number})" for number in range(1, 35)]:
        raise ValueError(f"Chapter 31 formulas missing or out of order: {numbered}")
    unnumbered = [block for block in blocks
                  if block["kind"] == "formula" and not block["number"]]
    if unnumbered:
        raise ValueError(f"Unexpected unnumbered display formulas: {unnumbered}")
    exercises = [block for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"31\.\d+", block["label"]).group()
                        for block in exercises]
    if exercise_numbers != ["31.1", "31.2", "31.3"]:
        raise ValueError(f"Chapter 31 exercises missing or out of order: {exercise_numbers}")
    recommended = [block["label"] for block in exercises if block.get("recommendedIcon")]
    if recommended != ["习题 31.3"]:
        raise ValueError(f"Exercise 31.3 source rat icon is missing: {recommended}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    figure_names = [Path(block["src"]).name for block in figures]
    if figure_names != [f"figure-31-{number}.png" for number in range(1, 20)]:
        raise ValueError(f"Chapter 31 figure order incorrect: {figure_names}")
    for block in figures:
        if block["width"] >= 800:
            block["wide"] = True
    if any(block["kind"] in {"code", "table"} for block in blocks):
        raise ValueError("Source chapter 31 has no code or table")
    toc = [{"number": "31", "title": "Ising 模型", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [412, 424],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbered)} numbered formulas, {len(figures)} figures, "
          f"{len(exercises)} exercises")


if __name__ == "__main__":
    main()
