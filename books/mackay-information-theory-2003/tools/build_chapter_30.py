"""Compile the page-checked MacKay chapter 30 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_30", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-30"
ASSETS = BOOK / "assets" / "chapter-30"
OUTPUT = BOOK / "chapter-30.draft.json"
PAGES = range(399, 411)
HEADING = re.compile(r"^(30\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-30/([\w.-]+\.png)$")
IMAGES = {
    "figure-30-2.png", "figure-30-3.png", "leapfrog-geometry.png",
    "exercise-30-12-slice-direction.png",
}
EXERCISES = [f"30.{number}" for number in range(1, 13) if number != 4]


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 30 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-30/{match.group(1)}"


def flatten(blocks: list[dict]):
    for block in blocks:
        if block["kind"] == "box":
            yield from flatten(block["blocks"])
        else:
            yield block


def outline_algorithm(blocks: list[dict]) -> list[dict]:
    indices = [index for index, block in enumerate(blocks)
               if block["pdfPage"] == 400 and block["kind"] == "code"]
    if len(indices) != 1:
        raise ValueError(f"Algorithm 30.1 code block missing or duplicated: {indices}")
    index = indices[0]
    code = blocks[index]
    box = {
        "id": "box-30-1",
        "kind": "box",
        "pdfPage": 400,
        "page": 2,
        "outlined": True,
        "blocks": [code],
    }
    return blocks[:index] + [box] + blocks[index + 1:]


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=399, chapter_number=30,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 30 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 30 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"30.{number}" for number in range(1, 10)]:
        raise ValueError(f"Chapter 30 sections missing or out of order: {section_numbers}")
    numbers = [block["number"] for block in blocks
               if block["kind"] == "formula" and block["number"]]
    if numbers != [f"(30.{number})" for number in range(1, 19)]:
        raise ValueError(f"Chapter 30 formulas missing or out of order: {numbers}")
    unnumbered = [block for block in blocks
                  if block["kind"] == "formula" and not block["number"]]
    if len(unnumbered) != 1 or unnumbered[0]["pdfPage"] != 409:
        raise ValueError("PDF409 unnumbered two-line Gaussian density is missing")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"30\.\d+", label).group() for label in exercises]
    if exercise_numbers != EXERCISES:
        raise ValueError(f"Chapter 30 exercises missing or out of order: {exercises}")
    icons = [block for block in blocks if block["kind"] == "exercise"
             and block.get("recommendedIcon")]
    if len(icons) != 1 or icons[0]["label"] != "习题 30.1":
        raise ValueError("Exercise 30.1's source rat icon is missing")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if {Path(block["src"]).name for block in figures} != IMAGES or len(figures) != 4:
        raise ValueError(f"Unexpected chapter 30 image set: {[block['src'] for block in figures]}")
    for block in figures:
        if block["width"] >= 800:
            block["wide"] = True
    code = [block for block in blocks if block["kind"] == "code"]
    if len(code) != 1 or code[0]["pdfPage"] != 400:
        raise ValueError("Algorithm 30.1's source code is missing")
    if any(block["kind"] == "table" for block in blocks):
        raise ValueError("The source chapter has no table")
    toc = [{"number": "30", "title": "高效蒙特卡罗方法", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    blocks = outline_algorithm(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [399, 410],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    visible = list(flatten(blocks))
    print(f"Wrote {OUTPUT}: {len(blocks)} top-level/{len(visible)} visible blocks, "
          f"{len(toc)} TOC entries, {len(numbers)} numbered + {len(unnumbered)} "
          f"unnumbered formulas, {len(figures)} source images, "
          f"{len(exercises)} exercises, 1 outlined algorithm")


if __name__ == "__main__":
    main()
