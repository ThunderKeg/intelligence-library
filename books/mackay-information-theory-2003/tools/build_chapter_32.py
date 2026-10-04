"""Compile the page-checked MacKay chapter 32 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_32", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-32"
ASSETS = BOOK / "assets" / "chapter-32"
OUTPUT = BOOK / "chapter-32.draft.json"
PAGES = range(425, 434)
HEADING = re.compile(r"^(32\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-32/([\w.-]+\.png)$")
IMAGES = [
    "figure-32-1.png",
    "figure-32-2.png",
    "figure-32-3.png",
    "algorithm-32-4.png",
    "figure-32-5.png",
    "figure-32-6.png",
]


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 32 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-32/{match.group(1)}"


def attach_algorithm_caption(blocks: list[dict]) -> None:
    matches = [index for index, block in enumerate(blocks)
               if block["kind"] == "figure" and block["src"].endswith("algorithm-32-4.png")]
    if len(matches) != 1:
        raise ValueError(f"Algorithm 32.4 image missing or duplicated: {matches}")
    index = matches[0]
    if index + 1 >= len(blocks):
        raise ValueError("Algorithm 32.4 caption missing")
    caption = blocks[index + 1]
    if caption["kind"] != "paragraph" or not caption["text"].startswith("算法 32.4。"):
        raise ValueError(f"Algorithm 32.4 caption missing: {caption}")
    blocks[index]["caption"] = caption["text"]
    blocks[index]["captionSegments"] = caption["segments"]
    del blocks[index + 1]


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=425,
            chapter_number=32,
        )
    ]
    attach_algorithm_caption(blocks)
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 32 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 32 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"32.{number}" for number in range(1, 6)]:
        raise ValueError(f"Chapter 32 sections missing or out of order: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != ["(32.1)"]:
        raise ValueError(f"Chapter 32 numbered formula missing: {numbered}")
    unnumbered = [block for block in blocks
                  if block["kind"] == "formula" and not block["number"]]
    if len(unnumbered) != 1 or unnumbered[0]["pdfPage"] != 431:
        raise ValueError(f"Chapter 32 summary-state display missing: {unnumbered}")
    exercises = [block for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"32\.\d+", block["label"]).group()
                        for block in exercises]
    if exercise_numbers != [f"32.{number}" for number in range(1, 7)]:
        raise ValueError(f"Chapter 32 exercises missing or out of order: {exercise_numbers}")
    recommended = [block["label"] for block in exercises if block.get("recommendedIcon")]
    if recommended:
        raise ValueError(f"Source chapter 32 has no rat-icon exercises: {recommended}")
    marked = [block["label"] for block in exercises if block["label"].startswith("▷")]
    if marked != [f"▷ 习题 32.{number}" for number in (1, 2, 5)]:
        raise ValueError(f"Chapter 32 triangle exercise markers missing: {marked}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    names = [Path(block["src"]).name for block in figures]
    if names != IMAGES:
        raise ValueError(f"Chapter 32 figures and algorithm missing or out of order: {names}")
    for block in figures:
        if block["width"] >= 800:
            block["wide"] = True
    footnotes = [block for block in blocks if block["kind"] == "footnote"]
    if [block["label"] for block in footnotes] != ["1", "2"]:
        raise ValueError(f"Chapter 32 footnotes missing: {footnotes}")
    if any(block["kind"] in {"table", "code"} for block in blocks):
        raise ValueError("Source chapter 32 has no tables or program code")
    toc = [{"number": "32", "title": "精确蒙特卡罗采样", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [425, 433],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbered)} numbered + {len(unnumbered)} unnumbered formulas, "
          f"{len(figures)} images including algorithm, "
          f"{len(exercises)} exercises, {len(footnotes)} footnotes")


if __name__ == "__main__":
    main()
