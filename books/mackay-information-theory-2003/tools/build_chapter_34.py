"""Compile the page-checked MacKay chapter 34 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_34", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-34"
ASSETS = BOOK / "assets" / "chapter-34"
OUTPUT = BOOK / "chapter-34.draft.json"
PAGES = range(449, 457)
HEADING = re.compile(r"^(34\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-34/([\w.-]+\.png)$")
IMAGES = [
    "figure-34-1.png",
    "algorithm-34-2.png",
    "figure-34-3.png",
    "algorithm-34-4.png",
]


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 34 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-34/{match.group(1)}"


def attach_algorithm_captions(blocks: list[dict]) -> None:
    for number in (2, 4):
        name = f"algorithm-34-{number}.png"
        indices = [index for index, block in enumerate(blocks)
                   if block["kind"] == "figure" and block["src"].endswith(name)]
        if len(indices) != 1:
            raise ValueError(f"Algorithm 34.{number} image missing or duplicated: {indices}")
        index = indices[0]
        if index + 1 >= len(blocks):
            raise ValueError(f"Algorithm 34.{number} caption missing")
        caption = blocks[index + 1]
        if caption["kind"] != "paragraph" or not caption["text"].startswith(f"算法 34.{number}。"):
            raise ValueError(f"Algorithm 34.{number} caption missing: {caption}")
        blocks[index]["caption"] = caption["text"]
        blocks[index]["captionSegments"] = caption["segments"]
        del blocks[index + 1]


def group_chapter_title(block: dict) -> None:
    parts = ("第 34 章　", "独立成分分析", "与隐变量建模")
    if block["text"] != "".join(parts):
        raise ValueError(f"Chapter 34 title changed unexpectedly: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch34-title-part">{part}</span>' for part in parts
    ) + "</h1>"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=449,
            chapter_number=34,
        )
    ]
    attach_algorithm_captions(blocks)
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 34 title is missing")
    group_chapter_title(blocks[0])
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 34 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"34.{number}" for number in range(1, 5)]:
        raise ValueError(f"Chapter 34 sections missing or out of order: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(34.{number})" for number in range(1, 31)]:
        raise ValueError(f"Chapter 34 numbered formulas missing or out of order: {numbered}")
    if any(block["kind"] == "formula" and not block["number"] for block in blocks):
        raise ValueError("The source chapter 34 has no unnumbered display equations")
    exercises = [block for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"34\.\d+", block["label"]).group()
                        for block in exercises]
    if exercise_numbers != [f"34.{number}" for number in range(1, 6)]:
        raise ValueError(f"Chapter 34 exercises missing or out of order: {exercise_numbers}")
    if any(block.get("recommendedIcon") or block["label"].startswith("▷")
           for block in exercises):
        raise ValueError("Source chapter 34 has no rat or triangle exercise markers")
    figures = [block for block in blocks if block["kind"] == "figure"]
    names = [Path(block["src"]).name for block in figures]
    if names != IMAGES:
        raise ValueError(f"Chapter 34 images missing or out of order: {names}")
    for block in figures:
        if not block.get("caption"):
            raise ValueError(f"Chapter 34 image caption missing: {block['src']}")
        block["wide"] = True
    lists = [block for block in blocks if block["kind"] == "list"]
    if [len(block["items"]) for block in lists] != [3, 4] or not all(
        block["ordered"] for block in lists
    ):
        raise ValueError("Algorithms 34.2 and 34.4 need their 3 and 4 translated steps")
    if any(block["kind"] in {"code", "table", "footnote", "box"} for block in blocks):
        raise ValueError("Source chapter 34 has no code, table, footnote, or separate box")
    toc = [{"number": "34", "title": "独立成分分析与隐变量建模", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [449, 456],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbered)} numbered formulas, {len(figures)} images including 2 algorithms, "
          f"{len(exercises)} exercises")


if __name__ == "__main__":
    main()
